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


# ── artifacts/README 가 실제 보관 상태와 어긋나지 않는가 ────────────────────

def test_artifacts_readme_lists_every_indexed_bundle():
    """★ 19차 — README 의 상태표가 **이미 없는 v1/v2** 만 가리키고 있었다.

    `artifact_index.yaml` 이 무엇이 근거인지의 authority 인데, README 는
    2026-08-07 상태에서 멈춰 v4 계열을 한 줄도 안 적었다. 문서가 stale 이면
    저장소를 여는 사람이 폐기된 묶음을 근거로 착각한다 (17차 발견 8 과 같은
    실패 모드가 artifacts/ 쪽에 남아 있었다).
    """
    import yaml

    root = DOCS.parent
    idx = root / "artifacts" / "artifact_index.yaml"
    readme = root / "artifacts" / "README.md"
    if not idx.exists() or not readme.exists():
        pytest.skip("artifacts/ 없음")

    runs = (yaml.safe_load(idx.read_text(encoding="utf-8")) or {}).get("runs") or {}
    text = readme.read_text(encoding="utf-8")

    missing = [n for n in runs if n not in text]
    assert not missing, (
        f"artifact_index 에 있는 묶음이 README 에 없다: {missing}")


def test_artifacts_readme_marks_unindexed_bundles_as_history():
    """★ 인덱스에 없는데 디스크에 남은 묶음은 **이력**임을 명시해야 한다.

    복원은 되지만 근거가 아니다. 표시가 없으면 인용될 수 있다.
    """
    import yaml

    root = DOCS.parent
    arts = root / "artifacts"
    idx = arts / "artifact_index.yaml"
    readme = arts / "README.md"
    if not idx.exists() or not readme.exists():
        pytest.skip("artifacts/ 없음")

    runs = set((yaml.safe_load(idx.read_text(encoding="utf-8")) or {}).get("runs") or {})
    # ★ 옛 묶음(v1/v2)에는 `payload_sha256.yaml` 이 없다 — 그것으로 걸러내면
    #   정작 "이력으로 표시해야 할" 묶음이 전부 빠져 축이 안 태워진다(skip).
    on_disk = {p.name for p in arts.iterdir()
               if p.is_dir() and any(p.glob("*.parquet"))}
    unindexed = sorted(on_disk - runs)
    if not unindexed:
        pytest.skip("인덱스 밖 묶음 없음")

    text = readme.read_text(encoding="utf-8")
    bad = [n for n in unindexed if n not in text]
    assert not bad, f"인덱스 밖 묶음이 README 에 언급조차 없다: {bad}"
    assert "이력" in text or "history" in text.lower(), \
        "인덱스 밖 묶음을 이력으로 표시하는 문구가 없다"


# ── 문서 ↔ 정본 대조 (자체 리뷰 F-1 재발 방지) ────────────────────────────
#
# ★ 19차 자체 리뷰에서 `docs/09_22P_GAP.md` §7.6 의 grid 행이 half-cell 행을
#   그대로 복제한 **조작 값**으로 실려 있었다 (8칸 전부 정본 불일치). 사람이
#   손으로 옮긴 표는 아무도 검사하지 않았고, 정본 txt 가 커밋조차 안 돼 있어
#   외부 리뷰어도 대조할 수 없었다. 이제 정본이 저장소에 있으므로 **기계가
#   대조한다** — 문서에 손으로 쓴 수치가 정본과 어긋나면 여기서 깨진다.

import re as _re

_CANON = Path(__file__).resolve().parent.parent / "docs" / "22p_gap"
_DOC = Path(__file__).resolve().parent.parent / "docs" / "09_22P_GAP.md"

#: §0 표의 (기준, 목적함수, noise) → 정본 파일 stem
_P22_ROWS = {
    ("grid", "pocv_dvdq", "0"): "dense_pocv_dvdq",
    ("grid", "pocv_dvdq_dqdv", "0"): "dense_pocv_dvdq_dqdv",
    ("half-cell", "pocv_dvdq", "0"): "dense_pocv_dvdq_hc",
    ("half-cell", "pocv_dvdq_dqdv", "0"): "dense_pocv_dvdq_dqdv_hc",
    ("grid", "pocv_dvdq", "0.005"): "seed_pocv_dvdq",
    ("grid", "pocv_dvdq_dqdv", "0.005"): "seed_pocv_dvdq_dqdv",
    ("half-cell", "pocv_dvdq", "0.005"): "seed_pocv_dvdq_hc",
    ("half-cell", "pocv_dvdq_dqdv", "0.005"): "seed_pocv_dvdq_dqdv_hc",
}


def _canon_facts(stem: str) -> dict:
    """정본 출력에서 ①' 의 (참 격차 0 붕괴, ≥4%p 누적) 을 뽑는다."""
    txt = (_CANON / f"{stem}.txt").read_text(encoding="utf-8")
    near = txt.split("①'")[1].split("\n② ")[0]
    m = _re.search(r"^\s*0%p\s+(\d+)\s+(\d+)/(\d+)", near, _re.M)
    assert m, f"{stem}: ①' 의 참 격차 0 행을 못 찾음"
    n, k = int(m.group(1)), int(m.group(2))
    assert int(m.group(3)) == n, f"{stem}: 분모 불일치"
    cum = _re.search(r"동작점 근방\(①'\)\s+≥4%p:\s*(\d+)/(\d+)", txt.split("④")[1])
    assert cum, f"{stem}: ④ 누적 ≥4%p 를 못 찾음"
    return {"gap0_n": n, "gap0_collapse": k, "false_split": n - k,
            "ge4_k": int(cum.group(1)), "ge4_n": int(cum.group(2))}


