"""Generate all publication-quality figures from saved experiment results.

Produces 6+ figures as both PNG (300 DPI) and PDF:
1. Performance comparison bar chart
2. HashLife speedup log-scale plot
3. Wolfram 1D classification heatmap
4. 2D rule classification scatter plot
5. Sensitivity analysis population dynamics
6. Memory scaling plot
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# Consistent styling
def setup_style():
    """Apply consistent publication-quality styling."""
    if HAS_SEABORN:
        sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    mpl.rcParams.update({
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

def get_palette():
    """Get consistent color palette."""
    if HAS_SEABORN:
        return sns.color_palette("deep")
    return ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
            "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]


def save_fig(fig, name):
    """Save figure as PNG and PDF."""
    fig.savefig(f"figures/{name}.png", dpi=300)
    fig.savefig(f"figures/{name}.pdf")
    plt.close(fig)
    print(f"  Saved figures/{name}.png and .pdf")


def fig1_performance_comparison(data):
    """Figure 1: Performance comparison bar chart."""
    palette = get_palette()
    fig, ax = plt.subplots(figsize=(10, 6))

    sizes = ["100x100", "500x500", "1000x1000"]
    naive_times = [
        data["benchmarks"]["soup_100x100"]["naive_time"],
        data["benchmarks"]["soup_500x500"]["naive_time"],
        data["benchmarks"]["soup_1000x1000"]["naive_time"],
    ]
    numpy_times = [
        data["benchmarks"]["soup_100x100"]["numpy_time"],
        data["benchmarks"]["soup_500x500"]["numpy_time"],
        data["benchmarks"]["soup_1000x1000"]["numpy_time"],
    ]

    x = np.arange(len(sizes))
    width = 0.35

    bars1 = ax.bar(x - width/2, naive_times, width, label="Naive Python",
                   color=palette[0], edgecolor="white", linewidth=0.5)
    bars2 = ax.bar(x + width/2, numpy_times, width, label="NumPy Vectorized",
                   color=palette[1], edgecolor="white", linewidth=0.5)

    # Add speedup annotations
    for i in range(len(sizes)):
        speedup = naive_times[i] / numpy_times[i]
        ax.annotate(f"{speedup:.0f}x",
                    xy=(x[i] + width/2, numpy_times[i]),
                    xytext=(0, 5), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold", color=palette[1])

    ax.set_xlabel("Grid Size")
    ax.set_ylabel("Time for 100 Generations (s)")
    ax.set_title("Performance: Naive Python vs NumPy Vectorized")
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_yscale("log")
    ax.legend(frameon=True)
    ax.grid(axis="y", alpha=0.3)

    save_fig(fig, "fig1_performance_comparison")


def fig2_hashlife_speedup(data):
    """Figure 2: HashLife speedup log-scale plot."""
    palette = get_palette()
    fig, ax = plt.subplots(figsize=(10, 6))

    # HashLife data points
    hl_gens = [1024, 16384, 131072]
    hl_times = [
        data["benchmarks"]["gun_1024_gen"]["hashlife_time"],
        data["benchmarks"]["gun_16384_gen"]["hashlife_time"],
        data["benchmarks"]["gun_131072_gen"]["hashlife_time"],
    ]

    # NumPy reference for 1024 gens
    numpy_1024 = data["benchmarks"]["gun_1024_numpy"]["numpy_time"]
    # Extrapolate NumPy for higher gen counts (linear scaling)
    numpy_times = [numpy_1024 * g / 1024 for g in hl_gens]

    ax.plot(hl_gens, numpy_times, "s--", color=palette[1], label="NumPy (extrapolated)",
            linewidth=2, markersize=8)
    ax.plot(hl_gens, hl_times, "D-", color=palette[2], label="HashLife",
            linewidth=2, markersize=8)

    # Shade the speedup region
    ax.fill_between(hl_gens, hl_times, numpy_times, alpha=0.15, color=palette[2])

    # Annotate speedup at each point
    for i, g in enumerate(hl_gens):
        speedup = numpy_times[i] / hl_times[i]
        mid_y = np.sqrt(numpy_times[i] * hl_times[i])
        ax.annotate(f"{speedup:.0f}x", xy=(g, mid_y),
                    fontsize=10, fontweight="bold", color=palette[2],
                    ha="center")

    ax.set_xlabel("Generations Simulated")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("HashLife vs NumPy: Gosper Glider Gun")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(frameon=True)

    save_fig(fig, "fig2_hashlife_speedup")


def fig3_wolfram_heatmap(data):
    """Figure 3: Wolfram 1D classification heatmap (16x16 grid of rules 0-255)."""
    palette = get_palette()
    fig, ax = plt.subplots(figsize=(10, 8))

    # Build 16x16 grid of predicted classes
    grid = np.zeros((16, 16), dtype=int)
    for result in data["results"]:
        rule = result["rule"]
        row = rule // 16
        col = rule % 16
        grid[row, col] = result["predicted_class"]

    # Custom colormap: Class I=blue, II=green, III=red, IV=gold
    from matplotlib.colors import ListedColormap, BoundaryNorm
    colors = ["#FFFFFF", "#4C72B0", "#55A868", "#C44E52", "#CCB974"]
    cmap = ListedColormap(colors)
    bounds = [0, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = BoundaryNorm(bounds, cmap.N)

    im = ax.imshow(grid, cmap=cmap, norm=norm, aspect="equal")

    # Add rule numbers in each cell
    for i in range(16):
        for j in range(16):
            rule_num = i * 16 + j
            cls = grid[i, j]
            text_color = "white" if cls in (1, 3) else "black"
            ax.text(j, i, str(rule_num), ha="center", va="center",
                    fontsize=5.5, color=text_color)

    ax.set_xlabel("Rule Number mod 16")
    ax.set_ylabel("Rule Number div 16")
    ax.set_title("Wolfram Classification of 256 Elementary CA Rules")
    ax.set_xticks(range(16))
    ax.set_yticks(range(16))

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors[1], label="Class I (Uniform)"),
        Patch(facecolor=colors[2], label="Class II (Periodic)"),
        Patch(facecolor=colors[3], label="Class III (Chaotic)"),
        Patch(facecolor=colors[4], label="Class IV (Complex)"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(1.02, 1),
              frameon=True)

    fig.tight_layout()
    save_fig(fig, "fig3_wolfram_heatmap")


def fig4_2d_classification_scatter(data):
    """Figure 4: 2D rule classification scatter plot (entropy vs LZ complexity)."""
    palette = get_palette()
    fig, ax = plt.subplots(figsize=(10, 7))

    class_colors = {1: "#4C72B0", 2: "#55A868", 3: "#C44E52", 4: "#CCB974"}
    class_markers = {1: "o", 2: "s", 3: "^", 4: "D"}
    class_names = {1: "Class I", 2: "Class II", 3: "Class III", 4: "Class IV"}

    for result in data["results"]:
        if result.get("predicted_class") is None:
            continue
        cls = result["predicted_class"]
        ax.scatter(result["final_entropy"], result["lz_complexity"],
                   c=class_colors[cls], marker=class_markers[cls],
                   s=80, alpha=0.7, edgecolors="black", linewidth=0.5,
                   label=class_names[cls] if cls not in [r.get("predicted_class")
                   for r in data["results"][:data["results"].index(result)]]
                   else "")

    # Clean up legend duplicates
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), frameon=True)

    # Annotate notable rules
    for result in data["results"]:
        if result.get("rulestring") == "B3/S23":
            ax.annotate("Life (B3/S23)", xy=(result["final_entropy"], result["lz_complexity"]),
                        xytext=(10, 10), textcoords="offset points", fontsize=9,
                        arrowprops=dict(arrowstyle="->", color="black", lw=0.8))
            break

    ax.set_xlabel("Final Shannon Entropy")
    ax.set_ylabel("Lempel-Ziv Complexity")
    ax.set_title("2D Outer-Totalistic Rule Classification")

    save_fig(fig, "fig4_2d_classification")


def fig5_sensitivity_dynamics(data):
    """Figure 5: Sensitivity analysis population dynamics."""
    palette = get_palette()
    markers = ["o", "s", "^", "D", "v"]
    fig, ax = plt.subplots(figsize=(10, 6))

    grid_exps = [e for e in data["experiments"] if e["type"] == "grid_size"]

    for i, exp in enumerate(grid_exps):
        size = exp["size"]
        pops_normalized = [p / (size * size) for p in exp["populations"]]
        step_indices = list(range(len(pops_normalized)))
        stride = max(1, len(step_indices) // 100)
        ax.plot(step_indices[::stride], pops_normalized[::stride],
                color=palette[i % len(palette)], label=f"{size}\u00d7{size}",
                linewidth=1.5, marker=markers[i % len(markers)], markersize=3,
                markevery=10, alpha=0.8)

    ax.set_xlabel("Generation")
    ax.set_ylabel("Population Density (cells / area)")
    ax.set_title("Population Dynamics vs Grid Size (Toroidal Boundary)")
    ax.legend(frameon=True, title="Grid Size")

    save_fig(fig, "fig5_sensitivity_dynamics")


def fig6_memory_scaling(data):
    """Figure 6: Memory scaling plot."""
    palette = get_palette()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)

    # Left: Memory vs grid size for naive and numpy
    naive_data = [(p["size"], p["peak_mb"]) for p in data["profiles"]
                  if p["engine"] == "naive" and p.get("peak_mb") is not None]
    numpy_data = [(p["size"], p["peak_mb"]) for p in data["profiles"]
                  if p["engine"] == "numpy"]

    if naive_data:
        sizes_n, mems_n = zip(*naive_data)
        ax1.plot(sizes_n, mems_n, "o-", color=palette[0], label="Naive Python",
                 linewidth=2, markersize=8)
    sizes_np, mems_np = zip(*numpy_data)
    ax1.plot(sizes_np, mems_np, "s-", color=palette[1], label="NumPy",
             linewidth=2, markersize=8)

    # Reference: quadratic scaling
    ref_sizes = np.array([100, 500, 1000, 2000, 5000])
    ref_mem = (ref_sizes / 100) ** 2 * mems_np[0]
    ax1.plot(ref_sizes, ref_mem, ":", color="gray", alpha=0.5, label="O(n\u00b2) reference")

    ax1.set_xlabel("Grid Side Length")
    ax1.set_ylabel("Peak Memory (MB)")
    ax1.set_title("Memory Scaling by Grid Size")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.legend(frameon=True)

    # Right: HashLife memory vs generations
    hl_data = [(p["steps"], p["peak_mb"]) for p in data["profiles"]
               if p["engine"] == "hashlife"]
    steps_hl, mems_hl = zip(*hl_data)
    ax2.plot(steps_hl, mems_hl, "D-", color=palette[2], label="HashLife (Glider Gun)",
             linewidth=2, markersize=8)

    ref_steps = np.array(steps_hl)
    ref_linear = ref_steps / ref_steps[0] * mems_hl[0]
    ax2.plot(ref_steps, ref_linear, ":", color="gray", alpha=0.5, label="O(n) reference")

    ax2.set_xlabel("Generations Simulated")
    ax2.set_ylabel("Peak Memory (MB)")
    ax2.set_title("HashLife Memory vs Generations")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.legend(frameon=True)

    save_fig(fig, "fig6_memory_scaling")


def fig7_boundary_comparison(data):
    """Bonus Figure 7: Boundary condition comparison."""
    palette = get_palette()
    boundary_exps = [e for e in data["experiments"] if e["type"] == "boundary"]

    sizes_done = []
    for exp in boundary_exps:
        if exp["size"] not in sizes_done:
            sizes_done.append(exp["size"])

    fig, axes = plt.subplots(1, min(3, len(sizes_done)), figsize=(15, 5),
                             constrained_layout=True, sharey=True)
    if len(sizes_done) == 1:
        axes = [axes]

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
        ax.set_title(f"{size}\u00d7{size} Grid")
        ax.legend(frameon=True)

    fig.suptitle("Boundary Condition Effect on Population Dynamics", fontweight="bold")
    save_fig(fig, "fig7_boundary_comparison")


def main():
    setup_style()
    os.makedirs("figures", exist_ok=True)

    # Load all result files
    print("Loading result data...")
    with open("results/performance_comparison.json") as f:
        perf_data = json.load(f)
    with open("results/wolfram_classification.json") as f:
        wolfram_data = json.load(f)
    with open("results/2d_classification.json") as f:
        class2d_data = json.load(f)
    with open("results/sensitivity_data.json") as f:
        sens_data = json.load(f)
    with open("results/memory_profile.json") as f:
        mem_data = json.load(f)

    print("\nGenerating figures...")

    print("\n[1/7] Performance comparison bar chart")
    fig1_performance_comparison(perf_data)

    print("[2/7] HashLife speedup log-scale plot")
    fig2_hashlife_speedup(perf_data)

    print("[3/7] Wolfram 1D classification heatmap")
    fig3_wolfram_heatmap(wolfram_data)

    print("[4/7] 2D rule classification scatter plot")
    fig4_2d_classification_scatter(class2d_data)

    print("[5/7] Sensitivity analysis population dynamics")
    fig5_sensitivity_dynamics(sens_data)

    print("[6/7] Memory scaling plot")
    fig6_memory_scaling(mem_data)

    print("[7/7] Boundary condition comparison")
    fig7_boundary_comparison(sens_data)

    print("\nAll figures generated successfully!")


if __name__ == "__main__":
    main()
