# Data Survey: Real-World ATSP Datasets, OSRM APIs, and OSM Data Pipelines

## 1. TSPLIB95 ATSP Instances

**Source:** Gerhard Reinelt, Universität Heidelberg
**URL:** http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
**Mirror:** http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsplib.html

**Description:** TSPLIB is the standard benchmark library for TSP and related problems. The ATSP section contains 19 asymmetric instances ranging from 17 to 443 cities.

**ATSP Instances:**
| Instance | Nodes | Optimal/Best Known |
|----------|-------|--------------------|
| br17     | 17    | 39                 |
| ft53     | 53    | 6905               |
| ft70     | 70    | 38673              |
| ftv33    | 34    | 1286               |
| ftv35    | 36    | 1473               |
| ftv38    | 39    | 1530               |
| ftv44    | 45    | 1613               |
| ftv47    | 48    | 1776               |
| ftv55    | 56    | 1608               |
| ftv64    | 65    | 1839               |
| ftv70    | 71    | 1950               |
| ftv170   | 171   | 2755               |
| kro124p  | 100   | 36230              |
| p43      | 43    | 5620               |
| rbg323   | 323   | 1326               |
| rbg358   | 358   | 1163               |
| rbg403   | 403   | 2465               |
| rbg443   | 443   | 2720               |
| ry48p    | 48    | 14422              |

**Format:** TSPLIB format with EDGE_WEIGHT_TYPE = EXPLICIT and EDGE_WEIGHT_FORMAT = FULL_MATRIX. Distances are integers. Files have `.atsp` extension.

**Accessibility:** Freely downloadable. Python parser available via `tsplib95` PyPI package.

---

## 2. DIMACS ATSP Challenge Instances

**Source:** DIMACS Implementation Challenges
**URL:** http://dimacs.rutgers.edu/programs/challenge/

**Description:** The DIMACS TSP challenge (part of the broader implementation challenge series) includes both symmetric and asymmetric instances. Notable ATSP instances from DIMACS:

- Stacker crane scheduling instances (Ascheuer)
- Random asymmetric matrices
- Structured asymmetric instances (e.g., flow-shop scheduling reductions)

**Format:** TSPLIB-compatible format. Edge weights as full matrices.

**Sizes:** Range from tens to hundreds of nodes. Primarily used for exact algorithm benchmarking.

**Accessibility:** Available via DIMACS challenge archives and the Waterloo TSP page.

---

## 3. Waterloo TSP Data

**Source:** University of Waterloo, William Cook's group
**URL:** https://www.math.uwaterloo.ca/tsp/data/

**Description:** Comprehensive collection of TSP instances including:
- **National datasets:** Points representing cities/towns in various countries (e.g., USA 115,475 cities, Sweden 24,978 cities)
- **VLSI datasets:** Points from VLSI design problems (up to 744,710 nodes)
- **Art TSP instances:** Points derived from artwork
- **Korea 81,998-bar instance:** The record-breaking OSRM-based instance solved in 2025

**Format:** TSPLIB format (node coordinates for symmetric instances). The Korea instance uses OSRM-computed travel times.

**Sizes:** Small (hundreds) to very large (744K+ nodes). Primarily symmetric TSP, but the Korea instance uses real road-network distances.

**Accessibility:** Freely downloadable from the Waterloo TSP website.

---

## 4. Ascheuer TSPTW Instances

**Source:** Norbert Ascheuer, Technische Universität Berlin
**Download:** https://lopez-ibanez.eu/tsptw-instances (López-Ibáñez & Blum collection)

**Description:** 50 asymmetric TSPTW instances derived from an industry project optimizing stacker crane routing in automated storage systems. These are among the most widely used ATSP with time windows benchmarks.

**Instance Details:**
- Based on real-world industrial data
- Asymmetric distance matrices (crane travel times differ by direction)
- Time windows on each node
- Sizes: 17–233 nodes
- Labeled as "AFG" or "rbg" instances in literature
- Base instance rbg027a (27 nodes) with relaxed variants (rbg27.b.x)

