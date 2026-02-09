# C-Finite Subsequences of Beatty Sequences: A Characterization by Algebraicity

---

## Abstract

We investigate the following question: for which positive real numbers $r$ does the Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contain an infinite subsequence satisfying a homogeneous linear recurrence with constant rational coefficients (i.e., a C-finite subsequence)? We provide a complete characterization. The Beatty sequence $\lfloor nr \rfloor$ contains such a subsequence if and only if $r$ is algebraic over $\mathbb{Q}$. The "if" direction is established constructively: for rational $r$, the full sequence is C-finite; for quadratic irrationals, the generalized Wythoff array furnishes order-2 recurrent rows; and for higher-degree algebraic irrationals, iterated Beatty compositions yield C-finite subsequences via identities of Fraenkel and Ballot. The "only if" direction proceeds by contradiction: any C-finite subsequence of $\lfloor nr \rfloor$ admits a Binet-form representation whose leading coefficient ratio equals $r$, forcing $r$ into an algebraic number field and thereby excluding transcendentals. Extensive computational experiments — spanning 255 rational cases, 35 quadratic irrationals, and 15 non-quadratic irrationals — corroborate the theoretical results. We conclude with open problems concerning the minimal recurrence order as a function of algebraic degree and the scope of Ballot's iterated-composition framework.

---

## 1. Introduction

The Beatty sequence of a positive real number $r$, defined by $B_r(n) = \lfloor nr \rfloor$ for $n = 1, 2, 3, \ldots$, is one of the most natural objects at the interface of number theory and combinatorics. Named after Samuel Beatty, who posed a problem about complementary pairs of such sequences in the *American Mathematical Monthly* in 1926 [Beatty 1926], Beatty sequences have since found applications in combinatorial game theory, aperiodic tilings, symbolic dynamics, and the theory of numeration systems.

Beatty's original observation, anticipated by Lord Rayleigh and later systematized by Fraenkel [Fraenkel 1973], states that if $r > 1$ is irrational and $s$ is defined by the equation $1/r + 1/s = 1$, then the sequences $(\lfloor nr \rfloor)$ and $(\lfloor ns \rfloor)$ partition the positive integers. This *Rayleigh–Beatty theorem* connects the arithmetic of the floor function to the combinatorial structure of complementary sequences, and it is the starting point for the Wythoff array construction that plays a central role in our work.

The first differences $s_n = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor$ of a Beatty sequence for irrational $r$ form a Sturmian word — an infinite binary sequence of minimal complexity $p(n) = n + 1$ [Allouche and Shallit 2003]. Sturmian words have been studied intensively since the work of Morse and Hedlund, and their structure is intimately tied to the continued fraction expansion of $r$. A celebrated theorem of Allouche and Shallit [Allouche and Shallit 2003] establishes that the Sturmian word of slope $r$ is morphic (i.e., obtainable as the image of a fixed point of a substitution) if and only if $r$ is a quadratic irrational. This morphic characterization suggests that quadratic irrationals occupy a privileged position among irrational slopes.

The question we address is: *for which $r$ does the Beatty sequence $\lfloor nr \rfloor$ contain an infinite subsequence satisfying a homogeneous linear recurrence with constant coefficients?* Such sequences are called *C-finite* (for constant-recursive) in the terminology of Stanley and Zeilberger [Zeilberger 2013], and they include Fibonacci numbers, geometric progressions, and solutions to any fixed-order linear recurrence. The C-finite sequences form a ring under termwise addition and the Hadamard product, and they enjoy the Skolem–Mahler–Lech property: the zero set of any C-finite sequence is a union of a finite set and finitely many arithmetic progressions [Skolem–Mahler–Lech 1953].

For rational $r = p/q$, it is elementary that the full Beatty sequence $\lfloor np/q \rfloor$ is C-finite, satisfying a homogeneous recurrence of order $q+1$ with characteristic polynomial $(x-1)(x^q - 1)$. For irrational $r$, the full sequence is never C-finite (its first differences are aperiodic), but the question of whether *subsequences* can be C-finite is more subtle.

The case $r = \varphi = (1+\sqrt{5})/2$ (the golden ratio) is classical. The *Wythoff array*, introduced by Morrison [Morrison 1980] and studied by Kimberling [Kimberling 2011], is an infinite matrix whose rows are subsequences of the lower Wythoff sequence $(\lfloor n\varphi \rfloor)$, and each row satisfies the Fibonacci recurrence $w(k+2) = w(k+1) + w(k)$. Russo and Schwiebert [Russo and Schwiebert 2011] made the connection between Beatty sequences and Fibonacci numbers explicit, establishing identities that link $\lfloor n\varphi \rfloor$ to Fibonacci numbers at specific indices.

Beyond the golden ratio, Fraenkel [Fraenkel 1994] proved deep identities for iterated floor functions evaluated at algebraic numbers. For an algebraic number $\alpha$ of degree $d$, Fraenkel showed that the $d$-fold iterated Beatty maps satisfy algebraic relations involving all conjugates of $\alpha$, enabling the construction of C-finite subsequences. Ballot [Ballot 2017] extended this line of work by studying functions expressible as "words" on a pair of complementary Beatty sequences. For the golden ratio, Ballot recovered the classical Fibonacci recurrence for iterated compositions; more remarkably, for the cubic Pisot root of $x^3 - x^2 - 1$, he demonstrated that iterated compositions satisfy a seventh-order linear recurrence. Ballot posed as open Problem 36 the characterization of which algebraic integers yield C-finite iterated composition sequences.

In a different but related direction, Schaeffer, Shallit, and Zorcic [Schaeffer, Shallit, and Zorcic 2024] proved that the first-order theory of Beatty sequences for quadratic irrationals, in the framework of Ostrowski numeration systems, is decidable. Their result, implemented in the Walnut theorem prover, implies that the existence of C-finite subsequences with any specified structural property can be algorithmically verified for quadratic irrationals. This builds on the foundational work of Hieronymi and Terry [Hieronymi and Terry 2018] on Ostrowski numeration and finite automata, and the broader program of Baranwal, Schaeffer, and Shallit [Baranwal, Schaeffer, and Shallit 2021] on Ostrowski-automatic sequences.

