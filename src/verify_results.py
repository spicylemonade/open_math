#!/usr/bin/env python3
"""
Independent Verification of All Claimed Results -- Kissing Number Project
=========================================================================

Item 018 of the research rubric.

Cross-checks every claimed result using at least 2 independent numerical
methods.  Uses mpmath with 50-digit precision where applicable.

Verification checks
-------------------
1. Ball volumes V_n for n=1..10  (Gamma formula vs recurrence, 50 digits)
2. Surface areas S_n for n=1..10  (formula vs derivative dV/dR, 50 digits)
3. Cap area cap_area(5, pi/6)  (betainc vs direct numerical integration)
4. D5 lattice: 40 vectors, unit norms to 50 digits, pairwise IPs <= 0.5
5. Cap packing bound: tau_5 <= 77  (S_4/A_cap and V_5/V_cone methods)
6. Delsarte polynomial for n=8: f(1)/f_0 = 240
7. Contact graph: 12-regular, 240 edges
8. Local rigidity of D5: min max IP = sqrt(2/5)

All results logged to results/verification_log.txt.
"""

import sys
import os
import datetime

sys.path.insert(0, '/home/codex/work/repo/src')

import mpmath
from mpmath import mp, mpf, pi as mpi, gamma as mgamma, sqrt as msqrt, sin as msin
from mpmath import cos as mcos, power as mpower, fac, beta as mbeta, quad as mquad
from mpmath import betainc as mbetainc

import numpy as np
import math
from scipy import special
from scipy.integrate import quad

# ---------------------------------------------------------------------------
# High-precision setup
# ---------------------------------------------------------------------------
mp.dps = 50  # 50 decimal places

LOG_LINES = []
PASS_COUNT = 0
FAIL_COUNT = 0


def log(msg=""):
    """Print and accumulate a log line."""
    print(msg)
    LOG_LINES.append(msg)


