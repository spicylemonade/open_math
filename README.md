# Minimal Cellular Automata Simulator

A research-oriented cellular automata (CA) simulator implementing three simulation engines — naive cell-by-cell, NumPy-vectorized, and HashLife memoized — for both 1D elementary and 2D outer-totalistic rules.

## Overview

This project is a comparative study of cellular automata simulation strategies. It implements the core CA algorithms in fewer than 2,000 lines of Python, providing a clean testbed for evaluating performance, memory efficiency, and applicability to complexity classification.

### Key Results

- **NumPy engine**: 88-100x speedup over naive Python on Game of Life grids up to 1000x1000
- **HashLife engine**: Simulates 131,072 generations of a Gosper glider gun in 0.035 seconds with sub-linear memory growth
- **Classification accuracy**: 91.4% on Wolfram's 256 elementary 1D CA rules using Shannon entropy, Lempel-Ziv complexity, and Lyapunov exponent metrics
- **2D rule exploration**: 56 outer-totalistic rules classified, 3 Class IV rules identified

## Installation

Requires Python 3.8+.

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
pip install -r requirements.txt

# Or using make
make install
```

### Dependencies

| Package    | Version | Purpose                        |
|------------|---------|--------------------------------|
| numpy      | 2.2.6   | Array operations, vectorized computation |
| scipy      | 1.15.3  | 2D convolution for neighbor counting |
| matplotlib | 3.10.8  | Figure generation              |
| seaborn    | 0.13.2  | Publication-quality plot styling |
| pytest     | 9.0.2   | Unit testing                   |

## Usage

### Command-Line Interface

```bash
# Run Game of Life on a 50x50 grid for 100 steps
python -m src.cli --rule life --width 50 --height 50 --steps 100

# Run Wolfram Rule 110 on a 1D grid
python -m src.cli --rule 110 --width 100 --steps 50

# Use fixed boundary instead of toroidal wrap
python -m src.cli --rule life --width 100 --height 100 --steps 200 --boundary fixed

# Set random seed for reproducibility
python -m src.cli --rule life --width 50 --height 50 --steps 100 --seed 42
```

### Programmatic API

```python
from src.grid_numpy import NumPyGrid, NumPyLifeRule
from src.simulator import Simulator

# Create a 100x100 grid with toroidal boundary
grid = NumPyGrid(100, 100, "wrap")
grid.set(50, 50, 1)  # Set a cell alive
grid.set(51, 50, 1)
grid.set(50, 51, 1)

# Run simulation
rule = NumPyLifeRule()
sim = Simulator(grid, rule)
sim.run(100)
print(f"Population after 100 steps: {sim.grid.population()}")
```

### HashLife for Large-Scale Simulation

```python
from src.hashlife import HashLife
from src.patterns import parse_rle, GOSPER_GLIDER_GUN_RLE

hl = HashLife()
cells, w, h = parse_rle(GOSPER_GLIDER_GUN_RLE)
padded = [[0]*64 for _ in range(64)]
for y in range(h):
    for x in range(w):
        padded[y][x] = cells[y][x]

node = hl.from_cells(padded, 64, 64)
result = hl.advance_pow2(node, 20)  # 2^20 = 1,048,576 generations
print(f"Population after 2^20 generations: {result.population}")
```

### Terminal Visualization

```python
from src.visualizer import run_visualizer
run_visualizer(width=60, height=30, rule_name="life", fps=10)
```

## Running Tests and Experiments

```bash
# Run all tests
make test

# Run benchmarks (baseline, comparison, memory profiling)
make benchmark

# Run experiments (sensitivity analysis, 2D rule classification)
make experiment

# Generate publication-quality figures from saved results
make figures

# Run everything
make all
```

## Project Structure

```
src/
  grid.py           # Core Grid class (list-of-lists, wrap/fixed boundary)
  grid_numpy.py     # NumPy-accelerated grid and rules (convolve2d)
  rules.py          # Elementary1DRule, LifeRule, GenericTotalisticRule
  simulator.py      # Simulator with step/run/reset/history
  hashlife.py       # Gosper HashLife algorithm (quadtree memoization)
  patterns.py       # RLE and plaintext pattern I/O
  analysis.py       # Shannon entropy, LZ complexity, Lyapunov exponent
  visualizer.py     # Terminal visualization (curses + Unicode)
  cli.py            # Command-line interface

tests/
  test_grid.py          # 17 grid tests
  test_rules.py         # 14 rule tests
  test_simulator.py     # 8 simulator tests
  test_hashlife.py      # 8 HashLife tests
  test_patterns.py      # 9 pattern I/O tests
  test_correctness.py   # 4 cross-engine validation tests

benchmarks/
  bench_baseline.py     # Naive engine baselines
  bench_comparison.py   # 3-engine performance comparison
  bench_memory.py       # Memory profiling and scalability

experiments/
  sensitivity.py        # Grid size and boundary condition analysis
  classify_2d_rules.py  # 2D outer-totalistic rule classification

figures/
  generate_figures.py   # Unified figure generation script
  fig1_*.png/pdf        # Performance comparison
  fig2_*.png/pdf        # HashLife speedup
  fig3_*.png/pdf        # Wolfram classification heatmap
  fig4_*.png/pdf        # 2D rule classification scatter
  fig5_*.png/pdf        # Sensitivity dynamics
  fig6_*.png/pdf        # Memory scaling
  fig7_*.png/pdf        # Boundary comparison

docs/
  research_report.md        # Full research report (4800+ words)
  literature_review.md      # Literature review (15 sources)
  problem_statement.md      # Scope and goals
  benchmarks.md             # Baseline benchmark analysis
  classification_methodology.md  # Metric definitions
  sensitivity_analysis.md   # Sensitivity findings
  prior_implementations.md  # Survey of 6 existing projects
  repo_analysis.md          # Initial repository analysis

results/                    # JSON result files from experiments
sources.bib                 # BibTeX bibliography (19 entries)
requirements.txt            # Pinned Python dependencies
Makefile                    # Build/test/run automation
```

## Simulation Engines

| Engine | Approach | Best For | Speedup |
|--------|----------|----------|---------|
| Naive  | Cell-by-cell Python loops | Correctness baseline, small grids | 1x |
| NumPy  | Vectorized convolution (scipy) | Medium grids, real-time display | 88-100x |
| HashLife | Quadtree memoization + macro-stepping | Large patterns, long runs | Exponential on regular patterns |

## References

See `sources.bib` for the complete bibliography. Key references:

- Wolfram, S. (2002). *A New Kind of Science*. Wolfram Media.
- Gosper, R.W. (1984). Exploiting regularities in large cellular spaces. *Physica D*, 10(1-2), 75-80.
- Gardner, M. (1970). The fantastic combinations of John Conway's new solitaire game "Life." *Scientific American*, 223(4), 120-123.

## License

Research project. See repository for details.
