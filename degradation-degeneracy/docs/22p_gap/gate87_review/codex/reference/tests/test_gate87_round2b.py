"""87차 라운드 2b — R2-a 실물 v6 leg gate · R2-c 이름 체계 · G84-N2 (고정 표 `STAGE3_IMPL_ROUND1_SPEC.md` §13).

84차 리뷰어 G84-N2: v5 승인 spec (`leg_spec_version: 2`) 의 닫힌 `LEG_SPEC_FIT_KEYS` 에 `stage3: null` 을 넣으면
canonical 바이트 · digest 가 바뀌어 "기존 spec digest 불변" 과 양립하지 않는다. 그래서 v6 는 **버전 분기** — 새 builder
`leg_run_spec_v3` 가 envelope 에서 유도한 닫힌 `stage3` 축을 필수로 갖고, 소비자는 `leg_spec_version` 으로만 갈린다 (v3 계획
+ 문맥 없음 → 거부 · v2 계획 + 문맥 → 거부). 원장 계획 index 는 `planned_envelope` · `stage3_context` 를 싣는 자리를 얻고,
production 진입점 `stage3_context_from_plan` **한 곳**이 원장 → `run_fit(stage3=…)` 문맥을 만든다. CLI 는
`--stage3-plan <leg_id>`.

node 이름은 §13-6 의 s00–s07. RED 에서 "통과" 로 떨어지는 node 가 결함 증거이고, 새 함수 부재 (`AttributeError` · argparse
`unrecognized`) 는 무관 예외로 따로 센다. s00 (v5 골든) · s07 (세대 이름 집합) 은 처음부터 GREEN 이어야 하는 **골든**이다.
native 계산은 s04 양성 한 건 (tiny curves · smoke namespace) · COMSOL 0.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

from src import fitting as F
from src import io as IO
from tests import test_gate81_stage3_wire as G81
from tests import test_gate84_round2a as G84
from tests.test_preserve import _F49
from tools import design_wire as DW
from tools import preserve as PV

ROOT = Path(__file__).resolve().parents[1]
OBJS = G81.OBJS
HEX64 = "ab" * 32
SRC = IO.source_digest()
LEG = "g87_v6_leg"
DESIGN_REL = "docs/22p_gap/g87_ctx/design.json"

#: §13-2 a — 고정 입력의 v5 spec digest (2026-10-01 · `0b21490d` 의 `leg_run_spec` 으로 계산). 이 상수가 움직이면 v5
#: 승인 바이트가 움직인 것이다 — 운영 원장 `grid_fit_v5` 의 `0838df84…` 도 같은 함수가 지킨다.
V5_GOLDEN = "b8f90ad97a7509f72742f0962c50646787171fb0214ea83478c9e597117073b4"

_PIN = {"schema_version": 3, "compute_sha256": "a" * 16, "row_projection_py_sha256": "b" * 16,
        "src_scoring_py_sha256": "c" * 16, "analysis_spec_sha256": "d" * 16,
        "producer_semantic_sha256": "e" * 16}


# ─────────────────────────────────────────────────────────────────────────────
# 도구
# ─────────────────────────────────────────────────────────────────────────────
def _v5_pair(key="results/g87_golden"):
    g = {"config_digest": "a" * 16, "condition_ids_sha256": "b" * 16, "n_conditions": 12,
         "discharged_cache_sha256": HEX64, "out": key}
    f = dict(_F49, out=key, **{"in": key})
    return g, f


def _fit_axis(key="results/g87_out", in_digest=HEX64) -> dict:
    """v6 다리의 fit 절반 — adaptive · warm_start 는 끈다 (계약 v6 arm)."""
    f = copy.deepcopy(_F49)
    f["optimizer"] = {"method": "Nelder-Mead", "n_restarts": 2, "adaptive": False, "warm_start": False}
    f["objective_order"] = list(OBJS)
    f["in"] = key
    f["in_digest"] = in_digest
    f["out"] = key
    return f


def _grid_axis(key="results/g87_out") -> dict:
    return {"config_digest": "c" * 16, "condition_ids_sha256": "d" * 16, "n_conditions": 3,
            "discharged_cache_sha256": HEX64, "out": key}


def _planned(*, warm=False, source_digest=SRC, leg_id=LEG, **over) -> PV.PlannedLegV4:
    """index · 진입점 시험용 v4 계획 (곡선 없이). warm=True 면 provider 가 필요한 edge 하나."""
    inputs = {"reference": "grid", "curves_sha256": HEX64,
              "base_config_digest": F.config_closure_sha256("configs/base.yaml")}
    if warm:
        edge = {"stage": "condition", "arm": "G_C", "consumer_objective": OBJS[1], "provider_objective": OBJS[0],
                "provider_artifact_sha256": HEX64, "solution_map_sha256": HEX64, "provider_protocol_sha256": HEX64}
        return G81._planned_v4(stages=G81._stages(arm="G_C", warm_map={OBJS[0]: None, OBJS[1]: OBJS[0]}),
                               edges=[edge], source_digest=source_digest, leg_id=leg_id, inputs=inputs, **over)
    return G81._planned_v4(source_digest=source_digest, leg_id=leg_id, inputs=inputs, **over)


def _axis(env: dict) -> dict:
    return PV.stage3_axis_from_envelope(env)


def _entry(spec: dict, *, leg_id=LEG, src=SRC, envelope=None, context=None, scope="no_active_claim") -> dict:
    e = {"leg_id": leg_id, "cohort_id": "g87", "status": "planned", "authorization_kind": "prospective",
         "authorized_source_digest": src, "run_spec_digest": PV.run_spec_digest(spec), "run_spec": spec,
         "recorded_on": "2026-10-01", "근거": "87차 시험 — 운영 원장이 아니다"}
    if scope is not None:
        e["claim_scope"] = scope
    if envelope is not None:
        e["planned_envelope"] = envelope
    if context is not None:
        e["stage3_context"] = context
    return e


def _doc(*entries) -> dict:
    return {"schema_version": 4,
            "cohorts": [{"cohort_id": "g87", "dir": "docs/22p_gap/coh", "status": "active", "legs": [],
                         "prospective_legs": [e["leg_id"] for e in entries],
                         "cross_leg_comparison": "allowed_within_cohort", "pin": _PIN}],
            "planned": list(entries), "legs": []}


def _write(where: Path, doc: dict) -> Path:
    where.parent.mkdir(parents=True, exist_ok=True)
    where.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return where


def _v3_entry(p: PV.PlannedLegV4, *, grid=None, fit=None, design=DESIGN_REL, provider_runs=None, **kw) -> dict:
    env = p.envelope()
    spec = PV.leg_run_spec_v3(p.leg_id, grid or _grid_axis(), fit or _fit_axis(), _axis(env))
    ctx = {"design": design, "provider_runs": dict(provider_runs or {})}
    return _entry(spec, leg_id=p.leg_id, src=env["source_digest"], envelope=env, context=ctx, **kw)


def _reseal(e: dict) -> dict:
    """spec 을 손본 뒤 주소를 다시 맞춘다 — 자기일관 (index 의 digest 대조는 통과해야 다음 검사가 보인다)."""
    e["run_spec_digest"] = PV.run_spec_digest(e["run_spec"])
    return e


def _design_file(root: Path, design: dict, rel=DESIGN_REL) -> Path:
    q = root / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(json.dumps(design, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return q


def _add_arm(design: dict) -> None:
    """설계를 **다른 유효한 설계** (arm 하나 — G_A 만) 로 바꾼다 — digest 는 움직이고 nested schema 는 지킨다.
    (arm 추가 · arm 설명 변경은 arm registry 대조가 먼저 거부해 digest 대조가 보이지 않는다 — 두 번 실측.)"""
    design.clear()
    design.update(G81._design(arms=("G_A",)))


def _relabel(ctx: dict, leg_id: str = LEG) -> dict:
    """`_v6_context` 의 계획 (`g22p_v6_armGA_b3`) 을 이 모듈의 다리 이름으로 — 다른 필드 · 봉인 불변."""
    p = ctx["planned"]
    return {**ctx, "planned": PV.PlannedLegV4(**{**p.__dict__, "leg_id": leg_id})}


def _scratch(name: str) -> Path:
    """s02 의 **비-smoke** 산출 자리 — 결정적 경로 (변이 증인에 든 digest 가 실행마다 같아야 한다 · G67-T1-b).
    smoke namespace 밖이어야 gate 가 실제로 걸린다 (conftest 의 tmp_path 는 smoke 안으로 옮겨져 있다)."""
    import shutil
    d = Path(tempfile.gettempdir()) / "dd87" / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    return d


def _isolated_authority(monkeypatch, where: Path) -> Path:
    """원장 · claims · attempts · exec_class 파생 root 를 전부 격리 디렉터리 옆으로 (test_grid 의 49차 방식)."""
    led = where / "ledger" / "LEG_PRESERVATION.yaml"
    led.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(PV, "DEFAULT_LEDGER", led)
    monkeypatch.setattr(PV, "DEFAULT_CLAIMS_ROOT", PV.claims_root_for_ledger(led))
    return led


def _not_new_helper_missing(exc: BaseException) -> None:
    """RED 집계용 — 새 helper 부재 (`AttributeError`) 는 결함 증거가 아니라 무관 예외다."""
    assert not isinstance(exc, AttributeError), f"무관 예외 (helper 부재): {exc!r}"


# ─────────────────────────────────────────────────────────────────────────────
# s00 — v5 골든 (처음부터 GREEN 이어야 한다)
# ─────────────────────────────────────────────────────────────────────────────
def test_s00_01_the_v5_spec_bytes_and_digest_are_unchanged():
    g, f = _v5_pair()
    spec = PV.leg_run_spec("g87_golden", g, f)
    assert set(spec) == {"leg_spec_version", "leg_id", "grid", "fit"}, sorted(spec)
    assert spec["leg_spec_version"] == 2
    assert "stage3" not in spec and "stage3" not in spec["fit"], "v5 spec 에 stage3 키가 생겼다 (G84-N2)"
    assert PV.run_spec_digest(spec) == V5_GOLDEN


def test_s00_02_the_live_ledger_indexes_and_grid_fit_v5_keeps_its_address():
    idx = PV.planned_index()                    # conftest 가 세운 운영 원장 사본 (바이트 동일)
    e = idx["grid_fit_v5"]
    assert e["run_spec"]["leg_spec_version"] == 2
    assert e["run_spec_digest"].startswith("0838df841ae7e4e6")
    assert e["run_spec_digest"] == PV.run_spec_digest(e["run_spec"])
    for x in idx.values():
        assert "planned_envelope" not in x and "stage3_context" not in x, x["leg_id"]


# ─────────────────────────────────────────────────────────────────────────────
# s01 — v3 builder
# ─────────────────────────────────────────────────────────────────────────────
def test_s01_01_the_v3_builder_seals_the_stage3_axis_derived_from_the_envelope():
    p = _planned()
    env = p.envelope()
    axis = _axis(env)
    spec = PV.leg_run_spec_v3(LEG, _grid_axis(), _fit_axis(), axis)
    assert set(spec) == {"leg_spec_version", "leg_id", "grid", "fit", "stage3"}
    assert spec["leg_spec_version"] == 3 and spec["leg_id"] == LEG
    assert spec["stage3"] == axis
    assert set(axis) == set(PV.LEG_SPEC_STAGE3_KEYS) == {
        "planned_id", "pairing_design_sha256", "parameter_order_sha256", "bank", "roster_sha256",
        "provider_edges_sha256", "arm", "stage", "candidate_mode"}
    assert axis["planned_id"] == p.planned_id(), "stage3.planned_id 가 envelope digest 가 아니다"
    assert axis["pairing_design_sha256"] == env["pairing_design_sha256"]
    assert axis["parameter_order_sha256"] == env["parameter_order_sha256"]
    assert axis["bank"] == env["bank"] and set(axis["bank"]) == PV._BANK_KEYS
    assert axis["roster_sha256"] == env["roster"]["roster_sha256"]
    assert axis["provider_edges_sha256"] == PV.digest(env["provider_edges"])
    st = env["stages"][0]
    assert (axis["arm"], axis["stage"], axis["candidate_mode"]) == (st["arm"], st["stage"], st["candidate_mode"])


@pytest.mark.parametrize("mutate", [
    lambda a: a.pop("planned_id"),                                   # 누락
    lambda a: a.__setitem__("budget", 3),                            # 추가
    lambda a: a["bank"].pop("length"),                               # 중첩 열림
    lambda a: a.__setitem__("bank", {**a["bank"], "seed": 1}),       # 중첩 추가
    lambda a: a.__setitem__("planned_id", a["planned_id"][:16]),     # hex64 아님
    lambda a: a.__setitem__("roster_sha256", None),                  # 타입
    lambda a: a.__setitem__("arm", 7),                               # 타입
], ids=["missing", "extra", "bank-open", "bank-extra", "short-planned-id", "roster-none", "arm-int"])
def test_s01_02_the_v3_builder_refuses_an_open_or_mistyped_stage3_axis(mutate):
    axis = _axis(_planned().envelope())
    mutate(axis)
    with pytest.raises(PV.PreserveError):
        PV.leg_run_spec_v3(LEG, _grid_axis(), _fit_axis(), axis)


def test_s01_03_the_v3_address_moves_with_planned_id_and_differs_from_v2():
    axis = _axis(_planned().envelope())
    g, f = _grid_axis(), _fit_axis()
    d3 = PV.run_spec_digest(PV.leg_run_spec_v3(LEG, g, f, axis))
    other = dict(axis, planned_id=("0" if axis["planned_id"][0] != "0" else "1") + axis["planned_id"][1:])
    assert PV.run_spec_digest(PV.leg_run_spec_v3(LEG, g, f, other)) != d3
    assert PV.run_spec_digest(PV.leg_run_spec(LEG, g, f)) != d3, "v2 와 v3 가 같은 주소를 낸다"


def test_s01_04_grid_and_fit_checks_are_one_function_for_both_versions():
    axis = _axis(_planned().envelope())
    g, f = _grid_axis(), _fit_axis()
    for bad_g, bad_f in ((dict(g, nproc=8), f), (g, dict(f, seed=1)),
                         ({k: v for k, v in g.items() if k != "out"}, f),
                         (g, dict(f, optimizer={**f["optimizer"], "x": 1}))):
        with pytest.raises(PV.PreserveError):
            PV.leg_run_spec(LEG, bad_g, bad_f)
        with pytest.raises(PV.PreserveError):
            PV.leg_run_spec_v3(LEG, bad_g, bad_f, axis)


# ─────────────────────────────────────────────────────────────────────────────
# s02 — 소비자 분기 (`_assert_fit_authorized`) · 비-smoke out · 격리 원장
# ─────────────────────────────────────────────────────────────────────────────
def _live_pair(tmp_path, out_dir):
    """tiny curves 로 지금 코드가 만들 fit 축 + 그것을 승인하는 v6 문맥."""
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    ctx = _relabel(G81._v6_context(in_dir))
    live = F.live_fit_axis(G81._OBJ_W, _obj_cfg_min(), _BOUNDS_MIN, "expanded", 2, True, None, None, "grid",
                           False, False, "Nelder-Mead", "ocp", {}, in_dir, out_dir)
    in_digest = hashlib.sha256((in_dir / "curves.parquet").read_bytes()).hexdigest()
    return in_dir, ctx, live, in_digest


def _grid_for(live: dict) -> dict:
    return _grid_axis(live["in"])


def _run_nonsmoke(in_dir, out_dir, ctx, **kw):
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min
    return F.run_fit(in_dir, out_dir, _obj_cfg_min(), G81._OBJ_W, _BOUNDS_MIN, "expanded", 2, nproc=1,
                     adaptive=False, warm_start=False, leg=LEG, may_open=True, stage3=ctx, **kw)


def test_s02_01_a_v3_plan_without_a_stage3_context_is_refused_before_fit_one(tmp_path, monkeypatch):
    out = _scratch("s02a")
    led = _isolated_authority(monkeypatch, out)
    in_dir, ctx, live, ind = _live_pair(tmp_path, out)
    p = ctx["planned"]
    spec = PV.leg_run_spec_v3(LEG, _grid_for(live), dict(live, in_digest=ind), _axis(p.envelope()))
    _write(led, _doc(_entry(spec, src=SRC, envelope=p.envelope(),
                            context={"design": DESIGN_REL, "provider_runs": {}})))
    calls = G84._sentinel(monkeypatch)
    with pytest.raises(PV.PreserveError) as ei:
        _run_nonsmoke(in_dir, out, None)                       # legacy 호출 — stage3 없음
    assert "legacy" in str(ei.value) and "leg_spec_version 3" in str(ei.value), \
        "거부 이유가 v6 계획의 legacy fallback 금지 규칙이 아니다"
    assert calls == [], "거부가 첫 수치 작업 뒤다"
    assert PV.planned_index(ledger=led)[LEG]["status"] == "planned", "거부하면서 계획을 running 으로 옮겼다"


def test_s02_02_a_v2_plan_with_a_stage3_context_is_refused_before_fit_one(tmp_path, monkeypatch):
    out = _scratch("s02b")
    led = _isolated_authority(monkeypatch, out)
    in_dir, ctx, live, ind = _live_pair(tmp_path, out)
    spec = PV.leg_run_spec(LEG, _grid_for(live), dict(live, in_digest=ind))      # v5 계획
    _write(led, _doc(_entry(spec, src=SRC)))
    calls = G84._sentinel(monkeypatch)
    with pytest.raises(PV.PreserveError) as ei:
        _run_nonsmoke(in_dir, out, ctx)
    assert "leg_spec_version 2" in str(ei.value), "거부 이유가 v5 계획의 v6 문맥 금지 규칙이 아니다"
    assert calls == []


@pytest.mark.parametrize("version", [None, 1, 4, "3"], ids=["absent", "one", "four", "str3"])
def test_s02_03_an_unknown_or_missing_spec_version_is_refused(tmp_path, monkeypatch, version):
    out = _scratch("s02c")
    led = _isolated_authority(monkeypatch, out)
    in_dir, ctx, live, ind = _live_pair(tmp_path, out)
    p = ctx["planned"]
    spec = PV.leg_run_spec_v3(LEG, _grid_for(live), dict(live, in_digest=ind), _axis(p.envelope()))
    if version is None:
        spec.pop("leg_spec_version")
    else:
        spec["leg_spec_version"] = version
    e = _entry(spec, src=SRC, envelope=p.envelope(), context={"design": DESIGN_REL, "provider_runs": {}})
    _write(led, _doc(e))
    calls = G84._sentinel(monkeypatch)
    with pytest.raises(PV.PreserveError):
        _run_nonsmoke(in_dir, out, ctx)
    assert calls == []


def test_s02_05_an_unknown_spec_version_without_v6_slots_is_refused_by_the_consumer(tmp_path, monkeypatch):
    """index 는 v6 자리가 없는 항목의 버전을 묻지 않는다 (기존 손 spec 호환) — 그러면 소비자 분기가 마지막 방어다."""
    out = _scratch("s02e")
    led = _isolated_authority(monkeypatch, out)
    in_dir, ctx, live, ind = _live_pair(tmp_path, out)
    spec = PV.leg_run_spec(LEG, _grid_for(live), dict(live, in_digest=ind))
    spec["leg_spec_version"] = 4
    _write(led, _doc(_entry(spec, src=SRC)))
    calls = G84._sentinel(monkeypatch)
    with pytest.raises(PV.PreserveError) as ei:
        _run_nonsmoke(in_dir, out, None)
    assert "leg_spec_version" in str(ei.value) and "계약 (2 · 3) 밖" in str(ei.value), \
        "거부 이유가 spec 버전 규칙이 아니다"
    assert calls == []


def test_s02_04_a_matching_v3_plan_and_context_reach_claim_issuance(tmp_path, monkeypatch):
    out = _scratch("s02d")
    led = _isolated_authority(monkeypatch, out)
    in_dir, ctx, live, ind = _live_pair(tmp_path, out)
    p = ctx["planned"]
    spec = PV.leg_run_spec_v3(LEG, _grid_for(live), dict(live, in_digest=ind), _axis(p.envelope()))
    _write(led, _doc(_entry(spec, src=SRC, envelope=p.envelope(),
                            context={"design": DESIGN_REL, "provider_runs": {}})))
    claim, fit_axis, cap = F._assert_fit_authorized(live, out, leg=LEG, may_open=True, stage3=ctx)
    assert claim is not None and claim.attempt_id
    assert fit_axis["in_digest"] == ind
    assert PV.planned_index(ledger=led)[LEG]["status"] == "running"


# ─────────────────────────────────────────────────────────────────────────────
# s03 — 계획 index 의 v4 자리
# ─────────────────────────────────────────────────────────────────────────────
def test_s03_01_a_v3_entry_with_envelope_and_context_indexes(tmp_path):
    p = _planned()
    led = _write(tmp_path / "L.yaml", _doc(_v3_entry(p)))
    e = PV.planned_index(ledger=led)[LEG]
    assert e["planned_envelope"] == p.envelope()
    assert e["stage3_context"] == {"design": DESIGN_REL, "provider_runs": {}}
    assert e["run_spec"]["leg_spec_version"] == 3
    assert PV.assert_planned_leg(LEG, SRC, ledger=led)["leg_id"] == LEG


@pytest.mark.parametrize("drop", ["planned_envelope", "stage3_context"])
def test_s03_02_a_v3_entry_missing_either_slot_is_refused(tmp_path, drop):
    e = _v3_entry(_planned())
    e.pop(drop)
    led = _write(tmp_path / "L.yaml", _doc(e))
    with pytest.raises(PV.PreserveError) as ei:
        PV.planned_index(ledger=led)
    assert drop in str(ei.value) or "leg_spec_version" in str(ei.value), str(ei.value)


@pytest.mark.parametrize("slot", ["planned_envelope", "stage3_context", "both"])
def test_s03_03_a_v2_entry_carrying_a_v6_slot_is_refused(tmp_path, slot):
    p = _planned()
    spec = PV.leg_run_spec(LEG, _grid_axis(), _fit_axis())
    env = p.envelope() if slot in ("planned_envelope", "both") else None
    ctx = {"design": DESIGN_REL, "provider_runs": {}} if slot in ("stage3_context", "both") else None
    led = _write(tmp_path / "L.yaml", _doc(_entry(spec, envelope=env, context=ctx)))
    with pytest.raises(PV.PreserveError):
        PV.planned_index(ledger=led)


@pytest.mark.parametrize("edit", [
    lambda env, e: env.__setitem__("leg_id", "someone_else"),
    lambda env, e: env.__setitem__("source_digest", "0" * 16),
    lambda env, e: env.__setitem__("protocol_generation", "v6_prep"),
    lambda env, e: env["inputs"].__setitem__("curves_sha256", "nothex"),   # envelope 자체가 유효하지 않다 (hex64 아님)
], ids=["leg_id", "source_digest", "generation", "invalid-envelope"])
def test_s03_04_an_envelope_that_disagrees_with_the_entry_is_refused(tmp_path, edit):
    e = _v3_entry(_planned())
    edit(e["planned_envelope"], e)
    # ★ 자기일관 위조 — envelope 만 바꾸면 `run_spec.stage3 ≠ 유도값` 검사가 먼저 거부해 결속 검사가 보이지 않는다
    #   (87차 첫 재생에서 세 변이가 살아남은 이유). 바꾼 envelope 에서 축을 다시 유도하고 주소를 다시 맞춘다.
    try:
        e["run_spec"]["stage3"] = PV.stage3_axis_from_envelope(e["planned_envelope"])
    except PV.PreserveError:
        pass                                       # envelope 자체가 유효하지 않은 경우 (invalid-envelope) — 그대로 둔다
    _reseal(e)
    led = _write(tmp_path / "L.yaml", _doc(e))
    with pytest.raises(PV.PreserveError) as ei:
        PV.planned_index(ledger=led)
    assert "planned_envelope" in str(ei.value), str(ei.value)


@pytest.mark.parametrize("key", ["planned_id", "roster_sha256", "provider_edges_sha256", "arm", "candidate_mode"])
def test_s03_05_a_stage3_axis_that_is_not_derived_from_the_envelope_is_refused(tmp_path, key):
    """손으로 적은 축 ≠ 유도값 — digest 는 자기일관으로 다시 맞춘다 (index 의 주소 대조는 지나야 이 검사가 보인다)."""
    e = _v3_entry(_planned())
    s3 = e["run_spec"]["stage3"]
    if key == "arm":
        s3[key] = "G_C"
    elif key == "candidate_mode":
        s3[key] = "legacy_slot_replace" if s3[key] != "legacy_slot_replace" else "random_only"
    else:
        s3[key] = ("0" if s3[key][0] != "0" else "1") + s3[key][1:]
    _reseal(e)
    led = _write(tmp_path / "L.yaml", _doc(e))
    with pytest.raises(PV.PreserveError) as ei:
        PV.planned_index(ledger=led)
    assert "stage3" in str(ei.value), str(ei.value)


def test_s03_06_provider_runs_must_name_exactly_the_warm_consumers(tmp_path):
    # no-warm 계획에 provider 를 더하면 추가
    e = _v3_entry(_planned(), provider_runs={OBJS[1]: "results/_smoke/g87_provider"})
    with pytest.raises(PV.PreserveError) as ei:
        PV.planned_index(ledger=_write(tmp_path / "A.yaml", _doc(e)))
    assert "provider" in str(ei.value), str(ei.value)
    # warm 계획에 provider 를 빼면 누락
    e = _v3_entry(_planned(warm=True), provider_runs={})
    with pytest.raises(PV.PreserveError) as ei:
        PV.planned_index(ledger=_write(tmp_path / "B.yaml", _doc(e)))
    assert "provider" in str(ei.value), str(ei.value)
    # 맞으면 통과
    e = _v3_entry(_planned(warm=True), provider_runs={OBJS[1]: "results/_smoke/g87_provider"})
    assert PV.planned_index(ledger=_write(tmp_path / "C.yaml", _doc(e)))[LEG]["stage3_context"]["provider_runs"] \
        == {OBJS[1]: "results/_smoke/g87_provider"}


@pytest.mark.parametrize("design,provider", [
    ("/etc/design.json", None), ("../design.json", None), ("", None), ("docs/../design.json", None),
    (DESIGN_REL, "/abs/run"), (DESIGN_REL, "../run"), (DESIGN_REL, ""),
], ids=["abs-design", "dotdot-design", "empty-design", "inner-dotdot", "abs-provider", "dotdot-provider", "empty-provider"])
def test_s03_07_context_paths_must_be_repo_relative(tmp_path, design, provider):
    if provider is None:
        e = _v3_entry(_planned(), design=design)
    else:
        e = _v3_entry(_planned(warm=True), design=design, provider_runs={OBJS[1]: provider})
    with pytest.raises(PV.PreserveError):
        PV.planned_index(ledger=_write(tmp_path / "L.yaml", _doc(e)))


def test_s03_08_g74_start_conditions_still_apply_to_a_v3_plan(tmp_path):
    p = _planned()
    e = _v3_entry(p, grid=dict(_grid_axis(), discharged_cache_sha256=None))
    with pytest.raises(PV.PreserveError) as ei:
        PV.assert_planned_leg(LEG, SRC, ledger=_write(tmp_path / "A.yaml", _doc(e)))
    assert "discharged_cache_sha256" in str(ei.value)
    e = _v3_entry(p, scope=None)
    with pytest.raises(PV.PreserveError) as ei:
        PV.assert_planned_leg(LEG, SRC, ledger=_write(tmp_path / "B.yaml", _doc(e)))
    assert "claim_scope" in str(ei.value)


# ─────────────────────────────────────────────────────────────────────────────
# s04 — production 진입점 한 곳
# ─────────────────────────────────────────────────────────────────────────────
def _entry_with_design(tmp_path, ctx, *, provider_runs=None, mutate_design=None):
    """`_v6_context` 의 계획을 원장 항목으로 — 설계 JSON 은 tmp 저장소 뿌리의 논리 경로에."""
    p = ctx["planned"]
    design = copy.deepcopy(ctx["design"])
    if mutate_design:
        mutate_design(design)
    root = tmp_path / "repo"
    _design_file(root, design)
    e = _v3_entry(p, provider_runs=provider_runs)
    led = _write(root / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml", _doc(e))
    return root, led, e


def test_s04_01_the_entrypoint_builds_the_context_from_the_ledger_and_run_fit_completes(tmp_path):
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    ctx0 = _relabel(G81._v6_context(in_dir))
    root, led, e = _entry_with_design(tmp_path, ctx0)
    ctx = F.stage3_context_from_plan(LEG, ledger=led, repo_root=root)
    assert set(ctx) == {"planned", "design", "provider_runs"}
    assert ctx["planned"].planned_id() == ctx0["planned"].planned_id()
    assert ctx["planned"].envelope() == e["planned_envelope"]
    assert DW.pairing_design_sha256(ctx["design"]) == e["planned_envelope"]["pairing_design_sha256"]
    assert ctx["provider_runs"] == {}
    out = G84._run(tmp_path, "o", ctx, in_dir)                       # smoke namespace → 승인 면제 · 실제 완주
    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    assert man["run_spec"]["sig_version"] == 6
    assert man["run_spec"]["stage3"]["planned_id"] == ctx0["planned"].planned_id()
    v = IO.validate_provenance(out)
    assert [k for k in v["fail"] if k not in G81._DIRTY_TREE_CHECKS] == [], v["fail"]


def test_s04_02_a_design_file_whose_bytes_differ_from_the_plan_is_refused_before_run_fit(tmp_path, monkeypatch):
    from tests.test_fitting import _tiny_curves
    ctx0 = _relabel(G81._v6_context(_tiny_curves(tmp_path / "in")))
    root, led, _ = _entry_with_design(tmp_path, ctx0, mutate_design=_add_arm)
    called = []
    monkeypatch.setattr(F, "run_fit", lambda *a, **k: called.append(1))
    with pytest.raises((PV.PreserveError, ValueError)) as ei:
        F.stage3_context_from_plan(LEG, ledger=led, repo_root=root)
    _not_new_helper_missing(ei.value)
    assert "pairing_design_sha256" in str(ei.value), str(ei.value)       # digest 대조 경로 (schema 거부가 아니다)
    assert called == []


def test_s04_03_a_missing_design_file_or_provider_dir_is_refused(tmp_path):
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    # 설계 파일 없음
    ctx0 = _relabel(G81._v6_context(in_dir))
    root, led, _ = _entry_with_design(tmp_path, ctx0)
    (root / DESIGN_REL).unlink()
    with pytest.raises((PV.PreserveError, ValueError, FileNotFoundError)) as ei:
        F.stage3_context_from_plan(LEG, ledger=led, repo_root=root)
    _not_new_helper_missing(ei.value)
    # provider 디렉터리 없음 (warm 계획)
    edge = {"stage": "condition", "arm": "G_C", "consumer_objective": OBJS[1], "provider_objective": OBJS[0],
            "provider_artifact_sha256": HEX64, "solution_map_sha256": HEX64, "provider_protocol_sha256": HEX64}
    ctxw = _relabel(G81._v6_context(in_dir, arm="G_C", warm_map={OBJS[0]: None, OBJS[1]: OBJS[0]}, edges=[edge]))
    root2 = tmp_path / "repo2"
    _design_file(root2, ctxw["design"])
    led2 = _write(root2 / "docs/22p_gap/LEG_PRESERVATION.yaml",
                  _doc(_v3_entry(ctxw["planned"], provider_runs={OBJS[1]: "results/_smoke/g87_no_such_run"})))
    with pytest.raises((PV.PreserveError, ValueError, FileNotFoundError)) as ei:
        F.stage3_context_from_plan(LEG, ledger=led2, repo_root=root2)
    _not_new_helper_missing(ei.value)
    assert "provider" in str(ei.value), str(ei.value)


def test_s04_04_the_entrypoint_does_not_trust_the_index_for_planned_id(tmp_path, monkeypatch):
    """index 가 뚫려도 (monkeypatch) 진입점은 envelope 를 다시 세워 `run_spec.stage3.planned_id` 와 대조한다."""
    from tests.test_fitting import _tiny_curves
    ctx0 = _relabel(G81._v6_context(_tiny_curves(tmp_path / "in")))
    root, led, e = _entry_with_design(tmp_path, ctx0)
    bad = copy.deepcopy(e)
    pid = bad["run_spec"]["stage3"]["planned_id"]
    bad["run_spec"]["stage3"]["planned_id"] = ("0" if pid[0] != "0" else "1") + pid[1:]
    monkeypatch.setattr(PV, "planned_index", lambda ledger=None: {LEG: bad})
    with pytest.raises((PV.PreserveError, ValueError)) as ei:
        F.stage3_context_from_plan(LEG, ledger=led, repo_root=root)
    _not_new_helper_missing(ei.value)
    assert "planned_id" in str(ei.value), str(ei.value)


def test_s04_05_an_unknown_leg_is_refused(tmp_path):
    led = _write(tmp_path / "L.yaml", _doc(_v3_entry(_planned())))
    with pytest.raises(PV.PreserveError):
        F.stage3_context_from_plan("no_such_leg", ledger=led, repo_root=tmp_path)


def test_s04_06_a_context_that_disagrees_with_the_plan_is_still_refused_by_prepare_stage3(tmp_path, monkeypatch):
    """진입점을 건너 손으로 어긋난 문맥을 만들어도 `run_fit` 안의 대조가 거부한다 (83차 N2 — 우회 없음)."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    ctx = G81._v6_context(in_dir)
    other = copy.deepcopy(ctx["design"]); _add_arm(other)
    calls = G84._sentinel(monkeypatch)
    with pytest.raises(ValueError) as ei:
        G84._run(tmp_path, "o", {**ctx, "design": other}, in_dir)
    assert "pairing_design_sha256" in str(ei.value) and calls == []


