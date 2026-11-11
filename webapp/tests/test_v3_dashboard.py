#!/usr/bin/env python3
"""test_v3_dashboard.py — v3 묶음 B(대시보드 `/`)의 회귀 시험.

여기 담은 건 전부 **실제로 한 번 틀렸던 것**이다.
  · 카드 41장이 통째로 펼쳐져 26,672자(정독 89분)짜리 첫 화면이었다
  · 손으로 쓴 `v2` 배지·부제 요약이 두 번 낡았다 (09-03·09-07·09-08 비준을 광고 못 함)
  · 미결 수를 `## ` 절 단위로만 걸러 이미 닫힌 `### ` 항목까지 대기로 셌다
  · "MP frozen-4f 값을 인용할 것" 이 27일 낡은 채 화면에 지시형으로 떠 있었다
  · 문헌 수가 대시보드 218 / `/literature` 215 로 갈렸다 (`__seminar` 동반 대본)
  · 통계 4칸이 전부 클릭 안 되는 숫자였고, 매트릭스 cascade 열은 14칸 중 12칸이 N/A 였다

⚠ 시험마다 **음성 경로**(틀린 입력을 잡아내는지)를 같이 둔다. 양성만 있는 시험은
  통과해도 아무것도 보증 못 한다.

⛔ 이 시험이 **못 하는 것**
  · 축 배정이 물리적으로 옳은지 판정하지 못한다. "카드를 잃지 않는가 · 제목을
    본문보다 먼저 보는가" 만 본다.
  · 브라우저를 안 띄운다. 접힘이 눈에 어떻게 보이는지는 확인 못 했다.

    pytest webapp/tests/test_v3_dashboard.py -q
"""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A       # noqa: E402
import data as D      # noqa: E402

INDEX_HTML = ROOT / "webapp" / "templates" / "index.html"


@pytest.fixture(scope="module")
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


@pytest.fixture(scope="module")
def home(client):
    r = client.get("/")
    assert r.status_code == 200, "대시보드가 안 뜬다"
    return r.get_data(as_text=True)


# ══ ① 미결 카운트 — 닫힌 항목을 대기로 세지 않는다 ═══════════════════════════
def test_open_items_closed_are_not_counted_as_waiting():
    """양성: 원장이 제목에 닫혔다고 적은 항목은 대기에서 빠지고 따로 센다."""
    oi = D.open_items_summary()
    assert oi["closed"] > 0, "전제: 원장에 제목으로 닫은 항목이 있다"
    # 대기 목록 안에는 닫힘 표식이 하나도 없어야 한다
    for s in oi["sections"]:
        for it in s["items"]:
            assert not D._oi_is_closed(it), f"닫힌 항목이 대기에 남았다: {it[:50]}"
    # **버리지는 않았다** — 닫힌 것도 그대로 들고 있어야 화면이 접어 보일 수 있다
    assert len(oi["closed_items"]) == oi["closed"]


def test_open_items_closed_detector_negative():
    """⛔음성: 안 닫힌 제목을 닫혔다고 하면 안 된다 (그러면 미결이 조용히 사라진다)."""
    closed = ["~~M6~~. ✅ cascade 양극 반응성 게이트 — 완료",
              "3. ~~VGCF 2×2 barrier 행렬~~ → ✅ 완료 (2026-07-30)",
              "O. ✅ **Nd 갭 — 3종 자체 측정 완료**"]
    still_open = ["2. b2o3 MD Ea 재실행 — 미완",
                  "⏭-2. cascade 해제조건 8건 중 ②만 이행",
                  "5. NEB 3×3×3 재개 대기",
                  # ⚠ 함정: 본문에 '완료' 라는 **낱말**만 있는 항목은 여전히 대기다.
                  "7. 완료 판정을 받을 것 — 아직 안 받음"]
    for t in closed:
        assert D._oi_is_closed(t), f"닫힘 표식을 못 읽었다: {t}"
    for t in still_open:
        assert not D._oi_is_closed(t), f"안 닫힌 항목을 닫혔다고 했다: {t}"


