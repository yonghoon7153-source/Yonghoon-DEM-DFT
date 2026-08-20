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


def _rewrite_cycle_numbers(session: Session, run: Run) -> None:
    """Cycle numbers are stored, so shifting the offset means rewriting them."""
    for record in session.exec(
            select(CycleRecord).where(CycleRecord.run_id == run.id)).all():
        record.cycle_number = record.cycle_index + 1 + run.cycle_offset
        session.add(record)


def _attach_to_sample(session: Session, run: Run, sample_id: int) -> None:
    """Move an unassigned run into a sample, offsets and numbering included.

    Every path that changes which sample a run belongs to has to do all of
    this; attaching without the offset recomputation leaves two files of one
    sample numbering their cycles from the same base.
    """
    if session.get(Sample, sample_id) is None:
        raise HTTPException(404, f"sample {sample_id} not found")
    run.sample_id = sample_id
    if run.cycle_offset_source != "manual":
        run.cycle_offset = auto_cycle_offset(session, sample_id, run.start_time,
                                             run.original_name, exclude_run_id=run.id)
        run.cycle_offset_source = "auto"
    _rewrite_cycle_numbers(session, run)
    session.add(run)
    session.flush()
    renumber_sample_runs(session, sample_id)


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
    # Starlette has already spooled the body, but reading it turns the whole
    # upload into one bytes object -- refuse before that allocation.  Rejecting
    # before the body arrives at all would need middleware, which is outside
    # this router.
    if file.size is not None and file.size > settings.max_upload_bytes:
        raise HTTPException(
            413,
            f"file is {file.size / 1e6:.0f} MB; the limit is "
            f"{settings.max_upload_bytes / 1e6:.0f} MB",
        )

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
            if existing.sample_id is not None:
                # Re-uploading the same bytes must not move a run out of the
                # sample it already belongs to: the old sample would lose a
                # file without a word, and both samples' cycle numbering would
                # shift.  Moving is an explicit request -- PATCH does it.
                raise HTTPException(
                    409,
                    f"run {existing.id} already belongs to sample "
                    f"{existing.sample_id}; use PATCH /api/runs/{existing.id} "
                    "to move it",
                )
            _attach_to_sample(session, existing, sample_id)
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
    # Kept because the rollback below detaches ``run`` from the session.
    run_id_before_parse = run.id
    try:
        persist_parse(session, run, wrd)
    except Exception as exc:  # noqa: BLE001 - surface the failure, keep the upload
        # Roll back before recording anything.  persist_parse stages the run's
        # metadata and every CycleRecord before it can fail; committing that
        # session publishes a half-written cycle table and skips the renumber
        # below, so the sample keeps a run whose cycles overlap its neighbours
        # and nothing says why.  The original bytes are already on disk under
        # their hash, so the upload itself is not lost -- only the parse is,
        # and that is what the error field is for.
        session.rollback()
        failed = session.get(Run, run_id_before_parse)
        if failed is not None:
            failed.parse_error = str(exc)
            failed.cycle_count = 0
            failed.complete_cycle_count = 0
            session.add(failed)
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


def _overlapping_run(session: Session, run: Run, offset: int) -> Run | None:
    """A sibling run whose cycle numbers would collide with *run* at *offset*.

    Cycle numbers are 1-based within a run and shifted by the offset, so a run
    covers ``offset+1 .. offset+cycle_count``.  Two such ranges may touch but
    not overlap.
    """
    if run.sample_id is None or not run.cycle_count:
        return None
    start, end = offset + 1, offset + run.cycle_count
    siblings = session.exec(
        select(Run).where(Run.sample_id == run.sample_id, Run.id != run.id)).all()
    for other in siblings:
        if not other.cycle_count:
            continue
        other_start = other.cycle_offset + 1
        other_end = other.cycle_offset + other.cycle_count
        if start <= other_end and other_start <= end:
            return other
    return None


@router.patch("/{run_id}", response_model=RunOut)
def update_run(run_id: int, payload: RunUpdate,
               session: Session = Depends(get_session)):
    """Attach a run to a sample, or correct its cycle offset."""
    run = get_run(session, run_id)
    values = payload.model_dump(exclude_unset=True)
    previous_sample_id = run.sample_id

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
        # A hand-set offset is honoured, but not blindly: two runs of one
        # sample numbering the same cycles makes "cycle 3" ambiguous, and
        # which one answers depends on query order.  The reference cycle and
        # every profile pick would then change between two identical requests.
        clash = _overlapping_run(session, run, values["cycle_offset"])
        if clash is not None:
            raise HTTPException(
                422,
                f"cycle_offset {values['cycle_offset']} makes this run overlap "
                f"run {clash.id} ({clash.original_name}), which covers cycles "
                f"{clash.cycle_offset + 1}-{clash.cycle_offset + clash.cycle_count}")
        run.cycle_offset = values["cycle_offset"]
        run.cycle_offset_source = "manual"

    _rewrite_cycle_numbers(session, run)

    session.add(run)
    session.flush()
    renumber_sample_runs(session, run.sample_id)
    # The sample the run just left has to close the gap too, or its remaining
    # files keep offsets that counted the departed run's cycles.
    if previous_sample_id is not None and previous_sample_id != run.sample_id:
        renumber_sample_runs(session, previous_sample_id)
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
    session.flush()
    # A better parser can change this file's cycle count, which moves every
    # later file of the same sample.
    renumber_sample_runs(session, run.sample_id)
    session.commit()
    session.refresh(run)
    return _out(session, run)


@router.delete("/{run_id}", status_code=204)
def delete_run(run_id: int, session: Session = Depends(get_session)):
    """Remove the run row and its parse cache.

    The original ``.wrd`` in ``data/uploads/`` stays: it is the one thing
    nothing can rebuild, and both non-negotiable #2 and ADR 0003 promise it is
    never removed.  The endpoint used to take ``delete_original=true`` and
    unlink it, which broke that promise and the reparse recovery path with it.
    """
    run = get_run(session, run_id)
    for record in session.exec(
            select(CycleRecord).where(CycleRecord.run_id == run.id)).all():
        session.delete(record)
    storage.drop_run_cache(run.id)
    sample_id = run.sample_id
    session.delete(run)
    session.flush()
    renumber_sample_runs(session, sample_id)
    session.commit()


@router.get("/{run_id}/schedule")
def run_schedule(run_id: int, session: Session = Depends(get_session)):
    """The decoded protocol: steps, cut-offs, C-rate, planned cycles."""
    run = get_run(session, run_id)
    payload = json.loads(run.schedule_json) if run.schedule_json else {}
    return {"run_id": run.id, "sequence": sequence_number(run.original_name),
            **payload}
