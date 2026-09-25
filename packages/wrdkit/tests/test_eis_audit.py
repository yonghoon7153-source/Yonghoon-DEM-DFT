"""The audit of one stored fit (ADR 0040).

The anchor is the cell that started it: `2600922_No1_55_sym_60um_#1_C01`,
fitted with a blocking circuit it did not need.  Its twin -- a cell that
really blocks, fitted with the right circuit -- must come out clean, or the
audit is just noise.
"""

import math
import re
from dataclasses import dataclass

import numpy as np
import pytest
import synthetic_eis as S

from wrdkit.eis.audit import (
    CHECK,
    NOTE,
    PROBLEM,
    _summed_parts,
    _with_wiring,
    audit_conductivity_scan,
    audit_fit,
    audit_record,
    circuit_end,
    config_from_name,
    sort_findings,
    thickness_from_name,
    worst,
)
from wrdkit.eis.circuit import parse_circuit
from wrdkit.eis.conductivity import backwards_steps, backwards_warning
from wrdkit.eis.derive import FULL, LIQUID, SOLID, SYMMETRIC
from wrdkit.eis.fit import fit_circuit
from wrdkit.eis.spectrum import Spectrum

FREQUENCY = S.log_sweep(7e6, 1e-2, 10)
THICKNESS_CM = 60e-4
AREA_CM2 = math.pi / 4
BAND = (float(FREQUENCY.min()), float(FREQUENCY.max()))


@dataclass
class P:
    """A stored parameter, as the API hands it over."""

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


def codes(audit, severity=None):
    return [f.code for f in audit.findings if severity is None or f.severity == severity]


# -- 그 셀 -------------------------------------------------------------------

USER = {"R0": 4.897, "R1": 10.42, "CPE1_Q": 3.06e-5, "CPE1_n": 0.658,
        "R2": 6.635, "CPE2_Q": 1.36e-3, "CPE2_n": 0.757}
USER_SPECTRUM = spectrum_of("R0-p(R1,CPE1)-p(R2,CPE2)", USER)
#: 그 셀에 기본 회로를 씌운 맞춤 — 끝의 CPE3 가 둘 다 경계에 붙었다.
USER_FIT = Fit("R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
               [P(name, value) for name, value in USER.items()]
               + [P("CPE3_Q", 1000.0, "undetermined", "at_upper_bound"),
                  P("CPE3_n", 1.0, "undetermined", "at_upper_bound")])


def audit_user(**overrides):
    kwargs = {"kind": SOLID, "config": SYMMETRIC, "thickness_cm": THICKNESS_CM,
              "area_cm2": AREA_CM2, "band": BAND}
    kwargs.update(overrides)
    return audit_fit(USER_FIT, USER_SPECTRUM, **kwargs)


def test_a_blocking_tail_on_a_cell_that_does_not_block_is_a_problem():
    audit = audit_user()
    (finding,) = [f for f in audit.findings
                  if f.code == "blocking_element_on_open_cell"]
    assert finding.severity == PROBLEM
    assert "CPE3" in finding.message
    assert finding.message.startswith("스펙트럼은 저주파에서 실수축으로 내려오는데 (위상 ")
    # 무엇으로 다시 맞출지까지 — 꼬리를 뺀 같은 회로.
    assert "`R0-p(R1,CPE1)-p(R2,CPE2)`" in finding.message
    assert audit.blocking["blocking"] is False
    assert audit.end == "blocking"
    # 위상 0° 근처가 "-0°" 로 찍히면 부호에 뜻이 있는 것처럼 읽힌다.
    assert "-0°" not in finding.message and "위상 0°" in finding.message


def test_a_vanishing_cpe_is_one_finding_not_three():
    """Q 가 상한이면 n 은 무엇이든 상관없다 — 합성 쌍둥이를 맞추면 n 이 하한
    0.3 에 붙었고, "Q 상한" · "n 하한" · "n = 0.30 확산" 이 함께 떴다.

    스펙트럼이 없으면(무엇이 그 소자를 지우는지 모르면) 사라지는 것 한 줄만."""
    parameters = [P(name, value) for name, value in USER.items()] + [
        P("CPE3_Q", 1000.0, "undetermined", "at_upper_bound"),
        P("CPE3_n", 0.3, "undetermined", "at_lower_bound")]
    audit = audit_fit(Fit(USER_FIT.circuit, parameters), None, kind=SOLID,
                      config=SYMMETRIC, band=BAND)
    about_cpe3 = [f.code for f in audit.findings if "CPE3" in f.message]
    assert about_cpe3 == ["element_vanishing", "undetermined"]


def test_the_cause_explains_the_vanishing_element_once():
    """안 막는 셀에 막는 꼬리를 단 회로 — 그 꼬리가 경계로 가는 **이유**가 이미
    적혔으므로, 경계에 붙은 것·미결정인 것을 다시 적지 않는다."""
    parameters = [P(name, value) for name, value in USER.items()] + [
        P("CPE3_Q", 1000.0, "undetermined", "at_upper_bound"),
        P("CPE3_n", 0.3, "undetermined", "at_lower_bound")]
    audit = audit_fit(Fit(USER_FIT.circuit, parameters), USER_SPECTRUM, kind=SOLID,
                      config=SYMMETRIC, band=BAND)
    about_cpe3 = [f.code for f in audit.findings if "CPE3" in f.message]
    assert about_cpe3 == ["blocking_element_on_open_cell"]


def test_a_series_cpe_with_a_low_n_is_a_diffusion_tail_not_an_arc():
    fit = Fit("R0-p(R1,CPE1)-CPE2", [P("R0", 5.0), P("R1", 20.0), P("CPE1_Q", 1e-9),
                                     P("CPE1_n", 0.95), P("CPE2_Q", 1e-3),
                                     P("CPE2_n", 0.5)])
    audit = audit_fit(fit, None, kind=SOLID, config=SYMMETRIC)
    (finding,) = [f for f in audit.findings if f.code == "cpe_like_diffusion"]
    assert "꼬리" in finding.message and "아크" not in finding.message


def test_the_vanishing_cpe_is_named_for_what_it_is_doing():
    """스펙트럼 없이 맞춤만 보면 — 직렬 CPE 가 사라지려 한다는 한 줄."""
    audit = audit_fit(USER_FIT, None, kind=SOLID, config=SYMMETRIC)
    vanishing = [f for f in audit.findings if f.code == "element_vanishing"]
    assert [f.severity for f in vanishing] == [CHECK]
    assert "CPE3" in vanishing[0].message and "없이" in vanishing[0].message
    # 사라지려는 소자의 n 은 뜻이 없다 — 따로 적지 않는다.
    assert "cpe_ideal" not in codes(audit)


def test_an_ideal_capacitor_that_stays_is_only_a_note():
    """n = 1 에 붙은 것은 이상적인 축전기일 뿐이다 — 틀렸다고 하지 않는다."""
    values = dict(BLOCKING, CPE3_n=1.0)
    parameters = [P(n, v) for n, v in values.items() if n != "CPE3_n"]
    parameters.append(P("CPE3_n", 1.0, "not_checked", "at_upper_bound"))
    audit = audit_fit(Fit(BLOCKING_CIRCUIT, parameters),
                      spectrum_of(BLOCKING_CIRCUIT, values), kind=SOLID,
                      config=SYMMETRIC, band=BAND)
    assert codes(audit) == ["cpe_ideal"]
    assert audit.findings[0].severity == NOTE


def test_both_names_the_capacitances_rule_out_are_replaced():
    """처음 받은 실측 (2026-09-23): "벌크" 4.66e-7 F 와 "입계" 3.0e-4 F.  그때는
    문제 둘이었다.  이제 이름이 커패시턴스를 따르니 (ADR 0047) 어긋날 것이
    없다 — "벌크" 자리는 입계·전극 계면 어느 쪽인지 못 정해 "고주파 아크",
    "입계" 자리는 전기화학 반응뿐이라 "전극 계면 저항"."""
    audit = audit_user()
    assert "label_contradicts_capacitance" not in codes(audit)
    rows = {row["resistor"]: row for row in audit.arcs}
    assert (rows["R1"]["label"], rows["R1"]["claims"]) == ("고주파 아크", None)
    assert (rows["R2"]["label"], rows["R2"]["claims"]) == ("전극 계면 저항", "face")
    # 겉보기 εr 는 아크 줄에 그대로 있다 — 누구나 확인할 수 있는 수다 (ISW 1990).
    assert rows["R1"]["capacitance_f"] == pytest.approx(4.66e-7, rel=0.01)
    assert rows["R1"]["permittivity"] == pytest.approx(4.0e4, rel=0.02)
    assert rows["R2"]["candidates"] == ["reaction"]


def test_the_symmetric_cell_is_told_it_gives_no_conductivity():
    audit = audit_user()
    assert "symmetric_cell_does_not_block" in codes(audit, CHECK)


def test_the_fit_itself_draws_through_the_points():
    """The curve was fine -- the circuit's *meaning* was not.  That is the
    whole reason chi-square never flagged this cell."""
    audit = audit_user()
    assert audit.misfit.mean < 1e-3
    # 거의 완벽한 맞춤에서도 "가장 작은 오차들" 은 어딘가에 몰려 있다 — 그것을
    # 적으면 잡음이다 (처음 판에서 "오차의 98 % 가 저주파에" 가 떴다).
    assert not {"misfit_everywhere", "misfit_somewhere",
                "misfit_at_edge"} & set(codes(audit))
    assert worst(audit.findings) == PROBLEM


def test_without_geometry_the_names_are_not_judged():
    audit = audit_user(thickness_cm=None)
    assert "label_contradicts_capacitance" not in codes(audit)
    assert all(row["candidates"] is None for row in audit.arcs)


def test_a_full_cell_makes_no_claim_the_capacitance_could_contradict():
    audit = audit_user(config=FULL)
    assert "label_contradicts_capacitance" not in codes(audit)
    assert "symmetric_cell_does_not_block" not in codes(audit)


# -- 진짜로 막는 셀 ---------------------------------------------------------------

BLOCKING_CIRCUIT = "R0-p(R1,C1)-p(R2,CPE2)-CPE3"
#: 벌크 1e-10 F (C·l/A 7.6e-13), 입계 5.0e-8 F (C·l/A 3.8e-10), 이중층 1e-5.
BLOCKING = {"R0": 2.0, "R1": 1000.0, "C1": 1e-10, "R2": 2000.0,
            "CPE2_Q": 2e-7, "CPE2_n": 0.85, "CPE3_Q": 1e-5, "CPE3_n": 0.9}


def test_a_cell_that_really_blocks_with_the_right_circuit_is_clean():
    spectrum = spectrum_of(BLOCKING_CIRCUIT, BLOCKING)
    fit = Fit(BLOCKING_CIRCUIT, [P(n, v) for n, v in BLOCKING.items()])
    audit = audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=THICKNESS_CM, area_cm2=AREA_CM2, band=BAND)
    assert audit.findings == []
    assert audit.blocking["blocking"] is True
    rows = {row["resistor"]: row for row in audit.arcs}
    assert rows["R1"]["candidates"] == ["bulk"]
    assert "grain_boundary" in rows["R2"]["candidates"]


def test_a_blocking_cell_whose_circuit_closes_on_the_real_axis_is_flagged():
    spectrum = spectrum_of(BLOCKING_CIRCUIT, BLOCKING)
    values = {k: v for k, v in BLOCKING.items() if not k.startswith("CPE3")}
    fit = Fit("R0-p(R1,C1)-p(R2,CPE2)", [P(n, v) for n, v in values.items()])
    audit = audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC, band=BAND)
    assert "open_end_on_blocking_cell" in codes(audit, CHECK)
    # 곡선이 꼬리를 못 따라가는 것도 함께 보인다.
    assert "misfit_everywhere" in codes(audit) or "misfit_at_edge" in codes(audit)


