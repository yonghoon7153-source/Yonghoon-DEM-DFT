"""v3 묶음 G — 원장 화면(/governance · /ledger · /kb) 회귀.

이 파일이 지키는 것 (전부 **음성 경로 포함**):
  ① 결정 원장이 인용위험 표 **위**에 온다 · 옛 결정은 접히되 DOM 에 남는다
  ② 행 앵커(`id=<결정 ID>`)와 본문 안 결정 ID 자동 링크 — **원장에 있는 id 만**
  ③ kb 마크다운 읽기 화면 — 화이트리스트가 탈출·비-md·kb 밖을 실제로 막는가
  ④ correction 레코드가 **빈 행이 아니다** (게이트 필드만 읽던 버그)
  ⑤ 초록 배너가 검사 **범위**를 말하고, 실제 위험 카운터가 원장에서 파생된다
  ⑥ 인용위험 행의 '결속됨 / 산문' 구분이 hazard_ids ↔ hazard_claims 의 차이와 맞는가

⛔ 이 파일이 못 하는 것: 화면이 **예쁜지**·읽기 쉬운지는 못 본다. 그리고 원장 값이
  물리적으로 맞는지는 여기서도 안 본다 (이 화면의 설계 선언 그대로).
"""
import html
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as A          # noqa: E402
import canonical as C    # noqa: E402
import data as D         # noqa: E402


@pytest.fixture()
def gov_html():
    A.app.config["TESTING"] = True
    r = A.app.test_client().get("/governance")
    assert r.status_code == 200
    return r.get_data(as_text=True)


# ── ① 절 순서 · 옛 결정 접기 ────────────────────────────────────────────────
def test_decision_ledger_comes_before_citation_hazards(gov_html):
    """결정 원장이 인용위험 표 **위**에 온다 (v3 IA).

    종전에는 페이지 절반을 먹는 결정 표가 25행짜리 인용위험 표 뒤에 있어서, 가장 최신·
    가장 자주 보는 원장에 스크롤로만 닿았다.
    """
    i_dec = gov_html.find("📜 결정 원장")
    i_haz = gov_html.find("⛔ 인용 위험 원장")
    assert i_dec > 0 and i_haz > 0, "두 절이 다 있어야 한다"
    assert i_dec < i_haz, "결정 원장이 인용위험 표보다 뒤에 있다"


def test_old_decisions_are_folded_not_deleted(gov_html):
    """[음성] 대체·철회된 결정을 **DOM 에서 빼면** 안 된다 — 접기만 한다."""
    old = [d for d in C.decisions().values()
           if C.decision_state(d) in ("superseded", "retracted")]
    assert old, "전제: 대체·철회된 결정이 원장에 있다"
    for d in old:
        assert f'id="{d["id"]}"' in gov_html, (
            f"{d['id']} 가 DOM 에 없다 — 접는 것과 지우는 것은 다르다")
    # 접혀 있기는 해야 한다 (활성 결정과 같은 굵기로 인라인에 두지 않는다)
    m = re.search(r"<details[^>]*>\s*<summary>↩ 옛 결정.*?</details>", gov_html, re.S)
    assert m, "옛 결정 접힘 블록이 없다"
    for d in old:
        assert f'id="{d["id"]}"' in m.group(0), f"{d['id']} 가 접힘 밖에 있다"


def _probe(s):
    """이스케이프·`**`볼드 변환을 **안 타는** 안전한 조각(12자 이상)을 고른다.

    화면은 `|bold` 를 거치므로 원문 그대로 비교하면 `**`·따옴표·`&` 에서 헛방이 난다.
    그런 글자가 없는 구간만 골라 대조한다. 없으면 None (그 항목은 건너뛴다).
    """
    parts = [p.strip() for p in re.split(r"[*<>&'\"]+", str(s))]
    parts = [p for p in parts if len(p) >= 12]
    return parts[0] if parts else None


