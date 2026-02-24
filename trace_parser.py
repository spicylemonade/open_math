"""
Workload trace parser for Google Cluster Trace and Azure Packing Trace.

Produces a unified internal format:
  - VMRequest: (id, arrival_time, departure_time, cpu_demand, ram_demand)
  - HostSpec: (cpu_capacity, ram_capacity)

Since the actual Google BigQuery and Azure SQLite datasets require external
downloads, this module also provides synthetic trace generators that mimic
the statistical properties of real traces for development and testing.
"""

import csv
import json
import os
import sqlite3
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional

import numpy as np


@dataclass
class VMRequest:
    """A VM placement request with resource demands and lifecycle."""
    id: int
    arrival_time: float
    departure_time: float
    cpu_demand: float
    ram_demand: float


@dataclass
class HostSpec:
    """Physical host specification."""
    cpu_capacity: float
    ram_capacity: float


@dataclass
class TraceData:
    """Unified trace data format."""
    vms: List[VMRequest]
    hosts: List[HostSpec]
    name: str
    source: str


def generate_synthetic_trace(
    n_vms: int = 10000,
    n_hosts: int = 500,
    host_cpu: float = 64.0,
    host_ram: float = 256.0,
    seed: int = 42,
    duration: float = 86400.0,  # 24 hours in seconds
    vm_size_dist: str = "realistic",
    load_factor: float = 0.85,
) -> TraceData:
    """Generate a synthetic trace mimicking production workload characteristics.

    VM sizes are drawn from distributions observed in production traces:
    - Small (1-2 CPU, 1-4 GB RAM): ~60% of VMs
    - Medium (4-8 CPU, 8-32 GB RAM): ~25% of VMs
    - Large (16-32 CPU, 64-128 GB RAM): ~12% of VMs
    - XLarge (48-64 CPU, 192-256 GB RAM): ~3% of VMs
    """
    rng = np.random.RandomState(seed)

    # Define VM size classes based on production observations
    if vm_size_dist == "realistic":
        size_classes = [
            # (prob, cpu_range, ram_range)
            (0.60, (1, 2), (1, 4)),
            (0.25, (4, 8), (8, 32)),
            (0.12, (16, 32), (64, 128)),
            (0.03, (48, 64), (192, 256)),
        ]
    elif vm_size_dist == "cpu_heavy":
        size_classes = [
            (0.50, (4, 8), (2, 4)),
            (0.30, (16, 32), (8, 16)),
            (0.15, (32, 48), (16, 32)),
            (0.05, (48, 64), (32, 64)),
        ]
    elif vm_size_dist == "ram_heavy":
        size_classes = [
            (0.50, (1, 2), (8, 16)),
            (0.30, (2, 4), (32, 64)),
            (0.15, (4, 8), (64, 128)),
            (0.05, (8, 16), (128, 256)),
        ]
    elif vm_size_dist == "uniform_small":
        size_classes = [
            (0.80, (1, 2), (1, 4)),
            (0.15, (2, 4), (4, 8)),
            (0.05, (4, 8), (8, 16)),
        ]
    elif vm_size_dist == "bimodal":
        size_classes = [
            (0.50, (1, 2), (1, 4)),
            (0.10, (4, 8), (8, 16)),
            (0.10, (8, 16), (16, 64)),
            (0.30, (32, 64), (128, 256)),
        ]
    else:
        raise ValueError(f"Unknown VM size distribution: {vm_size_dist}")

    vms = []
    probs = [sc[0] for sc in size_classes]

    # Generate VM arrivals using Poisson process
    arrival_rate = n_vms / duration
    arrival_times = np.cumsum(rng.exponential(1.0 / arrival_rate, n_vms))
    arrival_times = arrival_times * (duration / arrival_times[-1])  # Scale to duration

    for i in range(n_vms):
        # Choose size class
        cls_idx = rng.choice(len(size_classes), p=probs)
        _, cpu_range, ram_range = size_classes[cls_idx]

        # Sample CPU and RAM demands
        cpu = rng.uniform(cpu_range[0], cpu_range[1])
        ram = rng.uniform(ram_range[0], ram_range[1])

        # Round to practical values
        cpu = max(1.0, round(cpu))
        ram = max(1.0, round(ram))

        # VM lifetime: log-normal distribution (median ~2 hours, heavy tail)
        lifetime = rng.lognormal(mean=np.log(7200), sigma=1.5)
        lifetime = max(60.0, min(lifetime, duration * 0.9))

        arrival = arrival_times[i]
        departure = arrival + lifetime

        vms.append(VMRequest(
            id=i,
            arrival_time=arrival,
            departure_time=departure,
            cpu_demand=cpu,
            ram_demand=ram,
        ))

    hosts = [HostSpec(cpu_capacity=host_cpu, ram_capacity=host_ram)
             for _ in range(n_hosts)]

    return TraceData(
        vms=vms,
        hosts=hosts,
        name=f"synthetic_{vm_size_dist}_{n_vms}",
        source="synthetic",
    )


