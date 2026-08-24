"""Cycle tables, profiles, cell reports and comparisons.

Every capacity leaves this module tagged with the basis it is in, and every
request may override the sample's mass/area for a what-if without saving.
"""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from wrdkit import Basis, ResolvedCell, basis_label, c_rate
from wrdkit.deltas import previous_cycle_deltas
from wrdkit.ica import (
    DEFAULT_POLY_ORDER,
    DEFAULT_SMOOTHER,
    DEFAULT_SMOOTHING,
    DEFAULT_VOLTAGE_STEP,
    SMOOTHERS,
)

from ..db import get_session
from ..deps import get_run, get_sample, resolved_cell_out, validate_basis
from ..models import CycleRecord, Sample
from ..schemas import (
    CycleOut,
    CycleTableOut,
    DqdvOut,
    DqdvSeriesOut,
    DvdqOut,
    DvdqSeriesOut,
    PartialCycleOut,
    ProfileOut,
    ProfileSeriesOut,
    ReportOut,
)
from ..services import (
    build_cell_report,
    cycle_records,
    dqdv_series,
    dvdq_series,
    effective_basis,
    knee_payload,
    normalized,
    profile_series,
    resolve_cell,
    sample_cycle_records,
)
from ..settings import settings


def _validate_smoother(smoother: str) -> None:
    """Refuse an unknown filter by name instead of falling back silently.

    Falling back would put "savgol" on the screen and a moving average in the
    numbers, and the two differ enough at order 2 to change what a reader
    concludes about a peak (ADR 0015).
    """
    if smoother not in SMOOTHERS:
        raise HTTPException(
            422, f"unknown smoother {smoother!r}; expected one of "
                 f"{', '.join(SMOOTHERS)}")


#: How many cells one comparison may hold.  Both compare endpoints share it:
#: /compare/cycles used to 422 past thirty while /compare/profiles silently
#: dropped everything after the thirtieth, so selecting thirty-one cells gave
#: an error on one tab and a quietly incomplete plot on the other.
_COMPARE_LIMIT = 30

router = APIRouter(prefix="/api", tags=["analysis"])


def _overrides(active_mass_mg, area_cm2, diameter_mm, total_mass_mg,
               active_wt_percent, nominal_specific_capacity_mah_g,
               thickness_um) -> dict:
    return {
        "active_mass_mg": active_mass_mg,
        "area_cm2": area_cm2,
        "diameter_mm": diameter_mm,
        "total_mass_mg": total_mass_mg,
        "active_wt_percent": active_wt_percent,
        "nominal_specific_capacity_mah_g": nominal_specific_capacity_mah_g,
        "thickness_um": thickness_um,
    }


def _parse_cycles(spec: str | None) -> set[int] | None:
    """``1,3,10-20`` -> the set of cycle numbers it names."""
    if not spec or spec.strip().lower() == "all":
        return None
    wanted: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            if "-" in part:
                start, stop = part.split("-", 1)
                if int(stop) < int(start):
                    raise ValueError
                wanted.update(range(int(start), int(stop) + 1))
            else:
                wanted.add(int(part))
        except ValueError as exc:
            raise HTTPException(
                422, f"could not read cycle selection {part!r}; "
                     "use forms like 1,3,10-20") from exc
    return wanted


def _parse_branches(branches: str) -> list[str]:
    """``charge,discharge`` -> the branches it names.

    A typo has to come back as a 422 from every endpoint that takes it; left
    unchecked it reaches ``extract_profile`` and surfaces as a 500.
    """
    parsed = [b.strip() for b in branches.split(",") if b.strip()]
    for branch in parsed:
        if branch not in ("charge", "discharge"):
            raise HTTPException(422, f"branch must be charge or discharge, got {branch!r}")
    return parsed


def _reference_note(requested: int | None, used_cycle: int | None) -> str:
    """Why retention is not anchored where the caller asked (ADR 0004)."""
    if used_cycle is None:
        return "no completed cycle, so retention cannot be measured"
    if requested is None:
        return ("no reference cycle is set for this file, so retention is "
                f"measured from cycle {used_cycle}")
    return (f"cycle {requested} is not in this record, so retention is "
            f"measured from cycle {used_cycle}")


