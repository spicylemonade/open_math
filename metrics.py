"""
Evaluation metrics collection and reporting module.

Computes all 5 metrics defined in evaluation_metrics.md at configurable intervals.
Outputs: JSON summary files and CSV time-series files.
"""

import csv
import json
import math
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

import numpy as np

from simulator import SimMetricsSnapshot, HostState


@dataclass
class MetricsSummary:
    """Aggregate metrics for a simulation run."""
    heuristic: str
    trace: str
    seed: int
    total_allocations: int
    failed_allocations: int
    allocation_failure_rate: float
    avg_host_utilization: float
    avg_fragmentation_index: float
    avg_active_hosts: float
    max_active_hosts: int
    avg_waste_pct: float
    final_waste_pct: float
    cpu_waste_pct: float
    ram_waste_pct: float
    wall_clock_seconds: float
    events_per_second: float


def compute_detailed_metrics(
    snapshots: List[SimMetricsSnapshot],
    heuristic_name: str,
    trace_name: str,
    seed: int,
    wall_clock: float = 0.0,
) -> MetricsSummary:
    """Compute aggregate metrics from a list of snapshots."""
    if not snapshots:
        return MetricsSummary(
            heuristic=heuristic_name, trace=trace_name, seed=seed,
            total_allocations=0, failed_allocations=0, allocation_failure_rate=0,
            avg_host_utilization=0, avg_fragmentation_index=0,
            avg_active_hosts=0, max_active_hosts=0,
            avg_waste_pct=0, final_waste_pct=0,
            cpu_waste_pct=0, ram_waste_pct=0,
            wall_clock_seconds=wall_clock, events_per_second=0,
        )

    n = len(snapshots)
    final = snapshots[-1]

    total_alloc = final.total_allocations
    failed = final.failed_allocations
    afr = failed / max(1, total_alloc)

    avg_util = np.mean([s.utilization for s in snapshots])
    avg_frag = np.mean([s.fragmentation_index for s in snapshots])
    avg_active = np.mean([s.active_hosts for s in snapshots])
    max_active = max(s.active_hosts for s in snapshots)
    avg_waste = np.mean([s.waste_pct for s in snapshots])

    # Decompose CPU vs RAM waste
    cpu_wastes = []
    ram_wastes = []
    for s in snapshots:
        if s.total_cpu_capacity > 0:
            cpu_wastes.append((s.total_cpu_capacity - s.total_cpu_used) / s.total_cpu_capacity * 100)
        if s.total_ram_capacity > 0:
            ram_wastes.append((s.total_ram_capacity - s.total_ram_used) / s.total_ram_capacity * 100)

    cpu_waste = np.mean(cpu_wastes) if cpu_wastes else 0
    ram_waste = np.mean(ram_wastes) if ram_wastes else 0

    events = total_alloc * 2
    eps = events / max(0.001, wall_clock)

    return MetricsSummary(
        heuristic=heuristic_name,
        trace=trace_name,
        seed=seed,
        total_allocations=total_alloc,
        failed_allocations=failed,
        allocation_failure_rate=afr,
        avg_host_utilization=avg_util,
        avg_fragmentation_index=avg_frag,
        avg_active_hosts=avg_active,
        max_active_hosts=max_active,
        avg_waste_pct=avg_waste,
        final_waste_pct=final.waste_pct,
        cpu_waste_pct=cpu_waste,
        ram_waste_pct=ram_waste,
        wall_clock_seconds=wall_clock,
        events_per_second=eps,
    )


def save_summary_json(summary: MetricsSummary, path: str):
    """Save metrics summary as JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(asdict(summary), f, indent=2)


def save_timeseries_csv(snapshots: List[SimMetricsSnapshot], path: str):
    """Save per-interval metrics as CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'time', 'active_hosts', 'utilization', 'fragmentation_index',
            'waste_pct', 'total_cpu_used', 'total_ram_used',
            'total_cpu_capacity', 'total_ram_capacity',
            'failed_allocations', 'total_allocations',
        ])
        for s in snapshots:
            writer.writerow([
                f"{s.time:.2f}", s.active_hosts,
                f"{s.utilization:.6f}", f"{s.fragmentation_index:.6f}",
                f"{s.waste_pct:.4f}",
                f"{s.total_cpu_used:.4f}", f"{s.total_ram_used:.4f}",
                f"{s.total_cpu_capacity:.4f}", f"{s.total_ram_capacity:.4f}",
                s.failed_allocations, s.total_allocations,
            ])


def load_summary_json(path: str) -> MetricsSummary:
    """Load metrics summary from JSON."""
    with open(path, 'r') as f:
        data = json.load(f)
    return MetricsSummary(**data)


