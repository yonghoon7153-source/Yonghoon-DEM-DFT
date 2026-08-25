"""DRT: how many processes, at what times, carrying how much resistance.

The inversion is ill-posed, so most of these tests are about the regularisation
weight -- that it changes the answer, that both failure modes are reachable,
and that when the L curve has no corner we say so instead of picking one (§0.4).
"""

import numpy as np
import pytest
import synthetic_eis as S

from wrdkit.eis.drt import DrtPeak, drt, find_peaks, lcurve_corner, sweep
from wrdkit.eis.spectrum import Spectrum

#: Ideal RC pairs (n = 1), so each process has one exact relaxation time:
#: tau = R Q.  A depressed arc has a *distribution*, which is the right physics
#: but the wrong fixture for checking that a known time comes back.
TWO_RC = {"rs": 5.0, "r1": 20.0, "q1": 1e-5, "n1": 1.0,
          "r2": 40.0, "q2": 1e-3, "n2": 1.0}


def two_process_spectrum(noise: float = 0.0, seed: int = 5) -> Spectrum:
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, **TWO_RC)
    if noise:
        rng = np.random.default_rng(seed)
        scale = np.abs(z) * noise
        z = z + rng.normal(0, scale) + 1j * rng.normal(0, scale)
    return Spectrum(frequency, z.real, z.imag)


def test_two_rc_pairs_come_back_as_two_peaks_at_their_own_times():
    result = drt(two_process_spectrum(), regularisation=1e-3)
    assert len(result.peaks) == 2
    fast, slow = result.peaks
    assert fast.tau_s == pytest.approx(TWO_RC["r1"] * TWO_RC["q1"], rel=0.2)
    assert slow.tau_s == pytest.approx(TWO_RC["r2"] * TWO_RC["q2"], rel=0.2)


def test_the_area_under_a_peak_is_the_resistance_it_carries():
    """This is what makes the DRT quantitative rather than a picture."""
    result = drt(two_process_spectrum(), regularisation=1e-3)
    fast, slow = result.peaks
    assert fast.resistance_ohm == pytest.approx(TWO_RC["r1"], rel=0.1)
    assert slow.resistance_ohm == pytest.approx(TWO_RC["r2"], rel=0.1)
    assert result.total_polarisation_ohm == pytest.approx(
        TWO_RC["r1"] + TWO_RC["r2"], rel=0.1)


def test_the_high_frequency_intercept_is_separated_from_the_processes():
    """R_inf is not polarisation.  Folded into gamma it would appear as a
    process at the fastest time on the grid -- an edge spike that reads real."""
    result = drt(two_process_spectrum(), regularisation=1e-3)
    assert result.r_inf_ohm == pytest.approx(TWO_RC["rs"], rel=0.1)


def test_a_peak_is_reported_at_the_frequency_a_person_would_look_for_it():
    result = drt(two_process_spectrum(), regularisation=1e-3)
    for peak in result.peaks:
        assert peak.frequency_hz == pytest.approx(1 / (2 * np.pi * peak.tau_s))


def test_over_smoothing_merges_the_two_processes():
    """The failure mode at one end.  If this stopped happening the penalty
    would have stopped doing anything, and the weight would be decoration."""
    merged = drt(two_process_spectrum(), regularisation=10.0)
    assert len(merged.peaks) < 2


def test_the_weight_changes_the_answer_which_is_why_it_is_reported():
    loose = drt(two_process_spectrum(), regularisation=1e-6)
    tight = drt(two_process_spectrum(), regularisation=1e-1)
    assert loose.chi_squared < tight.chi_squared
    assert loose.penalty_norm > tight.penalty_norm
    assert loose.regularisation != tight.regularisation


def test_gamma_never_goes_negative():
    """A negative relaxation strength is a process that supplies polarisation.

    Unconstrained, the solver buys residual with a positive spike beside a
    negative one and both get reported.
    """
    result = drt(two_process_spectrum(noise=0.01), regularisation=1e-4)
    assert np.all(result.gamma_ohm >= -1e-12)


def test_the_l_curve_corner_names_the_weight_it_chose():
    results = sweep(two_process_spectrum())
    index, reason = lcurve_corner(results)
    assert index >= 0
    assert "λ=" in reason
    assert results[index].regularisation > 0


def test_a_curve_with_no_corner_is_admitted_rather_than_guessed():
    """Three identical points have no corner.  Returning one anyway is exactly
    what the knee work stopped doing."""
    flat = sweep(two_process_spectrum(), regularisations=[1e-3])
    index, reason = lcurve_corner(flat)
    assert index == -1
    assert "많지 않습니다" in reason


def test_the_inductive_tail_is_dropped_and_counted():
    base = two_process_spectrum()
    z = base.z + 1j * np.where(base.frequency_hz > 3e5, 6.0, 0.0)
    result = drt(Spectrum(base.frequency_hz, z.real, z.imag), regularisation=1e-3)
    assert result.dropped_inductive > 0
    assert result.r_inf_ohm == pytest.approx(TWO_RC["rs"], rel=0.15)


