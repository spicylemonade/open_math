# Comparison Table: Our Simulator vs Prior Implementations

## Overview

This document compares our minimal CA simulator against five existing open-source implementations surveyed in the literature review (item_004). The comparison covers features, languages, codebase size, performance, and unique characteristics.

## Detailed Comparison

| Feature | **Our Simulator** | **Golly** [golly2005] | **Lenia** [chan2019lenia] | **CellPyLib** [cellpylib2020] | **python-lifelib** | **jakevdp GoL** [jakevdp2013gol] |
|---------|-------------------|----------------------|--------------------------|-------------------------------|--------------------|---------------------------------|
| **Language** | Python | C++ / Python / Lua | Python / MATLAB / JS | Python | C++ / Python / x86 ASM | Python |
| **Lines of Code** | ~1,800 (core) | ~100,000 | ~5,000 | ~2,000 | ~50,000 | ~20 |
| **CA Dimensions** | 1D, 2D | 1D, 2D | N-D | 1D, 2D | 2D | 2D |
| **CA States** | 2 | Up to 256 | Continuous | Discrete / Continuous | 2 | 2 |
| **Rule Families** | Elementary, Life, Outer-totalistic | All standard families + custom | Continuous growth functions | Elementary, totalistic, custom | Life-like (B/S notation) | Life only |
| **Algorithms** | Naive, NumPy, HashLife | HashLife, QuickLife | FFT convolution | NumPy array ops | StreamLife, tile-based (SIMD) | convolve2d |
| **Boundary Conditions** | Wrap, Fixed | Wrap, Plane, Klein bottle, Cross-surface | Wrap | Wrap | Infinite plane | Wrap |
| **Pattern I/O** | RLE, Plaintext | RLE, Macrocell, Life 1.05/1.06, dblife, MCell | Custom | None standard | RLE, Macrocell | None |
| **Visualization** | Terminal (curses/Unicode) | Full GUI (wxWidgets) | Jupyter / Matplotlib | Matplotlib | None (library) | Matplotlib animation |
| **CLI Support** | Yes (argparse) | Yes (bgolly) | No | No | No | No |
| **Complexity Metrics** | Entropy, LZ, Lyapunov | None built-in | None built-in | Lambda parameter | apgcode periodicity | None |
| **Classification** | Wolfram 4-class (91.4%) | None | None | None | Object classification | None |
| **Unit Tests** | 60 tests | Yes (extensive) | Minimal | Yes | Yes | None |
| **Reproducibility** | Makefile, requirements.txt, seed=42 | CMake build | Notebooks | pip install | pip install | Blog post |

## Performance Comparison

| Benchmark | **Our Simulator** | **Golly** [golly2005] | **CellPyLib** [cellpylib2020] | **python-lifelib** | **jakevdp GoL** [jakevdp2013gol] |
|-----------|-------------------|----------------------|-------------------------------|--------------------|---------------------------------|
| **Life 100x100, 100 gen** | | | | | |
| &nbsp;&nbsp;Naive engine | 2.61s | N/A | ~1-2s (est.) | N/A | N/A |
| &nbsp;&nbsp;NumPy engine | 0.028s | N/A | ~0.05s (est.) | N/A | ~0.03s (est.) |
| **Life 500x500, 100 gen** | | | | | |
| &nbsp;&nbsp;Naive engine | 68.5s | N/A | ~60s (est.) | N/A | N/A |
| &nbsp;&nbsp;NumPy engine | 0.68s | N/A | ~0.8s (est.) | N/A | ~0.7s (est.) |
| **Life 1000x1000, 100 gen** | | | | | |
| &nbsp;&nbsp;NumPy engine | 3.15s | ~0.1s (QuickLife) | ~3s (est.) | ~0.01s (SIMD) | ~3s (est.) |
| **Glider gun 131K gen** | | | | | |
| &nbsp;&nbsp;HashLife engine | 0.035s | ~0.001s (C++ HashLife) | N/A | N/A | N/A |
| **Memory (1000x1000)** | 17 MB (NumPy) | ~4 MB (QuickLife) | ~16 MB (est.) | ~4 MB (SIMD) | ~16 MB (est.) |
| **Cells/sec (1000x1000)** | 32M (NumPy) | ~500M (QuickLife) | ~30M (est.) | ~5,000M (SIMD) | ~30M (est.) |

*Note: "est." values are estimated from published descriptions and similar hardware. Actual performance varies by hardware and configuration.*

## Unique Strengths and Weaknesses

### Our Simulator

**Strengths:**
- Three algorithms in one codebase behind a shared interface, enabling direct comparison
- Built-in complexity classification (Shannon entropy, LZ, Lyapunov) — unique among surveyed tools
- Automated Wolfram classification with 91.4% accuracy
- Comprehensive test suite (60 tests) with cross-engine validation
- Full reproducibility package (Makefile, pinned requirements, deterministic seeds)
- Minimal codebase (~1,800 lines) — easy to understand, modify, and extend

**Weaknesses:**
- Limited to 2-state CA (no multi-state support)
- HashLife hardcoded for B3/S23 only
- Pure Python — absolute performance lags behind C++/SIMD implementations
- No GUI, only terminal visualization
- No infinite-plane support (fixed-size grids only)

### Golly [golly2005]

**Strengths:**
- Most comprehensive CA simulator available
- Dual algorithm engine (HashLife + QuickLife) with seamless switching
- Full GUI with unlimited undo/redo, layers, scripting
- Supports unbounded universes and exotic topologies
- Extensive pattern library and community

**Weaknesses:**
- Very large codebase (~100k lines) — difficult to modify or extend
- No built-in complexity analysis or classification tools
- Requires compilation from C++ source

### Lenia [chan2019lenia]

**Strengths:**
- Pioneered continuous-state CA with beautiful emergent creatures
- N-dimensional support
- FFT convolution for efficient large-kernel computation

**Weaknesses:**
- Not applicable to discrete CA (Life, elementary rules)
- No standard pattern I/O formats
- Limited CLI/automation support

### CellPyLib [cellpylib2020]

**Strengths:**
- Clean functional API similar to ours
- Lambda parameter calculation (Langton's edge-of-chaos metric)
- Supports reversible and asynchronous CA
- Good balance of features and simplicity (~2,000 lines)

**Weaknesses:**
- No HashLife or advanced algorithm support
- No standard pattern I/O
- Limited visualization options

### python-lifelib

**Strengths:**
- Extreme performance via SIMD instructions (AVX2/AVX-512)
- Specialized algorithms for different pattern types (StreamLife, tile-based)
- Professional apgsearch integration for pattern census

**Weaknesses:**
- Very large codebase (~50k lines) with code generation
- Requires x86_64 hardware for SIMD acceleration
- Limited to 2-state Life-like rules
- Complex build process

## Summary

Our simulator occupies a unique niche: it is the only implementation among those surveyed that combines multiple simulation algorithms with built-in complexity classification in a minimal, research-oriented package. While it cannot match the absolute performance of C++/SIMD implementations like Golly or python-lifelib, its NumPy engine achieves competitive throughput (~32M cells/sec) for a pure Python implementation, and its HashLife engine correctly demonstrates the algorithm's asymptotic advantages. The built-in classification pipeline — applying Shannon entropy, LZ complexity, and Lyapunov exponent to automatically categorize CA rules — is a distinguishing feature not found in any of the other five projects surveyed.
