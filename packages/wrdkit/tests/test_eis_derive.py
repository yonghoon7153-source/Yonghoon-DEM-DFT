"""Naming the arcs, and turning resistances into conductivities.

The same fit means different things in a liquid cell and a solid one.  These
tests exist because the failure is silent: a solid-electrolyte grain boundary
labelled "charge transfer" is a number under the wrong name in a report nobody
re-derives.
"""

import numpy as np
import pytest
import synthetic_eis as S

from wrdkit.eis.derive import (
    FULL,
    LIQUID,
    SOLID,
    SYMMETRIC,
    conductivity,
    ionic_conductivity,
    label_arcs,
    total_resistance,
)
from wrdkit.eis.fit import fit_circuit
from wrdkit.eis.spectrum import Spectrum

CIRCUIT = "R0-p(R1,CPE1)-p(R2,CPE2)"


def fitted(**overrides):
    values = {"rs": 5.0, "r1": 20.0, "q1": 1e-5, "n1": 0.9, "r2": 40.0,
              "q2": 1e-3, "n2": 0.8}
    values.update(overrides)
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, **values)
    return fit_circuit(Spectrum(frequency, z.real, z.imag), CIRCUIT)


def test_the_same_fit_gets_different_names_in_the_two_worlds():
    result = fitted()
    liquid = {m.parameter: m.label for m in label_arcs(result, LIQUID)}
    solid = {m.parameter: m.label for m in label_arcs(result, SOLID, SYMMETRIC)}
    assert liquid["R1"] == "SEI 저항"
    assert liquid["R2"] == "전하이동 저항"
    assert solid["R1"] == "벌크 저항"
    assert solid["R2"] == "입계 저항"


def test_a_solid_full_cell_does_not_get_the_symmetric_cell_names():
    """같은 두 아크가 대칭셀에서는 벌크·입계고 풀셀에서는 아니다.

    풀셀은 전극이 활물질이므로 저주파 아크를 계면이 지배한다.  거기에
    '입계 저항' 이라는 이름을 붙이고 두께를 나누면, 전도도가 아닌 것에
    S/cm 이 붙는다.
    """
    result = fitted()
    full = {m.parameter: m.label for m in label_arcs(result, SOLID, FULL)}
    assert full["R1"] == "전해질 저항"
    assert full["R2"] == "계면 저항"


def test_without_a_cell_configuration_the_solid_arcs_are_not_named():
    """모르면 모른다고 하고, 무엇을 물어야 하는지 함께 말한다 (§0.4)."""
    arcs = {m.parameter: m for m in label_arcs(fitted(), SOLID)}
    assert arcs["R1"].label == "고주파 아크"
    assert "셀 구성" in arcs["R1"].note


def test_an_unknown_cell_configuration_is_refused():
    with pytest.raises(ValueError, match="unknown cell configuration"):
        label_arcs(fitted(), SOLID, "coin")


def test_the_first_resistance_is_a_series_term_only_when_the_circuit_says_so():
    """``p(R1,CPE1)-p(R2,CPE2)`` has no series element, so R1 is an arc."""
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, rs=0.0, r1=20.0, q1=1e-5, n1=0.9,
                  r2=40.0, q2=1e-3, n2=0.8)
    result = fit_circuit(Spectrum(frequency, z.real, z.imag),
                         "p(R1,CPE1)-p(R2,CPE2)")
    names = {m.parameter: m.label for m in label_arcs(result, SOLID, SYMMETRIC)}
    assert names["R1"] == "벌크 저항"
    assert names["R2"] == "입계 저항"


def test_an_unknown_kind_is_refused_rather_than_defaulted():
    with pytest.raises(ValueError, match="unknown measurement kind"):
        label_arcs(fitted(), "gitt")


def test_conductivity_needs_both_a_thickness_and_an_area():
    assert conductivity(50.0, thickness_cm=None, area_cm2=1.0) is None
    assert conductivity(50.0, thickness_cm=0.007, area_cm2=None) is None
    assert conductivity(0.0, thickness_cm=0.007, area_cm2=1.0) is None


def test_conductivity_is_length_over_resistance_times_area():
    assert conductivity(100.0, thickness_cm=0.01, area_cm2=0.5) == \
        pytest.approx(0.01 / (100.0 * 0.5))


