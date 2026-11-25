"""v3 묶음 I — 문헌 화면 (/literature · /paper/<slug> · litdb 문서).

무엇을 지키는 시험인가
  ① 기본 정렬이 digest 등록일 최신순이고, **날짜 없는 digest 가 사라지지 않는다**
  ② 인용 제한 스캔이 "인용 금지 **해제**" 를 세지 않는다 (음성 경로)
  ③ 뼈대(문서 대기)가 헤드라인 카운트에 안 들어가고 배지가 붙는다
  ④ 캡션 색인이 DOM 에서 빠지고 /api/lit-index 로 옮겨졌다 (음성 경로 포함)
  ⑤ 발표덱이 논문 위로 올라가되 **인용등급 경고가 같이 움직였다**
  ⑥ /paper/<slug> 가 열리고 `_` 접두는 404
  ⑦ litdb 의 죽은 경로(our_dem_baseline · properties/)가 정리됐다

⛔ 이 시험이 못 하는 것
  · 브라우저를 안 띄운다 — 서버 렌더 HTML 문자열만 본다. JS(정렬 토글·색인 지연로딩·
    뼈대 자동 펼침)의 실동작은 여기서 보증되지 않는다.
  · digest 내용의 참·거짓을 판정하지 않는다. 인용 제한 배지는 산문 스캔이라는
    사실만 확인하고, 그 판정이 맞는지는 묻지 않는다.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as A          # noqa: E402
import data as D         # noqa: E402


@pytest.fixture(scope="module")
def client():
    return A.app.test_client()


@pytest.fixture(scope="module")
def lit_html(client):
    r = client.get("/literature")
    assert r.status_code == 200
    return r.data.decode()


# ── ① 정렬 ────────────────────────────────────────────────────────────────
def test_default_sort_is_digest_desc():
    """양성: 서버가 주는 기본 순서가 digest 등록일 내림차순이다."""
    ps = D.list_papers()
    dates = [p["digested"] or "" for p in ps]
    assert dates == sorted(dates, reverse=True), "기본 정렬이 날짜 내림차순이 아니다"
    assert ps[0]["digested"], "맨 앞이 날짜 없는 digest 면 정렬이 뒤집힌 것이다"


def test_undated_digests_survive_sorting():
    """음성: 날짜가 없는 digest 를 정렬이 **떨어뜨리면** 실패.

    실측 2편(bzox… · hollmann2025…)이 이 경로로 조용히 사라진 적이 있다.
    """
    ps = D.list_papers()
    undated = [p["id"] for p in ps if not p["digested"]]
    assert undated, "날짜 없는 digest 가 하나도 없다 — 픽스처 전제가 바뀌었으면 이 시험을 고친다"
    # 목록에 남아 있고, 맨 뒤로만 밀린다
    tail = [p["id"] for p in ps[-len(undated):]]
    assert set(undated) == set(tail)


# ── ② 인용 제한 스캔 (음성 경로가 핵심) ────────────────────────────────────
def test_ban_scan_positive():
    n = D.paper_notice("ahn2026_cej_agno3_pvp_li3n_anodefree")
    assert n["ban_n"] >= 1
    assert "인용 금지" in n["ban"]


def test_ban_scan_ignores_lifted_bans():
    """음성: "인용 금지 **해제**" 를 제한으로 세면 실패.

    anderson2024 는 본문에 `인용 금지` 가 여러 번 나오지만 그중 일부는
    "§19.5의 4칸 미해결이 §20에서 전부 확정됐다 — 인용 금지 해제." 다.
    문자열만 세면 해제된 것을 제한으로 광고한다.
    """
    slug = "anderson2024_llzo_comprehensive_dopant_screening"
    raw = (D.LITDB / "papers" / f"{slug}.md").read_text(encoding="utf-8")
    n_raw = len([ln for ln in raw.splitlines() if re.search(r"인용\s*금지", ln)])
    n_lift = len([ln for ln in raw.splitlines()
                  if re.search(r"인용\s*금지\s*(해제|아님|아니)", ln)])
    assert n_lift > 0, "픽스처 전제(해제 문구가 있다)가 깨졌다"
    assert D.paper_notice(slug)["ban_n"] == n_raw - n_lift


def test_ban_absent_is_not_a_clearance(lit_html):
    """음성: 제한 배지가 **없는** 논문이 '인용 가능' 으로 읽히면 안 된다 —
    화면이 그 문장을 실제로 달고 있는지 본다(문구가 사라지면 실패)."""
    assert "배지가 없다고 인용 가능이라는 뜻이 아니" in lit_html
    assert "원장 판정이 아니" in lit_html


# ── ③ 뼈대 ────────────────────────────────────────────────────────────────
def test_skeleton_flagged():
    ps = D.list_papers()
    sk = [p["id"] for p in ps if p["skeleton"]]
    assert sk, "뼈대 카드가 하나도 안 잡힌다"
    for s in sk:
        head = (D.LITDB / "papers" / f"{s}.md").read_text(encoding="utf-8")
        assert "⏳ 문서 대기" in head or "🌱 skeleton" in head


def test_headline_count_excludes_skeletons(lit_html):
    """양성: 헤드라인은 완성 digest 만. 음성: 그렇다고 목록에서 지우지는 않는다."""
    ps = D.list_papers()
    full = sum(1 for p in ps if not p["skeleton"])
    skel = len(ps) - full
    assert skel > 0
    assert f"완성 digest <b>{full}</b>편" in lit_html
    # 지운 게 아니라 접은 것이다 — 뼈대 카드도 DOM 에 있어야 한다
    for p in ps:
        if p["skeleton"]:
            assert f'data-id="{p["id"]}"' in lit_html


def test_skeleton_evidence_level_not_fulltext():
    """음성: PDF 미확보인 뼈대가 `evidence_level fulltext` 를 주장하면 실패.

    CLAUDE.md 충돌 규칙(fulltext > abstract > snippet > title)에서 빈 카드가
    나중에 들어올 진짜 분석을 이기는 경로다.
    """
    bad = []
    for f in sorted((D.LITDB / "papers").glob("*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        head = "\n".join(t.splitlines()[:16])
        if "⏳ 미확보" in head and re.search(r"evidence_level\s*`fulltext`", head):
            bad.append(f.stem)
    assert not bad, f"PDF 미확보인데 fulltext 로 적힌 digest: {bad}"


# ── ④ 캡션 색인 이주 ──────────────────────────────────────────────────────
def test_caption_index_not_baked_into_dom(lit_html):
    """음성: 색인이 다시 HTML 로 들어오면 실패 (899 KB → 이 경로로 돌아간다)."""
    assert "data-fig=" not in lit_html
    assert "data-cmt=" not in lit_html


def test_lit_index_api_serves_the_index(client):
    """양성: 뺀 색인을 실제로 내주는가. 안 그러면 캡션 검색이 통째로 죽는다."""
    r = client.get("/api/lit-index")
    assert r.status_code == 200
    d = r.get_json()
    assert set(d) == {"fig", "cmt"}
    assert len(d["fig"]) > 50, "캡션 색인이 비었다 — 검색이 제목만 훑게 된다"
    # 색인 값의 모양(‘<key> <캡션>’ 을 ¦ 로 이음)이 화면 파서와 맞아야 한다
    some = next(iter(d["fig"].values()))
    assert isinstance(some, str) and some == some.lower()


# ── ⑤ 발표덱 승격 + 경고 동반 ─────────────────────────────────────────────
def test_talks_above_papers_with_their_warning(lit_html):
    i_talk = lit_html.find("🎤 학회 발표자료")
    i_paper = lit_html.find("📄 논문 digest")
    assert i_talk > 0 and i_paper > 0
    assert i_talk < i_paper, "발표덱이 논문 그리드 위로 안 올라갔다"
    # ⚠⚠ 경고 callout 이 그 묶음에 **붙어서** 같이 움직였는가 (핵심)
    i_warn = lit_html.find("소환값보다 한 단계 낮은 신뢰 등급")
    assert i_talk < i_warn < i_paper, "인용등급 경고가 발표덱 묶음에서 떨어졌다"
    assert "부재의 증거가 아니" in lit_html


def test_talk_cards_have_anchor_ids(lit_html):
    """⌘K 가 거는 /literature#<id> 가 실제로 걸릴 자리가 있는가."""
    for t in D.list_talks():
        assert f'id="{t["id"]}"' in lit_html


