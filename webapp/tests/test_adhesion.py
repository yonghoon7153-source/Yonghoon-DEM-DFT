#!/usr/bin/env python3
"""test_adhesion.py — 점착 파이프라인 화면(/adhesion)의 회귀 + **음성시험**.

    pytest webapp/tests/test_adhesion.py -q

이 화면의 계약:
  ① 내용은 **원장 하나에서만** 온다 (`db/pipelines/adhesion_pipeline.json`) — 원장을 바꾸면 화면이 바뀐다
  ② 원장이 없거나 기록 경로가 죽으면 **조용히 비지 않고 경고**를 그린다
  ③ 결정은 decisions.json 에서 scope `adhesion.` 으로 **실시간** — 화면이 자체 보관하지 않는다
  ④ 판정 전 물리값(W·γ)은 화면에 없다 (원장 규약) · COMSOL 은 이름만 (관할 밖)
  ⑤ 원장 글에 철회값이 섞여 들어오면 **결속**된다 (선언을 지우면 미결속으로 떨어진다)

⛔ 이 파일이 못 하는 것: 과학적 판정이 옳은지 보지 않는다. 원장·결정 원장을 **읽어서**
  그리는지와, 못 읽었을 때 그것을 말하는지만 본다.
"""
import copy
import json
import re
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import canonical as C          # noqa: E402
import data as D               # noqa: E402
import decisions_view as DV    # noqa: E402
import nav as N                # noqa: E402
from app import app            # noqa: E402

_REAL_LOAD = D._load_json
LEDGER = json.loads(D.ADHESION_LEDGER.read_text(encoding="utf-8"))


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    return app.test_client()


def _html(client):
    r = client.get("/adhesion")
    assert r.status_code == 200, f"/adhesion 가 {r.status_code}"
    return r.get_data(as_text=True)


def _txt(html: str) -> str:
    """렌더된 화면의 **글자만** (태그·스크립트 제거 · 엔티티 복원)."""
    import html as _h
    body = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S)
    return _h.unescape(re.sub(r"<[^>]+>", "", body))


def _plain(md: str) -> str:
    """원장의 마크다운 원문 → 화면에 보일 글자 (``·**·==·~~ 표식 제거)."""
    return re.sub(r"`|\*\*|==|~~", "", md)


def _with_ledger(led):
    """원장 파일 읽기만 바꿔치기 (다른 기록은 진짜를 읽는다)."""
    def fake(p):
        return copy.deepcopy(led) if Path(p) == D.ADHESION_LEDGER else _REAL_LOAD(p)
    return patch.object(D, "_load_json", side_effect=fake)


# ── ① 원장에서 온다 ────────────────────────────────────────────────────
def test_page_shows_ledger_sections(client):
    h = _html(client)
    for token in ("DFT → DEM 인계 규약", "계 (계면)", "누적 로그", "db/pipelines/adhesion_pipeline.json"):
        assert token in h, f"'{token}' 이 화면에 없다"
    assert len(LEDGER["log"]) >= 1 and _plain(LEDGER["log"][-1]["text"])[:12] in _txt(h), "원장의 로그가 화면에 없다"


def test_screen_follows_the_ledger_not_a_copy(client):
    """원장의 숫자·로그를 바꾸면 화면이 **따라 바뀐다** — 화면이 자체 보관하면 이 시험이 깨진다."""
    led = copy.deepcopy(LEDGER)
    led["runs"][0]["jobs"][0]["peak_vram_mib"] = 12345
    led["log"].append({"date": "2099-01-01", "stage": "dft", "text": "시험용 로그 줄 — 원장 추종 확인"})
    with _with_ledger(led):
        h = _html(client)
    assert "12,345 MiB" in h, "원장의 VRAM 값을 바꿨는데 화면이 안 바뀌었다"
    assert "시험용 로그 줄" in h, "원장에 덧붙인 로그가 화면에 없다"
    # 최신이 위 — 2099 줄이 기존 최신 줄보다 먼저 나와야 한다
    t = _txt(h)
    assert t.index("시험용 로그 줄") < t.index(_plain(LEDGER["log"][-1]["text"])[:12]), "로그가 최신-위 순서가 아니다"


def test_missing_vram_is_dash_not_zero(client):
    """⛔ 없는 값을 0 으로 그리지 않는다 — VRAM·벽시계가 빈 잡은 `—`.

    2026-09-25: 원장의 실제 잡이 다 끝나 VRAM 이 다 찼다 → 전제를 원장에 기대면 시험이 조용히
    할 일을 잃는다. **합성 잡**(값 None)을 넣어 본다.
    """
    led = copy.deepcopy(LEDGER)
    led["runs"][0]["jobs"].append({"dir": "99_synthetic_empty_vram", "state": "run",
                                   "wall_s": None, "peak_vram_mib": None})
    with _with_ledger(led):
        h = _html(client)
    row = h.split("99_synthetic_empty_vram", 1)[1].split("</tr>", 1)[0]
    assert "—" in row, "빈 값 자리에 — 가 없다"
    assert "0 MiB" not in row and "0 s" not in _txt(row), "없는 VRAM·벽시계를 0 으로 그렸다"


def test_ledger_markdown_is_rendered_not_literal(client):
    """원장 글의 마크다운(굵게·코드)이 **그려진다** — `**`·백틱이 글자로 새면 안 된다."""
    led = copy.deepcopy(LEDGER)
    led["log"].append({"date": "2099-01-03", "stage": "dft", "text": "굵게 **표지굵게** · 코드 `표지코드` · ==표지강조=="})
    with _with_ledger(led):
        h = _html(client)
    assert "<strong>표지굵게</strong>" in h or "<b>표지굵게</b>" in h, "굵게가 안 그려졌다"
    assert "<code" in h and "표지코드</code>" in h, "코드 스팬이 안 그려졌다"
    assert "<mark>표지강조</mark>" in h, "==강조== 가 안 그려졌다"
    t = _txt(h)
    assert "**" not in t and "`" not in t, "마크다운 표식이 글자로 샜다"


