"""The linear Kramers–Kronig test, and what the audit makes of it (ADR 0043).

Anchors: the paper's own synthetic spectrum (Schönleber et al. 2014, IS1:
100 Ω + 200 Ω ∥ 0.8 µF + 500 Ω ∥ Warburg 0.4 mS·s^½, 1 µHz–10 MHz, noise
|Z|/1000) and the shapes of this lab's cells.  Every noisy spectrum has a fixed
seed -- a KK verdict that depends on the draw is not a test.
"""

import re

import numpy as np
import pytest

from wrdkit.eis.audit import CHECK, NOTE, _kk_findings, audit_spectrum
from wrdkit.eis.circuit import parse_circuit
from wrdkit.eis.kk import MU_LIMIT, KKResult, _mu, lin_kk
from wrdkit.eis.spectrum import Spectrum


def sweep(fmax, fmin, per_decade=10):
    n = int(round(np.log10(fmax / fmin) * per_decade)) + 1
    return np.logspace(np.log10(fmax), np.log10(fmin), n)


def cpe(q, n, w):
    return 1.0 / (q * (1j * w) ** n)


def par(a, b):
    return a * b / (a + b)


def noisy(z, rel, seed):
    rng = np.random.default_rng(seed)
    scale = np.abs(z) * rel
    return z + scale * rng.standard_normal(z.size) + 1j * scale * rng.standard_normal(z.size)


def spectrum(f, z):
    return Spectrum(f, z.real, z.imag)


def is1(seed=1, rel=1e-3):
    f = sweep(1e7, 1e-6)
    w = 2 * np.pi * f
    warburg = 1 / (0.4e-3 * np.sqrt(1j * w))
    return f, noisy(100 + par(200, 1 / (1j * w * 0.8e-6)) + par(500, warburg), rel, seed)


def oxide(f, k=1.0):
    """A pellet whose bulk and grain boundary both show, and a blocking tail."""
    w = 2 * np.pi * f
    return (5 + par(2e4 * k, cpe(1e-10, 0.95, w)) + par(4e4 * k, cpe(3.23e-8, 0.85, w))
            + cpe(1e-6, 0.9, w))


def sulfide(f):
    """B15 50 °C: cable L, intercept R0, double-layer CPE -- 7 MHz to 10 Hz."""
    w = 2 * np.pi * f
    return 8.3 + 1j * w * 1.73e-6 + cpe(1.9e-6, 0.86, w)


# -- the test itself ---------------------------------------------------------

def test_mu_is_one_minus_the_negative_share():
    assert _mu(np.array([3.0, 1.0])) == 1.0
    assert _mu(np.array([3.0, 1.0, -1.0])) == pytest.approx(0.75)
    assert MU_LIMIT == 0.85                      # SCHOENLEBER2014.mu-threshold-c


def test_the_papers_synthetic_spectrum_passes_at_a_few_elements_per_decade():
    """IS1a: the μ-optimum is 2–4 elements per decade (Fig. 8 read), and the
    residuals are at the noise level."""
    f, z = is1()
    result = lin_kk(f, z.real, z.imag)
    assert result.judged and not result.capped
    assert 2.0 <= result.per_decade <= 5.0
    assert result.mu < MU_LIMIT <= result.mu_trace[-2]
    assert result.max_residual < 0.01


def test_a_blocking_pellet_with_cables_brings_its_capacitor_and_inductor():
    f = sweep(7e6, 10)
    z = noisy(sulfide(f), 1e-3, 4)
    result = lin_kk(f, z.real, z.imag)
    assert result.with_capacitance and result.with_inductance
    assert result.max_residual < 0.015


def test_too_little_to_test_is_said_so():
    f = sweep(1e3, 1e2, 3)
    z = oxide(f)
    result = lin_kk(f, z.real, z.imag)
    assert not result.judged and "점이" in result.reason
    narrow = np.linspace(100, 500, 20)
    z = oxide(narrow)
    assert "decade" in lin_kk(narrow, z.real, z.imag).reason


# -- what the audit says ---------------------------------------------------------

