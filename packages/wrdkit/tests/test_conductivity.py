"""이온전도도와 활성화에너지 — 랩이 손으로 낸 수를 그대로 낼 수 있는가.

기준이 둘 있고 둘 다 랩에서 왔다.

1. **엑셀 계산기** (`이온전도도.xlsx`) -- ``= D4/(E4*F4)*1000`` 로 두께 0.085 cm,
   면적 0.7854 cm², 저항 10.93 Ω 에서 ``9.9016567452066084 mS/cm``.
2. **슬라이드의 표** (전해질 분석 2026.09, B12) -- 온도 아홉 점의 저항과
   이온전도도, 그리고 활성화에너지 ``0.328 eV``.

두 번째가 이 모듈이 있는 이유다: 그 표를 손으로 만드는 데 Origin 을 한 번
열어야 했다.
"""

from __future__ import annotations

import numpy as np
import pytest

from wrdkit.eis.conductivity import (
    BOLTZMANN_EV_PER_K,
    ConductivityPoint,
    activation_energy,
    conductivity_ms_cm,
    kelvin,
    real_axis_crossing,
)

#: 슬라이드 4쪽, B12 의 표.  온도(°C) · 저항(Ω) · 이온전도도(mS/cm).
LAB_TABLE = [
    (60, 9.69, 9.59), (50, 10.21, 9.10), (40, 14.56, 6.38),
    (30, 22.00, 4.22), (20, 34.66, 2.68), (10, 55.88, 1.66),
    (0, 94.30, 0.98), (-10, 171.0, 0.54), (-20, 300.0, 0.31),
]
#: 같은 표의 두께.  면적은 적혀 있지 않지만 세 열이 서로를 정해 준다 --
#: ``A = t/(sigma·R)`` 이 아홉 줄에서 같은 값(0.8501 cm²)으로 나온다.
LAB_THICKNESS_MM = 0.79
LAB_AREA_CM2 = 0.8501


def test_the_lab_spreadsheet_formula_to_every_digit_it_shows():
    got = conductivity_ms_cm(10.93, thickness_mm=0.85, area_cm2=0.7854)
    assert got == pytest.approx(9.9016567452066084, rel=1e-12)


def test_the_thickness_is_millimetres_and_only_converted_in_one_place():
    """10 배 틀릴 자리가 한 곳뿐임을 못박는다."""
    thin = conductivity_ms_cm(10.0, thickness_mm=1.0, area_cm2=1.0)
    thick = conductivity_ms_cm(10.0, thickness_mm=10.0, area_cm2=1.0)
    # 1 mm = 0.1 cm 이므로 0.1/(10·1)·1000 = 10 mS/cm.
    assert thin == pytest.approx(10.0)
    assert thick == pytest.approx(100.0)


def test_the_whole_table_comes_back_from_resistance_alone():
    """저항 아홉 개에서 슬라이드의 이온전도도 아홉 개가 나와야 한다."""
    for temperature_c, resistance, expected in LAB_TABLE:
        got = conductivity_ms_cm(resistance, thickness_mm=LAB_THICKNESS_MM,
                                 area_cm2=LAB_AREA_CM2)
        assert got == pytest.approx(expected, abs=0.006), temperature_c


def test_a_missing_or_impossible_input_gives_none_not_infinity():
    """0 이나 음수는 값이 아니라 '아직 안 적었다' 다 (§0.4).

    나누면 inf 가 나오고, inf 는 화면에서 아주 큰 전도도처럼 보인다.
    """
    assert conductivity_ms_cm(None, thickness_mm=0.8, area_cm2=1.0) is None
    assert conductivity_ms_cm(10.0, thickness_mm=None, area_cm2=1.0) is None
    assert conductivity_ms_cm(10.0, thickness_mm=0.8, area_cm2=None) is None
    assert conductivity_ms_cm(0.0, thickness_mm=0.8, area_cm2=1.0) is None
    assert conductivity_ms_cm(-5.0, thickness_mm=0.8, area_cm2=1.0) is None
    assert conductivity_ms_cm(10.0, thickness_mm=-0.8, area_cm2=1.0) is None
    assert conductivity_ms_cm(10.0, thickness_mm=0.8, area_cm2=0.0) is None


# --- 활성화에너지 -----------------------------------------------------------

