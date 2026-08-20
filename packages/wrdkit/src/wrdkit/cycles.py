"""Segment a ``.wrd`` record into steps and cycles, and pull out profiles.

The cycler already stamps every sample with a step and a cycle index, so
segmentation is a matter of finding the runs of equal index rather than
re-deriving boundaries from the current sign.  That keeps this module honest
about what the instrument actually did -- including partial cycles at the end
of a file, which are common because long runs are split across files.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .wrd import CellStatus, WrdFile

__all__ = [
    "StepSegment", "CycleSummary", "Profile", "segment_steps",
    "summarize_cycles", "extract_profile", "SECONDS_PER_HOUR",
]

SECONDS_PER_HOUR = 3600.0


@dataclass
class StepSegment:
    """One contiguous run of samples belonging to a single schedule step."""

    total_step: int
    step_index: int
    cycle_index: int
    mode: str
    start: int
    stop: int  # exclusive
    duration_s: float
    capacity_mah: float
    energy_wh: float
    current_mean_a: float
    voltage_start: float
    voltage_end: float
    voltage_min: float
    voltage_max: float

    @property
    def n_points(self) -> int:
        return self.stop - self.start


@dataclass
class CycleSummary:
    """Per-cycle electrochemistry, in raw instrument units (mAh / Wh)."""

    cycle_index: int          # as recorded in the file (0-based)
    cycle_number: int         # 1-based, shifted by the run's cycle offset
    start: int
    stop: int
    charge_capacity_mah: float = 0.0
    discharge_capacity_mah: float = 0.0
    charge_energy_wh: float = 0.0
    discharge_energy_wh: float = 0.0
    mean_charge_voltage: float | None = None
    mean_discharge_voltage: float | None = None
    voltage_max: float | None = None
    voltage_min: float | None = None
    start_time_s: float = 0.0
    duration_s: float = 0.0
    max_charge_current_a: float | None = None
    max_discharge_current_a: float | None = None
    temperature_mean: float | None = None
    complete: bool = True
    steps: list[StepSegment] = field(default_factory=list)

    @property
    def n_points(self) -> int:
        return self.stop - self.start

    @property
    def coulombic_efficiency(self) -> float | None:
        """Discharge / charge capacity, in percent."""
        if not self.charge_capacity_mah:
            return None
        return 100.0 * self.discharge_capacity_mah / self.charge_capacity_mah

    @property
    def energy_efficiency(self) -> float | None:
        if not self.charge_energy_wh:
            return None
        return 100.0 * self.discharge_energy_wh / self.charge_energy_wh

    @property
    def voltage_hysteresis(self) -> float | None:
        """Mean charge minus mean discharge voltage -- a polarisation proxy."""
        if self.mean_charge_voltage is None or self.mean_discharge_voltage is None:
            return None
        return self.mean_charge_voltage - self.mean_discharge_voltage


@dataclass
class Profile:
    """One charge or discharge branch, ready to plot."""

    cycle_number: int
    branch: str  # "charge" | "discharge"
    capacity_mah: np.ndarray
    voltage: np.ndarray
    time_s: np.ndarray
    current_a: np.ndarray

    def __len__(self) -> int:
        return len(self.voltage)


def _runs(values: np.ndarray) -> list[tuple[int, int]]:
    """Index ranges over which *values* stays constant."""
    if len(values) == 0:
        return []
    changes = np.flatnonzero(values[1:] != values[:-1]) + 1
    bounds = np.concatenate(([0], changes, [len(values)]))
    return [(int(a), int(b)) for a, b in zip(bounds[:-1], bounds[1:], strict=True)]


def _mode_of(cell_status: np.ndarray, current: np.ndarray) -> str:
    """Classify a step as rest / charge / discharge.

    ``CELL STATUS`` is authoritative -- it agrees with the current sign on
    every sample of the reference file -- but fall back to the current when a
    step carries an unfamiliar status code.
    """
    if len(cell_status):
        status = int(np.bincount(cell_status.astype(np.int64)).argmax())
        name = CellStatus.name(status)
        if name in ("rest", "charge", "discharge"):
            return name
    mean = float(np.mean(current)) if len(current) else 0.0
    if mean > 1e-9:
        return "charge"
    if mean < -1e-9:
        return "discharge"
    return "rest"


def segment_steps(wrd: WrdFile) -> list[StepSegment]:
    """Split the record into schedule steps using the instrument's counter."""
    if not len(wrd):
        return []
    data = wrd.data
    total_step = data["total_step"]
    seconds = wrd.seconds("test_time")
    voltage = data["voltage"]
    current = data["current"]
    charge = wrd.charge_mah()
    discharge = wrd.discharge_mah()
    charge_e = wrd.energy_wh("charge_e")
    discharge_e = wrd.energy_wh("discharge_e")
    cell_status = data["cell_status"]
    step_index = data["step_index"]
    cycle_index = data["cycle_index"]

    segments: list[StepSegment] = []
    for start, stop in _runs(total_step):
        mode = _mode_of(cell_status[start:stop], current[start:stop])
        if mode == "charge":
            capacity = float(charge[stop - 1] - charge[start])
            energy = float(charge_e[stop - 1] - charge_e[start])
        elif mode == "discharge":
            capacity = float(discharge[stop - 1] - discharge[start])
            energy = float(discharge_e[stop - 1] - discharge_e[start])
        else:
            capacity = energy = 0.0
        window = voltage[start:stop]
        segments.append(StepSegment(
            total_step=int(total_step[start]),
            step_index=int(step_index[start]),
            cycle_index=int(cycle_index[start]),
            mode=mode,
            start=start,
            stop=stop,
            duration_s=float(seconds[stop - 1] - seconds[start]),
            capacity_mah=max(capacity, 0.0),
            energy_wh=max(energy, 0.0),
            current_mean_a=float(np.mean(current[start:stop])),
            voltage_start=float(window[0]),
            voltage_end=float(window[-1]),
            voltage_min=float(window.min()),
            voltage_max=float(window.max()),
        ))
    return segments