def test_list_reopen_criteria_is_not_rendered_as_python_repr(gov_html):
    """[음성] 배열로 적힌 재개 조건이 **파이썬 repr** 로 새면 안 된다.

    ⛔ 2026-09-15 실측 — 원장 34건 중 **6건이 `reopen_criteria` 를 배열**로 적는데 화면이
      `{{ d.reopen_criteria|bold }}` 로 그렸다. 필터가 `str(list)` 를 해서
      `['다음 5–10 캠페인에서 escaped P0/P1 …']` 가 대괄호·따옴표째 화면에 나왔다.
      **오류는 안 났다** — 1저자가 눈으로 보고 "깨져서 나온다" 고 알려 줘야 잡혔다.
      같은 결함이 `/composition` 에도 있었다(`(… or "")[:240]` 가 리스트에서는
      **원소 240개**를 자른다 — 240자가 아니다).

    ⛔ 이 시험이 못 하는 것: 재개 조건이 **옳은지**는 안 본다. 모양만 본다.
    """
    rows = [d for d in C.decisions().values()
            if isinstance(d.get("reopen_criteria"), list) and d["reopen_criteria"]]
    assert rows, "전제: 배열로 적힌 재개 조건이 원장에 있다 (없으면 이 시험이 헛것을 잰다)"
    # ⚠ **이스케이프를 푼 뒤** 본다. `|bold` 가 escape() 를 먼저 걸어서 repr 의 작은따옴표가
    #   `&#39;` 로 나간다 — 날 HTML 에서 `['` 를 찾으면 **깨진 화면에서도 통과한다**.
    #   (이 시험을 쓰고 대상을 일부러 되돌려 봤더니 초록이었다. 그래서 고쳤다.)
    plain = html.unescape(gov_html)
    bad = [m.start() for m in re.finditer(r"\['|\[\"", plain)]
    assert not bad, ("파이썬 repr 이 화면에 샜다 — 목록을 문자열처럼 그린 자리가 있다: "
                     + plain[max(0, bad[0] - 60):bad[0] + 90])
    # ⚠ **태그를 벗긴 뒤** 항목 존재를 본다 (2026-09-18 추가).
    #   `declink` 가 본문에 적힌 **결정 id 를 링크로** 바꾼다 — 그건 맞는 동작이고
    #   권장되는 상호참조다. 그런데 날 HTML 에서 원문을 찾으면 그 자리에서 문자열이
    #   끊겨 **화면이 멀쩡한데도 빨간불**이 난다 (D-2026-09-18-…-neb-estimand 실측).
    #   ⛔ 위 repr 검사는 `plain`(태그 살아있음) 그대로 둔다 — 그건 다른 결함을 본다.
    stripped = re.sub(r"<[^>]+>", "", plain)
    for d in rows:
        for item in d["reopen_criteria"]:
            p = _probe(item)
            if p:
                assert p in stripped, \
                    f"{d['id']} 의 재개 조건 항목이 화면에 없다: {p[:40]}"


def test_old_ratifications_fold_keeps_unratified_rows_open(gov_html):
    """오래된 **비준**만 접는다 — 미결(제안·비준 없음)은 나이와 무관하게 편다.

    1저자 요청(2026-09-15): "오래된 비준은 토글로 닫아주고". 접는 것과 지우는 것은 다르다 —
    접힌 행도 DOM 에 그대로 있고(`test_every_decision_row_has_an_anchor` 가 본다),
    접힌 규칙은 **여전히 유효**하다.

    [음성] 비준이 없는 행이 접힘 **안**으로 들어가면 실패한다. 미결을 접으면 잊힌다.
    """
    m = re.search(r"<details[^>]*>\s*<summary>🔒 오래된 비준.*?</details>", gov_html, re.S)
    if not m:
        pytest.skip("접을 만큼 오래된 비준이 아직 없다 (원장이 자라면 이 시험이 켜진다)")
    fold = m.group(0)
    unratified = [d for d in C.decisions().values()
                  if (d.get("ratification") or {}).get("state") != "ratified"
                  and C.decision_state(d) not in ("superseded", "retracted")]
    assert unratified, "전제: 비준 없는 결정이 원장에 있다"
    for d in unratified:
        assert f'id="{d["id"]}"' not in fold, \
            f"{d['id']} 는 비준이 없는데 접혔다 — 미결은 펴 둔다"
    # 접힌 것은 전부 비준된 행이어야 한다
    folded_ids = re.findall(r'<tr id="(D-[^"]+)"', fold)
    assert folded_ids, "접힘이 비어 있다"
    for i in folded_ids:
        d = C.decisions().get(i) or {}
        assert (d.get("ratification") or {}).get("state") == "ratified", \
            f"{i} 는 비준 상태가 아닌데 '오래된 비준' 으로 접혔다"


