"""Generate benchmark planar graph instances."""

import os
import sys
import json
import math
import signal
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph import (
    generate_grid_graph, generate_random_planar_graph,
    generate_delaunay_planar_graph, save_pace_format,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


class Timeout(Exception):
    pass

def _handler(signum, frame):
    raise Timeout()


def generate_all_instances():
    os.makedirs(DATA_DIR, exist_ok=True)

    instances = []

    def add_instance(name, gen_func, *args, **kwargs):
        filepath = os.path.join(DATA_DIR, f"{name}.gr")
        signal.signal(signal.SIGALRM, _handler)
        signal.alarm(120)
        try:
            g = gen_func(*args, **kwargs)
            signal.alarm(0)
            save_pace_format(g, filepath)
            instances.append({
                'name': name,
                'n': g.n,
                'm': g.m,
                'type': name.split('_n')[0],
                'path': os.path.abspath(filepath),
            })
            print(f"  {name}: n={g.n}, m={g.m}")
        except Timeout:
            signal.alarm(0)
            print(f"  TIMEOUT generating {name}, skipping")

    # Grid graphs
    for size in [50, 100, 500, 1000, 5000, 10000]:
        rows = int(math.sqrt(size))
        cols = size // rows
        for t in range(2):
            r = rows + t
            c = max(1, size // r)
            name = f"grid_n{r*c}_t{t}"
            add_instance(name, generate_grid_graph, r, c)

    # Delaunay graphs
    for size in [50, 100, 500, 1000, 5000, 10000]:
        for t in range(2):
            seed = 42 + t
            name = f"delaunay_n{size}_t{t}"
            add_instance(name, generate_delaunay_planar_graph, size, seed=seed)

    # Random planar graphs
    for size in [50, 100, 500, 1000, 5000, 10000]:
        for t in range(2):
            seed = 42 + t
            name = f"random_planar_n{size}_t{t}"
            add_instance(name, generate_random_planar_graph, size, seed=seed)

    # Save manifest
    manifest_path = os.path.join(DATA_DIR, 'manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(instances, f, indent=2)
    print(f"\nGenerated {len(instances)} instances total.")
    return instances


if __name__ == '__main__':
    generate_all_instances()
