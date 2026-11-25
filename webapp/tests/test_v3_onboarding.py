"""검증 ③ — "처음 오는 사람이 5분 안에 이 앱을 쓸 수 있는가" 를 시험으로 박는다.

00_PLAN.md §온보딩 의 5분 경로(0–30초 / 30초–1분 / 1–2분 / 2–4분 / 4–5분)를
사람이 한 번 밟아 보고 끝내면 다음 주에 또 낡는다. 그래서 밟은 경로를 그대로
시험으로 옮겼다. 여기가 깨지면 "처음 온 사람이 막힌다" 는 뜻이다.

⛔ 이 시험이 못 하는 것
  · **읽히는가**를 못 잰다. 문구가 있는지, 링크가 사는지, 숫자가 db 에서 오는지만 본다.
    글이 이해되는지·다크모드 대비·모바일 폭·실제 키보드 조작은 브라우저가 필요하다.
  · 값이 물리적으로 맞는지 안 본다 (그건 어느 화면 시험도 안 본다).
  · 카드 **개수**를 고정하지 않는다 — 원장이 늘면 늘어야 정상이다.
"""
import html
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A          # noqa: E402
import canonical as C    # noqa: E402
import data as D         # noqa: E402
import glossary as G     # noqa: E402
import nav as NAV        # noqa: E402


@pytest.fixture(scope="module")
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


# ═══════════════════════════════════════════════════════════════════════════
# 도구 — 접힌 곳으로 가는 앵커 찾기 (음성 픽스처로 먼저 검증한다)
# ═══════════════════════════════════════════════════════════════════════════
def _closed_details_spans(doc: str):
    """`open` 없는 <details> 의 (start, end) 목록."""
    return [(m.start(), m.end()) for m in
            re.finditer(r'(?is)<details\b(?![^>]*\bopen\b).*?</details>', doc)]


def buried_anchors(doc: str):
    """이 문서 안의 `href="#x"` 중 **목적지가 닫힌 <details> 안**인 것.

    v3 는 "삭제보다 접기" 라서 이 상황이 구조적으로 생긴다. details 를 fragment
    로 자동으로 펴는 건 최신 Chrome/Firefox 뿐이라, 그 밖에서는 눌러도 빈 자리로
    스크롤한다 — 그래서 화면이 스스로 펴 줘야 한다.
    """
    closed = _closed_details_spans(doc)
    out = []
    for frag in set(re.findall(r'href="#([^"]+)"', doc)):
        try:
            fid = html.unescape(frag)
        except Exception:                                # noqa: BLE001
            fid = frag
        i = doc.find('id="%s"' % fid)
        if i < 0:
            continue
        if any(s < i < e for s, e in closed):
            out.append(fid)
    return sorted(out)


def test_buried_anchor_detector_negative_and_positive():
    """★ 음성 경로 — 탐지기가 **틀린 입력을 잡아내는지** 부터 본다.

    이 단언이 없으면 아래 `buried_anchors(...) == []` 류는 "정규식이 아무것도
    못 찾아서" 통과할 수 있다. 그건 통과가 아니라 침묵이다.
    """
    buried = ('<a href="#t">가기</a>'
              '<details><summary>접힘</summary><p id="t">본문</p></details>')
    assert buried_anchors(buried) == ["t"], "닫힌 details 안 앵커를 못 잡는다"

    opened = ('<a href="#t">가기</a>'
              '<details open><summary>펼침</summary><p id="t">본문</p></details>')
    assert buried_anchors(opened) == [], "펼쳐진 details 를 묻혔다고 오판한다"

    plain = '<a href="#t">가기</a><p id="t">본문</p>'
    assert buried_anchors(plain) == [], "접힘이 없는데 묻혔다고 오판한다"

    assert buried_anchors('<a href="#nope">가기</a>') == [], \
        "목적지가 아예 없는 앵커까지 '묻혔다' 로 세면 안 된다(다른 결함이다)"


# ═══════════════════════════════════════════════════════════════════════════
# 0–30초 — 한 줄 정체 · 4칸 · 위험 배너
# ═══════════════════════════════════════════════════════════════════════════
def test_first_30s_identity_and_four_panels(client):
    doc = client.get("/").get_data(as_text=True)
    assert "그 값을 써도 되는지" in doc, "홈에 한 줄 정체가 없다"
    stats = re.findall(r'class="v3-stat[^"]*" href="(/[^"]*)"', doc)
    assert len(stats) == 4, "온보딩 4칸이 4개가 아니다: %r" % stats
    # 숫자가 있으면 반드시 갈 데가 있다 — 죽은 숫자는 온보딩이 아니다.
    for url in set(stats):
        assert client.get(url).status_code == 200, "%s 로 가는 칸이 죽었다" % url