def summarize_cycles(wrd: WrdFile, *, cycle_offset: int = 0,
                     steps: list[StepSegment] | None = None) -> list[CycleSummary]:
    """Roll the record up into one :class:`CycleSummary` per cycle.

    ``cycle_offset`` shifts the reported cycle numbers, which is how a long
    experiment split over several files (``..._011.wrd``, ``..._012.wrd``)
    gets a single continuous numbering.
    """
    if not len(wrd):
        return []
    steps = segment_steps(wrd) if steps is None else steps
    data = wrd.data
    seconds = wrd.seconds("test_time")
    voltage = data["voltage"]
    current = data["current"]
    temperature = data.get("temperature")
    cycle_index = data["cycle_index"]

    summaries: list[CycleSummary] = []
    by_cycle: dict[int, list[StepSegment]] = {}
    for step in steps:
        by_cycle.setdefault(step.cycle_index, []).append(step)

    for start, stop in _runs(cycle_index):
        index = int(cycle_index[start])
        window = voltage[start:stop]
        cycle_steps = [s for s in by_cycle.get(index, []) if start <= s.start < stop]

        summary = CycleSummary(
            cycle_index=index,
            cycle_number=index + 1 + cycle_offset,
            start=start,
            stop=stop,
            start_time_s=float(seconds[start]),
            duration_s=float(seconds[stop - 1] - seconds[start]),
            voltage_max=float(window.max()),
            voltage_min=float(window.min()),
            steps=cycle_steps,
        )
        for step in cycle_steps:
            if step.mode == "charge":
                summary.charge_capacity_mah += step.capacity_mah
                summary.charge_energy_wh += step.energy_wh
            elif step.mode == "discharge":
                summary.discharge_capacity_mah += step.capacity_mah
                summary.discharge_energy_wh += step.energy_wh

        window_current = current[start:stop]
        charging = window_current > 1e-12
        discharging = window_current < -1e-12
        if charging.any():
            summary.max_charge_current_a = float(window_current[charging].max())
        if discharging.any():
            summary.max_discharge_current_a = float(-window_current[discharging].min())
        if temperature is not None and len(temperature):
            mean_t = float(np.mean(temperature[start:stop]))
            summary.temperature_mean = mean_t if mean_t else None

        # Energy-weighted mean voltage: E / Q, the quantity that actually
        # reflects where the plateau sits.
        if summary.charge_capacity_mah:
            summary.mean_charge_voltage = (
                summary.charge_energy_wh * 1000.0 / summary.charge_capacity_mah
            )
        if summary.discharge_capacity_mah:
            summary.mean_discharge_voltage = (
                summary.discharge_energy_wh * 1000.0 / summary.discharge_capacity_mah
            )

        has_charge = any(s.mode == "charge" for s in cycle_steps)
        has_discharge = any(s.mode == "discharge" for s in cycle_steps)
        is_last = stop >= len(cycle_index)
        summary.complete = bool(has_charge and has_discharge) and not (
            is_last and _ends_mid_step(wrd, stop)
        )
        summaries.append(summary)

    return summaries


