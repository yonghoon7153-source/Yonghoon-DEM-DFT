"""dQ/dV — 답을 아는 곡선으로만 검증한다.

실측 파일에 맞추면 "우리 구현이 우리 구현과 같다" 밖에 확인하지 못한다.
여기 쓰는 곡선들은 해석적으로 미분값이 알려져 있어서, 틀리면 틀렸다고 말할 수
있다.

로지스틱 Q(V) = A / (1 + exp(-(V - V0)/s)) 의 미분은 V0 에서 최대이고 그
높이가 정확히 A/(4s) 다. 상전이 하나짜리 평탄부의 이상화이고, dQ/dV 가 실제로
하는 일(평탄부 → 봉우리)을 그대로 담는다.
"""

from __future__ import annotations

import numpy as np
import pytest

from wrdkit.cycles import Profile
from wrdkit.ica import (
    MIN_SAMPLES,
    DifferentialCapacity,
    differential_capacities,
    differential_capacity,
    monotonic_mask,
)


def _profile(voltage, capacity, *, branch="charge", cycle=3) -> Profile:
    voltage = np.asarray(voltage, dtype=np.float64)
    capacity = np.asarray(capacity, dtype=np.float64)
    empty = np.zeros(len(voltage))
    return Profile(cycle, branch, capacity, voltage, empty, empty)


def _logistic(voltage, *, amplitude=1.0, centre=3.8, width=0.05):
    return amplitude / (1.0 + np.exp(-(voltage - centre) / width))


def _peak_voltage(result: DifferentialCapacity) -> float:
    return float(result.voltage[int(np.argmax(result.dq_dv))])


# --- 아는 답 ----------------------------------------------------------------

def test_a_straight_line_differentiates_to_its_slope():
    """Q 가 V 에 선형이면 dQ/dV 는 그 기울기 하나다.

    가장 단순한 참값이고, 평활·격자·가장자리 처리가 값을 흔들지 않는지를
    한 번에 본다 — 이동평균은 상수를 상수로 남겨야 한다.
    """
    voltage = np.linspace(3.0, 4.2, 400)
    result = differential_capacity(_profile(voltage, 2.5 * voltage))

    assert result.usable
    assert np.allclose(result.dq_dv, 2.5, atol=1e-6)


def test_a_plateau_becomes_a_peak_where_it_is():
    """로지스틱의 봉우리는 V0 에, 높이는 A/(4s) 에 있다."""
    voltage = np.linspace(3.2, 4.4, 1200)
    result = differential_capacity(
        _profile(voltage, _logistic(voltage, amplitude=2.0, centre=3.85, width=0.04)))

    assert result.usable
    # 격자 한 칸(5 mV) 안에서 맞아야 한다.
    assert _peak_voltage(result) == pytest.approx(3.85, abs=result.voltage_step)
    # 평활이 봉우리를 낮추므로 정확히는 아니지만 몇 % 안이어야 한다.
    assert result.dq_dv.max() == pytest.approx(2.0 / (4 * 0.04), rel=0.05)


def test_two_plateaus_become_two_peaks():
    voltage = np.linspace(3.0, 4.4, 1400)
    capacity = (_logistic(voltage, amplitude=1.0, centre=3.5, width=0.03)
                + _logistic(voltage, amplitude=1.5, centre=4.1, width=0.03))
    result = differential_capacity(_profile(voltage, capacity))

    # 국소 최대 두 개를 찾는다.
    values = result.dq_dv
    peaks = [i for i in range(1, len(values) - 1)
             if values[i] > values[i - 1] and values[i] >= values[i + 1]
             and values[i] > 0.2 * values.max()]
    found = sorted(float(result.voltage[i]) for i in peaks)
    assert len(found) == 2, found
    assert found[0] == pytest.approx(3.5, abs=0.02)
    assert found[1] == pytest.approx(4.1, abs=0.02)


