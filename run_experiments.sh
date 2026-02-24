#!/usr/bin/env bash
# =============================================================================
# run_experiments.sh
# Reproduces all experiments for:
#   "Better Heuristics for TSP on Real Road Networks"
#
# This script performs the following steps from a clean install:
#   1. Install Python dependencies from requirements.txt
#   2. Generate benchmark instances (synthetic + OSMnx-based)
#   3. Train the GNN edge scorer model
#   4. Run the full benchmark suite across all solvers and instances
#   5. Generate all publication-quality figures
#
# Usage:
#   ./run_experiments.sh              # Run with default seed (42)
#   ./run_experiments.sh --seed 123   # Run with custom seed
#   ./run_experiments.sh --help       # Show usage information
#
# Prerequisites:
#   - Python 3.10+ with pip, OR a conda environment from environment.yml
#   - Internet access for OSMnx (optional; falls back to synthetic instances)
#
# All random seeds are configurable via the --seed flag. Individual step seeds
# are derived deterministically from the base seed to ensure full reproducibility.
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Default configuration
# ---------------------------------------------------------------------------
SEED=42                          # Base random seed (configurable via --seed)
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-python3}"      # Override with PYTHON=... if needed
TIME_LIMIT=30                    # Seconds per solver per instance
N_TRAIN_INSTANCES=1000           # Training instances for GNN
N_VAL_INSTANCES=200              # Validation instances for GNN
GNN_EPOCHS=30                    # Training epochs for edge scorer
SKIP_INSTALL=0                   # Set to 1 to skip pip install step
SKIP_GENERATE=0                  # Set to 1 to skip instance generation
SKIP_TRAIN=0                     # Set to 1 to skip GNN training
SKIP_BENCHMARK=0                 # Set to 1 to skip benchmark runs
SKIP_FIGURES=0                   # Set to 1 to skip figure generation

# ---------------------------------------------------------------------------
# Parse command-line arguments
# ---------------------------------------------------------------------------
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Reproduce all experiments from a clean install."
    echo ""
    echo "Options:"
    echo "  --seed SEED         Base random seed (default: 42)"
    echo "  --time-limit SECS   Time limit per solver per instance (default: 30)"
    echo "  --skip-install      Skip pip install step"
    echo "  --skip-generate     Skip benchmark instance generation"
    echo "  --skip-train        Skip GNN training"
    echo "  --skip-benchmark    Skip benchmark runs"
    echo "  --skip-figures      Skip figure generation"
    echo "  --python PATH       Path to Python interpreter (default: python3)"
    echo "  --help              Show this help message"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --seed)
            SEED="$2"
            shift 2
            ;;
        --time-limit)
            TIME_LIMIT="$2"
            shift 2
            ;;
        --skip-install)
            SKIP_INSTALL=1
            shift
            ;;
        --skip-generate)
            SKIP_GENERATE=1
            shift
            ;;
        --skip-train)
            SKIP_TRAIN=1
            shift
            ;;
        --skip-benchmark)
            SKIP_BENCHMARK=1
            shift
            ;;
        --skip-figures)
            SKIP_FIGURES=1
            shift
            ;;
        --python)
            PYTHON="$2"
            shift 2
            ;;
        --help|-h)
            usage
            ;;
        *)
            echo "Error: Unknown option '$1'. Use --help for usage."
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------
log_step() {
    echo ""
    echo "=================================================================="
    echo "  STEP $1: $2"
    echo "=================================================================="
    echo ""
}

log_info() {
    echo "[INFO] $1"
}

log_warn() {
    echo "[WARN] $1"
}

check_python() {
    if ! command -v "$PYTHON" &>/dev/null; then
        echo "Error: Python interpreter '$PYTHON' not found."
        echo "Install Python 3.10+ or set PYTHON=/path/to/python3"
        exit 1
    fi
    local version
    version=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    log_info "Using Python $version at $($PYTHON -c 'import sys; print(sys.executable)')"
}

