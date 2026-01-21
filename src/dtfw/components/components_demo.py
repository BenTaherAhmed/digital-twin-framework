import random
import simpy
from dtfw.core.engine import Engine
from dtfw.components.source import Source
from dtfw.components.queue import Queue
from dtfw.components.server import Server
from dtfw.components.sink import Sink


def run(sim_time: int = 300):
    engine = Engine(seed=42)
    env = engine.env

    s0 = simpy.Store(env)
    s1 = simpy.Store(env)
    s2 = simpy.Store(env)

    metrics = {"completed": 0, "busy_time": 0.0, "wait_times": [], "system_times": []}

    src = Source("src", s0, interarrival_fn=lambda: random.expovariate(0.9))
    q = Queue("q", s0, s1)
    srv = Server("srv", s1, s2, capacity=2, service_time_fn=lambda: random.expovariate(1.0), metrics=metrics)
    snk = Sink("snk", s2)

    src.build(engine)
    q.build(engine)
    srv.build(engine)
    snk.build(engine)

    engine.run(until=sim_time)
    return metrics


if __name__ == "__main__":
    m = run()
    print(m["completed"])
