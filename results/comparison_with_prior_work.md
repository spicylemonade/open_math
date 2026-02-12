# Comparison with Prior Work on the Kissing Number in Dimension 5

**Research Rubric Item 019** | Kissing Number Problem, Dimension 5

---

## 1. Comprehensive Comparison Table

The following table compares our results with every paper in the bibliography that provides a bound (upper or lower) on the kissing number $\tau_5$, or contributes a technique that has been applied to $\tau_5$. All citations refer to entries in `sources.bib`.

| Paper | Year | Method | Upper Bound on $\tau_5$ | Lower Bound on $\tau_5$ | Our Result | Match? |
|-------|------|--------|------------------------|------------------------|------------|--------|
| \cite{delsarte1973algebraic} | 1973 | LP framework (abstract) | (framework only) | -- | We implement the LP framework with polynomial ansatz search | Partial: we use the same framework but with a suboptimal polynomial search |
| \cite{delsarte1977spherical} | 1977 | Spherical LP bound | $\sim$46 (implicit) | -- | Our LP ansatz gives $\leq 51$; literature-optimal LP gives $\leq 46$ | NO: our polynomial search is weaker; we do not recover the optimal LP certificate |
| \cite{kabatyansky1978bounds} | 1978 | Asymptotic packing bounds | $\sim$47 (asymptotic, not sharp for $n{=}5$) | -- | Cap-packing bound: $\leq 77$ | NO: both are weaker than LP, but KB bound is tighter asymptotically |
| \cite{odlyzko1979kissing} | 1979 | Delsarte LP (optimized) | $\leq 46$ | 40 (D$_5$ lattice implicit) | Our LP: $\leq 51$; our cap bound: $\leq 77$ | NO: Odlyzko--Sloane's LP is significantly tighter than our ansatz |
| \cite{levenshtein1979boundaries} | 1979 | Levenshtein bound | $\leq 46$ (same as Delsarte for $n{=}5$) | -- | Our LP: $\leq 51$ | NO: Levenshtein's optimal polynomial gives $\leq 46$; our search does not find it |
| \cite{conway1999sphere} | 1999 | D$_5$ lattice construction | -- | 40 | We verify 40-point D$_5$ configuration | YES: we independently verify the D$_5$ construction with all 780 pairwise inner products |
| \cite{pfender2004kissing} | 2004 | Survey; cap-packing folklore | 77 (cap bound, $n{=}5$) | 40 | Cap-packing bound: 77 | YES: our cap-packing bound of 77 matches the folklore bound exactly |
| \cite{pfender2007improved} | 2007 | Improved Delsarte polynomials | $\leq 45$ (for certain small $n$; for $n{=}5$ gives $\leq 46$) | -- | Our LP: $\leq 51$ | NO: Pfender's refined polynomial search is tighter |
| \cite{cohn2007universally} | 2007 | Universal optimality / sharp codes | -- | 40 (D$_5$ minimal vectors) | D$_5$ verified as 40-point configuration | YES: our D$_5$ verification is consistent |
| \cite{bachoc2008new} | 2008 | 3-point SDP bound | $\leq 45$ | -- | Our LP (without SDP): $\leq 51$ | NO: Bachoc--Vallentin's SDP exploits three-point correlations we do not capture |
| \cite{musin2008kissing} | 2008 | LP + geometric arguments | (proved $\tau_4{=}24$) | -- | We use $\tau_4{=}24$ as input to degree bound D1 | INDIRECT: Musin's result is an input to our contact graph analysis |
| \cite{mittelmann2010high} | 2010 | High-accuracy SDP | $\leq 44$ | -- | Our LP: $\leq 51$; enhanced LP with D1--D3: $\leq 51$ | NO: Mittelmann--Vallentin's SDP bound of 44 is far tighter |
| \cite{boyvalenkov2012survey} | 2012 | Survey of bounds | Documents $\leq 44$ | Documents $\geq 40$ | Consistent with our findings | YES: our summary of the state of the art matches their survey |
| \cite{machado2018improving} | 2018 | Symmetry-exploiting SDP | $\leq 44$ (confirms) | -- | Our LP: $\leq 51$ | NO: Machado--de Oliveira Filho exploit polynomial symmetry in SDP; we do not |
| \cite{szollosi2023five} | 2023 | New kissing arrangement $Q_5$ | -- | 40 (third non-isometric construction) | We verify D$_5$ achieves 40; we do not construct $Q_5$ | PARTIAL: our lower bound matches but we do not explore alternative 40-point configs |
| \cite{cohn2024variations} | 2024 | Fourth 5D kissing arrangement | -- | 40 (fourth non-isometric) | We attempt (and fail) to find a 41st point | CONSISTENT: our failure to augment D$_5$ is consistent with $\tau_5 = 40$ |

