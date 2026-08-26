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
    #: 이 그룹을 담을 상위 그룹.  None 이면 최상위 그룹이다 (ADR 0025).
    parent_id: int | None = None
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
    #: 여기만 ``null`` 이 뜻을 갖는다: "최상위로 꺼내라".  나머지 세 열은
    #: NOT NULL 이라 아래 검사기가 막는다.
    parent_id: int | None = None
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
    parent_id: int | None = None
    #: 상위 그룹 이름.  화면이 그룹 목록만 받고도 "부모 · 자식" 을 그릴 수
    #: 있도록 같이 낸다 -- 안 그러면 매 행마다 그룹을 한 번 더 물어야 한다.
    parent_name: str = ""
    subgroup_count: int = 0
    description: str
    color: str
    created_at: datetime
    updated_at: datetime
    #: 소그룹에 든 셀까지 센다.  그래야 드롭다운의 수와 그걸 골랐을 때 보이는
    #: 목록이 같다 -- 상위 그룹은 제 셀을 하나도 직접 갖지 않을 수 있다.
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
    #: 그룹이 소그룹이면 그 위 그룹의 이름.  최상위 그룹이면 빈 문자열이다.
    group_parent_name: str = ""
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
    #: 저장된 값이 아니라 **실제로 쓰이는** 기준 사이클과 그 이유 (ADR 0018).
    #: ``user`` | ``formationless`` | ``default``.  formation 이 없는 스케줄은
    #: 1번에 앵커하고, 사람이 입력한 값은 언제나 그대로다.
    reference_cycle_effective: int = 3
    reference_cycle_reason: str = "default"
    #: 스케줄이 말하는 formation 유무 -- ``yes`` | ``no`` | ``unclear``.
    formation: str = "unclear"
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
    #: 그 기준을 누가 정했나 (ADR 0018): ``user`` | ``formationless`` |
    #: ``default``.  1번에 앵커한 표를 보고 "왜 3번이 아니지" 를 묻게 두지 않는다.
    reference_cycle_reason: str = "default"
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
    #: 실제로 그린 사이클 번호들.  `cycles=all` 은 골라 뽑을 수 있으므로
    #: (아래 `cycles_note`), 무엇이 그려졌는지는 요청만 봐서는 알 수 없다.
    cycles: list[int] = []
    #: 전부를 그리지 못했을 때 무엇을 어떻게 골랐는지 한 줄.  비어 있으면
    #: 고른 것이 곧 전부다 -- 조용히 줄이지 않는다.
    cycles_note: str = ""
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
    #: 실제로 그린 사이클 번호들.  `cycles=all` 은 골라 뽑을 수 있으므로
    #: (아래 `cycles_note`), 무엇이 그려졌는지는 요청만 봐서는 알 수 없다.
    cycles: list[int] = []
    #: 전부를 그리지 못했을 때 무엇을 어떻게 골랐는지 한 줄.  비어 있으면
    #: 고른 것이 곧 전부다 -- 조용히 줄이지 않는다.
    cycles_note: str = ""
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
    #: 실제로 그린 사이클 번호들.  `cycles=all` 은 골라 뽑을 수 있으므로
    #: (아래 `cycles_note`), 무엇이 그려졌는지는 요청만 봐서는 알 수 없다.
    cycles: list[int] = []
    #: 전부를 그리지 못했을 때 무엇을 어떻게 골랐는지 한 줄.  비어 있으면
    #: 고른 것이 곧 전부다 -- 조용히 줄이지 않는다.
    cycles_note: str = ""
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
    #: 그 기준을 누가 정했나 (ADR 0018): ``user`` | ``formationless`` | ``default``.
    reference_cycle_reason: str = "default"
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


