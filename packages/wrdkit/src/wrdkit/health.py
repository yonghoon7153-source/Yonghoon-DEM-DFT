"""Answer the two questions asked of every cell on the rack.

*Is this cell still running, or is it done?*  and, given that,
*what is its discharge capacity, and how much of cycle 3 is left?*

Those need different arithmetic.  A running cell's newest cycle is partial,
so quoting it would understate the capacity; the honest number is the last
cycle that actually finished -- the cycle before the one in progress.  A
finished cell has no such caveat.

Cycle 3 is the reference because the first cycles are formation: they lose
several percent by design, so retention measured against cycle 1 mixes
formation loss with degradation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .cycles import CycleSummary
from .knee import KneeAnalysis, detect_knee

__all__ = ["CellState", "StateEvidence", "CycleReadout", "CellReport", "build_report",
           "DEFAULT_REFERENCE_CYCLE"]

#: Formation normally takes two cycles, so cycle 3 is the first that reflects
#: steady-state behaviour.  Overridable per sample.
DEFAULT_REFERENCE_CYCLE = 3


class CellState:
    RUNNING = "running"
    FINISHED = "finished"
    UNKNOWN = "unknown"


@dataclass
class StateEvidence:
    """One observation that argued for the reported state."""

    signal: str
    detail: str
    points_to: str


@dataclass
class CycleReadout:
    """The numbers for one cycle, in raw mAh."""

    cycle: int
    discharge_mah: float
    charge_mah: float
    coulombic_efficiency: float | None
    mean_discharge_voltage: float | None = None
    energy_efficiency: float | None = None
    complete: bool = True


@dataclass
class CellReport:
    """Everything the dashboard shows for one cell."""

    state: str
    state_confidence: str  # high | medium | low
    state_summary: str
    evidence: list[StateEvidence] = field(default_factory=list)

    cycles_observed: int = 0
    cycles_complete: int = 0
    planned_cycles: int | None = None
    in_progress_cycle: int | None = None

    #: The cycle whose capacity is quoted -- the last completed one.
    reported: CycleReadout | None = None
    #: The reference cycle (3 by default) used for retention and initial CE.
    reference: CycleReadout | None = None
    reference_cycle_requested: int = DEFAULT_REFERENCE_CYCLE
    reference_available: bool = False
    #: The true first cycle, kept because "ICE" conventionally means cycle 1.
    first_cycle: CycleReadout | None = None

    retention_pct: float | None = None
    retention_note: str = ""
    knee: KneeAnalysis | None = None

    @property
    def initial_coulombic_efficiency(self) -> float | None:
        """CE of the reference cycle -- what the user calls the initial CE."""
        return self.reference.coulombic_efficiency if self.reference else None


def _readout(cycle: CycleSummary) -> CycleReadout:
    return CycleReadout(
        cycle=cycle.cycle_number,
        discharge_mah=cycle.discharge_capacity_mah,
        charge_mah=cycle.charge_capacity_mah,
        coulombic_efficiency=cycle.coulombic_efficiency,
        mean_discharge_voltage=cycle.mean_discharge_voltage,
        energy_efficiency=cycle.energy_efficiency,
        complete=cycle.complete,
    )


def _classify(cycles: list[CycleSummary], *, planned_cycles: int | None,
              last_sample_time: datetime | None, now: datetime | None,
              schedule_finished: bool | None,
              declared_state: str | None) -> tuple[str, str, list[StateEvidence]]:
    """Decide running vs finished, and say why."""
    evidence: list[StateEvidence] = []

    if declared_state in (CellState.RUNNING, CellState.FINISHED):
        evidence.append(StateEvidence(
            "manual", "state was set by hand on the sample", declared_state))
        return declared_state, "high", evidence

    complete = [c for c in cycles if c.complete]

    if schedule_finished:
        evidence.append(StateEvidence(
            "schedule", "the record reaches the step after the cycling loop",
            CellState.FINISHED))
    if planned_cycles and len(complete) >= planned_cycles:
        evidence.append(StateEvidence(
            "cycle count", f"{len(complete)} of {planned_cycles} planned cycles completed",
            CellState.FINISHED))
    if cycles and not cycles[-1].complete:
        evidence.append(StateEvidence(
            "partial cycle",
            f"cycle {cycles[-1].cycle_number} is cut off mid-step",
            CellState.RUNNING))
    if planned_cycles and len(complete) < planned_cycles:
        evidence.append(StateEvidence(
            "cycle count",
            f"only {len(complete)} of {planned_cycles} planned cycles are present",
            CellState.RUNNING))

    if last_sample_time and now:
        idle_hours = (now - last_sample_time).total_seconds() / 3600.0
        typical = _typical_cycle_hours(complete)
        if typical and idle_hours < 2 * typical:
            evidence.append(StateEvidence(
                "recency",
                f"last sample is {idle_hours:.1f} h old, under two cycle times "
                f"({typical:.1f} h)",
                CellState.RUNNING))
        elif typical and idle_hours > 5 * typical:
            evidence.append(StateEvidence(
                "recency",
                f"no data for {idle_hours:.1f} h, over five cycle times "
                f"({typical:.1f} h)",
                CellState.FINISHED))

    finished_votes = sum(1 for e in evidence if e.points_to == CellState.FINISHED)
    running_votes = sum(1 for e in evidence if e.points_to == CellState.RUNNING)

    if finished_votes and not running_votes:
        return CellState.FINISHED, "high" if finished_votes > 1 else "medium", evidence
    if running_votes and not finished_votes:
        return CellState.RUNNING, "high" if running_votes > 1 else "medium", evidence
    if finished_votes or running_votes:
        state = CellState.FINISHED if finished_votes > running_votes else CellState.RUNNING
        return state, "low", evidence

    evidence.append(StateEvidence(
        "none", "the file carries no schedule and no partial cycle to judge by",
        CellState.UNKNOWN))
    return CellState.UNKNOWN, "low", evidence


def _typical_cycle_hours(cycles: list[CycleSummary]) -> float | None:
    durations = sorted(c.duration_s for c in cycles[-10:] if c.duration_s > 0)
    if not durations:
        return None
    return durations[len(durations) // 2] / 3600.0


def build_report(cycles: list[CycleSummary], *,
                 reference_cycle: int = DEFAULT_REFERENCE_CYCLE,
                 planned_cycles: int | None = None,
                 last_sample_time: datetime | None = None,
                 now: datetime | None = None,
                 schedule_finished: bool | None = None,
                 declared_state: str | None = None,
                 knee_options: dict | None = None) -> CellReport:
    """Build the running/finished readout for one cell.

    ``cycles`` is the full cycle list for the cell -- if the cell spans
    several files, concatenate them first so cycle numbers are continuous.
    """
    complete = [c for c in cycles if c.complete]
    state, confidence, evidence = _classify(
        cycles, planned_cycles=planned_cycles, last_sample_time=last_sample_time,
        now=now, schedule_finished=schedule_finished, declared_state=declared_state)

    report = CellReport(
        state=state,
        state_confidence=confidence,
        state_summary="",
        evidence=evidence,
        cycles_observed=len(cycles),
        cycles_complete=len(complete),
        planned_cycles=planned_cycles,
        reference_cycle_requested=reference_cycle,
    )

    if cycles and not cycles[-1].complete:
        report.in_progress_cycle = cycles[-1].cycle_number

    if not complete:
        report.state_summary = "no completed cycle yet"
        return report

    # The quoted capacity is always the last cycle that actually finished.
    # For a running cell that is, by construction, (in-progress cycle - 1).
    report.reported = _readout(complete[-1])
    report.first_cycle = _readout(complete[0])

    reference = next((c for c in complete if c.cycle_number == reference_cycle), None)
    if reference is not None:
        report.reference = _readout(reference)
        report.reference_available = True
    else:
        # Fall back to the earliest cycle at or after the requested one, so a
        # continuation file that starts at cycle 200 still gets a baseline.
        later = [c for c in complete if c.cycle_number > reference_cycle]
        fallback = later[0] if later else complete[0]
        report.reference = _readout(fallback)
        report.reference_available = False

    if report.reference and report.reference.discharge_mah:
        report.retention_pct = (
            100.0 * report.reported.discharge_mah / report.reference.discharge_mah
        )
        if report.reference_available:
            report.retention_note = (
                f"cycle {report.reported.cycle} vs cycle {report.reference.cycle}"
            )
        else:
            report.retention_note = (
                f"cycle {report.reported.cycle} vs cycle {report.reference.cycle} "
                f"- cycle {reference_cycle} is not in this record, so retention "
                f"is measured from the earliest cycle available"
            )

    options = dict(knee_options or {})
    options.setdefault("reference_cycle", report.reference.cycle if report.reference else None)
    report.knee = detect_knee(
        [c.cycle_number for c in complete],
        [c.discharge_capacity_mah for c in complete],
        **options,
    )

    report.state_summary = _summarize(report)
    return report


def _summarize(report: CellReport) -> str:
    parts = []
    if report.state == CellState.RUNNING:
        if report.in_progress_cycle:
            parts.append(f"running, cycle {report.in_progress_cycle} in progress")
        else:
            parts.append("running")
    elif report.state == CellState.FINISHED:
        parts.append(f"finished after {report.cycles_complete} cycles")
    else:
        parts.append(f"{report.cycles_complete} cycles recorded, state unclear")

    if report.reported:
        parts.append(
            f"cycle {report.reported.cycle} discharge {report.reported.discharge_mah:.4g} mAh"
        )
    if report.retention_pct is not None:
        parts.append(f"{report.retention_pct:.1f}% retention")
    if report.reference and report.reference.coulombic_efficiency:
        parts.append(
            f"cycle {report.reference.cycle} CE {report.reference.coulombic_efficiency:.2f}%"
        )
    if report.knee and report.knee.primary.detected:
        parts.append(f"knee at cycle {report.knee.primary.cycle:.0f}")
    return "; ".join(parts)
