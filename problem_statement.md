# Problem Statement: Characterizing r for Which floor(n·r) Contains a Homogeneous Linearly Recurrent Subsequence

## 1. The Beatty Sequence

**Definition 1 (Beatty Sequence).** For a real number $r > 0$, the *Beatty sequence* of $r$ is the integer sequence
$$B_r(n) = \lfloor n \cdot r \rfloor, \quad n = 1, 2, 3, \ldots$$
where $\lfloor x \rfloor$ denotes the floor function (greatest integer $\leq x$).

**Convention.** We index the sequence starting at $n = 1$. The sequence is monotonically non-decreasing; for $r \geq 1$ it is strictly increasing.

**Examples.**
- $r = 3/2$: $B_r = (1, 3, 4, 6, 7, 9, 10, 12, \ldots)$
- $r = \varphi = (1+\sqrt{5})/2$: $B_r = (1, 3, 4, 6, 8, 9, 11, 12, 14, \ldots)$ (OEIS A000201)
- $r = \pi$: $B_r = (3, 6, 9, 12, 15, 18, 21, 25, 28, \ldots)$

## 2. Homogeneous Linear Recurrence (C-finite Sequence)

**Definition 2 (C-finite Sequence).** An integer sequence $(a_n)_{n \geq 0}$ is *C-finite* (or *constant-recursive*, or satisfies a *homogeneous linear recurrence with constant coefficients*) if there exist an integer $k \geq 1$ and constants $c_1, c_2, \ldots, c_k \in \mathbb{Q}$ with $c_k \neq 0$ such that for all $n \geq k$:
$$a_n = c_1 \, a_{n-1} + c_2 \, a_{n-2} + \cdots + c_k \, a_{n-k}.$$

The integer $k$ is the *order* of the recurrence. The polynomial $x^k - c_1 x^{k-1} - \cdots - c_k$ is the *characteristic polynomial*.

**Key property.** A C-finite sequence is uniquely determined by its recurrence coefficients and initial values $a_0, a_1, \ldots, a_{k-1}$. Its general term has the form $a_n = \sum_{i} p_i(n) \lambda_i^n$ where $\lambda_i$ are the roots of the characteristic polynomial and $p_i$ are polynomials.

**Homogeneity distinction.** The recurrence $a_n = c_1 a_{n-1} + \cdots + c_k a_{n-k}$ is *homogeneous*. An *inhomogeneous* recurrence would add a non-zero constant: $a_n = c_1 a_{n-1} + \cdots + c_k a_{n-k} + d$. Any inhomogeneous recurrence of order $k$ can be converted to a homogeneous recurrence of order $k+1$ (by differencing), but the distinction matters: the question specifically asks about *homogeneous* recurrences.

**Examples.** Fibonacci: $F_n = F_{n-1} + F_{n-2}$ (order 2). Geometric: $a_n = c \cdot a_{n-1}$ (order 1). Tribonacci: $T_n = T_{n-1} + T_{n-2} + T_{n-3}$ (order 3).

## 3. The Precise Question

### 3.1 Full Sequence vs. Subsequence

There are two distinct questions:

**(Q1) Full sequence.** For which $r$ is the Beatty sequence $B_r = (\lfloor nr \rfloor)_{n \geq 1}$ itself a C-finite sequence?

**Answer to Q1:** $B_r$ is C-finite if and only if $r$ is rational. (When $r = p/q$ in lowest terms, $B_r$ satisfies $a_{n+q} = a_n + p$.)

**(Q2) Subsequence.** For which $r$ does the Beatty sequence $B_r$ *contain* an infinite subsequence that is C-finite? This is the question we study.

### 3.2 Definition of "Subsequence"

**Definition 3 (Subsequence by Index Selection).** Given a sequence $(a_n)_{n \geq 1}$ and a strictly increasing sequence of positive integers $n_1 < n_2 < n_3 < \cdots$, the *subsequence* is $(a_{n_k})_{k \geq 1}$.

We say the Beatty sequence $B_r$ *contains an infinite homogeneous C-finite subsequence* if there exists:
1. A strictly increasing sequence of positive integers $n_1 < n_2 < n_3 < \cdots$ (the *index sequence*), and
2. Constants $c_1, \ldots, c_m \in \mathbb{Q}$ with $c_m \neq 0$, such that

$$\lfloor n_{k} \cdot r \rfloor = c_1 \lfloor n_{k-1} \cdot r \rfloor + c_2 \lfloor n_{k-2} \cdot r \rfloor + \cdots + c_m \lfloor n_{k-m} \cdot r \rfloor \quad \text{for all } k > m.$$

**Important clarifications:**
- The index sequence $(n_k)$ need *not* be an arithmetic progression; it can be any strictly increasing sequence of natural numbers.
- "Contiguous block" (a finite initial segment) does not suffice: we require an *infinite* subsequence.
- The recurrence must hold for *all* sufficiently large $k$, not just finitely many.
- The recurrence coefficients $c_i$ are *constants* (independent of $k$).

### 3.3 Formal Problem Statement

**Problem.** Characterize the real numbers $r > 0$ for which there exists a strictly increasing sequence of positive integers $(n_k)_{k \geq 1}$ such that the sequence $(\lfloor n_k \cdot r \rfloor)_{k \geq 1}$ satisfies a homogeneous linear recurrence with constant coefficients.

### 3.4 Conjectured Answer

**Conjecture (Main).** The Beatty sequence $\lfloor nr \rfloor$ contains an infinite homogeneous C-finite subsequence if and only if $r$ is rational or a quadratic irrational.

This conjecture is motivated by:
- For rational $r$: the full sequence is C-finite (trivial).
- For quadratic irrational $r$: explicit constructions via Wythoff arrays and iterated Beatty compositions yield C-finite subsequences (Ballot 2017, Kimberling 2011).
- For non-quadratic irrationals: computational experiments and structural arguments (non-morphicity, equidistribution) suggest no infinite C-finite subsequence exists.

## 4. Scope and Conventions

- All sequences are over the integers $\mathbb{Z}$.
- "Linear recurrence" always means "linear recurrence with constant coefficients over $\mathbb{Q}$."
- "Homogeneous" means no additive constant term.
- We consider $r > 0$ only (for $r < 0$, one studies $\lceil n|r| \rceil$ instead, which is equivalent up to sign).
- A "quadratic irrational" is a number of the form $(a + b\sqrt{d})/c$ where $a, b, c \in \mathbb{Z}$, $c \neq 0$, $b \neq 0$, $d \geq 2$ is square-free.