# --------------------------------------------------------------------------
# 임피던스 (ADR 0019)
# --------------------------------------------------------------------------
class SpectrumOut(BaseModel):
    #: True when the upload was the same bytes as an existing record and
    #: that record was returned -- "올렸습니다" 와 "이미 있었습니다" 는
    #: 다른 일이고, 화면이 구별해 말해야 한다 (Codex #22).
    duplicate: bool = False
    #: 무엇을 보려고 잰 측정인가 (자유 입력).
    purpose: str = ""
    #: 한 파일 안에서 몇 번째 스윕인지와 전부 몇 개인지 (ADR 0022).
    sweep_index: int = 1
    sweep_count: int = 1
    #: 그 스윕의 셀 상태 — SOC 스캔의 x축.
    potential_v: float | None = None
    capacity_mah: float | None = None
    id: int
    sample_id: int | None
    sample_name: str | None = None
    name: str
    #: "liquid" | "solid" — 같은 두 아크가 무엇으로 불릴지를 정한다.
    kind: str
    #: "sym" | "full" | "half" | "" — 무엇을 쟀나.  전해질과는 다른 질문이고,
    #: 대칭셀이 아니면 전도도를 내지 않는다.
    cell_config: str = ""
    original_name: str
    sha256: str
    size_bytes: int
    source_format: str
    uploaded_at: datetime
    n_points: int
    frequency_start_hz: float | None
    frequency_end_hz: float | None
    amplitude_mv: float | None
    device: str
    technique: str
    #: 몇 번째 사이클의 임피던스인가.  None 은 "안 적음", 0 은 "구동 전".
    at_cycle: int | None = None
    measured_at: datetime | None
    thickness_um: float | None
    area_cm2: float | None
    #: 원형 펠릿의 지름.  면적이 비어 있으면 면적이 여기서 나온다.
    diameter_mm: float | None = None
    #: 이 측정 자신의 조건 (ADR 0027).  비어 있으면 붙은 셀의 것이 `*_effective`
    #: 로 나온다 -- 적어 넣은 값이 늘 이긴다.
    group_id: int | None = None
    test_date: str = ""
    cathode_type: str = ""
    process: str = ""
    temperature_c: float | None = None
    #: 실제로 쓰이는 값 (자기 것 → 셀 것 순).  화면이 회색으로 그릴 수 있게
    #: 어디서 왔는지도 함께 낸다.
    group_id_effective: int | None = None
    group_label: str = ""
    test_date_effective: str = ""
    cathode_type_effective: str = ""
    process_effective: str = ""
    temperature_c_effective: float | None = None
    #: 위 값 중 셀에서 빌려 온 칸들의 이름.  화면이 "이건 셀에서 온 값" 이라고
    #: 적을 수 있어야 사람이 덮어쓸지 말지를 안다.
    inherited: list[str] = []
    last_circuit: str
    parse_error: str
    created_by: str = ""
    updated_by: str = ""
    updated_at: datetime
    fit_count: int = 0
    best_chi_squared: float | None = None
    best_circuit: str = ""


class SpectrumFitOut(BaseModel):
    id: int
    spectrum_id: int
    circuit: str
    #: 피팅 당시의 종류.  스펙트럼의 현재 종류(``kind_now``)와 다를 수 있고,
    #: 다르면 화면이 그렇게 말해야 한다 — 이름이 달라진다는 뜻이므로.
    kind: str
    kind_now: str = ""
    converged: bool
    chi_squared: float | None
    reason: str
    #: [{"name","value","unit","stderr","determined","relative_error"}, ...]
    parameters: list[dict[str, Any]] = []
    #: 그 저항들이 이 셀에서 무엇인지.  읽을 때 붙인다 (이름은 고정값이 아니다).
    arcs: list[dict[str, Any]] = []
    #: 맞춘 회로를 **맞추는 데 쓴 주파수 위에서** 서버가 계산한 곡선 (ADR 0019).
    #: 화면이 회로를 다시 해석하면 서버와 조용히 어긋난다 — L·Ws·Wo·중첩을 못
    #: 그리는 근사 재구성이 실제로 다른 곡선을 "맞춤" 으로 그렸다 (리뷰 #6).
    #: 회로를 못 읽으면 null 이고 ``fitted_note`` 가 이유를 말한다.
    #:
    #: 한때 저장된 **전체** 주파수 위에서 그렸다.  창을 좁혀 맞추면 그 밖은
    #: 외삽인데, 모델이 거기서 되돌아 나오며 저주파 끝에 갈고리를 만들었다 —
    #: 맞춤이 실패한 것처럼 보이지만 사실은 아무 점도 없는 곳의 그림이다.
    fitted_frequency_hz: list[float] | None = None
    fitted_z_re: list[float] | None = None
    fitted_z_im: list[float] | None = None
    fitted_note: str = ""
    #: 오차가 저주파 끝에 몰렸을 때, 거기를 빼려면 하한에 무엇을 적어야 하나.
    #: 값이 있으면 그 자체가 "몰려 있다" 는 뜻이다 (`reason` 이 같은 것을
    #: 문장으로 말한다).  읽을 때 다시 재므로 옛 피팅에도 붙는다.
    suggested_low_hz: float | None = None
    suggested_low_drops: int = 0
    #: 이 피팅이 실제로 쓸 수 있는 상한 — 유도성 점을 뺀 뒤의 최고 주파수.
    suggested_high_hz: float | None = None
    #: 전고체일 때의 전도도.  두께·면적이 없으면 무엇이 없는지 말한다.
    conductivity: dict[str, Any] = {}
    dropped_inductive: int = 0
    dropped_out_of_range: int = 0
    frequency_low_hz: float | None = None
    frequency_high_hz: float | None = None
    starts: int = 0
    starts_converged: int = 0
    created_at: datetime
    created_by: str = ""


