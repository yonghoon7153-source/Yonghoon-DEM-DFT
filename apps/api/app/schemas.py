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
    created_by: str = ""
    updated_by: str = ""


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


class ActivityOut(BaseModel):
    """One line of "누가 무엇을 했는지".

    ``actor`` is a display name nobody verified (ADR 0012); "" means the
    person did not say who they were, or the row predates the feature.
    """

    id: int
    at: datetime
    actor: str = ""
    action: str = ""
    entity: str = ""
    entity_id: int | None = None
    #: What it was called at the time -- kept so a deleted thing is still
    #: readable, which is exactly when somebody goes looking for it.
    label: str = ""
    fields: list[str] = Field(default_factory=list)


class PresetSettings(BaseModel):
    """Cell settings a preset may carry.

    These are properties of the *build*, not of the individual cell: the same
    recipe is punched with the same die, rated at the same nominal specific
    capacity, and cycled against the same counter electrode.  Masses are
    deliberately absent -- they are measured per cell, and a preset that
    carried one would put it silently under another cell's mAh/g (ADR 0010).

    Every field is optional and ``None`` means "this preset does not carry
    it", so applying leaves that field alone rather than clearing it.
    """

    area_cm2: PositiveLength | None = None
    diameter_mm: PositiveLength | None = None
    thickness_um: PositiveLength | None = None
    nominal_specific_capacity_mah_g: PositiveMass | None = None
    reference_electrode: str | None = None
    reference_offset_v: Finite | None = None

    def filled(self) -> dict[str, Any]:
        """Only the settings actually set, ready to PATCH onto a sample."""
        return {key: value for key, value in self.model_dump().items()
                if value is not None and value != ""}


class CompositionPresetIn(BaseModel):
    name: str
    composition: list[ComponentIn] = Field(default_factory=list)
    settings: PresetSettings = Field(default_factory=PresetSettings)
    #: Replace a preset that already has this name.  Off by default: saving
    #: over somebody's recipe is a deliberate act, not a side effect of
    #: reusing a name.
    overwrite: bool = False


class CompositionPresetOut(BaseModel):
    id: int
    name: str
    created_by: str = ""
    updated_by: str = ""
    #: ``AM:SE:VGCF = 80:17:3`` -- the blend, as a lab says it.
    text: str
    #: What the dropdown shows: ``이름 · AM:SE:VGCF = 80:17:3``.
    label: str
    composition: list[ComponentOut] = Field(default_factory=list)
    settings: PresetSettings = Field(default_factory=PresetSettings)
    created_at: datetime
    updated_at: datetime


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
    # The counter electrode and its offset were stored and never sent back, so
    # the editor's 기준전극 select re-opened on "환산 안 함" for a cell saved as
    # Li-In -- and looked clean while doing it, because `dirty` compares the
    # draft against exactly this field.  0.62 V is the difference between a
    # 4.40 V cutoff and a 3.78 V one.
    reference_electrode: str = ""
    reference_offset_v: float | None = None
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
    created_by: str = ""
    updated_by: str = ""


class RunOut(BaseModel):
    id: int
    sample_id: int | None
    sample_name: str | None = None
    original_name: str
    sha256: str
    size_bytes: int
    uploaded_at: datetime
    #: 누가 올렸는지.  파일 카드에 이름이 붙는 이유다 — 20 MB 짜리가 열 개
    #: 쌓이면 "이거 누가 올린 거지" 가 첫 질문이 된다.
    created_by: str = ""
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
    #: Step against the most recent *complete* cycle before this one, in the
    #: table's basis.  Retention answers "how much is left against cycle 3";
    #: this answers "how much went this cycle", and the two are not
    #: interchangeable -- a cell can hold 92 % for forty cycles and then drop
    #: four points in one, which a retention column renders as the same small
    #: step formation makes at the start.
    discharge_delta: float | None = None
    charge_delta: float | None = None
    #: The same discharge step as a percentage of that base cycle.  None when
    #: the base is zero: the relative change from nothing is undefined, not
    #: enormous.
    discharge_delta_pct: float | None = None
    #: Which cycle the step was measured against, and how many cycle numbers
    #: back that is.  A gap means the step covers several cycles' fade -- 1 is
    #: adjacent.  Both are None/0 when there is no base yet.
    delta_base_cycle: int | None = None
    delta_span: int = 0
    #: ``discharge_delta / delta_span`` -- the honest per-cycle rate when
    #: cycles are missing from the record.
    discharge_delta_per_cycle: float | None = None
    c_rate: float | None = None
    temperature_mean: float | None = None
    duration_h: float
    n_points: int
    complete: bool


class PartialCycleOut(BaseModel):
    """A cycle that exists in the record but carries no cycle-level numbers.

    The table hides these on purpose -- a truncated cycle's capacity is
    whatever had accumulated when the file stopped, and printing it puts a
    point on the fade curve that drops for no physical reason.  Hiding the
    *row* also hid the *fact*, though, and a screen of em-dashes with no
    explanation reads as a parse failure.  This says they are there and why
    they are empty, without quoting a number.
    """

    cycle: int
    run_id: int
    #: ``truncated`` | ``no_discharge`` | ``no_charge`` | ``no_steps`` | ``""``
    #: (unknown -- written before the parser recorded a reason).
    reason: str
    has_charge: bool
    has_discharge: bool


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
    #: Cycles left out of ``cycles`` because they carry no numbers.  Always
    #: reported, whatever ``complete_only`` says -- their existence is not a
    #: number, and hiding it is what made an empty table unreadable.
    partial_cycles: list[PartialCycleOut] = []


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
    #: False when this curve comes from a cycle with no cycle-level numbers.
    #: The trace itself is measured data and worth drawing; what it must not do
    #: is sit on the plot looking like a finished cycle.
    complete: bool = True
    #: Why, when it is not complete.  Same codes as ``PartialCycleOut``.
    incomplete_reason: str = ""


