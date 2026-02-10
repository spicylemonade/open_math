"""Analysis of the product equation prod(1 + 1/p_i^{a_i}) = 2.

Studies the Diophantine constraint that characterizes unitary perfect numbers,
analyzing the solution space and the maximum achievable product.
"""

import json
import math
from fractions import Fraction
from sympy import primerange, nextprime


def max_product_first_k_primes(k):
    """Compute the maximal product prod_{i=1}^{k} (1 + 1/p_i) for the first k primes.

    This is the maximum achievable by choosing the k smallest primes each with
    exponent 1 (since higher exponents reduce the contribution).

    Args:
        k: Number of primes.

    Returns:
        Tuple of (exact Fraction, float approximation).
    """
    product = Fraction(1)
    p = 2
    for _ in range(k):
        product *= Fraction(1 + p, p)
        p = int(nextprime(p))
    return product, float(product)


def max_product_table(max_k=50):
    """Compute table of max products for k = 1..max_k.

    Args:
        max_k: Maximum number of primes.

    Returns:
        List of dicts with k, max_product, exceeds_2.
    """
    table = []
    product = Fraction(1)
    p = 2
    for k in range(1, max_k + 1):
        product *= Fraction(1 + p, p)
        exceeds_2 = product >= 2
        table.append({
            "k": k,
            "max_product_float": float(product),
            "exceeds_2": exceeds_2,
            "prime_used": p,
        })
        p = int(nextprime(p))
    return table


def find_threshold_k():
    """Find the smallest k such that prod_{i=1}^{k} (1 + 1/p_i) < 2.

    Since each factor (1 + 1/p) > 1, the product grows without bound
    (by Mertens' theorem, prod_{p<=x}(1+1/p) ~ 2*e^gamma * log(x) / pi).
    Wait - actually prod(1+1/p) = prod(p+1)/p. By Mertens' third theorem,
    prod_{p<=x}(1 - 1/p) ~ e^{-gamma}/log(x), so
    prod_{p<=x}(1 + 1/p) = prod_{p<=x}(1 - 1/p^2)/(1-1/p)
                          = prod(1-1/p^2) * prod 1/(1-1/p)
                          ~ (6/pi^2) * e^gamma * log(x)

    So the product grows like C * log(x) and NEVER stays below 2 permanently.
    This means: for ANY k, there exist k primes whose product exceeds 2.

    However, for a UPN, the primes must give EXACTLY 2, and they can use
    higher exponents (which reduce contributions). The key constraint is
    that the 2-component uses one of the factors.

    Returns:
        None (the product diverges), but computes when it first exceeds 2.
    """
    product = Fraction(1)
    p = 2
    for k in range(1, 100):
        product *= Fraction(1 + p, p)
        if product >= 2:
            return k, p
        p = int(nextprime(p))
    return None, None


def analyze_known_upn_products():
    """Analyze how the known UPN factorizations relate to the maximum product.

    Returns:
        List of analysis dicts for each known UPN.
    """
    from src.unitary import KNOWN_UPN_FACTORIZATIONS

    results = []
    for n, fact in KNOWN_UPN_FACTORIZATIONS.items():
        # Actual product (should be exactly 2)
        actual = Fraction(1)
        for p, a in fact.items():
            actual *= Fraction(1 + p**a, p**a)

        # Maximum product using same primes but all with exponent 1
        max_with_same_primes = Fraction(1)
        for p in fact.keys():
            max_with_same_primes *= Fraction(1 + p, p)

        # Ratio: how much of the maximum is used
        efficiency = float(actual) / float(max_with_same_primes)

        results.append({
            "n": n,
            "omega": len(fact),
            "actual_product": float(actual),
            "max_product_same_primes": float(max_with_same_primes),
            "efficiency": efficiency,
            "factorization": {str(p): a for p, a in fact.items()},
        })

    return results