class SpectrumDetailOut(SpectrumOut):
    settings: dict[str, Any] = {}
    #: 실제로 쓰이는 기하 — 스펙트럼 자신의 값이 없으면 셀에서 온다.
    thickness_cm: float | None = None
    area_cm2_effective: float | None = None
    fits: list[SpectrumFitOut] = []


class SpectrumPointsOut(BaseModel):
    id: int
    name: str
    kind: str
    at_cycle: int | None = None
    #: raw 만 (ADR 0001): Hz 와 Ω.  z_im 은 **허수부 자체**이고 그 음수가 아니다.
    frequency_hz: list[float]
    z_re: list[float]
    z_im: list[float]
    magnitude: list[float]
    phase_deg: list[float]


class SpectrumUpdate(BaseModel):
    """PATCH 는 이름을 댄 필드만 건드린다."""

    name: str | None = None
    kind: str | None = None
    #: 빈 문자열은 "아직 안 정함" 이다.
    cell_config: str | None = None
    at_cycle: int | None = Field(default=None, ge=0)
    sample_id: int | None = None
    thickness_um: PositiveLength | None = None
    area_cm2: PositiveLength | None = None
    #: 원형 펠릿의 지름.  면적이 비어 있을 때 면적이 여기서 나온다.
    diameter_mm: PositiveLength | None = None
    measured_at: datetime | None = None
    #: 이 측정 자신의 조건 (ADR 0027).  빈 문자열이 "안 적음" 이다.
    group_id: int | None = None
    test_date: str | None = None
    cathode_type: str | None = None
    process: str | None = None
    temperature_c: float | None = None

    #: 무엇을 보려고 잰 측정인가.  빈 문자열이 "안 적음" 이므로 clear 는 필요 없다.
    purpose: str | None = None
    #: 숫자 필드를 비우려면 이름을 여기에 담는다.
    clear: list[str] = Field(default_factory=list)


class ScanPointOut(BaseModel):
    """한 스윕과, 그 스윕에서 맞춘 값들."""

    spectrum_id: int
    sweep_index: int
    name: str
    #: SOC 축이 되는 두 값.  둘 다 없으면 이 점은 x 축에 놓을 자리가 없다.
    capacity_mah: float | None = None
    potential_v: float | None = None
    #: 가장 잘 맞은 피팅 (수렴한 것 중 χ² 최소).  없으면 나머지가 전부 비어 있다.
    fit_id: int | None = None
    circuit: str = ""
    chi_squared: float | None = None
    #: 파라미터 이름 → 값.  미결정 파라미터는 **넣지 않는다** — SOC 추세선에
    #: 못 믿을 점이 섞이면 추세 자체가 거짓이 된다 (§0.4).
    values: dict[str, float] = {}
    #: 그 저항들이 이 셀에서 무엇인지 (파라미터 이름 → 라벨).
    labels: dict[str, str] = {}


class ScanOut(BaseModel):
    """한 파일에서 나온 스윕들 — SOC 스캔 하나 (ADR 0022)."""

    sha256: str
    name: str
    original_name: str = ""
    kind: str
    cell_config: str = ""
    purpose: str = ""
    sample_id: int | None = None
    sample_name: str | None = None
    sweeps: int
    fitted: int
    #: 이 스캔에서 추세선을 그릴 수 있는 파라미터 이름들 (한 점이라도 있는 것).
    parameters: list[str] = []
    points: list[ScanPointOut] = []


class DrtPeakOut(BaseModel):
    tau_s: float
    frequency_hz: float
    gamma_ohm: float
    #: 봉우리 아래 넓이 — 그 과정이 감당하는 저항.  DRT 를 그림이 아니라 수로
    #: 만드는 것이 이것이다.
    resistance_ohm: float
    tau_low_s: float
    tau_high_s: float


