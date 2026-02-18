# Research Summary: Characterizing Homogeneous Linear Recurrence in Beatty Sequences

## Item 022 -- Phase 5: Analysis & Documentation

---

## Abstract

We investigate the question of which positive real numbers $r$ have the property that the Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains a non-trivial subsequence, indexed by an arithmetic progression, that satisfies a homogeneous linear recurrence with constant integer coefficients. We obtain a clean and complete characterization: **$r$ must be rational**. For rational $r = p/q$ written in lowest terms, the full Beatty sequence satisfies a minimal-order homogeneous linear recurrence of order $q + 1$, with characteristic polynomial $(x - 1)(x^q - 1)$. The roots of this polynomial are $x = 1$ (a double root) together with the non-trivial $q$-th roots of unity, and the general solution decomposes into a linear-growth term $A + Bn$ plus a periodic oscillation with period $q$. For irrational $r$ -- regardless of algebraic degree, irrationality measure, continued fraction structure, or transcendence -- no arithmetic-progression-indexed subsequence of $\lfloor nr \rfloor$ satisfies any homogeneous linear recurrence of any finite order. The impossibility proof rests on the rationality constraint governing the asymptotic slope of integer-valued linear recurrence sequences: the slope must be rational, but for irrational $r$ and integer step $d \geq 1$, the asymptotic slope $dr$ is necessarily irrational. We verify the theorem computationally against 102 values of $r$ spanning four classes (rational, quadratic irrational, algebraic of degree $\geq 3$, transcendental) with perfect agreement: 60 out of 60 rationals yield recurrences and 0 out of 42 irrationals do. We further clarify the independence of two distinct notions of "linear recurrence" appearing in the literature: combinatorial pattern recurrence of Sturmian words (Notion A, studied by Durand and Cassaigne) and algebraic integer-valued recurrence (Notion B, the subject of this work).

---

## 1. Problem Statement and Motivation

### 1.1 Beatty Sequences and Their Role in Number Theory

The Beatty sequence associated with a positive real number $r$ is the integer sequence $a_n = \lfloor nr \rfloor$ for $n \geq 1$, where $\lfloor \cdot \rfloor$ denotes the floor function. These sequences are among the most natural objects in combinatorial number theory, arising in the 1926 problem posed by Samuel Beatty \cite{beatty1926problem}: if $r$ and $s$ are positive irrationals satisfying $1/r + 1/s = 1$, then the sequences $(\lfloor nr \rfloor)$ and $(\lfloor ns \rfloor)$ partition the positive integers. This result, sometimes attributed to Lord Rayleigh in the context of acoustics, established Beatty sequences as a foundational construct linking floor functions, irrational rotations, and partitions of the integers.

Since Beatty's original work, the sequences $\lfloor nr \rfloor$ have appeared throughout mathematics: in combinatorial game theory (Wythoff's game and its generalizations), in the theory of balanced sequences and Sturmian words, in Diophantine approximation (via the connection to continued fractions and the three-distance theorem), and in automata theory (via Ostrowski numeration for quadratic irrationals). Fraenkel \cite{fraenkel1969bracket} developed a systematic theory of the bracket function $\lfloor nr \rfloor$ and its complementary sets, establishing algebraic identities and partition properties that remain central to the field.

### 1.2 Why the Recurrence Question Is Natural

A homogeneous linear recurrence with constant coefficients is one of the most fundamental algebraic structures an integer sequence can possess. Sequences satisfying such recurrences -- including the Fibonacci numbers, Lucas numbers, powers of integers, and more generally all exponential-polynomial sequences -- form a well-understood class with deep connections to algebra (characteristic polynomials, roots of unity), analysis (generating functions), and logic (the Skolem-Mahler-Lech theorem on zero sets \cite{skolem1934einige, mahler1935arithmetische, lech1953note}). Given the ubiquity and structural importance of Beatty sequences, it is natural to ask: for which values of $r$ does $\lfloor nr \rfloor$ (or some natural subsequence thereof) satisfy a homogeneous linear recurrence?

For rational $r$, the answer is elementary: the first differences $\lfloor (n+1)r \rfloor - \lfloor nr \rfloor$ are periodic, and periodicity of first differences implies the original sequence satisfies a finite-order linear recurrence. For irrational $r$, the question is far more subtle. The first-difference sequence is a Sturmian word -- a highly structured but aperiodic binary sequence -- and the relationship between the symbolic properties of this word and the algebraic properties of the cumulative sum $\lfloor nr \rfloor$ is delicate.

