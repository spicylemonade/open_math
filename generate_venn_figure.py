#!/usr/bin/env python3
"""Generate the characterization Venn diagram and CF vs recurrence order figure."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
mpl.rcParams.update({
    'figure.figsize': (8, 5),
    'figure.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'legend.framealpha': 0.9,
    'legend.edgecolor': '0.8',
    'font.family': 'serif',
    'grid.alpha': 0.3,
    'grid.linewidth': 0.5,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

palette = sns.color_palette("muted")
# Assign colors
COLOR_TRANSCENDENTAL = palette[3]  # red-ish
COLOR_HIGHER_ALG     = palette[0]  # blue
COLOR_QUADRATIC      = palette[2]  # green
COLOR_RATIONAL       = palette[1]  # orange

# ─────────────────────────────────────────────────────────────────────
# Figure 1: Characterization Venn (nested-regions) diagram
# ─────────────────────────────────────────────────────────────────────

def draw_venn():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect('equal')
    ax.axis('off')

    # --- Outer rectangle: R > 0 (transcendental region) ---
    outer = mpatches.FancyBboxPatch(
        (0.02, 0.02), 0.96, 0.90,
        boxstyle="round,pad=0.02",
        linewidth=2.5, edgecolor='#444444',
        facecolor=(*COLOR_TRANSCENDENTAL[:3], 0.18),
    )
    ax.add_patch(outer)

    # --- Algebraic region (large inner rectangle) ---
    alg = mpatches.FancyBboxPatch(
        (0.06, 0.06), 0.58, 0.82,
        boxstyle="round,pad=0.02",
        linewidth=2.0, edgecolor='#333333',
        facecolor=(*COLOR_HIGHER_ALG[:3], 0.20),
    )
    ax.add_patch(alg)

    # --- Quadratic irrational region ---
    quad = mpatches.FancyBboxPatch(
        (0.10, 0.10), 0.38, 0.55,
        boxstyle="round,pad=0.02",
        linewidth=1.8, edgecolor='#333333',
        facecolor=(*COLOR_QUADRATIC[:3], 0.25),
    )
    ax.add_patch(quad)

    # --- Rational region (innermost) ---
    rat = mpatches.FancyBboxPatch(
        (0.14, 0.14), 0.22, 0.30,
        boxstyle="round,pad=0.02",
        linewidth=1.5, edgecolor='#333333',
        facecolor=(*COLOR_RATIONAL[:3], 0.35),
    )
    ax.add_patch(rat)

    # ---- Labels inside regions ----
    # Rational
    ax.text(0.25, 0.34, r"$\mathbb{Q}_{>0}$", fontsize=14, fontweight='bold',
            ha='center', va='center', color='#333333')
    ax.text(0.25, 0.26, r"$\lfloor nr \rfloor$ is itself", fontsize=9.5,
            ha='center', va='center', color='#444444')
    ax.text(0.25, 0.21, "C-finite (order q+1)", fontsize=9.5,
            ha='center', va='center', color='#444444')

    # Quadratic irrational
    ax.text(0.34, 0.56, "Quadratic Irrationals", fontsize=11, fontweight='bold',
            ha='center', va='center', color='#2a5e2a')
    ax.text(0.34, 0.50, r"e.g. $\varphi, \sqrt{2}, \sqrt{3}$", fontsize=9.5,
            ha='center', va='center', color='#444444', style='italic')
    ax.text(0.34, 0.45, "Order-2 Wythoff recurrence", fontsize=9.5,
            ha='center', va='center', color='#444444')

    # Higher-degree algebraic
    ax.text(0.50, 0.80, "Higher-Degree Algebraic", fontsize=11, fontweight='bold',
            ha='center', va='center', color='#1a3a6e')
    ax.text(0.50, 0.74, r"e.g. $2^{1/3}$, plastic ratio", fontsize=9.5,
            ha='center', va='center', color='#444444', style='italic')
    ax.text(0.50, 0.69, "Higher-order recurrences", fontsize=9.5,
            ha='center', va='center', color='#444444')
    ax.text(0.50, 0.64, "(Ballot / Fraenkel)", fontsize=9.5,
            ha='center', va='center', color='#444444')

    # Transcendental
    ax.text(0.82, 0.72, "Transcendental", fontsize=12, fontweight='bold',
            ha='center', va='center', color='#8b2020')
    ax.text(0.82, 0.65, r"e.g. $\pi,\; e,\; \ln 2$", fontsize=10,
            ha='center', va='center', color='#555555', style='italic')
    ax.text(0.82, 0.58, "NO C-finite", fontsize=10,
            ha='center', va='center', color='#8b2020', fontweight='bold')
    ax.text(0.82, 0.53, "subsequence", fontsize=10,
            ha='center', va='center', color='#8b2020', fontweight='bold')

    # ---- Bracket annotations showing C-finite boundary ----
    bracket_x = 0.035
    ax.annotate('', xy=(bracket_x, 0.06), xytext=(bracket_x, 0.88),
                arrowprops=dict(arrowstyle='-', color='#228B22', lw=3.5))
    # small ticks at top and bottom
    ax.plot([bracket_x - 0.008, bracket_x + 0.008], [0.06, 0.06],
            color='#228B22', lw=3.5)
    ax.plot([bracket_x - 0.008, bracket_x + 0.008], [0.88, 0.88],
            color='#228B22', lw=3.5)
    ax.text(bracket_x - 0.015, 0.47, "C-finite\nBeatty\nsubseq.\nexists",
            fontsize=8.5, fontweight='bold', color='#228B22',
            ha='right', va='center', rotation=0,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#228B22', alpha=0.9))

    # Draw a red X annotation on the transcendental side
    ax.text(0.82, 0.40, r"$\times$", fontsize=28, color='#CC3333',
            ha='center', va='center', fontweight='bold')
    ax.text(0.82, 0.33, "No C-finite\nsubsequence", fontsize=9,
            ha='center', va='center', color='#CC3333')

    # ---- Outer label: R > 0 ----
    ax.text(0.50, 0.96, r"$\mathbb{R}_{>0}$  (Real numbers $> 0$)",
            fontsize=13, fontweight='bold', ha='center', va='center',
            color='#222222',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#666666', alpha=0.95))

    # ---- Legend ----
    legend_elements = [
        mpatches.Patch(facecolor=(*COLOR_RATIONAL[:3], 0.5),
                       edgecolor='#333', label='Rational (order q+1)'),
        mpatches.Patch(facecolor=(*COLOR_QUADRATIC[:3], 0.5),
                       edgecolor='#333', label='Quadratic irrational (order 2)'),
        mpatches.Patch(facecolor=(*COLOR_HIGHER_ALG[:3], 0.5),
                       edgecolor='#333', label='Algebraic deg $\\geq$ 3'),
        mpatches.Patch(facecolor=(*COLOR_TRANSCENDENTAL[:3], 0.35),
                       edgecolor='#333', label='Transcendental (no C-finite)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              framealpha=0.95, edgecolor='0.7', borderpad=0.8)

    ax.set_title("Classification of Real Numbers by C-finite Beatty Subsequence Existence",
                 fontsize=13, fontweight='bold', pad=12)

    fig.savefig("figures/characterization_venn.png", dpi=300)
    fig.savefig("figures/characterization_venn.pdf")
    plt.close(fig)
    print("Saved figures/characterization_venn.png and .pdf")


# ─────────────────────────────────────────────────────────────────────
# Figure 2: CF vs recurrence order scatter/strip plot
# ─────────────────────────────────────────────────────────────────────

def draw_cf_vs_recurrence():
    # --- Experimental data ---
    # Rational: order = q+1 for denominator q
    rational_orders = [q + 1 for q in range(1, 11)]

    # Quadratic irrationals: all order 2
    quadratic_orders = [2] * 8

    # Algebraic degree >= 3
    higher_alg_orders = [4, 5]

    # Transcendental
    trans_orders = [25, 25, 12, 8]

    # Build arrays
    categories = []
    orders = []

    for o in rational_orders:
        categories.append("Rational")
        orders.append(o)
    for o in quadratic_orders:
        categories.append("Quadratic")
        orders.append(o)
    for o in higher_alg_orders:
        categories.append(r"Algebraic deg$\geq$3")
        orders.append(o)
    for o in trans_orders:
        categories.append("Transcendental")
        orders.append(o)

    cat_order = ["Rational", "Quadratic", r"Algebraic deg$\geq$3", "Transcendental"]
    cat_colors = {
        "Rational": COLOR_RATIONAL,
        "Quadratic": COLOR_QUADRATIC,
        r"Algebraic deg$\geq$3": COLOR_HIGHER_ALG,
        "Transcendental": COLOR_TRANSCENDENTAL,
    }

    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Map categories to numeric x positions
    cat_to_x = {c: i for i, c in enumerate(cat_order)}
    np.random.seed(42)

    for cat in cat_order:
        # Get orders for this category
        cat_ords = [o for c, o in zip(categories, orders) if c == cat]
        x_base = cat_to_x[cat]
        jitter = np.random.uniform(-0.18, 0.18, size=len(cat_ords))
        xs = x_base + jitter
        ax.scatter(xs, cat_ords, color=cat_colors[cat], s=70, alpha=0.8,
                   edgecolors='white', linewidth=0.6, zorder=5)

    # Horizontal line at y=2 (quadratic boundary)
    ax.axhline(y=2, color='#228B22', linestyle='--', linewidth=1.8, alpha=0.7,
               zorder=3, label='Quadratic boundary (order 2)')

    # Add annotation for the boundary line
    ax.text(3.35, 2.6, "Quadratic\nboundary", fontsize=9, color='#228B22',
            ha='center', va='bottom', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='#228B22', alpha=0.85))

    ax.set_xticks(range(len(cat_order)))
    ax.set_xticklabels(cat_order, fontsize=10.5)
    ax.set_ylabel("Best (Lowest) Non-trivial Recurrence Order", fontsize=12)
    ax.set_xlabel("Number Type", fontsize=12)
    ax.set_title("Best Recurrence Order Found by Number Type",
                 fontsize=13, fontweight='bold', pad=10)

    # y-axis formatting
    ax.set_ylim(0, 28)
    ax.set_yticks([0, 2, 5, 10, 15, 20, 25])

    # Legend
    legend_patches = [
        mpatches.Patch(color=cat_colors[c], label=c) for c in cat_order
    ]
    legend_patches.append(
        plt.Line2D([0], [0], color='#228B22', linestyle='--', linewidth=1.8,
                   label='Quadratic boundary (order 2)')
    )
    ax.legend(handles=legend_patches, loc='upper left', fontsize=9,
              framealpha=0.95, edgecolor='0.7')

    # Annotate a few key points
    ax.annotate(r"$\pi$", xy=(3 - 0.10, 25), xytext=(3 - 0.35, 27),
                fontsize=8, color='#555', ha='center',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.8))
    ax.annotate(r"$e$", xy=(3 + 0.10, 25), xytext=(3 + 0.35, 27),
                fontsize=8, color='#555', ha='center',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.8))
    ax.annotate("plastic\nratio", xy=(2 - 0.05, 4), xytext=(2 - 0.4, 7),
                fontsize=7.5, color='#555', ha='center',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.8))

    fig.savefig("figures/cf_vs_recurrence.png", dpi=300)
    fig.savefig("figures/cf_vs_recurrence.pdf")
    plt.close(fig)
    print("Saved figures/cf_vs_recurrence.png and .pdf")


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    os.makedirs("figures", exist_ok=True)
    draw_venn()
    draw_cf_vs_recurrence()
    print("All figures generated successfully.")
