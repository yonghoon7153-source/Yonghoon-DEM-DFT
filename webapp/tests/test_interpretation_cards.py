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
    # 2026-09-28 — x = 0.02 전환으로 §1 의 판정 문장이 바뀌었다 (옛 "24 조건이 개별로도" → 칸별 잔차).
    assert "칸별 최대 |잔차|도" in body, "§1 보강 문장(x = 0.02 칸별 잔차)이 화면에 없다"


def test_report_images_are_served_relative_to_it(client):
    """양성 — 그림도 같은 경로에서 온다 (상대 src 가 풀린다)."""
    for name in ("cei_nd_o_decomposition_x002.png", "cei_nd_o_decomposition.png",
                 "cei_nd_o_decomposition_x002_si.png", "cei_nd_phase_x002.png"):
        r = client.get(f"/api/file/db/properties/cei_figs/{name}")
        assert r.status_code == 200 and r.data[:4] == b"\x89PNG", f"{name} 가 안 온다"


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
    """⛔음성 — 분해 절(§S1 · id="s1")의 읽는 순서를 고정한다 (1저자 지정, 2026-09-17).

    그림 → "Fig. S1 을 읽는 법" → "세로축의 reaction energy 는 무엇인가".
    정의 상자가 앞으로 올라오면 독자가 그림에 닿기 전에 벽을 만난다.
    셋 다 그 절 안에 있어야 한다 — 절 밖으로 밀려나면 그것도 잡는다.
    2026-09-29 — 1저자 'si 쪽으로': 이 절은 SI 자리(§8 뒤)로 옮겼고 그림은 Fig. S1 (a)(b) 다.
    기계 id 는 s1 그대로다 (원장·시험·링크가 끊기지 않게). 끝 표식은 §2 가 아니라 **그 절의 끝**이다.
    """
    h = _report_html(client)
    s1 = h.index('<section id="s1"')
    marks = {
        "figure":     h.find('<img src="cei_nd_o_decomposition_x002_si.png"', s1),
        "howto":      h.find("Fig. S1 을 읽는 법", s1),
        "definition": h.find("세로축의 <span", s1),
        "s1_end":     h.find("</section>", s1),
    }
    missing = [k for k, v in marks.items() if v < 0]
    assert not missing, f"§S1 에서 못 찾은 표식: {missing} — 시험이 헛것을 재고 있다"
    order = sorted(marks, key=marks.get)
    assert order == ["figure", "howto", "definition", "s1_end"], \
        f"§S1 순서가 바뀌었다: {' → '.join(order)}"


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
    assert 'src="cei_p_host_ladder_x002.png"' in h, "Fig. 2 (사다리 · x = 0.02) 가 화면에 없다"
    r = client.get(LOCAL_REPORT.rsplit("/", 1)[0] + "/cei_p_host_ladder_x002.png")
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


_IDENTITY_DECISION = "D-2026-09-28-cei-li-ledger-identity"


def test_slope_mechanism_stays_forbidden_on_both_surfaces(client):
    """⛔음성 — **풀리지 않은 것**이 풀린 것처럼 보이면 잡는다.

    자리 판정은 해제됐지만, 전압 기울기를 '예측으로 검증된 기전' 이나 'Nd 화학의 효과' 로 쓰는 것은
    여전히 금지다. 해제가 통째로 번지는 것이 제일 흔한 사고다.
    2026-09-29 개정 — 1저자가 항등식 결정(D-2026-09-28-cei-li-ledger-identity)을 비준했다 ('권고하는걸로 해줘'):
    기울기 = 방출 Li 는 계산 방식의 항등식이라 '검증 전' 딱지를 걷고 '항등식' 으로 적는다. 사전등록 예측의
    실패 기록(부호가 틀렸다)은 남긴다. 두 화면(보고서 · Nd 카드)이 같은 상태를 말해야 한다 — 한쪽만 고치면 잡는다.
    잡는 것: 비준 전인데 '항등식' 으로 적기 · 옛 '검증 전' 딱지가 기울기 설명에 남기 · 09-19 직선 계수(β) 인용 ·
      'Nd 화학의 효과로 읽지 않는다' 금지가 빠지기.
    """
    import json as _json
    rec = _json.loads(SITE_RESULT.read_text(encoding="utf-8"))
    assert any("기울기" in x and "⛔" in x for x in rec["금지_서술"]), \
        "원장 금지 목록에 기울기 항목이 없다 — 시험이 헛것을 재고 있다"
    ds = {d["id"]: d for d in _json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]}
    dec = ds.get(_IDENTITY_DECISION) or {}
    assert dec.get("decision_state") == "active" and (dec.get("ratification") or {}).get("state") == "ratified", \
        "항등식 결정이 비준되지 않았는데 화면이 '항등식' 으로 적는다"
    h = _report_html(client)
    blob = json.dumps(V.interpretation_cards_for(ND), ensure_ascii=False)
    assert "부호가 틀렸고" in h, "보고서가 사전등록 예측의 실패 기록을 안 싣는다"
    for name, text in (("보고서", h), ("Nd 카드", blob)):
        assert "항등식" in text, f"{name}: 기울기 = 방출 Li 를 항등식으로 적지 않았다"
        assert "Nd 화학" in text, f"{name}: 기울기를 Nd 화학의 효과로 읽지 말라는 금지가 없다"
        assert "2.0051" not in text, f"{name}: 09-19 직선의 계수(β)를 싣는다 — 물리 계수가 아니다"
        stale = [m.start() for m in re.finditer("검증 전", text)
                 if re.search("기울기|Li 장부|dΦ/dV|방출 Li", text[max(0, m.start() - 200): m.start() + 60])]
        assert not stale, f"{name}: 기울기 설명에 옛 '검증 전' 딱지가 남았다 ({len(stale)} 곳)"


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


def test_fig_s1_decomposition_is_si_two_panels(client):
    """양성+음성 — 분해 그림은 **SI** 다: Fig. S1 · 두 패널 (a)(b) · SI 자리(§8 뒤)
    (1저자 2026-09-29 *'ㅇㅇ si 쪽으로 가는게 좋을듯 · 둘다 해줘'* · 원고 틀 카드).
    옛 3 패널 PNG 는 이력 파일로 남지만 **페이지에는 안 걸린다**. 캡션은 취소선 철회문 없이 서고,
    철회 표지는 한글 '읽는 법' 상자에 ⛔ 로 있다 (그림은 복사될 때 캡션을 안 데려간다).
    잡는 것: 옛 3 패널이 다시 걸림 · 절이 본문 자리로 돌아옴 · SI 판이 두 패널이 아님 · 철회 표지·Li 맞춤 범위 빠짐."""
    h = _report_html(client)
    assert '<img src="cei_nd_o_decomposition_x002.png"' not in h, "옛 3 패널이 페이지에 다시 걸렸다"
    s1 = _section(h, "s1")
    head = s1[:s1.index("</h2>")]
    assert "S1." in head and "보충" in head, f"§S1 제목이 아니다: {head[-120:]}"
    order = re.findall(r'<section id="(\w+)" class="sec">', h)
    assert order.index("s8") < order.index("s1") < order.index("s8b"), f"§S1 이 SI 자리(§8 뒤)가 아니다: {order}"
    i = s1.index('<img src="cei_nd_o_decomposition_x002_si.png"')
    cap = s1[i:s1.index("</figcaption>", i)]
    assert 'alt="Two panels' in cap and "Fig. S1." in cap, "SI 그림이 두 패널 Fig. S1 이 아니다"
    assert "x&#8201;=&#8201;0.02" in cap, "Fig. S1 캡션이 x = 0.02 를 말하지 않는다"
    assert "RETRACTED" not in cap and "<s>" not in cap, "캡션 안에 취소선 철회문이 남아 있다"
    assert "lithium-matched" in cap, "Li 장부 설명이 캡션에서 빠졌다"
    r = client.get(LOCAL_REPORT.rsplit("/", 1)[0] + "/cei_nd_o_decomposition_x002_si.png")
    import struct
    w, hgt = struct.unpack(">II", r.data[16:24])            # PNG IHDR
    assert 1.8 < w / hgt < 2.9, f"SI 그림이 1×2 가 아니다: {w}×{hgt}"
    gen = (REPORT.parents[3] / "tools/figures/plot_cei_nd_o_decomposition.py").read_text("utf-8")
    assert "plt.subplots(1, 3" in gen and re.search(r"^\s*a3\.", gen, re.M) is None, \
        "생성기에 옛 (c) 패널(a3)이 되돌아왔다"
    assert '"cei_nd_o_decomposition_si.png"' in gen and '"cei_nd_phase.png"' in gen, \
        "생성기가 SI 판·본문 판을 안 만든다 (화면 파일의 출처가 끊긴다)"
    j = s1.index("Fig. S1 을 읽는 법")
    box = s1[j:s1.index("<!-- 방법 박스", j)]
    assert "⛔" in box and "Li 장부" in box, "읽는 법 상자에 철회 표지가 없다"
    lo, hi = _x002_limatched_range()
    assert f"{lo:.1f}".replace("-", "−") in box and f"{hi:.1f}".replace("-", "−") in box, \
        f"읽는 법 상자의 Li 맞춤 범위가 원장({lo} ~ {hi})과 다르다"


