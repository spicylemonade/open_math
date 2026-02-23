"""Validate approximation ratios against ILP-optimal solutions on small instances."""

import os
import sys
import json
import csv
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph import generate_delaunay_planar_graph, generate_grid_graph, generate_random_planar_graph
from src.greedy import greedy_dominating_set, modified_greedy_dominating_set
from src.lp_solver import solve_ilp_exact, lp_rounding_dominating_set
from src.separator_mds import separator_mds
from src.planar_lp import planar_lp_rounding
from src.local_search import local_search
from src.hybrid_mds import hybrid_mds

SEED = 42
BENCHMARKS_DIR = os.path.dirname(__file__)


def generate_instances(count=50):
    """Generate diverse small planar graph instances for exact validation."""
    rng = np.random.RandomState(SEED)
    instances = []

    # Grid graphs: various sizes
    for n_side in [5, 6, 7, 8, 9, 10]:
        for trial in range(2):
            cols = n_side if trial == 0 else n_side - 1
            if cols < 2:
                cols = 2
            g = generate_grid_graph(n_side, cols)
            instances.append((f"grid_{g.n}_t{trial}", g))

    # Delaunay graphs
    for n in [30, 50, 75, 100, 150, 200]:
        for trial in range(2):
            seed = rng.randint(0, 100000)
            g = generate_delaunay_planar_graph(n, seed=seed)
            instances.append((f"delaunay_{g.n}_t{trial}", g))

    # Random planar graphs
    for n in [30, 50, 75, 100, 150, 200]:
        for trial in range(2):
            seed = rng.randint(0, 100000)
            g = generate_random_planar_graph(n, seed=seed)
            instances.append((f"random_{g.n}_t{trial}", g))

    print(f"Generated {len(instances)} instances")
    return instances[:max(count, len(instances))]


def main():
    instances = generate_instances(count=60)

    algorithms = {
        'greedy': lambda g: greedy_dominating_set(g),
        'modified_greedy': lambda g: modified_greedy_dominating_set(g),
        'lp_rounding': lambda g: lp_rounding_dominating_set(g)[0],
        'separator': lambda g: separator_mds(g),
        'planar_lp': lambda g: planar_lp_rounding(g)[0],
        'hybrid': lambda g: hybrid_mds(g, separator_threshold=200, local_search_depth=100)[0],
    }

    results = []

    for name, g in instances:
        n = g.n
        print(f"\n=== {name} (n={n}) ===")

        # Compute exact optimal via ILP
        try:
            start = time.time()
            opt_ds, opt_val = solve_ilp_exact(g, time_limit=120)
            opt_time = time.time() - start
            if opt_ds is None:
                print(f"  ILP: FAILED/TIMEOUT")
                continue
            opt_size = len(opt_ds)
            print(f"  OPT = {opt_size} (ILP time: {opt_time:.2f}s)")
        except Exception as e:
            print(f"  ILP ERROR: {e}")
            continue

        for alg_name, alg_func in algorithms.items():
            try:
                start = time.time()
                ds = alg_func(g)
                elapsed = time.time() - start
                if ds is None:
                    print(f"  {alg_name}: FAILED")
                    continue
                sol_size = len(ds)
                valid = g.is_dominating_set(ds)
                ratio = sol_size / opt_size if opt_size > 0 else None

                row = {
                    'instance': name,
                    'n': n,
                    'algorithm': alg_name,
                    'opt_size': opt_size,
                    'solution_size': sol_size,
                    'exact_ratio': round(ratio, 4) if ratio else None,
                    'runtime': round(elapsed, 4),
                    'valid': valid,
                }
                results.append(row)
                ratio_str = f"{ratio:.3f}" if ratio else "N/A"
                print(f"  {alg_name}: size={sol_size}, ratio={ratio_str}, valid={valid}")
            except Exception as e:
                print(f"  {alg_name}: ERROR {e}")

    # Save CSV
    csv_path = os.path.join(BENCHMARKS_DIR, 'exact_validation.csv')
    fieldnames = ['instance', 'n', 'algorithm', 'opt_size', 'solution_size',
                  'exact_ratio', 'runtime', 'valid']
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved {len(results)} rows to {csv_path}")

    # Summary statistics
    from collections import defaultdict
    from scipy import stats

    alg_ratios = defaultdict(list)
    for r in results:
        if r['exact_ratio'] is not None:
            alg_ratios[r['algorithm']].append(r['exact_ratio'])

    print("\n=== Exact Ratio Summary ===")
    summary = {}
    for alg in sorted(alg_ratios.keys()):
        arr = np.array(alg_ratios[alg])
        s = {
            'mean': round(float(np.mean(arr)), 4),
            'median': round(float(np.median(arr)), 4),
            'std': round(float(np.std(arr)), 4),
            'min': round(float(np.min(arr)), 4),
            'max': round(float(np.max(arr)), 4),
            'count': len(arr),
            'optimal_pct': round(float(np.mean(arr == 1.0) * 100), 1),
        }
        summary[alg] = s
        print(f"  {alg:20s}: mean={s['mean']:.3f}, max={s['max']:.3f}, "
              f"optimal={s['optimal_pct']:.0f}%, n={s['count']}")

    # Statistical test: hybrid vs greedy
    if 'hybrid' in alg_ratios and 'greedy' in alg_ratios:
        # Paired comparison on common instances
        instance_results = defaultdict(dict)
        for r in results:
            if r['exact_ratio'] is not None:
                instance_results[r['instance']][r['algorithm']] = r['exact_ratio']

        hybrid_vals, greedy_vals = [], []
        for inst, algs in instance_results.items():
            if 'hybrid' in algs and 'greedy' in algs:
                hybrid_vals.append(algs['hybrid'])
                greedy_vals.append(algs['greedy'])

        if len(hybrid_vals) >= 5:
            stat, p_val = stats.wilcoxon(hybrid_vals, greedy_vals, alternative='less')
            print(f"\n  Hybrid vs Greedy Wilcoxon: p={p_val:.6f}")
            print(f"  Hybrid mean={np.mean(hybrid_vals):.4f}, Greedy mean={np.mean(greedy_vals):.4f}")
            summary['hybrid_vs_greedy_p_value'] = float(p_val)

    # Save summary
    summary_path = os.path.join(BENCHMARKS_DIR, 'exact_validation_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to {summary_path}")

    return results


if __name__ == '__main__':
    main()
