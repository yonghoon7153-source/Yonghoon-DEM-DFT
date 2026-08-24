"""dV/dQ — dQ/dV 와 같은 방식으로, 답을 아는 곡선으로만 검증한다.

이 분석의 존재 이유는 **봉우리 사이 간격이 곧 용량**이라는 것이다. 그래서
검사의 중심도 거기에 둔다: 알려진 위치에 스테이지 경계 두 개를 심고, 되찾은
간격이 심은 값과 같은지 본다. 봉우리 높이만 보는 검사는 이 분석이 실제로 쓰이는
방식(전극 슬리피지 읽기)을 전혀 지키지 못한다.

dQ/dV 와 서로 역수라는 것도 여기서 고정한다. 한쪽만 고치고 다른 쪽을 잊으면
두 화면이 조용히 어긋나는데, 둘을 나란히 놓고 보는 것이 이 기능의 목적이다.
"""

from __future__ import annotations

import numpy as np
import pytest

from wrdkit.cycles import Profile
from wrdkit.dva import (
    MIN_SPAN_MAH,
    advancing_mask,
    differential_voltage,
    differential_voltages,
)
from wrdkit.ica import MIN_SAMPLES, differential_capacity


def _profile(capacity, voltage, *, branch="charge", cycle=3) -> Profile:
    capacity = np.asarray(capacity, dtype=np.float64)
    voltage = np.asarray(voltage, dtype=np.float64)
    empty = np.zeros(len(capacity))
    return Profile(cycle, branch, capacity, voltage, empty, empty)


def _stage(q, at, height, sharpness=0.01):
    """전압에 계단 하나 — 스테이지 경계 하나의 이상화."""
    return height / (1.0 + np.exp(-(q - at) / sharpness))


# --- 해석적으로 답이 있는 경우 -----------------------------------------------

def test_a_straight_line_differentiates_to_its_slope():
    q = np.linspace(0.0, 2.0, 500)
    result = differential_voltage(_profile(q, 3.0 + 0.5 * q))
    assert result.usable
    assert np.abs(result.dv_dq - 0.5).max() < 1e-9


def test_it_is_the_reciprocal_of_dqdv():
    """같은 직선 위에서 dV/dQ · dQ/dV = 1. 두 화면이 어긋나면 여기서 걸린다."""
    q = np.linspace(0.0, 2.0, 500)
    voltage = 3.0 + 0.5 * q
    dvdq = differential_voltage(_profile(q, voltage))
    dqdv = differential_capacity(_profile(q, voltage))
    assert dvdq.dv_dq.mean() * dqdv.dq_dv.mean() == pytest.approx(1.0, rel=1e-6)


def test_the_gap_between_two_peaks_is_the_capacity_between_them():
    """이 분석이 존재하는 이유. 심은 간격을 그대로 되찾아야 한다."""
    q = np.linspace(0.0, 2.0, 4000)
    voltage = 3.0 + 0.15 * q + _stage(q, 0.4, 0.06) + _stage(q, 1.2, 0.06)
    result = differential_voltage(_profile(q, voltage), smoothing=9,
                                  smoother="savgol", poly_order=2)
    y = result.dv_dq
    peaks = [i for i in range(1, len(y) - 1)
             if y[i] > y[i - 1] and y[i] >= y[i + 1] and y[i] > 2 * y.mean()]
    assert len(peaks) == 2
    found = [float(result.capacity[i]) for i in peaks]
    assert found[0] == pytest.approx(0.4, abs=0.02)
    assert found[1] == pytest.approx(1.2, abs=0.02)
    assert found[1] - found[0] == pytest.approx(0.8, abs=0.02)


def test_a_plateau_is_a_valley_not_a_peak():
    """dQ/dV 와 반대다. 평탄부에서 dV/dQ 는 최소가 된다."""
    q = np.linspace(0.0, 2.0, 2000)
    voltage = 3.0 + 0.02 * q + _stage(q, 1.0, 0.4, sharpness=0.15)
    result = differential_voltage(_profile(q, voltage), smoothing=9)
    # 계단 한가운데가 최대, 양 끝(평탄부)이 최소여야 한다.
    peak_at = float(result.capacity[int(np.argmax(result.dv_dq))])
    assert peak_at == pytest.approx(1.0, abs=0.05)
    assert result.dv_dq[0] < result.dv_dq.max() / 4


