# Survey of Open-Source N-Body and Gravitational Simulation Codes

This document surveys notable open-source N-body and gravitational dynamics codes,
documenting their language, integration methods, force algorithms, feature sets,
performance characteristics, and licenses. Design patterns and best practices
relevant to our project are identified at the end.

---

## 1. REBOUND (Rein & Liu, 2012)

- **Website:** https://rebound.readthedocs.io/
- **GitHub:** https://github.com/hannorein/rebound
- **Language:** C (core), with a full Python wrapper (installable via `pip install rebound`)
- **License:** GNU General Public License v3 (GPLv3)

### Integration Methods

REBOUND offers the most extensive suite of integrators among the codes surveyed:

| Integrator | Type | Order | Notes |
|---|---|---|---|
| IAS15 | Non-symplectic, adaptive | 15th | Highest accuracy; adaptive time-stepping; Rein & Spiegel (2015) |
| WHFast | Symplectic (Wisdom-Holman) | 2nd | Fast, unbiased, machine-independent; Rein & Tamayo (2015) |
| WHFastHelio | Symplectic (democratic heliocentric) | 2nd | Better for close encounters than Jacobi-coordinate WHFast |
| WHFast512 | Symplectic (AVX512) | 2nd | SIMD-accelerated; Javaheri, Rein & Tamayo (2023) |
| MERCURIUS | Hybrid symplectic | 2nd | Planetary dynamics with close encounters |
| TRACE | Hybrid reversible | varies | Arbitrary close encounters |
| SABA/SABAC/SABACL | Symplectic | High-order | Rein, Tamayo & Brown (2019) |
| Leapfrog | Symplectic | 2nd | Standard kick-drift-kick |
| SEI | Symplectic | 2nd | Exact for shearing-sheet without self-gravity |
| EOS | Embedded operator splitting | varies | Flexible symplectic composition |

REBOUND also supports integration of arbitrary user-defined ODEs coupled to N-body
dynamics (e.g., for tides, spin evolution).

### Force Algorithm

- **Direct summation** (default for small N)
- **Barnes-Hut tree** for self-gravity and collision detection, fully parallelized
  with MPI and OpenMP using static domain decomposition and distributed essential trees

### Feature Set

- Open, periodic, and shearing-sheet boundary conditions
- Two collision detection modules (plane-sweep and tree-based)
- Gravitational softening support
- SimulationArchive for exact bitwise reproducibility (Rein & Tamayo, 2017)
- REBOUNDx extension library for additional physics: migration forces, general
  relativity corrections, spin-orbit coupling, tidal effects
- No external library dependencies

### Performance Characteristics

- WHFast and IAS15 are among the most accurate integrators available for long-term
  planetary dynamics
- WHFast is machine-independent (uses only +, *, sqrt -- no sin/cos)
- WHFast512 exploits AVX512 SIMD for ~4x speedup on supported hardware
- MPI + OpenMP parallelism for tree-based calculations
- Optimized for planetary-system-scale problems (N ~ 2 to ~10^5)

### Design Patterns to Adopt

- Modular integrator design with a common interface
- Separation of force computation from integration
- Simulation archive / state recording for reproducibility
- Gravitational softening as a configurable parameter

---

## 2. GADGET-4 (Springel et al.)

- **Website:** https://wwwmpa.mpa-garching.mpg.de/gadget4/
- **Repository:** Public git repository hosted at MPCDF GitLab; forks on GitHub
- **Reference:** Springel, Pakmor, Zier & Reinecke, MNRAS (2021)
- **Language:** C++11 (requires MPI-3)
- **License:** GNU General Public License (GPL)

### Integration Methods

- Leapfrog (kick-drift-kick) with individual adaptive block time-steps
- Hierarchical time-stepping with high dynamic range support

### Force Algorithms

| Method | Description |
|---|---|
| Tree (Barnes-Hut oct-tree) | Hierarchical multipole expansion for gravity |
| TreePM | Long-range PM + short-range tree; original GADGET approach |
| FMM | Fast Multipole Method; momentum-conserving variant |
| FMM+PM | FMM for short-range + PM for long-range |

