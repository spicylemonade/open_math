"""
Run advanced heuristics (DotProduct, L2, Harmonic2D) plus
the novel FARB and AdaptiveHybrid on both traces.

Also produces fragmentation analysis for item_012.
"""

import json
import os
import time

import numpy as np

from trace_parser import generate_google_like_trace, generate_azure_like_trace
from simulator import Simulator
from heuristics import HEURISTICS
from metrics import compute_detailed_metrics, save_summary_json, save_timeseries_csv, format_comparison_table


def run_advanced():
    """Run advanced heuristics on both traces."""
    results_dir = "results/advanced_baselines"
    os.makedirs(results_dir, exist_ok=True)

    print("Generating traces...")
    google_trace = generate_google_like_trace(n_vms=100000, n_hosts=12000, seed=42)
    azure_trace = generate_azure_like_trace(n_vms=50000, n_hosts=1000, seed=42)

    traces = {
        'google_like': google_trace,
        'azure_like': azure_trace,
    }

    advanced_heuristics = ['DotProduct', 'L2', 'Harmonic2D', 'FARB', 'AdaptiveHybrid']
    seeds = [42, 123, 456]

    all_summaries = []

    for trace_name, trace in traces.items():
        print(f"\n{'='*60}")
        print(f"Running on {trace_name} ({len(trace.vms)} VMs, {len(trace.hosts)} hosts)")
        print(f"{'='*60}")

        for hname in advanced_heuristics:
            heuristic = HEURISTICS[hname]

            for seed in seeds:
                print(f"\n  {hname} (seed={seed})...", end=" ", flush=True)
                start = time.time()

                sim = Simulator(trace.hosts, heuristic, seed=seed)
                history = sim.run(trace.vms, collect_interval=500)
                elapsed = time.time() - start

                summary = compute_detailed_metrics(
                    history, hname, trace_name, seed, elapsed)
                all_summaries.append(summary)

                prefix = f"{results_dir}/{trace_name}_{hname}_seed{seed}"
                save_summary_json(summary, f"{prefix}_summary.json")
                save_timeseries_csv(history, f"{prefix}_timeseries.csv")

                print(f"util={summary.avg_host_utilization*100:.1f}%, "
                      f"waste={summary.avg_waste_pct:.1f}%, "
                      f"frag={summary.avg_fragmentation_index*100:.1f}%, "
                      f"hosts={summary.avg_active_hosts:.0f}, "
                      f"time={elapsed:.1f}s")

    # Print comparison
    print(f"\n{'='*60}")
    print("ADVANCED HEURISTICS SUMMARY")
    print(f"{'='*60}")
    print(format_comparison_table(all_summaries))

    # Load baseline results for comparison
    baseline_dir = "results/baselines"
    baseline_agg_path = f"{baseline_dir}/baseline_aggregate.json"
    if os.path.exists(baseline_agg_path):
        with open(baseline_agg_path) as f:
            baseline_agg = json.load(f)

        print(f"\n{'='*60}")
        print("COMPARISON: ADVANCED vs BEST BASELINE (BFD)")
        print(f"{'='*60}")

        for trace_name in traces:
            bfd_key = f"BFD_{trace_name}"
            if bfd_key in baseline_agg:
                bfd_waste = baseline_agg[bfd_key]['avg_waste_pct']
                bfd_util = baseline_agg[bfd_key]['avg_utilization']

                for hname in advanced_heuristics:
                    heuristic_summaries = [s for s in all_summaries
                                           if s.heuristic == hname and s.trace == trace_name]
                    if heuristic_summaries:
                        avg_waste = np.mean([s.avg_waste_pct for s in heuristic_summaries])
                        avg_util = np.mean([s.avg_host_utilization for s in heuristic_summaries])
                        improvement = bfd_waste - avg_waste

                        print(f"  {hname} on {trace_name}: "
                              f"waste={avg_waste:.2f}% (BFD={bfd_waste:.2f}%), "
                              f"improvement={improvement:+.2f}pp, "
                              f"util={avg_util*100:.1f}% (BFD={bfd_util*100:.1f}%)")

    # Save aggregate
    agg = {}
    for s in all_summaries:
        key = f"{s.heuristic}_{s.trace}"
        if key not in agg:
            agg[key] = []
        agg[key].append(s)

    agg_results = {}
    for key, summaries in agg.items():
        agg_results[key] = {
            'heuristic': summaries[0].heuristic,
            'trace': summaries[0].trace,
            'avg_utilization': float(np.mean([s.avg_host_utilization for s in summaries])),
            'std_utilization': float(np.std([s.avg_host_utilization for s in summaries])),
            'avg_waste_pct': float(np.mean([s.avg_waste_pct for s in summaries])),
            'std_waste_pct': float(np.std([s.avg_waste_pct for s in summaries])),
            'avg_fragmentation': float(np.mean([s.avg_fragmentation_index for s in summaries])),
            'avg_active_hosts': float(np.mean([s.avg_active_hosts for s in summaries])),
        }

    with open(f"{results_dir}/advanced_aggregate.json", 'w') as f:
        json.dump(agg_results, f, indent=2)

    print(f"\nResults saved to {results_dir}/")
    return all_summaries


if __name__ == "__main__":
    run_advanced()
