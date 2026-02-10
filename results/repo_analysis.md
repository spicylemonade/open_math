# Repository Structure Analysis

## Overview
This repository is set up as a research project investigating unitary perfect numbers and Subbarao's finiteness conjecture.

## Directory Structure

### `figures/`
- **Purpose**: Storage for publication-quality plots and visualizations (PNG and PDF formats)
- **Contents**: Will contain growth constraint plots, factorization diagrams, sieve density charts, and product equation solution space visualizations

### `results/`
- **Purpose**: Storage for experimental data (JSON), analysis documents (Markdown), and intermediate results
- **Contents**: Will contain search metrics, proof verification results, literature reviews, and the final research report

### `.archivara/`
- **Purpose**: Logging infrastructure for the orchestration system
- **Contents**:
  - `logs/orchestrator.log` - Orchestrator agent activity log
  - `logs/researcher_attempt_1.log` - Researcher agent activity log

### `src/`
- **Purpose**: Main computational code directory for the research project
- **Contents**:
  - `__init__.py` - Package initialization
  - `utils/` - Shared helper functions and utilities
    - `__init__.py` - Utils subpackage initialization
  - Will contain: `unitary.py`, `abundance.py`, `search_brute.py`, `search_structured.py`, `product_analysis.py`, `modular_obstructions.py`, etc.

### `tests/`
- **Purpose**: Unit tests for all computational modules
- **Contents**:
  - `__init__.py` - Test package initialization
  - Will contain: `test_unitary.py`, `test_abundance.py`, etc.

## Configuration Files

### `research_rubric.json`
- **Purpose**: Master research plan and progress tracker with 26 items across 5 phases
- **Format**: JSON with phases, items, acceptance criteria, and status tracking

### `.gitattributes`
- **Purpose**: Git LFS tracking configuration for large binary files (`.gz`, `.npy`, `.h5`, `.csv`, etc.)

### `.gitignore`
- **Purpose**: Prevents committing secrets (`.env`, `.key`, `.pem`), task files, and orchestration logs

### `README.md`
- **Purpose**: Project readme (currently minimal - "open_math")

### `TASK_researcher_attempt_1.md`
- **Purpose**: Task specification for the researcher agent (excluded from git via .gitignore)

### `sources.bib`
- **Purpose**: BibTeX bibliography for all consulted references throughout the research
