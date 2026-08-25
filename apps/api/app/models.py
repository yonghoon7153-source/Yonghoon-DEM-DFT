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
    #: Content hash of the original.  Duplicate uploads are the same row.
    sha256: str = Field(default="", index=True, unique=True)
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