def test_fig1_is_the_phase_ladder_in_s2_and_matches_the_raw(client):
    """양성+음성 — 본문 Fig. 1 은 §2 의 **상 사다리**(옛 분해 그림의 (c))다 (1저자 2026-09-29 · 원고 본문 Fig. 2).
    사슬: 원자료 반응식 → (도구 _rxn_side_terms 로 다시 센) 전압별 Nd 상 = 생성기 CSV = 캡션 문장.
    잡는 것: 그림이 §2 밖·Fig. 2 뒤로 감 · CSV 가 원자료와 다름 · 캡션이 CSV 와 다른 상을 말함 ·
      '1 할' 옆에서 '9 할' 이 빠짐 (원장 금지: 'x = 0.02 에서 Nd 가 양극 대신 P 방을 댄다')."""
    import csv as _csv
    h = _report_html(client)
    s2 = _section(h, "s2")
    i = s2.index('<img src="cei_nd_phase_x002.png"')
    assert i < s2.index('<img src="cei_p_host_ladder_x002.png"'), "Fig. 1 이 Fig. 2 뒤에 있다"
    cap = s2[i:s2.index("</figcaption>", i)]
    assert "Fig. 1. The phase the neodymium ends up in" in cap, "본문 Fig. 1 캡션이 아니다"
    assert "x&#8201;=&#8201;0.02" in cap and "k&#183;x" in cap and "<s>" not in cap
    rows = list(_csv.DictReader(open(REPORT.parent / "cei_nd_phase_x002.csv", encoding="utf-8")))
    assert rows, "CSV 가 비었다 — 시험이 헛것을 재고 있다"
    got = {}
    for r in rows:
        got.setdefault(float(r["voltage_V"]), {})[r["nd_phase"]] = int(r["n_cathodes_giving_phase"])
    T = _x002_tool()
    R = json.loads(X002_IFACE.read_text("utf-8"))["results"]
    want = {}
    for cat, d in R.items():
        for k, rxs in d["reactions"].items():
            if (d.get("endpoint_degenerate") or {}).get(k, {}).get("nd_p_002_asused") is not False:
                continue
            rx = (rxs or {}).get("nd_p_002_asused") or ""
            if "->" not in rx:
                continue
            for _n, f, comp in T._rxn_side_terms(rx.split("->", 1)[1]):
                if comp.get("Nd", 0) > 0:
                    want.setdefault(float(k), {})
                    want[float(k)][f] = want[float(k)].get(f, 0) + 1
    assert want == got, f"CSV 가 원자료 반응식과 다르다: 원자료 {want} · CSV {got}"
    #: 캡션 문장 ↔ CSV (문장이 말하는 것만)
    assert set(got[2.5]) == set(got[3.0]) == {"NdPO4"} and got[2.5]["NdPO4"] == 4
    assert {"LiNd(PO3)4", "NdCl3"} <= set(got[3.5])
    assert {"Nd(PO3)3", "NdP5O14"} <= set(got[4.0]) and set(got[4.5]) == {"NdP5O14"}
    assert not any("Nd2(SO4)3" in dd for dd in got.values()), "캡션은 Nd2(SO4)3 줄이 비었다고 말한다"
    j = s2.index("Fig. 1 을 읽는 법")
    box = s2[j:s2.index("그 짝을 누가 대느냐다", j)]
    assert "1 할" in box and "9 할" in box, "1 할 문장에 9 할이 같이 없다"


def test_s2_lead_share_and_scope_match_fig1(client):
    """⛔음성 — §2 요지 줄(접어도 보이는 한 줄)이 Fig. 1 원자료와 같은 몫·양극 범위를 말한다 (2026-09-29).
    잡는 것: 4 V 이상의 몫을 '1 할' 하나로 씀 (4.0 V 의 LiNiO₂·NMC811 은 Nd(PO₃)₃ 6 %) ·
      '전량' 을 양극 범위 없이 씀 (LiMnO₂ 는 NdCl₃ 0 %) · 1 할 옆에서 9 할이 빠짐 (원장 금지)."""
    import csv as _csv
    s2 = _section(_report_html(client), "s2")
    m = re.search(r'<span class="sec-one">(.*?)</span></summary>', s2, re.S)
    lead = re.sub(r"<[^>]+>", "", m.group(1))
    rows = list(_csv.DictReader(open(REPORT.parent / "cei_nd_phase_x002.csv", encoding="utf-8")))
    hi = [r for r in rows if float(r["voltage_V"]) >= 4.0]
    #: k·x 를 % 로 (x = 0.02 → 2k %)
    share = sorted({round(2 * float(r["p_per_nd_k"])) for r in hi if float(r["p_per_nd_k"]) > 0})
    assert share == [6, 10], f"원자료의 4 V 이상 몫이 {share} % 다 — 시험을 다시 본다"
    assert f"{share[0]}–{share[-1]} %" in lead and "최대 1 할" in lead and "4 V 이상" in lead, \
        f"요지의 몫이 Fig. 1 원자료({share[0]}–{share[-1]} %)와 다르다"
    zero = {r["nd_phase"] for r in hi if float(r["p_per_nd_k"]) == 0}
    assert zero == {"NdCl3"}, f"원자료의 0 % 상이 {zero} 다 — 시험을 다시 본다"
    assert "Co·Ni·NMC811" in lead and "NdCl₃" in lead, "'전량' 에 양극 범위(LiMnO₂ 예외)가 없다"
    assert "9 할" in lead, "1 할 옆에 9 할이 없다"


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
        # ⛔ 2026-09-28 — 환원 칸은 reduction_limit_V 가 **아니다** (그 필드는 '아직 Li 를 흡수하는 단계' 를 집는
        #   계통 오류 · HZ-esw-reduction-limit-label). 같은 원장 profile 에서 Li 교환 0 인 첫 경계와 대조한다.
        prof = sorted(esw[lab]["profile"], key=lambda e: e["V_vs_Li"])
        red = next(e["V_vs_Li"] for e in prof if abs(e["evolution_Li"]) < 1e-6)
        assert float(cells[1]) == red, (lab, cells, "교환 0 첫 경계", red)
        assert float(cells[1]) != esw[lab]["reduction_limit_V"], (lab, "계통 오류 값이 표에 남았다")
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


