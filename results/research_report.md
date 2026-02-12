# The Kissing Number in Dimension Five: A Dimensional Analysis Approach

## Abstract

The kissing number $\tau_5$ in dimension five --- the maximum number of non-overlapping unit spheres in $\mathbb{R}^5$ that can simultaneously touch a central unit sphere --- remains one of the most prominent open problems in discrete geometry. The current best bounds are $40 \leq \tau_5 \leq 44$, with the lower bound achieved by the $D_5$ lattice and the upper bound established through high-accuracy semidefinite programming. In this work, we investigate whether the dimensional analysis framework rooted in the calculus of $n$-ball volumes --- specifically the derivative relationship $\frac{d}{dR}[V_n(R)] = S_{n-1}(R)$, the two-step recurrence $V_n = \frac{2\pi}{n} R^2 V_{n-2}$, and the pyramid decomposition $\int r^{n-1}\,dr = \frac{r^n}{n}$ --- can yield improved bounds on $\tau_5$. We implement the Delsarte linear programming bound augmented with three dimensional integration constraints (equatorial slicing, Gram matrix trace, and volume recurrence consistency), perform contact graph analysis with a refined vertex degree bound of 21 (improved from the naive bound of 24), and carry out extensive construction attempts for a 41st kissing vector. Our main finding is negative: the dimensional analysis framework does not improve the upper bound beyond the known $\tau_5 \leq 44$, and no 41-point kissing configuration was found. Nevertheless, the investigation produces novel geometric insights, including a clean proof of local rigidity for the $D_5$ configuration with an angular gap of $9.23^\circ$, the refined degree bound $d(v) \leq 21$ for contact graphs in $\mathbb{R}^5$, and a systematic cap density analysis showing $\rho_5 \in [0.514, 0.566]$ for $\tau_5 \in [40, 44]$.

---

## 1. Introduction

The kissing number problem asks: in $n$-dimensional Euclidean space, what is the maximum number of non-overlapping unit spheres that can simultaneously be tangent to a given central unit sphere? This maximum, denoted $\tau_n$, is equivalently the maximum number of points on the unit sphere $S^{n-1}$ such that any two points have angular separation at least $60^\circ$ (i.e., inner product at most $1/2$). The problem has a long and distinguished history, tracing back to the famous Newton--Gregory debate of 1694 concerning $\tau_3$, which was finally settled by Schutte and van der Waerden \cite{schutte1953problem} in 1953, who proved $\tau_3 = 12$. The exact kissing number is known in only a few dimensions: $\tau_1 = 2$, $\tau_2 = 6$, $\tau_3 = 12$ \cite{schutte1953problem}, $\tau_4 = 24$ \cite{musin2008kissing}, $\tau_8 = 240$, and $\tau_{24} = 196{,}560$ \cite{odlyzko1979kissing}. The cases $n = 8$ and $n = 24$ were resolved by Odlyzko and Sloane using the Delsarte linear programming method, which is tight in these "magic" dimensions due to the existence of exceptionally symmetric lattice structures ($E_8$ and the Leech lattice).

The case $n = 5$ is the first open dimension and has resisted all attempts at resolution for over four decades. The best known bounds are $40 \leq \tau_5 \leq 44$, where the lower bound is achieved by the $D_5$ root system \cite{conway1999sphere} and the upper bound is due to the high-accuracy semidefinite programming computation of Mittelmann and Vallentin \cite{mittelmann2010high}.

The motivation for this investigation is to explore whether the dimensional analysis framework --- the family of identities linking $n$-ball volumes, surface areas, and their derivatives --- can provide geometric constraints strong enough to tighten bounds on $\tau_5$. The central identities are the derivative relationship

$$\frac{d}{dR}\bigl[V_n(R)\bigr] = S_{n-1}(R), \tag{1}$$

the two-step volume recurrence

$$V_n(R) = \frac{2\pi}{n}\,R^2\,V_{n-2}(R), \tag{2}$$

and the pyramid decomposition arising from the integral $\int_0^R r^{n-1}\,dr = R^n/n$, which implies that each infinitesimal cone from the center of an $n$-ball to a surface patch $d\Omega$ has volume $(1/n)\,R^n\,d\Omega$. Equation (1) encodes the fundamental connection between a ball's volume and its bounding surface area. Equation (2) links the geometry of $S^{n-1}$ to that of $S^{n-3}$ through a factor of $2\pi/n$. Together, these identities create a web of cross-dimensional constraints that, in principle, could restrict the packing of spherical caps on $S^4$.

