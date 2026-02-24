"""
Comprehensive experiment runner for all phases.

Runs: advanced heuristics, parameter sweep, defragmentation evaluation,
fragmentation analysis, full evaluation on both traces, scalability,
and sensitivity analysis.
"""

import json
import os
import time
import csv
import signal

import numpy as np
import pandas as pd

from trace_parser import (generate_google_like_trace, generate_azure_like_trace,
                          generate_synthetic_trace, TraceData)
from simulator import Simulator, SimMetricsSnapshot
from heuristics import HEURISTICS, make_adaptive_hybrid
from metrics import (compute_detailed_metrics, save_summary_json,
                     save_timeseries_csv, format_comparison_table, MetricsSummary)
from defragmentation import defragmentation_pass


class ComputeTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise ComputeTimeout()


def run_single_experiment(trace, heuristic_func, heuristic_name, trace_name,
                          seed=42, collect_interval=500, timeout_sec=300):
    """Run a single experiment with timeout protection."""
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_sec)

    try:
        start = time.time()
        sim = Simulator(trace.hosts, heuristic_func, seed=seed)
        history = sim.run(trace.vms, collect_interval=collect_interval)
        elapsed = time.time() - start
        signal.alarm(0)

        summary = compute_detailed_metrics(history, heuristic_name, trace_name, seed, elapsed)
        return summary, history, sim
    except ComputeTimeout:
        signal.alarm(0)
        print(f" TIMEOUT after {timeout_sec}s")
        return None, None, None


