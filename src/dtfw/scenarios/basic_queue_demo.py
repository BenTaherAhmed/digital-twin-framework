import random
import statistics
import simpy


class Metrics:
    def __init__(self):
        self.wait_times = []
        self.system_times = []
        self.completed = 0
        self.busy_time = 0.0

    def report(self, sim_time: float, capacity: int):
        rep = {"completed": self.completed}
        if self.completed > 0:
            rep["avg_wait"] = statistics.mean(self.wait_times)
            rep["avg_system_time"] = statistics.mean(self.system_times)
        else:
            rep["avg_wait"] = None
            rep["avg_system_time"] = None

        rep["utilization"] = min(1.0, self.busy_time / (capacity * sim_time)) if sim_time > 0 else 0.0
        return rep


class Job:
    def __init__(self, jid: int, created_at: float):
        self.jid = jid
        self.created_at = created_at
        self.enter_queue_at = None


def run_basic_queue_demo(
    *,
    seed: int = 42,
    sim_time: int = 300,
    capacity: int = 2,
    arrival_rate: float = 0.9,
    service_rate: float = 1.0,
):
    random.seed(seed)
    env = simpy.Environment()
    metrics = Metrics()

    s_in = simpy.Store(env)
    s_q = simpy.Store(env)
    s_out = simpy.Store(env)

    def interarrival():
        return random.expovariate(arrival_rate)

    def service_time():
        return random.expovariate(service_rate)

    def source():
        jid = 0
        while env.now < sim_time:
            yield env.timeout(interarrival())
            yield s_in.put(Job(jid, env.now))
            jid += 1

    def queue():
        while True:
            job = yield s_in.get()
            job.enter_queue_at = env.now
            yield s_q.put(job)

    resource = simpy.Resource(env, capacity=capacity)

    def server():
        while True:
            job = yield s_q.get()
            with resource.request() as req:
                yield req
                wait = env.now - (job.enter_queue_at or job.created_at)

                st = service_time()
                metrics.busy_time += st
                yield env.timeout(st)

                metrics.wait_times.append(wait)
                metrics.system_times.append(env.now - job.created_at)
                metrics.completed += 1
                yield s_out.put(job)

    def sink():
        while True:
            _ = yield s_out.get()

    env.process(source())
    env.process(queue())
    env.process(server())
    env.process(sink())
    env.run(until=sim_time)

    rep = metrics.report(sim_time=sim_time, capacity=capacity)
    rep.update(sim_time=sim_time, capacity=capacity, arrival_rate=arrival_rate, service_rate=service_rate)
    return rep
