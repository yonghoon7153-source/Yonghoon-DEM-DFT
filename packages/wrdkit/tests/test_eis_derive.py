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


def test_the_total_ionic_conductivity_comes_from_the_summed_resistance():
    """Not the sum of the two conductivities.

    The resistances are in series, so they add; summing sigmas instead
    over-states the total, and the result still looks like a conductivity.
    """
    out = ionic_conductivity(fitted(), thickness_cm=0.007, area_cm2=0.785)
    assert out["missing"] == []
    expected = 0.007 / ((20.0 + 40.0) * 0.785)
    assert out["total_s_cm"] == pytest.approx(expected, rel=0.01)
    assert out["total_s_cm"] < out["bulk_s_cm"]
    assert out["total_s_cm"] < out["grain_boundary_s_cm"]
    naive = out["bulk_s_cm"] + out["grain_boundary_s_cm"]
    assert naive > out["total_s_cm"] * 2


def test_the_series_resistance_is_left_out_of_the_ionic_total():
    """Wiring is not ion transport.  A cell thickness divided by a contact
    resistance has the units of a conductivity and the meaning of nothing."""
    out = ionic_conductivity(fitted(rs=500.0), thickness_cm=0.007, area_cm2=0.785)
    expected = 0.007 / ((20.0 + 40.0) * 0.785)
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
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, rs=5.0, r1=20.0, q1=1e-5, n1=0.9,
                  r2=40.0, q2=1e-3, n2=0.8)
    result = fit_circuit(Spectrum(frequency, z.real, z.imag),
                         "p(R1,CPE1)-p(R2,CPE2)-R0")
    labels = {m.parameter: m.label for m in label_arcs(result, SOLID, SYMMETRIC)}
    assert labels["R0"] == "직렬 저항"
    assert labels["R1"] == "벌크 저항"
    assert labels["R2"] == "입계 저항"

    out = ionic_conductivity(result, thickness_cm=0.007, area_cm2=0.785,
                             config=SYMMETRIC)
    expected = 0.007 / ((20.0 + 40.0) * 0.785)
    assert out["total_s_cm"] == pytest.approx(expected, rel=0.02)


def test_a_third_arc_is_kept_out_of_the_ionic_total_and_named():
    """세 번째 아크는 자기 라벨부터 '전극 계면일 수 있습니다' 다.

    σ 합계에 넣으면 전해질 전도도가 그만큼 과소평가된다 — 리뷰 재현에서
    100 Ω 계면 아크가 σ_total 을 2.7배 깎았다, 표시 없이.  빼고, 뺐다고
    말한다.
    """
    frequency = S.log_sweep(1e6, 1e-3, 12)
    z = S.randles(frequency, rs=5.0, r1=20.0, q1=1e-6, n1=0.95,
                  r2=40.0, q2=1e-4, n2=0.9)
    # 세 번째 아크(계면 100 Ω)를 손으로 직렬로 얹는다.
    w = 2 * np.pi * frequency
    z = z + 1.0 / (1.0 / 100.0 + 1e-2 * (1j * w) ** 0.85)
    result = fit_circuit(Spectrum(frequency, z.real, z.imag),
                         "R0-p(R1,CPE1)-p(R2,CPE2)-p(R3,CPE3)", restarts=12)
    assert result.converged

    out = ionic_conductivity(result, thickness_cm=0.007, area_cm2=0.785,
                             config=SYMMETRIC)
    expected = 0.007 / ((20.0 + 40.0) * 0.785)
    assert out["total_s_cm"] == pytest.approx(expected, rel=0.1)
    assert len(out["excluded"]) == 1
    assert "R3" in out["excluded"][0]