def _cycle_rows(records: list[CycleRecord], cell, basis: str,
                reference_cycle: int | None) -> tuple[list[CycleOut], dict]:
    """The rows, plus what the retention column was actually anchored to."""
    used = effective_basis(cell, basis)
    reference = None
    if reference_cycle is not None:
        reference = next((r for r in records
                          if r.cycle_number == reference_cycle and r.complete), None)
    reference_available = reference is not None
    if reference is None:
        # ADR 0004: a missing reference cycle must not quietly anchor on
        # formation.  Prefer the earliest complete cycle *after* the requested
        # one -- a continuation file starting at cycle 201 carries no formation
        # at all -- and tell the caller which cycle stood in, the same way
        # health.build_report does.
        later = [r for r in records
                 if r.complete and reference_cycle is not None
                 and r.cycle_number > reference_cycle]
        reference = (min(later, key=lambda r: r.cycle_number) if later
                     else next((r for r in records if r.complete), None))
    reference_info = {
        "reference_cycle_used": reference.cycle_number if reference else None,
        "reference_available": reference_available,
        "retention_note": "" if reference_available else _reference_note(
            reference_cycle, reference.cycle_number if reference else None),
    }

    # One fixed denominator for the whole column.  Dividing each row by its own
    # capacity makes a constant-current protocol look like an accelerating one
    # as the cell fades (1 mA / 5 mAh = 0.20C -> 1 mA / 2.5 mAh = 0.40C).
    rate_reference_mah = reference.discharge_capacity_mah if reference else None
    if not rate_reference_mah:
        rate_reference_mah = next(
            (r.discharge_capacity_mah for r in records if r.discharge_capacity_mah), None)

    # 단차는 표 전체를 한 번에 봐야 한다 — 앞 행을 보고 계산하는 것이라
    # 행마다 따로 구할 수 없다.  잘린 사이클이 기준이 되지 않게 하는 규칙도
    # 여기 한 곳(wrdkit/deltas.py)에만 둔다.
    #
    # 정규화된 값으로 계산한다.  표에 보이는 열과 그 열의 차가 같아야 하기
    # 때문이다 — mAh 로 빼고 mAh/g 로 보여 주면, 사람이 두 행을 직접 빼 본
    # 값과 단차 열이 어긋난다.
    numbers = [r.cycle_number for r in records]
    flags = [r.complete for r in records]
    discharge_steps = previous_cycle_deltas(
        numbers,
        [normalized(r.discharge_capacity_mah, cell, used) if r.complete else None
         for r in records],
        flags)
    charge_steps = previous_cycle_deltas(
        numbers,
        [normalized(r.charge_capacity_mah, cell, used) if r.complete else None
         for r in records],
        flags)

    rows: list[CycleOut] = []
    for record, discharge_step, charge_step in zip(
            records, discharge_steps, charge_steps, strict=True):
        # 잘린 사이클의 파생 수치는 내보내지 않는다.  complete_only=false 는
        # "그 행을 보여 달라" 이지 "부분값을 측정값으로 달라" 가 아니다 —
        # JSON 의 숫자 칸은 complete 플래그가 뭐라고 하든 측정값으로 읽힌다.
        # CSV writer 가 같은 자리를 비우므로 두 출력이 같은 말을 한다.
        partial = not record.complete

        def kept(value, _partial=partial):
            return None if _partial else value

        hysteresis = None
        if record.mean_charge_voltage is not None and record.mean_discharge_voltage is not None:
            hysteresis = record.mean_charge_voltage - record.mean_discharge_voltage
        retention = None
        if reference and reference.discharge_capacity_mah:
            retention = 100.0 * record.discharge_capacity_mah / reference.discharge_capacity_mah
        rate = None
        if record.max_discharge_current_a:
            rate = c_rate(record.max_discharge_current_a, cell,
                          measured_capacity_mah=rate_reference_mah)
        rows.append(CycleOut(
            cycle=record.cycle_number,
            cycle_index=record.cycle_index,
            run_id=record.run_id,
            charge_capacity=kept(normalized(record.charge_capacity_mah, cell, used)),
            discharge_capacity=kept(normalized(record.discharge_capacity_mah, cell, used)),
            charge_capacity_mah=kept(record.charge_capacity_mah),
            discharge_capacity_mah=kept(record.discharge_capacity_mah),
            coulombic_efficiency=kept(record.coulombic_efficiency),
            energy_efficiency=kept(record.energy_efficiency),
            charge_energy_mwh=kept(record.charge_energy_wh * 1000.0),
            discharge_energy_mwh=kept(record.discharge_energy_wh * 1000.0),
            # 전위는 옮기고, 차이는 그대로 둔다.  이력(hysteresis)은 두 전위의
            # 차라 오프셋이 양쪽에서 상쇄된다 — 여기에 또 더하면 있지도 않은
            # 0.62 V 의 분극을 만들어 낸다.  에너지도 건드리지 않는다
            # (wrdkit/reference.py 참고).
            mean_charge_voltage=kept(cell.potential(record.mean_charge_voltage)),
            mean_discharge_voltage=kept(cell.potential(record.mean_discharge_voltage)),
            voltage_hysteresis=kept(hysteresis),
            voltage_max=kept(cell.potential(record.voltage_max)),
            voltage_min=kept(cell.potential(record.voltage_min)),
            retention_pct=kept(retention),
            # `kept` 를 다시 씌우지 않는다.  deltas 가 이미 잘린 사이클에
            # None 을 넣었고, 그 판정이 한 곳에만 있어야 두 규칙이 어긋나지
            # 않는다.
            discharge_delta=discharge_step.delta,
            charge_delta=charge_step.delta,
            discharge_delta_pct=discharge_step.delta_pct,
            delta_base_cycle=discharge_step.previous_cycle,
            delta_span=discharge_step.span,
            discharge_delta_per_cycle=discharge_step.per_cycle,
            c_rate=rate,
            temperature_mean=record.temperature_mean,
            duration_h=record.duration_s / 3600.0,
            n_points=record.n_points,
            complete=record.complete,
        ))
    return rows, reference_info


def _partial_cycles(records: list[CycleRecord]) -> list[PartialCycleOut]:
    """The cycles that carry no numbers, and why.

    ``incomplete_reason`` is stored at parse time.  Rows written before that
    column existed hold "", and rather than guess, they are reported as "" and
    the screen says "이유 미상 — 재파싱하면 나옵니다".  Guessing here would be
    wrong in the case that matters most: a running cell cut off during its
    charge looks exactly like a charge-only protocol from the stored numbers,
    and the two need opposite readings.
    """
    out: list[PartialCycleOut] = []
    for record in records:
        if record.complete:
            continue
        out.append(PartialCycleOut(
            cycle=record.cycle_number,
            run_id=record.run_id,
            reason=record.incomplete_reason,
            # 용량도 전류도 아닌 **스텝**으로 본다.  용량으로 보면 CV 홀드만
            # 있는 브랜치가 없는 것이 되고, 전류로 보면 -2e-12 A 짜리 잡음
            # 한 점이 "방전이 있었다" 가 된다 -- 뒤쪽은 incomplete_reason 과
            # 정면으로 어긋난다.  옛 행(NULL)만 예전처럼 전류로 읽는다.
            has_charge=(record.has_charge_step if record.has_charge_step is not None
                        else record.max_charge_current_a is not None),
            has_discharge=(record.has_discharge_step if record.has_discharge_step is not None
                           else record.max_discharge_current_a is not None),
        ))
    return out


