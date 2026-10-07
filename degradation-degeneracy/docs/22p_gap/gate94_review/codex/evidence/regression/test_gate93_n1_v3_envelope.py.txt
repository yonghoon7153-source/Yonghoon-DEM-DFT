"""★ 93차 G93-N1 — 유효한 planned-leg/v3 envelope 가 sig6 의 v6 재유도로 넘어가는 경로.

`check_planned_envelope` (역사 reader · 공통) 는 유효한 v3 에 `[]` 를 돌려준다. v6 의 schema 검사
(`stage3_planned_envelope`) 와 축 유도 (`stage3_축_유도`) 는 실패하지만, 재유도 차단 분기는 reader 의 결과
(`ebad`) 만 보았다 → 정상 map · fits 가 있으면 `_stage3_rederive` 로 넘어가 v4 전용 키
(`parameter_order_sha256`) 접근에서 `KeyError` 로 빠진다 (설계 SHA 를 대조군과 맞춘 경우).

고정하는 것:
  n1   sig6 + 유효 v3 → 구조화된 실패 (예외 0) · 재유도 호출 0 · 재유도 4 검사는 "실패" 로 남는다
  c1   대조 — 정상 v4 는 지금처럼 통과하고 재유도를 부른다
  c2   대조 — planned_id **단독** 불일치는 지금처럼 `stage3_planned_envelope` 만 실패시키고 재유도는 그대로 돈다
"""
from __future__ import annotations

import pytest

from tests import test_gate81_stage3_wire as G81
from tests import test_gate82_residuals as G82
from tests import test_gate85_closure_members as G85
from tests.test_gate92_stage4_linkage import _copy, _edit_s3, _flip, _validate_no_rederive, runs  # noqa: F401
from tools import preserve as PV

REDERIVE = ("후보_재유도", "실현_재계산", "restart_예산_완주", "관측_roster_재구성")


def _as_v3(env: dict) -> None:
    """v4 envelope 를 **같은 이름의 값** 으로 유효한 planned-leg/v3 로 바꾼다 (설계 SHA · 세대 · source_digest 유지)."""
    st0 = env["stages"][0]
    v3 = {
        "schema": "planned-leg/v3",
        "leg_id": env["leg_id"],
        "protocol_generation": env["protocol_generation"],
        "pairing_design_sha256": env["pairing_design_sha256"],
        "source_digest": env["source_digest"],
        "objectives": sorted(env["objective_order"]),
        "total_start_budget": sum(st0["budget_by_objective"].values()),
        "candidate_mode": st0["candidate_mode"],
        "min_retention_days": env["min_retention_days"],
    }
    assert PV.check_planned_envelope(v3) == [], "fixture 가 유효한 v3 를 만들지 못했다 — 이 시험의 전제"
    env.clear()
    env.update(v3)


def test_g93_n1_a_valid_v3_envelope_under_sig6_is_refused_without_rederivation(runs, tmp_path, monkeypatch):
    out = _copy(runs["base"], tmp_path)
    G82._forge_stage3(out, env_mutate=_as_v3)
    G85._resign(out)
    v, calls = _validate_no_rederive(out, monkeypatch)       # KeyError 등 예외는 여기서 그대로 올라온다 (음성 PASS 아님)
    assert calls == [], "유효 v3 envelope 로 v6 후보 재유도를 불렀다"
    assert "stage3_planned_envelope" in v["fail"], v["fail"]
    for k in REDERIVE:
        assert k in v["fail"], f"재유도를 막았으면 {k} 는 통과가 아니라 실패로 남아야 한다: {v['fail']}"
        assert "planned-leg/v4" in str(v["checks"][k]), f"{k} 의 이유가 v4 경계를 말하지 않는다: {v['checks'][k]}"


def test_g93_c1_a_normal_v4_run_still_validates_and_rederives(runs, tmp_path, monkeypatch):
    out = _copy(runs["base"], tmp_path)
    v, calls = _validate_no_rederive(out, monkeypatch)
    assert G81._fails(v) == [], v["fail"]
    assert calls, "정상 v4 는 재유도를 불러야 한다"


def test_g93_c2_a_planned_id_only_mismatch_keeps_its_meaning(runs, tmp_path, monkeypatch):
    out = _copy(runs["base"], tmp_path)
    _edit_s3(out, lambda s3: s3.update(planned_id=_flip(s3["planned_id"])))
    v, calls = _validate_no_rederive(out, monkeypatch)
    assert "stage3_planned_envelope" in v["fail"], v["fail"]
    assert calls, "planned_id 단독 불일치는 재유도 차단 사유가 아니었다 (기존 의미 유지)"
    for k in REDERIVE:
        assert "planned-leg/v4" not in str(v["checks"].get(k, "")), f"{k} 가 v4 경계 차단으로 바뀌었다: {v['checks'][k]}"