class DrtOut(BaseModel):
    spectrum_id: int
    #: 이 답을 만든 벌점 가중치.  결과의 일부다 — λ 가 답을 정한다 (ADR 0005).
    regularisation: float
    derivative_order: int
    tau_s: list[float]
    gamma_ohm: list[float]
    r_inf_ohm: float
    inductance_h: float | None = None
    chi_squared: float
    residual_norm: float
    penalty_norm: float
    peaks: list[DrtPeakOut] = []
    total_polarisation_ohm: float = 0.0
    dropped_inductive: int = 0


class DrtSweepOut(BaseModel):
    spectrum_id: int
    results: list[DrtOut] = []
    #: L 곡선 모서리가 가리키는 결과의 자리.  없으면 -1 이고 이유가 붙는다.
    suggested_index: int = -1
    suggested_reason: str = ""


# --------------------------------------------------------------------------
# GITT (ADR 0020)
# --------------------------------------------------------------------------
class GittRunOut(BaseModel):
    id: int
    #: 어느 셀의 것인가.  `None` 은 "아직 안 붙였다" 이고, 그 상태로도 분석은
    #: 다 된다 -- 소속은 비교와 상호 링크를 위한 것이지 계산의 입력이 아니다.
    sample_id: int | None = None
    sample_name: str | None = None
    name: str
    original_name: str
    sha256: str
    size_bytes: int
    uploaded_at: datetime
    n_points: int
    n_pulses: int
    duration_h: float | None
    start_time: datetime | None
    molar_volume_cm3: float | None
    molar_mass_g: float | None
    active_mass_g: float | None
    #: 저울이 읽는 전극 전체와 그 안의 활물질 비율.  둘이 있으면 활물질 질량이
    #: 여기서 나온다 -- 적어 넣은 `active_mass_g` 가 늘 이긴다.
    electrode_mass_g: float | None = None
    active_wt_percent: float | None = None
    area_cm2: float | None
    #: 캘리퍼가 읽는 지름.  면적이 비어 있으면 여기서 나온다.
    diameter_mm: float | None = None
    #: 실제로 계산에 들어가는 두 값.  화면이 "지름에서: 0.7854 cm²" 처럼
    #: 적을 수 있게 계산 결과를 함께 낸다 -- 없으면 `None` 이다 (§0.4).
    active_mass_g_effective: float | None = None
    area_cm2_effective: float | None = None
    min_rest_s: float
    #: 무엇을 보려고 잰 측정인가 (자유 입력).  비어 있는 것이 정상이다.
    purpose: str = ""
    #: 이 측정 자신의 조건 (ADR 0027).  비어 있으면 붙은 셀의 것이 `*_effective`
    #: 로 나온다 -- 적어 넣은 값이 늘 이긴다.
    group_id: int | None = None
    test_date: str = ""
    cathode_type: str = ""
    process: str = ""
    temperature_c: float | None = None
    #: 실제로 쓰이는 값 (자기 것 → 셀 것 순).  화면이 회색으로 그릴 수 있게
    #: 어디서 왔는지도 함께 낸다.
    group_id_effective: int | None = None
    group_label: str = ""
    test_date_effective: str = ""
    cathode_type_effective: str = ""
    process_effective: str = ""
    temperature_c_effective: float | None = None
    #: 위 값 중 셀에서 빌려 온 칸들의 이름.  화면이 "이건 셀에서 온 값" 이라고
    #: 적을 수 있어야 사람이 덮어쓸지 말지를 안다.
    inherited: list[str] = []

    parse_error: str
    #: 펄스 수에 대한 관찰 한 줄.  비어 있으면 할 말이 없다는 뜻이다.
    pulse_note: str = ""
    created_by: str = ""
    updated_by: str = ""
    updated_at: datetime
    #: 확산계수를 내려면 아직 무엇이 필요한가.  비어 있으면 낼 수 있다.
    missing_for_diffusion: list[str] = []


class GittRunUpdate(BaseModel):
    name: str | None = None
    sample_id: int | None = None
    purpose: str | None = None
    #: 이 측정 자신의 조건 (ADR 0027).  빈 문자열이 "안 적음" 이다.
    group_id: int | None = None
    test_date: str | None = None
    cathode_type: str | None = None
    process: str | None = None
    temperature_c: float | None = None

    molar_volume_cm3: PositiveMass | None = None
    molar_mass_g: PositiveMass | None = None
    active_mass_g: PositiveMass | None = None
    electrode_mass_g: PositiveMass | None = None
    active_wt_percent: Percent | None = None
    area_cm2: PositiveLength | None = None
    diameter_mm: PositiveLength | None = None
    min_rest_s: NonNegativeMass | None = None
    clear: list[str] = Field(default_factory=list)


