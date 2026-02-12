"""
Spherical Code Validator and Optimizer.

Tools for validating and constructing kissing configurations
(spherical codes with minimum angular separation >= 60 degrees).
"""
import numpy as np
from scipy.optimize import minimize


def validate_kissing_config(vectors, tol=1e-8):
    """Validate a kissing configuration.

    Checks:
    1. All vectors are unit vectors
    2. All pairwise inner products <= 0.5 (angular separation >= 60 degrees)

    Args:
        vectors: array of shape (k, n) where k is number of vectors, n is dimension
        tol: tolerance for floating point comparisons

    Returns:
        dict with 'valid', 'n_vectors', 'dimension', 'violations', 'max_inner_product'
    """
    vectors = np.asarray(vectors, dtype=float)
    k, n = vectors.shape

    # Check unit vectors
    norms = np.linalg.norm(vectors, axis=1)
    norm_violations = np.sum(np.abs(norms - 1.0) > tol)

    # Compute Gram matrix
    G = vectors @ vectors.T

    # Check pairwise inner products
    max_inner = -np.inf
    violations = []
    for i in range(k):
        for j in range(i + 1, k):
            ip = G[i, j]
            if ip > max_inner:
                max_inner = ip
            if ip > 0.5 + tol:
                violations.append((i, j, ip))

    return {
        'valid': norm_violations == 0 and len(violations) == 0,
        'n_vectors': k,
        'dimension': n,
        'norm_violations': int(norm_violations),
        'angle_violations': violations,
        'n_angle_violations': len(violations),
        'max_inner_product': float(max_inner)
    }


def greedy_spherical_code(n, target_k, min_angle_deg=60.0, n_attempts=10, seed=42):
    """Attempt to place target_k points on S^{n-1} with minimum angular separation.

    Uses greedy placement followed by gradient-based local optimization.

    Args:
        n: dimension
        target_k: target number of points
        min_angle_deg: minimum angular separation in degrees
        n_attempts: number of random restarts
        seed: random seed

    Returns:
        dict with 'vectors', 'n_placed', 'valid', 'min_angle_achieved'
    """
    rng = np.random.RandomState(seed)
    cos_min = np.cos(np.radians(min_angle_deg))  # = 0.5 for 60 degrees

    best_result = None
    best_n_placed = 0

    for attempt in range(n_attempts):
        vectors = []

        # Try to greedily add points
        for _ in range(target_k * 100):  # max iterations
            if len(vectors) >= target_k:
                break

            # Random point on S^{n-1}
            v = rng.randn(n)
            v = v / np.linalg.norm(v)

            # Check against existing vectors
            ok = True
            for u in vectors:
                if np.dot(v, u) > cos_min:
                    ok = False
                    break

            if ok:
                vectors.append(v)

        n_placed = len(vectors)
        if n_placed > best_n_placed:
            best_n_placed = n_placed
            best_result = np.array(vectors)

    if best_result is None:
        return {'vectors': None, 'n_placed': 0, 'valid': False, 'min_angle_achieved': 0.0}

    # Try to optimize placement via scipy
    def objective(x):
        """Minimize the maximum inner product (want it <= cos_min)."""
        pts = x.reshape(-1, n)
        # Project to unit sphere
        norms = np.linalg.norm(pts, axis=1, keepdims=True)
        pts = pts / np.maximum(norms, 1e-10)
        G = pts @ pts.T
        # Penalize inner products > cos_min
        penalty = 0.0
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                excess = max(0, G[i, j] - cos_min)
                penalty += excess ** 2
        return penalty

    if best_n_placed >= target_k:
        x0 = best_result[:target_k].flatten()
        try:
            res = minimize(objective, x0, method='L-BFGS-B', options={'maxiter': 1000})
            optimized = res.x.reshape(-1, n)
            norms = np.linalg.norm(optimized, axis=1, keepdims=True)
            optimized = optimized / np.maximum(norms, 1e-10)
            best_result = optimized
        except Exception:
            pass

    # Compute actual minimum angle
    G = best_result @ best_result.T
    min_angle = 180.0
    for i in range(len(best_result)):
        for j in range(i + 1, len(best_result)):
            cos_a = np.clip(G[i, j], -1, 1)
            angle = np.degrees(np.arccos(cos_a))
            min_angle = min(min_angle, angle)

    validation = validate_kissing_config(best_result)

    return {
        'vectors': best_result,
        'n_placed': len(best_result),
        'valid': validation['valid'],
        'min_angle_achieved': min_angle,
        'max_inner_product': validation['max_inner_product']
    }


if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/home/codex/work/repo/src')
    from d5_lattice import generate_d5_vectors, normalize_vectors

    print("=" * 70)
    print("SPHERICAL CODE VALIDATOR AND OPTIMIZER")
    print("=" * 70)

    # Test 1: Validate D5 configuration
    print("\n1. Validate 40-point D5 configuration:")
    d5 = normalize_vectors(generate_d5_vectors())
    result = validate_kissing_config(d5)
    print(f"   Valid: {result['valid']}")
    print(f"   Vectors: {result['n_vectors']}, Dimension: {result['dimension']}")
    print(f"   Max inner product: {result['max_inner_product']:.6f}")
    print(f"   Angle violations: {result['n_angle_violations']}")

    # Test 2: Try to construct 41-point configuration
    print("\n2. Attempt 41-point configuration in R^5:")
    r41 = greedy_spherical_code(5, 41, seed=42)
    print(f"   Points placed: {r41['n_placed']}")
    print(f"   Valid: {r41['valid']}")
    print(f"   Min angle: {r41['min_angle_achieved']:.2f} degrees")

    # Test 3: Random 45-point should fail
    print("\n3. Validate random 45-point configuration:")
    rng = np.random.RandomState(42)
    random_45 = rng.randn(45, 5)
    random_45 = random_45 / np.linalg.norm(random_45, axis=1, keepdims=True)
    result_45 = validate_kissing_config(random_45)
    print(f"   Valid: {result_45['valid']}")
    print(f"   Angle violations: {result_45['n_angle_violations']}")
    print(f"   Max inner product: {result_45['max_inner_product']:.6f}")