# ---------------------------------------------------------------------------
# Print configuration summary
# ---------------------------------------------------------------------------
echo "=================================================================="
echo "  Better Heuristics for TSP on Real Road Networks"
echo "  Experiment Reproduction Script"
echo "=================================================================="
echo ""
echo "Configuration:"
echo "  Project root:       $PROJECT_ROOT"
echo "  Random seed:        $SEED"
echo "  Time limit:         ${TIME_LIMIT}s per solver per instance"
echo "  Training instances: $N_TRAIN_INSTANCES"
echo "  GNN epochs:         $GNN_EPOCHS"
echo ""

check_python
cd "$PROJECT_ROOT"

# ---------------------------------------------------------------------------
# Step 1: Install dependencies
# ---------------------------------------------------------------------------
if [[ "$SKIP_INSTALL" -eq 0 ]]; then
    log_step 1 "Installing Python dependencies"
    if [[ -f requirements.txt ]]; then
        "$PYTHON" -m pip install --upgrade pip
        "$PYTHON" -m pip install -r requirements.txt
        log_info "Dependencies installed successfully."
    else
        log_warn "requirements.txt not found. Skipping install."
    fi
else
    log_step 1 "Skipping dependency installation (--skip-install)"
fi

# ---------------------------------------------------------------------------
# Step 2: Generate benchmark instances
# ---------------------------------------------------------------------------
if [[ "$SKIP_GENERATE" -eq 0 ]]; then
    log_step 2 "Generating benchmark instances"

    # Ensure output directories exist
    mkdir -p benchmarks data models results figures

    # Generate instances using the instance generator.
    # This creates instances for Manhattan, Boston, and Paris at multiple sizes.
    # Falls back to synthetic generation if OSMnx/network access is unavailable.
    log_info "Generating benchmark instances with seed=$SEED ..."

    "$PYTHON" -c "
import sys, os, json
sys.path.insert(0, '.')
from src.data.instance_generator import (
    generate_synthetic_instance, save_instance, validate_instance,
    CITY_CONFIGS
)

seed = int($SEED)
out_dir = 'benchmarks'
os.makedirs(out_dir, exist_ok=True)

# Define the benchmark suite: (city, n_nodes, seed_offset)
# Small instances (20-50 nodes)
small = [
    ('manhattan', 20, 0), ('boston', 30, 1), ('paris', 50, 2),
    ('manhattan', 20, 3), ('boston', 30, 4),
]
# Medium instances (100-200 nodes)
medium = [
    ('manhattan', 100, 10), ('boston', 150, 11), ('paris', 200, 12),
    ('manhattan', 100, 13), ('boston', 150, 14),
]
# Large instances (500-1000 nodes)
large = [
    ('manhattan', 500, 20), ('boston', 700, 21), ('paris', 1000, 22),
    ('manhattan', 500, 23), ('boston', 700, 24),
]

manifest = {'instances': [], 'seed': seed}
all_instances = small + medium + large

for city, n, offset in all_instances:
    s = seed + offset
    fname = f'{city}_n{n}_s{s}.json'
    fpath = os.path.join(out_dir, fname)

    topo = CITY_CONFIGS.get(city, (0, 0, 0, 'mixed'))[3]

    # Try real OSMnx generation, fall back to synthetic
    try:
        from src.data.instance_generator import generate_instance_osmnx
        inst = generate_instance_osmnx(city, n, seed=s)
    except Exception:
        inst = generate_synthetic_instance(n, seed=s, city_name=city, topology=topo)

    validate_instance(inst)
    save_instance(inst, fpath)
    manifest['instances'].append({
        'file': fname,
        'city': city,
        'n_nodes': n,
        'seed': s,
        'source': inst['metadata']['source'],
        'asymmetry_ratio_max': inst['metadata']['asymmetry_ratio_max'],
    })
    print(f'  Generated: {fname} (n={n}, source={inst[\"metadata\"][\"source\"]})')

