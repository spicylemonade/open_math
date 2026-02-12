"""
Generate visualizations of key results for the Kissing Number research.

Produces 4 PNG figures saved in /home/codex/work/repo/figures/:
  1. bound_comparison.png       - Bar chart of upper bounds across dimensions 2-8
  2. dimensional_recurrence.png - Multi-panel plot of V_n, S_n, ratios, cap angles
  3. cap_density.png            - Cap packing density vs dimension
  4. contact_graph.png          - D5 contact graph network visualization

Item 020 of the research rubric.
"""

import sys
import os
import math

import numpy as np

# ---------------------------------------------------------------------------
# Matplotlib setup (Agg backend for headless rendering)
# ---------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.switch_backend("Agg")

# Use a professional style
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
})

# ---------------------------------------------------------------------------
# Ensure our src modules are importable
# ---------------------------------------------------------------------------
sys.path.insert(0, "/home/codex/work/repo/src")

from ndim_geometry import V_n, S_n, cap_solid_angle, cap_area, cap_packing_bound
from d5_lattice import generate_d5_vectors, normalize_vectors, verify_kissing_configuration

# Output directory
FIGURES_DIR = "/home/codex/work/repo/figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# ===================================================================
# FIGURE 1: bound_comparison.png
# Bar chart comparing upper bounds from different methods, dims 2-8
# ===================================================================

def figure_bound_comparison():
    """Bar chart comparing upper bounds from different methods across dims 2-8."""
    dims = list(range(2, 9))

    # Literature data  (source: Pfender-Zong 2004, Odlyzko-Sloane 1979,
    # Mittelmann-Vallentin 2010, Musin 2008, Viazovska 2017, etc.)
    # Cap packing bound: S_{n-1} / A_cap(n, pi/6) -- computed from our code
    cap_bounds = []
    for n in dims:
        cb = cap_packing_bound(n)
        cap_bounds.append(int(math.floor(cb)))

    # Delsarte LP bounds (from the literature -- optimal LP values)
    delsarte_lp = {
        2: 6,
        3: 13,
        4: 25,
        5: 46,
        6: 82,
        7: 140,
        8: 240,
    }

    # SDP / semidefinite programming bounds (Bachoc-Vallentin 2008,
    # Mittelmann-Vallentin 2010)
    sdp_bounds = {
        2: 6,
        3: 12,
        4: 24,
        5: 44,
        6: 78,
        7: 134,
        8: 240,
    }

    # Known exact values (where lower == upper is proven)
    known_exact = {
        2: 6,
        3: 12,
        4: 24,
        5: None,   # open: 40..44
        6: None,   # open: 72..78
        7: None,   # open: 126..134
        8: 240,
    }

    cap_vals = [cap_bounds[i] for i in range(len(dims))]
    del_vals = [delsarte_lp[d] for d in dims]
    sdp_vals = [sdp_bounds[d] for d in dims]
    exact_vals = [known_exact[d] for d in dims]

    x = np.arange(len(dims))
    width = 0.20

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(x - 1.5 * width, cap_vals, width, label="Cap Packing", color="#4c72b0")
    bars2 = ax.bar(x - 0.5 * width, del_vals, width, label="Delsarte LP", color="#dd8452")
    bars3 = ax.bar(x + 0.5 * width, sdp_vals, width, label="SDP", color="#55a868")

    # Known exact: only plot where known
    exact_for_plot = []
    exact_x = []
    for i, d in enumerate(dims):
        if known_exact[d] is not None:
            exact_for_plot.append(known_exact[d])
            exact_x.append(x[i] + 1.5 * width)
    ax.bar(exact_x, exact_for_plot, width, label="Known Exact", color="#c44e52", edgecolor="black", linewidth=0.8)

    ax.set_xlabel("Dimension $n$")
    ax.set_ylabel("Upper Bound on Kissing Number $\\tau_n$")
    ax.set_title("Comparison of Upper Bounds on Kissing Numbers ($n = 2$ to $8$)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(d) for d in dims])
    ax.legend(loc="upper left")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)

    # Annotate the bars with values (only for readable ranges)
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{int(h)}",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=7, rotation=90)

    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, "bound_comparison.png")
    fig.savefig(outpath)
    plt.close(fig)
    print(f"  Saved {outpath}")


# ===================================================================
# FIGURE 2: dimensional_recurrence.png
# Multi-panel: V_n(1), S_n(1), V_n/S_n, cap_solid_angle vs n
# ===================================================================

