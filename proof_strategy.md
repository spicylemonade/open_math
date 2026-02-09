# Proof Strategy: Characterization of r for C-finite Subsequences in ⌊nr⌋

## 1. Conjectured Answer

**Main Theorem (Conjectured).** Let $r > 0$ be a real number. The Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains an infinite subsequence satisfying a homogeneous linear recurrence with constant coefficients if and only if $r$ is rational or a quadratic irrational.

**Note on scope:** Ballot (2017) showed that iterated compositions of complementary Beatty sequences can satisfy linear recurrences even for some cubic algebraic integers (the dominant root of $x^3 - x^2 - 1$). However, the iterated composition $b^y(1)$ is a sequence indexed by the iteration depth $y$, not a subsequence of $\lfloor nr \rfloor$ indexed by positions $n$. The distinction is crucial: $b^y(1)$ is a sequence of *different Beatty sequence values* at recursively defined positions, which does form a subsequence of $\lfloor nr \rfloor$ (since $b^y(1) = \lfloor n_y r' \rfloor$ for some $n_y$). So for cubic Pisot numbers, C-finite subsequences may indeed exist, potentially broadening the characterization.

After careful analysis (see Phase 3 work), we will determine whether:
- **Conjecture A:** The characterization is exactly "rational or quadratic irrational"
- **Conjecture B:** The characterization is "rational or algebraic irrational" (any degree)

## 2. Proof Strategy: The "If" Direction

### 2.1 Rational Case (Elementary)
**Strategy:** Direct computation.
- For $r = p/q$ in lowest terms: $\lfloor (n+q) \cdot p/q \rfloor = \lfloor np/q \rfloor + p$
- So $a(n+q) = a(n) + p$, an inhomogeneous recurrence of order $q$
- Convert to homogeneous: $a(n+q) - a(n+q-1) - a(n) + a(n-1) = 0$ (order $q+1$)
- **Alternatively:** The full sequence is C-finite, so every subsequence along an arithmetic progression is C-finite too.

### 2.2 Quadratic Irrational Case — Wythoff Array Construction
**Strategy:** Use the generalized Wythoff array.
- For quadratic irrational $r > 1$ with $1/r + 1/s = 1$, construct the complementary pair $A(n) = \lfloor nr \rfloor$, $B(n) = \lfloor ns \rfloor$
- Build the Wythoff-type array: Row $m$ starts with $A(m), B(m)$ and extends via the recurrence $w(m,k+2) = c_1 w(m,k+1) + c_0 w(m,k)$ where $c_1, c_0$ come from the minimal polynomial of $r$
- **Key fact (Kimberling 2011, Morrison 1980):** For $r = \varphi = (1+\sqrt{5})/2$, every row of the Wythoff array satisfies the Fibonacci recurrence $F_k = F_{k-1} + F_{k-2}$
- **Generalization:** For $r = (a + \sqrt{d})/b$ with minimal polynomial $x^2 - px + q = 0$ for $r$ and its conjugate $r'$, the analogous array rows satisfy $w(m,k+2) = p \cdot w(m,k+1) - q \cdot w(m,k)$
- Each row is an infinite subsequence of $\lfloor nr \rfloor$ (since all entries are Beatty sequence values at specific indices), and each row satisfies the homogeneous second-order recurrence.

### 2.3 Quadratic Irrational Case — Iterated Composition Construction (Ballot)
**Strategy:** Define $b^0(n) = n$, $b^{y+1}(n) = B(b^y(n))$ where $B(n) = \lfloor ns \rfloor$.
- The sequence $(b^y(n))_{y \geq 0}$ for fixed $n$ satisfies a linear recurrence
- For $r = \varphi$: the recurrence is second-order (Fibonacci)
- The terms $b^y(n)$ are values of the Beatty sequence at recursively defined indices, hence form a subsequence of the positive integers appearing in $\lfloor ms \rfloor$ (and relatedly in $\lfloor mr \rfloor$)

## 3. Proof Strategy: The "Only If" Direction

### 3.1 Growth Rate Argument
**Strategy:** Use the asymptotic form of C-finite sequences.
- A C-finite sequence $a(k)$ satisfying a recurrence of order $d$ has the form $a(k) = \sum_{i=1}^{d} p_i(k) \lambda_i^k$ where $\lambda_i$ are roots of the characteristic polynomial
- If $(a(k))$ is a subsequence of $\lfloor nr \rfloor$, then $a(k) \approx r \cdot n_k$ for some index sequence $n_k$
- The dominant root $\lambda_1$ (spectral radius) determines the exponential growth rate
- For this to be consistent with $\lfloor n_k r \rfloor$ growing as $r \cdot n_k$, we need $n_k \sim C \cdot \lambda_1^k / r$
- **Constraint:** The index sequence $n_k$ must consist of positive integers, which constrains $\lambda_1$ and $r$

### 3.2 Equidistribution Argument
**Strategy:** For non-quadratic irrational $r$, use equidistribution of $\{nr\} = nr - \lfloor nr \rfloor$ modulo 1.
- The fractional parts $\{nr\}$ are equidistributed mod 1 (Weyl's theorem)
- For a C-finite subsequence $a(k) = \lfloor n_k r \rfloor$, the fractional parts $\{n_k r\}$ would need to satisfy strong constraints imposed by the recurrence
- The recurrence $a(k) = c_1 a(k-1) + \cdots + c_d a(k-d)$ translates to a constraint on $n_k r - \{n_k r\} = c_1(n_{k-1}r - \{n_{k-1}r\}) + \cdots$
- This imposes a linear constraint on the fractional parts $\{n_j r\}$, which conflicts with equidistribution for "generic" irrationals

### 3.3 Skolem-Mahler-Lech Approach
**Strategy:** Apply the S-M-L theorem "in reverse."
- If $\lfloor n_k r \rfloor$ is C-finite, consider the sequence $f(n) = \lfloor nr \rfloor$ evaluated at all $n$
- The positions where $f(n)$ matches the C-finite prediction form a set characterized by S-M-L
- For non-quadratic irrationals, the Sturmian structure should prevent the prediction from matching at an arithmetic progression of positions

### 3.4 Non-Automaticity Argument (for the Sturmian characteristic sequence)
**Strategy:** Use the fact that $\lfloor nr \rfloor$ is morphic iff $r$ is quadratic irrational.
- **Key theorem (Allouche-Shallit 2003):** The Sturmian word $s_n = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor$ is morphic iff $r$ is quadratic irrational
- If $s_n$ is not morphic, its complexity grows in a way that prevents C-finite subsequences
- **Argument:** A C-finite sequence has eventually periodic differences of any fixed order. If a subsequence of $\lfloor nr \rfloor$ were C-finite, it would impose periodicity constraints on a subsequence of $s_n$. For non-morphic Sturmian words, the subword complexity (which is $n+1$) prevents such periodic structure from persisting along any infinite index set.

## 4. Key Obstacles and Open Problems

### 4.1 Ballot's Open Problem 36
**Statement:** Characterize pairs of complementary Beatty sequences $(a, b)$ such that the associated iterated sequences satisfy linear recurrences.
**Status:** Open. Our work addresses the case where the recurrence arises from subsequences rather than iterated compositions.
**Relationship:** If Ballot's problem is resolved showing only quadratic irrationals yield C-finite iterated compositions, this would support Conjecture A.

### 4.2 Ballot's Open Problem 37 (Implicit)
The question of whether the characteristic polynomial of the recurrence for iterated compositions always relates to a power of the minimal polynomial of $\alpha$.
**Status:** Verified for degree 2 (quadratic) and partially for degree 3 (cubic Pisot).

### 4.3 Fraenkel's Related Conjectures
- Fraenkel's conjecture on partitions into Beatty sequences (proved for $k \leq 7$)
- Fraenkel's work on iterated floor functions for algebraic numbers of degree $\leq n$

### 4.4 The Cubic Obstruction
The main obstacle to confirming Conjecture A over Conjecture B is Ballot's cubic example. We need to determine:
1. Whether $b^y(1)$ for the cubic Pisot root is genuinely a subsequence of $\lfloor nr \rfloor$ (it is, by construction)
2. Whether the 7th-order recurrence it satisfies is homogeneous (needs verification)
3. Whether similar constructions work for all algebraic irrationals or only special ones

## 5. Proof Roadmap

1. **Phase 3, item_012:** Prove rational case (elementary) ✓ expected straightforward
2. **Phase 3, item_013:** Prove quadratic case via Wythoff + Ballot constructions
3. **Phase 3, item_014:** Attack "only if" direction — this is the hard part
   - First establish growth-rate constraints
   - Then use equidistribution to show fractional parts cannot satisfy recurrence constraints for non-quadratic irrationals
   - Key: carefully analyze what happens at cubic/higher-degree algebraic irrationals
4. **Phase 3, item_015:** Investigate bounded-CF transcendentals as a boundary test
5. **Phase 3, item_016:** Synthesize into unified theorem