**Summary.** Out of 16 papers explicitly compared, our upper bound results match prior work only for the simple cap-packing bound ($\tau_5 \leq 77$, folklore) and the D$_5$ lower bound ($\tau_5 \geq 40$). Our enhanced LP with dimensional constraints (D1--D3) achieves $\tau_5 \leq 51$, which is weaker than the standard Delsarte LP bound of $\leq 46$ \cite{odlyzko1979kissing, levenshtein1979boundaries} and far weaker than the SDP bound of $\leq 44$ \cite{mittelmann2010high}. No improvement over any prior upper bound was achieved.

---

## 2. What Is Novel in Our Approach

### 2.1 The Dimensional Analysis Framework ($V_n$ Recurrence, Pyramid Decomposition)

Our approach begins from the identity $V_n(R) = \frac{1}{n} R \cdot S_{n-1}(R)$, equivalently the derivative relation $\frac{d}{dR}[V_n(R)] = S_{n-1}(R)$, and the two-step recurrence $V_n = \frac{2\pi}{n} R^2 V_{n-2}$. We interpret these as a "pyramid decomposition" of the $n$-ball: each infinitesimal cone from the center to a surface patch $d\Omega$ has volume $\frac{1}{n} R^n d\Omega$, so the cone fills only $1/n$ of its bounding cylinder (base area times radius). For $n = 5$, this factor is $1/5$, meaning five-dimensional cones are "thinner" than their three-dimensional counterparts ($1/3$) or four-dimensional counterparts ($1/4$).

This geometric picture is not new in substance---it follows directly from polar coordinate integration---but the explicit framing as a "pyramid efficiency factor" and the systematic exploration of whether the $1/n$ thinning creates useful packing constraints appears not to have been pursued in the kissing number literature. The result, however, is negative: as we show in `results/pyramid_decomposition.md`, the $1/n$ factor cancels when comparing cone volumes to total ball volume, so the pyramid decomposition yields the same cap-packing bound ($\tau_5 \leq 77$) as the surface area argument. This cancellation is not a computational accident but a mathematical identity: both bounds reduce to $k \cdot A_{\text{cap}} \leq S_{n-1}$.

**Honest assessment.** The pyramid decomposition provides geometric intuition (visualizing how caps sit on $S^4$ as cones from the center) but does not produce a tighter bound. It is a reformulation, not an improvement.

### 2.2 The Enhanced LP with Dimensional Constraints (D1--D3)

We augmented the standard Delsarte LP polynomial search with three additional constraints motivated by dimensional analysis:

- **D1 (Equatorial Slicing):** Each vertex in the contact graph has degree at most $\tau_4 = 24$ \cite{musin2008kissing}, because its neighbors project onto $S^3$. This is a well-known observation.

- **D2 (Second-Moment Trace):** The Gram matrix $G = X^T X$ of a $k$-point configuration in $\mathbb{R}^5$ has rank at most 5, so $\operatorname{tr}(G^2) \geq k^2/5$. Combined with the diagonal bound $\operatorname{tr}(G^2) \leq k(k+3)/4$ (from inner products in $[-1, 1/2]$), this gives $k^2/5 \leq k(k+3)/4$, which is satisfied for all $k > 0$. The constraint is vacuous for $n \geq 4$.

- **D3 (Volume Recurrence Consistency):** The recurrence $V_n = \frac{2\pi}{n} V_{n-2}$ relates cap geometry across dimensions. However, the Delsarte LP certificate is a polynomial in the dual space, not a geometric object; its Gegenbauer coefficients need not satisfy cross-dimensional consistency.

As our results in `results/enhanced_bound_results.txt` show, none of the constraints D1--D3 are binding for $n = 5$. The sensitivity analysis confirms: removing any individual constraint does not change the bound ($\tau_5 \leq 51$ with or without D1--D3).

**Honest assessment.** The dimensional constraints operate at a different level (geometric/structural) than the Delsarte LP (spectral/global). They are not strong enough to tighten the LP bound. The idea of adding geometric constraints to the LP is sound in principle, but the specific constraints we derive are either already implied by the LP or are too weak to be active. This is a negative result, but an informative one: it clarifies the boundary between what geometric arguments and what spectral methods can achieve.

### 2.3 The Refined Contact Graph Degree Bound (21 Instead of 24)

In `results/contact_graph_analysis.md`, we derive a refined upper bound on the vertex degree in the contact graph of any kissing configuration on $S^4$. The standard argument gives $d(v) \leq \tau_4 = 24$ by projecting neighbors onto the equatorial $S^3$. We observe that the projected minimum angle is $\arccos(1/3) \approx 70.53°$, not $60°$, because:

$$\langle w_1, w_2 \rangle = \frac{1}{4} + \frac{3}{4}\langle u_1, u_2 \rangle \leq \frac{1}{2} \implies \langle u_1, u_2 \rangle \leq \frac{1}{3}$$

Applying the cap-packing bound on $S^3$ with half-angle $\frac{1}{2}\arccos(1/3) \approx 35.26°$ gives $d(v) \leq 21$. This is tighter than the naive bound of 24.

**Honest assessment.** This projection argument is elementary and may well appear in the literature, possibly in the work of Boyvalenkov, Dodunekov, and Musin \cite{boyvalenkov2012survey} or in unpublished analyses of the five-dimensional kissing problem. The key observation that the projected angle is $\arccos(1/3)$ rather than $\arccos(1/2)$ follows from a straightforward computation. We have not found an explicit statement of $d(v) \leq 21$ for $n = 5$ in the papers we surveyed, but this may reflect incomplete coverage of the literature rather than genuine novelty. Moreover, the bound $d(v) \leq 21$ does not by itself rule out any value of $\tau_5$ in $\{41, \ldots, 44\}$, since any graph on 44 vertices can easily accommodate maximum degree 21.

### 2.4 The Explicit Local Rigidity Proof for D$_5$ ($\sqrt{2/5}$ Gap)

We prove that for any unit vector $x \in \mathbb{R}^5$, the maximum inner product with the D$_5$ configuration satisfies:

$$\max_{w \in D_5} \langle x, w \rangle \geq \sqrt{2/5} = 0.632456\ldots$$

This minimum is attained uniquely (up to sign permutations) at the "democratic" direction $x = \pm(1, 1, 1, 1, 1)/\sqrt{5}$, where exactly 10 D$_5$ vectors achieve the maximum. Since $\sqrt{2/5} > 1/2$, no 41st point can be added to the D$_5$ configuration. The angular gap is $\arccos(1/2) - \arccos(\sqrt{2/5}) \approx 9.23°$.

The proof uses Lagrange multipliers on the optimization problem $\min_{x \in S^4} \max_{i<j} (|x_i| + |x_j|)/\sqrt{2}$, which has a clean closed-form solution.

**Honest assessment.** This appears to be a clean and self-contained presentation that we have not found stated explicitly in the literature. The fact that D$_5$ cannot be augmented is well known and follows from more general results (the covering radius of the D$_5$ root system is well understood; see \cite{conway1999sphere}). Our contribution is the explicit, elementary proof with the closed-form extremal direction $x = (1,\ldots,1)/\sqrt{5}$ and the precise gap $\sqrt{2/5} - 1/2 \approx 0.1325$. This is pedagogically useful but not a research breakthrough. We also verified this result with 100,000 Monte Carlo samples on $S^4$, none of which achieved $\max \langle x, w \rangle < 0.5$.

### 2.5 Summary of Novelty Assessment

| Claimed Result | Genuinely Novel? | Prior Work |
|---------------|-----------------|------------|
| Cap-packing bound ($\tau_5 \leq 77$) | No | Folklore; \cite{pfender2004kissing} |
| Pyramid decomposition ($1/n$ factor) | Reformulation only | Standard polar coordinates |
| Enhanced LP with D1--D3 ($\tau_5 \leq 51$) | Negative result is informative | LP framework from \cite{delsarte1973algebraic}; constraints are redundant |
| Degree bound $d(v) \leq 21$ | Possibly novel presentation | Projection argument is elementary; may exist in literature |
| D$_5$ local rigidity ($\sqrt{2/5}$ gap) | Clean presentation, likely novel in this form | D$_5$ covering radius known; \cite{conway1999sphere} |
| D$_5$ verification (40 points) | Verification, not novel | \cite{conway1999sphere, cohn2007universally, szollosi2023five} |

**Most of these are reformulations, not improvements.** The dimensional analysis framework provides geometric insight into why caps pack the way they do on $S^4$, and the pyramid decomposition gives an appealing visual picture of the $1/n$ efficiency factor. But no bound in this work improves upon what was already known. The gap $40 \leq \tau_5 \leq 44$ remains exactly as it was before we began.

---

## 3. Comparison of Derivations

For each result that matches or parallels a prior result, we provide a detailed comparison of whether our derivation differs from existing work.

### 3.1 Cap-Packing Bound ($\tau_5 \leq 77$): Standard, Matches Folklore

The cap-packing bound computes $\lfloor S_4(1) / A_{\text{cap}}(5, \pi/6) \rfloor = \lfloor 26.319 / 0.338 \rfloor = 77$. This is the simplest possible bound: non-overlapping caps of half-angle $\pi/6$ on $S^4$ cannot cover more than the total surface area. The bound appears (sometimes without proof) in survey articles such as \cite{pfender2004kissing} and is mentioned as a starting point in \cite{boyvalenkov2012survey}.

