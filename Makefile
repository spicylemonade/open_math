.PHONY: install test benchmark figures clean all

PYTHON ?= python3

all: install test benchmark figures

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/ -v

benchmark:
	$(PYTHON) -m scripts.run_benchmarks

figures:
	$(PYTHON) -m scripts.generate_figures

clean:
	rm -rf results/*.json results/*.md
	rm -rf figures/*.png figures/*.pdf
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