def _gen():
    """그림 생성기 모듈 — 판정 함수는 **거기 하나**만 쓴다 (두 곳에서 판정하면 두 판정이 갈린다)."""
    import importlib.util
    src = REPORT.parents[3] / "tools/figures/plot_cei_nd_protection.py"
    spec = importlib.util.spec_from_file_location("plot_cei_nd_protection", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fnum(v):
    v = (v or "").strip()
    return None if v in ("", "None") else float(v)


def _prot_counts(rows):
    """행 수·통과·탈락·열 수·전농도통과 열.

    ⛔ 2026-09-22 정정 (2차 리뷰 ②). 종전엔 여기서 `all(gate_pass)` 로 **따로** 판정했다 —
    생성기 `_full_pass` 가 완전성 검사를 받은 뒤에도 이 쌍둥이는 그대로여서, 탈락 행을 지우면
    시험 쪽 18 · 생성기 쪽 17 로 갈렸다(실측). 이제 전농도통과는 **생성기 함수 한 곳**에서 받는다.
    격자가 깨지면(농도 누락·낯선 농도) 그 함수가 SystemExit 로 죽고, 이 헬퍼도 그대로 죽는다.
    """
    n_all = len(rows)
    n_fail = sum(1 for r in rows if r["gate_pass"] == "False")
    n_pass = sum(1 for r in rows if r["gate_pass"] == "True")
    cols = {(r["cathode"], r["voltage_V"]) for r in rows}
    typed = [{"cathode": r["cathode"], "voltage_V": _fnum(r["voltage_V"]),
              "x_Nd": _fnum(r["x_Nd"]), "gate_pass": r["gate_pass"] == "True"} for r in rows]
    gen_full = _gen()._full_pass(typed)
    full = {(c, v) for (c, v) in cols
            if any(c == fc and abs(float(v) - fV) < 1e-9 for fc, fV in gen_full)}
    assert len(full) == len(gen_full), (sorted(full), gen_full)   # 형 변환에서 잃은 열이 없다
    return n_all, n_pass, n_fail, len(cols), full


def _prot_deviation(rows, full):
    """열별 최대 |실측 − 예측식| (%p) 와 'k 가 없어 견줄 수 없는' 열 — 예측식 min(1, k·x/(1−x)) 기준.

    ⛔ P_taken_by_Nd 와 빼지 않는다 (2026-09-21 외부 리뷰 P1-1) — 식을 평가하는 자리다.
    두 시험(오차 계층 · ⏭ 블록)이 **같은 함수**로 문턱을 만든다.
    """
    def _pred(r):
        k, x = _fnum(r["k_observed"]), _fnum(r["x_Nd"])
        return None if k is None else min(1.0, k * x / (1 - x))
    dev, nok = {}, set()
    for c in full:
        sub = [r for r in rows if (r["cathode"], r["voltage_V"]) == c]
        ds = [abs(_fnum(r["protection_observed"]) - _pred(r)) * 100 for r in sub
              if _fnum(r["protection_observed"]) is not None and _pred(r) is not None]
        if not ds:
            if any(_fnum(r["protection_observed"]) is not None for r in sub):
                nok.add(c)          #: Nd 인산염이 아예 안 나온 열 — 0 = 0 은 일치가 아니다
            continue
        dev[c] = max(ds)
    return dev, nok


def _resume_block_violations(blk, thresh):
    """⏭ 블록이 철회된 문턱을 **주장으로** 되살렸는지 — 굵기·띄어쓰기에 흔들리지 않게 본다.

    ⛔ 2026-09-22 정정 (2차 리뷰 ③). 종전 시험은 `"식이 **≤2.5 %p** 로 맞는"` 정확한 굵기
    표기만 금지했다 — 굵기 없이 `식이 ≤2.5 %p 로 맞는 열은 셋뿐이다` 라고 쓰면 **통과**했고,
    반대로 현행 문장의 `**셋뿐**` 을 `**세 개뿐**` 으로 바꾸면 **실패**했다(실측). 문자열
    스냅숏이지 주장 검사가 아니었다. 이제 별표를 전부 벗기고 공백을 접은 뒤 "≤X %p (…) 로 맞는"
    꼴의 **모든** 주장을 찍어, 현행 문턱과 다른 값이 하나라도 있으면 위반이다.
    (리뷰 이력으로 "철회된 ≤2.5 %p 잔존" 이라 적는 것은 '로 맞는' 이 없어 걸리지 않는다.)
    """
    import re as _re
    norm = _re.sub(r"\s+", " ", _re.sub(r"\*+", "", blk))
    claims = _re.findall(r"≤\s*([0-9]+(?:\.[0-9]+)?)\s*%p\s*(?:\([^)]{0,40}\)\s*)?(?:로|으로)\s+맞는", norm)
    bad = []
    if not claims:
        bad.append("현행 문턱 주장('≤X.X %p 로 맞는')이 ⏭ 블록에 없다")
    want = f"{thresh:.1f}"
    for c in claims:
        if c != want:
            bad.append(f"⏭ 블록이 현행({want})과 다른 문턱 ≤{c} %p 를 주장한다 — 철회값이 되살아났다")
    return bad


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

    #: ⛔ 예측식 기준 (P1-1). 계산은 공용 헬퍼 한 곳 — ⏭ 블록 시험과 같은 문턱을 쓴다.
    dev, noк = _prot_deviation(rows, full)

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
    assert f"식과 견줄 수 있는 <b>{len(dev)} 개</b>" in h0, f"화면의 견줄 수 있는 열 수가 자료({len(dev)})와 다르다"
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


def _x002_measurable(rows):
    """x = 0.02 에서 **잴 수 있는 칸** — 게이트 통과 + 보호율 정의 (양쪽 다 TM 인산염이 없는 칸은 빈칸)."""
    return [r for r in rows if _fnum(r["x_Nd"]) == 0.02 and r["gate_pass"] == "True"
            and _fnum(r["protection_observed"]) is not None]


def test_s2b_lead_separates_gate_pass_from_fit_and_scopes_x002(client):
    """⛔음성 — §2b 요지 줄(접어도 보이는 한 줄)이 '통과' 를 '식이 맞음' 으로 읽히게 두지 않고,
    x = 0.02 값을 한 열에서 가져왔다는 것을 밝힌다 (2026-09-29).
    잡는 것: '17 통과(NMC811 6/6)' 만 식 바로 뒤에 둠 — NMC811 은 식이 3.5 V 한 열에서만 맞는다 ·
      식이 맞는 셋의 분모(견줄 수 있는 열) 누락 · x = 0.02 의 10.3 % 를 열 없이 씀 (LiCoO₂ 4.3 V 한 열 값) ·
      x = 0.02 칸 전체 범위·개수가 자료와 다름 · 본문 상자에 같은 한정이 없음."""
    rows = _prot_rows()
    _, _, _, _, full = _prot_counts(rows)
    dev, _ = _prot_deviation(rows, full)
    good = [c for c in dev if dev[c] <= 3.11]
    assert len(good) == 3 and len(dev) == 11, (len(good), len(dev))
    s2b = _section(_report_html(client), "s2b")
    lead = re.search(r'<span class="sec-one">(.*?)</span></summary>', s2b, re.S).group(1)
    assert "식이 맞았다는 뜻이 아니다" in lead, "요지가 게이트 통과와 식의 적중을 가르지 않는다"
    assert f"견줄 수 있는 <b>{len(dev)} 중 셋</b>" in lead, "식이 맞는 셋의 분모가 요지에 없다"
    ref = [r for r in rows if r["cathode"] == "LiCoO2" and r["voltage_V"] == "4.3" and _fnum(r["x_Nd"]) == 0.02]
    assert len(ref) == 1
    assert f"LiCoO₂ 4.3 V 에서 <b>{100 * float(ref[0]['protection_observed']):.1f} %</b>" in lead, \
        "x = 0.02 값에 열(LiCoO₂ 4.3 V)이 없거나 자료와 다르다"
    m = _x002_measurable(rows)
    vals = [float(r["protection_observed"]) for r in m]
    lo, hi = (f"{round(100 * v):d}".replace("-", "−") for v in (min(vals), max(vals)))
    assert f"잴 수 있는 x = 0.02 칸 {len(m)} 개 전체로는 <b>{lo}~{hi} %</b>" in lead, \
        f"요지의 x = 0.02 범위가 자료({len(m)} 칸 · {lo}~{hi} %)와 다르다"
    box = s2b[s2b.index("는 곡선 어디에 있나"):]
    assert "<b>LiCoO₂ 4.3 V 한 열</b>" in box and f"x = 0.02 칸 <b>{len(m)} 개</b>" in box \
        and f"<b>{lo}~{hi} %</b>" in box, "본문 상자에 한 열 한정·전체 범위가 없다"
    worst = min(m, key=lambda r: float(r["protection_observed"]))
    assert (worst["cathode"], worst["voltage_V"]) == ("NMC811", "4.5"), (worst["cathode"], worst["voltage_V"])
    assert max(m, key=lambda r: float(r["delta_x"])) is worst, "음수 칸이 |Δx| 최대 칸이 아니다 — 상자 문장이 틀렸다"
    assert f"<b>{float(worst['delta_x']):.3f}</b>" in box, "음수 칸의 |Δx| 가 자료와 다르다"


def test_s2b_reading_box_ladder_and_thiophosphate_scope(client):
    """⛔음성 — §2b 읽는 법 상자의 계수 사다리가 §2 Fig. 1 CSV 와 같고, P₂S₇ 칸 범위가 자료와 같다 (2026-09-29).
    잡는 것: 사다리에서 4.0 V 의 Nd(PO₃)₃(3) 이 빠져 k 가 단조로 읽힘 · 분해 그림 SI 이동 뒤 남은
      '(c) 는 장식이 아니라 계수다' (지금 (c) 는 Fig. 3 의 비교 게이트다) · P₂S₇ 를 '4.5 V' 한정으로 씀."""
    import csv as _csv
    s2b = _section(_report_html(client), "s2b")
    box = s2b[s2b.index("읽는 법 — 세 패널이 한 사슬이다"):s2b.index("P₂S₇ 칸은")]
    sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    phase = list(_csv.DictReader(open(REPORT.parent / "cei_nd_phase_x002.csv", encoding="utf-8")))
    ks = {r["nd_phase"]: int(float(r["p_per_nd_k"])) for r in phase if float(r["p_per_nd_k"]) > 0}
    assert ks.get("Nd(PO3)3") == 3 and len(ks) == 4, f"Fig. 1 CSV 의 인산염 사다리가 바뀌었다 — {ks}"
    for f, k in ks.items():
        assert f"{f.translate(sub)}({k})" in box, f"읽는 법 사다리에 {f}({k}) 가 없다"
    assert "(c) 는 장식이 아니라" not in s2b, "SI 이동 전의 '(c)' 참조가 남았다 — 지금 (c) 는 Fig. 3 의 게이트다"
    assert "§2 Fig. 1 은 장식이 아니라 계수다" in box
    rows = _prot_rows()
    thio = [r for r in rows if (r["P_to_thiophosphate"] or "").strip()]
    assert thio and all("P2S7" in r["P_to_thiophosphate"] for r in thio)
    assert {r["cathode"] for r in thio} == {"LiCoO2", "LiMnO2"}, sorted({r["cathode"] for r in thio})
    para = s2b[s2b.index("P₂S₇ 칸은"):]
    para = para[:para.index("</p>")]
    assert f"P₂S₇ 가 나오는 <b>{len(thio)} 칸</b>" in para and "LiMnO₂" in para, \
        f"P₂S₇ 칸 범위가 자료({len(thio)} 칸 · LiCoO₂·LiMnO₂)와 다르다"


def test_tldr_protection_bullets_do_not_read_gate_pass_as_benefit(client):
    """⛔음성 — 머리 요약(✅ 말하는 것)의 이득 줄이 게이트 통과를 이득으로 읽히게 두지 않는다 (2026-09-29).
    잡는 것: '조건이 크게 넓어졌다 — 17/24 통과' 꼴 (통과는 비교 게이트인데 이득의 조건이 넓어진 것으로 읽힘) ·
      식이 맞는 열의 분모·x = 0.02 실측 범위가 §2b 자료와 다름 · '전량' 에 양극 범위 없음 (LiMnO₂ 는 NdCl₃)."""
    import csv as _csv
    h = _report_html(client)
    yes = h[h.index('<div class="tldr-yes">'):h.index('<div class="tldr-no">')]
    items = re.findall(r"<li>(.*?)</li>", yes, re.S)
    gain = [li for li in items if "그 이득은" in li]
    assert len(gain) == 1, f"이득 줄이 {len(gain)} 개다 — 시험이 헛것을 잰다"
    g = gain[0]
    assert "넓어졌다" not in g, "게이트 통과 수를 '조건이 넓어졌다' 로 읽는 문장이 남았다"
    assert "이득이 확인됐다는 뜻이 아니다" in g, "이득 줄이 게이트 통과와 이득을 가르지 않는다"
    rows = _prot_rows()
    _, _, _, _, full = _prot_counts(rows)
    dev, _ = _prot_deviation(rows, full)
    assert len([c for c in dev if dev[c] <= 3.11]) == 3
    assert f"견줄 수 있는 <b>{len(dev)} 중 셋</b>" in g, "식이 맞는 셋의 분모가 이득 줄에 없다"
    m = _x002_measurable(rows)
    vals = [float(r["protection_observed"]) for r in m]
    lo, hi = (f"{round(100 * v):d}".replace("-", "−") for v in (min(vals), max(vals)))
    assert f"잴 수 있는 {len(m)} 칸에서 <b>{lo}~{hi} %</b>" in g, \
        f"x = 0.02 범위가 자료({len(m)} 칸 · {lo}~{hi} %)와 다르다"
    whole = [li for li in items if "<b>전량</b> 인산염" in li]
    assert len(whole) == 1, f"'전량' 줄이 {len(whole)} 개다"
    phase = list(_csv.DictReader(open(REPORT.parent / "cei_nd_phase_x002.csv", encoding="utf-8")))
    nonp = {r["nd_phase"] for r in phase if float(r["voltage_V"]) >= 3.5 and float(r["p_per_nd_k"]) == 0}
    assert nonp == {"NdCl3"}, f"3.5 V 이상 인산염 아닌 Nd 상이 {nonp} 다 — 시험을 다시 본다"
    assert "Co·Ni·NMC811 양극" in whole[0] and "LiMnO₂ 는 NdCl₃" in whole[0], "'전량' 에 양극 범위가 없다"


def test_s2b_plain_box_matches_the_raw(client):
    """양성+음성 — §2b '쉽게 다시 읽기' 상자(1저자 2026-09-29 "쉬운 버전 밑으로")의 수가 원자료와 같다.
    잡는 것: 쉬운 말로 옮기며 수가 바뀜 — 제외 19/120 · 통과 17/24 · 미정의 5 · k 없음 1 (LiMnO₂ 3.5 V = NdCl₃) ·
      견줄 11 = 3 + 3 + 5 와 오차 구간 · Mn 바닥 10 % · 저전압 최대 25 % · 고전압 NMC811 멈춤 46–48 % · 예측 71·75 % ·
      LiMnO₂ 3.0 V 수열 · 예시(10.2 대 10.3) · 게이트 0.05 · 그리고 '보호율 = 양극이 덜 녹는다' 로 읽히게 둠
      (인산염을 면한 금속의 몫이 대부분 황화물로 간다 — 반응식에서 다시 센다)."""
    h = _report_html(client)
    s2b = _section(h, "s2b")
    i = s2b.index('id="s2b-plain"')
    box = s2b[i:s2b.index('<div class="box" style="border-left:3px solid var(--nd)">', i)]
    rows = _prot_rows()
    n_all, _, n_fail, n_col, full = _prot_counts(rows)
    dev, nok = _prot_deviation(rows, full)
    undef = [c for c in full if all(_fnum(r["protection_observed"]) is None
                                    for r in rows if (r["cathode"], r["voltage_V"]) == c)]
    good = [c for c in dev if dev[c] <= 3.11]
    mid = [c for c in dev if 3.11 < dev[c] < 20]
    worst = [c for c in dev if dev[c] >= 20]
    assert (len(good), len(mid), len(worst), len(dev), len(undef)) == (3, 3, 5, 11, 5)
    assert nok == {("LiMnO2", "3.5")}
    rng = lambda cs: f"{min(dev[c] for c in cs):.0f}–{max(dev[c] for c in cs):.0f} %p"
    need = [f"<b>{n_all} 경우</b>(양극 4 × 전압 6 × Nd 양 5) 중 <b>{n_fail} 개</b>를 뺐다",
            f"양극·전압 조합 {n_col} 개 중 Nd 양 다섯 모두 검사를 통과한 것은 <b>{len(full)} 개</b>",
            f"{len(full)} 개 중 {len(undef)} 개는", "1 개(LiMnO₂ 3.5 V)",
            f"남은 <b>{len(dev)} 개</b> 중 예측이 잘 맞는 것({max(dev[c] for c in good):.1f} %p 안)이 <b>{len(good)} 개</b>",
            f"조금 어긋나는 것({rng(mid)})이 {len(mid)} 개", f"크게 어긋나는 것({rng(worst)})이 <b>{len(worst)} 개</b>",
            "“양극이 덜 녹는다” 가 아니라"]
    miss = [s for s in need if s not in box]
    assert not miss, f"쉬운 상자의 수·문장이 자료와 다르다: {miss}"
    #: 게이트 문턱 — 동결된 사전등록 값
    g1 = json.loads((REPORT.parents[3] / "db/properties/cei_protection_allcells_result_2026_09_21.json"
                     ).read_text("utf-8"))["gates_frozen"]["G1_dx_max"]
    assert f"{g1} 넘게 다른" in box
    #: 예시 — LiCoO₂ 4.3 V · x = 0.02 의 예측·계산
    ref = [r for r in rows if r["cathode"] == "LiCoO2" and r["voltage_V"] == "4.3" and _fnum(r["x_Nd"]) == 0.02][0]
    pred = min(1.0, _fnum(ref["k_observed"]) * 0.02 / 0.98)
    assert f"예측 {100 * pred:.1f} %, 계산 {100 * float(ref['protection_observed']):.1f} %" in box
    #: 저전압 NMC811 — Mn 바닥과 Nd 가 가져간 P 의 최대
    low = [r for r in rows if r["cathode"] == "NMC811" and r["voltage_V"] in ("2.5", "3.0")]
    floor = {round(float(r["tm_phosphate_share"]), 3) for r in low}
    assert floor == {0.1}, floor
    #: ⚠ 두 자리(④ 저전압 · ⑦ 이유)를 각각 문맥으로 묶는다 — '금속의 10 %' 하나만 찾으면 한쪽이 틀려도 통과했다
    mn = f"{100 * floor.pop():.0f}"
    assert f"금속의 {mn} % — 딱 Mn 만큼" in box and f"Mn(금속의 {mn} %)" in box, "Mn 바닥 몫이 자료와 다르다"
    assert f"최대 {100 * max(float(r['P_taken_by_Nd']) for r in low):.0f} %" in box
    #: 고전압 NMC811 — Nd 10 % 이상에서 보호율이 멈추는 구간 · 15·20 % 의 예측 · 벌어짐
    hi = [r for r in rows if r["cathode"] == "NMC811" and r["voltage_V"] in ("4.3", "4.5") and _fnum(r["x_Nd"]) >= 0.10]
    stop = [100 * float(r["protection_observed"]) for r in hi]
    assert f"{min(stop):.0f}–{max(stop):.0f} % 에서 멈추고" in box, f"멈춤 구간이 자료({min(stop):.1f}–{max(stop):.1f})와 다르다"
    top = [r for r in hi if _fnum(r["x_Nd"]) >= 0.15]
    by_x = {}
    for r in top:        #: 4.3·4.5 V 의 예측이 같은 x 에서 같아야 한 수로 적을 수 있다
        p = 100 * min(1.0, _fnum(r["k_observed"]) * _fnum(r["x_Nd"]) / (1 - _fnum(r["x_Nd"])))
        assert abs(by_x.setdefault(_fnum(r["x_Nd"]), p) - p) < 1e-6, (r["voltage_V"], r["x_Nd"])
    assert sorted(by_x) == [0.15, 0.2], sorted(by_x)
    assert f"15·20 % 에서 {by_x[0.15]:.0f}·{by_x[0.2]:.0f} %" in box
    gap = [dev_ for dev_ in (abs(100 * float(r["protection_observed"]) -
                                  100 * min(1.0, _fnum(r["k_observed"]) * _fnum(r["x_Nd"]) / (1 - _fnum(r["x_Nd"]))))
                              for r in top)]
    assert f"{min(gap):.0f}–{max(gap):.0f} %p 벌어진다" in box
    #: 수열 (LiMnO₂ 3.0 V)
    seq = [float(r["protection_observed"]) for r in sorted(
        (r for r in rows if r["cathode"] == "LiMnO2" and r["voltage_V"] == "3.0"), key=lambda r: _fnum(r["x_Nd"]))]
    assert " → ".join(f"{round(v * 100, 1):g}" for v in seq) + " %" in box
    #: 인산염을 면한 금속의 행선지 — 반응식에서 다시 센다 (게이트 통과 · 보호율 정의 칸)
    n_cells, sul = _tm_escape_to_sulfide(rows)
    assert f"<b>{n_cells} 경우</b>를 합치면 그 몫의 <b>{sul:.0f} %</b> 는" in box, \
        f"황화물 몫이 자료({n_cells} 경우 · {sul:.1f} %)와 다르다"


def _tm_escape_to_sulfide(rows):
    """인산염을 면한 양극 금속이 어디로 가나 — (칸 수, 황화물 몫 %).

    게이트를 통과하고 보호율이 정해지는 칸마다 도핑·대조 반응식(cei_protection_full.jsonl)의 우변을
    도구 `_rxn_side_terms` 로 다시 읽어, 좌변 양극 금속 중 인산염(P 포함)·황화물(S 포함 · O·P 없음)·기타로
    간 몫을 센다. 도핑 − 대조의 인산염 감소분 합계 중 황화물 증가분 합계가 차지하는 몫을 돌려준다.
    ⚠ 이 도구가 못 하는 것: 칸마다의 몫은 돌려주지 않는다 (화면은 합계만 인용한다)."""
    T = _x002_tool()
    recs = {}
    for ln in (REPORT.parents[3] / "db/properties/cei_protection_full.jsonl").read_text("utf-8").splitlines():
        if ln.strip():
            r = json.loads(ln)
            recs[(r["species"], r["cathode"])] = r
    tms = ("Co", "Ni", "Mn")

    def _where(sp, cat, V):
        bv = recs[(sp, cat)]["by_voltage"]
        key = next(k for k in bv if abs(float(k) - V) < 1e-9)
        lhs, rhs = bv[key]["reaction"].split("->", 1)
        tl = sum(n * sum(k.get(e, 0) for e in tms) for n, _, k in T._rxn_side_terms(lhs))
        out = {"P": 0.0, "S": 0.0, "X": 0.0}
        for n, _, k in T._rxn_side_terms(rhs):
            tm = sum(k.get(e, 0) for e in tms)
            if tm > 0:
                c = "P" if k.get("P", 0) > 0 else ("S" if k.get("S", 0) > 0 and k.get("O", 0) == 0 else "X")
                out[c] += n * tm / tl
        return out
    dP = dS = 0.0
    cells = [r for r in rows if r["gate_pass"] == "True" and _fnum(r["protection_observed"]) is not None]
    for r in cells:
        tag = f"{round(100 * _fnum(r['x_Nd'])):03d}"
        d = _where(f"ndP{tag}", r["cathode"], _fnum(r["voltage_V"]))
        c = _where(f"liMatch{tag}", r["cathode"], _fnum(r["voltage_V"]))
        dP += d["P"] - c["P"]
        dS += d["S"] - c["S"]
    assert cells and dP < 0, "도핑 쪽 금속 인산염 몫이 줄지 않았다 — 시험이 헛것을 잰다"
    return len(cells), 100 * dS / -dP


def test_s3_reactions_loops_and_schematic_match_the_records(client):
    """⛔음성 — §3 의 균형반응 10 개 표 · 검산 고리 · 밀려난 Li 세 행선지 · 모식도가 원자료와 같다 (2026-09-29).
    잡는 것: 표의 반응식·ΔE 가 cei_formation 과 다름 · 고리(③−④ = ⑤−⑥ = ①)가 안 닫힘 · Li₂S 경로(⑦) 누락 ·
      교차점 1.67 이 ②·⑨ 와 다름 · 모식도가 '무도핑의 대안은 P₂S₇ 뿐' 으로 되돌아감 (§2: 4 V 이상은 양극 전이금속
      인산염이 주 경로이고 P₂S₇ 는 LiMnO₂ 4.3 V 에서만 같이 나온다 — P 수용상 원자료에서 다시 센다)."""
    s3 = _section(_report_html(client), "s3")
    R = list(json.loads((REPORT.parents[3] / "db/properties/cei_formation_2026_09_16.json")
                        .read_text("utf-8"))["reactions"].values())
    assert len(R) == 10 and all(r.get("ok") for r in R), "원자료의 반응이 10 개가 아니다 — 시험을 다시 본다"
    E = [r["E_eV_per_P"] for r in R]
    marks = "①②③④⑤⑥⑦⑧⑨⑩"
    for m, r, e in zip(marks, R, E):
        row = re.search(r"<tr><td>%s</td><td[^>]*>(.*?)</td><td[^>]*>(.*?)</td>" % m, s3)
        assert row, f"§3 표에 {m} 행이 없다"
        assert row.group(1) == r["reaction"], f"{m} 반응식이 원자료와 다르다: {row.group(1)!r}"
        assert row.group(2) == f"{e:+.4f}", f"{m} ΔE {row.group(2)} vs 원자료 {e:+.4f}"
    loop = {round(E[2] - E[3], 4), round(E[4] - E[5], 4), round(E[0], 4)}
    assert len(loop) == 1, f"검산 고리가 안 닫힌다: {loop}"
    assert f"③−④ = ⑤−⑥ = ① = {E[0]:+.4f}" in s3
    #: 교차점 — ②(Li/P 1) 와 ⑨(Li/P 2) 사이 선형 보간
    cross = 1 + abs(E[1]) / (abs(E[1]) + E[8])
    lead = re.search(r'<span class="sec-one">(.*?)</span></summary>', s3, re.S).group(1)
    assert f"Li/P ≲ {cross:.2f}" in lead, f"요지의 교차점이 ②·⑨ 보간({cross:.4f})과 다르다"
    #: 밀려난 Li 세 행선지 — Li₂O(①) · Li₂S(⑦) 는 지고 LiCl(⑧) 만 이긴다
    assert E[0] > 0 and E[6] > 0 and E[7] < 0
    rx = s3[s3.index("버려지는 Li 가 어디로 가느냐"):s3.index("살아남은 절반")]
    for m_i, dest in ((0, "Li₂O 로"), (6, "Li₂S 로"), (7, "LiCl 로")):
        assert dest in rx and f"ΔE = {E[m_i]:+.4f} eV/P" in rx, f"{dest} 줄의 값이 원자료({E[m_i]:+.4f})와 다르다"
    assert "Li₂O · Li₂S 로 가면 진다" in lead, "요지에 Li₂S 로 가도 진다는 한정이 없다"
    #: 모식도 — 무도핑의 고전압 주 경로는 양극 전이금속 인산염 (P 수용상 원자료로 다시 센다)
    lad = json.loads((REPORT.parents[3] / "db/properties/cei_p_host_ladder_x002_2026_09_28.json").read_text("utf-8"))
    hi = [r for r in lad["rows"] if r["electrolyte"] == "modelc" and r["voltage_V"] >= 4.0]
    tm = ("Co", "Ni", "Mn")
    assert hi and all(any(any(e in h["formula"] for e in tm) and "P" in h["formula"] and h["anion"] == "P-O"
                              for h in r["p_hosts"]) for r in hi), "원자료: 4 V 이상 무도핑에 전이금속 인산염 없는 칸이 있다"
    p2s7 = sorted({(r["cathode"], r["voltage_V"]) for r in lad["rows"] if r["electrolyte"] == "modelc"
                   and any(h["formula"] == "P2S7" for h in r["p_hosts"])})
    assert p2s7 == [("LiMnO2", 4.3)], f"원자료: 무도핑 P₂S₇ 칸이 {p2s7} 다 — 모식도 문장을 다시 본다"
    fig = s3[s3.index("① 충전하면"):s3.index("Fig. 4 를 읽는 법")]
    assert "대안이 P₂S₇ 뿐" not in fig and "양극 전이금속 인산염" in fig, "모식도가 무도핑 대안을 P₂S₇ 로 적는다"
    assert "4 V 이상 네 양극 전부" in fig and "LiMnO₂ 4.3 V 에서만" in fig
    assert "<b>하나 더</b>" in fig, "읽는 법이 Nd 를 '유일한 Li 안 드는 방' 으로 읽게 둔다"


def test_protection_is_not_read_as_cathode_sparing(client):
    """⛔음성 — 보호율을 '양극을 아낀다 · 덜 빠진다 · 코팅처럼' 으로 쓰는 문장이 화면에 다시 생기면 잡는다
    (1저자 2026-09-29 "고치자"). 인산염을 면한 금속은 반응에서 빠지지 않고 대부분 황화물이 된다.
    잡는 것: 제목·머리 요약·§0·§2b·Fig. 3 캡션의 옛 표현 되살림 · §9 금지 항목과 캡션·원고 틀 카드의
    72 칸·94 % 가 반응식 재계수와 다름. §9 안의 금지 문장만 검사에서 뺀다.
    ⚠ 따옴표 안을 빼지 않는다 — 첫 판은 “ ” 안을 지웠는데, 옛 표현 “아껴진 양극 TM” 자체가 따옴표 안이라
      되살아나도 못 잡았다. 부정문(“양극이 덜 녹는다” 가 아니라)은 아래 어느 꼴에도 안 걸린다."""
    h = _report_html(client)
    s9 = _section(h, "s9")
    body = h.replace(s9, "")
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    text = re.sub(r"<[^>]+>", "", body)
    bad = [p for p in ("양극을 아끼", "얼마나 아끼", "아껴진 양극", "덜 빠진다",
                       "phosphate spares", "하는 일 가운데 양극", "양극을 지킨") if p in text]
    assert not bad, f"보호율을 양극 절약으로 읽는 표현이 남았다: {bad}"
    s2b = _section(h, "s2b")
    title = re.sub(r"<[^>]+>", "", re.search(r'<h2 class="sec-h">(.*?)</h2>', s2b).group(1))
    assert "금속 인산염을 얼마나 줄이나" in title, title
    n, sul = _tm_escape_to_sulfide(_prot_rows())
    item = [li for li in re.findall(r"<li>(.*?)</li>", s9, re.S) if "보호율을 “양극이 덜 녹는다" in li]
    assert len(item) == 1, "§9 에 보호율 뜻 금지 항목이 없다"
    assert f"<b>{n} 칸</b>을 합치면 그 몫의 <b>{sul:.0f} %</b> 가 황화물" in item[0], "§9 항목의 수가 반응식과 다르다"
    i = s2b.index("<figcaption><b>Fig. 3.")
    cap = s2b[i:s2b.index("</figcaption>", i)]
    assert "keeps out of phosphate products" in cap
    assert f"summed over the {n} cells that pass the gates and have a defined value, {sul:.0f}&#8201;% of it forms sulfides" in cap
    card = (REPORT.parents[3] / "kb/syntheses/cei_nd_manuscript_framing_2026_09_18.md").read_text("utf-8")
    assert f"{n} 칸 합계로 그 몫의 **{sul:.0f} % 가 황화물**" in card, "원고 틀 카드의 보강이 반응식과 다르다"


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

    #: 철회된 문턱이 **주장으로** 되살아나면 잡는다 — 굵기·띄어쓰기 무관 (2026-09-22 ③).
    #  현행 문턱은 손으로 안 적는다: 자료에서 '식이 맞는 셋' 의 최악값으로 만든다.
    dev, _ = _prot_deviation(rows, full)
    good = sorted(c for c in dev if dev[c] <= 3.11)
    assert len(good) == 3, good
    thresh = max(dev[c] for c in good)
    viol = _resume_block_violations(blk, thresh)
    assert not viol, viol

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
    # ⛔ 2026-09-28 뒤집음 — 종전 이 시험은 창 폭(oxidation − reduction_limit_V)이 화면에 **있어야** 통과했다.
    #   그런데 reduction_limit_V 는 '아직 Li 를 흡수하는 단계' 를 집는 계통 오류다 (HZ-esw-reduction-limit-label ·
    #   2026-09-22). 원장만 고쳐지고 화면·시험은 따라가지 않아 **막힌 숫자를 시험이 강제**하고 있었다.
    #   ⇒ 환원 쪽은 같은 원장 profile 에서 **Li 교환이 0 인 첫 경계**로 다시 읽고, 옛 값·창 폭은 **없어야** 한다.
    for sysn in ("comp1", "modelc", "lpsocl", "modelc_nd"):
        prof = sorted(esw[sysn]["profile"], key=lambda e: e["V_vs_Li"])
        red = next(e["V_vs_Li"] for e in prof if abs(e["evolution_Li"]) < 1e-6)
        ox = min(e["V_vs_Li"] for e in prof if e["evolution_Li"] < -1e-6)
        assert abs(ox - esw[sysn]["oxidation_limit_V"]) < 1e-9, f"{sysn}: 첫 Li 방출 {ox} ≠ oxidation_limit_V (원장 자체 모순)"
        assert f"{red}" in s0, f"{sysn}: 교환 0 첫 경계 {red} V 가 §0 에 없다"
        assert f"{ox}" in s0, f"{sysn}: 산화 onset {ox} V 가 §0 에 없다"
        bad = esw[sysn]["reduction_limit_V"]
        assert f"{bad}" not in s0, f"{sysn}: 계통 오류 값 reduction_limit_V {bad} 가 §0 에 남아 있다"
        w_bad = esw[sysn]["oxidation_limit_V"] - bad
        assert f"{w_bad:.3f}" not in s0, f"{sysn}: 막힌 창 폭 {w_bad:.3f} 가 §0 에 남아 있다"
    assert "HZ-esw-reduction-limit-label" in s0, "환원 열을 다시 읽은 근거(위험 원장 id)가 화면에 없다"
    assert "산화 쪽뿐" in s0 or "산화 쪽에서만" in s0, "Nd 가 산화 쪽만 움직인다는 문장이 없다"
    # 해석과 측정을 갈라 적었는가
    assert "해석" in s0 and "측정된 것은" in s0, "'황친화' 가 해석이라는 구분이 없다"


def test_s0_conclusion_keeps_the_onset_and_coating_claims_honest(client):
    """⛔음성 — §0 결론 단락 (2026-09-28 같이 읽기에서 잡은 셋).

    ① 'onset 은 건드리지 않는다' — 같은 §0 머리 줄·반응식이 2.14 → 1.92 V 로 **내린다**고 쓴다.
    ② 코팅 비유를 G5 단서 없이 쓰기 — 연속성·두께·Li⁺ 전도는 계산에 없다 (§6 G5).
    ③ 'Li 를 안 쓰는 방' 을 Nd 만의 차별점처럼 쓰기 — 무도핑 TM 인산염도 Li/P = 0 이다.
       차이는 **방을 누가 대느냐** (양극을 헐어서 · 전해질이 제자리에서).
    """
    s0 = _section(_report_html(client), "s0")
    i0 = s0.index("그래서 창이 아니라 산물을 본다"); i1 = s0.index("읽는 순서", i0)
    concl = s0[i0:i1]
    assert "건드리지 않" not in concl, "① Nd 는 onset 을 2.14 → 1.92 V 로 내린다 — '안 건드린다' 는 §0 과 모순"
    assert "올리지 못한다" in concl and "1.92" in concl, "① 'onset 을 올리지 못한다 · 오히려 내린다' 가 없다"
    assert "G5" in concl and "Li⁺" in concl, "② 코팅 비유에 G5 단서(Li⁺ 통과 등 미계산)가 없다"
    assert "양쪽 다" in concl and "누가 대느냐" in concl, "③ 차별점이 'Li 를 안 쓴다' 로 읽힌다 — 방을 누가 대느냐가 없다"
    assert "Li 하나" in concl, "③ LiNd(PO₃)₄ 에 Li 가 있다는 단서가 없다"


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


def test_s0_scopes_the_pdos_to_the_x020_cell(client):
    """⛔음성 — x = 0.20 셀의 PDOS 가 x = 0.02 이야기로 조용히 번지면 잡는다 (2026-09-28 판).

    ESW 는 x = 0.02 두 자리로 다시 쟀고 onset 이 그대로였다. PDOS 만 x = 0.20 Li 자리 셀이다 —
    구조가 필요한 계산이라 x = 0.02 셀(약 618 원자)로 못 옮겼다. 그 이름표가 §0 에 있어야 한다.
    """
    s0 = _section(_report_html(client), "s0")
    assert "x = 0.20 셀" in s0 and "618 원자" in s0, "PDOS 가 x = 0.20 셀이라는 이름표가 없다"
    assert "추론이지 계산이 아니다" in s0, "'x 가 작으면 Nd 몫이 작을 것' 이 추론이라는 한정이 없다"
    assert "P 자리" in s0 and "부호가 반대" in s0, "PDOS 를 P 자리로 못 옮기는 이유가 없다"


# ── x = 0.02 전환 (2026-09-28) ─────────────────────────────────────────────────
#   왜: 1저자가 화면 전체를 Nd x = 0.02 로 옮기라고 했다 (D-2026-09-28-cei-page-x002).
#   화면의 x = 0.02 수는 전부 원자료(cei_interface_V_x002 · cei_esw_Li_x002)와 판정·결과 기록에서
#   왔다 — 문자열이 아니라 **값으로** 묶는다. 화면이나 원장 한쪽만 고치면 여기서 빨개진다.
X002_IFACE = REPORT.parents[3] / "db/properties/cei_interface_V_x002_2026_09_28.json"
X002_ESW = REPORT.parents[3] / "db/properties/cei_esw_Li_x002_2026_09_28.json"
X002_VERD = REPORT.parents[3] / "db/properties/cei_x002_verdicts_2026_09_28.json"
X002_RES = REPORT.parents[3] / "db/properties/cei_x002_result_2026_09_28.json"


def _x002_tool():
    """판정 코드는 **도구 한 곳**에만 있다 — 시험이 몫을 따로 세면 두 판정이 갈린다."""
    import importlib.util
    src = REPORT.parents[3] / "tools/oxidation/interface_reactivity_v2.py"
    spec = importlib.util.spec_from_file_location("iface_v2_x002", src)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _x002_limatched_range():
    """결과 기록의 x = 0.02 Li 맞춤 Nd 항(4.5 V · 끝점 뺀 칸) — (가장 음수, 가장 덜 음수)."""
    r = json.loads(X002_RES.read_text("utf-8"))["1_게이트"]["G5_Li_맞춤_대조"]["Nd항_4.50V_양극별_meV_per_atom"]
    vals = [v for k in ("Li자리_x002", "P자리_x002", "1저자조성") for v in r[k].values() if v is not None]
    assert vals, "Li 맞춤 값을 못 읽었다 — 시험이 헛것을 재고 있다"
    return min(vals), max(vals)


def test_x002_esw_rows_match_the_record(client):
    """⛔음성 — §0 표의 x = 0.02 행(산화 onset · 환원 교환 0 경계)이 x = 0.02 ESW 원장과 값으로 같다.

    ⚠ 환원 칸은 reduction_limit_V 가 아니라 profile 의 '교환 0 첫 경계' 다 (HZ-esw-reduction-limit-label).
    """
    esw = json.loads(X002_ESW.read_text("utf-8"))["results"]
    s0 = _section(_report_html(client), "s0")
    for lab in ("comp1", "modelc", "lpsocl", "o_only_003", "ndo_li_002", "nd_p_002_asused", "modelc_nd"):
        row = re.search(r'<tr><td class="mono">%s \([^<]*</td>(.*?)</tr>' % lab, s0, re.S)
        assert row, f"§0 표에 {lab} 행이 없다"
        cells = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row.group(1), re.S)]
        assert float(cells[0]) == esw[lab]["oxidation_limit_V"], (lab, cells)
        prof = sorted(esw[lab]["profile"], key=lambda e: e["V_vs_Li"])
        red = next(e["V_vs_Li"] for e in prof if abs(e["evolution_Li"]) < 1e-6)
        assert float(cells[1]) == red, (lab, cells, "교환 0 첫 경계", red)
    assert "x 와 무관" in s0 and "0.016" in s0, "1.92 V 가 x 와 무관하고 양만 준다는 설명이 없다"