This report presents our methods, results, and a thorough assessment of the framework's strengths and limitations. The main conclusion is that while dimensional analysis provides valuable geometric intuition, it does not yield computational improvements over existing LP/SDP bounds. The gap $40 \leq \tau_5 \leq 44$ remains open.

---

## 2. Background and Prior Work

### 2.1 Known Bounds on $\tau_5$

The lower bound $\tau_5 \geq 40$ is achieved by the minimal vectors of the $D_5$ root lattice, which consist of all permutations of $(\pm 1, \pm 1, 0, 0, 0)/\sqrt{2}$, giving $\binom{5}{2} \times 2^2 = 40$ unit vectors in $\mathbb{R}^5$ with pairwise inner products in $\{-1, -1/2, 0, +1/2\}$. This configuration was well known by the time of Conway and Sloane's comprehensive treatise \cite{conway1999sphere}. Recently, Szollosi \cite{szollosi2023five} discovered a third non-isometric 40-point kissing arrangement $Q_5$, distinct from $D_5$ and the Leech-type construction $L_5$, refuting a conjecture of Cohn, Jiao, Kumar, and Torquato about uniqueness. Cohn and Rajagopal \cite{cohn2024variations} subsequently constructed a fourth non-isometric 40-point configuration and analyzed the associated sphere packings.

The upper bound has improved over several decades. Delsarte's linear programming method \cite{delsarte1973algebraic, delsarte1977spherical}, applied systematically by Odlyzko and Sloane \cite{odlyzko1979kissing}, yielded $\tau_5 \leq 46$ using optimal Gegenbauer polynomial certificates. The asymptotic bounds of Kabatyansky and Levenshtein \cite{kabatyansky1978bounds} give $\tau_n \leq 2^{0.401n(1+o(1))}$ but are not sharp for specific small dimensions. Bachoc and Vallentin \cite{bachoc2008new} introduced semidefinite programming (SDP) bounds incorporating three-point correlations, improving the upper bound to $\tau_5 \leq 45$. Mittelmann and Vallentin \cite{mittelmann2010high} then performed high-accuracy numerical SDP computations to obtain $\tau_5 \leq 44.998$, giving the integer bound $\tau_5 \leq 44$, which remains the current best upper bound.

### 2.2 The Delsarte LP Method

The Delsarte linear programming bound \cite{delsarte1973algebraic, delsarte1977spherical} for the kissing number in dimension $n$ uses the Gegenbauer polynomial expansion $f(t) = \sum_{k=0}^{d} f_k\,C_k^{\lambda}(t)$ with $\lambda = (n-2)/2$. The bound states that $\tau_n \leq f(1)/f_0$ whenever $\hat{f}(k) = f_k \geq 0$ for all $k \geq 1$ and $f(t) \leq 0$ for all $t \in [-1, 1/2]$. This approach is tight for $n = 8$ and $n = 24$, where "magic" polynomials exist whose root structure matches the inner product spectrum of the optimal codes ($E_8$ and the Leech lattice). For $n = 5$, no such magic polynomial exists, and the LP bound plateaus at approximately 46 \cite{odlyzko1979kissing, pfender2007improved}.

### 2.3 SDP Extensions

The SDP method of Bachoc and Vallentin \cite{bachoc2008new} extends the Delsarte LP by incorporating three-point correlations --- the joint distribution of inner products among triples of points on the sphere. This is enforced through positive semidefiniteness constraints on matrix-valued functions of triple inner products $(t_1, t_2, t_3)$. The resulting bound is strictly stronger than the Delsarte LP for most dimensions and has been further refined by Machado and de Oliveira Filho \cite{machado2018improving} using polynomial symmetry exploitation. The survey of Pfender and Ziegler \cite{pfender2004kissing} provides an accessible introduction to the history of the problem, while Boyvalenkov, Dodunekov, and Musin \cite{boyvalenkov2012survey} give a comprehensive overview of bounds across all dimensions.

---

## 3. The Dimensional Analysis Framework

### 3.1 Volume--Surface Derivative Relationship

The $n$-dimensional ball of radius $R$ has volume $V_n(R) = \frac{\pi^{n/2}}{\Gamma(n/2+1)}\,R^n$ and bounding surface area $S_{n-1}(R) = \frac{2\pi^{n/2}}{\Gamma(n/2)}\,R^{n-1}$. The derivative relationship $\frac{d}{dR}[V_n(R)] = S_{n-1}(R)$ follows by direct differentiation and the identity $\Gamma(n/2+1) = (n/2)\,\Gamma(n/2)$. We verified this numerically for $n = 3, 4, 5$ using central difference approximation with step size $\varepsilon = 10^{-8}$, obtaining agreement to at least five significant digits (see Figure 2: `dimensional_recurrence.png`).

