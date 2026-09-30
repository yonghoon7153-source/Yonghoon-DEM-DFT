"""라운드 2a — 84차 정정 반영 고정 표 `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` §11.

G84-N1 (§11-2) base-config closure 의 hex64 결속 — 같은 preimage · v5 hex16 유지 · staged closure 대조 · v6 null 거부.
G84-N3 (§11-3) 시작 전 공통 경계 — v6 거부 · source/config/reference 결속이 halfcell `_fit_one` · worker 보다 앞.
G84-N4 (§11-4) `finite` · `converged` 계수 + `execution-record/v2` — writer · consumer schema 분기 · v1 원문 · 하향 거부.
R2-e   dead 정의 삭제 — 역사적 reader 의미 불변.

RED 는 결함 이유로만 센다 — 새 API 의 AttributeError/TypeError 는 무관 예외 (요청문 §3 에서 분리).
"""
from __future__ import annotations

import copy
import inspect
import json
import math
import shutil
from pathlib import Path

import pandas as pd
import pytest
import yaml

from src import fitting as F
from src import io as IO
from tests import test_gate81_stage3_wire as G81
from tests import test_gate82_residuals as G82
from tools import preserve as PV

OBJS = G81.OBJS
ROOT = Path(__file__).resolve().parents[1]
BASE_CFG = "configs/base.yaml"


# ─────────────────────────────────────────────────────────────────────────────
# 도구
# ─────────────────────────────────────────────────────────────────────────────
def _hex64_plan_ctx(in_dir, **kw):
    """§11-2 — 계획 `inputs.base_config_digest` 를 실행이 읽는 closure 의 hex64 로 채운 v6 문맥."""
    ctx = G81._v6_context(in_dir, **kw)
    p = ctx["planned"]
    inputs = {**p.inputs, "base_config_digest": F.config_closure_sha256(BASE_CFG)}
    ctx["planned"] = PV.PlannedLegV4(**{**p.__dict__, "inputs": inputs})
    return ctx


def _with_plan(ctx, **over):
    p = ctx["planned"]
    return {**ctx, "planned": PV.PlannedLegV4(**{**p.__dict__, **over})}


def _run(tmp_path, name, ctx, in_dir, **kw):
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min
    out = tmp_path / name
    F.run_fit(in_dir, out, _obj_cfg_min(), G81._OBJ_W, _BOUNDS_MIN, "expanded", kw.pop("n_restarts", 2),
              nproc=1, adaptive=False, warm_start=False, stage3=ctx, **kw)
    return out


def _sentinel(monkeypatch):
    """`_fit_one` 에 도달하면 즉시 표가 난다 — 시작 전 거부가 **첫 수치 작업보다 앞**인지 잰다 (native 계산 0)."""
    calls: list = []

    def reached(task):
        calls.append(task.get("cond_id"))
        raise AssertionError("_fit_one 에 도달했다 — 시작 전 경계가 수치 작업 뒤에 있다")
    monkeypatch.setattr(F, "_fit_one", reached)
    return calls


def _copy_configs(tmp: Path, *, parent_edit=None, leaf_edit=None) -> Path:
    """`configs/base.yaml` + 그것을 extends 하는 leaf 를 tmp 저장소 뿌리에 같은 논리 경로로 복사한다."""
    (tmp / "configs").mkdir(parents=True, exist_ok=True)
    base = yaml.safe_load((ROOT / BASE_CFG).read_text(encoding="utf-8"))
    if parent_edit:
        parent_edit(base)
    (tmp / BASE_CFG).write_text(yaml.safe_dump(base, allow_unicode=True, sort_keys=False), encoding="utf-8")
    leaf = {"extends": "base.yaml", "note": "gate84 leaf"}
    if leaf_edit:
        leaf_edit(leaf)
    (tmp / "configs" / "g84_leaf.yaml").write_text(yaml.safe_dump(leaf, allow_unicode=True), encoding="utf-8")
    return tmp / "configs" / "g84_leaf.yaml"


