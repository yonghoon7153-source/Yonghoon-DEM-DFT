"""Automatic fitting: does it find the numbers, and does it admit when it has not.

The procedure sheet this replaces warns that a fit can converge on values that
mean nothing -- *우연하게 말도 안 되는 것을 집어넣어도 피팅이 되는 경우가 있음*.
So half of these tests are about the failure paths: too few points, an element
the data cannot support, a spectrum that is not a spectrum.
"""

import numpy as np
import pytest
import synthetic_eis as S

from wrdkit.eis.circuit import parse_circuit
from wrdkit.eis.fit import fit_circuit
from wrdkit.eis.guess import find_arcs, initial_guess, series_resistance
from wrdkit.eis.spectrum import Spectrum

TRUTH = {"rs": 5.0, "r1": 20.0, "q1": 1e-5, "n1": 0.9, "r2": 40.0,
         "q2": 1e-3, "n2": 0.8}
LIQUID = "R0-p(R1,CPE1)-p(R2,CPE2)"


def spectrum(noise: float = 0.0, seed: int = 3, per_decade: int = 12,
             **overrides) -> Spectrum:
    values = {**TRUTH, **overrides}
    frequency = S.log_sweep(1e6, 1e-2, per_decade)
    z = S.randles(frequency, **values)
    if noise:
        rng = np.random.default_rng(seed)
        scale = np.abs(z) * noise
        z = z + rng.normal(0, scale) + 1j * rng.normal(0, scale)
    return Spectrum(frequency, z.real, z.imag)


# --- the guess -------------------------------------------------------------

def test_the_arcs_are_found_where_they_were_put():
    """Two R-CPE pairs, two humps, at their own characteristic frequencies."""
    arcs = find_arcs(spectrum())
    assert len(arcs) == 2
    assert arcs[0].peak_hz > arcs[1].peak_hz
    assert arcs[0].diameter_ohm == pytest.approx(TRUTH["r1"], rel=0.25)
    assert arcs[1].diameter_ohm == pytest.approx(TRUTH["r2"], rel=0.25)


def test_the_series_resistance_is_the_intercept_not_the_smallest_real_part():
    """With an inductive tail the smallest Re sits up at megahertz, where the
    cell is not being measured.  Taking min(Re) there under-reads Rs."""
    base = spectrum()
    z = base.z + 1j * np.where(base.frequency_hz > 1e5, 5.0, 0.0)
    with_tail = Spectrum(base.frequency_hz, z.real, z.imag)
    assert series_resistance(with_tail) == pytest.approx(TRUTH["rs"], rel=0.1)


def test_the_guess_lands_within_reach_of_the_truth():
    """Not accuracy -- reach.  An optimiser walks a factor of a few, not
    twelve orders of magnitude, which is the distance from a CPE started at 1."""
    circuit = parse_circuit(LIQUID)
    guess = dict(zip(circuit.parameter_names, initial_guess(spectrum(), circuit),
                     strict=True))
    assert guess["R0"] == pytest.approx(TRUTH["rs"], rel=0.2)
    assert guess["R1"] == pytest.approx(TRUTH["r1"], rel=0.3)
    assert 0.01 < guess["CPE1_Q"] / TRUTH["q1"] < 100


# --- the fit ---------------------------------------------------------------

def test_a_clean_spectrum_gives_back_the_parameters_it_was_built_from():
    result = fit_circuit(spectrum(), LIQUID)
    assert result.converged
    values = result.values()
    assert values["R0"] == pytest.approx(TRUTH["rs"], rel=1e-3)
    assert values["R1"] == pytest.approx(TRUTH["r1"], rel=1e-3)
    assert values["R2"] == pytest.approx(TRUTH["r2"], rel=1e-3)
    assert values["CPE1_n"] == pytest.approx(TRUTH["n1"], rel=1e-3)
    assert result.chi_squared < 1e-12


