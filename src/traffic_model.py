"""
Traffic-aware and time-dependent cost model for road-network ATSP.

Models time-dependent edge costs using piecewise-linear speed profiles
per road type: peak morning, off-peak, peak evening, night.
"""

import numpy as np
from typing import List, Tuple, Optional


# Time-of-day periods (hours from midnight)
PERIODS = {
    "night":         (0, 6),     # 00:00-06:00
    "morning_peak":  (6, 9),     # 06:00-09:00
    "midday":        (9, 16),    # 09:00-16:00
    "evening_peak":  (16, 19),   # 16:00-19:00
    "evening":       (19, 24),   # 19:00-24:00
}

# Speed multipliers by road type and time period
# (relative to free-flow speed)
TRAFFIC_PROFILES = {
    "highway": {
        "night": 1.0,
        "morning_peak": 0.55,
        "midday": 0.85,
        "evening_peak": 0.50,
        "evening": 0.90,
    },
    "arterial": {
        "night": 1.0,
        "morning_peak": 0.45,
        "midday": 0.75,
        "evening_peak": 0.40,
        "evening": 0.80,
    },
    "local": {
        "night": 1.0,
        "morning_peak": 0.70,
        "midday": 0.90,
        "evening_peak": 0.65,
        "evening": 0.95,
    },
}


def get_period(hour: float) -> str:
    """Get the traffic period for a given hour of day."""
    hour = hour % 24
    for period, (start, end) in PERIODS.items():
        if start <= hour < end:
            return period
    return "night"


def get_speed_multiplier(road_type: str, hour: float) -> float:
    """Get the speed multiplier for a given road type and hour."""
    period = get_period(hour)
    profile = TRAFFIC_PROFILES.get(road_type, TRAFFIC_PROFILES["local"])
    return profile[period]


def generate_traffic_multipliers(n_edges: int, seed: int = 42) -> dict:
    """
    Generate synthetic but realistic traffic multiplier arrays for edges.

    Returns a dict mapping period name to array of multipliers per edge.
    Each edge gets a road type assignment and corresponding traffic profile
    with some random perturbation.
    """
    rng = np.random.RandomState(seed)

    # Assign road types: 10% highway, 30% arterial, 60% local
    road_types = rng.choice(
        ["highway", "arterial", "local"],
        size=n_edges,
        p=[0.1, 0.3, 0.6],
    )

    multipliers = {}
    for period in PERIODS:
        mults = np.ones(n_edges)
        for i, rt in enumerate(road_types):
            base = TRAFFIC_PROFILES[rt][period]
            # Add random perturbation (±10%)
            mults[i] = base * rng.uniform(0.9, 1.1)
        multipliers[period] = mults

    return {"multipliers": multipliers, "road_types": road_types}


def compute_time_dependent_cost(base_cost_matrix: np.ndarray,
                                 departure_hour: float,
                                 traffic_data: dict = None,
                                 seed: int = 42) -> np.ndarray:
    """
    Compute time-dependent cost matrix for a given departure time.

    Parameters
    ----------
    base_cost_matrix : (N, N) baseline duration matrix (free-flow or average)
    departure_hour : float, hour of day (0-24)
    traffic_data : dict with 'multipliers' and 'road_types', or None to generate
    seed : int, random seed for traffic generation

    Returns
    -------
    (N, N) duration matrix adjusted for traffic at departure_hour
    """
    n = base_cost_matrix.shape[0]

    if traffic_data is None:
        traffic_data = generate_traffic_multipliers(n * n, seed=seed)

    period = get_period(departure_hour)
    mults = traffic_data["multipliers"][period]

    # Reshape multipliers to match matrix (fill edge-by-edge)
    mult_matrix = mults[:n * n].reshape(n, n)

    # Duration increases as speed decreases: new_time = base_time / speed_multiplier
    adjusted = base_cost_matrix / mult_matrix
    np.fill_diagonal(adjusted, 0)

    return adjusted


def compute_departure_time_aware_tour_cost(
    base_cost_matrix: np.ndarray,
    tour: List[int],
    departure_hour: float = 8.0,
    service_time: float = 300.0,
    traffic_data: dict = None,
    seed: int = 42,
) -> Tuple[float, List[float]]:
    """
    Compute tour cost with departure-time-dependent costs.

    At each stop, the arrival time determines the traffic conditions
    for the next edge.

    Parameters
    ----------
    base_cost_matrix : (N, N) free-flow duration matrix (seconds)
    tour : ordered list of node indices
    departure_hour : starting hour of day
    service_time : time spent at each stop (seconds)
    traffic_data : pre-computed traffic data
    seed : random seed

    Returns
    -------
    total_cost : float (seconds)
    arrival_times : list of arrival hours at each stop
    """
    n = len(tour)
    n_nodes = base_cost_matrix.shape[0]

    if traffic_data is None:
        traffic_data = generate_traffic_multipliers(n_nodes * n_nodes, seed=seed)

    current_time_hours = departure_hour
    total_cost = 0.0
    arrival_times = [departure_hour]

    for i in range(n):
        src = tour[i]
        dst = tour[(i + 1) % n]

        # Get traffic multiplier for current time
        period = get_period(current_time_hours)
        edge_idx = src * n_nodes + dst
        if edge_idx < len(traffic_data["multipliers"][period]):
            mult = traffic_data["multipliers"][period][edge_idx]
        else:
            mult = 1.0

        # Compute travel time
        base_time = base_cost_matrix[src, dst]
        actual_time = base_time / mult  # Duration increases as speed decreases

        total_cost += actual_time
        current_time_hours += actual_time / 3600.0  # Convert seconds to hours
        current_time_hours += service_time / 3600.0  # Service time at stop

        if i < n - 1:
            arrival_times.append(current_time_hours % 24)

    return total_cost, arrival_times


# ── Self-test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.data_pipeline import load_instance
    from src.baselines import solve, tour_cost

    print("Testing traffic model...")

    data = load_instance("benchmarks/manhattan_50_s42")
    cost_mat = data["durations"]
    tour, static_cost = solve(cost_mat, "ortools", time_limit_s=5, seed=42)

    # Generate traffic data
    n = cost_mat.shape[0]
    traffic_data = generate_traffic_multipliers(n * n, seed=42)

    # Test different departure times
    print(f"\nStatic tour cost: {static_cost:.1f}s")
    for hour in [3.0, 8.0, 12.0, 17.0, 21.0]:
        td_cost, arrivals = compute_departure_time_aware_tour_cost(
            cost_mat, tour, departure_hour=hour,
            service_time=0, traffic_data=traffic_data
        )
        ratio = td_cost / static_cost
        period = get_period(hour)
        print(f"  Departure {hour:5.1f}h ({period:15s}): cost={td_cost:10.1f}s  ratio={ratio:.3f}")

    # Check that peak vs off-peak differs by >= 10%
    night_cost, _ = compute_departure_time_aware_tour_cost(
        cost_mat, tour, departure_hour=3.0, service_time=0, traffic_data=traffic_data)
    peak_cost, _ = compute_departure_time_aware_tour_cost(
        cost_mat, tour, departure_hour=17.0, service_time=0, traffic_data=traffic_data)
    variation = abs(peak_cost - night_cost) / night_cost * 100
    print(f"\n  Peak vs night variation: {variation:.1f}%")
    assert variation >= 10, f"Expected >= 10% variation, got {variation:.1f}%"
    print("  PASS: Tour cost varies by >= 10% between peak and off-peak")
    print("\nTraffic model test passed!")
