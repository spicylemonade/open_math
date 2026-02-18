# Sturmian Words and Beatty Sequences: Linear Recurrence in the Symbolic and Number-Theoretic Settings

## Item 004 — Phase 1: Problem Analysis & Literature Review

---

## 1. The First-Difference Sequence and Sturmian Words

### 1.1 Setup

Recall from the problem formalization (Item 001) that for $r > 0$, the Beatty sequence is $b_r(n) = \lfloor nr \rfloor$ and the first-difference sequence is

$$\Delta_r(n) = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor, \quad n \geq 1.$$

We view $\Delta_r$ as an infinite word over a finite alphabet. The fundamental connection is:

> **The sequence $\Delta_r$ is a Sturmian word if and only if $r$ is irrational.**

We now prove this precisely.

### 1.2 Proof that $\Delta_r$ is Sturmian if and only if $r$ is Irrational

**Definition (Sturmian word).** An infinite word $\mathbf{s} = s_1 s_2 s_3 \cdots$ over a finite alphabet is *Sturmian* if its subword complexity function satisfies $p_{\mathbf{s}}(n) = n + 1$ for all $n \geq 1$, where $p_{\mathbf{s}}(n)$ counts the number of distinct factors (contiguous subwords) of length $n$ appearing in $\mathbf{s}$. This is the minimal complexity for a non-eventually-periodic sequence, by the Morse--Hedlund theorem \cite{morse1938symbolic, morse1940symbolic2}.

**Theorem 1.1.** *The first-difference sequence $\Delta_r$ is Sturmian if and only if $r$ is irrational.*

**Proof.**

**(A) $\Delta_r$ takes exactly two values when $r$ is irrational.**

For any real $r > 0$ and integer $n \geq 1$, we have

$$\Delta_r(n) = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor.$$

Write $nr = \lfloor nr \rfloor + \{nr\}$, where $\{x\}$ denotes the fractional part. Then:

$$\Delta_r(n) = \lfloor nr + r \rfloor - \lfloor nr \rfloor = \lfloor \lfloor nr \rfloor + \{nr\} + r \rfloor - \lfloor nr \rfloor = \lfloor \{nr\} + r \rfloor.$$

Since $0 \leq \{nr\} < 1$, we have $r \leq \{nr\} + r < r + 1$, so

$$\lfloor \{nr\} + r \rfloor \in \{\lfloor r \rfloor, \lfloor r \rfloor + 1\} = \{\lfloor r \rfloor, \lceil r \rceil\}.$$

(When $r$ is not an integer, $\lceil r \rceil = \lfloor r \rfloor + 1$; when $r$ is a positive integer, both values coincide, but then $\Delta_r(n) = r$ for all $n$, which is constant.)

