# Survey: Real-World Road Network Routing Tools and Datasets

## Overview
To benchmark TSP heuristics on real road networks, we need tools to extract road graph data from OpenStreetMap and compute travel-time/distance matrices between arbitrary points. This survey covers the major open-source routing engines and data extraction tools.

## Tool Comparison Table

| Tool | Type | Language | Distance Matrix | Asymmetric Support | Traffic Data | License | Scale |
|------|------|----------|----------------|-------------------|-------------|---------|-------|
| OSRM | Routing engine | C++ | Yes (Table API) | Yes (inherently asymmetric) | No (static profiles) | BSD-2 | Continental |
| Valhalla | Routing engine | C++ | Yes (Matrix API) | Yes | Yes (time-dependent costing) | MIT | Continental |
| GraphHopper | Routing engine | Java | Yes (Matrix API) | Yes | Yes (commercial) | Apache 2.0 (core), Proprietary (matrix) | Continental |
| OSMnx | Data extraction + analysis | Python | Via NetworkX shortest paths | Yes (directed graph) | No | MIT | City-scale |
| pyrosm | Fast OSM data reader | Python | No (data extraction only) | N/A | No | MIT | Regional |

## Detailed Tool Reviews

### 1. OSRM (Open Source Routing Machine)
- **Description**: High-performance routing engine using OpenStreetMap data. Precomputes contraction hierarchies for fast queries.
- **Table API**: Returns asymmetric NxN travel time and distance matrices. Endpoint: `/table/v1/driving/{coordinates}`. Supports source/destination filtering for rectangular matrices.
- **Asymmetric travel times**: Inherently asymmetric because road networks have one-way streets, different speed limits by direction, and varying connectivity. The matrix `durations[i][j]` naturally differs from `durations[j][i]`.
- **Data format**: Accepts coordinates (lon,lat), returns durations in seconds and distances in meters as JSON arrays.
- **Limitations**: No traffic/time-dependent routing. Static road profiles only. Must self-host for large-scale use (public demo server has rate limits).
- **Setup**: Download OSM PBF file → run `osrm-extract` → `osrm-partition` → `osrm-customize` → start `osrm-routed`.
- **Reference**: Luxen and Vetter (2011), "Real-time routing with OpenStreetMap data"

### 2. Valhalla
- **Description**: Modern open-source routing engine with dynamic, runtime costing. Uses tiled graph hierarchy for memory efficiency.
- **Matrix API**: Computes time and distance matrices. Supports asymmetric queries.
- **Traffic support**: Integrates time-dependent speed data into routing (except Matrix API currently). Historical traffic patterns can be incorporated.
- **Key advantage**: Dynamic costing — can change cost model at query time without rebuilding the graph.
- **Limitations**: Matrix API slower than OSRM for large queries. Traffic not in matrix computations.
- **License**: MIT (fully open source, originated at Mapzen, now maintained by community + Mapbox contributors).
- **Reference**: Valhalla documentation, GitHub repository

### 3. GraphHopper
- **Description**: Fast, memory-efficient routing engine in Java. Uses contraction hierarchies for speed.
- **Matrix API**: Extremely fast — 100M costs on single core (~350K routes/sec). For 1000 locations, matrix in <5 seconds.
- **Limitation**: Matrix API code is proprietary (closed-source for business reasons). Open-source core supports routing but not the optimized matrix computation.
- **Reference**: GraphHopper documentation and blog

### 4. OSMnx (Boeing, 2017)
- **Description**: Python package for downloading, modeling, and analyzing OpenStreetMap street networks using NetworkX.
- **Key capabilities**:
  - Download street network for any city/region with one line of code
  - Returns NetworkX directed multigraph with edge attributes (length, speed, travel time)
  - Can compute shortest paths and travel times between arbitrary nodes
  - Supports graph simplification, projection, and visualization
- **Distance matrix computation**: Can compute all-pairs shortest paths using NetworkX algorithms (Dijkstra). For ATSP instances, compute the NxN asymmetric travel time matrix by running shortest path from each node to all others.
- **Advantages for this project**: Pure Python, no external server needed. Direct access to graph topology. Can sample random nodes on the network for instance generation.
- **Limitations**: Shortest path computation is slow for large networks (no contraction hierarchies). City-scale practical, not continental.
- **Reference**: Boeing (2017), "OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks"

### 5. pyrosm
- **Description**: Fast OSM data reader using Cython. Can parse PBF files much faster than osmium or osmnx for bulk data extraction.
- **Use case**: Extract raw OSM data quickly for preprocessing before routing.
- **Limitations**: No routing functionality, just data extraction.

## Recommended Approach for This Project

For generating ATSP benchmark instances from real road networks:

1. **Use OSMnx** to download road network graphs for target cities
2. **Sample random points** on the network as TSP customer locations
3. **Compute asymmetric travel-time matrices** using NetworkX shortest paths on the OSMnx graph
4. **For larger instances**, optionally use a local OSRM server for faster matrix computation
5. **Store instances** in standardized JSON format with metadata (city, coordinates, matrix, asymmetry metrics)

This avoids dependency on external OSRM servers while giving us real road network data with natural asymmetry from one-way streets and road topology.

## Data Sources
- **OpenStreetMap**: Free, open geographic database. Primary source for all road network data.
- **TSPLIB/ATSPLIB**: Standard benchmark library for TSP instances. Useful for validation but uses synthetic/geometric instances.
- **DIMACS TSP Challenge**: Large-scale symmetric TSP benchmarks. Not directly applicable to ATSP on road networks.
