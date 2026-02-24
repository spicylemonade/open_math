"""
Minimal pendulum simulation with multiple numerical integrators.

Solves: theta'' = -(g/L)*sin(theta) - b*omega
State:  [theta, omega] where omega = d(theta)/dt

Integrators: Euler (1st order), RK4 (4th order), Stormer-Verlet (2nd order, symplectic)
"""

import numpy as np
from scipy.special import ellipk


# ---------------------------------------------------------------------------
# Core physics
# ---------------------------------------------------------------------------

def pendulum_deriv(theta, omega, g, L, b=0.0):
    """Compute d(omega)/dt = -(g/L)*sin(theta) - b*omega."""
    return -(g / L) * np.sin(theta) - b * omega


def energy(theta, omega, m, L, g):
    """Total mechanical energy: E = 0.5*m*L^2*omega^2 - m*g*L*cos(theta)."""
    return 0.5 * m * L**2 * omega**2 - m * g * L * np.cos(theta)


def exact_period(theta0, L, g):
    """Exact period via complete elliptic integral: T = 4*sqrt(L/g)*K(sin(theta0/2))."""
    k = np.sin(theta0 / 2.0)
    return 4.0 * np.sqrt(L / g) * ellipk(k**2)  # ellipk takes m = k^2


def small_angle_period(L, g):
    """Small-angle period: T0 = 2*pi*sqrt(L/g)."""
    return 2.0 * np.pi * np.sqrt(L / g)


# ---------------------------------------------------------------------------
# Integrators
# ---------------------------------------------------------------------------

def step_euler(theta, omega, dt, g, L, b=0.0):
    """Forward Euler step."""
    a = pendulum_deriv(theta, omega, g, L, b)
    theta_new = theta + dt * omega
    omega_new = omega + dt * a
    return theta_new, omega_new


def step_rk4(theta, omega, dt, g, L, b=0.0):
    """Classical 4th-order Runge-Kutta step."""
    def f(th, om):
        return om, pendulum_deriv(th, om, g, L, b)

    k1_th, k1_om = f(theta, omega)
    k2_th, k2_om = f(theta + 0.5*dt*k1_th, omega + 0.5*dt*k1_om)
    k3_th, k3_om = f(theta + 0.5*dt*k2_th, omega + 0.5*dt*k2_om)
    k4_th, k4_om = f(theta + dt*k3_th, omega + dt*k3_om)

    theta_new = theta + (dt / 6.0) * (k1_th + 2*k2_th + 2*k3_th + k4_th)
    omega_new = omega + (dt / 6.0) * (k1_om + 2*k2_om + 2*k3_om + k4_om)
    return theta_new, omega_new


def step_verlet(theta, omega, dt, g, L, b=0.0):
    """Stormer-Verlet (leapfrog) kick-drift-kick step."""
    # Half kick
    omega_half = omega + 0.5 * dt * pendulum_deriv(theta, omega, g, L, b)
    # Full drift
    theta_new = theta + dt * omega_half
    # Half kick
    omega_new = omega_half + 0.5 * dt * pendulum_deriv(theta_new, omega_half, g, L, b)
    return theta_new, omega_new


INTEGRATORS = {
    'euler': step_euler,
    'rk4': step_rk4,
    'verlet': step_verlet,
}


# ---------------------------------------------------------------------------
# Simulation runner
# ---------------------------------------------------------------------------

