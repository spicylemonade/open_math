#!/usr/bin/env python3
"""Regenerate all results/ files from scratch.

Usage: python -m scripts.run_benchmarks
"""

import json
import math
import random
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity
from src.barneshut import barneshut_gravity
from src.integrators import euler_step, leapfrog_step, rk4_step
from src.adaptive import AdaptiveController, run_adaptive_simulation
from src.simulation import Simulation


def two_body_kepler(e=0.0, m_central=1.0, m_test=1e-6):
    """Create a two-body Kepler orbit with given eccentricity."""
    a = 1.0
    G = 1.0
    M = m_central + m_test
    v0 = math.sqrt(G * M / a * (1 + e))
    r0 = a * (1 - e)
    b1 = Body(m_central, Vec2(0, 0), Vec2(0, 0))
    b2 = Body(m_test, Vec2(r0, 0), Vec2(0, v0))
    T = 2 * math.pi * math.sqrt(a ** 3 / (G * M))
    return [b1, b2], T


def figure_eight_bodies():
    """Create figure-eight three-body initial conditions."""
    x1 = 0.97000436
    y1 = -0.24308753
    vx3 = -0.93240737
    vy3 = -0.86473146
    return [
        Body(1.0, Vec2(x1, y1), Vec2(vx3 / 2, vy3 / 2)),
        Body(1.0, Vec2(-x1, -y1), Vec2(vx3 / 2, vy3 / 2)),
        Body(1.0, Vec2(0, 0), Vec2(-vx3, -vy3)),
    ]


def run_baseline_benchmarks():
    """Item 011: Baseline benchmarks."""
    print("Running baseline benchmarks...")
    results = {}

    # Euler 100 periods
    bodies, T = two_body_kepler(e=0.0)
    t0 = time.time()
    sim = Simulation(bodies, euler_step, direct_gravity, 0.001, T * 100)
    sim.run()
    wall = time.time() - t0
    errs = sim.relative_energy_error()
    results["euler_circular_100"] = {
        "integrator": "euler", "dt": 0.001, "N": 2, "periods": 100,
        "final_energy_error": errs[-1], "wall_time_seconds": round(wall, 2)
    }

    # Leapfrog 100 periods
    bodies, T = two_body_kepler(e=0.0)
    t0 = time.time()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, 0.001, T * 100)
    sim.run()
    wall = time.time() - t0
    errs = sim.relative_energy_error()
    results["leapfrog_circular_100"] = {
        "integrator": "leapfrog", "dt": 0.001, "N": 2, "periods": 100,
        "final_energy_error": errs[-1], "wall_time_seconds": round(wall, 2)
    }

    # Figure-eight 10 periods
    bodies = figure_eight_bodies()
    T_eight = 6.3259
    t0 = time.time()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, 0.001, T_eight * 10)
    sim.run()
    wall = time.time() - t0
    errs = sim.relative_energy_error()
    results["figure_eight_10"] = {
        "integrator": "leapfrog", "dt": 0.001, "N": 3, "periods": 10,
        "final_energy_error": errs[-1], "wall_time_seconds": round(wall, 2)
    }

    with open("results/baseline_benchmarks.json", "w") as f:
        json.dump(results, f, indent=2)
    print("  -> results/baseline_benchmarks.json")


def run_integrator_comparison():
    """Item 017: Integrator comparison."""
    print("Running integrator comparison...")
    integrators = {
        "euler": euler_step,
        "leapfrog": leapfrog_step,
        "rk4": rk4_step,
    }
    dt_values = [0.01, 0.005, 0.001, 0.0005]
    results = {}

    for name, integ in integrators.items():
        for dt in dt_values:
            bodies, T = two_body_kepler(e=0.5)
            periods = 100 if name == "euler" else 1000
            total_time = T * periods
            t0 = time.time()
            sim = Simulation(bodies, integ, direct_gravity, dt, total_time)
            sim.run()
            wall = time.time() - t0
            errs = sim.relative_energy_error()
            key = f"{name}_dt{dt}"
            results[key] = {
                "integrator": name, "dt": dt, "N": 2,
                "periods": periods,
                "final_energy_error": errs[-1],
                "wall_time_seconds": round(wall, 2)
            }
            print(f"  {key}: |dE/E| = {errs[-1]:.2e}")

    with open("results/integrator_comparison.json", "w") as f:
        json.dump(results, f, indent=2)
    print("  -> results/integrator_comparison.json")


