from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict
import math


@dataclass
class MetricsRecorder:
    warmup_time: float = 0.0
    completed: int = 0
    busy_time: float = 0.0
    wait_times: List[float] = field(default_factory=list)
    system_times: List[float] = field(default_factory=list)

    def record(self, *, now: float, wait: float, system: float, service: float) -> None:
        """
        Record one completed entity.
        If now < warmup_time, ignore it (warm-up period).
        """
        if now < self.warmup_time:
            return

        self.completed += 1
        self.busy_time += float(service)
        self.wait_times.append(float(wait))
        self.system_times.append(float(system))

    def _percentile(self, values: List[float], p: float) -> float:
        if not values:
            return 0.0
        values_sorted = sorted(values)
        k = (len(values_sorted) - 1) * p
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return float(values_sorted[int(k)])
        d0 = values_sorted[int(f)] * (c - k)
        d1 = values_sorted[int(c)] * (k - f)
        return float(d0 + d1)

    def summary(self, *, sim_time: float | None = None, capacity: int | None = None) -> Dict[str, float]:
        avg_wait = (sum(self.wait_times) / len(self.wait_times)) if self.wait_times else 0.0
        avg_system = (sum(self.system_times) / len(self.system_times)) if self.system_times else 0.0

        out: Dict[str, float] = {
            "completed": float(self.completed),
            "throughput": float(self.completed / sim_time) if sim_time is not None and sim_time > 0 else 0.0, 
            "avg_wait": float(avg_wait),
            "p95_wait": float(self._percentile(self.wait_times, 0.95)),
            "avg_system": float(avg_system),
            "p95_system": float(self._percentile(self.system_times, 0.95)),
        }

        # Optional utilization if sim_time and capacity are provided
        if sim_time is not None and capacity is not None and sim_time > 0:
            out["utilization"] = float(self.busy_time / (sim_time * max(1, capacity)))
        else:
            out["utilization"] = 0.0

        return out
