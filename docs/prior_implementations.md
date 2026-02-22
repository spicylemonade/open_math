# Survey of Existing Open-Source Cellular Automata Simulators

## 1. Golly

- **Repository URL**: https://golly.sourceforge.io/ (source: https://github.com/AlephAlpha/golly)
- **Language**: C++ (core), Python/Lua (scripting)
- **Feature Set**:
  - Dual algorithm engine: HashLife (memoized quadtree) and QuickLife (bit-parallel tiles)
  - Supports unbounded universes with multiple topologies (plane, torus, Klein bottle)
  - Multi-state CAs up to 256 states (von Neumann 29-state, WireWorld, Generations, etc.)
  - Reads RLE, macrocell, Life 1.05/1.06, dblife, and MCell file formats
  - Unlimited undo/redo, multiple layers, scriptable via Python and Lua
  - Cross-platform (Windows, Mac, Linux, Android, iOS)
  - Includes `bgolly` command-line variant
- **Architecture Pattern**: Dual-engine design with shared GUI frontend. Algorithms are abstracted behind a common `lifealgo` interface, allowing seamless switching between HashLife and QuickLife. Pattern I/O is handled through format-specific readers/writers.
- **Lessons for Our Design**:
  - The dual-algorithm approach validates our plan to implement multiple engines (naive, NumPy, HashLife) behind a shared interface
  - File format support (especially RLE) is essential for interoperability with the Life community
  - Separating CLI (`bgolly`) from GUI allows headless batch execution

## 2. Lenia (Chakazul/Lenia)

- **Repository URL**: https://github.com/Chakazul/Lenia
- **Language**: Python (primary), MATLAB, JavaScript
- **Feature Set**:
  - Continuous-state, continuous-time, continuous-space cellular automata
  - Produces diverse artificial life forms ("mathematical life forms")
  - N-dimensional support (2D, 3D, 4D confirmed)
  - NumPy/SciPy-based computation using FFT convolution
  - Jupyter notebook interface for interactive exploration
  - Published in *Complex Systems* journal and arXiv (1812.05433)
- **Architecture Pattern**: Single-module design centered around NumPy array operations. The kernel function and growth function are parameterized, allowing exploration of continuous rule spaces. Uses FFT-based convolution (scipy.signal.fftconvolve) for efficient neighbor summation.
- **Lessons for Our Design**:
  - Demonstrates that NumPy + SciPy convolution is effective for CA neighbor counting
  - FFT convolution is more efficient than direct convolution for large kernels, but for our small (3×3) kernels, direct convolution or array slicing is faster
  - Parameterized rule functions enable systematic rule space exploration

## 3. CellPyLib

- **Repository URL**: https://github.com/lantunes/cellpylib
- **Language**: Python
- **Feature Set**:
  - 1D and 2D cellular automata with discrete or continuous states
  - Adjustable neighborhood radii, Moore and von Neumann neighborhoods
  - Supports Wolfram's elementary CA rules and arbitrary rule functions
  - Asynchronous CA and reversible CA support
  - Langton's lambda parameter calculation
  - Built on NumPy with Matplotlib visualization
  - Periodic boundary conditions
- **Architecture Pattern**: Functional design — CA state is a NumPy array, rule is a Python function, and evolution is performed by `evolve()` which applies the rule function to the neighborhood array. Clean separation between state, rule, and visualization.
- **Lessons for Our Design**:
  - The functional `evolve(state, rule_fn, steps)` pattern is clean and testable
  - NumPy array-based state representation is the natural choice
  - Lambda parameter calculation is relevant to our complexity classification work
  - Good example of minimal API design (~2000 lines for full feature set)

## 4. cellular-automaton (PyPI)

- **Repository URL**: https://pypi.org/project/cellular-automaton/
- **Language**: Python
- **Feature Set**:
  - N-dimensional cellular automata support
  - Multi-process capable for performance
  - Pygame-based 2D visualization
  - Moore neighborhood with configurable edge rules (ignore, ignore missing, wrap)
  - Object-oriented API: inherit from `Rule` to define evolution
  - Clean test coverage
- **Architecture Pattern**: OOP inheritance-based — users subclass `Rule` and implement `evolve_rule()`. Grid creation is handled by `CAFactory`. Visualization is optional and depends on pygame. Multi-process support uses Python multiprocessing.
- **Lessons for Our Design**:
  - Edge rule configuration (ignore/wrap/fixed) maps directly to our boundary condition design
  - Factory pattern for CA creation adds unnecessary complexity for a minimal simulator
  - Pygame dependency is heavy; our terminal-based approach is lighter-weight
  - Multi-process approach shows Python's GIL limitations for CA computation

## 5. python-lifelib

- **Repository URL**: https://gitlab.com/apgoucher/lifelib (PyPI: python-lifelib)
- **Language**: C++ (core), Python (bindings), x86_64 assembly (inner loops)
- **Feature Set**:
  - High-performance Life simulation using SIMD instructions (SSE, AVX, AVX2, AVX-512)
  - HashLife variant (StreamLife) optimized for glider streams
  - Tile-based algorithm for random patterns (used in apgsearch)
  - Nine different "genera" (rule-specific code generators)
  - Fast periodicity detection and apgcode determination
  - Pattern manipulation: separation, component detection, spanning trees
- **Architecture Pattern**: Code generation approach — Python scripts generate C++ inner loops optimized for specific rule families. The `genus` abstraction targets each rule family with hand-tuned code. Algorithms (hashlife, tile-based) are interchangeable via iterators.
- **Lessons for Our Design**:
  - Demonstrates extreme optimization is possible but requires assembly-level programming
  - Code generation for rule-specific inner loops is beyond our "minimal" scope
  - The iterator/algorithm separation is a good architectural pattern
  - Performance comparison target: lifelib is one of the fastest Life simulators

## 6. Game of Life in Python (jakevdp)

- **Repository URL**: https://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/
- **Language**: Python (NumPy)
- **Feature Set**:
  - Minimal Game of Life implementation using NumPy
  - Uses `scipy.signal.convolve2d` for neighbor counting
  - Matplotlib animation for visualization
  - Entire implementation in ~20 lines of code
- **Architecture Pattern**: Single-function design: `life_step(X)` takes a boolean array, computes neighbor counts via 2D convolution with a 3×3 kernel, and returns the next state. Elegantly minimal.
- **Lessons for Our Design**:
  - Validates that `convolve2d` with a ones kernel (center zeroed) is the canonical NumPy approach
  - Shows that a useful CA simulator can be extremely concise
  - Our NumPy engine should follow this convolution-based pattern
  - Animation via `matplotlib.animation.FuncAnimation` is an alternative to curses

## Summary Table

| Project | Language | Lines of Code | Algorithms | Dimensions | Key Strength |
|---------|----------|---------------|------------|------------|--------------|
| Golly | C++/Python | ~100k | HashLife, QuickLife | 1D, 2D | Most comprehensive CA simulator |
| Lenia | Python | ~5k | FFT convolution | N-D | Continuous CA, beautiful life forms |
| CellPyLib | Python | ~2k | NumPy array ops | 1D, 2D | Clean API, lambda parameter |
| cellular-automaton | Python | ~3k | Multi-process | N-D | N-dimensional, pygame viz |
| python-lifelib | C++/Python | ~50k | StreamLife, tile-based | 2D | Extreme performance (SIMD) |
| jakevdp GoL | Python | ~20 | convolve2d | 2D | Minimal elegance |