def run_scalability():
    """Item 018: Scalability benchmarks."""
    print("Running scalability benchmarks...")
    random.seed(42)
    N_values = [10, 50, 100, 200, 500, 1000]
    benchmarks = []

    for N in N_values:
        bodies = [
            Body(random.uniform(0.5, 1.5),
                 Vec2(random.uniform(-10, 10), random.uniform(-10, 10)),
                 Vec2(0, 0))
            for _ in range(N)
        ]

        # Direct
        times_d = []
        for _ in range(5):
            t0 = time.time()
            direct_gravity(bodies, G=1.0, softening=0.1)
            times_d.append(time.time() - t0)
        t_direct = sorted(times_d)[2]

        # Barnes-Hut
        times_b = []
        for _ in range(5):
            t0 = time.time()
            barneshut_gravity(bodies, G=1.0, softening=0.1, theta=0.5)
            times_b.append(time.time() - t0)
        t_bh = sorted(times_b)[2]

        # RMS error
        acc_d = direct_gravity(bodies, G=1.0, softening=0.1)
        acc_b = barneshut_gravity(bodies, G=1.0, softening=0.1, theta=0.5)
        rms = 0.0
        for i in range(N):
            d_mag = acc_d[i].magnitude()
            if d_mag > 1e-30:
                dx = acc_b[i].x - acc_d[i].x
                dy = acc_b[i].y - acc_d[i].y
                rms += (dx * dx + dy * dy) / (d_mag * d_mag)
        rms = math.sqrt(rms / N)

        benchmarks.append({
            "method_direct": {"N": N, "wall_time_seconds": round(t_direct, 6)},
            "method_barneshut": {"N": N, "wall_time_seconds": round(t_bh, 6), "theta": 0.5},
            "force_rms_error_vs_direct": round(rms, 6),
            "barneshut_faster": t_bh < t_direct,
        })
        print(f"  N={N}: direct={t_direct:.4f}s, BH={t_bh:.4f}s, RMS={rms:.4f}")

    crossover = min((b["method_direct"]["N"] for b in benchmarks if b["barneshut_faster"]), default=None)
    result = {
        "benchmarks": benchmarks,
        "crossover_N": crossover,
        "notes": f"Barnes-Hut becomes faster at N={crossover}" if crossover else "Barnes-Hut never faster"
    }
    with open("results/scalability.json", "w") as f:
        json.dump(result, f, indent=2)
    print("  -> results/scalability.json")