@router.get("/samples/{sample_id}/cycles", response_model=CycleTableOut)
def sample_cycles(
    sample_id: int,
    session: Session = Depends(get_session),
    basis: str = Query(Basis.ABSOLUTE),
    complete_only: bool = Query(True, description="hide the cycle still in progress"),
    active_mass_mg: float | None = None,
    area_cm2: float | None = None,
    diameter_mm: float | None = None,
    total_mass_mg: float | None = None,
    active_wt_percent: float | None = None,
    nominal_specific_capacity_mah_g: float | None = None,
    thickness_um: float | None = None,
):
    """The cycle table for one cell, across every file it owns."""
    validate_basis(basis)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample, _overrides(
        active_mass_mg, area_cm2, diameter_mm, total_mass_mg,
        active_wt_percent, nominal_specific_capacity_mah_g, thickness_um))

    records = sample_cycle_records(session, sample)
    # 걸러내기 **전에** 센다.  complete_only 는 표에서 그 행을 빼라는 뜻이지,
    # 그런 사이클이 없다고 말하라는 뜻이 아니다.
    partial = _partial_cycles(records)
    if complete_only:
        records = [r for r in records if r.complete]

    used = effective_basis(cell, basis)
    rows, reference_info = _cycle_rows(records, cell, basis, sample.reference_cycle)
    return CycleTableOut(
        basis=used,
        basis_label=basis_label(used),
        requested_basis=basis,
        basis_fallback_reason=cell.missing_for(basis) if used != basis else None,
        reference_cycle=sample.reference_cycle,
        resolved_cell=resolved_cell_out(cell),
        cycles=rows,
        partial_cycles=partial,
        **reference_info,
    )


@router.get("/runs/{run_id}/cycles", response_model=CycleTableOut)
def run_cycles(
    run_id: int,
    session: Session = Depends(get_session),
    basis: str = Query(Basis.ABSOLUTE),
    complete_only: bool = Query(False),
):
    """The cycle table for a single file."""
    validate_basis(basis)
    run = get_run(session, run_id)
    sample = session.get(Sample, run.sample_id) if run.sample_id else None
    cell = resolve_cell(sample)
    records = cycle_records(session, [run.id])
    partial = _partial_cycles(records)
    if complete_only:
        records = [r for r in records if r.complete]
    used = effective_basis(cell, basis)
    reference = sample.reference_cycle if sample else None
    rows, reference_info = _cycle_rows(records, cell, basis, reference)
    return CycleTableOut(
        basis=used,
        basis_label=basis_label(used),
        requested_basis=basis,
        basis_fallback_reason=cell.missing_for(basis) if used != basis else None,
        reference_cycle=reference,
        resolved_cell=resolved_cell_out(cell),
        cycles=rows,
        partial_cycles=partial,
        **reference_info,
    )


#: How many cycles may be drawn at once.  The old ceiling was 60 and a 196-cycle
#: cell could not show its own record: "all" quietly stopped at cycle 41.
_PROFILE_CYCLE_LIMIT = 400
#: Points across *every* curve in one response.  What has to stay bounded is the
#: payload, not the number of curves, so a request for four hundred curves gets
#: fewer samples of each rather than a refusal.  1,200 points per curve times
#: 400 curves is ten megabytes of JSON; this is about one.
_PROFILE_POINT_BUDGET = 120_000
#: Below this a curve stops being a curve.
_MIN_POINTS_PER_CURVE = 80