**Format:** Custom format with distance matrix and time windows. Standardized versions available from López-Ibáñez collection.

**Accessibility:** Freely downloadable. 467 total TSPTW instances from various sources in the López-Ibáñez collection.

**Caution:** Recent analysis (arxiv:2512.01064) suggests some classical TSPTW benchmarks may not adequately test modern solvers due to loose time windows.

**References:** Ascheuer (1995) PhD thesis [ascheuer1995]; Ascheuer et al. (2001) [ascheuer2001solving].

---

## 5. OSRM Table API

**Documentation:** https://project-osrm.org/docs/v5.24.0/api/#table-service

**Description:** The OSRM Table service computes duration or distance matrices for sets of coordinates on a road network.

**Capabilities:**
- **Input:** List of coordinates (longitude, latitude pairs)
- **Output:** N×N matrix of shortest-path durations (seconds) and/or distances (meters)
- **Asymmetry:** Results are inherently asymmetric — d(A→B) ≠ d(B→A) due to one-way streets, turn restrictions, and road network topology
- **Profiles:** Car, bicycle, foot (different speed profiles and road access rules)
- **Scaling:** Can handle matrices up to ~10,000×10,000 on a well-provisioned server. Public demo server limited to ~100 coordinates.
- **Annotations:** Can return both `duration` and `distance` annotations

**Request Format:**
```
GET /table/v1/{profile}/{coordinates}?sources={indices}&destinations={indices}&annotations=duration,distance
```

**Response Format:** JSON with `durations` and `distances` as 2D arrays (null for unreachable pairs).

**Self-hosting:** Docker image available. Requires OSM PBF data preprocessing with `osrm-extract`, `osrm-partition`, `osrm-customize` (MLD) or `osrm-contract` (CH).

**Limitations:**
- No real-time traffic integration in open-source version
- Static cost model (based on OSM speed limits and road classifications)
- Public demo server has rate limits and size limits
- Large matrices require self-hosted instance

---

## 6. OSRM Trip API

**Documentation:** https://project-osrm.org/docs/v5.24.0/api/#trip-service

**Description:** The Trip service solves the TSP using a farthest-insertion heuristic on OSRM road-network data.

**Capabilities:**
- **Input:** List of coordinates
- **Output:** Optimized round-trip visiting all coordinates
- **Algorithm:** Farthest-insertion construction heuristic (no local search improvement)
- **Constraints:** Can fix start/end points; can handle round trips or point-to-point

**Limitations:**
- Solution quality is basic — typically 5–15% above optimal
- No local search improvement after construction
- Limited to a few hundred coordinates on public server
- Not suitable as a competitive TSP solver, but useful as a fast baseline

---

## 7. OSMnx Library for Graph Extraction

**Source:** Geoff Boeing, University of Southern California
**URL:** https://github.com/gboeing/osmnx
**PyPI:** `pip install osmnx`

**Description:** Python package for downloading and analyzing OpenStreetMap street networks as NetworkX graphs. Provides a complete pipeline from geographic query to graph analysis.

**Capabilities:**
- **Graph download:** Retrieve street network for any city, region, or bounding box
- **Network types:** Drive, walk, bike, all (configurable)
- **Graph representation:** NetworkX MultiDiGraph with node attributes (lat, lon, osmid) and edge attributes (length, maxspeed, highway type, oneway, name, geometry)
- **Routing:** Built-in shortest path computation
- **Speed/travel time:** Can impute travel times based on road type and speed limits
- **Simplification:** Topology simplification for graph analysis
- **Visualization:** Built-in plotting with matplotlib

**Data Format:** NetworkX graph objects. Can export to GeoPackage, Shapefile, GraphML.

**Relevance:** Enables generating road-network graphs with rich edge attributes for any metro area without needing a self-hosted OSRM instance. Can compute node features (degree, betweenness centrality) and edge features (length, speed, road type) needed for GNN training.

**Limitations:**
- Shortest-path routing is slower than OSRM (no contraction hierarchies)
- No turn costs or turn restrictions in the basic graph model
- Speed imputation is approximate (based on highway classification, not real traffic)

