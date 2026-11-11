# -*- coding: utf-8 -*-
"""v3 묶음 F — 마크다운 렌더 + 문서·용어 표면.

이 파일이 지키는 것 (전부 **음성 경로를 같이** 시험한다 — 양성만 있는 시험은
통과해도 아무것도 보증하지 못한다):
  · `_mdlite` 가 결속(`_bind_claims`)을 탄다        ← P0-4
  · `_mdlite(0)` 이 빈 문자열이 아니다              ← 실측 0 이 결측으로 보이던 버그
  · 이탤릭이 **단어경계를 요구**한다                 ← `D*(design) / D*(host)` 충돌
  · 볼드 가드 3개(globstar 사고)가 살아 있다
  · kb frontmatter 가 본문으로 안 샌다              ← P0-34
  · heading id 가 **한글을 보존**한다                ← 죽은 §딥링크
  · `data.md_to_html`(/seminar)도 결속을 탄다

⛔ 이 파일이 **못 하는 것**: 브라우저를 안 띄운다. 스크롤·목차 클릭·검색 하이라이트
   같은 JS 동작은 문자열 존재로만 확인한다 — 실동작은 확인 못 했다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as A          # noqa: E402
import canonical as C    # noqa: E402
import data as D         # noqa: E402
import glossary as G     # noqa: E402


def _client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


def _retracted():
    """결속 대상 하나 (철회 · 텍스트 있는 것). 없으면 이 시험 전체가 무의미하다."""
    return next(x for x in C.all_claims() if x["state"] == "retracted" and x["text"])


# ── _mdlite ────────────────────────────────────────────────────────────────
def test_mdlite_binds_claims_and_can_fail():
    """⛔음성 포함: 카드 본문 경로(`_mdlite`)가 철회값을 **이름으로** 감싼다.

    종전 `_mdlite` 는 escape→bold→mark→표→<br> 만 하고 결속을 안 붙였다. 템플릿 8개
    73곳이 그 경로인데 그때 unbound 가 0 이었던 건 그 73곳에 결속 대상 문자열이
    **없어서**였다 — 검사가 초록인 이유가 "지켜서" 가 아니라 "안 마주쳐서" 였다.
    """
    t = _retracted()
    out = str(A._mdlite("옛 값 %s eV 를 인용한 문장." % t["text"]))
    assert 'data-claim="%s"' % t["id"] in out, "mdlite 가 결속을 안 붙였다: " + out[:200]
    assert not C.scan_claim_bindings(out, C.all_claims())["unbound"], out[:300]
    # ⛔음성 — 같은 문장을 결속 없이 그리면 스캐너가 **반드시** 잡아야 한다.
    naked = "<p>옛 값 %s eV 를 인용한 문장.</p>" % t["text"]
    assert C.scan_claim_bindings(naked, C.all_claims())["unbound"], \
        "표시 없이도 통과한다 — 검사가 죽었다"


def test_mdlite_zero_is_rendered_not_swallowed():
    """⛔음성 포함: 실측 0 이 화면에서 **사라지면 결측으로 읽힌다.**

    종전 `text or ""` 는 0 · 0.0 · False 를 전부 빈 문자열로 만들었다. '0 이라고 쟀다'
    와 '안 쟀다' 는 이 repo 에서 전혀 다른 판정이라(TODO / N-A / 비인용 3구분) 같은
    화면 표시를 주면 안 된다.
    """
    assert str(A._mdlite(0)) == "0"
    assert str(A._mdlite(0.0)) == "0.0"
    assert str(A._mdlite("")) == ""
    assert str(A._mdlite(None)) == "", "None 만 빈 문자열이어야 한다"


def test_mdlite_italic_requires_word_boundary():
    """⛔음성 픽스처: `D*(design) / D*(host)` — 실측 유일 충돌.

    단어경계를 안 걸면 두 별표가 짝지어져 `(design) / D` 가 통째로 기울어진다.
    """
    bad = "표기 규약: D*(design) / D*(host) 는 서로 다른 양이다"
    out = str(A._mdlite(bad))
    assert "<em>" not in out, "단어경계 없는 이탤릭이 별표를 훔쳤다: " + out
    assert "D*(design)" in out and "D*(host)" in out
    # 양성 — 진짜 이탤릭은 살아야 한다
    assert "<em>강조</em>" in str(A._mdlite("이건 *강조* 다"))
    # 곱셈·각주도 기울이지 않는다
    assert "<em>" not in str(A._mdlite("2*3*4 = 24"))


def test_mdlite_strikethrough_after_code_span_isolation():
    """취소선은 **코드 스팬 격리 뒤**다 — 백틱 안 물결은 데이터다."""
    # 결속 대상이 아닌 문자열을 쓴다 (결속 span 이 끼면 정확 일치가 깨진다)
    assert "<s>옛 문구</s>" in str(A._mdlite("~~옛 문구~~ 는 폐기"))
    out = str(A._mdlite("`~~a~~` 는 리터럴"))
    assert "<s>" not in out, "코드 스팬 안 물결을 취소선으로 먹었다: " + out
    assert "~~a~~" in out


def test_mdlite_bold_guards_still_hold():
    """⛔음성: globstar 사고 재현 — 데이터 별표가 300자 뒤 짝을 훔치면 안 된다."""
    s = "globstar(**) 지원 " + "가" * 60 + " **진짜 강조** 끝"
    out = str(A._mdlite(s))
    assert "globstar(**)" in out, "여는 별표 뒤 닫는 문장부호 가드가 죽었다: " + out[:200]
    assert "<strong>진짜 강조</strong>" in out
    # 300자 상한 — 멀리 떨어진 짝은 포기한다
    far = "**열고 " + "나" * 400 + " 닫고**"
    assert "<strong>" not in str(A._mdlite(far))


def test_mdlite_escapes_before_anything_else():
    """XSS 규율 — 강조를 붙이기 전에 escape 가 먼저다."""
    out = str(A._mdlite("<script>alert(1)</script> **굵게**"))
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


# ── frontmatter (P0-34) ────────────────────────────────────────────────────
_FM_KEYS = ("verifiedBy", "evidenceScope", "authoredBy", "claimType")


def test_frontmatter_is_stripped_from_body():
    """kb_wiki 규약을 지킨 문서일수록 화면이 깨지던 자리."""
    c = _client()
    for url in ("/sdcp/self-doping", "/concept/msd_reading",
                "/concept/sdcp_self_doping_explainer_2026_08_26"):
        h = c.get(url).get_data(as_text=True)
        for k in _FM_KEYS:
            assert k not in h, f"{url} 에 frontmatter `{k}` 가 본문으로 샜다"


def test_frontmatter_is_promoted_to_badges_and_not_invented():
    """뗀 것을 **버리지 않는다.** 그리고 **없는 것을 채우지도 않는다.**"""
    md = (D.CONCEPTS / "msd_reading.md").read_text(encoding="utf-8")
    meta, body = A.split_frontmatter(md)
    assert meta.get("updated"), "frontmatter 를 못 읽었다 (전제 붕괴)"
    assert not body.lstrip().startswith("---")
    labs = dict(A.doc_badges(meta))
    assert labs.get("갱신") == meta["updated"]
    # ⛔음성 ① frontmatter 가 없으면 배지도 없다 (오늘 날짜로 안 메운다)
    assert A.doc_badges(A.split_frontmatter("# 제목만 있는 문서")[0]) == []
    # ⛔음성 ② 갱신일 없는 frontmatter 는 '미기재'(None) 로 남는다
    only = A.split_frontmatter("---\nstatus: 초안\n---\n본문")[0]
    assert ("갱신", None) in A.doc_badges(only), A.doc_badges(only)


def test_frontmatter_split_never_eats_body():
    """⛔음성: 문서 중간의 `---` 수평선을 frontmatter 로 오인하면 본문이 날아간다."""
    src = "# 제목\n\n첫 문단\n\n---\n\n둘째 문단"
    meta, body = A.split_frontmatter(src)
    assert meta == {} and body == src, (meta, body[:40])
    # 리스트·중첩 줄은 값으로 안 읽는다 (YAML 파서가 아니다 — 그렇다고 오독하지도 않는다)
    meta2, _ = A.split_frontmatter('---\ntags: [a, b]\n  nested: x\n- item\nstatus: ok\n---\nx')
    assert meta2["status"] == "ok" and "nested" not in meta2, meta2


# ── heading slug (죽은 §딥링크) ────────────────────────────────────────────
def test_heading_ids_keep_korean():
    """python-markdown 기본 slugify 는 한글을 통째로 버려 id 가 빈다."""
    html = A.doc_html("## 12. 활성화 에너지는 방법마다 다른 양이다\n\n본문")
    ids = re.findall(r'<h2 id="([^"]+)"', html)
    assert ids, "heading 에 id 가 없다: " + html[:200]
    assert "활성화" in ids[0], ids
    # ⛔음성 — 위치 기반 id(`h0`)로 되돌아가면 절이 하나만 늘어도 딥링크가 어긋난다
    assert ids[0] not in ("h0", "0", ""), ids
    # md_html(toc) 경로도 같은 규칙
    ids2 = re.findall(r'<h2 id="([^"]+)"',
                      A.md_html("## 한글 제목\n\n본문", ("tables", "fenced_code", "toc")))
    assert ids2 and "한글" in ids2[0], ids2


def test_concept_page_carries_server_heading_ids():
    h = _client().get("/concept/dft").get_data(as_text=True)
    ids = re.findall(r'<h2 id="([^"]+)"', h)
    assert any(i.startswith("12-") for i in ids), ids[:10]


# ── /seminar 결속 (md_to_html) ─────────────────────────────────────────────
def test_seminar_markdown_path_binds_claims():
    """⛔음성 포함: 렌더러는 둘이어도 **판정기는 하나**여야 한다."""
    t = _retracted()
    out = D.md_to_html("옛 값 %s eV 를 인용한 문장." % t["text"])
    assert 'data-claim="%s"' % t["id"] in out, "seminar 경로가 결속 밖이다: " + out[:200]
    assert not C.scan_claim_bindings(out, C.all_claims())["unbound"]
    assert C.scan_claim_bindings("<p>옛 값 %s eV.</p>" % t["text"],
                                 C.all_claims())["unbound"], "검사가 죽었다"


# ── 용어집: 연구 규율 5장 ──────────────────────────────────────────────────
_DISCIPLINE = ("estimand", "closure_criteria", "control_job", "claim_ceiling", "prereg_seal")


def test_governance_vocabulary_cards_render():
    """이 repo 에서 제일 자주 쓰는 말인데 정의가 0건이던 자리."""
    assert "연구 규율" in G.CATS_G, "카테고리가 CATS_G 에 없으면 카드가 통째로 사라진다"
    ids = {g["id"] for g in G.GLOSSARY}
    assert set(_DISCIPLINE) <= ids, set(_DISCIPLINE) - ids
    h = _client().get("/glossary").get_data(as_text=True)
    for gid in _DISCIPLINE:
        assert 'id="%s"' % gid in h, f"{gid} 카드가 화면에 없다"
    # 부르는 이름은 한국어로 (2026-09-01 용어 규율). 영문은 병기만.
    for word in ("보고량", "닫힘 조건", "대조 잡", "허용 서술 범위", "사전등록"):
        assert word in h, word
    # 실제 사례 링크 — 카드가 개념만 말하고 끝나면 '우리 계산' 칸이 아니다
    for href in ("/files?q=estimand_card", "/files?q=sdcp_neutral_closed",
                 "/files?q=cascade_seal_v2", "/governance"):
        assert href in h, href


def test_governance_cards_keep_machine_field_names_intact():
    """⛔ 부르는 이름만 한국어다 — 기계 필드명·파일명을 개서하면 원장이 끊긴다."""
    h = _client().get("/glossary").get_data(as_text=True)
    assert "estimand_card.md" in h
    assert "kind: estimand" in h or "kind: estimand" in h.replace("&quot;", '"')
    # ⛔음성 — 기계 이름을 한국어로 갈아치웠으면 걸린다
    assert "보고량_카드.md" not in h and "kind: 보고량" not in h


def test_glossary_cards_have_anchor_ids():
    """홈 부제가 이미 /glossary#beta-gate 로 보내는데 카드 id 가 0개였다."""
    h = _client().get("/glossary").get_data(as_text=True)
    for g in G.GLOSSARY:
        assert 'id="%s"' % g["id"] in h, g["id"]
    # ⛔음성 — 없는 용어의 id 가 있으면 그건 다른 요소를 잘못 집은 것이다
    assert 'id="이런-용어는-없다"' not in h