Both periodic and non-periodic boundary conditions supported for TreePM and FMM-PM.

### Feature Set

- Smoothed Particle Hydrodynamics (SPH) for gas dynamics
- Cosmological integration (expanding universe, comoving coordinates)
- On-the-fly group/substructure finding (Friends-of-Friends, SUBFIND)
- Power spectrum estimation
- Built-in cosmological initial conditions generator
- Merger tree construction
- Lagrangian, adaptive in space and time

### Performance Characteristics

- Massively parallel: MPI with shared-memory optimization
- Sophisticated domain decomposition for load balancing
- Demonstrated scaling to >10^5 MPI ranks
- Designed for cosmological simulations with 10^9 -- 10^12 particles
- Improved force accuracy and time-stepping over GADGET-2/3

### Design Patterns to Adopt

- Separation of long-range and short-range force computation (PM + tree split)
- Adaptive individual time-steps per particle
- Modular force solver architecture (tree vs. FMM vs. PM selectable)

---

## 3. NBODY6 / NBODY6++GPU (Aarseth; Spurzem et al.)

- **GitHub (NBODY6):** https://github.com/mtrenti/NBODY6
- **GitHub (NBODY6++GPU):** https://github.com/nbody6ppgpu/Nbody6PPGPU-beijing
- **Reference:** Aarseth (2003), "Gravitational N-Body Simulations"; Wang et al. (2015)
- **Language:** Fortran (core), with C++/CUDA for GPU and SIMD acceleration
- **License:** Not explicitly stated in repositories (academic/public domain tradition);
  check individual repository LICENSE files

### Integration Methods

- 4th-order Hermite integrator with individual adaptive (block) time-steps
- Ahmad-Cohen neighbour scheme: splits force into regular (distant, slowly changing)
  and irregular (local, fast-changing) components with different update frequencies
- Kustaanheimo-Stiefel (KS) regularization for close two-body encounters
- Chain regularization (Mikkola 1990) for few-body subsystems (triples, quadruples)

### Force Algorithm

- **Direct summation** O(N^2) -- no approximations in force calculation
- Neighbour scheme reduces effective cost by splitting into regular/irregular forces
- GPU-accelerated force computation in NBODY6-GPU and NBODY6++GPU variants

### Feature Set

- Specifically designed for collisional stellar dynamics (star clusters)
- Binary and hierarchical system detection and treatment
- Stellar evolution prescriptions (mass loss, supernova kicks)
- Tidal fields from host galaxy
- Primordial binary populations

### Performance Characteristics

- NBODY6: Single-node, optimized for N ~ 10^4 to 2x10^5 on dual-GPU systems
- NBODY6++GPU: Hybrid MPI + GPU + OpenMP + AVX/SSE parallelization
- NBODY6++GPU is 400-2000x faster than serial NBODY6 (with 320 CPU cores + 32 K20X GPUs)
- Targets the "million-body problem" for globular cluster simulations
- Highest accuracy of all codes surveyed for collisional dynamics (no force approximation)

### Design Patterns to Adopt

- Neighbour scheme concept (splitting forces by timescale) for performance
- Regularization techniques for handling close encounters
- Block time-step scheme for efficient adaptive integration

---

## 4. pynbody

- **GitHub:** https://github.com/pynbody/pynbody
- **Documentation:** https://pynbody.readthedocs.io/
- **Language:** Python (with compiled extensions)
- **License:** BSD-style (consistent with pynbody ecosystem; verify at repository)

### Purpose

pynbody is an **analysis framework** rather than a simulation code. It provides tools
for loading, manipulating, and analyzing outputs from N-body and hydrodynamic
simulations.

### Supported Simulation Formats

- PKDGRAV / Gasoline
- Gadget / Gadget-4 / Arepo
- N-Chilada
- RAMSES AMR

### Feature Set

