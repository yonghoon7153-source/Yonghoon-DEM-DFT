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
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class ExperimentGroup(SQLModel, table=True):
    """A set of cells meant to be compared -- one experiment, one series."""

    __tablename__ = "experiment_group"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = ""
    #: Plot colour hint for the web UI; not interpreted by the backend.
    color: str = ""
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

    samples: List["Sample"] = Relationship(back_populates="group")


class Sample(SQLModel, table=True):
    """One cell: what it is made of, and how it should be normalised."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    group_id: Optional[int] = Field(default=None, foreign_key="experiment_group.id",
                                    index=True)

    # -- what was tested ---------------------------------------------------
    test_date: Optional[str] = Field(default=None, index=True)  # YYYY-MM-DD
    cathode_type: str = Field(default="", index=True)   # "High-Ni", "Mid-Ni", ...
    cathode_detail: str = ""                            # "NCM811", "NCM622", ...
    anode: str = ""
    electrolyte: str = ""
    process: str = Field(default="", index=True)        # "dry", "wet", ...
    notes: str = ""

    # -- cell spec: the inputs that turn mAh into mAh/g and mAh/cm2 --------
    total_mass_mg: Optional[float] = None
    current_collector_mass_mg: Optional[float] = None
    active_wt_percent: Optional[float] = None
    active_mass_mg: Optional[float] = None
    area_cm2: Optional[float] = None
    diameter_mm: Optional[float] = None
    thickness_um: Optional[float] = None
    nominal_specific_capacity_mah_g: Optional[float] = None

    # -- test conditions; parsed from the schedule unless overridden -------
    temperature_c: Optional[float] = Field(default=None, index=True)
    pressure_mpa: Optional[float] = None
    cutoff_upper_v: Optional[float] = None
    cutoff_lower_v: Optional[float] = None
    c_rate: Optional[float] = Field(default=None, index=True)
    c_rate_formation: Optional[float] = None

    # -- analysis settings -------------------------------------------------
    #: Cycle used for retention and "initial" CE.  3 by default: cycles 1-2
    #: are formation and lose capacity by design (ADR 0004).
    reference_cycle: int = 3
    #: "auto" lets the evidence decide; "running"/"finished" pin it.
    declared_state: str = "auto"

    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

    group: Optional[ExperimentGroup] = Relationship(back_populates="samples")
    runs: List["Run"] = Relationship(
        back_populates="sample",
        sa_relationship_kwargs={"order_by": "Run.start_time"},
    )


class Run(SQLModel, table=True):
    """One uploaded ``.wrd`` file and what parsing it produced."""

    id: Optional[int] = Field(default=None, primary_key=True)
    sample_id: Optional[int] = Field(default=None, foreign_key="sample.id", index=True)

    original_name: str
    sha256: str = Field(index=True, unique=True)
    size_bytes: int = 0
    uploaded_at: datetime = Field(default_factory=_now)

    # -- parsed metadata ---------------------------------------------------
    device_model: str = ""
    serial_no: str = ""
    channel: Optional[int] = None
    app_version: str = ""
    firmware_version: str = ""
    start_time: Optional[datetime] = Field(default=None, index=True)
    end_time: Optional[datetime] = None
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
    parsed_at: Optional[datetime] = None

    sample: Optional[Sample] = Relationship(back_populates="runs")
    cycles: List["CycleRecord"] = Relationship(
        back_populates="run",
        sa_relationship_kwargs={"cascade": "all, delete-orphan",
                                "order_by": "CycleRecord.cycle_index"},
    )


class CycleRecord(SQLModel, table=True):
    """Per-cycle summary in raw units.  Never normalised (ADR 0001)."""

    __tablename__ = "cycle_record"

    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: int = Field(foreign_key="run.id", index=True)

    cycle_index: int = Field(index=True)   # as recorded in the file, 0-based
    cycle_number: int = Field(index=True)  # 1-based, offset applied

    charge_capacity_mah: float = 0.0
    discharge_capacity_mah: float = 0.0
    charge_energy_wh: float = 0.0
    discharge_energy_wh: float = 0.0
    coulombic_efficiency: Optional[float] = None
    energy_efficiency: Optional[float] = None
    mean_charge_voltage: Optional[float] = None
    mean_discharge_voltage: Optional[float] = None
    voltage_max: Optional[float] = None
    voltage_min: Optional[float] = None
    max_charge_current_a: Optional[float] = None
    max_discharge_current_a: Optional[float] = None
    temperature_mean: Optional[float] = None
    start_time_s: float = 0.0
    duration_s: float = 0.0
    n_points: int = 0
    complete: bool = True

    # Row slice into the cached npz, so a profile request need not rescan.
    row_start: int = 0
    row_stop: int = 0

    run: Optional[Run] = Relationship(back_populates="cycles")
