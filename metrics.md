# Metrics for Recurrence Quality and Subsequence Density

## 1. Recurrence Order
**Definition:** The order $k$ of the linear recurrence $a_n = c_1 a_{n-1} + \cdots + c_k a_{n-k}$.
**Interpretation:** Lower order indicates a stronger/simpler recurrence. Order 1 = geometric, order 2 = Fibonacci-type.
**Trivial filter:** Order 1 with coefficient 1 (constant sequence) or coefficient 0 (all-zeros) should be flagged as trivial.

## 2. Verified Length
**Definition:** The number of terms $L$ beyond the initial $k$ values for which the recurrence is verified to hold exactly.
**Interpretation:** Larger $L$ gives more confidence that the recurrence is genuine, not a coincidence. We require $L \geq 10$ as a minimum threshold.

## 3. Subsequence Density
**Definition:** If the subsequence uses indices $n_1 < n_2 < \cdots < n_M$ from the original sequence $\lfloor nr \rfloor$ for $n = 1, \ldots, N$, then the density is $M / N$.
**Interpretation:** Higher density means a larger fraction of the Beatty sequence participates in the recurrence. Density 1 means the full sequence is C-finite.
**Note:** For Wythoff rows and iterated compositions, the density is typically 0 (the subsequence has exponentially growing gaps).

## 4. Spectral Radius
**Definition:** The spectral radius $\rho$ of the companion matrix of the recurrence:
$$C = \begin{pmatrix} c_1 & c_2 & \cdots & c_{k-1} & c_k \\ 1 & 0 & \cdots & 0 & 0 \\ 0 & 1 & \cdots & 0 & 0 \\ \vdots & & \ddots & & \vdots \\ 0 & 0 & \cdots & 1 & 0 \end{pmatrix}$$
The spectral radius is $\rho = \max_i |\lambda_i|$ where $\lambda_i$ are eigenvalues of $C$ (equivalently, roots of the characteristic polynomial).
**Interpretation:** $\rho$ determines the asymptotic growth rate: $a_n \sim \rho^n$. For the golden ratio Beatty sequence, $\rho = \varphi \approx 1.618$.
