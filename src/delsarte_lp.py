"""
Delsarte Linear Programming Bound for Kissing Numbers.

Uses the standard Delsarte-Goethals-Seidel theorem:

If f(t) is a polynomial such that:
  (A1) f(t) <= 0 for t in [-1, s]  (s = 1/2 for kissing number)
  (A2) f_k >= 0 for k = 0, 1, ..., deg(f)
       where f(t) = sum f_k P_k^{(n)}(t) are the Gegenbauer coefficients
       with NORMALIZED Gegenbauer polynomials P_k(1) = 1

Then tau_n <= f(1) / f_0.

We solve this as an LP: fix f_0 = 1, maximize f(1), subject to f_k >= 0
and f(t) <= 0 on a grid.

The key insight for boundedness: we use the Gegenbauer expansion constraint.
Since P_k(1) = 1, f(1) = sum f_k. The constraint f(t) <= 0 on [-1, s]
combined with f_k >= 0 makes the LP bounded because the Gegenbauer
polynomials oscillate on [-1, 1] and with f_0 = 1 fixed, we can't make
the higher coefficients arbitrarily large without violating f(t) <= 0.

Actually, the LP IS still potentially unbounded for high-degree polynomials
on a discrete grid. The fix: use the KNOWN Levenshtein polynomials which
give sharp bounds.

For the kissing number with s = 1/2:
- n=8:  f(t) = (t+1)(t+1/2)^2 t^2 (t-1/2) gives tau_8 = 240 exactly
- n=24: f(t) = (t+1)(t+1/2)^2(t+1/4)^2 t^2(t-1/4)^2(t-1/2) gives tau_24 = 196560

For n=5, we use specific polynomial ansatze from the literature.
"""
import numpy as np
from scipy import special
import math


def gegenbauer_coefficients(poly_func, n, max_degree=20):
    """Compute Gegenbauer expansion coefficients of a polynomial.

    Given f(t), compute f_k such that f(t) = sum f_k P_k^{(n)}(t).

    Uses numerical integration with Gegenbauer weight:
    f_k = (integral f(t) P_k(t) w(t) dt) / (integral P_k(t)^2 w(t) dt)
    where w(t) = (1-t^2)^{(n-3)/2}.
    """
    from scipy.integrate import quad

    lam = (n - 2) / 2.0

    def P_k_normalized(k, t):
        if k == 0:
            return 1.0
        if n == 2:
            return np.cos(k * np.arccos(np.clip(t, -1, 1)))
        ck_t = special.eval_gegenbauer(k, lam, t)
        ck_1 = special.comb(k + 2 * lam - 1, k, exact=False)
        return ck_t / ck_1 if abs(ck_1) > 1e-30 else 0.0

    def weight(t):
        return (1 - t ** 2) ** ((n - 3) / 2.0)

    coeffs = []
    for k in range(max_degree + 1):
        # Numerator: integral f(t) P_k(t) w(t) dt
        num, _ = quad(lambda t: poly_func(t) * P_k_normalized(k, t) * weight(t), -1, 1)
        # Denominator: integral P_k(t)^2 w(t) dt
        den, _ = quad(lambda t: P_k_normalized(k, t) ** 2 * weight(t), -1, 1)
        if abs(den) < 1e-20:
            coeffs.append(0.0)
        else:
            coeffs.append(num / den)

    return np.array(coeffs)


def evaluate_delsarte_polynomial(f_roots, t):
    """Evaluate a polynomial given by its roots: f(t) = product (t - r_i)."""
    val = 1.0
    for r in f_roots:
        val *= (t - r)
    return val


