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

from wrdkit.eis.audit import CHECK, NOTE, PROBLEM, Finding, audit_fit
from wrdkit.eis.circuit import parse_circuit
from wrdkit.eis.derive import SOLID, SYMMETRIC, blocking_verdict, ionic_conductivity
from wrdkit.eis.fit import fit_circuit
from wrdkit.eis.guess import inductive_mask
from wrdkit.eis.refit import (
    Candidate,
    accept_refit,
    added_arc,
    electrolyte_short,
    moved_number,
    refit_candidates,
    remaining_problems,
    seed_arc,
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


def test_a_missing_cable_inductance_is_refitted_though_it_is_a_check():
    """보완 8: 배선 L 이 빠졌다는 판정은 확인인데도 회로를 부른다 — 셀을 읽는
    방식은 그대로이고 케이블의 소자 하나를 더할 뿐이다.  다른 확인은 그대로 사람
    몫이다 (실측 08:07 검수: 확인 71 중 스물셋)."""
    cable = Finding(CHECK, "inductance_missing", "고주파 끝", circuits=("L1-OLD",))
    open_end = Finding(CHECK, "open_end_on_blocking_cell", "열린 끝", circuits=("D",))
    assert refit_candidates([cable, open_end], circuit="OLD") == [
        Candidate("L1-OLD", ("inductance_missing",))]
    drift = Finding(CHECK, "kk_violation", "저주파 끝", low_hz=1.29)
    assert refit_candidates([cable, drift], circuit="OLD") == [
        Candidate("L1-OLD", ("inductance_missing",), 1.29),
        Candidate("OLD", (), 1.29),
    ]


def test_an_arc_above_the_window_is_refitted_though_it_is_a_check():
    """보완 10: 차가운 펠릿의 구간 위 아크 판정(확인)도 회로를 부른다 — 판정이 까닭을
    말하고, 받아들이는 조건이 새 맞춤에서 그 까닭을 확인한다 (실측 10:24 검수: 일곱)."""
    arc = Finding(CHECK, "arc_above_window", "구간 위 아크",
                  circuits=("L1-R0-p(R1,CPE1)-CPE2",))
    assert refit_candidates([arc], circuit="L1-R0-CPE1") == [
        Candidate("L1-R0-p(R1,CPE1)-CPE2", ("arc_above_window",))]
    # 판정이 상한을 실으면 그 회로는 거기까지 맞춘다 — 아크가 쓰던 구간 위에 있다.
    wide = Finding(CHECK, "arc_above_window", "구간 위 아크",
                   circuits=("L1-R0-p(R1,CPE1)-CPE2",), high_hz=3.49e6)
    drift = Finding(CHECK, "kk_violation", "저주파 끝", low_hz=1.29)
    assert refit_candidates([wide, drift], circuit="L1-R0-CPE1") == [
        Candidate("L1-R0-p(R1,CPE1)-CPE2", ("arc_above_window",), 1.29, 3.49e6),
        Candidate("L1-R0-CPE1", (), 1.29)]
    # 회로를 못 찾은 판정은 부를 것이 없다.
    assert refit_candidates([Finding(CHECK, "arc_above_window", "구간 위 아크")]) == []


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


def test_the_added_arc_starts_where_the_audit_puts_it():
    """보완 10: 더한 아크는 데이터가 못 보여 준다 — 꼭지가 구간 위라 −Z'' 에 봉우리가
    없다.  그래서 판정이 아는 수에서 시작한다: 직렬 저항은 교점, 아크의 R 은 옛 직렬
    저항 − 교점, 꼭지는 맞춘 구간의 꼭대기, n 0.85.  꼬리는 옛 꼬리에서 온다.
    실측 B15 #9 (#114): R0 135.9 Ω, 교점 114.9 Ω."""
    old = {"L1": 1e-12, "R0": 135.9, "CPE1_Q": 6.5e-7, "CPE1_n": 0.86}
    seeded = seed_arc("L1-R0-CPE1", old, "L1-R0-p(R1,CPE1)-CPE2", skip=["L1"],
                      series_ohm=135.9, crossing_ohm=114.9, top_hz=1.71e5)
    assert seeded.pop("CPE1_Q") == pytest.approx(1 / (21.0 * (2 * np.pi * 1.71e5) ** 0.85))
    assert seeded == pytest.approx({"R0": 114.9, "R1": 21.0, "CPE1_n": 0.85,
                                    "CPE2_Q": 6.5e-7, "CPE2_n": 0.86})
    # 아크가 있던 회로면 옛 아크는 한 자리 뒤로 간다 — 새 아크가 가장 빠르다.
    two = seed_arc("L1-R0-p(R1,CPE1)-CPE2",
                   {"L1": 2e-6, "R0": 90.0, "R1": 300.0, "CPE1_Q": 2e-6, "CPE1_n": 0.9,
                    "CPE2_Q": 1e-5, "CPE2_n": 0.8},
                   "L1-R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
                   series_ohm=90.0, crossing_ohm=80.0, top_hz=1e5)
    assert {name: two[name] for name in ("L1", "R0", "R1", "CPE1_n", "R2", "CPE2_Q",
                                         "CPE2_n", "CPE3_Q", "CPE3_n")} == pytest.approx(
        {"L1": 2e-6, "R0": 80.0, "R1": 10.0, "CPE1_n": 0.85, "R2": 300.0, "CPE2_Q": 2e-6,
         "CPE2_n": 0.9, "CPE3_Q": 1e-5, "CPE3_n": 0.8})
    # 아크가 하나 늘지 않았으면 이름으로 옮긴 그대로다.
    assert seed_arc("L1-R0-CPE1", old, "L1-R0-CPE1", series_ohm=135.9, crossing_ohm=114.9,
                    top_hz=1.71e5) == seed_values("L1-R0-CPE1", old, "L1-R0-CPE1")
    # 더한 아크는 새 회로의 가장 빠른 가지다.
    assert added_arc("L1-R0-CPE1", "L1-R0-p(R1,CPE1)-CPE2") == ("R1", "CPE1")
    assert added_arc("L1-R0-p(R1,CPE1)-CPE2",
                     "L1-R0-p(R1,CPE1)-p(R2,CPE2)-CPE3") == ("R1", "CPE1")
    assert added_arc("L1-R0-CPE1", "L1-R0-CPE1") is None


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


def test_a_wiring_refit_is_taken_only_when_the_top_end_is_drawn():
    """L 이 있는 회로에는 배선 판정이 뜰 수 없어 "그 판정이 풀렸나" 는 늘 참이다.
    그래서 판정이 본 증상 — 가장 크게 어긋난 점이 고주파 끝에서 문턱을 넘음 — 이
    사라졌는지 보고, 소자 하나를 더했으니 평균이 나빠지지 않았는지 본다 (보완 8)."""
    cable = Finding(CHECK, "inductance_missing", "고주파 끝", circuits=("L1-OLD",))
    triggers = ("inductance_missing",)
    assert accept_refit([cable], [], triggers, converged=True,
                        old_misfit=0.021, new_misfit=0.008).accepted

    top = accept_refit([cable], [], triggers, converged=True, old_misfit=0.021,
                       new_misfit=0.018, new_top_misfit=(0.12, 2.15e5))
    assert not top.accepted
    assert top.reason == ("고주파 끝이 그대로입니다 — L 을 넣어도 2.15e+05 Hz 가 12 % "
                          "어긋납니다. L 로는 그 끝이 안 그려집니다")
    # 실측 #105: 38 → 11 % 로 줄었는데 "그대로" 라고 적었다 — 줄었으면 그렇게 적는다.
    less = accept_refit([cable], [], triggers, converged=True, old_misfit=0.05,
                        new_misfit=0.02, new_top_misfit=(0.11, 8.72e5),
                        old_top_misfit=(0.38, 8.72e5))
    assert not less.accepted
    assert less.reason == ("고주파 끝이 아직 가장 크게 어긋납니다 — L 을 넣어 8.72e+05 Hz 가 "
                           "38 → 11 % 로 줄었지만 문턱을 넘습니다. L 하나로는 그 끝을 다 "
                           "못 그립니다")
    same = accept_refit([cable], [], triggers, converged=True, old_misfit=0.05,
                        new_misfit=0.05, new_top_misfit=(0.37, 8.72e5),
                        old_top_misfit=(0.38, 8.72e5))
    assert same.reason.startswith("고주파 끝이 그대로입니다")

    worse = accept_refit([cable], [], triggers, converged=True,
                         old_misfit=0.021, new_misfit=0.03)
    assert not worse.accepted
    assert worse.reason.startswith("오차 평균이 2.1 → 3 % 로 늘었습니다")
    assert not accept_refit([cable], [], triggers, converged=True).accepted
    # 문제 판정이 권한 회로는 전처럼 — 증상을 넘겨도 보지 않는다.
    assert accept_refit([TAIL], [], ("tail_mimicked_by_arc",), converged=True,
                        new_top_misfit=(0.12, 2.15e5)).accepted


def test_an_arc_refit_is_taken_only_when_r0_comes_down_and_the_arc_is_electrolyte():
    """보완 10: 판정은 L 이 0 일 때만 떠서 코드로는 풀린 것처럼 보일 수 있다.  그래서
    증상 — 직렬 저항이 교점 위 — 이 사라졌는지, 아크 하나를 더했으니 평균이 나빠지지
    않았는지 본다.  σ 저항이 교점 이상인지는 σ 를 아는 쪽이 본다 (`electrolyte_short`)."""
    arc = Finding(CHECK, "arc_above_window", "구간 위 아크", circuits=("NEW",))
    triggers = ("arc_above_window",)
    assert accept_refit([arc], [], triggers, converged=True,
                        old_misfit=0.024, new_misfit=0.004).accepted
    still = accept_refit([arc], [], triggers, converged=True, old_misfit=0.024,
                         new_misfit=0.004, new_above_crossing=(130.0, 114.9))
    assert not still.accepted
    assert still.reason == ("직렬 저항 130 Ω 이 아직 실수축 교점 114.9 Ω 보다 13 % 큽니다 — "
                            "더한 아크가 구간 위의 아크를 그리지 않았습니다")
    worse = accept_refit([arc], [], triggers, converged=True,
                         old_misfit=0.024, new_misfit=0.035)
    assert worse.reason == ("오차 평균이 2.4 → 3.5 % 로 늘었습니다 — 아크 하나를 더했는데 "
                            "더 어긋나면 다른 골짜기입니다")
    # 실측 #123 (11:44 맞춰 보기): R0 가 0 (경계) 으로 가 교점 아래가 됐다 — 더한 소자가
    # 절편까지 가져간 것이지, 교점 너머의 아크를 그린 것이 아니다.
    gone = Finding(CHECK, "series_resistance_gone", "R0 이 0 에 붙었습니다 (1.06e-09 Ω)")
    lost = accept_refit([arc], [gone], triggers, converged=True,
                        old_misfit=0.033, new_misfit=0.018)
    assert not lost.accepted
    assert lost.reason == ("더한 아크가 고주파 절편까지 가져갔습니다 — R0 이 0 에 붙었습니다 "
                           "(1.06e-09 Ω)")
    # 옛 맞춤에도 있었으면 그 때문에 막지 않는다.  배선·문제 판정의 회로도 전처럼.
    assert accept_refit([arc, gone], [gone], triggers, converged=True,
                        old_misfit=0.033, new_misfit=0.018).accepted
    assert accept_refit([TAIL], [gone], ("tail_mimicked_by_arc",), converged=True).accepted
    assert not accept_refit([arc], [], triggers, converged=True).accepted

    def sigma(ohm, *parts):
        return {"total_s_cm": 1e-4, "total_ohm": ohm, "total_parts": list(parts)}

    assert electrolyte_short(114.9, sigma(142.0, "R0", "R1"), "R1") == ""
    assert electrolyte_short(114.9, sigma(114.9, "R0", "R1"), "R1") == ""
    # 실측 #114 (11:15 맞춰 보기): σ 135.9 → 120.1 Ω 으로 받아들여졌다.  σ 가 R0 하나이고
    # R0 가 교점 위 5 % 안이면, σ ≥ 교점만 봐서는 더한 아크가 빠진 것을 모른다.
    assert electrolyte_short(114.9, sigma(120.1, "R0"), "R1") == (
        "더한 아크 R1 이 σ 에 안 듭니다 — 커패시턴스가 전극 쪽이라 구간 위의 아크가 "
        "아닙니다")
    # 벌크 크기로 읽혀 R0 를 배선으로 뺐다 — σ 는 R1 하나라 교점에 못 미친다.
    assert electrolyte_short(114.9, sigma(22.2, "R1"), "R1") == (
        "σ 저항 22.2 Ω 이 실수축 교점 114.9 Ω 보다 작습니다 — 새 맞춤이 구간 위의 아크를 "
        "전해질 저항으로 읽지 않았습니다. 판정의 까닭과 어긋나니 사람이 봅니다")
    assert electrolyte_short(114.9, {"total_s_cm": None,
                                     "missing": ["결정되지 않은 저항"]}, "R1") == (
        "σ 를 못 냅니다 (결정되지 않은 저항) — 더한 아크가 전해질 저항에 드는지 확인할 수 "
        "없습니다")
    assert electrolyte_short(None, sigma(142.0, "R0", "R1"), "R1") == (
        "실수축 교점을 몰라 σ 저항과 견줄 수 없습니다")


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


def test_a_fit_without_the_cable_gets_l1_in_front_and_draws_the_top_end():
    """보완 8: 배선 L 이 있는 펠릿을 L 없이 맞춘 것 — 실측 mid_Ni #38–#48 · B18
    #133–#138 의 쌍둥이.  검수가 권한 `L1-` 회로로 맞추면 고주파 끝이 풀리고
    받아들여진다."""
    old = fit_circuit(pellet(), "R0-CPE1", frequency_range=BAND)
    before = audit(old, pellet())
    (cable,) = [f for f in before.findings if f.code == "inductance_missing"]
    assert cable.severity == CHECK and cable.circuits == ("L1-R0-CPE1",)
    assert before.top_misfit is not None and before.top_misfit[1] > BAND[1] / 2
    (first,) = refit_candidates(before.findings, circuit=old.circuit)
    assert first == Candidate("L1-R0-CPE1", ("inductance_missing",))

    seeded = seed_values(old.circuit, old.values(), first.circuit)
    assert "L1" not in seeded                     # 새 소자는 데이터로 잡은 시작점
    result = fit_circuit(pellet(), first.circuit, start_from=seeded, frequency_range=BAND)
    after = audit(result, pellet())
    assert after.top_misfit is None
    assert accept_refit(before.findings, after.findings, first.triggers,
                        converged=result.converged, old_misfit=before.misfit.mean,
                        new_misfit=after.misfit.mean,
                        new_top_misfit=after.top_misfit).accepted
    assert result.values()["L1"] == pytest.approx(1.73e-6, rel=1e-3)


def pellet_with_an_arc(noise_seed: int | None, *, inductance: float, series: float,
                       arc: float, apex_hz: float, n: float, tail_q: float,
                       tail_n: float) -> Spectrum:
    """식은 황화물 펠릿 — 배선 L, 직렬 저항, 잰 주파수 안으로 내려온 전해질 아크, 블로킹
    꼬리, 잡음 0.3 %.  전해질 저항은 ``series + arc`` 다."""
    w = 2 * np.pi * FREQUENCY
    tau = 1 / (2 * np.pi * apex_hz)
    z = (1j * w * inductance + series + arc / (1 + (1j * w * tau) ** n)
         + 1 / (tail_q * (1j * w) ** tail_n))
    if noise_seed is not None:
        rng = np.random.default_rng(noise_seed)
        z = z * (1 + 0.003 * (rng.standard_normal(z.size)
                              + 1j * rng.standard_normal(z.size)))
    return Spectrum(FREQUENCY, z.real, z.imag)


#: B15 #9 (-20 °C) 꼴 — 배선 L 2 µH, 90 Ω 뒤에 꼭지 300 kHz 의 46 Ω 아크.  136 Ω.
COLD = {"inductance": 2e-6, "series": 90.0, "arc": 46.0, "apex_hz": 3e5, "n": 0.9,
        "tail_q": 6.3e-7, "tail_n": 0.87}
#: B16 #9 (#123) 꼴 — 유도성 점이 꼭대기 셋뿐이고 (배선 L 0.3 µH) 아크는 1 MHz 에
#: 있다.  쓰던 구간(215 kHz 까지)과 교점(MHz) 사이에 아크가 통째로 있다.  128 Ω.
GAP = {"inductance": 3e-7, "series": 98.0, "arc": 30.0, "apex_hz": 1e6, "n": 0.9,
       "tail_q": 1.03e-6, "tail_n": 0.852}


def refit_cold(spectrum: Spectrum, *, widen: bool = True):
    """`bml refit` 이 하는 대로 — 쓰던 구간(215 kHz 까지)의 옛 맞춤과 그 검수, 판정의
    회로·상한, 판정이 아는 수의 시작점, 새 검수와 σ.  ``widen=False`` 는 상한을
    무시하고 쓰던 구간으로 맞춘다 (첫 실측 맞춰 보기의 길)."""
    verdict = blocking_verdict(spectrum.frequency_hz, spectrum.z_re, spectrum.z_im)
    old = fit_circuit(spectrum, "L1-R0-CPE1", frequency_range=BAND)
    window = (float(old.frequency_hz.min()), float(old.frequency_hz.max()))

    def judged(fit):
        band = (float(fit.frequency_hz.min()), float(fit.frequency_hz.max()))
        sigma = ionic_conductivity(fit, thickness_cm=PELLET_CM, area_cm2=AREA_CM2,
                                   config=SYMMETRIC, blocking=verdict)
        return sigma, audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC,
                                thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=band,
                                conductivity=sigma, alternatives=PRESETS)

    _, before = judged(old)
    (candidate,) = refit_candidates(before.findings, circuit=old.circuit)
    series, crossing = before.above_crossing
    top = candidate.high_hz if widen and candidate.high_hz is not None else window[1]
    railed = [p.name for p in old.parameters if p.reason in ("at_lower_bound",
                                                             "at_upper_bound")]
    seeded = seed_arc(old.circuit, old.values(), candidate.circuit, skip=railed,
                      series_ohm=series, crossing_ohm=crossing, top_hz=top)
    new = fit_circuit(spectrum, candidate.circuit, start_from=seeded,
                      frequency_range=(window[0], top))
    sigma, after = judged(new)
    verdict = accept_refit(before.findings, after.findings, candidate.triggers,
                           converged=new.converged, old_misfit=before.misfit.mean,
                           new_misfit=after.misfit.mean,
                           new_above_crossing=after.above_crossing)
    short = electrolyte_short(crossing, sigma,
                              added_arc(old.circuit, candidate.circuit)[0])
    return candidate, crossing, new, sigma, after, verdict, short


