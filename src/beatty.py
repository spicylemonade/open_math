"""
Beatty sequence computation module.

Computes floor(n*r) for arbitrary real r, supporting:
- Exact rational arithmetic
- High-precision irrational computation via mpmath
- Subsequence extraction along arithmetic progressions and arbitrary index sets

References:
  - Beatty (1926), "Problem 3173", Amer. Math. Monthly
  - Fraenkel (1969), "The bracket function and complementary sets of integers"
"""

from fractions import Fraction
from typing import List, Optional, Sequence, Tuple, Union
import math

try:
    import mpmath
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False

# Standard constants
GOLDEN_RATIO_EXPR = "golden_ratio"
SQRT2_EXPR = "sqrt(2)"
SQRT3_EXPR = "sqrt(3)"
SQRT5_EXPR = "sqrt(5)"
PI_EXPR = "pi"
E_EXPR = "e"


def _ensure_mpmath(precision: int = 50):
    """Ensure mpmath is available and set precision."""
    if not HAS_MPMATH:
        raise ImportError("mpmath is required for irrational number computation")
    mpmath.mp.dps = precision


def parse_r_value(r_spec: str, precision: int = 50) -> Union[Fraction, 'mpmath.mpf']:
    """Parse a string specification of r into a numeric value.

    Supports:
      - Fractions: "3/2", "5/3", "7/4"
      - Named constants: "golden_ratio", "sqrt(2)", "pi", "e"
      - Expressions: "sqrt(D)" for any integer D
      - Float strings: "1.41421356..."
    """
    r_spec = r_spec.strip()

    # Try fraction first
    if '/' in r_spec and not r_spec.startswith('sqrt'):
        parts = r_spec.split('/')
        if len(parts) == 2:
            try:
                return Fraction(int(parts[0]), int(parts[1]))
            except (ValueError, ZeroDivisionError):
                pass

    # Try integer
    try:
        val = int(r_spec)
        return Fraction(val, 1)
    except ValueError:
        pass

    # Named constants and expressions (need mpmath)
    _ensure_mpmath(precision)

    if r_spec == "golden_ratio" or r_spec == "phi":
        return (1 + mpmath.sqrt(5)) / 2
    elif r_spec == "pi":
        return mpmath.pi
    elif r_spec == "e":
        return mpmath.e
    elif r_spec == "ln2" or r_spec == "ln(2)":
        return mpmath.log(2)
    elif r_spec.startswith("sqrt(") and r_spec.endswith(")"):
        d = int(r_spec[5:-1])
        return mpmath.sqrt(d)
    elif r_spec.startswith("cbrt(") and r_spec.endswith(")"):
        d = int(r_spec[5:-1])
        return mpmath.cbrt(d)
    elif r_spec.startswith("root(") and r_spec.endswith(")"):
        # root(base,degree) e.g. root(2,4) = 2^(1/4)
        inner = r_spec[5:-1]
        parts = inner.split(',')
        base, degree = int(parts[0]), int(parts[1])
        return mpmath.power(base, mpmath.mpf(1) / degree)
    else:
        # Try as float
        try:
            return mpmath.mpf(r_spec)
        except Exception:
            raise ValueError(f"Cannot parse r specification: {r_spec}")


