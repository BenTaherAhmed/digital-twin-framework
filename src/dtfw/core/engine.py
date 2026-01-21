import simpy
import random
from typing import Optional


class Engine:
    def __init__(self, *, seed: Optional[int] = None):
        self.env = simpy.Environment()
        self.seed = seed
        self.rng = random.Random(seed)  # RNG local à l'engine

    @property
    def now(self) -> float:
        return self.env.now

    def process(self, generator):
        return self.env.process(generator)

    def timeout(self, delay: float):
        return self.env.timeout(delay)

    def run(self, until: Optional[float] = None):
        self.env.run(until=until)