def figure_dimensional_recurrence():
    """Multi-panel plot showing dimensional recurrence relationships."""
    ns_full = list(range(1, 16))
    ns_cap = list(range(2, 16))

    v_vals = [V_n(n, 1.0) for n in ns_full]
    s_vals = [S_n(n, 1.0) for n in ns_full]
    ratio_vals = [V_n(n, 1.0) / S_n(n, 1.0) for n in ns_full]  # = 1/n * R
    cap_vals = [cap_solid_angle(n, math.pi / 6) for n in ns_cap]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Panel 1: V_n(1) vs n
    ax1 = axes[0, 0]
    ax1.plot(ns_full, v_vals, "o-", color="#4c72b0", linewidth=1.5, markersize=5)
    ax1.set_xlabel("Dimension $n$")
    ax1.set_ylabel("$V_n(1)$")
    ax1.set_title("Volume of Unit $n$-Ball")
    ax1.set_xticks(ns_full)

    # Panel 2: S_n(1) vs n
    ax2 = axes[0, 1]
    ax2.plot(ns_full, s_vals, "s-", color="#dd8452", linewidth=1.5, markersize=5)
    ax2.set_xlabel("Dimension $n$")
    ax2.set_ylabel("$S_{n-1}(1)$")
    ax2.set_title("Surface Area of Unit $(n{-}1)$-Sphere")
    ax2.set_xticks(ns_full)

    # Panel 3: V_n / S_n = R/n  (for R=1 this is 1/n)
    ax3 = axes[1, 0]
    ax3.plot(ns_full, ratio_vals, "D-", color="#55a868", linewidth=1.5, markersize=5)
    theoretical = [1.0 / n for n in ns_full]
    ax3.plot(ns_full, theoretical, "k--", linewidth=1, alpha=0.6, label="$1/n$")
    ax3.set_xlabel("Dimension $n$")
    ax3.set_ylabel("$V_n / S_{n-1}$")
    ax3.set_title("Volume-to-Surface Ratio ($= R/n = 1/n$ for $R=1$)")
    ax3.legend()
    ax3.set_xticks(ns_full)

    # Panel 4: cap_solid_angle(n, pi/6) vs n
    ax4 = axes[1, 1]
    ax4.plot(ns_cap, cap_vals, "^-", color="#c44e52", linewidth=1.5, markersize=5)
    ax4.set_xlabel("Dimension $n$")
    ax4.set_ylabel("$\\Omega_{\\mathrm{cap}}(n, \\pi/6) / \\Omega_n$")
    ax4.set_title("Fractional Cap Solid Angle ($\\theta = \\pi/6$)")
    ax4.set_xticks(ns_cap)
    ax4.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.4f"))

    fig.suptitle("Dimensional Recurrence Relationships for $n$-Balls and Spherical Caps",
                 fontsize=14, y=1.01)
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, "dimensional_recurrence.png")
    fig.savefig(outpath)
    plt.close(fig)
    print(f"  Saved {outpath}")


# ===================================================================
# FIGURE 3: cap_density.png
# Cap packing density rho_n = tau_n * omega_cap vs n
# ===================================================================

def figure_cap_density():
    """Plot of cap packing density rho_n = tau_n * omega_cap(n, pi/6) vs n."""
    # Known exact kissing numbers
    known_tau = {
        2: 6,
        3: 12,
        4: 24,
        8: 240,
        24: 196560,
    }

    # Hypothetical values for n=5
    hyp_tau5_low = 40
    hyp_tau5_high = 44

    # Compute fractional cap solid angles
    dims_known = sorted(known_tau.keys())
    omega_caps = {n: cap_solid_angle(n, math.pi / 6) for n in dims_known}

    # Also compute for n=5
    omega_5 = cap_solid_angle(5, math.pi / 6)

    # Cap packing density: rho = tau * omega_cap
    rho_known = {n: known_tau[n] * omega_caps[n] for n in dims_known}

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot known exact values
    ns_known = [n for n in dims_known]
    rhos_known = [rho_known[n] for n in dims_known]
    ax.scatter(ns_known, rhos_known, s=90, zorder=5, color="#4c72b0", edgecolors="black",
               linewidth=0.8, label="Known exact $\\tau_n$")

    # Hypothetical n=5
    rho5_low = hyp_tau5_low * omega_5
    rho5_high = hyp_tau5_high * omega_5
    ax.scatter([5], [rho5_low], s=120, zorder=6, marker="v", color="#dd8452",
               edgecolors="black", linewidth=0.8,
               label=f"$\\tau_5 = {hyp_tau5_low}$ (D5 lower bound)")
    ax.scatter([5], [rho5_high], s=120, zorder=6, marker="^", color="#c44e52",
               edgecolors="black", linewidth=0.8,
               label=f"$\\tau_5 = {hyp_tau5_high}$ (LP upper bound)")

    # Exponential interpolation trend line
    # Fit log(rho) = a + b*n to the known values (excluding n=24 as outlier for fit)
    ns_fit = np.array([n for n in dims_known if n <= 8], dtype=float)
    rhos_fit = np.array([rho_known[n] for n in dims_known if n <= 8])
    log_rhos = np.log(rhos_fit)
    coeffs = np.polyfit(ns_fit, log_rhos, 1)  # linear in log space

    n_trend = np.linspace(1.5, 25, 200)
    rho_trend = np.exp(coeffs[1] + coeffs[0] * n_trend)
    ax.plot(n_trend, rho_trend, "--", color="gray", alpha=0.6, linewidth=1.5,
            label=f"Exponential trend ($\\rho \\approx e^{{{coeffs[0]:.2f}n {coeffs[1]:+.2f}}}$)")

    # Upper bound line (density = 1 means full coverage)
    ax.axhline(y=1.0, color="red", linestyle=":", linewidth=1, alpha=0.5, label="$\\rho = 1$ (full coverage)")

    ax.set_xlabel("Dimension $n$")
    ax.set_ylabel("Cap Packing Density $\\rho_n = \\tau_n \\cdot \\Omega_{\\mathrm{cap}} / \\Omega_n$")
    ax.set_title("Cap Packing Density of Optimal Kissing Configurations")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_xlim(1, 26)
    ax.set_ylim(0, 1.1)

    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, "cap_density.png")
    fig.savefig(outpath)
    plt.close(fig)
    print(f"  Saved {outpath}")