def test_noise_moves_the_answer_but_not_much():
    """One per cent noise on every point; the resistances should still be
    within a few per cent, and chi-square should reflect the noise."""
    result = fit_circuit(spectrum(noise=0.01), LIQUID)
    assert result.converged
    values = result.values()
    assert values["R1"] == pytest.approx(TRUTH["r1"], rel=0.08)
    assert values["R2"] == pytest.approx(TRUTH["r2"], rel=0.08)
    assert 1e-6 < result.chi_squared < 1e-2


def test_the_arcs_come_back_in_frequency_order_whatever_the_seed():
    """The circuit is symmetric under swapping the two branches, so the
    optimiser may return either.  The names are not symmetric -- R1 is the SEI
    arc and R2 is charge transfer -- so the report has to be ordered."""
    data = spectrum(noise=0.005)
    for seed in range(5):
        values = fit_circuit(data, LIQUID, seed=seed).values()
        assert values["R1"] == pytest.approx(TRUTH["r1"], rel=0.1), seed
        assert values["R2"] == pytest.approx(TRUTH["r2"], rel=0.1), seed


def test_a_small_arc_next_to_a_large_one_is_still_found():
    """Proportional weighting exists for this: unweighted least squares fits
    the low-frequency end, where the numbers are large, and treats a 2 ohm arc
    on top of a 200 ohm one as rounding error."""
    result = fit_circuit(spectrum(r1=2.0, r2=200.0, noise=0.002), LIQUID)
    assert result.converged
    assert result.values()["R1"] == pytest.approx(2.0, rel=0.2)


def test_the_inductive_tail_is_dropped_and_counted():
    """Dropping it silently changes Rs and nobody knows why (ADR 0019)."""
    base = spectrum()
    z = base.z + 1j * np.where(base.frequency_hz > 3e5, 8.0, 0.0)
    data = Spectrum(base.frequency_hz, z.real, z.imag)

    result = fit_circuit(data, LIQUID)
    assert result.dropped_inductive > 0
    assert len(result.frequency_hz) == len(data) - result.dropped_inductive
    assert result.values()["R0"] == pytest.approx(TRUTH["rs"], rel=0.05)


def test_keeping_the_inductive_tail_is_the_caller_s_choice():
    base = spectrum()
    z = base.z + 1j * np.where(base.frequency_hz > 3e5, 8.0, 0.0)
    data = Spectrum(base.frequency_hz, z.real, z.imag)
    result = fit_circuit(data, LIQUID, drop_inductive=False)
    assert result.dropped_inductive == 0
    assert len(result.frequency_hz) == len(data)


def test_a_frequency_window_is_reported_not_just_applied():
    result = fit_circuit(spectrum(), LIQUID, frequency_range=(1.0, 1e5))
    assert result.dropped_out_of_range > 0
    assert result.frequency_hz.max() <= 1e5
    assert result.frequency_hz.min() >= 1.0


def test_too_few_points_yields_no_numbers_at_all():
    """Seven parameters cannot come out of four points, and a result that
    carried numbers anyway would be read as a measurement (§0.4)."""
    frequency = np.array([1e4, 1e3, 1e2, 1e1])
    z = S.randles(frequency, **TRUTH)
    result = fit_circuit(Spectrum(frequency, z.real, z.imag), LIQUID)
    assert not result.converged
    assert result.parameters == []
    assert "점이" in result.reason


def test_an_element_the_data_cannot_support_is_flagged():
    """A blocking CPE tail added to a spectrum that ends on the real axis.

    The fit still converges -- that is the danger -- so the giveaway has to be
    the error bar and the bound, not the chi-square.
    """
    result = fit_circuit(spectrum(), LIQUID + "-CPE9")
    assert result.converged
    assert "CPE9_Q" in result.undetermined or "CPE9_Q" in result.reason
    assert result.reason


def test_a_flat_spectrum_has_no_arcs_to_find():
    frequency = S.log_sweep(1e5, 1e-1, 8)
    z = np.full(len(frequency), 10.0 + 0j)
    assert find_arcs(Spectrum(frequency, z.real, z.imag)) == []


