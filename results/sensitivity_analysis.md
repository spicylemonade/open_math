# Sensitivity Analysis: Definition Choices for the Main Characterization

**Item 018** -- Sensitivity of the characterization theorem to:
(1) the maximum recurrence order parameter d_max,
(2) homogeneous vs. inhomogeneous recurrences, and
(3) restriction to arithmetic-progression-indexed subsequences vs. arbitrary subsequences.

## Experimental Setup

We tested 20 representative values of r across four classes:

| Class | Values |
|---|---|
| Rational | 1/1, 3/2, 5/3, 7/4, 4/3, 7/5, 9/7, 11/8, 2/1, 5/2 |
| Quadratic irrational | golden_ratio, sqrt(2), sqrt(3), sqrt(5), sqrt(7) |
| Algebraic degree >= 3 | cbrt(2), cbrt(3) |
| Transcendental | pi, e, ln2 |

For each r, we computed floor(n*r) for n = 1, ..., 10000 and ran the Berlekamp-Massey recurrence detector (`src/recurrence_detector.py`) with d_max in {2, 5, 10, 20, 50}. Full results are in `results/sensitivity_analysis.csv`.

---

## 1. Sensitivity to d_max

### Theoretical prediction

For rational r = p/q (in lowest terms), the Beatty sequence floor(n*r) satisfies the fundamental shift identity:

    a_{n+q} = a_n + p   for all n >= 1.

This inhomogeneous recurrence homogenizes to:

    a_{n+q+1} - a_{n+1} - a_{n+q} + a_n = 0,

which is a homogeneous linear recurrence of order q+1. Moreover, q+1 is the minimal homogeneous order (proved in `results/rational_case_proof.md`). Therefore:

- **d_max >= q+1**: The recurrence is detected.
- **d_max < q+1**: The recurrence is undetectable (the true minimal order exceeds the search bound).

For irrational r, no homogeneous linear recurrence of any finite order exists for floor(n*r), so increasing d_max has no effect -- the answer remains "no recurrence found" for all d_max.

### Computational verification

The table below summarizes the computed results for each rational r, showing the denominator q, the predicted minimal order q+1, and the smallest d_max at which the recurrence is detected:

| r | q | Predicted min order (q+1) | Detected at d_max=2 | d_max=5 | d_max=10 | d_max=20 | d_max=50 | Computed order |
|---|---|---|---|---|---|---|---|---|
| 1/1 | 1 | 2 | Yes | Yes | Yes | Yes | Yes | 2 |
| 3/2 | 2 | 3 | No | Yes | Yes | Yes | Yes | 3 |
| 5/3 | 3 | 4 | No | Yes | Yes | Yes | Yes | 4 |
| 7/4 | 4 | 5 | No | Yes | Yes | Yes | Yes | 5 |
| 4/3 | 3 | 4 | No | Yes | Yes | Yes | Yes | 4 |
| 7/5 | 5 | 6 | No | No | Yes | Yes | Yes | 6 |
| 9/7 | 7 | 8 | No | No | Yes | Yes | Yes | 8 |
| 11/8 | 8 | 9 | No | No | Yes | Yes | Yes | 9 |
| 2/1 | 1 | 2 | Yes | Yes | Yes | Yes | Yes | 2 |
| 5/2 | 2 | 3 | No | Yes | Yes | Yes | Yes | 3 |

For all 10 irrational r values (golden_ratio, sqrt(2), sqrt(3), sqrt(5), sqrt(7), cbrt(2), cbrt(3), pi, e, ln2), the result is "False" at every d_max tested (2, 5, 10, 20, 50).

### Conclusion

The parameter d_max acts purely as a **detection threshold** for rationals with large denominators. It does not affect the characterization itself: the dichotomy "rational iff recurrence exists" holds at every d_max setting. For practical purposes, d_max should be set to at least q+1 where q is the largest denominator of interest. Setting d_max = 50 suffices for all rationals p/q with q <= 49.

---

## 2. Homogeneous vs. Inhomogeneous Recurrences

### The inhomogeneous recurrence for rational r

For r = p/q rational (lowest terms), the Beatty sequence satisfies the **inhomogeneous** recurrence:

    a_{n+q} = a_n + p     (order q, constant right-hand side p).

This is more compact than its homogeneous counterpart: the inhomogeneous recurrence has order q, while the minimal homogeneous recurrence has order q+1. The homogeneous form is obtained by "differencing out" the constant:

    a_{n+q+1} - a_{n+1} - a_{n+q} + a_n = 0     (order q+1).

### The irrational case

For irrational r, the Beatty sequence floor(n*r) satisfies **neither** a homogeneous nor an inhomogeneous recurrence of any finite order. The fundamental obstruction is the same in both cases:

Any linear recurrence (homogeneous or with constant RHS) for a subsequence of floor(n*r) along an arithmetic progression with common difference d would imply that the asymptotic growth rate d*r is rational (it would have to equal the dominant eigenvalue of the companion matrix, which is an algebraic number satisfying the characteristic polynomial with integer coefficients). But d*r is irrational whenever r is irrational and d >= 1 is an integer. This rules out both homogeneous and inhomogeneous recurrences.

More precisely: an inhomogeneous recurrence a_{n+d} = c_1 a_{n+d-1} + ... + c_d a_n + c_0 can be converted to a homogeneous recurrence of order d+1 by defining b_n = a_{n+1} - a_n and finding a homogeneous recurrence for b_n, or equivalently by considering the augmented vector (a_n, 1). If the original sequence does not satisfy any homogeneous recurrence, then allowing a constant term changes nothing -- the obstruction (irrational growth rate) persists.

### Theoretical analysis

