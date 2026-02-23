# Literature Review: MDS Approximation Algorithms for Planar and Sparse Graph Classes

**Project:** Tightening the Practical Polynomial-Time Approximation Ratio for Minimum Dominating Set on Planar Graphs
**Date:** 2026-02-23
**Status:** Complete

---

## Overview

This document surveys the state of the art on Minimum Dominating Set (MDS) approximation
algorithms for planar graphs and related sparse graph classes. Papers are organized into six
thematic categories as required by the research rubric (item_003). For each paper we provide:
authors, year, title, venue, key result, technique used, and relevance to our research.

All BibTeX entries are collected in `sources.bib` at the repository root (25 entries).

---

## Category (a): Baker's Technique and PTAS Variants

### Paper 1 -- Baker (1994)

| Field | Value |
|-------|-------|
| **Authors** | Brenda S. Baker |
| **Year** | 1994 |
| **Title** | Approximation Algorithms for NP-Complete Problems on Planar Graphs |
| **Venue** | Journal of the ACM, 41(1):153--180 |
| **Key Result** | PTAS for a broad class of NP-hard problems on planar graphs, including MDS, via k-outerplanar decomposition. With the corrected application (see Marzban & Gu 2013), gives a (1+2/k)-approximation in O(2^{ck} n) time. |
| **Technique** | BFS-layering decomposes a planar graph into k-outerplanar subgraphs of bounded treewidth; dynamic programming solves each piece exactly; solutions are combined with a shifting argument to obtain a (1+2/k) ratio. |
| **Relevance** | Foundational baseline. Our project aims to achieve a practical constant-factor algorithm that runs faster than Baker's PTAS for moderate k while giving competitive approximation ratios. Baker's framework is also a building block for our separator-based decomposition approach. |
| **BibTeX Key** | `Baker1994` |

### Paper 2 -- Demaine & Hajiaghayi (2005)

| Field | Value |
|-------|-------|
| **Authors** | Erik D. Demaine, MohammadTaghi Hajiaghayi |
| **Year** | 2005 |
| **Title** | Bidimensionality: New Connections between FPT Algorithms and PTASs |
| **Venue** | SODA 2005, pp. 590--601 |
| **Key Result** | Unified framework giving PTASs and EPTASs for all bidimensional problems (including MDS) on planar and H-minor-free graphs. First PTASs for connected dominating set and feedback vertex set on planar graphs. |
| **Technique** | Bidimensionality theory: if a problem's value on a k x k grid is Omega(k^2) and is monotone under contraction/deletion, then (i) treewidth is O(sqrt(OPT)), enabling subexponential FPT, and (ii) separator of size O(sqrt(OPT)) enables PTAS. Unifies Baker's layering and Lipton-Tarjan separator approaches. |
| **Relevance** | Provides the theoretical ceiling for what approximation schemes can achieve on planar graphs. The separator-of-size-O(sqrt(OPT)) result directly motivates our separator-based algorithm design (Phase 3). The connection between treewidth and OPT size is crucial for our proof sketch. |
| **BibTeX Key** | `DemaineHajiaghayi2005` |

### Paper 3 -- Fomin, Lokshtanov, Raman & Saurabh (2011)

| Field | Value |
|-------|-------|
| **Authors** | Fedor V. Fomin, Daniel Lokshtanov, Venkatesh Raman, Saket Saurabh |
| **Year** | 2011 (arXiv 2010) |
| **Title** | Bidimensionality and EPTAS |
| **Venue** | arXiv:1005.5449 (STACS 2011) |
| **Key Result** | Decomposition lemma: for bidimensional problems on H-minor-free graphs, one can find a set X of size eps * OPT such that treewidth of G \ X is f(eps), yielding EPTASs. |
| **Technique** | Extends bidimensionality to efficient PTASs by removing a small fraction of OPT and reducing treewidth, enabling DP on the remaining graph. Covers packing problems and partial covering. |
| **Relevance** | Strengthens the theoretical foundation. The EPTAS running time 2^{O(1/eps)} n^{O(1)} is the best known for MDS on planar graphs, but the constant in the exponent makes it impractical for small eps. This motivates our search for practical algorithms with explicit (if larger) constant-factor guarantees. |
| **BibTeX Key** | `FominLokshtanovRamanSaurabh2011` |

