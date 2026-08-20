"""The synthetic fixture's own contract.

Every other test in this package reads a file this module wrote, so a fixture
that invents its own convention makes the whole suite agree on the wrong
number.  These tests pin the two conventions the reference file established
(``docs/raw/specs/wrd-binary-format.md``): ``CHARGE Q`` / ``DISCHARGE Q`` are
per-cycle running totals, and a step's capacity is therefore the difference
across the step rather than the value at its end.
"""

import pytest

from wrdkit import extract_profile, read_wrd_bytes, segment_steps, summarize_cycles

import synthetic


def _read(samples, **kwargs):
    return read_wrd_bytes(synthetic.build_wrd(samples, **kwargs))


def test_charge_q_resets_once_per_cycle_not_once_per_step():
    wrd = _read(synthetic.make_cycles(3, 20))
    charge = wrd.charge_mah()
    discharge = wrd.discharge_mah()
    for cycle in summarize_cycles(wrd):
        assert charge[cycle.start] == pytest.approx(0.0)
        assert discharge[cycle.start] == pytest.approx(0.0)
        assert charge[cycle.stop - 1] == pytest.approx(cycle.charge_capacity_mah)
        assert discharge[cycle.stop - 1] == pytest.approx(
            cycle.discharge_capacity_mah)


def test_charge_q_is_parked_at_the_charge_capacity_while_discharging():
    """The instrument holds CHARGE Q through the discharge; it does not zero it."""
    wrd = _read(synthetic.make_cycles(2, 20))
    charge = wrd.charge_mah()
    for cycle in summarize_cycles(wrd):
        steps = [s for s in cycle.steps if s.mode == "discharge"]
        assert steps
        for step in steps:
            window = charge[step.start:step.stop]
            assert window.min() == pytest.approx(window.max())
            assert window[0] == pytest.approx(cycle.charge_capacity_mah)


def test_a_two_step_charge_counts_each_step_delta_once():
    """CC and CV share one running total, so each step contributes its delta.

    Reading the value at the *end* of each step instead would count the CC
    capacity twice (4 + 5 instead of 4 + 1) -- the regression that silently
    inflates charge capacity and depresses coulombic efficiency on real CC-CV
    files.  This is the lock on ``segment_steps``' difference arithmetic.
    """
    wrd = _read(synthetic.make_cycles(1, 20, cv_points=8,
                                      cv_capacity_fraction=0.2))
    charge_steps = [s for s in segment_steps(wrd) if s.mode == "charge"]
    assert len(charge_steps) == 2
    assert charge_steps[0].capacity_mah == pytest.approx(4.0)
    assert charge_steps[1].capacity_mah == pytest.approx(1.0)

    cycle = summarize_cycles(wrd)[0]
    assert cycle.charge_capacity_mah == pytest.approx(5.0)
    assert cycle.coulombic_efficiency == pytest.approx(100.0)
    assert cycle.mean_charge_voltage == pytest.approx(3.2)

    profile = extract_profile(wrd, cycle, "charge")
    assert profile.capacity_mah[0] == pytest.approx(0.0)
    assert profile.capacity_mah[-1] == pytest.approx(5.0)


def test_unit_coulomb_header_switches_the_capacity_unit():
    samples = synthetic.make_cycles(1, 20)
    amp_hours = _read(samples)
    coulombs = _read(samples, unit_coulomb=True)
    assert amp_hours.metadata.unit_coulomb is False
    assert coulombs.metadata.unit_coulomb is True
    assert coulombs.charge_mah()[-1] == pytest.approx(
        amp_hours.charge_mah()[-1] / 3600.0)
