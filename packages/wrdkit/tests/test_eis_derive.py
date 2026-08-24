"""Naming the arcs, and turning resistances into conductivities.

The same fit means different things in a liquid cell and a solid one.  These
tests exist because the failure is silent: a solid-electrolyte grain boundary
labelled "charge transfer" is a number under the wrong name in a report nobody
re-derives.
"""

import pytest
import synthetic_eis as S

from wrdkit.eis.derive import (
    LIQUID,
    SOLID,
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
    solid = {m.parameter: m.label for m in label_arcs(result, SOLID)}
    assert liquid["R1"] == "SEI 저항"
    assert liquid["R2"] == "전하이동 저항"
    assert solid["R1"] == "벌크 저항"
    assert solid["R2"] == "입계 저항"


def test_the_first_resistance_is_a_series_term_only_when_the_circuit_says_so():
    """``p(R1,CPE1)-p(R2,CPE2)`` has no series element, so R1 is an arc."""
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, rs=0.0, r1=20.0, q1=1e-5, n1=0.9,
                  r2=40.0, q2=1e-3, n2=0.8)
    result = fit_circuit(Spectrum(frequency, z.real, z.imag),
                         "p(R1,CPE1)-p(R2,CPE2)")
    names = {m.parameter: m.label for m in label_arcs(result, SOLID)}
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
