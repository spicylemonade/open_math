"""
Comprehensive Numerical Experiments for the Kissing Number Project.

Runs all computational approaches from Phase 3 with multiple parameter
settings and records every result in results/experiments_summary.csv.

Item 017 of the research rubric.

Experiment categories:
  (a) Cap packing bounds for n=2..8
  (b) Delsarte LP polynomial search for n=3,5
  (c) Enhanced bound (with dimensional constraints) for n=5
  (d) D5 lattice verification
  (e) Greedy spherical code construction for various (n, target_k) pairs
  (f) Construction attempts for 41st point (reduced scale)
  (g) Cross-dimensional consistency checks for tau_5 in {40..44}

All results are reproducible with fixed random seeds.
"""

import sys
import os
import csv
import math
import time
import traceback

import numpy as np

sys.path.insert(0, '/home/codex/work/repo/src')

from ndim_geometry import V_n, S_n, cap_area, cap_solid_angle, cap_packing_bound
from delsarte_lp import (
    delsarte_kissing_bound,
    delsarte_bound_from_polynomial,
    gegenbauer_coefficients,
    normalized_gegenbauer,
    harmonic_dim,
)
from d5_lattice import (
    generate_d5_vectors,
    normalize_vectors,
    verify_kissing_configuration,
    analyze_contact_graph,
)
from spherical_codes import validate_kissing_config, greedy_spherical_code
from enhanced_bound import (
    search_enhanced_bound,
    check_equatorial_slicing,
    check_second_moment_trace,
    check_volume_recurrence_consistency,
    enhanced_delsarte_bound_full,
    KNOWN_LOWER,
    KNOWN_UPPER,
)
from cross_dim_check import cap_density, cross_dim_ratio, project_density_constraint
from construct_kissing import (
    get_d5_unit_vectors,
    max_inner_product_with_config,
    attempt_grid_search,
    attempt_optimization,
    attempt_algebraic,
)

# ---------------------------------------------------------------------------
# Global configuration
# ---------------------------------------------------------------------------
SEED = 42
TIMEOUT_PER_EXPERIMENT = 120  # seconds

RESULTS_DIR = '/home/codex/work/repo/results'
CSV_PATH = os.path.join(RESULTS_DIR, 'experiments_summary.csv')

CSV_COLUMNS = [
    'Method', 'Dimension', 'Parameters', 'Upper_Bound', 'Lower_Bound',
    'Runtime_Seconds', 'Notes',
]

# Accumulator for rows
rows = []


def add_row(method, dimension, parameters, upper_bound, lower_bound,
            runtime, notes):
    """Append a result row to the global list."""
    rows.append({
        'Method': method,
        'Dimension': dimension,
        'Parameters': parameters,
        'Upper_Bound': upper_bound,
        'Lower_Bound': lower_bound,
        'Runtime_Seconds': f'{runtime:.4f}',
        'Notes': notes,
    })


def timed(func, *args, **kwargs):
    """Run *func* and return (result, elapsed_seconds).

    If the function takes longer than TIMEOUT_PER_EXPERIMENT we still
    return whatever it produces (Python-level timeout via signal is
    unreliable in multithreaded scipy code, so we just record the time).
    """
    t0 = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - t0
    return result, elapsed


# ===================================================================
# (a) Cap packing bounds for n = 2 .. 8
# ===================================================================
def run_cap_packing_experiments():
    print('\n=== (a) Cap Packing Bounds ===')
    for n in range(2, 9):
        t0 = time.time()
        bound = cap_packing_bound(n)
        ibound = int(math.floor(bound))
        elapsed = time.time() - t0
        known_lo = KNOWN_LOWER.get(n, '')
        known_hi = KNOWN_UPPER.get(n, '')
        add_row(
            method='CapPacking',
            dimension=n,
            parameters='min_angle=60deg',
            upper_bound=f'{bound:.6f}',
            lower_bound=str(known_lo),
            runtime=elapsed,
            notes=f'floor={ibound}; known_UB={known_hi}',
        )
        print(f'  n={n}: bound={bound:.4f} (floor {ibound})')

    # Additional: cap bounds with varying exclusion angles
    for n in [3, 5, 8]:
        for angle_deg in [55, 58, 60, 62, 65, 70, 75, 80, 90]:
            min_angle = math.radians(angle_deg)
            t0 = time.time()
            bound = cap_packing_bound(n, min_angle=min_angle)
            ibound = int(math.floor(bound))
            elapsed = time.time() - t0
            add_row(
                method='CapPacking_VaryAngle',
                dimension=n,
                parameters=f'min_angle={angle_deg}deg',
                upper_bound=f'{bound:.6f}',
                lower_bound='',
                runtime=elapsed,
                notes=f'floor={ibound}',
            )
        print(f'  n={n}: angle sweep (9 angles) done')


