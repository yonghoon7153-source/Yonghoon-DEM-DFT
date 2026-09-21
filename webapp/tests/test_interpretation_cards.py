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
    # 2026-09-19 — v2 개편으로 제목이 <section id="s1"> … <h2 class="sec-h"> 가 됐다.
    # 시험은 **절이 있는가**를 보지, 옛 태그 모양을 보지 않는다.
    assert '<section id="s1"' in body, "보고서 본문이 아니다"
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


# ── §1 방법 박스의 μ_Li 산수 접이식 (2026-09-17) ──────────────────────────────
#   왜 시험하나: 이 절은 **서술**이고, 틀린 서술이 제일 비싸다. 특히 마지막 경고
#   ("§3 교환 표에는 μ_Li 가 안 들어간다")가 빠지면 두 축이 섞여서 표가 한 적 없는
#   말을 하게 된다. 그리고 숫자는 사다리 CSV 와 **같아야** 한다 — 손으로 적은 수가
#   원장과 갈라지는 것이 여기서 일어날 수 있는 조용히 틀린 경로다.

LADDER_CSV = REPORT.parent / "cei_li_budget_ladder.csv"


def _mu_details(h):
    """μ_Li 산수 접이식 하나만 잘라 준다 (§3 본문의 같은 수에 속지 않으려고)."""
    m = re.search(r"<details[^>]*>\s*<summary[^>]*>\s*왜 &quot;손해&quot;|"
                  r"<details[^>]*>\s*<summary[^>]*>\s*왜 \"손해\"", h)
    assert m, "μ_Li 산수 접이식을 못 찾았다 — 시험이 헛것을 재고 있다"
    end = h.index("</details>", m.start())
    return h[m.start():end]


def test_mu_li_arithmetic_block_is_on_the_report(client):
    """양성 — Φ 대입과 dΦ/dV 두 줄이 실제로 화면에 실린다."""
    d = _mu_details(_report_html(client))
    assert "E + (1.9089 + V)" in d, "Φ 를 풀어 쓴 줄이 없다 — '손해'가 다시 한 줄 주장이 된다"
    assert re.search(r"d&#934;/dV\s*=\s*\+N_Li|dΦ/dV\s*=\s*\+N_Li", d), \
        "전압 기울기 = Li 개수 줄이 없다"
    assert "기회비용" in d, "기회비용 읽기가 빠졌다"


def test_mu_li_block_numbers_match_the_ladder_csv(client):
    """⛔음성 — 박스에 손으로 적은 수가 사다리 CSV 와 갈라지면 잡는다.

    문자열이 아니라 **값**으로 본다 (1.5035 ≡ 1.50352 반올림, 1.67 ≡ 1.6715).
    """
    rows, cross = [], None
    for ln in LADDER_CSV.read_text(encoding="utf-8").splitlines():
        f = ln.split(",")
        if f and f[0] == "Li3PO4":
            rows.append(float(f[3]))
        if f and f[0].startswith("crossover_li_per_P"):
            cross = float(f[1])
    assert rows and cross is not None, "사다리 CSV 를 못 읽었다 — 시험이 헛것을 재고 있다"

    d = _mu_details(_report_html(client))
    quoted = re.search(r"\+([0-9]+\.[0-9]+)\s*eV/P", d)
    assert quoted, "박스가 교환에너지를 인용하지 않는다"
    assert round(rows[0], 4) == float(quoted.group(1)), \
        f"박스 {quoted.group(1)} vs CSV {rows[0]} — 두 판정이 갈렸다"

    qc = re.search(r"Li/P\s*(?:&#8776;|≈)\s*([0-9]+\.[0-9]+)", d)
    assert qc, "박스가 교차점을 인용하지 않는다"
    assert round(cross, 2) == float(qc.group(1)), \
        f"박스 교차점 {qc.group(1)} vs CSV {cross}"

    # Φ/P 상승 표는 Li/P × 4.5 V 산수다 — 그 관계가 깨지면 잡는다.
    for li_per_p, rise in ((3, 13.5), (2, 9.0), (1, 4.5)):
        assert abs(li_per_p * 4.5 - rise) < 1e-9
        assert f"+{rise:g}" in d, f"Li/P={li_per_p} 행({rise:+g})이 표에 없다"


def test_mu_li_box_states_the_closed_system_boundary(client):
    """⛔음성 — 이 경고가 빠지면 화면이 §3 표가 한 적 없는 말을 하게 된다.

    §3 의 교환 반응은 양변 Li 가 같아서 μ_Li 가 **안 들어간다**. 그 사실이 화면에
    없으면 독자는 +1.5035 eV/P 를 전압 의존량으로 읽는다.
    """
    d = _mu_details(_report_html(client))
    assert "&#916;N_Li = 0" in d or "ΔN_Li = 0" in d, \
        "Li 수지가 0 이라는 근거가 없다"
    assert "안 변한다" in d, "전압을 바꿔도 값이 안 변한다는 말이 없다"
    assert "해석의 다리" in d, "Li 예산이 해석의 다리라는 한정이 빠졌다"


def test_collapsed_details_are_expanded_for_print(client):
    """⛔음성 — 접힌 details 는 PDF 에 **안 실린다**.

    방법 박스의 μ_Li 산수·MP 코드가 그 안에 있으므로, 펼침 처리가 없으면
    PDF 만 받아 본 사람에게는 그 절이 통째로 없는 문서가 된다.
    CSS 로는 못 하므로(open 은 속성이다) beforeprint 훅이 있어야 한다.
    """
    h = _report_html(client)
    assert "<details" in h, "접이식이 하나도 없다 — 시험이 헛것을 재고 있다"
    assert "beforeprint" in h, "인쇄 전에 details 를 펼치는 훅이 없다"
    hook = re.search(r"<script>(.*?)</script>", h, re.S)
    assert hook, "스크립트가 없다"
    js = hook.group(1)
    assert "details" in js and re.search(r"\.open\s*=\s*true", js), \
        "훅이 details 를 펼치지 않는다"
    assert "afterprint" in js and re.search(r"\.open\s*=\s*false", js), \
        "인쇄 뒤 원래 접힘 상태로 안 되돌린다 — 화면이 바뀐 채로 남는다"


def test_section1_order_is_figure_then_howto_then_definition(client):
    """⛔음성 — §1 의 읽는 순서를 고정한다 (1저자 지정, 2026-09-17).

    그림 → "Fig. 1 을 읽는 법" → "세로축의 reaction energy 는 무엇인가".
    정의 상자가 앞으로 올라오면 독자가 그림에 닿기 전에 벽을 만난다.
    셋 다 §1 안에 있어야 한다 — §2 로 밀려나면 그것도 잡는다.
    """
    h = _report_html(client)
    marks = {
        "figure":     h.find('<img src="cei_nd_o_decomposition.png"'),
        "howto":      h.find("Fig. 1 을 읽는 법"),
        "definition": h.find("세로축의 <span"),
        "s2":         h.find('<section id="s2"'),
    }
    missing = [k for k, v in marks.items() if v < 0]
    assert not missing, f"§1 에서 못 찾은 표식: {missing} — 시험이 헛것을 재고 있다"
    order = sorted(marks, key=marks.get)
    assert order == ["figure", "howto", "definition", "s2"], \
        f"§1 순서가 바뀌었다: {' → '.join(order)}"


# ── ③ 기회비용 절의 정직 한정 (2026-09-17 확장) ──────────────────────────────
#   이 절은 **설명**이라 조용히 틀리면 화면이 물리를 잘못 가르친다.
#   특히 둘: 1.9089 를 응집에너지로 읽는 것, 그리고 저울 부등식을 우리가 **잰 양**
#   으로 읽는 것. 둘 다 원장에 없는 말이므로 화면이 스스로 막아야 한다.

def test_opportunity_cost_explains_why_one_Li_is_exactly_V_eV(client):
    """양성 — 환율 1:1 의 근거(Li 하나가 전자 하나를 데려간다)가 화면에 있다.

    이게 빠지면 "Li 한 개 = V eV" 가 근거 없는 단정으로 되돌아간다.
    """
    d = _mu_details(_report_html(client))
    assert "전하 &#215; 전압" in d or "전하 × 전압" in d, "일 = 전하×전압 이라는 근거가 없다"
    assert "1가" in d, "Li⁺ 가 전자를 하나만 데려간다는 근거가 없다"
    assert "환율" in d, "1:1 환율이라는 말이 없다"


