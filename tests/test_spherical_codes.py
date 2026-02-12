"""Tests for spherical code validator and optimizer."""
import numpy as np
import sys
sys.path.insert(0, '/home/codex/work/repo/src')

from spherical_codes import validate_kissing_config, greedy_spherical_code
from d5_lattice import generate_d5_vectors, normalize_vectors


def test_validate_d5():
    """D5 40-point configuration should be valid."""
    d5 = normalize_vectors(generate_d5_vectors())
    result = validate_kissing_config(d5)
    assert result['valid'], f"D5 config invalid: {result}"
    assert result['n_vectors'] == 40
    assert result['dimension'] == 5
    print("PASS: D5 configuration validated (40 vectors, dim 5)")


def test_reject_random_45():
    """Random 45-point configuration should be invalid."""
    rng = np.random.RandomState(42)
    vecs = rng.randn(45, 5)
    vecs = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
    result = validate_kissing_config(vecs)
    assert not result['valid'], "Random 45-point config should be invalid"
    assert result['n_angle_violations'] > 0
    print(f"PASS: Random 45-point config rejected ({result['n_angle_violations']} violations)")


def test_greedy_low_target():
    """Greedy should easily place a small number of points."""
    result = greedy_spherical_code(3, 6, seed=42)
    assert result['n_placed'] >= 6, f"Only placed {result['n_placed']}/6"
    print(f"PASS: Greedy placed {result['n_placed']} points in R^3 (target 6)")


def test_greedy_high_target():
    """Greedy cannot place 50 points in R^5 with 60-degree separation."""
    result = greedy_spherical_code(5, 50, n_attempts=3, seed=42)
    assert result['n_placed'] < 50, "Should not place 50 points"
    print(f"PASS: Greedy placed only {result['n_placed']}/50 in R^5")


if __name__ == '__main__':
    test_validate_d5()
    test_reject_random_45()
    test_greedy_low_target()
    test_greedy_high_target()
    print("\nAll tests passed!")
