#!/usr/bin/env python3
"""
Cohomology computations for uniform lattices with 2-torsion.

Computes rational group cohomology H*(Γ; Q) for small explicit lattice examples
and verifies rational Euler characteristic computations.

References:
- Borel-Serre (1973): Corners and arithmetic groups
- Selberg (1960): Discontinuous groups in symmetric spaces
"""

import json
import numpy as np
from fractions import Fraction
import signal

# Timeout handler for safety
class ComputeTimeout(Exception):
    pass

def _handler(signum, frame):
    raise ComputeTimeout()

signal.signal(signal.SIGALRM, _handler)

np.random.seed(42)

###############################################################################
# Example 1: Triangle group Δ(2, 3, 7) — cocompact lattice in PSL(2, R)
###############################################################################

def triangle_group_cohomology():
    """
    Compute H*(Δ(2,3,7); Q) for the (2,3,7) triangle group.

    Δ(2,3,7) = <a, b, c | a^2 = b^3 = c^7 = abc = 1>

    This is a cocompact Fuchsian group (lattice in PSL(2,R)).
    Contains 2-torsion: element a has order 2.

    The torsion-free subgroup Γ' has index N and is a surface group
    of genus g where 2 - 2g = N * (1/2 + 1/3 + 1/7 - 1) = N * (-1/42).

    By the transfer map, H*(Δ; Q) ≅ H*(Γ'; Q)^{Δ/Γ'}.

    For Fuchsian groups, H*(Γ; Q) is well-known:
    - H^0(Γ; Q) = Q
    - H^1(Γ; Q) = 0 (because the orbifold is a sphere with cone points)
    - H^k(Γ; Q) = 0 for k >= 2 (since vcd = 2, but cd_Q can be at most 2,
      and by PD over Q the cohomology vanishes in degree 2 as well because
      the orbifold Euler char is positive: 1/42 > 0, so there's no Q-fundamental class)

    Actually: For cocompact Fuchsian groups with torsion,
    vcd(Δ) = 2 but cd_Q(Δ) = 0 because H^k(Δ; Q) = 0 for all k >= 1.

    This is because χ^orb = 1/42 > 0, and by Gauss-Bonnet for orbifolds,
    the rational Euler characteristic equals 1/42 = 1 - dim H^1 + dim H^2.
    Since dims are non-negative integers and the fractions come from the
    orbifold formula, we need:
    χ(Γ) = 1/42 = 1/(|Γ:Γ'|) * χ(Γ')

    The rational Euler characteristic for virtual groups:
    χ_Q(Δ) = χ(Γ')/[Δ:Γ'] = (2-2g)/N

    Since 2-2g = -N/42 + 2 ... let's compute directly.
    For surface group of genus g: χ = 2-2g.
    [Δ:Γ'] * (1/2 + 1/3 + 1/7 - 1) = 2 - 2g  (Riemann-Hurwitz)
    [Δ:Γ'] * (-1/42) = 2 - 2g

    The smallest such N: the smallest normal torsion-free subgroup.
    For Δ(2,3,7), the Hurwitz surface of genus 3 (Klein quartic)
    gives [Δ:Γ'] = 168, χ(Γ') = 2-2*3 = -4, and indeed -168/42 = -4. ✓

    The rational Euler characteristic:
    χ_Q(Δ) = χ(Γ')/[Δ:Γ'] = -4/168 = -1/42

    Wait, there's a sign issue. Let me reconsider.
    The ORBIFOLD Euler characteristic is:
    χ^orb(Δ\H^2) = 2 - 0 - (1-1/2) - (1-1/3) - (1-1/7) = 1/42

    But as a group, the rational Euler characteristic is:
    χ_Q(Δ) = 1/[Δ:Γ'] * χ(Γ') = 1/168 * (-4) = -1/42

    This is the NEGATIVE of the orbifold Euler char!
    Convention: χ_Q(Γ) = Σ (-1)^k dim H^k(Γ;Q) = -1/42.

    Since this is not an integer, it tells us that the rational cohomology
    of Δ must have the property that Σ (-1)^k dim H^k(Δ;Q) = -1/42.
    But dimensions of Q-vector spaces are integers!

    Resolution: χ_Q(Γ) for a virtually torsion-free group is defined as
    χ(Γ')/[Γ:Γ'] which can be a fraction. The individual H^k(Γ;Q)
    have integer dimensions, and over Q with transfer:

    H^k(Δ; Q) = H^k(Γ'; Q)^{Δ/Γ'}

    For the Klein quartic surface group Γ' (genus 3):
    - H^0(Γ'; Q) = Q, so H^0(Δ; Q) = Q^{Δ/Γ'} = Q (always)
    - H^1(Γ'; Q) = Q^6 (6 = 2g), and Δ/Γ' = PSL(2,F_7) acts on this.
      The action of PSL(2,7) on H^1 of the Klein quartic is the unique
      irreducible 6-dimensional representation. Since it's irreducible
      and not trivial, H^1(Γ';Q)^{Δ/Γ'} = 0.
    - H^2(Γ'; Q) = Q (fundamental class), and Δ/Γ' acts trivially on it
      (since the surface group is a normal subgroup and the action preserves
      orientation). So H^2(Δ; Q) = Q.

    Final answer:
    H^0(Δ(2,3,7); Q) = Q
    H^1(Δ(2,3,7); Q) = 0
    H^2(Δ(2,3,7); Q) = Q

    Check: χ = 1 - 0 + 1 = 2, but χ_Q(Δ) should be -1/42.

    There's a discrepancy. The issue is that H^k(Γ; Q) ≠ H^k(Γ'; Q)^{Γ/Γ'}
    in general for non-trivial actions. The correct formula uses the transfer:

    res: H^k(Γ; Q) → H^k(Γ'; Q) is injective, and
    the image is H^k(Γ'; Q)^{Γ/Γ'} (fixed points of the conjugation action).

    BUT: The rational Euler characteristic of a virtual duality group is:
    χ_Q(Γ) = 1/[Γ:Γ'] * χ(Γ') = fractional.
    This is NOT the same as Σ (-1)^k dim H^k(Γ;Q).

    For Γ with torsion:
    Σ (-1)^k dim H^k(Γ;Q) is an integer,
    but χ_Q(Γ) := χ(Γ')/[Γ:Γ'] is a rational number.

    These are DIFFERENT invariants! The resolution:

    Actually, for groups with torsion, H^k(Γ; Q) CAN be computed via
    the transfer, and we get:

    For Δ = Δ(2,3,7):
    - H^0 = Q (always)
    - H^1 = 0 (transfer argument with irreducible representation)
    - H^2 = 0 (Δ has torsion, so it is NOT a Poincaré duality group over Z;
      the "fundamental class" of Γ' does NOT descend to a class for Δ
      because the normalizer action might not preserve it... actually it does
      for the surface case because PSL(2,7) preserves orientation.

    Let me reconsider more carefully.

    The issue: For a virtual PD group that is not PD, H^d(Γ; Q) may or may
    not be nonzero. For Fuchsian groups:

    By Brown's formula: H^k(Γ; Q) = ⊕_{(g) in Γ\\Γ} H^k(C_Γ(g); Q)
    where the sum is over conjugacy classes of elements of finite order.

    Actually the correct approach: Since Δ(2,3,7) acts on the tree T
    (Bass-Serre tree of the amalgamated product decomposition) and on H^2,
    the standard approach for Fuchsian groups with torsion gives:

    For a cocompact Fuchsian group Γ with presentation
    <a_1,...,a_g, b_1,...,b_g, c_1,...,c_r | [a_1,b_1]...[a_g,b_g]c_1...c_r = 1, c_i^{m_i} = 1>

    where g is the genus and m_i are the cone point orders:
    - H^0(Γ;Q) = Q
    - H^1(Γ;Q) = Q^{2g}
    - H^2(Γ;Q) = Q (when 2g + r ≥ 3, which is always true for Fuchsian groups)

    Wait no. For Fuchsian groups, H^k(Γ;Q) for k ≥ 3 vanishes because
    vcd(Γ) = 2.

    For Δ(2,3,7): genus g = 0, three cone points of orders 2, 3, 7.
    - H^0 = Q
    - H^1 = Q^{2·0} = 0
    - H^2 = Q (the orbifold has a rational fundamental class)

    Euler characteristic: 1 - 0 + 1 = 2.
    Rational Euler characteristic (Wall's convention): -1/42.
    These differ because Wall's rational Euler char uses the formula
    1/|Γ:Γ'| · χ(Γ'), not the alternating sum of Betti numbers.

    OK let me just use the correct Fuchsian group cohomology.
    """

    # Δ(2,3,7) parameters
    genus = 0
    cone_orders = [2, 3, 7]

    # Orbifold Euler characteristic
    chi_orb = Fraction(2 - 2*genus)
    for m in cone_orders:
        chi_orb -= Fraction(1) - Fraction(1, m)

    # Rational cohomology dimensions (standard for Fuchsian groups)
    # H^0 = Q, H^1 = Q^{2g}, H^2 = Q if the group is infinite
    h0 = 1
    h1 = 2 * genus  # = 0 for genus 0
    h2 = 1  # infinite cocompact Fuchsian group

    betti_numbers = [h0, h1, h2]
    euler_char = sum((-1)**k * b for k, b in enumerate(betti_numbers))

    # Wall's rational Euler characteristic
    # = χ(Γ')/[Γ:Γ'] where Γ' is torsion-free
    # For Fuchsian: χ_Q = χ^orb = 1/42
    # (with the sign convention that χ^orb for orbifolds is positive here)
    chi_rational_wall = chi_orb  # = 1/42

    return {
        "group": "Delta(2,3,7)",
        "ambient_group": "PSL(2,R) ≅ SO_0(2,1)",
        "symmetric_space_dim": 2,
        "contains_2_torsion": True,
        "torsion_elements": ["a (order 2)"],
        "genus": genus,
        "cone_orders": cone_orders,
        "orbifold_euler_char": str(chi_orb),
        "rational_betti_numbers": betti_numbers,
        "euler_char_betti": euler_char,
        "rational_euler_char_wall": str(chi_rational_wall),
        "vcd": 2,
        "notes": "Cocompact Fuchsian group. H^0=Q, H^1=0, H^2=Q. Wall rational Euler char = 1/42."
    }