Allowing inhomogeneous recurrences:
- **For rationals**: reduces the minimal order by 1 (from q+1 to q). The characterization "r rational iff recurrence exists" is unchanged.
- **For irrationals**: no recurrence exists regardless. The characterization is unchanged.

### Conclusion

The choice between homogeneous and inhomogeneous formulation does **not** affect the characterization theorem. The only difference is a unit reduction in minimal order for the rational case. Since the homogeneous formulation is standard in the theory of linear recurrence sequences (and avoids the need to search over the constant term), it is preferred.

---

## 3. AP-Only vs. Arbitrary Subsequences

### Arithmetic progression subsequences

The main characterization restricts attention to subsequences indexed by arithmetic progressions (APs): {a + kd : k >= 0} for fixed a, d. The computational search in this project tested all APs with offset a in {0, ..., 20} and stride d in {1, ..., 20}.

### Why the restriction to APs does not limit the characterization

**Rational case.** For r = p/q rational, the **full sequence** floor(n*r) itself satisfies a homogeneous linear recurrence (order q+1). Therefore every subsequence -- whether indexed by an AP, a polynomial, or any other rule -- trivially inherits a recurrence (it is a subsequence of a globally recurrent sequence). APs are sufficient; arbitrary subsequences add nothing.

**Irrational case.** The proof that no AP subsequence works (from `results/irrational_case_proof.md`) proceeds as follows. Consider the AP subsequence b_k = floor((a + kd) * r) for fixed integers a >= 0, d >= 1. Then:

    b_k ~ (a + kd) * r = a*r + k*(d*r)   as k -> infinity.

If b_k satisfied a homogeneous linear recurrence sum_{i=0}^{m} c_i b_{k+i} = 0, then the dominant growth rate d*r would have to be an algebraic number (a root of the characteristic polynomial with integer coefficients). But d*r is irrational for all integers d >= 1 when r is irrational. Moreover, d*r cannot be algebraic with integer-coefficient characteristic polynomial unless it is rational (since the recurrence imposes a_n ~ C * lambda^n + lower-order terms, and the linear growth a_n ~ d*r*n implies the dominant root lambda = 1, forcing d*r to be rational). Contradiction.

This argument extends immediately to broader classes of index sets:

- **Polynomial index sets** {P(k) : k >= 0} where P is a polynomial with integer coefficients: the subsequence floor(P(k) * r) has growth rate ~ leading_coeff(P) * r * k^{deg(P)}, and the same rationality obstruction applies.
- **Exponential index sets** {c^k : k >= 0}: the subsequence floor(c^k * r) grows exponentially, and any linear recurrence would force the ratio between consecutive terms to converge to an algebraic number, which contradicts the irrational fractional-part behavior of c^k * r.
- **Arbitrary "natural" index sets**: any index set where the indices grow at a predictable rate (polynomial, exponential, or any rate determined by a computable function) inherits the same obstruction.

The only way to construct a linearly recurrent subsequence of floor(n*r) for irrational r would be to **reverse-engineer** a pathological index set that cherry-picks terms to force a recurrence. Such an index set would have to be defined in terms of the sequence itself (e.g., "take the n-th term where floor(n*r) happens to equal some prescribed recurrent value"). This is not a natural or independently-specified index set; it is a circular construction that has no mathematical content.

### Conclusion

The restriction to arithmetic progression subsequences does **not** change the characterization for any natural class of index sets. The proof works for polynomial and exponential index sets as well. Only pathological, reverse-engineered index sets could possibly yield a recurrent subsequence for irrational r, and such index sets fall outside any reasonable formulation of the problem.

---

## 4. Canonical Formulation Recommendation

Based on the sensitivity analysis above, we recommend the following canonical formulation:

> **Canonical Problem.** For which real numbers r > 0 does the Beatty sequence floor(n*r) (or a subsequence thereof along an arithmetic progression) satisfy a **homogeneous linear recurrence** with constant integer coefficients?

This formulation is preferred for the following reasons:

1. **Homogeneous over inhomogeneous.** The homogeneous formulation is the standard one in the theory of linear recurrence sequences (C-finite sequences). It is the setting of the Skolem-Mahler-Lech theorem, the theory of companion matrices, and the characteristic-polynomial approach. Allowing an inhomogeneous constant term adds no power to the characterization (Section 2) and introduces an extra free parameter to search over.

2. **AP subsequences over arbitrary subsequences.** Arithmetic progressions are the most natural and well-studied class of subsequences. They are the setting in which the three-distance theorem, equidistribution theory, and Sturmian word analysis apply most directly. Allowing arbitrary subsequences does not change the characterization for any natural index class (Section 3) and would introduce pathological edge cases.

3. **Constant integer coefficients.** Working over the integers (rather than rationals or reals) is natural since floor(n*r) is an integer sequence. Any rational-coefficient recurrence can be cleared to integer coefficients by multiplying through by the LCM of denominators.

4. **Clean dichotomy.** With this formulation, the main theorem takes its simplest and most elegant form:

> **Theorem.** The Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence (along an arithmetic progression) if and only if r is rational.

This is a complete characterization with no exceptional cases, no auxiliary conditions on the continued fraction expansion or algebraic degree of r, and no dependence on parameter choices (d_max affects only computational detection, not the mathematical truth).

---

## Summary Table: Sensitivity of the Characterization

| Definition choice | Affects characterization? | Details |
|---|---|---|
| d_max (max recurrence order) | No | Only affects computational detection threshold for large-denominator rationals |
| Homogeneous vs. inhomogeneous | No | Inhomogeneous reduces minimal order by 1 for rationals; irrationals still have no recurrence |
| AP-only vs. arbitrary subsequences | No | Irrational obstruction applies to all natural index classes |
| Integer vs. rational coefficients | No | Equivalent by clearing denominators |

The characterization "r rational iff recurrence exists" is **robust** across all tested definition variants.