@pytest.mark.parametrize("noise_seed", [1, 2, 3])
def test_a_cold_pellet_gets_its_arc_back_and_the_electrolyte_its_whole_resistance(noise_seed):
    """보완 10: 아크 하나를 더한 회로가 구간 위의 아크를 그리고, σ 는 R0 + R1 — 참값
    136 Ω 의 0.2 % 안이다.  옛 `L1-R0-CPE1` 의 R0 (130.8 Ω) 도, 교점 (96 Ω) 도 작았다.
    구간을 유도성이 아닌 꼭대기까지 넓히니 나누는 자리(R0 90 Ω)와 배선 L 도 나온다."""
    spectrum = pellet_with_an_arc(noise_seed, **COLD)
    candidate, crossing, new, sigma, after, verdict, short = refit_cold(spectrum)
    usable = float(spectrum.frequency_hz[~inductive_mask(spectrum)].max())
    assert candidate == Candidate("L1-R0-p(R1,CPE1)-CPE2", ("arc_above_window",),
                                  None, usable)
    assert verdict.accepted and short == ""
    assert after.above_crossing is None
    assert sigma["total_parts"] == ["R0", "R1"]
    assert sigma["total_ohm"] == pytest.approx(136.0, rel=0.002)
    assert sigma["total_ohm"] > crossing
    values = new.values()
    assert values["R0"] == pytest.approx(90.0, rel=0.03)
    assert values["L1"] == pytest.approx(2e-6, rel=0.2)
    # 꼭지(300 kHz)는 넓힌 구간 안이다 — 꼭지 판정이 없다.
    assert "arc_apex_above_window" not in [f.code for f in after.findings]