def test_a_full_cell_gets_no_conductivity_at_all():
    """저주파 아크가 계면이면 그것은 이온 전도가 아니다.  숫자를 내지 않는다."""
    out = ionic_conductivity(fitted(), thickness_cm=0.007, area_cm2=0.785,
                             config=FULL)
    assert out["total_s_cm"] is None
    assert out["missing"]


def test_without_a_cell_configuration_no_conductivity_is_offered():
    out = ionic_conductivity(fitted(), thickness_cm=0.007, area_cm2=0.785,
                             config="")
    assert out["total_s_cm"] is None
    assert "셀 구성" in " ".join(out["missing"])


#: 물리적으로 맞는 블로킹 펠릿 (700 µm, 10 mm) — 전도도 시험은 이것으로 한다.
#:
#: 전에는 `fitted()` 의 아크(Q 1e-5, 1e-3)로 σ 를 냈는데, 70 µm 펠릿에서 그것은
#: µF·mF — 전극 이중층의 크기다.  실측 검수가 연구실 데이터에서 잡아낸 바로 그
#: 오류가 시험에 박혀 있었다 (2026-09-23, ADR 0041).  벌크 5e-11 F (C·l/A
#: 4.5e-12), 입계 1e-8 F (C·l/A 8.9e-10), 끝에 이중층 CPE.
PELLET_CM = 0.07
PELLET_AREA = 0.785
PELLET = {"rs": 5.0, "r1": 2e4, "q1": 1.0e-10, "n1": 0.95,
          "r2": 4e4, "q2": 3.23e-8, "n2": 0.85}
PELLET_CIRCUIT = "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"


def fitted_pellet(circuit=PELLET_CIRCUIT, q_block=1e-6, restarts=24, **overrides):
    values = dict(PELLET, **overrides)
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, q_block=q_block, **values)
    # 시작점을 넉넉히 — 해가 하나뿐이면 "비교 못 함" 으로 결정이 안 된다.
    return fit_circuit(Spectrum(frequency, z.real, z.imag), circuit,
                       restarts=restarts)


def test_the_total_ionic_conductivity_comes_from_the_summed_resistance():
    """Not the sum of the two conductivities.

    The resistances are in series, so they add; summing sigmas instead
    over-states the total, and the result still looks like a conductivity.
    """
    out = ionic_conductivity(fitted_pellet(), thickness_cm=PELLET_CM,
                             area_cm2=PELLET_AREA)
    assert out["missing"] == []
    assert out["total_from"] == "arcs"
    expected = PELLET_CM / ((2e4 + 4e4) * PELLET_AREA)
    assert out["total_s_cm"] == pytest.approx(expected, rel=0.01)
    assert out["total_s_cm"] < out["bulk_s_cm"]
    assert out["total_s_cm"] < out["grain_boundary_s_cm"]
    naive = out["bulk_s_cm"] + out["grain_boundary_s_cm"]
    assert naive > out["total_s_cm"] * 2


def test_the_series_resistance_is_left_out_of_the_ionic_total():
    """Wiring is not ion transport.  A cell thickness divided by a contact
    resistance has the units of a conductivity and the meaning of nothing."""
    out = ionic_conductivity(fitted_pellet(rs=500.0), thickness_cm=PELLET_CM,
                             area_cm2=PELLET_AREA)
    expected = PELLET_CM / ((2e4 + 4e4) * PELLET_AREA)
    assert out["total_s_cm"] == pytest.approx(expected, rel=0.02)


def test_a_missing_dimension_is_named_rather_than_assumed():
    out = ionic_conductivity(fitted(), thickness_cm=None, area_cm2=0.785)
    assert out["total_s_cm"] is None
    assert "두께" in out["missing"]


def test_a_total_resistance_built_on_an_undetermined_number_is_withheld():
    result = fitted()
    result.parameters[1].stderr = 1e6      # R1 is now meaningless
    assert total_resistance(result) is None


def test_a_series_resistor_written_last_is_still_the_series_resistor():
    """`p(R1,CPE1)-p(R2,CPE2)-R0` 는 물리적으로 같은 회로다.

    "문자열이 R 로 시작하나" 휴리스틱은 이 표기에서 배선 저항을 아크로
    분류해 σ 합계에 넣었다 (리뷰 재현: σ_total 8% 오차).  직렬인지는 구조가
    정한다.
    """
    result = fitted_pellet("p(R1,CPE1)-p(R2,CPE2)-R0", q_block=None)
    labels = {m.parameter: m.label for m in label_arcs(result, SOLID, SYMMETRIC)}
    assert labels["R0"] == "직렬 저항"
    assert labels["R1"] == "벌크 저항"
    assert labels["R2"] == "입계 저항"

    out = ionic_conductivity(result, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA,
                             config=SYMMETRIC)
    expected = PELLET_CM / ((2e4 + 4e4) * PELLET_AREA)
    assert out["total_s_cm"] == pytest.approx(expected, rel=0.02)


