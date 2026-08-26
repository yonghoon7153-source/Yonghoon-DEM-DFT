"""쓰다가 걸린 것을 겪은 자리에 적는 칸 (ADR 0033).

로그인이 없으므로 (ADR 0012) 누가 지우는지도 검증하지 않는다.  두 사람이 쓰는
저장소에서 남의 글을 지우는 것을 막을 방법도, 막아야 할 이유도 없다 -- 실수로
지운 것이 문제라면 그건 `Activity` 에 남는다.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..actor import current_actor
from ..db import get_session
from ..models import FeedbackNote, FeedbackReply
from ..schemas import (
    FeedbackNoteIn,
    FeedbackNoteOut,
    FeedbackNoteUpdate,
    FeedbackReplyIn,
    FeedbackReplyOut,
)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

#: 한 항목이 얼마나 길 수 있나.  막는 것이 목적이 아니라, 실수로 파일을 통째로
#: 붙여 넣었을 때 데이터베이스가 그것을 그대로 삼키지 않게 하는 것이 목적이다.
MAX_BODY = 4000
KINDS = frozenset({"issue", "question", "idea"})


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _clean(body: str) -> str:
    text = (body or "").strip()
    if not text:
        raise HTTPException(422, "내용이 비어 있습니다")
    if len(text) > MAX_BODY:
        raise HTTPException(422, f"{MAX_BODY}자까지 적을 수 있습니다 (지금 {len(text)}자)")
    return text


def _out(session: Session, note: FeedbackNote) -> FeedbackNoteOut:
    replies = session.exec(
        select(FeedbackReply)
        .where(FeedbackReply.note_id == note.id)
        .order_by(FeedbackReply.id)
    ).all()
    return FeedbackNoteOut(
        **note.model_dump(exclude={"updated_by"}),
        replies=[FeedbackReplyOut(**r.model_dump(exclude={"updated_by"})) for r in replies],
    )


@router.get("", response_model=list[FeedbackNoteOut])
def list_notes(session: Session = Depends(get_session),
               include_resolved: bool = Query(True)):
    """열린 것이 위, 그 안에서 최근 것이 위.

    정리된 항목을 목록에서 **빼지 않는 이유**: 같은 불편이 두 달 뒤에 다시
    올라올 때 "그때 이렇게 정리했다" 가 보여야 한다.  대신 아래로 내린다.
    """
    statement = select(FeedbackNote)
    if not include_resolved:
        statement = statement.where(FeedbackNote.resolved_at.is_(None))
    notes = session.exec(statement).all()
    # 두 번 정렬한다: 최근 순으로 한 번, 그다음 열린 것이 위로.  파이썬 sort 가
    # 안정 정렬이라 각 무리 안에서 최근 순이 남는다.
    notes = sorted(notes, key=lambda n: n.created_at, reverse=True)
    notes.sort(key=lambda n: n.resolved_at is not None)
    return [_out(session, note) for note in notes]


@router.post("", response_model=FeedbackNoteOut, status_code=201)
def create_note(payload: FeedbackNoteIn, session: Session = Depends(get_session)):
    if payload.kind not in KINDS:
        raise HTTPException(422, f"kind 는 {sorted(KINDS)} 중 하나입니다")
    note = FeedbackNote(kind=payload.kind, body=_clean(payload.body))
    session.add(note)
    session.commit()
    session.refresh(note)
    return _out(session, note)


@router.patch("/{note_id}", response_model=FeedbackNoteOut)
def update_note(note_id: int, payload: FeedbackNoteUpdate,
                session: Session = Depends(get_session)):
    """고치기 · 정리하기 · 다시 열기 — 셋이 한 창구다.

    `resolved` 를 되돌릴 수 있게 두는 것이 중요하다.  잘못 눌러서 접힌 항목을
    되살릴 길이 없으면, 사람은 접는 버튼 자체를 안 누른다.
    """
    note = session.get(FeedbackNote, note_id)
    if note is None:
        raise HTTPException(404, f"note {note_id} not found")
    if payload.kind is not None:
        if payload.kind not in KINDS:
            raise HTTPException(422, f"kind 는 {sorted(KINDS)} 중 하나입니다")
        note.kind = payload.kind
    if payload.body is not None:
        note.body = _clean(payload.body)
    if payload.resolved is not None:
        if payload.resolved:
            note.resolved_at = note.resolved_at or _now()
            note.resolved_by = current_actor()
        else:
            note.resolved_at = None
            note.resolved_by = ""
    note.updated_at = _now()
    session.add(note)
    session.commit()
    session.refresh(note)
    return _out(session, note)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    """항목을 지우면 그 아래 답글도 같이 간다 -- 답글만 남으면 무엇에 대한
    답인지 알 수 없다."""
    note = session.get(FeedbackNote, note_id)
    if note is None:
        raise HTTPException(404, f"note {note_id} not found")
    for reply in session.exec(
            select(FeedbackReply).where(FeedbackReply.note_id == note_id)).all():
        session.delete(reply)
    session.delete(note)
    session.commit()


@router.post("/{note_id}/replies", response_model=FeedbackNoteOut, status_code=201)
def add_reply(note_id: int, payload: FeedbackReplyIn,
              session: Session = Depends(get_session)):
    note = session.get(FeedbackNote, note_id)
    if note is None:
        raise HTTPException(404, f"note {note_id} not found")
    session.add(FeedbackReply(note_id=note_id, body=_clean(payload.body)))
    # 답글이 붙은 것도 그 항목이 움직인 것이다 -- 안 찍으면 알림 점이 안 뜬다.
    note.updated_at = _now()
    session.add(note)
    session.commit()
    session.refresh(note)
    return _out(session, note)


@router.delete("/{note_id}/replies/{reply_id}", status_code=204)
def delete_reply(note_id: int, reply_id: int, session: Session = Depends(get_session)):
    reply = session.get(FeedbackReply, reply_id)
    if reply is None or reply.note_id != note_id:
        raise HTTPException(404, f"reply {reply_id} not found")
    session.delete(reply)
    session.commit()
