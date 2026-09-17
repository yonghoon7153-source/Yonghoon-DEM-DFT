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
import re
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
    """⛔음성: 소속은 **카드가 선언**한다. 파일명 접두어로 찾으면 남의 화면에 샌다.

    ⚠ 2026-09-15 수정 — 종전 판은 `assert not interpretation_cards_for(cid)`, 즉 **다른 조성에
      카드가 하나도 없어야** 통과였다. 그건 Nd 카드가 유일할 때만 맞는 잣대라, modelc 에 정당한
      해석 카드를 하나 올리자마자 "Nd 카드가 샜다" 는 **엉뚱한 메시지로** 빨간불이 났다
      (시험이 재려던 것과 실제로 재던 것이 달랐다). 지금은 **그 Nd 카드가 있는지**만 본다.
    """
    nd_files = {r["file"] for r in V.interpretation_cards_for(ND)}
    assert nd_files, "전제: Nd 조성에 해석 카드가 있다"
    for cid in ("comp1", "modelc", "lpsocl", "b2o3"):
        leaked = nd_files & {r["file"] for r in V.interpretation_cards_for(cid)}
        assert not leaked, f"{cid} 에 Nd 카드가 샜다: {sorted(leaked)}"
        # 남의 카드가 아니라도, 거기 뜬 카드는 **자기 소속을 선언**하고 있어야 한다
        for r in V.interpretation_cards_for(cid):
            assert r.get("composition") == cid, \
                f"{cid} 화면에 소속이 {r.get('composition')} 인 카드가 떴다: {r['file']}"


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


def test_no_literal_markdown_asterisks_on_the_card(client):
    """⛔음성: 원장 문자열의 `**` 가 **기호로** 화면에 나오면 잡는다.

    2026-09-14 실측 — 표 제목만 `|mdlite` 를 안 타서 "창이 **좁아진다**고" 가 별표째 나왔다.
    셀·설명은 필터를 탔는데 제목만 빠진 자리였다. 새 필드를 늘릴 때 같은 구멍이 또 난다.
    ⚠ 못 하는 것: script·style·주석 안은 안 본다 (JS 리터럴의 `**` 는 정당하다).
    """
    import re as _re
    h = client.get(f"/composition/{ND}").get_data(as_text=True)
    body = _re.sub(r"<script.*?</script>", "", h, flags=_re.S)
    body = _re.sub(r"<style.*?</style>", "", body, flags=_re.S)
    body = _re.sub(r"<!--.*?-->", "", body, flags=_re.S)
    hits = [m.group(0).replace("\n", " ") for m in _re.finditer(r".{0,40}\*\*.{0,40}", body, _re.S)]
    assert not hits, f"별표가 기호로 노출된 자리 {len(hits)}곳: {hits[:3]}"


def test_card_markdown_actually_becomes_bold(client):
    """양성: 카드의 `**강조**` 가 실제로 <b>/<strong> 으로 바뀐다.

    ⚠ 위 음성만 있으면 "필터가 문자열을 통째로 지워도" 통과한다 — 별표가 없어지니까.
      강조가 **살아서 태그로** 나왔는지 같이 본다.
    """
    h = client.get(f"/composition/{ND}").get_data(as_text=True)
    tabs = V.interpretation_cards_for(ND)[0]["tables"]
    marked = [t for t in tabs if "**" in t["title"]]
    assert marked, "전제 실패: 제목에 강조가 든 표가 없다 (이 시험이 공허해진다)"
    # ⛔ 강조 **안쪽 단어만** 찾으면 안 된다 — 같은 단어가 카드 머리글에도 강조로 들어 있어서
    #   표 제목의 강조를 통째로 지워도 통과했다 (2026-09-14 실측, 고장 주입으로 잡음).
    #   **제목 전체**를 렌더된 형태로 만들어 대조한다: 별표가 남아도, 강조가 사라져도 어긋난다.
    import re as _re
    for t in marked:
        want_b = _re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t["title"])
        want_s = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t["title"])
        assert (want_b in h) or (want_s in h), \
            f"표 제목이 렌더된 형태로 안 나온다: {want_s[:70]}"



# ── 보고서 버튼이 **정본**을 가리키는가 (2026-09-17) ─────────────────────────
#   왜 생겼나 (실측): Nd/O 카드의 보고서 버튼이 외부 아티팩트 URL 하나만 가리켰는데,
#   그 URL 은 만든 세션 밖에서 갱신이 안 된다(publish 거부 — 원본을 못 받는다).
#   그래서 repo 를 고쳐도 버튼은 낡은 화면을 열었다. 이제 webapp 이 정본을 직접 서빙한다.
LOCAL_REPORT = "/api/file/db/properties/cei_figs/index.html"


def test_nd_card_report_button_points_at_the_repo_copy():
    """양성 — Nd/O 카드의 보고서 버튼이 **이 화면이 서빙하는 정본**이다."""
    cards = V.interpretation_cards_for(ND)
    urls = [l["url"] for c in cards for l in c["links"]]
    assert LOCAL_REPORT in urls, f"정본 링크가 버튼에 없다: {urls}"
    local = [l for c in cards for l in c["links"] if l.get("local")]
    assert local and local[0]["url"] == LOCAL_REPORT, "정본이 첫 버튼이어야 한다"


def test_local_report_is_actually_served(client):
    """양성 — 그 경로가 **진짜로 열린다**. 링크만 걸고 404 면 붙인 게 아니다."""
    r = client.get(LOCAL_REPORT)
    assert r.status_code == 200, f"정본이 안 열린다 ({r.status_code})"
    body = r.get_data(as_text=True)
    assert "<h2 id=\"s1\">" in body, "보고서 본문이 아니다"
    # 이번 세션이 고친 그 문장이 실제로 화면에 온다 (원장↔화면 결속)
    assert "24 조건이 개별로도" in body, "§1 보강 문장이 화면에 없다"


