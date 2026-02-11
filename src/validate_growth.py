"""Validate the growth constraint function f(m) for unitary perfect numbers.

Computes f(m) for m=1..100, where f(m) is the minimum number of distinct odd
primes s such that prod_{i=1}^{s} (1 + 1/q_i) >= R(m), with q_1=3, q_2=5, ...
consecutive odd primes and R(m) = 2^{m+1} / (1 + 2^m).

Verifies monotonicity of f(m), creates publication-quality plots, computes
the combined constraint region, and saves numerical results.

References:
    - Subbarao & Warren (1966): Fixed-valuation finiteness
    - Goto (2007): Upper bound N < 2^{2^k}
    - Wall (1988): New UPNs have >= 9 odd prime factors (omega >= 10)
"""

import json
import math
import os
import sys
from fractions import Fraction

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns
from sympy import nextprime

# ---------------------------------------------------------------------------
# Plot configuration
# ---------------------------------------------------------------------------
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
mpl.rcParams.update({
    'figure.figsize': (8, 5), 'figure.dpi': 300,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 0.8, 'axes.labelsize': 13,
    'axes.titlesize': 14, 'axes.titleweight': 'bold',
    'xtick.labelsize': 11, 'ytick.labelsize': 11,
    'legend.fontsize': 11, 'legend.framealpha': 0.9,
    'legend.edgecolor': '0.8', 'font.family': 'serif',
    'grid.alpha': 0.3, 'grid.linewidth': 0.5,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
})

# ---------------------------------------------------------------------------
# Known UPNs (for plotting)
# ---------------------------------------------------------------------------
KNOWN_UPNS = [
    {"n": 6, "m": 1, "omega_odd": 1, "omega": 2, "label": "6"},
    {"n": 60, "m": 2, "omega_odd": 2, "omega": 3, "label": "60"},
    {"n": 90, "m": 1, "omega_odd": 2, "omega": 3, "label": "90"},
    {"n": 87360, "m": 6, "omega_odd": 4, "omega": 5, "label": "87360"},
    {"n": 146361946186458562560000, "m": 18, "omega_odd": 11, "omega": 12,
     "label": r"$n_5$"},
]


def compute_R(m):
    """Compute R(m) = 2^{m+1} / (1 + 2^m) as an exact Fraction.

    For a UPN n = 2^m * D, the odd part D must satisfy
    sigma*(D)/D = R(m).

    Args:
        m: Non-negative integer (2-adic valuation).

    Returns:
        Fraction value of R(m).
    """
    two_m = Fraction(2) ** m
    return Fraction(2) * two_m / (1 + two_m)


def consecutive_odd_primes(count):
    """Return the first `count` consecutive odd primes: 3, 5, 7, 11, ...

    Args:
        count: Number of odd primes to generate.

    Returns:
        List of the first `count` odd primes.
    """
    primes = []
    p = 3
    for _ in range(count):
        primes.append(p)
        p = int(nextprime(p))
    return primes


def cumulative_products(primes):
    """Compute cumulative products P(s) = prod_{i=1}^{s} (1 + 1/q_i).

    Args:
        primes: List of odd primes q_1, q_2, ...

    Returns:
        List of Fraction values [P(1), P(2), ...].
    """
    products = []
    running = Fraction(1)
    for q in primes:
        running *= Fraction(q + 1, q)
        products.append(running)
    return products


def compute_f(m_max=100, prime_count=200):
    """Compute f(m) for m = 1 .. m_max.

    f(m) = min{ s >= 1 : P(s) >= R(m) }

    where P(s) = prod_{i=1}^{s} (1 + 1/q_i) over the first s consecutive
    odd primes.

    Args:
        m_max: Maximum value of m to compute.
        prime_count: Number of consecutive odd primes to precompute.

    Returns:
        Dict mapping m -> f(m).
    """
    primes = consecutive_odd_primes(prime_count)
    P = cumulative_products(primes)

    f_values = {}
    for m in range(1, m_max + 1):
        Rm = compute_R(m)
        # Find smallest s such that P(s) >= R(m)
        found = False
        for s in range(len(P)):
            if P[s] >= Rm:
                f_values[m] = s + 1  # 1-indexed
                found = True
                break
        if not found:
            # Should not happen since P(s) diverges
            f_values[m] = prime_count + 1
    return f_values


