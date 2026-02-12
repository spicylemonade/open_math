"""Tests for n-dimensional geometry module."""
import math
import sys
sys.path.insert(0, '/home/codex/work/repo/src')

from ndim_geometry import V_n_gamma, V_n_recurrence, V_n, S_n, cap_area, cap_solid_angle


def test_V3():
    """V_3(1) = 4*pi/3."""
    expected = 4.0 * math.pi / 3.0
    assert abs(V_n(3, 1.0) - expected) < 1e-12, f"V_3(1) = {V_n(3)} != {expected}"
    print("PASS: V_3(1) = 4*pi/3")


def test_V5():
    """V_5(1) = 8*pi^2/15."""
    expected = 8.0 * math.pi**2 / 15.0
    assert abs(V_n(5, 1.0) - expected) < 1e-12, f"V_5(1) = {V_n(5)} != {expected}"
    print("PASS: V_5(1) = 8*pi^2/15")


def test_S4():
    """S_4(1) = 8*pi^2/3."""
    expected = 8.0 * math.pi**2 / 3.0
    assert abs(S_n(5, 1.0) - expected) < 1e-12, f"S_4(1) = {S_n(5)} != {expected}"
    print("PASS: S_4(1) = 8*pi^2/3")


def test_recurrence_matches_gamma():
    """Recurrence V_n = (2*pi/n)*V_{n-2} matches Gamma formula to 1e-12 for n=1..20."""
    for n in range(1, 21):
        gamma_val = V_n_gamma(n, 1.0)
        recur_val = V_n_recurrence(n, 1.0)
        diff = abs(gamma_val - recur_val)
        assert diff < 1e-12, f"n={n}: Gamma={gamma_val}, Recur={recur_val}, diff={diff}"
    print("PASS: Recurrence matches Gamma formula for n=1..20")


def test_cap_area_3_pi6():
    """cap_area(3, pi/6) = 2*pi*(1 - cos(pi/6))."""
    theta = math.pi / 6.0
    expected = 2.0 * math.pi * (1.0 - math.cos(theta))
    computed = cap_area(3, theta)
    assert abs(computed - expected) < 1e-8, f"cap_area(3, pi/6) = {computed} != {expected}"
    print("PASS: cap_area(3, pi/6) matches known value")


def test_derivative_relationship():
    """d/dR[V_n(R)] = S_{n-1}(R) numerically."""
    eps = 1e-8
    R = 1.0
    for n in range(2, 11):
        dVdR = (V_n(n, R + eps) - V_n(n, R - eps)) / (2 * eps)
        S = S_n(n, R)
        assert abs(dVdR - S) < 1e-4, f"n={n}: dV/dR={dVdR}, S={S}"
    print("PASS: d/dR[V_n] = S_{n-1} for n=2..10")


def test_cap_solid_angle_hemisphere():
    """Cap of half-angle pi/2 (hemisphere) should be 0.5."""
    for n in [3, 4, 5, 6]:
        frac = cap_solid_angle(n, math.pi / 2.0)
        assert abs(frac - 0.5) < 1e-8, f"n={n}: hemisphere fraction = {frac}"
    print("PASS: Hemisphere cap fraction = 0.5")


if __name__ == '__main__':
    test_V3()
    test_V5()
    test_S4()
    test_recurrence_matches_gamma()
    test_cap_area_3_pi6()
    test_derivative_relationship()
    test_cap_solid_angle_hemisphere()
    print("\nAll tests passed!")
