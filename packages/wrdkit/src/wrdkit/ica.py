"""Differential capacity — dQ/dV, the incremental-capacity curve.

A charge curve's plateau is where a phase transition happens, and a plateau is
exactly what a capacity plot renders as a featureless flat line.  dQ/dV turns
each plateau into a peak, so where it sits and how it changes with cycling says
which mechanism is degrading.

Computing it from the definition does not work, and the reason is worth
stating: the denominator is the voltage step between samples, and on a plateau
that step falls to the instrument's resolution.  The plateau is the part we
came to look at.  During a constant-voltage hold the step is *exactly* zero
while capacity keeps rising.  Dividing by those numbers produces spikes that
look like peaks and are noise.

So the curve is built on a voltage grid we choose (ADR 0013):

1. keep only the monotonic part of the branch -- this drops the CV hold and
   any noise-driven backtracking, because dQ/dV is undefined where dV is zero
   and the honest thing is to leave it out rather than invent it;
2. interpolate capacity onto a uniform grid, so the denominator is ours;
3. differentiate with a central difference;
4. smooth with a moving average over an odd window.

Units out are mAh/V.  Normalising to mAh/g/V is the caller's job, so that
correcting a mass never requires re-reading the file (ADR 0001).

**Discharge comes out negative, and that is the answer, not a bug.**  Capacity
rises while voltage falls, so dQ/dV is genuinely below zero there.  Keeping the
sign is what lets a charge and a discharge share one plot and show their
hysteresis: peaks up, peaks down, and the gap between them is the thing you
came to see.  Take ``abs`` at the point of display if a single-sided plot is
wanted -- never here, where it would erase which direction the current went.

Measured against a real 161-cycle cell: integrating the curve back over voltage
returns the branch capacity to within 0.01-0.07 % on discharge.  Charge lands
0.7-2.6 % low, and that shortfall *is* the constant-voltage hold this module
deliberately drops -- it grows with cycle number (3, 7, 10 samples at cycles 3,
80, 161) exactly as a cell ageing into longer CV tails should.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .cycles import Profile

__all__ = ["DifferentialCapacity", "differential_capacities",
           "differential_capacity", "monotonic_mask"]

#: Grid spacing, in volts.  5 mV resolves graphite staging and keeps a
#: 2.5-4.5 V window to 400 points, which draws without downsampling.
DEFAULT_VOLTAGE_STEP = 0.005

#: Moving-average width, in grid points.  Forced odd: an even window shifts
#: the result half a cell, and in an analysis whose answer *is* a peak
#: position that half cell is not free.
DEFAULT_SMOOTHING = 5

#: Below this many usable samples there is nothing to differentiate.  Three is
#: the minimum a central difference needs; ten is where the result stops being
#: an artefact of two or three points.
MIN_SAMPLES = 10

#: A branch has to actually span some voltage.  20 mV is four grid cells at
#: the default step -- narrower than that and every peak is the window.
MIN_SPAN_V = 0.02


@dataclass
class DifferentialCapacity:
    """One branch's dQ/dV, on the grid it was computed on.

    ``voltage`` and ``dq_dv`` are empty when the branch could not support the
    calculation; ``reason`` then says why, in the manner of ``KneeResult`` --
    a guess presented as a measurement is worse than a blank.

    ``voltage_step`` and ``smoothing`` ride along because they change the
    answer: smoothing lowers and widens a peak, so comparing peak *heights*
    between cells is only meaningful when both were built the same way.  A
    screen or a CSV has to be able to say what it is showing.
    """

    cycle_number: int
    branch: str
    voltage: np.ndarray = field(default_factory=lambda: np.empty(0))
    dq_dv: np.ndarray = field(default_factory=lambda: np.empty(0))
    voltage_step: float = DEFAULT_VOLTAGE_STEP
    smoothing: int = DEFAULT_SMOOTHING
    #: Samples that survived the monotonic filter, and how many did not.
    points_used: int = 0
    points_dropped: int = 0
    reason: str = ""

    def __len__(self) -> int:
        return len(self.voltage)

    @property
    def usable(self) -> bool:
        return len(self.voltage) > 0


def monotonic_mask(voltage: np.ndarray, branch: str) -> np.ndarray:
    """Samples where the voltage is still moving the way the branch moves.

    Charging keeps the samples that set a new running maximum, discharging a
    new running minimum.  What this removes is the constant-voltage hold at
    the end of a charge -- where dV is zero and dQ is not -- and the small
    backwards wobbles noise puts on a slow curve.  Both would otherwise
    contribute a division by something at or near zero.

    Equality counts as *not* moving: a run of identical voltages is a hold,
    and keeping its first sample only is what makes the survivors strictly
    monotonic, which is what interpolation needs.
    """
    if len(voltage) == 0:
        return np.zeros(0, dtype=bool)
    if branch == "charge":
        running = np.maximum.accumulate(voltage)
    else:
        running = np.minimum.accumulate(voltage)
    keep = np.empty(len(voltage), dtype=bool)
    keep[0] = True
    # A sample is kept when it moved the running extreme, i.e. when it is the
    # first to reach that value.
    keep[1:] = running[1:] != running[:-1]
    return keep


def _moving_average(values: np.ndarray, window: int) -> np.ndarray:
    """Smooth without moving the peaks or eating the ends.

    The edges are averaged over whatever falls inside the array rather than
    zero-padded.  Zero padding pulls the first and last points towards zero,
    and on a dQ/dV curve the ends are the cutoff voltages -- the place a
    reader looks to see whether the cell reached them.
    """
    if window <= 1 or len(values) == 0:
        return values
    window = min(window, len(values))
    if window % 2 == 0:
        window -= 1
    if window <= 1:
        return values
    half = window // 2
    padded = np.concatenate([values[:half][::-1], values, values[-half:][::-1]])
    kernel = np.ones(window) / window
    return np.convolve(padded, kernel, mode="valid")


def differential_capacity(
    profile: Profile,
    *,
    voltage_step: float = DEFAULT_VOLTAGE_STEP,
    smoothing: int = DEFAULT_SMOOTHING,
) -> DifferentialCapacity:
    """dQ/dV for one branch of one cycle, in mAh/V.

    Returns an empty curve with a reason rather than raising: one unusable
    branch among ten selected cycles should leave the other nine on screen.
    """
    result = DifferentialCapacity(
        cycle_number=profile.cycle_number,
        branch=profile.branch,
        voltage_step=voltage_step,
        smoothing=smoothing,
    )
    if voltage_step <= 0:
        result.reason = "voltage step must be positive"
        return result

    voltage = np.asarray(profile.voltage, dtype=np.float64)
    capacity = np.asarray(profile.capacity_mah, dtype=np.float64)
    if len(voltage) != len(capacity) or len(voltage) < MIN_SAMPLES:
        result.reason = f"branch has {len(voltage)} samples, needs {MIN_SAMPLES}"
        return result

    # Non-finite samples poison every later step: one NaN in the input becomes
    # a NaN in the interpolation and then, through the moving average, a band
    # of NaN wide as the window.
    finite = np.isfinite(voltage) & np.isfinite(capacity)
    voltage, capacity = voltage[finite], capacity[finite]

    keep = monotonic_mask(voltage, profile.branch)
    result.points_used = int(keep.sum())
    result.points_dropped = int(len(voltage) - keep.sum())
    if result.points_used < MIN_SAMPLES:
        result.reason = (
            f"only {result.points_used} samples move in voltage "
            f"({result.points_dropped} held or reversed)")
        return result

    voltage, capacity = voltage[keep], capacity[keep]
    low, high = float(voltage.min()), float(voltage.max())
    if high - low < MIN_SPAN_V:
        result.reason = f"branch spans {high - low:.3f} V, needs {MIN_SPAN_V} V"
        return result

    # np.interp wants ascending x.  A discharge runs the other way, so it is
    # flipped rather than special-cased downstream -- the grid is ascending
    # either way, and a plot that always reads left to right in volts is the
    # one people can compare between charge and discharge.
    if voltage[0] > voltage[-1]:
        voltage, capacity = voltage[::-1], capacity[::-1]

    grid = np.arange(low, high + voltage_step * 0.5, voltage_step)
    if len(grid) < 3:
        result.reason = f"branch spans fewer than 3 steps of {voltage_step} V"
        return result

    on_grid = np.interp(grid, voltage, capacity)
    # `np.gradient` uses a central difference inside and one-sided differences
    # at the ends, so the result keeps the grid's length and its edges are not
    # silently biased the way a plain `diff` would leave them.
    derivative = np.gradient(on_grid, grid)

    result.voltage = grid
    result.dq_dv = _moving_average(derivative, smoothing)
    return result


def differential_capacities(
    profiles, *, voltage_step: float = DEFAULT_VOLTAGE_STEP,
    smoothing: int = DEFAULT_SMOOTHING,
) -> list[DifferentialCapacity]:
    """dQ/dV for many branches, keeping the unusable ones and their reasons."""
    return [differential_capacity(profile, voltage_step=voltage_step,
                                  smoothing=smoothing)
            for profile in profiles]