def test_an_arc_whose_apex_is_above_the_sweep_is_extrapolated():
    """Sulfide pellets: the bulk arc peaks far above 7 MHz."""
    values = dict(BLOCKING, R1=10.0)            # f0 = 1/(2π·1e-9) ≈ 160 MHz
    spectrum = spectrum_of(BLOCKING_CIRCUIT, values)
    fit = Fit(BLOCKING_CIRCUIT, [P(n, v) for n, v in values.items()])
    audit = audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=THICKNESS_CM, area_cm2=AREA_CM2, band=BAND)
    (finding,) = [f for f in audit.findings if f.code == "arc_apex_above_window"]
    assert finding.severity == CHECK and "R1" in finding.message


def test_an_electrode_arc_that_sigma_leaves_out_is_only_noted_when_its_apex_is_outside():
    """ADR 0047 보완 1 — 실측 B18 #5 (2026-09-25, 배선 L 을 붙여 다시 맞춘 뒤): 막는
    펠릿의 전극 아크 꼭지가 9.35 Hz 로 옮겨 10 Hz 창 끝 바로 아래가 되자 "꼭지가 구간
    아래" 하나로 확인에 남았다.  σ 는 그 아크를 빼고 R0 로 낸다 — 그 저항은 이 셀의
    어느 수에도 들지 않는다.  참고로 적는다."""
    from wrdkit.eis.derive import blocking_verdict, ionic_conductivity

    circuit = "L1-R0-p(R1,CPE1)-CPE3"
    values = {"L1": 1.88e-6, "R0": 9.61, "R1": 2.94e3, "CPE1_Q": 1.43e-5,
              "CPE1_n": 0.777, "CPE3_Q": 1.53e-6, "CPE3_n": 0.908}
    frequency = S.log_sweep(7e6, 10.0, 10)
    model = parse_circuit(circuit)
    z = model.impedance([values[name] for name in model.parameter_names], frequency)
    spectrum = Spectrum(frequency, z.real, z.imag)
    fit = Fit(circuit, [P(n, v) for n, v in values.items()])
    band = (10.0, 1.71e5)
    cell = {"kind": SOLID, "config": SYMMETRIC, "thickness_cm": 0.08, "area_cm2": 0.785}
    sigma = ionic_conductivity(fit, thickness_cm=0.08, area_cm2=0.785, config=SYMMETRIC,
                               blocking=blocking_verdict(spectrum.frequency_hz,
                                                         spectrum.z_re, spectrum.z_im))
    assert sigma["electrode_arcs"] == ["R1"] and sigma["total_ohm"] == 9.61

    noted = audit_fit(fit, spectrum, band=band, conductivity=sigma, **cell)
    (apex,) = [f for f in noted.findings if f.code == "arc_apex_below_window"]
    assert apex.severity == NOTE
    assert apex.message.endswith("σ 에 안 드는 전극 쪽 아크라 이 셀의 수에는 들지 않습니다")
    assert codes(noted, CHECK) == [] and codes(noted, PROBLEM) == []
    # σ 를 모르면(전도도를 안 물었으면) 전처럼 확인이다 — 그 저항이 쓰일 수 있다.
    (bare,) = [f for f in audit_fit(fit, spectrum, band=band, **cell).findings
               if f.code == "arc_apex_below_window"]
    assert bare.severity == CHECK


def test_the_only_series_resistor_at_zero_is_not_to_be_left_out():
    """실측 하프셀 #28: R0 = 1e-9 Ω 에 "이 저항은 없어도 되는 소자입니다" 가 붙었다.
    셀의 직렬 저항(배선·전해질)은 0 이 될 수 없다 — n = 0.40 인 첫 아크가 고주파
    절편을 그리고 있었다."""
    circuit = "R0-p(R1,CPE1)-CPE2"
    values = {"R0": 1e-9, "R1": 9.94, "CPE1_Q": 2.42e-4, "CPE1_n": 0.397,
              "CPE2_Q": 1e-3, "CPE2_n": 0.85}
    fit = Fit(circuit, [P(n, v, reason="at_lower_bound" if n == "R0" else "")
                        for n, v in values.items()])
    (gone,) = [f for f in audit_fit(fit, spectrum_of(circuit, values), kind=LIQUID,
                                    band=BAND).findings if f.message.startswith("R0 이 0")]
    assert gone.code == "series_resistance_gone"
    assert "직렬 저항" in gone.message and "없어도 되는" not in gone.message
    # 절편을 가져간 소자를 이름으로 — 그 아크가 고주파에서 실수부를 그린다.
    assert "가져간 것은 `p(R1,CPE1)`" in gone.message

    # 직렬 저항이 둘이면 0 이 된 쪽은 정말 없어도 된다.
    circuit = "R0-R1-p(R2,CPE2)"
    values = {"R0": 5.0, "R1": 1e-9, "R2": 20.0, "CPE2_Q": 1e-5, "CPE2_n": 0.9}
    fit = Fit(circuit, [P(n, v, reason="at_lower_bound" if n == "R1" else "")
                        for n, v in values.items()])
    (spare,) = [f for f in audit_fit(fit, spectrum_of(circuit, values), kind=LIQUID,
                                     band=BAND).findings if f.message.startswith("R1 이 0")]
    assert spare.code == "element_vanishing" and "없어도 되는 소자" in spare.message


def test_a_series_resistor_too_small_to_see_is_at_zero_too():
    """실측 풀셀 #13: R0 = 3.7e-4 Ω — 경계(1e-9)의 1 % 밖이라 경계 판정을 비껴가
    아무 말이 없었다.  전송선의 두 레일(25 ∥ 80 Ω = 19 Ω)이 고주파 절편을
    가져갔다.  B17 0 °C (#150) 의 R0 = 2.4e-9 Ω 도 같았다."""
    circuit = "L1-R0-p(R1,CPE1)-TL1"
    values = {"L1": 4.22e-7, "R0": 3.72e-4, "R1": 258.0, "CPE1_Q": 3.01e-5,
              "CPE1_n": 0.748, "TL1_Ri": 25.1, "TL1_Re": 80.1, "TL1_Rct": 30.1,
              "TL1_Q": 1.73e-5, "TL1_n": 0.688, "TL1_Wr": 335.0, "TL1_Wn": 0.276,
              "TL1_Wt": 6.94e3}

    def audited(values):
        fit = Fit(circuit, [P(n, v) for n, v in values.items()])
        return audit_fit(fit, spectrum_of(circuit, values), kind=SOLID, config=FULL,
                         band=BAND)

    (gone,) = [f for f in audited(values).findings
               if f.code == "series_resistance_gone"]
    assert gone.message.startswith("R0 이 0") and "0.000372 Ω" in gone.message
    # 아크가 아니라 전송선의 두 레일(25 ∥ 80 Ω = 19 Ω)이다 — "n 이 낮은 CPE" 가 아니다.
    assert "가져간 것은 `TL1`" in gone.message and "n 이 낮은" not in gone.message

    # 절편을 정말 나눠 가진 작은 R0 은 그대로 둔다 — 실측 #12: 0.42 Ω, 절편 3 Ω.
    values.update(R0=0.416, TL1_Ri=1.6e3, TL1_Re=2.64)
    assert "series_resistance_gone" not in codes(audited(values))


def test_an_element_that_is_not_an_arc_has_no_apex():
    """실측 풀셀 #5: CPE1 의 n 이 하한 0.3 — 목록은 "반원이 아니라 확산" 이라
    판정하지 않는데, 꼭지 1e8 Hz 가 "맞춘 구간 위 — 반원의 꼭대기를 못 보고 정한
    저항" 으로 한 줄 더 붙었다 (실측 여덟 건)."""
    values = {"R0": 5.0, "R1": 8.0, "CPE1_Q": 2.8e-4, "CPE1_n": 0.3,
              "CPE2_Q": 1e-5, "CPE2_n": 0.9}
    spectrum = spectrum_of("R0-p(R1,CPE1)-CPE2", values)
    fit = Fit("R0-p(R1,CPE1)-CPE2",
              [P(n, v, reason="at_lower_bound" if n == "CPE1_n" else "")
               for n, v in values.items()])
    audit = audit_fit(fit, spectrum, kind=LIQUID, band=BAND)
    assert not [c for c in codes(audit) if c.startswith("arc_apex")]
    assert "at_bound" in codes(audit, CHECK)          # n 의 경계 붙음은 그대로


def test_an_arc_whose_resistance_went_to_zero_is_one_finding():
    """실측 하프셀 #39: R1 = 1.13e-9 Ω — 경계(1e-9)의 1 % 밖이라 경계 판정을
    비껴갔고, 꼭지 3.6e19 Hz 가 "맞춘 구간 위" 로 적혔다.  0 Ω 인 아크는 아크가
    아니다: "R1 이 0" 한 줄만 적고, 그 CPE 의 n·꼭지·이름은 말하지 않는다."""
    values = {"R0": 6.68, "R1": 1.13e-9, "CPE1_Q": 3.96e-12, "CPE1_n": 1.0,
              "R2": 37.0, "CPE2_Q": 7.64e-4, "CPE2_n": 0.62,
              "CPE3_Q": 0.2, "CPE3_n": 0.8}
    circuit = "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"
    spectrum = spectrum_of(circuit, values)
    fit = Fit(circuit, [P(n, v, reason="at_upper_bound" if n == "CPE1_n" else "")
                        for n, v in values.items()])
    audit = audit_fit(fit, spectrum, kind=LIQUID, band=BAND)
    (gone,) = [f for f in audit.findings if f.code == "element_vanishing"]
    assert gone.message.startswith("R1 이 0 에 붙었습니다 (1.13e-09 Ω)")
    assert not [c for c in codes(audit) if c.startswith("arc_apex")]
    assert "cpe_ideal" not in codes(audit)            # CPE1 의 n = 1 은 그 아크의 일
    (row,) = [one for one in audit.arcs if one["resistor"] == "R1"]
    assert row["candidates"] is None and "아크가 아닙니다" in row["reason"]

    # 경계에 딱 붙은 저항도 같다 — 그 옆 CPE 의 n 이 하한에 붙은 것은 따로 적지 않는다.
    values.update(R1=1e-9, CPE1_n=0.3)
    fit = Fit(circuit, [P(n, v, reason={"R1": "at_lower_bound",
                                         "CPE1_n": "at_lower_bound"}.get(n, ""))
                        for n, v in values.items()])
    found = audit_fit(fit, spectrum, kind=LIQUID, band=BAND).findings
    assert [f.message.split(" —")[0] for f in found if "CPE1" in f.message
            or f.code == "element_vanishing"] == ["R1 이 0 에 붙었습니다 (1e-09 Ω)"]

    # 옆 Q 가 하한에 붙어도 원인은 0 Ω 이다 (실측 #47: R1 = 1.07e-9, CPE1_Q = 1e-15).
    values.update(R1=1.07e-9, CPE1_Q=1e-15, CPE1_n=0.3)
    fit = Fit(circuit, [P(n, v, reason={"CPE1_Q": "at_lower_bound",
                                         "CPE1_n": "at_lower_bound"}.get(n, ""))
                        for n, v in values.items()])
    found = audit_fit(fit, spectrum, kind=LIQUID, band=BAND).findings
    assert [f.message.split(" —")[0] for f in found if "CPE1" in f.message
            or f.code == "element_vanishing"] == ["R1 이 0 에 붙었습니다 (1.07e-09 Ω)"]


# -- 곡선이 점을 못 지나갈 때 -------------------------------------------------------

def test_a_circuit_that_misses_everywhere_says_so():
    spectrum = spectrum_of("R0-p(R1,CPE1)", {"R0": 5.0, "R1": 20.0,
                                             "CPE1_Q": 1e-5, "CPE1_n": 0.9})
    fit = Fit("R0-p(R1,CPE1)", [P("R0", 5.0), P("R1", 40.0),
                                P("CPE1_Q", 1e-5), P("CPE1_n", 0.9)])
    audit = audit_fit(fit, spectrum, kind=LIQUID, band=BAND)
    assert "misfit_everywhere" in codes(audit, CHECK)
    assert audit.misfit.mean > 0.03