# ─────────────────────────────────────────────────────────────────────────────
# s05 — CLI argv (`python -m src.fitting --stage3-plan`)
# ─────────────────────────────────────────────────────────────────────────────
def _cli(monkeypatch, *argv):
    seen = {"ctx": [], "run": []}
    monkeypatch.setattr(F, "stage3_context_from_plan",
                        lambda leg, **kw: (seen["ctx"].append(leg), {"planned": "P", "design": "D", "provider_runs": {}})[1])
    monkeypatch.setattr(F, "run_fit", lambda **kw: (seen["run"].append(kw), {"ok": True})[1])
    monkeypatch.setattr(sys, "argv", ["src.fitting", "--in", "results/_smoke/g87_in", "--nproc", "1", *argv])
    return seen


def test_s05_01_stage3_plan_conflicting_with_leg_exits_before_reading_the_ledger(monkeypatch):
    seen = _cli(monkeypatch, "--stage3-plan", "X", "--leg", "Y", "--no-adaptive", "--no-warm-start")
    with pytest.raises(SystemExit) as ei:
        F.main()
    assert ei.value.code == 2
    assert seen["ctx"] == [] and seen["run"] == []


@pytest.mark.parametrize("flags", [(), ("--no-adaptive",), ("--no-warm-start",)], ids=["none", "adaptive-only", "warm-only"])
def test_s05_02_stage3_plan_requires_explicit_no_adaptive_and_no_warm_start(monkeypatch, flags):
    seen = _cli(monkeypatch, "--stage3-plan", "X", *flags)
    with pytest.raises(SystemExit) as ei:
        F.main()
    assert ei.value.code == 2
    assert seen["ctx"] == [] and seen["run"] == []