def _points_per_curve(requested: int | None, curves: int) -> int:
    """Share the point budget out over however many curves were asked for."""
    limit = requested or settings.default_plot_points
    if curves <= 0:
        return limit
    return max(min(limit, _PROFILE_POINT_BUDGET // curves), _MIN_POINTS_PER_CURVE)


@router.get("/samples/{sample_id}/profile", response_model=ProfileOut)
def sample_profile(
    sample_id: int,
    session: Session = Depends(get_session),
    cycles: str = Query("1", description="cycle numbers, e.g. 1,3,10-20 or all"),
    branches: str = Query("charge,discharge"),
    basis: str = Query(Basis.ABSOLUTE),
    include_partial: bool = Query(
        False, description="also draw cycles that carry no cycle-level numbers"),
    max_points: int | None = Query(None, ge=50, le=20000),
    active_mass_mg: float | None = None,
    area_cm2: float | None = None,
    diameter_mm: float | None = None,
    total_mass_mg: float | None = None,
    active_wt_percent: float | None = None,
    nominal_specific_capacity_mah_g: float | None = None,
    thickness_um: float | None = None,
):
    """Voltage-vs-capacity curves for the requested cycles."""
    validate_basis(basis)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample, _overrides(
        active_mass_mg, area_cm2, diameter_mm, total_mass_mg,
        active_wt_percent, nominal_specific_capacity_mah_g, thickness_um))

    wanted = _parse_cycles(cycles)
    requested_branches = _parse_branches(branches)

    # 잘리거나 한쪽 브랜치가 없는 사이클도 **곡선은 실측이다.**  숫자를 내는
    # 것과 그리는 것은 다르다 -- 사이클 용량은 여전히 안 내고(표가 비운다),
    # 그린 곡선에는 complete=false 를 달아 화면이 그렇게 그리게 한다.
    #
    # 기본이 False 인 이유: 완료 사이클들 사이에 잘린 곡선이 아무 표시 없이 끼면
    # 셀이 갑자기 용량을 잃은 것처럼 보인다.  달라고 해야 준다.
    records = sample_cycle_records(session, sample)
    if not include_partial:
        records = [r for r in records if r.complete]
    if wanted is not None:
        records = [r for r in records if r.cycle_number in wanted]
    if len(records) > _PROFILE_CYCLE_LIMIT:
        raise HTTPException(
            422, f"{len(records)} cycles requested; ask for at most "
                 f"{_PROFILE_CYCLE_LIMIT} at a time")

    runs = {run.id: run for run in sample.runs}
    limit = _points_per_curve(max_points, len(records) * len(requested_branches))
    series: list[ProfileSeriesOut] = []
    for record in records:
        run = runs.get(record.run_id)
        if run is None:
            continue
        for branch in requested_branches:
            payload = profile_series(run, record, branch, cell, basis,
                                     max_points=limit)
            if not payload["points"]:
                continue
            series.append(ProfileSeriesOut(
                **payload, run_id=run.id,
                complete=record.complete,
                incomplete_reason=record.incomplete_reason,
                label=f"{sample.name} · cycle {record.cycle_number} {branch}"))

    used = effective_basis(cell, basis)
    return ProfileOut(basis=used, basis_label=basis_label(used),
                      requested_basis=basis,
                      resolved_cell=resolved_cell_out(cell), series=series)


@router.get("/samples/{sample_id}/dqdv", response_model=DqdvOut)
def sample_dqdv(
    sample_id: int,
    session: Session = Depends(get_session),
    cycles: str = Query("1", description="cycle numbers, e.g. 1,3,10-20 or all"),
    branches: str = Query("charge,discharge"),
    basis: str = Query(Basis.ABSOLUTE),
    voltage_step: float = Query(DEFAULT_VOLTAGE_STEP, gt=0.0001, le=0.2),
    smoothing: int = Query(DEFAULT_SMOOTHING, ge=1, le=101),
    smoother: str = Query(DEFAULT_SMOOTHER,
                          description="moving | savgol (ADR 0015)"),
    poly_order: int = Query(DEFAULT_POLY_ORDER, ge=0, le=6,
                            description="savgol only; 1 reproduces the lab "
                                        "script and equals a moving average"),
    max_points: int | None = Query(None, ge=50, le=20000),
    active_mass_mg: float | None = None,
    area_cm2: float | None = None,
    diameter_mm: float | None = None,
    total_mass_mg: float | None = None,
    active_wt_percent: float | None = None,
    nominal_specific_capacity_mah_g: float | None = None,
    thickness_um: float | None = None,
):
    """dQ/dV for the requested cycles -- the same cycles the profile takes.

    Deliberately its own endpoint rather than a mode of ``/profile``: the two
    have different axes (volts across, mAh/V up) and different point budgets,
    and a client that had to guess which shape came back would guess wrong on
    the first empty result.
    """
    validate_basis(basis)
    _validate_smoother(smoother)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample, _overrides(
        active_mass_mg, area_cm2, diameter_mm, total_mass_mg,
        active_wt_percent, nominal_specific_capacity_mah_g, thickness_um))

    records, requested_branches = _differential_records(
        session, sample, cycles, branches)
    runs = {run.id: run for run in sample.runs}
    limit = _points_per_curve(max_points, len(records) * len(requested_branches))
    series: list[DqdvSeriesOut] = []
    for record in records:
        run = runs.get(record.run_id)
        if run is None:
            continue
        for branch in requested_branches:
            payload = dqdv_series(run, record, branch, cell, basis,
                                  voltage_step=voltage_step, smoothing=smoothing,
                                  smoother=smoother, poly_order=poly_order,
                                  max_points=limit)
            # 계산이 안 된 곡선도 이유와 함께 돌려준다.  빼 버리면 화면에서 그
            # 사이클이 왜 없는지 알 방법이 없다.
            series.append(DqdvSeriesOut(
                **payload, run_id=run.id,
                label=f"{sample.name} · cycle {record.cycle_number} {branch}"))

    used = effective_basis(cell, basis)
    return DqdvOut(basis=used, basis_label=basis_label(used),
                   requested_basis=basis,
                   resolved_cell=resolved_cell_out(cell), series=series,
                   voltage_step=voltage_step, smoothing=smoothing,
                   smoother=smoother, poly_order=poly_order,
                   mixed_basis=_mixed(series))


def _differential_records(session, sample, cycles: str, branches: str):
    """The complete cycles and branches a dQ/dV or dV/dQ request asked for.

    Shared by both so the two endpoints can never disagree about which cycles
    exist -- they are drawn one above the other and a cycle present on one
    plot and absent on the other reads as a data problem in the cell.
    """
    wanted = _parse_cycles(cycles)
    requested_branches = _parse_branches(branches)
    records = [r for r in sample_cycle_records(session, sample) if r.complete]
    if wanted is not None:
        records = [r for r in records if r.cycle_number in wanted]
    if len(records) > _PROFILE_CYCLE_LIMIT:
        raise HTTPException(
            422, f"{len(records)} cycles requested; ask for at most "
                 f"{_PROFILE_CYCLE_LIMIT} at a time")
    return records, requested_branches


def _mixed(series) -> bool:
    """Do the curves that actually carry data disagree about their unit?

    Empty curves have a basis but no numbers, so counting them would report a
    mixed axis for a plot that draws in one unit.
    """
    return len({item.basis for item in series if item.points}) > 1


