"""Initial values, read off the spectrum instead of typed in.

The lab's procedure sheet is explicit that this is the step that decides
whether a fit works: *R1 은 전극의 Solution Bulk Resistance (X절편 값), R2 는
첫번째 Semi-Circle 지름, R3 는 두번째 Semi-Circle 지름, CPE-T 는 1e-4/1e-3,
CPE-P 는 0.6~1.2*.  Those are rules a person applies by looking at the plot, so
they are rules code can apply too -- and then the fit can be run many times
without anybody looking at anything.

Each arc is found where it actually lives: at its own characteristic frequency,
the top of a hump in -Z'' against log f.  Two arcs that overlap on the Nyquist
plot are still two humps there, because their relaxation times differ -- which
is the whole reason impedance is measured across frequency at all.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .circuit import ELEMENTS, Circuit
from .spectrum import Spectrum

__all__ = ["Arc", "find_arcs", "initial_guess", "inductive_mask"]


@dataclass
class Arc:
    """One hump in -Z'' vs log f, and what it implies for an R-CPE pair."""

    #: Frequency at the top of the hump.  ``w_peak * tau = 1``.
    peak_hz: float
    #: -Z'' at the top.  For an ideal arc this is half the diameter.
    peak_neg_z_im: float
    #: Estimated diameter -- the resistance of the R in the R-CPE pair.
    diameter_ohm: float
    #: Where the arc starts on the real axis.
    left_ohm: float
    index: int


def inductive_mask(spectrum: Spectrum) -> np.ndarray:
    """Points that sit **above** the real axis -- wiring, not the cell.

    Real spectra start inductive: the reference file is positive-imaginary from
    7 MHz down to a few hundred kHz.  Those points are the cables and the cell
    holder, and no cell circuit can reproduce them.  Left in, they drag the
    series resistance and the first arc off by whole ohms; dropped silently,
    the series resistance changes and nobody knows why.  So this returns the
    mask and the caller decides -- and says so on screen (ADR 0019).
    """
    return spectrum.z_im > 0


def _smooth(values: np.ndarray, window: int) -> np.ndarray:
    """Moving average, edge-padded.  Nothing clever: this only has to stop a
    single noisy point from being called an arc."""
    if window < 3 or len(values) < window:
        return values
    if window % 2 == 0:
        window += 1
    pad = window // 2
    padded = np.concatenate([np.full(pad, values[0]), values,
                             np.full(pad, values[-1])])
    kernel = np.ones(window) / window
    return np.convolve(padded, kernel, mode="valid")


def find_arcs(spectrum: Spectrum, *, max_arcs: int = 3,
              smoothing: int = 3) -> list[Arc]:
    """Locate arcs, high frequency first.

    A hump has to clear two hurdles to count.  It must be a local maximum of
    -Z'' with real minima on both sides (a shoulder on the way down to the
    diffusion tail is not an arc), and its height must be a real fraction of
    the largest hump -- otherwise measurement noise on a flat stretch becomes a
    third arc, and the fit gains two free parameters describing nothing.
    """
    ordered = spectrum.sorted_by_frequency(descending=True)
    keep = ~inductive_mask(ordered)
    ordered = ordered.select(keep)
    if len(ordered) < 5:
        return []

    neg_im = -ordered.z_im
    smoothed = _smooth(neg_im, smoothing)
    peaks = []
    for i in range(1, len(smoothed) - 1):
        if smoothed[i] >= smoothed[i - 1] and smoothed[i] > smoothed[i + 1]:
            peaks.append(i)
    if not peaks:
        return []

    tallest = max(smoothed[i] for i in peaks)
    #: A hump under a tenth of the tallest is noise or a shoulder.  Ten per
    #: cent is low enough to keep a small bulk arc next to a large boundary arc
    #: -- the case this lab actually has in solid electrolytes.
    peaks = [i for i in peaks if smoothed[i] >= 0.10 * tallest]
    peaks = sorted(peaks, key=lambda i: -smoothed[i])[:max_arcs]
    peaks.sort()

    arcs = []
    for order, i in enumerate(peaks):
        left_i = i
        while left_i > 0 and smoothed[left_i - 1] < smoothed[left_i]:
            left_i -= 1
        right_i = i
        while right_i < len(smoothed) - 1 and smoothed[right_i + 1] < smoothed[right_i]:
            right_i += 1
        left = float(ordered.z_re[left_i])
        right = float(ordered.z_re[right_i])
        # An ideal arc's height is half its diameter; a depressed one is
        # shorter.  Take whichever of the two readings is larger -- the width
        # on the real axis, or twice the height -- because under-estimating the
        # diameter is what starts a fit inside the wrong arc.
        diameter = max(right - left, 2.0 * float(neg_im[i]))
        arcs.append(Arc(peak_hz=float(ordered.frequency_hz[i]),
                        peak_neg_z_im=float(neg_im[i]),
                        diameter_ohm=diameter, left_ohm=left, index=order))
    return arcs


def series_resistance(spectrum: Spectrum) -> float:
    """The high-frequency real-axis intercept -- the procedure sheet's R1.

    Not simply ``min(Z')``: on a spectrum with an inductive tail the smallest
    real part can sit up at megahertz where the cell is not being measured at
    all.  Take the real part where the (non-inductive) spectrum starts, and
    never let it go negative.
    """
    ordered = spectrum.sorted_by_frequency(descending=True)
    usable = ordered.select(~inductive_mask(ordered))
    if len(usable) == 0:
        usable = ordered
    candidate = float(usable.z_re[0])
    floor = float(np.min(usable.z_re))
    return max(min(candidate, floor), 1e-6)


#: What to start a CPE at when the spectrum cannot say.  The procedure sheet's
#: numbers: 1e-4 for the first, 1e-3 for the second.
_CPE_FALLBACK_Q = (1e-4, 1e-3, 1e-2)


def initial_guess(spectrum: Spectrum, circuit: Circuit) -> np.ndarray:
    """Starting values for every parameter of *circuit*.

    Arcs are matched to ``p(R, CPE)`` pairs in circuit order, highest frequency
    first, because that is the order they are written in and the order they
    happen in.  Anything the spectrum cannot speak to falls back to the
    procedure sheet's numbers rather than to 1.0 -- a CPE started at 1 F is
    twelve orders of magnitude out and no optimiser walks that far.
    """
    arcs = find_arcs(spectrum)
    rs = series_resistance(spectrum)
    span = float(np.max(spectrum.z_re) - np.min(spectrum.z_re)) or 1.0

    names = list(circuit.parameter_names)
    values = np.zeros(len(names))
    element_kinds = _kinds_by_name(circuit)

    arc_index = 0
    used_series_r = False
    for i, name in enumerate(names):
        kind = element_kinds[name]
        if kind == "R":
            if not used_series_r:
                values[i] = rs
                used_series_r = True
            else:
                arc = arcs[arc_index] if arc_index < len(arcs) else None
                values[i] = arc.diameter_ohm if arc else span / (len(arcs) + 1)
                arc_index = min(arc_index + 1, max(len(arcs) - 1, 0)) \
                    if arcs else arc_index
        elif name.endswith("_Q"):
            # w_peak = 1 / (R Q)^(1/n) for an R-CPE pair; with n near 1 that
            # is Q = 1 / (R w_peak), which turns the located arc into a
            # capacitance instead of a guess.
            slot = min(_cpe_slot(names, i), len(_CPE_FALLBACK_Q) - 1)
            paired_r = _preceding_arc_resistance(names, values, i)
            arc = arcs[min(slot, len(arcs) - 1)] if arcs else None
            if arc and paired_r > 0:
                omega = 2 * np.pi * arc.peak_hz
                values[i] = float(np.clip(1.0 / (paired_r * omega), 1e-12, 1e2))
            else:
                values[i] = _CPE_FALLBACK_Q[slot]
        elif name.endswith("_n"):
            # 0.85 rather than 1.0: real arcs are depressed, and starting at
            # the boundary leaves the optimiser pressed against it.
            values[i] = 0.85
        elif kind == "C":
            values[i] = 1e-6
        elif kind == "L":
            values[i] = 1e-7
        elif kind == "W" or name.endswith("_R"):
            values[i] = span
        elif name.endswith("_tau"):
            values[i] = 1.0
        else:
            values[i] = 1.0
    return np.clip(values, circuit.lower, circuit.upper)


def _kinds_by_name(circuit: Circuit) -> dict[str, str]:
    out: dict[str, str] = {}
    for element in circuit.element_names():
        kind = "".join(ch for ch in element if ch.isalpha())
        for suffix in ELEMENTS[kind].suffixes:
            out[element + suffix] = kind
    return out


def _cpe_slot(names: list[str], index: int) -> int:
    """How many CPE ``_Q`` parameters come before this one."""
    return sum(1 for name in names[:index] if name.endswith("_Q"))


def _preceding_arc_resistance(names: list[str], values: np.ndarray,
                              index: int) -> float:
    """The resistance this CPE is in parallel with -- the R just before it.

    Circuit order puts ``p(R2,CPE1)`` next to each other, so the nearest
    preceding plain ``R`` is the pair.  It is a convention, not a deduction,
    which is why it only sets a starting point.
    """
    for i in range(index - 1, -1, -1):
        if "_" not in names[i] and names[i][0] == "R":
            return float(values[i])
    return 0.0
