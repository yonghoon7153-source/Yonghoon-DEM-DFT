"""검수가 권한 회로로 다시 맞추기 — 무엇을, 어디서 시작해, 받아들일지 (ADR 0045).

끝에서 끝까지의 두 경우가 이 기능의 전부다.  꼬리를 아크로 흉내 낸 펠릿은
권한 회로로 풀리고, 아크가 정말 보이는 펠릿은 아크 없는 회로로 바꾸지 않는다 —
이름을 고치려고 모양을 못 그리는 회로를 고르면 값이 없어진다.
"""

import math
from dataclasses import dataclass

import numpy as np
import pytest
import synthetic_eis as S

from wrdkit.eis.audit import CHECK, PROBLEM, Finding, audit_fit
from wrdkit.eis.circuit import parse_circuit
from wrdkit.eis.derive import SOLID, SYMMETRIC, blocking_verdict, ionic_conductivity
from wrdkit.eis.fit import fit_circuit
from wrdkit.eis.refit import (
    Candidate,
    accept_refit,
    moved_number,
    refit_candidates,
    remaining_problems,
    seed_values,
)
from wrdkit.eis.spectrum import Spectrum

FREQUENCY = S.log_sweep(7e6, 10.0, 10)
BAND = (10.0, 2.15e5)
PELLET_CM = 700e-4
AREA_CM2 = math.pi / 4
PRESETS = ["R0-TL1", "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3", "L1-R0-CPE1",
           "L1-R0-p(R1,CPE1)-CPE2", "L1-R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"]


@dataclass
class P:
    name: str
    value: float
    status: str = "determined"
    reason: str = ""

    @property
    def determined(self) -> bool:
        return self.status == "determined"


@dataclass
class Fit:
    circuit: str
    parameters: list


def spectrum_of(circuit: str, values: dict[str, float]) -> Spectrum:
    model = parse_circuit(circuit)
    z = model.impedance([values[name] for name in model.parameter_names], FREQUENCY)
    return Spectrum(FREQUENCY, z.real, z.imag)


def audit(fit, spectrum):
    return audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC, thickness_cm=PELLET_CM,
                     area_cm2=AREA_CM2, band=BAND, alternatives=PRESETS)


# -- 무엇을 맞춰 볼까 ------------------------------------------------------------

def test_only_problems_offer_circuits_and_each_circuit_is_tried_once():
    """확인은 사람이 보고 정할 일이다.  같은 회로를 두 판정이 권하면 한 번만
    맞추고, 다시 맞춘 뒤에는 두 판정이 다 풀려야 한다."""
    findings = [
        Finding(PROBLEM, "tail_mimicked_by_arc", "꼬리", circuits=("A", "B")),
        Finding(CHECK, "open_end_on_blocking_cell", "열린 끝", circuits=("D",)),
        Finding(PROBLEM, "arcs_are_electrode", "전극", circuits=("B", "C")),
        Finding(PROBLEM, "label_contradicts_capacitance", "이름"),
    ]
    assert refit_candidates(findings) == [
        Candidate("A", ("tail_mimicked_by_arc",)),
        Candidate("B", ("tail_mimicked_by_arc", "arcs_are_electrode")),
        Candidate("C", ("arcs_are_electrode",)),
    ]
    assert refit_candidates([findings[1], findings[3]]) == []


def test_a_broken_low_end_moves_every_try_up_to_its_bound():
    """보완 4: 저주파 끝이 KK 를 어긴 판정(확인)은 회로를 부르지 않고 하한을
    싣는다.  그 아래 점은 셀이 변하는 동안 잰 것이라 권한 회로도 그 하한부터
    맞추고, 쓰는 회로도 그 하한부터 한 번 — 문제 판정이 없어도, 맨 끝에."""
    drift = Finding(CHECK, "kk_violation", "저주파 끝", low_hz=1.29)
    tail = Finding(PROBLEM, "tail_mimicked_by_arc", "꼬리", circuits=("A",))
    assert refit_candidates([drift], circuit="OLD") == [Candidate("OLD", (), 1.29)]
    assert refit_candidates([tail, drift], circuit="OLD") == [
        Candidate("A", ("tail_mimicked_by_arc",), 1.29),
        Candidate("OLD", (), 1.29),
    ]
    # 쓰는 회로를 이미 권했으면 그 후보가 하한까지 맡는다 — 두 번 맞추지 않는다.
    assert refit_candidates([tail, drift], circuit="A") == [
        Candidate("A", ("tail_mimicked_by_arc",), 1.29)]
    # 하한이 없으면 전과 같다.
    assert refit_candidates([tail], circuit="OLD") == [
        Candidate("A", ("tail_mimicked_by_arc",))]
    # 쓰는 회로를 모르면 하한만으로는 맞춰 볼 것이 없다.
    assert refit_candidates([drift]) == []


