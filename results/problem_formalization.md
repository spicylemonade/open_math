# Formal Problem Statement: Characterizing Numbers r for which ⌊nr⌋ Contains a Homogeneous Linearly Recurrent Subsequence

## 1. Definition of the Beatty Sequence

**Definition 1.1 (Beatty Sequence).** For a real number $r > 0$, the *Beatty sequence* associated with $r$ is the integer sequence
$$B_r = (b_r(n))_{n \geq 1}, \quad \text{where } b_r(n) = \lfloor n r \rfloor.$$

Here $\lfloor x \rfloor$ denotes the floor function, i.e., the greatest integer not exceeding $x$.

**Remark 1.2.** When $r > 1$ is irrational, $B_r$ is called a *(homogeneous) Beatty sequence* in the classical sense. Beatty's Theorem (1926) states that if $r, s > 1$ are irrational with $1/r + 1/s = 1$, then $B_r$ and $B_s$ partition the positive integers. We allow $r$ to be any positive real, including rationals and values in $(0,1]$.

**Remark 1.3.** The *inhomogeneous Beatty sequence* $\lfloor n\alpha + \beta \rfloor$ generalizes the above. Our investigation focuses on the homogeneous case $\beta = 0$.

**Definition 1.4 (First-Difference Sequence).** The *first-difference sequence* (or *characteristic word*) of $B_r$ is
$$\Delta_r(n) = b_r(n+1) - b_r(n) = \lfloor (n+1)r \rfloor - \lfloor n r \rfloor, \quad n \geq 1.$$

When $r$ is irrational, $\Delta_r$ is a *Sturmian word* over the alphabet $\{\lfloor r \rfloor, \lceil r \rceil\}$.

## 2. Formal Definition of Homogeneous Linear Recurrence

**Definition 2.1 (Homogeneous Linear Recurrence of Order $d$).** A sequence $(a_n)_{n \geq 0}$ of real (or integer) numbers satisfies a *homogeneous linear recurrence with constant coefficients of order $d$* if there exist constants $c_0, c_1, \ldots, c_d \in \mathbb{Z}$ (or $\mathbb{R}$), not all zero, with $c_0 \neq 0$ and $c_d \neq 0$, such that
$$c_0 \, a_{n} + c_1 \, a_{n+1} + \cdots + c_d \, a_{n+d} = 0 \quad \text{for all } n \geq 0.$$

Equivalently, $a_{n+d} = -\frac{1}{c_d}(c_0 \, a_n + c_1 \, a_{n+1} + \cdots + c_{d-1} \, a_{n+d-1})$.

**Definition 2.2 (Minimal Order).** The *minimal order* of a homogeneous linear recurrence satisfied by $(a_n)$ is the smallest $d \geq 1$ for which such a relation exists.

**Definition 2.3 (Characteristic Polynomial).** The *characteristic polynomial* of the recurrence $\sum_{i=0}^{d} c_i \, a_{n+i} = 0$ is
$$p(x) = c_0 + c_1 x + c_2 x^2 + \cdots + c_d x^d.$$

The roots of $p(x)$ (counted with multiplicity) determine the general solution of the recurrence via the standard theory: if the roots are $\lambda_1, \ldots, \lambda_k$ with multiplicities $m_1, \ldots, m_k$, then
$$a_n = \sum_{i=1}^{k} \left(\sum_{j=0}^{m_i - 1} \alpha_{i,j} \, n^j \right) \lambda_i^n$$
for appropriate constants $\alpha_{i,j}$.

## 3. Precise Statement of the Containment Problem

**Definition 3.1 (Subsequence).** A *subsequence* of a sequence $(a_n)_{n \geq 1}$ is any sequence of the form $(a_{n_k})_{k \geq 1}$ where $n_1 < n_2 < n_3 < \cdots$ is a strictly increasing sequence of positive integers.

**Definition 3.2 (Homogeneous Linearly Recurrent Subsequence — General).** We say that the Beatty sequence $B_r = (\lfloor n r \rfloor)_{n \geq 1}$ *contains a homogeneous linearly recurrent subsequence* if there exists a strictly increasing sequence of indices $n_1 < n_2 < n_3 < \cdots$ (infinite) such that the subsequence
$$S = (\lfloor n_k r \rfloor)_{k \geq 1}$$
satisfies a homogeneous linear recurrence of some finite order $d$. That is, there exist integer coefficients $c_0, \ldots, c_d$ (not all zero, $c_0 c_d \neq 0$) such that
$$\sum_{i=0}^{d} c_i \, \lfloor n_{k+i} \, r \rfloor = 0 \quad \text{for all } k \geq 1.$$

**Definition 3.3 (Arithmetic-Progression-Indexed Subsequence).** An important special case is when the index set forms an arithmetic progression: $n_k = a + kd$ for fixed $a \geq 0$, $d \geq 1$. In this case the subsequence is
$$S_{a,d}(r) = (\lfloor (a + kd) \, r \rfloor)_{k \geq 0}.$$

