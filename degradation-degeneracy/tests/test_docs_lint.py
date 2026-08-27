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

import hashlib
import json
import os
import time
import re
import shutil
import subprocess
import sys
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
from pathlib import Path as _Path

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


def test_p22_canon_outputs_are_not_empty():
    """★ 0바이트 정본이 커밋돼 있으면 '대조 가능' 이 거짓말이 된다.

    13차 자체 리뷰 실측: `dense_pocv_dvdq_dqdv_hc_breakdown.txt` 가 HEAD 에
    **0바이트**로 커밋돼 있었다 (blob 크기 0). §7.9 의 참 격차 0 칸 분해 표는
    그 파일을 근거로 내세우는데, 파일에는 아무것도 없었다 — 외부 리뷰어가
    열면 빈 파일을 본다. 존재 검사만으로는 못 잡는다.
    """
    empty = [p.name for p in sorted(_CANON.glob("*.txt"))
             if not p.read_text(encoding="utf-8").strip()]
    assert not empty, f"0바이트 정본: {empty}"


def test_p22_doc_only_cites_canon_files_that_exist_and_have_content():
    """★ 문서가 이름을 부른 정본은 전부 실재하고 내용이 있어야 한다."""
    doc = _DOC.read_text(encoding="utf-8")
    cited = set(_re.findall(r"22p_gap/([A-Za-z0-9_]+)\.txt", doc))
    bad = [s for s in sorted(cited)
           if not (_CANON / f"{s}.txt").is_file()
           or not (_CANON / f"{s}.txt").read_text(encoding="utf-8").strip()]
    assert not bad, f"문서가 부르는데 없거나 빈 정본: {bad}"


#: OCP 모델 오차 민감도 표 — **원점이 건강한 다리만**.
#:
#: ★ 13차 정정. dense 의 PE 2·5·10 mV 는 Case 1 좌표 원점(p_ini)이 오염돼
#:   있었다 (a_ne ≈ 1.03, 건강한 다리는 1.06). 세 다리 모두 96~100% 파탄했고
#:   그것을 "2 mV 상전이" 로 읽었는데, 같은 왜곡이 원점이 멀쩡한 seed 격자
#:   6개에서는 전부 무해했다. 그 세 점은 왜곡 효과가 아니라 **최적화 인공물**
#:   이므로 표에서 뺀다. 정본 파일은 남긴다 (docs/22p_gap/pini_all.txt 가
#:   왜 뺐는지의 근거다) — 표가 가리키지 않을 뿐이다.
#: ★ 변이 M75 로 발견 — 격자 열이 생긴 뒤 라벨("0 mV")이 두 번 나오는데 키가
#:   mV 뿐이라 **seed_101 행 4개가 대조 밖**이었다. 10 mV 붕괴를 무해로 위조해도
#:   통과했다. 가장 중요한 수치가 무방비였다. 키에 격자를 넣는다.
_P22_BIAS_ROWS = {
    ("dense", "0"): "dense_pocv_dvdq_dqdv_hc",
    ("dense", "1"): "bias_pe1mv",
    ("dense", "1.5"): "bias_pe1p5mv",
    ("seed_101", "0"): "seed101_pocv_dvdq_dqdv_hc",
    ("seed_101", "2"): "bias_seed101_pe2mv",
    ("seed_101", "5"): "bias_seed101_pe5mv",
    ("seed_101", "10"): "bias_seed101_pe10mv",
}

#: restart 예산 검증 — 같은 왜곡(dense PE +2 mV)을 restart 5 vs 20 으로.
#:   ★ restart 를 늘리자 원점이 회복되고 파탄이 사라졌다. 이 두 행이 "처방이
#:     실증됐다" 의 근거이자, **restart 5 가 이 연구 전체의 미검증 전제**라는
#:     경고의 근거다. 값이 틀어지면 두 주장이 동시에 무너진다.
_P22_RESTART_ROWS = {
    "5": "bias_pe2mv",
    "20": "bias_pe2mv_r20",
}

#: 원점 건강 판정 — a_ne 가 이 범위 밖이면 좌표계가 오염된 것으로 본다.
#:   건강한 11개 다리: 1.0582~1.0693 · 오염된 3개: 1.0289~1.0312
_P22_PINI_ANE_OK = (1.05, 1.08)

#: 표에 쓰는 다리는 **원점이 건강해야 한다**. (라벨 → 진단 JSON 의 다리 이름)
_P22_PINI_LEGS = {
    ("dense", "0"): "fit_22p_dense_hc",
    ("dense", "1"): "fit_dense_pe1mv",
    ("dense", "1.5"): "fit_dense_pe1p5mv",
    ("seed_101", "5"): "fit_seed101_pe5mv",
    ("seed_101", "10"): "fit_seed101_pe10mv",
}

#: 격자 의존성 표 — 같은 왜곡을 seed_101 격자에서 되풀이한 값
#:   ★ dense 에서 2 mV 가 상전이를 일으켰는데 seed_101 에서는 5 mV 까지
#:     아무 일도 안 난다. "문턱 = 2 mV" 를 격자 불변인 것처럼 적으면 거짓이다.
_P22_SEED_ROWS = {
    "0": "seed101_pocv_dvdq_dqdv_hc",
    "2": "bias_seed101_pe2mv",
    "5": "bias_seed101_pe5mv",
    "10": "bias_seed101_pe10mv",
}

#: 축 비교 — 전압 오프셋 vs 화학량론 window
_P22_AXIS_ROWS = {
    "stretch 0.95": "bias_pest095",
}


def test_p22_bias_canon_outputs_are_committed():
    """★ 민감도 표가 근거로 삼는 정본이 저장소에 있어야 한다.

    자체 리뷰(R11): §0 표만 기계 대조 대상이라, 앞으로 들어올 민감도 표는
    §7.6 복제-행 사고(문서 `:11-15` 배너가 자인하는 그 사고)를 막을 장치가
    없는 사각지대였다. 표가 생기는 시점에 함께 닫는다.
    """
    missing = [s for s in sorted(set(_P22_BIAS_ROWS.values()))
               if not (_CANON / f"{s}.txt").exists()]
    assert not missing, f"민감도 표가 근거로 삼는 정본이 없다: {missing}"


def test_p22_bias_table_matches_the_canon_outputs():
    """★ 민감도 표의 7행이 정본과 셈 단위까지 맞아야 한다."""
    doc = _DOC.read_text(encoding="utf-8")
    assert "OCP 오차" in doc, "민감도 절이 문서에 없다"

    checked = 0
    for (grid, mv), stem in _P22_BIAS_ROWS.items():
        c = _canon_facts(stem)
        # 표는 | 오프셋 | 격자 | 거짓 분리 | 놓침 | ... — 격자까지 맞춰야 한다
        row = _re.search(
            r"^\|\s*(?:\*\*)?" + _re.escape(mv)
            + r"\s*mV(?:\*\*)?[^|]*\|\s*" + _re.escape(grid)
            + r"\s*\|([^|]*)\|([^|]*)\|",
            doc, _re.M)
        assert row, f"민감도 표에서 ({grid}, {mv} mV) 행을 못 찾음"
        fs, col = row.group(1), row.group(2)

        want_fs = f"{c['false_split']}/{c['gap0_n']}"
        assert want_fs in fs, (
            f"({grid}, {mv} mV) 거짓 분리: 문서 '{fs.strip()}' vs 정본 {want_fs} "
            f"({stem}.txt: 붕괴 {c['gap0_collapse']}/{c['gap0_n']})")
        want_col = f"{c['ge4_k']}/{c['ge4_n']}"
        assert want_col in col, (
            f"({grid}, {mv} mV) 놓침: 문서 '{col.strip()}' vs 정본 {want_col}")
        checked += 1
    assert checked == 7, checked


def test_p22_seed_grid_table_matches_the_canon_outputs():
    """★ 격자 의존성 표가 정본과 맞아야 한다.

    이 표의 존재 이유는 "문턱 2 mV" 가 **격자 불변이 아님**을 문서에 못 박는
    것이다. 값이 틀어지면 그 경고 자체가 거짓이 되므로 기계로 고정한다.
    """
    doc = _DOC.read_text(encoding="utf-8")
    assert "seed_101" in doc, "격자 의존성 절이 문서에 없다"
    # ★ §7.10 앞쪽의 dense 전용 표에도 "0 mV" 행이 있다 — 구간을 좁히지 않으면
    #   그쪽을 잡아 엉뚱한 열을 대조한다 (실측으로 그랬다).
    doc = (doc.split("같은 왜곡이 원점 건강한 격자에서는 무해했다")[1]
              .split("#### NE stretch")[0])

    checked = 0
    for mv, stem in _P22_SEED_ROWS.items():
        c = _canon_facts(stem)
        row = _re.search(
            r"^\|\s*(?:\*\*)?" + _re.escape(mv)
            + r"\s*mV(?:\*\*)?[^|]*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|",
            doc, _re.M)
        assert row, f"격자 표에서 {mv} mV 행을 못 찾음"
        seed_fs, seed_col = row.group(3), row.group(4)   # 3·4열이 seed_101 쪽
        want_fs = f"{c['false_split']}/{c['gap0_n']}"
        assert want_fs in seed_fs, (
            f"{mv} mV seed_101 거짓 분리: 문서 '{seed_fs.strip()}' vs 정본 {want_fs}")
        want_col = f"{c['ge4_k']}/{c['ge4_n']}"
        assert want_col in seed_col, (
            f"{mv} mV seed_101 놓침: 문서 '{seed_col.strip()}' vs 정본 {want_col}")
        checked += 1
    assert checked == 4, checked


def test_p22_axis_comparison_matches_the_canon_output():
    """★ stretch 축 행도 정본과 맞아야 한다 (전압축과 비교하는 근거)."""
    doc = _DOC.read_text(encoding="utf-8")
    for label, stem in _P22_AXIS_ROWS.items():
        c = _canon_facts(stem)
        row = _re.search(r"^\|[^|]*" + _re.escape(label) + r"[^|]*\|([^|]*)\|([^|]*)\|",
                         doc, _re.M)
        assert row, f"축 비교 표에서 '{label}' 행을 못 찾음"
        want_fs = f"{c['false_split']}/{c['gap0_n']}"
        assert want_fs in row.group(1), (
            f"{label} 거짓 분리: 문서 '{row.group(1).strip()}' vs 정본 {want_fs}")
        want_col = f"{c['ge4_k']}/{c['ge4_n']}"
        assert want_col in row.group(2), (
            f"{label} 놓침: 문서 '{row.group(2).strip()}' vs 정본 {want_col}")


def test_p22_bias_table_only_cites_legs_with_a_healthy_origin():
    """★ 표에 쓰는 다리는 Case 1 좌표 원점이 건강해야 한다.

    13차에서 dense 의 PE 2·5·10 mV 를 "2 mV 상전이" 의 근거로 표에 넣었는데,
    셋 다 원점이 오염돼 있었다 (a_ne ≈ 1.03). 같은 왜곡이 원점 멀쩡한 격자
    6개에서는 무해했으니, 그 수치는 왜곡 효과가 아니라 최적화 인공물이다.
    **원점을 안 보고 표를 만들면 같은 사고가 반복된다** — 기계로 막는다.
    """
    import json

    diag = _CANON / "pini_all.json"
    assert diag.is_file(), "원점 진단 정본(pini_all.json)이 없다"
    by_name = {_Path(r["dir"]).name: r
               for r in json.loads(diag.read_text(encoding="utf-8"))}

    lo, hi = _P22_PINI_ANE_OK
    for (grid, label), leg in _P22_PINI_LEGS.items():
        r = by_name.get(leg)
        assert r, f"({grid}, {label}): 진단 정본에 {leg} 가 없다"
        a_ne = r["p_ini"][2]
        assert lo <= a_ne <= hi, (
            f"({grid}, {label}) 행이 원점 오염 다리({leg})를 가리킨다: a_ne={a_ne} "
            f"(건강 범위 {lo}~{hi})")


def test_p22_doc_records_the_discarded_origin_polluted_legs():
    """★ 뺀 이유가 문서에 남아야 한다 — 조용히 지우면 은폐다."""
    doc = _DOC.read_text(encoding="utf-8")
    assert "원점 오염" in doc, "원점 오염으로 뺀 다리의 사유가 문서에 없다"
    assert "pini_all.txt" in doc, "판정 근거 정본을 가리키지 않는다"
    assert "bias_pe{2,5,10}mv.txt" in doc, "뺀 다리의 정본 파일을 밝히지 않았다"
    for leg in ("2 mV", "5 mV", "10 mV"):
        assert leg in doc, f"뺀 다리 {leg} 가 문서에 언급조차 없다"


def test_p22_restart_table_matches_the_canon_outputs():
    """★ 예산 상한 5 ↔ 20 대조가 정본과 맞아야 한다.

    이 두 행이 떠받치는 주장은 **하나뿐**이다 — 상한 5 가 이 연구 전체의
    미검증 전제라는 것. "처방이 실증됐다" 는 21차 리뷰 발견 8 로 철회했다
    (원점 예산·조건 예산·adaptive 가 함께 바뀐 n=1 교란 다리다,
    철회[R20_RX]). 표의 수치 결속만 남긴다.

    ★ 이 테스트는 문서 문구를 고칠 때 먼저 깨졌다 — 앵커가 "restart 20 으로
      늘리면 파탄이 사라진다" 는 옛 제목과 `restart 5` 라는 행 이름에 걸려
      있었기 때문이다. 앵커는 새 문구로 옮기되 **검사 자체(정본 대조)는
      그대로** 둔다.
    """
    doc = _DOC.read_text(encoding="utf-8")
    assert "restart" in doc, "restart 검증 절이 문서에 없다"
    body = doc.split("예산 상한 20 으로 다시 돌렸다")[1].split("####")[0]

    checked = 0
    for n, stem in _P22_RESTART_ROWS.items():
        c = _canon_facts(stem)
        row = _re.search(
            r"^\|\s*(?:\*\*)?(?:restart|예산 상한)\s*" + _re.escape(n)
            + r"(?:\*\*)?[^|]*\|([^|]*)\|([^|]*)\|([^|]*)\|", body, _re.M)
        assert row, f"restart {n} 행을 못 찾음"
        want_fs = f"{c['false_split']}/{c['gap0_n']}"
        assert want_fs in row.group(2), (
            f"restart {n} 거짓 분리: 문서 '{row.group(2).strip()}' vs 정본 {want_fs}")
        want_col = f"{c['ge4_k']}/{c['ge4_n']}"
        assert want_col in row.group(3), (
            f"restart {n} 놓침: 문서 '{row.group(3).strip()}' vs 정본 {want_col}")
        checked += 1
    assert checked == 2, checked


#: §7.10 "무엇을 재지 않았나" 가 다루는 축 → 그 축을 돌렸다면 남았을 정본.
#: 정본이 있으면 그 축은 **쟀다** 이고, 목록은 그것을 정본 이름으로 인정해야 한다.
_P22_MEASURED_AXES = {
    "PE 화학량론 window": ("bias_pest095",),
    "NE 화학량론 window": ("bias_nest095",),
    "NE 전압 오프셋": ("bias_ne2mv",),
    "양극 동시 왜곡": ("bias_both2mv",),
    "잡음 층": ("bias_seed101_pe2mv_n005", "bias_seed101_pe5mv_n005",
                "bias_seed101_pe10mv_n005"),
}

#: 갱신되지 않은 채 남아 있던 원문장들. 다시 들어오면 표와 모순된다.
_P22_STALE_DENIALS = (
    "다리는 아직 안 돌렸다",
    "안 돌렸다. PE 단독 축 하나다",
    "여섯 다리 전부 noise 0 이다",
    "화학량론 축(stretch)은 아직 안 쟀다",
)


def test_p22_unmeasured_list_credits_every_leg_that_was_run():
    """★ 20차 사전 자체발견 — "안 쟀다" 목록이 표와 정면으로 모순됐다.

    `19856e7e` 가 §7.10 에 "무엇을 재지 않았나" 를 썼을 때는 셋 다 참이었다.
    그 뒤 `8ce869f0`(NE 축·공통 모드) · `1542688d`(stretch·seed) ·
    `58f53bb4`(§7.10 재작성) 가 그 다리들을 **실제로 돌려 표에 실었는데**
    목록은 갱신되지 않았다. 결과: 같은 절 안에서 50줄 위 표가
    `PE stretch 0.95` · `NE +2 mV` · `PE+2 · NE+2` 수치를 인용하면서
    아래에서는 "다리는 아직 안 돌렸다" 고 말한다. 심지어 stretch 표는
    본문에서 `"무엇을 재지 않았나" 참조` 로 그 문단을 가리킨다.

    이 실패 모드는 다리가 늘 때마다 재발한다 — 목록은 사람이 지워야 하는데
    표를 추가하는 커밋은 목록을 보지 않는다. 그래서 **정본 존재**로 묶는다.

    부정 키워드 사냥("안 쟀다" 라는 말이 있는가)은 처음 시도했다가 버렸다 —
    축 이름이 "쟀다" 쪽 표에 나오기만 해도 걸려서 정상 문서를 막았다.
    대신 **양성 결속**을 쓴다: 정본이 있으면 그 정본 이름이 이 절에 있어야
    한다. 이러면 축을 새로 돌린 사람이 목록을 갱신해야만 통과한다.
    """
    doc = _DOC.read_text(encoding="utf-8")
    assert "#### 무엇을 재지 않았나" in doc, "§7.10 의 '무엇을 재지 않았나' 절이 없다"
    block = doc.split("#### 무엇을 재지 않았나")[1].split("\n## ")[0]

    bad = []
    for axis, stems in _P22_MEASURED_AXES.items():
        ran = [s for s in stems if (_CANON / f"{s}.txt").exists()]
        if not ran:
            continue                      # 아직 안 돌린 축 — 목록에 없어도 된다
        missing = [s for s in ran if f"{s}.txt" not in block]
        if missing:
            bad.append(f"{axis}: 정본 {missing} 이 있는데 이 절이 인용하지 않는다")
    assert not bad, (
        "「무엇을 재지 않았나」가 이미 돌린 다리를 반영하지 않았다:\n  "
        + "\n  ".join(bad))

    stale = [s for s in _P22_STALE_DENIALS if s in block]
    assert not stale, f"표와 모순되던 옛 문장이 되살아났다: {stale}"


# ── warm-start 분리 실험: 문서 수치를 봉인 summary 에 결속 ────────────────────
_WARM = Path(__file__).resolve().parent.parent / "docs" / "22p_gap" / "warm_probe"

#: §20.4 재정정 표가 인용하는 (다리, 목적함수) → 그 값이 있어야 할 곳.
_WARM_CLAIMS = [
    ("paired_fixed5_v4", "pocv_dvdq"), ("paired_fixed5_v4", "pocv_dvdq_dqdv"),
    ("paired_fixed5_v4_nowarm_now", "pocv_dvdq"),
    ("paired_fixed5_v4_nowarm_now", "pocv_dvdq_dqdv"),
    ("paired_fixed5_v4_warm", "pocv_dvdq"),
    ("paired_fixed5_v4_warm", "pocv_dvdq_dqdv"),
]

#: **같은 digest** 에서 warm 만 다른 짝 → 연쇄 1번째는 동일해야 한다.
#: ★ 초판에 `fit_seed404_pe5mv` 를 넣었다가 이 테스트에 잡혔다 — 그 다리는
#:   옛 digest(`d842894`)라 same-digest 짝이 아니다. warm 축만 분리하려면
#:   digest 가 같아야 한다는 것을 테스트가 먼저 강제했다.
#: ★★ 두 번째로, 21차 리뷰 발견 4 를 새 run_spec 회귀가 **독립 재현**하면서
#:   half-cell 짝(`fit_22p_seed_404_hc_*`)이 여기서 빠졌다. 그 짝은 warm 이
#:   `p_ini` 까지 바꿔 단일 축 짝이 아니다 → `_CONFOUNDED_PAIRS` 로 옮겼다.
_WARM_PAIRS = [("paired_fixed5_v4_nowarm_now", "paired_fixed5_v4_warm")]

#: warm 을 켰지만 **다른 축도 함께 움직인** 짝. 인과 귀속에 쓸 수 없다.
#: 목록에서 조용히 사라지거나 `_WARM_PAIRS` 로 승격되는 것을 막기 위해
#: "정말 교란돼 있는가" 를 양성으로 검사한다 (아래 테스트).
_CONFOUNDED_PAIRS = [
    ("fit_22p_seed_404_hc_nowarm", "fit_22p_seed_404_hc_warm_now",
     "half-cell 은 pristine 기준의 `p_ini` 도 같은 warm 플래그로 계산한다 "
     "(`src/fitting.py:862`) → 원점이 함께 이동한다. adaptive 도 켜져 있어 "
     "실제 예산 분포까지 달라진다 (2회 종료 223 → 238)."),
]

#: digest 가 다른 짝 — warm 축 귀속에는 못 쓰지만, 1번째가 그래도 같다는 것은
#: 그 digest 구간이 수치적으로 무해하다는 별도 증거다 (LEG_INVENTORY §22).
_XDIGEST_PAIRS = [("fit_seed404_pe5mv_nowarm", "fit_seed404_pe5mv"),
                  ("fit_22p_seed_404_hc_warm_now", "fit_22p_seed_404_hc")]


def _warm_summary(leg: str) -> dict:
    import yaml
    return yaml.safe_load((_WARM / f"{leg}.summary.yaml").read_text(encoding="utf-8"))


def _warm_manifest(leg: str) -> dict:
    import yaml
    return yaml.safe_load((_WARM / f"{leg}.manifest.yaml").read_text(encoding="utf-8"))


def test_warm_probe_summaries_are_committed():
    """★ 20차 리뷰 후속 — §20.4 재정정이 인용하는 다리는 봉인돼 있어야 한다.

    원자료(`fits.parquet`)는 `results/` 에만 있어 git 밖이다. summary·manifest
    조차 없으면 §20.4 재정정 전체가 자기신고가 된다 (원칙 2 위반).
    """
    missing = [l for l, _ in _WARM_CLAIMS if not (_WARM / f"{l}.summary.yaml").is_file()]
    assert not missing, f"§20.4 가 인용하는 다리의 summary 가 없다: {missing}"