### 1.3 Connection to Sturmian Words, Automatic Sequences, and OEIS

The first-difference sequence $\Delta_r(n) = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor$ is a Sturmian word when $r$ is irrational: it is a binary sequence over the alphabet $\{\lfloor r \rfloor, \lceil r \rceil\}$ with subword complexity $p(n) = n + 1$, the minimal complexity for a non-eventually-periodic sequence. Sturmian words have been studied intensively in the combinatorics-on-words literature, with major contributions by Morse and Hedlund, Coven and Hedlund, and more recently Durand \cite{durand1998characterization} and Cassaigne \cite{cassaigne1999limit}. For quadratic irrationals, the Sturmian word is morphic (the fixed point of a substitution), and the Beatty sequence is recognizable by finite automata in the Ostrowski numeration system \cite{schaeffer2024beatty, allouche2003automatic}. Many specific Beatty sequences appear in the Online Encyclopedia of Integer Sequences (OEIS), including $\lfloor n\varphi \rfloor$ (A000201), $\lfloor n\sqrt{2} \rfloor$ (A001951), and $\lfloor n\sqrt{3} \rfloor$ (A022838).

A key motivation for the present work is to determine whether the rich combinatorial structure of Sturmian words translates into algebraic recurrence for the integer-valued Beatty sequence. As we shall see, it does not.

### 1.4 Four-Class Taxonomy of $r$

We classify positive reals into four classes based on their algebraic and number-theoretic properties:

**Class I: Rational numbers** ($r = p/q$ in lowest terms). The first-difference sequence is periodic with period $q$. This is the class where recurrences exist.

**Class II: Quadratic irrationals** ($r = (a + b\sqrt{D})/c$). By Lagrange's theorem \cite{lagrange1770continued}, these have eventually periodic continued fractions with bounded partial quotients. By Durand's theorem \cite{durand1998characterization}, the Sturmian word $\Delta_r$ is linearly recurrent in the combinatorial sense. Examples: the golden ratio $\varphi = (1+\sqrt{5})/2$, $\sqrt{2}$, $\sqrt{3}$.

**Class III: Algebraic irrationals of degree $\geq 3$**. By Roth's theorem \cite{roth1955rational}, these have irrationality measure exactly 2, but their continued fraction expansions are conjectured to have unbounded partial quotients. Examples: $\sqrt[3]{2}$, $\sqrt[3]{3}$, $2^{1/4}$.

**Class IV: Transcendental numbers**. These may have irrationality measure equal to 2 (like $e$) or larger (like certain Liouville numbers). Their continued fraction structures vary widely. Examples: $\pi$, $e$, $\ln 2$.

---

## 2. Main Results

### 2.1 Main Characterization Theorem

The central result of this research is a three-way equivalence that completely resolves the recurrence question.

**Theorem (Main Characterization).** *Let $r > 0$ be a real number. The following are equivalent:*

> **(i)** $r$ is rational.
>
> **(ii)** The Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ itself satisfies a non-trivial homogeneous linear recurrence with constant integer coefficients.
>
> **(iii)** The Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains an infinite subsequence, indexed by an arithmetic progression, that satisfies a non-trivial homogeneous linear recurrence with constant integer coefficients.

The implication (i) $\Rightarrow$ (ii) is the constructive rational case. The implication (ii) $\Rightarrow$ (iii) is trivial (take the full sequence as a subsequence with step $d = 1$). The implication (iii) $\Rightarrow$ (i) is the irrational impossibility result, proved by contrapositive.

### 2.2 The Rational Case: Explicit Minimal Recurrence of Order $q + 1$

For rational $r = p/q$ with $\gcd(p,q) = 1$ and $p, q > 0$, we establish the fundamental shift identity $a_{n+q} = a_n + p$ for all $n \geq 1$. This is an inhomogeneous recurrence of order $q$ with constant right-hand side $p$. Applying the annihilator $(E - 1)$ of constants to both sides yields the homogeneous recurrence of order $q + 1$:

$$a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0 \qquad \text{for all } n \geq 1.$$

The characteristic polynomial is $x^{q+1} - x^q - x + 1 = (x-1)(x^q - 1) = (x-1)^2 \prod_{d \mid q, d > 1} \Phi_d(x)$, where $\Phi_d(x)$ denotes the $d$-th cyclotomic polynomial. The roots are $x = 1$ (double root) and the non-trivial $q$-th roots of unity (each simple). The general solution takes the form $a_n = A + Bn + \sum_{k=1}^{q-1} \gamma_k e^{2\pi ikn/q}$, expressing the sequence as a linear trend plus a periodic oscillation.

