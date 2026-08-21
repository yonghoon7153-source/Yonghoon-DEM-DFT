"""Checks that only run against a real instrument file.

    WRDKIT_SAMPLE=/path/to/file.wrd pytest

These assert on physics rather than on exact values, so they hold for any
WBCS3000 cycling file, not just the one used to reverse-engineer the format.
"""

import numpy as np
import pytest

from wrdkit import (
    CellStatus,
    differential_capacity,
    extract_profile,
    summarize_cycles,
)
from wrdkit.health import build_report


def test_the_whole_file_is_consumed(sample_wrd):
    assert sample_wrd.metadata.trailing_bytes == 0
    assert len(sample_wrd) > 0


def test_cell_status_agrees_with_the_current_sign(sample_wrd):
    status = sample_wrd["cell_status"]
    current = sample_wrd["current"]
    assert np.all(current[status == CellStatus.CHARGE] > 0)
    assert np.all(current[status == CellStatus.DISCHARGE] < 0)
    assert np.all(current[status == CellStatus.REST] == 0)


def test_reported_capacity_matches_the_current_integral(sample_wrd):
    """Coulomb counting is computed independently of the reported column."""
    cycles = [c for c in summarize_cycles(sample_wrd) if c.complete]
    if len(cycles) < 3:
        pytest.skip("file has fewer than three complete cycles")
    cycle = cycles[len(cycles) // 2]
    seconds = sample_wrd.seconds("test_time")[cycle.start:cycle.stop]
    current = sample_wrd["current"][cycle.start:cycle.stop]
    discharging = current < 0
    integrated = np.trapezoid(-current[discharging], seconds[discharging]) / 3.6
    assert integrated == pytest.approx(cycle.discharge_capacity_mah, rel=0.02)


def test_time_advances_monotonically(sample_wrd):
    seconds = sample_wrd.seconds("test_time")
    assert np.all(np.diff(seconds) >= 0)


def test_schedule_cutoffs_bracket_the_measured_voltage(sample_wrd):
    schedule = sample_wrd.metadata.schedule
    if not schedule or schedule.upper_cutoff_v is None:
        pytest.skip("file carries no voltage cut-offs")
    voltage = sample_wrd["voltage"]
    assert voltage.max() <= schedule.upper_cutoff_v + 0.05
    assert voltage.min() >= schedule.lower_cutoff_v - 0.05


def test_profiles_span_the_cycle_capacity(sample_wrd):
    cycles = [c for c in summarize_cycles(sample_wrd) if c.complete]
    if not cycles:
        pytest.skip("no complete cycle")
    cycle = cycles[len(cycles) // 2]
    profile = extract_profile(sample_wrd, cycle, "discharge")
    assert profile.capacity_mah[0] == pytest.approx(0.0, abs=1e-9)
    assert profile.capacity_mah[-1] == pytest.approx(cycle.discharge_capacity_mah)


def test_a_report_can_be_built(sample_wrd):
    schedule = sample_wrd.metadata.schedule
    report = build_report(
        summarize_cycles(sample_wrd),
        planned_cycles=schedule.planned_cycles if schedule else None,
    )
    assert report.state in ("running", "finished", "unknown")
    assert report.state_summary


def test_dqdv_integrates_back_to_the_branch_capacity(sample_wrd):
    """dQ/dV 를 전압으로 다시 적분하면 그 브랜치의 용량이 나와야 한다.

    이 분석이 물리를 지키는지 확인하는 가장 직접적인 방법이고, 격자·보간·평활
    어느 하나가 틀리면 여기서 어긋난다.

    방전만 본다.  충전은 정전압 구간을 일부러 빼므로(ADR 0013) 적분이 그
    용량만큼 모자라는 것이 정상이고, 그 모자람은 셀이 늙을수록 커진다 — 실측
    161 사이클 셀에서 0.7 % → 2.6 % 로 자랐다.  "오차" 가 아니라 CV 용량이다.

    부호도 함께 본다.  방전은 전압이 내려가면서 용량이 오르므로 음수여야 하고,
    그 부호가 충전·방전을 한 그래프에 겹칠 수 있게 하는 것이다.
    """
    cycles = [c for c in summarize_cycles(sample_wrd) if c.complete]
    if len(cycles) < 3:
        pytest.skip("file has fewer than three complete cycles")

    cycle = cycles[len(cycles) // 2]
    profile = extract_profile(sample_wrd, cycle, "discharge")
    result = differential_capacity(profile)
    if not result.usable:
        pytest.skip(f"discharge branch unusable: {result.reason}")

    integrated = np.trapezoid(result.dq_dv, result.voltage)
    assert integrated < 0, "방전 dQ/dV 가 음수가 아니다"
    assert abs(integrated) == pytest.approx(cycle.discharge_capacity_mah, rel=0.03)


def test_dqdv_drops_the_constant_voltage_hold(sample_wrd):
    """충전 끝의 CV 구간은 dV=0 이라 빼야 한다.

    안 빼면 컷오프 전압 자리에 0 으로 나눈 봉우리가 하나 서는데, 하필 그 자리가
    사람들이 상전이를 찾는 곳이다.
    """
    cycles = [c for c in summarize_cycles(sample_wrd) if c.complete]
    if len(cycles) < 3:
        pytest.skip("file has fewer than three complete cycles")

    cycle = cycles[len(cycles) // 2]
    profile = extract_profile(sample_wrd, cycle, "charge")
    result = differential_capacity(profile)
    if not result.usable:
        pytest.skip(f"charge branch unusable: {result.reason}")

    # 스케줄에 CV 가 없는 파일도 있으므로 개수를 못 박지 않는다.  못 박는 것은,
    # 뺀 만큼 적분이 모자라되 그 이상 어긋나지는 않는다는 것이다.
    integrated = np.trapezoid(result.dq_dv, result.voltage)
    assert integrated > 0, "충전 dQ/dV 가 양수가 아니다"
    assert integrated <= cycle.charge_capacity_mah * 1.01, "CV 구간이 들어갔다"
    assert integrated >= cycle.charge_capacity_mah * 0.85, "너무 많이 뺐다"
