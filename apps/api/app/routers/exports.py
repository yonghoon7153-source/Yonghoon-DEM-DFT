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
from fastapi.responses import FileResponse, Response, StreamingResponse
from sqlmodel import Session

from wrdkit import (
    Basis,
    WrdFile,
    cycles_csv_string,
    differential_capacity,
    dqdv_csv_string,
    extract_profile,
    profiles_csv_string,
    raw_csv_string,
    write_xlsx,
)
from wrdkit.ica import DEFAULT_SMOOTHING, DEFAULT_VOLTAGE_STEP  # noqa: E402

from .. import storage
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


@router.get("/runs/{run_id}/original.wrd")
def export_run_original(run_id: int, session: Session = Depends(get_session)):
    """The uploaded ``.wrd``, byte for byte.

    The point of a central instance is that the originals stop living on
    whichever laptop did the measurement.  That only holds if they can be got
    back out again -- otherwise "upload it to the workbench" is a one-way trip
    and nobody will do it with the only copy.

    The bytes are served straight from storage rather than re-serialised: the
    file is immutable by rule (CLAUDE.md §0.2) and its name is its SHA-256, so
    what comes back down is provably what went up.
    """
    run = get_run(session, run_id)
    path = storage.upload_path(run.sha256)
    if not path.exists():
        # Worth naming out loud: with the data directory on an external drive,
        # an unplugged disk looks exactly like a deleted file, and the useful
        # thing to check first is the cable.
        raise HTTPException(
            404,
            f"the original file for {run.original_name} is not in storage "
            f"({path.parent}) -- if the data directory is on an external "
            f"drive, check that it is mounted")
    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=_safe(run.original_name),
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
    summaries = records_to_summaries(records)
    # 거르는 일은 writer 한 곳에서 한다.  라우터가 미리 걸러 놓고 writer 도
    # 기본값으로 거르면, complete_only=false 로 달라고 한 행이 두 번째 체에서
    # 조용히 사라진다 — 요청한 것이 아예 안 나오는데 오류도 없다.
    text = cycles_csv_string(summaries, cell, basis=basis,
                             include_incomplete=not complete_only)
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


@router.get("/samples/{sample_id}/dqdv.csv")
def export_sample_dqdv(
    sample_id: int,
    session: Session = Depends(get_session),
    cycles: str = Query("all"),
    branches: str = Query("charge,discharge"),
    basis: str = Query(Basis.ABSOLUTE),
    voltage_step: float = Query(DEFAULT_VOLTAGE_STEP, gt=0.0001, le=0.2),
    smoothing: int = Query(DEFAULT_SMOOTHING, ge=1, le=101),
):
    """dQ/dV column pairs per cycle, laid out like the profile CSV.

    Written from the full-resolution curve, not the thinned one the plot
    draws.  A CSV is what somebody re-plots or fits against, and a peak
    position taken from a curve reduced for a 900-pixel canvas is accurate to
    the pixel rather than to the grid.
    """
    validate_basis(basis)
    sample = get_sample(session, sample_id)
    cell = resolve_cell(sample)
    profiles = _collect_profiles(session, sample, cycles, branches)
    if not profiles:
        raise HTTPException(404, "no complete cycle matched the selection")

    curves = [differential_capacity(p, voltage_step=voltage_step,
                                    smoothing=smoothing) for p in profiles]
    if not any(c.usable for c in curves):
        # 하나도 못 만들었으면 빈 파일 대신 이유를 준다.  빈 CSV 를 열어 본
        # 사람은 자기가 사이클을 잘못 골랐다고 생각하지, 전압이 안 움직였다고
        # 생각하지 않는다.
        why = next((c.reason for c in curves if c.reason), "no usable branch")
        raise HTTPException(422, f"dQ/dV could not be computed: {why}")

    text = dqdv_csv_string(curves, cell, basis=basis)
    return _csv_response(text, f"{_safe(sample.name)}_dqdv.csv")


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
