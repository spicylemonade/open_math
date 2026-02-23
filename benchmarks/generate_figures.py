"""Generate all publication-quality figures for the research report."""

import os
import sys
import json
import numpy as np
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

FIGURES_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

# Common styling
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'legend.fontsize': 10,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

COLORS = {
    'greedy': '#1f77b4',
    'modified_greedy': '#ff7f0e',
    'lp_rounding': '#2ca02c',
    'separator': '#d62728',
    'planar_lp': '#9467bd',
    'baker_k2': '#bcbd22',
    'baker_k3': '#8c564b',
    'baker_k5': '#17becf',
    'hybrid': '#e377c2',
}

LABELS = {
    'greedy': 'Greedy',
    'modified_greedy': 'Mod. Greedy',
    'lp_rounding': 'LP Rounding',
    'separator': 'Separator',
    'planar_lp': 'Planar LP',
    'baker_k2': "Baker (k=2)",
    'baker_k3': "Baker (k=3)",
    'baker_k5': "Baker (k=5)",
    'hybrid': 'Hybrid (ours)',
}

ALG_ORDER = ['hybrid', 'separator', 'planar_lp', 'greedy', 'modified_greedy',
             'baker_k5', 'lp_rounding', 'baker_k3', 'baker_k2']


def load_results():
    with open(os.path.join(RESULTS_DIR, 'full_results.json')) as f:
        return json.load(f)


def save_fig(fig, name):
    for ext in ['png', 'pdf']:
        path = os.path.join(FIGURES_DIR, f'{name}.{ext}')
        fig.savefig(path)
    print(f"  Saved {name}.png and {name}.pdf")


def fig1_ratio_comparison(results):
    """Bar chart comparing mean approximation ratios across algorithms."""
    with_ratio = [r for r in results if r['approx_ratio_vs_lp'] is not None]

    alg_ratios = defaultdict(list)
    for r in with_ratio:
        alg_ratios[r['algorithm']].append(r['approx_ratio_vs_lp'])

    algs = [a for a in ALG_ORDER if a in alg_ratios]
    means = [np.mean(alg_ratios[a]) for a in algs]
    stds = [np.std(alg_ratios[a]) for a in algs]
    colors = [COLORS.get(a, 'gray') for a in algs]

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(algs))
    bars = ax.bar(x, means, yerr=stds, capsize=4, color=colors, edgecolor='black',
                  linewidth=0.5, alpha=0.85)

    # Highlight hybrid bar
    bars[0].set_edgecolor('#333333')
    bars[0].set_linewidth(2)

    ax.set_xticks(x)
    ax.set_xticklabels([LABELS.get(a, a) for a in algs], rotation=30, ha='right')
    ax.set_ylabel('Mean Approximation Ratio (vs LP Lower Bound)')
    ax.set_title('Approximation Ratio Comparison Across Algorithms')
    ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, linewidth=0.8)
    ax.set_ylim(0.8, max(means) * 1.15)

    # Add value labels
    for i, (m, s) in enumerate(zip(means, stds)):
        ax.text(i, m + s + 0.05, f'{m:.3f}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    save_fig(fig, 'ratio_comparison')
    plt.close()


def fig2_ratio_distribution(results):
    """Box/violin plot of ratio distributions per algorithm."""
    with_ratio = [r for r in results if r['approx_ratio_vs_lp'] is not None]

    alg_ratios = defaultdict(list)
    for r in with_ratio:
        alg_ratios[r['algorithm']].append(r['approx_ratio_vs_lp'])

    algs = [a for a in ALG_ORDER if a in alg_ratios]
    data = [alg_ratios[a] for a in algs]

    fig, ax = plt.subplots(figsize=(12, 7))

    # Violin plot
    parts = ax.violinplot(data, positions=range(len(algs)), showmeans=True,
                          showmedians=True, showextrema=True)
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(COLORS.get(algs[i], 'gray'))
        pc.set_alpha(0.6)
    parts['cmeans'].set_color('red')
    parts['cmedians'].set_color('black')

    # Overlay individual points with jitter
    rng = np.random.RandomState(42)
    for i, (alg, vals) in enumerate(zip(algs, data)):
        jitter = rng.uniform(-0.15, 0.15, len(vals))
        ax.scatter([i + j for j in jitter], vals, s=12, alpha=0.4,
                   color=COLORS.get(alg, 'gray'), zorder=5)

    ax.set_xticks(range(len(algs)))
    ax.set_xticklabels([LABELS.get(a, a) for a in algs], rotation=30, ha='right')
    ax.set_ylabel('Approximation Ratio (vs LP Lower Bound)')
    ax.set_title('Distribution of Approximation Ratios')
    ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, linewidth=0.8)

    # Legend for mean/median
    ax.plot([], [], 'r-', label='Mean', linewidth=1.5)
    ax.plot([], [], 'k-', label='Median', linewidth=1.5)
    ax.legend(loc='upper right')

    plt.tight_layout()
    save_fig(fig, 'ratio_distribution')
    plt.close()


