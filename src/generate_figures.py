"""Generate publication-quality figures for the UPN research report."""

import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from fractions import Fraction
from sympy import primerange

from src.unitary import KNOWN_UPN_FACTORIZATIONS


def figure_known_upn_factorizations():
    """Figure 1: Prime factorization structure of all 5 known UPNs."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Bar chart of prime factorizations for the first 4 UPNs
    ax = axes[0]
    upns_small = [6, 60, 90, 87360]
    all_primes = sorted(set(p for n in upns_small for p in KNOWN_UPN_FACTORIZATIONS[n]))
    x = np.arange(len(all_primes))
    width = 0.2
    colors = sns.color_palette("deep", 4)
    for i, n in enumerate(upns_small):
        fact = KNOWN_UPN_FACTORIZATIONS[n]
        vals = [fact.get(p, 0) for p in all_primes]
        ax.bar(x + i * width, vals, width, label=f'n = {n}', color=colors[i], edgecolor='black', linewidth=0.5)

    ax.set_xlabel('Prime Factor', fontsize=12)
    ax.set_ylabel('Exponent', fontsize=12)
    ax.set_title('(a) First Four Known UPNs', fontsize=13)
    ax.set_xticks(x + 1.5 * width)
    ax.set_xticklabels([str(p) for p in all_primes], fontsize=11)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 7)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Panel B: The 5th UPN factorization
    ax = axes[1]
    n5 = 146361946186458562560000
    fact5 = KNOWN_UPN_FACTORIZATIONS[n5]
    primes5 = sorted(fact5.keys())
    exps5 = [fact5[p] for p in primes5]
    bar_colors = ['#e74c3c' if p == 2 else '#3498db' for p in primes5]
    bars = ax.bar(range(len(primes5)), exps5, color=bar_colors, edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Prime Factor', fontsize=12)
    ax.set_ylabel('Exponent', fontsize=12)
    ax.set_title(r'(b) Fifth UPN: $n_5 \approx 1.46 \times 10^{23}$', fontsize=13)
    ax.set_xticks(range(len(primes5)))
    ax.set_xticklabels([str(p) for p in primes5], fontsize=9, rotation=45)
    ax.set_ylim(0, 20)
    # Annotate key features
    ax.annotate(r'$v_2 = 18$', xy=(0, 18), xytext=(1.5, 19),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax.annotate(r'$5^4$', xy=(2, 4), xytext=(3, 6),
                arrowprops=dict(arrowstyle='->', color='blue'), fontsize=10, color='blue')

    plt.tight_layout()
    plt.savefig('figures/known_upn_factorizations.png', dpi=150, bbox_inches='tight')
    plt.savefig('figures/known_upn_factorizations.pdf', bbox_inches='tight')
    plt.close()
    print("  Saved figures/known_upn_factorizations.png")


def figure_product_equation_solutions():
    """Figure 2: Product equation solution space for different k."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Maximum achievable product P(k) vs k
    ax = axes[0]
    odd_primes = list(primerange(3, 500))
    k_vals = list(range(1, 51))
    max_products = []
    product = 1.0
    for i, k in enumerate(k_vals):
        product *= (1 + 1.0 / odd_primes[i])
        max_products.append(product)

    ax.plot(k_vals, max_products, 'b-', linewidth=2, label=r'$P(k) = \prod_{i=1}^{k}(1+1/q_i)$')
    ax.axhline(y=2.0, color='r', linestyle='--', linewidth=1.5, label='Target = 2')
    # Mark where P(k) crosses 2
    ax.axvline(x=5, color='green', linestyle=':', linewidth=1, alpha=0.7)
    ax.annotate('P(4) < 2 < P(5)', xy=(5, 2), xytext=(15, 1.5),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=10, color='green')
    # Mark known UPN solutions
    upn_omegas = {6: 2, 60: 3, 90: 3, 87360: 5, 146361946186458562560000: 12}
    for n, k in upn_omegas.items():
        ax.plot(k, 2.0, 'r*', markersize=12, zorder=5)
    ax.set_xlabel('Number of distinct prime factors (k)', fontsize=12)
    ax.set_ylabel(r'Maximum product $P(k)$', fontsize=12)
    ax.set_title('(a) Maximum Achievable Product vs. k', fontsize=13)
    ax.legend(fontsize=10, loc='lower right')
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 6)

    # Panel B: Contribution of each prime (1+1/p) showing diminishing returns
    ax = axes[1]
    primes_to_plot = list(primerange(2, 200))
    contributions = [1 + 1.0/p for p in primes_to_plot]
    ax.scatter(primes_to_plot, contributions, c='steelblue', s=15, alpha=0.7,
               label=r'$(1 + 1/p)$ per prime')
    # Mark the threshold where individual contribution < 1.01
    ax.axhline(y=1.01, color='orange', linestyle='--', linewidth=1, label='Contribution = 1.01')
    ax.axhline(y=1.0, color='red', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.set_xlabel('Prime p', fontsize=12)
    ax.set_ylabel(r'Factor $(1 + 1/p)$', fontsize=12)
    ax.set_title('(b) Diminishing Prime Power Contributions', fontsize=13)
    ax.legend(fontsize=10)
    ax.set_ylim(0.99, 1.55)

    plt.tight_layout()
    plt.savefig('figures/product_equation_solutions.png', dpi=150, bbox_inches='tight')
    plt.savefig('figures/product_equation_solutions.pdf', bbox_inches='tight')
    plt.close()
    print("  Saved figures/product_equation_solutions.png")


def figure_modular_sieve_density():
    """Figure 3: Cumulative sieve density as modulus increases."""
    # Load the modular validation results
    with open('results/modular_validation.json') as f:
        data = json.load(f)

    by_modulus = data['sieve_details']['by_modulus']
    moduli = [d['modulus'] for d in by_modulus]
    cumulative = [d['cumulative_density'] for d in by_modulus]
    individual = [d['density'] for d in by_modulus]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Cumulative sieve density
    ax = axes[0]
    ax.plot(moduli, cumulative, 'b-o', markersize=4, linewidth=1.5,
            label='Cumulative sieve density')
    ax.axhline(y=data['sieve_density'], color='red', linestyle='--', linewidth=1,
               label=f'Final density = {data["sieve_density"]:.4f}')
    ax.set_xlabel('Prime modulus q', fontsize=12)
    ax.set_ylabel('Cumulative sieve density', fontsize=12)
    ax.set_title('(a) Cumulative Sieve Density vs. Modulus', fontsize=13)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.1)

    # Panel B: Individual density per prime
    ax = axes[1]
    bars = ax.bar(range(len(moduli)), individual, color='steelblue',
                  edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Prime modulus q', fontsize=12)
    ax.set_ylabel('Fraction of allowed residues', fontsize=12)
    ax.set_title('(b) Allowed Fraction per Prime Modulus', fontsize=13)
    ax.set_xticks(range(len(moduli)))
    ax.set_xticklabels([str(q) for q in moduli], fontsize=8, rotation=45)
    ax.set_ylim(0, 1.1)
    ax.axhline(y=1.0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    # Annotate primes with strongest exclusion
    min_density = min(individual)
    min_idx = individual.index(min_density)
    ax.annotate(f'{min_density:.2f}', xy=(min_idx, min_density),
                xytext=(min_idx + 2, min_density + 0.15),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10, color='red')

    plt.tight_layout()
    plt.savefig('figures/modular_sieve_density.png', dpi=150, bbox_inches='tight')
    plt.savefig('figures/modular_sieve_density.pdf', bbox_inches='tight')
    plt.close()
    print("  Saved figures/modular_sieve_density.png")


def main():
    """Generate all figures."""
    print("=== Generating Publication-Quality Figures ===\n")

    sns.set_style("whitegrid")
    plt.rcParams.update({
        'font.size': 11,
        'axes.titlesize': 13,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.dpi': 150,
    })

    print("1. Known UPN factorizations...")
    figure_known_upn_factorizations()

    print("2. Product equation solution space...")
    figure_product_equation_solutions()

    print("3. Modular sieve density...")
    figure_modular_sieve_density()

    print("\nAll figures generated. Existing: figures/growth_constraint.png (from item_019)")
    print("Total: 4 figures (+ PDF versions)")


if __name__ == "__main__":
    main()