The dimensional interpretation is that differentiation "peels off" one radial dimension: just as $\frac{d}{dx}[x^2] = 2x$ expresses the perimeter of a square as the derivative of its area, $\frac{d}{dR}[V_n(R)] = S_{n-1}(R)$ expresses the surface area of an $n$-ball as the rate of change of its volume with respect to radius.

### 3.2 The Two-Step Recurrence

The volume recurrence $V_n(R) = \frac{2\pi}{n}\,R^2\,V_{n-2}(R)$ (Equation 2) connects volumes across two dimensions. For dimension 5, this gives $V_5(R) = \frac{2\pi}{5}\,R^2\,V_3(R)$, linking the geometry of $S^4$ to that of $S^2$. The factor $2\pi$ arises from angular integration (a full revolution in the two additional dimensions), while the $1/n$ factor reflects the "thinning" of higher-dimensional balls. We verified this identity numerically for $n = 2$ through $n = 10$, obtaining exact agreement to machine precision at all dimensions tested.

### 3.3 Pyramid Decomposition

The integral identity $\int_0^R r^{n-1}\,dr = R^n/n$ has a direct geometric interpretation: the $n$-ball decomposes into infinitesimal cones (pyramids) radiating from the center to the boundary. Each cone subtending solid angle $d\Omega$ on $S^{n-1}$ has volume

$$dV = \frac{1}{n}\,R^n\,d\Omega. \tag{3}$$

Integrating over all solid angles recovers $V_n(R) = \frac{1}{n}\,R\,S_{n-1}(R)$. Just as $\int x^2\,dx = x^3/3$ means a three-dimensional pyramid is one-third of its bounding cube, Equation (3) means each $n$-dimensional cone fills only $1/n$ of its bounding "cylinder" (the product of base area and radius).

For $n = 5$, the efficiency factor is $1/5 = 0.2$. Each spherical cap of half-angle $\theta$ on $S^4$ corresponds to a cone of volume $(1/5)\,A_{\text{cap}}(5,\theta)$. However, as we demonstrate in Section 5.3 and Figure 3 (`cap_density.png`), this $1/n$ factor cancels perfectly when comparing cone volumes to the total ball volume, so the pyramid decomposition yields the same cap-packing bound as the surface area argument.

### 3.4 Cap Area via Dimensional Integration

The area of a spherical cap of half-angle $\theta$ on $S^{n-1}$ is obtained by integrating lower-dimensional cross-sections:

$$A_{\text{cap}}(n,\theta) = \frac{2\pi^{(n-1)/2}}{\Gamma\!\bigl(\frac{n-1}{2}\bigr)} \int_0^{\theta} (\sin\phi)^{n-2}\,d\phi = \frac{S_{n-1}}{2}\,I_{\sin^2\!\theta}\!\Bigl(\frac{n-1}{2},\,\frac{1}{2}\Bigr), \tag{4}$$

where $I_x(a,b)$ is the regularized incomplete beta function. For $n = 5$ and $\theta = \pi/6$ (the kissing exclusion half-angle), this gives $A_{\text{cap}}(5, \pi/6) = 0.3384803298$, verified against numerical integration of $S^3$ cross-sections to six decimal places.

---

## 4. Methods

### 4.1 Delsarte LP Implementation

We implemented the Delsarte LP bound using a polynomial ansatz search over degree-6 Gegenbauer polynomials. Specifically, we searched over polynomials of the form $f(t) = (t+1)(t-0.5)(t-r_1)^2(t-r_2)^2$ with root parameters $r_1, r_2$ sampled from a grid covering $[-1, 0.5]$. For each candidate polynomial, we verified: (a) the Delsarte nonpositivity condition $f(t) \leq 0$ for $t \in [-1, 0.5]$, and (b) Gegenbauer coefficient positivity $\hat{f}(k) \geq 0$ for $k \geq 1$. The best polynomial found was $(t+1)(t+0.5)^2\,t^2\,(t-0.5)$, yielding $f(1)/f_0 = 51.08$ and hence $\tau_5 \leq 51$. We acknowledge this is weaker than the literature-optimal LP bound of $\tau_5 \leq 46$ \cite{odlyzko1979kissing} because our polynomial family does not include the optimal Gegenbauer combination. The optimal LP and SDP bounds of $\tau_5 \leq 44$ \cite{mittelmann2010high} are used as the definitive reference throughout.

### 4.2 Dimensional Constraints D1--D3

We augmented the LP search with three constraints derived from the dimensional analysis framework:

**D1 (Equatorial Slicing).** Each vertex $v$ in the contact graph of a kissing configuration on $S^4$ has neighbors lying on the equatorial $S^3$ at height $\langle x, v \rangle = 1/2$. Since these neighbors must form a valid spherical code on $S^3$ with minimum angle $60^\circ$, the degree satisfies $d(v) \leq \tau_4 = 24$ \cite{musin2008kissing}.

**D2 (Gram Matrix Trace).** For $k$ unit vectors in $\mathbb{R}^5$, the Gram matrix $G = X^TX$ has rank at most 5 and diagonal entries 1. The trace inequality $\operatorname{tr}(G^2) \geq k^2/5$ (from rank 5) combined with $\operatorname{tr}(G^2) \leq k(k+3)/4$ (from off-diagonal entries in $[-1, 1/2]$) gives $k^2/5 \leq k(k+3)/4$, equivalently $k(4-5) \leq 3 \cdot 5$, i.e., $-k \leq 15$, which is vacuous for positive $k$.

**D3 (Volume Recurrence Consistency).** The recurrence $V_n = (2\pi/n)\,V_{n-2}$ implies that Gegenbauer coefficients of the cap indicator function satisfy a cross-dimensional consistency relation. We measured the coefficient of variation (CoV) of the harmonic dimension ratios $h(5,k)/h(3,k)$ for the LP certificate polynomial; values exceeding 1.0 were flagged as inconsistent.

### 4.3 Contact Graph Analysis

We computed the contact graph of the $D_5$ kissing configuration using the criterion that vertices $i, j$ are adjacent if and only if $\langle w_i, w_j \rangle = 1/2$. We determined graph-theoretic invariants (clique number, independence number, chromatic number, eigenvalue spectrum) using networkx. We derived a refined vertex degree bound by observing that projected co-neighbors on $S^3$ have minimum angle $\arccos(1/3) \approx 70.53^\circ$ rather than $60^\circ$, yielding $d(v) \leq 21$ via the cap-packing bound on $S^3$.

### 4.4 Construction Attempts

We attempted to find a 41st kissing vector using three strategies applied to the $D_5$ base configuration: (a) random grid search with 100,000 uniformly sampled points on $S^4$, (b) nonlinear optimization with 50 random starting points minimizing the maximum inner product with the existing 40 vectors, and (c) algebraic construction of 354 candidate vectors based on symmetry subgroups of $D_5$. All candidates were validated using the spherical code checker from `src/spherical_codes.py`.

### 4.5 Cross-Dimensional Consistency

We implemented a cross-dimensional consistency check exploiting $V_n = (2\pi/n)\,V_{n-2}$ to derive implications for cap densities across dimensions. For each candidate $\tau_5 \in \{40, 41, 42, 43, 44\}$, we computed the implied cap density on $S^4$ and checked compatibility with known kissing numbers $\tau_3 = 12$ and $\tau_4 = 24$ via the projected density ratios.

---

## 5. Results

### 5.1 Baseline Bounds

Our baseline computations establish the following hierarchy of bounds for $\tau_5$ (see Figure 1: `bound_comparison.png`):

**Cap packing.** The simple area ratio bound gives

$$\tau_5 \leq \left\lfloor \frac{S_4(1)}{A_{\text{cap}}(5,\pi/6)} \right\rfloor = \left\lfloor \frac{26.3189}{0.3385} \right\rfloor = 77. \tag{5}$$

This is the weakest upper bound, reflecting only the constraint that non-overlapping caps cannot exceed the total sphere area.

**Delsarte LP (our search).** Our polynomial ansatz search yields $\tau_5 \leq 51$, corresponding to the polynomial $f(t) = (t+1)(t+0.5)^2\,t^2\,(t-0.5)$ with $f(1)/f_0 = 51.08$.

**Literature-optimal LP.** The optimal Delsarte LP bound, using carefully chosen Gegenbauer polynomial certificates, gives $\tau_5 \leq 46$ \cite{odlyzko1979kissing, levenshtein1979boundaries, pfender2007improved}.

**SDP bound.** The three-point SDP of Bachoc and Vallentin \cite{bachoc2008new} gives $\tau_5 \leq 45$, refined by Mittelmann and Vallentin \cite{mittelmann2010high} to $\tau_5 \leq 44$. This is the current best upper bound.

The complete baseline metrics across dimensions 2--8 are summarized in Table 1:

| $n$ | Known $\tau_n$ | Cap Packing | Delsarte LP | SDP (M--V) |
|-----|---------------|-------------|-------------|------------|
| 2   | 6             | 6           | 6           | 6          |
| 3   | 12            | 14          | 13          | 12         |
| 4   | 24            | 34          | 25          | 24         |
| 5   | 40--44        | 77          | 46          | 44         |
| 6   | 72--77        | 170         | 82          | 77         |
| 7   | 126--134      | 368         | 140         | 134        |
| 8   | 240           | 788         | 240         | 240        |

