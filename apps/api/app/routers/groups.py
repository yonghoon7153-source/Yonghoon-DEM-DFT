"""Experiment groups -- the folders cells get compared inside."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_group, group_scope
from ..models import ExperimentGroup, Run, Sample
from ..schemas import GroupIn, GroupOut, GroupUpdate

router = APIRouter(prefix="/api/groups", tags=["groups"])


def _out(session: Session, group: ExperimentGroup) -> GroupOut:
    scope = group_scope(session, group.id)
    samples = session.exec(select(Sample).where(Sample.group_id.in_(scope))).all()
    sample_ids = [s.id for s in samples]
    runs = 0
    if sample_ids:
        runs = len(session.exec(select(Run).where(Run.sample_id.in_(sample_ids))).all())
    parent_name = ""
    if group.parent_id:
        parent = session.get(ExperimentGroup, group.parent_id)
        parent_name = parent.name if parent else ""
    return GroupOut(**group.model_dump(), sample_count=len(samples), run_count=runs,
                    parent_name=parent_name, subgroup_count=len(scope) - 1)


def _validate_parent(session: Session, group_id: int | None, parent_id: int | None) -> None:
    """Say no to the nestings the two-dropdown UI cannot draw (ADR 0025).

    Depth is capped at two, so three rules cover it: a group cannot be its own
    parent, the parent must itself be top-level, and a group that already
    holds sub-groups cannot be pushed under another one.  Refusing here is the
    point -- a three-deep tree saves fine and then disappears from the screen
    that was supposed to show it.
    """
    if parent_id is None:
        return
    if group_id is not None and parent_id == group_id:
        raise HTTPException(422, "a group cannot be its own sub-group")
    parent = session.get(ExperimentGroup, parent_id)
    if parent is None:
        raise HTTPException(404, f"group {parent_id} not found")
    if parent.parent_id:
        raise HTTPException(
            422,
            f"'{parent.name}' is already a sub-group; groups nest one level only")
    if group_id is not None:
        children = session.exec(
            select(ExperimentGroup).where(ExperimentGroup.parent_id == group_id)).all()
        if children:
            raise HTTPException(
                422,
                f"this group holds {len(children)} sub-group(s), so it cannot "
                f"become one itself; move them out first")


@router.get("", response_model=list[GroupOut])
def list_groups(session: Session = Depends(get_session)):
    groups = session.exec(select(ExperimentGroup).order_by(ExperimentGroup.name)).all()
    return [_out(session, group) for group in groups]


@router.post("", response_model=GroupOut, status_code=201)
def create_group(payload: GroupIn, session: Session = Depends(get_session)):
    if not payload.name.strip():
        raise HTTPException(422, "group name cannot be empty")
    _validate_parent(session, None, payload.parent_id)
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
    fields = payload.model_dump(exclude_unset=True)
    if "parent_id" in fields:
        _validate_parent(session, group_id, fields["parent_id"])
    for key, value in fields.items():
        setattr(group, key, value)
    group.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(group)
    session.commit()
    session.refresh(group)
    return _out(session, group)


@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: int, session: Session = Depends(get_session)):
    """Delete the group only; its samples survive, ungrouped.

    Sub-groups survive too, as top-level groups.  Deleting a folder is not a
    statement about the cells inside it -- and cascading would take out
    everything a whole experiment was sorted into with one click.
    """
    group = get_group(session, group_id)
    for sample in session.exec(select(Sample).where(Sample.group_id == group_id)).all():
        sample.group_id = None
        session.add(sample)
    for child in session.exec(
            select(ExperimentGroup).where(ExperimentGroup.parent_id == group_id)).all():
        child.parent_id = None
        session.add(child)
    session.delete(group)
    session.commit()