def test_report_images_are_served_relative_to_it(client):
    """양성 — 그림도 같은 경로에서 온다 (상대 src 가 풀린다)."""
    r = client.get("/api/file/db/properties/cei_figs/cei_nd_o_decomposition.png")
    assert r.status_code == 200 and r.data[:4] == b"\x89PNG", "Fig 1 PNG 가 안 온다"


def test_bare_internal_path_in_prose_does_not_become_a_button():
    """⛔음성 — 산문에 경로가 우연히 들어가도 버튼이 **안** 생긴다.

    링크는 **선언**이지 발견이 아니다. 맨 경로까지 주우면 설명문에 쓴 예시가
    화면에서 버튼이 되고, 그건 카드가 가리킨 적 없는 곳이다.
    """
    j = {"note": "자세한 것은 /api/file/db/properties/anything.html 를 보라"}
    assert V.card_links(j) == [], f"맨 경로를 주웠다: {V.card_links(j)}"


def test_internal_link_outside_allowlist_is_not_a_button():
    """⛔음성 — 허용 접두(/api/file·/files·/kb) 밖은 버튼이 안 된다."""
    j = {"note": "[비밀](/etc/passwd) · [설정](/admin/settings)"}
    assert V.card_links(j) == [], f"허용 밖 경로를 주웠다: {V.card_links(j)}"


def test_https_links_still_work_alongside_local():
    """양성 — 외부 링크 기능이 죽지 않았다. 다만 정본이 **앞**에 선다."""
    j = {"a": "[정본](/api/file/db/properties/x.html)",
         "b": "[거울](https://example.com/mirror)"}
    got = V.card_links(j)
    assert [l["url"] for l in got] == ["/api/file/db/properties/x.html",
                                       "https://example.com/mirror"], got
    assert got[0].get("local") is True and "local" not in got[1]


# ── 보고서 PDF 저장(인쇄) 표면 (2026-09-17) ─────────────────────────────────
REPORT = Path(__file__).resolve().parents[2] / "db/properties/cei_figs/index.html"


def _report_html(client):
    r = client.get(LOCAL_REPORT)
    assert r.status_code == 200
    return r.get_data(as_text=True)


def test_pdf_button_is_on_the_report(client):
    """양성 — PDF 저장 버튼이 화면에 있고, 인쇄할 때는 자기가 사라진다."""
    h = _report_html(client)
    assert "window.print()" in h, "PDF 저장 버튼이 없다"
    assert 'class="noprint"' in h, "버튼이 noprint 로 안 감싸져 있다"
    assert re.search(r"@media print\b", h), "인쇄 규칙이 없다"
    assert re.search(r"\.noprint\s*\{[^}]*display\s*:\s*none", h), \
        "인쇄에서 버튼을 숨기지 않는다 — 종이에 버튼이 찍힌다"


def test_print_keeps_background_colours(client):
    """⛔음성 — 배경색을 버리면 §3 모식도의 보라 칸이 흰 칸이 된다.

    그 칸 색이 "Nd 가 여는 방" 이라는 **뜻을 나르는** 유일한 표식이라,
    색이 빠지면 그림이 말을 안 한다.
    """
    h = _report_html(client)
    blk = re.search(r"@media print\s*\{.*?\n  \}", h, re.S)
    assert blk, "인쇄 블록을 못 찾았다"
    assert "print-color-adjust" in blk.group(0), "print-color-adjust 가 없다"


def test_print_forces_light_palette_for_every_dark_selector(client):
    """⛔음성 — 다크 선택자를 늘리고 인쇄 블록을 안 고치면 **까맣게 인쇄된다**.

    다크 팔레트를 세우는 선택자를 전부 찾아, 인쇄 블록이 그 **전부**를 덮는지 본다.
    새 선택자가 생기면 이 시험이 먼저 빨개진다.
    """
    h = REPORT.read_text(encoding="utf-8")
    dark_bg = "--bg:#141220"
    # 다크 팔레트 직전의 선택자들
    darks = set()
    for m in re.finditer(r"([^{};]+)\{[^{}]*" + re.escape(dark_bg), h):
        darks.add(m.group(1).strip().rstrip("{").strip())
    assert darks, "다크 팔레트 블록을 못 찾았다 — 시험이 헛것을 재고 있다"
    pm = re.search(r"@media print\s*\{(.*?)\n  \}", h, re.S)
    assert pm, "인쇄 블록이 없다"
    printed = pm.group(1)
    missing = [d for d in darks if d not in printed]
    assert not missing, f"인쇄 블록이 안 덮는 다크 선택자: {missing}"


def test_long_table_is_not_glued_into_one_page(client):
    """⛔음성 — §8 원자료 표에 break-inside:avoid 를 걸면 한 쪽을 넘겨 **잘린다**.

    대신 머리 반복(thead)과 행 단위 보호만 건다. 이 구분이 사라지면 잡는다.
    """
    h = _report_html(client)
    blk = re.search(r"@media print\s*\{.*?\n  \}", h, re.S).group(0)
    assert "table-header-group" in blk, "여러 쪽 표의 머리를 반복하지 않는다"
    assert not re.search(r"(^|[\s,]) *table\s*(,[^{]*)?\{[^}]*break-inside\s*:\s*avoid", blk), \
        "table 전체에 break-inside:avoid 가 걸렸다 — 긴 표가 잘린다"
