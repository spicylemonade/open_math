"""
Naive brute-force solver for the Erdős–Straus conjecture.

Given n >= 2, finds positive integers (a, b, c) with a <= b <= c such that:
    4/n = 1/a + 1/b + 1/c

Equivalently (clearing denominators):
    4*a*b*c = n*(b*c + a*c + a*b)
"""

import math


def verify(n, a, b, c):
    """Verify that 4/n = 1/a + 1/b + 1/c using exact integer arithmetic."""
    return 4 * a * b * c == n * (b * c + a * c + a * b)


def solve(n):
    """
    Find (a, b, c) with a <= b <= c such that 4/n = 1/a + 1/b + 1/c.

    Returns (a, b, c) or None if no solution found.

    For 4/n = 1/a + 1/b + 1/c with a <= b <= c:
        1/a >= 4/(3n)  =>  a <= 3n/4
        1/a <= 4/n     =>  a >= n/4

    For each a, remaining = 4/n - 1/a = (4a - n)/(na)
    Then 1/b + 1/c = (4a - n)/(na) with b <= c
        1/b >= (4a-n)/(2na)  =>  b <= 2na/(4a-n)
        b >= a (ordering constraint)
        Also b >= na/(4a-n) since 1/b <= (4a-n)/(na)
    """
    a_min = max(1, math.ceil(n / 4))
    a_max = 3 * n // 4 + 1

    for a in range(a_min, a_max + 1):
        num = 4 * a - n  # numerator of remaining fraction
        if num <= 0:
            continue
        den = n * a  # denominator of remaining fraction

        # 1/b + 1/c = num/den with b <= c
        # b >= max(a, ceil(den/num)) and b <= 2*den//num
        b_min = max(a, -(-den // num))  # ceil(den/num)
        b_max = 2 * den // num

        for b in range(b_min, b_max + 1):
            c_num = den * b
            c_den = num * b - den
            if c_den <= 0:
                continue
            if c_num % c_den == 0:
                c = c_num // c_den
                if c >= b:
                    return (a, b, c)

    return None


def solve_all_primes(limit):
    """Solve for all primes up to limit. Returns dict {p: (a,b,c)}."""
    from sympy import primerange
    results = {}
    for p in primerange(2, limit + 1):
        sol = solve(p)
        if sol is not None:
            results[p] = sol
        else:
            results[p] = None
    return results


if __name__ == "__main__":
    import time
    from sympy import primerange

    limit = 10**4
    print(f"Testing naive solver on all primes up to {limit}...")
    start = time.time()
    failures = []
    count = 0
    for p in primerange(2, limit + 1):
        sol = solve(p)
        if sol is None:
            failures.append(p)
        else:
            a, b, c = sol
            if not verify(p, a, b, c):
                failures.append(p)
                print(f"  VERIFICATION FAILED for p={p}: ({a}, {b}, {c})")
        count += 1

    elapsed = time.time() - start
    print(f"Checked {count} primes in {elapsed:.2f}s")
    print(f"Throughput: {count/elapsed:.1f} primes/sec")
    if failures:
        print(f"FAILURES ({len(failures)}): {failures[:20]}...")
    else:
        print("ALL PASSED - no failures or verification errors")
