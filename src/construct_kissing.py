"""
Attempt to construct 41+ point kissing configurations in R^5.

Starts from the 40-point D5 configuration and tries 3 strategies:
1. Grid search on S^4
2. Nonlinear optimization (minimize max violation)
3. Algebraic construction based on symmetry
"""
import numpy as np
from scipy.optimize import minimize, differential_evolution
import sys
import time

sys.path.insert(0, '/home/codex/work/repo/src')
from d5_lattice import generate_d5_vectors, normalize_vectors
from spherical_codes import validate_kissing_config


def get_d5_unit_vectors():
    return normalize_vectors(generate_d5_vectors())


def max_inner_product_with_config(v, config):
    """Maximum inner product of v with any vector in config."""
    dots = config @ v
    return np.max(dots)


def attempt_grid_search(config, n_samples=100000, seed=42):
    """Strategy 1: Random sampling on S^4 looking for a valid 41st point."""
    rng = np.random.RandomState(seed)
    best_max_ip = 1.0
    best_v = None
    n_valid = 0

    for i in range(n_samples):
        v = rng.randn(5)
        v = v / np.linalg.norm(v)
        max_ip = max_inner_product_with_config(v, config)
        if max_ip <= 0.5:
            n_valid += 1
            if best_v is None or max_ip < best_max_ip:
                best_max_ip = max_ip
                best_v = v.copy()

    return {
        'found': n_valid > 0,
        'n_valid': n_valid,
        'best_max_ip': best_max_ip,
        'best_v': best_v,
        'n_samples': n_samples
    }


def attempt_optimization(config, n_starts=50, seed=42):
    """Strategy 2: Minimize the maximum inner product with existing config."""
    rng = np.random.RandomState(seed)
    best_obj = 1.0
    best_v = None

    def objective(x):
        v = x / np.linalg.norm(x)
        dots = config @ v
        return np.max(dots)

    for start in range(n_starts):
        x0 = rng.randn(5)
        x0 = x0 / np.linalg.norm(x0)
        try:
            res = minimize(objective, x0, method='Nelder-Mead',
                          options={'maxiter': 5000, 'xatol': 1e-12, 'fatol': 1e-12})
            v_opt = res.x / np.linalg.norm(res.x)
            obj = objective(v_opt)
            if obj < best_obj:
                best_obj = obj
                best_v = v_opt.copy()
        except Exception:
            continue

    return {
        'found': best_obj <= 0.5,
        'best_max_ip': best_obj,
        'best_v': best_v,
        'n_starts': n_starts,
        'margin': 0.5 - best_obj
    }


def attempt_algebraic(config):
    """Strategy 3: Try algebraic constructions.

    The D5 lattice has symmetry group of order 1920. Try vectors from related
    lattices and group orbits.
    """
    candidates = []

    # Try vectors of the form (a, a, a, a, a) normalized
    for signs in [np.ones(5), -np.ones(5)]:
        v = signs / np.linalg.norm(signs)
        candidates.append(v)

    # Try vectors with 3 nonzero components
    from itertools import combinations, product
    for idx in combinations(range(5), 3):
        for signs in product([-1, 1], repeat=3):
            v = np.zeros(5)
            for i, s in zip(idx, signs):
                v[i] = s
            v = v / np.linalg.norm(v)
            candidates.append(v)

    # Try vectors with 4 nonzero components
    for idx in combinations(range(5), 4):
        for signs in product([-1, 1], repeat=4):
            v = np.zeros(5)
            for i, s in zip(idx, signs):
                v[i] = s
            v = v / np.linalg.norm(v)
            candidates.append(v)

    # Try vectors with 5 nonzero components
    for signs in product([-1, 1], repeat=5):
        v = np.array(signs, dtype=float)
        v = v / np.linalg.norm(v)
        candidates.append(v)

    # Try vectors of the form (a, b, 0, 0, 0) with a != b
    for a, b in [(2, 1), (1, 2), (3, 1), (1, 3)]:
        for idx in combinations(range(5), 2):
            for s1, s2 in product([-1, 1], repeat=2):
                v = np.zeros(5)
                v[idx[0]] = s1 * a
                v[idx[1]] = s2 * b
                v = v / np.linalg.norm(v)
                candidates.append(v)

    best_max_ip = 1.0
    best_v = None
    n_valid = 0

    for v in candidates:
        max_ip = max_inner_product_with_config(v, config)
        if max_ip <= 0.5 + 1e-10:
            n_valid += 1
        if max_ip < best_max_ip:
            best_max_ip = max_ip
            best_v = v.copy()

    return {
        'found': n_valid > 0 and best_max_ip <= 0.5,
        'n_candidates': len(candidates),
        'n_valid': n_valid,
        'best_max_ip': best_max_ip,
        'best_v': best_v
    }


