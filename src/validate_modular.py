"""Validate modular obstruction analysis against known UPNs and random integers.

Empirically tests the modular sieve to verify known UPNs pass and estimate
what fraction of random integers survive all obstructions.
"""

import json
import random
import time

from src.unitary import KNOWN_UPNS, sigma_star
from src.modular_obstructions import _analyze_single_modulus
from sympy import primerange


def validate_known_upns(max_modulus=100):
    """Verify all known UPNs pass all modular obstruction tests.

    Args:
        max_modulus: Check all primes up to this.

    Returns:
        Dict with verification results.
    """
    primes = list(primerange(3, max_modulus + 1))
    results = {}

    for n in KNOWN_UPNS:
        n_results = {}
        all_pass = True
        for q in primes:
            allowed, _ = _analyze_single_modulus(q)
            r = n % q
            passes = r in allowed
            if not passes:
                all_pass = False
            n_results[str(q)] = {"residue": r, "passes": passes}
        results[str(n)] = {"all_pass": all_pass, "details": n_results}

    return results


def test_random_integers(num_samples=100000, max_modulus=100, seed=42):
    """Test random integers against modular obstructions.

    Args:
        num_samples: Number of random integers to test.
        max_modulus: Check all primes up to this.
        seed: Random seed for reproducibility.

    Returns:
        Dict with test results.
    """
    random.seed(seed)
    primes = list(primerange(3, max_modulus + 1))

    # Pre-compute allowed sets for each prime
    allowed_sets = {}
    for q in primes:
        allowed, _ = _analyze_single_modulus(q)
        allowed_sets[q] = allowed

    pass_count = 0
    total_tested = 0

    for _ in range(num_samples):
        # Generate random even integer (since all UPNs are even)
        n = random.randint(1, 10**12) * 2
        total_tested += 1

        passes_all = True
        for q in primes:
            r = n % q
            if r not in allowed_sets[q]:
                passes_all = False
                break

        if passes_all:
            pass_count += 1

    return {
        "total_tested": total_tested,
        "pass_count": pass_count,
        "pass_rate": pass_count / total_tested,
        "max_modulus": max_modulus,
        "num_primes_checked": len(primes),
    }


def compute_sieve_density(max_modulus=100):
    """Compute theoretical sieve density from modular obstructions.

    Args:
        max_modulus: Check all primes up to this.

    Returns:
        Dict with sieve density results.
    """
    primes = list(primerange(3, max_modulus + 1))
    cumulative_density = 1.0
    densities_by_modulus = []

    for q in primes:
        allowed, excluded = _analyze_single_modulus(q)
        density = len(allowed) / q
        cumulative_density *= density
        densities_by_modulus.append({
            "modulus": q,
            "density": density,
            "cumulative_density": cumulative_density,
            "num_allowed": len(allowed),
            "num_excluded": len(excluded),
        })

    return {
        "final_sieve_density": cumulative_density,
        "by_modulus": densities_by_modulus,
    }


def main():
    """Run all validation tests."""
    print("=== Modular Obstruction Validation ===\n")

    # 1. Verify known UPNs
    print("1. Verifying known UPNs (primes up to 100)...")
    upn_results = validate_known_upns(max_modulus=100)
    for n_str, data in upn_results.items():
        status = "PASS" if data["all_pass"] else "FAIL"
        print(f"   {n_str}: {status}")

    # 2. Test random integers
    print("\n2. Testing 10^6 random even integers...")
    start = time.time()
    random_results = test_random_integers(num_samples=1000000, max_modulus=100, seed=42)
    elapsed = time.time() - start
    print(f"   Pass rate: {random_results['pass_rate']:.6f} ({random_results['pass_count']}/{random_results['total_tested']})")
    print(f"   Time: {elapsed:.1f}s")

    # 3. Compute sieve density
    print("\n3. Computing sieve density...")
    sieve = compute_sieve_density(max_modulus=100)
    print(f"   Theoretical sieve density: {sieve['final_sieve_density']:.6f}")

    # 4. Compare
    print("\n4. Comparison:")
    print(f"   Theoretical sieve density: {sieve['final_sieve_density']:.6f}")
    print(f"   Empirical pass rate:       {random_results['pass_rate']:.6f}")
    print(f"   Density of actual UPNs in [1, 10^6]: 4/1000000 = {4/1000000:.6f}")

    # Save results
    all_results = {
        "known_UPN_verification": upn_results,
        "random_pass_rate": random_results['pass_rate'],
        "sieve_density": sieve['final_sieve_density'],
        "random_test_details": random_results,
        "sieve_details": sieve,
    }

    with open("results/modular_validation.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\nResults saved to results/modular_validation.json")


if __name__ == "__main__":
    main()