@router.get("/samples/{sample_id}/dvdq", response_model=DvdqOut)
def sample_dvdq(
    sample_id: int,
    session: Session = Depends(get_session),
    cycles: str = Query("1", description="cycle numbers, e.g. 1,3,10-20 or all"),
    branches: str = Query("charge,discharge"),
    basis: str = Query(Basis.ABSOLUTE),
    capacity_step: float | None = Query(
        None, gt=0,
        description="grid spacing in mAh; omit to use 1/400 of each branch's "
                    "own span (ADR 0015)"),
    smoothing: int = Query(DEFAULT_SMOOTHING, ge=1, le=101),
    smoother: str = Query(DEFAULT_SMOOTHER, description="moving | savgol"),
    poly_order: int = Query(DEFAULT_POLY_ORDER, ge=0, le=6),
    max_points: int | None = Query(None, ge=50, le=20000),
    active_mass_mg: float | None = None,
    area_cm2: float | None = None,
    diameter_mm: float | None = None,
    total_mass_mg: float | None = None,
    active_wt_percent: float | None = None,
    nominal_specific_capacity_mah_g: float | None = None,
    thickness_um: float | None = None,
):
    """dV/dQ for the requested cycles -- dQ/dV's mirror, on a capacity grid.

    Its own endpoint for the same reason dQ/dV is: the axes are different
    (capacity across, V per capacity up) and so is the point budget, and a
    client made to guess which shape came back would guess wrong on the first
    empty result.

    ``capacity_step`` matters more than it looks.  Left out, every branch gets
    a grid sized to its own span, which is right for one curve and wrong for an
    overlay -- pin it in mAh when comparing cycles or cells.
    """
    validate_basis(basis)
    _validate_smoother(smoother)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample, _overrides(
        active_mass_mg, area_cm2, diameter_mm, total_mass_mg,
        active_wt_percent, nominal_specific_capacity_mah_g, thickness_um))

    records, requested_branches = _differential_records(
        session, sample, cycles, branches)
    runs = {run.id: run for run in sample.runs}
    limit = _points_per_curve(max_points, len(records) * len(requested_branches))
    series: list[DvdqSeriesOut] = []
    for record in records:
        run = runs.get(record.run_id)
        if run is None:
            continue
        for branch in requested_branches:
            payload = dvdq_series(run, record, branch, cell, basis,
                                  capacity_step=capacity_step,
                                  smoothing=smoothing, smoother=smoother,
                                  poly_order=poly_order, max_points=limit)
            series.append(DvdqSeriesOut(
                **payload, run_id=run.id,
                label=f"{sample.name} · cycle {record.cycle_number} {branch}"))

    used = effective_basis(cell, basis)
    return DvdqOut(basis=used, basis_label=basis_label(used),
                   requested_basis=basis,
                   resolved_cell=resolved_cell_out(cell), series=series,
                   smoothing=smoothing, smoother=smoother,
                   poly_order=poly_order, capacity_step=capacity_step,
                   mixed_basis=_mixed(series))


@router.get("/samples/{sample_id}/report", response_model=ReportOut)
def sample_report(
    sample_id: int,
    session: Session = Depends(get_session),
    basis: str = Query(Basis.ABSOLUTE),
    threshold_pct: float = Query(80.0, gt=0, le=100),
    slope_factor: float = Query(2.0, gt=1),
    active_mass_mg: float | None = None,
    area_cm2: float | None = None,
    diameter_mm: float | None = None,
    total_mass_mg: float | None = None,
    active_wt_percent: float | None = None,
    nominal_specific_capacity_mah_g: float | None = None,
    thickness_um: float | None = None,
):
    """Is this cell running or done, what is its capacity, where is the knee.

    For a running cell the quoted cycle is the last one that finished -- the
    cycle before the one in progress -- because the newest is truncated.
    """
    validate_basis(basis)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample, _overrides(
        active_mass_mg, area_cm2, diameter_mm, total_mass_mg,
        active_wt_percent, nominal_specific_capacity_mah_g, thickness_um))

    report = build_cell_report(session, sample, knee_options={
        "threshold_pct": threshold_pct, "slope_factor": slope_factor})
    used = effective_basis(cell, basis)

    def readout(entry) -> dict | None:
        if entry is None:
            return None
        return {
            "cycle": entry.cycle,
            "discharge_capacity": normalized(entry.discharge_mah, cell, used),
            "charge_capacity": normalized(entry.charge_mah, cell, used),
            "discharge_capacity_mah": entry.discharge_mah,
            "charge_capacity_mah": entry.charge_mah,
            "coulombic_efficiency": entry.coulombic_efficiency,
            "energy_efficiency": entry.energy_efficiency,
            "mean_discharge_voltage": cell.potential(entry.mean_discharge_voltage),
            "complete": entry.complete,
        }

    planned = None
    for run in sample.runs:
        if run.schedule_json:
            planned = json.loads(run.schedule_json).get("planned_cycles") or planned

    return ReportOut(
        sample_id=sample.id,
        sample_name=sample.name,
        state=report.state,
        state_confidence=report.state_confidence,
        state_summary=report.state_summary,
        evidence=[{"signal": e.signal, "detail": e.detail, "points_to": e.points_to}
                  for e in report.evidence],
        cycles_observed=report.cycles_observed,
        cycles_complete=report.cycles_complete,
        planned_cycles=planned,
        in_progress_cycle=report.in_progress_cycle,
        reference_cycle_requested=report.reference_cycle_requested,
        reference_available=report.reference_available,
        retention_pct=report.retention_pct,
        retention_note=report.retention_note,
        no_complete_reason=report.no_complete_reason,
        basis=used,
        basis_label=basis_label(used),
        reported=readout(report.reported),
        reference=readout(report.reference),
        first_cycle=readout(report.first_cycle),
        knee=knee_payload(report.knee),
        resolved_cell=resolved_cell_out(cell),
    )


