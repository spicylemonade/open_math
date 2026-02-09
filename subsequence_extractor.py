"""Subsequence extraction module for Beatty sequences.

Provides multiple strategies for extracting subsequences from Beatty sequences:
1. Arithmetic progression indexing
2. Iterated Beatty compositions
3. Wythoff-type path extraction
"""

from __future__ import annotations
import math
from fractions import Fraction
from typing import List, Optional, Tuple

from beatty import beatty_sequence, QuadraticIrrational


def arithmetic_progression_subsequence(
    seq: List[int], start: int, step: int, count: int
) -> List[int]:
    """Extract subsequence at indices start, start+step, start+2*step, ...

    Args:
        seq: The base sequence (0-indexed internally, but represents B_r(1), B_r(2), ...)
        start: Starting index (0-based into seq)
        step: Step size
        count: Number of terms to extract

    Returns:
        List of extracted values.
    """
    result = []
    idx = start
    for _ in range(count):
        if idx >= len(seq):
            break
        result.append(seq[idx])
        idx += step
    return result


def iterated_composition(
    r: float | Fraction | QuadraticIrrational,
    n_start: int,
    depth: int,
    use_complement: bool = True,
) -> List[int]:
    """Compute iterated Beatty composition: b^0(n) = n, b^{y+1}(n) = B(b^y(n)).

    For complementary Beatty pair: if r > 1 and 1/r + 1/s = 1,
    we iterate using s (the complement) by default.

    Args:
        r: The base Beatty parameter
        n_start: Starting value n
        depth: Number of iterations
        use_complement: If True, iterate with the complementary parameter s = r/(r-1)

    Returns:
        List [b^0(n), b^1(n), ..., b^depth(n)]
    """
    # Compute r as float for iteration
    if isinstance(r, QuadraticIrrational):
        r_float = r.to_float()
    elif isinstance(r, Fraction):
        r_float = float(r)
    else:
        r_float = float(r)

    if use_complement and r_float > 1.0:
        # s = r/(r-1) so 1/r + 1/s = 1
        s_float = r_float / (r_float - 1.0)
        iterate_param = s_float
    else:
        iterate_param = r_float

    result = [n_start]
    current = n_start
    for _ in range(depth):
        current = int(math.floor(current * iterate_param))
        if current <= 0:
            break
        result.append(current)
    return result


def iterated_a_composition(
    r_float: float, n_start: int, depth: int
) -> List[int]:
    """Iterate using the lower Beatty function: a^0(n) = n, a^{y+1}(n) = floor(a^y(n) * r).

    Args:
        r_float: The Beatty parameter as a float
        n_start: Starting value
        depth: Number of iterations

    Returns:
        List [a^0(n), a^1(n), ..., a^depth(n)]
    """
    result = [n_start]
    current = n_start
    for _ in range(depth):
        current = int(math.floor(current * r_float))
        if current <= 0:
            break
        result.append(current)
    return result


def wythoff_row(
    r: float | Fraction | QuadraticIrrational, m: int, length: int
) -> List[int]:
    """Extract a row of the generalized Wythoff array.

    For r = phi, this gives the standard Wythoff array where each row
    satisfies the Fibonacci recurrence.

    Row m starts with A(m), B(m) and extends via:
      w(m, k+2) = w(m, k+1) + w(m, k) for the golden ratio case.

    For general quadratic irrational r with conjugate r', the recurrence is:
      w(m, k+2) = (r + r') * w(m, k+1) - r*r' * w(m, k)
    but since r + r' and r*r' may not be integers, we compute the first
    two terms exactly and then use the recurrence.

    Args:
        r: The Beatty parameter
        m: Row index (1-based)
        length: Number of terms in the row

    Returns:
        List of terms in the Wythoff row
    """
    if isinstance(r, QuadraticIrrational):
        r_float = r.to_float()
    elif isinstance(r, Fraction):
        r_float = float(r)
    else:
        r_float = float(r)

    if r_float <= 1.0:
        # For r <= 1, Wythoff construction doesn't apply directly
        # Just use arithmetic subsequences instead
        return arithmetic_progression_subsequence(
            beatty_sequence(r, max(m * length * 10, 1000)), m - 1, m, length
        )

    s_float = r_float / (r_float - 1.0)

    # First two terms: A(m) = floor(m*r), B(m) = floor(m*s)
    a_m = int(math.floor(m * r_float))
    b_m = int(math.floor(m * s_float))

    if length <= 0:
        return []
    if length == 1:
        return [a_m]

    row = [a_m, b_m]

    # Extend using Fibonacci-type recurrence
    # For golden ratio: w(k+2) = w(k+1) + w(k)
    # For general quadratic: w(k+2) = trace * w(k+1) - norm * w(k)
    # where trace = r + r' and norm = r * r'
    # But we need integer recurrence, so we detect the recurrence from the first few terms

    # For now, use the iterative approach: next term = floor of complement applied
    # Actually, the correct Wythoff extension is w(k+2) = w(k+1) + w(k) for phi
    # For general quadratic irrational, we use the trace/norm

    if isinstance(r, QuadraticIrrational):
        # r = (a + b*sqrt(d))/c, conjugate r' = (a - b*sqrt(d))/c
        # trace = r + r' = 2a/c
        # norm = r * r' = (a^2 - b^2*d)/c^2
        trace = Fraction(2 * r.a, r.c)
        norm = Fraction(r.a * r.a - r.b * r.b * r.d, r.c * r.c)
    else:
        # For float, try to detect phi
        phi = (1 + math.sqrt(5)) / 2
        if abs(r_float - phi) < 1e-10:
            trace = Fraction(1)  # phi + phi' = 1 (since phi' = (1-sqrt(5))/2, trace = 1)
            norm = Fraction(-1)  # phi * phi' = -1
        else:
            # Generic: use float approximation
            # Cannot determine exact trace/norm, use iterative method
            for k in range(length - 2):
                next_val = int(math.floor(row[-1] * r_float))
                if next_val <= row[-1]:
                    # Growth stalled, try complement
                    next_val = int(math.floor(row[-1] * s_float))
                row.append(next_val)
            return row[:length]

    # Use the recurrence w(k+2) = trace * w(k+1) - norm * w(k)
    for k in range(length - 2):
        w_next = trace * row[-1] - norm * row[-2]
        row.append(int(w_next))

    return row[:length]


