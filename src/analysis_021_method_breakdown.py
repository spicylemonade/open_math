#!/usr/bin/env python3
"""
Item 021: Method breakdown statistics for Erdos-Straus verification.

For primes up to 10^8, classify each prime by which method solves it:
  1. Mordell identity: can_solve_mordell(p) returns True
  2. Extended sieve: p is in the 6 hard residues mod 840, but solvable
     by the extended sieve (additional modular families mod 11,13,17,19,23)
  3. Brute-force/divisor search: remaining primes not covered by (1) or (2)

Uses segmented sieve for prime generation.

Outputs:
    results/method_breakdown.json   -- classification results
    figures/method_breakdown.png    -- stacked bar chart
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

from src.mordell_solver import can_solve_mordell
from src.verify_pipeline import sieve_segment, precompute_small_primes

# Seed for reproducibility
np.random.seed(42)

# The 6 hard residues mod 840 that Mordell identities cannot handle
HARD_RESIDUES_840 = frozenset({1, 121, 169, 289, 361, 529})

# Extended sieve: additional modular families that resolve some hard residues
# We replicate the logic from extended_sieve.py but inline the solvability check
# For each hard residue r mod 840 and extra modulus q, we precompute which
# combined residues (r mod 840, s mod q) are solvable.

EXTRA_MODULI = [11, 13, 17, 19, 23]


def _extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, s, t = _extended_gcd(b, a % b)
    return g, t, s - (a // b) * t


def _crt(r1, m1, r2, m2):
    """Chinese Remainder Theorem: find x = r1 (mod m1), x = r2 (mod m2)."""
    g = math.gcd(m1, m2)
    if (r1 - r2) % g != 0:
        return None
    lcm = m1 * m2 // g
    _, s, _ = _extended_gcd(m1, m2)
    x = (r1 + m1 * s * ((r2 - r1) // g)) % lcm
    return (x, lcm)


def _solve_quick(n):
    """Quick solver for checking if a prime can be solved."""
    if n <= 1:
        return None
    if n <= 5:
        return {2: (1, 2, 2), 3: (1, 4, 12), 4: (2, 4, 4), 5: (2, 4, 20)}.get(n)
    if n % 2 == 0:
        m = n // 2
        return (m, 2 * m, 2 * m)
    if n % 4 == 3:
        q = (n + 1) // 4
        m = n * q
        if m % 2 == 0:
            return tuple(sorted([q, 2 * m, 2 * m]))
        else:
            return tuple(sorted([q, m + 1, m * (m + 1)]))

    # Try divisor approach for p = 1 mod 4
    x_min = (n + 3) // 4
    for x in range(x_min, x_min + 200):
        A = 4 * x - n
        if A <= 0:
            continue
        nx = n * x
        D = nx * nx

        divs = _divisors_from_factored(n, x)
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
            if y >= x and z >= y:
                if 4 * x * y * z == n * (y * z + x * z + x * y):
                    return tuple(sorted([x, y, z]))
            elif z >= x and y >= z:
                if 4 * x * y * z == n * (y * z + x * z + x * y):
                    return tuple(sorted([x, y, z]))

    return None


def _divisors_from_factored(p, x):
    """Get divisors of p^2 * x^2 where p is prime."""
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
    return divs


def build_extended_sieve_table():
    """
    Build a lookup table for the extended sieve.
    For each hard residue r mod 840 and each extra modulus q,
    determine which residues s mod q are solvable.

    Returns a dict: (r, q) -> set of solvable residues s mod q.
    """
    from sympy import primerange

    solvable_table = {}
    for r in sorted(HARD_RESIDUES_840):
        for q in EXTRA_MODULI:
            solvable_s = set()
            for s in range(q):
                result = _crt(r, 840, s, q)
                if result is None:
                    continue
                t, full_mod = result

                # Find a small prime = t mod full_mod and test solvability
                solved = False
                for p in primerange(max(t, 2), max(t, 2) + full_mod * 200):
                    if p % full_mod == t:
                        sol = _solve_quick(p)
                        if sol is not None:
                            a, b, c = sol
                            if 4 * a * b * c == p * (b * c + a * c + a * b):
                                solved = True
                        break
                if solved:
                    solvable_s.add(s)
            solvable_table[(r, q)] = solvable_s

    return solvable_table


def is_extended_sieve_solvable(p, solvable_table):
    """
    Check if a hard prime (in hard residues mod 840) can be resolved
    by the extended sieve (additional modular families).
    """
    r = p % 840
    if r not in HARD_RESIDUES_840:
        return False  # not a hard prime

    for q in EXTRA_MODULI:
        s = p % q
        if s in solvable_table.get((r, q), set()):
            return True
    return False


def main():
    print("=" * 60)
    print("Item 021: Method breakdown statistics")
    print("=" * 60)

    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    LIMIT = 10**8

    # Step 1: Build extended sieve table
    print("\nStep 1: Building extended sieve lookup table...")
    t0 = time.time()
    solvable_table = build_extended_sieve_table()
    print(f"  Built in {time.time()-t0:.1f}s")

    # Report coverage
    total_classes = 0
    solvable_classes = 0
    for (r, q), ss in solvable_table.items():
        total_classes += EXTRA_MODULI[EXTRA_MODULI.index(q)] if q in EXTRA_MODULI else q
        solvable_classes += len(ss)
    print(f"  Extended sieve covers {solvable_classes} additional residue classes")

    # Step 2: Sieve primes and classify
    print(f"\nStep 2: Sieving primes up to {LIMIT:.0e} and classifying...")
    t0 = time.time()
    small_primes_list = precompute_small_primes(LIMIT)
    print(f"  Precomputed {len(small_primes_list)} small primes in {time.time()-t0:.1f}s")

    mordell_count = 0
    extended_sieve_count = 0
    bruteforce_count = 0
    total_primes = 0

    # Track per-decade breakdown
    decade_data = {}

    segment_size = 10_000_000
    last_report = time.time()

    for seg_lo in range(2, LIMIT + 1, segment_size):
        seg_hi = min(seg_lo + segment_size - 1, LIMIT)
        primes = sieve_segment(seg_lo, seg_hi, small_primes_list)

        for p in primes:
            total_primes += 1

            # Determine decade bucket
            if p >= 10:
                decade = int(math.log10(p))
            else:
                decade = 0
            decade_key = f"10^{decade}"
            if decade_key not in decade_data:
                decade_data[decade_key] = {
                    "mordell": 0, "extended_sieve": 0, "bruteforce": 0, "total": 0
                }
            decade_data[decade_key]["total"] += 1

            # Classification
            if can_solve_mordell(p):
                mordell_count += 1
                decade_data[decade_key]["mordell"] += 1
            else:
                # p is in the 6 hard residues mod 840
                if is_extended_sieve_solvable(p, solvable_table):
                    extended_sieve_count += 1
                    decade_data[decade_key]["extended_sieve"] += 1
                else:
                    bruteforce_count += 1
                    decade_data[decade_key]["bruteforce"] += 1

        now = time.time()
        if now - last_report > 10:
            elapsed = now - t0
            rate = total_primes / elapsed if elapsed > 0 else 0
            pct = (seg_hi - 2) / (LIMIT - 2) * 100
            print(f"  [{pct:.1f}%] {total_primes:,} primes, "
                  f"Mordell: {mordell_count:,}, ExtSieve: {extended_sieve_count:,}, "
                  f"BF: {bruteforce_count:,}, {rate:,.0f}/sec")
            last_report = now

    total_time = time.time() - t0

    print(f"\n  Completed in {total_time:.1f}s")
    print(f"  Total primes: {total_primes:,}")
    print(f"  Mordell identity: {mordell_count:,} "
          f"({100*mordell_count/total_primes:.2f}%)")
    print(f"  Extended sieve: {extended_sieve_count:,} "
          f"({100*extended_sieve_count/total_primes:.2f}%)")
    print(f"  Brute-force/divisor: {bruteforce_count:,} "
          f"({100*bruteforce_count/total_primes:.2f}%)")

    # Step 3: Save results
    output = {
        "description": "Method breakdown for Erdos-Straus verification pipeline",
        "item": "021",
        "limit": LIMIT,
        "total_primes": total_primes,
        "methods": {
            "mordell_identity": {
                "count": mordell_count,
                "percentage": round(100 * mordell_count / total_primes, 4)
                    if total_primes > 0 else 0,
                "description": "Mordell algebraic identities (O(1) closed-form for p mod 840 not in hard set)"
            },
            "extended_sieve": {
                "count": extended_sieve_count,
                "percentage": round(100 * extended_sieve_count / total_primes, 4)
                    if total_primes > 0 else 0,
                "description": "Extended modular sieve using additional moduli {11,13,17,19,23}"
            },
            "bruteforce_divisor": {
                "count": bruteforce_count,
                "percentage": round(100 * bruteforce_count / total_primes, 4)
                    if total_primes > 0 else 0,
                "description": "Brute-force divisor search (parametric x with divisor enumeration)"
            }
        },
        "hard_residues_mod_840": sorted(HARD_RESIDUES_840),
        "extra_moduli": EXTRA_MODULI,
        "decade_breakdown": decade_data,
        "runtime_seconds": round(total_time, 2),
    }

    outfile = "results/method_breakdown.json"
    with open(outfile, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {outfile}")

    # Step 4: Plot - Stacked bar chart by decade
    print("\nGenerating plot...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Panel 1: Stacked bar chart by decade
    ax1 = axes[0]
    decades_sorted = sorted(decade_data.keys(), key=lambda k: int(k.split('^')[1]))

    mordell_vals = [decade_data[d]["mordell"] for d in decades_sorted]
    extsieve_vals = [decade_data[d]["extended_sieve"] for d in decades_sorted]
    bf_vals = [decade_data[d]["bruteforce"] for d in decades_sorted]

    x_pos = np.arange(len(decades_sorted))
    width = 0.6

    p1 = ax1.bar(x_pos, mordell_vals, width, label='Mordell identity',
                 color='#4CAF50', edgecolor='black', linewidth=0.5)
    p2 = ax1.bar(x_pos, extsieve_vals, width, bottom=mordell_vals,
                 label='Extended sieve', color='#2196F3', edgecolor='black', linewidth=0.5)
    bottoms = [m + e for m, e in zip(mordell_vals, extsieve_vals)]
    p3 = ax1.bar(x_pos, bf_vals, width, bottom=bottoms,
                 label='Brute-force/divisor', color='#FF5722', edgecolor='black', linewidth=0.5)

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(decades_sorted, fontsize=9, rotation=15)
    ax1.set_xlabel('Prime range (decade)', fontsize=12)
    ax1.set_ylabel('Number of primes', fontsize=12)
    ax1.set_title(f'Method breakdown by decade\n(primes up to {LIMIT:.0e})', fontsize=13)
    ax1.legend(fontsize=10, loc='upper left')
    ax1.grid(axis='y', alpha=0.3)

    # Panel 2: Stacked bar chart by decade (percentage)
    ax2 = axes[1]

    totals = [decade_data[d]["total"] for d in decades_sorted]
    mordell_pct = [100 * m / t if t > 0 else 0 for m, t in zip(mordell_vals, totals)]
    extsieve_pct = [100 * e / t if t > 0 else 0 for e, t in zip(extsieve_vals, totals)]
    bf_pct = [100 * b / t if t > 0 else 0 for b, t in zip(bf_vals, totals)]

    p1 = ax2.bar(x_pos, mordell_pct, width, label='Mordell identity',
                 color='#4CAF50', edgecolor='black', linewidth=0.5)
    p2 = ax2.bar(x_pos, extsieve_pct, width, bottom=mordell_pct,
                 label='Extended sieve', color='#2196F3', edgecolor='black', linewidth=0.5)
    bottoms_pct = [m + e for m, e in zip(mordell_pct, extsieve_pct)]
    p3 = ax2.bar(x_pos, bf_pct, width, bottom=bottoms_pct,
                 label='Brute-force/divisor', color='#FF5722', edgecolor='black', linewidth=0.5)

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(decades_sorted, fontsize=9, rotation=15)
    ax2.set_xlabel('Prime range (decade)', fontsize=12)
    ax2.set_ylabel('Percentage (%)', fontsize=12)
    ax2.set_title(f'Method breakdown by decade (percentage)\n(primes up to {LIMIT:.0e})', fontsize=13)
    ax2.legend(fontsize=10, loc='center right')
    ax2.set_ylim(0, 105)
    ax2.grid(axis='y', alpha=0.3)

    # Add percentage labels on the bars for the brute-force portion (smallest)
    for i, (bfp, bp) in enumerate(zip(bf_pct, bottoms_pct)):
        if bfp > 0.5:
            ax2.text(i, bp + bfp / 2, f'{bfp:.1f}%', ha='center', va='center',
                     fontsize=8, fontweight='bold', color='white')

    plt.tight_layout()
    figfile = "figures/method_breakdown.png"
    plt.savefig(figfile, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Plot saved to {figfile}")

    # Summary overall pie chart as supplementary figure
    fig2, ax = plt.subplots(figsize=(8, 8))
    sizes = [mordell_count, extended_sieve_count, bruteforce_count]
    labels = [
        f'Mordell identity\n{mordell_count:,}\n({100*mordell_count/total_primes:.1f}%)',
        f'Extended sieve\n{extended_sieve_count:,}\n({100*extended_sieve_count/total_primes:.1f}%)',
        f'Brute-force\n{bruteforce_count:,}\n({100*bruteforce_count/total_primes:.1f}%)',
    ]
    colors = ['#4CAF50', '#2196F3', '#FF5722']
    explode = (0, 0, 0.05)
    wedges, texts = ax.pie(sizes, labels=labels, colors=colors,
                           explode=explode, startangle=90,
                           textprops={'fontsize': 11})
    ax.set_title(f'Overall method breakdown\n({total_primes:,} primes up to {LIMIT:.0e})',
                 fontsize=14)
    fig2.savefig("figures/method_breakdown_pie.png", dpi=150, bbox_inches='tight')
    plt.close(fig2)
    print("Supplementary pie chart saved to figures/method_breakdown_pie.png")

    print("\n" + "=" * 60)
    print("Item 021 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