@router.get("/compare/cycles")
def compare_cycles(
    session: Session = Depends(get_session),
    sample_ids: str = Query(..., description="comma-separated sample ids"),
    basis: str = Query(Basis.ABSOLUTE),
    metric: str = Query("discharge_capacity",
                        description="discharge_capacity | coulombic_efficiency | "
                                    "retention | energy_efficiency | "
                                    "mean_discharge_voltage | voltage_hysteresis"),
    complete_only: bool = Query(True),
):
    """One series per cell, for overlaying cycle-life curves."""
    validate_basis(basis)
    allowed = {"discharge_capacity", "charge_capacity", "coulombic_efficiency",
               "retention", "energy_efficiency", "mean_discharge_voltage",
               "voltage_hysteresis"}
    if metric not in allowed:
        raise HTTPException(422, f"metric must be one of {sorted(allowed)}")

    try:
        ids = [int(part) for part in sample_ids.split(",") if part.strip()]
    except ValueError as exc:
        raise HTTPException(422, "sample_ids must be comma-separated integers") from exc
    if not ids:
        raise HTTPException(422, "no sample ids given")
    if len(ids) > _COMPARE_LIMIT:
        raise HTTPException(
            422, f"compare at most {_COMPARE_LIMIT} samples at a time")

    series = []
    for sample_id in ids:
        sample = session.get(Sample, sample_id)
        if sample is None:
            continue
        cell = resolve_cell(sample)
        records = sample_cycle_records(session, sample)
        if complete_only:
            records = [r for r in records if r.complete]
        rows, reference_info = _cycle_rows(records, cell, basis, sample.reference_cycle)

        key = {"retention": "retention_pct"}.get(metric, metric)
        points = [
            {"cycle": row.cycle, "value": getattr(row, key)}
            for row in rows if getattr(row, key) is not None
        ]
        used = effective_basis(cell, basis)
        is_capacity = metric.endswith("capacity")
        series.append({
            "sample_id": sample.id,
            "sample_name": sample.name,
            "group_id": sample.group_id,
            "cathode_type": sample.cathode_type,
            "c_rate": sample.c_rate,
            "temperature_c": sample.temperature_c,
            "basis": used if is_capacity else "",
            # A mass-less cell falls back to raw mAh.  Without this the curve
            # joins the others on one axis with nothing saying it is in a
            # different unit, and reads as a forty-times-worse cell.
            "basis_fallback_reason": (cell.missing_for(basis)
                                      if is_capacity and used != basis else None),
            **reference_info,
            "points": points,
        })

    # Derived from the series that were actually built.  resolve_cell(None) has
    # no mass or area, so every capacity axis came back labelled "mAh" even when
    # the points were mAh/g.
    used_bases = {s["basis"] for s in series if s["basis"]}
    mixed_basis = len(used_bases) > 1
    response_basis = next(iter(used_bases)) if len(used_bases) == 1 else basis
    unit = basis_label(response_basis)
    labels = {
        "discharge_capacity": "Discharge capacity",
        "charge_capacity": "Charge capacity",
        "coulombic_efficiency": "Coulombic efficiency (%)",
        "retention": "Capacity retention (%)",
        "energy_efficiency": "Energy efficiency (%)",
        "mean_discharge_voltage": "Mean discharge voltage (V)",
        "voltage_hysteresis": "Voltage hysteresis (V)",
    }
    return {
        "metric": metric,
        "metric_label": labels[metric],
        "basis": response_basis,
        "requested_basis": basis,
        # True means the curves are not in the same unit; the axis cannot be
        # labelled for all of them at once, so the client has to annotate.
        "mixed_basis": mixed_basis,
        "y_label": unit if metric.endswith("capacity") else labels[metric],
        "series": series,
    }


@router.get("/compare/profiles", response_model=ProfileOut)
def compare_profiles(
    session: Session = Depends(get_session),
    sample_ids: str = Query(...),
    cycle: int = Query(..., ge=1),
    branches: str = Query("discharge"),
    basis: str = Query(Basis.ABSOLUTE),
    max_points: int | None = Query(None, ge=50, le=20000),
):
    """The same cycle from several cells, overlaid."""
    validate_basis(basis)
    try:
        ids = [int(part) for part in sample_ids.split(",") if part.strip()]
    except ValueError as exc:
        raise HTTPException(422, "sample_ids must be comma-separated integers") from exc
    requested_branches = _parse_branches(branches)

    if len(ids) > _COMPARE_LIMIT:
        raise HTTPException(
            422, f"at most {_COMPARE_LIMIT} cells can be compared at once "
                 f"({len(ids)} requested)")

    limit = max_points or settings.default_plot_points
    series: list[ProfileSeriesOut] = []
    drawn_cells: list[ResolvedCell] = []
    for sample_id in ids:
        sample = session.get(Sample, sample_id)
        if sample is None:
            continue
        cell = resolve_cell(sample)
        record = next((r for r in sample_cycle_records(session, sample)
                       if r.cycle_number == cycle and r.complete), None)
        if record is None:
            continue
        run = next((r for r in sample.runs if r.id == record.run_id), None)
        if run is None:
            continue
        drew = False
        for branch in requested_branches:
            payload = profile_series(run, record, branch, cell, basis, max_points=limit)
            if payload["points"]:
                drew = True
                series.append(ProfileSeriesOut(
                    **payload, run_id=run.id,
                    label=f"{sample.name} · cycle {cycle} {branch}",
                    basis_fallback_reason=(
                        cell.missing_for(basis)
                        if payload["basis"] != basis else None)))
        if drew:
            drawn_cells.append(cell)

    # Derived from the curves actually drawn, not from whichever sample the
    # loop happened to look at last.  Ask A (has mass) then B (has none) and
    # the old code labelled A's mAh/g axis "mAh", because B overwrote the
    # fallback cell on its way to being skipped.
    used_bases = {s.basis for s in series if s.basis}
    mixed = len(used_bases) > 1
    used = next(iter(used_bases)) if len(used_bases) == 1 else basis
    # One cell's mass and area only describe the plot when one cell is in it.
    shown_cell = drawn_cells[0] if len(drawn_cells) == 1 else resolve_cell(None)
    return ProfileOut(basis=used, basis_label=basis_label(used),
                      requested_basis=basis, mixed_basis=mixed,
                      resolved_cell=resolved_cell_out(shown_cell), series=series)


def _compare_ids(sample_ids: str) -> list[int]:
    try:
        ids = [int(part) for part in sample_ids.split(",") if part.strip()]
    except ValueError as exc:
        raise HTTPException(
            422, "sample_ids must be comma-separated integers") from exc
    if len(ids) > _COMPARE_LIMIT:
        raise HTTPException(
            422, f"at most {_COMPARE_LIMIT} cells can be compared at once "
                 f"({len(ids)} requested)")
    return ids


