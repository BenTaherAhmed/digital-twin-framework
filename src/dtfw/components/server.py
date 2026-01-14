<<<<<<< HEAD
from __future__ import annotations
import simpy
from .base import Component

class Server(Component):
    def __init__(self, name: str, inp: simpy.Store, out: simpy.Store, capacity: int, service_time_fn, metrics: dict):
        super().__init__(name)
        self.inp = inp
        self.out = out
=======
import simpy
from .base import Component


class Server(Component):
    def __init__(self, name, in_store, out_store, capacity, service_time_fn, metrics):
        super().__init__(name)
        self.inp = in_store
        self.out = out_store
>>>>>>> feature/engine-core
        self.capacity = capacity
        self.service_time_fn = service_time_fn
        self.metrics = metrics

<<<<<<< HEAD
    def build(self, engine) -> None:
=======
    def build(self, engine):
>>>>>>> feature/engine-core
        resource = simpy.Resource(engine.env, capacity=self.capacity)

        def run():
            while True:
<<<<<<< HEAD
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
=======
                job = yield self.inp.get()
                with resource.request() as req:
                    yield req
                    st = self.service_time_fn()
                    yield engine.env.timeout(st)
                    yield self.out.put(job)
                    self.metrics["completed"] += 1
>>>>>>> feature/engine-core

        engine.process(run())