def test_misfit_piled_up_at_the_low_end_points_at_a_new_lower_bound():
    """A process whose apex is below the sweep: the last points are the start
    of something nobody measured, and the rest of the fit is fine."""
    base = {"R0": 5.0, "R1": 20.0, "CPE1_Q": 1e-5, "CPE1_n": 0.9}
    clean = spectrum_of("R0-p(R1,CPE1)", base)
    w = 2 * np.pi * FREQUENCY
    # 스윕 아래에서 시작하는 꼬리: 10 mHz 에서 약 20 %, 1 Hz 에서 0.3 %.
    extra = 1.0 / (2.5 * (1j * w) ** 0.9)
    z = clean.z + extra
    spectrum = Spectrum(FREQUENCY, z.real, z.imag)
    fit = Fit("R0-p(R1,CPE1)", [P(n, v) for n, v in base.items()])
    audit = audit_fit(fit, spectrum, kind=LIQUID, band=BAND)
    (edge,) = [f for f in audit.findings if f.code == "misfit_at_edge"]
    assert edge.severity == CHECK
    assert "하한" in edge.message
    assert audit.misfit.mean < 0.03                # 나머지는 멀쩡하다
    assert not {"misfit_somewhere", "misfit_everywhere"} & set(codes(audit))


# -- 파라미터 하나하나 -------------------------------------------------------------

def test_a_resistor_on_zero_inside_an_arc_takes_the_arc_with_it():
    fit = Fit("R0-p(R1,CPE1)", [P("R0", 5.0), P("R1", 1e-9, "undetermined",
                                                "at_lower_bound"),
                                P("CPE1_Q", 1e-5), P("CPE1_n", 0.9)])
    audit = audit_fit(fit, None, kind=LIQUID)
    (finding,) = [f for f in audit.findings if f.code == "element_vanishing"]
    assert "아크" in finding.message


def test_bounds_are_found_from_the_circuit_when_the_row_is_old():
    """Rows saved before ``reason`` existed still carry the value."""
    fit = Fit("R0-p(R1,CPE1)", [P("R0", 1e-9, "legacy_unknown"),
                                P("R1", 20.0, "legacy_unknown"),
                                P("CPE1_Q", 1e-5, "legacy_unknown"),
                                P("CPE1_n", 0.9, "legacy_unknown")])
    audit = audit_fit(fit, None, kind=LIQUID)
    # 하나뿐인 직렬 저항이라 "없어도 된다" 가 아니다 (셀의 직렬 저항은 0 이 될 수 없다).
    (finding,) = [f for f in audit.findings if f.code == "series_resistance_gone"]
    assert "R0" in finding.message and "직렬 저항" in finding.message
    assert "legacy_fit" in codes(audit, NOTE)


def test_a_cpe_that_is_really_a_diffusion_line_is_not_read_as_an_arc():
    fit = Fit("R0-p(R1,CPE1)-p(R2,CPE2)",
              [P("R0", 5.0), P("R1", 20.0), P("CPE1_Q", 1e-9), P("CPE1_n", 0.95),
               P("R2", 40.0), P("CPE2_Q", 1e-3), P("CPE2_n", 0.5)])
    audit = audit_fit(fit, None, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=THICKNESS_CM, area_cm2=AREA_CM2)
    (finding,) = [f for f in audit.findings if f.code == "cpe_like_diffusion"]
    assert "CPE2" in finding.message
    rows = {row["resistor"]: row for row in audit.arcs}
    assert rows["R2"]["candidates"] is None
    assert "label_contradicts_capacitance" not in [
        f.code for f in audit.findings if "R2" in f.message]


def test_an_undetermined_arc_far_outside_is_still_renamed():
    """미결정 값은 몇 배 흔들리지, 벌크와 이중층 사이의 네 자릿수를 건너지
    않는다.  실측 B11 스캔의 "벌크" 들은 벌크 상한의 수만 배였는데 전부
    미결정이라 판정에서 빠졌었다 — 열 배 흔들어도 벌크가 아니면 이름이
    바뀐다 (ADR 0047)."""
    parameters = [P(name, value) for name, value in USER.items()]
    parameters[1] = P("R1", USER["R1"], "undetermined", "seed_spread")
    fit = Fit("R0-p(R1,CPE1)-p(R2,CPE2)", parameters)
    audit = audit_fit(fit, USER_SPECTRUM, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=THICKNESS_CM, area_cm2=AREA_CM2, band=BAND)
    rows = {row["resistor"]: row for row in audit.arcs}
    assert rows["R1"]["label"] == "고주파 아크"
    assert "label_contradicts_capacitance" not in codes(audit)
    assert "capacitance_not_judged" not in codes(audit)


def test_an_undetermined_arc_near_its_range_is_not_judged():
    """벌크 상한(C·l/A 1e-11)을 세 배만 넘는 미결정 아크 — 흔들림 안이다."""
    per_length = 3e-11
    capacitance = per_length * AREA_CM2 / THICKNESS_CM
    fit = Fit("R0-p(R1,C1)", [P("R0", 2.0), P("R1", 50.0, "undetermined", "seed_spread"),
                              P("C1", capacitance)])
    audit = audit_fit(fit, None, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=THICKNESS_CM, area_cm2=AREA_CM2)
    assert "label_contradicts_capacitance" not in codes(audit)
    assert "capacitance_not_judged" in codes(audit, NOTE)


def test_a_conductivity_no_electrolyte_can_have_points_at_the_units():
    fit = Fit("R0-p(R1,CPE1)", [P(n, v) for n, v in
                                {"R0": 5.0, "R1": 20.0, "CPE1_Q": 1e-9,
                                 "CPE1_n": 0.95}.items()])
    audit = audit_fit(fit, None, kind=SOLID, config=SYMMETRIC,
                      conductivity={"total_s_cm": 3.2})
    (finding,) = [f for f in audit.findings if f.code == "sigma_out_of_range"]
    assert "단위" in finding.message


def test_an_unreadable_circuit_stops_the_audit_with_a_reason():
    audit = audit_fit(Fit("R0-p(R1", []), None, kind=LIQUID)
    assert codes(audit, PROBLEM) == ["circuit_unreadable"]


def test_a_fresh_fit_result_is_audited_by_the_same_code():
    frequency = S.log_sweep(1e6, 1e-2, 8)
    z = S.randles(frequency, q_block=1e-2)
    spectrum = Spectrum(frequency, z.real, z.imag)
    result = fit_circuit(spectrum, "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3")
    audit = audit_fit(result, spectrum, kind=SOLID, config=SYMMETRIC,
                      band=(float(frequency.min()), float(frequency.max())))
    assert audit.blocking["blocking"] is True
    assert "blocking_element_on_open_cell" not in codes(audit)
    assert audit.misfit.mean < 0.01


# -- 회로의 저주파 끝 ------------------------------------------------------------

@pytest.mark.parametrize(("circuit", "end"), [
    ("R0-p(R1,CPE1)-CPE3", "blocking"),
    ("CPE3-R0-p(R1,CPE1)", "blocking"),             # 자리는 상관없다
    ("R0-p(R1,CPE1)-Wo2", "blocking"),              # 반사 경계
    ("R0-p(R1,CPE1)-Ws2", "resistive"),             # 투과 경계
    ("R0-p(R1,CPE1)-W2", "diffusive"),
    ("R0-TL1", "blocking"),                         # 입자 확산이 반사 경계
    ("L1-R0-p(R1,CPE1)-TL1", "blocking"),
    ("L1-R0-p(R1,CPE1)-TLR1", "resistive"),         # 계면이 Rct ∥ CPE
    ("L1-R0-p(R1,CPE1)-p(R2,CPE2)", "resistive"),
    ("R0-p(R1,CPE1,C1)", "resistive"),
])
def test_how_the_circuit_closes(circuit, end):
    assert circuit_end(circuit) == end


# -- 기록 -------------------------------------------------------------------------

def test_names_are_read_the_way_the_screen_reads_them():
    assert thickness_from_name("260719_No1_55_70um_sym_01") == 70
    assert thickness_from_name("2600922_No1_55_sym_60um_#1_C01") == 60
    assert thickness_from_name("pellet_1.5mm") is None
    assert config_from_name("2600922_No1_55_sym_60um_#1_C01") == "sym"
    assert config_from_name("symmetry_test") is None
    assert config_from_name("LiFull_01") is None
    assert config_from_name("NCM_half_03") == "half"


def test_a_thickness_ten_times_the_name_is_caught():
    found = audit_record(name="2600922_No1_55_sym_60um_#1", kind=SOLID,
                         config=SYMMETRIC, thickness_um=600.0, area_cm2=0.785)
    (finding,) = [f for f in found if f.code == "thickness_differs_from_name"]
    assert finding.severity == CHECK and "10배" in finding.message


def test_record_gaps_and_impossible_sizes():
    found = audit_record(name="pellet_full_02", kind=SOLID, config="",
                         thickness_um=60000.0, area_cm2=78.5, n_points=6)
    got = {f.code for f in found}
    assert got == {"config_missing", "config_differs_from_name",
                   "thickness_out_of_range", "area_out_of_range", "few_points"}


def test_a_symmetric_cell_without_geometry_is_told_what_it_loses():
    found = audit_record(name="pellet_sym_02", kind=SOLID, config=SYMMETRIC,
                         thickness_um=None, area_cm2=0.785)
    (finding,) = [f for f in found if f.code == "geometry_missing"]
    assert finding.severity == NOTE and "두께가 없습니다" in finding.message
    both = audit_record(name="pellet_sym_02", kind=SOLID, config=SYMMETRIC)
    assert "두께·면적이 없습니다" in both[0].message


def test_a_clean_record_says_nothing():
    assert audit_record(name="2600922_No1_55_sym_60um_#1", kind=SOLID,
                        config=SYMMETRIC, thickness_um=60.0, area_cm2=0.785,
                        n_points=59) == []


# -- 온도 스캔 ---------------------------------------------------------------------

def test_a_scan_with_a_decimal_slip_and_a_blank_temperature():
    sweeps = [
        {"index": 1, "temperature_c": 60.0, "typed_ohm": 7.37,
         "re_min_ohm": 7.2, "re_max_ohm": 40.0},
        {"index": 2, "temperature_c": None, "typed_ohm": 79.89,
         "re_min_ohm": 7.9, "re_max_ohm": 45.0},
        {"index": 3, "temperature_c": 40.0, "typed_ohm": None,
         "re_min_ohm": 9.0, "re_max_ohm": 50.0},
    ]
    found = audit_scan(sweeps)
    got = [f.code for f in found]
    assert got[:2] == ["temperatures_partly_missing", "typed_outside_spectrum"]
    slip = found[1]
    assert "스윕 2" in slip.message and "7.9–45" in slip.message
    assert "resistance_partly_missing" in got


def test_reading_the_right_end_of_a_visible_arc_is_not_a_slip():
    """아크가 보이면 랩은 그 오른쪽 끝을 읽는다 — 고주파 교점의 몇 배다.
    처음 규칙("교점의 세 배")은 이것을 소수점 실수로 적었다."""
    sweeps = [{"index": 1, "temperature_c": 60.0, "typed_ohm": 9.69,
               "crossing_ohm": 2.0, "re_min_ohm": 0.4, "re_max_ohm": 9.7}]
    assert audit_scan(sweeps) == []


def audit_scan(sweeps, **kwargs):
    return audit_conductivity_scan(sweeps, **kwargs)


def test_the_activation_energy_warnings_come_along():
    sweeps = [{"index": 1, "temperature_c": 60.0, "typed_ohm": 7.0,
               "re_min_ohm": 6.9, "re_max_ohm": 30.0}]
    found = audit_scan(sweeps, warnings=["직선이 점들을 설명하지 못합니다"],
                       reason="점이 모자랍니다")
    assert [f.code for f in found] == ["activation_warning", "activation_missing"]