def test_talk_tab_exists(lit_html):
    assert 'data-track="talk"' in lit_html
    assert "🎤 발표덱" in lit_html


# ── ⑥ /paper/<slug> ───────────────────────────────────────────────────────
def test_paper_fullpage_route(client):
    slug = D.list_papers()[0]["id"]
    r = client.get(f"/paper/{slug}")
    assert r.status_code == 200
    h = r.data.decode()
    assert "docbody" in h                      # doc.html 본문(목차·문서내 검색 포함)
    assert "/static/js/docnote.js" in h        # 형광펜·여백 메모 경로


def test_paper_route_rejects_underscore_and_talks(client):
    """음성: 목록에 안 나오는 것이 URL 로는 열리면 실패."""
    assert client.get("/paper/_TEMPLATE").status_code == 404
    assert client.get("/api/paper/_TEMPLATE").status_code == 404
    assert client.get("/paper/__없는논문__").status_code == 404
    # 발표덱은 /talk 가 담당한다 — /paper 로는 안 열린다(등급이 다른 문서다)
    t = D.list_talks()[0]["id"]
    assert client.get(f"/paper/{t}").status_code == 404
    assert client.get(f"/talk/{t}").status_code == 200


def test_paper_page_carries_restriction_band(client):
    """제한 문구가 있는 digest 는 정독 페이지 머리에도 그 사실이 나와야 한다."""
    slug = next(p["id"] for p in D.list_papers() if p["ban_n"])
    h = client.get(f"/paper/{slug}").data.decode()
    assert "인용 제한 문구" in h
    assert "원장 판정이 아니" in h


