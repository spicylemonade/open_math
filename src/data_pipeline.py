"""
Data pipeline for generating asymmetric distance/duration matrices
from road network data. Supports:
  1. OSRM Table API (when OSRM server is available)
  2. Offline OSMnx graph-based computation
  3. Synthetic road-network-like graph generation (fallback)
"""

import json
import hashlib
import os
import numpy as np
import networkx as nx
from pathlib import Path

# Try importing osmnx; fall back to synthetic if unavailable
try:
    import osmnx as ox
    HAS_OSMNX = True
except ImportError:
    HAS_OSMNX = False

# Try importing requests for OSRM API
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42


def _cache_key(city_name: str, n_points: int, seed: int) -> str:
    """Generate a deterministic cache key."""
    raw = f"{city_name}_{n_points}_{seed}"
    return hashlib.md5(raw.encode()).hexdigest()


def query_osrm_table(coordinates: list, profile: str = "driving",
                     server_url: str = "http://router.project-osrm.org") -> dict:
    """
    Query OSRM Table API to produce asymmetric NxN duration and distance matrices.

    Parameters
    ----------
    coordinates : list of (lon, lat) tuples
    profile : str, one of 'driving', 'walking', 'cycling'
    server_url : str, OSRM server base URL

    Returns
    -------
    dict with keys 'durations' (NxN array, seconds) and 'distances' (NxN array, meters)
    """
    if not HAS_REQUESTS:
        raise ImportError("requests library required for OSRM API queries")

    coords_str = ";".join(f"{lon},{lat}" for lon, lat in coordinates)
    url = f"{server_url}/table/v1/{profile}/{coords_str}"
    params = {"annotations": "duration,distance"}

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    data = response.json()

    if data.get("code") != "Ok":
        raise RuntimeError(f"OSRM error: {data.get('message', 'unknown')}")

    durations = np.array(data["durations"], dtype=np.float64)
    distances = np.array(data["distances"], dtype=np.float64)

    return {"durations": durations, "distances": distances}


def generate_from_osmnx(city_name: str, n_points: int, seed: int = SEED,
                        network_type: str = "drive") -> dict:
    """
    Generate asymmetric cost matrices from an OSMnx road network graph.

    Downloads the road network for the given city, samples n_points random
    nodes, and computes all-pairs shortest path durations and distances
    on the directed graph.

    Parameters
    ----------
    city_name : str, e.g. "Manhattan, New York, USA"
    n_points : int, number of stops to sample
    seed : int, random seed for reproducibility
    network_type : str, one of 'drive', 'walk', 'bike', 'all'

    Returns
    -------
    dict with keys:
        'durations': NxN numpy array (seconds)
        'distances': NxN numpy array (meters)
        'coordinates': list of (lat, lon) tuples
        'node_ids': list of OSM node IDs
        'metadata': dict with city, seed, n_points, etc.
    """
    if not HAS_OSMNX:
        raise ImportError("osmnx required for graph-based pipeline")

    rng = np.random.RandomState(seed)

    # Download road network
    G = ox.graph_from_place(city_name, network_type=network_type)
    G = ox.routing.add_edge_speeds(G)
    G = ox.routing.add_edge_travel_times(G)

    # Sample random nodes
    all_nodes = list(G.nodes())
    if len(all_nodes) < n_points:
        raise ValueError(f"Graph has only {len(all_nodes)} nodes, need {n_points}")
    sampled = rng.choice(all_nodes, size=n_points, replace=False)

    # Get coordinates
    coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in sampled]

    # Compute all-pairs shortest paths for duration and distance
    n = len(sampled)
    durations = np.full((n, n), np.inf)
    distances = np.full((n, n), np.inf)

    for i, src in enumerate(sampled):
        try:
            dur_paths = nx.single_source_dijkstra_path_length(G, src, weight="travel_time")
            dist_paths = nx.single_source_dijkstra_path_length(G, src, weight="length")
        except nx.NetworkXError:
            continue
        for j, dst in enumerate(sampled):
            if i == j:
                durations[i, j] = 0.0
                distances[i, j] = 0.0
            elif dst in dur_paths:
                durations[i, j] = dur_paths[dst]
                distances[i, j] = dist_paths.get(dst, np.inf)

    # Replace inf with large value (unreachable pairs)
    max_dur = np.max(durations[np.isfinite(durations)]) if np.any(np.isfinite(durations)) else 1e6
    max_dist = np.max(distances[np.isfinite(distances)]) if np.any(np.isfinite(distances)) else 1e6
    durations[~np.isfinite(durations)] = max_dur * 10
    distances[~np.isfinite(distances)] = max_dist * 10

    metadata = {
        "city": city_name,
        "n_points": n_points,
        "seed": seed,
        "network_type": network_type,
        "source": "osmnx",
        "n_graph_nodes": len(all_nodes),
        "n_graph_edges": G.number_of_edges(),
    }

    return {
        "durations": durations,
        "distances": distances,
        "coordinates": coords,
        "node_ids": sampled.tolist(),
        "metadata": metadata,
    }