def beatty_sequence(r: Union[Fraction, float, 'mpmath.mpf'], N: int,
                    start: int = 1) -> List[int]:
    """Compute the Beatty sequence floor(n*r) for n = start, start+1, ..., start+N-1.

    Args:
        r: The real number r > 0
        N: Number of terms to compute
        start: Starting index (default 1)

    Returns:
        List of integers [floor(start*r), floor((start+1)*r), ..., floor((start+N-1)*r)]
    """
    result = []
    if isinstance(r, Fraction):
        # Exact rational arithmetic
        p, q = r.numerator, r.denominator
        for n in range(start, start + N):
            result.append((n * p) // q)
    else:
        # For speed: convert mpmath to Python float and use math.floor
        # Python float has 53-bit mantissa, good for n*r up to ~2^53
        if HAS_MPMATH and isinstance(r, mpmath.mpf):
            r_float = float(r)
            max_n = start + N - 1
            # Check if Python float precision is sufficient
            if max_n * abs(r_float) < 2**50:
                for n in range(start, start + N):
                    result.append(math.floor(n * r_float))
                # Spot-check with mpmath
                _ensure_mpmath(30)
                for check_n in [start, start + N // 3, start + 2 * N // 3, max_n]:
                    exact = int(mpmath.floor(check_n * r))
                    idx = check_n - start
                    if idx < len(result) and result[idx] != exact:
                        # Precision loss - fall back to mpmath
                        result = []
                        for n in range(start, start + N):
                            result.append(int(mpmath.floor(n * r)))
                        break
            else:
                _ensure_mpmath(30)
                for n in range(start, start + N):
                    result.append(int(mpmath.floor(n * r)))
        else:
            for n in range(start, start + N):
                result.append(math.floor(n * float(r)))
    return result


def first_differences(seq: List[int]) -> List[int]:
    """Compute first differences: Delta(n) = seq[n+1] - seq[n]."""
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


def subsequence_arithmetic(seq: List[int], offset: int, stride: int) -> List[int]:
    """Extract subsequence along arithmetic progression.

    Returns [seq[offset], seq[offset+stride], seq[offset+2*stride], ...]

    Args:
        seq: The base sequence (0-indexed)
        offset: Starting offset (0-indexed)
        stride: Common difference

    Returns:
        Extracted subsequence
    """
    return [seq[i] for i in range(offset, len(seq), stride)]


def subsequence_by_indices(seq: List[int], indices: Sequence[int]) -> List[int]:
    """Extract subsequence at arbitrary indices.

    Args:
        seq: The base sequence (0-indexed)
        indices: List of indices to extract (0-indexed)

    Returns:
        Extracted subsequence
    """
    return [seq[i] for i in indices if i < len(seq)]


def continued_fraction(r: Union[Fraction, float, 'mpmath.mpf'],
                       max_terms: int = 50) -> List[int]:
    """Compute the continued fraction expansion of r.

    Returns the first max_terms partial quotients [a_0; a_1, a_2, ...].
    """
    cf = []
    if isinstance(r, Fraction):
        # Exact for rationals
        a, b = r.numerator, r.denominator
        while b != 0 and len(cf) < max_terms:
            q, rem = divmod(a, b)
            cf.append(q)
            a, b = b, rem
        return cf

    # For irrationals, use mpmath precision
    if HAS_MPMATH:
        _ensure_mpmath(100)
        x = mpmath.mpf(r)
        for _ in range(max_terms):
            a = int(mpmath.floor(x))
            cf.append(a)
            frac = x - a
            if frac < mpmath.mpf('1e-30'):
                break
            x = 1 / frac
    else:
        x = float(r)
        for _ in range(max_terms):
            a = math.floor(x)
            cf.append(a)
            frac = x - a
            if frac < 1e-12:
                break
            x = 1.0 / frac
    return cf


def classify_r(r_spec: str) -> str:
    """Classify r into one of the 4 taxonomy classes.

    Returns one of: 'rational', 'quadratic_irrational', 'algebraic_degree_ge3', 'transcendental'
    """
    r_spec = r_spec.strip()

    # Rationals
    if '/' in r_spec and not r_spec.startswith('sqrt'):
        return 'rational'
    try:
        int(r_spec)
        return 'rational'
    except ValueError:
        pass

    # Quadratic irrationals
    if r_spec in ("golden_ratio", "phi"):
        return 'quadratic_irrational'
    if r_spec.startswith("sqrt("):
        return 'quadratic_irrational'

    # Higher algebraic
    if r_spec.startswith("cbrt(") or r_spec.startswith("root("):
        return 'algebraic_degree_ge3'

    # Transcendentals
    if r_spec in ("pi", "e", "ln2", "ln(2)"):
        return 'transcendental'

    return 'unknown'


# ----- Self-test -----
if __name__ == "__main__":
    print("=== Beatty Sequence Module Self-Test ===\n")

    # Test 1: Rational r = 3/2
    r = Fraction(3, 2)
    seq = beatty_sequence(r, 20)
    print(f"r = 3/2: {seq}")
    expected = [1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18, 19, 21, 22, 24, 25, 27, 28, 30]
    assert seq == expected, f"Mismatch for r=3/2: got {seq}"
    print("  PASS: matches expected values")

    # Test 2: Golden ratio (lower Wythoff sequence A000201)
    r_phi = parse_r_value("golden_ratio")
    seq_phi = beatty_sequence(r_phi, 20)
    expected_phi = [1, 3, 4, 6, 8, 9, 11, 12, 14, 16, 17, 19, 21, 22, 24, 25, 27, 29, 30, 32]
    print(f"r = phi: {seq_phi}")
    assert seq_phi == expected_phi, f"Mismatch for golden_ratio: got {seq_phi}"
    print("  PASS: matches A000201")

    # Test 3: sqrt(2) (A001951)
    r_s2 = parse_r_value("sqrt(2)")
    seq_s2 = beatty_sequence(r_s2, 20)
    expected_s2 = [1, 2, 4, 5, 7, 8, 9, 11, 12, 14, 15, 16, 18, 19, 21, 22, 24, 25, 26, 28]
    print(f"r = sqrt(2): {seq_s2}")
    assert seq_s2 == expected_s2, f"Mismatch for sqrt(2): got {seq_s2}"
    print("  PASS: matches A001951")

    # Test 4: pi
    r_pi = parse_r_value("pi")
    seq_pi = beatty_sequence(r_pi, 10)
    expected_pi = [3, 6, 9, 12, 15, 18, 21, 25, 28, 31]
    print(f"r = pi: {seq_pi}")
    assert seq_pi == expected_pi, f"Mismatch for pi: got {seq_pi}"
    print("  PASS: matches expected values for pi")

    # Test 5: Continued fractions
    cf_phi = continued_fraction(r_phi, 20)
    print(f"\nCF(golden_ratio) = {cf_phi}")
    assert all(a == 1 for a in cf_phi), "Golden ratio CF should be all 1s"
    print("  PASS: all partial quotients are 1")

    cf_32 = continued_fraction(Fraction(3, 2), 10)
    print(f"CF(3/2) = {cf_32}")
    assert cf_32 == [1, 2], "CF(3/2) = [1; 2]"
    print("  PASS: CF(3/2) = [1; 2]")

    # Test 6: Subsequence extraction
    seq_full = beatty_sequence(Fraction(3, 2), 100)
    sub = subsequence_arithmetic(seq_full, 0, 2)  # every other term
    print(f"\nr=3/2, every other term (first 10): {sub[:10]}")
    print(f"  (These are floor((2k+1)*3/2) for k=0,1,...)")

    # Test 7: First differences
    diffs = first_differences(seq_full[:20])
    print(f"\nr=3/2, first differences: {diffs}")
    assert set(diffs) == {1, 2}, f"First diffs for r=3/2 should be {{1,2}}, got {set(diffs)}"
    print("  PASS: first differences are {1, 2}")

    # Test 8: Classification
    assert classify_r("3/2") == 'rational'
    assert classify_r("golden_ratio") == 'quadratic_irrational'
    assert classify_r("sqrt(5)") == 'quadratic_irrational'
    assert classify_r("cbrt(2)") == 'algebraic_degree_ge3'
    assert classify_r("pi") == 'transcendental'
    print("\nClassification tests: PASS")

    # Test 9: Large computation
    seq_large = beatty_sequence(r_phi, 10000)
    print(f"\nLarge test: computed {len(seq_large)} terms of floor(n*phi)")
    print(f"  First 5: {seq_large[:5]}, Last 5: {seq_large[-5:]}")
    assert len(seq_large) == 10000
    print("  PASS: 10000 terms computed")

    print("\n=== All tests passed ===")
