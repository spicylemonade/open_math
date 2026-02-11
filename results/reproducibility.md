# Reproducibility Guide

This document explains how to run each computational component of the research project
and describes expected outputs.

---

## 1. Prerequisites

### Python Version
- Python 3.10+ (tested with Python 3.10.17)

### Dependencies
Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- `sympy` (>= 1.12): Prime generation, factorization, primality testing
- `matplotlib` (>= 3.7): Figure generation
- `seaborn` (>= 0.12): Figure styling
- `numpy` (>= 1.24): Numerical arrays for plotting
- `pytest` (>= 7.0): Test runner

### Hardware Requirements
- **Minimum:** Any modern CPU, 2 GB RAM
- **Recommended:** Multi-core CPU, 4+ GB RAM
- Most scripts complete in under 60 seconds
- The exhaustive search (`src/exhaustive_search.py`) uses a 300-second timeout

---

## 2. Running the Test Suite

```bash
python -m pytest tests/ -v
```

**Expected output:** 32 tests pass (20 in `test_unitary.py`, 12 in `test_abundance.py`).
**Runtime:** ~1 second.

---

## 3. Running Individual Scripts

All scripts are run as Python modules from the repository root:

### 3.1 Brute-Force Search
```bash
python -m src.search_brute
```
**Output:** `results/brute_search_metrics.json`
**Expected:** Finds {6, 60, 90, 87360} up to 10^5. Confirms no UPNs in [87361, 10^6].
**Runtime:** ~30 seconds.

### 3.2 Structured Search
```bash
python -m src.search_structured
```
**Output:** `results/structured_search_metrics.json`
**Expected:** Finds 4 of 5 known UPNs via factorization enumeration with pruning.
**Runtime:** ~300 seconds (5-minute timeout).

### 3.3 Product Equation Analysis
```bash
python -m src.product_analysis
```
**Output:** `results/product_equation_results.json`
**Expected:** Max product table for k=1..50, threshold analysis, 4 solutions found for k<=6.
**Runtime:** ~10 seconds.

### 3.4 Modular Obstruction Analysis
```bash
python -m src.modular_obstructions
```
**Output:** `results/modular_analysis_results.json`
**Expected:** Allowed residues per modulus, all 5 UPNs verified, combined sieve density.
**Runtime:** ~5 seconds.

### 3.5 Exhaustive Search
```bash
python -m src.exhaustive_search
```
**Output:** `results/exhaustive_search_results.json`
**Expected:** 4 UPNs found, 74 cells fully searched, 240 timed out. No new UPNs.
**Runtime:** ~300 seconds (5-minute timeout).

### 3.6 Growth Constraint Validation
```bash
python -m src.validate_growth
```
**Output:** `results/growth_validation.json`, `figures/growth_constraint.png`, `figures/growth_constraint.pdf`
**Expected:** f(m)=5 for m>=9, f(m) non-decreasing, feasible region analysis.
**Runtime:** ~5 seconds.

### 3.7 Modular Validation
```bash
python -m src.validate_modular
```
**Output:** `results/modular_validation.json`
**Expected:** All 5 UPNs pass. Pass rate ~0.606 for 10^6 random integers. Sieve density ~0.606.
**Runtime:** ~5 seconds.

### 3.8 Proof Verification
```bash
python -m src.verify_proof
```
**Output:** `results/proof_verification.json`
**Expected:** All 19 verifications pass (18 claims + appendix).
**Runtime:** ~10 seconds.

### 3.9 Figure Generation
```bash
python -m src.generate_figures
```
**Output:** `figures/known_upn_factorizations.{png,pdf}`, `figures/product_equation_solutions.{png,pdf}`, `figures/modular_sieve_density.{png,pdf}`
**Expected:** 3 two-panel figures with proper labels, titles, legends.
**Runtime:** ~5 seconds.

---

## 4. Random Seeds

All stochastic computations use fixed random seed 42 for reproducibility:
- `src/validate_modular.py`: `random.seed(42)` for random integer testing
- `src/search_structured.py`: Deterministic (no randomness)
- `src/exhaustive_search.py`: Deterministic (no randomness)

---

## 5. Output File Locations

### Results (JSON data)
| File | Description |
|------|-------------|
| `results/brute_search_metrics.json` | Brute-force search timing and results |
| `results/structured_search_metrics.json` | Structured search metrics |
| `results/product_equation_results.json` | Product equation enumeration results |
| `results/modular_analysis_results.json` | Modular obstruction analysis |
| `results/exhaustive_search_results.json` | Exhaustive search cell-by-cell results |
| `results/growth_validation.json` | f(m) values and feasibility analysis |
| `results/modular_validation.json` | Modular validation with random testing |
| `results/proof_verification.json` | Claim-by-claim verification results |

### Results (Markdown documents)
| File | Description |
|------|-------------|
| `results/problem_formalization.md` | Mathematical definitions and formalization |
| `results/literature_review.md` | Comprehensive literature review |
| `results/known_results.md` | Catalog of known partial results |
| `results/research_gaps.md` | Identified research gaps |
| `results/baseline_comparison.md` | Brute vs structured search comparison |
| `results/product_equation_analysis.md` | Product equation analysis |
| `results/uniform_finiteness.md` | Subbarao-Warren uniformity analysis |
| `results/density_analysis.md` | Analytic density bounds |
| `results/modular_analysis.md` | Modular obstruction documentation |
| `results/growth_constraint.md` | Growth constraint f(m) analysis |
| `results/finiteness_attempt.md` | 18-claim finiteness proof attempt |
| `results/comparison_with_prior_work.md` | Comparison with literature |
| `results/synthesis.md` | Synthesis of all results |
| `results/final_report.md` | Final research report (5000+ words) |

### Figures
| File | Description |
|------|-------------|
| `figures/growth_constraint.{png,pdf}` | f(m) and feasible region plots |
| `figures/known_upn_factorizations.{png,pdf}` | UPN factorization bar charts |
| `figures/product_equation_solutions.{png,pdf}` | Product equation solution space |
| `figures/modular_sieve_density.{png,pdf}` | Cumulative sieve density plots |

---

## 6. Full Reproduction

To reproduce all results from scratch:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Run all computational scripts (total ~12 minutes)
python -m src.search_brute
python -m src.product_analysis
python -m src.modular_obstructions
python -m src.validate_growth
python -m src.validate_modular
python -m src.verify_proof
python -m src.generate_figures

# Longer runs (5+ minutes each)
python -m src.search_structured
python -m src.exhaustive_search
```

All JSON outputs use deterministic computation (or seed=42 for randomized tests),
so results should be identical across runs on any platform with the specified dependencies.
