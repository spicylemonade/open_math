"""
Early termination detection for Lychrel candidates.

Uses statistical cutoffs to abandon candidates unlikely to reach palindrome
within useful iteration counts. Based on Doucette's regression formula.
"""

import math


def compute_cutoff(num_digits, sigma_multiplier=3.0):
    """
    Compute iteration depth cutoff based on Doucette's formula.

    Expected Max Delay = 14.255934 * digits - 17.320261
    sigma = 11.087996

    Cutoff at mean + sigma_multiplier * sigma.
    """
    expected = 14.255934 * num_digits - 17.320261
    sigma = 11.087996
    cutoff = expected + sigma_multiplier * sigma
    return int(math.ceil(cutoff))


def adaptive_cutoff(num_digits):
    """
    Use 3-sigma above expected max as the iteration cutoff.
    Any number not reaching palindrome by this point is almost
    certainly a Lychrel candidate.
    """
    return compute_cutoff(num_digits, sigma_multiplier=3.0)


# Precomputed cutoffs for common digit lengths
CUTOFFS = {d: adaptive_cutoff(d) for d in range(5, 40)}


def should_terminate(num_digits, current_iteration):
    """Return True if we should give up on this candidate."""
    cutoff = CUTOFFS.get(num_digits, adaptive_cutoff(num_digits))
    return current_iteration >= cutoff


def estimate_savings(num_digits, sample_delays):
    """
    Estimate computation savings from early termination.

    Given a sample of actual delays, compute how much time we save
    by not running Lychrel candidates to the full max_iter.
    """
    cutoff = adaptive_cutoff(num_digits)

    # Without early termination: all Lychrel candidates run to max_iter
    # With: they run to cutoff
    # Savings = (max_iter - cutoff) * fraction_lychrel
    total_iters_without = sum(
        d if d > 0 else 10000 for d in sample_delays
    )
    total_iters_with = sum(
        d if d > 0 else cutoff for d in sample_delays
    )

    if total_iters_without > 0:
        savings_pct = (1 - total_iters_with / total_iters_without) * 100
    else:
        savings_pct = 0

    return {
        "cutoff": cutoff,
        "total_without_termination": total_iters_without,
        "total_with_termination": total_iters_with,
        "savings_percent": savings_pct,
        "lychrel_count": sum(1 for d in sample_delays if d <= 0),
        "sample_size": len(sample_delays),
    }


if __name__ == "__main__":
    print("Adaptive cutoffs by digit length:")
    print(f"{'Digits':>8} {'Expected':>10} {'Cutoff (3σ)':>12}")
    print("-" * 32)
    for d in range(5, 36):
        expected = 14.255934 * d - 17.320261
        cutoff = adaptive_cutoff(d)
        print(f"{d:>8} {expected:>10.1f} {cutoff:>12}")

    # Demonstrate savings on 13-digit numbers
    print("\nDemonstrating savings on 13-digit numbers...")
    import ctypes
    import os
    import random

    random.seed(42)

    lib_path = os.path.join(os.path.dirname(__file__), "fast_core.so")
    lib = ctypes.CDLL(lib_path)
    lib.reverse_and_add_count.argtypes = [
        ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
    ]
    lib.reverse_and_add_count.restype = ctypes.c_int

    delays = []
    n_samples = 10000
    for _ in range(n_samples):
        n = random.randint(10**12, 10**13 - 1)
        d = lib.reverse_and_add_count(str(n).encode(), 10000, None, 0)
        delays.append(d)

    stats = estimate_savings(13, delays)
    print(f"Cutoff: {stats['cutoff']}")
    print(f"Lychrel candidates: {stats['lychrel_count']}/{stats['sample_size']}")
    print(f"Savings: {stats['savings_percent']:.1f}%")