def test_opportunity_cost_denies_the_cohesive_energy_reading(client):
    """⛔음성 — 1.9089 를 '응집에너지' 로 읽으면 틀린다. 그 부인이 화면에 있어야 한다.

    1.9089 는 MP 총에너지 눈금 위의 Li 금속 원자당 에너지이지, Li 금속에서 Li 하나를
    떼는 에너지가 아니다. 이 한 줄이 빠지면 화면이 틀린 물리를 가르친다.
    """
    d = _mu_details(_report_html(client))
    i = d.find("응집에너지")
    assert i > 0, "응집에너지가 아니라는 부인이 없다"
    near = d[i:i + 200]
    assert "아니다" in near, "'응집에너지' 를 언급만 하고 부인하지 않는다"


def test_opportunity_cost_says_the_balance_is_a_picture_not_a_measurement(client):
    """⛔음성 — 저울 부등식을 우리가 **잰 양**으로 읽으면 조용히 틀린 경로다.

    상별 'Li 하나 떼는 비용' 은 잰 적이 없다. 실제 게이트는 hull 이 모든 분해 경로를
    동시에 비교한 것이다. 이 한정이 빠지면 독자는 없는 측정을 인용하게 된다.
    """
    d = _mu_details(_report_html(client))
    assert "잰 적이 없다" in d, "재지 않았다는 사실이 화면에 없다"
    assert "모든 분해 경로를 동시에" in d, "실제 게이트가 hull 이라는 말이 없다"
    assert "0 K 열역학" in d, "'저절로'가 속도가 아니라는 한정이 없다"


def test_threshold_table_is_actually_mu_plus_V(client):
    """⛔음성 — 문턱 표의 수가 1.9089 + V 와 어긋나면 잡는다 (오타·복붙 사고).

    문자열이 아니라 **값**으로 본다.
    """
    d = _mu_details(_report_html(client))
    head = d.find("문턱 = 1.9089 + V")
    assert head > 0, "문턱 표를 못 찾았다 — 시험이 헛것을 재고 있다"
    body = d[head:d.index("</table>", head)]
    rows = re.findall(r"<tr><td>(?:<strong>)?([0-9.]+)(?:</strong>)?</td>"
                      r"<td>(?:<strong>)?([0-9.]+)(?:</strong>)?</td></tr>", body)
    assert len(rows) >= 4, f"문턱 표 행을 {len(rows)} 개만 읽었다 — 시험이 헛것을 재고 있다"
    for v, thr in rows:
        want = round(1.9089 + float(v), 2)
        assert abs(want - float(thr)) < 5e-3, \
            f"V={v}: 화면 {thr} vs 1.9089+V = {want:.2f}"


# ── §2 가설 카드의 사후 정정 (2026-09-17) ────────────────────────────────────
#   화면이 원장과 갈라지는 두 길을 막는다:
#     ① 표의 수가 레코드와 달라지는 것 (손편집·재생성 어긋남)
#     ② 한정("반증 아님"·"최소 꺾임만"·"proposed")이 지워져 관찰이 판정으로 격상되는 것

LADDER_JSON = REPORT.parents[3] / "db/properties/cei_p_host_ladder_2026_09_17.json"
DECISIONS = REPORT.parents[3] / "db/governance/decisions.json"
_LADDER_ID = "D-2026-09-17-cei-p-host-li-ladder"


def _s2_card(h):
    """§2 의 '1·2·4 번도 산물이 뒷받침하지 않는다' 상자만 잘라 준다.

    ⚠ 앞판은 표 뒤 첫 </div> 에서 잘라서 **표만** 들어왔다 — 한정 문장은 표 뒤에 있는데
      그걸 못 보고 "한정이 없다" 고 빨개졌다. 상자 끝까지 잡는다.
    ⚠ 2026-09-19 — 끝 표식을 <strong>가법성 설명</strong> 이라는 **문구**로 잡고 있었는데,
      화면에서 내부 용어("가법성")를 걷어내자 그 문구가 사라져 시험이 빨개졌다.
      **문구는 바뀐다. 구조는 덜 바뀐다** ⇒ 다음 <section 경계로 잡는다.
    """
    i = h.find("⛔ 1·2·4 번도 산물이 뒷받침하지 않는다")
    assert i > 0, "§2 정정 상자를 못 찾았다 — 시험이 헛것을 재고 있다"
    j = h.find("<section id=", i)
    assert j > i, "§2 의 끝(다음 절 시작)을 못 찾았다 — 시험이 헛것을 재고 있다"
    return h[i:j]


def test_s2_ladder_table_matches_the_record(client):
    """⛔음성 — 화면 표의 Li/P 가 레코드와 갈라지면 잡는다.

    문자열이 아니라 **값**으로 본다. 화면은 무도핑(modelc) 6 전압 x 4 양극을 싣는다.
    """
    import json as _json
    rec = _json.loads(LADDER_JSON.read_text(encoding="utf-8"))
    want = {}
    for r in rec["rows"]:
        if r["electrolyte"] != "modelc":
            continue
        for hst in r["p_hosts"]:
            want.setdefault(hst["formula"], set()).add(hst["li_per_P"])
    assert want, "레코드에서 modelc 행을 못 읽었다 — 시험이 헛것을 재고 있다"

    card = _s2_card(_report_html(client))
    seen = re.findall(r'<span class="mono"[^>]*>(.*?)</span>\s*<b>([0-9.]+)</b>', card)
    assert len(seen) >= 24, f"화면 표에서 상을 {len(seen)} 개만 읽었다 — 시험이 헛것을 재고 있다"
    for raw, val in seen:
        f = re.sub(r"</?sub>", "", raw)
        assert f in want, f"화면에 레코드에 없는 상이 있다: {f}"
        assert float(val) in want[f], \
            f"{f}: 화면 Li/P {val} vs 레코드 {sorted(want[f])}"


def test_s2_correction_keeps_its_epistemic_limits(client):
    """⛔음성 — 한정이 지워지면 사후 관찰이 판정으로 격상된다.

    셋 다 필요하다: 반증이 아니라는 것 · 최소 꺾임만 봤다는 것 · 아직 비준 전이라는 것.

    ⚠ 2026-09-19 — 비준 전 표시를 `"proposed"` 라는 **영어 원장 낱말**로 잡고 있었다.
      1저자 지시로 화면에서 내부 용어를 걷어내면서 그 자리가 "1저자 검토 전" 로 바뀌자
      시험이 빨개졌다. 화면은 맞고 시험이 낡았던 것이다.
      ⇒ 낱말이 아니라 **원장과의 결속**을 본다: 결정이 active 가 아니면 화면에
        (허용된 어휘 중) 비준 전 표시가 있어야 한다.
    """
    import json as _json
    _st = {d["id"]: d.get("decision_state")
           for d in _json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]}
    card = _s2_card(_report_html(client))
    assert "반증한 것이 아니라" in card, "'반증이 아니다' 한정이 없다 — 관찰이 반증으로 읽힌다"
    assert "최소 꺾임 하나만" in card, "최소 꺾임 한정이 없다"
    assert "결과를 본 뒤의 관찰" in card, "사후 관찰이라는 표시가 없다"
    assert _LADDER_ID in _st, f"원장에 {_LADDER_ID} 가 없다 — 시험이 헛것을 재고 있다"
    if _st[_LADDER_ID] != "active":
        NOT_RATIFIED = ("proposed", "1저자 검토 전", "비준 전", "검토 전")
        assert any(w in card for w in NOT_RATIFIED), (
            f"원장은 {_st[_LADDER_ID]} 인데 화면에 비준 전 표시가 없다 "
            f"(허용 어휘 {NOT_RATIFIED})")


def test_s2_ladder_decision_is_registered_and_not_silently_active():
    """⛔음성 — 사후 관찰을 active 로 올리면 잡는다 (사람 비준 없이 판정이 되면 안 된다)."""
    import json as _json
    ds = _json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]
    row = [d for d in ds if d["id"] == _LADDER_ID]
    assert row, f"{_LADDER_ID} 가 원장에 없다 — 화면이 없는 결정을 가리킨다"
    d = row[0]
    assert d["decision_state"] == "proposed", \
        f"사후 관찰인데 decision_state 가 {d['decision_state']} 다 — 비준 없이 격상됐다"
    assert d.get("results_seen") is True and d.get("exploratory") is True, \
        "results_seen / exploratory 가 안 서 있다"
    assert Path(d["record"]).name == LADDER_JSON.name, "record 가 실제 레코드를 안 가리킨다"