def test_kind_chips_are_derived_from_the_ledger(gov_html):
    """칩 개수는 **원장에서 파생**된다 — 손으로 쓴 숫자는 반드시 낡는다."""
    from collections import Counter
    kinds = Counter(d.get("kind") or "미기재" for d in C.decisions().values())
    for k, n in kinds.items():
        assert re.search(r'data-kind="%s"[^>]*>\s*[^<]*<span class="v3-chip-n">%d</span>'
                         % (re.escape(k), n), gov_html), \
            f"종류 칩 {k}={n} 이 원장 개수와 다르다"


# ── ② 행 앵커 · 결정 ID 자동 링크 ──────────────────────────────────────────
def test_every_decision_row_has_an_anchor(gov_html):
    """결정 ID 는 repo 전체가 인용 단위로 쓴다 — 갈 곳(행 앵커)이 있어야 한다."""
    missing = [k for k in C.decisions() if f'id="{k}"' not in gov_html]
    assert not missing, f"행 앵커 없는 결정: {missing}"


def test_declink_links_only_ids_that_exist():
    """[음성] 없는 결정 ID 를 링크하면 안 된다 — 죽은 앵커는 있는 척하는 것이다."""
    known = ["D-2026-09-07-b2o3-md-closure-retrospective"]
    ok = str(A._declink("근거는 D-2026-09-07-b2o3-md-closure-retrospective 다", known))
    assert 'href="#D-2026-09-07-b2o3-md-closure-retrospective"' in ok, "있는 id 를 안 잇는다"

    bad = str(A._declink("근거는 D-2026-01-01-does-not-exist 다", known))
    assert "href=" not in bad, "원장에 없는 id 를 링크했다 (죽은 앵커)"
    assert "D-2026-01-01-does-not-exist" in bad, "모르는 id 는 글자 그대로 남아야 한다"

    # 자기 행에서 자기 자신으로 가는 링크는 만들지 않는다
    self_ = str(A._declink("D-2026-09-07-b2o3-md-closure-retrospective",
                           known, skip=known[0]))
    assert "href=" not in self_, "자기 자신을 링크했다"

    # [음성] 이스케이프를 우회하면 안 된다
    inj = str(A._declink("<script>alert(1)</script>", known))
    assert "<script>" not in inj, "declink 가 raw HTML 을 통과시켰다"


def test_decision_cross_references_are_walkable(gov_html):
    """양성: 결정끼리의 참조가 화면에서 실제로 링크로 나온다."""
    ids = set(C.decisions())
    refs = [(d["id"], r) for d in C.decisions().values()
            for fld in ("statement", "reopen_criteria")
            for r in re.findall(r"D-\d{4}-\d{2}-\d{2}-[A-Za-z0-9_-]+",
                                str(d.get(fld) or ""))
            if r in ids and r != d["id"]]
    if not refs:
        pytest.skip("원장에 결정 간 상호참조가 없다 (생기면 이 시험이 켜진다)")
    for src, ref in refs:
        assert f'href="#{ref}"' in gov_html, f"{src} 의 {ref} 참조가 링크가 아니다"


# ── ③ kb 마크다운 읽기 ─────────────────────────────────────────────────────
def test_safe_kb_doc_rejects_escape_and_nonmarkdown():
    """[음성] 화이트리스트가 실제로 막는가 — 통과 경로만 있는 검사는 아무것도 보증 못 한다."""
    assert D.safe_kb_doc("kb/open_items.md") is not None, "전제: 실물 kb md 가 열린다"
    for bad in ("kb/../webapp/app.py",          # 경로 탈출
                "../kb/open_items.md",          # 뿌리 밖에서 진입
                "kb/open_items.txt",            # md 가 아니다
                "docs/README.md",               # kb 밖
                "tools/kb_wiki.py",             # 코드
                "kb/does-not-exist.md",         # 없는 파일
                "kb", "", None):
        assert D.safe_kb_doc(bad) is None, f"⛔ 막았어야 할 경로가 통과했다: {bad!r}"


def test_kb_route_renders_and_refuses():
    A.app.config["TESTING"] = True
    c = A.app.test_client()
    assert c.get("/kb?path=kb/open_items.md").status_code == 200
    for bad in ("kb/../webapp/app.py", "docs/README.md", "kb/nope.md", "tools/x.py"):
        assert c.get("/kb?path=" + bad).status_code == 404, f"열리면 안 되는 경로: {bad}"