# ===================================================================
# (b) Delsarte LP polynomial search for n = 3, 5
# ===================================================================
def run_delsarte_experiments():
    print('\n=== (b) Delsarte LP Polynomial Search ===')
    for n in [3, 5]:
        t0 = time.time()
        r = delsarte_kissing_bound(n, max_degree=20)
        elapsed = time.time() - t0
        bound = r['bound']
        ibound = r['integer_bound']
        status = r['status']
        known_lo = KNOWN_LOWER.get(n, '')
        known_hi = KNOWN_UPPER.get(n, '')
        add_row(
            method='DelsarteLP',
            dimension=n,
            parameters='max_degree=20; ansatz_search',
            upper_bound=f'{bound:.6f}' if bound is not None else 'N/A',
            lower_bound=str(known_lo),
            runtime=elapsed,
            notes=f'floor={ibound}; status={status}; known_UB={known_hi}',
        )
        if bound is not None:
            print(f'  n={n}: bound={bound:.4f} (floor {ibound}) [{elapsed:.1f}s]')
        else:
            print(f'  n={n}: FAILED [{elapsed:.1f}s]')

    # Also verify the known n=8 Levenshtein polynomial
    print('  Verifying known n=8 Levenshtein polynomial ...')
    t0 = time.time()
    poly_8 = lambda t: (t + 1) * (t + 0.5) ** 2 * t ** 2 * (t - 0.5)
    r8 = delsarte_bound_from_polynomial(8, poly_8)
    elapsed = time.time() - t0
    add_row(
        method='DelsarteLP_Verify',
        dimension=8,
        parameters='Levenshtein_poly; (t+1)(t+0.5)^2*t^2*(t-0.5)',
        upper_bound=f'{r8["bound"]:.6f}',
        lower_bound='240',
        runtime=elapsed,
        notes=f'A1={r8["a1_satisfied"]}; A2_violations={len(r8["a2_violations"])}',
    )
    print(f'  n=8 verify: bound={r8["bound"]:.4f} [{elapsed:.1f}s]')


# ===================================================================
# (c) Enhanced bound (with dimensional constraints) for n = 5
# ===================================================================
def run_enhanced_bound_experiments():
    print('\n=== (c) Enhanced Bound with Dimensional Constraints ===')
    for n in [5]:
        t0 = time.time()
        r = search_enhanced_bound(n, verbose=False)
        elapsed = time.time() - t0
        bound = r['best_bound']
        ibound = r['integer_bound']
        known_lo = KNOWN_LOWER.get(n, '')
        known_hi = KNOWN_UPPER.get(n, '')
        add_row(
            method='EnhancedDelsarte',
            dimension=n,
            parameters='D1+D2+D3 constraints',
            upper_bound=f'{bound:.6f}' if bound is not None else 'N/A',
            lower_bound=str(known_lo),
            runtime=elapsed,
            notes=(f'floor={ibound}; tested={r["candidates_tested"]}; '
                   f'passed_delsarte={r["candidates_passed_delsarte"]}; '
                   f'passed_all={r["candidates_passed_all"]}; '
                   f'known_UB={known_hi}'),
        )
        if bound is not None:
            print(f'  n={n}: enhanced bound={bound:.4f} (floor {ibound}) [{elapsed:.1f}s]')
        else:
            print(f'  n={n}: FAILED [{elapsed:.1f}s]')

    # Individual dimensional constraint checks for several k values in dim 5
    print('  Running individual constraint checks for n=5 ...')
    for k in range(38, 48):
        t0 = time.time()
        d1 = check_equatorial_slicing(5, k)
        d2 = check_second_moment_trace(5, k)
        elapsed = time.time() - t0
        add_row(
            method='DimConstraint_D1D2',
            dimension=5,
            parameters=f'k={k}',
            upper_bound='',
            lower_bound='',
            runtime=elapsed,
            notes=f'D1_sat={d1["satisfied"]}; D2_sat={d2["satisfied"]}; '
                  f'D2_max_k={d2["max_k_from_trace"]}',
        )


