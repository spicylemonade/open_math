#!/usr/bin/env python3
"""Rational Beatty sequence recurrence experiments.

For every reduced fraction r = p/q with 1 <= p, q <= 20, compute the Beatty
sequence floor(n*r) for n = 1..500, then use Berlekamp-Massey to detect the
minimal linear recurrence.  Compare the detected order against the theoretical
upper bound of q+1.

Results are saved to:
  results/rational_experiments.json
  results/rational_summary.md
"""

from __future__ import annotations

import json
import math
import os
import signal
import sys
import time
from fractions import Fraction

# Ensure the repo root is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from beatty import beatty_sequence
from recurrence_detector import find_recurrence

# ---------------------------------------------------------------------------
# Timeout handling
# ---------------------------------------------------------------------------

TIMEOUT_SECONDS = 120


class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError(f"Experiment exceeded {TIMEOUT_SECONDS}s timeout")


signal.signal(signal.SIGALRM, _timeout_handler)

# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------


def run_experiments():
    """Run all rational Beatty experiments and return the results dict."""
    # Enumerate all reduced fractions p/q with 1 <= p, q <= 20
    fractions_to_test = []
    for q in range(1, 21):
        for p in range(1, 21):
            if math.gcd(p, q) == 1:
                fractions_to_test.append((p, q))

    total = len(fractions_to_test)
    print(f"Testing {total} reduced fractions p/q with 1 <= p,q <= 20")
    print(f"Timeout: {TIMEOUT_SECONDS}s")
    print("-" * 60)

    experiments = []
    all_passed = True
    start_time = time.perf_counter()

    # Start the global alarm
    signal.alarm(TIMEOUT_SECONDS)

    try:
        for idx, (p, q) in enumerate(fractions_to_test):
            r = Fraction(p, q)
            theoretical_order = q + 1

            # Compute Beatty sequence
            seq = beatty_sequence(r, N=500)

            # Run recurrence detection
            result = find_recurrence(seq, max_order=50)

            if result is not None:
                detected_order = result["order"]
                detected_coefficients = [
                    float(c) if not isinstance(c, int) else c
                    for c in result["coefficients"]
                ]
                # Key test: does BM find order <= q+1?
                matches = detected_order <= theoretical_order
            else:
                detected_order = None
                detected_coefficients = []
                matches = False

            if not matches:
                all_passed = False

            experiments.append({
                "p": p,
                "q": q,
                "r_str": f"{p}/{q}",
                "theoretical_order": theoretical_order,
                "detected_order": detected_order,
                "detected_coefficients": detected_coefficients,
                "matches_theory": matches,
            })

            # Progress every 20 test cases
            if (idx + 1) % 20 == 0 or (idx + 1) == total:
                elapsed = time.perf_counter() - start_time
                print(
                    f"  [{idx + 1:>3}/{total}]  elapsed={elapsed:.1f}s  "
                    f"last: r={p}/{q}  detected_order={detected_order}  "
                    f"theory={theoretical_order}  ok={matches}"
                )

    except TimeoutError as exc:
        print(f"\nTIMEOUT: {exc}")
        print(f"Completed {len(experiments)}/{total} experiments before timeout.")
    finally:
        # Cancel alarm
        signal.alarm(0)

    elapsed_total = time.perf_counter() - start_time
    summary = {
        "total_tested": len(experiments),
        "total_planned": total,
        "all_passed": all_passed,
        "elapsed_seconds": round(elapsed_total, 2),
    }

    return {"experiments": experiments, "summary": summary}


