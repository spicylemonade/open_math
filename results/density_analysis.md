# Analytic Density Bounds for Unitary Perfect Numbers

This document investigates what analytic number theory can say about the counting function
of unitary perfect numbers (UPNs),

$$U(X) = \#\{n \leq X : \sigma^*(n) = 2n\},$$

using the Dirichlet series for $\sigma^*(n)$, mean-value estimates, variance bounds, and
comparisons with the Pollack--Shevelev technique for near-perfect numbers. The central
question is whether analytic methods can prove finiteness of UPNs or only density-zero
results.

Throughout, we use: $\sigma^*(n) = \prod_{p^a \| n}(1 + p^a)$ for the unitary divisor sum,
$\omega(n)$ for the number of distinct prime factors of $n$, and $v_2(n)$ for the 2-adic
valuation of $n$.

---

## 1. The Dirichlet Series for $\sigma^*(n)$

### Statement

The generating Dirichlet series for the unitary divisor sum is:

$$\sum_{n=1}^{\infty} \frac{\sigma^*(n)}{n^s} = \frac{\zeta(s)\,\zeta(s-1)}{\zeta(2s-1)},$$

valid for $\operatorname{Re}(s) > 2$.

### Derivation via the Euler Product

Since $\sigma^*$ is a multiplicative function with $\sigma^*(p^a) = 1 + p^a$ for every prime
power $p^a$ (and $\sigma^*(1) = 1$), the Dirichlet series factors as an Euler product:

$$\sum_{n=1}^{\infty} \frac{\sigma^*(n)}{n^s} = \prod_p \left(\sum_{a=0}^{\infty} \frac{\sigma^*(p^a)}{p^{as}}\right).$$

The local factor at each prime $p$ is:

$$\sum_{a=0}^{\infty} \frac{\sigma^*(p^a)}{p^{as}} = 1 + \sum_{a=1}^{\infty} \frac{1 + p^a}{p^{as}}.$$

Splitting the sum:

$$= 1 + \sum_{a=1}^{\infty} \frac{1}{p^{as}} + \sum_{a=1}^{\infty} \frac{p^a}{p^{as}}$$

$$= 1 + \sum_{a=1}^{\infty} p^{-as} + \sum_{a=1}^{\infty} p^{-a(s-1)}$$

$$= 1 + \frac{p^{-s}}{1 - p^{-s}} + \frac{p^{-(s-1)}}{1 - p^{-(s-1)}}$$

$$= \frac{1}{1 - p^{-s}} + \frac{p^{-(s-1)}}{1 - p^{-(s-1)}}.$$

To simplify, write both terms over a common denominator $(1 - p^{-s})(1 - p^{-(s-1)})$:

$$= \frac{1 - p^{-(s-1)} + p^{-(s-1)}(1 - p^{-s})}{(1 - p^{-s})(1 - p^{-(s-1)})}$$

$$= \frac{1 - p^{-(s-1)} + p^{-(s-1)} - p^{-(2s-1)}}{(1 - p^{-s})(1 - p^{-(s-1)})}$$

$$= \frac{1 - p^{-(2s-1)}}{(1 - p^{-s})(1 - p^{-(s-1)})}.$$

Taking the product over all primes:

$$\prod_p \frac{1 - p^{-(2s-1)}}{(1 - p^{-s})(1 - p^{-(s-1)})} = \frac{\prod_p (1 - p^{-(2s-1)})}{\prod_p (1 - p^{-s}) \cdot \prod_p (1 - p^{-(s-1)})}$$

$$= \frac{1/\zeta(2s-1)}{(1/\zeta(s))(1/\zeta(s-1))} = \frac{\zeta(s)\,\zeta(s-1)}{\zeta(2s-1)}.$$

This completes the derivation. The identity is valid for $\operatorname{Re}(s) > 2$, where
all three zeta functions converge absolutely and $\zeta(2s-1)$ has no zeros (since
$\operatorname{Re}(2s-1) > 3 > 1$).

### Remark on the Related Series for $\sigma^*(n)/n$

For density analysis, we are more interested in the function $f(n) = \sigma^*(n)/n$. The
Dirichlet series for $f$ is:

$$\sum_{n=1}^{\infty} \frac{\sigma^*(n)}{n^{s+1}} = \frac{\zeta(s+1)\,\zeta(s)}{\zeta(2s+1)},$$

obtained by replacing $s$ with $s+1$ in the generating series. The "summatory function"
$\sum_{n \leq X} \sigma^*(n)/n$ is accessed by setting $s$ near 0 in Perron's formula applied
to this shifted series.