def test_the_ea_the_fits_draw_is_said_beside_the_typed_one():
    """ADR 0039 보완 1: 적은 저항(대개 실수축 교점)은 양 끝에서 반대로 틀려 Ea 를
    작게 만든다 — 실측 B14 는 0.297 eV, 맞춤 R0 로는 0.311 eV 였다.  스캔의 Ea 는
    적은 값 그대로이고, 맞춤의 것은 옆에 적는다 (참고)."""
    sweeps = [{"index": i, "temperature_c": t, "typed_ohm": 10.0,
               "re_min_ohm": 5.0, "re_max_ohm": 50.0}
              for i, t in enumerate((60.0, 40.0, 20.0), start=1)]
    (beside,) = audit_scan(sweeps, typed_ev=0.297, fit_ev=(0.311, 0.998, 3))
    assert beside.severity == NOTE and beside.code == "activation_from_fit"
    assert beside.message == (
        "맞춤의 전해질 저항으로 내면 Ea = 0.311 eV (R² = 0.998, 스윕 3개) — 적은 "
        "저항으로 낸 이 스캔의 Ea(0.297 eV)보다 4.7 % 큽니다")
    (fewer,) = audit_scan(sweeps, typed_ev=0.311, fit_ev=(0.297, 0.99, 2))
    assert "스윕 3개 중 2개" in fewer.message and "4.5 % 작습니다" in fewer.message
    (alone,) = audit_scan(sweeps, fit_ev=(0.311, 0.998, 3))
    assert alone.message.endswith("적은 저항으로는 아직 Ea 가 없습니다")
    (why,) = audit_scan(sweeps, typed_ev=0.297, fit_missing="점이 모자랍니다")
    assert why.message == "맞춤의 전해질 저항으로는 Ea 가 안 나옵니다 — 점이 모자랍니다"
    assert audit_scan(sweeps, typed_ev=0.297) == []
    # 까닭이 적은 값의 것과 같으면 (실측 B17_ACTI E: 온도를 안 적었다) 한 번만 적는다.
    same = "온도와 이온전도도가 모두 적힌 스윕이 둘 이상이어야 직선이 섭니다 (지금 0개)"
    assert [f.code for f in audit_scan(sweeps, reason=same, fit_missing=same)] == [
        "activation_missing"]


def test_a_scan_with_nothing_written_yet_is_only_noted():
    sweeps = [{"index": i, "temperature_c": None, "typed_ohm": None,
               "re_min_ohm": 6.9, "re_max_ohm": 30.0} for i in (1, 2, 3)]
    found = audit_scan(sweeps)
    assert {f.severity for f in found} == {NOTE}


def test_findings_sort_worst_first():
    from wrdkit.eis.audit import Finding
    mixed = [Finding(NOTE, "a", ""), Finding(PROBLEM, "b", ""), Finding(CHECK, "c", "")]
    assert [f.code for f in sort_findings(mixed)] == ["b", "c", "a"]
    assert worst([]) is None


# -- 실측 2026-09-23 검수에서 나온 모양들 ------------------------------------------
#
# 연구실 PC 의 131 스펙트럼을 검수했더니 한 원인이 여러 줄로 반복됐다.  아래는
# 그 보고서의 맞춤값을 그대로 옮긴 것이다 — 스펙트럼은 그 셀이 실제로 어떻게
# 생겼을지를 합성했다 (황화물 블로킹 펠릿: 배선 L + 전해질 R + 이중층 CPE).

SULFIDE_FREQUENCY = S.log_sweep(7e6, 10.0, 10)
SULFIDE_BAND = (10.0, 2.15e5)            # 보고서의 맞춘 구간


def sulfide_pellet(r0=8.3, q=1.9e-6, n=0.86, inductance=1.73e-6):
    w = 2 * np.pi * SULFIDE_FREQUENCY
    z = r0 + 1j * w * inductance + 1.0 / (q * (1j * w) ** n)
    return Spectrum(SULFIDE_FREQUENCY, z.real, z.imag)


PELLET_CM = 700e-4                       # B15: 700 µm, 10 mm


def test_an_arc_that_is_the_blocking_tail_is_said_once():
    """B15 #2 (50 °C): `R0-p(R1,CPE1)` 로 맞춘 블로킹 펠릿.  보고서는 한 원인을
    셋으로 적었다 — 회로가 실수축으로 닫힌다 · R1 은 벌크일 수 없다 · R1 의
    꼭지가 구간 아래.  R1 은 반원이 아니라 꼬리이고, 전해질은 R0 다."""
    fit = Fit("R0-p(R1,CPE1)", [P("R0", 7.89), P("R1", 1.37e5), P("CPE1_Q", 1.95e-6),
                                P("CPE1_n", 0.856)])
    audit = audit_fit(fit, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=["R0-TL1", "L1-R0-CPE1", "R0-p(R1,CPE1)-CPE2"])
    (tail,) = [f for f in audit.findings if f.code == "tail_mimicked_by_arc"]
    assert tail.severity == PROBLEM
    assert "R1 (전극 계면 저항)" in tail.message         # 커패시턴스가 붙인 이름
    assert "R0 = 7.89 Ω" in tail.message                 # 전해질이 어디 있는지
    # 막는 계면의 커패시턴스는 Brug 의 식(Hirschorn 2010 식 12)에 옴 저항 R0 를
    # 넣어 낸다.  R1 (꼬리의 높이, 외삽값) 로 낸 1.56e-6 F 는 그 경계를 따라간다.
    assert "3.02e-07 F" in tail.message
    assert "1.56e-06" not in tail.message
    assert "`L1-R0-CPE1`" in tail.message                # 막는 끝을 가진 대안만
    assert "`R0-TL1`" not in tail.message
    for repeated in ("open_end_on_blocking_cell", "label_contradicts_capacitance",
                     "arc_apex_below_window"):
        assert repeated not in codes(audit)


def test_a_missing_inductance_is_named_as_the_cause_of_the_top_misfit():
    """같은 스캔에서 L1 을 단 첫 스윕은 최대 1.4–3.7 %, 나머지는 11–30 % 였다 —
    전부 맞춘 구간의 꼭대기에서."""
    fit = Fit("R0-p(R1,CPE1)", [P("R0", 7.89), P("R1", 1.37e5), P("CPE1_Q", 1.95e-6),
                                P("CPE1_n", 0.856)])
    audit = audit_fit(fit, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      band=SULFIDE_BAND)
    (hint,) = [f for f in audit.findings if f.code == "inductance_missing"]
    assert "`L1-`" in hint.message
    assert "misfit_somewhere" not in codes(audit)
    # `bml refit` 이 문장을 긁지 않고 이것으로 다시 맞춘다 (ADR 0045 보완 8).
    assert hint.circuits == ("L1-R0-p(R1,CPE1)",)
    share, hz = audit.top_misfit
    assert share >= 0.10 and hz >= SULFIDE_BAND[1] / 2

    with_l = Fit("L1-R0-CPE1", [P("L1", 1.73e-6), P("R0", 8.3), P("CPE1_Q", 1.9e-6),
                                P("CPE1_n", 0.86)])
    clean = audit_fit(with_l, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND)
    assert clean.findings == []
    assert clean.top_misfit is None


def test_the_top_end_symptom_is_kept_when_the_circuit_has_an_l_that_does_nothing():
    """L 이 0 이면 L 이 없는 것과 같다 — 판정(`inductance_missing`)은 L 이 있어 안
    뜨지만 증상은 남는다.  `bml refit` 이 `L1-` 를 붙인 맞춤을 받을지 이것으로
    본다 (ADR 0045 보완 8)."""
    idle = Fit("L1-R0-CPE1", [P("L1", 1e-12), P("R0", 8.3), P("CPE1_Q", 1.9e-6),
                              P("CPE1_n", 0.86)])
    audit = audit_fit(idle, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      band=SULFIDE_BAND)
    assert "inductance_missing" not in codes(audit)
    assert audit.top_misfit is not None and audit.top_misfit[0] >= 0.10


def test_the_offered_inductor_takes_a_name_the_circuit_does_not_use():
    """직렬에 L 이 없어도 병렬 가지 안에 L1 이 있을 수 있다 — 같은 이름 둘은
    회로가 못 읽는다."""
    assert _with_wiring(parse_circuit("R0-p(R1,CPE1)")) == "L1-R0-p(R1,CPE1)"
    offered = _with_wiring(parse_circuit("R0-p(R1,L1)-CPE2"))
    assert offered == "L2-R0-p(R1,L1)-CPE2"
    parse_circuit(offered)


def cold_pellet():
    """B15 #9 (-20 °C) 처럼 식은 펠릿: 배선 L 2 µH, 90 Ω 뒤에 잰 주파수 안으로
    내려온 전해질 아크 (46 Ω, 꼭지 300 kHz), 그 뒤 블로킹 꼬리.  전해질 저항은
    90 + 46 = 136 Ω 이다."""
    w = 2 * np.pi * SULFIDE_FREQUENCY
    tau = 1 / (2 * np.pi * 3e5)
    z = (2e-6j * w + 90.0 + 46.0 / (1 + (1j * w * tau) ** 0.9)
         + 1 / (6.3e-7 * (1j * w) ** 0.87))
    return Spectrum(SULFIDE_FREQUENCY, z.real, z.imag)


def test_an_inductor_on_zero_with_r0_above_the_crossing_is_an_arc_above_the_window():
    """실측 B15 #9 (-20 °C, 열두 번째 검수): `L1-R0-CPE1` 의 L1 = 1e-12, R0 136 Ω,
    실수축 교점 115 Ω, 꼭대기 유도 5점 — 그 5점 옆에 "이 파일에는 배선 인덕턴스가
    안 보입니다" 가 적혔다.  R0 에 CPE 를 이은 회로는 R0 아래의 실수부를 못
    그린다 — 교점이 R0 아래면 구간 위에 회로에 없는 아크가 있다.  합성하면 같은
    모양이 나온다: L1 은 0, 가장 크게 어긋난 곳은 171 kHz (실측도 171 kHz)."""
    spectrum = cold_pellet()
    result = fit_circuit(spectrum, "L1-R0-CPE1", frequency_range=SULFIDE_BAND)
    values = result.values()
    assert values["L1"] < 1e-9                              # 인덕턴스를 버렸다
    audit = audit_fit(result, spectrum, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=PRESETS)
    (arc,) = [f for f in audit.findings if f.code == "arc_above_window"]
    assert arc.severity == CHECK
    assert "L1 이 0 에 붙었는데 꼭대기 9점은 유도성입니다" in arc.message
    assert "R0 130.9 Ω 이 실수축 교점 96.04 Ω 보다 36 % 큽니다" in arc.message
    assert "`L1-R0-p(R1,CPE1)-CPE2`" in arc.message
    # 확인인데도 회로를 싣는다 — `bml refit` 이 차가운 펠릿을 다시 맞춘다 (ADR 0045 보완 10).
    assert arc.circuits == ("L1-R0-p(R1,CPE1)-CPE2",)
    series, crossing = audit.above_crossing
    assert series == pytest.approx(values["R0"]) and crossing == pytest.approx(96.04, abs=0.01)
    assert "no_inductance" not in codes(audit)
    assert not any("안 보입니다" in f.message for f in audit.findings)
    # "R0 도 모자랄 수 있습니다": 교점 < R0 < 참값.  아크 하나를 더한 회로가 참값을 낸다.
    assert 96.0 < values["R0"] < 136.0
    one_arc = fit_circuit(spectrum, "L1-R0-p(R1,CPE1)-CPE2",
                          frequency_range=SULFIDE_BAND).values()
    assert one_arc["R0"] + one_arc["R1"] == pytest.approx(136.0, rel=0.01)