@pytest.mark.parametrize("seed", [1, 2, 3])
def test_clean_spectra_say_nothing(seed):
    f = sweep(1e6, 0.01)
    for z in (oxide(f), ):
        audit = audit_spectrum(spectrum(f, noisy(z, 1e-3, seed)))
        assert audit.kk["judged"]
        assert audit.findings == []
    f = sweep(7e6, 10)
    assert audit_spectrum(spectrum(f, noisy(sulfide(f), 1e-3, seed))).findings == []


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_a_step_in_the_middle_of_the_sweep_is_found_where_it_is(seed):
    """10 Hz 아래가 5 % 계단으로 바뀐 스펙트럼 — 눌림·접촉이 바뀐 셀."""
    f = sweep(1e6, 0.01)
    z = noisy(np.where(f < 10, oxide(f, 1.05), oxide(f)), 1e-3, seed)
    (finding,) = audit_spectrum(spectrum(f, z)).findings
    assert finding.severity == CHECK and finding.code == "kk_violation"
    span = finding.message.split(" 에서 ")[0]
    low, high = (float(x) for x in span.replace(" Hz", "").split("–"))
    assert low <= 10 <= high                     # 계단이 있는 자리
    assert "SCHOENLEBER2014.residuals" in finding.refs


def test_one_point_that_flew_is_a_note():
    f = sweep(1e6, 0.01)
    z = noisy(oxide(f), 1e-3, 1)
    z[25] *= 1.05
    (finding,) = audit_spectrum(spectrum(f, z)).findings
    assert finding.severity == NOTE and finding.code == "kk_outlier"
    assert f"{f[25]:.3g} Hz" in finding.message


def test_a_noisy_spectrum_is_named_noisy_not_broken():
    f = sweep(7e6, 10)
    (finding,) = audit_spectrum(spectrum(f, noisy(sulfide(f), 2e-2, 4))).findings
    assert finding.code == "kk_noisy" and finding.severity == NOTE


def test_where_mu_stops_too_early_the_second_look_judges():
    """이상적 RC 아크 (n = 1) 와 참 저주파 유도성 루프 — KK 를 만족하는데 μ 가
    decade 당 0.5 개에서 멈춰 잔차가 수십 % 다.  '어긴다' 고 하지 않는다: 두 번째
    보기가 판정하고, 이유가 무엇을 했는지 말한다."""
    f = sweep(7e6, 0.1)
    w = 2 * np.pi * f
    sharp = 5 + par(2e4, 1 / (1j * w * 1e-10)) + par(4e4, 1 / (1j * w * 3e-8)) \
        + 1 / (1j * w * 1e-6)
    audit = audit_spectrum(spectrum(f, noisy(sharp, 2e-3, 5)))
    assert audit.findings == []
    assert audit.kk["judged"] is True and audit.kk["max_residual"] < 0.02
    assert "일찍 멈춥니다" in audit.kk["reason"]
    assert "어긋남은 없습니다" in audit.kk["reason"]

    f = sweep(7e6, 1e-2)
    w = 2 * np.pi * f
    loop = 4.9 + par(10.4, cpe(3.06e-5, 0.658, w)) + par(6.6, cpe(1.36e-3, 0.757, w)) \
        + par(2.0, 1j * w * 20.0)
    audit = audit_spectrum(spectrum(f, noisy(loop, 2e-3, 6)))
    assert "어긋남은 없습니다" in audit.kk["reason"]
    assert not [one for one in audit.findings if one.code.startswith("kk_")]
    # 끝이 축 위라는 것은 KK 와 별개로 말한다 — 드리프트인지 루프인지는 사람이.
    assert [one.code for one in audit.findings] == ["low_frequency_inductive"]


def test_no_points_no_verdict():
    assert audit_spectrum(None).kk == {"judged": False, "reason": "점이 없습니다"}


# -- 실측 검수(2026-09-23 04:13) 뒤에 고친 것 ---------------------------------------

def test_the_cable_run_at_the_top_is_left_out_like_the_fit_leaves_it():
    """배선 L 이 7 MHz 부터 수백 kHz 까지를 축 위로 올린다.  그 점들은 셀이
    아니다 — 실측에서 거의 모든 스윕이 1.7–7 MHz 에서 "어긴다" 가 떴다."""
    f = sweep(7e6, 10)
    z = noisy(sulfide(f), 2e-3, 3)
    bent = z.copy()
    cables = (f > 1.5e6) & (f < 5e6)
    bent[cables] = bent[cables] * (1 + 0.06j)        # L 하나로는 안 그려지는 배선
    result = lin_kk(f, bent.real, bent.imag)
    assert result.dropped_inductive > 0
    assert result.frequency_hz.max() < 1.5e6
    assert result.with_inductance                     # 아래 점에는 아직 L 이 걸린다
    assert audit_spectrum(spectrum(f, bent)).findings == []


