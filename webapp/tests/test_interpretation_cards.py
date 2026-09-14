#!/usr/bin/env python3
"""test_interpretation_cards.py — 해석 카드(`interpretation_card/v1`) 표면의 회귀.

    pytest webapp/tests/test_interpretation_cards.py -q

왜 따로인가 (2026-09-14): 해석 카드는 **값이 아니라 서술**이라 조용히 틀리면 더 비싸다.
남의 조성 화면에 뜨거나(소속 오판), 못 읽은 파일이 조용히 사라지거나(있는데 없다고 보임),
금지 서술이 화면에서 빠지는 것 — 셋 다 검사한다.

⛔ 이 파일이 못 하는 것: 카드 **내용의 과학적 타당성**을 판정하지 않는다. 원장이 적은 것을
  화면이 그대로 옮기는지만 본다.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

from app import app            # noqa: E402
import decisions_view as V     # noqa: E402

ND = "modelc_nd_doped"


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_nd_card_is_found_and_bound_to_its_composition():
    rows = V.interpretation_cards_for(ND)
    assert rows, "Nd/O 조성에 해석 카드가 0건이다 (원장에 있다)"
    r = rows[0]
    assert r["composition"] == ND
    assert r["title"] and r["headline"], "제목·한 줄이 비었다"
    assert r["forbidden"], "금지 서술이 비었다 — 해석 카드의 핵심이다"
    assert r["counter"], "반대 증거가 비었다 — 숨기지 않기로 한 절이다"


def test_card_does_not_leak_to_other_compositions():
    """⛔음성: 소속은 **카드가 선언**한다. 파일명 접두어로 찾으면 남의 화면에 샌다."""
    for cid in ("comp1", "modelc", "lpsocl", "b2o3"):
        assert not V.interpretation_cards_for(cid), f"{cid} 에 Nd 카드가 샜다"


def test_unreadable_card_is_reported_not_skipped(tmp_path, monkeypatch):
    """⛔음성: 깨진 카드를 **조용히 건너뛰지 않는다** — 없는 것과 못 읽은 것은 다르다."""
    d = tmp_path / "db" / "properties"
    d.mkdir(parents=True)
    (d / "broken_card.json").write_text(
        '{"schema": "interpretation_card/v1", "composition": "x", BROKEN', encoding="utf-8")
    rows = V.interpretation_cards_for("anything", root=tmp_path)
    assert rows and rows[0].get("error"), f"깨진 카드가 조용히 사라졌다: {rows}"


def test_non_card_json_is_ignored(tmp_path):
    """⛔음성: 스키마가 아닌 JSON 을 해석 카드로 읽지 않는다."""
    d = tmp_path / "db" / "properties"
    d.mkdir(parents=True)
    (d / "plain.json").write_text(json.dumps({"composition": "x", "값": 1}), encoding="utf-8")
    assert V.interpretation_cards_for("x", root=tmp_path) == []


def test_screen_shows_headline_forbidden_and_citable_flag(client):
    """양성: 화면이 한 줄·금지 서술·citable 지위를 **실제로** 그린다."""
    import html as _h
    html = _h.unescape(client.get(f"/composition/{ND}").data.decode())
    r = V.interpretation_cards_for(ND)[0]
    assert r["title"][:20] in html, "제목이 화면에 없다"
    assert "금지 서술" in html and "반대 증거" in html
    assert "citable = no" in html, "비인용 카드인데 지위 배지가 없다"
    assert r["file"] in html, "원본 파일 경로가 화면에 없다"


def test_forbidden_lines_actually_reach_the_page(client):
    """⛔음성: 금지 서술이 **한 줄이라도** 화면에 빠지면 잡는다 (접힘은 DOM 에 남는다)."""
    # ⚠ 템플릿이 따옴표를 이스케이프한다(`'` → `&#39;`). **풀고 비교한다** —
    #   2026-09-14 에 이걸 안 풀어서 화면은 멀쩡한데 시험만 빨간불이었다.
    #   시험을 느슨하게 하는 게 아니라 비교 기준을 맞추는 것이다.
    import html as _h
    page = _h.unescape(client.get(f"/composition/{ND}").data.decode())
    for line in V.interpretation_cards_for(ND)[0]["forbidden"]:
        probe = line.replace("⛔ ", "")[:18]
        assert probe in page, f"금지 서술이 화면에 안 나간다: {probe}"


def test_other_composition_page_has_no_card_section(client):
    html = client.get("/composition/comp1").data.decode()
    assert "해석</span>" not in html and "금지 서술" not in html


# ── 숫자 표 ─────────────────────────────────────────────────────────────────
def test_tables_render_with_their_source(client):
    """양성: 표가 화면에 그려지고 **출처 파일**을 달고 나간다."""
    import html as _h
    page = _h.unescape(client.get(f"/composition/{ND}").data.decode())
    tabs = V.interpretation_cards_for(ND)[0]["tables"]
    assert tabs, "해석 카드에 표가 0개다"
    for tb in tabs:
        assert not tb["error"], f"표 모양이 어긋난다: {tb['title']} — {tb['error']}"
        assert tb["title"][:12] in page, f"표 제목이 화면에 없다: {tb['title']}"
        assert tb["source"] and tb["source"] in page, f"표에 출처가 안 붙었다: {tb['title']}"
        for cell in tb["rows"][0]:
            probe = cell.replace("**", "")[:10]
            assert probe in page, f"표 첫 행이 화면에 안 나간다: {probe}"


def test_table_numbers_still_match_the_raw_record():
    """⛔음성 **표류 감시**: 카드의 표가 원자료와 어긋나면 잡는다.

    카드는 손으로 쓴 문서다. 원자료(`pdos_band_edge_composition_*.json`)를 다시 계산하면
    카드의 수는 자동으로 안 바뀐다 — 그 간극이 '화면이 낡은 수를 계속 보여주는' 경로다.
    """
    raw = json.loads((ROOT / "db/properties/pdos_band_edge_composition_2026_09_14.json")
                     .read_text(encoding="utf-8"))
    src = {r["label"]: r for r in raw}
    tab = next(t for t in V.interpretation_cards_for(ND)[0]["tables"]
               if "가장자리" in t["title"])
    cells = " ".join(" ".join(r) for r in tab["rows"])
    checked = 0
    for label, edge in (("ndo_lpscl16_n5fu", "VBM"), ("ndo_lpscl16_n5fu", "CBM"),
                        ("modelc_undoped", "VBM"), ("modelc_undoped", "CBM")):
        comp = src[label][f"{edge}_composition_pct"]
        for el, pct in comp.items():
            if pct < 1.0:            # 1 % 미만은 표에서 생략될 수 있다 — 요구하지 않는다
                continue
            # ⚠ 카드는 사람이 읽는 요약이라 **소수 1자리**로 적는다 (선언된 반올림).
            #   원문 그대로(77.34)든 1자리(77.3)든 하나는 있어야 한다 — 78.1 로 표류하면 둘 다 없다.
            ok = (f"{el} {pct}" in cells) or (f"{el} {round(pct, 1)}" in cells)
            assert ok, (f"표가 원자료와 어긋난다: {label} {edge} {el} 은 {pct} % "
                        f"(1자리 {round(pct, 1)}) 인데 표에 없다")
            checked += 1
    assert checked >= 12, f"대조한 값이 {checked}개뿐이다 — 검사가 공허하다"


def test_malformed_table_is_reported_not_hidden(tmp_path):
    """⛔음성: 열 수와 칸 수가 다른 표를 **조용히 그리지 않는다**."""
    d = tmp_path / "db" / "properties"
    d.mkdir(parents=True)
    (d / "t.json").write_text(json.dumps({
        "schema": "interpretation_card/v1", "composition": "x",
        "표": [{"제목": "깨진 표", "columns": ["a", "b"], "rows": [["1"], ["2", "3"]]}],
    }, ensure_ascii=False), encoding="utf-8")
    tb = V.interpretation_cards_for("x", root=tmp_path)[0]["tables"][0]
    assert tb["error"] and "[0]" in tb["error"], f"어긋난 행을 안 잡았다: {tb}"