def simulate(method='euler', theta0=0.5, omega0=0.0, L=1.0, g=9.81,
             m=1.0, dt=0.01, n_steps=10000, b=0.0):
    """
    Run a pendulum simulation.

    Parameters
    ----------
    method : str
        Integration method: 'euler', 'rk4', or 'verlet'.
    theta0, omega0 : float
        Initial conditions (rad, rad/s).
    L, g, m : float
        Pendulum length (m), gravity (m/s^2), mass (kg).
    dt : float
        Time step (s).
    n_steps : int
        Number of integration steps.
    b : float
        Damping coefficient (1/s). Default 0 (undamped).

    Returns
    -------
    dict with keys:
        't'      : ndarray of times
        'theta'  : ndarray of angles
        'omega'  : ndarray of angular velocities
        'energy' : ndarray of total energies
        'params' : dict of simulation parameters
    """
    step_fn = INTEGRATORS[method]

    t_arr = np.empty(n_steps + 1)
    theta_arr = np.empty(n_steps + 1)
    omega_arr = np.empty(n_steps + 1)
    energy_arr = np.empty(n_steps + 1)

    theta_arr[0] = theta0
    omega_arr[0] = omega0
    t_arr[0] = 0.0
    energy_arr[0] = energy(theta0, omega0, m, L, g)

    th, om = theta0, omega0
    for i in range(1, n_steps + 1):
        th, om = step_fn(th, om, dt, g, L, b)
        theta_arr[i] = th
        omega_arr[i] = om
        t_arr[i] = i * dt
        energy_arr[i] = energy(th, om, m, L, g)

    return {
        't': t_arr,
        'theta': theta_arr,
        'omega': omega_arr,
        'energy': energy_arr,
        'params': {
            'method': method, 'theta0': theta0, 'omega0': omega0,
            'L': L, 'g': g, 'm': m, 'dt': dt, 'n_steps': n_steps, 'b': b,
        },
    }


def energy_drift(result):
    """Compute energy conservation metric: max|E(t)-E(0)|/|E(0)|."""
    E = result['energy']
    E0 = E[0]
    if abs(E0) < 1e-15:
        return np.max(np.abs(E - E0))
    return np.max(np.abs(E - E0)) / abs(E0)


def extract_period(result):
    """Extract period from simulation via zero-crossing detection of theta."""
    theta = result['theta']
    t = result['t']
    # Find downward zero crossings (positive to negative)
    crossings = []
    for i in range(1, len(theta)):
        if theta[i-1] > 0 and theta[i] <= 0:
            # Linear interpolation
            frac = theta[i-1] / (theta[i-1] - theta[i])
            t_cross = t[i-1] + frac * (t[i] - t[i-1])
            crossings.append(t_cross)
    if len(crossings) < 2:
        return None
    # Period = time between successive same-direction crossings = 2 * half-periods
    periods = np.diff(crossings)
    return np.mean(periods)


def run_timed(method='euler', theta0=0.5, omega0=0.0, L=1.0, g=9.81,
              m=1.0, dt=0.01, n_steps=10000, b=0.0):
    """Run simulate() with wall-clock timing. Returns result dict with 'wall_time_s' added."""
    import time
    t0 = time.perf_counter()
    result = simulate(method=method, theta0=theta0, omega0=omega0,
                      L=L, g=g, m=m, dt=dt, n_steps=n_steps, b=b)
    result['wall_time_s'] = time.perf_counter() - t0
    return result


if __name__ == '__main__':
    import argparse, json

    parser = argparse.ArgumentParser(description='Simple pendulum simulation')
    parser.add_argument('--method', choices=['euler', 'rk4', 'verlet'], default='rk4')
    parser.add_argument('--theta0', type=float, default=0.5)
    parser.add_argument('--omega0', type=float, default=0.0)
    parser.add_argument('--L', type=float, default=1.0)
    parser.add_argument('--g', type=float, default=9.81)
    parser.add_argument('--m', type=float, default=1.0)
    parser.add_argument('--dt', type=float, default=0.01)
    parser.add_argument('--n-steps', type=int, default=10000)
    parser.add_argument('--damping', type=float, default=0.0)
    parser.add_argument('--output', type=str, default=None, help='Save results JSON to file')
    args = parser.parse_args()

    result = run_timed(method=args.method, theta0=args.theta0, omega0=args.omega0,
                       L=args.L, g=args.g, m=args.m, dt=args.dt,
                       n_steps=args.n_steps, b=args.damping)

    drift = energy_drift(result)
    print(f"Method: {args.method}")
    print(f"Steps: {args.n_steps}, dt: {args.dt}")
    print(f"Final theta: {result['theta'][-1]:.6f}")
    print(f"Energy drift: {drift:.6e}")
    print(f"Wall time: {result['wall_time_s']:.4f}s")

    if args.output:
        out = {
            'params': result['params'],
            'wall_time_s': result['wall_time_s'],
            'energy_drift': drift,
            'final_theta': float(result['theta'][-1]),
            'final_omega': float(result['omega'][-1]),
        }
        with open(args.output, 'w') as f:
            json.dump(out, f, indent=2)
        print(f"Results saved to {args.output}")
