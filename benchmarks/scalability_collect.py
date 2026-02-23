"""Collect scalability data from existing experiments and generate figures."""

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

FIGURES_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

# Data collected from scalability.py runs
RAW_DATA = [
    # n=1000 trials
    {'n': 1000, 'trial': 0, 'algorithm': 'greedy', 'runtime': 0.248, 'memory_mb': 0.1, 'solution_size': 193, 'timed_out': False},
    {'n': 1000, 'trial': 0, 'algorithm': 'modified_greedy', 'runtime': 0.416, 'memory_mb': 0.1, 'solution_size': 200, 'timed_out': False},
    {'n': 1000, 'trial': 0, 'algorithm': 'lp_rounding', 'runtime': 0.237, 'memory_mb': 3.4, 'solution_size': 449, 'timed_out': False},
    {'n': 1000, 'trial': 0, 'algorithm': 'separator', 'runtime': 0.135, 'memory_mb': 0.9, 'solution_size': 191, 'timed_out': False},
    {'n': 1000, 'trial': 0, 'algorithm': 'planar_lp', 'runtime': 0.978, 'memory_mb': 14.7, 'solution_size': 175, 'timed_out': False},
    {'n': 1000, 'trial': 0, 'algorithm': 'baker_k3', 'runtime': 0.559, 'memory_mb': 0.9, 'solution_size': 464, 'timed_out': False},
    {'n': 1000, 'trial': 0, 'algorithm': 'hybrid', 'runtime': 35.291, 'memory_mb': 16.1, 'solution_size': 169, 'timed_out': False},

    {'n': 1000, 'trial': 1, 'algorithm': 'greedy', 'runtime': 0.240, 'memory_mb': 0.1, 'solution_size': 186, 'timed_out': False},
    {'n': 1000, 'trial': 1, 'algorithm': 'modified_greedy', 'runtime': 0.387, 'memory_mb': 0.1, 'solution_size': 194, 'timed_out': False},
    {'n': 1000, 'trial': 1, 'algorithm': 'lp_rounding', 'runtime': 0.202, 'memory_mb': 3.4, 'solution_size': 427, 'timed_out': False},
    {'n': 1000, 'trial': 1, 'algorithm': 'separator', 'runtime': 0.150, 'memory_mb': 0.9, 'solution_size': 187, 'timed_out': False},
    {'n': 1000, 'trial': 1, 'algorithm': 'planar_lp', 'runtime': 0.744, 'memory_mb': 16.1, 'solution_size': 167, 'timed_out': False},
    {'n': 1000, 'trial': 1, 'algorithm': 'baker_k3', 'runtime': 0.552, 'memory_mb': 0.8, 'solution_size': 473, 'timed_out': False},
    {'n': 1000, 'trial': 1, 'algorithm': 'hybrid', 'runtime': 28.727, 'memory_mb': 16.1, 'solution_size': 166, 'timed_out': False},

    {'n': 1000, 'trial': 2, 'algorithm': 'greedy', 'runtime': 0.230, 'memory_mb': 0.1, 'solution_size': 178, 'timed_out': False},
    {'n': 1000, 'trial': 2, 'algorithm': 'modified_greedy', 'runtime': 0.370, 'memory_mb': 0.1, 'solution_size': 183, 'timed_out': False},
    {'n': 1000, 'trial': 2, 'algorithm': 'lp_rounding', 'runtime': 0.215, 'memory_mb': 3.4, 'solution_size': 420, 'timed_out': False},
    {'n': 1000, 'trial': 2, 'algorithm': 'separator', 'runtime': 0.125, 'memory_mb': 0.9, 'solution_size': 187, 'timed_out': False},
    {'n': 1000, 'trial': 2, 'algorithm': 'planar_lp', 'runtime': 0.796, 'memory_mb': 15.5, 'solution_size': 168, 'timed_out': False},
    {'n': 1000, 'trial': 2, 'algorithm': 'baker_k3', 'runtime': 0.524, 'memory_mb': 0.8, 'solution_size': 476, 'timed_out': False},
    {'n': 1000, 'trial': 2, 'algorithm': 'hybrid', 'runtime': 21.133, 'memory_mb': 11.8, 'solution_size': 165, 'timed_out': False},

    # n=5000 trials
    {'n': 5000, 'trial': 0, 'algorithm': 'greedy', 'runtime': 6.113, 'memory_mb': 0.7, 'solution_size': 894, 'timed_out': False},
    {'n': 5000, 'trial': 0, 'algorithm': 'modified_greedy', 'runtime': 9.762, 'memory_mb': 0.7, 'solution_size': 934, 'timed_out': False},
    {'n': 5000, 'trial': 0, 'algorithm': 'lp_rounding', 'runtime': 3.512, 'memory_mb': 16.7, 'solution_size': 2186, 'timed_out': False},
    {'n': 5000, 'trial': 0, 'algorithm': 'separator', 'runtime': 3.516, 'memory_mb': 4.8, 'solution_size': 910, 'timed_out': False},
    {'n': 5000, 'trial': 0, 'algorithm': 'planar_lp', 'runtime': 11.945, 'memory_mb': 72.7, 'solution_size': 860, 'timed_out': False},
    {'n': 5000, 'trial': 0, 'algorithm': 'hybrid', 'runtime': 35.989, 'memory_mb': 58.9, 'solution_size': 860, 'timed_out': False},

    {'n': 5000, 'trial': 1, 'algorithm': 'greedy', 'runtime': 6.292, 'memory_mb': 0.7, 'solution_size': 896, 'timed_out': False},
    {'n': 5000, 'trial': 1, 'algorithm': 'modified_greedy', 'runtime': 9.860, 'memory_mb': 0.7, 'solution_size': 936, 'timed_out': False},
    {'n': 5000, 'trial': 1, 'algorithm': 'lp_rounding', 'runtime': 3.371, 'memory_mb': 16.7, 'solution_size': 2099, 'timed_out': False},
    {'n': 5000, 'trial': 1, 'algorithm': 'separator', 'runtime': 3.397, 'memory_mb': 4.8, 'solution_size': 902, 'timed_out': False},
    {'n': 5000, 'trial': 1, 'algorithm': 'planar_lp', 'runtime': 11.392, 'memory_mb': 72.7, 'solution_size': 846, 'timed_out': False},
    {'n': 5000, 'trial': 1, 'algorithm': 'hybrid', 'runtime': 36.560, 'memory_mb': 59.0, 'solution_size': 846, 'timed_out': False},

    {'n': 5000, 'trial': 2, 'algorithm': 'greedy', 'runtime': 6.176, 'memory_mb': 0.7, 'solution_size': 904, 'timed_out': False},
    {'n': 5000, 'trial': 2, 'algorithm': 'modified_greedy', 'runtime': 9.818, 'memory_mb': 0.7, 'solution_size': 944, 'timed_out': False},
    {'n': 5000, 'trial': 2, 'algorithm': 'lp_rounding', 'runtime': 3.341, 'memory_mb': 16.7, 'solution_size': 2165, 'timed_out': False},
    {'n': 5000, 'trial': 2, 'algorithm': 'separator', 'runtime': 3.456, 'memory_mb': 4.8, 'solution_size': 899, 'timed_out': False},
    {'n': 5000, 'trial': 2, 'algorithm': 'planar_lp', 'runtime': 11.451, 'memory_mb': 72.7, 'solution_size': 847, 'timed_out': False},
    {'n': 5000, 'trial': 2, 'algorithm': 'hybrid', 'runtime': 35.738, 'memory_mb': 59.0, 'solution_size': 847, 'timed_out': False},

    # n=10000 trials
    {'n': 10000, 'trial': 0, 'algorithm': 'greedy', 'runtime': 25.125, 'memory_mb': 1.4, 'solution_size': 1811, 'timed_out': False},
    {'n': 10000, 'trial': 0, 'algorithm': 'modified_greedy', 'runtime': 39.623, 'memory_mb': 1.4, 'solution_size': 1880, 'timed_out': False},
    {'n': 10000, 'trial': 0, 'algorithm': 'separator', 'runtime': 14.082, 'memory_mb': 10.1, 'solution_size': 1819, 'timed_out': False},
    {'n': 10000, 'trial': 0, 'algorithm': 'hybrid', 'runtime': 59.862, 'memory_mb': 10.0, 'solution_size': 1793, 'timed_out': False},

    {'n': 10000, 'trial': 1, 'algorithm': 'greedy', 'runtime': 25.197, 'memory_mb': 1.4, 'solution_size': 1814, 'timed_out': False},
    {'n': 10000, 'trial': 1, 'algorithm': 'modified_greedy', 'runtime': 42.630, 'memory_mb': 1.4, 'solution_size': 1880, 'timed_out': False},
    {'n': 10000, 'trial': 1, 'algorithm': 'separator', 'runtime': 14.274, 'memory_mb': 10.0, 'solution_size': 1827, 'timed_out': False},
    {'n': 10000, 'trial': 1, 'algorithm': 'hybrid', 'runtime': 60.467, 'memory_mb': 10.0, 'solution_size': 1794, 'timed_out': False},

    {'n': 10000, 'trial': 2, 'algorithm': 'greedy', 'runtime': 25.104, 'memory_mb': 1.4, 'solution_size': 1796, 'timed_out': False},
    {'n': 10000, 'trial': 2, 'algorithm': 'modified_greedy', 'runtime': 40.693, 'memory_mb': 1.4, 'solution_size': 1855, 'timed_out': False},
    {'n': 10000, 'trial': 2, 'algorithm': 'separator', 'runtime': 14.006, 'memory_mb': 10.1, 'solution_size': 1799, 'timed_out': False},
    {'n': 10000, 'trial': 2, 'algorithm': 'hybrid', 'runtime': 60.483, 'memory_mb': 10.0, 'solution_size': 1776, 'timed_out': False},

    # n=50000 - greedy timeouts
    {'n': 50000, 'trial': 0, 'algorithm': 'greedy', 'runtime': 120, 'memory_mb': None, 'solution_size': None, 'timed_out': True},
    {'n': 50000, 'trial': 1, 'algorithm': 'greedy', 'runtime': 120, 'memory_mb': None, 'solution_size': None, 'timed_out': True},
    {'n': 50000, 'trial': 2, 'algorithm': 'greedy', 'runtime': 120, 'memory_mb': None, 'solution_size': None, 'timed_out': True},

    # n=100000 - greedy timeouts
    {'n': 100000, 'trial': 0, 'algorithm': 'greedy', 'runtime': 120, 'memory_mb': None, 'solution_size': None, 'timed_out': True},
]


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

        if len(sizes) >= 2:
            log_n = np.log(np.array(sizes, dtype=float))
            log_t = np.log(np.array(mean_times, dtype=float))
            valid = np.isfinite(log_n) & np.isfinite(log_t)
            if np.sum(valid) >= 2:
                coeffs = np.polyfit(log_n[valid], log_t[valid], 1)
                exponent = coeffs[0]
            else:
                exponent = None
        else:
            exponent = None

        timeout_at = None
        for r in results:
            if r['algorithm'] == alg and r['timed_out']:
                timeout_at = r['n']
                break

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
        exp_str = f"{exponent:.3f}" if exponent is not None else "N/A"
        print(f"  {alg}: exponent={exp_str}, class={growth_class}, timeout_at={timeout_at}")

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

    plot_order = ['greedy', 'modified_greedy', 'separator', 'hybrid',
                  'lp_rounding', 'planar_lp', 'baker_k3']

    for alg in plot_order:
        if alg not in alg_data:
            continue
        sizes = sorted(alg_data[alg].keys())
        means = [np.mean(alg_data[alg][s]) for s in sizes]
        stds = [np.std(alg_data[alg][s]) for s in sizes]
        ax1.errorbar(sizes, means, yerr=stds,
                     label=labels.get(alg, alg),
                     color=colors.get(alg, 'gray'),
                     marker=markers.get(alg, 'o'),
                     markersize=8, linewidth=2, capsize=3)

    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Number of Nodes (n)')
    ax1.set_ylabel('Runtime (seconds)')
    ax1.set_title('Runtime Scalability')
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)

    # Reference lines
    xs = np.array([1000, 10000])
    base = 0.24
    ax1.plot(xs, [base, base * 10], '--', color='gray', alpha=0.4, linewidth=1)
    ax1.text(11000, base * 10, 'O(n)', fontsize=9, color='gray', alpha=0.6)
    ax1.plot(xs, [base, base * 100], ':', color='gray', alpha=0.4, linewidth=1)
    ax1.text(11000, base * 100, 'O(n\u00b2)', fontsize=9, color='gray', alpha=0.6)

    for alg in plot_order:
        if alg not in mem_data:
            continue
        sizes = sorted(mem_data[alg].keys())
        means = [np.mean(mem_data[alg][s]) for s in sizes]
        ax2.plot(sizes, means,
                 label=labels.get(alg, alg),
                 color=colors.get(alg, 'gray'),
                 marker=markers.get(alg, 'o'),
                 markersize=8, linewidth=2)

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Number of Nodes (n)')
    ax2.set_ylabel('Peak Memory (MB)')
    ax2.set_title('Memory Usage')
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(FIGURES_DIR, exist_ok=True)
    for ext in ['png', 'pdf']:
        path = os.path.join(FIGURES_DIR, f'scalability.{ext}')
        fig.savefig(path)
        print(f"  Saved {path}")
    plt.close()


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Save raw data
    json_path = os.path.join(RESULTS_DIR, 'scalability.json')
    with open(json_path, 'w') as f:
        json.dump(RAW_DATA, f, indent=2)
    print(f"Saved {len(RAW_DATA)} data points to {json_path}")

    # Compute summary
    print("\n=== Scalability Summary ===")
    summary = compute_summary(RAW_DATA)
    summary_path = os.path.join(os.path.dirname(__file__), 'scalability.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to {summary_path}")

    # Generate figure
    generate_figure(RAW_DATA)
    print("\nFigures generated.")


if __name__ == '__main__':
    main()
