"""Unit tests for Vec2."""

import math
import pytest
from src.vector import Vec2


def test_creation():
    v = Vec2(3.0, 4.0)
    assert v.x == 3.0
    assert v.y == 4.0


def test_creation_default():
    v = Vec2()
    assert v.x == 0.0 and v.y == 0.0


def test_addition():
    assert Vec2(1, 2) + Vec2(3, 4) == Vec2(4, 6)


def test_subtraction():
    assert Vec2(5, 7) - Vec2(2, 3) == Vec2(3, 4)


def test_scalar_multiply():
    assert Vec2(1, 2) * 3 == Vec2(3, 6)


def test_rmul():
    assert 3 * Vec2(1, 2) == Vec2(3, 6)


def test_division():
    assert Vec2(6, 4) / 2 == Vec2(3, 2)


def test_negation():
    assert -Vec2(1, -2) == Vec2(-1, 2)


def test_dot_product():
    assert Vec2(1, 2).dot(Vec2(3, 4)) == 11.0


def test_cross_product():
    assert Vec2(1, 0).cross(Vec2(0, 1)) == 1.0
    assert Vec2(0, 1).cross(Vec2(1, 0)) == -1.0


def test_magnitude():
    assert Vec2(3, 4).magnitude() == 5.0


def test_magnitude_squared():
    assert Vec2(3, 4).magnitude_squared() == 25.0


def test_unit_vector():
    u = Vec2(3, 4).unit()
    assert abs(u.x - 0.6) < 1e-10
    assert abs(u.y - 0.8) < 1e-10
    assert abs(u.magnitude() - 1.0) < 1e-10


def test_unit_zero_raises():
    with pytest.raises(ValueError):
        Vec2(0, 0).unit()


def test_distance_to():
    d = Vec2(0, 0).distance_to(Vec2(3, 4))
    assert abs(d - 5.0) < 1e-10


def test_immutability():
    v = Vec2(1, 2)
    with pytest.raises(AttributeError):
        v.x = 5


def test_repr():
    assert "Vec2" in repr(Vec2(1, 2))