def _ends_mid_step(wrd: WrdFile, stop: int) -> bool:
    """True when the file stops part-way through a step.

    Long runs are split across files, so the final cycle of a file is usually
    truncated.  Current still flowing on the last sample is the primary tell,
    but a schedule whose last step *is* the charge or discharge will also end
    that way legitimately -- so a final voltage that has reached the
    schedule's cut-off counts as a normal termination.
    """
    if stop <= 0 or stop > len(wrd):
        return False
    current = float(wrd.data["current"][stop - 1])
    if abs(current) <= 1e-9:
        return False

    schedule = wrd.metadata.schedule
    if schedule is None:
        return True
    voltage = float(wrd.data["voltage"][stop - 1])
    tolerance = 0.01
    if current < 0:
        cutoff = schedule.lower_cutoff_v
        direction = "discharge"
        at_cutoff = cutoff is not None and voltage <= cutoff + tolerance
    else:
        cutoff = schedule.upper_cutoff_v
        direction = "charge"
        at_cutoff = cutoff is not None and voltage >= cutoff - tolerance
    if not at_cutoff:
        return True

    # A CV hold sits *at* the cut-off voltage for its whole length while the
    # current tapers, so the voltage alone cannot separate a finished hold from
    # a file split in the middle of one.  When the schedule tapers this
    # direction, the current must have reached the taper setpoint as well.
    taper = schedule.taper_current_a(direction)
    return taper is not None and abs(current) > taper * 1.1


def extract_profile(wrd: WrdFile, cycle: CycleSummary, branch: str) -> Profile:
    """Capacity-vs-voltage for one branch of one cycle.

    Capacity is re-zeroed at the start of the branch so a cycle plots from
    0 mAh regardless of what the cycler's running total was.
    """
    if branch not in ("charge", "discharge"):
        raise ValueError(f"branch must be 'charge' or 'discharge', got {branch!r}")

    segments = [s for s in cycle.steps if s.mode == branch]
    if not segments:
        empty = np.empty(0, dtype=np.float64)
        return Profile(cycle.cycle_number, branch, empty, empty, empty, empty)

    column = "charge_q" if branch == "charge" else "discharge_q"
    capacity_all = wrd.charge_mah() if branch == "charge" else wrd.discharge_mah()
    del column
    voltage_all = wrd.data["voltage"]
    current_all = wrd.data["current"]
    seconds_all = wrd.seconds("test_time")

    capacity_parts, voltage_parts, time_parts, current_parts = [], [], [], []
    consumed = 0.0
    for segment in segments:
        chunk = capacity_all[segment.start:segment.stop]
        # Successive segments of the same branch (CC then CV) continue the
        # cycler's running total, so only the first needs re-zeroing.
        capacity_parts.append(chunk - chunk[0] + consumed)
        consumed = float(capacity_parts[-1][-1])
        voltage_parts.append(voltage_all[segment.start:segment.stop])
        time_parts.append(seconds_all[segment.start:segment.stop])
        current_parts.append(current_all[segment.start:segment.stop])

    return Profile(
        cycle_number=cycle.cycle_number,
        branch=branch,
        capacity_mah=np.concatenate(capacity_parts),
        voltage=np.concatenate(voltage_parts),
        time_s=np.concatenate(time_parts),
        current_a=np.concatenate(current_parts),
    )
