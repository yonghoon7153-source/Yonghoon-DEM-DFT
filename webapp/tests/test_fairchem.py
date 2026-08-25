#!/usr/bin/env python3
"""test_fairchem.py — Fair-Chem 번들 화면의 **필수 회귀**.

인계 문서(kb/fairchem/07_webapp_handoff_for_claude.md)가 요구한 테스트를 옮긴 것이다.
전부 **음성 경로**가 있다 — "통과했다" 가 아니라 "틀린 걸 잡아내나" 를 본다.

    pytest webapp/tests/test_fairchem.py -q

⛔ 이 파일이 보증하지 **못하는 것**
  · 공식 주장의 참·거짓. claim_status 를 옮기는지만 본다.
  · 화면 디자인·접근성.
  · 번들 자체의 정확성 (그건 upstream 스냅샷 문제다).
"""
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import fairchem as FC          # noqa: E402
from app import app            # noqa: E402


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ── 무결성 ──────────────────────────────────────────────────────────────
def test_bundle_present_and_hashes_match():
    """sha256 이 전부 맞아야 한다. 하나라도 어긋나면 화면이 '공식 스냅샷' 이라고
    말할 자격이 없다 — 번들은 외부에서 왔고 repo 에 들어온 뒤 손대면 조용히 달라진다."""
    assert FC.available(), "번들이 설치되지 않았다"
    v = FC.verify_hashes()
    assert v["mismatch"] == [], f"내용이 바뀐 파일: {v['mismatch']}"
    assert v["missing"] == [], f"선언됐는데 없는 파일: {v['missing']}"
    assert v["checked"] == v["declared"], (v["checked"], v["declared"])


def test_verify_hashes_catches_tampering(tmp_path, monkeypatch):
    """[음성] 파일을 한 글자 고치면 반드시 잡아야 한다.

    이 검사가 없으면 verify_hashes 가 항상 ok 를 돌려줘도 아무도 모른다
    (양성만 있는 selftest 는 통과해도 아무것도 보증 못 한다 — CLAUDE.md)."""
    fake_root = tmp_path
    d = fake_root / "db" / "knowledge" / "fairchem"
    d.mkdir(parents=True)
    (d / "x.json").write_text('{"a":1}', encoding="utf-8")
    man = {"files": [{"repo_path": "db/knowledge/fairchem/x.json",
                      "sha256": "0" * 64}]}
    (d / "_release_manifest.json").write_text(json.dumps(man), encoding="utf-8")
    monkeypatch.setattr(FC, "ROOT", str(fake_root))
    monkeypatch.setattr(FC, "FCDIR", str(d))
    monkeypatch.setattr(FC, "MANIFEST", str(d / "_release_manifest.json"))
    FC.manifest.cache_clear()
    try:
        v = FC.verify_hashes()
        assert v["ok"] is False and v["mismatch"], "변조를 못 잡았다"
    finally:
        FC.manifest.cache_clear()


# ── 상태축을 합치지 않는다 ─────────────────────────────────────────────
def test_three_status_axes_stay_separate():
    """http_status · content_status · execution_status 는 별개 필드여야 한다.
    하나로 뭉치면 200 인데 실행 실패한 튜토리얼이 '정상' 으로 보인다."""
    rows = FC.page_status_rows()
    assert rows, "site_pages 가 비었다"
    for r in rows[:5]:
        assert "http_status" in r and "content_status" in r and "execution_status" in r


def test_source_only_orphan_not_promoted():
    """[음성] TOC 에 없는 문서(orphan)가 정상 문서로 승격되면 안 된다."""
    rows = FC.page_status_rows()
    orphans = [r for r in rows if r.get("in_toc") is False]
    for r in orphans:
        assert r.get("content_status") != "live" or r.get("in_toc") is False


# ── 논문 진행 네 단계 ──────────────────────────────────────────────────
def test_paper_stages_are_four_separate_flags():
    """색인됨 ≠ 읽음 ≠ 그림 확인 ≠ 사람 승인. 합치면 '읽었다' 가 과장된다."""
    ps = FC.papers_rows()
    assert ps, "papers 가 비었다"
    for p in ps[:5]:
        assert set(p["stages"]) == set(FC.PAPER_STAGES)


def test_human_approval_is_never_automatic():
    """[음성] 사람 승인은 코드가 절대 켜지 않는다 — 켜지면 미검토 주장이
    manuscript export 로 새어 나간다."""
    assert all(p["stages"]["human_approved"] is False for p in FC.papers_rows())


def test_digest_flag_requires_an_actual_litdb_file():
    """[음성] digest_read 는 litdb/papers/*.md 가 실제로 있을 때만 켜져야 한다."""
    litdir = ROOT / "litdb" / "papers"
    have = {p.stem.lower() for p in litdir.glob("*.md")} if litdir.is_dir() else set()
    for p in FC.papers_rows():
        if p["stages"]["digest_read"]:
            assert p["litdb_slug"] in have, f"{p['paper_id']}: 없는 digest 를 연결했다"


