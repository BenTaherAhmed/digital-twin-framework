from dtfw.scenarios.routing_demo_v2 import run, RoutingV2Config

if __name__ == "__main__":
    cfg = RoutingV2Config(
        sim_time=300,
        seed=42,
        warmup_time=50,
        drop_policy="drop",
    )
    out = run(cfg)
    print(out)
