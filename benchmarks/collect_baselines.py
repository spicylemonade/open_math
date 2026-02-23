"""Collect baseline performance metrics for all algorithms on benchmark instances."""

import os
import sys
import json
import time
import signal
import csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph import load_pace_format
from src.greedy import greedy_dominating_set, modified_greedy_dominating_set
from src.lp_solver import lp_rounding_dominating_set, solve_lp_relaxation
from src.baker_ptas import baker_ptas

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')


class Timeout(Exception):
    pass

def _handler(signum, frame):
    raise Timeout()


def run_with_timeout(func, args, timeout_sec=300):
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout_sec)
    try:
        start = time.time()
        result = func(*args)
        elapsed = time.time() - start
        signal.alarm(0)
        return result, elapsed
    except Timeout:
        signal.alarm(0)
        return None, timeout_sec


def collect_baselines():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    manifest_path = os.path.join(DATA_DIR, 'manifest.json')
    with open(manifest_path, 'r') as f:
        instances = json.load(f)

    results = []
    algorithms = {
        'greedy': lambda g: (greedy_dominating_set(g), None),
        'modified_greedy': lambda g: (modified_greedy_dominating_set(g), None),
        'lp_rounding': lambda g: lp_rounding_dominating_set(g),
        'baker_k3': lambda g: (baker_ptas(g, k=3, exact_threshold=100), None),
    }

    for inst in instances:
        n = inst['n']
        name = inst['name']
        print(f"\n=== {name} (n={n}) ===")

        g = load_pace_format(inst['path'])

        # Get LP lower bound for ratio computation (skip for large instances)
        lp_lb = None
        if n <= 2000:
            try:
                (lp_val, _), lp_time = run_with_timeout(
                    solve_lp_relaxation, (g,), timeout_sec=120
                )
                if lp_val is not None:
                    lp_lb = lp_val
                    print(f"  LP lower bound: {lp_lb:.2f} ({lp_time:.2f}s)")
            except Exception as e:
                print(f"  LP failed: {e}")

        for alg_name, alg_func in algorithms.items():
            # Skip slow algorithms on large instances
            if n > 2000 and alg_name in ('lp_rounding', 'baker_k3'):
                continue
            if n > 5000 and alg_name == 'modified_greedy':
                continue

            timeout = 300 if n <= 1000 else 120
            try:
                result, elapsed = run_with_timeout(alg_func, (g,), timeout_sec=timeout)
                if result is None:
                    print(f"  {alg_name}: TIMEOUT ({timeout}s)")
                    continue
                ds, extra = result
                if ds is None:
                    print(f"  {alg_name}: FAILED")
                    continue

                sol_size = len(ds)
                valid = g.is_dominating_set(ds)
                ratio = sol_size / lp_lb if lp_lb and lp_lb > 0 else None

                row = {
                    'instance_name': name,
                    'n': n,
                    'm': inst['m'],
                    'algorithm': alg_name,
                    'solution_size': sol_size,
                    'lp_lower_bound': round(lp_lb, 4) if lp_lb else None,
                    'approx_ratio_vs_lp': round(ratio, 4) if ratio else None,
                    'runtime_seconds': round(elapsed, 4),
                    'valid': valid,
                }
                results.append(row)
                ratio_str = f"{ratio:.3f}" if ratio is not None else "N/A"
                print(f"  {alg_name}: size={sol_size}, ratio={ratio_str}, time={elapsed:.3f}s, valid={valid}")

            except Exception as e:
                print(f"  {alg_name}: ERROR {e}")

    # Save to CSV
    csv_path = os.path.join(os.path.dirname(__file__), 'baseline_results.csv')
    fieldnames = ['instance_name', 'n', 'm', 'algorithm', 'solution_size',
                  'lp_lower_bound', 'approx_ratio_vs_lp', 'runtime_seconds', 'valid']
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Also save as JSON
    json_path = os.path.join(RESULTS_DIR, 'baseline_results.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n=== Collected {len(results)} data points ===")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    return results


if __name__ == '__main__':
    collect_baselines()
