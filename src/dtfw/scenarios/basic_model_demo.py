import random
import simpy

from dtfw.core.engine import Engine
from dtfw.core.model import Model
from dtfw.components.source import Source
from dtfw.components.server import Server


def run():
    engine = Engine(seed=42)
    env = engine.env

    metrics = {"completed": 0}

    s0 = simpy.Store(env)
    s1 = simpy.Store(env)

    model = Model(engine)

    model.add(
        Source(
            "source",
            s0,
            interarrival_fn=lambda: random.expovariate(0.9),
        )
    )

    model.add(
        Server(
            "server",
            s0,
            s1,
            capacity=2,
            service_time_fn=lambda: random.expovariate(1.0),
            metrics=metrics,
        )
    )

    model.build()
    engine.run(until=300)

    print(metrics)
