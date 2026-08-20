"""CSV and XLSX downloads.

The CSV encoding is UTF-8 with a BOM: Excel on a Korean Windows install
otherwise reads the header row as mojibake, and these files exist to be
opened in Excel.
"""

from __future__ import annotations

import io
import re
from datetime import datetime

import numpy as np
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
from ..models import Run, Sample
from ..services import (
    _metadata_stub,
    _rebuild_steps,
    load_wrd_columns,
    records_to_summaries,
    resolve_cell,
    run_order_key,
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

    loaded: dict[int, WrdFile] = {}
    wrd = _sample_wrd(sample, loaded, with_data=include_raw)

    profiles = _collect_profiles(session, sample, cycles, branches, loaded)
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


def _wrd_for(run: Run, loaded: dict[int, WrdFile]) -> WrdFile:
    """One run's columns, read from the cache at most once per request.

    Every read decompresses the whole ``.npz``.  Loading inside the per-cycle
    loop made a 500-cycle export decompress the same archive 500 times, and
    these endpoints default to ``cycles=all`` with no cap.
    """
    wrd = loaded.get(run.id)
    if wrd is None:
        wrd = WrdFile(_metadata_stub(run), load_wrd_columns(run))
        loaded[run.id] = wrd
    return wrd


def _sample_wrd(sample: Sample, loaded: dict[int, WrdFile], *,
                with_data: bool) -> WrdFile:
    """The whole sample as one file, for the workbook's metadata and raw sheet.

    A long experiment arrives as ``_011.wrd``, ``_012.wrd`` ... and the
    workbook has a single raw sheet.  Writing only the run that owns the last
    cycle dropped every earlier file's rows without saying so, while the
    cycles sheet still covered them all -- a workbook kept as a stand-in for
    the originals would have been missing half the experiment.
    """
    runs = sorted((r for r in sample.runs if r.id is not None),
                  key=lambda r: run_order_key(r.start_time, r.original_name, r.id))
    if not runs:
        raise HTTPException(404, "the sample's files are missing")

    metadata = _metadata_stub(runs[0])
    metadata.source_name = ", ".join(run.original_name for run in runs)
    metadata.row_count = sum(run.row_count for run in runs)
    if not with_data:
        return WrdFile(metadata, {})

    if len({run.unit_coulomb for run in runs}) > 1:
        raise HTTPException(
            409, "this sample's files disagree on the capacity unit "
                 "(UnitCoulomb), so their raw rows cannot share one sheet; "
                 "export them one file at a time")
    parts = [(run, _wrd_for(run, loaded)) for run in runs]
    if len({tuple(wrd.data) for _, wrd in parts}) > 1:
        raise HTTPException(
            409, "this sample's files record different columns, so their raw "
                 "rows cannot share one sheet; export them one file at a time")

    data = {name: np.concatenate([wrd.data[name] for _, wrd in parts])
            for name in parts[0][1].data}
    # test_time restarts at zero in each file, so without this the reader
    # cannot tell which file a row came from.
    data["source_file"] = np.concatenate([
        np.full(len(next(iter(wrd.data.values()))), run.original_name)
        for run, wrd in parts])
    metadata.row_count = len(data["source_file"])
    return WrdFile(metadata, data)


def _collect_profiles(session: Session, sample: Sample, cycles: str, branches: str,
                      loaded: dict[int, WrdFile] | None = None):
    wanted = _parse_cycles(cycles)
    requested = [b.strip() for b in branches.split(",") if b.strip()]
    records = [r for r in sample_cycle_records(session, sample) if r.complete]
    if wanted is not None:
        records = [r for r in records if r.cycle_number in wanted]

    runs = {run.id: run for run in sample.runs}
    loaded = {} if loaded is None else loaded
    profiles = []
    for record in records:
        run = runs.get(record.run_id)
        if run is None:
            continue
        wrd = _wrd_for(run, loaded)
        summary = records_to_summaries([record])[0]
        summary.steps = _rebuild_steps(wrd, record)
        for branch in requested:
            profile = extract_profile(wrd, summary, branch)
            if len(profile):
                profiles.append(profile)
    return profiles
