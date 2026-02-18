# Skolem--Mahler--Lech, the Three-Distance Theorem, and Decidability for Quadratic Beatty Sequences

## Item 005 — Phase 1: Problem Analysis & Literature Review

---

## 1. The Skolem--Mahler--Lech Theorem

### 1.1 Statement

**Theorem 1.1 (Skolem--Mahler--Lech).** *Let $(u_n)_{n \geq 0}$ be a sequence of complex numbers satisfying a linear recurrence relation with constant coefficients:*

$$c_0 u_n + c_1 u_{n+1} + \cdots + c_d u_{n+d} = 0 \quad \text{for all } n \geq 0,$$

*where $c_0, c_d \neq 0$. Then the zero set*

$$Z = \{n \in \mathbb{N} : u_n = 0\}$$

*is the union of a finite set and finitely many arithmetic progressions.*

This theorem was proved independently by Skolem \cite{skolem1934einige} (for algebraic number fields, 1934), Mahler \cite{mahler1935arithmetische} (using $p$-adic methods, 1935), and Lech \cite{lech1953note} (simplified proof, 1953).

### 1.2 Proof Outline

The standard proof uses $p$-adic analysis. The key steps are:

1. **Exponential representation.** By the theory of linear recurrences, the general term can be written as
   $$u_n = \sum_{i=1}^{k} P_i(n) \lambda_i^n,$$
   where $\lambda_1, \ldots, \lambda_k$ are the distinct roots of the characteristic polynomial and $P_i$ are polynomials of degree less than the multiplicity of $\lambda_i$.

2. **$p$-adic interpolation.** For a suitable prime $p$, the function $f(x) = \sum_{i=1}^{k} P_i(x) \lambda_i^x$ can be extended to a $p$-adic analytic function on $\mathbb{Z}_p$ (or on cosets of $p^N \mathbb{Z}_p$ for sufficiently large $N$).

3. **Strassmann's theorem.** A non-zero $p$-adic power series converging on $\mathbb{Z}_p$ has finitely many zeros. Applied to $f$ restricted to each coset $a + p^N \mathbb{Z}_p$, this shows that either $f$ vanishes identically on the coset (giving an arithmetic progression of zeros) or has finitely many zeros in the coset.

4. **Finiteness.** Since there are finitely many cosets of $p^N \mathbb{Z}_p$ in $\mathbb{Z}$, the zero set is a finite union of arithmetic progressions plus a finite set.

### 1.3 Relevance to Beatty Sequences

The Skolem--Mahler--Lech theorem constrains the structure of zero sets (and, by translation, level sets) of linearly recurrent sequences. Its relevance to our project is:

**Application 1: Structure of level sets.** If a subsequence of $\lfloor nr \rfloor$ satisfies a linear recurrence, say $S = (\lfloor n_k r \rfloor)_{k \geq 0}$ with $\sum_{i=0}^{d} c_i S_{k+i} = 0$, then for any integer value $v$, the set $\{k : S_k = v\}$ is a finite union of arithmetic progressions plus a finite set. Since $\lfloor nr \rfloor$ grows to infinity, each value $v$ is achieved only finitely many times, so the level sets are automatically finite. The SML constraint is thus automatically satisfied in a trivial way for growing sequences.

**Application 2: Difference sequences.** More usefully, consider the sequence $u_n = S_n - An - B$ for appropriate constants $A, B$. If $S$ satisfies a linear recurrence and $An + B$ also satisfies one (which it does: $a_{n+2} - 2a_{n+1} + a_n = 0$), then $u_n$ satisfies a linear recurrence. The set $\{n : u_n = c\}$ for each integer $c$ is then structured by SML. For Beatty sequences, $u_n = \lfloor n_k r \rfloor - An_k - B$ captures the "fractional part" behavior, and SML constrains how often specific deviations from linearity can occur.

**Application 3: Obstruction to recurrence.** Conversely, SML can be used as an obstruction: if we can show that a candidate subsequence of $\lfloor nr \rfloor$ has a level set (or difference set) that is NOT a finite union of arithmetic progressions plus a finite set, then that subsequence CANNOT satisfy a linear recurrence.

### 1.4 Citations

