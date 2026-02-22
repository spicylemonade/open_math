"""Performance comparison: naive vs NumPy vs HashLife engines."""

import json
import os
import random
import signal
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grid import Grid
from src.grid_numpy import NumPyGrid, NumPyLifeRule
from src.rules import LifeRule
from src.simulator import Simulator
from src.hashlife import HashLife
from src.patterns import parse_rle, GOSPER_GLIDER_GUN_RLE, R_PENTOMINO_RLE


class ComputeTimeout(Exception):
    pass


def _handler(signum, frame):
    raise ComputeTimeout()


def make_random_grids(width, height, seed=42, density=0.25):
    """Create matching random grids for naive and numpy engines."""
    rng = random.Random(seed)
    g = Grid(width, height, "wrap")
    ng = NumPyGrid(width, height, "wrap")
    for y in range(height):
        for x in range(width):
            val = 1 if rng.random() < density else 0
            g.set(x, y, val)
            ng.set(x, y, val)
    return g, ng


def benchmark_naive(grid, steps, timeout_sec=120):
    """Benchmark naive engine."""
    rule = LifeRule()
    sim = Simulator(grid.copy(), rule)
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout_sec)
    try:
        t0 = time.perf_counter()
        sim.run(steps)
        elapsed = time.perf_counter() - t0
        signal.alarm(0)
        return elapsed
    except ComputeTimeout:
        signal.alarm(0)
        return None


def benchmark_numpy(ngrid, steps, timeout_sec=120):
    """Benchmark NumPy engine."""
    rule = NumPyLifeRule()
    sim = Simulator(ngrid.copy(), rule)
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout_sec)
    try:
        t0 = time.perf_counter()
        sim.run(steps)
        elapsed = time.perf_counter() - t0
        signal.alarm(0)
        return elapsed
    except ComputeTimeout:
        signal.alarm(0)
        return None


def benchmark_hashlife_gun(log2_steps):
    """Benchmark HashLife on Gosper glider gun."""
    hl = HashLife()
    cells, size = parse_rle(GOSPER_GLIDER_GUN_RLE)[:2]
    # Pad to power of 2
    padded = [[0]*64 for _ in range(64)]
    for y in range(len(cells)):
        for x in range(len(cells[0])):
            padded[y][x] = cells[y][x]
    node = hl.from_cells(padded, 64, 64)

    t0 = time.perf_counter()
    result = hl.advance_pow2(node, log2_steps)
    elapsed = time.perf_counter() - t0
    return elapsed, result.population


def main():
    results = {"benchmarks": {}}

    # 1. Random soup benchmarks
    print("=== Random Soup Benchmarks (100 generations) ===")
    for size in [100, 500, 1000]:
        print(f"\nGrid {size}x{size}:")
        g, ng = make_random_grids(size, size)

        # Naive (skip 1000x1000 - too slow)
        if size <= 500:
            t_naive = benchmark_naive(g, 100, timeout_sec=180)
            print(f"  Naive: {t_naive:.3f}s" if t_naive else "  Naive: TIMEOUT")
        else:
            # For 1000x1000, just do 10 steps
            t_naive = benchmark_naive(g, 10, timeout_sec=120)
            if t_naive:
                t_naive = t_naive * 10  # extrapolate
                print(f"  Naive (extrapolated from 10 steps): {t_naive:.3f}s")
            else:
                t_naive = None
                print("  Naive: TIMEOUT")

        t_numpy = benchmark_numpy(ng, 100)
        print(f"  NumPy: {t_numpy:.3f}s" if t_numpy else "  NumPy: TIMEOUT")

        results["benchmarks"][f"soup_{size}x{size}"] = {
            "naive_time": t_naive,
            "numpy_time": t_numpy,
            "speedup": t_naive / t_numpy if (t_naive and t_numpy) else None,
        }

    # 2. Gosper glider gun benchmarks
    print("\n=== Gosper Glider Gun (HashLife) ===")
    for log2 in [10, 14, 17]:
        steps = 2 ** log2
        print(f"\n{steps} generations (2^{log2}):")
        t_hl, pop = benchmark_hashlife_gun(log2)
        print(f"  HashLife: {t_hl:.4f}s, population={pop}")
        results["benchmarks"][f"gun_{steps}_gen"] = {
            "hashlife_time": t_hl,
            "population": pop,
        }

    # Compare with numpy for gun at 1024 steps
    print("\nGlider gun 1024 gen - NumPy comparison:")
    cells, w, h = parse_rle(GOSPER_GLIDER_GUN_RLE)
    ng = NumPyGrid(64, 64, "fixed")
    for y in range(h):
        for x in range(w):
            if cells[y][x]:
                ng.set(x, y, 1)
    t_numpy_gun = benchmark_numpy(ng, 1024)
    print(f"  NumPy: {t_numpy_gun:.3f}s" if t_numpy_gun else "  NumPy: TIMEOUT")
    results["benchmarks"]["gun_1024_numpy"] = {"numpy_time": t_numpy_gun}

    # 3. R-pentomino stabilization
    print("\n=== R-pentomino Stabilization ===")
    cells, w, h = parse_rle(R_PENTOMINO_RLE)
    ng = NumPyGrid(200, 200, "wrap")
    for y in range(h):
        for x in range(w):
            if cells[y][x]:
                ng.set(x + 98, y + 98, 1)
    t_rpent = benchmark_numpy(ng, 1103)
    print(f"  NumPy (1103 steps): {t_rpent:.3f}s" if t_rpent else "  TIMEOUT")
    results["benchmarks"]["r_pentomino_1103"] = {"numpy_time": t_rpent}

    # Save
    os.makedirs("results", exist_ok=True)
    with open("results/performance_comparison.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to results/performance_comparison.json")


if __name__ == "__main__":
    main()
