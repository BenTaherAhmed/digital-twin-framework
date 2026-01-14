import random
import simpy
from .base import Component


class Source(Component):
    def __init__(self, name, out_store, interarrival_fn):
        super().__init__(name)
        self.out = out_store
        self.interarrival_fn = interarrival_fn

    def build(self, engine):
        def run():
            i = 0
            while True:
                yield engine.env.timeout(self.interarrival_fn())
                yield self.out.put(i)
                i += 1

        engine.process(run())
