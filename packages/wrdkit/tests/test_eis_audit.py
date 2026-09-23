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


def test_the_vanishing_cpe_is_named_for_what_it_is_doing():
    audit = audit_user()
    vanishing = [f for f in audit.findings if f.code == "element_vanishing"]
    assert [f.severity for f in vanishing] == [CHECK]
    assert "CPE3" in vanishing[0].message and "없이" in vanishing[0].message
    # n = 1 은 이상적인 축전기일 뿐이다 — 틀렸다고 하지 않는다.
    assert "cpe_ideal" in codes(audit, NOTE)


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
    rows = {row["resistor"]: row for row in audit.arcs}
    assert rows["R1"]["claims"] == "bulk"
    assert rows["R1"]["capacitance_f"] == pytest.approx(4.66e-7, rel=0.01)
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


def test_an_undetermined_arc_is_reported_but_not_judged():
    parameters = [P(name, value) for name, value in USER.items()]
    parameters[1] = P("R1", USER["R1"], "undetermined", "seed_spread")
    fit = Fit("R0-p(R1,CPE1)-p(R2,CPE2)", parameters)
    audit = audit_fit(fit, USER_SPECTRUM, kind=SOLID, config=SYMMETRIC,
                      thickness_cm=THICKNESS_CM, area_cm2=AREA_CM2, band=BAND)
    assert "capacitance_not_judged" in codes(audit, NOTE)
    judged = [f for f in audit.findings if f.code == "label_contradicts_capacitance"]
    assert ["R2" in f.message for f in judged] == [True]
    assert "undetermined" in codes(audit, NOTE)


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


def test_a_clean_record_says_nothing():
    assert audit_record(name="2600922_No1_55_sym_60um_#1", kind=SOLID,
                        config=SYMMETRIC, thickness_um=60.0, area_cm2=0.785,
                        n_points=59) == []


# -- 온도 스캔 ---------------------------------------------------------------------

def test_a_scan_with_a_decimal_slip_and_a_blank_temperature():
    sweeps = [
        {"index": 1, "temperature_c": 60.0, "typed_ohm": 7.37, "crossing_ohm": 7.31},
        {"index": 2, "temperature_c": None, "typed_ohm": 79.89, "crossing_ohm": 7.99},
        {"index": 3, "temperature_c": 40.0, "typed_ohm": None, "crossing_ohm": 9.1},
    ]
    found = audit_scan(sweeps)
    got = [f.code for f in found]
    assert got[:2] == ["temperatures_partly_missing", "typed_far_from_crossing"]
    slip = found[1]
    assert "스윕 2" in slip.message and "10배" in slip.message
    assert "resistance_partly_missing" in got


def audit_scan(sweeps, **kwargs):
    return audit_conductivity_scan(sweeps, **kwargs)


def test_the_activation_energy_warnings_come_along():
    sweeps = [{"index": 1, "temperature_c": 60.0, "typed_ohm": 7.0,
               "crossing_ohm": 7.0}]
    found = audit_scan(sweeps, warnings=["직선이 점들을 설명하지 못합니다"],
                       reason="점이 모자랍니다")
    assert [f.code for f in found] == ["activation_warning", "activation_missing"]


def test_a_scan_with_nothing_written_yet_is_only_noted():
    sweeps = [{"index": i, "temperature_c": None, "typed_ohm": None,
               "crossing_ohm": 7.0} for i in (1, 2, 3)]
    found = audit_scan(sweeps)
    assert {f.severity for f in found} == {NOTE}


def test_findings_sort_worst_first():
    from wrdkit.eis.audit import Finding
    mixed = [Finding(NOTE, "a", ""), Finding(PROBLEM, "b", ""), Finding(CHECK, "c", "")]
    assert [f.code for f in sort_findings(mixed)] == ["b", "c", "a"]
    assert worst([]) is None
