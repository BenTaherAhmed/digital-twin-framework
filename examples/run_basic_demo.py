from dtfw.scenarios.basic_queue_demo import run_basic_queue_demo

if __name__ == "__main__":
    result = run_basic_queue_demo(sim_time=300, capacity=2, arrival_rate=0.9, service_rate=1.0)
    print("=== Basic Queue Demo Results ===")
    for k, v in result.items():
        print(f"{k}: {v}")