We prove that this order $q + 1$ is minimal: no homogeneous recurrence of order $\leq q$ is satisfied by $\lfloor np/q \rfloor$ when $\gcd(p,q) = 1$ and $q > 1$. The minimality proof shows that the $q$-fold periodicity of the fractional parts $\{np/q\}$ requires exactly $q - 1$ oscillatory roots, which combined with the double root at 1 yields $q + 1$ roots total. Notably, the minimal homogeneous order is $q + 1$, not the naive estimate of $2q$ obtained from the double application $(E^q - 1)^2 a_n = 0$.

For arithmetic-progression subsequences with step $d$, the recurrence order reduces to $q' + 1$ where $q' = q / \gcd(d, q)$. In particular, when $d$ is a multiple of $q$, the subsequence is a simple arithmetic progression satisfying a second-order recurrence.

### 2.3 The Irrational Case: Impossibility Proof

For irrational $r$, we prove that no AP-indexed subsequence $s_k = \lfloor (a + kd)r \rfloor$ (with $d \geq 1$) satisfies a homogeneous linear recurrence with integer coefficients. The proof proceeds in three steps:

**Step 1 (Growth analysis).** Since $s_k \sim kdr$ as $k \to \infty$, any hypothetical recurrence solution $\sum P_j(k)\lambda_j^k$ must exhibit linear growth. This forces all characteristic roots to have $|\lambda_j| \leq 1$, and requires a double root at $\lambda = 1$ to produce the leading term $\alpha_1 k + \alpha_0$.

**Step 2 (Rationality constraint).** Because the recurrence has integer coefficients and integer initial conditions, and the root $\lambda = 1$ is rational, the coefficient $\alpha_1$ in the polynomial part at $\lambda = 1$ must be rational. This follows from the fact that $\alpha_1$ is determined by rational linear algebra on integer data through a rational characteristic root.

**Step 3 (Contradiction).** The asymptotic slope $\alpha_1 = \lim_{k \to \infty} s_k / k = dr$. Since $d \geq 1$ is a positive integer and $r$ is irrational, $dr$ is irrational. But Step 2 requires $\alpha_1 \in \mathbb{Q}$. This is a contradiction.

An alternative proof uses Weyl's equidistribution theorem \cite{weyl1916gleichverteilung}: the error term $\varepsilon_k = -\{(a + kd)r\}$ is equidistributed in $(-1, 0]$ (since $dr$ is irrational), but any bounded linear recurrence sequence takes only finitely many values in each period (by the Kronecker theorem, algebraic integers on the unit circle that are roots of integer-coefficient polynomials must be roots of unity, so the bounded part of any recurrence solution is eventually periodic). An equidistributed sequence cannot be eventually periodic, giving the contradiction.

### 2.4 Uniformity Across All Classes of Irrationals

