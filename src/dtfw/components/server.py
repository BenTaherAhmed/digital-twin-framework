from __future__ import annotations

import simpy

from .base import Component
from dtfw.metrics.recorder import MetricsRecorder


class Server(Component):
    def __init__(
        self,
        name: str,
        inp: simpy.Store,
        out: simpy.Store,
        capacity: int,
        service_time_fn,
        recorder: MetricsRecorder,
    ):
        super().__init__(name)
        self.inp = inp
        self.out = out
        self.capacity = capacity
        self.service_time_fn = service_time_fn
        self.recorder = recorder

    def build(self, engine) -> None:
        resource = simpy.Resource(engine.env, capacity=self.capacity)

        def run():
            while True:
                entity = yield self.inp.get()
                with resource.request() as req:
                    yield req

                    q_enter = entity.get("queue_enter_at", entity["created_at"])
                    wait = engine.now - q_enter

                    st = self.service_time_fn()
                    self.recorder.busy_time += st

                    yield engine.timeout(st)

                    self.recorder.completed += 1
                    self.recorder.wait_times.append(wait)
                    self.recorder.system_times.append(engine.now - entity["created_at"])

                    yield self.out.put(entity)

        engine.process(run())
