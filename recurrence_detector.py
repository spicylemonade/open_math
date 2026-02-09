#!/usr/bin/env python3
"""Detect and fit homogeneous linear recurrences from integer sequences.

Uses the Berlekamp-Massey algorithm implemented over the rationals
(via ``fractions.Fraction``) so that all arithmetic is exact.

Public API
----------
find_recurrence(seq, max_order=50) -> dict | None
    Given a finite integer (or rational) sequence, return the minimal-order
    homogeneous linear recurrence that generates it, or ``None`` when no
    recurrence of order <= *max_order* exists.

berlekamp_massey(seq) -> list[Fraction]
    Raw Berlekamp-Massey: return the connection polynomial coefficients
    (excluding the leading 1) for the shortest LFSR that generates *seq*.
"""

from __future__ import annotations

import copy
from fractions import Fraction
from typing import List, Optional, Union

# ---------------------------------------------------------------------------
# Berlekamp-Massey algorithm over the rationals
# ---------------------------------------------------------------------------

def berlekamp_massey(seq: list[Union[int, Fraction]]) -> list[Fraction]:
    """Return the minimal LFSR connection-polynomial coefficients for *seq*.

    The algorithm works over an arbitrary field; here we use ``Fraction`` so
    that the computation is exact for integer / rational inputs.

    Parameters
    ----------
    seq : list of int or Fraction
        The input sequence  s_0, s_1, ..., s_{N-1}.

    Returns
    -------
    list of Fraction
        Coefficients ``[c_1, c_2, ..., c_L]`` of the connection polynomial
        ``C(x) = 1 - c_1 x - c_2 x^2 - ... - c_L x^L`` such that for all
        valid *n*::

            s_n = c_1 * s_{n-1} + c_2 * s_{n-2} + ... + c_L * s_{n-L}

    Notes
    -----
    If the sequence is all zeros the returned list is empty (order 0).
    """
    # Convert everything to Fraction for exact arithmetic.
    s: list[Fraction] = [Fraction(v) for v in seq]
    n = len(s)

    if n == 0:
        return []

    # C is the current connection polynomial stored as a list where
    # C[j] is the coefficient of x^j.  C(x) = 1 initially.
    # B is the previous best polynomial, similarly stored.
    C: list[Fraction] = [Fraction(1)]
    B: list[Fraction] = [Fraction(1)]

    L = 0          # current LFSR length
    m = 1          # how many steps since B was last updated
    b = Fraction(1)  # previous discrepancy when B was updated

    for i in range(n):
        # Compute discrepancy d = s[i] + sum_{j=1}^{L} C[j] * s[i-j]
        # (where C[0] = 1 and the recurrence is  sum_{j=0}^{L} C[j]*s[i-j] = 0)
        d = Fraction(0)
        for j in range(len(C)):
            if j <= i:
                d += C[j] * s[i - j]

        if d == 0:
            m += 1
            continue

        # T = copy of C (for potential later use as new B)
        T = copy.copy(C)

        # Update C:  C(x) <- C(x) - (d/b) * x^m * B(x)
        coeff = d / b
        # Ensure C is long enough
        needed = m + len(B)
        while len(C) < needed:
            C.append(Fraction(0))
        for j in range(len(B)):
            C[j + m] -= coeff * B[j]

        if 2 * L <= i:
            # Complexity increase: update L, B, b
            L = i + 1 - L
            B = T
            b = d
            m = 1
        else:
            m += 1

    # The connection polynomial C satisfies  sum_{j=0}^{L} C[j]*s[n-j] = 0,
    # i.e.  s[n] = -C[1]*s[n-1] - C[2]*s[n-2] - ...
    # We return  c_k = -C[k]  for k = 1..L  so that
    #   s[n] = c_1*s[n-1] + c_2*s[n-2] + ... + c_L*s[n-L].
    coeffs = [-C[j] for j in range(1, L + 1)]
    return coeffs


# ---------------------------------------------------------------------------
# High-level recurrence finder
# ---------------------------------------------------------------------------

def _verify_recurrence(
    seq: list[Fraction],
    coeffs: list[Fraction],
    start: int,
) -> int:
    """Return the number of terms from index *start* onward that satisfy the recurrence."""
    order = len(coeffs)
    verified = 0
    for i in range(start, len(seq)):
        if i < order:
            continue
        predicted = sum(coeffs[j] * seq[i - 1 - j] for j in range(order))
        if predicted != seq[i]:
            break
        verified += 1
    return verified


