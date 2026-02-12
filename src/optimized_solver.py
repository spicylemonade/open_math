"""
Optimized brute-force solver for the Erdős–Straus conjecture.

Uses parametric search with divisor enumeration:
1. Closed-form for p ≡ 3 mod 4, even n (O(1))
2. For p ≡ 1 mod 4: iterate x near ceil(p/4), then enumerate divisors of (px)^2
   to find valid y,z without a linear inner loop.

The key identity: for 4/n = 1/x + 1/y + 1/z,
  let A = 4x - n. Then 1/y + 1/z = A/(nx).
  So (Ay - nx)(Az - nx) = (nx)^2.
  Enumerate divisors d of (nx)^2 with d ≡ nx mod A, d <= nx.
  Then y = (d + nx)/A, z = ((nx)^2/d + nx)/A.
"""

import math
from functools import lru_cache


def verify(n, a, b, c):
    """Verify that 4/n = 1/a + 1/b + 1/c using exact integer arithmetic."""
    return 4 * a * b * c == n * (b * c + a * c + a * b)


def _divisors(n):
    """Return sorted list of all divisors of n."""
    if n <= 0:
        return []
    small = []
    large = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i != n // i:
                large.append(n // i)
        i += 1
    return small + large[::-1]


def _divisors_of_p2x2(p, x):
    """
    Efficiently enumerate divisors of (p*x)^2 = p^2 * x^2.
    Since p is prime, p^2 has divisors {1, p, p^2}.
    x^2 divisors come from factoring x.

    Returns sorted list of divisors.
    """
    # Factor x
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

    # x^2 factors: double all exponents
    x2_factors = {k: 2 * v for k, v in x_factors.items()}

    # p^2 * x^2 factors: add p^2
    all_factors = dict(x2_factors)
    all_factors[p] = all_factors.get(p, 0) + 2

    # Generate all divisors from prime factorization
    divs = [1]
    for prime, exp in all_factors.items():
        new_divs = []
        pe = 1
        for _ in range(exp + 1):
            for d in divs:
                new_divs.append(d * pe)
            pe *= prime
        divs = new_divs

    return divs


def solve(n):
    """Find (x, y, z) with x <= y <= z such that 4/n = 1/x + 1/y + 1/z."""
    return solve_fast(n)


def solve_fast(n):
    """Fast solver combining closed-form identities with divisor-based search."""
    if n <= 1:
        return None
    if n == 2:
        return (1, 2, 2)
    if n == 3:
        return (1, 4, 12)
    if n == 4:
        return (2, 4, 4)
    if n == 5:
        return (2, 4, 20)

    # Even n: always easy
    if n % 2 == 0:
        m = n // 2
        return (m, 2 * m, 2 * m)

    # p ≡ 3 mod 4: immediate O(1) closed-form
    if n % 4 == 3:
        q = (n + 1) // 4
        m = n * q
        if m % 2 == 0:
            return tuple(sorted([q, 2 * m, 2 * m]))
        else:
            return tuple(sorted([q, m + 1, m * (m + 1)]))

    # p ≡ 1 mod 4: the hard case
    # Strategy: iterate x from ceil(n/4), use divisor enumeration
    x_min = (n + 3) // 4  # ceil(n/4)
    x_max = 3 * n // 4 + 1

    for x in range(x_min, x_max + 1):
        A = 4 * x - n  # numerator of remainder
        if A <= 0:
            continue
        nx = n * x  # denominator of remainder

        # (A*y - nx)(A*z - nx) = nx^2
        # Let D = nx^2. Enumerate divisors d1 of D with d1 <= nx (so y >= x? not exactly)
        # d1 = A*y - nx, d2 = A*z - nx, d1*d2 = nx^2
        # y = (d1 + nx)/A, z = (d2 + nx)/A
        # Need d1 + nx ≡ 0 mod A and d2 + nx ≡ 0 mod A
        # Since d1*d2 = nx^2 and d2 = nx^2/d1, if d1 ≡ -nx mod A then
        # d2 = nx^2/d1. Check d2 + nx ≡ 0 mod A too.

        D = nx * nx
        # Get all divisors of D
        divs = _divisors_of_p2x2(n, x)

        target_mod = (-nx) % A  # d1 ≡ target_mod (mod A)

        for d1 in divs:
            if d1 > nx:
                continue  # ensures y >= x (roughly)
            if d1 % A != target_mod:
                continue
            d2 = D // d1
            # Check d2
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
            if verify(n, x, y, z):
                return tuple(sorted([x, y, z]))

    return None


if __name__ == "__main__":
    import time
    import sys
    sys.path.insert(0, '.')
    from sympy import primerange

    # Correctness test on primes up to 10^4
    print("Correctness test on primes up to 10^4...")
    failures = []
    count = 0
    for p in primerange(2, 10001):
        sol = solve_fast(p)
        if sol is None:
            failures.append(('none', p))
        elif not verify(p, *sol):
            failures.append(('bad', p, sol))
        count += 1
    if failures:
        print(f"FAILURES ({len(failures)}): {failures[:20]}")
    else:
        print(f"All {count} primes passed!")

    # Speed test on hard primes around 10^6
    print("\nCollecting hard primes in [10^6, 2*10^6]...")
    hard_residues = {1, 121, 169, 289, 361, 529}
    hard_primes = [p for p in primerange(10**6, 2 * 10**6) if p % 840 in hard_residues]
    print(f"  Found {len(hard_primes)} hard primes")

    sample = hard_primes[:200]
    start = time.time()
    fail = 0
    for p in sample:
        sol = solve_fast(p)
        if sol is None or not verify(p, *sol):
            fail += 1
    elapsed_opt = time.time() - start
    print(f"  Optimized: {len(sample)} hard primes in {elapsed_opt:.3f}s = {len(sample)/elapsed_opt:.1f} primes/sec, failures={fail}")

    # Compare with naive on same hard primes
    from src.naive_solver import solve as naive_solve
    sample_small = hard_primes[:5]

    start = time.time()
    for p in sample_small:
        naive_solve(p)
    elapsed_naive = time.time() - start

    start = time.time()
    for p in sample_small:
        solve_fast(p)
    elapsed_opt2 = time.time() - start

    speedup = elapsed_naive / elapsed_opt2 if elapsed_opt2 > 0 else float('inf')
    print(f"\nComparison on {len(sample_small)} hard primes near 10^6:")
    print(f"  Naive:     {elapsed_naive:.3f}s ({len(sample_small)/elapsed_naive:.1f} primes/sec)")
    print(f"  Optimized: {elapsed_opt2:.3f}s ({len(sample_small)/elapsed_opt2:.1f} primes/sec)")
    print(f"  Speedup: {speedup:.1f}x")

    # Full pipeline test on all primes
    print("\nFull pipeline: all primes in [10^6, 10^6+10^5]...")
    all_primes = list(primerange(10**6, 10**6 + 100000))
    start = time.time()
    fail = 0
    for p in all_primes:
        sol = solve_fast(p)
        if sol is None or not verify(p, *sol):
            fail += 1
    elapsed = time.time() - start
    print(f"  {len(all_primes)} primes in {elapsed:.3f}s = {len(all_primes)/elapsed:.1f} primes/sec, failures={fail}")