class PocvPointOut(BaseModel):
    capacity_mah: float
    voltage_v: float
    #: 그 휴지가 얼마나 길었나, 그리고 끝에서도 얼마나 움직이고 있었나.
    #: 짧은 휴지의 전압은 OCV 가 아니고, 얼마나 아닌지를 이 둘이 말한다.
    rest_s: float
    drift_mv: float


class RawTraceOut(BaseModel):
    """pOCV 곡선 밑에 깔리는 실제 측정 전압.  같은 x 축이다."""

    capacity_mah: list[float] = []
    voltage_v: list[float] = []


class PocvOut(BaseModel):
    gitt_id: int
    charge: list[PocvPointOut] = []
    discharge: list[PocvPointOut] = []
    #: 위 두 곡선의 원본.  점선으로 겹쳐 그리면 각 점에 **어떻게** 도달했는지
    #: (펄스의 분극과 그 뒤의 완화) 가 보인다 -- 평형 곡선이 버리는 것이다.
    charge_raw: RawTraceOut = RawTraceOut()
    discharge_raw: RawTraceOut = RawTraceOut()
    #: 휴지가 뒤따르지 않아 뺀 펄스 수.  조용히 버리면 잘린 파일과 정상 파일이
    #: 곡선에서 구분되지 않는다.
    skipped_charge: int = 0
    skipped_discharge: int = 0
    skipped_reasons: list[str] = []


class DiffusionPointOut(BaseModel):
    capacity_mah: float
    voltage_v: float
    #: cm²/s, 또는 낼 수 없으면 null 과 이유.
    d_cm2_s: float | None
    delta_es_v: float
    delta_et_v: float
    pulse_s: float
    #: √t 에 대한 직선성.  Weppner-Huggins 의 가정이 곧 이것이다.
    sqrt_t_r_squared: float
    reason: str = ""
    #: ΔE_s 가 기대는 휴지의 길이와, 그 끝에서 전압이 아직 움직인 양 (mV).
    #: D 와 같은 행에 있어야 하는 증거다 (ADR 0020, 리뷰 #17).
    rest_s: float | None = None
    drift_mv: float | None = None


class DiffusionOut(BaseModel):
    gitt_id: int
    points: list[DiffusionPointOut] = []
    #: 없는 재료 상수의 이름들.  추정한 몰부피로 계산한 D 는 그 추정의
    #: 제곱만큼 틀린다 (§0.4).
    missing: list[str] = []
    molar_volume_cm3: float | None = None
    molar_mass_g: float | None = None
    mass_g: float | None = None
    area_cm2: float | None = None
    #: 숫자가 나온 점의 수와 전체 점의 수.
    usable: int = 0
    total: int = 0


# --------------------------------------------------------------------------
# 한 셀의 측정들 — 세 섹션이 서로를 찾는 길
# --------------------------------------------------------------------------
class MeasurementOut(BaseModel):
    """한 셀에 붙어 있는 측정 하나.

    세 종류를 한 모양으로 줄인다.  상세 페이지들이 서로를 가리킬 때 필요한
    것은 "무엇이 있고, 어디로 가면 되고, 한 줄로 뭐라고 적을까" 뿐이라,
    각 종류의 전체 스키마를 세 번 실어 보낼 이유가 없다.
    """

    #: "cycling" | "eis" | "gitt".  화면이 어느 섹션으로 보낼지 정한다.
    kind: str
    id: int
    name: str
    #: 그 종류에서만 뜻이 있는 한 줄 (사이클 수 · 주파수 범위 · 펄스 수).
    detail: str = ""
    measured_at: datetime | None = None


class MeasurementsOut(BaseModel):
    """`GET /api/samples/{id}/measurements` 의 답."""

    sample_id: int
    sample_name: str
    cycling: list[MeasurementOut] = []
    eis: list[MeasurementOut] = []
    gitt: list[MeasurementOut] = []

    @property
    def total(self) -> int:
        return len(self.cycling) + len(self.eis) + len(self.gitt)


