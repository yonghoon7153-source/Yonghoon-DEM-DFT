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


def test_the_crossing_is_the_end_of_the_leading_inductive_run():
    """배선 인덕턴스는 **주파수 맨 위**에 있다.  거기서 올라오는 자리가 교점이다.

    실측 파일의 7 MHz 에서 ``-Im`` 은 -82.9 Ω 다 -- 배선이지 셀이 아니다.
    """
    frequency = np.array([7e6, 1e6, 1e5, 1e4])
    stored_im = np.array([-5.0, -3.0, 1.0, 8.0])   # 유도성으로 시작해 올라간다
    real = np.array([1.0, 3.0, 5.0, 9.0])
    got = real_axis_crossing(frequency, real, -stored_im)
    # -3 에서 1 로 지나므로 3 과 5 사이의 3/4 자리 = 4.5.
    assert got == pytest.approx(4.5, rel=1e-12)


def test_noise_in_the_blocking_tail_is_not_a_crossing():
    """이 시험이 2026-09-22 의 실측 사고를 막는다.

    블로킹 대칭셀의 스윕은 유도성 구간이 안 찍히는 일이 잦다 (고주파 끝에서
    이미 ``-Im > 0``).  그런데 예전 코드는 스윕 **전체**에서 올라가는 교차를
    찾아서, 꼬리 깊숙한 곳의 잡음 점 하나를 전해질 저항으로 읽었다.

    실측 `B11_activationE_C01` 의 0 °C 스윕에서 **111400 Ω** 이 나왔고 (아크가
    아니라 꼬리다), 그 때문에 저항이 온도에 대해 거꾸로 갔다 -- 20 °C 79.89 Ω
    인데 10 °C 25.19 Ω.  Arrhenius 직선의 R² 가 0.27 이었다.
    """
    frequency = np.logspace(np.log10(7e6), 1.0, 40)
    real = np.linspace(15.5, 120000.0, 40)
    stored_im = np.linspace(1.0, 60000.0, 40)      # 처음부터 용량성이다
    stored_im[25] = -0.4                           # 꼬리 한복판의 잡음 하나
    # 예전에는 여기서 76928 Ω 이 나왔다.
    assert real_axis_crossing(frequency, real, -stored_im) is None


def test_a_sweep_that_starts_capacitive_has_no_visible_crossing():
    """유도성 구간이 안 찍혔으면 교점은 **볼 수 없다**.

    없는 것을 지어내느니 비운다 (§0.4).  비어 있으면 사람이 ZView 에서 읽어
    적지만, 잘못된 수가 적혀 있으면 아무도 다시 안 본다.
    """
    frequency = np.array([7e6, 1e6, 1e5, 1e4])
    real = np.array([15.6, 15.8, 16.1, 16.4])
    stored_im = np.array([0.98, 2.12, 3.31, 4.58])   # 전부 양수
    assert real_axis_crossing(frequency, real, -stored_im) is None


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


# --- 값은 나왔는데 먼저 봐야 할 것 (2026-09-22) -----------------------------

#: 실측 `B11_activationE_C01`.  교점 검출이 꼬리의 잡음을 집어서 나온 저항들.
#: 이 표가 화면에서 `0.415 eV` 라는 결과로 보였다.
BAD_READING_C = [60, 50, 40, 30, 20, 10, 0, -10, -20]
BAD_READING_OHM = [7.372, 7.285, 8.824, 15.44, 79.89, 25.19, 111400, 56.93, 84.40]


def bad_sigmas():
    return [conductivity_ms_cm(r, thickness_mm=0.79, area_cm2=0.7854)
            for r in BAD_READING_OHM]


def test_a_series_that_goes_backwards_in_temperature_is_called_out():
    """온도가 내려가면 이온전도도는 **반드시** 내려간다.

    거꾸로 가는 구간이 있으면 그 줄의 저항을 잘못 읽은 것이다.  Arrhenius
    직선은 그래도 그려지고 R² 만 조용히 낮아진다 -- 그 침묵이 0.415 eV 를
    결과로 만들었다.
    """
    got = activation_energy(BAD_READING_C, bad_sigmas())
    assert got.activation_energy_ev is not None      # 값을 감추지는 않는다
    backwards = [one for one in got.warnings if "안 내려가는" in one]
    assert len(backwards) == 1
    # 어느 구간인지 짚어야 다시 읽을 수 있다.
    assert "20→10 °C" in backwards[0]
    assert "0→-10 °C" in backwards[0]


def test_a_line_that_does_not_explain_the_points_says_so():
    got = activation_energy(BAD_READING_C, bad_sigmas())
    assert got.fit is not None and got.fit.r_squared < 0.3
    weak = [one for one in got.warnings if "R²" in one]
    assert len(weak) == 1
    assert "값으로 쓸 수 없습니다" in weak[0]


def test_a_good_table_says_nothing_at_all():
    """할 일이 없다는 문장은 소음이다 — 멀쩡하면 조용해야 한다."""
    temperatures, sigmas = lab_columns()
    got = activation_energy(temperatures, sigmas)
    assert got.warnings == ()
    assert got.fit is not None and got.fit.r_squared > 0.99


def test_one_backwards_step_alone_is_enough_to_say_it():
    """R² 가 멀쩡해도 거꾸로 간 구간은 말한다 — 둘은 다른 증상이다."""
    temperatures, sigmas = lab_columns()
    nudged = list(sigmas)
    nudged[1] = nudged[0] + 0.01          # 50 °C 가 60 °C 보다 높다
    got = activation_energy(temperatures, nudged)
    assert any("안 내려가는" in one for one in got.warnings)
    assert got.fit is not None and got.fit.r_squared > 0.9
