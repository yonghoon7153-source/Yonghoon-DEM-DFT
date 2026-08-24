"""The circuit language, and that it computes the impedance it claims to.

Every element is checked against a closed form rather than against the
implementation, because the whole point of the fitting module is that it agrees
with what a textbook says a circuit does.
"""

import numpy as np
import pytest

from wrdkit.eis.circuit import CircuitError, parse_circuit


def test_a_series_string_names_its_parameters_in_order():
    circuit = parse_circuit("R0-p(R1,CPE1)-p(R2,CPE2)")
    assert circuit.parameter_names == (
        "R0", "R1", "CPE1_Q", "CPE1_n", "R2", "CPE2_Q", "CPE2_n")
    assert circuit.element_names() == ["R0", "R1", "CPE1", "R2", "CPE2"]


def test_a_single_parameter_element_keeps_its_bare_name():
    """``R1``, not ``R1_R``.  The screen shows these and so does the CSV."""
    assert parse_circuit("R1-C1").parameter_names == ("R1", "C1")


def test_resistors_in_series_add():
    circuit = parse_circuit("R1-R2")
    z = circuit.impedance([3.0, 4.0], [1.0, 1000.0])
    assert z.real == pytest.approx([7.0, 7.0])
    assert z.imag == pytest.approx([0.0, 0.0])


def test_resistors_in_parallel_halve():
    circuit = parse_circuit("p(R1,R2)")
    z = circuit.impedance([10.0, 10.0], [1.0])
    assert z.real == pytest.approx([5.0])


def test_an_rc_pair_is_a_semicircle_at_its_own_frequency():
    """At w = 1/RC the impedance of R||C is exactly R/2 - jR/2.

    That single point pins both the parallel arithmetic and the capacitor's
    sign: if Im came out positive the arc would be drawn above the axis.
    """
    r, c = 100.0, 1e-6
    frequency = 1.0 / (2 * np.pi * r * c)
    z = parse_circuit("p(R1,C1)").impedance([r, c], [frequency])
    assert z.real[0] == pytest.approx(r / 2)
    assert z.imag[0] == pytest.approx(-r / 2)


def test_a_cpe_with_n_one_is_a_capacitor():
    frequency = [1.0, 10.0, 1000.0]
    cpe = parse_circuit("CPE1").impedance([1e-6, 1.0], frequency)
    capacitor = parse_circuit("C1").impedance([1e-6], frequency)
    assert cpe == pytest.approx(capacitor)


def test_a_warburg_sits_at_forty_five_degrees():
    z = parse_circuit("W1").impedance([10.0], [0.1, 1.0, 10.0])
    assert np.degrees(np.angle(z)) == pytest.approx([-45.0] * 3)


def test_the_two_finite_warburgs_are_not_the_same_element():
    """Ws uses tanh and Wo uses coth.  Swapping them is a silent physics bug:
    one returns to the real axis, the other turns capacitive."""
    low = [1e-3]
    ws = parse_circuit("Ws1").impedance([50.0, 1.0], low)
    wo = parse_circuit("Wo1").impedance([50.0, 1.0], low)
    assert abs(ws[0]) < abs(wo[0])
    # At low frequency Ws tends to its own R; Wo diverges.
    assert ws.real[0] == pytest.approx(50.0, rel=1e-3)
    assert abs(wo[0]) > 1e3


def test_an_unknown_element_is_named_in_the_error():
    with pytest.raises(CircuitError, match="Zed"):
        parse_circuit("R0-Zed1")


def test_two_elements_with_the_same_name_are_refused():
    """Otherwise one parameter silently shadows the other in every report."""
    with pytest.raises(CircuitError, match="R1"):
        parse_circuit("R1-p(R1,CPE1)")


def test_unbalanced_brackets_are_refused():
    with pytest.raises(CircuitError, match=r"unbalanced"):
        parse_circuit("R0-p(R1,CPE1")


def test_a_parallel_block_needs_two_members():
    with pytest.raises(CircuitError, match="at least two"):
        parse_circuit("p(R1)")


def test_the_wrong_number_of_parameters_is_refused():
    circuit = parse_circuit("R0-p(R1,CPE1)")
    with pytest.raises(CircuitError, match="takes 4"):
        circuit.impedance([1.0, 2.0], [1.0])