def test_x002_series_card_shares_match_the_raw(client):
    """⛔음성 — 계열 카드 'LiCoO₂ 4.3 V · P 가 간 곳' 표가 원자료 반응식에서 **다시 센** 몫과 같다."""
    T = _x002_tool()
    R = json.loads(X002_IFACE.read_text("utf-8"))["results"]["LiCoO2"]["reactions"]["4.30"]
    labs = ("modelc", "ndo_li_002", "nd_p_002_asused", "modelc_nd")
    h = _report_html(client)
    i = h.index("왜 0.20 에서 0.02 로 옮겼나")
    card = h[i:h.index("</table>", i)]
    rows = re.findall(r"<tr><td[^>]*>(.*?)</td><td[^>]*>([\d.]+) %</td><td[^>]*>([\d.]+) %</td></tr>", card)
    assert len(rows) == 4, f"표 행이 넷이 아니다: {rows} — 시험이 헛것을 재고 있다"
    for (name, nd, tm), lab in zip(rows, labs):
        sh = T.x002_p_share(R[lab])
        assert abs(float(nd) - 100 * sh["dopant_phosphate"]) < 0.6, (lab, name, nd, sh)
        assert abs(float(tm) - 100 * sh["tm_phosphate"]) < 0.6, (lab, name, tm, sh)