def test_the_answer_is_in_mah_per_volt_so_it_scales_with_capacity():
    """정규화는 부르는 쪽 몫이다 (ADR 0001).  여기서 나오는 것은 raw 다."""
    voltage = np.linspace(3.0, 4.2, 400)
    single = differential_capacity(_profile(voltage, 2.5 * voltage))
    double = differential_capacity(_profile(voltage, 5.0 * voltage))

    assert np.allclose(double.dq_dv, 2 * single.dq_dv, atol=1e-6)


def test_a_discharge_is_negative_and_that_is_the_answer():
    """방전은 전압이 내려가면서 용량이 오르므로 dQ/dV 가 음수다.

    부호를 지우면(abs) 충전과 방전을 한 그래프에 겹쳐도 히스테리시스가 보이지
    않는다 — 위로 선 봉우리와 아래로 선 봉우리 사이의 간격이 보려던 것이다.
    실측 셀에서도 방전 곡선을 전압으로 적분하면 브랜치 용량의 음수가 나온다.
    """
    voltage = np.linspace(4.4, 3.2, 1200)
    capacity = np.linspace(0, 2.0, 1200)      # 전압이 내려가는 동안 용량은 오른다
    result = differential_capacity(_profile(voltage, capacity, branch="discharge"))

    assert result.usable
    assert np.all(result.dq_dv < 0), "방전 dQ/dV 가 음수가 아니다"
    # 다시 적분하면 브랜치 용량의 음수. (격자가 오름차순이므로 dV > 0)
    assert np.trapezoid(result.dq_dv, result.voltage) == pytest.approx(-2.0, rel=0.02)


def test_a_charge_is_positive():
    voltage = np.linspace(3.2, 4.4, 1200)
    result = differential_capacity(_profile(voltage, np.linspace(0, 2.0, 1200)))
    assert np.all(result.dq_dv > 0)
    assert np.trapezoid(result.dq_dv, result.voltage) == pytest.approx(2.0, rel=0.02)


def test_a_discharge_reads_left_to_right_in_volts_too():
    """방전은 전압이 내려간다.  격자는 그래도 오름차순이어야 한다.

    아니면 화면에서 충전 곡선과 방전 곡선의 x 축이 서로 뒤집혀 있고, 둘을
    겹쳐 보는 것이 dQ/dV 를 보는 이유의 절반이다.
    """
    voltage = np.linspace(4.4, 3.2, 1200)   # 내려간다
    capacity = _logistic(voltage, amplitude=2.0, centre=3.85, width=0.04)
    result = differential_capacity(_profile(voltage, capacity, branch="discharge"))

    assert result.usable
    assert np.all(np.diff(result.voltage) > 0), "격자가 오름차순이 아니다"
    assert _peak_voltage(result) == pytest.approx(3.85, abs=result.voltage_step)


# --- 빼야 하는 것들 ----------------------------------------------------------

def test_the_cv_hold_is_dropped_not_divided_by():
    """정전압 구간은 dV=0 이고 dQ 는 0 이 아니다.

    안 빼면 마지막 격자점에 실제 열화보다 큰 봉우리가 하나 서고, 그것은
    상전이가 아니라 0 으로 나눈 결과다.
    """
    cc = np.linspace(3.2, 4.3, 600)
    cv = np.full(300, 4.3)                     # 전압 고정, 용량은 계속 오른다
    voltage = np.concatenate([cc, cv])
    capacity = np.concatenate([_logistic(cc, amplitude=2.0, centre=3.85, width=0.04),
                               np.linspace(2.0, 2.4, 300)])

    result = differential_capacity(_profile(voltage, capacity))

    assert result.points_dropped == 300
    assert result.usable
    # 봉우리는 여전히 상전이 자리에 하나뿐이다.
    assert _peak_voltage(result) == pytest.approx(3.85, abs=result.voltage_step)
    assert result.dq_dv.max() == pytest.approx(2.0 / (4 * 0.04), rel=0.05)


