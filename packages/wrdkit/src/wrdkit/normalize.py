"""Turn raw mAh into the units a battery lab actually reports.

A dry-processed electrode gets re-weighed and re-punched constantly, so the
mass and area that convert mAh into mAh/g and mAh/cm2 change far more often
than the underlying measurement.  Everything here is therefore a pure
function of (raw capacity, cell spec): the parsed file is never re-read when
a mass is corrected, and no normalised number is ever persisted.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable

import numpy as np

__all__ = [
    "CellSpec", "ResolvedCell", "Basis", "BASES", "basis_label",
    "normalize_capacity", "c_rate", "areal_loading",
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
    """

    active_mass_mg: float | None = None
    total_mass_mg: float | None = None
    current_collector_mass_mg: float | None = None
    active_wt_percent: float | None = None
    area_cm2: float | None = None
    diameter_mm: float | None = None
    thickness_um: float | None = None
    nominal_specific_capacity_mah_g: float | None = None

    def resolve(self) -> "ResolvedCell":
        notes: dict[str, str] = {}

        mass_g: float | None = None
        if self.active_mass_mg and self.active_mass_mg > 0:
            mass_g = self.active_mass_mg / 1000.0
            notes["active_mass"] = "entered directly"
        elif self.total_mass_mg and self.total_mass_mg > 0:
            electrode_mg = self.total_mass_mg - (self.current_collector_mass_mg or 0.0)
            if electrode_mg <= 0:
                notes["active_mass"] = "current collector mass exceeds total mass"
            else:
                fraction = (self.active_wt_percent or 100.0) / 100.0
                mass_g = electrode_mg * fraction / 1000.0
                parts = [f"{electrode_mg:g} mg"]
                if self.current_collector_mass_mg:
                    parts.append(f"(after {self.current_collector_mass_mg:g} mg collector)")
                parts.append(f"x {fraction * 100:g} wt%")
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

        return ResolvedCell(
            active_mass_g=mass_g,
            area_cm2=area,
            volume_cm3=volume,
            nominal_capacity_mah=nominal,
            nominal_specific_capacity_mah_g=self.nominal_specific_capacity_mah_g,
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
    notes: dict[str, str] = field(default_factory=dict)

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
            return self.active_mass_g or None
        if basis == Basis.AREAL:
            return self.area_cm2 or None
        if basis == Basis.VOLUMETRIC:
            return self.volume_cm3 or None
        if basis == Basis.NORMALIZED:
            if not self.nominal_capacity_mah:
                return None
            return self.nominal_capacity_mah / 100.0
        raise ValueError(f"unknown basis {basis!r}")

    def available_bases(self) -> list[str]:
        return [b for b in BASES if self.divisor(b)]

    def missing_for(self, basis: str) -> str | None:
        """Human-readable reason a basis cannot be used, if it cannot."""
        if self.divisor(basis):
            return None
        return {
            Basis.SPECIFIC: "active mass not set",
            Basis.AREAL: "electrode area not set",
            Basis.VOLUMETRIC: "electrode area and thickness not set",
            Basis.NORMALIZED: "active mass and nominal specific capacity not set",
        }.get(basis, "unavailable")


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
    """Capacity retention (%) against one reference cycle."""
    values = list(capacities)
    if not values:
        return []
    if not 0 <= reference_index < len(values):
        reference_index = 0
    reference = values[reference_index]
    if not reference:
        return [None] * len(values)
    return [None if v is None else 100.0 * v / reference for v in values]