def extract_all_strategies(
    r: float | Fraction | QuadraticIrrational,
    N: int = 10000,
    max_subseq_len: int = 200,
) -> List[Tuple[str, List[int]]]:
    """Apply all extraction strategies and return named subsequences.

    Args:
        r: Beatty parameter
        N: Length of base Beatty sequence to compute
        max_subseq_len: Maximum length of extracted subsequences

    Returns:
        List of (strategy_name, subsequence) pairs
    """
    if isinstance(r, QuadraticIrrational):
        r_float = r.to_float()
    elif isinstance(r, Fraction):
        r_float = float(r)
    else:
        r_float = float(r)

    # Compute base sequence
    seq = beatty_sequence(r, N)
    results = []

    # Strategy 1: Arithmetic progressions with various steps
    for start in [0, 1]:
        for step in range(1, 21):
            count = min(max_subseq_len, (N - start) // step)
            if count >= 20:
                subseq = arithmetic_progression_subsequence(seq, start, step, count)
                results.append((f"arith_start{start}_step{step}", subseq))

    # Strategy 2: Iterated compositions (complement)
    for n_start in [1, 2, 3, 5, 10]:
        depth = min(max_subseq_len, 100)
        subseq = iterated_composition(r, n_start, depth, use_complement=True)
        if len(subseq) >= 10:
            results.append((f"iter_comp_n{n_start}", subseq))

    # Strategy 3: Iterated a-compositions (using r itself)
    for n_start in [1, 2, 3, 5]:
        subseq = iterated_a_composition(r_float, n_start, min(max_subseq_len, 100))
        if len(subseq) >= 10:
            results.append((f"iter_a_n{n_start}", subseq))

    # Strategy 4: Wythoff rows
    for m in [1, 2, 3, 4, 5, 10]:
        row = wythoff_row(r, m, min(max_subseq_len, 50))
        if len(row) >= 5:
            results.append((f"wythoff_row{m}", row))

    return results


if __name__ == "__main__":
    import math

    print("=== Subsequence Extractor Tests ===")

    # Test 1: Arithmetic progression extraction
    seq = list(range(1, 101))  # 1, 2, ..., 100
    subseq = arithmetic_progression_subsequence(seq, 0, 3, 10)
    assert subseq == [1, 4, 7, 10, 13, 16, 19, 22, 25, 28], f"AP test failed: {subseq}"
    print("PASS: Arithmetic progression extraction")

    # Test 2: Wythoff row for phi - should produce Fibonacci-type sequence
    phi = QuadraticIrrational(1, 1, 5, 2)  # (1 + sqrt(5))/2
    row1 = wythoff_row(phi, 1, 7)
    # Row 1 of Wythoff array: 1, 2, 3, 5, 8, 13, 21
    expected_row1 = [1, 2, 3, 5, 8, 13, 21]
    assert row1 == expected_row1, f"Wythoff row 1 test failed: got {row1}, expected {expected_row1}"
    print("PASS: Wythoff row 1 produces Fibonacci numbers")

    # Verify Fibonacci recurrence holds
    for i in range(2, len(row1)):
        assert row1[i] == row1[i-1] + row1[i-2], f"Fibonacci recurrence failed at index {i}"
    print("PASS: Wythoff row 1 satisfies Fibonacci recurrence")

    # Test 3: Iterated composition for phi
    comp = iterated_composition(phi, 1, 20, use_complement=True)
    print(f"Iterated composition b^y(1) for phi: {comp[:15]}")
    # For phi, b(n) = floor(n*phi^2) = floor(n*(phi+1)) = n + floor(n*phi)
    # b^y(1) should grow like phi^y

    # Test 4: extract_all_strategies returns non-empty results
    all_subseqs = extract_all_strategies(phi, N=5000, max_subseq_len=100)
    assert len(all_subseqs) > 20, f"Expected many strategies, got {len(all_subseqs)}"
    print(f"PASS: extract_all_strategies returned {len(all_subseqs)} subsequences")

    # Test 5: Iterated composition for rational
    r_rat = Fraction(3, 2)
    comp_rat = iterated_composition(r_rat, 1, 20, use_complement=False)
    print(f"Iterated a-composition for 3/2: {comp_rat[:15]}")

    print("\n=== All tests passed ===")
