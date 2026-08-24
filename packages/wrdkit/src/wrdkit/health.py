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

    #: Why there is no completed cycle, when there is none.  Empty otherwise.
    #: ``no_discharge`` | ``no_charge`` | ``truncated`` | ``no_steps`` |
    #: ``no_cycles``.
    #:
    #: Without this the screen showed a column of em-dashes and the word "no
    #: completed cycle yet", which reads as a parse failure.  The three causes
    #: need three different actions: wait for the run (truncated), upload the
    #: next file in the split, or accept that a charge-only protocol will never
    #: produce a cycle capacity.
    no_complete_reason: str = ""

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


#: How strongly each observation argues for a state.  These are not votes of
#: equal weight: a file that ends mid-cycle is only weak evidence of a live
#: cell, because Smart Interface splits long runs into ``_011``, ``_012`` ...
#: and every one of those ends mid-cycle too.  A long silence, by contrast, is
#: decisive -- nothing is running if nothing has been logged in days.
_WEIGHTS = {
    "schedule_end": 3.0,
    "planned_reached": 3.0,
    "recency_stale": 3.0,
    "recency_fresh": 2.5,
    "partial_cycle": 1.0,
    "planned_incomplete": 0.5,
}

#: Silence beyond this multiple of a cycle time means the cell is not running.
_STALE_CYCLE_MULTIPLE = 5.0
#: Silence within this multiple means it almost certainly is.
_FRESH_CYCLE_MULTIPLE = 2.0
#: Fallback when cycle durations are unknown (a file with no complete cycle).
_FRESH_HOURS = 6.0
_STALE_HOURS = 48.0


def _classify(cycles: list[CycleSummary], *, planned_cycles: int | None,
              last_sample_time: datetime | None, now: datetime | None,
              schedule_finished: bool | None,
              declared_state: str | None) -> tuple[str, str, list[StateEvidence]]:
    """Decide running vs finished, and say why.

    Evidence is weighted rather than counted, and the margin between the two
    sides sets the confidence.  When the signals genuinely disagree the state
    is reported with low confidence rather than asserted -- the operator can
    then pin it by hand.
    """
    evidence: list[StateEvidence] = []

    if declared_state in (CellState.RUNNING, CellState.FINISHED):
        evidence.append(StateEvidence(
            "manual", "state was set by hand on the sample", declared_state))
        return declared_state, "high", evidence

    complete = [c for c in cycles if c.complete]
    scores = {CellState.RUNNING: 0.0, CellState.FINISHED: 0.0}

    def note(signal: str, detail: str, points_to: str, weight: float) -> None:
        evidence.append(StateEvidence(signal, detail, points_to))
        scores[points_to] += weight

    if schedule_finished:
        note("schedule", "the record reaches the step after the cycling loop",
             CellState.FINISHED, _WEIGHTS["schedule_end"])
    if planned_cycles and len(complete) >= planned_cycles:
        note("cycle count",
             f"{len(complete)} of {planned_cycles} planned cycles completed",
             CellState.FINISHED, _WEIGHTS["planned_reached"])

    # "Incomplete" is not one thing.  A cycle cut off mid-step argues the cell
    # is still running; a cycle that simply has no discharge argues nothing at
    # all -- the schedule never asked for one.  Saying "cut off mid-step" about
    # a multi-step CCCV charge that ran to its cut-off and stopped cleanly is
    # false, and it was the only line the screen had to explain an empty table.
    reason = cycles[-1].incomplete_reason if cycles else ""
    last_incomplete = bool(cycles) and not cycles[-1].complete
    # 이유를 모르면(옛 기록, 손으로 만든 요약) 예전처럼 "잘렸다" 로 읽는다 --
    # 아는 것이 늘었을 때만 판단이 바뀌어야 한다.
    ends_mid_cycle = last_incomplete and reason not in ("no_discharge", "no_charge")
    if ends_mid_cycle:
        note("partial cycle",
             f"cycle {cycles[-1].cycle_number} is cut off mid-step",
             CellState.RUNNING, _WEIGHTS["partial_cycle"])
    elif reason in ("no_discharge", "no_charge"):
        # A note, not a vote: it explains the empty table without pretending to
        # know whether the rack is still busy.
        evidence.append(StateEvidence(
            "branch missing",
            f"cycle {cycles[-1].cycle_number} has no "
            f"{'discharge' if reason == 'no_discharge' else 'charge'} "
            f"- the schedule never asked for one",
            CellState.UNKNOWN))
    if planned_cycles and len(complete) < planned_cycles:
        note("cycle count",
             f"only {len(complete)} of {planned_cycles} planned cycles are present",
             CellState.RUNNING, _WEIGHTS["planned_incomplete"])

    if last_sample_time and now:
        idle_hours = (now - last_sample_time).total_seconds() / 3600.0
        typical = _typical_cycle_hours(complete)
        fresh_limit = typical * _FRESH_CYCLE_MULTIPLE if typical else _FRESH_HOURS
        stale_limit = typical * _STALE_CYCLE_MULTIPLE if typical else _STALE_HOURS
        window = (f"two cycle times ({typical:.1f} h)" if typical
                  else f"{_FRESH_HOURS:.0f} h")
        if idle_hours < fresh_limit:
            note("recency",
                 f"last sample is {_hours(idle_hours)} old, under {window}",
                 CellState.RUNNING, _WEIGHTS["recency_fresh"])
        elif idle_hours > stale_limit:
            detail = f"nothing logged for {_hours(idle_hours)}"
            if ends_mid_cycle:
                # The honest reading: this file stopped mid-cycle long ago, so
                # either the test ended or it continued into a file nobody has
                # uploaded.  Either way the cell is not running now.
                detail += " even though the record ends mid-cycle - the test " \
                          "stopped, or it continued in a file that is not here"
            note("recency", detail, CellState.FINISHED, _WEIGHTS["recency_stale"])

    running, finished = scores[CellState.RUNNING], scores[CellState.FINISHED]
    if not running and not finished:
        evidence.append(StateEvidence(
            "none", "the file carries no schedule and no partial cycle to judge by",
            CellState.UNKNOWN))
        return CellState.UNKNOWN, "low", evidence

    state = CellState.RUNNING if running > finished else CellState.FINISHED
    margin = abs(running - finished)
    confidence = "high" if margin >= 2.5 else "medium" if margin >= 1.0 else "low"
    return state, confidence, evidence


