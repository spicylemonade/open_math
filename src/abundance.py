"""Abundance ratio analysis toolkit for unitary perfect numbers.

Provides tools for analyzing the ratio sigma*(n)/(2n) and the product
equation prod(1 + 1/p_i^{a_i}) = 2 that characterizes unitary perfect numbers.
"""

from math import prod as math_prod
from sympy import factorint
from fractions import Fraction

from src.unitary import sigma_star


def unitary_abundance_ratio(n):
    """Compute sigma*(n) / (2n), the unitary abundance ratio.

    For a unitary perfect number, this equals exactly 1.0.

    Args:
        n: A positive integer.

    Returns:
        Float value of sigma*(n) / (2n).
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    return sigma_star(n) / (2 * n)


def unitary_abundance_ratio_exact(n):
    """Compute sigma*(n) / (2n) as an exact Fraction.

    Args:
        n: A positive integer.

    Returns:
        Fraction value of sigma*(n) / (2n).
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    return Fraction(sigma_star(n), 2 * n)


def prime_power_contribution(p, a):
    """Compute the contribution of prime power p^a to the product equation.

    Returns (1 + p^a) / p^a = 1 + 1/p^a.

    Args:
        p: A prime number.
        a: A positive integer exponent.

    Returns:
        Float value of 1 + 1/p^a.
    """
    pa = p ** a
    return (1 + pa) / pa


def prime_power_contribution_exact(p, a):
    """Compute the contribution of prime power p^a as an exact Fraction.

    Returns (1 + p^a) / p^a as a Fraction.

    Args:
        p: A prime number.
        a: A positive integer exponent.

    Returns:
        Fraction(1 + p^a, p^a).
    """
    pa = p ** a
    return Fraction(1 + pa, pa)


def required_product_from_factorization(factorization):
    """Compute prod(1 + 1/p_i^{a_i}) for a given factorization.

    For a unitary perfect number, this product equals exactly 2.

    Args:
        factorization: Dict mapping prime p to exponent a.

    Returns:
        Float value of the product.
    """
    result = 1.0
    for p, a in factorization.items():
        result *= prime_power_contribution(p, a)
    return result


def required_product_exact(factorization):
    """Compute prod(1 + 1/p_i^{a_i}) as an exact Fraction.

    Args:
        factorization: Dict mapping prime p to exponent a.

    Returns:
        Fraction value of the product.
    """
    result = Fraction(1)
    for p, a in factorization.items():
        result *= prime_power_contribution_exact(p, a)
    return result


def remaining_product_needed(partial_factorization):
    """Given a partial factorization, return the remaining product needed to reach 2.

    If the partial product already exceeds 2, returns a value less than 1.

    Args:
        partial_factorization: Dict mapping prime p to exponent a (subset of full factorization).

    Returns:
        Float value of 2 / prod(1 + 1/p_i^{a_i}) for the given primes.
    """
    current_product = required_product_from_factorization(partial_factorization)
    if current_product == 0:
        return float('inf')
    return 2.0 / current_product


def remaining_product_needed_exact(partial_factorization):
    """Given a partial factorization, return the remaining product needed as exact Fraction.

    Args:
        partial_factorization: Dict mapping prime p to exponent a.

    Returns:
        Fraction value of 2 / prod(1 + 1/p_i^{a_i}).
    """
    current_product = required_product_exact(partial_factorization)
    if current_product == 0:
        return None
    return Fraction(2) / current_product
