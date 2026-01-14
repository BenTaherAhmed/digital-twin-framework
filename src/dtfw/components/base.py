from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Component:
    name: str

    def build(self, engine) -> None:
        """Register SimPy processes/events into the engine."""
        raise NotImplementedError
