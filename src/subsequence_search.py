"""
Systematic search framework for finding homogeneous linearly recurrent
subsequences within Beatty sequences floor(n*r).

Searches over:
  (a) Arithmetic progression subsequences with offset a and stride d
  (b) Nested Beatty subsequences indexed by floor(n*s)

References:
  - Beatty (1926), Fraenkel (1969)
  - Berlekamp (1968), Massey (1969) for recurrence detection
"""

import csv
import json
import os
import sys
import signal
import time
from fractions import Fraction
from typing import List, Optional, Tuple, Dict, Any

sys.path.insert(0, os.path.dirname(__file__))
from beatty import (beatty_sequence, parse_r_value, classify_r,
                    continued_fraction, subsequence_arithmetic)
from recurrence_detector import (find_homogeneous_recurrence,
                                 recurrence_to_homogeneous_form)


class ComputeTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise ComputeTimeout("Computation timed out")


def search_arithmetic_subsequences(
    r_spec: str,
    N: int = 50000,
    A_max: int = 20,
    D_max: int = 20,
    d_max_recurrence: int = 50,
    min_subseq_len: int = 500,
    timeout_seconds: int = 120,
    verbose: bool = False
) -> List[Dict[str, Any]]:
    """Search for linearly recurrent subsequences along arithmetic progressions.

    For each pair (a, d) with 0 <= a < d, 1 <= d <= D_max, extracts the
    subsequence floor((a + k*d)*r) for k = 0, 1, ..., and tests if it
    satisfies a homogeneous linear recurrence.

    Args:
        r_spec: String specification of r (e.g., "3/2", "golden_ratio")
        N: Length of the base Beatty sequence to compute
        A_max: Maximum offset to search
        D_max: Maximum stride to search
        d_max_recurrence: Maximum recurrence order to test
        min_subseq_len: Minimum subsequence length required
        timeout_seconds: Maximum time for the entire search
        verbose: Print progress

    Returns:
        List of dicts, each describing a found recurrence
    """
    results = []
    r_val = parse_r_value(r_spec)
    r_type = classify_r(r_spec)

    # Compute base sequence
    seq = beatty_sequence(r_val, N)

    # Set timeout
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_seconds)

    try:
        count = 0
        for d in range(1, D_max + 1):
            for a in range(min(A_max + 1, d)):
                # Extract subsequence: seq[a], seq[a+d], seq[a+2d], ...
                subseq = subsequence_arithmetic(seq, a, d)
                if len(subseq) < min_subseq_len:
                    continue

                result = find_homogeneous_recurrence(subseq, d_max_recurrence)
                count += 1

                if result is not None:
                    order, coeffs = result
                    int_c, readable = recurrence_to_homogeneous_form(order, coeffs)
                    entry = {
                        'r_spec': r_spec,
                        'r_type': r_type,
                        'subsequence_type': 'arithmetic_progression',
                        'ap_offset': a,
                        'ap_stride': d,
                        'recurrence_found': True,
                        'recurrence_order': order,
                        'recurrence_coefficients': str(int_c),
                        'recurrence_readable': readable,
                        'subseq_length': len(subseq),
                    }
                    results.append(entry)
                    if verbose:
                        print(f"  FOUND: r={r_spec}, a={a}, d={d}, "
                              f"order={order}: {readable}")

        if verbose and not results:
            print(f"  No recurrence found for r={r_spec} "
                  f"(tested {count} subsequences)")

    except ComputeTimeout:
        if verbose:
            print(f"  TIMEOUT for r={r_spec}")
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

    return results


