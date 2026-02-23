"""Unit tests for direct gravitational force computation."""

import math
import pytest
from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity


def test_two_body_force_magnitude():
    """Force on body 0 due to body 1 should match G*m1*m2/r^2."""
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(1.0, Vec2(1, 0))
    accel = direct_gravity([b0, b1], G=1.0, softening=0.0)
    # a = G * m_j / r^2 = 1.0 * 1.0 / 1.0 = 1.0 in +x direction
    assert abs(accel[0].x - 1.0) < 1e-10
    assert abs(accel[0].y) < 1e-10


def test_two_body_force_direction():
    """Force on each body points toward the other."""
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(1.0, Vec2(0, 2))
    accel = direct_gravity([b0, b1], G=1.0)
    # a0 should point toward b1 (+y), a1 toward b0 (-y)
    assert accel[0].y > 0
    assert accel[1].y < 0


def test_two_body_inverse_square():
    """Doubling distance should reduce acceleration by factor 4."""
    b0 = Body(1.0, Vec2(0, 0))
    b1_near = Body(1.0, Vec2(1, 0))
    b1_far = Body(1.0, Vec2(2, 0))

    a_near = direct_gravity([b0, b1_near], G=1.0)[0].x
    a_far = direct_gravity([b0, b1_far], G=1.0)[0].x

    assert abs(a_near / a_far - 4.0) < 1e-10


def test_newton_third_law():
    """Forces on two bodies should be equal and opposite (F = ma)."""
    b0 = Body(2.0, Vec2(0, 0))
    b1 = Body(3.0, Vec2(1, 1))
    accel = direct_gravity([b0, b1], G=1.0)
    # m0*a0 + m1*a1 should be zero
    fx = b0.mass * accel[0].x + b1.mass * accel[1].x
    fy = b0.mass * accel[0].y + b1.mass * accel[1].y
    assert abs(fx) < 1e-10
    assert abs(fy) < 1e-10


def test_symmetric_triangle_zero_net():
    """Three equal masses at equilateral triangle vertices: by symmetry, net force on centroid-placed body not tested,
    but net total force on system should be zero."""
    s = 1.0
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(1.0, Vec2(s, 0))
    b2 = Body(1.0, Vec2(s / 2, s * math.sqrt(3) / 2))
    accel = direct_gravity([b0, b1, b2], G=1.0)
    # Total force on system = sum(m_i * a_i) should be zero
    total_fx = sum(b.mass * a.x for b, a in zip([b0, b1, b2], accel))
    total_fy = sum(b.mass * a.y for b, a in zip([b0, b1, b2], accel))
    assert abs(total_fx) < 1e-10
    assert abs(total_fy) < 1e-10


def test_symmetric_square_zero_net():
    """Four equal masses at square corners: total force zero."""
    bodies = [
        Body(1.0, Vec2(1, 1)),
        Body(1.0, Vec2(-1, 1)),
        Body(1.0, Vec2(-1, -1)),
        Body(1.0, Vec2(1, -1)),
    ]
    accel = direct_gravity(bodies, G=1.0)
    total_fx = sum(b.mass * a.x for b, a in zip(bodies, accel))
    total_fy = sum(b.mass * a.y for b, a in zip(bodies, accel))
    assert abs(total_fx) < 1e-10
    assert abs(total_fy) < 1e-10


def test_softening_prevents_singularity():
    """With zero separation, softening should prevent NaN/inf."""
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(1.0, Vec2(0, 0))
    accel = direct_gravity([b0, b1], G=1.0, softening=0.1)
    assert math.isfinite(accel[0].x) and math.isfinite(accel[0].y)
    assert math.isfinite(accel[1].x) and math.isfinite(accel[1].y)


def test_softening_reduces_force():
    """Softening should reduce force magnitude compared to unsoftened."""
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(1.0, Vec2(0.1, 0))
    a_hard = direct_gravity([b0, b1], G=1.0, softening=0.0)[0].magnitude()
    a_soft = direct_gravity([b0, b1], G=1.0, softening=0.1)[0].magnitude()
    assert a_soft < a_hard


def test_single_body():
    """Single body should have zero acceleration."""
    b0 = Body(1.0, Vec2(0, 0))
    accel = direct_gravity([b0], G=1.0)
    assert accel[0] == Vec2(0, 0)


def test_gravitational_constant_scaling():
    """Doubling G should double the acceleration."""
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(1.0, Vec2(1, 0))
    a1 = direct_gravity([b0, b1], G=1.0)[0].x
    a2 = direct_gravity([b0, b1], G=2.0)[0].x
    assert abs(a2 / a1 - 2.0) < 1e-10
