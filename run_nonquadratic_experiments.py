#!/usr/bin/env python3
"""Run non-quadratic irrational and CF-boundary experiments on Beatty sequences.

Part 1 (item_019): Test non-quadratic irrationals (algebraic degree >=3 and
transcendentals) to see if any subsequences of their Beatty sequences satisfy
non-trivial linear recurrences.

Part 2 (item_020): Test CF boundary experiments across three groups:
quadratic irrationals (bounded CF), near-bounded CF transcendentals,
and unbounded CF numbers.
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

from beatty import beatty_sequence, QuadraticIrrational
from recurrence_detector import find_recurrence
from subsequence_extractor import extract_all_strategies

# ---------------------------------------------------------------------------
# Timeout helper
# ---------------------------------------------------------------------------

class TimeoutError(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutError("Timed out")

TIMEOUT_SECONDS = 180

# ---------------------------------------------------------------------------
# Helpers
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


def is_trivial_recurrence(rec):
    """Return True if the recurrence is trivial (order 1 with coeff 0 or 1)."""
    if rec is None:
        return True
    if rec["order"] == 1:
        c = rec["coefficients"][0]
        if isinstance(c, Fraction):
            c = float(c)
        if isinstance(c, str):
            try:
                c = float(c)
            except ValueError:
                return False
        if c == 0 or c == 1:
            return True
    return False


def cf_to_float(cf_list, max_terms=None):
    """Convert a continued fraction [a0; a1, a2, ...] to a float using convergents."""
    if max_terms is not None:
        cf_list = cf_list[:max_terms]
    if not cf_list:
        return 0.0
    # Compute convergent p/q from right to left
    # More numerically stable: use forward recurrence
    # p_{-1} = 1, p_0 = a_0
    # q_{-1} = 0, q_0 = 1
    # p_k = a_k * p_{k-1} + p_{k-2}
    # q_k = a_k * q_{k-1} + q_{k-2}
    p_prev, p_curr = 1, cf_list[0]
    q_prev, q_curr = 0, 1
    for i in range(1, len(cf_list)):
        a = cf_list[i]
        p_prev, p_curr = p_curr, a * p_curr + p_prev
        q_prev, q_curr = q_curr, a * q_curr + q_prev
    return p_curr / q_curr


def solve_cubic_real(a, b, c, d):
    """Find the real root of ax^3 + bx^2 + cx + d = 0 closest to a given
    approximate value, using Newton's method."""
    # Start with a rough estimate from Cardano or just iterate
    # For simplicity, use Newton's method from a reasonable starting point
    import numpy as np
    coeffs = [a, b, c, d]
    roots = np.roots(coeffs)
    # Return the real root with largest real part
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-10]
    if real_roots:
        return max(real_roots)
    # fallback
    return roots[0].real


# ---------------------------------------------------------------------------
# Part 1: Non-quadratic irrationals
# ---------------------------------------------------------------------------

def build_nonquadratic_candidates():
    """Return list of (name, category, float_value) for non-quadratic irrationals."""
    candidates = []

    # Algebraic degree 3
    candidates.append(("2^(1/3)", "algebraic_deg3", 2.0 ** (1.0 / 3.0)))

    # Plastic ratio: real root of x^3 - x - 1 = 0
    plastic = solve_cubic_real(1, 0, -1, -1)
    candidates.append(("plastic_ratio (x^3-x-1)", "algebraic_deg3", plastic))

    # Tribonacci constant: real root of x^3 - x^2 - 1 = 0
    tribonacci = solve_cubic_real(1, -1, 0, -1)
    candidates.append(("tribonacci_const (x^3-x^2-1)", "algebraic_deg3", tribonacci))

    # 1 + 2^(1/3)
    candidates.append(("1+2^(1/3)", "algebraic_deg3", 1.0 + 2.0 ** (1.0 / 3.0)))

    # 1 + 5^(1/3)
    candidates.append(("1+5^(1/3)", "algebraic_deg3", 1.0 + 5.0 ** (1.0 / 3.0)))

    # Algebraic degree 4+
    candidates.append(("2^(1/4)", "algebraic_deg4+", 2.0 ** (1.0 / 4.0)))
    candidates.append(("3^(1/3)", "algebraic_deg4+", 3.0 ** (1.0 / 3.0)))
    candidates.append(("sqrt(2)+sqrt(3)", "algebraic_deg4+", math.sqrt(2) + math.sqrt(3)))
    candidates.append(("2^(1/5)", "algebraic_deg4+", 2.0 ** (1.0 / 5.0)))

    # Transcendentals
    candidates.append(("pi", "transcendental", math.pi))
    candidates.append(("e", "transcendental", math.e))
    candidates.append(("1+ln(2)", "transcendental", 1.0 + math.log(2)))
    candidates.append(("1+pi/4", "transcendental", 1.0 + math.pi / 4.0))
    candidates.append(("sqrt(2)+pi", "transcendental", math.sqrt(2) + math.pi))

    # Liouville-type number: sum(10^(-k!) for k=1..10) + 1
    liouville = 1.0 + sum(10.0 ** (-math.factorial(k)) for k in range(1, 11))
    candidates.append(("liouville_type", "transcendental", liouville))

    return candidates