def verify_monotonicity(f_values):
    """Verify that f(m) is monotonically non-decreasing.

    Args:
        f_values: Dict mapping m -> f(m).

    Returns:
        Tuple (is_monotone, violations) where violations is a list of m values
        where f(m) < f(m-1).
    """
    violations = []
    m_sorted = sorted(f_values.keys())
    for i in range(1, len(m_sorted)):
        m_prev = m_sorted[i - 1]
        m_curr = m_sorted[i]
        if f_values[m_curr] < f_values[m_prev]:
            violations.append(m_curr)
    return len(violations) == 0, violations


def compute_combined_constraint(f_values, m_max=100):
    """Compute the combined constraint region.

    A pair (m, k) is feasible for a UPN with v_2(n) = m and omega_odd = k if:
      1. k >= f(m)  (product constraint)
      2. m < 2^{2^k}  (Goto bound: n < 2^{2^{k+1}}, simplified via D > 2^m)
         More precisely: m < 2^k  (since 2m < 2^{k+1} => m < 2^k)

    We also compute the effective constraint g(m) = max(f(m), floor(log2(m)) + 1).

    Args:
        f_values: Dict mapping m -> f(m).
        m_max: Maximum m to consider.

    Returns:
        Dict with constraint analysis results.
    """
    results = []
    for m in range(1, m_max + 1):
        fm = f_values[m]
        Rm = compute_R(m)
        log2_m = math.floor(math.log2(m)) + 1 if m >= 1 else 1
        gm = max(fm, log2_m)
        goto_limit = 2 ** gm  # m must be < 2^{g(m)}
        room = goto_limit - m
        feasible = m < goto_limit

        results.append({
            "m": m,
            "R_m": float(Rm),
            "f_m": fm,
            "log2_bound": log2_m,
            "g_m": gm,
            "goto_limit": goto_limit,
            "room": room,
            "feasible": feasible,
        })
    return results


def find_effective_threshold(constraint_results):
    """Find m_0 beyond which the region is 'effectively constrained'.

    Wall (1988) says any new (6th) UPN has >= 9 odd prime factors, i.e., k >= 9.
    Combined with m < 2^k, for k = 9 we get m < 512, and for k = 10 we get
    m < 1024.

    The threshold m_0 is the largest m such that the Wall bound k >= 9
    combined with the Goto bound m < 2^k is the binding constraint (rather
    than f(m)).

    Returns:
        Dict with threshold analysis.
    """
    # With Wall's bound: k >= 9 (for new UPNs)
    # Goto: m < 2^k
    # So for k = 9: m < 512
    # For k = 10: m < 1024
    # etc.
    #
    # The effective threshold is where f(m) first exceeds the Wall bound
    # (which never happens since f(m) <= 5 < 9).
    #
    # More meaningfully: for a NEW UPN:
    #   k >= max(9, f(m)) = 9  (since f(m) <= 5)
    #   m < 2^k where k >= 9
    # So m < 2^9 = 512 is the minimum Goto limit.
    # For k = 10: m < 1024, etc.
    #
    # The region becomes "effectively constrained" in the sense that:
    # - Wall says k >= 9 for new UPNs
    # - Goto says N < 2^{2^{k+1}} = 2^{2^{10}} for k = 9
    #   => N < 2^{1024}
    # This is a finite (but astronomically large) region.

    wall_min_k = 9  # minimum omega_odd for new (6th+) UPN
    wall_total_omega = 10  # minimum omega (including 2)

    # For each k >= wall_min_k, the maximum feasible m is 2^k - 1
    k_values = list(range(wall_min_k, wall_min_k + 10))
    feasible_ranges = []
    for k in k_values:
        max_m = 2 ** k - 1
        feasible_ranges.append({
            "k": k,
            "omega_total": k + 1,
            "max_m_goto": max_m,
            "max_N_log2": 2 ** (k + 1),
        })

    return {
        "wall_min_omega_odd": wall_min_k,
        "wall_min_omega_total": wall_total_omega,
        "note": ("Wall (1988): any new UPN has >= 9 odd prime factors. "
                 "Combined with Goto: for omega_odd = k, v_2(n) = m < 2^k. "
                 "So for k=9: m <= 511, k=10: m <= 1023, etc."),
        "m0_wall_threshold": 2 ** wall_min_k - 1,
        "feasible_ranges_by_k": feasible_ranges,
    }


