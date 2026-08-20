"""Reference electrodes: turning what the instrument measured into what gets published.

An all-solid-state sulfide cell is usually built against a Li-In alloy counter
electrode rather than lithium metal, because Li metal reduces the electrolyte.
The instrument then records the cathode's potential *versus Li-In*, and every
number in the file is on that scale -- but papers report versus Li/Li+, and so
does everyone's lab notebook.  The gap is a constant 0.62 V, which is exactly
large enough to be wrong and small enough to look plausible: a 4.40 V cutoff
shows up as 3.78 V, and a 2.50 V discharge floor as 1.88 V.

So the offset is a *display convention*, stored once per cell and applied on
the way out (ADR 0001: the database keeps what the instrument said).

What it may and may not touch
-----------------------------
A potential shifts; a difference does not; an energy must not.

- Potentials shift: the profile's voltage, ``voltage_max``/``voltage_min``,
  the schedule's cutoffs, and the energy-weighted mean voltages.  The last one
  works out because a weighted mean is linear: mean(V + c) = mean(V) + c, for
  the same weights.
- Differences already cancel it: ``voltage_hysteresis`` is
  mean_charge - mean_discharge, so both ends carry +c and it drops out.
  Shifting it again would invent 0.62 V of polarisation that is not there.
- Energies must not move.  The cell really did deliver E = integral of V.I.dt
  against its actual counter electrode; re-basing that to a reference the cell
  was never built against would report an energy nobody measured, and would
  change energy efficiency, which is a ratio of two energies at different
  capacities.  Energy stays as recorded, and the UI says which scale it is on.
"""

from __future__ import annotations

__all__ = ["ReferenceElectrode", "REFERENCE_ELECTRODES", "offset_for", "shift_potential"]


class ReferenceElectrode:
    """The electrode a measurement was taken against."""

    LITHIUM = "Li"
    LI_IN = "Li-In"
    LTO = "LTO"
    CUSTOM = "custom"


#: Potential of each reference versus Li/Li+, in volts.
#:
#: Li-In is the two-phase In/LiIn plateau at 0.62 V, the flat region the alloy
#: is deliberately held in so that it *is* a reference rather than drifting
#: with state of charge.  LTO's 1.55 V plateau is used the same way.
REFERENCE_ELECTRODES: tuple[tuple[str, float, str], ...] = (
    (ReferenceElectrode.LITHIUM, 0.0, "Li 금속 (vs Li/Li⁺ 그대로)"),
    (ReferenceElectrode.LI_IN, 0.62, "Li-In 합금 (+0.62 V) — 황화물계 전고체 표준"),
    (ReferenceElectrode.LTO, 1.55, "Li₄Ti₅O₁₂ (+1.55 V)"),
)

_BY_NAME = {name: volts for name, volts, _ in REFERENCE_ELECTRODES}


def offset_for(electrode: str | None, custom_offset_v: float | None = None) -> float:
    """Volts to add so a potential reads against Li/Li+.

    An explicit ``custom_offset_v`` wins: a researcher who measured their own
    reference means that number.  An unknown name yields 0.0 rather than an
    error -- refusing to draw a curve because a label is unfamiliar is worse
    than drawing it on the scale the file already used, which is what the
    unset case does anyway.
    """
    if custom_offset_v is not None:
        return float(custom_offset_v)
    if not electrode:
        return 0.0
    return _BY_NAME.get(electrode, 0.0)


def shift_potential(value: float | None, offset_v: float) -> float | None:
    """A potential on the Li/Li+ scale, or ``None`` when there was none."""
    if value is None:
        return None
    return float(value) + offset_v