def fig3_ratio_vs_size(results):
    """Scatter plot of ratio vs graph size, colored by algorithm."""
    with_ratio = [r for r in results if r['approx_ratio_vs_lp'] is not None]

    fig, ax = plt.subplots(figsize=(12, 7))

    main_algs = ['hybrid', 'greedy', 'separator', 'planar_lp', 'lp_rounding', 'baker_k3']

    markers = {
        'hybrid': '*', 'greedy': 'o', 'separator': 'D',
        'planar_lp': 'v', 'lp_rounding': '^', 'baker_k3': 'P',
        'modified_greedy': 's', 'baker_k2': 'X', 'baker_k5': 'p',
    }

    for alg in main_algs:
        alg_data = [r for r in with_ratio if r['algorithm'] == alg]
        if not alg_data:
            continue
        sizes = [r['n'] for r in alg_data]
        ratios = [r['approx_ratio_vs_lp'] for r in alg_data]
        ax.scatter(sizes, ratios,
                   label=LABELS.get(alg, alg),
                   color=COLORS.get(alg, 'gray'),
                   marker=markers.get(alg, 'o'),
                   s=60 if alg == 'hybrid' else 40,
                   alpha=0.7,
                   edgecolors='black' if alg == 'hybrid' else 'none',
                   linewidths=0.5 if alg == 'hybrid' else 0)

    ax.set_xscale('log')
    ax.set_xlabel('Number of Nodes (n)')
    ax.set_ylabel('Approximation Ratio (vs LP Lower Bound)')
    ax.set_title('Approximation Ratio vs Graph Size')
    ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, linewidth=0.8)
    ax.legend(loc='upper right', framealpha=0.9)

    plt.tight_layout()
    save_fig(fig, 'ratio_vs_size')
    plt.close()