def test_home_internal_links_all_alive(client):
    """처음 온 사람이 홈에서 누를 수 있는 내부 링크가 전부 살아 있나."""
    doc = client.get("/").get_data(as_text=True)
    urls = sorted({u for u in re.findall(r'href="(/[^"#?]*)"', doc)})
    assert len(urls) > 20, "홈 링크를 못 긁었다 — 정규식이 죽었는지 본다"
    dead = [(u, client.get(u).status_code) for u in urls
            if client.get(u).status_code != 200]
    assert dead == [], "홈에서 죽은 링크: %r" % dead


def test_hazard_panel_reconciles_with_governance(client):
    """★ 홈 "29건" 과 /governance "인용 금지 9건" 이 서로를 부정하면 안 된다.

    원장에는 RESOLVED·SUPERSEDED 도 **남긴다**(규율). 그래서 등재 전건과
    지금 유효한 금지 건수는 원래 다르다. 다른 건 괜찮은데, 홈이 큰 수만 보여
    주고 설명을 안 하면 처음 온 사람은 두 화면에서 3배 다른 수를 보고 둘 다
    안 믿는다. 그래서 홈 칸 설명이 쪼갠 수를 **db 에서 세어** 말해야 한다.
    """
    rows = D.citation_hazards().get("hazards") or []
    live = sum(1 for z in rows if C.prohibition_active(z))
    blocked = sum(1 for z in rows if z.get("level") == "BLOCKED")

    card = next(c for c in NAV.onboard_stats()["cards"] if c["key"] == "hazard")
    assert card["n"] == len(rows), "홈 칸 수가 원장 등재 건수와 다르다"
    assert str(live) in card["why"] and str(blocked) in card["why"], \
        "홈 칸 설명이 '유효 %d · 금지 %d' 를 말하지 않는다: %r" % (live, blocked, card["why"])

    doc = client.get("/").get_data(as_text=True)
    assert card["why"] in doc, "쪼갠 수가 화면까지 안 내려갔다"
    gov = client.get("/governance").get_data(as_text=True)
    assert "인용 금지(BLOCKED) %d건" % blocked in gov, \
        "판정 원장 쪽 BLOCKED 표기가 바뀌었다 — 두 화면 문구를 같이 옮겨야 한다"


# ═══════════════════════════════════════════════════════════════════════════
# 30초–1분 — 빈 칸 세 가지가 눈으로 갈리나
# ═══════════════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("url", ["/", "/explorer"])
def test_three_kinds_of_empty_cell_are_taught_and_distinct(client, url):
    """TODO(안 했다) · N/A(성립 안 한다) · 비인용(했는데 못 쓴다).

    셋이 같은 점선 회색 칸으로 뭉쳐 있던 게 v3 이전 상태다. 어휘가 있는지와
    **설명이 서로 다른지**를 같이 본다 — 같은 문장을 세 번 쓰면 안 갈린다.
    """
    doc = client.get(url).get_data(as_text=True)
    for word, must in (("TODO", "안 했다"),
                       ("N/A", "성립 안 한다"),
                       ("비인용", "했는데 못 쓴다")):
        assert word in doc, "%s 에 '%s' 어휘가 없다" % (url, word)
        assert must in doc, "%s 에 '%s' 설명이 없다 (%s)" % (url, must, word)
    assert len({"안 했다", "성립 안 한다", "했는데 못 쓴다"}) == 3


# ═══════════════════════════════════════════════════════════════════════════
# 1–2분 — "이번 주 바뀐 것" 이 실제로 그 카드로 데려가나
# ═══════════════════════════════════════════════════════════════════════════
def test_this_week_anchors_exist(client):
    doc = client.get("/").get_data(as_text=True)
    frags = sorted(set(re.findall(r'href="#(hl-[^"]+)"', doc)))
    assert frags, "'이번 주 바뀐 것' 앵커가 하나도 없다"
    missing = [f for f in frags if ('id="%s"' % f) not in doc]
    assert missing == [], "가리키는 카드가 문서에 없다: %r" % missing


