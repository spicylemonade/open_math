"""Systematic performance comparison of all algorithms on full benchmark suite."""

import os
import sys
import json
import time
import signal
import csv
import tracemalloc
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph import load_pace_format
from src.greedy import greedy_dominating_set, modified_greedy_dominating_set
from src.lp_solver import lp_rounding_dominating_set, solve_lp_relaxation
from src.baker_ptas import baker_ptas
from src.separator_mds import separator_mds
from src.planar_lp import planar_lp_rounding
from src.hybrid_mds import hybrid_mds
from src.local_search import local_search

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')


class Timeout(Exception):
    pass

def _handler(signum, frame):
    raise Timeout()


def run_with_timeout(func, args=(), kwargs=None, timeout_sec=300):
    if kwargs is None:
        kwargs = {}
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout_sec)
    try:
        tracemalloc.start()
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        signal.alarm(0)
        return result, elapsed, peak_mem / (1024 * 1024)  # MB
    except Timeout:
        signal.alarm(0)
        try:
            tracemalloc.stop()
        except Exception:
            pass
        return None, timeout_sec, 0
    except Exception as e:
        signal.alarm(0)
        try:
            tracemalloc.stop()
        except Exception:
            pass
        return None, 0, 0


def run_all():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    manifest_path = os.path.join(DATA_DIR, 'manifest.json')
    with open(manifest_path, 'r') as f:
        instances = json.load(f)

    results = []

    # Define algorithms with size limits
    def make_algorithms(n):
        algs = {
            'greedy': lambda g: greedy_dominating_set(g),
            'modified_greedy': lambda g: modified_greedy_dominating_set(g),
        }
        if n <= 1000:
            algs['lp_rounding'] = lambda g: lp_rounding_dominating_set(g)[0]
            algs['separator'] = lambda g: separator_mds(g, threshold=200)
            algs['planar_lp'] = lambda g: planar_lp_rounding(g)[0]
            algs['hybrid'] = lambda g: hybrid_mds(g)[0]
        if n <= 500:
            algs['baker_k2'] = lambda g: baker_ptas(g, k=2, exact_threshold=80)
            algs['baker_k3'] = lambda g: baker_ptas(g, k=3, exact_threshold=80)
            algs['baker_k5'] = lambda g: baker_ptas(g, k=5, exact_threshold=80)
        if 1000 < n <= 5000:
            algs['separator'] = lambda g: separator_mds(g, threshold=200)
            algs['hybrid'] = lambda g: hybrid_mds(g, use_lp=True, local_search_depth=50)[0]
        elif n > 5000:
            algs['hybrid'] = lambda g: hybrid_mds(g, use_lp=False, use_separator=True, local_search_depth=30)[0]
        return algs

    for inst in instances:
        n = inst['n']
        name = inst['name']
        print(f"\n=== {name} (n={n}) ===")

        g = load_pace_format(inst['path'])

        # Get LP lower bound
        lp_lb = None
        if n <= 5000:
            try:
                res, _, _ = run_with_timeout(solve_lp_relaxation, (g,), timeout_sec=120)
                if res is not None:
                    lp_lb = res[0] if isinstance(res, tuple) else res
            except Exception:
                pass

        algorithms = make_algorithms(n)
        timeout = 300 if n <= 1000 else 120 if n <= 5000 else 60

        for alg_name, alg_func in algorithms.items():
            res, elapsed, peak_mb = run_with_timeout(alg_func, (g,), timeout_sec=timeout)
            if res is None:
                print(f"  {alg_name}: TIMEOUT/ERROR")
                continue

            ds = res
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
                'peak_memory_mb': round(peak_mb, 2),
            }
            results.append(row)
            ratio_str = f"{ratio:.3f}" if ratio is not None else "N/A"
            print(f"  {alg_name}: size={sol_size}, ratio={ratio_str}, time={elapsed:.3f}s, mem={peak_mb:.1f}MB, valid={valid}")

    # Save results
    csv_path = os.path.join(os.path.dirname(__file__), 'results.csv')
    fieldnames = ['instance_name', 'n', 'm', 'algorithm', 'solution_size',
                  'lp_lower_bound', 'approx_ratio_vs_lp', 'runtime_seconds',
                  'peak_memory_mb']
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    json_path = os.path.join(RESULTS_DIR, 'full_results.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n=== Collected {len(results)} data points ===")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    return results


if __name__ == '__main__':
    run_all()