def lab_columns():
    return ([row[0] for row in LAB_TABLE], [row[2] for row in LAB_TABLE])


def test_the_slides_activation_energy_comes_back():
    """0.328 eV -- 이 저장소가 이 모듈을 만든 이유."""
    temperatures, sigmas = lab_columns()
    got = activation_energy(temperatures, sigmas)
    assert got.activation_energy_ev is not None
    # 0.001 eV 안쪽 -- 우리가 가진 σ 가 표에서 읽은 소수 두 자리라서 그렇다.
    # Origin 이 맞춘 것은 반올림 전의 수이고, 그 차이가 0.00073 eV 다.
    assert got.activation_energy_ev == pytest.approx(0.328, abs=1e-3)
    assert got.points_used == 9
    assert got.basis == "sigma"
    assert got.reason == ""
    assert got.fit is not None and got.fit.r_squared == pytest.approx(0.993, abs=1e-3)


def test_the_basis_is_always_said_because_the_two_answers_differ():
    """``ln sigma`` 와 ``ln(sigma·T)`` 는 같은 점에서 다른 수를 낸다.

    0.33 과 0.35 는 표에 나란히 놓이면 다른 물질처럼 보인다.  어느 쪽을 맞춘
    수인지 안 적힌 활성화에너지는 비교할 수 없다.
    """
    temperatures, sigmas = lab_columns()
    plain = activation_energy(temperatures, sigmas, basis="sigma")
    with_t = activation_energy(temperatures, sigmas, basis="sigma_t")
    assert plain.activation_energy_ev == pytest.approx(0.3287, abs=5e-4)
    assert with_t.activation_energy_ev == pytest.approx(0.3537, abs=5e-4)
    assert plain.basis == "sigma" and with_t.basis == "sigma_t"


def test_the_unit_of_sigma_does_not_move_the_activation_energy():
    """mS/cm 든 S/cm 든 기울기는 같다 -- 단위는 절편만 옮긴다.

    이것이 성립하지 않으면 어딘가에서 로그 밖에 단위 환산이 끼어든 것이다.
    """
    temperatures, sigmas = lab_columns()
    one = activation_energy(temperatures, sigmas)
    thousand = activation_energy(temperatures, [s * 1000 for s in sigmas])
    assert one.activation_energy_ev == pytest.approx(
        thousand.activation_energy_ev, rel=1e-12)
    assert one.fit is not None and thousand.fit is not None
    assert thousand.fit.intercept - one.fit.intercept == pytest.approx(
        np.log(1000.0), rel=1e-12)


def test_an_exact_arrhenius_series_returns_the_energy_it_was_built_from():
    """합성으로 0.45 eV 를 넣고 0.45 eV 가 나오는지 -- 상수 자리를 못박는다."""
    wanted = 0.45
    temperatures = [-20, 0, 20, 40, 60, 80]
    sigmas = [1e3 * np.exp(-wanted / (BOLTZMANN_EV_PER_K * kelvin(t)))
              for t in temperatures]
    got = activation_energy(temperatures, sigmas)
    assert got.activation_energy_ev == pytest.approx(wanted, rel=1e-10)
    assert got.fit is not None
    assert got.fit.r_squared == pytest.approx(1.0, abs=1e-12)


def test_sweeps_without_a_temperature_are_left_out_not_read_as_zero():
    """온도를 안 적은 스윕은 빠진다.  0 °C 로 읽으면 직선이 통째로 달라진다."""
    temperatures, sigmas = lab_columns()
    holey = list(temperatures)
    holey[3] = None
    got = activation_energy(holey, sigmas)
    assert got.points_used == 8
    # 여덟 점으로도 같은 물질이므로 답은 거의 같아야 한다.
    assert got.activation_energy_ev == pytest.approx(0.328, abs=0.01)


def test_one_point_says_why_rather_than_inventing_a_line():
    got = activation_energy([25], [1.0])
    assert got.activation_energy_ev is None
    assert got.fit is None
    assert "둘 이상" in got.reason


def test_one_temperature_measured_twice_is_not_a_slope():
    got = activation_energy([25, 25, 25], [1.0, 1.1, 0.9])
    assert got.activation_energy_ev is None
    assert "온도가 모두 같아" in got.reason