def test_glossary_search_index_includes_ours_and_how():
    """색인이 what 만 담으면 **철회를 확인하러 온 검색어**가 다 빠진다."""
    h = _client().get("/glossary").get_data(as_text=True)
    idx = re.findall(r'data-t="(.*?)"', h, re.S)
    assert len(idx) == len(G.GLOSSARY), (len(idx), len(G.GLOSSARY))
    for q, floor in (("b2o3", 5), ("철회", 4)):
        n = sum(1 for m in idx if q in m.lower())
        assert n >= floor, f"{q}: {n} 장만 걸린다 — 색인이 'ours' 를 안 담았다"
    # ⛔음성 — 실제로 어느 카드에도 없는 말은 걸리지 않아야 한다 (색인이 다 삼키면 무의미)
    assert sum(1 for m in idx if "존재하지않는용어xyz" in m) == 0


# ── 문서 화면 ──────────────────────────────────────────────────────────────
def test_doc_pages_render_with_toc_and_search():
    c = _client()
    for url in ("/methods", "/sdcp", "/sdcp/self-doping", "/todo"):   # doc.html 을 쓰는 라우트만
        r = c.get(url)
        assert r.status_code == 200, (url, r.status_code)
        h = r.get_data(as_text=True)
        assert 'id="doctoc"' in h and 'id="docq"' in h, url