@pytest.mark.parametrize("url", ["/", "/governance"])
def test_buried_anchors_have_a_way_out(client, url):
    """접힌 곳으로 가는 링크가 있으면 화면이 그걸 펴 줘야 한다.

    실측(2026-09-09): 홈은 '이번 주 바뀐 것' 3장 중 1장, /governance 는 결정행
    2건(superseded·retracted 접힘)이 닫힌 details 안이다. 접는 건 규율이고
    지우면 안 되니, 고칠 자리는 **여는 배선**이다.
    """
    doc = client.get(url).get_data(as_text=True)
    if buried_anchors(doc):
        assert "_revealHash" in doc, \
            "%s: 접힌 곳으로 가는 앵커 %r 가 있는데 펴는 배선이 없다" % (url, buried_anchors(doc))
    # 배선은 항상 실려 있어야 한다 — 지금 안 묻혀 있어도 다음 편집에서 묻힌다.
    assert "_revealHash" in doc, "%s 에 딥링크 펼침 배선이 없다" % url


# ═══════════════════════════════════════════════════════════════════════════
# 2–4분 — 값이 궁금하다 / 뭘 조심해야 하나, 두 갈래
# ═══════════════════════════════════════════════════════════════════════════
def test_explorer_puts_method_anchors_above_the_table(client):
    """"이 표를 믿을지 말지" 를 정하는 정보가 27칸 표 **위**에 있어야 한다."""
    doc = client.get("/explorer").get_data(as_text=True)
    assert "정본 값 진입점" in doc, "explorer 부제에 진입점 선언이 없다"
    anchor = doc.find("방법 검증 앵커")
    table = doc.find("<table")
    assert anchor >= 0, "방법 검증 앵커 절이 없다"
    assert anchor < table, "방법 검증 앵커가 표 아래에 있다 (믿을 근거가 뒤에 온다)"


def test_governance_green_banner_states_its_scope(client):
    """초록 배너가 **무엇을 보증했는지** 를 말해야 한다.

    구조 검증 통과 바로 밑에 유실·BLOCKED 가 이어지면, 범위를 안 적은 초록은
    "다 괜찮다" 로 읽힌다.
    """
    doc = client.get("/governance").get_data(as_text=True)
    assert "그래프·어휘만" in doc, "초록 배너에 검사 범위가 없다"
    assert "타당성은 검사하지 않는다" in doc, "안 본 것을 안 봤다고 말하지 않는다"


# ═══════════════════════════════════════════════════════════════════════════
# 4–5분 — 용어
# ═══════════════════════════════════════════════════════════════════════════
def test_glossary_has_research_discipline_terms(client):
    """이 repo 에서 제일 자주 쓰는 개념 5개가 용어집에 있고 앵커가 걸리나."""
    disc = [t for t in G.GLOSSARY if t.get("cat") == "연구 규율"]
    assert len(disc) >= 5, "연구 규율 카테고리가 5장 미만이다"
    terms = {t["term"] for t in disc}
    for want in ("보고량", "닫힘 조건", "대조 잡", "허용 서술 범위"):
        assert any(want in t for t in terms), "'%s' 가 용어집에 없다: %r" % (want, terms)

    doc = client.get("/glossary").get_data(as_text=True)
    for t in disc:
        assert 'id="%s"' % t["id"] in doc, "%s 카드에 앵커 id 가 없다" % t["term"]


def test_cmdk_index_finds_the_discipline_terms():
    """⌘K 는 사이드바와 같은 출처에서 나오고, 새 용어를 찾을 수 있어야 한다."""
    items = D.search_index()
    def hit(q):
        q = q.lower()
        return [i for i in items
                if q in (i.get("label", "") + " " + (i.get("sub") or "") + " "
                         + (i.get("kw") or "")).lower()]
    assert hit("/governance") or [i for i in items if i.get("url") == "/governance"], \
        "⌘K 에 /governance 가 없다"
    for q in ("보고량", "봉인", "닫힘"):
        assert hit(q), "⌘K 에서 '%s' 가 안 걸린다" % q
    # 음성 짝 — 아무 문자열이나 걸리면 위 단언은 아무것도 보증 못 한다.
    assert not hit("존재하지않는용어zzzq"), "검색이 아무거나 다 걸린다"
