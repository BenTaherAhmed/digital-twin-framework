from __future__ import annotations

import simpy
from .base import Component


class Router(Component):
    """
    Route entities from inp to out_a or out_b based on a routing function.
    route_fn(engine, entity) -> bool
      True  -> out_a
      False -> out_b
    """
    def __init__(self, name: str, inp: simpy.Store, out_a: simpy.Store, out_b: simpy.Store, route_fn):
        super().__init__(name)
        self.inp = inp
        self.out_a = out_a
        self.out_b = out_b
        self.route_fn = route_fn

    def build(self, engine) -> None:
        def run():
            while True:
                entity = yield self.inp.get()
                if self.route_fn(engine, entity):
                    yield self.out_a.put(entity)
                else:
                    yield self.out_b.put(entity)

        engine.process(run())
