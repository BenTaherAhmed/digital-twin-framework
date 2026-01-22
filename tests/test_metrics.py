from dtfw.metrics.recorder import MetricsRecorder


def test_metrics_summary_keys():
    rec = MetricsRecorder()
    rec.completed = 10
    rec.busy_time = 5.0
    rec.wait_times = [1.0, 2.0, 3.0]
    rec.system_times = [2.0, 3.0, 4.0]

    s = rec.summary(sim_time=10.0, capacity=2)

    expected = {"completed", "throughput", "avg_wait", "p95_wait", "avg_system", "p95_system", "utilization"}
    assert expected.issubset(set(s.keys()))
