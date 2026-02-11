"""Exhaustive structured search for unitary perfect numbers.

Searches all (m, k) pairs with m = 1..30 (v_2(n) <= 30) and k = 2..15
(omega(n) <= 15).  For each cell, enumerates candidate factorizations
    n = 2^m * p_1^{a_1} * ... * p_{k-1}^{a_{k-1}}
with k-1 distinct odd primes, applies Goto's bound n < 2^{2^k} to limit
prime-power sizes, and uses the product equation
    prod(1 + p_i^{a_i}) = 2 * prod(p_i^{a_i})
to prune and verify candidates.

Uses the fast integer-arithmetic recursive search from
src.search_structured.
"""

import json
import math
import time

from src.search_structured import (
    _search_fast,
    ODD_PRIMES,
    _get_max_product,
    _CellTimeout,
    _cell_deadline,
)
import src.search_structured as _ss
from src.unitary import KNOWN_UPNS


def exhaustive_search(max_m=30, max_k=15, timeout_seconds=300, verbose=True):
    """Run an exhaustive search over all (m, k) cells.

    Args:
        max_m: Maximum power of 2 (v_2(n)), range 1..max_m.
        max_k: Maximum omega(n) (total distinct prime factors including 2),
               range 2..max_k.
        timeout_seconds: Global timeout in seconds.
        verbose: Whether to print progress.

    Returns:
        dict with solutions_found, cells, total_candidates, total_time.
    """
    start_time = time.time()
    global_deadline = start_time + timeout_seconds

    solutions_found = set()
    cells = []
    total_candidates = 0

    # Iterate k first (small k = fast), then sweep all m values
    # This ensures we find UPNs with few prime factors quickly
    for k in range(2, max_k + 1):
        if time.time() > global_deadline:
            # Mark remaining cells as timeout
            for k2 in range(k, max_k + 1):
                for m2 in range(1, max_m + 1):
                    if not any(c["m"] == m2 and c["k"] == k2 for c in cells):
                        cells.append({
                            "m": m2, "k": k2, "candidates": 0,
                            "solutions": 0, "status": "timeout"
                        })
            break

        for m in range(1, max_m + 1):
            num_odd = k - 1  # number of distinct odd prime factors

            if time.time() > global_deadline:
                cells.append({
                    "m": m, "k": k, "candidates": 0,
                    "solutions": 0, "status": "timeout"
                })
                continue

            # --- Goto's bound: n < 2^{2^k} ---
            # Since n = 2^m * (odd part), the odd part must satisfy
            # log2(odd part) < 2^k - m.
            goto_log2 = 2 ** k
            max_odd_log2 = goto_log2 - m
            if max_odd_log2 <= 0:
                cells.append({
                    "m": m, "k": k, "candidates": 0,
                    "solutions": 0, "status": "pruned_goto"
                })
                continue

            # --- Product equation setup ---
            # sigma*(n) = 2n requires:
            #   (1 + 2^m) * prod_{i}(1 + p_i^{a_i}) = 2 * 2^m * prod_{i}(p_i^{a_i})
            # Rearranging:
            #   prod_{i}((1 + p_i^{a_i}) / p_i^{a_i}) = 2^{m+1} / (1 + 2^m)
            #
            # We pass target_num / target_den as an exact fraction to _search_fast.
            two_power = 2 ** m
            target_num = 2 ** (m + 1)       # = 2 * 2^m
            target_den = 1 + two_power      # = 1 + 2^m

            # Quick feasibility check: can num_odd smallest primes reach
            # the target ratio?
            target_float = target_num / target_den
            max_achievable = _get_max_product(0, num_odd)
            if max_achievable < target_float * 0.9999:
                cells.append({
                    "m": m, "k": k, "candidates": 0,
                    "solutions": 0, "status": "pruned_impossible"
                })
                continue

            # --- Per-cell timeout ---
            # Scale with complexity but respect global deadline.
            cell_budget = min(3.0 + num_odd * 2.0, global_deadline - time.time())
            if cell_budget <= 0:
                cells.append({
                    "m": m, "k": k, "candidates": 0,
                    "solutions": 0, "status": "timeout"
                })
                continue

            _ss._cell_deadline = time.time() + cell_budget

            try:
                sols, cands = _search_fast(
                    target_num, target_den, num_odd, 0, max_odd_log2
                )
                total_candidates += cands

                cell_solutions = []
                for sol in sols:
                    n = two_power
                    for p, a in sol:
                        n *= p ** a
                    cell_solutions.append(n)
                    solutions_found.add(n)

                cells.append({
                    "m": m, "k": k, "candidates": cands,
                    "solutions": len(sols), "status": "complete"
                })

                if verbose and sols:
                    for sol in sols:
                        parts = " * ".join(
                            f"{p}^{a}" if a > 1 else str(p) for p, a in sol
                        )
                        n = two_power
                        for p, a in sol:
                            n *= p ** a
                        print(f"  FOUND UPN: {n} = 2^{m} * {parts}")

            except _CellTimeout:
                cells.append({
                    "m": m, "k": k, "candidates": 0,
                    "solutions": 0, "status": "timeout"
                })
                if verbose:
                    print(f"  Cell (m={m}, k={k}) timed out")

        if verbose:
            elapsed = time.time() - start_time
            complete = sum(1 for c in cells if c["status"] == "complete")
            timeout_ct = sum(1 for c in cells if c["status"] == "timeout")
            if m == max_m or time.time() > global_deadline:
                print(
                    f"k={k:2d} done | cells complete={complete}, "
                    f"timeout={timeout_ct}, total_cands={total_candidates:,}, "
                    f"elapsed={elapsed:.1f}s"
                )

    elapsed = time.time() - start_time
    solutions_sorted = sorted(solutions_found)

    return {
        "solutions_found": solutions_sorted,
        "cells": cells,
        "total_candidates": total_candidates,
        "total_time": round(elapsed, 3),
    }


def main():
    """Run exhaustive search and save results."""
    print("=" * 70)
    print("Exhaustive search for UPNs: omega(n) <= 15, v_2(n) <= 30")
    print("=" * 70)
    print(f"Using {len(ODD_PRIMES)} odd primes up to {ODD_PRIMES[-1]}")
    print(f"Timeout: 300 seconds")
    print()

    result = exhaustive_search(
        max_m=30, max_k=15, timeout_seconds=300, verbose=True
    )

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Solutions found: {result['solutions_found']}")
    print(f"Total candidates evaluated: {result['total_candidates']:,}")
    print(f"Total time: {result['total_time']}s")
    print()

    # Check against known UPNs
    found_set = set(result["solutions_found"])
    for n in KNOWN_UPNS:
        tag = "FOUND" if n in found_set else "not found"
        print(f"  Known UPN {n}: {tag}")

    # Cell summary
    statuses = {}
    for c in result["cells"]:
        s = c["status"]
        statuses[s] = statuses.get(s, 0) + 1
    print()
    print("Cell status summary:")
    for s, cnt in sorted(statuses.items()):
        print(f"  {s}: {cnt}")

    # Save results
    with open("results/exhaustive_search_results.json", "w") as f:
        # Convert any large ints to strings for JSON compatibility
        output = {
            "solutions_found": [
                str(x) if x > 2**53 else x for x in result["solutions_found"]
            ],
            "cells": result["cells"],
            "total_candidates": result["total_candidates"],
            "total_time": result["total_time"],
        }
        json.dump(output, f, indent=2)

    print("\nResults saved to results/exhaustive_search_results.json")


if __name__ == "__main__":
    main()
