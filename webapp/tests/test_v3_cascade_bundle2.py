#!/usr/bin/env python3
"""test_v3_cascade_bundle2.py — `/cascade` 묶음 2 패널 (원소별 효과 · 두 축 Pareto 그림 · 2026-11-11).

결속: 숫자는 `data.cascade_bundle2()` 하나에서만 온다 — 마감 결정 active · 판독 sha16 = 마감 기록 ·
막는 게이트 없음. 하나라도 어긋나면 사유만 (표 · 그림 · 숫자 0 개).

⚠ 시험마다 음성 경로를 둔다 (해시 어긋남 · 결정 proposed · 막힌 판독 · 방향 뒤집힘 · 절대값 누출).

⛔ 이 시험이 **못 하는 것**
  · 순위 · 층이 옳은지 판정하지 않는다 — 판독 파일과 화면이 같은가만 본다 (판정은 판독기 selftest 몫).
  · 브라우저를 안 띄운다 — Plotly 그림이 실제로 그려지는지는 수동 스크린숏으로 봤다 (2026-11-11).

    pytest webapp/tests/test_v3_cascade_bundle2.py -q
"""
import json
import re
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A       # noqa: E402
import data as D      # noqa: E402

CLO = ROOT / "db" / "properties" / "cascade_axes_bundle2_closed_2026_11_11.json"


def _readout():
    clo = json.loads(CLO.read_text(encoding="utf-8"))
    rel = re.search(r"(db/properties/\S+\.json)", clo["1_확정"]["판독"]).group(1)
    return clo, json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _section(html: str) -> str:
    i, j = html.find('id="bundle2"'), html.find('class="card cascade-method"')
    assert i >= 0 and j > i, "묶음 2 패널이 페이지에 없다"
    return html[i:j]


@pytest.fixture(scope="module")
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


def test_loader_binds_to_closure_and_matches_readout():
    """양성: 마감 기록의 sha16 · 선택 · 값이 화면 데이터와 같다."""
    b = D.cascade_bundle2()
    assert b["ok"], b.get("why")
    clo, r = _readout()
    want = re.search(r"sha16 ([0-9a-f]{16})", clo["1_확정"]["판독"]).group(1)
    assert b["readout_sha16"] == want
    assert b["selection"] == clo["1_확정"]["R13_선택 (무리 A 줄의 Pareto 층 1 · DFT 확인 후보 · 결론 아님)"]
    assert len(b["rows"]) == len(r["rows"]) == 91
    by = {x["species"]: x for x in r["rows"]}
    for row in b["rows"]:
        src = by[row["species"]]
        for a in [x["key"] for x in b["axes"]]:
            assert row["values"][a] == src["values"][a], (row["species"], a)
        assert row["layer"] == src.get("pareto_layer") and row["selected"] == bool(src.get("selected"))


def test_cls_follows_width_and_direction():
    """양성 + ⛔음성 (방향): ⑤ 는 작을수록 좋다 — SiO2 (s_V −1.68) 나음 · SiS2 (+9.70) 나쁨 · SrCl2 (+0.21) 같음.
    ① 은 클수록 좋다 — As2S3 (+44.5) 나음 · CaCl2 (−2.66) 같음. 모든 칸을 판독 파일의 폭 · 방향으로 다시 낸다."""
    b = D.cascade_bundle2()
    rows = {x["species"]: x for x in b["rows"]}
    assert rows["SiO2"]["cls"]["sv_ncm"] == "better" and rows["SiS2"]["cls"]["sv_ncm"] == "worse"
    assert rows["SrCl2"]["cls"]["sv_ncm"] == "tie"
    assert rows["As2S3"]["cls"]["d_ncm"] == "better" and rows["CaCl2"]["cls"]["d_ncm"] == "tie"
    ax = {a["key"]: a for a in b["axes"]}
    for row in b["rows"]:
        for k, a in ax.items():
            v, c = row["values"][k], row["cls"][k]
            if v is None or not a["relative"]:
                assert c is None
                continue
            g = v if a["dir"] == "larger" else -v
            assert c == ("better" if g > a["w"] else "worse" if g < -a["w"] else "tie"), (row["species"], k)


def test_page_section_renders_rows_and_marks(client):
    """양성: 패널 · 91 행 · 그림 데이터 91 행 · 선택 표식 6 (텍스트 노드)."""
    sec = _section(client.get("/cascade").get_data(as_text=True))
    assert 'id="b2-gate"' not in sec
    assert sec.count("data-b2-species=") == 91
    m = re.search(r"var B2 = (\{.*?\});\n", sec, re.S)
    assert m and len(json.loads(m.group(1))["rows"]) == 91
    assert sec.count('<span class="b2-mk" title="선택 (Pareto 층 1)">◆</span>') == 6