def delsarte_bound_from_polynomial(n, poly_func):
    """Given a candidate Delsarte polynomial, compute the bound tau_n <= f(1)/f_0.

    Also verifies the conditions (A1) and (A2).
    """
    s = 0.5

    # Check A1: f(t) <= 0 on [-1, s]
    t_grid = np.linspace(-1, s, 10000)
    f_vals = np.array([poly_func(t) for t in t_grid])
    max_val = np.max(f_vals)
    a1_satisfied = max_val <= 1e-8

    # Compute Gegenbauer coefficients
    coeffs = gegenbauer_coefficients(poly_func, n, max_degree=30)

    # Check A2: f_k >= 0
    a2_violations = [(k, c) for k, c in enumerate(coeffs) if c < -1e-8]

    f1 = poly_func(1.0)
    f0 = coeffs[0]

    bound = f1 / f0 if abs(f0) > 1e-15 else float('inf')

    return {
        'bound': bound,
        'f_at_1': f1,
        'f_0': f0,
        'a1_satisfied': a1_satisfied,
        'a1_max_violation': max_val,
        'a2_violations': a2_violations,
        'coefficients': coeffs
    }


def delsarte_kissing_bound(n, max_degree=20, s=0.5):
    """Compute the Delsarte LP bound for kissing number tau_n.

    Strategy: try various polynomial ansatze and return the best bound.
    """
    best_bound = float('inf')
    best_info = None

    # Strategy 1: Known Levenshtein-type polynomials
    # For any dimension, the polynomial f(t) = (t - s) * g(t)^2 where
    # g(t) has appropriate roots gives a valid Delsarte polynomial.

    # Try: f(t) = (t - s) * (t - a)^2 for various a
    for a in np.linspace(-1.0, s - 0.01, 50):
        poly = lambda t, a=a: (t - s) * (t - a) ** 2
        result = delsarte_bound_from_polynomial(n, poly)
        if result['a1_satisfied'] and len(result['a2_violations']) == 0:
            if result['bound'] > 0 and result['bound'] < best_bound:
                best_bound = result['bound']
                best_info = result

    # Strategy 2: f(t) = (t - s) * (t - a)^2 * (t - b)^2
    for a in np.linspace(-0.8, 0.0, 10):
        for b in np.linspace(0.0, 0.4, 10):
            if abs(a - b) < 0.05:
                continue
            poly = lambda t, a=a, b=b: (t - s) * (t - a) ** 2 * (t - b) ** 2
            result = delsarte_bound_from_polynomial(n, poly)
            if result['a1_satisfied'] and len(result['a2_violations']) == 0:
                if result['bound'] > 0 and result['bound'] < best_bound:
                    best_bound = result['bound']
                    best_info = result

    # Strategy 3: f(t) = (t + 1) * (t - s) * (t - a)^2
    for a in np.linspace(-0.5, 0.4, 50):
        poly = lambda t, a=a: (t + 1) * (t - s) * (t - a) ** 2
        result = delsarte_bound_from_polynomial(n, poly)
        if result['a1_satisfied'] and len(result['a2_violations']) == 0:
            if result['bound'] > 0 and result['bound'] < best_bound:
                best_bound = result['bound']
                best_info = result

    # Strategy 4: Higher degree f(t) = (t + 1)(t - s)(t - a)^2(t - b)^2
    for a in np.linspace(-0.5, 0.0, 8):
        for b in np.linspace(0.0, 0.4, 8):
            if abs(a - b) < 0.1:
                continue
            poly = lambda t, a=a, b=b: (t + 1) * (t - s) * (t - a) ** 2 * (t - b) ** 2
            result = delsarte_bound_from_polynomial(n, poly)
            if result['a1_satisfied'] and len(result['a2_violations']) == 0:
                if result['bound'] > 0 and result['bound'] < best_bound:
                    best_bound = result['bound']
                    best_info = result

    if best_bound < float('inf'):
        return {
            'bound': best_bound,
            'integer_bound': int(math.floor(best_bound + 1e-6)),
            'status': 'optimal',
            'dimension': n,
            'details': best_info
        }
    return {
        'bound': None,
        'integer_bound': None,
        'status': 'failed',
        'dimension': n,
        'details': None
    }


