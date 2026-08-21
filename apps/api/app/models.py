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
    #: are formation and lose capacity by design (ADR 0004).
    reference_cycle: int = 3
    #: "auto" lets the evidence decide; "running"/"finished" pin it.
    declared_state: str = "auto"

    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

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