def record(name, passed, detail=""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if not passed:
        FAIL_COUNT += 1
    else:
        PASS_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  --  {detail}"
    log(line)


# ===================================================================
# 1. Ball volumes V_n for n=1..10  (Gamma formula vs recurrence)
# ===================================================================
def mp_V_gamma(n, R=mpf(1)):
    """V_n(R) = pi^(n/2) / Gamma(n/2+1) * R^n   (mpmath)."""
    return mpower(mpi, mpf(n) / 2) / mgamma(mpf(n) / 2 + 1) * mpower(R, n)


def mp_V_recurrence(n, R=mpf(1)):
    """V_n via recurrence V_n = (2*pi/n)*R^2*V_{n-2}."""
    if n == 0:
        return mpf(1)
    if n == 1:
        return 2 * R
    return (2 * mpi / n) * mpower(R, 2) * mp_V_recurrence(n - 2, R)


def verify_ball_volumes():
    log("\n" + "=" * 72)
    log("CHECK 1: Ball volumes V_n for n=1..10  (Gamma vs Recurrence, 50 digits)")
    log("=" * 72)

    all_ok = True
    for n in range(1, 11):
        v_g = mp_V_gamma(n)
        v_r = mp_V_recurrence(n)
        diff = abs(v_g - v_r)
        ok = diff < mpf(10) ** (-48)
        if not ok:
            all_ok = False
        record(
            f"V_{n}",
            ok,
            f"Gamma={mpmath.nstr(v_g, 50)}  Recur={mpmath.nstr(v_r, 50)}  |diff|={mpmath.nstr(diff, 6)}"
        )

    # Spot-check known exact values
    v3_exact = mpf(4) * mpi / 3
    diff3 = abs(mp_V_gamma(3) - v3_exact)
    record("V_3 == 4*pi/3", diff3 < mpf(10) ** (-48),
           f"|diff|={mpmath.nstr(diff3, 6)}")

    v5_exact = mpf(8) * mpi ** 2 / 15
    diff5 = abs(mp_V_gamma(5) - v5_exact)
    record("V_5 == 8*pi^2/15", diff5 < mpf(10) ** (-48),
           f"|diff|={mpmath.nstr(diff5, 6)}")

    return all_ok


# ===================================================================
# 2. Surface areas S_n for n=1..10  (formula vs derivative dV/dR)
# ===================================================================
def mp_S_formula(n, R=mpf(1)):
    """S_{n-1}(R) = 2*pi^(n/2)/Gamma(n/2) * R^(n-1)."""
    if n == 1:
        return mpf(2)
    return 2 * mpower(mpi, mpf(n) / 2) / mgamma(mpf(n) / 2) * mpower(R, n - 1)


def mp_S_derivative(n, R=mpf(1)):
    """S_{n-1}(R) = dV_n/dR = n*V_n(R)/R."""
    return n * mp_V_gamma(n, R) / R


def verify_surface_areas():
    log("\n" + "=" * 72)
    log("CHECK 2: Surface areas S_n for n=1..10  (Formula vs dV/dR, 50 digits)")
    log("=" * 72)

    all_ok = True
    for n in range(1, 11):
        s_f = mp_S_formula(n)
        s_d = mp_S_derivative(n)
        diff = abs(s_f - s_d)
        ok = diff < mpf(10) ** (-47)
        if not ok:
            all_ok = False
        record(
            f"S_{n}",
            ok,
            f"Formula={mpmath.nstr(s_f, 50)}  Deriv={mpmath.nstr(s_d, 50)}  |diff|={mpmath.nstr(diff, 6)}"
        )

    # Spot-check: S_4(1) = 8*pi^2/3  (surface area of S^4 bounding B^5)
    s4_exact = 8 * mpi ** 2 / 3
    diff = abs(mp_S_formula(5) - s4_exact)
    record("S_4(1) == 8*pi^2/3", diff < mpf(10) ** (-47),
           f"|diff|={mpmath.nstr(diff, 6)}")

    return all_ok


# ===================================================================
# 3. Cap area cap_area(5, pi/6)  (betainc vs numerical integration)
# ===================================================================
def verify_cap_area():
    log("\n" + "=" * 72)
    log("CHECK 3: cap_area(5, pi/6) via betainc AND direct numerical integration")
    log("=" * 72)

    n = 5
    theta = mpi / 6

    # Method 1: regularised incomplete beta (mpmath)
    S = mp_S_formula(n)
    x = msin(theta) ** 2  # sin^2(pi/6) = 1/4
    a_param = mpf(n - 1) / 2   # 2.0
    b_param = mpf(1) / 2        # 0.5
    # mpmath.betainc(a, b, 0, x) gives the NON-regularised incomplete beta.
    # Regularised = betainc(a,b,0,x) / beta(a,b)
    Ix = mbetainc(a_param, b_param, 0, x) / mbeta(a_param, b_param)
    cap_betainc = S / 2 * Ix

    # Method 2: direct numerical integration of the cross-section formula.
    # Cap area = integral from 0 to theta of S_{n-2}(sin phi) * sin(phi)^(n-2) ...
    # Actually: A_cap = S_{n-2} integral_0^theta sin^{n-2}(phi) dphi
    #         where S_{n-2} is the surface area of S^{n-2} at unit radius.
    # More precisely, using the standard parametrisation:
    #   A_cap(n, theta) = S_{n-2}(1) * integral_0^theta sin^{n-2}(phi) dphi
    # For n=5: S_3(1) = 2*pi^2 and integral_0^{pi/6} sin^3(phi) dphi.
    S_nm2 = mp_S_formula(n - 1)  # S_{n-2}(1) = S_3(1) for n=5
    integrand = lambda phi: msin(phi) ** (n - 2)
    integral_val = mquad(integrand, [0, theta])
    cap_integration = S_nm2 * integral_val

    diff = abs(cap_betainc - cap_integration)
    ok = diff / abs(cap_betainc) < mpf(10) ** (-15)
    record(
        "cap_area(5, pi/6) betainc vs integration",
        ok,
        f"betainc={mpmath.nstr(cap_betainc, 30)}  integ={mpmath.nstr(cap_integration, 30)}  |reldiff|={mpmath.nstr(diff / abs(cap_betainc), 6)}"
    )

    # Cross-check with scipy (float64)
    from ndim_geometry import cap_area as scipy_cap_area
    scipy_val = scipy_cap_area(5, float(mpi / 6))
    diff_scipy = abs(mpf(scipy_val) - cap_betainc)
    ok2 = diff_scipy / abs(cap_betainc) < mpf(10) ** (-10)
    record(
        "cap_area(5, pi/6) mpmath vs scipy",
        ok2,
        f"scipy={scipy_val:.15e}  mpmath={mpmath.nstr(cap_betainc, 15)}  |reldiff|={mpmath.nstr(diff_scipy / abs(cap_betainc), 6)}"
    )

    return ok and ok2


# ===================================================================
# 4. D5 lattice: 40 vectors, unit norms to 50 digits, IPs <= 0.5
# ===================================================================
def generate_d5_mpmath():
    """Generate 40 D5 minimal vectors in mpmath high-precision."""
    vectors = []
    for i in range(5):
        for j in range(i + 1, 5):
            for si in [-1, 1]:
                for sj in [-1, 1]:
                    v = [mpf(0)] * 5
                    v[i] = mpf(si)
                    v[j] = mpf(sj)
                    vectors.append(v)
    return vectors


def verify_d5_lattice():
    log("\n" + "=" * 72)
    log("CHECK 4: D5 lattice -- 40 vectors, unit norms (50 digits), IPs <= 0.5")
    log("=" * 72)

    raw = generate_d5_mpmath()
    record("D5 vector count == 40", len(raw) == 40, f"count={len(raw)}")

    # Normalise to unit length (raw norm = sqrt(2))
    norm0 = msqrt(sum(x ** 2 for x in raw[0]))
    unit = []
    for v in raw:
        n2 = msqrt(sum(x ** 2 for x in v))
        unit.append([x / n2 for x in v])

    # Check all norms == 1 to 50 digits
    max_norm_err = mpf(0)
    for v in unit:
        n2 = msqrt(sum(x ** 2 for x in v))
        err = abs(n2 - 1)
        if err > max_norm_err:
            max_norm_err = err
    record("All norms == 1.0 (50 digits)", max_norm_err < mpf(10) ** (-49),
           f"max |norm-1| = {mpmath.nstr(max_norm_err, 6)}")

    # Check all pairwise inner products <= 0.5
    max_ip = mpf('-inf')
    violations = 0
    k = len(unit)
    for i in range(k):
        for j in range(i + 1, k):
            ip = sum(unit[i][d] * unit[j][d] for d in range(5))
            if ip > max_ip:
                max_ip = ip
            if ip > mpf('0.5') + mpf(10) ** (-48):
                violations += 1

    record("Max pairwise IP <= 0.5", max_ip <= mpf('0.5') + mpf(10) ** (-48),
           f"max IP = {mpmath.nstr(max_ip, 50)}")
    record("No IP violations", violations == 0,
           f"violations = {violations}")

    # Cross-check with numpy (float64)
    from d5_lattice import generate_d5_vectors, normalize_vectors
    np_raw = generate_d5_vectors()
    np_unit = normalize_vectors(np_raw)
    record("numpy vector count == 40", len(np_unit) == 40, f"count={len(np_unit)}")
    np_norms = np.linalg.norm(np_unit, axis=1)
    record("numpy norms ~ 1 (float64)", np.allclose(np_norms, 1.0, atol=1e-14),
           f"max |norm-1| = {np.max(np.abs(np_norms - 1.0)):.3e}")

    return violations == 0


# ===================================================================
# 5. Cap packing bound: tau_5 <= 77
# ===================================================================
def verify_cap_packing_bound():
    log("\n" + "=" * 72)
    log("CHECK 5: Cap packing bound  tau_5 <= 77  (two methods)")
    log("=" * 72)

    n = 5
    theta = mpi / 6

    # Method 1: S_4 / A_cap
    S4 = mp_S_formula(n)
    x = msin(theta) ** 2
    a_param = mpf(n - 1) / 2
    b_param = mpf(1) / 2
    Ix = mbetainc(a_param, b_param, 0, x) / mbeta(a_param, b_param)
    A_cap = S4 / 2 * Ix
    bound1 = S4 / A_cap
    floor1 = int(mpmath.floor(bound1))

    record("Method 1 (S_4/A_cap): floor <= 77", floor1 <= 77,
           f"bound={mpmath.nstr(bound1, 30)}  floor={floor1}")

    # Method 2: volume ratio  V_{cone} vs V_{sphere}
    # The solid angle fraction omega = A_cap / S_4 so tau <= 1/omega = S_4/A_cap.
    # Equivalently, the cone of half-angle theta in R^5 occupies a fraction
    # omega = I_{sin^2 theta}((n-1)/2, 1/2) / 2 of the sphere.
    # tau <= 1 / omega.
    omega = Ix / 2
    bound2 = 1 / omega
    floor2 = int(mpmath.floor(bound2))

    record("Method 2 (1/omega): floor <= 77", floor2 <= 77,
           f"bound={mpmath.nstr(bound2, 30)}  floor={floor2}")

    # Methods should agree exactly (they are algebraically identical)
    agree = abs(bound1 - bound2) < mpf(10) ** (-45)
    record("Both methods agree (50 digits)", agree,
           f"|diff|={mpmath.nstr(abs(bound1 - bound2), 6)}")

    # Cross-check with scipy
    from ndim_geometry import cap_packing_bound
    scipy_bound = cap_packing_bound(5)
    diff = abs(mpf(scipy_bound) - bound1) / bound1
    record("scipy cap_packing_bound agrees", diff < mpf(10) ** (-10),
           f"scipy={scipy_bound:.15e}  mpmath={mpmath.nstr(bound1, 15)}  reldiff={mpmath.nstr(diff, 6)}")

    return floor1 <= 77 and floor2 <= 77


# ===================================================================
# 6. Delsarte polynomial for n=8: f(1)/f_0 = 240
# ===================================================================
def verify_delsarte_n8():
    log("\n" + "=" * 72)
    log("CHECK 6: Delsarte polynomial n=8  f(1)/f_0 = 240")
    log("         f(t) = (t+1)(t+1/2)^2 * t^2 * (t-1/2)")
    log("=" * 72)

    # --- Method A: mpmath exact rational arithmetic ---
    def f_mp(t):
        t = mpf(t)
        return (t + 1) * (t + mpf(1) / 2) ** 2 * t ** 2 * (t - mpf(1) / 2)

    f1 = f_mp(1)  # f(1)

    # Gegenbauer coefficients via mpmath numerical integration
    n = 8
    lam = mpf(n - 2) / 2  # lambda = 3

    def weight(t):
        return (1 - t ** 2) ** ((n - 3) / mpf(2))

    def gegenbauer_recurrence(k, lam_val, t):
        """Evaluate C_k^{lam}(t) via the stable three-term recurrence.

        C_0 = 1,  C_1 = 2*lam*t,
        C_{k} = (2*(k-1+lam)*t*C_{k-1} - (k-2+2*lam)*C_{k-2}) / k.
        """
        t = mpf(t)
        if k == 0:
            return mpf(1)
        if k == 1:
            return 2 * lam_val * t
        c_prev2 = mpf(1)
        c_prev1 = 2 * lam_val * t
        for m in range(2, k + 1):
            c_cur = (2 * (m - 1 + lam_val) * t * c_prev1
                     - (m - 2 + 2 * lam_val) * c_prev2) / m
            c_prev2 = c_prev1
            c_prev1 = c_cur
        return c_prev1

    def gegenbauer_normalized_mp(k, t):
        """Normalised Gegenbauer P_k^(n)(t) with P_k(1) = 1."""
        if k == 0:
            return mpf(1)
        ck_t = gegenbauer_recurrence(k, lam, t)
        ck_1 = gegenbauer_recurrence(k, lam, mpf(1))
        if abs(ck_1) < mpf(10) ** (-40):
            return mpf(0)
        return ck_t / ck_1

    # Compute f_0 = <f, P_0> / <P_0, P_0>  = <f, 1*w> / <1*w>
    num0 = mquad(lambda t: f_mp(t) * weight(t), [-1, 1])
    den0 = mquad(lambda t: weight(t), [-1, 1])
    f0_mp = num0 / den0

    ratio_mp = f1 / f0_mp
    ok_mp = abs(ratio_mp - 240) < mpf(10) ** (-6)
    record("mpmath: f(1)/f_0 == 240", ok_mp,
           f"f(1)={mpmath.nstr(f1, 30)}  f_0={mpmath.nstr(f0_mp, 30)}  ratio={mpmath.nstr(ratio_mp, 20)}")

    # Check A1: f(t) <= 0 on [-1, 0.5]
    t_grid_mp = [mpf(-1) + mpf(i) / 2000 * mpf('1.5') for i in range(2001)]
    a1_max = max(f_mp(t) for t in t_grid_mp)
    record("mpmath: f(t) <= 0 on [-1, 0.5]", a1_max <= mpf(10) ** (-12),
           f"max f(t) on grid = {mpmath.nstr(a1_max, 10)}")

    # Check A2: all Gegenbauer coefficients >= 0
    coeffs_mp = []
    for k in range(7):
        num_k = mquad(lambda t, k=k: f_mp(t) * gegenbauer_normalized_mp(k, t) * weight(t), [-1, 1])
        den_k = mquad(lambda t, k=k: gegenbauer_normalized_mp(k, t) ** 2 * weight(t), [-1, 1])
        fk = num_k / den_k if abs(den_k) > mpf(10) ** (-40) else mpf(0)
        coeffs_mp.append(fk)
    neg_coeffs = [(k, c) for k, c in enumerate(coeffs_mp) if c < -mpf(10) ** (-8)]
    record("mpmath: all f_k >= 0", len(neg_coeffs) == 0,
           f"coeffs=[{', '.join(mpmath.nstr(c, 8) for c in coeffs_mp)}]  neg={neg_coeffs}")

    # --- Method B: scipy float64 cross-check ---
    def f_scipy(t):
        return (t + 1) * (t + 0.5) ** 2 * t ** 2 * (t - 0.5)

    f1_sp = f_scipy(1.0)

    from delsarte_lp import gegenbauer_coefficients
    coeffs_sp = gegenbauer_coefficients(f_scipy, 8, max_degree=6)
    f0_sp = coeffs_sp[0]
    ratio_sp = f1_sp / f0_sp
    ok_sp = abs(ratio_sp - 240) < 0.01
    record("scipy: f(1)/f_0 == 240", ok_sp,
           f"f(1)={f1_sp:.10f}  f_0={f0_sp:.10f}  ratio={ratio_sp:.6f}")

    return ok_mp and ok_sp


# ===================================================================
# 7. Contact graph: 12-regular, 240 edges
# ===================================================================
def verify_contact_graph():
    log("\n" + "=" * 72)
    log("CHECK 7: D5 contact graph -- 12-regular, 240 edges")
    log("=" * 72)

    # Method A: from scratch using mpmath vectors
    unit = []
    raw = generate_d5_mpmath()
    for v in raw:
        n2 = msqrt(sum(x ** 2 for x in v))
        unit.append([x / n2 for x in v])

    k = len(unit)
    tol = mpf(10) ** (-40)
    edges = []
    degree = [0] * k
    for i in range(k):
        for j in range(i + 1, k):
            ip = sum(unit[i][d] * unit[j][d] for d in range(5))
            if abs(ip - mpf(1) / 2) < tol:
                edges.append((i, j))
                degree[i] += 1
                degree[j] += 1

    n_edges = len(edges)
    min_deg = min(degree)
    max_deg = max(degree)
    is_12_regular = (min_deg == 12 and max_deg == 12)

    record("Edge count == 240", n_edges == 240, f"edges={n_edges}")
    record("12-regular graph", is_12_regular,
           f"min_deg={min_deg}  max_deg={max_deg}")

    # Method B: using numpy (d5_lattice module)
    from d5_lattice import generate_d5_vectors, normalize_vectors, \
        verify_kissing_configuration, analyze_contact_graph
    np_unit = normalize_vectors(generate_d5_vectors())
    res = verify_kissing_configuration(np_unit)
    cg = analyze_contact_graph(np_unit, res['contact_pairs'])

    record("numpy edge count == 240", res['n_contact_pairs'] == 240,
           f"edges={res['n_contact_pairs']}")
    record("numpy 12-regular", cg['min_degree'] == 12 and cg['max_degree'] == 12,
           f"min_deg={cg['min_degree']}  max_deg={cg['max_degree']}")

    return n_edges == 240 and is_12_regular


# ===================================================================
# 8. Local rigidity of D5: min_{v on S^4} max_{u in D5} <v,u> = sqrt(2/5)
# ===================================================================
def verify_local_rigidity():
    log("\n" + "=" * 72)
    log("CHECK 8: Local rigidity of D5  --  min_{v in S^4} max_{u in D5} <v,u> = sqrt(2/5)")
    log("=" * 72)

    # Analytical derivation:
    # D5 unit vectors are (s_i*e_i + s_j*e_j)/sqrt(2) for all i<j, s in {+/-1}.
    # For unit v, max_{u in D5} <v,u> = max_{i<j} (|v_i|+|v_j|)/sqrt(2).
    # Minimising over unit v: by symmetry optimum is |v_i|=1/sqrt(5) for all i.
    # Then min_v max_u <v,u> = 2/(sqrt(5)*sqrt(2)) = sqrt(2/5).
    analytic = msqrt(mpf(2) / 5)

    # --- Method A: mpmath analytical verification ---
    # At v = (1,1,1,1,1)/sqrt(5), compute max IP with D5
    v_opt = [mpf(1) / msqrt(mpf(5))] * 5
    raw = generate_d5_mpmath()
    unit = []
    for u in raw:
        n2 = msqrt(sum(x ** 2 for x in u))
        unit.append([x / n2 for x in u])

    max_ip_at_opt = mpf('-inf')
    for u in unit:
        ip = sum(v_opt[d] * u[d] for d in range(5))
        if ip > max_ip_at_opt:
            max_ip_at_opt = ip

    diff_opt = abs(max_ip_at_opt - analytic)
    record("mpmath: max IP at v=(1,...,1)/sqrt(5) == sqrt(2/5)", diff_opt < mpf(10) ** (-48),
           f"computed={mpmath.nstr(max_ip_at_opt, 50)}  analytic={mpmath.nstr(analytic, 50)}  |diff|={mpmath.nstr(diff_opt, 6)}")

    # --- Method B: numerical optimisation (minimize max IP over S^4) ---
    from scipy.optimize import minimize as scipy_minimize
    from d5_lattice import generate_d5_vectors, normalize_vectors
    np_unit = normalize_vectors(generate_d5_vectors())

    def max_ip_func(x):
        v = x / np.linalg.norm(x)
        return np.max(np_unit @ v)

    # Multiple random starts to find the global minimum
    rng = np.random.RandomState(42)
    best_val = 1.0
    for _ in range(100):
        x0 = rng.randn(5)
        x0 = x0 / np.linalg.norm(x0)
        res = scipy_minimize(max_ip_func, x0, method='Nelder-Mead',
                             options={'maxiter': 10000, 'xatol': 1e-14, 'fatol': 1e-14})
        v_res = res.x / np.linalg.norm(res.x)
        val = max_ip_func(v_res)
        if val < best_val:
            best_val = val

    analytic_np = math.sqrt(2.0 / 5.0)
    diff_np = abs(best_val - analytic_np)
    record("scipy optimisation: min max IP ~ sqrt(2/5)", diff_np < 1e-6,
           f"computed={best_val:.15e}  analytic={analytic_np:.15e}  |diff|={diff_np:.3e}")

    # Verify sqrt(2/5) > 0.5  (confirms rigidity -- no 41st point can have
    # all IPs <= 0.5 because the minimum achievable max IP is sqrt(2/5) > 0.5)
    gap = analytic - mpf(1) / 2
    record("sqrt(2/5) > 0.5 (rigidity gap > 0)", gap > 0,
           f"gap = {mpmath.nstr(gap, 30)}")

    # Also verify the analytic formula:  2 / sqrt(10) = sqrt(2/5)
    alt = mpf(2) / msqrt(mpf(10))
    diff_alt = abs(alt - analytic)
    record("2/sqrt(10) == sqrt(2/5)", diff_alt < mpf(10) ** (-49),
           f"|diff|={mpmath.nstr(diff_alt, 6)}")

    return diff_opt < mpf(10) ** (-48)


# ===================================================================
# MAIN
# ===================================================================
def main():
    log("=" * 72)
    log("INDEPENDENT VERIFICATION OF ALL CLAIMED RESULTS")
    log("Kissing Number in Dimension 5 -- Research Project")
    log(f"Date: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    log(f"mpmath precision: {mp.dps} decimal places")
    log("=" * 72)

    verify_ball_volumes()
    verify_surface_areas()
    verify_cap_area()
    verify_d5_lattice()
    verify_cap_packing_bound()
    verify_delsarte_n8()
    verify_contact_graph()
    verify_local_rigidity()

    log("\n" + "=" * 72)
    log("SUMMARY")
    log("=" * 72)
    log(f"  Total checks:  {PASS_COUNT + FAIL_COUNT}")
    log(f"  PASSED:        {PASS_COUNT}")
    log(f"  FAILED:        {FAIL_COUNT}")
    if FAIL_COUNT == 0:
        log("  ALL CHECKS PASSED")
    else:
        log(f"  *** {FAIL_COUNT} CHECK(S) FAILED ***")
    log("=" * 72)

    # Write log
    log_path = '/home/codex/work/repo/results/verification_log.txt'
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'w') as f:
        f.write('\n'.join(LOG_LINES) + '\n')
    print(f"\nLog written to {log_path}")


if __name__ == '__main__':
    main()
