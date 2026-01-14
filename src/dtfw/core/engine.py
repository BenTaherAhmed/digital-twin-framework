import simpy
import random
from typing import Optional


class Engine:
    """
    Simulation engine wrapping SimPy environment.
    Responsible for time, scheduling and reproducibility.
    """

    def __init__(self, *, seed: Optional[int] = None):
        self.env = simpy.Environment()
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    @property
    def now(self) -> float:
        """Current simulation time"""
        return self.env.now

    def process(self, generator):
        """Register a SimPy process"""
        return self.env.process(generator)

    def timeout(self, delay: float):
        """Create a timeout event"""
        return self.env.timeout(delay)

    def run(self, until: Optional[float] = None):
        """Run the simulation"""
        self.env.run(until=until)