def generate_synthetic_road_network(n_points: int, city_name: str = "synthetic",
                                     seed: int = SEED,
                                     area_km: float = 10.0) -> dict:
    """
    Generate a synthetic road-network-like graph with realistic asymmetry.

    Creates a grid-based road network with:
    - Randomly placed one-way streets (~20% of edges)
    - Road hierarchy (highways faster than local roads)
    - Turn penalties (asymmetry from route structure)
    - Realistic speed variation by road type

    Parameters
    ----------
    n_points : int, number of stops (delivery locations)
    city_name : str, label for the instance
    seed : int, random seed
    area_km : float, side length of the square area in km

    Returns
    -------
    dict with same structure as generate_from_osmnx
    """
    rng = np.random.RandomState(seed)

    # Generate road network as a grid with perturbations
    grid_size = max(int(np.sqrt(n_points * 10)), 20)
    spacing = area_km / grid_size  # km between grid intersections

    # Create directed grid graph
    G = nx.DiGraph()
    node_pos = {}
    node_id = 0
    for i in range(grid_size):
        for j in range(grid_size):
            # Perturb positions slightly
            x = i * spacing + rng.normal(0, spacing * 0.1)
            y = j * spacing + rng.normal(0, spacing * 0.1)
            G.add_node(node_id, x=x, y=y)
            node_pos[node_id] = (x, y)
            node_id += 1

    # Add edges (grid connectivity + some diagonals)
    for i in range(grid_size):
        for j in range(grid_size):
            nid = i * grid_size + j
            neighbors = []
            if i + 1 < grid_size:
                neighbors.append((i + 1) * grid_size + j)
            if j + 1 < grid_size:
                neighbors.append(i * grid_size + (j + 1))
            if i - 1 >= 0:
                neighbors.append((i - 1) * grid_size + j)
            if j - 1 >= 0:
                neighbors.append(i * grid_size + (j - 1))
            # Occasional diagonals (highway shortcuts)
            if i + 1 < grid_size and j + 1 < grid_size and rng.random() < 0.1:
                neighbors.append((i + 1) * grid_size + (j + 1))
            if i - 1 >= 0 and j - 1 >= 0 and rng.random() < 0.1:
                neighbors.append((i - 1) * grid_size + (j - 1))

            for nbr in neighbors:
                pos_a = node_pos[nid]
                pos_b = node_pos[nbr]
                dist_km = np.sqrt((pos_a[0] - pos_b[0])**2 + (pos_a[1] - pos_b[1])**2)
                dist_m = dist_km * 1000

                # Assign road type with hierarchy
                is_diagonal = abs(nid // grid_size - nbr // grid_size) == 1 and abs(nid % grid_size - nbr % grid_size) == 1
                if is_diagonal:
                    speed_kph = rng.uniform(60, 100)  # Highway
                    road_type = "highway"
                elif i % 5 == 0 or j % 5 == 0:
                    speed_kph = rng.uniform(40, 60)  # Arterial
                    road_type = "arterial"
                else:
                    speed_kph = rng.uniform(20, 40)  # Local
                    road_type = "local"

                travel_time_s = (dist_km / speed_kph) * 3600

                # One-way streets: ~20% of local roads are one-way
                is_oneway = road_type == "local" and rng.random() < 0.2

                G.add_edge(nid, nbr, length=dist_m, travel_time=travel_time_s,
                          speed=speed_kph, road_type=road_type)
                if not is_oneway:
                    # Reverse edge with slightly different speed (asymmetry)
                    reverse_speed = speed_kph * rng.uniform(0.85, 1.15)
                    reverse_time = (dist_km / reverse_speed) * 3600
                    G.add_edge(nbr, nid, length=dist_m, travel_time=reverse_time,
                              speed=reverse_speed, road_type=road_type)

    # Sample n_points random delivery stops from graph nodes
    all_nodes = list(G.nodes())
    sampled = rng.choice(all_nodes, size=min(n_points, len(all_nodes)), replace=False)
    n = len(sampled)

    # Compute all-pairs shortest paths
    durations = np.full((n, n), np.inf)
    distances = np.full((n, n), np.inf)

    for i, src in enumerate(sampled):
        try:
            dur_paths = nx.single_source_dijkstra_path_length(G, src, weight="travel_time")
            dist_paths = nx.single_source_dijkstra_path_length(G, src, weight="length")
        except nx.NetworkXError:
            continue
        for j, dst in enumerate(sampled):
            if i == j:
                durations[i, j] = 0.0
                distances[i, j] = 0.0
            elif dst in dur_paths:
                durations[i, j] = dur_paths[dst]
                distances[i, j] = dist_paths.get(dst, np.inf)

    # Replace inf with large value
    finite_dur = durations[np.isfinite(durations)]
    finite_dist = distances[np.isfinite(distances)]
    max_dur = np.max(finite_dur) if len(finite_dur) > 0 else 1e6
    max_dist = np.max(finite_dist) if len(finite_dist) > 0 else 1e6
    durations[~np.isfinite(durations)] = max_dur * 10
    distances[~np.isfinite(distances)] = max_dist * 10

    # Generate lat/lon-like coordinates for compatibility
    base_lat, base_lon = 40.75, -73.98  # Manhattan-like
    coords = []
    for nid in sampled:
        x, y = node_pos[nid]
        lat = base_lat + (x / 111.0)
        lon = base_lon + (y / (111.0 * np.cos(np.radians(base_lat))))
        coords.append((lat, lon))

    metadata = {
        "city": city_name,
        "n_points": n,
        "seed": seed,
        "source": "synthetic",
        "area_km": area_km,
        "grid_size": grid_size,
        "n_graph_nodes": len(all_nodes),
        "n_graph_edges": G.number_of_edges(),
        "oneway_fraction": 0.2,
    }

    return {
        "durations": durations,
        "distances": distances,
        "coordinates": coords,
        "node_ids": sampled.tolist(),
        "metadata": metadata,
    }


def save_instance(data: dict, filepath: str) -> None:
    """Save instance data to disk in .npz format with JSON metadata."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        str(path),
        durations=data["durations"],
        distances=data["distances"],
    )

    meta_path = path.with_suffix(".json")
    meta = {
        "coordinates": data["coordinates"],
        "node_ids": data.get("node_ids", []),
        "metadata": data["metadata"],
        "n": len(data["coordinates"]),
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, default=str)


def load_instance(filepath: str) -> dict:
    """Load instance data from disk."""
    path = Path(filepath)
    npz_path = path.with_suffix(".npz")
    meta_path = path.with_suffix(".json")

    arrays = np.load(str(npz_path))
    with open(meta_path, "r") as f:
        meta = json.load(f)

    return {
        "durations": arrays["durations"],
        "distances": arrays["distances"],
        "coordinates": meta["coordinates"],
        "node_ids": meta.get("node_ids", []),
        "metadata": meta["metadata"],
    }


def generate_instance(city_name: str, n_points: int, seed: int = SEED,
                      method: str = "auto") -> dict:
    """
    High-level function to generate a road-network ATSP instance.

    Parameters
    ----------
    city_name : str, city name or 'synthetic_<name>'
    n_points : int, number of stops
    seed : int, random seed
    method : str, one of 'osmnx', 'osrm', 'synthetic', 'auto'

    Returns
    -------
    dict with durations, distances, coordinates, metadata
    """
    # Check cache
    cache_key = _cache_key(city_name, n_points, seed)
    cache_path = CACHE_DIR / cache_key
    if cache_path.with_suffix(".npz").exists():
        return load_instance(str(cache_path))

    if method == "auto":
        if city_name.startswith("synthetic"):
            method = "synthetic"
        elif HAS_OSMNX:
            method = "osmnx"
        else:
            method = "synthetic"

    if method == "synthetic":
        area_map = {
            "synthetic_manhattan": 6.0,
            "synthetic_london": 8.0,
            "synthetic_berlin": 10.0,
        }
        area = area_map.get(city_name, 8.0)
        data = generate_synthetic_road_network(n_points, city_name, seed, area)
    elif method == "osmnx":
        data = generate_from_osmnx(city_name, n_points, seed)
    elif method == "osrm":
        raise NotImplementedError("OSRM method requires running OSRM server")
    else:
        raise ValueError(f"Unknown method: {method}")

    # Cache
    save_instance(data, str(cache_path))

    return data


# ── Unit tests ────────────────────────────────────────────────────────────

def test_matrix_asymmetry():
    """Test that generated matrices are asymmetric."""
    data = generate_synthetic_road_network(20, "test_city", seed=42, area_km=5.0)
    dur = data["durations"]
    # Check asymmetry: at least some off-diagonal entries differ
    diff = np.abs(dur - dur.T)
    np.fill_diagonal(diff, 0)
    n_asymmetric = np.sum(diff > 1e-6)
    assert n_asymmetric > 0, "Duration matrix should be asymmetric"
    print(f"  PASS: {n_asymmetric} asymmetric pairs out of {dur.shape[0]*(dur.shape[0]-1)}")


def test_matrix_dimensions():
    """Test that matrices have correct dimensions."""
    n = 30
    data = generate_synthetic_road_network(n, "test_dim", seed=42)
    assert data["durations"].shape == (n, n), f"Expected ({n},{n}), got {data['durations'].shape}"
    assert data["distances"].shape == (n, n), f"Expected ({n},{n}), got {data['distances'].shape}"
    assert len(data["coordinates"]) == n, f"Expected {n} coordinates, got {len(data['coordinates'])}"
    print(f"  PASS: All matrices are {n}x{n}, {n} coordinates")


def test_diagonal_zero():
    """Test that diagonal entries are zero (self-loops cost nothing)."""
    data = generate_synthetic_road_network(25, "test_diag", seed=42)
    diag_dur = np.diag(data["durations"])
    diag_dist = np.diag(data["distances"])
    assert np.allclose(diag_dur, 0), "Diagonal of duration matrix should be 0"
    assert np.allclose(diag_dist, 0), "Diagonal of distance matrix should be 0"
    print("  PASS: Diagonal entries are all zero")


def test_save_load_roundtrip():
    """Test saving and loading preserves data."""
    data = generate_synthetic_road_network(15, "test_save", seed=42, area_km=3.0)
    path = "data/cache/test_roundtrip"
    save_instance(data, path)
    loaded = load_instance(path)
    assert np.allclose(data["durations"], loaded["durations"]), "Durations differ after roundtrip"
    assert np.allclose(data["distances"], loaded["distances"]), "Distances differ after roundtrip"
    for a, b in zip(data["coordinates"], loaded["coordinates"]):
        assert abs(a[0] - b[0]) < 1e-10 and abs(a[1] - b[1]) < 1e-10, "Coordinates differ"
    # Cleanup
    os.remove(f"{path}.npz")
    os.remove(f"{path}.json")
    print("  PASS: Save/load roundtrip preserves data")


if __name__ == "__main__":
    print("Running data_pipeline unit tests...")
    test_matrix_asymmetry()
    test_matrix_dimensions()
    test_diagonal_zero()
    test_save_load_roundtrip()
    print("\nAll tests passed!")