# -- 어디서 시작할까 -------------------------------------------------------------

OLD = "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"
OLD_VALUES = {"R0": 84.3, "R1": 2.92e3, "CPE1_Q": 7.47e-6, "CPE1_n": 0.851,
              "R2": 2.6e5, "CPE2_Q": 9.18e-7, "CPE2_n": 1.0,
              "CPE3_Q": 2.68e-5, "CPE3_n": 0.663}


def test_the_blocking_tail_moves_to_the_new_tail_not_by_name():
    """옛 CPE3 는 새 `L1-R0-CPE1` 의 CPE1 이다.  이름으로 옮기면 옛 CPE1 —
    벌크라 부른 아크의 것 — 이 막는 꼬리로 들어간다."""
    assert seed_values(OLD, OLD_VALUES, "L1-R0-CPE1") == {
        "R0": 84.3, "CPE1_Q": 2.68e-5, "CPE1_n": 0.663}
    assert seed_values(OLD, OLD_VALUES, "L1-R0-p(R1,CPE1)-CPE2") == {
        "R0": 84.3, "R1": 2.92e3, "CPE1_Q": 7.47e-6, "CPE1_n": 0.851,
        "CPE2_Q": 2.68e-5, "CPE2_n": 0.663}


def test_an_element_that_is_the_tail_on_one_side_only_is_not_carried():
    # 옛 꼬리 CPE2 는 새 회로에서 아크의 CPE2 다.
    old = {"R0": 8.0, "R1": 50.0, "CPE1_Q": 2e-6, "CPE1_n": 0.9,
           "CPE2_Q": 1e-5, "CPE2_n": 0.8}
    assert seed_values("R0-p(R1,CPE1)-CPE2", old, "R0-p(R1,CPE1)-p(R2,CPE2)") == {
        "R0": 8.0, "R1": 50.0, "CPE1_Q": 2e-6, "CPE1_n": 0.9}
    # 옛 CPE1 은 꼬리를 흉내 낸 아크의 것이고, 새 CPE1 은 막는 꼬리다.
    assert seed_values("R0-p(R1,CPE1)", {"R0": 7.89, "R1": 1.37e5, "CPE1_Q": 1.95e-6,
                                         "CPE1_n": 0.856}, "L1-R0-CPE1") == {"R0": 7.89}


def test_a_value_on_its_bound_is_not_a_start():
    """경계에 붙은 값은 답이 아니라 벽이다."""
    seeded = seed_values(OLD, OLD_VALUES, "L1-R0-p(R1,CPE1)-CPE2", skip=["R1", "CPE3_n"])
    assert "R1" not in seeded and "CPE2_n" not in seeded
    assert seeded["CPE2_Q"] == 2.68e-5
    assert seed_values("R0-p(R1", OLD_VALUES, "L1-R0-CPE1") == {}
    assert seed_values(OLD, {"R0": float("nan")}, "L1-R0-CPE1") == {}


def test_the_fitter_starts_from_the_seed_and_fills_the_rest_from_the_data():
    """이름이 빠진 파라미터(여기서는 L1)는 데이터로 잡은 기본 시작점을 쓴다."""
    spectrum = spectrum_of("L1-R0-CPE1", {"L1": 1.73e-6, "R0": 8.3, "CPE1_Q": 1.9e-6,
                                          "CPE1_n": 0.86})
    result = fit_circuit(spectrum, "L1-R0-CPE1", start_from={"R0": 8.0, "CPE1_n": 0.85},
                         frequency_range=BAND)
    assert result.converged
    assert result.values()["R0"] == pytest.approx(8.3, rel=1e-3)
    assert result.values()["L1"] == pytest.approx(1.73e-6, rel=1e-3)


# -- 받아들일까 ------------------------------------------------------------------

LABEL = Finding(PROBLEM, "label_contradicts_capacitance", "R2 는 입계일 수 없습니다")
TAIL = Finding(PROBLEM, "tail_mimicked_by_arc", "R1 은 꼬리를 흉내 냈습니다",
               circuits=("L1-R0-CPE1",))


