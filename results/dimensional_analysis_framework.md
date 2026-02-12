# Dimensional Analysis on Calculus: A Standalone Framework

**Research Rubric Item 023** | General Mathematical Framework

---

## 1. Formal Statement of the Derivative/Integral Dimensional Correspondence

The central identity of dimensional analysis on calculus is the observation that differentiation and integration with respect to a radial parameter correspond to moving between adjacent dimensions in the family of $n$-balls and $(n{-}1)$-spheres. This section formalizes this correspondence and states its most important consequences.

**The fundamental power rule in geometric form.** The elementary calculus identity

$$\frac{d}{dx}\left[\frac{x^n}{n!}\right] = \frac{x^{n-1}}{(n-1)!}$$

has a geometric counterpart. Replacing the factorial $n!$ with the Gamma function $\Gamma(n/2 + 1)$ (which generalizes the factorial to half-integers and real arguments), and interpreting $x$ as a radius $R$, the identity becomes a statement about the volumes and surface areas of $n$-dimensional balls and their bounding spheres.

**Theorem 1 (Derivative-Volume-Surface Correspondence).** The volume of the $n$-ball of radius $R$ is

$$V_n(R) = \frac{\pi^{n/2}}{\Gamma(n/2 + 1)} \, R^n$$

and its derivative with respect to $R$ yields the surface area of the bounding $(n{-}1)$-sphere:

$$\frac{d}{dR}\bigl[V_n(R)\bigr] = S_{n-1}(R) = \frac{2\pi^{n/2}}{\Gamma(n/2)} \, R^{n-1}.$$

**Proof.** Direct differentiation gives

$$\frac{d}{dR}\bigl[V_n(R)\bigr] = \frac{\pi^{n/2}}{\Gamma(n/2+1)} \cdot n \cdot R^{n-1} = \frac{n\,\pi^{n/2}}{\Gamma(n/2+1)} \, R^{n-1}.$$

Applying the Gamma function recurrence $\Gamma(n/2+1) = (n/2)\,\Gamma(n/2)$, this simplifies to

$$\frac{n\,\pi^{n/2}}{(n/2)\,\Gamma(n/2)} \, R^{n-1} = \frac{2\pi^{n/2}}{\Gamma(n/2)} \, R^{n-1} = S_{n-1}(R). \qquad \square$$

**Geometric interpretation.** The derivative "peels off" one radial dimension. Just as $d/dx[x^2] = 2x$ expresses the fact that the perimeter of a square of side $x$ consists of two sides of length $x$ (the boundary of a 2D region is a 1D curve), the derivative of the $n$-ball volume with respect to $R$ gives its bounding surface area. The boundary of an $n$-ball is an $(n{-}1)$-sphere, and this topological fact is encoded as a calculus identity.

**Numerical verification** (at $R = 1$, central difference with $h = 10^{-8}$):

| $n$ | $dV/dR$ (numerical) | $S_{n-1}(1)$ (analytical) | Discrepancy |
|-----|----------------------|---------------------------|-------------|
| 3   | 12.5663705663        | 12.5663706144              | $4.8 \times 10^{-8}$ |
| 4   | 19.7392088452        | 19.7392088022              | $4.3 \times 10^{-8}$ |
| 5   | 26.3189451122        | 26.3189450696              | $4.3 \times 10^{-8}$ |

The equivalence $V_n(R) = (1/n) \cdot R \cdot S_{n-1}(R)$ provides a dual formulation: the volume of an $n$-ball equals $1/n$ times the product of its radius and surface area. This "cone formula" decomposes the ball into infinitesimal pyramids from its center to its boundary, each contributing $dV = (1/n)\,R\,dA$ where $dA$ is a surface element on $S^{n-1}(R)$.

---

## 2. The $n$-Ball Recurrence as the Fundamental Identity

**Theorem 2 (Two-Step Recurrence).** The unit $n$-ball volumes satisfy the recurrence

