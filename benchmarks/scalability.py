"""Scalability analysis: runtime and memory vs graph size for all algorithms."""

import os
import sys
import json
import time
import signal
import tracemalloc
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph import generate_delaunay_planar_graph
from src.greedy import greedy_dominating_set, modified_greedy_dominating_set
from src.lp_solver import lp_rounding_dominating_set
from src.separator_mds import separator_mds
from src.planar_lp import planar_lp_rounding
from src.hybrid_mds import hybrid_mds
from src.baker_ptas import baker_ptas

FIGURES_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
SEED = 42
TIMEOUT = 300  # 5 minutes


class TimeoutError(Exception):
    pass

def _handler(signum, frame):
    raise TimeoutError()


def run_timed(func, args, timeout_sec=TIMEOUT):
    """Run function with timeout, return (result, time, peak_memory_mb) or None on timeout."""
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout_sec)
    tracemalloc.start()
    try:
        start = time.time()
        result = func(*args)
        elapsed = time.time() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        signal.alarm(0)
        return result, elapsed, peak / (1024 * 1024)
    except TimeoutError:
        tracemalloc.stop()
        signal.alarm(0)
        return None, timeout_sec, None
    except Exception as e:
        tracemalloc.stop()
        signal.alarm(0)
        print(f"    ERROR: {e}")
        return None, None, None


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    sizes = [1000, 5000, 10000, 50000, 100000]
    trials_per_size = 3
    rng = np.random.RandomState(SEED)

    algorithms = {
        'greedy': lambda g: greedy_dominating_set(g),
        'modified_greedy': lambda g: modified_greedy_dominating_set(g),
        'lp_rounding': lambda g: lp_rounding_dominating_set(g)[0],
        'separator': lambda g: separator_mds(g),
        'planar_lp': lambda g: planar_lp_rounding(g)[0],
        'baker_k3': lambda g: baker_ptas(g, k=3, exact_threshold=100),
        'hybrid': lambda g: hybrid_mds(g, separator_threshold=200, local_search_depth=50)[0],
    }

    # Size limits: skip algorithms that are too slow for large instances
    size_limits = {
        'greedy': 200000,
        'modified_greedy': 10000,
        'lp_rounding': 5000,
        'separator': 10000,
        'planar_lp': 5000,
        'baker_k3': 1000,
        'hybrid': 10000,
    }

    results = []

    for n in sizes:
        print(f"\n=== n = {n} ===", flush=True)
        for trial in range(trials_per_size):
            seed = rng.randint(0, 100000)
            print(f"  Trial {trial} (seed={seed})")
            g = generate_delaunay_planar_graph(n, seed=seed)
            actual_n = g.n
            actual_m = g.m
            print(f"    Generated: n={actual_n}, m={actual_m}", flush=True)

            for alg_name, alg_func in algorithms.items():
                if n > size_limits.get(alg_name, 100000):
                    print(f"    {alg_name}: SKIPPED (n>{size_limits[alg_name]})")
                    continue

                timeout = min(TIMEOUT, 300 if n <= 10000 else 120)
                res, elapsed, mem_mb = run_timed(alg_func, (g,), timeout_sec=timeout)

                if res is None and elapsed == timeout:
                    print(f"    {alg_name}: TIMEOUT ({timeout}s)")
                    row = {
                        'n': actual_n, 'm': actual_m, 'trial': trial,
                        'algorithm': alg_name, 'runtime': timeout,
                        'memory_mb': None, 'solution_size': None, 'timed_out': True,
                    }
                elif res is None:
                    print(f"    {alg_name}: FAILED")
                    continue
                else:
                    sol_size = len(res) if isinstance(res, (set, list, frozenset)) else None
                    print(f"    {alg_name}: size={sol_size}, time={elapsed:.3f}s, mem={mem_mb:.1f}MB")
                    row = {
                        'n': actual_n, 'm': actual_m, 'trial': trial,
                        'algorithm': alg_name, 'runtime': round(elapsed, 4),
                        'memory_mb': round(mem_mb, 2), 'solution_size': sol_size,
                        'timed_out': False,
                    }
                results.append(row)

    # Save results
    json_path = os.path.join(RESULTS_DIR, 'scalability.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} data points to {json_path}")

    # Compute scalability summary
    summary = compute_summary(results)
    summary_path = os.path.join(os.path.dirname(__file__), 'scalability.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to {summary_path}")

    # Generate figure
    generate_figure(results)
    print("Figures generated.")


def compute_summary(results):
    """Compute per-algorithm scalability summary with growth rate fitting."""
    from collections import defaultdict

    alg_data = defaultdict(lambda: defaultdict(list))
    for r in results:
        if not r['timed_out'] and r['runtime'] is not None:
            alg_data[r['algorithm']][r['n']].append(r['runtime'])

    summary = {}
    for alg, size_data in alg_data.items():
        sizes = sorted(size_data.keys())
        mean_times = [np.mean(size_data[s]) for s in sizes]

        # Fit growth rate: log(t) = a * log(n) + b  =>  t ~ n^a
        if len(sizes) >= 2:
            log_n = np.log(np.array(sizes, dtype=float))
            log_t = np.log(np.array(mean_times, dtype=float))
            # Filter out any non-finite values
            valid = np.isfinite(log_n) & np.isfinite(log_t)
            if np.sum(valid) >= 2:
                coeffs = np.polyfit(log_n[valid], log_t[valid], 1)
                exponent = coeffs[0]
            else:
                exponent = None
        else:
            exponent = None

        # Find practical timeout limit
        timeout_at = None
        for r in results:
            if r['algorithm'] == alg and r['timed_out']:
                timeout_at = r['n']
                break

        # Classify growth
        if exponent is not None:
            if exponent < 1.15:
                growth_class = "O(n)"
            elif exponent < 1.4:
                growth_class = "O(n log n)"
            elif exponent < 1.7:
                growth_class = "O(n^1.5)"
            elif exponent < 2.2:
                growth_class = "O(n^2)"
            else:
                growth_class = f"O(n^{exponent:.1f})"
        else:
            growth_class = "insufficient data"

        summary[alg] = {
            'sizes_tested': sizes,
            'mean_runtimes': [round(t, 4) for t in mean_times],
            'growth_exponent': round(exponent, 3) if exponent is not None else None,
            'growth_class': growth_class,
            'timeout_at_n': timeout_at,
        }
        print(f"  {alg}: exponent={exponent:.3f if exponent else 'N/A'}, class={growth_class}, timeout_at={timeout_at}")

    return summary


def generate_figure(results):
    """Generate scalability plot."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from collections import defaultdict

    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'legend.fontsize': 10,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
    })

    alg_data = defaultdict(lambda: defaultdict(list))
    mem_data = defaultdict(lambda: defaultdict(list))
    for r in results:
        if not r['timed_out'] and r['runtime'] is not None:
            alg_data[r['algorithm']][r['n']].append(r['runtime'])
        if r.get('memory_mb') is not None:
            mem_data[r['algorithm']][r['n']].append(r['memory_mb'])

    colors = {
        'greedy': '#1f77b4', 'modified_greedy': '#ff7f0e',
        'lp_rounding': '#2ca02c', 'separator': '#d62728',
        'planar_lp': '#9467bd', 'baker_k3': '#8c564b',
        'hybrid': '#e377c2',
    }
    markers = {
        'greedy': 'o', 'modified_greedy': 's', 'lp_rounding': '^',
        'separator': 'D', 'planar_lp': 'v', 'baker_k3': 'P',
        'hybrid': '*',
    }
    labels = {
        'greedy': 'Greedy', 'modified_greedy': 'Modified Greedy',
        'lp_rounding': 'LP Rounding', 'separator': 'Separator',
        'planar_lp': 'Planar LP', 'baker_k3': "Baker's PTAS (k=3)",
        'hybrid': 'Hybrid (ours)',
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Runtime plot
    for alg in ['greedy', 'modified_greedy', 'separator', 'hybrid',
                'lp_rounding', 'planar_lp', 'baker_k3']:
        if alg not in alg_data:
            continue
        sizes = sorted(alg_data[alg].keys())
        means = [np.mean(alg_data[alg][s]) for s in sizes]
        stds = [np.std(alg_data[alg][s]) for s in sizes]
        ax1.errorbar(sizes, means, yerr=stds,
                     label=labels.get(alg, alg),
                     color=colors.get(alg, 'gray'),
                     marker=markers.get(alg, 'o'),
                     markersize=6, linewidth=1.5, capsize=3)

    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Number of Nodes (n)')
    ax1.set_ylabel('Runtime (seconds)')
    ax1.set_title('Runtime Scalability')
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)

    # Reference lines
    xs = np.array([1000, 100000])
    ax1.plot(xs, xs / 1000 * 0.003, '--', color='gray', alpha=0.3, linewidth=1)
    ax1.text(100000, 0.3, 'O(n)', fontsize=8, color='gray')

    # Memory plot
    for alg in ['greedy', 'modified_greedy', 'separator', 'hybrid',
                'lp_rounding', 'planar_lp', 'baker_k3']:
        if alg not in mem_data:
            continue
        sizes = sorted(mem_data[alg].keys())
        means = [np.mean(mem_data[alg][s]) for s in sizes]
        ax2.plot(sizes, means,
                 label=labels.get(alg, alg),
                 color=colors.get(alg, 'gray'),
                 marker=markers.get(alg, 'o'),
                 markersize=6, linewidth=1.5)

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Number of Nodes (n)')
    ax2.set_ylabel('Peak Memory (MB)')
    ax2.set_title('Memory Usage')
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    for ext in ['png', 'pdf']:
        path = os.path.join(FIGURES_DIR, f'scalability.{ext}')
        fig.savefig(path)
        print(f"  Saved {path}")
    plt.close()


if __name__ == '__main__':
    main()