def test_a_third_arc_is_kept_out_of_the_ionic_total_and_named():
    """세 번째 아크는 자기 라벨부터 '전극 계면일 수 있습니다' 다.

    σ 합계에 넣으면 전해질 전도도가 그만큼 과소평가된다 — 리뷰 재현에서
    100 Ω 계면 아크가 σ_total 을 2.7배 깎았다, 표시 없이.  빼고, 뺐다고
    말한다.
    """
    frequency = S.log_sweep(1e6, 1e-3, 12)
    z = S.randles(frequency, **PELLET)
    # 세 번째 아크(전극 계면 1e5 Ω, 1e-5 F 대)를 손으로 직렬로 얹는다.
    w = 2 * np.pi * frequency
    z = z + 1.0 / (1.0 / 1e5 + 1e-5 * (1j * w) ** 0.9)
    result = fit_circuit(Spectrum(frequency, z.real, z.imag),
                         "R0-p(R1,CPE1)-p(R2,CPE2)-p(R3,CPE3)", restarts=12)
    assert result.converged

    out = ionic_conductivity(result, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA,
                             config=SYMMETRIC)
    expected = PELLET_CM / ((2e4 + 4e4) * PELLET_AREA)
    assert out["total_s_cm"] == pytest.approx(expected, rel=0.1)
    assert len(out["excluded"]) == 1
    assert "R3" in out["excluded"][0]


# --- 대칭셀이 정말로 이온을 막는가 (2026-09-23) -----------------------------
#
# 대칭셀에는 막는 것(SS|전해질|SS)과 안 막는 것(Li|전해질|Li)이 있다.  벌크·
# 입계로 나눠 전도도를 낼 수 있는 것은 앞쪽뿐인데 셀 구성 "대칭셀" 은 둘을 안
# 가른다.  실측 `2600922_No1_55_sym_60um_#1_C01` 이 안 막는 쪽이었는데 화면이
# 두 아크를 벌크·입계라 부르며 σ 를 냈다.


from wrdkit.eis.derive import blocking_verdict  # noqa: E402

_F = np.logspace(-2, 6, 60)
_W = 2 * np.pi * _F


def _zarc(r, q, n):
    return r / (1 + r * q * (1j * _W) ** n)


#: 그 셀의 맞춤값 그대로 — 끝에 블로킹이 없다.
_USER_CELL = 4.897 + _zarc(10.42, 3.06e-5, 0.658) + _zarc(6.635, 1.36e-3, 0.757)


def test_a_cell_that_passes_dc_is_not_blocking():
    """저주파 위상이 0° 로 돌아오고 스펙트럼이 실수축 위에서 끝난다."""
    got = blocking_verdict(_F, _USER_CELL.real, _USER_CELL.imag)
    assert got["blocking"] is False
    assert abs(got["phase_deg"]) < 5
    # 그 셀의 보드 그림과 같은 수 — R0+R1+R2 에서 끝난다.
    assert abs(_USER_CELL[0]) == pytest.approx(21.95, abs=0.05)
    assert "막지 않습니다" in got["reason"]


def test_a_blocking_cell_is_blocking():
    blocked = _USER_CELL + 1 / (1e-5 * (1j * _W) ** 0.9)
    got = blocking_verdict(_F, blocked.real, blocked.imag)
    assert got["blocking"] is True
    assert got["phase_deg"] < -60


def test_in_between_is_said_to_be_unclear_rather_than_guessed():
    """-60° 와 -30° 사이는 애매하다 — 막는다고도 안 막는다고도 안 한다 (§0.4)."""
    f = np.array([1e-2, 2e-2, 5e-2])
    z = 10.0 * np.exp(1j * np.radians(-45.0)) * np.ones(3)
    got = blocking_verdict(f, z.real, z.imag)
    assert got["blocking"] is None
    assert "애매" in got["reason"]


def test_too_few_points_is_none_with_a_reason():
    got = blocking_verdict([1.0, 2.0], [1.0, 1.0], [0.0, 0.0])
    assert got["blocking"] is None and got["reason"]