**Our derivation.** We compute $A_{\text{cap}}(5, \pi/6)$ using the regularized incomplete beta function $I_x(a, b)$ with $x = \sin^2(\pi/6) = 1/4$, $a = 2$, $b = 3/2$. The numerical value $0.3384803298$ is verified against numerical integration of the surface area element on $S^4$. The derivation is standard; the only difference is that we explicitly connect it to the pyramid volume formula $V_{\text{cone}} = \frac{1}{5} A_{\text{cap}}$, which provides geometric context but does not change the bound.

**Verdict:** Our derivation is not genuinely different. The pyramid reformulation is aesthetically distinct but mathematically equivalent.

### 3.2 Delsarte LP (Our $\sim$51 vs. Optimal $\sim$46): Our Polynomial Search Is Suboptimal

The Delsarte LP bound \cite{delsarte1973algebraic, delsarte1977spherical} for $\tau_5$ is obtained by optimizing over polynomials $f(t)$ satisfying: (i) $f(t) \leq 0$ for $t \in [-1, 1/2]$, (ii) Gegenbauer coefficients $\hat{f}(k) \geq 0$ for $k \geq 1$, and (iii) maximize $f(1)/f(0)$. The optimal polynomial for $n = 5$ gives $\tau_5 \leq 46.3$ \cite{odlyzko1979kissing}. With further refinement by Pfender \cite{pfender2007improved}, one obtains $\tau_5 \leq 46$.

**Our implementation.** We search over a family of degree-6 polynomial ansatzes of the form $(t+1)(t-0.5)(t-r_1)^2(t-r_2)^2$ with roots on a grid. Our best polynomial $(t+1)(t+0.5)^2 t^2 (t-0.5)$ gives $f(1)/f(0) = 51.08$, yielding $\tau_5 \leq 51$. This is substantially worse than the optimal LP bound of 46 because our polynomial family does not include the optimal Gegenbauer combination. A proper implementation using CVXPY or a semi-infinite LP solver with sufficiently many discretization points would recover the optimal bound. We did not pursue this because the optimal LP bound of 46 is already documented in the literature and the SDP bound of 44 \cite{mittelmann2010high} supersedes it.

**Verdict:** Our derivation uses the same framework but with a weaker polynomial search. The result is strictly inferior to \cite{odlyzko1979kissing}. We were transparent about this in `results/enhanced_bound_results.txt`.

### 3.3 Enhanced Bound (51 with D1--D3): Dimensional Constraints Are Redundant

The enhanced Delsarte LP augments the standard LP with three constraints: D1 (contact graph degree $\leq 24$), D2 (Gram matrix trace bound), and D3 (volume recurrence consistency). As documented in `results/enhanced_bound_results.txt`, the sensitivity analysis shows:

- **D1 is not active:** For $k = 51$ and max degree 24, the constraint $|E| \leq k \cdot 24/2 = 612$ is easily satisfied. Even for the true bound $k = 44$, max degree $\leq 24$ is not binding.
- **D2 is vacuous:** The trace constraint $k^2/n \leq \operatorname{tr}(G^2) \leq k(k+3)/4$ is satisfied for all positive $k$ when $n \geq 4$.
- **D3 does not restrict the LP:** The volume recurrence relates geometric cap areas across dimensions, but the LP certificate polynomial is not a cap indicator function. Its Gegenbauer coefficients are not required to satisfy cross-dimensional consistency.

**Comparison with Bachoc--Vallentin \cite{bachoc2008new}.** Their SDP approach extends the Delsarte LP by constraining three-point correlations, which is fundamentally different from our dimensional constraints. The SDP enforces positive semidefiniteness of a matrix-valued function of triple inner products $(t_1, t_2, t_3)$. This captures geometric constraints that the Delsarte LP misses entirely. Our dimensional constraints D1--D3, by contrast, are essentially structural constraints on the contact graph and the Gram matrix rank---information that the LP already implicitly encodes (or that is too weak to be useful). The gap between our approach and the SDP approach is not a matter of implementation quality but of the fundamental power of the constraints.

**Verdict:** The dimensional constraints are genuinely different from the SDP constraints of \cite{bachoc2008new}, but they are strictly weaker. They represent a different direction of generalization from the Delsarte LP, one that turns out to be a dead end for improving the $\tau_5$ bound.

### 3.4 D$_5$ Verification (40 Points): Matches Known Construction

The D$_5$ lattice minimal vectors are all permutations of $(\pm 1, \pm 1, 0, 0, 0)/\sqrt{2}$, giving $\binom{5}{2} \times 2^2 = 40$ vectors. This construction is classical and appears in \cite{conway1999sphere}, with the contact graph structure analyzed in numerous subsequent works.