def test_open_items_pipeline_on_fixture(tmp_path, monkeypatch):
    """양성+⛔음성: 만든 원장을 넣으면 대기 2 · 닫힘 2 로 갈린다."""
    md = tmp_path / "open_items.md"
    md.write_text(
        "## A 절\n"
        "### 1. 살아 있는 항목\n"
        "### 2. ~~닫은 항목~~ → ✅ 완료 (2026-01-01)\n"
        "## ✅ 닫힌 항목\n"
        "### 3. 여기 것은 절째로 빠진다\n"
        "## B 절\n"
        "### 4. ✅ 판정 완료\n"
        "### 5. 또 살아 있는 항목\n", encoding="utf-8")
    monkeypatch.setattr(D, "OPEN_ITEMS_MD", md)
    D._open_items_c.cache_clear()
    try:
        oi = D.open_items_summary()
        assert oi["total"] == 2, f"대기 수가 틀렸다: {oi['total']}"
        assert oi["closed"] == 2, f"닫힘 수가 틀렸다: {oi['closed']}"
        titles = [it for s in oi["sections"] for it in s["items"]]
        assert titles == ["1. 살아 있는 항목", "5. 또 살아 있는 항목"]
    finally:
        D._open_items_c.cache_clear()


# ══ ② 축 묶기 — 카드를 잃지 않는다 ══════════════════════════════════════════
def test_highlight_groups_lose_no_card():
    """양성: 묶어도 카드 수가 그대로다. 접기는 되고 **삭제는 안 된다**."""
    cards = D.dashboard_highlights()
    groups = D.highlight_groups(cards)
    seen = [c for g in groups for c in [g["latest"]] + g["rest"]]
    assert len(seen) == len(cards), "축으로 묶으면서 카드가 사라졌다"
    assert {id(c) for c in seen} == {id(c) for c in cards}
    for g in groups:
        assert g["n"] == 1 + len(g["rest"])
        # 묶음 안 정렬은 최신순 그대로 (1저자 요청 2026-08-20)
        ds = [c.get("d") or "" for c in [g["latest"]] + g["rest"]]
        assert ds == sorted(ds, reverse=True), f"{g['axis']} 축 안이 최신순이 아니다"
    # 묶음 사이도 최신순 — "새로 안 것이 위" 규칙이 축을 얹어도 안 깨져야 한다
    heads = [g["latest"].get("d") or "" for g in groups]
    assert heads == sorted(heads, reverse=True)


def test_highlight_axis_reads_title_before_body():
    """⛔음성: 본문부터 보면 오분류한다 — 실제로 그랬던 두 카드를 픽스처로."""
    # 본문에 '마감' 이 나오지만 이 카드는 β/Ea 축이다 (실측: b2o3 아레니우스 카드)
    beta = {"t": "b2o3 아레니우스가 **굽는다** — 단일 Ea 철회", "v": "",
            "n": "SDCP 캠페인 마감 문서와 같은 날 …"}
    assert D.highlight_axis(beta) == "beta", "본문의 '마감' 에 끌려갔다"
    # 반대로 제목이 마감이면 본문에 3×3×1 이 있어도 closure 다
    clo = {"t": "⭐ LPSOCl 3×3×1 닫힘 조건 **비준**", "v": "",
           "n": "상자 크기 3×3×1 · 셀 크기 논의"}
    assert D.highlight_axis(clo) == "closure"
    # 어느 축에도 안 걸리면 **버리지 않고** other 로 (조용히 사라지면 안 된다)
    assert D.highlight_axis({"t": "zzz", "v": "", "n": ""}) == "other"
    assert D.highlight_axis({}) == "other"


def test_key_cards_keep_their_anchors():
    """시험이 key 로 집는 카드 3장은 앵커도 key 에서 나온다 (제목이 바뀌어도 안 죽는다)."""
    cards = {c.get("key"): c for c in D.dashboard_highlights() if c.get("key")}
    for k in ("md_ea_ranking", "lpsocl_box331_closure", "ndo_lpscl16_anneal"):
        assert k in cards, f"key={k} 카드가 사라졌다"
        assert cards[k]["aid"] == f"hl-{k}"