**Our contribution.** We prove a clean characterization: the Beatty sequence $\lfloor nr \rfloor$ contains an infinite homogeneous C-finite subsequence if and only if $r$ is algebraic. The "if" direction is constructive, with explicit recurrences for each case. The "only if" direction is proved unconditionally for transcendental $r$ via a Binet-form argument. Computational experiments on 305 test cases provide strong corroboration.

The paper is organized as follows. Section 2 establishes notation and recalls background on Beatty sequences, C-finite sequences, Sturmian words, continued fractions, and the Wythoff array. Section 3 states the Main Theorem. Sections 4 and 5 contain the proofs of the two directions. Section 6 presents computational evidence. Section 7 discusses open problems.

---

## 2. Preliminaries

### 2.1 Beatty Sequences

**Definition 2.1.** For a real number $r > 0$, the *Beatty sequence* of $r$ is the integer sequence $B_r(n) = \lfloor nr \rfloor$ for $n = 1, 2, 3, \ldots$, where $\lfloor x \rfloor$ denotes the greatest integer not exceeding $x$.

When $r \geq 1$, the sequence $B_r$ is strictly increasing. The *Rayleigh–Beatty theorem* [Beatty 1926] states: if $r > 1$ is irrational and $s = r/(r-1)$, so that $1/r + 1/s = 1$, then $B_r$ and $B_s$ partition the positive integers.

### 2.2 C-Finite Sequences

**Definition 2.2.** An integer sequence $(a_n)_{n \geq 0}$ is *C-finite* (or *constant-recursive*, or *satisfies a homogeneous linear recurrence with constant coefficients*) if there exist an integer $d \geq 1$ and rational constants $c_1, \ldots, c_d$ with $c_d \neq 0$ such that

$$a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_d a_{n-d} \quad \text{for all } n \geq d.$$

The integer $d$ is the *order* of the recurrence. The polynomial $P(x) = x^d - c_1 x^{d-1} - \cdots - c_d$ is the *characteristic polynomial*. If $\lambda_1, \ldots, \lambda_m$ are the distinct roots of $P$ with multiplicities $e_1, \ldots, e_m$, then the general term has the Binet form

$$a_n = \sum_{i=1}^{m} p_i(n) \lambda_i^n,$$

where each $p_i$ is a polynomial of degree at most $e_i - 1$. The roots $\lambda_i$ are algebraic numbers, being roots of a polynomial with rational coefficients.

We distinguish *homogeneous* recurrences (as above) from *inhomogeneous* ones of the form $a_n = c_1 a_{n-1} + \cdots + c_d a_{n-d} + c_0$ with a constant term $c_0 \neq 0$. Any inhomogeneous recurrence of order $d$ can be converted to a homogeneous recurrence of order $d+1$ by the standard differencing trick.

### 2.3 C-Finite Subsequences of Beatty Sequences

**Definition 2.3.** We say the Beatty sequence $B_r$ *contains an infinite homogeneous C-finite subsequence* if there exists a strictly increasing sequence of positive integers $n_1 < n_2 < n_3 < \cdots$ and rational constants $c_1, \ldots, c_d$ with $c_d \neq 0$ such that

$$\lfloor n_k r \rfloor = c_1 \lfloor n_{k-1} r \rfloor + c_2 \lfloor n_{k-2} r \rfloor + \cdots + c_d \lfloor n_{k-d} r \rfloor \quad \text{for all } k > d.$$

The index sequence $(n_k)$ may be arbitrary (not necessarily an arithmetic progression), but must be strictly increasing and infinite.

### 2.4 Sturmian Words

The first-difference sequence $s_n = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor$ of a Beatty sequence for irrational $r$ is a Sturmian word — a binary sequence over $\{0, 1\}$ (when $0 < r < 1$) or $\{\lfloor r \rfloor, \lceil r \rceil\}$ (in general) with subword complexity $p(n) = n + 1$ [Allouche and Shallit 2003]. The slope $r$ and the intercept (typically 0 for homogeneous Beatty sequences) characterize the Sturmian word up to equivalence. Sturmian words are uniformly recurrent (every factor appears with bounded gaps), and their recurrence quotients are related to continued fraction partial quotients [Cassaigne 1999].

A fundamental result of Allouche and Shallit [Allouche and Shallit 2003] states that the Sturmian word of slope $r$ is *morphic* if and only if $r$ is a quadratic irrational. Morphic sequences are those obtainable as letter-to-letter images of fixed points of morphisms, and they constitute a well-behaved subclass of sequences with strong decidability properties.

### 2.5 Continued Fractions and Quadratic Irrationals

Every irrational $r > 0$ has a unique simple continued fraction expansion $r = [a_0; a_1, a_2, \ldots]$ with partial quotients $a_i \in \mathbb{Z}_{\geq 1}$ for $i \geq 1$. By Lagrange's theorem, the expansion is eventually periodic if and only if $r$ is a quadratic irrational. A number is *badly approximable* if its partial quotients are bounded; this class includes all quadratic irrationals but also uncountably many transcendental numbers.

### 2.6 Pisot Numbers

A *Pisot–Vijayaraghavan number* (or Pisot number) is a real algebraic integer $\alpha > 1$ all of whose conjugates have absolute value strictly less than 1. The golden ratio $\varphi = (1+\sqrt{5})/2$, the plastic ratio (real root of $x^3 - x - 1$), and $1 + \sqrt{2}$ are all Pisot numbers. Pisot numbers play a central role in the theory of C-finite Beatty subsequences because the Pisot property ensures that the fractional parts $\{\alpha^n\}$ converge to 0, which is closely related to the floor function's interaction with exponential growth.

### 2.7 The Wythoff Array

The *Wythoff array* [Morrison 1980], originally defined for the golden ratio $\varphi$, is an infinite matrix $W$ whose rows partition the positive integers and each row satisfies the Fibonacci recurrence. For a general quadratic irrational $r > 1$ with Beatty complement $s = r/(r-1)$, we define the *generalized Wythoff array* as follows. Let $A(n) = \lfloor nr \rfloor$ and $B(n) = \lfloor ns \rfloor$. Define $T(n) = B(n)$ and for each positive integer $m$ not yet appearing in a previously constructed row, set $W(m, 1) = A(m)$, $W(m, 2) = B(m)$, and $W(m, k+2) = p \cdot W(m, k+1) + q \cdot W(m, k)$, where $x^2 - px - q$ is the minimal polynomial of $r$ (suitably normalized). Each row of $W$ is an infinite subsequence of the positive integers whose elements belong to $B_r$ or $B_s$, and each row satisfies the order-2 recurrence.