def test_p22_canon_outputs_are_committed():
    """★ 인용 규칙이 가리키는 정본이 저장소에 있어야 한다.

    자체 리뷰: 문서가 `docs/22p_gap/*.txt` 를 정본이라 선언했는데 그 파일이
    커밋된 적이 없어, 외부 리뷰어가 **어떤 수치도** 대조할 수 없었다.
    """
    assert _CANON.is_dir(), "docs/22p_gap 이 없다 — 정본 미커밋"
    missing = [s for s in sorted(set(_P22_ROWS.values()))
               if not (_CANON / f"{s}.txt").exists()]
    assert not missing, f"§0 표가 근거로 삼는 정본 출력이 없다: {missing}"


def test_p22_headline_table_matches_the_canon_outputs():
    """★ §0 표의 8행이 정본과 셈 단위까지 맞아야 한다 (F-1 재발 방지)."""
    head = _DOC.read_text(encoding="utf-8").split("## 1. 질문")[0]

    checked = 0
    for (ref, obj, noise), stem in _P22_ROWS.items():
        c = _canon_facts(stem)
        row = _re.search(
            r"^\|\s*(?:\*\*)?" + _re.escape(ref) + r"(?:\*\*)?\s*\|\s*(?:\*\*)?`"
            + _re.escape(obj) + r"`(?:\*\*)?\s*\|\s*" + _re.escape(noise)
            + r"\s*\|([^|]*)\|([^|]*)\|", head, _re.M)
        assert row, f"§0 표에서 ({ref}, {obj}, noise={noise}) 행을 못 찾음"
        fs, col = row.group(1), row.group(2)

        want_fs = f"{c['false_split']}/{c['gap0_n']}"
        assert want_fs in fs, (
            f"({ref},{obj},{noise}) 거짓 분리: 문서 '{fs.strip()}' vs "
            f"정본 {want_fs} ({stem}.txt: 붕괴 {c['gap0_collapse']}/{c['gap0_n']})")
        want_col = f"{c['ge4_k']}/{c['ge4_n']}"
        assert want_col in col, (
            f"({ref},{obj},{noise}) 붕괴: 문서 '{col.strip()}' vs 정본 {want_col}")
        checked += 1
    assert checked == 8, checked


# ── 종료 시 SIGABRT flake 방지 (게이트 신뢰성) ────────────────────────────
#
# ★ smoke 가 간헐적으로(4~6회 중 1회) 실패했다. 잡아 보니 검사는 전부 ✅ 인데
#   인터프리터 **종료 중**에 죽었다:
#       ✅ results/_smoke/grid_fit: 통과
#       ✅ results/_smoke/halfcell_fit: 통과
#       terminate called without an active exception
#       ./scripts/smoke_e2e.sh: line 242: 7374 Aborted
#   PyBaMM/CasADi 가 끌어오는 C++ 런타임이 teardown 에서 std::terminate 를
#   부르는 전형적 패턴이다. 결과는 옳은데 exit code 만 오염된다 — 10시간짜리
#   본 실행을 지키는 게이트가 이유 없이 빨개지고, 반복 실행으로 초록을 뽑는
#   습관이 들면 게이트 자체가 무의미해진다.
#
#   처방: heredoc 은 `sys.exit()` 대신 **flush 후 `os._exit()`** 로 끝낸다
#   (teardown 을 건너뛴다). 두 곳에만 발라져 있던 것을 전부로 넓혔다.

_SCRIPTS = [Path(__file__).resolve().parent.parent / "scripts" / n
            for n in ("smoke_e2e.sh", "archive_results.sh")]


def test_shell_heredocs_do_not_use_sys_exit():
    """★ 무거운 import 를 한 heredoc 이 sys.exit 로 끝나면 teardown abort 에 노출."""
    offenders = []
    for sc in _SCRIPTS:
        for i, line in enumerate(sc.read_text(encoding="utf-8").splitlines(), 1):
            if _re.match(r"\s*sys\.exit\(", line):
                offenders.append(f"{sc.name}:{i}: {line.strip()}")
    assert not offenders, (
        "heredoc 종료가 sys.exit 다 — PyBaMM/CasADi teardown 에서 SIGABRT 가 나면 "
        "검사가 전부 통과해도 게이트가 빨개진다. flush 후 os._exit 를 쓸 것:\n  "
        + "\n  ".join(offenders))


def test_os_exit_calls_flush_first():
    """★ `os._exit` 는 버퍼를 안 비운다 — 앞줄에서 flush 해야 출력이 안 잘린다."""
    bad = []
    for sc in _SCRIPTS:
        lines = sc.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if "os._exit(" in line and not line.strip().startswith("#"):
                window = "\n".join(lines[max(0, i - 3):i + 1])
                if "flush()" not in window:
                    bad.append(f"{sc.name}:{i + 1}: {line.strip()}")
    assert not bad, "os._exit 앞 3줄 안에 flush() 가 없다:\n  " + "\n  ".join(bad)