def parse_azure_packing_trace(db_path: str) -> TraceData:
    """Parse Azure Traces for Packing 2020 (SQLite format).

    Expected tables:
    - vmType: vmTypeId, core, memory (normalized)
    - vm: vmId, vmTypeId, starttime, endtime
    - machineType: machineTypeId, core, memory
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get machine types for host specs
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    hosts = []
    if "machineType" in tables:
        cursor.execute("SELECT core, memory FROM machineType")
        for row in cursor.fetchall():
            hosts.append(HostSpec(cpu_capacity=float(row[0]), ram_capacity=float(row[1])))

    # Get VM types
    vm_types = {}
    if "vmType" in tables:
        cursor.execute("SELECT vmTypeId, core, memory FROM vmType")
        for row in cursor.fetchall():
            vm_types[row[0]] = (float(row[1]), float(row[2]))

    # Get VMs
    vms = []
    if "vm" in tables:
        cursor.execute("SELECT vmId, vmTypeId, starttime, endtime FROM vm ORDER BY starttime")
        for i, row in enumerate(cursor.fetchall()):
            vm_id, type_id, start, end = row
            if type_id in vm_types:
                cpu, ram = vm_types[type_id]
                vms.append(VMRequest(
                    id=i,
                    arrival_time=float(start),
                    departure_time=float(end) if end else float(start) + 86400,
                    cpu_demand=cpu,
                    ram_demand=ram,
                ))

    conn.close()

    if not hosts:
        # Default host spec if not in database
        hosts = [HostSpec(cpu_capacity=1.0, ram_capacity=1.0) for _ in range(1000)]

    return TraceData(vms=vms, hosts=hosts, name="azure_packing_2020", source="azure")


def parse_google_cluster_trace_csv(events_path: str, machines_path: str = None) -> TraceData:
    """Parse Google ClusterData2019 from CSV exports.

    Expected columns in events file:
    - time, type (0=submit, 4=finish, etc.), collection_id, instance_index,
      machine_id, cpu_request, memory_request

    Resources are already normalized to [0, 1] relative to the largest machine.
    """
    vms = []
    vm_dict = {}  # Track active VMs for departure matching

    with open(events_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            if len(row) < 6:
                continue
            try:
                time_val = float(row[0])
                event_type = int(row[1]) if row[1] else -1
                collection_id = row[2]
                instance_idx = row[3]
                cpu_req = float(row[4]) if row[4] else 0.0
                mem_req = float(row[5]) if row[5] else 0.0
            except (ValueError, IndexError):
                continue

            vm_key = f"{collection_id}_{instance_idx}"

            if event_type == 0:  # SUBMIT/SCHEDULE
                if cpu_req > 0 and mem_req > 0:
                    vm_dict[vm_key] = {
                        'arrival': time_val,
                        'cpu': cpu_req,
                        'ram': mem_req,
                    }
            elif event_type in (4, 5, 6):  # FINISH/FAIL/KILL
                if vm_key in vm_dict:
                    info = vm_dict.pop(vm_key)
                    vms.append(VMRequest(
                        id=len(vms),
                        arrival_time=info['arrival'],
                        departure_time=time_val,
                        cpu_demand=info['cpu'],
                        ram_demand=info['ram'],
                    ))

    # For VMs that never finished, set departure to max time + buffer
    if vms:
        max_time = max(v.departure_time for v in vms)
    else:
        max_time = 86400.0

    for key, info in vm_dict.items():
        vms.append(VMRequest(
            id=len(vms),
            arrival_time=info['arrival'],
            departure_time=max_time + 3600,
            cpu_demand=info['cpu'],
            ram_demand=info['ram'],
        ))

    # Sort by arrival time
    vms.sort(key=lambda v: v.arrival_time)

    # Google traces use normalized resources [0,1]; host capacity = 1.0
    hosts = [HostSpec(cpu_capacity=1.0, ram_capacity=1.0) for _ in range(12000)]

    return TraceData(vms=vms, hosts=hosts, name="google_cluster_2019", source="google")


def generate_google_like_trace(n_vms: int = 100000, n_hosts: int = 12000, seed: int = 42) -> TraceData:
    """Generate a synthetic trace mimicking Google cluster workload properties.

    Google traces show normalized resources in [0, 1]. Typical task characteristics:
    - Most tasks are small (< 0.05 CPU, < 0.05 RAM)
    - Some batch tasks are medium (0.05-0.25 CPU/RAM)
    - Few large tasks (> 0.25 CPU or RAM)
    """
    rng = np.random.RandomState(seed)
    duration = 86400.0 * 7  # 7 days

    size_classes = [
        (0.65, (0.005, 0.05), (0.005, 0.05)),    # Tiny tasks
        (0.20, (0.05, 0.15), (0.05, 0.15)),       # Small tasks
        (0.10, (0.15, 0.35), (0.10, 0.30)),       # Medium tasks
        (0.04, (0.30, 0.60), (0.25, 0.50)),       # Large tasks
        (0.01, (0.50, 1.00), (0.50, 1.00)),       # Huge tasks
    ]
    probs = [sc[0] for sc in size_classes]

    arrival_times = np.cumsum(rng.exponential(duration / n_vms, n_vms))
    arrival_times = arrival_times * (duration / arrival_times[-1])

    vms = []
    for i in range(n_vms):
        cls_idx = rng.choice(len(size_classes), p=probs)
        _, cpu_range, ram_range = size_classes[cls_idx]

        cpu = rng.uniform(cpu_range[0], cpu_range[1])
        ram = rng.uniform(ram_range[0], ram_range[1])

        # Lifetime: bimodal (short batch jobs + long-running services)
        if rng.random() < 0.7:  # Batch jobs
            lifetime = rng.exponential(300)  # ~5 min average
        else:  # Long-running services
            lifetime = rng.exponential(86400)  # ~1 day average

        lifetime = max(10.0, min(lifetime, duration * 0.95))

        vms.append(VMRequest(
            id=i,
            arrival_time=arrival_times[i],
            departure_time=arrival_times[i] + lifetime,
            cpu_demand=cpu,
            ram_demand=ram,
        ))

    hosts = [HostSpec(cpu_capacity=1.0, ram_capacity=1.0) for _ in range(n_hosts)]

    return TraceData(vms=vms, hosts=hosts, name="google_like_synthetic", source="google_synthetic")


def generate_azure_like_trace(n_vms: int = 50000, n_hosts: int = 1000, seed: int = 42) -> TraceData:
    """Generate a synthetic trace mimicking Azure VM workload properties.

    Azure VMs have discrete sizes (D-series, E-series, etc.) with specific CPU:RAM ratios.
    Resources normalized to fractional machine units.
    """
    rng = np.random.RandomState(seed)
    duration = 86400.0 * 14  # 14 days

    # Azure-like VM types (cpu_frac, ram_frac) as fraction of host capacity
    # Mimicking D-series (balanced), E-series (memory), F-series (compute)
    vm_types = [
        (0.10, (0.0625, 0.0625)),  # Standard_D2  (2/32 CPU, 8/128 RAM ~ balanced)
        (0.15, (0.125, 0.125)),    # Standard_D4
        (0.10, (0.250, 0.250)),    # Standard_D8
        (0.05, (0.500, 0.500)),    # Standard_D16
        (0.15, (0.0625, 0.125)),   # Standard_E2 (memory optimized)
        (0.10, (0.125, 0.250)),    # Standard_E4
        (0.05, (0.250, 0.500)),    # Standard_E8
        (0.15, (0.125, 0.0625)),   # Standard_F4 (compute optimized)
        (0.08, (0.250, 0.125)),    # Standard_F8
        (0.07, (0.500, 0.250)),    # Standard_F16
    ]
    probs = [vt[0] for vt in vm_types]

    arrival_times = np.cumsum(rng.exponential(duration / n_vms, n_vms))
    arrival_times = arrival_times * (duration / arrival_times[-1])

    vms = []
    for i in range(n_vms):
        type_idx = rng.choice(len(vm_types), p=probs)
        _, (cpu, ram) = vm_types[type_idx]

        # VM lifetime: log-normal (median ~12 hours)
        lifetime = rng.lognormal(mean=np.log(43200), sigma=1.2)
        lifetime = max(300.0, min(lifetime, duration * 0.9))

        vms.append(VMRequest(
            id=i,
            arrival_time=arrival_times[i],
            departure_time=arrival_times[i] + lifetime,
            cpu_demand=cpu,
            ram_demand=ram,
        ))

    hosts = [HostSpec(cpu_capacity=1.0, ram_capacity=1.0) for _ in range(n_hosts)]

    return TraceData(vms=vms, hosts=hosts, name="azure_like_synthetic", source="azure_synthetic")


def save_trace(trace: TraceData, path: str):
    """Save trace data to JSON."""
    data = {
        'name': trace.name,
        'source': trace.source,
        'n_vms': len(trace.vms),
        'n_hosts': len(trace.hosts),
        'vms': [asdict(vm) for vm in trace.vms],
        'hosts': [asdict(h) for h in trace.hosts],
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def load_trace(path: str) -> TraceData:
    """Load trace data from JSON."""
    with open(path, 'r') as f:
        data = json.load(f)
    vms = [VMRequest(**vm) for vm in data['vms']]
    hosts = [HostSpec(**h) for h in data['hosts']]
    return TraceData(vms=vms, hosts=hosts, name=data['name'], source=data['source'])


# ---- Unit tests ----

def test_synthetic_trace_generation():
    """Test that synthetic traces produce valid data."""
    trace = generate_synthetic_trace(n_vms=1000, n_hosts=50, seed=42)
    assert len(trace.vms) == 1000, f"Expected 1000 VMs, got {len(trace.vms)}"
    assert len(trace.hosts) == 50, f"Expected 50 hosts, got {len(trace.hosts)}"

    for vm in trace.vms:
        assert vm.cpu_demand > 0, f"VM {vm.id} has non-positive CPU"
        assert vm.ram_demand > 0, f"VM {vm.id} has non-positive RAM"
        assert vm.departure_time > vm.arrival_time, f"VM {vm.id} departs before arrival"
        assert vm.cpu_demand <= trace.hosts[0].cpu_capacity, f"VM {vm.id} CPU exceeds host"
        assert vm.ram_demand <= trace.hosts[0].ram_capacity, f"VM {vm.id} RAM exceeds host"

    # Check arrival times are sorted
    for i in range(1, len(trace.vms)):
        assert trace.vms[i].arrival_time >= trace.vms[i-1].arrival_time, \
            f"VMs not sorted by arrival time at index {i}"

    print(f"  [PASS] Synthetic trace: {len(trace.vms)} VMs, {len(trace.hosts)} hosts")


def test_google_like_trace():
    """Test Google-like synthetic trace."""
    trace = generate_google_like_trace(n_vms=1000, n_hosts=100, seed=42)
    assert len(trace.vms) == 1000
    for vm in trace.vms:
        assert 0 < vm.cpu_demand <= 1.0, f"Google trace CPU should be in (0,1]: {vm.cpu_demand}"
        assert 0 < vm.ram_demand <= 1.0, f"Google trace RAM should be in (0,1]: {vm.ram_demand}"
    print(f"  [PASS] Google-like trace: {len(trace.vms)} VMs")


def test_azure_like_trace():
    """Test Azure-like synthetic trace."""
    trace = generate_azure_like_trace(n_vms=1000, n_hosts=100, seed=42)
    assert len(trace.vms) == 1000
    for vm in trace.vms:
        assert 0 < vm.cpu_demand <= 1.0, f"Azure trace CPU should be in (0,1]: {vm.cpu_demand}"
        assert 0 < vm.ram_demand <= 1.0, f"Azure trace RAM should be in (0,1]: {vm.ram_demand}"
    print(f"  [PASS] Azure-like trace: {len(trace.vms)} VMs")


def test_save_load_roundtrip():
    """Test save/load roundtrip."""
    trace = generate_synthetic_trace(n_vms=100, n_hosts=10, seed=42)
    path = "/tmp/test_trace.json"
    save_trace(trace, path)
    loaded = load_trace(path)
    assert len(loaded.vms) == len(trace.vms)
    assert loaded.vms[0].cpu_demand == trace.vms[0].cpu_demand
    os.remove(path)
    print("  [PASS] Save/load roundtrip")


if __name__ == "__main__":
    print("Running trace parser tests...")
    test_synthetic_trace_generation()
    test_google_like_trace()
    test_azure_like_trace()
    test_save_load_roundtrip()
    print("All trace parser tests passed!")
