"""Experiment groups -- the folders cells get compared inside."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_group
from ..models import ExperimentGroup, Run, Sample
from ..schemas import GroupIn, GroupOut, GroupUpdate

router = APIRouter(prefix="/api/groups", tags=["groups"])


def _out(session: Session, group: ExperimentGroup) -> GroupOut:
    samples = session.exec(select(Sample).where(Sample.group_id == group.id)).all()
    sample_ids = [s.id for s in samples]
    runs = 0
    if sample_ids:
        runs = len(session.exec(select(Run).where(Run.sample_id.in_(sample_ids))).all())
    return GroupOut(**group.model_dump(), sample_count=len(samples), run_count=runs)


@router.get("", response_model=list[GroupOut])
def list_groups(session: Session = Depends(get_session)):
    groups = session.exec(select(ExperimentGroup).order_by(ExperimentGroup.name)).all()
    return [_out(session, group) for group in groups]


@router.post("", response_model=GroupOut, status_code=201)
def create_group(payload: GroupIn, session: Session = Depends(get_session)):
    if not payload.name.strip():
        raise HTTPException(422, "group name cannot be empty")
    group = ExperimentGroup(**payload.model_dump(exclude_unset=True))
    session.add(group)
    session.commit()
    session.refresh(group)
    return _out(session, group)


@router.get("/{group_id}", response_model=GroupOut)
def read_group(group_id: int, session: Session = Depends(get_session)):
    return _out(session, get_group(session, group_id))


@router.patch("/{group_id}", response_model=GroupOut)
def update_group(group_id: int, payload: GroupUpdate,
                 session: Session = Depends(get_session)):
    group = get_group(session, group_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(group, key, value)
    group.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(group)
    session.commit()
    session.refresh(group)
    return _out(session, group)


@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: int, session: Session = Depends(get_session)):
    """Delete the group only; its samples survive, ungrouped."""
    group = get_group(session, group_id)
    for sample in session.exec(select(Sample).where(Sample.group_id == group_id)).all():
        sample.group_id = None
        session.add(sample)
    session.delete(group)
    session.commit()
