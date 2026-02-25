# Benchmark Instance Suite

Asymmetric TSP instances derived from synthetic road networks modeling real metro areas.

## Instance Naming Convention

`{city}_{n_stops}_s{seed}` — e.g., `manhattan_200_s42`

## Instance Scales

| Scale | Stops | Instances per City | Total |
|-------|-------|--------------------|-------|
| Small | 50 | 1 (seed 42) | 3 |
| Medium | 200 | 5 (seeds 42, 123, 456, 789, 1024) | 15 |
| Large | 1000 | 1 (seed 42) | 3 |

**Total: 21 instances**

## Metro Areas

| City | Area (km²) | Grid Size | Road Network Properties |
|------|-----------|-----------|------------------------|
| Manhattan | 6×6 | ~20% one-way, dense grid | High asymmetry from one-way streets |
| London | 8×8 | ~20% one-way, irregular | Mixed road hierarchy |
| Berlin | 10×10 | ~20% one-way, sparse | Wide arterials, large blocks |

## File Format

Each instance consists of two files:
- `{id}.npz` — NumPy compressed archive with:
  - `durations`: N×N asymmetric duration matrix (seconds)
  - `distances`: N×N asymmetric distance matrix (meters)
- `{id}.json` — Metadata including:
  - `coordinates`: list of (lat, lon) tuples
  - `node_ids`: graph node IDs
  - `metadata`: generation parameters (city, seed, area, source)

## Key Properties

- **Asymmetry**: All matrices are asymmetric due to one-way streets and directional speed differences
- **Road hierarchy**: Highways (60-100 km/h), arterials (40-60 km/h), local roads (20-40 km/h)
- **One-way streets**: ~20% of local road edges are one-directional
- **Diagonal shortcuts**: ~10% probability of highway diagonal connections

## Loading in Python

```python
from src.data_pipeline import load_instance
data = load_instance("benchmarks/manhattan_200_s42")
durations = data["durations"]  # 200×200 asymmetric matrix
```

## Generation

```bash
python scripts/generate_benchmarks.py
```

Generated on 2026-02-25 using synthetic road-network model with fixed seeds for reproducibility.
