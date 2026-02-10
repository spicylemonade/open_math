"""Brute-force search for unitary perfect numbers.

Enumerates integers up to a given bound and checks each for the unitary
perfect property sigma*(n) = 2n.
"""

import json
import time
import sys

from src.unitary import is_unitary_perfect


def brute_search(bound, verbose=True):
    """Search for unitary perfect numbers up to bound.

    Args:
        bound: Upper limit for the search (inclusive).
        verbose: If True, print progress updates.

    Returns:
        Dict with keys: upns_found (list), integers_checked (int),
        time_elapsed (float).
    """
    upns_found = []
    start_time = time.time()

    for n in range(1, bound + 1):
        if is_unitary_perfect(n):
            upns_found.append(n)
            if verbose:
                elapsed = time.time() - start_time
                print(f"  Found UPN: {n} (after {elapsed:.2f}s, checked {n} integers)")

        if verbose and n % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"  Progress: checked {n}/{bound} ({100*n/bound:.1f}%) in {elapsed:.2f}s")

    elapsed = time.time() - start_time
    return {
        "upns_found": upns_found,
        "integers_checked": bound,
        "time_elapsed": round(elapsed, 3),
    }


def main():
    """Run brute-force search and save results."""
    bounds = [100000, 1000000]
    all_results = {}

    for bound in bounds:
        print(f"\nSearching up to {bound:,}...")
        result = brute_search(bound)
        all_results[str(bound)] = result
        print(f"  Found UPNs: {result['upns_found']}")
        print(f"  Time: {result['time_elapsed']}s")

    # Save results
    with open("results/brute_search_metrics.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\nResults saved to results/brute_search_metrics.json")


if __name__ == "__main__":
    main()