def test_old_fig2_bar_count_does_not_come_back(client):
    """⛔음성 — 지운 옛 Fig. 2 (양극 개수 막대 집계) 가 되돌아오면 잡는다.

    그 그림은 **끝점 퇴화 칸을 세는 결함**을 가진 채로 발행돼 있었다
    (modelc@4.5V/LiMnO2 는 x=1.0 자체분해인데 P2S7 1 건으로 세어졌다).
    2026-09-17 에 지우고 사다리 그림이 Fig. 2 번호를 승계했다. 되돌아오면
    그 결함도 같이 돌아온다.
    """
    h = _report_html(client)
    assert "cei_nd_phosphate_sink" not in h, \
        "지운 옛 Fig. 2 가 화면에 다시 들어왔다 (끝점 결함째로)"
    assert not (REPORT.parent / "cei_nd_phosphate_sink.png").exists(), \
        "옛 그림 파일이 되살아났다"
    gen = (REPORT.parents[3] / "tools/figures/plot_cei_nd_o_decomposition.py").read_text("utf-8")
    assert "nd_phosphate_sink" not in gen, "생성기가 옛 그림을 다시 만든다"
    # 번호는 사다리 그림이 가져갔다
    assert "Fig. 2. Voltage changes who neodymium competes against" in h, \
        "Fig. 2 번호 승계가 안 돼 있다"


# ── Fig. 2 = P 수용상 사다리 (2026-09-17 교체) ─────────────────────────────────────────────────────
FIG2_CSV = REPORT.parent / "cei_p_host_ladder_fig.csv"


def test_fig2_ladder_image_is_served(client):
    """양성 — 그림이 참조돼 있고 실제로 200 으로 나온다."""
    h = _report_html(client)
    assert 'src="cei_p_host_ladder.png"' in h, "Fig. 2 (사다리) 가 화면에 없다"
    r = client.get(LOCAL_REPORT.rsplit("/", 1)[0] + "/cei_p_host_ladder.png")
    assert r.status_code == 200 and len(r.data) > 20000, \
        f"그림이 안 나온다 ({r.status_code}, {len(r.data)} B)"


def test_fig2_exchange_values_match_the_record(client):
    """⛔음성 — 화면이 인용한 교환에너지가 레코드와 갈라지면 잡는다 (값으로 본다)."""
    import json as _json
    rec = _json.loads((REPORT.parents[3] / "db/properties/cei_tm_exchange_2026_09_17.json")
                      .read_text(encoding="utf-8"))
    vals = {k.split(",")[0]: v["E_eV_per_P"] for k, v in rec["reactions"].items() if v.get("ok")}
    assert vals, "교환 레코드를 못 읽었다 — 시험이 헛것을 재고 있다"
    assert abs(vals["Li3PO4"] - 1.5035) < 5e-4, \
        f"대조 잡이 §3 값을 재현하지 않는다: {vals['Li3PO4']}"
    tm = [v for k, v in vals.items() if k != "Li3PO4"]
    assert all(v < 0 for v in tm), "전이금속 교환이 전부 음수가 아니다"
    h = _report_html(client)
    m = re.search(r"<b>−([0-9.]+) ~ −([0-9.]+)</b>", h)
    assert m, "화면이 전이금속 교환 범위를 인용하지 않는다"
    lo, hi = float(m.group(1)), float(m.group(2))
    assert abs(lo - abs(max(tm))) < 5e-3 and abs(hi - abs(min(tm))) < 5e-3, \
        f"화면 −{lo}~−{hi} vs 레코드 {max(tm):.4f}~{min(tm):.4f}"


def test_fig2_refuses_to_rank_within_the_tie_width(client):
    """⛔음성 — 0.30 eV/P 안의 차이를 순위로 쓰면 잡는다.

    NiP4O11 −2.1511 과 CoP4O11 −2.1646 은 0.0135 차다. 순위를 주장하면 없는 해상도를
    쓰는 것이고, 화면은 그걸 명시적으로 거절해야 한다.
    """
    h = _report_html(client)
    assert "0.30" in h and "구분 못 하는 폭" in h, "구분되지 않는 폭이 화면에 없다"
    assert "순위는 못 쓴다" in h, "순위를 쓰지 않는다는 선언이 없다"
    assert "not ranked against each other" in h, "캡션(영문)에 같은 한정이 없다"


def test_fig2_separates_onset_from_growth(client):
    """⛔음성 — "교환 부호가 이득 전부" 로 읽히면 틀린다.

    ΔE 중앙값은 4.0 V 에서 포화(−1.751)하는데 Fig. 1 의 Δ 는 1.9 배 더 커진다.
    그 구분이 빠지면 가설 4 번(공급)을 부당하게 닫은 것이 된다.
    """
    h = _report_html(client)
    assert "포화" in h, "교환에너지가 포화한다는 사실이 화면에 없다"
    assert "성장은 설명 못 한다" in h, "시작/성장 구분이 없다"
    assert "다시 살아 있다" in h, "가설 4 번이 되살아났다는 자기정정이 없다"
    assert "고전압이 아니다" in h, "부호 전환 자리가 고전압이 아니라는 한정이 없다"


def test_fig2_ladder_caption_says_price_not_amount(client):
    """⛔음성 — 세로축을 '풀려난 P 의 양' 으로 읽으면 이 그림이 안 한 말을 하게 된다."""
    h = _report_html(client)
    i = h.find("Fig. 2. Voltage changes who")
    assert i > 0, "Fig. 2 캡션을 못 찾았다"
    cap = h[i:h.index("</figcaption>", i)]
    assert "not an amount of P" in cap, "세로축이 양이 아니라는 한정이 캡션에 없다"
    assert "chosen, not selected by the hull" in cap, \
        "반응물·생성물을 사람이 골랐다는 고지가 없다"
    assert "mix functionals" in cap, "GGA/GGA+U 혼합 눈금 고지가 없다"


def test_fig2_refuses_to_predict_hull_products(client):
    """⛔음성 — 2상 교환 부호로 hull 산물을 설명한다고 읽히면 틀린다.

    2026-09-17 에 세 번 어긋났다 (Cl·S 사각지대 · Nd 는 P 선호인데 산물은 NdCl3 ·
    Mn/Ni 방향은 맞지만 0.30 띠 안). 그 경계가 화면에서 빠지면 다음 사람이
    네 번째로 같은 벽에 닿는다.
    """
    h = _report_html(client)
    i = h.find("Fig. 2 를 읽는 법")
    assert i > 0, "Fig. 2 설명 상자를 못 찾았다 — 시험이 헛것을 재고 있다"
    d = h[i:h.index("<h3", i)]          # ⚠ 앞판은 §1 의 μ_Li 접이식을 봤다 (다른 절)
    assert "hull 이 고른 상" in d, "hull 산물 예측 금지가 화면에 없다"
    assert "방향 힌트" in d, "교환이 방향 힌트라는 한정이 없다"
    assert "부호가 어긋났다" in d, "실제로 어긋난 사례가 없다"


# ── 치환 자리 × 농도 2×2 (2026-09-19) ────────────────────────────────────────
#   왜 생겼나: 이 2×2 는 **화면 두 곳**에 실린다 — 정본 보고서(cei_figs/index.html)와
#   Nd 카드(`/composition/modelc_nd_doped`). 원장은 세 번째 곳이다. 셋이 갈라지면
#   사람은 눈앞의 화면을 인용한다. 값으로 묶는다 (문자열 일치가 아니라 **숫자**).
SITE_RESULT = REPORT.parents[3] / "db/properties/cei_site_concentration_result_2026_09_19.json"
_SITE_DECISION = "D-2026-09-19-cei-site-vs-concentration"


def _site_2x2():
    import json as _json
    t = _json.loads(SITE_RESULT.read_text(encoding="utf-8"))["★_2x2_공통기준"]["표"]
    return {k: float(v["값"]) for k, v in t.items()}


def _nums(text):
    """텍스트의 부호 붙은 소수 → float 집합. −(U+2212) 도 마이너스로 읽는다."""
    return {float(x.replace("−", "-"))
            for x in re.findall(r"[−+-]?\d+\.\d+", text.replace(",", ""))}