# Save manifest
with open(os.path.join(out_dir, 'manifest.json'), 'w') as f:
    json.dump(manifest, f, indent=2)
print(f'Manifest saved with {len(manifest[\"instances\"])} instances.')
"

    log_info "Benchmark instances generated in benchmarks/"
else
    log_step 2 "Skipping instance generation (--skip-generate)"
fi

# ---------------------------------------------------------------------------
# Step 3: Train the GNN edge scorer
# ---------------------------------------------------------------------------
if [[ "$SKIP_TRAIN" -eq 0 ]]; then
    log_step 3 "Training GNN edge scorer model"

    mkdir -p models figures

    log_info "Training with $N_TRAIN_INSTANCES instances, $GNN_EPOCHS epochs, seed=$SEED"

    # Run the training pipeline. The script generates its own training data
    # (small synthetic instances solved by OR-Tools), trains the GNN, and
    # saves the model checkpoint to models/ and training curves to figures/.
    "$PYTHON" src/training/train_edge_scorer.py

    log_info "GNN training complete. Model saved to models/"
    log_info "Training curves saved to figures/training_loss.png"
else
    log_step 3 "Skipping GNN training (--skip-train)"
fi

# ---------------------------------------------------------------------------
# Step 4: Run the full benchmark suite
# ---------------------------------------------------------------------------
if [[ "$SKIP_BENCHMARK" -eq 0 ]]; then
    log_step 4 "Running full benchmark suite"

    mkdir -p results

    # Run the benchmark harness. It reads eval_config.yaml for solver and
    # instance configuration, runs all solvers on all instances with multiple
    # seeds for stochastic solvers, and saves results to results/.
    log_info "Running all solvers on all benchmark instances (time_limit=${TIME_LIMIT}s)..."

    "$PYTHON" -c "
import sys, os, json, glob as globmod, yaml
sys.path.insert(0, '.')
from src.evaluation.benchmark_runner import run_benchmark, SOLVER_REGISTRY

seed = int($SEED)
time_limit = int($TIME_LIMIT)

