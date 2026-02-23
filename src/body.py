"""Body (particle) representation for the gravity simulator."""

from src.vector import Vec2


class Body:
    """A gravitational body with mass, position, and velocity.

    Bodies are treated as value objects: integrators create new Body instances
    rather than mutating existing ones.
    """

    __slots__ = ('mass', 'pos', 'vel')

    def __init__(self, mass: float, pos: Vec2, vel: Vec2 = None):
        self.mass = float(mass)
        self.pos = pos
        self.vel = vel if vel is not None else Vec2(0.0, 0.0)

    def kinetic_energy(self):
        """Kinetic energy: 0.5 * m * |v|^2."""
        return 0.5 * self.mass * self.vel.magnitude_squared()

    def momentum(self):
        """Linear momentum: m * v."""
        return self.vel * self.mass

    def angular_momentum(self):
        """Angular momentum (scalar, 2D): m * (r x v)."""
        return self.mass * self.pos.cross(self.vel)

    def __repr__(self):
        return f"Body(mass={self.mass}, pos={self.pos}, vel={self.vel})"

    def __eq__(self, other):
        if isinstance(other, Body):
            return (self.mass == other.mass and
                    self.pos == other.pos and
                    self.vel == other.vel)
        return NotImplemented
