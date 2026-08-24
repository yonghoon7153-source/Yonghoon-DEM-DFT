"""패치노트 — `docs/log.md` 를 화면이 읽을 수 있는 모양으로.

**두 번째 목록을 만들지 않는다.**  "무엇이 바뀌었나" 를 쓰는 자리가 이미 있고
(`docs/log.md`), 커밋마다 한 줄을 남기는 규율이 그것을 최신으로 유지한다
(`bml feed` 가 빠진 것을 세어 준다).  화면용 changelog 를 따로 두면 반드시
한쪽만 갱신되고, 그때 사람이 보는 쪽이 틀린 쪽이 된다.

형식은 `docs/SCHEMA.md` 가 정한다::

    ## [YYYY-MM-DD] action | subject
    (다음 ## 까지가 본문)

파일은 append-only 이므로 **아래쪽이 최신**이다.  뒤집어서 준다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

#: `## [2026-08-24] fix | 제목` — 날짜·action·제목.
#:
#: action 을 목록으로 못 박지 않는다.  실제 파일에는 문서가 적어 둔 일곱 개
#: 말고도 `feat` 과 `docs` 가 들어와 있고, 목록에 없다고 항목을 버리면 그
#: 커밋만 패치노트에서 조용히 사라진다 — 기록을 읽는 쪽이 기록을 검열하면 안
#: 된다.  모르는 action 은 모르는 대로 넘긴다 (화면이 중립 색으로 그린다).
_HEADING = re.compile(r"^##\s+\[(\d{4}-\d{2}-\d{2})\]\s+([A-Za-z]+)\s*\|\s*(.+?)\s*$")


@dataclass(frozen=True)
class ChangeNote:
    date: str
    action: str
    subject: str
    #: 커밋 메시지에 안 들어간 것 — 무엇을 보고 그렇게 판단했는지, 실측 값,
    #: 일부러 남긴 것.  없을 수도 있다 (한 줄짜리 항목).
    body: str


def parse_log(text: str) -> list[ChangeNote]:
    """`docs/log.md` 본문을 최신 순으로.

    제목 줄이 아닌 앞머리(파일 설명, 형식 안내)는 어느 항목에도 붙지 않는다 --
    첫 제목을 만나기 전의 줄은 버린다.
    """
    notes: list[ChangeNote] = []
    date = action = subject = ""
    body: list[str] = []
    started = False

    def flush() -> None:
        if started:
            notes.append(ChangeNote(date, action, subject, "\n".join(body).strip()))

    for line in text.splitlines():
        match = _HEADING.match(line)
        if match:
            flush()
            started = True
            date, action, subject = match.group(1), match.group(2).lower(), match.group(3)
            body = []
            continue
        # `# 작업 로그` 같은 다른 제목은 항목을 끝내지 않는다 -- 본문 안의
        # `###` 소제목까지 항목을 끊으면 한 항목이 여러 개로 쪼개진다.
        if started:
            body.append(line)
    flush()

    notes.reverse()  # append-only 파일이라 아래쪽이 최신이다.
    return notes


def read_notes(path: Path, limit: int) -> list[ChangeNote]:
    """파일에서 읽는다.  없으면 빈 목록 -- 지어내지 않는다.

    배포된 서버에 `docs/` 가 없을 수 있다 (저장소를 통째로 두는 것이 지금
    방식이지만, 그것이 계약은 아니다).  그때 화면은 "기록이 없습니다" 를 보여
    주면 되고, 그것은 거짓이 아니다.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    return parse_log(text)[:limit]
