"""
Analysis of open math problems amenable to dimensional/geometric reasoning.
Demonstrates verifiability via Python computation.
"""
import math
from functools import lru_cache

# =============================================================================
# UTILITY: n-ball volume and surface area via dimensional analysis
# =============================================================================
# The key insight from "dimensional analysis on calculus":
#   - derivative of volume = surface area  (peeling off a dimension)
#   - integral of lower-dim cross-section = higher-dim volume (adding a dimension)
#   - Circle area pi*r^2 -> derivative 2*pi*r (circumference)
#   - Circle area pi*r^2 -> integral (4/3)*pi*r^3 (sphere volume, via revolution)
#
# General formulas:
#   V_n(R) = pi^(n/2) / Gamma(n/2 + 1) * R^n
#   S_{n-1}(R) = dV_n/dR = n * pi^(n/2) / Gamma(n/2 + 1) * R^(n-1)
#            = 2 * pi^(n/2) / Gamma(n/2) * R^(n-1)

def n_ball_volume(n, R=1.0):
    """Volume of an n-dimensional ball of radius R."""
    return (math.pi ** (n / 2.0)) / math.gamma(n / 2.0 + 1) * (R ** n)

def n_sphere_surface_area(n, R=1.0):
    """Surface area of the (n-1)-sphere bounding an n-ball of radius R."""
    return 2 * (math.pi ** (n / 2.0)) / math.gamma(n / 2.0) * (R ** (n - 1))

def verify_derivative_relationship():
    """Verify: surface area = d(volume)/dR via numerical derivative."""
    print("=" * 70)
    print("VERIFICATION: Surface area = d(Volume)/dR (dimensional analysis)")
    print("=" * 70)
    eps = 1e-8
    for n in range(2, 10):
        R = 1.0
        numerical_deriv = (n_ball_volume(n, R + eps) - n_ball_volume(n, R - eps)) / (2 * eps)
        analytical_sa = n_sphere_surface_area(n, R)
        print(f"  dim={n}: dV/dR = {numerical_deriv:.10f}, S = {analytical_sa:.10f}, "
              f"match = {abs(numerical_deriv - analytical_sa) < 1e-5}")
    print()

