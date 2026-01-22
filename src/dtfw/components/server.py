from __future__ import annotations

import simpy
from .base import Component


class Server(Component):
    def __init__(
        self,
        name: str,
        inp: simpy.Store,
        out: simpy.Store,
        capacity: int,
        service_time_fn,
        recorder=None,
        metrics=None,
    ):
        super().__init__(name)
        self.inp = inp
        self.out = out
        self.capacity = capacity
        self.service_time_fn = service_time_fn
        self.recorder = recorder
        self.metrics = metrics

    def build(self, engine) -> None:
        resource = simpy.Resource(engine.env, capacity=self.capacity)

        def run():
            while True:
                entity = yield self.inp.get()
                with resource.request() as req:
                    yield req

                    st = self.service_time_fn()

                    # busy time
                    if self.recorder is not None:
                        self.recorder.busy_time += st
                    if self.metrics is not None:
                        self.metrics["busy_time"] += st

                    yield engine.timeout(st)

                    # completed + wait/system times
                    if isinstance(entity, dict):
                        created = entity.get("created_at", engine.now)
                        q_enter = entity.get("queue_enter_at", created)
                        wait = engine.now - q_enter
                        system = engine.now - created
                    else:
                        wait = 0.0
                        system = 0.0

                    if self.recorder is not None:
                        self.recorder.completed += 1
                        self.recorder.wait_times.append(wait)
                        self.recorder.system_times.append(system)

                    if self.metrics is not None:
                        self.metrics["completed"] += 1
                        self.metrics["wait_times"].append(wait)
                        self.metrics["system_times"].append(system)

                    yield self.out.put(entity)

        engine.process(run())