def test_a_band_just_under_the_top_is_the_top_not_the_middle():
    """꼭대기 7 MHz 바로 아래 2–5 MHz 가 어긋나도 "고주파 끝" 이다.  실측에서
    이것이 "셀이나 접촉이 바뀌었습니다" (확인) 로 읽혔다."""
    f = sweep(7e6, 0.01)
    z = noisy(oxide(f), 1e-3, 2)
    band = (f > 2e6) & (f < 5e6)
    z[band] = z[band] * 1.05
    (finding,) = audit_spectrum(spectrum(f, z)).findings
    assert finding.code == "kk_high_frequency" and finding.severity == NOTE


def test_where_mu_stops_early_a_second_look_tells_sharp_from_broken():
    """μ 가 일찍 멈추면 decade 당 3 개로 한 번 더 본다.  날카로운 아크뿐이면
    거기서 잡음 수준이라 어긋남이 없고, 점이 틀렸으면 거기서도 어긋난다."""
    f = sweep(7e6, 0.1)
    w = 2 * np.pi * f

    def sharp(k=1.0):
        return (5 + par(2e4 * k, 1 / (1j * w * 1e-10)) + par(4e4 * k, 1 / (1j * w * 3e-8))
                + 1 / (1j * w * 1e-6))

    clean = audit_spectrum(spectrum(f, noisy(sharp(), 2e-3, 5)))
    assert clean.findings == [] and "어긋남은 없습니다" in clean.kk["reason"]
    # 1.95 % 를 "2 %" 로 반올림하면 기준(2 %)과 모순으로 읽힌다 — 소수 한 자리.
    assert re.search(r"잔차가 \d+\.\d % 라", clean.kk["reason"])

    broken = audit_spectrum(spectrum(f, noisy(np.where(f < 100, sharp(1.2), sharp()),
                                              2e-3, 5)))
    assert broken.kk["judged"] is True and "다시 보니" in broken.kk["reason"]
    assert "어긋남은 없습니다" not in broken.kk["reason"]
    (finding,) = broken.findings
    assert finding.code == "kk_violation"


def test_a_fixed_count_is_fitted_as_asked():
    f, z = is1()
    result = lin_kk(f, z.real, z.imag, m=20)
    assert result.m == 20 and result.forced and len(result.mu_trace) == 1


# -- 세 번째 실측 검수(2026-09-23 05:03) 뒤에 고친 것 ---------------------------------

def build(circuit, values, f):
    model = parse_circuit(circuit)
    return model.impedance([values[name] for name in model.parameter_names], f)


#: 실측 풀셀 #33 (260903_Poly(L&F)_60um_full_#01) 에 맞춘 값 — 대역 바닥에서 막
#: 꺾이는 꼬리.  이 꼴에서 μ 가 decade 당 1.4–2.2 개에서 멈췄다.
FULL_33 = ("L1-R0-p(R1,CPE1)-TL1",
           {"L1": 4.1e-07, "R0": 3.02, "R1": 5.94, "CPE1_Q": 0.0101, "CPE1_n": 0.342,
            "TL1_Ri": 20.3, "TL1_Re": 1e-3, "TL1_Rct": 0.0446, "TL1_Q": 5.87e-05,
            "TL1_n": 0.99, "TL1_Wr": 2.02, "TL1_Wn": 0.716, "TL1_Wt": 14.7})
#: 실측 B17 #2 — 대역 아래로 이어지는 막는 CPE 꼬리 (n = 0.88).
TAIL_B17 = ("L1-R0-p(R1,CPE1)", {"L1": 1.7e-6, "R0": 5.91, "R1": 1.11e5,
                                 "CPE1_Q": 2.59e-06, "CPE1_n": 0.88})


@pytest.mark.parametrize("seed", range(4))
def test_a_full_cell_the_mu_fit_starves_is_not_called_drifting(seed):
    """KK 를 만족하게 만든 풀셀인데 μ 크기의 맞춤은 저주파 끝이 2–5 % 어긋났다 —
    실측 검수의 "측정 중에 셀이 변했습니다" 여덟 개 중 이 꼴이 섞여 있었다.
    소자가 모자란 맞춤은 멀쩡한 스펙트럼을 무효로 부른다 (논문 그림 3)."""
    f = sweep(7e6, 0.01)
    z = noisy(build(*FULL_33, f), 2.9e-3, seed)
    audit = audit_spectrum(spectrum(f, z))
    assert not [one for one in audit.findings if one.code.startswith("kk_")]


