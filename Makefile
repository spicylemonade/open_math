.PHONY: install test benchmark experiment figures report all clean

# Install all dependencies
install:
	pip install -r requirements.txt

# Run all unit tests
test:
	python -m pytest tests/ -v

# Run baseline and comparison benchmarks
benchmark:
	python benchmarks/bench_baseline.py
	python benchmarks/bench_comparison.py
	python benchmarks/bench_memory.py

# Run all experiments
experiment:
	python experiments/sensitivity.py
	python experiments/classify_2d_rules.py

# Generate all figures from saved results
figures:
	python figures/generate_figures.py

# Generate the full research report (already written as markdown)
report:
	@echo "Research report is at docs/research_report.md"
	@wc -w docs/research_report.md

# Run everything: install, test, benchmark, experiment, figures
all: install test benchmark experiment figures report

# Remove generated outputs
clean:
	rm -rf results/*.json
	rm -rf figures/*.png figures/*.pdf
	@echo "Cleaned generated outputs. Source code and docs preserved."