# --- 부호는 답이다 -----------------------------------------------------------

def test_a_discharge_is_negative_and_that_is_the_answer():
    """방전은 용량이 오르는 동안 전압이 내려간다 — 음수가 측정값이다.

    여기서 abs 를 취하면 충전과 방전을 한 화면에 겹쳤을 때 이력(hysteresis)이
    사라진다. 그 이력을 보려고 겹치는 것이다.
    """
    q = np.linspace(0.0, 2.0, 500)
    result = differential_voltage(_profile(q, 4.2 - 0.5 * q, branch="discharge"))
    assert result.usable
    assert (result.dv_dq < 0).all()
    assert result.dv_dq.mean() == pytest.approx(-0.5, abs=1e-6)


def test_a_charge_is_positive():
    q = np.linspace(0.0, 2.0, 500)
    result = differential_voltage(_profile(q, 3.0 + 0.5 * q))
    assert (result.dv_dq > 0).all()


# --- 분모가 0 이 되는 곳을 빼는가 --------------------------------------------

def test_a_constant_voltage_hold_is_dropped_not_divided_by():
    """CV 홀드에서는 용량이 멈추고 전압만 움직인다 — dQ = 0 인 자리다.

    dQ/dV 는 평탄부에서 분모가 무너지고, dV/dQ 는 바로 이 자리에서 무너진다.
    빼지 않으면 무한대가 곡선에 들어간다.
    """
    moving = np.linspace(0.0, 1.0, 300)
    q = np.concatenate([moving, np.full(120, 1.0)])
    voltage = np.concatenate([3.0 + 0.5 * moving, np.linspace(3.5, 3.52, 120)])
    result = differential_voltage(_profile(q, voltage))
    assert result.usable
    assert result.points_dropped == 120
    assert np.isfinite(result.dv_dq).all()
    assert result.dv_dq.mean() == pytest.approx(0.5, abs=1e-6)


def test_a_rest_is_dropped_too():
    """휴지 구간도 용량이 멈춘다. CV 와 같은 이유로 같은 처리를 받는다."""
    moving = np.linspace(0.0, 1.0, 200)
    q = np.concatenate([moving[:100], np.full(50, moving[99]), moving[100:]])
    voltage = np.concatenate([3.0 + 0.5 * moving[:100],
                              np.full(50, 3.05), 3.0 + 0.5 * moving[100:]])
    result = differential_voltage(_profile(q, voltage))
    assert result.points_dropped == 50
    assert np.isfinite(result.dv_dq).all()


def test_a_nan_does_not_spread_through_the_curve():
    q = np.linspace(0.0, 2.0, 500)
    voltage = 3.0 + 0.5 * q
    voltage[250] = np.nan
    result = differential_voltage(_profile(q, voltage))
    assert result.usable
    assert np.isfinite(result.dv_dq).all()


# --- 격자 ---------------------------------------------------------------------

def test_the_grid_is_relative_so_cells_of_any_size_get_the_same_resolution():
    """0.3 mAh 버튼셀과 3000 mAh 파우치가 같은 점 수를 받아야 한다.

    고정 mAh 격자였다면 한쪽은 네 점, 다른 쪽은 육만 점이 된다.
    """
    small = differential_voltage(
        _profile(np.linspace(0, 0.3, 900), 3.0 + np.linspace(0, 0.3, 900)))
    large = differential_voltage(
        _profile(np.linspace(0, 3000, 900), 3.0 + np.linspace(0, 3000, 900) / 1e4))
    assert abs(len(small) - len(large)) <= 1


def test_an_explicit_step_wins_over_the_fraction():
    """사이클을 겹쳐 볼 때는 고정 mAh 격자라야 x 축이 맞는다."""
    q = np.linspace(0.0, 2.0, 900)
    result = differential_voltage(_profile(q, 3.0 + 0.5 * q), capacity_step=0.01)
    assert result.capacity_step == pytest.approx(0.01)
    assert np.diff(result.capacity).max() == pytest.approx(0.01, rel=1e-9)