def test_folded_cards_keep_forbidden_statements(home):
    """접기는 되고 삭제는 안 된다 — 접힌 카드의 ⛔ 금지 서술이 DOM 에 그대로 있다."""
    assert "<details class=\"v3-fold\">" in home, "축 이력 접기가 없다"
    folded = [c for g in D.highlight_groups() for c in g["rest"]]
    assert folded, "전제: 접힌 카드가 있다"
    bans = [c for c in folded if "⛔" in str(c.get("n") or "")]
    assert bans, "전제: 접힌 카드 중에 금지 서술을 담은 게 있다"
    # 카드 본문을 **화면과 같은 필터**로 그려서 그 조각이 DOM 에 있는지 본다
    # (평문으로 비교하면 mdlite 가 붙인 <strong> 때문에 헛나간다).
    mdlite = A.app.jinja_env.filters["mdlite"]
    for c in bans[:5]:
        drawn = str(mdlite(str(c["n"]).split("⛔", 1)[1]))
        chunk = drawn[:60]
        assert chunk in home, f"접으면서 금지 서술이 사라졌다: {chunk!r}"


# ══ ③ '이번 주 바뀐 것' — 손으로 쓰는 판 번호를 대신한다 ═══════════════════
def test_no_handwritten_version_badge():
    """⛔ 손으로 올리던 `v2` 배지·부제 요약이 되살아나면 또 낡는다."""
    src = INDEX_HTML.read_text(encoding="utf-8")
    body = re.sub(r"\{#.*?#\}", "", src, flags=re.S)      # 주석의 경고문은 남겨 둔다
    assert not re.search(r">\s*v\d+\s*<", body), "손으로 쓴 판 번호 배지가 돌아왔다"
    assert "실시간 동기화" not in body, \
        "매트릭스는 db/_index.json 스냅샷이다 — '실시간 동기화' 로 되돌리면 안 된다"


def test_recent_changes_come_from_cards(home):
    """양성: 최근 3장이 실제 카드에서 나오고 그 카드 앵커로 간다."""
    cards = D.dashboard_highlights()
    rec = D.recent_changes(cards)
    aids = {c["aid"] for c in cards}
    assert 1 <= len(rec["items"]) <= 3
    for it in rec["items"]:
        assert it["aid"] in aids, "가리키는 카드가 화면에 없다"
        assert f'href="#{it["aid"]}"' in home, "앵커 링크가 화면에 없다"
        assert f'id="{it["aid"]}"' in home, "앵커 대상이 화면에 없다"
    assert rec["week_n"] >= len([i for i in rec["items"] if i["age_days"] <= rec["days"]])
    # 최신 3장 중에는 그 축의 최신이 아니라 **접힘 안**에 있는 카드가 섞인다 —
    # 접힌 details 를 열어 주는 손잡이가 없으면 그 링크는 아무 일도 안 한다.
    folded = {c["aid"] for g in D.highlight_groups(cards) for c in g["rest"]}
    if any(it["aid"] in folded for it in rec["items"]):
        assert "v3OpenHash" in home, "접힘 안 앵커를 열어 주는 처리가 없다"


def test_recent_changes_does_not_invent_dates():
    """⛔음성: 날짜 없는 카드만 주면 **빈 목록**이다 (0 을 지어내지 않는다)."""
    rec = D.recent_changes([{"t": "날짜 없는 카드", "v": "", "n": "", "aid": "hl-x"}])
    assert rec["items"] == [] and rec["week_n"] == 0 and rec["n_dated"] == 0
    # 날짜가 아주 오래된 카드만 주면 이번 주 0건이라고 말해야 한다
    old = [{"t": "옛 카드", "v": "", "n": "", "aid": "hl-y", "d": "2020-01-01"}]
    rec2 = D.recent_changes(old)
    assert rec2["week_n"] == 0 and len(rec2["items"]) == 1
    assert rec2["items"][0]["age_days"] > 365