The cap-packing bound grows exponentially weaker relative to the true kissing number as dimension increases, while the Delsarte LP is tight only for $n = 2$ and $n = 8$.

### 5.2 Enhanced Bounds with Dimensional Constraints

Adding the dimensional constraints D1--D3 to the Delsarte LP produces the following sensitivity analysis:

| Constraint   | Bound with only this | Bound without this | Impact | Status            |
|-------------|---------------------|-------------------|--------|-------------------|
| D1 (equatorial) | 51               | 51                | 0      | Non-binding       |
| D2 (trace)      | 51               | 51                | 0      | Vacuous for $n \geq 4$ |
| D3 (recurrence) | 51               | 51                | 0      | Soft, no rejections |

All three constraints are entirely redundant for $n = 5$. D1 is non-binding because the LP bound of $\leq 51$ (or the true bound of $\leq 44$) permits contact graphs with maximum degree well below $\tau_4 = 24$. D2 is algebraically vacuous for $n \geq 4$ because the coefficient $(4 - n)$ in the trace inequality $k(4-n) \leq 3n$ becomes non-positive. D3 is a soft constraint measuring cross-dimensional consistency of the LP polynomial's Gegenbauer coefficients; the CoV of 0.7368 indicates substantial variation, but this is expected since the LP certificate is not a geometric object subject to volume recurrence.

The fundamental issue is a **category mismatch**: the Delsarte LP operates in the dual polynomial space (spectral constraints on Gegenbauer coefficients), while dimensional constraints encode geometric/structural information about actual point configurations. These two types of information live in different mathematical spaces, and the geometric constraints are not strong enough to eliminate valid LP certificates.

The enhanced bound remains $\tau_5 \leq 51$ (our search) or $\tau_5 \leq 44$ (literature SDP). No improvement was achieved.

### 5.3 Pyramid Decomposition

The pyramid decomposition recasts the cap-packing bound in terms of cone volumes:

$$k \cdot \frac{1}{n}\,A_{\text{cap}}(n,\pi/6) \leq \frac{1}{n}\,S_{n-1}(1). \tag{6}$$

The factor $1/n$ cancels from both sides, yielding $k \cdot A_{\text{cap}} \leq S_{n-1}$, which is identical to the surface area bound (Equation 5). We verified this algebraic cancellation numerically for $n = 3, 4, 5$: in all cases, the ratio of volume fraction to surface fraction per cap equals exactly 1.0.

The cap density analysis provides additional geometric insight (Figure 3: `cap_density.png`). Defining $\rho_n = \tau_n \cdot A_{\text{cap}}(n,\pi/6) / S_{n-1}$, the fraction of $S^{n-1}$ covered by exclusion caps, we find:

| $\tau_5$ | Total cap area | Fraction of $S^4$ | $\rho_5$ |
|----------|---------------|-------------------|----------|
| 40       | 13.539        | 51.44\%           | 0.5144   |
| 41       | 13.878        | 52.73\%           | 0.5273   |
| 42       | 14.216        | 54.01\%           | 0.5401   |
| 43       | 14.555        | 55.30\%           | 0.5530   |
| 44       | 14.893        | 56.59\%           | 0.5659   |

Both $\tau_5 = 40$ and $\tau_5 = 44$ use only about 51--57\% of the sphere's surface area, confirming that the cap-packing bound (which allows up to 100\% coverage) is far from tight. The cap density decreases monotonically with dimension: $\rho_2 = 1.00$, $\rho_3 = 0.80$, $\rho_4 = 0.69$, $\rho_8 = 0.30$, $\rho_{24} = 0.002$, reflecting the curse of dimensionality in sphere packing.

Three verified lemmas from the pyramid decomposition analysis are:

- **Lemma 1.** $V_n(1)/S_{n-1}(1) = 1/n$, decreasing monotonically with $n$. (Verified for $n = 2, \ldots, 10$ to machine precision.)
- **Lemma 2.** The cap density satisfies $\rho_n \leq 1$ with equality if and only if $n = 2$. (Verified for $n = 2, 3, 4, 8, 24$.)
- **Lemma 3.** The pyramid volume bound for $\tau_5$ gives $\tau_5 \leq 77$, identical to the cap-packing bound; the $1/n$ factor cancels. (Verified numerically: volume fraction equals surface fraction for $n = 3, 4, 5$.)

### 5.4 Contact Graph Analysis

The contact graph of the $D_5$ configuration has the following structure (see Figure 4: `contact_graph.png`):

