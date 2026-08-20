"""CSV and XLSX downloads.

The CSV encoding is UTF-8 with a BOM: Excel on a Korean Windows install
otherwise reads the header row as mojibake, and these files exist to be
opened in Excel.
"""

from __future__ import annotations

import io
import re
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response, StreamingResponse
from sqlmodel import Session

from wrdkit import (
    Basis,
    WrdFile,
    cycles_csv_string,
    extract_profile,
    profiles_csv_string,
    raw_csv_string,
    write_xlsx,
)

from ..db import get_session
from ..deps import get_run, get_sample, validate_basis
from ..models import Sample
from ..services import (
    _metadata_stub,
    _rebuild_steps,
    load_wrd_columns,
    records_to_summaries,
    resolve_cell,
    sample_cycle_records,
)
from .analysis import _parse_cycles

router = APIRouter(prefix="/api/export", tags=["export"])

_BOM = "﻿"


def _safe(name: str) -> str:
    """A filename that survives every OS and HTTP header we hand it to."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return cleaned or "export"


def _csv_response(text: str, filename: str) -> Response:
    return Response(
        content=(_BOM + text).encode("utf-8"),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{_safe(filename)}"'},
    )


@router.get("/runs/{run_id}/raw.csv")
def export_run_raw(run_id: int, session: Session = Depends(get_session)):
    """Every sample of one file -- the direct replacement for hand-exporting."""
    run = get_run(session, run_id)
    columns = load_wrd_columns(run)
    wrd = WrdFile(_metadata_stub(run), columns)
    stem = _safe(run.original_name.rsplit(".", 1)[0])
    return _csv_response(raw_csv_string(wrd), f"{stem}_raw.csv")


@router.get("/samples/{sample_id}/cycles.csv")
def export_sample_cycles(
    sample_id: int,
    session: Session = Depends(get_session),
    basis: str = Query(Basis.ABSOLUTE),
    complete_only: bool = Query(True),
):
    validate_basis(basis)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample)
    records = sample_cycle_records(session, sample)
    if complete_only:
        records = [r for r in records if r.complete]
    summaries = records_to_summaries(records)
    text = cycles_csv_string(summaries, cell, basis=basis)
    return _csv_response(text, f"{_safe(sample.name)}_cycles.csv")


@router.get("/samples/{sample_id}/profiles.csv")
def export_sample_profiles(
    sample_id: int,
    session: Session = Depends(get_session),
    cycles: str = Query("all"),
    branches: str = Query("charge,discharge"),
    basis: str = Query(Basis.ABSOLUTE),
):
    """Column pairs per cycle -- the layout Origin wants for an overlay."""
    validate_basis(basis)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample)
    profiles = _collect_profiles(session, sample, cycles, branches)
    if not profiles:
        raise HTTPException(404, "no complete cycle matched the selection")
    text = profiles_csv_string(profiles, cell, basis=basis)
    return _csv_response(text, f"{_safe(sample.name)}_profiles.csv")


@router.get("/samples/{sample_id}/workbook.xlsx")
def export_sample_workbook(
    sample_id: int,
    session: Session = Depends(get_session),
    cycles: str = Query("all"),
    branches: str = Query("charge,discharge"),
    basis: str = Query(Basis.ABSOLUTE),
    include_raw: bool = Query(False, description="add every sample; makes a large file"),
):
    """A multi-sheet workbook: metadata, cycles, profiles, optionally raw."""
    validate_basis(basis)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample)
    records = [r for r in sample_cycle_records(session, sample) if r.complete]
    if not records:
        raise HTTPException(404, "this sample has no completed cycle yet")

    run = next((r for r in sample.runs if r.id == records[-1].run_id), None)
    if run is None:
        raise HTTPException(404, "the sample's files are missing")
    wrd = WrdFile(_metadata_stub(run), load_wrd_columns(run))
    wrd.metadata.schedule = None

    profiles = _collect_profiles(session, sample, cycles, branches)
    summaries = records_to_summaries(records)

    buffer = io.BytesIO()
    try:
        write_xlsx(buffer, wrd, summaries, profiles, cell, basis=basis,
                   include_raw=include_raw)
    except RuntimeError as exc:
        raise HTTPException(501, str(exc)) from exc
    buffer.seek(0)

    stamp = datetime.now().strftime("%Y%m%d")
    filename = _safe(f"{sample.name}_{stamp}.xlsx")
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def _collect_profiles(session: Session, sample: Sample, cycles: str, branches: str):
    wanted = _parse_cycles(cycles)
    requested = [b.strip() for b in branches.split(",") if b.strip()]
    records = [r for r in sample_cycle_records(session, sample) if r.complete]
    if wanted is not None:
        records = [r for r in records if r.cycle_number in wanted]

    runs = {run.id: run for run in sample.runs}
    profiles = []
    for record in records:
        run = runs.get(record.run_id)
        if run is None:
            continue
        wrd = WrdFile(_metadata_stub(run), load_wrd_columns(run))
        summary = records_to_summaries([record])[0]
        summary.steps = _rebuild_steps(wrd, record)
        for branch in requested:
            profile = extract_profile(wrd, summary, branch)
            if len(profile):
                profiles.append(profile)
    return profiles