def test_x002_decomposition_table_matches_the_verdicts(client):
    """⛔음성 — §1 분해표(두 자리 × 전압 6)가 판정 파일의 전압별 Δ 와 **값으로** 같다."""
    V = json.loads(X002_VERD.read_text("utf-8"))["sites"]
    s1 = _section(_report_html(client), "s1")
    i = s1.index("Li 자리 (x = 0.02)")
    tbl = s1[i:s1.index("</table>", i)]
    rows = re.findall(r"<tr><td>([\d.]+)</td>(.*?)</tr>", tbl, re.S)
    assert len(rows) == 6, f"전압 행이 6 이 아니다: {len(rows)} — 시험이 헛것을 재고 있다"
    for vtxt, rest in rows:
        got = [float(x.replace("−", "-")) for x in re.findall(r">([−+-]?\d+\.\d+)<", rest)]
        k = f"{float(vtxt):.2f}"
        want = [V["Li"]["delta_by_V"]["nd"][k], V["Li"]["delta_by_V"]["o"][k], V["Li"]["delta_by_V"]["both"][k], None,
                V["P"]["delta_by_V"]["nd"][k], V["P"]["delta_by_V"]["o"][k], V["P"]["delta_by_V"]["both"][k], None]
        assert len(got) == len(want), (vtxt, got)
        for g, w in zip(got, want):
            if w is not None:
                assert abs(g - w) < 6e-5, (vtxt, g, w)


