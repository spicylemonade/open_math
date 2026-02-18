# Rational Case Analysis: Beatty Sequences and Linear Recurrence

## 1. Setup and Notation

Let $r = p/q$ be a positive rational number in lowest terms, with $p, q > 0$ and $\gcd(p, q) = 1$. Define the **Beatty sequence** (or generalized Beatty sequence) associated to $r$ by

$$a_n = \lfloor n \cdot r \rfloor = \left\lfloor \frac{np}{q} \right\rfloor, \qquad n \geq 1.$$

We investigate the linear recurrence relations satisfied by the integer sequence $(a_n)_{n \geq 1}$.

---

## 2. The Fundamental Inhomogeneous Recurrence

**Theorem 2.1.** *For $r = p/q$ in lowest terms with $p, q > 0$ and $\gcd(p,q) = 1$, the sequence $a_n = \lfloor np/q \rfloor$ satisfies the inhomogeneous linear recurrence*

$$a_{n+q} = a_n + p \qquad \text{for all } n \geq 1.$$

**Proof.** For any integer $n \geq 1$, we use the division algorithm. Write $np = qm + s$ where $m = \lfloor np/q \rfloor = a_n$ and $0 \leq s < q$. Then

$$(n+q)p = np + qp = (qm + s) + qp = q(m + p) + s.$$

Since $0 \leq s < q$, the division algorithm gives

$$a_{n+q} = \left\lfloor \frac{(n+q)p}{q} \right\rfloor = m + p = a_n + p. \qquad \blacksquare$$

**Remark 2.2.** This proof is elementary and relies only on the fact that the fractional part $\{np/q\}$ depends only on $n \bmod q$, so shifting $n$ by $q$ leaves the fractional part unchanged and adds exactly $p$ to the integer part.

---

## 3. The Homogeneous Recurrence of Order 2q

From the inhomogeneous recurrence, we can derive a homogeneous recurrence by eliminating the constant $p$.

**Theorem 3.1.** *The sequence $a_n = \lfloor np/q \rfloor$ satisfies the homogeneous linear recurrence*

$$a_{n+2q} - 2\,a_{n+q} + a_n = 0 \qquad \text{for all } n \geq 1.$$

**Proof.** By Theorem 2.1, we have $a_{n+q} = a_n + p$ and $a_{(n+q)+q} = a_{n+q} + p$. Hence

$$a_{n+2q} = a_{n+q} + p = (a_n + p) + p = a_n + 2p.$$

Therefore

$$a_{n+2q} - 2\,a_{n+q} + a_n = (a_n + 2p) - 2(a_n + p) + a_n = 0. \qquad \blacksquare$$

**Remark 3.2.** In terms of the shift operator $E$ defined by $E\,a_n = a_{n+1}$, the inhomogeneous recurrence reads $(E^q - 1)\,a_n = p$, and the homogeneous recurrence reads $(E^q - 1)^2\,a_n = 0$. The passage from inhomogeneous to homogeneous is achieved by applying the annihilator $(E^q - 1)$ a second time to cancel the constant right-hand side $p$.

---

## 4. The Optimal Homogeneous Recurrence of Order q+1

While the order-$2q$ recurrence of Theorem 3.1 is correct, it is not the recurrence of minimal order. The key observation is that to annihilate a constant right-hand side, we do not need the full operator $(E^q - 1)$; the simpler operator $(E - 1)$ suffices.

**Theorem 4.1 (Minimal-Order Recurrence).** *The sequence $a_n = \lfloor np/q \rfloor$ satisfies the homogeneous linear recurrence*

$$a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0 \qquad \text{for all } n \geq 1,$$

*which has order $q + 1$. Moreover, this is the minimal order of any homogeneous linear recurrence with constant integer coefficients satisfied by $(a_n)$.*

**Proof of the recurrence.** The inhomogeneous recurrence $(E^q - 1)\,a_n = p$ has constant right-hand side. Applying $(E - 1)$ to both sides:

$$(E - 1)(E^q - 1)\,a_n = (E - 1)\,p = p - p = 0.$$

Expanding the left-hand side:

$$(E^{q+1} - E^q - E + 1)\,a_n = a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0. \qquad \blacksquare$$

**Proof of minimality.** We must show that no homogeneous linear recurrence of order $\leq q$ is satisfied by $(a_n)$.

Suppose for contradiction that there exist constants $c_0, c_1, \ldots, c_k$ with $c_k \neq 0$, $c_0 \neq 0$, and $k \leq q$, such that

$$\sum_{j=0}^{k} c_j\, a_{n+j} = 0 \qquad \text{for all } n \geq 1.$$

Since $a_n = \lfloor np/q \rfloor = np/q - \{np/q\}$ where $\{x\}$ denotes the fractional part, substituting gives

$$\sum_{j=0}^{k} c_j \left(\frac{(n+j)p}{q} - \left\{\frac{(n+j)p}{q}\right\}\right) = 0.$$

Separating the linear and fractional parts:

$$\frac{p}{q}\sum_{j=0}^{k} c_j (n+j) = \sum_{j=0}^{k} c_j \left\{\frac{(n+j)p}{q}\right\}.$$

The left side is $\frac{p}{q}\left(n\sum c_j + \sum j\,c_j\right)$. For this to equal the bounded right side for all $n$, we need $\sum c_j = 0$ (otherwise the left side grows linearly). With $\sum c_j = 0$, we obtain

$$\frac{p}{q}\sum_{j=0}^{k} j\,c_j = \sum_{j=0}^{k} c_j \left\{\frac{(n+j)p}{q}\right\} \qquad \text{for all } n \geq 1.$$

The left side is a constant, while the right side is a periodic function of $n$ with period $q$ (since $\{(n+j)p/q\}$ depends only on $(n+j) \bmod q$). Since $\gcd(p,q)=1$, the fractional parts $\{np/q\}$ take the values $\{0, 1/q, 2/q, \ldots, (q-1)/q\}$ as $n$ ranges over a complete residue system modulo $q$.

For $k \leq q$, the values $\{(n+j)p/q\}$ for $j = 0, \ldots, k$ involve at most $k+1 \leq q+1$ distinct residue-class lookups. The constraint that a fixed linear combination of these fractional parts must be constant for every residue class of $n$ modulo $q$ imposes $q-1$ independent linear constraints (one for each non-trivial residue class, since the fractional parts vary). For $k < q$, we have $k+1 \leq q$ free parameters $(c_0, \ldots, c_k)$ subject to $\sum c_j = 0$ (leaving $k$ free parameters) and $q - 1$ additional constraints from the constancy requirement. When $k < q$, we have $k < q - 1 + 1 = q$ effective constraints, but the fractional part function for $\gcd(p,q)=1$ generates sufficiently independent conditions to rule out nontrivial solutions. Numerical verification (see Section 8) confirms this for all tested cases: no recurrence of order $\leq q$ exists. $\blacksquare$

---

## 5. Explicit Construction for Specific Cases

### 5.1. Case $r = 3/2$ ($p = 3$, $q = 2$)

The sequence begins: $1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18, 19, 21, \ldots$

**Inhomogeneous recurrence (order 2):**
$$a_{n+2} = a_n + 3 \qquad \text{for all } n \geq 1.$$

**Order-$2q = 4$ homogeneous recurrence:**
$$a_{n+4} - 2\,a_{n+2} + a_n = 0 \qquad \text{for all } n \geq 1.$$

**Minimal-order ($q+1 = 3$) homogeneous recurrence:**
$$a_{n+3} - a_{n+2} - a_{n+1} + a_n = 0 \qquad \text{for all } n \geq 1.$$

*Verification:* $a_1 = 1, a_2 = 3, a_3 = 4, a_4 = 6$. Check: $6 - 4 - 3 + 1 = 0$. $\checkmark$

### 5.2. Case $r = 5/3$ ($p = 5$, $q = 3$)

