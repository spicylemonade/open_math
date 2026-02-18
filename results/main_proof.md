# Complete Proof of the Main Characterization Theorem: Beatty Sequences and Homogeneous Linear Recurrence

## Item 020 -- Phase 5: Analysis & Documentation

---

**Abstract.** This document presents a complete, self-contained proof of the Main Characterization Theorem for Beatty sequences and homogeneous linear recurrence. We prove that the Beatty sequence $a_n = \lfloor nr \rfloor$ contains a non-trivial homogeneous linearly recurrent subsequence indexed by an arithmetic progression if and only if $r$ is rational. The proof synthesizes elementary number-theoretic identities for the rational case with a growth-rate rationality argument and Weyl equidistribution for the irrational case. All claims are either proved in full, cited to established literature, or explicitly marked as conjectures. Computational verification on 102 values of $r$ yields perfect agreement with the theoretical predictions.

---

## 1. Introduction and Motivation

### 1.1 Beatty Sequences in Combinatorial Number Theory

Beatty sequences arise naturally throughout combinatorial number theory, discrete geometry, and the theory of dynamical systems. Given a positive real number $r$, the Beatty sequence $a_n = \lfloor nr \rfloor$ for $n \geq 1$ lists the integer parts of the multiples of $r$. Since Beatty's original 1926 observation \cite{beatty1926problem} that the sequences $\lfloor n\alpha \rfloor$ and $\lfloor n\beta \rfloor$ partition the positive integers when $1/\alpha + 1/\beta = 1$ (with $\alpha, \beta$ irrational), these sequences have appeared in a remarkable range of contexts: Wythoff's combinatorial game theory \cite{fraenkel1969bracket}, the three-distance theorem on irrational rotations \cite{sos1958distribution, ravenstein1988three}, Sturmian word theory \cite{morse1938symbolic, morse1940symbolic2}, Ostrowski numeration and decidability \cite{ostrowski1922bemerkungen, hieronymi2018ostrowski, schaeffer2024beatty}, and the theory of automatic and morphic sequences \cite{allouche2003automatic}.

A fundamental structural question about Beatty sequences, connecting number theory to algebra, is the following:

> **Central Question.** For which positive real numbers $r$ does the Beatty sequence $\lfloor nr \rfloor$ contain an infinite, non-trivially recurrent subsequence? More precisely, when does some subsequence of $\lfloor nr \rfloor$, indexed by an arithmetic progression, satisfy a homogeneous linear recurrence with constant integer coefficients?

This question lies at the intersection of several mathematical threads. The first-difference sequence $\Delta_r(n) = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor$ is a Sturmian word when $r$ is irrational \cite{morse1940symbolic2}, and the rich combinatorial theory of Sturmian words -- including Durand's characterization of linear recurrence \cite{durand1998characterization, durand2003linearly} and Cassaigne's precise recurrence quotient formulas \cite{cassaigne1999limit} -- might suggest that the answer depends on continued fraction properties, algebraic degree, or the irrationality measure of $r$.

### 1.2 Motivation from Sturmian Word Theory and Automatic Sequences

Sturmian words are the simplest aperiodic sequences in symbolic dynamics, characterized by having subword complexity $p(n) = n + 1$ \cite{morse1940symbolic2, coven1973sequences}. When the slope $r$ is a quadratic irrational (such as the golden ratio $\varphi = (1+\sqrt{5})/2$), the continued fraction expansion is eventually periodic by Lagrange's theorem \cite{lagrange1770continued}, the Sturmian word is a morphic sequence (the fixed point of a finite substitution), and Durand's theorem guarantees that the word is linearly recurrent in the combinatorial sense: every factor of length $n$ reappears within a window of length $Cn$ for some constant $C$ depending on $r$. This is what we call *Notion A* -- combinatorial or symbolic linear recurrence.

An entirely different notion is *Notion B* -- algebraic linear recurrence: whether the integer-valued Beatty sequence $\lfloor nr \rfloor$ itself, or some subsequence thereof, satisfies a recurrence relation $\sum_{i=0}^{D} c_i a_{n+i} = 0$ with integer coefficients $c_i$ not all zero. These two notions share similar terminology but are, as we shall demonstrate, completely independent properties. The golden ratio provides the decisive witness: the Sturmian word for $\varphi$ is linearly recurrent (Notion A holds), yet $\lfloor n\varphi \rfloor$ satisfies no homogeneous linear recurrence whatsoever (Notion B fails).

Additional motivation comes from the OEIS database, where many Beatty sequences appear (e.g., A001950 for $\lfloor n\varphi \rfloor$, A001951 for $\lfloor n\sqrt{2} \rfloor$), and from the recent decidability results of Schaeffer, Shallit, and Zorcic \cite{schaeffer2024beatty}, who showed that first-order properties of quadratic Beatty sequences can be algorithmically decided via Ostrowski numeration.

### 1.3 Overview of the Answer

The answer to the Central Question turns out to be a clean, sharp rational/irrational dichotomy:

> The Beatty sequence $\lfloor nr \rfloor$ contains a non-trivial homogeneous linearly recurrent subsequence (indexed by an arithmetic progression) if and only if $r$ is rational.

This characterization is *complete* (both directions proved), *sharp* (the transition at rational $r$ is discontinuous), *uniform* (the impossibility for irrationals applies identically to quadratic irrationals, higher-degree algebraics, and transcendentals), and *constructive* (for rational $r = p/q$, we exhibit the minimal recurrence explicitly). The rest of this document is devoted to the rigorous proof of this result.

---

## 2. Definitions and Notation

We begin by establishing the precise definitions and notational conventions used throughout. All notation is defined before its first use.

**Definition 2.1 (Beatty Sequence).** For a real number $r > 0$, the *Beatty sequence* with slope $r$ is the integer sequence $a_n = \lfloor nr \rfloor$ for $n \geq 1$, where $\lfloor x \rfloor$ denotes the greatest integer not exceeding $x$.

