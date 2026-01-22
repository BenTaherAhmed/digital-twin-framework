from dtfw.scenarios.routing_demo_v2 import run, RoutingV2Config


def test_routing_v2_runs():
    out = run(RoutingV2Config(sim_time=60, seed=123, warmup_time=10, drop_policy="drop"))
    assert "total_completed" in out
    assert out["total_completed"] >= 0


def test_routing_v2_reproducible():
    a = run(RoutingV2Config(sim_time=80, seed=42, warmup_time=10))
    b = run(RoutingV2Config(sim_time=80, seed=42, warmup_time=10))
    assert a["total_completed"] == b["total_completed"]
    assert a["drops"] == b["drops"]