def test_x002_s2_nd_share_table_matches_the_raw(client):
    """⛔음성 — §2 'Nd 가 가는 상과 그 몫' 표(1저자 조성)가 원자료 반응식에서 다시 센 값과 같다.

    끝점(자체분해) 칸은 숫자 대신 '끝점' 이어야 한다 — 0 으로 그리면 없는 값을 0 으로 읽힌다.
    """
    T = _x002_tool()
    R = json.loads(X002_IFACE.read_text("utf-8"))["results"]
    s2 = _section(_report_html(client), "s2")
    i = s2.index("x = 0.02 에서 Nd 가 가는 상과")
    tbl = s2[i:s2.index("</table>", i)]
    rows = re.findall(r"<tr><td><strong>([\d.]+)</strong></td>(.*?)</tr>", tbl, re.S)
    assert len(rows) == 6, f"전압 행이 6 이 아니다: {len(rows)}"
    for vtxt, rest in rows:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", rest, re.S)
        assert len(cells) == 4, (vtxt, cells)
        k = f"{float(vtxt):.2f}"
        for cat, cell in zip(("LiCoO2", "LiNiO2", "LiMnO2", "NMC811"), cells):
            if R[cat]["endpoint_degenerate"][k]["nd_p_002_asused"] is not False:
                assert "끝점" in cell, (cat, k, cell)
                continue
            sh = T.x002_p_share(R[cat]["reactions"][k]["nd_p_002_asused"])
            pct = int(re.search(r"<b>(\d+) %</b>", cell).group(1))
            assert pct == round(100 * sh["dopant_phosphate"]), (cat, k, pct, sh)


def test_x002_li_matched_range_and_minus_50p8_scope(client):
    """⛔음성 — Li 맞춤 Nd 항의 x = 0.02 범위가 원장과 같고, 옛 −50.8 은 **양극 한정과 함께만** 나온다.

    왜: 2026-09-28 에 '−50.8 meV/atom' 이 LiCoO₂ 한 양극의 값인데 일반값처럼 적혀 있던 것을 찾았다.
    """
    lo, hi = _x002_limatched_range()
    txt = f"{hi:.1f} ~ {lo:.1f}".replace("-", "−")
    h = _report_html(client)
    for sec in ("s0b", "s1", "s9"):
        assert txt in _section(h, sec), f"{sec} 의 Li 맞춤 범위가 원장({txt})과 다르다"
    hits = list(re.finditer("−50\\.8", h))
    assert hits, "−50.8 이 한 번도 없다 — 시험이 헛것을 재고 있다"
    for m in hits:
        ctx = h[max(0, m.start() - 200): m.end() + 200]
        assert "LiCoO₂" in ctx or "−22.8" in ctx, f"−50.8 이 양극 한정 없이 쓰였다: …{ctx[140:280]}…"


