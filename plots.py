"""
Publication-quality plotting for pendulum simulation results.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# ─── Professional figure setup ─────────────────────────────────────────────

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

PALETTE = sns.color_palette("colorblind")
FIGDIR = "figures"
os.makedirs(FIGDIR, exist_ok=True)

METHOD_STYLES = {
    "euler":            {"color": PALETTE[0], "ls": "-",  "marker": "o", "label": "Forward Euler"},
    "symplectic_euler": {"color": PALETTE[1], "ls": "--", "marker": "s", "label": "Symplectic Euler"},
    "rk4":              {"color": PALETTE[2], "ls": "-.", "marker": "^", "label": "RK4"},
    "verlet":           {"color": PALETTE[3], "ls": ":",  "marker": "D", "label": "Störmer–Verlet"},
}


def _save(fig, name):
    """Save figure as PNG and PDF."""
    fig.savefig(os.path.join(FIGDIR, f"{name}.png"), dpi=300)
    fig.savefig(os.path.join(FIGDIR, f"{name}.pdf"))
    plt.close(fig)


def plot_theta_time(results_dict, title="Angular Displacement vs Time",
                    filename="theta_time"):
    """Plot theta(t) for one or more methods.

    results_dict: {method_name: simulate() result dict}
    """
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for method, res in results_dict.items():
        s = METHOD_STYLES.get(method, {"color": "gray", "ls": "-", "marker": ".", "label": method})
        ax.plot(res["t"], res["theta"], color=s["color"], ls=s["ls"],
                label=s["label"], linewidth=1.5, markevery=len(res["t"]) // 10,
                marker=s["marker"], markersize=4)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(r"$\theta$ (rad)")
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="best", frameon=True, shadow=True)
    _save(fig, filename)


def plot_energy_time(results_dict, title="Total Energy vs Time",
                     filename="energy_time"):
    """Plot E(t) for one or more methods."""
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for method, res in results_dict.items():
        s = METHOD_STYLES.get(method, {"color": "gray", "ls": "-", "marker": ".", "label": method})
        ax.plot(res["t"], res["energy"], color=s["color"], ls=s["ls"],
                label=s["label"], linewidth=1.5, markevery=len(res["t"]) // 10,
                marker=s["marker"], markersize=4)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Energy (J)")
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="best", frameon=True, shadow=True)
    _save(fig, filename)


def plot_phase_space(results_dict, title="Phase Portrait",
                     filename="phase_space"):
    """Plot theta vs omega phase portrait."""
    fig, ax = plt.subplots(figsize=(7, 6), constrained_layout=True)
    for method, res in results_dict.items():
        s = METHOD_STYLES.get(method, {"color": "gray", "ls": "-", "marker": ".", "label": method})
        label = s["label"]
        if "ic" in res:
            label += f" ({res['ic']})"
        ax.plot(res["theta"], res["omega"], color=s["color"], ls=s["ls"],
                label=label, linewidth=1.0, alpha=0.8)
    ax.set_xlabel(r"$\theta$ (rad)")
    ax.set_ylabel(r"$\omega$ (rad/s)")
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="best", frameon=True, shadow=True)
    _save(fig, filename)


def plot_convergence(dt_values, drift_by_method,
                     title="Energy Drift Convergence",
                     filename="convergence"):
    """Log-log plot of energy drift vs dt."""
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for method, drifts in drift_by_method.items():
        s = METHOD_STYLES.get(method, {"color": "gray", "ls": "-", "marker": ".", "label": method})
        ax.loglog(dt_values, drifts, color=s["color"], ls=s["ls"],
                  marker=s["marker"], label=s["label"], linewidth=1.5,
                  markersize=6)
    # Reference slopes
    dt_arr = np.array(dt_values)
    ax.loglog(dt_arr, 0.5 * dt_arr**1, "k--", alpha=0.3, linewidth=0.8, label=r"$\propto \Delta t^1$")
    ax.loglog(dt_arr, 0.5 * dt_arr**2, "k-.", alpha=0.3, linewidth=0.8, label=r"$\propto \Delta t^2$")
    ax.loglog(dt_arr, 10 * dt_arr**4, "k:", alpha=0.3, linewidth=0.8, label=r"$\propto \Delta t^4$")
    ax.set_xlabel(r"Time step $\Delta t$ (s)")
    ax.set_ylabel("Energy drift (J)")
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="best", frameon=True, shadow=True, ncol=2)
    _save(fig, filename)


def plot_long_time_energy(results_dict, title="Long-Time Energy Stability",
                          filename="long_time_energy"):
    """Energy vs time for long simulation runs."""
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    for method, res in results_dict.items():
        s = METHOD_STYLES.get(method, {"color": "gray", "ls": "-", "marker": ".", "label": method})
        ax.plot(res["t"], res["energy"], color=s["color"], ls=s["ls"],
                label=s["label"], linewidth=1.0)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Energy (J)")
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="best", frameon=True, shadow=True)
    _save(fig, filename)


def plot_accuracy_vs_time(methods_data, title="Accuracy vs Computation Time",
                          filename="perf_accuracy"):
    """Scatter plot of RMS error vs wall-clock time."""
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for method, points in methods_data.items():
        s = METHOD_STYLES.get(method, {"color": "gray", "ls": "-", "marker": ".", "label": method})
        times = [p["wall_time_ms"] for p in points]
        errors = [p["rms_error"] for p in points]
        ax.scatter(times, errors, color=s["color"], marker=s["marker"],
                   label=s["label"], s=60, edgecolors="white", linewidth=0.5,
                   zorder=3)
        ax.plot(times, errors, color=s["color"], ls=s["ls"], alpha=0.5,
                linewidth=1.0)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Wall-clock time (ms)")
    ax.set_ylabel("RMS error (rad)")
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="best", frameon=True, shadow=True)
    _save(fig, filename)


def plot_large_angle(result, analytical_period, title="Large-Angle Oscillation",
                     filename="large_angle"):
    """Plot theta(t) for large-angle regime."""
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    ax.plot(result["t"], result["theta"], color=PALETTE[2], linewidth=1.5,
            label=r"RK4 ($\theta_0 = 3.0$ rad)")
    # Mark one period
    ax.axvline(x=analytical_period, color=PALETTE[4], ls="--", alpha=0.7,
               label=f"Exact period T = {analytical_period:.4f} s")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(r"$\theta$ (rad)")
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="best", frameon=True, shadow=True)
    _save(fig, filename)


# ─── Quick test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from pendulum import simulate
    res = simulate(method="euler", dt=0.01, total_time=10.0)
    plot_theta_time({"euler": res}, filename="theta_time_euler")
    plot_energy_time({"euler": res}, filename="energy_time_euler")
    print("Baseline plots saved to figures/")