**Reference:** Boeing (2017) [boeing2017osmnx].

---

## 8. Real-World Road Network Sources

### 8.1 Geofabrik OpenStreetMap Extracts

**URL:** https://download.geofabrik.de/
**Format:** `.osm.pbf` (Protocolbuffer Binary Format)

**Description:** Daily-updated country and region-level OSM data extracts. The most widely used source for bulk OSM data downloads.

**Coverage:** Every country and most administrative subdivisions worldwide.

**Relevant Metro Area Data:**
- **New York City:** Available via `north-america/us/new-york-latest.osm.pbf` (New York State, ~700 MB). Manhattan can be clipped with osmium or osmconvert.
- **London:** Available via `europe/great-britain/england/greater-london-latest.osm.pbf` (~120 MB)
- **Berlin:** Available via `europe/germany/berlin-latest.osm.pbf` (~60 MB)
- **Tokyo:** Available via `asia/japan/kanto-latest.osm.pbf` (Kanto region, ~400 MB)

**Usage for Our Project:** Download PBF files → preprocess with OSRM for Table API, or load directly with OSMnx.

### 8.2 Interline/Transitland OSM Extracts

**URL:** https://app.interline.io/osm_extracts/interactive_view

**Description:** City and metro-area sized OSM extracts, updated daily. Provides pre-clipped metro area data that is more convenient than extracting from country-level Geofabrik files.

**Format:** PBF, GeoJSON

**Coverage:** Major metro areas worldwide. More granular than Geofabrik for city-level data.

### 8.3 BBBike Extracts

**URL:** https://extract.bbbike.org/

**Description:** Custom bounding box extracts from OSM. Users can draw a polygon and get an extract in PBF, Shapefile, or other formats.

---

## Data Pipeline Architecture for Our Project

```
OSM PBF Data (Geofabrik)
    ├── osmnx → NetworkX Graph → Node/Edge Features → GNN Training Data
    └── OSRM Preprocessing → OSRM Server
            ├── Table API → Asymmetric Duration/Distance Matrices → Benchmark Instances
            └── Trip API → Baseline Tour (farthest-insertion)
```

**Offline Approach (used in this project):**
Since we cannot host an OSRM server in this environment, we use OSMnx to:
1. Download road network graphs for target metro areas
2. Compute shortest-path travel times using NetworkX (Dijkstra's algorithm)
3. Generate asymmetric cost matrices by computing all-pairs shortest paths on the directed road graph
4. Extract node features (coordinates, degree, centrality) and edge features (length, speed, road type)

This approach produces realistically asymmetric cost matrices that reflect one-way streets, road hierarchy, and network topology, though without OSRM's turn-cost modeling and contraction-hierarchy speed.

---

## Summary Table

| Dataset/Source | Type | Size Range | Asymmetric | Format | Access |
|---------------|------|-----------|-----------|--------|--------|
| TSPLIB95 ATSP | Benchmark | 17–443 nodes | Yes | TSPLIB (.atsp) | Free download |
| DIMACS ATSP | Benchmark | 10s–100s nodes | Yes | TSPLIB-compatible | Free download |
| Waterloo TSP | Benchmark | 100s–744K nodes | Mostly symmetric | TSPLIB (.tsp) | Free download |
| Ascheuer TSPTW | Benchmark (industrial) | 17–233 nodes | Yes + time windows | Custom/standardized | Free download |
| OSRM Table API | Live computation | Up to ~10K×10K | Yes (road network) | JSON | Self-host or public server |
| OSRM Trip API | TSP baseline | Up to ~500 | Yes (road network) | JSON | Self-host or public server |
| OSMnx | Graph extraction | Any metro area | Yes (directed graph) | NetworkX graph | Free (Python library) |
| Geofabrik | Raw OSM data | Country/region | N/A (raw) | PBF | Free download |
| Interline | Metro OSM data | City-level | N/A (raw) | PBF/GeoJSON | Free |