# ── 두 번째 정본 금지 ──────────────────────────────────────────────────
def test_crosswalk_carries_no_numeric_values():
    """⛔ 우리 수치를 번들에 복사하면 두 번째 정본이 생긴다.
    crosswalk 는 **FK 와 규칙 문장**만 들고 있어야 한다."""
    for c in FC.crosswalk_rows():
        for k, v in c.items():
            if k == "n_sources":
                continue
            assert not isinstance(v, (int, float)) or isinstance(v, bool), \
                f"{c['crosswalk_id']}.{k} 에 수치가 들어 있다 — 정본은 db/properties 다"


def test_project_rules_survive_official_support():
    """공식이 지원한다고 우리 금지가 풀리지 않는다 — 규칙 문장이 살아 있어야 한다.
    (UMA–Li3N 금지 · OMat↔MP 혼합 금지가 crosswalk 에 실려 있다)"""
    txt = json.dumps(FC.entities("lpscl_crosswalk"), ensure_ascii=False)
    assert "Li3N" in txt or "Li₃N" in txt, "Li3N 금지 규칙이 사라졌다"
    assert "Materials Project" in txt, "OMat↔MP 혼합 금지 규칙이 사라졌다"


# ── 라우트 · API ───────────────────────────────────────────────────────
def test_page_renders(client):
    """⚠ 제목 문구로 단언하지 않는다 — 문구를 다듬으면 깨지는 나쁜 테스트가 된다
    (실제로 1판이 그랬다). 화면에 **반드시 있어야 하는 사실**로 건다."""
    r = client.get("/fairchem")
    assert r.status_code == 200
    body = r.data.decode()
    assert FC.OUR_PINNED["model_id"] in body, "우리가 쓰는 모델이 화면에 없다"
    assert FC.OUR_PINNED["task"] in body, "우리가 쓰는 task 가 화면에 없다"
    assert "PBE" in body, "omat 의 기준 DFT 가 화면에 없다 — 이게 없으면 에너지의 정체를 모른다"
    assert len(body) > 8000, "페이지가 껍데기만 렌더됐다"


def test_bans_are_on_the_page(client):
    """공식이 지원해도 막아 둔 것은 **화면에서** 보여야 한다.
    db 에만 있고 화면에 없으면 아무도 안 본다."""
    body = client.get("/fairchem").data.decode()
    assert "Li₃N" in body or "Li3N" in body, "Li3N 금지가 화면에 없다"
    assert "Materials Project" in body, "OMat↔MP 혼합 금지가 화면에 없다"


def test_pinned_model_is_in_the_official_registry():
    """[음성] 우리가 고정한 모델이 공식 레지스트리에 없으면 오타이거나
    upstream 이 내린 것이다 — 조용히 지나가면 안 된다."""
    ids = {m.get("model_id") for m in FC.entities("models")}
    assert FC.OUR_PINNED["model_id"] in ids, \
        f"{FC.OUR_PINNED['model_id']} 가 레지스트리에 없다 (있는 것: {sorted(ids)})"


def test_newer_models_are_flagged_not_auto_adopted():
    """[음성] 더 새 UMA 가 있으면 알리기만 한다 — 핀이 저절로 바뀌면 안 된다."""
    newer = FC.newer_models()
    assert FC.OUR_PINNED["model_id"] not in newer, "핀이 '더 새 것' 목록에 섞였다"
    if newer:
        body = app.test_client().get("/fairchem").data.decode()
        assert any(m in body for m in newer), "새 버전이 있는데 화면이 알리지 않는다"


def test_api_envelope_shape(client):
    r = client.get("/api/fairchem/v1/models")
    assert r.status_code == 200
    o = r.get_json()
    for k in ("schema_version", "generated_at", "source_commit", "status",
              "warnings", "data"):
        assert k in o, f"봉투에 {k} 가 없다"
    assert isinstance(o["data"], list) and o["data"]


def test_api_unknown_name_is_404_not_empty(client):
    """[음성] 모르는 이름에 빈 배열을 주면 '없다' 와 '이름을 틀렸다' 가 구분 안 된다.
    fail-closed 로 404 를 낸다."""
    r = client.get("/api/fairchem/v1/definitely-not-an-entity")
    assert r.status_code == 404


def test_nav_link_present(client):
    r = client.get("/")
    assert '/fairchem' in r.data.decode(), "사이드바에 링크가 없다"

def test_screening_page_carries_the_ranking_limit(client):
    """스크리닝 화면이 **순위 한계**를 결과보다 먼저 말해야 한다.

    ⚠ 이 축의 일이 곧 '근접 후보 순위' 인데, 우리 엔진이 바로 거기서 약하다.
      각주로 달면 아무도 안 본다 — 화면에 있는지 기계가 본다.
    """
    body = client.get("/cascade").data.decode()
    assert "평균이 좋아도 순위는 틀린다" in body, "순위 한계 카드가 없다"
    for k in ("44", "16배", "best-of-N"):
        assert k in body, f"근거 수치 '{k}' 가 화면에 없다"
    # ⛔ 저자 면책을 우리 실패에 쓰지 말라는 경고가 같이 있어야 한다
    assert "6.63" in body and ("130" in body or "320" in body), \
        "near-degenerate 면책을 우리 실패에 적용하면 안 된다는 경고가 없다"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))