A striking feature of the impossibility proof is its uniformity. The argument uses only the single fact that $r$ is irrational. It does not invoke the algebraic degree of $r$, the irrationality measure (Roth's theorem \cite{roth1955rational} gives measure exactly 2 for all algebraics, but our proof does not use this), the continued fraction structure (bounded or unbounded partial quotients), or any Diophantine approximation property. Whether $r$ is a quadratic irrational like $\varphi = (1 + \sqrt{5})/2$ with perfectly structured continued fraction $[1; \overline{1}]$, a cubic irrational like $\sqrt[3]{2}$ with apparently random partial quotients, or a transcendental like $\pi$ with the famous large partial quotient $a_5 = 292$, the obstruction is identical: the product $dr$ is irrational whenever $d$ is a positive integer and $r$ is irrational.

### 2.5 Sharp Discontinuous Transition at the Rational Boundary

The characterization reveals a sharp discontinuous transition. Consider the perturbation $r_\varepsilon = p/q + \varepsilon$: for $\varepsilon = 0$, the Beatty sequence satisfies a recurrence of order $q + 1$; for any irrational $\varepsilon \neq 0$ (no matter how small), no recurrence of any order exists. There is no "approximately recurrent" intermediate regime. The recurrence either holds exactly (rational $r$) or fails completely (irrational $r$). This discontinuity is particularly vivid in the comparison of $\pi$ versus its famous rational approximation $355/113$: the sequences $\lfloor n\pi \rfloor$ and $\lfloor 355n/113 \rfloor$ agree for the first several million terms, yet the former satisfies no recurrence while the latter satisfies one of order 114.

---

## 3. Methodology

### 3.1 Berlekamp-Massey Algorithm with Dual-Prime Modular Screening

The computational backbone of our recurrence detection is the Berlekamp-Massey (BM) algorithm \cite{berlekamp1968algebraic, massey1969shift}, which finds the shortest linear feedback shift register that generates a given finite sequence. We implemented BM with a dual-prime modular screening approach: candidate recurrences are first detected modulo two distinct large primes $p_1$ and $p_2$, and only candidates that agree modulo both primes are promoted to exact verification over the integers. This dramatically reduces false positives arising from modular coincidences while maintaining computational efficiency.

The BM algorithm has a well-known susceptibility to quasi-periodic sequences: for irrational $r$, the Beatty sequence is "almost periodic" (in the sense that its first differences have low complexity), and BM may return spurious recurrences of high order that happen to hold for the first $N$ terms but fail for larger $N$. To combat this, we imposed a conservative order cap of $N/10$ (where $N$ is the sequence length) and required all candidate recurrences to be verified on at least 10,000 terms using exact integer arithmetic.

### 3.2 Exact Rational Arithmetic Verification

For rational $r = p/q$, the Beatty sequence $\lfloor np/q \rfloor$ can be computed exactly using integer division, avoiding any floating-point error. For irrational $r$, we used the `mpmath` library with configurable precision (typically 50 decimal digits, far exceeding the precision needed for sequences of length 10,000). All recurrence verifications were performed using exact integer arithmetic: given candidate coefficients $c_0, \ldots, c_D$, we checked $\sum_{i=0}^D c_i a_{n+i} = 0$ for every valid $n$ in the sequence.

### 3.3 Systematic Arithmetic-Progression Subsequence Search

For each tested value of $r$, we enumerated arithmetic-progression subsequences $s_k = \lfloor (a + kd) r \rfloor$ for offsets $a \in \{0, 1, \ldots, A_{\max}\}$ and steps $d \in \{1, 2, \ldots, D_{\max}\}$. The baseline search used $A_{\max} = D_{\max} = 20$, and the large-scale search maintained these parameters across 102 values of $r$. For each candidate subsequence of length at least 50, the BM algorithm was run to detect recurrences of order up to $d_{\max} = 10$ (with extended searches up to $d_{\max} = 50$ for sensitivity analysis).

### 3.4 Extended Verification to Eliminate False Positives

Two initial false positives were encountered during the large-scale search: for $r = \sqrt{13}$ and $r = \sqrt{14}$, the BM algorithm reported recurrences of high order that held for the first 1,000 terms but failed upon extension to 10,000 terms. Investigation revealed that these were artifacts of the quasi-periodic structure of the Beatty sequence interacting with the BM algorithm's greedy search. The extended verification protocol (requiring agreement on 10,000+ terms) successfully eliminated all such false positives. After correction, the search produced zero false positives across all 42 irrational values tested.

### 3.5 Large-Scale Computational Survey

The final survey tested 102 values of $r$: 60 rational (including all $p/q$ with $q \leq 20$ and selected larger denominators), 24 quadratic irrationals ($\sqrt{D}$ for various squarefree $D$ and numbers of the form $(a + \sqrt{D})/b$), 15 algebraic irrationals of degree 3 through 6 (cube roots, fourth roots, fifth roots, and roots of specific irreducible polynomials), and 3 transcendentals ($\pi$, $e$, $\ln 2$). Results are stored in `results/large_scale_search.csv`.

---

## 4. Key Findings

### 4.1 Perfect Rational/Irrational Dichotomy

The computational results exhibit a perfect binary dichotomy. Of the 60 rational values tested, every single one yielded a verified homogeneous linear recurrence (60/60). Of the 42 irrational values tested (spanning all three irrational classes), not a single one yielded a recurrence (0/42). The contingency table has zero false positives and zero false negatives. The theorem's prediction agrees with experiment in all 102 cases -- a 100% agreement rate with no exceptions, caveats, or marginal cases.

### 4.2 Minimal Recurrence Order $q + 1$, Not $2q$

A notable finding is that the minimal homogeneous recurrence order for $r = p/q$ is $q + 1$, which is strictly less than the naive estimate $2q$ obtained from the double-difference $(E^q - 1)^2 a_n = 0$ whenever $q \geq 2$. The key insight is that the inhomogeneous term in $(E^q - 1)a_n = p$ is a constant, which is annihilated by the first-order operator $(E - 1)$ rather than the order-$q$ operator $(E^q - 1)$. This gives $(E - 1)(E^q - 1)a_n = 0$, an operator of order $q + 1$, which is minimal. For example, the sequence $\lfloor 3n/2 \rfloor$ satisfies a recurrence of order 3 (not 4), and $\lfloor 5n/3 \rfloor$ satisfies one of order 4 (not 6).

### 4.3 Characteristic Polynomial and Cyclotomic Structure

The characteristic polynomial $(x-1)(x^q - 1) = (x-1)^2 \prod_{d \mid q, d > 1} \Phi_d(x)$ has a clean cyclotomic factorization. The double root at $x = 1$ governs the linear growth, while the simple roots at the non-trivial $q$-th roots of unity govern the periodic oscillation of the fractional parts. This cyclotomic structure connects the Beatty sequence recurrence to the arithmetic of roots of unity, providing an algebraic explanation for why the first differences have period exactly $q$.

For the specific case $r = 3/2$ ($q = 2$), the characteristic polynomial is $(x-1)^2(x+1)$, with roots $1, 1, -1$, and general solution $a_n = A + Bn + C(-1)^n$. For $r = 5/3$ ($q = 3$), the polynomial is $(x-1)^2(x^2 + x + 1)$, with roots including the primitive cube roots of unity. For $r = 7/4$ ($q = 4$), the polynomial factors as $(x-1)^2(x+1)(x^2+1)$, incorporating both the square root of $-1$ and the real root $-1$.

### 4.4 First Differences: Periodic for Rationals, Equidistributed for Irrationals

For rational $r = p/q$, the first-difference sequence $\Delta_r(n) = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor$ is periodic with minimal period $q$ and takes values in $\{\lfloor p/q \rfloor, \lceil p/q \rceil\}$. For irrational $r$, the first differences form a Sturmian word: they are aperiodic and the fractional parts $\{nr\}$ are equidistributed in $[0, 1)$ by Weyl's theorem \cite{weyl1916gleichverteilung}. This equidistribution is the geometric manifestation of the irrationality obstruction: it ensures that the error term $-\{(a + kd)r\}$ in the decomposition $s_k = kdr + ar - \{(a + kd)r\}$ cannot be captured by any finite combination of periodic functions, which is precisely what a linear recurrence would require.

### 4.5 False Positive Susceptibility and Mitigation

The Berlekamp-Massey algorithm is susceptible to false positives on quasi-periodic sequences. For irrational $r$ close to a rational $p/q$ (or more generally, when the continued fraction has large partial quotients), the Beatty sequence has long stretches that closely mimic the periodic behavior of a rational Beatty sequence. The BM algorithm may lock onto this near-periodicity and report a high-order recurrence that holds for the observed data but fails for longer sequences. Our dual-prime modular screening eliminates most such candidates, and the extended verification to 10,000+ terms catches the remainder. The two false positives encountered during testing ($\sqrt{13}$ and $\sqrt{14}$) were both successfully caught and corrected by the extended verification protocol, demonstrating the importance of rigorous validation in computational number theory.

### 4.6 Independence of Combinatorial Recurrence (Notion A) and Algebraic Recurrence (Notion B)

A central conceptual finding is the complete independence of two notions of "linear recurrence" that arise in the Beatty sequence literature:

**Notion A (Combinatorial/Symbolic).** The Sturmian word $\Delta_r$ is linearly recurrent in the combinatorics-on-words sense: every factor of length $n$ reappears within a window of length $Cn$. By Durand's theorem \cite{durand1998characterization}, this holds if and only if the partial quotients of $r$ are bounded, which by Lagrange's theorem \cite{lagrange1770continued} is equivalent to $r$ being a quadratic irrational.

**Notion B (Algebraic/Integer-Valued).** The Beatty sequence $\lfloor nr \rfloor$ (or a subsequence thereof) satisfies a homogeneous linear recurrence $\sum c_i a_{n+i} = 0$ with integer coefficients. Our theorem shows this holds if and only if $r$ is rational.

These notions operate in entirely different mathematical domains: Notion A concerns the symbolic dynamics of a bounded binary sequence, while Notion B concerns the algebra of an unbounded integer sequence. Neither implies the other. The golden ratio $\varphi$ witnesses $A \not\Rightarrow B$ (the Sturmian word for $\varphi$ is linearly recurrent, but $\lfloor n\varphi \rfloor$ satisfies no algebraic recurrence). Any rational $r$ like $3/2$ witnesses $B \not\Rightarrow A$ (the sequence $\lfloor 3n/2 \rfloor$ satisfies an algebraic recurrence, but its first-difference sequence is periodic and not Sturmian). This independence resolves a potential source of confusion in the literature, where the shared terminology "linearly recurrent" might suggest a connection that does not exist.

---

## 5. Comparison with Prior Work

### 5.1 Beatty (1926) and Fraenkel (1969)

Beatty's original theorem \cite{beatty1926problem} established that $(\lfloor nr \rfloor)$ and $(\lfloor ns \rfloor)$ partition the positive integers when $1/r + 1/s = 1$ and $r, s$ are positive irrationals. Fraenkel \cite{fraenkel1969bracket} extended this to a comprehensive theory of the bracket function, including complementary sets, partition identities, and connections to combinatorial game theory. Our work addresses a different question (algebraic recurrence rather than partition properties) but builds on the same foundational understanding of $\lfloor nr \rfloor$.

### 5.2 Durand (1998, 2000): Sturmian Linear Recurrence

Durand \cite{durand1998characterization} proved that a Sturmian word is linearly recurrent (Notion A) if and only if its continued fraction partial quotients are bounded. In a companion paper \cite{durand2003linearly}, he showed that linearly recurrent subshifts have finitely many non-periodic factors. These results characterize Notion A completely. Our work proves that Notion A is independent of Notion B and provides the analogous complete characterization for Notion B. The two characterizations are strikingly different: Notion A depends on CF structure (bounded PQ iff quadratic irrational), while Notion B depends only on rationality.

### 5.3 Cassaigne (1999): Recurrence Quotient Computations

Cassaigne \cite{cassaigne1999limit} computed exact formulas for the liminf and limsup of the recurrence quotient $R(n)/n$ for Sturmian words in terms of the continued fraction partial quotients. These formulas provide precise quantitative information about Notion A. Our work shows that the Cassaigne recurrence quotient, despite being a deep invariant of the Sturmian symbolic dynamics, has no bearing on Notion B. The golden ratio, with $\limsup R(n)/n \leq 4$, and $\pi$, with $\limsup R(n)/n = \infty$, both fail Notion B identically.

### 5.4 Allouche and Shallit (2003): Automatic/Morphic Sequence Taxonomy

Allouche and Shallit \cite{allouche2003automatic} developed a comprehensive theory of automatic and morphic sequences. For quadratic irrationals, the Sturmian first-difference sequence is morphic (the fixed point of a substitution), and many properties are decidable via automata-theoretic methods. However, the integer-valued Beatty sequence $\lfloor nr \rfloor$ is unbounded and therefore cannot be automatic or morphic in the classical sense. The cumulative summation that produces $\lfloor nr \rfloor$ from the morphic sequence $\Delta_r$ does not preserve the exponential-polynomial solution structure required by linear recurrences, which is why the morphic structure of $\Delta_r$ does not propagate to algebraic recurrence of $\lfloor nr \rfloor$.

### 5.5 Schaeffer, Shallit, and Zorcic (2024): Decidability for Quadratic Beatty Sequences

Schaeffer, Shallit, and Zorcic \cite{schaeffer2024beatty} proved that the first-order theory of $(\mathbb{N}, +, B_\alpha)$ is decidable when $\alpha$ is a quadratic irrational, by showing that the Beatty sequence is "synchronized" in the Ostrowski-$\alpha$ numeration system. This means that questions about quadratic Beatty sequences can in principle be answered by finite automaton constructions. The statement "no AP subsequence of $\lfloor n\alpha \rfloor$ satisfies a homogeneous linear recurrence of order $\leq D$" is a first-order sentence that their framework can verify for specific quadratic irrationals and specific bounds $D$. Our proof provides a uniform argument that works for all irrationals simultaneously, without case-by-case automaton construction. The Ostrowski framework could serve as independent computational confirmation of our theorem for specific quadratic values.

### 5.6 Skolem-Mahler-Lech: Zero Sets of Linear Recurrence Sequences

The Skolem-Mahler-Lech theorem \cite{skolem1934einige, mahler1935arithmetische, lech1953note} states that the zero set of a linear recurrence sequence over a field of characteristic zero is a finite union of arithmetic progressions plus a finite set. In our proof, this theorem plays a supporting role: it constrains the structure of the bounded remainder $g(k) = s_k - \alpha_1 k - \alpha_0$, ensuring that its level sets are eventually periodic. Since the fractional parts $\{(a + kd)r\}$ are equidistributed (by Weyl's theorem) and therefore not eventually periodic, the Skolem-Mahler-Lech structure is incompatible with the error term of an irrational Beatty sequence, reinforcing the contradiction.

### 5.7 Novel Contributions

The principal novel contributions of this work, beyond what was known in the existing literature, are:

1. **The complete clean characterization**: $r$ is rational if and only if $\lfloor nr \rfloor$ satisfies a homogeneous linear recurrence, if and only if some AP subsequence does. This three-way equivalence with proof of both directions appears to be new.

2. **The uniform impossibility proof for all irrationals**: The proof makes no distinction among quadratic irrationals, higher-degree algebraics, and transcendentals. The sole property used is that $dr$ is irrational whenever $d$ is a positive integer and $r$ is irrational.

3. **The explicit minimal order formula**: The determination that the minimal homogeneous recurrence order for $r = p/q$ is exactly $q + 1$ (not $2q$), with characteristic polynomial $(x-1)(x^q-1)$ and its cyclotomic factorization, appears to be new in this explicit form.

4. **The independence of Notion A and Notion B**: The rigorous demonstration that Durand-Cassaigne combinatorial recurrence and algebraic integer-valued recurrence are completely independent properties, with explicit witnesses for both non-implications.

---

## 6. Open Questions and Future Directions

### 6.1 Non-Constructive Subsequences

Our theorem covers arithmetic-progression-indexed subsequences and extends (via corollaries) to polynomial and exponential index sets. For completely arbitrary (non-constructive) index sets, one can in principle reverse-engineer indices $n_k$ so that $\lfloor n_k r \rfloor$ equals any desired target sequence. If the target is chosen to satisfy a recurrence, this produces a "recurrent subsequence" by construction. However, the resulting index set has no independent mathematical characterization -- it is defined circularly by the desired output.

**Open Question 1.** *For irrational $r$, does there exist any "natural" (definable, constructive) infinite index set $n_1 < n_2 < \cdots$ such that $\lfloor n_k r \rfloor$ satisfies a homogeneous linear recurrence? What is the correct formalization of "natural" that makes the answer provably negative?*

### 6.2 Inhomogeneous Beatty Sequences

The inhomogeneous Beatty sequence $\lfloor n\alpha + \beta \rfloor$ generalizes the homogeneous case $\beta = 0$ studied here. For rational $\alpha$, the inhomogeneous sequence is still eventually quasi-periodic and should satisfy a linear recurrence. For irrational $\alpha$, the asymptotic slope is still $\alpha$ (independent of $\beta$), so the impossibility proof should adapt directly.

**Open Question 2.** *Prove that $\lfloor n\alpha + \beta \rfloor$ satisfies a homogeneous linear recurrence (with some AP subsequence) if and only if $\alpha$ is rational, for all $\beta \in \mathbb{R}$.*

### 6.3 Quantitative Recurrence Residual Bounds

For near-rational $r = p/q + \varepsilon$ with small irrational $\varepsilon$, the "recurrence residual" $|a_{n+q+1} - a_{n+q} - a_{n+1} + a_n|$ is zero for $\varepsilon = 0$ and nonzero at a rate proportional to $|\varepsilon|$ for $\varepsilon \neq 0$. A precise quantitative relationship between $|\varepsilon|$, $q$, and the density of nonzero residuals would strengthen the qualitative dichotomy established here.

**Open Question 3.** *For $r = p/q + \varepsilon$ with $|\varepsilon|$ small and irrational, give an asymptotic formula for $\#\{n \leq N : R_n(\varepsilon) \neq 0\} / N$ as a function of $\varepsilon$ and $q$.*

### 6.4 Higher-Dimensional Beatty Sequences

For sequences of the form $\lfloor n_1 r_1 + n_2 r_2 \rfloor$ indexed by lattice points $(n_1, n_2) \in \mathbb{Z}^2$, the analogous characterization question is unexplored. The one-dimensional proof relies on the linear growth of $\lfloor (a + kd)r \rfloor$ and the irrationality of its slope; the higher-dimensional setting introduces polynomial growth in multiple variables and new phenomena related to simultaneous Diophantine approximation.

**Open Question 4.** *Characterize the pairs $(r_1, r_2)$ for which the two-dimensional Beatty sequence $\lfloor n_1 r_1 + n_2 r_2 \rfloor$ contains a linearly recurrent subsequence along a lattice arithmetic progression.*

### 6.5 Decidability and Automatic Verification

The Schaeffer-Shallit-Zorcic framework \cite{schaeffer2024beatty} can in principle verify our theorem for specific quadratic irrationals, one at a time. An interesting meta-question is whether the theorem itself -- as a universal statement about all irrationals -- can be proved within a formal decidability framework.

**Open Question 5.** *Can the main characterization theorem be proved within a decidability framework (e.g., using the theory of real-closed fields or Presburger arithmetic augmented with floor functions)?*

### 6.6 Generalizations to Non-Integer-Coefficient Recurrences

Our theorem concerns homogeneous linear recurrences with integer (equivalently, rational) coefficients. If one allows real or algebraic coefficients, the landscape changes: the rationality constraint on the asymptotic slope no longer applies, and new possibilities may arise.

**Open Question 6.** *For irrational $r$, does $\lfloor nr \rfloor$ satisfy a homogeneous linear recurrence with algebraic (but not necessarily rational) coefficients? For example, does $\lfloor n\varphi \rfloor$ satisfy a recurrence with coefficients in $\mathbb{Q}(\sqrt{5})$?*

---

## Bibliography

\cite{beatty1926problem} Beatty, S. (1926). Problem 3173. *The American Mathematical Monthly* 33(3), 159.

\cite{fraenkel1969bracket} Fraenkel, A.S. (1969). The bracket function and complementary sets of integers. *Canadian Journal of Mathematics* 21, 6--27.

\cite{durand1998characterization} Durand, F. (1998). A characterization of substitutive sequences using return words. *Discrete Mathematics* 179, 89--101.

\cite{durand2003linearly} Durand, F. (2000). Linearly recurrent subshifts have a finite number of non-periodic subshift factors. *Ergodic Theory and Dynamical Systems* 20(4), 1061--1078.

\cite{cassaigne1999limit} Cassaigne, J. (1999). Limit values of the recurrence quotient of Sturmian sequences. *Theoretical Computer Science* 218(1), 3--12.

\cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences: Theory, Applications, Generalizations.* Cambridge University Press.

\cite{schaeffer2024beatty} Schaeffer, L., Shallit, J., and Zorcic, S. (2024). Beatty Sequences for a Quadratic Irrational: Decidability and Applications. arXiv:2402.08331.

\cite{skolem1934einige} Skolem, T. (1934). Ein Verfahren zur Behandlung gewisser exponentialer Gleichungen und diophantischer Gleichungen. *Comptes rendus du 8e Congres des Mathematiciens Scandinaves*, 163--188.

\cite{mahler1935arithmetische} Mahler, K. (1935). Uber das Verschwinden von Potenzreihen mehrerer Veranderlichen in speziellen Punktfolgen. *Mathematische Annalen* 103, 573--587.

\cite{lech1953note} Lech, C. (1953). A note on recurring series. *Arkiv for Matematik* 2(5), 417--421.

\cite{weyl1916gleichverteilung} Weyl, H. (1916). Uber die Gleichverteilung von Zahlen mod. Eins. *Mathematische Annalen* 77, 313--352.

\cite{lagrange1770continued} Lagrange, J.-L. (1770). *Additions au memoire sur la resolution des equations numeriques.* Proof that quadratic irrationals have eventually periodic continued fractions.

\cite{roth1955rational} Roth, K.F. (1955). Rational approximations to algebraic numbers. *Mathematika* 2(1), 1--20.

\cite{berlekamp1968algebraic} Berlekamp, E.R. (1968). *Algebraic Coding Theory.* McGraw-Hill, New York.

\cite{massey1969shift} Massey, J.L. (1969). Shift-register synthesis and BCH decoding. *IEEE Transactions on Information Theory* 15(1), 122--127.

---

*This document was prepared as part of the research project on Beatty sequences and homogeneous linear recurrence. All proofs are contained in the companion documents `results/rational_case_proof.md`, `results/irrational_case_proof.md`, and `results/main_characterization.md`. Computational results are in `results/large_scale_search.csv`, `results/baseline_metrics.csv`, and `results/theorem_validation.md`. Source code is in `src/beatty.py`, `src/recurrence_detector.py`, and `src/subsequence_search.py`. The bibliography is maintained in `sources.bib`.*