# --------------------------------------------------------------------------
# EIS 대시보드 — 셀 한 줄
# --------------------------------------------------------------------------
class EisDashboardRow(BaseModel):
    """임피던스를 가진 셀 하나.

    충방전 대시보드가 "이 셀이 지금 어디쯤인가" 를 한 줄로 말하듯, 이쪽은
    "이 셀의 임피던스가 몇 개 있고, 맞췄고, 저항이 얼마인가" 를 한 줄로 말한다.
    """

    sample_id: int | None = None
    sample_name: str = ""
    #: 이 줄이 무엇에서 온 것인가 -- 붙은 줄은 가장 최근 스펙트럼의 원래 이름,
    #: 안 붙은 줄은 그 파일 자신의 이름이다.  파일 이름에 조건이 적혀 있는
    #: 일이 많아서, 셀 이름만으로는 어느 측정인지 모른다.
    name: str = ""
    #: 그 이름이 가리키는 스펙트럼.  이름을 눌러 바로 갈 수 있게, 그리고 안 붙은
    #: 줄을 그 자리에서 지울 수 있게 함께 낸다.
    spectrum_id: int | None = None
    #: 셀에 붙어 있는가.  안 붙은 것도 줄로 나온다 -- 배너로만 세면 "하나
    #: 있습니다" 만 알고 그게 무엇인지는 다른 화면에 가야 안다.
    attached: bool = True
    #: 소속 그룹.  id 는 화면이 그룹·소그룹으로 거를 수 있게, 이름 둘은 그걸
    #: 다시 물어보지 않고 "부모 · 자식" 으로 적을 수 있게 함께 낸다.
    group_id: int | None = None
    group_name: str = ""
    group_parent_name: str = ""
    owner: str = ""
    #: "liquid" | "solid" | "" (한 셀에 둘이 섞여 있으면 빈 문자열)
    kind: str = ""
    cell_config: str = ""
    #: 스펙트럼 몇 개, 그중 스윕이 여럿인 **파일**(SOC 스캔)이 몇 개.
    spectra: int = 0
    scans: int = 0
    fitted: int = 0
    #: 이 셀에 적힌 목적들 — 자유 입력이라 목록이 아니라 모아 보여 준다.
    purposes: list[str] = []
    #: 가장 최근 스펙트럼의 가장 잘 맞은 피팅에서.  없으면 전부 `None` 이다:
    #: 안 맞췄다는 것과 저항이 0 이라는 것은 다른 말이다 (§0.4).
    last_circuit: str = ""
    last_at_cycle: int | None = None
    series_resistance_ohm: float | None = None
    total_resistance_ohm: float | None = None
    measured_at: datetime | None = None


class EisDashboardOut(BaseModel):
    rows: list[EisDashboardRow] = []
    #: 셀에 안 붙은 스펙트럼의 수.  0 이면 안 보여 준다 -- 붙이는 것은 일이고,
    #: 그 일이 남아 있다는 사실은 여기서만 보인다.
    unattached: int = 0


# --------------------------------------------------------------------------
# GITT 대시보드 — 셀 한 줄
# --------------------------------------------------------------------------
class GittDashboardRow(BaseModel):
    """GITT 를 가진 셀 하나.

    확산계수가 이 섹션의 답이므로 한 줄의 요점도 그것이다: 낼 수 있는가,
    낼 수 없다면 무엇이 없어서인가.
    """

    sample_id: int | None = None
    sample_name: str = ""
    #: EIS 대시보드와 같은 셋 -- 안 붙은 기록도 이름으로 한 줄 나오고,
    #: 그 이름은 기록으로 가는 길이자 지울 대상이다.
    name: str = ""
    gitt_id: int | None = None
    attached: bool = True
    #: EIS 대시보드와 같은 셋 -- 화면이 그룹·소그룹으로 거를 수 있게.
    group_id: int | None = None
    group_name: str = ""
    group_parent_name: str = ""
    owner: str = ""
    #: 이 셀의 GITT 기록들에 적힌 목적들 (자유 입력).
    purposes: list[str] = []
    records: int = 0
    pulses: int = 0
    #: D 를 낼 수 있는 기록의 수.  재료 상수가 없으면 못 낸다 (ADR 0020).
    ready: int = 0
    #: 아직 없는 재료 상수의 이름들 -- 이 셀에서 다음에 할 일이 곧 이것이다.
    missing: list[str] = []
    #: 낼 수 있는 기록들의 D 중 최소·최대 (cm²/s).  하나뿐이면 둘이 같다.
    #: 평균을 내지 않는 이유는 D 가 SOC 를 따라 자릿수로 움직이기 때문이다 --
    #: 한 숫자로 줄이면 그 숫자가 아무 SOC 도 뜻하지 않는다.
    diffusion_low: float | None = None
    diffusion_high: float | None = None
    measured_at: datetime | None = None


class GittDashboardOut(BaseModel):
    rows: list[GittDashboardRow] = []
    unattached: int = 0