def test_kb_index_lists_only_ledger_referenced_docs():
    """/kb 는 kb **색인이 아니다** — 원장이 이름 댄 근거 문서만 편다."""
    A.app.config["TESTING"] = True
    h = A.app.test_client().get("/kb").get_data(as_text=True)
    refs = {str(r or "").partition("#")[0]
            for d in C.decisions().values() for r in (d.get("record"), d.get("card"))
            if str(r or "").startswith("kb/")}
    assert refs, "전제: 원장이 kb 문서를 근거로 든다"
    for r in refs:
        assert r in h, f"원장이 이름 댄 {r} 이 목록에 없다"
    # [음성] 원장이 안 가리킨 kb 문서를 목록에 세우면 안 된다
    assert "kb/open_items.md" not in refs, "전제가 바뀌었다 — 다른 비참조 문서를 골라라"
    assert "kb/open_items.md" not in h, "원장이 이름 대지 않은 문서가 목록에 있다"


def test_governance_evidence_links_reach_kb(gov_html):
    """결정의 kb 근거가 **링크**여야 한다 (종전에는 회색 문자열로 끝났다)."""
    kb_refs = {str(r or "").partition("#")[0]
               for d in C.decisions().values() for r in (d.get("record"), d.get("card"))
               if str(r or "").startswith("kb/")}
    assert kb_refs, "전제: kb 근거가 원장에 있다"
    for r in sorted(kb_refs):
        if D.safe_kb_doc(r) is None:
            continue                      # 실물이 없는 것은 링크하지 않는 게 맞다
        assert f'href="/kb?path={r}"' in gov_html, f"{r} 이 아직 죽은 문자열이다"


def test_kb_read_route_is_not_a_download_gate():
    """[음성] kb 읽기 라우트가 `/api/file` 허용 뿌리를 넓히면 안 된다."""
    assert D.safe_repo_path("kb/open_items.md") is None, \
        "⛔ safe_repo_path 가 kb 를 삼켰다 — 다운로드 게이트와 읽기 게이트는 분리다"
    A.app.config["TESTING"] = True
    assert A.app.test_client().get("/api/file/kb/open_items.md").status_code == 404


# ── ④ correction 레코드 ────────────────────────────────────────────────────
def _corrections():
    return [a for a in C.assessments().values() if a.get("kind") == "correction"]


def test_correction_records_are_not_blank_rows(gov_html):
    """정정 레코드의 본문이 화면에 있어야 한다.

    종전 템플릿은 `gate`/`result`/`reason` 만 읽어서, correction 레코드가
    "대상 | – | – | (빈칸)" 으로 그려졌다. 원장 자신의 _rules 는 "★ 정정도 산출물이다"
    라고 못 박는데 화면에서는 그 산출물이 빈 줄이었다.
    """
    import html as _h
    corr = _corrections()
    assert corr, "전제: correction 레코드가 원장에 있다"
    gov_html = _h.unescape(gov_html)      # 따옴표 등이 엔티티로 나가므로 풀고 본다
    for a in corr:
        assert "✎ 정정" in gov_html, "정정 판정 표시가 없다"
        for fld in ("what_was_wrong", "scope", "second_error_corrected",
                    "third_error_corrected"):
            v = a.get(fld)
            if not v:
                continue
            # `|bold` 가 ** 를 <b> 로 바꾸므로 **첫 별표 앞** 조각으로 찾는다
            frag = str(v).split("**")[0].strip()[:30]
            if len(frag) < 8:
                continue
            assert frag in gov_html, f"{a['assessment_id']} 의 {fld} 가 화면에 없다"
        for e in (a.get("evidence") or []):
            assert str(e)[:30] in gov_html, "정정 근거가 화면에 없다"
        assert a["assessment_id"] in gov_html, "레코드 ID 가 화면에 없다"