def test_site_2x2_record_is_self_consistent():
    """⛔음성 — 원장 자체가 앞뒤가 맞나 (화면을 보기 전에 원장부터).

    부호가 표의 주장(Li 자리 양수 · P 자리 음수)과 어긋나면 잡는다.
    """
    v = _site_2x2()
    assert set(v) == {"Li자리_x002", "P자리_x002", "Li자리_x020", "P자리_x020"}, \
        f"2×2 의 칸이 넷이 아니다: {sorted(v)} — 시험이 헛것을 재고 있다"
    assert v["Li자리_x002"] > 0 and v["Li자리_x020"] > 0, "Li 자리는 양수여야 한다"
    assert v["P자리_x002"] < 0 and v["P자리_x020"] < 0, "P 자리는 음수여야 한다"
    # 농도 선형성: x=0.20 이 x=0.02 의 10 배 언저리 (사전 봉인 문턱 0.010)
    for site, a, b in (("Li", "Li자리_x020", "Li자리_x002"),
                       ("P", "P자리_x020", "P자리_x002")):
        assert abs(v[a] - 10 * v[b]) <= 0.010, \
            f"{site} 자리 선형성 잔차 {v[a] - 10 * v[b]:+.5f} 가 문턱 0.010 을 넘는다"


def test_site_2x2_numbers_are_on_the_report(client):
    """⛔음성 — 정본 보고서의 2×2 표가 원장과 **값으로** 같은가."""
    h = _report_html(client)
    i = h.find("빠진 칸을 채웠다")
    assert i > 0, "2×2 카드를 못 찾았다 — 시험이 헛것을 재고 있다"
    card = h[i:h.index("</table>", i)]
    seen = _nums(card)
    for k, want in _site_2x2().items():
        assert any(abs(x - want) < 5e-5 for x in seen), \
            f"{k}: 원장 {want:+.5f} 가 보고서 표에 없다 (화면의 수 {sorted(seen)})"


def test_site_2x2_numbers_are_on_the_nd_card():
    """⛔음성 — Nd 카드(webapp 조성 화면)가 같은 값을 싣는가.

    ⚠ 보고서만 고치고 카드를 안 고치면 **두 화면이 갈라진다** — 이 시험이 그걸 잡는다.
    """
    cards = V.interpretation_cards_for(ND)
    blob = json.dumps(cards, ensure_ascii=False)
    assert "치환 자리" in blob, "Nd 카드에 치환 자리 절이 없다 — 시험이 헛것을 재고 있다"
    seen = _nums(blob)
    for k, want in _site_2x2().items():
        assert any(abs(x - want) < 5e-5 for x in seen), \
            f"{k}: 원장 {want:+.5f} 가 Nd 카드에 없다"


def test_site_decision_is_ratified_by_a_human():
    """⛔음성 — 화면이 '확정' 이라고 말하려면 원장에 사람 비준이 있어야 한다."""
    import json as _json
    ds = {d["id"]: d for d in
          _json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]}
    d = ds.get(_SITE_DECISION)
    assert d, f"{_SITE_DECISION} 가 원장에 없다 — 시험이 헛것을 재고 있다"
    assert d.get("decision_state") == "active", f"상태가 {d.get('decision_state')!r} 다"
    rat = d.get("ratification") or {}
    assert rat.get("state") == "ratified" and rat.get("role") == "scientific_owner", \
        f"사람(scientific_owner) 비준이 없다: {rat.get('state')!r}/{rat.get('role')!r}"


def test_slope_mechanism_stays_forbidden_on_both_surfaces(client):
    """⛔음성 — **풀리지 않은 것**이 풀린 것처럼 보이면 잡는다.

    자리 판정은 해제됐지만 '전압 기울기를 Li 수로 설명한다' 는 사후 적합이라
    여전히 금지다. 해제가 통째로 번지는 것이 제일 흔한 사고다.
    """
    import json as _json
    rec = _json.loads(SITE_RESULT.read_text(encoding="utf-8"))
    assert any("기울기" in x and "⛔" in x for x in rec["금지_서술"]), \
        "원장 금지 목록에 기울기 항목이 없다 — 시험이 헛것을 재고 있다"
    h = _report_html(client)
    assert "부호가 틀렸고" in h, "보고서가 예측 실패를 안 싣는다"
    assert "검증 전" in h, "보고서가 '아직 검증 전' 한정을 안 싣는다"
    blob = json.dumps(V.interpretation_cards_for(ND), ensure_ascii=False)
    assert "검증 전" in blob, "Nd 카드가 '아직 검증 전' 한정을 안 싣는다"


# ── 2026-09-21 쇄신 — 층 가르기 · Fig 번호 · Fig. 1 3패널 · §6 10/10 · §9 개수 · §0 onset ────
#   왜 생겼나: 보고서를 통째로 재배열했다. 재배열은 문자열 시험이 제일 잘 깨지는 자리라
#   시험을 **재는 것(구조·번호·원장 일치)** 으로 다시 썼다. 각 시험은 쓴 뒤 대상을 일부러
#   깨서 빨간불을 확인했다 (커밋 메시지에 기록).
GAP_RESULT = REPORT.parents[3] / "db/properties/cei_gap_results_2026_09_19.json"
HAZARDS = REPORT.parents[3] / "db/properties/citation_hazards.json"
ESW = REPORT.parents[3] / "db/properties/cei_esw_Li_2026_09_16.json"
_NDP_HZ = "HZ-cei-gap-ndp5o14-unreproduced"


def _section(h, sid):
    i = h.index(f'<section id="{sid}"')
    return h[i:h.index("</section>", i)]


def test_figure_numbers_are_unique_and_in_document_order(client):
    """양성 — 캡션 번호가 문서 순서로 1..8 이고 중복이 없다.
    2026-09-21 전에는 1, 2, 2, 4, 5, 6, 7, 3 이었다 (보호율 곡선이 Fig. 2 를 두 번 썼다)."""
    h = _report_html(client)
    nums = re.findall(r"<figcaption><b>Fig\. (\d+)\.", h)
    assert nums == [str(i) for i in range(1, 9)], nums


def test_fig1_is_three_panels_and_caption_carries_no_strikethrough(client):
    """양성+음성 — 옛 (c) ×6.58 패널이 그림에서 빠졌고, 캡션은 취소선 철회문 없이 선다.
    철회 표지는 한글 '읽는 법' 상자에 ⛔ 로 있다 (그림은 복사될 때 캡션을 안 데려간다)."""
    h = _report_html(client)
    i = h.index('<img src="cei_nd_o_decomposition.png"')
    cap = h[i:h.index("</figcaption>", i)]
    assert 'alt="Three panels.' in cap, "alt 가 아직 네 패널이다"
    assert "RETRACTED" not in cap and "<s>" not in cap, "캡션 안에 취소선 철회문이 남아 있다"
    assert "lithium-matched" in cap, "Li 장부 설명이 캡션에서 빠졌다"
    r = client.get(LOCAL_REPORT.rsplit("/", 1)[0] + "/cei_nd_o_decomposition.png")
    import struct
    w, hgt = struct.unpack(">II", r.data[16:24])            # PNG IHDR
    assert w / hgt > 2.5, f"그림이 1×3 이 아니다 (옛 2×2 는 비 1.38): {w}×{hgt}"
    gen = (REPORT.parents[3] / "tools/figures/plot_cei_nd_o_decomposition.py").read_text("utf-8")
    assert "plt.subplots(1, 3" in gen and re.search(r"^\s*a3\.", gen, re.M) is None, \
        "생성기에 옛 (c) 패널(a3)이 되돌아왔다"
    j = h.index("Fig. 1 을 읽는 법")
    box = h[j:h.index("<!-- 방법 박스", j)]
    assert "⛔" in box and "Li 장부" in box and "−50.8" in box, "읽는 법 상자에 철회 표지가 없다"


def test_layer_split_open_sections_are_the_thesis(client):
    """양성 — 접힘 밖(open)은 논지 절이고, 근거·검산·반론 절은 접혀 있되 요지 한 줄이 밖에 있다."""
    h = _report_html(client)
    st = dict(re.findall(r'<section id="(\w+)" class="sec">\n<details class="secfold"( open)?>', h))
    assert set(st) >= {"s0", "s1", "s2", "s2b", "s3", "s4", "s5", "s6", "s7", "s8", "s8b", "s9", "sf"}, sorted(st)
    opened = {k for k, v in st.items() if v}
    assert opened == {"s0", "s2", "s2b", "s6", "s7", "sf"}, sorted(opened)
    for sid in st:
        m = re.search(r'<span class="sec-one">(.*?)</span></summary>', _section(h, sid), re.S)
        assert m and len(re.sub(r"<[^>]+>", "", m.group(1)).strip()) > 10, f"{sid}: 요지 줄이 없다"


