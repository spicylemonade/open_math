# Baseline Metrics: Kissing Number Bounds by Dimension

| Dimension | Known Lower | Known Upper | Cap-Packing Bound | Delsarte LP | SDP Bound (M-V) | Our Recurrence |
|-----------|-------------|-------------|-------------------|-------------|-----------------|----------------|
|         2 |           6 |           6 |                 6 |           6 |               6 |              6 |
|         3 |          12 |          12 |                14 |          13 |              12 |             14 |
|         4 |          24 |          24 |                34 |          25 |              24 |             34 |
|         5 |          40 |          44 |                77 |          46 |              44 |             77 |
|         6 |          72 |          77 |               170 |          82 |              77 |            170 |
|         7 |         126 |         134 |               368 |         140 |             134 |            368 |
|         8 |         240 |         240 |               788 |         240 |             240 |            788 |

## Notes

- **Known Lower/Upper**: Best known bounds from the literature (see sources.bib)
- **Cap-Packing Bound**: S_{n-1} / A_cap(n, pi/6), the simple area ratio bound
- **Delsarte LP**: Optimal LP bound using Gegenbauer polynomials (Odlyzko-Sloane 1979)
- **SDP Bound (M-V)**: Semidefinite programming bound (Mittelmann-Vallentin 2010)
- **Our Recurrence**: Bound from dimensional analysis framework (= cap-packing in Phase 2)

## Key Observations

1. The cap-packing bound is exponentially weaker than Delsarte LP in higher dimensions
2. Delsarte LP is tight for n=2, 8 (and n=24, not shown)
3. SDP improves on LP significantly for n=5,6,7 (from 46->44, 82->77, 140->134)
4. The gap between lower and SDP bounds is widest for n=5 (40 vs 44)
5. For n=5, the dimensional analysis framework provides geometric insight but the simple
   cap bound (77) is much weaker. The value of the framework is in providing additional
   constraints for the LP/SDP, explored in Phase 3.

## Verification Status

- D5 lattice (40 vectors): VERIFIED (all pairwise angles >= 60 degrees)
- Known polynomial for n=8: VERIFIED (f(1)/f_0 = 240.0000 exactly)
- Cap-packing bounds: VERIFIED via ndim_geometry.py
- All numerical computations use fixed seed 42 and are reproducible