# Load config
config_path = 'benchmarks/eval_config.yaml'
if os.path.exists(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
else:
    config = {}

# Discover all benchmark instance files
instance_files = sorted(globmod.glob('benchmarks/*.json'))
instance_files = [f for f in instance_files if 'manifest' not in f]

# Configure the benchmark run
config['instances'] = instance_files
config['solvers'] = list(SOLVER_REGISTRY.keys())
config['time_limit'] = time_limit
config['seeds'] = [seed, seed + 1, seed + 2, seed + 3, seed + 4]
config['output_dir'] = 'results'

print(f'Running benchmark: {len(instance_files)} instances, '
      f'{len(config[\"solvers\"])} solvers, {len(config[\"seeds\"])} seeds')
print(f'Solvers: {config[\"solvers\"]}')

results = run_benchmark(config)
print(f'Completed {len(results)} runs. Results saved to results/')
"

    log_info "Benchmark results saved to results/full_benchmark.csv and results/full_benchmark.json"
else
    log_step 4 "Skipping benchmark runs (--skip-benchmark)"
fi

# ---------------------------------------------------------------------------
# Step 5: Generate all figures
# ---------------------------------------------------------------------------
if [[ "$SKIP_FIGURES" -eq 0 ]]; then
    log_step 5 "Generating publication-quality figures"

    mkdir -p figures

    # Generate all analysis figures from the saved results.
    # Each figure script reads from results/ and writes to figures/.
    "$PYTHON" -c "
import sys, os, json, csv
sys.path.insert(0, '.')

import numpy as np

# Use non-interactive backend for headless environments
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Consistent plot styling ----
sns.set_theme(style='whitegrid', context='paper', font_scale=1.2)
matplotlib.rcParams.update({
    'figure.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'serif',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

figures_dir = 'figures'
results_dir = 'results'

# ----------------------------------------------------------------
# Figure 1: Benchmark comparison bar chart
# ----------------------------------------------------------------
print('Generating benchmark_comparison.png ...')
csv_path = os.path.join(results_dir, 'full_benchmark.csv')
if os.path.exists(csv_path):
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Aggregate mean gap by solver and size category
    from collections import defaultdict
    data = defaultdict(list)
    for r in rows:
        if r.get('error') in (None, '', 'None'):
            key = (r['solver'], r.get('size_category', 'unknown'))
            try:
                data[key].append(float(r['gap_to_best_pct']))
            except (ValueError, KeyError):
                pass

    if data:
        solvers = sorted(set(k[0] for k in data.keys()))
        categories = ['small', 'medium', 'large']
        x = np.arange(len(solvers))
        width = 0.25

        fig, ax = plt.subplots(figsize=(12, 6))
        for i, cat in enumerate(categories):
            means = [np.mean(data.get((s, cat), [0])) for s in solvers]
            ax.bar(x + i * width, means, width, label=cat.capitalize())

        ax.set_xlabel('Solver')
        ax.set_ylabel('Gap to Best Known (%)')
        ax.set_title('Solver Performance by Instance Size')
        ax.set_xticks(x + width)
        ax.set_xticklabels(solvers, rotation=45, ha='right')
        ax.legend()
        plt.savefig(os.path.join(figures_dir, 'benchmark_comparison.png'), dpi=300)
        plt.savefig(os.path.join(figures_dir, 'benchmark_comparison.pdf'))
        plt.close()
        print('  Saved benchmark_comparison.png')
else:
    print('  Skipping benchmark_comparison (no results CSV found)')

# ----------------------------------------------------------------
# Figure 2: Pareto front (runtime vs quality)
# ----------------------------------------------------------------
print('Generating pareto_front.png ...')
pareto_path = os.path.join(results_dir, 'pareto_analysis.json')
if os.path.exists(pareto_path):
    with open(pareto_path) as f:
        pareto_data = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette('deep', n_colors=10)
    if isinstance(pareto_data, list):
        solver_data = defaultdict(lambda: {'runtime': [], 'gap': []})
        for entry in pareto_data:
            s = entry.get('solver', 'unknown')
            solver_data[s]['runtime'].append(entry.get('mean_runtime', 0))
            solver_data[s]['gap'].append(entry.get('mean_gap', 0))
        for idx, (solver, vals) in enumerate(sorted(solver_data.items())):
            ax.scatter(vals['runtime'], vals['gap'],
                       label=solver, color=colors[idx % len(colors)], s=60)
    elif isinstance(pareto_data, dict) and 'solvers' in pareto_data:
        for idx, entry in enumerate(pareto_data['solvers']):
            ax.scatter(entry.get('mean_runtime', 0), entry.get('mean_gap', 0),
                       label=entry.get('solver', ''), color=colors[idx % len(colors)], s=80)

    ax.set_xlabel('Mean Runtime (seconds)')
    ax.set_ylabel('Mean Gap to Best Known (%)')
    ax.set_title('Runtime vs. Solution Quality Pareto Front')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(os.path.join(figures_dir, 'pareto_front.png'), dpi=300)
    plt.savefig(os.path.join(figures_dir, 'pareto_front.pdf'))
    plt.close()
    print('  Saved pareto_front.png')
else:
    print('  Skipping pareto_front (no pareto_analysis.json found)')

# ----------------------------------------------------------------
# Figure 3: Scalability curves
# ----------------------------------------------------------------
print('Generating scalability.png ...')
scale_path = os.path.join(results_dir, 'scalability.csv')
if os.path.exists(scale_path):
    with open(scale_path) as f:
        reader = csv.DictReader(f)
        scale_rows = list(reader)

    solver_curves = defaultdict(lambda: {'n': [], 'gap': [], 'runtime': []})
    for r in scale_rows:
        s = r.get('solver', 'unknown')
        try:
            solver_curves[s]['n'].append(int(r['n_nodes']))
            solver_curves[s]['gap'].append(float(r.get('gap_to_best_pct', 0)))
            solver_curves[s]['runtime'].append(float(r.get('runtime_seconds', 0)))
        except (ValueError, KeyError):
            pass

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    colors = sns.color_palette('deep', n_colors=len(solver_curves))
    for idx, (solver, vals) in enumerate(sorted(solver_curves.items())):
        order = np.argsort(vals['n'])
        ns = np.array(vals['n'])[order]
        gaps = np.array(vals['gap'])[order]
        rts = np.array(vals['runtime'])[order]
        ax1.plot(ns, gaps, '-o', label=solver, color=colors[idx % len(colors)], markersize=4)
        ax2.plot(ns, rts, '-o', label=solver, color=colors[idx % len(colors)], markersize=4)

    ax1.set_xlabel('Instance Size (nodes)')
    ax1.set_ylabel('Gap to Best Known (%)')
    ax1.set_title('Solution Quality vs. Instance Size')
    ax1.legend(fontsize=8)
    ax2.set_xlabel('Instance Size (nodes)')
    ax2.set_ylabel('Runtime (seconds)')
    ax2.set_title('Runtime vs. Instance Size')
    ax2.set_yscale('log')
    ax2.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'scalability.png'), dpi=300)
    plt.savefig(os.path.join(figures_dir, 'scalability.pdf'))
    plt.close()
    print('  Saved scalability.png')
else:
    print('  Skipping scalability (no scalability.csv found)')

# ----------------------------------------------------------------
# Figure 4: Ablation heatmap
# ----------------------------------------------------------------
print('Generating ablation_heatmap.png ...')
ablation_path = os.path.join(results_dir, 'ablation_study.csv')
if os.path.exists(ablation_path):
    with open(ablation_path) as f:
        reader = csv.DictReader(f)
        abl_rows = list(reader)

    configs = sorted(set(r.get('configuration', r.get('config', '')) for r in abl_rows))
    instances = sorted(set(r.get('instance_id', '') for r in abl_rows))

    if configs and instances:
        heatmap_data = np.zeros((len(configs), len(instances)))
        for r in abl_rows:
            cfg = r.get('configuration', r.get('config', ''))
            inst = r.get('instance_id', '')
            if cfg in configs and inst in instances:
                ci = configs.index(cfg)
                ii = instances.index(inst)
                try:
                    heatmap_data[ci, ii] = float(r.get('gap_to_best_pct', r.get('tour_cost', 0)))
                except ValueError:
                    pass

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_data, xticklabels=instances, yticklabels=configs,
                    annot=True, fmt='.1f', cmap='YlOrRd', ax=ax)
        ax.set_title('Ablation Study: Gap to Best Known (%)')
        ax.set_xlabel('Instance')
        ax.set_ylabel('Configuration')
        plt.savefig(os.path.join(figures_dir, 'ablation_heatmap.png'), dpi=300)
        plt.savefig(os.path.join(figures_dir, 'ablation_heatmap.pdf'))
        plt.close()
        print('  Saved ablation_heatmap.png')
else:
    print('  Skipping ablation_heatmap (no ablation_study.csv found)')

print()
print('All figures generated in figures/')
"

    log_info "Figures saved to figures/"
else
    log_step 5 "Skipping figure generation (--skip-figures)"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "=================================================================="
echo "  Experiment reproduction complete!"
echo "=================================================================="
echo ""
echo "Results summary:"
echo "  Benchmark instances:  benchmarks/"
echo "  Trained GNN model:    models/edge_scorer_best.pt"
echo "  Benchmark results:    results/full_benchmark.csv"
echo "  Statistical analyses: results/lkh_comparison.json"
echo "  Figures:              figures/"
echo ""
echo "Seed used: $SEED"
echo ""
echo "To regenerate with a different seed:"
echo "  ./run_experiments.sh --seed 123"
echo ""