def test_s05_03_stage3_plan_builds_the_context_once_and_hands_it_to_run_fit(monkeypatch):
    seen = _cli(monkeypatch, "--stage3-plan", "X", "--no-adaptive", "--no-warm-start")
    F.main()
    assert seen["ctx"] == ["X"], "CLI 가 stage3_context_from_plan 을 한 번 부르지 않았다"
    (kw,) = seen["run"]
    assert kw["stage3"] == {"planned": "P", "design": "D", "provider_runs": {}}
    assert kw["leg"] == "X" and kw["adaptive"] is False and kw["warm_start"] is False


def test_s05_04_stage3_plan_with_the_same_leg_is_accepted(monkeypatch):
    seen = _cli(monkeypatch, "--stage3-plan", "X", "--leg", "X", "--no-adaptive", "--no-warm-start")
    F.main()
    assert seen["ctx"] == ["X"] and seen["run"][0]["leg"] == "X"


def test_s05_05_without_stage3_plan_the_legacy_argv_passes_no_context(monkeypatch):
    seen = _cli(monkeypatch)
    F.main()
    assert seen["ctx"] == []
    (kw,) = seen["run"]
    assert kw.get("stage3") is None and kw["adaptive"] is True and kw["warm_start"] is True


# ─────────────────────────────────────────────────────────────────────────────
# s06 — run.sh dry
# ─────────────────────────────────────────────────────────────────────────────
#: 2026-10-01 `0b21490d` 실측 — `--stage3-plan` 없는 fit 의 dry argv (골든 · 바이트 불변)
FIT_DRY_GOLDEN = ("--in results/_smoke/x --nproc 4 --bounds expanded --log-level INFO --out results/_smoke/y "
                  "--reference grid --may-open")