# ══ ④ Nd 갭 — 27일 낡은 지시를 되돌리지 않는다 ═════════════════════════════
def test_nd_gap_cites_our_frozen4f_not_mp(home):
    """양성: 우리 frozen-4f 값이 화면에 있고 행 이름에 표시가 붙는다.

    ⛔음성: 폐기된 지시("MP frozen-4f 값을 인용할 것")와, tag 를 잘라 만든
      **없는 MP id**(`mp-2763_frozen4f`)가 화면에 있으면 실패다.
    """
    assert "MP frozen-4f 값을 인용" not in home, "폐기된 MP 우회 지시가 되살아났다"
    assert "MP 인용 우회는 2026-08-12 에 폐기" in home
    ledger = json.loads((ROOT / "db/properties/sei_electronic.json")
                        .read_text(encoding="utf-8"))
    fz = {k: v for k, v in (ledger.get("results") or {}).items() if "frozen4f" in k}
    assert fz, "전제: 갭 원장에 frozen-4f 실행본이 있다"
    for tag, rec in fz.items():
        assert f"{rec['gap']:.3f}" in home, f"{tag} 의 우리 값이 화면에 없다"
        assert tag.split("_", 1)[1] not in home, \
            f"없는 MP id 가 찍힌다: {tag.split('_', 1)[1]}"
    assert home.count("frozen-4f") >= len(fz), "행 이름에 frozen-4f 표시가 없다"


# ══ ⑤ 문헌 수 — 두 화면이 같은 정의를 쓴다 ══════════════════════════════════
def test_literature_count_matches_literature_page():
    """양성: 대시보드 숫자 == /literature 목록 길이 (218 vs 215 로 갈렸던 자리)."""
    assert D.build_matrix()["literature_count"] == len(D.list_papers())


def test_digest_stem_filter_negative():
    """⛔음성: 템플릿·동반 발표대본을 digest 로 세면 안 된다."""
    assert D._is_digest_stem("sun2024_solid_electrolyte")
    assert not D._is_digest_stem("_TEMPLATE")
    assert not D._is_digest_stem("sun2024__seminar_20min")


# ══ ⑥ 통계 4칸 · 커버리지 매트릭스 ═════════════════════════════════════════
def test_stat_cells_are_links(home):
    """양성: 네 칸이 전부 갈 데가 있다 (종전엔 넷 다 클릭이 안 됐다)."""
    stats = re.findall(r'<a class="stat" href="([^"]+)"', home)
    assert len(stats) == 4, f"통계 칸이 4개가 아니다: {stats}"
    assert set(stats) == {"/explorer", "/governance", "/todo", "/literature"}


def test_home_matrix_drops_cascade_column_without_deleting_the_dict(home):
    """양성: 홈 매트릭스에 cascade 열이 없다.

    ⛔음성: NOT_APPLICABLE 사전에서 cascade 항목이 **지워지면** 실패다 — 열을 화면에서
      빼는 것과 '금지된 계산을 TODO 로 광고하지 않기' 규율을 지우는 것은 다른 일이다.
    """
    cat = next(c for c in D.CATEGORIES if c["id"] == "cascade")
    head = re.search(r'<table class="matrix">.*?</thead>', home, re.S).group(0)
    assert cat["label"] not in head, "홈 매트릭스에 cascade 열이 남았다"
    assert any(k == "cascade" for _c, k in D.NOT_APPLICABLE), \
        "NOT_APPLICABLE 의 cascade 항목이 지워졌다 (열만 빼야 한다)"
    assert 'href="/cascade"' in home, "열을 뺐으면 어디로 갔는지 말해야 한다"


def test_coverage_stats_and_matrix_use_the_same_columns(client):
    """⛔음성: 열은 뺐는데 %는 안 뺀 상태로 두면 한 화면 안에서 분모가 갈린다."""
    b = D.build_matrix()
    cov = D.build_coverage(b["properties"], b["prop_category"], b["index_metrics"])
    full = D.coverage_stats(cov)
    trimmed = D.coverage_stats({cid: {k: v for k, v in row.items()
                                      if k not in A.HOME_MATRIX_DROP}
                                for cid, row in cov.items()})
    assert trimmed["na"] < full["na"], "전제: cascade 열이 N/A 를 크게 물고 있다"
    home = client.get("/").get_data(as_text=True)
    assert f"{trimmed['done']}/{trimmed['total']}" in home, \
        "화면의 커버리지가 매트릭스에 실제로 그린 열과 다른 분모를 쓴다"
    assert f"{full['done']}/{full['total']}" not in home


