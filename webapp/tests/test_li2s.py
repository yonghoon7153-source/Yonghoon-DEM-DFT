#!/usr/bin/env python3
"""test_li2s.py — Li₂S 계면상 파이프라인 화면(/li2s)의 회귀 + **음성시험**.

    pytest webapp/tests/test_li2s.py -q

이 화면의 핵심 계약 셋:
  ① 숫자는 **기록에서만** 온다 (화면이 자체 보관하지 않는다 — CLAUDE.md §화면 규율)
  ② 기록을 못 읽으면 **조용히 사라지지 않는다** — 경고를 그린다 (0 으로도 안 그린다)
  ③ 소셀이 통과해도 **400 원자 표지를 떼지 않는다** (G-B2 탈락 · 소셀 카드 §6)

⛔ 이 파일이 못 하는 것: 과학적 판정이 옳은지 보지 않는다. 화면이 원장을 **읽어서**
  그리는지, 못 읽었을 때 그것을 말하는지만 본다.
"""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import data as D               # noqa: E402
import nav as N                # noqa: E402
from app import app            # noqa: E402

GB3 = "lpscl_smallcell_gb3_result_2026_09_18.json"


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    return app.test_client()


def _html(client):
    r = client.get("/li2s")
    assert r.status_code == 200, f"/li2s 가 {r.status_code}"
    return r.get_data(as_text=True)


# ── ① 숫자가 기록에서 온다 ─────────────────────────────────────────────
def test_renders_numbers_from_records(client):
    h = _html(client)
    for token in ("0.039",        # G-B3 힘 RMSE
                  "0.55",         # 상대 E MAE
                  "48.2",         # 0층 대조 잡 E_above_hull
                  "-17.86",       # 1층 밀도 이탈
                  "15.18"):       # 탐침 메모리 추정
        assert token in h, f"기록의 값 {token} 이 화면에 없다"


def test_element_table_shows_split_softening(client):
    """원소별 softening 의 **부호가 갈리는 것**이 화면에 보인다 (전체값은 이걸 가린다)."""
    h = _html(client)
    assert "0.9785" in h and "0.9766" in h, "무른 쪽(S·P) 이 없다"
    assert "1.0104" in h and "1.0149" in h, "단단한 쪽(Cl·Li) 이 없다"


def test_element_table_says_it_is_not_a_gate(client):
    """원소별 표가 **게이트로 읽히지 않게** 하는 문장이 화면에 있어야 한다.

    ⚠ 단정 문자열은 기록의 **실제 문구**에서 온다 — 처음에 "문턱이 아니다" 로 적었다가
      빨간불이 떴다. 기록은 같은 뜻을 *"원소 하나가 나빠도 떨어뜨리지 않는다"* 로 쓴다.
      **시험이 틀렸던 것**이지 화면이 틀린 게 아니었다.
    """
    h = _html(client)
    assert "원소 하나가 나빠도" in h, "원소별이 게이트처럼 읽힐 수 있다"
    assert "PS₄ 강성" in h, "허용 서술에 주는 단서(§2 → claim ceiling)가 화면에 없다"


# ⛔음성 — 화면이 숫자를 **자체 보관하면** 이 시험이 잡는다.
def test_numbers_follow_the_record_not_the_template(client):
    """기록의 값을 바꾸면 화면이 **따라 바뀌어야** 한다. 안 바뀌면 화면이 값을 품은 것이다."""
    real = D._load_json

    def fake(p):
        d = real(p)
        if d and Path(p).name == GB3:
            d = dict(d)
            blk = dict(d["★_G_B3_힘·에너지"])
            blk["F_RMSE_eVA"] = 0.4242            # 있을 수 없는 값
            d["★_G_B3_힘·에너지"] = blk
        return d

    with patch.object(D, "_load_json", side_effect=fake):
        h = _html(client)
    assert "0.4242" in h, "기록을 바꿨는데 화면이 안 바뀐다 — 화면이 숫자를 자체 보관한다"
    # ⚠ "옛 값이 아예 없어야 한다" 로는 못 쓴다 — **마감 카드가 정당한 두 번째 출처**다
    #   (마감 규율이 확정값을 카드에 적으라고 한다). 둘이 갈라지지 않는지는
    #   `test_closure_value_matches_its_source` 가 따로 본다.


