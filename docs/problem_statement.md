# Problem Statement: Minimal Cellular Automata Simulator

## 1. Definition of "Minimal"

The term **minimal** in this project means:

- **Fewest abstractions**: The simulator uses plain Python data structures (lists, dicts, numpy arrays) rather than deep class hierarchies or plugin systems. Each concept (grid, rule, simulator) maps to exactly one module.
- **Small codebase**: The core library targets fewer than 2,000 lines of Python across all modules. No external simulation frameworks are used — only standard library, NumPy, and SciPy as computational dependencies.
- **Core CA rules only**: The simulator implements the essential rule families that cover the major CA classes. There is no scripting engine, no GUI toolkit, and no network simulation capability.
- **No over-engineering**: No abstract factory patterns, no dependency injection, no configuration file parsers. Arguments come from the command line or function parameters.

## 2. Cellular Automata Types in Scope

| CA Type | Dimensionality | Rule Parameterization | Example |
|---------|---------------|----------------------|---------|
| Elementary CA | 1D | Wolfram rule number (0–255) | Rule 110, Rule 30 |
| Game of Life | 2D | Fixed B3/S23 | Conway's Life |
| Outer-totalistic CA | 2D | Arbitrary birth/survival sets | HighLife (B36/S23) |

**Out of scope**: continuous-valued CA (Lenia), multi-state CA (> 2 states), non-rectangular lattices, probabilistic CA, asynchronous update schemes.

## 3. Target Interface

- **Primary interface**: Command-line interface (CLI) via `python -m src.cli`
  - Flags: `--rule`, `--width`, `--height`, `--steps`, `--boundary`, `--seed`, `--output`
  - Output: grid state printed to stdout or saved to file
- **Optional visualization**: Terminal-based rendering using curses/Unicode block characters
  - Interactive controls: pause/resume, step-by-step, configurable frame rate
  - Fallback plain-text mode for non-interactive environments
- **Programmatic API**: Direct Python import of `Grid`, `Rule`, and `Simulator` classes for scripting and benchmarking

## 4. Performance Goals

| Metric | Target |
|--------|--------|
| Grid size support | Up to 1,000 × 1,000 cells |
| Naive Python engine | Functional at all sizes (no speed target) |
| NumPy engine | Real-time stepping (≥10 gen/sec) at 1,000 × 1,000 |
| HashLife engine | Exponential speedup on repetitive patterns; 2^20 generations feasible |
| Memory | ≤ 500 MB for 1,000 × 1,000 naive; sub-quadratic for HashLife on repetitive patterns |

## 5. Research Contributions

This project serves as a comparative study of three CA simulation strategies:

1. **Naive cell-by-cell** — baseline for correctness validation
2. **NumPy vectorized** — practical speedup via array operations
3. **HashLife memoized** — algorithmic speedup via space-time compression

The research evaluates these along axes of correctness, performance, memory usage, and applicability to complexity classification of CA rule spaces.