def test_s6_gap_table_is_10_of_10_and_matches_the_record(client):
    """양성 — §6 표의 우리 값 10 개가 원장과 같고, 미재현 값은 자기 id 를 단 요소 **안**에
    텍스트 표식과 같이 있다 (근처 ⛔ 는 결속이 아니다 — CLAUDE.md 화면 규율)."""
    rec = json.loads(GAP_RESULT.read_text("utf-8"))
    sec = _section(_report_html(client), "s6")
    assert "아직 없다" not in sec, "§6 이 아직 9/10 이다"
    for r in rec["rows"]:
        assert f"{r['gap_eV']:.3f}" in sec, f"{r['phase']} 우리 값 {r['gap_eV']} 이 §6 에 없다"
    nd = [r for r in rec["rows"] if r["phase"] == "NdP5O14"][0]
    assert abs(nd["gap_eV"] - 5.393) < 1e-6 and "⛔" in nd, "원장의 NdP5O14 행이 바뀌었다 — 시험이 헛것을 재고 있다"
    rows = re.findall(r'<tr data-claim="%s">(.*?)</tr>' % _NDP_HZ, sec, re.S)
    assert len(rows) == 1 and "5.393" in rows[0], "미재현 값이 자기 id 요소 안에 없다"
    assert '<span class="claim-mark">[미재현]</span>' in rows[0], "표식이 텍스트 노드가 아니다"
    assert "0.053" in sec and "10/10" in sec


def test_s6_prediction_failure_is_recorded_and_threshold_not_moved(client):
    """양성+음성 — 등록 예측(6.33–6.46)이 지워지지 않았고, 틀렸다고 적혀 있고, 문턱을 안 옮겼다.
    실패한 예측을 '재현' 으로 읽게 하는 문장이 없다."""
    sec = _section(_report_html(client), "s6")
    assert "6.33 ~ 6.46" in sec, "등록 예측이 지워졌다 — 사후해석이 된다"
    assert "예측이 틀렸다" in sec and "문턱을 옮기지 않는다" in sec
    assert "부피 가설은 반증됐다" in sec and "9.42" in sec
    assert "축합될수록 갭이 넓어진다" in sec and "쓰지 않는다" in sec
    assert "10/10 재현" not in sec and "10 종 재현" not in sec and "10 종 전부 재현" not in sec


def test_ndp5o14_hazard_registered_bound_and_ledger_valid(client):
    """양성 — 인용위험 원장에 CONDITIONAL 항목이 있고, 원장 검사가 0 이고, 화면이 그 id 로
    두 자리(표 행 · 예측 카드)에서 결속하며, §9 도 같은 id 를 이름으로 댄다."""
    hz = json.loads(HAZARDS.read_text("utf-8"))["hazards"]
    z = [x for x in hz if x.get("id") == _NDP_HZ]
    assert len(z) == 1 and z[0]["level"] == "CONDITIONAL" and "5.393" in z[0]["what"]
    from webapp import canonical as C
    assert C.validate_hazards() == [], C.validate_hazards()
    h = _report_html(client)
    assert h.count(f'data-claim="{_NDP_HZ}"') >= 2, "표 행과 예측 카드 둘 다 결속돼야 한다"
    assert h.count('<span class="claim-mark">[미재현]</span>') >= 2
    assert _NDP_HZ in _section(h, "s9")


def test_s9_count_matches_tldr_and_gist(client):
    """양성 — §9 항목 수가 TL;DR 과 요지 줄에 적힌 개수와 같다 (25 로 굳어 있던 사고 방지)."""
    h = _report_html(client)
    s9 = _section(h, "s9")
    n = s9.count('<li><span class="no">⛔</span>')
    m1 = re.search(r"⛔ 말하지 않는 것 <span class=\"mono\">— 전체 (\d+) 개는", h)
    m2 = re.search(r"<b>금지 서술 (\d+) 개</b>", s9)
    assert m1 and m2, "개수 표기를 못 찾았다 — 시험이 헛것을 재고 있다"
    assert int(m1.group(1)) == n == int(m2.group(1)), (m1.group(1), n, m2.group(1))
    for must in ("6.6 배", "Xiao 2019", _NDP_HZ):
        assert must in s9, f"§9 에 {must!r} 항목이 없다"


def test_s0_onset_table_matches_the_esw_record(client):
    """양성 — §0 자가반증 표의 onset 이 esw 원장 값 그대로이고, 부제가 '창' 이 아니라 '열화 억제' 다."""
    esw = json.loads(ESW.read_text("utf-8"))["results"]
    h = _report_html(client)
    s0 = _section(h, "s0")
    for lab in ("comp1", "modelc", "lpsocl", "modelc_nd"):
        row = re.search(r'<tr><td class="mono">%s \([^<]*</td>(.*?)</tr>' % lab, s0, re.S)
        assert row, f"§0 표에 {lab} 행이 없다"
        cells = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row.group(1), re.S)]
        assert float(cells[0]) == esw[lab]["oxidation_limit_V"], (lab, cells)
        assert float(cells[1]) == esw[lab]["reduction_limit_V"], (lab, cells)
    assert "1.92" in s0 and "좁힌다" in s0 and "Banik" in s0
    assert "고전압 양극 계면 열화 억제" in h[:h.index('<ul class="toc">')], "부제가 아직 '안정성 개선' 이다"


# ── 보호율 게이트의 분모 (2026-09-21) ───────────────────────────────────────
#   왜 생겼나: 화면이 5 곳에서 "24 칸 중 12 탈락" 이라 적었는데 24 가 CSV 에서
#   유도되지 않았다. 추적해 보니 **선행 지표**(cei_tm_fate, 4 양극 × 6 전압 = 24)의
#   격자 수가 산문으로 옮겨와 **다른 표의 분모**가 돼 있었다. 한 기록 안에 두 분모가
#   있으면 산문은 가까운 쪽을 집어 간다 — 그래서 CSV 에 값으로 묶는다.
#   2026-09-21 재결속: 34 행 부분 라운드 → **전조건 라운드 120 행**(4 × 6 × 5).
#   옛 CSV 는 정정 기록이 가리키는 역사라 지우지 않고, 화면의 현재 숫자는 새 CSV 에 묶는다.
PROT_CSV = REPORT.parent / "cei_nd_protection_curve.csv"
PROT_CSV_ALL = REPORT.parent / "cei_nd_protection_allcells.csv"


def _prot_rows(path=None):
    import csv as _csv
    return list(_csv.DictReader((path or PROT_CSV_ALL).open(encoding="utf-8")))


def _prot_counts(rows):
    n_all = len(rows)
    n_fail = sum(1 for r in rows if r["gate_pass"] == "False")
    n_pass = sum(1 for r in rows if r["gate_pass"] == "True")
    cols = {(r["cathode"], r["voltage_V"]) for r in rows}
    full = {c for c in cols
            if all(r["gate_pass"] == "True" for r in rows
                   if (r["cathode"], r["voltage_V"]) == c)}
    return n_all, n_pass, n_fail, len(cols), full