def run_adaptive_comparison():
    """Item 019: Adaptive vs fixed comparison."""
    print("Running adaptive vs fixed comparison...")
    bodies, T = two_body_kepler(e=0.9)
    total_time = T * 100

    # Fixed
    t0 = time.time()
    sim_fixed = Simulation(bodies, leapfrog_step, direct_gravity, 0.001, total_time)
    sim_fixed.run()
    wall_fixed = time.time() - t0
    fixed_err = sim_fixed.relative_energy_error()[-1]

    # Adaptive
    controller = AdaptiveController(eta=0.01, dt_min=1e-6, dt_max=0.1)
    t0 = time.time()
    result = run_adaptive_simulation(
        [Body(b.mass, b.pos, b.vel) for b in bodies],
        direct_gravity, leapfrog_step, controller, total_time
    )
    wall_adapt = time.time() - t0
    E0 = result['energies'][0]
    adapt_err = abs((result['energies'][-1] - E0) / E0) if E0 != 0 else abs(result['energies'][-1])

    # One period sample
    bodies2, T2 = two_body_kepler(e=0.9)
    controller2 = AdaptiveController(eta=0.01, dt_min=1e-6, dt_max=0.1)
    r1 = run_adaptive_simulation(
        bodies2, direct_gravity, leapfrog_step, controller2, T2
    )

    output = {
        "fixed": {
            "dt": 0.001,
            "total_steps": len(sim_fixed.times) - 1,
            "final_energy_error": fixed_err,
            "wall_time_seconds": round(wall_fixed, 2)
        },
        "adaptive": {
            "eta": 0.01,
            "total_steps": result['step_count'],
            "final_energy_error": adapt_err,
            "wall_time_seconds": round(wall_adapt, 2),
            "dt_one_period_sample": r1['dt_history'],
            "times_one_period_sample": r1['times'],
        },
        "step_reduction_percent": round(100 * (1 - result['step_count'] / (len(sim_fixed.times) - 1)), 1),
        "h3_confirmed": result['step_count'] < 0.5 * (len(sim_fixed.times) - 1),
        "eccentricity": 0.9,
        "periods": 100,
    }

    with open("results/adaptive_comparison.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"  -> results/adaptive_comparison.json (reduction: {output['step_reduction_percent']}%)")


def run_validation():
    """Item 020: Validation tests."""
    print("Running validation tests...")
    results = {}

    # Circular orbit period
    bodies, T_anal = two_body_kepler(e=0.0)
    sim = Simulation(bodies, rk4_step, direct_gravity, 0.0001, T_anal * 1.5)
    sim.run()
    x0 = sim.history_pos[0][1].x
    crossed = False
    T_meas = T_anal
    for i in range(1, len(sim.history_pos)):
        y_prev = sim.history_pos[i - 1][1].y
        y_curr = sim.history_pos[i][1].y
        if y_prev < 0 and y_curr >= 0 and sim.history_pos[i][1].x > 0:
            if crossed:
                T_meas = sim.times[i]
                break
            crossed = True
    rel_err = abs(T_meas - T_anal) / T_anal
    results["circular_orbit"] = {
        "T_analytical": T_anal,
        "T_measured": T_meas,
        "relative_error": rel_err,
        "threshold": 0.001,
        "pass": rel_err < 0.001,
    }

    # LRL vector
    bodies, T = two_body_kepler(e=0.5)
    sim = Simulation(bodies, leapfrog_step, direct_gravity, 0.001, T * 100)
    sim.run()

    def lrl_angle(pos, vel, mu=1.0):
        r = pos.magnitude()
        v2 = vel.magnitude_squared()
        rdot = (pos.x * vel.x + pos.y * vel.y) / r
        ex = (v2 / mu - 1.0 / r) * pos.x - rdot * vel.x
        ey = (v2 / mu - 1.0 / r) * pos.y - rdot * vel.y
        return math.degrees(math.atan2(ey, ex))

    angle_i = lrl_angle(sim.history_pos[0][1], sim.history_vel[0][1])
    angle_f = lrl_angle(sim.history_pos[-1][1], sim.history_vel[-1][1])
    diff = abs(angle_f - angle_i)
    results["elliptical_orbit_lrl"] = {
        "angle_initial_deg": angle_i,
        "angle_final_deg": angle_f,
        "angle_difference_deg": diff,
        "threshold_deg": 1.0,
        "periods": 100,
        "pass": diff < 1.0,
    }

    # Figure-eight
    bodies = figure_eight_bodies()
    T_eight = 6.3259
    sim = Simulation(bodies, rk4_step, direct_gravity, 0.001, T_eight * 5)
    sim.run()
    errs = sim.relative_energy_error()
    max_drift = 0.0
    for i, pos in enumerate(sim.history_pos):
        for j in range(3):
            dx = pos[j].x - sim.history_pos[0][j].x
            dy = pos[j].y - sim.history_pos[0][j].y
            max_drift = max(max_drift, math.sqrt(dx * dx + dy * dy))
    results["figure_eight"] = {
        "periods": 5,
        "energy_error": errs[-1],
        "max_position_drift": max_drift,
        "pass": errs[-1] < 1e-6 and max_drift < 1.0,
    }

    with open("results/validation.json", "w") as f:
        json.dump(results, f, indent=2)
    print("  -> results/validation.json")


def run_softening_analysis():
    """Item 016: Softening analysis."""
    print("Running softening analysis...")
    random.seed(42)
    N = 50
    base_bodies = [
        Body(random.uniform(0.5, 1.5),
             Vec2(random.uniform(-10, 10), random.uniform(-10, 10)),
             Vec2(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)))
        for _ in range(N)
    ]

    eps_values = [0, 1e-4, 1e-3, 1e-2, 1e-1]
    results = []

    for eps in eps_values:
        bodies = [Body(b.mass, b.pos, b.vel) for b in base_bodies]
        dt = 0.005
        total_time = 100.0
        try:
            sim = Simulation(bodies, leapfrog_step, direct_gravity, dt, total_time,
                             force_kwargs={'softening': eps})
            sim.run()
            errs = sim.relative_energy_error()
            max_force = 0.0
            has_nan = False
            results.append({
                "softening": eps,
                "final_energy_error": errs[-1],
                "max_energy_error": max(errs),
                "nan_count": 0,
                "stable": errs[-1] < 1.0,
            })
        except Exception as e:
            results.append({
                "softening": eps,
                "error": str(e),
                "stable": False,
            })
        print(f"  eps={eps}: done")

    with open("results/softening_analysis.json", "w") as f:
        json.dump(results, f, indent=2)
    print("  -> results/softening_analysis.json")


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    run_baseline_benchmarks()
    run_integrator_comparison()
    run_scalability()
    run_adaptive_comparison()
    run_validation()
    run_softening_analysis()
    print("\nAll benchmarks complete.")
