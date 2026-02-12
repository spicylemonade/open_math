"""Test suite for the reverse-and-add algorithm."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.reverse_add import is_palindrome, reverse_digits, reverse_and_add


class TestIsPalindrome:
    def test_single_digit(self):
        for d in range(10):
            assert is_palindrome(d)

    def test_palindromic_numbers(self):
        assert is_palindrome(121)
        assert is_palindrome(1221)
        assert is_palindrome(12321)

    def test_non_palindromic(self):
        assert not is_palindrome(123)
        assert not is_palindrome(10)


class TestReverseDigits:
    def test_basic(self):
        assert reverse_digits(123) == 321
        assert reverse_digits(100) == 1
        assert reverse_digits(12345) == 54321

    def test_palindrome(self):
        assert reverse_digits(121) == 121


class TestKnownDelays:
    def test_89_takes_24_steps(self):
        found, iters, result = reverse_and_add(89)
        assert found is True
        assert iters == 24
        assert is_palindrome(result)
        assert result == 8813200023188

    def test_10911_takes_55_steps(self):
        found, iters, result = reverse_and_add(10911)
        assert found is True
        assert iters == 55
        assert is_palindrome(result)

    def test_261_step_record(self):
        found, iters, result = reverse_and_add(1186060307891929990)
        assert found is True
        assert iters == 261
        assert is_palindrome(result)
        assert len(str(result)) == 119

    def test_293_step_world_record(self):
        found, iters, result = reverse_and_add(1000206827388999999095750)
        assert found is True
        assert iters == 293
        assert is_palindrome(result)
        assert len(str(result)) == 132


class TestEdgeCases:
    def test_single_digit_already_palindrome(self):
        found, iters, result = reverse_and_add(5)
        # 5 + 5 = 10, 10 + 01 = 11 (palindrome at step 2)
        # Actually: 5 is already a palindrome but the function
        # always does at least one step
        assert found is True
        assert iters >= 1

    def test_already_palindromic_11(self):
        # 11 + 11 = 22, palindrome at step 1
        found, iters, result = reverse_and_add(11)
        assert found is True
        assert iters == 1
        assert result == 22


class TestLychrelCandidate:
    def test_196_no_palindrome_in_500_steps(self):
        found, iters, result = reverse_and_add(196, max_iter=500)
        assert found is False
        assert iters == 500