def test_a_refit_is_accepted_only_when_its_problem_is_gone_and_nothing_got_worse():
    old = [TAIL, LABEL, LABEL]
    triggers = ("tail_mimicked_by_arc",)
    assert accept_refit(old, [], triggers, converged=False).reason == "수렴하지 않았습니다"

    left = accept_refit(old, [TAIL], triggers, converged=True)
    assert not left.accepted
    assert left.reason == "그 문제가 그대로입니다 — R1 은 꼬리를 흉내 냈습니다"

    # 아크 하나의 이름만 고쳐져도 같은 코드가 남는다 — 늘지만 않으면 된다.
    assert accept_refit(old, [LABEL], triggers, converged=True).accepted
    worse = accept_refit([TAIL, LABEL], [LABEL, LABEL], triggers, converged=True)
    assert not worse.accepted
    assert worse.reason.startswith("없던 문제가 생깁니다 — R2 는 입계일 수")


def test_a_circuit_that_cannot_draw_the_shape_is_refused_whatever_it_fixes():
    """확인 심각도라도 막는다 — 문제가 하나 줄어도 곡선이 점을 안 지나가면
    값이 없다."""
    misfit = Finding(CHECK, "misfit_everywhere",
                     "맞춤이 평균 22.7 % 어긋납니다 — 회로가 이 스펙트럼의 모양을 못 그립니다")
    refused = accept_refit([TAIL], [misfit], ("tail_mimicked_by_arc",), converged=True)
    assert not refused.accepted
    assert refused.reason == misfit.message
    assert remaining_problems([TAIL, LABEL, misfit]) == 2


def test_a_shape_the_old_fit_could_not_draw_either_does_not_block_the_same_model():
    """실측 B15 #9 · B16 #9: 옛 `R0-p(R1,CPE1)` 는 R1 이 10⁹ Ω 로 가 곧 `R0-CPE1`
    이었다.  새 `L1-R0-CPE1` 도 같은 3.2 % 로 못 그린다 — 같은 모양을 이름만 바로
    그린 것이다.  모양 판정은 **새로 생기거나 더 나빠질 때만** 막는다."""
    misfit = Finding(CHECK, "misfit_everywhere",
                     "맞춤이 평균 3.2 % 어긋납니다 — 회로가 이 스펙트럼의 모양을 못 그립니다")
    old = [TAIL, misfit]
    triggers = ("tail_mimicked_by_arc",)
    assert accept_refit(old, [misfit], triggers, converged=True,
                        old_misfit=0.032, new_misfit=0.032).accepted
    assert accept_refit(old, [misfit], triggers, converged=True,
                        old_misfit=0.032, new_misfit=0.036).accepted       # 0.5 안
    worse = accept_refit(old, [misfit], triggers, converged=True,
                         old_misfit=0.032, new_misfit=0.045)
    assert not worse.accepted and worse.reason == misfit.message
    # 오차를 모르면 막는다 — 모르는 것을 받아들이지 않는다.
    assert not accept_refit(old, [misfit], triggers, converged=True).accepted


# -- 끝에서 끝까지 ----------------------------------------------------------------

def pellet():
    """황화물 블로킹 펠릿 (배선 L + 전해질 R + 이중층 CPE) — 실측 B15 #2 의 쌍둥이."""
    return spectrum_of("L1-R0-CPE1", {"L1": 1.73e-6, "R0": 8.3, "CPE1_Q": 1.9e-6,
                                      "CPE1_n": 0.86})


def test_a_tail_mimicked_by_an_arc_is_refitted_with_the_offered_circuit():
    old_fit = Fit("R0-p(R1,CPE1)", [P("R0", 7.89),
                                    P("R1", 1.37e5, "undetermined", "at_upper_bound"),
                                    P("CPE1_Q", 1.95e-6), P("CPE1_n", 0.856)])
    before = audit(old_fit, pellet())
    first = refit_candidates(before.findings)[0]
    assert first == Candidate("L1-R0-CPE1", ("tail_mimicked_by_arc",))

    values = {p.name: p.value for p in old_fit.parameters}
    seeded = seed_values(old_fit.circuit, values, first.circuit, skip=["R1"])
    result = fit_circuit(pellet(), first.circuit, start_from=seeded, frequency_range=BAND)
    after = audit(result, pellet())
    assert accept_refit(before.findings, after.findings, first.triggers,
                        converged=result.converged).accepted
    assert remaining_problems(after.findings) == 0
    assert result.values()["R0"] == pytest.approx(8.3, rel=1e-3)