### Paper 4 -- Marzban & Gu (2013)

| Field | Value |
|-------|-------|
| **Authors** | Marjan Marzban, Qian-Ping Gu |
| **Year** | 2013 |
| **Title** | Computational Study on a PTAS for Planar Dominating Set Problem |
| **Venue** | Algorithms (MDPI), 6(1):43--59 |
| **Key Result** | Shows that Baker's original direct application has an approximation ratio that is unbounded for MDS. Provides a corrected PTAS with ratio (1+2/k). First computational evaluation of a PTAS for planar MDS -- finds near-optimal solutions in practical time. |
| **Technique** | Modified BFS-layering: carefully handles boundary vertices between layers to maintain domination invariant. Computational study compares against heuristics and exact branch-width solver. |
| **Relevance** | Directly relevant as the only published computational study of PTAS for planar MDS. Their experimental methodology (comparing against exact solver on small instances, heuristics on larger) is a template for our Phase 4 experiments. |
| **BibTeX Key** | `MarzbanGu2013` |

---

## Category (b): Greedy and Modified-Greedy Approaches

### Paper 5 -- Dvorak (2013)

| Field | Value |
|-------|-------|
| **Authors** | Zdenek Dvorak |
| **Year** | 2013 |
| **Title** | Constant-factor approximation of the domination number in sparse graphs |
| **Venue** | European Journal of Combinatorics, 34(5):833--840 |
| **Key Result** | Linear-time constant-factor approximation for distance-r dominating sets on any graph class with bounded expansion (which includes planar graphs). Bounds MDS size in terms of maximum independent set size and generalized coloring numbers. |
| **Technique** | Uses the characterization of bounded expansion via generalized coloring numbers (grad_r). The ratio between domination number and 2r-independence number is bounded by a function of the expansion parameters. |
| **Relevance** | Provides the theoretical basis for constant-factor approximation on planar graphs without LP solving. The dependence on generalized coloring numbers suggests that planar-specific structure (arboricity <= 3, genus 0) should yield small concrete constants, which our experiments will measure. |
| **BibTeX Key** | `Dvorak2013` |

### Paper 6 -- Siebertz (2019)