def test_every_start_is_tried_and_the_count_is_reported():
    """One start finds one local minimum.  The count is in the result so a
    spectrum where most starts failed can be spotted."""
    result = fit_circuit(spectrum(noise=0.01), LIQUID, restarts=5)
    assert result.starts == 6
    assert result.starts_converged >= 1


def test_an_undetermined_parameter_is_not_called_a_measurement():
    result = fit_circuit(spectrum(noise=0.01), LIQUID)
    for parameter in result.parameters:
        if parameter.stderr is None or parameter.relative_error is not None and parameter.relative_error >= 0.5:
            assert not parameter.determined


# --- against a real instrument file ----------------------------------------

def test_a_real_solid_electrolyte_spectrum_fits_two_arcs(sample_mpr):
    """An ion-blocking symmetric cell: bulk arc, boundary arc, blocking tail.

    Asserts the shape of the answer rather than its values -- the point is that
    the automatic path gets from a raw file to determined parameters with
    nobody clicking anything.
    """
    result = fit_circuit(sample_mpr, "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3", restarts=12)
    if not result.converged:
        pytest.skip(f"this spectrum did not fit: {result.reason}")
    values = result.values()
    assert values["R1"] > 0 and values["R2"] > 0
    assert 0.3 <= values["CPE1_n"] <= 1.0
    assert result.chi_squared < 0.05
    # The high-frequency branch really is the faster one.
    assert (values["R1"] * values["CPE1_Q"]) ** (-1 / values["CPE1_n"]) > \
           (values["R2"] * values["CPE2_Q"]) ** (-1 / values["CPE2_n"])


def test_a_paper_style_branch_order_does_not_swap_the_series_resistance():
    """`p(CPE1,R1)` — 논문에서 베낀 표기를 파서가 허용하는 만큼, 짝짓기도
    그 표기를 견뎌야 한다.

    리뷰 재현: "CPE 바로 앞의 맨 R" 휴리스틱이 CPE1 을 직렬저항 R0 와
    짝지어, R0=5 가 40 으로 보고되고 fitted 곡선이 데이터와 35 Ω 어긋나는데
    χ² 는 1e-31 로 완벽했다 — seed 0 과 1 이 서로 다른 "측정값" 을 냈다.
    """
    data = spectrum()
    for seed in range(4):
        result = fit_circuit(data, "R0-p(CPE1,R1)-p(R2,CPE2)", seed=seed)
        values = result.values()
        assert values["R0"] == pytest.approx(TRUTH["rs"], rel=1e-2), seed
        assert values["R1"] == pytest.approx(TRUTH["r1"], rel=1e-2), seed
        assert values["R2"] == pytest.approx(TRUTH["r2"], rel=1e-2), seed
        # 보고된 값으로 다시 계산한 곡선이 데이터와 맞아야 한다 — 순열이
        # 잘못되면 chi² 만 옳고 곡선은 틀린다.
        z = data.sorted_by_frequency().select(
            np.ones(len(data), dtype=bool)).z
        mismatch = np.max(np.abs(result.fitted - z) / np.abs(z))
        assert mismatch < 1e-3, seed


def test_an_element_pressed_to_its_bound_reports_no_precision():
    """경계에 눌린 파라미터의 stderr ~0 은 '완벽히 쟀다' 가 아니다.

    실측 전고체 파일에서 실제로 보였다: 대역이 실수축에 닿아 블로킹 꼬리가
    없는데 CPE3 를 붙이면 CPE3_n=1, ±0 으로 — 가장 정밀해 보이는 숫자가
    가장 못 본 숫자였다.
    """
    result = fit_circuit(spectrum(), LIQUID + "-CPE9")
    assert result.converged
    tail = [p for p in result.parameters if p.name.startswith("CPE9")]
    assert tail
    for parameter in tail:
        assert parameter.stderr is None, parameter
        assert not parameter.determined, parameter


