"""
Visualization module for N-body simulation.

Usage:
    python -m src.visualize                    # Generate demo trajectory plot
    python -m src.visualize <results_file>     # Plot from saved results
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import json
import sys
import os


def setup_style():
    """Configure publication-quality matplotlib styling."""
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


def plot_trajectories(sim_result, filename='figures/trajectories.png', title='Particle Trajectories'):
    """
    Plot 2D particle trajectories from simulation results.

    Parameters
    ----------
    sim_result : dict with 'positions' (list of N×2 arrays) and 'masses'
    filename : str - output path
    title : str - plot title
    """
    setup_style()
    colors = sns.color_palette("deep", n_colors=len(sim_result['masses']))

    fig, ax = plt.subplots(figsize=(8, 8))

    n_bodies = len(sim_result['masses'])
    n_frames = len(sim_result['positions'])

    for i in range(n_bodies):
        traj = np.array([sim_result['positions'][t][i] for t in range(n_frames)])
        ax.plot(traj[:, 0], traj[:, 1], color=colors[i], linewidth=0.8,
                alpha=0.7, label=f'Body {i+1} (m={sim_result["masses"][i]:.2g})')
        ax.plot(traj[0, 0], traj[0, 1], 'o', color=colors[i], markersize=8, zorder=5)
        ax.plot(traj[-1, 0], traj[-1, 1], 's', color=colors[i], markersize=6, zorder=5)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.legend(loc='upper right', frameon=True)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, dpi=300)
    plt.savefig(filename.replace('.png', '.pdf'))
    plt.close()
    print(f'Saved: {filename}')


def plot_energy_error(times, energy_errors, labels=None, filename='figures/energy_error.png',
                      title='Energy Conservation'):
    """
    Plot energy error |dE/E0| vs time.

    Parameters
    ----------
    times : list of arrays
    energy_errors : list of arrays
    labels : list of str
    """
    setup_style()
    colors = sns.color_palette("deep", n_colors=len(energy_errors))
    markers = ['o', 's', '^', 'D', 'v']

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, (t, e) in enumerate(zip(times, energy_errors)):
        label = labels[i] if labels else f'Method {i+1}'
        marker = markers[i % len(markers)]
        # Subsample for readability
        step = max(1, len(t) // 200)
        ax.semilogy(t[::step], np.array(e[::step]) + 1e-16, color=colors[i],
                     marker=marker, markersize=3, markevery=max(1, len(t[::step]) // 20),
                     linewidth=1.0, alpha=0.8, label=label)

    ax.set_xlabel('Time (orbital periods)')
    ax.set_ylabel('Relative Energy Error |dE/E₀|')
    ax.set_title(title)
    ax.legend(loc='best', frameon=True)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, dpi=300)
    plt.savefig(filename.replace('.png', '.pdf'))
    plt.close()
    print(f'Saved: {filename}')


def generate_demo_figure():
    """Generate a demo figure-eight trajectory plot."""
    from src.body import create_figure_eight
    from src.integrators import run_simulation

    bodies = create_figure_eight()
    masses = np.array([b.mass for b in bodies])
    positions = np.array([b.pos for b in bodies])
    velocities = np.array([b.vel for b in bodies])

    # Run for ~5 periods (T ≈ 6.3259)
    dt = 0.001
    T_period = 6.3259
    n_steps = int(5 * T_period / dt)

    result = run_simulation(masses, positions, velocities, dt=dt, n_steps=n_steps,
                            integrator='leapfrog', G=1.0, store_every=10)

    plot_trajectories(result, filename='figures/figure_eight_demo.png',
                      title='Figure-Eight Three-Body Choreography')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Load and plot from results file
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
        if 'energy_error_history' in data:
            times = [data['energy_error_history']['times']]
            errors = [data['energy_error_history']['errors']]
            labels = [data.get('method', 'Unknown')]
            plot_energy_error(times, errors, labels,
                              filename='figures/energy_from_file.png')
        print('Done.')
    else:
        generate_demo_figure()