def enumerate_solutions_small_k(max_k=8, max_prime=200, max_exponent=20):
    """Enumerate solutions to prod(1+1/p_i^{a_i}) = 2 for small k.

    For the equation to have a solution, we need a factorization
    n = p_1^{a_1} * ... * p_k^{a_k} (NOT including the power of 2 separately;
    here all p_i are considered including p=2).

    Args:
        max_k: Maximum number of distinct primes.
        max_prime: Maximum prime to consider.
        max_exponent: Maximum exponent.

    Returns:
        Dict mapping k to list of solutions.
    """
    primes = list(primerange(2, max_prime + 1))
    solutions_by_k = {}

    for k in range(1, max_k + 1):
        solutions = _enum_recursive(Fraction(2), k, primes, 0, max_exponent)
        solutions_by_k[k] = solutions
        print(f"  k={k}: {len(solutions)} solutions found")

    return solutions_by_k


def _enum_recursive(target, remaining, primes, min_idx, max_exp):
    """Recursively enumerate solutions."""
    if remaining == 0:
        if target == Fraction(1):
            return [[]]
        return []

    if target <= Fraction(1):
        return []

    if min_idx >= len(primes):
        return []

    # Pruning: max product from remaining smallest primes
    if min_idx + remaining > len(primes):
        return []

    max_prod = Fraction(1)
    for i in range(remaining):
        p = primes[min_idx + i]
        max_prod *= Fraction(1 + p, p)
    if max_prod < target:
        return []

    solutions = []

    for idx in range(min_idx, len(primes)):
        p = primes[idx]

        # Check feasibility with remaining-1 primes
        if remaining > 1 and idx + remaining <= len(primes):
            max_rest = Fraction(1)
            for i in range(remaining - 1):
                rp = primes[idx + 1 + i]
                max_rest *= Fraction(1 + rp, rp)
        elif remaining == 1:
            max_rest = Fraction(1)
        else:
            break

        if Fraction(1 + p, p) * max_rest < target:
            break

        for a in range(1, max_exp + 1):
            pa = p ** a
            contrib = Fraction(1 + pa, pa)

            if contrib * max_rest < target:
                break

            new_target = target / contrib

            sub_sols = _enum_recursive(new_target, remaining - 1, primes, idx + 1, max_exp)
            for sol in sub_sols:
                solutions.append([(p, a)] + sol)

    return solutions


def main():
    """Run product equation analysis."""
    import time

    print("=== Product Equation Analysis ===\n")

    # 1. Max product table
    print("1. Maximum product table (first k primes, exponent 1):")
    table = max_product_table(50)
    print(f"   {'k':>3} {'product':>12} {'exceeds 2?':>10} {'prime':>6}")
    for row in table:
        print(f"   {row['k']:>3} {row['max_product_float']:>12.6f} {'YES' if row['exceeds_2'] else 'no':>10} {row['prime_used']:>6}")

    # 2. Threshold
    k_thresh, p_thresh = find_threshold_k()
    print(f"\n2. Product first exceeds 2 at k={k_thresh} (using primes up to {p_thresh})")
    print(f"   Actually, the product diverges (Mertens), so it exceeds 2 early.")
    print("   Key insight: prod_{p<=x}(1+1/p) ~ (6/pi^2)*e^gamma*ln(x) -> infinity")
    print(f"   So there is NO k beyond which the max product drops below 2.")
    print("   HOWEVER, for UPNs, one factor must be (1+2^m)/2^m and the remaining")
    print("   odd factors must contribute exactly 2^{m+1}/(1+2^m).")

    # 3. Known UPN analysis
    print("\n3. Known UPN product analysis:")
    upn_analysis = analyze_known_upn_products()
    for a in upn_analysis:
        print(f"   n = {a['n']}: omega={a['omega']}, "
              f"max_product_same_primes={a['max_product_same_primes']:.6f}, "
              f"efficiency={a['efficiency']:.6f}")

    # 4. Enumerate solutions for small k
    print("\n4. Enumerating solutions to prod(1+1/p^a) = 2:")
    start = time.time()
    solutions = enumerate_solutions_small_k(max_k=6, max_prime=350, max_exponent=20)
    elapsed = time.time() - start

    all_results = {
        "max_product_table": table,
        "threshold_k": k_thresh,
        "known_upn_analysis": upn_analysis,
        "solutions_by_k": {str(k): [[(p, a) for p, a in sol] for sol in sols]
                           for k, sols in solutions.items()},
        "enumeration_time": round(elapsed, 3),
    }

    with open("results/product_equation_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved. Enumeration took {elapsed:.1f}s")


if __name__ == "__main__":
    main()
