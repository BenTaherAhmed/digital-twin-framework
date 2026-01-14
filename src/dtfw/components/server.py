import simpy
from .base import Component


class Server(Component):
    def __init__(self, name, in_store, out_store, capacity, service_time_fn, metrics):
        super().__init__(name)
        self.inp = in_store
        self.out = out_store
        self.capacity = capacity
        self.service_time_fn = service_time_fn
        self.metrics = metrics

    def build(self, engine):
        resource = simpy.Resource(engine.env, capacity=self.capacity)

        def run():
            while True:
                job = yield self.inp.get()
                with resource.request() as req:
                    yield req
                    st = self.service_time_fn()
                    yield engine.env.timeout(st)
                    yield self.out.put(job)
                    self.metrics["completed"] += 1

        engine.process(run())