# ═════════════════════════════════════════════════════════════════════════════
# G84-N1 — base-config closure hex64
# ═════════════════════════════════════════════════════════════════════════════
def test_g84_n1_00_hex64_shares_the_preimage_with_the_legacy_hex16_and_binds_the_whole_closure(tmp_path):
    """같은 preimage: hex64[:16] == 기존 hex16 (v5 승인 축 불변) · parent 만 바꿔도 · leaf 만 바꿔도 다르다 ·
    같은 논리 입력의 다른 staging 위치는 같다 (키가 저장소 상대경로)."""
    full = F.config_closure_sha256(BASE_CFG)
    assert isinstance(full, str) and len(full) == 64 and int(full, 16) >= 0
    assert full[:16] == F._config_closure_digest(BASE_CFG), "v5 hex16 은 같은 preimage 의 접두어여야 한다"
    a = _copy_configs(tmp_path / "a")
    b = _copy_configs(tmp_path / "b")
    da = F.config_closure_sha256(a, repo_root=tmp_path / "a")
    assert da == F.config_closure_sha256(b, repo_root=tmp_path / "b"), "다른 staging 위치 · 같은 논리 입력 → 같은 digest"
    c = _copy_configs(tmp_path / "c", parent_edit=lambda d: d.setdefault("_g84", {}).update(x=1))
    assert F.config_closure_sha256(c, repo_root=tmp_path / "c") != da, "parent 변경이 digest 에 잡혀야 한다"
    d = _copy_configs(tmp_path / "d", leaf_edit=lambda l: l.update(note="changed"))
    assert F.config_closure_sha256(d, repo_root=tmp_path / "d") != da, "leaf 변경이 digest 에 잡혀야 한다"


def test_g84_n1_01_a_v6_plan_with_null_base_config_digest_does_not_start(tmp_path, monkeypatch):
    """v6 실행은 base-config 를 읽는다 → 계획 `null` 은 우회가 아니라 거부 (§11-2). 첫 수치 작업 전."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    calls = _sentinel(monkeypatch)
    ctx = _hex64_plan_ctx(in_dir)
    ctx = _with_plan(ctx, inputs={**ctx["planned"].inputs, "base_config_digest": None})   # 라운드 1 fixture 의 모양
    with pytest.raises(ValueError, match="base_config_digest"):
        _run(tmp_path, "o", ctx, in_dir)
    assert calls == [] and not (tmp_path / "o" / "fits.parquet").exists()


def test_g84_n1_02_a_truncated_or_padded_hex16_is_not_the_closure(tmp_path, monkeypatch):
    """16자 접두어를 0 으로 padding 한 값 — 형식(hex64)은 맞지만 closure 가 아니다."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    calls = _sentinel(monkeypatch)
    padded = F._config_closure_digest(BASE_CFG) + "0" * 48
    ctx = _hex64_plan_ctx(in_dir)
    ctx = _with_plan(ctx, inputs={**ctx["planned"].inputs, "base_config_digest": padded})
    with pytest.raises(ValueError, match="base_config_digest"):
        _run(tmp_path, "o", ctx, in_dir)
    assert calls == []


def test_g84_n1_03_a_plan_sealed_on_a_changed_parent_does_not_start_on_the_real_closure(tmp_path, monkeypatch):
    """계획은 parent 를 바꾼 closure 의 hex64 · 실행은 실제 staged closure → 시작 전 거부 (이유: base_config_digest)."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    calls = _sentinel(monkeypatch)
    c = _copy_configs(tmp_path / "c", parent_edit=lambda d: d.setdefault("_g84", {}).update(x=1))
    other = F.config_closure_sha256(c, repo_root=tmp_path / "c")
    ctx = _hex64_plan_ctx(in_dir)
    ctx = _with_plan(ctx, inputs={**ctx["planned"].inputs, "base_config_digest": other})
    with pytest.raises(ValueError, match="base_config_digest"):
        _run(tmp_path, "o", ctx, in_dir)
    assert calls == []


def test_g84_n1_04_the_validator_rebuilds_the_closure_from_the_sealed_snapshots(tmp_path):
    """validator: run_spec 의 closure hex64 · 계획 digest 를 **봉인 스냅샷 바이트**에서 다시 만든 값과 대조한다.
    run_spec · 계획 · record 를 함께 바꾼 자기일관 위조는 스냅샷 재계산만이 잡는다."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = _run(tmp_path, "o", _hex64_plan_ctx(in_dir), in_dir)
    v = IO.validate_provenance(out)
    assert v["checks"].get("base_config_결속") == "통과", v["checks"].get("base_config_결속", "검사 없음")
    assert G81._fails(v) == [], v["fail"]
    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    s3 = man["run_spec"]["stage3"]
    want = F.config_closure_sha256(BASE_CFG)
    assert s3["base_config_closure_sha256"] == want == s3["planned_envelope"]["inputs"]["base_config_digest"]
    restore = G81._snapshot(out)
    forged = "f" * 64
    G82._forge_stage3(out, env_mutate=lambda e: e["inputs"].update(base_config_digest=forged))
    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    man["run_spec"]["stage3"]["base_config_closure_sha256"] = forged
    (out / "manifest.yaml").write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
    v = IO.validate_provenance(out)
    assert "base_config_결속" in v["fail"], v["fail"]
    restore()


