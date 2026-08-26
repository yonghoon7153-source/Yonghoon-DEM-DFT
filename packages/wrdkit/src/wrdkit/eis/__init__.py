"""Impedance: read a spectrum, fit a circuit to it, ask it how many processes.

Kept apart from the cycling code because nothing is shared but the cell it was
measured on -- different instrument, different file, different axes (ADR 0019).

Fitting and DRT need scipy, which the rest of ``wrdkit`` does not: install
``wrdkit[eis]``.  Both import it **inside the function that needs it**, so a
machine that only reads and plots spectra can import everything here without
the dependency -- and one that tries to fit gets a sentence telling it what to
install rather than an ImportError from three frames down.
"""

from . import drt
from .biologic import UnknownColumn, read_mpr_bytes, read_mps_text, read_mpt_text
from .circuit import Circuit, CircuitError, parse_circuit
from .derive import (
    CONFIGS,
    FULL,
    HALF,
    LIQUID,
    SOLID,
    SYMMETRIC,
    conductivity,
    ionic_conductivity,
    label_arcs,
    total_resistance,
)
from .drt import DrtPeak, DrtResult, lcurve_corner
from .fit import EdgeMisfit, FitResult, Parameter, edge_misfit, fit_circuit
from .guess import Arc, find_arcs, inductive_mask, initial_guess
from .spectrum import Spectrum

__all__ = ["Arc", "CONFIGS", "Circuit", "CircuitError", "DrtPeak", "DrtResult",
           "EdgeMisfit", "FULL", "FitResult", "HALF", "LIQUID", "Parameter",
           "SOLID",
           "SYMMETRIC", "Spectrum", "UnknownColumn", "conductivity", "drt",
           "edge_misfit", "find_arcs", "fit_circuit", "inductive_mask",
           "initial_guess",
           "ionic_conductivity", "label_arcs", "lcurve_corner", "parse_circuit",
           "read_mpr_bytes", "read_mps_text", "read_mpt_text",
           "total_resistance"]