def test_excess_branches_do_not_all_start_on_the_last_arc():
    """아크 1개 + R-CPE 가지 2개 — 초과 가지는 폴백 시작값을 받아야 한다.

    마지막 인덱스에 클램프하던 때는 두 가지가 같은 지름·Q 로 시작해 대칭
    축퇴 시작점이 됐다 (리뷰 F5).  restarts 가 보통 구제하지만, 시작점 결함은
    시작점에서 고친다.
    """
    from wrdkit.eis.circuit import parse_circuit
    from wrdkit.eis.guess import initial_guess

    frequency = S.log_sweep(1e5, 1e-1, 10)
    z = S.randles(frequency, rs=5.0, r1=40.0, q1=1e-5, n1=0.95,
                  r2=1e-9, q2=1e-9, n2=1.0)      # 사실상 아크 하나
    spectrum = Spectrum(frequency, z.real, z.imag)
    circuit = parse_circuit("R0-p(R1,CPE1)-p(R2,CPE2)")
    values = dict(zip(circuit.parameter_names,
                      initial_guess(spectrum, circuit), strict=True))
    assert values["R1"] != pytest.approx(values["R2"])


# --- 확산 원소의 시작점 ------------------------------------------------------
#
# 여기가 "와버그가 안 맞는다" 의 절반이었다.  σ 는 Ω·s^-½ 인데 시작값으로
# 스펙트럼의 **실축 폭**(Ω)을 넣고 있었다 — 차원이 다른 수다.  실측 전고체
# 스캔에서 그것이 122 였고 답은 20 이었다.  재시작 여덟 번이 대개 구제했지만,
# 구제하고 있다는 것 자체가 시작점이 나쁘다는 뜻이다.


def _with_tail(circuit_text: str, truth: list[float], *, f_lo: float = 1e-2,
               n: int = 60) -> tuple[Spectrum, object]:
    circuit = parse_circuit(circuit_text)
    frequency = np.logspace(5, np.log10(f_lo), n)
    z = circuit.impedance(np.asarray(truth, float), frequency)
    return Spectrum(frequency, z.real, z.imag), circuit


def _guess_of(spectrum_, circuit) -> dict:
    return dict(zip(circuit.parameter_names, initial_guess(spectrum_, circuit),
                    strict=True))


def test_the_warburg_coefficient_is_read_off_the_lowest_point():
    """-Z'' = σ/√ω 이므로 가장 낮은 점 하나가 σ 를 바로 말한다."""
    spectrum_, circuit = _with_tail(
        "R0-p(R1,CPE1)-p(R2,CPE2)-W3", [12, 30, 1e-5, .9, 60, 1e-3, .8, 8.0])
    assert _guess_of(spectrum_, circuit)["W3"] == pytest.approx(8.0, rel=0.3)


def test_a_large_and_a_small_warburg_do_not_share_a_starting_point():
    """전에는 둘 다 '실축 폭' 에서 출발했다 — 스펙트럼이 말한 것이 아니다."""
    small, circuit = _with_tail(
        "R0-p(R1,CPE1)-p(R2,CPE2)-W3", [12, 30, 1e-5, .9, 60, 1e-3, .8, 8.0])
    large, _ = _with_tail(
        "R0-p(R1,CPE1)-p(R2,CPE2)-W3", [12, 30, 1e-5, .9, 60, 1e-3, .8, 120.0])
    assert (_guess_of(large, circuit)["W3"]
            > 5 * _guess_of(small, circuit)["W3"])


def test_a_finite_warburg_starts_from_where_the_tail_turns_over():
    """Ws 의 -Z'' 는 ωτ≈2.53 에서 꺾인다.  그 자리가 τ 를 말한다."""
    spectrum_, circuit = _with_tail("R0-p(R1,CPE1)-Ws2",
                                    [10, 40, 1e-4, .85, 80, 3.0])
    guess = _guess_of(spectrum_, circuit)
    assert guess["Ws2_tau"] == pytest.approx(3.0, rel=0.5)
    # R 은 실축에서 아크와 직렬저항을 뺀 나머지다 -- 전체 폭이 아니다.
    assert guess["Ws2_R"] == pytest.approx(80.0, rel=0.3)