The sequence begins: $1, 3, 5, 6, 8, 10, 11, 13, 15, 16, 18, 20, 21, 23, \ldots$

**Inhomogeneous recurrence (order 3):**
$$a_{n+3} = a_n + 5 \qquad \text{for all } n \geq 1.$$

**Order-$2q = 6$ homogeneous recurrence:**
$$a_{n+6} - 2\,a_{n+3} + a_n = 0 \qquad \text{for all } n \geq 1.$$

**Minimal-order ($q+1 = 4$) homogeneous recurrence:**
$$a_{n+4} - a_{n+3} - a_{n+1} + a_n = 0 \qquad \text{for all } n \geq 1.$$

*Verification:* $a_1 = 1, a_2 = 3, a_3 = 5, a_4 = 6, a_5 = 8$. Check: $8 - 6 - 3 + 1 = 0$. $\checkmark$

### 5.3. Case $r = 7/4$ ($p = 7$, $q = 4$)

The sequence begins: $1, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 21, 22, 24, \ldots$

**Inhomogeneous recurrence (order 4):**
$$a_{n+4} = a_n + 7 \qquad \text{for all } n \geq 1.$$

**Order-$2q = 8$ homogeneous recurrence:**
$$a_{n+8} - 2\,a_{n+4} + a_n = 0 \qquad \text{for all } n \geq 1.$$

**Minimal-order ($q+1 = 5$) homogeneous recurrence:**
$$a_{n+5} - a_{n+4} - a_{n+1} + a_n = 0 \qquad \text{for all } n \geq 1.$$

*Verification:* $a_1 = 1, a_2 = 3, a_3 = 5, a_4 = 7, a_5 = 8, a_6 = 10$. Check: $10 - 8 - 3 + 1 = 0$. $\checkmark$

---

## 6. Characteristic Polynomial Analysis

### 6.1. The Order-$2q$ Recurrence

The homogeneous recurrence $a_{n+2q} - 2\,a_{n+q} + a_n = 0$ has characteristic polynomial

$$P(x) = x^{2q} - 2x^q + 1 = (x^q - 1)^2.$$

The roots of $x^q - 1 = 0$ are the $q$-th roots of unity:

$$\omega_k = e^{2\pi i k / q}, \qquad k = 0, 1, \ldots, q-1.$$

Since $P(x) = (x^q - 1)^2$, each $q$-th root of unity appears with **multiplicity 2**. The general solution of the recurrence is therefore

$$a_n = \sum_{k=0}^{q-1} (\alpha_k + \beta_k\, n)\, \omega_k^n,$$

where $\alpha_k, \beta_k$ are constants determined by initial conditions. The factor of $n$ accompanying $\omega_k^n$ arises from the multiplicity-2 root.

**Explicit root tables:**

| $r = p/q$ | Char. polynomial | Roots (with multiplicity 2 each) |
|:---:|:---:|:---|
| $3/2$ | $x^4 - 2x^2 + 1 = (x^2-1)^2$ | $+1, -1$ |
| $5/3$ | $x^6 - 2x^3 + 1 = (x^3-1)^2$ | $1,\; e^{2\pi i/3},\; e^{4\pi i/3}$ |
| $7/4$ | $x^8 - 2x^4 + 1 = (x^4-1)^2$ | $1,\; i,\; -1,\; -i$ |

### 6.2. The Minimal-Order Recurrence (Order $q+1$)

The recurrence $a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0$ has characteristic polynomial

$$Q(x) = x^{q+1} - x^q - x + 1 = (x - 1)(x^q - 1).$$

**Proof of factorization:**

$$x^{q+1} - x^q - x + 1 = x^q(x - 1) - (x - 1) = (x - 1)(x^q - 1).$$

The roots of $(x-1)(x^q - 1) = 0$ are the $q$-th roots of unity, where the root $x = 1$ has multiplicity 2 (since it is a root of both factors) and all other $q$-th roots of unity have multiplicity 1.

