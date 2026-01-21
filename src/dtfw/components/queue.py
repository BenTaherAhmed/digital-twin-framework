from __future__ import annotations

import simpy

from .base import Component


class Queue(Component):
    def __init__(self, name: str, inp: simpy.Store, out: simpy.Store):
        super().__init__(name)
        self.inp = inp
        self.out = out

    def build(self, engine) -> None:
        def run():
            while True:
                entity = yield self.inp.get()
                entity["queue_enter_at"] = engine.now
                yield self.out.put(entity)

        engine.process(run())
