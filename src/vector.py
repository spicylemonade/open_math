"""2D vector mathematics for the gravity simulator."""

import math


class Vec2:
    """Immutable 2D vector with standard arithmetic operations."""

    __slots__ = ('x', 'y')

    def __init__(self, x: float = 0.0, y: float = 0.0):
        object.__setattr__(self, 'x', float(x))
        object.__setattr__(self, 'y', float(y))

    def __setattr__(self, name, value):
        raise AttributeError("Vec2 is immutable")

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vec2(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __eq__(self, other):
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def dot(self, other):
        """Dot product with another Vec2."""
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        """2D cross product (scalar): self.x * other.y - self.y * other.x."""
        return self.x * other.y - self.y * other.x

    def magnitude(self):
        """Euclidean magnitude (length) of the vector."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def magnitude_squared(self):
        """Squared magnitude, avoids sqrt for performance."""
        return self.x * self.x + self.y * self.y

    def unit(self):
        """Return the unit vector in the same direction. Raises if zero vector."""
        mag = self.magnitude()
        if mag == 0.0:
            raise ValueError("Cannot normalize zero vector")
        return Vec2(self.x / mag, self.y / mag)

    def distance_to(self, other):
        """Euclidean distance to another Vec2."""
        return (self - other).magnitude()