$$V_n(R) = \frac{2\pi}{n} \, R^2 \cdot V_{n-2}(R)$$

with base cases $V_0 = 1$ (a point) and $V_1(R) = 2R$ (an interval of length $2R$).

**Proof via Gamma function identities.** Starting from the ratio

$$\frac{V_n(R)}{V_{n-2}(R)} = \frac{\pi^{n/2} / \Gamma(n/2+1)}{\pi^{(n-2)/2} / \Gamma((n-2)/2+1)} \cdot R^2 = \frac{\pi \cdot \Gamma(n/2 - 1 + 1)}{\Gamma(n/2+1)} \cdot R^2 = \frac{\pi \cdot \Gamma(n/2)}{\Gamma(n/2+1)} \cdot R^2$$

and applying $\Gamma(n/2+1) = (n/2)\,\Gamma(n/2)$, we obtain

$$\frac{V_n(R)}{V_{n-2}(R)} = \frac{\pi}{n/2} \cdot R^2 = \frac{2\pi}{n} \, R^2. \qquad \square$$

**Proof via integration (cross-sectional slicing).** The $n$-ball of radius $R$ can be sliced perpendicular to any axis. At distance $x$ from the center along that axis ($-R \le x \le R$), the cross-section is an $(n{-}1)$-ball of radius $\sqrt{R^2 - x^2}$. Therefore

$$V_n(R) = \int_{-R}^{R} V_{n-1}\!\left(\sqrt{R^2 - x^2}\right) dx.$$

This integral can be evaluated by substituting $x = R\sin\phi$, yielding a product of the $(n{-}1)$-ball volume coefficient and a beta function integral. Iterating this slicing twice (once in each of two orthogonal directions) and switching to polar coordinates $(r, \theta)$ in the two sliced dimensions produces the factor $2\pi \cdot R^2$ from the angular integration and $V_{n-2}$ from the remaining $(n{-}2)$-dimensional cross-section, with the factor $1/n$ arising from $\int_0^R r^{n-1}\,dr = R^n/n$.

**Numerical verification** (at $R = 1$, slicing integral via `scipy.integrate.quad`):

| $n$ | $V_n$ (slice integral) | $V_n$ (exact) | Discrepancy |
|-----|------------------------|---------------|-------------|
| 3   | 4.1887902048           | 4.1887902048  | $< 10^{-15}$ |
| 4   | 4.9348022005           | 4.9348022005  | $6.6 \times 10^{-11}$ |
| 5   | 5.2637890139           | 5.2637890139  | $< 10^{-15}$ |
| 6   | 5.1677127800           | 5.1677127800  | $6.1 \times 10^{-11}$ |

**Connection to the power rule.** The recurrence $V_n = (2\pi/n)\,R^2\,V_{n-2}$ is fundamentally linked to the integral $\int r^{n-1}\,dr = r^n/n$. In polar coordinates, the Jacobian for the $n$-ball contains the factor $r^{n-1}$, and integrating this radial factor produces $1/n$. The factor $2\pi$ arises from the angular integration over one pair of coordinates. Together, the recurrence encodes the interplay between angular and radial integration in the volume computation.

**Verification of recurrence ratios** (at $R = 1$):

| $n$ | $V_n / V_{n-2}$ | $2\pi/n$     | Match |
|-----|------------------|--------------|-------|
| 2   | 3.1415926536     | 3.1415926536 | Yes   |
| 3   | 2.0943951024     | 2.0943951024 | Yes   |
| 4   | 1.5707963268     | 1.5707963268 | Yes   |
| 5   | 1.2566370614     | 1.2566370614 | Yes   |
| 8   | 0.7853981634     | 0.7853981634 | Yes   |

Since $2\pi/n < 1$ for $n > 2\pi \approx 6.28$, the recurrence tells us that $V_n(1) < V_{n-2}(1)$ for $n \ge 7$. This foreshadows the volume decrease discussed in the next section.

---

## 3. Worked Examples Beyond Kissing Numbers

