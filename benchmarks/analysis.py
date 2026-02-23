"""Statistical analysis of approximation ratio improvements."""

import os
import sys
import json
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')


def load_results():
    with open(os.path.join(RESULTS_DIR, 'full_results.json')) as f:
        return json.load(f)


def analyze():
    results = load_results()

    # Filter to instances where we have ratio data
    with_ratio = [r for r in results if r['approx_ratio_vs_lp'] is not None]

    # Group by algorithm
    alg_ratios = {}
    for r in with_ratio:
        alg = r['algorithm']
        if alg not in alg_ratios:
            alg_ratios[alg] = []
        alg_ratios[alg].append(r['approx_ratio_vs_lp'])

    # Summary statistics
    summary = {}
    for alg, ratios in alg_ratios.items():
        arr = np.array(ratios)
        summary[alg] = {
            'mean': float(np.mean(arr)),
            'median': float(np.median(arr)),
            'std': float(np.std(arr)),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'count': len(ratios),
        }
    print("\n=== Approximation Ratio Summary ===")
    for alg in sorted(summary.keys(), key=lambda a: summary[a]['mean']):
        s = summary[alg]
        print(f"  {alg:20s}: mean={s['mean']:.3f}, median={s['median']:.3f}, "
              f"std={s['std']:.3f}, min={s['min']:.3f}, max={s['max']:.3f}, n={s['count']}")

    # Paired Wilcoxon signed-rank tests: hybrid vs each baseline
    comparisons = {}
    hybrid_key = 'hybrid'
    baselines = ['greedy', 'modified_greedy', 'lp_rounding', 'separator',
                 'planar_lp', 'baker_k3']

    # Get paired data (same instance)
    instance_results = {}
    for r in with_ratio:
        inst = r['instance_name']
        if inst not in instance_results:
            instance_results[inst] = {}
        instance_results[inst][r['algorithm']] = r['approx_ratio_vs_lp']

    print("\n=== Paired Wilcoxon Tests (Hybrid vs Baselines) ===")
    for baseline in baselines:
        hybrid_vals = []
        baseline_vals = []
        for inst, algs in instance_results.items():
            if hybrid_key in algs and baseline in algs:
                hybrid_vals.append(algs[hybrid_key])
                baseline_vals.append(algs[baseline])

        if len(hybrid_vals) < 5:
            print(f"  {baseline}: insufficient paired data ({len(hybrid_vals)} pairs)")
            comparisons[baseline] = {
                'n_pairs': len(hybrid_vals),
                'p_value': None,
                'effect_size': None,
                'hybrid_better': None,
            }
            continue

        h = np.array(hybrid_vals)
        b = np.array(baseline_vals)
        diffs = b - h  # positive = hybrid is better

        # Wilcoxon signed-rank test
        try:
            stat, p_value = stats.wilcoxon(h, b, alternative='less')
        except ValueError:
            # All differences are zero
            stat, p_value = 0, 1.0

        # Effect size: rank-biserial correlation
        n = len(diffs)
        if n > 0:
            ranks = stats.rankdata(np.abs(diffs))
            pos_ranks = sum(ranks[diffs > 0])
            neg_ranks = sum(ranks[diffs < 0])
            r_rb = (pos_ranks - neg_ranks) / (n * (n + 1) / 2) if n > 0 else 0
        else:
            r_rb = 0

        hybrid_better_pct = np.mean(h < b) * 100

        comparisons[baseline] = {
            'n_pairs': len(hybrid_vals),
            'p_value': float(p_value),
            'effect_size_rank_biserial': float(r_rb),
            'hybrid_mean': float(np.mean(h)),
            'baseline_mean': float(np.mean(b)),
            'hybrid_better_pct': float(hybrid_better_pct),
        }

        sig = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
        print(f"  {baseline:20s}: p={p_value:.4f} {sig}, r_rb={r_rb:.3f}, "
              f"hybrid_better={hybrid_better_pct:.0f}%, n={len(hybrid_vals)}")

    # Save analysis
    analysis = {
        'summary': summary,
        'comparisons': comparisons,
        'significant_improvements': sum(
            1 for c in comparisons.values()
            if c.get('p_value') is not None and c['p_value'] < 0.05
        ),
    }

    output_path = os.path.join(os.path.dirname(__file__), 'statistical_analysis.json')
    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"\nSaved to {output_path}")
    print(f"Significant improvements (p<0.05): {analysis['significant_improvements']}")

    return analysis


if __name__ == '__main__':
    analyze()