# =============================================================================
# PROBLEM 1: KISSING NUMBER IN DIMENSION 5
# =============================================================================
def kissing_number_analysis():
    """
    KISSING NUMBER PROBLEM (dimension 5)

    Wikipedia: https://en.wikipedia.org/wiki/Kissing_number

    Open question: What is the exact kissing number in dimension 5?
    Known: 40 <= tau_5 <= 44
    Best known: 40 (from D5 lattice)

    Dimensional analysis connection:
    - The naive "solid angle" bound compares spherical cap area to total sphere area
    - Each tangent sphere subtends a cap of angular radius pi/6 on the central sphere
    - Cap area depends on (n-1)-sphere geometry -> dimensional analysis of sphere volumes
    """
    print("=" * 70)
    print("PROBLEM 1: KISSING NUMBER IN DIMENSION 5")
    print("Wikipedia: https://en.wikipedia.org/wiki/Kissing_number")
    print("=" * 70)

    print("\nOpen question: Is tau_5 = 40, 41, 42, 43, or 44?")
    print("Known bounds: 40 <= tau_5 <= 44")
    print("A verifiable answer: a single integer in {40, 41, 42, 43, 44}")
    print()

    # Naive geometric bound: total solid angle / cap solid angle
    # Cap of angular radius theta on S^{n-1} has fractional area:
    #   f(n, theta) = I_{sin^2(theta)}((n-1)/2, 1/2) / 2
    # where I is the regularized incomplete beta function

    # For kissing number, theta = pi/6 (30 degrees, since tangent spheres of
    # radius 1 touch at distance 2, subtending arcsin(1/2) = pi/6 from center
    # of each cap)
    # Actually theta = pi/3 for the minimum angular separation between centers

    # Simple bound: tau_n <= surface area of S^{n-1} / cap area at pi/3
    # But this overcounts because caps don't tile perfectly.

    for n in range(1, 13):
        # Total surface area of unit (n-1)-sphere
        S = n_sphere_surface_area(n)

        # Spherical cap fractional area at angular radius pi/6
        # (each touching sphere's center is at angular distance >= pi/3 from others,
        #  equivalently each sphere covers a cap of angular radius pi/6)
        # The cap area fraction = I_{sin^2(pi/6)}((n-1)/2, 1/2) / 2
        # For the simple "Rankin-type" bound, we use:
        # tau_n <= 1 / (fraction of S^{n-1} covered by one cap of angular radius pi/3)

        # Fraction of S^{n-1} covered by a cap of half-angle pi/3:
        # This equals the regularized incomplete beta function value
        # For simplicity, use the known formula for cap area

        # Cap area of half-angle alpha on S^{n-1}:
        # A_cap = (S_{n-1}/2) * I_{sin^2(alpha)}((n-1)/2, 1/2)
        # where S_{n-1} = n_sphere_surface_area(n)

        # Simple estimate: cap fraction ~ (sin(alpha))^{n-1} is very rough
        # Better: for the one-side bound from below, use packing:
        pass

    # Known kissing numbers and bounds
    known = {
        1: (2, 2), 2: (6, 6), 3: (12, 12), 4: (24, 24),
        5: (40, 44), 6: (72, 77), 7: (126, 134),
        8: (240, 240), 9: (306, 363), 10: (510, 553),
        11: (593, 868), 12: (840, 1355),
        24: (196560, 196560)
    }

    print("Kissing number bounds by dimension:")
    print(f"  {'Dim':>3}  {'Lower':>8}  {'Upper':>8}  {'Ratio':>6}  {'Volume V_n':>12}  {'Surface S_{n-1}':>14}")
    print(f"  {'-'*3}  {'-'*8}  {'-'*8}  {'-'*6}  {'-'*12}  {'-'*14}")
    for n in sorted(known.keys()):
        lo, hi = known[n]
        Vn = n_ball_volume(n)
        Sn = n_sphere_surface_area(n)
        ratio = hi / lo
        print(f"  {n:3d}  {lo:8d}  {hi:8d}  {ratio:6.3f}  {Vn:12.6f}  {Sn:14.6f}")

    print()
    print("Dimensional analysis insight:")
    print("  The kissing number is bounded by surface area ratios:")
    print("  tau_n <= S_{n-1}(2) / cap_area(n, pi/3)")
    print("  where S_{n-1}(2) is the surface area of a sphere of radius 2")
    print("  (the locus of centers of tangent unit spheres)")
    print("  and cap_area is the spherical cap subtended by one tangent sphere.")
    print()
    print("  The n-ball volume formula V_n = pi^(n/2) / Gamma(n/2 + 1)")
    print("  directly connects to the cap area calculation through:")
    print("  cap_area = integral of (n-2)-sphere cross sections")
    print("  This IS the dimensional analysis: integrating lower-dim slices to get")
    print("  higher-dim volumes, exactly as circle area -> sphere volume.")
    print()
    print("  Verifiable answer: an integer in [40, 44].")
    print("  Check: construct 40 unit vectors in R^5 with pairwise angles >= 60 deg")

    # Verify the D5 lattice gives kissing number 40
    # D5 vectors: all permutations of (+-1, +-1, 0, 0, 0) with even number of minus signs
    # Actually D5 minimal vectors: (+-1, +-1, 0, 0, 0) with all sign combinations
    # That gives C(5,2) * 2^2 = 10 * 4 = 40 vectors

    d5_vectors = []
    for i in range(5):
        for j in range(i + 1, 5):
            for si in [-1, 1]:
                for sj in [-1, 1]:
                    v = [0] * 5
                    v[i] = si
                    v[j] = sj
                    d5_vectors.append(tuple(v))

    print(f"\n  D5 lattice minimal vectors: {len(d5_vectors)} vectors")

    # Verify all pairs have angle >= 60 degrees (dot product <= 1, with ||v|| = sqrt(2))
    # For unit vectors: dot product <= cos(60) = 0.5
    # For D5 vectors with ||v|| = sqrt(2): dot product <= 1
    min_angle = float('inf')
    max_dot = float('-inf')
    for i in range(len(d5_vectors)):
        for j in range(i + 1, len(d5_vectors)):
            dot = sum(a * b for a, b in zip(d5_vectors[i], d5_vectors[j]))
            norm_i = math.sqrt(sum(a * a for a in d5_vectors[i]))
            norm_j = math.sqrt(sum(a * a for a in d5_vectors[j]))
            cos_angle = dot / (norm_i * norm_j)
            cos_angle = max(-1, min(1, cos_angle))  # numerical safety
            angle = math.degrees(math.acos(cos_angle))
            min_angle = min(min_angle, angle)
            max_dot = max(max_dot, cos_angle)

    print(f"  Minimum angle between any two D5 vectors: {min_angle:.2f} degrees")
    print(f"  Maximum cosine of angle: {max_dot:.6f}")
    print(f"  All angles >= 60 degrees: {min_angle >= 59.99}")
    print(f"  -> VERIFIED: 40 non-overlapping unit spheres can touch a central sphere in R^5")
    print()

