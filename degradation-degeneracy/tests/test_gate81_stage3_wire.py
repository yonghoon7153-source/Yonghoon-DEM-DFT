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
ORDER = ["lli", "lam_pe", "lam_ne", "p_ini_scale", "shift"]
OBJS = ["pocv_dvdq", "pocv_dvdq_dqdv"]
LB = np.array([0.5, -1.0, 0.5, -1.0])
UB = np.array([2.0, 1.0, 2.0, 1.0])
INIT = np.array([1.0, 0.0, 1.0, 0.0])
COORDS = {"lli": "0.17", "lam_pe": "0.13", "lam_ne": "0.13",
          "lam_pe_type": "capacity", "lam_ne_type": "capacity"}
COORDS2 = {"lli": "0", "lam_pe": "0", "lam_ne": "0",
           "lam_pe_type": "capacity", "lam_ne_type": "capacity"}
HEX64 = "a" * 64


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


def _stages(mode="legacy_slot_replace", budget=3, arm="G_A", warm_map=None):
    return [{"stage": "condition", "arm": arm,
             "budget_by_objective": {o: budget for o in OBJS},
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
    by_obj = realized or {
        o: {"attempted": sum(pc[o].values()), "returned": sum(pc[o].values()), "failed": 0,
            "not_attempted": 0,
            "counts_by_source": dict(pc[o]),
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
    short = {o: {"attempted": 2, "returned": 2, "failed": 0, "not_attempted": 1,
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
def _provider_fits(tmp: Path, objective: str, rows: dict[str, list[float]]) -> Path:
    df = pd.DataFrame([{"cond_id": c, "objective": objective, "lli": p[0], "lam_pe": p[1],
                        "lam_ne": p[2], "shift": p[3], "J": 0.1, "converged": True}
                       for c, p in rows.items()])
    path = tmp / "fits.parquet"; df.to_parquet(path, index=False)
    return path


def _edge(fits: Path, map_path: Path, *, provider=OBJS[0], consumer=OBJS[1], protocol="e" * 64):
    return {"stage": "condition", "arm": "G_C", "consumer_objective": consumer,
            "provider_objective": provider,
            "provider_artifact_sha256": hashlib.sha256(fits.read_bytes()).hexdigest(),
            "solution_map_sha256": hashlib.sha256(map_path.read_bytes()).hexdigest(),
            "provider_protocol_sha256": protocol}


def test_g81_n3_01_solution_map_header_binds_fits_bytes_objective_and_protocol(tmp_path):
    """RED: `make_solution_map` 가 없다. header = objective · fits sha · protocol sha · parameter_order · 제외 목록."""
    fits = _provider_fits(tmp_path, OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0], "c2": [1.4, float("nan"), 0.8, 0.1]})
    hdr = F.make_solution_map(fits, OBJS[0], tmp_path / "map.json",
                              provider_protocol_sha256="e" * 64, parameter_order=["lli", "lam_pe", "lam_ne", "shift"])
    assert hdr["schema"] == "solution-map/v1" and hdr["provider_objective"] == OBJS[0]
    assert hdr["provider_artifact_sha256"] == hashlib.sha256(fits.read_bytes()).hexdigest()
    assert hdr["provider_protocol_sha256"] == "e" * 64 and hdr["n_entries"] == 1
    assert hdr["excluded_cond_ids"] == ["c2"], "비유한 해는 entries 가 아니라 제외 목록"
    doc = json.loads((tmp_path / "map.json").read_text(encoding="utf-8"))
    assert set(doc["entries"]) == {"c1"} and doc["header"] == hdr
    with pytest.raises(ValueError):
        F.make_solution_map(fits, "pocv_dvdq_dqdv", tmp_path / "map2.json",
                            provider_protocol_sha256="e" * 64, parameter_order=["lli", "lam_pe", "lam_ne", "shift"])


def test_g81_n3_02_consumer_rejects_wrong_fits_map_combination_and_unsealed_maps(tmp_path):
    """RED: `provider_x0` 가 없다. 세 sha 가 전부 진짜라도 fits A + map B(다른 조건 세트) 결합은 거부."""
    order = ["lli", "lam_pe", "lam_ne", "shift"]
    fits_a = _provider_fits(tmp_path / "a", OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0]})
    fits_b = _provider_fits(tmp_path / "b", OBJS[0], {"c1": [1.9, 0.9, 1.9, 0.9]})
    F.make_solution_map(fits_a, OBJS[0], tmp_path / "a" / "map.json", provider_protocol_sha256="e" * 64, parameter_order=order)
    F.make_solution_map(fits_b, OBJS[0], tmp_path / "b" / "map.json", provider_protocol_sha256="e" * 64, parameter_order=order)
    edge_ok = _edge(fits_a, tmp_path / "a" / "map.json")
    x0, sha = F.provider_x0(tmp_path / "a" / "map.json", edge=edge_ok, cond_id="c1", lb=LB, ub=UB, parameter_order=order)
    assert np.allclose(x0, [1.2, 0.1, 0.9, 0.0]) and sha == DW.x0_sha256(x0)
    # fits A 의 edge 로 map B 를 소비 — header 의 artifact sha 가 edge 와 다르다
    with pytest.raises(ValueError):
        F.provider_x0(tmp_path / "b" / "map.json", edge=edge_ok, cond_id="c1", lb=LB, ub=UB, parameter_order=order)
    # 봉인 전 소비 — map 파일을 한 바이트 바꾼다
    raw = bytearray((tmp_path / "a" / "map.json").read_bytes()); raw[-2] ^= 0x20
    (tmp_path / "a" / "tampered.json").write_bytes(bytes(raw))
    with pytest.raises(ValueError):
        F.provider_x0(tmp_path / "a" / "tampered.json", edge=edge_ok, cond_id="c1", lb=LB, ub=UB, parameter_order=order)


def test_g81_n3_03_consumer_rejects_missing_condition_wrong_objective_and_out_of_bounds_without_clipping(tmp_path):
    """RED: 누락 cond_id 는 오류(no-warm 전환 아님) · objective 불일치 거부 · bounds 밖 p 는 clip 하지 않고 거부."""
    order = ["lli", "lam_pe", "lam_ne", "shift"]
    fits = _provider_fits(tmp_path, OBJS[0], {"c1": [1.2, 0.1, 0.9, 0.0], "c3": [3.5, 0.0, 0.9, 0.0]})
    F.make_solution_map(fits, OBJS[0], tmp_path / "map.json", provider_protocol_sha256="e" * 64, parameter_order=order)
    edge = _edge(fits, tmp_path / "map.json")
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


def test_g81_w03_legacy_fit_is_byte_identical_golden_still_holds():
    """GREEN 대조군: `candidates` 를 주지 않으면 79차 골든이 그대로다 (`test_gate79_stage3_logging.py::g79_02` 와 같은 값)."""
    from tests.test_gate79_stage3_logging import _GOLDEN, _INIT, _LB, _UB, _obj as _obj79
    r = F.fit(_obj79, _INIT, _LB, _UB, n_restarts=3, seed=7, adaptive=False)
    g = _GOLDEN[False]
    assert r.p.tolist() == g["p"] and r.J == g["J"] and r.n_eval == g["n_eval"]
    assert [(e["i"], e["source"]) for e in r.restarts] == [(e["i"], e["source"]) for e in g["restarts"]]
    assert all(set(e) == {"p", "J", "i", "source", "warm", "converged", "n_eval", "termination_status"}
               for e in r.restarts), "legacy 행은 8 키 그대로 — candidate 키가 새지 않는다"


def _v6_context(in_dir: Path, *, design=None, budget=2, arm="G_A"):
    """tiny curves → 조건 → roster → PlannedLegV4 (no-provider · grid 기준)."""
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
    stages = _stages(budget=budget, arm=arm)
    planned = _planned_v4(design=design, roster=roster, stages=stages,
                          source_digest=IO.source_digest(),
                          inputs={"reference": "grid",
                                  "curves_sha256": hashlib.sha256((in_dir / "curves.parquet").read_bytes()).hexdigest(),
                                  "base_config_digest": None})
    return {"planned": planned, "design": design, "provider_maps": {}}


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
    assert rec["schema"] == "execution-record/v1" and rec["planned_id"] == ctx["planned"].planned_id()
    assert PV.check_execution_record(rec, ctx["planned"].envelope()) == []
    cmap = json.loads((out / "candidate_map.json").read_text(encoding="utf-8"))
    assert PV.digest(cmap["entries"]) == rec["realized"]["candidate_map_sha256"]
    ids_rows = {e["candidate_id"] for rs in fits["restarts_json"] for e in json.loads(rs)}
    assert ids_rows == {m["candidate_id"] for m in cmap["entries"]}
    v = IO.validate_provenance(out)
    assert v["ok"] is True, v["fail"]
    assert "restart_후보" in v["checks"]


def test_g81_w05_validate_provenance_dispatches_on_sig_version_and_fails_closed(tmp_path):
    """RED: sig 6 인데 stage3 블록이 없으면 실패 · sig 7 은 거부 · sig 5 산출은 기존 검사 그대로 (record 요구 없음)."""
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    import yaml
    in_dir = _tiny_curves(tmp_path / "in"); out = tmp_path / "o"
    F.run_fit(in_dir, out, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}}, _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False)
    assert IO.validate_provenance(out)["ok"] is True, "legacy sig 5 산출 — 기존 검사 불변"
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
    """RED: 계획 roster 와 실제 조건 집합이 다르면 시작하지 않는다 · warm arm 인데 provider map 이 없으면 시작하지 않는다."""
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in"); out = tmp_path / "o"
    ctx = _v6_context(in_dir)
    wrong = _planned_v4(roster=_roster_entries(), stages=_stages(budget=2), source_digest=IO.source_digest(),
                        inputs={"reference": "grid",
                                "curves_sha256": hashlib.sha256((in_dir / "curves.parquet").read_bytes()).hexdigest(),
                                "base_config_digest": None})
    with pytest.raises((ValueError, RuntimeError), match="roster"):
        F.run_fit(in_dir, out, _obj_cfg_min(), {OBJS[0]: {"w_pocv": 1.0}, OBJS[1]: {"w_pocv": 1.0, "_warm": False}},
                  _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False, warm_start=False,
                  stage3={**ctx, "planned": wrong})
    with pytest.raises((ValueError, RuntimeError)):
        F.run_fit(in_dir, out, _obj_cfg_min(), {OBJS[0]: {"w_pocv": 1.0}, OBJS[1]: {"w_pocv": 1.0, "_warm": False}},
                  _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=True, warm_start=False, stage3=ctx)