**Our verification.** We generate all 40 vectors, compute all $\binom{40}{2} = 780$ pairwise inner products, and confirm: (i) all inner products lie in $\{-1, -1/2, 0, +1/2\}$, (ii) no inner product exceeds $1/2$ in absolute value (for non-antipodal pairs), (iii) the contact graph (edges at inner product $+1/2$) is 12-regular with 240 edges. We also compute graph-theoretic invariants: clique number $\omega = 4$, independence number $\alpha = 8$, chromatic number $\chi = 5$.

**Comparison with \cite{szollosi2023five} and \cite{cohn2024variations}.** These papers go beyond D$_5$ by constructing non-isometric 40-point kissing configurations ($Q_5$ and a fourth configuration). Our work does not explore these alternative constructions; we focus exclusively on D$_5$.

**Verdict:** Our verification is routine and consistent with prior work. It adds no new information about the lower bound.

### 3.5 Local Rigidity ($\sqrt{2/5}$): Possibly Novel Presentation

Our proof that $\max_{w \in D_5} \langle x, w \rangle \geq \sqrt{2/5}$ for all unit $x$ proceeds by:

1. Writing the D$_5$ vectors as $(s_i e_i + s_j e_j)/\sqrt{2}$ for $i < j$ and $s_i, s_j \in \{+1, -1\}$.
2. Observing that $\max \langle x, w \rangle = \max_{i<j} (|x_i| + |x_j|)/\sqrt{2}$.
3. Minimizing $\max_{i<j} (|x_i| + |x_j|)/\sqrt{2}$ subject to $\sum x_i^2 = 1$ by Lagrange multipliers.
4. The minimum occurs at $|x_i| = 1/\sqrt{5}$ for all $i$, giving $(1/\sqrt{5} + 1/\sqrt{5})/\sqrt{2} = \sqrt{2/5}$.

This argument is elementary but, to our knowledge, has not been written out explicitly in the kissing number literature. The covering radius of the D$_5$ root system is computed in \cite{conway1999sphere} (Table 1.2, Chapter 4), but the connection to the impossibility of augmenting the kissing configuration by a single additional point is typically stated without the explicit closed-form proof.

**Comparison with covering radius theory.** The covering radius of a lattice $\Lambda$ is $\max_{x \in \mathbb{R}^n} \min_{v \in \Lambda} \|x - v\|$. For the D$_5$ root system (viewed as a spherical code on $S^4$), the analogous quantity is the covering radius on $S^4$: the maximum angular distance from any point on $S^4$ to the nearest code point. Our result $\sqrt{2/5}$ translates to a minimum angle of $\arccos(\sqrt{2/5}) \approx 50.77°$, which is less than $60°$. This means $S^4$ is not "covered" by caps of half-angle $60°$ centered at the D$_5$ points, confirming that D$_5$ cannot be augmented.

**Verdict:** The result itself is not new (it follows from the covering radius), but our explicit proof with the closed-form extremal direction $(1,\ldots,1)/\sqrt{5}$ and the precise inner product gap $\sqrt{2/5} - 1/2 \approx 0.1325$ appears to be a clean, self-contained presentation that may be novel in this specific form.

### 3.6 Degree Bound Refinement (21 Instead of 24): Derived from Projection Argument

The standard bound on the contact graph degree in a 5-dimensional kissing configuration is $d(v) \leq \tau_4 = 24$, from projecting neighbors of $v$ onto the equatorial $S^3$. Our refinement observes that the projected pairwise inner products satisfy $\langle u_1, u_2 \rangle \leq 1/3$ (not $\leq 1/2$), because the projection introduces a scaling factor:

$$\langle w_1, w_2 \rangle = \frac{1}{4} + \frac{3}{4}\langle u_1, u_2 \rangle \leq \frac{1}{2} \implies \langle u_1, u_2 \rangle \leq \frac{1}{3}$$

The cap-packing bound on $S^3$ with the reduced half-angle $\frac{1}{2}\arccos(1/3) \approx 35.26°$ gives $d(v) \leq \lfloor 19.739 / 0.905 \rfloor = 21$.

**Comparison with prior work.** This type of projection argument is standard in the coding theory literature. The observation that neighbors of a vertex in a kissing configuration project to a spherical code with a tighter angular constraint is well known in principle---it underlies Musin's proof of $\tau_4 = 24$ \cite{musin2008kissing}, where the projected minimum angle on $S^2$ is $\arccos(1/3) \approx 70.53°$ (not $60°$). For $n = 5$, the same argument gives the tighter degree bound of 21. Whether this specific bound has been stated explicitly in the literature is unclear; it may appear in the work of Boyvalenkov et al. \cite{boyvalenkov2012survey} or in unpublished analyses.

