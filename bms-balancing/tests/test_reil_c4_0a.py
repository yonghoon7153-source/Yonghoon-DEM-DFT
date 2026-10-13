"""REIL C4-0a — 감시 · 기록 보완 (C4-N2 · N3) · Phase A 배열 정식 봉인 · E3a 실행기 · identity · 계획 건조 (상태 문서 §39).

합성 입력과 보존된 util 사본만 쓴다. REIL xlsx · pkl · 노트북은 열지 않는다. 실행 경로 · 횟수는 상태 문서 §39 (RED 1 · GREEN 1).
"""
import copy
import hashlib
import io
import json
import os
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import reil_c4_e3a as e3a
from scripts import reil_c4_monitor as mon

BMS = Path(__file__).resolve().parents[1]
NEW_SEAL = BMS / "reil_c6_rebuild_20261013"
NEW_SEAL_MANIFEST = "4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc"
UTIL_COPY = BMS / "reviews" / "prereview_pybamm_reil_20261003" / "external" / "util_LFP.py.txt"
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"

LIM = {"measure": 30.0, "grace": 3.0, "rss": 10 ** 12, "rss_gap": 5.0, "disk_new": 10 ** 12, "disk_free": 0, "disk_gap": 15.0}


def _sleep_task(task, ctx, notify=None, progress=None):
    time.sleep(task.get("s", 0.05))
    return {"task_id": task["task_id"], "value": task["task_id"] * 2}


def _tasks(n, n_workers, s=0.05):
    return [{"task_id": i, "worker": i % n_workers, "s": s} for i in range(n)]


# ======================================================================== (1) 감시 — 늦은 성공 표본 · None · 예외 · 첫 지연 (C4-N2)
def test_01_a_late_successful_sample_does_not_hide_the_gap():
    w = mon.Watch("rss", gap_limit=5.0, t_start=0.0)
    assert w.observe(0.5, 100, 1.0) is None
    reason = w.observe(1.5, 100, 7.2)                 # 값은 왔지만 마지막 유효 표본에서 6.2 s 뒤
    assert reason is not None and "늦은 성공 표본" in reason
    assert w.samples[-1]["t_after"] == 7.2 and w.samples[-1]["latency"] == pytest.approx(5.7)


def test_01_the_gap_is_measured_when_the_sample_arrives_not_when_it_was_requested():
    w = mon.Watch("disk", gap_limit=15.0, t_start=0.0)
    assert w.observe(14.0, (1, 2), 14.5) is None       # 요청 · 도착 모두 15 s 안
    assert w.observe(28.0, (1, 2), 30.1) is not None   # 요청은 14.5 + 13.5 · 도착은 15.6 s 뒤


def test_01_none_exception_and_first_delay_are_told_apart():
    first = mon.Watch("rss", gap_limit=5.0, t_start=0.0)
    r = first.observe(5.5, 100, 6.0)                  # 유효 표본이 한 번도 없었는데 6 s
    assert r is not None and "첫 표본 지연" in r
    none = mon.Watch("rss", gap_limit=5.0, t_start=0.0)
    assert none.observe(0.5, 100, 0.6) is None
    assert none.observe(2.0, None, 2.1) is None        # None 은 공백 한도 안에서는 기다린다
    r = none.observe(5.9, None, 6.0)
    assert r is not None and "표본 없음" in r
    exc = mon.Watch("rss", gap_limit=5.0, t_start=0.0)
    r = exc.observe(0.5, None, 0.6, error="OSError: boom")
    assert r is not None and "예외" in r                # 예외는 기다리지 않는다 (fail-closed)