def test_an_arc_counted_only_through_the_sum_may_have_its_apex_above_the_window():
    """아크 하나를 더해 맞춘 차가운 펠릿 — 새 아크의 꼭지(300 kHz)는 맞춘 구간 위다.
    그래서 판정이 떴다.  구간이 정하는 것은 그 아크의 저주파 끝, 곧 R0 + R1 이고
    σ 는 그 합만 쓴다 (중립 이름이라 제 칸이 없다) — 꼭지 판정은 참고다.  σ 를 모르는
    검수와, 합이 아닌 길로 σ 에 드는 아크는 전처럼 확인이다 (ADR 0045 보완 10)."""
    spectrum = cold_pellet()
    fit = Fit("L1-R0-p(R1,CPE1)-CPE2",
              [P("L1", 2e-6), P("R0", 90.0), P("R1", 46.0),
               P("CPE1_Q", 1 / (46.0 * (2 * np.pi * 3e5) ** 0.9)), P("CPE1_n", 0.9),
               P("CPE2_Q", 6.3e-7), P("CPE2_n", 0.87)])
    band = (10.0, 1.71e5)
    summed = {"total_from": "series_and_arcs", "total_parts": ["R0", "R1"]}
    audit = audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC, thickness_cm=PELLET_CM,
                      area_cm2=AREA_CM2, band=band, conductivity=summed,
                      alternatives=PRESETS)
    assert audit.above_crossing is None                     # R0 가 교점 아래로 내려왔다
    assert "arc_above_window" not in codes(audit)
    (apex,) = [f for f in audit.findings if f.code == "arc_apex_above_window"]
    assert apex.severity == NOTE
    assert apex.message.endswith("— σ 에는 R0 + R1 의 합으로만 들고, 그 합은 아크의 "
                                 "저주파 끝(맞춘 구간 안)이 정합니다. 구간이 못 보는 것은 "
                                 "저항을 나누는 자리뿐입니다")
    for conductivity in (None, {"total_from": "series", "total_parts": ["R0"]}):
        plain = audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC,
                          thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=band,
                          conductivity=conductivity, alternatives=PRESETS)
        (apex,) = [f for f in plain.findings if f.code == "arc_apex_above_window"]
        assert apex.severity == CHECK and apex.message.endswith("정한 저항입니다")
    # 입계라 부른 아크는 입계 σ 를 제 저항 하나로 낸다 — 나누는 자리가 그 수다.
    assert _summed_parts(summed, {"R1": None}) == ("R0", "R1")
    assert _summed_parts(summed, {"R1": "grain_boundary"}) == ()
    assert _summed_parts({"total_from": "arcs", "total_parts": ["R1"]}, {}) == ()


def test_an_inductor_on_zero_says_what_the_sweep_shows():
    """꼭대기에 유도성 점이 없으면 그 파일에는 인덕턴스가 안 보인다.  있으면 인덕턴스는
    있다 — R0 가 교점과 같으면(5 % 안) 맞춘 구간이 그것을 쓰지 않았을 뿐이다."""
    stub = [P("L1", 1e-12, "undetermined", "at_lower_bound"), P("R0", 136.0),
            P("CPE1_Q", 6.3e-7), P("CPE1_n", 0.87)]
    fit = Fit("L1-R0-CPE1", stub)
    bare = audit_fit(fit, sulfide_pellet(r0=136.0, q=6.3e-7, n=0.87, inductance=0.0),
                     kind=SOLID, config=SYMMETRIC, band=SULFIDE_BAND)
    (note,) = [f for f in bare.findings if f.code == "no_inductance"]
    assert note.severity == NOTE
    assert note.message == "L1 이 0 에 붙었습니다 — 이 파일에는 배선 인덕턴스가 안 보입니다"

    wired = audit_fit(fit, sulfide_pellet(r0=136.0, q=6.3e-7, n=0.87, inductance=2e-6),
                      kind=SOLID, config=SYMMETRIC, band=SULFIDE_BAND)
    (note,) = [f for f in wired.findings if f.code == "no_inductance"]
    assert "꼭대기 13점이 유도성이라 배선 인덕턴스는 있지만" in note.message
    assert "arc_above_window" not in codes(wired)


B14_CIRCUIT = "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"
#: B14 #9 (-20 °C), 850 µm.  ? 가 붙었던 것은 미결정으로.
B14 = [P("R0", 84.3), P("R1", 2.92e3, "undetermined", "seed_spread"),
       P("CPE1_Q", 7.47e-6), P("CPE1_n", 0.851), P("R2", 2.6e5),
       P("CPE2_Q", 9.18e-7), P("CPE2_n", 1.0, "undetermined", "at_upper_bound"),
       P("CPE3_Q", 2.68e-5, "undetermined", "seed_spread"), P("CPE3_n", 0.663)]


def b14_spectrum():
    values = {p.name: p.value for p in B14}
    return spectrum_of_at(B14_CIRCUIT, values, SULFIDE_FREQUENCY)


def spectrum_of_at(circuit, values, frequency):
    model = parse_circuit(circuit)
    z = model.impedance([values[name] for name in model.parameter_names], frequency)
    return Spectrum(frequency, z.real, z.imag)


def test_arcs_that_are_all_electrode_sized_point_at_r0():
    """B11–B14·B7: 벌크·입계 자리의 두 아크가 모두 µF 대 — 전극 계면.  벌크·입계
    아크는 7 MHz 위에 있어 R0 에 들어 있다 (R0 84.3 Ω ≈ 적은 저항 78.1 Ω).
    이름이 이미 커패시턴스를 따르니 (ADR 0047) 고칠 것은 없고 읽기만 남는다 —
    참고이고, 다시 맞출 회로가 없다."""
    audit = audit_fit(Fit(B14_CIRCUIT, B14), b14_spectrum(), kind=SOLID,
                      config=SYMMETRIC, thickness_cm=850e-4, area_cm2=AREA_CM2,
                      band=(10.0, 1.71e5), alternatives=["L1-R0-CPE1"])
    (merged,) = [f for f in audit.findings if f.code == "arcs_are_electrode"]
    assert merged.severity == NOTE and merged.circuits == ()
    assert "R1 (전극 계면 저항)" in merged.message
    assert "R2 (전극 계면 저항)" in merged.message
    assert "R0 = 84.3 Ω" in merged.message
    assert "L1-R0-CPE1" not in merged.message
    for wrong_name in ("label_contradicts_capacitance", "capacitance_not_judged"):
        assert wrong_name not in codes(audit)


def test_a_boundary_arc_with_the_bulk_above_the_window_is_said_once():
    """벌크 반원은 10⁸ Hz 에 있어 안 보이고, 보이는 첫 아크는 입계 크기 —
    Irvine–Sinclair–West 그림 4b 의 읽기로 전해질은 R0 + R1 이다.  아크마다
    "벌크일 수 없다" 를 따로 적지 않고 원인 하나로."""
    values = {"R0": 8.0, "R1": 5.0, "CPE1_Q": 5e-9, "CPE1_n": 1.0,
              "CPE2_Q": 2e-6, "CPE2_n": 0.9}
    spectrum = spectrum_of_at("R0-p(R1,CPE1)-CPE2", values, SULFIDE_FREQUENCY)
    fit = Fit("R0-p(R1,CPE1)-CPE2", [P(n, v) for n, v in values.items()])
    audit = audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2,
                      band=(10.0, 7e6))
    (merged,) = [f for f in audit.findings if f.code == "bulk_above_window"]
    assert merged.severity == NOTE and merged.circuits == ()
    # C/A 6.4e-9 은 표면층에도 닿아 입계라고 못 박지 않는다 — 중립 이름 (ADR 0047).
    assert "R1 (고주파 아크) 는 입계 쪽(C·l/A 4.46e-10 F/cm)" in merged.message
    assert "R0 + R1 = 13 Ω" in merged.message
    assert "arcs_are_electrode" not in codes(audit)
    assert "label_contradicts_capacitance" not in codes(audit)


def test_a_real_bulk_arc_is_not_swept_into_the_electrode_verdict():
    """벌크가 벌크 크기인 셀 — 묶음 판정이 나오면 안 된다."""
    spectrum = spectrum_of(BLOCKING_CIRCUIT, BLOCKING)
    fit = Fit(BLOCKING_CIRCUIT, [P(n, v) for n, v in BLOCKING.items()])
    audit = audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=THICKNESS_CM, area_cm2=AREA_CM2, band=BAND)
    assert "arcs_are_electrode" not in codes(audit)


def test_suggestions_come_from_the_offered_circuits_that_fit_the_ending():
    """안 막는 셀 — 블로킹 꼬리를 뺀 회로와, 보기 중 실수축으로 돌아오는 끝을
    가진 것만 권한다.  `R0-TL1` 은 아니다: 입자에 리튬을 쌓는 확산(coth)이라
    저주파에서 `Z_계면 + R_ion/3` 의 수직 꼬리로 끝난다.  처음 판은 이것을
    돌아오는 끝으로 세어 실측 여섯 셀(#31 #32 #104 #142 #143 #38)에 권했다."""
    audit = audit_user(alternatives=["R0-TL1", "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
                                     "L1-R0-CPE1", "R0-p(R1,CPE1)-p(R2,CPE2)"])
    (finding,) = [f for f in audit.findings
                  if f.code == "blocking_element_on_open_cell"]
    assert finding.message.endswith("`R0-p(R1,CPE1)-p(R2,CPE2)` 로 다시 맞추세요")
    assert "TL1" not in finding.message and "L1-R0-CPE1" not in finding.message


def test_a_transmission_line_fit_is_not_told_about_bulk_sigma():
    """`R0-TL1` 로 맞춘 복합전극 대칭셀은 벌크·입계 σ 를 낸 적이 없다 — 그
    경고는 소음이다 (실측 Poly(L&F)_vgcf2_sym 두 셀)."""
    fit = Fit("R0-TL1", [P("R0", 1.8), P("TL1_Ri", 0.06), P("TL1_Re", 1e-9),
                         P("TL1_Rct", 0.016), P("TL1_Q", 0.23), P("TL1_n", 0.87),
                         P("TL1_Wr", 0.026), P("TL1_Wn", 0.17), P("TL1_Wt", 8e5)])
    audit = audit_fit(fit, USER_SPECTRUM, kind=SOLID, config=SYMMETRIC, band=BAND)
    assert "symmetric_cell_does_not_block" not in codes(audit)


def test_an_open_cell_is_not_offered_a_diffusion_ending():
    """반무한 W 도, 입자에 전하를 쌓는 전송선도 실수축으로 돌아오지 않는다
    (Lasia 1999) — 안 막는 셀에 권하지 않는다."""
    audit = audit_user(alternatives=["R0-p(R1,CPE1)-W2", "R0-TL1"])
    (finding,) = [f for f in audit.findings
                  if f.code == "blocking_element_on_open_cell"]
    assert "W2" not in finding.message and "TL1" not in finding.message


def test_a_large_amplitude_is_noted():
    found = audit_record(name="cell", kind=SOLID, config=SYMMETRIC,
                         thickness_um=700.0, area_cm2=0.785, amplitude_mv=100.0)
    (note,) = [f for f in found if f.code == "amplitude_large"]
    assert note.severity == NOTE and "100 mV" in note.message
    assert "VADHVA2021.small-amplitude-linearity" in note.refs
    quiet = audit_record(name="cell", kind=SOLID, config=SYMMETRIC,
                         thickness_um=700.0, area_cm2=0.785, amplitude_mv=10.0)
    assert "amplitude_large" not in [f.code for f in quiet]


def test_a_low_frequency_end_above_the_axis_is_asked_about():
    """저주파 끝의 +Im — 쉬지 않은 셀의 드리프트거나 흡착의 느린 루프.  고주파의
    배선 인덕턴스와는 다르다 (그것은 말하지 않는다)."""
    from wrdkit.eis.audit import audit_spectrum
    z = USER_SPECTRUM.z.copy()
    order = np.argsort(USER_SPECTRUM.frequency_hz)
    z[order[:4]] = z[order[:4]].real + 0.3j            # 가장 낮은 넷이 축 위
    drifted = Spectrum(USER_SPECTRUM.frequency_hz, z.real, z.imag)
    (finding,) = [f for f in audit_spectrum(drifted).findings
                  if f.code == "low_frequency_inductive"]
    assert finding.severity == CHECK and "가장 낮은 4개 점" in finding.message

    pellet = sulfide_pellet()
    assert np.any(pellet.z_im > 0)                     # 고주파는 배선으로 축 위다
    assert "low_frequency_inductive" not in codes(audit_spectrum(pellet))


def test_the_file_name_is_named_when_it_is_the_one_that_disagrees():
    found = audit_record(name="260831_Poly(L&F)_60um_sym_#01_C01", kind=SOLID,
                         config=SYMMETRIC, thickness_um=60.0, area_cm2=0.785,
                         file_name="260831_Poly(L&F)_60um_full_#01_C01.mpr")
    (note,) = [f for f in found if f.code == "file_name_differs"]
    assert note.severity == NOTE and "_full_" in note.message
    assert "config_differs_from_name" not in [f.code for f in found]


