"""이온전도도와 활성화에너지 — 대칭셀 온도 스윕이 끝나면 남는 두 수.

랩의 절차는 이렇다.  블로킹 대칭셀(SS|전해질|SS)을 챔버에 넣고 온도를 60 °C
에서 -20 °C 까지 10 °C 씩 내리면서, 온도마다 오래 쉬어 평형을 잡고 PEIS 를 한
번씩 건다.  한 `.mpt` 안에 스윕이 아홉 개 들어 있고, 온도마다 저항 하나를 읽어
::

    sigma = t / (R · A)

로 이온전도도를 낸 다음, ``ln sigma`` 대 ``1000/T`` 직선의 기울기에서 활성화
에너지를 얻는다.

**온도는 파일이 모른다.**  `.mpt` 의 어느 열에도 온도가 없다 -- 챔버를 돌린
것은 사람이고, 계측기는 자기가 몇 도에서 쟀는지 기록하지 않는다.  그래서 SOC
와 같은 종류의 칸이다 (ADR 0038): 사람이 적고, 안 적으면 모르는 것이다.

**EC-Lab 이 같이 내보낸 전도도 열은 쓰지 않는다.**  `.mpt` 머리말의
``Electrode surface area : 0.001 cm2`` 는 아무도 안 고친 기본값이고,
``Re(Conductivity)/mS/cm`` 이하 여섯 열이 전부 그 면적에서 나온 수다.  단위가
맞고 그럴듯해서 제일 위험하다 -- 실제 면적이 0.85 cm² 면 850배 틀린다.  여기서는
`Re(Z)` 에서 읽은 저항과 **사람이 적은** 두께·면적으로만 계산한다.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..linfit import LinearFit, linear_fit

__all__ = ["ACTIVATION_BASES", "BOLTZMANN_EV_PER_K", "ActivationEnergy",
           "ConductivityPoint", "activation_energy", "conductivity_ms_cm",
           "kelvin", "real_axis_crossing"]

#: 볼츠만 상수, eV/K.  SI 의 정의상수 둘의 몫이라 반올림이 아니라 정의값이다
#: (k = 1.380649e-23 J/K, e = 1.602176634e-19 C).
BOLTZMANN_EV_PER_K = 1.380649e-23 / 1.602176634e-19

#: 절대영도.
_ZERO_C_IN_K = 273.15

#: ``sigma``  — ``ln sigma``  대 1000/T.  랩이 쓰는 쪽이고 기본값이다.
#: ``sigma_t`` — ``ln(sigma·T)`` 대 1000/T.  호핑 전도의 교과서 형태.
ACTIVATION_BASES = ("sigma", "sigma_t")


def kelvin(temperature_c: float) -> float:
    return float(temperature_c) + _ZERO_C_IN_K


def conductivity_ms_cm(resistance_ohm: float | None, *,
                       thickness_mm: float | None,
                       area_cm2: float | None) -> float | None:
    """``sigma = t / (R·A)`` 를 mS/cm 로.  셋 중 하나라도 없으면 ``None``.

    두께를 **mm** 로 받는 이유는 캘리퍼가 읽는 단위가 그것이고 슬라이드의 표도
    mm 로 적혀 있어서다 (0.79 mm).  cm 로 고쳐 나누는 자리는 여기 한 곳뿐이라,
    10 배 틀릴 자리도 한 곳뿐이다.

    랩의 계산기(엑셀)와 같은 식이다::

        = D4/(E4*F4)*1000      D4 두께(cm), E4 면적(cm²), F4 저항(Ω)

    0 이나 음수는 값이 아니라 "아직 안 적었다" 이거나 잘못 적은 것이다.  나누면
    inf 가 나오고, inf 는 화면에서 커다란 전도도로 보인다.
    """
    if resistance_ohm is None or thickness_mm is None or area_cm2 is None:
        return None
    if not (resistance_ohm > 0 and thickness_mm > 0 and area_cm2 > 0):
        return None
    thickness_cm = float(thickness_mm) / 10.0
    return thickness_cm / (float(resistance_ohm) * float(area_cm2)) * 1000.0


@dataclass(frozen=True)
class ConductivityPoint:
    """표의 한 줄 — 온도 하나에서 읽은 저항과 거기서 나온 전도도."""

    temperature_c: float | None
    resistance_ohm: float | None
    thickness_mm: float | None
    area_cm2: float | None
    sigma_ms_cm: float | None

    @property
    def usable(self) -> bool:
        """활성화에너지의 직선에 들어갈 수 있는 줄인가."""
        return (self.temperature_c is not None
                and self.sigma_ms_cm is not None
                and self.sigma_ms_cm > 0)


@dataclass(frozen=True)
class ActivationEnergy:
    """Arrhenius 직선 하나와, 거기서 읽은 활성화에너지.

    ``activation_energy_ev`` 가 ``None`` 이면 ``reason`` 이 왜인지 말한다 --
    점이 모자라거나, 온도가 하나뿐이거나, 전도도를 낼 수 없는 줄뿐이거나.
    """

    activation_energy_ev: float | None
    #: 기울기의 표준오차에서 그대로 온 것.  ``None`` 이면 점이 둘뿐이라 오차를
    #: 말할 수 없다는 뜻이다 (0 이 아니다).
    stderr_ev: float | None
    #: ``sigma`` | ``sigma_t`` — 무엇의 로그를 세로축에 놓았는가.
    basis: str
    #: Origin 의 Linear Fit 보고서 그대로.  ``None`` 이면 직선이 없다.
    fit: LinearFit | None
    #: 직선에 실제로 들어간 점의 수.
    points_used: int
    reason: str = ""
    #: 값은 나왔지만 **믿을 근거가 약한** 자리들.  `reason` 과 다르다: 저쪽은
    #: "값이 없다" 이고 이쪽은 "값은 있는데 이것부터 보라" 다.
    #:
    #: 이 칸이 생긴 이유 (실측 2026-09-22): R² 가 0.27 인 직선에서 나온
    #: 0.415 eV 가 화면 맨 위에 결과처럼 앉아 있었다.  R² 는 다른 칸에 따로
    #: 적혀 있어서, 둘을 이어 보지 않으면 그냥 답으로 읽힌다 -- 그리고 그
    #: 숫자가 슬라이드로 넘어간다 (§0.4).
    warnings: tuple[str, ...] = ()
    #: 직선을 그린 두 열 — x = 1000/T (K⁻¹), y = ln σ (또는 ln σT).  화면이
    #: 다시 계산하지 않게 함께 낸다: 계산이 두 군데 있으면 언젠가 갈라진다.
    x: tuple[float, ...] = ()
    y: tuple[float, ...] = ()

    @property
    def prefactor_s_cm(self) -> float | None:
        """``sigma_0`` — 절편의 지수.  ``sigma_t`` 기준에서는 단위가 S·K/cm 다."""
        if self.fit is None:
            return None
        return float(np.exp(self.fit.intercept))


def activation_energy(temperature_c, sigma_ms_cm, *,
                      basis: str = "sigma") -> ActivationEnergy:
    """``ln sigma`` 대 ``1000/T`` 직선의 기울기에서 활성화에너지 (eV).

    ``Ea = -slope · 1000 · k_B`` 다.  가로축을 ``1000/T`` 로 두는 것은 Origin
    화면의 관행이고 (그래야 눈금이 3.0~4.0 처럼 읽힌다), 1000 은 그 때문에 다시
    곱해 준다.

    **왜 ``ln sigma`` 이고 ``ln(sigma·T)`` 가 아닌가.**  호핑 전도의 교과서
    식은 ``sigma·T = A·exp(-Ea/kT)`` 라 세로축에 ``ln(sigma·T)`` 를 놓는 쪽이
    더 흔하다.  그런데 랩이 슬라이드에 적어 온 0.328 eV 는 ``ln sigma`` 쪽의
    수다 -- 같은 아홉 점에서 ``ln(sigma·T)`` 로 맞추면 0.353 eV 가 나온다 (7.6 %
    차이).  **둘 다 맞는 수이고 뜻이 다르다.**  기본값을 랩의 관행에 맞추되
    어느 쪽인지 늘 함께 낸다 (``basis``): 0.33 과 0.35 는 표에 나란히 놓이면
    다른 물질처럼 보이므로, 무엇을 맞춘 수인지 안 적힌 활성화에너지는 비교할 수
    없다.

    ``sigma`` 는 mS/cm 로 받고 S/cm 로 고쳐 로그를 취한다.  단위를 바꾸면
    기울기는 그대로고 절편만 ``ln 1000`` 만큼 움직이므로 **활성화에너지는 변하지
    않지만**, 절편(전지수인자)은 달라진다 -- 그쪽도 화면에 나가므로 랩이 Origin
    에 붙여 넣는 것과 같은 단위(S/cm)를 쓴다.
    """
    if basis not in ACTIVATION_BASES:
        raise ValueError(f"기준은 {ACTIVATION_BASES} 중 하나여야 한다: {basis!r}")

    temperatures = np.asarray(temperature_c, dtype=object).ravel()
    sigmas = np.asarray(sigma_ms_cm, dtype=object).ravel()
    if temperatures.size != sigmas.size:
        raise ValueError(f"온도 {temperatures.size}개, 전도도 {sigmas.size}개 "
                         f"-- 짝이 맞아야 한다")

    x: list[float] = []
    y: list[float] = []
    for temperature, sigma in zip(temperatures, sigmas, strict=True):
        if temperature is None or sigma is None:
            continue
        t_k = kelvin(float(temperature))
        value = float(sigma)
        # 절대영도 이하는 온도가 아니고, 0 이하의 전도도는 로그를 가질 수 없다.
        if not (t_k > 0 and value > 0):
            continue
        x.append(1000.0 / t_k)
        y.append(np.log(value * 1e-3 * (t_k if basis == "sigma_t" else 1.0)))

    if len(x) < 2:
        return ActivationEnergy(
            None, None, basis, None, len(x),
            "온도와 이온전도도가 모두 적힌 스윕이 둘 이상이어야 직선이 섭니다"
            f" (지금 {len(x)}개)", tuple(x), tuple(y))

    fit = linear_fit(x, y)
    if fit is None:
        return ActivationEnergy(
            None, None, basis, None, len(x),
            "온도가 모두 같아 기울기가 없습니다 — 두 온도 이상에서 재야 합니다",
            tuple(x), tuple(y))

    ev_per_slope = 1000.0 * BOLTZMANN_EV_PER_K
    stderr = (fit.slope_stderr * ev_per_slope
              if fit.slope_stderr is not None else None)
    return ActivationEnergy(
        activation_energy_ev=-fit.slope * ev_per_slope,
        stderr_ev=stderr, basis=basis, fit=fit, points_used=fit.n_points,
        reason="" if fit.slope < 0 else
               "기울기가 양수입니다 — 온도가 높을수록 전도도가 낮게 적혀 "
               "있습니다. 온도 순서를 확인해 주세요",
        warnings=_activation_warnings(temperatures, sigmas, fit),
        x=tuple(x), y=tuple(y),
    )


#: 직선이 점들을 설명한다고 보기 어려운 R².
#:
#: 실측 전해질은 0.99 위에서 논다 (랩 슬라이드가 0.993).  0.9 는 넉넉히 잡은
#: 값이고, 그 아래로 내려가면 그것은 "조금 흩어졌다" 가 아니라 **점들이 직선이
#: 아니다** 이다 -- 보통 저항을 잘못 읽은 스윕이 섞인 것이다.
_WEAK_R_SQUARED = 0.9


def _activation_warnings(temperature_c, sigma_ms_cm,
                         fit: LinearFit) -> tuple[str, ...]:
    """값은 나왔는데 **먼저 봐야 할 것**이 있으면 그것을 적는다.

    둘 다 값싸고 결정적인 검사다.  둘 다 통과하면 조용하다 -- 할 일이 없다는
    문장은 소음이다.
    """
    out: list[str] = []

    # 1) 온도가 내려가면 전도도는 **반드시** 내려간다.  거꾸로 가는 구간이
    #    있으면 그 줄의 저항을 잘못 읽은 것이다 (실측 2026-09-22: 20 °C 에서
    #    79.89 Ω 인데 10 °C 에서 25.19 Ω 이었다 -- 교점 검출이 꼬리의 잡음을
    #    집었다).  Arrhenius 직선은 그래도 그려지고 R² 만 조용히 낮아진다.
    pairs = [(float(t), float(s))
             for t, s in zip(temperature_c, sigma_ms_cm, strict=True)
             if t is not None and s is not None and s > 0]
    pairs.sort(key=lambda one: one[0], reverse=True)      # 높은 온도부터
    backwards = [(pairs[i - 1][0], pairs[i][0])
                 for i in range(1, len(pairs))
                 if pairs[i][1] >= pairs[i - 1][1]]
    if backwards:
        where = ", ".join(f"{high:g}→{low:g} °C" for high, low in backwards[:4])
        out.append(
            f"온도가 내려가는데 이온전도도가 안 내려가는 구간이 "
            f"{len(backwards)}개 있습니다 ({where}) — 그 온도의 저항을 다시 "
            f"읽어 주세요")

    # 2) 직선이 점들을 설명하는가.
    if fit.r_squared is not None and fit.r_squared < _WEAK_R_SQUARED:
        out.append(
            f"직선이 점들을 설명하지 못합니다 (R² = {fit.r_squared:.3f}) — "
            f"이 활성화에너지는 아직 값으로 쓸 수 없습니다")
    return tuple(out)


def real_axis_crossing(frequency_hz, z_re, z_im) -> float | None:
    """``-Im(Z)`` 가 **아래에서 위로** 0 을 지나는 자리의 ``Re(Z)``.

    **이것은 제안이지 측정값이 아니다.**  실측 ``B12_activationE_C02.mpt`` 아홉
    스윕에서 재 보면, 이 교점과 맞춤의 직렬저항(``R0``)과 ``-Im`` 최솟값은 서로
    2 % 안에서 같다 (Ea 0.2897 · 0.2959 · 0.2894 eV).  이 파일에서는 어느 쪽으로
    읽어도 거의 같은 답이 나온다는 뜻이다.

    그래도 기계가 고르지 않는 이유는 **셋이 서로 다른 것을 재기 때문**이다.  이
    파일은 60 °C 에서도 아크가 7 MHz 위에 있어 나이퀴스트가 사실상 "직렬저항 +
    블로킹 꼬리" 뿐이고, 그래서 셋이 같은 자리에 온다.  벌크와 입계 아크가
    분해되는 전해질에서는 교점이 아크 **앞**에 찍혀 입계 저항이 통째로 빠진다 --
    그때 σ 는 과대평가되고 표는 여전히 멀쩡해 보인다.  어느 쪽을 쓸지는 그
    나이퀴스트를 본 사람이 정한다 (§0.4).

    맞춤의 **총저항**은 더 위험하다: 회로에 블로킹 꼬리를 담을 요소가 없으면
    맞춤이 ``p(R1,CPE1)`` 로 꼬리를 흉내내고, 같은 실측 파일에서 총저항이 이
    교점의 4710~8193배로 나왔다 (60 °C 에서 4.82 Ω 대 22687 Ω).

    올라가는 교차만 찾는 이유는 고주파 쪽의 유도성 구간 때문이다: 배선 인덕턴스가
    ``-Im`` 을 음수로 끌고 내려가 있다가 (실측 7 MHz 에서 -82.9 Ω) 아크가 시작
    되며 위로 지난다.  내려가는 교차를 잡으면 배선을 전해질로 읽게 된다.

    **그 교차는 주파수 맨 위의 연속된 유도성 구간 끝에만 있다.**  그 뒤로는
    아무리 0 을 지나도 전해질 저항이 아니다 -- 블로킹 꼬리의 잡음이다.
    처음에는 스윕 **전체**에서 올라가는 교차를 찾았고, 그래서 이런 일이 났다
    (실측 2026-09-22, `B11_activationE_C01`):

    ======  ====  ==========  ===============================================
    스윕    온도  낸 값       실제
    ======  ====  ==========  ===============================================
    5       20 °C   79.89 Ω   앞쪽 점들로 외삽하면 15.4 Ω (5배)
    7        0 °C  111400 Ω   꼬리 깊숙한 곳의 잡음 점 하나
    ======  ====  ==========  ===============================================

    그 결과 저항이 온도에 대해 **거꾸로** 갔다 (20 °C 79.89 Ω 인데 10 °C 25.19 Ω).
    합성으로 재현하면, 꼬리 한복판에 ``-Im`` 이 0 아래로 내려간 점 **하나**만
    있어도 76928 Ω 이 나온다.

    그래서 이제 **맨 위부터 이어진 유도성 구간**만 본다.  가장 높은 주파수의
    점이 이미 용량성이면 (``-Im > 0``) 유도성 구간이 이 스윕에 안 찍힌 것이고,
    교점은 **볼 수 없다** -- 그때는 ``None`` 이다.  없는 것을 지어내느니 비우는
    편이 낫다 (§0.4): 비어 있으면 사람이 ZView 에서 읽어 적지만, 잘못된 수가
    적혀 있으면 아무도 다시 안 본다.

    보간은 두 점 사이 선형이다.
    """
    frequency = np.asarray(frequency_hz, dtype=np.float64).ravel()
    stored_im = -np.asarray(z_im, dtype=np.float64).ravel()   # 파일이 담는 -Im
    real = np.asarray(z_re, dtype=np.float64).ravel()
    if not (frequency.size == stored_im.size == real.size) or frequency.size < 2:
        return None
    order = np.argsort(-frequency)          # 높은 주파수부터 — 측정 순서다
    stored_im, real = stored_im[order], real[order]

    usable = np.flatnonzero(np.isfinite(stored_im) & np.isfinite(real))
    if len(usable) < 2:
        return None
    stored_im, real = stored_im[usable], real[usable]

    # 맨 위(가장 높은 주파수)가 이미 용량성이면 유도성 구간이 안 찍힌 것이다.
    # 이 스윕으로는 교점을 볼 수 없다.
    if not stored_im[0] < 0:
        return None

    # 이어진 유도성 구간이 끝나는 자리 — 거기가 교점이고, 그 뒤는 안 본다.
    for i in range(1, len(stored_im)):
        before, after = stored_im[i - 1], stored_im[i]
        if before < 0 <= after:
            span = after - before
            if span <= 0:
                return float(real[i])
            weight = -before / span
            return float(real[i - 1] + weight * (real[i] - real[i - 1]))
        if before >= 0:
            # 유도성 구간이 이미 끝났는데 교차를 못 만났다 -- 여기서 멈춘다.
            # 계속 가면 꼬리의 잡음을 교점으로 읽는다.
            return None
    return None
