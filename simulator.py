"""
Discrete-event simulation framework for online VM-to-host packing.

Processes VM arrival/departure events chronologically, maintains host state,
supports pluggable placement policies, and collects per-event metrics.
"""

import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple

import numpy as np

from trace_parser import VMRequest, HostSpec, TraceData


@dataclass
class HostState:
    """Runtime state of a physical host."""
    id: int
    cpu_capacity: float
    ram_capacity: float
    cpu_used: float = 0.0
    ram_used: float = 0.0
    vm_ids: List[int] = field(default_factory=list)

    @property
    def cpu_free(self) -> float:
        return self.cpu_capacity - self.cpu_used

    @property
    def ram_free(self) -> float:
        return self.ram_capacity - self.ram_used

    @property
    def is_active(self) -> bool:
        return len(self.vm_ids) > 0

    def can_fit(self, cpu: float, ram: float) -> bool:
        return self.cpu_free >= cpu - 1e-9 and self.ram_free >= ram - 1e-9

    def allocate(self, vm: VMRequest):
        self.cpu_used += vm.cpu_demand
        self.ram_used += vm.ram_demand
        self.vm_ids.append(vm.id)

    def deallocate(self, vm: VMRequest):
        self.cpu_used -= vm.cpu_demand
        self.ram_used -= vm.ram_demand
        self.cpu_used = max(0.0, self.cpu_used)  # Avoid floating point drift
        self.ram_used = max(0.0, self.ram_used)
        if vm.id in self.vm_ids:
            self.vm_ids.remove(vm.id)


# Type alias for placement policy
PlacementPolicy = Callable[[VMRequest, List[HostState], np.random.RandomState], Optional[int]]


@dataclass
class SimEvent:
    """A simulation event."""
    time: float
    event_type: str  # "arrive" or "depart"
    vm: VMRequest


@dataclass
class SimMetricsSnapshot:
    """Metrics at a point in time."""
    time: float
    active_hosts: int
    total_cpu_used: float
    total_ram_used: float
    total_cpu_capacity: float
    total_ram_capacity: float
    utilization: float
    fragmentation_index: float
    waste_pct: float
    failed_allocations: int
    total_allocations: int


class Simulator:
    """Discrete-event simulator for online VM-to-host packing."""

    def __init__(self, hosts: List[HostSpec], policy: PlacementPolicy, seed: int = 42):
        self.host_states: List[HostState] = [
            HostState(id=i, cpu_capacity=h.cpu_capacity, ram_capacity=h.ram_capacity)
            for i, h in enumerate(hosts)
        ]
        self.policy = policy
        self.rng = np.random.RandomState(seed)

        # VM tracking
        self.vm_to_host: Dict[int, int] = {}  # vm_id -> host_id
        self.active_vms: Dict[int, VMRequest] = {}

        # Active host tracking for O(1) lookup
        self._active_host_ids: set = set()
        self._host_by_id: Dict[int, HostState] = {h.id: h for h in self.host_states}
        # Pool of empty host IDs for fast access
        self._empty_pool: List[int] = list(range(len(self.host_states)))

        # Metrics
        self.total_allocations = 0
        self.failed_allocations = 0
        self.metrics_history: List[SimMetricsSnapshot] = []

    def _compute_metrics(self, time: float) -> SimMetricsSnapshot:
        """Compute current metrics snapshot."""
        active = [self._host_by_id[hid] for hid in self._active_host_ids]
        n_active = len(active)

        if n_active == 0:
            return SimMetricsSnapshot(
                time=time, active_hosts=0,
                total_cpu_used=0, total_ram_used=0,
                total_cpu_capacity=0, total_ram_capacity=0,
                utilization=0, fragmentation_index=0, waste_pct=0,
                failed_allocations=self.failed_allocations,
                total_allocations=self.total_allocations,
            )

        total_cpu_used = sum(h.cpu_used for h in active)
        total_ram_used = sum(h.ram_used for h in active)
        total_cpu_cap = sum(h.cpu_capacity for h in active)
        total_ram_cap = sum(h.ram_capacity for h in active)

        utilization = 0.5 * (total_cpu_used / total_cpu_cap + total_ram_used / total_ram_cap) if total_cpu_cap > 0 else 0

        # Fragmentation: hosts with stranded resources
        tau = 0.1  # Stranding threshold
        stranded = 0
        for h in active:
            cpu_frac = h.cpu_free / h.cpu_capacity
            ram_frac = h.ram_free / h.ram_capacity
            if (min(cpu_frac, ram_frac) < tau and max(cpu_frac, ram_frac) > tau):
                stranded += 1
        frag_idx = stranded / n_active if n_active > 0 else 0

        # Waste percentage
        waste = ((total_cpu_cap - total_cpu_used) + (total_ram_cap - total_ram_used))
        total_cap = total_cpu_cap + total_ram_cap
        waste_pct = (waste / total_cap * 100) if total_cap > 0 else 0

        return SimMetricsSnapshot(
            time=time, active_hosts=n_active,
            total_cpu_used=total_cpu_used, total_ram_used=total_ram_used,
            total_cpu_capacity=total_cpu_cap, total_ram_capacity=total_ram_cap,
            utilization=utilization, fragmentation_index=frag_idx,
            waste_pct=waste_pct,
            failed_allocations=self.failed_allocations,
            total_allocations=self.total_allocations,
        )

    def run(self, vms: List[VMRequest], collect_interval: int = 100) -> List[SimMetricsSnapshot]:
        """Run simulation on a list of VM requests.

        Args:
            vms: List of VM requests (should be sorted by arrival_time).
            collect_interval: Collect metrics every N events.

        Returns:
            List of metrics snapshots.
        """
        # Build event list
        events = []
        for vm in vms:
            events.append(SimEvent(time=vm.arrival_time, event_type="arrive", vm=vm))
            events.append(SimEvent(time=vm.departure_time, event_type="depart", vm=vm))

        # Sort by time, with departures before arrivals at same time
        events.sort(key=lambda e: (e.time, 0 if e.event_type == "depart" else 1))

        event_count = 0
        for event in events:
            if event.event_type == "arrive":
                self._handle_arrival(event.vm)
            else:
                self._handle_departure(event.vm)

            event_count += 1
            if event_count % collect_interval == 0:
                snapshot = self._compute_metrics(event.time)
                self.metrics_history.append(snapshot)

        # Final snapshot
        if events:
            final = self._compute_metrics(events[-1].time)
            self.metrics_history.append(final)

        return self.metrics_history

    def _get_candidates(self) -> List[HostState]:
        """Return active hosts + a small pool of empty hosts."""
        candidates = [self._host_by_id[hid] for hid in self._active_host_ids]
        # Add a few empty hosts from the pool
        added = 0
        for hid in self._empty_pool:
            if hid not in self._active_host_ids:
                candidates.append(self._host_by_id[hid])
                added += 1
                if added >= 10:
                    break
        return candidates

    def _handle_arrival(self, vm: VMRequest):
        """Place a VM on a host using the policy."""
        self.total_allocations += 1
        candidates = self._get_candidates()
        idx = self.policy(vm, candidates, self.rng)

        if idx is not None and 0 <= idx < len(candidates):
            host = candidates[idx]
            if host.can_fit(vm.cpu_demand, vm.ram_demand):
                host.allocate(vm)
                self.vm_to_host[vm.id] = host.id
                self._active_host_ids.add(host.id)
                self.active_vms[vm.id] = vm
                return

        self.failed_allocations += 1

    def _handle_departure(self, vm: VMRequest):
        """Remove a VM from its host."""
        if vm.id in self.vm_to_host:
            host_id = self.vm_to_host.pop(vm.id)
            host = self._host_by_id[host_id]
            host.deallocate(vm)
            if not host.is_active:
                self._active_host_ids.discard(host_id)
            self.active_vms.pop(vm.id, None)

    def get_summary(self) -> Dict:
        """Get summary metrics."""
        if not self.metrics_history:
            return {}

        snapshots = self.metrics_history
        return {
            'total_allocations': self.total_allocations,
            'failed_allocations': self.failed_allocations,
            'allocation_failure_rate': self.failed_allocations / max(1, self.total_allocations),
            'avg_active_hosts': np.mean([s.active_hosts for s in snapshots]),
            'max_active_hosts': max(s.active_hosts for s in snapshots),
            'avg_utilization': np.mean([s.utilization for s in snapshots]),
            'avg_fragmentation': np.mean([s.fragmentation_index for s in snapshots]),
            'avg_waste_pct': np.mean([s.waste_pct for s in snapshots]),
            'final_waste_pct': snapshots[-1].waste_pct,
            'final_utilization': snapshots[-1].utilization,
            'final_active_hosts': snapshots[-1].active_hosts,
        }


