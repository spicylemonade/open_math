"""
Generate benchmark instance suite for road-network ATSP experiments.

Creates instances across 3 scales (50, 200, 1000 stops) from 3 metro areas
(Manhattan, London, Berlin) using synthetic road network generation.
"""

import sys
import os
import json
import time
import signal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_pipeline import generate_synthetic_road_network, save_instance

# Timeout handler
class ComputeTimeout(Exception):
    pass

def _handler(signum, frame):
    raise ComputeTimeout()

signal.signal(signal.SIGALRM, _handler)

# City configurations
CITIES = {
    "manhattan": {"area_km": 6.0, "base_lat": 40.758, "base_lon": -73.985},
    "london": {"area_km": 8.0, "base_lat": 51.509, "base_lon": -0.118},
    "berlin": {"area_km": 10.0, "base_lat": 52.520, "base_lon": 13.405},
}

SCALES = [50, 200, 1000]
SEEDS = [42]  # Single seed for benchmark generation; solver seeds vary

BENCHMARK_DIR = "benchmarks"
os.makedirs(BENCHMARK_DIR, exist_ok=True)


def generate_all():
    instances = []
    for city_name, config in CITIES.items():
        for n_stops in SCALES:
            for seed in SEEDS:
                instance_id = f"{city_name}_{n_stops}_s{seed}"
                filepath = os.path.join(BENCHMARK_DIR, instance_id)

                print(f"Generating {instance_id}...", end=" ", flush=True)
                t0 = time.time()

                # Set timeout: 5 min for large, 2 min for medium, 30s for small
                timeout = {50: 60, 200: 180, 1000: 600}.get(n_stops, 300)
                signal.alarm(timeout)

                try:
                    data = generate_synthetic_road_network(
                        n_points=n_stops,
                        city_name=f"synthetic_{city_name}",
                        seed=seed,
                        area_km=config["area_km"],
                    )
                    signal.alarm(0)

                    # Verify asymmetry
                    import numpy as np
                    dur = data["durations"]
                    diff = np.abs(dur - dur.T)
                    np.fill_diagonal(diff, 0)
                    n_asym = int(np.sum(diff > 1e-6))
                    asym_ratio = n_asym / (dur.shape[0] * (dur.shape[0] - 1))

                    save_instance(data, filepath)
                    elapsed = time.time() - t0

                    info = {
                        "instance_id": instance_id,
                        "city": city_name,
                        "n_stops": n_stops,
                        "seed": seed,
                        "area_km": config["area_km"],
                        "asymmetric_pairs_fraction": round(asym_ratio, 4),
                        "generation_time_s": round(elapsed, 2),
                        "source": "synthetic_road_network",
                    }
                    instances.append(info)
                    print(f"done ({elapsed:.1f}s, {asym_ratio:.1%} asymmetric)")

                except ComputeTimeout:
                    signal.alarm(0)
                    print(f"TIMEOUT after {timeout}s - skipping")
                    instances.append({
                        "instance_id": instance_id,
                        "city": city_name,
                        "n_stops": n_stops,
                        "seed": seed,
                        "status": "timeout",
                    })
                except Exception as e:
                    signal.alarm(0)
                    print(f"ERROR: {e}")
                    instances.append({
                        "instance_id": instance_id,
                        "city": city_name,
                        "n_stops": n_stops,
                        "seed": seed,
                        "status": "error",
                        "error": str(e),
                    })

    # Also generate extra instances with different seeds for 200-stop
    extra_seeds = [123, 456, 789, 1024]
    for city_name, config in CITIES.items():
        for seed in extra_seeds:
            instance_id = f"{city_name}_200_s{seed}"
            filepath = os.path.join(BENCHMARK_DIR, instance_id)

            if os.path.exists(filepath + ".npz"):
                continue

            print(f"Generating extra {instance_id}...", end=" ", flush=True)
            t0 = time.time()
            signal.alarm(180)

            try:
                data = generate_synthetic_road_network(
                    n_points=200,
                    city_name=f"synthetic_{city_name}",
                    seed=seed,
                    area_km=config["area_km"],
                )
                signal.alarm(0)

                import numpy as np
                dur = data["durations"]
                diff = np.abs(dur - dur.T)
                np.fill_diagonal(diff, 0)
                n_asym = int(np.sum(diff > 1e-6))
                asym_ratio = n_asym / (dur.shape[0] * (dur.shape[0] - 1))

                save_instance(data, filepath)
                elapsed = time.time() - t0

                info = {
                    "instance_id": instance_id,
                    "city": city_name,
                    "n_stops": 200,
                    "seed": seed,
                    "area_km": config["area_km"],
                    "asymmetric_pairs_fraction": round(asym_ratio, 4),
                    "generation_time_s": round(elapsed, 2),
                    "source": "synthetic_road_network",
                }
                instances.append(info)
                print(f"done ({elapsed:.1f}s)")

            except (ComputeTimeout, Exception) as e:
                signal.alarm(0)
                print(f"FAILED: {e}")

    # Save instance catalog
    catalog_path = os.path.join(BENCHMARK_DIR, "instance_catalog.json")
    with open(catalog_path, "w") as f:
        json.dump(instances, f, indent=2)

    print(f"\nGenerated {len([i for i in instances if 'status' not in i])} instances")
    print(f"Catalog saved to {catalog_path}")

    return instances


if __name__ == "__main__":
    generate_all()
