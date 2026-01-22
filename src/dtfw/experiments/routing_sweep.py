from __future__ import annotations

from dataclasses import asdict
import json
import csv
from pathlib import Path

from dtfw.scenarios.routing_demo_v2 import run, RoutingV2Config


def sweep(
    out_dir: str = "artifacts",
    seeds: list[int] | None = None,
    p_fasts: list[float] | None = None,
    drop_policies: list[str] | None = None,
):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    seeds = seeds or [42, 43, 44]
    p_fasts = p_fasts or [0.2, 0.5, 0.8]  # (on gardera p_fast si tu l’ajoutes dans v2 plus tard)
    drop_policies = drop_policies or ["drop", "block"]

    rows = []

    # Ici on varie surtout policy + seed.
    # (Ton routing v2 est adaptatif; si tu veux re-introduire un p_fast hybride, on le fera ensuite.)
    for policy in drop_policies:
        for seed in seeds:
            cfg = RoutingV2Config(
                sim_time=300,
                seed=seed,
                warmup_time=30,
                drop_policy=policy,
            )

            out = run(cfg)

            row = {
                "seed": seed,
                "drop_policy": policy,
                "total_completed": out["total_completed"],
                "drops": out["drops"],

                # fast KPIs
                "fast_completed": out["fast"]["completed"],
                "fast_throughput": out["fast"]["throughput"],
                "fast_avg_wait": out["fast"]["avg_wait"],
                "fast_p95_system": out["fast"]["p95_system"],
                "fast_util": out["fast"]["utilization"],

                # slow KPIs
                "slow_completed": out["slow"]["completed"],
                "slow_throughput": out["slow"]["throughput"],
                "slow_avg_wait": out["slow"]["avg_wait"],
                "slow_p95_system": out["slow"]["p95_system"],
                "slow_util": out["slow"]["utilization"],
            }

            rows.append(row)

    # Console table
    print("seed | policy | completed | drops | fast_util | slow_util | slow_p95")
    print("-" * 75)
    for r in rows:
        print(
            f"{r['seed']:>4} | {r['drop_policy']:<6} | {r['total_completed']:>9} | {r['drops']:>5} | "
            f"{r['fast_util']:.2f}     | {r['slow_util']:.2f}    | {r['slow_p95_system']:.2f}"
        )

    # Export JSON
    json_file = out_path / "routing_sweep.json"
    json_file.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    # Export CSV
    csv_file = out_path / "routing_sweep.csv"
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return rows, str(json_file), str(csv_file)


if __name__ == "__main__":
    sweep()
