"""Request and response shapes.

Capacity fields carry the basis they were computed in, so the client never
has to guess whether a number is mAh or mAh/g.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field, field_validator

from wrdkit import BASES, Basis


class GroupIn(BaseModel):
    name: str
    description: str = ""
    color: str = ""


class GroupUpdate(BaseModel):
    """Every field optional -- a PATCH only touches what it names.

    ``GroupIn`` cannot serve here: its defaults are real values, so
    ``model_dump()`` turns "you did not mention description" into "set
    description to the empty string" and a colour-only edit wipes the text
    somebody wrote.
    """

    name: str | None = None
    description: str | None = None
    color: str | None = None

    @field_validator("name", "description", "color")
    @classmethod
    def _no_explicit_null(cls, value: str | None) -> str | None:
        """`null` is not the same as leaving a field out.

        Omitting a field means "keep it".  These columns are NOT NULL, so
        writing None reaches SQLite as an IntegrityError and the client sees a
        500 for what is really bad input.  Clearing a field is what the empty
        string is for, and that already works.
        """
        if value is None:
            raise ValueError('send "" to clear this field, or omit it to keep it')
        return value


class GroupOut(BaseModel):
    id: int
    name: str
    description: str
    color: str
    created_at: datetime
    updated_at: datetime
    sample_count: int = 0
    run_count: int = 0


# --- 물리량 입력의 문지기 ------------------------------------------------------
#
# 여기가 데이터 계약의 입구다.  음수 질량, NaN, 800 wt% 는 wrdkit 이 뒤에서
# 걸러 주더라도 DB 에는 그대로 남고, 나중에 조회할 때마다 같은 잘못된 수를
# 다시 만들어 낸다.  raw 만 저장한다는 원칙(ADR 0001)은 저장된 raw 가 물리적으로
# 가능한 값일 때만 성립한다.
#
# allow_inf_nan=False 가 핵심이다.  JSON 의 NaN 은 파이썬 float 로 조용히
# 들어와서 모든 산술을 NaN 으로 물들이고, 화면에는 빈칸으로 보인다.
PositiveMass = Annotated[float, Field(gt=0, allow_inf_nan=False)]
NonNegativeMass = Annotated[float, Field(ge=0, allow_inf_nan=False)]
Percent = Annotated[float, Field(ge=0, le=100, allow_inf_nan=False)]
PositiveLength = Annotated[float, Field(gt=0, allow_inf_nan=False)]
Finite = Annotated[float, Field(allow_inf_nan=False)]


class ComponentIn(BaseModel):
    """One ingredient of the electrode film."""

    name: str
    #: 0 wt% is legitimate -- a formulation that lists PTFE at zero is
    #: recording that it has none, and that record is worth keeping.
    wt_percent: Percent = 0.0
    role: str = "other"


class ComponentOut(BaseModel):
    """What comes back, with no input bounds attached.

    Inheriting ``ComponentIn`` looked tidy and made the API unable to show a
    row it had itself stored before the bounds existed: a composition saved
    with wt% 150 then failed *output* validation, so GET /samples/{id} 500'd
    and the one screen that could correct the value refused to open.  Input is
    where a contract is enforced; output has to be able to describe what is
    already there.
    """

    name: str
    wt_percent: float = 0.0
    role: str = "other"


class CellSpecIn(BaseModel):
    """The inputs that turn mAh into mAh/g and mAh/cm2."""

    #: The blend, component by component.  Takes precedence over
    #: ``composition_text`` when both are sent.
    composition: list[ComponentIn] | None = None
    #: The shorthand a researcher types: ``AM:SE:VGCF:PTFE = 80:17:3:0``.
    composition_text: str | None = None
    total_mass_mg: PositiveMass | None = None
    #: Zero is meaningful here: a free-standing film has no collector.
    current_collector_mass_mg: NonNegativeMass | None = None
    active_wt_percent: Percent | None = None
    active_mass_mg: PositiveMass | None = None
    area_cm2: PositiveLength | None = None
    diameter_mm: PositiveLength | None = None
    thickness_um: PositiveLength | None = None
    nominal_specific_capacity_mah_g: PositiveMass | None = None
    #: "Li" | "Li-In" | "LTO" | "" (기록 그대로)
    reference_electrode: str | None = None
    #: 직접 특성화한 오프셋. 표보다 우선한다.
    reference_offset_v: Finite | None = None


class SampleIn(CellSpecIn):
    name: str
    group_id: int | None = None
    test_date: str | None = None
    cathode_type: str = ""
    cathode_detail: str = ""
    anode: str = ""
    electrolyte: str = ""
    process: str = ""
    notes: str = ""
    temperature_c: Finite | None = None
    pressure_mpa: NonNegativeMass | None = None
    cutoff_upper_v: Finite | None = None
    cutoff_lower_v: Finite | None = None
    c_rate: PositiveMass | None = None
    c_rate_formation: PositiveMass | None = None
    #: Cycle numbering starts at 1; cycle 0 does not exist.
    reference_cycle: int = Field(3, ge=1)
    declared_state: str = "auto"


class SampleUpdate(BaseModel):
    """Every field optional -- a PATCH only touches what it names."""

    composition: list[ComponentIn] | None = None
    composition_text: str | None = None
    name: str | None = None
    group_id: int | None = None
    test_date: str | None = None
    cathode_type: str | None = None
    cathode_detail: str | None = None
    anode: str | None = None
    electrolyte: str | None = None
    process: str | None = None
    notes: str | None = None
    total_mass_mg: PositiveMass | None = None
    #: Zero is meaningful here: a free-standing film has no collector.
    current_collector_mass_mg: NonNegativeMass | None = None
    active_wt_percent: Percent | None = None
    active_mass_mg: PositiveMass | None = None
    area_cm2: PositiveLength | None = None
    diameter_mm: PositiveLength | None = None
    thickness_um: PositiveLength | None = None
    nominal_specific_capacity_mah_g: PositiveMass | None = None
    #: "Li" | "Li-In" | "LTO" | "" (기록 그대로)
    reference_electrode: str | None = None
    #: 직접 특성화한 오프셋. 표보다 우선한다.
    reference_offset_v: Finite | None = None
    temperature_c: Finite | None = None
    pressure_mpa: NonNegativeMass | None = None
    cutoff_upper_v: Finite | None = None
    cutoff_lower_v: Finite | None = None
    c_rate: PositiveMass | None = None
    # POST 와 같은 제약이어야 한다.  한쪽만 걸어 두면 저장할 때는 막히는
    # 값이 고칠 때는 통과해, 결국 같은 잘못된 수가 DB 에 들어간다.
    c_rate_formation: PositiveMass | None = None
    reference_cycle: int | None = None
    declared_state: str | None = None
    #: Send null explicitly to clear a numeric field.
    clear: list[str] = Field(default_factory=list)


class ResolvedCellOut(BaseModel):
    active_mass_g: float | None = None
    active_wt_percent: float | None = None
    composition: list[ComponentOut] = Field(default_factory=list)
    composition_label: str = ""
    composition_compact_label: str = ""
    composition_problems: list[str] = Field(default_factory=list)
    area_cm2: float | None = None
    volume_cm3: float | None = None
    loading_mg_cm2: float | None = None
    nominal_capacity_mah: float | None = None
    nominal_specific_capacity_mah_g: float | None = None
    available_bases: list[str] = Field(default_factory=list)
    unavailable: dict[str, str] = Field(default_factory=dict)
    notes: dict[str, str] = Field(default_factory=dict)


class SampleOut(BaseModel):
    id: int
    name: str
    group_id: int | None
    group_name: str | None = None
    test_date: str | None
    cathode_type: str
    cathode_detail: str
    anode: str
    electrolyte: str
    process: str
    notes: str
    total_mass_mg: float | None
    current_collector_mass_mg: float | None
    active_wt_percent: float | None
    active_mass_mg: float | None
    area_cm2: float | None
    diameter_mm: float | None
    thickness_um: float | None
    nominal_specific_capacity_mah_g: float | None
    composition: list[ComponentOut] = Field(default_factory=list)
    composition_label: str = ""
    temperature_c: float | None
    pressure_mpa: float | None
    cutoff_upper_v: float | None
    cutoff_lower_v: float | None
    c_rate: float | None
    c_rate_formation: float | None
    reference_cycle: int
    declared_state: str
    created_at: datetime
    updated_at: datetime
    run_count: int = 0
    cycle_count: int = 0
    resolved_cell: ResolvedCellOut


class RunOut(BaseModel):
    id: int
    sample_id: int | None
    sample_name: str | None = None
    original_name: str
    sha256: str
    size_bytes: int
    uploaded_at: datetime
    device_model: str
    serial_no: str
    channel: int | None
    app_version: str
    firmware_version: str
    start_time: datetime | None
    end_time: datetime | None
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
    sample_id: int | None = None
    cycle_offset: int | None = None
    detach_sample: bool = False


class CycleOut(BaseModel):
    cycle: int
    cycle_index: int
    run_id: int
    charge_capacity: float | None
    discharge_capacity: float | None
    charge_capacity_mah: float | None
    discharge_capacity_mah: float | None
    coulombic_efficiency: float | None
    energy_efficiency: float | None
    charge_energy_mwh: float | None
    discharge_energy_mwh: float | None
    mean_charge_voltage: float | None
    mean_discharge_voltage: float | None
    voltage_hysteresis: float | None
    voltage_max: float | None
    voltage_min: float | None
    retention_pct: float | None = None
    c_rate: float | None = None
    temperature_mean: float | None = None
    duration_h: float
    n_points: int
    complete: bool


class CycleTableOut(BaseModel):
    basis: str
    basis_label: str
    requested_basis: str
    basis_fallback_reason: str | None = None
    #: What was asked for, and what the retention column is really anchored to.
    #: They differ when the reference cycle is not in the record (ADR 0004).
    reference_cycle: int | None = None
    reference_cycle_used: int | None = None
    reference_available: bool = True
    retention_note: str = ""
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
    #: Why this one curve is not in the requested unit, when it is not.
    basis_fallback_reason: str | None = None


class ProfileOut(BaseModel):
    basis: str
    basis_label: str
    requested_basis: str
    resolved_cell: ResolvedCellOut
    series: list[ProfileSeriesOut]
    #: True when the curves are not all in the same unit, so one axis label
    #: cannot describe them and the client has to annotate each curve.
    mixed_basis: bool = False


class ReportOut(BaseModel):
    sample_id: int
    sample_name: str
    state: str
    state_confidence: str
    state_summary: str
    evidence: list[dict[str, str]]
    cycles_observed: int
    cycles_complete: int
    planned_cycles: int | None
    in_progress_cycle: int | None
    reference_cycle_requested: int
    reference_available: bool
    retention_pct: float | None
    retention_note: str
    basis: str
    basis_label: str
    reported: dict[str, Any] | None
    reference: dict[str, Any] | None
    first_cycle: dict[str, Any] | None
    knee: dict[str, Any] | None
    resolved_cell: ResolvedCellOut


class BasisInfo(BaseModel):
    value: str
    label: str


def basis_choices() -> list[BasisInfo]:
    from wrdkit import basis_label

    return [BasisInfo(value=b, label=basis_label(b)) for b in BASES]


DEFAULT_BASIS = Basis.ABSOLUTE
