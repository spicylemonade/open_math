#!/usr/bin/env python3
"""
Generate publication-quality figures for the Wythoff / C-finite research.

Figure 1: Bar chart of C-finite subsequence counts for quadratic irrationals,
          grouped by extraction strategy family.
Figure 2: Grouped bar chart comparing C-finite detection across CF structure classes.
"""

import json
import os
import re
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np

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

REPO = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(REPO, "results")
FIGURES = os.path.join(REPO, "figures")
os.makedirs(FIGURES, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────
# Helper: classify a strategy name into a human-readable family
# ──────────────────────────────────────────────────────────────────────
def strategy_family(name: str) -> str:
    if name.startswith("wythoff_row"):
        return "Wythoff row"
    if name.startswith("iterated_a_comp"):
        return "Iterated floor(a*n)"
    if name.startswith("iterated_comp"):
        return "Iterated comp."
    return "Other"


# ======================================================================
# FIGURE 1 — quadratic_recurrence_orders.png
# ======================================================================
def make_figure1():
    with open(os.path.join(RESULTS, "quadratic_experiments.json")) as f:
        data = json.load(f)

    # ------------------------------------------------------------------
    # Because best_order is universally 1 (trivial constant subsequence)
    # and the Wythoff-row recurrences are all order 2, a scatter plot of
    # "best order vs d" would be uninformative.  Instead we build a bar
    # chart showing, for a curated selection of quadratic irrationals,
    # the number of distinct C-finite subsequences found grouped by
    # extraction-strategy family.
    # ------------------------------------------------------------------

    # Build per-entry, per-strategy-family counts
    strategy_families_all = set()
    per_entry = []

    # Select a representative subset (every other entry, up to ~18)
    selected = data[::2][:18] if len(data) > 18 else data

    for entry in selected:
        raw = entry["name"]
        d = entry["discriminant_d"]

        # Build a nice short LaTeX label
        if "phi" in raw:
            short = r"$\varphi$"
        elif raw.startswith("sqrt("):
            short = r"$\sqrt{" + str(d) + r"}$"
        elif raw.startswith("(1+sqrt"):
            short = r"$\frac{1+\sqrt{" + str(d) + r"}}{2}$"
        elif "+sqrt" in raw:
            m = re.match(r"(\d+)\+sqrt\((\d+)\)", raw)
            if m:
                short = r"$" + m.group(1) + r"+\sqrt{" + m.group(2) + r"}$"
            else:
                short = raw
        else:
            short = raw

        counts = defaultdict(int)
        for rec in entry["all_recurrences"]:
            fam = strategy_family(rec["strategy"])
            counts[fam] += 1
            strategy_families_all.add(fam)
        per_entry.append((short, dict(counts), d))

    # Sorted strategy families for consistent ordering
    strat_fams = sorted(strategy_families_all)

    x_labels = [p[0] for p in per_entry]
    x = np.arange(len(x_labels))
    width = 0.8 / len(strat_fams)

    palette = sns.color_palette("deep", n_colors=len(strat_fams))

    fig, ax = plt.subplots(figsize=(12, 5.5))
    for i, sf in enumerate(strat_fams):
        vals = [p[1].get(sf, 0) for p in per_entry]
        bars = ax.bar(x + i * width - 0.4 + width / 2, vals, width,
                      label=sf, color=palette[i], edgecolor="white", linewidth=0.5)
        # Annotate bars
        for bar, v in zip(bars, vals):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                        str(v), ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel("Number of C-finite subsequences found")
    ax.set_xlabel("Quadratic irrational (discriminant $d$)")
    ax.set_title("C-finite Subsequence Counts by Extraction Strategy\n"
                 "for Quadratic Irrationals (Wythoff rows universally order 2)")
    ax.legend(title="Strategy family", loc="upper right")
    ax.set_ylim(0, ax.get_ylim()[1] * 1.15)

    # Add a text annotation about universality
    ax.annotate(
        "All Wythoff-row subsequences satisfy\na linear recurrence of order 2,\n"
        "confirming the universal pattern for\nquadratic irrationals.",
        xy=(0.02, 0.95), xycoords='axes fraction',
        fontsize=9, va='top', ha='left',
        bbox=dict(boxstyle='round,pad=0.4', fc='lightyellow', ec='0.7', alpha=0.95),
    )

    fig.tight_layout()
    for ext in ("png", "pdf"):
        path = os.path.join(FIGURES, f"quadratic_recurrence_orders.{ext}")
        fig.savefig(path, dpi=300)
        print(f"  Saved {path}")
    plt.close(fig)


# ======================================================================
# FIGURE 2 — cf_boundary_comparison.png
# ======================================================================
def make_figure2():
    with open(os.path.join(RESULTS, "cf_boundary_experiments.json")) as f:
        data = json.load(f)

    group_keys = [
        "group1_quadratic_bounded_cf",
        "group2_nonquadratic_bounded_cf",
        "group3_unbounded_cf",
    ]
    group_labels = [
        "Quadratic\n(bounded CF)",
        "Non-quadratic\nbounded CF",
        "Unbounded CF",
    ]

    avg_rec_counts = []
    avg_best_orders = []

    for gk in group_keys:
        entries = data[gk]
        rec_counts = [e["recurrences_found_count"] for e in entries]
        best_orders = [e["best_recurrence"]["order"]
                       for e in entries if e.get("best_recurrence")]
        avg_rec_counts.append(np.mean(rec_counts) if rec_counts else 0)
        avg_best_orders.append(np.mean(best_orders) if best_orders else 0)

    palette = sns.color_palette("muted", n_colors=2)
    x = np.arange(len(group_labels))
    width = 0.32

    fig, ax = plt.subplots(figsize=(8, 5))

    bars1 = ax.bar(x - width / 2, avg_rec_counts, width,
                   label="Avg. recurrences found", color=palette[0],
                   edgecolor="white", linewidth=0.6)
    bars2 = ax.bar(x + width / 2, avg_best_orders, width,
                   label="Avg. best (lowest) order", color=palette[1],
                   edgecolor="white", linewidth=0.6)

    # Value annotations on top of bars
    for bars in (bars1, bars2):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.3,
                    f"{height:.1f}", ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(group_labels, fontsize=11)
    ax.set_ylabel("Value")
    ax.set_title("Comparison of C-finite Subsequence Detection\nAcross CF Structure Classes")
    ax.legend(loc="upper left")
    ax.set_ylim(0, max(max(avg_rec_counts), max(avg_best_orders)) * 1.25)

    fig.tight_layout()
    for ext in ("png", "pdf"):
        path = os.path.join(FIGURES, f"cf_boundary_comparison.{ext}")
        fig.savefig(path, dpi=300)
        print(f"  Saved {path}")
    plt.close(fig)


# ======================================================================
if __name__ == "__main__":
    print("Generating Figure 1: quadratic_recurrence_orders")
    make_figure1()
    print()
    print("Generating Figure 2: cf_boundary_comparison")
    make_figure2()
    print()
    print("Done.")
