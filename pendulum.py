"""
Super-minimal simple pendulum simulation with multiple numerical integrators.

Physics: theta'' + (g/L) * sin(theta) = 0
State vector: [theta, omega] where omega = d(theta)/dt

Integrators: forward Euler, symplectic Euler, RK4, Stormer-Verlet
"""

import numpy as np
import json
import os
import time

# ─── Physical constants and defaults ───────────────────────────────────────

DEFAULT_PARAMS = {
    "g": 9.81,       # gravitational acceleration (m/s^2)
    "L": 1.0,        # pendulum length (m)
    "m": 1.0,        # bob mass (kg) — cancels in EOM but needed for energy
    "dt": 0.01,      # time step (s)
    "total_time": 10.0,
    "theta_0": np.pi / 6,  # initial angle (rad)
    "omega_0": 0.0,        # initial angular velocity (rad/s)
}

SEED = 42
np.random.seed(SEED)


# ─── Pendulum ODE ──────────────────────────────────────────────────────────

def pendulum_accel(theta, g, L):
    """Compute angular acceleration: alpha = -(g/L)*sin(theta)."""
    return -(g / L) * np.sin(theta)


# ─── Integrators ───────────────────────────────────────────────────────────

def step_euler(theta, omega, dt, g, L):
    """Forward (explicit) Euler method — 1st order, non-symplectic."""
    alpha = pendulum_accel(theta, g, L)
    theta_new = theta + omega * dt
    omega_new = omega + alpha * dt
    return theta_new, omega_new


def step_symplectic_euler(theta, omega, dt, g, L):
    """Symplectic (semi-implicit) Euler — 1st order, symplectic."""
    omega_new = omega + pendulum_accel(theta, g, L) * dt
    theta_new = theta + omega_new * dt
    return theta_new, omega_new


def step_rk4(theta, omega, dt, g, L):
    """Classical 4th-order Runge-Kutta — 4th order, non-symplectic."""
    def f(th, om):
        return om, pendulum_accel(th, g, L)

    k1_th, k1_om = f(theta, omega)
    k2_th, k2_om = f(theta + 0.5 * dt * k1_th, omega + 0.5 * dt * k1_om)
    k3_th, k3_om = f(theta + 0.5 * dt * k2_th, omega + 0.5 * dt * k2_om)
    k4_th, k4_om = f(theta + dt * k3_th, omega + dt * k3_om)

    theta_new = theta + (dt / 6) * (k1_th + 2 * k2_th + 2 * k3_th + k4_th)
    omega_new = omega + (dt / 6) * (k1_om + 2 * k2_om + 2 * k3_om + k4_om)
    return theta_new, omega_new


def step_verlet(theta, omega, dt, g, L):
    """Stormer-Verlet (velocity Verlet) — 2nd order, symplectic."""
    alpha_n = pendulum_accel(theta, g, L)
    theta_new = theta + omega * dt + 0.5 * alpha_n * dt ** 2
    alpha_new = pendulum_accel(theta_new, g, L)
    omega_new = omega + 0.5 * (alpha_n + alpha_new) * dt
    return theta_new, omega_new


INTEGRATORS = {
    "euler": step_euler,
    "symplectic_euler": step_symplectic_euler,
    "rk4": step_rk4,
    "verlet": step_verlet,
}


# ─── Simulation runner ─────────────────────────────────────────────────────

def simulate(method="euler", g=9.81, L=1.0, m=1.0, dt=0.01,
             total_time=10.0, theta_0=np.pi / 6, omega_0=0.0):
    """Run pendulum simulation and return time series.

    Returns dict with keys: t, theta, omega, energy.
    """
    step_fn = INTEGRATORS[method]
    n_steps = int(total_time / dt)

    t = np.zeros(n_steps + 1)
    theta = np.zeros(n_steps + 1)
    omega = np.zeros(n_steps + 1)

    theta[0] = theta_0
    omega[0] = omega_0
    t[0] = 0.0

    for i in range(n_steps):
        theta[i + 1], omega[i + 1] = step_fn(theta[i], omega[i], dt, g, L)
        t[i + 1] = t[i] + dt

    energy = compute_energy(theta, omega, m, g, L)

    return {"t": t, "theta": theta, "omega": omega, "energy": energy}


# ─── Energy computation ────────────────────────────────────────────────────

def compute_energy(theta, omega, m, g, L):
    """Total mechanical energy: E = 0.5*m*L^2*omega^2 - m*g*L*cos(theta)."""
    kinetic = 0.5 * m * L ** 2 * omega ** 2
    potential = -m * g * L * np.cos(theta)
    return kinetic + potential


def energy_drift(energy):
    """Max absolute energy deviation from initial value."""
    return float(np.max(np.abs(energy - energy[0])))


def energy_drift_pct(energy):
    """Energy drift as percentage of initial |energy|."""
    e0 = np.abs(energy[0])
    if e0 < 1e-15:
        return float(np.max(np.abs(energy - energy[0])))
    return float(np.max(np.abs(energy - energy[0])) / e0 * 100)


# ─── Analytical small-angle solution ───────────────────────────────────────

def analytical_small_angle(t, theta_0, g, L):
    """theta(t) = theta_0 * cos(sqrt(g/L) * t) for small angles."""
    omega_n = np.sqrt(g / L)
    return theta_0 * np.cos(omega_n * t)


# ─── Utility: save results to JSON ────────────────────────────────────────

def save_results(data, filename):
    """Save dict to results/ directory as JSON."""
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)
    # Convert numpy arrays to lists for JSON serialization
    serializable = {}
    for k, v in data.items():
        if isinstance(v, np.ndarray):
            serializable[k] = v.tolist()
        elif isinstance(v, (np.floating, np.integer)):
            serializable[k] = float(v)
        else:
            serializable[k] = v
    with open(filepath, "w") as f:
        json.dump(serializable, f, indent=2)
    return filepath


# ─── Main: run forward Euler baseline ──────────────────────────────────────

if __name__ == "__main__":
    result = simulate(method="euler", **{k: DEFAULT_PARAMS[k]
                      for k in ["g", "L", "m", "dt", "total_time",
                                "theta_0", "omega_0"]})
    drift = energy_drift(result["energy"])
    drift_pct = energy_drift_pct(result["energy"])
    print(f"Forward Euler: dt={DEFAULT_PARAMS['dt']}, "
          f"total_time={DEFAULT_PARAMS['total_time']}")
    print(f"  Energy drift (abs): {drift:.6e}")
    print(f"  Energy drift (%):   {drift_pct:.4f}%")
    print(f"  Final theta: {result['theta'][-1]:.6f} rad")

    save_results({
        "method": "euler",
        "dt": DEFAULT_PARAMS["dt"],
        "total_time": DEFAULT_PARAMS["total_time"],
        "theta_0": DEFAULT_PARAMS["theta_0"],
        "omega_0": DEFAULT_PARAMS["omega_0"],
        "g": DEFAULT_PARAMS["g"],
        "L": DEFAULT_PARAMS["L"],
        "energy_drift_abs": drift,
        "energy_drift_pct": drift_pct,
        "final_theta": float(result["theta"][-1]),
        "final_omega": float(result["omega"][-1]),
    }, "euler_baseline.json")
    print("Results saved to results/euler_baseline.json")