def test_x002_kink_and_dopant_axes_match_the_record(client):
    """⛔음성 — §4 Nd 인산염 kink 수와 §5 의 x = 0.02 세 축이 결과 기록과 값으로 같다."""
    res = json.loads(X002_RES.read_text("utf-8"))
    h = _report_html(client)
    s4 = _section(h, "s4")
    for lab in ("ndo_li_002", "nd_p_002_asused"):
        frac = res["3_혼합범위"]["Nd인산염_kink"][lab]
        assert frac in s4, f"§4 에 {lab} 의 kink 수 {frac} 가 없다"
    s5 = _section(h, "s5")
    for M, v in res["4_도펀트_x002"].items():
        row = re.search(r"<tr[^>]*><td>%s(?: ★)?</td>(.*?)</tr>" % M, s5, re.S)
        assert row, f"§5 표에 {M} 행이 없다"
        vals = [float(x.replace("−", "-")) for x in re.findall(r">([−+-]?\d+\.\d+)<", row.group(1))]
        # 열 순서: B · MPO4 깊이 · 계면 Δ(x002) · kink %(x002) · 반경 · 닫힌계(x002)
        assert abs(vals[2] - v["계면_Δ_vs_base_4.50V_LiCoO2_eV_per_atom"]) < 6e-6, (M, vals, v)
        assert abs(vals[3] - v["M인산염_kink_비율_percent"]) < 0.06, (M, vals, v)
        assert abs(vals[5] - v["닫힌계_0V_LiCoO2_eV_per_atom"]) < 6e-6, (M, vals, v)


def test_x002_g4_closure_matches_the_ledger(client):
    """⛔음성 — G4 마감 상태가 원장 · 결과 기록 · 화면에서 같다 (1저자 2026-09-28 'ㅇㅇ 그렇게 해줘').

    G4 는 적힌 그대로 위반 9 이고, 원인(반응식 계수 반올림)이 규명돼 1저자가 그대로 닫았다.
    잡는 것 셋: ① 원장은 닫혔는데 화면에 '확인 대기' 가 남는 것 ② 화면이 G4 를 '통과' 로
    격상하는 것 ③ 결과 기록에서 '위반 9' 이력이 지워지는 것.
    """
    did = "D-2026-09-28-cei-x002-result"
    ds = {d["id"]: d for d in json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]}
    assert did in ds, f"원장에 {did} 가 없다 — 시험이 헛것을 재고 있다"
    d = ds[did]
    assert Path(d["record"]).name == X002_RES.name, "결정이 x = 0.02 결과 기록을 안 가리킨다"
    res = json.loads(X002_RES.read_text("utf-8"))
    g4 = res["1_게이트"]["G4_상한"]
    assert len(g4["위반_칸"]) == 9 and g4["적힌_그대로"].startswith("위반 9"), "위반 이력이 지워졌다"
    closed = d["decision_state"] == "active"
    assert (res["status"] == "ratified") == closed, (res["status"], d["decision_state"])
    assert g4["상태"].startswith("닫힘") == closed, g4["상태"][:40]
    h = _report_html(client)
    ctx = [h[max(0, m.start() - 300): m.end() + 500] for m in re.finditer(r"G4", h)]
    x002 = [c for c in ctx if "적힌 그대로" in c and "위반" in c]
    assert len(x002) >= 2, f"화면의 x = 0.02 G4 문구가 {len(x002)} 곳뿐이다 (§2 주 · 꼬리말)"
    for c in x002:
        assert "원인 규명" in c, "G4 문구에 원인 규명이 없다"
        if closed:
            assert "확인 대기" not in c, "원장은 닫혔는데 화면이 아직 '확인 대기' 다"
            assert did in c, "G4 문구가 마감 결정을 안 가리킨다"
    assert not re.search(r"G4\s*(?:는|은|가|이|:)?\s*[‘'\"]?통과", h), "화면이 G4 를 '통과' 로 격상했다"


X010_VERD = REPORT.parents[3] / "db/properties/cei_x010_verdicts_2026_09_28.json"
X010_RES = REPORT.parents[3] / "db/properties/cei_x010_result_2026_09_28.json"
X010_RAW = REPORT.parents[3] / "db/properties/cei_interface_V_x010_2026_09_28.json"


def test_x010_curvature_line_matches_the_result(client):
    """⛔음성 — 머리 2×2 의 x = 0.10 곡률 문장이 판정 파일 · 결과 기록 · 원자료와 **값으로** 같다.

    사슬 셋을 다 묶는다: ① 결과 기록의 GC 수 = gabia 판정 파일 ② 결과 기록의 칸별 초과 목록 =
    원자료에서 도구(x010_cell_residuals)로 다시 센 것 ③ 화면 숫자 = 결과 기록.
    잡는 것: 판정이 불통과인데 화면이 '직선 위' 라고 쓰는 것 · 옛 문장('곡률은 못 본다')이 남는 것.
    """
    V = json.loads(X010_VERD.read_text("utf-8"))["GC_curvature"]
    res = json.loads(X010_RES.read_text("utf-8"))
    gc = res["1_게이트"]["GC_곡률"]
    assert set(gc) == {"Li", "P"} == set(V), "자리가 둘이 아니다 — 시험이 헛것을 재고 있다"
    for s in ("Li", "P"):
        for k in ("n_cells", "residual", "tol", "pass", "info_n_cells_over_tol", "info_max_abs_cell_residual"):
            assert gc[s][k] == V[s][k], (s, k, gc[s][k], V[s][k])
    cells = _x002_tool().x010_cell_residuals(json.loads(X010_RAW.read_text("utf-8"))["results"])
    over = res["1_게이트"]["GC_칸별_초과_정보"]["칸"]
    for s in ("Li", "P"):
        want = [r for r in cells[s] if abs(r["residual"]) > gc[s]["tol"]]
        assert over[s] == want, (s, over[s], want)
        assert len(want) == gc[s]["info_n_cells_over_tol"], s
    h = _report_html(client)
    m = re.search(r'<span id="x010-curvature">(.*?)</span></li>', h, re.S)
    assert m, "화면에 x = 0.10 곡률 문장이 없다"
    t = m.group(1)
    assert "곡률은 못 본다" not in h, "옛 문장('두 점으로 잰 선형성이라 곡률은 못 본다')이 남았다"
    got = _nums(t)
    for s in ("Li", "P"):
        assert round(gc[s]["residual"], 4) in got, (s, "평균 어긋남", gc[s]["residual"], sorted(got))
        assert round(gc[s]["info_max_abs_cell_residual"], 4) in got, (s, "칸별 최대", sorted(got))
        assert f"{s} {gc[s]['n_cells']}" in t, (s, "칸 수", gc[s]["n_cells"])
        top = over[s][0]
        assert f"{top['cathode'].replace('O2', 'O₂')} {float(top['V']):.1f} V" in t, (s, "넘은 칸 이름", top)
    assert gc["Li"]["tol"] in got, "문턱이 화면과 다르다"
    passed = all(gc[s]["pass"] is True for s in ("Li", "P"))
    assert ("직선 위다" in t) == passed, "판정과 화면 문장이 어긋난다"
    assert "점 하나" in t and "안쪽" in t, "'점 하나 · 안쪽 꺾임은 못 봤다' 한정이 빠졌다"


def test_x010_row_on_the_2x2_matches_the_raw(client):
    """⛔음성 — 머리 2×2 의 가운데 x = 0.10 행이 원자료에서 도구로 다시 잰 **공통 20 칸** 평균과 같고,
    두 화면(보고서 표 · Nd 카드)에 같은 값이 있다 (2026-09-29 · 1저자 '0.1도 돌렸잖앙 … 넣자').

    사슬: ① 원자료 → _x002_cells · _x002_mean (09-19 공통기준 규약) = 결과 기록 ★_표_x010_행_공통기준
    ② 여섯 조성 공통 칸이 09-19 네 조성 공통 칸과 **같은 20 칸** ③ 같은 칸에서 09-19 네 값이 재현된다
    ④ 보고서 표 · Nd 카드에 두 값.
    잡는 것: 0.10 행을 다른 묶음(GC 의 Li 23 칸 평균 0.0216)에서 뽑아 표에 섞는 것 · 한 화면만 고치는 것.
    """
    tool = _x002_tool()
    raw = json.loads(X010_RAW.read_text("utf-8"))["results"]
    rec = json.loads(X010_RES.read_text("utf-8"))["★_표_x010_행_공통기준"]
    four = ["nd_li_002", "nd_p_002", "nd_only", "nd_p_020"]
    c4 = tool._x002_cells(raw, four)
    c6 = tool._x002_cells(raw, four + ["nd_li_010", "nd_p_010"])
    assert len(c6) == 20 and sorted(c4) == sorted(c6), ("공통 칸이 09-19 의 20 칸이 아니다", len(c4), len(c6))
    got = {"Li자리_x010": tool._x002_mean(raw, c6, "nd_li_010"),
           "P자리_x010": tool._x002_mean(raw, c6, "nd_p_010")}
    for k, v in got.items():
        assert abs(rec["표_행"][k]["값"] - v) < 5e-6, (k, "결과 기록", rec["표_행"][k]["값"], "원자료", v)
    for k, lab in (("Li자리_x002", "nd_li_002"), ("P자리_x002", "nd_p_002"),
                   ("Li자리_x020", "nd_only"), ("P자리_x020", "nd_p_020")):
        assert abs(_site_2x2()[k] - tool._x002_mean(raw, c6, lab)) < 1e-5, (k, "09-19 값이 같은 칸에서 재현되지 않는다")
    h = _report_html(client)
    i = h.find("빠진 칸을 채웠다")
    assert i > 0, "2×2 카드를 못 찾았다 — 시험이 헛것을 재고 있다"
    seen = _nums(h[i:h.index("</table>", i)])
    seen_card = _nums(json.dumps(V.interpretation_cards_for(ND), ensure_ascii=False))
    for k, v in got.items():
        assert any(abs(x - v) < 5e-5 for x in seen), (k, "보고서 2×2 표에 없다", v, sorted(seen))
        assert any(abs(x - v) < 5e-5 for x in seen_card), (k, "Nd 카드에 없다", v)
    assert "0.02 · 0.10 · 0.20 을 잇는 다리다" in h, "머리 문장이 아직 '0.02 와 0.20 을 잇는' 이다"


GA_VERD = REPORT.parents[3] / "db/properties/cei_ga_verdicts_2026_09_29.json"
GA_RES = REPORT.parents[3] / "db/properties/cei_ga_result_2026_09_29.json"
GA_RAW = REPORT.parents[3] / "db/properties/cei_interface_V_ga_2026_09_29.json"