- Publication-quality analysis routines
- Halo finding and profile computation
- Morphological decomposition tools
- Ionisation and cooling calculations
- Phase diagram plotting
- Python 3 only (SPEC0 version support policy)

### Performance Characteristics

- Designed for post-processing, not runtime simulation
- Handles large simulation outputs efficiently through lazy loading
- Latest version (2.x) with modernized internals

### Design Patterns to Adopt

- Clean Python API for simulation data access
- Separation of simulation execution from analysis/visualization
- Support for multiple file formats through a common interface

---

## 5. galpy (Bovy, 2015)

- **Website:** https://www.galpy.org/
- **GitHub:** https://github.com/jobovy/galpy
- **Documentation:** https://docs.galpy.org/
- **Language:** Python (with C extensions for performance-critical paths)
- **License:** BSD 3-Clause ("New BSD")

### Integration Methods

- Multiple Runge-Kutta-type integrators
- Symplectic integrators
- Supports numerical orbit integration in arbitrary potentials

### Force Algorithm

galpy uses **analytical potential models** rather than particle-particle force
calculation. It provides a library of gravitational potential classes (Miyamoto-Nagai,
NFW, logarithmic, Milky Way composite models, etc.) with analytical or semi-analytical
force evaluation.

### Feature Set

- Orbit integration in arbitrary galactic potentials
- Action-angle coordinate computation:
  - Adiabatic approximation (Binney 2010)
  - Staeckel approximation (Bovy & Rix 2013)
  - Isochrone approximation (Bovy 2014)
- Distribution functions (2D/3D disk DFs, tidal stream DFs)
- Built-in Milky Way potential model (MWPotential2014)
- Full astropy Quantity/unit support (astropy affiliated package)
- 99.8% test coverage

### Performance Characteristics

- C extensions for computationally intensive operations
- ~54,000 lines of code (23,000 module + 11,000 tests + 20,000 documentation)
- Used in >200 scientific publications
- Fast for single-orbit and few-body problems in smooth potentials
- Not designed for self-gravitating N-body simulations

### Design Patterns to Adopt

- Potential abstraction: define a common potential interface with analytical force methods
- Comprehensive unit testing (99.8% coverage as a gold standard)
- Integration of physical units through astropy
- Clear separation between potential specification and orbit integration

---

## 6. Arepo (Springel, 2010; Weinberger et al., 2019)

- **Website:** https://arepo-code.org/
- **GitHub Mirror:** https://github.com/dnelson/arepo
- **GitLab:** https://gitlab.mpcdf.mpg.de/vrs/arepo
- **Language:** C (with MPI parallelization)
- **License:** GNU General Public License v3 (GPLv3)

### Integration Methods

- Leapfrog with adaptive individual time-steps per cell/particle
- Second-order unsplit Godunov scheme with exact Riemann solver for hydrodynamics

### Force Algorithm

- **Tree-Particle-Mesh (TreePM)** for gravitational interactions
- Moving unstructured Voronoi mesh for hydrodynamics (not standard SPH)

### Feature Set

- Moving-mesh hydrodynamics (Galilean-invariant, unlike fixed Eulerian grids)
- Magnetohydrodynamics (MHD) on Voronoi tessellation
- Cosmological integration (Newtonian and expanding spacetime)
- Adaptive spatial resolution (inherits SPH advantage for structure formation)
- Used for the Illustris and IllustrisTNG simulation projects

### Performance Characteristics

- Fully MPI parallel, tested with >10,000 MPI tasks
- Dynamic load and memory balancing
- High dynamic range in space and time
- Primarily optimized for cosmological galaxy formation simulations

---

## 7. SWIFT (Schaller et al.)

- **Website:** https://www.swiftsim.com/
- **GitHub:** https://github.com/SWIFTSIM/SWIFT
- **Language:** C (85.6% of codebase)
- **License:** LGPL-3.0 and GPL-3.0 (dual licensed)

### Integration Methods

- Leapfrog with adaptive time-stepping
- Task-based parallelism for asynchronous updates

### Force Algorithm

