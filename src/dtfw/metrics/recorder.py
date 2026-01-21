from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any
import math


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]

    k = (len(xs) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return xs[int(k)]

    return xs[f] + (xs[c] - xs[f]) * (k - f)


@dataclass
class MetricsRecorder:
    wait_times: List[float] = field(default_factory=list)
    system_times: List[float] = field(default_factory=list)
    completed: int = 0
    busy_time: float = 0.0

    def summary(self, *, sim_time: float, capacity: int | None = None) -> Dict[str, Any]:
        throughput = self.completed / sim_time if sim_time > 0 else 0.0

        utilization = None
        if capacity is not None and sim_time > 0:
            utilization = self.busy_time / (capacity * sim_time)

        return {
            "completed": self.completed,
            "throughput": throughput,
            "avg_wait": sum(self.wait_times) / len(self.wait_times) if self.wait_times else 0.0,
            "p95_wait": percentile(self.wait_times, 95),
            "avg_system": sum(self.system_times) / len(self.system_times) if self.system_times else 0.0,
            "p95_system": percentile(self.system_times, 95),
            "utilization": utilization,
        }