| Property              | Value                                    |
|-----------------------|------------------------------------------|
| Vertices              | 40                                       |
| Edges (contact pairs) | 240                                      |
| Regularity            | 12-regular                               |
| Diameter              | 3                                        |
| Clique number $\omega$ | 4                                       |
| Independence number $\alpha$ | 8                                 |
| Chromatic number $\chi$ | 5                                      |
| Vertex-transitive     | Yes (4-class association scheme)         |

The inner product spectrum contains exactly four values: $\{-1, -1/2, 0, +1/2\}$ with multiplicities $(20, 240, 280, 240)$ among the $\binom{40}{2} = 780$ pairs.

**Refined degree bound.** If $w_1, w_2$ are both neighbors of $v$ (so $\langle w_i, v \rangle = 1/2$), writing $w_i = (1/2)v + (\sqrt{3}/2)\,u_i$ where $u_i$ is a unit vector orthogonal to $v$, the kissing constraint $\langle w_1, w_2 \rangle \leq 1/2$ becomes

$$\langle u_1, u_2 \rangle \leq \frac{1}{3}. \tag{7}$$

The projected minimum angle on $S^3$ is therefore $\arccos(1/3) \approx 70.53^\circ$, which is stricter than the $60^\circ$ kissing constraint. The cap-packing bound on $S^3$ with half-angle $\arccos(1/3)/2 \approx 35.26^\circ$ gives

$$d(v) \leq \left\lfloor \frac{S_3(1)}{A_{\text{cap}}(4, 35.26^\circ)} \right\rfloor = \left\lfloor \frac{19.739}{0.905} \right\rfloor = 21. \tag{8}$$

This improves the naive bound $d(v) \leq \tau_4 = 24$ by three. In the $D_5$ lattice, the maximum vertex degree is 12, well below either bound. The refined bound $d(v) \leq 21$ does not, by itself, rule out any value of $\tau_5$ in $\{41, \ldots, 44\}$, as the edge and degree constraints are easily satisfiable for all candidate values.

**Local rigidity of $D_5$.** For any unit vector $x \in \mathbb{R}^5$, the maximum inner product with the $D_5$ configuration satisfies

$$\max_{w \in D_5} \langle x, w \rangle \geq \sqrt{2/5} = 0.6325. \tag{9}$$

The minimum is attained at the "democratic" direction $x = \pm(1,1,1,1,1)/\sqrt{5}$, where exactly 10 $D_5$ vectors achieve the maximum. Since $\sqrt{2/5} > 1/2$, no 41st point can be added to $D_5$. The angular gap between the achieved minimum angle ($\arccos(\sqrt{2/5}) \approx 50.77^\circ$) and the required $60^\circ$ is $9.23^\circ$, corresponding to an inner product violation of $\sqrt{2/5} - 1/2 \approx 0.1325$. Monte Carlo verification with 100,000 random points on $S^4$ confirmed that no sampled point achieved a maximum inner product below 0.5.

### 5.5 Construction Attempts

All three strategies for finding a 41st point failed:

| Strategy                | Samples/Starts | Valid 41st points | Best max inner product |
|------------------------|----------------|-------------------|----------------------|
| Random grid search      | 100,000        | 0                 | 1.0000               |
| Nonlinear optimization  | 50             | 0                 | 0.6325               |
| Algebraic construction  | 354            | 0                 | 0.6325               |

The best achievable maximum inner product is $\sqrt{2/5} \approx 0.6325$, with a margin from feasibility of $-0.1325$. This provides computational evidence supporting the conjecture $\tau_5 = 40$, consistent with the fact that multiple independent research groups have found several non-isometric 40-point configurations \cite{szollosi2023five, cohn2024variations} but no 41-point configuration has ever been constructed.

---

## 6. Discussion

### 6.1 Why Dimensional Analysis Does Not Close the Gap

The fundamental limitation of the dimensional analysis framework is that it operates on **individual cap constraints** rather than the **global angular distribution** of the configuration. The cap-packing bound states that the total area of $k$ non-overlapping caps of half-angle $\pi/6$ cannot exceed the total surface area of $S^{n-1}$. This is a constraint on the sum of individual cap areas. It does not incorporate any information about pairwise relationships between caps --- the fact that if two caps are close together, the constraints on their joint neighborhood become more restrictive.