# ── ② 못 읽은 것을 조용히 지우지 않는다 ────────────────────────────────
def test_missing_record_is_announced_not_hidden(client):
    """기록 파일이 없으면 단계를 빼지 않고 **없다고 말한다**."""
    real = D._load_json

    def fake(p):
        return None if Path(p).name == GB3 else real(p)

    with patch.object(D, "_load_json", side_effect=fake):
        r = client.get("/li2s")
        assert r.status_code == 200, "기록 하나가 없다고 화면이 죽으면 안 된다"
        h = r.get_data(as_text=True)
    assert GB3 in h, "없는 기록의 파일명을 화면이 대지 않는다"
    assert "못 읽" in h, "못 읽었다는 말이 화면에 없다 — 빈 화면과 구분이 안 된다"


def test_missing_stage_stays_in_the_list(client):
    """⛔음성: 기록이 없어도 **단계 자체는 목록에 남는다.**

    ⚠ 이 시험은 위 시험이 **엉뚱한 것을 재서** 추가됐다 (2026-09-18). 위 시험은 상단
      배너(`p.missing` 목록)만 보고 있어서, 단계를 목록에서 통째로 빼도 초록이었다.
      단계가 사라지면 "안 한 것" 과 "기록이 없는 것" 이 화면에서 같아진다.
    """
    n_declared = len(D.LI2S_STAGES)
    real = D._load_json

    def fake(p):
        return None if Path(p).name == GB3 else real(p)

    with patch.object(D, "_load_json", side_effect=fake):
        pipe = D.li2s_pipeline()
    assert len(pipe["stages"]) == n_declared, (
        f"기록이 없다고 단계가 사라졌다 ({len(pipe['stages'])} ≠ {n_declared}) — "
        "'안 한 것' 과 '기록이 없는 것' 이 화면에서 같아진다")
    gb3 = [s for s in pipe["stages"] if s["record"] == GB3]
    assert gb3 and gb3[0]["missing"] is True, "그 단계가 missing 으로 표시되지 않았다"
    assert gb3[0]["verdict"] is None, "기록이 없는데 판정이 붙어 있다"


# ⛔음성 — 경로가 틀리면 **행이 사라지는 게 아니라** 경고가 떠야 한다.
def test_bad_field_path_shows_warning_not_silence():
    """`_dig` 가 못 판 값은 행을 지우지 않고 `unread` 로 남는다."""
    facts = D._li2s_facts("gb3", {"아무것도": "없다"})
    assert facts, "경로를 하나도 못 읽으면 행이 통째로 사라진다 — 조용히 틀린 경로다"
    assert all(f["unread"] for f in facts), "못 읽었는데 unread 표시가 없다"


def test_dig_handles_keys_containing_dots():
    """⛔음성: 키 안에 점이 있으면 문자열 경로로는 못 판다 — 리스트 경로가 답이다."""
    d = {"a": {"x=0.25": 7}}
    assert D._dig(d, "a.x=0.25") is None, "점 든 키를 문자열 경로가 우연히 읽으면 시험이 무의미하다"
    assert D._dig(d, ["a", "x=0.25"]) == 7, "리스트 경로가 점 든 키를 못 읽는다"


# ── ③ 소셀 통과가 400 원자 표지를 떼지 않는다 ──────────────────────────
def test_does_not_lift_the_400atom_label(client):
    h = _html(client)
    assert "UMA 미검증" in h, "400 원자가 아직 미검증이라는 말이 화면에 없다"
    assert "탈락" in h, "G-B2 탈락이 화면에 없다 — 통과만 보이면 전이가 열린 줄 안다"