def run_nonquadratic_experiment(name, category, r_float, N=10000, max_subseq_len=200, max_order=30):
    """Run pipeline for one non-quadratic irrational."""
    print(f"  Computing Beatty sequence (N={N}) for {name} ~ {r_float:.10f} ...")

    # Extract all subsequences
    all_subseqs = extract_all_strategies(r_float, N=N, max_subseq_len=max_subseq_len)
    print(f"    Extracted {len(all_subseqs)} subsequences")

    recurrences_found = []
    strategies_searched = 0

    for strat_name, subseq in all_subseqs:
        if len(subseq) < 10:
            continue
        strategies_searched += 1
        try:
            rec = find_recurrence(subseq, max_order=max_order)
            if rec is not None and not is_trivial_recurrence(rec):
                recurrences_found.append(_summarise_recurrence(rec, strat_name, subseq))
        except Exception as e:
            pass  # Skip errors in individual strategies

    # Determine best
    best = None
    if recurrences_found:
        best = min(recurrences_found, key=lambda r: r["order"])

    return {
        "name": name,
        "category": category,
        "r_float": r_float,
        "N": N,
        "strategies_searched": strategies_searched,
        "recurrences_found_count": len(recurrences_found),
        "best_recurrence": best,
        "all_recurrences": recurrences_found,
    }


def run_part1():
    """Run Part 1: non-quadratic irrational experiments."""
    print("=" * 80)
    print("PART 1: Non-Quadratic Irrational Experiments (item_019)")
    print("=" * 80)

    candidates = build_nonquadratic_candidates()
    print(f"Built {len(candidates)} non-quadratic irrational candidates.\n")

    results = []
    total = len(candidates)

    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)

    for idx, (name, category, r_float) in enumerate(candidates, 1):
        print(f"[{idx}/{total}] Processing: {name} ({category})")
        signal.alarm(TIMEOUT_SECONDS)
        t0 = time.time()
        try:
            result = run_nonquadratic_experiment(name, category, r_float)
            elapsed = time.time() - t0
            result["elapsed_seconds"] = round(elapsed, 2)
            results.append(result)
            n_rec = result["recurrences_found_count"]
            print(f"  Done in {elapsed:.1f}s ({n_rec} non-trivial recurrences found)\n")
        except TimeoutError:
            elapsed = time.time() - t0
            print(f"  TIMEOUT after {elapsed:.1f}s -- skipping\n")
            results.append({
                "name": name,
                "category": category,
                "r_float": r_float,
                "error": "timeout",
                "elapsed_seconds": round(elapsed, 2),
            })
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR: {e} (after {elapsed:.1f}s)\n")
            results.append({
                "name": name,
                "category": category,
                "r_float": r_float,
                "error": str(e),
                "elapsed_seconds": round(elapsed, 2),
            })
        finally:
            signal.alarm(0)

    signal.signal(signal.SIGALRM, old_handler)

    # Save results
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "non_quadratic_experiments.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Results saved to {out_path}")

    # Print summary table
    print("\n" + "=" * 100)
    print(f"{'Name':<35} {'Category':<18} {'r_float':>12} {'#Rec':>5} {'Best Order':>11} {'Time(s)':>8}")
    print("-" * 100)
    for r in results:
        best_order = "--"
        if r.get("best_recurrence"):
            best_order = str(r["best_recurrence"]["order"])
        elif "error" in r:
            best_order = "ERR"
        n_rec = r.get("recurrences_found_count", 0)
        print(f"{r['name']:<35} {r.get('category',''):<18} {r['r_float']:>12.8f} "
              f"{n_rec:>5} {best_order:>11} {r.get('elapsed_seconds', 0):>8.1f}")
    print("=" * 100)

    total_rec = sum(r.get("recurrences_found_count", 0) for r in results)
    print(f"\nTotal candidates: {len(results)}")
    print(f"Total non-trivial recurrences found: {total_rec}")

    return results