The Delsarte LP, by contrast, constrains the angular distribution of all $\binom{k}{2}$ pairwise inner products simultaneously through the polynomial positivity conditions on the Gegenbauer expansion. This is why the LP can prove $\tau_5 \leq 46$ while the cap-packing bound gives only $\tau_5 \leq 77$: the LP exploits pairwise correlations that the geometric bound ignores. The SDP of Bachoc and Vallentin \cite{bachoc2008new} goes further by constraining three-point correlations (the joint distribution of angles in triples of points), which is why the SDP improves the bound from 46 to 44 \cite{mittelmann2010high}. Each step up the hierarchy --- from cap packing (1-point) to Delsarte LP (2-point) to SDP (3-point) --- captures more structural information and yields tighter bounds.

Our dimensional constraints D1--D3 attempt to bridge this gap by adding structural constraints to the LP. However, as the sensitivity analysis demonstrates, these constraints operate at a different mathematical level (geometric/structural vs. spectral/global) and are either already implied by the LP or too weak to be active. The volume recurrence $V_n = (2\pi/n)\,V_{n-2}$ relates cap geometry across dimensions, but the LP certificate polynomial is a mathematical tool in a dual space, not a geometric object constrained by cross-dimensional volume identities.

### 6.2 Comparison to Prior Methods

Our investigation explicitly compared results with 16 papers from the bibliography. The comparison reveals that our upper bound results match prior work only for the simple cap-packing bound ($\tau_5 \leq 77$, folklore \cite{pfender2004kissing}) and the $D_5$ lower bound ($\tau_5 \geq 40$, \cite{conway1999sphere}). Our enhanced LP achieves $\tau_5 \leq 51$, which is weaker than the standard LP bound of $\leq 46$ \cite{odlyzko1979kissing} and far weaker than the SDP bound of $\leq 44$ \cite{mittelmann2010high}. The complete comparison table, including 10 specific papers with method-by-method analysis, is documented in `results/comparison_with_prior_work.md`.

### 6.3 The Refined Degree Bound as a Minor Contribution

The refined degree bound $d(v) \leq 21$ (Equation 8), improved from the naive $\tau_4 = 24$ bound via the projected angle argument (Equation 7), represents a modest contribution. The projection argument is elementary and follows the same logic used by Musin \cite{musin2008kissing} in his proof of $\tau_4 = 24$, where the projected minimum angle on $S^2$ is also $\arccos(1/3)$. Whether the specific bound $d(v) \leq 21$ for $n = 5$ has been stated explicitly in the literature is unclear; it may appear in unpublished analyses or in work we did not survey. Importantly, this bound does not by itself rule out any value of $\tau_5 \in \{41, \ldots, 44\}$, since any graph on 44 vertices can easily accommodate maximum degree 21.

### 6.4 Numerical Robustness

The sensitivity analysis tested all computations at four precision levels (16, 32, 64, and 128 decimal digits) using mpmath high-precision arithmetic. All cap area and bound computations agreed to at least 15 significant digits across precision levels. The regularized incomplete beta function converges rapidly for the parameter values relevant to $n = 5$ ($a = 2$, $b = 1/2$, $x = 1/4$), confirming numerical stability.

---

## 7. Conclusion

This investigation explored the potential of the dimensional analysis framework --- the derivative relationship $\frac{d}{dR}[V_n] = S_{n-1}$, the volume recurrence $V_n = (2\pi/n)\,R^2\,V_{n-2}$, and the pyramid decomposition $\int r^{n-1}\,dr = r^n/n$ --- to improve bounds on the five-dimensional kissing number $\tau_5$. Our principal findings are as follows.

**Best bounds remain unchanged:** $40 \leq \tau_5 \leq 44$. The lower bound is achieved by the $D_5$ lattice \cite{conway1999sphere}, and the upper bound is due to the SDP computation of Mittelmann and Vallentin \cite{mittelmann2010high}. No improvement was achieved through dimensional analysis.

**The dimensional analysis framework provides geometric insight but not computational improvement.** The pyramid decomposition reveals that $n$-dimensional cones fill only $1/n$ of their bounding cylinders, but this factor cancels when computing cap-packing bounds. The cap density analysis shows $\rho_5 \in [0.514, 0.566]$ for $\tau_5 \in [40, 44]$, meaning only 51--57\% of $S^4$ is covered by exclusion caps --- far from the 100\% ceiling of the cap-packing bound. The dimensional constraints D1--D3 are redundant for $n = 5$.

**Novel contributions.** The investigation yields two minor results that may not have been explicitly stated in the prior literature: (1) the refined degree bound $d(v) \leq 21$ for contact graphs of kissing configurations in $\mathbb{R}^5$, derived from the projected angle constraint $\langle u_1, u_2 \rangle \leq 1/3$ on $S^3$; and (2) a clean, elementary proof of local rigidity for the $D_5$ configuration, showing that the minimum maximum inner product with any candidate 41st point is $\sqrt{2/5} \approx 0.6325$, achieved at the democratic direction $(1,1,1,1,1)/\sqrt{5}$, with an angular gap of $9.23^\circ$.

