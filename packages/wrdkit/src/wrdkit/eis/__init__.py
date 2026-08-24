"""Impedance: read a spectrum, fit a circuit to it, say how well it fitted.

Kept apart from the cycling code because nothing is shared but the cell it was
measured on -- different instrument, different file, different axes (ADR 0019).

Fitting needs scipy, which the rest of ``wrdkit`` does not: install
``wrdkit[eis]``.  Reading and plotting work without it, so a machine that only
looks at spectra does not need the dependency.
"""

from .biologic import UnknownColumn, read_mpr_bytes, read_mps_text, read_mpt_text
from .circuit import Circuit, CircuitError, parse_circuit
from .derive import (
    LIQUID,
    SOLID,
    conductivity,
    ionic_conductivity,
    label_arcs,
    total_resistance,
)
from .guess import Arc, find_arcs, inductive_mask, initial_guess
from .spectrum import Spectrum

__all__ = ["Arc", "Circuit", "CircuitError", "LIQUID", "SOLID", "Spectrum",
           "UnknownColumn", "conductivity", "find_arcs", "inductive_mask",
           "initial_guess", "ionic_conductivity", "label_arcs", "parse_circuit",
           "read_mpr_bytes", "read_mps_text", "read_mpt_text",
           "total_resistance"]


def __getattr__(name):
    """``fit_circuit`` and friends, imported only when asked for.

    ``from wrdkit.eis import Spectrum`` must work on a machine without scipy --
    otherwise the reader, which needs nothing but numpy, becomes unusable
    because of a dependency only the fitter has.
    """
    if name in ("fit_circuit", "FitResult", "Parameter"):
        from . import fit
        return getattr(fit, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
