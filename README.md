# Digital Twin Framework (dtfw)

A lightweight, component-based **discrete-event simulation** framework in Python (SimPy),
built to experiment with complex systems (queues, routing, capacity constraints, drops) and extract performance KPIs.

## Features
- **Engine** wrapper with reproducible RNG (seeded)
- Reusable components: `Source`, `Queue`, `Router`, `Server`, `Sink`
- Metrics: throughput, avg/p95 wait time, avg/p95 system time, utilization
- Advanced scenarios:
  - `components_demo`
  - `routing_demo` (fast/slow paths, multi-servers, drops)
  - `routing_demo_v2` (warm-up, adaptive routing, drop policy)
- Tests with `pytest`

## Installation
```bash
pip install -e .[dev]

## 🚀 Quick Start

```bash
git clone https://github.com/BenTaherAhmed/digital-twin-framework
cd digital-twin-framework
pip install -e .
pytest