# ---------------------------------------------------------------------------
# Part 2: CF Boundary Experiments
# ---------------------------------------------------------------------------

def build_cf_boundary_groups():
    """Return dict of group_name -> list of (name, r_value, cf_description)."""
    groups = {}

    # Group 1: Quadratic irrationals (bounded CF by Lagrange's theorem)
    group1 = []
    group1.append(("phi=(1+sqrt(5))/2", QuadraticIrrational(1, 1, 5, 2), "CF purely periodic [1;1,1,1,...]"))
    group1.append(("sqrt(2)", QuadraticIrrational(0, 1, 2, 1), "CF [1;2,2,2,...] - bounded"))
    group1.append(("sqrt(3)", QuadraticIrrational(0, 1, 3, 1), "CF [1;1,2,1,2,...] - bounded"))
    group1.append(("1+sqrt(2)", QuadraticIrrational(1, 1, 2, 1), "CF [2;2,4,2,4,...] - bounded"))
    # (1+sqrt(5))/2 is the same as phi, so use a different one
    group1.append(("(3+sqrt(5))/2", QuadraticIrrational(3, 1, 5, 2), "CF [2;1,1,1,...] - bounded"))
    groups["group1_quadratic_bounded_cf"] = group1

    # Group 2: Non-quadratic with nearly-bounded CF
    # Construct numbers from explicit CF expansions
    group2 = []

    # CF [1; 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, ...]
    # Period [1,2] with one perturbation (3) inserted at position 7
    cf_pattern_1 = [1]
    # Build a long CF: period [1,2] with perturbation at every 7th partial quotient
    for i in range(500):
        if (i + 1) % 7 == 0:
            cf_pattern_1.append(3)  # perturbation
        elif i % 2 == 0:
            cf_pattern_1.append(1)
        else:
            cf_pattern_1.append(2)
    val_1 = cf_to_float(cf_pattern_1, max_terms=200)
    group2.append(("cf_perturbed_12_period", val_1, "CF [1;1,2,1,2,1,3,1,2,...] perturbed period"))

    # CF [1; 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 1, 2, ...] - period broken once
    cf_pattern_2 = [1]
    for i in range(500):
        if i == 11:  # position 12 (0-indexed), break the period once
            cf_pattern_2.append(3)
        elif i % 2 == 0:
            cf_pattern_2.append(1)
        else:
            cf_pattern_2.append(2)
    val_2 = cf_to_float(cf_pattern_2, max_terms=200)
    group2.append(("cf_single_perturbation", val_2, "CF [1;1,2,1,2,...,3,...,1,2,...] single break"))

    # CF with bounded but non-periodic quotients: [1; 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, ...]
    # Quotients are always 1 or 2 (bounded) but pattern is non-periodic (increasing runs)
    cf_pattern_3 = [1]
    run_len = 1
    current_val = 1
    count = 0
    while count < 500:
        for _ in range(run_len):
            if count >= 500:
                break
            cf_pattern_3.append(current_val)
            count += 1
        run_len += 1
        current_val = 3 - current_val  # toggle between 1 and 2
    val_3 = cf_to_float(cf_pattern_3, max_terms=200)
    group2.append(("cf_bounded_nonperiodic", val_3, "CF with quotients in {1,2} non-periodic increasing runs"))

    # CF with Thue-Morse-like pattern on {1,2} (known to be transcendental by Adamczewski-Bugeaud)
    # Thue-Morse: t(0)=0, t(2n)=t(n), t(2n+1)=1-t(n)
    def thue_morse(n):
        return bin(n).count('1') % 2
    cf_thue_morse = [1]
    for i in range(500):
        cf_thue_morse.append(1 + thue_morse(i))  # values in {1, 2}
    val_tm = cf_to_float(cf_thue_morse, max_terms=200)
    group2.append(("cf_thue_morse_12", val_tm, "CF [1; Thue-Morse on {1,2}] - transcendental, bounded"))

    # CF with Rudin-Shapiro-like pattern on {1,2}
    def rudin_shapiro_bit(n):
        """Count of '11' in binary representation of n, mod 2."""
        b = bin(n)[2:]
        count = sum(1 for i in range(len(b)-1) if b[i] == '1' and b[i+1] == '1')
        return count % 2
    cf_rs = [1]
    for i in range(500):
        cf_rs.append(1 + rudin_shapiro_bit(i))
    val_rs = cf_to_float(cf_rs, max_terms=200)
    group2.append(("cf_rudin_shapiro_12", val_rs, "CF [1; Rudin-Shapiro on {1,2}] - bounded"))

    groups["group2_nonquadratic_bounded_cf"] = group2

    # Group 3: Unbounded CF
    group3 = []
    group3.append(("e", math.e, "CF [2;1,2,1,1,4,1,1,6,...] - unbounded"))
    group3.append(("pi", math.pi, "CF [3;7,15,1,292,...] - unbounded"))
    group3.append(("e^2", math.e ** 2, "CF unbounded"))
    group3.append(("1+ln(3)", 1.0 + math.log(3), "CF likely unbounded"))
    group3.append(("1+tan(1)", 1.0 + math.tan(1), "CF likely unbounded"))
    groups["group3_unbounded_cf"] = group3

    return groups


