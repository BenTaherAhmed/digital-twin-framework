from dtfw.scenarios.components_demo import run

def test_components_demo_runs():
    metrics = run(sim_time=20)
    assert "completed" in metrics