def _num_leaves(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from _num_leaves(v)
    elif isinstance(o, list):
        for v in o:
            yield from _num_leaves(v)
    elif isinstance(o, float):
        yield o


def test_no_absolute_values_leak(client):
    """⛔음성: 절대값 (호스트 ⑤ ΔV/V · 호스트 ④ ⑤ ⑥ 원값 · G1b 앵커) 은 판독 파일에 있어도 화면에 안 나간다.

    전체 자릿수 (repr) 로 찾는다 — 소수 한두 자리로 찾으면 91 × 5 개 상대값 중 우연히 같은 모양에 걸린다
    (2026-11-11 첫 판이 '-3.9' 로 그랬다 · 누출이 아니라 시험이 거칠었다)."""
    _, r = _readout()
    absolutes = [v for v in list(_num_leaves(r.get("host") or {})) + list(_num_leaves(r["gates"]["G1b"]))
                 if abs(v) > 1e-9 and len(repr(v)) >= 8]
    assert len(absolutes) >= 3, "호스트 · 앵커 절대값을 못 모았다 — 시험이 헛것을 잰다"
    b = D.cascade_bundle2()
    blob = json.dumps(b, ensure_ascii=False)
    sec = _section(client.get("/cascade").get_data(as_text=True))
    leaked = [repr(v) for v in absolutes if repr(v) in blob or repr(v) in sec]
    assert not leaked, f"절대값이 화면 데이터에 새었다: {leaked[:5]}"
    assert "host" not in b and "gates" not in b
    for row in b["rows"]:
        assert set(row["values"]) <= {"d_ncm", "d_li", "sv_ncm", "dphi_li", "f_ins"}


def _copy_closure(tmp_path, mutate):
    c = json.loads(CLO.read_text(encoding="utf-8"))
    mutate(c)
    p = tmp_path / CLO.name
    p.write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")
    return p


def test_sha_mismatch_gives_no_numbers(client, tmp_path, monkeypatch):
    """⛔음성: 마감 기록의 sha16 이 판독 파일과 다르면 숫자 0 개 (사유만)."""
    def bad(c):
        c["1_확정"]["판독"] = re.sub(r"sha16 [0-9a-f]{16}", "sha16 0000000000000000", c["1_확정"]["판독"])
    monkeypatch.setattr(D, "CASCADE_B2_CLOSURE", _copy_closure(tmp_path, bad))
    b = D.cascade_bundle2()
    assert b["ok"] is False and "sha16" in b["why"] and "rows" not in b
    sec = _section(client.get("/cascade").get_data(as_text=True))
    assert 'id="b2-gate"' in sec and "data-b2-species=" not in sec and "var B2" not in sec


def test_decision_not_active_gives_no_numbers(monkeypatch):
    """⛔음성: 마감 결정이 active 가 아니면 (proposed · 없음) 숫자 0 개."""
    import canonical as C
    real = C.decisions()
    for state in ("proposed", None):
        fake = dict(real)
        if state is None:
            fake.pop(D.CASCADE_B2_DECISION, None)
        else:
            fake[D.CASCADE_B2_DECISION] = {**real[D.CASCADE_B2_DECISION], "decision_state": state, "status": state}
        monkeypatch.setattr(C, "decisions", lambda root=None, _f=fake: _f)
        b = D.cascade_bundle2()
        assert b["ok"] is False and "active" in b["why"] and "rows" not in b, state


def test_blocked_readout_gives_no_numbers(tmp_path, monkeypatch):
    """⛔음성: 해시가 맞아도 막는 게이트로 멈춘 판독 (G2 멈춤 꼴) 이면 숫자 0 개."""
    _, r = _readout()
    blocked = {**r, "blocking": ["G2"]}
    rel = "db/properties/cascade_axes_bundle2_readout_x_blocked.json"
    root = tmp_path / "root"
    (root / "db" / "properties").mkdir(parents=True)
    data = json.dumps(blocked, ensure_ascii=False).encode("utf-8")
    (root / rel).write_bytes(data)
    import hashlib
    sha = hashlib.sha256(data).hexdigest()[:16]
    p = _copy_closure(tmp_path, lambda c: c["1_확정"].__setitem__("판독", f"{rel} (sha16 {sha}) · CSV"))
    monkeypatch.setattr(D, "ROOT", root)
    monkeypatch.setattr(D, "CASCADE_B2_CLOSURE", p)
    b = D.cascade_bundle2()
    assert b["ok"] is False and "막는 게이트" in b["why"] and "rows" not in b


def test_missing_closure_gives_no_numbers(tmp_path, monkeypatch):
    """⛔음성: 마감 기록이 없으면 숫자 0 개."""
    monkeypatch.setattr(D, "CASCADE_B2_CLOSURE", tmp_path / "nope.json")
    b = D.cascade_bundle2()
    assert b["ok"] is False and "rows" not in b
