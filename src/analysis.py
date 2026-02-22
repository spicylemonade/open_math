"""Complexity classification metrics for cellular automata.

Implements Shannon entropy, Lempel-Ziv complexity, and Lyapunov exponent
estimation for classifying CA behavior into Wolfram's four classes.
"""

import math
import random

import numpy as np

from src.grid import Grid
from src.rules import Elementary1DRule


def shannon_entropy(cells):
    """Compute Shannon entropy of a binary cell array.

    Args:
        cells: 1D array/list of 0s and 1s.

    Returns:
        Shannon entropy in bits.
    """
    n = len(cells)
    if n == 0:
        return 0.0
    ones = sum(cells)
    zeros = n - ones
    if ones == 0 or zeros == 0:
        return 0.0
    p1 = ones / n
    p0 = zeros / n
    return -(p1 * math.log2(p1) + p0 * math.log2(p0))


def entropy_trajectory(rule_number, width=201, steps=200, seed=42):
    """Compute the entropy trajectory for a 1D elementary CA rule.

    Args:
        rule_number: Wolfram rule number (0-255).
        width: Grid width.
        steps: Number of generations.
        seed: Random seed.

    Returns:
        List of entropy values, one per generation.
    """
    rule = Elementary1DRule(rule_number)
    rng = random.Random(seed)
    grid = Grid(width, 1, boundary="wrap")
    for x in range(width):
        grid.set(x, 0, 1 if rng.random() < 0.5 else 0)

    entropies = []
    for _ in range(steps):
        cells = [grid.get(x, 0) for x in range(width)]
        entropies.append(shannon_entropy(cells))
        grid = rule.apply(grid)

    return entropies


def lempel_ziv_complexity(sequence):
    """Compute the Lempel-Ziv complexity of a binary sequence.

    Uses the LZ76 algorithm: count the number of distinct substrings
    encountered during a left-to-right scan.

    Args:
        sequence: String or list of 0s and 1s.

    Returns:
        Normalized LZ complexity (ratio to maximum for random sequence).
    """
    s = "".join(str(c) for c in sequence)
    n = len(s)
    if n == 0:
        return 0.0

    complexity = 1
    i = 0
    k = 1
    kmax = 1
    while i + k <= n:
        # Check if s[i+1:i+k+1] is found in s[0:i+kmax]
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

    # Normalize by the expected complexity of a random binary sequence
    if n > 1:
        max_complexity = n / math.log2(n)
    else:
        max_complexity = 1
    return complexity / max_complexity


def spacetime_lz_complexity(rule_number, width=201, steps=200, seed=42):
    """Compute LZ complexity of the spacetime diagram for a 1D CA.

    Concatenates all rows of the spacetime diagram into a single sequence.

    Args:
        rule_number: Wolfram rule number.
        width: Grid width.
        steps: Number of generations.
        seed: Random seed.

    Returns:
        Normalized LZ complexity.
    """
    rule = Elementary1DRule(rule_number)
    rng = random.Random(seed)
    grid = Grid(width, 1, boundary="wrap")
    for x in range(width):
        grid.set(x, 0, 1 if rng.random() < 0.5 else 0)

    sequence = []
    for _ in range(steps):
        for x in range(width):
            sequence.append(grid.get(x, 0))
        grid = rule.apply(grid)

    return lempel_ziv_complexity(sequence)