**Definition 3.4 (Non-Trivial Subsequence).** A subsequence is *non-trivial* if:
- It is infinite (has infinitely many terms).
- It is not eventually constant (i.e., it is not the case that $\lfloor n_k r \rfloor = C$ for all sufficiently large $k$).
- The recurrence has order $d \geq 1$ (excluding the degenerate "recurrence" $0 \cdot a_n = 0$).

**Remark 3.5.** We must be careful about trivial cases:
- If $r = 0$, then $\lfloor n \cdot 0 \rfloor = 0$ for all $n$, so the sequence is the zero sequence, which trivially satisfies $a_{n+1} - a_n = 0$.
- Any constant subsequence satisfies a recurrence. This is why we require non-triviality.
- For any $r > 0$, the subsequence along $n_k = k$ (the full sequence) is the main candidate.

**The Central Question:** *For which positive real numbers $r$ does the Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contain a non-trivial homogeneous linearly recurrent subsequence?*

## 4. Taxonomy of the Parameter Space for $r$

We partition the positive reals $r > 0$ into four classes based on their algebraic and number-theoretic properties:

### Class I: Rational Numbers ($r \in \mathbb{Q}_{>0}$)

$r = p/q$ where $p, q \in \mathbb{Z}_{>0}$, $\gcd(p,q) = 1$.

**Key property:** The first-difference sequence $\Delta_r$ is purely periodic with period $q$. The sequence $\lfloor nr \rfloor$ itself satisfies $b_r(n+q) = b_r(n) + p$, which yields the homogeneous recurrence $b_r(n+2q) - 2b_r(n+q) + b_r(n) = 0$.

### Class II: Quadratic Irrationals ($r$ algebraic of degree 2)

$r = (a + b\sqrt{D})/c$ where $a, b, c \in \mathbb{Z}$, $D > 0$ squarefree, $b \neq 0$.

**Key property:** By Lagrange's theorem, $r$ has an eventually periodic continued fraction expansion $r = [a_0; a_1, a_2, \ldots]$ with bounded partial quotients. Equivalently, the Sturmian word $\Delta_r$ is *linearly recurrent* in the combinatorics-on-words sense (Durand's characterization). The Beatty sequence is related to Ostrowski numeration systems, and many first-order properties are decidable (Schaeffer–Shallit–Zorcic, 2024).

Examples: $r = \varphi = (1+\sqrt{5})/2$ (golden ratio), $r = \sqrt{2}$, $r = \sqrt{3}$, $r = 1 + \sqrt{2}$.

### Class III: Algebraic Irrationals of Degree $\geq 3$

$r$ is a root of an irreducible polynomial $p(x) \in \mathbb{Z}[x]$ of degree $\geq 3$.

**Key property:** By Roth's theorem, the irrationality measure of $r$ is exactly 2 (same as quadratic irrationals). However, the continued fraction expansion of $r$ is *not* eventually periodic (by the converse of Lagrange's theorem). The partial quotients are conjectured (but not proven in general) to be unbounded for most such numbers. The Sturmian word $\Delta_r$ is *not* linearly recurrent (assuming unbounded partial quotients).

Examples: $r = \sqrt[3]{2}$, $r = \sqrt[3]{3}$, $r = 2^{1/4}$, roots of $x^3 - x - 1 = 0$.

### Class IV: Transcendental Numbers

$r$ is not the root of any polynomial with integer coefficients.

**Key property:** Transcendental numbers may have irrationality measure equal to 2 (like $e$, where the CF expansion $e = [2; 1, 2, 1, 1, 4, 1, 1, 6, \ldots]$ has unbounded but structured partial quotients), or may have arbitrarily large irrationality measure (Liouville numbers). The CF structure varies widely.

Examples: $r = \pi$, $r = e$, $r = \ln 2$, $r = \sum_{k=0}^{\infty} 10^{-k!}$ (Liouville's constant).

## 5. Summary of Expected Results by Class

| Class | Description | CF Structure | Expected Recurrence? |
|-------|-------------|--------------|---------------------|
| I | Rational $p/q$ | Finite CF | **Yes** — full sequence satisfies order-$2q$ homogeneous recurrence |
| II | Quadratic irrational | Eventually periodic CF, bounded PQ | **To be determined** — connection to linear recurrence in Sturmian word sense |
| III | Algebraic degree $\geq 3$ | Non-periodic, PQ conjectured unbounded | **To be determined** — likely no non-trivial recurrent subsequence |
| IV | Transcendental | Varies widely | **To be determined** — depends on Diophantine properties |

The central goal of this research is to fill in the "To be determined" entries with rigorous proofs or well-supported conjectures.