**Verdict:** The derivation method is not novel (it is the same projection argument used by Musin and others), but the specific application to $n = 5$ yielding $d(v) \leq 21$ may be a minor new observation. It does not, however, lead to any improvement in the bound on $\tau_5$.

---

## 4. What Our Approach Does NOT Achieve

It is important to state clearly what this work does not accomplish, to prevent any overstatement of results.

### 4.1 Does Not Improve the Upper Bound Below 44

The current best upper bound is $\tau_5 \leq 44$, established by Mittelmann and Vallentin \cite{mittelmann2010high} using high-accuracy SDP computation of the Bachoc--Vallentin three-point bound \cite{bachoc2008new}. Our enhanced LP with dimensional constraints gives $\tau_5 \leq 51$, which is 7 points weaker than the standard LP bound of $\leq 46$ and 7 points weaker still than the SDP bound of $\leq 44$. The dimensional constraints D1--D3 do not tighten the LP bound at all; the sensitivity analysis shows they are entirely redundant.

To improve below 44, one would likely need either: (a) higher-order SDP bounds using $k$-point correlations for $k \geq 4$, which are computationally intractable with current methods, (b) Viazovska-type modular form techniques \cite{viazovska2017sphere}, which are currently applicable only in dimensions 8 and 24, or (c) entirely new techniques such as flag algebras or topological methods.

### 4.2 Does Not Find a 41-Point Configuration

Despite testing over 100,000 random points, 50 nonlinear optimization runs, and 354 algebraically constructed candidates, no valid 41st point could be added to the D$_5$ configuration. The closest approach achieved a maximum inner product of $\sqrt{2/5} \approx 0.6325$, which exceeds the required threshold of $0.5$ by a margin of $0.1325$. This provides computational evidence that $\tau_5 = 40$, but it does not constitute a proof.

Importantly, our search was limited to augmenting the D$_5$ lattice configuration. It is theoretically possible that a 41-point kissing configuration exists that does not contain D$_5$ as a subconfiguration. Szollosi \cite{szollosi2023five} and Cohn--Rajagopal \cite{cohn2024variations} have shown that multiple non-isometric 40-point configurations exist, so the space of configurations is richer than the D$_5$ lattice alone. A comprehensive search for 41-point configurations from scratch (without starting from D$_5$) was not attempted and would require significantly more computational resources.

### 4.3 Does Not Prove $\tau_5 = 40$

Proving $\tau_5 = 40$ would require either: (a) improving the upper bound from 44 to 40, which is equivalent to showing that no 41-point kissing configuration exists in $\mathbb{R}^5$, or (b) finding a fundamentally new approach that bypasses the LP/SDP hierarchy. Our work makes no progress toward either goal. The gap $40 \leq \tau_5 \leq 44$ is exactly the same after our investigation as it was before.

### 4.4 The Dimensional Constraints Are Not Strong Enough to Tighten the LP Bound

This is perhaps the most important negative result of our investigation. We had hoped that the dimensional analysis framework---specifically the volume recurrence $V_n = \frac{2\pi}{n} R^2 V_{n-2}$ and the pyramid decomposition---would yield constraints that, when added to the Delsarte LP, would tighten the bound. The idea was that the cross-dimensional structure of spherical caps (relating $S^4$ cap geometry to $S^2$ and $S^3$ cap geometry) encodes information not captured by the standard LP.

In practice, all three dimensional constraints (D1, D2, D3) proved redundant:

- **D1** is a contact graph degree bound. The LP already gives $k \leq 44$ (or $k \leq 51$ in our weaker version), and any graph on 44 or 51 vertices can have maximum degree $\leq 24$ (or even $\leq 21$). The degree constraint never eliminates a feasible LP solution.

- **D2** is a Gram matrix trace bound. For $n \geq 4$, the inequality $k^2/n \leq k(k+3)/4$ is satisfied for all $k > 0$, making the constraint vacuous.

- **D3** attempts to enforce cross-dimensional consistency of Gegenbauer coefficients. But the LP certificate polynomial lives in a dual space where such consistency is not required: the polynomial is a tool for proving an upper bound, not a physical object on the sphere. Its Gegenbauer coefficients reflect the spectral structure of the LP, not the geometric structure of any particular configuration.

The fundamental issue is that the Delsarte LP and SDP methods are **spectral** (they work with the Gegenbauer expansion of the angular distribution), while our dimensional constraints are **geometric** (they work with cap volumes and contact graph structure). These two types of information live in different mathematical spaces. Bridging them would require a deeper connection between the spectral and geometric perspectives---something akin to how Viazovska's modular forms \cite{viazovska2017sphere} connect analytic number theory to sphere packing geometry, but no such bridge is currently known for the five-dimensional kissing problem.

