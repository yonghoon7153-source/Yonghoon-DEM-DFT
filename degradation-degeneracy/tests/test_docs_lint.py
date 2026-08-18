"""문서 lint — 인용 가능한 현행 문서에 철회된 주장이 남아 있지 않은가.

★ 17차 발견 8 / 18차 발견 5 — `RESULTS*.md` 만 고쳐도 저장소를 여는 사람은
`docs/05_HANDOFF.md` 나 `docs/GATE14_CYCLE_SUMMARY.md` 의 철회 전 결론을 현행
답으로 인용할 수 있다. `RESULTS*.md` 는 생성물이라 코드 회귀로 지켜지지만,
손으로 쓴 문서는 지켜주는 것이 없었다.

18차가 지적한 1차 lint 의 한계를 모두 고친다.

1. fenced code 안의 `#` 를 heading 으로 오인하지 않는다
2. 절에 마커 하나만 있으면 그 절 전체를 건너뛰던 것을 **claim ID 별 마커**로
3. 정확히 한 문구만 찾던 regex 를 동의어까지 포함하도록
4. Hessian 순위·합성 하한 주장에 대한 rule 추가
5. 최신 문구에 대한 **positive assertion** (정본 링크가 실제로 있는가)
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parent.parent / "docs"

#: 철회 마커 — claim ID 를 함께 적어야 그 claim 만 면제된다
#:   예)  > ⛔ 철회[LR_POSTERIOR] — …
MARKER = re.compile(r"⛔\s*철회\[([A-Z0-9_]+)\]")

#: claim_id → 철회된 명제를 잡는 정규식 (동의어 포함)
RETRACTED = {
    "LR_POSTERIOR": re.compile(
        r"46\s*:\s*1|실제로 비슷하게 열화|우도비.{0,20}(쪽|입니다)"),
    "P22_ALL_EQUAL": re.compile(
        r"애초에\s*`?LAM_PE\s*=\s*LAM_NE|근방.{0,20}참값이\s*(전부|모두)\s*같"),
    "PRINCIPALLY_UNRECOVERABLE": re.compile(
        r"원리적으로\s*\*{0,2}\s*(복원\s*불가|정답이\s*안\s*나)"
        r"|feasible domain\s*밖"),
    "ANTISYM_AS_IMPROVEMENT": re.compile(
        r"상쇄\s*(지문)?\s*(이|을|가)?\s*68%?\s*→\s*48%?|상쇄 지문을 옅게"),
    "REFERENCE_SOLE_CAUSE": re.compile(r"기준 곡선(만|이)\s*.{0,12}(원인|때문)"),
    #: ★ 18차 발견 5 — 아래 둘은 1차 lint 에 rule 이 없었다
    "HESSIAN_EPS_ORDER": re.compile(r"같은\s*eps\s*에서의\s*\*{0,2}순서"),
    "SYNTHETIC_IS_LOWER_BOUND": re.compile(
        r"(하한|lower bound).{0,24}실제.{0,12}(더\s*나쁨|나쁩|나쁘)"),
    #: 철회된 수치를 copy-ready 로 권하는 것도 같은 실패 모드다
    "STALE_GAP_NUMBERS": re.compile(r"36/98|61/156|3\.69|(?<![\d.])90\.0(?![\d])"),
}

#: 손으로 쓴 현행 문서 — 표시 없는 철회 명제가 있으면 실패
ACTIVE_DOCS = ["05_HANDOFF.md", "GATE14_CYCLE_SUMMARY.md"]

#: **생성물** 정본 — 마커가 아니라 positive assertion 으로 지킨다.
#: ★ 18차 Q4 4층. 생성 코드에는 회귀가 붙어 있지만, 커밋된 산출물 자체가
#: 최신 생성기로 만들어졌는지는 아무도 안 봤다. 옛 보고서를 커밋해 두고
#: 코드만 고치면 저장소의 정본은 여전히 철회된 문장을 말한다.
GENERATED_DOCS = ["RESULTS.md", "RESULTS_PAIRED_FIXED5.md"]

#: 생성물 정본에 **반드시** 있어야 하는 provenance 앵커
REQUIRED_ANCHORS = (
    "artifact producer git/source_digest",
    "report generator git/source_digest/dirty",
    "앵커 fits_sha256",
)

#: 정본 링크 — 현행 문서는 정본을 가리켜야 한다 (positive assertion)
CANON = "docs/RESULTS.md"


def _strip_fences(lines: list[str]) -> list[bool]:
    """줄별 "fenced code 안인가" — ★ 18차 발견 5 (1) heading 오인 방지."""
    inside, out, fence = False, [], None
    for ln in lines:
        m = re.match(r"^\s*(`{3,}|~{3,})", ln)
        if m and not inside:
            inside, fence = True, m.group(1)[0]
            out.append(True)
            continue
        if m and inside and m.group(1)[0] == fence:
            inside = False
            out.append(True)
            continue
        out.append(inside)
    return out


def _sections(text: str):
    """(시작줄, 줄목록) — fenced code 밖의 heading 만 절 경계로 본다."""
    lines = text.splitlines()
    in_code = _strip_fences(lines)
    starts = [i for i, ln in enumerate(lines)
              if re.match(r"^#{1,6}\s", ln) and not in_code[i]]
    if not starts or starts[0] != 0:
        starts = [0] + starts
    bounds = list(zip(starts, starts[1:] + [len(lines)]))
    return [(a, lines[a:b]) for a, b in bounds]


@pytest.mark.parametrize("name", ACTIVE_DOCS)
def test_active_doc_points_at_the_canonical_source(name):
    """★ positive assertion — 현행 문서가 정본을 실제로 가리키는가."""
    path = DOCS / name
    if not path.exists():
        pytest.skip(f"{name} 없음")
    head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:60])
    assert MARKER.search(head) or "⛔" in head, (
        f"{name} 최상단에 철회/폐기 안내가 없다")
    assert CANON in head, f"{name} 최상단이 정본({CANON})을 가리키지 않는다"


@pytest.mark.parametrize("name", ACTIVE_DOCS)
def test_active_doc_has_no_unmarked_retracted_claim(name):
    """★ claim ID 별 마커 — 절에 마커 하나 있다고 전부 면제되지 않는다."""
    path = DOCS / name
    if not path.exists():
        pytest.skip(f"{name} 없음")
    text = path.read_text(encoding="utf-8")

    bad = []
    for start, body in _sections(text):
        blob = "\n".join(body)
        marked = set(MARKER.findall(blob))
        for claim_id, rx in RETRACTED.items():
            if claim_id in marked:
                continue                  # 이 claim 은 이 절에서 철회 표시됨
            m = rx.search(blob)
            if m:
                off = blob[:m.start()].count("\n")
                bad.append(f"{name}:{start + off + 1} [{claim_id}] {m.group(0)!r}")
    assert not bad, (
        "철회 표시(⛔ 철회[CLAIM_ID]) 없는 절에 철회된 주장이 남아 있다:\n  "
        + "\n  ".join(bad))


@pytest.mark.parametrize("name", GENERATED_DOCS)
def test_generated_report_has_no_retracted_claim(name):
    """★ 18차 Q4 4층 — 커밋된 정본 보고서에 철회 명제가 있으면 안 된다.

    생성 코드 회귀(`tests/test_report_matrix.py`)는 **새로 만든** 문서를 본다.
    저장소에 커밋돼 있는 파일이 그 코드로 만들어졌는지는 별개 문제다.
    """
    path = DOCS / name
    if not path.exists():
        pytest.skip(f"{name} 없음")
    text = path.read_text(encoding="utf-8")

    bad = []
    for claim_id, rx in RETRACTED.items():
        if claim_id == "STALE_GAP_NUMBERS":
            continue          # 수치는 아래 별도 검사에서 본다
        m = rx.search(text)
        if m:
            bad.append(f"[{claim_id}] {m.group(0)!r}")
    assert not bad, f"{name} 에 철회된 주장이 남아 있다: {bad}"


@pytest.mark.parametrize("name", GENERATED_DOCS)
def test_generated_report_carries_its_provenance_anchors(name):
    """★ positive assertion — 정본은 자기 근거를 밝혀야 한다."""
    path = DOCS / name
    if not path.exists():
        pytest.skip(f"{name} 없음")
    text = path.read_text(encoding="utf-8")

    missing = [a for a in REQUIRED_ANCHORS if a not in text]
    assert not missing, f"{name} 에 provenance 앵커가 없다: {missing}"
    assert "인용 금지" not in text, (
        f"{name} 가 인용 금지 배너를 단 채 커밋돼 있다")


@pytest.mark.parametrize("name", GENERATED_DOCS)
def test_generated_report_uses_the_current_gap_numbers(name):
    """★ 커밋된 정본이 **경계 규약 수정 이후** 값을 쓰는가.

    17차 발견 1 이전 값(`36/98`·`90.0`·`61/156`·`3.69`)이 남아 있으면 그
    파일은 옛 생성기 산출물이다.
    """
    path = DOCS / name
    if not path.exists():
        pytest.skip(f"{name} 없음")
    text = path.read_text(encoding="utf-8")

    m = RETRACTED["STALE_GAP_NUMBERS"].search(text)
    assert not m, (f"{name} 가 경계 수정 이전 수치를 쓴다: {m.group(0)!r} — "
                   f"봉인 fits 에서 score → compare → report 를 다시 돌릴 것")