def test_an_area_that_reads_like_a_diameter_is_asked_about():
    """실측: 같은 조건의 두 셀 중 하나만 면적 10 cm² 였다 (짝은 0.785 cm²)."""
    found = audit_record(name="260913_Poly(L&F)_vgcf2_sym_70um_#02", kind=SOLID,
                         config=SYMMETRIC, thickness_um=70.0, area_cm2=10.0)
    (finding,) = [f for f in found if f.code == "area_looks_like_diameter"]
    assert "0.785 cm²" in finding.message


# -- 온도 스캔 (실측 B11·B13) ---------------------------------------------------------

def b11_like(**change):
    temperatures = [60, 50, 40, 30, 20, 10, 0, -10, -20]
    typed = [7.372, 7.285, 8.824, 15.44, 79.89, 25.19, 1.114e5, 56.93, 84.4]
    rows = []
    for index, (t, r) in enumerate(zip(temperatures, typed, strict=True), start=1):
        rows.append({"index": index, "temperature_c": t, "typed_ohm": r,
                     "crossing_ohm": r, "re_min_ohm": r * 0.6, "re_max_ohm": 5000.0,
                     "blocking": True, "phase_deg": -75.0,
                     "start_s": 7200.0 * index, "end_s": 7200.0 * index + 90})
    rows[6].update(blocking=False, phase_deg=-12.0, crossing_ohm=None)   # 0 °C
    for key, value in change.items():
        rows[int(key[1:]) - 1].update(value)
    return rows


def test_the_one_sweep_that_stops_blocking_is_named():
    found = audit_conductivity_scan(b11_like())
    (odd,) = [f for f in found if f.code == "sweep_unlike_its_neighbours"]
    assert "스윕 7 (0 °C)" in odd.message and "-12°" in odd.message
    assert "-75°" in odd.message


def test_a_sweep_whose_verdict_is_only_unclear_is_still_named():
    """ADR 0044 뒤로 B11 0 °C 스윕(-12°)의 판정이 "안 막음" 에서 "애매" 로
    바뀌었고, 판정끼리 비교하던 검사에서 빠졌다.  다른 것은 위상이다."""
    rows = b11_like()
    rows[6].update(blocking=None)
    (odd,) = [f for f in audit_conductivity_scan(rows)
              if f.code == "sweep_unlike_its_neighbours"]
    assert "스윕 7 (0 °C)" in odd.message and "-12°" in odd.message


def test_the_sweeps_off_the_arrhenius_line_are_named_with_the_expected_value():
    """실측 B11: 20 °C 79.9 Ω 과 0 °C 1.11e5 Ω.  둘을 빼면 R² 0.270 → 0.986, 직선이
    말하는 0 °C 값 37.7 Ω 은 따로 잰 0 °C 스펙트럼(#68)의 R0 36 Ω 과 맞는다."""
    (off,) = [f for f in audit_conductivity_scan(b11_like())
              if f.code == "sweep_off_the_line"]
    assert "스윕 5 (20 °C, 79.9 Ω)" in off.message
    assert "스윕 7 (0 °C, 1.11e+05 Ω)" in off.message
    assert "직선이 말하는 값은 19 Ω, 37.7 Ω" in off.message
    # 20 °C 는 스펙트럼도 80 Ω 에서 실수축을 건넜다 — 다시 읽을 것이 아니라 다시 잴 것.
    # 어느 값인지 수로 적는다: "교점도 그 값" 은 직선의 19 Ω 을 가리키는 것으로 읽혔다.
    assert ("적은 값 중 스윕 5 의 79.9 Ω 은 스펙트럼의 실수축 교점 그대로입니다"
            in off.message)
    assert "그 값" not in off.message
    assert "Ea = 0.236 eV" in off.message and "R² = 0.986" in off.message


def test_a_scattered_scan_or_a_first_sweep_alone_names_nobody_off_the_line():
    """B17 은 넷이 흩어져 누구를 짚을 수 없다 (R² 경고가 말한다).  B15 는 첫
    스윕만 벗어난다 — 그것은 first_sweep_suspect 가 말한다."""
    def rows(values):
        return [{"index": i, "temperature_c": t, "typed_ohm": r}
                for i, (t, r) in enumerate(zip([60, 50, 40, 30, 20, 10, 0, -10, -20],
                                               values, strict=True), start=1)]
    b17 = [11, 6.181, 8.214, 25.72, 45.87, 49.66, 28.14, 47.91, 78.65]
    b15 = [8.586, 8.311, 10.48, 14.02, 19.75, 30.38, 47.9, 81.01, 114.9]
    for values in (b17, b15):
        assert "sweep_off_the_line" not in [
            f.code for f in audit_conductivity_scan(rows(values))]


def test_a_scan_at_one_temperature_draws_no_line():
    """SOC 스캔처럼 온도가 하나뿐이면 Arrhenius 직선은 없다 — 조용히 넘어간다."""
    rows = [{"index": i, "temperature_c": 25.0, "typed_ohm": r}
            for i, r in enumerate([10.0, 11.0, 30.0, 10.5, 9.8, 10.2], start=1)]
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        found = audit_conductivity_scan(rows)
    assert "sweep_off_the_line" not in [f.code for f in found]


PRESETS = ["R0-TL1", "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3", "L1-R0-CPE1",
           "L1-R0-p(R1,CPE1)-CPE2", "L1-R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"]


def test_the_refit_offered_first_has_the_cable_and_the_arcs_worth_keeping():
    """실측: 꼬리를 흉내 낸 27 개 맞춤에 L 없는 두 아크 회로를 첫 줄로 권했다.
    L 이 든 것, 그리고 남길 만한 아크 수가 먼저다.  꼬리를 흉내 낸 아크는
    아크가 아니다."""
    fit = Fit("R0-p(R1,CPE1)", [P("R0", 7.89), P("R1", 1.37e5), P("CPE1_Q", 1.95e-6),
                                P("CPE1_n", 0.856)])
    audit = audit_fit(fit, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=PRESETS)
    (tail,) = [f for f in audit.findings if f.code == "tail_mimicked_by_arc"]
    assert ". `L1-R0-CPE1` 또는" in tail.message      # 꼬리는 아크가 아니다
    # 전송선의 끝도 막지만 펠릿에 권하지 않는다 — 복합전극이라는 주장은 셀
    # 구성(대칭셀)도 스펙트럼도 하지 않는다.
    assert "TL1" not in tail.message


def test_an_electrode_arc_counts_as_an_arc_worth_keeping():
    """전극 크기 아크 하나 + 꼬리를 흉내 낸 아크.  예전에는 전극 아크를 "다시
    맞춰도 벌크라 불린다" 며 세지 않아 아크 없는 회로부터 권했다.  이제 다시
    맞추면 "전극 계면" 이라 불리니 (ADR 0047) 그 아크를 남기는 회로가 먼저다."""
    circuit = "L1-R0-p(R1,CPE1)-p(R2,CPE2)"
    values = {"L1": 1.7e-6, "R0": 8.0, "R1": 200.0, "CPE1_Q": 2e-6, "CPE1_n": 0.9,
              "R2": 1e7, "CPE2_Q": 1e-5, "CPE2_n": 0.9}
    spectrum = spectrum_of_at(circuit, values, SULFIDE_FREQUENCY)
    fit = Fit(circuit, [P(name, value) for name, value in values.items()])
    audit = audit_fit(fit, spectrum, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=PRESETS)
    (tail,) = [f for f in audit.findings if f.code == "tail_mimicked_by_arc"]
    assert "R2" in tail.message
    assert tail.circuits[0] == "L1-R0-p(R1,CPE1)-CPE2"


def test_a_transmission_line_is_not_told_its_end_closes():
    """실측 B17 재측정 (#144 #150) 과 풀셀 #7: 전송선으로 맞춘 막는 스펙트럼에
    "회로의 저주파 끝이 실수축으로 닫힙니다 — 마지막 아크가 꼬리를 흉내
    냅니다" 가 붙었다.  아크는 없고, `TL` 의 계면 확산(`Wr·coth(x)/x`)은
    `Wo` 와 같은 반사 경계라 끝이 막힌다 — #144 는 Wr 가 1e9 Ω 이라 구간 안에서
    이미 -63° 꼬리였다."""
    values = {"R0": 13.9, "TL1_Ri": 39.2, "TL1_Re": 39.3, "TL1_Rct": 1.13e3,
              "TL1_Q": 3.96e-7, "TL1_n": 0.996, "TL1_Wr": 9.98e8, "TL1_Wn": 0.704,
              "TL1_Wt": 4.46e4}
    fit = Fit("R0-TL1", [P(n, v) for n, v in values.items()])
    audit = audit_fit(fit, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=PRESETS)
    assert audit.blocking["blocking"] is True and audit.end == "blocking"
    assert not {"open_end_on_blocking_cell", "tail_mimicked_by_arc",
                "blocking_element_on_open_cell"} & set(codes(audit))


def test_a_parameter_on_its_bound_shows_the_bound_not_itself():
    """실측 B17 재측정 #144: "TL1_n 이 상한(0.9963)에 붙었습니다" — 괄호가 경계로
    읽힌다.  맞춤은 경계의 1 % 안을 경계로 보므로 값과 경계가 다르다: n 의 상한은
    1, Wr 의 상한은 1e9 Ω 이다.  괄호에는 경계를, 값은 따로 적는다."""
    values = {"R0": 13.9, "TL1_Ri": 39.2, "TL1_Re": 39.3, "TL1_Rct": 1.13e3,
              "TL1_Q": 3.96e-7, "TL1_n": 0.9963, "TL1_Wr": 9.984e8, "TL1_Wn": 0.704,
              "TL1_Wt": 1e-6}
    rails = {"TL1_n": "at_upper_bound", "TL1_Wr": "at_upper_bound",
             "TL1_Wt": "at_lower_bound"}
    fit = Fit("R0-TL1", [P(n, v, reason=rails.get(n, "")) for n, v in values.items()])
    said = [f.message for f in audit_fit(fit, sulfide_pellet(), kind=SOLID,
                                         config=SYMMETRIC).findings
            if f.code == "at_bound"]
    assert "TL1_n 이 상한(1)에 붙었습니다 (값 0.9963) — 경계가" in " / ".join(said)
    assert "TL1_Wr 이 상한(1e+09)에 붙었습니다 (값 9.984e+08)" in " / ".join(said)
    # 값이 경계와 같게 찍히면 한 번만 적는다.
    assert "TL1_Wt 이 하한(1e-06)에 붙었습니다 — 경계가" in " / ".join(said)

    # 실측 풀셀 #7: CPE1 의 n = 0.3001, 하한 0.3.
    circuit = "R0-p(R1,CPE1)"
    values = {"R0": 4.25, "R1": 16.4, "CPE1_Q": 2.29e-4, "CPE1_n": 0.3001}
    fit = Fit(circuit, [P(n, v, reason="at_lower_bound" if n == "CPE1_n" else "")
                        for n, v in values.items()])
    (low,) = [f for f in audit_fit(fit, spectrum_of(circuit, values), kind=LIQUID,
                                   band=BAND).findings if f.code == "at_bound"]
    assert low.message.startswith("CPE1 의 n 이 하한(0.3)에 붙었습니다 (값 0.3001) — ")