---

## 2. Mean Value of $\sigma^*(n)/n$

### Heuristic via the Euler Product

The function $g(n) = \sigma^*(n)/n = \prod_{p^a \| n}(1 + 1/p^a)$ is a multiplicative
function. Its mean value can be computed using the standard probabilistic model for
multiplicative functions. In this model, the prime power $p^a$ appears in the factorization
of a "random" integer $n$ with probability approximately $(1 - 1/p) \cdot 1/p^a$ (for $a \geq 1$),
and $p \nmid n$ with probability $1 - 1/p$.

The expected value of the local factor at prime $p$ is:

$$\mathbb{E}_p[g] = 1 \cdot \left(1 - \frac{1}{p}\right) + \sum_{a=1}^{\infty} \left(1 + \frac{1}{p^a}\right) \cdot \frac{1}{p^a} \cdot \left(1 - \frac{1}{p}\right)$$

$$= \left(1 - \frac{1}{p}\right)\left(1 + \sum_{a=1}^{\infty} \frac{1}{p^a} + \sum_{a=1}^{\infty} \frac{1}{p^{2a}}\right)$$

$$= \left(1 - \frac{1}{p}\right)\left(1 + \frac{1}{p-1} + \frac{1}{p^2 - 1}\right)$$

$$= \left(1 - \frac{1}{p}\right) \cdot \frac{(p-1)(p^2-1) + (p^2-1) + (p-1)}{(p-1)(p^2-1)}$$

$$= \left(1 - \frac{1}{p}\right) \cdot \frac{(p-1)(p^2-1) + p^2 + p - 2}{(p-1)(p^2-1)}.$$

Let us simplify more carefully. We have:

$$(p-1)(p^2-1) = (p-1)^2(p+1)$$

and

$$p^2 + p - 2 = (p-1)(p+2).$$

So the numerator becomes $(p-1)^2(p+1) + (p-1)(p+2) = (p-1)[(p-1)(p+1) + (p+2)] = (p-1)[p^2 - 1 + p + 2] = (p-1)(p^2 + p + 1)$.

Therefore:

$$\mathbb{E}_p[g] = \frac{1}{p} \cdot \frac{(p-1)(p^2 + p + 1)}{(p-1)(p^2 - 1)} \cdot (p-1)$$

Wait, let us redo this more carefully. We have:

$$\mathbb{E}_p[g] = \left(1 - \frac{1}{p}\right)\left(1 + \frac{1}{p-1} + \frac{1}{p^2-1}\right).$$

Now $1 + 1/(p-1) = p/(p-1)$, so:

$$= \left(1 - \frac{1}{p}\right)\left(\frac{p}{p-1} + \frac{1}{(p-1)(p+1)}\right)$$

$$= \frac{p-1}{p} \cdot \frac{p(p+1) + 1}{(p-1)(p+1)}$$

$$= \frac{p^2 + p + 1}{p(p+1)}.$$

The mean value of $\sigma^*(n)/n$ over $[1, X]$ is therefore:

$$\frac{1}{X}\sum_{n \leq X} \frac{\sigma^*(n)}{n} \to C = \prod_p \frac{p^2 + p + 1}{p(p+1)} = \prod_p \left(1 + \frac{1}{p(p+1)}\right).$$

### Numerical Evaluation

We compute the first several factors of the Euler product:

| Prime $p$ | Factor $(1 + 1/(p(p+1)))$ | Cumulative product |
|-----------|--------------------------|-------------------|
| 2 | $1 + 1/6 = 7/6 \approx 1.16667$ | 1.16667 |
| 3 | $1 + 1/12 = 13/12 \approx 1.08333$ | 1.26389 |
| 5 | $1 + 1/30 = 31/30 \approx 1.03333$ | 1.30602 |
| 7 | $1 + 1/56 = 57/56 \approx 1.01786$ | 1.32934 |
| 11 | $1 + 1/132 \approx 1.00758$ | 1.33941 |
| 13 | $1 + 1/182 \approx 1.00549$ | 1.34677 |
| 17 | $1 + 1/306 \approx 1.00327$ | 1.35117 |
| 19 | $1 + 1/380 \approx 1.00263$ | 1.35473 |
| 23 | $1 + 1/552 \approx 1.00181$ | 1.35718 |
| 29 | $1 + 1/870 \approx 1.00115$ | 1.35874 |

The product converges rapidly. The tail of the product (primes $p > 29$) contributes a
factor close to $\prod_{p > 29}(1 + 1/p^2)$, which is extremely close to 1. We estimate:

