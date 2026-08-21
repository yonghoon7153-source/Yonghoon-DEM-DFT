"""누가 무엇을 했는지 — 최근 순으로.

Rows are written by the flush listener in ``db.py``, never by a route, so
this endpoint only reads.  See ADR 0012 for why the names are unverified.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from ..db import get_session
from ..models import Activity
from ..schemas import ActivityOut

router = APIRouter(prefix="/api/activity", tags=["activity"])


@router.get("", response_model=list[ActivityOut])
def list_activity(
    session: Session = Depends(get_session),
    limit: int = Query(50, ge=1, le=500),
    entity: str | None = None,
    entity_id: int | None = None,
):
    """The feed, newest first.

    ``entity``/``entity_id`` narrow it to one cell's history, which is the
    question people actually ask -- "who changed this mass" beats "what
    happened on Tuesday".
    """
    statement = select(Activity).order_by(Activity.id.desc()).limit(limit)
    if entity:
        statement = statement.where(Activity.entity == entity)
    if entity_id is not None:
        statement = statement.where(Activity.entity_id == entity_id)
    rows = session.exec(statement).all()
    return [
        ActivityOut(
            **row.model_dump(exclude={"fields"}),
            fields=[f for f in row.fields.split(",") if f],
        )
        for row in rows
    ]
