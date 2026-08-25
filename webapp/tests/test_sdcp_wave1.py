#!/usr/bin/env python3
"""test_sdcp_wave1.py — /sdcp 화면의 **필수 회귀**.

전부 음성 경로가 있다 — "표가 그려진다" 가 아니라 **틀린 값을 내보내는지**를 본다.
이 화면의 위험은 하나로 모인다: *basin 이 어긋난 값을 멀쩡한 값처럼 보이게 하는 것.*

    pytest webapp/tests/test_sdcp_wave1.py -q

⛔ 이 파일이 보증하지 못하는 것
  · 계산 자체의 정확성 (VASP 결과의 참·거짓).
  · basin 벌점 50 meV 의 물리적 타당성 — 그건 4점 추정이고 카드에 한계가 적혀 있다.
  · 화면 디자인.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import data as D  # noqa: E402
from app import app  # noqa: E402

RAW = json.loads((ROOT / "db" / "properties" / "sdcp_wave1_results.json")
                 .read_text(encoding="utf-8"))


def _html():
    return app.test_client().get("/sdcp").data.decode()


def test_route_renders():
    assert app.test_client().get("/sdcp").status_code == 200


def test_shared_doc_routes_unaffected():
    """doc.html 에 표를 얹었다 — data 를 안 넘기는 라우트가 깨지면 안 된다."""
    c = app.test_client()
    for url in ("/methods", "/todo"):
        assert c.get(url).status_code == 200


def test_delta_e_matches_raw_energies():
    """ΔE 는 화면에서 계산된다 — 원자료 총에너지와 어긋나면 안 된다."""
    rows = D.sdcp_wave1_rows()["dE"]
    by = {}
    for j in RAW["jobs"]:
        by.setdefault((j["fragment"], j["seed"]), {})[j["pose"]] = j
    for r in rows:
        d = by[(r["fragment"], r["seed"])]
        want = (d["Nitop"]["E_total_eV"] - d["Litop"]["E_total_eV"]) * 1000
        assert abs(r["dE_meV"] - want) < 0.051, r


def test_ptfe_dimer_two_seeds_agree():
    """★ 이 데이터셋의 신뢰 근거 — 두 시드가 0.1 meV 로 일치한다."""
    v = {r["seed"]: r["dE_meV"] for r in D.sdcp_wave1_rows()["dE"]
         if r["fragment"] == "ptfe_dimer"}
    assert set(v) == {"pm1", "net4"}
    assert abs(v["pm1"] - v["net4"]) <= 0.5, v


def test_basin_mismatch_is_flagged_not_hidden():
    """⛔음성: basin 이 어긋난 잡을 **지우면** 안 된다 — 경고와 함께 보여야 한다.

    지우면 "안 돌린 계산" 으로 보여 3일짜리 배치를 다시 돌리게 된다.
    """
    bad = [j for j in RAW["jobs"] if not j["basin_consistent"]]
    assert bad, "전제: 어긋난 잡이 실제로 있다"
    html = _html()
    for j in bad:
        assert j["job"] in html, f"어긋난 잡이 화면에서 사라졌다: {j['job']}"
    assert "다른 basin" in html


def test_no_basin_correction_applied():
    """⛔음성: 50 meV 벌점을 **빼서** 값을 고치면 안 된다 (측정이 아니라 가정이 된다).

    화면 값이 원자료와 한 글자도 달라선 안 된다.
    """
    html = _html()
    for j in RAW["jobs"]:
        assert f"{j['E_ads_eV']:.3f}" in html, j["job"]


def test_invalid_delta_e_not_counted_as_valid():
    """⛔음성: basin 이 갈린 ΔE 가 유효 집계에 들어가면 안 된다."""
    r = D.sdcp_wave1_rows()
    assert r["n_valid"] < r["n_dE"], "전제: 무효 행이 있다"
    assert r["n_valid"] == sum(1 for x in r["dE"] if x["valid"])
    for x in r["dE"]:
        assert x["valid"] == (x["basin_pair"].split("/")[0]
                              == x["basin_pair"].split("/")[1])


def test_missing_json_degrades_quietly(monkeypatch):
    """⛔음성: 원자료가 없으면 빈 dict — 예외로 화면 전체를 죽이지 않는다."""
    monkeypatch.setattr(D, "SDCP_WAVE1_JSON", ROOT / "db" / "properties" / "__none__.json")
    assert D.sdcp_wave1_rows() == {}
