# Contact Graph Analysis via Dimensional Volume Arguments

## 1. D5 Contact Graph Structure

The D5 lattice kissing configuration consists of 40 unit vectors in R^5, namely all
permutations of (+/-1, +/-1, 0, 0, 0)/sqrt(2). The **contact graph** G has a vertex
for each vector and an edge for each pair with inner product exactly +1/2 (angular
separation exactly 60 degrees).

### Basic Properties (verified computationally)

| Property | Value |
|----------|-------|
| Vertices | 40 |
| Edges (contact pairs) | 240 |
| Regularity | 12-regular (every vertex has degree 12) |
| Connected | Yes |
| Diameter | 3 |
| Girth (shortest cycle) | 3 |
| Triangles | 400 |
| Vertex-transitive | Yes (all neighborhood profiles identical) |

### Inner Product Spectrum

The 780 = C(40,2) pairwise inner products take exactly four values:

| Inner product | Angle (degrees) | Number of pairs | Interpretation |
|--------------|-----------------|-----------------|----------------|
| -1 | 180.0 | 20 | Antipodal pairs |
| -1/2 | 120.0 | 240 | "Anti-contact" pairs |
| 0 | 90.0 | 280 | Orthogonal pairs |
| +1/2 | 60.0 | 240 | Contact pairs (edges) |

The four-valued inner product spectrum is characteristic of the D5 root system. The
inner products between co-neighbors of any vertex take values {-1/2, 0, +1/2}, with
multiplicities (6, 30, 30) respectively.

### Graph-Theoretic Invariants

| Invariant | Value | Method |
|-----------|-------|--------|
| Clique number (omega) | 4 | Exact computation (max clique found) |
| Independence number (alpha) | 8 | Exact (via complement max clique, networkx) |
| Chromatic number (chi) | 5 | Exact (constructive 5-coloring via coordinate partition) |
| Fractional chromatic number | 5.0 | Equals n/alpha for vertex-transitive graphs |

**Chromatic number proof.** The 40 vectors are indexed by coordinate pairs {i,j} with
i < j (10 pairs) and sign patterns (4 per pair). Two vectors sharing no coordinate index
are orthogonal (inner product 0), hence non-adjacent. A partition of the 10 coordinate
pairs into 5 groups of 2 disjoint pairs yields a proper 5-coloring with color classes of
size 8. For example:

    Color 0: {0,1} union {2,3}  (8 vertices)
    Color 1: {0,2} union {1,4}  (8 vertices)
    Color 2: {0,3} union {2,4}  (8 vertices)
    Color 3: {0,4} union {1,3}  (8 vertices)
    Color 4: {1,2} union {3,4}  (8 vertices)

Since alpha = 8 and n = 40, we have chi >= ceil(40/8) = 5, matching the construction.

### Spectral Properties

The adjacency matrix has exactly 6 distinct eigenvalues:

| Eigenvalue | Multiplicity |
|------------|-------------|
| +12 | 1 |
| +6 | 5 |
| +2 | 4 |
| 0 | 10 |
| -2 | 15 |
| -4 | 5 |

The Hoffman independence bound gives alpha <= 40 * 4 / (12 + 4) = 10, and the Hoffman
chromatic bound gives chi >= 1 + 12/4 = 4. Both are satisfied by the actual values
(alpha = 8, chi = 5). The graph is **not** strongly regular: non-adjacent pairs have
varying numbers of common neighbors depending on their inner product:

| Relation | Inner product | Common neighbors | Number of pairs |
|----------|--------------|-----------------|-----------------|
| Adjacent | +1/2 | 5 | 240 |
| Orthogonal | 0 | 4 or 6 | 280 |
| Anti-contact | -1/2 | 1 | 240 |
| Antipodal | -1 | 0 | 20 |

The four inner product classes form a 4-class association scheme on 40 points.

---

## 2. Constraints on Hypothetical 41-Point Contact Graphs

### Maximum Vertex Degree

For any kissing configuration in R^5, each vertex v has neighbors lying on the
equatorial 3-sphere S^3 (the intersection of S^4 with the hyperplane orthogonal to v,
at height <x,v> = 1/2). The degree d(v) is bounded in two ways:

**Naive bound (from tau_4).** The neighbors of v lie on a great S^3, and they must
form a valid spherical code with minimum angle 60 degrees. Since the kissing number
in R^4 is tau_4 = 24, we get d(v) <= 24.

