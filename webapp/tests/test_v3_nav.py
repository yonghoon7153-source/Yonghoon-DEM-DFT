#!/usr/bin/env python3
"""test_v3_nav.py — v3 묶음 A(셸·IA·온보딩)의 회귀 시험.

여기 담은 건 전부 **실제로 한 번 어긋났던 것**이다.
  · 사이드바 21줄 vs ⌘K 15줄 — 손으로 맞춘 두 목록이 갈려 6개가 검색에서 빠졌다
  · 손으로 쓴 판 번호·요약이 낡았다 (두 번)
  · 표기(배지·TODO·N/A·비인용) 어휘가 화면마다 갈렸다

⚠ 시험마다 **음성 경로**(틀린 입력을 잡아내는지)를 같이 둔다. 양성만 있는 시험은
  통과해도 아무것도 보증 못 한다.

    pytest webapp/tests/test_v3_nav.py -q
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A       # noqa: E402
import data as D      # noqa: E402
import nav as NAV     # noqa: E402


@pytest.fixture(scope="module")
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


# ── 렌더된 사이드바에서 href 를 실제로 긁는다 (선언을 다시 읽는 게 아니다) ──────
class _NavHrefs(HTMLParser):
    """`<nav class="sidebar">` 안의 `<a href>` 만 모은다."""

    def __init__(self):
        super().__init__()
        self.depth = 0          # sidebar nav 안이면 >0
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "nav" and "sidebar" in (a.get("class") or ""):
            self.depth = 1
            return
        if not self.depth:
            return
        if tag == "nav":
            self.depth += 1
        elif tag == "a" and a.get("href"):
            # 로고(.brand)는 메뉴 항목이 아니다 — 세면 '첫 줄' 이 하나씩 밀린다
            if "brand" in (a.get("class") or "").split():
                return
            self.hrefs.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "nav" and self.depth:
            self.depth -= 1


def _sidebar_hrefs(html: str) -> list:
    p = _NavHrefs()
    p.feed(html)
    return p.hrefs


# ═══════════════════════════════════════════════════════════════════════════
# 1) 단일 출처 — 사이드바 href ⊆ ⌘K 검색 url
# ═══════════════════════════════════════════════════════════════════════════
def test_sidebar_hrefs_are_all_searchable(client):
    """⌘K 로 못 찾는 사이드바 항목이 있으면 실패.

    실측 사고(2026-09-08 v3 조사): 사이드바 21개 vs 검색 15개로 갈려
    /governance /ledger /fairchem /seminar /requests /sdcp 6개가 ⌘K 에 없었다.
    '판정' 이나 'governance' 를 쳐도 판정 원장이 안 나왔다.
    """
    html = client.get("/").get_data(as_text=True)
    nav_urls = {h for h in _sidebar_hrefs(html) if h.startswith("/")}
    assert nav_urls, "사이드바에서 href 를 하나도 못 긁었다 — 파서나 마크업이 깨졌다"

    idx = client.get("/api/search").get_json()["items"]
    search_urls = {i["url"] for i in idx}

    gaps = NAV.pairing_gaps(nav_urls, search_urls)
    assert gaps == [], f"사이드바에 있는데 ⌘K 에 없는 url: {gaps}"


def test_pairing_checker_catches_a_gap():
    """★ 음성 경로 — 짝 검사기가 **빠진 것을 실제로 잡는지**.

    양성만 보면 검사기가 늘 [] 를 돌려줘도 통과한다. 그래서 한쪽에서 지웠을 때
    실패하는지를 여기서 못 박는다.
    """
    assert NAV.pairing_gaps({"/a", "/b"}, {"/a", "/b", "/c"}) == []
    assert NAV.pairing_gaps({"/a", "/b"}, {"/a"}) == ["/b"]
    # 실제 nav 를 빈 검색 인덱스와 맞대면 전건이 위반으로 나와야 한다
    assert len(NAV.pairing_gaps(NAV.nav_page_urls(), set())) == len(NAV.nav_page_urls())


def test_search_index_is_delegated_to_nav(client):
    """data.py 가 페이지 목록을 손으로 다시 갖고 있지 않아야 한다.

    두 번째 사본이 생기는 순간 또 갈라진다 — 그래서 위임 자체를 시험한다.
    """
    idx = client.get("/api/search").get_json()["items"]
    page_urls = {i["url"] for i in idx if i["t"] == "페이지"}
    assert page_urls == NAV.nav_page_urls(), (
        "⌘K '페이지' 목록이 nav.py 와 다르다 — data.py 에 사본이 생겼다: "
        f"검색에만 {sorted(page_urls - NAV.nav_page_urls())} · "
        f"nav 에만 {sorted(NAV.nav_page_urls() - page_urls)}")


@pytest.mark.parametrize("url", ["/governance", "/ledger", "/fairchem",
                                 "/seminar", "/requests", "/sdcp"])
def test_previously_missing_pages_are_searchable(client, url):
    """검색에서 빠져 있던 6개가 다시 빠지면 여기서 걸린다."""
    idx = client.get("/api/search").get_json()["items"]
    assert url in {i["url"] for i in idx}, f"{url} 이 ⌘K 에서 또 사라졌다"


def test_nav_hrefs_are_live(client):
    """nav 가 거는 url 이 전부 살아 있는 라우트여야 한다 (nav.py 는 이걸 못 본다)."""
    dead = []
    for u in sorted(NAV.nav_page_urls()):
        code = client.get(u).status_code
        if code >= 400:
            dead.append((u, code))
    assert dead == [], f"nav 에 죽은 링크가 있다: {dead}"


# ═══════════════════════════════════════════════════════════════════════════
# 2) IA — 6묶음 · 판정 원장 승격 · 조성 묶기
# ═══════════════════════════════════════════════════════════════════════════
def test_governance_is_second_group_first_line(client):
    """⚖ 판정 원장이 두 번째 묶음 첫 줄에 있어야 한다 (종전: 5번째 묶음 5번째 줄).

    이 repo 가 굴러가는 축은 '이 값을 써도 되나' 인데 그걸 담은 화면이 맨 아래
    있었고 대시보드 본문 링크가 0건이었다.
    """
    assert NAV.SECTIONS[1]["items"][0]["url"] == "/governance"
    html = client.get("/").get_data(as_text=True)
    hrefs = [h for h in _sidebar_hrefs(html) if h.startswith("/")]
    assert hrefs[0] == "/", hrefs[:3]
    assert hrefs[1] == "/governance", f"판정 원장이 두 번째 줄이 아니다: {hrefs[:4]}"


def test_sidebar_has_six_labeled_groups(client):
    """v3 6묶음(오늘/값/어떻게 쟀나/캠페인/문헌/자료·보관)."""
    labels = [s["label"] for s in NAV.SECTIONS if s.get("label")]
    assert len(labels) == 6, labels
    html = client.get("/").get_data(as_text=True)
    for lab in labels:
        assert lab in html, f"묶음 머리말 '{lab}' 이 화면에 없다"


def test_compositions_grouped_by_family_and_active_first(client):
    """조성이 FAMILY_ORDER 로 묶이고, 묶음 안은 자료 많은 순이어야 한다."""
    cg = NAV.composition_groups(D)
    fams = [g["family"] for g in cg["groups"]]
    assert fams == [f for f in D.FAMILY_ORDER if f in fams], f"family 순서가 다르다: {fams}"
    for g in cg["groups"]:
        ns = [r["n"] for r in g["links"]]
        assert ns == sorted(ns, reverse=True), f"{g['family']} 이 활성 순이 아니다: {ns}"
    html = client.get("/").get_data(as_text=True)
    for fam in fams:
        assert f'aria-label="{fam} 조성"' in html, fam


def test_planned_compositions_are_folded_not_deleted(client):
    """자료 0인 조성은 접히되 **DOM 에 남아 있어야** 한다 — 캠페인 범위 선언이다."""
    cg = NAV.composition_groups(D)
    shown = {r["cid"] for g in cg["groups"] for r in g["links"]}
    planned = {r["cid"] for r in cg["planned"]}
    assert shown | planned == set(D.COMPOSITIONS), (
        f"조성이 사라졌다: {sorted(set(D.COMPOSITIONS) - shown - planned)}")
    assert planned, "접힘 묶음이 비었다 — 판정 규칙이 바뀌었는지 확인"

    html = client.get("/").get_data(as_text=True)
    assert 'data-fold="nav-comps-planned"' in html
    for cid in planned:
        assert f'href="/composition/{cid}"' in html, f"{cid} 이 DOM 에서 빠졌다(삭제 금지)"


def test_planned_fold_opens_when_you_are_inside_it(client):
    """접힌 묶음 안 페이지를 보고 있으면 서버가 펴서 보낸다 — 현재 위치가 숨으면 안 된다."""
    cid = NAV.composition_groups(D)["planned"][0]["cid"]
    html = client.get(f"/composition/{cid}").get_data(as_text=True)
    assert re.search(r'data-fold="nav-comps-planned" open', html), \
        "접힌 조성 페이지인데 사이드바가 접힌 채로 왔다"
    # 음성: 홈에서는 열려 있으면 안 된다(기본 접힘이라는 뜻이 사라진다)
    home = client.get("/").get_data(as_text=True)
    assert not re.search(r'data-fold="nav-comps-planned" open', home)


def test_planned_rule_is_derived_not_a_hardcoded_list():
    """★ 음성 경로 — '자료 없음' 이 손으로 적은 조성 목록이면 안 된다.

    자료 수를 0 으로 만든 가짜 데이터 모듈을 넣으면 **전부** 접힘으로 가야 한다.
    특정 cid 만 접히면 목록이 코드에 박혀 있다는 뜻이다.
    """
    class _Fake:
        COMPOSITIONS = {"aa": {"label": "A", "formula": "A", "family": "argyrodite", "color": "#000"},
                        "bb": {"label": "B", "formula": "B", "family": "argyrodite", "color": "#111"}}
        FAMILY_ORDER = ["argyrodite"]

        @staticmethod
        def canonical_values(cid):
            return {}

        @staticmethod
        def datafiles_for(cid):
            return ()

        @staticmethod
        def structures_for(cid):
            return []

    cg = NAV.composition_groups(_Fake)
    assert cg["groups"] == [], "자료가 0인데 펼침 묶음이 생겼다"
    assert {r["cid"] for r in cg["planned"]} == {"aa", "bb"}

    # 반대로 자료를 붙이면 접힘에서 빠져나와야 한다
    _Fake.datafiles_for = staticmethod(lambda cid: ({"x": 1},) * 5)
    cg2 = NAV.composition_groups(_Fake)
    assert cg2["planned"] == [], "자료가 붙었는데도 '자료 없음' 으로 남아 있다"


def test_campaign_slug_needs_token_boundaries():
    """★ 음성 경로 — 캠페인 슬러그가 낱말 안쪽에 걸리면 없는 배지가 생긴다.

    실측: 슬러그 'nd' 가 `hash-bou**nd**-carry` · `cascade_d_rel_estima**nd**` 에
    걸려 Nd/O 캠페인에 '결정 3 · 카드 2' 라는 가짜 배지가 떴다.
    """
    rx = NAV._slug_re("nd")
    for wrong in ("d-2026-08-20-hash-bound-carry", "cascade_d_rel_estimand_2026_09_08.json"):
        assert not rx.search(wrong), f"토큰 경계가 없다 — '{wrong}' 에 걸렸다"
    for right in ("d-2026-09-09-nd-anneal", "modelc_nd_doped_closed.json", "nd_survey"):
        assert rx.search(right), right
    # 배지는 없으면 안 단다 (0 으로 찍지 않는다)
    row = [it for sec in NAV.sidebar() for it in sec["links"]
           if it["url"] == "/composition/modelc_nd_doped"][0]
    st = NAV.campaign_status("nd")
    assert (row.get("badge") is None) == (st["decisions"] == 0 and st["cards"] == 0)


# ═══════════════════════════════════════════════════════════════════════════
# 3) 온보딩 — 숫자는 전부 db 파생, 못 읽으면 0 이 아니라 '못 읽음'
# ═══════════════════════════════════════════════════════════════════════════
def test_onboard_panel_is_on_home_with_links(client):
    html = client.get("/").get_data(as_text=True)
    assert 'class="v3-onboard"' in html
    assert "그 값을 써도 되는지" in html, "한 줄 정체가 없다"
    for url in ("/explorer", "/governance", "/glossary"):
        assert f'class="v3-stat" href="{url}"' in html, f"{url} 로 가는 칸이 없다"


def test_onboard_numbers_match_db_now():
    """4칸 숫자가 **지금 db 를 세어 나온 값**과 같아야 한다 (템플릿에 박으면 실패)."""
    import canonical as C
    import glossary as G
    st = {c["key"]: c["n"] for c in NAV.onboard_stats()["cards"]}
    reg = C.load_registry()
    assert st["canonical"] == sum(1 for e in reg.get("entries", [])
                                  if e.get("status") == "canonical")
    assert st["hazard"] == len(D.citation_hazards().get("hazards") or [])
    assert st["decision"] == sum(1 for d in C.decisions().values()
                                 if C.decision_state(d) == "active")
    assert st["term"] == len(G.GLOSSARY)


def test_onboard_says_unreadable_instead_of_zero(tmp_path):
    """★ 음성 경로 — db 가 없으면 숫자를 지어내지 않는다.

    '없다(0)' 와 '못 읽었다' 는 화면에서 달라야 한다. 여기서 0 이 나오면
    숫자가 어딘가에 하드코딩돼 있다는 뜻이다.
    """
    st = NAV.onboard_stats(root=str(tmp_path))          # 빈 디렉터리 = db 없음
    got = {c["key"]: c["n"] for c in st["cards"]}
    assert got["canonical"] in (None, 0), got
    assert got["decision"] in (None, 0), got
    assert st["risk"]["lost"] in (None, 0), st["risk"]
    # 그리고 진짜 db 에서는 숫자가 나와야 한다 (양성 짝)
    real = {c["key"]: c["n"] for c in NAV.onboard_stats()["cards"]}
    assert (real["canonical"] or 0) > 0 and (real["decision"] or 0) > 0


def test_risk_banner_links_to_governance(client):
    """유실·유일본 경보가 홈에서 판정 원장으로 이어져야 한다 (종전엔 링크 0건)."""
    rk = NAV.onboard_stats()["risk"]
    html = client.get("/").get_data(as_text=True)
    if (rk["lost"] or 0) or (rk["single"] or 0):
        assert 'class="v3-risk" href="/governance"' in html
        assert f"<b>{rk['lost']}건</b>" in html and f"<b>{rk['single']}건</b>" in html
    else:
        pytest.skip("지금 원장에 유실·유일본이 없다")


# ═══════════════════════════════════════════════════════════════════════════
# 4) 범례 — 어휘를 손으로 쓰지 않는다
# ═══════════════════════════════════════════════════════════════════════════
def test_status_legend_comes_from_status_badge_dict(client):
    """범례 문구가 `_STATUS_BADGE` 에서 나와야 한다 — 화면마다 말이 갈리는 걸 막는다."""
    leg = NAV.status_legend(D)
    assert {k for r in leg for k in r["keys"]} == set(D._STATUS_BADGE)
    assert len(leg) == len({v[0] for v in D._STATUS_BADGE.values()}), \
        "표시명 합치기가 어긋났다 (예: superseded·retracted → '철회')"
    html = client.get("/").get_data(as_text=True)
    for r in leg:
        assert f">{r['label']}</span>" in html, f"범례에 '{r['label']}' 이 안 찍혔다"


def test_status_legend_is_not_hardcoded():
    """★ 음성 경로 — 가짜 배지 dict 를 주면 그대로 따라와야 한다."""
    class _Fake:
        _STATUS_BADGE = {"zz": ("가짜상태", "#000", "#fff", "시험용 설명")}
    got = NAV.status_legend(_Fake)
    assert len(got) == 1 and got[0]["label"] == "가짜상태", got

    # 표시명이 같은 두 키는 한 줄로 합치고 **긴 설명**을 남긴다
    class _Fake2:
        _STATUS_BADGE = {"a": ("철회", "#a", "#b", "짧다"),
                         "b": ("철회", "#a", "#b", "이쪽이 훨씬 길고 자세한 설명이다")}
    got2 = NAV.status_legend(_Fake2)
    assert len(got2) == 1 and got2[0]["keys"] == ["a", "b"]
    assert got2[0]["desc"].startswith("이쪽이")


def test_unknown_three_way_is_taught(client):
    """TODO(안 했다) / N/A(성립 안 한다) / 비인용(했는데 못 쓴다) 3구분."""
    rows = NAV.unknown_legend(D)
    assert [r["key"] for r in rows] == ["todo", "na", "noncite"]
    html = client.get("/").get_data(as_text=True)
    for r in rows:
        assert r["label"] in html, r
    # 셋이 **다른 모양**이어야 한다 — 같은 점선 회색으로 뭉치면 안 갈린다
    css = (ROOT / "webapp" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    styles = {k: re.search(r"\.uk-%s\{([^}]*)\}" % k, css) for k in ("todo", "na", "noncite")}
    assert all(styles.values()), f"uk-* 클래스가 없다: {[k for k, v in styles.items() if not v]}"
    bodies = [m.group(1) for m in styles.values()]
    assert len(set(bodies)) == 3, "세 상태가 같은 모양이다 — 눈으로 안 갈린다"


def test_mark_legend_counts_real_cards_only():
    """카드 표지 범례는 **지금 쓰인 것만** 센다. 관례에 없는 표지는 '뜻 미정' 으로 드러난다."""
    rows = NAV.mark_legend(D)
    assert rows, "표지 범례가 비었다"
    assert all(r["n"] > 0 for r in rows), "안 쓰인 표지를 범례에 적었다"

    class _Fake:
        @staticmethod
        def dashboard_highlights():
            return [{"t": "⭐ 진짜"}, {"t": "✦ 처음 보는 표지"}, {"t": "표지 없음"}]
    got = {r["mark"]: r["means"] for r in NAV.mark_legend(_Fake)}
    assert got["⭐"] == "비준 · 재현됨"
    assert "미정" in got["✦"], "관례에 없는 표지를 아는 척했다"
    assert len(got) == 2, got


# ═══════════════════════════════════════════════════════════════════════════
# 5) 접근성·조작 배선이 살아 있는지 (v3 재편이 통째로 다시 쓰지 않았는지)
# ═══════════════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("url", ["/", "/glossary", "/explorer", "/governance"])
def test_shell_wiring_survives(client, url):
    """skip-link · rail · ⌘K combobox · aria-expanded · Esc 우선순위."""
    h = client.get(url).get_data(as_text=True)
    for needle in ('class="skip-link" href="#main"',
                   'id="railbtn"', "function toggleRail",
                   'role="combobox"', "aria-activedescendant",
                   'aria-expanded="false"', "function closeCmdk"):
        assert needle in h, f"{url}: '{needle}' 이 사라졌다"


def test_active_page_is_marked(client):
    """현재 페이지가 aria-current 로 표시돼야 한다 (하위 항목이면 부모도)."""
    h = client.get("/requests").get_data(as_text=True)
    assert h.count('aria-current="page"') >= 2, "1저자 요청에서 부모(작업 기록) 강조가 빠졌다"
    assert re.search(r'href="/requests" aria-current="page"', h)
    assert re.search(r'href="/log" aria-current="page"', h)


def test_css_keeps_prohibition_marks():
    """⛔ 인용 금지를 화면에 보이게 하는 클래스는 지우면 안 된다."""
    css = (ROOT / "webapp" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    for cls in (".cell-blocked", ".claim-mark", ".claim-flag"):
        assert cls + "{" in css, f"{cls} 가 사라졌다"
    # v3 가 다른 묶음에 약속한 클래스
    for cls in (".v3-fold", ".v3-band", ".v3-onboard", ".v3-legend", ".v3-chip"):
        assert cls in css, f"{cls} 가 없다 — 다른 묶음이 이걸 기다린다"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
