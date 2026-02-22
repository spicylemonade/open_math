"""Classify 2D outer-totalistic rules using complexity metrics.

Samples random birth/survival conditions and classifies each rule
using entropy, LZ complexity, and Lyapunov exponent.
"""

import json
import math
import os
import random
import signal
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grid_numpy import NumPyGrid, NumPyTotalisticRule
from src.simulator import Simulator


class ComputeTimeout(Exception):
    pass


def _handler(signum, frame):
    raise ComputeTimeout()


def shannon_entropy_2d(grid):
    """Compute Shannon entropy of a 2D grid."""
    total = grid.width * grid.height
    ones = grid.population()
    zeros = total - ones
    if ones == 0 or zeros == 0:
        return 0.0
    p1 = ones / total
    p0 = zeros / total
    return -(p1 * math.log2(p1) + p0 * math.log2(p0))


def lz_complexity_2d(grid):
    """Compute LZ complexity of the flattened grid."""
    seq = grid.cells.flatten().tolist()
    s = "".join(str(int(c)) for c in seq)
    n = len(s)
    if n == 0:
        return 0.0

    complexity = 1
    i = 0
    k = 1
    kmax = 1
    while i + k <= n:
        substr = s[i + 1:i + k + 1]
        if substr in s[0:i + kmax]:
            k += 1
            if i + k > n:
                complexity += 1
                break
        else:
            complexity += 1
            i += kmax if kmax > k else k
            k = 1
            kmax = 1
            continue
        kmax = max(kmax, k)

    if n > 1:
        max_complexity = n / math.log2(n)
    else:
        max_complexity = 1
    return complexity / max_complexity


