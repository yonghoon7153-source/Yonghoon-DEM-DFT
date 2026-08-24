"""Differential voltage — dV/dQ, the sibling of dQ/dV.

dQ/dV turns a plateau into a peak.  dV/dQ turns the *boundaries between*
plateaus into peaks and the plateaus themselves into valleys, and that
difference is the reason to have both rather than one.

- On dQ/dV a peak's **area** is the capacity of that phase transition, so it
  answers "how much of this material is still active".
- On dV/dQ the **spacing between two peaks** is the capacity between two stage
  boundaries -- a length along the x axis, read straight off the plot.  That
  is what makes it the standard tool for splitting loss of lithium inventory
  from loss of active material: the electrode-slippage picture is drawn in
  capacity, not in voltage.

The numerical problem is the mirror image of dQ/dV's and so is the fix
(ADR 0013, ADR 0015).  There the denominator dV collapses on a plateau; here
the denominator dQ collapses during a **constant-voltage hold and any rest**,
where charge stops moving while voltage keeps changing.  Same answer: build a
uniform grid in the variable we divide by -- capacity -- interpolate onto it,
differentiate, smooth.

Sign convention matches ``ica``: the branch is kept as measured.  Charging
gives dV/dQ > 0, discharging < 0, and the two on one plot show hysteresis.
Never take ``abs`` here; that erases which way the current went.

Units out are V/mAh.  Normalisation is the caller's job (ADR 0001) -- and note
it goes the *other* way from dQ/dV: dividing capacity by mass makes the
denominator smaller, so V/(mAh/g) is a **larger** number than V/mAh, not a
smaller one.  ``normalize.normalize_per_capacity`` exists precisely so that the
inversion is written down once, and tested.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .cycles import Profile
from .ica import (
    DEFAULT_POLY_ORDER,
    DEFAULT_SMOOTHER,
    DEFAULT_SMOOTHING,
    MIN_SAMPLES,
    SMOOTHERS,
    smooth,
)

__all__ = ["DifferentialVoltage", "differential_voltage",
           "differential_voltages"]

#: Grid spacing, as a fraction of the branch's own capacity span.
#:
#: Deliberately *relative*, where dQ/dV's grid is absolute.  A voltage window
#: is 2.5-4.5 V for a coin cell and for a pouch cell alike, so 5 mV means the
#: same thing on both.  Capacity does not work that way: 0.05 mAh is a sixth of
#: a 0.3 mAh dry-electrode button cell and a rounding error on a 3000 mAh
#: pouch.  A fixed step would give one of them four points and the other sixty
#: thousand.  1/400 of the span gives every cell the same resolution in the
#: only unit that is comparable between them -- state of charge.
DEFAULT_CAPACITY_FRACTION = 1.0 / 400.0

#: The branch has to actually pass some charge.  Below this the "curve" is the
#: instrument's last-digit noise divided by itself.
MIN_SPAN_MAH = 1e-6


@dataclass
class DifferentialVoltage:
    """One branch's dV/dQ, on the capacity grid it was computed on.

    Empty ``capacity``/``dv_dq`` with a filled ``reason`` is the honest answer
    for a branch that cannot support the calculation -- the same contract as
    ``DifferentialCapacity`` and ``KneeResult``.

    ``capacity_step`` is reported in mAh (the resolved step, not the fraction)
    because that is what a reader needs to judge whether two peaks that look
    adjacent are actually resolved.
    """

    cycle_number: int
    branch: str
    capacity: np.ndarray = field(default_factory=lambda: np.empty(0))
    dv_dq: np.ndarray = field(default_factory=lambda: np.empty(0))
    capacity_step: float = 0.0
    smoothing: int = DEFAULT_SMOOTHING
    smoother: str = DEFAULT_SMOOTHER
    poly_order: int = DEFAULT_POLY_ORDER
    points_used: int = 0
    points_dropped: int = 0
    reason: str = ""

    def __len__(self) -> int:
        return len(self.capacity)

    @property
    def usable(self) -> bool:
        return len(self.capacity) > 0


def advancing_mask(capacity: np.ndarray) -> np.ndarray:
    """Samples where charge is still moving.

    The capacity column of a branch is a running total, so it only ever rises
    -- but it stops rising during a constant-voltage hold and during a rest,
    and it is those flat runs that would put a zero in the denominator.  This
    is ``monotonic_mask``'s counterpart, and it is deliberately written as its
    own function rather than reusing that one with ``branch="charge"``: the
    variable is different, and a reader who follows the reuse would conclude
    that a *discharge* needs the falling variant.  It does not.  Capacity
    accumulates upward on both branches.
    """
    if len(capacity) == 0:
        return np.zeros(0, dtype=bool)
    running = np.maximum.accumulate(capacity)
    keep = np.empty(len(capacity), dtype=bool)
    keep[0] = True
    keep[1:] = running[1:] != running[:-1]
    return keep


def differential_voltage(
    profile: Profile,
    *,
    capacity_fraction: float = DEFAULT_CAPACITY_FRACTION,
    capacity_step: float | None = None,
    smoothing: int = DEFAULT_SMOOTHING,
    smoother: str = DEFAULT_SMOOTHER,
    poly_order: int = DEFAULT_POLY_ORDER,
) -> DifferentialVoltage:
    """dV/dQ for one branch of one cycle, in V/mAh.

    ``capacity_step`` in mAh wins when given; otherwise the step is
    ``capacity_fraction`` of this branch's own span.  Both exist because the
    two questions are different: overlaying cycles of one cell wants a fixed
    mAh step so the x axes line up, while comparing cells of different sizes
    wants the relative one.

    Returns an empty curve with a reason rather than raising, so one bad branch
    among ten does not take the other nine off the screen.
    """
    result = DifferentialVoltage(
        cycle_number=profile.cycle_number,
        branch=profile.branch,
        smoothing=smoothing,
        smoother=smoother,
        poly_order=poly_order,
    )
    if smoother not in SMOOTHERS:
        result.reason = f"unknown smoother {smoother!r}"
        return result
    if capacity_step is not None and capacity_step <= 0:
        result.reason = "capacity step must be positive"
        return result
    if capacity_step is None and capacity_fraction <= 0:
        result.reason = "capacity fraction must be positive"
        return result

    voltage = np.asarray(profile.voltage, dtype=np.float64)
    capacity = np.asarray(profile.capacity_mah, dtype=np.float64)
    if len(voltage) != len(capacity) or len(voltage) < MIN_SAMPLES:
        result.reason = f"branch has {len(voltage)} samples, needs {MIN_SAMPLES}"
        return result

    # One non-finite sample becomes a NaN in the interpolation and then, through
    # the smoothing window, a band of NaN as wide as the window.
    finite = np.isfinite(voltage) & np.isfinite(capacity)
    voltage, capacity = voltage[finite], capacity[finite]

    keep = advancing_mask(capacity)
    result.points_used = int(keep.sum())
    result.points_dropped = int(len(capacity) - keep.sum())
    if result.points_used < MIN_SAMPLES:
        result.reason = (
            f"only {result.points_used} samples advance in capacity "
            f"({result.points_dropped} held)")
        return result

    voltage, capacity = voltage[keep], capacity[keep]
    low, high = float(capacity.min()), float(capacity.max())
    span = high - low
    if span < MIN_SPAN_MAH:
        result.reason = f"branch passes {span:.3g} mAh, too little to differentiate"
        return result

    step = capacity_step if capacity_step is not None else span * capacity_fraction
    grid = np.arange(low, high + step * 0.5, step)
    if len(grid) < 3:
        result.reason = (
            f"branch spans fewer than 3 steps of {step:.4g} mAh")
        return result

    on_grid = np.interp(grid, capacity, voltage)
    derivative = np.gradient(on_grid, grid)

    result.capacity = grid
    result.capacity_step = float(step)
    result.dv_dq = smooth(derivative, smoothing, method=smoother,
                          poly_order=poly_order)
    return result


def differential_voltages(
    profiles, *,
    capacity_fraction: float = DEFAULT_CAPACITY_FRACTION,
    capacity_step: float | None = None,
    smoothing: int = DEFAULT_SMOOTHING,
    smoother: str = DEFAULT_SMOOTHER,
    poly_order: int = DEFAULT_POLY_ORDER,
) -> list[DifferentialVoltage]:
    """dV/dQ for many branches, keeping the unusable ones and their reasons."""
    return [differential_voltage(profile, capacity_fraction=capacity_fraction,
                                 capacity_step=capacity_step,
                                 smoothing=smoothing, smoother=smoother,
                                 poly_order=poly_order)
            for profile in profiles]