# ===================================================================
# (d) D5 lattice verification
# ===================================================================
def run_d5_verification():
    print('\n=== (d) D5 Lattice Verification ===')
    t0 = time.time()
    raw = generate_d5_vectors()
    unit = normalize_vectors(raw)
    result = verify_kissing_configuration(unit)
    cg = analyze_contact_graph(unit, result['contact_pairs'])
    elapsed = time.time() - t0

    add_row(
        method='D5_Lattice_Verify',
        dimension=5,
        parameters='40 minimal vectors',
        upper_bound='',
        lower_bound='40',
        runtime=elapsed,
        notes=(f'valid={result["valid"]}; max_ip={result["max_inner_product"]:.6f}; '
               f'contact_pairs={result["n_contact_pairs"]}; '
               f'min_deg={cg["min_degree"]}; max_deg={cg["max_degree"]}'),
    )
    print(f'  D5 verified: {result["n_vectors"]} vectors, valid={result["valid"]} [{elapsed:.2f}s]')

    # Also validate with the spherical_codes module
    t0 = time.time()
    val = validate_kissing_config(unit)
    elapsed = time.time() - t0
    add_row(
        method='D5_Lattice_Validate',
        dimension=5,
        parameters='spherical_codes.validate_kissing_config',
        upper_bound='',
        lower_bound='40',
        runtime=elapsed,
        notes=(f'valid={val["valid"]}; max_ip={val["max_inner_product"]:.6f}; '
               f'angle_violations={val["n_angle_violations"]}'),
    )

    # Inner product spectrum
    G = unit @ unit.T
    ips = []
    for i in range(len(unit)):
        for j in range(i + 1, len(unit)):
            ips.append(G[i, j])
    ips = np.array(ips)
    unique_ips = np.unique(np.round(ips, 10))
    for ip_val in sorted(unique_ips):
        cnt = int(np.sum(np.abs(ips - ip_val) < 1e-10))
        add_row(
            method='D5_IP_Spectrum',
            dimension=5,
            parameters=f'inner_product={ip_val:.4f}',
            upper_bound='',
            lower_bound='',
            runtime=0.0,
            notes=f'count={cnt}',
        )


# ===================================================================
# (e) Greedy spherical code construction
# ===================================================================
def run_greedy_code_experiments():
    print('\n=== (e) Greedy Spherical Code Construction ===')
    configs = [
        # (n, target_k, n_attempts, seed)
        (3, 12, 5, 42),
        (3, 13, 5, 42),
        (3, 6, 5, 42),
        (4, 24, 5, 42),
        (4, 25, 5, 42),
        (4, 12, 5, 42),
        (5, 20, 5, 42),
        (5, 30, 5, 42),
        (5, 35, 5, 42),
        (5, 38, 5, 42),
        (5, 40, 5, 42),
        (5, 41, 5, 42),
        (5, 42, 5, 42),
        (6, 40, 5, 42),
        (6, 50, 5, 42),
        (6, 72, 3, 42),
        (7, 60, 3, 42),
        (7, 126, 3, 42),
        (8, 100, 3, 42),
        (8, 240, 2, 42),
    ]
    for n, target_k, n_att, seed in configs:
        t0 = time.time()
        r = greedy_spherical_code(n, target_k, n_attempts=n_att, seed=seed)
        elapsed = time.time() - t0
        add_row(
            method='GreedyCode',
            dimension=n,
            parameters=f'target_k={target_k}; n_attempts={n_att}; seed={seed}',
            upper_bound='',
            lower_bound=str(r['n_placed']),
            runtime=elapsed,
            notes=(f'placed={r["n_placed"]}; valid={r["valid"]}; '
                   f'min_angle={r["min_angle_achieved"]:.2f}deg; '
                   f'max_ip={r["max_inner_product"]:.6f}'),
        )
        print(f'  n={n}, target={target_k}: placed={r["n_placed"]} '
              f'valid={r["valid"]} [{elapsed:.1f}s]')