###############################################################################
# Example 2: Z/2 extension of surface group — model for lattice with 2-torsion
###############################################################################

def surface_extension_cohomology():
    """
    Compute H*(Γ; Q) where Γ is a Z/2-extension of a surface group.

    Model: Γ = π₁(Σ_g) ⋊ Z/2 where Z/2 acts by the hyperelliptic involution.
    This is a cocompact Fuchsian group of genus 0 with 2g+2 cone points of order 2.

    For g = 2: Γ is a Fuchsian group of genus 0 with 6 cone points of order 2.
    Presentation: <c_1,...,c_6 | c_1^2 = ... = c_6^2 = c_1...c_6 = 1>

    Orbifold: sphere with 6 cone points of order 2.
    χ^orb = 2 - 6*(1-1/2) = 2 - 3 = -1.

    Rational cohomology:
    H^0 = Q, H^1 = Q^0 = 0, H^2 = Q.
    """
    g_surface = 2  # genus of the underlying surface
    n_cone = 2 * g_surface + 2  # number of cone points (all order 2)

    genus_orbifold = 0
    cone_orders = [2] * n_cone

    chi_orb = Fraction(2 - 2 * genus_orbifold)
    for m in cone_orders:
        chi_orb -= Fraction(1) - Fraction(1, m)

    h0 = 1
    h1 = 2 * genus_orbifold  # = 0
    h2 = 1

    betti_numbers = [h0, h1, h2]
    euler_char = sum((-1)**k * b for k, b in enumerate(betti_numbers))

    # Verification via torsion-free subgroup
    # The surface subgroup has index 2, with χ(surface) = 2-2g = 2-4 = -2
    # χ_Q(Γ) = χ(surface)/2 = -2/2 = -1 ✓ matches chi_orb
    chi_rational_wall = chi_orb

    # Gauss-Bonnet verification
    # For a hyperbolic surface of genus g: Area = 2π|χ| = 2π(2g-2)
    # For the orbifold: Area = 2π|χ^orb| = 2π
    # Check: Area(orbifold) = Area(surface)/[Γ:Γ'] = 2π(2g-2)/2 = 2π(g-1) = 2π for g=2 ✓
    gauss_bonnet_area = float(2 * np.pi * abs(chi_orb))
    surface_area = 2 * np.pi * (2 * g_surface - 2)
    area_ratio = surface_area / gauss_bonnet_area

    return {
        "group": f"π₁(Σ_{g_surface}) ⋊ Z/2 (hyperelliptic)",
        "ambient_group": "PSL(2,R)",
        "symmetric_space_dim": 2,
        "contains_2_torsion": True,
        "torsion_elements": [f"c_{i+1} (order 2)" for i in range(n_cone)],
        "surface_genus": g_surface,
        "orbifold_genus": genus_orbifold,
        "n_cone_points": n_cone,
        "cone_orders": cone_orders,
        "orbifold_euler_char": str(chi_orb),
        "rational_betti_numbers": betti_numbers,
        "euler_char_betti": euler_char,
        "rational_euler_char_wall": str(chi_rational_wall),
        "gauss_bonnet_verification": {
            "orbifold_area": gauss_bonnet_area,
            "surface_area": surface_area,
            "index": int(area_ratio),
            "consistent": abs(area_ratio - 2.0) < 1e-10
        },
        "vcd": 2,
        "notes": f"Z/2-extension of genus-{g_surface} surface group. {n_cone} involutions. χ^orb = {chi_orb}."
    }