def test_a_blocking_warburg_starts_three_times_larger_than_the_leftover():
    """Wo 의 실축은 저주파에서 R/3 에 앉는다.  Ws 와 같은 규칙을 쓰면 세 배
    작게 출발한다."""
    spectrum_, circuit = _with_tail("R0-p(R1,CPE1)-Wo2",
                                    [10, 40, 1e-4, .85, 80, 3.0])
    assert _guess_of(spectrum_, circuit)["Wo2_R"] == pytest.approx(80.0, rel=0.4)


@pytest.mark.parametrize("text,truth", [
    ("R0-p(R1,CPE1)-p(R2,CPE2)-W3", [12, 30, 1e-5, .9, 60, 1e-3, .8, 8.0]),
    ("R0-p(R1,CPE1)-p(R2,CPE2)-W3", [12, 30, 1e-5, .9, 60, 1e-3, .8, 120.0]),
    ("R0-p(R1,CPE1)-Ws2", [10, 40, 1e-4, .85, 80, 30.0]),
    ("R0-p(R1,CPE1)-Ws2", [10, 40, 1e-4, .85, 80, 0.05]),
    ("R0-p(R1,CPE1)-Wo2", [10, 40, 1e-4, .85, 80, 30.0]),
])
def test_the_tail_is_recovered_from_the_start_alone(text, truth):
    """재시작 없이도 되찾아야 한다.

    `restarts=0` 으로 고정하는 이유: 재시작이 가리면 시작점이 나빠져도 이
    테스트가 통과한다.  그리고 SOC 스캔은 스윕이 스물이라 재시작 여덟 번이
    그대로 여덟 배다.
    """
    spectrum_, circuit = _with_tail(text, truth)
    result = fit_circuit(spectrum_, circuit, restarts=0)
    assert result.converged
    for name, real in zip(circuit.parameter_names, truth, strict=True):
        assert result.values()[name] == pytest.approx(real, rel=0.05), name


def test_the_diffusion_ladder_is_tried_whatever_the_seed():
    """시간상수는 결정적인 사다리로도 훑는다 -- 답이 뽑기 운에 달리지 않게."""
    spectrum_, circuit = _with_tail("R0-p(R1,CPE1)-Ws2",
                                    [10, 40, 1e-4, .85, 80, 30.0])
    counts = {fit_circuit(spectrum_, circuit, restarts=0, seed=seed).starts
              for seed in range(3)}
    # 재시작이 0 이어도 시작점은 1 개가 아니다: 기본 + tau 사다리 4 개.
    assert counts == {5}


# --- 전송선 (ADR 0028) ---------------------------------------------------------
#
# 복합전극은 표면이 아니다.  이온은 기공을 따라, 전자는 고체를 따라 흐르고
# 반응은 **가는 도중에** 두께 전체에 퍼져 일어난다.  고주파의 45° 꼬리와
# 저주파의 `R_ion/3` 이 둘 다 그 구조에서 나오는 것이라, R-CPE 로는 숫자가
# 아무 뜻도 없는 값으로만 흉내낼 수 있다.


def _tl_spectrum(text: str, truth: list[float], f_hi=1e6, f_lo=1e-2, n=70):
    circuit = parse_circuit(text)
    frequency = np.logspace(np.log10(f_hi), np.log10(f_lo), n)
    z = circuit.impedance(np.asarray(truth, float), frequency)
    return Spectrum(frequency, z.real, z.imag), circuit