def test_cascade_carries_ml_transfer_insight(client):
    """스크리닝 화면이 **우리가 안 한 세 단계**를 말해야 한다.

    ⚠ kb 카드에만 있고 화면에 없으면 아무도 안 본다. 그리고 축을 넘나드는
      이전이므로 **출처가 DEM 축이라는 것**이 화면에 있어야 오해가 안 생긴다.
    """
    body = client.get("/cascade").data.decode()
    assert "우리가 안 한 세 단계" in body, "이전 인사이트 카드가 없다"
    for k in ("0.25", "0.321", "0.326", "LODO"):
        assert k in body, f"근거 수치 '{k}' 가 화면에 없다"
    # ⛔ 화학이 안 겹친다는 경고가 반드시 같이 있어야 한다 (억지 연결 방지)
    assert "화학은 하나도 안 겹친다" in body or "화학은 안 겹친다" in body, \
        "축이 다르다는 경고가 없다 — 억지 연결로 읽힌다"
    # 관계형 — 근거 문서들로 가는 길
    for link in ("/literature", "/fairchem", "microstructure_ml_transfer_to_cascade"):
        assert link in body, f"근거 링크 '{link}' 가 없다"


def test_cascade_is_readable_for_first_timers(client):
    """처음 보는 사람이 **숫자 네 개의 뜻**과 **말할 수 있는 것/없는 것**을 알 수 있어야.

    ⚠ 이 페이지는 3615/681/90/47 이 돌아다니는데 그게 뭔지 어디에도 없었다.
      그리고 난이도 표시가 없어 어디부터 어려운지 구분이 안 됐다.
    """
    body = client.get("/cascade").data.decode()
    assert "이 페이지가 무엇인가" in body, "오리엔테이션이 없다"
    for n in ("3,615", "681", "90", "47"):
        assert n in body, f"숫자 {n} 의 설명이 없다"
    assert "ESW" in body and "가른 축은" in body, "47 vs 90 을 가른 축 설명이 없다"
    # 난이도 표시 — 기초/심화가 둘 다 있어야 구분이 된다
    assert 'lv-b' in body and 'lv-a' in body, "난이도 배지가 없다"
    # 심화 카드에는 '한 줄로' 요약이 붙어야 한다
    assert body.count("한 줄로:") >= 2, "심화 카드에 평문 요약이 없다"


def test_compute_carries_hard_won_rules(client):
    """입력을 만드는 페이지에 **규율**이 있어야 실제로 지켜진다.

    ⚠ 특히 --save_traj 는 2026-07(12런) · 2026-08(21런) 두 번 빠져서 궤적이 없고,
      둘 다 화면상으로는 정상 완료였다. 그 대가가 지금 18런 재실행이다.
    """
    body = client.get("/compute").data.decode()
    assert "save_traj" in body, "궤적 저장 규율이 화면에 없다"
    assert "2–50 ps" in body or "2-50 ps" in body, "MSD 창 규약이 없다"
    assert ("Li₃N" in body or "Li3N" in body), "UMA-Li3N 금지가 없다"
    assert "600/800/1000" in body, "아레니우스 3점 규약이 없다"
    # 규율마다 **왜 생겼는지**가 붙어 있어야 한다 (근거 없는 금지는 안 지켜진다)
    assert "사고가 난 뒤" in body or "대가" in body, "규율의 유래가 없다"


def test_methods_page_has_no_retracted_value_as_live(client):
    """[음성] /methods 가 철회된 값을 살아있는 것처럼 말하면 안 된다."""
    body = client.get("/methods").data.decode()
    if "0.199" in body:
        assert "철회" in body, "0.199 가 있는데 철회 표시가 없다"


def test_glossary_has_sto_mto_and_axes(client):
    """STO/MTO 와 시간·이온 축이 용어집에 있어야 한다.

    ⚠ 2026-08-25 에 "MTO 가 시간이고 STO 가 공간이냐" 는 질문이 실제로 나왔다.
      이름이 헷갈리는 축이라 **둘 다 시간**이라는 것이 용어집에 있어야 한다.
    """
    import glossary as G
    ids = {g["id"] for g in G.GLOSSARY}
    assert {"sto-mto", "time-vs-ions"} <= ids, "STO/MTO 항목이 없다"
    e = next(g for g in G.GLOSSARY if g["id"] == "sto-mto")
    body = " ".join(str(v) for v in e.values())
    assert "공간" in body and "무관" in body, "'둘 다 시간축' 이라는 구분이 없다"
    assert "save_traj" in body, "궤적 없으면 소급 불가라는 결론이 없다"
    # 화면에도 떠야 한다
    page = client.get("/glossary").data.decode()
    assert "STO / MTO" in page, "용어집 화면에 안 뜬다"