def _compare_differential(session, ids, cycle, requested_branches, basis, build):
    """Walk the selected cells for one cycle and let *build* make each curve.

    dQ/dV and dV/dQ differ only in which service function runs and which
    schema wraps it; everything around that -- skipping a cell that has no such
    cycle, tracking which units were actually drawn, deciding whose mass may
    describe the plot -- is identical, and having it twice is how the two
    screens end up disagreeing about a fallback.
    """
    out = []
    drawn_cells: list[ResolvedCell] = []
    for sample_id in ids:
        sample = session.get(Sample, sample_id)
        if sample is None:
            continue
        cell = resolve_cell(sample)
        record = next((r for r in sample_cycle_records(session, sample)
                       if r.cycle_number == cycle and r.complete), None)
        if record is None:
            continue
        run = next((r for r in sample.runs if r.id == record.run_id), None)
        if run is None:
            continue
        drew = False
        for branch in requested_branches:
            payload = build(run, record, branch, cell)
            # 비교 화면에서는 빈 곡선을 싣지 않는다.  상세 화면과 다른 선택인데
            # 이유가 있다: 거기서는 "이 사이클이 왜 없나" 를 셀 하나에 대해
            # 말해 줘야 하고, 여기서는 서른 셀의 빈 항목이 범례를 덮는다.
            if not payload["points"]:
                continue
            drew = True
            out.append((payload, run, sample, branch, cell))
        if drew:
            drawn_cells.append(cell)

    used_bases = {p["basis"] for p, *_ in out if p["basis"]}
    mixed = len(used_bases) > 1
    used = next(iter(used_bases)) if len(used_bases) == 1 else basis
    # 한 셀의 질량·면적은 그 셀 하나만 그려졌을 때에만 이 화면을 설명한다.
    shown_cell = drawn_cells[0] if len(drawn_cells) == 1 else resolve_cell(None)
    return out, used, mixed, shown_cell


@router.get("/compare/dqdv", response_model=DqdvOut)
def compare_dqdv(
    session: Session = Depends(get_session),
    sample_ids: str = Query(...),
    cycle: int = Query(..., ge=1),
    branches: str = Query("discharge"),
    basis: str = Query(Basis.ABSOLUTE),
    voltage_step: float = Query(DEFAULT_VOLTAGE_STEP, gt=0.0001, le=0.2),
    smoothing: int = Query(DEFAULT_SMOOTHING, ge=1, le=101),
    smoother: str = Query(DEFAULT_SMOOTHER, description="moving | savgol"),
    poly_order: int = Query(DEFAULT_POLY_ORDER, ge=0, le=6),
    max_points: int | None = Query(None, ge=50, le=20000),
):
    """The same cycle's dQ/dV from several cells, overlaid.

    Every cell is gridded and smoothed identically here, which is the whole
    point: peak *height* is only comparable between curves built the same way
    (ADR 0013), and a comparison screen is exactly where someone reads heights
    off against each other.
    """
    validate_basis(basis)
    _validate_smoother(smoother)
    ids = _compare_ids(sample_ids)
    requested_branches = _parse_branches(branches)
    limit = max_points or settings.default_plot_points

    built, used, mixed, shown_cell = _compare_differential(
        session, ids, cycle, requested_branches, basis,
        lambda run, record, branch, cell: dqdv_series(
            run, record, branch, cell, basis, voltage_step=voltage_step,
            smoothing=smoothing, smoother=smoother, poly_order=poly_order,
            max_points=limit))

    series = [DqdvSeriesOut(**payload, run_id=run.id,
                            label=f"{sample.name} · cycle {cycle} {branch}")
              for payload, run, sample, branch, _cell in built]
    return DqdvOut(basis=used, basis_label=basis_label(used),
                   requested_basis=basis, mixed_basis=mixed,
                   resolved_cell=resolved_cell_out(shown_cell), series=series,
                   voltage_step=voltage_step, smoothing=smoothing,
                   smoother=smoother, poly_order=poly_order)


@router.get("/compare/dvdq", response_model=DvdqOut)
def compare_dvdq(
    session: Session = Depends(get_session),
    sample_ids: str = Query(...),
    cycle: int = Query(..., ge=1),
    branches: str = Query("discharge"),
    basis: str = Query(Basis.ABSOLUTE),
    capacity_step: float | None = Query(None, gt=0),
    smoothing: int = Query(DEFAULT_SMOOTHING, ge=1, le=101),
    smoother: str = Query(DEFAULT_SMOOTHER, description="moving | savgol"),
    poly_order: int = Query(DEFAULT_POLY_ORDER, ge=0, le=6),
    max_points: int | None = Query(None, ge=50, le=20000),
):
    """The same cycle's dV/dQ from several cells, overlaid.

    ``capacity_step`` is left free rather than forced: cells of different sizes
    each get a grid scaled to their own capacity, which is what makes their
    curves the same *shape* and comparable at all.  Pin it in mAh when the
    cells really are the same size and the absolute x positions matter.
    """
    validate_basis(basis)
    _validate_smoother(smoother)
    ids = _compare_ids(sample_ids)
    requested_branches = _parse_branches(branches)
    limit = max_points or settings.default_plot_points

    built, used, mixed, shown_cell = _compare_differential(
        session, ids, cycle, requested_branches, basis,
        lambda run, record, branch, cell: dvdq_series(
            run, record, branch, cell, basis, capacity_step=capacity_step,
            smoothing=smoothing, smoother=smoother, poly_order=poly_order,
            max_points=limit))

    series = [DvdqSeriesOut(**payload, run_id=run.id,
                            label=f"{sample.name} · cycle {cycle} {branch}")
              for payload, run, sample, branch, _cell in built]
    return DvdqOut(basis=used, basis_label=basis_label(used),
                   requested_basis=basis, mixed_basis=mixed,
                   resolved_cell=resolved_cell_out(shown_cell), series=series,
                   smoothing=smoothing, smoother=smoother,
                   poly_order=poly_order, capacity_step=capacity_step)


