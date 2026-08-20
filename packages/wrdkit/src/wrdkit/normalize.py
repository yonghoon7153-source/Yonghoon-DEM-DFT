"""Turn raw mAh into the units a battery lab actually reports.

A dry-processed electrode gets re-weighed and re-punched constantly, so the
mass and area that convert mAh into mAh/g and mAh/cm2 change far more often
than the underlying measurement.  Everything here is therefore a pure
function of (raw capacity, cell spec): the parsed file is never re-read when
a mass is corrected, and no normalised number is ever persisted.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass, field

import numpy as np

from .composition import Composition

__all__ = [
    "CellSpec", "ResolvedCell", "Basis", "BASES", "basis_label",
    "normalize_capacity", "c_rate", "areal_loading", "retention",
]


class Basis:
    """Supported capacity axes."""

    ABSOLUTE = "mAh"
    SPECIFIC = "mAh/g"
    AREAL = "mAh/cm2"
    VOLUMETRIC = "mAh/cm3"
    NORMALIZED = "%"  # percent of the nominal (theoretical) capacity


BASES = (Basis.ABSOLUTE, Basis.SPECIFIC, Basis.AREAL, Basis.VOLUMETRIC, Basis.NORMALIZED)

_LABELS = {
    Basis.ABSOLUTE: "Capacity (mAh)",
    Basis.SPECIFIC: "Specific capacity (mAh g⁻¹)",
    Basis.AREAL: "Areal capacity (mAh cm⁻²)",
    Basis.VOLUMETRIC: "Volumetric capacity (mAh cm⁻³)",
    Basis.NORMALIZED: "Capacity utilisation (%)",
}


def basis_label(basis: str) -> str:
    return _LABELS.get(basis, basis)


def _positive(value: float | None) -> float | None:
    """A mass or an area that is not positive is a typo, not a divisor.

    ``value or None`` would let a negative float through and turn it into a
    negative mAh/g that reads like a real measurement.
    """
    return value if value is not None and value > 0 else None


@dataclass
class CellSpec:
    """What the operator knows about the electrode, in lab units.

    Active mass can be given three ways, in order of precedence:

    1. ``active_mass_mg`` directly;
    2. ``total_mass_mg`` minus ``current_collector_mass_mg``, times
       ``active_wt_percent`` -- the dry-electrode workflow, where a punched
       disc is weighed and the composition is known;
    3. not at all, in which case mAh/g is simply unavailable.

    Area likewise comes from ``area_cm2`` or from ``diameter_mm`` (the
    ``13pi`` punch in the file names).

    ``composition`` records the whole blend (AM : SE : conductive : binder).
    It supplies ``active_wt_percent`` when that was not set directly, and --
    more importantly -- it makes the provenance of the denominator visible:
    "80 wt% because the electrode is AM:SE:VGCF = 80:17:3", not just "80".
    """

    active_mass_mg: float | None = None
    total_mass_mg: float | None = None
    current_collector_mass_mg: float | None = None
    active_wt_percent: float | None = None
    area_cm2: float | None = None
    diameter_mm: float | None = None
    thickness_um: float | None = None
    nominal_specific_capacity_mah_g: float | None = None
    composition: Composition | None = None

    @property
    def effective_active_wt_percent(self) -> float | None:
        """The active weight fraction the maths will use, and nothing else.

        An explicit ``active_wt_percent`` wins, because a researcher who typed
        a number meant it; otherwise the composition supplies one.
        """
        if self.active_wt_percent is not None:
            return self.active_wt_percent
        if self.composition and not self.composition.is_empty():
            return self.composition.active_wt_percent
        return None

    @property
    def composition_names_no_active(self) -> bool:
        """A blend was written down, and none of it is active material.

        This is not the same as writing nothing down, and the difference
        decides a number that gets published.  With no composition at all the
        only reading available is "the mass I was given is the active mass" --
        wrong in general, but stated as an assumption.  With a composition
        whose every component is unrecognised, the operator *did* tell us what
        the film is, and the honest answer is that the active fraction is
        unknown (non-negotiable #4).  Treating the two the same puts the
        binder, the electrolyte and the carbon into the mAh/g denominator and
        reports the result as if it were measured.
        """
        if self.active_wt_percent is not None or not self.composition:
            return False
        if self.composition.is_empty():
            return False
        # "no component is active" only.  A blend that *does* name an active
        # material at 0 wt% is a different statement -- the operator weighed it
        # and it is zero -- and it already has its own reason.
        return not any(c.role == "active" for c in self.composition.components)

    @property
    def unrecognised_component_names(self) -> list[str]:
        """Components whose role could not be told from their name."""
        if not self.composition:
            return []
        return [c.name for c in self.composition.components
                if c.role == "other" and c.wt_percent]

    def resolve(self) -> ResolvedCell:
        notes: dict[str, str] = {}

        mass_g: float | None = None
        if self.active_mass_mg is not None and self.active_mass_mg <= 0:
            # A sign typo must not fall through to the total-mass path, where
            # it would look like the operator never entered a mass at all.
            notes["active_mass"] = "directly entered active mass is not positive - ignored"
        elif self.active_mass_mg:
            mass_g = self.active_mass_mg / 1000.0
            notes["active_mass"] = "entered directly"
        elif self.total_mass_mg and self.total_mass_mg > 0:
            electrode_mg = self.total_mass_mg - (self.current_collector_mass_mg or 0.0)
            wt_percent = self.effective_active_wt_percent
            if electrode_mg <= 0:
                notes["active_mass"] = "current collector mass exceeds total mass"
            elif self.composition_names_no_active:
                unknown = self.unrecognised_component_names
                detail = (f" - none of {', '.join(unknown)} is a known active material"
                          if unknown else "")
                notes["active_mass"] = (
                    "the composition names no active material" + detail
                    + "; enter the active wt% to use mAh/g")
            elif wt_percent is not None and not 0 <= wt_percent <= 100:
                # -80 or 800 would silently make mAh/g negative or eight times
                # too small; a fraction outside [0, 100] is not a fraction.
                notes["active_mass"] = (
                    f"active wt% {wt_percent:g} is outside [0, 100] - ignored")
            else:
                fraction = (100.0 if wt_percent is None else wt_percent) / 100.0
                mass_g = electrode_mg * fraction / 1000.0
                parts = [f"{electrode_mg:g} mg"]
                if self.current_collector_mass_mg:
                    parts.append(f"(after {self.current_collector_mass_mg:g} mg collector)")
                if wt_percent is None:
                    parts.append("x 100 wt% (no composition given - assuming the whole "
                                 "electrode is active material)")
                else:
                    parts.append(f"x {fraction * 100:g} wt%")
                    if self.active_wt_percent is None and self.composition:
                        parts.append(f"from {self.composition.label()}")
                notes["active_mass"] = " ".join(parts)

        area: float | None = None
        if self.area_cm2 and self.area_cm2 > 0:
            area = self.area_cm2
            notes["area"] = "entered directly"
        elif self.diameter_mm and self.diameter_mm > 0:
            radius_cm = self.diameter_mm / 20.0
            area = math.pi * radius_cm * radius_cm
            notes["area"] = f"π x ({self.diameter_mm:g} mm / 2)²"

        volume: float | None = None
        if area and self.thickness_um and self.thickness_um > 0:
            volume = area * (self.thickness_um * 1e-4)
            notes["volume"] = f"{area:.4g} cm² x {self.thickness_um:g} µm"

        nominal: float | None = None
        if mass_g and self.nominal_specific_capacity_mah_g:
            nominal = mass_g * self.nominal_specific_capacity_mah_g
            notes["nominal_capacity"] = (
                f"{mass_g * 1000:.4g} mg x {self.nominal_specific_capacity_mah_g:g} mAh/g"
            )

        composition = self.composition
        if composition and composition.problems():
            notes["composition"] = "; ".join(composition.problems())

        return ResolvedCell(
            active_mass_g=mass_g,
            area_cm2=area,
            volume_cm3=volume,
            nominal_capacity_mah=nominal,
            nominal_specific_capacity_mah_g=self.nominal_specific_capacity_mah_g,
            active_wt_percent=self.effective_active_wt_percent,
            composition=composition,
            composition_label=composition.label() if composition else "",
            composition_problems=composition.problems() if composition else [],
            notes=notes,
        )


@dataclass
class ResolvedCell:
    """A :class:`CellSpec` reduced to the numbers the maths needs."""

    active_mass_g: float | None = None
    area_cm2: float | None = None
    volume_cm3: float | None = None
    nominal_capacity_mah: float | None = None
    nominal_specific_capacity_mah_g: float | None = None
    active_wt_percent: float | None = None
    composition: Composition | None = None
    composition_label: str = ""
    composition_problems: list[str] = field(default_factory=list)
    notes: dict[str, str] = field(default_factory=dict)

    @property
    def composition_compact_label(self) -> str:
        """The blend on one line, with 0 wt% components left out."""
        return self.composition.label(skip_zero=True) if self.composition else ""

    @property
    def loading_mg_cm2(self) -> float | None:
        """Active-material areal loading -- the headline dry-electrode number."""
        if not self.active_mass_g or not self.area_cm2:
            return None
        return self.active_mass_g * 1000.0 / self.area_cm2

    def divisor(self, basis: str) -> float | None:
        """Factor that converts mAh into *basis*, or ``None`` if unavailable."""
        if basis == Basis.ABSOLUTE:
            return 1.0
        if basis == Basis.SPECIFIC:
            return _positive(self.active_mass_g)
        if basis == Basis.AREAL:
            return _positive(self.area_cm2)
        if basis == Basis.VOLUMETRIC:
            return _positive(self.volume_cm3)
        if basis == Basis.NORMALIZED:
            nominal = _positive(self.nominal_capacity_mah)
            return None if nominal is None else nominal / 100.0
        raise ValueError(f"unknown basis {basis!r}")

    def available_bases(self) -> list[str]:
        return [b for b in BASES if self.divisor(b)]

    def missing_for(self, basis: str) -> str | None:
        """Human-readable reason a basis cannot be used, if it cannot.

        The reason has to match what is actually absent.  Telling someone the
        area is missing when the area is set and the thickness is not sends
        them to re-enter a number that was already right.
        """
        if self.divisor(basis):
            return None
        if basis == Basis.SPECIFIC:
            if self.active_mass_g == 0 and self.active_wt_percent == 0:
                return "active material is 0 wt% of the composition"
            return "active mass not set"
        if basis == Basis.AREAL:
            return "electrode area not set"
        if basis == Basis.VOLUMETRIC:
            # Thickness is not carried here, so it can only be named as the
            # sole culprit once the area is known to be present.
            if _positive(self.area_cm2) is not None:
                return "electrode thickness not set"
            return "electrode area and thickness not set"
        if basis == Basis.NORMALIZED:
            has_mass = _positive(self.active_mass_g) is not None
            has_nominal = _positive(self.nominal_specific_capacity_mah_g) is not None
            if has_mass and not has_nominal:
                return "nominal specific capacity not set"
            if has_nominal and not has_mass:
                return "active mass not set"
            return "active mass and nominal specific capacity not set"
        return "unavailable"


def normalize_capacity(values, cell: ResolvedCell, basis: str):
    """Convert mAh to *basis*.  Accepts a scalar, a sequence or an ndarray."""
    divisor = cell.divisor(basis)
    if divisor is None:
        raise ValueError(f"cannot express capacity as {basis}: {cell.missing_for(basis)}")
    if isinstance(values, np.ndarray):
        return values / divisor
    if isinstance(values, (list, tuple)):
        return [None if v is None else v / divisor for v in values]
    if values is None:
        return None
    return values / divisor


def c_rate(current_a: float, cell: ResolvedCell,
           measured_capacity_mah: float | None = None) -> float | None:
    """Express a current as a C-rate.

    Prefers the nominal capacity the operator specified; falls back to a
    measured capacity so a file with no nominal value still gets a rate.
    """
    reference = cell.nominal_capacity_mah or measured_capacity_mah
    if not reference:
        return None
    return abs(current_a) * 1000.0 / reference


def areal_loading(cell: ResolvedCell) -> float | None:
    return cell.loading_mg_cm2


def retention(capacities: Iterable[float | None], reference_index: int = 0
              ) -> list[float | None]:
    """Capacity retention (%) against one reference cycle.

    A reference the series does not contain yields ``None`` throughout, not a
    quiet fallback to the first cycle: cycles 1-2 are formation and lose a few
    percent by design, so anchoring there would report formation loss as
    degradation (ADR 0004).
    """
    values = list(capacities)
    if not values:
        return []
    if not 0 <= reference_index < len(values):
        return [None] * len(values)
    reference = values[reference_index]
    if not reference:
        return [None] * len(values)
    return [None if v is None else 100.0 * v / reference for v in values]