# ===================================================================
# (f) Construction attempts for 41st point (reduced scale)
# ===================================================================
def run_construction_41_experiments():
    print('\n=== (f) 41st Point Construction Attempts (Reduced Scale) ===')
    config = get_d5_unit_vectors()

    # Grid search with 10K samples
    t0 = time.time()
    r1 = attempt_grid_search(config, n_samples=10000, seed=SEED)
    elapsed = time.time() - t0
    add_row(
        method='Construct41_GridSearch',
        dimension=5,
        parameters='n_samples=10000; seed=42',
        upper_bound='',
        lower_bound='41' if r1['found'] else '40',
        runtime=elapsed,
        notes=(f'found={r1["found"]}; n_valid={r1["n_valid"]}; '
               f'best_max_ip={r1["best_max_ip"]:.6f}'),
    )
    print(f'  Grid search (10K): found={r1["found"]}, '
          f'best_ip={r1["best_max_ip"]:.4f} [{elapsed:.1f}s]')

    # Optimization with 10 starts
    t0 = time.time()
    r2 = attempt_optimization(config, n_starts=10, seed=SEED)
    elapsed = time.time() - t0
    add_row(
        method='Construct41_Optimization',
        dimension=5,
        parameters='n_starts=10; seed=42',
        upper_bound='',
        lower_bound='41' if r2['found'] else '40',
        runtime=elapsed,
        notes=(f'found={r2["found"]}; best_max_ip={r2["best_max_ip"]:.6f}; '
               f'margin={r2["margin"]:.6f}'),
    )
    print(f'  Optimization (10 starts): found={r2["found"]}, '
          f'best_ip={r2["best_max_ip"]:.4f} [{elapsed:.1f}s]')

    # Algebraic construction
    t0 = time.time()
    r3 = attempt_algebraic(config)
    elapsed = time.time() - t0
    add_row(
        method='Construct41_Algebraic',
        dimension=5,
        parameters='D5_symmetry_candidates',
        upper_bound='',
        lower_bound='41' if r3['found'] else '40',
        runtime=elapsed,
        notes=(f'found={r3["found"]}; n_candidates={r3["n_candidates"]}; '
               f'n_valid={r3["n_valid"]}; best_max_ip={r3["best_max_ip"]:.6f}'),
    )
    print(f'  Algebraic: found={r3["found"]}, '
          f'candidates={r3["n_candidates"]} [{elapsed:.1f}s]')

    # Grid search with different seeds
    for seed in [100, 200, 300]:
        t0 = time.time()
        r = attempt_grid_search(config, n_samples=10000, seed=seed)
        elapsed = time.time() - t0
        add_row(
            method='Construct41_GridSearch',
            dimension=5,
            parameters=f'n_samples=10000; seed={seed}',
            upper_bound='',
            lower_bound='41' if r['found'] else '40',
            runtime=elapsed,
            notes=(f'found={r["found"]}; n_valid={r["n_valid"]}; '
                   f'best_max_ip={r["best_max_ip"]:.6f}'),
        )


