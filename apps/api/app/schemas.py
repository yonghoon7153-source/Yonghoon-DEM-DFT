"""Request and response shapes.

Capacity fields carry the basis they were computed in, so the client never
has to guess whether a number is mAh or mAh/g.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from wrdkit import BASES, Basis


class GroupIn(BaseModel):
    name: str
    description: str = ""
    color: str = ""


class GroupOut(BaseModel):
    id: int
    name: str
    description: str
    color: str
    created_at: datetime
    updated_at: datetime
    sample_count: int = 0
    run_count: int = 0


class CellSpecIn(BaseModel):
    """The inputs that turn mAh into mAh/g and mAh/cm2."""

    total_mass_mg: Optional[float] = None
    current_collector_mass_mg: Optional[float] = None
    active_wt_percent: Optional[float] = None
    active_mass_mg: Optional[float] = None
    area_cm2: Optional[float] = None
    diameter_mm: Optional[float] = None
    thickness_um: Optional[float] = None
    nominal_specific_capacity_mah_g: Optional[float] = None


class SampleIn(CellSpecIn):
    name: str
    group_id: Optional[int] = None
    test_date: Optional[str] = None
    cathode_type: str = ""
    cathode_detail: str = ""
    anode: str = ""
    electrolyte: str = ""
    process: str = ""
    notes: str = ""
    temperature_c: Optional[float] = None
    pressure_mpa: Optional[float] = None
    cutoff_upper_v: Optional[float] = None
    cutoff_lower_v: Optional[float] = None
    c_rate: Optional[float] = None
    c_rate_formation: Optional[float] = None
    reference_cycle: int = 3
    declared_state: str = "auto"


class SampleUpdate(BaseModel):
    """Every field optional -- a PATCH only touches what it names."""

    name: Optional[str] = None
    group_id: Optional[int] = None
    test_date: Optional[str] = None
    cathode_type: Optional[str] = None
    cathode_detail: Optional[str] = None
    anode: Optional[str] = None
    electrolyte: Optional[str] = None
    process: Optional[str] = None
    notes: Optional[str] = None
    total_mass_mg: Optional[float] = None
    current_collector_mass_mg: Optional[float] = None
    active_wt_percent: Optional[float] = None
    active_mass_mg: Optional[float] = None
    area_cm2: Optional[float] = None
    diameter_mm: Optional[float] = None
    thickness_um: Optional[float] = None
    nominal_specific_capacity_mah_g: Optional[float] = None
    temperature_c: Optional[float] = None
    pressure_mpa: Optional[float] = None
    cutoff_upper_v: Optional[float] = None
    cutoff_lower_v: Optional[float] = None
    c_rate: Optional[float] = None
    c_rate_formation: Optional[float] = None
    reference_cycle: Optional[int] = None
    declared_state: Optional[str] = None
    #: Send null explicitly to clear a numeric field.
    clear: list[str] = Field(default_factory=list)


class ResolvedCellOut(BaseModel):
    active_mass_g: Optional[float] = None
    area_cm2: Optional[float] = None
    volume_cm3: Optional[float] = None
    loading_mg_cm2: Optional[float] = None
    nominal_capacity_mah: Optional[float] = None
    nominal_specific_capacity_mah_g: Optional[float] = None
    available_bases: list[str] = Field(default_factory=list)
    unavailable: dict[str, str] = Field(default_factory=dict)
    notes: dict[str, str] = Field(default_factory=dict)


class SampleOut(BaseModel):
    id: int
    name: str
    group_id: Optional[int]
    group_name: Optional[str] = None
    test_date: Optional[str]
    cathode_type: str
    cathode_detail: str
    anode: str
    electrolyte: str
    process: str
    notes: str
    total_mass_mg: Optional[float]
    current_collector_mass_mg: Optional[float]
    active_wt_percent: Optional[float]
    active_mass_mg: Optional[float]
    area_cm2: Optional[float]
    diameter_mm: Optional[float]
    thickness_um: Optional[float]
    nominal_specific_capacity_mah_g: Optional[float]
    temperature_c: Optional[float]
    pressure_mpa: Optional[float]
    cutoff_upper_v: Optional[float]
    cutoff_lower_v: Optional[float]
    c_rate: Optional[float]
    c_rate_formation: Optional[float]
    reference_cycle: int
    declared_state: str
    created_at: datetime
    updated_at: datetime
    run_count: int = 0
    cycle_count: int = 0
    resolved_cell: ResolvedCellOut


class RunOut(BaseModel):
    id: int
    sample_id: Optional[int]
    sample_name: Optional[str] = None
    original_name: str
    sha256: str
    size_bytes: int
    uploaded_at: datetime
    device_model: str
    serial_no: str
    channel: Optional[int]
    app_version: str
    firmware_version: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    row_count: int
    cycle_count: int
    complete_cycle_count: int
    unit_coulomb: bool
    data_format: int
    instrument_path: str
    schedule_path: str
    cycle_offset: int
    cycle_offset_source: str
    parse_error: str
    schedule: dict[str, Any] = Field(default_factory=dict)


class RunUpdate(BaseModel):
    sample_id: Optional[int] = None
    cycle_offset: Optional[int] = None
    detach_sample: bool = False


class CycleOut(BaseModel):
    cycle: int
    cycle_index: int
    run_id: int
    charge_capacity: Optional[float]
    discharge_capacity: Optional[float]
    charge_capacity_mah: float
    discharge_capacity_mah: float
    coulombic_efficiency: Optional[float]
    energy_efficiency: Optional[float]
    charge_energy_mwh: float
    discharge_energy_mwh: float
    mean_charge_voltage: Optional[float]
    mean_discharge_voltage: Optional[float]
    voltage_hysteresis: Optional[float]
    voltage_max: Optional[float]
    voltage_min: Optional[float]
    retention_pct: Optional[float] = None
    c_rate: Optional[float] = None
    temperature_mean: Optional[float] = None
    duration_h: float
    n_points: int
    complete: bool


class CycleTableOut(BaseModel):
    basis: str
    basis_label: str
    requested_basis: str
    basis_fallback_reason: Optional[str] = None
    reference_cycle: Optional[int] = None
    resolved_cell: ResolvedCellOut
    cycles: list[CycleOut]


class ProfileSeriesOut(BaseModel):
    cycle: int
    branch: str
    basis: str
    points: int
    capacity: list[float]
    voltage: list[float]
    run_id: int
    label: str


class ProfileOut(BaseModel):
    basis: str
    basis_label: str
    requested_basis: str
    resolved_cell: ResolvedCellOut
    series: list[ProfileSeriesOut]


class ReportOut(BaseModel):
    sample_id: int
    sample_name: str
    state: str
    state_confidence: str
    state_summary: str
    evidence: list[dict[str, str]]
    cycles_observed: int
    cycles_complete: int
    planned_cycles: Optional[int]
    in_progress_cycle: Optional[int]
    reference_cycle_requested: int
    reference_available: bool
    retention_pct: Optional[float]
    retention_note: str
    basis: str
    basis_label: str
    reported: Optional[dict[str, Any]]
    reference: Optional[dict[str, Any]]
    first_cycle: Optional[dict[str, Any]]
    knee: Optional[dict[str, Any]]
    resolved_cell: ResolvedCellOut


class BasisInfo(BaseModel):
    value: str
    label: str


def basis_choices() -> list[BasisInfo]:
    from wrdkit import basis_label

    return [BasisInfo(value=b, label=basis_label(b)) for b in BASES]


DEFAULT_BASIS = Basis.ABSOLUTE