### Example 1: Why $n$-Ball Volume Peaks Near $n = 5$ and Then Decreases

The unit $n$-ball volume $V_n(1) = \pi^{n/2} / \Gamma(n/2+1)$ initially increases with $n$ but eventually decreases toward zero. The peak occurs at a non-integer value of $n$, which we can find by treating $n$ as a continuous parameter and solving $dV/dn = 0$.

**Derivation.** Taking the logarithm,

$$\ln V_n(1) = \frac{n}{2} \ln \pi - \ln \Gamma\!\left(\frac{n}{2}+1\right).$$

Differentiating with respect to $n$:

$$\frac{d}{dn}\bigl[\ln V_n(1)\bigr] = \frac{1}{2}\ln\pi - \frac{1}{2}\,\psi\!\left(\frac{n}{2}+1\right)$$

where $\psi(x) = \Gamma'(x)/\Gamma(x)$ is the digamma function. Setting this to zero yields the condition

$$\psi\!\left(\frac{n^*}{2}+1\right) = \ln\pi.$$

Since $\ln\pi \approx 1.14473$ and the digamma function is monotonically increasing, a unique solution exists. Numerical root-finding gives

$$n^* \approx 5.25695, \qquad V_{n^*}(1) \approx 5.27777.$$

The second derivative is $-(1/4)\,\psi'\!\bigl(n^*/2 + 1\bigr) \approx -0.07925 < 0$, confirming a maximum.

**Integer volume table:**

| $n$ | $V_n(1)$     |
|-----|--------------|
| 1   | 2.0000000000 |
| 2   | 3.1415926536 |
| 3   | 4.1887902048 |
| 4   | 4.9348022005 |
| **5**   | **5.2637890139** |
| 6   | 5.1677127800 |
| 7   | 4.7247659703 |
| 8   | 4.0587121264 |
| 10  | 2.5501640399 |
| 15  | 0.3814432808 |
| 20  | 0.0258068914 |

**Geometric interpretation.** The decrease for large $n$ has a clean explanation through the identity $V_n = S_{n-1}/n$. The surface area $S_{n-1}(1)$ itself peaks near $n \approx 7.26$ (at $S \approx 33.16$), but the $1/n$ factor pulls the volume peak to a lower dimension. In high dimensions, the ball's volume is "concentrated near its surface" in the following sense: a thin shell of thickness $\epsilon$ near $r = 1$ contains a fraction $1 - (1-\epsilon)^n$ of the total volume, which approaches 1 as $n \to \infty$. For instance, at $n = 100$ and $\epsilon = 0.05$, the shell $0.95 \le r \le 1$ contains more than $99.4\%$ of the ball's volume.

**Asymptotic behavior.** For large $n$, Stirling's approximation gives

$$V_n(1) \sim \frac{1}{\sqrt{n\pi}} \left(\frac{2\pi e}{n}\right)^{n/2}$$

which decays super-exponentially because $(2\pi e / n)^{n/2} \to 0$ once $n > 2\pi e \approx 17.08$. Numerical verification:

| $n$  | $V_n(1)$ exact     | $V_n(1)$ Stirling  | Ratio  |
|------|--------------------|--------------------|--------|
| 10   | $2.5502 \times 10^{0}$  | $2.5930 \times 10^{0}$  | 0.9835 |
| 20   | $2.5807 \times 10^{-2}$ | $2.6023 \times 10^{-2}$ | 0.9917 |
| 50   | $1.7302 \times 10^{-13}$| $1.7360 \times 10^{-13}$| 0.9967 |
| 100  | $2.3682 \times 10^{-40}$| $2.3722 \times 10^{-40}$| 0.9983 |

### Example 2: The Isoperimetric Inequality and Dimensional Scaling

The classical isoperimetric inequality states that among all bodies of fixed surface area in $\mathbb{R}^n$, the ball maximizes the enclosed volume. The dimensional analysis framework provides a precise quantitative characterization of this optimality through the ratio $V_n / S_{n-1}$.