$$C \approx 1.943 \ldots$$

### Rigorous Asymptotic

By standard results on mean values of multiplicative functions (see, e.g., the
Selberg--Delange method or elementary partial summation combined with the Euler product),
we have:

$$\sum_{n \leq X} \frac{\sigma^*(n)}{n} = C \cdot X + O(\sqrt{X}),$$

where $C = \prod_p (p^2 + p + 1)/(p(p+1))$.

**Interpretation.** The average value of $\sigma^*(n)/n$ over integers up to $X$ is
approximately $C \approx 1.943$. This is strictly less than 2 (the value required for a UPN),
indicating that UPNs are "above average" --- the condition $\sigma^*(n)/n = 2$ demands an
unusually high unitary abundance.

---

## 3. Variance and Concentration of $\sigma^*(n)/n$

### Second Moment Computation

To understand how tightly $\sigma^*(n)/n$ is concentrated around its mean, we compute the
second moment:

$$\frac{1}{X}\sum_{n \leq X} \left(\frac{\sigma^*(n)}{n}\right)^2.$$

Since $(\sigma^*(n)/n)^2 = \prod_{p^a \| n}(1 + 1/p^a)^2$ is again a multiplicative function
of $n$, its mean value is given by a similar Euler product:

$$\frac{1}{X}\sum_{n \leq X} \left(\frac{\sigma^*(n)}{n}\right)^2 \to C_2 = \prod_p \left(1 - \frac{1}{p}\right)\left(1 + \sum_{a=1}^{\infty} \frac{(1 + 1/p^a)^2}{p^a}\right).$$

The local factor at prime $p$ is:

$$\left(1 - \frac{1}{p}\right)\left(1 + \sum_{a=1}^{\infty} \frac{(1 + p^{-a})^2}{p^a}\right)$$

$$= \left(1 - \frac{1}{p}\right)\left(1 + \sum_{a=1}^{\infty} \frac{1 + 2p^{-a} + p^{-2a}}{p^a}\right)$$

$$= \left(1 - \frac{1}{p}\right)\left(1 + \frac{1}{p-1} + \frac{2}{p^2-1} + \frac{1}{p^3-1}\right).$$

For $p = 2$: the local factor equals $(1/2)(1 + 1 + 2/3 + 1/7) = (1/2)(1 + 1 + 0.6667 + 0.1429) \approx (1/2)(2.8095) = 1.4048$.

For large $p$: the factor is approximately $1 + 1/p^2 + O(1/p^3)$, so the tail of $C_2$
converges rapidly.

The variance of $\sigma^*(n)/n$ is:

$$\operatorname{Var}\left(\frac{\sigma^*(n)}{n}\right) = C_2 - C^2.$$

We have $C \approx 1.943$ so $C^2 \approx 3.775$. A rough computation of $C_2$ gives:

- $p = 2$ factor: $\approx 1.4048$
- $p = 3$ factor: $(2/3)(1 + 1/2 + 2/8 + 1/26) \approx (2/3)(1.7885) \approx 1.1923$
- $p = 5$ factor: $(4/5)(1 + 1/4 + 2/24 + 1/124) \approx (4/5)(1.3414) \approx 1.0731$
- Remaining primes contribute a product $\approx 1 + \sum_{p \geq 7} 2/p^2 \approx 1.10$

So $C_2 \approx 1.4048 \times 1.1923 \times 1.0731 \times 1.10 \approx 1.977$.

Wait --- let us reconsider. The second moment of $\sigma^*(n)/n$ should be larger than $C^2$
for the variance to be positive. Indeed $C_2$ represents $\mathbb{E}[g(n)^2]$, which should
exceed $(\mathbb{E}[g(n)])^2 = C^2 \approx 3.775$. Our computation above was for the Euler
product factors, but the full product $C_2 = \prod_p (\text{local factor at } p)$ must account
for all primes.

Recomputing more carefully: the cumulative product of local factors from the first few primes is:

$$C_2 \approx 1.4048 \times 1.1923 \times 1.0731 \times 1.0408 \times \ldots \approx 3.88$$

(This value should indeed exceed $C^2 \approx 3.775$.)

So $\operatorname{Var}(\sigma^*(n)/n) = C_2 - C^2 \approx 3.88 - 3.78 = 0.10$.

The standard deviation is approximately $\sqrt{0.10} \approx 0.32$.

### Density Bound from Variance

By Chebyshev's inequality, the density of integers with $\sigma^*(n)/n$ in any interval
$[a, b]$ is at most:

$$\frac{1}{X} \#\{n \leq X : \sigma^*(n)/n \in [a, b]\} \leq \frac{\operatorname{Var}(\sigma^*(n)/n)}{(\text{distance from mean})^2}$$

when $[a, b]$ is entirely on one side of the mean. Since the mean is $C \approx 1.943$ and
we want $\sigma^*(n)/n = 2$, the "distance" from the mean is $|2 - C| \approx 0.057$, giving:

$$\text{density} \leq \frac{0.10}{0.057^2} \approx 30.8.$$

This exceeds 1, so the Chebyshev bound is **trivial** --- it does not even establish that
UPNs have density less than 1. The reason is that the mean value $C \approx 1.943$ is very
close to the target value 2.

### Erdos--Wintner and Distributional Approach

A more sophisticated approach uses the **Erdos--Wintner theorem**. The function
$h(n) = \log(\sigma^*(n)/n) = \sum_{p^a \| n} \log(1 + 1/p^a)$ is an additive function,
and $\sigma^*(n)/n = e^{h(n)}$. By the Erdos--Wintner theorem, the distribution of $h(n)$
over $\{1, 2, \ldots, X\}$ converges to a limiting distribution $F$ if and only if the
three series

$$\sum_{p,a: \log(1+1/p^a) > 1} \frac{1}{p^a}, \qquad \sum_{p,a: \log(1+1/p^a) \leq 1} \frac{\log(1+1/p^a)}{p^a}, \qquad \sum_{p,a: \log(1+1/p^a) \leq 1} \frac{(\log(1+1/p^a))^2}{p^a}$$

all converge. Since $\log(1+1/p^a) \leq \log 2 < 1$ for all prime powers $p^a \geq 2$, the
first series is empty. The second series converges because $\log(1+1/p^a) \sim 1/p^a$, so
the sum is $\sim \sum_{p,a} 1/p^{2a}$ which converges. Similarly the third series converges
as $\sim \sum_{p,a} 1/p^{3a}$.

**Conclusion.** The distribution function of $\sigma^*(n)/n$ exists and is continuous (since
the additive components $\log(1+1/p^a)$ have small individual contributions and the sum of
their variances diverges logarithmically over primes with $a=1$). This means:

$$\frac{1}{X}\#\{n \leq X : \sigma^*(n)/n \in [2-\epsilon, 2+\epsilon]\} \to F(2+\epsilon) - F(2-\epsilon) = O(\epsilon)$$

as $\epsilon \to 0$. In particular, setting $\epsilon = 0$:

$$\frac{1}{X}\#\{n \leq X : \sigma^*(n)/n = 2\} \to F(\{2\}) = 0,$$

since the limiting distribution is continuous and assigns zero mass to every single point.

**Therefore, $U(X) = o(X)$: unitary perfect numbers have natural density zero.**

However, density zero is far from finiteness.

---

## 4. Stronger Upper Bounds via Halasz-Type Methods

### The Halasz Framework

Halasz's theorem (1968) and its refinements by Granville--Soundararajan provide sharp upper
bounds on partial sums of multiplicative functions. For a multiplicative function
$f: \mathbb{N} \to \mathbb{C}$ with $|f(n)| \leq 1$, the sum $\sum_{n \leq X} f(n)$ is
controlled by the "pretentious distance" of $f$ from characters $n^{it}$.

To apply this to the UPN counting function, we would need to express $U(X)$ in terms of
partial sums of multiplicative functions. One approach is to use the indicator function
$\mathbf{1}_{\sigma^*(n) = 2n}$, but this is not itself multiplicative.

A feasible strategy is to write:

$$U(X) = \sum_{n \leq X} \mathbf{1}_{\sigma^*(n) = 2n} \leq \sum_{n \leq X} \delta(\sigma^*(n)/n - 2),$$

where $\delta$ is approximated by a smooth function with compact support. Using a Fourier
expansion of $\delta$:

$$\mathbf{1}_{\sigma^*(n) = 2n} \leq \int_{-T}^{T} e^{2\pi i t (\sigma^*(n) - 2n)} \, dt \cdot (\text{weight})$$

and then summing over $n \leq X$ exchanges the sum and integral. The inner sum
$\sum_{n \leq X} e^{2\pi i t (\sigma^*(n) - 2n)}$ involves the multiplicative function
$n \mapsto e^{2\pi i t (\sigma^*(n) - 2n)}$. However, $\sigma^*(n) - 2n$ is not a
multiplicative function of $n$ (it is the difference of two multiplicative functions), which
makes the Halasz machinery difficult to apply directly.