def test_permanent_rider_is_on_screen(client):
    """비준된 영구 단서가 **텍스트로** 나간다 (CSS 로 그리면 복사·추출에 안 따라간다)."""
    h = _html(client)
    assert "감김 홉" in h and "2.33" in h, "자기이미지 단서가 화면에 없다"


# ── nav ────────────────────────────────────────────────────────────────
def test_nav_has_li2s_and_it_is_live(client):
    urls = {i["url"] for i in N._items()}
    assert "/li2s" in urls, "nav 에 /li2s 가 없다 — 색인 밖 화면은 없는 화면이다"
    assert client.get("/li2s").status_code == 200


# ── 마감 카드 ──────────────────────────────────────────────────────────
CLOSED = "lpscl_smallcell_closed_2026_09_18.json"


def test_closure_card_shows_allowed_forbidden_reopen(client):
    """마감의 **세 목록이 화면에 실물로** 나온다 (파일명만 대면 아무도 안 읽는다)."""
    h = _html(client)
    assert "허용 서술" in h and "금지 서술" in h and "재개 조건" in h
    assert "400 원자에 대한 어떤 것도" in h, "제일 센 금지 서술이 화면에 없다"
    assert "감김 홉 2.33" in h, "허용 서술의 영구 단서가 화면에 없다"


def test_closure_card_admits_reopen_was_written_after(client):
    """⛔음성: **재개 조건이 사후 작성**이라는 고백이 화면에 남아야 한다.

    마감 규율은 '조건을 먼저 정하고 그게 채워졌으므로 닫는다' 다. 게이트는 사전등록이었지만
    재개 조건은 아니었다 — 그 구분이 화면에서 사라지면 다음 사람이 전부 사전등록으로 읽는다.
    """
    h = _html(client)
    assert "사후에 쓰는 것" in h, "재개 조건이 사후 작성이라는 고백이 화면에서 사라졌다"
    assert "사전등록이었던 것" in h, "무엇이 사전등록이었는지가 화면에 없다"
    assert "지금 새로 쓰는 것" in h, "무엇이 사후 작성인지 라벨이 화면에 없다"


def test_closure_values_come_from_the_card(client):
    """⛔음성: 확정값도 카드에서 온다 — 바꾸면 화면이 따라간다."""
    real = D._load_json

    def fake(p):
        d = real(p)
        if d and Path(p).name == CLOSED:
            d = dict(d)
            fx = dict(d["1_확정값"]); fx["힘_RMSE_eVA"] = 0.777
            d["1_확정값"] = fx
        return d

    with patch.object(D, "_load_json", side_effect=fake):
        h = _html(client)
    assert "0.777" in h, "마감 카드를 바꿨는데 화면이 안 바뀐다"


def test_closure_card_missing_is_announced(client):
    """⛔음성: 마감 카드가 없으면 **빈 카드로 흉내내지 않는다**."""
    real = D._load_json

    def fake(p):
        return None if Path(p).name == CLOSED else real(p)

    with patch.object(D, "_load_json", side_effect=fake):
        r = client.get("/li2s")
        assert r.status_code == 200
        h = r.get_data(as_text=True)
    assert "마감 카드를 못 읽었다" in h, "카드가 없는데 화면이 조용하다"
    assert "허용 서술 — 이대로만" not in h, "카드가 없는데 허용 서술 칸이 그려졌다"


def test_closure_value_matches_its_source():
    """⛔음성: 마감 카드의 확정값이 **원본 게이트 기록과 갈라지면** 잡는다.

    마감 카드는 값을 **옮겨 적는다**(마감 규율이 확정값을 요구한다). 그래서 같은 숫자가
    원장에 두 벌 생긴다 — 원본이 고쳐지면 조용히 갈라질 수 있는 자리다. 여기서 묶는다.
    """
    closed = D._load_json(D.DB / "properties" / CLOSED)
    gate = D._load_json(D.DB / "properties" / GB3)
    assert closed and gate, "기록을 못 읽었다"
    a = closed["1_확정값"]["힘_RMSE_eVA"]
    b = gate["★_G_B3_힘·에너지"]["F_RMSE_eVA"]
    assert a == b, f"마감 카드 {a} ≠ 게이트 기록 {b} — 두 벌이 갈라졌다"
    a2 = closed["1_확정값"]["상대_에너지_MAE_meV_atom"]
    b2 = gate["★_G_B3_힘·에너지"]["상대_E_MAE_meV_atom"]
    assert a2 == b2, f"마감 카드 {a2} ≠ 게이트 기록 {b2} — 두 벌이 갈라졌다"