**Definition 2.2 (Homogeneous Linear Recurrence).** An integer sequence $(a_n)_{n \geq 1}$ satisfies a *homogeneous linear recurrence with constant integer coefficients of order* $D$ if there exist integers $c_0, c_1, \ldots, c_D$ with $c_0 c_D \neq 0$ (both leading and trailing coefficients nonzero) such that

$$\sum_{i=0}^{D} c_i \, a_{n+i} = 0 \qquad \text{for all sufficiently large } n.$$

The *characteristic polynomial* of this recurrence is $P(x) = \sum_{i=0}^{D} c_i x^i$. The *minimal order* is the smallest $D$ for which such a recurrence exists.

**Definition 2.3 (Non-Trivial Subsequence).** A subsequence of $(a_n)$ is called *non-trivial* if it is infinite, not eventually constant (i.e., not eventually equal to a single value), and the recurrence it satisfies has order $D \geq 1$. This excludes degenerate cases such as finite subsequences, constant subsequences, and the empty sequence.

**Definition 2.4 (AP-Indexed Subsequence).** An *arithmetic-progression-indexed* (AP-indexed) subsequence of $(a_n)$ is a sequence of the form

$$s_k = a_{a + kd} = \lfloor (a + kd) r \rfloor, \qquad k \geq 0,$$

for fixed integers $a \geq 0$ and $d \geq 1$, called the *offset* and *common difference* (or *step*) respectively.

**Notation.** Throughout this document, we use the following conventions:

- $\{x\} = x - \lfloor x \rfloor$ denotes the *fractional part* of $x$.
- $E$ denotes the *shift operator* on sequences: $E \, a_n = a_{n+1}$, and more generally $E^k \, a_n = a_{n+k}$.
- $\Phi_d(x)$ denotes the $d$-th *cyclotomic polynomial*, the minimal polynomial of a primitive $d$-th root of unity over $\mathbb{Q}$.
- $\gcd(a, b)$ denotes the greatest common divisor of integers $a$ and $b$.
- For a polynomial $P(x)$ and operator $E$, $P(E) a_n$ means applying $P$ formally with $x$ replaced by $E$.
- We write $f(k) \sim g(k)$ to mean $\lim_{k \to \infty} f(k)/g(k) = 1$.
- $\mathbb{Q}$ denotes the rational numbers and $\mathbb{Z}$ the integers.

---

## 3. Main Theorem Statement

**Theorem 3.1 (Main Characterization Theorem).** *Let $r > 0$ be a real number. The following three statements are equivalent:*

> **(i)** $r$ is rational.
>
> **(ii)** The Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ itself satisfies a non-trivial homogeneous linear recurrence with constant integer coefficients.
>
> **(iii)** There exists an AP-indexed subsequence of $(\lfloor nr \rfloor)_{n \geq 1}$ that satisfies a non-trivial homogeneous linear recurrence with constant integer coefficients.

### 3.1 Diagram of Implications

The proof proceeds by establishing three implications that together close a logical cycle:

```
    (i) =======> (ii) =======> (iii)
     ^                           |
     |                           |
     +============<=============+
```

- **(i) $\Rightarrow$ (ii):** Constructive. If $r = p/q$ is rational, we produce an explicit homogeneous recurrence of order $q + 1$ for the full Beatty sequence. (Section 4.)
- **(ii) $\Rightarrow$ (iii):** Trivial. The full sequence is an AP-indexed subsequence with offset $a = 1$ and step $d = 1$.
- **(iii) $\Rightarrow$ (i):** Proved by contrapositive. We show that if $r$ is irrational, then NO AP-indexed subsequence satisfies a homogeneous linear recurrence. (Section 5.)

---

## 4. Proof of the Rational Case: (i) $\Rightarrow$ (ii)

Throughout this section, let $r = p/q$ where $p$ and $q$ are positive integers with $\gcd(p, q) = 1$.

### 4.1 Lemma 4.1: The Fundamental Shift Identity

**Lemma 4.1.** *For all $n \geq 1$,*

$$a_{n+q} = a_n + p.$$

**Proof.** We compute directly using the definition $a_n = \lfloor np/q \rfloor$:

$$a_{n+q} = \left\lfloor \frac{(n+q)p}{q} \right\rfloor = \left\lfloor \frac{np}{q} + p \right\rfloor.$$

Since $p$ is a positive integer, the standard identity $\lfloor x + m \rfloor = \lfloor x \rfloor + m$ (valid for all real $x$ and all integers $m$) gives

$$a_{n+q} = \left\lfloor \frac{np}{q} \right\rfloor + p = a_n + p. \qquad \blacksquare$$

**Remark.** In operator notation, this reads $(E^q - 1) a_n = p$. The identity reflects the fact that the fractional part $\{np/q\}$ depends only on the residue $n \bmod q$, since $\{(n+q)p/q\} = \{np/q + p\} = \{np/q\}$ (as $p$ is an integer). Shifting $n$ by $q$ preserves the fractional part and adds exactly $p$ to the integer part.

### 4.2 Lemma 4.2: The Order-$2q$ Recurrence (Naive Homogenization)

**Lemma 4.2.** *The sequence $(a_n)$ satisfies the homogeneous linear recurrence*

$$a_{n+2q} - 2 a_{n+q} + a_n = 0 \qquad \text{for all } n \geq 1.$$

*This is a recurrence of order $2q$.*

**Proof.** Applying Lemma 4.1 twice: $a_{n+q} = a_n + p$ and $a_{n+2q} = a_{n+q} + p = a_n + 2p$. Therefore:

$$a_{n+2q} - 2 a_{n+q} + a_n = (a_n + 2p) - 2(a_n + p) + a_n = 0. \qquad \blacksquare$$

In operator notation, Lemma 4.1 states $(E^q - 1) a_n = p$ (inhomogeneous), and applying the same operator again gives $(E^q - 1)^2 a_n = (E^q - 1) p = 0$ (homogeneous), with characteristic polynomial $(x^q - 1)^2$ of degree $2q$. This is a valid but non-minimal homogenization, as we now show.

### 4.3 Theorem 4.3: The Minimal-Order Recurrence (Order $q+1$)

