# Survey of Existing Open-Source Implementations

## 1. esc-paper/erdos-straus (GitHub)

- **URL:** https://github.com/esc-paper/erdos-straus
- **Language:** Python + C++ (with GMP)
- **Authors:** Mihnea & Bogdan (accompanying arXiv:2509.00128)
- **Approach:** Implements Salez's modular sieve in Python (for arbitrary-precision filter generation), then checks residual integers in C++ using GMP for arbitrary-precision arithmetic. Uses the 7 Salez modular equations to pre-filter candidates.
- **Maximum Verified Bound:** $10^{18}$
- **Runtime:** Approximately 2 weeks on a medium setup
- **Notes:** This is the state-of-the-art implementation. The Python/C++ hybrid approach handles the integer overflow issues that arise beyond $10^{17}$. The main bottleneck is GMP arithmetic being slower than native 64-bit operations.

## 2. Suro-One/auro-zera_Erdos-Straus_proof (GitHub)

- **URL:** https://github.com/Suro-One/auro-zera_Erdos-Straus_proof
- **Language:** Python
- **Approach:** A constructive resolution attempt. Implements a brute-force search over candidate values of $x$ and $y$ to find valid decompositions $4/n = 1/x + 1/y + 1/z$. Includes a `verify` function using Python's `Fraction` class for exact arithmetic verification. Handles the special case $n \equiv 0 \pmod{4}$ separately.
- **Maximum Verified Bound:** Small ($< 10^6$ range, limited by Python speed)
- **Notes:** Pure Python, educational implementation. No modular sieve optimization.

## 3. sean-dickinson/Erdos-Straus-Programs (GitHub)

- **URL:** https://github.com/atinybeardedman/Erdos-Straus-Programs (also: https://github.com/sean-dickinson/Erdos-Straus-Programs)
- **Language:** Multiple (JavaScript/TypeScript based)
- **Approach:** Programs to check individual primes for the Erdős–Straus conjecture. Implements a direct search algorithm.
- **Maximum Verified Bound:** Small (educational scope)
- **Notes:** Focus on visualization and educational exploration rather than large-scale computation.

## 4. Another Math Blog Implementation (Blog Post)

- **URL:** https://www.anothermathblog.com/?p=1047
- **Language:** C++
- **Approach:** Optimized implementation using:
  1. `special_cases` function for known congruence class solutions
  2. Continued fraction approach for remaining cases
  3. Brute-force fallback only when all else fails
- **Maximum Verified Bound:** All integers up to 15 million; all primes up to 23,879,519
- **Notes:** Demonstrates the continued-fraction approach as an effective intermediate strategy before brute force. Reports that special cases + continued fractions handle nearly all primes.

## Comparison Table

| Implementation | Language | Sieve | Max Bound | Speed |
|---|---|---|---|---|
| esc-paper/erdos-straus | Python+C++/GMP | Salez 7-eq | $10^{18}$ | ~2 weeks |
| Suro-One | Python | None | $< 10^6$ | Slow |
| sean-dickinson | JS/TS | None | $< 10^5$ | Slow |
| Another Math Blog | C++ | Special cases + CF | $2.4 \times 10^7$ | Minutes |

## Key Takeaways

1. **Salez's sieve is essential** for large-scale verification — without it, brute force cannot go beyond $10^7$ in reasonable time.
2. **GMP is needed beyond $10^{17}$** because the intermediate computations overflow 64-bit integers.
3. **Continued fractions** provide a good intermediate strategy that handles most primes without full brute force.
4. **No implementation has attempted to go beyond $10^{18}$** — this represents the frontier.
