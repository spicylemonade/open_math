"""
Salez-style modular sieve filter for the Erdős–Straus conjecture.

Precomputes a mod-840 residue filter based on Mordell's identities and
Salez's additional modular equations to identify primes that require
brute-force checking.

References:
- Mordell (1967): Basic identities for mod 3, 4, 5, 7, 8
- Salez (2014, arXiv:1406.6307): 7 modular equations
"""

from sympy import primerange
import math


# The 6 hard residues mod 840 that Mordell's identities cannot handle
HARD_RESIDUES_840 = frozenset({1, 121, 169, 289, 361, 529})

# Total coprime residues mod 840
# 840 = 2^3 * 3 * 5 * 7, phi(840) = 840 * (1-1/2)(1-1/3)(1-1/5)(1-1/7) = 192
PHI_840 = 192


def _build_solvable_residues_mod(m, small_primes_limit=1000):
    """
    Build the set of residues r mod m for which we can find a closed-form
    solution to 4/p = 1/a + 1/b + 1/c via a modular identity.

    Strategy: for each residue class r mod m with gcd(r, m) = 1,
    check whether a parametric solution exists by testing on the
    smallest prime p ≡ r (mod m).
    """
    from src.mordell_solver import solve_mordell, verify
    solvable = set()
    for r in range(m):
        if math.gcd(r, m) != 1:
            continue
        # Find a small prime ≡ r mod m
        for p in primerange(max(r, 2), small_primes_limit * m):
            if p % m == r:
                sol = solve_mordell(p)
                if sol and verify(p, *sol):
                    solvable.add(r)
                break
    return solvable


def build_sieve_mod840():
    """
    Build the set of residues mod 840 that require brute-force checking.

    Returns the set of 'hard' residues — primes with p % 840 in this set
    need individual checking beyond Mordell's identities.
    """
    # Mordell's identities solve all primes EXCEPT those congruent to
    # {1, 121, 169, 289, 361, 529} mod 840
    return HARD_RESIDUES_840


def build_extended_sieve():
    """
    Build extended sieve using Salez's 7 modular equations.

    In addition to mod-840 filtering, we apply additional modular conditions
    with larger moduli (products involving 11, 13, 17, 19, 23) to further
    reduce the set of primes requiring checking.

    Returns a function: is_hard(p) -> bool
    """
    hard_840 = HARD_RESIDUES_840

    # Salez's additional equations use larger moduli. We approximate them
    # by checking additional modular conditions that can provide solutions.
    # These are: mod 11, 13, 17, 19, 23 conditions that extend Mordell's set.

    # For primes in hard_840 classes, check additional conditions:
    # - If p ≡ certain values mod 11, 13, etc., solutions may exist
    #   via Salez's extended identities.

    # Precompute which (r mod 840, s mod q) pairs are solvable for q in {11, 13, 17, 19, 23}
    # For efficiency, we just check small primes in each double-residue class.

    from src.mordell_solver import solve_mordell, verify

    extra_moduli = [11, 13, 17, 19, 23]
    # For each hard residue r mod 840 and each extra modulus q,
    # find which residues s mod q allow a solution
    solvable_extra = {}  # (r, q, s) -> True if solvable

    for r in hard_840:
        for q in extra_moduli:
            full_mod = 840 * q
            for s in range(q):
                # Find residue mod full_mod that is ≡ r mod 840 and ≡ s mod q
                # Using CRT: find t such that t ≡ r (mod 840) and t ≡ s (mod q)
                # Since gcd(840, q) = 1 for q in {11,13,17,19,23}:
                for t in range(full_mod):
                    if t % 840 == r and t % q == s:
                        break
                # Find a small prime ≡ t mod full_mod
                found = False
                for p in primerange(max(t, 2), max(t, 2) + full_mod * 100):
                    if p % full_mod == t:
                        sol = solve_mordell(p)
                        if sol and verify(p, *sol):
                            solvable_extra[(r, q, s)] = True
                            found = True
                        break
                if not found:
                    solvable_extra[(r, q, s)] = False

    def is_hard(p):
        """Return True if prime p requires brute-force checking."""
        r = p % 840
        if r not in hard_840:
            return False
        # Check extended conditions
        for q in extra_moduli:
            s = p % q
            if solvable_extra.get((r, q, s), False):
                return False
        return True

    return is_hard


def primes_requiring_bruteforce(lo, hi, use_extended=False):
    """
    Return list of primes in [lo, hi] that require brute-force checking.

    Args:
        lo: lower bound (inclusive)
        hi: upper bound (inclusive)
        use_extended: if True, use extended Salez sieve (slower to initialize)

    Returns:
        list of primes requiring brute-force
    """
    if use_extended:
        is_hard = build_extended_sieve()
        return [p for p in primerange(lo, hi + 1) if is_hard(p)]
    else:
        hard = HARD_RESIDUES_840
        return [p for p in primerange(lo, hi + 1) if p % 840 in hard]


def compute_sieve_statistics(limit):
    """Compute statistics about sieve effectiveness up to limit."""
    hard = HARD_RESIDUES_840
    total_primes = 0
    hard_primes = 0

    for p in primerange(2, limit + 1):
        total_primes += 1
        if p % 840 in hard:
            hard_primes += 1

    surviving_fraction = hard_primes / total_primes if total_primes > 0 else 0
    return {
        "limit": limit,
        "total_primes": total_primes,
        "hard_primes_mod840": hard_primes,
        "surviving_fraction": surviving_fraction,
        "eliminated_fraction": 1 - surviving_fraction,
    }


if __name__ == "__main__":
    import time
    import json

    # Test basic sieve statistics
    for exp in [4, 5, 6, 7]:
        limit = 10 ** exp
        start = time.time()
        stats = compute_sieve_statistics(limit)
        elapsed = time.time() - start
        print(f"Limit 10^{exp}: {stats['total_primes']} primes, "
              f"{stats['hard_primes_mod840']} hard ({stats['surviving_fraction']:.4f}), "
              f"time: {elapsed:.2f}s")

    # Test primes_requiring_bruteforce
    print("\nBrute-force primes in [2, 10000]:")
    bf_primes = primes_requiring_bruteforce(2, 10000)
    print(f"  Count: {len(bf_primes)}")
    print(f"  First 10: {bf_primes[:10]}")

    # Verify against known: density should be ~6/192 ≈ 3.1%
    stats = compute_sieve_statistics(10**7)
    print(f"\nSieve verification (up to 10^7):")
    print(f"  Surviving fraction: {stats['surviving_fraction']:.4f}")
    print(f"  Expected (6/192): {6/192:.4f}")