**The dimensional ratio.** From the identity $V_n(R) = (1/n) \cdot R \cdot S_{n-1}(R)$, we obtain

$$\frac{V_n(R)}{S_{n-1}(R)} = \frac{R}{n}.$$

This ratio has a direct geometric meaning: it is the average "depth" of the ball as measured from its surface. Each infinitesimal pyramid from the center to a surface element $dA$ has height $R$ and volume $(1/n)\,R\,dA$, so the average volume per unit surface area is $R/n$.

**Sharpness characterization.** For a general convex body $K$ in $\mathbb{R}^n$ with volume $|K|$ and surface area $|\partial K|$, the isoperimetric inequality states

$$\frac{|K|}{|\partial K|} \le \frac{R_{\text{iso}}}{n}$$

where $R_{\text{iso}}$ is the radius of the ball with surface area $|\partial K|$. Equality holds if and only if $K$ is a ball. The factor $1/n$ means that in high dimensions, the isoperimetric ratio becomes small even for the optimal shape.

**Numerical illustration:**

| $n$  | $V_n(1) / S_{n-1}(1) = R/n$ |
|------|------------------------------|
| 2    | 0.500000                     |
| 3    | 0.333333                     |
| 5    | 0.200000                     |
| 10   | 0.100000                     |
| 20   | 0.050000                     |
| 50   | 0.020000                     |
| 100  | 0.010000                     |

The ball becomes "less efficient" at enclosing volume relative to its surface area as dimension grows. In $\mathbb{R}^{100}$, the unit ball encloses only $1/100 = 1\%$ of the volume of the "cylinder" with the same base area and height, compared to $33.3\%$ in $\mathbb{R}^3$. This is a reflection of the concentration-of-measure phenomenon: high-dimensional geometry is dominated by the surface layer.

**Connection to the recurrence.** The two-step recurrence $V_n = (2\pi/n)\,R^2\,V_{n-2}$ provides a second perspective. Since $2\pi/n < 1$ for $n > 6$, each step of two dimensions reduces the volume. The isoperimetric ratio $R/n$ and the recurrence ratio $2\pi/n$ are both manifestations of the same underlying phenomenon: the $1/n$ factor arising from $\int_0^R r^{n-1}\,dr = R^n/n$ makes higher-dimensional balls progressively "thinner" relative to their bounding surfaces.

### Example 3: The Pyramid Volume Formula in $n$ Dimensions

The classical formula for the volume of a pyramid in $\mathbb{R}^3$ with base area $B$ and height $h$ is $V = (1/3)\,B\,h$. The dimensional analysis framework reveals this as a special case of a general $n$-dimensional identity.

**Theorem 3 (Generalized Pyramid Volume).** In $\mathbb{R}^n$, a cone (pyramid) with $(n{-}1)$-dimensional base of content $B$ and apex at perpendicular distance $h$ from the base has $n$-dimensional volume

$$V_{\text{pyramid}} = \frac{1}{n}\,B\,h.$$

**Proof.** At distance $t$ from the apex ($0 \le t \le h$), the cross-section of the cone is a scaled copy of the base with linear scale factor $t/h$, so the $(n{-}1)$-dimensional cross-sectional content is $B \cdot (t/h)^{n-1}$. Integrating:

$$V_{\text{pyramid}} = \int_0^h B\left(\frac{t}{h}\right)^{n-1} dt = \frac{B}{h^{n-1}} \cdot \frac{h^n}{n} = \frac{B\,h}{n}. \qquad \square$$

This is precisely the identity $\int_0^h t^{n-1}\,dt = h^n/n$ applied to the scaling of cross-sections.

**Classical cases:**
- $n = 2$: A triangle with base $b$ and height $h$ has area $(1/2)\,b\,h$.
- $n = 3$: A pyramid with base area $B$ and height $h$ has volume $(1/3)\,B\,h$.
- $n = 4$: A 4D cone has 4-volume $(1/4)\,B\,h$.
- $n = 5$: A 5D cone has 5-volume $(1/5)\,B\,h$.