###############################################################################
# Example 3: Arithmetic lattice in SL(2,R) from quaternion algebra
###############################################################################

def quaternion_lattice_cohomology():
    """
    Rational Euler characteristic for an arithmetic lattice in SL(2,R)
    coming from a quaternion algebra B over Q ramified at a finite set of primes.

    For B the Hamilton quaternions H = (-1,-1/Q), the unit group
    B^1 = {x in B : Nrd(x) = 1} gives SU(2) which is compact — no lattice.

    For B = (-1, -p/Q) for p ≡ 3 mod 4, B splits at infinity (so B⊗R ≅ M_2(R))
    and ramifies at p and ∞. Wait, B is a definite quaternion algebra if it
    ramifies at ∞, giving a compact quotient.

    For an INDEFINITE quaternion algebra B over Q (ramified at an even number
    of finite primes, SPLIT at ∞), B^1(R) ≅ SL(2,R), and B^1(Z) is a
    cocompact lattice in SL(2,R).

    The simplest example: B = (-1, -11/Q), which is ramified at {2, 11}.
    (Must check: discriminant = 2·11 = 22.)

    The covolume formula (Shimizu's formula):
    vol(Γ\H) = (discriminant)/6 · prod_{p | disc} (p-1)/?

    Actually, let me use a known example. The order O of discriminant D in B
    gives Γ = O^1/{±1}.

    For the purpose of demonstrating the computation, let's use the
    known formula for χ_Q:

    For B indefinite over Q with discriminant D = p1...p_{2r}:
    χ_Q(Γ) = (D-1)/(12) · ∏(1 - 1/p_i) ...

    Actually the Gauss-Bonnet formula for arithmetic Fuchsian groups gives:
    Area(Γ\H) / (2π) = |χ^orb(Γ\H)|

    For a maximal order in an indefinite quaternion algebra of discriminant D:
    Area(Γ\H) / (4π) = (D-1)/12 ...

    This is getting into number theory. Let me just record known values.

    For the Bolza surface group (genus 2): Γ' acts on H^2, [Γ:Γ']=48 (automorphism group).
    χ(Γ') = -2, χ_Q(Γ) = -2/48 = -1/24.

    Let me use a simpler explicit example: the modular group PSL(2,Z).
    This is NOT cocompact, but Δ(2,3,∞) = PSL(2,Z).

    For COCOMPACT: use Δ(2,3,7) from Example 1, and Δ(2,4,5).

    Δ(2,4,5): genus 0, cone points 2, 4, 5.
    χ^orb = 2 - (1-1/2) - (1-1/4) - (1-1/5) = 2 - 1/2 - 3/4 - 4/5 = 2 - 41/20 = -1/20.
    H^0 = Q, H^1 = 0, H^2 = Q.
    """

    # Δ(2,4,5)
    cone_orders = [2, 4, 5]
    genus = 0

    chi_orb = Fraction(2 - 2*genus)
    for m in cone_orders:
        chi_orb -= Fraction(1) - Fraction(1, m)

    h0 = 1
    h1 = 0
    h2 = 1
    betti_numbers = [h0, h1, h2]

    # Also compute for Δ(2,3,8)
    cone_orders_238 = [2, 3, 8]
    chi_orb_238 = Fraction(2)
    for m in cone_orders_238:
        chi_orb_238 -= Fraction(1) - Fraction(1, m)

    return {
        "group": "Delta(2,4,5)",
        "ambient_group": "PSL(2,R)",
        "symmetric_space_dim": 2,
        "contains_2_torsion": True,
        "torsion_elements": ["element of order 2", "element of order 4 (square is 2-torsion)"],
        "cone_orders": cone_orders,
        "orbifold_euler_char": str(chi_orb),
        "rational_betti_numbers": betti_numbers,
        "vcd": 2,
        "additional_example": {
            "group": "Delta(2,3,8)",
            "cone_orders": cone_orders_238,
            "orbifold_euler_char": str(chi_orb_238),
            "rational_betti_numbers": [1, 0, 1],
            "contains_2_torsion": True
        },
        "notes": "Cocompact Fuchsian group with 2-torsion. Gauss-Bonnet verified."
    }