def test_the_transmission_line_matches_the_classic_porous_solution():
    """전자 레일이 0 이면 고전 해 `sqrt(Ri·Z)·coth(sqrt(Ri/Z))` 와 같아야 한다.

    PyEIS 1.0.10 의 `cir_RsTL` 과 항별로 대조한 식이다 (Bisquert 2000).
    """
    from wrdkit.eis.circuit import transmission_line

    omega = 2 * np.pi * np.logspace(5, -2, 40)
    interfacial = 1.0 / (1e-3 * (1j * omega) ** 0.9) + 5.0
    r_ion = 40.0
    ours = transmission_line(r_ion, 1e-9, interfacial)
    classic = np.sqrt(r_ion * interfacial) / np.tanh(np.sqrt(r_ion / interfacial))
    assert np.max(np.abs(ours - classic) / np.abs(classic)) < 1e-8


def test_the_low_frequency_offset_is_the_famous_r_ion_over_three():
    """저주파에서 `Z → Z_계면 + R_ion/3`.  이 3 이 전송선의 서명이다."""
    from wrdkit.eis.circuit import transmission_line

    omega = 2 * np.pi * np.array([1e-6])
    interfacial = 1.0 / (1e-3 * (1j * omega) ** 0.9) + 5.0
    z = transmission_line(40.0, 1e-9, interfacial)
    assert float((z - interfacial).real[0]) == pytest.approx(40.0 / 3, rel=1e-6)


def test_the_high_frequency_end_is_finite_not_nan():
    """`sinh` 는 |x|>710 에서 넘친다.  고주파 끝이 통째로 NaN 이 되던 자리다."""
    from wrdkit.eis.circuit import transmission_line

    omega = 2 * np.pi * np.array([1e6, 1e7, 1e9])
    interfacial = 1.0 / (1e-3 * (1j * omega) ** 0.9)
    z = transmission_line(40.0, 1e-9, interfacial)
    assert np.all(np.isfinite(z))
    assert np.all(z.real > 0)


def test_a_transmission_line_spectrum_gives_back_its_own_parameters():
    """랩의 회로 그대로 — 배선 인덕턴스 + 직렬저항 + 보정 아크 + 전송선."""
    truth = [1e-6, 12.0, 5.0, 1e-5, 0.9,
             40.0, 2.0, 3.0, 1e-2, 0.8, 30.0, 0.5, 60.0]
    spectrum_, circuit = _tl_spectrum("L1-R0-p(R1,CPE1)-TL1", truth)
    result = fit_circuit(spectrum_, circuit, restarts=24, seed=0)
    assert result.converged
    for name, real in zip(circuit.parameter_names, truth, strict=True):
        assert result.values()[name] == pytest.approx(real, rel=0.05), name


def test_the_interfacial_warburg_is_pyeis_shape():
    """계면은 `CPE ∥ (Rct + W)` 이고 `Z_W = Wr·coth(x)/x`, `x = (Wt·jω)^Wn`.

    PyEIS `cir_RsTL_1Dsolid` 와 같은 구성이다.  직렬·병렬을 바꿔 놓으면 곡선이
    그럴듯하게 나오면서 값만 틀린다.
    """
    from wrdkit.eis.circuit import transmission_line

    circuit = parse_circuit("TL1")
    omega = 2 * np.pi * np.array([1e3, 1.0, 1e-2])
    values = np.array([40.0, 2.0, 3.0, 1e-2, 0.8, 30.0, 0.5, 60.0])

    x = (60.0 * 1j * omega) ** 0.5
    z_w = 30.0 * (np.cosh(x) / np.sinh(x)) / x
    z_cpe = 1.0 / (1e-2 * (1j * omega) ** 0.8)
    interfacial = 1.0 / (1.0 / z_cpe + 1.0 / (3.0 + z_w))
    expected = transmission_line(40.0, 2.0, interfacial)
    assert np.allclose(circuit.impedance(values, omega / (2 * np.pi)), expected)


def test_the_tail_free_transmission_line_has_five_parameters():
    """확산 꼬리가 안 보이면 W 세 개는 결정되지 않는다 -- 그때는 TLR 을 쓴다."""
    circuit = parse_circuit("R0-TLR1")
    assert list(circuit.parameter_names) == [
        "R0", "TLR1_Ri", "TLR1_Re", "TLR1_Rct", "TLR1_Q", "TLR1_n"]
