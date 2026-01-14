<<<<<<< HEAD
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Component:
    name: str

    def build(self, engine) -> None:
        """Register SimPy processes/events into the engine."""
=======
class Component:
    def __init__(self, name: str):
        self.name = name

    def build(self, engine):
        """
        Register processes inside the engine
        """
>>>>>>> feature/engine-core
        raise NotImplementedError
