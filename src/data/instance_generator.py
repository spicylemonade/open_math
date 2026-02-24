"""
ATSP Instance Generator from OpenStreetMap Road Networks.

Generates asymmetric traveling salesman problem instances by:
1. Downloading road networks via OSMnx
2. Sampling random locations on the network
3. Computing asymmetric travel-time matrices via shortest paths
4. Outputting standardized JSON format
"""

import json
import time
import numpy as np
import networkx as nx

try:
    import osmnx as ox
    HAS_OSMNX = True
except ImportError:
    HAS_OSMNX = False


# City configurations: (lat, lon, radius_meters, topology_type)
CITY_CONFIGS = {
    "manhattan": (40.7580, -73.9855, 3000, "grid"),
    "paris": (48.8566, 2.3522, 3000, "radial"),
    "boston": (42.3601, -71.0589, 3000, "mixed"),
    "chicago": (41.8781, -87.6298, 3000, "grid"),
    "london": (51.5074, -0.1278, 3000, "mixed"),
}


def generate_instance_osmnx(city_name, n_nodes, seed=42, speed_kmh=30.0):
    """Generate an ATSP instance from a real road network using OSMnx.

    Parameters
    ----------
    city_name : str
        Name of the city (key in CITY_CONFIGS) or custom.
    n_nodes : int
        Number of locations (depot + customers).
    seed : int
        Random seed for reproducibility.
    speed_kmh : float
        Default travel speed in km/h for edges without speed data.

    Returns
    -------
    dict
        Instance dictionary with cost matrix, coordinates, and metadata.
    """
    if not HAS_OSMNX:
        raise ImportError("osmnx is required for real road network instances")

    rng = np.random.RandomState(seed)

    if city_name.lower() in CITY_CONFIGS:
        lat, lon, radius, topology = CITY_CONFIGS[city_name.lower()]
    else:
        raise ValueError(f"Unknown city: {city_name}. Available: {list(CITY_CONFIGS.keys())}")

    # Download road network - increase radius for larger instances
    adj_radius = max(radius, int(radius * (n_nodes / 50) ** 0.5))
    G = ox.graph_from_point((lat, lon), dist=adj_radius, network_type='drive')

    # Add travel time to edges
    G = ox.routing.add_edge_speeds(G)
    G = ox.routing.add_edge_travel_times(G)

    # Sample random nodes from the network
    all_nodes = list(G.nodes)
    if len(all_nodes) < n_nodes:
        raise ValueError(
            f"Network has only {len(all_nodes)} nodes, need {n_nodes}. "
            f"Try a larger radius or different city."
        )

    selected_indices = rng.choice(len(all_nodes), size=n_nodes, replace=False)
    selected_nodes = [all_nodes[i] for i in selected_indices]

    # Get coordinates
    coords = []
    for node in selected_nodes:
        data = G.nodes[node]
        coords.append((data['y'], data['x']))  # (lat, lon)

    # Compute asymmetric travel time matrix using shortest paths
    cost_matrix = np.full((n_nodes, n_nodes), np.inf)
    np.fill_diagonal(cost_matrix, 0.0)

    for i, src in enumerate(selected_nodes):
        try:
            lengths = nx.single_source_dijkstra_path_length(
                G, src, weight='travel_time'
            )
            for j, dst in enumerate(selected_nodes):
                if i != j and dst in lengths:
                    cost_matrix[i, j] = lengths[dst]
        except nx.NetworkXError:
            pass

    # Handle unreachable pairs: use large but finite cost
    max_finite = np.max(cost_matrix[np.isfinite(cost_matrix)])
    unreachable_mask = np.isinf(cost_matrix) & (np.eye(n_nodes) == 0)
    if unreachable_mask.any():
        cost_matrix[unreachable_mask] = max_finite * 3.0

    # Compute asymmetry metrics
    asym_ratios = []
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if cost_matrix[i, j] > 0 and cost_matrix[j, i] > 0:
                ratio = max(cost_matrix[i, j], cost_matrix[j, i]) / min(
                    cost_matrix[i, j], cost_matrix[j, i]
                )
                asym_ratios.append(ratio)

    instance = {
        "metadata": {
            "city": city_name,
            "n_nodes": n_nodes,
            "seed": seed,
            "topology": topology if city_name.lower() in CITY_CONFIGS else "unknown",
            "source": "osmnx",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "asymmetry_ratio_max": float(max(asym_ratios)) if asym_ratios else 1.0,
            "asymmetry_ratio_mean": float(np.mean(asym_ratios)) if asym_ratios else 1.0,
            "density": len(G.edges) / len(G.nodes) if len(G.nodes) > 0 else 0,
        },
        "coordinates": coords,
        "cost_matrix": cost_matrix.tolist(),
    }

    return instance