def write_json(data, path):
    """Write data dict to JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"\nJSON results written to {path}")


def write_summary_md(data, path):
    """Write a brief Markdown summary of the experiments."""
    exps = data["experiments"]
    summ = data["summary"]
    os.makedirs(os.path.dirname(path), exist_ok=True)

    lines = []
    lines.append("# Rational Beatty Sequence Recurrence Experiments\n")
    lines.append(f"**Total fractions tested:** {summ['total_tested']}\n")
    lines.append(f"**All passed (detected order <= q+1):** {summ['all_passed']}\n")
    lines.append(f"**Elapsed time:** {summ['elapsed_seconds']}s\n")
    lines.append("")

    # Statistics
    if exps:
        orders_match_exact = sum(
            1 for e in exps
            if e["detected_order"] is not None and e["detected_order"] == e["theoretical_order"]
        )
        orders_strictly_less = sum(
            1 for e in exps
            if e["detected_order"] is not None and e["detected_order"] < e["theoretical_order"]
        )
        orders_exceeded = sum(
            1 for e in exps
            if e["detected_order"] is not None and e["detected_order"] > e["theoretical_order"]
        )
        no_recurrence = sum(1 for e in exps if e["detected_order"] is None)

        lines.append("## Summary Statistics\n")
        lines.append(f"| Metric | Count |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Detected order == q+1 (exact match) | {orders_match_exact} |")
        lines.append(f"| Detected order < q+1 (BM found lower) | {orders_strictly_less} |")
        lines.append(f"| Detected order > q+1 (exceeded theory) | {orders_exceeded} |")
        lines.append(f"| No recurrence found (order > max_order) | {no_recurrence} |")
        lines.append("")

        # Show the cases where BM found a strictly lower order
        lower_cases = [
            e for e in exps
            if e["detected_order"] is not None and e["detected_order"] < e["theoretical_order"]
        ]
        if lower_cases:
            lines.append("## Cases Where BM Found Lower Order Than q+1\n")
            lines.append("| r = p/q | Theory (q+1) | Detected | Difference |")
            lines.append("|---------|-------------|----------|------------|")
            for e in lower_cases:
                diff = e["theoretical_order"] - e["detected_order"]
                lines.append(
                    f"| {e['r_str']} | {e['theoretical_order']} | {e['detected_order']} | -{diff} |"
                )
            lines.append("")

        # Show any failures
        failures = [e for e in exps if not e["matches_theory"]]
        if failures:
            lines.append("## Failures (detected order > q+1)\n")
            lines.append("| r = p/q | Theory (q+1) | Detected |")
            lines.append("|---------|-------------|----------|")
            for e in failures:
                lines.append(
                    f"| {e['r_str']} | {e['theoretical_order']} | {e['detected_order']} |"
                )
            lines.append("")
        else:
            lines.append("## No Failures\n")
            lines.append(
                "All detected recurrence orders were at most q+1, "
                "consistent with the theoretical prediction.\n"
            )

        # Distribution table for small q
        lines.append("## Sample Results (q <= 5)\n")
        lines.append("| r = p/q | Theory (q+1) | Detected | Coefficients |")
        lines.append("|---------|-------------|----------|--------------|")
        for e in exps:
            if e["q"] <= 5:
                coeffs_str = str(e["detected_coefficients"][:6])
                if len(e["detected_coefficients"]) > 6:
                    coeffs_str = coeffs_str[:-1] + ", ...]"
                lines.append(
                    f"| {e['r_str']} | {e['theoretical_order']} "
                    f"| {e['detected_order']} | {coeffs_str} |"
                )
        lines.append("")

    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"Summary written to {path}")


def main():
    print("=" * 60)
    print("Rational Beatty Sequence Recurrence Experiments")
    print("=" * 60)
    print()

    data = run_experiments()

    # Paths
    repo_root = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(repo_root, "results", "rational_experiments.json")
    md_path = os.path.join(repo_root, "results", "rational_summary.md")

    write_json(data, json_path)
    write_summary_md(data, md_path)

    # Final console summary
    summ = data["summary"]
    print()
    print("=" * 60)
    print(f"DONE: {summ['total_tested']} fractions tested in {summ['elapsed_seconds']}s")
    print(f"All passed: {summ['all_passed']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