def test_the_arc_is_fitted_where_it_is_not_in_the_old_window():
    """실측 첫 맞춰 보기 (2026-09-25 11:15 UTC): 일곱 중 여섯이 그대로였다.  쓰던 맞춤이
    171–215 kHz 에서 끝나고, 아크는 그 위와 교점(MHz) 사이에 있었다 — 같은 구간으로
    맞추면 더한 아크가 그릴 점이 없다.  B16 #9 꼴 쌍둥이: 같은 구간이면 받지 않고,
    유도성이 아닌 꼭대기까지 넓히면 σ 가 참값 128 Ω 의 0.1 % 안이다."""
    spectrum = pellet_with_an_arc(1, **GAP)
    candidate, crossing, _, sigma, _, verdict, short = refit_cold(spectrum, widen=False)
    assert candidate.high_hz is not None and candidate.high_hz > 3e6
    assert not (verdict.accepted and short == "")
    candidate, crossing, new, sigma, _, verdict, short = refit_cold(spectrum)
    assert verdict.accepted and short == ""
    assert sigma["total_ohm"] == pytest.approx(128.0, rel=0.001)
    assert new.values()["L1"] == pytest.approx(3e-7, rel=0.1)


def test_an_arc_that_is_really_there_is_not_a_refit_target():
    """아크가 정말 보이는 펠릿 — 아크 없는 회로는 그 모양을 못 그린다.  실측
    `bml refit` (2026-09-25) 이 그런 여덟에 `L1-R0-CPE1` 을 맞춰 모두 3.1–5.9 %
    어긋났다.  이제 그 아크는 커패시턴스대로 "전극 계면" 이라 불리고 (ADR 0047),
    고칠 이름이 없으니 다시 맞출 대상도 아니다 — 매번 헛되이 맞추지 않는다."""
    circuit = "L1-R0-p(R1,CPE1)-CPE2"
    values = {"L1": 1.7e-6, "R0": 8.0, "R1": 200.0, "CPE1_Q": 2e-6, "CPE1_n": 0.9,
              "CPE2_Q": 1e-5, "CPE2_n": 0.9}
    spectrum = spectrum_of(circuit, values)
    before = audit(Fit(circuit, [P(name, value) for name, value in values.items()]),
                   spectrum)
    assert refit_candidates(before.findings) == []
    assert remaining_problems(before.findings) == 0
    (arc,) = before.arcs
    assert arc["label"] == "전극 계면 저항"
    (note,) = [f for f in before.findings if f.code == "arcs_are_electrode"]
    assert note.severity == NOTE and not note.circuits
    assert "R0 = 8 Ω" in note.message


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


