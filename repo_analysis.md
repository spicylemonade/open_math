# Repository Analysis

## Project Overview
This repository contains a mathematical research project investigating the characterization of real numbers $r$ for which the Beatty sequence $\lfloor nr \rfloor$ contains a homogeneous linearly recurrent (C-finite) subsequence.

## File and Directory Structure

### Root Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview (currently minimal: "# open_math") |
| `research_rubric.json` | Research plan with 26 items across 5 phases; tracks progress with status fields; used by the frontend for monitoring |
| `research-report.md` | Comprehensive literature survey compiled by the orchestrator; covers Beatty sequences, Sturmian words, C-finite sequences, Wythoff arrays, decidability results, and key references |
| `sources.bib` | BibTeX bibliography for all consulted sources |
| `TASK_researcher_attempt_1.md` | Task instructions for the researcher agent (this run) |
| `.gitignore` | Excludes secrets (.env, .key, .pem), agent artifacts (TASK_*.md, agent_*.log), and internal dirs (.claude/, .codex/, .archivara/) |
| `.gitattributes` | Git LFS configuration for large binary files: .zip, .tar.gz, .dat, .stl, .h5, .pkl, .tar, .csv, .ply, .gz, .obj, .npz, .hdf5, .npy, .pickle, .parquet, .feather |

### Directories

| Directory | Purpose |
|-----------|---------|
| `results/` | Stores experimental results as JSON files (created during Phase 4) |
| `figures/` | Stores publication-quality figures as PNG and PDF (created during Phases 4-5) |
| `proofs/` | Stores mathematical proof documents in Markdown (created during Phase 3) |
| `.archivara/logs/` | Internal logging for the orchestration system; contains orchestrator.log and researcher_attempt_1.log |
| `.git/` | Git version control data; branch: research-lab-1770627146 |

### Module Interconnections

1. **Orchestration flow**: `TASK_researcher_attempt_1.md` → instructs agent → reads `research_rubric.json` → executes items → updates rubric
2. **Literature foundation**: `research-report.md` provides the knowledge base that informs all proof and experiment work
3. **Bibliography**: `sources.bib` collects citations referenced across `research-report.md`, proof files, and `paper.md`
4. **Data pipeline**: Python modules (to be created in Phase 2) → `results/` JSON files → `figures/` plots → `paper.md`
5. **Proof chain**: `proofs/rational_case.md` + `proofs/quadratic_case.md` + `proofs/only_if_direction.md` → `proofs/main_theorem.md` → `paper.md`

### Configuration Details

- **Git LFS** (`.gitattributes`): Configured for 17 binary/large-file extensions to prevent bloating the Git history with data files
- **Git Ignore** (`.gitignore`): Prevents committing secrets, agent task files, and orchestration logs
- **Research Rubric** (`research_rubric.json`): JSON schema with version, timestamps, agent status tracking (orchestrator/researcher/writer/reviewer), 5 phases with 26 items total, and summary counters
