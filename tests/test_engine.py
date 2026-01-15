from dtfw.core.engine import Engine


def test_engine_time_advances():
    engine = Engine()

    def proc():
        yield engine.timeout(5)

    engine.process(proc())
    engine.run()

    assert engine.now == 5


def test_engine_reproducibility():
    e1 = Engine(seed=42)
    e2 = Engine(seed=42)

    assert e1.rng.random() == e2.rng.random()
    assert e1.rng.random() == e2.rng.random()