@pytest.mark.parametrize("seed", range(4))
def test_a_cpe_tail_that_goes_on_below_the_band_is_not_a_flying_point(seed):
    """대역 안에만 시정수를 두면 가장 낮은 점이 2 % 어긋난다 — 두 번째 보기는
    대역 밖 1/4 decade 까지 둔다."""
    f = sweep(7e6, 10)
    z = noisy(build(*TAIL_B17, f), 2e-3, seed)
    assert not [one for one in audit_spectrum(spectrum(f, z)).findings
                if one.code.startswith("kk_")]


def test_extend_puts_time_constants_beyond_the_band():
    f = sweep(7e6, 10)
    z = build(*TAIL_B17, f)
    inside = lin_kk(f, z.real, z.imag, m=18)
    wider = lin_kk(f, z.real, z.imag, m=18, extend=0.25)
    lowest = int(np.argmin(inside.frequency_hz))
    assert wider.residual[lowest] < inside.residual[lowest] / 2


def test_a_large_low_frequency_drift_survives_the_second_look():
    """두 번째 보기가 진짜 드리프트까지 지우면 안 된다 — 가장 낮은 decade 에서
    임피던스가 20 % 까지 커진 풀셀은 여전히 저주파 끝에서 어긋난다."""
    f = sweep(7e6, 0.01)
    ramp = np.clip(np.log10(0.1 / f), 0, None) * 0.20
    z = noisy(build(*FULL_33, f) * (1 + ramp), 2.9e-3, 1)
    (finding,) = [one for one in audit_spectrum(spectrum(f, z)).findings
                  if one.code.startswith("kk_")]
    assert finding.code == "kk_violation" and finding.severity == CHECK
    assert finding.message.startswith("저주파 끝 0.01")


def test_a_noisy_rising_tail_still_brings_its_capacitor():
    """실측 풀셀 #1 꼴, 잡음 0.42 %.  이 뽑기에서는 가장 낮은 세 점이 차례로
    오르지 않는다 (잡음) — 옛 규칙은 C 를 빼서 6.4 % 를 냈다."""
    f = sweep(7e6, 0.01)
    values = {"L1": 3.28e-07, "R0": 9.7, "R1": 30.6, "CPE1_Q": 4.79e-05, "CPE1_n": 0.852,
              "TL1_Ri": 10.6, "TL1_Re": 1e-3, "TL1_Rct": 45.6, "TL1_Q": 0.0142,
              "TL1_n": 0.347, "TL1_Wr": 3.56, "TL1_Wn": 0.8, "TL1_Wt": 7.7}
    z = noisy(build("L1-R0-p(R1,CPE1)-TL1", values, f), 4.2e-3, 7)
    lowest = -z.imag[np.argsort(f)[:3]]
    assert not np.all(np.diff(lowest) < 0)          # 옛 규칙이 깨지는 뽑기
    result = lin_kk(f, z.real, z.imag)
    assert result.with_capacitance and result.max_residual < 0.03


def test_a_step_at_a_current_range_switch_is_named_as_the_instrument():
    """100 Hz 에서 기기의 전류 범위가 바뀌며 이득이 4 % 뛴 스펙트럼.  EC-Lab 의
    ``I Range`` 가 있으면 그 자리를 짚고 (참고), 없으면 가운데의 어긋남이다."""
    f = sweep(1e6, 0.01)
    z = noisy(oxide(f), 1e-3, 0)
    z = np.where(f < 100, z * 1.04, z)
    switched = Spectrum(f, z.real, z.imag, columns={"I Range": np.where(f < 100, 3, 4)})
    audit = audit_spectrum(switched)
    (finding,) = audit.findings
    assert finding.code == "kk_range_switch" and finding.severity == NOTE
    assert "전류 범위가 89.1 Hz 에서 바뀐 자리" in finding.message
    assert audit.kk["range_switches_hz"] == [pytest.approx(89.1, rel=1e-3)]
    (plain,) = audit_spectrum(spectrum(f, z)).findings
    assert plain.code == "kk_violation" and "셀·접촉이 바뀌었거나" in plain.message


def _residuals(f, bumps):
    """A KK result whose residual is 0.1 % everywhere but at ``bumps``."""
    residual = np.full(f.size, 1e-3)
    for at, size in bumps.items():
        residual[int(np.argmin(np.abs(f - at)))] = size
    result = KKResult(judged=True, frequency_hz=f, residual_re=residual,
                      residual_im=np.zeros(f.size))
    summary = {"max_residual": float(residual.max()), "sigma": 1e-3}
    return result, summary


