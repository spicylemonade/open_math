"""Modular arithmetic obstruction analysis for unitary perfect numbers.

Analyzes which residue classes mod q can contain a UPN, using the
constraint sigma*(n) = 2n mod q and the multiplicativity of sigma*.
"""

import json
from math import gcd
from itertools import product as iter_product
from sympy import primerange, factorint


def analyze_modular_obstructions(moduli=None, max_prime_power_exp=10):
    """For each modulus q, determine which residue classes mod q can contain a UPN.

    A UPN n satisfies sigma*(n) = 2n. Since sigma*(n) = prod(1 + p^a) for p^a || n,
    and n = prod(p^a), we need prod(1 + p^a) = 2 * prod(p^a) mod q.

    For each q, we enumerate all possible (n mod q, sigma*(n) mod q) pairs
    and check which n mod q values are consistent with sigma*(n) = 2n mod q.

    Args:
        moduli: List of moduli to check. Default: standard set.
        max_prime_power_exp: Max exponent for prime powers.

    Returns:
        Dict mapping each modulus to analysis results.
    """
    if moduli is None:
        moduli = [3, 4, 5, 7, 8, 9, 11, 13, 16]

    results = {}
    for q in moduli:
        allowed, excluded = _analyze_single_modulus(q, max_prime_power_exp)
        results[q] = {
            "modulus": q,
            "allowed_residues": sorted(allowed),
            "excluded_residues": sorted(excluded),
            "num_allowed": len(allowed),
            "num_excluded": len(excluded),
            "density": len(allowed) / q,
        }

    return results


def _analyze_single_modulus(q, max_exp=10):
    """Determine allowed residue classes for UPNs mod q.

    We use a direct approach: for UPN n, sigma*(n) = 2n mod q.
    Since n is even (all UPNs are even), we consider n mod q and check
    if there exists a factorization consistent with sigma*(n) ≡ 2n (mod q).

    For a practical approach, we check: for each r in {0,...,q-1},
    can there exist a UPN n ≡ r (mod q)?

    We use the fact that a UPN must be even and check all possible
    combinations of prime power residues.
    """
    allowed = set()

    # Enumerate possible prime power contributions mod q
    # Each prime power p^a contributes (p^a mod q) to n and (1+p^a mod q) to sigma*
    # Since p^a mod q is periodic in p (for fixed a), we only need primes up to q + some margin
    contributions = set()
    for p in primerange(2, max(50, 3 * q)):
        for a in range(1, max_exp + 1):
            pa = pow(p, a, q)  # p^a mod q
            s_contrib = (1 + pow(p, a)) % q  # (1+p^a) mod q - need exact for small q
            contributions.add((pa % q, s_contrib))

    # Build the set of all achievable (n mod q, sigma* mod q) pairs
    # by taking products of any number of contributions.
    # This is the multiplicative closure starting from (1, 1).
    current_pairs = {(1, 1)}

    for _ in range(20):  # iterate until saturated
        new_pairs = set(current_pairs)  # include existing
        for (cn, cs) in current_pairs:
            for (dn, ds) in contributions:
                new_n = (cn * dn) % q
                new_s = (cs * ds) % q
                new_pairs.add((new_n, new_s))
        if new_pairs == current_pairs:
            break
        current_pairs = new_pairs

    # Check which residues satisfy sigma* = 2n mod q
    for (n_mod, s_mod) in current_pairs:
        if s_mod == (2 * n_mod) % q:
            allowed.add(n_mod)

    excluded = set(range(q)) - allowed
    return allowed, excluded


def combined_sieve_density(max_modulus=100, max_prime_power_exp=8):
    """Compute the fraction of integers surviving all modular obstructions.

    For each prime q <= max_modulus, compute the fraction of residue classes
    that can contain a UPN, then combine (approximately) via inclusion-exclusion.

    Args:
        max_modulus: Check all primes up to this.
        max_prime_power_exp: Max exponent for prime powers.

    Returns:
        Dict with individual and combined densities.
    """
    primes = list(primerange(3, max_modulus + 1))
    individual_results = {}
    combined_density = 1.0

    for q in primes:
        allowed, excluded = _analyze_single_modulus(q, max_prime_power_exp)
        density = len(allowed) / q
        individual_results[q] = {
            "allowed": len(allowed),
            "total": q,
            "density": density,
            "excluded_residues": sorted(excluded),
        }
        combined_density *= density

    return {
        "individual": individual_results,
        "combined_density": combined_density,
        "num_primes_checked": len(primes),
        "max_modulus": max_modulus,
    }


def verify_known_upns(moduli=None):
    """Verify that all known UPNs pass modular obstruction tests.

    Args:
        moduli: List of moduli to check.

    Returns:
        Dict with verification results.
    """
    from src.unitary import KNOWN_UPNS

    if moduli is None:
        moduli = [3, 4, 5, 7, 8, 9, 11, 13, 16]

    results = {}
    for n in KNOWN_UPNS:
        n_results = {}
        for q in moduli:
            allowed, _ = _analyze_single_modulus(q)
            r = n % q
            passes = r in allowed
            n_results[q] = {"residue": r, "passes": passes}
        results[n] = n_results

    return results


def main():
    """Run modular obstruction analysis."""
    print("=== Modular Obstruction Analysis ===\n")

    # 1. Analyze standard moduli
    print("1. Analyzing obstructions for standard moduli...")
    obstructions = analyze_modular_obstructions()
    for q, data in obstructions.items():
        print(f"  mod {q:>3}: {data['num_allowed']:>3}/{q} allowed "
              f"(density={data['density']:.3f}), "
              f"excluded={data['excluded_residues']}")

    # 2. Verify known UPNs
    print("\n2. Verifying known UPNs pass all obstructions...")
    verification = verify_known_upns()
    for n, v in verification.items():
        all_pass = all(d['passes'] for d in v.values())
        print(f"  n={n}: {'ALL PASS' if all_pass else 'FAIL'}")

    # 3. Combined sieve density
    print("\n3. Computing combined sieve density (primes up to 50)...")
    sieve = combined_sieve_density(max_modulus=50)
    print(f"  Combined density: {sieve['combined_density']:.6f}")
    print(f"  Primes checked: {sieve['num_primes_checked']}")

    # Save all results
    all_results = {
        "obstructions": {str(k): v for k, v in obstructions.items()},
        "known_upn_verification": {str(k): v for k, v in verification.items()},
        "sieve_density": sieve,
    }

    # Convert non-serializable types
    def make_serializable(obj):
        if isinstance(obj, set):
            return sorted(obj)
        if isinstance(obj, dict):
            return {str(k): make_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [make_serializable(v) for v in obj]
        return obj

    with open("results/modular_analysis_results.json", "w") as f:
        json.dump(make_serializable(all_results), f, indent=2)

    print("\nResults saved to results/modular_analysis_results.json")


if __name__ == "__main__":
    main()