- Tree-based gravity solver (Fast Multipole Method variant)
- Coupled to SPH for hydrodynamics

### Feature Set

- Multiple SPH flavours (SPHENIX as default)
- Cosmological simulations with subgrid physics
- Cooling models (Ploeckinger+2020 tables)
- Quick Lyman-alpha mode for cosmological runs
- HDF5 output with optional lossy compression
- Built-in halo finding

### Performance Characteristics

- Task-based parallelism (not traditional MPI domain decomposition)
- Asynchronous MPI communications
- SIMD vectorization
- Demonstrated scaling to >10^5 compute cores with >10^11 particles
- Designed from the ground up for modern HPC architectures

---

## 8. GIZMO (Hopkins, 2015)

- **Website:** http://www.tapir.caltech.edu/~phopkins/Site/GIZMO.html
- **GitHub:** https://github.com/pfhopkins/gizmo-public
- **Language:** ANSI C (with MPI)
- **License:** GNU General Public License (GPL) for public version

### Integration Methods

- Leapfrog with hierarchical adaptive time-steps (inherited from GADGET)
- Godunov-type finite-volume methods for hydrodynamics

### Force Algorithm

- Hybrid PM-Tree method for gravity (fully adaptive resolution)
- Lagrangian mesh-free finite-volume Godunov methods for hydrodynamics
- Also supports SPH and fixed-grid Eulerian methods

### Feature Set

The most feature-rich multi-physics code surveyed:
- MHD (ideal and non-ideal)
- Radiation hydrodynamics
- Anisotropic conduction and viscosity
- Radiative cooling
- Cosmic rays
- Dust-gas mixtures
- Sink particles
- Galaxy/star/black hole formation and feedback
- Self-interacting and scalar-field dark matter
- On-the-fly structure finding
- Fully compatible with GADGET analysis tools and file formats

### Performance Characteristics

- Hybrid MPI + OpenMP parallelization
- Verified scaling to >1 million threads on national supercomputers
- Portable across platforms from laptops to petascale machines

---

## 9. PeTar (Wang et al., 2020)

- **GitHub:** https://github.com/lwang-astro/PeTar
- **Language:** C++ (with MPI, OpenMP, SIMD support)
- **License:** MIT License

### Integration Methods

- 4th-order Hermite integrator for long-range forces
- Slow-down algorithmic regularization (SDAR) for close encounters and binaries

### Force Algorithm

- Barnes-Hut tree for long-range gravity
- Direct integration for short-range interactions
- No gravitational softening needed (exact treatment of close encounters)

### Feature Set

- Star cluster evolution with binary/hierarchical system dynamics
- Single and binary stellar evolution
- Galactic tidal field support
- Designed as a successor to NBODY6++GPU

### Performance Characteristics

- Demonstrated to be more efficient than NBODY6++GPU for many problem sizes
- Hybrid MPI + OpenMP + SIMD parallelization
- Suitable for large collisional N-body simulations

---

## Summary Comparison Table

| Code | Language | Primary Method | Force Algorithm | Domain | Parallelism | License |
|---|---|---|---|---|---|---|
| REBOUND | C/Python | IAS15, WHFast, Leapfrog, + many | Direct, Barnes-Hut tree | Planetary systems | MPI + OpenMP | GPLv3 |
| GADGET-4 | C++11 | Leapfrog (adaptive) | Tree, TreePM, FMM, FMM+PM | Cosmology | MPI + shared-mem | GPL |
| NBODY6 | Fortran/C++ | 4th-order Hermite | Direct O(N^2) | Star clusters | MPI + GPU + OpenMP | Academic |
| pynbody | Python | N/A (analysis only) | N/A | Analysis/post-processing | Serial/parallel I/O | BSD-style |
| galpy | Python/C | RK, symplectic | Analytical potentials | Galactic dynamics | Serial (C extensions) | BSD-3-Clause |
| Arepo | C | Leapfrog + Godunov | TreePM | Cosmology (moving mesh) | MPI | GPLv3 |
| SWIFT | C | Leapfrog (task-based) | Tree (FMM variant) | Cosmology | Task-based + MPI + SIMD | LGPL-3.0/GPL-3.0 |
| GIZMO | C | Leapfrog + Godunov | PM-Tree hybrid | Multi-physics | MPI + OpenMP | GPL |
| PeTar | C++ | Hermite + SDAR | Barnes-Hut tree + direct | Star clusters | MPI + OpenMP + SIMD | MIT |