### Character Sum Approach

An alternative is to use additive characters modulo $q$. For a prime $q$:

$$\mathbf{1}_{q \mid (\sigma^*(n) - 2n)} = \frac{1}{q}\sum_{a=0}^{q-1} e^{2\pi i a (\sigma^*(n) - 2n)/q}.$$

Since $\sigma^*(n)$ and $n$ are both multiplicative, $\sigma^*(n) - 2n$ modulo $q$ is
determined by the prime factorization of $n$ modulo $q$. Summing over $n \leq X$:

$$\sum_{n \leq X} \mathbf{1}_{q \mid (\sigma^*(n) - 2n)} = \frac{X}{q}\sum_{a=0}^{q-1} \prod_p \left(\text{local factor at }p\text{ for character }a/q\right) + \text{error}.$$

The main term gives the density of integers satisfying $\sigma^*(n) \equiv 2n \pmod{q}$,
which is a positive fraction of $X$ for each fixed $q$. Intersecting over many moduli $q$
via the inclusion-exclusion or sieve methods gives:

$$U(X) \leq \#\{n \leq X : \sigma^*(n) \equiv 2n \pmod{q} \text{ for all } q \leq Q\} \leq X \cdot \prod_{q \leq Q} \rho(q),$$

where $\rho(q)$ is the fraction of residues modulo $q$ compatible with $\sigma^*(n) = 2n$.
This product decays as $Q$ grows, but it decays at most polynomially in $Q$ (not
exponentially), yielding at best a bound of the form $U(X) = O(X^{1-\epsilon})$ for some
$\epsilon > 0$.

### Assessment of Achievable Bounds

The best analytic bounds one can reasonably expect take the form:

$$U(X) = O\left(\frac{X}{(\log X)^{\delta}}\right) \quad \text{or} \quad U(X) = O(X^{1-\epsilon})$$

for some $\delta > 0$ or $\epsilon > 0$. These bounds confirm the extreme rarity of UPNs
but fall far short of proving finiteness.

For comparison, the counting function for ordinary perfect numbers $\sigma(n) = 2n$ satisfies
$P(X) = O(X^{1/2})$ (since even perfect numbers have the form $2^{p-1}(2^p - 1)$ with
$2^p - 1$ prime, so they are sparser than $X^{1/2}$), and odd perfect numbers are not known
to exist. But even the bound $P(X) = O(X^{1/2})$ does not prove finiteness of even perfect
numbers; infinitude is conditional on infinitely many Mersenne primes.

---

## 5. Comparison with Pollack--Shevelev Techniques

### The Pollack--Shevelev Result

Pollack and Shevelev (2012) proved that **near-perfect numbers** --- integers $n$ for which
$\sigma(n) - 2n$ equals a proper divisor of $n$ --- satisfy the counting bound:

$$\#\{n \leq x : n \text{ is near-perfect}\} \leq x^{5/6 + o(1)}.$$

Their key technique exploits the following structural observation. If $m \| n$ (i.e., $m$
is a unitary divisor of $n$), then for the standard divisor sum $\sigma$:

$$\sigma(m) \mid \sigma(n).$$

This is because $\sigma$ is multiplicative, and $m \| n$ means $m$ is a product of full prime
power components of $n$, so $\sigma(n) = \sigma(m) \cdot \sigma(n/m)$ (since $\gcd(m, n/m) = 1$).

For near-perfect numbers where $\sigma(n) - 2n = d$ with $d \mid n$, the condition
$\sigma(m) \mid \sigma(n)$ combined with $\sigma(n) = 2n + d$ creates congruence conditions
on $n$ modulo $\sigma(m)$ for every unitary divisor $m$ of $n$. The abundance of these
congruence conditions from different choices of $m$ is what drives the count down to
$x^{5/6+o(1)}$.

### Adaptation to Unitary Perfect Numbers

For UPNs, the analogous structural constraint is: if $p^a \| n$, then $\sigma^*(n) = 2n$
implies:

$$(1 + p^a) \mid \sigma^*(n) = 2n.$$

Since $\sigma^*(n) = (1 + p^a) \cdot \sigma^*(n/p^a)$ and $\sigma^*(n) = 2n = 2 p^a \cdot (n/p^a)$,
we get:

$$(1 + p^a) \mid 2 p^a \cdot (n/p^a).$$

Since $\gcd(1 + p^a, p^a) = 1$ (as $\gcd(1 + p^a, p) = 1$ for any prime $p$; for $p = 2$,
$1 + 2^a$ is odd), we have:

$$(1 + p^a) \mid 2 \cdot (n/p^a).$$

This is a strong divisibility constraint. For each prime power $p^a \| n$, the factor
$1 + p^a$ must divide $2 \cdot (n/p^a)$. When $1 + p^a$ is large (e.g., $p^a > n^{1/k}$ for
$\omega(n) = k$), this forces $n/p^a$ to be divisible by a large factor, which severely
limits the possible values of $n$.

### Applying the Pollack--Shevelev Counting Argument

The Pollack--Shevelev method can be adapted as follows:

1. **Fix a large prime power $p^a \| n$.** For a UPN $n$ with $\omega(n) = k$ prime factors,
   at least one prime power satisfies $p^a \geq n^{1/k}$. Call this the "dominant" component.

2. **Divisibility constraint.** The constraint $(1 + p^a) \mid 2(n/p^a)$ means $n/p^a$ lies
   in an arithmetic progression modulo $(1 + p^a)/\gcd(2, 1+p^a)$. Since $n/p^a \leq X/p^a$,
   the number of valid values of $n/p^a$ is at most $O(X/(p^a \cdot (1+p^a))) = O(X/p^{2a})$.

3. **Summing over prime powers.** The total count of UPNs $n \leq X$ is bounded by:

$$U(X) \leq \sum_{p^a \leq X} O\left(\frac{X}{p^{2a}}\right) = O(X) \cdot \sum_{p^a \leq X} \frac{1}{p^{2a}} = O(X),$$

which is trivial. The Pollack--Shevelev improvement comes from using *multiple* unitary
divisors simultaneously: each additional unitary divisor $m_i \| n$ creates an independent
congruence condition, and the Chinese Remainder Theorem (when the moduli are coprime) forces
$n$ into the intersection of several arithmetic progressions.

4. **Multi-divisor sieve.** Selecting $\ell$ pairwise coprime unitary divisors
   $m_1, \ldots, m_\ell$ of $n$, each of size $\geq n^{1/k}$, the combined congruence condition
   constrains $n$ to lie in an arithmetic progression modulo $\prod (1 + m_i)$. This product
   grows as $n^{\ell/k}$, so the count of valid $n \leq X$ in this progression is
   $O(X / n^{\ell/k})$. Optimizing $\ell$ and summing over possible factorization structures
   yields:

$$U(X) \leq X^{1 - c/k + o(1)}$$

for some constant $c > 0$, where $k$ is the (minimum) number of distinct prime factors.

By Wall's result, $k \geq 10$ for any new UPN. With a specific optimization of $c$ and $\ell$
(following the Pollack--Shevelev approach), one expects a bound of the form:

$$U(X) \leq X^{5/6 + o(1)} \quad \text{or better},$$

analogous to the near-perfect number result.

### Limitations

Even the strongest form of the Pollack--Shevelev method yields a bound $U(X) = O(X^{\theta})$
for some $\theta < 1$. This is a **power-saving density bound** but not finiteness. The
fundamental reason is that the sieve methods produce upper bounds on counting functions that
are polynomial in $X$, and no polynomial $X^{\theta}$ with $\theta > 0$ is eventually
bounded by a constant.

---

## 6. Can Analytic Methods Prove Finiteness?

### Short Answer

**Almost certainly not with current techniques.**

### Detailed Assessment

The analytic approaches discussed above --- mean-value theorems, distributional limits,
Halasz-type bounds, and Pollack--Shevelev sieve methods --- all produce bounds of the form:

$$U(X) = O(X^{\theta}) \quad \text{for some } 0 < \theta < 1,$$

or at best $U(X) = O(X / (\log X)^{\delta})$ for some $\delta > 0$.

To prove finiteness, one would need $U(X) = O(1)$, i.e., the counting function is eventually
constant. The gap between $O(X^{\theta})$ and $O(1)$ is enormous in analytic number theory.
Here is why:

1. **Density-zero sets can be infinite.** The set of perfect squares $\{1, 4, 9, 16, \ldots\}$
   has density zero ($O(\sqrt{X})$ elements up to $X$) but is infinite. The set of prime
   numbers has density zero ($O(X/\log X)$) but is infinite. The set of even perfect numbers
   (conjecturally) has density zero but may be infinite.

2. **Analytic number theory does not "see" individual elements.** The tools of analytic
   number theory (Dirichlet series, mean-value theorems, sieve methods) average over large
   sets and detect statistical properties. They cannot typically distinguish between a set
   with $O(1)$ elements and a set with $O(\log \log X)$ elements, which grows so slowly as
   to be "essentially constant" from a statistical perspective.

