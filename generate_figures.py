"""
Generate all publication-quality figures for the research report.

Covers rubric items 012 (fragmentation analysis) and 023 (publication figures).
Produces 8+ figures saved as PNG in figures/ directory.
"""

import json
import os
import glob
import csv

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Publication style
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 9,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)


def load_trace_summaries(trace_dir):
    """Load per-heuristic, per-seed summaries from a trace results directory."""
    results = {}
    for f in sorted(glob.glob(os.path.join(trace_dir, '*_summary.json'))):
        with open(f) as fh:
            d = json.load(fh)
        name = os.path.basename(f).replace('_summary.json', '')
        heur = name.rsplit('_seed', 1)[0]
        if heur not in results:
            results[heur] = []
        results[heur].append(d)
    return results


def load_timeseries(trace_dir, heuristic, seed=42):
    """Load timeseries CSV for a specific heuristic and seed."""
    path = f"{trace_dir}/{heuristic}_seed{seed}_timeseries.csv"
    if not os.path.exists(path):
        return None
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({k: float(v) for k, v in row.items()})
    return rows


# ============================================================
# Figure 1: Bar chart - Resource Waste % across heuristics
# ============================================================
def fig1_waste_comparison():
    """Bar chart comparing resource waste % across all heuristics on each trace."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    heur_order = ['FF', 'FFD', 'BF', 'BFD', 'DotProduct', 'L2', 'Harmonic2D', 'FARB', 'AdaptiveHybrid']
    heur_labels = ['FF', 'FFD', 'BF', 'BFD', 'DotProd', 'L2', 'Harm2D', 'FARB\n(ours)', 'Adaptive\n(ours)']
    colors = ['#bdc3c7', '#95a5a6', '#7f8c8d', '#2c3e50',
              '#3498db', '#2980b9', '#1abc9c',
              '#e74c3c', '#e67e22']

    for ax, (trace_name, trace_dir, title) in zip(axes, [
        ('azure', 'results/azure_trace', 'Azure-like Trace (50K VMs)'),
        ('google', 'results/google_trace', 'Google-like Trace (100K VMs)')
    ]):
        results = load_trace_summaries(trace_dir)
        means = []
        stds = []
        for h in heur_order:
            if h in results:
                wastes = [r['avg_waste_pct'] for r in results[h]]
                means.append(np.mean(wastes))
                stds.append(np.std(wastes))
            else:
                means.append(0)
                stds.append(0)

        x = np.arange(len(heur_order))
        bars = ax.bar(x, means, yerr=stds, capsize=3, color=colors, edgecolor='white', linewidth=0.5)

        # Highlight FARB bar
        bars[7].set_edgecolor('#c0392b')
        bars[7].set_linewidth(2)
        bars[8].set_edgecolor('#d35400')
        bars[8].set_linewidth(2)

        ax.set_xticks(x)
        ax.set_xticklabels(heur_labels, rotation=0)
        ax.set_ylabel('Resource Waste (%)')
        ax.set_title(title)
        ax.set_ylim(0, max(means) * 1.3)

        # Add value labels on bars
        for bar, m in zip(bars, means):
            if m > 0:
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.15,
                       f'{m:.1f}', ha='center', va='bottom', fontsize=8)

    plt.suptitle('Resource Waste Comparison Across Heuristics', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig1_waste_comparison.png')
    plt.close()
    print("  [DONE] fig1_waste_comparison.png")


# ============================================================
# Figure 2: Fragmentation index time-series
# ============================================================
def fig2_fragmentation_timeseries():
    """Time-series plot of fragmentation index for top heuristics."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    heuristics_to_plot = ['BFD', 'DotProduct', 'FARB', 'AdaptiveHybrid']
    colors = {'BFD': '#2c3e50', 'DotProduct': '#3498db', 'FARB': '#e74c3c', 'AdaptiveHybrid': '#e67e22'}
    styles = {'BFD': '-', 'DotProduct': '--', 'FARB': '-', 'AdaptiveHybrid': '-.'}

    for ax, (trace_dir, title) in zip(axes, [
        ('results/azure_trace', 'Azure-like Trace'),
        ('results/google_trace', 'Google-like Trace')
    ]):
        for h in heuristics_to_plot:
            ts = load_timeseries(trace_dir, h, seed=42)
            if ts:
                times = [r['time'] for r in ts]
                frags = [r['fragmentation_index'] * 100 for r in ts]
                # Smooth with rolling average
                window = max(1, len(frags) // 50)
                frags_smooth = np.convolve(frags, np.ones(window)/window, mode='valid')
                times_smooth = times[:len(frags_smooth)]
                label = 'FARB (ours)' if h == 'FARB' else ('Adaptive (ours)' if h == 'AdaptiveHybrid' else h)
                ax.plot(times_smooth, frags_smooth, label=label,
                       color=colors[h], linestyle=styles[h], linewidth=1.5)

        ax.set_xlabel('Simulation Time')
        ax.set_ylabel('Fragmentation Index (%)')
        ax.set_title(title)
        ax.legend(loc='upper right')

    plt.suptitle('Fragmentation Index Over Time', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig2_fragmentation_timeseries.png')
    plt.close()
    print("  [DONE] fig2_fragmentation_timeseries.png")


# ============================================================
# Figure 3: Host Utilization Heatmap (CPU vs RAM)
# ============================================================
def fig3_utilization_heatmap():
    """Heatmap of host CPU utilization vs RAM utilization showing fragmentation patterns."""
    from trace_parser import generate_azure_like_trace
    from simulator import Simulator
    from heuristics import HEURISTICS

    trace = generate_azure_like_trace(n_vms=20000, n_hosts=500, seed=42)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, hname in zip(axes, ['BFD', 'FARB']):
        sim = Simulator(trace.hosts, HEURISTICS[hname], seed=42)
        sim.run(trace.vms, collect_interval=500)

        # Collect host utilizations at a mid-point
        cpu_utils = []
        ram_utils = []
        for h in sim.host_states:
            if h.is_active:
                cpu_utils.append(h.cpu_used / h.cpu_capacity * 100)
                ram_utils.append(h.ram_used / h.ram_capacity * 100)

        # 2D histogram
        bins = np.linspace(0, 100, 21)
        hist, xedges, yedges = np.histogram2d(cpu_utils, ram_utils, bins=bins)
        im = ax.pcolormesh(xedges, yedges, hist.T, cmap='YlOrRd', shading='auto')
        plt.colorbar(im, ax=ax, label='Number of Hosts')

        # Plot diagonal (balanced line)
        ax.plot([0, 100], [0, 100], 'k--', alpha=0.5, linewidth=1, label='Balanced')

        title = 'FARB (ours)' if hname == 'FARB' else hname
        ax.set_xlabel('CPU Utilization (%)')
        ax.set_ylabel('RAM Utilization (%)')
        ax.set_title(f'{title} — Host Resource Usage')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.legend(loc='lower right')

    plt.suptitle('Host CPU vs RAM Utilization (Fragmentation Patterns)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig3_utilization_heatmap.png')
    plt.close()
    print("  [DONE] fig3_utilization_heatmap.png")


# ============================================================
# Figure 4: Scalability Plot
# ============================================================
def fig4_scalability():
    """Scaling plot of allocation time vs cluster size."""
    with open('results/scalability/scalability_results.json') as f:
        data = json.load(f)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    heuristics = ['BFD', 'FARB', 'DotProduct', 'L2']
    colors = {'BFD': '#2c3e50', 'FARB': '#e74c3c', 'DotProduct': '#3498db', 'L2': '#2980b9'}
    markers = {'BFD': 's', 'FARB': 'o', 'DotProduct': '^', 'L2': 'D'}

    # Left: time per allocation vs hosts
    ax = axes[0]
    for hname in heuristics:
        hdata = [d for d in data if d['heuristic'] == hname and d['load_factor'] == 0.95]
        if hdata:
            hosts = [d['n_hosts'] for d in hdata]
            times = [d['time_per_alloc_ms'] for d in hdata]
            label = 'FARB (ours)' if hname == 'FARB' else hname
            ax.plot(hosts, times, marker=markers[hname], label=label,
                   color=colors[hname], linewidth=2, markersize=6)

    ax.set_xlabel('Number of Hosts')
    ax.set_ylabel('Time per Allocation (ms)')
    ax.set_title('Allocation Latency vs Cluster Size')
    ax.legend()
    ax.axhline(y=10, color='gray', linestyle=':', alpha=0.5, label='10ms threshold')

    # Right: waste vs hosts at load 0.95
    ax = axes[1]
    for hname in heuristics:
        hdata = [d for d in data if d['heuristic'] == hname and d['load_factor'] == 0.95]
        if hdata:
            hosts = [d['n_hosts'] for d in hdata]
            waste = [d['waste_pct'] for d in hdata]
            label = 'FARB (ours)' if hname == 'FARB' else hname
            ax.plot(hosts, waste, marker=markers[hname], label=label,
                   color=colors[hname], linewidth=2, markersize=6)

    ax.set_xlabel('Number of Hosts')
    ax.set_ylabel('Resource Waste (%)')
    ax.set_title('Resource Waste vs Cluster Size (Load=0.95)')
    ax.legend()

    plt.suptitle('Scalability Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig4_scalability.png')
    plt.close()
    print("  [DONE] fig4_scalability.png")


# ============================================================
# Figure 5: Box Plot of Waste Distribution
# ============================================================
def fig5_waste_boxplot():
    """Box plot of per-window waste % distribution across seeds."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    heur_order = ['BFD', 'DotProduct', 'L2', 'FARB', 'AdaptiveHybrid']
    heur_labels = ['BFD', 'DotProd', 'L2', 'FARB\n(ours)', 'Adaptive\n(ours)']
    colors_list = ['#2c3e50', '#3498db', '#2980b9', '#e74c3c', '#e67e22']

    for ax, (trace_dir, title) in zip(axes, [
        ('results/azure_trace', 'Azure-like Trace'),
        ('results/google_trace', 'Google-like Trace')
    ]):
        all_data = []
        for h in heur_order:
            wastes = []
            for seed in [42, 123, 456]:
                ts = load_timeseries(trace_dir, h, seed=seed)
                if ts:
                    wastes.extend([r['waste_pct'] for r in ts])
            all_data.append(wastes if wastes else [0])

        bp = ax.boxplot(all_data, labels=heur_labels, patch_artist=True,
                       showfliers=False, widths=0.6)
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_ylabel('Resource Waste (%)')
        ax.set_title(title)

    plt.suptitle('Distribution of Resource Waste Across Time Windows', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig5_waste_boxplot.png')
    plt.close()
    print("  [DONE] fig5_waste_boxplot.png")


# ============================================================
# Figure 6: Sensitivity Analysis Heatmap
# ============================================================
def fig6_sensitivity():
    """Heatmap of waste % across workload distributions and heuristics."""
    sens_path = 'results/sensitivity/sensitivity_results.json'
    if not os.path.exists(sens_path):
        print("  [SKIP] fig6_sensitivity — no sensitivity results")
        return

    with open(sens_path) as f:
        data = json.load(f)

    distributions = ['cpu_heavy', 'ram_heavy', 'uniform_small', 'bimodal', 'realistic']
    heuristics = ['FF', 'BFD', 'DotProduct', 'L2', 'FARB', 'AdaptiveHybrid']
    heur_labels = ['FF', 'BFD', 'DotProd', 'L2', 'FARB\n(ours)', 'Adaptive\n(ours)']

    # Build matrix
    matrix = np.full((len(distributions), len(heuristics)), np.nan)
    for d in data:
        if d['distribution'] in distributions and d['heuristic'] in heuristics:
            i = distributions.index(d['distribution'])
            j = heuristics.index(d['heuristic'])
            matrix[i, j] = d['waste_pct']

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto')
    plt.colorbar(im, ax=ax, label='Resource Waste (%)')

    ax.set_xticks(range(len(heuristics)))
    ax.set_xticklabels(heur_labels)
    ax.set_yticks(range(len(distributions)))
    ax.set_yticklabels([d.replace('_', ' ').title() for d in distributions])

    # Add value annotations
    for i in range(len(distributions)):
        for j in range(len(heuristics)):
            if not np.isnan(matrix[i, j]):
                ax.text(j, i, f'{matrix[i,j]:.1f}', ha='center', va='center',
                       fontsize=10, fontweight='bold',
                       color='white' if matrix[i,j] > 15 else 'black')

    ax.set_title('Sensitivity Analysis: Waste % by Distribution and Heuristic',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig6_sensitivity_heatmap.png')
    plt.close()
    print("  [DONE] fig6_sensitivity_heatmap.png")


# ============================================================
# Figure 7: Defragmentation Benefit
# ============================================================
def fig7_defrag_benefit():
    """Bar chart showing defragmentation benefit per heuristic."""
    with open('results/defrag/defrag_results.json') as f:
        data = json.load(f)

    heuristics = ['BFD', 'FARB', 'DotProduct']
    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(len(heuristics))
    width = 0.15

    configs = [
        ('No defrag', 'none', 0, 0),
        ('Defrag 500/5', 'yes', 500, 5),
        ('Defrag 500/10', 'yes', 500, 10),
        ('Defrag 500/20', 'yes', 500, 20),
    ]

    colors_list = ['#2c3e50', '#3498db', '#2980b9', '#1abc9c']

    for k, (label, defrag, interval, max_mig) in enumerate(configs):
        wastes = []
        for hname in heuristics:
            matches = [d for d in data
                      if d['heuristic'] == hname
                      and d['defrag'] == defrag
                      and d['interval'] == interval
                      and d['max_migrations'] == max_mig]
            if matches:
                wastes.append(matches[0]['waste_pct'])
            else:
                wastes.append(0)

        bars = ax.bar(x + k * width, wastes, width, label=label,
                     color=colors_list[k], edgecolor='white')
        for bar, w in zip(bars, wastes):
            if w > 0:
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                       f'{w:.1f}', ha='center', va='bottom', fontsize=8)

    ax.set_xticks(x + width * 1.5)
    heur_labels = ['BFD', 'FARB (ours)', 'DotProduct']
    ax.set_xticklabels(heur_labels)
    ax.set_ylabel('Resource Waste (%)')
    ax.set_title('Impact of Defragmentation on Resource Waste', fontsize=14, fontweight='bold')
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig7_defrag_benefit.png')
    plt.close()
    print("  [DONE] fig7_defrag_benefit.png")


# ============================================================
# Figure 8: Stranded Resources Distribution (item 012)
# ============================================================
def fig8_stranded_resources():
    """Distribution of stranded resource types under BFD vs FARB."""
    from trace_parser import generate_azure_like_trace
    from simulator import Simulator
    from heuristics import HEURISTICS

    trace = generate_azure_like_trace(n_vms=20000, n_hosts=500, seed=42)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    tau = 0.1  # stranding threshold

    for ax, hname in zip(axes, ['BFD', 'FARB']):
        sim = Simulator(trace.hosts, HEURISTICS[hname], seed=42)
        sim.run(trace.vms, collect_interval=500)

        stranded_cpu = 0  # Free CPU but no RAM
        stranded_ram = 0  # Free RAM but no CPU
        balanced = 0
        empty = 0

        for h in sim.host_states:
            if not h.is_active:
                empty += 1
                continue
            cpu_frac = h.cpu_free / h.cpu_capacity
            ram_frac = h.ram_free / h.ram_capacity

            if cpu_frac > tau and ram_frac < tau:
                stranded_cpu += 1
            elif ram_frac > tau and cpu_frac < tau:
                stranded_ram += 1
            else:
                balanced += 1

        total_active = stranded_cpu + stranded_ram + balanced
        cats = ['Stranded CPU\n(free CPU, no RAM)', 'Stranded RAM\n(free RAM, no CPU)', 'Balanced']
        vals = [stranded_cpu, stranded_ram, balanced]
        colors = ['#e74c3c', '#3498db', '#2ecc71']

        bars = ax.bar(cats, vals, color=colors, edgecolor='white')
        for bar, v in zip(bars, vals):
            pct = v / total_active * 100 if total_active > 0 else 0
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                   f'{v} ({pct:.1f}%)', ha='center', va='bottom', fontsize=10)

        title_name = 'FARB (ours)' if hname == 'FARB' else hname
        ax.set_ylabel('Number of Hosts')
        ax.set_title(f'{title_name} — Active={total_active}, Empty={empty}')

    plt.suptitle('Distribution of Stranded Resource Types at End of Trace',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig8_stranded_resources.png')
    plt.close()
    print("  [DONE] fig8_stranded_resources.png")


# ============================================================
# Figure 9: VM Size Distribution & Fragmentation Correlation (item 012)
# ============================================================
def fig9_vm_size_fragmentation():
    """VM size distribution analysis and its correlation with fragmentation."""
    from trace_parser import generate_azure_like_trace

    trace = generate_azure_like_trace(n_vms=20000, n_hosts=500, seed=42)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: VM CPU/RAM ratio distribution
    ax = axes[0]
    ratios = [vm.cpu_demand / vm.ram_demand for vm in trace.vms if vm.ram_demand > 0]
    ax.hist(ratios, bins=30, color='#3498db', edgecolor='white', alpha=0.8)
    ax.set_xlabel('CPU:RAM Demand Ratio')
    ax.set_ylabel('Number of VMs')
    ax.set_title('VM Resource Ratio Distribution')
    ax.axvline(x=1.0, color='red', linestyle='--', alpha=0.5, label='Balanced (1:1)')
    ax.legend()

    # Right: Scatter of VM imbalance vs resulting host fragmentation delta
    ax = axes[1]
    # Compute VM imbalance as |cpu_frac - ram_frac| for a reference host
    ref_cpu = trace.hosts[0].cpu_capacity
    ref_ram = trace.hosts[0].ram_capacity
    imbalances = [abs(vm.cpu_demand/ref_cpu - vm.ram_demand/ref_ram) for vm in trace.vms]

    # Bin VMs by imbalance and show average fragmentation for workloads dominated by each bin
    bins_edges = np.linspace(0, max(imbalances), 11)
    bin_centers = (bins_edges[:-1] + bins_edges[1:]) / 2
    counts = np.histogram(imbalances, bins=bins_edges)[0]

    ax.bar(bin_centers, counts, width=(bins_edges[1]-bins_edges[0])*0.8,
          color='#e74c3c', edgecolor='white', alpha=0.8)
    ax.set_xlabel('VM Resource Imbalance |cpu_frac − ram_frac|')
    ax.set_ylabel('Number of VMs')
    ax.set_title('VM Resource Imbalance Distribution')

    plt.suptitle('VM Size Characteristics and Fragmentation Potential',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig9_vm_size_fragmentation.png')
    plt.close()
    print("  [DONE] fig9_vm_size_fragmentation.png")


def main():
    print("Generating publication figures...")
    print()

    # Item 023 figures
    fig1_waste_comparison()
    fig2_fragmentation_timeseries()
    fig3_utilization_heatmap()
    fig4_scalability()
    fig5_waste_boxplot()
    fig6_sensitivity()
    fig7_defrag_benefit()

    # Item 012 figures
    fig8_stranded_resources()
    fig9_vm_size_fragmentation()

    print(f"\nAll figures saved to {FIGURES_DIR}/")
    print(f"Total files: {len(os.listdir(FIGURES_DIR))}")


if __name__ == "__main__":
    main()
