"""The work between an HTTP request and ``wrdkit``.

Kept out of the routers so the parse pipeline, the cell-spec resolution and
the series builders can be tested without a client.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone

import numpy as np
from sqlmodel import Session, select

from wrdkit import (
    Basis,
    CellSpec,
    Composition,
    CycleSummary,
    ResolvedCell,
    WrdFile,
    lttb,
    normalize_capacity,
    parse_composition,
    summarize_cycles,
)
from wrdkit.cycles import Profile, extract_profile
from wrdkit.health import CellReport, build_report
from wrdkit.knee import KneeAnalysis

from . import storage
from .models import CycleRecord, Run, Sample
from .settings import settings

#: Smart Interface splits a long run into ..._011.wrd, ..._012.wrd and so on.
_SEQUENCE_SUFFIX = re.compile(r"_(\d{2,4})\.wrd$", re.IGNORECASE)


# --------------------------------------------------------------------------
# cell spec
# --------------------------------------------------------------------------
def sample_composition(sample: Sample | None) -> Composition:
    """The stored blend, or an empty one."""
    if sample is None or not sample.composition_json:
        return Composition()
    try:
        return Composition.from_json(json.loads(sample.composition_json))
    except (ValueError, TypeError):
        return Composition()


def apply_composition(sample: Sample, components: list | None,
                      text: str | None, explicit_wt_percent: bool) -> None:
    """Store a composition and let it drive the active weight percent.

    A researcher who typed ``active_wt_percent`` in the same request meant it,
    so the composition does not overwrite that.
    """
    if components is not None:
        composition = Composition.from_json(
            [c if isinstance(c, dict) else c.model_dump() for c in components])
    elif text is not None:
        composition = parse_composition(text)
    else:
        return

    sample.composition_json = json.dumps(composition.to_json(), ensure_ascii=False)
    if not explicit_wt_percent:
        sample.active_wt_percent = composition.active_wt_percent


def cell_spec_from_sample(sample: Sample | None) -> CellSpec:
    if sample is None:
        return CellSpec()
    return CellSpec(
        composition=sample_composition(sample),
        active_mass_mg=sample.active_mass_mg,
        total_mass_mg=sample.total_mass_mg,
        current_collector_mass_mg=sample.current_collector_mass_mg,
        active_wt_percent=sample.active_wt_percent,
        area_cm2=sample.area_cm2,
        diameter_mm=sample.diameter_mm,
        thickness_um=sample.thickness_um,
        nominal_specific_capacity_mah_g=sample.nominal_specific_capacity_mah_g,
    )


def resolve_cell(sample: Sample | None, overrides: dict | None = None) -> ResolvedCell:
    """Sample spec, optionally overridden per request for what-if normalisation."""
    spec = cell_spec_from_sample(sample)
    for key, value in (overrides or {}).items():
        if value is not None and hasattr(spec, key):
            setattr(spec, key, value)
    return spec.resolve()


# --------------------------------------------------------------------------
# parsing and persistence
# --------------------------------------------------------------------------
def sequence_number(name: str) -> int | None:
    """The ``012`` in ``..._1000cyc_60oC_012.wrd``, when present."""
    match = _SEQUENCE_SUFFIX.search(name)
    return int(match.group(1)) if match else None


def run_order_key(start_time: datetime | None, name: str, run_id: int | None):
    """Sort files the way the experiment actually ran.

    Acquisition start time decides, truncated to the second: two continuation
    files of one experiment are hours apart, so truncation never reorders
    them, but it stops a sub-second difference from outranking the ``_012``
    suffix the instrument appends -- and that suffix is the *stated* order.
    The row id breaks any remaining tie deterministically.
    """
    moment = start_time or datetime.min
    return (
        moment.replace(microsecond=0),
        sequence_number(name) or 0,
        moment,
        run_id if run_id is not None else 1 << 62,
    )


def renumber_sample_runs(session: Session, sample_id: int | None) -> None:
    """Recompute cycle offsets so a sample's files read as one experiment.

    Runs whose offset was set by hand keep it; the automatic ones continue
    from whatever came before.  Called after every change that can reorder a
    sample's files, so uploading ``_011`` after ``_012`` still lands right.
    """
    if sample_id is None:
        return
    runs = list(session.exec(select(Run).where(Run.sample_id == sample_id)).all())
    runs.sort(key=lambda r: run_order_key(r.start_time, r.original_name, r.id))

    running_total = 0
    for run in runs:
        if run.cycle_offset_source == "manual":
            offset = run.cycle_offset
        else:
            offset = running_total
        if run.cycle_offset != offset:
            run.cycle_offset = offset
            session.add(run)
            for record in session.exec(
                    select(CycleRecord).where(CycleRecord.run_id == run.id)).all():
                record.cycle_number = record.cycle_index + 1 + offset
                session.add(record)
        running_total = max(running_total, offset + run.cycle_count)


def auto_cycle_offset(session: Session, sample_id: int | None,
                      start_time: datetime | None, name: str = "",
                      exclude_run_id: int | None = None) -> int:
    """Cycle offset for a file about to be added to *sample_id*."""
    if sample_id is None:
        return 0
    runs = [r for r in session.exec(select(Run).where(Run.sample_id == sample_id)).all()
            if r.id != exclude_run_id]
    if not runs:
        return 0
    key = run_order_key(start_time, name, exclude_run_id)
    earlier = [r for r in runs
               if run_order_key(r.start_time, r.original_name, r.id) < key]
    return sum(run.cycle_count for run in earlier)


def persist_parse(session: Session, run: Run, wrd: WrdFile) -> list[CycleSummary]:
    """Write parsed metadata, the cycle table and the column cache."""
    metadata = wrd.metadata
    run.device_model = metadata.model or ""
    run.serial_no = metadata.serial_no or ""
    run.channel = metadata.channel
    run.app_version = metadata.app_version or ""
    run.firmware_version = metadata.firmware_version or ""
    run.start_time = metadata.start_time
    run.end_time = metadata.end_time
    run.row_count = metadata.row_count
    run.data_format = metadata.data_format
    run.unit_coulomb = metadata.unit_coulomb
    run.instrument_path = metadata.instrument_path or ""
    run.schedule_path = metadata.schedule_path or ""
    run.schedule_json = json.dumps(schedule_payload(wrd), ensure_ascii=False)
    run.parse_error = ""
    run.parsed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    cycles = summarize_cycles(wrd, cycle_offset=run.cycle_offset)
    run.cycle_count = len(cycles)
    run.complete_cycle_count = sum(1 for c in cycles if c.complete)

    run.cycles.clear()
    session.flush()

    for cycle in cycles:
        session.add(CycleRecord(
            run_id=run.id,
            cycle_index=cycle.cycle_index,
            cycle_number=cycle.cycle_number,
            charge_capacity_mah=cycle.charge_capacity_mah,
            discharge_capacity_mah=cycle.discharge_capacity_mah,
            charge_energy_wh=cycle.charge_energy_wh,
            discharge_energy_wh=cycle.discharge_energy_wh,
            coulombic_efficiency=cycle.coulombic_efficiency,
            energy_efficiency=cycle.energy_efficiency,
            mean_charge_voltage=cycle.mean_charge_voltage,
            mean_discharge_voltage=cycle.mean_discharge_voltage,
            voltage_max=cycle.voltage_max,
            voltage_min=cycle.voltage_min,
            max_charge_current_a=cycle.max_charge_current_a,
            max_discharge_current_a=cycle.max_discharge_current_a,
            temperature_mean=cycle.temperature_mean,
            start_time_s=cycle.start_time_s,
            duration_s=cycle.duration_s,
            n_points=cycle.n_points,
            complete=cycle.complete,
            row_start=cycle.start,
            row_stop=cycle.stop,
        ))

    storage.cache_columns(run.id, wrd)
    return cycles


def schedule_payload(wrd: WrdFile) -> dict:
    """The decoded protocol, in a shape the UI can render directly."""
    schedule = wrd.metadata.schedule
    if schedule is None:
        return {}
    nominal = schedule.nominal_capacity_ah()
    return {
        "source_path": schedule.source_path,
        "version": schedule.version,
        "upper_cutoff_v": schedule.upper_cutoff_v,
        "lower_cutoff_v": schedule.lower_cutoff_v,
        "planned_cycles": schedule.planned_cycles,
        "c_rate": schedule.infer_c_rate(),
        "cycling_current_a": schedule.cycling_current_a,
        "formation_current_a": schedule.formation_current_a,
        "nominal_capacity_mah": nominal * 1000 if nominal else None,
        "sampling_interval_s": schedule.sampling_interval_s,
        "steps": [
            {
                "index": step.index,
                "name": step.name,
                "control": step.control,
                "direction": step.direction,
                "current_a": step.current_a,
                "voltage_limit_v": step.voltage_limit_v,
                "taper_current_a": step.taper_current_a,
                "loop_count": step.loop_count,
                "loop_target": step.loop_target,
                "sampling_interval_s": step.sampling_interval_s,
                "cutoffs": [
                    {"kind": c.kind, "condition": c.condition,
                     "value": c.value, "seconds": c.seconds,
                     "text": c.describe()}
                    for c in step.cutoffs
                ],
                "text": step.describe(),
            }
            for step in schedule.steps
        ],
    }


def apply_schedule_defaults(sample: Sample, payload: dict) -> bool:
    """Fill blank sample conditions from the schedule; never overwrite input."""
    changed = False
    mapping = {
        "cutoff_upper_v": payload.get("upper_cutoff_v"),
        "cutoff_lower_v": payload.get("lower_cutoff_v"),
        "c_rate": payload.get("c_rate"),
    }
    for field, value in mapping.items():
        if value is not None and getattr(sample, field) is None:
            setattr(sample, field, value)
            changed = True
    nominal = payload.get("nominal_capacity_mah")
    if (nominal and sample.nominal_specific_capacity_mah_g is None
            and sample.active_mass_mg is None and sample.total_mass_mg is None):
        # Without a mass the nominal capacity cannot become a specific one,
        # so leave it; the UI shows it from schedule_json instead.
        pass
    return changed


# --------------------------------------------------------------------------
# reading back
# --------------------------------------------------------------------------
def cycle_records(session: Session, run_ids: list[int]) -> list[CycleRecord]:
    if not run_ids:
        return []
    statement = (select(CycleRecord)
                 .where(CycleRecord.run_id.in_(run_ids))
                 .order_by(CycleRecord.cycle_number))
    return list(session.exec(statement).all())


def sample_cycle_records(session: Session, sample: Sample) -> list[CycleRecord]:
    """Every cycle of a sample, across all its files, in cycle order."""
    return cycle_records(session, [run.id for run in sample.runs if run.id])


def records_to_summaries(records: list[CycleRecord]) -> list[CycleSummary]:
    """Rebuild the wrdkit view from stored rows, so analysis code is shared."""
    summaries = []
    for record in records:
        summary = CycleSummary(
            cycle_index=record.cycle_index,
            cycle_number=record.cycle_number,
            start=record.row_start,
            stop=record.row_stop,
            charge_capacity_mah=record.charge_capacity_mah,
            discharge_capacity_mah=record.discharge_capacity_mah,
            charge_energy_wh=record.charge_energy_wh,
            discharge_energy_wh=record.discharge_energy_wh,
            mean_charge_voltage=record.mean_charge_voltage,
            mean_discharge_voltage=record.mean_discharge_voltage,
            voltage_max=record.voltage_max,
            voltage_min=record.voltage_min,
            start_time_s=record.start_time_s,
            duration_s=record.duration_s,
            max_charge_current_a=record.max_charge_current_a,
            max_discharge_current_a=record.max_discharge_current_a,
            temperature_mean=record.temperature_mean,
            complete=record.complete,
        )
        summaries.append(summary)
    return summaries


#: How far ahead of this machine's clock an instrument timestamp may sit and
#: still be read as "just now".  Two PCs drift by seconds, not by hours.
_CLOCK_SKEW_TOLERANCE = timedelta(minutes=5)


def _usable_last_sample_time(last_sample_time: datetime | None,
                             now: datetime) -> datetime | None:
    """Drop a last-sample time whose clock does not match ours.

    A future timestamp makes the record's age negative, which reads as fresh
    and is printed to the user as "-8.5 h old".  Within the drift of two
    clocks the honest reading is "just now"; beyond it the two clocks are on
    different zones or badly set, and no recency verdict can be earned from
    them -- so none is offered (non-negotiable #4).
    """
    if last_sample_time is None or last_sample_time <= now:
        return last_sample_time
    if last_sample_time - now <= _CLOCK_SKEW_TOLERANCE:
        return now
    return None


def build_cell_report(session: Session, sample: Sample, *,
                      knee_options: dict | None = None) -> CellReport:
    """The running/finished readout for a sample, across all its files."""
    records = sample_cycle_records(session, sample)
    summaries = records_to_summaries(records)

    planned = None
    last_sample_time = None
    schedule_finished = None
    for run in sample.runs:
        if run.schedule_json:
            payload = json.loads(run.schedule_json)
            planned = payload.get("planned_cycles") or planned
        if run.end_time and (last_sample_time is None or run.end_time > last_sample_time):
            last_sample_time = run.end_time

    declared = None if sample.declared_state == "auto" else sample.declared_state
    # ``last_sample_time`` is the wall clock of the PC that ran Smart
    # Interface, stored naive because the file says nothing about its zone.
    # Comparing it against a naive *UTC* now subtracts two different clocks:
    # in a KST lab every file looks nine hours into the future, so a cell that
    # stopped yesterday still reads "running", and the stale-record signal
    # ADR 0008 calls decisive arrives nine hours late.  The server runs beside
    # the instrument, so its own local clock is the matching one.
    now = datetime.now()
    last_sample_time = _usable_last_sample_time(last_sample_time, now)
    return build_report(
        summaries,
        reference_cycle=sample.reference_cycle,
        planned_cycles=planned,
        last_sample_time=last_sample_time,
        now=now,
        schedule_finished=schedule_finished,
        declared_state=declared,
        knee_options=knee_options,
    )


def knee_payload(analysis: KneeAnalysis | None) -> dict | None:
    if analysis is None:
        return None
    return {
        "primary": asdict(analysis.primary),
        "results": [asdict(r) for r in analysis.results],
        "reference_cycle": analysis.reference_cycle,
        "reference_capacity_mah": analysis.reference_capacity_mah,
        "search_start_cycle": analysis.search_start_cycle,
        "n_points": analysis.n_points,
        "fade_rate_early_pct_per_cycle": analysis.fade_rate_early_pct_per_cycle,
        "fade_rate_late_pct_per_cycle": analysis.fade_rate_late_pct_per_cycle,
        "projected_cycle_at_80pct": analysis.projected_cycle_at_80pct,
    }


def normalized(value: float | None, cell: ResolvedCell, basis: str) -> float | None:
    """Normalise when possible; return the raw mAh when the basis is unavailable."""
    if value is None:
        return None
    divisor = cell.divisor(basis)
    if divisor is None:
        return value
    return normalize_capacity(value, cell, basis)


def effective_basis(cell: ResolvedCell, basis: str) -> str:
    """The basis actually used, after falling back for missing inputs."""
    return basis if cell.divisor(basis) else Basis.ABSOLUTE


# --------------------------------------------------------------------------
# profiles
# --------------------------------------------------------------------------
def load_wrd_columns(run: Run) -> dict[str, np.ndarray]:
    """Cached columns for a run, re-parsing the original if the cache is gone."""
    columns = storage.load_columns(run.id, expect_sha256=run.sha256)
    if columns is not None:
        return columns
    wrd = storage.reparse(run.sha256)
    storage.cache_columns(run.id, wrd)
    return wrd.data


def profile_series(run: Run, record: CycleRecord, branch: str,
                   cell: ResolvedCell, basis: str, *,
                   max_points: int | None = None) -> dict:
    """One downsampled capacity-vs-voltage branch, ready for the plot."""
    columns = load_wrd_columns(run)
    wrd = WrdFile(_metadata_stub(run), columns)
    summary = records_to_summaries([record])[0]
    summary.steps = _rebuild_steps(wrd, record)
    profile = extract_profile(wrd, summary, branch)
    return _profile_payload(profile, cell, basis,
                            max_points or settings.default_plot_points)


def _profile_payload(profile: Profile, cell: ResolvedCell, basis: str,
                     max_points: int) -> dict:
    used = effective_basis(cell, basis)
    capacity = profile.capacity_mah
    if used != Basis.ABSOLUTE:
        capacity = normalize_capacity(capacity, cell, used)
    if len(capacity) > max_points:
        capacity, voltage = lttb(capacity, profile.voltage, max_points)
    else:
        voltage = profile.voltage
    return {
        "cycle": profile.cycle_number,
        "branch": profile.branch,
        "basis": used,
        "points": len(capacity),
        "capacity": [round(float(v), 6) for v in capacity],
        "voltage": [round(float(v), 6) for v in voltage],
    }


def _metadata_stub(run: Run):
    """A minimal metadata object so wrdkit's unit helpers work off cached columns."""
    from wrdkit.wrd import WrdMetadata

    return WrdMetadata(
        source_name=run.original_name,
        sha256=run.sha256,
        file_size=run.size_bytes,
        unit_coulomb=run.unit_coulomb,
        row_count=run.row_count,
    )


def _rebuild_steps(wrd: WrdFile, record: CycleRecord):
    """Re-segment just the one cycle we are plotting."""
    from wrdkit.cycles import segment_steps

    window = {name: values[record.row_start:record.row_stop]
              for name, values in wrd.data.items()}
    # A copy, not the caller's metadata: a file loaded once and reused for
    # every cycle of an export would otherwise end up claiming the row count
    # of whichever cycle was segmented last.
    sliced = WrdFile(replace(wrd.metadata,
                             row_count=record.row_stop - record.row_start), window)
    steps = segment_steps(sliced)
    for step in steps:
        step.start += record.row_start
        step.stop += record.row_start
    return steps
