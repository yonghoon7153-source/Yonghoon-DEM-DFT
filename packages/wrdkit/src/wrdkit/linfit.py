"""Origin 의 ``Analysis ▸ Fitting ▸ Linear Fit`` 이 내는 보고서, 그대로.

랩이 활성화에너지를 구하는 절차가 "Origin 에 붙여 넣고 Linear Fit 을 누른다"
이고, 슬라이드에 붙는 것은 그 회색 표다 -- ``Intercept 7.01784 ± 0.4115``,
``Slope -3.80724 ± 0.11916``, ``R-Square (COD) 0.99319``.  워크벤치가 기울기만
내고 나머지를 빼면 사람은 그 표를 만들려고 다시 Origin 을 연다.  그래서 **표
전체**를 낸다: 값과 표준오차, t, Prob>|t|, 잔차제곱합, Pearson r, R², 수정 R²,
그리고 ANOVA.

어디까지가 Origin 의 규약인가:

* **가중 없음** (``No Weighting``).  점마다 오차를 모르는 상태에서 무게를 주면
  그 무게가 결과를 정한다.  랩의 화면이 쓰는 것도 이쪽이다.
* 표준오차는 보통최소제곱의 그것에 ``sqrt(reduced chi-square)`` 를 곱한 값이다.
  가중이 없을 때 reduced chi-square 는 곧 잔차평균제곱이므로, 여기 식이 Origin
  의 화면과 같은 수를 낸다 (실측 대조는 ``test_linfit.py``).
* 자유도는 ``n - 2``.  점이 둘이면 직선은 지나가지만 오차를 말할 근거가 없어서
  ``dof = 0`` 이고, 그때 표준오차와 p 값은 ``None`` 이다 -- 0 이 아니라 모름이다
  (§0.4).

p 값에 scipy 를 쓰지 않는다.  ``wrdkit`` 의 핵심은 numpy 만 의존한다(§1)는
약속이 있고, 여기 필요한 것은 정규화 불완전베타 함수 하나뿐이라 직접 쓴다.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

__all__ = ["LinearFit", "linear_fit", "regularized_incomplete_beta"]


@dataclass(frozen=True)
class LinearFit:
    """``y = a + b·x`` 한 번의 결과 — Origin 의 보고서와 같은 항목들.

    ``None`` 인 칸은 "이 점들로는 말할 수 없다" 이다.  점 둘로 그은 직선의
    표준오차를 0 으로 적으면 완벽한 맞춤처럼 보이는데, 실제로는 재어 볼 잔차가
    하나도 없는 것이다.
    """

    #: ``b`` — x 한 단위당 y 의 변화.
    slope: float
    #: ``a`` — x = 0 에서의 y.  Arrhenius 에서는 ln(전지수인자) 다.
    intercept: float
    slope_stderr: float | None
    intercept_stderr: float | None
    n_points: int
    #: ``n - 2``.  0 이면 오차를 말할 수 없다.
    dof: int
    #: 잔차제곱합 (Origin 의 ``Residual Sum of Squares``).
    rss: float
    #: 전체제곱합.  0 이면 y 가 모두 같아서 R² 를 정의할 수 없다.
    tss: float
    pearson_r: float | None
    #: ``R-Square (COD)`` = 1 - RSS/TSS.
    r_squared: float | None
    #: ``Adj. R-Square`` — 자유도로 벌점을 준 R².
    adj_r_squared: float | None
    slope_t: float | None
    slope_p: float | None
    intercept_t: float | None
    intercept_p: float | None
    #: ANOVA 의 F 와 Prob>F.  단순선형회귀에서는 Prob>F 가 기울기의 Prob>|t| 와
    #: 같다 -- 같은 가설을 두 가지로 적은 것이라 그렇고, 화면의 두 수가 어긋나면
    #: 둘 중 하나가 틀린 것이다.
    f_value: float | None
    f_p: float | None

    @property
    def equation(self) -> str:
        return "y = a + b*x"


def linear_fit(x, y) -> LinearFit | None:
    """유한한 점만 골라 ``y = a + b·x`` 를 맞춘다.  못 맞추면 ``None``.

    NaN 을 조용히 0 으로 읽지 않는다: 온도를 안 적은 스윕이 있으면 그 점은
    빠져야 하고, 0 으로 들어가면 1000/T 축의 원점에 가짜 점이 생겨 기울기가
    통째로 달라진다.

    x 가 모두 같으면 기울기가 존재하지 않으므로 ``None`` 이다 (한 온도에서만
    쟀다는 뜻이다).
    """
    xs = np.asarray(x, dtype=np.float64).ravel()
    ys = np.asarray(y, dtype=np.float64).ravel()
    if xs.size != ys.size:
        raise ValueError(f"x 는 {xs.size}개, y 는 {ys.size}개 -- 짝이 맞아야 한다")
    good = np.isfinite(xs) & np.isfinite(ys)
    xs, ys = xs[good], ys[good]
    n = int(xs.size)
    if n < 2:
        return None
    # x 가 퍼져 있지 않으면 기울기가 존재하지 않는다.  **``sxx > 0`` 으로는
    # 못 잡는다**: 같은 값 셋의 평균이 부동소수점에서 1 ulp 어긋나 ``sxx`` 가
    # 5.9e-31 로 나오고, 그것으로 나눈 기울기가 그대로 통과한다.  실측 --
    # 25 °C 에서 세 번 잰 것으로 활성화에너지 0.115 eV 가 나왔다.  퍼짐은
    # 크기에 견주어 봐야 뜻이 있으므로 상대 기준을 쓴다 (1e-9 은 어떤 실측
    # 온도차보다도 작다).
    spread = float(np.ptp(xs))
    scale = float(np.max(np.abs(xs)))
    if spread <= 1e-9 * max(scale, 1.0):
        return None
    sxx = float(((xs - xs.mean()) ** 2).sum())
    if sxx <= 0:
        return None

    syy = float(((ys - ys.mean()) ** 2).sum())
    sxy = float(((xs - xs.mean()) * (ys - ys.mean())).sum())
    slope = sxy / sxx
    intercept = float(ys.mean() - slope * xs.mean())
    residual = ys - (intercept + slope * xs)
    rss = float(residual @ residual)
    dof = n - 2

    pearson = sxy / math.sqrt(sxx * syy) if syy > 0 else None
    r_squared = 1.0 - rss / syy if syy > 0 else None
    adj = None
    if syy > 0 and dof > 0:
        adj = 1.0 - (rss / dof) / (syy / (n - 1))

    slope_se = intercept_se = None
    slope_t = slope_p = intercept_t = intercept_p = None
    f_value = f_p = None
    if dof > 0:
        # 가중이 없으므로 reduced chi-square 가 곧 잔차평균제곱이다.
        mse = rss / dof
        slope_se = math.sqrt(mse / sxx)
        intercept_se = math.sqrt(mse * (1.0 / n + xs.mean() ** 2 / sxx))
        # 잔차가 정확히 0 이면 (점 둘을 지나는 직선 등) t 가 무한대다.  Origin
        # 은 빈칸을 내고 우리도 "모름" 으로 둔다 -- inf 를 화면에 흘리면 표가
        # 깨지고, 그 수는 "무한히 확실하다" 가 아니라 "잴 것이 없다" 이다.
        if slope_se > 0:
            slope_t = slope / slope_se
            slope_p = _two_sided_t(slope_t, dof)
        if intercept_se > 0:
            intercept_t = intercept / intercept_se
            intercept_p = _two_sided_t(intercept_t, dof)
        if mse > 0:
            f_value = (syy - rss) / mse
            f_p = _prob_greater_f(f_value, 1, dof)

    return LinearFit(
        slope=slope, intercept=intercept,
        slope_stderr=slope_se, intercept_stderr=intercept_se,
        n_points=n, dof=dof, rss=rss, tss=syy,
        pearson_r=pearson, r_squared=r_squared, adj_r_squared=adj,
        slope_t=slope_t, slope_p=slope_p,
        intercept_t=intercept_t, intercept_p=intercept_p,
        f_value=f_value, f_p=f_p,
    )


# --------------------------------------------------------------------------
# p 값 — 정규화 불완전베타 하나로 t 와 F 를 둘 다 낸다
# --------------------------------------------------------------------------
def _two_sided_t(t: float, dof: int) -> float:
    """``Prob>|t|`` — 학생 t 분포의 양측 꼬리."""
    if not math.isfinite(t):
        return 0.0
    return regularized_incomplete_beta(dof / 2.0, 0.5, dof / (dof + t * t))


def _prob_greater_f(f: float, d1: int, d2: int) -> float:
    """``Prob>F`` — F 분포의 윗꼬리."""
    if not math.isfinite(f) or f <= 0:
        return 1.0
    return regularized_incomplete_beta(d2 / 2.0, d1 / 2.0, d2 / (d2 + d1 * f))


def regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    """``I_x(a, b)`` — Lentz 의 연분수 (Numerical Recipes §6.4).

    t 와 F 의 꼬리확률이 둘 다 이 함수의 값이라, 이것 하나면 scipy 없이 표를
    채울 수 있다.  수렴은 ``x < (a+1)/(a+b+2)`` 쪽에서 빠르므로, 반대쪽이면
    대칭식 ``I_x(a,b) = 1 - I_{1-x}(b,a)`` 로 바꿔 계산한다.
    """
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                     + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _beta_continued_fraction(a, b, x) / a
    return 1.0 - front * _beta_continued_fraction(b, a, 1.0 - x) / b


def _beta_continued_fraction(a: float, b: float, x: float,
                             max_terms: int = 300) -> float:
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, max_terms + 1):
        m2 = 2 * m
        # 짝수 항
        numerator = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        # 홀수 항
        numerator = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        step = d * c
        h *= step
        if abs(step - 1.0) < 3e-16:
            break
    return h
