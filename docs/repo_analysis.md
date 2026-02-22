# Repository Structure Analysis

## Existing Directory Structure

The repository was initialized as a greenfield project with the following structure:

```
repo/
├── .archivara/          # Archivara orchestration logs
│   └── logs/
│       ├── orchestrator.log
│       └── researcher_attempt_1.log
├── .git/                # Git repository metadata
├── .gitignore           # Ignores .env files, secrets, .claude/, .codex/, .archivara/, TASK_*.md
├── .gitattributes       # Git attributes configuration
├── README.md            # Contains only: "# open_math" (effectively empty)
├── research_rubric.json # Research task rubric (25 items across 5 phases)
├── TASK_researcher_attempt_1.md  # Task specification (gitignored)
├── figures/             # Directory for output figures (empty)
├── results/             # Directory for experimental results (empty)
└── sources.bib          # Bibliography file (newly created)
```

## Key Observations

1. **Greenfield project**: There are **no existing code modules**, libraries, or source files. The repository contains only configuration files (`.gitignore`, `.gitattributes`), a stub README, and the research rubric.

2. **No Python packages**: No `setup.py`, `pyproject.toml`, `requirements.txt`, or any Python source files exist.

3. **No test infrastructure**: No test files, `pytest.ini`, or test configuration.

4. **Pre-existing directories**: Only `.archivara/` exists as a non-standard directory (for orchestration logging). The `figures/` and `results/` directories were created as part of project setup.

5. **.gitignore contents**:
   - `.env`, `.env.*`, `.env.local` — environment/secrets files
   - `*.key`, `*.pem` — cryptographic key files
   - `.claude/`, `.codex/` — AI assistant working directories
   - `.archivara/` — orchestration logs
   - `TASK_*.md` — task specification files
   - `agent_*.log`, `orchestration.log` — log files

## Proposed Directory Layout

```
repo/
├── src/                 # Core simulator source code
│   ├── __init__.py
│   ├── grid.py          # Grid data structure and cell state management
│   ├── grid_numpy.py    # NumPy-accelerated grid implementation
│   ├── rules.py         # CA rule engine (elementary, Life, totalistic)
│   ├── simulator.py     # Simulation loop and history tracking
│   ├── hashlife.py      # HashLife algorithm implementation
│   ├── patterns.py      # Pattern I/O (RLE, plaintext formats)
│   ├── visualizer.py    # Terminal-based visualization
│   ├── analysis.py      # Complexity classification metrics
│   └── cli.py           # Command-line interface
├── tests/               # Unit and integration tests
│   ├── test_grid.py
│   ├── test_rules.py
│   ├── test_simulator.py
│   ├── test_hashlife.py
│   ├── test_patterns.py
│   └── test_correctness.py
├── benchmarks/          # Performance benchmark scripts
│   ├── bench_baseline.py
│   ├── bench_comparison.py
│   └── bench_memory.py
├── experiments/         # Experimental scripts
│   ├── classify_2d_rules.py
│   └── sensitivity.py
├── docs/                # Documentation
│   ├── repo_analysis.md
│   ├── problem_statement.md
│   ├── literature_review.md
│   ├── prior_implementations.md
│   ├── benchmarks.md
│   ├── classification_methodology.md
│   ├── sensitivity_analysis.md
│   ├── research_report.md
│   ├── comparison_table.md
│   └── validation_checklist.md
├── data/                # Embedded test patterns and data files
├── results/             # JSON output from experiments
├── figures/             # PNG and PDF figures
├── sources.bib          # BibTeX bibliography
├── requirements.txt     # Python dependencies
├── Makefile             # Build/run automation
└── README.md            # Project documentation
```

## Conclusion

This is a **greenfield project** starting from an empty repository. All source code, tests, benchmarks, and documentation must be created from scratch. The proposed layout follows standard Python project conventions with clear separation of concerns between core library code (`src/`), tests (`tests/`), benchmarks (`benchmarks/`), experiments (`experiments/`), and documentation (`docs/`).
