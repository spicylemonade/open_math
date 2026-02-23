"""
Minimal Newtonian gravity N-body simulation.

Implements direct-summation O(N^2) force computation with gravitational
softening, plus multiple integration schemes (Forward Euler, Velocity
Verlet, Leapfrog KDK) for benchmarking energy conservation and
performance scaling.

References:
    - Verlet (1967), Yoshida (1990), Barnes & Hut (1986)
    - Hairer, Lubich & Wanner (2006) — Geometric Numerical Integration
    - Dehnen & Read (2011) — N-body simulations of gravitational dynamics
"""

import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
G_DEFAULT = 1.0  # gravitational constant (natural units)

# ---------------------------------------------------------------------------
# Data structures & initialization
# ---------------------------------------------------------------------------

def init_bodies(masses, positions, velocities):
    """
    Create a simulation state from arrays.

    Parameters
    ----------
    masses : array-like, shape (N,)
    positions : array-like, shape (N, 2)
    velocities : array-like, shape (N, 2)

    Returns
    -------
    dict with keys 'masses', 'positions', 'velocities' as numpy arrays.
    """
    return {
        'masses': np.asarray(masses, dtype=np.float64),
        'positions': np.asarray(positions, dtype=np.float64),
        'velocities': np.asarray(velocities, dtype=np.float64),
    }


def init_circular_binary(m1=1.0, m2=1.0, a=1.0, G=G_DEFAULT):
    """
    Initialize a 2-body system on a circular Keplerian orbit.

    Bodies orbit their common center of mass with semi-major axis *a*.
    The orbital period is T = 2*pi*sqrt(a^3 / (G*(m1+m2))).

    Parameters
    ----------
    m1, m2 : float  — masses of the two bodies
    a : float        — orbital separation
    G : float        — gravitational constant

    Returns
    -------
    state : dict     — simulation state
    T : float        — orbital period
    """
    M = m1 + m2
    # positions relative to COM
    r1 = -a * m2 / M
    r2 = a * m1 / M
    # circular orbital speed
    v_orb = np.sqrt(G * M / a)
    v1 = -v_orb * m2 / M
    v2 = v_orb * m1 / M

    masses = np.array([m1, m2])
    positions = np.array([[r1, 0.0], [r2, 0.0]])
    velocities = np.array([[0.0, v1], [0.0, v2]])

    T = 2.0 * np.pi * np.sqrt(a**3 / (G * M))
    return init_bodies(masses, positions, velocities), T


def init_random_bodies(N, seed=42, box_size=10.0, max_mass=1.0):
    """Initialize N random bodies in a square box with small random velocities."""
    rng = np.random.RandomState(seed)
    masses = rng.uniform(0.1, max_mass, size=N)
    positions = rng.uniform(-box_size / 2, box_size / 2, size=(N, 2))
    velocities = rng.uniform(-0.1, 0.1, size=(N, 2))
    return init_bodies(masses, positions, velocities)


# ---------------------------------------------------------------------------
# Force computation — direct summation O(N^2)
# ---------------------------------------------------------------------------

def compute_accelerations(state, G=G_DEFAULT, softening=1e-4):
    """
    Compute gravitational acceleration on each body via direct pairwise
    summation with Plummer softening.

    a_i = G * sum_{j!=i} m_j * (r_j - r_i) / (|r_j - r_i|^2 + eps^2)^{3/2}

    Parameters
    ----------
    state : dict
    G : float
    softening : float — softening length epsilon

    Returns
    -------
    acc : ndarray, shape (N, 2)
    """
    pos = state['positions']
    mass = state['masses']
    N = len(mass)
    acc = np.zeros_like(pos)

    for i in range(N):
        for j in range(i + 1, N):
            rij = pos[j] - pos[i]
            dist_sq = np.dot(rij, rij) + softening**2
            inv_dist3 = dist_sq ** (-1.5)
            # Acceleration contribution (softened)
            acc[i] += G * mass[j] * rij * inv_dist3
            acc[j] -= G * mass[i] * rij * inv_dist3  # Newton's 3rd law

    return acc


# ---------------------------------------------------------------------------
# Energy computation
# ---------------------------------------------------------------------------

def kinetic_energy(state):
    """Total kinetic energy: sum of 0.5 * m_i * |v_i|^2."""
    m = state['masses']
    v = state['velocities']
    return 0.5 * np.sum(m * np.sum(v**2, axis=1))


def potential_energy(state, G=G_DEFAULT, softening=1e-4):
    """Total gravitational PE: sum_{i<j} -G * m_i * m_j / sqrt(r_ij^2 + eps^2)."""
    pos = state['positions']
    mass = state['masses']
    N = len(mass)
    pe = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            rij = pos[j] - pos[i]
            dist = np.sqrt(np.dot(rij, rij) + softening**2)
            pe -= G * mass[i] * mass[j] / dist
    return pe


