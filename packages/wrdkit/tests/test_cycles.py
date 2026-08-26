"""Step and cycle segmentation."""

import dataclasses
import types

import numpy as np
import pytest

from wrdkit import extract_profile, read_wrd_bytes, segment_steps, summarize_cycles
from wrdkit.cycles import _ends_mid_step
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


# --- 잘린 CV 판정은 실제 스텝의 taper 로 -------------------------------------
#
# 방향의 taper 를 전부 모아 max() 하면 화성과 사이클이 섞인다. STEP INDEX 가
# 스케줄 step 목록을 그대로 가리킨다는 것을 실측 6개 파일(53 스텝, 전부 설정
# 전류와 일치)로 확인했으므로, 추측하지 않고 읽는다.

class _FakeWrd:
    def __init__(self, data, schedule):
        self.data = data
        self.metadata = types.SimpleNamespace(schedule=schedule)

    def __len__(self):
        return len(self.data["voltage"])


def _plan():
    """루프 *안에* taper 가 둘인 계획 — 방향 전체 max() 로는 못 가르는 경우.

    실제로 흔하다: 빠른 사이클(taper 0.05 mA) 사이에 느린 점검 사이클
    (RPT, taper 0.5 mA)을 끼워 넣는 계획이 그렇다.  방향의 taper 를 모아
    max() 하면 0.5 mA 가 잣대가 되어, 0.05 mA 짜리 스텝에서 0.2 mA 에 잘린
    파일이 완료로 통과한다.  방전 쪽도 CCCV 한 다리와 평범한 CC 한 다리를
    같이 둬서, CC 다리가 남의 taper 를 빌려 오는지 본다.
    """
    from wrdkit.schedule import Cutoff, Schedule, ScheduleStep

    return Schedule(version=0, source_path="", steps=[
        ScheduleStep(index=0, name="form-chg", control="CCCV", control_raw=13,
                     current_a=0.001, voltage_limit_v=4.3, taper_current_a=0.0009),
        ScheduleStep(index=1, name="fast-chg", control="CCCV", control_raw=13,
                     current_a=0.002, voltage_limit_v=4.3, taper_current_a=0.00005,
                     loop_target="fast-chg", loop_count=500),
        ScheduleStep(index=2, name="fast-dch", control="CC", control_raw=0,
                     current_a=-0.002, loop_target="fast-chg", loop_count=500,
                     cutoffs=[Cutoff("voltage", "<=", 2.5, 0.0)]),
        ScheduleStep(index=3, name="rpt-chg", control="CCCV", control_raw=13,
                     current_a=0.0005, voltage_limit_v=4.3, taper_current_a=0.0005,
                     loop_target="fast-chg", loop_count=500),
        ScheduleStep(index=4, name="rpt-dch", control="CCCV", control_raw=13,
                     current_a=-0.0005, voltage_limit_v=2.5, taper_current_a=0.0004,
                     loop_target="fast-chg", loop_count=500),
    ])


def _rows(step_index, voltage, current):
    return {
        "step_index": np.array([step_index], dtype=np.int32),
        "voltage": np.array([voltage], dtype=np.float64),
        "current": np.array([current], dtype=np.float64),
    }


def test_a_cv_hold_cut_off_above_its_own_taper_is_incomplete():
    """0.2 mA 에서 잘린 사이클 CV 를 화성 taper 0.5 mA 로 재면 완료로 통과한다."""
    schedule = _plan()
    wrd = _FakeWrd(_rows(1, 4.3, 0.0002), schedule)   # 사이클 CV, taper 0.05 mA
    assert _ends_mid_step(wrd, 1) is True


def test_a_cv_hold_that_reached_its_own_taper_is_complete():
    schedule = _plan()
    wrd = _FakeWrd(_rows(1, 4.3, 0.00004), schedule)  # taper 아래로 내려왔다
    assert _ends_mid_step(wrd, 1) is False


def test_a_plain_cc_leg_ending_at_its_voltage_cutoff_is_complete():
    """taper 가 없는 CC 다리는 전압 컷오프 도달이 곧 종료다.

    방향의 taper 를 빌려 오면(화성의 엄격한 0.5 mA) 정상 종료한 CC 사이클이
    미완료로 버려진다 — 반대 방향의 오류이고, 리포트에서 사이클이 통째로
    사라지므로 더 나쁘다.
    """
    schedule = _plan()
    # step 2 는 taper 가 없는 CC 다리다.  방향의 taper 를 빌려 오면 rpt-dch 의
    # 0.4 mA 가 잣대가 되어, 2.0 mA 로 컷오프에 도달한 정상 종료가 미완료가 된다.
    wrd = _FakeWrd(_rows(2, 2.49, -0.002), schedule)
    assert _ends_mid_step(wrd, 1) is False