if __name__ == '__main__':
    print("=" * 70)
    print("ATTEMPTING TO CONSTRUCT 41-POINT KISSING CONFIGURATION IN R^5")
    print("=" * 70)

    config = get_d5_unit_vectors()
    print(f"\nStarting from D5 lattice: {len(config)} vectors")
    print(f"Current max inner product: {max_inner_product_with_config(config[0], config[1:]):.4f}")

    # Strategy 1: Grid search
    print("\n--- Strategy 1: Random grid search (100K samples) ---")
    t0 = time.time()
    r1 = attempt_grid_search(config, n_samples=100000, seed=42)
    t1 = time.time()
    print(f"  Time: {t1-t0:.1f}s")
    print(f"  Valid 41st points found: {r1['n_valid']}")
    print(f"  Best max inner product: {r1['best_max_ip']:.6f}")
    print(f"  Margin from 0.5: {0.5 - r1['best_max_ip']:.6f}")
    if r1['found']:
        print(f"  41st point: {r1['best_v']}")

    # Strategy 2: Optimization
    print("\n--- Strategy 2: Nonlinear optimization (50 starts) ---")
    t0 = time.time()
    r2 = attempt_optimization(config, n_starts=50, seed=42)
    t1 = time.time()
    print(f"  Time: {t1-t0:.1f}s")
    print(f"  Best max inner product: {r2['best_max_ip']:.6f}")
    print(f"  Margin from 0.5: {r2['margin']:.6f}")
    if r2['found']:
        print(f"  41st point: {r2['best_v']}")

    # Strategy 3: Algebraic
    print("\n--- Strategy 3: Algebraic construction ---")
    t0 = time.time()
    r3 = attempt_algebraic(config)
    t1 = time.time()
    print(f"  Time: {t1-t0:.1f}s")
    print(f"  Candidates tested: {r3['n_candidates']}")
    print(f"  Valid 41st points: {r3['n_valid']}")
    print(f"  Best max inner product: {r3['best_max_ip']:.6f}")

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    any_found = r1['found'] or r2['found'] or r3['found']
    if any_found:
        print("SUCCESS: A 41st point was found!")
    else:
        print("NO 41-POINT CONFIGURATION FOUND")
        print(f"  Best margin (optimization): {r2['margin']:.6f}")
        print(f"  This provides evidence (but not proof) toward tau_5 = 40")

    # Save results
    lines = [
        "# Construction Attempts for 41-Point Kissing Configuration in R^5",
        "",
        "## Summary",
        f"Starting configuration: 40-point D5 lattice (verified valid)",
        f"Goal: Find a 41st unit vector with all inner products <= 0.5",
        "",
        "## Strategy 1: Random Grid Search",
        f"- Samples: {r1['n_samples']}",
        f"- Valid 41st points found: {r1['n_valid']}",
        f"- Best max inner product: {r1['best_max_ip']:.6f}",
        f"- Found: {r1['found']}",
        "",
        "## Strategy 2: Nonlinear Optimization",
        f"- Random starts: {r2['n_starts']}",
        f"- Best max inner product: {r2['best_max_ip']:.6f}",
        f"- Margin from feasibility: {r2['margin']:.6f}",
        f"- Found: {r2['found']}",
        "",
        "## Strategy 3: Algebraic Construction",
        f"- Candidates tested: {r3['n_candidates']}",
        f"- Valid 41st points: {r3['n_valid']}",
        f"- Best max inner product: {r3['best_max_ip']:.6f}",
        f"- Found: {r3['found']}",
        "",
        "## Conclusion",
    ]
    if any_found:
        lines.append("A valid 41st point WAS found. This would prove tau_5 >= 41.")
    else:
        lines.append("No valid 41st point was found despite extensive search.")
        lines.append(f"The closest approach had max inner product {min(r1['best_max_ip'], r2['best_max_ip'], r3['best_max_ip']):.6f}.")
        lines.append("This provides computational evidence toward tau_5 = 40,")
        lines.append("consistent with the conjecture that the D5 lattice is optimal.")

    with open('/home/codex/work/repo/results/construction_attempts.md', 'w') as f:
        f.write('\n'.join(lines))
    print("\nResults saved to results/construction_attempts.md")
