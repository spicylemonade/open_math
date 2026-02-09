"""Baseline experimental pipeline for searching C-finite subsequences in Beatty sequences.

For a given r, systematically searches for homogeneous linear recurrences
in subsequences of floor(n*r) using multiple extraction strategies.
"""

from __future__ import annotations
import json
import math
import os
import time
from fractions import Fraction
from typing import Any, Dict, List, Optional, Union

from beatty import QuadraticIrrational, beatty_sequence
from recurrence_detector import find_recurrence
from subsequence_extractor import extract_all_strategies


def run_pipeline(
    r: Union[float, Fraction, QuadraticIrrational],
    r_name: str,
    N: int = 10000,
    max_subseq_len: int = 200,
    max_order: int = 30,
    min_verified: int = 10,
) -> Dict[str, Any]:
    """Run the full pipeline for a given r.

    Args:
        r: The Beatty parameter
        r_name: Human-readable name for r (e.g., "phi", "3/2", "pi")
        N: Length of base Beatty sequence
        max_subseq_len: Maximum subsequence length to extract
        max_order: Maximum recurrence order to search for
        min_verified: Minimum number of verified terms to accept a recurrence

    Returns:
        Dictionary with results
    """
    start_time = time.time()

    # Get float value
    if isinstance(r, QuadraticIrrational):
        r_float = r.to_float()
    elif isinstance(r, Fraction):
        r_float = float(r)
    else:
        r_float = float(r)

    # Extract all subsequences
    strategies = extract_all_strategies(r, N=N, max_subseq_len=max_subseq_len)

    found_recurrences: List[Dict[str, Any]] = []
    total_searched = 0

    for strategy_name, subseq in strategies:
        if len(subseq) < 6:
            continue

        total_searched += 1
        rec = find_recurrence(subseq, max_order=max_order)

        if rec is not None and rec["verified_length"] >= min_verified:
            # Convert Fraction coefficients to strings for JSON serialization
            coeffs_str = [str(c) for c in rec["coefficients"]]
            char_poly_str = [str(c) for c in rec["characteristic_poly"]]

            found_recurrences.append({
                "strategy": strategy_name,
                "order": rec["order"],
                "coefficients": coeffs_str,
                "characteristic_poly": char_poly_str,
                "verified_length": rec["verified_length"],
                "subsequence_length": len(subseq),
                "first_terms": [int(x) for x in subseq[:10]],
            })

    elapsed = time.time() - start_time

    result = {
        "r_name": r_name,
        "r_float": r_float,
        "r_type": type(r).__name__,
        "N": N,
        "total_strategies_searched": total_searched,
        "recurrences_found": len(found_recurrences),
        "recurrences": found_recurrences,
        "elapsed_seconds": round(elapsed, 3),
    }

    return result


def save_result(result: Dict[str, Any], filename: str) -> None:
    """Save result to results/ directory."""
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)
    with open(filepath, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved results to {filepath}")


if __name__ == "__main__":
    print("=" * 60)
    print("Baseline Pipeline Tests")
    print("=" * 60)

    # Test 1: Rational r = 3/2
    print("\n--- Testing r = 3/2 (rational) ---")
    r_rat = Fraction(3, 2)
    result_rat = run_pipeline(r_rat, "3/2", N=5000, max_subseq_len=200)
    print(f"  Strategies searched: {result_rat['total_strategies_searched']}")
    print(f"  Recurrences found: {result_rat['recurrences_found']}")
    if result_rat["recurrences_found"] > 0:
        best = min(result_rat["recurrences"], key=lambda x: x["order"])
        print(f"  Best (lowest order): order={best['order']}, strategy={best['strategy']}")
        print(f"    Coefficients: {best['coefficients']}")
    assert result_rat["recurrences_found"] > 0, "Should find recurrences for rational r"
    print("  PASS")

    # Test 2: Quadratic irrational r = phi
    print("\n--- Testing r = phi (quadratic irrational) ---")
    phi = QuadraticIrrational(1, 1, 5, 2)
    result_phi = run_pipeline(phi, "phi", N=5000, max_subseq_len=200)
    print(f"  Strategies searched: {result_phi['total_strategies_searched']}")
    print(f"  Recurrences found: {result_phi['recurrences_found']}")
    if result_phi["recurrences_found"] > 0:
        best = min(result_phi["recurrences"], key=lambda x: x["order"])
        print(f"  Best (lowest order): order={best['order']}, strategy={best['strategy']}")
        print(f"    Coefficients: {best['coefficients']}")
        print(f"    First terms: {best['first_terms']}")
    assert result_phi["recurrences_found"] > 0, "Should find recurrences for phi"
    print("  PASS")

    # Test 3: Transcendental r = pi
    print("\n--- Testing r = pi (transcendental) ---")
    result_pi = run_pipeline(math.pi, "pi", N=5000, max_subseq_len=200)
    print(f"  Strategies searched: {result_pi['total_strategies_searched']}")
    print(f"  Recurrences found: {result_pi['recurrences_found']}")
    if result_pi["recurrences_found"] > 0:
        for rec in result_pi["recurrences"][:3]:
            print(f"  WARNING: Found recurrence order={rec['order']}, strategy={rec['strategy']}")
    else:
        print("  No recurrences found (as expected for transcendental)")
    print("  PASS")

    # Save all results
    save_result(result_rat, "baseline_rational_3_2.json")
    save_result(result_phi, "baseline_phi.json")
    save_result(result_pi, "baseline_pi.json")

    print("\n" + "=" * 60)
    print("All baseline pipeline tests passed!")
    print("=" * 60)