def create_plots(f_values, constraint_results, threshold_info, figures_dir):
    """Create publication-quality plots.

    Panel 1: f(m) vs m
    Panel 2: Combined constraint region in (m, k) space

    Args:
        f_values: Dict mapping m -> f(m).
        constraint_results: List of constraint dicts.
        threshold_info: Threshold analysis dict.
        figures_dir: Directory to save figures.
    """
    deep = sns.color_palette("deep")
    color_f = deep[0]       # blue
    color_g = deep[1]       # orange
    color_goto = deep[2]    # green
    color_wall = deep[3]    # red
    color_upn = deep[4]     # purple
    color_feasible = deep[8] if len(deep) > 8 else deep[5]  # gray or brown

    # -----------------------------------------------------------------------
    # Create figure with two subplots
    # -----------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # ===== Panel 1: f(m) vs m =====
    ms = sorted(f_values.keys())
    fs = [f_values[m] for m in ms]

    ax1.step(ms, fs, where='post', color=color_f, linewidth=2.0,
             label=r'$f(m)$', zorder=3)
    ax1.scatter(ms, fs, color=color_f, s=12, zorder=4, alpha=0.7)

    # Also plot g(m) = max(f(m), floor(log2(m)) + 1)
    gs = [max(f_values[m], math.floor(math.log2(m)) + 1) for m in ms]
    ax1.step(ms, gs, where='post', color=color_g, linewidth=1.8,
             linestyle='--', label=r'$g(m) = \max(f(m),\, \lfloor\log_2 m\rfloor + 1)$',
             zorder=2)

    # Mark known UPNs
    for upn in KNOWN_UPNS:
        ax1.scatter(upn["m"], f_values.get(upn["m"], 0), marker='*', s=200,
                    color=color_upn, edgecolors='black', linewidths=0.5,
                    zorder=5)
    # One legend entry for UPNs
    ax1.scatter([], [], marker='*', s=200, color=color_upn, edgecolors='black',
                linewidths=0.5, label='Known UPNs')

    # R(m) asymptote annotation
    ax1.axhline(y=5, color='gray', linewidth=0.5, linestyle=':', alpha=0.5)
    ax1.text(85, 5.15, r'$f(m)=5$ plateau', fontsize=9, color='gray',
             ha='center', va='bottom')

    ax1.set_xlabel(r'$m = v_2(n)$ (2-adic valuation)')
    ax1.set_ylabel(r'$f(m)$ (minimum odd prime factors)')
    ax1.set_title(r'Growth Constraint $f(m)$')
    ax1.set_xlim(0, 101)
    ax1.set_ylim(0, max(gs) + 1.5)
    ax1.legend(loc='upper left', frameon=True)

    # ===== Panel 2: Combined constraint region in (m, k) space =====
    # We show m on x-axis and k (omega_odd) on y-axis.
    # Region where k >= f(m): above the f(m) step curve
    # Region where m < 2^k: below the doubly-exponential boundary
    # Feasible region: intersection of both

    # f(m) curve (lower bound on k)
    m_range = np.arange(1, 101)
    f_curve = np.array([f_values[m] for m in m_range])

    ax2.fill_between(m_range, f_curve, 0, alpha=0.15, color='gray',
                     label=r'$k < f(m)$ (infeasible)')
    ax2.step(m_range, f_curve, where='post', color=color_f, linewidth=2.0,
             label=r'$k = f(m)$ (product bound)', zorder=3)

    # Goto bound: m < 2^k  =>  k > log2(m)
    # Plot the curve k = log2(m) (below which m >= 2^k, so infeasible)
    m_cont = np.linspace(1, 100, 500)
    k_goto_bound = np.log2(m_cont)
    ax2.plot(m_cont, k_goto_bound, color=color_goto, linewidth=2.0,
             linestyle='-.', label=r'$k = \log_2(m)$ (Goto bound)', zorder=3)

    # The ACTUAL doubly exponential: m < 2^{2^k} means k > log2(log2(m))
    # For the plot range m in [1, 100], log2(log2(m)) is very small
    # (log2(log2(100)) ~ 2.7), so the Goto bound in its original form
    # is extremely permissive for small m.
    # Let us instead show the inverse: for each k, the max m is 2^k - 1
    k_vals_for_region = np.arange(1, 16)
    m_goto_limits = np.array([2**k for k in k_vals_for_region])

    # Shade feasible region (above f(m), below Goto limit)
    # Use fill_betweenx to shade where k >= f(m) AND m < 2^k
    k_grid = np.arange(1, 15)
    for k in k_grid:
        m_max_goto = min(2**k - 1, 100)
        # f(m) <= k for all m where f(m) <= k
        m_start = 1
        m_end = m_max_goto
        if m_end >= m_start:
            ms_in_range = np.arange(m_start, m_end + 1)
            f_in_range = np.array([f_values.get(int(m_val), 5) for m_val in ms_in_range])
            feasible_mask = f_in_range <= k
            if np.any(feasible_mask):
                feasible_ms = ms_in_range[feasible_mask]
                if len(feasible_ms) > 0:
                    ax2.fill_between(
                        [feasible_ms[0], feasible_ms[-1]],
                        k, k + 0.4, alpha=0.06, color=color_goto
                    )

    # Wall's bound for new UPNs: k >= 9
    ax2.axhline(y=9, color=color_wall, linewidth=1.5, linestyle='--',
                alpha=0.8, label=r"Wall's bound: $k \geq 9$ (new UPNs)",
                zorder=2)
    ax2.fill_between([0, 100], 0, 9, alpha=0.08, color=color_wall)

    # Plot Goto staircase: vertical lines showing m = 2^k limits
    for k in range(1, 12):
        m_limit = 2 ** k
        if m_limit <= 110:
            ax2.axvline(x=m_limit, color=color_goto, linewidth=0.6,
                        linestyle=':', alpha=0.4)
            if m_limit <= 100:
                ax2.text(m_limit, 13.3, rf'$2^{{{k}}}$', fontsize=7,
                         ha='center', color=color_goto, alpha=0.7)

    # Plot known UPNs as points in (m, k=omega_odd) space
    for upn in KNOWN_UPNS:
        ax2.scatter(upn["m"], upn["omega_odd"], marker='D', s=80,
                    color=color_upn, edgecolors='black', linewidths=0.6,
                    zorder=5)
        offset_x = 2 if upn["m"] < 15 else -3
        offset_y = 0.5
        ax2.annotate(upn["label"], (upn["m"], upn["omega_odd"]),
                     xytext=(upn["m"] + offset_x, upn["omega_odd"] + offset_y),
                     fontsize=8, color=color_upn, ha='center',
                     arrowprops=dict(arrowstyle='->', color=color_upn,
                                     lw=0.6, connectionstyle='arc3,rad=0.2'))

    ax2.scatter([], [], marker='D', s=80, color=color_upn, edgecolors='black',
                linewidths=0.6, label='Known UPNs')

    ax2.set_xlabel(r'$m = v_2(n)$ (2-adic valuation)')
    ax2.set_ylabel(r'$k = \omega_{\mathrm{odd}}(n)$ (distinct odd primes)')
    ax2.set_title('Combined Constraint Region')
    ax2.set_xlim(0, 101)
    ax2.set_ylim(0, 14)
    ax2.legend(loc='upper left', frameon=True, fontsize=9)

    # -----------------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------------
    plt.tight_layout()

    png_path = os.path.join(figures_dir, "growth_constraint.png")
    pdf_path = os.path.join(figures_dir, "growth_constraint.pdf")
    fig.savefig(png_path, dpi=300)
    fig.savefig(pdf_path)
    plt.close(fig)
    print(f"Saved: {png_path}")
    print(f"Saved: {pdf_path}")