# ======================================================================== (2) 감시 — 마감 재검사 · 마감 뒤 신규 시작 없음 (C4-N2)
def test_02_a_slow_sample_past_the_deadline_stops_before_new_tasks_start():
    calls = {"n": 0}

    def slow_rss(pids):
        calls["n"] += 1
        if calls["n"] == 2:
            time.sleep(1.5)                              # 표본 하나가 마감 (1.0 s) 을 넘겨 돌아온다
        return 1000

    lim = dict(LIM, measure=1.0, rss_gap=60.0)
    out = mon.supervise(_tasks(40, 2, s=0.1), {}, _sleep_task, n_workers=2, limits=lim, t0=time.monotonic(),
                        rss_fn=slow_rss, disk_fn=lambda roots: (0, 10 ** 12), out_roots=[], tick=0.05, disk_every=0.05)
    assert out["global_stop"] is not None and "마감" in out["global_stop"]
    starts_after = [s for s in out["states"] if s.get("t_start_rel") is not None and s["t_start_rel"] > lim["measure"] + 0.25]
    assert starts_after == []                           # 작업자도 마감 뒤에는 새 작업을 시작하지 않는다
    assert sum(1 for s in out["states"] if s["state"] == "NOT_STARTED") > 0


class _ListQueue:
    def __init__(self):
        self.items = []

    def put(self, item):
        self.items.append(item)


class _NeverStop:
    def is_set(self):
        return False


def test_02_workers_check_the_deadline_themselves():
    q = _ListQueue()                                    # 부모가 멈추지 않아도 작업자 스스로 마감 뒤 시작하지 않는다
    mon.worker_loop(0, _tasks(3, 1), {}, _sleep_task, q, _NeverStop(), {}, deadline_abs=time.monotonic() - 0.01)
    kinds = [k for k, _, _ in q.items]
    assert "start" not in kinds and "worker_deadline" in kinds
    q2 = _ListQueue()
    mon.worker_loop(0, _tasks(2, 1), {}, _sleep_task, q2, _NeverStop(), {}, deadline_abs=time.monotonic() + 60)
    assert [k for k, _, _ in q2.items].count("done") == 2


def test_02_a_late_rss_sample_inside_supervise_is_a_global_stop():
    calls = {"n": 0}

    def late(pids):
        calls["n"] += 1
        if calls["n"] == 3:
            time.sleep(1.2)
        return 1000

    lim = dict(LIM, measure=30.0, rss_gap=1.0)
    out = mon.supervise(_tasks(30, 2, s=0.2), {}, _sleep_task, n_workers=2, limits=lim, t0=time.monotonic(),
                        rss_fn=late, disk_fn=lambda r: (0, 10 ** 12), out_roots=[], tick=0.05, disk_every=0.05)
    assert out["global_stop"] is not None and "늦은 성공 표본" in out["global_stop"]
    assert out["owned_alive_after"] == 0


def test_02_all_tasks_complete_without_a_stop():
    out = mon.supervise(_tasks(8, 2), {}, _sleep_task, n_workers=2, limits=LIM, t0=time.monotonic(),
                        rss_fn=lambda p: 1000, disk_fn=lambda r: (0, 10 ** 12), out_roots=[], tick=0.05, disk_every=0.05)
    assert out["global_stop"] is None
    assert [s["state"] for s in out["states"]] == ["COMPLETED"] * 8
    assert [s["value"] for s in out["states"]] == [2 * i for i in range(8)]


# ======================================================================== (3) 산출량 — 본체 · 래퍼 · 임시 · 최종 기록 합산 (C4-N3)
def test_03_output_bytes_sum_every_owned_root_once(tmp_path):
    body, wrapper, tmp = tmp_path / "out", tmp_path / "out_wrapper", tmp_path / "tmp"
    for d, n in ((body, 10), (wrapper, 20), (tmp, 30)):
        d.mkdir()
        (d / "f.bin").write_bytes(b"x" * n)
    (body / "sub").mkdir()
    (body / "sub" / "g.bin").write_bytes(b"y" * 5)
    assert mon.output_bytes([body, wrapper, tmp]) == 65
    assert mon.output_bytes([body, body / "sub", wrapper]) == 35          # 겹친 루트는 한 번만
    assert mon.output_bytes([tmp_path / "missing"]) == 0