class ProfileOut(BaseModel):
    basis: str
    basis_label: str
    requested_basis: str
    resolved_cell: ResolvedCellOut
    series: list[ProfileSeriesOut]
    #: True when the curves are not all in the same unit, so one axis label
    #: cannot describe them and the client has to annotate each curve.
    mixed_basis: bool = False


class DqdvSeriesOut(BaseModel):
    """One branch's dQ/dV, and what it was computed with.

    ``voltage_step`` and ``smoothing`` ride along because they change the
    curve: smoothing lowers and widens a peak, so peak *heights* only compare
    between curves built the same way (ADR 0013).

    A curve that could not be computed still comes back -- empty, with
    ``reason``.  Dropping it would leave a cycle missing from the plot with
    nothing on screen to say why.
    """

    cycle: int
    branch: str
    basis: str
    points: int
    voltage: list[float]
    #: mAh/V, or (mAh/g)/V etc. once normalised.  Negative on discharge, which
    #: is the answer and not a bug: capacity rises while voltage falls.
    dqdv: list[float]
    run_id: int
    label: str
    voltage_step: float
    smoothing: int
    #: Which filter ran, and its polynomial order when that filter is
    #: Savitzky-Golay.  Peak *heights* only compare between curves whose
    #: window, filter and order all match, so all three travel with the
    #: numbers (ADR 0015).
    smoother: str = "moving"
    poly_order: int = 2
    #: Samples excluded by the monotonic filter -- the CV hold and any
    #: noise-driven backtracking.
    points_dropped: int = 0
    reason: str = ""


class DqdvOut(BaseModel):
    basis: str
    basis_label: str
    requested_basis: str
    resolved_cell: ResolvedCellOut
    series: list[DqdvSeriesOut]
    voltage_step: float
    smoothing: int
    smoother: str = "moving"
    poly_order: int = 2
    mixed_basis: bool = False


class DvdqSeriesOut(BaseModel):
    """One branch's dV/dQ, and what it was computed with.

    The sibling of ``DqdvSeriesOut`` and deliberately its mirror image: the
    x axis is capacity, the y axis is V per capacity, and the useful reading is
    the **distance between two peaks**, which is the capacity between two stage
    boundaries (ADR 0015).

    ``capacity_step`` is the resolved grid spacing in the series' own capacity
    unit.  It is reported rather than assumed because the default step is a
    fraction of each branch's own span, so two cells do not share a grid unless
    the caller pinned one.
    """

    cycle: int
    branch: str
    basis: str
    points: int
    #: The grid, in ``basis`` units.
    capacity: list[float]
    #: V/mAh, or V/(mAh/g) etc. once normalised.  Negative on discharge --
    #: voltage falls while capacity rises, and erasing that sign would erase
    #: the hysteresis a charge/discharge overlay exists to show.
    dvdq: list[float]
    run_id: int
    label: str
    capacity_step: float
    smoothing: int
    smoother: str = "moving"
    poly_order: int = 2
    #: Samples excluded because capacity stopped advancing -- the CV hold and
    #: any rest.
    points_dropped: int = 0
    reason: str = ""


class DvdqOut(BaseModel):
    basis: str
    basis_label: str
    requested_basis: str
    resolved_cell: ResolvedCellOut
    series: list[DvdqSeriesOut]
    smoothing: int
    smoother: str = "moving"
    poly_order: int = 2
    #: The step the caller pinned, in mAh, or None when each branch used a
    #: fraction of its own span.
    capacity_step: float | None = None
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
    #: Why there is no completed cycle, when there is none.  Empty otherwise.
    #: ``no_discharge`` | ``no_charge`` | ``truncated`` | ``no_steps`` |
    #: ``no_cycles``.
    no_complete_reason: str = ""
    basis: str
    basis_label: str
    reported: dict[str, Any] | None
    reference: dict[str, Any] | None
    first_cycle: dict[str, Any] | None
    knee: dict[str, Any] | None
    resolved_cell: ResolvedCellOut


class ChangeNoteOut(BaseModel):
    """`docs/log.md` 의 한 항목.

    `action` 을 Enum 으로 좁히지 않는다 -- 파일에 있는 그대로 낸다.  목록에 없는
    action 을 거르면 그 커밋만 패치노트에서 조용히 빠지고, 화면은 그 사실을
    말할 방법이 없다.
    """

    date: str
    action: str
    subject: str
    body: str


class BasisInfo(BaseModel):
    value: str
    label: str


def basis_choices() -> list[BasisInfo]:
    from wrdkit import basis_label

    return [BasisInfo(value=b, label=basis_label(b)) for b in BASES]


DEFAULT_BASIS = Basis.ABSOLUTE