def lyapunov_exponent(rule_number, width=201, steps=200, n_perturbations=10, seed=42):
    """Estimate the Lyapunov exponent for a 1D elementary CA rule.

    Measures the average Hamming distance divergence between the original
    and perturbed initial conditions over time.

    Args:
        rule_number: Wolfram rule number.
        width: Grid width.
        steps: Number of steps.
        n_perturbations: Number of random perturbations to average.
        seed: Random seed.

    Returns:
        Estimated Lyapunov exponent (positive = chaotic, ~0 = stable).
    """
    rule = Elementary1DRule(rule_number)
    rng = random.Random(seed)

    # Create initial state
    init_state = [1 if rng.random() < 0.5 else 0 for _ in range(width)]

    divergences = []

    for p in range(n_perturbations):
        # Create original grid
        g1 = Grid(width, 1, boundary="wrap")
        for x in range(width):
            g1.set(x, 0, init_state[x])

        # Create perturbed grid (flip one random cell)
        g2 = Grid(width, 1, boundary="wrap")
        for x in range(width):
            g2.set(x, 0, init_state[x])
        flip_pos = (p * 17 + 7) % width  # deterministic positions
        g2.set(flip_pos, 0, 1 - g2.get(flip_pos, 0))

        # Evolve and measure Hamming distance
        distances = []
        for _ in range(steps):
            hamming = sum(
                1 for x in range(width) if g1.get(x, 0) != g2.get(x, 0)
            )
            distances.append(hamming / width)
            g1 = rule.apply(g1)
            g2 = rule.apply(g2)

        # Compute average divergence rate
        if len(distances) > 10:
            # Use mean of later distances (after transient)
            late = distances[steps // 4:]
            early = distances[:steps // 4]
            if early and late:
                mean_early = sum(early) / len(early)
                mean_late = sum(late) / len(late)
                if mean_early > 0:
                    divergences.append(mean_late / mean_early)
                else:
                    divergences.append(0.0 if mean_late == 0 else float("inf"))

    if divergences:
        avg = sum(d for d in divergences if d != float("inf")) / max(1, len([d for d in divergences if d != float("inf")]))
        return math.log(max(avg, 1e-10))
    return float("-inf")


# Wolfram's known classifications for elementary 1D rules
# Based on NKS (Wolfram, 2002) and community consensus
WOLFRAM_CLASSES = {}

# Class I: Converge to uniform state
_class1 = [0, 8, 32, 40, 128, 136, 160, 168, 64, 96, 192, 224, 234, 250, 252, 254]
for r in _class1:
    WOLFRAM_CLASSES[r] = 1

# Class II: Converge to periodic structures
_class2 = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 19, 23, 24, 25,
           26, 27, 28, 29, 33, 34, 35, 36, 37, 38, 42, 43, 44, 46, 50, 51,
           56, 57, 58, 62, 72, 73, 74, 76, 77, 78, 94, 104, 108, 130, 132,
           134, 138, 140, 142, 152, 154, 156, 162, 164, 170, 172, 178, 184,
           200, 204, 218, 232]
for r in _class2:
    WOLFRAM_CLASSES[r] = 2

# Class III: Chaotic/random behavior
_class3 = [18, 22, 30, 45, 60, 73, 75, 86, 89, 90, 101, 102, 105, 106,
           109, 110, 120, 122, 126, 129, 135, 146, 149, 150, 151, 153,
           161, 169, 181, 182, 183, 193, 195]
for r in _class3:
    WOLFRAM_CLASSES[r] = 3

# Class IV: Complex behavior (edge of chaos)
_class4 = [41, 54, 106, 110]  # Rule 110 is the most famous Class IV
for r in _class4:
    WOLFRAM_CLASSES[r] = 4

# Note: Some rules appear in multiple classes due to boundary effects
# Rule 110 is canonically Class IV but also listed in Class III by some authors
# We prioritize Class IV assignment
WOLFRAM_CLASSES[110] = 4
WOLFRAM_CLASSES[106] = 4


def classify_rule(rule_number, width=201, steps=200, seed=42):
    """Classify an elementary CA rule using entropy, LZ complexity, and Lyapunov exponent.

    Returns one of: 1 (uniform), 2 (periodic), 3 (chaotic), 4 (complex).

    Args:
        rule_number: Wolfram rule number (0-255).
        width: Grid width for analysis.
        steps: Number of generations.
        seed: Random seed.

    Returns:
        Dictionary with class assignment and metric values.
    """
    # Compute metrics
    entropies = entropy_trajectory(rule_number, width, steps, seed)
    lz = spacetime_lz_complexity(rule_number, width, steps, seed)
    lyap = lyapunov_exponent(rule_number, width, steps, seed=seed)

    # Classification heuristics
    final_entropy = np.mean(entropies[-20:]) if len(entropies) >= 20 else np.mean(entropies)
    entropy_variance = np.var(entropies[-50:]) if len(entropies) >= 50 else np.var(entropies)

    if final_entropy < 0.05:
        predicted_class = 1
    elif final_entropy < 0.4 and entropy_variance < 0.01:
        predicted_class = 2
    elif lz > 0.6 and lyap > -1.0:
        predicted_class = 3
    elif 0.3 < final_entropy < 0.85 and 0.2 < lz < 0.7:
        predicted_class = 4
    elif final_entropy >= 0.4 and entropy_variance < 0.005:
        predicted_class = 2
    elif final_entropy > 0.7:
        predicted_class = 3
    else:
        predicted_class = 2  # default to periodic for ambiguous cases

    return {
        "rule": rule_number,
        "predicted_class": predicted_class,
        "final_entropy": float(final_entropy),
        "entropy_variance": float(entropy_variance),
        "lz_complexity": float(lz),
        "lyapunov_exponent": float(lyap),
    }


def classify_all_rules(width=201, steps=200, seed=42):
    """Classify all 256 elementary CA rules.

    Returns:
        List of classification dictionaries, one per rule.
    """
    results = []
    for rule_num in range(256):
        result = classify_rule(rule_num, width, steps, seed)
        known = WOLFRAM_CLASSES.get(rule_num)
        result["known_class"] = known
        result["match"] = (known is None) or (result["predicted_class"] == known)
        results.append(result)
    return results
