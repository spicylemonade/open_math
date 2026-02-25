# Statistical Significance Testing

## Methods
- Wilcoxon signed-rank test (non-parametric paired test)
- 95% confidence intervals for mean difference
- Cohen's d effect size

## hybrid_vs_lkh_10s
- Paired samples: 9
- Mean cost difference: 113.87
- Wilcoxon p-value: 0.0039
- 95% CI: [94.50, 133.24]
- Cohen's d: 3.841
- Significant (p<0.05): Yes

## hybrid_vs_ortools_10s
- Paired samples: 9
- Mean cost difference: 42.62
- Wilcoxon p-value: 0.2500
- 95% CI: [0.77, 84.47]
- Cohen's d: 0.665
- Significant (p<0.05): No

## hybrid_vs_lkh_30s
- Paired samples: 9
- Mean cost difference: -54.81
- Wilcoxon p-value: 0.0508
- 95% CI: [-100.58, -9.04]
- Cohen's d: -0.782
- Significant (p<0.05): No

## hybrid_vs_ortools_30s
- Paired samples: 9
- Mean cost difference: 10.76
- Wilcoxon p-value: 0.0312
- 95% CI: [3.06, 18.46]
- Cohen's d: 0.913
- Significant (p<0.05): Yes

## Interpretation

The tests measure whether tour cost differences between the hybrid solver
and baselines are systematic across instances and seeds. Small sample sizes
(N=9 pairs) limit statistical power, so effect sizes (Cohen's d) provide
additional insight into practical significance.