# =============================================================================
# PROBLEM 2: LEBESGUE'S UNIVERSAL COVERING PROBLEM
# =============================================================================
def lebesgue_covering_analysis():
    """
    LEBESGUE'S UNIVERSAL COVERING PROBLEM

    Wikipedia: https://en.wikipedia.org/wiki/Lebesgue%27s_universal_covering_problem

    Open question: What is the minimum area of a convex set that can cover
    (contain a congruent copy of) every planar set of diameter 1?

    Known bounds: 0.832 <= area <= 0.8440935944

    Dimensional analysis connection:
    - The problem is fundamentally about 2D area (dimension 2)
    - The covering constraint involves 1D diameter (dimension 1)
    - The relationship between diameter (1D measure) and area (2D measure) is
      precisely the kind of dimensional analysis at play
    - Isoperimetric-type inequalities relate 1D boundary to 2D content
    - The optimal shape involves curves whose curvature (1/length) integrates
      to give area - a 1D -> 2D dimensional integration
    """
    print("=" * 70)
    print("PROBLEM 2: LEBESGUE'S UNIVERSAL COVERING PROBLEM")
    print("Wikipedia: https://en.wikipedia.org/wiki/Lebesgue%27s_universal_covering_problem")
    print("=" * 70)

    print("\nOpen question: What is the minimum area of a convex set that contains")
    print("a congruent copy of every planar set of diameter 1?")
    print()
    print("Known bounds:")

    # Best upper bound (Gibbs 2018)
    upper = 0.8440935944
    # Best lower bound (Brass & Sharifi)
    lower = 0.832

    print(f"  Lower bound: {lower} (Brass & Sharifi)")
    print(f"  Upper bound: {upper} (Gibbs, 2018 preprint)")
    print(f"  Gap: {upper - lower:.10f}")
    print(f"  Relative gap: {(upper - lower) / lower * 100:.2f}%")
    print()

    # Key shapes and their areas for comparison
    print("Reference shapes containing all diameter-1 sets:")

    # Circle of diameter 1
    circle_area = math.pi / 4
    print(f"  Circle (diameter 1): area = pi/4 = {circle_area:.10f}")
    print(f"    (NOT a universal cover - can't contain equilateral triangle of diameter 1)")

    # Reuleaux triangle of width 1
    reuleaux_area = (math.pi - math.sqrt(3)) / 2
    print(f"  Reuleaux triangle (width 1): area = (pi - sqrt(3))/2 = {reuleaux_area:.10f}")

    # Regular hexagon with inscribed circle of diameter 1 (Pal's starting point)
    hex_area = math.sqrt(3) / 2
    print(f"  Regular hexagon (inscribed circle diam 1): area = sqrt(3)/2 = {hex_area:.10f}")

    # Pal's reduced cover
    pal_area = hex_area  # Pal started from this and removed corners
    print(f"  Pal's cover (1920, hexagon minus 2 corners): area ~ 0.84529...")

    print()
    print("Dimensional analysis insight:")
    print("  Diameter is a 1D measure. Area is a 2D measure.")
    print("  For a circle: area = pi/4 * diameter^2 (conversion factor = pi/4)")
    print("  For the universal cover: area ~ 0.844 * diameter^2")
    print("  The ratio area/diameter^2 is the key dimensionless constant.")
    print(f"  Current best: {upper} (to be determined exactly)")
    print()
    print("  Verifiable answer: a decimal number in [0.832, 0.8441].")
    print("  Check: given a proposed shape, verify computationally that it contains")
    print("  all constant-width curves of width 1 (necessary and sufficient).")
    print()