# ===================================================================
# (g) Cross-dimensional consistency checks
# ===================================================================
def run_cross_dim_experiments():
    print('\n=== (g) Cross-Dimensional Consistency Checks ===')

    known_tau = {1: 2, 2: 6, 3: 12, 4: 24, 8: 240, 24: 196560}

    # Cap solid angles for n = 2..9
    for n in range(2, 10):
        t0 = time.time()
        omega = cap_solid_angle(n, math.pi / 6)
        elapsed = time.time() - t0
        tau = known_tau.get(n, KNOWN_UPPER.get(n, None))
        coverage = tau * omega if tau is not None else None
        add_row(
            method='CrossDim_CapSolidAngle',
            dimension=n,
            parameters='half_angle=pi/6',
            upper_bound=f'{1.0 / omega:.6f}' if omega > 0 else 'N/A',
            lower_bound='',
            runtime=elapsed,
            notes=(f'omega={omega:.10f}; '
                   f'coverage={coverage * 100:.2f}%' if coverage is not None
                   else f'omega={omega:.10f}'),
        )

    # Cross-dim omega ratios for n = 4..9
    for n in range(4, 10):
        t0 = time.time()
        ratio = cross_dim_ratio(n)
        vol_ratio = V_n(n) / V_n(n - 2)
        expected = 2 * math.pi / n
        elapsed = time.time() - t0
        add_row(
            method='CrossDim_OmegaRatio',
            dimension=n,
            parameters=f'omega_{n}/omega_{n-2}',
            upper_bound='',
            lower_bound='',
            runtime=elapsed,
            notes=(f'ratio={ratio:.10f}; '
                   f'2pi/n={expected:.10f}; '
                   f'V_ratio={vol_ratio:.10f}'),
        )

    # Consistency check for tau_5 in {40..44}
    for k in range(40, 45):
        t0 = time.time()
        omega = cap_solid_angle(5, math.pi / 6)
        coverage = k * omega
        density_3 = 12 * cap_solid_angle(3, math.pi / 6)
        density_4 = 24 * cap_solid_angle(4, math.pi / 6)
        ratio_53 = coverage / density_3 if density_3 > 0 else float('inf')
        ratio_54 = coverage / density_4 if density_4 > 0 else float('inf')
        consistent = coverage <= 1.0
        proj_ok = project_density_constraint(5, k, known_tau)
        elapsed = time.time() - t0
        add_row(
            method='CrossDim_Tau5Check',
            dimension=5,
            parameters=f'tau_5={k}',
            upper_bound='44',
            lower_bound='40',
            runtime=elapsed,
            notes=(f'coverage={coverage * 100:.2f}%; '
                   f'ratio_53={ratio_53:.4f}; '
                   f'ratio_54={ratio_54:.4f}; '
                   f'consistent={consistent}; '
                   f'proj_ok={proj_ok}'),
        )
        print(f'  tau_5={k}: coverage={coverage * 100:.2f}%, consistent={consistent}')

    # Volume and surface area cross-checks for n = 2..9
    for n in range(2, 10):
        t0 = time.time()
        vol = V_n(n)
        surf = S_n(n)
        ratio_vs = surf / vol if vol > 0 else float('inf')
        elapsed = time.time() - t0
        add_row(
            method='CrossDim_VolSurf',
            dimension=n,
            parameters='R=1',
            upper_bound='',
            lower_bound='',
            runtime=elapsed,
            notes=f'V_n={vol:.10f}; S_n={surf:.10f}; S/V={ratio_vs:.6f}; n_check={n / vol * vol:.1f}',
        )

    # Cap area vs dimension for several half-angles
    for theta_deg in [15, 30, 45, 60]:
        theta = math.radians(theta_deg)
        for n in [3, 5, 8]:
            t0 = time.time()
            area = cap_area(n, theta)
            frac = cap_solid_angle(n, theta)
            elapsed = time.time() - t0
            add_row(
                method='CrossDim_CapAreaSweep',
                dimension=n,
                parameters=f'half_angle={theta_deg}deg',
                upper_bound='',
                lower_bound='',
                runtime=elapsed,
                notes=f'cap_area={area:.10f}; frac={frac:.10f}',
            )


# ===================================================================
# Write CSV
# ===================================================================
def write_csv():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f'\nWrote {len(rows)} rows to {CSV_PATH}')


# ===================================================================
# Main
# ===================================================================
def main():
    np.random.seed(SEED)

    print('=' * 72)
    print('COMPREHENSIVE NUMERICAL EXPERIMENTS - KISSING NUMBER PROJECT')
    print('=' * 72)
    print(f'Random seed: {SEED}')
    print(f'Timeout per experiment: {TIMEOUT_PER_EXPERIMENT}s')
    print(f'Output: {CSV_PATH}')

    t_global = time.time()

    # (a) Cap packing bounds -- fast
    run_cap_packing_experiments()

    # (b) Delsarte LP -- only n=3,5 to keep runtime manageable
    run_delsarte_experiments()

    # (c) Enhanced bound -- only n=5
    run_enhanced_bound_experiments()

    # (d) D5 lattice verification -- fast
    run_d5_verification()

    # (e) Greedy spherical code construction -- moderate
    run_greedy_code_experiments()

    # (f) Construction attempts for 41st point -- reduced scale
    run_construction_41_experiments()

    # (g) Cross-dimensional consistency checks -- fast
    run_cross_dim_experiments()

    total_time = time.time() - t_global
    print(f'\n{"=" * 72}')
    print(f'ALL EXPERIMENTS COMPLETED')
    print(f'Total experiments: {len(rows)}')
    print(f'Total time: {total_time:.1f}s')
    print(f'{"=" * 72}')

    write_csv()


if __name__ == '__main__':
    main()
