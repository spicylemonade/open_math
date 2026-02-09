# Characterizing r for Which floor(nr) Contains a Homogeneous C-finite Subsequence

## Main Result

**Theorem.** The Beatty sequence floor(nr) (n = 1, 2, 3, ...) contains an infinite subsequence satisfying a homogeneous linear recurrence with constant rational coefficients if and only if r is a positive algebraic number.

- **Rational r = p/q:** The full sequence is C-finite (order q+1).
- **Quadratic irrational r:** Wythoff-type array rows yield order-2 recurrences.
- **Algebraic irrational r (degree >= 3):** Iterated Beatty compositions yield higher-order recurrences (Fraenkel 1994, Ballot 2017).
- **Transcendental r:** No C-finite subsequence exists (proved via Binet-form analysis).

## Installation

**Python version:** 3.10+

**Dependencies:**
```bash
pip install -r requirements.txt
```

## Repository Structure

### Core Modules

| File | Description |
|------|-------------|
| `beatty.py` | Beatty sequence computation with exact arithmetic for rationals and quadratic irrationals |
| `recurrence_detector.py` | Berlekamp-Massey algorithm for detecting homogeneous linear recurrences |
| `subsequence_extractor.py` | Extraction strategies: arithmetic progressions, iterated compositions, Wythoff rows |
| `baseline_pipeline.py` | Full pipeline: extract subsequences + detect recurrences + output JSON |
| `metrics.py` | Quality metrics: recurrence order, verified length, density, spectral radius |

### Proof Files

| File | Description |
|------|-------------|
| `proofs/rational_case.md` | Proof that floor(np/q) satisfies a(n)-a(n-1)-a(n-q)+a(n-q-1)=0 |
| `proofs/quadratic_case.md` | Two constructions for quadratic irrationals (Wythoff + iterated composition) |
| `proofs/only_if_direction.md` | Proof that transcendentals admit no C-finite Beatty subsequence |
| `proofs/bounded_cf_case.md` | Analysis of bounded continued fraction irrationals |
| `proofs/main_theorem.md` | Unified characterization theorem with full proof |

### Documentation

| File | Description |
|------|-------------|
| `paper.md` | Complete research paper (~7000 words) |
| `problem_statement.md` | Formal problem definition and conventions |
| `literature_review.md` | Comprehensive literature review with taxonomy |
| `proof_strategy.md` | Proof strategy and roadmap |
| `open_problems.md` | Gap analysis and open problems |
| `review_checklist.md` | Final review verification |
| `sources.bib` | BibTeX bibliography (21 entries) |

## Reproducing Experiments

### Rational experiments (255 test cases)
```bash
python run_rational_experiments.py
# Output: results/rational_experiments.json, results/rational_summary.md
```

### Quadratic irrational experiments (35 test cases)
```bash
python run_quadratic_experiments.py
# Output: results/quadratic_experiments.json
```

### Non-quadratic and CF boundary experiments
```bash
python run_nonquadratic_experiments.py
# Output: results/non_quadratic_experiments.json, results/cf_boundary_experiments.json
```

### Generate all figures
```bash
python generate_figures.py
python generate_extra_figures.py
python generate_venn_figure.py
# Output: figures/*.png, figures/*.pdf
```

### Run unit tests
```bash
python beatty.py
python recurrence_detector.py
python subsequence_extractor.py
python metrics.py
```