def test_correction_branch_survives_missing_fields():
    """[음성] 필드가 빠진 정정 레코드에도 `None` 을 찍거나 죽으면 안 된다."""
    real = C.assessments()
    fake = dict(real)
    fake["A-TEST-empty-correction"] = {
        "assessment_id": "A-TEST-empty-correction", "kind": "correction",
        "claim_ref": "value:MD_Ea_eV/b2o3", "state": "active",
    }
    orig = C.assessments
    try:
        C.assessments = lambda *a, **k: fake     # noqa: E731
        A.app.config["TESTING"] = True
        r = A.app.test_client().get("/governance")
        assert r.status_code == 200, "빈 정정 레코드 하나로 화면이 죽었다"
        h = r.get_data(as_text=True)
        assert "A-TEST-empty-correction" in h, "레코드가 화면에서 조용히 사라졌다"
        assert ">None<" not in h, "빈 칸에 None 을 찍는다"
    finally:
        C.assessments = orig


# ── ⑤ 초록 배너의 검사 범위 · 실제 위험 카운터 ──────────────────────────────
def test_green_banner_states_its_scope(gov_html):
    """[음성] 초록 도장이 **페이지 전체 건강 신호**로 읽히면 안 된다.

    검사 함수 자신의 docstring 이 범위를 좁혀 놓았는데(canonical.py: "판정의 과학적
    타당성은 안 본다") 화면이 그 한정을 안 옮겼다. 바로 아래에 유실·BLOCKED 가 이어진다.
    """
    if "원장 검증 실패" in gov_html:
        pytest.skip("지금 원장에 구조 위반이 있어 초록 배너가 안 뜬다")
    assert "값·판정의 타당성은 검사하지 않는다" in gov_html, "검사 범위가 화면에 없다"
    assert "그래프·어휘만 본다" in gov_html


def test_risk_counters_come_from_the_ledgers(gov_html):
    """위험 카운터는 원장 파생이다 — 손으로 쓴 숫자는 반드시 낡는다."""
    haz = D.citation_hazards().get("hazards", [])
    n_blocked = sum(1 for h in haz if h.get("level") == "BLOCKED")
    n_lost = sum(1 for a in C.artifacts().values() if a.get("status") == "lost")
    assert f"인용 금지(BLOCKED) {n_blocked}건" in gov_html
    assert f"되돌릴 수 없는 유실 {n_lost}건" in gov_html
    # 원장 _rules: ratification 없이 active 가 될 수 없다 → 0 이 정상이고, 0 이 아니면 표시된다
    bad = [d["id"] for d in C.decisions().values()
           if C.decision_state(d) == "active"
           and (d.get("ratification") or {}).get("state") != "ratified"]
    assert f"비준 없는 active {len(bad)}건" in gov_html
    for did in bad:
        assert did in gov_html, f"비준 없는 active {did} 를 화면이 이름 대지 않는다"


# ── ⑥ 인용위험 '결속됨 / 산문' ─────────────────────────────────────────────
def test_hazard_binding_badge_matches_the_two_functions(gov_html):
    """화면의 결속 배지가 `hazard_ids()` 와 `hazard_claims()` 의 **차이**를 말한다."""
    vocab = C.hazard_ids()
    req = {c["id"] for c in C.hazard_claims()}
    assert vocab, "전제: 위험 어휘가 있다"
    assert req <= vocab, "결속 요구가 어휘보다 넓다 — 유령 결속이다"
    assert f"결속 어휘 {len(vocab)}개" in gov_html
    assert f"살아있는 결속 요구 {len(req)}건" in gov_html

    rows = D.citation_hazards().get("hazards", [])
    # ⛔ BI-3 P0-1: level 이 아니라 **금지 상태**로 센다. SUPERSEDED 라도 금지는 살아 있다.
    inactive = [h for h in rows if h.get("id") and not C.prohibition_active(h)]
    assert len(vocab) - len(req) == len(inactive), (
        "어휘와 결속 요구의 차이가 **금지 해제** 건수와 안 맞는다")
    assert f"결속 해제 {len(inactive)}" in gov_html


def test_hazard_rows_are_not_all_drawn_the_same(gov_html):
    """[음성] 29행을 **똑같이** 그리면 안 된다 — 결속된 행과 산문 행이 구분돼야 한다."""
    rows = D.citation_hazards().get("hazards", [])
    assert len(rows) > 5, "전제: 위험 원장이 여러 행이다"
    bound = [h for h in rows
             if h.get("id") and C.prohibition_active(h)
             and (h.get("claim") or h.get("forbidden_phrases"))]
    prose = [h for h in rows
             if h.get("id") and C.prohibition_active(h)
             and not (h.get("claim") or h.get("forbidden_phrases"))]
    assert bound and prose, "전제: 결속된 행과 산문 행이 둘 다 있다"
    assert "🔗 결속됨" in gov_html, "결속된 행 표시가 없다"
    assert "✎ 이름만(산문)" in gov_html, "산문 행 표시가 없다"
    # binding_scope 는 원장 선언을 옮길 뿐 — 화면이 지어내지 않는다
    for h in rows:
        if h.get("binding_scope"):
            assert h["binding_scope"] in gov_html