def test_a_finer_grid_resolves_two_close_boundaries():
    q = np.linspace(0.0, 2.0, 8000)
    voltage = (3.0 + 0.1 * q + _stage(q, 0.90, 0.05, 0.004)
               + _stage(q, 1.00, 0.05, 0.004))
    coarse = differential_voltage(_profile(q, voltage), capacity_step=0.05,
                                  smoothing=1)
    fine = differential_voltage(_profile(q, voltage), capacity_step=0.002,
                                smoothing=1)

    def peaks(result):
        y = result.dv_dq
        return sum(1 for i in range(1, len(y) - 1)
                   if y[i] > y[i - 1] and y[i] >= y[i + 1] and y[i] > 2 * y.mean())

    assert peaks(fine) == 2
    assert peaks(coarse) < 2


# --- 모르면 이유를 적고 비운다 ------------------------------------------------

def test_too_few_samples_says_so_instead_of_guessing():
    result = differential_voltage(_profile(np.arange(5.0), np.arange(5.0)))
    assert not result.usable
    assert str(MIN_SAMPLES) in result.reason


def test_a_branch_that_never_advances_says_so():
    result = differential_voltage(_profile(np.zeros(50), np.linspace(3, 4, 50)))
    assert not result.usable
    assert "advance" in result.reason
    assert result.points_dropped == 49


def test_an_empty_branch_does_not_raise():
    result = differential_voltage(_profile(np.empty(0), np.empty(0)))
    assert not result.usable
    assert result.reason


def test_a_bad_step_is_refused_not_divided_by():
    q = np.linspace(0.0, 2.0, 500)
    result = differential_voltage(_profile(q, 3.0 + 0.5 * q), capacity_step=0.0)
    assert not result.usable
    assert "positive" in result.reason


def test_an_unknown_smoother_is_refused_by_name_not_ignored():
    """조용히 기본값으로 되돌아가면 화면은 SG 라고 적고 이동평균을 그린다."""
    q = np.linspace(0.0, 2.0, 500)
    result = differential_voltage(_profile(q, 3.0 + 0.5 * q), smoother="gaussian")
    assert not result.usable
    assert "gaussian" in result.reason


def test_a_span_below_the_floor_says_so():
    q = np.linspace(0.0, MIN_SPAN_MAH / 10, 50)
    result = differential_voltage(_profile(q, 3.0 + q))
    assert not result.usable
    assert "differentiate" in result.reason


# --- 결과가 자기 설정을 말하는가 ----------------------------------------------

def test_the_curve_says_what_it_was_made_with():
    """평활은 봉우리를 낮춘다. 무엇으로 만든 곡선인지 화면과 CSV 가 말할 수
    있어야 두 곡선의 높이를 비교해도 되는지 판단할 수 있다."""
    q = np.linspace(0.0, 2.0, 900)
    result = differential_voltage(_profile(q, 3.0 + 0.5 * q), smoothing=11,
                                  smoother="savgol", poly_order=3,
                                  capacity_step=0.004)
    assert result.smoothing == 11
    assert result.smoother == "savgol"
    assert result.poly_order == 3
    assert result.capacity_step == pytest.approx(0.004)
    assert result.branch == "charge"
    assert result.cycle_number == 3


def test_many_branches_keep_their_unusable_ones():
    """빼 버리면 화면에서 그 사이클이 왜 없는지 알 방법이 없다."""
    q = np.linspace(0.0, 2.0, 500)
    good = _profile(q, 3.0 + 0.5 * q, cycle=1)
    bad = _profile(np.arange(4.0), np.arange(4.0), cycle=2)
    results = differential_voltages([good, bad])
    assert len(results) == 2
    assert results[0].usable
    assert not results[1].usable
    assert results[1].reason


# --- advancing_mask 자체 ------------------------------------------------------

def test_advancing_mask_keeps_the_first_of_a_flat_run():
    mask = advancing_mask(np.array([0.0, 1.0, 1.0, 1.0, 2.0]))
    assert list(mask) == [True, True, False, False, True]


