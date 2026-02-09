# Bounded Continued Fraction Case: Non-Quadratic Irrationals with Bounded Partial Quotients

## 1. Background

**Definition.** A real number $\alpha$ is *badly approximable* if there exists $c > 0$ such that $|\alpha - p/q| > c/q^2$ for all rationals $p/q$. Equivalently, $\alpha$ has *bounded partial quotients* in its continued fraction expansion: $\alpha = [a_0; a_1, a_2, \ldots]$ with $\sup_i a_i < \infty$.

**Key fact (Lagrange's Theorem).** A real number has an eventually periodic continued fraction expansion if and only if it is a quadratic irrational.

Thus:
- **Quadratic irrationals** → bounded CF (eventually periodic) → morphic Sturmian word
- **Non-quadratic with bounded CF** → bounded but NOT eventually periodic → non-morphic Sturmian word
- **General irrationals** → unbounded CF (e.g., $e = [2; 1,2,1,1,4,1,1,6,\ldots]$)

The question: do non-quadratic irrationals with bounded CF behave like quadratic irrationals (allowing C-finite subsequences) or like transcendentals (blocking them)?

## 2. Analysis: The Morphic Discriminator

**Theorem (Allouche-Shallit 2003).** The Sturmian word $s_n = \lfloor (n+1)\alpha \rfloor - \lfloor n\alpha \rfloor$ is morphic (fixed point of a substitution followed by a coding) if and only if $\alpha$ is a quadratic irrational [AlloucheShallit2003].

**Consequence for our problem:**
- For quadratic $\alpha$: the Sturmian word is morphic, the Ostrowski representation is automatic, and the Wythoff-type array produces C-finite subsequences.
- For non-quadratic $\alpha$ (even with bounded CF): the Sturmian word is NOT morphic, and the Ostrowski-automatic framework does not apply in the same way.

However, the morphic property governs the *Sturmian word* (first differences), not directly the Beatty sequence values. The C-finite subsequences we construct (Wythoff rows) depend on the algebraic structure of $r$ (its minimal polynomial), not just the combinatorial structure of the Sturmian word.

## 3. The Key Distinction

For the Wythoff-type construction to work, we need:
1. $r$ satisfies a polynomial equation $r^2 = pr + q$ (or higher degree analog)
2. The companion Beatty sequence $s = r/(r-1)$ is algebraically related to $r$
3. The rows of the generalized Wythoff array satisfy a recurrence with *integer* (or rational) coefficients

**For algebraic irrationals of any degree:** Conditions 1-3 are satisfied. Fraenkel (1994) showed that for algebraic $\alpha$ of degree $d$, iterated floor functions satisfy identities involving the conjugates of $\alpha$, enabling constructions of C-finite subsequences.

**For transcendental irrationals (including those with bounded CF):** $r$ does not satisfy any polynomial equation with rational coefficients. The Wythoff-type construction fails because the recurrence coefficients would be transcendental, not rational. And as proved in the only_if_direction (Case 1), any C-finite subsequence forces $r$ to be algebraic.

## 4. Computational Experiments

We test specific badly approximable numbers that are transcendental (or believed to be).

### Example 1: $e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, \ldots]$
The number $e$ has unbounded CF (the partial quotients grow as $2, 4, 6, 8, \ldots$ at positions $2, 5, 8, 11, \ldots$). So $e$ is NOT badly approximable. However, the CF is still highly structured.

**Prediction:** No C-finite subsequence exists (since $e$ is transcendental).
**Experimental result:** Confirmed — no non-trivial recurrences found (see Phase 4 experiments).

### Example 2: Badly approximable transcendental with bounded CF
Constructing explicit badly approximable transcendentals with bounded CF is possible but the numbers are not "named" constants. By Jarnik's theorem, the set of badly approximable numbers has Lebesgue measure 0 but Hausdorff dimension 1.

One explicit construction: take the continued fraction $\alpha = [1; 2, 1, 2, 1, 2, \ldots, 1, 2, 3, 1, 2, 1, 2, \ldots]$ where we insert a single 3 at position $N$ for very large $N$. This is badly approximable (partial quotients bounded by 3) but NOT eventually periodic (hence not quadratic irrational if $N$ is chosen to break periodicity). However, such $\alpha$ could be algebraic — determining transcendence is hard.

A more rigorous approach: the set of badly approximable transcendentals is known to be uncountable (it has Hausdorff dimension 1, while algebraic numbers are countable). So "most" badly approximable numbers are transcendental.

**For ANY transcendental badly approximable number:** Our theorem (only_if direction, Case 1) proves no C-finite Beatty subsequence exists. The bounded CF property is irrelevant — what matters is algebraic vs. transcendental.

### Example 3: $\sum_{k=0}^{\infty} 2^{-a_k}$ (Badly approximable Liouville-type)
Specific constructions of badly approximable transcendentals exist via the theory of normal numbers and CF expansions. For all such numbers, our theorem applies.

## 5. Theorem: Bounded CF Does Not Help Transcendentals

**Theorem.** Let $\alpha$ be a transcendental irrational with bounded partial quotients. Then $(\lfloor n\alpha \rfloor)_{n \geq 1}$ contains no infinite homogeneous C-finite subsequence.

*Proof.* By the unconditional theorem for transcendentals (proofs/only_if_direction.md, Case 1): any C-finite subsequence forces $\alpha \in \overline{\mathbb{Q}}$, contradicting transcendence. The bounded CF condition plays no role in the proof. $\square$

## 6. The True Discriminator

The analysis reveals that the key discriminator is **algebraicity vs. transcendence**, not the CF structure:

| Property | Quadratic irrational | Non-quadratic algebraic | Transcendental (bounded CF) | Transcendental (unbounded CF) |
|---|---|---|---|---|
| CF eventually periodic | YES | NO | NO | NO |
| CF bounded | YES | Possible | YES (by hypothesis) | NO |
| Sturmian word morphic | YES | NO | NO | NO |
| C-finite Beatty subseq | **YES** | **YES** (Ballot/Fraenkel) | **NO** | **NO** |

The morphic property of the Sturmian word (which correlates with quadratic irrationals) is a **sufficient** but not **necessary** condition for C-finite subsequences. The Wythoff/iterated-composition constructions work for all algebraic irrationals, including non-morphic ones, because they use the algebraic (not combinatorial) structure of $r$.

## 7. Connection to Allouche-Shallit 2003

The result in [AlloucheShallit2003] that Sturmian words are morphic iff the slope is quadratic irrational is about the *symbolic dynamics* of the first-difference sequence. This is relevant but not decisive for our question, because:

1. C-finite subsequences of $\lfloor nr \rfloor$ involve the VALUES of the Beatty sequence, not just the pattern of first differences.
2. The morphic property gives access to automatic/decidable tools (Walnut, Ostrowski automata), but the algebraic constructions (Wythoff arrays, Fraenkel identities) work more broadly.
3. The true obstruction to C-finite subsequences for transcendentals is the *algebraic irrationality* of $r$ — which is independent of CF boundedness.

## References

- [AlloucheShallit2003] Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences*. Cambridge UP.
- [Ballot2017] Ballot, C. (2017). "On Functions Expressible as Words on a Pair of Beatty Sequences." JIS 20.
- [Fraenkel1994] Fraenkel, A.S. (1994). "Iterated Floor Function, Algebraic Numbers, Discrete Chaos." Trans. AMS 341.
- [Cassaigne2001] Cassaigne, J. (2001). "Recurrence in Infinite Words." STACS 2001.
- [Lagrange1770] Lagrange, J.L. (1770). "Additions to Euler's Elements of Algebra."