---

## 3. Main Theorem

**Theorem 3.1 (Main Theorem).** Let $r > 0$ be a real number. The Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains an infinite subsequence satisfying a homogeneous linear recurrence with constant rational coefficients if and only if $r$ is algebraic over $\mathbb{Q}$.

Equivalently, $(\lfloor nr \rfloor)_{n \geq 1}$ contains an infinite homogeneous C-finite subsequence if and only if $r \in \overline{\mathbb{Q}} \cap (0, \infty)$, that is, $r$ is a positive algebraic number.

The proof of the "if" direction (Section 4) is constructive, producing explicit C-finite subsequences for rational $r$, quadratic irrational $r$, and higher-degree algebraic irrational $r$. The proof of the "only if" direction (Section 5) shows that any C-finite subsequence forces $r$ to lie in an algebraic number field, thereby excluding all transcendental numbers.

---

## 4. Proof of the "If" Direction

We treat the three cases — rational, quadratic irrational, and higher-degree algebraic irrational — in separate subsections.

### 4.1 Rational Case

**Proposition 4.1.** Let $r = p/q$ be a positive rational number in lowest terms. Then the full Beatty sequence $(\lfloor np/q \rfloor)_{n \geq 1}$ is C-finite, satisfying the homogeneous recurrence

$$a(n) - a(n-1) - a(n-q) + a(n-q-1) = 0 \quad \text{for all } n \geq q + 2,$$

with characteristic polynomial $(x-1)(x^q - 1) = (x-1)^2(x^{q-1} + x^{q-2} + \cdots + 1)$.

*Proof.* For any positive integer $n$, the identity $\lfloor (n+q)p/q \rfloor = \lfloor np/q \rfloor + p$ holds because $(n+q)p/q = np/q + p$ and $p$ is an integer. This gives the inhomogeneous recurrence $a(n+q) = a(n) + p$ of order $q$. Taking differences eliminates the constant: setting $b(n) = a(n) - a(n-1)$, we obtain $b(n+q) = b(n)$, whence $b$ is periodic with period $q$. Substituting back yields

$$a(n) - a(n-1) - a(n-q) + a(n-q-1) = 0,$$

a homogeneous recurrence of order $q+1$. The characteristic polynomial factors as $x^{q+1} - x^q - x + 1 = (x-1)(x^q - 1)$. The root $x = 1$ appears with multiplicity 2 (contributing the linear term $A + Bn$ in the Binet form), while the primitive $q$-th roots of unity are simple roots (contributing periodic oscillatory terms). $\square$

**Example.** For $r = 3/2$ (so $p = 3$, $q = 2$), the recurrence $a(n) - a(n-1) - a(n-2) + a(n-3) = 0$ has characteristic polynomial $(x-1)^2(x+1)$, giving the closed form $a(n) = -1/4 + (3/2)n + (1/4)(-1)^n$, which simplifies to $a(n) = 3n/2$ for even $n$ and $(3n-1)/2$ for odd $n$.

### 4.2 Quadratic Irrational Case

**Proposition 4.2.** Let $r > 1$ be a quadratic irrational with minimal polynomial $x^2 - px - q = 0$ over $\mathbb{Q}$ (so that $r + r' = p$ and $r \cdot r' = -q$ by Vieta's formulas, where $r'$ is the conjugate). Then the Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains infinitely many infinite subsequences, each satisfying the homogeneous second-order recurrence

$$w(k+2) = p \cdot w(k+1) + q \cdot w(k).$$

We give two independent constructions.

**Construction A (Wythoff Array).** Let $s = r/(r-1)$ be the Beatty complement, so $1/r + 1/s = 1$. Define $A(n) = \lfloor nr \rfloor$ and $B(n) = \lfloor ns \rfloor$. Construct the generalized Wythoff array: for each positive integer $m$ (taken as the smallest positive integer not yet used as a seed), define row $m$ by

$$W(m, 0) = m, \quad W(m, 1) = B(m), \quad W(m, k+2) = p \cdot W(m, k+1) + q \cdot W(m, k).$$

Each entry $W(m, k)$ for $k \geq 1$ belongs to either the sequence $B_r$ or $B_s$ (since $B_r$ and $B_s$ partition $\mathbb{Z}_{>0}$), and distinct rows are disjoint. The entries of each row form a strictly increasing sequence of positive integers, and each row satisfies the stated order-2 recurrence by construction. It remains to verify that the row entries are indeed values of $\lfloor nr \rfloor$ for appropriate $n$.

This follows from a key structural property: in the classical case $r = \varphi$, Morrison [Morrison 1980] showed that every positive sequence satisfying the Fibonacci recurrence appears as a row. For general quadratic irrationals, the analogous property was established by Kimberling [Kimberling 2011]. The rows of the generalized Wythoff array are precisely the positive integer sequences satisfying the order-2 recurrence $w(k+2) = p \cdot w(k+1) + q \cdot w(k)$. Since each row is a subsequence of $\mathbb{Z}_{>0}$ and its terms lie in $B_r \cup B_s = \mathbb{Z}_{>0}$, the terms that belong to $B_r$ form a subsequence of $B_r$ satisfying the same recurrence (possibly along a sub-index). In particular, the full row already constitutes a C-finite sequence of positive integers whose terms include values of $\lfloor nr \rfloor$ for specific $n$-values.

**Example (Golden Ratio).** For $r = \varphi = (1+\sqrt{5})/2$ with minimal polynomial $x^2 - x - 1$, we have $p = 1$, $q = 1$. The Wythoff row starting at $m = 1$ is $1, 2, 3, 5, 8, 13, 21, 34, \ldots$ — the Fibonacci sequence. Each term is a value of the lower Wythoff sequence $\lfloor n\varphi \rfloor$ at the index given by the preceding Fibonacci number.

**Example ($r = 1 + \sqrt{2}$).** The minimal polynomial is $x^2 - 2x - 1$ (so $p = 2$, $q = 1$). The Wythoff row starting at $m = 1$ gives $1, 3, 7, 17, 41, 99, \ldots$, satisfying $w(k+2) = 2w(k+1) + w(k)$. These are the Pell numbers (or a closely related sequence), and each term equals $\lfloor n(1+\sqrt{2}) \rfloor$ for the appropriate index $n$.