def _dry(*argv):
    env = {k: v for k, v in os.environ.items() if k != "LEG"}
    env["RUN_SH_DRY"] = "1"
    return subprocess.run(["bash", str(ROOT / "run.sh"), *argv], cwd=ROOT, capture_output=True, text=True, env=env)


def test_s06_01_fit_dry_argv_without_stage3_plan_is_unchanged():
    r = _dry("--mode", "fit", "--in", "results/_smoke/x", "--out", "results/_smoke/y", "--nproc", "4")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == FIT_DRY_GOLDEN, r.stdout


def test_s06_02_fit_dry_argv_carries_stage3_plan_and_leg_exactly_once():
    r = _dry("--mode", "fit", "--in", "results/_smoke/x", "--out", "results/_smoke/y", "--nproc", "4",
             "--stage3-plan", "X", "--no-adaptive", "--no-warm-start")
    assert r.returncode == 0, r.stderr
    argv = r.stdout.strip().split()
    assert argv.count("--stage3-plan") == 1 and argv[argv.index("--stage3-plan") + 1] == "X", \
        "fit dry argv 에 --stage3-plan X 가 정확히 한 번 있어야 한다"
    assert argv.count("--leg") == 1 and argv[argv.index("--leg") + 1] == "X", "fit dry argv 에 --leg X 가 정확히 한 번 있어야 한다"
    assert "--no-adaptive" in argv and "--no-warm-start" in argv
    assert argv.count("--may-open") == 1


