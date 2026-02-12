#!/usr/bin/env python3
"""
Item 020: Analyze distribution of Type-1 vs Type-2 solutions.

For primes up to 10^7, classify solutions into:
  - Type-1: at least one denominator divides n.
    For prime p, this means some denominator equals 1 or p.
    In practice for p > 4, this means setting a = p so that
    4/p = 1/p + 1/b + 1/c  =>  3/p = 1/b + 1/c.
  - Type-2: no denominator divides n.
    The standard parametric (x, y, z) decomposition where none of x, y, z
    divide p (for prime p, none equal 1 or p).

For each prime we search for BOTH types:
  - Type-1 via 3/p = 1/b + 1/c decomposition
  - Type-2 via the optimized parametric solver (skipping x=p)
Then we count how many primes have Type-1 solutions, Type-2 solutions,
or both.

Outputs:
    results/type_distribution.json  -- classification results and ratio
    figures/type_distribution.png   -- bar chart of distribution
"""

import sys
import os
import json
import math
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from src.optimized_solver import solve_fast, verify
from src.verify_pipeline import sieve_segment, precompute_small_primes

# Seed for reproducibility
np.random.seed(42)


def has_type1_solution(p):
    """
    Check if prime p has a Type-1 solution: 4/p = 1/p + 1/b + 1/c.
    This requires 3/p = 1/b + 1/c, i.e., 3*b*c = p*(b + c).
    Rearranging: c = p*b / (3*b - p).  For c to be a positive integer:
      3*b - p > 0  =>  b > p/3  =>  b >= ceil(p/3)
      also b <= 2*p/3 (for c >= b)
    and (3*b - p) | p*b.
    """
    if p <= 4:
        # p=2: 4/2=2, 1/2+1/b+1/c => 3/2=1/b+1/c => b=1,c=2. Sol: (1,2,2) but a=1|2, Type-1.
        # p=3: 4/3, a=3 => 3/3=1 => 1/b+1/c=1 => b=2,c=2. Sol: (2,2,3). 3|3? yes Type-1.
        return True

    b_min = p // 3 + 1  # ceil(p/3)
    b_max = 2 * p // 3 + 1  # slightly above p*2/3

    for b in range(b_min, b_max + 1):
        denom = 3 * b - p
        if denom <= 0:
            continue
        num = p * b
        if num % denom == 0:
            c = num // denom
            if c >= b:
                # Verify: 4/p = 1/p + 1/b + 1/c
                if verify(p, p, b, c):
                    return True
    return False


def has_type2_solution(p):
    """
    Check if prime p has a Type-2 solution: 4/p = 1/a + 1/b + 1/c
    where none of (a, b, c) divides p. For prime p, this means none
    of (a, b, c) equals 1 or p.
    """
    sol = solve_fast(p)
    if sol is None:
        return False
    a, b, c = sol
    # Check if this solution is Type-2 (no denominator divides p)
    if a != 1 and a != p and b != 1 and b != p and c != 1 and c != p:
        return True

    # The default solution might be Type-1; try harder to find Type-2
    # by searching with different x values that avoid x=p
    x_min = (p + 3) // 4
    x_max = x_min + 500

    for x in range(x_min, x_max + 1):
        if x == p or x == 1:
            continue
        A = 4 * x - p
        if A <= 0:
            continue
        nx = p * x
        D = nx * nx

        # Get divisors of (px)^2
        x_factors = {}
        temp = x
        d = 2
        while d * d <= temp:
            while temp % d == 0:
                x_factors[d] = x_factors.get(d, 0) + 1
                temp //= d
            d += 1
        if temp > 1:
            x_factors[temp] = x_factors.get(temp, 0) + 1

        all_factors = {k: 2 * v for k, v in x_factors.items()}
        all_factors[p] = all_factors.get(p, 0) + 2

        divs = [1]
        for prime, exp in all_factors.items():
            new_divs = []
            pe = 1
            for _ in range(exp + 1):
                for dd in divs:
                    new_divs.append(dd * pe)
                pe *= prime
            divs = new_divs

        target_mod = (-nx) % A

        for d1 in divs:
            if d1 > nx:
                continue
            if d1 % A != target_mod:
                continue
            d2 = D // d1
            if (d2 + nx) % A != 0:
                continue
            y = (d1 + nx) // A
            z = (d2 + nx) // A
            if y < x:
                continue
            if z < y:
                y, z = z, y
            if y < x:
                continue
            if verify(p, x, y, z):
                # Check Type-2
                vals = sorted([x, y, z])
                if all(v != 1 and v != p for v in vals):
                    return True

    return False