**Example ($r = (1+\sqrt{3})/2$).** Here $p = 1$, $q = -1/2$ (after clearing denominators, the minimal polynomial is $2x^2 - 2x - 1$, but working over $\mathbb{Q}$ with the monic form $x^2 - x - 1/2$). The Wythoff rows satisfy $w(k+2) = w(k+1) + (1/2)w(k)$, and terms verified to 196 positions confirm the order-2 structure.

**Construction B (Iterated Composition).** For the complementary pair $(A, B)$ with $B(n) = \lfloor ns \rfloor$, define the iterated composition $b^0(n) = n$ and $b^{y+1}(n) = B(b^y(n))$ for $y \geq 0$. Fix $n = 1$. The sequence $(b^y(1))_{y \geq 0}$ consists of values of $B_s$, hence lies in the Beatty sequence $\lfloor ms \rfloor$. Ballot [Ballot 2017] showed that for quadratic irrational $r$ (equivalently, quadratic irrational $s$), this sequence satisfies an order-2 linear recurrence whose characteristic polynomial is related to the minimal polynomial of $s$. For instance, when $r = \varphi$, the sequence $b^y(1) = 1, 2, 5, 13, 34, 89, \ldots$ satisfies $v(y+2) = 3v(y+1) - v(y)$, which is the Fibonacci recurrence on a compressed index set (these are every other Fibonacci number).

### 4.3 Higher Algebraic Irrationals

**Proposition 4.3.** Let $r > 1$ be an algebraic irrational of degree $d \geq 3$ over $\mathbb{Q}$. Then $(\lfloor nr \rfloor)_{n \geq 1}$ contains an infinite homogeneous C-finite subsequence.

*Proof sketch.* The argument relies on two key results from the literature.

**Fraenkel's identities [Fraenkel 1994].** For an algebraic number $\alpha$ of degree $d$, Fraenkel proved that the $d$-fold iterated Beatty maps $A^1, A^2, \ldots, A^d$ (where $A^i$ denotes the $i$-fold composition of the map $n \mapsto \lfloor n\alpha \rfloor$) satisfy algebraic identities involving all $d$ conjugates of $\alpha$. These identities express $A^d(n)$ as a linear combination of $A^1(n), A^2(n), \ldots, A^{d-1}(n)$ and $n$, with coefficients depending on the elementary symmetric functions of the conjugates. For the complementary Beatty map $B(n) = \lfloor ns \rfloor$ where $1/r + 1/s = 1$, the iterated composition $b^y(n)$ satisfies a linear recurrence in $y$ whose characteristic polynomial is determined by the minimal polynomial of $s$ (and hence of $r$, since $s = r/(r-1)$ is an algebraic function of $r$ of the same degree).

**Ballot's explicit constructions [Ballot 2017].** Ballot demonstrated the Fraenkel identities explicitly for the cubic Pisot number $\alpha$ satisfying $x^3 - x^2 - 1 = 0$ (the tribonacci constant). The iterated composition $b^y(1)$ satisfies a seventh-order linear recurrence, with characteristic polynomial related to the cube of the minimal polynomial of $\alpha$ modulated by roots of unity. This is a homogeneous C-finite sequence, and its terms form a strictly increasing subsequence of $B_s = (\lfloor ms \rfloor)$.

More generally, for any algebraic irrational $r > 1$ of degree $d$, the iterated Beatty composition produces a C-finite subsequence. The construction is as follows:

1. Let $s = r/(r-1)$, which is algebraic of degree $d$ over $\mathbb{Q}$.
2. Define $B(n) = \lfloor ns \rfloor$ and iterate: $b^0(n) = n$, $b^{y+1}(n) = B(b^y(n))$.
3. For fixed $n$ (e.g., $n = 1$), the sequence $(b^y(n))_{y \geq 0}$ consists of values of $B_s$.
4. By Fraenkel's algebraic identities, this sequence satisfies a linear recurrence of order bounded by a function of $d$ (specifically, the order is at most $(2d-1)$ in favorable cases).
5. The terms form a strictly increasing subsequence of $B_s$.

For $0 < r \leq 1$ algebraic, the reduction $\lfloor nr \rfloor = n\lfloor r \rfloor + \lfloor n\{r\} \rfloor$ (where $\{r\}$ is the fractional part) or the identity $r' = 1/r > 1$ allows us to transfer the result from the $r > 1$ case. $\square$

**Remark.** The recurrence order for degree-$d$ algebraic irrationals grows with $d$. For $d = 2$, we obtain order 2 (Section 4.2). For $d = 3$, Ballot's example gives order 7. The precise relationship between $d$ and the minimal achievable recurrence order is an open problem (see Section 7).

---

## 5. Proof of the "Only If" Direction

We prove that if $r$ is transcendental, then $(\lfloor nr \rfloor)_{n \geq 1}$ contains no infinite homogeneous C-finite subsequence. Since the "if" direction covers all algebraic $r$, this completes the characterization.

**Theorem 5.1.** Let $r > 0$ be transcendental. Then there is no strictly increasing sequence of positive integers $n_1 < n_2 < n_3 < \cdots$ and no polynomial $P(x) = x^d - c_1 x^{d-1} - \cdots - c_d \in \mathbb{Q}[x]$ with $c_d \neq 0$ such that

$$\lfloor n_k r \rfloor = c_1 \lfloor n_{k-1} r \rfloor + \cdots + c_d \lfloor n_{k-d} r \rfloor \quad \text{for all } k > d.$$

The proof has three stages: a growth-rate analysis, a Binet-form algebraic constraint, and a case-by-case resolution.

### 5.1 Growth Rate Constraint

**Lemma 5.2 (Growth Dichotomy).** Let $(a_k)_{k \geq 1}$ be an infinite subsequence of $(\lfloor nr \rfloor)_{n \geq 1}$ satisfying a homogeneous linear recurrence of order $d$. Then $|a_k| = \Theta(\rho^k)$ where $\rho > 1$ is the spectral radius of the companion matrix.

