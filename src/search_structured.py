"""Structured factorization-based search for unitary perfect numbers.

Exploits the multiplicative structure of sigma* to search for UPNs by
enumerating candidate prime factorizations and checking the product
equation prod(1 + p_i^{a_i}) = 2 * prod(p_i^{a_i}).
"""

import json
import time
import math
import signal
from sympy import primerange

from src.unitary import KNOWN_UPNS


# Pre-compute odd primes
ODD_PRIMES = list(primerange(3, 2000))

# Pre-compute cumulative max products (float) for fast pruning
# _cum_max[(i, j)] = max product achievable with j primes starting at index i
_MAX_K = 15
_cum_max = {}
for _i in range(len(ODD_PRIMES)):
    prod_val = 1.0
    for _j in range(min(_MAX_K, len(ODD_PRIMES) - _i)):
        prod_val *= (1 + 1.0 / ODD_PRIMES[_i + _j])
        _cum_max[(_i, _j + 1)] = prod_val


class _CellTimeout(Exception):
    pass


_cell_deadline = None


def _get_max_product(prime_idx, count):
    """Get upper bound on product achievable with 'count' primes starting at prime_idx."""
    key = (prime_idx, count)
    if key in _cum_max:
        return _cum_max[key]
    if prime_idx + count > len(ODD_PRIMES):
        return 0.0
    result = 1.0
    for i in range(count):
        result *= (1 + 1.0 / ODD_PRIMES[prime_idx + i])
    return result


def search_structured(max_m=20, max_k=13, max_odd_primes=None, verbose=True,
                      timeout_seconds=300):
    """Search for UPNs via structured factorization enumeration.

    Args:
        max_m: Maximum 2-adic valuation to consider.
        max_k: Maximum number of distinct prime factors (including 2).
        max_odd_primes: Maximum number of odd primes.
        verbose: Print progress.
        timeout_seconds: Maximum time in seconds.

    Returns:
        Dict with results.
    """
    global _cell_deadline

    if max_odd_primes is None:
        max_odd_primes = max_k - 1

    upns_found = set()
    candidates_evaluated = 0
    cells_searched = []
    start_time = time.time()
    deadline = start_time + timeout_seconds
    timed_out = False

    # Iterate num_odd first (small values first = fast), then sweep all m
    # This ensures we cover all m values for small num_odd before spending
    # time on large num_odd values
    for num_odd in range(1, min(max_odd_primes, max_k - 1) + 1):
        if time.time() > deadline:
            timed_out = True
            break

        if verbose:
            elapsed = time.time() - start_time
            print(f"--- num_odd={num_odd}, elapsed={elapsed:.1f}s ---")

        for m in range(1, max_m + 1):
            if time.time() > deadline:
                timed_out = True
                break

            two_power = 2**m
            target_num = 2**(m + 1)
            target_den = 1 + two_power
            target_float = target_num / target_den

            k = num_odd + 1
            goto_log2 = 2**k
            max_odd_log2 = goto_log2 - m

            if max_odd_log2 <= 0:
                continue

            # Quick check: can num_odd smallest primes even reach target?
            if _get_max_product(0, num_odd) < target_float * 0.9999:
                cells_searched.append({"m": m, "num_odd": num_odd, "candidates": 0,
                                       "status": "pruned_impossible"})
                continue

            # Per-cell timeout: scale with complexity
            cell_time = min(3.0 + num_odd * 3.0, deadline - time.time())
            if cell_time <= 0:
                timed_out = True
                break

            _cell_deadline = time.time() + cell_time

            try:
                sols, cands = _search_fast(
                    target_num, target_den, num_odd, 0, max_odd_log2
                )
                candidates_evaluated += cands
                cells_searched.append({"m": m, "num_odd": num_odd, "candidates": cands,
                                       "solutions": len(sols), "status": "complete"})

                for sol in sols:
                    n = two_power
                    for p, a in sol:
                        n *= p**a
                    if n not in upns_found:
                        upns_found.add(n)
                        if verbose:
                            parts = ' * '.join(f'{p}^{a}' if a > 1 else str(p) for p, a in sol)
                            print(f"  FOUND UPN: {n} = 2^{m} * {parts} (m={m})")

            except _CellTimeout:
                cells_searched.append({"m": m, "num_odd": num_odd,
                                       "status": "cell_timeout"})
                if verbose:
                    print(f"  Cell (m={m}, num_odd={num_odd}) timed out")

        if timed_out:
            break

    elapsed = time.time() - start_time
    upns_sorted = sorted(upns_found)

    return {
        "upns_found": upns_sorted,
        "candidates_evaluated": candidates_evaluated,
        "time_elapsed": round(elapsed, 3),
        "timed_out": timed_out,
        "cells_searched": len(cells_searched),
        "parameters": {"max_m": max_m, "max_k": max_k, "max_odd_primes": max_odd_primes}
    }


def _search_fast(target_num, target_den, remaining, prime_idx, max_log2):
    """Fast recursive search using integer arithmetic for exact checks."""
    # Check cell timeout periodically
    if _cell_deadline is not None and time.time() > _cell_deadline:
        raise _CellTimeout()

    if remaining == 0:
        if target_num == target_den:
            return [[]], 1
        return [], 1

    target_float = target_num / target_den
    if target_float <= 1.0:
        return [], 1

    if prime_idx + remaining > len(ODD_PRIMES):
        return [], 1

    max_achievable = _get_max_product(prime_idx, remaining)
    if max_achievable < target_float * 0.9999:
        return [], 1

    solutions = []
    candidates = 0

    for idx in range(prime_idx, len(ODD_PRIMES)):
        p = ODD_PRIMES[idx]

        max_with_p = (1 + 1.0 / p)
        if remaining > 1 and idx + 1 < len(ODD_PRIMES):
            max_rest = _get_max_product(idx + 1, remaining - 1)
        elif remaining == 1:
            max_rest = 1.0
        else:
            break

        if max_with_p * max_rest < target_float * 0.9999:
            break

        pa = p
        for a in range(1, 30):
            log2_pa = a * math.log2(p)
            if log2_pa > max_log2:
                break

            contrib_float = (1 + pa) / pa
            if contrib_float * max_rest < target_float * 0.9999:
                break

            new_num = target_num * pa
            new_den = target_den * (1 + pa)
            g = math.gcd(new_num, new_den)
            new_num //= g
            new_den //= g

            sub_sols, sub_cands = _search_fast(
                new_num, new_den, remaining - 1, idx + 1, max_log2 - log2_pa
            )
            candidates += sub_cands

            for sol in sub_sols:
                solutions.append([(p, a)] + sol)

            pa *= p

    return solutions, candidates


def main():
    """Run structured search and save results."""
    print("Running structured search for UPNs...")
    print("Parameters: max_m=20, max_k=13, timeout=300s")

    result = search_structured(max_m=20, max_k=13, verbose=True, timeout_seconds=300)

    print(f"\nFound UPNs: {result['upns_found']}")
    print(f"Candidates evaluated: {result['candidates_evaluated']:,}")
    print(f"Time: {result['time_elapsed']}s")
    print(f"Timed out: {result['timed_out']}")

    found = set(result['upns_found'])
    for n in KNOWN_UPNS:
        status = "FOUND" if n in found else "not found"
        print(f"  {n}: {status}")

    with open("results/structured_search_metrics.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\nResults saved to results/structured_search_metrics.json")


if __name__ == "__main__":
    main()
