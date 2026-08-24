"""패치노트 — 무엇이 바뀌었나.

`docs/log.md` 를 그대로 읽는다.  왜 두 번째 목록을 안 만드는지는
``app/changelog.py`` 의 머리말에 있다.
"""

from __future__ import annotations

from fastapi import APIRouter, Query

from ..changelog import read_notes
from ..schemas import ChangeNoteOut
from ..settings import settings

router = APIRouter(prefix="/api/changelog", tags=["changelog"])


@router.get("", response_model=list[ChangeNoteOut])
def list_changelog(limit: int = Query(20, ge=1, le=200)) -> list[ChangeNoteOut]:
    """최신 순.  파일이 없으면 빈 목록이다 (없는 것을 지어내지 않는다)."""
    return [
        ChangeNoteOut(date=note.date, action=note.action, subject=note.subject, body=note.body)
        for note in read_notes(settings.changelog_path, limit)
    ]