@router.get("/dashboard")
def dashboard(session: Session = Depends(get_session),
              group_id: int | None = None,
              basis: str = Query(Basis.ABSOLUTE)):
    """One line per cell: state, latest capacity, retention, initial CE, knee."""
    validate_basis(basis)
    statement = select(Sample)
    if group_id is not None:
        statement = statement.where(Sample.group_id == group_id)
    samples = session.exec(statement.order_by(Sample.name)).all()

    rows = []
    for sample in samples:
        cell = resolve_cell(sample)
        report = build_cell_report(session, sample)
        used = effective_basis(cell, basis)
        knee = report.knee.primary if report.knee else None

        # A retention percentage says where the cell is; the shape says how it
        # got there.  A handful of points draws that inside a table cell and
        # keeps the payload small with fifty cells listed.
        complete = [r for r in sample_cycle_records(session, sample) if r.complete]
        trend = _trend(complete, report.reference.cycle if report.reference else None)

        rows.append({
            "trend": trend["values"],
            "trend_cycles": trend["cycles"],
            "trend_first_cycle": trend["first_cycle"],
            "trend_last_cycle": trend["last_cycle"],
            "knee_trend_index": _trend_index(
                trend, knee.cycle if knee and knee.detected else None),
            "sample_id": sample.id,
            "sample_name": sample.name,
            "group_id": sample.group_id,
            # The group's own name, so the board can show it without a second
            # request and can count cells per group without asking the server
            # again for every chip.
            "group_name": sample.group.name if sample.group else "",
            "group_color": sample.group.color if sample.group else "",
            "cathode_type": sample.cathode_type,
            "c_rate": sample.c_rate,
            "temperature_c": sample.temperature_c,
            "test_date": sample.test_date,
            "state": report.state,
            "state_confidence": report.state_confidence,
            "in_progress_cycle": report.in_progress_cycle,
            "cycles_complete": report.cycles_complete,
            "reported_cycle": report.reported.cycle if report.reported else None,
            "discharge_capacity": normalized(
                report.reported.discharge_mah, cell, used) if report.reported else None,
            "discharge_capacity_mah": report.reported.discharge_mah if report.reported else None,
            "retention_pct": report.retention_pct,
            "reference_cycle": report.reference.cycle if report.reference else None,
            "reference_available": report.reference_available,
            "initial_coulombic_efficiency": report.initial_coulombic_efficiency,
            # `null` for anything but a confirmed knee collapsed the four
            # states the core works to keep apart back into two, on the one
            # screen that compares cells side by side.  A cell whose knee is
            # unconfirmed for want of cycles looked exactly like a cell that
            # never bent.
            "knee_cycle": knee.cycle if knee and knee.detected else None,
            "knee_method": knee.method if knee and knee.detected else None,
            "knee_status": knee.status if knee else None,
            "knee_candidate_cycle": knee.candidate_cycle if knee else None,
            "knee_reason": knee.reason if knee else "",
            "basis": used,
            # Without this a mass-less cell's raw mAh sits in the same column
            # as the other cells' mAh/g, under one mAh/g header.
            "basis_fallback_reason": cell.missing_for(basis) if used != basis else None,
            "loading_mg_cm2": cell.loading_mg_cm2,
            "composition_label": cell.composition_compact_label,
            # 이 셀이 누구 것인지.  한 서버를 여럿이 쓰면 표에서 남의 셀과 내
            # 셀이 섞이는데, 이름이 없으면 열어 봐야 안다 (ADR 0012).
            "owner": sample.created_by or "",
        })

    used_bases = {row["basis"] for row in rows}
    response_basis = next(iter(used_bases)) if len(used_bases) == 1 else basis
    return {"basis": response_basis, "basis_label": basis_label(response_basis),
            "requested_basis": basis,
            "mixed_basis": len(used_bases) > 1,
            "rows": rows}


#: Points in a dashboard sparkline.  Enough to show a knee, small enough that
#: fifty cells stay a modest payload.
_TREND_POINTS = 28


def _trend(records: list[CycleRecord], reference_cycle: int | None) -> dict:
    """Retention against the reference cycle, thinned to a drawable series."""
    usable = [r for r in records if r.discharge_capacity_mah > 0]
    if not usable:
        return {"values": [], "cycles": [], "first_cycle": None, "last_cycle": None}

    reference = next(
        (r for r in usable if r.cycle_number == reference_cycle), usable[0])
    base = reference.discharge_capacity_mah or usable[0].discharge_capacity_mah
    if not base:
        return {"values": [], "cycles": [], "first_cycle": None, "last_cycle": None}

    if len(usable) <= _TREND_POINTS:
        picked = usable
    else:
        step = (len(usable) - 1) / (_TREND_POINTS - 1)
        picked = [usable[round(i * step)] for i in range(_TREND_POINTS)]

    return {
        "values": [round(100.0 * r.discharge_capacity_mah / base, 2) for r in picked],
        # The cycle each point actually belongs to.  Without it the client can
        # only assume even spacing between the first and last, and cycles
        # 3, 4, 100 get drawn at 3, 51.5, 100 -- the shape of the fade and the
        # position of the knee marker both move.  Gaps are normal: a run
        # continues in a file nobody uploaded, or early cycles were discarded.
        "cycles": [r.cycle_number for r in picked],
        "first_cycle": picked[0].cycle_number,
        "last_cycle": picked[-1].cycle_number,
    }


def _trend_index(trend: dict, cycle: float | None) -> int | None:
    """Where a cycle number falls inside the thinned sparkline series.

    Snapped to the nearest point that is actually in the series rather than
    interpolated: the series is thinned, so the knee's own cycle may not be one
    of the points, and interpolating across a gap puts the marker where no
    measurement exists.
    """
    cycles = trend.get("cycles") or []
    if cycle is None or len(cycles) < 2:
        return None
    if cycle < cycles[0] or cycle > cycles[-1]:
        return None
    return min(range(len(cycles)), key=lambda i: abs(cycles[i] - cycle))
