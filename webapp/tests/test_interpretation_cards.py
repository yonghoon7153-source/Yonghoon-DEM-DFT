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