def fig4_algorithm_pipeline():
    """Algorithm pipeline/flowchart diagram."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Hybrid MDS Algorithm Pipeline', fontsize=18, fontweight='bold', pad=20)

    # Box style
    bbox_main = dict(boxstyle='round,pad=0.4', facecolor='#E8F4FD', edgecolor='#2196F3', linewidth=2)
    bbox_sub = dict(boxstyle='round,pad=0.3', facecolor='#FFF3E0', edgecolor='#FF9800', linewidth=1.5)
    bbox_result = dict(boxstyle='round,pad=0.4', facecolor='#E8F5E9', edgecolor='#4CAF50', linewidth=2)
    bbox_input = dict(boxstyle='round,pad=0.4', facecolor='#F3E5F5', edgecolor='#9C27B0', linewidth=2)

    # Input
    ax.text(7, 7.3, 'Input: Planar Graph G = (V, E)', fontsize=13, ha='center',
            va='center', bbox=bbox_input, fontweight='bold')

    # Four parallel strategies
    strategies = [
        (2.0, 5.0, 'Strategy 1:\nGreedy MDS'),
        (5.0, 5.0, 'Strategy 2:\nMod. Greedy'),
        (8.5, 5.0, 'Strategy 3:\nSeparator\nDecomposition'),
        (12.0, 5.0, 'Strategy 4:\nPlanar LP\nRounding'),
    ]

    for x, y, text in strategies:
        ax.text(x, y, text, fontsize=10, ha='center', va='center', bbox=bbox_sub)

    # Local search
    for x, _, _ in strategies:
        ax.text(x, 3.2, 'Local Search\n(1-swap + 2-swap)', fontsize=9, ha='center',
                va='center', bbox=bbox_main)

    # Arrows from input to strategies
    for x, y, _ in strategies:
        ax.annotate('', xy=(x, y + 0.7), xytext=(7, 6.9),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))

    # Arrows from strategies to local search
    for x, y, _ in strategies:
        ax.annotate('', xy=(x, 3.8), xytext=(x, y - 0.7),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))

    # Selection
    ax.text(7, 1.5, 'Select Best Solution\n(minimum |D|)', fontsize=12, ha='center',
            va='center', bbox=bbox_result, fontweight='bold')

    # Arrows from local search to selection
    for x, _, _ in strategies:
        ax.annotate('', xy=(7, 2.1), xytext=(x, 2.6),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))

    # Output
    ax.text(7, 0.3, 'Output: Dominating Set D with |D| \u2264 4\u00b7OPT + 3\u221an',
            fontsize=12, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFEBEE', edgecolor='#F44336', linewidth=2),
            fontweight='bold')

    ax.annotate('', xy=(7, 0.7), xytext=(7, 1.0),
                arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))

    plt.tight_layout()
    save_fig(fig, 'algorithm_pipeline')
    plt.close()


def fig5_exact_validation():
    """Bar chart of exact ratios from ILP validation."""
    summary_path = os.path.join(os.path.dirname(__file__), 'exact_validation_summary.json')
    with open(summary_path) as f:
        summary = json.load(f)

    algs = ['hybrid', 'separator', 'planar_lp', 'greedy', 'modified_greedy', 'lp_rounding']
    algs = [a for a in algs if a in summary and isinstance(summary[a], dict)]

    means = [summary[a]['mean'] for a in algs]
    maxes = [summary[a]['max'] for a in algs]
    opt_pcts = [summary[a]['optimal_pct'] for a in algs]
    colors = [COLORS.get(a, 'gray') for a in algs]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Mean and max exact ratios
    x = np.arange(len(algs))
    width = 0.35
    bars1 = ax1.bar(x - width / 2, means, width, label='Mean', color=colors, alpha=0.7,
                    edgecolor='black', linewidth=0.5)
    bars2 = ax1.bar(x + width / 2, maxes, width, label='Worst Case', color=colors, alpha=0.4,
                    edgecolor='black', linewidth=0.5, hatch='//')

    ax1.set_xticks(x)
    ax1.set_xticklabels([LABELS.get(a, a) for a in algs], rotation=30, ha='right')
    ax1.set_ylabel('Approximation Ratio (vs ILP Optimal)')
    ax1.set_title('Exact Approximation Ratios (n \u2264 200)')
    ax1.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, linewidth=0.8)
    ax1.legend()

    for i, m in enumerate(means):
        ax1.text(i - width / 2, m + 0.02, f'{m:.3f}', ha='center', va='bottom', fontsize=8)

    # Optimal percentage
    ax2.bar(x, opt_pcts, color=colors, edgecolor='black', linewidth=0.5, alpha=0.85)
    ax2.set_xticks(x)
    ax2.set_xticklabels([LABELS.get(a, a) for a in algs], rotation=30, ha='right')
    ax2.set_ylabel('Percentage of Instances with Optimal Solution (%)')
    ax2.set_title('Optimality Rate (n \u2264 200)')
    ax2.set_ylim(0, 110)

    for i, p in enumerate(opt_pcts):
        ax2.text(i, p + 2, f'{p:.0f}%', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    save_fig(fig, 'exact_validation')
    plt.close()


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)

    results = load_results()
    print("Generating figures...")

    print("Figure 1: Ratio comparison bar chart")
    fig1_ratio_comparison(results)

    print("Figure 2: Ratio distribution violin plot")
    fig2_ratio_distribution(results)

    print("Figure 3: Ratio vs size scatter plot")
    fig3_ratio_vs_size(results)

    print("Figure 4: Algorithm pipeline flowchart")
    fig4_algorithm_pipeline()

    print("Figure 5: Exact validation results")
    fig5_exact_validation()

    print(f"\nAll figures saved to {FIGURES_DIR}/")
    print("Figures: ratio_comparison, ratio_distribution, ratio_vs_size, algorithm_pipeline, exact_validation, scalability")


if __name__ == '__main__':
    main()