def test_s06_03_stage3_plan_conflicting_with_leg_is_refused_by_the_shell():
    r = _dry("--mode", "fit", "--in", "results/_smoke/x", "--out", "results/_smoke/y",
             "--stage3-plan", "X", "--leg", "Y")
    assert r.returncode == 1 and "--stage3-plan" in r.stderr, "셸이 --stage3-plan 과 --leg 의 충돌을 거부하지 않았다"


@pytest.mark.parametrize("mode", ["all", "grid"])
def test_s06_04_stage3_plan_is_only_valid_for_mode_fit(mode):
    r = _dry("--mode", mode, "--in", "results/_smoke/x", "--out", "results/_smoke/y", "--stage3-plan", "X")
    assert r.returncode == 1 and "--stage3-plan" in r.stderr, f"--mode {mode} 에서 --stage3-plan 이 거부되지 않았다"


# ─────────────────────────────────────────────────────────────────────────────
# s07 — 세대 이름 체계 (R2-c · 골든)
# ─────────────────────────────────────────────────────────────────────────────
def test_s07_01_the_generation_name_is_v6_and_the_generation_table_values_are_declared_names():
    from tests import test_docs_lint as DL
    creg = DL._claim_status()
    gens = list(creg.get("protocol_generations") or [])
    assert DW.STAGE3_PROTOCOL_GENERATION == "v6" and "v6" in gens, gens
    values = set((creg.get("source_digest_generations") or {}).values())
    assert values <= set(gens), sorted(values - set(gens))
    assert all(PV._GENERATION_RE.match(g) for g in gens), gens
    # validator 세대를 이름으로 등록하지 않는다 — `v6` 값은 실물 v6 leg 의 봉인 투영이 있을 때만
    for d, gen in (creg.get("source_digest_generations") or {}).items():
        if gen != "v6":
            continue
        legs = (creg.get("source_digest_evidence") or {}).get(d) or []
        assert legs, f"{d}: v6 로 등록됐는데 근거 다리가 없다 (R2-c)"
        for leg in legs:
            projs = DL._sealed_projections(leg)
            assert projs and all(p.get("protocol_generation") == "v6" for p in projs.values()), (d, leg)