def _no_complete_summary(reason: str) -> str:
    """Say what is missing, not just that something is.

    "no completed cycle yet" was the whole message, and "yet" is wrong for a
    charge-only protocol: that record will never produce a cycle capacity no
    matter how long anyone waits.
    """
    return {
        "no_discharge": "no completed cycle: the record has no discharge, "
                        "so there is no cycle capacity to report",
        "no_charge": "no completed cycle: the record has no charge",
        "truncated": "no completed cycle yet: the record stops part-way "
                     "through a step",
        "no_cycles": "no cycles in this record",
    }.get(reason, "no completed cycle yet")


def _hours(value: float) -> str:
    """A duration a human reads at a glance."""
    if value < 48:
        return f"{value:.1f} h"
    if value < 24 * 60:
        return f"{value / 24:.1f} days"
    return f"{value / 24 / 30.44:.1f} months"


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

    last_reason = cycles[-1].incomplete_reason if cycles else ""
    if cycles and not cycles[-1].complete and last_reason not in (
            "no_discharge", "no_charge"):
        # A cycle missing a branch the schedule never asked for is not "in
        # progress" -- putting a cycle number there promises one that will
        # never advance.  An unknown reason keeps the old reading (in progress),
        # so nothing regresses on records parsed before this existed.
        report.in_progress_cycle = cycles[-1].cycle_number

    if not complete:
        report.no_complete_reason = last_reason if cycles else "no_cycles"
        report.state_summary = _no_complete_summary(report.no_complete_reason)
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
        # Fall back to the earliest cycle *after* the requested one, so a
        # continuation file that starts at cycle 200 still gets a baseline.
        #
        # And only then.  Falling back to `complete[0]` when nothing follows the
        # request put cycle 1 -- a formation cycle, the one thing the reference
        # exists to exclude (ADR 0004) -- back in as the retention denominator
        # and the knee baseline.  `detect_knee` learned to answer
        # `indeterminate` for exactly this, and this line reached past it by
        # handing over cycle 1 as if the caller had asked for it.
        later = [c for c in complete if c.cycle_number > reference_cycle]
        if later:
            report.reference = _readout(later[0])
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
                f"is measured from the earliest cycle after it"
            )

    options = dict(knee_options or {})
    # The requested cycle, not the fallback: the core knows what to do when
    # there is nothing at or after it, and passing the fallback along hides the
    # question from it.
    options.setdefault(
        "reference_cycle",
        report.reference.cycle if report.reference_available else reference_cycle,
    )
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
        if report.in_progress_cycle:
            parts.append(
                f"not running; the record stops during cycle "
                f"{report.in_progress_cycle} with {report.cycles_complete} complete")
        else:
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
