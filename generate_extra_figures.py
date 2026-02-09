#!/usr/bin/env python3
"""Generate two additional publication-quality figures for the Beatty sequence research."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import math

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

# ---------------------------------------------------------------------------
# Figure 1: figures/beatty_examples.png
# Show floor(n*r) for n=1..50 for 4 representative r values in a 2x2 subplot
# ---------------------------------------------------------------------------

phi = (1.0 + math.sqrt(5)) / 2.0
r_values = [
    (3.0 / 2.0,      r"$r = 3/2$ (rational)"),
    (phi,             r"$r = \varphi = \frac{1+\sqrt{5}}{2}$ (quadratic irrational)"),
    (2.0 ** (1.0/3),  r"$r = 2^{1/3}$ (cubic algebraic irrational)"),
    (math.pi,         r"$r = \pi$ (transcendental)"),
]

palette = sns.color_palette("muted")
subplot_labels = ["(a)", "(b)", "(c)", "(d)"]

ns = np.arange(1, 51)

fig1, axes1 = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)

for idx, (ax, (r_val, label_text)) in enumerate(zip(axes1.flat, r_values)):
    beatty = np.array([math.floor(n * r_val) for n in ns])
    color = palette[idx]

    # Step plot of floor(n*r)
    ax.step(ns, beatty, where='mid', color=color, linewidth=1.4,
            label=r"$\lfloor n \cdot r \rfloor$", zorder=3)
    # Scatter markers on top for clarity
    ax.scatter(ns, beatty, color=color, s=12, zorder=4, edgecolors='white',
               linewidths=0.3)

    # Dashed linear trend y = r*n
    ax.plot(ns, r_val * ns, '--', color='0.35', linewidth=1.0, alpha=0.8,
            label=r"$y = r \cdot n$")

    ax.set_xlabel("$n$")
    ax.set_ylabel(r"$\lfloor n \cdot r \rfloor$")
    ax.set_title(f"{subplot_labels[idx]}  {label_text}", fontsize=12)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_xlim(0, 52)

fig1.suptitle("Beatty Sequences for Representative Irrationality Classes",
              fontsize=15, fontweight='bold', y=1.02)

fig1.savefig("figures/beatty_examples.png", dpi=300)
fig1.savefig("figures/beatty_examples.pdf")
plt.close(fig1)
print("Saved figures/beatty_examples.png and .pdf")

# ---------------------------------------------------------------------------
# Figure 2: figures/recurrence_detection.png
# Illustrate how a C-finite (Fibonacci) subsequence is extracted from the
# phi Beatty sequence.
# ---------------------------------------------------------------------------

# Full Beatty sequence for phi, n=1..30
ns_full = np.arange(1, 31)
beatty_phi = np.array([math.floor(n * phi) for n in ns_full])

# Wythoff row-1 indices: n values whose floor(n*phi) gives Fibonacci numbers.
# The lower Wythoff sequence evaluated at Fibonacci-indexed positions gives
# Fibonacci numbers: floor(F_k * phi) = F_{k+1}.
fib_n_indices = [1, 2, 3, 5, 8, 13, 21]
fib_values    = [math.floor(n * phi) for n in fib_n_indices]

extracted = fib_values

fig2, (ax_top, ax_bot) = plt.subplots(
    2, 1, figsize=(10, 7), constrained_layout=True,
    gridspec_kw={'height_ratios': [1, 1]}
)

# ---- Top panel ----
ax_top.scatter(ns_full, beatty_phi, color=palette[0], s=40, zorder=3,
               edgecolors='white', linewidths=0.4, label=r"$\lfloor n \varphi \rfloor$")

# Highlight the Fibonacci-indexed entries
highlight_y = np.array(fib_values)
highlight_x = np.array(fib_n_indices)
ax_top.scatter(highlight_x, highlight_y, color=sns.color_palette("bright")[3],
               s=110, zorder=4, edgecolors='black', linewidths=0.8,
               marker='D', label="Fibonacci-indexed entries")

# Connect highlighted dots with a thin line
ax_top.plot(highlight_x, highlight_y, color=sns.color_palette("bright")[3],
            linewidth=0.9, alpha=0.5, zorder=2)

ax_top.set_xlabel("$n$")
ax_top.set_ylabel(r"$\lfloor n \varphi \rfloor$")
ax_top.set_title(r"(a)  $\lfloor n \varphi \rfloor$ for $n = 1 \ldots 30$"
                 " — Fibonacci-indexed entries highlighted", fontsize=12)
ax_top.legend(loc="upper left", fontsize=10)
ax_top.set_xlim(0, 32)

# ---- Bottom panel ----
k_vals = np.arange(len(extracted))

# Plot the extracted subsequence as large dots
ax_bot.scatter(k_vals, extracted, color=sns.color_palette("bright")[3],
               s=120, zorder=5, edgecolors='black', linewidths=0.8, marker='D')

# Label each point with its value
for k, val in enumerate(extracted):
    ax_bot.annotate(f"{val}", (k, val), textcoords="offset points",
                    xytext=(0, 14), ha='center', fontsize=10, fontweight='bold',
                    color='0.15')

# Draw arrows showing the recurrence w(k+2) = w(k+1) + w(k)
arrow_color = palette[2]
for k in range(len(extracted) - 2):
    # Arrow from w(k) curving to w(k+2)
    ax_bot.annotate(
        "", xy=(k + 2, extracted[k + 2]), xytext=(k, extracted[k]),
        arrowprops=dict(arrowstyle='->', color=arrow_color, lw=1.3,
                        connectionstyle='arc3,rad=-0.3', alpha=0.7),
    )
    # Arrow from w(k+1) curving to w(k+2)
    ax_bot.annotate(
        "", xy=(k + 2, extracted[k + 2]), xytext=(k + 1, extracted[k + 1]),
        arrowprops=dict(arrowstyle='->', color=palette[4], lw=1.3,
                        connectionstyle='arc3,rad=-0.2', alpha=0.7),
    )

# Add a text box explaining the recurrence
recurrence_text = r"$w(k\!+\!2) = w(k\!+\!1) + w(k)$"
ax_bot.text(0.98, 0.08, recurrence_text, transform=ax_bot.transAxes,
            fontsize=13, ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                      edgecolor='0.7', alpha=0.95))

# Add legend entries for the arrows
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=arrow_color, lw=1.5, linestyle='-',
           label=r"$w(k) \to w(k\!+\!2)$"),
    Line2D([0], [0], color=palette[4], lw=1.5, linestyle='-',
           label=r"$w(k\!+\!1) \to w(k\!+\!2)$"),
]
ax_bot.legend(handles=legend_elements, loc='upper left', fontsize=10)

ax_bot.set_xlabel("Subsequence index $k$")
ax_bot.set_ylabel("$w(k)$")
ax_bot.set_title("(b)  Extracted subsequence with Fibonacci recurrence",
                 fontsize=12)
ax_bot.set_xlim(-0.5, len(extracted) - 0.5)
ax_bot.set_ylim(min(extracted) - 3, max(extracted) + 6)

fig2.suptitle("Extracting a Fibonacci Subsequence from the Golden Ratio Beatty Sequence",
              fontsize=14, fontweight='bold', y=1.02)

fig2.savefig("figures/recurrence_detection.png", dpi=300)
fig2.savefig("figures/recurrence_detection.pdf")
plt.close(fig2)
print("Saved figures/recurrence_detection.png and .pdf")

print("\nAll figures generated successfully.")