def test_protection_gate_denominator_matches_the_csv(client):
    """양성 — 화면이 인용하는 분모·탈락·통과·열수가 전부 **전조건 CSV** 에서 나온다.

    ⚠ 맨 숫자로 재지 않는다. 첫 판은 `re.search(r"\\b7\\b", h)` 였는데 "7" 은 이 페이지
    어디에나 있어서 **열 수를 지워도 통과했다**(2026-09-21 break-verify 에서 잡았다).
    그래서 숫자를 **자기 문맥에 묶어** 찾는다.
    """
    rows = _prot_rows()
    n_all, n_pass, n_fail, n_col, full = _prot_counts(rows)
    n_full = len(full)
    assert n_all == n_pass + n_fail, "gate_pass 가 True/False 말고 다른 값을 갖는다"
    h = _report_html(client)
    need = {
        "본문 분모":      f"잰 <b>{n_all} 칸</b>",
        "본문 탈락":      f"중 <b>{n_fail} 칸</b>이",
        "본문 통과":      f"(통과 <b>{n_pass}</b>)",
        "본문 열수":      f"열 <b>{n_col} 개</b> 중 다섯 농도를 전부 통과한 것은 <b>{n_full} 개</b>",
        "TL;DR 칸수":     f"전조건 라운드(<b>{n_all} 칸</b>",
        "TL;DR 열수":     f"열 <b>{n_col} 개 중 {n_full} 개</b>가 전 농도 통과",
        "요지줄":         f"<b>{n_all} 칸</b> 전조건에서 열 <b>{n_col} 중 {n_full}</b> 통과",
        "§9":             f"잰 <b>{n_all} 칸</b> 중 <b>{n_fail} 칸</b>이 탈락했다(통과 {n_pass} · 열 {n_col} 개)",
        "영문 캡션":      f"Of {n_all} measured cells, {n_fail} fail",
        "영문 캡션 열":   f"of the {n_col} (cathode, voltage) columns, {n_full} pass at every",
    }
    missing = [k for k, v in need.items() if v not in h]
    assert not missing, f"CSV 수가 화면의 그 자리에 없다: {missing}"

    #: NMC811 6/6 은 이 개정의 표제다 — 자료에서 세고, 화면 문구와 맞춘다
    nmc = sorted(v for c, v in full if c == "NMC811")
    assert len(nmc) == 6, f"NMC811 전 농도 통과 열이 {len(nmc)} 개다 — 화면은 6 이라 적었다"
    assert "<b>NMC811 은 6 전압 전부</b>" in h

    #: 식이 잘 맞는 세 열은 이름으로 화면에 있어야 한다
    for cath, volt in [("LiCoO2", "4.3"), ("LiNiO2", "3.5"), ("NMC811", "3.5")]:
        assert (cath, volt) in full, f"{cath} {volt} V 가 CSV 에서 전 농도 통과가 아니다"
        sub = cath.replace("LiCoO2", "LiCoO₂").replace("LiNiO2", "LiNiO₂")
        assert f"{sub} {float(volt):.2f} V" in h, f"통과 열 {cath} {volt} V 가 화면에 없다"


def test_undefined_protection_columns_are_not_drawn_as_zero(client):
    """양성 — 보호율이 **정의되지 않는** 열(양쪽 다 TM 인산염 없음)을 0 으로 말하지 않는다.

    repo 규율: "화면·출력에서 없는 값을 0 으로 그리지 않는다". 여기선 그 열이 몇 개인지를
    자료에서 세고, 화면이 같은 수를 **'정의되지 않는다'** 라고 적었는지 본다.
    """
    rows = _prot_rows()
    _, _, _, _, full = _prot_counts(rows)
    undef = sorted(c for c in full
                   if all((r["protection_observed"] or "").strip() == ""
                          for r in rows if (r["cathode"], r["voltage_V"]) == c))
    assert undef, "정의되지 않는 열이 자료에 없다 — 시험이 헛것을 잰다"
    h = _report_html(client)
    #: ⛔ 열 **이름도** 자료에서 만든다. 개수만 맞으면 통과하던 시험이었다
    #  (2026-09-21 외부 리뷰: 미정의 열을 다른 열로 바꿔도 5 만 맞으면 통과했다).
    sub = {"LiCoO2": "LiCoO₂", "LiNiO2": "LiNiO₂", "LiMnO2": "LiMnO₂"}
    by_cat = {}
    for c, v in sorted(undef):
        by_cat.setdefault(sub.get(c, c), []).append(f"{float(v):.1f}")
    want = " · ".join(f"{k} {'·'.join(vs)}" for k, vs in by_cat.items()) + " V"
    assert f"<b>{len(undef)} 개</b>({want})" in h, \
        f"미정의 열 목록이 자료와 다르다 — 자료는 {want!r}"
    assert "보호율이 <b>정의되지 않는다</b>" in h
    assert "<b>0 이 아니라 빈칸(&#8212;)</b> 으로 둔다" in h
    #: 예측선 CSV 는 (a) 가 그리는 세 곡선과 열 수가 같아야 한다 — 조용히 빠진 적이 있다
    hdr = (REPORT.parent / "cei_nd_protection_fig.csv").read_text("utf-8").splitlines()[0]
    assert hdr.count(",") == 3, f"예측선 CSV 열이 {hdr.count(',')} 개다 — 곡선 셋과 안 맞는다"
    for tag in ("LiCoO2_4.3V", "LiNiO2_3.5V", "NMC811_3.5V"):
        assert tag in hdr, f"예측선 CSV 에 {tag} 열이 없다"


def test_the_rule_counts_phosphorus_but_the_measurement_counts_tm(client):
    """양성 — 이 라운드가 새로 알려준 **조건**이 화면에 결속돼 있다.

    저전압 NMC811 은 도핑·대조의 TM-인산염 몫이 둘 다 0.100(= Mn 분율)이라 보호율이 0 이다.
    수치를 CSV 에서 읽어 화면 문구와 맞춘다 — 산문만 고치고 자료가 안 바뀌는 일을 막는다.
    """
    rows = _prot_rows()
    zero = [r for r in rows if r["cathode"] == "NMC811"
            and r["voltage_V"] in ("2.5", "3.0")]
    assert len(zero) == 10, len(zero)
    vals = {round(float(r["tm_phosphate_share"]), 3) for r in zero} | \
           {round(float(r["tm_phosphate_share_control"]), 3) for r in zero}
    assert vals == {0.100}, f"NMC811 저전압 TM-인산염 몫이 {vals} 다 — 0.100 바닥이 아니다"
    assert all(abs(float(r["protection_observed"])) < 1e-9 for r in zero)
    h = _report_html(client)
    assert "둘 다 0.100" in h and "Mn 분율" in h, "Mn 바닥 설명이 화면에 없다"
    assert "<b>식은 P 를 세고 실측은 TM 을 센다</b>" in h, "요지줄에 조건이 없다"
    assert "예측 보호율과 실측 보호율을 같은 양으로 쓰기" in _section(h, "s9"), \
        "§9 에 새 금지 항목이 없다"


def test_deviation_tiers_match_the_csv(client):
    """양성 — "식이 잘 맞는 열" 의 **문턱과 식구**가 CSV 에서 나온다.

    왜 생겼나: 처음엔 세 열을 "≤2.5 %p" 라고 적었는데 그중 LiNiO₂ 3.50 V 가 **3.1 %p** 였다.
    셋 중 제일 나쁜 값을 문턱으로 써야 하는데 둘째 값을 썼다 — 산문이 자료보다 좋게 들렸다.
    그리고 **오차 0.0 %p 인 열이 하나 더 있는데 그건 일치가 아니다**(예측도 실측도 0).
    """
    rows = _prot_rows()
    _, _, _, _, full = _prot_counts(rows)

    def _f(v):
        v = (v or "").strip()
        return None if v == "" else float(v)

    #: ⛔ 2026-09-21 정정 (외부 리뷰). 첫 판은 `P_taken_by_Nd` 와 뺐다 — **식의 오차가 아니다**.
    #  hull 이 식보다 Nd 를 덜 쓰는 칸에서 갈린다(NMC811 4.00 V: 5.49 대 14.63 %p).
    #  식을 평가하는 자리이므로 예측식 min(1, k·x/(1−x)) 로 잰다. 원장과 같은 기준이다.
    def _pred(r):
        k, x = _f(r["k_observed"]), _f(r["x_Nd"])
        return None if k is None else min(1.0, k * x / (1 - x))

    dev, noк = {}, set()
    for c in full:
        sub = [r for r in rows if (r["cathode"], r["voltage_V"]) == c]
        ds = [abs(_f(r["protection_observed"]) - _pred(r)) * 100 for r in sub
              if _f(r["protection_observed"]) is not None and _pred(r) is not None]
        if not ds:
            #: k 가 아예 없는 열 — Nd 인산염이 안 나온다. 식과 견줄 수 없다(0 = 0 은 일치가 아니다)
            if any(_f(r["protection_observed"]) is not None for r in sub):
                noк.add(c)
            continue
        dev[c] = max(ds)

    #: 원장과 **같은 값**이어야 한다 — 화면·그림·원장이 세 갈래로 갈리는 것을 막는다
    led = json.loads((REPORT.parents[3] /
                      "db/properties/cei_protection_allcells_result_2026_09_21.json"
                      ).read_text("utf-8"))["★_식_vs_실측_열별_오차_%p"]
    for c, d in dev.items():
        key = f"{c[0]}@{float(c[1]):.2f}V"
        assert key in led, f"원장에 {key} 가 없다"
        assert abs(led[key]["최대"] - round(d, 2)) < 0.011, (key, led[key]["최대"], d)
    assert len(dev) == len(led) == 11, (len(dev), len(led))
    assert noк == {("LiMnO2", "3.5")}, sorted(noк)

    h0 = _report_html(client)
    assert "식과 견줄 수 있는 <b>11 개</b>" in h0
    assert "LiMnO₂ 3.50 V 는 여기 없다" in h0, "k 없는 열을 뺐다는 말이 화면에 없다"
    assert "14.6 %p" in h0, "식 기준과 P_taken 기준이 갈리는 칸을 화면이 안 밝힌다"

    good = sorted(c for c in dev if dev[c] <= 3.11)
    assert good == [("LiCoO2", "4.3"), ("LiNiO2", "3.5"), ("NMC811", "3.5")], good
    thresh = max(dev[c] for c in good)
    h = _report_html(client)
    assert f"<b>≤{thresh:.1f} %p</b>" in h, \
        f"문턱이 셋 중 **제일 나쁜** 값({thresh:.1f})으로 적혀 있지 않다"
    assert "≤2.5 %p" not in h, "옛 문턱(둘째로 나쁜 값)이 남아 있다"

    #: 계층은 **여집합**으로 센다. 25.0 문턱으로 세면 24.9999 인 NMC811 3.00 V 가 빠진다
    #  (첫 판에서 실제로 빠졌다) — 사소한 부동소수 경계가 산문의 수를 바꾸면 안 된다.
    mid = sorted(c for c in dev if 3.11 < dev[c] <= 8.85)
    odd = sorted(c for c in dev if 8.85 < dev[c] < 20)
    worst = sorted(c for c in dev if dev[c] >= 20)
    assert len(mid) == 2, sorted((c, round(dev[c], 1)) for c in mid)
    assert len(odd) == 1 and odd[0] == ("NMC811", "4.0"), odd
    assert len(worst) == 5, sorted((c, round(dev[c], 1)) for c in worst)
    assert f"<b>≤{max(dev[c] for c in mid):.1f} %p</b> 둘" in h
    assert f"<b>{dev[odd[0]]:.1f} %p</b> 하나" in h, f"14.6 계층이 화면에 없다 ({dev[odd[0]]:.4f})"
    assert f"나머지 <b>다섯</b>이 <b>25~{max(dev.values()):.0f} %p</b> 어긋난다" in h