**Refined bound (projected constraint).** If w1, w2 are both neighbors of v (so
<w_i, v> = 1/2), then writing w_i = (1/2)v + (sqrt(3)/2)u_i where u_i lies on the
unit S^3 orthogonal to v:

    <w1, w2> = 1/4 + (3/4)<u1, u2>

The kissing constraint <w1, w2> <= 1/2 then requires <u1, u2> <= 1/3. This is
**stricter** than the kissing constraint <u1, u2> <= 1/2; the projected minimum angle
is arccos(1/3) = 70.53 degrees rather than 60 degrees.

Applying the cap packing bound on S^3 with half-angle arccos(1/3)/2 = 35.26 degrees:

    d(v) <= floor(S_3 / A_cap(4, 35.26 deg)) = floor(19.739 / 0.905) = floor(21.81) = 21

**Verified:** In the D5 lattice, vertex 0 has 12 neighbors. The projected neighbors on
S^3 have inner product spectrum {-1, -1/3, +1/3} with multiplicities (6, 30, 30). The
maximum projected inner product is exactly 1/3, confirming the constraint is tight.

### Handshaking Constraints

For a k-vertex contact graph with degree sequence (d_1, ..., d_k):

    sum(d_i) = 2|E|,  0 <= d_i <= 21

For k = 41: if average degree is d_avg, then |E| = 41 * d_avg / 2. A 41-point
configuration need not be regular. The degree sequence must satisfy:

- Each d_i in {0, 1, ..., 21}
- sum(d_i) is even (handshaking lemma)
- The sequence is graphically realizable (Erdos-Gallai conditions)

### Degree Sequence Constraints for Adding a 41st Point

If the 41st point v* has degree d in the contact graph, then:
- d neighbors of v* come from the existing configuration (or a modified one)
- The remaining 40 - d vertices are non-adjacent to v*
- v* must have inner product <= 1/2 with all 40 other points, and exactly = 1/2 with
  its d neighbors

In the D5 lattice, the minimum achievable max inner product for a 41st point is
sqrt(2/5) = 0.6325, attained at the "democratic" point (1,1,1,1,1)/sqrt(5). This
exceeds 0.5, so **no 41st point can be added to the D5 configuration**.

However, this does not rule out a completely different 41-point configuration that is
not an extension of D5.

---

## 3. Dimensional Volume Constraints on Subconfigurations

### Equatorial Projection Lemma

**Lemma 1.** For any vertex v in a kissing configuration on S^4, the d(v) neighbors
project to points on S^3 (after removing the v-component) with pairwise inner products
at most 1/3. The cap packing bound for this projected configuration gives d(v) <= 21.

*Proof.* See Section 2 (refined bound). Verified numerically for all 40 vertices of D5.

### Chain Constraints

**Lemma 2.** If v has d(v) = 21 neighbors (the maximum possible), the neighbors of v
occupy a large fraction of the equatorial S^3. Any vertex w adjacent to one of v's
neighbors but not to v itself must be "squeezed" into the remaining angular space.

Quantitatively, the solid angle subtended by v and its d neighbors on S^4 is at least:

    Omega(v, N(v)) >= (1 + d) * omega_cap(5, pi/6)

where omega_cap(5, pi/6) = 0.012861 is the fractional solid angle of a single cap of
half-angle pi/6 on S^4.

| d(v) | (1+d) * omega_cap | Percentage of S^4 |
|------|-------------------|-------------------|
| 12 | 0.1672 | 16.72% |
| 20 | 0.2701 | 27.01% |
| 21 | 0.2829 | 28.29% |
| 24 | 0.3215 | 32.15% |

Even at the maximum degree d = 21, a vertex and its neighbors consume only ~28% of S^4.
This leaves substantial room for the remaining k - 1 - d vertices, so the pyramid-volume
constraint is not binding.

### The 1/n Factor and Dimensional Wastage

The identity V_n = S_{n-1} * R / n implies that each spherical cap of half-angle theta
on S^{n-1} corresponds to a "pyramid" of volume (1/n) * cap_area * R. For n = 5, the
factor 1/5 means each cap's pyramid is only 20% of what a "flat" slab of the same base
area would occupy. Higher dimensions have greater wastage (smaller 1/n factor), but this
affects all configurations equally and does not differentiate between k = 40 and k = 41.