def test_the_order_of_points_does_not_matter():
    """EC-Lab 은 내려가며 쓸고 `.mpr` 에 따라 올라가며 쓰는 것도 있다."""
    a = blocking_verdict(_F, _USER_CELL.real, _USER_CELL.imag)
    b = blocking_verdict(_F[::-1], _USER_CELL.real[::-1], _USER_CELL.imag[::-1])
    assert a["blocking"] == b["blocking"]
    assert a["phase_deg"] == pytest.approx(b["phase_deg"])


def test_conductivity_is_refused_when_the_cell_does_not_block():
    """셀 구성이 대칭셀이어도 스펙트럼이 안 막으면 벌크·입계 σ 를 안 낸다."""
    from wrdkit.eis.derive import ionic_conductivity
    from wrdkit.eis.fit import fit_circuit
    from wrdkit.eis.spectrum import Spectrum

    spectrum = Spectrum(frequency_hz=_F, z_re=_USER_CELL.real, z_im=_USER_CELL.imag)
    result = fit_circuit(spectrum, "R0-p(R1,CPE1)-p(R2,CPE2)")
    verdict = blocking_verdict(_F, _USER_CELL.real, _USER_CELL.imag)

    got = ionic_conductivity(result, thickness_cm=0.006, area_cm2=0.785,
                             config="sym", blocking=verdict)
    assert got["bulk_s_cm"] is None and got["total_s_cm"] is None
    assert got.get("not_blocking") is True
    assert any("막지 않습니다" in one for one in got["missing"])

    # 판정을 안 주면 예전처럼 셀 구성만 본다 — 되돌아가는 길이 남아 있다.
    old = ionic_conductivity(result, thickness_cm=0.006, area_cm2=0.785,
                             config="sym")
    assert old.get("not_blocking") is None


# --- 아크가 전해질이 아닐 때: σ 는 고주파 절편에서 (ADR 0041) ---------------------

def sulfide(frequency, r0=8.3, q=1.9e-6, n=0.86, inductance=1.73e-6):
    """황화물 블로킹 펠릿 — 벌크·입계는 잰 주파수 위, 보이는 것은 배선 L,
    절편 R0, 이중층 CPE 뿐 (실측 B15 50 °C 의 맞춤값)."""
    w = 2 * np.pi * frequency
    z = r0 + 1j * w * inductance + 1.0 / (q * (1j * w) ** n)
    return Spectrum(frequency, z.real, z.imag)


def test_a_pellet_with_no_visible_arc_gets_its_sigma_from_the_intercept():
    """`L1-R0-CPE1` — 아크가 없으니 예전 규칙으로는 σ 가 안 나왔다.  이 셀의
    전해질 저항은 R0 이고, 랩이 실수축 교점으로 읽는 그 값이다."""
    frequency = S.log_sweep(7e6, 10.0, 10)
    result = fit_circuit(sulfide(frequency), "L1-R0-CPE1", restarts=24)
    out = ionic_conductivity(result, thickness_cm=0.07, area_cm2=0.785,
                             blocking={"blocking": True})
    assert out["total_from"] == "series"
    assert out["total_ohm"] == pytest.approx(8.3, rel=1e-3)
    assert out["total_s_cm"] == pytest.approx(0.07 / (8.3 * 0.785), rel=1e-3)
    assert "고주파 절편" in out["total_note"]
    assert out["bulk_s_cm"] is None and out["grain_boundary_s_cm"] is None


def test_electrode_sized_arcs_are_not_the_electrolyte():
    """실측 B11–B14: 벌크·입계라 부른 두 아크가 µF 대 — 이름으로 σ 를 내면
    수만 배 작은 σ 가 나온다.  빼고, 전해질은 R0 에서."""
    frequency = S.log_sweep(1e6, 10.0, 12)
    z = S.randles(frequency, rs=84.3, r1=2.92e3, q1=7.47e-6, n1=0.851,
                  r2=2.6e5, q2=9.18e-7, n2=0.99, q_block=2.68e-5, n_block=0.663)
    result = fit_circuit(Spectrum(frequency, z.real, z.imag),
                         "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3", restarts=24)
    out = ionic_conductivity(result, thickness_cm=0.085, area_cm2=0.785,
                             blocking={"blocking": True})
    assert out["electrode_arcs"] == ["R1", "R2"]
    assert all("면 쪽" in line for line in out["excluded"])
    assert out["total_from"] == "series"
    assert out["total_parts"] == ["R0"]
    assert out["total_ohm"] == pytest.approx(84.3, rel=0.02)