def test_resume_block_does_not_carry_retracted_numbers(client):
    """양성 — 새 세션이 **먼저 읽는** kb/open_items.md ⏭ 블록이 화면과 같은 수를 말한다.

    왜 생겼나: 화면의 오차 문턱을 2.5 → 3.1 로 고쳤는데 ⏭ 블록에는 2.5 가 남았다
    (2026-09-21 외부 리뷰). CLAUDE.md 가 모든 새 세션을 이 블록으로 보내므로,
    여기가 낡으면 다음 사람이 **철회된 값을 되살린다** — band gap 줄에서 이미 겪은 실패다.
    그래서 산문끼리가 아니라 **CSV → 화면 → ⏭** 세 곳을 같은 수에 묶는다.
    """
    rows = _prot_rows()
    n_all, n_pass, n_fail, n_col, full = _prot_counts(rows)
    blk = (REPORT.parents[3] / "kb/open_items.md").read_text("utf-8")
    i = blk.find("### ⏭-NOW-t")
    assert i >= 0, "⏭-NOW-t 블록이 없다 — 이 시험이 헛것을 잰다"
    j = blk.find("### ⏭-NOW-s", i)
    blk = blk[i: j if j > 0 else len(blk)]

    for must in (f"집계: {n_all} 칸 중 **탈락 {n_fail}**(통과 {n_pass})",
                 f"열 **{n_col} 중 {len(full)}** 전 농도 통과"):
        assert must in blk, f"⏭ 블록에 {must!r} 가 없다 — 화면과 갈렸다"

    #: 철회된 문턱이 **주장으로** 되살아나면 잡는다 (리뷰 이력으로 언급하는 것은 허용)
    assert "식이 **≤2.5 %p** 로 맞는" not in blk, \
        "⏭ 블록이 철회된 문턱 2.5 %p 를 다시 주장한다"
    assert "식이 **≤3.1 %p** 로 맞는 열은 **셋뿐**" in blk, "⏭ 블록에 현행 문턱이 없다"

    #: 시험 개수도 실물과 맞춘다 — "62 → 65" 로 적어 두고 66 개였다
    n_tests = sum(1 for ln in (REPORT.parents[3] /
                               "webapp/tests/test_interpretation_cards.py"
                               ).read_text("utf-8").splitlines()
                  if ln.startswith("def test_"))
    assert f"**62 → {n_tests}**" in blk, f"⏭ 블록의 시험 개수가 실물({n_tests})과 다르다"


def test_non_monotonic_column_is_flagged_and_no_gate_was_added(client):
    """양성 — LiMnO₂ 3.00 V 가 단조롭지 않다는 사실과, **게이트를 지금 넣지 않았다**는 사실 둘 다.

    ⚠ 두 번째가 핵심이다. 결과를 보고 문턱을 만들면 사전등록이 죽는다 — 그래서 동결된
    게이트가 셋 그대로인지도 기록에서 확인한다.
    """
    rows = _prot_rows()
    seq = [float(r["protection_observed"]) for r in
           sorted((r for r in rows if r["cathode"] == "LiMnO2" and r["voltage_V"] == "3.0"),
                  key=lambda r: float(r["x_Nd"]))]
    assert any(b < a for a, b in zip(seq, seq[1:])), f"{seq} 가 단조증가다 — 시험이 헛것을 잰다"
    h = _report_html(client)
    #: ⛔ 수열을 **자료에서 만든다**. 고정 문자열로 두면 CSV 가 바뀌어도 옛 수열이 있는
    #  화면을 통과시킨다 (2026-09-21 외부 리뷰: 1.5 → 20 으로 바꿔도 통과했다).
    seq_txt = " → ".join(f"{round(v * 100, 1):g}" for v in seq) + " %"
    assert seq_txt in h, f"화면의 수열이 자료와 다르다 — 자료는 {seq_txt!r}"
    assert "단조성 게이트를 지금 넣지 않는다" in h, "게이트를 안 넣었다는 기록이 화면에 없다"

    #: 몇 개인지도 자료에서 센다. 처음엔 화면이 **하나만** 적었는데 실제로는 셋이었다
    #  (탐지기를 쓰고서야 알았다) — 수를 자료에 묶어 다시 벌어지지 않게 한다.
    #  ⚠ 범위는 **전 농도 통과 열**이다. 안 적으면 3 과 5 가 갈린다 — 통과·탈락이 섞인
    #  열은 남은 점이 성긴 것이지 단조롭지 않은 것이 아니다.
    _, _, _, _, full_cols = _prot_counts(rows)
    nm = set()
    for c in full_cols:
        ys = [float(r["protection_observed"]) for r in
              sorted((r for r in rows if (r["cathode"], r["voltage_V"]) == c),
                     key=lambda r: float(r["x_Nd"]))
              if (r["protection_observed"] or "").strip() != ""]
        if any(b < a - 1e-9 for a, b in zip(ys, ys[1:])):
            nm.add(c)
    assert len(nm) == 3, f"단조롭지 않은 열이 {len(nm)} 개다 — 화면은 셋이라 적었다: {sorted(nm)}"
    assert f"<b>통과 열 {len(full_cols)} 개 중 단조롭지 않은 열이 셋</b>" in h, \
        "화면이 그 수를(범위와 함께) 적지 않았다"
    for cath, volt in sorted(nm):
        sub = cath.replace("LiMnO2", "LiMnO₂")
        assert f"{sub} {float(volt):.2f}" in h, f"{cath} {volt} V 가 화면에 없다"
    rec_nm = json.loads((REPORT.parents[3] /
                         "db/properties/cei_protection_allcells_result_2026_09_21.json"
                         ).read_text("utf-8")).get("⭐_추가_2026_09_21_단조성_탐지", {})
    assert set(rec_nm.get("열", {})) == {f"{c}@{float(v):.2f}V" for c, v in nm}, \
        "원장의 단조성 덧댐이 자료와 다르다"
    rec = json.loads((REPORT.parents[3] /
                      "db/properties/cei_protection_allcells_result_2026_09_21.json"
                      ).read_text("utf-8"))
    assert set(rec["gates_frozen"]) >= {"G1_dx_max", "G2", "G3"}, rec["gates_frozen"]
    assert rec["gates_frozen"]["G1_dx_max"] == 0.05, "동결 게이트 문턱이 바뀌었다"
    assert not any("단조" in k for k in rec["gates_frozen"]), \
        "결과를 본 뒤 단조성 게이트가 들어갔다 — 사전등록이 죽는다"


