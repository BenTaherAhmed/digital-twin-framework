from __future__ import annotations

import random
import simpy

from dtfw.core.engine import Engine
from dtfw.components.source import Source
from dtfw.components.queue import Queue
from dtfw.components.server import Server
from dtfw.components.sink import Sink
from dtfw.metrics.recorder import MetricsRecorder


def run(sim_time: int = 300, capacity: int = 2, arrival_rate: float = 0.9, service_rate: float = 1.0, seed: int = 42):
    engine = Engine(seed=seed)
    env = engine.env

    s0 = simpy.Store(env)
    s1 = simpy.Store(env)
    s2 = simpy.Store(env)

    rec = MetricsRecorder()

    # ⚠️ IMPORTANT: use engine-local RNG for reproducibility
    interarrival_fn = lambda: engine.rng.expovariate(arrival_rate)
    service_time_fn = lambda: engine.rng.expovariate(service_rate)

    src = Source("src", s0, interarrival_fn=interarrival_fn)
    q = Queue("q", s0, s1)
    srv = Server("srv", s1, s2, capacity=capacity, service_time_fn=service_time_fn, recorder=rec)
    snk = Sink("snk", s2)

    src.build(engine)
    q.build(engine)
    srv.build(engine)
    snk.build(engine)

    engine.run(until=sim_time)

    return rec.summary(sim_time=sim_time, capacity=capacity)


if __name__ == "__main__":
    out = run()
    print("=== Components Demo Metrics ===")
    for k, v in out.items():
        print(f"{k}: {v}")
