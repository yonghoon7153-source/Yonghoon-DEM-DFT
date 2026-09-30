"""81차 — 단계 3 한정 구현 라운드 1 (G81-N1·N2·N3 반영 · 사용자 비준 2026-09-28 · 원장 §114).

고정 표: `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` (§1 표 A planned↔realized · §2 표 B 세대 dispatch · §3 표 C provider
결속 · §4 bank). 이 파일은 그 표를 시험으로 옮긴 것이다.

RED 규칙 (리뷰 §7-4): **새 기능**은 현행 코드에서 실패해야 한다 (대개 AttributeError — 함수가 없다). 기존
호환/정상 대조군(legacy fit 골든 · g79_06 prep 보존 · 골든 31)은 처음부터 GREEN 이어도 정상이며 그것을 억지로 RED
로 만들지 않는다. 각 시험 docstring 의 첫 줄이 "왜 실패해야 하는가" 다.

범위 밖 (여기서 시험하지 않는다): 실제 v6 연구 leg · provider canary · floor · pilot · p_ini stage 구현 · adaptive
diagnostic arm · row_projection.py · 골든 재생성.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from src import fitting as F                                        # noqa: E402
from src import io as IO                                            # noqa: E402
from tools import design_wire as DW                                 # noqa: E402
from tools import preserve as PV                                    # noqa: E402

# ─────────────────────────────────────────────────────────────────────────────
# 공통 fixture 재료
# ─────────────────────────────────────────────────────────────────────────────
#: ★ 82차 전 자체 점검 F11 — 설계의 parameter_order 는 **optimizer 벡터** 순서다 (bounds·bank n_params·solution map 열과
#:   같은 것). 라운드 1 fixture 는 5 개 좌표 이름(lli·lam_pe·lam_ne·p_ini_scale·shift)을 썼고, 그 이름이 fits 의
#:   **truth 열**과 겹쳐 solution map 이 해 대신 truth 를 읽을 수 있다는 것을 가렸다.
ORDER = list(F.PARAM_NAMES)
OBJS = ["pocv_dvdq", "pocv_dvdq_dqdv"]
LB = np.array([0.5, -1.0, 0.5, -1.0])
UB = np.array([2.0, 1.0, 2.0, 1.0])
INIT = np.array([1.0, 0.0, 1.0, 0.0])
COORDS = {"lli": "0.17", "lam_pe": "0.13", "lam_ne": "0.13",
          "lam_pe_type": "capacity", "lam_ne_type": "capacity"}
COORDS2 = {"lli": "0", "lam_pe": "0", "lam_ne": "0",
           "lam_pe_type": "capacity", "lam_ne_type": "capacity"}
HEX64 = "a" * 64
#: validate_provenance 의 dirty-tree 검사 — 개발 중(미커밋 RUN_SCOPE)에는 떨어지지만 clean 커밋의 전체 회귀에서는 통과한다
_DIRTY_TREE_CHECKS = {"clean_worktree", "코드_identity"}


def _design(arms=("G_A", "G_C")) -> dict:
    return DW.canonical_design_spec(
        label="p22_grid_primary_v6", arms=list(arms), parameter_order=ORDER,
        bounds_policy="exact_ordered_bounds_digest", objective_plan=OBJS,
        bank_generator="pcg64", bank_version="v6.0",
        seed_derivation="H(pair_group_id, bank_version)", dtype="float64",
        endian="little", coordinate_unit="fraction")


def _pair_group(design=None, coords=COORDS) -> str:
    design = design or _design()
    pos = DW.parameter_order_sha256(design["parameter_order"])
    return DW.pair_group_id(DW.pairing_design_sha256(design), coords, pos)


def _obj(p):
    p = np.asarray(p, float)
    return float((p[0] - 1.3) ** 2 + 10 * (p[1] - 0.2) ** 2 + (p[2] - 0.9) ** 4
                 + np.sin(3 * p[0]) * 0.1 + (p[3] + 0.1) ** 2)


def _roster_entries(design=None, n=2, seeds=(1, 2)):
    """같은 물리좌표 · 다른 noise 실현 두 개 — pair_group 은 같고 obs_key 는 다르다."""
    design = design or _design()
    pg = _pair_group(design)
    out = []
    for k, s in enumerate(seeds[:n]):
        out.append({"obs_key": DW.obs_key(comparison_family_id="p22_grid_primary_v6",
                                          pair_group_id=pg, treatment_id="none",
                                          noise_level="0.001", noise_realization_id=str(s),
                                          replicate_id=0),
                    "cond_id": f"cond{k:02d}", "pair_group_id": pg})
    return out


def _stages(mode="legacy_slot_replace", budget=3, arm="G_A", warm_map=None, budgets=None):
    return [{"stage": "condition", "arm": arm,
             "budget_by_objective": dict(budgets) if budgets is not None else {o: budget for o in OBJS},
             "candidate_mode": mode,
             "warm_provider_map": warm_map if warm_map is not None
             else {o: None for o in OBJS}}]


def _planned_v4(tmp=None, *, design=None, roster=None, stages=None, edges=None,
                source_digest="deadbeefcafe0001", bank_length=8, **over):
    design = design or _design()
    roster = roster if roster is not None else _roster_entries(design)
    stages = stages or _stages()
    kw = dict(
        leg_id="g22p_v6_armGA_b3", protocol_generation="v6",
        pairing_design_sha256=DW.pairing_design_sha256(design),
        parameter_order_sha256=DW.parameter_order_sha256(design["parameter_order"]),
        source_digest=source_digest, objective_order=list(OBJS), stages=stages,
        planned_counts=DW.planned_counts(stages[0]["candidate_mode"],
                                         stages[0]["budget_by_objective"],
                                         stages[0]["warm_provider_map"]),
        bank={"generator": "pcg64", "version": "v6.0", "length": bank_length,
              "n_params": 4, "exact_bounds_sha256": DW.exact_bounds_sha256(LB, UB)},
        inputs={"reference": "grid", "curves_sha256": HEX64, "base_config_digest": HEX64},
        provider_edges=edges or [],
        roster={"roster_sha256": DW.roster_sha256(roster), "n_obs": len(roster),
                "comparison_family_id": "p22_grid_primary_v6", "treatment_id": "none",
                "replicate_id": 0},
        design_label="p22_grid_primary_v6")
    kw.update(over)
    return PV.PlannedLegV4(**kw)


def _record_for(planned, *, realized=None, candidate_entries=None):
    """planned 와 정합하는 최소 execution record."""
    env = planned.envelope()
    pc = env["planned_counts"]
    n = env["roster"]["n_obs"]                       # 실현 count 는 조건 × 후보의 합, 계획 count 는 조건당
    by_obj = realized or {
        o: {"attempted": sum(pc[o].values()) * n, "returned": sum(pc[o].values()) * n, "failed": 0,
            "not_attempted": 0,
            "counts_by_source": {k: v * n for k, v in pc[o].items()},
            "random_bank_prefix_len": pc[o]["random"]} for o in OBJS}
    entries = candidate_entries if candidate_entries is not None else []
    rec = {"schema": "execution-record/v1", "leg_id": env["leg_id"],
           "planned_id": planned.planned_id(), "source_digest": env["source_digest"],
           "protocol_generation": env["protocol_generation"],
           "realized": {"by_objective": by_obj,
                        "candidate_map_sha256": PV.digest(entries),
                        "n_candidates": len(entries),
                        "roster_observed_sha256": env["roster"]["roster_sha256"],
                        "n_obs_observed": env["roster"]["n_obs"],
                        "provider_consumed": []}}
    rec["record_digest"] = PV.digest(rec)
    return rec


# ═════════════════════════════════════════════════════════════════════════════
# §4 bank — Q1 포함 (RED)
# ═════════════════════════════════════════════════════════════════════════════
def test_g81_b01_unit_cube_bank_is_deterministic_per_pair_group_and_version():
    """RED: `unit_cube_bank` 가 없다. 같은 (pair_group, version) → 같은 바이트, 다른 version → 다른 바이트."""
    pg = _pair_group()
    a = DW.unit_cube_bank(pg, "v6.0", 8, 4)
    b = DW.unit_cube_bank(pg, "v6.0", 8, 4)
    c = DW.unit_cube_bank(pg, "v6.1", 8, 4)
    assert a.shape == (8, 4) and a.dtype == np.float64
    assert np.array_equal(a, b) and not np.array_equal(a, c)
    assert (a >= 0).all() and (a < 1).all()
    assert DW.unit_cube_bank_sha256(a) == hashlib.sha256(a.astype("<f8", order="C").tobytes()).hexdigest()
    other = DW.unit_cube_bank(_pair_group(coords=COORDS2), "v6.0", 8, 4)
    assert not np.array_equal(a, other), "pair_group 이 다르면 bank 가 달라야 한다 (공유 bank 는 pair group 단위)"


def test_g81_b02_full_bank_identity_does_not_depend_on_consumed_prefix():
    """RED: full-bank sha 는 B(prefix 길이)와 무관해야 한다 — B 마다 재해시하면 공통 후보의 ID 가 바뀐다."""
    pg = _pair_group()
    bank = DW.unit_cube_bank(pg, "v6.0", 8, 4)
    sha_full = DW.unit_cube_bank_sha256(bank)
    plan3 = DW.candidate_plan("legacy_slot_replace", 3, False)
    plan5 = DW.candidate_plan("legacy_slot_replace", 5, False)
    assert [s for s, _ in plan3] == ["base_init", "random", "random"]
    assert [i for _, i in plan5] == [None, 0, 1, 2, 3]
    # 두 계획이 같은 bank_id 를 갖는다 — prefix 길이는 실현 기록에만
    bid3 = DW.bank_id(pg, "v6.0", sha_full)
    bid5 = DW.bank_id(pg, "v6.0", sha_full)
    assert bid3 == bid5
    # row 바이트 sha 는 행마다 다르고, prefix 안의 행은 같은 값이다
    r0 = DW.unit_cube_bytes_sha256(bank[0]); r1 = DW.unit_cube_bytes_sha256(bank[1])
    assert r0 != r1 and r0 == hashlib.sha256(bank[0].astype("<f8").tobytes()).hexdigest()


def test_g81_b03_exact_bounds_sha_is_the_real_ordered_lb_ub_bytes_and_mapping_is_lb_plus_u_range():
    """RED: `exact_bounds_sha256` · `map_unit_to_bounds` · `x0_sha256` 이 없다. 값은 실제 바이트에서 나온다."""
    s = DW.exact_bounds_sha256(LB, UB)
    assert s == hashlib.sha256(b"exact-bounds/v1" + LB.astype("<f8").tobytes()
                               + UB.astype("<f8").tobytes()).hexdigest()
    assert DW.exact_bounds_sha256(LB, UB * 1.5) != s
    u = np.array([0.0, 0.5, 1.0, 0.25])
    x0 = DW.map_unit_to_bounds(u, LB, UB)
    assert np.allclose(x0, LB + u * (UB - LB)) and x0.dtype == np.float64
    assert DW.x0_sha256(x0) == hashlib.sha256(np.asarray(x0, "<f8").tobytes()).hexdigest()


def test_g81_b04_random_candidate_id_uses_the_real_row_bytes_not_a_placeholder():
    """RED: 실물 row 바이트로 만든 candidate_id 가 골든의 placeholder(`4`*64) 와 다르고, 행마다 다르다."""
    design = _design(); pg = _pair_group(design)
    bank = DW.unit_cube_bank(pg, "v6.0", 8, 4)
    bsha = DW.unit_cube_bank_sha256(bank)
    ids = [DW.candidate_id(DW.exact_bounds_sha256(LB, UB), "random",
                           {"bank_index": i, "unit_cube_bytes_sha256": DW.unit_cube_bytes_sha256(bank[i])},
                           design=design, coords=COORDS, unit_cube_bank_sha256=bsha) for i in range(3)]
    assert len(set(ids)) == 3
    placeholder = DW.candidate_id(DW.exact_bounds_sha256(LB, UB), "random",
                                  {"bank_index": 0, "unit_cube_bytes_sha256": "4" * 64},
                                  design=design, coords=COORDS, unit_cube_bank_sha256=bsha)
    assert placeholder != ids[0]


@pytest.mark.parametrize("mode,budget,has_provider,want", [
    ("legacy_slot_replace", 3, False, ["base_init", "random", "random"]),
    ("legacy_slot_replace", 3, True, ["warm", "random", "random"]),
    ("equal_start_count_base_retained", 3, True, ["base_init", "warm", "random"]),
    ("union", 3, True, ["base_init", "warm", "random", "random"]),
    ("equal_start_count_base_retained", 3, False, ["base_init", "random", "random"]),
])
def test_g81_b05_candidate_plan_follows_contract_section3(mode, budget, has_provider, want):
    """RED: `candidate_plan` 이 없다. 계약 §3 표의 다섯 배열 · random index 는 0.. 순서."""
    plan = DW.candidate_plan(mode, budget, has_provider)
    assert [s for s, _ in plan] == want
    idx = [i for s, i in plan if s == "random"]
    assert idx == list(range(len(idx)))
    assert all(i is None for s, i in plan if s != "random")


@pytest.mark.parametrize("mode,budget,has_provider", [
    ("equal_start_count_base_retained", 1, True),   # B<2
    ("legacy_slot_replace", 0, False),               # B<1
    ("random_only", 3, False),                       # 계약에 없는 mode
])
def test_g81_b06_candidate_plan_rejects_invalid_budget_or_unknown_mode(mode, budget, has_provider):
    """RED: 지원하지 않는 mode/B 는 legacy 로 조용히 대체하지 않고 거부한다."""
    with pytest.raises((DW.WireError, ValueError)):
        DW.candidate_plan(mode, budget, has_provider)


def test_g81_b07_planned_counts_are_derived_from_mode_budget_and_provider_presence():
    """RED: `planned_counts` 가 없다. 계획값은 유도값이다 — 실행 결과가 아니다."""
    pc = DW.planned_counts("legacy_slot_replace", {o: 3 for o in OBJS}, {OBJS[0]: None, OBJS[1]: OBJS[0]})
    assert pc[OBJS[0]] == {"base_init": 1, "warm": 0, "random": 2}
    assert pc[OBJS[1]] == {"base_init": 0, "warm": 1, "random": 2}


# ═════════════════════════════════════════════════════════════════════════════
# §1 표 A — planned ↔ realized (G81-N1)  (RED)
# ═════════════════════════════════════════════════════════════════════════════
def test_g81_n1_01_planned_leg_v4_envelope_is_closed_and_carries_no_realized_values():
    """RED: `PlannedLegV4` 가 없다. envelope 는 planned-leg/v4 · 닫힌 키 · 실현 count 키 없음."""
    p = _planned_v4()
    env = p.envelope()
    assert env["schema"] == "planned-leg/v4"
    assert set(env) == PV._ENVELOPE_KEYS_V4
    assert "realized" not in json.dumps(env) and "returned" not in json.dumps(env)
    assert PV.check_envelope_v4(env) == []
    assert PV.check_planned_envelope(env) == []
    assert p.planned_id() == PV.digest(env)
    # v3 는 그대로 — 분기가 옛 검사를 넓히지 않는다
    v3 = PV.PlannedLeg(leg_id="x", protocol_generation="v6", pairing_design_sha256=HEX64,
                       source_digest="deadbeefcafe0001", objectives=tuple(sorted(OBJS)),
                       total_start_budget=3, candidate_mode="legacy_slot_replace")
    assert PV.check_planned_envelope(v3.envelope()) == [] and PV.check_envelope(v3.envelope()) == []
    assert PV.check_planned_envelope({"schema": "planned-leg/v9"}), "모르는 schema 는 거부"


def test_g81_n1_02_planned_id_is_invariant_to_realized_counts_and_v3_validator_rejects_v4_keys():
    """RED: 실현값을 넣을 자리가 envelope 에 없다 — planned_id 는 실행 결과와 무관. v3 검사에 v4 를 넣으면 거부."""
    p = _planned_v4()
    before = p.planned_id()
    rec_a = _record_for(p)
    n = p.envelope()["roster"]["n_obs"]; per = sum(p.envelope()["planned_counts"][OBJS[0]].values())
    short = {o: {"attempted": 2, "returned": 2, "failed": 0, "not_attempted": per * n - 2,
                 "counts_by_source": {"base_init": 1, "warm": 0, "random": 1},
                 "random_bank_prefix_len": 1} for o in OBJS}
    rec_b = _record_for(p, realized=short)
    assert rec_a["planned_id"] == rec_b["planned_id"] == before
    assert PV.check_execution_record(rec_a, p.envelope()) == []
    assert PV.check_execution_record(rec_b, p.envelope()) == [], "계획 동일 · 실현 count 상이는 정상 record 다"
    assert PV.check_envelope(p.envelope()), "v3 validator 는 v4 envelope 를 받지 않는다"


def test_g81_n1_03_execution_record_of_another_plan_or_inconsistent_counts_is_rejected():
    """RED: `check_execution_record` 가 없다. 다른 planned_id · attempted≠returned+failed · planned 초과 · source 초과 거부."""
    p = _planned_v4(); q = _planned_v4(leg_id="other_leg")
    good = _record_for(p)
    assert PV.check_execution_record(good, p.envelope()) == []
    assert PV.check_execution_record(good, q.envelope()), "다른 계획의 receipt 혼입"
    # 같은 leg · 다른 계획 (bank 길이만 다르다 — leg_id·count·digest 는 전부 같다). 변이 재생에서 `other_leg` 는
    #   leg_id 대조가 먼저 걸려 planned_id 참조 대조를 가렸다 (실측: 변이 rc 0). 이 자리만이 잡는 반례.
    p2 = _planned_v4(bank_length=16)
    assert p2.leg_id == p.leg_id and p2.planned_id() != p.planned_id()
    probs = PV.check_execution_record(_record_for(p2), p.envelope())
    assert any("다른 계획의 기록" in b for b in probs), f"같은 leg 의 다른 계획 기록이 통과했다: {probs}"
    bad = copy.deepcopy(good); bad["realized"]["by_objective"][OBJS[0]]["failed"] = 1
    assert PV.check_execution_record(bad, p.envelope()), "attempted ≠ returned + failed"
    bad = copy.deepcopy(good); bad["realized"]["by_objective"][OBJS[0]]["attempted"] = 9
    bad["realized"]["by_objective"][OBJS[0]]["returned"] = 9
    assert PV.check_execution_record(bad, p.envelope()), "계획 예산 초과"
    bad = copy.deepcopy(good); bad["realized"]["by_objective"][OBJS[0]]["counts_by_source"]["warm"] = 1
    assert PV.check_execution_record(bad, p.envelope()), "no-provider 계획에 warm 실현"
    bad = copy.deepcopy(good); bad["realized"]["n_obs_observed"] = 99
    assert PV.check_execution_record(bad, p.envelope()), "roster 보다 많은 관측"
    bad = copy.deepcopy(good); bad["source_digest"] = "0000000000000000"
    assert PV.check_execution_record(bad, p.envelope()), "code identity 불일치"
    bad = copy.deepcopy(good); bad["extra"] = 1
    assert PV.check_execution_record(bad, p.envelope()), "닫힌 키"


def test_g81_n1_06_planned_counts_are_derived_and_a_hand_edited_count_is_refused():
    """RED: 계획 count 는 mode·B·provider 에서 유도한 값과 같아야 한다 — 손으로 고친(또는 실현값을 넣은) 계획은 봉인되지 않는다."""
    good = _planned_v4()
    pc = copy.deepcopy(good.envelope()["planned_counts"])
    pc[OBJS[0]]["random"] += 1                                  # "실현값" 을 계획 자리에 넣은 꼴
    with pytest.raises(PV.PreserveError, match="planned_counts"):
        _planned_v4(planned_counts=pc)
    env = good.envelope(); env["planned_counts"] = pc
    assert any("planned_counts" in m for m in PV.check_envelope_v4(env))


def test_g81_n1_04_roster_rejects_duplicate_obs_key_cross_seed_and_cond_id_collision():
    """RED: `check_roster`/`roster_sha256`/`obs_key` 가 없다. 같은 pair group 의 두 noise 실현은 정상, 중복/충돌은 거부."""
    good = _roster_entries()
    assert PV.digest(good) == DW.roster_sha256(good) or DW.roster_sha256(good)  # 값은 구현이 정하되 hex64
    assert DW.check_roster(good) == []
    assert len({e["obs_key"]["noise_realization_id"] for e in good}) == 2
    dup = copy.deepcopy(good); dup[1]["obs_key"] = dict(dup[0]["obs_key"])
    assert DW.check_roster(dup), "obs_key 중복"
    col = copy.deepcopy(good); col[1]["cond_id"] = col[0]["cond_id"]
    assert DW.check_roster(col), "cond_id 충돌 (교차 seed pairing)"
    objk = copy.deepcopy(good); objk[0]["obs_key"]["objective"] = OBJS[0]
    assert DW.check_roster(objk), "objective 는 key 의 값이 아니다"
    with pytest.raises((DW.WireError, TypeError)):
        DW.obs_key(comparison_family_id="f", pair_group_id="not-hex", treatment_id="none",
                   noise_level="0.001", noise_realization_id="1", replicate_id=0)


def test_g81_n1_05_run_transaction_with_a_v4_plan_requires_a_consistent_execution_record(tmp_path):
    """RED: v4 계획으로 트랜잭션을 돌리면 `execution_record.json` 이 없거나 다른 계획이면 planned_seal 에서 멈춘다."""
    from tests.test_preserve import _hooks, _FITS
    p = _planned_v4()
    run = tmp_path / "run"; (run / "_inputs").mkdir(parents=True)
    (run / "fits.parquet").write_bytes(_FITS)
    (run / "manifest.yaml").write_text("leg: x\n", encoding="utf-8")
    (run / "_inputs" / "base.yaml").write_text("noise: 0.001\n", encoding="utf-8")
    (run / "run_spec.json").write_text(json.dumps({"planned_id": p.planned_id(),
                                                   "source_digest": p.source_digest}), encoding="utf-8")
    backend = PV.CasBackend(root=tmp_path / "cas"); index = tmp_path / "index"
    with pytest.raises(PV.PreserveError) as ei:
        PV.run_transaction(p, run, backend, index, _hooks())
    assert ei.value.stage == "planned_seal" and "execution_record" in str(ei.value)
    (run / "execution_record.json").write_text(json.dumps(_record_for(_planned_v4(leg_id="other_leg"))),
                                               encoding="utf-8")
    with pytest.raises(PV.PreserveError) as ei:
        PV.run_transaction(p, run, backend, index, _hooks())
    assert ei.value.stage == "planned_seal"
    # 같은 leg · 다른 계획의 기록 (bank 길이만 다르다) — leg_id 가 같으니 planned_id 참조 대조만이 멈춘다
    (run / "execution_record.json").write_text(json.dumps(_record_for(_planned_v4(bank_length=16))),
                                               encoding="utf-8")
    with pytest.raises(PV.PreserveError) as ei:
        PV.run_transaction(p, run, backend, index, _hooks())
    assert ei.value.stage == "planned_seal" and "다른 계획의 기록" in str(ei.value), str(ei.value)
    (run / "execution_record.json").write_text(json.dumps(_record_for(p)), encoding="utf-8")
    res = PV.run_transaction(p, run, backend, tmp_path / "index2", _hooks())
    assert res["ok"]
    entry = PV.index_entries(tmp_path / "index2")[p.leg_id]
    assert entry["planned_id"] == p.planned_id()
    assert entry["planned_envelope"]["schema"] == "planned-leg/v4"


# ═════════════════════════════════════════════════════════════════════════════
# §2 표 B — 세대 dispatch (G81-N2)
# ═════════════════════════════════════════════════════════════════════════════
_TERM = {"outer": "no_improvement", "n_rounds": 1,
         "native_last": {"status": 0, "success": True, "message": "ok", "nfev": 12, "nit": 3},
         "native_best": {"status": 0, "success": True, "message": "ok", "nfev": 12, "nit": 3}}
ROW5 = {"p": [1.0, 0.0, 1.0, 0.0], "J": 0.5, "i": 0, "source": "base_init", "warm": False}
ROW8 = {**ROW5, "converged": True, "n_eval": 12, "termination_status": _TERM}
ROW10 = {**ROW8, "candidate_id": "c" * 64, "bank_index": None}
ROW10R = {**ROW8, "source": "random", "i": 1, "candidate_id": "d" * 64, "bank_index": 0}


def test_g81_n2_00_historical_reader_is_unchanged_for_legacy_pair_dict_and_prep_rows():
    """GREEN 대조군 (g79_06 과 같은 축): 선언 없는 역사적 호출은 세 세대를 그대로 낸다."""
    a, b, c = (F.normalize_restart_record(x) for x in ([[1.0, 0.0, 1.0, 0.0], 0.5], ROW5, ROW8))
    assert (a["record_generation"], b["record_generation"], c["record_generation"]) == \
        ("legacy_pair", "legacy_dict", "v6_prep_logging")
    assert c["converged"] is True and c["n_eval"] == 12


def test_g81_n2_01_a_ten_key_row_without_a_declared_v6_context_is_not_accepted_as_v6():
    """RED: 현행 reader 는 10 키 행을 8 키 prep 으로 읽는다 (키 개수 추론). 선언 없으면 `v6_undeclared` 여야 한다."""
    r = F.normalize_restart_record(ROW10)
    assert r["record_generation"] == "v6_undeclared"
    assert r["candidate_id"] == "c" * 64, "값은 보여 준다 — 승인은 하지 않는다"


def test_g81_n2_02_declared_v6_accepts_exactly_ten_keys_and_never_downgrades_a_stripped_row():
    """RED: `declared` 인자가 없다. v6 선언 아래 8 키 행(ID 삭제)은 `mixed_invalid` — prep 으로 내려가지 않는다."""
    ok = F.normalize_restart_record(ROW10R, declared="v6")
    assert ok["record_generation"] == "v6" and ok["bank_index"] == 0 and ok["candidate_id"] == "d" * 64
    stripped = F.normalize_restart_record(ROW8, declared="v6")
    assert stripped["record_generation"] == "mixed_invalid"
    partial = F.normalize_restart_record({**ROW8, "candidate_id": "c" * 64}, declared="v6")
    assert partial["record_generation"] == "mixed_invalid"


def test_g81_n2_03_declared_prep_preserves_logging_values_and_flags_a_ten_key_row_as_conflict():
    """RED: prep 선언 아래 8 키 행은 그대로(로깅 3 값 보존 · ID 미기록 정상), 10 키 행은 선언-행 충돌."""
    r = F.normalize_restart_record(ROW8, declared="v6_prep_logging")
    assert r["record_generation"] == "v6_prep_logging" and r["converged"] is True and r["n_eval"] == 12
    assert r["candidate_id"] is None and r["bank_index"] is None
    assert F.normalize_restart_record(ROW10, declared="v6_prep_logging")["record_generation"] == "mixed_invalid"
    assert F.normalize_restart_record(ROW5, declared="legacy")["record_generation"] == "legacy_dict"
    assert F.normalize_restart_record(ROW8, declared="legacy")["record_generation"] == "mixed_invalid"


def test_g81_n2_04_candidate_mode_name_is_not_a_generation_selector():
    """RED: 같은 mode 이름(`legacy_slot_replace`)의 legacy 행과 v6 행은 선언으로만 갈린다."""
    assert F.normalize_restart_record(ROW10R, declared="v6")["record_generation"] == "v6"
    assert F.normalize_restart_record(ROW5, declared="legacy")["record_generation"] == "legacy_dict"
    with pytest.raises(ValueError):
        F.normalize_restart_record(ROW10R, declared="legacy_slot_replace")   # mode 이름은 declared 값이 아니다


def test_g81_n2_05_v6_restart_validator_requires_all_ten_keys_and_source_consistent_bank_index():
    """RED: `_restart_ok_v6` 가 없다. 8 키 거부 · random 은 index int≥0 · base/warm 은 null · 옛 `_restart_ok` 불변."""
    assert IO._restart_ok_v6(ROW10) is True and IO._restart_ok_v6(ROW10R) is True
    assert IO._restart_ok_v6(ROW8) is False, "v6 에서 ID 를 지운 행"
    assert IO._restart_ok_v6({**ROW10R, "bank_index": None}) is False, "random 인데 index 없음"
    assert IO._restart_ok_v6({**ROW10R, "bank_index": -1}) is False
    assert IO._restart_ok_v6({**ROW10, "bank_index": 0}) is False, "base_init 인데 index 있음"
    assert IO._restart_ok_v6({**ROW10, "candidate_id": "zz"}) is False
    assert IO._restart_ok_v6({**ROW10, "extra": 1}) is False, "닫힌 10 키"
    # 옛 validator 는 그대로 — 넓히지 않는다
    assert IO._restart_ok(ROW5) is True and IO._restart_ok(ROW8) is True


# ═════════════════════════════════════════════════════════════════════════════
# §3 표 C — provider 결속 (G81-N3)  (RED)
# ═════════════════════════════════════════════════════════════════════════════
def _provider_fits(tmp: Path, objective: str, rows: dict[str, list[float]], *, run_spec=None) -> Path:
    """provider **run 디렉터리** (fits.parquet + manifest.yaml) — ★ 82차 전 자체 점검 F5·F11.

    해는 실제 fits 처럼 `PARAM_NAMES` 열(a_pe·b_pe·a_ne·b_ne)에 두고, 같은 행의 truth 열(lli·lam_pe·lam_ne)에는
    **다른 값(0.5)** 을 넣는다 — map 이 truth 를 해로 읽으면 좌표가 틀려 시험이 잡는다. 라운드 1 판은 해를
    truth 열 이름으로 적어 그 구분을 가렸다.
    """
    import yaml
    tmp = Path(tmp); tmp.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([{"cond_id": c, "objective": objective, **dict(zip(F.PARAM_NAMES, p)),
                        "lli": 0.5, "lam_pe": 0.5, "lam_ne": 0.5, "J": 0.1, "converged": True}
                       for c, p in rows.items()])
    df.to_parquet(tmp / "fits.parquet", index=False)
    spec = run_spec if run_spec is not None else {"sig_version": 6, "objective_order": list(OBJS), "note": "provider"}
    (tmp / "manifest.yaml").write_text(yaml.safe_dump({"run_spec": spec}, allow_unicode=True), encoding="utf-8")
    return tmp


def _protocol_sha(run: Path) -> str:
    import yaml
    spec = yaml.safe_load((Path(run) / "manifest.yaml").read_text(encoding="utf-8"))["run_spec"]
    return hashlib.sha256(PV.canonical_bytes(spec)).hexdigest()


def _edge(run: Path, map_path: Path, *, provider=OBJS[0], consumer=OBJS[1]):
    return {"stage": "condition", "arm": "G_C", "consumer_objective": consumer,
            "provider_objective": provider,
            "provider_artifact_sha256": hashlib.sha256((Path(run) / "fits.parquet").read_bytes()).hexdigest(),
            "solution_map_sha256": hashlib.sha256(map_path.read_bytes()).hexdigest(),
            "provider_protocol_sha256": _protocol_sha(run)}


def test_g81_n3_01_solution_map_header_binds_fits_bytes_objective_and_protocol(tmp_path):
    """RED: `make_solution_map` 가 없다. header = objective · fits sha · protocol sha · parameter_order · 제외 목록."""
    run = _provider_fits(tmp_path, OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0], "c2": [1.4, float("nan"), 0.8, 0.1]})
    hdr = F.make_solution_map(run, OBJS[0], tmp_path / "map.json")
    assert hdr["schema"] == "solution-map/v1" and hdr["provider_objective"] == OBJS[0]
    assert hdr["provider_artifact_sha256"] == hashlib.sha256((run / "fits.parquet").read_bytes()).hexdigest()
    assert hdr["provider_protocol_sha256"] == _protocol_sha(run) and hdr["n_entries"] == 1
    assert hdr["parameter_order"] == list(F.PARAM_NAMES)
    assert hdr["excluded_cond_ids"] == ["c2"], "비유한 해는 entries 가 아니라 제외 목록"
    doc = json.loads((tmp_path / "map.json").read_text(encoding="utf-8"))
    assert set(doc["entries"]) == {"c1"} and doc["header"] == hdr
    with pytest.raises(ValueError):
        F.make_solution_map(run, "pocv_dvdq_dqdv", tmp_path / "map2.json")


def test_g81_n3_02_consumer_rejects_wrong_fits_map_combination_and_unsealed_maps(tmp_path):
    """RED: `provider_x0` 가 없다. 세 sha 가 전부 진짜라도 fits A + map B(다른 조건 세트) 결합은 거부."""
    order = list(F.PARAM_NAMES)
    run_a = _provider_fits(tmp_path / "a", OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0]})
    run_b = _provider_fits(tmp_path / "b", OBJS[0], {"c1": [1.9, 0.9, 1.9, 0.9]})
    F.make_solution_map(run_a, OBJS[0], tmp_path / "a" / "map.json")
    F.make_solution_map(run_b, OBJS[0], tmp_path / "b" / "map.json")
    edge_ok = _edge(run_a, tmp_path / "a" / "map.json")
    x0, sha = F.provider_x0(tmp_path / "a" / "map.json", edge=edge_ok, cond_id="c1", lb=LB, ub=UB, parameter_order=order)
    assert np.allclose(x0, [1.2, 0.1, 0.9, 0.0]) and sha == DW.x0_sha256(x0)
    # fits A 의 edge 로 map B 를 소비 — header 의 artifact sha 가 edge 와 다르다
    with pytest.raises(ValueError):
        F.provider_x0(tmp_path / "b" / "map.json", edge=edge_ok, cond_id="c1", lb=LB, ub=UB, parameter_order=order)
    # 봉인 전 소비 — header 는 그대로 두고 **유효한 JSON** 으로 바꾼다 (좌표 하나 · 공백 하나). 바이트 봉인만이
    #   이것을 잡는다. (처음 반례는 마지막 바이트를 뒤집었는데, 그것은 JSONDecodeError(ValueError 의 하위)
    #   로 통과해 봉인 대조 변이를 가렸다 — 실측: 변이 rc 0.)
    doc = json.loads((tmp_path / "a" / "map.json").read_text(encoding="utf-8"))
    doc["entries"]["c1"]["p"] = [1.3, 0.1, 0.9, 0.0]
    (tmp_path / "a" / "tampered.json").write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(ValueError, match="봉인 전 소비"):
        F.provider_x0(tmp_path / "a" / "tampered.json", edge=edge_ok, cond_id="c1", lb=LB, ub=UB, parameter_order=order)
    (tmp_path / "a" / "respaced.json").write_bytes((tmp_path / "a" / "map.json").read_bytes() + b"\n")
    with pytest.raises(ValueError, match="봉인 전 소비"):
        F.provider_x0(tmp_path / "a" / "respaced.json", edge=edge_ok, cond_id="c1", lb=LB, ub=UB, parameter_order=order)


def test_g81_n3_03_consumer_rejects_missing_condition_wrong_objective_and_out_of_bounds_without_clipping(tmp_path):
    """RED: 누락 cond_id 는 오류(no-warm 전환 아님) · objective 불일치 거부 · bounds 밖 p 는 clip 하지 않고 거부."""
    order = list(F.PARAM_NAMES)
    run = _provider_fits(tmp_path, OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0], "c3": [3.5, 0.0, 0.9, 0.0]})
    F.make_solution_map(run, OBJS[0], tmp_path / "map.json")
    edge = _edge(run, tmp_path / "map.json")
    with pytest.raises(ValueError, match="c9"):
        F.provider_x0(tmp_path / "map.json", edge=edge, cond_id="c9", lb=LB, ub=UB, parameter_order=order)
    with pytest.raises(ValueError):
        F.provider_x0(tmp_path / "map.json", edge=dict(edge, provider_objective=OBJS[1]), cond_id="c1",
                      lb=LB, ub=UB, parameter_order=order)
    with pytest.raises(ValueError, match="bounds|경계|밖"):
        F.provider_x0(tmp_path / "map.json", edge=edge, cond_id="c3", lb=LB, ub=UB, parameter_order=order)


def test_g81_n3_04_provider_edges_must_match_the_warm_map_precede_the_consumer_and_not_be_cyclic():
    """RED: `check_provider_edges` 가 없다. self/순환/order 밖/warm map 불일치/warm-off arm 의 edge 거부."""
    e = {"stage": "condition", "arm": "G_C", "consumer_objective": OBJS[1], "provider_objective": OBJS[0],
         "provider_artifact_sha256": HEX64, "solution_map_sha256": HEX64, "provider_protocol_sha256": HEX64}
    wm = {OBJS[0]: None, OBJS[1]: OBJS[0]}
    assert DW.check_provider_edges([e], objective_order=OBJS, warm_provider_map=wm, arm="G_C") == []
    assert DW.check_provider_edges([dict(e, provider_objective=OBJS[1])], objective_order=OBJS, warm_provider_map=wm, arm="G_C"), "self"
    rev = dict(e, consumer_objective=OBJS[0], provider_objective=OBJS[1])
    assert DW.check_provider_edges([rev], objective_order=OBJS, warm_provider_map={OBJS[0]: OBJS[1], OBJS[1]: None}, arm="G_C"), "order 역방향"
    assert DW.check_provider_edges([], objective_order=OBJS, warm_provider_map=wm, arm="G_C"), "map 은 provider 를 말하는데 edge 가 없다"
    assert DW.check_provider_edges([e], objective_order=OBJS, warm_provider_map={o: None for o in OBJS}, arm="G_A"), "warm-off arm 에 edge"
    assert DW.check_provider_edges([dict(e, stage="p_ini")], objective_order=OBJS, warm_provider_map=wm, arm="G_C"), "p_ini stage 는 이번 라운드 명시 거부"
    assert DW.check_provider_edges([], objective_order=OBJS, warm_provider_map={OBJS[0]: None, OBJS[1]: None}, arm="G_C"), \
        "warm arm(G_C) 에서 두 번째 objective 의 provider 가 null — no-warm 으로 전환 금지"


# ═════════════════════════════════════════════════════════════════════════════
# writer — fit(candidates) · _fit_one(stage3) · run_fit(stage3) · validate_provenance sig 6
# ═════════════════════════════════════════════════════════════════════════════
def _candidates(design=None, budget=3, coords=COORDS):
    design = design or _design(); pg = _pair_group(design, coords)
    bank = DW.unit_cube_bank(pg, "v6.0", 8, 4); bsha = DW.unit_cube_bank_sha256(bank)
    eb = DW.exact_bounds_sha256(LB, UB)
    out = []
    for src, idx in DW.candidate_plan("legacy_slot_replace", budget, False):
        if src == "base_init":
            x0 = INIT.copy()
            payload = {"base_coord_sha256": DW.x0_sha256(x0)}
        else:
            x0 = DW.map_unit_to_bounds(bank[idx], LB, UB)
            payload = {"bank_index": idx, "unit_cube_bytes_sha256": DW.unit_cube_bytes_sha256(bank[idx])}
        out.append({"source": src, "x0": x0, "bank_index": idx,
                    "candidate_id": DW.candidate_id(eb, src, payload, design=design, coords=coords,
                                                    unit_cube_bank_sha256=bsha)})
    return out


def test_g81_w01_fit_with_explicit_candidates_writes_ten_key_rows_and_a_candidate_map():
    """RED: `fit(candidates=…)` 인자가 없다. 행 10 키 · candidate_id/bank_index 가 후보와 같다 · x0 결속."""
    cands = _candidates()
    r = F.fit(_obj, INIT, LB, UB, n_restarts=3, seed=7, adaptive=False, candidates=cands)
    assert len(r.restarts) == 3
    for e in r.restarts:
        assert set(e) == {"p", "J", "i", "source", "warm", "converged", "n_eval", "termination_status",
                          "candidate_id", "bank_index"}, sorted(e)
        c = cands[e["i"]]
        assert e["candidate_id"] == c["candidate_id"] and e["bank_index"] == c["bank_index"] and e["source"] == c["source"]
    assert [m["x0_sha256"] for m in r.candidate_map] == [DW.x0_sha256(c["x0"]) for c in cands]
    assert [m["candidate_id"] for m in r.candidate_map] == [c["candidate_id"] for c in cands]


def test_g81_w02_fit_with_candidates_rejects_adaptive_and_out_of_bounds_x0():
    """RED: 새 경로는 adaptive=False 만 · bounds 밖 x0 는 clip 하지 않고 거부 (legacy 의 np.clip 은 legacy 에만)."""
    cands = _candidates()
    with pytest.raises(ValueError):
        F.fit(_obj, INIT, LB, UB, n_restarts=3, seed=7, adaptive=True, candidates=cands)
    bad = copy.deepcopy(cands); bad[0]["x0"] = np.array([9.0, 0.0, 1.0, 0.0])
    with pytest.raises(ValueError):
        F.fit(_obj, INIT, LB, UB, n_restarts=3, seed=7, adaptive=False, candidates=bad)
    dup = copy.deepcopy(cands); dup[2]["bank_index"] = dup[1]["bank_index"]      # 같은 bank 행을 두 번
    with pytest.raises(ValueError, match="중복"):
        F.fit(_obj, INIT, LB, UB, n_restarts=3, seed=7, adaptive=False, candidates=dup)


def test_g81_w03_legacy_fit_is_byte_identical_golden_still_holds():
    """GREEN 대조군: `candidates` 를 주지 않으면 79차 골든이 그대로다 (`test_gate79_stage3_logging.py::g79_02` 와 같은 값)."""
    from tests.test_gate79_stage3_logging import _GOLDEN, _INIT, _LB, _UB, _obj as _obj79
    r = F.fit(_obj79, _INIT, _LB, _UB, n_restarts=3, seed=7, adaptive=False)
    g = _GOLDEN[False]
    assert r.p.tolist() == g["p"] and r.J == g["J"] and r.n_eval == g["n_eval"]
    assert [(e["i"], e["source"]) for e in r.restarts] == [(e["i"], e["source"]) for e in g["restarts"]]
    assert all(set(e) == {"p", "J", "i", "source", "warm", "converged", "n_eval", "termination_status"}
               for e in r.restarts), "legacy 행은 8 키 그대로 — candidate 키가 새지 않는다"


def _v6_context(in_dir: Path, *, design=None, budget=2, arm="G_A", warm_map=None, edges=None, budgets=None,
                provider_runs=None):
    """tiny curves → 조건 → roster → PlannedLegV4 (기본 no-provider · grid 기준; warm arm 은 warm_map·edges·provider_runs)."""
    from src.grid import Condition
    design = design or _design()
    cur = pd.read_parquet(in_dir / "curves.parquet")
    conds = []
    for cid, g in cur.groupby("cond_id", sort=True):
        r0 = g.iloc[0]
        conds.append(Condition(float(r0["lli"]), float(r0["lam_pe"]), float(r0["lam_ne"]),
                               str(r0["lam_pe_type"]), str(r0["lam_ne_type"]), float(r0["noise"]), int(r0["seed"])))
    roster = DW.roster_from_conditions(conds, design=design, comparison_family_id="p22_grid_primary_v6",
                                       treatment_id="none", replicate_id=0)
    stages = _stages(budget=budget, arm=arm, warm_map=warm_map, budgets=budgets)
    planned = _planned_v4(design=design, roster=roster, stages=stages, edges=edges,
                          source_digest=IO.source_digest(),
                          inputs={"reference": "grid",
                                  "curves_sha256": hashlib.sha256((in_dir / "curves.parquet").read_bytes()).hexdigest(),
                                  # ★ 84차 G84-N1 — v6 실행은 base-config closure 를 읽으므로 계획도 그 hex64 를 갖는다
                                  #   (라운드 1 fixture 의 None 은 §11-2 로 거부된다)
                                  "base_config_digest": F.config_closure_sha256("configs/base.yaml")})
    return {"planned": planned, "design": design, "provider_runs": dict(provider_runs or {})}


def test_g81_w04_run_fit_with_stage3_context_writes_sig6_run_spec_execution_record_and_candidate_map(tmp_path):
    """RED: `run_fit(stage3=…)` 인자가 없다. v6 산출 = sig_version 6 + stage3 블록 + 행 10 키 + record/map 파일."""
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in"); out = tmp_path / "o"
    ctx = _v6_context(in_dir)
    F.run_fit(in_dir, out, _obj_cfg_min(), {OBJS[0]: {"w_pocv": 1.0}, OBJS[1]: {"w_pocv": 1.0, "_warm": False}},
              _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False, warm_start=False, stage3=ctx)
    import yaml
    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    spec = man["run_spec"]
    assert spec["sig_version"] == 6
    assert spec["stage3"]["planned_id"] == ctx["planned"].planned_id()
    assert spec["stage3"]["candidate_mode"] == "legacy_slot_replace" and spec["optimizer"]["adaptive"] is False
    assert spec["optimizer"]["seed_scheme"] == "unit_cube_bank/v1"
    fits = pd.read_parquet(out / "fits.parquet")
    assert {"pair_group_id", "bank_id", "record_generation"} <= set(fits.columns)
    assert set(fits["record_generation"]) == {"v6"}
    for rs in fits["restarts_json"]:
        rows = json.loads(rs)
        assert rows and all(IO._restart_ok_v6(e) for e in rows), rows
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    # ★ 84차 G84-N4 — writer 는 v2 를 쓴다 (v1 은 읽기 그대로 · `test_gate84_round2a.py::n4_01`)
    assert rec["schema"] == "execution-record/v2" and rec["planned_id"] == ctx["planned"].planned_id()
    assert PV.check_execution_record(rec, ctx["planned"].envelope()) == []
    cmap = json.loads((out / "candidate_map.json").read_text(encoding="utf-8"))
    assert PV.digest(cmap["entries"]) == rec["realized"]["candidate_map_sha256"]
    ids_rows = {e["candidate_id"] for rs in fits["restarts_json"] for e in json.loads(rs)}
    assert ids_rows == {m["candidate_id"] for m in cmap["entries"]}
    v = IO.validate_provenance(out)
    # 개발 중 dirty tree 에서는 dirty-tree 검사 둘(`clean_worktree` · `코드_identity`)만 떨어질 수 있다 — 이 시험의 축이 아니다
    assert [k for k in v["fail"] if k not in _DIRTY_TREE_CHECKS] == [], v["fail"]
    assert "restart_후보" in v["checks"] and v["checks"]["restart_후보"] == "통과"
    for k in ("stage3_schema", "stage3_planned_envelope", "execution_record", "candidate_map", "candidate_ids_결속"):
        assert v["checks"][k] == "통과", (k, v["checks"][k])


def test_g81_w05_validate_provenance_dispatches_on_sig_version_and_fails_closed(tmp_path):
    """RED: sig 6 인데 stage3 블록이 없으면 실패 · sig 7 은 거부 · sig 5 산출은 기존 검사 그대로 (record 요구 없음)."""
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    import yaml
    in_dir = _tiny_curves(tmp_path / "in"); out = tmp_path / "o"
    F.run_fit(in_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}}, _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False)
    v0 = IO.validate_provenance(out)
    assert [k for k in v0["fail"] if k not in _DIRTY_TREE_CHECKS] == [], "legacy sig 5 산출 — 기존 검사 불변"
    assert "restart_출처" in v0["checks"] and "restart_후보" not in v0["checks"]
    man_p = out / "manifest.yaml"
    man = yaml.safe_load(man_p.read_text(encoding="utf-8"))
    man["run_spec"]["sig_version"] = 6                       # v6 라고 주장하지만 stage3 축이 없다
    man_p.write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
    v = IO.validate_provenance(out)
    assert v["ok"] is False and any("stage3" in v["checks"][k] or "restart_후보" in k for k in v["fail"]), v["fail"]
    man["run_spec"]["sig_version"] = 7
    man_p.write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
    v = IO.validate_provenance(out)
    assert v["ok"] is False and any("sig_version" in k for k in v["fail"]), v["fail"]


def test_g81_w06_stage3_run_refuses_a_roster_that_does_not_match_the_curves_and_p_ini_edges(tmp_path):
    """RED: 계획 roster 와 실제 조건 집합이 다르면 시작하지 않는다 · adaptive=True 는 시작하지 않는다.

    (라운드 1 docstring 은 "warm arm 인데 provider map 이 없으면" 도 적었지만 몸체는 그것을 재지 않았다 — 82차 전 자체
    점검 F6. 그 사례는 `test_g81_s06_*` 가 실제 warm arm 으로 잰다.)
    """
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in"); out = tmp_path / "o"
    ctx = _v6_context(in_dir)
    wrong = _planned_v4(roster=_roster_entries(), stages=_stages(budget=2), source_digest=IO.source_digest(),
                        inputs={"reference": "grid",
                                "curves_sha256": hashlib.sha256((in_dir / "curves.parquet").read_bytes()).hexdigest(),
                                # 84차 — null 은 시작 전 경계가 먼저 거부하므로 (§11-2) roster 축을 재려면 실제 closure
                                "base_config_digest": F.config_closure_sha256("configs/base.yaml")})
    with pytest.raises((ValueError, RuntimeError), match="roster"):
        F.run_fit(in_dir, out, _obj_cfg_min(), {OBJS[0]: {"w_pocv": 1.0}, OBJS[1]: {"w_pocv": 1.0, "_warm": False}},
                  _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False, warm_start=False,
                  stage3={**ctx, "planned": wrong})
    with pytest.raises((ValueError, RuntimeError)):
        F.run_fit(in_dir, out, _obj_cfg_min(), {OBJS[0]: {"w_pocv": 1.0}, OBJS[1]: {"w_pocv": 1.0, "_warm": False}},
                  _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=True, warm_start=False, stage3=ctx)


# ═════════════════════════════════════════════════════════════════════════════
# §s 82차 발송 전 자체 점검 (2026-09-28) — 81차 회신 닫힘 조건을 코드에 하나씩 대조해 찾은 구멍
#   F1 선언-행 충돌(sig 5) · F2 후보 재유도 · F3 실현 재계산 · F4 provider_consumed ↔ 계획 edge ·
#   F5 protocol sha 재계산 · F6 warm 공급 경로 실행 · F7 두 noise 실현 소비 경로 · F11 parameter_order = optimizer
#   벡터 · F12 objective 별 예산. 반례는 먼저 실측했다 (원장 §115 · 사용자 결정 "지금 고치고 영수증 한 번 더").
# ═════════════════════════════════════════════════════════════════════════════
_OBJ_W = {OBJS[0]: {"w_pocv": 1.0}, OBJS[1]: {"w_pocv": 1.0, "_warm": False}}


def _run_v6(tmp_path, name, ctx, in_dir, n_restarts=2):
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min
    out = tmp_path / name
    F.run_fit(in_dir, out, _obj_cfg_min(), _OBJ_W, _BOUNDS_MIN, "expanded", n_restarts, nproc=1,
              adaptive=False, warm_start=False, stage3=ctx)
    return out


def _fails(v) -> list:
    return [k for k in v["fail"] if k not in _DIRTY_TREE_CHECKS]


def _rewrite_map_and_record(out, mutate):
    """candidate_map 을 바꾸고 record 의 map sha · n · record_digest 를 **다시 맞춘다** — 자기일관 위조."""
    cm = json.loads((out / "candidate_map.json").read_text(encoding="utf-8"))
    mutate(cm["entries"])
    (out / "candidate_map.json").write_bytes(PV.canonical_bytes(cm))
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    rec["realized"]["candidate_map_sha256"] = PV.digest(cm["entries"])
    rec["realized"]["n_candidates"] = len(cm["entries"])
    rec["record_digest"] = PV.digest({k: v for k, v in rec.items() if k != "record_digest"})
    (out / "execution_record.json").write_bytes(PV.canonical_bytes(rec))


def _snapshot(out, names=("candidate_map.json", "execution_record.json", "fits.parquet", "manifest.yaml")):
    snap = {n: (out / n).read_bytes() for n in names}
    return lambda: [(out / n).write_bytes(b) for n, b in snap.items()]


def test_g81_s01_a_sig5_run_that_carries_v6_rows_or_a_stage3_block_is_a_declaration_conflict(tmp_path):
    """RED (F1): sig 5 선언 아래 v6 전용 행 키(candidate_id·bank_index) · `stage3` 블록 · v6 표식 열을 거부하지 않는다 —
    행 모양을 선언 문맥에 대조하지 않는다 (81차 N2 "행 모양은 그 문맥에 대조한다")."""
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    import yaml
    in_dir = _tiny_curves(tmp_path / "in"); out = tmp_path / "o"
    F.run_fit(in_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}}, _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False)
    restore = _snapshot(out, ("fits.parquet", "manifest.yaml"))
    # (a) sig 5 행에 v6 전용 키
    fits = pd.read_parquet(out / "fits.parquet")
    fits["restarts_json"] = [json.dumps([{**e, "candidate_id": HEX64, "bank_index": None} for e in json.loads(v)])
                             for v in fits["restarts_json"]]
    fits.to_parquet(out / "fits.parquet", index=False)
    v = IO.validate_provenance(out)
    assert "세대_선언_일치" in v["fail"], v["fail"]
    restore()
    # (b) sig 5 run_spec 에 stage3 블록
    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    man["run_spec"]["stage3"] = {"planned_id": HEX64}
    (out / "manifest.yaml").write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
    v = IO.validate_provenance(out)
    assert "세대_선언_일치" in v["fail"], v["fail"]
    restore()
    # (c) sig 5 fits 에 v6 표식 열
    fits = pd.read_parquet(out / "fits.parquet"); fits["record_generation"] = "v6"
    fits.to_parquet(out / "fits.parquet", index=False)
    v = IO.validate_provenance(out)
    assert "세대_선언_일치" in v["fail"], v["fail"]
    restore()
    v0 = IO.validate_provenance(out)
    assert _fails(v0) == [] and v0["checks"]["세대_선언_일치"] == "통과", "정상 sig 5 산출은 그대로 통과 (넓히지도 좁히지도 않음)"


def test_g81_s02_the_validator_rederives_every_candidate_from_plan_bank_bounds_and_design(tmp_path):
    """RED (F2): sig 6 validator 가 후보 ID **집합**만 대조한다 — 가짜 x0 digest · map 과 행에서 함께 바꾼 candidate_id ·
    뒤바꾼 bank_index 를 못 잡는다 ("64hex 존재만으로 통과 금지", 81차 §6)."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = _run_v6(tmp_path, "o", _v6_context(in_dir, budget=3), in_dir, n_restarts=3)
    restore = _snapshot(out)
    # (a) random 후보의 x0 digest 를 가짜로 (map 만 — 행에는 x0 가 없다)
    _rewrite_map_and_record(out, lambda ents: next(m for m in ents if m["source"] == "random").update(x0_sha256="0" * 64))
    assert "후보_재유도" in IO.validate_provenance(out)["fail"]
    restore()
    # (b) candidate_id 를 map 과 행에서 **같이** 바꾼다 — 집합 대조(candidate_ids_결속)는 통과한다
    target = {}

    def bad_id(ents):
        e = next(m for m in ents if m["source"] == "random")
        target.update(e); e["candidate_id"] = "1" * 64
    _rewrite_map_and_record(out, bad_id)
    fits = pd.read_parquet(out / "fits.parquet")

    def fix(v, cid, obj):
        rows = json.loads(v)
        if cid == target["cond_id"] and obj == target["objective"]:
            for e in rows:
                if e["i"] == target["i"]:
                    e["candidate_id"] = "1" * 64
        return json.dumps(rows)
    fits["restarts_json"] = [fix(v, c, o) for v, c, o in zip(fits["restarts_json"], fits["cond_id"], fits["objective"])]
    fits.to_parquet(out / "fits.parquet", index=False)
    v = IO.validate_provenance(out)
    assert v["checks"]["candidate_ids_결속"] == "통과", "집합 대조는 이 위조를 통과시킨다 — 그래서 재유도가 필요하다"
    assert "후보_재유도" in v["fail"], v["fail"]
    restore()
    # (c) 한 (조건, objective) 의 random 두 후보의 bank_index 를 map 에서 맞바꾼다 → 계획 구성과 다르다
    def swap(ents):
        key = next((m["cond_id"], m["objective"]) for m in ents if m["source"] == "random")
        rs = [m for m in ents if (m["cond_id"], m["objective"]) == key and m["source"] == "random"]
        rs[0]["bank_index"], rs[1]["bank_index"] = rs[1]["bank_index"], rs[0]["bank_index"]
    _rewrite_map_and_record(out, swap)
    assert "후보_재유도" in IO.validate_provenance(out)["fail"]
    restore()
    # (d) bank 를 계획 순서가 아닌 순서로 소비한 producer — 두 random 후보의 index·x0·ID 를 map 과 행에서 **통째로**
    #   맞바꾼다. x0 digest·candidate_id 는 각자 자기 bank 행과 맞으므로 구성(계획 순서) 대조만이 잡는다.
    moved = {}

    def reorder(ents):
        key = next((m["cond_id"], m["objective"]) for m in ents if m["source"] == "random")
        a, b = [m for m in ents if (m["cond_id"], m["objective"]) == key and m["source"] == "random"][:2]
        for f in ("bank_index", "x0_sha256", "candidate_id"):
            a[f], b[f] = b[f], a[f]
        moved.update({"key": key, a["i"]: (a["candidate_id"], a["bank_index"]), b["i"]: (b["candidate_id"], b["bank_index"])})
    _rewrite_map_and_record(out, reorder)
    fits = pd.read_parquet(out / "fits.parquet")

    def reorder_rows(v, cid, obj):
        rows = json.loads(v)
        if (cid, obj) == moved["key"]:
            for e in rows:
                if e["i"] in moved:
                    e["candidate_id"], e["bank_index"] = moved[e["i"]]
        return json.dumps(rows)
    fits["restarts_json"] = [reorder_rows(v, c, o) for v, c, o in zip(fits["restarts_json"], fits["cond_id"], fits["objective"])]
    fits.to_parquet(out / "fits.parquet", index=False)
    v = IO.validate_provenance(out)
    assert "후보_재유도" in v["fail"] and "계획 candidate_plan" in v["checks"]["후보_재유도"], v["checks"].get("후보_재유도")
    restore()
    v0 = IO.validate_provenance(out)
    assert _fails(v0) == [] and v0["checks"]["후보_재유도"] == "통과", v0["fail"]


