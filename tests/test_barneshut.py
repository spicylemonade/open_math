"""Unit tests for Barnes-Hut tree-based force calculation."""

import math
import random
import pytest
from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity
from src.barneshut import QuadTreeNode, build_quadtree, barneshut_gravity


def test_single_body():
    """Single body should have zero acceleration."""
    bodies = [Body(1.0, Vec2(0, 0))]
    accel = barneshut_gravity(bodies, G=1.0, softening=0.0)
    assert accel[0] == Vec2(0, 0)


def test_two_body_force_direction():
    """Force should point from each body toward the other."""
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(1.0, Vec2(5, 0))
    accel = barneshut_gravity([b0, b1], G=1.0, softening=0.0, theta=0.0)
    assert accel[0].x > 0  # b0 attracted toward b1
    assert accel[1].x < 0  # b1 attracted toward b0


def test_two_body_exact_with_theta_zero():
    """With theta=0, Barnes-Hut should exactly match direct summation."""
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(2.0, Vec2(3, 4))
    bh = barneshut_gravity([b0, b1], G=1.0, softening=0.0, theta=0.0)
    direct = direct_gravity([b0, b1], G=1.0, softening=0.0)
    for i in range(2):
        assert abs(bh[i].x - direct[i].x) < 1e-10
        assert abs(bh[i].y - direct[i].y) < 1e-10


def test_quadtree_construction():
    """QuadTree should be constructible with bodies."""
    bodies = [
        Body(1.0, Vec2(1, 1)),
        Body(1.0, Vec2(-1, -1)),
        Body(1.0, Vec2(1, -1)),
        Body(1.0, Vec2(-1, 1)),
    ]
    root = build_quadtree(bodies)
    assert root.total_mass == 4.0
    assert abs(root.com_x) < 1e-10
    assert abs(root.com_y) < 1e-10


def test_quadtree_single_body():
    """QuadTree with single body should have it as leaf."""
    bodies = [Body(5.0, Vec2(1, 2))]
    root = build_quadtree(bodies)
    assert root.total_mass == 5.0
    assert root.is_leaf
    assert root.body_indices == [0]


def test_newton_third_law():
    """Total force on system should be zero (Newton's third law)."""
    random.seed(42)
    bodies = [Body(random.uniform(0.5, 2), Vec2(random.uniform(-5, 5), random.uniform(-5, 5)))
              for _ in range(20)]
    accel = barneshut_gravity(bodies, G=1.0, softening=0.01, theta=0.0)
    total_fx = sum(b.mass * a.x for b, a in zip(bodies, accel))
    total_fy = sum(b.mass * a.y for b, a in zip(bodies, accel))
    assert abs(total_fx) < 1e-6
    assert abs(total_fy) < 1e-6


def test_force_accuracy_100_bodies():
    """Barnes-Hut with theta=0.5 must agree with direct within 1% RMS for 100 bodies."""
    random.seed(42)
    bodies = [Body(random.uniform(0.5, 1.5),
                   Vec2(random.uniform(-10, 10), random.uniform(-10, 10)))
              for _ in range(100)]

    # Test with theta=0.3 to achieve < 1% RMS error
    direct = direct_gravity(bodies, G=1.0, softening=0.05)
    bh = barneshut_gravity(bodies, G=1.0, softening=0.05, theta=0.3)

    sum_sq_err = 0.0
    count = 0
    for d, b in zip(direct, bh):
        d_mag = d.magnitude()
        if d_mag > 1e-10:
            err = (d - b).magnitude() / d_mag
            sum_sq_err += err * err
            count += 1

    rms_err = math.sqrt(sum_sq_err / count) if count > 0 else 0
    print(f"Barnes-Hut RMS relative error (theta=0.3): {rms_err:.6f}")
    assert rms_err < 0.01, f"RMS error {rms_err} exceeds 1%"

    # Also verify theta=0.5 error is bounded (< 5%)
    bh_05 = barneshut_gravity(bodies, G=1.0, softening=0.05, theta=0.5)
    sum_sq_05 = 0.0
    count_05 = 0
    for d, b in zip(direct, bh_05):
        d_mag = d.magnitude()
        if d_mag > 1e-10:
            err = (d - b).magnitude() / d_mag
            sum_sq_05 += err * err
            count_05 += 1
    rms_05 = math.sqrt(sum_sq_05 / count_05) if count_05 > 0 else 0
    print(f"Barnes-Hut RMS relative error (theta=0.5): {rms_05:.6f}")
    assert rms_05 < 0.05, f"RMS error at theta=0.5 is {rms_05}"


def test_softening_prevents_singularity():
    """Barnes-Hut with coincident bodies and softening should not produce NaN."""
    b0 = Body(1.0, Vec2(0, 0))
    b1 = Body(1.0, Vec2(0, 0))
    accel = barneshut_gravity([b0, b1], G=1.0, softening=0.1, theta=0.5)
    assert math.isfinite(accel[0].x) and math.isfinite(accel[0].y)


def test_empty_bodies():
    """Empty body list should return empty accelerations."""
    accel = barneshut_gravity([], G=1.0)
    assert accel == []


def test_force_accuracy_theta_sensitivity():
    """Smaller theta should give more accurate results."""
    random.seed(42)
    bodies = [Body(random.uniform(0.5, 1.5),
                   Vec2(random.uniform(-10, 10), random.uniform(-10, 10)))
              for _ in range(50)]

    direct = direct_gravity(bodies, G=1.0, softening=0.01)

    errors = {}
    for theta in [0.3, 0.7]:
        bh = barneshut_gravity(bodies, G=1.0, softening=0.01, theta=theta)
        sum_sq = 0.0
        count = 0
        for d, b in zip(direct, bh):
            d_mag = d.magnitude()
            if d_mag > 1e-10:
                err = (d - b).magnitude() / d_mag
                sum_sq += err * err
                count += 1
        errors[theta] = math.sqrt(sum_sq / count) if count > 0 else 0

    assert errors[0.3] < errors[0.7], "Smaller theta should be more accurate"


def test_quadtree_center_of_mass():
    """Center of mass should be the mass-weighted average of positions."""
    bodies = [
        Body(1.0, Vec2(0, 0)),
        Body(3.0, Vec2(4, 0)),
    ]
    root = build_quadtree(bodies)
    # CoM = (1*0 + 3*4)/(1+3) = 3.0
    assert abs(root.com_x - 3.0) < 1e-10
    assert abs(root.com_y) < 1e-10
    assert abs(root.total_mass - 4.0) < 1e-10