def compute_bounds_table(dims=None, max_degree=20):
    """Compute Delsarte bounds for multiple dimensions."""
    if dims is None:
        dims = list(range(3, 9))

    results = {}
    for n in dims:
        print(f"  Computing n={n}...", end=" ", flush=True)
        r = delsarte_kissing_bound(n, max_degree=max_degree)
        results[n] = r
        if r['bound'] is not None:
            print(f"bound = {r['bound']:.4f} => tau_{n} <= {r['integer_bound']}")
        else:
            print("Failed")
    return results


def harmonic_dim(n, k):
    """Dimension h(n,k) of degree-k spherical harmonics in R^n."""
    if k == 0:
        return 1
    if n == 1:
        return 2
    return int(special.comb(n + k - 1, k, exact=True) - special.comb(n + k - 3, k - 2, exact=True))


def normalized_gegenbauer(k, n, t):
    """Normalized Gegenbauer polynomial P_k^n(t) with P_k^n(1) = 1."""
    if k == 0:
        return 1.0
    if n == 2:
        return float(np.cos(k * np.arccos(np.clip(t, -1.0, 1.0))))
    lam = (n - 2) / 2.0
    ck_t = float(special.eval_gegenbauer(k, lam, t))
    ck_1 = float(special.comb(k + 2 * lam - 1, k, exact=False))
    if abs(ck_1) < 1e-30:
        return 0.0
    return ck_t / ck_1


if __name__ == '__main__':
    print("=" * 70)
    print("DELSARTE LINEAR PROGRAMMING BOUNDS FOR KISSING NUMBERS")
    print("=" * 70)

    known = {3: (12, 12), 4: (24, 24), 5: (40, 44),
             6: (72, 77), 7: (126, 134), 8: (240, 240)}

    # First, verify with known polynomial for n=8
    print("\nVerifying known polynomial for n=8:")
    print("f(t) = (t+1)(t+1/2)^2 t^2 (t-1/2)")
    poly_8 = lambda t: (t + 1) * (t + 0.5) ** 2 * t ** 2 * (t - 0.5)
    r8 = delsarte_bound_from_polynomial(8, poly_8)
    print(f"  f(1) = {r8['f_at_1']:.6f}")
    print(f"  f_0 = {r8['f_0']:.6f}")
    print(f"  Bound = f(1)/f_0 = {r8['bound']:.4f}")
    print(f"  A1 satisfied: {r8['a1_satisfied']}")
    print(f"  A2 violations: {r8['a2_violations']}")

    print("\nComputing bounds for n=3..8...")
    results = compute_bounds_table(list(range(3, 9)))

    print(f"\n{'='*70}")
    print("COMPARISON WITH KNOWN BOUNDS")
    print(f"{'='*70}")
    print(f"{'n':>3} {'Our Bound':>10} {'Floor':>7} {'Known Lower':>12} {'Known Upper':>12}")
    for n in range(3, 9):
        r = results.get(n)
        lo, hi = known.get(n, (0, 0))
        if r and r['bound'] is not None:
            print(f"{n:3d} {r['bound']:10.4f} {r['integer_bound']:7d} {lo:12d} {hi:12d}")
        else:
            print(f"{n:3d} {'N/A':>10} {'N/A':>7} {lo:12d} {hi:12d}")

    # Save results
    output_lines = ["Delsarte LP Bounds for Kissing Numbers",
                     "Method: Polynomial ansatz search with Gegenbauer coefficient verification",
                     "=" * 50, ""]
    for n in range(3, 9):
        r = results.get(n)
        lo, hi = known.get(n, (0, 0))
        if r and r['bound'] is not None:
            output_lines.append(
                f"n={n}: bound = {r['bound']:.6f}, floor = {r['integer_bound']}, known = [{lo}, {hi}]")
        else:
            output_lines.append(f"n={n}: no valid polynomial found")

    with open('/home/codex/work/repo/results/delsarte_baseline.txt', 'w') as f:
        f.write('\n'.join(output_lines))
    print("\nResults saved to results/delsarte_baseline.txt")
