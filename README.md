# MDPN: Most Delayed Palindromic Number Search

Systematic search for a number requiring more than 293 reverse-and-add iterations
to reach a palindrome, attempting to break the current world record set by
Dmitry Maslov in December 2021.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Compile C extension (requires gcc)
gcc -O3 -shared -fPIC -o src/fast_core.so src/fast_core.c

# Verify the current world record
python scripts/verify_record.py 1000206827388999999095750
# Output: Palindrome reached in 293 iterations (132-digit palindrome)

# Run tests
python -m pytest tests/ -v

# Run the full search
python scripts/run_search.py
```

## Project Structure

See [STRUCTURE.md](STRUCTURE.md) for details.

- `src/` — Core algorithms (baseline, optimized, pruning, parallel search)
- `tests/` — pytest test suite
- `scripts/` — Standalone scripts for search and verification
- `results/` — Experimental data and analysis
- `figures/` — Publication-quality plots
- `sources.bib` — Bibliography

## Key Results

After testing ~98 million candidates across 25-33 digit numbers using five
search strategies, no number exceeding 293 iterations was found. See
[results/RESULTS.md](results/RESULTS.md) for the full analysis.

## References

See [sources.bib](sources.bib) and [literature_review.md](literature_review.md).
