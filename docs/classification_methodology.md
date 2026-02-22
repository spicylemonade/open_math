# Classification Methodology for Wolfram's Elementary CA Rules

## Overview

We classify all 256 elementary 1D cellular automata rules into Wolfram's four behavioral classes using three quantitative complexity metrics: Shannon entropy, Lempel-Ziv complexity, and Lyapunov exponent estimation.

## Metrics

### 1. Shannon Entropy

Shannon entropy measures the randomness of the cell state distribution at each generation:

    H = -Σ p_i log₂(p_i)

where p_i is the proportion of cells in state i. For binary CAs:
- H = 0: All cells are in the same state (uniform)
- H = 1: Equal numbers of 0s and 1s (maximum disorder)

**Usage**: We compute an entropy trajectory over all generations and use the mean of the final 20 steps as the "final entropy." Class I rules converge to H ≈ 0 (uniform), Class II rules converge to low-to-moderate entropy, and Class III rules maintain high entropy (H > 0.7).

### 2. Lempel-Ziv (LZ76) Complexity

The LZ76 algorithm (Lempel & Ziv, 1976) measures the compressibility of the spacetime diagram by counting the number of distinct substrings encountered during a left-to-right scan of the concatenated row sequence.

We normalize the raw LZ count by n/log₂(n) (the expected value for a random binary sequence).

- LZ ≈ 0: Highly compressible (repetitive or uniform)
- LZ ≈ 1: Incompressible (random)
- 0.2 < LZ < 0.7: Intermediate complexity (potentially Class IV)

### 3. Lyapunov Exponent Estimation

We estimate the Lyapunov exponent by measuring how initial perturbations (single-cell flips) propagate over time:

1. Create the original initial condition and n perturbed copies (each with one random cell flipped).
2. Evolve both for T steps, measuring the Hamming distance at each step.
3. Compute the ratio of late-time to early-time mean Hamming distance.
4. The Lyapunov exponent is log(ratio).

- λ >> 0 (positive): Perturbations grow — chaotic (Class III)
- λ ≈ 0: Perturbations neither grow nor shrink — edge of chaos (Class IV)
- λ << 0 (negative): Perturbations die out — stable (Class I/II)

## Classification Decision Rules

We combine the three metrics using threshold-based heuristics:

| Condition | Predicted Class |
|-----------|----------------|
| Final entropy < 0.05 | Class I (uniform) |
| Final entropy < 0.4, low variance | Class II (periodic) |
| LZ > 0.6 and λ > -1.0 | Class III (chaotic) |
| 0.3 < entropy < 0.85, 0.2 < LZ < 0.7 | Class IV (complex) |
| Entropy ≥ 0.4, very low variance | Class II (stable periodic) |
| Entropy > 0.7 (fallback) | Class III |
| Default | Class II |

## Results

Classification of all 256 rules achieved **91.4% accuracy** against known Wolfram classifications (106/116 known rules correctly classified).

### Parameters Used
- Grid width: 101 cells
- Steps: 100 generations
- Seed: 42
- Perturbations for Lyapunov: 10

### Class Distribution (Predicted)
The distribution across 256 rules follows the expected pattern: a majority of rules exhibit Class I or II behavior (stable/periodic), a significant minority show Class III (chaotic), and very few exhibit Class IV (complex).

## Limitations

1. **Boundary effects**: Classification accuracy depends on grid width and generation count. Very narrow grids or short runs may misclassify rules.
2. **Class IV detection**: Class IV is the hardest to detect algorithmically because it occupies a narrow region between periodic and chaotic behavior.
3. **Threshold sensitivity**: The heuristic thresholds were tuned for the 1D elementary CA family and may not generalize to 2D rules without adjustment.

## References

- Wolfram, S. (2002). *A New Kind of Science*. Wolfram Media.
- Zenil, H. (2010). Compression-based investigation of the dynamical properties of cellular automata. *Complex Systems*, 19(1).
- Langton, C.G. (1990). Computation at the edge of chaos. *Physica D*, 42(1-3).
