"""Step and cycle segmentation."""

import dataclasses

import pytest

from wrdkit import extract_profile, read_wrd_bytes, segment_steps, summarize_cycles
from wrdkit.schedule import Cutoff, Schedule, ScheduleStep

import synthetic

TAPER_A = 0.26e-3


def _cccv_discharge_schedule() -> Schedule:
    """A CCCV discharge holding 1.9 V until the current tapers to TAPER_A."""
    return Schedule(version=None, source_path=None, steps=[
        ScheduleStep(index=0, name="chg", control="CC", control_raw=0,
                     current_a=1.0e-3,
                     cutoffs=[Cutoff("voltage", ">=", 3.6, 0.0)]),
        ScheduleStep(index=1, name="dch", control="CCCV", control_raw=13,
                     current_a=-1.0e-3, voltage_limit_v=1.9,
                     taper_current_a=TAPER_A,
                     cutoffs=[Cutoff("voltage", "<=", 1.9, 0.0),
                              Cutoff("current", "<=", TAPER_A, 0.0)]),
    ])


def _file_ending_in_cv_hold(current_a: float):
    """A file whose last sample sits at the cut-off voltage, still discharging."""
    samples = synthetic.make_cycles(2, 20)
    while samples[-1].cell_status == 1:   # drop the trailing rest of cycle 2
        samples.pop()
    samples[-1] = dataclasses.replace(samples[-1], voltage=1.9, current=current_a)
    wrd = read_wrd_bytes(synthetic.build_wrd(samples))
    wrd.metadata.schedule = _cccv_discharge_schedule()
    return wrd


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


def test_a_file_split_during_a_cv_hold_is_flagged_incomplete():
    """Voltage alone cannot see the missing taper: it sits at the cut-off."""
    cycles = summarize_cycles(_file_ending_in_cv_hold(-1.0e-3))
    assert cycles[0].complete is True
    assert cycles[-1].complete is False


def test_a_cv_hold_that_reached_its_taper_stays_complete():
    cycles = summarize_cycles(_file_ending_in_cv_hold(-0.2e-3))
    assert cycles[-1].complete is True


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


# --- taper 후보 범위 --------------------------------------------------------
#
# 후보를 스케줄 전체에서 max() 로 고르면 formation taper 와 cycling taper 가
# 섞인다. formation 이 0.5 mA 까지, cycling 이 0.05 mA 까지 내려가는 흔한
# 조합에서, 0.2 mA 에서 잘린 cycling CV 가 0.5 mA 를 잣대로 삼아 complete 로
# 통과했다.

def _schedule_with_two_tapers():
    from wrdkit.schedule import Schedule, ScheduleStep

    return Schedule(version=0, source_path="", steps=[
        ScheduleStep(index=0, name="form-chg", control="CCCV", control_raw=13,
                     current_a=0.001, taper_current_a=0.0005),
        ScheduleStep(index=1, name="form-dch", control="CC", control_raw=0,
                     current_a=-0.001),
        ScheduleStep(index=2, name="cyc-chg", control="CCCV", control_raw=13,
                     current_a=0.002, taper_current_a=0.00005),
        ScheduleStep(index=3, name="cyc-dch", control="CC", control_raw=0,
                     current_a=-0.002, loop_target="cyc-chg", loop_count=1000),
    ])


def test_the_taper_comes_from_the_looped_steps_not_the_whole_schedule():
    schedule = _schedule_with_two_tapers()
    assert schedule.taper_current_a("charge") == 0.00005, \
        "formation taper 가 cycling 판정의 잣대가 됐다"


def test_a_schedule_without_a_loop_still_answers():
    from wrdkit.schedule import Schedule, ScheduleStep

    schedule = Schedule(version=0, source_path="", steps=[
        ScheduleStep(index=0, name="chg", control="CCCV", control_raw=13,
                     current_a=0.001, taper_current_a=0.0005),
    ])
    assert schedule.taper_current_a("charge") == 0.0005


def test_a_direction_with_no_taper_is_none():
    assert _schedule_with_two_tapers().taper_current_a("discharge") is None
