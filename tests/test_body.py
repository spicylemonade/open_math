"""Unit tests for Body."""

import math
from src.vector import Vec2
from src.body import Body


def test_creation():
    b = Body(1.0, Vec2(0, 0))
    assert b.mass == 1.0
    assert b.pos == Vec2(0, 0)
    assert b.vel == Vec2(0, 0)


def test_creation_with_velocity():
    b = Body(2.0, Vec2(1, 2), Vec2(3, 4))
    assert b.mass == 2.0
    assert b.vel == Vec2(3, 4)


def test_kinetic_energy():
    b = Body(2.0, Vec2(0, 0), Vec2(3, 4))
    assert abs(b.kinetic_energy() - 25.0) < 1e-10


def test_kinetic_energy_at_rest():
    b = Body(1.0, Vec2(0, 0))
    assert b.kinetic_energy() == 0.0


def test_momentum():
    b = Body(2.0, Vec2(0, 0), Vec2(3, 4))
    p = b.momentum()
    assert p == Vec2(6, 8)


def test_angular_momentum():
    b = Body(1.0, Vec2(1, 0), Vec2(0, 1))
    assert abs(b.angular_momentum() - 1.0) < 1e-10


def test_angular_momentum_zero():
    b = Body(1.0, Vec2(1, 0), Vec2(1, 0))
    assert abs(b.angular_momentum()) < 1e-10


def test_repr():
    b = Body(1.0, Vec2(0, 0))
    assert "Body" in repr(b)


def test_equality():
    b1 = Body(1.0, Vec2(1, 2), Vec2(3, 4))
    b2 = Body(1.0, Vec2(1, 2), Vec2(3, 4))
    assert b1 == b2