# ── ⑦ litdb 문서 ──────────────────────────────────────────────────────────
def test_our_dem_baseline_path_resolves():
    """DEM digest 84편이 98곳에서 가리키던 경로가 이제 존재한다."""
    p = D.LITDB / "our_dem_baseline.md"
    assert p.exists()
    t = p.read_text(encoding="utf-8")
    # 값을 지어내지 않았다는 것 자체가 이 파일의 계약이다
    assert "이 브랜치에는 아직 없다" in t or "값 0개" in t


def test_litdb_readme_has_no_dead_properties_path():
    """음성: 없는 폴더(`properties/`)를 정본처럼 가리키면 실패."""
    t = (D.LITDB / "README.md").read_text(encoding="utf-8")
    assert not (D.LITDB / "properties").exists()
    for ln in t.splitlines():
        if "properties/" in ln and "db/properties/" not in ln:
            assert "없다" in ln or "⛔" in ln, f"죽은 경로가 살아 있다: {ln}"


def test_litdb_readme_lists_both_tracks():
    t = (D.LITDB / "README.md").read_text(encoding="utf-8")
    for name in ("INDEX_DEM.md", "comparison_vs_ours_DEM.md", "talks/", "surveys/",
                 "topics.json", "_INDEX_proposals.md"):
        assert name in t, f"README 구조표에 {name} 이 없다"


def test_index_md_has_no_hardcoded_check_count():
    """음성: --check 결과 수를 문서에 박으면 실패 (세 번 낡은 자리)."""
    t = (D.LITDB / "INDEX.md").read_text(encoding="utf-8")
    head = "\n".join(t.splitlines()[:14])
    assert "기준 0편" not in head
    assert "--check" in head