- \cite{skolem1934einige} Skolem, T. (1934). Original proof using $p$-adic methods for algebraic fields.
- \cite{mahler1935arithmetische} Mahler, K. (1935). Extended to power series in several variables.
- \cite{lech1953note} Lech, C. (1953). Simplified proof and clean formulation.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). Chapter 1 discusses linear recurrence sequences and their zero sets; the SML theorem is presented in the context of automatic sequences.

---

## 2. The Three-Distance Theorem

### 2.1 Statement

**Theorem 2.1 (Three-Distance Theorem / Steinhaus Conjecture).** *Let $\alpha$ be an irrational number and $N$ a positive integer. Consider the $N$ points*

$$\{\alpha\}, \{2\alpha\}, \{3\alpha\}, \ldots, \{N\alpha\}$$

*on the circle $\mathbb{R}/\mathbb{Z}$ (equivalently, in the interval $[0,1)$). These $N$ points partition the circle into $N$ arcs. The lengths of these arcs take at most 3 distinct values. Moreover, if there are exactly 3 distinct lengths, then one of them equals the sum of the other two.*

This result was conjectured by Steinhaus and proved independently by Sos \cite{sos1958distribution}, Swierczkowski (1958), and Suranyi (1958). See van Ravenstein \cite{ravenstein1988three} for a comprehensive treatment.

### 2.2 Connection to Continued Fractions

The three distances are determined by the continued fraction expansion of $\alpha$. If $\alpha = [0; a_1, a_2, \ldots]$ with convergents $p_k/q_k$, then for $N$ in the range $q_k \leq N < q_{k+1}$, the three gap lengths are:

$$d_1 = \frac{1}{q_k} - \frac{p_k}{q_k}\alpha + \alpha \cdot q_{k-1}/q_k, \quad d_2 = \ldots$$

More concretely, writing $N = mq_k + q_{k-1} + s$ for appropriate $m$ and $s$, the three gap lengths involve $q_k\alpha - p_k$, $p_{k-1} - q_{k-1}\alpha$, and their sum. The largest gap is bounded by $1/q_k$, which decreases as $N$ grows through the denominators of convergents.

### 2.3 Connection to Beatty Sequences and Gap Structure

The three-distance theorem directly constrains the gap structure of Beatty sequences. Consider the first differences:

$$\Delta_r(n) = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor = \lfloor \{nr\} + r \rfloor.$$

As shown in Item 004, $\Delta_r(n) \in \{\lfloor r \rfloor, \lceil r \rceil\}$, taking exactly **two** distinct values (for irrational $r$ that is not an integer). This is consistent with the three-distance theorem: the first difference of $\lfloor nr \rfloor$ depends on which arc of the circle partition $\{nr\}$ falls in, and the two-value property reflects the binary partition $[0, 1-\{r\}) \cup [1-\{r\}, 1)$.

**Higher-order differences and three values.** The connection to three distances becomes more visible when examining second-order or structured gap patterns:

1. **Gaps between occurrences of a specific first difference.** Consider the positions where $\Delta_r(n) = \lceil r \rceil$. The gaps between consecutive such positions take at most 3 distinct values. This follows directly from the three-distance theorem applied to the rotation by $\{r\}$ and the interval $[1-\{r\}, 1)$.

2. **Three-distance and Sturmian balance.** A Sturmian word is *balanced*: for any two factors $u, v$ of the same length, the number of occurrences of each letter in $u$ and $v$ differs by at most 1. The three-distance theorem is the geometric reason behind this balance property.

3. **Constraints on recurrence.** For the central question of this project, the three-distance theorem implies that the "error" term $\lfloor nr \rfloor - nr$ (which equals $-\{nr\}$) has a gap structure with at most 3 distinct spacings at any scale. This regularity constrains but does not determine whether algebraic linear recurrences can hold.

### 2.4 Citations

- \cite{sos1958distribution} Sos, V.T. (1958). First published proof, using the geometry of irrational rotations.
- \cite{ravenstein1988three} van Ravenstein, T. (1988). Comprehensive proof with connections to continued fractions.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). Discussion in the context of Sturmian words (Chapter 2).
- \cite{fraenkel1969bracket} Fraenkel, A.S. (1969). Early work on bracket functions connecting floor sequences to the circle partition.
- \cite{morse1940symbolic2} Morse, M. and Hedlund, G.A. (1940). Sturmian trajectories, which encode the circle partition.
- \cite{cassaigne1999limit} Cassaigne, J. (1999). Uses three-distance ideas in computing Sturmian recurrence quotients.

---