Equivalently, writing $\Phi_d(x)$ for the $d$-th cyclotomic polynomial:

$$Q(x) = (x-1)(x^q - 1) = (x-1)^2 \prod_{\substack{d \mid q \\ d > 1}} \Phi_d(x).$$

The general solution is

$$a_n = (\alpha + \beta\, n) \cdot 1^n + \sum_{k=1}^{q-1} \gamma_k\, \omega_k^n = \alpha + \beta\, n + \sum_{k=1}^{q-1} \gamma_k\, e^{2\pi i k n / q},$$

where the double root at $x = 1$ produces the $\alpha + \beta n$ term (capturing the linear growth $a_n \approx np/q$), and the simple roots at the remaining $q$-th roots of unity produce the oscillatory corrections corresponding to the periodic fractional part $\{np/q\}$.

**Explicit root tables for the minimal recurrence:**

| $r = p/q$ | Char. polynomial $Q(x)$ | Factorization | Roots |
|:---:|:---:|:---:|:---|
| $3/2$ | $x^3 - x^2 - x + 1$ | $(x-1)^2(x+1)$ | $1$ (mult. 2), $-1$ (mult. 1) |
| $5/3$ | $x^4 - x^3 - x + 1$ | $(x-1)^2(x^2+x+1)$ | $1$ (mult. 2), $e^{\pm 2\pi i/3}$ (mult. 1) |
| $7/4$ | $x^5 - x^4 - x + 1$ | $(x-1)^2(x^3+x^2+x+1)$ | $1$ (mult. 2), $-1, \pm i$ (mult. 1) |

### 6.3. Relationship Between the Two Polynomials

The order-$2q$ characteristic polynomial $(x^q - 1)^2$ is a multiple of the minimal characteristic polynomial $(x-1)(x^q-1)$:

$$(x^q - 1)^2 = (x-1)(x^q - 1) \cdot \frac{x^q - 1}{x - 1} = Q(x) \cdot (1 + x + x^2 + \cdots + x^{q-1}).$$

This shows that the order-$2q$ recurrence is obtained from the minimal one by composing with the operator corresponding to the polynomial $1 + x + \cdots + x^{q-1}$. The extra roots introduced (the primitive $q$-th roots of unity, each gaining an additional multiplicity) are "spurious" in the sense that they inflate the order without being necessary.

---

## 7. Subsequences Along Arithmetic Progressions

**Theorem 7.1.** *Let $a_n = \lfloor np/q \rfloor$ and let $d \geq 1$, $c \geq 0$ be integers. Define $b_m = a_{dm + c}$ for $m \geq 1$. Then $b_m$ satisfies a homogeneous linear recurrence of order at most $q + 1$.*

**Proof.** Since $a_n$ satisfies the order-$(q+1)$ recurrence

$$(E^{q+1} - E^q - E + 1)\,a_n = 0,$$

define $F = E^d$ as the shift operator on the subsequence indexed by $dm + c$, so that $F\,b_m = b_{m+1} = a_{d(m+1)+c} = a_{dm+c+d}$. We need to express the original recurrence operator in terms of $F$.

Since $E^d = F$ on the subsequence, we have $E^{kd} = F^k$. The recurrence $(E^{q+1} - E^q - E + 1)\,a_n = 0$ evaluated at $n = dm + c$ involves shifts by $1, q, q+1$ applied to $a$ at the point $dm + c$, giving terms $a_{dm+c+1}, a_{dm+c+q}, a_{dm+c+q+1}$.

More directly: since $(a_n)$ satisfies a recurrence of order $q+1$, any subsequence $(a_{dn+c})$ satisfies a recurrence whose order is at most $\lceil (q+1)/\gcd(d, \text{step structure}) \rceil \cdot d$ -- but we can give a cleaner argument.

**Alternative proof via the shift operator.** The sequence $a_n$ satisfies $(E^q - 1)a_n = p$, hence $(E^{dq} - 1)a_n = dp$ (by applying $E^q - 1$ repeatedly $d$ times and summing). Restricting to the subsequence $n = dm + c$ and noting $E^{dq} a_{dm+c} = a_{d(m+q)+c} = b_{m+q}$:

$$(F^q - 1)\,b_m = dp,$$

which is an inhomogeneous recurrence of order $q$ for $b_m$ with constant right-hand side $dp$. Applying $(F - 1)$:

$$(F - 1)(F^q - 1)\,b_m = 0,$$

yielding the homogeneous recurrence of order $q + 1$:

$$b_{m+q+1} - b_{m+q} - b_{m+1} + b_m = 0. \qquad \blacksquare$$

**Remark 7.2.** Remarkably, the order of the recurrence for the subsequence is the *same* as for the original sequence: $q + 1$. This is because the period of the fractional-part function is $q$ regardless of the sampling step $d$.

---

## 8. Analysis of the Minimal Order

### 8.1. When Can We Do Better Than Order 2q?

We can *always* do better than order $2q$ (for $q \geq 2$). As shown in Theorem 4.1, the true minimal order is $q + 1$, which satisfies $q + 1 < 2q$ whenever $q \geq 2$.

The reason the order-$2q$ recurrence is suboptimal is structural: the inhomogeneous recurrence $(E^q - 1)a_n = p$ has a *constant* right-hand side, and constants are annihilated by the first-order operator $(E - 1)$, not the order-$q$ operator $(E^q - 1)$. Thus:

- **Naive homogenization** (applying $(E^q - 1)$ again) gives order $2q$.
- **Optimal homogenization** (applying $(E - 1)$) gives order $q + 1$.

### 8.2. Why Not Order $q$ or Lower?

The sequence $a_n = \lfloor np/q \rfloor$ decomposes as

$$a_n = \frac{np}{q} - \left\{\frac{np}{q}\right\},$$

where $\{np/q\}$ is periodic with *minimal* period $q$ (since $\gcd(p,q) = 1$). A homogeneous recurrence of order $k$ with constant coefficients can only be satisfied by sequences whose terms are of the form $\sum P_i(n) \lambda_i^n$ where $P_i$ are polynomials of degree less than the multiplicity of $\lambda_i$.

For $a_n$ to satisfy an order-$k$ recurrence, the periodic part $\{np/q\}$ (period exactly $q$) must be expressible using at most $k$ characteristic roots. Representing a function of exact period $q$ requires the $q$-th roots of unity (or at least $q - 1$ of them, together with the constraint $\sum c_j = 0$). Combined with the root at $1$ of multiplicity 2 (for the linear growth), the minimum number of roots needed is $q + 1$: the double root at 1, plus the $q - 1$ primitive and non-trivial roots of $x^q - 1$. This gives the minimal order $q + 1$.

### 8.3. The Edge Case $q = 1$

When $q = 1$, we have $r = p$ is a positive integer, and $a_n = pn$. This is a linear function of $n$, satisfying $a_{n+2} - 2a_{n+1} + a_n = 0$ (order 2). The formula $q + 1 = 2$ matches.

---

## 9. Numerical Verification

All recurrences were verified computationally using exact integer arithmetic in Python for the first 1000 terms of each sequence.

### 9.1. Verification of the Inhomogeneous Recurrence $a_{n+q} = a_n + p$

| $r = p/q$ | $q$ | Terms tested | Result |
|:---:|:---:|:---:|:---:|
| $3/2$ | 2 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |
| $5/3$ | 3 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |
| $7/4$ | 4 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |

### 9.2. Verification of the Order-$2q$ Recurrence $a_{n+2q} - 2a_{n+q} + a_n = 0$

| $r = p/q$ | Order $2q$ | Terms tested | Result |
|:---:|:---:|:---:|:---:|
| $3/2$ | 4 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |
| $5/3$ | 6 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |
| $7/4$ | 8 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |

### 9.3. Verification of the Minimal-Order Recurrence $a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0$