def run_cf_experiment_for(name, r_value, cf_desc, N=10000, max_subseq_len=200, max_order=30):
    """Run pipeline for one CF-boundary experiment."""
    # Determine if r_value is a QuadraticIrrational or float
    if isinstance(r_value, QuadraticIrrational):
        r_float = r_value.to_float()
        r_for_beatty = r_float  # Use float path for consistency across all groups
    else:
        r_float = float(r_value)
        r_for_beatty = r_float

    print(f"    {name} ~ {r_float:.10f}")

    all_subseqs = extract_all_strategies(r_for_beatty, N=N, max_subseq_len=max_subseq_len)

    recurrences_found = []
    strategies_searched = 0

    for strat_name, subseq in all_subseqs:
        if len(subseq) < 10:
            continue
        strategies_searched += 1
        try:
            rec = find_recurrence(subseq, max_order=max_order)
            if rec is not None and not is_trivial_recurrence(rec):
                recurrences_found.append(_summarise_recurrence(rec, strat_name, subseq))
        except Exception:
            pass

    best = None
    if recurrences_found:
        best = min(recurrences_found, key=lambda r: r["order"])

    return {
        "name": name,
        "r_float": r_float,
        "cf_description": cf_desc,
        "N": N,
        "strategies_searched": strategies_searched,
        "recurrences_found_count": len(recurrences_found),
        "best_recurrence": best,
        "all_recurrences": recurrences_found,
    }