def test_an_arc_that_is_really_there_is_not_refitted_away():
    """아크가 정말 보이는 펠릿 — 아크 없는 회로는 그 모양을 못 그린다.  그 아크는
    전극 크기라 "벌크" 라는 이름이 틀렸지만, 이름을 고치려고 모양을 버리지
    않는다 (ADR 0045 의 비용: 이것은 랩이 이름 규칙을 정할 일이다)."""
    circuit = "L1-R0-p(R1,CPE1)-CPE2"
    values = {"L1": 1.7e-6, "R0": 8.0, "R1": 200.0, "CPE1_Q": 2e-6, "CPE1_n": 0.9,
              "CPE2_Q": 1e-5, "CPE2_n": 0.9}
    spectrum = spectrum_of(circuit, values)
    before = audit(Fit(circuit, [P(name, value) for name, value in values.items()]),
                   spectrum)
    (only,) = refit_candidates(before.findings)
    assert only == Candidate("L1-R0-CPE1", ("arcs_are_electrode",))

    seeded = seed_values(circuit, values, only.circuit)
    assert seeded["CPE1_Q"] == 1e-5                      # 꼬리에서, 아크가 아니라
    result = fit_circuit(spectrum, only.circuit, start_from=seeded, frequency_range=BAND)
    verdict = accept_refit(before.findings, audit(result, spectrum).findings,
                           only.triggers, converged=result.converged)
    assert not verdict.accepted
    assert "모양을 못 그립니다" in verdict.reason
    assert np.isfinite(result.chi_squared)


# -- 수를 옮기는가 ----------------------------------------------------------------

def test_a_worse_drawing_does_not_get_to_move_the_number():
    """이름이 맞아지는 대신 σ 가 틀려지면 받지 않는다.  더 잘 그리면 받는다."""
    moved = moved_number(8.0, 9.34, 0.0, 0.01)
    assert moved.startswith("σ 에 쓰는 저항이 8 → 9.34 Ω (+17 %) 로 옮겨 가는데")
    assert "오차 평균 < 0.01 → 1 %" in moved
    assert moved_number(8.0, 9.34, 0.037, 0.0092) == ""        # 더 잘 그린다
    assert moved_number(8.0, 8.3, 0.0, 0.01) == ""             # 4 % — 안 옮겼다
    # 실측 B12 #4: −7 % 지만 1.9 → 2.0 % 는 같은 그림이다 (옛 맞춤엔 배선 L 이 없었다).
    assert moved_number(9.43, 8.815, 0.019, 0.020) == ""
    assert moved_number(None, 9.34, 0.0, 0.01) == ""           # σ 를 못 내는 셀
    assert moved_number(8.0, 9.34, None, 0.01) == ""


def test_an_electrode_arc_swallowed_into_r0_is_caught_even_when_the_audit_passes():
    """작은 전극 크기 아크 — 아크 없는 회로가 그것을 R0 로 삼켜도 평균 오차는 1 %
    라 검수는 받아들인다.  σ 에 쓰는 저항은 17 % 옮겨 간다."""
    circuit = "L1-R0-p(R1,CPE1)-CPE2"
    values = {"L1": 1.7e-6, "R0": 8.0, "R1": 1.5, "CPE1_Q": 5e-6, "CPE1_n": 0.85,
              "CPE2_Q": 1e-5, "CPE2_n": 0.9}
    spectrum = spectrum_of(circuit, values)
    verdict = blocking_verdict(spectrum.frequency_hz, spectrum.z_re, spectrum.z_im)

    def sigma(fit):
        return ionic_conductivity(fit, thickness_cm=PELLET_CM, area_cm2=AREA_CM2,
                                  config=SYMMETRIC, blocking=verdict)

    old_fit = Fit(circuit, [P(name, value) for name, value in values.items()])
    before = audit(old_fit, spectrum)
    (only,) = refit_candidates(before.findings)
    result = fit_circuit(spectrum, only.circuit,
                         start_from=seed_values(circuit, values, only.circuit),
                         frequency_range=BAND)
    after = audit(result, spectrum)
    assert accept_refit(before.findings, after.findings, only.triggers,
                        converged=result.converged).accepted
    assert sigma(old_fit)["total_ohm"] == 8.0                  # 아크는 전극 쪽이라 뺐다
    moved = moved_number(sigma(old_fit)["total_ohm"], sigma(result)["total_ohm"],
                         before.misfit.mean, after.misfit.mean)
    assert "8 → 9.3" in moved and "(+17 %)" in moved