def main():
    print("=" * 60)
    print("Item 020: Type-1 vs Type-2 solution distribution")
    print("=" * 60)

    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    LIMIT = 10**7

    # Step 1: Generate primes up to LIMIT
    print(f"\nStep 1: Sieving primes up to {LIMIT:.0e}...")
    t0 = time.time()
    small_primes = precompute_small_primes(LIMIT)
    primes = sieve_segment(2, LIMIT, small_primes)
    print(f"  Found {len(primes)} primes in {time.time()-t0:.1f}s")

    # Step 2: Classify each prime
    print(f"\nStep 2: Classifying {len(primes)} primes (Type-1 / Type-2 / Both)...")
    t0 = time.time()

    type1_only = 0   # has Type-1 but NOT Type-2
    type2_only = 0   # has Type-2 but NOT Type-1
    both_types = 0   # has both
    neither = 0      # should not happen

    # Total counts
    s1_total = 0  # primes with at least one Type-1 solution
    s2_total = 0  # primes with at least one Type-2 solution

    type1_examples = []
    type2_examples = []

    # Decade breakdown
    decade_data = {}

    last_report = t0
    for idx, p in enumerate(primes):
        t1 = has_type1_solution(p)
        t2 = has_type2_solution(p)

        if t1:
            s1_total += 1
        if t2:
            s2_total += 1

        # Decade bucket
        if p >= 10:
            decade = int(math.log10(p))
        else:
            decade = 0
        dk = f"10^{decade}"
        if dk not in decade_data:
            decade_data[dk] = {"type1_only": 0, "type2_only": 0, "both": 0,
                               "s1": 0, "s2": 0, "total": 0}
        decade_data[dk]["total"] += 1
        if t1:
            decade_data[dk]["s1"] += 1
        if t2:
            decade_data[dk]["s2"] += 1

        if t1 and t2:
            both_types += 1
            decade_data[dk]["both"] += 1
        elif t1:
            type1_only += 1
            decade_data[dk]["type1_only"] += 1
            if len(type1_examples) < 20:
                type1_examples.append(p)
        elif t2:
            type2_only += 1
            decade_data[dk]["type2_only"] += 1
            if len(type2_examples) < 20:
                type2_examples.append(p)
        else:
            neither += 1

        now = time.time()
        if now - last_report > 10 or idx == len(primes) - 1:
            elapsed = now - t0
            rate = (idx + 1) / elapsed if elapsed > 0 else 0
            pct = (idx + 1) / len(primes) * 100
            print(f"  [{pct:.1f}%] {idx+1}/{len(primes)}, "
                  f"S1={s1_total} S2={s2_total} Both={both_types} "
                  f"T1only={type1_only} T2only={type2_only}, "
                  f"{rate:.0f}/sec")
            last_report = now

    total_time = time.time() - t0
    ratio = s1_total / s2_total if s2_total > 0 else float('inf')

    print(f"\n  Completed in {total_time:.1f}s")
    print(f"  Total primes: {len(primes)}")
    print(f"  S1 (has Type-1 solution): {s1_total}")
    print(f"  S2 (has Type-2 solution): {s2_total}")
    print(f"  Both types: {both_types}")
    print(f"  Type-1 only: {type1_only}")
    print(f"  Type-2 only: {type2_only}")
    print(f"  Neither: {neither}")
    print(f"  Ratio S1/S2: {ratio:.4f}")

    # Step 3: Save results
    ratio_safe = ratio if ratio != float('inf') else "inf"
    output = {
        "description": (
            "Type-1 vs Type-2 solution distribution for Erdos-Straus conjecture. "
            "Type-1: 4/p = 1/p + 1/b + 1/c (one denominator = p, so it divides p). "
            "Type-2: 4/p = 1/a + 1/b + 1/c where no denominator is 1 or p."
        ),
        "item": "020",
        "limit": LIMIT,
        "total_primes": len(primes),
        "S1_has_type1": s1_total,
        "S2_has_type2": s2_total,
        "both_types": both_types,
        "type1_only": type1_only,
        "type2_only": type2_only,
        "neither": neither,
        "ratio_S1_S2": ratio_safe,
        "S1_fraction": round(s1_total / len(primes), 6),
        "S2_fraction": round(s2_total / len(primes), 6),
        "decade_breakdown": decade_data,
        "type1_only_examples": type1_examples[:20],
        "type2_only_examples": type2_examples[:20],
        "runtime_seconds": round(total_time, 2),
        "reference_note": (
            "The 2025 paper (arXiv:2509.00128) reports S1=12,763,383 vs S2=5,838,200 "
            "for a broader range. Our analysis covers primes up to 10^7."
        ),
    }

    outfile = "results/type_distribution.json"
    with open(outfile, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {outfile}")

    # Step 4: Plots
    print("\nGenerating plots...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Panel 1: Overall bar chart
    ax1 = axes[0]
    categories = ['Type-1 only', 'Type-2 only', 'Both']
    counts = [type1_only, type2_only, both_types]
    colors_bar = ['#2196F3', '#FF9800', '#4CAF50']
    bars = ax1.bar(categories, counts, color=colors_bar, edgecolor='black', linewidth=0.5)
    for bar, count in zip(bars, counts):
        if count > 0:
            ax1.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + max(max(counts), 1) * 0.01,
                     f'{count:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Number of primes', fontsize=12)
    ax1.set_title(f'Solution type classification\n(primes up to {LIMIT:.0e})', fontsize=13)
    ax1.grid(axis='y', alpha=0.3)

    # Panel 2: Pie chart of S1 vs S2
    ax2 = axes[1]
    pie_sizes = [s1_total, s2_total]
    pie_labels = [
        f'S1 (Type-1)\n{s1_total:,}\n({100*s1_total/len(primes):.1f}%)',
        f'S2 (Type-2)\n{s2_total:,}\n({100*s2_total/len(primes):.1f}%)',
    ]
    pie_colors = ['#2196F3', '#FF9800']
    if all(s > 0 for s in pie_sizes):
        wedges, texts = ax2.pie(pie_sizes, labels=pie_labels, colors=pie_colors,
                                startangle=90, textprops={'fontsize': 10})
        ax2.set_title(f'S1/S2 = {ratio:.3f}', fontsize=13)
    else:
        # Handle case where one category is 0
        nonzero = [(s, l, c) for s, l, c in zip(pie_sizes, pie_labels, pie_colors) if s > 0]
        if nonzero:
            wedges, texts = ax2.pie([s for s, _, _ in nonzero],
                                    labels=[l for _, l, _ in nonzero],
                                    colors=[c for _, _, c in nonzero],
                                    startangle=90, textprops={'fontsize': 10})
        ax2.set_title(f'S1={s1_total:,}, S2={s2_total:,}', fontsize=13)

    # Panel 3: Distribution by decade
    ax3 = axes[2]
    decades_sorted = sorted(decade_data.keys(), key=lambda k: int(k.split('^')[1]))
    s1_decade = [decade_data[d]["s1"] for d in decades_sorted]
    s2_decade = [decade_data[d]["s2"] for d in decades_sorted]
    total_decade = [decade_data[d]["total"] for d in decades_sorted]

    # Plot ratio S1/total and S2/total per decade
    s1_frac = [100 * s / t if t > 0 else 0 for s, t in zip(s1_decade, total_decade)]
    s2_frac = [100 * s / t if t > 0 else 0 for s, t in zip(s2_decade, total_decade)]

    x_pos = np.arange(len(decades_sorted))
    width = 0.35
    ax3.bar(x_pos - width / 2, s1_frac, width, label='% with Type-1',
            color='#2196F3', edgecolor='black', linewidth=0.5)
    ax3.bar(x_pos + width / 2, s2_frac, width, label='% with Type-2',
            color='#FF9800', edgecolor='black', linewidth=0.5)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(decades_sorted, fontsize=9)
    ax3.set_xlabel('Prime range (decade)', fontsize=12)
    ax3.set_ylabel('Percentage (%)', fontsize=12)
    ax3.set_title('Type-1/Type-2 availability by decade', fontsize=13)
    ax3.legend(fontsize=10)
    ax3.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    figfile = "figures/type_distribution.png"
    plt.savefig(figfile, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Plot saved to {figfile}")

    print("\n" + "=" * 60)
    print("Item 020 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