def generate_synthetic_instance(n_nodes, seed=42, city_name="synthetic",
                                topology="grid", asymmetry_level=0.15):
    """Generate a synthetic ATSP instance with road-network-like properties.

    Creates instances with realistic asymmetry from simulated one-way streets
    and varying road conditions.

    Parameters
    ----------
    n_nodes : int
        Number of locations.
    seed : int
        Random seed.
    city_name : str
        Name label for metadata.
    topology : str
        "grid", "radial", or "mixed".
    asymmetry_level : float
        Controls degree of asymmetry (0=symmetric, 1=highly asymmetric).

    Returns
    -------
    dict
        Instance dictionary.
    """
    rng = np.random.RandomState(seed)

    # Generate coordinates based on topology
    if topology == "grid":
        side = int(np.ceil(np.sqrt(n_nodes)))
        grid_x = np.linspace(0, 1, side)
        grid_y = np.linspace(0, 1, side)
        xx, yy = np.meshgrid(grid_x, grid_y)
        all_pts = np.column_stack([xx.ravel(), yy.ravel()])
        idx = rng.choice(len(all_pts), size=n_nodes, replace=False)
        coords_arr = all_pts[idx] + rng.normal(0, 0.02, (n_nodes, 2))
    elif topology == "radial":
        angles = rng.uniform(0, 2 * np.pi, n_nodes)
        radii = rng.exponential(0.3, n_nodes)
        coords_arr = np.column_stack([
            0.5 + radii * np.cos(angles),
            0.5 + radii * np.sin(angles),
        ])
    else:  # mixed
        n_grid = n_nodes // 2
        n_radial = n_nodes - n_grid
        side = int(np.ceil(np.sqrt(n_grid)))
        grid_x = np.linspace(0.0, 0.5, side)
        grid_y = np.linspace(0, 1, side)
        xx, yy = np.meshgrid(grid_x, grid_y)
        all_pts = np.column_stack([xx.ravel(), yy.ravel()])
        idx = rng.choice(len(all_pts), size=min(n_grid, len(all_pts)), replace=False)
        grid_coords = all_pts[idx] + rng.normal(0, 0.02, (len(idx), 2))

        angles = rng.uniform(0, 2 * np.pi, n_radial)
        radii = rng.exponential(0.2, n_radial)
        radial_coords = np.column_stack([
            0.75 + radii * np.cos(angles),
            0.5 + radii * np.sin(angles),
        ])
        coords_arr = np.vstack([grid_coords, radial_coords])
        if len(coords_arr) < n_nodes:
            extra = rng.uniform(0, 1, (n_nodes - len(coords_arr), 2))
            coords_arr = np.vstack([coords_arr, extra])
        coords_arr = coords_arr[:n_nodes]

    coords = [(float(c[0]), float(c[1])) for c in coords_arr]

    # Compute Euclidean distance matrix
    dist_matrix = np.zeros((n_nodes, n_nodes))
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:
                dx = coords_arr[i, 0] - coords_arr[j, 0]
                dy = coords_arr[i, 1] - coords_arr[j, 1]
                dist_matrix[i, j] = np.sqrt(dx * dx + dy * dy)

    # Add asymmetry to simulate one-way streets and varying conditions
    # 1. Random multiplicative asymmetry
    asym_noise = 1.0 + asymmetry_level * rng.standard_normal((n_nodes, n_nodes))
    asym_noise = np.clip(asym_noise, 0.5, 2.0)
    cost_matrix = dist_matrix * asym_noise

    # 2. Simulate some one-way preferences (add extra cost in one direction)
    n_oneway = int(0.1 * n_nodes * n_nodes)
    for _ in range(n_oneway):
        i, j = rng.randint(0, n_nodes, 2)
        if i != j:
            cost_matrix[i, j] *= (1.0 + rng.uniform(0.2, 0.8))

    # Scale to realistic travel times (seconds)
    # Assume coordinates span ~5km, speed ~30km/h
    scale_factor = 5000.0 / 30.0 * 3.6  # meters/speed = seconds
    cost_matrix *= scale_factor
    np.fill_diagonal(cost_matrix, 0.0)

    # Compute asymmetry metrics
    asym_ratios = []
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if cost_matrix[i, j] > 0 and cost_matrix[j, i] > 0:
                ratio = max(cost_matrix[i, j], cost_matrix[j, i]) / min(
                    cost_matrix[i, j], cost_matrix[j, i]
                )
                asym_ratios.append(ratio)

    instance = {
        "metadata": {
            "city": city_name,
            "n_nodes": n_nodes,
            "seed": seed,
            "topology": topology,
            "source": "synthetic",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "asymmetry_ratio_max": float(max(asym_ratios)) if asym_ratios else 1.0,
            "asymmetry_ratio_mean": float(np.mean(asym_ratios)) if asym_ratios else 1.0,
            "density": 0.0,
        },
        "coordinates": coords,
        "cost_matrix": cost_matrix.tolist(),
    }

    return instance


def save_instance(instance, filepath):
    """Save an instance to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(instance, f, indent=2)


def load_instance(filepath):
    """Load an instance from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def validate_instance(instance):
    """Validate instance format and data integrity."""
    assert "metadata" in instance
    assert "coordinates" in instance
    assert "cost_matrix" in instance

    n = instance["metadata"]["n_nodes"]
    matrix = np.array(instance["cost_matrix"])

    assert matrix.shape == (n, n), f"Matrix shape {matrix.shape} != ({n}, {n})"
    assert np.all(np.diag(matrix) == 0), "Diagonal must be zero"
    assert np.all(matrix >= 0), "Costs must be non-negative"
    assert len(instance["coordinates"]) == n

    return True


if __name__ == "__main__":
    import os

    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "benchmarks")
    os.makedirs(out_dir, exist_ok=True)

    # Try generating real instances; fall back to synthetic
    for city in ["manhattan", "boston", "paris"]:
        for n in [50, 100, 200]:
            fname = f"{city}_n{n}.json"
            fpath = os.path.join(out_dir, fname)
            print(f"Generating {fname}...")
            try:
                inst = generate_instance_osmnx(city, n, seed=42)
            except Exception as e:
                print(f"  OSMnx failed ({e}), using synthetic fallback")
                topo = CITY_CONFIGS.get(city, (0, 0, 0, "mixed"))[3]
                inst = generate_synthetic_instance(n, seed=42, city_name=city, topology=topo)

            validate_instance(inst)
            save_instance(inst, fpath)
            print(f"  Saved: {fname} (n={n}, asym_max={inst['metadata']['asymmetry_ratio_max']:.2f})")
