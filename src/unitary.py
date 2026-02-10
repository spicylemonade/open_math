"""Core functions for unitary divisors and unitary perfect numbers.

Implements the fundamental operations needed for studying unitary perfect
numbers: checking unitary divisibility, listing unitary divisors, computing
the unitary sigma function sigma*(n), and testing whether a number is
unitary perfect.
"""

from math import gcd
from sympy import factorint


def is_unitary_divisor(d, n):
    """Check whether d is a unitary divisor of n.

    A divisor d of n is unitary if gcd(d, n/d) = 1.

    Args:
        d: A positive integer that divides n.
        n: A positive integer.

    Returns:
        True if d divides n and gcd(d, n/d) == 1, False otherwise.
    """
    if n <= 0 or d <= 0:
        return False
    if n % d != 0:
        return False
    return gcd(d, n // d) == 1


def unitary_divisors(n):
    """Return the list of all unitary divisors of n.

    Since the unitary divisors of n = p1^a1 * ... * pk^ak are exactly
    the products of subsets of {p1^a1, ..., pk^ak}, there are 2^k of them.

    Args:
        n: A positive integer.

    Returns:
        Sorted list of all unitary divisors of n.
    """
    if n <= 0:
        return []
    if n == 1:
        return [1]

    factorization = factorint(n)
    prime_powers = [p ** a for p, a in factorization.items()]

    # Generate all subsets of prime powers
    divisors = [1]
    for pp in prime_powers:
        divisors = divisors + [d * pp for d in divisors]

    return sorted(divisors)


def sigma_star(n):
    """Compute sigma*(n), the sum of unitary divisors of n.

    Uses the multiplicative formula: sigma*(n) = prod_{p^a || n} (1 + p^a).

    Args:
        n: A positive integer.

    Returns:
        The sum of all unitary divisors of n.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return 1

    factorization = factorint(n)
    result = 1
    for p, a in factorization.items():
        result *= (1 + p ** a)
    return result


def is_unitary_perfect(n):
    """Check whether n is a unitary perfect number.

    n is unitary perfect if sigma*(n) = 2n, equivalently if the sum of
    its proper unitary divisors equals n.

    Args:
        n: A positive integer.

    Returns:
        True if n is a unitary perfect number, False otherwise.
    """
    if n <= 1:
        return False
    return sigma_star(n) == 2 * n


# The five known unitary perfect numbers
KNOWN_UPNS = [6, 60, 90, 87360, 146361946186458562560000]

# Their prime factorizations
KNOWN_UPN_FACTORIZATIONS = {
    6: {2: 1, 3: 1},
    60: {2: 2, 3: 1, 5: 1},
    90: {2: 1, 3: 2, 5: 1},
    87360: {2: 6, 3: 1, 5: 1, 7: 1, 13: 1},
    146361946186458562560000: {
        2: 18, 3: 1, 5: 4, 7: 1, 11: 1, 13: 1,
        19: 1, 37: 1, 79: 1, 109: 1, 157: 1, 313: 1
    },
}
