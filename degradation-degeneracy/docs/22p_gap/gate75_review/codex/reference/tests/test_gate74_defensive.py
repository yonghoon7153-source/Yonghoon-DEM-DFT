"""74차 회신 (원장 §102) — 세 결함을 **RED 먼저** 닫는다.

  G74-1  null 캐시 계획은 첫 시작이 캐시를 저장하는 순간 재개가 성립하지 않는다.
         → **고정 캐시 SHA(hex64) 계획만** 진입을 허용한다. 계획 도구(`plan_leg.py`)와
           실제 진입(`assert_planned_leg` — precheck·발급·finalize 가 전부 지난다)이
           **같은 검사**를 한다. live 축을 claim 값으로 덮어 비교를 없애지 않는다.
  G74-3  E9 의 실행 명부와 투영 계약이 충돌한다 (완료된 prospective 다리가 cohort `legs`
         에 들어가면 투영·주장 lint 가 그 다리의 투영을 요구한다).
         → 실행 이력(`executed_legs`)과 투영 membership(`legs`)을 **분리**하고, 다리마다
           `claim_scope ∈ {active_claims, no_active_claim}` 을 **명시**한다 (누락·모름·모순 =
           거부). `no_active_claim` 은 claim_roles 를 가질 수 없고 투영 명부에 있을 수 없으며
           full_bundle 증거 계약은 그대로 진다. 생산(plan → finalize)과 소비(planned_index ·
           row_projection · docs-lint)가 **같은 분류**를 읽는다. 리뷰어의 여섯 회귀 경계.
  G74-4  `archive_results.sh <run>` 이 `artifact_index.yaml` 을 그 묶음만으로 덮어써 v4
         네 항목을 지웠다. → 기존 index 를 **먼저** 읽어(불명확하면 중지) 검증된 entry 만
         병합하고, 같은 이름·다른 identity 는 명시적 거부, 실패 시 index 불변, 원자 교체.

fixture 규칙 (CLAUDE.md 작업 규율 2): 새 시험이 처음부터 통과하면 fixture 가 진실을 가린
것이다. 이 파일은 패치 전 전부 RED 여야 한다.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import tools.preserve as P                                      # noqa: E402
from tests import test_docs_lint as DL                          # noqa: E402

HEX64 = "ab" * 32
SRC = "0123456789abcdef"
_PIN = {"schema_version": 3, "compute_sha256": "a" * 16, "row_projection_py_sha256": "b" * 16,
        "src_scoring_py_sha256": "c" * 16, "analysis_spec_sha256": "d" * 16,
        "producer_semantic_sha256": "e" * 16}


# ─────────────────────────────────────────────────────────────────────────────
# fixtures — 시험 원장 (production 함수로 digest 를 만든다 — 손으로 적지 않는다)
# ─────────────────────────────────────────────────────────────────────────────
def _spec(cache, *, with_grid: bool = True) -> dict:
    spec = {"leg_id": "L", "leg_spec_version": 2,
            "fit": {"objective_order": ["pocv"], "out": "results/L"}}
    if with_grid:
        spec["grid"] = {"config_digest": "c" * 16, "condition_ids_sha256": "d" * 16,
                        "n_conditions": 3, "discharged_cache_sha256": cache, "out": "results/L"}
    return spec


def _ledger(tmp_path: Path, *, cache=HEX64, plan_scope="no_active_claim",
            with_grid: bool = True) -> Path:
    spec = _spec(cache, with_grid=with_grid)
    plan = {"leg_id": "L", "cohort_id": "gA", "status": "planned",
            "authorization_kind": "prospective", "authorized_source_digest": SRC,
            "run_spec_digest": P.run_spec_digest(spec), "run_spec": spec,
            "recorded_on": "2026-09-27", "근거": "74차 시험"}
    if plan_scope is not None:
        plan["claim_scope"] = plan_scope
    doc = {"schema_version": 4,
           "cohorts": [{"cohort_id": "gA", "dir": "docs/22p_gap/coh", "status": "active",
                        "legs": [], "prospective_legs": ["L"],
                        "cross_leg_comparison": "allowed_within_cohort", "pin": _PIN}],
           "planned": [plan], "legs": []}
    p = tmp_path / "LEG_PRESERVATION.yaml"
    p.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


def _live():
    return DL._live_contract()


def _leg(reg: dict, lid: str) -> dict:
    return next(e for e in reg["legs"] if e["leg_id"] == lid)


def _cohort(reg: dict, cid: str) -> dict:
    return next(c for c in reg["cohorts"] if c["cohort_id"] == cid)


def _write(tmp_path: Path, doc: dict) -> Path:
    p = tmp_path / "LEG_PRESERVATION.yaml"
    p.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


# ─────────────────────────────────────────────────────────────────────────────
# G74-1 — 고정 캐시 SHA 계획만 진입한다 (계획 도구 = 실제 진입)
# ─────────────────────────────────────────────────────────────────────────────
def test_g74_1_01_a_null_cache_plan_is_refused_at_entry(tmp_path):
    """null 은 "이 실행이 계산한다" 였고, 그 계산이 캐시를 저장해 재개를 깬다 (§99·§102)."""
    led = _ledger(tmp_path, cache=None)
    with pytest.raises(P.PreserveError) as ei:
        P.assert_planned_leg("L", SRC, ledger=led)
    assert "discharged_cache_sha256" in str(ei.value) and "캐시" in str(ei.value), str(ei.value)


@pytest.mark.parametrize("bad", ["", "ab" * 8, "zz" * 32, 17, HEX64.upper()])
def test_g74_1_02_a_cache_sha_that_is_not_lowercase_hex64_is_refused(tmp_path, bad):
    led = _ledger(tmp_path, cache=bad)
    with pytest.raises(P.PreserveError) as ei:
        P.assert_planned_leg("L", SRC, ledger=led)
    assert "discharged_cache_sha256" in str(ei.value), str(ei.value)


def test_g74_1_03_a_plan_without_a_grid_axis_is_refused(tmp_path):
    """축 자체가 없으면 "고정했다" 고 말할 수 없다 — 부재는 null 과 같다."""
    led = _ledger(tmp_path, with_grid=False)
    with pytest.raises(P.PreserveError) as ei:
        P.assert_planned_leg("L", SRC, ledger=led)
    assert "discharged_cache_sha256" in str(ei.value), str(ei.value)


def test_g74_1_04_a_fixed_cache_sha_plan_passes_entry_and_issues(tmp_path):
    led = _ledger(tmp_path)
    assert P.assert_planned_leg("L", SRC, ledger=led)["leg_id"] == "L"
    c = P.open_leg_run("L", _spec(HEX64), SRC, ledger=led)
    assert c.attempt_id


def test_g74_1_05_precheck_refuses_the_null_plan_before_any_issuance(tmp_path):
    led = _ledger(tmp_path, cache=None)
    with pytest.raises(P.PreserveError):
        P.precheck_leg_run("L", SRC, ledger=led)
    assert not list(tmp_path.rglob("*.claim")), "거부하면서 claim 을 만들었다"


def test_g74_1_06_the_live_axis_is_still_compared_not_overwritten(tmp_path):
    """리뷰어: live 축을 claim 값으로 덮어 비교를 없애는 방식은 받지 않는다."""
    led = _ledger(tmp_path)
    P.open_leg_run("L", _spec(HEX64), SRC, ledger=led)
    other = _spec("cd" * 32)                     # 실행이 다른 캐시 바이트를 보고 있다
    tok = P.read_token_file(P.attempt_path_for("L", ledger=led), "L")
    with pytest.raises(P.PreserveError) as ei:
        P.assert_run_is_authorized("L", "grid", ["results/L"], other, SRC, ledger=led, token=tok)
    assert "run_spec" in str(ei.value), str(ei.value)


def _plan_leg_module():
    spec = importlib.util.spec_from_file_location("plan_leg", REPO / "docs" / "22p_gap" / "plan_leg.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_g74_1_07_plan_leg_refuses_to_emit_a_plan_when_no_cache_exists(monkeypatch, tmp_path):
    """계획 도구가 실제 진입과 **같은** 규칙을 먼저 말한다 — 캐시를 먼저 만들라."""
    import src.grid as G

    monkeypatch.setattr(G, "discharged_cache_path_for", lambda cfg: tmp_path / "no_such_cache.json")
    pl = _plan_leg_module()
    with pytest.raises(SystemExit) as ei:
        pl.build_entry("gate74_probe", "g18_2026_09_15", "configs/grid_fine.yaml",
                       "results/gate74_probe", objective=None, bounds="expanded", n_restarts=None,
                       clean=False, adaptive=True, warm_start=True, reference="grid",
                       halfcell_method="ocp", halfcell_args=[], recorded_on="2026-09-27",
                       근거="74차 시험", claim_scope="no_active_claim")
    assert "캐시" in str(ei.value) and "discharged_cache_sha256" in str(ei.value), str(ei.value)


# ─────────────────────────────────────────────────────────────────────────────
# G74-3 — 진단 전용 분류 계약 (리뷰어의 여섯 회귀)
# ─────────────────────────────────────────────────────────────────────────────
def test_g74_3_01_the_live_ledger_keeps_grid_fit_v5_as_diagnostic_only_outside_the_projection_roster():
    """① 진단 전용 양성 — 실행/영수증 결속 유지 · 투영 membership 아님 · active claim 없음."""
    reg, creg, roles_ok, sealed = _live()
    leg = _leg(reg, "grid_fit_v5")
    assert leg.get("claim_scope") == "no_active_claim", leg.get("claim_scope")
    assert not leg.get("claim_roles")
    assert (leg["preservation_status"], leg["validation_status"]) == ("full_bundle", "current_validated")
    assert leg["evidence"]["out"] == "results/grid_fit_v5"
    g18 = _cohort(reg, "g18_2026_09_15")
    assert g18["legs"] == ["paired_fixed5_v4"], g18["legs"]          # 투영 명부 — 봉인 그대로
    assert g18.get("executed_legs") == ["grid_fit_v5"], g18.get("executed_legs")
    assert g18.get("prospective_legs") == []
    assert DL._scope_problems(reg) == []
    assert DL._no_active_claim_evidence_problems(reg) == []
    assert DL._claim_role_problems(reg, creg, roles_ok, sealed) == []
    assert P.assert_planned_index_consistent()      # production 소비자도 같은 분류를 읽는다


def test_g74_3_02_an_active_claim_reference_on_a_no_active_claim_leg_is_refused():
    """② 같은 자료에 active claim 참조를 붙이면 거부."""
    reg, creg, roles_ok, sealed = _live()
    _leg(reg, "grid_fit_v5")["claim_roles"] = [
        {"claim_id": "P22_NOWARM_PRIMARY", "inference_role": "diagnostic"}]
    bad = DL._claim_role_problems(reg, creg, roles_ok, sealed)
    assert any("grid_fit_v5" in b and "no_active_claim" in b for b in bad), bad


def _drop_out(leg):
    del leg["evidence"]["out"]


def _drop_receipt(leg):
    del leg["evidence"]["verification_receipt"]


def _alter_core(leg):
    leg["evidence"]["verification_receipt_core_sha256"] = "0" * 64


def _unvalidated(leg):
    leg["validation_status"] = "unvalidated"


def _pending(leg):
    leg["preservation_status"] = "preservation_pending"


def _validator_drift(leg):
    leg["evidence"]["validator_identity"]["source_digest"] = "ffffffffffffffff"


@pytest.mark.parametrize("mutate", [_drop_out, _drop_receipt, _alter_core, _unvalidated,
                                    _pending, _validator_drift])
def test_g74_3_03_the_full_bundle_evidence_contract_still_binds_a_no_active_claim_leg(mutate):
    """③ out/receipt/hash/필수 상태를 빼거나 바꾸면 거부 — diagnostic 이 면제가 아니다."""
    reg, *_ = _live()
    assert DL._no_active_claim_evidence_problems(reg) == []
    mutate(_leg(reg, "grid_fit_v5"))
    bad = DL._no_active_claim_evidence_problems(reg)
    assert any("grid_fit_v5" in b for b in bad), bad


@pytest.mark.parametrize("scope", [None, "diagnostic", "", 3])
def test_g74_3_04a_a_missing_or_unknown_scope_is_refused_by_lint_and_by_the_gate(tmp_path, scope):
    """④ 분류 누락·알 수 없는 분류 — 소비자(lint)와 생산자(planned_index) 둘 다 거부."""
    reg, *_ = _live()
    leg = _leg(reg, "grid_fit_v5")
    if scope is None:
        del leg["claim_scope"]
    else:
        leg["claim_scope"] = scope
    bad = DL._scope_problems(reg)
    assert any("grid_fit_v5" in b and "claim_scope" in b for b in bad), bad
    with pytest.raises(P.PreserveError) as ei:
        P.planned_index(ledger=_write(tmp_path, reg))
    assert "claim_scope" in str(ei.value), str(ei.value)


def test_g74_3_04b_a_no_active_claim_leg_inside_a_projection_roster_is_a_contradiction(tmp_path):
    reg, *_ = _live()
    g18 = _cohort(reg, "g18_2026_09_15")
    g18["legs"] = sorted(g18["legs"] + ["grid_fit_v5"])
    g18["executed_legs"] = []
    bad = DL._scope_problems(reg)
    assert any("grid_fit_v5" in b and "legs" in b for b in bad), bad
    with pytest.raises(P.PreserveError) as ei:
        P.planned_index(ledger=_write(tmp_path, reg))
    assert "grid_fit_v5" in str(ei.value), str(ei.value)


def test_g74_3_04c_an_active_claims_leg_inside_executed_legs_is_a_contradiction(tmp_path):
    reg, *_ = _live()
    g18 = _cohort(reg, "g18_2026_09_15")
    g18["executed_legs"] = sorted(g18["executed_legs"] + ["paired_fixed5_v4"])
    bad = DL._scope_problems(reg)
    assert any("paired_fixed5_v4" in b and "executed_legs" in b for b in bad), bad
    with pytest.raises(P.PreserveError):
        P.planned_index(ledger=_write(tmp_path, reg))


def test_g74_3_04e_an_executed_legs_name_that_is_not_a_finished_no_active_claim_leg_is_refused(tmp_path):
    """반대 방향 — `executed_legs` 의 이름은 끝난 prospective · no_active_claim 다리여야 한다.
    (계획에 없는 이름은 `legs`/`prospective_legs` 와 겹치지 않으므로 교집합 검사로는 안 잡힌다.)"""
    reg, *_ = _live()
    g18 = _cohort(reg, "g18_2026_09_15")
    g18["executed_legs"] = sorted(g18["executed_legs"] + ["ghost_leg"])
    bad = DL._scope_problems(reg)
    assert any("ghost_leg" in b for b in bad), bad
    with pytest.raises(P.PreserveError) as ei:
        P.planned_index(ledger=_write(tmp_path, reg))
    assert "ghost_leg" in str(ei.value) and "executed_legs" in str(ei.value), str(ei.value)


def test_g74_3_04d_a_plan_and_its_record_disagreeing_on_scope_is_refused(tmp_path):
    reg, *_ = _live()
    plan = next(e for e in reg["planned"] if e["leg_id"] == "grid_fit_v5")
    plan["claim_scope"] = "active_claims"                    # 기록은 no_active_claim
    with pytest.raises(P.PreserveError) as ei:
        P.planned_index(ledger=_write(tmp_path, reg))
    assert "claim_scope" in str(ei.value) and "grid_fit_v5" in str(ei.value), str(ei.value)


def test_g74_3_05_existing_projection_cohorts_and_claim_roles_are_untouched():
    """⑤ 기존 g18/frozen/claim 양성 유지 — 8개 투영 다리는 `active_claims` 이고 claim_roles 그대로."""
    reg, creg, roles_ok, sealed = _live()
    with_roles = [e for e in reg["legs"] if e.get("claim_roles")]
    assert len(with_roles) == 8 and all(e["claim_scope"] == "active_claims" for e in with_roles)
    assert all(e["claim_scope"] in ("active_claims", "no_active_claim") for e in reg["legs"])
    frozen = [c for c in reg["cohorts"] if c.get("status") == "frozen"]
    assert frozen and all(not c.get("executed_legs") for c in frozen)
    assert DL._claim_role_problems(reg, creg, roles_ok, sealed) == []


def _run_both_phases(led: Path):
    c = P.open_leg_run("L", _spec(HEX64), SRC, ledger=led)
    c.phase_done("grid", {"n": 1})
    c.phase_done("fit", {"n": 1})
    return c


def test_g74_3_06a_finalize_routes_a_no_active_claim_plan_into_executed_legs_and_stamps_the_scope(tmp_path):
    """⑥ 생산(finalize)과 소비(planned_index · lint)의 fixture 통합."""
    led = _ledger(tmp_path, plan_scope="no_active_claim")
    c = _run_both_phases(led)
    r = P.finalize_leg("L", {"leg_source_digest": SRC, "cohorts": ["gA"], "out": "results/L"},
                       ledger=led, token=c.token)
    assert r["status"] == "executed"
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    coh = doc["cohorts"][0]
    assert coh["executed_legs"] == ["L"] and coh["legs"] == [] and coh["prospective_legs"] == []
    leg = doc["legs"][0]
    assert leg["claim_scope"] == "no_active_claim" and "claim_roles" not in leg
    assert P.assert_planned_index_consistent(ledger=led)
    assert DL._scope_problems(doc) == []


def test_g74_3_06b_an_active_claims_plan_still_routes_into_the_projection_roster(tmp_path):
    led = _ledger(tmp_path, plan_scope="active_claims")
    c = _run_both_phases(led)
    P.finalize_leg("L", {"leg_source_digest": SRC, "cohorts": ["gA"], "out": "results/L"},
                   ledger=led, token=c.token)
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    coh = doc["cohorts"][0]
    assert coh["legs"] == ["L"] and not coh.get("executed_legs")
    assert doc["legs"][0]["claim_scope"] == "active_claims"
    assert P.assert_planned_index_consistent(ledger=led)


@pytest.mark.parametrize("scope", [None, "diagnostic"])
def test_g74_3_06c_a_plan_without_a_valid_scope_is_refused_at_entry_and_the_ledger_is_unchanged(tmp_path, scope):
    led = _ledger(tmp_path, plan_scope=scope)
    before = led.read_bytes()
    with pytest.raises(P.PreserveError) as ei:
        P.open_leg_run("L", _spec(HEX64), SRC, ledger=led)
    assert "claim_scope" in str(ei.value), str(ei.value)
    assert led.read_bytes() == before and not list(tmp_path.rglob("*.claim"))


def test_g74_3_06d_the_projection_publisher_is_untouched_and_its_seal_does_not_move():
    """`row_projection.py` 는 건드리지 않았다 (원장 §103 결정) — 봉인 필드(`_LEDGER_SEALED`)에
    `executed_legs` 가 없으므로 g18 의 `CURRENT` ledger_seal 은 진단 실행 뒤에도 그대로고, 활성
    cohort 재생성(투영 게시)이 필요 없다. publisher 가 `executed_legs` 를 읽지 않는 것은 결함이
    아니라 분리다: 그 명부의 다리가 투영 명부에 끼는 것은 production `planned_index` 와 lint
    `_scope_problems` 가 막는다 (04b)."""
    spec = importlib.util.spec_from_file_location("row_projection", REPO / "docs" / "22p_gap" / "row_projection.py")
    rp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rp)
    assert "executed_legs" not in rp._LEDGER_AUTHORITY and "executed_legs" not in rp._LEDGER_SEALED
    reg, *_ = _live()
    g18 = _cohort(reg, "g18_2026_09_15")
    rec = rp._ledger_authority(g18)
    assert rec["legs"] == ["paired_fixed5_v4"] and "executed_legs" not in rec
    cur = (REPO / g18["dir"] / "CURRENT").read_text(encoding="utf-8")
    assert rp._ledger_seal(g18) in cur, "진단 실행 뒤 g18 의 CURRENT ledger_seal 이 움직였다"


# ─────────────────────────────────────────────────────────────────────────────
# G74-4 — archive index 병합 보존 (shell wrapper 회귀)
# ─────────────────────────────────────────────────────────────────────────────
_FAKE = {name: {"artifact_kind": "fit",
                "payload_index_sha256": hashlib.sha256(name.encode()).hexdigest(),
                "source_commit": "1" * 40, "run_dir": f"results/{name}",
                "fits_sha256": "f" * 64, "curves_sha256": "c" * 64}
         for name in ("a_v4", "b_v4", "c_v4", "d_v4")}


def _archive_harness(tmp_path):
    if shutil.which("bash") is None:
        pytest.skip("bash 없음 — archive shell 회귀는 POSIX shell 환경에서만")
    from tests.conftest import isolated_tree
    from tests.test_compare import _complete_artifact

    repo = isolated_tree()
    d, _ = _complete_artifact(tmp_path)
    dest = tmp_path / "arch"
    dest.mkdir()

    def run(target=None, extra=None):
        env = {**os.environ, "ARCHIVE_DEST": str(dest), **(extra or {})}
        return subprocess.run(["bash", str(repo / "scripts" / "archive_results.sh"),
                               str(target or d)], cwd=repo, env=env, capture_output=True, text=True)
    return d, dest, run


def _seed(dest: Path, runs: dict) -> bytes:
    p = dest / "artifact_index.yaml"
    p.write_text(yaml.safe_dump({"_주의": "seed", "source_commit": "1" * 40, "runs": runs},
                                allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p.read_bytes()


def _index(dest: Path) -> dict:
    return yaml.safe_load((dest / "artifact_index.yaml").read_text(encoding="utf-8"))


def test_g74_4_01_a_single_run_archive_keeps_every_other_index_entry_byte_for_byte(tmp_path):
    d, dest, run = _archive_harness(tmp_path)
    _seed(dest, _FAKE)
    r = run()
    assert r.returncode == 0, r.stdout + r.stderr
    idx = _index(dest)
    assert set(idx["runs"]) == set(_FAKE) | {"res"}, sorted(idx["runs"])
    for n, ent in _FAKE.items():
        assert idx["runs"][n] == ent, n
    assert idx["runs"]["res"]["payload_index_sha256"] == hashlib.sha256(
        (dest / "res" / "payload_sha256.yaml").read_bytes()).hexdigest()
    assert idx["source_commit"] is None, "묶음마다 계산 commit 이 다르면 최상위는 null (스크립트 자신의 규칙)"


def test_g74_4_02_re_archiving_the_same_run_is_idempotent_for_the_index(tmp_path):
    d, dest, run = _archive_harness(tmp_path)
    _seed(dest, _FAKE)
    assert run().returncode == 0
    first = _index(dest)
    assert set(first["runs"]) == set(_FAKE) | {"res"}       # 첫 호출부터 병합이다
    assert run().returncode == 0
    assert _index(dest) == first


def test_g74_4_03_the_same_name_with_a_different_identity_is_refused_unless_replacement_is_explicit(tmp_path):
    d, dest, run = _archive_harness(tmp_path)
    before = _seed(dest, {**_FAKE, "res": dict(_FAKE["a_v4"], run_dir="results/res",
                                              payload_index_sha256="0" * 64)})
    r = run()
    assert r.returncode != 0, "같은 이름·다른 identity 를 조용히 덮었다"
    assert (dest / "artifact_index.yaml").read_bytes() == before
    assert not (dest / "res").exists(), "index 를 거부하면서 묶음은 승격했다 — 둘이 어긋난다"
    r2 = run(extra={"ARCHIVE_REPLACE": "1"})
    assert r2.returncode == 0, r2.stdout + r2.stderr
    idx = _index(dest)
    assert idx["runs"]["res"]["payload_index_sha256"] != "0" * 64
    for n, ent in _FAKE.items():
        assert idx["runs"][n] == ent, n


def test_g74_4_04_a_failed_verification_leaves_the_index_unchanged(tmp_path):
    d, dest, run = _archive_harness(tmp_path)
    before = _seed(dest, _FAKE)
    (d / "manifest.yaml").unlink()
    r = run()
    assert r.returncode != 0
    assert (dest / "artifact_index.yaml").read_bytes() == before


@pytest.mark.parametrize("body", ["runs: 5\n", "- not\n- a\n- mapping\n", "runs: {res: 3}\n", ":\n  - [\n"])
def test_g74_4_05_a_malformed_existing_index_stops_before_any_promotion(tmp_path, body):
    d, dest, run = _archive_harness(tmp_path)
    (dest / "artifact_index.yaml").write_text(body, encoding="utf-8")
    before = (dest / "artifact_index.yaml").read_bytes()
    r = run()
    assert r.returncode != 0, r.stdout + r.stderr
    assert (dest / "artifact_index.yaml").read_bytes() == before
    assert not (dest / "res").exists(), "index 가 불명확한데 묶음을 승격했다"