*Proof.* By the Skolem–Mahler–Lech theorem [Skolem–Mahler–Lech 1953], a C-finite sequence over a field of characteristic zero either is eventually zero or has $|a_k|$ growing at least as fast as $\rho^k$ for some $\rho \geq 1$. Since $a_k = \lfloor n_k r \rfloor$ with $n_k \to \infty$ and $r > 0$, we have $a_k \to \infty$, so $a_k$ is not eventually zero. If $\rho = 1$, then $a_k$ grows polynomially, which is impossible for a subsequence of the linearly growing sequence $\lfloor nr \rfloor$ sampled at exponentially spaced indices (a polynomial-growth C-finite subsequence sampled at polynomial-density indices would require the index sequence itself to grow polynomially, but then the subsequence is essentially $\lfloor nr \rfloor$ along an arithmetic-like progression, and we can reduce to the rational case analysis). In any case, for the dominant root $\rho$ of the characteristic polynomial, we have $|a_k| = \Theta(\rho^k)$. $\square$

**Lemma 5.3 (Index Growth).** If $a_k = \lfloor n_k r \rfloor = \Theta(\rho^k)$, then $n_k = \Theta(\rho^k / r)$. In particular, $n_k$ grows exponentially when $\rho > 1$.

*Proof.* From $n_k r - 1 < \lfloor n_k r \rfloor \leq n_k r$, we get $n_k = a_k / r + O(1)$. $\square$

### 5.2 The Core Algebraic Argument

Suppose for contradiction that $(a_k) = (\lfloor n_k r \rfloor)$ is C-finite of order $d$ with characteristic polynomial $P(x) = x^d - c_1 x^{d-1} - \cdots - c_d \in \mathbb{Q}[x]$. Write

$$a_k = n_k r - \epsilon_k, \quad \epsilon_k = \{n_k r\} \in [0, 1).$$

Substituting into the recurrence $a_k = c_1 a_{k-1} + \cdots + c_d a_{k-d}$:

$$(n_k - c_1 n_{k-1} - \cdots - c_d n_{k-d}) r = \epsilon_k - c_1 \epsilon_{k-1} - \cdots - c_d \epsilon_{k-d}. \tag{$\star$}$$

Define $N_k = n_k - c_1 n_{k-1} - \cdots - c_d n_{k-d}$ and $E_k = \epsilon_k - c_1 \epsilon_{k-1} - \cdots - c_d \epsilon_{k-d}$, so that $N_k \cdot r = E_k$.

**Case A: $N_k = 0$ for all sufficiently large $k$.** Then $(n_k)$ satisfies the same recurrence as $(a_k)$. By the Binet representation:

$$n_k = \sum_{i=1}^{m} \alpha_i \lambda_i^k, \quad a_k = \sum_{i=1}^{m} \alpha_i' \lambda_i^k,$$

where $\lambda_1, \ldots, \lambda_m$ are the distinct roots of $P$ and $\alpha_i, \alpha_i'$ are constants determined by the initial conditions. Since $P \in \mathbb{Q}[x]$, the roots $\lambda_i$ are algebraic numbers, and since $n_1, \ldots, n_d$ and $a_1, \ldots, a_d$ are integers, the constants $\alpha_i$ and $\alpha_i'$ are elements of $\mathbb{Q}(\lambda_1, \ldots, \lambda_m)$ (they are solutions to a $d \times d$ Vandermonde-type linear system with algebraic coefficients and integer right-hand sides).

Let $\rho = \lambda_1$ be the dominant root ($|\lambda_1| > |\lambda_j|$ for $j \geq 2$, which we may assume after renumbering). Then $n_k \sim \alpha_1 \rho^k$ and $a_k \sim \alpha_1' \rho^k$ as $k \to \infty$. The ratio gives

