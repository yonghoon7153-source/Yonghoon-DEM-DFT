#!/usr/bin/env python3
"""test_v3_cascade_sdcp.py — v3 묶음 E(캠페인 감사: `/cascade` · `/sdcp`) 회귀 시험.

여기 담은 건 전부 **실제로 한 번 틀렸던 것**이다.
  · `/cascade` 가 자기 지위를 몰랐다 — 회신 AL NO-GO(08-30)·09-08 보고량 카드 비준·
    cascade #7 봉인이 화면에 한 글자도 없었고, 화면 최신 날짜가 2026-08-25 였다
  · 2026-08-12 에 **해소된** 값 충돌이 '미해소' 빨간 제목 아래 떠 있었고, 그 값이
    dict 라 `|bold` 가 **파이썬 repr 을 이스케이프해 화면에 노출**했다
  · 딥링크 핸들러가 `r.cells[1]` undefined 로 TypeError 를 내고, 같은 script 블록의
    THEMES/TDOP 할당을 통째로 죽여 🎯 테마 탭이 안 돌았다(페이지가 뿌리는 칩 48개)
  · manifest 미등재 v1 산출물 셋(champions 141행·litransport·synergy)이 기본 DOM 에
    전량 실렸다 — 같은 파일을 `/api/file` 로 받으면 403 인데 화면은 내보냈다
  · SDCP wave1 인용 게이트가 키 모양 불일치(`조각_시드` vs `조각`)로 **영원히
    CITABLE 0** 이었다. 원장에 `dE_site_meV/ptfe_dimer_pm1 = 36.071` 로 등록된 값을
    화면이 "등록돼 있지 않다" 고 말했다

⚠ 시험마다 **음성 경로**(틀린 입력을 잡아내는지)를 같이 둔다. 양성만 있는 시험은
  통과해도 아무것도 보증 못 한다 — 그게 정확히 이 게이트가 영구히 잠긴 채 전 시험을
  통과한 이유다(기존 게이트 시험이 음성 3개뿐이었다).

⛔ 이 시험이 **못 하는 것**
  · 어느 조각·시드가 인용 가능해야 **옳은지** 판정하지 않는다. 원장이 등록한 것과
    화면이 세는 것이 같은가만 본다.
  · 밴드에 실린 문장이 물리적으로 맞는지 보지 않는다. 비준 카드에서 왔는가만 본다.
  · 브라우저를 안 띄운다. 딥링크 가드는 **소스 문자열**로 확인한다 — JS 를 실행해
    TypeError 가 안 나는지까지는 못 본다.

    pytest webapp/tests/test_v3_cascade_sdcp.py -q
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

CASCADE_HTML = ROOT / "webapp" / "templates" / "cascade.html"
BAND_HTML = ROOT / "webapp" / "templates" / "_campaign_band.html"
EST_JSON = ROOT / "db" / "properties" / "cascade_d_rel_estimand_2026_09_08.json"
SEAL_JSON = ROOT / "db" / "properties" / "cascade_seal_v2_2026_09_08.json"


@pytest.fixture(scope="module")
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


def _tbody(html: str, tid: str) -> str:
    m = re.search(r'id="' + tid + r'".*?<tbody>(.*?)</tbody>', html, re.S)
    return m.group(1) if m else ""


# ══════════════════════════════════════════════════════════════════════════
# P0-07 — SDCP wave1 인용 게이트: 키 모양 정합
# ══════════════════════════════════════════════════════════════════════════
def test_wave1_gate_allowlist_key_shape_is_fragment_seed():
    """allow-list 는 `<조각>_<시드>` 다 — 조회도 같은 모양이어야 한다.

    ⛔ 이게 갈려 있어서 게이트가 영구히 잠겼다(CITABLE 0). 모양이 다시 갈리면
      화면이 원장에 있는 값을 '없다' 고 말한다.
    """
    g = D._wave1_gate()
    assert not g["source_missing"], "인용 원장을 못 읽었다 — 픽스처가 아니라 정본 문제다"
    keys = g["citable_dE"]
    assert keys, "dE_site_meV allow-list 가 비었다"
    assert g.get("citable_key_shape") == "fragment_seed"
    # 원장 키가 실제로 `<조각>_<시드>` 인가 (맨 조각 이름만 있으면 게이트 의미가 바뀐다)
    assert any(k.startswith("ptfe_dimer_") for k in keys), sorted(keys)
    # dE_notes 는 반대로 **조각 단위** 키다 — 두 모양이 공존한다는 사실 자체를 못박는다
    assert "ptfe_dimer" in g["dE_notes"], "dE_notes 가 조각 키가 아니다 — 사유가 빈다"


def test_wave1_status_seed_gating_positive_and_negative():
    """양성 + 음성 — 시드별 게이팅이 **좁아지는** 방향인지 본다."""
    from data import _wave1_status
    gate = {"source_missing": False,
            "citable_dE": {"ptfe_dimer_pm1"},
            "dE_notes": {"ptfe_dimer": "허용 문구"}, "hazards_by_fragment": {}}

    # 양성: 원장에 등록된 조각_시드 조합만 통과
    st, why = _wave1_status("ptfe_dimer", "dE", gate, "pm1")
    assert st == "CITABLE", f"원장에 등록된 조합을 막는다 (과교정): {why}"
    assert why == "허용 문구", "사유가 dE_notes(조각 키)에서 안 온다"

    # ⛔음성: **다른 시드**는 통과하면 안 된다. 조각 단위로 접어 버리면 여기서 샌다.
    st2, _ = _wave1_status("ptfe_dimer", "dE", gate, "net4")
    assert st2 != "CITABLE", "미등록 시드가 통과한다 — 게이트가 조각 단위로 느슨해졌다"

    # ⛔음성: allow-list 가 통째로 비면 통과 금지
    assert _wave1_status("ptfe_dimer", "dE", dict(gate, citable_dE=set()), "pm1")[0] != "CITABLE"

    # ⛔음성: hazard 가 걸리면 allow-list 에 있어도 BLOCKED (검사가 앞에 온다)
    st3, why3 = _wave1_status("ptfe_dimer", "dE",
                              dict(gate, hazards_by_fragment={"ptfe_dimer": "BLOCKED — x"}), "pm1")
    assert st3 == "BLOCKED", f"hazard 가 걸렸는데 {st3} 다 — 원장이 화면을 못 막는다"
    assert "인용 위험" in why3

    # ⛔음성: 원장을 못 읽으면 전부 BLOCKED (fail-closed)
    assert _wave1_status("ptfe_dimer", "dE", dict(gate, source_missing=True), "pm1")[0] == "BLOCKED"

    # 기존 특례는 강등이 아니라 그대로 (seed 를 줘도 순서가 안 바뀐다)
    assert _wave1_status("sdcp_doped", "dE", gate, "pm1")[0] == "BLOCKED"
    assert _wave1_status("ptfe_dimer", "eads", gate, "pm1")[0] == "HOLD"
    assert _wave1_status("sdcp_neutral", "dE", gate, "pm1")[0] == "NO_VERDICT"


def test_wave1_rows_have_citable_and_reason_matches_ledger():
    """양성 — 게이트가 **영구히 잠겨 있지 않다**.

    기존 시험은 음성만 있었다(`n_citable_dE == 0` 을 확인하는 것뿐). 그래서 게이트가
    한 건도 통과시키지 못하는 상태가 전 시험을 통과했다.
    """
    r = D.sdcp_wave1_rows()
    assert not r.get("unreadable"), r.get("unreadable")
    cit = [x for x in r["dE"] if x["status"] == "CITABLE"]
    assert cit, "인용 가능 행이 0 이다 — 원장에 등록된 값을 화면이 못 센다"
    assert r["n_citable_dE"] == len(cit)

    gate = r["gate"]
    for row in cit:
        # 인용 가능한 행은 반드시 (a) 원장 등록 (b) basin 일치 둘 다여야 한다
        assert f'{row["fragment"]}_{row["seed"]}' in gate["citable_dE"], row
        assert row["basin_same"], f"basin 이 갈린 행이 CITABLE 이다: {row}"
        assert row["why"] == gate["dE_notes"].get(row["fragment"]), row

    # ⛔음성: 마감·보류 축은 여전히 못 나온다
    assert not any(x["fragment"] == "sdcp_doped" and x["status"] == "CITABLE" for x in r["dE"]), \
        "doped 는 캠페인 마감이다 — 어느 표에서도 CITABLE 이 될 수 없다"
    assert all(j.get("status") != "CITABLE" for j in r["jobs"]), \
        "절대 E_ads(잡 행)가 CITABLE 이다 — 회신 O 보류가 풀렸다"


def test_wave1_no_unknown_left_when_ledger_is_readable():
    """UNKNOWN 은 '원장에 없다' 는 뜻이다 — 원장이 멀쩡한데 UNKNOWN 이 남으면 신호다.

    ⚠ 이 시험이 못 하는 것: UNKNOWN 이 옳은 경우(정말 미등록 조각이 새로 들어온 경우)와
      키 모양이 또 갈린 경우를 구분하지 못한다. 그래서 실패하면 **원장부터** 본다.
    """
    r = D.sdcp_wave1_rows()
    unknown = [x for x in r["dE"] if x["status"] == "UNKNOWN"]
    assert not unknown, (
        "원장을 읽었는데 UNKNOWN 행이 남았다 — 키 모양이 또 갈렸거나 원장에 조각이 빠졌다: "
        f"{[(x['fragment'], x['seed']) for x in unknown]}")


def test_sdcp_page_table_and_body_agree(client):
    """화면이 자기 본문과 싸우지 않는가 — 표 CITABLE 0 인데 본문은 값을 결론으로 썼다."""
    h = client.get("/sdcp").get_data(as_text=True)
    assert client.get("/sdcp").status_code == 200
    r = D.sdcp_wave1_rows()
    assert f'CITABLE {r["n_citable_dE"]}' in h, "헤더 배지가 게이트가 센 수와 다르다"
    # ⛔음성: **원장에 등록된** 키를 화면이 '등록돼 있지 않다' 고 말하면 안 된다.
    #   (등록 안 된 조합 — 예: ptfe_c10_net4 — 에 그렇게 쓰는 것은 옳다. 그건 남긴다.)
    for key in r["gate"]["citable_dE"]:
        assert f"`{key}` 가 인용 원장" not in h, \
            f"원장에 있는 {key} 를 화면이 '등록돼 있지 않다' 고 말한다 (키 모양 불일치 재발)"


def test_sdcp_closure_card_quotes_ledger_verbatim(client):
    """마감 문서의 허용/금지/재개 세 절이 **그대로** 화면에 있는가."""
    clo = json.loads((ROOT / "db" / "properties" / D.SDCP_CLOSED_JSON)
                     .read_text(encoding="utf-8"))
    card = D.sdcp_closure_card()
    assert card["ok"]
    assert card["forbidden"] == clo["⛔_금지_서술"], "금지 서술을 다듬었다"
    assert card["state"] == clo["status_history"][-1]["state"]
    assert card["reopen_only"] == clo["재개_조건_이것들만"]["⛔"]

    h = client.get("/sdcp").get_data(as_text=True)
    assert card["state"] in h and "재개 조건" in h
    from markupsafe import escape
    for s in clo["⛔_금지_서술"]:
        # `**`→<b> 와 escape 를 지나므로, 첫 `*`/`—` 전까지의 평문 토막으로 확인한다
        core = str(escape(re.split(r"[*—]", s)[0].strip()))
        assert len(core) >= 4 and core in h, f"금지 서술이 화면에서 빠졌다: {s}"


def test_sdcp_closure_card_omits_held_absolute_eads(client):
    """⛔음성 — 보류(HOLD)된 절대 E_ads 를 마감 카드가 헤드라인으로 되살리면 안 된다.

    같은 값을 `/sdcp` 는 접힘 안에서 다루는데 마감 카드가 큰 글씨로 띄우면 한 화면이
    같은 값에 두 지위를 준다. hazard 원장(HZ-sdcp-wave1-absolute-eads)이 BLOCKED 다.
    """
    card = D.sdcp_closure_card()
    assert "확정값" not in json.dumps(card, ensure_ascii=False), "확정값 절이 카드에 들어왔다"
    blob = json.dumps(card, ensure_ascii=False)
    for v in ("-0.7675", "-0.7582", "-0.7728", "-0.4124"):
        assert v not in blob, f"보류된 절대 E_ads {v} 가 마감 카드에 실렸다"


def test_sdcp_closure_card_fails_closed(monkeypatch, tmp_path):
    (tmp_path / "properties").mkdir()
    monkeypatch.setattr(D, "DB", tmp_path)
    c = D.sdcp_closure_card()
    assert c["ok"] is False and "못 읽었다" in c["why"]


# ══════════════════════════════════════════════════════════════════════════
# P0-13 — 캠페인 지위 밴드 (값은 원장 파생, 하드코딩 금지)
# ══════════════════════════════════════════════════════════════════════════
def test_campaign_band_reads_ratified_cards_not_literals():
    b = D.cascade_campaign_band()
    assert b["ok"], b.get("why")
    est = json.loads(EST_JSON.read_text(encoding="utf-8"))
    seal = json.loads(SEAL_JSON.read_text(encoding="utf-8"))
    assert b["estimand"] == est["1_보고량_정의_해제조건6"]["보고량"]
    assert b["remaining"] == est["6_아직_안_닫은_것"]["해제조건_잔여"]
    assert b["forbidden"] == est["5_금지_서술"]
    assert b["ratified_at"] == est["ratification"]["at"]
    assert b["seal"]["label"] == seal["label"]
    assert b["seal"]["n_sources"] == len(seal["sources"])
    # 'NO-GO' 는 우리가 붙이는 낱말이 아니라 카드 본문에서 온 것이어야 한다
    assert "NO-GO" in b["nogo_text"] and b["nogo_text"] in json.dumps(est, ensure_ascii=False)


def test_campaign_band_fails_closed(monkeypatch, tmp_path):
    """⛔음성 — 카드가 없거나 비준 전이면 **아무 값도 만들지 않는다**."""
    (tmp_path / "properties").mkdir()
    monkeypatch.setattr(D, "DB", tmp_path)
    b = D.cascade_campaign_band()
    assert b["ok"] is False and "못 읽었다" in b["why"], b

    # 비준 전(proposed) 카드도 통과하면 안 된다
    src = json.loads(EST_JSON.read_text(encoding="utf-8"))
    src["status"] = "proposed"
    (tmp_path / "properties" / D.CASCADE_ESTIMAND_JSON).write_text(
        json.dumps(src, ensure_ascii=False), encoding="utf-8")
    b2 = D.cascade_campaign_band()
    assert b2["ok"] is False and "비준 전" in b2["why"], b2


def test_cascade_page_shows_campaign_status(client):
    h = client.get("/cascade").get_data(as_text=True)
    b = D.cascade_campaign_band()
    for token in ("NO-GO", "D_rel", "해제조건", b["seal"]["label"]):
        assert token in h, f"캠페인 지위 밴드에 {token!r} 이 없다 — 화면이 자기 지위를 모른다"
    assert f'/governance#{b["decision"]}' in h, "판정 원장으로 가는 문이 없다"


def test_campaign_band_template_has_no_hardcoded_values():
    """⛔음성 — 템플릿에 숫자를 박으면 원장이 바뀌어도 화면이 조용히 낡는다."""
    src = BAND_HTML.read_text(encoding="utf-8")
    for lit in ("600 K", "2–50 ps", "v2_2026_09_08", "#3", "#4", "#7", "#8"):
        assert lit not in src, f"밴드 템플릿에 {lit!r} 가 박혀 있다 — 원장에서 읽어야 한다"


# ══════════════════════════════════════════════════════════════════════════
# P0-10 — 해소된 충돌 · dict repr 누출
# ══════════════════════════════════════════════════════════════════════════
def test_resolved_conflict_is_folded_not_shown_as_open(client):
    h = client.get("/cascade").get_data(as_text=True)
    ver = D.load_cascade().get("verified") or {}
    done = [k for k in ver if k.startswith("_CONFLICT") and not k.startswith("_CONFLICT_UNRESOLVED")]
    assert done, "픽스처 전제가 사라졌다 — 해소된 충돌 키가 원장에 없다"
    assert f"해소된 값 충돌 {len(done)}건" in h, "해소분이 접힌 절로 안 내려갔다"
    # ⛔음성: 파이썬 dict repr 이 화면에 새면 안 된다
    for leak in ("&#39;resolution&#39;", "&#39;consequence&#39;", "{&#39;"):
        assert leak not in h, f"파이썬 dict repr 이 화면에 노출된다: {leak}"
    # ⛔음성: 근거 없는 '전부 잠정' 꼬리말은 삭제됐다
    assert "verdict 는 전부 <b>잠정</b>" not in h


def test_unresolved_conflict_still_shown_if_present(client):
    """양성 — 해소분만 접는 것이지 **미해소를 숨기는 게 아니다**."""
    ver = D.load_cascade().get("verified") or {}
    if not any(k.startswith("_CONFLICT_UNRESOLVED") for k in ver):
        pytest.skip("원장에 미해소 충돌이 없다")
    h = client.get("/cascade").get_data(as_text=True)
    assert "미해소 값 충돌" in h, "미해소 충돌을 안 띄운다 — 사이트가 스스로 모순된다"


# ══════════════════════════════════════════════════════════════════════════
# P0-11 — 딥링크 TypeError 가 테마 탭을 죽였다
# ══════════════════════════════════════════════════════════════════════════
def test_deeplink_handler_is_guarded():
    src = CASCADE_HTML.read_text(encoding="utf-8")
    m = re.search(r"// 딥링크.*?\n(.{0,700})", src, re.S)
    assert m, "딥링크 블록을 못 찾았다"
    blk = m.group(1)
    assert "r.cells.length>1" in blk, "cells 길이 가드가 없다 — undefined 로 죽는다"
    assert "try{" in blk and "catch" in blk, "try/catch 격리가 없다"


def test_gate_notice_is_outside_tbody(client):
    """게이트 안내 행이 데이터 행과 섞이면 딥링크 JS 가 그 행에서 죽는다."""
    h = client.get("/cascade").get_data(as_text=True)
    body = _tbody(h, "board-tbl")
    assert "colspan" not in body, "게이트 안내가 아직 tbody 안에 있다"
    assert "보관함 열기" in h, "안내를 tbody 밖으로 빼면서 통째로 잃었다"


def test_theme_wiring_survives_default_view(client):
    """THEMES/TDOP 할당이 딥링크 블록 **뒤**에 있고 실제로 렌더된다."""
    h = client.get("/cascade").get_data(as_text=True)
    assert re.search(r"var THEMES=", h) and re.search(r"var TDOP=", h)
    # 빈 TDOP 가 '없다' 인지 '가려졌다' 인지 JS 가 구분할 수 있어야 한다
    assert "var THEME_GATED=true" in h, "게이트 플래그가 JS 에 안 내려간다"


# ══════════════════════════════════════════════════════════════════════════
# P0-12 — archive 게이트 확장 (완화가 아니라 확장)
# ══════════════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("key", ["ranked", "champions", "litransport", "synergy"])
def test_archive_only_artifacts_absent_from_default_dom(client, key):
    """⛔음성 — 기본 응답에 v1 산출물의 **행**이 실리면 안 된다.

    같은 파일을 `/api/file` 로 받으면 403(원장 미등재)이다. 다운로드는 막고 화면은
    내보내는 상태로 되돌아가면 여기서 걸린다.
    """
    assert key in A.CASCADE_ARCHIVE_ONLY
    ctx = A.app.test_request_context("/cascade")
    with ctx:
        pass
    r = client.get("/cascade")
    ra = client.get("/cascade?archive=1")
    full = (D.load_cascade().get(key) or {}).get("data") or []
    assert full, f"{key} 원자료가 비었다 — 시험 전제가 사라졌다"
    # 대표 행의 첫 열 값이 기본 화면 표에 없어야 한다
    h, ha = r.get_data(as_text=True), ra.get_data(as_text=True)
    assert len(h) < len(ha), "게이트를 걸었는데 기본 응답이 보관함보다 작지 않다"
    if key == "champions":
        assert _tbody(h, "champ-tbl").count("<tr") == 0
        assert _tbody(ha, "champ-tbl").count("<tr") == len(full)
    if key == "ranked":
        assert _tbody(h, "board-tbl").count("<tr") == 0
        assert _tbody(ha, "board-tbl").count("<tr") == len(full)


def test_gated_slots_say_hidden_not_zero(client):
    """⛔ 없는 것을 0 으로 표시하지 않는다 (CLAUDE.md)."""
    h = client.get("/cascade").get_data(as_text=True)
    assert "가려짐" in h
    assert "아래 0종 리더보드" not in h, "게이트 뒤의 0 을 사실처럼 찍는다"
    assert "전 0개 도펀트" not in h
    ha = client.get("/cascade?archive=1").get_data(as_text=True)
    assert "아래 47종 리더보드" in ha, "보관함에서는 실제 수를 찍어야 한다"


def test_fail_closed_gates_still_hold(client):
    """게이팅 3종은 Codex 가 두 번 잡아 만든 장치다 — 확장하다 풀지 않았는지 본다."""
    assert client.get("/cascade/diagnostic").status_code == 403
    assert client.get("/cascade/diagnostic?view=diagnostic").status_code == 200
    # manifest 미등재 = 미승인 403
    r = client.get("/api/file/db/properties/cascade_v23_champions.csv")
    assert r.status_code == 403, f"미등재 artifact 가 {r.status_code} 로 나간다"
    assert "원장" in r.get_json()["error"], "403 이 왜인지 말하지 않는다"


@pytest.mark.parametrize("url", ["/cascade", "/cascade?archive=1", "/cascade?view=diagnostic"])
def test_no_literal_markdown_asterisks(client, url):
    """`|bold` 필터를 빠뜨린 자리는 화면에 `**` 를 기호로 노출한다 (실측 48회였다).

    ⛔음성 성격 — 필터를 지우거나 새 자리에 db 문자열을 그냥 찍으면 여기서 걸린다.
    ⚠ 못 하는 것: 스크립트·스타일·주석 안은 안 본다 (JS 리터럴에 `**` 가 정당하게 있다).
    """
    h = client.get(url).get_data(as_text=True)
    body = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    hits = [m.group(0).replace("\n", " ") for m in re.finditer(r".{40}\*\*.{40}", body, re.S)]
    assert not hits, f"|bold 를 빠뜨린 자리 {len(hits)}곳: {hits[:3]}"


def test_protected_markers_survive(client):
    """FORBIDDEN 주석쌍 · data-claim-not 부인은 **이동은 되고 삭제는 안 된다**."""
    h = client.get("/cascade").get_data(as_text=True)
    assert h.count("<!--FORBIDDEN-->") == h.count("<!--/FORBIDDEN-->") >= 2
    assert 'data-claim-not="MD_Ea_eV@b2o3"' in h, "codoping 표의 부인 래퍼가 사라졌다"
    for tab in ("tab-board", "tab-champ", "tab-syn", "tab-stab"):
        assert f'id="{tab}"' in h, f"superseded/diagnostic 탭 {tab} 이 사라졌다 (삭제 금지)"


# ── /cascade 판정 밴드 (2026-09-19) ────────────────────────────────────────
#   ⛔ 왜 생겼나: 화면을 **실제로 렌더해 보니** ratified 판정 둘이 한 글자도 없었다.
#     그런데 화면은 3,615 · 681 · 91종을 큰 숫자로 띄우고 있었다. CLAUDE.md §화면 규율 —
#     "규율이 원장에만 있고 화면에 안 실리면 사람은 화면을 인용한다."
def test_cascade_verdicts_come_from_ledger_and_reach_the_page():
    """양성: 원장 판정이 `/cascade` 본문에 **실제로 실린다**."""
    vs = D.cascade_verdicts()
    assert vs, "판정 목록이 비었다"
    ok = [v for v in vs if v.get("ok")]
    assert len(ok) >= 2, f"원장에서 읽힌 판정이 {len(ok)}건 — 2건 이상이어야 한다"
    for v in ok:
        assert v.get("text"), f"{v['label']}: 원장 문장이 비었다"
        assert v.get("record", "").startswith("db/properties/"), \
            f"{v['label']}: 출처가 db/properties 가 아니다 ({v.get('record')})"
    html = A.app.test_client().get("/cascade").get_data(as_text=True)
    for v in ok:
        # 원장 문장의 꼬리 토막이 화면에 있어야 한다 (전체 문자열은 이스케이프로 갈릴 수 있다)
        tail = v["text"].split("—")[-1].strip()[:14]
        assert tail and tail in html, f"{v['label']}: 원장 문장이 화면에 없다 ({tail!r})"


def test_cascade_verdict_gap_is_shown_not_swallowed():
    """⛔음성: 원장에 **없는** 판정은 지어내지도, 조용히 빼지도 않는다 — 구멍으로 싣는다."""
    vs = D.cascade_verdicts()
    gaps = [v for v in vs if not v.get("ok")]
    assert gaps, "구멍이 하나도 없다 — CASCADE_VERDICT_GAPS 가 배선에서 빠졌다"
    for g in gaps:
        assert g.get("why"), f"{g.get('label')}: 왜 못 싣는지를 안 적었다"
        assert not g.get("text"), f"{g.get('label')}: 원장에 없는데 문장을 지어냈다"
    html = A.app.test_client().get("/cascade").get_data(as_text=True)
    assert "원장 기록이 없다" in html, "구멍이 화면에 안 나간다 — 조용히 삼켰다"


def test_cascade_verdicts_fail_closed_on_missing_record():
    """⛔음성: 원장 파일이 없으면 **ok=False 로 구멍**이지, 조용한 생략이 아니다."""
    keep = D.CASCADE_VERDICT_SOURCES
    try:
        D.CASCADE_VERDICT_SOURCES = [("없는 것", "no_such_cascade_record_xyz.json")]
        vs = D.cascade_verdicts()
        bad = [v for v in vs if v.get("label") == "없는 것"]
        assert bad, "없는 기록이 목록에서 **사라졌다** (조용한 생략)"
        assert bad[0]["ok"] is False and "못 읽었다" in bad[0]["why"]
    finally:
        D.CASCADE_VERDICT_SOURCES = keep