def format_comparison_table(summaries: List[MetricsSummary]) -> str:
    """Format a comparison table of multiple heuristics."""
    header = f"{'Heuristic':<20} {'Trace':<25} {'Seed':>4} {'Util%':>7} {'Waste%':>7} {'Frag%':>7} {'Hosts':>7} {'AFR%':>6}"
    lines = [header, "-" * len(header)]

    for s in summaries:
        line = (f"{s.heuristic:<20} {s.trace:<25} {s.seed:>4} "
                f"{s.avg_host_utilization*100:>6.2f}% {s.avg_waste_pct:>6.2f}% "
                f"{s.avg_fragmentation_index*100:>6.2f}% {s.avg_active_hosts:>6.1f} "
                f"{s.allocation_failure_rate*100:>5.2f}%")
        lines.append(line)

    return "\n".join(lines)


# ---- Validation test ----

def test_metrics_hand_computed():
    """Validate metrics on a hand-computed 5-host, 20-VM example.

    Setup:
    - 5 hosts, each (cpu=10, ram=20)
    - 20 VMs, each (cpu=2, ram=4) — each host fits exactly 5 VMs (5*2=10, 5*4=20)
    - So 20 VMs fill exactly 4 hosts perfectly (100% utilization on each)

    Expected metrics at steady state (all 20 VMs active):
    - Active hosts: 4
    - CPU utilization per host: 10/10 = 1.0
    - RAM utilization per host: 20/20 = 1.0
    - Host utilization: 0.5 * (1.0 + 1.0) = 1.0
    - Waste: 0%
    - Fragmentation: 0%
    - AFR: 0%
    """
    from simulator import Simulator
    from trace_parser import VMRequest, HostSpec

    hosts = [HostSpec(cpu_capacity=10, ram_capacity=20) for _ in range(5)]

    def ff(vm, host_list, rng):
        for i, h in enumerate(host_list):
            if h.can_fit(vm.cpu_demand, vm.ram_demand):
                return i
        return None

    vms = [VMRequest(id=i, arrival_time=float(i), departure_time=1000.0,
                     cpu_demand=2.0, ram_demand=4.0)
           for i in range(20)]

    sim = Simulator(hosts, ff, seed=42)
    history = sim.run(vms, collect_interval=1)

    # Find the snapshot at peak load (after all 20 arrivals, before any departures)
    # All VMs arrive at times 0..19, depart at 1000. So snapshot around event 20-39
    # should show all 20 VMs active on 5 hosts.
    peak = max(history, key=lambda s: s.active_hosts)

    # After all 20 arrivals (first 20 events), we should have 4 hosts fully packed.
    # Snapshot at index 19 (0-indexed) = after 20th arrival event.
    # With collect_interval=1, we get a snapshot after each event.
    # Events: 20 arrivals (times 0..19) then 20 departures (all at 1000).
    # Snapshot index 19 = after the 20th arrival.
    peak = history[19]  # After all 20 arrivals

    assert peak.active_hosts == 4, f"Expected 4 active hosts at peak, got {peak.active_hosts}"
    assert abs(peak.utilization - 1.0) < 0.01, f"Expected util 1.0, got {peak.utilization}"
    assert peak.waste_pct < 0.1, f"Expected waste ~0%, got {peak.waste_pct}"
    assert peak.fragmentation_index == 0.0, f"Expected frag 0, got {peak.fragmentation_index}"
    assert peak.failed_allocations == 0, f"Expected 0 failures, got {peak.failed_allocations}"

    # Compute detailed metrics (excluding post-departure snapshots)
    active_history = [s for s in history if s.active_hosts > 0]
    summary = compute_detailed_metrics(active_history, "FF", "hand_computed", 42, 0.1)
    assert summary.allocation_failure_rate == 0.0

    print(f"  [PASS] Hand-computed metrics: util={peak.utilization:.3f}, "
          f"waste={peak.waste_pct:.1f}%, frag={peak.fragmentation_index:.3f}, "
          f"hosts={peak.active_hosts}")

    # Test JSON save/load
    path = "/tmp/test_metrics.json"
    save_summary_json(summary, path)
    loaded = load_summary_json(path)
    assert abs(loaded.avg_waste_pct - summary.avg_waste_pct) < 0.01
    os.remove(path)
    print("  [PASS] JSON save/load roundtrip")

    # Test CSV output
    csv_path = "/tmp/test_timeseries.csv"
    save_timeseries_csv(history, csv_path)
    with open(csv_path) as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert len(rows) > 1, "CSV should have header + data rows"
    os.remove(csv_path)
    print("  [PASS] CSV timeseries output")


if __name__ == "__main__":
    print("Running metrics tests...")
    test_metrics_hand_computed()
    print("All metrics tests passed!")