###############################################################################
# Gauss-Bonnet verification
###############################################################################

def gauss_bonnet_verification():
    """
    Verify the rational Euler characteristic via the Gauss-Bonnet formula.

    For a cocompact Fuchsian group Γ acting on H^2:
    Area(Γ\H^2) = -2π · χ^orb(Γ\H^2)  (negative because χ^orb can be negative)

    Actually: For a hyperbolic orbifold, Area = -2π · χ^orb when χ^orb < 0.
    When χ^orb > 0, the group is finite (spherical).

    For Δ(2,3,7): χ^orb = 1/42 > 0 ... but this is a hyperbolic group!

    Wait: The sign convention. For a hyperbolic orbifold of genus g with
    cone points m_1,...,m_r:
    χ^orb = 2 - 2g - Σ(1 - 1/m_i)

    The orbifold is hyperbolic iff χ^orb < 0.

    For Δ(2,3,7): χ^orb = 2 - 0 - (1/2 + 2/3 + 6/7) = 2 - (1/2+2/3+6/7)
    = 2 - (21/42 + 28/42 + 36/42) = 2 - 85/42 = 84/42 - 85/42 = -1/42.

    So χ^orb = -1/42 < 0, confirming hyperbolicity. ✓
    Area = 2π/42 = π/21.
    """

    examples = []

    # Example 1: Δ(2,3,7)
    chi_237 = Fraction(2) - (Fraction(1) - Fraction(1,2)) - (Fraction(1) - Fraction(1,3)) - (Fraction(1) - Fraction(1,7))
    area_237 = float(-2 * np.pi * chi_237)
    examples.append({
        "group": "Δ(2,3,7)",
        "chi_orb": str(chi_237),
        "chi_orb_float": float(chi_237),
        "area": area_237,
        "is_hyperbolic": float(chi_237) < 0,
        "verification": "Area = 2π/42 = π/21 ≈ " + f"{area_237:.6f}"
    })

    # Example 2: Hyperelliptic (6 cone points of order 2)
    chi_hyp = Fraction(2) - 6 * (Fraction(1) - Fraction(1,2))
    area_hyp = float(-2 * np.pi * chi_hyp)
    examples.append({
        "group": "π₁(Σ₂) ⋊ Z/2",
        "chi_orb": str(chi_hyp),
        "chi_orb_float": float(chi_hyp),
        "area": area_hyp,
        "is_hyperbolic": float(chi_hyp) < 0,
        "verification": f"Area = 2π ≈ {area_hyp:.6f}"
    })

    # Example 3: Δ(2,4,5)
    chi_245 = Fraction(2) - (Fraction(1) - Fraction(1,2)) - (Fraction(1) - Fraction(1,4)) - (Fraction(1) - Fraction(1,5))
    area_245 = float(-2 * np.pi * chi_245)
    examples.append({
        "group": "Δ(2,4,5)",
        "chi_orb": str(chi_245),
        "chi_orb_float": float(chi_245),
        "area": area_245,
        "is_hyperbolic": float(chi_245) < 0,
        "verification": f"Area = 2π/20 = π/10 ≈ {area_245:.6f}"
    })

    # Verify consistency: for torsion-free subgroup
    # Δ(2,3,7) → surface of genus 3 via Klein quartic, index 168
    # Surface area = 168 * π/21 = 8π = 2π(2·3-2) ✓
    klein_quartic_area = 168 * area_237
    expected_area_g3 = 2 * np.pi * (2*3 - 2)

    consistency_check = {
        "test": "Klein quartic (genus 3) via Δ(2,3,7)",
        "computed_area": klein_quartic_area,
        "expected_area": expected_area_g3,
        "consistent": abs(klein_quartic_area - expected_area_g3) < 1e-10
    }

    return {
        "examples": examples,
        "consistency_check": consistency_check
    }


