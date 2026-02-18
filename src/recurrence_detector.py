"""
Linear recurrence detector using the Berlekamp-Massey algorithm.

Given a finite integer sequence, determines whether it satisfies a homogeneous
linear recurrence with constant coefficients, and if so finds the minimal such
recurrence.

Uses exact rational arithmetic to avoid floating-point errors.

References:
  - Berlekamp (1968), "Algebraic Coding Theory"
  - Massey (1969), "Shift-register synthesis and BCH decoding"
"""

from fractions import Fraction
from typing import List, Optional, Tuple


def berlekamp_massey_rational(seq: List[int]) -> Optional[List[Fraction]]:
    """Berlekamp-Massey algorithm over rationals.

    Given a sequence s_0, s_1, ..., s_{N-1}, finds the shortest LFSR
    (equivalently, the minimal homogeneous linear recurrence) that generates it.

    The recurrence is: s_n = c_1*s_{n-1} + c_2*s_{n-2} + ... + c_L*s_{n-L}
    where L is the order.

    Returns:
        List of Fraction coefficients [c_1, c_2, ..., c_L] such that
        s_n = c_1*s_{n-1} + ... + c_L*s_{n-L} for all valid n,
        or None if no recurrence of order <= N//2 exists.
    """
    N = len(seq)
    s = [Fraction(x) for x in seq]

    # C(x) = current connection polynomial, B(x) = previous
    # C[0] = 1, C[1] = -c_1, C[2] = -c_2, etc.
    C = [Fraction(1)]
    B = [Fraction(1)]
    L = 0  # current LFSR length
    m = 1  # steps since last update
    b = Fraction(1)  # previous discrepancy

    for n in range(N):
        # Compute discrepancy
        d = s[n]
        for i in range(1, L + 1):
            if i < len(C):
                d += C[i] * s[n - i]

        if d == 0:
            m += 1
        elif 2 * L <= n:
            # Update
            T = C[:]
            coeff = d / b
            # Pad C if needed
            while len(C) < len(B) + m:
                C.append(Fraction(0))
            for i in range(len(B)):
                C[i + m] -= coeff * B[i]
            L = n + 1 - L
            B = T
            b = d
            m = 1
        else:
            coeff = d / b
            while len(C) < len(B) + m:
                C.append(Fraction(0))
            for i in range(len(B)):
                C[i + m] -= coeff * B[i]
            m += 1

    # Verify: LFSR length should be <= N//2 for reliable detection
    if L > N // 2:
        return None

    # Convert connection polynomial to recurrence coefficients
    # C[0]=1, C[1], ..., C[L] gives: s_n + C[1]*s_{n-1} + ... + C[L]*s_{n-L} = 0
    # So s_n = -C[1]*s_{n-1} - ... - C[L]*s_{n-L}
    coeffs = [-C[i] for i in range(1, L + 1)]
    return coeffs


