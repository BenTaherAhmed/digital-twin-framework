from __future__ import annotations
import simpy
from .base import Component

class Server(Component):
    def __init__(self, name: str, inp: simpy.Store, out: simpy.Store, capacity: int, service_time_fn, metrics: dict):
        super().__init__(name)
        self.inp = inp
        self.out = out
        self.capacity = capacity
        self.service_time_fn = service_time_fn
        self.metrics = metrics

    def build(self, engine) -> None:
        resource = simpy.Resource(engine.env, capacity=self.capacity)

        def run():
            while True:
                entity = yield self.inp.get()
                with resource.request() as req:
                    yield req

                    # waiting time (if queue timestamp exists)
                    q_enter = entity.get("queue_enter_at", entity["created_at"])
                    wait = engine.now - q_enter

                    st = self.service_time_fn()
                    self.metrics["busy_time"] += st

                    yield engine.timeout(st)

                    self.metrics["completed"] += 1
                    self.metrics["wait_times"].append(wait)
                    self.metrics["system_times"].append(engine.now - entity["created_at"])

                    yield self.out.put(entity)

        engine.process(run())