**Numerical verification** (with $B = 3.0$, $h = 2.0$):

| $n$ | $V_{\text{pyramid}} = B\,h/n$ |
|-----|-------------------------------|
| 2   | 3.000000                      |
| 3   | 2.000000                      |
| 4   | 1.500000                      |
| 5   | 1.200000                      |
| 6   | 1.000000                      |

**Application to spherical caps.** A particularly important application is the cone from the center of an $n$-ball to a spherical cap on its boundary. If the cap has area $A_{\text{cap}}$ on the unit $(n{-}1)$-sphere, then the cone subtended from the center has volume

$$V_{\text{cone}} = \frac{1}{n} \cdot R \cdot A_{\text{cap}}.$$

For the full sphere, summing over all infinitesimal caps recovers $V_n(R) = (1/n)\,R\,S_{n-1}(R)$. This decomposition is the bridge between the pyramid formula and the derivative identity: the ball is a union of infinitesimal pyramids, and the $n$-dependent factor $1/n$ governs how much volume each pyramid contributes.

**Numerical verification** (cap area and cone volume for half-angle $\theta = \pi/6$):

| $n$ | $A_{\text{cap}}(n, \pi/6)$ | $V_{\text{cone}} = (1/n) A_{\text{cap}}$ | $V_{\text{cone}} / V_n$ | $A_{\text{cap}} / S_{n-1}$ |
|-----|----------------------------|------------------------------------------|--------------------------|----------------------------|
| 3   | 0.8417872145               | 0.2805957382                             | 0.0669872981             | 0.0669872981               |
| 4   | 0.5691690873               | 0.1422922718                             | 0.0288344428             | 0.0288344428               |
| 5   | 0.3384803298               | 0.0676960660                             | 0.0128607104             | 0.0128607104               |
| 6   | 0.1817713670               | 0.0302952278                             | 0.0058624055             | 0.0058624055               |
| 7   | 0.0896941360               | 0.0128134480                             | 0.0027119752             | 0.0027119752               |
| 8   | 0.0411715122               | 0.0051464390                             | 0.0012679980             | 0.0012679980               |

The last two columns are identical, confirming that the volume fraction of the cone equals the surface area fraction of the cap. This is because the $1/n$ factor appears in both numerator ($V_{\text{cone}} = (1/n)\,A_{\text{cap}}$) and denominator ($V_n = (1/n)\,S_{n-1}$), and cancels in the ratio. The pyramid decomposition thus provides a volume-based perspective on cap geometry that is exactly equivalent to the surface-area perspective, but offers geometric intuition about how the interior of the ball is partitioned.

---

## 4. Limitations and When the Framework Does vs. Does Not Help

The dimensional analysis on calculus framework is a powerful organizational tool for understanding the geometry of $n$-balls and $n$-spheres, but it has clear boundaries. This section provides an honest assessment of its scope.

**The framework DOES help in the following situations:**

1. **Providing geometric intuition about dimensional scaling.** The identity $V_n = S_{n-1} \cdot R/n$ immediately explains why high-dimensional balls have vanishing volume relative to their surface area. The recurrence $V_n = (2\pi/n)\,R^2\,V_{n-2}$ makes the exponential decay of volume with dimension transparent: once $2\pi/n < 1$ (i.e., $n > 6$), each two-step increment shrinks the volume. These are not merely algebraic facts but carry geometric meaning about the distribution of mass within the ball.

2. **Unifying volume, surface area, and cap area calculations.** The framework shows that the spherical cap area formula $A_{\text{cap}}(n,\theta) = (S_{n-1}/2)\,I_{\sin^2\theta}((n{-}1)/2, 1/2)$ arises by integrating $(n{-}2)$-sphere cross-sections across the cap, exactly paralleling how $V_n$ arises by integrating $(n{-}1)$-ball cross-sections across the diameter. This unification makes it straightforward to derive identities relating different geometric quantities.