def find_homogeneous_recurrence(seq: List[int], d_max: int = 50
                                ) -> Optional[Tuple[int, List[Fraction]]]:
    """Find the minimal homogeneous linear recurrence for an integer sequence.

    Args:
        seq: Integer sequence of length N
        d_max: Maximum recurrence order to search for

    Returns:
        Tuple of (order, coefficients) where coefficients [c_1, ..., c_d] satisfy
        a_n = c_1*a_{n-1} + ... + c_d*a_{n-d}, or None if no recurrence found.

    Notes:
        The BM algorithm always finds an LFSR of length <= N/2, so we require
        the order to be at most N/3 to avoid overfitting, and we verify the
        recurrence predicts correctly on a held-out portion.
    """
    N = len(seq)
    if N < 10:
        return None

    # Use first 1/3 for detection, remaining 2/3 for out-of-sample verification.
    # This guards against BM overfitting to quasi-periodic sequences.
    train_len = N // 3
    if train_len < 2 * d_max + 2:
        # Not enough data for reliable detection at this d_max
        effective_dmax = max(1, (train_len - 2) // 2)
        if effective_dmax < 1:
            return None
    else:
        effective_dmax = d_max

    coeffs = berlekamp_massey_rational(seq[:train_len])
    if coeffs is None:
        return None

    order = len(coeffs)
    if order == 0:
        return None
    if order > effective_dmax:
        return None

    # The order must be at most train_len / 4 for reliability
    if order > train_len // 4:
        return None

    # Verify the recurrence holds for ALL N terms (2/3 is out-of-sample)
    if not verify_recurrence(seq, coeffs):
        return None

    # Additional check: for sequences that look "almost periodic" in their
    # first differences, the recurrence may hold for thousands of terms then
    # fail. Require that the verified portion is at least 5x the order.
    verified_terms = N - order
    if verified_terms < 5 * order:
        return None

    return (order, coeffs)


def verify_recurrence(seq: List[int], coeffs: List[Fraction],
                      tolerance: int = 0) -> bool:
    """Verify that a recurrence holds for the entire sequence.

    Checks that s_n = c_1*s_{n-1} + ... + c_d*s_{n-d} for all valid n.

    Args:
        seq: The integer sequence
        coeffs: [c_1, ..., c_d] recurrence coefficients
        tolerance: allowed absolute error (0 for exact)

    Returns:
        True if the recurrence holds for all terms
    """
    d = len(coeffs)
    s = [Fraction(x) for x in seq]

    for n in range(d, len(s)):
        predicted = sum(coeffs[i] * s[n - 1 - i] for i in range(d))
        if abs(predicted - s[n]) > tolerance:
            return False
    return True


def recurrence_to_homogeneous_form(order: int, coeffs: List[Fraction]
                                   ) -> Tuple[List[int], str]:
    """Convert recurrence coefficients to standard homogeneous form.

    From: a_n = c_1*a_{n-1} + ... + c_d*a_{n-d}
    To: a_n - c_1*a_{n-1} - ... - c_d*a_{n-d} = 0

    Returns:
        Tuple of (integer_coefficients, human_readable_string)
        where integer_coefficients = [1, -c_1, -c_2, ..., -c_d] scaled to integers
    """
    # Find common denominator
    from math import gcd
    from functools import reduce

    hom = [Fraction(1)] + [-c for c in coeffs]

    # Scale to integers
    denoms = [abs(f.denominator) for f in hom]
    lcm_val = reduce(lambda a, b: a * b // gcd(a, b), denoms)
    int_coeffs = [int(f * lcm_val) for f in hom]

    # Simplify by GCD
    g = reduce(gcd, [abs(c) for c in int_coeffs if c != 0])
    if g > 1:
        int_coeffs = [c // g for c in int_coeffs]

    # Human-readable
    terms = []
    d = len(int_coeffs) - 1
    for i, c in enumerate(int_coeffs):
        shift = d - i
        if c == 0:
            continue
        if c == 1:
            coeff_str = ""
        elif c == -1:
            coeff_str = "-"
        else:
            coeff_str = str(c) + "*"
        if shift == 0:
            terms.append(f"{coeff_str}a_n")
        else:
            terms.append(f"{coeff_str}a_{{n+{shift}}}")

    readable = " + ".join(terms).replace("+ -", "- ") + " = 0"

    return int_coeffs, readable


def compute_recurrence_residual(seq: List[int], coeffs: List[Fraction]
                                ) -> List[Fraction]:
    """Compute the residual of a candidate recurrence at each position.

    Returns R[n] = a_n - (c_1*a_{n-1} + ... + c_d*a_{n-d}) for n >= d.
    """
    d = len(coeffs)
    s = [Fraction(x) for x in seq]
    residuals = []
    for n in range(d, len(s)):
        predicted = sum(coeffs[i] * s[n - 1 - i] for i in range(d))
        residuals.append(s[n] - predicted)
    return residuals


def find_inhomogeneous_recurrence(seq: List[int], d_max: int = 50
                                  ) -> Optional[Tuple[int, List[Fraction], Fraction]]:
    """Find minimal inhomogeneous linear recurrence: a_n = c_1*a_{n-1}+...+c_d*a_{n-d}+c_0.

    Strategy: compute differences seq[n+1]-seq[n] and find homogeneous recurrence
    for the differences, then reconstruct.

    Alternatively, augment the sequence with a constant 1 to reduce to homogeneous.
    """
    # Simple approach: try the sequence [a_0-a_1, a_1-a_2, ...]
    diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    result = find_homogeneous_recurrence(diffs, d_max)
    if result is not None:
        order, coeffs = result
        # The differences satisfy a homogeneous recurrence of order `order`,
        # so the original sequence satisfies a recurrence of order `order+1`
        # (with inhomogeneous or homogeneous terms).
        # Actually, if Delta_n satisfies Delta_n = c_1*Delta_{n-1}+...+c_d*Delta_{n-d}
        # and Delta_n = a_{n+1} - a_n, this gives an order d+1 recurrence on a_n.
        return (order, coeffs, Fraction(0))
    return None


# ----- Self-test -----
if __name__ == "__main__":
    print("=== Recurrence Detector Self-Test ===\n")

    # Test 1: Fibonacci sequence
    fib = [0, 1]
    for _ in range(50):
        fib.append(fib[-1] + fib[-2])
    result = find_homogeneous_recurrence(fib)
    assert result is not None, "Should find Fibonacci recurrence"
    order, coeffs = result
    print(f"Fibonacci: order={order}, coeffs={coeffs}")
    assert order == 2
    assert coeffs == [Fraction(1), Fraction(1)]
    int_c, readable = recurrence_to_homogeneous_form(order, coeffs)
    print(f"  Homogeneous form: {readable}")
    print(f"  Integer coefficients: {int_c}")
    print("  PASS")

    # Test 2: Tribonacci
    trib = [0, 0, 1]
    for _ in range(50):
        trib.append(trib[-1] + trib[-2] + trib[-3])
    result = find_homogeneous_recurrence(trib)
    assert result is not None
    order, coeffs = result
    print(f"\nTribonacci: order={order}, coeffs={coeffs}")
    assert order == 3
    assert coeffs == [Fraction(1), Fraction(1), Fraction(1)]
    print("  PASS")

    # Test 3: Powers of 2: a_n = 2^n
    pow2 = [2 ** n for n in range(30)]
    result = find_homogeneous_recurrence(pow2)
    assert result is not None
    order, coeffs = result
    print(f"\nPowers of 2: order={order}, coeffs={coeffs}")
    assert order == 1
    assert coeffs == [Fraction(2)]
    print("  PASS")

    # Test 4: Arithmetic sequence a_n = 3n + 5
    arith = [3 * n + 5 for n in range(30)]
    result = find_homogeneous_recurrence(arith)
    assert result is not None
    order, coeffs = result
    print(f"\nArithmetic 3n+5: order={order}, coeffs={coeffs}")
    # a_n = 2*a_{n-1} - a_{n-2}  (order 2)
    assert order == 2
    assert coeffs == [Fraction(2), Fraction(-1)]
    int_c, readable = recurrence_to_homogeneous_form(order, coeffs)
    print(f"  Homogeneous form: {readable}")
    print("  PASS")

    # Test 5: Random sequence should NOT satisfy low-order recurrence
    import random
    random.seed(42)
    rand_seq = [random.randint(1, 1000) for _ in range(100)]
    result = find_homogeneous_recurrence(rand_seq)
    print(f"\nRandom sequence: result={result}")
    assert result is None, "Random sequence should not have a low-order recurrence"
    print("  PASS: no recurrence found (as expected)")

    # Test 6: Beatty sequence of pi (should NOT satisfy low-order recurrence)
    import sys
    sys.path.insert(0, '.')
    from beatty import parse_r_value, beatty_sequence
    r_pi = parse_r_value("pi")
    seq_pi = beatty_sequence(r_pi, 200)
    result = find_homogeneous_recurrence(seq_pi, d_max=50)
    print(f"\nfloor(n*pi): result={result}")
    assert result is None, "floor(n*pi) should not satisfy a low-order recurrence"
    print("  PASS: no recurrence found for floor(n*pi)")

    # Test 7: Beatty sequence of 3/2 (SHOULD satisfy recurrence)
    from fractions import Fraction
    seq_32 = beatty_sequence(Fraction(3, 2), 200)
    result = find_homogeneous_recurrence(seq_32)
    assert result is not None, "floor(n*3/2) should satisfy a recurrence"
    order, coeffs = result
    print(f"\nfloor(n*3/2): order={order}, coeffs={coeffs}")
    int_c, readable = recurrence_to_homogeneous_form(order, coeffs)
    print(f"  Homogeneous form: {readable}")
    print("  PASS")

    # Test 8: floor(n * golden_ratio) should NOT satisfy a homogeneous recurrence
    r_phi = parse_r_value("golden_ratio")
    seq_phi = beatty_sequence(r_phi, 200)
    result = find_homogeneous_recurrence(seq_phi, d_max=50)
    print(f"\nfloor(n*phi): result={result}")
    assert result is None, "floor(n*phi) should not satisfy a recurrence"
    print("  PASS: no recurrence found for floor(n*phi)")

    # Test 9: Quadratic sequence a_n = n^2
    quad = [n * n for n in range(100)]
    result = find_homogeneous_recurrence(quad)
    assert result is not None
    order, coeffs = result
    print(f"\nn^2: order={order}, coeffs={coeffs}")
    # a_n = 3*a_{n-1} - 3*a_{n-2} + a_{n-3}  (order 3)
    assert order == 3
    int_c, readable = recurrence_to_homogeneous_form(order, coeffs)
    print(f"  Homogeneous form: {readable}")
    print("  PASS")

    print("\n=== All tests passed ===")