# ═════════════════════════════════════════════════════════════════════════════
# G84-N3 — 시작 전 공통 경계
# ═════════════════════════════════════════════════════════════════════════════
def test_g84_n3_00_a_plan_with_another_source_digest_is_refused_before_any_fitting(tmp_path, monkeypatch):
    """계획 `source_digest` ≠ 실행 `source_digest()` → 첫 수치 작업 전 거부 (grid 경로)."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    calls = _sentinel(monkeypatch)
    ctx = _with_plan(_hex64_plan_ctx(in_dir), source_digest="deadbeefcafe0001")
    with pytest.raises(ValueError, match="source_digest"):
        _run(tmp_path, "o", ctx, in_dir)
    assert calls == [] and not (tmp_path / "o" / "fits.parquet").exists()


def test_g84_n3_01_halfcell_reference_under_a_v6_context_is_refused_before_the_p_ini_self_fit(tmp_path, monkeypatch):
    """★ G84-N3 핵심 — halfcell 분기의 `_fit_one` (원점 self-fit) 이 `_prepare_stage3` 보다 앞이다. v6 거부는 그 앞에
    있어야 한다: sentinel 도달 0 · 이유는 reference/p_ini."""
    import src.halfcell as H
    from tests.test_fitting import _fake_halfcell_cache, _tiny_curves
    cache = _fake_halfcell_cache(tmp_path)
    monkeypatch.setattr(H, "halfcell_cache_path", lambda cfg, cache_dir=None, method="ocp", **kw: cache)
    in_dir = _tiny_curves(tmp_path / "in")
    ctx = _hex64_plan_ctx(in_dir)
    calls = _sentinel(monkeypatch)
    from tests.test_fitting import _obj_cfg_min
    with pytest.raises(ValueError, match="reference|p_ini"):
        F.run_fit(in_dir, tmp_path / "o", _obj_cfg_min(), G81._OBJ_W,
                  {"init": [1.05, -0.05, 1.4, -0.4], "lb": [0.5, -1.5, 0.5, -1.5], "ub": [3.0, 1.0, 3.0, 1.0]},
                  "halfcell", 2, nproc=1, reference="halfcell", adaptive=False, warm_start=False, stage3=ctx)
    assert calls == [], f"원점 self-fit 에 도달했다: {calls}"
    assert not (tmp_path / "o" / "fits.parquet").exists()


def test_g84_n3_02_plan_reference_must_equal_the_run_reference(tmp_path, monkeypatch):
    """계획 `inputs.reference` 가 실행 reference 와 다르면 시작하지 않는다."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    calls = _sentinel(monkeypatch)
    ctx = _hex64_plan_ctx(in_dir)
    ctx = _with_plan(ctx, inputs={**ctx["planned"].inputs, "reference": "halfcell"})
    with pytest.raises(ValueError, match="reference"):
        _run(tmp_path, "o", ctx, in_dir)
    assert calls == []