def test_noise_that_walks_backwards_is_dropped():
    """느린 전류에서 전압은 계속 조금씩 되돌아간다.

    그 표본들의 ΔV 는 부호가 반대라, 남겨 두면 격자 보간이 흔들린다.
    """
    rng = np.random.default_rng(0)
    clean = np.linspace(3.2, 4.3, 800)
    voltage = clean + rng.normal(0, 0.002, clean.size)
    capacity = 2.0 * (clean - clean[0]) / (clean[-1] - clean[0])

    result = differential_capacity(_profile(voltage, capacity))

    assert result.points_dropped > 0
    assert result.usable
    # 되돌아감을 걸러 냈으므로 기울기가 참값 근처에 머문다.
    expected = 2.0 / (clean[-1] - clean[0])
    assert result.dq_dv.mean() == pytest.approx(expected, rel=0.1)


def test_a_nan_does_not_spread_through_the_curve():
    """NaN 하나가 보간을 타고 평활 창 너비만큼 번진다."""
    voltage = np.linspace(3.0, 4.2, 400)
    capacity = 2.5 * voltage
    capacity[100] = np.nan

    result = differential_capacity(_profile(voltage, capacity))

    assert result.usable
    assert np.all(np.isfinite(result.dq_dv))


# --- 못 하겠으면 못 하겠다고 -------------------------------------------------

def test_too_few_samples_says_so_instead_of_guessing():
    voltage = np.linspace(3.0, 4.2, 5)
    result = differential_capacity(_profile(voltage, 2.5 * voltage))

    assert not result.usable
    assert str(MIN_SAMPLES) in result.reason


def test_a_branch_that_barely_moves_says_so():
    """3.999-4.000 V 짜리 구간에서는 모든 봉우리가 평활 창이다."""
    voltage = np.linspace(3.999, 4.0, 200)
    result = differential_capacity(_profile(voltage, np.linspace(0, 1, 200)))

    assert not result.usable
    assert "V" in result.reason


def test_a_branch_that_never_moves_says_so():
    """휴지 구간만 잡힌 경우.  전부 같은 전압이라 단조 표본이 하나뿐이다."""
    voltage = np.full(200, 4.0)
    result = differential_capacity(_profile(voltage, np.linspace(0, 1, 200)))

    assert not result.usable
    assert result.points_used == 1
    assert "move in voltage" in result.reason


def test_an_empty_branch_does_not_raise():
    """열 사이클 중 하나가 비어도 나머지 아홉은 화면에 남아야 한다."""
    result = differential_capacity(_profile([], []))
    assert not result.usable
    assert result.reason


def test_a_bad_voltage_step_is_refused_not_divided_by():
    voltage = np.linspace(3.0, 4.2, 400)
    result = differential_capacity(_profile(voltage, 2.5 * voltage), voltage_step=0)
    assert not result.usable
    assert "positive" in result.reason


# --- 설정이 결과를 바꾸므로 함께 돌려준다 -------------------------------------

def test_the_curve_says_what_it_was_made_with():
    """평활은 봉우리를 낮춘다.  같은 격자·같은 창일 때만 높이를 비교할 수 있다."""
    voltage = np.linspace(3.2, 4.4, 1200)
    capacity = _logistic(voltage, amplitude=2.0, centre=3.85, width=0.04)

    sharp = differential_capacity(_profile(voltage, capacity), smoothing=1)
    blunt = differential_capacity(_profile(voltage, capacity), smoothing=41)

    assert (sharp.voltage_step, sharp.smoothing) == (0.005, 1)
    assert blunt.smoothing == 41
    assert blunt.dq_dv.max() < sharp.dq_dv.max(), "평활이 봉우리를 낮추지 않았다"


def test_an_even_smoothing_window_does_not_shift_the_peak():
    """짝수 창은 결과를 반 칸 민다.  답이 봉우리 위치인 분석에서는 공짜가 아니다."""
    voltage = np.linspace(3.2, 4.4, 1200)
    capacity = _logistic(voltage, amplitude=2.0, centre=3.85, width=0.04)

    odd = differential_capacity(_profile(voltage, capacity), smoothing=7)
    even = differential_capacity(_profile(voltage, capacity), smoothing=8)

    assert _peak_voltage(even) == pytest.approx(_peak_voltage(odd), abs=1e-9)


