"""Database tables.

Only *raw* electrochemistry is stored: mAh, Wh, V, A, s.  Specific and areal
capacities are derived at query time from the sample's cell spec, so
correcting a mass never requires touching a stored number (ADR 0001).
"""

# NOTE: no ``from __future__ import annotations`` here.  SQLModel resolves
# relationship targets from the annotations at class-creation time, and
# stringified builtin generics (``list['Sample']``) are not resolvable by
# SQLAlchemy's registry.  Keep the typing imports explicit instead.

from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class ExperimentGroup(SQLModel, table=True):
    """A set of cells meant to be compared -- one experiment, one series."""

    __tablename__ = "experiment_group"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = ""
    #: Plot colour hint for the web UI; not interpreted by the backend.
    color: str = ""
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    #: 누가 만들었고 누가 마지막으로 고쳤는지.  빈 문자열은 "이름을 대지 않은
    #: 사람" 이고, 이 기능이 생기기 전에 저장된 행도 그렇다 — 둘을 구분하지
    #: 않는다.  검증되지 않은 이름이므로 신원이 아니라 기록이다 (ADR 0012).
    created_by: str = ""
    updated_by: str = ""

    samples: list["Sample"] = Relationship(back_populates="group")


class Sample(SQLModel, table=True):
    """One cell: what it is made of, and how it should be normalised."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    group_id: int | None = Field(default=None, foreign_key="experiment_group.id",
                                    index=True)

    # -- what was tested ---------------------------------------------------
    test_date: str | None = Field(default=None, index=True)  # YYYY-MM-DD
    cathode_type: str = Field(default="", index=True)   # "High-Ni", "Mid-Ni", ...
    cathode_detail: str = ""                            # "NCM811", "NCM622", ...
    anode: str = ""
    electrolyte: str = ""
    process: str = Field(default="", index=True)        # "dry", "wet", ...
    notes: str = ""

    # -- cell spec: the inputs that turn mAh into mAh/g and mAh/cm2 --------
    #: The blend, as JSON: [{"name", "wt_percent", "role"}, ...].  Components
    #: recorded at 0 wt% are kept -- "this batch had no PTFE" is a deliberate
    #: record, not a blank.  Drives `active_wt_percent` unless that was typed.
    composition_json: str = ""
    total_mass_mg: float | None = None
    current_collector_mass_mg: float | None = None
    active_wt_percent: float | None = None
    active_mass_mg: float | None = None
    area_cm2: float | None = None
    diameter_mm: float | None = None
    thickness_um: float | None = None
    nominal_specific_capacity_mah_g: float | None = None
    #: 계측기가 무엇을 기준으로 전압을 기록했는지.  raw 는 그대로 두고
    #: 조회할 때 vs Li/Li+ 로 환산한다 (ADR 0001 과 같은 원칙).
    reference_electrode: str = ""
    reference_offset_v: float | None = None

    # -- test conditions; parsed from the schedule unless overridden -------
    temperature_c: float | None = Field(default=None, index=True)
    pressure_mpa: float | None = None
    cutoff_upper_v: float | None = None
    cutoff_lower_v: float | None = None
    c_rate: float | None = Field(default=None, index=True)
    c_rate_formation: float | None = None

    # -- analysis settings -------------------------------------------------
    #: Cycle used for retention and "initial" CE.  3 by default: cycles 1-2
    #: are formation and lose capacity by design (ADR 0004).  A schedule with
    #: no formation at all moves the anchor to cycle 1 -- resolved on read, not
    #: written here, so correcting a schedule never needs a re-upload (ADR 0018).
    reference_cycle: int = 3
    #: Who put that number there: "user" when a person typed it, "" when the
    #: row predates this column.  Without it a stored 3 cannot be told apart
    #: from the default, and the schedule would overwrite a typed 3 forever.
    reference_cycle_source: str = ""
    #: "auto" lets the evidence decide; "running"/"finished" pin it.
    declared_state: str = "auto"

    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    #: 누가 만들었고 누가 마지막으로 고쳤는지.  빈 문자열은 "이름을 대지 않은
    #: 사람" 이고, 이 기능이 생기기 전에 저장된 행도 그렇다 — 둘을 구분하지
    #: 않는다.  검증되지 않은 이름이므로 신원이 아니라 기록이다 (ADR 0012).
    created_by: str = ""
    updated_by: str = ""

    group: ExperimentGroup | None = Relationship(back_populates="samples")
    runs: list["Run"] = Relationship(
        back_populates="sample",
        sa_relationship_kwargs={"order_by": "Run.start_time"},
    )


class Run(SQLModel, table=True):
    """One uploaded ``.wrd`` file and what parsing it produced."""

    id: int | None = Field(default=None, primary_key=True)
    sample_id: int | None = Field(default=None, foreign_key="sample.id", index=True)

    original_name: str
    sha256: str = Field(index=True, unique=True)
    size_bytes: int = 0
    uploaded_at: datetime = Field(default_factory=_now)
    #: 누가 올렸는지.  파일은 불변이므로 고친 사람은 없다 (CLAUDE.md §0.2).
    created_by: str = ""
    updated_by: str = ""

    # -- parsed metadata ---------------------------------------------------
    device_model: str = ""
    serial_no: str = ""
    channel: int | None = None
    app_version: str = ""
    firmware_version: str = ""
    start_time: datetime | None = Field(default=None, index=True)
    end_time: datetime | None = None
    row_count: int = 0
    cycle_count: int = 0
    complete_cycle_count: int = 0
    data_format: int = 0
    unit_coulomb: bool = False
    instrument_path: str = ""
    schedule_path: str = ""
    #: Decoded schedule, stored as JSON so the UI can show the protocol.
    schedule_json: str = ""

    #: Added to this file's cycle numbers so a run split across several files
    #: reads as one continuous experiment.
    cycle_offset: int = 0
    cycle_offset_source: str = "auto"  # auto | manual

    parse_error: str = ""
    parsed_at: datetime | None = None

    sample: Sample | None = Relationship(back_populates="runs")
    cycles: list["CycleRecord"] = Relationship(
        back_populates="run",
        sa_relationship_kwargs={"cascade": "all, delete-orphan",
                                "order_by": "CycleRecord.cycle_index"},
    )


class CycleRecord(SQLModel, table=True):
    """Per-cycle summary in raw units.  Never normalised (ADR 0001)."""

    __tablename__ = "cycle_record"

    id: int | None = Field(default=None, primary_key=True)
    run_id: int = Field(foreign_key="run.id", index=True)

    cycle_index: int = Field(index=True)   # as recorded in the file, 0-based
    cycle_number: int = Field(index=True)  # 1-based, offset applied

    charge_capacity_mah: float = 0.0
    discharge_capacity_mah: float = 0.0
    charge_energy_wh: float = 0.0
    discharge_energy_wh: float = 0.0
    coulombic_efficiency: float | None = None
    energy_efficiency: float | None = None
    mean_charge_voltage: float | None = None
    mean_discharge_voltage: float | None = None
    voltage_max: float | None = None
    voltage_min: float | None = None
    max_charge_current_a: float | None = None
    max_discharge_current_a: float | None = None
    temperature_mean: float | None = None
    start_time_s: float = 0.0
    duration_s: float = 0.0
    n_points: int = 0
    complete: bool = True
    #: Why this cycle carries no cycle-level numbers, when it carries none.
    #: ``truncated`` | ``no_discharge`` | ``no_charge`` | ``no_steps``; empty
    #: for a complete cycle.
    #:
    #: Stored rather than derived because the two causes cannot be told apart
    #: after the fact.  A running cell cut off during its charge and a
    #: charge-only protocol both end up "has charge, no discharge" -- but one
    #: will have a discharge in an hour and the other never will, and only the
    #: parser (which can see whether the file stops mid-step) knows which.
    #: Rows written before this column existed hold "" and are read as unknown.
    incomplete_reason: str = ""

    #: 이 사이클에 그 방향의 **스텝**이 있었는가.
    #:
    #: 전류 최댓값으로 판정하면 -2e-12 A 짜리 잡음 한 점이 "방전이 있었다" 가
    #: 된다.  그러면 같은 응답 안에서 incomplete_reason 은 ``no_discharge`` 인데
    #: ``has_discharge`` 는 참인 모순이 나온다 -- 화면이 둘 중 무엇을 믿어도
    #: 한쪽은 거짓말이다.  브랜치의 존재는 스텝(CELL STATUS)이 정한다.
    #:
    #: 이 열이 생기기 전 행은 NULL 이고, 그때는 예전처럼 전류로 읽는다.
    has_charge_step: bool | None = None
    has_discharge_step: bool | None = None

    # Row slice into the cached npz, so a profile request need not rescan.
    row_start: int = 0
    row_stop: int = 0

    run: Run | None = Relationship(back_populates="cycles")


class CompositionPreset(SQLModel, table=True):
    """A build saved by name: its blend, and the cell settings that go with it.

    Applying one fills in several fields at once, which is the point -- cells
    from the same recipe share a punch diameter, a nominal specific capacity
    and a counter electrode -- and also the risk.  Two rules keep it honest
    (ADR 0010):

    *No masses.*  ``total_mass_mg`` and ``active_mass_mg`` are measured per
    cell.  Carried in a preset they would put one cell's mass under another
    cell's mAh/g with nothing on screen to say so.

    *The blend is stored as components, not as ``AM:SE:VGCF = 80:17:3``.*
    Re-parsing the shorthand re-runs role inference, and a role corrected by
    hand -- the value that decides what enters the mAh/g denominator -- would
    be quietly guessed again (ADR 0007).
    """

    __tablename__ = "composition_preset"

    id: int | None = Field(default=None, primary_key=True)
    #: Unique: saving over a name is a deliberate act, not a side effect.
    name: str = Field(index=True, unique=True)
    #: [{"name", "wt_percent", "role"}, ...], same shape as Sample.composition_json.
    components_json: str = ""
    #: Only the spec fields that had a value when the preset was saved.  A
    #: field the preset does not carry is one it must not touch on apply --
    #: absent is "I do not know", not "clear it".
    settings_json: str = ""
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    #: 누가 만들었고 누가 마지막으로 고쳤는지.  빈 문자열은 "이름을 대지 않은
    #: 사람" 이고, 이 기능이 생기기 전에 저장된 행도 그렇다 — 둘을 구분하지
    #: 않는다.  검증되지 않은 이름이므로 신원이 아니라 기록이다 (ADR 0012).
    created_by: str = ""
    updated_by: str = ""


class Activity(SQLModel, table=True):
    """무엇이 언제 누구에 의해 바뀌었는지 — 한 줄에 하나.

    Written by a flush listener rather than by the routes (see ``db.py``), so
    a new endpoint is recorded from the moment it exists.  A log somebody has
    to remember to append to is a log with exactly one kind of edit missing,
    and that gap is invisible: the feed looks complete.

    Only the things people talk about are logged -- cells, groups, presets,
    files.  A cycle row is not an edit anybody made; ten thousand of them
    arrive from one upload, and the upload is the event.
    """

    __tablename__ = "activity"

    id: int | None = Field(default=None, primary_key=True)
    at: datetime = Field(default_factory=_now, index=True)
    #: Unverified display name; "" when nobody said who they were.
    actor: str = Field(default="", index=True)
    action: str = ""            # create | update | delete
    entity: str = Field(default="", index=True)   # sample | group | preset | run
    entity_id: int | None = None
    #: What it was called at the time.  Kept rather than joined: the feed has
    #: to keep reading after the thing is deleted, and that is exactly when
    #: somebody is looking for it.
    label: str = ""
    #: Which fields changed, comma separated.  Empty on create and delete.
    fields: str = ""


class SpectrumRecord(SQLModel, table=True):
    """One impedance measurement: the file it came from and what it says.

    Attached to a ``Sample`` like a cycling run is, because it is the same cell
    -- the library filters, the group, the owner and the name all come along
    (ADR 0019).  It can also stand alone: a pellet measured before anybody
    decided it was a cell still needs somewhere to live.

    ``kind`` decides what the fitted arcs are **called**, not how they are
    found.  ``liquid`` reads them as an SEI film and a charge transfer;
    ``solid`` reads the same two arcs as a grain interior and a grain
    boundary, and offers conductivity instead of resistance.
    """

    __tablename__ = "spectrum"
    __table_args__ = (UniqueConstraint("sha256", "sweep_index",
                                      name="uq_spectrum_sha_sweep"),)

    id: int | None = Field(default=None, primary_key=True)
    sample_id: int | None = Field(default=None, foreign_key="sample.id", index=True)
    name: str = Field(default="", index=True)
    #: "liquid" | "solid".  Not inferred from the data: the two look alike and
    #: only the person who built the cell knows which it was (§0.4).
    kind: str = Field(default="liquid", index=True)
    #: "sym" | "full" | "half" | "" (모름).  Which cell was measured, which is
    #: a different question from what the electrolyte was -- and it changes
    #: what the arcs mean.  A solid **symmetric** cell with ion-blocking
    #: electrodes shows grain interior and grain boundary; a solid **full**
    #: cell shows those plus the electrode interfaces, and calling the second
    #: arc "grain boundary" there is simply wrong.  The file name usually says
    #: (`..._70um_sym_01`), but a name is a hint, not a record -- so it is
    #: shown beside the field and the person chooses (ADR 0019).
    cell_config: str = Field(default="", index=True)

    original_name: str = ""
    #: Content hash of the original.  **Not** unique on its own any more: one
    #: SOC-scan file holds twenty sweeps and they all came from these bytes
    #: (ADR 0022).  The pair with ``sweep_index`` is what identifies a row, so
    #: re-uploading the same file is still a duplicate rather than a copy.
    sha256: str = Field(default="", index=True)
    size_bytes: int = 0
    #: "mpr" | "mpt".  Which reader made the points, so a re-parse is not a guess.
    source_format: str = ""
    uploaded_at: datetime = Field(default_factory=_now)

    n_points: int = 0
    frequency_start_hz: float | None = None
    frequency_end_hz: float | None = None
    #: What the .mps said, when a .mps came with it.
    amplitude_mv: float | None = None
    device: str = ""
    technique: str = ""
    #: Which cycle of the cell's cycling this spectrum belongs to.
    #:
    #: The lab's solid-state work measures impedance twice -- before cycling and
    #: after a couple of hundred cycles -- and the whole point is comparing the
    #: two.  Without a number they sort by upload time, which is the order
    #: somebody happened to drag files in.  ``None`` is "not said"; ``0`` is a
    #: real answer meaning before any cycling.
    at_cycle: int | None = Field(default=None, index=True)
    #: When the instrument measured it, if the file says.
    measured_at: datetime | None = None
    #: Everything else the settings file carried, verbatim.
    settings_json: str = ""
    #: 무엇을 보려고 잰 측정인가 — "SOC별", "200 사이클", "온도별".  자유
    #: 입력이다: 랩이 새 목적을 계속 만들고, 목록을 고정하면 그때마다 코드를
    #: 고쳐야 한다.  SOC 스캔처럼 파일이 스스로 말하는 경우에는 채워 준다
    #: (§0.3 — 계측기가 아는 것을 사람에게 다시 묻지 않는다).
    purpose: str = Field(default="", index=True)
    #: 한 `.mpr` 이 스윕 여럿을 담을 때 몇 번째인가, 그리고 전부 몇 개인가
    #: (ADR 0022).  같은 원본 sha 를 공유하므로 이 번호가 행을 가른다.
    sweep_index: int = 1
    sweep_count: int = 1
    #: 그 스윕을 찍은 셀 상태.  SOC 스캔의 x축이라 스펙트럼과 함께 산다.
    potential_v: float | None = None
    capacity_mah: float | None = None
    #: 올라온 `.mps` 원문의 내용 해시와 원래 이름.  파서가 이해한 부분집합
    #: (settings_json)과 별개로 원문 바이트를 보존한다 (§0.2 정신, 리뷰 #21) —
    #: 파서가 모르는 설정 줄은 여기서만 되찾을 수 있다.
    settings_sha256: str = ""
    settings_name: str = ""

    #: Cell geometry for conductivity.  Kept on the spectrum rather than only
    #: on the sample because a pellet gets measured at several thicknesses and
    #: each spectrum belongs to one of them.  Blank means "take the sample's".
    thickness_um: float | None = None
    area_cm2: float | None = None

    #: The circuit last fitted here, so the screen can re-offer it.
    last_circuit: str = ""
    parse_error: str = ""

    created_by: str = ""
    updated_by: str = ""
    updated_at: datetime = Field(default_factory=_now)


class SpectrumFit(SQLModel, table=True):
    """One fit of one circuit to one spectrum.

    Kept rather than recomputed: a fit is not deterministic in the way a
    parse is -- it starts from scattered points and keeps the best -- so a
    number quoted in a report has to be the number that was quoted, not one
    that will be re-derived slightly differently next week.
    """

    __tablename__ = "spectrum_fit"

    id: int | None = Field(default=None, primary_key=True)
    spectrum_id: int = Field(foreign_key="spectrum.id", index=True)
    circuit: str = ""
    #: Copied from the spectrum at fit time.  A spectrum re-labelled later must
    #: not silently rename the arcs of a fit already reported.
    kind: str = "liquid"

    converged: bool = True
    chi_squared: float | None = None
    reason: str = ""
    #: [{"name", "value", "unit", "stderr", "determined"}, ...]
    parameters_json: str = ""

    dropped_inductive: int = 0
    dropped_out_of_range: int = 0
    frequency_low_hz: float | None = None
    frequency_high_hz: float | None = None
    starts: int = 0
    starts_converged: int = 0

    created_at: datetime = Field(default_factory=_now)
    created_by: str = ""


class GittRun(SQLModel, table=True):
    """One GITT record: a ``.wrd`` full of pulses and rests.

    A table of its own rather than a flag on ``Run`` (ADR 0020).  A GITT file
    *is* a ``.wrd``, but summarising it the cycling way produces hundreds of
    "cycles" whose capacities and efficiencies all mean nothing, and they would
    sit in the library next to real ones with no way to tell them apart.
    Cycling and GITT also do not meet in practice -- impedance gets measured
    part-way through a cycling run, GITT almost never does.

    The material constants live here because they belong to *this* measurement:
    the same powder measured in two cells has two interfacial areas, and the
    diffusion coefficient is proportional to the square of that.
    """

    __tablename__ = "gitt_run"

    id: int | None = Field(default=None, primary_key=True)
    #: 어느 셀의 GITT 인가.  `Run`·`SpectrumRecord` 와 같은 자리를 가리키므로,
    #: 이것이 붙는 순간 한 셀의 충방전·임피던스·GITT 가 서로를 찾을 수 있다.
    #:
    #: `None` 이 정상 상태다 -- 셀을 만들기 전에 파일부터 올리는 일이 흔하고
    #: (GITT 는 특히), 없는 소속을 지어내는 것보다 비워 두는 편이 맞다 (§0.4).
    sample_id: int | None = Field(default=None, foreign_key="sample.id", index=True)
    name: str = Field(default="", index=True)
    original_name: str = ""
    #: Content hash of the ``.wrd``.  Duplicate uploads are the same row.
    sha256: str = Field(default="", index=True, unique=True)
    size_bytes: int = 0
    uploaded_at: datetime = Field(default_factory=_now)

    n_points: int = 0
    n_pulses: int = 0
    duration_h: float | None = None
    start_time: datetime | None = None

    # -- what the file cannot say (ADR 0020) -------------------------------
    #: cm³/mol of the active material.
    molar_volume_cm3: float | None = None
    #: g/mol of the active material.
    molar_mass_g: float | None = None
    #: g of active material in this electrode.
    active_mass_g: float | None = None
    #: cm², the electrode/electrolyte interfacial area.
    area_cm2: float | None = None
    #: Rests shorter than this are not treated as equilibrium.  0 = keep all,
    #: and report the drift per point instead.
    min_rest_s: float = 0.0

    parse_error: str = ""
    #: 펄스 수에 대한 한 줄, 올릴 때 적어 둔다.  판정이 아니라 관찰이다 --
    #: `.wrd` 에 사이클링과 GITT 를 가르는 표식은 없다.
    pulse_note: str = ""
    created_by: str = ""
    updated_by: str = ""
    updated_at: datetime = Field(default_factory=_now)
