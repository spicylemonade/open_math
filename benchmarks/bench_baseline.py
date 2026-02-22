"""Baseline performance benchmarks for the naive CA engine.

Measures time per generation and memory usage at various grid sizes.
"""

import json
import os
import random
import signal
import sys
import time
import tracemalloc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grid import Grid
from src.rules import LifeRule, Elementary1DRule
from src.simulator import Simulator


class ComputeTimeout(Exception):
    pass


def _handler(signum, frame):
    raise ComputeTimeout()


def make_random_grid(width, height, boundary="wrap", seed=42, density=0.25):
    """Create a random grid with given density."""
    rng = random.Random(seed)
    g = Grid(width, height, boundary)
    for y in range(height):
        for x in range(width):
            if rng.random() < density:
                g.set(x, y, 1)
    return g


def benchmark_life_step(width, height, n_runs=5, timeout_sec=120):
    """Benchmark time per generation for Game of Life."""
    rule = LifeRule()
    times = []
    for run in range(n_runs):
        grid = make_random_grid(width, height, seed=42 + run)
        signal.signal(signal.SIGALRM, _handler)
        signal.alarm(timeout_sec)
        try:
            start = time.perf_counter()
            rule.apply(grid)
            elapsed = time.perf_counter() - start
            signal.alarm(0)
            times.append(elapsed)
            print(f"  Run {run+1}/{n_runs}: {elapsed:.4f}s")
        except ComputeTimeout:
            print(f"  Run {run+1}/{n_runs}: TIMEOUT ({timeout_sec}s)")
            signal.alarm(0)
            break
    if not times:
        return {"mean": None, "std": None, "n_runs": 0}
    import statistics
    return {
        "mean": statistics.mean(times),
        "std": statistics.stdev(times) if len(times) > 1 else 0.0,
        "n_runs": len(times),
    }


def benchmark_memory(width, height):
    """Measure peak memory for creating and stepping a grid."""
    tracemalloc.start()
    rule = LifeRule()
    grid = make_random_grid(width, height, seed=42)
    rule.apply(grid)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"current_mb": current / 1e6, "peak_mb": peak / 1e6}


def benchmark_1d_rule(width, steps, n_runs=5, timeout_sec=120):
    """Benchmark Rule 110 on a 1D grid."""
    rule = Elementary1DRule(110)
    times = []
    for run in range(n_runs):
        grid = Grid(width, 1, boundary="wrap")
        grid.set(width // 2, 0, 1)
        sim = Simulator(grid, rule)
        signal.signal(signal.SIGALRM, _handler)
        signal.alarm(timeout_sec)
        try:
            start = time.perf_counter()
            sim.run(steps)
            elapsed = time.perf_counter() - start
            signal.alarm(0)
            times.append(elapsed)
            print(f"  Run {run+1}/{n_runs}: {elapsed:.4f}s")
        except ComputeTimeout:
            print(f"  Run {run+1}/{n_runs}: TIMEOUT ({timeout_sec}s)")
            signal.alarm(0)
            break
    if not times:
        return {"mean": None, "std": None, "n_runs": 0}
    import statistics
    return {
        "mean": statistics.mean(times),
        "std": statistics.stdev(times) if len(times) > 1 else 0.0,
        "n_runs": len(times),
    }


def main():
    results = {"engine": "naive_python", "benchmarks": {}}

    # Game of Life benchmarks
    grid_sizes = [(100, 100), (500, 500)]
    # Skip 1000x1000 for naive engine (too slow) - just measure one step
    print("=== Game of Life: time per generation step ===")
    for w, h in grid_sizes:
        print(f"\nGrid {w}x{h}:")
        result = benchmark_life_step(w, h, n_runs=5, timeout_sec=60)
        results["benchmarks"][f"life_{w}x{h}_step"] = result

    # 1000x1000: single run with timeout
    print(f"\nGrid 1000x1000:")
    result = benchmark_life_step(1000, 1000, n_runs=3, timeout_sec=120)
    results["benchmarks"]["life_1000x1000_step"] = result

    # Memory usage
    print("\n=== Memory usage ===")
    for w, h in [(100, 100), (500, 500), (1000, 1000)]:
        print(f"\nGrid {w}x{h}:")
        mem = benchmark_memory(w, h)
        print(f"  Peak: {mem['peak_mb']:.2f} MB")
        results["benchmarks"][f"memory_{w}x{h}"] = mem

    # Rule 110 1D benchmark
    print("\n=== Rule 110: 1000 steps on width 10000 ===")
    result = benchmark_1d_rule(10000, 1000, n_runs=5, timeout_sec=120)
    results["benchmarks"]["rule110_10000w_1000steps"] = result

    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/baseline_benchmarks.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to results/baseline_benchmarks.json")


if __name__ == "__main__":
    main()
