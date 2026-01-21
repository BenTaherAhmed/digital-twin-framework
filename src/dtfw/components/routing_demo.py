from __future__ import annotations

import simpy

from dtfw.core.engine import Engine
from dtfw.components.source import Source
from dtfw.components.queue import Queue
from dtfw.components.router import Router
from dtfw.components.server import Server
from dtfw.components.sink import Sink
from dtfw.metrics.recorder import MetricsRecorder


def run(
    sim_time: int = 300,
    seed: int = 42,
    arrival_rate: float = 0.95,
    p_fast: float = 0.6,
    capacity_in: int = 50,
    fast_capacity: int = 2,
    slow_capacity: int = 1,
    fast_service_rate: float = 1.4,
    slow_service_rate: float = 0.7,
):
    engine = Engine(seed=seed)
    env = engine.env

    # Stores
    # Queue d’entrée limitée (si full => drop)
    in_store = simpy.Store(env, capacity=capacity_in)
    q_to_router = simpy.Store(env)

    to_fast = simpy.Store(env)
    to_slow = simpy.Store(env)

    out_fast = simpy.Store(env)
    out_slow = simpy.Store(env)

    # Metrics
    rec_fast = MetricsRecorder()
    rec_slow = MetricsRecorder()

    drops = {"count": 0}

    def try_put_with_drop(store: simpy.Store, item) -> bool:
        # simpy.Store with capacity: if full => len(items) >= capacity
        cap = getattr(store, "capacity", None)
        if cap is not None and len(store.items) >= cap:
            drops["count"] += 1
            return False
        store.put(item)
        return True

    # Source (reproducible RNG)
    interarrival_fn = lambda: engine.rng.expovariate(arrival_rate)

    def make_entity_fn(i, t):
        return {"id": i, "created_at": t}

    class DroppingSource(Source):
        def build(self, engine) -> None:
            def run():
                i = 0
                while True:
                    yield engine.timeout(self.interarrival_fn())
                    entity = self.make_entity_fn(i, engine.now)
                    try_put_with_drop(self.out, entity)
                    i += 1

            engine.process(run())

    src = DroppingSource("src", in_store, interarrival_fn=interarrival_fn, make_entity_fn=make_entity_fn)

    # Queue stamps queue_enter_at (for wait KPI)
    q = Queue("q_in", in_store, q_to_router)

    # Router: True -> fast, False -> slow
    route_fn = lambda eng, ent: (eng.rng.random() < p_fast)
    r = Router("router", q_to_router, to_fast, to_slow, route_fn=route_fn)

    # Servers
    fast_service_time_fn = lambda: engine.rng.expovariate(fast_service_rate)
    slow_service_time_fn = lambda: engine.rng.expovariate(slow_service_rate)

    srv_fast = Server("srv_fast", to_fast, out_fast, capacity=fast_capacity, service_time_fn=fast_service_time_fn, recorder=rec_fast)
    srv_slow = Server("srv_slow", to_slow, out_slow, capacity=slow_capacity, service_time_fn=slow_service_time_fn, recorder=rec_slow)

    # Sinks
    snk_fast = Sink("snk_fast", out_fast)
    snk_slow = Sink("snk_slow", out_slow)

    # Build
    for c in (src, q, r, srv_fast, srv_slow, snk_fast, snk_slow):
        c.build(engine)

    engine.run(until=sim_time)

    fast = rec_fast.summary(sim_time=sim_time, capacity=fast_capacity)
    slow = rec_slow.summary(sim_time=sim_time, capacity=slow_capacity)

    total_completed = fast["completed"] + slow["completed"]
    total_throughput = total_completed / sim_time if sim_time > 0 else 0.0

    return {
        "total_completed": total_completed,
        "total_throughput": total_throughput,
        "drops": drops["count"],
        "fast": fast,
        "slow": slow,
        "config": {
            "sim_time": sim_time,
            "arrival_rate": arrival_rate,
            "p_fast": p_fast,
            "capacity_in": capacity_in,
            "fast_capacity": fast_capacity,
            "slow_capacity": slow_capacity,
        },
    }


if __name__ == "__main__":
    out = run()
    print("=== Routing Demo Metrics ===")
    print(out)
