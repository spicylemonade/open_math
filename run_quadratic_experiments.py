#!/usr/bin/env python3
"""Run quadratic irrational experiments on Beatty sequences.

For each quadratic irrational r = (a + b*sqrt(d))/c, compute the Beatty
sequence, extract Wythoff rows and iterated compositions, then search for
linear recurrences.
"""

import json
import math
import os
import signal
import sys
import time
from fractions import Fraction

# Ensure repo is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from beatty import QuadraticIrrational, beatty_sequence
from recurrence_detector import find_recurrence
from subsequence_extractor import wythoff_row, iterated_composition

# ---------------------------------------------------------------------------
# Timeout helper
# ---------------------------------------------------------------------------

class TimeoutError(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutError("Timed out")

TIMEOUT_SECONDS = 120

# ---------------------------------------------------------------------------
# Build the list of quadratic irrationals to test
# ---------------------------------------------------------------------------

def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    s = math.isqrt(n)
    return s * s == n


def build_candidates():
    """Return list of (name, QuadraticIrrational) pairs, all with value > 1
    and non-perfect-square d."""
    candidates = []

    # phi = (1+sqrt(5))/2
    candidates.append(("phi=(1+sqrt5)/2", QuadraticIrrational(1, 1, 5, 2)))

    # sqrt(d) for d in {2,3,5,6,7,8,10}
    for d in [2, 3, 5, 6, 7, 8, 10]:
        if not is_perfect_square(d):
            qi = QuadraticIrrational(0, 1, d, 1)
            if qi.to_float() > 1.0:
                candidates.append((f"sqrt({d})", qi))

    # (1+sqrt(d))/2 for many d values
    d_values_half = [2, 3, 5, 6, 7, 8, 10, 11, 13, 14, 15, 17, 19, 21,
                     23, 26, 29, 30, 33, 37, 41, 43, 46, 47, 50]
    for d in d_values_half:
        if not is_perfect_square(d):
            qi = QuadraticIrrational(1, 1, d, 2)
            if qi.to_float() > 1.0:
                candidates.append((f"(1+sqrt({d}))/2", qi))

    # 1+sqrt(2), 1+sqrt(3), 2+sqrt(5)
    extras = [
        ("1+sqrt(2)", QuadraticIrrational(1, 1, 2, 1)),
        ("1+sqrt(3)", QuadraticIrrational(1, 1, 3, 1)),
        ("2+sqrt(5)", QuadraticIrrational(2, 1, 5, 1)),
    ]
    for name, qi in extras:
        if not is_perfect_square(qi.d) and qi.to_float() > 1.0:
            candidates.append((name, qi))

    # De-duplicate by (a, b, d, c) tuple
    seen = set()
    unique = []
    for name, qi in candidates:
        key = (qi.a, qi.b, qi.d, qi.c)
        if key not in seen:
            seen.add(key)
            unique.append((name, qi))

    return unique


# ---------------------------------------------------------------------------
# Helpers to make JSON-serialisable results
# ---------------------------------------------------------------------------

def _coeff_to_str(c):
    """Convert a coefficient (int or Fraction) to a JSON-friendly string."""
    if isinstance(c, Fraction):
        if c.denominator == 1:
            return str(int(c))
        return str(c)
    return str(c)


def _summarise_recurrence(rec, strategy_name, subseq):
    """Create a JSON-friendly summary dict from a find_recurrence result."""
    return {
        "strategy": strategy_name,
        "order": rec["order"],
        "coefficients": [_coeff_to_str(c) for c in rec["coefficients"]],
        "characteristic_poly": [_coeff_to_str(c) for c in rec["characteristic_poly"]],
        "verified_length": rec["verified_length"],
        "subsequence_length": len(subseq),
        "first_terms": subseq[:10],
    }


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment_for(name: str, qi: QuadraticIrrational, N: int = 5000):
    """Run all extraction + recurrence detection for one quadratic irrational."""
    r_float = qi.to_float()
    print(f"  Computing Beatty sequence (N={N}) for {name} ~ {r_float:.10f} ...")

    seq = beatty_sequence(qi, N)

    recurrences_found = []
    strategies_searched = 0

    # --- Wythoff rows m=1,2,3 ---
    for m in [1, 2, 3]:
        strategy_name = f"wythoff_row_m{m}"
        strategies_searched += 1
        try:
            row = wythoff_row(qi, m, 200)
            if len(row) < 10:
                continue
            rec = find_recurrence(row, max_order=50)
            if rec is not None:
                recurrences_found.append(_summarise_recurrence(rec, strategy_name, row))
                print(f"    [FOUND] {strategy_name}: order={rec['order']}, "
                      f"verified={rec['verified_length']}")
        except Exception as e:
            print(f"    [ERROR] {strategy_name}: {e}")

    # --- Iterated composition (complement) for n_start=1, depth=30 ---
    strategy_name = "iterated_comp_n1_depth30"
    strategies_searched += 1
    try:
        comp_seq = iterated_composition(qi, n_start=1, depth=30, use_complement=True)
        if len(comp_seq) >= 10:
            rec = find_recurrence(comp_seq, max_order=50)
            if rec is not None:
                recurrences_found.append(_summarise_recurrence(rec, strategy_name, comp_seq))
                print(f"    [FOUND] {strategy_name}: order={rec['order']}, "
                      f"verified={rec['verified_length']}")
    except Exception as e:
        print(f"    [ERROR] {strategy_name}: {e}")

    # --- Iterated composition (complement) for n_start=2,3 as extras ---
    for ns in [2, 3]:
        strategy_name = f"iterated_comp_n{ns}_depth30"
        strategies_searched += 1
        try:
            comp_seq = iterated_composition(qi, n_start=ns, depth=30, use_complement=True)
            if len(comp_seq) >= 10:
                rec = find_recurrence(comp_seq, max_order=50)
                if rec is not None:
                    recurrences_found.append(_summarise_recurrence(rec, strategy_name, comp_seq))
                    print(f"    [FOUND] {strategy_name}: order={rec['order']}, "
                          f"verified={rec['verified_length']}")
        except Exception as e:
            print(f"    [ERROR] {strategy_name}: {e}")

    # --- Iterated a-composition (using r itself) for n_start=1 ---
    strategy_name = "iterated_a_comp_n1_depth30"
    strategies_searched += 1
    try:
        from subsequence_extractor import iterated_a_composition
        a_comp_seq = iterated_a_composition(r_float, n_start=1, depth=30)
        if len(a_comp_seq) >= 10:
            rec = find_recurrence(a_comp_seq, max_order=50)
            if rec is not None:
                recurrences_found.append(_summarise_recurrence(rec, strategy_name, a_comp_seq))
                print(f"    [FOUND] {strategy_name}: order={rec['order']}, "
                      f"verified={rec['verified_length']}")
    except Exception as e:
        print(f"    [ERROR] {strategy_name}: {e}")

    # Determine best (lowest non-trivial order) recurrence
    non_trivial = [r for r in recurrences_found if r["order"] > 0]
    best = None
    if non_trivial:
        best = min(non_trivial, key=lambda r: r["order"])

    return {
        "name": name,
        "r_repr": repr(qi),
        "r_float": r_float,
        "r_params": {"a": qi.a, "b": qi.b, "d": qi.d, "c": qi.c},
        "discriminant_d": qi.d,
        "N": N,
        "strategies_searched": strategies_searched,
        "recurrences_found_count": len(recurrences_found),
        "best_recurrence": best,
        "all_recurrences": recurrences_found,
    }


def main():
    candidates = build_candidates()
    print(f"Built {len(candidates)} quadratic irrational candidates.\n")

    results = []
    total = len(candidates)

    # Set up signal-based timeout
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)

    for idx, (name, qi) in enumerate(candidates, 1):
        print(f"[{idx}/{total}] Processing: {name}")
        signal.alarm(TIMEOUT_SECONDS)
        t0 = time.time()
        try:
            result = run_experiment_for(name, qi, N=5000)
            elapsed = time.time() - t0
            result["elapsed_seconds"] = round(elapsed, 2)
            results.append(result)
            print(f"  Done in {elapsed:.1f}s  "
                  f"({result['recurrences_found_count']} recurrences found)\n")
        except TimeoutError:
            elapsed = time.time() - t0
            print(f"  TIMEOUT after {elapsed:.1f}s -- skipping\n")
            results.append({
                "name": name,
                "r_repr": repr(qi),
                "r_float": qi.to_float(),
                "r_params": {"a": qi.a, "b": qi.b, "d": qi.d, "c": qi.c},
                "discriminant_d": qi.d,
                "error": "timeout",
                "elapsed_seconds": round(elapsed, 2),
            })
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR: {e} (after {elapsed:.1f}s)\n")
            results.append({
                "name": name,
                "r_repr": repr(qi),
                "r_float": qi.to_float(),
                "r_params": {"a": qi.a, "b": qi.b, "d": qi.d, "c": qi.c},
                "discriminant_d": qi.d,
                "error": str(e),
                "elapsed_seconds": round(elapsed, 2),
            })
        finally:
            signal.alarm(0)

    signal.signal(signal.SIGALRM, old_handler)

    # Save results
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "quadratic_experiments.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Results saved to {out_path}")

    # Print summary table
    print("\n" + "=" * 90)
    print(f"{'Name':<25} {'r_float':>12} {'d':>4} {'#Rec':>5} {'Best Order':>11} {'Time(s)':>8}")
    print("-" * 90)
    for r in results:
        best_order = "--"
        if "best_recurrence" in r and r.get("best_recurrence"):
            best_order = str(r["best_recurrence"]["order"])
        elif "error" in r:
            best_order = "ERR"
        n_rec = r.get("recurrences_found_count", 0)
        print(f"{r['name']:<25} {r['r_float']:>12.8f} {r.get('discriminant_d','?'):>4} "
              f"{n_rec:>5} {best_order:>11} {r.get('elapsed_seconds', 0):>8.1f}")
    print("=" * 90)

    total_rec = sum(r.get("recurrences_found_count", 0) for r in results)
    print(f"\nTotal candidates: {len(results)}")
    print(f"Total recurrences found: {total_rec}")
    best_overall = None
    for r in results:
        b = r.get("best_recurrence")
        if b:
            if best_overall is None or b["order"] < best_overall["order"]:
                best_overall = b
                best_overall["_source_name"] = r["name"]
    if best_overall:
        print(f"Best overall: order {best_overall['order']} from "
              f"'{best_overall['_source_name']}' via {best_overall['strategy']}")
        print(f"  Coefficients: {best_overall['coefficients']}")


if __name__ == "__main__":
    main()
