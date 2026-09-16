"""Origin 의 Linear Fit 을 옮겼다면, Origin 의 화면과 같은 수가 나와야 한다.

기준은 랩이 실제로 돌린 것이다: 전해질 B12 의 온도 아홉 점을 Origin 에 붙여
넣고 ``Linear Fit`` 을 누른 결과 (2026-09-16).  그 회색 표의 모든 칸이 여기
적혀 있다.

  Equation                 y = a + b*x
  Weight                   No Weighting
  Intercept                 7.01784 +- 0.4115
  Slope                    -3.80724 +- 0.11916
  Residual Sum of Squares   0.0837
  Pearson's r              -0.99659
  R-Square (COD)            0.99319
  Adj. R-Square             0.99222
  t (Intercept, Slope)      17.05433, -31.95141
  Prob>|t|                  5.8451E-7, 7.60521E-9
  ANOVA  Model SS 12.20625  MSE 0.01196  F 1020.89284  Prob>F 7.60521E-9

**허용오차가 넉넉한 이유**는 알고리즘이 아니라 입력에 있다: 우리가 가진 σ 는
슬라이드의 표에서 읽은 소수 두 자리(9.59, 9.10, …)이고 Origin 이 맞춘 것은
반올림 전의 수다.  0.3 % 는 그 반올림이 기울기에 만드는 차이이며, 실제로 모든
칸이 같은 방향으로 같은 정도만 어긋난다 -- 한 칸만 크게 틀리면 그것은 반올림이
아니라 공식이 다른 것이고, 이 시험이 잡으려는 것이 그쪽이다.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from wrdkit.linfit import linear_fit, regularized_incomplete_beta

#: 60 °C 에서 -20 °C 까지, 10 °C 간격 아홉 점.
LAB_TEMPERATURE_C = [60, 50, 40, 30, 20, 10, 0, -10, -20]
#: 같은 순서의 이온전도도 (mS/cm), 슬라이드의 표에서.
LAB_SIGMA_MS_CM = [9.59, 9.10, 6.38, 4.22, 2.68, 1.66, 0.98, 0.54, 0.31]


def lab_points() -> tuple[np.ndarray, np.ndarray]:
    """랩이 Origin 에 붙여 넣은 두 열 — x = 1000/T, y = ln σ (S/cm)."""
    kelvin = np.array(LAB_TEMPERATURE_C, dtype=float) + 273.15
    sigma_s_cm = np.array(LAB_SIGMA_MS_CM, dtype=float) * 1e-3
    return 1000.0 / kelvin, np.log(sigma_s_cm)


def test_reproduces_origins_linear_fit_report():
    fit = linear_fit(*lab_points())
    assert fit is not None
    assert fit.n_points == 9 and fit.dof == 7
    assert fit.equation == "y = a + b*x"

    assert fit.slope == pytest.approx(-3.80724, rel=3e-3)
    assert fit.intercept == pytest.approx(7.01784, rel=3e-3)
    assert fit.slope_stderr == pytest.approx(0.11916, rel=3e-3)
    assert fit.intercept_stderr == pytest.approx(0.4115, rel=3e-3)

    assert fit.rss == pytest.approx(0.0837, rel=1e-2)
    # 1e-4 도 느슨하지 않다: 공식이 틀리면 (중심화하지 않은 TSS 를 쓴다든지)
    # R² 는 세 자리째부터 달라진다.  반올림이 만드는 차이는 다섯 자리째다.
    assert fit.pearson_r == pytest.approx(-0.99659, abs=1e-4)
    assert fit.r_squared == pytest.approx(0.99319, abs=1e-4)
    assert fit.adj_r_squared == pytest.approx(0.99222, abs=1e-4)

    assert fit.intercept_t == pytest.approx(17.05433, rel=1e-3)
    assert fit.slope_t == pytest.approx(-31.95141, rel=1e-3)
    # 꼬리확률은 지수가 맞는지가 요점이다 -- 5.8e-7 이 5.8e-6 이 되면 "유의하다"
    # 의 뜻이 달라진다.
    assert fit.intercept_p == pytest.approx(5.8451e-7, rel=5e-3)
    assert fit.slope_p == pytest.approx(7.60521e-9, rel=1e-2)

    assert fit.f_value == pytest.approx(1020.89284, rel=3e-3)
    assert fit.tss - fit.rss == pytest.approx(12.20625, rel=3e-3)
    assert fit.rss / fit.dof == pytest.approx(0.01196, rel=1e-2)


def test_prob_greater_f_equals_the_slopes_two_sided_p():
    """단순선형회귀에서 두 수는 같은 가설을 두 가지로 적은 것이다.

    Origin 의 화면에도 둘 다 ``7.60521E-9`` 로 같은 수가 적혀 있다.  여기가
    어긋나면 t 쪽이든 F 쪽이든 하나는 틀린 것이다.
    """
    fit = linear_fit(*lab_points())
    assert fit is not None
    assert fit.f_p == pytest.approx(fit.slope_p, rel=1e-12)


def test_an_exact_line_is_reported_exactly_and_the_errors_are_unknown():
    """잔차가 0 이면 표준오차는 0 이 아니라 **모름**이다.

    0 으로 적으면 "완벽하게 확실한 기울기" 로 읽히는데, 실제로는 재어 볼 잔차가
    하나도 없다는 뜻이다 (§0.4).
    """
    x = np.array([1.0, 2.0, 3.0, 4.0])
    fit = linear_fit(x, 3.0 + 2.5 * x)
    assert fit is not None
    assert fit.slope == pytest.approx(2.5, abs=1e-12)
    assert fit.intercept == pytest.approx(3.0, abs=1e-12)
    assert fit.rss == pytest.approx(0.0, abs=1e-24)
    assert fit.r_squared == pytest.approx(1.0, abs=1e-12)
    assert fit.pearson_r == pytest.approx(1.0, abs=1e-12)
    assert fit.slope_stderr == pytest.approx(0.0, abs=1e-12)
    assert fit.slope_t is None and fit.slope_p is None
    assert fit.f_value is None and fit.f_p is None


def test_two_points_have_a_line_but_nothing_to_say_about_it():
    fit = linear_fit([1.0, 2.0], [0.0, 1.0])
    assert fit is not None
    assert fit.dof == 0
    assert fit.slope == pytest.approx(1.0)
    assert fit.slope_stderr is None and fit.adj_r_squared is None


def test_a_point_without_a_temperature_is_dropped_not_read_as_zero():
    """온도를 안 적은 스윕이 0 으로 들어가면 1000/T 축에 가짜 점이 생긴다."""
    x, y = lab_points()
    with_gap_x = np.concatenate([x, [np.nan]])
    with_gap_y = np.concatenate([y, [np.log(1e-3)]])
    clean = linear_fit(x, y)
    gapped = linear_fit(with_gap_x, with_gap_y)
    assert clean is not None and gapped is not None
    assert gapped.n_points == 9
    assert gapped.slope == pytest.approx(clean.slope, rel=1e-12)


def test_one_temperature_only_has_no_slope():
    """``sxx > 0`` 으로는 못 잡는 자리다.

    같은 값 셋의 평균이 부동소수점에서 1 ulp 어긋나면 ``sxx`` 가 0 이 아니라
    5.9e-31 이 되고, 그것으로 나눈 기울기가 멀쩡한 수처럼 통과한다.  실측:
    25 °C 에서 세 번 잰 것으로 활성화에너지 0.115 eV 가 나왔다.
    """
    assert linear_fit([3.0, 3.0, 3.0], [1.0, 2.0, 3.0]) is None
    assert linear_fit([1000 / 298.15] * 3, [1.0, 1.1, 0.9]) is None
    assert linear_fit([1.0], [1.0]) is None
    # 실측 온도차는 이 문턱보다 아홉 자리 위에 있다 -- 멀쩡한 두 점은 지난다.
    assert linear_fit([3.0017, 3.9502], [-4.6, -8.1]) is not None


def test_mismatched_lengths_are_refused_rather_than_zipped_short():
    with pytest.raises(ValueError, match="짝이 맞아야"):
        linear_fit([1.0, 2.0, 3.0], [1.0, 2.0])


# --- 꼬리확률 자체를 닫힌 형태와 견준다 -------------------------------------

def test_the_t_tail_matches_the_closed_forms_at_one_and_two_degrees():
    """자유도 1·2 의 t 분포는 초등함수로 적히므로 정확한 기준이 된다.

    ν=1 (코시): P(|T|>t) = 1 - (2/π)·arctan(t)
    ν=2:        P(|T|>t) = 1 - t/sqrt(2 + t²)
    """
    for t in (0.5, 1.0, 2.0, 7.5):
        cauchy = 1.0 - 2.0 / math.pi * math.atan(t)
        got = regularized_incomplete_beta(0.5, 0.5, 1.0 / (1.0 + t * t))
        assert got == pytest.approx(cauchy, rel=1e-12)

        two = 1.0 - t / math.sqrt(2.0 + t * t)
        got = regularized_incomplete_beta(1.0, 0.5, 2.0 / (2.0 + t * t))
        assert got == pytest.approx(two, rel=1e-12)


def test_the_incomplete_beta_obeys_its_own_symmetry():
    """``I_x(a,b) = 1 - I_{1-x}(b,a)`` — 두 갈래 계산이 만나는 자리다.

    구현이 x 의 크기에 따라 갈래를 바꾸므로, 이 항등식이 그 이음매를 짚는다.
    """
    for a, b in ((0.5, 0.5), (3.5, 1.0), (1.0, 7.0), (12.0, 4.5)):
        for x in (0.02, 0.2, 0.5, 0.8, 0.99):
            left = regularized_incomplete_beta(a, b, x)
            right = 1.0 - regularized_incomplete_beta(b, a, 1.0 - x)
            assert left == pytest.approx(right, abs=1e-14)
    assert regularized_incomplete_beta(2.0, 3.0, 0.0) == 0.0
    assert regularized_incomplete_beta(2.0, 3.0, 1.0) == 1.0
