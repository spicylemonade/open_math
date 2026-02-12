# Dimensional Analysis on the Kissing Number Problem in R^5

This repository contains the computational framework and results for investigating
the kissing number problem in dimension 5 using a dimensional analysis approach
based on the derivative/integral relationships between n-ball volumes and surface
areas. The kissing number tau_5 is the maximum number of non-overlapping unit
spheres in R^5 that can simultaneously touch a central unit sphere. It is currently
known that 40 <= tau_5 <= 44, where the lower bound comes from the D5 lattice
and the upper bound from Delsarte's linear programming method.

The project implements and evaluates multiple computational approaches: cap packing
bounds via dimensional integration, the Delsarte linear programming bound with
Gegenbauer polynomial expansions, enhanced LP bounds augmented with dimensional
constraints (equatorial slicing, second-moment trace, and volume recurrence
consistency), direct construction attempts for 41-point configurations, contact
graph analysis of the D5 lattice, and cross-dimensional consistency checks. All
results are independently verified using multiple numerical methods including
high-precision arithmetic with mpmath at 50-digit precision.

## Installation

Requires Python 3.8 or later. Install all dependencies with:

```bash
pip install -r requirements.txt
```

The pinned dependency versions in `requirements.txt` are:

- numpy==2.2.6
- scipy==1.15.3
- mpmath==1.3.0
- matplotlib==3.10.8
- networkx==3.4.2

## Reproducing All Results

Run the full experiment suite with a single command:

```bash
python src/run_experiments.py
```

This executes 119 experiment configurations across 7 categories (cap packing
bounds, Delsarte LP polynomial search, enhanced bounds with dimensional
constraints, D5 lattice verification, greedy spherical code construction,
41st-point construction attempts, and cross-dimensional consistency checks).
All experiments use fixed random seeds for reproducibility. Results are written
to `results/experiments_summary.csv`.

## Verifying Results

To independently cross-check every claimed bound using at least two numerical
methods (including mpmath interval arithmetic at 50-digit precision):

```bash
python src/verify_results.py
```

This performs 8 categories of verification (ball volumes, surface areas, cap
areas, D5 lattice properties, cap packing bounds, the Delsarte n=8 polynomial,
contact graph structure, and local rigidity of the D5 configuration). All checks
are logged to `results/verification_log.txt`.

## Generating Figures

To produce all visualizations:

```bash
python src/generate_figures.py
```

This creates 4 publication-quality PNG figures in the `figures/` directory.

## Output Files

### results/

| File | Description |
|------|-------------|
| `experiments_summary.csv` | Full CSV of all 119 experiment results with method, dimension, parameters, bounds, runtime, and notes |
| `verification_log.txt` | Independent verification log with PASS/FAIL status for every claimed result |
| `repo_analysis.md` | Project structure analysis and computational environment description |
| `literature_review.md` | Survey of 13 papers on kissing numbers, Delsarte LP, SDP bounds, and related work |
| `dimensional_framework.md` | Mathematical derivation of the dimensional analysis framework with verified formulas |
| `dimensional_constraints.md` | Three classes of dimensional constraints on Gegenbauer coefficients |
| `d5_verification.txt` | Verification that 40 D5 lattice minimal vectors form a valid kissing configuration |
| `delsarte_baseline.txt` | Delsarte LP bounds for dimensions 3 through 8 via polynomial ansatz search |
| `enhanced_bound_results.txt` | Enhanced LP bounds with dimensional constraints and redundancy analysis |
| `baseline_metrics.md` | Comparison table of cap packing, Delsarte LP, and known bounds for dimensions 2-8 |
| `upper_bound_survey.md` | Survey of upper bound techniques and identified gaps for dimensional analysis |
| `construction_attempts.md` | Documentation of three strategies for constructing a 41st kissing vector in R^5 |
| `contact_graph_analysis.md` | Analysis of the D5 contact graph structure and local rigidity |
| `pyramid_decomposition.md` | Pyramid decomposition of spherical caps with three verified lemmas |
| `cross_dim_results.txt` | Cross-dimensional consistency check for tau_5 in {40,...,44} |
| `comparison_with_prior_work.md` | Comparison of our results against 10 papers from the literature |
| `sensitivity_analysis.md` | Sensitivity analysis of dimensional constraints across precisions and dimensions |
| `sensitivity_data.csv` | Raw sensitivity data: 24 rows covering 6 dimensions at 4 precision levels |

### figures/

| File | Description |
|------|-------------|
| `bound_comparison.png` | Grouped bar chart comparing cap packing, Delsarte LP, SDP, and known exact bounds for dimensions 2-8 |
| `dimensional_recurrence.png` | Four-panel plot of V_n, S_n, V_n/S_n = 1/n, and cap solid angle fractions |
| `cap_density.png` | Cap packing density vs dimension with tau_5 = 40 and tau_5 = 44 markers and exponential trend |
| `contact_graph.png` | Spring-layout network visualization of the 40-node, 12-regular D5 contact graph colored by coordinate pair |

## Source Files

### src/

| File | Description |
|------|-------------|
| `ndim_geometry.py` | N-dimensional ball volume V_n(R), surface area S_n(R), spherical cap area, and cap packing bound functions using both the Gamma function formula and the 2-step recurrence V_n = (2*pi/n)*R^2*V_{n-2} |
| `delsarte_lp.py` | Delsarte linear programming bound computation: Gegenbauer polynomial expansion, coefficient verification, and polynomial ansatz search for kissing number upper bounds |
| `d5_lattice.py` | Generation and verification of all 40 minimal vectors of the D5 lattice, inner product spectrum analysis, and contact graph structure computation |
| `spherical_codes.py` | Spherical code validator (checks unit norms and pairwise angular separation) and greedy spherical code optimizer with random initialization and L-BFGS-B local refinement |
| `enhanced_bound.py` | Enhanced Delsarte LP with three dimensional integration constraints (equatorial slicing D1, second-moment trace D2, volume recurrence consistency D3), redundancy analysis, and sensitivity reporting |
| `construct_kissing.py` | Three strategies for attempting to construct a 41-point kissing configuration in R^5: random grid search, nonlinear optimization, and algebraic construction from D5 symmetry subgroups |
| `cross_dim_check.py` | Cross-dimensional consistency checks using the volume recurrence to test whether tau_5 values in {40,...,44} are compatible with known tau_3 = 12 and tau_4 = 24 |
| `run_experiments.py` | Main experiment runner: executes all 119 experiment configurations across 7 categories with fixed random seeds and writes results to CSV |
| `verify_results.py` | Independent verification script: cross-checks every claimed result using at least two numerical methods including mpmath at 50-digit precision |
| `generate_figures.py` | Figure generation script: produces 4 PNG visualizations (bound comparison, dimensional recurrence, cap density, contact graph) |

## Citation

For references to the mathematical results, methods, and prior work used in this
project, see `sources.bib` in the repository root. This BibTeX file contains
entries for Delsarte (1973), Kabatyansky-Levenshtein (1978), Odlyzko-Sloane (1979),
Conway-Sloane's "Sphere Packings, Lattices and Groups", Pfender-Zong (2004),
Musin (2008), Cohn-Kumar (2007), Bachoc-Vallentin (2008), Mittelmann-Vallentin
(2010), Viazovska (2017), and other foundational works on kissing numbers and
spherical codes.