3. **Deriving recurrence relations and closed forms.** The two-step recurrence $V_n = (2\pi/n)\,V_{n-2}$ and the derivative identity $dV_n/dR = S_{n-1}$ are efficient computational tools. The recurrence avoids evaluating the Gamma function directly and provides a numerically stable way to compute volumes for moderate $n$. The derivative identity provides an alternative to direct differentiation when analyzing how volumes change with radius.

4. **Understanding the pyramid (cone) decomposition.** The $1/n$ factor in the cone volume formula $V_{\text{cone}} = (1/n)\,B\,h$ gives a concrete geometric picture: an $n$-dimensional cone fills only $1/n$ of the bounding cylinder, with the "wasted" volume concentrated near the apex. This is directly observable in the volume-to-surface ratio $V_n/S_{n-1} = R/n$.

**The framework DOES NOT help in the following situations:**

1. **Constraining pairwise angular distributions on spheres.** The dimensional analysis framework captures "single-body" geometry--properties of individual balls, spheres, and caps--but not "multi-body" interactions. In problems like spherical code design or kissing number computation, the key constraint is pairwise: the angular separation between any two points must exceed a threshold. The volume and surface area identities say nothing about such pairwise constraints.

2. **Improving linear programming (LP) or semidefinite programming (SDP) bounds.** The Delsarte LP bound and its SDP extensions use spectral methods based on Gegenbauer polynomials and positive-definite functions on the sphere. These bounds exploit the full polynomial structure of spherical harmonics. The dimensional analysis constraints--being essentially algebraic identities relating volumes and surface areas--are already implicitly satisfied by any feasible LP/SDP solution and thus do not provide additional cutting planes. In concrete experiments (see `results/enhanced_bound_results.txt`), adding dimensional constraints to the Delsarte LP for dimension 5 produced no improvement over the baseline LP bound.

3. **Solving packing and covering problems.** The cap-packing upper bound $\tau_n \le S_{n-1}/A_{\text{cap}}$ is the strongest bound obtainable from single-cap area arguments, and it is exponentially weaker than LP/SDP bounds in high dimensions. For example, in dimension 5, the cap bound gives $\tau_5 \le 77$ while the Delsarte LP gives $\tau_5 \le 44$. The gap factor grows with $n$ because the cap bound treats caps independently, ignoring all correlations.

**The fundamental gap** is between "single-body" and "multi-body" geometry. Dimensional analysis captures how one ball, one sphere, or one cap behaves under scaling, slicing, and differentiation. But problems involving configurations of many objects on a sphere require information about the joint distribution of points, which lies outside the framework's scope. Spectral methods (LP/SDP bounds via Gegenbauer expansions) and algebraic methods (lattice theory, representation theory) address this multi-body regime, and the dimensional framework cannot substitute for them.

---

## 5. Connection to Broader Mathematics

The dimensional analysis on calculus framework, while elementary in its core identities, connects to several deep areas of mathematics.

**Gamma function and Euler's integral.** The volume formula $V_n(R) = \pi^{n/2}/\Gamma(n/2+1) \cdot R^n$ relies on the Gamma function $\Gamma(s) = \int_0^\infty t^{s-1} e^{-t}\,dt$. The appearance of $\Gamma$ is not accidental: the Gaussian integral $\int_{\mathbb{R}^n} e^{-\|x\|^2}\,dx = \pi^{n/2}$ factored in polar coordinates yields $S_{n-1}(1) \cdot \int_0^\infty r^{n-1} e^{-r^2}\,dr = \pi^{n/2}$, and evaluating the radial integral via the substitution $u = r^2$ gives $\Gamma(n/2)/2$. This is the standard derivation of the surface area formula and illustrates how the volume recurrence is ultimately rooted in properties of the Gaussian measure.

