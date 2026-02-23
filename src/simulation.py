"""Simulation loop and state recording for the N-body simulator."""

import math
from src.vector import Vec2
from src.body import Body


class Simulation:
    """Runs an N-body simulation and records state history.

    Parameters
    ----------
    bodies : list of Body
        Initial body states.
    integrator : callable
        Integration step function(bodies, dt, force_func, **kwargs) -> list of Body.
    force_func : callable
        Force function(bodies, **kwargs) -> list of Vec2 accelerations.
    dt : float
        Time step.
    total_time : float
        Total simulation time.
    force_kwargs : dict
        Additional keyword arguments for the force function.
    """

    def __init__(self, bodies, integrator, force_func, dt, total_time,
                 force_kwargs=None):
        self.bodies = [Body(b.mass, b.pos, b.vel) for b in bodies]
        self.integrator = integrator
        self.force_func = force_func
        self.dt = dt
        self.total_time = total_time
        self.force_kwargs = force_kwargs or {}

        self.history_pos = []  # list of list of Vec2 per step
        self.history_vel = []
        self.energies = []     # list of (KE, PE, E) per step
        self.momenta = []      # list of Vec2 (total linear momentum) per step
        self.angular_momenta = []  # list of float per step
        self.times = []

    def _compute_kinetic_energy(self, bodies):
        return sum(b.kinetic_energy() for b in bodies)

    def _compute_potential_energy(self, bodies, G=1.0, softening=0.0):
        n = len(bodies)
        pe = 0.0
        eps2 = softening * softening
        for i in range(n):
            for j in range(i + 1, n):
                dx = bodies[j].pos.x - bodies[i].pos.x
                dy = bodies[j].pos.y - bodies[i].pos.y
                r = math.sqrt(dx * dx + dy * dy + eps2)
                pe -= G * bodies[i].mass * bodies[j].mass / r
        return pe

    def _compute_linear_momentum(self, bodies):
        px, py = 0.0, 0.0
        for b in bodies:
            px += b.mass * b.vel.x
            py += b.mass * b.vel.y
        return Vec2(px, py)

    def _compute_angular_momentum(self, bodies):
        L = 0.0
        for b in bodies:
            L += b.mass * (b.pos.x * b.vel.y - b.pos.y * b.vel.x)
        return L

    def _record_state(self, bodies, t):
        G = self.force_kwargs.get('G', 1.0)
        softening = self.force_kwargs.get('softening', 0.0)

        self.history_pos.append([b.pos for b in bodies])
        self.history_vel.append([b.vel for b in bodies])

        ke = self._compute_kinetic_energy(bodies)
        pe = self._compute_potential_energy(bodies, G, softening)
        self.energies.append((ke, pe, ke + pe))

        self.momenta.append(self._compute_linear_momentum(bodies))
        self.angular_momenta.append(self._compute_angular_momentum(bodies))
        self.times.append(t)

    def run(self):
        """Execute the simulation, recording state at each step."""
        t = 0.0
        self._record_state(self.bodies, t)

        n_steps = int(self.total_time / self.dt)
        for _ in range(n_steps):
            self.bodies = self.integrator(
                self.bodies, self.dt, self.force_func, **self.force_kwargs
            )
            t += self.dt
            self._record_state(self.bodies, t)

        return self

    def relative_energy_error(self):
        """Return list of relative energy errors |E(t) - E(0)| / |E(0)|."""
        if not self.energies:
            return []
        E0 = self.energies[0][2]
        if E0 == 0:
            return [abs(e[2]) for e in self.energies]
        return [abs((e[2] - E0) / E0) for e in self.energies]