# ─────────────────────────────────────────────────────────────────────────────
# G1 — "불통과" 와 "미실시" 를 화면이 가르는가 (2026-09-18 추가)
#
# 왜: 이 단계에 사실 행이 **하나도 없었다**. 화면에는 제목과 status 만 떴고,
#     사다리 5칸·실패 지점·'불통과가 아니다' 는 전부 원장에만 있었다.
#     그러면 사람은 화면을 보고 "G1 은 실패했다(=UMA 가 틀렸다)" 로 읽는다.
#     실제로는 **한 점도 안 돌았다**. 이 구분이 이 캠페인의 유일한 결론이다.
# ─────────────────────────────────────────────────────────────────────────────
G1 = "li2s_layer1_g1_prereg_2026_09_14.json"
CLOSED_L1 = "lpscl_li2s_layer1_closed_2026_09_15.json"


def _stage(key):
    return next(s for s in D.li2s_pipeline()["stages"] if s["key"] == key)


def test_g1_stage_has_facts_at_all():
    """G1 단계에 사실 행이 있다 — 비어 있으면 화면이 제목만 보여준다."""
    f = _stage("g1")["facts"]
    assert f, "G1 단계에 사실 행이 하나도 없다 — 원장에만 있는 상태로 되돌아갔다"


def test_g1_says_not_a_failure_but_not_run():
    """⛔음성: '불통과가 아니다' 가 화면에서 사라지면 잡는다."""
    labels = {r["label"]: r["value"] for r in _stage("g1")["facts"]}
    k = [x for x in labels if "불통과" in x]
    assert k, f"'불통과가 아니다' 행이 없다: {list(labels)}"
    v = labels[k[0]] or ""
    assert "존재하지 않는" in v, f"힘 RMSE 부재를 말하지 않는다: {v[:120]}"


def test_g1_ladder_shows_all_five_rungs():
    """사다리가 **5칸**으로 보인다 — ⑤ gabia 48 GB 가 빠지면 '해볼 게 남았나' 를 다시 묻는다."""
    rows = {r["label"]: r["value"] for r in _stage("g1")["facts"]}
    k = [x for x in rows if "사다리" in x]
    assert k, "사다리 행이 없다"
    rungs = rows[k[0]]
    assert isinstance(rungs, list) and len(rungs) == 5, f"사다리가 5칸이 아니다: {rungs}"
    assert any("gabia" in str(x) for x in rungs), f"⑤ gabia 칸이 없다: {rungs}"


def test_g1_separates_closed_campaign_from_open_question():
    """★ 종결 ≠ 미결. 이 구분이 화면에 **글자로** 있어야 한다 (표지가 아니라 본문)."""
    rows = {r["label"]: r["value"] for r in _stage("g1")["facts"]}
    k = [x for x in rows if "종결" in x and "미결" in x]
    assert k, f"'종결 ≠ 미결' 행이 없다: {list(rows)}"
    v = rows[k[0]] or ""
    assert "미검증" in v, f"표지 문구(미검증)를 안 말한다: {v[:150]}"


def test_closed_stage_shows_the_gabia_retry_measurement():
    """재개조건 ①을 소진시킨 09-17 실측이 화면에 있다.

    ⛔음성: 없으면 다음 사람이 "gabia 48 GB 해보면 되지 않나" 를 다시 묻는다 —
    이미 해봤고 OOM 이다.
    """
    rows = {r["label"].strip(): r["value"] for r in _stage("closed")["facts"]}
    assert any("gabia" in x for x in rows), f"gabia 재시도 행이 없다: {list(rows)}"
    assert "GPU" in rows and rows["GPU"], "GPU 점유 실측이 없다"
    assert "33.9" in str(rows["GPU"]), f"GPU 실측이 원장과 다르다: {rows['GPU']}"