## 3. Schaeffer--Shallit--Zorcic: Decidability for Quadratic Beatty Sequences

### 3.1 Background: Ostrowski Numeration

For a quadratic irrational $\alpha$ with continued fraction $\alpha = [a_0; a_1, a_2, \ldots]$ (eventually periodic by Lagrange's theorem \cite{lagrange1770continued}), the *Ostrowski numeration system* (based on $\alpha$) represents non-negative integers using the denominators $q_0, q_1, q_2, \ldots$ of the convergents to $\alpha$ as a non-standard positional system \cite{ostrowski1922bemerkungen}.

Specifically, every non-negative integer $n$ has a unique representation:

$$n = \sum_{i=0}^{L} d_i q_i,$$

where the digits $d_i$ satisfy $0 \leq d_i \leq a_{i+1}$, with the additional constraint that if $d_i = a_{i+1}$ then $d_{i-1} = 0$ (the "greedy" or "canonical" representation). This is the *Ostrowski-$\alpha$ representation* of $n$.

The key property is that for quadratic irrationals, the continued fraction is eventually periodic, so the Ostrowski representation has a periodic digit constraint structure, which makes it amenable to finite automaton processing.

### 3.2 Main Results of Schaeffer--Shallit--Zorcic (2024)

**Theorem 3.1 (Schaeffer--Shallit--Zorcic \cite{schaeffer2024beatty}).** *Let $\alpha$ be a quadratic irrational and $\beta$ a real number such that $\beta \in \mathbb{Q}(\alpha)$ (i.e., $\beta = a + b\alpha$ for rationals $a, b$). Then the Beatty sequence*

$$B_{\alpha,\beta}(n) = \lfloor n\alpha + \beta \rfloor$$

*is "synchronized" in Ostrowski-$\alpha$ representation: there exists a finite automaton that, given the Ostrowski-$\alpha$ representations of $n$ and $y$ in parallel (reading digits from least significant to most significant), accepts if and only if $y = \lfloor n\alpha + \beta \rfloor$.*

**Corollary 3.2 (Decidability).** *The first-order theory of the structure $(\mathbb{N}, +, B_{\alpha,\beta})$ is decidable. That is, any first-order sentence involving:*
- *natural number variables,*
- *addition of natural numbers,*
- *the predicate $y = \lfloor n\alpha + \beta \rfloor$,*

*can be algorithmically decided (true or false).*

### 3.3 Consequences for the Central Question

The decidability result has profound implications for our research:

**Consequence 1: Existence of recurrent subsequences is decidable (for quadratic $\alpha$).**

The statement "there exists an arithmetic progression $a, a+d, a+2d, \ldots$ such that the subsequence $\lfloor (a+kd)\alpha \rfloor$ satisfies a homogeneous linear recurrence of order $\leq D$" can be expressed as a first-order sentence over $(\mathbb{N}, +, B_{\alpha,0})$ (with the order $D$ and the number of coefficients fixed as parameters). By Theorem 3.1, this sentence is decidable.

More precisely, fix an order $d$ and coefficients $c_0, \ldots, c_d$. The statement

$$\exists a \exists s \; \forall k : \sum_{i=0}^{d} c_i \cdot \lfloor (a + (k+i) \cdot s) \cdot \alpha \rfloor = 0$$

is a first-order sentence in the structure $(\mathbb{N}, +, B_\alpha)$ (where multiplication by a fixed integer is expressible via repeated addition). Since we can quantify over finitely many choices of coefficient vectors $(c_0, \ldots, c_d)$... but we actually need to quantify over ALL coefficient vectors, which requires bounding the search.

**Important caveat:** The decidability is for FIXED first-order sentences. The quantification "there exist coefficients $c_0, \ldots, c_d$" involves quantifying over $d+1$ integer variables, which IS expressible in the first-order theory (since integers can be represented as differences of naturals, and the coefficient bound can be imposed). So the full statement

$$\exists c_0 \cdots \exists c_d \exists a \exists s \; \forall k : \sum_{i=0}^{d} c_i \cdot \lfloor (a + (k+i) \cdot s) \cdot \alpha \rfloor = 0$$

is a first-order sentence (for each fixed $d$) and hence decidable.

**Consequence 2: Potential for automated proof.**

In principle, one could use the Schaeffer--Shallit--Zorcic automaton construction to automatically verify (or refute) the existence of linearly recurrent subsequences for specific quadratic irrationals like $\varphi$, $\sqrt{2}$, etc. The automaton construction is effective (implementable), though potentially computationally expensive.

**Consequence 3: The quadratic case may be fully resolvable.**

While the decidability result guarantees that the answer exists (for each fixed $\alpha$ and $d$), it does not immediately tell us what the answer is. However, combined with the theoretical analysis from Items 004 and 006, we expect the answer to be: for irrational $\alpha$ (including quadratic irrationals), NO non-trivial homogeneous linearly recurrent subsequence exists along arithmetic progressions. The decidability framework provides a potential path to rigorous verification.

### 3.4 Related Work

The Schaeffer--Shallit--Zorcic results build on a substantial body of work:

- **Hieronymi--Terry \cite{hieronymi2018ostrowski}:** Established that addition is computable by finite automata in Ostrowski numeration systems, laying the foundation for decidability results.

- **Baranwal--Schaeffer--Shallit \cite{baranwal2021decidability}:** Proved decidability results for properties of Sturmian words using automata over Ostrowski numeration, showing that questions about factor complexity, palindromes, and other combinatorial properties can be decided.

- **Allouche--Shallit \cite{allouche2003automatic}:** The foundational text on automatic sequences, providing the theoretical framework for connecting numeration systems, finite automata, and sequence properties.

### 3.5 Citations

- \cite{schaeffer2024beatty} Schaeffer, L., Shallit, J., and Zorcic, S. (2024). Beatty Sequences for a Quadratic Irrational: Decidability and Applications.
- \cite{hieronymi2018ostrowski} Hieronymi, P. and Terry, A. (2018). Ostrowski Numeration Systems, Addition, and Finite Automata.
- \cite{baranwal2021decidability} Baranwal, A.R., Schaeffer, L., and Shallit, J. (2021). Decidability for Sturmian words.
- \cite{ostrowski1922bemerkungen} Ostrowski, A. (1922). Original development of the Ostrowski numeration system.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). Automatic Sequences (textbook).
- \cite{lagrange1770continued} Lagrange, J.-L. (1770). Periodicity of continued fractions for quadratic irrationals.