def test_matrix_declares_its_snapshot_date(home):
    """스냅샷을 실시간이라고 말하지 않는다 — 조성 페이지는 이미 밝히고 있었다."""
    built = D.build_matrix().get("built")
    assert built, "전제: db/_index.json 에 built 가 있다"
    assert str(built)[:10] in home, "매트릭스 스냅샷 날짜가 화면에 없다"


def test_open_items_folded_sections_are_archived_not_waiting(tmp_path, monkeypatch):
    """양성+⛔음성: 원장이 `<details>` 로 접어 둔 절은 대기로 안 센다 (archived) — 접기 밖은 그대로 센다.

    2026-11-11 실측: ⏭ 절의 지난 세션 인계 53 절이 '대기 90 건' 에 섞여 있었다 (실제 대기 37).
    ⛔ 코드 펜스 안의 접기 줄 · `###` 줄은 접기도 제목도 아니다.
    """
    md = tmp_path / "open_items.md"
    md.write_text(
        "## A 절\n"
        "### 1. 살아 있는 항목\n"
        "<details><summary>지난 인계 기록</summary>\n\n"
        "### ⏭-NOW-z1. 지난 세션 기록\n"
        "### ⏭-NOW-z2. 또 지난 기록\n\n"
        "</details>\n\n"
        "### 2. 접기 뒤 살아 있는 항목\n"
        "```\n<details><summary>코드 안</summary>\n### 3. 코드 안 제목은 항목이 아니다\n```\n"
        "### 4. 펜스 뒤 항목\n", encoding="utf-8")
    monkeypatch.setattr(D, "OPEN_ITEMS_MD", md)
    D._open_items_c.cache_clear()
    try:
        oi = D.open_items_summary()
        titles = [it for s in oi["sections"] for it in s["items"]]
        assert titles == ["1. 살아 있는 항목", "2. 접기 뒤 살아 있는 항목", "4. 펜스 뒤 항목"], titles
        assert oi["archived"] == 2, f"접힌 절 수가 틀렸다: {oi['archived']}"
        assert oi["total"] == 3
    finally:
        D._open_items_c.cache_clear()


def test_long_headline_cards_read_as_prose(home):
    """양성+⛔음성: 핵심값이 80 자를 넘거나 여러 줄이면 본문 글씨 (`fc-v-long`) · 짧은 수치는 그대로 크게.

    2026-11-11 (사용자 *'적어도 글처럼은'*): 점착 원장 최신 세 줄 (670 자) 이 1.1 rem 800 굵기 남색 덩어리였다.
    """
    cards = re.findall(r'<div class="card find-card" id="([^"]+)"[^>]*>.*?<div class="(fc-v[^"]*)">',
                       home, re.S)
    assert cards, "전제: 대시보드에 카드가 있다"
    by_id = dict(cards)
    hl = D.dashboard_highlights()
    long_ = [h for h in hl if h.get("aid") in by_id
             and (len(str(h.get("v") or "")) > 80 or "\n" in str(h.get("v") or ""))]
    short = [h for h in hl if h.get("aid") in by_id and 0 < len(str(h.get("v") or "")) <= 40
             and "\n" not in str(h.get("v") or "")]
    assert long_ and short, "전제: 긴 핵심값 카드와 짧은 핵심값 카드가 둘 다 있다"
    for h in long_:
        assert by_id[h["aid"]] == "fc-v fc-v-long", f"{h['aid']} 긴 핵심값이 굵은 덩어리로 남았다"
    for h in short:
        assert by_id[h["aid"]] == "fc-v", f"{h['aid']} 짧은 수치까지 본문 글씨로 낮췄다"
