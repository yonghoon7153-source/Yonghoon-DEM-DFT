"""The audit of one stored fit (ADR 0040).

The anchor is the cell that started it: `2600922_No1_55_sym_60um_#1_C01`,
fitted with a blocking circuit it did not need.  Its twin -- a cell that
really blocks, fitted with the right circuit -- must come out clean, or the
audit is just noise.
"""

import math
from dataclasses import dataclass

import numpy as np
import pytest
import synthetic_eis as S

from wrdkit.eis.audit import (
    CHECK,
    NOTE,
    PROBLEM,
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


def test_both_names_are_ruled_out_by_the_capacitances():
    audit = audit_user()
    wrong = [f for f in audit.findings if f.code == "label_contradicts_capacitance"]
    assert len(wrong) == 2
    bulk, boundary = wrong
    assert bulk.severity == PROBLEM
    assert "R1" in bulk.message and "벌크" in bulk.message
    assert "입계 또는 전극 계면의 크기" in bulk.message   # 무엇일 수는 있는지
    assert "R2" in boundary.message and "입계일 수 없습니다" in boundary.message
    assert "전기화학 반응" in boundary.message
    # 벌크라는 이름에는 누구나 확인할 수 있는 수가 하나 더 — 겉보기 εr (ISW 1990).
    assert "겉보기 εr ≈ 4e+04" in bulk.message
    assert "εr" not in boundary.message
    rows = {row["resistor"]: row for row in audit.arcs}
    assert rows["R1"]["claims"] == "bulk"
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
    (finding,) = [f for f in audit.findings if f.code == "element_vanishing"]
    assert "R0" in finding.message and "없어도" in finding.message
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


def test_an_undetermined_arc_far_outside_is_still_judged():
    """미결정 값은 몇 배 흔들리지, 벌크와 이중층 사이의 네 자릿수를 건너지
    않는다.  실측 B11 스캔의 "벌크" 들은 벌크 상한의 수만 배였는데 전부
    미결정이라 판정에서 빠졌었다."""
    parameters = [P(name, value) for name, value in USER.items()]
    parameters[1] = P("R1", USER["R1"], "undetermined", "seed_spread")
    fit = Fit("R0-p(R1,CPE1)-p(R2,CPE2)", parameters)
    audit = audit_fit(fit, USER_SPECTRUM, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=THICKNESS_CM, area_cm2=AREA_CM2, band=BAND)
    judged = [f for f in audit.findings if f.code == "label_contradicts_capacitance"]
    assert [("R1" in f.message, "미결정" in f.message) for f in judged] == [
        (True, True), (False, False)]
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
    assert "R1 (벌크 저항)" in tail.message
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

    with_l = Fit("L1-R0-CPE1", [P("L1", 1.73e-6), P("R0", 8.3), P("CPE1_Q", 1.9e-6),
                                P("CPE1_n", 0.86)])
    clean = audit_fit(with_l, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND)
    assert clean.findings == []


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
    """B11–B14·B7: 벌크·입계라 부른 두 아크가 모두 µF 대 — 전극 계면.  벌크·입계
    아크는 7 MHz 위에 있어 R0 에 들어 있다 (R0 84.3 Ω ≈ 적은 저항 78.1 Ω)."""
    audit = audit_fit(Fit(B14_CIRCUIT, B14), b14_spectrum(), kind=SOLID,
                      config=SYMMETRIC, thickness_cm=850e-4, area_cm2=AREA_CM2,
                      band=(10.0, 1.71e5), alternatives=["L1-R0-CPE1"])
    (merged,) = [f for f in audit.findings if f.code == "arcs_are_electrode"]
    assert merged.severity == PROBLEM
    assert "R1 (벌크 저항)" in merged.message and "R2 (입계 저항)" in merged.message
    assert "R0 = 84.3 Ω" in merged.message
    assert "`L1-R0-CPE1`" in merged.message
    # 묶인 아크의 증상은 다시 적지 않는다.
    for repeated in ("label_contradicts_capacitance", "capacitance_not_judged",
                     "arc_apex_below_window"):
        assert repeated not in codes(audit)


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
    assert merged.severity == PROBLEM
    assert "R1 (벌크 저항) 는 입계 쪽(C·l/A 4.46e-10 F/cm)" in merged.message
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
    """안 막는 복합전극 대칭셀 — 블로킹 꼬리를 뺀 회로와, 보기 중 막지 않는
    끝을 가진 것 (전송선 포함)을 권한다."""
    audit = audit_user(alternatives=["R0-TL1", "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
                                     "L1-R0-CPE1"])
    (finding,) = [f for f in audit.findings
                  if f.code == "blocking_element_on_open_cell"]
    assert "`R0-p(R1,CPE1)-p(R2,CPE2)` 또는 `R0-TL1`" in finding.message
    assert "L1-R0-CPE1" not in finding.message


def test_a_transmission_line_fit_is_not_told_about_bulk_sigma():
    """`R0-TL1` 로 맞춘 복합전극 대칭셀은 벌크·입계 σ 를 낸 적이 없다 — 그
    경고는 소음이다 (실측 Poly(L&F)_vgcf2_sym 두 셀)."""
    fit = Fit("R0-TL1", [P("R0", 1.8), P("TL1_Ri", 0.06), P("TL1_Re", 1e-9),
                         P("TL1_Rct", 0.016), P("TL1_Q", 0.23), P("TL1_n", 0.87),
                         P("TL1_Wr", 0.026), P("TL1_Wn", 0.17), P("TL1_Wt", 8e5)])
    audit = audit_fit(fit, USER_SPECTRUM, kind=SOLID, config=SYMMETRIC, band=BAND)
    assert "symmetric_cell_does_not_block" not in codes(audit)


def test_an_open_cell_is_not_offered_a_diffusion_ending():
    """반무한 W 도 실수축으로 돌아오지 않는다 (Lasia 1999) — 안 막는 셀에
    권하지 않는다."""
    audit = audit_user(alternatives=["R0-p(R1,CPE1)-W2", "R0-TL1"])
    (finding,) = [f for f in audit.findings
                  if f.code == "blocking_element_on_open_cell"]
    assert "`R0-TL1`" in finding.message
    assert "W2" not in finding.message


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
    assert "스윕 5 는 스펙트럼의 실수축 교점도 그 값입니다" in off.message
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
    L 이 든 것, 그리고 남길 만한 아크 수가 먼저다.

    전극 쪽 크기의 아크는 남길 만하지 않다 — 다시 맞춰도 자리 순서로 같은
    이름(벌크·입계)이 붙어 같은 문제가 뜬다.  이름이 맞는 것은 아크가 없는
    회로이고, 아크가 정말 보이는 셀을 위한 아크 하나짜리는 따로 적는다."""
    audit = audit_fit(Fit(B14_CIRCUIT, B14), b14_spectrum(), kind=SOLID,
                      config=SYMMETRIC, thickness_cm=850e-4, area_cm2=AREA_CM2,
                      band=(10.0, 1.71e5), alternatives=PRESETS)
    (merged,) = [f for f in audit.findings if f.code == "arcs_are_electrode"]
    assert "; `L1-R0-CPE1` 로 다시 맞추면 이름이 맞습니다" in merged.message
    assert "안 그려지면 `L1-R0-p(R1,CPE1)-CPE2` — 그 아크는 전극 계면" in merged.message
    assert "`L1-R0-p(R1,CPE1)-p(R2,CPE2)-CPE3`" not in merged.message

    fit = Fit("R0-p(R1,CPE1)", [P("R0", 7.89), P("R1", 1.37e5), P("CPE1_Q", 1.95e-6),
                                P("CPE1_n", 0.856)])
    audit = audit_fit(fit, sulfide_pellet(), kind=SOLID, config=SYMMETRIC,
                      thickness_cm=PELLET_CM, area_cm2=AREA_CM2, band=SULFIDE_BAND,
                      alternatives=PRESETS)
    (tail,) = [f for f in audit.findings if f.code == "tail_mimicked_by_arc"]
    assert ". `L1-R0-CPE1` 또는" in tail.message      # 꼬리는 아크가 아니다


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
