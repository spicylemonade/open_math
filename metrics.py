"""Metrics for measuring recurrence quality and subsequence density.

Computes:
1. Recurrence order
2. Verified length
3. Subsequence density
4. Spectral radius of companion matrix
"""

from __future__ import annotations
import math
from fractions import Fraction
from typing import Dict, List, Any, Optional


def compute_spectral_radius(coefficients: List[Fraction]) -> float:
    """Compute the spectral radius of the companion matrix.

    The companion matrix for a_n = c_1*a_{n-1} + ... + c_k*a_{n-k} has
    eigenvalues equal to the roots of x^k - c_1*x^{k-1} - ... - c_k.

    Args:
        coefficients: List [c_1, ..., c_k] as Fractions.

    Returns:
        Spectral radius (max absolute value of eigenvalues).
    """
    import numpy as np

    k = len(coefficients)
    if k == 0:
        return 0.0

    # Build characteristic polynomial: x^k - c_1*x^{k-1} - ... - c_k
    # numpy.roots expects [1, -c_1, -c_2, ..., -c_k]
    poly_coeffs = [1.0] + [-float(c) for c in coefficients]
    roots = np.roots(poly_coeffs)
    return float(max(abs(r) for r in roots))


def compute_density(
    subsequence_length: int, total_sequence_length: int
) -> float:
    """Compute density of subsequence within the original sequence.

    Args:
        subsequence_length: Number of terms in the subsequence
        total_sequence_length: Total length N of the base Beatty sequence

    Returns:
        Density = subsequence_length / total_sequence_length
    """
    if total_sequence_length == 0:
        return 0.0
    return subsequence_length / total_sequence_length


def is_trivial_recurrence(order: int, coefficients: List[Fraction]) -> bool:
    """Check if a recurrence is trivial (constant or all-zeros).

    Args:
        order: Recurrence order
        coefficients: List [c_1, ..., c_k]

    Returns:
        True if the recurrence is trivial.
    """
    if order == 0:
        return True
    if order == 1:
        c = coefficients[0]
        if c == Fraction(1) or c == Fraction(0):
            return True
    return False


def compute_all_metrics(
    recurrence: Dict[str, Any],
    total_N: int,
) -> Dict[str, Any]:
    """Compute all quality metrics for a discovered recurrence.

    Args:
        recurrence: Dict with keys 'order', 'coefficients', 'verified_length',
                    'subsequence_length' (as returned by baseline_pipeline)
        total_N: Total length of the base Beatty sequence

    Returns:
        Dict with all computed metrics.
    """
    # Parse coefficients
    coeffs_str = recurrence.get("coefficients", [])
    coeffs = [Fraction(c) for c in coeffs_str]

    order = recurrence.get("order", 0)
    verified_length = recurrence.get("verified_length", 0)
    subseq_length = recurrence.get("subsequence_length", 0)

    # Spectral radius
    try:
        spectral_radius = compute_spectral_radius(coeffs)
    except Exception:
        spectral_radius = None

    # Density
    density = compute_density(subseq_length, total_N)

    # Trivial check
    trivial = is_trivial_recurrence(order, coeffs)

    return {
        "order": order,
        "verified_length": verified_length,
        "density": round(density, 6),
        "spectral_radius": round(spectral_radius, 6) if spectral_radius is not None else None,
        "is_trivial": trivial,
        "strategy": recurrence.get("strategy", ""),
    }


if __name__ == "__main__":
    print("=== Metrics Module Tests ===")

    # Test 1: Spectral radius of Fibonacci recurrence
    fib_coeffs = [Fraction(1), Fraction(1)]
    rho = compute_spectral_radius(fib_coeffs)
    phi = (1 + math.sqrt(5)) / 2
    assert abs(rho - phi) < 1e-10, f"Fibonacci spectral radius should be phi, got {rho}"
    print(f"PASS: Fibonacci spectral radius = {rho:.6f} (expected {phi:.6f})")

    # Test 2: Spectral radius of geometric (x2)
    geo_coeffs = [Fraction(2)]
    rho_geo = compute_spectral_radius(geo_coeffs)
    assert abs(rho_geo - 2.0) < 1e-10, f"Geometric spectral radius should be 2, got {rho_geo}"
    print(f"PASS: Geometric spectral radius = {rho_geo:.6f}")

    # Test 3: Density
    d = compute_density(100, 10000)
    assert abs(d - 0.01) < 1e-10
    print(f"PASS: Density = {d}")

    # Test 4: Trivial check
    assert is_trivial_recurrence(1, [Fraction(1)]) == True
    assert is_trivial_recurrence(1, [Fraction(0)]) == True
    assert is_trivial_recurrence(2, [Fraction(1), Fraction(1)]) == False
    assert is_trivial_recurrence(1, [Fraction(2)]) == False
    print("PASS: Trivial recurrence detection")

    # Test 5: Full metric computation
    rec = {
        "order": 2,
        "coefficients": ["1", "1"],
        "verified_length": 45,
        "subsequence_length": 50,
        "strategy": "wythoff_row1",
    }
    metrics = compute_all_metrics(rec, total_N=5000)
    assert metrics["order"] == 2
    assert metrics["verified_length"] == 45
    assert abs(metrics["density"] - 0.01) < 0.001
    assert abs(metrics["spectral_radius"] - phi) < 0.001
    assert metrics["is_trivial"] == False
    print(f"PASS: Full metrics = {metrics}")

    # Test 6: Pell spectral radius
    pell_coeffs = [Fraction(2), Fraction(1)]
    rho_pell = compute_spectral_radius(pell_coeffs)
    expected_pell = 1 + math.sqrt(2)
    assert abs(rho_pell - expected_pell) < 1e-10
    print(f"PASS: Pell spectral radius = {rho_pell:.6f} (expected {expected_pell:.6f})")

    print("\n=== All metrics tests passed ===")
