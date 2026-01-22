from dtfw.experiments.routing_sweep import sweep


def test_sweep_runs(tmp_path):
    rows, jf, cf = sweep(out_dir=str(tmp_path), seeds=[1], drop_policies=["drop"])
    assert len(rows) == 1