---

## 4. Synthesis: How These Three Topics Interact

### 4.1 The Logical Chain

The three topics in this document form an interconnected chain of tools for analyzing linear recurrence in Beatty sequences:

1. **Three-Distance Theorem** (Section 2): Establishes the geometric regularity of $\{n\alpha\}$ on the circle, which underlies the Sturmian structure of $\Delta_r$. This gives us the "two-value" property of first differences and constrains the gap structure.

2. **Skolem--Mahler--Lech** (Section 1): Provides structural constraints on zero/level sets of linearly recurrent sequences. If a subsequence of $\lfloor nr \rfloor$ were linearly recurrent, SML constrains which values it can take and how often. Combined with the three-distance regularity, this limits the possible recurrence structures.

3. **Schaeffer--Shallit--Zorcic** (Section 3): For quadratic irrationals, provides a decision procedure. Rather than proving by hand that no linearly recurrent subsequence exists, one can (in principle) construct the relevant automaton and check algorithmically.

### 4.2 The Overall Picture

```
Three-Distance Theorem          Durand's Theorem (Item 004)
        |                                |
        v                                v
  Gap structure of              Sturmian linear recurrence
  {nα} on circle                (symbolic, NOT algebraic)
        |                                |
        +----------+----------+----------+
                   |
                   v
        Structure of ⌊nα⌋
        (integer values, growth ~ nα)
                   |
          +--------+--------+
          |                 |
          v                 v
   Skolem-Mahler-Lech    Schaeffer-Shallit-Zorcic
   (obstructions to      (decidability for
    algebraic recurrence) quadratic irrationals)
          |                 |
          +--------+--------+
                   |
                   v
        Central Question: Does ⌊nα⌋ contain a
        homogeneous linearly recurrent subsequence?
```

### 4.3 Forward References

- **Item 006** uses the tools developed here to rigorously analyze the independence of symbolic and algebraic linear recurrence.
- **Item 012** (Phase 3) will apply the Schaeffer--Shallit--Zorcic framework specifically to the golden ratio and other quadratic irrationals.
- **Item 013** (Phase 3) will examine what happens beyond the quadratic case, where the decidability tools of Section 3 are not available, and where the three-distance constraints must be supplemented by Diophantine approximation arguments.
- **Item 014** (Phase 3) will synthesize all of these into the main characterization theorem.