def main():
    """Run the full growth constraint validation."""
    # Resolve paths relative to repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    figures_dir = os.path.join(repo_root, "figures")
    results_dir = os.path.join(repo_root, "results")
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    print("=" * 70)
    print("Growth Constraint Validation for Unitary Perfect Numbers")
    print("=" * 70)

    # ------------------------------------------------------------------
    # Step 1: Compute f(m) for m = 1..100
    # ------------------------------------------------------------------
    print("\n--- Step 1: Computing f(m) for m = 1..100 ---")
    M_MAX = 100
    f_values = compute_f(m_max=M_MAX, prime_count=200)

    print(f"{'m':>4}  {'R(m)':>12}  {'f(m)':>5}")
    print("-" * 28)
    for m in range(1, M_MAX + 1):
        Rm = compute_R(m)
        if m <= 20 or m % 10 == 0:
            print(f"{m:>4}  {float(Rm):>12.8f}  {f_values[m]:>5}")
    print(f"  ... (computed for all m = 1..{M_MAX})")

    # ------------------------------------------------------------------
    # Step 2: Verify monotonicity
    # ------------------------------------------------------------------
    print("\n--- Step 2: Verifying monotonicity ---")
    is_mono, violations = verify_monotonicity(f_values)
    if is_mono:
        print("  f(m) is monotonically non-decreasing. PASS")
    else:
        print(f"  FAIL: f(m) is NOT monotone. Violations at m = {violations}")

    # ------------------------------------------------------------------
    # Step 3: Combined constraint region
    # ------------------------------------------------------------------
    print("\n--- Step 3: Computing combined constraint region ---")
    constraint_results = compute_combined_constraint(f_values, m_max=M_MAX)
    threshold_info = find_effective_threshold(constraint_results)
    print(f"  Wall's minimum omega_odd for new UPN: "
          f"{threshold_info['wall_min_omega_odd']}")
    print(f"  Maximum m for k=9 (Goto): {2**9 - 1}")
    print(f"  Maximum m for k=10 (Goto): {2**10 - 1}")

    # Check feasibility across all m
    all_feasible = all(r["feasible"] for r in constraint_results)
    print(f"  All (m, g(m)) pairs feasible under Goto: {all_feasible}")

    if all_feasible:
        print("  => Combined constraints do NOT create an empty region for "
              "m <= 100.")
        print("     The Goto bound is doubly exponential and always provides "
              "room.")
    else:
        infeasible = [r["m"] for r in constraint_results if not r["feasible"]]
        print(f"  Infeasible m values: {infeasible}")

    # Determine m_0: threshold beyond which Wall's k >= 9 is binding
    # (rather than f(m) <= 5)
    m0 = None
    for r in constraint_results:
        if r["g_m"] >= 9:
            m0 = r["m"]
            break
    if m0 is None:
        # For m <= 100, g(m) = max(5, floor(log2(m))+1)
        # g(m) >= 9 when floor(log2(m))+1 >= 9, i.e., m >= 256
        m0 = 256  # beyond our computation range but we know it analytically
    print(f"  Effective threshold m_0 (where g(m) >= 9, matching Wall): "
          f"m_0 = {m0}")
    print("  Note: For new (6th+) UPNs, Wall requires k >= 9.")
    print(f"  With k >= 10 (omega >= 11), Goto gives m < 2^10 = 1024.")

    # ------------------------------------------------------------------
    # Step 4: Create plots
    # ------------------------------------------------------------------
    print("\n--- Step 4: Creating publication-quality plots ---")
    create_plots(f_values, constraint_results, threshold_info, figures_dir)

    # ------------------------------------------------------------------
    # Step 5: Save numerical results
    # ------------------------------------------------------------------
    print("\n--- Step 5: Saving numerical results ---")

    # Prepare JSON-serializable output
    f_table = []
    for m in range(1, M_MAX + 1):
        Rm = compute_R(m)
        gm = max(f_values[m], math.floor(math.log2(m)) + 1)
        f_table.append({
            "m": m,
            "R_m": float(Rm),
            "R_m_exact": str(Rm),
            "f_m": f_values[m],
            "g_m": gm,
            "goto_limit": 2 ** gm,
            "room": 2 ** gm - m,
            "feasible": m < 2 ** gm,
        })

    # Cumulative product table
    primes = consecutive_odd_primes(20)
    P = cumulative_products(primes)
    product_table = []
    for i, (q, Ps) in enumerate(zip(primes, P)):
        product_table.append({
            "s": i + 1,
            "prime": q,
            "P_s": float(Ps),
            "P_s_exact": str(Ps),
            "exceeds_2": Ps >= 2,
        })

    # Known UPN verification
    upn_verification = []
    for upn in KNOWN_UPNS:
        m = upn["m"]
        fm = f_values.get(m, None)
        upn_verification.append({
            "n": str(upn["n"]),
            "m": m,
            "omega_odd_actual": upn["omega_odd"],
            "f_m": fm,
            "satisfies_product_bound": upn["omega_odd"] >= fm if fm else None,
            "omega_total": upn["omega"],
        })

    output = {
        "description": ("Validation of growth constraint f(m) for unitary "
                        "perfect numbers"),
        "m_range": [1, M_MAX],
        "monotonicity": {
            "is_non_decreasing": is_mono,
            "violations": violations,
        },
        "f_m_summary": {
            "min_f": min(f_values.values()),
            "max_f": max(f_values.values()),
            "f_stabilizes_at": 5,
            "stabilization_m": 9,
            "note": ("f(m) = 5 for all m >= 9, because P(5) = 1536/715 ~ "
                     "2.148 > R(m) for all m"),
        },
        "f_table": f_table,
        "cumulative_product_table": product_table,
        "known_upn_verification": upn_verification,
        "combined_constraint": {
            "wall_threshold": threshold_info,
            "all_feasible_up_to_100": all_feasible,
            "effective_m0": m0,
            "note": ("The combined constraint region {(m,k): k >= f(m) and "
                     "m < 2^k} is non-empty for all m >= 1. Goto's doubly "
                     "exponential bound always provides room. For new UPNs, "
                     "Wall's k >= 9 bound with Goto gives m < 512."),
        },
        "figures": [
            "figures/growth_constraint.png",
            "figures/growth_constraint.pdf",
        ],
    }

    json_path = os.path.join(results_dir, "growth_validation.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"  Saved: {json_path}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  f(m) computed for m = 1..{M_MAX}")
    print(f"  Monotonically non-decreasing: {is_mono}")
    print(f"  f(m) stabilizes at 5 for m >= 9")
    print(f"  g(m) = max(f(m), floor(log2(m))+1) dominates for m >= 32")
    print(f"  Combined region never empty (Goto bound always has room)")
    print(f"  Wall (1988): new UPNs need k >= 9 => m < 512 for the minimum case")
    print(f"  All known UPNs satisfy the growth constraint")
    print("=" * 70)


if __name__ == "__main__":
    main()