def test_an_upward_slope_is_reported_with_a_warning_not_hidden():
    """온도 열을 거꾸로 적으면 활성화에너지가 음수로 나온다.

    숨기지 않는다 -- 계산은 그대로 내고 왜 이상한지 한 줄을 붙인다.  값을
    감추면 사람은 화면이 고장 났다고 생각하고, 음수만 내면 왜인지 모른다.
    """
    temperatures, sigmas = lab_columns()
    got = activation_energy(list(reversed(temperatures)), sigmas)
    assert got.activation_energy_ev is not None
    assert got.activation_energy_ev < 0
    assert "온도 순서" in got.reason


def test_a_zero_conductivity_row_drops_out_instead_of_taking_a_log_of_zero():
    temperatures, sigmas = lab_columns()
    spoiled = list(sigmas)
    spoiled[2] = 0.0
    got = activation_energy(temperatures, spoiled)
    assert got.points_used == 8


def test_mismatched_columns_are_refused():
    with pytest.raises(ValueError, match="짝이 맞아야"):
        activation_energy([20, 30], [1.0])


def test_an_unknown_basis_is_refused_rather_than_silently_defaulted():
    with pytest.raises(ValueError, match="기준은"):
        activation_energy([20, 30], [1.0, 2.0], basis="ln_sigma_over_t")


def test_a_row_knows_whether_it_can_join_the_line():
    assert ConductivityPoint(60, 9.69, 0.79, 0.85, 9.59).usable
    assert not ConductivityPoint(None, 9.69, 0.79, 0.85, 9.59).usable
    assert not ConductivityPoint(60, None, 0.79, 0.85, None).usable
    assert not ConductivityPoint(60, 9.69, 0.79, 0.85, 0.0).usable


# --- 실수축 교점: 제안이지 측정값이 아니다 ---------------------------------

def test_the_crossing_is_found_by_interpolating_between_two_points():
    """정확히 아는 두 점 사이에서 선형 보간이 맞는 자리를 짚는가."""
    frequency = np.array([1e6, 1e5, 1e4, 1e3])
    stored_im = np.array([-2.0, 2.0, 5.0, 9.0])     # 파일이 담는 -Im(Z)
    real = np.array([4.0, 6.0, 8.0, 12.0])
    got = real_axis_crossing(frequency, real, -stored_im)
    # -2 에서 2 로 지나므로 딱 절반 -- Re 는 4 와 6 사이의 5.
    assert got == pytest.approx(5.0, rel=1e-12)


def test_only_the_upward_crossing_counts_so_the_wiring_is_not_read_as_cell():
    """고주파의 유도성 구간에서 내려가는 교차를 잡으면 배선을 전해질로 읽는다.

    실측 파일의 7 MHz 에서 ``-Im`` 은 -82.9 Ω 다 -- 배선 인덕턴스이지 셀이
    아니다.
    """
    frequency = np.array([7e6, 1e6, 1e5, 1e4])
    stored_im = np.array([5.0, -3.0, 1.0, 8.0])    # 내려갔다가 다시 올라간다
    real = np.array([1.0, 3.0, 5.0, 9.0])
    got = real_axis_crossing(frequency, real, -stored_im)
    # 내려가는 교차(1→-3, Re≈2.25)가 아니라 올라가는 교차(-3→1, Re=4.5).
    assert got == pytest.approx(4.5, rel=1e-12)


def test_no_crossing_is_none_rather_than_an_end_point():
    frequency = np.array([1e5, 1e4, 1e3])
    real = np.array([5.0, 6.0, 7.0])
    assert real_axis_crossing(frequency, real, -np.array([1.0, 2.0, 3.0])) is None
    assert real_axis_crossing(frequency, real, -np.array([-1.0, -2.0, -3.0])) is None
    assert real_axis_crossing([1e5], [5.0], [-1.0]) is None


def test_the_points_may_arrive_in_either_frequency_order():
    """EC-Lab 은 내려가며 쓸고 `.mpr` 은 올라가며 쓰는 파일도 있다."""
    frequency = np.array([1e6, 1e5, 1e4, 1e3])
    stored_im = np.array([-2.0, 2.0, 5.0, 9.0])
    real = np.array([4.0, 6.0, 8.0, 12.0])
    descending = real_axis_crossing(frequency, real, -stored_im)
    ascending = real_axis_crossing(frequency[::-1], real[::-1], -stored_im[::-1])
    assert descending == pytest.approx(ascending, rel=1e-12)
