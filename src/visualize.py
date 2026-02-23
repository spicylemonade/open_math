"""Visualization module for the gravity simulator."""

import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# Publication-quality figure setup
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


def plot_trajectories(sim, filename='figures/trajectory_example', title='Body Trajectories',
                      colors=None):
    """Plot body trajectories from a completed simulation.

    Parameters
    ----------
    sim : Simulation
        A completed Simulation object with history_pos populated.
    filename : str
        Output filename (without extension). Saves .png and .pdf.
    title : str
        Plot title.
    colors : list, optional
        Colors for each body.
    """
    n_bodies = len(sim.history_pos[0])
    palette = colors or sns.color_palette("deep", n_bodies)
    markers = ['o', 's', 'D', '^', 'v', 'P', '*', 'X']

    fig, ax = plt.subplots(1, 1, figsize=(8, 8), constrained_layout=True)

    for b_idx in range(n_bodies):
        xs = [step[b_idx].x for step in sim.history_pos]
        ys = [step[b_idx].y for step in sim.history_pos]

        # Plot trajectory line
        ax.plot(xs, ys, color=palette[b_idx % len(palette)],
                linewidth=0.8, alpha=0.7, label=f'Body {b_idx}')
        # Mark start position
        ax.plot(xs[0], ys[0], marker=markers[b_idx % len(markers)],
                color=palette[b_idx % len(palette)], markersize=8, zorder=5)

    ax.set_xlabel('x position')
    ax.set_ylabel('y position')
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.legend(loc='best', frameon=True)

    plt.savefig(f'{filename}.png', dpi=300)
    plt.savefig(f'{filename}.pdf')
    plt.close()


def plot_energy_error(sim, filename='figures/energy_example', title='Relative Energy Error'):
    """Plot relative energy error over time.

    Parameters
    ----------
    sim : Simulation
        A completed Simulation object.
    filename : str
        Output filename (without extension).
    title : str
        Plot title.
    """
    errors = sim.relative_energy_error()
    times = sim.times

    fig, ax = plt.subplots(1, 1, figsize=(8, 5), constrained_layout=True)
    ax.semilogy(times, [max(e, 1e-16) for e in errors],
                color=sns.color_palette("deep")[0], linewidth=1.0)
    ax.set_xlabel('Time')
    ax.set_ylabel('Relative Energy Error |dE/E|')
    ax.set_title(title)

    plt.savefig(f'{filename}.png', dpi=300)
    plt.savefig(f'{filename}.pdf')
    plt.close()


def plot_energy_comparison(results_dict, filename='figures/energy_conservation',
                           title='Energy Conservation: Integrator Comparison'):
    """Plot energy error comparison across integrators.

    Parameters
    ----------
    results_dict : dict
        Mapping label -> (times, energy_errors).
    filename : str
    title : str
    """
    palette = sns.color_palette("deep", len(results_dict))
    line_styles = ['-', '--', '-.', ':']
    markers_list = ['o', 's', 'D', '^', 'v']

    fig, ax = plt.subplots(1, 1, figsize=(10, 6), constrained_layout=True)

    for i, (label, (times, errors)) in enumerate(results_dict.items()):
        ax.semilogy(times, [max(e, 1e-16) for e in errors],
                    color=palette[i % len(palette)],
                    linestyle=line_styles[i % len(line_styles)],
                    linewidth=1.0, label=label)

    ax.set_xlabel('Time (orbital periods)')
    ax.set_ylabel('Relative Energy Error |dE/E|')
    ax.set_title(title)
    ax.legend(loc='best', frameon=True, ncol=2)

    plt.savefig(f'{filename}.png', dpi=300)
    plt.savefig(f'{filename}.pdf')
    plt.close()