def test_g81_s03_the_validator_recounts_realized_counts_from_the_rows(tmp_path):
    """RED (F3): 계획 범위 안에서 조작한 실현 count (한 random 후보를 미시도로 옮김) 가 통과한다 — validator 가 기록을
    fits 행·후보 map 에서 다시 세어 대조하지 않는다 (계획만 보는 `check_execution_record` 는 정의상 못 잡는다)."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    ctx = _v6_context(in_dir)
    out = _run_v6(tmp_path, "o", ctx, in_dir)
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    r = rec["realized"]["by_objective"][OBJS[0]]
    r["attempted"] -= 1; r["returned"] -= 1; r["not_attempted"] += 1; r["counts_by_source"]["random"] -= 1
    # 84차 v2 — 계획 범위 안 조작을 유지하려면 새 계수도 `≤ returned` 안에 둔다 (범위 검사는 계획 대조의 일부)
    r["finite"] = min(r["finite"], r["returned"]); r["converged"] = min(r["converged"], r["returned"])
    rec["record_digest"] = PV.digest({k: v for k, v in rec.items() if k != "record_digest"})
    (out / "execution_record.json").write_bytes(PV.canonical_bytes(rec))
    assert PV.check_execution_record(rec, ctx["planned"].envelope()) == [], "계획 대조만으로는 이 조작이 보이지 않는다"
    v = IO.validate_provenance(out)
    assert "실현_재계산" in v["fail"], v["fail"]


def test_g81_s04_provider_consumed_must_be_exactly_the_planned_edges_that_were_used():
    """RED (F4): `provider_consumed` 는 목록이기만 하면 통과했다 — 계획 edge 와 대조하지 않는다."""
    p = _planned_v4()                                        # no-provider 계획
    rec = _record_for(p)
    for garbage in ([{"consumer_objective": OBJS[1], "provider_objective": OBJS[0], "n_conditions": 1}],
                    [{"consumer_objective": "없음", "provider_objective": "x", "n_conditions": 999}],
                    [{"x": 1}]):
        bad = copy.deepcopy(rec); bad["realized"]["provider_consumed"] = garbage
        bad["record_digest"] = PV.digest({k: v for k, v in bad.items() if k != "record_digest"})
        assert PV.check_execution_record(bad, p.envelope()), garbage
    edge = {"stage": "condition", "arm": "G_C", "consumer_objective": OBJS[1], "provider_objective": OBJS[0],
            "provider_artifact_sha256": HEX64, "solution_map_sha256": HEX64, "provider_protocol_sha256": HEX64}
    w = _planned_v4(stages=_stages(arm="G_C", warm_map={OBJS[0]: None, OBJS[1]: OBJS[0]}), edges=[edge])
    n = w.envelope()["roster"]["n_obs"]
    ok = _record_for(w)
    ok["realized"]["provider_consumed"] = [{"consumer_objective": OBJS[1], "provider_objective": OBJS[0], "n_conditions": n}]
    ok["record_digest"] = PV.digest({k: v for k, v in ok.items() if k != "record_digest"})
    assert PV.check_execution_record(ok, w.envelope()) == []
    missing = copy.deepcopy(ok); missing["realized"]["provider_consumed"] = []
    missing["record_digest"] = PV.digest({k: v for k, v in missing.items() if k != "record_digest"})
    assert PV.check_execution_record(missing, w.envelope()), "warm 으로 시도했는데 공급 기록이 없다"


def test_g81_s05_the_map_protocol_sha_is_recomputed_from_the_provider_run_spec(tmp_path):
    """RED (F5): protocol sha 를 호출자 인자로 받아 그대로 봉인했다 — 고정 표 C 의 정의(provider run_spec 의
    canonical_bytes sha256)를 파일에서 다시 재지 않는다."""
    run = _provider_fits(tmp_path / "a", OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0]})
    hdr = F.make_solution_map(run, OBJS[0], tmp_path / "a" / "map.json")
    assert hdr["provider_protocol_sha256"] == _protocol_sha(run)
    other = _provider_fits(tmp_path / "b", OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0]}, run_spec={"sig_version": 6, "note": "다른 protocol"})
    assert F.make_solution_map(other, OBJS[0], tmp_path / "b" / "map.json")["provider_protocol_sha256"] != hdr["provider_protocol_sha256"]
    with pytest.raises(TypeError):
        F.make_solution_map(run, OBJS[0], tmp_path / "a" / "m2.json", provider_protocol_sha256="0" * 64)


def _warm_context(in_dir, provider_run, planning_dir, *, budget=2):
    """provider run(no-provider v6) 의 OBJS[0] 해 → 계획 map → G_C arm 계획 (edge 는 실제 바이트에서)."""
    planning_dir = Path(planning_dir); planning_dir.mkdir(parents=True, exist_ok=True)
    map_p = planning_dir / "plan_map.json"
    hdr = F.make_solution_map(provider_run, OBJS[0], map_p)
    edge = {"stage": "condition", "arm": "G_C", "consumer_objective": OBJS[1], "provider_objective": OBJS[0],
            "provider_artifact_sha256": hdr["provider_artifact_sha256"],
            "solution_map_sha256": hashlib.sha256(map_p.read_bytes()).hexdigest(),
            "provider_protocol_sha256": hdr["provider_protocol_sha256"]}
    return _v6_context(in_dir, budget=budget, arm="G_C", warm_map={OBJS[0]: None, OBJS[1]: OBJS[0]},
                       edges=[edge], provider_runs={OBJS[1]: provider_run})


def test_g81_s06_the_warm_supply_path_runs_end_to_end_and_its_x0_is_rederived(tmp_path):
    """RED (F6): warm 공급 경로 전체(`_stage3_candidates` 의 warm 가지 · provider run 을 가진 run_fit)를 실행하는 시험이
    0 이었다. 정상 봉인 공급 · warm 필요 자리 누락 → 시작 거부 · 계획 뒤 바뀐 provider → 시작 거부 · warm x0 위조 → validator
    거부 (81차 N3 닫힘 조건)."""
    import shutil
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    prov = _run_v6(tmp_path, "provider", _v6_context(in_dir), in_dir)
    ctx = _warm_context(in_dir, prov, tmp_path / "plan")
    out = _run_v6(tmp_path, "consumer", ctx, in_dir)
    env = ctx["planned"].envelope()
    pf = pd.read_parquet(prov / "fits.parquet")
    cm = json.loads((out / "candidate_map.json").read_text(encoding="utf-8"))["entries"]
    warm = [m for m in cm if m["source"] == "warm"]
    assert warm and {m["objective"] for m in warm} == {OBJS[1]}
    for m in warm:                                           # warm x0 = provider 의 그 조건 · OBJS[0] 해 (PARAM_NAMES 열)
        row = pf[(pf["cond_id"] == m["cond_id"]) & (pf["objective"] == OBJS[0])].iloc[0]
        assert m["x0_sha256"] == DW.x0_sha256(np.array([float(row[c]) for c in F.PARAM_NAMES]))
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    assert rec["realized"]["provider_consumed"] == [{"consumer_objective": OBJS[1], "provider_objective": OBJS[0],
                                                     "n_conditions": env["roster"]["n_obs"]}]
    sealed = out / "_inputs" / "provider_maps" / f"{OBJS[1]}.solution_map.json"
    assert hashlib.sha256(sealed.read_bytes()).hexdigest() == env["provider_edges"][0]["solution_map_sha256"]
    fits = pd.read_parquet(out / "fits.parquet")
    assert set(fits[fits["objective"] == OBJS[1]]["warm_started"]) == {True}
    assert set(fits[fits["objective"] == OBJS[0]]["warm_started"]) == {False}
    v = IO.validate_provenance(out)
    assert _fails(v) == [], v["fail"]
    assert v["checks"]["후보_재유도"] == "통과" and v["checks"]["실현_재계산"] == "통과"
    # 음성 ① warm 이 필요한 자리의 provider run 누락 → 시작하지 않는다 (no-warm 전환 금지)
    with pytest.raises(ValueError, match="provider"):
        _run_v6(tmp_path, "c_missing", {**ctx, "provider_runs": {}}, in_dir)
    # 음성 ② 계획 뒤 provider fits 가 바뀌었다 → 다시 만든 map 이 계획 edge 와 다르다 → 시작하지 않는다
    prov2 = tmp_path / "provider_changed"; shutil.copytree(prov, prov2)
    pf2 = pd.read_parquet(prov2 / "fits.parquet")
    pf2.loc[pf2.index[0], F.PARAM_NAMES[0]] = float(pf2.loc[pf2.index[0], F.PARAM_NAMES[0]]) + 1e-6
    pf2.to_parquet(prov2 / "fits.parquet", index=False)
    #   (실행 **시작 전** 거부여야 한다 — 변이 재생 실측: 시작 대조를 끄면 worker 안의 `provider_x0` 봉인 대조가 같은
    #   조건을 늦게 잡아 "map|sha" 는 여전히 맞았다. 그래서 시작 대조의 문장과 fits 미생성을 함께 본다.)
    with pytest.raises(ValueError, match="다시 만든 map sha"):
        _run_v6(tmp_path, "c_changed", {**ctx, "provider_runs": {OBJS[1]: prov2}}, in_dir)
    assert not (tmp_path / "c_changed" / "fits.parquet").exists(), "계획 뒤 바뀐 provider 로는 fitting 이 시작되지 않는다"
    # 음성 ③ consumer 산출의 warm x0 digest 위조 → validator 재유도가 잡는다
    _rewrite_map_and_record(out, lambda ents: next(m for m in ents if m["source"] == "warm").update(x0_sha256="0" * 64))
    assert "후보_재유도" in IO.validate_provenance(out)["fail"]


def _two_noise_curves(tmp):
    """같은 물리좌표 (0.02, 0.02, 0.02) 의 noise 0 · 0.001 두 실현 + reference — 실제 producer 형식 (sign_producer).

    producer 검증(`관측_noise_family_완전성`)은 **모든** 물리 family 가 서명된 noise 집합 전체를 갖기를 요구한다 —
    그래서 reference family 도 두 noise 를 갖는다 (첫 판은 reference 를 noise 0 하나로 두어 실측으로 거부됐다).
    """
    from tests.test_fitting import sign_producer
    x = np.linspace(0.0, 1.0, 48); rows = []
    for lli, pe, ne, noise in [(0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.001),
                               (0.02, 0.02, 0.02, 0.0), (0.02, 0.02, 0.02, 0.001)]:
        q = 4000.0 * (1.0 - 0.5 * (pe + ne))
        for xi in x:
            v_full = 4.2 - 0.9 * xi - 0.3 * pe * xi; v_ne = 0.1 + 0.4 * xi
            rows.append({"cond_id": f"c_{lli}_{noise}", "x_norm": xi, "v_full": v_full, "v_pe": v_full + v_ne,
                         "v_ne": v_ne, "q_mah": q, "lli": lli, "lam_pe": pe, "lam_ne": ne, "noise": noise})
    return sign_producer(tmp, pd.DataFrame(rows))


def test_g81_s07_two_noise_realizations_of_one_pair_group_through_the_real_consumption_path(tmp_path):
    """81차 N1 닫힘 조건 (F7): 같은 pair group 의 두 noise 실현을 실제 소비 경로(run_fit → validate)에 건다.

    기능은 라운드 1 에 있었고 빠졌던 것은 **실제 소비 경로의 fixture** 다 — 처음부터 GREEN 일 수 있는 대조군 (리뷰 §7-4).
    둘은 pair_group·bank 를 공유하고(noise 는 제외 축) obs_key 로만 갈린다.
    """
    from src.grid import Condition
    in_dir = _two_noise_curves(tmp_path / "in")
    ctx = _v6_context(in_dir, budget=3)
    out = _run_v6(tmp_path, "o", ctx, in_dir, n_restarts=3)
    fits = pd.read_parquet(out / "fits.parquet")
    pair = fits[fits["lli"] == 0.02]
    assert pair["cond_id"].nunique() == 2 and set(pair["noise"]) == {0.0, 0.001}
    assert pair["pair_group_id"].nunique() == 1 and pair["bank_id"].nunique() == 1
    cm = json.loads((out / "candidate_map.json").read_text(encoding="utf-8"))["entries"]
    ids = [sorted(m["candidate_id"] for m in cm if m["cond_id"] == c and m["objective"] == OBJS[0] and m["source"] == "random")
           for c in sorted(pair["cond_id"].unique())]
    assert ids[0] == ids[1] and ids[0], "같은 bank 행 → 같은 random candidate_id (noise 는 ID 축이 아니다)"
    cur = pd.read_parquet(in_dir / "curves.parquet")
    conds = [Condition(float(g["lli"].iloc[0]), float(g["lam_pe"].iloc[0]), float(g["lam_ne"].iloc[0]),
                       str(g["lam_pe_type"].iloc[0]), str(g["lam_ne_type"].iloc[0]), float(g["noise"].iloc[0]),
                       int(g["seed"].iloc[0])) for _, g in cur.groupby("cond_id")]
    roster = DW.roster_from_conditions(conds, design=ctx["design"], comparison_family_id="p22_grid_primary_v6",
                                       treatment_id="none", replicate_id=0)
    two = [e for e in roster if e["pair_group_id"] == pair["pair_group_id"].iloc[0]]
    assert len(two) == 2 and two[0]["obs_key"] != two[1]["obs_key"]
    v = IO.validate_provenance(out)
    assert _fails(v) == [], v["fail"]


def test_g81_s08_parameter_order_is_the_optimizer_vector_and_the_map_reads_solution_columns(tmp_path):
    """RED (F11): 설계 parameter_order 가 optimizer 벡터(`PARAM_NAMES`)에 묶이지 않았다 — 5 이름 좌표 order 로도 v6 실행이
    시작되고, solution map 은 이름이 같은 **truth 열**(lli·lam_pe·lam_ne)을 해로 읽을 수 있었다."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    old = DW.canonical_design_spec(
        label="p22_grid_primary_v6", arms=["G_A", "G_C"], parameter_order=["lli", "lam_pe", "lam_ne", "p_ini_scale", "shift"],
        bounds_policy="exact_ordered_bounds_digest", objective_plan=OBJS, bank_generator="pcg64", bank_version="v6.0",
        seed_derivation="H(pair_group_id, bank_version)", dtype="float64", endian="little", coordinate_unit="fraction")
    with pytest.raises(ValueError, match="parameter_order"):
        _run_v6(tmp_path, "o", _v6_context(in_dir, design=old), in_dir)
    run = _provider_fits(tmp_path / "p", OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0]})      # truth 열은 0.5 (미끼)
    hdr = F.make_solution_map(run, OBJS[0], tmp_path / "p" / "map.json")
    assert hdr["parameter_order"] == list(F.PARAM_NAMES)
    doc = json.loads((tmp_path / "p" / "map.json").read_text(encoding="utf-8"))
    assert [float(v) for v in doc["entries"]["c1"]["p"]] == [1.2, 0.1, 0.9, 0.0], "해 열을 읽어야 한다 — truth 0.5 가 아니다"


def test_g81_s09_budgets_are_checked_per_objective_for_v6(tmp_path):
    """RED (F12): sig 6 산출에도 legacy `restart_예산_완주`(전역 n_restarts) 를 적용해 objective 별 예산(2 · 3)을 거부했다."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = _run_v6(tmp_path, "o", _v6_context(in_dir, budgets={OBJS[0]: 2, OBJS[1]: 3}), in_dir, n_restarts=3)
    v = IO.validate_provenance(out)
    assert _fails(v) == [], v["fail"]
    assert v["checks"]["restart_예산_완주"] == "통과"
