from __future__ import annotations

import simpy
import random


class Engine:
    def __init__(self, seed: int | None = None):
        self.env = simpy.Environment()
        self.seed = seed
        self.rng = random.Random(seed)

    @property
    def now(self) -> float:
        return self.env.now

    def timeout(self, delay: float):
        return self.env.timeout(delay)

    def process(self, proc):
        return self.env.process(proc)

    def run(self, until: float):
        self.env.run(until=until)