# =============================================================================
# PROBLEM 3: SPHERE PACKING DENSITY IN DIMENSION 5
# =============================================================================
def sphere_packing_analysis():
    """
    SPHERE PACKING IN DIMENSION 5

    Wikipedia: https://en.wikipedia.org/wiki/Sphere_packing

    Open question: What is the maximum sphere packing density in R^5?
    Conjectured: D5 lattice is optimal, with density pi^2 / (15*sqrt(2))

    Dimensional analysis connection:
    - Packing density = (volume of one sphere) / (volume of fundamental domain)
    - V_5(R) = 8*pi^2/15 * R^5
    - The density directly involves the n-ball volume formula
    - The recurrence V_n = (2*pi/n) * R^2 * V_{n-2} is pure dimensional analysis:
      multiplying by R^2 (area dimension) and 2*pi/n (angular factor) to step up 2 dims
    - The relationship between packing density and kissing number connects
      Problems 1 and 3 through the same dimensional geometry
    """
    print("=" * 70)
    print("PROBLEM 3: SPHERE PACKING DENSITY IN DIMENSION 5")
    print("Wikipedia: https://en.wikipedia.org/wiki/Sphere_packing")
    print("=" * 70)

    print("\nOpen question: Is the D5 lattice packing the densest sphere packing in R^5?")
    print()

    # D5 lattice packing density
    d5_density = math.pi ** 2 / (15 * math.sqrt(2))
    print(f"D5 lattice packing density: pi^2 / (15*sqrt(2)) = {d5_density:.10f}")
    print()

    # Verify via n-ball volume
    # D5 lattice: fundamental domain volume = 4 (for sphere radius 1/sqrt(2))
    # Actually, D5 has determinant 4, center density = 1/4
    # Packing density = center_density * V_5(1) where we use the covering radius
    # More precisely: density = V_5(r) / det(Lambda)^{1/2} per sphere

    # For D5 with minimal vector length sqrt(2):
    # Packing radius = sqrt(2)/2 = 1/sqrt(2)
    # Determinant of D5 = 4
    # Number of spheres per fundamental domain = 1 (since D5 is a lattice)
    # Wait, D5 has 2 points per fundamental cell of the cubic lattice
    # det(D5) = 4, so fundamental domain volume = 4
    # But we can also pack with radius 1 if minimal distance is 2
    # Let's normalize: minimal distance = sqrt(2), radius = sqrt(2)/2

    r_pack = math.sqrt(2) / 2  # packing radius for D5 with min distance sqrt(2)
    vol_sphere = n_ball_volume(5, r_pack)
    det_D5 = 4  # determinant of D5 lattice
    density_check = vol_sphere / det_D5

    print(f"Verification via n-ball volume:")
    print(f"  Packing radius (min dist sqrt(2)): r = sqrt(2)/2 = {r_pack:.10f}")
    print(f"  V_5(r) = {vol_sphere:.10f}")
    print(f"  det(D5) = {det_D5}")
    print(f"  Density = V_5(r) / det(D5) = {density_check:.10f}")
    print(f"  Expected = pi^2/(15*sqrt(2)) = {d5_density:.10f}")
    print(f"  Match: {abs(density_check - d5_density) < 1e-10}")
    print()

    # Show all solved dimensions for context
    print("Packing densities (solved dimensions):")
    solved = {
        1: (1.0, "trivial"),
        2: (math.pi / math.sqrt(12), "hexagonal"),
        3: (math.pi / math.sqrt(18), "FCC (Kepler)"),
        8: (math.pi ** 4 / 384, "E8 (Viazovska 2016)"),
        24: (math.pi ** 12 / math.factorial(12), "Leech (Viazovska+ 2016)"),
    }

    for n in sorted(solved.keys()):
        density, name = solved[n]
        Vn = n_ball_volume(n)
        print(f"  dim {n:2d}: density = {density:.10f}  ({name}), V_{n} = {Vn:.10f}")

    print()
    print("Unsolved dimensions (best known lattice packings):")
    unsolved = {
        4: (math.pi ** 2 / 16, "D4"),
        5: (math.pi ** 2 / (15 * math.sqrt(2)), "D5"),
        6: (math.pi ** 3 / (48 * math.sqrt(3)), "E6"),
        7: (math.pi ** 3 / 105, "E7"),
    }
    for n in sorted(unsolved.keys()):
        density, name = unsolved[n]
        Vn = n_ball_volume(n)
        print(f"  dim {n:2d}: best known density = {density:.10f}  ({name} lattice), V_{n} = {Vn:.10f}")

    print()
    print("Dimensional analysis insight:")
    print("  The packing density in dim n is: delta_n = V_n(r) * (centers per unit volume)")
    print("  The n-ball volume V_n enters directly, and its recurrence relation")
    print("    V_n = (2*pi/n) * R^2 * V_{n-2}")
    print("  is a pure dimensional transformation: each step up by 2 dimensions")
    print("  multiplies by an 'area worth' of pi*R^2 scaled by 2/n.")
    print()
    print("  This means the packing density ratios between consecutive even/odd")
    print("  dimensions follow a pattern governed by pi and factorials -- the same")
    print("  objects that control the Gamma function in the volume formula.")
    print()
    print("  Furthermore, the KISSING NUMBER tau_n and PACKING DENSITY delta_n")
    print("  are connected: for lattice packings, a higher kissing number generally")
    print("  implies better packing. Both quantities ultimately derive from the")
    print("  same geometric object: the n-ball and its volume/surface relationships.")
    print()
    print("  Verifiable answer: a real number, expected to be pi^2/(15*sqrt(2)).")
    print(f"  If D5 is optimal: density = {d5_density:.15f}")
    print("  Check: compare against known upper bounds from linear programming.")

    # Upper bounds from Cohn-Elkies and three-point bounds
    # Approximate upper bound for dim 5 from Cohn-Kumar-Miller-Radchenko-Viazovska methods
    # The ratio is ~1.032 (from earlier search: best known 0.4653, upper ~0.4803)
    print()

    # Show the dimensional pattern
    print("\n  Volume and density pattern across dimensions:")
    print(f"  {'Dim':>3}  {'V_n(1)':>12}  {'V_n/V_{n-2}':>12}  {'2*pi/n':>10}")
    print(f"  {'-'*3}  {'-'*12}  {'-'*12}  {'-'*10}")
    for n in range(2, 13):
        Vn = n_ball_volume(n)
        Vn_minus_2 = n_ball_volume(n - 2)
        ratio = Vn / Vn_minus_2
        expected_ratio = 2 * math.pi / n
        print(f"  {n:3d}  {Vn:12.8f}  {ratio:12.8f}  {expected_ratio:10.8f}")
    print("  (Note: V_n / V_{n-2} = 2*pi/n for unit radius -- exact dimensional recurrence)")

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    verify_derivative_relationship()
    kissing_number_analysis()
    print("\n")
    lebesgue_covering_analysis()
    print("\n")
    sphere_packing_analysis()

    print("\n")
    print("=" * 70)
    print("SUMMARY: TOP 3 OPEN PROBLEMS FOR DIMENSIONAL ANALYSIS APPROACH")
    print("=" * 70)
    print("""
1. KISSING NUMBER IN DIMENSION 5
   Wikipedia: https://en.wikipedia.org/wiki/Kissing_number
   Open question: Is tau_5 = 40, or could it be 41, 42, 43, or 44?
   Verifiable answer: A single integer in [40, 44]
   Dimensional analysis connection: STRONG
     - Bounding kissing numbers involves ratios of n-sphere surface areas
     - Spherical cap area calculations are n-ball volume integrals
     - The derivative/integral chain V_n -> S_{n-1} -> cap geometry is exactly
       the dimensional analysis framework (lower dim -> higher dim via integration)
   Why tractable: The gap is only 4 integers. Novel geometric insight about
     how 5D spherical caps tile could narrow or close this gap.

2. LEBESGUE'S UNIVERSAL COVERING PROBLEM
   Wikipedia: https://en.wikipedia.org/wiki/Lebesgue%27s_universal_covering_problem
   Open question: Minimum area of convex set covering all diameter-1 planar sets?
   Verifiable answer: A real number in [0.832, 0.8441]
   Dimensional analysis connection: MODERATE
     - Relates 1D measure (diameter) to 2D measure (area) -- a fundamental
       dimensional relationship
     - The optimal cover's boundary curves have curvature properties that
       connect 1D (arc length) to 2D (enclosed area) via integration
     - Isoperimetric reasoning (which IS dimensional analysis) provides bounds
   Why tractable: Steady computational progress; the gap is ~1.4%.
     A new geometric insight about diameter-to-area conversion could help.

3. SPHERE PACKING DENSITY IN DIMENSION 5
   Wikipedia: https://en.wikipedia.org/wiki/Sphere_packing
   Open question: Is D5 the densest packing? What is the exact maximum density?
   Verifiable answer: A real number, conjectured pi^2/(15*sqrt(2)) ~ 0.4653
   Dimensional analysis connection: VERY STRONG
     - The density formula directly uses n-ball volumes V_n(R)
     - The recurrence V_n = (2*pi/n) * R^2 * V_{n-2} is dimensional analysis
     - Surface area = d(Volume)/dR governs the kissing number (connected problem)
     - The proof technique for dims 8, 24 used modular forms that encode
       the dimensional structure of lattice theta functions
   Why tractable: D5 is widely conjectured optimal; the Cohn-Elkies bound
     is close. Progress on the "magic function" approach could close the gap.
     The dimensional recurrence provides structural constraints.
""")