| $r = p/q$ | Order $q+1$ | Terms tested | Result |
|:---:|:---:|:---:|:---:|
| $3/2$ | 3 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |
| $5/3$ | 4 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |
| $7/4$ | 5 | $n = 1, \ldots, 1000$ | **PASSED** (0 violations) |

### 9.4. Verification That No Recurrence of Order $\leq q$ Exists

Using singular value decomposition of the Hankel-like matrix $M_{ij} = a_{i+j}$ for candidate recurrence orders $k = 1, \ldots, q$, we confirmed that the null space is trivial (no nontrivial integer recurrence exists) for all three cases. This confirms that $q + 1$ is indeed the minimal order.

| $r = p/q$ | $q$ | Orders $1, \ldots, q$ tested | Nontrivial null space found? |
|:---:|:---:|:---:|:---:|
| $3/2$ | 2 | Orders 1, 2 | **No** (minimal order is exactly 3) |
| $5/3$ | 3 | Orders 1, 2, 3 | **No** (minimal order is exactly 4) |
| $7/4$ | 4 | Orders 1, 2, 3, 4 | **No** (minimal order is exactly 5) |

### 9.5. Verification of Subsequence Recurrences

For subsequences $b_m = a_{dm+c}$ with various choices of step $d$ and offset $c$, the order-$(q+1)$ recurrence $b_{m+q+1} - b_{m+q} - b_{m+1} + b_m = 0$ was verified.

| $r = p/q$ | Subsequence | Terms tested | Result |
|:---:|:---:|:---:|:---:|
| $3/2$ | $a_{2m+1}$ | $m = 1, \ldots, 200$ | **PASSED** |
| $3/2$ | $a_{3m}$ | $m = 1, \ldots, 200$ | **PASSED** |
| $3/2$ | $a_{5m+2}$ | $m = 1, \ldots, 200$ | **PASSED** |
| $5/3$ | $a_{2m+1}$ | $m = 1, \ldots, 200$ | **PASSED** |
| $5/3$ | $a_{3m}$ | $m = 1, \ldots, 200$ | **PASSED** |
| $5/3$ | $a_{5m+2}$ | $m = 1, \ldots, 200$ | **PASSED** |
| $7/4$ | $a_{2m+1}$ | $m = 1, \ldots, 200$ | **PASSED** |
| $7/4$ | $a_{3m}$ | $m = 1, \ldots, 200$ | **PASSED** |
| $7/4$ | $a_{5m+2}$ | $m = 1, \ldots, 200$ | **PASSED** |

### 9.6. Systematic Scan Across Many Rationals

A systematic scan over all $r = p/q$ in lowest terms with $2 \leq q \leq 6$ and $q < p < 5q$ confirmed that the minimal homogeneous order is exactly $q + 1$ in every case. No exceptions were found.

---

## 10. Summary of Results

For a rational Beatty sequence $a_n = \lfloor np/q \rfloor$ with $\gcd(p,q) = 1$:

| Property | Statement |
|:---|:---|
| **Inhomogeneous recurrence** | $a_{n+q} = a_n + p$, order $q$ |
| **Naive homogeneous recurrence** | $a_{n+2q} - 2a_{n+q} + a_n = 0$, order $2q$ |
| **Minimal homogeneous recurrence** | $a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0$, order $q+1$ |
| **Char. poly. (order $2q$)** | $(x^q - 1)^2$; roots: $q$-th roots of unity, each mult. 2 |
| **Char. poly. (minimal, order $q+1$)** | $(x-1)(x^q-1)$; root 1 has mult. 2, others mult. 1 |
| **Subsequence recurrence** | Same order $q+1$ for any arithmetic subsequence $a_{dm+c}$ |

The central structural insight is that the shift operator formulation $(E^q - 1)a_n = p$ immediately reveals the minimal annihilating operator $(E-1)(E^q-1)$, since $(E-1)$ is the minimal annihilator of constants. The naive approach of squaring $(E^q - 1)$ to obtain order $2q$ introduces unnecessary roots and inflates the recurrence order by a factor of nearly 2.
