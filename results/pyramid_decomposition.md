# Dimensional Pyramid Decomposition of Spherical Caps

**Research Rubric Item 013** | Kissing Number Problem, Dimension 5

## 1. Pyramid Volume Correspondence

The fundamental identity of "dimensional analysis on calculus" is this: the operation
integral(x^{n-1} dx) = x^n / n tells us that an n-dimensional ball decomposes into
infinitesimal cones (pyramids) radiating from its center.

**Decomposition.** Consider the n-ball B^n(R). Every point in B^n lies on a unique ray
from the origin through the bounding sphere S^{n-1}(R). Partitioning S^{n-1} into
infinitesimal solid angle elements dOmega, the n-ball decomposes into infinitesimal cones
of the form {t * x : 0 <= t <= R, x in dOmega}. Each such cone has volume:

    dV = (1/n) * R^n * dOmega

This follows directly from integrating in polar coordinates:

    dV = integral_0^R r^{n-1} dr * dOmega = (R^n / n) * dOmega

Integrating over all solid angles recovers the full volume:

    V_n(R) = (1/n) * R^n * S_{n-1}(1) = (1/n) * R * S_{n-1}(R)

This identity, V_n(R) = (1/n) * R * S_{n-1}(R), is equivalent to the derivative relation
d/dR[V_n(R)] = S_{n-1}(R), since:

    d/dR[V_n(R)] = d/dR[(1/n) * R * S_{n-1}(R)]
                 = d/dR[(1/n) * R * (n * V_n(R) / R)]
                 = d/dR[V_n(R)]  ... (self-consistent)

and more directly: V_n(R) = c_n * R^n implies d/dR = n * c_n * R^{n-1} = n * V_n / R = S_{n-1}.

**Numerical verification** (R = 1):

| n  | V_n(1)       | S_{n-1}(1)   | V_n / S_{n-1} | 1/n        | Match |
|----|--------------|--------------|---------------|------------|-------|
| 2  | 3.1415926536 | 6.2831853072 | 0.5000000000  | 0.5000000  | Yes   |
| 3  | 4.1887902048 | 12.5663706144| 0.3333333333  | 0.3333333  | Yes   |
| 4  | 4.9348022005 | 19.7392088022| 0.2500000000  | 0.2500000  | Yes   |
| 5  | 5.2637890139 | 26.3189450696| 0.2000000000  | 0.2000000  | Yes   |
| 6  | 5.1677127800 | 31.0062766803| 0.1666666667  | 0.1666667  | Yes   |
| 7  | 4.7247659703 | 33.0733617923| 0.1428571429  | 0.1428571  | Yes   |
| 8  | 4.0587121264 | 32.4696970113| 0.1250000000  | 0.1250000  | Yes   |
| 9  | 3.2985089027 | 29.6865801246| 0.1111111111  | 0.1111111  | Yes   |
| 10 | 2.5501640399 | 25.5016403988| 0.1000000000  | 0.1000000  | Yes   |

The derivative relationship is also confirmed numerically (central difference, h = 1e-8):

| n | dV/dR (numerical) | S_{n-1}(1) (analytical) | Discrepancy |
|---|-------------------|-------------------------|-------------|
| 3 | 12.5663705663     | 12.5663706144           | 4.8e-08     |
| 4 | 19.7392088452     | 19.7392088022           | 4.3e-08     |
| 5 | 26.3189451122     | 26.3189450696           | 4.3e-08     |

**Geometric interpretation.** Just as integral(x^2 dx) = x^3/3 means a pyramid with
square base of side x has volume (1/3) * x^2 * x = x^3/3 (one-third of the bounding
cube), the identity integral(r^{n-1} dr) = r^n/n means each infinitesimal cone from the
center to the boundary of an n-ball has volume 1/n of its bounding "cylinder" (the product
of the base patch area and the radius).


## 2. Cap Pyramid Decomposition

A spherical cap on S^{n-1} of half-angle theta (centered at some pole) corresponds to a
cone from the center of the ball. This cone has:

- **Solid angle:** Omega_cap = A_cap(n, theta), the area of the cap on the unit sphere
- **Pyramid volume:** V_cone = (1/n) * R^n * Omega_cap

For k non-overlapping caps of half-angle theta on S^{n-1}, we require:

    k * Omega_cap <= S_{n-1}(1)

This is exactly the simple cap-packing bound. The pyramid decomposition recasts it as:

    k * V_cone <= V_n(R)
    k * (1/n) * R^n * Omega_cap <= (1/n) * R^n * S_{n-1}(1)

The 1/n and R^n factors cancel, recovering k * Omega_cap <= S_{n-1}(1).

**Numerical values for the cap at half-angle pi/6 (the kissing number exclusion angle):**