def test_advancing_mask_does_not_care_about_the_branch():
    """용량은 방전에서도 올라간다. 방향을 셀 필요가 없다."""
    rising = np.array([0.0, 0.5, 0.5, 1.0])
    assert list(advancing_mask(rising)) == [True, True, False, True]


def test_advancing_mask_on_nothing():
    assert len(advancing_mask(np.empty(0))) == 0


# --- CSV ----------------------------------------------------------------------

def test_the_csv_lays_curves_out_like_the_dqdv_csv():
    """dQ/dV 옆에 놓고 읽는 표다. 레이아웃이 다르면 그때마다 다시 익혀야 한다."""
    from wrdkit import Basis, CellSpec
    from wrdkit.export import dvdq_csv_string

    q = np.linspace(0.0, 2.0, 500)
    curves = [
        differential_voltage(_profile(q, 3.0 + 0.5 * q, cycle=3)),
        differential_voltage(_profile(q, 4.2 - 0.5 * q, branch="discharge",
                                      cycle=3)),
    ]
    cell = CellSpec(total_mass_mg=20.0, active_wt_percent=80).resolve()
    header = dvdq_csv_string(curves, cell, basis=Basis.SPECIFIC).splitlines()[0]

    assert header.split(",") == [
        "cycle3_charge_capacity (mAh/g)", "cycle3_charge_dVdQ (V/(mAh/g))",
        "cycle3_discharge_capacity (mAh/g)", "cycle3_discharge_dVdQ (V/(mAh/g))",
    ]


def test_the_csv_normalises_the_denominator_the_right_way_round():
    """0.5 V/mAh 짜리 곡선을 활물질 16 mg 으로 정규화하면 0.008 V/(mAh/g) 다.

    거꾸로 나누면 31.25 가 나오는데, 그것도 그럴듯한 숫자라 화면에서는 안 걸린다.
    """
    from wrdkit import Basis, CellSpec
    from wrdkit.export import dvdq_csv_string

    q = np.linspace(0.0, 2.0, 500)
    curve = differential_voltage(_profile(q, 3.0 + 0.5 * q, cycle=1))
    cell = CellSpec(total_mass_mg=20.0, active_wt_percent=80).resolve()
    assert cell.divisor(Basis.SPECIFIC) == pytest.approx(0.016)

    rows = dvdq_csv_string([curve], cell, basis=Basis.SPECIFIC).splitlines()
    value = float(rows[5].split(",")[1])
    assert value == pytest.approx(0.5 * 0.016, rel=1e-6)


def test_the_csv_falls_back_to_raw_units_rather_than_refusing():
    from wrdkit import Basis, CellSpec
    from wrdkit.export import dvdq_csv_string

    q = np.linspace(0.0, 2.0, 500)
    curve = differential_voltage(_profile(q, 3.0 + 0.5 * q, cycle=1))
    header = dvdq_csv_string([curve], CellSpec().resolve(),
                             basis=Basis.SPECIFIC).splitlines()[0]
    assert header.split(",") == ["cycle1_charge_capacity (mAh)",
                                 "cycle1_charge_dVdQ (V/mAh)"]


def test_an_unusable_curve_still_takes_its_two_columns():
    """빼 버리면 열을 세어 사이클과 맞추는 사람이 행을 밀려 읽는다."""
    from wrdkit import CellSpec
    from wrdkit.export import dvdq_csv_string

    q = np.linspace(0.0, 2.0, 500)
    good = differential_voltage(_profile(q, 3.0 + 0.5 * q, cycle=1))
    bad = differential_voltage(_profile(np.arange(4.0), np.arange(4.0), cycle=2))
    header = dvdq_csv_string([good, bad], CellSpec().resolve()).splitlines()[0]
    assert len(header.split(",")) == 4


def test_no_curves_still_writes_a_header():
    from wrdkit import CellSpec
    from wrdkit.export import dvdq_csv_string

    assert dvdq_csv_string([], CellSpec().resolve()).splitlines()[0] == "capacity,dVdQ"
