from __future__ import annotations

import simpy

from .base import Component


class Sink(Component):
    def __init__(self, name: str, inp: simpy.Store):
        super().__init__(name)
        self.inp = inp

    def build(self, engine) -> None:
        def run():
            while True:
                _ = yield self.inp.get()

        engine.process(run())