def run_part2():
    """Run Part 2: CF boundary experiments."""
    print("\n" + "=" * 80)
    print("PART 2: Continued Fraction Boundary Experiments (item_020)")
    print("=" * 80)

    groups = build_cf_boundary_groups()
    all_results = {}

    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)

    for group_name, members in groups.items():
        print(f"\n--- {group_name} ({len(members)} members) ---")
        group_results = []

        for idx, member in enumerate(members, 1):
            name = member[0]
            r_value = member[1]
            cf_desc = member[2]

            print(f"  [{idx}/{len(members)}] Processing: {name}")
            signal.alarm(TIMEOUT_SECONDS)
            t0 = time.time()
            try:
                result = run_cf_experiment_for(name, r_value, cf_desc)
                elapsed = time.time() - t0
                result["elapsed_seconds"] = round(elapsed, 2)
                group_results.append(result)
                n_rec = result["recurrences_found_count"]
                print(f"      {n_rec} non-trivial recurrences, {elapsed:.1f}s")
            except TimeoutError:
                elapsed = time.time() - t0
                print(f"      TIMEOUT after {elapsed:.1f}s")
                group_results.append({
                    "name": name,
                    "r_float": r_value.to_float() if isinstance(r_value, QuadraticIrrational) else float(r_value),
                    "cf_description": cf_desc,
                    "error": "timeout",
                    "elapsed_seconds": round(elapsed, 2),
                })
            except Exception as e:
                elapsed = time.time() - t0
                print(f"      ERROR: {e} ({elapsed:.1f}s)")
                group_results.append({
                    "name": name,
                    "r_float": r_value.to_float() if isinstance(r_value, QuadraticIrrational) else float(r_value),
                    "cf_description": cf_desc,
                    "error": str(e),
                    "elapsed_seconds": round(elapsed, 2),
                })
            finally:
                signal.alarm(0)

        all_results[group_name] = group_results

    signal.signal(signal.SIGALRM, old_handler)

    # Save results
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cf_boundary_experiments.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to {out_path}")

    # Print summary
    print("\n" + "=" * 100)
    print("CF BOUNDARY EXPERIMENT SUMMARY")
    print("=" * 100)
    for group_name, group_results in all_results.items():
        total_rec = sum(r.get("recurrences_found_count", 0) for r in group_results)
        n_with_rec = sum(1 for r in group_results if r.get("recurrences_found_count", 0) > 0)
        print(f"\n  {group_name}:")
        print(f"    Members tested: {len(group_results)}")
        print(f"    Members with non-trivial recurrences: {n_with_rec}")
        print(f"    Total non-trivial recurrences: {total_rec}")
        for r in group_results:
            best_order = "--"
            if r.get("best_recurrence"):
                best_order = str(r["best_recurrence"]["order"])
            elif "error" in r:
                best_order = "ERR"
            n_rec = r.get("recurrences_found_count", 0)
            print(f"      {r['name']:<35} r={r['r_float']:>12.8f}  #rec={n_rec:>3}  best_order={best_order:>4}  {r.get('elapsed_seconds',0):.1f}s")
    print("=" * 100)

    return all_results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.time()

    part1_results = run_part1()
    part2_results = run_part2()

    total_elapsed = time.time() - t_start
    print(f"\n\nTotal wall-clock time: {total_elapsed:.1f}s")

    # Final combined analysis
    print("\n" + "=" * 80)
    print("COMBINED ANALYSIS")
    print("=" * 80)

    # Part 1 analysis
    p1_with_rec = [r for r in part1_results if r.get("recurrences_found_count", 0) > 0]
    p1_without = [r for r in part1_results if r.get("recurrences_found_count", 0) == 0 and "error" not in r]
    print(f"\nPart 1 (non-quadratic irrationals):")
    print(f"  Tested: {len(part1_results)}")
    print(f"  With non-trivial recurrences: {len(p1_with_rec)}")
    print(f"  Without non-trivial recurrences: {len(p1_without)}")
    if p1_with_rec:
        print("  Numbers with recurrences:")
        for r in p1_with_rec:
            best = r["best_recurrence"]
            print(f"    {r['name']}: best order={best['order']}, strategy={best['strategy']}, "
                  f"coeffs={best['coefficients'][:5]}{'...' if len(best['coefficients']) > 5 else ''}")

    # Part 2 analysis
    print(f"\nPart 2 (CF boundary experiments):")
    for group_name, group_results in part2_results.items():
        total_rec = sum(r.get("recurrences_found_count", 0) for r in group_results)
        n_with = sum(1 for r in group_results if r.get("recurrences_found_count", 0) > 0)
        print(f"  {group_name}: {n_with}/{len(group_results)} have recurrences, total={total_rec}")

    # Key finding: do quadratic irrationals show more recurrences than others?
    g1_data = part2_results.get("group1_quadratic_bounded_cf", [])
    g2_data = part2_results.get("group2_nonquadratic_bounded_cf", [])
    g3_data = part2_results.get("group3_unbounded_cf", [])

    g1_rec_rate = sum(1 for r in g1_data if r.get("recurrences_found_count", 0) > 0) / max(len(g1_data), 1)
    g2_rec_rate = sum(1 for r in g2_data if r.get("recurrences_found_count", 0) > 0) / max(len(g2_data), 1)
    g3_rec_rate = sum(1 for r in g3_data if r.get("recurrences_found_count", 0) > 0) / max(len(g3_data), 1)

    print(f"\n  Recurrence detection rates:")
    print(f"    Group 1 (quadratic, bounded CF):      {g1_rec_rate:.0%}")
    print(f"    Group 2 (non-quadratic, bounded CF):   {g2_rec_rate:.0%}")
    print(f"    Group 3 (unbounded CF):               {g3_rec_rate:.0%}")

    g1_avg = sum(r.get("recurrences_found_count", 0) for r in g1_data) / max(len(g1_data), 1)
    g2_avg = sum(r.get("recurrences_found_count", 0) for r in g2_data) / max(len(g2_data), 1)
    g3_avg = sum(r.get("recurrences_found_count", 0) for r in g3_data) / max(len(g3_data), 1)

    print(f"\n  Average recurrences per number:")
    print(f"    Group 1 (quadratic, bounded CF):      {g1_avg:.1f}")
    print(f"    Group 2 (non-quadratic, bounded CF):   {g2_avg:.1f}")
    print(f"    Group 3 (unbounded CF):               {g3_avg:.1f}")


if __name__ == "__main__":
    main()