def test_too_few_points_is_refused_with_a_reason():
    frequency = np.array([1e3, 1e2, 1e1])
    z = S.randles(frequency, **TWO_RC)
    with pytest.raises(ValueError, match="점이 더 필요합니다"):
        drt(Spectrum(frequency, z.real, z.imag))


def test_ringing_beside_a_peak_is_not_a_second_process():
    """Regularised inversions oscillate.  Without a floor a DRT plot ends up
    with nine processes, most of them one grid point wide."""
    tau = np.logspace(-6, 2, 200)
    gamma = np.exp(-((np.log10(tau) + 2) ** 2) / 0.02)
    gamma[50] = 0.005          # a ripple at half a per cent of the peak
    peaks = find_peaks(tau, gamma)
    assert len(peaks) == 1


def test_a_real_solid_electrolyte_spectrum_shows_its_two_transport_steps(sample_mpr):
    """벌크와 입계 — 회로 피팅과 **독립적으로** 같은 결론에 닿아야 한다.

    등가회로는 사람이 반원 두 개를 그려 넣고 시작하지만 DRT 는 그러지 않는다.
    두 방법이 같은 저항을 내놓으면 그 두 아크는 회로를 그린 사람의 가정이
    아니라 스펙트럼 안에 있는 것이다.
    """
    result = drt(sample_mpr, regularisation=1e-3)
    big = [peak for peak in result.peaks if peak.resistance_ohm > 1.0]
    assert len(big) >= 2
    assert big[0].frequency_hz > big[1].frequency_hz
    assert result.total_polarisation_ohm > 0


def test_a_solution_with_a_peak_outside_the_measured_band_is_not_recommended():
    """아무 주파수도 재지 않은 곳에서 "과정을 찾았다" 는 답은 추천하지 않는다.

    τ 격자는 측정 대역 밖으로 조금 넘겨 잡는다 — 대역 바로 밖의 실제 과정이
    어깨를 놓을 자리가 필요해서다.  그 연장 구간에 **봉우리**가 서 있으면
    그것은 정칙화가 막으려던 과대적합 그 자체다.

    실측 파일에서 이것이 갈랐다: 곡률 최대가 λ=1e-5 였는데 그 답에는 측정
    대역(≤1.39 MHz) 밖 2.19 MHz 봉우리가 있었다.
    """
    results = sweep(two_process_spectrum(noise=0.02))
    band = (float(np.min(results[0].frequency_hz)),
            float(np.max(results[0].frequency_hz)))
    index, reason = lcurve_corner(results)
    if index < 0:
        pytest.skip(f"이 스펙트럼에는 추천할 수 있는 λ 가 없다: {reason}")
    for peak in results[index].peaks:
        assert band[0] <= peak.frequency_hz <= band[1], reason


def _fake_lcurve() -> list:
    """A hand-made L curve whose corner is known.

    Built rather than measured so the test says one thing.  The residual is
    flat along the first arm and the penalty is flat along the second, so the
    sharpest bend is unambiguously at index 2 -- and that is where the
    out-of-band peak is planted.
    """
    from wrdkit.eis.drt import DrtResult

    shape = [(1e-6, 1.00, 0.010), (1e-5, 0.98, 0.011), (1e-4, 0.95, 0.013),
             (1e-3, 0.60, 0.10), (1e-2, 0.30, 0.40), (1e-1, 0.20, 0.90)]
    band = np.array([1e5, 1e0, 1e-2])
    out = []
    for regularisation, penalty, residual in shape:
        result = DrtResult(tau_s=np.array([1e-4, 1e-2, 1.0]),
                           gamma_ohm=np.array([1.0, 2.0, 0.5]))
        result.regularisation = regularisation
        result.penalty_norm = penalty
        result.residual_norm = residual
        result.frequency_hz = band
        result.peaks = [DrtPeak(tau_s=1e-2, frequency_hz=15.9, gamma_ohm=2.0,
                                resistance_ohm=10.0, tau_low_s=1e-3,
                                tau_high_s=1e-1)]
        out.append(result)
    return out


def test_the_corner_moves_off_a_candidate_with_an_out_of_band_peak():
    clean = _fake_lcurve()
    corner, _ = lcurve_corner(clean)

    planted = _fake_lcurve()
    planted[corner].peaks = list(planted[corner].peaks) + [DrtPeak(
        tau_s=1e-9, frequency_hz=1e7, gamma_ohm=1.0, resistance_ohm=1.0,
        tau_low_s=1e-10, tau_high_s=1e-8)]
    moved, reason = lcurve_corner(planted)

    assert moved != corner
    assert "측정 대역 밖" in reason
    assert "1e+07 Hz" in reason


def test_when_every_candidate_is_out_of_band_none_is_recommended():
    """하나를 골라 주는 것보다 못 고르겠다고 하는 편이 낫다 (§0.4)."""
    results = _fake_lcurve()
    for result in results:
        result.peaks = [DrtPeak(tau_s=1e-9, frequency_hz=1e7, gamma_ohm=1.0,
                                resistance_ohm=1.0, tau_low_s=1e-10,
                                tau_high_s=1e-8)]
    index, reason = lcurve_corner(results)
    assert index == -1
    assert "모든 후보" in reason