def find_recurrence(
    seq: list[int],
    max_order: int = 50,
) -> Optional[dict]:
    """Find the minimal homogeneous linear recurrence for *seq*.

    Parameters
    ----------
    seq : list of int
        The input integer sequence, length >= 1.
    max_order : int, optional
        Maximum recurrence order to consider (default 50).

    Returns
    -------
    dict or None
        If a valid recurrence is found, a dict with keys:

        - ``'order'``: int -- the recurrence order *k*.
        - ``'coefficients'``: list -- ``[c_1, ..., c_k]`` as ``int`` when
          possible, otherwise ``Fraction``.
        - ``'characteristic_poly'``: list -- coefficients of the
          characteristic polynomial
          ``x^k - c_1 x^{k-1} - ... - c_k`` from highest to lowest power.
        - ``'verified_length'``: int -- how many sequence terms beyond the
          minimum fitting window were successfully verified.

        Returns ``None`` when no recurrence of order <= *max_order* is found.
    """
    if not seq:
        return None

    s = [Fraction(v) for v in seq]
    n = len(s)

    # All-zero sequence: trivially order-0 (or order-1 with coeff 0).
    # We treat it as order 1 with coeff [0] for consistency, but actually
    # we can consider it order 0.  For the purposes of the spec we skip
    # ahead and let Berlekamp-Massey handle it.

    # Run Berlekamp-Massey on the whole sequence.
    coeffs = berlekamp_massey(s)

    order = len(coeffs)

    # Edge: BM on all-zeros returns order 0.
    if order == 0:
        # Check: is the entire sequence zero?
        if all(v == 0 for v in s):
            # Trivial: every value is 0; any recurrence works.
            # Report order 1, coeff [0].
            return {
                "order": 1,
                "coefficients": [0],
                "characteristic_poly": [1, 0],
                "verified_length": max(n - 1, 0),
            }
        # Non-zero sequence but BM returned order 0 -- shouldn't happen.
        return None

    if order > max_order:
        return None

    # The recurrence requires *order* initial values.  We need at least
    # 2*order terms for BM to guarantee uniqueness.  Verify the recurrence
    # on all terms from index *order* onward.
    verified = _verify_recurrence(s, coeffs, start=order)

    # Total terms that *should* be verified (all terms from index order..n-1).
    verifiable = max(n - order, 0)

    if verified < verifiable:
        # The recurrence doesn't actually hold for the full sequence.
        return None

    # We also check that we have enough data: BM needs at least 2*order
    # terms to guarantee the LFSR is correct.  If n < 2*order we can still
    # report, but flag that verification is weak.  Here, verified_length
    # counts how many terms beyond the minimal 2*order fitting window were
    # verified.
    fitting_window = 2 * order
    extra_verified = max(verified - max(fitting_window - order, 0), 0)

    # Pretty-print coefficients: convert to int when denominator is 1.
    def _nice(f: Fraction):
        return int(f) if f.denominator == 1 else f

    nice_coeffs = [_nice(c) for c in coeffs]

    # Characteristic polynomial: x^k - c_1 x^{k-1} - ... - c_k
    # Stored as list from highest power to lowest:
    #   [1, -c_1, -c_2, ..., -c_k]
    char_poly = [_nice(Fraction(1))] + [_nice(-c) for c in coeffs]

    return {
        "order": order,
        "coefficients": nice_coeffs,
        "characteristic_poly": char_poly,
        "verified_length": extra_verified,
    }


# ---------------------------------------------------------------------------
# Predict future terms using a discovered recurrence
# ---------------------------------------------------------------------------

def predict(
    seq: list[int],
    recurrence: dict,
    n_terms: int = 10,
) -> list[Union[int, Fraction]]:
    """Extend *seq* by *n_terms* using the given *recurrence*.

    Parameters
    ----------
    seq : list of int
        Original sequence (must have at least ``recurrence['order']`` terms).
    recurrence : dict
        As returned by :func:`find_recurrence`.
    n_terms : int
        Number of new terms to generate.

    Returns
    -------
    list of int or Fraction
        The predicted terms.
    """
    order = recurrence["order"]
    coeffs = [Fraction(c) for c in recurrence["coefficients"]]
    buf = [Fraction(v) for v in seq]

    result = []
    for _ in range(n_terms):
        val = sum(coeffs[j] * buf[-(j + 1)] for j in range(order))
        nice = int(val) if val.denominator == 1 else val
        result.append(nice)
        buf.append(val)
    return result


# ---------------------------------------------------------------------------
# Unit tests (run via ``python recurrence_detector.py``)
# ---------------------------------------------------------------------------