def test_without_blocking_the_intercept_is_not_the_electrolyte():
    """막지 않는 셀의 절편은 전해질만이 아니다 — 거기서 σ 를 내지 않는다."""
    frequency = S.log_sweep(7e6, 10.0, 10)
    result = fit_circuit(sulfide(frequency), "L1-R0-CPE1", restarts=24)
    out = ionic_conductivity(result, thickness_cm=0.07, area_cm2=0.785,
                             blocking={"blocking": None, "reason": "애매"})
    # 판정이 애매하면 회로 끝(CPE)을 믿는다 — 사람이 막는 회로를 골랐다.
    assert out["total_from"] == "series"
    stub = fit_circuit(sulfide(frequency), "L1-R0-p(R1,CPE1)", restarts=12)
    closed = ionic_conductivity(stub, thickness_cm=0.07, area_cm2=0.785)
    assert closed["total_s_cm"] is None


class _P:
    """저장된 파라미터처럼 — 이름·값·결정 여부만."""

    def __init__(self, name, value, determined=True):
        self.name, self.value, self.determined = name, value, determined


class _Fit:
    def __init__(self, circuit, values):
        self.circuit = circuit
        self.parameters = [_P(name, value) for name, value in values.items()]


def test_a_bulk_arc_of_boundary_size_keeps_the_total_but_not_its_name():
    """벌크라 부른 아크가 입계 크기 (C·l/A 4.5e-10) — 전해질이긴 하니 합계엔
    들어가지만, '벌크 σ' 라는 이름으로는 내지 않는다.  그리고 벌크 크기의
    아크가 없으니 벌크는 잰 주파수 위, R0 에 있다 (Irvine–Sinclair–West 그림
    4b) — 합계는 R0 부터."""
    fit = _Fit("R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
               {"R0": 5.0, "R1": 2e4, "CPE1_Q": 5e-9, "CPE1_n": 1.0,
                "R2": 4e4, "CPE2_Q": 3e-8, "CPE2_n": 1.0,
                "CPE3_Q": 1e-6, "CPE3_n": 0.9})
    out = ionic_conductivity(fit, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA)
    assert out["bulk_s_cm"] is None
    assert out["missing"] == []
    assert any("R1 (벌크 저항)" in line and "벌크 크기가 아닙니다" in line
               for line in out["notes"])
    assert out["grain_boundary_s_cm"] == pytest.approx(
        PELLET_CM / (4e4 * PELLET_AREA))
    assert out["total_from"] == "series_and_arcs"
    assert out["total_parts"] == ["R0", "R1", "R2"]
    assert out["total_s_cm"] == pytest.approx(PELLET_CM / (60005.0 * PELLET_AREA))


# --- 벌크가 잰 주파수 위에 있을 때 (Irvine–Sinclair–West 그림 4b) ----------------
#
# 700 µm, 10 mm 펠릿.  l/A = 0.0892 cm⁻¹ — 벌크 1e-11 F 는 C·l/A 8.9e-13,
# 입계 5e-9 F 는 4.5e-10, 이중층 2e-6 F 는 C/A 2.5e-6 F/cm².

BULK_SIZED = {"CPE1_Q": 1e-11, "CPE1_n": 1.0}
BOUNDARY_SIZED = {"CPE1_Q": 5e-9, "CPE1_n": 1.0}


