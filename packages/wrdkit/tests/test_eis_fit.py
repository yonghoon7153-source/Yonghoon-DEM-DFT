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
from wrdkit.eis.fit import Parameter, fit_circuit
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
    spectrum where most starts failed can be spotted.

    기본 추측 1 + 순차 피팅 1 + 재시작 5.  (이 회로에는 폭넓은 파라미터가
    없어 사다리 항이 붙지 않는다.)
    """
    result = fit_circuit(spectrum(noise=0.01), LIQUID, restarts=5)
    assert result.starts == 7
    assert result.starts_converged >= 1


def test_an_undetermined_parameter_is_not_called_a_measurement():
    result = fit_circuit(spectrum(noise=0.01), LIQUID)
    for parameter in result.parameters:
        if parameter.stderr is None or parameter.relative_error is not None and parameter.relative_error >= 0.5:
            assert not parameter.determined


# --- the error bar is not the whole story ----------------------------------

def test_the_determined_rule_reads_both_the_error_bar_and_the_scatter():
    """세 갈래로 떨어진다.  **전부** 통과해야 '쟀다' 고 적는다."""
    # 오차 막대만 보던 규칙 — 여전히 유효하다.
    assert Parameter("R0", 10.0, stderr=1.0, spread=1.1).determined
    assert not Parameter("R0", 10.0, stderr=6.0, spread=1.1).determined
    # 야코비안이 특이하면 그 자체가 발견이다: 이 값은 맞춤을 안 바꾼다.
    assert not Parameter("R0", 10.0).determined

    # 흩어짐이 더해진다.
    assert Parameter("R0", 10.0, stderr=1.0, spread=2.9).determined
    assert not Parameter("R0", 10.0, stderr=1.0, spread=3.0).determined
    assert not Parameter("R0", 10.0, stderr=1.0, spread=1e9).determined

    # **못 본 것(None)도 통과를 막는다.**  전에는 통과시켰는데, 그것이
    # 검사가 안 돈 수를 총저항·전도도·추세·클립보드로 흘려보냈다.
    assert not Parameter("R0", 10.0, stderr=1.0, spread=None).determined



def _flat_valley_spectrum():
    """전고체 풀셀 모양 — `Rct` 가 측정창에 안 보이게 작다.

    랩의 Dry_2 에서 본 것을 합성으로 재현한 것이다: chi^2 는 소수점 셋째
    자리까지 같은데 `Rct` 는 씨앗을 바꿀 때마다 자릿수로 움직였고, 그래도
    +-1sigma 는 ±10% 로 나왔다.
    """
    circuit = "L1-R0-p(R1,CPE1)-TL1"
    truth = {"L1": 1e-6, "R0": 12.0, "R1": 6.0, "CPE1_Q": 2e-5, "CPE1_n": 0.85,
             "TL1_Ri": 30.0, "TL1_Re": 1.0, "TL1_Rct": 0.05, "TL1_Q": 3e-3,
             "TL1_n": 0.8, "TL1_Wr": 40.0, "TL1_Wn": 0.5, "TL1_Wt": 20.0}
    model = parse_circuit(circuit)
    values = np.array([truth[name] for name in model.parameter_names], float)
    frequency = np.logspace(np.log10(7e6), np.log10(0.05), 60)
    z = model.impedance(values, frequency)
    rng = np.random.default_rng(7)
    z = z * (1 + rng.normal(0, 0.004, z.shape) + 1j * rng.normal(0, 0.004, z.shape))
    return circuit, Spectrum(frequency_hz=frequency, z_re=z.real, z_im=z.imag)


def test_a_flat_valley_is_undetermined_even_with_a_small_error_bar():
    """±1σ 가 작아도, 씨앗을 바꾸면 값이 자릿수로 움직이면 측정이 아니다.

    오차 막대는 해 **한 점**의 곡률이다.  데이터가 못 잡는 파라미터는 긴
    평평한 골짜기에 앉아 있고, 골짜기를 가로지르는 곡률은 어디서 멈추든
    작으므로 sigma 는 작게 나온다.  실측에서 `Rct = 0.5807 ± 0.2217`
    (상대오차 0.38 — 넉넉히 '결정됨') 이 그렇게 통과했다.
    """
    circuit, data = _flat_valley_spectrum()
    result = fit_circuit(data, circuit, seed=0)
    assert result.converged

    rct = next(p for p in result.parameters if p.name == "TL1_Rct")
    # 옛 규칙(±1σ 만)이라면 통과했을 값이다 -- 그것이 이 시험의 요점이다.
    assert rct.relative_error is not None and rct.relative_error < 0.5
    # 새 규칙: 같은 chi^2 에 닿은 시작점들 사이에서 자릿수로 움직였다.
    assert rct.spread is not None and rct.spread > 100
    assert not rct.determined
    assert "TL1_Rct" in result.undetermined


def test_the_scatter_check_does_not_downgrade_a_parameter_that_holds_still():
    """한쪽으로만 틀린다 — 못 보고 지나칠 수는 있어도 없는 흩어짐을 만들지 않는다."""
    circuit, data = _flat_valley_spectrum()
    result = fit_circuit(data, circuit, seed=0)
    for name in ("CPE1_n", "TL1_n", "R1"):
        parameter = next(p for p in result.parameters if p.name == name)
        assert parameter.spread is None or parameter.spread < 3.0, parameter
        assert parameter.determined, parameter


def test_scatter_is_none_when_there_was_nothing_to_compare_against():
    """§0.4 — 하나뿐이었으면 '안 움직인다' 가 아니라 '못 봤다' 다.

    그리고 **어느 쪽으로** 못 봤는지까지 적는다 (Codex 판정 리뷰 #4).
    다듬은 답이 하나뿐인 것과, 여럿인데 같은 답으로 볼 것이 하나뿐인 것은
    사람이 할 다음 일이 다르다 — 앞은 재시작을 늘리는 일이고 뒤는 왜 답들이
    갈렸는지 보는 일이다.
    """
    from wrdkit.eis.fit import _seed_spread

    model = parse_circuit(LIQUID)
    one = [(1e-6, np.ones(len(model.parameter_names)))]
    got = _seed_spread(model, one, 1e-6, 24)
    assert all(one.ratio is None for one in got)
    assert {one.reason for one in got} == {"one_polished_solution"}

    # 여럿인데 하나만 "같은 답" 인 경우 — 사유가 다르다.
    far = [(1e-6, np.ones(len(model.parameter_names))),
           (5e-1, np.full(len(model.parameter_names), 9.0))]
    got = _seed_spread(model, far, 1e-6, 24)
    assert {one.reason for one in got} == {"no_comparable_solution"}

    # 못 잰 것은 통과시키지 않는다 — 그것이 이 검사의 요점이다.
    assert not Parameter("R0", 10.0, stderr=0.1, spread=None,
                         spread_missing="one_polished_solution").determined


def test_a_near_zero_cost_fit_still_finds_its_ties():
    """비율만으로 "같은 답" 을 재면 chi^2 가 0 에 가까울 때 무너진다.

    합성 스펙트럼은 cost 가 1e-30 까지 내려간다.  그때 `best * 1.05` 도
    1e-30 이라 **수치적으로 같은** 답들이 창 밖으로 떨어졌다 — 시작점 10/10 이
    수렴했는데 파라미터 일곱이 전부 "비교할 답이 하나뿐" 으로 나왔다
    (Codex 판정 리뷰 #4).  절대 바닥이 그것을 막는다.
    """
    frequency = np.logspace(6, -2, 97)
    z = np.full(97, 500.0, dtype=complex)
    for r, q, n in ((20.0, 1e-5, 0.9), (40.0, 1e-3, 0.8)):
        z = z + 1 / (1 / r + q * (1j * 2 * np.pi * frequency) ** n)
    result = fit_circuit(Spectrum(frequency, z.real, z.imag), LIQUID)
    assert result.chi_squared < 1e-20          # 사실상 정확히 맞았다
    assert result.starts_converged >= 2        # 견줄 답이 여럿 있었다
    measured = [p for p in result.parameters if p.spread is not None]
    assert len(measured) == len(result.parameters), [
        (p.name, p.spread_missing) for p in result.parameters]
    # 전부 같은 답으로 모였으므로 흩어짐은 1 에 가깝고, 그래서 결정된다.
    assert all(p.determined for p in result.parameters)


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
    # 재시작이 0 이어도 시작점은 1 개가 아니다: 기본 + tau 사다리 4 개 +
    # 순차 피팅 1 개.
    assert counts == {6}


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
    """랩의 회로 그대로 — 배선 인덕턴스 + 직렬저항 + 보정 아크 + 전송선.

    두 레일만 **짝으로** 본다.  `transmission_line` 은 `Ri` 와 `Re` 를 맞바꿔도
    정확히 같은 곡선을 내므로 (차이 0.0), 어느 쪽이 어느 쪽인지는 스펙트럼에
    없는 정보다 -- 그것을 요구하는 테스트는 실은 최적화의 출발점 난수를
    고정하고 있을 뿐이다.
    """
    truth = [1e-6, 12.0, 5.0, 1e-5, 0.9,
             40.0, 2.0, 3.0, 1e-2, 0.8, 30.0, 0.5, 60.0]
    spectrum_, circuit = _tl_spectrum("L1-R0-p(R1,CPE1)-TL1", truth)
    result = fit_circuit(spectrum_, circuit, restarts=24, seed=0)
    assert result.converged
    rails = {"TL1_Ri", "TL1_Re"}
    for name, real in zip(circuit.parameter_names, truth, strict=True):
        if name in rails:
            continue
        assert result.values()[name] == pytest.approx(real, rel=0.05), name

    got = sorted(result.values()[name] for name in rails)
    for value, real in zip(got, sorted([40.0, 2.0]), strict=True):
        assert value == pytest.approx(real, rel=0.05)
    # 그리고 그 사실을 결과가 말한다 -- 두 줄을 서로 다른 측정값처럼 읽으면 안 된다.
    assert "TL1_Ri ↔ TL1_Re" in result.reason


def test_every_element_draws_a_smooth_curve_across_its_own_bounds():
    """경계 안의 어떤 값에서도 곡선이 **매끄러워야** 한다.

    이 검사가 없어서 놓친 것: ``TL`` 의 ``Wn`` 상한이 1.0 이었고, 거기서
    ``x = (Wt·jω)^1`` 이 순허수가 되어 ``coth`` 가 극점의 열이 된다.  확산이
    아니라 무손실 선로이고, 나이퀴스트 곡선이 저주파에서 톱니로 꺾인다.
    적합도만 보면 그것이 이득이라 최적화가 상한에 눌러붙었고, 사람이 화면에서
    톱니를 보고 나서야 알았다.

    "매끄럽다" 는 **이웃 걸음과 견줘서** 정한다.  저주파에서 임피던스가 크게
    발산하는 것은 정상이므로 (블로킹 전극), 절대 크기로 재면 정상까지 걸린다.
    """
    from wrdkit.eis.circuit import ELEMENTS, parse_circuit

    frequency = np.logspace(7, -2, 400)
    rng = np.random.default_rng(0)
    for kind in ELEMENTS:
        circuit = parse_circuit(f"{kind}1")
        lower = np.maximum(np.asarray(circuit.lower), 1e-9)
        upper = np.minimum(np.asarray(circuit.upper), 1e6)
        worst, worst_values = 0.0, None
        for _ in range(200):
            values = 10 ** rng.uniform(np.log10(lower), np.log10(upper))
            z = circuit.impedance(values, frequency)
            assert np.all(np.isfinite(z)), (kind, values)
            step = np.abs(np.diff(z))
            neighbours = np.maximum(step[:-2], step[2:])
            # 곡선이 사실상 상수인 조합이 있다 (Rct 가 0 에 가까우면 전송선이
            # 주파수를 안 탄다).  거기서는 걸음이 전부 부동소수점 먼지라
            # 비율이 아무 뜻도 없으므로, 곡선 크기에 견줘 의미 있는 걸음만 센다.
            worth = step[1:-1] > 1e-9 * np.abs(z).max()
            ratio = np.where(worth & (neighbours > 0),
                             step[1:-1] / np.where(neighbours > 0, neighbours, 1.0),
                             0.0)
            if ratio.max() > worst:
                worst, worst_values = float(ratio.max()), values
        # 매끄러운 곡선은 1 근처다.  Wn=1.0 이던 시절의 TL 은 15.6 이었다.
        assert worst < 3.0, (kind, worst, worst_values)


def test_every_diffusion_circuit_gets_the_wide_ladder():
    """자릿수를 넘나드는 파라미터가 있으면 **회로를 가리지 않고** 사다리를 탄다.

    이것이 없어서 놓친 것: 사다리 대상을 `_tau` 와 반무한 `W` 의 σ 로만 봤고,
    전송선의 시간상수는 이름이 `_Wt` 라 통째로 빠졌다.  화면에 그대로 찍혔다 --
    파라미터 아홉 개짜리 `Ws` 회로는 `시작점 29`, **열세 개**짜리 `TL` 회로는
    `시작점 9`.  더 험한 지형을 더 적은 시작점으로 훑고 있었다.
    """
    from wrdkit.eis.circuit import parse_circuit
    from wrdkit.eis.fit import _is_wide

    for text in ("R0-p(R1,CPE1)-W2", "R0-p(R1,CPE1)-Ws2", "R0-p(R1,CPE1)-Wo2",
                 "L1-R0-p(R1,CPE1)-TL1", "R0-TL1"):
        model = parse_circuit(text)
        wide = [name for name in model.parameter_names if _is_wide(model, name)]
        assert wide, f"{text}: 확산이 있는데 사다리 대상이 없다"

    # 확산이 없는 회로는 사다리도 필요 없다 -- 있으면 시작점만 늘어난다.
    plain = parse_circuit("R0-p(R1,CPE1)-p(R2,CPE2)")
    assert not [n for n in plain.parameter_names if _is_wide(plain, n)]


def test_a_harder_circuit_does_not_get_fewer_starts():
    """파라미터가 많을수록 지형이 험한데, 예전에는 그쪽이 시작점이 적었다."""
    spectrum_, _ = _tl_spectrum("L1-R0-p(R1,CPE1)-TL1",
                                [1e-6, 12.0, 5.0, 1e-5, 0.9,
                                 40.0, 2.0, 3.0, 1e-2, 0.8, 30.0, 0.5, 60.0])
    easy = fit_circuit(spectrum_, "R0-p(R1,CPE1)-Ws2")
    hard = fit_circuit(spectrum_, "L1-R0-p(R1,CPE1)-TL1")
    assert hard.starts >= easy.starts


def test_the_diffusion_exponent_stops_below_the_pole_line():
    """``Wn`` 상한은 취향이 아니라 ``coth`` 의 극점이 시작되는 자리다.

    ``Im x / Re x = tan(Wn·π/2)`` 이므로, ``tan(Wn·π/2) < π`` 이면 ``Im x`` 가
    π 를 넘는 순간 ``Re x`` 도 1 을 넘어 극점에 닿을 수 없다.  경계는
    ``2·atan(π)/π = 0.8038``.
    """
    from wrdkit.eis.circuit import ELEMENTS

    index = ELEMENTS["TL"].suffixes.index("_Wn")
    _, upper = ELEMENTS["TL"].bounds[index]
    assert upper <= 2 * np.arctan(np.pi) / np.pi


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


# --- ZView 관행: 순차 피팅과 대역 끝 경고 ----------------------------------

def test_series_blocks_follows_the_written_order():
    """직렬로 쓴 순서 그대로 나눈다 — 순차 피팅이 그 순서를 밟는다."""
    from wrdkit.eis.circuit import series_blocks

    blocks = series_blocks(parse_circuit("R0-p(R1,CPE1)-p(R2,CPE2)-Ws1"))
    assert [name for name, _ in blocks] == ["R0", "R1+CPE1", "R2+CPE2", "Ws1"]
    assert [indices for _, indices in blocks] == [(0,), (1, 2, 3), (4, 5, 6), (7, 8)]

    # 나눌 것이 없는 회로도 답이 있어야 한다 — 부르는 쪽이 예외를 안 받는다.
    assert [n for n, _ in series_blocks(parse_circuit("R0"))] == ["R0"]
    assert [n for n, _ in series_blocks(parse_circuit("p(R1,CPE1)"))] == ["R1+CPE1"]


def test_staged_start_walks_the_blocks_and_lands_near_the_answer():
    """사람이 ZView 에서 하는 것 — 고주파부터 원소를 하나씩 풀어 간다.

    여기서 고정하는 것은 "쓸 만한 시작점이 나온다" 이지 "이것이 답이다" 가
    아니다.  값은 다중시작 주머니에 하나로 들어가고, 전체 스펙트럼에서 이긴
    것이 답이 된다 (`_staged_start` 머리말).
    """
    from scipy.optimize import least_squares

    from wrdkit.eis.fit import _residuals, _staged_start

    data = spectrum()
    model = parse_circuit(LIQUID)
    weights = 1.0 / np.abs(data.z)
    guess = initial_guess(data, model)
    staged = _staged_start(model, data.frequency_hz, data.z, weights, guess,
                           least_squares)
    assert staged is not None

    def cost(values):
        return float(np.sum(_residuals(values, model, data.frequency_hz,
                                       data.z, weights) ** 2))

    # 시작점으로서 처음 추측보다 나쁘지 않아야 뜻이 있다.
    assert cost(staged) <= cost(guess)
    # 그리고 값 자체가 답 근처여야 한다.  잡음 없는 합성이라 여기서는 사실상
    # 답에 닿는데, 두 비용이 모두 부동소수 0 이라 비율로는 못 잰다.
    truth = {"R0": TRUTH["rs"], "R1": TRUTH["r1"], "CPE1_Q": TRUTH["q1"],
             "CPE1_n": TRUTH["n1"], "R2": TRUTH["r2"], "CPE2_Q": TRUTH["q2"],
             "CPE2_n": TRUTH["n2"]}
    got = dict(zip(model.parameter_names, staged, strict=True))
    for name, want in truth.items():
        assert got[name] == pytest.approx(want, rel=0.05), name


def test_staged_start_says_no_when_there_is_nothing_to_stage():
    """블록이 하나면 순서가 없다.  억지로 한 판 더 돌리지 않는다."""
    from scipy.optimize import least_squares

    from wrdkit.eis.fit import _staged_start

    data = spectrum()
    model = parse_circuit("p(R1,CPE1)")
    assert _staged_start(model, data.frequency_hz, data.z,
                         1.0 / np.abs(data.z), initial_guess(data, model),
                         least_squares) is None


def test_staged_start_never_makes_the_answer_worse():
    """주머니에 하나 더 넣는 것이므로, 켜고 끈 결과가 나빠질 수는 없다."""
    data = spectrum(noise=0.01)
    with_staged = fit_circuit(data, LIQUID)

    import wrdkit.eis.fit as module
    real = module._staged_start
    module._staged_start = lambda *args, **kwargs: None
    try:
        without = fit_circuit(data, LIQUID)
    finally:
        module._staged_start = real
    # 같거나 낫다.  수치 오차만큼의 여유를 준다.
    assert with_staged.chi_squared <= without.chi_squared * 1.000001
def test_edge_misfit_measures_and_names_a_threshold_to_type():
    """재는 것과 문장으로 말하는 것을 나눠 둔다 — API 도 같은 자를 쓴다."""
    from wrdkit.eis.fit import _edge_misfit_note, edge_misfit

    frequency = S.log_sweep(1e5, 1e-2, 6)
    total = len(frequency)
    order = np.argsort(frequency)
    z = 5.0 + 20.0 / (1.0 + 1j * 2 * np.pi * frequency * 1e-3)

    # 어디나 조금씩 어긋난 곡선에는 할 말이 없다.
    assert edge_misfit(frequency, z, z * 1.01) is None
    assert _edge_misfit_note(None) == ""

    # 저주파 끝만 크게 어긋난 곡선.
    fitted = z * 1.001
    take = max(3, total // 10)
    fitted[order[:take]] = z[order[:take]] * 2.0
    edge = edge_misfit(frequency, z, fitted)
    assert edge is not None
    assert edge.count == take
    assert edge.share > 0.5
    assert edge.upper_hz == pytest.approx(float(frequency[order[take - 1]]))
    # 문턱은 뺄 것의 맨 위와 남길 것의 맨 아래 **사이**다.
    assert frequency[order[take - 1]] < edge.threshold_hz < frequency[order[take]]
    assert "하한을" in _edge_misfit_note(edge)

    # 길이가 안 맞거나 점이 적으면 아무 말도 하지 않는다.
    assert edge_misfit(frequency, z, fitted[:-1]) is None
    assert edge_misfit(frequency[:8], z[:8], fitted[:8]) is None


# --- 배선 인덕턴스 (실측 2026-08-27) ---------------------------------------

def test_the_wiring_inductance_bends_the_points_below_the_crossover_too():
    """유도성 점을 빼도 **그 아래 점들이 이미 휘어 있다.**

    7 MHz 까지 재면 케이블·셀 홀더의 인덕턴스가 고주파 점을 실수축 위로
    밀어 올린다.  올라간 점은 우리가 뺀다 (`drop_inductive`) -- 셀의 것이
    아니니까.  그런데 **인덕턴스의 영향은 거기서 끊기지 않는다**: 교차점
    아래로도 한두 십년대에 걸쳐 아크를 왼쪽 위로 당긴다.

    `L` 없는 회로로 맞추면 모델이 그 굽이를 **첫 아크를 찌그러뜨려** 흉내낸다.
    화면에서는 "반원 두 개가 안 나온다" 로 보인다 — 실측 하프셀 SOC 스캔
    11스윕 전부에서 최대오차가 12–15 % 였고, 그 오차가 전부 고주파 끝에
    몰려 있었다.  `L1` 을 넣으면 2–4 % 가 된다.
    """
    frequency = S.log_sweep(7e6, 1e-2, 10)
    model = parse_circuit("L1-" + LIQUID)
    truth = [8e-7, 5.0, 20.0, 1e-5, 0.7, 40.0, 1e-3, 0.8]
    z = model.impedance(np.array(truth), frequency)
    made = Spectrum(frequency, z.real, z.imag)

    def worst(circuit: str) -> float:
        best = None
        for seed in range(3):
            result = fit_circuit(made, circuit, restarts=32, seed=seed)
            used = np.isin(frequency, result.frequency_hz)
            deviation = (np.abs(result.fitted - z[used]) / np.abs(z[used])).max()
            best = deviation if best is None else min(best, deviation)
        return float(best)

    without = worst(LIQUID)
    with_l = worst("L1-" + LIQUID)
    # 인덕턴스를 모델에 두면 **그 스펙트럼을 만든 식**이라 거의 완벽해야 한다.
    assert with_l < 0.02, f"L 을 넣고도 {with_l:.1%}"
    # 빼면 눈에 띄게 나빠진다.  이 배수가 곧 화면에서 보이던 차이다.
    assert without > 5 * with_l, f"L 없이 {without:.1%}, 있고 {with_l:.1%}"


def test_the_dropped_inductive_points_are_not_the_whole_story():
    """뺀 점의 수만 보고 "인덕턴스는 처리했다" 로 읽으면 안 된다.

    뺀 점이 있다는 것은 **남은 점에도 그 영향이 있다**는 신호다.  이 시험은
    그 신호가 실재함을 고정한다: 유도성 점을 다 뺀 뒤에도, 남은 가장 높은
    주파수의 점은 인덕턴스가 없을 때와 뚜렷이 다르다.
    """
    frequency = S.log_sweep(7e6, 1e-2, 10)
    bare = parse_circuit(LIQUID)
    withl = parse_circuit("L1-" + LIQUID)
    arcs = [5.0, 20.0, 1e-5, 0.7, 40.0, 1e-3, 0.8]
    z_bare = bare.impedance(np.array(arcs), frequency)
    z_ind = withl.impedance(np.array([8e-7, *arcs]), frequency)

    capacitive = z_ind.imag < 0
    top = frequency[capacitive].max()
    at = frequency == top
    # 실수축을 아직 안 넘은 (즉 우리가 **남기는**) 가장 높은 점에서도 차이가
    # 크다.  1 % 면 아크 하나를 찌그러뜨리기에 충분하다.
    apart = float(np.abs(z_ind[at] - z_bare[at])[0] / np.abs(z_bare[at])[0])
    assert apart > 0.05, f"교차점 바로 아래에서 차이가 {apart:.1%} 뿐"


# --- 실수축 위의 점은 어디에 있느냐로 갈린다 (Codex #3) ---------------------

def test_only_the_high_frequency_run_counts_as_wiring():
    """부호는 관측이지 "배선이다" 의 증명이 아니다.

    배터리는 제 저주파 유도성 고리를 갖는다 — 느린 표면 피복이나 피막 성장에서
    오는 화학적 인덕턴스, 그리고 아직 안정되지 않은 셀의 드리프트.  그것은
    **셀의 측정값**이고, 부호만으로는 케이블 인덕턴스와 구별할 수 없다.
    구별하는 것은 **스윕 안에서의 자리**다.

    Codex 재현: 100 kHz~0.01 Hz 스무 점 중 **아래쪽** 다섯이 양수인 스펙트럼에서
    옛 규칙은 맞춘 하한을 0.01 Hz 에서 0.695 Hz 로 밀어 올렸다 — 가장 느린
    한 자리를 통째로 버리고 나머지를 측정값으로 보고했다.
    """
    from wrdkit.eis.guess import inductive_mask

    frequency = np.logspace(5, -2, 20)
    z_im = np.full(20, -1.0)
    z_im[:3] = 1.5      # 고주파 세 점 — 배선
    z_im[-5:] = 0.4     # 저주파 다섯 점 — 셀 자신의 것
    spectrum = Spectrum(frequency_hz=frequency, z_re=np.linspace(5, 50, 20),
                        z_im=z_im)

    mask = inductive_mask(spectrum)
    assert mask[:3].all()          # 위에서부터 이어진 것만
    assert not mask[3:].any()      # 저주파 다섯 점은 남는다
    assert spectrum.select(~mask).frequency_hz.min() == pytest.approx(0.01)


def test_a_gap_ends_the_run():
    """가운데 한 점만 양수여도 그것은 배선이 아니다 — 이어져 있지 않다."""
    from wrdkit.eis.guess import inductive_mask

    frequency = np.array([1e4, 1e3, 1e2, 1e1, 1e0])
    spectrum = Spectrum(frequency_hz=frequency,
                        z_re=np.array([10.0, 11.0, 12.0, 13.0, 14.0]),
                        z_im=np.array([10.0, -2.0, 3.0, -4.0, -5.0]))
    mask = inductive_mask(spectrum)
    assert list(mask) == [True, False, False, False, False]


def test_the_run_is_found_by_frequency_not_array_order():
    """배열이 저주파부터 담겨 있어도 판정은 같다 — 파일마다 순서가 다르다."""
    from wrdkit.eis.guess import inductive_mask

    frequency = np.array([1e0, 1e1, 1e2, 1e3, 1e4])
    spectrum = Spectrum(frequency_hz=frequency,
                        z_re=np.array([14.0, 13.0, 12.0, 11.0, 10.0]),
                        z_im=np.array([-5.0, -4.0, 3.0, -2.0, 10.0]))
    mask = inductive_mask(spectrum)
    # 가장 높은 10 kHz 하나만 배선이다.  100 Hz 의 양수는 남는다.
    assert list(mask) == [False, False, False, False, True]


# --- 회로가 아는 축퇴, 그리고 "무엇이 안 걸렸나" (Codex #2·#8) ----------------


def test_the_circuit_declares_its_exchangeable_pair():
    """짝은 회로가 안다 — 피팅이 이름 끝을 보고 알아내는 것이 아니라."""
    from wrdkit.eis.circuit import parse_circuit

    assert parse_circuit("R0-TL1").exchangeable_pairs == (("TL1_Ri", "TL1_Re"),)
    assert parse_circuit("R0-TLR2").exchangeable_pairs == (("TLR2_Ri", "TLR2_Re"),)
    # 축퇴가 없는 회로는 빈 채로 둔다.  "모르면 아무 말도 안 한다".
    assert parse_circuit("R0-p(R1,CPE1)").exchangeable_pairs == ()


def test_swapping_the_rails_does_not_move_the_curve_at_all():
    """짝이 축퇴라는 근거 — 두 값을 맞바꾼 임피던스가 **비트까지** 같다.

    이것이 성립하니까 `alias_of` 가 정당하다: 어떤 스펙트럼도, 어떤 재시작도
    둘을 가를 수 없다.  가를 수 있었다면 씨앗 흩기가 잡았을 것이다.
    """
    from wrdkit.eis.circuit import parse_circuit

    circuit = parse_circuit("R0-TL1")
    frequency = np.logspace(5, -2, 40)
    straight = np.array([5.0, 40.0, 12.0, 60.0, 1e-4, 0.8, 3.0, 0.5, 10.0])
    swapped = straight.copy()
    swapped[1], swapped[2] = straight[2], straight[1]
    assert np.array_equal(circuit.impedance(straight, frequency),
                          circuit.impedance(swapped, frequency))


def test_both_rails_are_marked_undetermined_with_the_reason():
    """맞바꿔도 같은 두 값은 **각각 측정된 값이 아니다** (Codex #2).

    오차 막대로는 절대 안 잡힌다 — 두 순서가 정확히 같은 chi² 라, 곡률도 같고
    씨앗 흩기에도 안 걸린다.  회로에서 표시를 받아 온다.
    """
    pytest.importorskip("scipy")
    from wrdkit.eis.circuit import parse_circuit

    circuit = parse_circuit("R0-TL1")
    frequency = np.logspace(4, -1.5, 45)
    truth = np.array([5.0, 40.0, 12.0, 60.0, 1e-4, 0.8, 3.0, 0.5, 10.0])
    z = circuit.impedance(truth, frequency)
    spectrum = Spectrum(frequency_hz=frequency, z_re=z.real, z_im=z.imag)

    result = fit_circuit(spectrum, "R0-TL1", restarts=4)
    rails = {p.name: p for p in result.parameters if p.name.endswith(("_Ri", "_Re"))}
    assert set(rails) == {"TL1_Ri", "TL1_Re"}
    for name, parameter in rails.items():
        assert parameter.alias_of == ("TL1_Re" if name == "TL1_Ri" else "TL1_Ri")
        assert parameter.status == "undetermined"
        assert parameter.reason == "structural_alias"
        assert not parameter.determined
    assert "TL1_Ri ↔ TL1_Re" in result.reason
    # R0 는 이 축퇴와 무관하다 — 표시가 회로 전체로 번지면 안 된다.
    r0 = next(p for p in result.parameters if p.name == "R0")
    assert r0.alias_of == ""


def test_one_solution_is_not_checked_and_is_not_a_measurement():
    """비교할 답이 하나뿐이면 흩어짐 검사는 **돌지 않은** 것이다 (Codex #8).

    **값은 그리고, 재지는 않는다.**  처음에는 `determined` 를 True 로 뒀다 —
    "답이 하나인 피팅의 수를 다 감추면 화면이 빈다" 는 이유였는데 둘 다
    틀렸다.  화면은 안 빈다 (파라미터 표가 값을 그리고 옆에 `미결정` 을
    붙이며, 맞춤 곡선은 어느 쪽이든 원래 값을 쓴다 — `value_available`).
    그리고 `determined` 가 실제로 막는 것은 **측정값만 받아야 하는 소비자**
    다: 총저항·전도도·추세·무표시 TSV.  거기에 "검사를 안 했다" 를 흘려
    보내는 것이 이 표시가 존재하는 이유 그 자체였다.
    """
    from wrdkit.eis.fit import Parameter

    quiet = Parameter(name="R0", value=10.0, stderr=0.1, spread=None)
    assert quiet.status == "not_checked"
    assert quiet.reason == "scatter_not_measured"   # 사유가 안 실렸을 때의 기본
    assert not quiet.determined        # 총저항·전도도에 못 들어간다
    assert quiet.value_available       # 그래도 그림과 표에는 그린다

    checked = Parameter(name="R0", value=10.0, stderr=0.1, spread=1.2)
    assert checked.status == "determined"
    assert checked.reason == ""

    scattered = Parameter(name="R0", value=10.0, stderr=0.1, spread=9.0)
    assert scattered.status == "undetermined"
    assert scattered.reason == "seed_spread"
    assert not scattered.determined

    blind = Parameter(name="R0", value=10.0, stderr=None, spread=None)
    assert blind.status == "undetermined"
    assert blind.reason == "no_error_bar"

    fuzzy = Parameter(name="R0", value=10.0, stderr=8.0, spread=1.0)
    assert fuzzy.status == "undetermined"
    assert fuzzy.reason == "relative_stderr"
