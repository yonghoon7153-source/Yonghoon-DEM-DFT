"""Uploading and managing ``.wrd`` files."""

from __future__ import annotations

import hashlib
import json

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session, select

from wrdkit import WrdError, read_wrd_bytes

from .. import storage
from ..db import get_session
from ..deps import get_run
from ..models import CycleRecord, Run, Sample
from ..schemas import RunOut, RunUpdate
from ..services import (
    apply_schedule_defaults,
    auto_cycle_offset,
    persist_parse,
    renumber_sample_runs,
    schedule_payload,
    sequence_number,
)
from ..settings import settings

router = APIRouter(prefix="/api/runs", tags=["runs"])


def _out(session: Session, run: Run) -> RunOut:
    sample_name = None
    if run.sample_id:
        sample = session.get(Sample, run.sample_id)
        sample_name = sample.name if sample else None
    schedule = json.loads(run.schedule_json) if run.schedule_json else {}
    return RunOut(**run.model_dump(exclude={"schedule_json", "parsed_at"}),
                  sample_name=sample_name, schedule=schedule)


@router.get("", response_model=list[RunOut])
def list_runs(session: Session = Depends(get_session),
              sample_id: int | None = None,
              unassigned: bool = False):
    statement = select(Run)
    if sample_id is not None:
        statement = statement.where(Run.sample_id == sample_id)
    elif unassigned:
        statement = statement.where(Run.sample_id.is_(None))
    runs = session.exec(statement.order_by(Run.start_time.desc())).all()
    return [_out(session, run) for run in runs]


@router.post("/upload", response_model=RunOut, status_code=201)
async def upload_run(
    file: UploadFile = File(...),
    sample_id: int | None = Query(None, description="attach to this sample"),
    session: Session = Depends(get_session),
):
    """Parse a ``.wrd`` and store its summary.

    Uploading the same bytes twice returns the existing run rather than
    creating a duplicate -- the same file often arrives from two machines.
    """
    content = await file.read()
    if not content:
        raise HTTPException(422, "uploaded file is empty")
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(
            413,
            f"file is {len(content) / 1e6:.0f} MB; the limit is "
            f"{settings.max_upload_bytes / 1e6:.0f} MB",
        )

    digest = hashlib.sha256(content).hexdigest()
    existing = session.exec(select(Run).where(Run.sha256 == digest)).first()
    if existing is not None:
        if sample_id is not None and existing.sample_id != sample_id:
            existing.sample_id = sample_id
            session.add(existing)
            session.commit()
            session.refresh(existing)
        return _out(session, existing)

    try:
        wrd = read_wrd_bytes(content, source_name=file.filename or "upload.wrd")
    except WrdError as exc:
        raise HTTPException(422, f"could not read {file.filename!r}: {exc}") from exc

    if sample_id is not None and session.get(Sample, sample_id) is None:
        raise HTTPException(404, f"sample {sample_id} not found")

    storage.store_upload(content, digest)
    run = Run(
        sample_id=sample_id,
        original_name=file.filename or "upload.wrd",
        sha256=digest,
        size_bytes=len(content),
    )
    session.add(run)
    session.commit()
    session.refresh(run)

    run.cycle_offset = auto_cycle_offset(session, sample_id, wrd.metadata.start_time,
                                         run.original_name, exclude_run_id=run.id)
    try:
        persist_parse(session, run, wrd)
    except Exception as exc:  # noqa: BLE001 - surface the failure, keep the upload
        run.parse_error = str(exc)
        session.add(run)
        session.commit()
        raise HTTPException(500, f"parsed the header but failed to store: {exc}") from exc

    if run.sample_id:
        sample = session.get(Sample, run.sample_id)
        if sample and apply_schedule_defaults(sample, schedule_payload(wrd)):
            session.add(sample)

    session.add(run)
    session.flush()
    # Uploading an earlier file after a later one must re-shift the later one.
    renumber_sample_runs(session, run.sample_id)
    session.commit()
    session.refresh(run)
    return _out(session, run)


@router.get("/{run_id}", response_model=RunOut)
def read_run(run_id: int, session: Session = Depends(get_session)):
    return _out(session, get_run(session, run_id))


@router.patch("/{run_id}", response_model=RunOut)
def update_run(run_id: int, payload: RunUpdate,
               session: Session = Depends(get_session)):
    """Attach a run to a sample, or correct its cycle offset."""
    run = get_run(session, run_id)
    values = payload.model_dump(exclude_unset=True)

    if payload.detach_sample:
        run.sample_id = None
    elif "sample_id" in values and values["sample_id"] is not None:
        if session.get(Sample, values["sample_id"]) is None:
            raise HTTPException(404, f"sample {values['sample_id']} not found")
        run.sample_id = values["sample_id"]
        if "cycle_offset" not in values:
            run.cycle_offset = auto_cycle_offset(session, run.sample_id, run.start_time,
                                                 run.original_name, exclude_run_id=run.id)
            run.cycle_offset_source = "auto"

    if "cycle_offset" in values and values["cycle_offset"] is not None:
        if values["cycle_offset"] < 0:
            raise HTTPException(422, "cycle_offset cannot be negative")
        run.cycle_offset = values["cycle_offset"]
        run.cycle_offset_source = "manual"

    # Cycle numbers are stored, so shifting the offset means rewriting them.
    for record in session.exec(
            select(CycleRecord).where(CycleRecord.run_id == run.id)).all():
        record.cycle_number = record.cycle_index + 1 + run.cycle_offset
        session.add(record)

    session.add(run)
    session.flush()
    renumber_sample_runs(session, run.sample_id)
    session.commit()
    session.refresh(run)
    return _out(session, run)


@router.post("/{run_id}/reparse", response_model=RunOut)
def reparse_run(run_id: int, session: Session = Depends(get_session)):
    """Re-read the stored original -- used after the parser improves."""
    run = get_run(session, run_id)
    try:
        wrd = storage.reparse(run.sha256)
    except FileNotFoundError as exc:
        raise HTTPException(410, str(exc)) from exc
    except WrdError as exc:
        raise HTTPException(422, str(exc)) from exc
    persist_parse(session, run, wrd)
    session.add(run)
    session.commit()
    session.refresh(run)
    return _out(session, run)


@router.delete("/{run_id}", status_code=204)
def delete_run(run_id: int, session: Session = Depends(get_session),
               delete_original: bool = Query(
                   False, description="also remove the stored .wrd (irreversible)")):
    """Remove the run and its cache.  The original is kept unless asked otherwise."""
    run = get_run(session, run_id)
    for record in session.exec(
            select(CycleRecord).where(CycleRecord.run_id == run.id)).all():
        session.delete(record)
    storage.drop_run_cache(run.id)
    digest = run.sha256
    sample_id = run.sample_id
    session.delete(run)
    session.flush()
    renumber_sample_runs(session, sample_id)
    session.commit()

    if delete_original:
        others = session.exec(select(Run).where(Run.sha256 == digest)).first()
        if others is None:
            path = storage.upload_path(digest)
            if path.exists():
                path.unlink()


@router.get("/{run_id}/schedule")
def run_schedule(run_id: int, session: Session = Depends(get_session)):
    """The decoded protocol: steps, cut-offs, C-rate, planned cycles."""
    run = get_run(session, run_id)
    payload = json.loads(run.schedule_json) if run.schedule_json else {}
    return {"run_id": run.id, "sequence": sequence_number(run.original_name),
            **payload}