def test_concept_h1_is_not_a_slug_when_frontmatter_has_a_title():
    """용어집에 안 걸린 문서 4개가 `msd_reading` 같은 슬러그 제목을 달고 있었다."""
    h = _client().get("/concept/msd_reading").get_data(as_text=True)
    h1 = re.search(r"<h1>(.*?)</h1>", h, re.S).group(1)
    assert h1.strip() != "msd_reading", h1
    assert "MSD" in h1, h1
    # ⛔음성 — frontmatter title 도 GLOSSARY 항목도 없으면 슬러그로 떨어지는 게 맞다
    assert (A.split_frontmatter("본문뿐")[0].get("title") or "cid") == "cid"


# ── kb 문서 접기 (2026-11-11 · 사용자 '미결 리스트 · 원장이 사람이 읽을 수 있게') ─────────────
#   md_html 은 raw HTML 을 끈다. 우리 kb 문서 (origin internal) 의 줄 단위 `<details><summary>…</summary>` ·
#   `</details>` 두 꼴만 접기로 살리고, 줄머리 HTML 주석은 뺀다. 판정기는 `D.md_fold_lines` 하나다.
_FOLD_MD = ("# 제목\n\n<!-- 갱신 규칙: 사람에게 안 보일 메모 -->\n\n"
            "<details><summary>지난 기록 (3 항목)</summary>\n\n- 가\n- 나\n\n</details>\n\n끝 문단\n")