def test_ga_additivity_line_matches_the_result(client):
    """⛔음성 — 'Li 를 맞춰도 더해진다' 문장이 판정 파일 · 결과 기록 · 원자료와 **값으로** 같고,
    판정이 두 자리 다 통과일 때만 옛 조건('Li 를 보정하지 않으면')이 떨어진다
    (2026-09-29 · 1저자 '이건 시뮬레이션 돌릴 수 있는거 있어?' → GA 사전등록 · gabia).

    사슬: ① 원자료 → 도구(ga_verdicts)로 다시 낸 판정 = gabia 판정 파일 ② 결과 기록의 GA 수 = 판정 파일
    ③ 화면(§0b span#ga-additivity · §1 그림 설명)의 잔차·칸 수·문턱 = 판정 파일
    ④ 통과면 옛 조건 문장과 목차의 '(Li 미보정)' 이 없다.
    잡는 것: 판정은 한 값인데 화면이 다른 값을 쓰는 것 · 불통과인데 조건을 떼는 것 · 한 화면만 고치는 것.
    """
    tool = _x002_tool()
    raw = json.loads(GA_RAW.read_text("utf-8"))
    rv = tool.ga_verdicts(raw["results"], repro=raw.get("reproduce_check"))
    V = json.loads(GA_VERD.read_text("utf-8"))
    rec = json.loads(GA_RES.read_text("utf-8"))["1_게이트"]["GA_가산성"]
    assert set(V["GA_additivity"]) == {"Li", "P"}, "자리가 둘이 아니다 — 시험이 헛것을 재고 있다"
    for s in ("Li", "P"):
        g = V["GA_additivity"][s]
        for k in ("n_cells", "residual", "pass", "tol"):
            assert rv["GA_additivity"][s][k] == g[k], (s, k, "원자료 재판정", rv["GA_additivity"][s][k], "판정 파일", g[k])
            assert rec[s][k] == g[k], (s, k, "결과 기록", rec[s][k], "판정 파일", g[k])
        assert V["design_pairs"][s]["ok"] is True, (s, "짝 검사가 통과하지 않은 판정을 화면에 올렸다")
    h = _report_html(client)
    m = re.search(r'<span id="ga-additivity">(.*?)</span>', _section(h, "s0b"), re.S)
    assert m, "§0b 에 Li 맞춤 가산성 문장이 없다"
    t = m.group(1)
    got = _nums(t)
    passed = all(V["GA_additivity"][s]["pass"] is True for s in ("Li", "P"))
    for s in ("Li", "P"):
        g = V["GA_additivity"][s]
        assert round(g["residual"], 6) in got, (s, "잔차", g["residual"], sorted(got))
        assert f"{s} {g['n_cells']}" in t, (s, "칸 수", g["n_cells"])
    assert V["tol"] in got, "문턱이 화면과 다르다"
    assert ("마찬가지다" in t) == passed, "판정과 화면 문장이 어긋난다"
    s1 = _nums(_section(h, "s1"))
    for s in ("Li", "P"):
        assert round(V["GA_additivity"][s]["residual"], 6) in s1, (s, "§1 그림 설명에 잔차가 없다")
    #: §1 사전등록 판정 목록의 GA 줄 (2026-09-29 추가) — 잔차 · 칸 수 · 문턱 · 통과 여부가 판정 파일과 같다
    li = re.search(r'<li id="s1-ga">(.*?)</li>', _section(h, "s1"), re.S)
    assert li, "§1 판정 목록에 GA 줄이 없다"
    lt = li.group(1)
    for s in ("Li", "P"):
        g = V["GA_additivity"][s]
        assert round(g["residual"], 6) in _nums(lt), (s, "§1 GA 줄 잔차", g["residual"])
        assert f"{s} {g['n_cells']}" in lt, (s, "§1 GA 줄 칸 수", g["n_cells"])
    assert V["tol"] in _nums(lt), "§1 GA 줄 문턱이 판정 파일과 다르다"
    assert ("<b>통과</b>" in lt) == passed, "§1 GA 줄의 통과 표기가 판정과 어긋난다"
    if passed:
        assert "보정하지 않으면 두 효과가 그냥 더해진다" not in h, "GA 통과인데 옛 조건 문장이 남았다"
        assert "분해 (Li 미보정)" not in h, "GA 통과인데 목차에 옛 조건 표지가 남았다"


#: §1 조성표의 행 순서 = 원자료 라벨 (화면 이름은 사람용이라 라벨로 대조한다)
_S1_COMP_LABELS = ("modelc", "lpsocl", "o_only_003", "nd_li_002", "ndo_li_002", "nd_p_002", "nd_p_002_asused",
                   "lim_li_002", "lim_li_002_o", "lim_p_002", "lim_p_002_asused")
_OX = {"Li": 1, "Nd": 3, "P": 5, "S": -2, "O": -2, "Cl": -1}


def test_s1_composition_table_matches_the_raw(client):
    """⛔음성 — §1 조성표의 조성 · Nd · O · 전하 칸이 원자료 반응식의 전해질 조성에서 **다시 센** 값과 같다.

    왜 (2026-09-29): Li 맞춤 대조 넷(위 Nd 조성에서 Nd 만 뺀 것 · 전하 −0.06 은 설계)을 표에 올렸다.
      조성을 손으로 옮겨 적으면 한 글자만 틀려도 **다른 대조**가 된다 — x002 · GA 실행 원자료의
      반응식 좌변(도구 `_ga_formula`)과 대조한다. 전하는 형식 산화수로 다시 센다
      (Li +1 · Nd +3 · P +5 · S −2 · O −2 · Cl −1) — '0 ✓' 는 0 일 때만 붙는다.
    """
    T = _x002_tool()
    srcs = (json.loads(X002_IFACE.read_text("utf-8"))["results"], json.loads(GA_RAW.read_text("utf-8"))["results"])
    s1 = _section(_report_html(client), "s1")
    i = s1.index("<th>이름</th><th>조성</th>")
    tbl = s1[i:s1.index("</table>", i)]
    rows = re.findall(r'<tr><td[^>]*>(?:(?!</td>).)*</td><td class="mono">([^<]+)</td>'
                      r'<td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td></tr>', tbl, re.S)
    assert len(rows) == len(_S1_COMP_LABELS), f"조성 행이 {len(rows)} 개다 — 시험이 헛것을 재고 있다"
    for (formula, nd, ox, q), lab in zip(rows, _S1_COMP_LABELS):
        got = T.parse_formula(formula.replace(" ", ""))
        raw = next((c for c in (T._ga_formula(r, lab) for r in srcs) if c), None)
        assert raw, f"{lab}: 원자료에서 조성을 못 읽었다"
        for el in set(got) | set(raw):
            assert abs(got.get(el, 0) - raw.get(el, 0)) < 1e-6, (lab, formula, el, got, raw)
        assert float(nd) == got.get("Nd", 0) and float(ox) == got.get("O", 0), (lab, nd, ox, got)
        charge = sum(_OX[el] * n for el, n in got.items())
        assert abs(charge - float(q.replace("✓", "").replace("−", "-"))) < 1e-6, (lab, q, charge)
        assert ("✓" in q) == (abs(charge) < 1e-6), (lab, q, "✓ 는 전하 0 일 때만")



def test_prot_counts_dies_when_the_grid_is_broken():
    """⛔음성 — 시험 쪽 전농도통과 판정도 격자가 깨지면 **세지 않고 죽는다** (2차 리뷰 ①②).

    왜: 탈락 행 3 개를 지우면 종전 `_prot_counts` 는 LiMnO₂ 4.0 V 를 전농도통과로 올려
    18 을 냈고, 생성기는 17 을 냈다 — 같은 질문에 두 답. 이제 한 함수라 둘 다 죽는다.
    """
    import pytest as _pt
    rows = _prot_rows()
    n_all, n_pass, n_fail, n_col, full = _prot_counts(rows)
    assert (n_all, n_col, len(full)) == (120, 24, 17), (n_all, n_col, len(full))
    #: 생성기가 자기 load() 로 센 것과 형 변환을 거친 시험 쪽이 같다 — 어댑터 검사
    P = _gen()
    assert len(P._full_pass(P.load())) == len(full)
    dropped = [r for r in rows if not (r["cathode"] == "LiMnO2" and r["voltage_V"] == "4.0"
                                       and r["gate_pass"] != "True")]
    with _pt.raises(SystemExit, match="농도 집합이 다르다"):
        _prot_counts(dropped)
    stray = list(rows) + [dict(rows[0], x_Nd="0.25")]
    with _pt.raises(SystemExit, match="농도 집합이 다르다"):
        _prot_counts(stray)


def test_resume_block_checker_catches_unbolded_retracted_claim():
    """⛔음성 — ⏭ 검사기가 굵기 없는 재주장·다른 문턱을 실제로 잡는다 (2차 리뷰 ③).

    시험을 쓴 뒤 대상을 일부러 깨서 빨간불을 본다 — 검사기 자체를 여기서 깬다.
    """
    ok_blk = "집계 … 식이 **≤3.1 %p** 로 맞는 열은 **셋뿐**이다. ⏭ 블록에 철회된 ≤2.5 %p 잔존 · 고정 문자열"
    assert _resume_block_violations(ok_blk, 3.0991) == []
    #: 굵기 없이 되살린 철회 문턱 — 종전 시험은 이걸 **통과**시켰다
    esc = ok_blk + " 식이 ≤2.5 %p 로 맞는 열은 셋뿐이다(LiCoO₂ 4.30 V · LiNiO₂ 3.50 V · NMC811 3.50 V)."
    assert any("2.5" in v for v in _resume_block_violations(esc, 3.0991)), "굵기 없는 재주장을 놓쳤다"
    #: 굵기 있는 재주장도, 괄호 삽입도 잡는다
    assert _resume_block_violations(ok_blk + " 식이 **≤2.5 %p**(예측식 기준) 으로 맞는다", 3.0991)
    #: 현행 주장이 하나도 없으면 그것도 위반이다
    assert _resume_block_violations("아무 말도 없다", 3.0991)
    #: 같은 뜻의 다른 표기(세 개뿐)는 위반이 아니다 — 스냅숏이 아니라 주장 검사다
    assert _resume_block_violations("식이 ≤3.1 %p 로 맞는 열은 세 개뿐", 3.0991) == []
