"""Memory profiling and scalability analysis for all CA engines."""

import json
import os
import random
import signal
import sys
import tracemalloc
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grid import Grid
from src.grid_numpy import NumPyGrid, NumPyLifeRule
from src.rules import LifeRule
from src.simulator import Simulator
from src.hashlife import HashLife
from src.patterns import parse_rle, GOSPER_GLIDER_GUN_RLE


class ComputeTimeout(Exception):
    pass


def _handler(signum, frame):
    raise ComputeTimeout()


def profile_naive(size, steps=10, timeout_sec=120):
    """Profile naive engine memory."""
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout_sec)
    try:
        tracemalloc.start()
        rng = random.Random(42)
        grid = Grid(size, size, "wrap")
        for y in range(size):
            for x in range(size):
                grid.set(x, y, 1 if rng.random() < 0.25 else 0)
        rule = LifeRule()
        for _ in range(steps):
            grid = rule.apply(grid)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        signal.alarm(0)
        return peak / 1e6
    except ComputeTimeout:
        tracemalloc.stop()
        signal.alarm(0)
        return None


def profile_numpy(size, steps=10):
    """Profile NumPy engine memory."""
    tracemalloc.start()
    rng = random.Random(42)
    grid = NumPyGrid(size, size, "wrap")
    for y in range(size):
        for x in range(size):
            grid.set(x, y, 1 if rng.random() < 0.25 else 0)
    rule = NumPyLifeRule()
    for _ in range(steps):
        grid = rule.apply(grid)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1e6


def profile_hashlife_gun(steps_log2):
    """Profile HashLife memory on Gosper glider gun."""
    tracemalloc.start()
    hl = HashLife()
    cells, w, h = parse_rle(GOSPER_GLIDER_GUN_RLE)
    padded = [[0]*64 for _ in range(64)]
    for y in range(h):
        for x in range(w):
            padded[y][x] = cells[y][x]
    node = hl.from_cells(padded, 64, 64)
    result = hl.advance_pow2(node, steps_log2)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1e6, result.population


def main():
    results = {"profiles": []}

    sizes = [100, 500, 1000, 2000]

    # Naive engine
    print("=== Naive Engine Memory ===")
    for size in sizes:
        if size > 1000:
            print(f"  {size}x{size}: skipped (too slow)")
            results["profiles"].append({
                "engine": "naive", "size": size, "peak_mb": None, "note": "skipped"})
            continue
        mem = profile_naive(size, steps=5, timeout_sec=60)
        if mem:
            print(f"  {size}x{size}: {mem:.2f} MB")
        else:
            print(f"  {size}x{size}: TIMEOUT")
        results["profiles"].append({"engine": "naive", "size": size, "peak_mb": mem})

    # NumPy engine
    print("\n=== NumPy Engine Memory ===")
    for size in sizes + [5000]:
        mem = profile_numpy(size, steps=10)
        print(f"  {size}x{size}: {mem:.2f} MB")
        results["profiles"].append({"engine": "numpy", "size": size, "peak_mb": mem})

    # HashLife on repetitive patterns (glider gun)
    print("\n=== HashLife Memory (Glider Gun) ===")
    for log2 in [8, 10, 12, 14, 16]:
        steps = 2 ** log2
        mem, pop = profile_hashlife_gun(log2)
        print(f"  2^{log2} = {steps} gen: {mem:.2f} MB (pop={pop})")
        results["profiles"].append({
            "engine": "hashlife", "steps_log2": log2, "steps": steps,
            "peak_mb": mem, "population": pop,
        })

    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/memory_profile.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to results/memory_profile.json")

    # Generate figure
    generate_figure(results)


def generate_figure(results):
    """Generate memory scaling plot."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import seaborn as sns
    import numpy as np

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

    palette = sns.color_palette("deep")
    os.makedirs("figures", exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)

    # Left: Memory vs grid size for naive and numpy
    naive_data = [(p["size"], p["peak_mb"]) for p in results["profiles"]
                  if p["engine"] == "naive" and p["peak_mb"] is not None]
    numpy_data = [(p["size"], p["peak_mb"]) for p in results["profiles"]
                  if p["engine"] == "numpy"]

    if naive_data:
        sizes_n, mems_n = zip(*naive_data)
        ax1.plot(sizes_n, mems_n, "o-", color=palette[0], label="Naive Python",
                linewidth=2, markersize=8)
    sizes_np, mems_np = zip(*numpy_data)
    ax1.plot(sizes_np, mems_np, "s-", color=palette[1], label="NumPy",
            linewidth=2, markersize=8)

    # Reference: quadratic scaling line
    ref_sizes = np.array([100, 500, 1000, 2000, 5000])
    ref_mem = (ref_sizes / 100) ** 2 * mems_np[0]
    ax1.plot(ref_sizes, ref_mem, ":", color="gray", alpha=0.5, label="O(n²) reference")

    ax1.set_xlabel("Grid Side Length")
    ax1.set_ylabel("Peak Memory (MB)")
    ax1.set_title("Memory Scaling by Grid Size")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.legend(frameon=True)

    # Right: HashLife memory vs generations
    hl_data = [(p["steps"], p["peak_mb"]) for p in results["profiles"]
               if p["engine"] == "hashlife"]
    steps_hl, mems_hl = zip(*hl_data)
    ax2.plot(steps_hl, mems_hl, "D-", color=palette[2], label="HashLife (Glider Gun)",
            linewidth=2, markersize=8)

    # Reference: linear and quadratic lines
    ref_steps = np.array(steps_hl)
    ref_linear = ref_steps / ref_steps[0] * mems_hl[0]
    ax2.plot(ref_steps, ref_linear, ":", color="gray", alpha=0.5, label="O(n) reference")

    ax2.set_xlabel("Generations Simulated")
    ax2.set_ylabel("Peak Memory (MB)")
    ax2.set_title("HashLife Memory vs Generations")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.legend(frameon=True)

    plt.savefig("figures/memory_scaling.png", dpi=300)
    plt.savefig("figures/memory_scaling.pdf")
    plt.close()
    print("Saved figures/memory_scaling.png")


if __name__ == "__main__":
    main()
