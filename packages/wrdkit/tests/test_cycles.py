"""Step and cycle segmentation."""

import pytest

import synthetic
from wrdkit import extract_profile, read_wrd_bytes, segment_steps, summarize_cycles


def test_steps_split_on_the_instrument_step_counter(synthetic_wrd):
    steps = segment_steps(synthetic_wrd)
    assert [s.mode for s in steps[:4]] == ["charge", "rest", "discharge", "rest"]
    assert len(steps) == 12  # 3 cycles x (charge, rest, discharge, rest)


def test_step_capacity_is_the_delta_across_the_step(synthetic_wrd):
    charge = next(s for s in segment_steps(synthetic_wrd) if s.mode == "charge")
    assert charge.capacity_mah == pytest.approx(5.0)
    assert charge.voltage_start == pytest.approx(1.9)
    assert charge.voltage_end == pytest.approx(3.6)


def test_cycle_capacities_and_efficiency(synthetic_wrd):
    cycles = summarize_cycles(synthetic_wrd)
    assert [c.cycle_number for c in cycles] == [1, 2, 3]
    assert cycles[0].discharge_capacity_mah == pytest.approx(5.0)
    assert cycles[1].discharge_capacity_mah == pytest.approx(4.9)
    assert cycles[0].coulombic_efficiency == pytest.approx(100.0)
    assert cycles[0].energy_efficiency == pytest.approx(100.0 * 3.1 / 3.2)


def test_mean_voltages_are_energy_weighted(synthetic_wrd):
    cycle = summarize_cycles(synthetic_wrd)[0]
    assert cycle.mean_charge_voltage == pytest.approx(3.2)
    assert cycle.mean_discharge_voltage == pytest.approx(3.1)
    assert cycle.voltage_hysteresis == pytest.approx(0.1)


def test_cycle_offset_renumbers_a_continuation_file(synthetic_wrd):
    cycles = summarize_cycles(synthetic_wrd, cycle_offset=100)
    assert [c.cycle_number for c in cycles] == [101, 102, 103]


def test_a_truncated_final_cycle_is_flagged_incomplete():
    samples = synthetic.make_cycles(2, 20)
    truncated = read_wrd_bytes(synthetic.build_wrd(samples[:-15]))
    cycles = summarize_cycles(truncated)
    assert cycles[0].complete is True
    assert cycles[-1].complete is False


def test_profiles_start_from_zero_capacity(synthetic_wrd):
    cycles = summarize_cycles(synthetic_wrd)
    discharge = extract_profile(synthetic_wrd, cycles[1], "discharge")
    assert discharge.branch == "discharge"
    assert discharge.capacity_mah[0] == pytest.approx(0.0)
    assert discharge.capacity_mah[-1] == pytest.approx(4.9)
    assert discharge.voltage[0] == pytest.approx(3.6)
    assert discharge.voltage[-1] == pytest.approx(1.9)


def test_profile_for_a_missing_branch_is_empty(synthetic_wrd):
    cycles = summarize_cycles(synthetic_wrd)
    cycles[0].steps = [s for s in cycles[0].steps if s.mode != "charge"]
    assert len(extract_profile(synthetic_wrd, cycles[0], "charge")) == 0


def test_unknown_branch_is_rejected(synthetic_wrd):
    cycles = summarize_cycles(synthetic_wrd)
    with pytest.raises(ValueError, match="branch must be"):
        extract_profile(synthetic_wrd, cycles[0], "float")