---

## 5. Assessment of the Dimensional Analysis Framework

### 5.1 Strengths: Geometric Insight

The dimensional analysis framework provides genuine geometric insight into the kissing number problem, even though it does not yield improved bounds:

**Pyramid decomposition.** The identity $V_n = \frac{1}{n} R \cdot S_{n-1}$ decomposes the $n$-ball into infinitesimal cones, each filling $1/n$ of its bounding cylinder. This gives a vivid picture of how spherical caps on $S^{n-1}$ correspond to "thinner" and "thinner" cones as $n$ increases. The 1/5 factor for $n = 5$ means each cap-pyramid occupies only 20% of its bounding region, compared to 33% in $\mathbb{R}^3$.

**Unification of volume and surface area bounds.** The framework shows that the volume-based cap-packing bound ($k \cdot V_{\text{cone}} \leq V_n$) and the surface-area-based cap-packing bound ($k \cdot A_{\text{cap}} \leq S_{n-1}$) are mathematically identical. The $1/n$ factor cancels because both the cone volumes and the total ball volume scale with $1/n$. This resolves a potential confusion: one might think that "volume packing" and "area packing" give different bounds, but they do not.

**Cap density analysis.** The cap density $\rho_n = \tau_n \cdot A_{\text{cap}}(n, \pi/6) / S_{n-1}$ decreases monotonically across all known dimensions: $\rho_2 = 1.00$, $\rho_3 = 0.80$, $\rho_4 = 0.69$, $\rho_8 = 0.30$, $\rho_{24} = 0.002$. For $n = 5$, $\rho_5(40) = 0.51$ and $\rho_5(44) = 0.57$, both within the expected range. The exponential decrease of cap density is a manifestation of the "curse of dimensionality" in sphere packing.

### 5.2 Limitations: Does Not Capture Pairwise Angular Constraints

The central limitation of the dimensional analysis framework is that it operates on **individual caps**, not on the **global angular distribution** of the configuration. The cap-packing bound says: "the total cap area cannot exceed the sphere's surface area." This is a constraint on the sum of individual cap areas. It does not incorporate any information about how caps relate to each other.

The Delsarte LP, by contrast, constrains the **angular distribution** of all $\binom{k}{2}$ pairwise inner products simultaneously. The LP condition $f(t) \leq 0$ for $t \in [-1, 1/2]$, combined with the Gegenbauer coefficient positivity $\hat{f}(k) \geq 0$, encodes a global constraint on the distribution of pairwise angles. This is why the LP can prove $\tau_5 \leq 46$ while the cap-packing bound gives only $\tau_5 \leq 77$: the LP exploits pairwise correlations that the geometric bound ignores.

The SDP of Bachoc--Vallentin \cite{bachoc2008new} goes further by constraining **three-point** correlations (the joint distribution of angles in triples of points), which is why the SDP can improve the bound from 46 to 45 (and then to 44 with high-accuracy numerics \cite{mittelmann2010high}). Each step up the hierarchy---from cap packing (1-point) to Delsarte LP (2-point, via polynomial positivity) to SDP (3-point)---captures more structural information about the configuration and yields tighter bounds.

**The main limitation: dimensional analysis operates on individual caps, not on the global angular distribution.** The $V_n$ recurrence and the pyramid decomposition relate the geometry of individual caps to the geometry of the ambient sphere, but they say nothing about how multiple caps interact. To close the gap $40 \leq \tau_5 \leq 44$, one needs methods that capture the full structure of the point configuration on $S^4$---its inner product spectrum, its Gram matrix rank, its association scheme structure. The dimensional analysis framework, for all its geometric elegance, does not reach this level of structural analysis.

### 5.3 Could the Framework Be Strengthened?

One might ask whether there is a way to extend the dimensional analysis framework to capture pairwise or higher-order constraints. Several possibilities present themselves:

1. **Cross-cap interaction volumes.** If two caps on $S^4$ are separated by angle $\theta < \pi/3 + 2 \cdot \pi/6 = 2\pi/3$, their "interaction region" (the set of points within angular distance $\pi/6$ of both cap centers) is non-empty. The volume of this interaction region could provide pairwise constraints. However, this is essentially equivalent to computing the intersection of two spherical caps, which leads back to the Delsarte LP framework (the LP encodes this information spectrally via Gegenbauer polynomials).

2. **Dimensional projection constraints.** Projecting the configuration onto lower-dimensional subspaces (from $\mathbb{R}^5$ to $\mathbb{R}^4$ or $\mathbb{R}^3$) could yield constraints from the known kissing numbers $\tau_3 = 12$ and $\tau_4 = 24$. Our D1 constraint (degree bound from $\tau_4$) is one instance of this, but it is too weak. A more sophisticated version might project the entire configuration (not just the neighbors of a single vertex) and derive global constraints.