**Lemma 3.** The total solid angle of k = 44 caps on S^4 is 44 * 0.012861 = 0.5659,
or 56.59% of the sphere. Since this is less than 100%, the simple volume argument does
not rule out k = 44.

*Verified numerically.* For each k in {40, 41, 42, 43, 44}, the total cap fraction is
well below 100%.

---

## 4. Can a 41-Point Graph Exist?

### Local Rigidity of D5

The D5 lattice achieves 40 points with degree 12. To add a 41st point, one needs a unit
vector v* on S^4 such that <v*, w> <= 1/2 for all 40 D5 vectors w.

**Theorem (computational).** For any unit vector x in R^5, the maximum inner product
with the D5 configuration satisfies:

    max_w <x, w> >= sqrt(2/5) = 0.632456...

This minimum is achieved when |x_0| = |x_1| = ... = |x_4| = 1/sqrt(5) (the
"democratic" directions). In these directions, exactly 10 D5 vectors achieve the
maximum inner product.

*Proof.* For a unit vector x = (x_0, ..., x_4), the maximum inner product with D5 is:

    max_{i<j, s_i, s_j} (s_i x_i + s_j x_j) / sqrt(2)  =  max_{i<j} (|x_i| + |x_j|) / sqrt(2)

This equals (|x_{(1)}| + |x_{(2)}|) / sqrt(2), where |x_{(1)}| >= |x_{(2)}| >= ...
are the sorted absolute values. Minimizing subject to sum x_i^2 = 1, by Lagrange
multipliers the minimum occurs when all |x_i| = 1/sqrt(5), giving
2/(sqrt(5)*sqrt(2)) = sqrt(2/5).

### The Angular Gap

| Quantity | Value |
|----------|-------|
| Required max inner product | <= 0.5000 (60.00 degrees) |
| Best achievable max inner product | 0.6325 (50.77 degrees) |
| Angular gap | 9.23 degrees |
| Inner product violation | 0.1325 |

The gap of 9.23 degrees means the D5 configuration is **locally rigid** against
augmentation: there is no direction on S^4 that is at least 60 degrees from all 40
D5 vectors.

### Monte Carlo Verification

100,000 uniformly random points on S^4 were tested. Results:

| Statistic | Max inner product | Angle to nearest D5 vector |
|-----------|------------------|---------------------------|
| Minimum (worst case) | 0.6519 | 49.31 degrees |
| 1st percentile | 0.7354 | 42.65 degrees |
| Median | 0.8679 | 29.78 degrees |
| Maximum (best case) | 0.9991 | 2.45 degrees |
| Fraction with max_ip < 0.5 | 0.0000 | -- |

No random point achieved max inner product below 0.5. The theoretical minimum of
sqrt(2/5) = 0.6325 was not reached by random sampling (the Monte Carlo minimum was
0.6519), confirming that the extremal point (1,...,1)/sqrt(5) lies in a thin region
of S^4.

### Implication for Non-D5 Configurations

The above analysis shows that a 41st point cannot be added **to D5**. It does not
rule out an entirely different 41-point configuration. To construct such a configuration,
one would need to:

1. Abandon the D5 lattice structure entirely
2. Find 41 unit vectors with pairwise inner products <= 1/2
3. The contact graph would likely be non-regular and less symmetric than D5

No such construction has been found (see construction_attempts.md), but this remains
an open possibility.

---

## 5. Ruling Out High Kissing Numbers

### Graph-Theoretic Feasibility Table

For each hypothetical k in {40, ..., 44}, the following constraints must be satisfied:

| k  | Min edges (rigidity) | Max edges (d<=21) | Cap fraction | d_avg range | Graph-feasible? |
|----|---------------------|-------------------|-------------|-------------|----------------|
| 40 | 150 | 420 | 51.44% | 7.50 -- 21 | YES (D5: 240 edges, d_avg=12) |
| 41 | 154 | 430 | 52.73% | 7.51 -- 21 | YES |
| 42 | 158 | 441 | 54.01% | 7.52 -- 21 | YES |
| 43 | 162 | 451 | 55.30% | 7.53 -- 21 | YES |
| 44 | 166 | 462 | 56.59% | 7.55 -- 21 | YES |

