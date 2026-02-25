#!/usr/bin/env python3
"""Generate publication-quality figures for the ATSP learned heuristics paper.

Reads results from CSV files in results/ and produces six PNG figures in figures/.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Global style configuration
# ---------------------------------------------------------------------------
plt.style.use("seaborn-v0_8-paper")
plt.rcParams.update({
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 150,
})

# Consistent colour palette (colour-blind friendly)
COLORS = {
    "nearest_neighbor": "#999999",
    "farthest_insertion": "#f1a340",
    "ortools": "#998ec3",
    "lkh_style": "#d73027",
    "hybrid": "#4575b4",
    # ablation configs
    "A_lkh_default": "#d73027",
    "B_learned_candidates": "#f1a340",
    "C_rl_only": "#999999",
    "D_full_hybrid": "#4575b4",
    # misc
    "learned": "#4575b4",
    "alpha": "#d73027",
}

SOLVER_LABELS = {
    "nearest_neighbor": "Nearest Neighbour",
    "farthest_insertion": "Farthest Insertion",
    "ortools": "OR-Tools",
    "lkh_style": "LKH-style",
    "hybrid": "Hybrid (ours)",
}

ABLATION_LABELS = {
    "A_lkh_default": "A: LKH default",
    "B_learned_candidates": "B: Learned cands.",
    "C_rl_only": "C: RL only",
    "D_full_hybrid": "D: Full hybrid",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(ROOT, "results")
FIGURES_DIR = os.path.join(ROOT, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def _save(fig, name):
    path = os.path.join(FIGURES_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")


# ===================================================================
# Figure 1 -- Solver comparison (grouped bar chart)
# ===================================================================
def fig1_solver_comparison():
    print("Generating fig1_solver_comparison.png ...")
    df = pd.read_csv(os.path.join(RESULTS_DIR, "full_comparison.csv"))
    df = df[df["time_limit"] == 30.0]
    solvers_order = ["nearest_neighbor", "farthest_insertion", "ortools", "lkh_style", "hybrid"]
    scales = sorted(df["n_stops"].unique())

    agg = (
        df.groupby(["n_stops", "solver"])["tour_cost"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    n_scales = len(scales)
    n_solvers = len(solvers_order)
    bar_width = 0.15
    x = np.arange(n_scales)

    for i, solver in enumerate(solvers_order):
        vals = []
        for s in scales:
            row = agg[(agg["n_stops"] == s) & (agg["solver"] == solver)]
            vals.append(row["tour_cost"].values[0] if len(row) else 0)
        ax.bar(
            x + i * bar_width,
            vals,
            bar_width,
            label=SOLVER_LABELS[solver],
            color=COLORS[solver],
            edgecolor="white",
            linewidth=0.5,
        )

    ax.set_xticks(x + bar_width * (n_solvers - 1) / 2)
    ax.set_xticklabels([f"{s} stops" for s in scales])
    ax.set_ylabel("Mean Tour Cost")
    ax.set_title("Solver Comparison (time limit = 30 s)")
    ax.legend(loc="upper left", frameon=True)
    ax.grid(axis="y", alpha=0.3)

    _save(fig, "fig1_solver_comparison.png")


# ===================================================================
# Figure 2 -- Scaling curve (time vs n_stops)
# ===================================================================
def fig2_scaling_curve():
    print("Generating fig2_scaling_curve.png ...")
    scalability_path = os.path.join(RESULTS_DIR, "scalability_results.csv")

    solvers_to_plot = ["ortools", "lkh_style", "hybrid"]

    if os.path.exists(scalability_path):
        df = pd.read_csv(scalability_path)
    else:
        df = pd.read_csv(os.path.join(RESULTS_DIR, "full_comparison.csv"))
        # Use time_limit=30 for fairest comparison
        df = df[df["time_limit"] == 30.0]

    agg = (
        df[df["solver"].isin(solvers_to_plot)]
        .groupby(["n_stops", "solver"])["time_s"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    for solver in solvers_to_plot:
        sub = agg[agg["solver"] == solver].sort_values("n_stops")
        ax.plot(
            sub["n_stops"],
            sub["time_s"],
            marker="o",
            label=SOLVER_LABELS[solver],
            color=COLORS[solver],
            linewidth=2,
            markersize=7,
        )

    ax.set_xlabel("Number of Stops")
    ax.set_ylabel("Mean Solve Time (s)")
    ax.set_title("Scaling Behaviour of Solvers")
    ax.legend(frameon=True)
    ax.grid(alpha=0.3)

    _save(fig, "fig2_scaling_curve.png")


# ===================================================================
# Figure 3 -- Gap histogram for hybrid solver
# ===================================================================
def fig3_gap_histogram():
    print("Generating fig3_gap_histogram.png ...")
    df = pd.read_csv(os.path.join(RESULTS_DIR, "full_comparison.csv"))
    df = df[(df["solver"] == "hybrid") & (df["time_limit"] == 30.0)]

    fig, ax = plt.subplots(figsize=(8, 5))
    gaps = df["gap_pct"].values

    ax.hist(
        gaps,
        bins=20,
        color=COLORS["hybrid"],
        edgecolor="white",
        linewidth=0.8,
        alpha=0.85,
    )
    median_gap = np.median(gaps)
    ax.axvline(median_gap, color="#d73027", linestyle="--", linewidth=1.5,
               label=f"Median = {median_gap:.2f}%")

    ax.set_xlabel("Optimality Gap (%)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Optimality Gaps (Hybrid Solver, 30 s)")
    ax.legend(frameon=True)
    ax.grid(axis="y", alpha=0.3)

    _save(fig, "fig3_gap_histogram.png")


# ===================================================================
# Figure 4 -- Ablation study (grouped bar chart)
# ===================================================================
def fig4_ablation():
    print("Generating fig4_ablation.png ...")
    df = pd.read_csv(os.path.join(RESULTS_DIR, "ablation_results.csv"))
    configs_order = ["A_lkh_default", "B_learned_candidates", "C_rl_only", "D_full_hybrid"]

    agg = df.groupby("config")["tour_cost"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(configs_order))
    bar_width = 0.55

    vals = []
    colors = []
    labels = []
    for cfg in configs_order:
        row = agg[agg["config"] == cfg]
        vals.append(row["tour_cost"].values[0] if len(row) else 0)
        colors.append(COLORS[cfg])
        labels.append(ABLATION_LABELS[cfg])

    bars = ax.bar(x, vals, bar_width, color=colors, edgecolor="white", linewidth=0.5)

    # Add value labels on bars
    for bar, val in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 50,
            f"{val:.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel("Mean Tour Cost")
    ax.set_title("Ablation Study (200-stop instances)")
    ax.grid(axis="y", alpha=0.3)

    # Tighten y-axis so differences are visible
    ymin = min(vals) * 0.92
    ymax = max(vals) * 1.06
    ax.set_ylim(ymin, ymax)

    _save(fig, "fig4_ablation.png")


# ===================================================================
# Figure 5 -- Candidate set recall (learned vs alpha-nearness)
# ===================================================================
def fig5_candidate_recall():
    print("Generating fig5_candidate_recall.png ...")
    k = [5, 10, 15, 20]
    learned = [0.945, 0.995, 1.0, 1.0]
    alpha = [0.915, 0.990, 1.0, 1.0]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(k, learned, marker="o", linewidth=2, markersize=7,
            color=COLORS["learned"], label="Learned candidates")
    ax.plot(k, alpha, marker="s", linewidth=2, markersize=7,
            color=COLORS["alpha"], linestyle="--", label=r"$\alpha$-nearness")

    ax.set_xlabel("Candidate Set Size (k)")
    ax.set_ylabel("Recall of Optimal Edges")
    ax.set_title("Candidate Set Quality: Learned vs. Alpha-Nearness")
    ax.set_xticks(k)
    ax.set_ylim(0.88, 1.02)
    ax.legend(frameon=True)
    ax.grid(alpha=0.3)

    _save(fig, "fig5_candidate_recall.png")


# ===================================================================
# Figure 6 -- Traffic / departure-time impact
# ===================================================================
def fig6_traffic_impact():
    print("Generating fig6_traffic_impact.png ...")
    times = [
        "Night\n(3 am)",
        "Morning Peak\n(8 am)",
        "Midday\n(12 pm)",
        "Evening Peak\n(5 pm)",
        "Evening\n(9 pm)",
    ]
    costs = [3681, 5274, 4100, 6619, 3900]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(times))
    bar_colors = ["#4575b4"] * len(times)
    # Highlight peaks
    bar_colors[1] = "#d73027"
    bar_colors[3] = "#d73027"

    bars = ax.bar(x, costs, width=0.6, color=bar_colors, edgecolor="white", linewidth=0.5)

    for bar, cost in zip(bars, costs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 60,
            f"{cost}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(times)
    ax.set_ylabel("Tour Cost")
    ax.set_title("Impact of Departure Time on Tour Cost")
    ax.grid(axis="y", alpha=0.3)

    # Give some headroom for labels
    ax.set_ylim(0, max(costs) * 1.15)

    _save(fig, "fig6_traffic_impact.png")


# ===================================================================
# Main
# ===================================================================
def main():
    print("=" * 60)
    print("Generating publication figures")
    print("=" * 60)

    fig1_solver_comparison()
    fig2_scaling_curve()
    fig3_gap_histogram()
    fig4_ablation()
    fig5_candidate_recall()
    fig6_traffic_impact()

    print("=" * 60)
    print("All figures generated successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
