# Survey of Public Workload Trace Datasets for VM Scheduling Evaluation

## 1. Google Cluster Trace v3 (ClusterData2019)

- **Source URL**: https://github.com/google/cluster-data/blob/master/ClusterData2019.md
- **Provider**: Google
- **Collection Period**: May 2019 (full month)
- **Scope**: 8 Borg cells, each with ~12,000 machines
- **Size**: ~2.4 TiB compressed; available via Google BigQuery
- **Schema/Fields**:
  - `instance_events`: instance_key, time, type, scheduling_class, priority, cpu_request, memory_request, assigned_machine
  - `machine_events`: time, machine_id, event_type, platform_id, cpu_capacity, memory_capacity
  - `collection_events`: collection_id, scheduling_class, priority, cpu_request, memory_request
  - CPU and RAM are normalized to the largest machine in the cell (values in [0, 1])
- **Time Span**: 31 days
- **Relevance**: Largest publicly available cluster trace. Provides both task resource requests and machine capacities, enabling direct evaluation of 2D bin packing. Includes arrival/departure events needed for online simulation. Heterogeneous machines add realism.
- **Limitations**: Only accessible via BigQuery (requires Google Cloud account). Very large, requiring significant preprocessing. Resource requests are normalized, not absolute values.

## 2. Azure Traces for Packing 2020

- **Source URL**: https://github.com/Azure/AzurePublicDataset/blob/master/AzureTracesForPacking2020.md
- **Provider**: Microsoft Azure
- **Download**: https://azurepublicdatasettraces.blob.core.windows.net/azurepublicdatasetv2/azurevmallocation_dataset2020/AzurePackingTraceV1.zip
- **Format**: SQLite database
- **Schema/Fields**:
  - `vm_type_table`: VM types with normalized CPU and RAM demands (fractional machine units)
  - `vm_table`: VM instances with type, creation time, deletion time
  - Machine types with CPU and RAM capacities
- **Size**: Single availability zone
- **Time Span**: Representative period from Azure production
- **Relevance**: **Primary evaluation dataset** — specifically designed for evaluating packing algorithms. Released alongside the Protean paper (Hadary et al., OSDI 2020). Compact format (SQLite) enables easy local processing. Contains VM type resource vectors directly applicable to vector bin packing evaluation.
- **Limitations**: Single zone only. VM types are anonymized with normalized resource values.

## 3. Azure VM Traces 2017/2019 (V1 and V2)

- **Source URL**: https://github.com/Azure/AzurePublicDataset
  - V1: AzurePublicDatasetV1.md (2017)
  - V2: AzurePublicDatasetV2.md (2019)
- **Provider**: Microsoft Azure
- **Schema/Fields**:
  - V1: VM ID, subscription ID, deployment ID, timestamp VM created, timestamp VM deleted, max/avg CPU utilization, category, VM virtual core count, VM memory (GB)
  - V2: Similar schema with additional fields, covering 30 days
- **Size**: V1: 2,000,000+ VMs over 30 days; V2: 2,600,000+ VMs over 30 days
- **Time Span**: 30 days each
- **Relevance**: Large-scale production VM workload traces with actual CPU and memory allocations. Useful for understanding VM size distributions and lifetime patterns. V2 includes VM priority levels.
- **Limitations**: Focused on VM lifecycle (creation/deletion) rather than explicit packing evaluation. Resource demands are at VM level but machine capacities are not provided — must be assumed or estimated.

## 4. Huawei Cloud VM Scheduling Dataset (Huawei-East-1)

- **Source URL**: https://github.com/huaweicloud/VM-placement-dataset
- **Provider**: Huawei Cloud
- **Format**: CSV
- **Schema/Fields**:
  - `vmid`: VM identifier
  - `cpu`: CPU demand (cores)
  - `memory`: RAM demand (GB)
  - `time`: Timestamp
  - `type`: Event type (creation/deletion)
  - 15 VM types defined
- **Size**: ~125,429 data points, 241,743 requests
- **Time Span**: 1 month
- **Relevance**: First standardized dataset specifically for VM scheduling research. Includes both creation and deletion events enabling dynamic simulation. Compact and easy to parse. Used with VMAgent RL framework. Resource demands are in absolute units (cores, GB).
- **Limitations**: Smaller scale than Google/Azure traces. Single data center. CC-BY-NC license restricts commercial use.

## Primary Evaluation Plan

For our experiments, we will use:

1. **Azure Traces for Packing 2020** (primary): Specifically designed for packing evaluation, compact SQLite format, directly provides VM type resource vectors and machine capacities. We will use the full dataset.

2. **Google ClusterData2019** (secondary): The largest and most comprehensive trace. We will extract a subset of ≥100,000 VM events from a single Borg cell via BigQuery or use pre-extracted samples available on Kaggle.

**Rationale**: The Azure Packing trace is purpose-built for evaluating packing algorithms with clean, well-documented resource vectors. Google's trace provides scale and diversity. Together, they represent the two largest cloud providers and cover different workload characteristics.

For initial development and testing, we will generate **synthetic traces** with configurable VM size distributions, arrival rates, and lifetimes, allowing controlled experiments before moving to production traces.
