"""The linear Kramers–Kronig test, and what the audit makes of it (ADR 0043).

Anchors: the paper's own synthetic spectrum (Schönleber et al. 2014, IS1:
100 Ω + 200 Ω ∥ 0.8 µF + 500 Ω ∥ Warburg 0.4 mS·s^½, 1 µHz–10 MHz, noise
|Z|/1000) and the shapes of this lab's cells.  Every noisy spectrum has a fixed
seed -- a KK verdict that depends on the draw is not a test.
"""

import numpy as np
import pytest

from wrdkit.eis.audit import CHECK, NOTE, audit_spectrum
from wrdkit.eis.kk import MU_LIMIT, _mu, lin_kk
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


def test_where_mu_stops_too_early_nothing_is_judged():
    """이상적 RC 아크 (n = 1) 와 참 저주파 유도성 루프 — KK 를 만족하는데 μ 가
    decade 당 0.5 개에서 멈춰 잔차가 수십 % 다.  '어긴다' 고 하지 않는다."""
    f = sweep(7e6, 0.1)
    w = 2 * np.pi * f
    sharp = 5 + par(2e4, 1 / (1j * w * 1e-10)) + par(4e4, 1 / (1j * w * 3e-8)) \
        + 1 / (1j * w * 1e-6)
    audit = audit_spectrum(spectrum(f, noisy(sharp, 2e-3, 5)))
    assert audit.findings == []
    assert audit.kk["judged"] is False and "일찍 멈춥니다" in audit.kk["reason"]

    f = sweep(7e6, 1e-2)
    w = 2 * np.pi * f
    loop = 4.9 + par(10.4, cpe(3.06e-5, 0.658, w)) + par(6.6, cpe(1.36e-3, 0.757, w)) \
        + par(2.0, 1j * w * 20.0)
    audit = audit_spectrum(spectrum(f, noisy(loop, 2e-3, 6)))
    assert audit.kk["judged"] is False
    assert not [one for one in audit.findings if one.code.startswith("kk_")]
    # 끝이 축 위라는 것은 KK 와 별개로 말한다 — 드리프트인지 루프인지는 사람이.
    assert [one.code for one in audit.findings] == ["low_frequency_inductive"]


def test_no_points_no_verdict():
    assert audit_spectrum(None).kk == {"judged": False, "reason": "점이 없습니다"}