More precisely, $\Delta_r(n) = \lceil r \rceil$ if and only if $\{nr\} + r \geq \lfloor r \rfloor + 1$, i.e., $\{nr\} \geq 1 - \{r\}$ (where $\{r\}$ is the fractional part of $r$). When $r$ is irrational, $\{r\} \neq 0$, and the sequence $\{nr\}$ is equidistributed modulo 1 (by Weyl's theorem), so both values $\lfloor r \rfloor$ and $\lceil r \rceil$ occur with positive frequency. Thus $\Delta_r$ is a binary sequence over the alphabet $\{\lfloor r \rfloor, \lceil r \rceil\}$.

**(B) The complexity function $p(n) = n + 1$ when $r$ is irrational.**

The key observation is that $\Delta_r$ is a *mechanical word* (also called a *rotation sequence*). Specifically, $\Delta_r(n) = \lceil r \rceil$ iff $\{nr\}$ falls in the interval $[1 - \{r\}, 1)$, and $\Delta_r(n) = \lfloor r \rfloor$ otherwise. By the classical theory of Sturmian sequences (see \cite{morse1940symbolic2}, \cite{coven1973sequences}, \cite{allouche2003automatic} Chapter 2):

A binary sequence defined by the partition of the circle $\mathbb{R}/\mathbb{Z}$ by an irrational rotation $T_\alpha : x \mapsto x + \alpha \pmod{1}$ has subword complexity exactly $p(n) = n + 1$. Here $\alpha = r \bmod 1 = \{r\}$, and the partition is $[0, 1-\alpha) \cup [1-\alpha, 1)$.

The proof proceeds by induction on $n$. For $n = 1$, there are exactly 2 factors (the two letters), so $p(1) = 2 = 1 + 1$. For general $n$, the $n$ points $\{r\}, \{2r\}, \ldots, \{nr\}$ divide the circle into $n$ arcs (by irrationality, all points are distinct). Each factor of length $n$ corresponds to a coding of an arc, and the $n$ division points create exactly $n + 1$ distinct codings. This is a consequence of the three-distance theorem applied to the coding structure (see also Item 005).

Therefore $p_{\Delta_r}(n) = n + 1$ for all $n \geq 1$, so $\Delta_r$ is Sturmian.

**(C) $\Delta_r$ is NOT Sturmian when $r$ is rational.**

If $r = p/q$ in lowest terms (with $q \geq 1$), then:

$$\Delta_r(n) = \lfloor (n+1)p/q \rfloor - \lfloor np/q \rfloor.$$

The fractional parts $\{np/q\}$ cycle with period $q$ (since $\{(n+q)p/q\} = \{np/q + p\} = \{np/q\}$). Therefore $\Delta_r$ is a purely periodic sequence with period $q$.

A periodic sequence with period $q$ has complexity $p(n) \leq q$ for all $n$. In particular, for $n \geq q$, we have $p(n) = q < n + 1$ (when $q \geq 2$). By the Morse--Hedlund theorem, a sequence with $p(n) \leq n$ for some $n$ is eventually periodic. Since $\Delta_r$ is actually periodic, it satisfies $p(n) \leq q$ for all $n$, and thus is not Sturmian (which requires $p(n) = n + 1$ for all $n$).

If $r$ is a positive integer ($q = 1$), then $\Delta_r(n) = r$ for all $n$, so the sequence is constant with $p(n) = 1$ for all $n$, which is trivially not Sturmian.

$\blacksquare$

---

## 2. Durand's Theorem: Linear Recurrence in the Sturmian Setting

### 2.1 Statement

We now address when a Sturmian word is *linearly recurrent* in the combinatorics-on-words sense. This notion is fundamentally different from the integer sequence $\lfloor nr \rfloor$ satisfying an algebraic linear recurrence (see Section 4 below), and the distinction is critical for this research project.

**Definition (Recurrence function).** For an infinite word $\mathbf{s}$, the *recurrence function* $R_{\mathbf{s}}(n)$ is defined as the smallest integer $R$ such that every factor of $\mathbf{s}$ of length $R$ contains every factor of $\mathbf{s}$ of length $n$ as a subfactor. Equivalently, $R_{\mathbf{s}}(n)$ is the supremum, over all factors $w$ of length $n$, of the maximum gap between consecutive occurrences of $w$ in $\mathbf{s}$.

**Definition (Linearly recurrent word).** An infinite word $\mathbf{s}$ is *linearly recurrent* if there exists a constant $C > 0$ such that $R_{\mathbf{s}}(n) \leq Cn$ for all $n \geq 1$.

**Theorem 2.1 (Durand's Characterization).** *Let $\mathbf{s}$ be a Sturmian word with slope $\alpha$ (where $\alpha$ is the frequency of one letter, equivalently $\alpha = \{r\}$ for the first-difference sequence $\Delta_r$). Then $\mathbf{s}$ is linearly recurrent if and only if the partial quotients in the continued fraction expansion $\alpha = [0; a_1, a_2, a_3, \ldots]$ are bounded, i.e., $\sup_k a_k < \infty$.*

### 2.2 Proof Sketch

The proof combines results from Durand \cite{durand1998characterization, durand2003linearly} and Cassaigne \cite{cassaigne1999limit, cassaigne2001recurrence}.

**Step 1: S-adic representation of Sturmian words.**

Every Sturmian word with slope $\alpha = [0; a_1, a_2, \ldots]$ can be generated by a directive sequence of substitutions. Specifically, define substitutions $\sigma_0$ and $\sigma_1$ on $\{0, 1\}$ by:

$$\sigma_0: 0 \mapsto 0, \; 1 \mapsto 10; \qquad \sigma_1: 0 \mapsto 01, \; 1 \mapsto 1.$$

Then the Sturmian word with slope $\alpha = [0; a_1, a_2, \ldots]$ is the limit of

$$\sigma_0^{a_1} \circ \sigma_1^{a_2} \circ \sigma_0^{a_3} \circ \cdots$$

applied to the letter $0$ (or $1$, depending on the intercept). This is the *S-adic representation* of the Sturmian word, where the "S" stands for the finite set of substitutions $\{\sigma_0, \sigma_1\}$.

**Step 2: Bounded partial quotients imply primitive S-adic representation.**

If $\sup_k a_k \leq M$, then the directive sequence uses at most $2M$ distinct substitution morphisms (namely $\sigma_0^j$ and $\sigma_1^j$ for $1 \leq j \leq M$). By a theorem of Durand \cite{durand1998characterization}, any S-adic word generated by a primitive directive sequence over a finite set of substitutions is linearly recurrent.

The key technical point is *primitivity*: we need that products of consecutive substitution matrices are strictly positive. For Sturmian words, this follows from the fact that alternating applications of $\sigma_0$ and $\sigma_1$ (with positive exponents) produce matrices with all entries positive after at most two consecutive steps.

**Step 3: Bounded partial quotients are necessary.**

Conversely, suppose the partial quotients are unbounded: $\sup_k a_k = \infty$. Then there exist arbitrarily large partial quotients $a_{k_j} \to \infty$. At the $k_j$-th step of the continued fraction algorithm, the Sturmian word contains long runs of one letter (roughly $a_{k_j}$ consecutive copies). These long runs create factors of moderate length $n$ whose gaps between consecutive occurrences grow faster than linearly.

More precisely, Cassaigne \cite{cassaigne1999limit} showed that the *recurrence quotient* $\limsup_{n \to \infty} R(n)/n$ of a Sturmian word with slope $\alpha = [0; a_1, a_2, \ldots]$ satisfies:

$$\limsup_{n \to \infty} \frac{R_{\mathbf{s}}(n)}{n} = \limsup_{k \to \infty} (a_k + 2 + 1/q_{k-1}),$$

where $q_k$ are the denominators of the convergents $p_k/q_k$ to $\alpha$. In particular:

- If $\sup_k a_k = M < \infty$, then $\limsup R(n)/n \leq M + 2 + 1 < \infty$, so $\mathbf{s}$ is linearly recurrent with constant $C = M + 3$.
- If $\sup_k a_k = \infty$, then $\limsup R(n)/n = \infty$, so $\mathbf{s}$ is NOT linearly recurrent.

This completes the characterization. $\blacksquare$

### 2.3 References for this section

- Durand \cite{durand1998characterization}: introduced the connection between S-adic representations and return words, proving that primitive S-adic sequences are linearly recurrent.
- Durand \cite{durand2003linearly}: proved that linearly recurrent subshifts have finitely many non-periodic factors, and further developed the characterization.
- Cassaigne \cite{cassaigne1999limit}: computed the exact recurrence quotient for Sturmian sequences in terms of continued fraction partial quotients.
- Cassaigne \cite{cassaigne2001recurrence}: survey of recurrence properties in infinite words.

---

## 3. Connection to Lagrange's Theorem

### 3.1 Lagrange's Theorem on Continued Fractions

**Theorem 3.1 (Lagrange, 1770).** *A real number $\alpha$ has an eventually periodic continued fraction expansion if and only if $\alpha$ is a quadratic irrational, i.e., $\alpha$ is a root of an irreducible polynomial $ax^2 + bx + c \in \mathbb{Z}[x]$ with $a \neq 0$ and discriminant $b^2 - 4ac > 0$ (not a perfect square).*

See \cite{lagrange1770continued} for the original and \cite{allouche2003automatic} Section 9.1 for a modern treatment.

### 3.2 The Equivalence

**Corollary 3.2.** *The partial quotients of $\alpha$ are bounded (i.e., $\sup_k a_k < \infty$) if and only if $\alpha$ is a quadratic irrational.*

**Proof.** If $\alpha$ is a quadratic irrational, then by Lagrange's theorem, its CF is eventually periodic: $\alpha = [a_0; a_1, \ldots, a_m, \overline{a_{m+1}, \ldots, a_{m+p}}]$. The partial quotients form an eventually periodic sequence, which is certainly bounded.

Conversely, if $\alpha$ is rational, its CF is finite (hence terminates, not relevant here since we consider only irrationals). If $\alpha$ is irrational but not quadratic, then by the contrapositive of Lagrange's theorem, its CF is not eventually periodic. However, we need more: we need that the partial quotients are *unbounded*.

**Important subtlety:** Lagrange's theorem tells us that non-quadratic irrationals have non-periodic CF, but does NOT immediately imply unbounded partial quotients. A non-periodic sequence can still be bounded (e.g., the Thue--Morse sequence over $\{1, 2\}$ is non-periodic but bounded). However, for the purpose of the equivalence stated in Corollary 3.2:

- If $\alpha$ is a quadratic irrational: partial quotients are bounded (by eventual periodicity). $\checkmark$
- If $\alpha$ is irrational with bounded partial quotients: the set of such numbers is precisely the set of *badly approximable numbers*. By a theorem from the metric theory of continued fractions, this set has Lebesgue measure zero but is uncountable. It includes all quadratic irrationals, but conceivably could include non-quadratic irrationals.

**Clarification for this project:** The precise statement we need is:

> **Bounded partial quotients $\Leftrightarrow$ badly approximable $\Leftarrow$ quadratic irrational.**

The reverse implication (badly approximable $\Rightarrow$ quadratic irrational) is FALSE in general. There exist transcendental numbers with bounded partial quotients (for instance, certain Sturmian-constructed transcendentals). However, for *algebraic* numbers:

- All algebraic irrationals of degree $\geq 3$ are conjectured to have unbounded partial quotients, but this is unproven (it is a major open problem in number theory).
- Roth's theorem \cite{roth1955rational} gives irrationality measure 2 for all algebraic irrationals, but this does not directly determine boundedness of partial quotients.

**For the purpose of our characterization of Sturmian linear recurrence**, the relevant equivalence is:

> **Theorem 3.3.** A Sturmian word $\Delta_r$ is linearly recurrent $\Leftrightarrow$ the partial quotients of $\{r\}$ are bounded $\Leftarrow$ $r$ is a quadratic irrational.

The converse ($\Leftarrow$ is not $\Leftrightarrow$ in the second step) means that there could in principle exist non-quadratic irrationals $r$ for which $\Delta_r$ is linearly recurrent (if their CF partial quotients happen to be bounded). However:

- Among quadratic irrationals, ALL have linearly recurrent $\Delta_r$. This is a provable fact.
- Among algebraic irrationals of degree $\geq 3$, it is widely believed (but unproven) that NONE have bounded partial quotients, hence none would have linearly recurrent $\Delta_r$.
- Among transcendentals, specific constructions can give bounded partial quotients, but "generic" transcendentals do not.

### 3.3 Examples

| $r$ | Type | CF Expansion | Partial Quotients Bounded? | $\Delta_r$ Linearly Recurrent? |
|-----|------|-------------|---------------------------|-------------------------------|
| $\varphi = \frac{1+\sqrt{5}}{2}$ | Quadratic | $[1; \overline{1}]$ | Yes ($\leq 1$) | **Yes**, $C \leq 4$ |
| $\sqrt{2}$ | Quadratic | $[1; \overline{2}]$ | Yes ($\leq 2$) | **Yes**, $C \leq 5$ |
| $\sqrt{3}$ | Quadratic | $[1; \overline{1, 2}]$ | Yes ($\leq 2$) | **Yes**, $C \leq 5$ |
| $1 + \sqrt{2}$ | Quadratic | $[2; \overline{2}]$ | Yes ($\leq 2$) | **Yes**, $C \leq 5$ |
| $\sqrt[3]{2}$ | Alg. deg. 3 | $[1; 3, 1, 5, 1, 1, 4, \ldots]$ | Conjectured No | Conjectured **No** |
| $\pi$ | Transcendental | $[3; 7, 15, 1, 292, \ldots]$ | No (292 already large) | **No** |
| $e$ | Transcendental | $[2; 1, 2, 1, 1, 4, 1, 1, 6, \ldots]$ | No ($a_k \to \infty$) | **No** |

---

## 4. Key Distinction: Two Notions of "Linear Recurrence"

This section highlights a terminological issue that is **critical** for the entire research project. Two entirely different mathematical concepts share similar names, and conflating them leads to erroneous reasoning.

### 4.1 Notion A: Linearly Recurrent Sturmian Word (Combinatorics on Words)

**Setting:** The infinite word $\Delta_r = \Delta_r(1)\Delta_r(2)\Delta_r(3)\cdots$ over the binary alphabet $\{\lfloor r \rfloor, \lceil r \rceil\}$.

**The property:** $\Delta_r$ is *linearly recurrent* if there exists $C > 0$ such that every factor of length $n$ reappears within every window of length $Cn$ in the word. Formally, $R_{\Delta_r}(n) \leq Cn$.

**Characterization (Durand + Lagrange):** This holds iff the CF partial quotients of $\{r\}$ are bounded, which is guaranteed (and, among algebraic numbers, equivalent to the condition) that $r$ is a quadratic irrational.

**Nature:** This is a property of the SYMBOLIC DYNAMICS of the first-difference sequence. It concerns the PATTERN STRUCTURE of the letters in $\Delta_r$: how often patterns repeat, how predictable the sequence is in a combinatorial sense.

### 4.2 Notion B: Homogeneous Linear Recurrence for the Integer Sequence (Algebra)

**Setting:** The integer-valued sequence $b_r(n) = \lfloor nr \rfloor$.

**The property:** There exist a finite order $d$ and integer coefficients $c_0, c_1, \ldots, c_d$ (not all zero) such that $\sum_{i=0}^{d} c_i \, b_r(n+i) = 0$ for all $n$ (or for all sufficiently large $n$), either for the full sequence or for some infinite subsequence.

**Characterization:** This is a property of the INTEGER VALUES of the sequence. Solutions to such recurrences have the form $a_n = \sum_j P_j(n) \lambda_j^n$ where $\lambda_j$ are algebraic numbers and $P_j$ are polynomials.

### 4.3 Why These Notions are Independent

**Notion A does NOT imply Notion B.** Consider $r = \varphi = (1+\sqrt{5})/2$, the golden ratio. The Sturmian word $\Delta_\varphi$ is linearly recurrent (since $\varphi$ is quadratic irrational with CF $[1; \overline{1}]$, and the partial quotients are bounded by 1). However, the integer sequence $\lfloor n\varphi \rfloor$ grows linearly (asymptotically $n\varphi$). Any subsequence along an arithmetic progression $\lfloor (a+kd)\varphi \rfloor$ grows like $kd\varphi$, which is linear in $k$. For this to satisfy a homogeneous linear recurrence, the characteristic polynomial would need a root $\lambda = 1$ with multiplicity 2 (to produce solutions of the form $Ak + B$). But $\lfloor (a+kd)\varphi \rfloor$ is NOT exactly equal to $Ak + B$ for any constants $A, B$, because $\{(a+kd)\varphi\}$ is equidistributed (since $d\varphi$ is irrational), so the floor function introduces fluctuations that prevent exact linear recurrence. The symbolic linear recurrence of the Sturmian word says nothing about algebraic recurrence of the integer values.

**Notion B does NOT imply Notion A.** Consider $r = 3/2$ (rational). The full sequence $\lfloor 3n/2 \rfloor$ satisfies the homogeneous linear recurrence $a_{n+4} - 2a_{n+2} + a_n = 0$ (derived from $a_{n+2} - a_n = 3$, then differencing again). So Notion B holds. But the first-difference sequence $\Delta_{3/2}$ is periodic (with period 2: it alternates 1, 2, 1, 2, ...), which is NOT Sturmian. Since $r$ is rational, Notion A does not even apply (Sturmian words require irrational slope), and the periodic sequence is certainly not linearly recurrent in the Sturmian sense (periodicity means $p(n) \leq q < n+1$ for large $n$, violating the Sturmian complexity requirement).

### 4.4 Summary Table

| | Notion A (Symbolic LR) | Notion B (Algebraic LR) |
|---|---|---|
| **Domain** | Infinite word $\Delta_r$ over finite alphabet | Integer sequence $\lfloor nr \rfloor$ |
| **Type of recurrence** | Combinatorial: pattern repetition with linear gap bound | Algebraic: linear combination of terms equals zero |
| **Growth** | Not applicable (letters from fixed alphabet) | Sequence grows like $nr$; solutions are exponential/polynomial |
| **Holds for $r$ rational** | Not applicable (not Sturmian) | **Yes** (full sequence is linearly recurrent) |
| **Holds for $r$ quadratic irrational** | **Yes** (Durand + Lagrange) | **Open / likely No** for non-trivial subsequences |
| **Holds for $r$ transcendental** | Depends on CF structure | **Open / likely No** |

### 4.5 Implications for the Research Project

The central question of this project (Item 001) asks about Notion B: for which $r$ does $\lfloor nr \rfloor$ contain a subsequence satisfying a homogeneous linear recurrence with constant coefficients?

The results of this document (Durand's theorem, Lagrange's theorem) concern Notion A. They are relevant as BACKGROUND CONTEXT but do NOT directly answer the central question. Specifically:

1. Durand's characterization tells us when the SYMBOLIC STRUCTURE of $\Delta_r$ has good combinatorial recurrence properties. This is useful for understanding the regularity of the Beatty sequence, but it does not imply (or refute) the existence of algebraically recurrent subsequences.

2. The connection to Ostrowski numeration (for quadratic irrationals) may provide tools for addressing the central question, via the decidability results of Schaeffer--Shallit--Zorcic \cite{schaeffer2024beatty} (see Item 005).

3. The key takeaway is: **linear recurrence of the Sturmian word is a DIFFERENT PROPERTY from linear recurrence of the integer-valued Beatty sequence**. Results about one do not automatically transfer to the other.

---

## 5. Conclusion and Forward References

This document establishes:

1. **Theorem 1.1:** $\Delta_r$ is Sturmian iff $r$ is irrational. (Proved in full.)

2. **Theorem 2.1 (Durand):** A Sturmian word is linearly recurrent iff its CF partial quotients are bounded. (Proof sketch given, citing \cite{durand1998characterization, durand2003linearly, cassaigne1999limit}.)

3. **Theorem 3.3 (Durand + Lagrange):** Among algebraic numbers, $\Delta_r$ is linearly recurrent iff $r$ is a quadratic irrational. (More precisely: quadratic irrational $\Rightarrow$ bounded PQ $\Rightarrow$ linearly recurrent. The converse "linearly recurrent $\Rightarrow$ quadratic irrational" holds among algebraic numbers but not in general.)

4. **Section 4:** The notions of "linearly recurrent Sturmian word" and "homogeneous linearly recurrent integer subsequence" are INDEPENDENT and must not be conflated.

**Forward references:**
- Item 005 explores the Skolem--Mahler--Lech theorem, three-distance theorem, and Schaeffer--Shallit decidability, which provide further tools for the central question.
- Item 006 provides a rigorous analysis of the independence of the two recurrence notions, with detailed proofs that neither implies the other.
- Items 011--014 (Phase 3) will synthesize these results into the main characterization theorem.

---

## References

- \cite{morse1938symbolic} Morse, M. and Hedlund, G.A. (1938). Symbolic dynamics. *Amer. J. Math.* 60(4), 815--866.
- \cite{morse1940symbolic2} Morse, M. and Hedlund, G.A. (1940). Symbolic dynamics II: Sturmian trajectories. *Amer. J. Math.* 62(1), 1--42.
- \cite{coven1973sequences} Coven, E.M. and Hedlund, G.A. (1973). Sequences with minimal block growth. *Math. Systems Theory* 7(2), 138--153.
- \cite{durand1998characterization} Durand, F. (1998). A characterization of substitutive sequences using return words. *Discrete Math.* 179, 89--101.
- \cite{durand2003linearly} Durand, F. (2000). Linearly recurrent subshifts have a finite number of non-periodic subshift factors. *Ergodic Theory Dynam. Systems* 20(4), 1061--1078.
- \cite{cassaigne1999limit} Cassaigne, J. (1999). Limit values of the recurrence quotient of Sturmian sequences. *Theoret. Comput. Sci.* 218(1), 3--12.
- \cite{cassaigne2001recurrence} Cassaigne, J. (2001). Recurrence in infinite words. *Proc. STACS 2001*.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences: Theory, Applications, Generalizations.* Cambridge University Press.
- \cite{lagrange1770continued} Lagrange, J.-L. (1770). Additions au memoire sur la resolution des equations numeriques.
- \cite{roth1955rational} Roth, K.F. (1955). Rational approximations to algebraic numbers. *Mathematika* 2(1), 1--20.
- \cite{schaeffer2024beatty} Schaeffer, L., Shallit, J., and Zorcic, S. (2024). Beatty Sequences for a Quadratic Irrational: Decidability and Applications. arXiv:2402.08331.
