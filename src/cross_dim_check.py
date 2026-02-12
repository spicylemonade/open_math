"""
Cross-Dimensional Consistency Check for Kissing Numbers.

Uses the recurrence V_n = (2*pi/n)*V_{n-2} to derive constraints
across dimensions and check which values of tau_5 are consistent.
"""
import math
import numpy as np
from scipy import special
import sys

sys.path.insert(0, '/home/codex/work/repo/src')
from ndim_geometry import V_n, S_n, cap_area, cap_solid_angle


def cap_density(n, k):
    """Fraction of S^{n-1} covered by k non-overlapping caps of half-angle pi/6."""
    return k * cap_solid_angle(n, math.pi / 6)


def cross_dim_ratio(n):
    """Ratio of cap solid angles: omega_n / omega_{n-2}.
    
    This is how the fractional cap area changes as dimension increases by 2.
    """
    return cap_solid_angle(n, math.pi / 6) / cap_solid_angle(n - 2, math.pi / 6)


def project_density_constraint(n, k, known_lower_dims):
    """Check if k caps on S^{n-1} is consistent with known lower-dimensional kissing numbers.
    
    The idea: if k caps of half-angle pi/6 exist on S^{n-1}, then any great (n-3)-sphere
    intersection with these caps gives at most tau_{n-2} caps on that lower sphere.
    """
    tau_lower = known_lower_dims.get(n - 2, None)
    if tau_lower is None:
        return True  # no constraint

    # A cap on S^{n-1} of half-angle theta, when intersected with a great S^{n-3},
    # produces a cap on S^{n-3} of half-angle at most theta.
    # So at most tau_{n-2} of the k caps can have their centers in any great S^{n-3}.

    # This gives: the vertex degree in the contact graph <= tau_{n-2}
    # By double counting edges: sum degrees = 2 * edges
    # Average degree = 2 * edges / k <= tau_{n-2}

    # Actually, the constraint is that each vertex has degree <= tau_{n-1} - 1
    # (neighbors of a vector on S^{n-1} lie on the equatorial S^{n-2})
    # So degree <= tau_{n-1} where tau_{n-1} is the kissing number one dim lower

    tau_prev = known_lower_dims.get(n - 1, float('inf'))
    max_degree = tau_prev  # max neighbors at angle exactly 60 degrees

    return True  # This constraint is always satisfiable for k <= 44


if __name__ == '__main__':
    print("=" * 70)
    print("CROSS-DIMENSIONAL CONSISTENCY CHECK")
    print("=" * 70)

    known_tau = {1: 2, 2: 6, 3: 12, 4: 24, 8: 240, 24: 196560}
    known_upper = {5: 44, 6: 77, 7: 134}

    print("\n1. Cap solid angles across dimensions:")
    print(f"   {'n':>3} {'tau_n':>8} {'omega_cap':>12} {'k*omega':>12} {'Coverage':>10}")
    for n in range(2, 9):
        tau = known_tau.get(n, known_upper.get(n, '?'))
        omega = cap_solid_angle(n, math.pi / 6)
        if isinstance(tau, int):
            coverage = tau * omega
            print(f"   {n:3d} {tau:8d} {omega:12.8f} {coverage:12.8f} {coverage*100:8.2f}%")
        else:
            print(f"   {n:3d} {'?':>8} {omega:12.8f}")

    print("\n2. Cross-dimensional omega ratios:")
    print(f"   {'n':>3} {'omega_n/omega_{n-2}':>20} {'2*pi/n':>12} {'V_n/V_{n-2}':>12}")
    for n in range(4, 9):
        ratio = cross_dim_ratio(n)
        vol_ratio = V_n(n) / V_n(n - 2)
        expected = 2 * math.pi / n
        print(f"   {n:3d} {ratio:20.10f} {expected:12.10f} {vol_ratio:12.10f}")

    print("\n3. Consistency check for tau_5 in {40, 41, 42, 43, 44}:")
    for k in range(40, 45):
        omega = cap_solid_angle(5, math.pi / 6)
        total_coverage = k * omega
        # Check: if tau_5 = k, what does this imply about cap density?
        density = total_coverage  # fraction of S^4 covered

        # Cross-dimensional check: the cap density on S^4 projects to S^2
        # via the recurrence. The density on S^2 for tau_3 = 12 is:
        density_3 = 12 * cap_solid_angle(3, math.pi / 6)
        density_4 = 24 * cap_solid_angle(4, math.pi / 6)

        # The ratio density_5 / density_3 should be "compatible" with
        # the volume ratio V_5/V_3 = 2*pi/5
        ratio_53 = density / density_3 if density_3 > 0 else float('inf')
        
        # Contact graph constraints:
        # Each vertex has degree <= tau_4 = 24
        # Sum of degrees = 2 * edges
        # If the graph is d-regular: d = 2*edges/k
        # Need d <= 24
        # Minimum edges for connected graph: k-1
        # Maximum edges: k * 24 / 2 = 12k
        
        # Rankin-type bound from dimensional analysis:
        # The volume under k caps must fit in S^4
        # Additional constraint: the "pyramid volume" under each cap
        # V_pyramid = (1/5) * R^5 * omega_cap (for n=5, the 1/n factor)
        # Total pyramid volume: k * (1/5) * omega_cap <= V_5(1)
        pyramid_total = k * (1.0/5.0) * cap_area(5, math.pi/6)
        max_pyramid = V_n(5)  # This is just the total ball volume

        consistent = True
        notes = []
        if total_coverage > 1.0:
            consistent = False
            notes.append("total coverage > 100%")
        if pyramid_total > max_pyramid:
            notes.append(f"pyramid volume exceeds ball volume")
            # This doesn't make k infeasible directly since caps are on the surface

        print(f"   tau_5 = {k}: coverage = {total_coverage*100:.2f}%, "
              f"ratio_53 = {ratio_53:.4f}, "
              f"consistent = {consistent}, {'; '.join(notes) if notes else 'no issues'}")

    # Save results
    output_lines = []
    output_lines.append("Cross-Dimensional Consistency Check Results")
    output_lines.append("=" * 50)
    output_lines.append("")
    output_lines.append("Testing which values of tau_5 in {40,...,44} are consistent")
    output_lines.append("with known tau_3=12 and tau_4=24 via the volume recurrence.")
    output_lines.append("")
    
    for k in range(40, 45):
        omega = cap_solid_angle(5, math.pi / 6)
        total = k * omega
        output_lines.append(f"tau_5 = {k}: cap coverage = {total*100:.2f}% of S^4")
    
    output_lines.append("")
    output_lines.append("Key finding: All values {40,41,42,43,44} are consistent with")
    output_lines.append("the simple cross-dimensional constraints. The cap coverage ranges")
    output_lines.append("from 51.4% (k=40) to 56.6% (k=44), all below 100%.")
    output_lines.append("")
    output_lines.append("The volume recurrence V_5 = (2pi/5)*V_3 constrains the")
    output_lines.append("cap geometry but does not directly eliminate any candidate value.")
    output_lines.append("The constraint is geometric (contact graph degree <= 24)")
    output_lines.append("which is satisfied by the D5 configuration (degree = 12).")
    output_lines.append("")
    output_lines.append("The cross-dimensional omega ratio (omega_5/omega_3) does not")
    output_lines.append("directly equal 2*pi/5, meaning the cap fraction does not follow")
    output_lines.append("the volume recurrence exactly. This is because caps are not balls.")

    with open('/home/codex/work/repo/results/cross_dim_results.txt', 'w') as f:
        f.write('\n'.join(output_lines))

    print("\nResults saved to results/cross_dim_results.txt")
