# Repository Structure Analysis

## Overview

This repository is a **fresh scaffold** for the Erdős–Straus conjecture verification project. It was initialized with minimal boilerplate and contains no pre-existing computational code.

## Directory Structure

```
repo/
├── .git/                      # Git version control
├── .gitignore                 # Excludes .env, keys, logs, TASK files
├── .gitattributes             # Git LFS and attribute configuration
├── .archivara/                # Orchestration logs (gitignored)
│   └── logs/
│       ├── orchestrator.log
│       └── researcher_attempt_1.log
├── README.md                  # Placeholder: "# open_math" (empty scaffold)
├── TASK_researcher_attempt_1.md  # Task instructions for researcher agent (gitignored)
├── research_rubric.json       # Research plan with 25 items across 5 phases
├── sources.bib                # Bibliography file (newly created, empty)
├── results/                   # Directory for experimental results (newly created)
├── figures/                   # Directory for publication-quality figures (newly created)
├── src/                       # Directory for source code (newly created)
├── benchmarks/                # Directory for benchmark scripts (newly created)
└── tests/                     # Directory for test scripts (newly created)
```

## File Purposes

| File/Directory | Purpose |
|---|---|
| `research_rubric.json` | Master research plan with 25 items across 5 phases, tracking status of each task |
| `README.md` | Project README (currently placeholder, to be updated in Phase 5) |
| `.gitignore` | Prevents committing secrets (.env, .key, .pem), agent logs, and task files |
| `sources.bib` | BibTeX bibliography for all references consulted during research |
| `results/` | Stores experimental results as JSON and Markdown files |
| `figures/` | Stores publication-ready plots (PNG at 300 DPI and PDF) |
| `src/` | Source code for solvers, sieves, and computational tools |
| `benchmarks/` | Benchmark scripts for measuring solver performance |
| `tests/` | Test scripts for verification and reproducibility |

## Confirmation

- **No pre-existing code**: The repository contains no Python, C, or Cython source files.
- **Fresh scaffold**: Only configuration files (`.gitignore`, `.gitattributes`), the research rubric, and a placeholder README exist.
- **Required directories created**: `figures/`, `results/`, `src/`, `benchmarks/`, `tests/` are all present and empty.
- **Bibliography initialized**: `sources.bib` created with header comment.

## Research Rubric Summary

The `research_rubric.json` defines 25 research items across 5 phases:

1. **Phase 1** (6 items): Problem Analysis & Literature Review
2. **Phase 2** (4 items): Baseline Implementation & Metrics
3. **Phase 3** (5 items): Core Research & Novel Approaches
4. **Phase 4** (6 items): Experiments & Evaluation
5. **Phase 5** (4 items): Analysis & Documentation

All items start as "pending" and will be worked through sequentially.