def run_parameter_sweep():
    """Item 015: Parameter sweep for adaptive hybrid."""
    print("\n" + "=" * 60)
    print("PARAMETER SWEEP: Adaptive Hybrid Thresholds")
    print("=" * 60)

    results_dir = "results/parameter_sweep"
    os.makedirs(results_dir, exist_ok=True)

    trace = generate_azure_like_trace(n_vms=20000, n_hosts=500, seed=42)

    configs = [
        (0.5, 0.1), (0.5, 0.2), (0.5, 0.3),
        (0.6, 0.1), (0.6, 0.2), (0.6, 0.3),
        (0.7, 0.1), (0.7, 0.2), (0.7, 0.3),
        (0.8, 0.15), (0.8, 0.25),
        (0.9, 0.1),
    ]

    results = []
    for util_t, frag_t in configs:
        policy = make_adaptive_hybrid(util_t, frag_t)
        name = f"AH_u{util_t}_f{frag_t}"
        print(f"  {name}...", end=" ", flush=True)

        summary, _, _ = run_single_experiment(
            trace, policy, name, "azure_like_small", seed=42, timeout_sec=120)

        if summary:
            results.append({
                'util_threshold': util_t,
                'frag_threshold': frag_t,
                'waste_pct': summary.avg_waste_pct,
                'utilization': summary.avg_host_utilization,
                'fragmentation': summary.avg_fragmentation_index,
                'active_hosts': summary.avg_active_hosts,
            })
            print(f"waste={summary.avg_waste_pct:.2f}%, "
                  f"frag={summary.avg_fragmentation_index*100:.1f}%")

    with open(f"{results_dir}/sweep_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    # Find best config
    if results:
        best = min(results, key=lambda r: r['waste_pct'])
        print(f"\nBest config: util_t={best['util_threshold']}, "
              f"frag_t={best['frag_threshold']}, waste={best['waste_pct']:.2f}%")
    return results


def run_defrag_evaluation():
    """Item 016: Evaluate defragmentation benefit."""
    print("\n" + "=" * 60)
    print("DEFRAGMENTATION EVALUATION")
    print("=" * 60)

    results_dir = "results/defrag"
    os.makedirs(results_dir, exist_ok=True)

    trace = generate_azure_like_trace(n_vms=20000, n_hosts=500, seed=42)

    heuristics_to_test = ['BFD', 'FARB', 'DotProduct']
    defrag_intervals = [500, 1000, 2000]  # Events between defrag passes
    max_migrations = [5, 10, 20]

    results = []

    for hname in heuristics_to_test:
        # Run without defrag first
        summary_no_defrag, _, _ = run_single_experiment(
            trace, HEURISTICS[hname], hname, "azure_defrag", seed=42, timeout_sec=120)

        if summary_no_defrag:
            results.append({
                'heuristic': hname,
                'defrag': 'none',
                'interval': 0,
                'max_migrations': 0,
                'waste_pct': summary_no_defrag.avg_waste_pct,
                'fragmentation': summary_no_defrag.avg_fragmentation_index,
                'active_hosts': summary_no_defrag.avg_active_hosts,
            })
            print(f"  {hname} (no defrag): waste={summary_no_defrag.avg_waste_pct:.2f}%")

        # Run with defrag at different intervals
        for interval in defrag_intervals:
            for max_mig in max_migrations:
                print(f"  {hname} + defrag(interval={interval}, max_mig={max_mig})...",
                      end=" ", flush=True)

                try:
                    start = time.time()
                    sim = Simulator(trace.hosts, HEURISTICS[hname], seed=42)

                    # Custom run loop with periodic defrag
                    from simulator import SimEvent
                    events = []
                    for vm in trace.vms:
                        events.append(SimEvent(time=vm.arrival_time, event_type="arrive", vm=vm))
                        events.append(SimEvent(time=vm.departure_time, event_type="depart", vm=vm))
                    events.sort(key=lambda e: (e.time, 0 if e.event_type == "depart" else 1))

                    event_count = 0
                    total_freed = 0
                    total_migrated = 0

                    for event in events:
                        if event.event_type == "arrive":
                            sim._handle_arrival(event.vm)
                        else:
                            sim._handle_departure(event.vm)

                        event_count += 1
                        if event_count % interval == 0:
                            freed, migrated = defragmentation_pass(
                                sim.host_states, sim.vm_to_host, sim.active_vms,
                                max_migrations=max_mig, rng=sim.rng)
                            total_freed += freed
                            total_migrated += migrated
                            # Update active host set
                            sim._active_host_ids = {h.id for h in sim.host_states if h.is_active}

                        if event_count % 500 == 0:
                            snapshot = sim._compute_metrics(event.time)
                            sim.metrics_history.append(snapshot)

                    elapsed = time.time() - start
                    summary = compute_detailed_metrics(
                        sim.metrics_history, f"{hname}+defrag", "azure_defrag", 42, elapsed)

                    results.append({
                        'heuristic': hname,
                        'defrag': 'yes',
                        'interval': interval,
                        'max_migrations': max_mig,
                        'waste_pct': summary.avg_waste_pct,
                        'fragmentation': summary.avg_fragmentation_index,
                        'active_hosts': summary.avg_active_hosts,
                        'hosts_freed': total_freed,
                        'total_migrations': total_migrated,
                    })
                    print(f"waste={summary.avg_waste_pct:.2f}%, "
                          f"freed={total_freed}, migrated={total_migrated}")

                except Exception as e:
                    print(f"ERROR: {e}")
                    continue

    with open(f"{results_dir}/defrag_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    return results


def run_full_evaluation(trace_name, trace, output_dir, seeds=[42, 123, 456]):
    """Run all heuristics on a trace (items 017, 018)."""
    print(f"\n{'='*60}")
    print(f"FULL EVALUATION: {trace_name} ({len(trace.vms)} VMs)")
    print(f"{'='*60}")

    os.makedirs(output_dir, exist_ok=True)

    all_heuristics = ['FF', 'BF', 'FFD', 'BFD', 'DotProduct', 'L2',
                       'Harmonic2D', 'FARB', 'AdaptiveHybrid']

    all_summaries = []
    all_rows = []

    for hname in all_heuristics:
        heuristic = HEURISTICS[hname]
        for seed in seeds:
            print(f"  {hname} (seed={seed})...", end=" ", flush=True)
            summary, history, _ = run_single_experiment(
                trace, heuristic, hname, trace_name, seed=seed, timeout_sec=300)

            if summary:
                all_summaries.append(summary)
                all_rows.append({
                    'heuristic': hname,
                    'seed': seed,
                    'utilization': summary.avg_host_utilization,
                    'waste_pct': summary.avg_waste_pct,
                    'fragmentation': summary.avg_fragmentation_index,
                    'active_hosts': summary.avg_active_hosts,
                    'afr': summary.allocation_failure_rate,
                })

                save_summary_json(summary, f"{output_dir}/{hname}_seed{seed}_summary.json")
                if history:
                    save_timeseries_csv(history, f"{output_dir}/{hname}_seed{seed}_timeseries.csv")

                print(f"waste={summary.avg_waste_pct:.2f}%, "
                      f"util={summary.avg_host_utilization*100:.1f}%")
            else:
                print("FAILED")

    # Save as CSV
    if all_rows:
        df = pd.DataFrame(all_rows)
        df.to_csv(f"{output_dir}/all_results.csv", index=False)

    # Print summary
    print(f"\n{format_comparison_table(all_summaries)}")
    return all_summaries


def run_scalability_experiments():
    """Item 020: Scalability analysis."""
    print(f"\n{'='*60}")
    print("SCALABILITY ANALYSIS")
    print(f"{'='*60}")

    results_dir = "results/scalability"
    os.makedirs(results_dir, exist_ok=True)

    host_sizes = [100, 500, 1000, 5000]
    load_factors = [0.5, 0.7, 0.85, 0.95]
    heuristics_to_test = ['BFD', 'FARB', 'DotProduct', 'L2']

    results = []

    for n_hosts in host_sizes:
        for load_factor in load_factors:
            n_vms = int(n_hosts * 10 * load_factor)
            print(f"\n  Hosts={n_hosts}, VMs={n_vms}, Load={load_factor}")

            trace = generate_azure_like_trace(
                n_vms=n_vms, n_hosts=n_hosts, seed=42)

            for hname in heuristics_to_test:
                print(f"    {hname}...", end=" ", flush=True)
                start = time.time()

                summary, history, _ = run_single_experiment(
                    trace, HEURISTICS[hname], hname,
                    f"scale_{n_hosts}_{load_factor}",
                    seed=42, timeout_sec=120)

                elapsed = time.time() - start

                if summary:
                    time_per_alloc = elapsed / max(1, summary.total_allocations) * 1000  # ms
                    results.append({
                        'n_hosts': n_hosts,
                        'n_vms': n_vms,
                        'load_factor': load_factor,
                        'heuristic': hname,
                        'waste_pct': summary.avg_waste_pct,
                        'utilization': summary.avg_host_utilization,
                        'time_per_alloc_ms': time_per_alloc,
                        'wall_clock_s': elapsed,
                    })
                    print(f"waste={summary.avg_waste_pct:.2f}%, "
                          f"{time_per_alloc:.3f}ms/alloc")

    with open(f"{results_dir}/scalability_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    df = pd.DataFrame(results)
    df.to_csv(f"{results_dir}/scalability_results.csv", index=False)

    return results


def run_sensitivity_analysis():
    """Item 021: Sensitivity to VM size distribution."""
    print(f"\n{'='*60}")
    print("SENSITIVITY ANALYSIS")
    print(f"{'='*60}")

    results_dir = "results/sensitivity"
    os.makedirs(results_dir, exist_ok=True)

    distributions = ['cpu_heavy', 'ram_heavy', 'uniform_small', 'bimodal', 'realistic']
    heuristics_to_test = ['FF', 'BFD', 'DotProduct', 'L2', 'FARB', 'AdaptiveHybrid']
    n_vms = 50000
    n_hosts = 500

    results = []

    for dist in distributions:
        print(f"\n  Distribution: {dist}")
        trace = generate_synthetic_trace(
            n_vms=n_vms, n_hosts=n_hosts, seed=42,
            vm_size_dist=dist, host_cpu=64, host_ram=256)

        for hname in heuristics_to_test:
            print(f"    {hname}...", end=" ", flush=True)

            summary, _, _ = run_single_experiment(
                trace, HEURISTICS[hname], hname,
                f"sensitivity_{dist}", seed=42, timeout_sec=120)

            if summary:
                results.append({
                    'distribution': dist,
                    'heuristic': hname,
                    'waste_pct': summary.avg_waste_pct,
                    'utilization': summary.avg_host_utilization,
                    'fragmentation': summary.avg_fragmentation_index,
                    'active_hosts': summary.avg_active_hosts,
                })
                print(f"waste={summary.avg_waste_pct:.2f}%, "
                      f"frag={summary.avg_fragmentation_index*100:.1f}%")

    with open(f"{results_dir}/sensitivity_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    df = pd.DataFrame(results)
    df.to_csv(f"{results_dir}/sensitivity_results.csv", index=False)

    return results


def main():
    """Run all experiments."""
    print("=" * 60)
    print("COMPREHENSIVE EXPERIMENT SUITE")
    print("=" * 60)

    # Phase 3: Parameter sweep and defragmentation
    sweep_results = run_parameter_sweep()
    defrag_results = run_defrag_evaluation()

    # Phase 4: Full evaluation on both traces
    google_trace = generate_google_like_trace(n_vms=100000, n_hosts=12000, seed=42)
    azure_trace = generate_azure_like_trace(n_vms=50000, n_hosts=1000, seed=42)

    google_summaries = run_full_evaluation(
        "google_like", google_trace, "results/google_trace")
    azure_summaries = run_full_evaluation(
        "azure_like", azure_trace, "results/azure_trace")

    # Scalability and sensitivity
    scale_results = run_scalability_experiments()
    sensitivity_results = run_sensitivity_analysis()

    print("\n" + "=" * 60)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
