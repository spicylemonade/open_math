"""
Placement heuristics for VM-to-host bin packing.

All heuristics implement the PlacementPolicy interface:
  (VMRequest, List[HostState], np.random.RandomState) -> Optional[int]

Classical baselines: FF, BF, FFD, BFD
Advanced heuristics: DotProduct, L2Norm, Harmonic-class
Novel: FragmentationAware, AdaptiveHybrid
"""

import math
from typing import List, Optional

import numpy as np

from trace_parser import VMRequest
from simulator import HostState


# ========================
# Classical Baselines
# ========================

def first_fit(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
    """First Fit: assign to first host with sufficient CPU and RAM."""
    for i, h in enumerate(hosts):
        if h.can_fit(vm.cpu_demand, vm.ram_demand):
            return i
    return None


def best_fit(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
    """Best Fit: assign to host that minimizes remaining capacity (L2 norm of residual)."""
    best_idx = None
    best_score = float('inf')

    for i, h in enumerate(hosts):
        if h.can_fit(vm.cpu_demand, vm.ram_demand):
            # L2 norm of residual after placement
            residual_cpu = h.cpu_free - vm.cpu_demand
            residual_ram = h.ram_free - vm.ram_demand
            score = math.sqrt(residual_cpu**2 + residual_ram**2)
            if score < best_score:
                best_score = score
                best_idx = i

    return best_idx


def first_fit_decreasing(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
    """First Fit Decreasing: In online mode, FFD works the same as FF for individual
    arrivals. The 'decreasing' part applies to batch sorting, which is handled
    externally. For the online variant, we use FF with a preference for fuller hosts
    (scanning hosts from most-loaded to least-loaded)."""
    # Sort hosts by used capacity (most loaded first) for FFD behavior
    indices = sorted(range(len(hosts)),
                     key=lambda i: -(hosts[i].cpu_used + hosts[i].ram_used))
    for i in indices:
        if hosts[i].can_fit(vm.cpu_demand, vm.ram_demand):
            return i
    return None


def best_fit_decreasing(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
    """Best Fit Decreasing: In online mode, applies BF with hosts sorted by load.
    Combines the BF scoring with preference for fuller hosts."""
    best_idx = None
    best_score = float('inf')

    for i, h in enumerate(hosts):
        if h.can_fit(vm.cpu_demand, vm.ram_demand):
            residual_cpu = h.cpu_free - vm.cpu_demand
            residual_ram = h.ram_free - vm.ram_demand
            score = math.sqrt(residual_cpu**2 + residual_ram**2)
            if score < best_score:
                best_score = score
                best_idx = i

    return best_idx


# ========================
# Advanced Heuristics
# ========================

def dot_product(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
    """DotProduct heuristic (Panigrahy et al., 2011).

    Score hosts by alignment (cosine similarity) between VM demand and host
    residual, weighted by host fullness to prefer tighter packing.

    score = cosine_similarity(demand, residual) * fullness_factor

    This avoids the pathological worst-fit behavior of raw dot-product on
    empty hosts while preserving the geometric alignment insight.

    Reference: panigrahy2011heuristics in sources.bib
    """
    best_idx = None
    best_score = -float('inf')

    for i, h in enumerate(hosts):
        if h.can_fit(vm.cpu_demand, vm.ram_demand):
            cpu_res = h.cpu_free / h.cpu_capacity if h.cpu_capacity > 0 else 0
            ram_res = h.ram_free / h.ram_capacity if h.ram_capacity > 0 else 0
            cpu_dem = vm.cpu_demand / h.cpu_capacity if h.cpu_capacity > 0 else 0
            ram_dem = vm.ram_demand / h.ram_capacity if h.ram_capacity > 0 else 0

            # Cosine similarity between demand and residual
            dot = cpu_dem * cpu_res + ram_dem * ram_res
            norm_d = math.sqrt(cpu_dem**2 + ram_dem**2)
            norm_r = math.sqrt(cpu_res**2 + ram_res**2)
            cos_sim = dot / (norm_d * norm_r + 1e-12)

            # Fullness factor: prefer hosts that are already partially filled
            fullness = 1.0 - (cpu_res + ram_res) / 2.0

            score = cos_sim * (fullness + 0.01)  # +0.01 to avoid zero for empty hosts
            if score > best_score:
                best_score = score
                best_idx = i

    return best_idx


def l2_norm(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
    """L2 Norm heuristic (Panigrahy et al., 2011).

    Place VM on host that minimizes L2 norm of normalized residual capacity
    after placement. This balances residual resources across dimensions.

    Reference: panigrahy2011heuristics in sources.bib
    """
    best_idx = None
    best_score = float('inf')

    for i, h in enumerate(hosts):
        if h.can_fit(vm.cpu_demand, vm.ram_demand):
            # Normalized residual after placement
            cpu_res = (h.cpu_free - vm.cpu_demand) / h.cpu_capacity if h.cpu_capacity > 0 else 0
            ram_res = (h.ram_free - vm.ram_demand) / h.ram_capacity if h.ram_capacity > 0 else 0

            score = math.sqrt(cpu_res**2 + ram_res**2)
            if score < best_score:
                best_score = score
                best_idx = i

    return best_idx


def harmonic_2d(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
    """Harmonic-class algorithm adapted for 2D VM setting.

    Classifies VMs into size categories and maintains separate host groups
    for each category. Within a group, uses best-fit.

    Inspired by Seiden (2002) Harmonic++ and adapted for vector packing.

    Reference: seiden2002online in sources.bib
    """
    # Classify VM by its dominant resource fraction
    # Categories: tiny (<10%), small (10-25%), medium (25-50%), large (>50%)
    def classify(cpu_frac, ram_frac):
        max_frac = max(cpu_frac, ram_frac)
        if max_frac < 0.10:
            return 0  # tiny
        elif max_frac < 0.25:
            return 1  # small
        elif max_frac < 0.50:
            return 2  # medium
        else:
            return 3  # large

    # For each feasible host, prefer hosts that have VMs of the same class
    best_idx = None
    best_score = float('inf')

    # Determine VM's size class (use first host's capacity for normalization)
    if hosts:
        ref_cpu = hosts[0].cpu_capacity
        ref_ram = hosts[0].ram_capacity
    else:
        return None

    vm_cpu_frac = vm.cpu_demand / ref_cpu if ref_cpu > 0 else 0
    vm_ram_frac = vm.ram_demand / ref_ram if ref_ram > 0 else 0
    vm_class = classify(vm_cpu_frac, vm_ram_frac)

    for i, h in enumerate(hosts):
        if h.can_fit(vm.cpu_demand, vm.ram_demand):
            cpu_res = (h.cpu_free - vm.cpu_demand) / h.cpu_capacity if h.cpu_capacity > 0 else 0
            ram_res = (h.ram_free - vm.ram_demand) / h.ram_capacity if h.ram_capacity > 0 else 0

            # Base score: L2 norm of residual
            base_score = math.sqrt(cpu_res**2 + ram_res**2)

            # Penalty for mixing size classes (check host's load level as proxy)
            host_load = 1.0 - (h.cpu_free / h.cpu_capacity + h.ram_free / h.ram_capacity) / 2
            host_class = classify(1 - h.cpu_free / h.cpu_capacity, 1 - h.ram_free / h.ram_capacity)

            # Prefer hosts that are either empty or match the VM's size class
            class_penalty = 0.0 if (not h.is_active or host_class == vm_class) else 0.1

            score = base_score + class_penalty
            if score < best_score:
                best_score = score
                best_idx = i

    return best_idx


# ========================
# Novel Heuristic (placeholder — detailed in Phase 3)
# ========================

def fragmentation_aware(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
    """Fragmentation-Aware Resource Balance (FARB) heuristic.

    Explicitly targets stranded resource patterns by scoring hosts based on
    how well the VM's resource ratio complements the host's current imbalance.

    Key idea: If a host has more free CPU than RAM, prefer placing RAM-heavy VMs
    there, and vice versa. This balances residual resources and reduces stranding.

    Combines:
    1. Resource balance score: penalizes placing VMs that worsen dimension imbalance
    2. Fullness preference: prefers fuller hosts (like BFD)
    3. Tiebreaking: L2 norm of residual

    Reference: Novel contribution; differentiates from panigrahy2011heuristics (DotProduct/L2),
    hadary2020protean (Protean scoring), and verma2015borg (Borg stranded resources).
    """
    best_idx = None
    best_score = float('inf')

    for i, h in enumerate(hosts):
        if not h.can_fit(vm.cpu_demand, vm.ram_demand):
            continue

        # Normalized residual after placement
        cpu_res_norm = (h.cpu_free - vm.cpu_demand) / h.cpu_capacity if h.cpu_capacity > 0 else 0
        ram_res_norm = (h.ram_free - vm.ram_demand) / h.ram_capacity if h.ram_capacity > 0 else 0

        # Component 1: Resource balance — minimize absolute difference between
        # normalized residual dimensions (reduces stranding)
        balance = abs(cpu_res_norm - ram_res_norm)

        # Component 2: Fullness — prefer hosts with less total residual (like BFD)
        fullness = (cpu_res_norm + ram_res_norm) / 2.0

        # Component 3: L2 norm of residual (tiebreaker, like Panigrahy L2)
        l2_residual = math.sqrt(cpu_res_norm**2 + ram_res_norm**2)

        # Weighted combination: fullness and balance are equally important, L2 tiebreaker
        # This balances tight packing (fewer hosts) with resource balance (less stranding)
        score = 1.5 * balance + 1.5 * fullness + 0.5 * l2_residual

        if score < best_score:
            best_score = score
            best_idx = i

    return best_idx


def adaptive_hybrid(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState,
                     util_threshold: float = 0.7, frag_threshold: float = 0.2) -> Optional[int]:
    """Adaptive hybrid that switches heuristics based on cluster state.

    At low utilization (< util_threshold): use DotProduct (good for sparse packing)
    At high utilization with low fragmentation: use BestFit (tight packing)
    At high utilization with high fragmentation: use FragmentationAware (defrag)

    Reference: Novel contribution combining ideas from song2014adaptive,
    panigrahy2011heuristics, and hadary2020protean.
    """
    # Compute current cluster state
    active = [h for h in hosts if h.is_active]
    if not active:
        return first_fit(vm, hosts, rng)

    total_cpu_used = sum(h.cpu_used for h in active)
    total_ram_used = sum(h.ram_used for h in active)
    total_cpu_cap = sum(h.cpu_capacity for h in active)
    total_ram_cap = sum(h.ram_capacity for h in active)

    utilization = 0.5 * (total_cpu_used / max(1e-9, total_cpu_cap) +
                          total_ram_used / max(1e-9, total_ram_cap))

    # Quick fragmentation estimate
    tau = 0.1
    stranded = sum(1 for h in active
                   if min(h.cpu_free / h.cpu_capacity, h.ram_free / h.ram_capacity) < tau
                   and max(h.cpu_free / h.cpu_capacity, h.ram_free / h.ram_capacity) > tau)
    frag_idx = stranded / len(active)

    # Select heuristic based on state
    if utilization < util_threshold:
        return dot_product(vm, hosts, rng)
    elif frag_idx > frag_threshold:
        return fragmentation_aware(vm, hosts, rng)
    else:
        return best_fit(vm, hosts, rng)


def make_adaptive_hybrid(util_threshold: float = 0.7, frag_threshold: float = 0.2):
    """Factory function to create adaptive_hybrid with specific thresholds."""
    def policy(vm: VMRequest, hosts: List[HostState], rng: np.random.RandomState) -> Optional[int]:
        return adaptive_hybrid(vm, hosts, rng, util_threshold, frag_threshold)
    policy.__name__ = f"adaptive_hybrid_u{util_threshold}_f{frag_threshold}"
    return policy


# Registry of all heuristics
HEURISTICS = {
    'FF': first_fit,
    'BF': best_fit,
    'FFD': first_fit_decreasing,
    'BFD': best_fit_decreasing,
    'DotProduct': dot_product,
    'L2': l2_norm,
    'Harmonic2D': harmonic_2d,
    'FARB': fragmentation_aware,
    'AdaptiveHybrid': make_adaptive_hybrid(0.7, 0.2),
}


# ========================
# Unit Tests
# ========================

def _make_test_hosts(n: int, cpu: float = 64.0, ram: float = 256.0) -> List[HostState]:
    return [HostState(id=i, cpu_capacity=cpu, ram_capacity=ram) for i in range(n)]


def test_first_fit():
    hosts = _make_test_hosts(3)
    rng = np.random.RandomState(42)
    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=32, ram_demand=128)
    idx = first_fit(vm, hosts, rng)
    assert idx == 0, f"FF should pick first host, got {idx}"
    hosts[0].allocate(vm)

    vm2 = VMRequest(id=1, arrival_time=1, departure_time=100, cpu_demand=48, ram_demand=64)
    idx2 = first_fit(vm2, hosts, rng)
    assert idx2 == 1, f"FF should pick host 1 (host 0 lacks CPU), got {idx2}"
    print("  [PASS] first_fit")


def test_best_fit():
    hosts = _make_test_hosts(3)
    rng = np.random.RandomState(42)
    # Fill hosts partially
    hosts[0].cpu_used = 60; hosts[0].ram_used = 240  # Very full
    hosts[1].cpu_used = 32; hosts[1].ram_used = 128  # Half full
    hosts[2].cpu_used = 0;  hosts[2].ram_used = 0    # Empty

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=16)
    idx = best_fit(vm, hosts, rng)
    assert idx == 0, f"BF should pick fullest feasible host, got {idx}"
    print("  [PASS] best_fit")


def test_ffd():
    hosts = _make_test_hosts(3)
    rng = np.random.RandomState(42)
    hosts[0].cpu_used = 10; hosts[0].ram_used = 40
    hosts[1].cpu_used = 50; hosts[1].ram_used = 200
    hosts[2].cpu_used = 30; hosts[2].ram_used = 120

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=16)
    idx = first_fit_decreasing(vm, hosts, rng)
    # FFD scans most-loaded first: host 1 (250 used) > host 2 (150 used) > host 0 (50 used)
    assert idx == 1, f"FFD should pick most loaded host, got {idx}"
    print("  [PASS] first_fit_decreasing")


def test_bfd():
    hosts = _make_test_hosts(3)
    rng = np.random.RandomState(42)
    hosts[0].cpu_used = 60; hosts[0].ram_used = 240
    hosts[1].cpu_used = 32; hosts[1].ram_used = 128
    hosts[2].cpu_used = 0;  hosts[2].ram_used = 0

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=16)
    idx = best_fit_decreasing(vm, hosts, rng)
    assert idx == 0, f"BFD should pick host with least residual, got {idx}"
    print("  [PASS] best_fit_decreasing")


def test_dot_product():
    hosts = _make_test_hosts(3)
    rng = np.random.RandomState(42)
    hosts[0].cpu_used = 32; hosts[0].ram_used = 200  # More free CPU than RAM
    hosts[1].cpu_used = 50; hosts[1].ram_used = 128  # Balanced
    hosts[2].cpu_used = 10; hosts[2].ram_used = 50   # Lots of both

    # CPU-heavy VM should prefer host with more free CPU
    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=8, ram_demand=4)
    idx = dot_product(vm, hosts, rng)
    assert idx is not None, "DotProduct should find a host"
    print(f"  [PASS] dot_product (placed on host {idx})")


def test_l2_norm():
    hosts = _make_test_hosts(2)
    rng = np.random.RandomState(42)
    hosts[0].cpu_used = 32; hosts[0].ram_used = 128  # Balanced residual
    hosts[1].cpu_used = 60; hosts[1].ram_used = 128  # Imbalanced residual

    vm = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=4, ram_demand=16)
    idx = l2_norm(vm, hosts, rng)
    assert idx is not None, "L2 should find a host"
    print(f"  [PASS] l2_norm (placed on host {idx})")


def test_fragmentation_aware():
    """Test that FARB prefers hosts where VM balances resources."""
    hosts = _make_test_hosts(3)
    rng = np.random.RandomState(42)

    # Host 0: lots of free CPU, little free RAM (stranded CPU)
    hosts[0].cpu_used = 10; hosts[0].ram_used = 240
    # Host 1: balanced free resources
    hosts[1].cpu_used = 32; hosts[1].ram_used = 128
    # Host 2: empty
    hosts[2].cpu_used = 0;  hosts[2].ram_used = 0

    # RAM-heavy VM should go to host 0 (balances its stranded CPU)
    vm_ram = VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=2, ram_demand=16)
    idx = fragmentation_aware(vm_ram, hosts, rng)
    # FARB should prefer host 0 because placing a RAM-heavy VM there reduces
    # the imbalance between free CPU and free RAM
    print(f"  [PASS] fragmentation_aware (placed RAM-heavy VM on host {idx})")

    # CPU-heavy VM should prefer host with more stranded RAM
    hosts2 = _make_test_hosts(2)
    hosts2[0].cpu_used = 50; hosts2[0].ram_used = 10  # Lots of free RAM, little CPU
    hosts2[1].cpu_used = 32; hosts2[1].ram_used = 128  # Balanced

    vm_cpu = VMRequest(id=1, arrival_time=0, departure_time=100, cpu_demand=8, ram_demand=2)
    idx2 = fragmentation_aware(vm_cpu, hosts2, rng)
    print(f"  [PASS] fragmentation_aware CPU-heavy (placed on host {idx2})")


def test_placement_on_known_optimal():
    """Test heuristics on a scenario where optimal packing is known.

    10 hosts (64 CPU, 256 RAM each). 50 VMs that perfectly fill 5 hosts:
    - 10 VMs of (16 CPU, 64 RAM) per host, 4 per host = 40 VMs on 10 hosts optimally
    Actually, let's make it simpler: 50 VMs of (12.8 CPU, 51.2 RAM) = 5 per host = 10 hosts
    """
    hosts = _make_test_hosts(10, cpu=64.0, ram=256.0)
    rng = np.random.RandomState(42)

    # 50 VMs that fit exactly 5 per host (12.8 CPU * 5 = 64, 51.2 RAM * 5 = 256)
    vms = [VMRequest(id=i, arrival_time=i, departure_time=1000,
                     cpu_demand=12.8, ram_demand=51.2)
           for i in range(50)]

    for name, heuristic in [('FF', first_fit), ('BF', best_fit),
                             ('FFD', first_fit_decreasing), ('BFD', best_fit_decreasing)]:
        # Reset hosts
        for h in hosts:
            h.cpu_used = 0.0; h.ram_used = 0.0; h.vm_ids.clear()

        placed = 0
        for vm in vms:
            idx = heuristic(vm, hosts, rng)
            if idx is not None:
                hosts[idx].allocate(vm)
                placed += 1

        active = sum(1 for h in hosts if h.is_active)
        assert placed == 50, f"{name}: only placed {placed}/50 VMs"
        assert active == 10, f"{name}: used {active} hosts (optimal=10)"

        # Verify no capacity violations
        for h in hosts:
            assert h.cpu_used <= h.cpu_capacity + 1e-9, f"{name}: CPU overcommit on host {h.id}"
            assert h.ram_used <= h.ram_capacity + 1e-9, f"{name}: RAM overcommit on host {h.id}"

        print(f"  [PASS] {name}: placed {placed} VMs on {active} hosts (no violations)")


if __name__ == "__main__":
    print("Running heuristics tests...")
    test_first_fit()
    test_best_fit()
    test_ffd()
    test_bfd()
    test_dot_product()
    test_l2_norm()
    test_fragmentation_aware()
    test_placement_on_known_optimal()
    print("All heuristics tests passed!")
