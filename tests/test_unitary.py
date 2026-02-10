"""Tests for src/unitary.py."""

import pytest
from src.unitary import (
    is_unitary_divisor,
    unitary_divisors,
    sigma_star,
    is_unitary_perfect,
    KNOWN_UPNS,
    KNOWN_UPN_FACTORIZATIONS,
)


class TestIsUnitaryDivisor:
    def test_basic_cases(self):
        # 1 is always a unitary divisor
        assert is_unitary_divisor(1, 12) is True
        # n is always a unitary divisor of itself
        assert is_unitary_divisor(12, 12) is True

    def test_unitary_divisors_of_12(self):
        # 12 = 2^2 * 3. Unitary divisors: 1, 4, 3, 12
        assert is_unitary_divisor(1, 12) is True
        assert is_unitary_divisor(4, 12) is True
        assert is_unitary_divisor(3, 12) is True
        assert is_unitary_divisor(12, 12) is True
        # Non-unitary divisors: 2, 6
        assert is_unitary_divisor(2, 12) is False
        assert is_unitary_divisor(6, 12) is False

    def test_non_divisor(self):
        assert is_unitary_divisor(5, 12) is False

    def test_invalid_inputs(self):
        assert is_unitary_divisor(0, 12) is False
        assert is_unitary_divisor(-1, 12) is False


class TestUnitaryDivisors:
    def test_prime(self):
        assert unitary_divisors(7) == [1, 7]

    def test_prime_power(self):
        # 8 = 2^3, unitary divisors are 1 and 8
        assert unitary_divisors(8) == [1, 8]

    def test_12(self):
        # 12 = 2^2 * 3, unitary divisors: {1, 3, 4, 12}
        assert unitary_divisors(12) == [1, 3, 4, 12]

    def test_60(self):
        # 60 = 2^2 * 3 * 5, unitary divisors: subsets of {4, 3, 5}
        expected = sorted([1, 4, 3, 5, 12, 20, 15, 60])
        assert unitary_divisors(60) == expected

    def test_one(self):
        assert unitary_divisors(1) == [1]

    def test_count_is_power_of_two(self):
        # Number of unitary divisors = 2^omega(n)
        from sympy import factorint
        for n in [6, 30, 60, 210, 2310]:
            k = len(factorint(n))
            assert len(unitary_divisors(n)) == 2 ** k


class TestSigmaStar:
    def test_prime(self):
        assert sigma_star(7) == 8  # 1 + 7

    def test_prime_power(self):
        assert sigma_star(8) == 9  # 1 + 8

    def test_known_values(self):
        assert sigma_star(1) == 1
        assert sigma_star(6) == 12  # (1+2)(1+3) = 12
        assert sigma_star(12) == 20  # (1+4)(1+3) = 20

    def test_multiplicativity(self):
        from math import gcd
        pairs = [(3, 4), (5, 7), (8, 9), (11, 13)]
        for a, b in pairs:
            assert gcd(a, b) == 1
            assert sigma_star(a * b) == sigma_star(a) * sigma_star(b)


class TestIsUnitaryPerfect:
    def test_known_upns(self):
        for n in KNOWN_UPNS:
            assert is_unitary_perfect(n) is True, f"{n} should be UPN"

    def test_non_upns(self):
        non_upns = [1, 2, 3, 4, 5, 7, 8, 10, 12, 15, 28, 100, 496, 1000]
        for n in non_upns:
            assert is_unitary_perfect(n) is False, f"{n} should not be UPN"

    def test_small_range(self):
        # Only 6 should be UPN in [1, 10]
        upns_found = [n for n in range(1, 11) if is_unitary_perfect(n)]
        assert upns_found == [6]

    def test_medium_range(self):
        # In [1, 100], only 6, 60, 90 are UPNs
        upns_found = [n for n in range(1, 101) if is_unitary_perfect(n)]
        assert upns_found == [6, 60, 90]


class TestKnownFactorizations:
    def test_factorizations_correct(self):
        from sympy import factorint
        for n, expected in KNOWN_UPN_FACTORIZATIONS.items():
            assert factorint(n) == expected

    def test_sigma_star_equals_2n(self):
        for n, fact in KNOWN_UPN_FACTORIZATIONS.items():
            product = 1
            for p, a in fact.items():
                product *= (1 + p ** a)
            assert product == 2 * n
