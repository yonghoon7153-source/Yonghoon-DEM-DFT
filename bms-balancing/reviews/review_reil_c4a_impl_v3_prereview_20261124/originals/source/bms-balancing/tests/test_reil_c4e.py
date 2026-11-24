"""REIL C4-E · E0 — 실행 진입점 (fetch · plan-e · run) · 감시 stop_rule · 호출당 상한 · 비용 투영 · 판정 · 기록의 대조 21 ID (v3 §5).

승인: 상태 문서 §66 (사용자 "권고대로 E0 승인") · 요청 `docs/REIL_C4E_APPROVAL_REQUEST_v3_20261014.md` (29cd92a4… · 수용 §65).
RED 예상 (v3 §6-1 3): 21 모두 실패 — 새 모듈 골격의 NotImplementedError, 또는 감시에 stop_rule 인자가 없어서 나는 TypeError 뿐.
매개변수화 없음 — 하위 사례 (r_6 의 (a)(b)(c) · s_3 의 (a)–(g) 등) 는 같은 시험 안에서 단언한다.

합성 입력 · 가짜 util · 가짜 로컬 git 저장소 (tmp) 만 쓴다. REIL xlsx · pkl · 노트북 · 네트워크 · 실제 optimizer (pymoo · COBYQA) · 보존 util
사본 · Sobol 생성은 0 이다. 실제 fork 세션은 m_1 1 · r_6 (a)(b) 2 · s_4 2 = 5 (세션 공유 없음 · m_2 는 모사 Process · r_6 (c) · s_3 은 fork 없음).
가짜 util 평가는 s_4 두 변형의 198 + 198 (호출당 3) 이 전부다 (≤ 2,000).
"""
import copy
import hashlib
import importlib.machinery
import importlib.util
import inspect
import json
import math
import queue
import socket
import subprocess
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import reil_c4_e3a as e3a
from scripts import reil_c4_monitor as mon
from scripts import reil_c4e_run as run
from scripts import reil_c5_pilot as c5

BMS = Path(__file__).resolve().parents[1]
REPO = BMS.parent
NEW_SEAL = BMS / "reil_c6_rebuild_20261013"
NEW_SEAL_MANIFEST = "4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc"
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
LIM = {"measure": 30.0, "grace": 3.0, "rss": 10 ** 12, "rss_gap": 5.0, "disk_new": 10 ** 12, "disk_free": 0, "disk_gap": 15.0}
STEP = 0.0078125                                  # 2^-7 — 가짜 시계의 한 호출 간격 (이진 정확)

#: C4-0a 기록 필드 — `e3a.run_e3a_call` 의 returned 행 (계획 7 · 계수 10 · 기록 7 · 결과 12 · 시간 3) + 감시 `_states` 의 t_start_rel
C4_0A_FIELDS = ("task_id", "call_id", "case", "row", "obj_selection", "algorithm", "worker",
                "n_eval", "n_nonfinite", "n_nonfinite_any_of_4", "n_out_eval_PE", "n_out_eval_NE", "n_out_eval_any",
                "n_out_unknown_eval", "n_dvdq_observed", "n_eval_x_out_of_box", "n_eval_G_violated",
                "extraction", "model_digest", "halfcell_digest", "warnings_count", "warnings_distinct_overflow",
                "success_is_evidence", "n_eval_minus_expected",
                "termination", "error", "X", "F", "G", "G_status", "n_solutions", "F_nonfinite_count", "G_violation_recomputed",
                "G_violation_exact", "box_violation_exact", "success_reported",
                "wall", "cpu", "state", "t_start_rel")