def test_g84_n3_04_a_plan_that_itself_claims_halfcell_is_still_refused_before_the_self_fit(tmp_path, monkeypatch):
    """★ 변이 생존자에서 나온 회귀 — `preflight-refuses-non-grid-reference-before-self-fit-g84` 가 n3_01 로는 안 죽었다
    (n3_01 의 계획은 `inputs.reference="grid"` 라서 reference 대조가 대신 막았다). 계획 **자체가** halfcell 을
    주장하면 (`inputs.reference="halfcell"` · 실행 reference halfcell) 두 값이 같아서 대조로는 못 막고, 오직
    `reference != "grid"` 거부만 남는다 — 그 거부가 원점 self-fit **앞**에 있어야 한다. RED 목격: 변이 rc 0 (이 시험
    추가 전) → rc 1."""
    import src.halfcell as H
    from tests.test_fitting import _fake_halfcell_cache, _obj_cfg_min, _tiny_curves
    cache = _fake_halfcell_cache(tmp_path)
    monkeypatch.setattr(H, "halfcell_cache_path", lambda cfg, cache_dir=None, method="ocp", **kw: cache)
    in_dir = _tiny_curves(tmp_path / "in")
    ctx = _hex64_plan_ctx(in_dir)
    ctx = _with_plan(ctx, inputs={**ctx["planned"].inputs, "reference": "halfcell"})
    calls = _sentinel(monkeypatch)
    with pytest.raises(ValueError, match="reference='grid'"):
        F.run_fit(in_dir, tmp_path / "o", _obj_cfg_min(), G81._OBJ_W,
                  {"init": [1.05, -0.05, 1.4, -0.4], "lb": [0.5, -1.5, 0.5, -1.5], "ub": [3.0, 1.0, 3.0, 1.0]},
                  "halfcell", 2, nproc=1, reference="halfcell", adaptive=False, warm_start=False, stage3=ctx)
    assert calls == [], f"원점 self-fit 에 도달했다: {calls}"
    assert not (tmp_path / "o" / "fits.parquet").exists()


def test_g84_n3_03_a_valid_v6_plan_reaches_the_prepared_state_and_legacy_halfcell_is_untouched(tmp_path, monkeypatch):
    """양성: 유효 v6 는 준비 지점(`_prepare_stage3` 반환)까지 도달한다 · legacy halfcell (stage3 없음) 은 예전처럼
    원점 self-fit 을 **한다** (경계가 legacy 를 막지 않는다)."""
    import src.halfcell as H
    from tests.test_fitting import _fake_halfcell_cache, _obj_cfg_min, _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    seen = []
    real_prepare = F._prepare_stage3

    def spy(*a, **k):
        seen.append("prepared")
        return real_prepare(*a, **k)
    monkeypatch.setattr(F, "_prepare_stage3", spy)
    out = _run(tmp_path, "o", _hex64_plan_ctx(in_dir), in_dir)
    assert seen == ["prepared"] and (out / "fits.parquet").exists()
    # legacy halfcell — sentinel 이 **도달해야** 한다 (원점 self-fit 은 legacy 의 정상 동작)
    cache = _fake_halfcell_cache(tmp_path)
    monkeypatch.setattr(H, "halfcell_cache_path", lambda cfg, cache_dir=None, method="ocp", **kw: cache)
    calls = _sentinel(monkeypatch)
    with pytest.raises(AssertionError, match="_fit_one 에 도달"):
        F.run_fit(in_dir, tmp_path / "legacy", _obj_cfg_min(), {"aa": {"w_pocv": 1.0}},
                  {"init": [1.05, -0.05, 1.4, -0.4], "lb": [0.5, -1.5, 0.5, -1.5], "ub": [3.0, 1.0, 3.0, 1.0]},
                  "halfcell", 1, nproc=1, reference="halfcell")
    assert len(calls) == 1


# ═════════════════════════════════════════════════════════════════════════════
# G84-N4 — finite · converged · execution-record/v2
# ═════════════════════════════════════════════════════════════════════════════
def _rows_of(out) -> tuple:
    fits = pd.read_parquet(out / "fits.parquet")
    return fits, {(c, o): json.loads(v) for c, o, v in zip(fits["cond_id"], fits["objective"], fits["restarts_json"])}


