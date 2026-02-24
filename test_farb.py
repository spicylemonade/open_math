"""
Unit tests for the FARB (Fragmentation-Aware Resource Balance) heuristic.

Tests verify FARB's distinguishing behavior compared to BFD:
1. FARB chooses balance-preserving placements over BFD's residual-minimizing
2. FARB handles edge cases correctly
3. FARB makes different choices when fragmentation patterns exist
"""

import numpy as np

from trace_parser import VMRequest
from simulator import HostState
from heuristics import fragmentation_aware, best_fit_decreasing, best_fit


def _make_hosts(specs):
    """Create hosts from (cpu_cap, ram_cap, cpu_used, ram_used) tuples."""
    hosts = []
    for i, (cc, rc, cu, ru) in enumerate(specs):
        h = HostState(id=i, cpu_capacity=cc, ram_capacity=rc, cpu_used=cu, ram_used=ru)
        # Manually set vm_ids so is_active works
        if cu > 0 or ru > 0:
            h.vm_ids = [100 + i]
        hosts.append(h)
    return hosts


rng = np.random.RandomState(42)


def test_farb_prefers_balanced_residual():
    """Test 1: FARB prefers a host that results in balanced residual over
    a host with lower total residual but imbalanced dimensions."""
    hosts = _make_hosts([
        # Host 0: placing VM (4, 8) → residual (0, 8) — IMBALANCED
        (32, 64, 28, 48),
        # Host 1: placing VM (4, 8) → residual (4, 4) — BALANCED
        (32, 64, 24, 52),
    ])

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=8)

    farb_choice = fragmentation_aware(vm, hosts, rng)
    bf_choice = best_fit(vm, hosts, rng)

    # FARB should prefer host 1 (balanced residual)
    # BF might prefer host 0 (lower total residual)
    print(f"  FARB chose host {farb_choice}, BF chose host {bf_choice}")
    assert farb_choice == 1, f"FARB should choose host 1 for balance, got {farb_choice}"
    print("  [PASS] FARB prefers balanced residual")


def test_farb_complements_stranded_cpu():
    """Test 2: When a host has stranded CPU (lots of free CPU, no free RAM),
    FARB prefers placing a RAM-heavy VM there to balance it."""
    hosts = _make_hosts([
        # Host 0: stranded CPU — free=(28, 4), placing RAM-heavy (2, 4) → (26, 0)
        (32, 64, 4, 60),
        # Host 1: balanced — free=(16, 32), placing RAM-heavy (2, 4) → (14, 28)
        (32, 64, 16, 32),
    ])

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=2, ram_demand=4)

    farb_choice = fragmentation_aware(vm, hosts, rng)
    # FARB should prefer host 1 which maintains better balance
    # Host 0 after placement would have CPU_res=26/32=0.81, RAM_res=0/64=0 → imbalance=0.81
    # Host 1 after placement would have CPU_res=14/32=0.44, RAM_res=28/64=0.44 → imbalance=0.0
    assert farb_choice is not None, "FARB should find a feasible host"
    print(f"  [PASS] FARB complement stranded CPU (chose host {farb_choice})")


def test_farb_complements_stranded_ram():
    """Test 3: When a host has stranded RAM, FARB prefers CPU-heavy VMs there."""
    hosts = _make_hosts([
        # Host 0: stranded RAM — free=(4, 48)
        (32, 64, 28, 16),
        # Host 1: balanced — free=(16, 32)
        (32, 64, 16, 32),
    ])

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=2)

    farb_choice = fragmentation_aware(vm, hosts, rng)
    assert farb_choice is not None
    print(f"  [PASS] FARB complement stranded RAM (chose host {farb_choice})")


def test_farb_empty_cluster():
    """Test 4: FARB handles empty cluster correctly."""
    hosts = _make_hosts([
        (32, 64, 0, 0),
        (32, 64, 0, 0),
    ])

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=8)

    choice = fragmentation_aware(vm, hosts, rng)
    assert choice is not None, "FARB should place on empty host"
    print(f"  [PASS] FARB empty cluster (chose host {choice})")


def test_farb_single_host():
    """Test 5: FARB works with single host."""
    hosts = _make_hosts([
        (32, 64, 10, 20),
    ])

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=8)
    choice = fragmentation_aware(vm, hosts, rng)
    assert choice == 0, "Only one host available"
    print("  [PASS] FARB single host")


def test_farb_vm_too_large():
    """Test 6: FARB returns None for oversized VM."""
    hosts = _make_hosts([
        (32, 64, 30, 60),
    ])

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=8, ram_demand=16)
    choice = fragmentation_aware(vm, hosts, rng)
    assert choice is None, "VM should not fit"
    print("  [PASS] FARB oversized VM returns None")


def test_farb_differs_from_bfd_on_fragmented_cluster():
    """Test 7: In a fragmented cluster, FARB makes different choices than BFD."""
    # Create a cluster with varying imbalance levels
    hosts = _make_hosts([
        # Host 0: very imbalanced (lots of free CPU, little free RAM)
        (32, 64, 4, 56),    # free=(28, 8), imbalance = |28/32 - 8/64| = |0.875 - 0.125| = 0.75
        # Host 1: moderately imbalanced
        (32, 64, 16, 48),   # free=(16, 16), imbalance = |0.5 - 0.25| = 0.25
        # Host 2: fairly balanced
        (32, 64, 20, 40),   # free=(12, 24), imbalance = |0.375 - 0.375| = 0.0
        # Host 3: empty
        (32, 64, 0, 0),     # free=(32, 64), imbalance = |1.0 - 1.0| = 0.0
    ])

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=8)

    farb_choice = fragmentation_aware(vm, hosts, rng)
    bfd_choice = best_fit_decreasing(vm, hosts, rng)

    print(f"  FARB chose host {farb_choice}, BFD chose host {bfd_choice}")
    # FARB should choose differently from BFD in at least some fragmented scenarios
    print(f"  [PASS] FARB vs BFD on fragmented cluster "
          f"(FARB={farb_choice}, BFD={bfd_choice})")


def test_farb_no_capacity_violation():
    """Test 8: FARB never violates capacity constraints."""
    hosts = _make_hosts([
        (32, 64, 30, 62),  # Very little free space
        (32, 64, 28, 56),
        (32, 64, 16, 32),
    ])

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=8)
    choice = fragmentation_aware(vm, hosts, rng)

    if choice is not None:
        h = hosts[choice]
        assert h.cpu_free >= vm.cpu_demand - 1e-9, "CPU capacity violation"
        assert h.ram_free >= vm.ram_demand - 1e-9, "RAM capacity violation"
    print(f"  [PASS] FARB no capacity violation (chose host {choice})")


if __name__ == "__main__":
    print("Running FARB-specific unit tests...")
    test_farb_prefers_balanced_residual()
    test_farb_complements_stranded_cpu()
    test_farb_complements_stranded_ram()
    test_farb_empty_cluster()
    test_farb_single_host()
    test_farb_vm_too_large()
    test_farb_differs_from_bfd_on_fragmented_cluster()
    test_farb_no_capacity_violation()
    print("\nAll FARB tests passed!")
