#!/usr/bin/env python3
"""
Generate publication-quality figures for Beatty sequence research project.

Research result: floor(n*r) contains a homogeneous linearly recurrent
subsequence if and only if r is rational.
"""

import json
import math
import ast
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from fractions import Fraction

# Reproducibility
np.random.seed(42)

# Global style
plt.style.use('seaborn-v0_8-whitegrid')

# ============================================================
# FIGURE 1: Beatty Sequence and Linearly Recurrent Subsequence
#            for Rational r = 3/2
# ============================================================

def make_figure1():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Compute the Beatty sequence for r = 3/2
    n_vals = list(range(1, 51))
    seq = [(n * 3) // 2 for n in n_vals]

    # Plot full sequence as blue dots
    ax.plot(n_vals, seq, 'o', color='#2171B5', markersize=5, label=r'$\lfloor n \cdot 3/2 \rfloor$', zorder=3)

    # AP subsequence with d=2 (every other term: n=1,3,5,...)
    ap_indices = list(range(0, 50, 2))  # 0-based indices for d=2 starting at n=1
    ap_n = [n_vals[i] for i in ap_indices]
    ap_seq = [seq[i] for i in ap_indices]

    ax.plot(ap_n, ap_seq, 'o', color='#CB181D', markersize=10, markerfacecolor='none',
            markeredgewidth=2, label=r'AP subsequence ($d=2$: $n=1,3,5,\ldots$)', zorder=4)

    # Connect AP subsequence with a dashed line to show linearity
    ax.plot(ap_n, ap_seq, '--', color='#CB181D', alpha=0.4, linewidth=1, zorder=2)

    # Annotate the recurrence relation
    ax.annotate(
        r'Recurrence: $a_{n+3} - a_{n+2} - a_{n+1} + a_n = 0$'
        '\n'
        r'(on the AP subsequence with $d=2$)',
        xy=(30, seq[29]),
        xytext=(10, 60),
        fontsize=11,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='gray', alpha=0.9),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='gray'),
        zorder=5
    )

    # Verify and annotate: show that the recurrence holds on the AP subseq
    # AP subsequence values: for n=1,3,5,...,49 -> indices 0,2,4,...,48
    ap_vals = ap_seq
    # Check: a_{k+3} - a_{k+2} - a_{k+1} + a_k = 0 for consecutive AP terms
    residuals_check = [ap_vals[k+3] - ap_vals[k+2] - ap_vals[k+1] + ap_vals[k]
                       for k in range(len(ap_vals) - 3)]
    all_zero = all(r == 0 for r in residuals_check)

    # Add a small verification note
    ax.text(0.02, 0.98,
            f'Verification: all residuals = 0? {all_zero}',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            fontstyle='italic', color='#2171B5',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('$n$', fontsize=13)
    ax.set_ylabel(r'$\lfloor n \cdot r \rfloor$', fontsize=13)
    ax.set_title('Beatty Sequence and Linearly Recurrent Subsequence for Rational $r = 3/2$',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
    ax.tick_params(labelsize=11)

    plt.tight_layout()
    plt.savefig('/home/codex/work/repo/figures/beatty_rational_recurrence.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Figure 1 saved: figures/beatty_rational_recurrence.png")


# ============================================================
# FIGURE 2: Recurrence Residuals for Irrational r = golden ratio
# ============================================================

def make_figure2():
    fig, ax = plt.subplots(figsize=(10, 6))

    phi = (1 + math.sqrt(5)) / 2
    seq = [math.floor(n * phi) for n in range(1, 201)]

    # Residuals: R_n = a_{n+3} - a_{n+2} - a_{n+1} + a_n
    # Using 0-based indexing: seq[n+2] - seq[n+1] - seq[n] + seq[n-1] for n=1..197
    # which corresponds to a_{n+3} - a_{n+2} - a_{n+1} + a_n in 1-based
    residuals = [seq[n+2] - seq[n+1] - seq[n] + seq[n-1] for n in range(1, 198)]
    n_res = list(range(1, 198))

    # Color residuals by value
    colors = []
    for r in residuals:
        if r == -1:
            colors.append('#CB181D')   # red
        elif r == 0:
            colors.append('#2171B5')   # blue
        elif r == 1:
            colors.append('#238B45')   # green
        else:
            colors.append('gray')

    ax.scatter(n_res, residuals, c=colors, s=12, alpha=0.8, zorder=3)

    # Add horizontal reference lines
    ax.axhline(y=0, color='black', linewidth=0.8, linestyle='-', alpha=0.5)
    ax.axhline(y=1, color='#238B45', linewidth=0.5, linestyle='--', alpha=0.4)
    ax.axhline(y=-1, color='#CB181D', linewidth=0.5, linestyle='--', alpha=0.4)

    # Count residual values
    from collections import Counter
    counts = Counter(residuals)

    # Add statistics annotation
    stats_text = (
        f'Residual distribution:\n'
        f'  $R_n = -1$: {counts.get(-1, 0)} times\n'
        f'  $R_n = \\;\\;0$: {counts.get(0, 0)} times\n'
        f'  $R_n = +1$: {counts.get(1, 0)} times\n\n'
        r'$\Rightarrow$ Recurrence $a_{{n+3}} - a_{{n+2}} - a_{{n+1}} + a_n = 0$'
        '\n'
        r'does NOT hold for irrational $\varphi$'
    )
    ax.text(0.62, 0.95, stats_text,
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9),
            fontfamily='monospace')

    # Custom legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#CB181D',
                   markersize=8, label='$R_n = -1$'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2171B5',
                   markersize=8, label='$R_n = 0$'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#238B45',
                   markersize=8, label='$R_n = +1$'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.9)

    ax.set_xlabel('$n$', fontsize=13)
    ax.set_ylabel('Residual $R_n$', fontsize=13)
    ax.set_title(r'Recurrence Residuals for Irrational $r = \varphi = (1+\sqrt{5})/2$',
                 fontsize=14, fontweight='bold')
    ax.set_ylim(-1.8, 1.8)
    ax.set_yticks([-1, 0, 1])
    ax.tick_params(labelsize=11)

    plt.tight_layout()
    plt.savefig('/home/codex/work/repo/figures/recurrence_residuals_irrational.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Figure 2 saved: figures/recurrence_residuals_irrational.png")


# ============================================================
# FIGURE 3: Recurrence Detection Across r-Values and Classes
# ============================================================

def make_figure3():
    with open('/home/codex/work/repo/results/large_scale_search.json', 'r') as f:
        data = json.load(f)

    # Count by r_type and recurrence_found
    type_order = ['rational', 'quadratic_irrational', 'algebraic_degree_ge3', 'transcendental']
    type_labels = ['Rational', 'Quadratic\nIrrational', 'Algebraic\n(degree $\\geq 3$)', 'Transcendental']

    found_counts = {t: 0 for t in type_order}
    not_found_counts = {t: 0 for t in type_order}

    for entry in data:
        rt = entry['r_type']
        if rt in found_counts:
            if entry['recurrence_found']:
                found_counts[rt] += 1
            else:
                not_found_counts[rt] += 1

    found_vals = [found_counts[t] for t in type_order]
    not_found_vals = [not_found_counts[t] for t in type_order]

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(type_order))
    width = 0.35

    bars_found = ax.bar(x - width/2, found_vals, width, label='Recurrence Found',
                        color='#2CA02C', edgecolor='white', linewidth=0.8, zorder=3)
    bars_not = ax.bar(x + width/2, not_found_vals, width, label='No Recurrence Found',
                      color='#D62728', edgecolor='white', linewidth=0.8, zorder=3)

    # Add count labels on top of bars
    for bar in bars_found:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 4), textcoords='offset points',
                        ha='center', va='bottom', fontsize=12, fontweight='bold',
                        color='#2CA02C')

    for bar in bars_not:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 4), textcoords='offset points',
                        ha='center', va='bottom', fontsize=12, fontweight='bold',
                        color='#D62728')

    ax.set_xlabel('Number Class of $r$', fontsize=13)
    ax.set_ylabel('Count', fontsize=13)
    ax.set_title('Recurrence Detection Across $r$-Values and Number Classes',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(type_labels, fontsize=11)
    ax.legend(fontsize=12, framealpha=0.9, loc='upper right')
    ax.tick_params(labelsize=11)

    # Add summary annotation
    total_rational = found_counts['rational'] + not_found_counts['rational']
    total_irrational = sum(found_counts[t] + not_found_counts[t] for t in type_order[1:])
    ax.text(0.02, 0.95,
            f'Total: {total_rational} rational ($100\\%$ found), '
            f'{total_irrational} irrational ($0\\%$ found)',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9))

    # Set y-axis to nice range
    max_val = max(max(found_vals), max(not_found_vals))
    ax.set_ylim(0, max_val * 1.2)

    plt.tight_layout()
    plt.savefig('/home/codex/work/repo/figures/heatmap_recurrence_detection.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Figure 3 saved: figures/heatmap_recurrence_detection.png")


# ============================================================
# FIGURE 4: Continued Fraction Structure vs Recurrence Detection
# ============================================================

def make_figure4():
    with open('/home/codex/work/repo/results/large_scale_search.json', 'r') as f:
        data = json.load(f)

    # Color map for r_type
    color_map = {
        'rational': '#2CA02C',
        'quadratic_irrational': '#D62728',
        'algebraic_degree_ge3': '#FF7F0E',
        'transcendental': '#9467BD'
    }
    label_map = {
        'rational': 'Rational',
        'quadratic_irrational': 'Quadratic Irrational',
        'algebraic_degree_ge3': r'Algebraic (degree $\geq 3$)',
        'transcendental': 'Transcendental'
    }

    # Parse data
    plot_data = {rt: {'x': [], 'y': []} for rt in color_map}

    for entry in data:
        cf_str = entry.get('cf_partial_quotients_50', '')
        if not cf_str or cf_str == '':
            continue

        try:
            cf_list = ast.literal_eval(cf_str)
        except (ValueError, SyntaxError):
            continue

        # Take first 20 partial quotients (or fewer if not available)
        cf_20 = cf_list[:20]
        if len(cf_20) == 0:
            continue

        max_pq = max(cf_20)
        recurrence_found = 1 if entry['recurrence_found'] else 0
        rt = entry['r_type']

        if rt in plot_data:
            # Add small jitter for visibility (especially for y which is 0/1)
            jitter_y = np.random.uniform(-0.06, 0.06)
            # Use multiplicative jitter to keep values positive on log scale
            jitter_x_factor = np.random.uniform(0.85, 1.15)
            plot_data[rt]['x'].append(max(0.5, max_pq * jitter_x_factor))
            plot_data[rt]['y'].append(recurrence_found + jitter_y)

    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot each category with its own style
    marker_map = {
        'rational': 'o',
        'quadratic_irrational': 's',
        'algebraic_degree_ge3': 'D',
        'transcendental': '^'
    }
    size_map = {
        'rational': 60,
        'quadratic_irrational': 60,
        'algebraic_degree_ge3': 60,
        'transcendental': 80
    }

    plot_order = ['rational', 'quadratic_irrational', 'algebraic_degree_ge3', 'transcendental']

    for rt in plot_order:
        if plot_data[rt]['x']:
            ax.scatter(plot_data[rt]['x'], plot_data[rt]['y'],
                       c=color_map[rt], marker=marker_map[rt], s=size_map[rt],
                       label=label_map[rt], alpha=0.75, edgecolors='white',
                       linewidths=0.5, zorder=3)

    # Add horizontal reference lines at y=0 and y=1
    ax.axhline(y=0, color='#D62728', linewidth=0.8, linestyle='--', alpha=0.3)
    ax.axhline(y=1, color='#2CA02C', linewidth=0.8, linestyle='--', alpha=0.3)

    # Label regions
    ax.text(0.98, 0.92, 'Recurrence Found', transform=ax.transAxes,
            fontsize=11, ha='right', va='top', color='#2CA02C', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    ax.text(0.98, 0.08, 'No Recurrence Found', transform=ax.transAxes,
            fontsize=11, ha='right', va='bottom', color='#D62728', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    ax.set_xlabel('Max of First 20 Continued Fraction Partial Quotients (log scale)', fontsize=13)
    ax.set_ylabel('Recurrence Found (1 = Yes, 0 = No)', fontsize=13)
    ax.set_title('Continued Fraction Structure vs. Recurrence Detection',
                 fontsize=14, fontweight='bold')

    ax.set_yticks([0, 1])
    ax.set_yticklabels(['No (0)', 'Yes (1)'], fontsize=11)
    ax.set_ylim(-0.25, 1.25)
    ax.tick_params(labelsize=11)

    # Use log scale for x -- all values are positive now
    ax.set_xscale('log')
    ax.set_xlim(left=0.4)

    ax.legend(loc='center left', fontsize=10, framealpha=0.9,
              bbox_to_anchor=(0.0, 0.5), borderaxespad=0.5)

    # Add interpretive annotation
    ax.annotate(
        'Rationals: low max PQ,\nrecurrence always found',
        xy=(3, 1.0), xytext=(30, 0.72),
        fontsize=9,
        arrowprops=dict(arrowstyle='->', color='gray'),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                  edgecolor='gray', alpha=0.9)
    )
    ax.annotate(
        'Irrationals: varied max PQ,\nno recurrence found',
        xy=(10, 0.0), xytext=(40, 0.28),
        fontsize=9,
        arrowprops=dict(arrowstyle='->', color='gray'),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                  edgecolor='gray', alpha=0.9)
    )

    plt.tight_layout()
    plt.savefig('/home/codex/work/repo/figures/cf_vs_recurrence.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Figure 4 saved: figures/cf_vs_recurrence.png")


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    make_figure1()
    make_figure2()
    make_figure3()
    make_figure4()
    print("\nAll 4 figures generated successfully.")
