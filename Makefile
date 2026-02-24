.PHONY: all install test baselines experiments figures clean

all: install test baselines experiments figures

install:
	pip install -r requirements.txt

test:
	@echo "=== Running unit tests ==="
	python3 heuristics.py
	python3 simulator.py
	python3 metrics.py
	python3 test_farb.py
	@echo "All unit tests passed."

baselines:
	@echo "=== Running baseline experiments ==="
	python3 run_baselines.py
	@echo "Baseline results saved to results/baselines/"

advanced:
	@echo "=== Running advanced heuristic experiments ==="
	python3 run_advanced.py
	@echo "Advanced results saved to results/advanced_baselines/"

experiments:
	@echo "=== Running comprehensive experiments ==="
	python3 run_experiments.py
	@echo "All experiment results saved to results/"

figures:
	@echo "=== Generating figures ==="
	python3 generate_figures.py
	@echo "Figures saved to figures/"

clean:
	rm -rf results/ figures/
	@echo "Results and figures removed."