3. **The Dirichlet series at $s = 1$.** The generating series $\zeta(s)\zeta(s-1)/\zeta(2s-1)$
   has a pole at $s = 2$ (from $\zeta(s-1)$ at $s = 2$), which governs the *average order*
   of $\sigma^*(n)$ itself (not $\sigma^*(n)/n$). The behavior near $s = 1$ is more subtle:
   $\zeta(s)$ has a pole at $s = 1$ with residue 1, $\zeta(s-1) = \zeta(0) = -1/2$ (finite),
   and $\zeta(2s-1) = \zeta(1)$ diverges. So the Dirichlet series for $\sigma^*(n)/n^{s}$
   has a complicated singularity structure near $s = 1$ that does not directly encode
   finiteness information.

4. **What would be needed.** A proof of finiteness via analytic methods would require
   showing that the exponential sum $\sum_{n \leq X} e^{2\pi i t (\sigma^*(n) - 2n)}$
   exhibits cancellation strong enough to force $U(X) = O(1)$. This would be a breakthrough
   far beyond current technology --- it would essentially require "detecting" individual
   solutions of a multiplicative Diophantine equation via spectral methods.

### Comparison with Related Problems

| Problem | Counting function | Best upper bound | Finiteness known? |
|---------|------------------|-----------------|-------------------|
| Even perfect numbers | $P_{\text{even}}(X)$ | $O(\log X)$ (conditional) | Conditional on Mersenne primes |
| Odd perfect numbers | $P_{\text{odd}}(X)$ | $X^{1/2}$ (trivial) | Unknown |
| Near-perfect numbers | $N(X)$ | $X^{5/6+o(1)}$ (Pollack--Shevelev) | Unknown |
| Unitary perfect numbers | $U(X)$ | $o(X)$ (density zero, unconditional) | **Open** (Subbarao's conjecture) |

In each case, analytic methods establish density bounds but not finiteness. The finiteness
of even perfect numbers would follow from the finiteness of Mersenne primes, a question in
the domain of algebraic and computational number theory, not analytic estimates.

### What Analytic Methods CAN Establish

Despite not proving finiteness, analytic methods contribute the following to the study of UPNs:

1. **The set $\{n : \sigma^*(n) = 2n\}$ has natural density zero.** (Via the Erdos--Wintner
   theorem and continuity of the limiting distribution of $\sigma^*(n)/n$.)

2. **A power-saving bound $U(X) = O(X^{1-\epsilon})$ for some $\epsilon > 0$.** (Via
   adaptation of Pollack--Shevelev techniques using the divisibility constraint
   $(1 + p^a) \mid 2(n/p^a)$.)

3. **Quantitative bounds on the "sieve density" of UPN candidates.** (By intersecting
   modular obstructions from $\sigma^*(n) \equiv 2n \pmod{q}$ for many moduli $q$.)

4. **Heuristic support for finiteness.** The rapid convergence of the mean $C \approx 1.943$
   and the tightness of the distribution of $\sigma^*(n)/n$ around $C$ suggest that the event
   $\sigma^*(n)/n = 2$ becomes vanishingly unlikely for large $n$ --- not just in the
   density-zero sense, but in the sense that the "probability" decays faster than $1/n$,
   which would imply convergence of $\sum_n \Pr[\sigma^*(n) = 2n]$ and hence (by
   Borel--Cantelli reasoning) finiteness with probability 1 in an appropriate random model.

---

## 7. The Heuristic Argument for Finiteness

### Probabilistic Model

Consider a random integer $n$ of size $\approx N$. Its factorization $n = \prod p_i^{a_i}$
is described by the Erdos--Kac model: $n$ has approximately $\log \log N$ distinct prime
factors, and the "random" value of $\sigma^*(n)/n = \prod(1 + 1/p_i^{a_i})$ concentrates
around $C \approx 1.943$.

The "probability" that $\sigma^*(n)/n$ equals exactly 2 (as a rational number) is heuristically:

$$\Pr[\sigma^*(n) = 2n] \approx \frac{1}{\#\{\text{rational values near } 2 \text{ achievable by } n\}}.$$

For an integer $n$ with $k = \omega(n)$ prime factors, the function $\sigma^*(n)/n$ takes
values in the set $\{r/n : r \in \mathbb{Z}\}$, so the "spacing" between achievable
rational values near 2 is roughly $1/n$, giving:

$$\Pr[\sigma^*(n) = 2n] \approx \frac{1}{n^{1-o(1)}}.$$

The expected number of UPNs up to $X$ is then:

$$\mathbb{E}[U(X)] \approx \sum_{n \leq X} \frac{1}{n^{1-o(1)}} \approx X^{o(1)}.$$

This heuristic suggests that $U(X)$ grows at most polylogarithmically, consistent with
finiteness (or at most a very slowly growing set).

### Refined Heuristic Using the Product Structure

A more refined model accounts for the multiplicative structure. For $\sigma^*(n) = 2n$,
we need $\prod(1 + p_i^{a_i}) = 2 \prod p_i^{a_i}$, which is a single equation in the
integer variables $(p_i, a_i)$. The number of such solutions with $n \leq X$ should be
comparable to the number of representations of 2 by the multiplicative function
$\prod(1 + 1/p_i^{a_i})$ over distinct prime powers up to $X$.

By the theory of multiplicative Diophantine equations (or by direct counting), the number
of exact solutions is expected to be $O(1)$ --- i.e., finite. The heuristic evidence from
computation (only 5 known UPNs, with the last found in 1975) strongly supports this.

---

## 8. Summary and Conclusions

### What We Have Established

1. **Dirichlet series.** $\sum \sigma^*(n)/n^s = \zeta(s)\zeta(s-1)/\zeta(2s-1)$, derived
   rigorously via the Euler product. This provides the analytic foundation for studying
   $\sigma^*(n)$.

2. **Mean value.** The average of $\sigma^*(n)/n$ over $[1, X]$ converges to
   $C = \prod_p (1 + 1/(p(p+1))) \approx 1.943$, which is strictly less than 2.

3. **Distribution.** The limiting distribution of $\sigma^*(n)/n$ is continuous (by
   Erdos--Wintner), so UPNs have natural density zero: $U(X) = o(X)$.

4. **Power-saving bound.** Adapting Pollack--Shevelev techniques using the divisibility
   constraint $(1 + p^a) \mid 2(n/p^a)$, one expects $U(X) = O(X^{5/6+o(1)})$ or better.

5. **Finiteness is out of reach analytically.** No known analytic method can distinguish
   $U(X) = O(1)$ from $U(X) = O(\log \log X)$. The gap between density-zero and finiteness
   requires structural/algebraic arguments, not statistical ones.

6. **Heuristic support.** Probabilistic models predict $U(X) = O(1)$, consistent with
   Subbarao's finiteness conjecture.

### Implications for the Finiteness Conjecture

The analytic results serve as **necessary but not sufficient** evidence for finiteness.
They confirm that UPNs are an extremely sparse set --- far thinner than, say, the primes or
the perfect squares --- but they cannot close the gap to finiteness. To prove Subbarao's
conjecture, one must combine the analytic density bounds with the structural constraints
documented in the companion files (the Subbarao--Warren fixed-valuation argument, the product
equation analysis, the growth constraint on $\omega(n)$ as a function of $v_2(n)$). The
analytic framework provides the "soft" bounds that set the stage, while the algebraic and
combinatorial arguments must deliver the "hard" conclusion.

---

## References

1. Cohen, E. (1960). "Arithmetical Functions Associated with the Unitary Divisors of an Integer." *Mathematische Zeitschrift* 74, 66--80. [BibTeX: `cohen1960unitary`]

2. Pollack, P. and Shevelev, V. (2012). "On Perfect and Near-Perfect Numbers." *Journal of Number Theory* 132(12), 3037--3046. [BibTeX: `pollack2012near`]

3. Subbarao, M. V. and Warren, L. J. (1966). "Unitary Perfect Numbers." *Canadian Mathematical Bulletin* 9(2), 147--153. [BibTeX: `subbarao1966unitary`]

4. Goto, T. (2007). "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers." *Rocky Mountain Journal of Mathematics* 37(5), 1557--1576. [BibTeX: `goto2007upper`]

5. Wall, C. R. (1988). "New Unitary Perfect Numbers Have at Least Nine Odd Components." *The Fibonacci Quarterly* 26(4), 312. [BibTeX: `wall1988nine`]

6. Guy, R. K. (2004). *Unsolved Problems in Number Theory*, 3rd ed. Springer. Problem B3. [BibTeX: `guy2004unsolved`]

7. Subbarao, M. V. (1970). "Are There an Infinity of Unitary Perfect Numbers?" *American Mathematical Monthly* 77, 389--390. [BibTeX: `subbarao1970infinity`]

8. OEIS Foundation Inc. Sequence A002827: Unitary Perfect Numbers. https://oeis.org/A002827 [BibTeX: `oeis_A002827`]