def test_the_low_end_is_the_lowest_point_not_half_a_decade():
    """실측 B13 #2: 25–51 Hz 가 어긋났고 그 아래 10–20 Hz 는 멀쩡했다.  드리프트는
    가장 늦게 잰 가장 낮은 점에서 가장 크다 — 가운데의 어긋남이다."""
    f = sweep(7e6, 10)
    result, summary = _residuals(f, {25.3: 0.03, 31.9: 0.04, 40.2: 0.035, 50.8: 0.03})
    (finding,) = _kk_findings(result, summary)
    assert finding.code == "kk_violation" and not finding.message.startswith("저주파 끝")

    result, summary = _residuals(f, {10: 0.03})
    (finding,) = _kk_findings(result, summary)
    assert finding.code == "kk_outlier" and finding.message.startswith("가장 낮은 점 10 Hz")

    result, summary = _residuals(f, {80.7: 0.03, 102: 0.035})
    (finding,) = _kk_findings(result, summary, switches=[95.0])
    assert finding.code == "kk_range_switch"


# -- 네 번째 실측 검수(2026-09-23 05:38) 뒤에 고친 것 ---------------------------------

def test_a_wide_low_end_drift_is_not_put_on_one_range_switch():
    """실측 풀셀 #15·#33·#34·#49: 저주파 끝 0.01–1.6 Hz (두 decade) 가 어긋났고
    그 안 0.14 Hz 에서 전류 범위가 바뀌었다.  이 기기는 전류가 한 decade 바뀔
    때마다 범위를 바꿔 넓은 구간 안에는 거의 늘 전환이 있다 — 전환 하나로 두
    decade 를 "기기 탓" (참고) 으로 돌리지 않는다.  확인으로 남기고 전환은 곁들인다."""
    f = sweep(7e6, 0.01)
    result, summary = _residuals(f, dict.fromkeys(f[f < 1.7], 0.05))
    (finding,) = _kk_findings(result, summary, switches=[0.141])
    assert finding.code == "kk_violation" and finding.severity == CHECK
    assert finding.message.startswith("저주파 끝 0.01")
    assert "그 근처 0.141 Hz 에서 기기의 전류 범위도 바뀌었습니다" in finding.message

    # 가운데라도 두 decade 넓이면 전환 하나의 흔적이 아니다.
    result, summary = _residuals(f, dict.fromkeys(f[(f > 1) & (f < 100)], 0.04))
    (finding,) = _kk_findings(result, summary, switches=[9.0])
    assert finding.code == "kk_violation" and "셀·접촉이 바뀌었거나" in finding.message
    assert "그 근처 9 Hz 에서 기기의 전류 범위도 바뀌었습니다" in finding.message

    # 저주파 끝의 점 하나는 원래대로 참고 — 옆의 전환을 함께 적는다.
    result, summary = _residuals(f, {0.01: 0.03})
    (finding,) = _kk_findings(result, summary, switches=[0.0112])
    assert finding.code == "kk_outlier" and finding.severity == NOTE
    assert "바로 옆 0.0112 Hz 에서" in finding.message

    # 한 decade 안의 가운데 구간은 그대로 전환의 흔적이다 (실측 #106: 80.7–410 Hz).
    result, summary = _residuals(f, dict.fromkeys(f[(f > 80) & (f < 420)], 0.03))
    (finding,) = _kk_findings(result, summary, switches=[90.6])
    assert finding.code == "kk_range_switch" and finding.severity == NOTE


def test_a_second_look_within_the_noise_does_not_say_there_is_no_deviation():
    """실측 B11 0 °C: "잔차가 25.0 % 라 어긋남은 없습니다".  25 % 가 기준(2 %) 을
    넘는데 판정이 안 난 것은 잡음(σ) 의 여섯 배 안이라서다 — 그렇게 말한다."""
    f = sweep(7e6, 0.1)
    w = 2 * np.pi * f
    sharp = 5 + par(2e4, 1 / (1j * w * 1e-10)) + par(4e4, 1 / (1j * w * 3e-8)) \
        + 1 / (1j * w * 1e-6)
    audit = audit_spectrum(spectrum(f, noisy(sharp, 1e-2, 0)))
    assert audit.kk["max_residual"] >= 0.02
    assert not [one for one in audit.findings if one.code.startswith("kk_v")]
    reason = audit.kk["reason"]
    assert "어긋남은 없습니다" not in reason
    assert re.search(r"잔차가 \d+\.\d % 지만 잡음\(σ ≈ \d\.\d\d %\)의 여섯 배 안이라 "
                     r"어긋남으로 보지 않습니다", reason)
