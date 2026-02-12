"""
N-dimensional ball volume, surface area, and spherical cap geometry.

Implements the dimensional analysis framework:
  - V_n(R): volume of n-ball of radius R
  - S_n(R): surface area of (n-1)-sphere
  - cap_area(n, theta): area of spherical cap
  - cap_solid_angle(n, theta): fractional area of cap
"""
import math
from scipy import special


def V_n_gamma(n, R=1.0):
    """Volume of n-ball of radius R using Gamma function formula.

    V_n(R) = pi^(n/2) / Gamma(n/2 + 1) * R^n
    """
    return (math.pi ** (n / 2.0)) / math.gamma(n / 2.0 + 1) * (R ** n)


def V_n_recurrence(n, R=1.0):
    """Volume of n-ball via 2-step recurrence: V_n = (2*pi/n)*R^2*V_{n-2}.

    Base cases: V_0 = 1, V_1 = 2R.
    """
    if n == 0:
        return 1.0
    if n == 1:
        return 2.0 * R
    return (2.0 * math.pi / n) * (R ** 2) * V_n_recurrence(n - 2, R)


def V_n(n, R=1.0):
    """Volume of n-ball (default: Gamma formula)."""
    return V_n_gamma(n, R)


def S_n(n, R=1.0):
    """Surface area of (n-1)-sphere bounding an n-ball of radius R.

    S_{n-1}(R) = 2 * pi^(n/2) / Gamma(n/2) * R^(n-1)

    Equivalently, S_{n-1}(R) = d/dR[V_n(R)] = n * V_n(R) / R.
    """
    if n == 1:
        return 2.0  # two points
    return 2.0 * (math.pi ** (n / 2.0)) / math.gamma(n / 2.0) * (R ** (n - 1))


def cap_area(n, theta):
    """Area of spherical cap of half-angle theta on S^{n-1} (unit sphere in R^n).

    A_cap = S_{n-1}/2 * I_{sin^2(theta)}((n-1)/2, 1/2)

    where I_x(a,b) is the regularized incomplete beta function.

    Derived via dimensional integration of S^{n-2} cross-sections.
    """
    if n < 2:
        raise ValueError("cap_area requires n >= 2")
    S = S_n(n, 1.0)
    x = math.sin(theta) ** 2
    a = (n - 1) / 2.0
    b = 0.5
    return S / 2.0 * float(special.betainc(a, b, x))


def cap_solid_angle(n, theta):
    """Fractional area of spherical cap: cap_area / total_surface_area.

    Returns a value in [0, 1].
    """
    S = S_n(n, 1.0)
    return cap_area(n, theta) / S


def cap_packing_bound(n, min_angle=None):
    """Simple upper bound on kissing number: tau_n <= S_{n-1} / A_cap(n, theta).

    For kissing number, the exclusion half-angle is pi/6 (each touching sphere
    subtends a cap of half-angle pi/6 on the central sphere, and these caps
    cannot overlap if minimum angular separation between centers is pi/3 = 60 deg).

    Args:
        n: dimension
        min_angle: minimum angular separation (default: pi/3 for kissing number)

    Returns:
        float upper bound (not floored to integer)
    """
    if min_angle is None:
        min_angle = math.pi / 3.0
    half_angle = min_angle / 2.0
    A = cap_area(n, half_angle)
    S = S_n(n, 1.0)
    return S / A