def test_warm_probe_numbers_match_the_review_response():
    """★ 문서에 적힌 `degenerate_frac` 이 봉인 summary 와 같아야 한다.

    손으로 옮겨 적은 수치가 stale 해지는 것이 이 저장소의 반복 실패 모드다
    (§20.4 자신이 그 사고의 기록이다). 기계로 묶는다.
    """
    doc = (DOCS / "08_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    bad = []
    for leg, obj in _WARM_CLAIMS:
        val = _warm_summary(leg)["by_objective"][obj]["degenerate_frac"]
        if f"{val:.6f}" not in doc:
            bad.append(f"{leg}/{obj} = {val:.6f} 가 문서에 없다")
    assert not bad, "§20.4 수치가 봉인본과 어긋난다:\n  " + "\n  ".join(bad)


def test_warm_probe_records_the_protocol_axes():
    """★ regime 3축(warm·adaptive·restart)이 manifest 에 남아 있어야 한다.

    20차 리뷰 발견 3 의 핵심 — 같은 수치도 protocol 이 다르면 다른 뜻이다.
    `paired_fixed5_v4` 가 `warm_start=False` 라는 사실이 §20.4 재정정의 출발점이다.
    """
    for leg, _ in _WARM_CLAIMS:
        rs = _warm_manifest(leg).get("run_spec") or {}
        assert rs.get("warm_start") is not None, f"{leg}: warm_start 미기록"
        assert (rs.get("optimizer") or {}).get("adaptive") is not None, \
            f"{leg}: optimizer.adaptive 미기록"
        assert rs.get("n_restarts"), f"{leg}: n_restarts 미기록"
    assert (_warm_manifest("paired_fixed5_v4")["run_spec"]["warm_start"]) is False, \
        "정본이 warm=False 라는 §20.4 재정정의 전제가 깨졌다"


def test_warm_only_moves_the_second_objective_in_the_chain():
    """★ 이 실험의 sanity check — 연쇄 1번째는 warm 영향을 받으면 안 된다.

    `--objective pocv_dvdq,pocv_dvdq_dqdv` 에서 warm start 는 앞 목적함수의 해를
    뒤로 넘긴다. 1번째는 넘겨받을 것이 없으므로 warm 여부와 무관해야 한다.
    이것이 깨지면 "34p 변화는 warm 때문" 이라는 §20.4 재정정의 귀속이 무너진다.

    실측 (같은 digest, warm 만 다름):
      paired  33p 0.615854 = 0.615854 · 34p 0.873984 → 0.628726

    ★ 404 half-cell 짝은 여기서 뺐다 (21차 발견 4). 33p 등식은 그 짝에서도
      성립하지만 warm 이 `p_ini` 까지 바꾸므로 **단일 축 짝이 아니다** —
      `_CONFOUNDED_PAIRS` 와 그 전용 테스트로 옮겼다.
    """
    assert _WARM_PAIRS, "matched warm 짝이 하나도 없다"
    for nowarm, warm in _WARM_PAIRS:
        mn, mw = _warm_manifest(nowarm)["run_spec"], _warm_manifest(warm)["run_spec"]
        assert mn["source_digest"] == mw["source_digest"], (
            f"{nowarm} vs {warm}: digest 가 달라 warm 축이 분리되지 않는다")
        assert mn["warm_start"] is False and mw["warm_start"] is True

        a = _warm_summary(nowarm)["by_objective"]["pocv_dvdq"]["degenerate_frac"]
        b = _warm_summary(warm)["by_objective"]["pocv_dvdq"]["degenerate_frac"]
        assert a == b, (
            f"{nowarm} vs {warm}: 연쇄 1번째(pocv_dvdq)가 움직였다 "
            f"({a:.6f} vs {b:.6f}) — warm 귀속이 성립하지 않는다")

        c = _warm_summary(nowarm)["by_objective"]["pocv_dvdq_dqdv"]["degenerate_frac"]
        d = _warm_summary(warm)["by_objective"]["pocv_dvdq_dqdv"]["degenerate_frac"]
        assert d < c, f"{warm}: warm 이 34p 를 개선하지 않았다 ({c:.6f} → {d:.6f})"


def test_cross_digest_pairs_still_agree_on_the_first_objective():
    """★ digest 가 달라도 연쇄 1번째가 같다 — 그 구간이 수치적으로 무해하다는 증거.

    warm 축 귀속에는 쓸 수 없는 짝이지만(코드가 섞인다), 1번째 목적함수가
    소수점 6자리까지 일치한다는 것은 그 digest 구간이 fit 수치를 안 바꿨다는
    독립 증거다. `fit_22p_seed_404_hc`(7250c6e6) ↔ `_warm_now`(a72c0f3a) 는
    34p 까지 일치한다 — LEG_INVENTORY §22 의 교차-digest 완전 재현.
    """
    for a, b in _XDIGEST_PAIRS:
        da = _warm_manifest(a)["run_spec"]["source_digest"]
        db = _warm_manifest(b)["run_spec"]["source_digest"]
        assert da != db, f"{a} vs {b}: digest 가 같다 — 이 목록의 전제가 깨졌다"
        va = _warm_summary(a)["by_objective"]["pocv_dvdq"]["degenerate_frac"]
        vb = _warm_summary(b)["by_objective"]["pocv_dvdq"]["degenerate_frac"]
        assert va == vb, (
            f"{a}({da[:8]}) vs {b}({db[:8]}): 연쇄 1번째가 digest 간에 갈렸다 "
            f"({va:.6f} vs {vb:.6f}) — 그 구간이 수치를 바꿨다는 뜻이다")


# ── 철회 원장: 철회한 결론이 활성 본문에서 되살아나지 않는다 ──────────────────
_CLAIM_STATUS = (Path(__file__).resolve().parent.parent
                 / "docs" / "22p_gap" / "CLAIM_STATUS.yaml")
_REPO = Path(__file__).resolve().parent.parent

#: 보이지 않는 격리 울타리. blockquote 여부로 격리를 판정하지 않는다 —
#: §20.4 는 정정 블록 **전체**가 인용이라, 인용을 격리로 치면 정정문 자신이
#: 검사에서 빠진다 (21차 리뷰 발견 8 이 지적한 실패 모드의 재발).
#: ★ 22차 자체 발견 — `search` 로 잡으면 **표 셀 안의 설명용 인용**까지 진짜
#:   울타리가 된다. §29.1 의 설명 표(`| \`<!-- QUARANTINE:ID -->\` … |`)가
#:   여는 울타리로 파싱돼 `08_REVIEW_RESPONSE.md` 의 1831줄 **이후 전체**가
#:   금지어 검사에서 조용히 빠져 있었다 (그 안에 금지어 4개가 있었다).
#:   그래서 **줄 전체가 마커 하나뿐일 때만** 울타리로 본다.
_Q_OPEN = re.compile(r"^<!--\s*QUARANTINE:([A-Z0-9_]+)\s*-->$")
_Q_CLOSE = re.compile(r"^<!--\s*/QUARANTINE\s*-->$")


def _claim_file(rel: str) -> Path:
    """원장 `files` 항목 → 실제 경로.

    원장은 프로젝트 상대(`docs/…`)와 repo 상대(`wiki/…`)를 섞어 쓴다.
    ★ 23차 발견 7 대응으로 wiki 를 files 에 넣으면서 필요해졌다.
    """
    a = _REPO / rel
    return a if a.exists() else _REPO_ROOT_FOR_CLAIMS / rel


_REPO_ROOT_FOR_CLAIMS = Path(__file__).resolve().parent.parent.parent


def _claim_status() -> dict:
    import yaml
    return yaml.safe_load(_CLAIM_STATUS.read_text(encoding="utf-8"))


def _active_text(text: str) -> tuple[str, set[str]]:
    """격리 구역을 빈 줄로 치환한 본문과, 울타리가 이름한 claim ID 집합.

    줄 수를 보존하므로 match offset → 원본 줄 번호가 그대로 맞는다.
    """
    out, fenced, depth = [], set(), 0
    for line in text.splitlines():
        m = _Q_OPEN.match(line.strip())
        if m:
            fenced.add(m.group(1))
            depth += 1
            out.append("")
            continue
        if _Q_CLOSE.match(line.strip()):
            depth = max(0, depth - 1)
            out.append("")
            continue
        out.append("" if depth else line)
    return "\n".join(out), fenced


def test_claim_status_registry_is_wellformed():
    """원장 자신이 깨지면 아래 검사가 조용히 통과한다 — 먼저 막는다."""
    reg = _claim_status()
    assert reg.get("schema_version") == 5
    ids = [c["id"] for c in reg["claims"]]
    assert len(ids) == len(set(ids)), f"claim id 중복: {ids}"

    # ★ 25차 발견 6 — 활성 주장도 같은 원장에 있다 (claim authority 는 하나)
    act = reg.get("active_claims") or []
    assert act, "active_claims 가 없다 — claim_roles 가 가리킬 곳이 없다"
    aids = [c["id"] for c in act]
    assert len(aids) == len(set(aids)), f"active claim id 중복: {aids}"
    both = sorted(set(aids) & set(ids))
    assert not both, f"같은 id 가 철회 원장과 활성 원장에 동시에 있다: {both}"
    gens = reg.get("protocol_generations") or []
    assert gens, "protocol_generations 가 없다 — 세대가 자유문자가 된다"
    for c in act:
        assert re.fullmatch(r"[A-Z0-9_]+", c["id"]), c["id"]
        assert c.get("protocol_generation") in gens, (
            f"{c['id']}: protocol_generation={c.get('protocol_generation')!r} "
            f"∉ {gens}")
        assert isinstance(c.get("requires_leg"), bool), f"{c['id']}: requires_leg"
        assert c.get("무엇"), f"{c['id']}: 설명 없음"
    for c in reg["claims"]:
        assert c["status"] in ("retracted", "downgraded"), c
        assert c["record"] in ("quarantined", "removed",
                               "legacy_section_marker"), c
        if c["record"] == "legacy_section_marker":
            # 금지어가 `RETRACTED` dict 에 있다 — 여기서 비어 있는 것이 정상이다.
            assert not c["banned"], (
                f"{c['id']}: legacy 인데 banned 가 있다 — 두 곳에 정의하면 갈린다")
        else:
            assert c["banned"], f"{c['id']}: banned 가 비었다 — 검사할 것이 없다"
        for pat in c["banned"]:
            re.compile(pat)          # 잘못된 정규식이면 여기서 죽는다
        for f in c["files"]:
            assert _claim_file(f).is_file(), f"{c['id']}: 대상 파일 없음 {f}"


def test_retracted_claims_do_not_reappear_in_active_prose():
    """★ 21차 리뷰 발견 8 — 배너를 붙여도 활성 본문이 옛 결론을 되살렸다.

    19~20차에서 7개 결론을 철회하면서 배너만 달았다. 배너 위아래의 본문·표·
    제목은 그대로 남아 같은 말을 계속했고, 21차 리뷰가 `:75-79` `:95-97`
    `:351-358` `:649` `:903-917` `:1067-1069` `:1190-1193` `:1361` 여덟 곳을
    찾아냈다. 사람이 배너를 다는 방식은 이미 두 번 실패했으므로 기계로 막는다.

    검사 대상은 **활성 본문** — `<!-- QUARANTINE:ID -->` 울타리 밖 전부다.
    옛 문장을 기록으로 남기고 싶으면 울타리 안에 넣으면 된다.
    """
    reg = _claim_status()
    bad = []
    for c in reg["claims"]:
        for rel in c["files"]:
            raw = _claim_file(rel).read_text(encoding="utf-8")
            active, _ = _active_text(raw)
            for pat in c["banned"]:
                for m in re.finditer(pat, active):
                    line = active[:m.start()].count("\n") + 1
                    bad.append(f"{rel}:{line} [{c['id']}] {m.group(0)!r}")
    assert not bad, (
        "철회한 주장이 활성 본문에 살아 있다 (원장: docs/22p_gap/CLAIM_STATUS.yaml):\n  "
        + "\n  ".join(bad))


def test_every_quarantined_claim_still_has_a_visible_retraction():
    """★ 양성 결속 — 배너를 지우면 실패한다.

    금지어 검사만 두면 "옛 문장을 통째로 지우기" 로도 통과한다. 이 저장소의
    철회 원칙은 **기록을 남기는 것**이므로(08_REVIEW_RESPONSE 원장), 울타리가
    사라지는 것도 회귀로 잡는다.
    """
    reg = _claim_status()
    missing = []
    for c in reg["claims"]:
        if c["record"] != "quarantined":
            continue
        seen = set()
        for rel in c["files"]:
            _, fenced = _active_text(_claim_file(rel).read_text(encoding="utf-8"))
            seen |= fenced
        if c["id"] not in seen:
            missing.append(f"{c['id']} — {c['files']}")
    assert not missing, (
        "철회 기록(QUARANTINE 울타리)이 사라졌다:\n  " + "\n  ".join(missing))


def test_p22_doc_records_the_noise_layer_reversal():
    """★ 21차 발견 2 — noise=0.005 층에서 34p 가 오히려 나았다.

    "개선은 어디서도 없다" 를 지우는 것만으로는 부족하다. **반례 자체**를
    문서에 남기지 않으면 다음 판이 같은 말을 다시 쓴다. 그래서 봉인 summary
    에서 계산한 세 층의 실패 건수를 문서가 그대로 인용하게 묶는다.
    """
    nw = _warm_summary("paired_fixed5_v4_nowarm_now")["by_objective_noise"]
    wm = _warm_summary("paired_fixed5_v4_warm")["by_objective_noise"]
    doc = (DOCS / "08_REVIEW_RESPONSE.md").read_text(encoding="utf-8")

    rows, bad = [], []
    for noise in ("0.0", "0.001", "0.005"):
        a = nw[f"pocv_dvdq|noise={noise}"]
        b = wm[f"pocv_dvdq_dqdv|noise={noise}"]
        na, nb = round(a["degenerate_frac"] * a["n"]), round(b["degenerate_frac"] * b["n"])
        rows.append((noise, na, a["n"], nb, b["n"]))
        for cell in (f"{na}/{a['n']}", f"{nb}/{b['n']}"):
            if cell not in doc:
                bad.append(f"noise={noise}: {cell} 가 §20.4 에 없다")
    assert not bad, "noise 층 반례가 문서에 없다:\n  " + "\n  ".join(bad)

    # 반례가 실제로 반례인지 — 0.005 에서만 34p 가 낫다.
    flips = [n for n, na, da, nb, db in rows if nb / db < na / da]
    assert flips == ["0.005"], (
        f"반례 층이 바뀌었다: 34p 가 나은 층 = {flips} (문서는 0.005 만 적고 있다)")


def test_random_only_multimodality_is_identical_across_the_warm_arms():
    """★ 21차 발견 3 — "warm 이 다봉성을 없앴다" 는 결과와 반대다.

    두 arm 의 `multistart_random_only` 는 같은 결정론적 난수에서 나온 같은
    restart 집합이라 **완전히 같아야 한다.** 실제로 같다. 따라서 warm 이 바꾼
    것은 다봉성이 아니라 slot 0 의 결정론적 후보가 교체된 것뿐이다
    (`base_init` → `warm`, 양 arm 후보 수 5로 동일 — 22차 발견 1).

    이 등식이 깨지면 발견 3 의 정정 근거가 사라지므로 회귀로 고정한다.
    """
    a = _warm_summary("paired_fixed5_v4_nowarm_now")["multistart_random_only"]
    b = _warm_summary("paired_fixed5_v4_warm")["multistart_random_only"]
    for obj in ("pocv_dvdq", "pocv_dvdq_dqdv"):
        assert a[obj] == b[obj], (
            f"{obj}: random-only 블록이 arm 사이에 갈렸다\n  nowarm={a[obj]}\n  warm={b[obj]}")
    assert a["pocv_dvdq_dqdv"]["multimodal_frac"] == 0.9695121951219512

    doc = (DOCS / "08_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    assert "0.969512" in doc, "§20.4 가 random-only multimodal 값을 인용하지 않는다"


# ── wiki 도구가 비-UTF8 콘솔에서도 살아남는다 (21차 리뷰 발견 10) ─────────────
_WIKI_TOOLS = Path(__file__).resolve().parent.parent.parent / "wiki" / "tools"


@pytest.mark.parametrize("tool", ["status.py", "lint.py"])
def test_wiki_tools_survive_a_cp949_console(tool):
    r"""★ 21차 리뷰 발견 10 — 입력만 UTF-8 로 고정한 것으로는 안 닫혔다.

    20차에서 `encoding='utf-8'` 을 **파일 읽기**에 넣고 13-3 을 닫았다고 했다.
    21차 리뷰어의 Windows 기본 환경에서 `status.py` 는 그래도 죽었다 — 읽기가
    아니라 **stdout** 이 CP949 였고, 본문의 em dash(U+2014)를 찍는 순간
    `UnicodeEncodeError` 가 났다.

    실측 (이 저장소에서 재현):
      수정 전 `PYTHONIOENCODING=cp949 python3 tools/status.py` → exit 1,
        `'cp949' codec can't encode character '—'`
      수정 후 → exit 0

    `lint.py` 는 지금 데이터에서는 수정 없이도 통과했다. 같은 구조라 예방으로
    함께 닫았고, 이 테스트는 **두 도구 모두** 를 비-UTF8 콘솔에서 돌려 고정한다.
    """
    import os
    import subprocess
    import sys

    if not (_WIKI_TOOLS / tool).is_file():
        pytest.skip(f"{tool} 없음 — wiki 트리 밖 체크아웃")
    env = dict(os.environ, PYTHONIOENCODING="cp949")
    r = subprocess.run([sys.executable, str(_WIKI_TOOLS / tool)],
                       cwd=str(_WIKI_TOOLS.parent), env=env,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    assert r.returncode == 0, (
        f"{tool} 이 CP949 콘솔에서 죽었다 (exit {r.returncode}):\n"
        f"{(r.stderr or '')[-800:]}")
    assert "UnicodeEncodeError" not in (r.stderr or ""), (r.stderr or "")[-800:]


# ── warm-probe 감사 강화: run_spec exact match · 봉인 결속 · 행 수준 digest ──
#   21차 리뷰 발견 7 — 기존 회귀 5건이 "주장한 변이보다 좁다".

#: 같은 digest·같은 조건집합의 warm 짝에서 **달라도 되는** manifest 키.
#: 여기 없는 키가 다르면 그 짝은 더 이상 "warm 한 축만 다른" 짝이 아니다.
_PAIR_ALLOWED_DIFF = (
    "timestamp", "elapsed_s", "attempt_id", "attempts_dir",
    "fits_parquet", "fits_seal", "run_signature",
    "warm_start", "run_spec.warm_start",
    # git_commit 은 **source_digest 가 같을 때만** 허용한다 (아래에서 강제).
    "git_commit", "git_commit_short", "run_spec.git_commit",
    "start_provenance",
)


def _flat(o, p=""):
    """중첩 dict/list → {점으로 이은 경로: 잎값}."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _flat(v, f"{p}.{k}" if p else str(k))
    elif isinstance(o, list) and o and isinstance(o[0], (dict, list)):
        for i, v in enumerate(o):
            yield from _flat(v, f"{p}[{i}]")
    else:
        yield p, o


def _allowed(key: str) -> bool:
    return any(key == a or key.startswith(a + ".") or key.startswith(a + "[")
               for a in _PAIR_ALLOWED_DIFF)


@pytest.mark.parametrize("nowarm,warm", _WARM_PAIRS)
def test_warm_pair_manifests_differ_only_by_the_warm_axis(nowarm, warm):
    """★ 21차 발견 7 항목 5 / Q2 항목 2 — normalized run_spec exact equality.

    기존 protocol 회귀는 `warm_start` 가 **non-null 인지**만 봤다.
    `adaptive=False→True`, `n_restarts=5→20`, 조건집합 해시 변경, 목적함수
    순서 변경을 전부 통과시켰다. 그 상태로는 "warm 만 다른 짝" 이라는 §20.4
    귀속의 전제를 테스트가 지키지 않는다.

    여기서는 두 manifest 를 평탄화해 **화이트리스트 밖 차이를 전부 거부**한다.
    화이트리스트는 실행 부산물(시각·경과·attempt id·출력 경로·fits 봉인·
    run_signature)과 warm 축 자신뿐이다.

    `git_commit` 은 예외적으로 허용하되 **`source_digest` 가 같을 때만** —
    두 다리 사이에 문서 커밋이 끼어 있어도 계산 경로는 같아야 한다.
    """
    a, b = _warm_manifest(nowarm), _warm_manifest(warm)
    fa, fb = dict(_flat(a)), dict(_flat(b))

    da = (a.get("run_spec") or {}).get("source_digest")
    db = (b.get("run_spec") or {}).get("source_digest")
    assert da and da == db, (
        f"{nowarm} vs {warm}: source_digest 가 다르다 ({da} vs {db}) — "
        f"git_commit 차이를 허용할 근거가 사라진다")

    assert fa.get("warm_start") is False and fb.get("warm_start") is True, (
        f"{nowarm}/{warm}: warm 축이 False→True 가 아니다")

    bad = [f"{k}: {fa.get(k)!r} ≠ {fb.get(k)!r}"
           for k in sorted(set(fa) | set(fb))
           if fa.get(k) != fb.get(k) and not _allowed(k)]
    assert not bad, (
        f"{nowarm} vs {warm}: warm 외의 축이 함께 움직였다 — "
        f"이 짝으로는 warm 효과를 귀속할 수 없다:\n  " + "\n  ".join(bad))


@pytest.mark.parametrize("leg", sorted({l for l, _ in _WARM_CLAIMS}))
def test_warm_probe_summary_fits_digest_matches_the_manifest_seal(leg):
    """★ 21차 발견 7 항목 4 — summary 의 fits digest ↔ manifest 봉인 결속.

    리뷰어가 손으로 대조해 준 등식이다. 테스트가 없으면 다음 판에서 한쪽만
    갱신돼도 아무도 모른다. summary 는 "내가 이 fits 를 채점했다" 고 적고
    manifest 는 "내가 이 fits 를 만들었다" 고 적는데, 둘이 갈리면 문서 수치의
    출처가 사라진다.
    """
    s = (_warm_summary(leg).get("_채점원본") or {}).get("fits_sha256")
    m = (_warm_manifest(leg).get("fits_seal") or {}).get("file_sha256")
    assert s and m, f"{leg}: fits digest 기록이 없다 (summary {s!r} / manifest {m!r})"
    assert s == m, (
        f"{leg}: 채점한 fits 와 봉인된 fits 가 다르다\n"
        f"  summary  {s}\n  manifest {m}")


#: §20.4 재정정 표의 (행 라벨 조각 → 다리). 표는 다리·digest·warm·33p·34p·차이 6열.
_S204_ROWS = {
    "paired_fixed5_v4` (정본)": "paired_fixed5_v4",
    "paired_fixed5_v4_nowarm_now": "paired_fixed5_v4_nowarm_now",
    "paired_fixed5_v4_warm": "paired_fixed5_v4_warm",
}


def test_warm_probe_numbers_are_bound_to_keyed_table_cells():
    """★ 21차 발견 7 항목 1 — 문자열이 문서 "어딘가" 있는지로는 부족하다.

    기존 회귀는 `f"{val:.6f}" not in doc` 였다. 목적함수 라벨·행 라벨·warm
    라벨을 서로 바꿔도 같은 숫자가 문서 어딘가에 남아 있으면 통과한다.
    실제로 이 표는 **어느 다리의 어느 목적함수인가**가 결론의 전부다.

    그래서 표를 **행 라벨로 찾아 열 위치로 읽는다**. 33p 는 4번째 칸,
    34p 는 5번째 칸이어야 한다.
    """
    doc = (DOCS / "08_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    rows = [ln for ln in doc.splitlines() if ln.lstrip().startswith("> |")]

    checked = {}
    for label, leg in _S204_ROWS.items():
        hit = [r for r in rows if label in r]
        assert len(hit) == 1, f"§20.4 표에서 '{label}' 행을 정확히 하나 못 찾았다: {len(hit)}"
        cells = [c.strip() for c in hit[0].lstrip("> ").strip("|").split("|")]
        assert len(cells) == 6, f"{leg}: 표 열 수가 6이 아니다 ({len(cells)}): {cells}"

        s = _warm_summary(leg)["by_objective"]
        want33 = f"{s['pocv_dvdq']['degenerate_frac']:.6f}"
        want34 = f"{s['pocv_dvdq_dqdv']['degenerate_frac']:.6f}"
        assert want33 in cells[3], (
            f"{leg}: 33p 칸이 봉인값과 다르다 — 문서 {cells[3]!r} vs 봉인 {want33}")
        assert want34 in cells[4], (
            f"{leg}: 34p 칸이 봉인값과 다르다 — 문서 {cells[4]!r} vs 봉인 {want34}")

        want_warm = str(_warm_manifest(leg)["run_spec"]["warm_start"])
        assert want_warm in cells[2], (
            f"{leg}: warm 칸이 manifest 와 다르다 — 문서 {cells[2]!r} vs {want_warm}")
        checked[leg] = (want33, want34)

    assert len(checked) == 3, checked


@pytest.mark.parametrize("nowarm,warm,why", _CONFOUNDED_PAIRS)
def test_confounded_pairs_really_are_confounded(nowarm, warm, why):
    """★ 21차 발견 4 — half-cell 짝은 "warm 한 축" 이 아니다. 양성으로 못박는다.

    이 짝을 `_WARM_PAIRS` 에 두면 warm 인과 귀속에 쓰이게 된다. 실제로는
    `src/fitting.py:862` 가 pristine 기준의 `p_ini` 도 **같은 warm 플래그로**
    계산하므로 원점이 함께 움직인다:

        no-warm  [1.509716, -0.418050, 1.087242, -0.084175]
        warm     [1.518503, -0.421892, 1.063315, -0.060152]

    `0.640625 → 0.184375` 은 (1) pristine `p_ini` warm 연쇄 (2) 조건별 warm
    초기값 (3) adaptive 실현 예산 변화가 합쳐진 **total protocol effect** 다.

    단순히 목록에서 빼면 다음 판이 "왜 뺐더라" 하고 되돌린다. 그래서 **교란이
    실재한다는 것 자체**를 검사한다 — 교란이 사라지면(예: 단계 3 에서
    `p_ini_warm_start` 를 분리해 원점을 고정하면) 이 테스트가 실패하고,
    그때 `_WARM_PAIRS` 로 승격하면 된다.
    """
    a, b = _warm_manifest(nowarm), _warm_manifest(warm)
    assert (a["run_spec"]["source_digest"] == b["run_spec"]["source_digest"]), \
        f"{nowarm}/{warm}: digest 가 다르다 — 교란 판정 이전의 문제다"

    pa = (a.get("run_spec") or {}).get("p_ini") or {}
    pb = (b.get("run_spec") or {}).get("p_ini") or {}
    moved = [k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k)]
    assert moved, (
        f"{nowarm} vs {warm}: `p_ini` 가 더 이상 함께 움직이지 않는다.\n"
        f"  교란이 사라졌다면 이 짝을 `_WARM_PAIRS` 로 승격하고 여기서 빼라.\n"
        f"  사유 기록: {why}")


def test_warm_probe_row_projections_are_committed_and_self_consistent():
    """★ 21차 발견 6·7 항목 3 / Q2 항목 3 — aggregate 일치는 조건별 일치가 아니다.

    지금까지 리뷰어가 확인할 수 있던 것은 "문서 숫자 == summary 숫자" 뿐이다.
    조건별 결과와 restart trace 가 그 aggregate 를 **실제로 만들었는지**,
    봉인 fits 를 다시 채점하면 같은 값이 나오는지는 확인할 수 없었다.
    원자료는 다리당 수십 MB 라 git 에 못 넣으므로, 리뷰가 제시한 대안인
    **compact keyed projection + full digest** 를 커밋한다.

    만드는 법 (원자료가 있는 기계에서):

        python docs/22p_gap/row_projection.py --all

    이 테스트는 그 산출물이 없으면 **실패한다** (skip 하지 않는다). 없는 상태가
    바로 "citation-ready 가 아니다" 라는 리뷰 판정이고, 조용히 넘어가면 그
    판정이 문서에서 사라진다.
    """
    import yaml

    # ★ 26차 P1-9·P1-10 — 초판은 `_WARM`(= frozen g1) 과 **현행** spec 을
    #   박아 뒀다. 그러면 (a) schema 를 올리는 순간 raw-lost g1 이 다시 충족
    #   불가능해지고, (b) 새 cohort 의 gzip payload 는 아무도 열지 않는다.
    #   실제로 `proj_g2/*.csv.gz` 를 지워도 통과했다. cohort 를 순회한다.
    claim_legs = sorted({l for l, _ in _WARM_CLAIMS}
                        | {l for p in _WARM_PAIRS for l in p}
                        | {l for a, b, _ in _CONFOUNDED_PAIRS for l in (a, b)}
                        | {l for p in _XDIGEST_PAIRS for l in p})
    # ★ 37차 #9 — cohort dir 이 아니라 **snapshot handle** 을 넘긴다. 경로를
    #   주면 소비자가 고정 이름을 직접 열 수 있고, 36차에 실제로 그랬다.
    targets = []                       # (cohort, leg, snapshot, schema)
    for c in _cohorts():
        snap = _snapshot(c)
        for leg in c["legs"]:
            targets.append((c["cohort_id"], leg, snap, c["pin"]["schema_version"]))

    covered = {leg for _, leg, _, _ in targets}
    missing = [l for l in claim_legs if l not in covered]
    assert not missing, (
        "인용되는 다리가 어느 cohort 에도 없다:\n  " + "\n  ".join(missing))

    bad = []
    for cohort, leg, snap, want_schema in targets:
        name = f"{leg}.projection.yaml"
        if not snap.has(name):
            bad.append(f"{cohort}/{leg}: 투영 YAML 이 없다")
            continue
        leg = f"{cohort}/{leg}"
        m = snap.yaml(name)
        # ★ 27차 P1-8 — `projection_file` 을 cohort dir 와 단순 join 하면
        #   `../warm_probe/...` 로 **다른 cohort 의 bytes** 를 대신 재해시할 수
        #   있다 (g2 payload 를 지우고 frozen g1 을 가리키는 false-green).
        for key in ("projection_file", "restart_projection_file"):
            rel = m.get(key) or ""
            if "/" in rel or "\\" in rel or rel in ("", ".", ".."):
                bad.append(f"{leg}: {key} 가 cohort 밖을 가리킨다 {rel!r}")
        if bad and bad[-1].startswith(f"{leg}: "):
            continue
        gz = _WARM / m["projection_file"]
        if not gz.is_file():
            bad.append(f"{leg}: 투영 파일 없음 {m['projection_file']}")
            continue
        # ★ 23차 자체 발견 — 초판은 `!= 2` 로 **숫자를 박아** 뒀다. 스키마가 3 이
        #   되자 정상 산출물을 거부했다. `BRANCHES.md` 의 휘발성 커밋 수와 같은
        #   형태다 (값이 바뀌는 곳에 리터럴). 정본은 `ANALYSIS_SPEC` 하나이므로
        #   거기서 읽는다. 하한 검사 대신 **정확히 같아야** 한다 — 낡은 산출물도
        #   앞선 스키마도 둘 다 거부해야 재생성 신호가 정확해진다.
        # ★ 정본은 **그 cohort 의 pin** 이다. 현행 spec 이 아니다 — frozen
        #   cohort 는 현행을 따라올 수 없기 때문이다 (25차 발견 1).
        if m.get("projection_schema") != want_schema:
            bad.append(
                f"{leg}: 투영 스키마가 {m.get('projection_schema')} 다 "
                f"(이 cohort 의 pin 은 {want_schema}). 활성 cohort 면 "
                f"`row_projection.py --out <cohort dir>` 로 재생성하고, "
                f"frozen 이면 손대지 마라")
            continue
        import gzip
        raw = gzip.decompress(gz.read_bytes())
        got = hashlib.sha256(raw).hexdigest()
        if got != m["projection_sha256"]:
            bad.append(f"{leg}: 투영 내용이 digest 와 다르다 {got[:16]} vs "
                       f"{m['projection_sha256'][:16]}")

        # ★ 22차 발견 7 — YAML 의 목적함수별 digest 를 **믿지 말고** TSV 에서
        #   다시 만든다. metadata 만 대조하면 metadata 가 틀렸을 때 통과한다.
        lines = raw.decode("utf-8").splitlines()
        head, body = lines[0], lines[1:]
        cols = head.split("\t")
        oi = cols.index("objective")
        # ★ 깨진 행에서 IndexError 로 죽으면 "무엇이 틀렸는지" 가 사라진다 —
        #   발견으로 보고한다 (변이 시험에서 실제로 크래시했다).
        ragged = [i for i, ln in enumerate(body, 2) if len(ln.split("\t")) != len(cols)]
        if ragged:
            bad.append(f"{leg}: 열 수가 머리와 다른 행 {ragged[:3]} "
                       f"(총 {len(ragged)}건)")
            continue
        for obj, want in (m.get("by_objective_sha256") or {}).items():
            sub = [ln for ln in body if ln.split("\t")[oi] == obj]
            blob = ("\n".join([head, *sub]) + "\n").encode("utf-8")
            if hashlib.sha256(blob).hexdigest() != want["sha256"]:
                bad.append(f"{leg}/{obj}: 부분 digest 가 TSV 재계산과 다르다")
            if len(sub) != want["n_rows"]:
                bad.append(f"{leg}/{obj}: 행 수 {len(sub)} vs 기록 {want['n_rows']}")

        # ★ 27차 P1-8 — 압축 해제 행 수를 top-level 기록과 대조한다.
        if len(body) != m.get("n_rows"):
            bad.append(f"{leg}: 투영 행 수 {len(body)} ≠ 기록 {m.get('n_rows')}")
        objs = {ln.split("\t")[oi] for ln in body}
        keyed = set((m.get("by_objective_sha256") or {}))
        if objs != keyed:
            bad.append(f"{leg}: by_objective key 가 불완전하다 "
                       f"(TSV {sorted(objs)} vs 기록 {sorted(keyed)})")

        # ★ 22차 발견 5 — 전체 semantic 대조와 fits 삼중 일치를 요구한다.
        v = m.get("재계산_검증") or {}
        if v.get("전체_일치") is not True:
            bad.append(f"{leg}: 봉인 summary **전체** 재계산 불일치 {v.get('불일치')}")
        if v.get("fits_삼중일치") is not True:
            bad.append(f"{leg}: 읽은 fits 바이트 ≠ summary 가 채점한 fits")
        if m.get("fits_봉인일치") is not True:
            bad.append(f"{leg}: 읽은 fits 바이트 ≠ manifest 봉인")
        if not (m.get("analyzer") or {}).get("row_projection_py_sha256"):
            bad.append(f"{leg}: 분석기 provenance 가 없다")
        # restart 수준 투영도 있어야 한다 (발견 5 항목 4)
        rp = m.get("restart_projection_file")
        if not rp or not snap.has(rp):
            bad.append(f"{leg}: restart 수준 투영이 없다")
        else:
            r_raw = gzip.decompress(snap.blob(rp))
            if hashlib.sha256(r_raw).hexdigest() != m.get("restart_projection_sha256"):
                bad.append(f"{leg}: restart 투영이 digest 와 다르다")
            r_body = r_raw.decode("utf-8").splitlines()[1:]
            if len(r_body) != m.get("n_restart_rows"):
                bad.append(f"{leg}: restart 행 수 {len(r_body)} ≠ 기록 "
                           f"{m.get('n_restart_rows')}")
    assert not bad, "행 수준 투영이 자기 근거와 어긋난다:\n  " + "\n  ".join(bad)


def test_warm_pairs_agree_row_by_row_on_the_first_objective():
    """★ 21차 Q2 항목 3 — "aggregate fraction 동일 ≠ 조건별 동일".

    warm 귀속의 핵심 sanity check 는 연쇄 1번째가 **한 조건도 빠짐없이** 같다는
    것이다. 총 비율만 같고 조건들이 서로 뒤바뀌어도 기존 회귀는 통과했다.
    여기서는 33p 부분 투영의 sha256 을 통째로 비교한다.
    """
    import yaml

    need = [l for p in _WARM_PAIRS for l in p]
    missing = [l for l in need if not (_WARM / f"{l}.projection.yaml").is_file()]
    assert not missing, (
        "warm 짝의 행 수준 투영이 없다 — "
        "`python docs/22p_gap/row_projection.py --all` 후 커밋할 것: " + str(missing))

    for nowarm, warm in _WARM_PAIRS:
        a = yaml.safe_load((_WARM / f"{nowarm}.projection.yaml").read_text(encoding="utf-8"))
        b = yaml.safe_load((_WARM / f"{warm}.projection.yaml").read_text(encoding="utf-8"))
        assert a["analysis_spec_sha256"] == b["analysis_spec_sha256"], (
            f"{nowarm}/{warm}: 투영 규격이 달라 digest 를 비교할 수 없다")

        pa = a["by_objective_sha256"]["pocv_dvdq"]
        pb = b["by_objective_sha256"]["pocv_dvdq"]
        assert pa["n_rows"] == pb["n_rows"], (
            f"{nowarm}/{warm}: 33p 행 수가 다르다 {pa['n_rows']} vs {pb['n_rows']}")
        assert pa["sha256"] == pb["sha256"], (
            f"{nowarm} vs {warm}: 33p 가 **조건별로는** 갈렸다 — 총 비율만 같았다.\n"
            f"  {pa['sha256'][:16]} vs {pb['sha256'][:16]}\n"
            f"  연쇄 1번째는 warm 경로에 닿지 않으므로 행 단위로 동일해야 한다.")

        # 34p 는 반대로 **달라야** 한다 — 같으면 warm 이 아무것도 안 한 것이다.
        qa = a["by_objective_sha256"]["pocv_dvdq_dqdv"]["sha256"]
        qb = b["by_objective_sha256"]["pocv_dvdq_dqdv"]["sha256"]
        assert qa != qb, f"{nowarm}/{warm}: 34p 투영이 동일하다 — warm 이 무효였다는 뜻"


#: 교차-digest 짝 중 **전 열·전 행이 동일**하다고 주장하는 짝.
#: 실측(2026-08-20, 행 수준 투영): `cbe040612aa4415a` 로 완전히 같다.
_XDIGEST_EXACT = [("fit_22p_seed_404_hc_warm_now", "fit_22p_seed_404_hc")]



def _row_projection_module():
    """`docs/22p_gap/row_projection.py` 를 import 한다 (원자료 없이 가능)."""
    import importlib.util

    src = _REPO / "docs" / "22p_gap" / "row_projection.py"
    spec = importlib.util.spec_from_file_location("_rp_mod", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _current_projection_schema() -> int:
    """산출물이 따라야 할 스키마 번호의 **정본**."""
    return int(_row_projection_module().ANALYSIS_SPEC["schema_version"])


def _projection(leg: str) -> dict:
    import yaml
    return yaml.safe_load((_WARM / f"{leg}.projection.yaml").read_text(encoding="utf-8"))


@pytest.mark.parametrize("a,b", _XDIGEST_EXACT)
def test_cross_digest_exact_pair_reproduces_row_for_row(a, b):
    """★ LEG_INVENTORY §22 의 "교차-digest 완전 재현" 을 **행 수준으로** 올린다.

    §22 는 aggregate 네 값(거짓 분리·bias·중앙값·원점)이 같다는 근거로
    "`7250c6e6` → `a72c0f3a` 사이의 `fitting.py +98` · `halfcell.py +144` 가
    이 경로의 수치를 전혀 안 바꿨다" 고 썼다. aggregate 일치는 조건별 일치가
    아니므로(21차 Q2) 그 문장은 원래 근거보다 강했다.

    행 수준 투영이 생기면서 이제 **전 행·전 열** 을 비교할 수 있다. 실측:

        fit_22p_seed_404_hc          (7250c6e6)  cbe040612aa4415a
        fit_22p_seed_404_hc_warm_now (a72c0f3a)  cbe040612aa4415a

    1280행 × 20열이 자리별로 같다 — truth·hats·J·restart source 까지.
    이것이 §22 주장의 **실제 근거**다.

    ⚠ 범위: "이 다리의 경로에서 불활성" 이지 "그 코드 구간이 어디서나 무해" 가
      아니다. 무왜곡 404 half-cell · warm=True 한 조건집합에서의 관측이다.
      21차 발견 5 가 지적한 5 mV 짝은 여기 없다 — 그쪽은 warm 축도 함께 달라
      애초에 exact 짝이 아니다.
    """
    pa, pb = _projection(a), _projection(b)
    da = _warm_manifest(a)["run_spec"]["source_digest"]
    db = _warm_manifest(b)["run_spec"]["source_digest"]
    assert da != db, f"{a}/{b}: digest 가 같다 — 이 목록의 전제가 깨졌다"
    assert pa["analysis_spec_sha256"] == pb["analysis_spec_sha256"]
    assert pa["n_rows"] == pb["n_rows"], f"행 수가 다르다 {pa['n_rows']}/{pb['n_rows']}"
    assert pa["projection_sha256"] == pb["projection_sha256"], (
        f"{a}({da[:8]}) vs {b}({db[:8]}): 행 수준 재현이 깨졌다\n"
        f"  {pa['projection_sha256'][:16]} vs {pb['projection_sha256'][:16]}\n"
        f"  LEG_INVENTORY §22 의 '교차-digest 완전 재현' 근거가 사라진다.")


@pytest.mark.parametrize("a,b", _XDIGEST_PAIRS)
def test_cross_digest_pairs_agree_row_by_row_on_the_first_objective(a, b):
    """★ 21차 Q2 — 교차-digest 짝의 33p 일치도 **조건별**로 확인한다.

    기존 회귀는 aggregate `degenerate_frac` 만 봤다. 총 비율이 같아도 조건들이
    서로 뒤바뀌었을 수 있다. 33p 부분 투영 digest 로 올린다.

    ⚠ 이것이 무엇을 말하고 무엇을 말하지 않는가 (21차 발견 5):
      **말한다** — 이 짝의 연쇄 1번째는 digest 가 달라도 행 단위로 동일하다.
      **말하지 않는다** — 그 digest 구간이 34p 경로에도 무해했다는 것.
      warm 인과나 "paired 밖에서도 계통적" 의 근거로 쓸 수 없다.
    """
    pa, pb = _projection(a), _projection(b)
    assert pa["analysis_spec_sha256"] == pb["analysis_spec_sha256"]
    ka = pa["by_objective_sha256"]["pocv_dvdq"]
    kb = pb["by_objective_sha256"]["pocv_dvdq"]
    assert ka["n_rows"] == kb["n_rows"], f"{a}/{b}: 33p 행 수가 다르다"
    assert ka["sha256"] == kb["sha256"], (
        f"{a} vs {b}: 33p 가 조건별로는 갈렸다 — 총 비율만 같았다\n"
        f"  {ka['sha256'][:16]} vs {kb['sha256'][:16]}")


# ── 단계 3 계약이 인용하는 코드 사실이 살아 있는가 ───────────────────────────
_CONTRACT = DOCS / "22p_gap" / "STAGE3_CONTRACT.md"
_SRC = DOCS.parent / "src"


def test_stage3_contract_cites_live_code_facts():
    """★ 21차 순서 4 — 계약의 §0 교란 세 가지는 **현재 코드의 사실**이어야 한다.

    이 문서는 "지금 이렇게 돼 있으니 이렇게 바꾸자" 는 제안서다. 근거로 든
    코드 사실이 이미 바뀌었거나 애초에 틀렸다면 제안 전체가 근거를 잃는다.
    그래서 세 교란을 **코드에서 다시 확인**한다.

    ★ 단계 3 을 구현하면 이 테스트는 **깨져야 정상**이다 — 교란이 사라지는
      것이 구현의 목적이기 때문이다. 그때 계약 §0 을 "이랬었다" 로 고치고
      이 테스트를 그 시점 기준으로 다시 쓴다. 조용히 통과하면 안 된다.
    """
    assert _CONTRACT.is_file(), "STAGE3_CONTRACT.md 가 없다"
    doc = _CONTRACT.read_text(encoding="utf-8")

    fitting = (_SRC / "fitting.py").read_text(encoding="utf-8").splitlines()
    grid = (_SRC / "grid.py").read_text(encoding="utf-8")

    # 교란 1 — 원점 fitting 이 조건 task 를 그대로 물려받는다 (warm 플래그 포함)
    ini = [i for i, ln in enumerate(fitting, 1)
           if "_fit_one({**ref_candidates[0]" in ln]
    assert len(ini) == 1, f"원점 fitting 호출을 정확히 하나 못 찾았다: {ini}"
    line = fitting[ini[0] - 1]
    assert "warm_start" not in line and "n_restarts" not in line, (
        f"src/fitting.py:{ini[0]} 이 원점 protocol 을 따로 지정하기 시작했다 — "
        f"교란 1 이 해소됐다면 계약 §0·§1 을 갱신하라:\n  {line.strip()}")
    assert f"src/fitting.py:{ini[0]}" in doc, (
        f"계약이 인용한 줄번호가 낡았다 — 실제는 src/fitting.py:{ini[0]}")

    # 교란 3 — cond_id 가 noise 를 포함하고, restart seed 가 cond_id 에서 나온다
    assert "noise: float" in grid and "seed: int" in grid, \
        "Condition 에서 noise/seed 필드가 사라졌다 — 계약 §2.1 갱신 필요"
    assert "hashlib.sha1(blob.encode()).hexdigest()[:12]" in grid, \
        "cond_id 해시 방식이 바뀌었다 — 계약 §2.1 갱신 필요"
    seed_lines = [i for i, ln in enumerate(fitting, 1)
                  if '"seed": int(hashlib.sha1(cond_id.encode())' in ln]
    assert len(seed_lines) == 1, f"restart seed 유도를 못 찾았다: {seed_lines}"
    assert f"src/fitting.py:{seed_lines[0]}" in doc, (
        f"계약이 인용한 줄번호가 낡았다 — 실제는 src/fitting.py:{seed_lines[0]}")

    # 교란 2 — adaptive 조기 종료가 여전히 예산을 조건별로 줄인다
    src = "\n".join(fitting)
    assert "if adaptive and k == 1 and len(results) == 2:" in src, \
        "adaptive 조기 종료 구조가 바뀌었다 — 계약 §0 교란 2 갱신 필요"

    # §4 plateau tolerance 가 코드의 실제 기본값과 같은가
    assert "agree_tol: float = 1e-3" in src, \
        "agree_tol 기본값이 바뀌었다 — 계약 §4 의 tolerance 표 갱신 필요"


def test_stage3_contract_declares_what_it_cannot_do():
    """★ 계약이 자기 한계를 적고 있는가 — 이 저장소가 반복해 틀린 지점이다.

    19~21차에서 철회한 것들의 공통 형태는 "관측을 그 관측이 지지하지 않는
    범위까지 밀어붙인 것" 이다 (철회[OP_EQUIV]·[NOISE_INERT]·[R20_RX]·
    [WARM_NO_IMPROVE_ANY]). 설계 문서가 그 습관을 그대로 가져가면 구현이
    끝난 뒤에 또 철회한다. 그래서 한계 절을 **구조로** 요구한다.
    """
    doc = _CONTRACT.read_text(encoding="utf-8")
    # ★ 절 번호에 걸지 않는다 — v2 에서 §8 → §12 로 옮겨가며 테스트가 깨졌다.
    #   요구하는 것은 "한계 절이 있는가" 이지 "그것이 몇 번인가" 가 아니다.
    m = re.search(r"^## \d+\.\s*이 계약이 스스로 (못|지키지 못)", doc, re.M)
    assert m, "계약에 한계 절('이 계약이 스스로 못 하는 것')이 없다"
    tail = doc[m.start():]
    need = [
        ("잡음 *지형*", "pair_group_id 로도 잡음 지형 축은 분리되지 않는다"),
        ("plateau", "plateau 가 이 격자·화학·bound 의 성질이라는 한정"),
        ("2×2", "2×2 가 half-cell 한 격자에서만 성립한다는 한정"),
        ("기술통계", "transition table 이 기술통계라는 한정"),
    ]
    missing = [why for key, why in need if key not in tail]
    assert not missing, "계약 §8 이 빠뜨린 한계: " + "; ".join(missing)


_BRANCHES = DOCS.parent.parent / "BRANCHES.md"


def test_branch_map_records_no_volatile_commit_counts():
    """★ 세 번째다 — `BRANCHES.md` 가 자기 규칙을 스스로 어겼다.

    20차 리뷰 발견 13-2 가 이 문서의 stale 커밋 수(88→89→90)를 지적했고,
    그래서 문서 자신이 "뒤처진 커밋 수는 여기 적지 않는다" 는 규칙을 달았다.
    그런데 21차 발견 9 를 정정하면서 `0 234` 를 다시 적었고, 22차 요청문을
    쓰는 사이에 `240` 이 돼 또 stale 이 됐다. 이 문서를 고치는 커밋 자체가
    그 수를 바꾸므로 **사람이 지킬 수 없는 규칙**이다 → 기계로 옮긴다.

    불변인 사실만 남긴다: `--is-ancestor` exit 0 · 왼쪽 카운트 0 ·
    고유 커밋 0개. 오른쪽 카운트는 재현 명령으로 그 자리에서 센다.
    """
    if not _BRANCHES.is_file():
        pytest.skip("BRANCHES.md 없음")
    lines = _BRANCHES.read_text(encoding="utf-8").splitlines()

    # `0 234` / `0/234` 처럼 **양쪽 다 숫자인** 카운트 쌍만 잡는다.
    # `0/518`(측정 건수)·`5/81` 같은 실측 분수는 이 문서에 없고, 있어도
    # rev-list 문맥에서만 본다.
    pair = re.compile(r"(?<!\d)0\s*[ /]\s*(\d{2,})(?!\d)")
    bad = []
    for i, ln in enumerate(lines, 1):
        if "rev-list" not in ln and "--count" not in ln and "커밋" not in ln:
            continue
        if ln.lstrip().startswith(("#", "for ", "[ ", "BR=", "n=", "git ")):
            continue                      # 재현 명령 블록 자체는 대상이 아니다
        m = pair.search(ln)
        if m:
            bad.append(f"BRANCHES.md:{i}  {m.group(0)!r} — {ln.strip()[:70]}")
    assert not bad, (
        "휘발성 커밋 수가 다시 박혔다 (20차 발견 13-2 · 21차 재발):\n  "
        + "\n  ".join(bad)
        + "\n  불변인 사실만 적어라 — is-ancestor exit 0 · 왼쪽 0 · 고유 커밋 0개.")


# ── warm 이 후보를 더하는가 교체하는가 (22차 리뷰 발견 1) ────────────────────
#: 커밋된 투영에서 실측한 후보 구성. `restart_sources` 는 source 별 개수다.
#: 22차 리뷰가 반증한 것: warm arm 은 후보가 **하나 늘지 않는다** — slot 0 의
#: 결정론적 후보가 `base_init` → `warm` 으로 **교체**된다.
_SLOT_EXPECT = {
    ("paired_fixed5_v4_nowarm_now", "pocv_dvdq"):      "base_init=1;random=4",
    ("paired_fixed5_v4_nowarm_now", "pocv_dvdq_dqdv"): "base_init=1;random=4",
    ("paired_fixed5_v4_warm", "pocv_dvdq"):            "base_init=1;random=4",
    ("paired_fixed5_v4_warm", "pocv_dvdq_dqdv"):       "random=4;warm=1",
}


def _projection_rows(leg: str) -> list[dict]:
    import csv
    import gzip
    import yaml
    m = yaml.safe_load((_WARM / f"{leg}.projection.yaml").read_text(encoding="utf-8"))
    raw = gzip.decompress((_WARM / m["projection_file"]).read_bytes())
    return list(csv.DictReader(raw.decode("utf-8").splitlines(), delimiter="\t"))


def test_warm_replaces_the_deterministic_slot_it_does_not_add_one():
    """★ 22차 리뷰 발견 1 — 21차 실험은 union 이 아니라 slot 교체였다.

    §20.4 초판은 "warm 이 결정론적 계산점을 하나 보탰다" 고 썼고, 계약 §2.5 는
    그 전제 위에서 후보 수와 비용을 정의했다. **둘 다 틀렸다.**

    `src/fitting.py` 의 restart 루프는 정확히 `n_restarts` 번 돈다:

        n_max = max(1, n_restarts)
        for k in range(n_max):
            x0 = init if k == 0 else rng.uniform(lb, ub)
            src = ("warm" if warm_init else "base_init") if k == 0 else "random"

    즉 slot 0 은 `base_init` **또는** `warm` 이고 총 후보 수는 같다. 커밋된
    투영이 3,069조건 전부에서 그것을 보인다.

    이 사실이 결론을 바꾼다 — 34p 개선을 "warm 후보가 좋다" 로만 읽을 수 없다.
    **`base_init` 이 34p 에서 나쁜 후보였다**는 해석과 구별되지 않는다.

    문장 검색이 아니라 **실제 후보 배열**을 고정한다 (발견 1 의 요구).
    """
    import collections
    bad = []
    for (leg, obj), want in _SLOT_EXPECT.items():
        rows = [r for r in _projection_rows(leg) if r["objective"] == obj]
        got = collections.Counter((r["restart_sources"], r["n_restarts"]) for r in rows)
        if len(got) != 1:
            bad.append(f"{leg}/{obj}: 후보 구성이 조건마다 다르다 {dict(got)}")
            continue
        (src, n), _ = got.most_common(1)[0]
        if src != want:
            bad.append(f"{leg}/{obj}: 후보 구성 {src!r} (기대 {want!r})")
        if int(n) != 5:
            bad.append(f"{leg}/{obj}: 후보 수 {n} (기대 5)")
    assert not bad, "후보 배열이 바뀌었다:\n  " + "\n  ".join(bad)

    # 핵심 불변량 — 두 arm 의 총 후보 수가 같다 (union 이 아니다)
    nw = {r["cond_id"]: r for r in _projection_rows("paired_fixed5_v4_nowarm_now")
          if r["objective"] == "pocv_dvdq_dqdv"}
    wm = {r["cond_id"]: r for r in _projection_rows("paired_fixed5_v4_warm")
          if r["objective"] == "pocv_dvdq_dqdv"}
    assert set(nw) == set(wm), "두 arm 의 조건 집합이 다르다"
    diff = [c for c in nw if nw[c]["n_restarts"] != wm[c]["n_restarts"]]
    assert not diff, (
        f"후보 수가 조건 {len(diff)}개에서 갈렸다 — union 이면 여기가 갈린다. "
        f"예: {diff[:3]}")

    # 그리고 base_init 은 warm arm 에서 사라져야 한다
    assert all("base_init" in r["restart_sources"] for r in nw.values())
    assert not any("base_init" in r["restart_sources"] for r in wm.values()), \
        "warm arm 에 base_init 이 남아 있다 — 그러면 교체가 아니라 추가다"


def test_warm_contrast_reports_the_paired_transition_table():
    """★ 22차 리뷰 발견 1·4 — aggregate 차이 하나로 보고하면 안 된다.

    `909 → 928` 은 +19 failures 지만, 조건별로 보면 훨씬 많이 움직였다.
    투영에서 직접 센 값 (recoverable 1,476조건):

      no-warm 34p → warm 34p :  fail→pass 366 · pass→fail 4 (순 362, 총 370)
      warm arm 33p → 34p     :  pass→fail 186 · fail→pass 167 → discordance 23.9%

    두 번째가 특히 중요하다 — aggregate 는 +19 인데 **353조건(23.9%)이 서로
    다르게 판정**된다. "두 목적함수가 비슷하다" 는 서술이 감추는 것이 이것이다.

    문서가 이 전이표를 싣지 않으면 실패한다.
    """
    import collections
    wm_rows = _projection_rows("paired_fixed5_v4_warm")
    wm = {(r["cond_id"], r["objective"]): r for r in wm_rows}

    rec = sorted({c for (c, o), r in wm.items()
                  if o == "pocv_dvdq_dqdv" and r["recoverable"] == "1"})
    assert len(rec) == 1476, len(rec)

    nw34 = {r["cond_id"]: r for r in _projection_rows("paired_fixed5_v4_nowarm_now")
            if r["objective"] == "pocv_dvdq_dqdv"}
    t1 = collections.Counter((nw34[c]["degenerate"], wm[(c, "pocv_dvdq_dqdv")]["degenerate"])
                             for c in rec)
    t2 = collections.Counter((wm[(c, "pocv_dvdq")]["degenerate"],
                              wm[(c, "pocv_dvdq_dqdv")]["degenerate"]) for c in rec)

    assert t1[("1", "0")] == 366 and t1[("0", "1")] == 4, dict(t1)
    disc = t2[("1", "0")] + t2[("0", "1")]
    assert disc == 353, dict(t2)

    doc = (DOCS / "08_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    need = ["366", "353/1476", "23.9%"]
    missing = [s for s in need if s not in doc]
    assert not missing, f"§20.4 가 전이표 값을 싣지 않았다: {missing}"


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

#: 원장 관할에서 **명시적으로** 빼는 것. 여기 없으면 전부 관할이다.
#: ★ 23차 발견 7 — 초판은 파일 5개를 하드코딩했다. 새 claim-bearing 문서가
#:   생기면 자동으로 들어오지 않아, "양방향 완전성" 이 관할 밖에서는 성립하지
#:   않았다. 목록을 **제외 기준**으로 뒤집는다 (기본은 포함).
_CLAIM_SCOPE_EXCLUDE = (
    "degradation-degeneracy/docs/22p_gap/GATE",   # 게이트 리뷰 요청문 — 왕복 기록
    "wiki/raw/",                                   # 불변 원본 (SCHEMA.md 3-layer)
    "wiki/inbox/",                                 # 미처리 대기 큐
    "degradation-degeneracy/artifacts/",           # 봉인 산출물
)


def _claim_scope() -> list[str]:
    """`docs/**/*.md` + `wiki/**/*.md` 에서 제외 목록을 뺀 전부.

    하드코딩 목록이 아니라 **발견**이다 — 새 문서가 claim ID 를 쓰기 시작하면
    자동으로 검사 대상이 된다.
    """
    out = []
    for base in ("degradation-degeneracy/docs", "wiki"):
        for f in sorted((_REPO_ROOT / base).rglob("*.md")):
            rel = f.relative_to(_REPO_ROOT).as_posix()
            if any(rel.startswith(x) for x in _CLAIM_SCOPE_EXCLUDE):
                continue
            out.append(rel)
    return out


_CLAIM_SCOPE = _claim_scope()


def test_claim_registry_is_complete_in_both_directions():
    """★ 22차 리뷰 발견 7 — 원장→파일만 봤고 파일→원장은 안 봤다.

    그 결과 문서에 `철회[MV_1P5]`·`철회[THRESH_FREE]`·`철회[FPR_AS_FDR]` 이
    있는데 원장에는 없었다. 등록되지 않은 ID 는 금지어 검사를 **하나도** 받지
    않으므로, 배너만 있고 본문은 자유로운 상태가 된다 — 발견 8 이 지적한 바로
    그 구조가 ID 별로 되살아난다.

    양방향으로 닫는다: 문서에 나타난 모든 claim ID 가 원장에 있어야 한다.
    """
    reg = {c["id"] for c in _claim_status()["claims"]}
    seen: dict[str, list[str]] = {}
    for rel in _CLAIM_SCOPE:
        f = _REPO_ROOT / rel
        if not f.is_file():
            continue
        txt = f.read_text(encoding="utf-8")
        # ★ QUARANTINE 마커는 **파서와 같은 규칙**으로 센다 — 줄 전체가 마커일
        #   때만 진짜 울타리다. 그러지 않으면 코드블록 안의 설명용 인용
        #   (`<!-- QUARANTINE:<claim> -->`)이 미등록 ID 로 잡힌다.
        for ln in txt.splitlines():
            m = _Q_OPEN.match(ln.strip())
            if m:
                seen.setdefault(m.group(1), []).append(rel)
        for m in re.finditer(r"철회\[([A-Z0-9_]+)\]", txt):
            seen.setdefault(m.group(1), []).append(rel)
    unknown = {k: sorted(set(v)) for k, v in seen.items() if k not in reg}
    assert not unknown, (
        "문서가 쓰는 claim ID 가 원장에 없다 — 금지어 검사를 전혀 안 받는다:\n  "
        + "\n  ".join(f"{k}: {v}" for k, v in sorted(unknown.items())))

    # ★ 23차 발견 7 두 번째 층 — ID 가 등록돼 있어도, **그 파일이 claim.files 에
    #   없으면** 금지어 검사는 그 파일을 보지 않는다. 배너만 있고 본문은 자유인
    #   상태가 파일 단위로 되살아난다. 실제로 `AXIS_RANK`·`R20_RX` 의 files 에
    #   wiki 가 없어 wiki 가 그 의미를 다시 주장해도 잡히지 않았다.
    claims = {c["id"]: c for c in _claim_status()["claims"]}
    gaps = []
    for cid, rels in sorted(seen.items()):
        c = claims[cid]
        if c["record"] == "legacy_section_marker":
            continue                       # (구) 체계가 절 단위로 본다
        listed = set(c["files"])
        for rel in sorted(set(rels)):
            # 원장의 files 는 프로젝트 상대경로다 (docs/…), scope 는 repo 상대다
            short = rel.split("degradation-degeneracy/", 1)[-1]
            if short not in listed and rel not in listed:
                gaps.append(f"{cid}: {rel} 이 금지어 검사 대상이 아니다 "
                            f"(files={sorted(listed)})")
    assert not gaps, (
        "claim ID 를 쓰는 파일이 그 claim 의 files 에 없다 — "
        "그 파일에서는 금지어가 자유롭다:\n  " + "\n  ".join(gaps))


def test_quarantine_fences_are_structurally_balanced():
    """★ 22차 리뷰 발견 7 — 닫는 울타리가 빠지면 이후 본문 전체가 격리된다.

    `_active_text` 는 depth 로 세므로, 여는 울타리만 있고 닫는 것이 없으면
    **그 뒤 문서 전부**가 활성 본문에서 빠진다. 금지어 검사가 조용히 통과한다.
    검사기 자신의 실패 모드라 구조 검사를 따로 둔다.

    함께 막는 것: 중첩(격리 안의 격리 — 의도가 모호하다), 짝 없는 닫기.
    """
    bad = []
    for rel in _CLAIM_SCOPE:
        f = _REPO_ROOT / rel
        if not f.is_file():
            continue
        depth, opened = 0, []
        for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            s = ln.strip()
            o, c = _Q_OPEN.match(s), _Q_CLOSE.match(s)
            if o:
                if depth:
                    bad.append(f"{rel}:{i} 중첩 울타리 (열린 것: {opened[-1]})")
                depth += 1
                opened.append(f"{o.group(1)}@{i}")
            elif c:
                if not depth:
                    bad.append(f"{rel}:{i} 짝 없는 닫기")
                else:
                    depth -= 1
                    opened.pop()
        if depth:
            bad.append(f"{rel}: 닫히지 않은 울타리 {opened} — 이후 본문 전체가 검사에서 빠진다")
    assert not bad, "QUARANTINE 울타리 구조 오류:\n  " + "\n  ".join(bad)


# ── /lean-review 의 base 결정이 세 git 상태에서 옳은가 (22차 발견 8) ──────────
_LEAN = _REPO_ROOT / ".claude" / "commands" / "lean-review.md"


def _lean_base_script() -> str:
    """커맨드 문서의 첫 bash 블록 = 실제로 사람이 복붙하는 것."""
    txt = _LEAN.read_text(encoding="utf-8")
    m = re.search(r"```bash\n(.*?)```", txt, re.S)
    assert m, "lean-review.md 에 bash 블록이 없다"
    return m.group(1)


def test_lean_review_base_resolution_in_four_git_states():
    """★ 22차 리뷰 발견 8 — 두 번 틀린 자리라 문서가 아니라 **동작**을 고정한다.

    초판: `origin/$(git rev-parse --abbrev-ref HEAD)` — detached 에서
      `--abbrev-ref HEAD` 가 문자열 `HEAD` 를 반환해 `origin/HEAD` 가 된다.
    2판: upstream 조회 실패 시 `origin/HEAD` 로 **자동 대체** — detached 에서
      결국 기본 브랜치와 비교한다. 20차 발견 11 이 지적한 증상이 그대로 남았다.

    세 상태를 진짜 git 저장소로 만들어 돌린다:
      (a) attached + upstream 있음 → upstream 을 쓴다
      (b) attached + upstream 없음 → 중단 (exit 1)
      (c) detached HEAD           → 중단 (exit 1)
    """
    import subprocess
    import tempfile

    script = _lean_base_script()
    # `git diff` 는 실제로 돌릴 필요 없다 — base 결정만 본다.
    script = script.replace('git diff "$base...HEAD"', 'echo "BASE=$base"')

    def run(cwd: str, arg: str = "") -> subprocess.CompletedProcess:
        return subprocess.run(["bash", "-c", f"set -- {arg}\n{script}"],
                              cwd=cwd, capture_output=True, text=True)

    def git(cwd: str, *a: str) -> None:
        subprocess.run(["git", *a], cwd=cwd, check=True,
                       capture_output=True, text=True)

    with tempfile.TemporaryDirectory() as tmp:
        upstream = Path(tmp) / "up"
        upstream.mkdir()
        git(str(upstream), "init", "-q", "-b", "main")
        git(str(upstream), "config", "user.email", "t@t")
        git(str(upstream), "config", "user.name", "t")
        (upstream / "a.txt").write_text("1", encoding="utf-8")
        git(str(upstream), "add", "-A")
        git(str(upstream), "commit", "-qm", "init")

        work = Path(tmp) / "work"
        subprocess.run(["git", "clone", "-q", str(upstream), str(work)],
                       check=True, capture_output=True)
        git(str(work), "config", "user.email", "t@t")
        git(str(work), "config", "user.name", "t")

        # (a) attached + upstream
        r = run(str(work))
        assert r.returncode == 0, f"(a) 중단됐다: {r.stdout}{r.stderr}"
        assert "BASE=origin/main" in r.stdout, f"(a) base={r.stdout!r}"

        # (b) attached, upstream 없는 새 브랜치
        git(str(work), "checkout", "-qb", "feature")
        r = run(str(work))
        assert r.returncode == 1, (
            f"(b) upstream 이 없는데 중단하지 않았다 — {r.stdout!r}")
        assert "origin/HEAD" not in r.stdout.replace(
            "origin/HEAD 로 자동 대체하지 않는다", ""), \
            f"(b) origin/HEAD 로 대체했다: {r.stdout!r}"

        # (c) detached HEAD
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(work),
                             capture_output=True, text=True, check=True).stdout.strip()
        git(str(work), "checkout", "-q", sha)
        r = run(str(work))
        assert r.returncode == 1, (
            f"(c) detached 인데 중단하지 않았다 — {r.stdout!r}")
        assert "BASE=" not in r.stdout, f"(c) base 를 정해 버렸다: {r.stdout!r}"

        # (d) 인자를 주면 그것을 쓴다 (detached 여도)
        r = run(str(work), "main")
        assert r.returncode == 0 and "BASE=main" in r.stdout, \
            f"(d) 명시 base 가 무시됐다: {r.stdout!r}"


def _restart_rows(leg: str) -> list[dict]:
    import csv
    import gzip
    import yaml
    m = yaml.safe_load((_WARM / f"{leg}.projection.yaml").read_text(encoding="utf-8"))
    assert m.get("restart_projection_file"), (
        f"{leg}: restart 수준 투영이 없다 (스키마 {m.get('projection_schema')}). "
        f"원자료가 있는 기계에서 `python docs/22p_gap/row_projection.py --all` 재실행 필요")
    raw = gzip.decompress((_WARM / m["restart_projection_file"]).read_bytes())
    return list(csv.DictReader(raw.decode("utf-8").splitlines(), delimiter="\t"))


def _recompute_random_only_kinds(leg: str) -> dict:
    """restart 투영만으로 `multistart_random_only` 의 분류를 다시 만든다.

    규칙은 `src/scoring.py::multistart_diagnostics` 를 따른다:
        random restart 만 남긴다 (source == 'random'), 2개 미만이면 제외
        near      = |J − J_best| ≤ 1e-3 · max(1, |J_best|)
        spread_*  = max_j |p_j − p_best,j|
        n_near ≥ 2 이고 spread_near > 1e-2      → flat_valley
        n_near == 1 이고 spread_all  > 1e-2     → multimodal
        그 밖                                    → unique_min
    """
    import collections
    import math

    # ★ 봉인 summary 는 **복원가능군에서만** 센다 (`rec_df = df[df.recoverable]`).
    #   restart 투영은 전 행을 담으므로 여기서 같은 모집단으로 맞춘다 — 초판은
    #   이 필터를 빼먹어 n 이 3069 vs 1476 으로 갈렸고 테스트가 잡았다.
    rec = {(r["cond_id"], r["objective"])
           for r in _projection_rows(leg) if r["recoverable"] == "1"}

    by: dict = collections.defaultdict(list)
    for r in _restart_rows(leg):
        if r["source"] != "random":
            continue
        if (r["cond_id"], r["objective"]) not in rec:
            continue
        try:
            J = float(r["J"])
            p = [float(r[f"p{i}"]) for i in range(4)]
        except ValueError:
            continue
        if not math.isfinite(J) or not all(map(math.isfinite, p)):
            continue
        by[(r["cond_id"], r["objective"])].append((J, p))

    out: dict = collections.defaultdict(collections.Counter)
    for (_c, obj), rs in by.items():
        if len(rs) < 2:
            continue
        j_best, p_best = min(rs, key=lambda t: t[0])
        d = [max(abs(a - b) for a, b in zip(p, p_best)) for _J, p in rs]
        near = [abs(J - j_best) <= 1e-3 * max(1.0, abs(j_best)) for J, _p in rs]
        n_near = sum(near)
        spread_all = max(d)
        spread_near = max(x for x, n in zip(d, near) if n)
        if n_near >= 2 and spread_near > 1e-2:
            kind = "flat_valley"
        elif n_near == 1 and spread_all > 1e-2:
            kind = "multimodal"
        else:
            kind = "unique_min"
        out[obj][kind] += 1
    return {o: {"n": sum(c.values()),
                "multimodal_frac": c["multimodal"] / sum(c.values()),
                "flat_valley_frac": c["flat_valley"] / sum(c.values())}
            for o, c in out.items()}


@pytest.mark.parametrize("leg", ["paired_fixed5_v4_nowarm_now", "paired_fixed5_v4_warm"])
def test_random_only_multimodality_is_recomputable_from_the_restart_projection(leg):
    """★ 22차 리뷰 발견 5 항목 4 — 발견 3 의 근거를 투영에서 **직접** 재계산한다.

    행 투영은 restart 개수만 담아서, "random-only 다봉성이 두 arm 에서 같다"
    (21차 발견 3 의 정정 근거)를 리뷰어가 투영에서 확인할 수 없었다. summary
    를 믿는 수밖에 없었고, 그건 자기신고다.

    restart 수준 투영이 생겼으므로 `(i, source, J, p)` 에서 분류를 다시 만들어
    봉인 summary 와 대조한다. 이게 맞으면 발견 3 의 근거가 **원자료 없이도**
    독립 검산 가능해진다.
    """
    got = _recompute_random_only_kinds(leg)
    sealed = _warm_summary(leg)["multistart_random_only"]
    bad = []
    for obj in ("pocv_dvdq", "pocv_dvdq_dqdv"):
        s, g = sealed[obj], got.get(obj)
        assert g, f"{leg}/{obj}: 재계산 결과가 비었다"
        if g["n"] != s["n"]:
            bad.append(f"{obj}: n {g['n']} vs 봉인 {s['n']}")
        for k in ("multimodal_frac", "flat_valley_frac"):
            if abs(g[k] - s[k]) > 1e-12:
                bad.append(f"{obj}.{k}: 재계산 {g[k]!r} vs 봉인 {s[k]!r}")
    assert not bad, (
        f"{leg}: restart 투영에서 재계산한 random-only 분류가 봉인과 다르다:\n  "
        + "\n  ".join(bad))


def test_projections_share_one_compute_provenance_within_each_cohort():
    """★ 22차 자체 발견 — 비교 집합이 두 생성기 판으로 갈려 있었다.

    비교 집합의 다리들이 서로 다른 분석기로 만들어지면, 다리 간 digest 비교
    (`test_cross_digest_exact_pair_reproduces_row_for_row` 등)가 "같은 규격으로
    만든 것을 비교한다" 는 전제를 잃는다.

    ★ 25차 발견 1 — 초판은 **여덟 전부**가 한 세대이길 요구했다. 그러면
      analyzer 를 고치는 순간, 원자료가 남은 다리만 재생성해도 이 회귀가
      깨지고 재생성을 안 해도 다른 회귀가 깨진다. 어느 쪽으로도 만족할 수
      없었다. 이제 **cohort 안에서** 하나이길 요구한다 — 교차-다리 비교가
      성립하는 단위가 정확히 그것이다.
    """
    import collections
    import yaml

    bad = []
    for c in _cohorts():
        seen: dict[str, dict[str, list[str]]] = collections.defaultdict(
            lambda: collections.defaultdict(list))
        for _n, m in _cohort_manifests(c):
            a = m.get("analyzer") or {}
            seen["compute_sha256"][a.get("compute_sha256")].append(m["leg_id"])
            seen["analysis_spec_sha256"][m.get("analysis_spec_sha256")].append(m["leg_id"])
            seen["src_scoring_py_sha256"][a.get("src_scoring_py_sha256")].append(m["leg_id"])
        for field, groups in seen.items():
            if None in groups:
                bad.append(f"{c['cohort_id']}/{field}: 기록 없는 다리 {groups[None]}")
            if len(groups) > 1:
                detail = " / ".join(f"{k}: {v[:3]}" for k, v in groups.items())
                bad.append(f"{c['cohort_id']}/{field} 가 갈렸다 — {detail}")
    assert not bad, (
        "cohort 안에서 분석기 provenance 가 하나가 아니다:\n  " + "\n  ".join(bad))


def test_legacy_and_registry_claim_systems_agree():
    """★ 23차 자체 발견 — 이 저장소에는 철회 체계가 **둘** 있었다.

    (구) `RETRACTED` dict + 절별 `⛔ 철회[ID]` 마커 — 17~18차, `05_HANDOFF.md`·
         `GATE14_CYCLE_SUMMARY.md` 담당
    (신) `CLAIM_STATUS.yaml` + `<!-- QUARANTINE:ID -->` 울타리 — 21차 이후

    둘 다 동작하지만 **서로를 몰랐다.** 22차까지 원장 관할이 파일 5개
    하드코딩이라 옛 문서가 아예 밖에 있었고, 그래서 이 갈라짐이 안 보였다.
    관할을 발견 기반(`_claim_scope`)으로 바꾸자마자 8건이 드러났다.

    한쪽에서 claim 이 사라져도 다른 쪽은 조용하다 — 그것이 이 저장소가
    반복해 온 실패 형태다. 양쪽 집합이 정확히 같은지 검사한다.

    ⚠ 단일 체계로의 이전은 하지 않았다. 옛 문서는 절 단위 마커를 쓰고 새
      체계는 울타리를 쓰는데, 그 변환은 문서 구조를 바꾸는 별도 작업이다.
      여기서는 **두 체계가 같은 claim 집합을 본다**는 것만 고정한다.
    """
    reg = {c["id"]: c for c in _claim_status()["claims"]}
    legacy_in_registry = {k for k, c in reg.items()
                          if c["record"] == "legacy_section_marker"}
    legacy_in_code = set(RETRACTED)

    only_code = legacy_in_code - legacy_in_registry
    only_reg = legacy_in_registry - legacy_in_code
    assert not only_code, (
        f"`RETRACTED` 에만 있고 원장에 없다: {sorted(only_code)} — "
        f"원장→파일 검사가 이 ID 를 못 본다")
    assert not only_reg, (
        f"원장에만 있고 `RETRACTED` 에 없다: {sorted(only_reg)} — "
        f"금지어 패턴이 사라졌는데 원장은 여전히 철회됐다고 말한다")

    # legacy claim 의 files 는 (구) 체계가 실제로 보는 문서여야 한다
    for cid in sorted(legacy_in_registry):
        files = {Path(f).name for f in reg[cid]["files"]}
        assert files <= set(ACTIVE_DOCS) | set(GENERATED_DOCS), (
            f"{cid}: files 가 (구) 체계의 검사 대상 밖이다 — {reg[cid]['files']}")


def test_stage3_contract_primary_table_matches_the_no_warm_projection():
    """★ 23차 P0-6 — 계약 §7.1 의 primary 표가 primary 와 **같은 arm** 인가.

    v2 는 primary 를 no-warm 이라고 정해 놓고 근거 표로 warm arm 을 실었다.
    두 표는 실제로 크게 다르다 — no-warm 순증 실패 381, warm 19. 어느 쪽을
    싣느냐가 "34p 가 얼마나 나쁜가" 를 20배 바꾼다.

    문서를 고치는 것만으로는 재발한다 (같은 실수를 v1·v2 가 반복했다).
    **투영에서 직접 계산해** 문서와 대조한다.
    """
    import csv
    import gzip

    leg = "paired_fixed5_v4_nowarm_now"
    f = _WARM / f"{leg}.projection.csv.gz"
    assert f.is_file(), f"{leg} 투영이 없다"
    with gzip.open(f, "rt", encoding="utf-8") as fh:
        rows = {(r["cond_id"], r["objective"]): r
                for r in csv.DictReader(fh, delimiter="\t")}

    cell = {}
    for (cid, obj), a in rows.items():
        if obj != "pocv_dvdq" or a["recoverable"] != "1":
            continue
        b = rows[(cid, "pocv_dvdq_dqdv")]
        k = ("fail" if a["degenerate"] == "1" else "pass",
             "fail" if b["degenerate"] == "1" else "pass")
        cell[k] = cell.get(k, 0) + 1

    n = sum(cell.values())
    net = cell[("pass", "fail")] - cell[("fail", "pass")]
    doc = _CONTRACT.read_text(encoding="utf-8")

    want = [str(cell[("pass", "pass")]), str(cell[("pass", "fail")]),
            str(cell[("fail", "pass")]), str(cell[("fail", "fail")])]
    missing = [v for v in want if v not in doc]
    assert not missing, (
        f"계약 §7.1 이 no-warm 전이표 값을 싣지 않았다: {missing}\n"
        f"  실측 pp/pf/fp/ff = {want} (n={n})")
    assert f"{net} / {n}" in doc or f"({cell[('pass','fail')]} − " in doc, (
        "primary scalar 의 분자를 문서가 밝히지 않는다")
    assert f"{net/n:.4f}" in doc, (
        f"primary scalar Δ = {net/n:.4f} 가 문서에 없다")


def test_projection_analyzer_digests_recompute_from_the_current_tree():
    """★ 23차 발견 5 — 회귀가 YAML 끼리만 비교하면 "다 같이 낡은" 것을 못 잡는다.

    스크립트를 고치고 재생성을 안 하면 여러 YAML 이 **사이좋게 낡은 채로**
    통과한다. 현재 트리에서 직접 재계산해 대조한다.

    ★ 25차 발견 1 — 초판은 여덟 전부를 현행 트리에 대고 검사했고, 원자료를
      잃은 7다리에는 영구히 충족 불가능한 요구였다. 이제 **cohort status** 로
      가른다:

        active cohort  → 현행 트리와 같아야 한다 (낡음 감시가 여기서 산다)
        frozen cohort  → 그 cohort 의 pin 과 같아야 한다 (재생성 불가)

    활성 cohort 가 반드시 하나 있어야 한다는 것은
    `test_exactly_one_cohort_is_active_and_it_tracks_the_current_tree` 가 본다.
    """
    import yaml

    cur = _current_analyzer()
    stale = []
    for c in _cohorts():
        want = cur if c.get("status") == "active" else c["pin"]
        기준 = "현행 트리" if c.get("status") == "active" else f"{c['cohort_id']} pin"
        for _n, m in _cohort_manifests(c):
            a = m.get("analyzer") or {}
            if a.get("compute_sha256") != want["compute_sha256"]:
                stale.append(f"{c['cohort_id']}/{m['leg_id']}: compute "
                             f"{a.get('compute_sha256')} ≠ {기준} "
                             f"{want['compute_sha256']}")
            if m.get("analysis_spec_sha256") != want["analysis_spec_sha256"]:
                stale.append(f"{c['cohort_id']}/{m['leg_id']}: analysis_spec ≠ {기준}")
            if a.get("src_scoring_py_sha256") != want["src_scoring_py_sha256"]:
                stale.append(f"{c['cohort_id']}/{m['leg_id']}: src_scoring ≠ {기준}")
    assert not stale, (
        "투영이 기준 코드로 만든 것이 아니다 — 활성 cohort 는 재생성하고, "
        "frozen cohort 는 손대지 말 것:\n  " + "\n  ".join(stale[:8]))


def test_projection_schema_is_declared_consistently():
    """★ 23차 발견 5 — 산출물은 `projection_schema: 2` 인데 spec 은 `1` 이었다.

    `analysis_spec_sha256` 이 앵커가 되려면 spec 이 **산출물이 무엇인지**
    알아야 한다. 둘이 어긋나면 "규격이 같다" 는 비교가 의미를 잃는다.

    ★ 25차 발견 1 — 산출물 쪽은 현행 spec 이 아니라 **자기 cohort 의 pin**
      과 맞아야 한다. frozen cohort 는 현행 spec 을 따라올 수 없다.
    """
    import yaml

    rp = _row_projection_module()
    s = rp.ANALYSIS_SPEC
    for key in ("row_projection", "restart_projection", "summary_comparison",
                "fits_binding"):
        assert key in s, f"spec 에 {key} 가 없다"
    assert s["restart_projection"]["sort_key"] == ["cond_id", "objective", "i"]
    assert s["summary_comparison"]["type_policy"] == "exact"

    for c in _cohorts():
        if c.get("status") == "active":
            assert c["pin"]["schema_version"] == s["schema_version"], (
                f"{c['cohort_id']}: 활성 cohort pin schema "
                f"{c['pin']['schema_version']} ≠ 현행 spec {s['schema_version']}")
        for _n, m in _cohort_manifests(c):
            assert m.get("projection_schema") == c["pin"]["schema_version"], (
                f"{c['cohort_id']}/{m['leg_id']}: 산출물 schema "
                f"{m.get('projection_schema')} ≠ cohort pin "
                f"{c['pin']['schema_version']}")
            for k in ("summary_sha256", "manifest_sha256"):
                assert m.get(k), f"{m['leg_id']}: {k} 가 없다 (발견 5)"


_PRESERVE = DOCS / "22p_gap" / "LEG_PRESERVATION.yaml"


def test_preservation_registry_covers_every_warm_probe_leg():
    """★ 2026-08-24 — 원자료 보존 상태가 문서 주장과 어긋나면 안 된다.

    기계 교체로 warm 실험 7다리의 원자료를 잃었다. 그 전까지 문서는 8다리를
    전부 "원자료 보유 기계에서 재생성 가능" 으로 적고 있었다 — **틀린 상태가
    문서에 있었다.** 24차 요청문도 그렇게 썼다.

    보존 상태를 기계가 읽는 정본(`LEG_PRESERVATION.yaml`)으로 두고, 투영이
    있는 모든 다리가 거기 등록됐는지 검사한다. 새 다리를 돌리면 이 테스트가
    먼저 깨져서 보존 상태를 적게 만든다.
    """
    import yaml

    assert _PRESERVE.is_file(), "LEG_PRESERVATION.yaml 이 없다"
    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    assert reg.get("schema_version") == 3

    recorded = {l["leg_id"]: l for l in reg["legs"]}
    # ★ 26차 P1-9 — 초판은 frozen g1 디렉터리 하나와 정확히 같기를 요구했다.
    #   새 cohort 에만 있는 다리는 영원히 `extra` 가 된다. cohort 전체를 본다.
    have = {n[: -len(".projection.yaml")]
            for c in _cohorts() for n in _snapshot(c).names()}

    missing = sorted(have - set(recorded))
    assert not missing, (
        f"투영은 있는데 보존 상태가 기록되지 않은 다리: {missing}\n"
        f"  `docs/22p_gap/LEG_PRESERVATION.yaml` 에 3축을 적어라")
    extra = sorted(set(recorded) - have)
    assert not extra, f"보존 원장에만 있고 투영이 없는 다리: {extra}"

    # ★ 24차 보충 발견 1 — enum 을 여기 옮겨 적지 않는다. 계약이 정본이다.
    enums = _contract_status_enums()
    bad = []
    for leg, e in sorted(recorded.items()):
        for axis, ok in enums.items():
            if e.get(axis) not in ok:
                bad.append(f"{leg}: {axis}={e.get(axis)!r} ∉ {sorted(ok)}")
        if not e.get("근거"):
            bad.append(f"{leg}: 근거가 없다")
        # ★ 원자료가 없으면 검증됐다고 주장할 수 없다 (23차 P0-6)
        if (e.get("preservation_status") in {"recorded_projection", "missing"}
                and e.get("validation_status") != "unvalidated"):
            bad.append(f"{leg}: 원자료가 없는데 validation_status="
                       f"{e['validation_status']} — 검증 근거가 없다")
    assert not bad, "보존 원장이 규칙과 어긋난다:\n  " + "\n  ".join(bad)


def test_docs_do_not_claim_lost_legs_are_regenerable():
    """★ 손실된 다리를 "되살릴 수 있다" 로 적는 문구가 되살아나지 않는가.

    이 저장소의 반복 실패 형태다 — 상태가 바뀌었는데 문서가 옛 상태를 계속
    말한다 (21차 발견 8 의 철회 잔여, 20차 13-2 의 stale 커밋 수). 보존 쪽에서
    같은 일이 나지 않게 **원장을 정본으로** 묶는다.

    ★ 24차 보충 발견 5 — 초판은 이름과 하는 일이 달랐다. §32 존재와 leg_id
    등장만 봤을 뿐 **금지 문구를 검색하지 않았다.** 문서가 옛 상태를 말하는
    것을 잡겠다고 만든 테스트가 정작 그 문장을 안 본 것이다. 여기서 본다.
    """
    import yaml

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    lost = sorted(l["leg_id"] for l in reg["legs"]
                  if l["preservation_status"] in {"recorded_projection", "missing"})
    assert lost, "원자료 없는 다리가 없다 — 이 테스트의 전제가 바뀌었다면 갱신하라"

    doc = (DOCS / "08_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    assert "§32" in doc or "## 32." in doc, "§32(손실 기록)이 문서에 없다"
    for leg in lost:
        assert leg in doc, f"{leg} 의 손실이 §32 에 기록되지 않았다"

    # ── 여기부터가 이름이 약속한 것 ──────────────────────────────────────
    #    원자료가 없는 다리를 "되살릴 수 있다" 로 읽히게 만드는 문구
    FORBIDDEN = [
        r"원자료\s*보유\s*기계",
        r"재생성\s*가능",
        r"재실행\s*시\s*바이트\s*동일",
        r"원자료가\s*로컬에만\s*있다",
    ]
    hits = []
    for rel in _CLAIM_SCOPE:                       # 발견 기반 — 새 문서도 자동 포함
        raw = (_REPO_ROOT / rel).read_text(encoding="utf-8")
        active, _ = _active_text(raw)              # QUARANTINE 울타리 밖만
        lines = active.splitlines()
        fenced = _strip_fences(lines)
        for i, line in enumerate(lines, 1):
            if fenced[i - 1]:
                continue
            for pat in FORBIDDEN:
                if re.search(pat, line):
                    hits.append(f"{rel}:{i}: {line.strip()[:90]}")
    assert not hits, (
        "원자료 없는 다리를 되살릴 수 있는 것처럼 읽히는 문구가 살아 있다:\n  "
        + "\n  ".join(hits))


# ─────────────────────────────────────────────────────────────────────────────
# 24차 **보충** 리뷰 (2026-08-24, NO-GO) — 보존 원장 schema 가 계약 밖으로 샜다
# ─────────────────────────────────────────────────────────────────────────────

def _contract_status_enums() -> dict[str, set[str]]:
    """계약 §8 의 3축 enum 을 **계약에서 읽는다** — 회귀가 옮겨 적지 않는다."""
    txt = _CONTRACT.read_text(encoding="utf-8")
    out: dict[str, set[str]] = {}
    for axis in ("preservation_status", "validation_status", "inference_role"):
        m = re.search(rf"(?m)^{axis}:\s*(.+)$", txt)
        assert m, f"계약 §8 에 `{axis}` 축 정의가 없다 — enum 의 정본이 사라졌다"
        out[axis] = {v.strip() for v in m.group(1).split("|") if v.strip()}
    return out


def test_status_axis_enums_have_exactly_one_authority():
    """★ 24차 보충 발견 1 — 구조적 literal 을 회귀가 독립 복제하면 안 된다.

    직전 라운드 Q5 가 "구조적 literal 의 독립 복제" 를 경고했는데, **같은
    커밋에서** 바로 재발했다: `canonical_candidate` 는 계약 §8 에 없는
    `inference_role` 인데 원장과 이 회귀 파일이 임의로 추가했다. 계약을 고친
    것이 아니라 **회귀가 계약 밖 상태를 두 번째 authority 로 만든** 것이다.

    이 테스트는 계약에서 enum 을 읽고, 회귀 파일 안에 계약 어휘장에서 온
    것처럼 보이는 상태 literal 이 계약 밖에 있지 않은지 본다.
    """
    allowed = set().union(*_contract_status_enums().values())
    src = Path(__file__).read_text(encoding="utf-8")
    # 상태 **값**의 어휘장만 본다 — `bundle_uri` 같은 필드명은 값이 아니다.
    def looks_like_status(tok: str) -> bool:
        return (tok.endswith("_bundle") or "validated" in tok
                or "canonical" in tok or tok.startswith("recorded_"))

    # ★ 코드 이름은 상태 값이 아니다. `canonical_bytes` · `score_canonical` 은
    #   실재하는 함수라 어휘장에 걸린다 — 저장소에 정의가 있으면 제외한다.
    code_names: set[str] = set()
    for py in sorted((_REPO / "tools").glob("*.py")) + \
            sorted((_REPO / "docs" / "22p_gap").glob("*.py")):
        code_names |= set(re.findall(r"(?m)^(?:def |class )([A-Za-z_]\w*)",
                                     py.read_text(encoding="utf-8")))
        code_names |= set(re.findall(r"(?m)^([A-Za-z_]\w*)\s*(?::[^=]+)?=",
                                     py.read_text(encoding="utf-8")))

    stray = sorted({
        tok for tok in re.findall(r'"([a-z][a-z0-9]*(?:_[a-z0-9]+)+)"', src)
        if tok not in allowed and tok not in code_names and looks_like_status(tok)
    })
    assert not stray, (
        "계약 §8 밖의 상태 토큰이 회귀 파일에 literal 로 박혀 있다: "
        f"{stray}\n  계약을 고치거나 토큰을 버려라 — 회귀는 authority 가 아니다")


def test_preservation_registry_validates_against_the_contract_enums():
    """★ 24차 보충 발견 2 — 원장의 3축 값은 계약 enum 안에 있어야 한다."""
    import yaml

    enums = _contract_status_enums()
    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    bad = []
    for e in reg["legs"]:
        for axis, ok in enums.items():
            if e.get(axis) not in ok:
                bad.append(f"{e['leg_id']}: {axis}={e.get(axis)!r} ∉ {sorted(ok)}")
    assert not bad, "원장이 계약 enum 을 벗어났다:\n  " + "\n  ".join(bad)


def test_legs_with_projection_but_no_raw_are_recorded_projection():
    """★ 24차 보충 발견 3 — 투영이 커밋돼 있으면 `missing` 이 아니다.

    계약 §8 이 `recorded_projection` 을 "summary/manifest/투영만 남아 원자료
    독립 재계산 불가" 로 정의했다. 7다리가 정확히 그 상태인데 원장은
    `missing` 이라고 적었다 — 계약이 이미 가진 칸을 안 쓰고 더 센 말을 골랐다.
    """
    import yaml

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    bad = []
    for e in reg["legs"]:
        has_proj = any(_snapshot(c).has(f"{e['leg_id']}.projection.yaml")
                       for c in _cohorts())
        if has_proj and e.get("preservation_status") == "missing":
            bad.append(f"{e['leg_id']}: 투영이 커밋돼 있는데 preservation_status=missing")
    assert not bad, (
        "계약 §8 의 `recorded_projection` 을 써야 한다:\n  " + "\n  ".join(bad))


def test_every_leg_binds_its_evidence_to_verifiable_anchors():
    """★ 24차 보충 발견 4 / 25차 발견 4 — `근거` 산문만으로는 보존 주장을 검증할 수 없다.

    `full_bundle` 이면 묶음 URI · payload index SHA · 바이트 수 · 검증 영수증 ·
    검증기 identity 가 있어야 한다. `recorded_projection` 이면 투영 세대
    (`projection_generation`) 와 재생성 가능성(`regeneration_capability`) 이
    있어야 한다 — 원자료가 없는 다리는 **기록된 분석기 바이트**에 대고
    검증하는 것 말고 할 수 있는 게 없기 때문이다.
    """
    import yaml

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    bad = []
    for e in reg["legs"]:
        leg, ps = e["leg_id"], e.get("preservation_status")
        ev = e.get("evidence") or {}
        if ps == "full_bundle":
            for k in ("bundle_uri", "payload_index_sha256", "payload_bytes",
                      "bundle_files", "fits_sha256", "member_rehash_by",
                      "verification_receipt", "verification_receipt_core_sha256",
                      "validator_identity", "empty_root_restore"):
                if not ev.get(k):
                    bad.append(f"{leg}: evidence.{k} 없음")
        elif ps == "recorded_projection":
            for k in ("leg_source_digest", "regeneration_capability"):
                if not ev.get(k):
                    bad.append(f"{leg}: evidence.{k} 없음")
        if not ev.get("cohorts"):
            bad.append(f"{leg}: evidence.cohorts 없음 — 어느 투영 세대인지 불명")
        if not e.get("claim_roles"):
            bad.append(f"{leg}: claim_roles 없음 — 어느 주장에 쓰이는지 불명")
    assert not bad, "보존 증거가 anchor 에 묶이지 않았다:\n  " + "\n  ".join(bad)


def _current_analyzer() -> dict:
    import importlib.util
    src = _REPO / "docs" / "22p_gap" / "row_projection.py"
    spec = importlib.util.spec_from_file_location("_rp_pin", src)
    rp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rp)
    return {
        "schema_version": rp.ANALYSIS_SPEC["schema_version"],
        "compute_sha256": rp._compute_sha256(),
        "row_projection_py_sha256": hashlib.sha256(src.read_bytes()).hexdigest()[:16],
        "src_scoring_py_sha256": hashlib.sha256(
            (_REPO / "src" / "scoring.py").read_bytes()).hexdigest()[:16],
        "analysis_spec_sha256": rp._spec_sha256(),
    }


def _allowed_combos() -> set[tuple[str, str, str]]:
    """계약 §8 의 **제약**에서 허용 조합을 생성한다 (v4 묶음 7 / 25차 발견 5).

    열거표였던 초판은 정상 상태를 빠뜨렸다 — 현행 코드로 보존·검증에 성공했지만
    설계가 교란된 arm(`full_bundle / current_validated / confounded`)을 사실대로
    적을 수 없었다. 세 축이 직교한다고 계약에 적어 놓고 표는 직교하지 않았다.

    이제 계약은 함의만 적고 조합은 여기서 만든다. 축 곱 전체에서 함의를 어기는
    것만 뺀다.
    """
    import itertools
    import yaml

    txt = _CONTRACT.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^allowed_status_constraints:\n(.*?)^```", txt)
    assert m, "계약 §8 에 `allowed_status_constraints` 가 없다"
    rules = yaml.safe_load("allowed_status_constraints:\n" + m.group(1))\
        ["allowed_status_constraints"]
    assert rules, "제약이 비었다"

    enums = _contract_status_enums()
    axes = ("preservation_status", "validation_status", "inference_role")
    out = set()
    for combo in itertools.product(*(sorted(enums[a]) for a in axes)):
        cand = dict(zip(axes, combo))
        ok = True
        for r in rules:
            if all(cand[k] in v for k, v in r["if"].items()) and \
                    not all(cand[k] in v for k, v in r["then"].items()):
                ok = False
                break
        if ok:
            out.add(combo)
    assert out, "생성된 허용 집합이 비었다"
    return out


def test_registry_rejects_impossible_status_tuples():
    """★ 24차 보충 발견 5-1 — 축별 membership 은 불가능한 튜플을 막지 못한다.

    리뷰가 준 반례 넷이 전부 통과했다:
      · 실물 bundle 없이 `full_bundle / current_validated / canonical`
      · `recorded_projection / current_validated / canonical`
      · `missing / unvalidated / canonical`
      · 같은 `leg_id` 를 두 번 등록 (dict comprehension 이 덮는다)

    허용 조합은 계약 §8 의 표 하나가 정본이다.
    """
    import yaml

    allowed = _allowed_combos()
    raw = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))["legs"]

    ids = [e["leg_id"] for e in raw]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    assert not dup, f"leg_id 가 중복 등록됐다: {dup} — 뒤엣것이 앞엣것을 덮는다"

    bad = []
    for e in raw:
        t = (e.get("preservation_status"), e.get("validation_status"),
             e.get("inference_role"))
        if t not in allowed:
            bad.append(f"{e['leg_id']}: {t} 는 계약 §8 허용 조합표에 없다")
    assert not bad, "불가능한 상태 튜플:\n  " + "\n  ".join(bad)


def test_full_bundle_claims_are_backed_by_a_real_bundle():
    """★ 24차 보충 발견 5-1 — `full_bundle` 을 **실물**에 대고 확인한다.

    원장이 "완전 묶음이 있다" 고 적는 것만으로는 아무 것도 증명하지 않는다.
    선언한 URI 가 실재하고, 파일 수·바이트 수·payload index 해시·검증
    영수증이 **지금 디스크에서 다시 계산해** 맞아야 한다.
    """
    import yaml

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    bad = []
    for e in reg["legs"]:
        if e.get("preservation_status") != "full_bundle":
            continue
        ev = e.get("evidence") or {}
        root = _REPO / ev["bundle_uri"]
        if not root.is_dir():
            bad.append(f"{e['leg_id']}: 묶음 경로가 없다 {ev['bundle_uri']}")
            continue
        files = sorted(p for p in root.rglob("*") if p.is_file())
        if len(files) != ev.get("bundle_files"):
            bad.append(f"{e['leg_id']}: 파일 수 {len(files)} ≠ 선언 {ev.get('bundle_files')}")
        nbytes = sum(p.stat().st_size for p in files)
        if nbytes != ev.get("payload_bytes"):
            bad.append(f"{e['leg_id']}: 바이트 {nbytes} ≠ 선언 {ev.get('payload_bytes')}")
        idx = _REPO / ev["payload_index"]
        got = hashlib.sha256(idx.read_bytes()).hexdigest()
        if got != ev.get("payload_index_sha256"):
            bad.append(f"{e['leg_id']}: payload index sha {got[:16]} ≠ 선언")
        # ★ 25차 발견 4 — 성공 **문자열** 두 개가 아니라 구조를 파싱하고,
        #   영수증이 이 묶음·이 검증기·이 산출과 결속돼 있는지 본다.
        rec = _REPO / ev["verification_receipt"]
        if not rec.is_file():
            bad.append(f"{e['leg_id']}: 검증 영수증 파일이 없다 {ev['verification_receipt']}")
        else:
            r = yaml.safe_load(rec.read_text(encoding="utf-8"))
            core = r.get("core") or {}
            declared = hashlib.sha256(
                yaml.safe_dump(core, allow_unicode=True, sort_keys=False,
                               width=100).encode("utf-8")).hexdigest()
            if declared != r.get("core_sha256"):
                bad.append(f"{e['leg_id']}: 영수증 자신의 core_sha256 이 core 와 안 맞는다")
            if r.get("core_sha256") != ev.get("verification_receipt_core_sha256"):
                bad.append(f"{e['leg_id']}: 영수증 core sha 가 원장 선언과 다르다")
            if core.get("leg_id") != e["leg_id"]:
                bad.append(f"{e['leg_id']}: 영수증이 다른 다리 것이다 "
                           f"({core.get('leg_id')})")
            b_ = core.get("bundle") or {}
            for k, want in (("uri", ev["bundle_uri"]),
                            ("payload_index_sha256", ev["payload_index_sha256"]),
                            ("fits_sha256", ev["fits_sha256"]),
                            ("bytes", ev["payload_bytes"]),
                            ("files", ev["bundle_files"])):
                if b_.get(k) != want:
                    bad.append(f"{e['leg_id']}: 영수증 bundle.{k} 가 원장과 다르다")
            if b_.get("member_mismatches") != 0:
                bad.append(f"{e['leg_id']}: 영수증이 member 불일치를 기록했다")
            if (core.get("restore") or {}).get("mode") != "empty_root":
                bad.append(f"{e['leg_id']}: empty-root 복원 기록이 없다")
            v_ = core.get("validation") or {}
            if not (v_.get("ok") is True and v_.get("fail") == []):
                bad.append(f"{e['leg_id']}: 영수증이 통과를 말하지 않는다")
            if v_.get("n_checks") != (ev.get("validator_identity") or {}).get("n_checks"):
                bad.append(f"{e['leg_id']}: 영수증 검사 수가 원장과 다르다")
            i_ = core.get("identity") or {}
            if i_.get("validator_source_digest") != \
                    (ev.get("validator_identity") or {}).get("source_digest"):
                bad.append(f"{e['leg_id']}: 영수증 validator digest 가 원장과 다르다")
            # ★ 영수증이 **현행 검증기**로 만든 것인가.
            #   이 검사가 없으면 RUN_SCOPE 를 고쳐도 영수증이 조용히 낡는다 —
            #   실제로 이번 라운드에 `tools/` 를 늘리자마자 그렇게 됐고,
            #   원장·영수증끼리만 비교하던 회귀는 통과했다.
            import sys as _sys
            if str(_REPO) not in _sys.path:
                _sys.path.insert(0, str(_REPO))
            from src.io import source_digest as _sd
            if i_.get("validator_source_digest") != _sd():
                bad.append(
                    f"{e['leg_id']}: 영수증이 낡았다 — "
                    f"{i_.get('validator_source_digest')} ≠ 현행 {_sd()}. "
                    f"`python3 docs/22p_gap/make_receipt.py {e['leg_id']}` 로 "
                    "다시 만들고 원장의 core sha 를 갱신하라")
            roles = {o.get("role") for o in (core.get("outputs") or [])}
            if "rescored_summary" not in roles:
                bad.append(f"{e['leg_id']}: 복원본 재채점 산출이 영수증에 없다")
            for o in core.get("outputs") or []:
                if not o.get("semantic_sha256") or not o.get("canonicalizer"):
                    bad.append(f"{e['leg_id']}: 산출 {o.get('role')} 에 semantic digest 없음")
    assert not bad, "`full_bundle` 주장이 실물과 어긋난다:\n  " + "\n  ".join(bad)


def test_preservation_registry_holds_executed_legs_only():
    """★ 25차 발견 5 — 계획 다리를 이 원장에 넣으면 상태가 왜곡된다.

    초판 규칙은 "사전 등록은 `preservation_status: missing` 으로만" 이었다.
    그런데 계약 §8 은 `missing` 에 `excluded` 만 허용한다 — 아직 돌리지도 않은
    다리가 **과학적으로 폐기됨**으로 기록된다. 그리고 `missing` 하나가
    "원자료를 잃었다" 와 "아직 안 돌렸다" 를 동시에 뜻하게 된다.

    계획 lifecycle 은 별도 `planned_leg_index` 이고 그것이 **묶음 9** 다.
    그때까지 이 원장은 **이미 실행된 다리만** 담는다.

    솔직하게 적어 두는 한계: coverage 기준이 커밋된 투영이므로, 새 다리를
    돌려도 투영을 만들기 전에는 이 회귀가 깨지지 않는다. 실행 **전에**
    강제하려면 planned leg index 와 실행 영수증이 있어야 한다 (묶음 9).
    """
    import yaml

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    recorded = {e["leg_id"] for e in reg["legs"]}
    in_cohorts = {leg for c in _cohorts() for leg in c["legs"]}

    assert recorded == in_cohorts, (
        f"원장 다리와 cohort 구성원이 다르다 — "
        f"원장에만 {sorted(recorded - in_cohorts)} · "
        f"cohort 에만 {sorted(in_cohorts - recorded)}")

    planned = [e["leg_id"] for e in reg["legs"]
               if e.get("preservation_status") == "missing"]
    assert not planned, (
        f"`missing` 다리가 있다: {planned}\n"
        "  아직 실행하지 않은 다리라면 `planned_leg_index`(묶음 9) 로 옮겨라. "
        "투영조차 없는 실행 다리라면 계약 §8 의 뜻을 다시 확인하라")

    txt = _CONTRACT.read_text(encoding="utf-8")
    assert "planned leg index" in txt and "묶음 9" in txt, (
        "계약이 '계획 다리는 여기 오지 않는다 / 실행 전 강제는 묶음 9' 를 적지 않았다")


def test_full_bundle_payload_members_are_rehashed_one_by_one():
    """★ 25차 발견 3 — 파일 수·총 바이트·index 파일 SHA 는 손상을 놓친다.

    `fits.parquet` 한 바이트를 **크기를 유지한 채** 뒤집으면 파일 수도, 총
    바이트도, `payload_sha256.yaml` 자신의 SHA 도, 영수증도 전부 그대로다.
    앞 테스트는 통과한다. 실물 검사라고 부를 수 없었다.

    필요한 구현은 이미 `tools/archive_bundle.py::check()` 에 있다 (F71 —
    payload 재해시). 옮겨 적지 않고 **그 함수를 호출한다**. 산문 문자열
    `bundle_check: "… → 0 mismatch"` 는 증거가 아니다.
    """
    import sys
    import yaml

    if str(_REPO) not in sys.path:
        sys.path.insert(0, str(_REPO))
    from tools.archive_bundle import check as _bundle_check

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    bad = []
    for e in reg["legs"]:
        if e.get("preservation_status") != "full_bundle":
            continue
        ev = e.get("evidence") or {}
        res = _bundle_check(_REPO / ev["bundle_uri"])
        miss = res.get("missing") or []
        if miss:
            bad.append(f"{e['leg_id']}: archive_bundle.check 불일치 {len(miss)}건 "
                       f"— {miss[:4]}")
        # 원장이 적은 fits SHA 도 실물에서 다시 계산한다
        fp = _REPO / ev["bundle_uri"] / "fits.parquet"
        if fp.is_file():
            got = hashlib.sha256(fp.read_bytes()).hexdigest()
            if got != ev.get("fits_sha256"):
                bad.append(f"{e['leg_id']}: fits sha {got[:16]} ≠ 원장 "
                           f"{str(ev.get('fits_sha256'))[:16]}")
    assert not bad, "묶음 member 재해시 실패:\n  " + "\n  ".join(bad)


def _load_projection_module(src_text: str, name: str):
    """주어진 소스로 `row_projection` 을 임시 파일에 만들어 import 한다."""
    import importlib.util
    import tempfile

    d = Path(tempfile.mkdtemp())
    f = d / "row_projection.py"
    f.write_text(src_text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(name, f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_compute_digest_moves_when_a_constant_the_compute_path_reads_moves():
    """★ 25차 발견 2 — 계산 digest 가 계산 의미를 빠뜨렸다.

    `_RESTART_SOURCES` 는 `_restart_list()` 의 허용·거부 동작을 바꾼다. 허용
    목록에 값을 하나 더하면 analyzer 의 의미가 달라지는데, `_compute_sha256()`
    는 손으로 고른 함수 body 와 상수 셋만 해시했으므로 digest 는 그대로였다.
    breaker 가 파일 전체 SHA 를 일부러 제외하므로 `comparison_set_status` 도
    `intact` 로 남는다 — 의미가 바뀌었는데 아무 것도 안 깨진다.

    digest 는 손으로 고른 목록이 아니라 **계산 경로가 실제로 읽는 것의
    닫힘(dependency closure)** 에서 나와야 한다.
    """
    src = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(encoding="utf-8")
    base = _load_projection_module(src, "_rp_base")

    a = '_RESTART_SOURCES = frozenset({"base_init", "warm", "random"})'
    b = '_RESTART_SOURCES = frozenset({"base_init", "warm", "random", "grid"})'
    assert src.count(a) == 1, "상수 정의를 못 찾았다 — 테스트를 갱신하라"
    moved = _load_projection_module(src.replace(a, b), "_rp_moved")

    assert base._compute_sha256() != moved._compute_sha256(), (
        "`_RESTART_SOURCES` 를 넓혔는데 compute digest 가 그대로다 — "
        "계산 경로가 읽는 상수가 digest 밖에 있다")


def test_compute_digest_ignores_display_only_changes():
    """반대 방향 — 표시 코드가 바뀌었다고 digest 가 흔들리면 안 된다.

    22차 자체 발견이 `compute_sha256` 을 만든 이유가 이것이다. 닫힘을 넓히면서
    이 성질을 잃으면 주석 한 줄에 교차비교 집합이 깨진다.
    """
    src = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(encoding="utf-8")
    base = _load_projection_module(src, "_rp_base2")

    marker = "def main("
    assert src.count(marker) >= 1
    i = src.index(marker)
    noisy = src[:i] + "# ★ 표시 전용 주석 — 계산과 무관\n" + src[i:]
    mod = _load_projection_module(noisy, "_rp_display")

    assert base._compute_sha256() == mod._compute_sha256(), (
        "표시 코드만 고쳤는데 compute digest 가 움직였다")


# ─────────────────────────────────────────────────────────────────────────────
# 25차 발견 1 — 투영은 **cohort** 에 속한다. 전역 pin 은 충족 불가능했다.
# ─────────────────────────────────────────────────────────────────────────────

_PIN_KEYS = ("schema_version", "compute_sha256", "row_projection_py_sha256",
             "src_scoring_py_sha256", "analysis_spec_sha256")


def _cohorts() -> list[dict]:
    import yaml
    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    cs = reg.get("cohorts")
    assert cs, ("`LEG_PRESERVATION.yaml` 에 `cohorts` 가 없다 — 투영을 전역 "
                "하나로 묶으면 analyzer 를 바꾸는 순간 충족 불가능해진다")
    return cs


def _cohort_names(c: dict, base=None) -> list[str]:
    """cohort 가 담은 투영 YAML 이름 — **active 는 CURRENT 가 정본**이다.

    ★ 34차 #9 — 33차판 reader 들은 `<cohort>/*.projection.yaml` 을 glob 했다.
      writer 는 CURRENT 로 옮겼는데 실제 소비자는 fixed name 을 읽고 있었다.
      그러면 pointer 전환 뒤 `_materialize` 중 죽었을 때 reader 가 stale G0
      또는 G0/G1 혼합을 **읽는다** — 다음 suite 의 `check_materialized()` 가
      나중에 잡는 것은 "reader authority 가 CURRENT" 라는 뜻이 아니다.

    frozen cohort 는 원자료를 잃어 migration 할 수 없으므로 fixed layout
    fallback 을 유지한다 (조용한 예외가 아니라 여기 적힌 예외다).
    """
    return _snapshot(c, base=base).names()


class _Snapshot:
    """한 cohort 의 **한 generation** 을 고정한 handle (37차 #9).

    ★ 36차판은 `_cohort_names()` 가 `CURRENT` 를 한 번 읽고, manifest 마다
      `_cohort_yaml()` 이 `CURRENT` 를 **또** 읽었다. 그 사이에 게시가 끼면
      한 assertion 안에서 G0 와 G1 이 섞인다. reader operation 이 시작할 때
      한 번 읽어 generation ID 와 file map 을 고정하고, 이후 모든 조회가
      **그 generation** 만 본다.

    ★ 그리고 **경로를 밖으로 내보내지 않는다.** cohort dir 을 넘기면 소비자가
      고정 이름을 직접 열 수 있고, 36차에 실제로 그랬다. 여기서 나가는 것은
      이름과 이미 읽힌 바이트뿐이다.
    """

    def __init__(self, c: dict, base=None):
        self.cohort_id = c.get("cohort_id")
        self.frozen = c.get("status") == "frozen"
        d = Path(base) if base is not None else _REPO / c["dir"]
        self._dir = d
        if self.frozen:
            # 원자료를 잃어 migration 할 수 없다 — fixed layout fallback 을
            # 유지하되, 목록도 **한 번만** 읽어 고정한다.
            self.generation_id = None
            self._files = {q.name: None for q in sorted(d.iterdir())
                           if q.is_file()}
        else:
            # ★ 37차 #9 — 기대 명부는 **원장**에서 온다. 고정 파일 목록에서
            #   유도하면 자기 자신을 근거로 삼는 꼴이라 leg 통째 누락을 못 본다.
            #   명부를 **선언한** cohort 에만 적용한다 — 선언이 없으면 빈
            #   집합이 아니라 "검사 안 함"(None) 이다.
            rec = _rp().read_current(
                d, expect_legs=set(c["legs"]) if c.get("legs") else None)
            self.generation_id = rec["generation_id"]
            self._files = dict(rec["files"])
            self._gdir = d / "gen" / rec["generation_id"]

    def names(self) -> list:
        return sorted(n for n in self._files if n.endswith(".projection.yaml"))

    def has(self, name: str) -> bool:
        return name in self._files

    def blob(self, name: str) -> bytes:
        """이 generation 의 바이트. 고정 사본이 흔들려도 영향받지 않는다."""
        if name not in self._files:
            raise AssertionError(
                f"{self.cohort_id}: snapshot 이 {name} 을 담고 있지 않다")
        if self.frozen:
            return (self._dir / name).read_bytes()
        data = (self._gdir / name).read_bytes()
        got = hashlib.sha256(data).hexdigest()
        if got != self._files[name]:
            raise AssertionError(
                f"{self.cohort_id}/{name}: 바이트가 snapshot 과 다르다")
        return data

    def yaml(self, name: str) -> dict:
        import yaml as _y

        return _y.safe_load(self.blob(name).decode("utf-8"))

    def manifests(self):
        for n in self.names():
            yield n, self.yaml(n)


def _snapshot(c: dict, base=None) -> _Snapshot:
    return _Snapshot(c, base=base)


def _cohort_yaml(c: dict, name: str, base=None) -> dict:
    """cohort 에서 투영 YAML 하나를 읽는다 — active 는 CURRENT 를 통해서."""
    return _snapshot(c, base=base).yaml(name)


def _cohort_manifests(c: dict):
    """cohort 의 투영 manifest 를 **(이름, dict)** 로 준다.

    ★ 37차 #9 — 한 snapshot 에서 전부 나온다. 36차판은 이름과 내용을 서로
      다른 `CURRENT` 읽기로 얻어 mixed generation 이 가능했다.
    """
    yield from _snapshot(c).manifests()


def test_every_projection_matches_its_own_cohort_pin():
    """★ 25차 발견 1 — 전역 pin 하나로는 analyzer 변경을 넘길 수 없었다.

    옛 모델에서는 분석기를 고치면 두 선택 모두 실패했다:

        살아 있는 다리를 옛 투영 그대로 둔다  → current-tree equality 실패
        살아 있는 다리만 새 analyzer 로 재생성 → 전역 pin·단일 세대 equality 실패

    `comparison_set_status` 를 바꿔도 저 세 회귀는 해제되지 않으므로 suite 를
    만족시킬 방법이 없었다. **cohort** 로 나눈다: 옛 여덟 투영은 immutable
    historical cohort 로 얼리고, 새 투영은 새 cohort_id 와 새 경로에 쓴다.
    """
    bad = []
    for c in _cohorts():
        pin = c["pin"]
        files = list(_cohort_manifests(c))
        assert files, f"{c['cohort_id']}: 투영이 하나도 없다"
        for _n, m in files:
            a = m.get("analyzer") or {}
            got = {"schema_version": m.get("projection_schema"),
                   "compute_sha256": a.get("compute_sha256"),
                   "row_projection_py_sha256": a.get("row_projection_py_sha256"),
                   "src_scoring_py_sha256": a.get("src_scoring_py_sha256"),
                   "analysis_spec_sha256": m.get("analysis_spec_sha256")}
            for k in _PIN_KEYS:
                if got[k] != pin.get(k):
                    bad.append(f"{c['cohort_id']}/{m['leg_id']}: {k}={got[k]!r} "
                               f"≠ pin {pin.get(k)!r}")
    assert not bad, "cohort pin 과 투영이 어긋난다:\n  " + "\n  ".join(bad)


def test_exactly_one_cohort_is_active_and_it_tracks_the_current_tree():
    """활성 cohort 하나만 현행 트리와 같아야 한다 — 낡음 감시는 거기서 산다.

    frozen cohort 는 현행 트리와 **달라도 된다**. 그것이 발견 1 의 요점이다.
    다만 활성 cohort 가 하나도 없으면 낡음 감시가 통째로 잠들므로 막는다.
    """
    cur = _current_analyzer()
    active = [c for c in _cohorts() if c.get("status") == "active"]
    assert len(active) == 1, (
        f"활성 cohort 가 {len(active)}개다 — 정확히 하나여야 한다. "
        "0이면 현행 트리를 아무도 안 본다")
    c = active[0]
    drift = [k for k in _PIN_KEYS if c["pin"].get(k) != cur.get(k)]
    assert not drift, (
        f"활성 cohort `{c['cohort_id']}` 가 현행 트리에서 벗어났다: {drift}\n"
        f"  `python3 docs/22p_gap/row_projection.py <leg> --cohort {c['cohort_id']}` 로 "
        "재생성하거나, 새 cohort 를 만들어라")

    for c in _cohorts():
        if c.get("status") == "frozen":
            assert c.get("frozen_reason"), f"{c['cohort_id']}: frozen 사유가 없다"


def test_raw_lost_legs_live_only_in_frozen_cohorts():
    """원자료가 없는 다리는 활성 cohort 에 들어갈 수 없다.

    들어가면 그 순간 "현행 트리로 재생성하라" 가 되고, 그것은 영구히 충족
    불가능한 요구다 — 25차 발견 1 이 지적한 바로 그 모순이다.
    """
    import yaml

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    cap = {e["leg_id"]: (e.get("evidence") or {}).get("regeneration_capability")
           for e in reg["legs"]}
    bad = []
    for c in _cohorts():
        if c.get("status") != "active":
            continue
        for leg in c["legs"]:
            if cap.get(leg) != "available_raw_present":
                bad.append(f"{c['cohort_id']}: {leg} 은 "
                           f"{cap.get(leg)!r} 인데 활성 cohort 에 있다")
    assert not bad, "충족 불가능한 요구가 생긴다:\n  " + "\n  ".join(bad)


def test_cohort_membership_is_consistent_in_both_directions():
    """cohort 가 선언한 다리와 디렉터리의 투영이 정확히 같아야 한다."""
    import yaml

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    known = {e["leg_id"] for e in reg["legs"]}
    bad = []
    for c in _cohorts():
        declared = set(c["legs"])
        on_disk = {n[: -len(".projection.yaml")]
                   for n, _m in _cohort_manifests(c)}
        if declared != on_disk:
            bad.append(f"{c['cohort_id']}: 선언 {sorted(declared - on_disk)} 누락 · "
                       f"디스크 {sorted(on_disk - declared)} 미선언")
        stray = sorted(declared - known)
        if stray:
            bad.append(f"{c['cohort_id']}: legs 원장에 없는 다리 {stray}")
    assert not bad, "cohort 구성원이 어긋난다:\n  " + "\n  ".join(bad)


def _leg_preservation() -> dict:
    import yaml

    return yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))


def _pick_sealed_digest(projections: dict[str, dict], active: str | None):
    """cohort 여럿이 같은 다리를 담을 때 어느 값이 근거인가.

    ★ 30차 P2 — 초판은 `_cohorts()` 를 돌며 **처음 찾은** 것을 돌려줬다.
      cohort 목록의 순서가 답을 바꿨고, 두 cohort 가 서로 다른 값을 적어도
      아무 일이 없었다. 규칙을 못 박는다:

        · 값이 갈리면 **실패**한다 (조용히 하나를 고르지 않는다)
        · 값이 같으면 active cohort 의 것을 돌려준다 — 어느 쪽을 돌려주든
          같은 값이지만, 근거의 출처가 순서에 의존하지 않게 한다
    """
    if not projections:
        return None
    vals = {c: p.get("source_digest") for c, p in projections.items()}
    if len(set(vals.values())) != 1:
        raise AssertionError(f"cohort 마다 source_digest 가 다르다: {vals}")
    if active in projections:
        return projections[active].get("source_digest")
    return next(iter(vals.values()))


def _sealed_source_digest(leg_id: str) -> str | None:
    """봉인된 투영이 적은 `source_digest` — 가변 원장이 아니라 이것이 근거다."""
    import yaml

    active = next((c["cohort_id"] for c in _cohorts()
                   if c.get("status") == "active"), None)
    return _pick_sealed_digest(_sealed_projections(leg_id), active)


def _current_generation(creg: dict) -> str:
    """**현행** protocol 세대 — 자유신고가 아니라 산출물에서 도출한다.

    ★ 30차 — 다리의 leg-level `inference_role` 이 무엇에 대한 판정인지가
    이 함수의 존재 이유다. `paired_fixed5_v4` 의 leg-level 이 `diagnostic`
    인 근거는 원장이 직접 적었듯 "**현행 정본은 아니다** — run_spec 의
    `source_digest` 가 현행과 다르다" 이다. 즉 leg-level 은 **현행 세대에
    대한** 역할이지 모든 세대에 대한 상한이 아니다. 옛 세대 주장
    (`LEGACY_PAIRED_FIXED5`) 의 정본이 되는 것은 그 판정과 모순되지 않는다.

    도출 규칙: `protocol_generations` 의 선언 순서에서, **실제 source digest
    가 도달한** 가장 새로운 세대. `v6` 는 아직 산출물이 없으므로 현행이 될
    수 없다. `source_digest_generations` 의 모든 digest 는 아래
    `_claim_role_problems` 가 **봉인된 다리에 묶여 있는지** 검사하므로,
    "현행 = v6" 을 위조하려면 v6 digest 로 실제 투영을 봉인해야 한다.
    """
    order = list(creg.get("protocol_generations") or [])
    attained = set((creg.get("source_digest_generations") or {}).values())
    live = [g for g in order if g in attained]
    assert live, "어떤 세대에도 산출물이 없다 — 현행 세대를 도출할 수 없다"
    return live[-1]


def _claim_role_problems(reg: dict, creg: dict, roles_ok: set[str],
                         sealed: dict[str, str | None]) -> list[str]:
    """`claim_roles` 계약 위반 목록. 순수 함수 — 변이 시험이 디스크를 안 탄다.

    ★ 30차 — 초판은 이 본문이 테스트 안에 인라인이라 **변이를 걸 수가
    없었다.** 규칙을 고쳐도 "고친 규칙이 실제로 무는가" 를 보일 방법이
    없었다는 뜻이다. 순수 함수로 꺼내 원장 사본을 변형해 물리는지 본다.
    """
    gens = creg.get("protocol_generations") or []
    assert gens, "protocol_generations 가 없다 — 세대가 자유문자가 된다"
    compat = {(r["source"], r["target"]): set(r["allowed_roles"])
              for r in (creg.get("role_compatibility") or [])}
    digest_gen = creg.get("source_digest_generations") or {}
    assert digest_gen, "`source_digest_generations` 가 없다 — 세대를 도출할 수 없다"
    assert compat, "`role_compatibility` 가 없다 — 세대 간 role 이 자유문장이 된다"
    known = {c["id"]: c for c in (creg.get("active_claims") or [])}
    retracted = {c["id"] for c in creg["claims"]}
    current = _current_generation(creg)

    seen: set[tuple[str, str]] = set()
    used: set[str] = set()
    bad: list[str] = []

    # ★ 30차 — 세대표가 **봉인되지 않은 digest** 를 담으면 `_current_generation`
    #   이 위조된다. 원장에 `deadbeef: v6` 한 줄을 더하는 것만으로 현행 세대가
    #   v6 이 되고, v6_prep 다리의 leg-level 상한이 통째로 풀린다. 표의 모든
    #   digest 는 **봉인된 투영이 실제로 적은** 다리 digest 여야 한다.
    anchored = {d for d in sealed.values() if d}
    for dg in sorted(digest_gen):
        if dg not in anchored:
            bad.append(f"`source_digest_generations` 의 {dg!r} 가 어떤 봉인된 "
                       "투영에도 없다 — 세대표를 봉인물에 묶어라")

    for e in reg["legs"]:
        leg = e["leg_id"]
        cap = (e.get("evidence") or {}).get("regeneration_capability")
        for r in e.get("claim_roles") or []:
            cid = r.get("claim_id")
            if cid in retracted:
                bad.append(f"{leg}: 철회된 주장 {cid} 에 role 을 붙였다")
                continue
            if cid not in known:
                bad.append(f"{leg}: {cid!r} 가 CLAIM_STATUS.active_claims 에 없다")
                continue
            used.add(cid)
            key = (cid, leg)
            if key in seen:
                bad.append(f"{leg}: {cid} role 이 두 번 선언됐다")
            seen.add(key)
            if r.get("inference_role") not in roles_ok:
                bad.append(f"{leg}/{cid}: inference_role={r.get('inference_role')!r} "
                           f"∉ 계약 enum")
            # ★ 26차 P2-11 — 초판은 둘 중 **하나만** 있으면 통과시켰고,
            #   role 의 세대를 claim 의 세대와 대조하지 않았다. `v6_prep` 을
            #   `v999` 로 바꿔도 통과했다.
            # ★ 27차 P2-10 — `reason` 하나로 legacy canonical 승격이 됐다.
            #   (role 세대, claim 세대) 쌍의 **허용표**로 본다. 표에 없는 쌍은
            #   fail-closed 다.
            # ★ 28차 P2 — role 행의 자기신고를 믿지 않는다. 다리의 봉인된
            #   `leg_source_digest` 에서 세대를 **도출**한다. 자기신고와 role 을
            #   함께 바꾸는 두 필드 loophole 을 막는다.
            if "protocol_generation" in r:
                bad.append(f"{leg}/{cid}: role 행에 protocol_generation 을 "
                           "적지 않는다 — 봉인된 digest 에서 도출한다")
            src_digest = (e.get("evidence") or {}).get("leg_source_digest")
            # ★ 29차 P2 — `evidence` 는 **가변 YAML** 이다. 봉인된 투영의
            #   `source_digest` 와 대조하지 않으면 evidence 와 role 을 함께
            #   바꾸는 변형이 그대로 통과한다.
            if sealed.get(leg) is not None and sealed[leg] != src_digest:
                bad.append(f"{leg}: evidence.leg_source_digest={src_digest!r} 가 "
                           f"봉인된 투영의 source_digest={sealed[leg]!r} 와 다르다")
            rg = digest_gen.get(src_digest)
            tg = known[cid]["protocol_generation"]
            if rg is None:
                bad.append(f"{leg}: source digest {src_digest!r} 의 세대가 "
                           "`source_digest_generations` 에 없다")
            elif (rg, tg) not in compat:
                bad.append(f"{leg}/{cid}: ({rg} → {tg}) 조합이 "
                           "`role_compatibility` 에 없다 — 규칙을 먼저 적어라")
            elif r.get("inference_role") not in compat[(rg, tg)]:
                bad.append(
                    f"{leg}/{cid}: ({rg} → {tg}) 에서 "
                    f"`{r.get('inference_role')}` 은 허용되지 않는다 "
                    f"(허용: {sorted(compat[(rg, tg)])})")
            elif rg != tg and not r.get("reason"):
                bad.append(f"{leg}/{cid}: 세대를 넘어 쓰는데 `reason` 이 없다")
            # ★ leg-level 보다 **센** role 의 성립 조건
            if r.get("inference_role") == "canonical":
                if cap != "available_raw_present":
                    bad.append(f"{leg}/{cid}: 원자료가 없는데 canonical")
                # ★ 29차 — 초판은 여기서 `r.get("protocol_generation")` 을 다시
                #   비교했다. 위에서 그 필드를 **금지**했으므로 dead condition
                #   이었다.
                # ★ 30차 — dead condition 을 `rg == tg` 로 되살렸더니 이번엔
                #   **너무 넓었다**: v5 다리가 v5 legacy 주장의 정본이 되는
                #   것까지 막았다 (24차 보충이 명시적으로 허용한 것 —
                #   "legacy claim scope 와 당시 protocol 을 명시한 채 유지할 수
                #   있다"). leg-level 은 **현행 세대에 대한** 판정이므로
                #   비교 대상은 `current` 다. 옛 세대는 위의 `role_compatibility`
                #   가 이미 관장한다.
                if e.get("inference_role") != "canonical" and tg == current:
                    bad.append(f"{leg}/{cid}: leg 는 {e.get('inference_role')} 인데 "
                               f"현행 세대({current}) 주장에 canonical 을 붙였다")

    # 양방향 — `requires_leg: true` 인 주장은 적어도 한 다리가 지지해야 한다
    orphan = sorted(cid for cid, c in known.items()
                    if c.get("requires_leg") and cid not in used)
    if orphan:
        bad.append(f"지지 다리가 없는 활성 주장: {orphan}")
    return bad


def test_claim_roles_are_a_machine_contract_not_free_prose():
    """★ 25차 발견 6 — `claim_roles` 가 자유문장이면 기계 계약이 아니다.

    초판은 `claim: "…한국어 문장…"` · `role: 인용가능` 이었고 회귀는 목록이
    비었는지만 봤다. 다음이 전부 빠져 있었다:

      · claim ID 가 원장(`CLAIM_STATUS.yaml`)에 실재하는가
      · role 이 계약 enum 인가 · protocol generation 이 있는가
      · `claim_id × leg_id` 중복
      · leg-level `inference_role` 과의 양립
      · claim 원장 양방향 coverage

    한 다리가 옛 protocol 주장에는 쓸 수 있고 새 protocol 주장에는 못 쓰는
    구분은 **필요하다** (25차 발견 3). 다만 그것을 자유문장으로 적으면 묶음 7
    을 닫은 것이 아니다.
    """
    enums = _contract_status_enums()
    reg = _leg_preservation()
    creg = _claim_status()
    sealed = {e["leg_id"]: _sealed_source_digest(e["leg_id"]) for e in reg["legs"]}
    bad = _claim_role_problems(reg, creg, enums["inference_role"], sealed)
    assert not bad, "claim_roles 가 기계 계약이 아니다:\n  " + "\n  ".join(bad)


def _live_contract() -> tuple[dict, dict, set[str], dict[str, str | None]]:
    """실제 원장의 **깊은 사본** — 변이 시험이 디스크를 건드리지 않게."""
    import copy

    reg = _leg_preservation()
    creg = _claim_status()
    sealed = {e["leg_id"]: _sealed_source_digest(e["leg_id"]) for e in reg["legs"]}
    return (copy.deepcopy(reg), copy.deepcopy(creg),
            _contract_status_enums()["inference_role"], sealed)


def test_the_current_generation_is_derived_from_artifacts_not_declared():
    """★ 30차 — `v6` 는 선언돼 있지만 **산출물이 없다**. 현행이 될 수 없다.

    이것을 자유필드(`current_generation: v6`)로 적었다면 그 한 줄을 고치는
    것만으로 v6_prep 다리들의 leg-level 상한이 풀렸을 것이다.
    """
    _, creg, _, _ = _live_contract()
    assert _current_generation(creg) == "v6_prep"

    # 산출물이 생기면 — 그리고 **그때만** — 현행이 옮겨간다
    creg["source_digest_generations"]["ffffffffffffffff"] = "v6"
    assert _current_generation(creg) == "v6"


def test_the_generation_table_must_be_anchored_to_sealed_projections():
    """★ 30차 — 세대표가 봉인물에 묶이지 않으면 `현행 세대`가 위조된다.

    변이: 어떤 다리도 쓰지 않는 digest 한 줄(`ffff…: v6`)을 표에 더한다.
    이것만으로 `_current_generation` 이 v6 이 되고, v6_prep 다리들이
    leg-level 상한 없이 canonical 을 붙일 수 있게 된다. 표의 모든 digest 가
    **봉인된 투영이 실제로 적은** 값이어야 한다는 검사가 이 경로를 막는다.
    """
    reg, creg, roles_ok, sealed = _live_contract()
    assert _claim_role_problems(reg, creg, roles_ok, sealed) == []

    creg["source_digest_generations"]["ffffffffffffffff"] = "v6"
    bad = _claim_role_problems(reg, creg, roles_ok, sealed)
    assert any("어떤 봉인된" in b and "ffffffffffffffff" in b for b in bad), bad


def test_a_leg_may_be_canonical_for_a_legacy_claim_but_not_the_current_one():
    """★ 30차 — 29차의 `rg == tg` 는 **너무 넓었다**.

    `paired_fixed5_v4` 의 leg-level 은 `diagnostic` 이다. 그 근거는 원장이
    적은 "현행 정본은 아니다" 이고, 그것은 **현행 세대에 대한** 판정이다.
    24차 보충 리뷰가 명시적으로 허용한 것 — 옛 `RESULTS_PAIRED_FIXED5.md`
    가 지지하던 v5 주장의 citation-grade 지위는 "legacy claim scope 와 당시
    protocol 을 명시한 채" 유지할 수 있다 — 을 `rg == tg` 가 막았다.

    이 시험은 **양쪽**을 고정한다. 옛 세대 정본은 통과하고, 같은 role 을
    현행 세대 주장으로 옮기면 물린다. 한쪽만 고정하면 규칙을 통째로 지워도
    시험이 초록이다.
    """
    reg, creg, roles_ok, sealed = _live_contract()
    leg = next(e for e in reg["legs"] if e["leg_id"] == "paired_fixed5_v4")
    role = next(r for r in leg["claim_roles"]
                if r["claim_id"] == "LEGACY_PAIRED_FIXED5")
    assert leg["inference_role"] == "diagnostic"
    assert role["inference_role"] == "canonical"
    assert _claim_role_problems(reg, creg, roles_ok, sealed) == []

    # 같은 다리·같은 role 을 **현행 세대** 주장으로 옮기면 물린다
    creg_now = copy_with_claim_generation(creg, "LEGACY_PAIRED_FIXED5", "v6_prep")
    bad = _claim_role_problems(reg, creg_now, roles_ok, sealed)
    assert any("현행 세대(v6_prep)" in b for b in bad), bad


def copy_with_claim_generation(creg: dict, claim_id: str, gen: str) -> dict:
    import copy

    out = copy.deepcopy(creg)
    for c in out["active_claims"]:
        if c["id"] == claim_id:
            c["protocol_generation"] = gen
    return out


def test_a_current_generation_leg_cannot_self_promote_to_canonical():
    """★ 30차 — 규칙이 **현행 세대 안에서** 실제로 무는지.

    변이: `paired_fixed5_v4_nowarm_now` (leg-level `diagnostic`, 원자료
    소실) 가 현행 세대 주장 `P22_NOWARM_PRIMARY` 에 canonical 을 붙인다.
    원자료 조항이 먼저 물어서 leg-level 조항이 **한 번도 실행되지 않는**
    가짜 초록을 피하려고, 원자료 조항을 만족시킨 채로도 물리는지 따로 본다.
    """
    reg, creg, roles_ok, sealed = _live_contract()
    leg = next(e for e in reg["legs"]
               if e["leg_id"] == "paired_fixed5_v4_nowarm_now")
    role = next(r for r in leg["claim_roles"]
                if r["claim_id"] == "P22_NOWARM_PRIMARY")
    role["inference_role"] = "canonical"

    bad = _claim_role_problems(reg, creg, roles_ok, sealed)
    assert any("원자료가 없는데 canonical" in b for b in bad), bad

    # 원자료 조항을 만족시켜도 leg-level 조항이 남는다
    leg["evidence"]["regeneration_capability"] = "available_raw_present"
    bad = _claim_role_problems(reg, creg, roles_ok, sealed)
    assert not any("원자료가 없는데" in b for b in bad), bad
    assert any("현행 세대(v6_prep)" in b and "nowarm_now" in b for b in bad), bad


def test_the_two_audit_tools_share_one_canonical_score_path():
    """★ 자체 발견 — 감사 도구 둘이 채점 경로를 각자 적고 있었다.

    `row_projection.py` 와 `make_receipt.py` 가 둘 다
    `add_error_columns → classify_recoverability → clean_bias →
    apply_bias_correction → summarize` 를 인라인으로 적었다. 한쪽만 고치면
    **두 감사 도구가 서로 다른 것을 검증**하게 되고, 그것을 알아차릴 방법이
    없다 — 24차 보충 Q5 가 경고한 구조적 복제의 실물이다.

    (초판에 "여기서 갈리면 두 감사 도구가 다른 것을 검증하게 된다" 는 주석까지
    달아 놓고 복제를 남겼다. 주석은 강제가 아니다.)
    """
    rp = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(encoding="utf-8")
    mr = (_REPO / "docs" / "22p_gap" / "make_receipt.py").read_text(encoding="utf-8")

    assert "def score_canonical(" in rp, (
        "`row_projection.py` 에 정본 채점 경로 함수가 없다")
    assert "score_canonical" in mr, (
        "`make_receipt.py` 가 정본 채점 경로를 쓰지 않는다")

    # 파이프라인 단계를 **각자** 부르는 곳이 둘 이상이면 복제다
    steps = ("add_error_columns", "classify_recoverability", "clean_bias",
             "apply_bias_correction")
    for step in steps:
        assert f"{step}(" not in mr, (
            f"`make_receipt.py` 가 `{step}` 를 직접 부른다 — "
            "`score_canonical` 하나만 부르게 하라")
        assert rp.count(f"{step}(") <= 2, (
            f"`row_projection.py` 안에서도 `{step}` 가 여러 번 불린다")


def test_semantic_digests_use_one_canonicalization():
    """★ 자체 발견 — 같은 `score-semantic/v1` 이 두 바이트 스트림을 뜻했다.

    `make_receipt._semantic` 은 기본 구분자(`", "` `": "`)로, `preserve.
    canonical_bytes` 는 고정 구분자(`","` `":"`)로 직렬화했다. 둘 다 산출
    manifest 에 `canonicalizer: score-semantic/v1` 이라고 적었다 — **한 버전
    라벨이 두 규격을 가리켰다.** 나중에 두 digest 를 대조하면 영원히 다르다.
    """
    mr = (_REPO / "docs" / "22p_gap" / "make_receipt.py").read_text(encoding="utf-8")
    assert "canonical_bytes" in mr, (
        "`make_receipt.py` 가 `tools.preserve.canonical_bytes` 를 쓰지 않는다")
    assert "json.dumps(" not in mr, (
        "`make_receipt.py` 가 직렬화를 따로 적는다 — 정규화는 한 곳이어야 한다")


def test_receipt_validation_actually_reads_the_restored_root():
    """★ 26차 P1-5 — 초판 영수증의 "빈 root" 도 원본 checkout 을 읽었다.

    `make_receipt.py` 는 `os.chdir(root)` 만 하고 `validate_provenance` 에
    `repo_root` 를 넘기지 않았다. 검증기는 cwd 가 아니라 **`src/io.py` 가 있는
    저장소**를 root 로 잡으므로 (`src/io.py:1328`), 봉인 입력을 원본
    checkout 에서 풀었다. 이 컨테이너에는 `results/grid_curves_v4` 가 남아
    있어서 통과했을 뿐이다 — 리뷰어의 clean checkout 에서는
    `producer_곡선일치`·`입력_digest_재해시` 로 실패했다.

    여기서 직접 확인한다: 복원 root 에서 봉인 입력 하나를 지우면
    `repo_root=root` 검증이 **실패해야** 한다. 실패하지 않으면 검증기가
    원본을 보고 있다는 뜻이다.
    """
    import sys
    import tempfile

    if str(_REPO) not in sys.path:
        sys.path.insert(0, str(_REPO))
    from src.io import validate_provenance
    from tools.archive_bundle import restore

    root = Path(tempfile.mkdtemp(prefix="receipt_root_"))
    try:
        res = restore(_REPO / "artifacts" / "paired_fixed5_v4", repo_root=root)
        assert res["ok"] and not res["conflict"], res.get("conflict")
        run_dir = Path(res["run_dir"])

        good = validate_provenance(run_dir, repo_root=root)
        assert good["ok"], f"복원본이 통과해야 한다: {good['fail']}"

        # 복원 root **안에서만** 봉인 입력을 지운다. 원본은 그대로다.
        curves = root / "results" / "grid_curves_v4" / "curves.parquet"
        assert curves.is_file(), "전제: 봉인 곡선이 복원 root 에 있다"
        curves.unlink()

        bad = validate_provenance(run_dir, repo_root=root)
        assert not bad["ok"], (
            "복원 root 에서 봉인 입력을 지웠는데 통과했다 — 검증기가 원본 "
            "checkout 을 보고 있다 (26차 P1-5 의 false-green)")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)


def test_make_receipt_binds_the_validator_to_the_restored_root():
    """구조적으로도 막는다 — `repo_root` 를 넘기고 `os.chdir` 에 기대지 않는다."""
    mr = (_REPO / "docs" / "22p_gap" / "make_receipt.py").read_text(encoding="utf-8")
    assert "repo_root=" in mr, (
        "`make_receipt.py` 가 `validate_provenance` 에 `repo_root` 를 넘기지 않는다")
    # 주석에서 "왜 안 쓰는가" 를 설명하는 것은 괜찮다 — **호출**이 없어야 한다.
    code = "\n".join(ln for ln in mr.splitlines()
                     if not ln.lstrip().startswith("#"))
    assert "os.chdir(" not in code, (
        "cwd 를 옮기는 것으로는 검증 root 가 바뀌지 않는다 (26차 P1-5)")


def test_receipt_compares_the_rescored_summary_against_the_sealed_one():
    """★ 26차 P1-6 — 영수증이 semantic 불일치를 **성공으로 기록**했다.

    `_score_manifest()` 는 재채점 결과와 봉인 summary 를 각각 append 할 뿐
    비교하지 않았다. 주석은 "자리별로 대조" 한다고 했지만 assertion 이 없었고,
    실제로 같은 `degeneracy-summary/v5` · `score-semantic/v1` 라벨 아래 두
    digest 가 달랐다.

    같은 semantic object 라면 정규 view 를 정의해 equality 를 강제해야 한다.
    """
    import yaml

    rec = yaml.safe_load(
        (DOCS / "22p_gap" / "receipts" / "paired_fixed5_v4.validate.yaml")
        .read_text(encoding="utf-8"))
    outs = {o["role"]: o for o in rec["core"]["outputs"]}
    assert {"rescored_summary", "sealed_summary"} <= set(outs), sorted(outs)

    a, b = outs["rescored_summary"], outs["sealed_summary"]
    assert a["semantic_schema"] == b["semantic_schema"]
    assert a["canonicalizer"] == b["canonicalizer"]
    assert a["semantic_sha256"] == b["semantic_sha256"], (
        "같은 schema·canonicalizer 인데 semantic digest 가 다르다 — "
        "같은 object 가 아니면 schema/role 을 갈라라")
    assert rec["core"]["outputs_agree"] is True, (
        "영수증이 대조 결과를 명시하지 않는다")


def test_evidence_cohorts_and_the_cohort_registry_agree_both_ways():
    """★ 26차 P1-10 — `evidence.cohorts` 가 nonempty 인지만 봤다.

    다리가 "나는 g1·g2 에 있다" 고 적어도 cohort 쪽 `legs` 와 대조하지 않으면
    아무 것도 보장되지 않는다. 양방향으로 묶는다.
    """
    import yaml

    reg = yaml.safe_load(_PRESERVE.read_text(encoding="utf-8"))
    by_cohort = {c["cohort_id"]: set(c["legs"]) for c in _cohorts()}
    bad = []
    for e in reg["legs"]:
        declared = set((e.get("evidence") or {}).get("cohorts") or [])
        actual = {cid for cid, legs in by_cohort.items() if e["leg_id"] in legs}
        if declared != actual:
            bad.append(f"{e['leg_id']}: evidence.cohorts={sorted(declared)} ≠ "
                       f"cohort registry {sorted(actual)}")
        unknown = sorted(declared - set(by_cohort))
        if unknown:
            bad.append(f"{e['leg_id']}: 존재하지 않는 cohort {unknown}")
    assert not bad, "cohort 선언이 양방향으로 맞지 않는다:\n  " + "\n  ".join(bad)


def test_the_projection_builder_refuses_to_write_into_a_frozen_cohort():
    """★ 26차 P1-9 — `--out` 을 생략하면 frozen g1 을 **직접 덮었다.**

    게다가 검증을 끝내기 전에 gzip payload 부터 썼다. 잃어버린 다리의 유일한
    사본을 실수 한 번으로 덮을 수 있는 상태였다. 목적지는 cohort 로만 고르고,
    frozen 이면 코드가 거부해야 한다.
    """
    rp = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(encoding="utf-8")
    assert "_frozen_cohort_dirs" in rp, (
        "`row_projection.py` 가 frozen cohort 목록을 읽지 않는다")
    assert "--cohort" in rp, "cohort 이름으로 목적지를 고르는 인자가 없다"

    import subprocess
    r = subprocess.run(
        [sys.executable, str(_REPO / "docs" / "22p_gap" / "row_projection.py"),
         "paired_fixed5_v4", "--out", "docs/22p_gap/warm_probe"],
        capture_output=True, text=True, cwd=_REPO)
    assert r.returncode != 0, "frozen cohort 로 쓰라는 명령이 성공했다"
    assert "frozen" in (r.stdout + r.stderr), (r.stdout + r.stderr)[:400]


def test_committed_gate_requests_are_self_contained():
    """★ 26차 P2-12 — 커밋된 요청문에 template placeholder 가 남아 있었다.

    `git add -A` 로 채우기 **전** 판을 함께 커밋했고, 리뷰 대상 커밋에서
    `__TARGET__`·`__TARGET_FULL__`·`__PYTEST__` 가 그대로 보였다. 외부 첨부만
    완성돼 있었으니 "committed 문서 자기완결" 은 닫히지 않았다.

    그리고 요청문이 인용하는 영수증 core sha 가 실물과 다르면 그것도 stale 이다.

    ★ 30차 자체 발견 — 초판은 **모든** 요청문의 인용을 **오늘의** 영수증과
    대조했다. 요청문은 그 회차의 기록이므로, 다음 회차에 영수증이 바뀌면
    지나간 요청문이 전부 거짓이 된다 (실제로 그 자리에서 빨갛게 됐다).
    그렇다고 "최신 것만 본다" 로 약화하면 archive 는 아무도 안 보게 된다.

    옳은 결속은 **그 요청문이 이름한 대상 커밋의 영수증**이다. 그것이
    자기완결의 뜻이기도 하다 — 요청문 하나와 그것이 이름한 커밋만으로
    검증이 닫힌다.
    """
    import yaml

    _RECEIPT = "degradation-degeneracy/docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml"

    def core_at(commit: str) -> str | None:
        r = subprocess.run(["git", "show", f"{commit}:{_RECEIPT}"],
                           cwd=_REPO_ROOT, capture_output=True)
        if r.returncode != 0:
            return None
        return yaml.safe_load(r.stdout.decode("utf-8")).get("core_sha256")

    bad = []
    for md in sorted((DOCS / "22p_gap").glob("GATE*_REQUEST.md")):
        txt = md.read_text(encoding="utf-8")
        for ph in re.findall(r"__[A-Z_]+__", txt):
            bad.append(f"{md.name}: 채우지 않은 placeholder {ph}")
        # 40-hex 전체 SHA 를 적었다면 실재하는 커밋이어야 한다
        for sha in set(re.findall(r"(?m)^[^`]*\b([0-9a-f]{40})\b", txt)):
            r = subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                               cwd=_REPO_ROOT, capture_output=True)
            if r.returncode != 0:
                bad.append(f"{md.name}: 존재하지 않는 커밋 {sha[:12]}")
        quoted = set(re.findall(r"core[_ ]sha\S*\s*[는은]?\s*`?([0-9a-f]{16,64})", txt))
        if not quoted:
            continue
        target = re.search(r"(?m)^대상 커밋:\s*`?([0-9a-f]{40})", txt)
        if not target:
            bad.append(f"{md.name}: core sha 를 인용했는데 대상 커밋이 없다 — "
                       "무엇에 대고 대조할지 알 수 없다")
            continue
        core = core_at(target.group(1))
        if core is None:
            bad.append(f"{md.name}: 대상 커밋 {target.group(1)[:12]} 에 영수증이 없다")
            continue
        for q in quoted:
            if not core.startswith(q):
                bad.append(f"{md.name}: 인용한 영수증 core sha {q[:16]} 가 대상 커밋 "
                           f"{target.group(1)[:12]} 의 것과 다르다 ({core[:16]})")
    assert not bad, "커밋된 요청문이 자기완결적이지 않다:\n  " + "\n  ".join(bad)


def _receipt_module():
    import importlib.util
    src = _REPO / "docs" / "22p_gap" / "make_receipt.py"
    spec = importlib.util.spec_from_file_location("_mr", src)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_citation_safety_metadata_is_not_thrown_out_of_the_hash():
    """★ 27차 P1-6 — 안전 문구를 정규 view 에서 빼면 뒤집어도 digest 가 같다.

    v2 의 `SEMANTIC_SKIP` 은 `_F4_주의` 까지 뗐다. 그런데 그것은 실행 메타가
    아니라 `summarize()` 가 결정론적으로 만드는 **인용 금지 경고**다
    (`src/scoring.py:369`). 리뷰가 준 반례가 정확히 이것이다:

        `_F4_주의: "do not cite"` → `"safe to cite"` ⇒ semantic_equal=True

    지금은 양쪽이 다 만드는 값이므로 비교된다.
    """
    mr = _receipt_module()
    base = {"overall": {"n": 3}, "_F4_주의": "이 블록의 두 지표는 그대로 인용하지 말 것."}
    flipped = dict(base, _F4_주의="인용해도 안전하다")
    assert mr._semantic(base) != mr._semantic(flipped), (
        "안전 문구를 뒤집었는데 semantic digest 가 같다")


@pytest.mark.parametrize("mut", [
    {"canonical": False}, {"봉인상태": "손상"}, {"인용가능": False},
    {"fits_sha256": "0" * 64},
])
def test_citation_safety_flags_are_checked_by_value(mut):
    """`_채점원본` 은 재채점이 못 만들지만 그 안의 flag 는 검사해야 한다.

    통째로 정규 view 에서 빼면 `인용가능` 을 뒤집어도 digest 가 같다.
    equality 로 못 보는 것은 **명시적 assertion** 으로 본다.
    """
    mr = _receipt_module()
    fits_sha = "a" * 64
    good = {"_채점원본": {"fits": "results/x/fits.parquet", "canonical": True,
                       "fits_sha256": fits_sha, "봉인상태": "정상", "인용가능": True}}
    assert mr._citation_safety(good, fits_sha)["fits_sha256_bound"] is True

    bad = {"_채점원본": dict(good["_채점원본"], **mut)}
    with pytest.raises(SystemExit) as e:
        mr._citation_safety(bad, fits_sha)
    assert "인용 안전" in str(e.value)


def test_a_receipt_with_nothing_to_compare_is_not_agreement():
    """산출이 하나뿐이면 "일치" 가 아니라 **비교 불가**다 (27차 P1-6)."""
    mr = _receipt_module()
    one = [{"role": "rescored_summary", "semantic_schema": "s",
            "canonicalizer": "c", "semantic_sha256": "a" * 64}]
    with pytest.raises(SystemExit) as e:
        mr._outputs_agree(one)
    assert "대조할 짝이 없다" in str(e.value)

    two_same = one + [dict(one[0], role="sealed_summary")]
    assert mr._outputs_agree(two_same) is True
    two_diff = one + [dict(one[0], role="sealed_summary", semantic_sha256="b" * 64)]
    with pytest.raises(SystemExit):
        mr._outputs_agree(two_diff)


def test_receipt_core_paths_are_os_independent():
    """★ 27차 P1-7 — core 에 `\\` 가 섞이면 OS 마다 다른 bytes 가 된다.

    리뷰가 Windows 에서 실측했다: core 의 세 경로가 backslash 로 바뀌고
    생성 YAML 이 CRLF 가 되어 8877 → 9087 bytes, core sha 불일치.
    """
    import yaml

    rec = yaml.safe_load(
        (DOCS / "22p_gap" / "receipts" / "paired_fixed5_v4.validate.yaml")
        .read_text(encoding="utf-8"))
    core = rec["core"]
    for path in (core["bundle"]["uri"], core["bundle"]["payload_index"],
                 core["restore"]["run_dir_relative"]):
        assert "\\" not in path, f"core 경로에 backslash 가 있다: {path!r}"
        assert not path.startswith("/"), path

    mr = (_REPO / "docs" / "22p_gap" / "make_receipt.py").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in mr.splitlines() if not ln.lstrip().startswith("#"))
    assert "write_text(" not in code, (
        "`write_text` 는 기본 newline 변환을 쓴다 — LF 를 명시하라 (27차 P1-7)")
    assert "as_posix()" in code, "core 경로를 POSIX 로 고정하지 않았다"


def test_the_frozen_guard_lives_at_the_write_primitive_not_the_cli():
    """★ 27차 P1-8 — frozen 거부가 `main()` 에만 있어 public API 로 우회됐다.

    `build(leg, out=WARM)` 이 frozen cohort 를 그대로 받아 썼고, 회귀는 CLI
    subprocess 만 검사했다. 이번 라운드의 다른 발견들과 같은 형태다 —
    **가장 낮은 공통 지점**에 두지 않으면 우회된다.
    """
    rp = _row_projection_module()
    with pytest.raises(SystemExit) as e:
        rp.build("paired_fixed5_v4", rp.WARM)
    assert "frozen" in str(e.value)

    src = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(encoding="utf-8")
    assert "_assert_writable(_out)" in src, (
        "쓰기 지점에서 frozen 을 막지 않는다")


def test_promotion_happens_only_after_the_recomputation_verdict():
    """★ 27차 P1-8 — staging 이 promotion gate 가 아니었다.

    초판은 semantic verdict 가 false 여도 세 파일을 먼저 승격하고 CLI 가 나중에
    exit 1 을 냈다. 검증 실패는 **승격 자체가 없어야** 한다.

    ★ 33차 #9 — 초판은 여기서 **manifest-last** 도 함께 요구했다 (YAML 을
    마지막에 옮겨 세대 섞임을 줄이는 완화책). 승격이 cohort 전체의 immutable
    generation + 단일 pointer 로 바뀌면서 그 요구는 **필요 없어졌다** —
    파일별 순서 자체가 사라졌고 전환은 한 번이다. 완화책을 계속 요구하면
    구조가 바뀐 뒤에도 옛 모양을 강제하게 된다.
    """
    src = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(encoding="utf-8")
    i = src.index("_v = meta.get(\"재계산_검증\")")
    j = src.index("promote_cohort_generation(_stage, _out, leg)")
    assert i < j, "승격이 verdict 검사보다 먼저 온다"
    assert "shutil.rmtree(_stage" in src[i:j], (
        "verdict 가 실패해도 staging 을 버리지 않는다")
    # 파일별 승격이 남아 있으면 원자성이 깨진다
    assert "os.replace(f, _out" not in src, "옛 파일별 승격이 남아 있다"


def test_both_audit_paths_share_one_semantic_view():
    """★ 28차 P1-4 — 두 감사 경로의 semantic 계약이 또 갈렸다.

    `make_receipt` 는 `_F4_주의` 를 정규 view 에 다시 넣었는데
    `row_projection` 의 비교기는 계속 떼고 있었다. 봉인 summary 의 인용 금지
    경고를 "안전" 으로 바꿔도 `재계산_검증.전체_일치` 에 diff 가 안 생겼다.

    정본은 `row_projection.SEMANTIC_SKIP` 하나다. `make_receipt` 는 그것을
    import 한다 — 복제하지 않는다.
    """
    rp_src = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(encoding="utf-8")
    mr_src = (_REPO / "docs" / "22p_gap" / "make_receipt.py").read_text(encoding="utf-8")

    assert "SEMANTIC_SKIP = (" in rp_src, "정본이 `row_projection` 에 없다"
    assert '"_F4_주의"' not in rp_src.split("SEMANTIC_SKIP = (")[1].split(")")[0], (
        "`_F4_주의` 를 아직 떼고 있다 — `summarize()` 가 만드는 인용 금지 경고다")
    assert "SEMANTIC_SKIP = (" not in mr_src, (
        "`make_receipt` 가 semantic view 를 **따로 정의**한다 (28차 P1-4)")
    assert "_row_projection().SEMANTIC_SKIP" in mr_src

    rp = _row_projection_module()
    mr = _receipt_module()
    assert tuple(rp.SEMANTIC_SKIP) == mr._semantic_skip()
    assert "_F4_주의" not in rp.SEMANTIC_SKIP


def test_the_frozen_guard_covers_descendants_and_fails_closed(tmp_path):
    """★ 28차 P1-5 — frozen guard 가 root **exact equality** 만 거부했다.

    `frozen_dir/child` 는 frozen tree 안인데 통과했고, 원장이 없으면 frozen
    set 을 빈 dict 로 돌려 **fail-open** 했다.
    """
    rp = _row_projection_module()
    frozen = next(iter(rp._frozen_cohort_dirs().values()))

    with pytest.raises(SystemExit):
        rp._assert_writable(frozen)                    # exact
    with pytest.raises(SystemExit):
        rp._assert_writable(frozen / "child")          # descendant
    with pytest.raises(SystemExit):
        rp._assert_writable(frozen / "a" / "b")

    src = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(encoding="utf-8")
    assert "원장이 없으면" in src or "fail-closed" in src, (
        "원장 부재 시 fail-closed 라는 근거가 코드에 없다")


# ─────────────────────────────────────────────────────────────────────────────
# 30차 P2 — 세대 chain 을 **등록 실물**에 결속한다
# ─────────────────────────────────────────────────────────────────────────────

def _bundle_dir(leg_id: str):
    d = _REPO / "artifacts" / leg_id
    return d if (d / "manifest.yaml").is_file() else None


def _manifest_bound_digest(leg_id: str) -> tuple[str, str] | None:
    """봉인 manifest **바이트에서** 다시 뽑은 `(manifest_sha256, source_digest)`.

    ★ 30차 P2 — 투영의 `manifest_sha256` 이 실제 manifest bytes 와 **재해시로
    결속되지 않았다.** 투영이 적은 값을 투영이 증명하는 구조였다.
    """
    import hashlib

    import yaml

    d = _bundle_dir(leg_id)
    if d is None:
        return None
    raw = (d / "manifest.yaml").read_bytes()
    man = yaml.safe_load(raw.decode("utf-8"))
    return hashlib.sha256(raw).hexdigest(), man["run_spec"]["source_digest"]


def _sealed_projections(leg_id: str) -> dict[str, dict]:
    """cohort 이름 → 그 cohort 의 봉인 투영.

    ★ 34차 #9 — active cohort 는 **CURRENT 를 통해** 읽는다. fixed-name 사본은
      호환·표시용이며 어떤 active 판정의 authority 도 아니다.
    """
    name = f"{leg_id}.projection.yaml"
    out = {}
    for c in _cohorts():
        if name in _cohort_names(c):
            out[c["cohort_id"]] = _cohort_yaml(c, name)
    return out


def test_a_projection_manifest_digest_is_rehashed_from_actual_bytes():
    """★ 30차 P2 — 투영의 `manifest_sha256` 을 실물에서 다시 계산한다.

    원자료가 남은 다리에서만 가능하다 (`available_raw_present`). 그 다리가
    이 결속의 **유일한 앵커**이며, 나머지 일곱은 원자료가 없어 영구히 불가능
    하다 — 그 사실 자체를 여기 고정한다.
    """
    reg = _leg_preservation()
    anchored = []
    for e in reg["legs"]:
        leg = e["leg_id"]
        got = _manifest_bound_digest(leg)
        cap = (e.get("evidence") or {}).get("regeneration_capability")
        if got is None:
            assert cap == "unavailable_raw_lost", (
                f"{leg}: 원자료가 있다는데 묶음이 없다")
            continue
        assert cap == "available_raw_present", f"{leg}: 묶음이 있는데 원장이 없다고 한다"
        man_sha, src = got
        for cohort, proj in _sealed_projections(leg).items():
            assert proj["manifest_sha256"] == man_sha, (
                f"{leg}/{cohort}: 투영의 manifest_sha256 이 실물 재해시와 다르다")
            assert proj["source_digest"] == src, (
                f"{leg}/{cohort}: 투영의 source_digest 가 봉인 manifest 의 "
                f"run_spec.source_digest 와 다르다")
        assert (e["evidence"]["leg_source_digest"] == src), (
            f"{leg}: 원장의 leg_source_digest 가 봉인 manifest 와 다르다")
        anchored.append(leg)
    assert anchored == ["paired_fixed5_v4"], (
        f"실물에 묶인 다리 목록이 바뀌었다: {anchored}")


def test_a_leg_in_two_cohorts_must_report_the_same_source_digest():
    """★ 30차 P2 — `_sealed_source_digest` 가 **처음 찾은** cohort 를 썼다.

    같은 다리가 g1 과 g2 에 모두 있어도 둘의 equality 를 강제하지 않았고
    active cohort 우선순위도 없었다. cohort 순서를 바꾸면 답이 달라졌다는 뜻이다.
    """
    reg = _leg_preservation()
    multi = []
    for e in reg["legs"]:
        projs = _sealed_projections(e["leg_id"])
        if len(projs) > 1:
            multi.append(e["leg_id"])
            vals = {c: p.get("source_digest") for c, p in projs.items()}
            assert len(set(vals.values())) == 1, (
                f"{e['leg_id']}: cohort 마다 source_digest 가 다르다 {vals}")
    assert multi, "두 cohort 에 걸친 다리가 없으면 이 검사는 잠들어 있다"

    # active cohort 를 먼저 본다 — 순서에 답이 의존하면 안 된다
    assert _sealed_source_digest("paired_fixed5_v4") == \
        _sealed_projections("paired_fixed5_v4")["g2_2026_08_25"]["source_digest"]

    # 규칙을 **순수 함수로** 시험한다. 실제 원장은 두 cohort 가 같은 값을
    # 적고 있어 disagreement 를 만들 수 없고, 그러면 이 시험이 규칙을 전혀
    # 시험하지 못한다 (이름만 강한 시험이 되는 자리다).
    same = {"g1": {"source_digest": "aaaa"}, "g2": {"source_digest": "aaaa"}}
    assert _pick_sealed_digest(same, "g2") == "aaaa"
    assert _pick_sealed_digest(same, None) == "aaaa"
    assert _pick_sealed_digest({}, "g2") is None
    with pytest.raises(AssertionError):
        _pick_sealed_digest({"g1": {"source_digest": "aaaa"},
                             "g2": {"source_digest": "bbbb"}}, "g2")


def test_every_generation_entry_names_the_legs_that_attained_it():
    """★ 30차 P2 — mapping 의 **값**에 봉인 근거가 없었다.

    key 가 투영에 등장하는지만 봤으므로 `digest → generation` 의 값 쪽은
    자유였다. 값마다 그것을 얻은 다리를 이름하게 하고, 그 다리의 봉인
    투영이 실제로 그 digest 를 적었는지 본다.

    **닫히지 않은 것을 그대로 적는다**: 실행이 남긴 어떤 산출물에도
    "protocol generation" 이라는 필드는 없다. 그 이름은 이 원장의 분류다.
    그래서 digest→generation 화살표는 *도출* 이 아니라 **선언**이며, 여기서
    할 수 있는 것은 선언을 봉인물이 지지하는 digest 에 묶어 두는 것뿐이다.
    묶음 9 로 등록되는 새 다리부터는 registered receipt 의
    `planned_envelope.protocol_generation` 이 정본이 된다 (아래 검사).
    """
    creg = _claim_status()
    reg = _leg_preservation()
    ev = creg.get("source_digest_evidence") or {}
    dg = creg.get("source_digest_generations") or {}
    assert set(ev) == set(dg), (
        f"근거 표와 세대 표의 digest 집합이 다르다: {sorted(set(ev) ^ set(dg))}")

    known = {e["leg_id"] for e in reg["legs"]}
    for d, legs in sorted(ev.items()):
        assert legs, f"{d}: 근거 다리가 비었다"
        for leg in legs:
            assert leg in known, f"{d}: 원장에 없는 다리 {leg}"
            projs = _sealed_projections(leg)
            assert projs, f"{d}/{leg}: 봉인 투영이 없다"
            for cohort, p in projs.items():
                assert p.get("source_digest") == d, (
                    f"{d}/{leg}/{cohort}: 봉인 투영이 다른 digest 를 적었다 "
                    f"({p.get('source_digest')})")


#: 묶음 9 의 보존 index 가 놓일 자리. 아직 **없다** — 그것이 지금의 상태다.
_PRESERVE_INDEX = _REPO / "docs" / "22p_gap" / "preserve_index"


#: 보존 backend 를 어디서 여는가 — 배선의 **정본**. 아직 없다.
_PRESERVE_BACKEND = _REPO / "docs" / "22p_gap" / "preserve_backend.yaml"


def _open_canonical_backend():
    """배선 파일이 이름하는 backend 를 연다. 없으면 `None`.

    ★ 33차 P2 — 32차판 live gate 는 `_registered_legs(_PRESERVE_INDEX)` 로
      **backend 없이** 불렀고, helper 는 backend 가 없으면 즉시 `{}` 를
      돌려줬다. 그래서 실제 index 에 잘못 결속된 registration 이 생겨도 gate
      는 "등록 leg 0개" 를 보고 통과했다. helper 를 고쳐 놓고 production
      caller 를 그 경로에 연결하지 않은 것이다.
    """
    import yaml

    import tools.preserve as P

    if not _PRESERVE_BACKEND.is_file():
        return None
    cfg = yaml.safe_load(_PRESERVE_BACKEND.read_text(encoding="utf-8")) or {}
    root = cfg.get("root")
    if not root:
        raise AssertionError(f"{_PRESERVE_BACKEND.name} 에 root 가 없다")
    return P.CasBackend(root=(_REPO / root))


def _registered_legs(index_path, backend=None):
    """**raw journal 을 열거해** 검증된 receipt 를 돌려준다.

    ★ 31차 P2 — 30차판은 가변 원장의 optional 필드가 검사 대상을 골랐다.
    ★ 32차 P2 — 31차판은 index/journal 의 **문자열** 일치로 등록을 셌다.
    ★ 33차 P2 — 32차판은 검증 실패를 `continue` 로 숨겼다.
    ★ 34차 P2 — 33차판은 후보를 `has_registration_journal()` 로 골랐다. 그
      술어는 **raw 파일 존재 술어가 아니다** — JSON·schema·digest 가 깨지면
      `registration()` 이 `None` 을 돌려주고, `receipt_object` 가 index 와
      다르거나 index entry 가 없어도 `False` 다. 즉 "journal 은 있는데 검증
      실패" 의 **가장 앞부분**을 후보 filter 가 다시 숨겼다.

      이제 `registered/*.json` 과 `legs/*.json` 을 **직접 열거**한다. 발견은
      semantic helper 가 아니라 raw namespace 에서 시작해야 한다.

    돌려주는 것: `(verified receipts, 오류 목록)`.
    """
    from pathlib import Path as _P

    import tools.preserve as P

    index_path = _P(index_path)
    raw_j = sorted(q.stem for q in (index_path / "registered").glob("*.json")) \
        if (index_path / "registered").is_dir() else []
    raw_e = sorted(q.stem for q in (index_path / "legs").glob("*.json")) \
        if (index_path / "legs").is_dir() else []
    if not raw_j and not raw_e:
        return {}, []

    bad = []
    if raw_j and backend is None:
        return {}, [f"등록 journal 이 {len(raw_j)}개 있는데 backend 를 열 수 "
                    f"없다: {raw_j[:3]} — `{_PRESERVE_BACKEND.name}` 를 두거나 "
                    "배선을 고쳐라"]

    entries = P.index_entries(index_path) if raw_e else {}
    out = {}
    for leg in raw_j:
        # 1. raw journal 이 파싱·schema 를 만족하는가
        j = P.registration(index_path, leg)
        if j is None:
            bad.append(f"{leg}: 등록 journal 이 있는데 파싱·schema 를 만족하지 "
                       "않는다 (잘렸거나 키가 어긋났다)")
            continue
        # 2. public index 에 대응 entry 가 있는가
        e = entries.get(leg)
        if e is None:
            bad.append(f"{leg}: 등록 journal 이 있는데 public index 에 entry 가 없다")
            continue
        # 3. 같은 receipt 를 가리키는가
        if j["receipt_object"] != e.get("receipt_object"):
            bad.append(f"{leg}: journal 이 index 와 다른 receipt 를 가리킨다")
            continue
        # 4. graph 가 실제로 회수되는가
        try:
            out[leg] = P.verify_registered_graph(backend, index_path, leg)
        except P.PreserveError as ex:
            bad.append(f"{leg}: 등록 journal 이 있는데 graph 검증이 실패했다 "
                       f"({ex.stage}: {ex.msg})")
    return out, bad


def _generation_binding_problems(registered: dict, reg: dict,
                                 creg: dict, entries: dict | None = None) -> list[str]:
    """등록 **receipt** ↔ 원장 ↔ 세대표 결속. 순수 함수라 변이를 걸 수 있다."""
    dg = creg.get("source_digest_generations") or {}
    legs = {e["leg_id"]: e for e in reg["legs"]}
    entries = entries or {}
    bad = []
    for leg, receipt in sorted(registered.items()):
        env = (receipt or {}).get("planned_envelope") or {}
        e = legs.get(leg)
        if e is None:
            bad.append(f"{leg}: index 에 등록돼 있는데 원장에 없다")
            continue
        src = (e.get("evidence") or {}).get("leg_source_digest")
        if env.get("source_digest") != src:
            bad.append(f"{leg}: 등록 receipt 의 source_digest "
                       f"{env.get('source_digest')!r} 가 원장 {src!r} 와 다르다")
        if dg.get(env.get("source_digest")) != env.get("protocol_generation"):
            bad.append(f"{leg}: 등록 receipt 의 protocol_generation "
                       f"{env.get('protocol_generation')!r} 가 세대표 "
                       f"{dg.get(env.get('source_digest'))!r} 와 다르다")
        # ★ 32차 P2 — index 의 사본은 **대조 대상**이다. receipt 와 갈리면
        #   그 자체가 오류다 (권위는 receipt).
        # ★ 34차 P2 — `copy is not None` 조건이 **누락 자체**를 봐주고
        #   있었다. 사본이 필수 계약이면 없는 것도 오류다.
        copy = (entries.get(leg) or {}).get("planned_envelope")
        if copy != env:
            bad.append(f"{leg}: public index 의 planned_envelope 사본이 "
                       f"등록 receipt 와 다르다 ({'없다' if copy is None else '값이 다르다'})")
    # 반대 방향 — 원장이 등록을 주장하는데 실물이 없으면 그것도 거짓이다
    for leg, e in sorted(legs.items()):
        if (e.get("evidence") or {}).get("registered_receipt") and \
                leg not in registered:
            bad.append(f"{leg}: 원장은 등록됐다는데 검증된 등록이 없다")
    return bad


def test_a_registered_leg_binds_its_generation_to_the_receipt():
    """★ 30차 P2 / 31차 P2 — 세대 정본은 **등록 receipt** 다.

    ★ 31차 — 30차판은 검사 대상을 가변 원장의 optional 필드로 골랐다. 그래서
      "등록이 생기는 순간 fail-closed 로 켜진다" 는 설명이 **거짓**이었다 —
      필드를 안 적으면 검사가 잠들었다. 그 문장은 철회한다.

      지금은 실제 index 를 읽는다. index 가 아직 없으므로 결과는 여전히
      비어 있지만, **이유가 다르다**: 원장이 고른 것이 아니라 실물이 없는
      것이다. 규칙 자체가 무는지는 아래 합성 index 시험이 보인다.
    """
    import tools.preserve as P

    backend = _open_canonical_backend()
    registered, unreadable = _registered_legs(_PRESERVE_INDEX, backend)
    entries = (P.index_entries(_PRESERVE_INDEX)
               if (_PRESERVE_INDEX / "legs").is_dir() else {})
    bad = unreadable + _generation_binding_problems(
        registered, _leg_preservation(), _claim_status(), entries=entries)
    assert not bad, "등록 세대 결속이 어긋난다:\n  " + "\n  ".join(bad)
    assert registered == {}, (
        f"보존 index 가 생겼다 ({sorted(registered)}) — 묶음 9 배선과 "
        "`STAGE3_CONTRACT.md` §8 의 세대 권위를 함께 갱신해야 한다")


def test_the_generation_binding_bites_on_a_synthetic_registry(tmp_path):
    """★ 31차 P2 — 규칙이 **실제로 무는지**를 합성 index 로 본다.

    실물 index 가 없으면 위 시험은 공허하게 참이다 (전건이 거짓). 30차에
    그것을 "fail-closed 가 미리 켜져 있다" 고 적었고 리뷰가 반박했다.
    여기서는 index 를 만들어 세 방향을 전부 물린다.
    """
    import tools.preserve as P

    reg = _leg_preservation()
    creg = _claim_status()
    leg = "paired_fixed5_v4"
    src = next(e for e in reg["legs"]
               if e["leg_id"] == leg)["evidence"]["leg_source_digest"]
    gen = creg["source_digest_generations"][src]

    def entry(**kw):
        base = {"planned_envelope": {"source_digest": src,
                                     "protocol_generation": gen}}
        base["planned_envelope"].update(kw)
        return {leg: base}

    def both(**kw):
        """receipt 와 index 사본을 **함께** 넘긴다 — 사본 누락도 오류이므로."""
        r = entry(**kw)
        return r, {leg: {"planned_envelope": dict(r[leg]["planned_envelope"])}}

    # 1. 일치하면 통과
    r, ent = both()
    assert _generation_binding_problems(r, reg, creg, entries=ent) == []
    # 2. receipt 의 source_digest 가 원장과 다르면 실패
    r, ent = both(source_digest="a72c0f3a485c19bb")
    bad = _generation_binding_problems(r, reg, creg, entries=ent)
    assert any("source_digest" in b for b in bad), bad
    # 3. receipt 의 세대가 세대표와 다르면 실패
    r, ent = both(protocol_generation="v6")
    bad = _generation_binding_problems(r, reg, creg, entries=ent)
    assert any("protocol_generation" in b for b in bad), bad
    # 3b. ★ 34차 P2 — index 사본이 **없으면** 그것도 오류다
    bad = _generation_binding_problems(entry(), reg, creg, entries={})
    assert any("사본이" in b and "없다" in b for b in bad), bad
    # 4. index 에 있는데 원장에 없으면 실패
    bad = _generation_binding_problems({"ghost_leg": {"planned_envelope": {}}},
                                       reg, creg)
    assert any("원장에 없다" in b for b in bad), bad
    # 5. 원장이 등록을 주장하는데 index 에 없으면 실패
    claimed = {"legs": [dict(e, evidence=dict(e.get("evidence") or {},
                                              registered_receipt={"x": 1}))
                        if e["leg_id"] == leg else e for e in reg["legs"]]}
    bad = _generation_binding_problems({}, claimed, creg)
    assert any("검증된 등록이 없다" in b for b in bad), bad


def test_the_registry_reader_recovers_the_actual_receipt(tmp_path):
    """★ 32차 P2 — reader 가 **실제 receipt** 를 회수하는지.

    31차판 시험은 `planned_id="p"` · `receipt_digest="r"` 로 CAS·receipt·
    backend 없이 `publish()` 와 private `_register()` 만 불러 놓고 그것을
    "real registration" 이라고 불렀다. journal reader 를 증명했을 뿐
    registered receipt discovery 를 증명하지 않았다.

    여기서는 **진짜 트랜잭션**을 돌린다.
    """
    import sys as _sys

    _sys.path.insert(0, str(_REPO / "tests"))
    import test_preserve as TP
    import tools.preserve as P

    index = tmp_path / "index"
    backend = P.CasBackend(root=tmp_path / "cas")
    assert _registered_legs(index, backend) == ({}, [])   # 없으면 비어 있다

    run = TP._make_run(tmp_path)
    P.run_transaction(TP.PLANNED, run, backend, index, TP._hooks())

    got, bad = _registered_legs(index, backend)
    assert bad == []
    assert set(got) == {TP.PLANNED.leg_id}
    env = got[TP.PLANNED.leg_id]["planned_envelope"]
    assert env["protocol_generation"] == TP.PLANNED.protocol_generation
    assert env["source_digest"] == TP.PLANNED.source_digest

    # ★ 33차 P2 — backend 를 못 열면 **조용히 빈 집합** 이 아니라 오류다.
    #   journal 이 있는데 판정할 수 없다는 사실 자체가 gate 실패여야 한다.
    empty, why = _registered_legs(index)
    assert empty == {} and why, "backend 없이 빈 집합을 조용히 돌려줬다"
    assert "backend 를 열 수 없다" in why[0]

    # ★ 33차 P2 — graph 를 잃으면 "등록되지 않은 leg" 로 **사라지면 안 된다**.
    #   32차판은 `continue` 로 숨겼다 — 가장 중요한 상태가 조용해졌다.
    import shutil as _sh
    _sh.rmtree(backend.root / "pins")
    got2, bad2 = _registered_legs(index, backend)
    assert got2 == {}
    assert bad2 and "graph 검증이 실패했다" in bad2[0], bad2


def test_the_index_copy_is_compared_against_the_receipt(tmp_path):
    """★ 32차 P2 — index 의 `planned_envelope` 사본은 **권위가 아니다**.

    receipt 와 갈리면 그 자체가 오류여야 한다.
    """
    reg = _leg_preservation()
    creg = _claim_status()
    leg = "paired_fixed5_v4"
    src = next(e for e in reg["legs"]
               if e["leg_id"] == leg)["evidence"]["leg_source_digest"]
    gen = creg["source_digest_generations"][src]
    env = {"source_digest": src, "protocol_generation": gen}

    receipts = {leg: {"planned_envelope": env}}
    assert _generation_binding_problems(receipts, reg, creg,
                                        entries={leg: {"planned_envelope": env}}) == []
    bad = _generation_binding_problems(
        receipts, reg, creg,
        entries={leg: {"planned_envelope": dict(env, protocol_generation="v6")}})
    assert any("사본이" in b for b in bad), bad


# ─────────────────────────────────────────────────────────────────────────────
# 32차 최소 증거 #9 — immutable generation + 단일 CURRENT
# ─────────────────────────────────────────────────────────────────────────────

def _leg3(tmp: Path, leg: str, tag: bytes) -> Path:
    """leg 하나의 **완전한** 세 파일 staging (36차 #9b).

    `promote_generation()` 이 비공개가 된 뒤로 generation 단위시험도 cohort
    publisher 를 지난다 — 완전성은 이제 우회할 수 없다.
    """
    return _stage(tmp, **{f"{leg}.projection.csv.gz": b"rows-" + tag,
                          f"{leg}.restarts.csv.gz": b"restarts-" + tag,
                          f"{leg}.projection.yaml": b"meta: " + tag + b"\n"})


def _rp():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_rp_mod", _REPO / "docs" / "22p_gap" / "row_projection.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _stage(tmp_path, **files):
    d = tmp_path / "stage"
    d.mkdir(parents=True, exist_ok=True)
    for n, b in files.items():
        (d / n).write_bytes(b)
    return d


def test_promotion_publishes_an_immutable_generation_then_one_pointer(tmp_path):
    """★ 32차 #9 — 승격이 **fixed-name 세 파일**이라 set atomicity 가 아니었다.

    셋을 하나씩 `os.replace` 하므로 중간에 죽으면 새 payload 와 옛 YAML 이
    섞일 수 있다 (manifest-last 로 완화했을 뿐 원자적이지 않다).

    immutable generation directory 에 한 번 쓰고, **단일 pointer** 를 원자적
    으로 옮긴다. generation 은 절대 덮지 않는다.
    """
    rp = _rp()
    out = tmp_path / "out"
    st = _leg3(tmp_path / "s0", "a", b"1")
    rec = rp.promote_cohort_generation(st, out, "a")

    gen = out / "gen" / rec["generation_id"]
    assert gen.is_dir(), "immutable generation directory 가 없다"
    assert not st.exists(), "staging 이 남았다"
    cur = rp.read_current(out)
    assert cur["generation_id"] == rec["generation_id"]
    assert set(cur["files"]) == {"a.projection.csv.gz", "a.restarts.csv.gz",
                                 "a.projection.yaml"}

    # 같은 내용은 멱등, 다른 내용은 **새 generation** (덮지 않는다)
    again = rp.promote_cohort_generation(_leg3(tmp_path / "s1", "a", b"1"), out, "a")
    assert again["generation_id"] == rec["generation_id"]

    two = rp.promote_cohort_generation(_leg3(tmp_path / "s2", "a", b"2"), out, "a")
    assert two["generation_id"] != rec["generation_id"]
    assert gen.is_dir(), "옛 generation 이 사라졌다 — immutable 이 아니다"
    assert (gen / "a.projection.csv.gz").read_bytes() == b"rows-1"
    assert rp.read_current(out)["generation_id"] == two["generation_id"]


def test_a_generation_directory_is_never_overwritten(tmp_path):
    """같은 generation_id 자리에 다른 바이트가 있으면 **거부**한다."""
    rp = _rp()
    out = tmp_path / "out"
    rec = rp.promote_cohort_generation(_leg3(tmp_path / "s0", "a", b"1"), out, "a")
    victim = out / "gen" / rec["generation_id"] / "a.projection.yaml"
    victim.write_bytes(b"tampered\n")
    with pytest.raises(SystemExit) as ei:
        rp.promote_cohort_generation(_leg3(tmp_path / "s1", "a", b"1"), out, "a")
    assert "generation" in str(ei.value)


def test_readers_follow_current_and_a_torn_pointer_is_refused(tmp_path):
    """CURRENT 가 없거나 깨졌거나 없는 generation 을 가리키면 fail-closed."""
    rp = _rp()
    out = tmp_path / "out"
    with pytest.raises(SystemExit):
        rp.read_current(out)                       # 아직 없다

    rec = rp.promote_cohort_generation(_leg3(tmp_path / "s0", "a", b"1"), out, "a")
    (out / "CURRENT").write_text("{oops", encoding="utf-8")
    with pytest.raises(SystemExit):
        rp.read_current(out)

    # ★ 자기정합인데 **실물이 없는** pointer — 앞의 id 검사에 업히지 않게
    #   `generation_id()` 로 직접 만든다. 그래야 "없는 generation" 축이 실제로
    #   실행된다 (변이로 확인: 이 축을 지워도 초판 시험은 초록이었다).
    ghost = {"ghost.yaml": hashlib.sha256(b"nope").hexdigest()}
    (out / "CURRENT").write_text(
        json.dumps({"schema": rp.CURRENT_SCHEMA,
                    "generation_id": rp.generation_id(ghost), "files": ghost}),
        encoding="utf-8")
    with pytest.raises(SystemExit) as ei:
        rp.read_current(out)
    assert "없는 generation" in str(ei.value)


def test_a_torn_pointer_write_never_replaces_a_good_one(tmp_path, monkeypatch):
    """★ 32차 #9 — pointer 전환이 **원자적**이어야 한다.

    CURRENT 를 제자리에서 쓰면 쓰다 죽었을 때 잘린 pointer 가 남고, 읽는 쪽은
    옛 generation 도 새 generation 도 못 본다. temp + `os.replace` 는 옛
    pointer 를 그대로 남긴다.
    """
    rp = _rp()
    out = tmp_path / "out"
    first = rp.promote_cohort_generation(_leg3(tmp_path / "s0", "a", b"1"), out, "a")

    real_write = os.write
    state = {"armed": False}

    def half(fd, data):
        if state["armed"] and len(data) > 8:
            real_write(fd, data[:8])
            raise OSError("쓰다 죽었다 (주입)")
        return real_write(fd, data)

    monkeypatch.setattr(os, "write", half)
    state["armed"] = True
    with pytest.raises(OSError):
        rp._publish_pointer(out, {"schema": rp.CURRENT_SCHEMA,
                                  "generation_id": "9" * 64,
                                  "files": {"x": "y" * 64}})
    state["armed"] = False
    monkeypatch.undo()

    assert rp.read_current(out)["generation_id"] == first["generation_id"], (
        "부분 쓰기가 옛 pointer 를 망가뜨렸다")


def test_a_crash_between_generation_and_pointer_leaves_no_mixed_state(tmp_path,
                                                                     monkeypatch):
    """★ 32차 #9 — pointer 를 옮기기 **직전**에 죽어도 섞이지 않는다.

    옛 CURRENT 가 옛 generation 을 계속 가리켜야 한다.
    """
    rp = _rp()
    out = tmp_path / "out"
    first = rp.promote_cohort_generation(_leg3(tmp_path / "s0", "a", b"1"), out, "a")

    boom = RuntimeError("pointer 직전에 죽었다 (주입)")

    def die(*a, **kw):
        raise boom

    monkeypatch.setattr(rp, "_publish_pointer", die)
    with pytest.raises(RuntimeError):
        rp.promote_cohort_generation(_leg3(tmp_path / "s1", "a", b"2"), out, "a")

    assert rp.read_current(out)["generation_id"] == first["generation_id"], (
        "pointer 가 안 옮겨졌는데 읽는 쪽이 새 generation 을 본다")
    assert rp.read_current(out)["files"]["a.projection.yaml"] == \
        hashlib.sha256(b"meta: 1\n").hexdigest()


def test_the_live_gate_actually_opens_a_backend_when_an_index_exists(tmp_path,
                                                                    monkeypatch):
    """★ 33차 P2 — live gate 가 실제로 backend 를 열어 판정하는지.

    32차판은 `_registered_legs(_PRESERVE_INDEX)` 를 backend 없이 불러
    **언제나 `{}`** 를 검사했다. helper 를 고쳐도 caller 가 그 경로에 닿지
    않으면 아무 것도 닫히지 않는다. 배선을 합성 index 로 물린다.
    """
    import sys as _sys

    import tools.preserve as P

    _sys.path.insert(0, str(_REPO / "tests"))
    import test_preserve as TP

    index = tmp_path / "index"
    backend = P.CasBackend(root=tmp_path / "cas")
    run = TP._make_run(tmp_path)
    P.run_transaction(TP.PLANNED, run, backend, index, TP._hooks())

    mod = _sys.modules[__name__]
    monkeypatch.setattr(mod, "_PRESERVE_INDEX", index)

    # 1. 배선이 없으면 — journal 이 있는데 판정 불가 → 실패해야 한다
    monkeypatch.setattr(mod, "_open_canonical_backend", lambda: None)
    with pytest.raises(AssertionError) as ei:
        mod.test_a_registered_leg_binds_its_generation_to_the_receipt()
    assert "backend 를 열 수 없다" in str(ei.value)

    # 2. 배선이 있으면 — 등록이 발견되고, 원장에 없는 다리라 결속이 실패한다
    monkeypatch.setattr(mod, "_open_canonical_backend", lambda: backend)
    with pytest.raises(AssertionError) as ei:
        mod.test_a_registered_leg_binds_its_generation_to_the_receipt()
    assert "원장에 없다" in str(ei.value), str(ei.value)

    # 3. graph 를 잃으면 조용해지지 않는다
    shutil.rmtree(backend.root / "pins")
    with pytest.raises(AssertionError) as ei:
        mod.test_a_registered_leg_binds_its_generation_to_the_receipt()
    assert "graph 검증이 실패했다" in str(ei.value)


def test_a_cohort_generation_keeps_every_leg_and_switches_once(tmp_path):
    """★ 33차 #9 — 한 leg stage 를 그대로 승격하면 cohort 가 **줄어든다**.

    요구는 immutable **cohort** generation 이지 leg generation 이 아니다.
    G0 에 두 leg 를 두고 한 leg 만 갱신해 G1 을 만든다 — G1 은 두 leg 를 모두
    담아야 하고, pointer 는 **한 번** 바뀌어야 한다.
    """
    rp = _rp()
    out = tmp_path / "cohort"

    g0 = rp.promote_cohort_generation(_stage(tmp_path, **{"a.projection.csv.gz": b"A0c",
                            "a.projection.yaml": b"A0y",
                            "a.restarts.csv.gz": b"A0r"} ), out, "a")
    g0b = rp.promote_cohort_generation(_stage(tmp_path, **{"b.projection.csv.gz": b"B0c",
                            "b.projection.yaml": b"B0y",
                            "b.restarts.csv.gz": b"B0r"} ), out, "b")
    assert len(g0b["files"]) == 6, sorted(g0b["files"])
    assert g0b["generation_id"] != g0["generation_id"]

    g1 = rp.promote_cohort_generation(_stage(tmp_path, **{"a.projection.csv.gz": b"A1c",
                            "a.projection.yaml": b"A1y",
                            "a.restarts.csv.gz": b"A1r"} ), out, "a")
    assert len(g1["files"]) == 6, (
        f"한 leg 를 갱신했더니 cohort 가 줄었다: {sorted(g1['files'])}")
    for sfx in rp.LEG_SUFFIXES:
        assert g1["files"]["b" + sfx] == g0b["files"]["b" + sfx], (
            "손대지 않은 leg 가 바뀌었다")
    assert rp.read_current(out)["generation_id"] == g1["generation_id"]

    # 옛 generation 은 그대로 남아 있다 (immutable)
    assert (out / "gen" / g0b["generation_id"] / "a.projection.yaml"
            ).read_bytes() == b"A0y"


def test_the_production_writer_and_reader_go_through_current(tmp_path):
    """★ 33차 #9 — primitive 가 **배선되지 않으면** 아무 것도 닫히지 않는다.

    32차판 `build()` 는 여전히 세 파일을 하나씩 `os.replace` 했고 reader 도
    fixed path 를 읽었다. `CURRENT` 단위시험이 production crash semantics 를
    증명하지 않는다는 지적 그대로다.
    """
    import inspect

    rp = _rp()
    src = inspect.getsource(rp.build)
    assert "promote_cohort_generation" in src, (
        "production writer 가 generation 승격을 쓰지 않는다")
    assert "os.replace(f, _out" not in src, "옛 파일별 승격이 남아 있다"

    # reader authority
    out = tmp_path / "cohort"
    rec = rp.promote_cohort_generation(_stage(tmp_path, **{"a.projection.csv.gz": b"A0c",
                            "a.projection.yaml": b"A0y",
                            "a.restarts.csv.gz": b"A0r"} ), out, "a")
    assert rp.cohort_bytes(out, "a.projection.yaml") == b"A0y"

    # CURRENT 가 가리키지 않는 이름은 못 읽는다 — fixed path 가 authority 가
    # 아니라는 뜻이다
    (out / "ghost.projection.yaml").write_bytes(b"GHOST\n")
    with pytest.raises(SystemExit):
        rp.cohort_bytes(out, "ghost.projection.yaml")

    # 호환 사본이 CURRENT 와 갈리면 그것도 오류다
    (out / "a.projection.yaml").write_bytes(b"TAMPERED\n")
    with pytest.raises(SystemExit) as ei:
        rp.check_materialized(out)
    assert "CURRENT" in str(ei.value)


def test_the_active_cohort_is_published_through_a_single_current_pointer():
    """★ 33차 #9 — 실제 active cohort 가 CURRENT 를 통해 게시되는지.

    primitive 를 만들어 두고 배선하지 않으면 아무 것도 닫히지 않는다는 지적
    그대로다. 실물 cohort 를 본다.

    frozen cohort(g1)는 **예외**다 — 다시 만들 수 없으므로 옛 fixed-name
    layout 그대로 얼려 둔다. 그 사실을 여기 고정한다 (조용한 예외가 아니라).
    """
    rp = _rp()
    active = [c for c in _cohorts() if c.get("status") == "active"]
    frozen = [c for c in _cohorts() if c.get("status") == "frozen"]
    assert len(active) == 1

    d = _REPO / active[0]["dir"]
    rec = rp.check_materialized(d)          # CURRENT ↔ fixed-name 사본 대조
    legs = sorted({n.split(".", 1)[0] for n in rec["files"]})
    assert legs == sorted(active[0]["legs"]), (
        f"CURRENT 가 담은 다리 {legs} 가 원장의 cohort 구성과 다르다")

    # 모든 leg 의 세 파일이 **한 generation** 안에 있다
    for leg in legs:
        for suffix in (".projection.csv.gz", ".projection.yaml", ".restarts.csv.gz"):
            assert leg + suffix in rec["files"], f"{leg}{suffix} 가 빠졌다"

    for c in frozen:
        assert not (_REPO / c["dir"] / "CURRENT").exists(), (
            f"{c['cohort_id']} 는 frozen 이다 — 새 layout 으로 바꾸지 않는다")


@pytest.mark.parametrize("damage", ["truncated", "empty_object", "foreign_receipt",
                                    "orphan_journal", "missing_index"])
def test_a_damaged_raw_journal_is_an_error_not_an_absence(tmp_path, damage):
    """★ 34차 P2 — 후보 filter 가 깨진 journal 을 graph verifier **앞에서** 숨겼다.

    `has_registration_journal()` 은 raw 파일 존재 술어가 아니다 — 파싱·schema·
    digest 가 깨지거나 `receipt_object` 가 index 와 다르거나 index entry 가
    없으면 전부 `False` 다. 그래서 raw journal 파일이 **실제로 있는데도**
    live gate 는 "등록 0건 · 오류 0건" 을 봤다.

    33차 회귀는 parse-valid journal 을 둔 채 `pins/` 만 지웠으므로 filter 를
    통과한 뒤의 실패만 증명했다 — 이름보다 범위가 한 단계 좁았다.
    """
    import sys as _sys

    import tools.preserve as P

    _sys.path.insert(0, str(_REPO / "tests"))
    import test_preserve as TP

    index = tmp_path / "index"
    backend = P.CasBackend(root=tmp_path / "cas")
    run = TP._make_run(tmp_path)
    P.run_transaction(TP.PLANNED, run, backend, index, TP._hooks())
    leg = TP.PLANNED.leg_id
    j = index / "registered" / f"{leg}.json"

    got, bad = _registered_legs(index, backend)
    assert set(got) == {leg} and bad == [], "전제: 정상 상태"

    if damage == "truncated":
        j.write_bytes(j.read_bytes()[:20])
    elif damage == "empty_object":
        j.write_bytes(b"{}")
    elif damage == "foreign_receipt":
        rec = P.load_canonical(j.read_bytes())
        j.write_bytes(P.canonical_bytes(dict(rec, receipt_object="a" * 64)))
    elif damage == "orphan_journal":
        (index / "registered" / "ghostleg.json").write_bytes(j.read_bytes())
    elif damage == "missing_index":
        (index / "legs" / f"{leg}.json").unlink()

    got, bad = _registered_legs(index, backend)
    assert bad, f"{damage}: raw journal 이 있는데 조용히 지나갔다"
    if damage == "orphan_journal":
        assert any("ghostleg" in b for b in bad), bad
    else:
        assert any(leg in b for b in bad), bad


def test_raw_journals_without_a_backend_are_an_error(tmp_path):
    """raw journal 이 있으면 backend 부재 자체가 오류다 — 조용한 통과가 아니라."""
    index = tmp_path / "index"
    (index / "registered").mkdir(parents=True)
    (index / "registered" / "someleg.json").write_bytes(b"{}")
    got, bad = _registered_legs(index, None)
    assert got == {} and bad and "backend 를 열 수 없다" in bad[0]


def test_real_readers_see_only_the_new_generation_after_a_materialize_crash(
        tmp_path, monkeypatch):
    """★ 34차 #9 — pointer 전환 뒤 `_materialize` 중 죽어도 **실제 reader** 가
    새 generation 만 봐야 한다.

    33차판은 writer 와 새 helper 만 CURRENT 를 썼고 실제 active reader 는
    fixed name 을 읽었다. 그 상태에서 이 crash 가 나면 reader 가 stale G0 또는
    G0/G1 혼합을 **읽는다**. 다음 suite 의 `check_materialized()` 가 나중에
    잡는 것은 이미 벌어진 일을 되돌리지 못한다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    g0 = rp.promote_cohort_generation(
        _stage(tmp_path, **{"a.projection.csv.gz": b"A0c",
                            "a.projection.yaml": b"leg: a\nv: 0\n",
                            "a.restarts.csv.gz": b"A0r"}), out, "a")
    assert (out / "a.projection.yaml").read_bytes() == b"leg: a\nv: 0\n"

    boom = RuntimeError("materialize 중에 죽었다 (주입)")
    monkeypatch.setattr(rp, "_materialize",
                        lambda *a, **kw: (_ for _ in ()).throw(boom))
    with pytest.raises(RuntimeError):
        rp.promote_cohort_generation(
            _stage(tmp_path, **{"a.projection.csv.gz": b"A1c",
                                "a.projection.yaml": b"leg: a\nv: 1\n",
                                "a.restarts.csv.gz": b"A1r"}), out, "a")
    monkeypatch.undo()

    # pointer 는 G1, fixed 사본은 아직 G0 — 여기가 위험 구간이다
    assert rp.read_current(out)["generation_id"] != g0["generation_id"]
    assert (out / "a.projection.yaml").read_bytes() == b"leg: a\nv: 0\n", "전제"

    # **실제 reader** 는 새 generation 을 본다
    cohort = {"cohort_id": "gX", "dir": str(out.relative_to(_REPO))
              if str(out).startswith(str(_REPO)) else None, "status": "active"}
    assert rp.cohort_bytes(out, "a.projection.yaml") == b"leg: a\nv: 1\n"
    assert rp.read_current(out)["files"]["a.projection.yaml"] == \
        hashlib.sha256(b"leg: a\nv: 1\n").hexdigest()


@pytest.mark.parametrize("stage_files", [
    {"a.projection.yaml": b"only-yaml"},                      # csv·restart 없음
    {"a.projection.csv.gz": b"c", "a.projection.yaml": b"y"},  # restart 없음
    {"a.projection.csv.gz": b"c", "a.projection.yaml": b"y",
     "a.restarts.csv.gz": b"r", "a.extra": b"x"},              # 남는 파일
    {"a.projection.csv.gz": b"c", "b.projection.yaml": b"y",
     "a.restarts.csv.gz": b"r"},                               # 다른 leg 섞임
])
def test_a_partial_leg_stage_cannot_be_promoted(tmp_path, stage_files):
    """★ 34차 #9 — "완전한 snapshot" 이 **구조로 강제되지 않았다**.

    `promote_cohort_generation()` 은 stage 의 이름 집합을 얻은 뒤 그 leg 의
    기존 파일을 base 에서 전부 제외했지만, stage 가 `leg + 세 suffix` exact
    set 인지 검사하지 않았다. `{a.projection.yaml}` 만 넘기면 A 의 CSV 와
    restart 를 **제거한** generation 을 정상 게시하고 `read_current()` 도
    통과했다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    with pytest.raises(SystemExit) as ei:
        rp.promote_cohort_generation(_stage(tmp_path, **stage_files), out, "a")
    assert "세 파일" in str(ei.value) or "leg" in str(ei.value)


def test_the_lint_readers_follow_current_not_the_fixed_copies(tmp_path):
    """★ 34차 #9 — **실제 lint reader** 가 CURRENT 를 따르는지.

    33차판은 `_cohort_projections`·`_sealed_projections`·
    `_sealed_source_digest` 가 fixed name 을 직접 읽었다. helper 가 맞는 것과
    실제 소비자가 그것을 쓰는 것은 다른 축이다 — 그래서 여기서는 helper 가
    아니라 **lint 가 쓰는 함수**를 부른다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    rp.promote_cohort_generation(
        _stage(tmp_path, **{"a.projection.csv.gz": b"c0",
                            "a.projection.yaml": b"v: 0\n",
                            "a.restarts.csv.gz": b"r0"}), out, "a")

    active = {"cohort_id": "gX", "dir": "unused", "status": "active"}
    frozen = {"cohort_id": "gF", "dir": "unused", "status": "frozen"}
    assert _cohort_names(active, base=out) == ["a.projection.yaml"]
    assert _cohort_yaml(active, "a.projection.yaml", base=out) == {"v": 0}

    # fixed 사본을 흔든다 — active reader 는 CURRENT 를 따라야 한다
    (out / "a.projection.yaml").write_bytes(b"v: 99\n")
    (out / "ghost.projection.yaml").write_bytes(b"v: 7\n")
    assert _cohort_names(active, base=out) == ["a.projection.yaml"], (
        "active reader 가 CURRENT 밖 파일을 봤다")
    assert _cohort_yaml(active, "a.projection.yaml", base=out) == {"v": 0}, (
        "active reader 가 흔들린 fixed 사본을 읽었다")

    # frozen 은 fixed layout fallback 이다 (원자료를 잃어 migration 불가)
    assert _cohort_names(frozen, base=out) == ["a.projection.yaml",
                                               "ghost.projection.yaml"]
    assert _cohort_yaml(frozen, "a.projection.yaml", base=out) == {"v": 99}


def test_an_incomplete_base_generation_cannot_be_carried_forward(tmp_path):
    """★ 34차 #9 — base 가 이미 불완전하면 물려받지 않는다.

    stage 검사가 새 불완전 generation 을 막지만, 그 검사가 생기기 **전에**
    만들어진 generation 이 있을 수 있다. 그것을 조용히 이어받으면 불완전
    snapshot 이 영구화된다.

    ★ 36차 #9b — 34차판은 이 fixture 를 **살아 있는 publisher**로 만들었다
      (`promote_generation()` 에 한 파일 staging). 그러면 publisher 를 고치는
      순간 fixture 가 같이 변해, 이 시험이 무엇을 보는지 알 수 없게 된다 —
      실제로 publisher 를 비공개로 만들자 fixture 가 먼저 깨졌다. 이제
      generation directory 와 CURRENT 를 **바이트에서** 직접 만든다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    _handmade_generation(rp, out, {"b.projection.yaml": b"y"})

    with pytest.raises(SystemExit) as ei:
        rp.promote_cohort_generation(
            _stage(tmp_path, **{"a.projection.csv.gz": b"c",
                                "a.projection.yaml": b"y",
                                "a.restarts.csv.gz": b"r"}), out, "a")
    assert "불완전" in str(ei.value)


def _handmade_generation(rp, out: Path, blobs: dict) -> str:
    """generation directory 와 CURRENT 를 **바이트에서** 만든다 (36차 #9b).

    publisher 를 전혀 부르지 않는다 — publisher 가 무엇을 막든 상관없이
    "이미 이런 상태가 디스크에 있다" 를 그대로 재현하기 위한 것이다.
    """
    files = {n: hashlib.sha256(b).hexdigest() for n, b in blobs.items()}
    gid = rp.generation_id(files)
    gdir = Path(out) / "gen" / gid
    gdir.mkdir(parents=True, exist_ok=True)
    for n, b in blobs.items():
        (gdir / n).write_bytes(b)
    (Path(out) / "CURRENT").write_text(
        json.dumps({"schema": rp.CURRENT_SCHEMA, "generation_id": gid,
                    "files": files}, sort_keys=True, separators=(",", ":")),
        encoding="utf-8")
    return gid


# ─────────────────────────────────────────────────────────────────────────────
# 36차 #9a — helper 는 CURRENT 를 따랐지만 **실제 판정**은 fixed path 를 읽었다
# ─────────────────────────────────────────────────────────────────────────────

def test_no_reader_touches_the_cohort_fixed_namespace():
    """★ 37차 #9 — 36차 금지는 **함수 이름 하나**였다.

    `_cohort_projections` 호출만 막았으므로 `c["dir"] / f"{leg}.projection.yaml"`
    · glob · 직접 gzip open 은 그대로 통과했고, 실제로 cohort self-consistency
    경로가 그렇게 읽고 있었다. 이름이 아니라 **namespace 접근**을 막는다.

    규칙: cohort record 의 `dir` 을 꺼내는 곳은 snapshot 생성자 하나뿐이다.
    그 밖에서 꺼내면 경로가 소비자에게 흘러가고, 그 순간 고정 사본을 읽을 수
    있게 된다.
    """
    import ast

    src = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    #: snapshot 생성자 — 여기서만 경로를 안다.
    #: `..._published_through_a_single_current_pointer` 는 **자재화 자체**를
    #: 보는 시험이라 예외다: CURRENT 와 고정 사본이 같은지, frozen 에 CURRENT
    #: 가 안 생겼는지를 보려면 layout 을 봐야 한다. 내용을 읽지는 않는다.
    allowed = {"_Snapshot", "__init__", "_snapshot",
               "test_the_active_cohort_is_published_through_a_single_current_pointer"}
    #: cohort record 를 담는 이름들. 다른 record 의 `dir` 은 이 규칙 밖이다
    #: (예: 원점 진단 JSON 의 `dir`).
    cohort_names = {"c", "cohort", "active", "frozen", "co"}

    def _is_cohort(node) -> bool:
        base = node.value
        while isinstance(base, ast.Subscript):
            base = base.value
        return isinstance(base, ast.Name) and base.id in cohort_names

    bad = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if fn.name in allowed:
            continue
        for n in ast.walk(fn):
            if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) \
                    and n.slice.value == "dir" and _is_cohort(n):
                bad.append(f"{fn.name}:{n.lineno}")
    assert not bad, (
        "cohort dir 을 snapshot 밖에서 꺼낸다 — 고정 namespace 로 가는 통로다:\n  "
        + "\n  ".join(bad))


def test_no_cohort_assertion_reads_a_fixed_path():
    """★ 36차 #9a — `_cohort_projections()` 가 우회로였다.

    34차에 `_cohort_names`·`_cohort_yaml` 을 CURRENT 로 옮겼지만, 실제
    판정 넷(cohort 계산 provenance · active 현행성 · schema/pin · 전 투영
    pin)은 여전히 `_cohort_projections(c)` 가 준 **고정 경로**를 열었다.
    docstring 에 "판정에는 쓰지 않는다" 라고 적어 두는 것은 강제가 아니다 —
    31차에 enforcement 를 caller label 로 받았던 것과 같은 실수다.

    그래서 그 함수를 **없앤다**. 여기서는 AST 로 확인한다 — 다시 생기면
    이 시험이 먼저 깨진다.
    """
    import ast

    src = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)

    defined = [n.name for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef) and n.name == "_cohort_projections"]
    assert not defined, (
        "`_cohort_projections` 가 다시 생겼다 — 고정 경로 우회로다. "
        "cohort 판정은 `_cohort_manifests()` 로만 한다")

    called = sorted({f.name for f in ast.walk(tree)
                     if isinstance(f, ast.FunctionDef)
                     for n in ast.walk(f)
                     if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                     and n.func.id == "_cohort_projections"})
    assert not called, f"고정 경로 reader 를 부르는 판정: {called}"


@pytest.mark.parametrize("k", [0, 1, 2])
def test_a_crash_midway_through_materialize_never_moves_the_authority(tmp_path, k,
                                                                     monkeypatch):
    """★ 36차 #9a — 파생 사본을 만드는 중에 죽으면 무엇이 참인가.

    `_materialize()` 는 `os.replace` 를 파일 수만큼 반복한다. 그 사이에 죽으면
    fixed-name 사본은 **새 것과 옛 것이 섞인다**. 34·35차는 이 상태를 한 번도
    만들어 보지 않았다 — 승격이 원자적인 것은 CURRENT 뿐인데, 소비자가 사본을
    읽던 시절의 상태 공간을 그대로 두고 "원자적" 이라고 불렀다.

    고정하는 불변식 셋:
      1. 권위(`read_current`·`cohort_bytes`)는 섞인 사본에 영향받지 않는다
      2. 섞인 것을 `check_materialized()` 가 **말한다** (조용히 넘어가지 않는다)
      3. 같은 승격을 다시 돌리면 복구된다 (멱등)
    """
    rp = _rp()
    out = tmp_path / "cohort"
    rp.promote_cohort_generation(
        _stage(tmp_path / "s0", **{"a.projection.csv.gz": b"c0",
                                   "a.projection.yaml": b"v: 0\n",
                                   "a.restarts.csv.gz": b"r0"}), out, "a")
    old = {n: (out / n).read_bytes() for n in ("a.projection.csv.gz",
                                               "a.projection.yaml",
                                               "a.restarts.csv.gz")}

    real, calls = os.replace, {"n": 0}

    def _dying(src, dst):
        # gen 디렉터리 이동·CURRENT 전환은 통과시키고, 사본 replace 만 센다
        if Path(dst).parent == out and Path(dst).name in old:
            if calls["n"] >= k:
                raise _MaterializeCrash(Path(dst).name)
            calls["n"] += 1
        return real(src, dst)

    monkeypatch.setattr(rp.os, "replace", _dying)
    with pytest.raises(_MaterializeCrash):
        rp.promote_cohort_generation(
            _stage(tmp_path / "s1", **{"a.projection.csv.gz": b"c1",
                                       "a.projection.yaml": b"v: 1\n",
                                       "a.restarts.csv.gz": b"r1"}), out, "a")
    monkeypatch.undo()

    # 1. 권위는 이미 새 generation 이고, 바이트도 새 것이다
    cur = rp.read_current(out)
    assert rp.cohort_bytes(out, "a.projection.yaml") == b"v: 1\n", (
        "섞인 사본이 권위 읽기를 오염시켰다")
    assert rp.cohort_bytes(out, "a.projection.csv.gz") == b"c1"

    # 2. 섞였다는 것을 말해야 한다 — k 개만 새 것이므로 하나 이상 옛 것이다
    with pytest.raises(SystemExit) as ei:
        rp.check_materialized(out)
    assert "CURRENT" in str(ei.value)

    # 3. 같은 승격을 다시 돌리면 복구된다
    rp.promote_cohort_generation(
        _stage(tmp_path / "s2", **{"a.projection.csv.gz": b"c1",
                                   "a.projection.yaml": b"v: 1\n",
                                   "a.restarts.csv.gz": b"r1"}), out, "a")
    assert rp.check_materialized(out)["generation_id"] == cur["generation_id"], (
        "재실행이 같은 generation 으로 복구하지 못했다")


class _MaterializeCrash(RuntimeError):
    """`_materialize` 중간에서 죽이는 표식."""


# ─────────────────────────────────────────────────────────────────────────────
# 36차 #9b — 불완전 generation 을 **public API 로 만들 수 있었다**
# ─────────────────────────────────────────────────────────────────────────────

def test_the_incomplete_publisher_is_not_public(tmp_path):
    """★ 36차 #9b — `promote_generation()` 이 공개 publisher 였다.

    34차에 `promote_cohort_generation()` 이 leg 세 파일 exact set 을 강제하게
    했지만, 그 검사를 **거치지 않는** `promote_generation(stage, out)` 이 같은
    module 의 공개 이름으로 남아 있었다. 한 파일짜리 staging 을 그대로 넘기면
    cohort 를 한 파일로 줄인 generation 이 CURRENT 로 정상 게시된다.
    검사를 하나 더 두는 것과 **만들 수 없게 하는 것**은 다르다.
    """
    rp = _rp()
    assert not hasattr(rp, "promote_generation"), (
        "불완전 generation 을 만들 수 있는 publisher 가 공개돼 있다")
    assert callable(getattr(rp, "_promote_generation", None)), (
        "내부 publisher 자체가 사라지면 안 된다 (cohort publisher 가 쓴다)")


def test_reading_current_refuses_an_incomplete_cohort(tmp_path):
    """★ 36차 #9b — 완전성 검사가 **쓰는 쪽에만** 있었다.

    `promote_cohort_generation()` 은 세 파일을 요구하지만, 이미 게시된
    CURRENT 가 불완전하면 읽는 쪽은 아무 말도 안 했다. 원장·CURRENT 를
    직접 편집하거나 옛 판으로 만든 generation 을 물려받으면 그대로 통과한다.
    fixture 는 **바이트에서** 만든다 — 살아 있는 publisher 로 만들면
    publisher 를 고치는 순간 이 시험이 무엇을 보는지 알 수 없게 된다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    rp.promote_cohort_generation(
        _stage(tmp_path / "s", **{"a.projection.csv.gz": b"c0",
                                  "a.projection.yaml": b"v: 0\n",
                                  "a.restarts.csv.gz": b"r0"}), out, "a")

    # 세 파일 중 하나를 뺀 generation 을 **손으로** 만든다 (publisher 우회)
    files = {"a.projection.yaml": hashlib.sha256(b"v: 0\n").hexdigest(),
             "a.projection.csv.gz": hashlib.sha256(b"c0").hexdigest()}
    gid = rp.generation_id(files)
    gdir = out / "gen" / gid
    gdir.mkdir(parents=True)
    (gdir / "a.projection.yaml").write_bytes(b"v: 0\n")
    (gdir / "a.projection.csv.gz").write_bytes(b"c0")
    (out / "CURRENT").write_text(json.dumps(
        {"schema": rp.CURRENT_SCHEMA, "generation_id": gid, "files": files},
        sort_keys=True, separators=(",", ":")), encoding="utf-8")

    with pytest.raises(SystemExit) as ei:
        rp.read_current(out)
    assert "restarts" in str(ei.value) or "불완전" in str(ei.value), (
        f"불완전한 cohort 를 그대로 읽었다: {ei.value}")


def test_a_lost_update_cannot_silently_drop_another_legs_generation(tmp_path):
    """★ 36차 #9 / 37차 #9 — **성공을 반환했으면 남아 있어야 한다.**

    36차판은 "A 가 거부된다" 를 요구했는데, 그것은 구현을 하나로 못 박는
    과잉 규정이었다. 진짜 불변식은 이것이다 — 성공을 돌려준 승격의 leg 는
    최종 `CURRENT` 에 있어야 한다. 직렬화로 이루든 거부로 이루든 상관없다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    rp.promote_cohort_generation(
        _stage(tmp_path / "s0", **{"a.projection.csv.gz": b"c0",
                                   "a.projection.yaml": b"v: 0\n",
                                   "a.restarts.csv.gz": b"r0"}), out, "a")

    real = rp.read_current
    ok = []

    def _interleave(o):
        rec = real(o)
        if not ok:                       # A 의 첫 read 중에 B 가 끼어든다
            ok.append("armed")
            rp.read_current = real
            try:
                rp.promote_cohort_generation(
                    _stage(tmp_path / "sb", **{"b.projection.csv.gz": b"bc",
                                               "b.projection.yaml": b"v: b\n",
                                               "b.restarts.csv.gz": b"br"}), o, "b")
                ok.append("b")
            except SystemExit:
                pass                     # 직렬화로 거부됐다 — 정당하다
            rp.read_current = _interleave
        return rec

    rp.read_current = _interleave
    try:
        try:
            rp.promote_cohort_generation(
                _stage(tmp_path / "s1", **{"a.projection.csv.gz": b"c1",
                                           "a.projection.yaml": b"v: 1\n",
                                           "a.restarts.csv.gz": b"r1"}), out, "a")
            ok.append("a")
        except SystemExit:
            pass
    finally:
        rp.read_current = real

    cur = rp.read_current(out)
    assert ok, "둘 다 거부됐다 — 진행이 불가능하면 그것도 고장이다"
    if "b" in ok:
        assert "b.projection.yaml" in cur["files"], (
            "B 가 성공을 돌려줬는데 leg 가 사라졌다")
    if "a" in ok:
        assert cur["files"]["a.projection.yaml"] == \
            hashlib.sha256(b"v: 1\n").hexdigest(), (
            "A 가 성공을 돌려줬는데 그 세대가 아니다")


# ─────────────────────────────────────────────────────────────────────────────
# 37차 #9 — `expected_current` 는 compare-and-swap 이 아니었다
# ─────────────────────────────────────────────────────────────────────────────

def test_a_publish_between_compare_and_replace_cannot_be_lost(tmp_path):
    """★ 37차 #9 — compare 와 replace 가 **따로**였다.

    36차판은 `CURRENT` 를 읽어 expected 와 대조한 뒤, 별도의 무조건
    `os.replace` 로 게시했다. 두 writer 가 같은 옛 값을 읽고 차례로 replace
    하면 뒤 writer 가 앞의 **완전한 generation** 을 조용히 잃게 한다:

        CURRENT = G0
        A: read_current() → G0 · expected == G0 확인
                                 B: 전 과정 게시 → CURRENT = GB
        A: CURRENT := GA          ← GB 가 사라진다

    36차 회귀는 A 의 비교 read **전에** B 를 게시해 A 가 GB 를 보고 실패하는
    쉬운 schedule 만 잡았다. 여기서는 A 의 비교 read 가 G0 를 **반환한 뒤**
    B 를 끼운다. 대조를 한 줄 뒤로 옮기는 것으로는 못 막는다 — 임계 구역이
    필요하다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    rp.promote_cohort_generation(
        _stage(tmp_path / "s0", **{"a.projection.csv.gz": b"c0",
                                   "a.projection.yaml": b"v: 0\n",
                                   "a.restarts.csv.gz": b"r0"}), out, "a")

    real = rp.read_current
    state = {"seen": 0, "b_ok": False, "a_ok": False}

    def _stale(o):
        rec = real(o)
        state["seen"] += 1
        if state["seen"] == 2:           # A 의 **비교용** read 직후
            rp.read_current = real
            try:
                rp.promote_cohort_generation(
                    _stage(tmp_path / "sb", **{"b.projection.csv.gz": b"bc",
                                               "b.projection.yaml": b"v: b\n",
                                               "b.restarts.csv.gz": b"br"}), o, "b")
                state["b_ok"] = True
            except SystemExit:
                pass                     # 임계 구역이 막았다 — 정당하다
            rp.read_current = _stale
        return rec

    rp.read_current = _stale
    try:
        try:
            rp.promote_cohort_generation(
                _stage(tmp_path / "s1", **{"a.projection.csv.gz": b"c1",
                                           "a.projection.yaml": b"v: 1\n",
                                           "a.restarts.csv.gz": b"r1"}), out, "a")
            state["a_ok"] = True
        except SystemExit:
            pass
    finally:
        rp.read_current = real

    cur = rp.read_current(out)
    assert state["a_ok"] or state["b_ok"], "둘 다 거부됐다"
    if state["b_ok"]:
        assert "b.projection.yaml" in cur["files"], (
            "B 가 성공을 돌려줬는데 A 의 replace 가 지웠다 — expected 대조는 "
            "CAS 가 아니다")
    if state["a_ok"]:
        assert cur["files"]["a.projection.yaml"] == \
            hashlib.sha256(b"v: 1\n").hexdigest()


def test_a_live_publish_lock_blocks_and_a_stale_one_is_reclaimed(tmp_path):
    """★ 37차 #9 — 임계 구역을 넣었으면 **crash 잔여 의미**도 정해야 한다.

    lock 이 죽은 채 남아 영구히 게시를 막으면 그것대로 고장이다. 살아 있는
    lock 은 막고, 오래된 lock 은 회수한다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    out.mkdir(parents=True)
    lock = out / ".publish.lock"

    lock.write_text("99999", encoding="utf-8")          # 방금 잡힌 lock
    with pytest.raises(SystemExit) as ei:
        rp.promote_cohort_generation(
            _stage(tmp_path / "s0", **{"a.projection.csv.gz": b"c0",
                                       "a.projection.yaml": b"v: 0\n",
                                       "a.restarts.csv.gz": b"r0"}), out, "a")
    assert "진행 중" in str(ei.value)

    old = time.time() - rp._LOCK_STALE_S - 60
    os.utime(lock, (old, old))                          # crash 잔여로 늙힌다
    rec = rp.promote_cohort_generation(
        _stage(tmp_path / "s1", **{"a.projection.csv.gz": b"c0",
                                   "a.projection.yaml": b"v: 0\n",
                                   "a.restarts.csv.gz": b"r0"}), out, "a")
    assert rec["generation_id"], "늙은 lock 이 게시를 영구히 막았다"
    assert not lock.exists(), "게시 뒤 lock 을 안 풀었다"


# ─────────────────────────────────────────────────────────────────────────────
# 37차 #9 — completeness 가 **observed files** 에 대해서만 닫혀 있었다
# ─────────────────────────────────────────────────────────────────────────────

def test_an_empty_generation_is_not_complete(tmp_path):
    """★ 37차 #9 — `files={}` 는 "모든 leg 가 완전하다" 를 공허참으로 만족했다.

    관측된 leg 를 순회하는 검사이므로 leg 가 하나도 없으면 통과한다. 빈
    generation 을 가리키는 CURRENT 가 정상으로 읽혔다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    _handmade_generation(rp, out, {})
    with pytest.raises(SystemExit) as ei:
        rp.read_current(out)
    assert "비었다" in str(ei.value) or "불완전" in str(ei.value)


def test_a_whole_leg_missing_from_the_roster_is_not_complete(tmp_path):
    """★ 37차 #9 — leg 가 **통째로** 빠지면 observed 순회는 못 본다.

    expected roster 가 `{A, B}` 인데 B 의 세 파일이 전부 없으면, 남은 A 는
    완전하므로 검사가 통과한다. cohort 를 축소한 generation 이 정상 게시되고
    정상으로 읽힌다. 완전성은 **관측된 것**이 아니라 **기대 명부**에 대해
    닫혀야 한다.
    """
    rp = _rp()
    out = tmp_path / "cohort"
    rp.promote_cohort_generation(
        _stage(tmp_path / "sa", **{"a.projection.csv.gz": b"c0",
                                   "a.projection.yaml": b"v: 0\n",
                                   "a.restarts.csv.gz": b"r0"}), out, "a")
    rp.promote_cohort_generation(
        _stage(tmp_path / "sb", **{"b.projection.csv.gz": b"bc",
                                   "b.projection.yaml": b"v: b\n",
                                   "b.restarts.csv.gz": b"br"}), out, "b")
    assert set(rp.read_current(out)["files"]) >= {"b.projection.yaml"}, "전제"

    # B 를 통째로 뺀 generation 을 **바이트에서** 만든다 (publisher 우회)
    _handmade_generation(rp, out, {"a.projection.csv.gz": b"c0",
                                   "a.projection.yaml": b"v: 0\n",
                                   "a.restarts.csv.gz": b"r0"})
    with pytest.raises(SystemExit) as ei:
        rp.read_current(out, expect_legs={"a", "b"})
    assert "b" in str(ei.value)


def test_the_publisher_and_the_reader_share_one_validator():
    """★ 37차 #9 — 36차에 publisher 쪽 검사를 **지운 것이 틀렸다.**

    변이가 안 물길래 중복으로 보고 지웠는데, 리뷰의 답은 "validator 가 약했던
    것" 이었다. 옳은 구조는 같은 **pure validator** 를 publish 와 read 양쪽에서
    부르는 것이다. publisher 가 private 라는 이름 규약은 trust boundary 가
    아니므로 read-side fail-closed 를 없앨 근거가 못 된다.
    """
    import ast

    rp = _rp()
    assert callable(getattr(rp, "assert_cohort_complete", None)), (
        "공유 validator 가 없다")

    src = (_REPO / "docs" / "22p_gap" / "row_projection.py").read_text(
        encoding="utf-8")
    callers = {fn.name for fn in ast.walk(ast.parse(src))
               if isinstance(fn, ast.FunctionDef)
               for n in ast.walk(fn)
               if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == "assert_cohort_complete"}
    assert "read_current" in callers, "reader 가 validator 를 안 부른다"
    assert any(c.startswith("_promote") or c.startswith("promote")
               for c in callers), "publisher 가 validator 를 안 부른다"