def lyapunov_2d(rule, width=50, height=50, steps=50, seed=42):
    """Estimate Lyapunov exponent for a 2D rule."""
    rng = random.Random(seed)
    g1 = NumPyGrid(width, height, "wrap")
    g2 = NumPyGrid(width, height, "wrap")
    for y in range(height):
        for x in range(width):
            val = 1 if rng.random() < 0.25 else 0
            g1.set(x, y, val)
            g2.set(x, y, val)

    # Perturb one cell
    g2.set(width // 2, height // 2, 1 - g2.get(width // 2, height // 2))

    total_cells = width * height
    early_dists = []
    late_dists = []

    for step in range(steps):
        hamming = int(np.sum(g1.cells != g2.cells))
        dist = hamming / total_cells
        if step < steps // 4:
            early_dists.append(dist)
        else:
            late_dists.append(dist)
        g1 = rule.apply(g1)
        g2 = rule.apply(g2)

    mean_early = np.mean(early_dists) if early_dists else 0
    mean_late = np.mean(late_dists) if late_dists else 0

    if mean_early > 0:
        return math.log(max(mean_late / mean_early, 1e-10))
    return -10.0 if mean_late == 0 else 10.0


def classify_2d_rule(birth, survival, width=50, height=50, steps=100, seed=42):
    """Classify a single 2D outer-totalistic rule."""
    rule = NumPyTotalisticRule(birth, survival)
    rng = random.Random(seed)

    # Create random soup
    grid = NumPyGrid(width, height, "wrap")
    for y in range(height):
        for x in range(width):
            grid.set(x, y, 1 if rng.random() < 0.25 else 0)

    # Collect entropy trajectory
    entropies = []
    sim = Simulator(grid, rule)
    for _ in range(steps):
        entropies.append(shannon_entropy_2d(sim.grid))
        sim.step()
    entropies.append(shannon_entropy_2d(sim.grid))

    # LZ complexity of final state
    lz = lz_complexity_2d(sim.grid)

    # Lyapunov exponent
    lyap = lyapunov_2d(rule, width, height, min(steps, 50), seed)

    # Classification
    final_entropy = np.mean(entropies[-20:]) if len(entropies) >= 20 else np.mean(entropies)
    entropy_var = np.var(entropies[-30:]) if len(entropies) >= 30 else np.var(entropies)

    if final_entropy < 0.05:
        predicted_class = 1
    elif final_entropy < 0.3 and entropy_var < 0.005:
        predicted_class = 2
    elif lz > 0.5 and lyap > -0.5:
        predicted_class = 3
    elif 0.2 < final_entropy < 0.8 and 0.15 < lz < 0.6 and -2 < lyap < 1:
        predicted_class = 4
    elif final_entropy > 0.6:
        predicted_class = 3
    else:
        predicted_class = 2

    return {
        "birth": sorted(list(birth)),
        "survival": sorted(list(survival)),
        "rulestring": f"B{''.join(str(b) for b in sorted(birth))}/S{''.join(str(s) for s in sorted(survival))}",
        "predicted_class": predicted_class,
        "final_entropy": float(final_entropy),
        "entropy_variance": float(entropy_var),
        "lz_complexity": float(lz),
        "lyapunov_exponent": float(lyap),
        "entropy_trajectory": [float(e) for e in entropies],
    }


def main():
    signal.signal(signal.SIGALRM, _handler)
    rng = random.Random(42)

    # Generate 50 random rules plus some known interesting ones
    rules_to_test = []

    # Known interesting rules
    known_rules = [
        ({3}, {2, 3}),        # Life (B3/S23)
        ({3, 6}, {2, 3}),     # HighLife
        ({3, 6, 7, 8}, {3, 4, 6, 7, 8}),  # Day & Night
        ({2}, set()),         # Seeds
        ({1}, {1}),           # Gnarl
        ({3}, {1, 2, 3, 4, 5, 6, 7, 8}),  # Life without Death
    ]
    for b, s in known_rules:
        rules_to_test.append((b, s))

    # Random rules
    while len(rules_to_test) < 56:
        birth = set()
        survival = set()
        for i in range(9):
            if rng.random() < 0.3:
                birth.add(i)
            if rng.random() < 0.3:
                survival.add(i)
        if not birth and not survival:
            continue
        rules_to_test.append((birth, survival))

    results = []
    class_counts = {1: 0, 2: 0, 3: 0, 4: 0}

    print(f"Classifying {len(rules_to_test)} 2D outer-totalistic rules...")
    for i, (birth, survival) in enumerate(rules_to_test):
        rulestring = f"B{''.join(str(b) for b in sorted(birth))}/S{''.join(str(s) for s in sorted(survival))}"
        signal.alarm(60)  # 60s per rule
        try:
            result = classify_2d_rule(birth, survival)
            results.append(result)
            class_counts[result["predicted_class"]] += 1
            print(f"  [{i+1}/{len(rules_to_test)}] {rulestring} -> Class {result['predicted_class']} "
                  f"(H={result['final_entropy']:.3f}, LZ={result['lz_complexity']:.3f}, "
                  f"λ={result['lyapunov_exponent']:.3f})")
            signal.alarm(0)
        except ComputeTimeout:
            signal.alarm(0)
            print(f"  [{i+1}/{len(rules_to_test)}] {rulestring} -> TIMEOUT")
            results.append({
                "rulestring": rulestring,
                "birth": sorted(list(birth)),
                "survival": sorted(list(survival)),
                "predicted_class": None,
                "error": "timeout",
            })

    # Identify Class IV rules
    class4_rules = [r for r in results if r.get("predicted_class") == 4]
    print(f"\n=== Summary ===")
    print(f"Class distribution: {class_counts}")
    print(f"Class IV rules found: {len(class4_rules)}")
    for r in class4_rules:
        print(f"  {r['rulestring']}: H={r['final_entropy']:.3f}, LZ={r['lz_complexity']:.3f}")

    # Save results
    os.makedirs("results", exist_ok=True)
    output = {
        "total_rules": len(rules_to_test),
        "class_distribution": class_counts,
        "class4_rules": [r["rulestring"] for r in class4_rules],
        "results": results,
    }
    with open("results/2d_classification.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to results/2d_classification.json")


if __name__ == "__main__":
    main()