def test_closed_stage_says_host_was_not_the_wall():
    """⛔음성: host 가 막았다는 옛 예상이 정정된 채로 보이는가.

    원장은 host rss 29.6 GB(여유)였고 **GPU 가 막았다**고 적었다. 화면이 이 정정을
    안 실으면, 다음 사람은 'host 메모리 큰 기계를 구하면 된다' 로 잘못 읽는다.
    """
    rows = {r["label"].strip(): (r["value"] or "") for r in _stage("closed")["facts"]}
    hk = [x for x in rows if "host" in x.lower()]
    assert hk, f"host rss 행이 없다: {list(rows)}"
    assert "29.6" in str(rows[hk[0]]), f"host rss 가 원장과 다르다: {rows[hk[0]]}"
    wrong = [v for k, v in rows.items() if "예상이 틀렸" in k]
    assert wrong and "GPU 가 막았다" in str(wrong[0]), f"정정 문구가 없다: {wrong}"


def test_g1_record_and_closure_card_do_not_diverge():
    """⛔음성: §6f 는 마감 카드의 **사본**이다. 갈라지면 잡는다.

    같은 사실이 두 파일에 있는 자리다 — 한쪽만 고치면 조용히 갈라진다.
    """
    g1 = D._load_json(D.DB / "properties" / G1)
    cl = D._load_json(D.DB / "properties" / CLOSED_L1)
    assert g1 and cl, "기록을 못 읽었다"
    src = cl["⭐_gabia_48GB_재시도_실측_2026_09_17"]
    cp = g1["6f_사다리_⑤_gabia_48GB_2026_09_17"]
    assert cp["실측_2026_09_17"]["죽은_자리"] == src["실측"]["죽은 자리"], "죽은 자리가 갈라졌다"
    assert cp["실측_2026_09_17"]["GPU"] == src["실측"]["실제 GPU"], "GPU 실측이 갈라졌다"
    assert cp["⇒_사다리는_이제_5칸_전부_실측이다"] == src["사다리_소진"], "사다리가 갈라졌다"


def test_g1_status_does_not_claim_the_question_is_settled():
    """⛔음성: status 가 '종결' 만 말하고 끝나면 안 된다 — 질문은 미결이다."""
    g1 = D._load_json(D.DB / "properties" / G1)
    st = g1["status"]
    assert "종결" in st, "종결 사실이 빠졌다"
    assert "미결" in st, f"질문이 미결이라는 말이 status 에 없다: {st}"


# ─────────────────────────────────────────────────────────────────────────────
# L-1~L-4 사다리 (2026-09-18 추가)
#
# 왜: 이 사다리는 **채팅에만** 살았다 — `L-1`·`앙상블 ≥5 시드`·`3.6일` 이
#     kb/·db/·webapp/ 어디에도 없었다. 그래서 1저자가 들고 있던 표가
#     L-2·L-3·L-4 셋이 바뀐 걸 모르고 "지금 여기 = L-2" 라고 말하고 있었다.
#     원장에 두고 화면이 읽게 한 뒤, **다시 낡는 것**을 시험으로 막는다.
# ─────────────────────────────────────────────────────────────────────────────
LADDER = "li2s_track_ladder_2026_09_18.json"


def test_ladder_has_all_four_rungs(client):
    ld = D.li2s_ladder()
    assert ld["ok"], ld.get("why")
    ids = [r["id"] for r in ld["rungs"]]
    assert ids == ["L-1", "L-2", "L-3", "L-4"], f"칸이 빠졌거나 순서가 바뀌었다: {ids}"


