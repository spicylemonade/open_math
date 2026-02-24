"""
VM migration/defragmentation module.

Periodically scans active hosts for consolidation opportunities,
proposing VM migrations that reduce total active hosts.
"""

from typing import List, Dict, Tuple, Optional
import numpy as np

from simulator import HostState
from trace_parser import VMRequest


def find_consolidation_opportunities(
    hosts: List[HostState],
    vm_registry: Dict[int, VMRequest],
    max_migrations: int = 10,
    rng: np.random.RandomState = None,
) -> List[Tuple[int, int, int]]:
    """Find VM migrations that reduce the number of active hosts.

    Strategy: Sort hosts by load (least loaded first). For each under-loaded host,
    try to migrate all its VMs to other hosts. If successful, the host becomes empty.

    Args:
        hosts: Current host states
        vm_registry: Map from vm_id to VMRequest
        max_migrations: Maximum migrations allowed per pass
        rng: Random state for tiebreaking

    Returns:
        List of (vm_id, source_host_id, target_host_id) migration tuples
    """
    if rng is None:
        rng = np.random.RandomState(42)

    active = [h for h in hosts if h.is_active]
    if len(active) <= 1:
        return []

    # Sort by total load (least loaded first — candidates for evacuation)
    active.sort(key=lambda h: h.cpu_used + h.ram_used)

    migrations = []
    migration_count = 0

    for source in active:
        if migration_count >= max_migrations:
            break
        if not source.is_active:
            continue

        # Try to evacuate this host by moving all its VMs elsewhere
        vm_ids = list(source.vm_ids)
        proposed = []  # (vm_id, target_host_id)
        feasible = True

        for vm_id in vm_ids:
            if vm_id not in vm_registry:
                continue
            vm = vm_registry[vm_id]

            # Find a target host (not the source) that can fit this VM
            target = None
            best_residual = float('inf')

            for h in active:
                if h.id == source.id:
                    continue
                if h.can_fit(vm.cpu_demand, vm.ram_demand):
                    residual = (h.cpu_free - vm.cpu_demand)**2 + (h.ram_free - vm.ram_demand)**2
                    if residual < best_residual:
                        best_residual = residual
                        target = h

            if target is None:
                feasible = False
                break

            proposed.append((vm_id, target.id))

        if feasible and proposed:
            # Execute the evacuation (virtually)
            for vm_id, target_id in proposed:
                vm = vm_registry[vm_id]
                target_host = next(h for h in active if h.id == target_id)
                source.deallocate(vm)
                target_host.allocate(vm)
                migrations.append((vm_id, source.id, target_id))
                migration_count += 1

                if migration_count >= max_migrations:
                    break

    return migrations


def defragmentation_pass(
    host_states: List[HostState],
    vm_to_host: Dict[int, int],
    active_vms: Dict[int, VMRequest],
    max_migrations: int = 10,
    rng: np.random.RandomState = None,
) -> Tuple[int, int]:
    """Execute a defragmentation pass on the cluster.

    Returns:
        (hosts_freed, migrations_executed)
    """
    active_before = sum(1 for h in host_states if h.is_active)

    migrations = find_consolidation_opportunities(
        host_states, active_vms, max_migrations, rng)

    # Update vm_to_host mapping
    for vm_id, source_id, target_id in migrations:
        vm_to_host[vm_id] = target_id

    active_after = sum(1 for h in host_states if h.is_active)

    return active_before - active_after, len(migrations)


# ---- Test ----

def test_defragmentation():
    """Test that defrag can consolidate under-loaded hosts."""
    hosts = [HostState(id=i, cpu_capacity=10, ram_capacity=20) for i in range(5)]

    # Create VMs
    vms = {
        0: VMRequest(id=0, arrival_time=0, departure_time=100, cpu_demand=2, ram_demand=4),
        1: VMRequest(id=1, arrival_time=0, departure_time=100, cpu_demand=2, ram_demand=4),
        2: VMRequest(id=2, arrival_time=0, departure_time=100, cpu_demand=2, ram_demand=4),
        3: VMRequest(id=3, arrival_time=0, departure_time=100, cpu_demand=2, ram_demand=4),
        4: VMRequest(id=4, arrival_time=0, departure_time=100, cpu_demand=2, ram_demand=4),
    }

    # Spread across 5 hosts (1 VM each — very fragmented)
    vm_to_host = {}
    for i in range(5):
        hosts[i].allocate(vms[i])
        vm_to_host[i] = i

    active_before = sum(1 for h in hosts if h.is_active)
    assert active_before == 5, f"Expected 5 active hosts, got {active_before}"

    freed, migrated = defragmentation_pass(hosts, vm_to_host, vms, max_migrations=10)

    active_after = sum(1 for h in hosts if h.is_active)
    print(f"  [PASS] Defragmentation: {active_before}→{active_after} hosts "
          f"(freed {freed}, migrated {migrated})")
    assert active_after < active_before, "Defrag should reduce active hosts"
    assert active_after == 1, f"All 5 VMs fit on 1 host, got {active_after}"


if __name__ == "__main__":
    print("Running defragmentation tests...")
    test_defragmentation()
    print("All defragmentation tests passed!")