**Open questions.** Closing the gap $40 \leq \tau_5 \leq 44$ will likely require techniques beyond both the dimensional analysis framework explored here and the current LP/SDP hierarchy. Promising directions include: (a) higher-order ($k$-point) SDP bounds for $k \geq 4$, which are currently computationally intractable; (b) Viazovska-type modular form techniques \cite{viazovska2017sphere}, currently applicable only in dimensions 8 and 24; (c) entirely new algebraic structures (flag algebras, topological methods) encoding the combinatorics of spherical codes; and (d) improved construction methods that might produce a 41-point kissing configuration not derived from the $D_5$ lattice.

---

## References

\cite{delsarte1973algebraic} -- Delsarte, P. (1973). An algebraic approach to the association schemes of coding theory. *Philips Research Reports Supplements*, 10.

\cite{delsarte1977spherical} -- Delsarte, P., Goethals, J.-M., Seidel, J. J. (1977). Spherical codes and designs. *Geometriae Dedicata*, 6(3), 363--388.

\cite{kabatyansky1978bounds} -- Kabatyansky, G. A., Levenshtein, V. I. (1978). Bounds for packings on the sphere and in space. *Problems of Information Transmission*, 14(1), 1--17.

\cite{odlyzko1979kissing} -- Odlyzko, A. M., Sloane, N. J. A. (1979). New bounds on the number of unit spheres that can touch a unit sphere in $n$ dimensions. *J. Combin. Theory Ser. A*, 26(2), 210--214.

\cite{levenshtein1979boundaries} -- Levenshtein, V. I. (1979). On bounds for packings in $n$-dimensional Euclidean space. *Soviet Mathematics Doklady*, 20, 417--421.

\cite{schutte1953problem} -- Schutte, K., van der Waerden, B. L. (1953). Das Problem der dreizehn Kugeln. *Math. Ann.*, 125, 325--334.

\cite{conway1999sphere} -- Conway, J. H., Sloane, N. J. A. (1999). *Sphere Packings, Lattices and Groups*, 3rd ed. Springer-Verlag.

\cite{pfender2004kissing} -- Pfender, F., Ziegler, G. M. (2004). Kissing numbers, sphere packings, and some unexpected proofs. *Notices of the AMS*, 51(8), 873--883.

\cite{pfender2007improved} -- Pfender, F. (2007). Improved Delsarte bounds for spherical codes in small dimensions. *J. Combin. Theory Ser. A*, 114(6), 1133--1147.

\cite{cohn2007universally} -- Cohn, H., Kumar, A. (2007). Universally optimal distribution of points on spheres. *J. Amer. Math. Soc.*, 20(1), 99--148.

\cite{musin2008kissing} -- Musin, O. R. (2008). The kissing number in four dimensions. *Ann. of Math.*, 168(1), 1--32.

\cite{bachoc2008new} -- Bachoc, C., Vallentin, F. (2008). New upper bounds for kissing numbers from semidefinite programming. *J. Amer. Math. Soc.*, 21(3), 909--924.

\cite{mittelmann2010high} -- Mittelmann, H. D., Vallentin, F. (2010). High-accuracy semidefinite programming bounds for kissing numbers. *Experimental Mathematics*, 19(2), 175--179.

\cite{boyvalenkov2012survey} -- Boyvalenkov, P., Dodunekov, S., Musin, O. R. (2012). A survey on the kissing numbers. *Serdica Math. J.*, 38, 507--522.

\cite{viazovska2017sphere} -- Viazovska, M. S. (2017). The sphere packing problem in dimension 8. *Ann. of Math.*, 185(3), 991--1015.

\cite{machado2018improving} -- Machado, F. C., de Oliveira Filho, F. M. (2018). Improving the semidefinite programming bound for the kissing number by exploiting polynomial symmetry. *Experimental Mathematics*, 27(3), 362--369.

\cite{szollosi2023five} -- Szollosi, F. (2023). A note on five dimensional kissing arrangements. *Math. Research Letters*, 30(5).

\cite{cohn2024variations} -- Cohn, H., Rajagopal, A. (2024). Variations on five-dimensional sphere packings. arXiv preprint arXiv:2412.00937.

\cite{cohn2003new} -- Cohn, H., Elkies, N. (2003). New upper bounds on sphere packings I. *Ann. of Math.*, 157(2), 689--714.

\cite{zong2008kissing} -- Zong, C. (2008). The kissing number, blocking number and covering number of a convex body. In *Surveys on Discrete and Computational Geometry*, Contemp. Math. 453, pp. 529--548.
