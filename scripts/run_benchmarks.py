"""
Benchmarking harness: runs all solvers on all instances and records results.

Usage:
    python scripts/run_benchmarks.py [--solvers all] [--scales all] [--seeds 42]
                                      [--time-limit 30] [--output results/baseline_results.csv]
"""

import sys
import os
import json
import csv
import time
import argparse
import signal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.data_pipeline import load_instance
from src.baselines import solve, validate_tour, SOLVERS
from src.metrics import compute_tour_cost, compute_gap, measure_solver

# Timeout
class SolverTimeout(Exception):
    pass

def _handler(signum, frame):
    raise SolverTimeout()

signal.signal(signal.SIGALRM, _handler)


def get_instances(scales=None, cities=None):
    """Get list of benchmark instance paths matching filters."""
    catalog_path = "benchmarks/instance_catalog.json"
    with open(catalog_path) as f:
        catalog = json.load(f)

    instances = []
    for entry in catalog:
        if "status" in entry:  # Skip failed entries
            continue
        if scales and entry["n_stops"] not in scales:
            continue
        if cities and entry["city"] not in cities:
            continue
        instances.append(entry)

    return instances


def run_benchmarks(solver_names=None, scales=None, seeds=None,
                   time_limit_s=30.0, output_path="results/baseline_results.csv"):
    """Run all specified solvers on all matching instances."""
    if solver_names is None:
        solver_names = list(SOLVERS.keys())
    if seeds is None:
        seeds = [42]

    instances = get_instances(scales=scales)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    results = []
    # First pass: find best known costs
    best_known = {}

    print(f"Running {len(solver_names)} solvers on {len(instances)} instances "
          f"with {len(seeds)} seeds each...")
    print(f"Time limit: {time_limit_s}s per solver per instance")
    print("-" * 80)

    for inst in instances:
        inst_id = inst["instance_id"]
        filepath = f"benchmarks/{inst_id}"
        data = load_instance(filepath)
        cost_mat = data["durations"]
        n = cost_mat.shape[0]

        for solver_name in solver_names:
            for seed in seeds:
                # Set alarm for 2x time limit as safety margin
                timeout = int(time_limit_s * 3) + 10
                signal.alarm(timeout)

                try:
                    t0 = time.time()
                    tour, cost = solve(cost_mat, solver_name,
                                      time_limit_s=time_limit_s, seed=seed)
                    elapsed = time.time() - t0
                    signal.alarm(0)

                    valid = validate_tour(tour, n)
                    if valid:
                        verified_cost = compute_tour_cost(cost_mat, tour)
                    else:
                        verified_cost = float("inf")

                    # Track best known
                    if inst_id not in best_known or verified_cost < best_known[inst_id]:
                        best_known[inst_id] = verified_cost

                    row = {
                        "instance_id": inst_id,
                        "city": inst["city"],
                        "n_stops": inst["n_stops"],
                        "solver": solver_name,
                        "seed": seed,
                        "tour_cost": round(verified_cost, 2),
                        "time_s": round(elapsed, 4),
                        "valid": valid,
                    }
                    results.append(row)

                    print(f"  {inst_id:30s} {solver_name:25s} seed={seed:4d} "
                          f"cost={verified_cost:12.1f} time={elapsed:6.2f}s")

                except SolverTimeout:
                    signal.alarm(0)
                    print(f"  {inst_id:30s} {solver_name:25s} seed={seed:4d} TIMEOUT")
                    results.append({
                        "instance_id": inst_id,
                        "city": inst["city"],
                        "n_stops": inst["n_stops"],
                        "solver": solver_name,
                        "seed": seed,
                        "tour_cost": float("inf"),
                        "time_s": timeout,
                        "valid": False,
                    })
                except Exception as e:
                    signal.alarm(0)
                    print(f"  {inst_id:30s} {solver_name:25s} seed={seed:4d} ERROR: {e}")
                    results.append({
                        "instance_id": inst_id,
                        "city": inst["city"],
                        "n_stops": inst["n_stops"],
                        "solver": solver_name,
                        "seed": seed,
                        "tour_cost": float("inf"),
                        "time_s": 0,
                        "valid": False,
                    })

    # Add gap_pct column
    for row in results:
        bk = best_known.get(row["instance_id"])
        if bk and row["tour_cost"] < float("inf"):
            row["gap_pct"] = round(compute_gap(row["tour_cost"], bk), 4)
        else:
            row["gap_pct"] = None

    # Write CSV
    if results:
        fieldnames = ["instance_id", "city", "n_stops", "solver", "seed",
                      "tour_cost", "gap_pct", "time_s", "valid"]
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    # Also save as JSON
    json_path = output_path.replace(".csv", ".json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_path} and {json_path}")
    print(f"Total runs: {len(results)}")

    return results, best_known


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TSP benchmarks")
    parser.add_argument("--solvers", nargs="+", default=None,
                       help="Solver names (default: all)")
    parser.add_argument("--scales", nargs="+", type=int, default=None,
                       help="Instance scales (default: all)")
    parser.add_argument("--seeds", nargs="+", type=int, default=[42],
                       help="Random seeds")
    parser.add_argument("--time-limit", type=float, default=30.0,
                       help="Time limit per solver per instance (seconds)")
    parser.add_argument("--output", type=str, default="results/baseline_results.csv",
                       help="Output file path")
    args = parser.parse_args()

    run_benchmarks(
        solver_names=args.solvers,
        scales=args.scales,
        seeds=args.seeds,
        time_limit_s=args.time_limit,
        output_path=args.output,
    )