---

## 5. Technical Appendix: Key Definitions for Cross-Reference

For convenience, we collect the key definitions used across Items 004, 005, and 006:

**Definition A.1 (Beatty sequence).** $b_r(n) = \lfloor nr \rfloor$ for $n \geq 1$, $r > 0$.

**Definition A.2 (First-difference / Sturmian word).** $\Delta_r(n) = b_r(n+1) - b_r(n) \in \{\lfloor r \rfloor, \lceil r \rceil\}$.

**Definition A.3 (Subword complexity).** $p_{\mathbf{s}}(n) = |\{w : |w| = n, w \text{ is a factor of } \mathbf{s}\}|$.

**Definition A.4 (Sturmian).** $\mathbf{s}$ is Sturmian iff $p_{\mathbf{s}}(n) = n+1$ for all $n \geq 1$.

**Definition A.5 (Recurrence function).** $R_{\mathbf{s}}(n) = \min\{R : \text{every factor of length } R \text{ contains every factor of length } n\}$.

**Definition A.6 (Linearly recurrent word).** $\exists C > 0$ such that $R_{\mathbf{s}}(n) \leq Cn$ for all $n$.

**Definition A.7 (Homogeneous linear recurrence).** $(a_n)$ satisfies $\sum_{i=0}^{d} c_i a_{n+i} = 0$ for all $n$, with $c_0 c_d \neq 0$.

**Definition A.8 (Ostrowski representation).** $n = \sum d_i q_i$ with digit constraints from the CF of $\alpha$.

**Definition A.9 (Synchronized sequence).** A sequence $f(n)$ is synchronized (in base $\alpha$) if the relation $\{(n, f(n))\}$ is recognizable by a finite automaton reading Ostrowski-$\alpha$ representations in parallel.

---

## References

- \cite{skolem1934einige} Skolem, T. (1934). Ein Verfahren zur Behandlung gewisser exponentialer Gleichungen. *Comptes rendus du 8e Congres des Math. Scandinaves*, 163--188.
- \cite{mahler1935arithmetische} Mahler, K. (1935). Uber das Verschwinden von Potenzreihen mehrerer Veranderlichen. *Math. Ann.* 103, 573--587.
- \cite{lech1953note} Lech, C. (1953). A note on recurring series. *Arkiv for Matematik* 2(5), 417--421.
- \cite{sos1958distribution} Sos, V.T. (1958). On the distribution mod 1 of the sequence $n\alpha$. *Ann. Univ. Sci. Budapest.* 1, 127--134.
- \cite{ravenstein1988three} van Ravenstein, T. (1988). The Three Gap Theorem (Steinhaus Conjecture). *J. Austral. Math. Soc. (Series A)* 45(3), 360--370.
- \cite{ostrowski1922bemerkungen} Ostrowski, A. (1922). Bemerkungen zur Theorie der Diophantischen Approximationen. *Abh. Math. Sem. Univ. Hamburg* 1(1), 77--98.
- \cite{schaeffer2024beatty} Schaeffer, L., Shallit, J., and Zorcic, S. (2024). Beatty Sequences for a Quadratic Irrational: Decidability and Applications. arXiv:2402.08331.
- \cite{hieronymi2018ostrowski} Hieronymi, P. and Terry, A. (2018). Ostrowski Numeration Systems, Addition, and Finite Automata. *Notre Dame J. Formal Logic* 59(2), 215--232.
- \cite{baranwal2021decidability} Baranwal, A.R., Schaeffer, L., and Shallit, J. (2021). Decidability for Sturmian words. arXiv:2102.08207.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences.* Cambridge University Press.
- \cite{lagrange1770continued} Lagrange, J.-L. (1770). Additions au memoire sur la resolution des equations numeriques.
- \cite{morse1940symbolic2} Morse, M. and Hedlund, G.A. (1940). Symbolic dynamics II: Sturmian trajectories. *Amer. J. Math.* 62(1), 1--42.
- \cite{fraenkel1969bracket} Fraenkel, A.S. (1969). The bracket function and complementary sets of integers. *Canad. J. Math.* 21, 6--27.
- \cite{cassaigne1999limit} Cassaigne, J. (1999). Limit values of the recurrence quotient of Sturmian sequences. *Theoret. Comput. Sci.* 218(1), 3--12.