def test_a_finer_grid_finds_a_sharper_peak():
    voltage = np.linspace(3.2, 4.4, 4000)
    capacity = _logistic(voltage, amplitude=2.0, centre=3.85, width=0.01)

    coarse = differential_capacity(_profile(voltage, capacity), voltage_step=0.02)
    fine = differential_capacity(_profile(voltage, capacity), voltage_step=0.001)

    assert fine.dq_dv.max() > coarse.dq_dv.max()
    assert _peak_voltage(fine) == pytest.approx(3.85, abs=0.002)


# --- 여러 개 ----------------------------------------------------------------

def test_many_branches_keep_their_unusable_ones():
    """쓸 수 없는 것을 조용히 빼면, 화면에서 그 사이클이 왜 없는지 알 수 없다."""
    good = np.linspace(3.0, 4.2, 400)
    results = differential_capacities([
        _profile(good, 2.5 * good, cycle=3),
        _profile(np.full(200, 4.0), np.linspace(0, 1, 200), cycle=4),
    ])

    assert [r.cycle_number for r in results] == [3, 4]
    assert [r.usable for r in results] == [True, False]
    assert results[1].reason


# --- 단조 필터 자체 ----------------------------------------------------------

def test_monotonic_mask_keeps_the_first_of_a_flat_run():
    """같은 전압이 이어지면 첫 표본만 남는다 — 보간이 요구하는 강한 단조성."""
    mask = monotonic_mask(np.array([3.0, 3.1, 3.1, 3.1, 3.2]), "charge")
    assert list(mask) == [True, True, False, False, True]


def test_monotonic_mask_follows_the_branch_direction():
    down = np.array([4.2, 4.1, 4.15, 4.0])
    assert list(monotonic_mask(down, "discharge")) == [True, True, False, True]
    # 같은 배열을 충전으로 보면 살아남는 것이 정반대다.
    assert list(monotonic_mask(down, "charge")) == [True, False, False, False]


# --- CSV --------------------------------------------------------------------

def test_the_csv_lays_curves_out_like_the_profile_csv():
    """용량 곡선과 그 미분을 같은 스프레드시트에서 비교하는 사람이, 두 번째
    레이아웃을 새로 익힐 이유가 없다."""
    from wrdkit import Basis, CellSpec, dqdv_csv_string

    voltage = np.linspace(3.0, 4.2, 400)
    curves = [
        differential_capacity(_profile(voltage, 2.5 * voltage, cycle=3)),
        differential_capacity(_profile(voltage[::-1], 2.0 * voltage[::-1],
                                       branch="discharge", cycle=3)),
    ]
    cell = CellSpec(total_mass_mg=20.0, active_wt_percent=80).resolve()
    header = dqdv_csv_string(curves, cell, basis=Basis.SPECIFIC).splitlines()[0]

    assert header.split(",") == [
        "cycle3_charge_voltage (V)", "cycle3_charge_dQdV (mAh/g/V)",
        "cycle3_discharge_voltage (V)", "cycle3_discharge_dQdV (mAh/g/V)",
    ]


def test_an_unusable_curve_still_takes_its_two_columns():
    """빼 버리면 열을 세어 사이클과 맞추는 사람이 51번 데이터를 30번 머리글
    아래에서 읽는다."""
    from wrdkit import CellSpec, dqdv_csv_string

    voltage = np.linspace(3.0, 4.2, 400)
    curves = [
        differential_capacity(_profile(voltage, 2.5 * voltage, cycle=3)),
        differential_capacity(_profile(np.full(200, 4.0), np.linspace(0, 1, 200),
                                       cycle=4)),
    ]
    lines = dqdv_csv_string(curves, CellSpec().resolve()).splitlines()

    assert lines[0].count("cycle4") == 2
    assert lines[1].split(",")[2:] == ["", ""]
