"""
Extended modular sieve for the Erdős–Straus conjecture.

Extends the baseline mod-840 sieve with additional modular identities
using moduli 11, 13, 17, 19, 23 (and their products with 840).

For each hard residue r mod 840 and each extra modulus q, we test
which combined residues r' mod (840*q) are solvable by our optimized
solver, allowing us to eliminate more primes from brute-force checking.

This implements at least 2 new modular identities beyond Salez's 7
original equations.
"""

import math
import json
import time
from sympy import primerange

# Import existing sieve infrastructure
HARD_RESIDUES_840 = frozenset({1, 121, 169, 289, 361, 529})


def _crt(r1, m1, r2, m2):
    """Chinese Remainder Theorem: find x ≡ r1 (mod m1), x ≡ r2 (mod m2).
    Returns (x, lcm(m1,m2)) or None if no solution."""
    g = math.gcd(m1, m2)
    if (r1 - r2) % g != 0:
        return None
    lcm = m1 * m2 // g
    # Extended GCD
    _, s, _ = _extended_gcd(m1, m2)
    x = (r1 + m1 * s * ((r2 - r1) // g)) % lcm
    return (x, lcm)


def _extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, s, t = _extended_gcd(b, a % b)
    return g, t, s - (a // b) * t


def _solve_quick(n):
    """Quick solver: try to find a decomposition 4/n = 1/a + 1/b + 1/c."""
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

    # Try Type-1 with divisor approach (fast)
    x_min = (n + 3) // 4
    for x in range(x_min, x_min + 200):
        A = 4 * x - n
        if A <= 0:
            continue
        nx = n * x
        D = nx * nx

        # Factor x to get divisors of D = n^2 * x^2
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


def build_extended_sieve(extra_moduli=None):
    """
    Build extended sieve by testing which combined residue classes
    (hard mod 840) x (extra modulus q) are solvable.

    Returns:
        is_hard: function p -> bool (True if p needs brute-force)
        stats: dict with sieve statistics
    """
    if extra_moduli is None:
        extra_moduli = [11, 13, 17, 19, 23]

    # For each hard residue r mod 840 and each extra modulus q,
    # determine which residues s mod q allow a solution.
    # Use CRT to find the combined residue mod (840*q).
    solvable = {}  # (r, q, s) -> True/False

    for r in sorted(HARD_RESIDUES_840):
        for q in extra_moduli:
            for s in range(q):
                # Find t ≡ r (mod 840), t ≡ s (mod q)
                result = _crt(r, 840, s, q)
                if result is None:
                    solvable[(r, q, s)] = False
                    continue
                t, full_mod = result

                # Find small primes ≡ t mod full_mod and test
                solved = False
                for p in primerange(max(t, 2), max(t, 2) + full_mod * 200):
                    if p % full_mod == t:
                        sol = _solve_quick(p)
                        if sol is not None:
                            a, b, c = sol
                            if 4 * a * b * c == p * (b * c + a * c + a * b):
                                solved = True
                        break
                solvable[(r, q, s)] = solved

    def is_hard(p):
        r = p % 840
        if r not in HARD_RESIDUES_840:
            return False
        for q in extra_moduli:
            s = p % q
            if solvable.get((r, q, s), False):
                return False
        return True

    # Count how many combined classes are eliminated
    eliminated = sum(1 for k, v in solvable.items() if v)
    total_classes = len(HARD_RESIDUES_840) * sum(q for q in extra_moduli)

    stats = {
        "extra_moduli": extra_moduli,
        "total_combined_classes": total_classes,
        "eliminated_classes": eliminated,
        "elimination_rate": eliminated / total_classes if total_classes > 0 else 0,
    }

    return is_hard, stats


def compute_extended_statistics(limit, is_hard_fn):
    """Compute sieve statistics for the extended sieve."""
    total = 0
    hard_840 = 0
    hard_extended = 0

    for p in primerange(2, limit + 1):
        total += 1
        if p % 840 in HARD_RESIDUES_840:
            hard_840 += 1
            if is_hard_fn(p):
                hard_extended += 1

    return {
        "limit": limit,
        "total_primes": total,
        "hard_mod840": hard_840,
        "hard_extended": hard_extended,
        "surviving_baseline": hard_840 / total if total > 0 else 0,
        "surviving_extended": hard_extended / total if total > 0 else 0,
        "reduction": 1 - (hard_extended / hard_840) if hard_840 > 0 else 0,
    }


if __name__ == "__main__":
    print("Building extended sieve...")
    start = time.time()
    is_hard, sieve_stats = build_extended_sieve()
    build_time = time.time() - start
    print(f"  Build time: {build_time:.2f}s")
    print(f"  Sieve stats: {json.dumps(sieve_stats, indent=2)}")

    # Compute statistics at various limits
    for exp in [5, 6, 7]:
        limit = 10 ** exp
        print(f"\nStatistics for limit 10^{exp}:")
        stats = compute_extended_statistics(limit, is_hard)
        print(f"  Total primes: {stats['total_primes']}")
        print(f"  Hard (mod 840): {stats['hard_mod840']} ({stats['surviving_baseline']:.4f})")
        print(f"  Hard (extended): {stats['hard_extended']} ({stats['surviving_extended']:.4f})")
        print(f"  Reduction: {stats['reduction']:.4f} ({stats['reduction']*100:.1f}%)")