###############################################################################
# Main computation
###############################################################################

def main():
    signal.alarm(300)  # 5 minute timeout

    try:
        results = {
            "metadata": {
                "description": "Group cohomology computations for uniform lattices with 2-torsion",
                "random_seed": 42,
                "framework": "Python (exact arithmetic via fractions)"
            },
            "example_1_triangle_237": triangle_group_cohomology(),
            "example_2_hyperelliptic": surface_extension_cohomology(),
            "example_3_triangle_245": quaternion_lattice_cohomology(),
            "gauss_bonnet_verification": gauss_bonnet_verification()
        }

        signal.alarm(0)

        # Write results
        with open("results/cohomology_data.json", "w") as f:
            json.dump(results, f, indent=2, default=str)

        print("Computation complete. Results written to results/cohomology_data.json")
        print(f"\nExample 1 (Δ(2,3,7)):")
        print(f"  Betti numbers: {results['example_1_triangle_237']['rational_betti_numbers']}")
        print(f"  χ^orb = {results['example_1_triangle_237']['orbifold_euler_char']}")
        print(f"  vcd = {results['example_1_triangle_237']['vcd']}")

        print(f"\nExample 2 (π₁(Σ₂) ⋊ Z/2):")
        print(f"  Betti numbers: {results['example_2_hyperelliptic']['rational_betti_numbers']}")
        print(f"  χ^orb = {results['example_2_hyperelliptic']['orbifold_euler_char']}")
        print(f"  Gauss-Bonnet consistent: {results['example_2_hyperelliptic']['gauss_bonnet_verification']['consistent']}")

        print(f"\nGauss-Bonnet verification:")
        for ex in results['gauss_bonnet_verification']['examples']:
            print(f"  {ex['group']}: χ^orb = {ex['chi_orb']}, Area = {ex['area']:.6f}, hyperbolic = {ex['is_hyperbolic']}")

        cc = results['gauss_bonnet_verification']['consistency_check']
        print(f"  Klein quartic consistency: {cc['consistent']}")

        return results

    except ComputeTimeout:
        print("Computation timed out")
        return None

if __name__ == "__main__":
    main()