| n | S_{n-1}(1)   | A_cap(n, pi/6) | cap_solid_angle | V_cone = (1/n)*A_cap | Cap bound (floor) |
|---|--------------|----------------|-----------------|----------------------|-------------------|
| 3 | 12.5663706144| 0.8417872145   | 6.6987%         | 0.2805957382         | 14                |
| 4 | 19.7392088022| 0.5691690873   | 2.8834%         | 0.1422922718         | 34                |
| 5 | 26.3189450696| 0.3384803298   | 1.2861%         | 0.0676960660         | 77                |
| 6 | 31.0062766803| 0.1817713670   | 0.5862%         | 0.0302952278         | 170               |
| 7 | 33.0733617923| 0.0896941360   | 0.2712%         | 0.0128134480         | 368               |
| 8 | 32.4696970113| 0.0411715122   | 0.1268%         | 0.0051464390         | 788               |

The cap solid angle fraction decreases exponentially with dimension, while the total
surface area S_{n-1}(1) peaks near n = 7 and then decreases. The cap-packing bound
grows roughly exponentially because the cap area shrinks faster than the total area.


## 3. The 1/n Efficiency Factor

**Definition.** For a spherical cap of half-angle theta on S^{n-1}(R), define the
**pyramid efficiency** as:

    eta_n = V_cone / V_cylinder

where V_cone = (1/n) * R^n * Omega_cap is the cone volume and V_cylinder = Omega_cap * R
is the volume of a "cylinder" with base area Omega_cap and height R.

Since V_cone = (1/n) * R * Omega_cap and V_cylinder = R * Omega_cap (at R = 1):

    eta_n = 1/n

This is independent of theta. The efficiency measures how much of the bounding cylinder
is actually filled by the cone.

**Numerical verification:**

| n | A_cap(n, pi/6) | V_cone = (1/n)*A_cap | V_cyl = A_cap*R | Efficiency = 1/n |
|---|----------------|----------------------|-----------------|------------------|
| 3 | 0.8417872145   | 0.2805957382         | 0.8417872145    | 0.3333333333     |
| 4 | 0.5691690873   | 0.1422922718         | 0.5691690873    | 0.2500000000     |
| 5 | 0.3384803298   | 0.0676960660         | 0.3384803298    | 0.2000000000     |
| 6 | 0.1817713670   | 0.0302952278         | 0.1817713670    | 0.1666666667     |
| 7 | 0.0896941360   | 0.0128134480         | 0.0896941360    | 0.1428571429     |
| 8 | 0.0411715122   | 0.0051464390         | 0.0411715122    | 0.1250000000     |

Higher-dimensional cap-pyramids are "less efficient" at filling space: in R^3 a cone
fills 1/3 of its cylinder, but in R^5 it fills only 1/5, and in R^8 only 1/8.

---

**Lemma 1** (Volume-to-Surface Ratio). *For the unit n-ball, the ratio V_n(1)/S_{n-1}(1)
equals exactly 1/n, and this ratio decreases monotonically with n.*

*Proof.* From V_n(R) = (1/n) * R * S_{n-1}(R), setting R = 1 gives V_n(1) = S_{n-1}(1)/n.
Monotone decrease follows since 1/n > 1/(n+1) for all n >= 1.

*Numerical verification:*

| n  | V_n(1)       | S_{n-1}(1)   | V_n(1)/S_{n-1}(1) | 1/n        |
|----|--------------|--------------|--------------------|-----------:|
| 2  | 3.1415926536 | 6.2831853072 | 0.5000000000       | 0.5000000  |
| 3  | 4.1887902048 | 12.5663706144| 0.3333333333       | 0.3333333  |
| 4  | 4.9348022005 | 19.7392088022| 0.2500000000       | 0.2500000  |
| 5  | 5.2637890139 | 26.3189450696| 0.2000000000       | 0.2000000  |
| 6  | 5.1677127800 | 31.0062766803| 0.1666666667       | 0.1666667  |
| 7  | 4.7247659703 | 33.0733617923| 0.1428571429       | 0.1428571  |
| 8  | 4.0587121264 | 32.4696970113| 0.1250000000       | 0.1250000  |
| 9  | 3.2985089027 | 29.6865801246| 0.1111111111       | 0.1111111  |
| 10 | 2.5501640399 | 25.5016403988| 0.1000000000       | 0.1000000  |

All values match to machine precision. QED.


## 4. Packing Density vs Dimension

**Definition.** The **cap density** for dimension n is:

    rho_n = tau_n * cap_solid_angle(n, pi/6)

This measures the fraction of S^{n-1} covered by non-overlapping exclusion caps
(each of half-angle pi/6) in an optimal kissing configuration.

**Computation for known dimensions:**

