<<<<<<< HEAD
from __future__ import annotations
import simpy
from .base import Component

class Source(Component):
    def __init__(self, name: str, out: simpy.Store, interarrival_fn, make_entity_fn=None):
        super().__init__(name)
        self.out = out
        self.interarrival_fn = interarrival_fn
        self.make_entity_fn = make_entity_fn or (lambda i, t: {"id": i, "created_at": t})

    def build(self, engine) -> None:
        def run():
            i = 0
            while True:
                yield engine.timeout(self.interarrival_fn())
                entity = self.make_entity_fn(i, engine.now)
                yield self.out.put(entity)
=======
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
>>>>>>> feature/engine-core
                i += 1

        engine.process(run())
