"""Tests for src/abundance.py."""

import pytest
from fractions import Fraction

from src.abundance import (
    unitary_abundance_ratio,
    unitary_abundance_ratio_exact,
    prime_power_contribution,
    prime_power_contribution_exact,
    required_product_from_factorization,
    required_product_exact,
    remaining_product_needed,
    remaining_product_needed_exact,
)
from src.unitary import KNOWN_UPNS, KNOWN_UPN_FACTORIZATIONS


class TestUnitaryAbundanceRatio:
    def test_known_upns_ratio_is_one(self):
        for n in KNOWN_UPNS:
            ratio = unitary_abundance_ratio(n)
            assert abs(ratio - 1.0) < 1e-10, f"Ratio for {n} should be 1.0, got {ratio}"

    def test_known_upns_exact_ratio(self):
        for n in KNOWN_UPNS:
            ratio = unitary_abundance_ratio_exact(n)
            assert ratio == Fraction(1), f"Exact ratio for {n} should be 1, got {ratio}"

    def test_non_upns(self):
        for n in [2, 3, 4, 5, 10, 12, 28, 100]:
            ratio = unitary_abundance_ratio(n)
            assert ratio != 1.0, f"Ratio for {n} should not be 1.0"


class TestPrimePowerContribution:
    def test_small_primes(self):
        assert prime_power_contribution(2, 1) == 1.5  # 3/2
        assert prime_power_contribution(3, 1) == pytest.approx(4 / 3)
        assert prime_power_contribution(5, 1) == 1.2  # 6/5

    def test_higher_powers(self):
        assert prime_power_contribution(2, 2) == 1.25  # 5/4
        assert prime_power_contribution(2, 6) == pytest.approx(65 / 64)

    def test_exact(self):
        assert prime_power_contribution_exact(2, 1) == Fraction(3, 2)
        assert prime_power_contribution_exact(3, 2) == Fraction(10, 9)


class TestRequiredProduct:
    def test_known_upn_factorizations(self):
        for n, fact in KNOWN_UPN_FACTORIZATIONS.items():
            product = required_product_from_factorization(fact)
            assert abs(product - 2.0) < 1e-10, f"Product for {n} should be 2.0, got {product}"

    def test_exact_product(self):
        for n, fact in KNOWN_UPN_FACTORIZATIONS.items():
            product = required_product_exact(fact)
            assert product == Fraction(2), f"Exact product for {n} should be 2, got {product}"


class TestRemainingProduct:
    def test_empty_factorization(self):
        assert remaining_product_needed({}) == 2.0

    def test_partial(self):
        # With just {2: 1}, product is 3/2, remaining is 2/(3/2) = 4/3
        remaining = remaining_product_needed({2: 1})
        assert abs(remaining - 4 / 3) < 1e-10

    def test_exact_partial(self):
        remaining = remaining_product_needed_exact({2: 1})
        assert remaining == Fraction(4, 3)

    def test_complete_factorization(self):
        # For a complete UPN factorization, remaining should be 1
        for n, fact in KNOWN_UPN_FACTORIZATIONS.items():
            remaining = remaining_product_needed_exact(fact)
            assert remaining == Fraction(1), f"Remaining for {n} should be 1, got {remaining}"