**Beta function and the regularized incomplete beta function.** The spherical cap area formula involves the regularized incomplete beta function $I_x(a,b) = B(x; a,b) / B(a,b)$, where $B(x; a,b) = \int_0^x t^{a-1}(1-t)^{b-1}\,dt$ and $B(a,b) = \Gamma(a)\Gamma(b)/\Gamma(a+b)$. In the cap area formula, $a = (n{-}1)/2$ and $b = 1/2$, with $x = \sin^2\theta$. The beta function arises from the substitution $t = \sin^2\phi$ in the integral $\int_0^\theta (\sin\phi)^{n-2}\,d\phi$ that defines the cap area. This integral is a special case of the Euler beta integral and connects the geometry of spherical caps to the theory of hypergeometric functions.

**Gegenbauer polynomials and harmonic analysis on spheres.** The Gegenbauer (ultraspherical) polynomials $C_k^{\lambda}(t)$ with $\lambda = (n{-}2)/2$ form a complete orthogonal system for functions on $S^{n-1}$ that depend only on the angle from a fixed pole. They are the zonal spherical harmonics for the sphere and satisfy the addition theorem: the reproducing kernel for degree-$k$ spherical harmonics on $S^{n-1}$ can be expressed in terms of $C_k^{(n-2)/2}(\cos\theta)$. The dimensional analysis framework intersects with Gegenbauer theory through the cap area formula, since $I_{\sin^2\theta}((n{-}1)/2, 1/2)$ can be expanded in Gegenbauer polynomials. For reference, representative values at $t = 0.5$ include $C_0^{1.5}(0.5) = 1$, $C_1^{1.5}(0.5) = 1.5$, $C_2^{1.5}(0.5) = 0.375$, $C_3^{1.5}(0.5) = -1.5625$, and $C_4^{1.5}(0.5) = -2.2266$ for dimension $n = 5$.

**The volume recurrence and the representation theory of $\mathrm{SO}(n)$.** The two-step recurrence $V_n = (2\pi/n)\,V_{n-2}$ reflects the structure of the rotation group $\mathrm{SO}(n)$. The sphere $S^{n-1}$ is the homogeneous space $\mathrm{SO}(n)/\mathrm{SO}(n{-}1)$, and the decomposition of $L^2(S^{n-1})$ into irreducible representations of $\mathrm{SO}(n)$ yields the spherical harmonic expansion. The volume recurrence, which relates $n$-dimensional and $(n{-}2)$-dimensional quantities, mirrors the branching rule for representations of $\mathrm{SO}(n)$ restricted to $\mathrm{SO}(n{-}2)$. While the volume identity itself is a purely analytic statement, its structural form--linking even and odd dimensions separately via a multiplicative factor--is a shadow of the deeper algebraic structure governing harmonic analysis on spheres.

---

## Computational Appendix

All numerical values in this document were computed using the Python module `src/ndim_geometry.py`, which implements:

- `V_n(n, R)`: volume via the Gamma function formula $\pi^{n/2}/\Gamma(n/2+1) \cdot R^n$
- `V_n_recurrence(n, R)`: volume via the two-step recurrence $V_n = (2\pi/n)R^2 V_{n-2}$
- `S_n(n, R)`: surface area via $2\pi^{n/2}/\Gamma(n/2) \cdot R^{n-1}$
- `cap_area(n, theta)`: cap area via $S_{n-1}/2 \cdot I_{\sin^2\theta}((n{-}1)/2, 1/2)$
- `cap_solid_angle(n, theta)`: fractional cap area $A_{\text{cap}} / S_{n-1}$

Dependencies: `scipy.special.betainc` for the regularized incomplete beta function, `scipy.special.digamma` and `scipy.special.polygamma` for digamma/trigamma evaluations, `scipy.optimize.brentq` for root-finding, `scipy.integrate.quad` for numerical integration verification, and `math.gamma` for Gamma function evaluations. All results are reproducible and agree to at least 10 significant digits with analytical formulas.