def _run_tests() -> None:
    import sys
    passed = 0
    failed = 0

    def check(name: str, condition: bool, detail: str = ""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {name}")
        else:
            failed += 1
            msg = f"  FAIL  {name}"
            if detail:
                msg += f"  -- {detail}"
            print(msg)

    print("=" * 60)
    print("Running recurrence_detector tests")
    print("=" * 60)

    # ----- Fibonacci -----
    print("\n--- Fibonacci ---")
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    res = find_recurrence(fib)
    check("fib: found", res is not None)
    if res:
        check("fib: order == 2", res["order"] == 2, f"got {res['order']}")
        check("fib: coeffs == [1, 1]", res["coefficients"] == [1, 1],
              f"got {res['coefficients']}")
        # Predict next two terms
        nxt = predict(fib, res, 2)
        check("fib: predict [233, 377]", nxt == [233, 377], f"got {nxt}")

    # ----- Tribonacci -----
    print("\n--- Tribonacci ---")
    tri = [1, 1, 2, 4, 7, 13, 24, 44, 81, 149]
    res = find_recurrence(tri)
    check("tri: found", res is not None)
    if res:
        check("tri: order == 3", res["order"] == 3, f"got {res['order']}")
        check("tri: coeffs == [1, 1, 1]", res["coefficients"] == [1, 1, 1],
              f"got {res['coefficients']}")

    # ----- Powers of 2 (geometric) -----
    print("\n--- Powers of 2 ---")
    geo = [1, 2, 4, 8, 16, 32, 64]
    res = find_recurrence(geo)
    check("geo: found", res is not None)
    if res:
        check("geo: order == 1", res["order"] == 1, f"got {res['order']}")
        check("geo: coeffs == [2]", res["coefficients"] == [2],
              f"got {res['coefficients']}")
        nxt = predict(geo, res, 3)
        check("geo: predict [128, 256, 512]", nxt == [128, 256, 512],
              f"got {nxt}")

    # ----- Constant sequence -----
    print("\n--- Constant sequence ---")
    const = [5, 5, 5, 5, 5, 5]
    res = find_recurrence(const)
    check("const: found", res is not None)
    if res:
        check("const: order == 1", res["order"] == 1, f"got {res['order']}")
        check("const: coeffs == [1]", res["coefficients"] == [1],
              f"got {res['coefficients']}")
        nxt = predict(const, res, 3)
        check("const: predict [5, 5, 5]", nxt == [5, 5, 5], f"got {nxt}")

    # ----- Non-recurrent / random -----
    print("\n--- Non-recurrent (random) ---")
    rand_seq = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]
    res = find_recurrence(rand_seq, max_order=6)
    check("rand: no recurrence (max_order=6)", res is None, f"got {res}")

    # ----- All-zeros -----
    print("\n--- All-zeros ---")
    zeros = [0, 0, 0, 0, 0]
    res = find_recurrence(zeros)
    check("zeros: found", res is not None)
    if res:
        check("zeros: order == 1", res["order"] == 1, f"got {res['order']}")
        check("zeros: coeffs == [0]", res["coefficients"] == [0],
              f"got {res['coefficients']}")

    # ----- Lucas numbers: a_n = a_{n-1} + a_{n-2}, starts 2,1 -----
    print("\n--- Lucas numbers ---")
    lucas = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123]
    res = find_recurrence(lucas)
    check("lucas: found", res is not None)
    if res:
        check("lucas: order == 2", res["order"] == 2, f"got {res['order']}")
        check("lucas: coeffs == [1, 1]", res["coefficients"] == [1, 1],
              f"got {res['coefficients']}")

    # ----- Pell numbers: a_n = 2*a_{n-1} + a_{n-2} -----
    print("\n--- Pell numbers ---")
    pell = [0, 1, 2, 5, 12, 29, 70, 169, 408, 985]
    res = find_recurrence(pell)
    check("pell: found", res is not None)
    if res:
        check("pell: order == 2", res["order"] == 2, f"got {res['order']}")
        check("pell: coeffs == [2, 1]", res["coefficients"] == [2, 1],
              f"got {res['coefficients']}")

    # ----- Characteristic polynomial check -----
    print("\n--- Characteristic polynomial ---")
    fib2 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    res = find_recurrence(fib2)
    if res:
        # x^2 - x - 1  =>  [1, -1, -1]
        check("char_poly: fib == [1, -1, -1]",
              res["characteristic_poly"] == [1, -1, -1],
              f"got {res['characteristic_poly']}")

    # ----- Single-element sequence -----
    print("\n--- Single element ---")
    res = find_recurrence([42])
    # Not enough data to find a meaningful recurrence; BM may return order 0 or 1
    # depending on value.  For a single nonzero element, BM needs at least 2 terms.
    check("single: returns something sensible (None or order <= 1)",
          res is None or (res is not None and res["order"] <= 1),
          f"got {res}")

    # ----- Empty sequence -----
    print("\n--- Empty ---")
    res = find_recurrence([])
    check("empty: returns None", res is None, f"got {res}")

    # ----- Summary -----
    print("\n" + "=" * 60)
    total = passed + failed
    print(f"Results: {passed}/{total} passed, {failed} failed")
    print("=" * 60)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
