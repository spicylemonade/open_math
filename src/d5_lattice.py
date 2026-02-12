"""
D5 Lattice Kissing Configuration
Generates and verifies the 40 minimal vectors of the D5 lattice.
"""
import numpy as np
import itertools
import sys

def generate_d5_vectors():
    """Generate all 40 minimal vectors of the D5 lattice.
    
    D5 minimal vectors are all permutations of (+-1, +-1, 0, 0, 0),
    giving C(5,2) * 2^2 = 10 * 4 = 40 vectors.
    """
    vectors = []
    for i in range(5):
        for j in range(i+1, 5):
            for si in [-1, 1]:
                for sj in [-1, 1]:
                    v = np.zeros(5)
                    v[i] = si
                    v[j] = sj
                    vectors.append(v)
    return np.array(vectors)

def normalize_vectors(vectors):
    """Normalize vectors to unit length."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

def verify_kissing_configuration(vectors, tol=1e-10):
    """Verify a kissing configuration: unit vectors with pairwise <v_i,v_j> <= 0.5.

    The kissing number constraint requires angular separation >= 60 degrees,
    i.e., cos(angle) = <v_i, v_j> <= cos(60°) = 0.5 for all i != j.
    Note: inner products can be negative (angles > 90°), which is allowed.
    """
    n = len(vectors)

    # Check unit vectors
    norms = np.linalg.norm(vectors, axis=1)
    unit_ok = np.all(np.abs(norms - 1.0) < tol)

    # Compute Gram matrix
    G = vectors @ vectors.T

    # Check pairwise inner products: <v_i, v_j> <= 0.5 for i != j
    max_inner = -np.inf
    violations = 0
    contact_pairs = []  # pairs achieving equality <v_i, v_j> = 0.5

    for i in range(n):
        for j in range(i+1, n):
            ip = G[i, j]
            if ip > max_inner:
                max_inner = ip
            if ip > 0.5 + tol:
                violations += 1
            if abs(ip - 0.5) < tol:
                contact_pairs.append((i, j))

    return {
        'n_vectors': n,
        'unit_ok': unit_ok,
        'max_inner_product': max_inner,
        'violations': violations,
        'valid': unit_ok and violations == 0,
        'contact_pairs': contact_pairs,
        'n_contact_pairs': len(contact_pairs)
    }

def analyze_contact_graph(vectors, contact_pairs):
    """Analyze the contact graph structure."""
    n = len(vectors)
    degree = np.zeros(n, dtype=int)
    for i, j in contact_pairs:
        degree[i] += 1
        degree[j] += 1
    
    return {
        'degrees': degree,
        'min_degree': int(degree.min()),
        'max_degree': int(degree.max()),
        'mean_degree': float(degree.mean()),
        'degree_distribution': dict(zip(*np.unique(degree, return_counts=True)))
    }

if __name__ == '__main__':
    output_lines = []
    def log(s=""):
        print(s)
        output_lines.append(s)
    
    log("=" * 70)
    log("D5 LATTICE KISSING CONFIGURATION VERIFICATION")
    log("=" * 70)
    
    # Generate vectors
    raw_vectors = generate_d5_vectors()
    log(f"\n1. Generated {len(raw_vectors)} D5 minimal vectors")
    log(f"   Raw vector norms: {np.linalg.norm(raw_vectors, axis=1)[0]:.4f} (all equal)")
    
    # Normalize
    unit_vectors = normalize_vectors(raw_vectors)
    log(f"\n2. Normalized to unit vectors")
    log(f"   Norm check: min={np.linalg.norm(unit_vectors, axis=1).min():.10f}, max={np.linalg.norm(unit_vectors, axis=1).max():.10f}")
    
    # Verify
    result = verify_kissing_configuration(unit_vectors)
    log(f"\n3. Kissing configuration verification:")
    log(f"   Number of vectors: {result['n_vectors']}")
    log(f"   All unit vectors: {result['unit_ok']}")
    log(f"   Max <v_i, v_j> (i!=j): {result['max_inner_product']:.10f}")
    log(f"   Violations (<v_i,v_j> > 0.5): {result['violations']}")
    log(f"   VALID KISSING CONFIGURATION: {result['valid']}")
    
    # Contact graph
    log(f"\n4. Contact graph (pairs with <v_i,v_j> = 0.5, i.e. angle exactly 60°):")
    log(f"   Number of contact pairs: {result['n_contact_pairs']}")
    log(f"   Total possible pairs: {result['n_vectors'] * (result['n_vectors']-1) // 2}")
    
    cg = analyze_contact_graph(unit_vectors, result['contact_pairs'])
    log(f"\n5. Contact graph structure:")
    log(f"   Min degree: {cg['min_degree']}")
    log(f"   Max degree: {cg['max_degree']}")
    log(f"   Mean degree: {cg['mean_degree']:.2f}")
    log(f"   Degree distribution: {dict((int(k), int(v)) for k, v in cg['degree_distribution'].items())}")
    
    # Inner product spectrum
    G = unit_vectors @ unit_vectors.T
    inner_products = []
    for i in range(len(unit_vectors)):
        for j in range(i+1, len(unit_vectors)):
            inner_products.append(G[i,j])
    inner_products = np.array(inner_products)
    unique_ips = np.unique(np.round(inner_products, 10))
    log(f"\n6. Inner product spectrum:")
    for ip in sorted(unique_ips):
        count = np.sum(np.abs(inner_products - ip) < 1e-10)
        log(f"   <v_i, v_j> = {ip:+.4f}: {count} pairs")
    
    log(f"\n7. First 5 vectors (normalized):")
    for i in range(5):
        log(f"   v_{i} = [{', '.join(f'{x:.4f}' for x in unit_vectors[i])}]")
    
    log(f"\n{'='*70}")
    log(f"CONCLUSION: The D5 lattice provides a valid kissing configuration")
    log(f"of {result['n_vectors']} unit spheres in R^5, confirming tau_5 >= 40.")
    log(f"{'='*70}")
    
    # Save output
    with open('/home/codex/work/repo/results/d5_verification.txt', 'w') as f:
        f.write('\n'.join(output_lines))
    print("\nOutput saved to results/d5_verification.txt")