def total_energy(state, G=G_DEFAULT, softening=1e-4):
    """Total energy E = KE + PE."""
    return kinetic_energy(state) + potential_energy(state, G, softening)


# ---------------------------------------------------------------------------
# Integrators
# ---------------------------------------------------------------------------

def step_euler(state, dt, G=G_DEFAULT, softening=1e-4):
    """Forward Euler: x += v*dt, v += a*dt."""
    acc = compute_accelerations(state, G, softening)
    state['positions'] = state['positions'] + state['velocities'] * dt
    state['velocities'] = state['velocities'] + acc * dt
    return state


def step_velocity_verlet(state, dt, G=G_DEFAULT, softening=1e-4, acc_old=None):
    """
    Velocity Verlet (Störmer-Verlet) integrator.

    x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2
    v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt

    Returns (state, acc_new) so the caller can cache acceleration.
    """
    if acc_old is None:
        acc_old = compute_accelerations(state, G, softening)

    # Half-step position update using current acceleration
    state['positions'] = (state['positions']
                          + state['velocities'] * dt
                          + 0.5 * acc_old * dt**2)

    acc_new = compute_accelerations(state, G, softening)

    # Velocity update using average of old and new acceleration
    state['velocities'] = (state['velocities']
                           + 0.5 * (acc_old + acc_new) * dt)

    return state, acc_new


def step_leapfrog_kdk(state, dt, G=G_DEFAULT, softening=1e-4, acc_old=None):
    """
    Leapfrog kick-drift-kick integrator.

    v(t+dt/2) = v(t) + a(t)*dt/2       (kick)
    x(t+dt)   = x(t) + v(t+dt/2)*dt    (drift)
    a(t+dt)   = compute_accel(x(t+dt))
    v(t+dt)   = v(t+dt/2) + a(t+dt)*dt/2  (kick)

    Returns (state, acc_new).
    """
    if acc_old is None:
        acc_old = compute_accelerations(state, G, softening)

    # Kick: half-step velocity update
    v_half = state['velocities'] + acc_old * (dt / 2.0)

    # Drift: full-step position update
    state['positions'] = state['positions'] + v_half * dt

    # Compute new accelerations
    acc_new = compute_accelerations(state, G, softening)

    # Kick: complete velocity update
    state['velocities'] = v_half + acc_new * (dt / 2.0)

    return state, acc_new


# ---------------------------------------------------------------------------
# Simulation runner
# ---------------------------------------------------------------------------

def run_simulation(state, dt, n_steps, integrator='verlet', G=G_DEFAULT,
                   softening=1e-4, record_energy_every=0):
    """
    Run an N-body simulation for n_steps time steps.

    Parameters
    ----------
    state : dict
    dt : float
    n_steps : int
    integrator : str — 'euler', 'verlet', or 'leapfrog'
    G : float
    softening : float
    record_energy_every : int — if > 0, record energy every this many steps

    Returns
    -------
    state : dict — final state
    energy_trace : list of (step, E) tuples (empty if record_energy_every==0)
    """
    energy_trace = []

    if record_energy_every > 0:
        E0 = total_energy(state, G, softening)
        energy_trace.append((0, E0))

    acc = None
    if integrator in ('verlet', 'leapfrog'):
        acc = compute_accelerations(state, G, softening)

    for step in range(1, n_steps + 1):
        if integrator == 'euler':
            state = step_euler(state, dt, G, softening)
        elif integrator == 'verlet':
            state, acc = step_velocity_verlet(state, dt, G, softening, acc)
        elif integrator == 'leapfrog':
            state, acc = step_leapfrog_kdk(state, dt, G, softening, acc)
        else:
            raise ValueError(f"Unknown integrator: {integrator}")

        if record_energy_every > 0 and step % record_energy_every == 0:
            E = total_energy(state, G, softening)
            energy_trace.append((step, E))

    return state, energy_trace


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Quick smoke test: circular binary
    state, T = init_circular_binary(m1=1.0, m2=1.0, a=1.0)
    print(f"Circular binary: T = {T:.6f}")
    print(f"  Initial positions: {state['positions']}")
    print(f"  Initial velocities: {state['velocities']}")
    print(f"  Initial KE = {kinetic_energy(state):.10f}")
    print(f"  Initial PE = {potential_energy(state):.10f}")
    print(f"  Initial E  = {total_energy(state):.10f}")

    # Verify initialization: COM at origin, total momentum zero
    com = np.average(state['positions'], weights=state['masses'], axis=0)
    total_p = np.sum(state['masses'][:, None] * state['velocities'], axis=0)
    print(f"  COM = {com}")
    print(f"  Total momentum = {total_p}")

    assert np.allclose(com, 0.0, atol=1e-14), "COM not at origin"
    assert np.allclose(total_p, 0.0, atol=1e-14), "Momentum not zero"
    print("\n  [PASS] Initialization tests passed")