def test_g84_n4_00_the_writer_emits_v2_with_finite_and_converged_that_match_the_rows(tmp_path):
    """writer → `execution-record/v2` · objective 마다 `finite` (저장 J 유한 수) · `converged` (legacy true 수) ·
    `0 ≤ finite, converged ≤ returned` · validator 재계산과 계획 대조 통과."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = _run(tmp_path, "o", _hex64_plan_ctx(in_dir), in_dir)
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    assert rec["schema"] == "execution-record/v2"
    _, rows = _rows_of(out)
    for obj in OBJS:
        r = rec["realized"]["by_objective"][obj]
        els = [e for (c, o), rs in rows.items() if o == obj for e in rs]
        assert r["returned"] == len(els)
        assert r["finite"] == sum(1 for e in els if isinstance(e["J"], (int, float)) and math.isfinite(e["J"]))
        assert r["converged"] == sum(1 for e in els if e["converged"] is True)
        assert 0 <= r["finite"] <= r["returned"] and 0 <= r["converged"] <= r["returned"]
    env = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))["run_spec"]["stage3"]["planned_envelope"]
    assert PV.check_execution_record(rec, env) == []
    v = IO.validate_provenance(out)
    assert G81._fails(v) == [] and v["checks"]["실현_재계산"] == "통과", v["fail"]


def test_g84_n4_01_v1_records_are_read_as_written_and_are_not_upgraded_or_mixed():
    """v1 원문 (닫힌 v1 키) 은 그대로 통과 · v1 에 `finite` 를 더하면 거부 · v2 인데 계수가 빠지면 v1 로 내려가지
    않고 거부 · 모르는 schema 거부."""
    p = G81._planned_v4()
    env = p.envelope()
    v1 = G81._record_for(p)
    assert v1["schema"] == "execution-record/v1" and PV.check_execution_record(v1, env) == [], "v1 원문은 그대로"

    def _re(rec):
        rec["record_digest"] = PV.digest({k: v for k, v in rec.items() if k != "record_digest"})
        return rec
    mixed = copy.deepcopy(v1)
    for o in OBJS:
        mixed["realized"]["by_objective"][o]["finite"] = mixed["realized"]["by_objective"][o]["returned"]
    assert PV.check_execution_record(_re(mixed), env), "v1 에 v2 키 — 닫힌 집합 위반"
    v2_missing = copy.deepcopy(v1); v2_missing["schema"] = "execution-record/v2"
    bad = PV.check_execution_record(_re(v2_missing), env)
    assert bad and any("finite" in b or "converged" in b or "키" in b for b in bad), bad
    v2 = copy.deepcopy(v2_missing)
    for o in OBJS:
        r = v2["realized"]["by_objective"][o]; r["finite"] = r["returned"]; r["converged"] = r["returned"]
    assert PV.check_execution_record(_re(v2), env) == [], "완전한 v2 는 통과"
    unknown = copy.deepcopy(v2); unknown["schema"] = "execution-record/v3"
    assert PV.check_execution_record(_re(unknown), env)


def test_g84_n4_02_finite_counts_the_stored_J_and_converged_counts_the_legacy_flag_not_healthy_termination(tmp_path):
    """**합성 NaN / legacy-flag 계수 재대조** — 행의 한 원소를 J=NaN · converged=True 로 · 다른 원소를 converged=False
    로 바꾸고 봉인을 다시 맞춘다 → validator 의 `실현_재계산` 이 record 의 finite/converged 를 행에서 다시 센 값과
    대조해 거부한다. 기록을 맞추면 **그 한 항목**이 통과한다 (전체 validator PASS 가 아니다).

    ★ 85차 G85-C2 — 이 합성 행은 실제 legacy 의 "유한 성공 다음 nonfinite round" 의 반환 모습이 **아니다**. 그 경로는
    이전 best 의 유한 J 를 반환하면서 ok=True · outer=nonfinite 가 공존할 수 있다 (80차 회귀가 다루는 경로). 여기서
    재는 것은 계수 정의 (저장 J 유한 수 · legacy True 수) 뿐이고, 두 계수가 정상 종료 판정이 아니라는 점이다."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = _run(tmp_path, "o", _hex64_plan_ctx(in_dir), in_dir)
    fits, rows = _rows_of(out)
    key = next(k for k in rows if k[1] == OBJS[0] and len(rows[k]) >= 2)
    rows[key][0]["J"] = float("nan"); rows[key][0]["converged"] = True
    rows[key][1]["converged"] = False
    fits["restarts_json"] = [json.dumps(rows[(c, o)]) for c, o in zip(fits["cond_id"], fits["objective"])]
    fits.to_parquet(out / "fits.parquet", index=False)
    G82._reseal_fits(out)
    v = IO.validate_provenance(out)
    assert "실현_재계산" in v["fail"] and ("finite" in v["checks"]["실현_재계산"] or "converged" in v["checks"]["실현_재계산"]
                                        or "by_objective" in v["checks"]["실현_재계산"]), v["checks"].get("실현_재계산")
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    r = rec["realized"]["by_objective"][OBJS[0]]
    els = [e for (c, o), rs in rows.items() if o == OBJS[0] for e in rs]
    r["finite"] = sum(1 for e in els if isinstance(e["J"], (int, float)) and math.isfinite(e["J"]))
    r["converged"] = sum(1 for e in els if e["converged"] is True)
    rec["record_digest"] = PV.digest({k: v for k, v in rec.items() if k != "record_digest"})
    (out / "execution_record.json").write_bytes(PV.canonical_bytes(rec))
    v = IO.validate_provenance(out)
    assert v["checks"]["실현_재계산"] == "통과", v["checks"]["실현_재계산"]
    assert r["finite"] == r["returned"] - 1 and r["converged"] == r["returned"] - 1


