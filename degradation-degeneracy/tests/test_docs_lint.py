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
    assert reg.get("schema_version") == 1
    ids = [c["id"] for c in reg["claims"]]
    assert len(ids) == len(set(ids)), f"claim id 중복: {ids}"
    for c in reg["claims"]:
        assert c["status"] in ("retracted", "downgraded"), c
        assert c["record"] in ("quarantined", "removed"), c
        assert c["banned"], f"{c['id']}: banned 가 비었다 — 검사할 것이 없다"
        for pat in c["banned"]:
            re.compile(pat)          # 잘못된 정규식이면 여기서 죽는다
        for f in c["files"]:
            assert (_REPO / f).is_file(), f"{c['id']}: 대상 파일 없음 {f}"


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
            raw = (_REPO / rel).read_text(encoding="utf-8")
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
            _, fenced = _active_text((_REPO / rel).read_text(encoding="utf-8"))
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
    것은 다봉성이 아니라 후보 집합에 결정론적 점 하나가 늘어난 것뿐이다.

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

    need = sorted({l for l, _ in _WARM_CLAIMS}
                  | {l for p in _WARM_PAIRS for l in p}
                  | {l for a, b, _ in _CONFOUNDED_PAIRS for l in (a, b)}
                  | {l for p in _XDIGEST_PAIRS for l in p})
    missing = [l for l in need if not (_WARM / f"{l}.projection.yaml").is_file()]
    assert not missing, (
        "행 수준 투영이 없는 다리 (원자료가 있는 기계에서 "
        "`python docs/22p_gap/row_projection.py --all` 을 돌려 커밋할 것):\n  "
        + "\n  ".join(missing))

    bad = []
    for leg in need:
        m = yaml.safe_load((_WARM / f"{leg}.projection.yaml").read_text(encoding="utf-8"))
        gz = _WARM / m["projection_file"]
        if not gz.is_file():
            bad.append(f"{leg}: 투영 파일 없음 {m['projection_file']}")
            continue
        if m.get("projection_schema") != 2:
            bad.append(
                f"{leg}: 투영 스키마가 {m.get('projection_schema')} 다 (2 필요). "
                f"22차 발견 5 대응 필드(실제 fits SHA·전체 semantic 대조·"
                f"restart 투영·분석기 provenance)가 없다 — 원자료가 있는 기계에서 "
                f"`python docs/22p_gap/row_projection.py --all` 을 다시 돌려라")
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
        for obj, want in (m.get("by_objective_sha256") or {}).items():
            sub = [ln for ln in body if ln.split("\t")[oi] == obj]
            blob = ("\n".join([head, *sub]) + "\n").encode("utf-8")
            if hashlib.sha256(blob).hexdigest() != want["sha256"]:
                bad.append(f"{leg}/{obj}: 부분 digest 가 TSV 재계산과 다르다")
            if len(sub) != want["n_rows"]:
                bad.append(f"{leg}/{obj}: 행 수 {len(sub)} vs 기록 {want['n_rows']}")

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
        if not rp or not (_WARM / rp).is_file():
            bad.append(f"{leg}: restart 수준 투영이 없다")
        elif hashlib.sha256(gzip.decompress((_WARM / rp).read_bytes())).hexdigest() \
                != m.get("restart_projection_sha256"):
            bad.append(f"{leg}: restart 투영이 digest 와 다르다")
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


#: 원장이 관할하는 파일 전체 — 여기 있는 파일의 claim ID 는 원장에 있어야 한다.
#: ★ 22차 발견 7: wiki 가 빠져 있었고, `wiki/questions/22p-physics-or-degeneracy.md`
#:   가 철회된 축 순위와 restart 처방을 다시 주장하고 있었다.
_CLAIM_SCOPE = [
    "degradation-degeneracy/docs/09_22P_GAP.md",
    "degradation-degeneracy/docs/08_REVIEW_RESPONSE.md",
    "degradation-degeneracy/docs/22p_gap/LEG_INVENTORY.md",
    "degradation-degeneracy/docs/22p_gap/STAGE3_CONTRACT.md",
    "wiki/questions/22p-physics-or-degeneracy.md",
]
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


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


def test_lean_review_base_resolution_in_three_git_states():
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


def test_all_projections_share_one_compute_provenance():
    """★ 22차 자체 발견 — 8다리가 두 생성기 판으로 갈려 있었다.

    비교 집합의 다리들이 서로 다른 분석기로 만들어지면, 다리 간 digest 비교
    (`test_cross_digest_exact_pair_reproduces_row_for_row` 등)가 "같은 규격으로
    만든 것을 비교한다" 는 전제를 잃는다.

    실제로 갈렸다: 7다리 `b46389d0`, `paired_fixed5_v4` `5711f104`. 확인해 보니
    **차이는 `main()` 의 출력 문구뿐**이었고 계산 함수는 바이트 동일이었다.
    그러나 리뷰어는 sha 만 보고 그것을 알 수 없다.

    그래서 provenance 를 **계산 경로만** 해시하도록 바꾸고(`compute_sha256`),
    비교 집합 전체가 하나로 같은지를 여기서 강제한다. 표시 코드를 고쳐도
    이 테스트는 깨지지 않고, **계산이 바뀌면 반드시 깨진다.**

    `analysis_spec_sha256`(무엇을 만들기로 했는가)도 함께 본다 — 둘 다 같아야
    "같은 규격을, 같은 코드로" 가 성립한다.
    """
    import collections
    import yaml

    seen: dict[str, dict[str, list[str]]] = collections.defaultdict(
        lambda: collections.defaultdict(list))
    for y in sorted(_WARM.glob("*.projection.yaml")):
        m = yaml.safe_load(y.read_text(encoding="utf-8"))
        a = m.get("analyzer") or {}
        seen["compute_sha256"][a.get("compute_sha256")].append(m["leg_id"])
        seen["analysis_spec_sha256"][m.get("analysis_spec_sha256")].append(m["leg_id"])
        seen["src_scoring_py_sha256"][a.get("src_scoring_py_sha256")].append(m["leg_id"])

    bad = []
    for field, groups in seen.items():
        if None in groups:
            bad.append(f"{field}: 기록이 없는 다리 {groups[None]}")
        if len(groups) > 1:
            detail = " / ".join(f"{k}: {len(v)}다리 {v[:3]}…" if len(v) > 3
                                else f"{k}: {v}" for k, v in groups.items())
            bad.append(f"{field} 가 갈렸다 — {detail}")
    assert not bad, (
        "비교 집합의 분석기 provenance 가 하나가 아니다:\n  " + "\n  ".join(bad)
        + "\n  원자료가 있는 기계에서 `python docs/22p_gap/row_projection.py --all` "
          "로 전부 다시 만들어라.")
