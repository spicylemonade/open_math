.PHONY: install test benchmark figures report clean all

# Default target
all: install test benchmark figures

# Install dependencies
install:
	pip install -r requirements.txt

# Run all tests
test:
	python -m pytest tests/ -v

# Generate benchmark instances and run all experiments
benchmark: benchmark-instances benchmark-baselines benchmark-full benchmark-analysis benchmark-exact

benchmark-instances:
	python benchmarks/generate_instances.py

benchmark-baselines:
	python benchmarks/collect_baselines.py

benchmark-full:
	python benchmarks/run_all.py

benchmark-analysis:
	python benchmarks/analysis.py

benchmark-exact:
	python benchmarks/exact_validation.py

benchmark-scalability:
	python benchmarks/scalability.py

# Generate all figures
figures:
	python benchmarks/generate_figures.py
	python benchmarks/scalability_collect.py

# Display report location
report:
	@echo "Research report: docs/research_report.md"
	@echo "Word count:"
	@wc -w docs/research_report.md

# Clean generated files
clean:
	rm -rf results/*.json
	rm -rf figures/*.png figures/*.pdf
	rm -rf benchmarks/*.csv benchmarks/*.json
	rm -rf __pycache__ src/__pycache__ tests/__pycache__ benchmarks/__pycache__
	find . -name '*.pyc' -delete
