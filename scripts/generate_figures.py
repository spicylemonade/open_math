#!/usr/bin/env python3
"""Regenerate all figures/ from results/ data and simulations.

Usage: python -m scripts.generate_figures
"""

import json
import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity
from src.integrators import euler_step, leapfrog_step, rk4_step
from src.simulation import Simulation
from src.adaptive import AdaptiveController, run_adaptive_simulation

# Publication-quality style
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
mpl.rcParams.update({
    'figure.figsize': (8, 5),
    'figure.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'legend.framealpha': 0.9,
    'legend.edgecolor': '0.8',
    'font.family': 'serif',
    'grid.alpha': 0.3,
    'grid.linewidth': 0.5,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

PALETTE = sns.color_palette("deep")


def two_body_kepler(e=0.0):
    a = 1.0
    G = 1.0
    m1, m2 = 1.0, 1e-6
    M = m1 + m2
    v0 = math.sqrt(G * M / a * (1 + e))
    r0 = a * (1 - e)
    T = 2 * math.pi * math.sqrt(a ** 3 / (G * M))
    return [Body(m1, Vec2(0, 0), Vec2(0, 0)), Body(m2, Vec2(r0, 0), Vec2(0, v0))], T


def fig_energy_conservation():
    """Figure 1: Integrator energy conservation comparison."""
    print("Generating energy_conservation...")
    integrators = {"Euler": euler_step, "Leapfrog": leapfrog_step, "RK4": rk4_step}
    dt = 0.001
    fig, ax = plt.subplots(1, 1, figsize=(10, 6), constrained_layout=True)

    for i, (name, integ) in enumerate(integrators.items()):
        bodies, T = two_body_kepler(e=0.5)
        periods = 100 if name == "Euler" else 1000
        sim = Simulation(bodies, integ, direct_gravity, dt, T * periods)
        sim.run()
        errs = sim.relative_energy_error()
        times_in_periods = [t / T for t in sim.times]
        ax.semilogy(times_in_periods, [max(e, 1e-16) for e in errs],
                     color=PALETTE[i], linewidth=1.0, label=f"{name} (dt={dt})")

    ax.set_xlabel("Time (orbital periods)")
    ax.set_ylabel("Relative Energy Error |dE/E|")
    ax.set_title("Energy Conservation: Integrator Comparison")
    ax.legend(loc="best", frameon=True)
    plt.savefig("figures/energy_conservation.png", dpi=300)
    plt.savefig("figures/energy_conservation.pdf")
    plt.close()


def fig_scalability():
    """Figure 2: Direct vs Barnes-Hut scalability."""
    print("Generating scalability...")
    with open("results/scalability.json") as f:
        data = json.load(f)

    Ns, t_direct, t_bh = [], [], []
    for b in data["benchmarks"]:
        Ns.append(b["method_direct"]["N"])
        t_direct.append(b["method_direct"]["wall_time_seconds"])
        t_bh.append(b["method_barneshut"]["wall_time_seconds"])

    fig, ax = plt.subplots(1, 1, figsize=(8, 6), constrained_layout=True)
    ax.loglog(Ns, t_direct, 'o-', color=PALETTE[0], label="Direct O(N²)", linewidth=1.5, markersize=6)
    ax.loglog(Ns, t_bh, 's-', color=PALETTE[1], label="Barnes-Hut O(N log N)", linewidth=1.5, markersize=6)
    ax.set_xlabel("Number of Bodies N")
    ax.set_ylabel("Wall Time (seconds)")
    ax.set_title("Force Computation Scalability")
    ax.legend(loc="best", frameon=True)
    plt.savefig("figures/scalability.png", dpi=300)
    plt.savefig("figures/scalability.pdf")
    plt.close()


def fig_adaptive_timestep():
    """Figure 3: Adaptive timestep variation."""
    print("Generating adaptive_timestep...")
    with open("results/adaptive_comparison.json") as f:
        data = json.load(f)

    dt_hist = data["adaptive"]["dt_one_period_sample"]
    times_hist = data["adaptive"]["times_one_period_sample"]
    n = min(len(dt_hist), len(times_hist) - 1)

    fig, ax = plt.subplots(1, 1, figsize=(8, 5), constrained_layout=True)
    ax.plot(times_hist[1:n + 1], dt_hist[:n], color=PALETTE[0], linewidth=1.0)
    ax.set_xlabel("Time")
    ax.set_ylabel("Adaptive Time Step dt")
    ax.set_title("Adaptive Time Step Variation (e=0.9, One Orbit)")
    plt.savefig("figures/adaptive_timestep.png", dpi=300)
    plt.savefig("figures/adaptive_timestep.pdf")
    plt.close()


def fig_trajectory_kepler():
    """Figure 4: Kepler orbit trajectory."""
    print("Generating trajectory_kepler...")
    bodies, T = two_body_kepler(e=0.5)
    sim = Simulation(bodies, leapfrog_step, direct_gravity, 0.001, T * 3)
    sim.run()

    xs = [step[1].x for step in sim.history_pos]
    ys = [step[1].y for step in sim.history_pos]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8), constrained_layout=True)
    ax.plot(xs, ys, color=PALETTE[0], linewidth=0.8, alpha=0.8)
    ax.plot(xs[0], ys[0], 'o', color=PALETTE[1], markersize=8, label="Start", zorder=5)
    ax.plot(0, 0, '*', color=PALETTE[2], markersize=12, label="Central body", zorder=5)
    ax.set_xlabel("x position")
    ax.set_ylabel("y position")
    ax.set_title("Kepler Orbit (e=0.5)")
    ax.set_aspect("equal")
    ax.legend(loc="best", frameon=True)
    plt.savefig("figures/trajectory_kepler.png", dpi=300)
    plt.savefig("figures/trajectory_kepler.pdf")
    plt.close()


def fig_softening_effects():
    """Figure 5: Energy error vs softening."""
    print("Generating softening_effects...")
    with open("results/softening_analysis.json") as f:
        data = json.load(f)

    eps_vals = [d["softening"] for d in data if "final_energy_error" in d and d["softening"] > 0]
    errs = [d["final_energy_error"] for d in data if "final_energy_error" in d and d["softening"] > 0]

    fig, ax = plt.subplots(1, 1, figsize=(8, 5), constrained_layout=True)
    ax.loglog(eps_vals, errs, 'o-', color=PALETTE[0], linewidth=1.5, markersize=8)
    ax.set_xlabel("Softening Length ε")
    ax.set_ylabel("Final Relative Energy Error |dE/E|")
    ax.set_title("Effect of Gravitational Softening on Energy Conservation")
    plt.savefig("figures/softening_effects.png", dpi=300)
    plt.savefig("figures/softening_effects.pdf")
    plt.close()


def fig_examples():
    """Generate example trajectory and energy plots."""
    print("Generating example figures...")
    bodies, T = two_body_kepler(e=0.0)
    sim = Simulation(bodies, leapfrog_step, direct_gravity, 0.001, T * 5)
    sim.run()

    from src.visualize import plot_trajectories, plot_energy_error
    plot_trajectories(sim, 'figures/trajectory_example', 'Two-Body Circular Orbit')
    plot_energy_error(sim, 'figures/energy_example', 'Energy Error: Leapfrog, Circular Orbit')


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    fig_energy_conservation()
    fig_scalability()
    fig_adaptive_timestep()
    fig_trajectory_kepler()
    fig_softening_effects()
    fig_examples()
    print("\nAll figures generated.")
