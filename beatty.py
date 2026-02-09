"""beatty — Compute Beatty sequences floor(n * r) for arbitrary real r.

Supports three representations of r:
  * fractions.Fraction  — exact rational arithmetic
  * QuadraticIrrational — exact arithmetic for (a + b*sqrt(d)) / c
  * float               — fast approximate computation via numpy
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import List, Union


class QuadraticIrrational:
    """Represent the real number (a + b * sqrt(d)) / c with integer a, b, c, d.

    Constraints:
        * a, b, c, d are integers
        * d >= 0 and square-free
        * c != 0

    Examples:
        The golden ratio phi = (1 + sqrt(5)) / 2:
            QuadraticIrrational(1, 1, 5, 2)

        sqrt(2) = (0 + 1*sqrt(2)) / 1:
            QuadraticIrrational(0, 1, 2, 1)
    """

    __slots__ = ("a", "b", "d", "c")

    def __init__(self, a: int, b: int, d: int, c: int) -> None:
        if c == 0:
            raise ValueError("Denominator c must be nonzero")
        if d < 0:
            raise ValueError("Radicand d must be non-negative")
        self.a = a
        self.b = b
        self.d = d
        self.c = c

    def __repr__(self) -> str:
        return f"QuadraticIrrational(a={self.a}, b={self.b}, d={self.d}, c={self.c})"

    def to_float(self) -> float:
        """Return a floating-point approximation."""
        return (self.a + self.b * math.sqrt(self.d)) / self.c


def _exact_floor_quad_single(n: int, a: int, b: int, d: int, c: int) -> int:
    """Compute floor(n * (a + b*sqrt(d)) / c) exactly using integer arithmetic.

    Parameters are pre-normalised so that c > 0.
    """
    num = n * a
    coeff = n * b

    # If coeff == 0 or d == 0, purely rational
    if coeff == 0 or d == 0:
        S = math.isqrt(d) if d > 0 else 0
        total = num + coeff * S
        return total // c if total >= 0 else -((-total + c - 1) // c)

    S = math.isqrt(d)
    is_perfect = S * S == d

    if is_perfect:
        total = num + coeff * S
        return total // c if total >= 0 else -((-total + c - 1) // c)

    # sqrt(d) is irrational, S < sqrt(d) < S + 1
    # We want floor((num + coeff * sqrt(d)) / c).
    # 
    # Candidate: use float approximation, then verify exactly.
    # floor_approx might be off by 1.
    #
    # float_val = (num + coeff * math.sqrt(d)) / c
    # But for large n this loses precision. Instead compute via isqrt of n^2*d.
    #
    # We want floor((num + coeff*sqrt(d)) / c).
    # = floor of (num/c + coeff*sqrt(d)/c)
    #
    # Let's compute k = candidate floor.
    # k <= (num + coeff*sqrt(d))/c < k+1
    # iff  num + coeff*sqrt(d) >= k*c  and  num + coeff*sqrt(d) < (k+1)*c
    #
    # For candidate: use isqrt(coeff^2 * d) to get |coeff|*sqrt(d) approximately.
    # isqrt(coeff^2 * d) = floor(|coeff| * sqrt(d))
    
    abs_coeff = abs(coeff)
    # floor(|coeff| * sqrt(d)) = isqrt(coeff^2 * d)
    fsqrt = math.isqrt(coeff * coeff * d)
    # So |coeff| * sqrt(d) is in (fsqrt, fsqrt+1) if not perfect,
    # or exactly fsqrt if perfect.
    sq_check = fsqrt * fsqrt
    target = coeff * coeff * d
    sqrt_exact = (sq_check == target)
    
    if coeff > 0:
        # coeff * sqrt(d) = fsqrt + frac, 0 < frac < 1 (if not exact)
        # num + coeff*sqrt(d) is in (num + fsqrt, num + fsqrt + 1)
        if sqrt_exact:
            total = num + fsqrt
            return total // c if total >= 0 else -((-total + c - 1) // c)
        # lower bound: num + fsqrt (strict), upper: num + fsqrt + 1 (strict)
        lo_total = num + fsqrt      # < actual numerator
        hi_total = num + fsqrt + 1  # > actual numerator
    else:
        # coeff < 0, coeff * sqrt(d) = -(|coeff| * sqrt(d))
        # = -(fsqrt + frac) where 0 < frac < 1
        # So coeff * sqrt(d) is in (-fsqrt - 1, -fsqrt)
        if sqrt_exact:
            total = num - fsqrt
            return total // c if total >= 0 else -((-total + c - 1) // c)
        lo_total = num - fsqrt - 1  # < actual
        hi_total = num - fsqrt      # > actual

    # Floor candidates
    if lo_total >= 0:
        cand_lo = lo_total // c
    else:
        cand_lo = -((-lo_total + c - 1) // c)
    
    if hi_total >= 0:
        cand_hi = hi_total // c
    else:
        cand_hi = -((-hi_total + c - 1) // c)

    if cand_lo == cand_hi:
        return cand_lo

    # At most differ by 1 (since hi_total - lo_total = 1 and c >= 1).
    # Check if cand_hi works: need num + coeff*sqrt(d) >= cand_hi * c
    # i.e. (num - cand_hi*c) + coeff*sqrt(d) >= 0
    # i.e. p + coeff*sqrt(d) >= 0 where p = num - cand_hi*c
    k = cand_hi
    p = num - k * c
    # Check p + coeff*sqrt(d) >= 0
    if coeff > 0:
        # Always >= 0 if p >= 0 (since coeff*sqrt(d) > 0)
        if p >= 0:
            return k
        # p < 0: need coeff*sqrt(d) >= -p, i.e. coeff^2*d >= p^2
        if coeff * coeff * d >= p * p:
            return k
        return k - 1
    else:
        # coeff < 0: p + coeff*sqrt(d) >= 0 iff p >= |coeff|*sqrt(d)
        if p < 0:
            return k - 1
        # p >= 0: need p^2 >= coeff^2 * d
        if p * p >= coeff * coeff * d:
            return k
        return k - 1


def _beatty_quad(qi: QuadraticIrrational, N: int) -> List[int]:
    """Compute [floor(n * qi) for n in 1..N] exactly for a quadratic irrational.

    Uses isqrt for exact integer arithmetic. Optimised to avoid per-element
    overhead where possible.
    """
    a, b, d, c = qi.a, qi.b, qi.d, qi.c

    # Normalise so c > 0
    if c < 0:
        a, b, c = -a, -b, -c

    # Special case: b == 0 or d == 0 => rational
    if b == 0 or d == 0:
        S = math.isqrt(d) if d > 0 else 0
        a_eff = a + b * S
        return _beatty_rational(Fraction(a_eff, c), N)

    S = math.isqrt(d)
    if S * S == d:
        # d is a perfect square, so this is rational
        a_eff = a + b * S
        return _beatty_rational(Fraction(a_eff, c), N)

    # General case: irrational sqrt(d)
    # For each n, compute floor(n*(a + b*sqrt(d))/c).
    # Use the optimised single-element function in a tight loop.
    # Pre-compute constants to speed things up.
    result: List[int] = [0] * N
    
    # For the common case where |cand_hi - cand_lo| <= 1, the inner loop
    # is quite fast. Let's inline the critical path.
    b_pos = b > 0
    
    for n in range(1, N + 1):
        num = n * a
        coeff = n * b
        
        # isqrt(coeff^2 * d)
        abs_coeff = coeff if coeff > 0 else -coeff
        # floor(abs_coeff * sqrt(d))
        fsqrt = math.isqrt(coeff * coeff * d)
        
        if b_pos:
            # coeff > 0 since b > 0 and n > 0
            lo_total = num + fsqrt
            # floor(lo_total / c) -- c > 0
            if lo_total >= 0:
                k = lo_total // c
            else:
                k = -((-lo_total + c - 1) // c)
            
            # Check if k+1 also works
            p = num - (k + 1) * c
            # Need p + coeff*sqrt(d) >= 0
            if p >= 0:
                result[n - 1] = k + 1
            elif coeff * coeff * d >= p * p:
                result[n - 1] = k + 1
            else:
                result[n - 1] = k
        else:
            # coeff < 0
            hi_total = num - fsqrt
            if hi_total >= 0:
                k = hi_total // c
            else:
                k = -((-hi_total + c - 1) // c)
            
            # k is the upper candidate; check if it works
            p = num - k * c
            # Need p + coeff*sqrt(d) >= 0, coeff < 0
            # p >= |coeff|*sqrt(d) iff p >= 0 and p^2 >= coeff^2*d
            if p < 0:
                result[n - 1] = k - 1
            elif p * p >= coeff * coeff * d:
                result[n - 1] = k
            else:
                result[n - 1] = k - 1
    
    return result


def _beatty_rational(r: Fraction, N: int) -> List[int]:
    """Compute [floor(n * r) for n in 1..N] exactly for rational r."""
    p, q = r.numerator, r.denominator
    if q < 0:
        p, q = -p, -q
    # floor(n*p / q) for positive q: use divmod-style
    result: List[int] = [0] * N
    for n in range(1, N + 1):
        val = n * p
        if val >= 0:
            result[n - 1] = val // q
        else:
            result[n - 1] = -((-val + q - 1) // q)
    return result


def _beatty_float(r: float, N: int) -> List[int]:
    """Compute [floor(n * r) for n in 1..N] using numpy for speed."""
    try:
        import numpy as np
    except ImportError:
        return [int(math.floor(n * r)) for n in range(1, N + 1)]
    ns = np.arange(1, N + 1, dtype=np.float64)
    return np.floor(ns * r).astype(np.int64).tolist()


def beatty_sequence(r: Union[Fraction, QuadraticIrrational, float], N: int) -> List[int]:
    """Compute the Beatty sequence [floor(n * r) for n = 1, 2, ..., N].

    Parameters
    ----------
    r : Fraction, QuadraticIrrational, or float
        The real multiplier.  Determines which arithmetic path is used:
        - Fraction: exact rational floor via integer arithmetic.
        - QuadraticIrrational: exact floor via isqrt-based integer arithmetic.
        - float: fast approximate computation via numpy (or pure Python fallback).
    N : int
        Number of terms (n ranges from 1 to N inclusive).

    Returns
    -------
    List[int]
        The first N terms of the Beatty sequence for r.

    Examples
    --------
    >>> beatty_sequence(Fraction(3, 2), 5)
    [1, 3, 4, 6, 7]
    >>> beatty_sequence(QuadraticIrrational(1, 1, 5, 2), 5)  # phi
    [1, 3, 4, 6, 8]
    """
    if N < 0:
        raise ValueError("N must be non-negative")
    if N == 0:
        return []

    if isinstance(r, Fraction):
        return _beatty_rational(r, N)
    elif isinstance(r, QuadraticIrrational):
        return _beatty_quad(r, N)
    elif isinstance(r, (int, float)):
        return _beatty_float(float(r), N)
    else:
        raise TypeError(f"Unsupported type for r: {type(r)}")


if __name__ == "__main__":
    import time

    # ------------------------------------------------------------------ #
    # Test 1: Beatty sequence for phi = (1 + sqrt(5)) / 2, n = 1..20
    # OEIS A000201
    # ------------------------------------------------------------------ #
    phi = QuadraticIrrational(1, 1, 5, 2)
    expected_phi = [1, 3, 4, 6, 8, 9, 11, 12, 14, 16,
                    17, 19, 21, 22, 24, 25, 27, 29, 30, 32]
    result_phi = beatty_sequence(phi, 20)
    assert result_phi == expected_phi, (
        f"phi test failed:\n  got      {result_phi}\n  expected {expected_phi}"
    )
    print("PASS: floor(n * phi) for n=1..20 matches OEIS A000201")

    # ------------------------------------------------------------------ #
    # Test 2: Beatty sequence for 3/2 (rational), n = 1..10
    # ------------------------------------------------------------------ #
    r_rat = Fraction(3, 2)
    expected_rat = [1, 3, 4, 6, 7, 9, 10, 12, 13, 15]
    result_rat = beatty_sequence(r_rat, 10)
    assert result_rat == expected_rat, (
        f"3/2 test failed:\n  got      {result_rat}\n  expected {expected_rat}"
    )
    print("PASS: floor(n * 3/2) for n=1..10 matches expected")

    # ------------------------------------------------------------------ #
    # Test 3: Beatty sequence for sqrt(2), n = 1..10
    # ------------------------------------------------------------------ #
    sqrt2 = QuadraticIrrational(0, 1, 2, 1)
    expected_sqrt2 = [1, 2, 4, 5, 7, 8, 9, 11, 12, 14]
    result_sqrt2 = beatty_sequence(sqrt2, 10)
    assert result_sqrt2 == expected_sqrt2, (
        f"sqrt(2) test failed:\n  got      {result_sqrt2}\n  expected {expected_sqrt2}"
    )
    print("PASS: floor(n * sqrt(2)) for n=1..10 matches expected")

    # ------------------------------------------------------------------ #
    # Test 4: Performance — N = 10^6, float path
    # ------------------------------------------------------------------ #
    t0 = time.perf_counter()
    _ = beatty_sequence(1.6180339887498949, 1_000_000)
    dt_float = time.perf_counter() - t0
    print(f"PASS: float path, N=10^6 in {dt_float:.3f}s (limit 5s)")
    assert dt_float < 5.0, f"Float path too slow: {dt_float:.3f}s"

    # ------------------------------------------------------------------ #
    # Test 5: Performance — N = 10^6, quadratic irrational path
    # ------------------------------------------------------------------ #
    t0 = time.perf_counter()
    _ = beatty_sequence(phi, 1_000_000)
    dt_quad = time.perf_counter() - t0
    print(f"PERF: quadratic irrational path, N=10^6 in {dt_quad:.3f}s (limit 5s)")
    assert dt_quad < 5.0, f"Quadratic irrational path too slow: {dt_quad:.3f}s"

    print("\nAll tests passed.")
