# Project Structure

## Most Delayed Palindromic Number (MDPN) World Record Search

### Directories

| Directory | Purpose |
|-----------|---------|
| `src/` | Core Python modules: reverse-and-add engine, search algorithms, optimizations |
| `tests/` | pytest test suite for verification and correctness |
| `scripts/` | Standalone scripts for running searches and verifying records |
| `results/` | Experimental data files (CSV, JSON, Markdown reports) |
| `figures/` | Publication-quality plots (PNG @ 300 DPI and PDF) |

### Key Files

| File | Purpose |
|------|---------|
| `research_rubric.json` | Research plan with phase/item tracking |
| `sources.bib` | BibTeX bibliography of all consulted sources |
| `STRUCTURE.md` | This file — project layout documentation |
| `src/reverse_add.py` | Baseline reverse-and-add implementation |
| `src/fast_reverse_add.py` | Optimized implementation using gmpy2/GMP |
| `src/search_pruning.py` | Digit-pair symmetry pruning |
| `src/parallel_search.py` | Multiprocessing-based parallel search |
| `src/heuristic_search.py` | Heuristic-guided candidate selection |
| `src/lychrel_detector.py` | Early termination for Lychrel candidates |
| `tests/test_reverse_add.py` | Core algorithm test suite |
| `scripts/verify_record.py` | Single-command record verification |
