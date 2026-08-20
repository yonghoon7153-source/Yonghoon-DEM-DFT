"""Conditions inferred from the embedded schedule."""

import pytest

from wrdkit import Schedule, ScheduleStep


def _schedule(formation_a: float | None, cycling_a: float,
              loop_count: int = 50) -> Schedule:
    """Formation once, then a looped charge/discharge pair.

    Mirrors what the Schedule Editor writes: the loop's last step points back
    at the first step of the loop, which is how ``cycling_current_a`` and
    ``formation_current_a`` tell the two parts apart.
    """
    steps: list[ScheduleStep] = []
    if formation_a is not None:
        steps += [
            ScheduleStep(index=len(steps), name="form_chg", control="CC",
                         control_raw=0, current_a=formation_a),
            ScheduleStep(index=len(steps) + 1, name="form_dch", control="CC",
                         control_raw=0, current_a=-formation_a),
        ]
    steps += [
        ScheduleStep(index=len(steps), name="cyc_chg", control="CC",
                     control_raw=0, current_a=cycling_a),
        ScheduleStep(index=len(steps) + 1, name="cyc_dch", control="CC",
                     control_raw=0, current_a=-cycling_a,
                     loop_count=loop_count, loop_target="cyc_chg"),
    ]
    return Schedule(version="1.0", source_path=None, steps=steps)


def test_an_unambiguous_current_ratio_gives_the_c_rate():
    # 0.1C formation, 0.5C cycling -- ratio 5 matches only one pair.
    schedule = _schedule(formation_a=0.52e-3, cycling_a=2.6e-3)
    assert schedule.infer_c_rate() == pytest.approx(0.5)
    assert schedule.nominal_capacity_ah() == pytest.approx(5.2e-3)


def test_an_ambiguous_current_ratio_is_reported_as_unknown():
    """0.05C/0.1C and 0.1C/0.2C are both ratio 2 -- guessing halves the capacity."""
    schedule = _schedule(formation_a=0.26e-3, cycling_a=0.52e-3)
    assert schedule.infer_c_rate() is None
    assert schedule.nominal_capacity_ah() is None
    # An explicit rate still works: only the guess is withheld.
    assert schedule.nominal_capacity_ah(0.1) == pytest.approx(5.2e-3)


def test_a_schedule_without_formation_infers_nothing():
    schedule = _schedule(formation_a=None, cycling_a=2.6e-3)
    assert schedule.infer_c_rate() is None
    assert schedule.nominal_capacity_ah() is None


def test_an_unrecognised_ratio_infers_nothing():
    schedule = _schedule(formation_a=1.0e-3, cycling_a=7.3e-3)
    assert schedule.infer_c_rate() is None


def test_the_cycling_current_is_the_looped_one():
    schedule = _schedule(formation_a=0.52e-3, cycling_a=2.6e-3)
    assert schedule.cycling_current_a == pytest.approx(2.6e-3)
    assert schedule.formation_current_a == pytest.approx(0.52e-3)
    assert schedule.planned_cycles == 50