def run_benchmark(trace: TraceData, policy: PlacementPolicy, seed: int = 42,
                   collect_interval: int = 100) -> Tuple[Dict, List[SimMetricsSnapshot]]:
    """Run a benchmark and return summary + history."""
    sim = Simulator(trace.hosts, policy, seed=seed)
    start = time.time()
    history = sim.run(trace.vms, collect_interval=collect_interval)
    elapsed = time.time() - start

    summary = sim.get_summary()
    summary['wall_clock_seconds'] = elapsed
    summary['events_per_second'] = (len(trace.vms) * 2) / max(0.001, elapsed)
    summary['heuristic_seed'] = seed

    return summary, history


# ---- Integration test ----

def test_simulator_basic():
    """Integration test with synthetic trace and First-Fit policy."""
    from trace_parser import generate_synthetic_trace

    def first_fit(vm: VMRequest, hosts: List[HostState], rng) -> Optional[int]:
        for i, h in enumerate(hosts):
            if h.can_fit(vm.cpu_demand, vm.ram_demand):
                return i
        return None

    trace = generate_synthetic_trace(n_vms=1000, n_hosts=100, seed=42)
    sim = Simulator(trace.hosts, first_fit, seed=42)

    start = time.time()
    history = sim.run(trace.vms, collect_interval=50)
    elapsed = time.time() - start

    summary = sim.get_summary()

    assert summary['total_allocations'] == 1000, f"Expected 1000 allocations, got {summary['total_allocations']}"
    assert len(history) > 0, "No metrics collected"
    assert summary['avg_utilization'] > 0, "Utilization should be positive"

    events_per_min = (1000 * 2) / elapsed * 60
    print(f"  [PASS] Simulator: {summary['total_allocations']} allocations, "
          f"{summary['failed_allocations']} failures, "
          f"utilization={summary['avg_utilization']:.3f}, "
          f"waste={summary['avg_waste_pct']:.1f}%")
    print(f"         Performance: {events_per_min:.0f} events/min "
          f"(requirement: >100,000)")
    assert events_per_min > 100000, f"Too slow: {events_per_min:.0f} events/min"


if __name__ == "__main__":
    print("Running simulator tests...")
    test_simulator_basic()
    print("All simulator tests passed!")