def search_single_r(
    r_spec: str,
    N: int = 50000,
    A_max: int = 20,
    D_max: int = 20,
    d_max_recurrence: int = 50,
    timeout_seconds: int = 120,
    verbose: bool = False
) -> Dict[str, Any]:
    """Run full search for a single r value.

    Returns a summary dict with the best (lowest-order) recurrence found.
    """
    r_val = parse_r_value(r_spec)
    r_type = classify_r(r_spec)

    # Get continued fraction
    cf = continued_fraction(r_val, 50)

    # Search arithmetic progression subsequences
    all_results = search_arithmetic_subsequences(
        r_spec, N=N, A_max=A_max, D_max=D_max,
        d_max_recurrence=d_max_recurrence,
        timeout_seconds=timeout_seconds, verbose=verbose
    )

    # Also test the full sequence (a=0, d=1)
    seq_full = beatty_sequence(r_val, N)
    full_result = find_homogeneous_recurrence(seq_full, d_max_recurrence)
    if full_result is not None:
        order, coeffs = full_result
        int_c, readable = recurrence_to_homogeneous_form(order, coeffs)
        all_results.insert(0, {
            'r_spec': r_spec,
            'r_type': r_type,
            'subsequence_type': 'full_sequence',
            'ap_offset': 0,
            'ap_stride': 1,
            'recurrence_found': True,
            'recurrence_order': order,
            'recurrence_coefficients': str(int_c),
            'recurrence_readable': readable,
            'subseq_length': N,
        })

    # Build summary
    summary = {
        'r_value': r_spec,
        'r_type': r_type,
        'cf_partial_quotients_50': str(cf),
        'recurrence_found': len(all_results) > 0,
        'num_recurrences_found': len(all_results),
    }

    if all_results:
        # Find best (lowest order) recurrence
        best = min(all_results, key=lambda x: x['recurrence_order'])
        summary['min_recurrence_order'] = best['recurrence_order']
        summary['recurrence_coefficients'] = best['recurrence_coefficients']
        summary['subsequence_type'] = best['subsequence_type']
        summary['subsequence_params'] = f"a={best['ap_offset']},d={best['ap_stride']}"
        summary['best_readable'] = best['recurrence_readable']
    else:
        summary['min_recurrence_order'] = None
        summary['recurrence_coefficients'] = None
        summary['subsequence_type'] = None
        summary['subsequence_params'] = None
        summary['best_readable'] = None

    return summary


def run_search_battery(
    r_specs: List[str],
    output_csv: str = 'results/subsequence_search.csv',
    output_json: str = 'results/subsequence_search.json',
    N: int = 50000,
    A_max: int = 20,
    D_max: int = 20,
    d_max_recurrence: int = 50,
    verbose: bool = True
) -> List[Dict]:
    """Run the search for a battery of r values and save results."""
    all_summaries = []

    for i, r_spec in enumerate(r_specs):
        if verbose:
            print(f"\n[{i+1}/{len(r_specs)}] Searching r = {r_spec} ...")
        start_time = time.time()

        summary = search_single_r(
            r_spec, N=N, A_max=A_max, D_max=D_max,
            d_max_recurrence=d_max_recurrence,
            timeout_seconds=120, verbose=verbose
        )
        summary['runtime_seconds'] = round(time.time() - start_time, 2)
        all_summaries.append(summary)

        if verbose:
            found = summary['recurrence_found']
            if found:
                print(f"  => FOUND: order {summary['min_recurrence_order']}, "
                      f"{summary['best_readable']}")
            else:
                print(f"  => No recurrence found")

    # Save CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    fieldnames = ['r_value', 'r_type', 'cf_partial_quotients_50',
                  'recurrence_found', 'num_recurrences_found',
                  'min_recurrence_order', 'recurrence_coefficients',
                  'subsequence_type', 'subsequence_params',
                  'best_readable', 'runtime_seconds']
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in all_summaries:
            writer.writerow(s)

    # Save JSON
    with open(output_json, 'w') as f:
        json.dump(all_summaries, f, indent=2, default=str)

    if verbose:
        print(f"\nResults saved to {output_csv} and {output_json}")

    return all_summaries


# Default test battery
DEFAULT_R_SPECS = [
    # Rationals
    "3/2", "5/3", "7/4", "4/3", "7/5",
    "9/7", "11/8", "2/1", "1/1", "5/2",
    # Quadratic irrationals
    "golden_ratio", "sqrt(2)", "sqrt(3)", "sqrt(5)", "sqrt(7)",
    # Higher algebraic
    "cbrt(2)", "cbrt(3)", "root(2,4)", "root(3,4)", "cbrt(5)",
    # Transcendentals
    "pi", "e", "ln2",
]


if __name__ == "__main__":
    print("=== Subsequence Search Framework ===\n")

    results = run_search_battery(
        DEFAULT_R_SPECS,
        output_csv='results/subsequence_search.csv',
        output_json='results/subsequence_search.json',
        N=50000,
        A_max=20,
        D_max=20,
        d_max_recurrence=50,
        verbose=True
    )

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for s in results:
        found = "YES" if s['recurrence_found'] else "NO"
        order = s.get('min_recurrence_order', '-')
        print(f"  r={s['r_value']:20s} type={s['r_type']:25s} "
              f"recurrence={found:3s} order={order}")