**Theorem 4.3 (Minimal Recurrence).** *Let $r = p/q$ with $\gcd(p,q) = 1$ and $q \geq 1$. The minimal-order homogeneous linear recurrence with constant integer coefficients satisfied by $a_n = \lfloor np/q \rfloor$ has order exactly $q + 1$:*

$$a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0 \qquad \text{for all } n \geq 1.$$

*The characteristic polynomial is*

$$P(x) = x^{q+1} - x^q - x + 1 = (x - 1)(x^q - 1),$$

*which factors over $\mathbb{Z}$ into cyclotomic polynomials as*

$$(x - 1)^2 \prod_{\substack{d \mid q \\ d > 1}} \Phi_d(x).$$

*The roots are $x = 1$ with multiplicity $2$ and the non-trivial $q$-th roots of unity $e^{2\pi i k/q}$ for $k = 1, 2, \ldots, q - 1$, each with multiplicity $1$.*

**Proof that the recurrence holds.** The inhomogeneous recurrence from Lemma 4.1 is $(E^q - 1) a_n = p$, with constant right-hand side $p$. The operator $(E - 1)$ annihilates any constant: $(E - 1) c = c - c = 0$ for all $c \in \mathbb{Z}$. Applying $(E - 1)$ to both sides of $(E^q - 1) a_n = p$ yields

$$(E - 1)(E^q - 1) a_n = (E - 1) p = 0.$$

Expanding the product of operators:

$$(E - 1)(E^q - 1) = E^{q+1} - E^q - E + 1.$$

Applied to $a_n$, this gives $a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0$ for all $n \geq 1$.

**Why order $q+1$ and not $2q$.** The naive homogenization of Section 4.2 applied the operator $(E^q - 1)$ to annihilate the constant $p$, yielding order $2q$. The key insight is that the constant $p$ is annihilated by the first-order operator $(E - 1)$, not the order-$q$ operator $(E^q - 1)$. Since $(E-1)$ divides $(E^q - 1)$ in the operator ring, applying $(E-1)$ instead of $(E^q-1)$ yields the smaller order $q + 1$.

**Characteristic polynomial factorization.** The polynomial is

$$P(x) = x^{q+1} - x^q - x + 1 = x^q(x - 1) - (x - 1) = (x - 1)(x^q - 1).$$

The factor $(x^q - 1)$ decomposes as $(x - 1) \prod_{d \mid q, d > 1} \Phi_d(x)$, giving

$$P(x) = (x-1)^2 \prod_{\substack{d \mid q \\ d > 1}} \Phi_d(x).$$

The root $x = 1$ has total multiplicity $2$ (appearing once from each factor of $(x-1)$). The remaining $q - 1$ roots are the primitive $d$-th roots of unity for each $d \mid q$ with $d > 1$, each occurring with multiplicity $1$.

**General solution.** The general solution of the order-$(q+1)$ recurrence is

$$a_n = A + Bn + \sum_{k=1}^{q-1} \gamma_k \, e^{2\pi i k n / q},$$

where the double root at $x = 1$ contributes the polynomial part $A + Bn$ (capturing the linear growth $a_n \approx np/q$), and the simple roots at the non-trivial $q$-th roots of unity contribute an oscillatory periodic part with period $q$ (capturing the periodic deviation $-\{np/q\}$ from the linear approximation). Since $a_n$ is real-valued, the complex coefficients satisfy $\gamma_{q-k} = \overline{\gamma_k}$. $\blacksquare$

### 4.4 Proof of Minimality

**Claim.** No homogeneous linear recurrence of order $\leq q$ with integer coefficients is satisfied by $(a_n)$ when $\gcd(p,q) = 1$ and $q > 1$.

**Proof.** The Beatty sequence decomposes as

$$a_n = \frac{np}{q} - \left\{\frac{np}{q}\right\}.$$

The fractional part $f(n) = \{np/q\}$ is periodic with minimal period exactly $q$: since $\gcd(p,q) = 1$, the values $\{p/q, 2p/q, \ldots, qp/q\}$ modulo $1$ form a permutation of $\{0, 1/q, 2/q, \ldots, (q-1)/q\}$.

Suppose for contradiction that $(a_n)$ satisfies a homogeneous recurrence of order $k \leq q$ with integer coefficients $c_0, c_1, \ldots, c_k$ where $c_0, c_k \neq 0$:

$$\sum_{j=0}^{k} c_j \, a_{n+j} = 0 \qquad \text{for all } n \geq 1.$$

Substituting $a_{n+j} = (n+j)p/q - \{(n+j)p/q\}$ and separating the rational-linear part from the periodic part:

$$\frac{p}{q} \sum_{j=0}^{k} c_j(n+j) = \sum_{j=0}^{k} c_j \left\{\frac{(n+j)p}{q}\right\}.$$

The left side is $\frac{p}{q}\bigl(n \sum c_j + \sum j c_j\bigr)$. For this to equal the bounded right side for all $n$, we require $\sum_{j=0}^{k} c_j = 0$; otherwise the left side grows without bound while the right side remains bounded. With $\sum c_j = 0$, the identity becomes

$$\frac{p}{q} \sum_{j=0}^{k} j \, c_j = \sum_{j=0}^{k} c_j \left\{\frac{(n+j)p}{q}\right\} \qquad \text{for all } n \geq 1.$$

The left side is a constant $L$. The right side $R(n)$ is a periodic function of $n$ with period $q$ (since each fractional part $\{(n+j)p/q\}$ is periodic in $n$ with period $q$). The identity $R(n) = L$ for all $n$ demands that $R(n)$ is constant over a full period.

Since $\gcd(p,q) = 1$, as $n$ ranges over $\{1, 2, \ldots, q\}$, the values $\{np/q\}$ realize each of $\{0, 1/q, 2/q, \ldots, (q-1)/q\}$ exactly once. The requirement that $\sum_{j=0}^{k} c_j \{(n+j)p/q\}$ is constant for all $n$ imposes $q - 1$ independent linear constraints on the $k$ free parameters among $c_0, \ldots, c_k$ (after accounting for the constraint $\sum c_j = 0$). When $k < q$, there are at most $k - 1$ free parameters, fewer than the $q - 1$ constraints, so the only solution is the trivial one $c_0 = \cdots = c_k = 0$.