def test_md_fold_renders_details_for_internal_docs():
    """양성: 줄 단위 접기 → `<details class="md-fold">` · 안의 목록은 접기 **안** · 뒤 문단은 접기 **밖**."""
    h = A.md_html(_FOLD_MD)
    assert '<details class="md-fold"><summary>지난 기록 (3 항목)</summary>' in h
    inner = h.split('<details class="md-fold">', 1)[1].split("</details>", 1)[0]
    assert "<li>가</li>" in inner and "<li>나</li>" in inner, "목록이 접기 밖으로 샜다"
    assert "끝 문단" in h.split("</details>", 1)[1], "접기 뒤 본문이 접기 안으로 삼켜졌다"
    assert "갱신 규칙" not in h and "&lt;!--" not in h, "줄머리 주석이 화면에 나왔다"
    assert "&lt;details" not in h, "접기 태그가 글자로 샜다"


def test_md_fold_is_not_applied_to_external_docs():
    """⛔음성: 남의 문서 (litdb · origin external) 에는 접기도 주석 빼기도 안 건다 — 글자로 남는다."""
    h = A.md_html(_FOLD_MD, origin="external")
    assert "<details" not in h, "외부 문서의 HTML 태그를 살렸다"
    assert "&lt;details&gt;" in h and "&lt;!--" in h, "외부 문서의 원문이 사라졌다"


def test_md_fold_leaves_code_fences_and_mid_line_tags_alone():
    """⛔음성: 코드 펜스 안의 접기 줄 · 앞에 글이 있는 태그 줄은 접지 않는다."""
    md = ("```\n<details><summary>코드 안</summary>\n</details>\n```\n\n"
          "메모 <details><summary>앞에 글</summary>\n\n본문\n")
    h = A.md_html(md)
    assert 'class="md-fold"' not in h, "코드 펜스나 줄 중간 태그를 접기로 읽었다"
    assert "&lt;summary&gt;코드 안&lt;/summary&gt;" in h, "코드 펜스 안 글이 바뀌었다"
    kinds = [k for _l, k, _d, _s in D.md_fold_lines(md)]
    assert "open" not in kinds and kinds[:4] == ["fence"] * 4


def test_md_fold_unclosed_is_closed_and_summary_is_escaped():
    """⛔음성: 안 닫은 접기는 끝에서 닫는다 (짝이 맞는다) · 요약글의 태그는 글자로 나간다 (주입 안 됨)."""
    h = A.md_html("<details><summary><img src=x onerror=alert(1)> 요약</summary>\n\n본문 하나\n")
    assert h.count("<details") == h.count("</details>") == 1, "접기 태그 짝이 안 맞는다"
    assert "<img" not in h and "&lt;img src=x" in h, "요약글의 HTML 이 살아났다"
    # 짝 없는 `</details>` 는 접기가 아니다 — 글자로 남는다
    h2 = A.md_html("본문\n\n</details>\n")
    assert "</details>" not in h2 and "&lt;/details&gt;" in h2


def test_todo_page_folds_every_ledger_fold():
    """양성: /todo 는 원장의 접기 줄 수만큼 접기를 그린다 · 접기 태그가 글자로 새지 않는다."""
    md = D.load_open_items_md()
    n = sum(1 for _l, k, _d, _s in D.md_fold_lines(md) if k == "open")
    assert n >= 2, "전제: 미결 리스트에 접어 둔 기록이 있다 (없으면 이 시험이 헛것을 잰다)"
    h = _client().get("/todo").get_data(as_text=True)
    assert h.count('<details class="md-fold">') == n
    assert "&lt;details&gt;" not in h and "&lt;!--" not in h