# ── ② 못 읽으면 말한다 ─────────────────────────────────────────────────
def test_missing_ledger_is_announced(client):
    with _with_ledger(None):
        h = _html(client)
    assert "원장을 못 읽었다" in h, "원장이 없는데 경고가 없다 — 빈 화면은 '일이 없었다' 로 읽힌다"
    assert "DFT → DEM 인계 규약" not in h


def test_dead_record_path_is_announced(client):
    led = copy.deepcopy(LEDGER)
    led["systems"][0]["records"] = ["kb/projects/없는_기록_2099.md"]
    with _with_ledger(led):
        h = _html(client)
    assert "원장이 가리키는 기록이 repo 에 없다" in h and "없는_기록_2099.md" in h


def test_repo_escape_path_is_not_ok():
    assert not D._repo_path_ok("../../etc/passwd"), "repo 밖 경로를 실재로 봤다"
    assert D._repo_path_ok("db/pipelines/adhesion_pipeline.json")


# ── ③ 결정은 원장에서 실시간 ────────────────────────────────────────────
def test_decisions_come_live_by_scope(client):
    dec = DV.decisions_by_scope("adhesion.", extra_ids=LEDGER.get("related_decisions") or ())
    assert dec["live"], "scope adhesion. 의 살아 있는 결정이 없다"
    h = _html(client)
    for d in dec["live"] + dec["folded"]:
        assert d["id"] in h, f"결정 {d['id']} 이 화면에 없다"
    states = {d["id"]: d["state"] for d in dec["folded"]}
    assert "D-2026-09-23-gabia-gpu-exception-sese" in states, "원장이 이름으로 댄 관련 결정이 빠졌다"
    assert all(s not in ("active", "proposed") for s in states.values()), "살아 있는 결정이 접힌 목록에 있다"


def test_scope_filter_rejects_others():
    """⛔음성: 다른 scope 의 결정은 이름을 대지 않으면 **안 걸린다** (추측으로 끌어오지 않는다)."""
    plain = DV.decisions_by_scope("adhesion.")
    ids = {d["id"] for d in plain["live"] + plain["folded"]}
    assert "D-2026-09-23-gabia-gpu-exception-sese" not in ids, "scope 가 다른 결정이 이름 없이 걸렸다"
    assert all(str(C.decisions()[i].get("scope", "")).startswith("adhesion.") for i in ids)
    none = DV.decisions_by_scope("없는.scope.")
    assert not none["live"] and not none["folded"]


# ── ④ 판정 전 값 없음 · COMSOL 은 이름만 ────────────────────────────────
def test_no_physics_values_before_verdict(client):
    """무이완 중간값은 open_items 에만 '중간 · 인용 금지' 로 있다 — 원장·화면에는 없어야 한다."""
    h = _html(client)
    raw = D.ADHESION_LEDGER.read_text(encoding="utf-8")
    for v in ("1.103", "1.518"):
        assert v not in raw, f"판정 전 값 {v} 이 원장에 들어왔다 (원장 규약 위반)"
        assert v not in h, f"판정 전 값 {v} 이 화면에 나왔다"
    assert any("판정 전 물리값" in x for x in LEDGER["⛔_이_원장이_하지_않는_것"]), "원장 규약 문장이 없다"


def test_comsol_is_name_only(client):
    h = _html(client)
    st = next(s for s in LEDGER["stages"] if s["key"] == "comsol")
    assert st["scope"] == "outside" and "관할 밖" in h
    card = h.split(st["title"], 1)[1].split('class="card"', 1)[0]
    assert "받는 것" not in card and "내는 것" not in card, "관할 밖 단계에 입출력을 그렸다"


# ── ⑤ 결속 음성시험 (표면별) ────────────────────────────────────────────
def test_binds_retracted_claims_in_ledger_text(client):
    """⛔음성 **표면별**: 원장 글에 철회값이 들어오면 결속되고, 선언을 지우면 미결속으로 떨어진다."""
    tgt = next(x for x in C.all_claims() if x["state"] == "retracted" and x["text"])
    led = copy.deepcopy(LEDGER)
    led["log"].append({"date": "2099-01-02", "stage": "dft",
                       "text": f"옛 값 {tgt['text']} eV 를 인용한 문장 (시험)."})
    with _with_ledger(led):
        html = _html(client)
    assert f'data-claim="{tgt["id"]}"' in html, "화면이 원장 글의 철회값에 결속을 안 붙였다"
    assert "claim-mark" in html, "표식이 텍스트 노드로 안 나갔다"
    sc = C.scan_claim_bindings(html, C.all_claims())
    assert sc["bound"] and not sc["unbound"], sc
    naked = re.sub(r'\sdata-claim="[^"]*"', "", html)
    assert C.scan_claim_bindings(naked, C.all_claims())["unbound"], \
        "선언을 지웠는데도 미결속이 아니다 — 스캐너가 이 화면을 안 본다"


# ── nav ────────────────────────────────────────────────────────────────
def test_nav_has_adhesion_and_it_is_live(client):
    urls = {i["url"] for i in N._items()}
    assert "/adhesion" in urls, "nav 에 /adhesion 이 없다 — 색인 밖 화면은 없는 화면이다"
    assert client.get("/adhesion").status_code == 200