def test_a_tail_cut_off_with_the_low_end_is_one_note_not_a_check_per_bound():
    """ADR 0045 보완 7 — 실측 풀셀 #1 을 KK 가 권한 1.29 Hz 부터 다시 맞추자 확산
    꼬리(TL1_Wr · Wn · Wt)가 경계로 갔고, 경계마다 "물리적으로 맞는 값인지
    보세요" 가 붙었다.  까닭은 하나다: 꼬리는 맞춘 구간 밖이다.  꼬리가 아닌
    TL1_Re 의 경계 붙음은 그대로 따로 본다."""
    from wrdkit.eis.audit import KKReference

    circuit = "L1-R0-p(R1,CPE1)-TL1"
    values = {"L1": 3.28e-07, "R0": 9.65, "R1": 30.9, "CPE1_Q": 4.85e-05,
              "CPE1_n": 0.85, "TL1_Ri": 10.7, "TL1_Re": 1e-09, "TL1_Rct": 48.1,
              "TL1_Q": 0.0154, "TL1_n": 0.34, "TL1_Wr": 1e-09, "TL1_Wn": 0.1,
              "TL1_Wt": 1e6}
    rails = {"TL1_Re": "at_lower_bound", "TL1_Wr": "at_lower_bound",
             "TL1_Wn": "at_lower_bound", "TL1_Wt": "at_upper_bound"}
    fit = Fit(circuit, [P(name, value, reason=rails.get(name, ""),
                          status="undetermined" if name in rails or name == "TL1_Ri"
                          else "determined")
                        for name, value in values.items()])
    spectrum = spectrum_of(circuit, values)
    cut = float(FREQUENCY[FREQUENCY >= 1.2].min())
    reference = KKReference(frequency_hz=FREQUENCY, residual=np.zeros(FREQUENCY.size),
                            low_limit_hz=cut, sigma=0.003)

    cut_off = audit_fit(fit, spectrum, kind=SOLID, config=FULL,
                        band=(cut, float(FREQUENCY.max())), reference=reference)
    (tail,) = [f for f in cut_off.findings if f.code == "tail_outside_window"]
    assert tail.severity == NOTE
    assert tail.message.startswith(
        "확산 꼬리가 경계에 붙었습니다 (TL1_Wr, TL1_Wn, TL1_Wt) — 꼬리의 크기(TL1_Wr)가 "
        "0 으로, 꼬리가 끝나는 곳(TL1_Wt)이 맞춘 구간 아래로 갔습니다")
    assert f"{cut:.3g} Hz 부터라" in tail.message
    bounds = " / ".join(f.message for f in cut_off.findings if f.code == "at_bound")
    assert "TL1_W" not in bounds and "TL1_Re" not in bounds
    (rail,) = [f for f in cut_off.findings if f.code == "transmission_line_one_rail"]
    assert "(TL1_Re)" in rail.message
    (unsettled,) = [f for f in cut_off.findings if f.code == "undetermined"]
    assert "TL1_W" not in unsettled.message and "TL1_Ri" in unsettled.message

    # 모든 점으로 맞춘 것이면 꼬리는 구간 안에 있었다 — 경계마다 따로 본다.
    whole = audit_fit(fit, spectrum, kind=SOLID, config=FULL, band=BAND,
                      reference=reference)
    assert "tail_outside_window" not in codes(whole)
    bounds = " / ".join(f.message for f in whole.findings if f.code == "at_bound")
    assert all(name in bounds for name in ("TL1_Wr", "TL1_Wn", "TL1_Wt"))


def test_the_tail_note_says_only_what_the_fit_did_to_the_tail():
    """실측 검수 (2026-09-25 06:24) — 보완 7 의 한 줄이 경계에 붙은 꼬리가 없는 #9
    (0.322 Hz 부터, TL1_Wr · Wt 는 미결정일 뿐) 에도 "꼬리가 맞춘 구간 밖입니다.
    경계에 붙은 것도 그 때문입니다" 라고 했다.  한 줄은 맞춤이 꼬리를 밀어낸 것
    — 크기 0 이나 시정수 상한 — 만 말하고 경계에 붙은 것만 묶는다."""
    from wrdkit.eis.audit import KKReference

    circuit = "L1-R0-p(R1,CPE1)-TL1"

    def audit(values, rails, undetermined, above_hz):
        fit = Fit(circuit, [P(name, value, reason=rails.get(name, ""),
                              status="undetermined" if name in undetermined
                              else "determined")
                            for name, value in values.items()])
        sweep = FREQUENCY
        cut = float(sweep[sweep >= above_hz].min())
        reference = KKReference(frequency_hz=sweep, residual=np.zeros(sweep.size),
                                low_limit_hz=cut, sigma=0.003)
        return audit_fit(fit, spectrum_of(circuit, values), kind=SOLID, config=FULL,
                         band=(cut, float(sweep.max())), reference=reference)

    def said(result, code):
        return " / ".join(f.message for f in result.findings if f.code == code)

    # #9: 꼬리는 미결정일 뿐 — 까닭을 모르니 미결정 목록에 둔다.
    lone = audit({"L1": 5.22e-07, "R0": 4.44, "R1": 22.4, "CPE1_Q": 2.64e-4,
                  "CPE1_n": 0.3, "TL1_Ri": 87.1, "TL1_Re": 0.211, "TL1_Rct": 156,
                  "TL1_Q": 3.24e-05, "TL1_n": 0.754, "TL1_Wr": 66.4, "TL1_Wn": 0.332,
                  "TL1_Wt": 40.0},
                 {"CPE1_n": "at_lower_bound"},
                 {"R0", "R1", "CPE1_Q", "CPE1_n", "TL1_Ri", "TL1_Re", "TL1_Wr", "TL1_Wt"},
                 0.3)
    assert "tail_outside_window" not in codes(lone)
    assert "TL1_Wr" in said(lone, "undetermined") and "TL1_Wt" in said(lone, "undetermined")

    # #33: 시정수가 상한 — 경계에 붙은 Wn · Wt 만 묶고, 미결정일 뿐인 Wr 는 목록에.
    pushed = audit({"L1": 5.52e-07, "R0": 2.69e-06, "R1": 0.858, "CPE1_Q": 2.16e-3,
                    "CPE1_n": 0.786, "TL1_Ri": 25.8, "TL1_Re": 1e-09, "TL1_Rct": 0.306,
                    "TL1_Q": 6.79e-4, "TL1_n": 0.492, "TL1_Wr": 13.3, "TL1_Wn": 0.1,
                    "TL1_Wt": 9.98e5},
                   {"TL1_Wn": "at_lower_bound", "TL1_Wt": "at_upper_bound"},
                   {"R0", "TL1_Ri", "TL1_Re", "TL1_Rct", "TL1_Q", "TL1_Wr", "TL1_Wn",
                    "TL1_Wt"},
                   1.6)
    assert said(pushed, "tail_outside_window").startswith(
        "확산 꼬리가 경계에 붙었습니다 (TL1_Wn, TL1_Wt) — 꼬리가 끝나는 곳(TL1_Wt)이 "
        "맞춘 구간 아래로 갔습니다")
    assert "TL1_W" not in said(pushed, "at_bound")
    assert "TL1_Wr" in said(pushed, "undetermined")
    assert "TL1_Wn" not in said(pushed, "undetermined")

    # 하한을 올렸어도 꼬리 모양(Wn)만 경계면 맞춤이 꼬리를 밀어낸 것이 아니다 —
    # 전처럼 경계마다 본다 (#16 의 Wn 0.8 모양).
    shaped = audit({"L1": 3.63e-07, "R0": 18.1, "R1": 284, "CPE1_Q": 7.11e-05,
                    "CPE1_n": 0.546, "TL1_Ri": 14.5, "TL1_Re": 14.5, "TL1_Rct": 1.17e3,
                    "TL1_Q": 1.01e-4, "TL1_n": 0.576, "TL1_Wr": 34.8, "TL1_Wn": 0.8,
                    "TL1_Wt": 8.28},
                   {"TL1_Wn": "at_upper_bound"}, {"TL1_Ri", "TL1_Re", "TL1_Wn"}, 0.05)
    assert "tail_outside_window" not in codes(shaped)
    assert "TL1_Wn" in said(shaped, "at_bound")


def test_one_rail_of_a_transmission_line_at_zero_is_de_levie_not_a_check():
    """실측 풀셀 #1 · #10 — TL1_Re 가 0 에 붙자 "경계가 물리적으로 맞는 값인지
    보세요" 가 붙었다.  레일 하나가 0 인 선은 de Levie 의 기공 모델이고, 두 레일은
    맞바꿔도 같은 곡선이라 (`transmission_line`) 어느 쪽이 0 인지는 스펙트럼이
    말하지 않는다 — 물을 것이 없다.  둘 다 0 이면 선이 무너진 것이라 따로 본다."""
    circuit = "L1-R0-p(R1,CPE1)-TL1"
    values = {"L1": 4.46e-07, "R0": 11.8, "R1": 147, "CPE1_Q": 3.93e-05,
              "CPE1_n": 0.769, "TL1_Ri": 23.1, "TL1_Re": 1e-09, "TL1_Rct": 34,
              "TL1_Q": 7.62e-05, "TL1_n": 0.529, "TL1_Wr": 10.3, "TL1_Wn": 0.147,
              "TL1_Wt": 0.132}

    def audit(values, rails, circuit=circuit):
        fit = Fit(circuit, [P(name, value, reason=rails.get(name, ""))
                            for name, value in values.items()])
        return audit_fit(fit, spectrum_of(circuit, values), kind=SOLID, config=FULL,
                         band=BAND)

    def bounds(result):
        return " / ".join(f.message for f in result.findings if f.code == "at_bound")

    one = audit(values, {"TL1_Re": "at_lower_bound"})
    (rail,) = [f for f in one.findings if f.code == "transmission_line_one_rail"]
    assert rail.severity == NOTE
    assert rail.message.startswith("TL1 의 레일 하나(TL1_Re)가 0 에 붙었습니다 — 레일이 "
                                   "하나인 de Levie 전송선")
    assert "LASIA1999.de-levie-porous-electrode" in rail.refs
    assert "TL1_Re" not in bounds(one)

    # 맞바꾼 짝도 같은 말이다.
    swapped = dict(values, TL1_Ri=1e-09, TL1_Re=23.1)
    (rail,) = [f for f in audit(swapped, {"TL1_Ri": "at_lower_bound"}).findings
               if f.code == "transmission_line_one_rail"]
    assert "(TL1_Ri)" in rail.message

    # 둘 다 0 이면 선이 무너졌다 — 경계마다 본다.
    both = audit(dict(values, TL1_Ri=1e-09),
                 {"TL1_Ri": "at_lower_bound", "TL1_Re": "at_lower_bound"})
    assert "transmission_line_one_rail" not in codes(both)
    assert "TL1_Ri" in bounds(both) and "TL1_Re" in bounds(both)

    # 확산 꼬리가 없는 전송선(TLR)도 같은 두 레일이다.
    plain = {"L1": 5.0e-07, "R0": 5.2, "R1": 161, "CPE1_Q": 6.41e-05, "CPE1_n": 0.762,
             "TLR1_Ri": 60.0, "TLR1_Re": 1e-09, "TLR1_Rct": 200.0, "TLR1_Q": 1e-3,
             "TLR1_n": 0.7}
    (rail,) = [f for f in audit(plain, {"TLR1_Re": "at_lower_bound"},
                                circuit="L1-R0-p(R1,CPE1)-TLR1").findings
               if f.code == "transmission_line_one_rail"]
    assert rail.message.startswith("TLR1 의 레일 하나(TLR1_Re)가")


def test_an_end_that_still_rises_gently_is_not_said_to_come_down():
    """실측 하프셀 #38: 끝이 26° 로 완만하게 오르는데 "실수축으로 내려오는데" 라고
    했다 — 헤더는 "꼬리 26°" 다.  30° 아래는 위상으로 판정하니 (ADR 0044) "안 막음"
    은 그대로고, 문장만 끝이 어떻게 생겼는지 말한다."""
    circuit = "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"
    values = {"R0": 13.3, "R1": 43.5, "CPE1_Q": 4.91e-4, "CPE1_n": 0.391,
              "R2": 9.99e8, "CPE2_Q": 0.104, "CPE2_n": 0.3, "CPE3_Q": 1e3,
              "CPE3_n": 0.3}
    rails = {"R2": "at_upper_bound", "CPE2_n": "at_lower_bound",
             "CPE3_Q": "at_upper_bound", "CPE3_n": "at_lower_bound"}
    fit = Fit(circuit, [P(n, v, reason=rails.get(n, "")) for n, v in values.items()])
    audit = audit_fit(fit, spectrum_of(circuit, values), kind=SOLID, band=BAND)
    assert audit.blocking["blocking"] is False
    (finding,) = [f for f in audit.findings
                  if f.code == "blocking_element_on_open_cell"]
    assert finding.message.startswith(
        "스펙트럼은 저주파에서 끝이 완만하게만 오르는데 (위상 -7°, 꼬리 26°) 회로 끝에 "
        "막는 소자 CPE3 가 있습니다")