3. **Harmonic analysis on the dimensional recurrence.** The recurrence $V_n = \frac{2\pi}{n} V_{n-2}$ links Gegenbauer polynomials across dimensions. If one could show that the optimal Delsarte polynomial for $n = 5$ must be "compatible" with the optimal polynomials for $n = 3$ and $n = 4$ in some precise sense, this could yield new constraints. However, our investigation (D3) found that the LP certificate polynomial is not required to satisfy such compatibility.

None of these extensions appear promising enough to close the gap, but they represent directions for future investigation.

---

## 6. Conclusions

This comparison reveals that our dimensional analysis approach to the kissing number problem in dimension 5, while geometrically motivated and internally consistent, does not produce any improvement over prior bounds. The current state of the art---$40 \leq \tau_5 \leq 44$, with the lower bound from the D$_5$ lattice \cite{conway1999sphere} and the upper bound from high-accuracy SDP \cite{mittelmann2010high}---remains unchanged.

The value of this investigation lies primarily in:

1. **Clarifying the boundary** between geometric (dimensional) methods and spectral (LP/SDP) methods for bounding kissing numbers.
2. **Demonstrating concretely** that the $V_n$ recurrence and pyramid decomposition, despite their intuitive appeal, produce bounds that are mathematically equivalent to the simple cap-packing argument.
3. **Providing a clean presentation** of the D$_5$ local rigidity result ($\sqrt{2/5}$ gap) and the refined degree bound ($d(v) \leq 21$).
4. **Documenting a negative result** honestly: the dimensional constraints D1--D3 are redundant, and the gap between 77 (cap packing) and 44 (SDP) cannot be bridged by the type of geometric constraints we consider.

The kissing number problem in dimension 5 remains one of the most tantalizing open problems in discrete geometry. Closing the gap will likely require techniques that go beyond both the dimensional analysis framework explored here and the current LP/SDP hierarchy---perhaps modular forms in the spirit of Viazovska \cite{viazovska2017sphere}, or new algebraic structures that encode the combinatorics of spherical codes in $\mathbb{R}^5$.

---

## References

All citations refer to entries in `sources.bib`:

- \cite{delsarte1973algebraic} -- Delsarte, P. (1973). LP framework for coding theory.
- \cite{delsarte1977spherical} -- Delsarte, P., Goethals, J.-M., Seidel, J. J. (1977). Spherical codes and designs.
- \cite{kabatyansky1978bounds} -- Kabatyansky, G. A., Levenshtein, V. I. (1978). Asymptotic packing bounds.
- \cite{odlyzko1979kissing} -- Odlyzko, A. M., Sloane, N. J. A. (1979). Delsarte LP bound for kissing numbers.
- \cite{levenshtein1979boundaries} -- Levenshtein, V. I. (1979). Packings in Euclidean space.
- \cite{conway1999sphere} -- Conway, J. H., Sloane, N. J. A. (1999). Sphere Packings, Lattices and Groups.
- \cite{pfender2004kissing} -- Pfender, F., Ziegler, G. M. (2004). Kissing numbers survey.
- \cite{pfender2007improved} -- Pfender, F. (2007). Improved Delsarte bounds.
- \cite{cohn2007universally} -- Cohn, H., Kumar, A. (2007). Universally optimal distributions.
- \cite{musin2008kissing} -- Musin, O. R. (2008). Kissing number in four dimensions.
- \cite{bachoc2008new} -- Bachoc, C., Vallentin, F. (2008). SDP bounds for kissing numbers.
- \cite{zong2008kissing} -- Zong, C. (2008). Kissing number, blocking number and covering number.
- \cite{mittelmann2010high} -- Mittelmann, H. D., Vallentin, F. (2010). High-accuracy SDP bounds.
- \cite{boyvalenkov2012survey} -- Boyvalenkov, P., Dodunekov, S., Musin, O. R. (2012). Survey on kissing numbers.
- \cite{machado2018improving} -- Machado, F. C., de Oliveira Filho, F. M. (2018). Symmetry-exploiting SDP.
- \cite{szollosi2023five} -- Szollosi, F. (2023). Five-dimensional kissing arrangements.
- \cite{cohn2024variations} -- Cohn, H., Rajagopal, A. (2024). Variations on five-dimensional sphere packings.
- \cite{viazovska2017sphere} -- Viazovska, M. S. (2017). Sphere packing in dimension 8.
- \cite{cohn2003new} -- Cohn, H., Elkies, N. (2003). New upper bounds on sphere packings.
- \cite{schutte1953problem} -- Schutte, K., van der Waerden, B. L. (1953). The problem of thirteen spheres.