# ===================================================================
# FIGURE 4: contact_graph.png
# Network visualization of the D5 contact graph
# ===================================================================

def figure_contact_graph():
    """Network visualization of the D5 contact graph (40 nodes, contact edges)."""
    import networkx as nx

    # Generate D5 configuration
    raw = generate_d5_vectors()
    vecs = normalize_vectors(raw)
    result = verify_kissing_configuration(vecs)
    contact_pairs = result["contact_pairs"]

    n_vecs = len(vecs)

    # Build networkx graph
    G = nx.Graph()
    G.add_nodes_from(range(n_vecs))
    G.add_edges_from(contact_pairs)

    # Color nodes by their first coordinate pair (i, j) where the two nonzero
    # entries are at positions i and j.  There are C(5,2) = 10 such pairs,
    # each giving 4 vectors (for the 4 sign combinations).
    pair_index = {}
    idx = 0
    for i in range(5):
        for j in range(i + 1, 5):
            pair_index[(i, j)] = idx
            idx += 1

    node_colors_idx = []
    for k in range(n_vecs):
        v = raw[k]
        nz = tuple(sorted(np.nonzero(np.abs(v) > 0.5)[0]))
        node_colors_idx.append(pair_index.get(nz, 0))

    # Create a colormap with 10 distinct colors
    cmap = plt.cm.get_cmap("tab10", 10)
    node_colors = [cmap(c) for c in node_colors_idx]

    # Layout
    pos = nx.spring_layout(G, seed=42, k=1.5, iterations=200)

    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.15, width=0.5, edge_color="gray")

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=200, node_color=node_colors,
                           edgecolors="black", linewidths=0.6)

    # Node labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_color="white",
                            font_weight="bold")

    # Build legend for coordinate-pair groups
    pair_labels = []
    for i in range(5):
        for j in range(i + 1, 5):
            pair_labels.append(f"({i},{j})")
    legend_handles = []
    for idx_l, label in enumerate(pair_labels):
        patch = plt.Line2D([0], [0], marker="o", color="w",
                           markerfacecolor=cmap(idx_l), markersize=8,
                           markeredgecolor="black", markeredgewidth=0.5,
                           label=f"Coord pair {label}")
        legend_handles.append(patch)
    ax.legend(handles=legend_handles, loc="upper left", fontsize=8, ncol=2,
              title="Nonzero coordinate pair", title_fontsize=9)

    ax.set_title(f"D5 Lattice Contact Graph\n"
                 f"({n_vecs} vertices, {len(contact_pairs)} edges, 12-regular)",
                 fontsize=13)
    ax.axis("off")

    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, "contact_graph.png")
    fig.savefig(outpath)
    plt.close(fig)
    print(f"  Saved {outpath}")


# ===================================================================
# MAIN
# ===================================================================

def main():
    print("=" * 60)
    print("GENERATING FIGURES FOR KISSING NUMBER RESEARCH")
    print("=" * 60)

    print("\n[1/4] Generating bound_comparison.png ...")
    figure_bound_comparison()

    print("\n[2/4] Generating dimensional_recurrence.png ...")
    figure_dimensional_recurrence()

    print("\n[3/4] Generating cap_density.png ...")
    figure_cap_density()

    print("\n[4/4] Generating contact_graph.png ...")
    figure_contact_graph()

    print("\n" + "=" * 60)
    print("ALL FIGURES GENERATED SUCCESSFULLY")
    # Verify files exist
    expected = [
        "bound_comparison.png",
        "dimensional_recurrence.png",
        "cap_density.png",
        "contact_graph.png",
    ]
    for fname in expected:
        fpath = os.path.join(FIGURES_DIR, fname)
        if os.path.isfile(fpath):
            size_kb = os.path.getsize(fpath) / 1024
            print(f"  [OK]  {fpath}  ({size_kb:.1f} KB)")
        else:
            print(f"  [MISSING]  {fpath}")
    print("=" * 60)


if __name__ == "__main__":
    main()