def test_old_24_denominator_survives_only_as_a_struck_correction(client):
    """⛔음성 — 옛 분모 24 가 **정정 표지 없이** 되돌아오면 잡는다.

    지우는 것이 아니라 취소선으로 남기는 것이 이 repo 규약이다(무엇이 틀렸는지가 기록).
    그래서 '사라졌나' 가 아니라 '표지 안에만 있나' 를 잰다.
    """
    h = _report_html(client)
    assert "24 cells" not in h, "영문 캡션에 옛 분모가 남아 있다"
    hits = [m.start() for m in re.finditer("24 칸", h)]
    assert len(hits) == 1, f"'24 칸' 이 {len(hits)}곳 — 정정 표지 하나만 남아야 한다"
    around = h[max(0, hits[0] - 120): hits[0] + 60]
    assert "<s>" in around and "분모 정정" in around, \
        "남은 '24 칸' 이 취소선·정정 표지 안에 있지 않다"
    #: 같은 날 전조건 라운드가 24 를 **열의 개수로는** 되살렸다. 두 층이 다 있어야 한다 —
    #  정정만 남으면 다음 사람이 24 라는 수 자체를 금지된 것으로 읽는다.
    assert "2026-09-21 2차 갱신" in h and "지금은 24 가 맞다 — 열의 개수로서" in h, \
        "정정 뒤 전조건 라운드가 24 를 열 수로 되살린 기록이 없다"
    old_rows = _prot_rows(PROT_CSV)
    assert len(old_rows) == 34, "옛 34 행 CSV 가 사라졌다 — 정정 기록이 가리키는 역사다"
    rec = json.loads((REPORT.parents[3] /
                      "db/properties/cei_nd_p_capture_result_2026_09_18.json").read_text("utf-8"))
    assert "⛔_정정_2026_09_21_24_칸_의_분모" in rec, "원장에 정정 주석이 없다"
    assert "24 칸" in json.dumps(rec, ensure_ascii=False), \
        "원장 원문이 덮어써졌다 — 정정은 덮어쓰기가 아니다"


def test_title_no_longer_claims_the_retracted_sink(client):
    """⛔음성 — 철회된 문장("NdPO₄ 가 Li₃PO₄ 보다 깊은 P 싱크")의 축약이 제목으로 돌아오면 잡는다."""
    h = _report_html(client)
    m = re.search(r"<h1>(.*?)</h1>", h, re.S)
    assert m, "h1 을 못 찾았다 — 시험이 헛것을 재고 있다"
    assert "싱크" not in m.group(1), f"제목이 다시 '싱크' 를 주장한다: {m.group(1)!r}"
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    assert t and "Sink" not in t.group(1), f"탭 제목이 아직 Sink 다: {t and t.group(1)!r}"
    assert "+1.5035" in h, "§3 의 철회 근거가 화면에서 빠졌다 — 제목만 고치면 반쪽이다"


# ── §0 산화 기전 (2026-09-21) ────────────────────────────────────────────────
#   왜 생겼나: §0 이 "onset 이 안 움직인다" 는 **사실**만 싣고 **왜**를 안 실었다.
#   1저자가 발표 준비 중에 물었고(2026-09-21), 근거는 이미 repo 에 있었다 —
#   우리 PDOS 밴드 가장자리 성분과 ESW 반응식. 화면에 없으면 사람은 문헌만 인용한다.
PDOS_EDGE = REPORT.parents[3] / "db/properties/pdos_band_edge_composition_2026_09_14.json"


def test_s0_vbm_composition_matches_the_pdos_record(client):
    """양성 — §0 의 VBM/CBM 성분이 원장 값 그대로다 (숫자를 화면이 자체 보관하지 않는다)."""
    rows = {r["label"]: r for r in json.loads(PDOS_EDGE.read_text("utf-8"))}
    s0 = _section(_report_html(client), "s0")
    for lab in ("modelc_undoped", "ndo_lpscl16_n5fu"):
        for edge in ("VBM_composition_pct", "CBM_composition_pct"):
            for el, pct in rows[lab][edge].items():
                assert f"{pct:.2f}" in s0, f"{lab} {edge} {el} {pct} 이 §0 에 없다"
    # 논지 문장: 산화는 S 에서 시작, Nd 는 CBM 쪽
    assert "산화 개시 자리는 S 쪽" in s0
    assert "frozen-4f" in s0 and "산화수" in s0, "4f 한정이 빠졌다 — 산화수 주장 금지의 근거다"
    assert "절대 위치" in s0 and "정렬" in s0, "VBM 절대 위치 비교 금지가 빠졌다"


def test_s0_nd_s_channel_reactions_match_the_esw_record(client):
    """양성 — Nd 가 onset 을 내리는 기전(Nd–S 채널)이 반응식과 함께 실려 있다."""
    esw = json.loads((REPORT.parents[3] /
                      "db/properties/cei_esw_Li_2026_09_16.json").read_text("utf-8"))["results"]
    s0 = _section(_report_html(client), "s0")
    assert "Nd₁₀S₁₉" in s0 and "LiS₄" in s0, "산화 onset 산물이 바뀐다는 사실이 화면에 없다"
    assert "Nd₂S₃" in s0, "환원 쪽 Nd 산물이 없다"
    # 창 폭이 두 원장값에서 나온다
    w0 = esw["modelc"]["oxidation_limit_V"] - esw["modelc"]["reduction_limit_V"]
    w1 = esw["modelc_nd"]["oxidation_limit_V"] - esw["modelc_nd"]["reduction_limit_V"]
    assert f"{w0:.3f}" in s0 and f"{w1:.3f}" in s0, f"창 폭 {w0:.3f}/{w1:.3f} 이 화면에 없다"
    # 해석과 측정을 갈라 적었는가
    assert "해석" in s0 and "측정된 것은" in s0, "'황친화' 가 해석이라는 구분이 없다"


def test_s0_refuses_to_harden_the_0p22V_and_to_call_nd_passivating(client):
    """⛔음성 — 0.22 V 를 단단한 값으로 쓰거나 Nd 산물을 부동태라 부르면 잡는다."""
    s0 = _section(_report_html(client), "s0")
    assert "뒤집히는 크기" in s0, "0.22 V 가 hull 오차로 뒤집힌다는 한정이 없다"
    assert "0.76" in s0 and "Nd₂S₃" in s0, "산화 쪽 Nd 산물이 샌다는 반대 증거가 없다"
    assert "부동태가 아니다" in s0, "'Nd 가 부동태를 만든다' 부인이 없다"


def test_s0_separates_thermodynamic_window_from_measured_CV(client):
    """양성+음성 — 열역학 창과 CV·LSV 실효 창을 같은 양으로 놓지 않는다.

    이 구분이 없으면 '계산은 창이 좁아진다는데 실험 CV 는 좋아진다' 가 모순으로 읽힌다.
    """
    h = _report_html(client)
    s0 = _section(h, "s0")
    assert 'data-claim="cei.esw.not_cv"' in s0, "CV 구분 상자가 자기 id 로 결속돼 있지 않다"
    assert '<span class="claim-mark">[다른 양]</span>' in s0, "표식이 텍스트 노드가 아니다"
    for must in ("열역학 창", "실효 창", "자기제한", "충분조건이 아니다"):
        assert must in s0, f"§0 에 {must!r} 가 없다"
    # §9 에도 같은 금지가 이름을 대고 있어야 한다
    s9 = _section(h, "s9")
    assert "CV·LSV" in s9 and "직접 비교" in s9, "§9 에 CV 비교 금지 항목이 없다"
    assert "ndo_passivation_argument_2026_09_14" in s0, "해석 카드 포인터가 없다"


def test_s0_scopes_the_esw_to_the_Li_site_cell(client):
    """⛔음성 — Li 자리 x=0.20 결과가 P 자리 x=0.02 이야기로 조용히 번지면 잡는다."""
    s0 = _section(_report_html(client), "s0")
    assert "Li 자리에 있는 셀" in s0 and "0.20" in s0, "ESW 셀이 Li 자리 x=0.20 이라는 한정이 없다"
    assert "P 자리" in s0 and "부호가 반대" in s0, "P 자리로 못 옮긴다는 이유가 없다"