| n  | tau_n   | cap_solid_angle(n, pi/6) | rho_n          |
|----|---------|--------------------------|----------------|
| 2  | 6       | 0.1666666667             | 1.0000000000   |
| 3  | 12      | 0.0669872981             | 0.8038475773   |
| 4  | 24      | 0.0288344428             | 0.6920266275   |
| 8  | 240     | 0.0012679980             | 0.3043195296   |
| 24 | 196560  | 1.118e-08                | 0.0021977475   |

**Observation.** The cap density rho_n decreases monotonically across all listed
dimensions, including the "magic" dimensions 8 and 24. Even though tau_8 = 240 and
tau_24 = 196560 are extraordinarily large, the cap solid angles shrink even faster,
so the packing efficiency (as measured by cap coverage) drops dramatically. The sphere
becomes exponentially "empty" in high dimensions.

---

**Lemma 2** (Cap Density Bound). *The cap density satisfies rho_n <= 1 for all n, with
equality if and only if n = 2 (where 6 hexagonally-arranged caps tile the circle exactly).*

*Proof.* By definition, rho_n = tau_n * A_cap(n, pi/6) / S_{n-1}(1). Since tau_n caps
of half-angle pi/6 must be non-overlapping on S^{n-1}, their total area cannot exceed the
total surface area, giving rho_n <= 1. Equality holds for n = 2 because the 6 arcs of
angular length pi/3 = 60 degrees exactly tile the circle of circumference 2*pi (since
6 * pi/3 = 2*pi).*

*For n >= 3, strict inequality rho_n < 1 holds because spherical caps on S^{n-1} (n >= 3)
cannot tile the sphere without gaps (unlike arcs on S^1).*

*Numerical verification:*

| n  | rho_n          | rho_n <= 1 | rho_n < 1 (for n >= 3) |
|----|----------------|------------|------------------------|
| 2  | 1.0000000000   | Yes        | N/A (equality at n=2)  |
| 3  | 0.8038475773   | Yes        | Yes                    |
| 4  | 0.6920266275   | Yes        | Yes                    |
| 8  | 0.3043195296   | Yes        | Yes                    |
| 24 | 0.0021977475   | Yes        | Yes                    |

QED.


## 5. Implications for tau_5

We now apply the pyramid decomposition specifically to the kissing number problem in
dimension 5.

**Key constants for n = 5:**
- V_5(1) = 8*pi^2/15 = 5.2637890139
- S_4(1) = 8*pi^2/3 = 26.3189450696
- A_cap(5, pi/6) = 0.3384803298
- cap_solid_angle(5, pi/6) = 0.0128607104 (about 1.29% of S^4)
- V_5(1) = (1/5) * S_4(1) (confirmed: 26.3189450696 / 5 = 5.2637890139)

**Cap density for tau_5 = 40 vs tau_5 = 44:**

| tau_5 | Total cap area | Fraction of S^4 | rho_5          |
|-------|----------------|-----------------|----------------|
| 40    | 13.5392131927  | 51.44%          | 0.5144284149   |
| 41    | 13.8776935225  | 52.73%          | 0.5272891252   |
| 42    | 14.2161738523  | 54.01%          | 0.5401498356   |
| 43    | 14.5546541821  | 55.30%          | 0.5530105460   |
| 44    | 14.8931345119  | 56.59%          | 0.5658712563   |

Both tau_5 = 40 and tau_5 = 44 use only about 51-57% of the sphere's surface area.
This confirms that the cap-packing bound (which allows up to 100% coverage) is far
from tight.

**Interpolation comparison.** We can compare the density at n = 5 with neighbors:

    rho_3 = 0.8038475773
    rho_4 = 0.6920266275
    rho_5 (tau=40) = 0.5144284149
    rho_5 (tau=44) = 0.5658712563
    rho_8 = 0.3043195296

Exponential interpolation through (n=3, rho_3) and (n=4, rho_4) predicts:

    rho_5 (exponential interp) = rho_4 * (rho_4/rho_3) = 0.5957607719

The value tau_5 = 44 gives rho_5 = 0.5659, which is below the exponential interpolation
of 0.5958, so the interpolation is consistent with (but does not rule out) tau_5 = 44.
The value tau_5 = 40 gives rho_5 = 0.5144, which represents a steeper drop, also below
the interpolation. Neither value is excluded by this analysis.

---

**Lemma 3** (Pyramid Volume Constraint for Kissing in R^5). *Each unit sphere touching
the central sphere in a kissing configuration in R^5 corresponds to a cone from the
center of S^4 with solid angle at least cap_solid_angle(5, pi/6) = 0.0128607104. The
cone has pyramid volume V_cone = (1/5) * A_cap(5, pi/6) = 0.0676960660. For tau_5 = k
kissing spheres, the total cone volume is k * V_cone, which must satisfy:*

    k * 0.0676960660 <= V_5(1) = 5.2637890139

