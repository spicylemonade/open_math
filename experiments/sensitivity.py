"""Sensitivity analysis: grid size and boundary condition effects on Game of Life.

Tests population dynamics across different grid sizes and boundary conditions.
"""

import json
import os
import random
import signal
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grid_numpy import NumPyGrid, NumPyLifeRule
from src.simulator import Simulator


class ComputeTimeout(Exception):
    pass


def _handler(signum, frame):
    raise ComputeTimeout()


def run_sensitivity(size, boundary, seed=42, density=0.25, steps=500, timeout_sec=120):
    """Run a sensitivity experiment for a given grid size and boundary."""
    rng = random.Random(seed)
    grid = NumPyGrid(size, size, boundary)
    for y in range(size):
        for x in range(size):
            grid.set(x, y, 1 if rng.random() < density else 0)

    rule = NumPyLifeRule()
    sim = Simulator(grid, rule)
    populations = [sim.grid.population()]

    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout_sec)
    try:
        for _ in range(steps):
            sim.step()
            populations.append(sim.grid.population())
        signal.alarm(0)
    except ComputeTimeout:
        signal.alarm(0)
        print(f"    TIMEOUT at step {len(populations)-1}")

    return populations


def main():
    results = {"experiments": []}
    seed = 42

    # 1. Grid size sensitivity (toroidal boundary)
    print("=== Grid Size Sensitivity (wrap boundary) ===")
    sizes = [50, 100, 200, 500, 1000]
    for size in sizes:
        print(f"\n  Grid {size}x{size}:")
        t0 = time.perf_counter()
        pops = run_sensitivity(size, "wrap", seed=seed, steps=500, timeout_sec=180)
        elapsed = time.perf_counter() - t0
        print(f"    {len(pops)-1} steps in {elapsed:.2f}s, "
              f"final pop={pops[-1]}, density={pops[-1]/(size*size):.4f}")
        results["experiments"].append({
            "type": "grid_size",
            "size": size,
            "boundary": "wrap",
            "seed": seed,
            "steps": len(pops) - 1,
            "populations": pops,
            "time_seconds": elapsed,
        })

    # 2. Boundary condition comparison
    print("\n=== Boundary Condition Comparison ===")
    for size in [100, 200, 500]:
        for boundary in ["wrap", "fixed"]:
            print(f"\n  Grid {size}x{size} ({boundary}):")
            t0 = time.perf_counter()
            pops = run_sensitivity(size, boundary, seed=seed, steps=500, timeout_sec=180)
            elapsed = time.perf_counter() - t0
            print(f"    {len(pops)-1} steps in {elapsed:.2f}s, final pop={pops[-1]}")
            results["experiments"].append({
                "type": "boundary",
                "size": size,
                "boundary": boundary,
                "seed": seed,
                "steps": len(pops) - 1,
                "populations": pops,
                "time_seconds": elapsed,
            })

    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/sensitivity_data.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to results/sensitivity_data.json")

    # Generate figures
    generate_figures(results)


def generate_figures(results):
    """Generate sensitivity analysis figures."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import seaborn as sns

    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    mpl.rcParams.update({
        "figure.figsize": (8, 5),
        "figure.dpi": 300,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "axes.labelsize": 13,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 11,
        "legend.framealpha": 0.9,
        "legend.edgecolor": "0.8",
        "font.family": "serif",
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
    })

    palette = sns.color_palette("colorblind")
    markers = ["o", "s", "^", "D", "v"]
    os.makedirs("figures", exist_ok=True)

    # Figure 1: Population dynamics for different grid sizes
    fig, ax = plt.subplots(figsize=(10, 6))
    grid_exps = [e for e in results["experiments"]
                 if e["type"] == "grid_size"]

    for i, exp in enumerate(grid_exps):
        size = exp["size"]
        # Normalize population by grid area for comparison
        pops_normalized = [p / (size * size) for p in exp["populations"]]
        step_indices = list(range(len(pops_normalized)))
        # Subsample for readability
        stride = max(1, len(step_indices) // 100)
        ax.plot(step_indices[::stride], pops_normalized[::stride],
                color=palette[i], label=f"{size}×{size}",
                linewidth=1.5, marker=markers[i], markersize=3,
                markevery=10, alpha=0.8)

    ax.set_xlabel("Generation")
    ax.set_ylabel("Population Density (cells / area)")
    ax.set_title("Population Dynamics vs Grid Size (Toroidal Boundary)")
    ax.legend(frameon=True, title="Grid Size")
    plt.savefig("figures/sensitivity_grid_size.png", dpi=300)
    plt.savefig("figures/sensitivity_grid_size.pdf")
    plt.close()
    print("Saved figures/sensitivity_grid_size.png")

    # Figure 2: Boundary condition comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True,
                             sharey=True)
    boundary_exps = [e for e in results["experiments"]
                     if e["type"] == "boundary"]

    sizes_done = []
    for exp in boundary_exps:
        size = exp["size"]
        if size not in sizes_done:
            sizes_done.append(size)

    for idx, size in enumerate(sizes_done[:3]):
        ax = axes[idx]
        for boundary, color, ls in [("wrap", palette[0], "-"), ("fixed", palette[1], "--")]:
            exp = next((e for e in boundary_exps
                       if e["size"] == size and e["boundary"] == boundary), None)
            if exp:
                pops = exp["populations"]
                stride = max(1, len(pops) // 200)
                gens = list(range(len(pops)))
                ax.plot(gens[::stride], [p/(size*size) for p in pops[::stride]],
                       color=color, linestyle=ls, label=boundary.title(),
                       linewidth=1.5, alpha=0.8)
        ax.set_xlabel("Generation")
        if idx == 0:
            ax.set_ylabel("Population Density")
        ax.set_title(f"{size}×{size} Grid")
        ax.legend(frameon=True)

    fig.suptitle("Boundary Condition Effect on Population Dynamics", fontweight="bold")
    plt.savefig("figures/sensitivity_boundary.png", dpi=300)
    plt.savefig("figures/sensitivity_boundary.pdf")
    plt.close()
    print("Saved figures/sensitivity_boundary.png")


if __name__ == "__main__":
    main()