def test_03_a_size_limit_broken_by_the_final_write_is_not_success(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "big.bin").write_bytes(b"z" * 900)
    fr = mon.final_record(out, {"ROWS.json": [{"a": "b" * 300}]}, roots=[out], limit_bytes=1000,
                          clock=time.monotonic, t0=time.monotonic(), limit_s=60.0)
    assert fr["record_state"] == "OUTPUT_LIMIT_EXCEEDED"
    assert fr["output_bytes_after"] > 1000 and (out / "ROWS.json").is_file()   # 쓴 파일은 보존


def test_03_final_record_within_limits_is_complete_and_hashed(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    fr = mon.final_record(out, {"A.json": {"k": 1}}, roots=[out], limit_bytes=10 ** 6, clock=time.monotonic,
                          t0=time.monotonic(), limit_s=60.0)
    assert fr["record_state"] == "COMPLETE"
    assert fr["files"]["A.json"] == hashlib.sha256((out / "A.json").read_bytes()).hexdigest()


# ======================================================================== (4) 자체 산출 경로 — 경계 비교 · Git 원문 (C4-N3)
def test_04_exact_and_sub_paths_are_owned_but_prefix_siblings_are_not():
    roots = ["bms-balancing/evidence/reil_c4_e3a_x"]
    assert mon.owned("bms-balancing/evidence/reil_c4_e3a_x", roots)
    assert mon.owned("bms-balancing/evidence/reil_c4_e3a_x/ROWS.json", roots)
    assert mon.owned("bms-balancing/evidence/reil_c4_e3a_x/", roots)
    assert not mon.owned("bms-balancing/evidence/reil_c4_e3a_x_wrapper/meta.txt", roots)
    assert not mon.owned("bms-balancing/evidence/reil_c4_e3a_xb", roots)
    assert not mon.owned("bms-balancing/evidence", roots)


def test_04_split_dirty_keeps_the_raw_text_and_does_not_own_ambiguous_lines():
    raw = ("?? bms-balancing/evidence/reil_c4_e3a_x/ROWS.json\n"
           "?? bms-balancing/evidence/reil_c4_e3a_x_wrapper/meta.txt\n"
           '?? "bms-balancing/evidence/reil_c4_e3a_x/a b.json"\n'
           "R  bms-balancing/evidence/reil_c4_e3a_x/a.json -> bms-balancing/scripts/b.py\n"
           " M bms-balancing/scripts/reil_c4_e3a.py\n")
    r = mon.split_dirty(raw, ["bms-balancing/evidence/reil_c4_e3a_x"])
    assert r["raw"] == raw
    assert r["own_output"] == ["?? bms-balancing/evidence/reil_c4_e3a_x/ROWS.json"]
    assert len(r["ambiguous"]) == 2 and len(r["other"]) == 2


# ======================================================================== (5) Phase A 배열 정식 봉인 (C4 v2 §4-3 · §39)
def test_05_phase_a_arrays_regenerate_byte_for_byte_against_the_accepted_seal():
    arrays = e3a.phase_a_arrays()
    assert sorted(arrays) == ["sobol_A0_their_box_seed0.npy", "sobol_A0_their_box_seed1.npy",
                              "sobol_A1_A2_wide_box_seed0.npy", "sobol_A1_A2_wide_box_seed1.npy"]
    for name, a in arrays.items():
        buf = io.BytesIO()
        np.save(buf, a, allow_pickle=False)
        assert buf.getvalue() == (NEW_SEAL / name).read_bytes(), name
        assert a.shape == (64, 4)


def test_05_seal_arrays_writes_a_new_folder_with_manifest_and_refuses_an_existing_one(tmp_path):
    out = tmp_path / "arrays"
    rec = e3a.seal_arrays(out, c6_seal=NEW_SEAL)
    man = json.loads((out / "MANIFEST.json").read_text(encoding="utf-8"))
    assert sorted(man) == ["ARRAYS.json", "sobol_A0_their_box_seed0.npy", "sobol_A0_their_box_seed1.npy",
                           "sobol_A1_A2_wide_box_seed0.npy", "sobol_A1_A2_wide_box_seed1.npy"]
    for n, h in man.items():
        assert hashlib.sha256((out / n).read_bytes()).hexdigest() == h
    meta = json.loads((out / "ARRAYS.json").read_text(encoding="utf-8"))
    assert set(meta["arrays"]["sobol_A0_their_box_seed0.npy"]) >= {"raw_float64_le_sha256", "npy_sha256", "c6_npy_sha256"}
    assert "label-seed" in meta["not_in_this_seal"]          # §39 의 이월 — 프로파일 Sobol 2 · 동시 Sobol 16 은 C4-0b
    assert rec["ok"] is True
    with pytest.raises(e3a.E3aStop):
        e3a.seal_arrays(out, c6_seal=NEW_SEAL)


def test_05_a_mismatch_with_the_accepted_seal_writes_nothing(tmp_path):
    out = tmp_path / "arrays"

    def wrong(seed, box):
        return np.zeros((64, 4))

    with pytest.raises(e3a.E3aStop):
        e3a.seal_arrays(out, c6_seal=NEW_SEAL, make=wrong)
    assert not out.exists()


# ======================================================================== (6) E3a 계획 — 노트북 case 표 · 66 호출 · 고정 배정
def test_06_algorithm_branches_follow_the_util_code():
    assert e3a.algorithm_of([1]) == {"name": "GA", "pop": 50, "gen": 100, "seeds": list(range(20)), "expected_evals": 100000}
    assert e3a.algorithm_of([0, 1])["name"] == "NSGA2" and e3a.algorithm_of([0, 1, 2])["expected_evals"] == 5000
    nsga3 = e3a.algorithm_of([0, 1, 2, 3])
    assert (nsga3["name"], nsga3["pop"], nsga3["seeds"], nsga3["expected_evals"]) == ("NSGA3", 165, [1], 16500)
    with pytest.raises(ValueError):
        e3a.algorithm_of([])


def test_06_the_plan_has_66_calls_fixed_by_call_id():
    plan = e3a.plan_calls(4)
    assert len(plan) == 66 and len({(p["case"], p["row"]) for p in plan}) == 66
    assert [p["call_id"] for p in plan] == list(range(66))
    assert all(p["worker"] == p["call_id"] % 4 for p in plan)
    assert {p["case"]: p["obj_selection"] for p in plan} == {0: [1], 1: [0, 1], 2: [2, 3], 3: [0, 1, 2], 4: [0, 1, 3], 5: [0, 1, 2, 3]}
    per_cell = {}
    for p in plan:
        per_cell[p["row"]] = per_cell.get(p["row"], 0) + p["algorithm"]["expected_evals"]
    assert set(per_cell.values()) == {136500} and sum(per_cell.values()) == 1501500   # v2 §1 산술 그대로
    assert sum(len(p["algorithm"]["seeds"]) for p in plan) == 275                      # 부속 A §3-8: optimizer 호출 275


# ======================================================================== (7) E3a 호출 하나 — 계수 · 외삽 · G · 원본 불변 · 오류 분류
FAKE_UTIL = '''
import numpy as np

MODE = {"kind": "ok"}


class Result:
    pass


def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
    q = np.linspace(0.0, 1.0, interp_len)
    return (q * m_P - d_P, q * m_N - d_N, None, None, None, None, None, None)


def objective_fun(x, Model, halfcell):
    Model["touched"] = Model.get("touched", 0) + 1
    if MODE["kind"] == "value_error" and Model["touched"] == 2:
        np.max(np.array([]))
    if MODE["kind"] == "memory":
        raise MemoryError("fake")
    dVdQ_hc(halfcell[1], halfcell[0], halfcell[3], halfcell[2], *x, interp_len=50)
    f = np.array([0.1, float(np.sum(np.asarray(x) ** 2)), 0.2, 0.3])
    if Model["touched"] % 3 == 0:
        f[1] = float("nan")
    return f


def run_optimization(Model, halfcell, obj_selection, pop_size=50):
    xs = [np.array([0.9, 0.8, 0.2, 0.1]), np.array([1.0, 1.0, 0.1, 0.4]), np.array([0.7, 0.6, 0.3, 0.2])]
    for x in xs:
        objective_fun(x, Model, halfcell)
    res = Result()
    res.X = np.array(xs)
    res.F = np.array([[0.5], [float("nan")], [0.2]])
    res.G = None if MODE["kind"] == "no_G" else np.array([[x[3] - x[2] + 1e-4] for x in xs])
    res.success = True
    return res
'''


@pytest.fixture
def fake(tmp_path):
    import importlib.machinery
    import importlib.util
    p = tmp_path / "fake_util_LFP.py"
    p.write_text(FAKE_UTIL, encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader(f"fake_util_c4_{tmp_path.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    model = {"Q_exp_interp": np.linspace(-0.2, 1.2, 50), "V_exp_interp": np.linspace(2.0, 3.6, 50)}
    halfcell = [np.linspace(0, 1, 10), np.linspace(3.2, 3.5, 10), np.linspace(0, 1, 10), np.linspace(0.6, 0.1, 10)]
    ctx = {"util": mod, "util_file": str(p.resolve()), "models": {3: model}, "halfcell": halfcell,
           "extraction": {3: {"row": 3, "n_points": 42, "status": "OK"}}}
    return SimpleNamespace(mod=mod, ctx=ctx, model=model)


def _task(case=1, row=3):
    sel = {0: [1], 1: [0, 1], 5: [0, 1, 2, 3]}[case]
    return {"call_id": 7, "case": case, "row": row, "obj_selection": sel, "algorithm": e3a.algorithm_of(sel), "worker": 0}


def test_07_a_call_records_counts_extrapolation_and_actual_violation(fake):
    row = e3a.run_e3a_call(_task(), fake.ctx)
    assert row["state"] == "COMPLETED" and row["termination"] == "returned"
    assert row["n_eval"] == 3 and row["n_nonfinite"] == 1
    assert row["n_out_eval_PE"] >= 1 and row["n_out_eval_any"] >= row["n_out_eval_PE"]    # Q_exp 가 반쪽전지 구간 밖으로 나간다
    assert row["X"][0] == [0.9, 0.8, 0.2, 0.1]
    assert row["F_nonfinite_count"] == 1
    assert row["G_violation_recomputed"] == pytest.approx([0.0, 0.3001, 0.0])               # max(0, d_N − d_P + 1e-4)
    assert row["success_reported"] is True and row["success_is_evidence"] is False
    assert row["extraction"] == {"row": 3, "n_points": 42, "status": "OK"}


def test_07_missing_G_is_recorded_as_missing_not_zero(fake):
    fake.mod.MODE["kind"] = "no_G"
    row = e3a.run_e3a_call(_task(), fake.ctx)
    assert row["G"] is None and row["G_status"] == "없음"


def test_07_the_original_model_and_util_functions_are_unchanged(fake):
    before = copy.deepcopy(fake.model)
    obj, dv = fake.mod.objective_fun, fake.mod.dVdQ_hc
    e3a.run_e3a_call(_task(), fake.ctx)
    assert set(fake.model) == set(before)                                 # 그들 objective 가 쓰는 키는 사본에만
    assert fake.mod.objective_fun is obj and fake.mod.dVdQ_hc is dv       # 계수용 감싸기는 호출이 끝나면 되돌린다


def test_07_a_util_value_error_is_a_local_error_row_and_memory_error_is_structural(fake):
    fake.mod.MODE["kind"] = "value_error"
    row = e3a.run_e3a_call(_task(), fake.ctx)
    assert row["termination"] == "error" and row["error"]["kind"] == "local" and row["n_eval"] == 2
    fake.mod.MODE["kind"] = "memory"
    with pytest.raises(mon.Structural):
        e3a.run_e3a_call(_task(), fake.ctx)


def test_07_the_preserved_util_copy_runs_one_nsga2_case_on_synthetic_curves():
    from scripts import reil_c5_pilot as c5
    util, uf = c5.load_util(UTIL_COPY, c5.UTIL_COPY_SHA)
    model, halfcell = c5.synthetic_inputs(util)
    ctx = {"util": util, "util_file": uf, "models": {1: model}, "halfcell": halfcell, "extraction": {1: {"row": 1}}}
    row = e3a.run_e3a_call(_task(case=1, row=1), ctx)
    # 합성 곡선에서 그들 코드가 끝까지 도는지는 미리 알 수 없다 (그들 205 행의 빈 배열 np.max 경로 — 승인 횟수 밖 탐색 실행 0).
    # 이 시험이 고정하는 것은 실행기의 계약이다: 완주면 X · 평가 수를 기록하고, 그들 util 의 예외면 '지역' 으로 분류해 행을 남긴다.
    assert row["state"] == "COMPLETED" and row["termination"] in ("returned", "error")
    assert 0 < row["n_eval"] <= row["algorithm"]["expected_evals"] == 5000
    if row["termination"] == "returned":
        assert row["X"] is not None and np.asarray(row["X"]).shape[-1] == 4
    else:
        assert row["error"]["kind"] == "local" and row["error"]["origin"] == "util"
    print("NSGA2_SYNTHETIC_OUTCOME", row["termination"], row["n_eval"])
    assert util.objective_fun.__name__ == "objective_fun" and util.dVdQ_hc.__name__ == "dVdQ_hc"


# ======================================================================== (8) identity — 명시 인자 · 전체 MANIFEST sha
def test_08_identity_requires_the_full_manifest_sha_of_the_named_seal():
    fake_ident = lambda **kw: {"ok": True, "problems": [], "record": {"sealed": str(kw["sealed"])}, "full_c6_check": "NOT_RUN"}
    good = e3a.identity(venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, env_identity=fake_ident)
    assert good["ok"] and good["record"]["sealed"] == str(NEW_SEAL)
    assert good["full_c6_check"].startswith("CREDITED")
    bad = e3a.identity(venv="/v", seal=NEW_SEAL, manifest_sha256="0" * 64, env_identity=fake_ident)
    assert not bad["ok"] and any("MANIFEST" in p for p in bad["problems"])


def test_08_the_cli_has_no_default_seal():
    with pytest.raises(SystemExit):
        e3a.main(["identity", "--venv", "/v", "--out", "/tmp/x.json"])


# ======================================================================== (9) 계획 건조 — 최적화 호출 0 · P0 추출 기록 결속
def test_09_dryrun_writes_the_plan_without_calling_the_optimizer(tmp_path, monkeypatch):
    arrays = tmp_path / "arrays"
    e3a.seal_arrays(arrays, c6_seal=NEW_SEAL)
    fake_ident = lambda **kw: {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"}
    out = tmp_path / "dry"
    rec = e3a.dryrun(out, venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, arrays_dir=arrays,
                     util_copy=UTIL_COPY, p0_result=P0_RESULT, env_identity=fake_ident, n_workers=4)
    plan = json.loads((out / "PLAN.json").read_text(encoding="utf-8"))
    assert rec["ok"] and len(plan["calls"]) == 66 and plan["optimizer_calls"] == 0
    assert {c["row"] for c in plan["calls"]} == set(range(11))
    assert all(c["extraction"]["status"] == "OK" and c["extraction"]["row"] == c["row"] for c in plan["calls"])
    assert plan["util_copy_sha256"] == "bdf78273d50f40ce3154d01a3ef8d36f0f5ea5ec1b04539584809d7b19b46f9c"


def test_09_data_paths_are_refused():
    with pytest.raises(e3a.E3aStop):
        e3a.dryrun(Path("/tmp/never"), venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST,
                   arrays_dir=Path("/tmp/none"), util_copy=Path("/x/LFP_Data.xlsx"), p0_result=P0_RESULT,
                   env_identity=lambda **kw: {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"})
