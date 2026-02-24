"""
Benchmarking harness for ATSP solvers.

Runs solvers on instances, records metrics, and outputs results.
"""

import json
import os
import time
import traceback
import csv

import numpy as np

# Solver imports
from src.baselines.lkh_baseline import solve_lkh
from src.baselines.ortools_baseline import solve_ortools
from src.baselines.construction_heuristics import (
    solve_nearest_neighbor, solve_greedy, solve_savings
)
from src.solvers.hybrid_gnn_lk import solve_hybrid_gnn_lk
from src.solvers.alns_learned import solve_alns
from src.solvers.ensemble import solve_ensemble

# Registry of available solvers
SOLVER_REGISTRY = {
    "nearest_neighbor": solve_nearest_neighbor,
    "greedy": solve_greedy,
    "savings": solve_savings,
    "ortools": solve_ortools,
    "lkh": solve_lkh,
    "hybrid_gnn_lk": solve_hybrid_gnn_lk,
    "alns": solve_alns,
    "ensemble": solve_ensemble,
}


def compute_tour_cost(tour, cost_matrix):
    """Compute the total cost of a directed tour."""
    cost = 0.0
    n = len(tour)
    for i in range(n):
        cost += cost_matrix[tour[i]][tour[(i + 1) % n]]
    return cost


def compute_asymmetry_exploitation(tour, cost_matrix):
    """Compute asymmetry exploitation score.

    Returns the fraction of tour edges where the solver chose the
    cheaper direction (i->j) compared to the reverse (j->i).
    """
    n = len(tour)
    cheaper_count = 0
    total_edges = 0

    for i in range(n):
        a, b = tour[i], tour[(i + 1) % n]
        c_ab = cost_matrix[a][b]
        c_ba = cost_matrix[b][a]
        if c_ab <= c_ba:
            cheaper_count += 1
        total_edges += 1

    return cheaper_count / total_edges if total_edges > 0 else 0.0


def load_instance(filepath):
    """Load an ATSP instance from JSON."""
    with open(filepath, 'r') as f:
        return json.load(f)


def run_solver(solver_name, instance, time_limit=60.0, seed=42, **kwargs):
    """Run a single solver on an instance and capture metrics.

    Returns
    -------
    dict or None
        Result dictionary with tour, cost, runtime, and metrics.
    """
    solver_fn = SOLVER_REGISTRY.get(solver_name)
    if solver_fn is None:
        # Try to find in extended registry (for novel solvers added later)
        raise ValueError(f"Unknown solver: {solver_name}")

    try:
        if solver_name in ("nearest_neighbor", "greedy", "savings"):
            result = solver_fn(instance, seed=seed)
        elif solver_name == "ortools":
            result = solver_fn(instance, time_limit=time_limit, seed=seed)
        elif solver_name == "lkh":
            max_trials = kwargs.get("max_trials", 10)
            result = solver_fn(instance, max_trials=max_trials,
                               time_limit=time_limit, seed=seed)
        else:
            result = solver_fn(instance, time_limit=time_limit, seed=seed,
                               **kwargs)

        # Add asymmetry exploitation metric
        cm = instance["cost_matrix"]
        result["asymmetry_exploitation"] = compute_asymmetry_exploitation(
            result["tour"], cm
        )
        return result

    except Exception as e:
        return {
            "tour": None,
            "cost": float("inf"),
            "runtime_seconds": 0.0,
            "solver_name": solver_name,
            "solver_params": {},
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


def run_benchmark(config):
    """Run a complete benchmark suite.

    Parameters
    ----------
    config : dict
        Configuration with keys:
        - solvers: list of solver names
        - instances: list of instance file paths
        - time_limit: default time limit per solver
        - seeds: list of random seeds for replication
        - output_dir: directory for results

    Returns
    -------
    list[dict]
        All benchmark results.
    """
    solvers = config.get("solvers", list(SOLVER_REGISTRY.keys()))
    instance_paths = config["instances"]
    time_limit = config.get("time_limit", 60.0)
    seeds = config.get("seeds", [42])
    output_dir = config.get("output_dir", "results")

    os.makedirs(output_dir, exist_ok=True)

    all_results = []
    best_known = {}  # instance_id -> best cost found

    total_runs = len(instance_paths) * len(solvers) * len(seeds)
    run_count = 0

    for inst_path in instance_paths:
        instance = load_instance(inst_path)
        inst_id = os.path.splitext(os.path.basename(inst_path))[0]
        n_nodes = instance["metadata"]["n_nodes"]

        for solver_name in solvers:
            for run_id, seed in enumerate(seeds):
                run_count += 1
                print(f"  [{run_count}/{total_runs}] {inst_id} | "
                      f"{solver_name} | seed={seed}")

                result = run_solver(
                    solver_name, instance,
                    time_limit=time_limit, seed=seed
                )

                record = {
                    "instance_id": inst_id,
                    "city": instance["metadata"].get("city", "unknown"),
                    "n_nodes": n_nodes,
                    "size_category": _size_category(n_nodes),
                    "solver": solver_name,
                    "run_id": run_id,
                    "seed": seed,
                    "tour_cost": result["cost"],
                    "runtime_seconds": result["runtime_seconds"],
                    "asymmetry_exploitation": result.get(
                        "asymmetry_exploitation", None
                    ),
                    "error": result.get("error", None),
                }

                all_results.append(record)

                # Track best known
                if result["cost"] < best_known.get(inst_id, float("inf")):
                    best_known[inst_id] = result["cost"]

    # Compute gap to best known
    for record in all_results:
        inst_id = record["instance_id"]
        bk = best_known.get(inst_id, record["tour_cost"])
        if bk > 0:
            record["gap_to_best_pct"] = (
                (record["tour_cost"] - bk) / bk * 100.0
            )
        else:
            record["gap_to_best_pct"] = 0.0

    # Save results
    _save_csv(all_results, os.path.join(output_dir, "full_benchmark.csv"))
    _save_json(all_results, os.path.join(output_dir, "full_benchmark.json"))

    return all_results


def _size_category(n):
    if n <= 50:
        return "small"
    elif n <= 200:
        return "medium"
    else:
        return "large"


def _save_csv(results, filepath):
    """Save results to CSV."""
    if not results:
        return

    fieldnames = list(results[0].keys())
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def _save_json(results, filepath):
    """Save results to JSON."""
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)


def register_solver(name, solver_fn):
    """Register a new solver in the registry."""
    SOLVER_REGISTRY[name] = solver_fn


if __name__ == "__main__":
    import yaml
    import glob

    # Load config or use defaults
    config_path = "benchmarks/eval_config.yaml"
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = yaml.safe_load(f)
    else:
        # Default: run all solvers on all instances
        instance_files = sorted(glob.glob("benchmarks/*.json"))
        instance_files = [f for f in instance_files if "manifest" not in f]
        config = {
            "solvers": list(SOLVER_REGISTRY.keys()),
            "instances": instance_files,
            "time_limit": 30,
            "seeds": [42],
            "output_dir": "results",
        }

    print(f"Running benchmark: {len(config['instances'])} instances, "
          f"{len(config['solvers'])} solvers")
    results = run_benchmark(config)
    print(f"\nCompleted {len(results)} runs. Results saved to results/")
