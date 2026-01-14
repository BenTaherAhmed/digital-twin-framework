# Engine

The Engine is the core of the Digital Twin Framework.
It wraps a SimPy environment and ensures reproducible simulations.

## Responsibilities
- Time management
- Process scheduling
- Random seed control

## Usage
```python
engine = Engine(seed=42)
engine.process(my_process())
engine.run(until=100)