def test_a_small_electrode_arc_is_no_longer_swallowed_into_r0():
    """작은 전극 크기 아크 — 예전에는 이름을 고치려고 아크 없는 회로를 권했고,
    그 회로는 아크를 R0 로 삼켜 σ 에 쓰는 저항이 17 % 옮겨 갔다 (그래서
    `moved_number` 가 막았다).  이름이 커패시턴스를 따르니 (ADR 0047) 권할 것이
    없고, σ 는 처음부터 R0 로 맞다."""
    circuit = "L1-R0-p(R1,CPE1)-CPE2"
    values = {"L1": 1.7e-6, "R0": 8.0, "R1": 1.5, "CPE1_Q": 5e-6, "CPE1_n": 0.85,
              "CPE2_Q": 1e-5, "CPE2_n": 0.9}
    spectrum = spectrum_of(circuit, values)
    verdict = blocking_verdict(spectrum.frequency_hz, spectrum.z_re, spectrum.z_im)
    old_fit = Fit(circuit, [P(name, value) for name, value in values.items()])
    before = audit(old_fit, spectrum)
    assert refit_candidates(before.findings) == []
    sigma = ionic_conductivity(old_fit, thickness_cm=PELLET_CM, area_cm2=AREA_CM2,
                               config=SYMMETRIC, blocking=verdict)
    assert sigma["total_ohm"] == 8.0                           # 아크는 전극 쪽이라 뺐다
    assert sigma["electrode_arcs"] == ["R1"]