*This yields k <= 77.76, i.e., tau_5 <= 77.*

*The 1/5 factor means that each cone in R^5 occupies only 20% of the volume of its
bounding cylinder, compared to 33.3% in R^3 and 25% in R^4. In this sense, cones
in higher dimensions are geometrically "thinner"--they have more volume concentrated
near the apex (center of the ball) and less near the base (surface). However, because
both the cone volume bound and the surface area bound produce the same inequality after
the 1/n cancellation, this thinning does not directly tighten the kissing number bound.*

*Numerical verification:*

| Quantity                     | n=3          | n=4          | n=5          |
|------------------------------|--------------|--------------|--------------|
| Surface fraction per cap     | 0.0669872981 | 0.0288344428 | 0.0128607104 |
| Volume fraction per cap      | 0.0669872981 | 0.0288344428 | 0.0128607104 |
| Ratio (vol frac / surf frac) | 1.0000000000 | 1.0000000000 | 1.0000000000 |

*The ratio is identically 1 because V_cone/V_n = (1/n)*A_cap / ((1/n)*S_{n-1}) = A_cap/S_{n-1},
which is the same as the surface fraction. The 1/n factor cancels perfectly.*

QED.


## 6. Why the Pyramid Argument Does Not Close the Gap

The pyramid decomposition, despite its geometric elegance, ultimately gives the **same
bound** as the simple cap-packing argument:

    tau_5 <= S_4(1) / A_cap(5, pi/6) = 26.3189450696 / 0.3384803298 = 77.76 => 77

**Why the 1/n factor cancels.** The volume-based argument says:

    k * V_cone <= V_n(R)
    k * (1/n) * R^n * A_cap <= (1/n) * R^n * S_{n-1}

Both sides contain the factor (1/n) * R^n, so:

    k * A_cap <= S_{n-1}

This is identical to the surface area bound. Equivalently:

    tau <= n * V_n / (R * A_cap) = n * (S_{n-1} / n) / A_cap = S_{n-1} / A_cap

The volume decomposition and the surface area argument are mathematically equivalent for
the non-overlap constraint on individual caps.

**The fundamental limitation.** The pyramid decomposition captures only the **individual**
cap constraint: each cap occupies a certain fraction of the sphere, and the fractions must
sum to at most 1. It does not capture **pairwise** constraints between caps--the fact that
if two caps are close to each other, the cones they subtend may interact in ways that
waste additional volume.

Specifically:
1. Two adjacent cones share no volume (cones from the center to non-overlapping caps are
   disjoint), so there is no "overlap volume" to account for.
2. The wasted volume lies in the **gaps between caps** on S^{n-1}, not in the cones
   themselves. The pyramid decomposition accounts for cone volume but not for gap geometry.
3. The Delsarte LP bound (tau_5 <= 44) exploits polynomial positivity conditions that
   encode pairwise angular constraints globally. This is fundamentally stronger than
   any single-cap or single-cone argument.

**To improve the bound** using geometric decomposition, one would need to:
- Account for the **angular distribution** of caps, not just their total area
- Incorporate constraints from the **contact graph** (pairwise angular separations)
- Use techniques like Delsarte LP or SDP that enforce positivity of the angular
  distribution function globally, not just cap-by-cap

The pyramid decomposition provides useful geometric intuition (the 1/n thinning of cones,
the monotone decrease of cap density) but does not, by itself, improve upon the trivial
cap-packing bound of tau_5 <= 77. The gap between 77 and the LP bound of 44 must be
closed by methods that account for the global structure of the point configuration on S^4.


## Summary of Verified Lemmas

| Lemma | Statement | Verification |
|-------|-----------|--------------|
| Lemma 1 | V_n(1)/S_{n-1}(1) = 1/n, decreasing with n | Confirmed for n=2..10 to machine precision |
| Lemma 2 | Cap density rho_n <= 1, with equality iff n=2 | Confirmed for n=2,3,4,8,24 |
| Lemma 3 | Pyramid volume bound for tau_5 gives tau_5 <= 77, same as cap bound; the 1/n factor cancels | Confirmed: volume fraction equals surface fraction for n=3,4,5 |


## Computational Details

All numerical values were computed using:
- `src/ndim_geometry.py`: V_n, S_n, cap_area, cap_solid_angle functions
- `scipy.special.betainc` for regularized incomplete beta function
- `math.gamma` for Gamma function evaluations
- Numerical differentiation with central difference (h = 1e-8) for derivative verification
- All values agree to at least 8 significant digits with analytical formulas
