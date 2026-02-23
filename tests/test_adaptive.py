"""Unit tests for adaptive time-stepping."""

import math
from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity
from src.integrators import leapfrog_step, rk4_step
from src.adaptive import AdaptiveController, adaptive_step, run_adaptive_simulation


def _close_encounter_bodies():
    """Two bodies on a collision course (close encounter)."""
    return [
        Body(1.0, Vec2(0, 0), Vec2(0, 0)),
        Body(1e-6, Vec2(0.1, 0), Vec2(0, 0.5)),
    ]


def _far_apart_bodies():
    """Two bodies far apart (weak forces)."""
    return [
        Body(1.0, Vec2(0, 0), Vec2(0, 0)),
        Body(1e-6, Vec2(100, 0), Vec2(0, 0.01)),
    ]


def test_dt_decreases_close_encounter():
    """dt should decrease when bodies are close (strong acceleration)."""
    close_bodies = _close_encounter_bodies()
    far_bodies = _far_apart_bodies()

    ctrl = AdaptiveController(eta=0.01)

    accel_close = direct_gravity(close_bodies, G=1.0, softening=0.0)
    accel_far = direct_gravity(far_bodies, G=1.0, softening=0.0)

    dt_close = ctrl.compute_dt(accel_close)
    dt_far = ctrl.compute_dt(accel_far)

    assert dt_close < dt_far, f"dt_close={dt_close} should be < dt_far={dt_far}"


def test_dt_increases_slow_phase():
    """dt should increase when forces are weak (far apart)."""
    far_bodies = _far_apart_bodies()
    ctrl = AdaptiveController(eta=0.01, dt_max=10.0)
    accel = direct_gravity(far_bodies, G=1.0, softening=0.0)
    dt = ctrl.compute_dt(accel)
    # Should be close to dt_max since forces are very weak
    assert dt > 0.1, f"dt={dt} should be large for weak forces"


def test_dt_bounded():
    """dt should be bounded between dt_min and dt_max."""
    ctrl = AdaptiveController(eta=0.01, dt_min=0.001, dt_max=0.1)

    # Very strong force -> dt should be dt_min
    strong_accel = [Vec2(1e10, 0)]
    dt = ctrl.compute_dt(strong_accel)
    assert dt == 0.001

    # Very weak force -> dt should be dt_max
    weak_accel = [Vec2(1e-20, 0)]
    dt = ctrl.compute_dt(weak_accel)
    assert dt == 0.1


def test_adaptive_step_returns_dt():
    """adaptive_step should return bodies and dt used."""
    bodies = _close_encounter_bodies()
    ctrl = AdaptiveController(eta=0.01)
    new_bodies, dt = adaptive_step(bodies, direct_gravity, leapfrog_step, ctrl,
                                   G=1.0, softening=0.01)
    assert dt > 0
    assert len(new_bodies) == 2


def test_energy_conservation_adaptive_leapfrog():
    """Adaptive leapfrog should approximately conserve energy on eccentric orbit."""
    # Eccentric two-body orbit
    m1, m2 = 1.0, 1e-6
    e = 0.5
    a = 1.0
    r_peri = a * (1 - e)
    v_peri = math.sqrt((1 + e) / (a * (1 - e)))  # G*M = 1

    bodies = [
        Body(m1, Vec2(0, 0), Vec2(0, 0)),
        Body(m2, Vec2(r_peri, 0), Vec2(0, v_peri)),
    ]

    ctrl = AdaptiveController(eta=0.01, dt_min=1e-6, dt_max=0.05)
    period = 2 * math.pi
    result = run_adaptive_simulation(
        bodies, direct_gravity, leapfrog_step, ctrl,
        total_time=5 * period,
        force_kwargs={'G': 1.0, 'softening': 0.0}
    )

    E0 = result['energies'][0]
    E_final = result['energies'][-1]
    rel_err = abs((E_final - E0) / abs(E0))
    print(f"Adaptive leapfrog energy error: {rel_err:.6e} over 5 periods, {result['step_count']} steps")
    assert rel_err < 0.01, f"Energy error {rel_err} too large"


def test_adaptive_with_rk4():
    """Adaptive stepping should also work with RK4 integrator."""
    bodies = [
        Body(1.0, Vec2(0, 0), Vec2(0, 0)),
        Body(1e-6, Vec2(1, 0), Vec2(0, 1)),
    ]

    ctrl = AdaptiveController(eta=0.01, dt_max=0.1)
    result = run_adaptive_simulation(
        bodies, direct_gravity, rk4_step, ctrl,
        total_time=6.28,
        force_kwargs={'G': 1.0, 'softening': 0.0}
    )

    E0 = result['energies'][0]
    E_final = result['energies'][-1]
    rel_err = abs((E_final - E0) / abs(E0))
    assert rel_err < 0.001, f"RK4 adaptive energy error {rel_err} too large"