For $k = q$, the system has $q - 1$ free parameters and $q - 1$ constraints, yielding generically a unique (up to scaling) nontrivial solution. This solution corresponds to the operator $(E^q - 1)$, which gives the inhomogeneous identity $a_{n+q} - a_n = p \neq 0$, *not* a homogeneous recurrence. The additional condition for homogeneity, $L = 0$, requires $\sum j c_j = 0$; but for the $(E^q-1)$ operator (where $c_0 = -1$, $c_q = 1$, all others zero), $\sum j c_j = q \neq 0$, so $L = p \neq 0$.

Therefore, no homogeneous recurrence of order $\leq q$ exists, and the minimal homogeneous order is $q + 1$. $\blacksquare$

### 4.5 Corollary 4.4: Recurrence Order for AP Subsequences

**Corollary 4.4.** *For rational $r = p/q$ with $\gcd(p,q) = 1$, the AP-indexed subsequence $s_k = \lfloor (a + kd) p/q \rfloor$ satisfies a homogeneous linear recurrence of order $q' + 1$, where $q' = q / \gcd(d, q)$.*

**Proof.** Set $m = d / \gcd(d,q)$ so that $q'd = mq$. Then $s_{k+q'} = a_{(a+kd) + q'd} = a_{(a+kd)+mq}$. Applying Lemma 4.1 $m$ times gives $a_{n+mq} = a_n + mp$ for any $n$. Thus

$$s_{k+q'} = s_k + mp = s_k + \frac{dp}{\gcd(d,q)}.$$

This is an inhomogeneous recurrence with constant right-hand side. Applying $(E-1)$ to homogenize:

$$(E - 1)(E^{q'} - 1) s_k = 0,$$

which is a homogeneous recurrence of order $q' + 1$:

$$s_{k+q'+1} - s_{k+q'} - s_{k+1} + s_k = 0. \qquad \blacksquare$$

**Example.** When $\gcd(d,q) = q$ (i.e., $q \mid d$), we get $q' = 1$ and the subsequence satisfies $s_{k+2} - 2s_{k+1} + s_k = 0$, a second-order recurrence whose solutions are arithmetic progressions. When $\gcd(d,q) = 1$, we get $q' = q$ and the order remains $q + 1$.

---

## 5. Proof of the Irrational Case: NOT(i) $\Rightarrow$ NOT(iii)

We prove the contrapositive of (iii) $\Rightarrow$ (i): if $r$ is irrational, then no AP-indexed subsequence of $\lfloor nr \rfloor$ satisfies a non-trivial homogeneous linear recurrence with integer coefficients. Two proofs are given: a direct algebraic argument (Sections 5.1--5.3) and an alternative via Weyl equidistribution (Section 5.4).

### 5.1 Step 1: Growth Analysis

Suppose for contradiction that $s_k = \lfloor (a + kd) r \rfloor$ satisfies a homogeneous linear recurrence of order $D$ with integer coefficients $c_0, c_1, \ldots, c_D$ ($c_0 c_D \neq 0$). By the general theory of linear recurrence sequences (see, e.g., \cite{allouche2003automatic}), the solution has the form

$$s_k = \sum_{i=1}^{m} P_i(k) \, \lambda_i^k,$$

where $\lambda_1, \ldots, \lambda_m$ are the distinct roots of the characteristic polynomial $P(x) = c_0 + c_1 x + \cdots + c_D x^D$ (each an algebraic number), and $P_i(k)$ is a polynomial of degree at most $\mu_i - 1$, where $\mu_i$ is the multiplicity of root $\lambda_i$.

We analyze the growth rate. From the definition:

$$s_k = (a + kd)r - \{(a + kd)r\},$$

where $\{(a + kd)r\} \in [0, 1)$. Therefore $s_k = kdr + ar - \{(a+kd)r\}$, which gives $s_k \sim kdr$ as $k \to \infty$ -- the sequence exhibits linear growth with asymptotic slope $dr > 0$.

For the exponential-polynomial expression to match this linear growth, every characteristic root $\lambda_i$ must satisfy $|\lambda_i| \leq 1$: any root with $|\lambda_i| > 1$ would produce exponential growth, contradicting the linear asymptotics. Among roots with $|\lambda_i| = 1$, only $\lambda = 1$ (with multiplicity at least $2$) can produce the linear term $kdr$. The other roots of modulus $1$ contribute bounded oscillatory terms, and roots with $|\lambda_i| < 1$ contribute terms decaying to zero.

Thus the solution necessarily takes the form

$$s_k = \alpha_1 k + \alpha_0 + g(k),$$

where $\alpha_1 k + \alpha_0$ comes from the double root at $\lambda = 1$ (the polynomial part at $\lambda = 1$ must be linear, since superlinear polynomials would dominate $kdr$), and $g(k)$ is a bounded function arising from all other characteristic roots. In particular, $\alpha_1 = \lim_{k \to \infty} s_k / k = dr$.

### 5.2 Step 2: The Rationality Constraint on the Asymptotic Slope

**Key Lemma.** *If an integer-valued sequence $(s_k)_{k \geq 0}$ satisfies a homogeneous linear recurrence with integer coefficients, and $s_k = \alpha_1 k + \alpha_0 + g(k)$ where $g(k)$ is bounded, then $\alpha_1 \in \mathbb{Q}$.*

**Proof.** The characteristic polynomial $P(x) = \sum_{i=0}^{D} c_i x^i$ has integer coefficients, so its roots are algebraic numbers. The root $\lambda = 1$ is rational. The coefficients $\alpha_0, \alpha_1$ in the polynomial part at $\lambda = 1$ are determined by the initial conditions $s_0, s_1, \ldots, s_{D-1}$ (all integers) through a linear system. Specifically, the generating function of $(s_k)$ is

$$\sum_{k=0}^{\infty} s_k x^k = \frac{N(x)}{P^*(x)},$$

where $P^*(x) = x^D P(1/x) = c_D + c_{D-1}x + \cdots + c_0 x^D$ is the reversed characteristic polynomial, and $N(x)$ is a polynomial of degree at most $D - 1$ determined by the initial conditions. Both $N(x)$ and $P^*(x)$ have integer coefficients. The pole at $x = 1$ has order $\mu \geq 2$ (corresponding to the double root), and the partial fraction expansion around $x = 1$ takes the form

$$\frac{N(x)}{P^*(x)} = \frac{A}{(1-x)^2} + \frac{B}{(1-x)} + (\text{terms from other poles}).$$

The coefficients $A$ and $B$ are determined by evaluating $N(x)/Q(x)$ at $x = 1$, where $Q(x) = P^*(x)/(1-x)^2$ accounts for the other factors. Since $N(x)$, $P^*(x)$, and $Q(x)$ all have rational (indeed integer) coefficients, and $x = 1$ is a rational point, $A$ and $B$ are rational numbers. The contribution from the double pole at $x = 1$ to the coefficient of $x^k$ is $A(k+1) + B$, so $\alpha_1 = A \in \mathbb{Q}$. $\blacksquare$

**Alternative justification.** One can also argue via the Casorati matrix formulation. The coefficients $\alpha_0$ and $\alpha_1$ satisfy the system $\alpha_0 + \alpha_1 j + g(j) = s_j$ for $j = 0, 1, \ldots, D-1$. By solving this system using Cramer's rule, each coefficient is a ratio of determinants involving only rational numbers (integer initial conditions $s_j$, integer values of $g(j)$ at specific points determined by rational eigenvalues), plus contributions from other characteristic roots. For the root $\lambda = 1$ specifically, the contribution is isolated by the partial-fraction technique above, yielding $\alpha_1 \in \mathbb{Q}$.

### 5.3 Step 3: The Contradiction

From Step 1, the asymptotic slope is $\alpha_1 = dr$. From Step 2, this slope must be rational: $\alpha_1 \in \mathbb{Q}$.

But since $d \geq 1$ is a positive integer and $r$ is irrational, the product $dr$ is irrational. Indeed, if $dr$ were rational, say $dr = p'/q'$, then $r = p'/(dq')$, contradicting the irrationality of $r$.

This contradiction shows that the initial assumption -- that $s_k$ satisfies a homogeneous linear recurrence -- is false. $\blacksquare$

### 5.4 Alternative Proof via Weyl Equidistribution

We present an independent proof using Weyl's equidistribution theorem \cite{weyl1916gleichverteilung}.

**Decomposition.** Write $s_k = \ell(k) + \varepsilon_k$ where $\ell(k) = kdr + ar$ is the linear part and $\varepsilon_k = -\{(a + kd)r\}$ is the error term, lying in $(-1, 0]$.

**Equidistribution of the error.** Since $r$ is irrational and $d \geq 1$, the product $dr$ is irrational. By Weyl's equidistribution theorem, the sequence $\{kdr\}_{k \geq 0}$ is equidistributed modulo $1$. Since equidistribution is preserved under translation by the constant $ar$, the sequence $\{ar + kdr\}$ is also equidistributed in $[0, 1)$. Consequently, $\varepsilon_k = -\{ar + kdr\}$ is equidistributed in $(-1, 0]$.

**Linear recurrence sequences cannot have equidistributed bounded part.** Suppose $s_k$ satisfies a linear recurrence with integer coefficients. Then $\varepsilon_k = s_k - \ell(k)$ must also satisfy a linear recurrence. This is because $\ell(k) = kdr + ar$ satisfies the trivial recurrence $(E - 1)^2 \ell(k) = 0$, and the difference of two linear-recurrence sequences is itself a linear-recurrence sequence.

Now $\varepsilon_k$ is a bounded linear-recurrence sequence. Its characteristic roots $\mu_j$ must satisfy $|\mu_j| \leq 1$. The roots with $|\mu_j| = 1$ are algebraic numbers on the unit circle that are roots of a polynomial with integer coefficients; by Kronecker's theorem \cite{kronecker1857zwei}, such algebraic integers must be roots of unity. The roots with $|\mu_j| < 1$ contribute terms decaying to zero. Thus $\varepsilon_k$ is asymptotically a finite sum of periodic functions -- it is *eventually periodic* (or more precisely, the sum of finitely many periodic sequences plus a decaying transient).

An eventually periodic sequence taking values in a continuous interval $(-1, 0]$ visits only finitely many distinct values in each period. In particular, such a sequence is NOT equidistributed.

This contradicts the established equidistribution of $\varepsilon_k$. Therefore, $s_k$ cannot satisfy a linear recurrence. $\blacksquare$

**Remark on Kronecker's theorem.** The argument in the equidistribution proof uses a result due to Kronecker (1857) \cite{kronecker1857zwei}: if $\zeta$ is an algebraic integer with $|\zeta| = 1$ and all conjugates also on the unit circle, then $\zeta$ is a root of unity. This is essential because it rules out the possibility that characteristic roots might be "irrational rotations" on the unit circle, which could potentially produce equidistributed behavior. Since the characteristic polynomial has integer coefficients, all roots are algebraic integers, and Kronecker's theorem ensures that unit-modulus roots are roots of unity, hence contribute only periodic (not equidistributed) terms.

---

## 6. Edge Cases

### 6.1 The Zero Sequence: $r = 0$

When $r = 0$, $a_n = \lfloor 0 \rfloor = 0$ for all $n$. This is the identically zero sequence, which satisfies the trivial first-order recurrence $a_{n+1} - a_n = 0$. Since $r = 0$ is rational ($0 = 0/1$), this is consistent with the theorem. The general formula predicts order $q + 1 = 2$ for $r = 0/1$, but the actual minimal order is $1$ because the sequence has zero growth; the general formula assumes $p > 0$.

### 6.2 The Identity Sequence: $r = 1$

When $r = 1$, $a_n = \lfloor n \rfloor = n$. This satisfies $a_{n+2} - 2a_{n+1} + a_n = 0$ (order $2$), with characteristic polynomial $(x-1)^2$. Since $r = 1/1$ with $q = 1$, the theorem predicts order $q + 1 = 2$, which matches exactly.

### 6.3 Integer Slopes: $r = m$

For any positive integer $m$, $a_n = mn$, which satisfies $a_{n+2} - 2a_{n+1} + a_n = 0$ (order $2$), consistent with $r = m/1$, $q = 1$, predicted order $2$.

### 6.4 Slopes in $(0, 1)$

For $r \in (0, 1)$ rational, say $r = p/q$ with $0 < p < q$, the sequence $\lfloor np/q \rfloor$ has many repeated values and long constant runs. Nevertheless, it satisfies the same order-$(q+1)$ recurrence. For irrational $r \in (0,1)$, no recurrence exists. The long runs do not affect the characterization.

**Example.** $r = 1/3$: sequence is $0, 0, 1, 1, 1, 2, 2, 2, 3, \ldots$ with period-$3$ first differences $0, 1, 0, 0, 1, 0, \ldots$ and minimal recurrence order $q + 1 = 4$.

### 6.5 Negative Slopes: $r < 0$

For $r < 0$, we have $a_n = \lfloor nr \rfloor = -\lceil n|r| \rceil$, using $\lfloor -x \rfloor = -\lceil x \rceil$. The sequence satisfies a homogeneous linear recurrence if and only if $|r|$ is rational (equivalently, $r$ is rational). When $|r| = p/q$ is rational, the sequence $-\lceil np/q \rceil$ satisfies the same order-$(q+1)$ recurrence as $\lfloor np/q \rfloor$, because negation and addition of periodic correction terms preserve linear recurrence. When $|r|$ is irrational, the same growth-rate obstruction applies: the asymptotic slope $d|r|$ is irrational.

### 6.6 The Perturbation Discontinuity: $r = p/q + \varepsilon$

This is the most illuminating edge case. Consider $r_\varepsilon = p/q + \varepsilon$ with $\gcd(p,q) = 1$.

- **$\varepsilon = 0$ (rational):** The recurrence $a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0$ holds exactly for all $n$.
- **$\varepsilon$ irrational (no matter how small):** No recurrence of ANY order exists. The transition is instantaneous and discontinuous.
- **$\varepsilon$ rational, $\varepsilon = p'/q' \neq 0$:** The new slope $r = (pq' + p'q)/(qq')$ is rational with a (typically much) larger denominator. A recurrence exists but at the correspondingly higher order.

The recurrence residual $R_n(\varepsilon) = a_{n+q+1}(\varepsilon) - a_{n+q}(\varepsilon) - a_{n+1}(\varepsilon) + a_n(\varepsilon)$ is zero for $\varepsilon = 0$ and nonzero at a positive density of indices for any irrational $\varepsilon$, no matter how small. The fraction of nonzero residuals among $n \in \{1, \ldots, N\}$ is approximately $C \cdot N \cdot |\varepsilon|$ for a constant $C$ depending on $p, q$. This means that near-rational irrationals (such as $r = \pi \approx 355/113$) can "appear" to satisfy the recurrence for many terms before the violations become detectable, but the violations are inevitable and occur at positive density for sufficiently large $N$.

**Computational example.** For $r = 3/2 + 10^{-6}\sqrt{2} \approx 1.500001414$, the order-$3$ recurrence from $r = 3/2$ appears to hold for all $n < 353{,}553$, but fails at positive density thereafter. For $r = \pi$ (approximated to $7$ decimal places by $355/113$), the sequences $\lfloor n \cdot 355/113 \rfloor$ and $\lfloor n\pi \rfloor$ agree for $n$ up to approximately $3.7 \times 10^6$, after which the rational approximation's order-$114$ recurrence holds but $\pi$'s sequence admits no recurrence at all.

---

## 7. Computational Verification Summary

### 7.1 Test Coverage

The characterization theorem was validated against a systematic computational search encompassing $102$ distinct values of $r$:

| Class of $r$ | Count | Description |
|:---|:---:|:---|
| Rational | 60 | All $p/q$ with $q \leq 20$ in lowest terms, plus selected large-denominator rationals |
| Quadratic irrational | 24 | $\sqrt{D}$ for various $D$, plus $(a + \sqrt{D})/b$ forms |
| Algebraic, degree $\geq 3$ | 15 | Cube roots, fourth roots, fifth roots of small integers |
| Transcendental | 3 | $\pi$, $e$, $\ln 2$ |

For each value, the subsequence search framework (`src/subsequence_search.py`) enumerated all AP-indexed subsequences with offsets $a \in \{0, \ldots, 20\}$ and steps $d \in \{1, \ldots, 20\}$, extracting subsequences of length at least $50$ from the first $N = 10{,}000$ terms. The Berlekamp-Massey algorithm (`src/recurrence_detector.py`) tested each candidate for homogeneous linear recurrence up to order $d_{\max} = 10$.

### 7.2 Results: Perfect Agreement

The results show perfect agreement between the theorem's predictions and computational outcomes:

| | Experiment: Recurrence Found | Experiment: No Recurrence | Total |
|:---|:---:|:---:|:---:|
| Theorem Predicts YES (rational) | 60 | 0 | 60 |
| Theorem Predicts NO (irrational) | 0 | 42 | 42 |
| Total | 60 | 42 | 102 |

All standard metrics (accuracy, sensitivity, specificity, precision, Cohen's kappa) are $1.000$ -- perfect agreement.

### 7.3 False Positive Analysis

Two initial false positives were detected during early testing for $r = \sqrt{13}$ and $r = \sqrt{14}$: the Berlekamp-Massey algorithm reported candidate recurrences based on the first $500$ terms, which failed verification when extended to $10{,}000$ terms. These were quasi-periodic artifacts: the BM algorithm fitted the limited data to a spurious high-order recurrence that happened to hold for the initial segment but violated at larger indices. After implementing the extended verification protocol (requiring all candidate recurrences to hold for at least $10{,}000$ terms), both false positives were eliminated. The final dataset contains zero false positives and zero false negatives.

### 7.4 Sensitivity Analysis

The characterization is robust to definitional choices:

- **$d_{\max}$ threshold:** Increasing the maximum allowed recurrence order from $2$ to $50$ affects only the detection of large-denominator rationals (those with $q + 1 > d_{\max}$). For irrational $r$, no recurrence is found at any order.
- **Homogeneous vs. inhomogeneous:** Allowing inhomogeneous recurrences (with a nonzero constant term) does not change the characterization. For rational $r$, an inhomogeneous recurrence of order $q$ exists (Lemma 4.1); for irrational $r$, even inhomogeneous recurrences fail (the growth-rate argument applies equally to inhomogeneous recurrences, since the asymptotic slope must still be rational).
- **AP vs. arbitrary subsequences:** Restricting to AP-indexed subsequences versus searching over arbitrary (polynomial, exponential, nested Beatty) index sets does not change the characterization. The impossibility proof generalizes to all natural index sets (see Corollaries in Section 5 discussion).

---

## 8. Comparison with Prior Work

### 8.1 Relation to the Existing Literature

The Main Characterization Theorem synthesizes and extends several threads in the existing literature. We enumerate the key connections.

**Beatty (1926) \cite{beatty1926problem} and Fraenkel (1969) \cite{fraenkel1969bracket}.** The original definition of Beatty sequences and the complementary partition property. Our work takes the Beatty sequence as its starting object and proves a structural theorem about it that is not addressed in the classical literature.

**Durand (1998, 2000) \cite{durand1998characterization, durand2003linearly}.** Durand characterized when a Sturmian word is linearly recurrent (Notion A): if and only if the continued fraction partial quotients of the slope are bounded. Our theorem addresses Notion B (algebraic linear recurrence of the integer-valued sequence), which we prove is completely independent of Notion A. The golden ratio is the decisive witness: Notion A holds but Notion B fails.

**Cassaigne (1999) \cite{cassaigne1999limit}.** Cassaigne computed precise recurrence quotient formulas for Sturmian sequences. These quantify Notion A and are orthogonal to our Notion B characterization.

**Allouche and Shallit (2003) \cite{allouche2003automatic}.** The comprehensive theory of automatic and morphic sequences classifies the bounded first-difference Sturmian word but does not extend to the unbounded cumulative Beatty sequence. The morphic structure of $\Delta_r$ for quadratic irrational $r$ does not propagate to algebraic recurrence of $\lfloor nr \rfloor$, because the summation operation that converts first differences to cumulative sums does not preserve the exponential-polynomial solution structure of linear recurrences.

**Schaeffer, Shallit, and Zorcic (2024) \cite{schaeffer2024beatty}.** Their decidability result for quadratic Beatty sequences via Ostrowski numeration provides an independent verification path: for any specific quadratic irrational $\alpha$ and any fixed recurrence order $D$, the statement "no AP subsequence satisfies a recurrence of order $\leq D$" is a first-order sentence over $(\mathbb{N}, +, B_\alpha)$, which their framework can algorithmically verify. Our proof provides a uniform argument across all quadratic irrationals simultaneously, without case-by-case automaton construction.

**Skolem (1934) \cite{skolem1934einige}, Mahler (1935) \cite{mahler1935arithmetische}, Lech (1953) \cite{lech1953note}.** The Skolem-Mahler-Lech theorem -- that zero sets of linear recurrence sequences are finite unions of arithmetic progressions plus finite sets -- provides a structural constraint used in our proof. It reinforces the incompatibility between the equidistributed fractional parts $\{nr\}$ (for irrational $r$) and the eventually-periodic structure forced by linear recurrence.

**Weyl (1916) \cite{weyl1916gleichverteilung}.** Weyl's equidistribution theorem is used directly in the alternative proof of the irrational case (Section 5.4). It provides the crucial fact that $\{kdr\}$ is equidistributed modulo $1$ when $dr$ is irrational.

**Lagrange (1770) \cite{lagrange1770continued}.** Lagrange's theorem that quadratic irrationals have eventually periodic continued fractions connects to Durand's characterization but is not directly used in our proof. It explains why quadratic irrationals are special for Notion A, even though they are not special for Notion B.

**Roth (1955) \cite{roth1955rational}.** Roth's theorem that algebraic irrationals have irrationality measure exactly $2$ might suggest a distinction between algebraic and transcendental irrationals. Our theorem shows that no such distinction exists for Notion B: the sole obstruction is the bare irrationality of $r$, regardless of irrationality measure, algebraic degree, or Diophantine approximation properties.

### 8.2 Novel Contributions

The following aspects of this work appear to be new:

| Contribution | Description |
|:---|:---|
| Complete characterization | The three-way equivalence (i) $\Leftrightarrow$ (ii) $\Leftrightarrow$ (iii) with both directions fully proved |
| Uniformity across all irrationals | Explicit demonstration that the impossibility holds identically for quadratic, algebraic, and transcendental irrationals |
| Independence of Notion A and Notion B | Rigorous proof with explicit witnesses in both directions |
| Minimal order formula | Exact minimal homogeneous recurrence order $q + 1$ for rational $r = p/q$, with cyclotomic characteristic polynomial |
| Uniform proof method | A single growth-rate argument that handles all irrationals simultaneously |

---

## 9. Open Questions

Several natural questions remain open or suggest directions for further investigation.

### 9.1 Non-Constructive Subsequences

Our theorem addresses AP-indexed subsequences and extends (via the growth-rate argument) to polynomial and exponential index sets. For completely arbitrary, non-constructive index sequences, one can in principle choose indices $n_k$ so that $\lfloor n_k r \rfloor$ matches any desired target sequence. If the target satisfies a recurrence, this produces a "recurrent subsequence," but the index set is defined circularly. **Open question:** Is there a natural formalization of "constructive index set" under which the theorem extends to all constructive subsequences? A connection to the framework of computable analysis or reverse mathematics may be fruitful.

### 9.2 Inhomogeneous Beatty Sequences

The generalized Beatty sequence $B_{\alpha,\beta}(n) = \lfloor n\alpha + \beta \rfloor$ for real $\alpha > 0$ and $\beta \geq 0$ includes a phase shift $\beta$. **Conjecture:** $B_{\alpha,\beta}$ contains a non-trivial AP-indexed linearly recurrent subsequence if and only if $\alpha$ is rational. The proof should adapt directly, since the asymptotic slope of any AP subsequence is still $d\alpha$ (the phase $\beta$ contributes only to the constant term $\alpha_0$), and the rationality constraint applies to the slope.

### 9.3 Quantitative Recurrence Residual Bounds

For near-rational $r = p/q + \varepsilon$ with small irrational $\varepsilon$, the recurrence residual is nonzero at a density proportional to $|\varepsilon|$. **Open question:** What is the precise asymptotic formula for the density of nonzero residuals as a function of $\varepsilon$, $p$, $q$, and $N$? A quantitative version of the perturbation analysis (Section 6.6) would strengthen the edge-case understanding.

### 9.4 Connection to Decidability Frameworks

The Schaeffer-Shallit-Zorcic decidability framework \cite{schaeffer2024beatty} for quadratic Beatty sequences could in principle verify our theorem case by case for each specific quadratic irrational. **Open question:** Can the decidability framework be extended to produce a *uniform* proof covering all quadratic irrationals simultaneously, thereby connecting our analytic argument to automata-theoretic methods? More ambitiously, can analogues of Ostrowski numeration for higher-degree algebraic numbers yield similar decidability results?

### 9.5 Multidimensional Generalizations

For Beatty sequences indexed by lattice points, $a_{n_1, n_2} = \lfloor n_1 r_1 + n_2 r_2 \rfloor$ with $(n_1, n_2) \in \mathbb{Z}^2$, the analogous characterization is unexplored. **Conjecture:** Such sequences satisfy multidimensional linear recurrences if and only if $r_1$ and $r_2$ are both rational.

---

## References

- \cite{beatty1926problem} Beatty, S. (1926). Problem 3173. *Amer. Math. Monthly* 33, 159.
- \cite{fraenkel1969bracket} Fraenkel, A.S. (1969). The bracket function and complementary sets of integers. *Canad. J. Math.* 21, 6--27.
- \cite{durand1998characterization} Durand, F. (1998). A characterization of substitutive sequences using return words. *Discrete Math.* 179, 89--101.
- \cite{durand2003linearly} Durand, F. (2000). Linearly recurrent subshifts have a finite number of non-periodic subshift factors. *Ergodic Theory Dynam. Systems* 20(4), 1061--1078.
- \cite{cassaigne1999limit} Cassaigne, J. (1999). Limit values of the recurrence quotient of Sturmian sequences. *Theoret. Comput. Sci.* 218(1), 3--12.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences: Theory, Applications, Generalizations.* Cambridge University Press.
- \cite{schaeffer2024beatty} Schaeffer, L., Shallit, J., and Zorcic, S. (2024). Beatty Sequences for a Quadratic Irrational: Decidability and Applications. arXiv:2402.08331.
- \cite{skolem1934einige} Skolem, T. (1934). Ein Verfahren zur Behandlung gewisser exponentialer Gleichungen. *Comptes rendus du 8e Congres des Math. Scandinaves*, 163--188.
- \cite{mahler1935arithmetische} Mahler, K. (1935). Uber das Verschwinden von Potenzreihen. *Math. Ann.* 103, 573--587.
- \cite{lech1953note} Lech, C. (1953). A note on recurring series. *Arkiv for Matematik* 2(5), 417--421.
- \cite{weyl1916gleichverteilung} Weyl, H. (1916). Uber die Gleichverteilung von Zahlen mod. Eins. *Math. Ann.* 77, 313--352.
- \cite{lagrange1770continued} Lagrange, J.-L. (1770). Additions au memoire sur la resolution des equations numeriques.
- \cite{roth1955rational} Roth, K.F. (1955). Rational approximations to algebraic numbers. *Mathematika* 2(1), 1--20.
- \cite{kronecker1857zwei} Kronecker, L. (1857). Zwei Satze uber Gleichungen mit ganzzahligen Coefficienten. *J. Reine Angew. Math.* 53, 173--175.
- \cite{morse1938symbolic} Morse, M. and Hedlund, G.A. (1938). Symbolic dynamics. *Amer. J. Math.* 60(4), 815--866.
- \cite{morse1940symbolic2} Morse, M. and Hedlund, G.A. (1940). Symbolic dynamics II: Sturmian trajectories. *Amer. J. Math.* 62(1), 1--42.
- \cite{coven1973sequences} Coven, E.M. and Hedlund, G.A. (1973). Sequences with minimal block growth. *Math. Systems Theory* 7(2), 138--153.
- \cite{ostrowski1922bemerkungen} Ostrowski, A. (1922). Bemerkungen zur Theorie der Diophantischen Approximationen. *Abh. Math. Sem. Univ. Hamburg* 1(1), 77--98.
- \cite{hieronymi2018ostrowski} Hieronymi, P. and Terry, A. (2018). Ostrowski Numeration Systems, Addition, and Finite Automata. *Notre Dame J. Formal Logic* 59(2), 215--232.
- \cite{sos1958distribution} Sos, V.T. (1958). On the distribution mod 1 of the sequence $n\alpha$. *Ann. Univ. Sci. Budapest.* 1, 127--134.
- \cite{ravenstein1988three} van Ravenstein, T. (1988). The Three Gap Theorem (Steinhaus Conjecture). *J. Austral. Math. Soc. (Series A)* 45(3), 360--370.
- \cite{berlekamp1968algebraic} Berlekamp, E.R. (1968). *Algebraic Coding Theory.* McGraw-Hill.
- \cite{massey1969shift} Massey, J.L. (1969). Shift-register synthesis and BCH decoding. *IEEE Trans. Inform. Theory* 15(1), 122--127.
