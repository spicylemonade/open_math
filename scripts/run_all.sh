#!/bin/bash
# Full pipeline reproduction script
# Usage: bash scripts/run_all.sh
#
# Reproduces the complete experimental pipeline:
# 1. Generate benchmark instances
# 2. Run baseline benchmarks
# 3. Train GNN edge scorer
# 4. Run hybrid solver experiments
# 5. Generate figures
#
# Prerequisites: pip install -r requirements.txt
# Expected total runtime: ~30-60 minutes depending on hardware

set -e

echo "========================================"
echo "Step 1: Generate benchmark instances"
echo "========================================"
python3 scripts/generate_benchmarks.py

echo ""
echo "========================================"
echo "Step 2: Run baseline benchmarks"
echo "========================================"
python3 scripts/run_benchmarks.py

echo ""
echo "========================================"
echo "Step 3: Train GNN edge scorer"
echo "========================================"
python3 scripts/train_edge_scorer.py

echo ""
echo "========================================"
echo "Step 4: Run Phase 4 experiments"
echo "========================================"
python3 run_phase4.py

echo ""
echo "========================================"
echo "Step 5: Generate figures"
echo "========================================"
python3 scripts/generate_figures.py

echo ""
echo "========================================"
echo "Pipeline complete!"
echo "========================================"
echo "Results stored in:"
echo "  results/baseline_results.csv"
echo "  results/full_comparison.csv"
echo "  results/ablation_results.csv"
echo "  results/statistical_tests.json"
echo "  results/scalability_results.csv"
echo "  figures/*.png"
echo "  FINDINGS.md"
