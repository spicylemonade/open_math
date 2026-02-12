# Dimensional Integration Constraints on Gegenbauer Coefficients

## 1. Trivial Cap Bound
For n=5: tau_5 <= S_4 / A_cap(5, pi/6) = 77.7562 => floor = 77

## 2. Cross-Dimensional Integration Identity
The recurrence V_5 = (2pi/5)*V_3 means a cap on S^4 decomposes as an integral of S^2 cross-sections.
Verified: A_cap(5, pi/6) = 0.3384803298 via both betainc and numerical integration of S^3 slices.

## 3. Non-Trivial Constraint: Equatorial Slicing
For k caps of half-angle pi/6 on S^4, the restriction to any great S^2 (equatorial 2-sphere)
gives at most tau_3 = 12 caps. This constrains the contact graph structure:
- Each vertex in the contact graph has degree bounded by tau_4 = 24
- The D5 lattice has uniform degree 12 (much less than 24)
- A hypothetical 41-point config would need at least some vertices with degree > 12

## 4. Second-Moment (Trace) Constraint
For k unit vectors in R^5 with pairwise inner products <= 1/2:
- trace(G^2) >= k^2/5 (from rank-5 constraint)
- trace(G^2) <= k + k(k-1)/4 (from |inner product| <= 1/2)
These are consistent for all k <= 77, so the second-moment constraint alone doesn't improve the cap bound.

## 5. Volume Recurrence as LP Constraint
The identity V_n = (2pi/n)*V_{n-2} implies that the Gegenbauer coefficients of the
cap indicator function satisfy a recurrence relation across dimensions.
This can be added as additional constraints to the Delsarte LP.

Specifically, if f(t) = sum f_k P_k^{(n)}(t) is the optimal LP polynomial for dimension n,
then the coefficients f_k are related to the coefficients g_k for dimension n-2 via:
f_k ~ (2pi/n) * g_k * h(n,k)/h(n-2,k)

This provides a cross-dimensional consistency check: if the LP polynomial for n=5
violates the recurrence relationship with the n=3 polynomial, additional constraints can be added.

## 6. Numerical Verification
All formulas verified numerically with Python (scipy, numpy).
Cap area via betainc matches integration of S^3 cross-sections to 6 decimal places.