| Field | Value |
|-------|-------|
| **Authors** | Sebastian Siebertz |
| **Year** | 2019 |
| **Title** | Greedy domination on biclique-free graphs |
| **Venue** | Information Processing Letters, 145:64--67 |
| **Key Result** | Modified greedy algorithm gives O(t * ln k)-approximation on K_{t,t}-free graphs, where k = gamma(G). Matching hardness of approximation on K_{3,3}-free graphs. |
| **Technique** | Extends the Jones et al. approach: instead of selecting the vertex covering the most uncovered vertices, the modification considers the ratio of new coverage to existing coverage. The biclique-free structure ensures bounded "density" in neighborhoods. |
| **Relevance** | Planar graphs are K_{3,3}-free (by Kuratowski's theorem), so this gives a concrete O(ln k) modified greedy bound for our graph class. The simplicity of implementation makes this an important baseline algorithm for our benchmark suite. |
| **BibTeX Key** | `Siebertz2019` |

### Paper 7 -- Dvorak (2019)

| Field | Value |
|-------|-------|
| **Authors** | Zdenek Dvorak |
| **Year** | 2019 |
| **Title** | On distance r-dominating and 2r-independent sets in sparse graphs |
| **Venue** | Journal of Graph Theory, 91(2):162--173 |
| **Key Result** | Improved bounds on the ratio gamma_r(G) / alpha_{2r}(G) for graphs with bounded expansion, using LP-based arguments. The approximation factor depends only on the expansion parameters. |
| **Technique** | LP relaxation combined with structural arguments from bounded expansion theory; inspired by Bansal-Umboh primal-dual approach. |
| **Relevance** | Bridges the greedy and LP-based approaches. The LP-informed bounds are tighter than purely combinatorial ones, suggesting our hybrid algorithm (LP + structural decomposition) has theoretical merit. |
| **BibTeX Key** | `Dvorak2019` |

---

## Category (c): LP-Based Methods and Integrality Gap Results

### Paper 8 -- Bansal & Umboh (2017)

| Field | Value |
|-------|-------|
| **Authors** | Nikhil Bansal, Seeun William Umboh |
| **Year** | 2017 |
| **Title** | Tight approximation bounds for dominating set on graphs of bounded arboricity |
| **Venue** | Information Processing Letters, 122:21--24 |
| **Key Result** | (2*alpha+1)-approximation for MDS on graphs of arboricity alpha via LP rounding. NP-hard to achieve (alpha-1-eps). For planar graphs (alpha <= 3), this gives a 7-approximation. |
| **Technique** | LP relaxation of the standard MDS ILP; rounding exploits the bounded arboricity to charge fractional values to a forest decomposition. Near-linear time via approximate LP solvers. |
| **Relevance** | Central to our LP-based approach. The bounded integrality gap (at most alpha+1 by Sun 2021) on planar graphs means our LP relaxation provides a strong lower bound. The 7-approximation is a concrete target to beat with our hybrid approach. |
| **BibTeX Key** | `BansalUmboh2017` |

### Paper 9 -- Sun (2021)

| Field | Value |
|-------|-------|
| **Authors** | Kevin Sun |
| **Year** | 2021 |
| **Title** | An Improved Approximation Bound for Minimum Weight Dominating Set on Graphs of Bounded Arboricity |
| **Venue** | WAOA 2021, LNCS 13059:39--53 |
| **Key Result** | Primal-dual algorithm showing the natural LP for MDS has integrality gap at most arboricity+1. For planar graphs, this means LP gap <= 4. |
| **Technique** | Primal-dual method: constructs dual feasible solution whose value matches the primal integral solution to within the arboricity+1 factor. Generalizes to weighted MDS. |
| **Relevance** | The LP integrality gap bound of 4 for planar graphs is a key structural result for our research. It means LP lower bounds are within a factor of 4 of OPT, enabling meaningful approximation ratio measurements even when exact OPT is unknown. This directly supports our experimental methodology (Phase 4). |
| **BibTeX Key** | `Sun2021` |

### Paper 10 -- Morgan, Solomon & Wein (2021)

| Field | Value |
|-------|-------|
| **Authors** | Adir Morgan, Shay Solomon, Nicole Wein |
| **Year** | 2021 |
| **Title** | Algorithms for the Minimum Dominating Set Problem in Bounded Arboricity Graphs: Simpler, Faster, and Combinatorial |
| **Venue** | DISC 2021, LIPIcs 209:33:1--33:19 |
| **Key Result** | First non-LP-based O(alpha)-approximation for MDS on bounded arboricity graphs, running in linear time. Also gives a randomized O(alpha log n)-round O(alpha)-approximation in the distributed CONGEST model. |
| **Technique** | Simple combinatorial algorithm based on iterative vertex selection using arboricity-based neighborhood counting. Avoids LP solving entirely while matching the LP-based approximation ratio asymptotically. |
| **Relevance** | Shows that LP solving is not strictly necessary to achieve O(alpha) ratios. Their linear-time centralized algorithm is an important practical baseline. For planar graphs, this gives an O(1)-approximation in O(n) time -- directly comparable to our hybrid approach. |
| **BibTeX Key** | `MorganSolomonWein2021` |

---

## Category (d): Distributed MDS Approximation

### Paper 11 -- Lenzen, Oswald & Wattenhofer (2008)

| Field | Value |
|-------|-------|
| **Authors** | Christoph Lenzen, Yvonne Anne Oswald, Roger Wattenhofer |
| **Year** | 2008 |
| **Title** | What Can Be Approximated Locally? Case Study: Dominating Sets in Planar Graphs |
| **Venue** | SPAA 2008, pp. 46--54 |
| **Key Result** | First constant-round 126-approximation for MDS on planar graphs in the LOCAL model of distributed computing. |
| **Technique** | Two-phase local algorithm: (1) vertices with neighborhoods not covered by <= 6 other nodes join the dominating set; (2) uncovered vertices elect a maximum-residual-degree neighbor. Uses only 2-hop information. |
| **Relevance** | Initiated the systematic study of distributed MDS on planar graphs. While the 126-approximation ratio is loose, the two-phase structure of their algorithm (structural selection + greedy cleanup) inspires our hybrid approach. |
| **BibTeX Key** | `LenzenOswaldWattenhofer2008` |

### Paper 12 -- Lenzen, Pignolet & Wattenhofer (2013)

| Field | Value |
|-------|-------|
| **Authors** | Christoph Lenzen, Yvonne Anne Pignolet, Roger Wattenhofer |
| **Year** | 2013 |
| **Title** | Distributed minimum dominating set approximations in restricted families of graphs |
| **Venue** | Distributed Computing, 26:119--137 |
| **Key Result** | 52-approximation for MDS on planar graphs in constant LOCAL rounds. Asymptotically tight trade-off between rounds and approximation ratio for unit disk graphs. |
| **Technique** | Refined local rules based on structural properties of planar graph neighborhoods. Builds on the 2008 framework with tighter analysis. |
| **Relevance** | The 52-approximation was the state of the art before Heydt et al. 2025. The tight trade-off results for unit disk graphs suggest inherent limitations of purely local approaches, motivating our use of global structure (separators, LP). |
| **BibTeX Key** | `LenzenPignoletWattenhofer2013` |

### Paper 13 -- Czygrinow, Hanckowiak & Wawrzyniak (2008)

| Field | Value |
|-------|-------|
| **Authors** | Andrzej Czygrinow, Michal Hanckowiak, Wojciech Wawrzyniak |
| **Year** | 2008 |
| **Title** | Fast Distributed Approximations in Planar Graphs |
| **Venue** | DISC 2008, LNCS 5218:78--92 |
| **Key Result** | Deterministic (1+/-delta)-approximation for MDS on planar graphs in O(log* n) rounds. Matching lower bound: no faster deterministic algorithm achieves any constant approximation. |
| **Technique** | Iterative local improvement using structural properties of planar graphs; the O(log* n) round complexity comes from symmetry-breaking (coloring). |
| **Relevance** | The (1+delta)-approximation shows that near-optimal solutions are achievable with local information on planar graphs, albeit with O(log* n) rounds rather than O(1). This suggests our centralized algorithm should aim for near-optimal ratios since the structural properties of planar graphs are rich enough to support them. |
| **BibTeX Key** | `CzygrinowHanckowiak2008` |

### Paper 14 -- Hilke, Lenzen & Suomela (2014)

| Field | Value |
|-------|-------|
| **Authors** | Miikka Hilke, Christoph Lenzen, Jukka Suomela |
| **Year** | 2014 |
| **Title** | Brief Announcement: Local Approximability of Minimum Dominating Set on Planar Graphs |
| **Venue** | PODC 2014, pp. 344--346 |
| **Key Result** | Proved that no deterministic constant-round LOCAL algorithm can achieve a (7-eps)-approximation for MDS on planar graphs. |
| **Technique** | Lower bound construction: families of planar graphs where any local algorithm must incur at least a factor-7 loss. |
| **Relevance** | Establishes fundamental limits of local (constant-round) algorithms. While our centralized algorithm is not constrained by this lower bound, it informs the comparison with distributed methods and highlights the advantage of global information (separators, LP) in centralized settings. |
| **BibTeX Key** | `HilkeLenzenSuomela2014` |

### Paper 15 -- Heydt, Kublenz, Ossona de Mendez, Siebertz & Vigny (2025)

| Field | Value |
|-------|-------|
| **Authors** | Ozan Heydt, Simeon Kublenz, Patrice Ossona de Mendez, Sebastian Siebertz, Alexandre Vigny |
| **Year** | 2025 |
| **Title** | Distributed domination on sparse graph classes |
| **Venue** | European Journal of Combinatorics, 123:103773 |
| **Key Result** | (11+eps)-approximation for MDS on planar graphs in constant LOCAL rounds -- the current best known ratio for distributed constant-round algorithms. Generalizes to bounded expansion classes. |
| **Technique** | Constant-factor approximation in constant rounds on bounded expansion graphs. For planar graphs, refined analysis and algorithmic modifications lower the ratio from 52 to 11+eps. Uses structural decompositions based on low treedepth colorings and generalized coloring numbers. |
| **Relevance** | State-of-the-art distributed result. The 11+eps ratio is a key reference point. Our centralized algorithm, with access to global structure (LP, separators), should significantly outperform this. If our hybrid achieves ratio <= 5, it would represent a major practical improvement over all known constant-time methods. |
| **BibTeX Key** | `HeydtKublenzOdMSiebertzVigny2025` |

### Paper 16 -- Bonamy, Cook, Groenland & Wesolek (2021)

| Field | Value |
|-------|-------|
| **Authors** | Marthe Bonamy, Linda Cook, Josse van den Heuvel, Alexandra Wesolek |
| **Year** | 2021 |
| **Title** | A Tight Local Algorithm for the Minimum Dominating Set Problem in Outerplanar Graphs |
| **Venue** | DISC 2021, LIPIcs 209:13:1--13:18 |
| **Key Result** | Deterministic local algorithm achieving a 5-approximation for MDS on outerplanar graphs, with a matching (5-eps) lower bound. Algorithm uses only vertex degree and neighbor degree information. |
| **Technique** | Classification of vertices by local structure (degree, neighbor degrees) with provably tight analysis on outerplanar graph families. |
| **Relevance** | Outerplanar graphs are the simplest nontrivial subclass of planar graphs. The tight ratio of 5 for local algorithms on outerplanar graphs suggests that achieving ratio <= 5 on general planar graphs with a centralized algorithm is ambitious but potentially feasible. Good test case for validating our algorithms. |
| **BibTeX Key** | `BonamyCookGroenlandWesolek2021` |

---

## Category (e): FPT and Kernelization

### Paper 17 -- Alber, Bodlaender, Fernau, Kloks & Niedermeier (2002)

| Field | Value |
|-------|-------|
| **Authors** | Jochen Alber, Hans L. Bodlaender, Henning Fernau, Ton Kloks, Rolf Niedermeier |
| **Year** | 2002 |
| **Title** | Fixed Parameter Algorithms for DOMINATING SET and Related Problems on Planar Graphs |
| **Venue** | Algorithmica, 33:461--493 |
| **Key Result** | First FPT algorithm for dominating set on planar graphs. Subexponential running time 2^{O(sqrt(k))} n^{O(1)}, breaking the 2^{O(k)} barrier. |
| **Technique** | Proof that planar graphs with domination number k have treewidth O(sqrt(k)). Dynamic programming on tree decomposition of width O(sqrt(k)) gives the subexponential algorithm. |
| **Relevance** | The treewidth-domination-number relationship tw(G) = O(sqrt(gamma(G))) is fundamental to our separator-based approach. When we decompose via separators, the pieces have bounded treewidth related to the local domination number, enabling exact DP on pieces. |
| **BibTeX Key** | `AlberBodlaenderFernauKloksNiedermeier2002` |

### Paper 18 -- Alber, Fellows & Niedermeier (2004)

| Field | Value |
|-------|-------|
| **Authors** | Jochen Alber, Michael R. Fellows, Rolf Niedermeier |
| **Year** | 2004 |
| **Title** | Polynomial-Time Data Reduction for Dominating Set |
| **Venue** | Journal of the ACM, 51(3):363--384 |
| **Key Result** | Linear kernel of 335k vertices for dominating set on planar graphs, obtained via two simple reduction rules: (1) remove dominated vertices with degree-1 dominators, (2) merge twin vertices. |
| **Technique** | Problem kernelization: polynomial-time preprocessing rules that reduce any planar instance with domination number k to an equivalent instance of size O(k). The two rules are simple to implement and run in linear time. |
| **Relevance** | Kernelization is directly applicable as a preprocessing step in our algorithm pipeline. Reducing the instance to O(k) vertices before applying LP or separator-based methods could dramatically improve practical runtime. We plan to implement these reduction rules in our hybrid algorithm (Phase 3). |
| **BibTeX Key** | `AlberFellowsNiedermeier2004` |

### Paper 19 -- Fomin & Thilikos (2004)

| Field | Value |
|-------|-------|
| **Authors** | Fedor V. Fomin, Dimitrios M. Thilikos |
| **Year** | 2004 |
| **Title** | Fast Parameterized Algorithms for Graphs on Surfaces: Linear Kernel and Exponential Speed-Up |
| **Venue** | ICALP 2004, LNCS 3142:581--592 |
| **Key Result** | Extended the linear kernel result to graphs of bounded genus. Algorithm runs in 2^{15.13 sqrt(k)} + n^3 time using branch-width decomposition rather than tree-width. |
| **Technique** | Branch-width based approach exploiting the min-max duality theorems of Robertson-Seymour graph minor theory. Same reduction rules as Alber et al. yield a linear kernel on bounded-genus graphs. |
| **Relevance** | Shows that the structural exploitation of planarity for kernelization extends to broader classes. The branch-width approach may offer practical advantages over tree-width for our exact sub-solver on decomposed pieces. |
| **BibTeX Key** | `FominThilikos2004` |

### Paper 20 -- Fomin, Lokshtanov, Saurabh & Thilikos (2010)

| Field | Value |
|-------|-------|
| **Authors** | Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh, Dimitrios M. Thilikos |
| **Year** | 2010 |
| **Title** | Bidimensionality and Kernels |
| **Venue** | SODA 2010, pp. 503--510 |
| **Key Result** | Meta-algorithmic framework: every bidimensional problem satisfying a separation property and expressible in CMSO logic admits a linear kernel on H-minor-free graphs. Unifies and generalizes all prior kernelization results for MDS on planar and bounded-genus graphs. |
| **Technique** | Bidimensionality + protrusion replacement: identifies "protrusions" (subgraphs of bounded treewidth attached via bounded boundary) and replaces them with equivalent smaller gadgets. |
| **Relevance** | The protrusion replacement technique could be applied as an advanced preprocessing step in our algorithm. While the meta-algorithmic nature means the concrete constants are large, the structural insight (protrusions can be simplified) directly applies to our separator-based decomposition. |
| **BibTeX Key** | `FominLokshtanovSaurabhThilikos2010` |

### Paper 21 -- Fomin, Lokshtanov, Saurabh & Thilikos (2018)

| Field | Value |
|-------|-------|
| **Authors** | Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh, Dimitrios M. Thilikos |
| **Year** | 2018 |
| **Title** | Kernels for (Connected) Dominating Set on Graphs with Excluded Topological Minors |
| **Venue** | ACM Transactions on Algorithms, 14(1):6:1--6:31 |
| **Key Result** | First linear kernels for dominating set and connected dominating set on H-topological-minor-free graphs: polynomial-time reduction to an equivalent instance on O(k) vertices. |
| **Technique** | Extension of the protrusion-based kernelization framework to topological-minor-free classes, which are strictly broader than minor-free classes. |
| **Relevance** | Further confirms that kernelization to O(k) vertices is possible across a wide range of sparse graph classes. The practical applicability of these kernelization rules to our benchmark instances is worth investigating. |
| **BibTeX Key** | `FominLokshtanovSaurabhThilikos2018` |

---

## Category (f): PACE 2025 Competition (Practical Solvers)

### Paper 22 -- Grobler & Siebertz (2025) -- PACE 2025 Challenge Report

| Field | Value |
|-------|-------|
| **Authors** | Mario Grobler, Sebastian Siebertz |
| **Year** | 2025 |
| **Title** | The PACE 2025 Parameterized Algorithms and Computational Experiments Challenge: Dominating Set and Hitting Set |
| **Venue** | IPEC 2025, LIPIcs 358:32:1--32:22 |
| **Key Result** | 71 participants from 25 teams competed on exact and heuristic dominating set tracks. Instances included nearly-planar OSM road network graphs. Many solvers solved all non-Watts-Strogatz instances. Planar/OSM instances were among the easiest for exact solvers. |
| **Technique** | Competition format: exact track (30 min, optimal solution required) and heuristic track (5 min, best solution). Instances structured to exploit planarity, bounded treewidth, bounded degeneracy. |
| **Relevance** | Provides a benchmark for practical solver performance on MDS. The observation that planar (OSM) instances were "easy" for exact solvers validates our hypothesis that planarity can be algorithmically exploited. We plan to use PACE 2025 instances in our benchmark suite. |
| **BibTeX Key** | `PACE2025report` |

### Paper 23 -- Dobler, Fink & Rocton (2025) -- "Bad Dominating Set Maker"

| Field | Value |
|-------|-------|
| **Authors** | Alexander Dobler, Simon Dominik Fink, Mathis Rocton |
| **Year** | 2025 |
| **Title** | PACE Solver Description: Bad Dominating Set Maker |
| **Venue** | IPEC 2025, LIPIcs 358:35:1--35:4 |
| **Key Result** | Competitive exact solver combining multiple techniques. Transforms instances into directed constrained domination, applies extensive reduction rules, uses tree decomposition DP when width <= 13, falls back to MaxSAT (EvalMaxSat). |
| **Technique** | Multi-phase: (1) reduction rules, (2) tree decomposition computation (via htd), (3) DP if low treewidth, (4) check for vertex cover structure (via peaty), (5) MaxSAT fallback. |
| **Relevance** | The multi-phase architecture (reduce, decompose, solve) mirrors our planned hybrid approach. Their use of treewidth thresholds for deciding between DP and SAT/ILP is directly applicable. The reduction rules they employ can inform our preprocessing module. |
| **BibTeX Key** | `PACE2025BadDSMaker` |

### Paper 24 -- Bannach, Chudigiewitsch & Wienobst (2025) -- UzL Solver

| Field | Value |
|-------|-------|
| **Authors** | Max Bannach, Florian Chudigiewitsch, Marcel Wienobst |
| **Year** | 2025 |
| **Title** | PACE Solver Description: UzL Solver for Dominating Set and Hitting Set |
| **Venue** | IPEC 2025, LIPIcs 358:39:1--39:4 |
| **Key Result** | Exact solver based on MaxSAT formulation supplemented by hitting-set-based reduction rules. Uses a clique solver for small vertex cover instances and SAT for lower-bound matching. |
| **Technique** | Direct MaxSAT encoding of MDS; hitting-set reductions simplify the instance before SAT solving. Competitive on structured (including planar) instances. |
| **Relevance** | Demonstrates that MaxSAT/SAT approaches are effective for exact MDS on structured graphs. Our ILP-based exact solver for validation (computing OPT on small instances) can draw on similar encoding strategies. |
| **BibTeX Key** | `PACE2025UzL` |

---

## Classic References

### Paper 25 -- Garey & Johnson (1979)

| Field | Value |
|-------|-------|
| **Authors** | Michael R. Garey, David S. Johnson |
| **Year** | 1979 |
| **Title** | Computers and Intractability: A Guide to the Theory of NP-Completeness |
| **Venue** | W. H. Freeman (Book) |
| **Key Result** | Establishes NP-completeness of Dominating Set, including on planar graphs of maximum degree 3. |
| **Relevance** | Foundational complexity reference motivating the study of approximation algorithms. |
| **BibTeX Key** | `GareyJohnson1979` |

---

## Summary Table

| # | BibTeX Key | Year | Category | Key Contribution | Approx Ratio (Planar) |
|---|-----------|------|----------|------------------|-----------------------|
| 1 | Baker1994 | 1994 | (a) PTAS | PTAS via k-outerplanar decomposition | (1+2/k) |
| 2 | DemaineHajiaghayi2005 | 2005 | (a) PTAS | Bidimensionality PTAS/EPTAS framework | (1+eps) |
| 3 | FominLokshtanovRamanSaurabh2011 | 2011 | (a) PTAS | EPTAS via decomposition lemma | (1+eps) |
| 4 | MarzbanGu2013 | 2013 | (a) PTAS | Corrected Baker PTAS + computational study | (1+2/k) |
| 5 | Dvorak2013 | 2013 | (b) Greedy | Constant-factor via bounded expansion | O(1) |
| 6 | Siebertz2019 | 2019 | (b) Greedy | Modified greedy on biclique-free graphs | O(ln k) |
| 7 | Dvorak2019 | 2019 | (b) Greedy | LP-informed bounds on sparse graphs | O(1) |
| 8 | BansalUmboh2017 | 2017 | (c) LP | LP rounding, tight bounds for arboricity | 7 (arb. 3) |
| 9 | Sun2021 | 2021 | (c) LP | LP integrality gap <= arboricity+1 | gap <= 4 |
| 10 | MorganSolomonWein2021 | 2021 | (c) LP | Combinatorial O(alpha)-approx, linear time | O(1) |
| 11 | LenzenOswaldWattenhofer2008 | 2008 | (d) Distributed | First constant-round MDS on planar | 126 |
| 12 | LenzenPignoletWattenhofer2013 | 2013 | (d) Distributed | Improved constant-round distributed MDS | 52 |
| 13 | CzygrinowHanckowiak2008 | 2008 | (d) Distributed | (1+delta)-approx in O(log* n) rounds | (1+delta) |
| 14 | HilkeLenzenSuomela2014 | 2014 | (d) Distributed | (7-eps) lower bound for constant-round | lower bound |
| 15 | HeydtKublenzOdMSiebertzVigny2025 | 2025 | (d) Distributed | Best constant-round distributed ratio | (11+eps) |
| 16 | BonamyCookGroenlandWesolek2021 | 2021 | (d) Distributed | Tight 5-approx on outerplanar graphs | 5 (outerplanar) |
| 17 | AlberBodlaenderFernauKloksNiedermeier2002 | 2002 | (e) FPT | First subexponential FPT for planar DS | exact (FPT) |
| 18 | AlberFellowsNiedermeier2004 | 2004 | (e) FPT | Linear kernel (335k) for planar DS | exact (kernel) |
| 19 | FominThilikos2004 | 2004 | (e) FPT | Linear kernel on bounded-genus graphs | exact (kernel) |
| 20 | FominLokshtanovSaurabhThilikos2010 | 2010 | (e) FPT | Bidimensionality => linear kernels | exact (kernel) |
| 21 | FominLokshtanovSaurabhThilikos2018 | 2018 | (e) FPT | Linear kernel on H-topo-minor-free | exact (kernel) |
| 22 | PACE2025report | 2025 | (f) Practical | Competition report, 71 participants | exact/heuristic |
| 23 | PACE2025BadDSMaker | 2025 | (f) Practical | Reduction + TD-DP + MaxSAT solver | exact |
| 24 | PACE2025UzL | 2025 | (f) Practical | MaxSAT + hitting-set reductions | exact |
| 25 | GareyJohnson1979 | 1979 | Classic | NP-completeness of DS on planar graphs | N/A |

---

## Key Observations and Research Gaps

### 1. The Practical Approximation Gap
While PTASs achieving (1+eps) exist theoretically (Baker 1994, Demaine & Hajiaghayi 2005), their
running times are exponential in 1/eps, making them impractical for small eps. The best practical
centralized constant-factor ratio comes from LP rounding (Bansal & Umboh 2017) at 7 for planar
graphs (arboricity <= 3), or from combinatorial methods (Morgan, Solomon & Wein 2021) at O(1) with
unspecified constants. There is a clear gap between the theoretical (1+eps) and the practical
constant-factor algorithms.

### 2. LP Lower Bounds Are Strong
Sun (2021) proved that the LP integrality gap for MDS on planar graphs is at most 4. This means
LP relaxation provides a lower bound within factor 4 of OPT, making it a reliable tool for
measuring approximation quality in experiments even when exact OPT is unknown.

### 3. Kernelization as Preprocessing
The 335k-vertex linear kernel of Alber et al. (2004) provides a powerful preprocessing step.
Reducing instance size before applying more expensive algorithms (LP, separator decomposition)
could make the hybrid approach scalable to large instances.

### 4. Distributed vs. Centralized Gap
The best distributed constant-round ratio is 11+eps (Heydt et al. 2025), with a lower bound
of 7-eps (Hilke et al. 2014). Centralized algorithms with global information (separators, LP)
should significantly outperform these bounds. Our target of ratio <= 5 is justified by this gap.

### 5. PACE 2025 Validates Exploitability of Planarity
PACE 2025 results show that planar (OSM) instances were among the easiest for exact solvers,
confirming that planarity can be effectively exploited in practice. The multi-phase solver
architectures (reduce, decompose, solve) from PACE winners directly inform our algorithm design.

### 6. Separator-Based Approach Is Underexplored for Approximation
While separators are central to PTAS design (Baker, Demaine & Hajiaghayi) and FPT algorithms
(Alber et al.), their use for practical constant-factor approximation (rather than (1+eps) schemes)
has not been thoroughly studied. Our proposed hybrid -- separator decomposition + LP rounding +
local search -- addresses this gap.

---

## References

All 25 BibTeX entries are in `/sources.bib`. Additional textbook references included:
- Vazirani (2001): Approximation Algorithms textbook (`Vazirani2001`)
- Williamson & Shmoys (2011): Design of Approximation Algorithms (`WilliamsonShmoys2011`)
