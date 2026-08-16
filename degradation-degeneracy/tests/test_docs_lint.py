"""문서 lint — 인용 가능한 현행 문서에 철회된 주장이 남아 있지 않은가.

★ 17차 발견 8 — `RESULTS*.md` 만 고쳐도 저장소를 여는 사람은
`docs/05_HANDOFF.md` 의 철회 전 결론을 현행 답으로 인용할 수 있다.
`RESULTS*.md` 는 생성물이라 코드 회귀로 지켜지지만, 손으로 쓴 문서는
지켜주는 것이 없었다.

이 lint 는 문구 금지가 아니라 **구조 검사**다: 철회된 명제가 나오는 절에는
같은 절 안에 철회 표시가 있어야 한다. 역사 기록을 지우라는 뜻이 아니라,
철회 표시 없이 현행 답처럼 두지 말라는 뜻이다.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parent.parent / "docs"

#: 철회 표시로 인정하는 토큰 (같은 절 안에 있어야 한다)
RETRACTION = "⛔ 철회"

#: (이름, 정규식) — 적대적 리뷰가 철회를 요구한 명제들
RETRACTED = [
    ("사건률 비를 posterior 로 읽음", re.compile(r"46\s*:\s*1|실제로 비슷하게 열화")),
    ("22p 근방이 모두 PE=NE 라는 거짓 전제", re.compile(r"애초에\s*`?LAM_PE\s*=\s*LAM_NE")),
    ("eligibility rule 을 '원리적 복원 불가' 로 확장",
     re.compile(r"원리적으로\s*\*{0,2}\s*복원\s*불가")),
    ("raw 반대부호를 실제 상쇄 감소로 해석",
     re.compile(r"상쇄\s*(지문)?\s*(이|을|가)?\s*68%?\s*→\s*48%?|상쇄 지문을 옅게")),
    ("Case 1/2 를 reference 단독 인과로 귀속",
     re.compile(r"기준 곡선(만|이)\s*.{0,12}(원인|때문)")),
]

#: 인용 가능한 현행 문서 — 여기에 철회 명제가 표시 없이 있으면 실패
ACTIVE_DOCS = ["05_HANDOFF.md"]


def _sections(text: str):
    """(제목줄 index, 본문 줄 목록) 로 자른다 — 마크다운 heading 기준."""
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if re.match(r"^#{1,6}\s", ln)]
    starts = [0] + starts if starts and starts[0] != 0 else starts or [0]
    bounds = list(zip(starts, starts[1:] + [len(lines)]))
    return [(a, lines[a:b]) for a, b in bounds]


@pytest.mark.parametrize("name", ACTIVE_DOCS)
def test_active_doc_has_no_unmarked_retracted_claim(name):
    path = DOCS / name
    if not path.exists():
        pytest.skip(f"{name} 없음")
    text = path.read_text(encoding="utf-8")

    # 문서 최상단에 폐기/정정 안내가 있는가 (독자가 먼저 본다)
    head = "\n".join(text.splitlines()[:40])
    assert RETRACTION in head, (
        f"{name} 최상단에 철회 안내가 없다 — 저장소를 여는 사람이 철회 전 "
        f"결론을 먼저 읽는다")

    bad = []
    for start, body in _sections(text):
        blob = "\n".join(body)
        if RETRACTION in blob:
            continue                      # 이 절은 철회 표시가 되어 있다
        for label, rx in RETRACTED:
            m = rx.search(blob)
            if m:
                off = blob[:m.start()].count("\n")
                bad.append(f"{name}:{start + off + 1} [{label}] {m.group(0)!r}")
    assert not bad, (
        "철회 표시 없는 절에 철회된 주장이 남아 있다:\n  " + "\n  ".join(bad))