def test_noise_just_above_the_axis_at_the_end_is_not_drift():
    """실수축으로 내려온 셀의 마지막 점들은 잡음만으로도 축 위에 선다 — |Z| 의
    1 % 는 넘어야 센다."""
    from wrdkit.eis.audit import audit_spectrum
    z = USER_SPECTRUM.z.copy()
    order = np.argsort(USER_SPECTRUM.frequency_hz)
    z[order[:3]] = z[order[:3]].real + 1j * 0.002 * np.abs(z[order[:3]])
    grazing = Spectrum(USER_SPECTRUM.frequency_hz, z.real, z.imag)
    assert "low_frequency_inductive" not in codes(audit_spectrum(grazing))


def test_a_sweep_taken_before_the_chamber_settled_is_named():
    rows = b11_like(s1={"start_s": 600.0, "end_s": 690.0})   # 10 분 만에 첫 스윕
    found = audit_conductivity_scan(rows)
    (short,) = [f for f in found if f.code == "short_rest_before_sweep"]
    assert "스윕 1 (10 min)" in short.message and "2.0 h" in short.message


def test_only_the_first_step_going_the_wrong_way_is_explained():
    """실측 9개 스캔 중 5개가 60 °C 저항이 50 °C 보다 컸다.  나머지 걸음이
    멀쩡하면 첫 스윕 탓이고, 빼고 맞춘 Ea 를 같이 낸다."""
    rows = [{"index": i, "temperature_c": t, "typed_ohm": r}
            for i, (t, r) in enumerate(zip([60, 50, 40, 30, 20],
                                           [5.136, 4.782, 5.899, 7.87, 11.13],
                                           strict=True), start=1)]
    found = audit_conductivity_scan(rows, without_first=(0.301, 0.998))
    (note,) = [f for f in found if f.code == "first_sweep_suspect"]
    assert "0.301 eV" in note.message and "0.998" in note.message
    # 다른 걸음도 거꾸로면 첫 스윕 탓이라고 하지 않는다.
    rows[3]["typed_ohm"] = 4.0
    assert "first_sweep_suspect" not in [
        f.code for f in audit_conductivity_scan(rows, without_first=(0.3, 0.9))]


def backwards_of(rows):
    """What the API hands over: `activation_energy` 의 거꾸로 간 걸음과 그 경고."""
    steps = backwards_steps([one["temperature_c"] for one in rows],
                            [1.0 / one["typed_ohm"] for one in rows])
    return {"backwards": steps, "warnings": [backwards_warning(steps)] if steps else []}


def test_a_wrong_way_step_the_first_sweep_explains_is_not_a_second_check():
    """실측 B13·B15·B18: "60→50 °C 가 거꾸로 — 저항을 다시 읽어 주세요" (확인) 가
    "첫 스윕만 거꾸로 갑니다" (참고) 옆에 같은 사실로 붙었다."""
    rows = [{"index": i, "temperature_c": t, "typed_ohm": r, "crossing_ohm": r}
            for i, (t, r) in enumerate(zip([60, 50, 40, 30, 20],
                                           [5.136, 4.782, 5.899, 7.87, 11.13],
                                           strict=True), start=1)]
    found = [f.code for f in audit_conductivity_scan(rows, without_first=(0.293, 0.994),
                                                     **backwards_of(rows))]
    assert found == ["first_sweep_suspect"]


def test_wrong_way_steps_are_said_once_and_measured_ones_are_to_be_measured_again():
    """실측 B11: 거꾸로 간 세 걸음 중 20→10·0→-10 °C 는 직선에서 먼 스윕 5·7 의
    것이다 — 남는 것은 60→50 °C 하나.  적은 값이 모두 실수축 교점이라 "다시 읽어
    주세요" 는 틀린 처방이다: 다시 잴 일이다.  (첫 스윕을 뺀 Ea 가 없을 때 —
    두께·면적이 없는 스캔.  있으면 그 걸음은 첫 스윕 이야기다: 아래 시험.)"""
    rows = b11_like()
    found = audit_conductivity_scan(rows, **backwards_of(rows))
    assert "activation_warning" not in [f.code for f in found]
    (wrong,) = [f for f in found if f.code == "conductivity_goes_backwards"]
    assert "구간이 1개 있습니다 (60→50 °C)" in wrong.message
    assert "실수축 교점과 같습니다" in wrong.message and "다시 재세요" in wrong.message

    # B17: 아무도 못 짚는 스캔은 두 걸음 그대로 — 교점과 같으니 역시 다시 잴 일.
    b17 = [{"index": i, "temperature_c": t, "typed_ohm": r, "crossing_ohm": r}
           for i, (t, r) in enumerate(zip([60, 50, 40, 30, 20, 10, 0, -10, -20],
                                          [11, 6.181, 8.214, 25.72, 45.87, 49.66,
                                           28.14, 47.91, 78.65], strict=True), start=1)]
    (wrong,) = [f for f in audit_conductivity_scan(b17, **backwards_of(b17))
                if f.code == "conductivity_goes_backwards"]
    assert "구간이 2개 있습니다 (60→50 °C, 10→0 °C)" in wrong.message
    assert "다시 재세요" in wrong.message

    # 교점을 모르면(또는 다르면) 읽기부터 본다.
    for one in b17:
        one.pop("crossing_ohm")
    (wrong,) = [f for f in audit_conductivity_scan(b17, **backwards_of(b17))
                if f.code == "conductivity_goes_backwards"]
    assert wrong.message.endswith("그 온도의 저항을 다시 읽어 주세요")


def test_the_first_sweep_is_explained_even_when_other_sweeps_are_off_the_line():
    """실측 B11 (열두 번째 검수): 60→50 °C 는 1.2 % 거꾸로 — B13·B15·B18 과 같은
    첫 가열 걸음인데, 직선에서 먼 스윕 5·7 의 걸음 때문에 첫 스윕 이야기를 못
    하고 "그 온도를 다시 재세요" (확인) 가 붙었다.  짚은 스윕을 빼고 보면 첫 걸음
    하나다.  Ea 는 부르는 쪽 것(짚은 스윕이 든 0.417 eV, R² 0.218)이 아니라 셋을
    다 뺀 것이다."""
    rows = b11_like()
    found = audit_conductivity_scan(rows, without_first=(0.417, 0.218),
                                    **backwards_of(rows))
    assert "conductivity_goes_backwards" not in [f.code for f in found]
    (note,) = [f for f in found if f.code == "first_sweep_suspect"]
    assert note.message.startswith("따로 짚은 스윕 5, 7 말고는 첫 스윕만 온도와 거꾸로")
    assert "첫 스윕까지 3개를 빼면 Ea = 0.248 eV (R² = 0.993)" in note.message
    assert "0.417" not in note.message

    # 짚은 스윕이 없으면 전과 같다 — 부르는 쪽의 수를 그대로 쓴다 (B13·B15·B18).
    plain = [{"index": i, "temperature_c": t, "typed_ohm": r}
             for i, (t, r) in enumerate(zip([60, 50, 40, 30, 20],
                                            [5.136, 4.782, 5.899, 7.87, 11.13],
                                            strict=True), start=1)]
    (note,) = [f for f in audit_conductivity_scan(plain, without_first=(0.301, 0.998))
               if f.code == "first_sweep_suspect"]
    assert note.message.startswith("첫 스윕만")
    assert note.message.endswith("첫 스윕을 빼면 Ea = 0.301 eV (R² = 0.998)")

    # 첫 스윕 자신이 짚혔으면 첫 스윕 이야기를 하지 않는다 — 그 판정이 말한다.
    rows = b11_like(s1={"phase_deg": -12.0})
    assert "first_sweep_suspect" not in [
        f.code for f in audit_conductivity_scan(rows, without_first=(0.417, 0.218))]


# -- ADR 0045: 판정이 "이 회로로 맞추면 풀린다" 를 싣는다 --------------------------

def quoted(message):
    return re.findall(r"`([^`]+)`", message)


def test_the_tail_and_open_cell_findings_carry_the_circuits_they_quote():
    """`bml refit` 은 문장을 긁지 않고 `circuits` 를 읽는다 — 둘이 같아야 한다."""
    fit = Fit("R0-p(R1,CPE1)", [P("R0", 7.89), P("R1", 1.37e5), P("CPE1_Q", 1.95e-6),
                                P("CPE1_n", 0.856)])
    audit = audit_fit(fit, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=PRESETS)
    (tail,) = [f for f in audit.findings if f.code == "tail_mimicked_by_arc"]
    assert tail.circuits and tail.circuits[0] == "L1-R0-CPE1"
    assert list(tail.circuits) == quoted(tail.message)

    audit = audit_user(alternatives=["R0-TL1", "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
                                     "L1-R0-CPE1", "R0-p(R1,CPE1)-p(R2,CPE2)"])
    (open_,) = [f for f in audit.findings if f.code == "blocking_element_on_open_cell"]
    assert open_.circuits == ("R0-p(R1,CPE1)-p(R2,CPE2)",)


def test_electrode_arcs_are_not_sent_to_be_refitted_away():
    """실측 `bml refit` (2026-09-25): 전극 아크가 있는 펠릿 여덟에 아크 없는
    `L1-R0-CPE1` 을 맞췄고 모두 3.1–5.9 % 어긋나 그대로였다 — 아크는 있다.
    이름이 커패시턴스를 따르니 (ADR 0047) 권할 회로가 없다."""
    audit = audit_fit(Fit(B14_CIRCUIT, B14), b14_spectrum(), kind=SOLID,
                      config=SYMMETRIC, thickness_cm=850e-4, area_cm2=AREA_CM2,
                      band=(10.0, 1.71e5), alternatives=PRESETS)
    assert not [f for f in audit.findings if f.circuits and f.code in (
        "arcs_are_electrode", "bulk_above_window", "label_contradicts_capacitance")]
    assert worst(audit.findings) != PROBLEM


#: 실측 B11 #8 (-10 °C, 790 µm): R1 은 전극 크기, R2 는 미결정 — 묶음 판정을 비껴가
#: "벌크일 수 없습니다" 만 남았다.
B11_8 = [P("R0", 52.9), P("R1", 7.35e3), P("CPE1_Q", 4.69e-6), P("CPE1_n", 0.759),
         P("R2", 4.49e5, "undetermined", "seed_spread"),
         P("CPE2_Q", 5.02e-7, "undetermined", "seed_spread"),
         P("CPE2_n", 0.997, "undetermined", "at_upper_bound"),
         P("CPE3_Q", 2.54e-3, "undetermined", "seed_spread"),
         P("CPE3_n", 0.3, "undetermined", "at_lower_bound")]


def test_an_electrode_sized_arc_is_named_for_it_not_sent_to_a_refit():
    """실측 B11 #8 (#66): R1 7.35e3 Ω 의 C 1.61e-6 F 는 전극 계면 — 예전에는
    "벌크일 수 없습니다" 문제에 `L1-R0-CPE1` 을 실었고, `bml refit` 이 그것으로
    맞추자 3.7 % 어긋났다.  이제 그 아크의 이름이 "전극 계면 저항" 이다
    (ADR 0047).  R2 는 미결정이라 열 배 흔들면 입계에도 닿는다 — 이름은 그대로
    두고 참고로 적는다."""
    values = {p.name: p.value for p in B11_8}
    spectrum = spectrum_of_at(B14_CIRCUIT, values, SULFIDE_FREQUENCY)
    audit = audit_fit(Fit(B14_CIRCUIT, B11_8), spectrum, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=790e-4, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=PRESETS)
    assert audit.blocking["blocking"] is True
    rows = {row["resistor"]: row for row in audit.arcs}
    assert rows["R1"]["label"] == "전극 계면 저항"
    assert rows["R2"]["label"] == "입계 저항"
    assert "label_contradicts_capacitance" not in codes(audit)
    (shaky,) = [f for f in audit.findings if f.code == "capacitance_not_judged"]
    assert shaky.severity == NOTE and "R2" in shaky.message
    assert not [f for f in audit.findings if f.circuits]

    # 셀 구성을 모르면 이름이 없고, 처방도 없다.
    blind = audit_fit(Fit(B14_CIRCUIT, B11_8), spectrum, kind=SOLID, config="",
                      thickness_cm=790e-4, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=PRESETS)
    assert not [f for f in blind.findings if f.circuits]