def test_a_boundary_arc_after_a_hidden_bulk_adds_to_the_intercept():
    """벌크 반원은 10⁸ Hz 에 있어 안 보이고, 보이는 첫 아크는 입계 크기.
    전해질 저항은 R0 + R1 이다 — R1 만 쓰면 σ 가 2.6 배, R0 만 쓰면 1.6 배
    커진다 (에이전트가 ISW 를 읽고 짚은 경우, 2026-09-23)."""
    fit = _Fit("R0-p(R1,CPE1)-CPE2", {"R0": 8.0, "R1": 5.0, **BOUNDARY_SIZED,
                                      "CPE2_Q": 2e-6, "CPE2_n": 0.9})
    out = ionic_conductivity(fit, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA,
                             blocking={"blocking": True})
    assert out["total_from"] == "series_and_arcs"
    assert out["total_parts"] == ["R0", "R1"]
    assert out["total_s_cm"] == pytest.approx(PELLET_CM / (13.0 * PELLET_AREA))
    assert out["total_s_cm"] == pytest.approx(6.86e-3, rel=1e-3)
    assert out["bulk_s_cm"] is None                 # 이름(벌크)이 틀렸다
    assert "R0 + R1" in out["total_note"] and "그림 4b" in out["total_note"]

    # 그 뒤에 이중층 아크가 하나 더 있어도 전해질은 그대로 R0 + R1.
    fit = _Fit("R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
               {"R0": 8.0, "R1": 5.0, **BOUNDARY_SIZED, "R2": 1e5,
                "CPE2_Q": 2e-6, "CPE2_n": 1.0, "CPE3_Q": 1e-5, "CPE3_n": 0.9})
    out = ionic_conductivity(fit, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA,
                             blocking={"blocking": True})
    assert out["total_parts"] == ["R0", "R1"]
    assert out["electrode_arcs"] == ["R2"]
    assert out["total_s_cm"] == pytest.approx(6.86e-3, rel=1e-3)


def test_a_visible_bulk_keeps_r0_out_and_drops_only_the_electrode_arc():
    """벌크 크기 아크가 보이면 R0 는 배선·접촉이다 — 예전처럼 뺀다.  입계라
    부른 두 번째 아크가 이중층 크기면 그것만 뺀다."""
    fit = _Fit("R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
               {"R0": 3.0, "R1": 1e4, **BULK_SIZED, "R2": 5e4,
                "CPE2_Q": 2e-6, "CPE2_n": 1.0, "CPE3_Q": 1e-5, "CPE3_n": 0.9})
    out = ionic_conductivity(fit, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA,
                             blocking={"blocking": True})
    assert out["total_from"] == "arcs"
    assert out["total_parts"] == ["R1"]
    assert out["bulk_s_cm"] == pytest.approx(PELLET_CM / (1e4 * PELLET_AREA))
    assert out["grain_boundary_s_cm"] is None
    assert out["electrode_arcs"] == ["R2"]
    assert out["total_s_cm"] == pytest.approx(PELLET_CM / (1e4 * PELLET_AREA))


def test_an_undecided_size_falls_back_to_the_names():
    """C·l/A 5e-11 은 벌크 상한의 다섯 배 — 결정된 값이면 입계 쪽이 확실하다
    (식이 흔들려도 세 배).  같은 값이 미결정 Q 에서 나왔으면 열 배까지
    흔들리므로 벌크인지 못 가린다: R0 를 끌어들이지 않고 예전처럼 이름대로."""
    values = {"R0": 3.0, "R1": 1e4, "CPE1_Q": 5.6e-10, "CPE1_n": 1.0,
              "R2": 5e4, "CPE2_Q": 5e-9, "CPE2_n": 1.0,
              "CPE3_Q": 1e-5, "CPE3_n": 0.9}
    sure = ionic_conductivity(_Fit("R0-p(R1,CPE1)-p(R2,CPE2)-CPE3", values),
                              thickness_cm=PELLET_CM, area_cm2=PELLET_AREA,
                              blocking={"blocking": True})
    assert sure["total_parts"] == ["R0", "R1", "R2"]

    shaky = _Fit("R0-p(R1,CPE1)-p(R2,CPE2)-CPE3", values)
    shaky.parameters[2].determined = False           # CPE1_Q
    out = ionic_conductivity(shaky, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA,
                             blocking={"blocking": True})
    assert out["total_from"] == "arcs"
    assert out["total_parts"] == ["R1", "R2"]


def test_a_composite_electrode_cell_gets_no_sigma_from_r0():
    """`R0-TL1` 은 복합전극 대칭셀 — R0 는 전해질 층이지만 적힌 두께가 그 층의
    두께인지 모른다.  예전에도 σ 가 안 나왔다 ("아크" 없음)."""
    fit = _Fit("R0-TL1", {"R0": 10.0, "TL1_Ri": 50.0, "TL1_Re": 1e-3,
                          "TL1_Rct": 1e6, "TL1_Q": 1e-3, "TL1_n": 0.9,
                          "TL1_Wr": 10.0, "TL1_Wn": 0.5, "TL1_Wt": 1.0})
    out = ionic_conductivity(fit, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA,
                             blocking={"blocking": True})
    assert out["total_s_cm"] is None
    assert any("전송선" in line for line in out["missing"])