def test_ladder_is_on_screen(client):
    h = client.get("/li2s").get_data(as_text=True)
    for k in ("트랙 사다리", "L-1", "L-2", "L-3", "L-4"):
        assert k in h, f"화면에 {k} 가 없다 — 원장에만 있으면 같은 일이 반복된다"


def test_ladder_says_l2_is_not_where_we_are():
    """⛔음성: L-2 가 'deferred' 가 아니라 진행 중으로 되돌아가면 잡는다.

    옛 표는 L-2 를 '← 지금 여기' 로 적었는데, 소셀 마감이 G3 를 **선언으로**
    처리했다(단일 시드 조건부 + 영구 단서). 이 구분이 사라지면 다음 사람이
    '앙상블이 돌고 있다' 로 읽는다.
    """
    r = next(x for x in D.li2s_ladder()["rungs"] if x["id"] == "L-2")
    assert r["state"] == "deferred_by_declaration", f"L-2 상태가 바뀌었다: {r['state']}"
    assert "지금 여기" in (r["now"] or ""), "옛 표의 '지금 여기' 를 정정한 문구가 사라졌다"


def test_ladder_l3_does_not_claim_400atom_g1_is_answered():
    """⛔음성: L-3 이 '통과' 로 뭉뚱그려지면 잡는다.

    120 원자가 통과했지 **400 원자 G1 은 여전히 미결**이다 (G-B2 탈락).
    이 둘이 섞이면 소셀 결과로 400 원자를 서술하게 된다.
    """
    r = next(x for x in D.li2s_ladder()["rungs"] if x["id"] == "L-3")
    assert r["state"] == "split", f"L-3 이 갈래를 잃었다: {r['state']}"
    cav = (r["caveat"] or "")
    assert "미결" in cav and "G-B2" in cav, f"400 원자가 미결이라는 단서가 없다: {cav[:120]}"


def test_ladder_l4_carries_the_translation_ban():
    """⛔음성: L-4 에서 σ·D·Ea 금지가 빠지면 잡는다."""
    r = next(x for x in D.li2s_ladder()["rungs"] if x["id"] == "L-4")
    txt = (r["now"] or "") + (r["caveat"] or "")
    assert "별도" in txt and ("σ" in txt or "Ea" in txt), f"번역 금지 단서가 없다: {txt[:150]}"


def test_ladder_marks_neb_as_off_ladder():
    """NEB 가 사다리 안으로 들어오면 안 된다 — 다른 축이고 다른 카드다."""
    ld = D.li2s_ladder()
    assert ld["branch"], "사다리 밖 가지(NEB)가 없다"
    assert all(r["id"] != "L-5" for r in ld["rungs"]), "NEB 가 사다리 칸으로 들어왔다"
    assert "없다" in (ld["branch_note"] or ""), "NEB 가 사다리에 없다는 말이 빠졌다"


def test_ladder_missing_record_is_announced(client):
    """⛔음성: 기록을 못 읽으면 **빈 사다리를 그리지 않는다**."""
    with patch.object(D, "LI2S_LADDER_JSON", "nonexistent_ladder.json"):
        ld = D.li2s_ladder()
        assert not ld["ok"] and not ld["rungs"], "기록이 없는데 사다리를 그렸다"
        h = client.get("/li2s").get_data(as_text=True)
    assert "사다리 기록을 못 읽었다" in h, "기록이 없는데 화면이 조용하다"
    assert "트랙 사다리" in h, "경고는 띄우되 절 제목은 남아야 한다"


def test_ladder_l1_numbers_match_what_we_measured():
    """⛔음성: L-1 재확인 수치가 실측과 갈라지면 잡는다 (ρ 1.6212 · PS₄ 1.0000)."""
    d = D._load_json(D.DB / "properties" / LADDER)
    r = next(x for x in d["2_사다리_실제_상태"] if x["id"] == "L-1")
    assert "1.6212" in r["지금"] and "1.0000" in r["지금"], \
        f"L-1 의 실측 수치가 바뀌었다: {r['지금'][:160]}"