where:
- **Min edges (rigidity):** A spherical framework on S^4 has 4k - 10 degrees of freedom
  (4 per point on S^4, minus dim SO(5) = 10). Rigidity requires at least this many edge
  constraints. Hence |E| >= 4k - 10, giving d_avg >= 2(4k - 10)/k.
- **Max edges (d <= 21):** From the refined degree bound d(v) <= 21 (Section 2), the
  maximum edge count is k * 21 / 2.
- **Cap fraction:** The fraction of S^4 covered by k non-overlapping caps of half-angle
  pi/6. All values are well below 100%.

### Can We Rule Out tau_5 = 44?

For k = 44 with d_max = 21:
- Minimum edges from rigidity: 4 * 44 - 10 = 166, giving d_avg >= 7.55
- Maximum edges: 44 * 21 / 2 = 462
- Cap fraction: 56.59% < 100%
- All constraints are satisfiable

**Conclusion:** Graph-theoretic constraints alone (degree bounds, edge bounds, cap
packing) **cannot** rule out tau_5 = 44. The constraints are too loose by themselves.

### Why Graph Theory Is Insufficient

The fundamental limitation is that graph-theoretic constraints are **necessary but not
sufficient** for geometric realizability. An abstract graph may satisfy all degree, edge,
and coloring constraints yet fail to embed on S^4 with the required angular separations.
The key obstructions are:

1. **Gram matrix rank constraint:** The k x k Gram matrix G = X^T X must have rank <= 5
   (since the vectors lie in R^5). This imposes k*(k-1)/2 - 5*(5+1)/2 + ... nonlinear
   constraints on the inner products.

2. **Positive semidefiniteness:** G must be positive semidefinite with diagonal entries 1
   and off-diagonal entries in [-1, 1/2].

3. **Rigidity:** The contact graph must be realizable as a **rigid** framework on S^4,
   not just as an abstract graph with consistent degree sequence.

These geometric constraints are captured by semidefinite programming (SDP) methods,
which give the tightest known bound tau_5 <= 44 (Delsarte LP, tightened by
Mittelmann-Vallentin SDP). Closing the gap 40-44 requires either new SDP constraints
or new constructions.

---

## 6. Summary

### Key Findings

1. **D5 contact graph structure:** 40 vertices, 12-regular, 240 edges, vertex-transitive.
   The graph is a 4-class association scheme with inner product spectrum {-1, -1/2, 0, +1/2}.
   Exact invariants: omega = 4, alpha = 8, chi = 5.

2. **Refined degree bound:** The projection of co-neighbors onto S^3 has minimum angle
   arccos(1/3) = 70.53 degrees (stricter than 60 degrees). The cap packing bound on S^3
   gives d(v) <= 21, improving the naive tau_4 = 24 bound.

3. **D5 local rigidity:** The minimum max inner product for any candidate 41st point is
   sqrt(2/5) = 0.6325, exceeding the required threshold of 0.5 by a margin of 0.1325
   (angular gap of 9.23 degrees). This proves no 41st point can be added to D5.

4. **Graph-theoretic feasibility:** For all k in {40, 41, 42, 43, 44}, the basic
   graph-theoretic constraints (degree <= 21, edge bounds from rigidity, cap fraction
   < 100%) are satisfied. Graph theory alone does not eliminate any candidate.

5. **Main obstruction is geometric:** The impossibility of adding a 41st point to D5 is
   a **geometric** fact (the angular gap is too small), not a combinatorial one. Ruling
   out 41-point configurations entirely would require geometric arguments (SDP, Gram
   matrix constraints) beyond pure graph theory.

6. **Dimensional volume is necessary but not sufficient:** The cap fraction for k = 44
   is only 56.59% of S^4, leaving ample room by the volume argument. The 1/n pyramid
   factor does not differentiate between k = 40 and k = 41. Dimensional volume arguments
   provide useful geometric intuition but are not sharp enough to close the 40-44 gap.

### Computations

All claims verified computationally using:
- `src/d5_lattice.py`: D5 vector generation and contact graph construction
- `src/ndim_geometry.py`: Cap areas, solid angles, surface areas via dimensional recurrence
- `networkx`: Graph-theoretic invariants (clique, independence, chromatic number, spectrum)
- Monte Carlo sampling (100,000 points on S^4) for angular gap distribution
- Exact algebraic analysis for the minimum max inner product (sqrt(2/5))