---

## Design Patterns and Best Practices to Adopt

Based on this survey, the following patterns and practices are recommended for our
N-body simulator project:

1. **Modular integrator interface**: REBOUND's approach of offering multiple integrators
   through a common API is the gold standard. Our code should define an integrator
   interface that Euler, leapfrog, and RK4 all implement.

2. **Separated force computation**: All major codes cleanly separate force calculation
   from time integration. Force functions should be pluggable (direct, Barnes-Hut, etc.).

3. **Gravitational softening as a parameter**: REBOUND and GADGET both treat softening
   as a configurable parameter. This is essential for avoiding singularities in direct
   N-body calculations.

4. **Symplectic integrators for long-term stability**: REBOUND (WHFast, Leapfrog) and
   GADGET (Leapfrog) demonstrate that symplectic methods are strongly preferred for
   long-term gravitational simulations due to bounded energy error.

5. **Adaptive time-stepping**: NBODY6's block time-step scheme and REBOUND's IAS15
   adaptive stepping show that adaptive methods are essential for handling close
   encounters and eccentric orbits efficiently.

6. **Energy/momentum tracking**: All codes track conserved quantities for validation.
   Our simulation loop should compute and record total energy, linear momentum, and
   angular momentum at each step.

7. **State serialization for reproducibility**: REBOUND's SimulationArchive pattern
   of recording full state for bitwise reproducibility is a best practice.

8. **Comprehensive testing**: galpy's 99.8% test coverage sets the standard. Our code
   should have unit tests for all modules and integration tests against known analytical
   solutions.

---

## Sources

- [REBOUND GitHub](https://github.com/hannorein/rebound)
- [REBOUND Documentation](https://rebound.readthedocs.io/)
- [Rein & Liu 2012, A&A 537, A128](https://arxiv.org/abs/1110.4876)
- [GADGET-4 Website](https://wwwmpa.mpa-garching.mpg.de/gadget4/)
- [Springel et al. 2021, MNRAS](https://arxiv.org/abs/2010.03567)
- [GADGET Wikipedia](https://en.wikipedia.org/wiki/GADGET)
- [NBODY6 GitHub (mtrenti)](https://github.com/mtrenti/NBODY6)
- [NBODY6++GPU GitHub](https://github.com/nbody6ppgpu/Nbody6PPGPU-beijing)
- [Wang et al. 2015, MNRAS 450, 4070](https://arxiv.org/abs/1504.03687)
- [N-body simulations - Scholarpedia](http://www.scholarpedia.org/article/N-body_simulations_(gravitational))
- [pynbody GitHub](https://github.com/pynbody/pynbody)
- [pynbody PyPI](https://pypi.org/project/pynbody/)
- [galpy Website](https://www.galpy.org/)
- [galpy GitHub](https://github.com/jobovy/galpy)
- [Bovy 2015, ApJS 216, 29](https://arxiv.org/abs/1412.3451)
- [Arepo GitHub](https://github.com/dnelson/arepo)
- [Arepo Documentation](https://arepo-code.org/wp-content/userguide/index.html)
- [SWIFT GitHub](https://github.com/SWIFTSIM/SWIFT)
- [GIZMO GitHub](https://github.com/pfhopkins/gizmo-public)
- [GIZMO Documentation](http://www.tapir.caltech.edu/~phopkins/Site/GIZMO_files/gizmo_documentation.html)
- [PeTar GitHub](https://github.com/lwang-astro/PeTar)
- [Wang et al. 2020, MNRAS 497, 536](https://academic.oup.com/mnras/article/497/1/536/5867779)
