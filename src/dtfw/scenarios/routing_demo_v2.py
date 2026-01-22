from __future__ import annotations

from dataclasses import dataclass
import simpy

from dtfw.core.engine import Engine
from dtfw.components.source import Source
from dtfw.components.queue import Queue
from dtfw.components.router import Router
from dtfw.components.server import Server
from dtfw.metrics.recorder import MetricsRecorder


@dataclass(frozen=True)
class RoutingV2Config:
    sim_time: int = 300
    seed: int = 42

    arrival_rate: float = 0.95
    capacity_in: int = 50

    fast_capacity: int = 2
    slow_capacity: int = 1

    fast_service_rate: float = 1.4
    slow_service_rate: float = 0.7

    warmup_time: int = 30
    drop_policy: str = "drop"  # "drop" | "block"


def run(config: RoutingV2Config = RoutingV2Config()):
    engine = Engine(seed=config.seed)
    env = engine.env

    # Stores
    in_store = simpy.Store(env, capacity=config.capacity_in)
    q_to_router = simpy.Store(env)

    to_fast = simpy.Store(env)
    to_slow = simpy.Store(env)

    out_fast = simpy.Store(env)
    out_slow = simpy.Store(env)

    # Metrics recorders
    rec_fast = MetricsRecorder(warmup_time=config.warmup_time)
    rec_slow = MetricsRecorder(warmup_time=config.warmup_time)

    drops = {"count": 0}

    def can_put(store: simpy.Store) -> bool:
        cap = getattr(store, "capacity", None)
        return (cap is None) or (len(store.items) < cap)

    # Source (reproducible RNG)
    interarrival_fn = lambda: engine.rng.expovariate(config.arrival_rate)

    def make_entity_fn(i, t):
        return {"id": i, "created_at": t}

    class EntrySource(Source):
        def build(self, engine) -> None:
            def proc():
                i = 0
                while True:
                    yield engine.timeout(self.interarrival_fn())
                    entity = self.make_entity_fn(i, engine.now)

                    if config.drop_policy == "drop":
                        if can_put(self.out):
                            self.out.put(entity)
                        else:
                            drops["count"] += 1
                    elif config.drop_policy == "block":
                        # on attend qu'il y ait de la place
                        while not can_put(self.out):
                            yield engine.timeout(0.1)
                        yield self.out.put(entity)
                    else:
                        raise ValueError("drop_policy must be 'drop' or 'block'")

                    i += 1

            engine.process(proc())

    src = EntrySource("src", in_store, interarrival_fn=interarrival_fn, make_entity_fn=make_entity_fn)

    # Queue stamps queue_enter_at (for wait KPI)
    q = Queue("q_in", in_store, q_to_router)

    # Adaptive routing: choose the less loaded path (normalized by capacity)
    def route_fn(eng, ent) -> bool:
        fast_load = (len(to_fast.items) / max(1, config.fast_capacity))
        slow_load = (len(to_slow.items) / max(1, config.slow_capacity))
        return fast_load <= slow_load  # True->fast, False->slow

    r = Router("router", q_to_router, to_fast, to_slow, route_fn=route_fn)

    # Servers
    fast_service_time_fn = lambda: engine.rng.expovariate(config.fast_service_rate)
    slow_service_time_fn = lambda: engine.rng.expovariate(config.slow_service_rate)

    srv_fast = Server("srv_fast", to_fast, out_fast, capacity=config.fast_capacity, service_time_fn=fast_service_time_fn, recorder=rec_fast)
    srv_slow = Server("srv_slow", to_slow, out_slow, capacity=config.slow_capacity, service_time_fn=slow_service_time_fn, recorder=rec_slow)

    # Build graph
    for comp in (src, q, r, srv_fast, srv_slow):
        comp.build(engine)

    # Run
    engine.run(until=config.sim_time)

    # Summary
    return {
        "total_completed": rec_fast.completed + rec_slow.completed,
        "drops": drops["count"],
        "fast": rec_fast.summary(),
        "slow": rec_slow.summary(),
        "config": config.__dict__,
    }
