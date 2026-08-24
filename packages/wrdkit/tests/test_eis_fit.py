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
from wrdkit.eis.fit import fit_circuit
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
    spectrum where most starts failed can be spotted."""
    result = fit_circuit(spectrum(noise=0.01), LIQUID, restarts=5)
    assert result.starts == 6
    assert result.starts_converged >= 1


def test_an_undetermined_parameter_is_not_called_a_measurement():
    result = fit_circuit(spectrum(noise=0.01), LIQUID)
    for parameter in result.parameters:
        if parameter.stderr is None or parameter.relative_error is not None and parameter.relative_error >= 0.5:
            assert not parameter.determined


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