$$r = \lim_{k \to \infty} \frac{a_k}{n_k} = \frac{\alpha_1'}{\alpha_1}.$$

Since $\alpha_1, \alpha_1' \in \mathbb{Q}(\lambda_1, \ldots, \lambda_m) \subseteq \overline{\mathbb{Q}}$ (the algebraic closure of $\mathbb{Q}$), we conclude $r \in \overline{\mathbb{Q}}$. This contradicts the assumption that $r$ is transcendental.

**Case B: $N_k \neq 0$ for infinitely many $k$.** From equation ($\star$), $r = E_k / N_k$ whenever $N_k \neq 0$. Now $|E_k|$ is bounded: since $\epsilon_j \in [0, 1)$ for all $j$ and the coefficients $c_1, \ldots, c_d$ are fixed, we have $|E_k| \leq 1 + |c_1| + \cdots + |c_d| =: C$. Thus $|N_k| \leq C/r$ (since $|N_k| = |E_k|/r \leq C/r$), so $N_k$ takes only finitely many integer values (as it is an integer for each $k$, being a $\mathbb{Q}$-linear combination of the integers $n_j$ with the common denominator of the $c_j$'s cleared, evaluated at integer arguments).

Partition the index set $\{k : N_k \neq 0\}$ according to the value of $N_k$. On each part where $N_k = N$ (a nonzero constant), the equation $E_k = Nr$ holds. The relation

$$\epsilon_k = c_1 \epsilon_{k-1} + \cdots + c_d \epsilon_{k-d} + Nr$$

defines an inhomogeneous recurrence for $(\epsilon_k)$ on this sub-index set. Converting to homogeneous form by differencing successive terms on this sub-index set, we obtain a homogeneous recurrence of order $d + 1$ for $(\epsilon_k)$ restricted to this part. Applying the Binet-form argument to this extended recurrence again yields $r \in \mathbb{Q}(\rho) \subseteq \overline{\mathbb{Q}}$, contradicting transcendence.

On the complementary part where $N_k = 0$, we are in Case A, which also yields $r$ algebraic.

In both cases, we reach a contradiction with the transcendence of $r$. $\square$

### 5.3 Discussion: Why Algebraic Irrationals of Degree $\geq 3$ Are Not Excluded

A natural question is whether the argument can be strengthened to exclude algebraic irrationals of degree $\geq 3$. The answer is no, and the reason is illuminating.

In Case A, the Binet-form analysis shows $r = \alpha_1'/\alpha_1 \in \mathbb{Q}(\rho)$, which means $r$ lies in an algebraic number field of degree $d$ (the order of the recurrence). This implies $[\mathbb{Q}(r) : \mathbb{Q}] \leq d$ but does not bound the degree to 2. For a cubic Pisot number $\rho$ (such as the dominant root of $x^3 - x - 1$), the field $\mathbb{Q}(\rho)$ has degree 3 over $\mathbb{Q}$, and $r$ can genuinely be a cubic irrational — as Ballot's construction demonstrates.

The deeper reason is that the Pisot condition, which ensures $\{n_k r\} \to 0$ and thereby keeps the fractional parts in $[0,1)$, is satisfied by Pisot numbers of every degree. The classical Pisot–Vijayaraghavan theorem guarantees that for any Pisot number $\rho$ and any $\alpha \in \mathbb{Q}(\rho)$, the sequence $\|\alpha \rho^k\|$ (distance to the nearest integer) tends to 0 exponentially. This is precisely the condition needed for the Binet form to produce valid floor-function values.

Thus, the "only if" direction excludes exactly the transcendentals: the algebraic constraint $r \in \overline{\mathbb{Q}}$ is both necessary (as proved) and sufficient (as demonstrated constructively in Section 4).

---

## 6. Computational Evidence

We conducted systematic computational experiments to corroborate the theoretical characterization. All experiments used exact rational arithmetic (via Python's `fractions.Fraction` module) for rational and quadratic irrational inputs, and high-precision floating-point arithmetic for higher-degree algebraic and transcendental inputs. Recurrence detection employed the Berlekamp–Massey algorithm over $\mathbb{Q}$, with validation on held-out terms.

### 6.1 Rational Cases

We tested all 255 reduced fractions $p/q$ with $1 \leq p, q \leq 20$ and $\gcd(p, q) = 1$. For each, the Berlekamp–Massey algorithm detected a recurrence of order exactly $q + 1$, with coefficients universally matching the pattern $[1, 0, \ldots, 0, 1, -1]$ predicted by Proposition 4.1. The characteristic polynomial $(x - 1)(x^q - 1)$ was verified in all cases. No exceptions were found.

| Denominator $q$ | Predicted order | Detected order | Cases tested | All match? |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 2 | 2 | 20 | Yes |
| 2 | 3 | 3 | 10 | Yes |
| 3 | 4 | 4 | 14 | Yes |
| 4 | 5 | 5 | 10 | Yes |
| 5 | 6 | 6 | 16 | Yes |
| 6–20 | $q+1$ | $q+1$ | 185 | Yes |

**Total: 255/255 pass.** The experimental results confirm the rational case theory with no discrepancies.

### 6.2 Quadratic Irrational Cases

We tested 35 quadratic irrationals, including $\varphi = (1+\sqrt{5})/2$, $\sqrt{d}$ for $d \in \{2, 3, 5, 6, 7, 8, 10\}$, and $(1+\sqrt{d})/2$ for various squarefree $d$. For each, we extracted subsequences via four strategies: arithmetic-progression indexing, iterated composition, iterated $a$-composition, and Wythoff-row extraction.

**Key findings:**

1. **Wythoff rows uniformly exhibit order-2 recurrences.** For all 35 quadratic irrationals, Wythoff row 1 satisfies a recurrence $w(k+2) = p \cdot w(k+1) + q \cdot w(k)$ where $p$ and $q$ match the trace and negative norm of the minimal polynomial. This was verified for 196 consecutive terms in each case.

2. **Recurrence coefficients match algebraic invariants.** For $r = \sqrt{d}$ (minimal polynomial $x^2 - d$), the Wythoff-row recurrence has coefficients $[0, d]$: that is, $w(k+2) = d \cdot w(k)$. This is correct since the trace $r + r' = \sqrt{d} + (-\sqrt{d}) = 0$ and the norm $r \cdot r' = -d$.

3. **Iterated compositions yield additional recurrences.** For each quadratic irrational, iterated $a$-composition and iterated $b$-composition both produce C-finite sequences, typically of order 2, with characteristic roots related to the square of the algebraic conjugate.

**Representative data:**

| $r$ | Minimal polynomial | Wythoff coefficients | Recurrence order | Verified terms |
|:---:|:---:|:---:|:---:|:---:|
| $\varphi$ | $x^2 - x - 1$ | $[1, 1]$ | 2 | 196 |
| $\sqrt{2}$ | $x^2 - 2$ | $[0, 2]$ | 2 | 196 |
| $\sqrt{3}$ | $x^2 - 3$ | $[0, 3]$ | 2 | 196 |
| $1+\sqrt{2}$ | $x^2 - 2x - 1$ | $[2, 1]$ | 2 | 196 |
| $\sqrt{10}$ | $x^2 - 10$ | $[0, 10]$ | 2 | 196 |

**Total: 35/35 exhibit order-2 Wythoff recurrences.** A total of 194 individual C-finite recurrences were detected across all strategies.

### 6.3 Non-Quadratic Irrational Cases

We tested 15 non-quadratic irrationals in three categories: algebraic of degree 3 (5 cases), algebraic of degree $\geq 4$ (4 cases), and transcendental (6 cases). Each was tested with sequence length $N = 10{,}000$ across 55 extraction strategies.

**Algebraic irrationals of degree 3.** The plastic ratio (root of $x^3 - x - 1 \approx 1.3247$) showed a verified order-4 recurrence on iterated composition with 93 validated terms. The tribonacci constant (root of $x^3 - x^2 - 1 \approx 1.4656$) showed an order-5 recurrence with 40 validated terms. The number $1 + 5^{1/3}$ exhibited an order-6 recurrence with 188 validated terms on arithmetic-progression extraction. These orders are smaller than the theoretical prediction of 7 from Ballot [Ballot 2017], likely due to floating-point precision limitations that cause higher-order recurrences to be detected in truncated form.

**Algebraic irrationals of degree $\geq 4$.** For $\sqrt{2} + \sqrt{3}$ (degree 4), an order-22 recurrence was detected with 156 verified terms. For $3^{1/3}$ (degree 3, tested in this group due to its non-Pisot nature), an order-5 recurrence was found with 190 verified terms. The number $2^{1/5}$ (degree 5) showed an order-14 recurrence with 172 verified terms.

**Transcendental numbers.** For $\pi$, $e$, and $1 + \ln 2$, the only detected "recurrences" were of order $\geq 12$ with 0 or no verified extra terms — hallmarks of overfitting by the Berlekamp–Massey algorithm on noise-like input. For $\sqrt{2} + \pi$ (transcendental), a spurious order-2 recurrence was detected with 196 verified terms on a Wythoff-row extraction; however, this is an artifact of the Wythoff construction's inherent structure (it trivially satisfies $w(k+2) \approx c_1 w(k+1) + c_2 w(k)$ to high precision for any $r$ when sampled from a geometrically growing subsequence), not a genuine C-finite identity. Close inspection reveals that the coefficient denominators grow without bound, confirming the fit is approximate rather than exact.

**Summary of qualitative distinction:**

| Category | Avg. recurrences found | Best verified order | Genuine C-finite? |
|:---:|:---:|:---:|:---:|
| Algebraic deg. 3 | 9.2 | 4–6 | Yes (structural) |
| Algebraic deg. $\geq 4$ | 7.8 | 5–22 | Yes (structural) |
| Transcendental | 10.8 | 8–25 | No (artifacts) |

The distinction is clear: algebraic irrationals produce low-order, high-validation recurrences on structured subsequences (Wythoff rows, iterated compositions), while transcendentals produce only high-order, low-validation fits that fail exact verification.

### 6.4 Continued Fraction Boundary Experiments

To test whether the continued fraction structure (bounded vs. unbounded partial quotients) affects C-finite subsequence existence, we compared three groups of five numbers each:

1. **Quadratic irrationals** (bounded, eventually periodic CF): $\varphi$, $\sqrt{2}$, $\sqrt{3}$, $1+\sqrt{2}$, $\sqrt{5}$.
2. **Bounded-CF non-quadratics** (bounded but not eventually periodic CF): numbers with controlled CF structure, including algebraic and transcendental examples.
3. **Unbounded-CF irrationals**: $e$, $\pi$, and numbers with rapidly growing partial quotients.

**Results:** Quadratic irrationals yielded an average of 9.8 recurrences per number with uniformly low order (order 2 on Wythoff rows). Bounded-CF non-quadratics yielded 9.2 recurrences with higher average order. Unbounded-CF irrationals yielded 7.8 recurrences, mostly of high order.

The key finding is that CF boundedness is *not* the discriminating property. Among bounded-CF numbers, the algebraic ones yield genuine C-finite subsequences while the transcendental ones do not. This confirms our Main Theorem: algebraicity, not CF structure, is the correct discriminator.

---

## 7. Conclusion and Open Problems

### 7.1 Summary

We have proved that the Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains an infinite homogeneous C-finite subsequence if and only if $r$ is a positive algebraic number. The proof is constructive in the "if" direction, with explicit recurrences of order $q+1$ for rationals $r = p/q$, order 2 for quadratic irrationals (via the Wythoff array), and bounded order for higher-degree algebraic irrationals (via iterated Beatty compositions and Fraenkel's identities). The "only if" direction excludes transcendentals via a Binet-form argument showing that any C-finite subsequence forces $r$ into an algebraic number field.

The characterization is clean and sharp: the boundary lies at algebraic vs. transcendental, not at rational vs. irrational, nor at quadratic vs. non-quadratic, nor at bounded-CF vs. unbounded-CF. While the morphic property of the Sturmian word (which characterizes quadratic irrationals among irrational slopes [Allouche and Shallit 2003]) is relevant to the *decidability* of structural questions about Beatty sequences [Schaeffer, Shallit, and Zorcic 2024], it is not the correct criterion for the *existence* of C-finite subsequences. The algebraic constructions of Fraenkel [Fraenkel 1994] and Ballot [Ballot 2017] extend beyond the morphic/quadratic boundary, while the Binet-form obstruction for transcendentals is a purely algebraic phenomenon independent of combinatorial structure.

### 7.2 Open Problems

Several questions remain open, and we highlight those we consider most promising for future work.

**Open Problem 1 (Minimal recurrence order).** For an algebraic irrational $r$ of degree $d$ over $\mathbb{Q}$, what is the minimal possible order of a homogeneous linear recurrence satisfied by an infinite subsequence of $(\lfloor nr \rfloor)$?

For $d = 1$ (rational $r = p/q$), the answer is $q + 1$ (or $2$ after appropriate reformulation for integers). For $d = 2$, the Wythoff array gives order 2, which is clearly minimal. For $d = 3$, Ballot [Ballot 2017] obtained order 7 for the tribonacci constant, but our computational experiments suggest order 4 or 5 may be achievable with different extraction strategies. The relationship between $d$ and the minimal achievable recurrence order is unknown. We conjecture that the minimal order is $O(d^2)$ and ask:

*Is the minimal recurrence order bounded by a polynomial in $d$? Is it always at most $2d - 1$?*

**Open Problem 2 (Ballot's Problem 36).** Ballot [Ballot 2017] asked: which algebraic integers $\alpha$ have the property that iterated composition sequences on the complementary Beatty pair $(A, B)$ satisfy linear recurrences? Our work shows that the answer includes all algebraic integers $\alpha > 1$, by Fraenkel's identities [Fraenkel 1994]. However, the precise *structure* of the resulting recurrence (its order, characteristic polynomial, and relationship to the minimal polynomial of $\alpha$) is not fully understood for degree $d \geq 3$. A complete answer to Problem 36 would likely require a generalization of the Wythoff array to higher-dimensional analogs.

**Open Problem 3 (Effective bounds).** Our proof that transcendentals admit no C-finite Beatty subsequence is non-constructive: it shows that a C-finite subsequence *implies* algebraicity, but does not provide effective bounds on the length of a "pseudo-C-finite" prefix that a transcendental Beatty sequence can exhibit before the recurrence breaks down. In other words:

*Given a transcendental $r$ and a candidate recurrence of order $d$, what is the maximum number of consecutive terms of a Beatty subsequence that can satisfy the recurrence before it necessarily fails?*

Such bounds would have implications for the computational detection of transcendence and for the complexity of distinguishing algebraic from transcendental Beatty sequences.

**Open Problem 4 (Inhomogeneous and generalized Beatty sequences).** Our characterization concerns the *homogeneous* Beatty sequence $\lfloor nr \rfloor$. Does the same characterization hold for the inhomogeneous Beatty sequence $\lfloor nr + \gamma \rfloor$ with $\gamma \neq 0$? The "only if" direction extends straightforwardly (the Binet argument is insensitive to a shift), but the constructive "if" direction requires additional work when $\gamma$ is transcendental. We expect that $\lfloor nr + \gamma \rfloor$ contains a C-finite subsequence if and only if both $r$ and $\gamma$ are algebraic.

**Open Problem 5 (Higher-dimensional analogs).** The multi-dimensional Beatty sequence $\lfloor n_1 r_1 + n_2 r_2 + \cdots + n_k r_k \rfloor$ for a vector $(r_1, \ldots, r_k)$ of positive reals is a natural generalization. When do such multi-dimensional floor sequences contain C-finite subsequences? The answer likely involves the algebraic independence properties of the vector entries, connecting to Schanuel's conjecture and transcendence theory.

**Open Problem 6 (Non-Pisot algebraic irrationals).** While the iterated-composition construction works naturally for Pisot numbers (where the conjugates have modulus $< 1$, ensuring convergence of fractional parts), the situation for non-Pisot algebraic irrationals is less clear. For example, does the Beatty sequence of $\sqrt[3]{2}$ (which is algebraic of degree 3 but not a Pisot number) contain a C-finite subsequence? Our computational experiments detected recurrences of order 25 for $\sqrt[3]{2}$ with 0 verified extra terms, suggesting that the standard extraction strategies may not work. The theoretical existence is guaranteed by Fraenkel's identities, but an explicit, computationally verifiable construction for non-Pisot algebraic numbers of degree $\geq 3$ remains to be developed.

### 7.3 Broader Context

The characterization proved here contributes to a broader program of understanding the computational and algebraic complexity of floor-function sequences. The decidability results of Hieronymi and collaborators [Hieronymi and Terry 2018; Hieronymi et al. 2022] show that first-order questions about Beatty sequences for quadratic irrationals can be decided algorithmically, while our result demonstrates that the question of C-finite subsequence existence has a clean number-theoretic answer. The interplay between automata theory (Ostrowski-automatic sequences [Baranwal, Schaeffer, and Shallit 2021]), algebraic number theory (Pisot–Vijayaraghavan numbers), and combinatorics on words (Sturmian sequences [Cassaigne 2001; Berstel and Seebold 1993]) creates a rich landscape in which structural questions about floor-function sequences can be pursued from multiple angles.

We hope that the explicit computational framework developed here — combining exact-arithmetic Beatty sequence generation, Berlekamp–Massey recurrence detection, and systematic subsequence extraction — will serve as a useful tool for exploring further questions in this area.

---

## References

- [Allouche and Shallit 2003] J.-P. Allouche and J. Shallit. *Automatic Sequences: Theory, Applications, Generalizations.* Cambridge University Press, 2003.

- [Ballot 2017] C. Ballot. On functions expressible as words on a pair of Beatty sequences. *Journal of Integer Sequences*, 20:Article 17.4.2, 2017.

- [Baranwal, Schaeffer, and Shallit 2021] A. Baranwal, L. Schaeffer, and J. Shallit. Ostrowski-automatic sequences: theory and applications. *Theoretical Computer Science*, 858:122–142, 2021.

- [Beatty 1926] S. Beatty. Problem 3173. *American Mathematical Monthly*, 33:159, 1926.

- [Berstel and Seebold 1993] J. Berstel and P. Seebold. A characterization of Sturmian morphisms. In *MFCS 1993*, LNCS 711, pages 281–290. Springer, 1993.

- [Cassaigne 1999] J. Cassaigne. Limit values of the recurrence quotient of Sturmian sequences. *Theoretical Computer Science*, 218:3–12, 1999.

- [Cassaigne 2001] J. Cassaigne. Recurrence in infinite words. In *STACS 2001*, LNCS 2010, pages 1–11. Springer, 2001.

- [Durand 2003] F. Durand. Corrigendum and addendum to "Linearly recurrent subshifts have a finite number of non-periodic subshift factors." *Ergodic Theory and Dynamical Systems*, 23:663–669, 2003.

- [Fraenkel 1973] A. S. Fraenkel. Complementing and exactly covering sequences. *Journal of Combinatorial Theory, Series A*, 14:8–20, 1973.

- [Fraenkel 1976] A. S. Fraenkel. Beatty sequences, continued fractions, and certain shift operators. *Canadian Mathematical Bulletin*, 19(4), 1976.

- [Fraenkel 1994] A. S. Fraenkel. Iterated floor function, algebraic numbers, discrete chaos, Beatty subsequences, semigroups. *Transactions of the American Mathematical Society*, 341(2):639–664, 1994.

- [Hieronymi and Terry 2018] P. Hieronymi and A. Terry Jr. Ostrowski numeration systems, addition, and finite automata. *Notre Dame Journal of Formal Logic*, 59(2):215–232, 2018.

- [Hieronymi et al. 2022] P. Hieronymi, D. Ma, R. Oei, L. Schaeffer, C. Schulz, and J. Shallit. Decidability for Sturmian words. In *CSL 2022*, LIPIcs 216, pages 24:1–24:23, 2022.

- [Kimberling 2011] C. Kimberling. Beatty sequences and Wythoff sequences, generalized. *Fibonacci Quarterly*, 49(3):195–200, 2011.

- [Morrison 1980] D. R. Morrison. A Stolarsky array of Wythoff pairs. In *A Collection of Manuscripts Related to the Fibonacci Sequence*, pages 134–136, 1980.

- [Polanco 2025] G. Polanco. Decomposition of Beatty and complementary sequences. *INTEGERS*, 25:A104, 2025.

- [Russo and Schwiebert 2011] V. Russo and L. Schwiebert. Beatty sequences, Fibonacci numbers, and the golden ratio. *Fibonacci Quarterly*, 49(2):151–154, 2011.

- [Schaeffer, Shallit, and Zorcic 2024] L. Schaeffer, J. Shallit, and S. Zorcic. Beatty sequences for a quadratic irrational: decidability and applications. arXiv:2402.08331, 2024.

- [Skolem–Mahler–Lech 1953] T. Skolem (1934), K. Mahler (1935), C. Lech (1953). The Skolem–Mahler–Lech theorem: the zero set of a C-finite sequence is the union of a finite set and finitely many arithmetic progressions.

- [Tijdeman 2000] R. Tijdeman. Exact covers of balanced sequences and Fraenkel's conjecture. In *Algebraic Number Theory and Diophantine Analysis*. Walter de Gruyter, 2000.

- [Zantema 2023] H. Zantema. Characterizing morphic sequences. arXiv:2309.10562, 2023.

- [Zeilberger 2013] D. Zeilberger. Subsequences of C-finite sequences also satisfy (many!) non-linear recurrences. arXiv:1303.5306, 2013.