def test_an_unknown_step_index_falls_back_to_the_direction():
    """스케줄이 닿지 않는 인덱스면 옛 방식으로라도 판단한다.

    폴백 잣대는 방향 전체의 taper(여기서는 rpt-chg 의 0.5 mA)다. 그보다 훨씬
    큰 전류가 흐르는 중이면 어느 잣대로 재도 잘린 것이다.
    """
    schedule = _plan()
    wrd = _FakeWrd(_rows(99, 4.3, 0.002), schedule)
    assert _ends_mid_step(wrd, 1) is True


def _row(*, total_step, cell_status, charge_q, discharge_q, index):
    """One packed row at a fixed 20 s cadence — the file that found this bug.

    `charge_q`/`discharge_q` are given in **mAh** for readability; the column
    itself is Ah when `UnitCoulomb` is false, which is what the writer wants.
    """
    from synthetic import Sample
    tick = index * 20 * 10_000_000
    return Sample(
        date_ticks=tick, test_ticks=tick, step_ticks=tick, cycle_ticks=tick,
        step_index=total_step, total_step=total_step, cycle_index=1,
        cell_status=cell_status, i_range="1mA",
        voltage=3.6 if cell_status == 3 else 3.4,
        current=0.001 if cell_status == 3 else -0.001,
        charge_q=charge_q / 1000.0, discharge_q=discharge_q / 1000.0,
    )


def test_a_step_keeps_the_charge_that_flowed_before_its_first_sample():
    """스텝 경계는 샘플 **사이**에 떨어진다 — 그 사이의 전하도 이 스텝 것이다.

    실측 (`cell16_… 0.5C_200cyc`, 20 s 샘플링): 방전 스텝의 첫 행이 이미
    0.001~0.005 mAh 를 들고 있다.  스텝이 시작되고 첫 샘플이 찍히기까지 이미
    14 초쯤 흘렀기 때문이다.  그것을 빼면 방전 용량이 **0.1~0.26 % 낮게** 나오고,
    200 사이클 내내 그랬다 (평균 0.18 %).

    계측기 자신의 엑셀은 그 전하를 담는다.  레지스터의 마지막 값이 그 표와
    5e-6 mAh 안에서 일치했다.
    """
    from synthetic import build_wrd

    # (총스텝, 상태, CHARGE Q, DISCHARGE Q) — mAh
    spec = [
        # 충전 스텝: 레지스터가 0 에서 시작해 5.0 까지.  첫 행이 이미 0.02 다.
        (1, 3, 0.02, 0.0), (1, 3, 2.0, 0.0), (1, 3, 5.0, 0.0),
        # 휴지: CHARGE Q 는 **값을 붙들고 있다** (0 으로 안 돌아간다).
        (2, 1, 5.0, 0.0),
        # 방전 스텝: DISCHARGE Q 가 0 에서 시작하지만 첫 행이 이미 0.03 이다.
        (3, 4, 5.0, 0.03), (3, 4, 5.0, 2.0), (3, 4, 5.0, 4.8),
    ]
    rows = [_row(total_step=t, cell_status=st, charge_q=c, discharge_q=d, index=i)
            for i, (t, st, c, d) in enumerate(spec)]

    steps = segment_steps(read_wrd_bytes(build_wrd(rows)))
    charge = next(s for s in steps if s.mode == "charge")
    discharge = next(s for s in steps if s.mode == "discharge")

    # 첫 행의 0.03 을 빼면 4.77 이 된다.  그것이 이 버그였다.
    assert discharge.capacity_mah == pytest.approx(4.8)
    assert charge.capacity_mah == pytest.approx(5.0)


def test_a_step_that_continues_the_one_before_it_still_takes_the_difference():
    """이어지는 스텝(CC 다음의 CV)은 **차분**이어야 한다 — 옛 동작을 지킨다.

    레지스터가 이 스텝에서 다시 시작했는지는 첫 행이 앞 행보다 **낮은가**로
    가른다.  낮으면 다시 시작한 것이라 마지막 값이 통째로 이 스텝의 것이고,
    같거나 높으면 앞 스텝을 이어받은 것이라 그만큼 뺀다.
    """
    from synthetic import build_wrd

    spec = [
        (1, 3, 0.02), (1, 3, 3.0),             # CC 다리
        (2, 3, 3.4), (2, 3, 4.0),              # CV 다리 — 3.0 을 이어받는다
    ]
    rows = [_row(total_step=t, cell_status=st, charge_q=c, discharge_q=0.0, index=i)
            for i, (t, st, c) in enumerate(spec)]

    steps = segment_steps(read_wrd_bytes(build_wrd(rows)))
    cc, cv = [s for s in steps if s.mode == "charge"][:2]
    assert cc.capacity_mah == pytest.approx(3.0)
    # 4.0 - 3.0.  여기서 4.0 을 통째로 담으면 사이클 용량이 두 배 가까이 된다.
    assert cv.capacity_mah == pytest.approx(1.0)