# ======================================================================== 공통 도우미
def _fake_ident(**kw):
    return {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"}


def _sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _has_xfg_key(o) -> bool:
    if isinstance(o, dict):
        return any(k in ("X", "F", "G") or _has_xfg_key(v) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return any(_has_xfg_key(v) for v in o)
    return False


class _ListQueue:
    def __init__(self):
        self.items = []

    def put(self, item):
        self.items.append(item)


class _SetStop:
    def is_set(self):
        return True


def _sleep_task(task, ctx, notify=None, progress=None):
    time.sleep(task.get("s", 0.02))
    return {"task_id": task["task_id"], "value": task["task_id"] * 2}


def _timed_task(task, ctx, notify=None, progress=None):
    """r_6 의 fork 작업 — wall 을 주면 그 값을 행에 적는다 (tick 사이 늦은 완료의 모사 · 계수는 1)."""
    t = time.monotonic()
    time.sleep(task.get("s", 0.01))
    if progress is not None:
        progress(1)
    return {"task_id": task["task_id"], "termination": "returned", "n_eval": 1, "state": "COMPLETED",
            "wall": task["wall"] if "wall" in task else time.monotonic() - t}


def _plan(n, n_workers, expected=1, **extra):
    return [{"task_id": i, "worker": i % n_workers, "algorithm": {"expected_evals": expected}, **extra} for i in range(n)]


def _snap(plan, now, started, done, progress=None):
    return {"now_rel": float(now), "started": dict(started), "done": copy.deepcopy(done),
            "progress": {t["task_id"]: (progress or {}).get(t["task_id"], 0) for t in plan}, "planned": [t["task_id"] for t in plan]}


def _cost_snap(plan, now):
    """r_2 · r_3 · r_5 의 비용 snapshot — 작업자 2 · 계획 12 (기대 평가 각 1,000).
    returned 0–7: c = wall / n_eval = 0.5 · 1.5 · 1.0 · 4.0 · 2.0 · 3.5 · 2.5 · 3.0 (위쪽 중앙 = 정렬 index 4 = 2.5) · 8 = error (표본 밖) ·
    9 = 진행 중 (작업자 1 · progress 400 → 남은 600) · 10 · 11 = 미착수 (작업자 0 · 1).
    남은 기대 평가: 작업자 0 = 1,000 · 작업자 1 = 600 + 1,000 = 1,600 → R = 2,500 · 4,000.
    시작 상대 시각은 now − 100 s — 진행 중 경과 100 s 로 호출당 상한 (1,800 s) 에 걸리지 않게 둔다 (비용 경로만 본다)."""
    walls = [1.0, 3.0, 2.0, 8.0, 4.0, 7.0, 5.0, 6.0]
    done = {i: {"wall": w, "n_eval": 2, "termination": "returned"} for i, w in enumerate(walls)}
    done[8] = {"wall": 100.0, "n_eval": 1, "termination": "error"}
    return _snap(plan, now, {i: float(now) - 100.0 for i in range(10)}, done, progress={9: 400})


def _good_row(t, wall=1.0):
    row = {k: None for k in C4_0A_FIELDS}
    row.update({k: t[k] for k in ("task_id", "call_id", "case", "row", "obj_selection", "algorithm", "worker")})
    row.update(n_eval=3, termination="returned", state="COMPLETED", wall=wall, cpu=wall, t_start_rel=1.0, X=[[0.9, 0.8, 0.2, 0.1]],
               F=[[0.1]], G=[[-0.1]], G_status="보고됨", success_is_evidence=False)
    return row


def _sup(states, n_workers=4, **kw):
    s = {"states": states, "global_stop": None, "structural": [], "samples": {"rss": [], "disk": []},
         "workers": {w: {"pid": 1, "t": 0.0} for w in range(n_workers)}, "worker_end": {w: {"t": 1.0} for w in range(n_workers)},
         "worker_deadline": {}, "exitcodes": {w: 0 for w in range(n_workers)}, "owned_alive_after": 0, "drain_ok": True,
         "t_stop": 10.0, "deadline_rel": 9000.0}
    s.update(kw)
    return s


class _Clk:
    """가짜 시계 — 부를 때마다 현재 값을 내고 step 만큼 나아간다."""

    def __init__(self, t, step):
        self.t, self.step = float(t), float(step)

    def __call__(self):
        v = self.t
        self.t += self.step
        return v


# ---- 모사 Process (0a 보완 n3 의 방식 — target 을 부르지 않는다 · 실제 프로세스 0)
class _FakeQueue:
    def __init__(self):
        self.items = []

    def put(self, item):
        self.items.append(item)

    def get(self, timeout=None):
        if self.items:
            return self.items.pop(0)
        raise queue.Empty


class _FakeEvent:
    def __init__(self):
        self.flag = False

    def set(self):
        self.flag = True

    def is_set(self):
        return self.flag


class _ScriptedProc:
    def __init__(self, script, target=None, args=(), daemon=None):
        self.wid, self.q, self.script = args[0], args[4], script
        self.pid, self.exitcode = None, None

    def start(self):
        self.pid = 4_100_000 + self.wid
        for item in self.script[self.wid]:
            self.q.put(item)
        self.exitcode = 0

    def is_alive(self):
        return False

    def terminate(self):
        pass

    def join(self, timeout=None):
        pass

    def kill(self):
        pass


class _ScriptedCtx:
    def __init__(self, script):
        self.script = script

    def Queue(self):
        return _FakeQueue()

    def Event(self):
        return _FakeEvent()

    def Array(self, typecode, n, lock=False):
        return [0] * n

    def Process(self, target=None, args=(), daemon=None):
        return _ScriptedProc(self.script, target=target, args=args, daemon=daemon)


# ---- 가짜 util (그들 함수 이름 · 인자 꼴만 같다 · 최상위는 import · 함수 · 메서드만 있는 클래스 — P0 의 util 정적 검사 규칙)
FAKE_UTIL = '''"""가짜 util (C4-E E0 대조) — 자료 파일을 열지 않고 시트 이름으로 곡선을 만든다 (REIL 자료 아님)."""
import numpy as np


class Result:
    """optimizer 반환 꼴 (X · F · G · success)."""

    def __init__(self, X, F, G):
        self.X, self.F, self.G, self.success = X, F, G, True


class SheetData(list):
    """셀별 [Q; V] 배열 목록 — 시트 이름을 붙인다."""


def _mode():
    return "MODE_TOKEN"


def _curve(sheet_name, n_cells):
    k = (sum(ord(c) for c in sheet_name) % 89) / 89.0
    g = 1.5 if "Graphite" in sheet_name else 1.0
    out = SheetData()
    for cell in range(n_cells):
        n = 40 + int(20 * k) + cell
        q = np.linspace(0.0, (2.0 + k + 0.1 * cell) * g, n)
        v = 3.0 + 0.4 * np.sqrt(q / q[-1]) + 0.01 * cell
        out.append(np.vstack([q, v]))
    out.sheet = sheet_name
    return out


def visualize_LFP_data(data_file, sheet_name, step_idx, visualize=True):
    return _curve(sheet_name, 2)


def extract_battery_data(data, idx):
    a = data[idx]
    q, v = np.asarray(a[0], dtype=float), np.asarray(a[1], dtype=float)
    qi = np.linspace(q[0], q[-1], 30)
    vi = np.interp(qi, q, v)
    return {"Q_exp": q, "V_exp": v, "Q_exp_max": float(np.max(q)), "Q_exp_interp": qi, "V_exp_interp": vi,
            "dVdQ_exp_interp": np.gradient(vi, qi), "sheet": getattr(data, "sheet", None)}


def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
    q = np.linspace(0.0, 1.0, interp_len)
    return (q * m_P - d_P, q * m_N - d_N, None, None, None, None, None, None)


def objective_fun(x, Model, halfcell):
    dVdQ_hc(halfcell[1], halfcell[0], halfcell[3], halfcell[2], *x, interp_len=20)
    return np.array([0.1, float(np.sum(np.asarray(x) ** 2)), 0.2, 0.3])


def run_optimization(Model, halfcell, obj_selection, pop_size=50):
    if _mode() == "local_error" and Model.get("sheet") == "12-LFP 16-Gr SOC-100" and list(obj_selection) == [2, 3]:
        np.max(np.array([]))
    xs = [np.array([0.9, 0.8, 0.2, 0.1]), np.array([1.0, 1.0, 0.1, 0.4]), np.array([0.7, 0.6, 0.3, 0.2])]
    fs = [objective_fun(x, Model, halfcell)[list(obj_selection)] for x in xs]
    if len(obj_selection) == 1:
        X = np.array([xs[0]] * 20)
        F = np.array([[fs[0][0]]] * 20)
    else:
        X = np.array(xs)
        F = np.array(fs)
    G = np.array([[x[3] - x[2] + 1e-4] for x in X])
    return Result(X, F, G)
'''


def _fake_util(d, mode):
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"util_LFP_fake_{mode}.py"
    p.write_text(FAKE_UTIL.replace("MODE_TOKEN", mode), encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader(f"fake_util_c4e_{mode}_{d.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod, p, _sha_file(p)


def _fake_p0(loaded):
    ext = ([dict(r, kind="reference", status="OK") for r in loaded["references"]]
           + [dict(r, kind="analysis", status="OK") for r in loaded["rows"]])
    return {"extraction": ext, "max_q": {"float": loaded["PE"]["max_q"], "n_q_PE_hc": loaded["PE"]["n_q_PE_hc"], "status": "OK"},
            "q_NE_hc_max_record_only": loaded["NE"]["q_NE_hc_max_record_only"], "notebook_check": {"ok": True}}


def _write_p0(d, obj):
    d.mkdir(parents=True, exist_ok=True)
    p = d / "P0_RESULT.json"
    p.write_bytes((json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8"))
    return p, _sha_file(p)


def _expected(xlsx, util_p, p0_sha):
    return {"LFP_Data.xlsx": {"sha256": _sha_file(xlsx), "bytes": Path(xlsx).stat().st_size},
            "util_LFP.py": {"sha256": _sha_file(util_p), "bytes": Path(util_p).stat().st_size},
            "P0_RESULT.json": {"sha256": p0_sha}}


def _git(cwd, *args):
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, (args, r.stderr[-500:])
    return r.stdout


# ======================================================================== m — 감시의 선택 인자 stop_rule
def test_m_1_a_rule_reason_is_a_global_stop_with_three_states():
    """[RED 실패 — TypeError: 지금 supervise 에 stop_rule 인자가 없다] (fork 세션 1) 규칙이 사유를 돌려주면 그 원문이 전역 중지 사유 ·
    완료 · 착수 뒤 중단 · 미착수 세 상태 · 기본값 None (기존 동작은 기존 감시 시험이 근거)."""
    seen = []

    def rule(snap):
        seen.append(snap)
        active = set(snap["started"]) - set(snap["done"])
        return "규칙 중지 — 시험 사유 원문" if len(snap["done"]) >= 2 and active else None

    tasks = [{"task_id": i, "worker": i % 2, "s": (0.02 if i < 2 else 4.0)} for i in range(8)]
    out = mon.supervise(tasks, {}, _sleep_task, n_workers=2, limits=dict(LIM), t0=time.monotonic(), rss_fn=lambda p: 1000,
                        disk_fn=lambda r: (0, 10 ** 12), out_roots=[], tick=0.05, disk_every=0.05, stop_rule=rule)
    assert out["global_stop"] == "규칙 중지 — 시험 사유 원문"
    assert {s["state"] for s in out["states"]} == {"COMPLETED", "STARTED_INTERRUPTED", "NOT_STARTED"}
    assert out["structural"] == [] and out["owned_alive_after"] == 0 and seen
    assert inspect.signature(mon.supervise).parameters["stop_rule"].default is None


def test_m_2_snapshot_coordinates_and_rule_exception_without_a_process(monkeypatch):
    """[RED 실패 — TypeError (stop_rule 인자 없음)] 모사 Process · 0 이 아닌 t0 · 가짜 clock: now_rel = clock − t0 · started = start.t − t0 ·
    내용은 v3 §3 의 키뿐 (완료 행은 wall · n_eval · termination — X · F · G 없음) · 규칙 예외 → 우리 구조 오류 (사유 원문)."""
    import multiprocessing
    done0 = {"task_id": 0, "wall": 0.5, "n_eval": 2, "termination": "returned", "X": [[0.9, 0.8, 0.2, 0.1]], "F": [[0.1]],
             "G": [[-0.1]], "state": "COMPLETED"}
    done1 = dict(done0, task_id=1, wall=0.25, n_eval=4)
    script = {0: [("worker_start", 0, {"pid": 1, "t": 5000.5}), ("start", 0, {"worker": 0, "t": 5001.0}), ("done", 0, done0),
                  ("start", 1, {"worker": 0, "t": 5002.5}), ("done", 1, done1), ("worker_end", 0, {"t": 5003.0})]}
    monkeypatch.setattr(multiprocessing, "get_context", lambda method=None: _ScriptedCtx(script))
    clk = {"t": 5000.0}

    def rss(pids):
        clk["t"] += 0.25
        return 1000

    seen = []

    def capture(snap):
        seen.append((clk["t"], copy.deepcopy(snap)))
        return None

    tasks = [{"task_id": 0, "worker": 0}, {"task_id": 1, "worker": 0}]
    kw = dict(n_workers=1, limits=dict(LIM), t0=5000.0, clock=lambda: clk["t"], rss_fn=rss, disk_fn=lambda r: (0, 10 ** 12),
              out_roots=[], tick=0.0, disk_every=0.0)
    out = mon.supervise(tasks, {}, None, stop_rule=capture, **kw)
    assert out["global_stop"] is None and seen
    for t, s in seen:
        assert set(s) == {"now_rel", "started", "done", "progress", "planned"}
        assert s["now_rel"] == t - 5000.0
        assert s["planned"] == [0, 1] and s["progress"] == {0: 0, 1: 0}
        assert all(set(d) == {"wall", "n_eval", "termination"} for d in s["done"].values())
    last = seen[-1][1]
    assert last["started"] == {0: 1.0, 1: 2.5}
    assert last["done"] == {0: {"wall": 0.5, "n_eval": 2, "termination": "returned"},
                            1: {"wall": 0.25, "n_eval": 4, "termination": "returned"}}

    def boom(snap):
        raise ValueError("규칙 내부 오류 — 시험")

    clk["t"] = 5000.0
    out2 = mon.supervise(tasks, {}, None, stop_rule=boom, **kw)
    assert out2["global_stop"] is not None and "구조 오류" in out2["global_stop"] and "규칙 내부 오류 — 시험" in out2["global_stop"]
    s = out2["structural"][-1]
    assert (s["origin"], s["stage"], s["type"], s["message"]) == ("ours", "stop_rule", "ValueError", "규칙 내부 오류 — 시험")
    clk["t"] = 5000.0
    out3 = mon.supervise(tasks, {}, None, stop_rule=lambda snap: 1, **kw)          # 문자열 · None 이 아닌 반환 = 형식 오류
    assert out3["global_stop"] is not None and out3["structural"][-1]["stage"] == "stop_rule"


# ======================================================================== r — 규칙 (호출당 상한 · 비용 투영 · 입력 검증 · 원시 근거)
def test_r_1_call_cap_active_late_between_samples_equal_and_reason():
    """[RED 실패 — NotImplementedError] 순수 함수: 진행 중 초과 · 표본 사이 늦은 완료 (직전 1,799.5 → wall 1,800.2) · 같음 (1,800.0) 은
    넘지 않음 (엄격한 >) · 사유 문구 (늦은 완료를 먼저)."""
    plan = _plan(4, 2)
    s1 = _snap(plan, now=1899.5, started={0: 100.0, 1: 200.0}, done={})
    assert run.call_cap(s1, 1800.0)["reason"] is None
    s2 = _snap(plan, now=1900.5, started={0: 100.0, 1: 200.0}, done={0: {"wall": 1800.2, "n_eval": 5, "termination": "returned"}})
    r2 = run.call_cap(s2, 1800.0)
    assert [x["task_id"] for x in r2["late"]] == [0] and r2["active_over"] == []
    assert "호출당 상한 (늦은 완료 · 0:" in r2["reason"]
    s3 = _snap(plan, now=1900.0, started={0: 100.0}, done={})
    assert run.call_cap(s3, 1800.0)["reason"] is None
    s4 = _snap(plan, now=1900.0, started={0: 100.0}, done={0: {"wall": 1800.0, "n_eval": 1, "termination": "returned"}})
    assert run.call_cap(s4, 1800.0)["reason"] is None
    s5 = _snap(plan, now=2000.25, started={0: 100.0, 1: 150.0}, done={1: {"wall": 1850.0, "n_eval": 2, "termination": "error"}})
    r5 = run.call_cap(s5, 1800.0)
    assert [(x["task_id"], x["elapsed_observed"], x["detected_rel"]) for x in r5["active_over"]] == [(0, 1900.25, 2000.25)]
    assert [x["task_id"] for x in r5["late"]] == [1]
    assert "호출당 상한 (진행 중 · 0:" in r5["reason"] and r5["reason"].index("늦은 완료") < r5["reason"].index("진행 중")


def test_r_2_cost_projection_upper_median_returned_only_minimum_eight_and_boundary():
    """[RED 실패 — NotImplementedError] 순수 함수: 위쪽 중앙 순서통계 · returned 만 · 7 이면 판정 없음 · 8 번째부터 · 작업자별 투영
    (진행 중의 progress 반영 · 음수 없음) · 경계 같음 / 넘음."""
    plan = _plan(12, 2, expected=1000)
    rec = run.cost_projection(_cost_snap(plan, 5000.0), plan, min_samples=8, measure=9000.0)
    assert rec["judged"] is True and rec["n_samples"] == 8 and rec["returned_ids"] == list(range(8))
    assert rec["m"] == 2.5 and [s["c"] for s in rec["samples"]] == [0.5, 1.5, 1.0, 4.0, 2.0, 3.5, 2.5, 3.0]
    assert rec["remaining_expected_evals"] == {"0": 1000, "1": 1600} and rec["R"] == {"0": 2500.0, "1": 4000.0}
    assert rec["value"] == 9000.0 and rec["stop"] is False and rec["reason"] is None
    over = run.cost_projection(_cost_snap(plan, 5000.5), plan, min_samples=8, measure=9000.0)
    assert over["stop"] is True and over["value"] == 9000.5 and over["reason"].startswith(run.COST_REASON)
    seven = _cost_snap(plan, 8999.0)
    del seven["done"][7]
    rec7 = run.cost_projection(seven, plan, min_samples=8, measure=9000.0)
    assert rec7["judged"] is False and rec7["stop"] is False and rec7["m"] is None and rec7["n_samples"] == 7
    ahead = _cost_snap(plan, 5000.5)
    ahead["progress"][9] = 1500                                          # 진행 수가 기대 평가를 넘어도 남은 몫은 0 (음수 없음)
    rec_a = run.cost_projection(ahead, plan, min_samples=8, measure=9000.0)
    assert rec_a["remaining_expected_evals"] == {"0": 1000, "1": 1000} and rec_a["stop"] is False


def test_r_3_the_rule_never_reads_result_values():
    """[RED 실패 — NotImplementedError] 접근하면 예외인 X · F · G 를 완료 행에 넣어도 판정 · 기록이 같다 (규칙은 결과값 0)."""
    plan = _plan(12, 2, expected=1000)

    class _Trap(dict):
        def __getitem__(self, k):
            if k in ("X", "F", "G"):
                raise AssertionError(f"결과값 {k} 를 읽었다")
            return super().__getitem__(k)

        def get(self, k, default=None):
            if k in ("X", "F", "G"):
                raise AssertionError(f"결과값 {k} 를 읽었다")
            return super().get(k, default)

        def items(self):
            raise AssertionError("완료 행 전체를 훑었다")

        def values(self):
            raise AssertionError("완료 행 전체를 훑었다")

    snap = _cost_snap(plan, 5000.5)
    trapped = copy.deepcopy(snap)
    trapped["done"] = {tid: _Trap(d, X=[[1.0, 1.0, 0.1, 0.2]], F=[[0.1]], G=[[0.0]]) for tid, d in snap["done"].items()}
    plain, trap = run.StopRule(plan), run.StopRule(plan)
    r_plain, r_trap = plain(copy.deepcopy(snap)), trap(trapped)
    assert r_plain is not None and r_plain == r_trap
    assert plain.record() == trap.record()


def test_r_4_rule_input_validation_raises_instead_of_dropping_or_zero_filling():
    """[RED 실패 — NotImplementedError] wall NaN · 음수 · n_eval 0 · 정수 아님 · progress 음수 · 계획 밖 ID · done ⊄ started · 모르는
    termination → 예외 (표본을 빼거나 0 으로 채우지 않는다)."""
    plan = _plan(3, 1)
    base = _snap(plan, now=10.0, started={0: 1.0, 1: 2.0}, done={0: {"wall": 1.0, "n_eval": 2, "termination": "returned"}},
                 progress={1: 3})
    assert run.StopRule(plan)(copy.deepcopy(base)) is None
    muts = [lambda s: s["done"][0].update(wall=float("nan")),
            lambda s: s["done"][0].update(wall=-0.5),
            lambda s: s["done"][0].update(n_eval=0),
            lambda s: s["done"][0].update(n_eval=2.5),
            lambda s: s["done"][0].update(n_eval=True),
            lambda s: s["progress"].update({1: -1}),
            lambda s: s["started"].update({99: 3.0}),
            lambda s: s["done"].update({1: {"wall": 1.0, "n_eval": 1, "termination": "returned"}}) or s["started"].pop(1),
            lambda s: s["done"][0].update(termination="finished")]
    for mut in muts:
        s = copy.deepcopy(base)
        mut(s)
        with pytest.raises(run.RuleInputError):
            run.StopRule(plan)(s)
    assert issubclass(run.RuleInputError, ValueError)


def test_r_5_judgment_raw_basis_has_every_key_and_no_result_values():
    """[RED 실패 — NotImplementedError] 중지 판정과 마지막 판정의 기록 키 (v3 §4-3: 상대 시각 · returned ID · 표본 수 · 각 wall / n_eval · m ·
    작업자별 남은 기대 평가 · R_w · 판정값 · 경계 · 사유) 가 모두 있고 X · F · G 키가 없다."""
    plan = _plan(12, 2, expected=1000)
    keys = {"now_rel", "returned_ids", "n_samples", "samples", "m", "remaining_expected_evals", "R", "value", "boundary", "reason",
            "judged", "stop"}
    go = run.StopRule(plan)
    assert go(_cost_snap(plan, 5000.0)) is None
    rec_go = go.record()
    assert keys <= set(rec_go["last"]) and rec_go["stop"] is None and rec_go["last"]["judged"] is True
    st = run.StopRule(plan)
    reason = st(_cost_snap(plan, 5000.5))
    assert reason is not None and reason.startswith(run.COST_REASON)
    rec = st.record()
    assert keys <= set(rec["stop"]) and rec["stop"]["kind"] == "cost" and rec["stop"]["reason"] == reason
    assert all(set(s) == {"task_id", "wall", "n_eval", "c"} for s in rec["stop"]["samples"])
    assert not _has_xfg_key(rec) and not _has_xfg_key(rec_go)


def test_r_6_call_cap_three_paths_fork_fork_and_pure_final_drain():
    """[RED 실패 — NotImplementedError] (a) fork: 진행 중 초과 → 중단 요청 대상 → 최종 drain 에 done 없음 → STARTED_INTERRUPTED.
    (b) fork: tick 사이 늦은 완료 → 다음 tick 전역 중지 · 반환 행 보존 · 늦은 완료 목록 · INCOMPLETE.
    (c) 순수 집계 fixture (fork 없음 · C4E-N3-FINAL-DRAIN): 진행 중 초과 감지 → 중지 요청 → 마지막 drain 에서만 done (returned · error) →
    원래 COMPLETED · termination 보존 · 초과 기록 · global_stop 유지 · 상한 넘은 wall 은 늦은 완료 목록에도 · INCOMPLETE."""
    kw = dict(n_workers=1, limits=dict(LIM), rss_fn=lambda p: 1000, disk_fn=lambda r: (0, 10 ** 12), out_roots=[], tick=0.05,
              disk_every=0.05)
    # (a)
    plan_a = [{"task_id": 0, "worker": 0, "algorithm": {"expected_evals": 1}, "s": 6.0},
              {"task_id": 1, "worker": 0, "algorithm": {"expected_evals": 1}, "s": 0.01}]
    rule_a = run.StopRule(plan_a, cap=0.4)
    out_a = mon.supervise(plan_a, {}, _timed_task, t0=time.monotonic(), stop_rule=rule_a, **kw)
    assert out_a["global_stop"] is not None and "호출당 상한 (진행 중 · 0:" in out_a["global_stop"]
    st_a = {s["task_id"]: s for s in out_a["states"]}
    assert st_a[0]["state"] == "STARTED_INTERRUPTED" and st_a[1]["state"] == "NOT_STARTED" and out_a["owned_alive_after"] == 0
    agg_a = run.aggregate(out_a, plan_a, rule_a)
    assert [(o["task_id"], o["final_state"]) for o in agg_a["over_cap_active"]] == [(0, "STARTED_INTERRUPTED")]
    assert agg_a["over_cap_active"][0]["elapsed_observed"] > 0.4 and agg_a["late_completions"] == []
    assert run.pre_verdict(plan_a, agg_a, out_a, {}, {}, n_workers=1)["complete"] is False
    # (b)
    plan_b = [{"task_id": 0, "worker": 0, "algorithm": {"expected_evals": 1}, "s": 0.05, "wall": 1.25},
              {"task_id": 1, "worker": 0, "algorithm": {"expected_evals": 1}, "s": 5.0}]
    rule_b = run.StopRule(plan_b, cap=1.0)
    out_b = mon.supervise(plan_b, {}, _timed_task, t0=time.monotonic(), stop_rule=rule_b, **kw)
    assert out_b["global_stop"] is not None and "호출당 상한 (늦은 완료 · 0:" in out_b["global_stop"]
    st_b = {s["task_id"]: s for s in out_b["states"]}
    assert (st_b[0]["state"], st_b[0]["termination"], st_b[0]["wall"]) == ("COMPLETED", "returned", 1.25)
    assert st_b[1]["state"] in ("STARTED_INTERRUPTED", "NOT_STARTED") and out_b["owned_alive_after"] == 0
    agg_b = run.aggregate(out_b, plan_b, rule_b)
    assert [x["task_id"] for x in agg_b["late_completions"]] == [0]
    assert run.pre_verdict(plan_b, agg_b, out_b, {}, {}, n_workers=1)["complete"] is False
    # (c)
    for term in ("returned", "error"):
        plan_c = _plan(3, 1)
        rule_c = run.StopRule(plan_c, cap=10.0)
        reason = rule_c(_snap(plan_c, now=25.0, started={0: 1.0, 1: 2.0},
                              done={0: {"wall": 3.0, "n_eval": 2, "termination": "returned"}}))
        assert reason is not None and "호출당 상한 (진행 중 · 1:" in reason
        states = [{"task_id": 0, "worker": 0, "state": "COMPLETED", "termination": "returned", "wall": 3.0, "n_eval": 2,
                   "t_start_rel": 1.0},
                  {"task_id": 1, "worker": 0, "state": "COMPLETED", "termination": term, "wall": 24.5, "n_eval": 3, "t_start_rel": 2.0},
                  {"task_id": 2, "worker": 0, "state": "NOT_STARTED", "t_start_rel": None}]
        sup = _sup(copy.deepcopy(states), n_workers=1, global_stop=reason)
        agg = run.aggregate(sup, plan_c, rule_c)
        assert sup["states"] == states                                            # 사후 집계는 행을 바꾸지 않는다
        assert [(o["task_id"], o["final_state"], o["termination"]) for o in agg["over_cap_active"]] == [(1, "COMPLETED", term)]
        assert agg["global_stop"] == reason and [x["task_id"] for x in agg["late_completions"]] == [1]
        assert agg["observed"]["COMPLETED_" + term] >= 1
        assert run.pre_verdict(plan_c, agg, sup, {}, {}, n_workers=1)["complete"] is False


# ======================================================================== t — 원점 · 마감 · 신규 시작
def test_t_1_nonzero_origin_prep_boundary_relative_deadline_and_no_start_after_stop(tmp_path):
    """[RED 실패 — NotImplementedError] 0 이 아닌 run 원점 (가짜 clock): prep 초과 → 작업자 시작 0 · 측정 마감 = 원점 + 9,000 s (상대) ·
    중지 신호 뒤 신규 시작 0."""
    class _Halt(Exception):
        pass

    calls = []

    def spy(tasks, ctx, task_fn, **kw):
        calls.append((task_fn, kw))
        raise _Halt()

    prep = {"out": tmp_path / "o", "plan": e3a.plan_calls(4), "ctx": {}, "files": {}, "expected": {}, "id_start": {}, "header": {}}
    with pytest.raises(run.E3aStop):
        run.execute(prep, t0=5000.0, clock=lambda: 5000.0 + 900.5, supervise=spy)
    assert calls == []
    with pytest.raises(_Halt):
        run.execute(prep, t0=5000.0, clock=lambda: 5000.0 + 900.0, supervise=spy)
    fn, kw = calls[0]
    assert fn is e3a.run_e3a_call and kw["t0"] == 5000.0 and kw["limits"]["measure"] == 9000.0
    assert kw["t0"] + kw["limits"]["measure"] == 14000.0
    assert isinstance(kw["stop_rule"], run.StopRule) and kw["n_workers"] == 4 and kw["out_roots"] == [tmp_path / "o"]
    q = _ListQueue()
    mon.worker_loop(0, [{"task_id": 0, "worker": 0}, {"task_id": 1, "worker": 0}], {}, _sleep_task, q, _SetStop(), {},
                    deadline_abs=time.monotonic() + 60)
    assert "start" not in [k for k, _, _ in q.items]


# ======================================================================== d — 자료 결속 · 경로 · fetch · 식별
def test_d_1_prepare_order_stops_before_later_steps(tmp_path, monkeypatch):
    """[RED 실패 — NotImplementedError] identity → 원천 · 입력 sha → 경로 → util import → 적재. 앞에서 어긋나면 뒤 (util import · 가짜
    util 의 적재 함수) 는 불리지 않고 출력 폴더도 만들지 않는다."""
    mod, util_p, _ = _fake_util(tmp_path / "u", "ok")
    xlsx = tmp_path / "LFP_Data.xlsx"
    xlsx.write_bytes(b"fake workbook path - never opened")
    loaded = run.load_inputs(mod, xlsx)
    p0_p, p0_sha = _write_p0(tmp_path / "p0", _fake_p0(loaded))
    exp = _expected(xlsx, util_p, p0_sha)
    order = []
    real_table, real_paths = run.identity_table, run.check_paths
    monkeypatch.setattr(run, "identity_table", lambda *a, **k: (order.append("sha"), real_table(*a, **k))[1])
    monkeypatch.setattr(run, "check_paths", lambda **k: (order.append("paths"), real_paths(**k))[1])

    def ident_ok(**kw):
        order.append("identity")
        return _fake_ident()

    def ident_bad(**kw):
        order.append("identity")
        return {"ok": False, "problems": ["시험 — identity 실패"], "record": {}, "full_c6_check": "NOT_RUN"}

    def spy_load(path, sha):
        order.append("util")
        m, uf = c5.load_util(path, sha)
        real_vis = m.visualize_LFP_data

        def vis(*a, **k):
            order.append("load")
            return real_vis(*a, **k)
        m.visualize_LFP_data = vis
        return m, uf

    base = dict(venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, xlsx=xlsx, util_path=util_p, p0_result=p0_p,
                load_util=spy_load)
    with pytest.raises(run.E3aStop):
        run.prepare(out=tmp_path / "o_a", expected=exp, env_identity=ident_bad, **base)
    assert order == ["identity"] and not (tmp_path / "o_a").exists()
    order.clear()
    with pytest.raises(run.E3aStop):
        run.prepare(out=tmp_path / "o_b", expected=dict(exp, **{"P0_RESULT.json": {"sha256": "0" * 64}}), env_identity=ident_ok, **base)
    assert order == ["identity", "sha"] and not (tmp_path / "o_b").exists()
    order.clear()
    pkl = tmp_path / "util_LFP.pkl"
    pkl.write_bytes(util_p.read_bytes())
    with pytest.raises(run.E3aStop):
        run.prepare(out=tmp_path / "o_c", expected=exp, env_identity=ident_ok, **dict(base, util_path=pkl))
    assert order == ["identity", "sha", "paths"] and not (tmp_path / "o_c").exists()
    order.clear()
    prep = run.prepare(out=tmp_path / "o_d", expected=exp, env_identity=ident_ok, **base)
    assert order == ["identity", "sha", "paths", "util"] + ["load"] * 13
    assert (tmp_path / "o_d").is_dir() and len(prep["plan"]) == 66 and sorted(prep["ctx"]["models"]) == list(range(11))


def test_d_2_exact_p0_binding_or_stop_before_any_optimizer(tmp_path):
    """[RED 실패 — NotImplementedError] 11 행 · reference 둘 · PE max_q / 길이 · NE 최대가 정확 일치면 통과. 어느 한 값 (NE 포함) 이 1 ulp
    달라도 E3aStop · optimizer 0."""
    mod, util_p, _ = _fake_util(tmp_path / "u", "ok")
    xlsx = tmp_path / "LFP_Data.xlsx"
    xlsx.write_bytes(b"fake")
    loaded = run.load_inputs(mod, xlsx)
    good = _fake_p0(loaded)
    assert run.binding_problems(loaded, good) == []
    opt = []

    def counting_load(path, sha):
        m, uf = c5.load_util(path, sha)
        real = m.run_optimization
        m.run_optimization = lambda *a, **k: (opt.append(1), real(*a, **k))[1]
        return m, uf

    def attempt(p0d, name):
        p, s = _write_p0(tmp_path / name, p0d)
        return run.prepare(venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, xlsx=xlsx, util_path=util_p,
                           out=tmp_path / name / "out", p0_result=p, expected=_expected(xlsx, util_p, s), env_identity=_fake_ident,
                           load_util=counting_load)

    prep = attempt(good, "good")
    assert prep["header"]["binding"]["equal"] is True

    def bump(x):
        return math.nextafter(x, math.inf)

    cases = []
    for key in ("n_points", "V_first", "V_last", "Q_first", "Q_exp_max"):
        d = copy.deepcopy(good)
        e = [x for x in d["extraction"] if x.get("kind") == "analysis" and x["row"] == 4][0]
        e[key] = e[key] + 1 if key == "n_points" else bump(e[key])
        cases.append((f"row_{key}", d))
    for key in ("n_points", "V_first", "V_last", "Q_first", "Q_last"):
        d = copy.deepcopy(good)
        e = [x for x in d["extraction"] if x.get("kind") == "reference" and x["sheet"] == c5.p0.SHEETS_REF[1]][0]
        e[key] = e[key] + 1 if key == "n_points" else bump(e[key])
        cases.append((f"ref_{key}", d))
    d = copy.deepcopy(good)
    d["max_q"]["float"] = bump(d["max_q"]["float"])
    cases.append(("pe_max_q", d))
    d = copy.deepcopy(good)
    d["max_q"]["n_q_PE_hc"] += 1
    cases.append(("pe_len", d))
    d = copy.deepcopy(good)
    d["q_NE_hc_max_record_only"] = bump(d["q_NE_hc_max_record_only"])
    cases.append(("ne_max", d))
    for name, d in cases:
        assert run.binding_problems(loaded, d), name
        with pytest.raises(run.E3aStop):
            attempt(d, name)
    assert opt == []


def test_d_3_halfcell_is_exactly_q_pe_v_pe_q_ne_v_ne_and_a_swap_fails(tmp_path):
    """[RED 실패 — NotImplementedError] 시트마다 다른 곡선을 주는 가짜 util → halfcell 이 정확히 [q_PE, v_PE, q_NE, v_NE] (slice · 질량 ·
    배율 20.16 / 11.4 를 시험이 따로 계산) · PE 를 NE 자리에 둔 적재는 P0 대조에서 실패."""
    mod, _, _ = _fake_util(tmp_path / "u", "ok")
    loaded = run.load_inputs(mod, tmp_path / "LFP_Data.xlsx")
    area = 0.25 * np.pi * 1.2 ** 2
    pe = mod.visualize_LFP_data(data_file="x", sheet_name=c5.p0.SHEETS_REF[0], step_idx=6)[1]
    ne = mod.visualize_LFP_data(data_file="x", sheet_name=c5.p0.SHEETS_REF[1], step_idx=6)[1]
    sp, sn = slice(int(np.argmin(pe[0])), int(np.argmax(pe[0]))), slice(int(np.argmin(ne[0])), int(np.argmax(ne[0])))
    want = [pe[0][sp] / (13.5 * area) * 20.16, pe[1][sp], ne[0][sn] / (5.77 * area) * 11.4, ne[1][sn]]
    hc = loaded["halfcell"]
    assert len(hc) == 4 and all(np.array_equal(np.asarray(a), b) and np.asarray(a).dtype == b.dtype for a, b in zip(hc, want))
    assert not np.array_equal(want[0], want[2])
    assert loaded["PE"] == {"max_q": float(np.max(want[0].flatten())), "n_q_PE_hc": int(want[0].size)}
    assert loaded["NE"] == {"q_NE_hc_max_record_only": float(np.max(want[2]))}
    swap = {c5.p0.SHEETS_REF[0]: c5.p0.SHEETS_REF[1], c5.p0.SHEETS_REF[1]: c5.p0.SHEETS_REF[0]}
    swapped = SimpleNamespace(
        visualize_LFP_data=lambda data_file, sheet_name, step_idx, visualize=True: mod.visualize_LFP_data(
            data_file, swap.get(sheet_name, sheet_name), step_idx, visualize),
        extract_battery_data=mod.extract_battery_data)
    bad = run.load_inputs(swapped, tmp_path / "LFP_Data.xlsx")
    probs = run.binding_problems(bad, _fake_p0(loaded))
    assert any("PE max_q" in p for p in probs) and any("NE q_NE_hc_max_record_only" in p for p in probs)


def test_d_4_paths_inside_the_repo_pickles_notebooks_existing_outputs_and_fetch_targets_are_refused(tmp_path):
    """[RED 실패 — NotImplementedError] 저장소 안 자료 · .pkl · .ipynb · 이미 있는 출력 폴더 · 이미 있는 (또는 저장소 안) fetch 목적지 거부."""
    ok_x, ok_u = tmp_path / "LFP_Data.xlsx", tmp_path / "util_LFP.py"
    run.check_paths(xlsx=ok_x, util=ok_u, out=tmp_path / "new_out")
    for kw in ({"xlsx": BMS / "LFP_Data.xlsx", "util": ok_u, "out": tmp_path / "o1"},
               {"xlsx": ok_x, "util": REPO / "util_LFP.py", "out": tmp_path / "o2"},
               {"xlsx": tmp_path / "results.pkl", "util": ok_u, "out": tmp_path / "o3"},
               {"xlsx": ok_x, "util": tmp_path / "Benchmarking_LFP_final.ipynb", "out": tmp_path / "o4"}):
        with pytest.raises(run.E3aStop):
            run.check_paths(**kw)
    exists = tmp_path / "exists"
    exists.mkdir()
    with pytest.raises(run.E3aStop):
        run.check_paths(xlsx=ok_x, util=ok_u, out=exists)
    called = []

    def no_git(*a, **k):
        called.append(a)
        raise AssertionError("git 을 부르면 안 된다")

    with pytest.raises(run.E3aStop):
        run.fetch(exists, repo_url="/nonexistent", commit="0" * 40, run=no_git)
    inside = BMS / "evidence" / "never_fetch_here_c4e0"
    with pytest.raises(run.E3aStop):
        run.fetch(inside, repo_url="/nonexistent", commit="0" * 40, run=no_git)
    assert called == [] and not inside.exists()


def test_d_5_fetch_takes_only_two_paths_from_the_fixed_commit_of_a_local_repo(tmp_path):
    """[RED 실패 — NotImplementedError] 가짜 로컬 git 저장소 (tmp) 의 고정 커밋에서 두 경로만 · 다른 경로 요청 거부 · sha / bytes 불일치 → 멈춤 ·
    기록에 argv · cwd · 시각 · sha · bytes (파일 바이트 없음) · 네트워크 0 (GIT_ALLOW_PROTOCOL=file)."""
    gd = tmp_path / "x" / "git"
    steps = run.fetch_steps(gd, "/up", "a" * 40)
    flat = [tok for argv in steps for tok in argv]
    assert steps[0][:2] == ["git", "init"] and "--depth" in flat and "--filter=blob:none" in flat and ("a" * 40) in flat
    assert not {"clone", "checkout", "pull", "lfs", "submodule"} & set(flat)
    assert run.show_argv(gd, "a" * 40, "util_LFP.py") == ["git", "-C", str(gd), "show", "a" * 40 + ":util_LFP.py"]
    up = tmp_path / "upstream"
    _git(tmp_path, "init", "-q", str(up))
    xlsx_b, util_b = b"FAKE-XLSX-BYTES " * 512, b"# fake util for the fetch control\n"
    (up / "LFP_Data.xlsx").write_bytes(xlsx_b)
    (up / "util_LFP.py").write_bytes(util_b)
    (up / "results").mkdir()
    (up / "results" / "never.pkl").write_bytes(b"FAKE-PICKLE-NEVER-FETCHED")
    _git(up, "add", "-A")
    _git(up, "-c", "commit.gpgsign=false", "-c", "user.name=c4e0", "-c", "user.email=c4e0@example.invalid", "commit", "-q", "-m", "fake")
    sha = _git(up, "rev-parse", "HEAD").strip()
    _git(up, "config", "uploadpack.allowFilter", "true")
    _git(up, "config", "uploadpack.allowAnySHA1InWant", "true")
    want = {"LFP_Data.xlsx": {"bytes": len(xlsx_b), "sha256": hashlib.sha256(xlsx_b).hexdigest()},
            "util_LFP.py": {"bytes": len(util_b), "sha256": hashlib.sha256(util_b).hexdigest()}}
    dest = tmp_path / "dest"
    rec = run.fetch(dest, repo_url=str(up), commit=sha, files=want, allow_protocol="file")
    assert (dest / "LFP_Data.xlsx").read_bytes() == xlsx_b and (dest / "util_LFP.py").read_bytes() == util_b
    assert not list(dest.rglob("never.pkl"))
    shows = [s["argv"] for s in rec["steps"] if "show" in s["argv"]]
    assert shows == [run.show_argv(dest.resolve() / "git", sha, n) for n in want]
    assert rec["commit"] == sha and rec["ok"] is True and rec["allow_protocol"] == "file"
    assert {n: (f["sha256"], f["bytes"]) for n, f in rec["files"].items()} == {n: (w["sha256"], w["bytes"]) for n, w in want.items()}
    assert all({"argv", "rc", "start_utc", "elapsed_s"} <= set(s) for s in rec["steps"]) and rec["cwd"] and rec["start_utc"]
    text = json.dumps(rec, ensure_ascii=False)
    assert "FAKE-XLSX-BYTES" not in text and "fake util for the fetch control" not in text
    with pytest.raises(run.E3aStop):
        run.fetch(tmp_path / "dest2", repo_url=str(up), commit=sha, files={"results/never.pkl": {"bytes": 1, "sha256": "0" * 64}},
                  allow_protocol="file")
    assert not (tmp_path / "dest2").exists()
    bad = {"LFP_Data.xlsx": want["LFP_Data.xlsx"], "util_LFP.py": {"bytes": len(util_b), "sha256": "0" * 64}}
    with pytest.raises(run.E3aStop):
        run.fetch(tmp_path / "dest3", repo_url=str(up), commit=sha, files=bad, allow_protocol="file")


def test_d_6_identity_start_end_table_and_consumed_digests(tmp_path):
    """[RED 실패 — NotImplementedError] 식별 표 (기대 · 시작 · 끝) · 시작과 끝이 다르면 INCOMPLETE · 기대와 다른 시작 sha 는 문제 ·
    소비 digest · 선택 인자 기록."""
    a, b = tmp_path / "a.bin", tmp_path / "b.bin"
    a.write_bytes(b"alpha")
    b.write_bytes(b"beta")
    exp = {"a": {"sha256": hashlib.sha256(b"alpha").hexdigest(), "bytes": 5}}
    start = run.identity_table({"a": a, "b": b}, exp)
    assert start["a"]["expected"] == exp["a"] and start["a"]["sha256"] == exp["a"]["sha256"] and start["b"]["expected"] is None
    assert start["b"]["sha256"] == hashlib.sha256(b"beta").hexdigest() and start["b"]["bytes"] == 4
    assert run.identity_problems(start) == []
    b.write_bytes(b"beta-changed")
    end = run.identity_table({"a": a, "b": b}, exp)
    assert run.identity_changed(start, end) == ["b"]
    plan = run.plan()
    rule = run.StopRule(plan)
    sup = _sup([_good_row(t) for t in plan])
    agg = run.aggregate(sup, plan, rule)
    pre = run.pre_verdict(plan, agg, sup, start, end)
    assert pre["complete"] is False and any("식별" in r and "'b'" in r for r in pre["reasons"])
    assert run.pre_verdict(plan, agg, sup, start, start)["complete"] is True
    a.write_bytes(b"alpha-tampered")
    assert run.identity_problems(run.identity_table({"a": a}, exp))
    models = {r: {"Q_exp_interp": np.linspace(0, 1, 5) + r, "V_exp_interp": np.linspace(3, 4, 5)} for r in e3a.ROWS}
    hc = [np.linspace(0, 1, 4), np.linspace(3.2, 3.4, 4), np.linspace(0, 1, 4), np.linspace(0.5, 0.1, 4)]
    con = run.consumed(models, hc)
    assert con["models"] == {str(r): c5.model_digest(models[r]) for r in e3a.ROWS} and con["halfcell"] == c5.model_digest(hc)
    sel = con["selection"]
    assert sel["sheets"] == list(c5.p0.SHEETS_ANALYSIS) and sel["step_idx"] == list(c5.p0.STEP_IDX)
    assert sel["cell_idx"] == list(c5.p0.CELL_IDX) and sel["reference"] == {"sheets": list(c5.p0.SHEETS_REF), "step_idx": 6, "cell_idx": 1}
    assert sel["scale"] == {"PE": 20.16, "NE": 11.4} and "argmin" in sel["slice"]


# ======================================================================== s — 계획 · 판정 · 종결 · 끝-끝 · 건조 · 관측 집계
def test_s_1_the_plan_is_the_c4_0a_plan():
    """[RED 실패 — NotImplementedError] 계획 = C4-0a `plan_calls(4)` (66 · 번호 · 작업자 · 알고리즘 · 기대 평가)."""
    calls = run.plan()
    assert calls == e3a.plan_calls(4)
    assert len(calls) == 66 and [c["call_id"] for c in calls] == list(range(66)) and all(c["worker"] == c["call_id"] % 4 for c in calls)
    assert sum(c["algorithm"]["expected_evals"] for c in calls) == 1501500
    assert {c["algorithm"]["name"] for c in calls} == {"GA", "NSGA2", "NSGA3"}


def test_s_2_complete_needs_66_returned_fields_operation_record_identity_and_the_stage_and():
    """[RED 실패 — NotImplementedError] 66 returned + 필드 + 운영 + 최종 기록 + 식별 → COMPLETE · 지역 오류 1 → INCOMPLETE (관측 집계에는
    COMPLETED · error) · C4-A 관문 false · 필드 하나 누락 → INCOMPLETE · 단계 판정 = 최종 AND rc 0 · timeout 없음."""
    plan = run.plan()
    rule = run.StopRule(plan)
    good = [_good_row(t) for t in plan]
    sup = _sup(good)
    agg = run.aggregate(sup, plan, rule)
    pre = run.pre_verdict(plan, agg, sup, {}, {})
    assert pre["complete"] is True and agg["observed"]["COMPLETED_returned"] == 66
    fr_ok = {"record_state": "COMPLETE", "limit_violations": [], "problems": [], "final_snapshot_s": 9000.5}
    fin = run.final_verdict(pre, fr_ok)
    assert (fin["complete"], fin["E3a"], fin["c4a_gate"]) == (True, "COMPLETE", True)
    assert run.stage_verdict(fin, {"rc": 0, "timed_out": False})["complete"] is True
    assert run.stage_verdict(fin, {"rc": 1, "timed_out": False})["complete"] is False
    assert run.stage_verdict(fin, {"rc": None, "timed_out": True})["complete"] is False
    assert run.stage_verdict(None, {"rc": 0, "timed_out": False})["complete"] is False
    fr_bad = {"record_state": "RECORD_INCOMPLETE", "limit_violations": ["time"], "problems": ["시험"], "final_snapshot_s": 9900.5}
    assert run.final_verdict(pre, fr_bad)["complete"] is False
    bad = copy.deepcopy(good)
    bad[25].update(termination="error", error={"kind": "local", "origin": "util", "type": "ValueError"}, X=None, F=None, G=None,
                   G_status="미반환 (호출 오류)")
    sup_b = _sup(bad)
    agg_b = run.aggregate(sup_b, plan, rule)
    assert (agg_b["observed"]["COMPLETED_returned"], agg_b["observed"]["COMPLETED_error"]) == (65, 1)
    fin_b = run.final_verdict(run.pre_verdict(plan, agg_b, sup_b, {}, {}), fr_ok)
    assert (fin_b["complete"], fin_b["E3a"], fin_b["c4a_gate"]) == (False, "INCOMPLETE", False)
    assert run.stage_verdict(fin_b, {"rc": 0, "timed_out": False})["complete"] is False
    miss = copy.deepcopy(good)
    del miss[7]["G_status"]
    sup_m = _sup(miss)
    pre_m = run.pre_verdict(plan, run.aggregate(sup_m, plan, rule), sup_m, {}, {})
    assert pre_m["complete"] is False and any("G_status" in r for r in pre_m["reasons"])
    assert set(run.REQUIRED_FIELDS) == set(C4_0A_FIELDS)


def test_s_3_operation_and_real_finalization_failures_each_leave_incomplete(tmp_path, monkeypatch):
    """[RED 실패 — NotImplementedError] 66 returned 뒤 각각 INCOMPLETE · 행 · 파일 보존. 운영 (합성 supervise 반환 · 순수 판정):
    (a) exitcode ≠ 0 (b) owned_alive_after > 0 (c) drain_ok 거짓 (f) global_stop (freshness) 만 실패. 실제 종결 경로 (finalize · 가짜 clock ·
    작은 크기 한도 — record_state 를 직접 넣지 않는다): (d) 끝 식별 재해시가 늦어 최종 snapshot 이 기록 마감을 넘음 (e) 마지막 끝 기록이 같은 산출
    루트를 크기 한도 위로 올림 (g) 끝 기록 쓰기 · 재읽기 실패. 어느 경우도 앞선 사전 판정이 COMPLETE 를 확정하지 않는다. snapshot 뒤 루트 안 쓰기 0."""
    plan = run.plan()
    rule = run.StopRule(plan)
    good = [_good_row(t) for t in plan]
    for kw in ({"exitcodes": {0: 0, 1: -15, 2: 0, 3: 0}}, {"owned_alive_after": 1}, {"drain_ok": False},
               {"global_stop": "디스크 공백 (확인 · 표본 아님) — 마지막 유효 표본 뒤 16.00 s > 15.0 s"}):
        sup = _sup(copy.deepcopy(good), **kw)
        pre = run.pre_verdict(plan, run.aggregate(sup, plan, rule), sup, {}, {})
        assert pre["complete"] is False and len(sup["states"]) == 66, kw
    files = {"x.bin": tmp_path / "x.bin", "y.bin": tmp_path / "y.bin"}
    files["x.bin"].write_bytes(b"x" * 10)
    files["y.bin"].write_bytes(b"y" * 20)
    start = run.identity_table(files, {})
    sup = _sup(good)

    def fin(out, clk, limit_bytes=10 ** 9, rehash=None):
        return run.finalize(out, plan=plan, sup=sup, rule=rule, ident_start=start, rehash=rehash or (lambda: run.identity_table(files, {})),
                            header={"kind": "E0 대조 s_3"}, limits=dict(run.LIMITS, disk_new=limit_bytes), roots=[out], clock=clk,
                            t0=5000.0, n_workers=4)

    out0 = tmp_path / "base"
    out0.mkdir()
    r0 = fin(out0, _Clk(14000.0, STEP))
    assert r0["pre"]["complete"] is True and r0["final"]["complete"] is True and r0["final_record"]["record_state"] == "COMPLETE"
    assert list(r0["final_record"]["files"]) == list(run.RECORD_FILES) and run.RECORD_FILES[-1] == "END_RECORD.json"
    assert sorted(p.name for p in out0.iterdir()) == sorted(run.RECORD_FILES)
    assert mon.output_bytes([out0]) == r0["final_record"]["output_bytes_after"]
    assert all(hashlib.sha256((out0 / n).read_bytes()).hexdigest() == h for n, h in r0["final_record"]["files"].items())
    assert json.loads((out0 / "END_RECORD.json").read_text(encoding="utf-8"))["pre_verdict"]["complete"] is True
    # (d)
    clk = _Clk(5000.0, STEP)
    n_files = len(run.RECORD_FILES)

    def slow_rehash():
        clk.t = 5000.0 + 9900.0 - n_files * STEP + STEP / 2            # 쓰기 전 확인 n 회는 마감 안 · snapshot 은 마감 뒤
        return run.identity_table(files, {})

    out_d = tmp_path / "d"
    out_d.mkdir()
    r_d = fin(out_d, clk, rehash=slow_rehash)
    assert r_d["pre"]["complete"] is True and r_d["final"]["complete"] is False
    assert (r_d["final_record"]["record_state"], r_d["final_record"]["limit_violations"]) == ("RECORD_INCOMPLETE", ["time"])
    assert r_d["final_record"]["final_snapshot_s"] > 9900.0 and sorted(p.name for p in out_d.iterdir()) == sorted(run.RECORD_FILES)
    # (e)
    sizes = {n: (out0 / n).stat().st_size for n in run.RECORD_FILES}
    total = sum(sizes.values())
    out_e = tmp_path / "e"
    out_e.mkdir()
    r_e = fin(out_e, _Clk(14000.0, STEP), limit_bytes=total - 1)
    assert total - sizes["END_RECORD.json"] <= total - 1
    assert (r_e["final_record"]["record_state"], r_e["final_record"]["limit_violations"]) == ("OUTPUT_LIMIT_EXCEEDED", ["size"])
    assert r_e["pre"]["complete"] is True and r_e["final"]["complete"] is False
    assert (out_e / "END_RECORD.json").is_file() and r_e["final_record"]["output_bytes_after"] == total
    # (g) 쓰기 실패
    out_g = tmp_path / "g"
    out_g.mkdir()
    (out_g / "END_RECORD.json").mkdir()
    r_g = fin(out_g, _Clk(14000.0, STEP))
    assert r_g["final_record"]["record_state"] == "RECORD_INCOMPLETE"
    assert any("END_RECORD.json" in p and "쓰기 실패" in p for p in r_g["final_record"]["problems"])
    assert r_g["pre"]["complete"] is True and r_g["final"]["complete"] is False
    # (g) 재읽기 불일치
    real_read = Path.read_bytes

    def tampered(self):
        data = real_read(self)
        return data + b" " if self.name == "END_RECORD.json" else data

    monkeypatch.setattr(Path, "read_bytes", tampered)
    out_h = tmp_path / "h"
    out_h.mkdir()
    r_h = fin(out_h, _Clk(14000.0, STEP))
    monkeypatch.undo()
    assert r_h["final_record"]["record_state"] == "RECORD_INCOMPLETE"
    assert any("END_RECORD.json" in p and "다시 읽은" in p for p in r_h["final_record"]["problems"])
    assert r_h["pre"]["complete"] is True and r_h["final"]["complete"] is False


def test_s_4_end_to_end_synthetic_run_complete_and_one_local_error_incomplete(tmp_path):
    """[RED 실패 — NotImplementedError] (fork 세션 2) 가짜 util (GA / NSGA2 / NSGA3 꼴 반환 · 최적화 없음 · 호출당 평가 3) · 가짜 xlsx 경로 ·
    fork 작업자 4 → 66 returned COMPLETE · 지역 오류 하나 섞인 변형 → INCOMPLETE."""
    results = {}
    for mode in ("ok", "local_error"):
        d = tmp_path / mode
        mod, util_p, _ = _fake_util(d, mode)
        xlsx = d / "LFP_Data.xlsx"
        xlsx.write_bytes(b"fake xlsx path - never opened by the fake util")
        loaded = run.load_inputs(mod, xlsx)
        p0_p, p0_sha = _write_p0(d / "p0", _fake_p0(loaded))
        res = run.run(d / "out", venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, xlsx=xlsx, util_path=util_p,
                      approval="E0 대조 s_4 (합성)", p0_result=p0_p, expected=_expected(xlsx, util_p, p0_sha), env_identity=_fake_ident,
                      tick=0.05)
        results[mode] = (d / "out", res)
    out, ok = results["ok"]
    assert ok["pre"]["complete"] is True and ok["final"]["complete"] is True and ok["final"]["c4a_gate"] is True
    assert ok["observed"]["COMPLETED_returned"] == 66 and ok["final_record"]["record_state"] == "COMPLETE"
    assert sorted(p.name for p in out.iterdir()) == sorted(run.RECORD_FILES)
    rows = json.loads((out / "ROWS.json").read_text(encoding="utf-8"))
    assert len(rows) == 66 and all(r["termination"] == "returned" for r in rows) and sum(r["n_eval"] for r in rows) == 198
    assert all(set(C4_0A_FIELDS) <= set(r) for r in rows)
    rule = json.loads((out / "RULE.json").read_text(encoding="utf-8"))
    assert rule["stop"] is None and rule["n_calls"] >= 1 and not _has_xfg_key(rule)
    out_e, bad = results["local_error"]
    assert bad["final"]["complete"] is False and bad["final"]["c4a_gate"] is False
    assert (bad["observed"]["COMPLETED_returned"], bad["observed"]["COMPLETED_error"]) == (65, 1)
    err = [r for r in json.loads((out_e / "ROWS.json").read_text(encoding="utf-8")) if r["termination"] == "error"]
    assert len(err) == 1 and (err[0]["case"], err[0]["row"]) == (2, 3) and err[0]["error"]["kind"] == "local"


def test_s_5_plan_e_writes_one_plan_without_util_data_optimizer_or_network(tmp_path, monkeypatch):
    """[RED 실패 — NotImplementedError] `plan-e` 건조: PLAN_E.json 하나 · util import · 자료 · optimizer · 네트워크 · 하위 프로세스 0 ·
    규칙 매개변수 (§4) · 기대 자료 식별 (두 파일 크기 · sha)."""
    def refuse(*a, **k):
        raise AssertionError("plan-e 가 util import · 네트워크 · 하위 프로세스를 썼다")

    monkeypatch.setattr(c5, "load_util", refuse)
    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(subprocess, "run", refuse)
    monkeypatch.setattr(subprocess, "Popen", refuse)
    out = tmp_path / "plan_e"
    summary = run.plan_e(out, venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, env_identity=_fake_ident)
    assert summary["ok"] is True and [p.name for p in out.iterdir()] == ["PLAN_E.json"]
    doc = json.loads((out / "PLAN_E.json").read_text(encoding="utf-8"))
    assert summary["plan_e_sha256"] == _sha_file(out / "PLAN_E.json")
    assert (doc["util_imported"], doc["data_opened"], doc["optimizer_calls"], doc["network"]) == (False, False, 0, 0)
    assert doc["expected_data"] == {"LFP_Data.xlsx": {"bytes": 10841377, "sha256": "fd50e09542be7adb2270963d65a6e7b5ccae1473a512f68462c2dd419d620ee1"},
                                    "util_LFP.py": {"bytes": 33754, "sha256": "3c19e45ef8a64ce67cda1f623551e758d4c0f67086bbae02b978428d78de1c76"}}
    assert doc["source"] == {"url": run.SOURCE_URL, "commit": "1188c371e5836df4a7e5f5acf336a34ffd4027e6"}
    assert doc["rule"]["cap_s"] == 1800.0 and doc["rule"]["min_samples"] == 8 and doc["rule"]["measure_s"] == 9000.0
    assert {k: doc["limits"][k] for k in ("prep", "measure", "record", "stage")} == {"prep": 900.0, "measure": 9000.0, "record": 9900.0,
                                                                                     "stage": 10800.0}
    assert doc["n_calls"] == 66 and len(doc["plan"]) == 66 and doc["expected_evals_total"] == 1501500
    assert doc["p0"]["sha256"] == "3875e65092b38c9b08c907926bd8d1f4ee25674c97c28b5ada935e9027d12a90"
    assert doc["p0"]["q_NE_hc_max_record_only"] == 3.6685628130367562 and doc["p0"]["max_q"] == 3.149013767655145
    flat = [tok for argv in doc["fetch_steps_template"] for tok in argv]
    assert "--filter=blob:none" in flat and "checkout" not in flat and doc["record_files"][-1] == "END_RECORD.json"


def test_s_6_the_observed_tally_partitions_the_66_calls():
    """[RED 실패 — NotImplementedError] 관측 집계: 66 = COMPLETED (returned · error) + STARTED_INTERRUPTED + NOT_STARTED · 칸이 겹치지 않음 ·
    합 = 66 · 같은 task 가 두 번이면 문제."""
    plan = run.plan()
    rule = run.StopRule(plan)
    states = []
    for t in plan:
        tid = t["task_id"]
        if tid < 40:
            states.append(_good_row(t))
        elif tid < 45:
            states.append(dict(_good_row(t), termination="error", X=None, F=None, G=None))
        elif tid < 50:
            states.append({"task_id": tid, "worker": t["worker"], "state": "STARTED_INTERRUPTED", "t_start_rel": 1.0})
        else:
            states.append({"task_id": tid, "worker": t["worker"], "state": "NOT_STARTED", "t_start_rel": None})
    obs = run.aggregate(_sup(states), plan, rule)["observed"]
    assert (obs["COMPLETED_returned"], obs["COMPLETED_error"], obs["STARTED_INTERRUPTED"], obs["NOT_STARTED"]) == (40, 5, 5, 16)
    assert obs["sum"] == obs["planned"] == 66 and obs["other"] == 0
    dup = run.aggregate(_sup(states + [copy.deepcopy(states[0])]), plan, rule)
    assert dup["problems"] and dup["observed"]["sum"] == 67
