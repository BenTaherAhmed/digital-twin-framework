from dtfw.scenarios.routing_demo import run


def test_routing_demo_runs():
    out = run(sim_time=50, seed=123)
    assert "total_completed" in out
    assert "drops" in out
    assert "fast" in out and "slow" in out


def test_routing_demo_reproducible():
    a = run(sim_time=80, seed=42)
    b = run(sim_time=80, seed=42)
    assert a["total_completed"] == b["total_completed"]
    assert a["drops"] == b["drops"]
    assert a["fast"]["completed"] == b["fast"]["completed"]
