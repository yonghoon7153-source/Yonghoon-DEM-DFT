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
    assert "0.039" not in h, "옛 값이 화면에 남아 있다 (두 곳에서 온다)"


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
    assert "0.039" not in h, "기록이 없는데 옛 숫자가 남아 있다"


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