def test_hazard_row_without_id_is_marked_as_unbindable():
    """[음성] id 없는 위험 행을 결속된 것처럼 그리면 안 된다."""
    orig = D.citation_hazards
    fake = {"updated": "2026-01-01",
            "hazards": [{"level": "BLOCKED", "file": "db/properties/x.json",
                         "what": "테스트", "why": "테스트", "fix": "테스트"}]}
    try:
        D.citation_hazards = lambda *a, **k: fake        # noqa: E731
        A.app.config["TESTING"] = True
        h = A.app.test_client().get("/governance").get_data(as_text=True)
        assert "⛔ id 없음" in h, "id 없는 행을 결속 대상처럼 그린다"
        assert "🔗 결속됨" not in h, "결속되지 않은 행에 결속 배지가 붙었다"
    finally:
        D.citation_hazards = orig


# ── /ledger — '오늘' 이 언제인지 화면이 말한다 ─────────────────────────────
def test_ledger_says_how_old_it_is():
    """화면의 '오늘/내일' 은 **원장 날짜** 기준이다 — 간격을 계산해서 박는다."""
    A.app.config["TESTING"] = True
    r = A.app.test_client().get("/ledger")
    assert r.status_code == 200
    h = r.get_data(as_text=True)
    leds = [x for x in D.load_tq_ledger() if not x.get("_error")]
    if not leds:
        pytest.skip("원장 파일이 없다")
    from datetime import date
    y, m, dd = (int(x) for x in str(leds[0]["date"]).split("-")[:3])
    age = (date.today() - date(y, m, dd)).days
    if age > 0:
        assert f"{age}일 전 원장" in h, "원장 나이를 화면이 말하지 않는다"
        assert f"'오늘' 은 {leds[0]['date']}" in h
    else:
        assert "오늘 원장" in h


def test_ledger_closed_rows_are_not_value_pending():
    """[음성] 끝난 행(✅·⛔)에 '내일 채워진다' 배지를 붙이면 안 된다."""
    A.app.config["TESTING"] = True
    h = A.app.test_client().get("/ledger").get_data(as_text=True)
    leds = [x for x in D.load_tq_ledger() if not x.get("_error")]
    if not leds:
        pytest.skip("원장 파일이 없다")
    closed_pending = [t for t in (leds[0].get("T") or [])
                      if str(t.get("상태") or "")[:1] in ("✅", "⛔")
                      and str(t.get("오늘") or "").strip() in ("", "-")]
    if not closed_pending:
        pytest.skip("종료·미기입 행이 원장에 없다 (생기면 이 시험이 켜진다)")
    assert "– 해당 없음(종료)" in h, "종료 행 표시가 없다"
    # 요약 타일의 '값 대기' 수에서도 빠져야 한다
    live = [t for t in (leds[0].get("T") or [])
            if str(t.get("오늘") or "").strip() in ("", "-")
            and str(t.get("상태") or "")[:1] not in ("✅", "⛔")]
    assert re.search(r'<div class="st-v">%d</div>\s*<div class="st-l">.{0,40}값 대기'
                     % len(live), h, re.S), "값 대기 타일이 종료 행을 아직 세고 있다"


# ── 규율 유지 확인 (문구를 다듬으려면 시험을 같은 커밋에서 옮긴다) ──────────
def test_five_literal_phrases_survive(gov_html):
    """시험이 **글자 그대로** 집는 문구 다섯이 재편 뒤에도 살아 있다."""
    for s in ("🔒 일치", "◻ 미평가", "미평가는 실패가 아니다", "철회된 옛 판정"):
        assert s in gov_html, f"문구가 사라졌다: {s}"
    assert "본문이 승인 뒤 바뀌었다" in A.app.jinja_env.loader.get_source(
        A.app.jinja_env, "governance.html")[0], "불일치 분기가 템플릿에서 사라졌다"