def test_g84_n4_03_type_and_bound_forgeries_of_the_new_counts_are_refused():
    """`finite` 가 문자열 · 음수 · returned 초과 → 거부 (0/False 로 바꿔 통과시키지 않는다)."""
    p = G81._planned_v4(); env = p.envelope()
    base = G81._record_for(p); base["schema"] = "execution-record/v2"
    for o in OBJS:
        r = base["realized"]["by_objective"][o]; r["finite"] = r["returned"]; r["converged"] = 0
    base["record_digest"] = PV.digest({k: v for k, v in base.items() if k != "record_digest"})
    assert PV.check_execution_record(base, env) == []
    for mut in (lambda r: r.update(finite=str(r["returned"])), lambda r: r.update(finite=-1),
                lambda r: r.update(finite=r["returned"] + 1), lambda r: r.update(converged=None),
                lambda r: r.update(converged=r["returned"] + 5)):
        bad = copy.deepcopy(base); mut(bad["realized"]["by_objective"][OBJS[0]])
        bad["record_digest"] = PV.digest({k: v for k, v in bad.items() if k != "record_digest"})
        assert PV.check_execution_record(bad, env), "위조가 통과했다"


def test_g84_n4_04_realized_from_fits_dispatches_on_schema_and_keeps_v1_shape(tmp_path):
    """공통 재계산 함수는 schema 로 분기한다 — v1 요청은 v1 키만 (새 계수 소급 없음)."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = _run(tmp_path, "o", _hex64_plan_ctx(in_dir), in_dir)
    fits = pd.read_parquet(out / "fits.parquet")
    env = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))["run_spec"]["stage3"]["planned_envelope"]
    v1 = IO.realized_from_fits(fits, planned_env=env, objective_order=OBJS, schema="execution-record/v1")
    v2 = IO.realized_from_fits(fits, planned_env=env, objective_order=OBJS, schema="execution-record/v2")
    assert set(v1["by_objective"][OBJS[0]]) == set(PV._REALIZED_OBJ_KEYS)
    assert set(v2["by_objective"][OBJS[0]]) == set(PV._REALIZED_OBJ_KEYS) | {"finite", "converged"}
    with pytest.raises(ValueError):
        IO.realized_from_fits(fits, planned_env=env, objective_order=OBJS, schema="execution-record/v9")


# ═════════════════════════════════════════════════════════════════════════════
# R2-e — dead 정의 삭제
# ═════════════════════════════════════════════════════════════════════════════
def test_g84_e_00_one_normalize_restart_record_definition_and_the_historical_reader_is_unchanged():
    src = inspect.getsource(F)
    assert src.count("def normalize_restart_record(") == 1, "dead 정의가 남아 있다"
    assert "noqa: F811" not in src.split("def normalize_restart_record(")[1].split("\n")[0]
    pair = F.normalize_restart_record([[1.0, 0.0, 1.0, 0.0], 0.5])
    legacy = F.normalize_restart_record({"p": [1, 0, 1, 0], "J": 0.5, "i": 0, "source": "base_init", "warm": False})
    prep = F.normalize_restart_record({"p": [1, 0, 1, 0], "J": 0.5, "i": 0, "source": "base_init", "warm": False,
                                       "converged": True, "n_eval": 3, "termination_status": "no_improvement"})
    assert (pair["record_generation"], legacy["record_generation"], prep["record_generation"]) == \
        ("legacy_pair", "legacy_dict", "v6_prep_logging")
    assert pair["converged"] is None and legacy["converged"] is None and prep["converged"] is True
