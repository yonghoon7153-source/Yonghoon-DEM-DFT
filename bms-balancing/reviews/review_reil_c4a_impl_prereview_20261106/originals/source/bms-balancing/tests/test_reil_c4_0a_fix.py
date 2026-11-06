"""REIL C4-0a 한정 보완 (C4-0A-N1–N4) — 변경부와 같은 분기의 양성 · 음성 대조 (C4-0a 결과 검토 회신 2026-10-13 · 상태 문서 §42).

승인 전 고정본: `docs/REIL_C4_0A_FIX_CONTROLS_DRAFT_20261013.py.txt`. 승인 뒤 `tests/test_reil_c4_0a_fix.py` 로 바이트 그대로 복사해 쓴다
(sha256 은 승인 요청문 `docs/REIL_C4_0A_FIX_APPROVAL_REQUEST_20261013.md`). 고칠 곳 `docs/REIL_C4_0A_FIX_PATCH_DRAFT_20261013.diff` 도 같이 고정.

합성 입력 · 보존된 util 사본 · 수용된 봉인만 쓴다. REIL xlsx · pkl · 노트북은 열지 않는다.
각 시험 docstring 의 [RED …] 는 지금 코드 (패치 전) 에서의 예상이다 — 음성은 실패, 양성 대조 · 특성 고정 · 기록용은 통과.
"""
import hashlib
import io
import json
import os
import queue
import shutil
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


def _fake_ident(**kw):
    return {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"}


# ======================================================================== N1 — 배열을 수용된 C6 MANIFEST 에 직접 결속
def _npy(a) -> bytes:
    buf = io.BytesIO()
    np.save(buf, np.ascontiguousarray(a, dtype="<f8"), allow_pickle=False)
    return buf.getvalue()


def _tamper_consistently(arrays: Path, name: str) -> None:
    """배열 하나를 바꾸고 로컬 ARRAYS.json 의 npy_sha256 과 MANIFEST 를 함께 갱신한다 (C6 라벨 · 옛 c6_npy_sha256 은 그대로) — 검토 회신의 반례."""
    new = _npy(np.full((64, 4), 0.75))
    (arrays / name).write_bytes(new)
    meta = json.loads((arrays / "ARRAYS.json").read_text(encoding="utf-8"))
    meta["arrays"][name]["npy_sha256"] = hashlib.sha256(new).hexdigest()
    aj = (json.dumps(meta, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")
    (arrays / "ARRAYS.json").write_bytes(aj)
    man = json.loads((arrays / "MANIFEST.json").read_text(encoding="utf-8"))
    man[name], man["ARRAYS.json"] = hashlib.sha256(new).hexdigest(), hashlib.sha256(aj).hexdigest()
    (arrays / "MANIFEST.json").write_text(json.dumps(man, sort_keys=True, indent=1) + "\n", encoding="utf-8")


def test_n1_a_an_array_changed_together_with_both_local_records_is_refused(tmp_path):
    """[RED 실패 — 지금 dryrun 은 로컬 자기 일치만 보고 계획을 쓴다] 수용 C6 와 다른 배열은 로컬 기록이 맞아도 거부 · 아무것도 쓰지 않는다."""
    arrays = tmp_path / "arrays"
    e3a.seal_arrays(arrays, c6_seal=NEW_SEAL)
    _tamper_consistently(arrays, "sobol_A1_A2_wide_box_seed1.npy")
    out = tmp_path / "dry"
    with pytest.raises(e3a.E3aStop):
        e3a.dryrun(out, venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, arrays_dir=arrays,
                   util_copy=UTIL_COPY, p0_result=P0_RESULT, env_identity=_fake_ident, n_workers=4)
    assert not out.exists()


def test_n1_b_check_arrays_authenticates_the_c6_manifest_before_using_its_entries(tmp_path):
    """[RED 실패 — TypeError: 지금 check_arrays 에 seal 인자가 없다 (구현 전)] 명시 sha 와 다른 C6 MANIFEST 의 항목은 쓰지 않는다."""
    arrays = tmp_path / "arrays"
    e3a.seal_arrays(arrays, c6_seal=NEW_SEAL)
    forged = tmp_path / "forged_seal"
    shutil.copytree(NEW_SEAL, forged)
    man = json.loads((forged / "MANIFEST.json").read_text(encoding="utf-8"))
    man["sobol_A0_their_box_seed0.npy"] = "0" * 64
    (forged / "MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(e3a.E3aStop):
        e3a.check_arrays(arrays, seal=forged, manifest_sha256=NEW_SEAL_MANIFEST)


def test_n1_c_untouched_arrays_match_every_c6_entry_directly(tmp_path):
    """[RED 실패 — TypeError (구현 전)] 양성 대조: 손대지 않은 봉인은 넷 모두 C6 항목과 직접 일치한다."""
    arrays = tmp_path / "arrays"
    e3a.seal_arrays(arrays, c6_seal=NEW_SEAL)
    rec = e3a.check_arrays(arrays, seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST)
    assert rec["c6_direct_match"] == {n: True for n in e3a.ARRAY_NAMES}


# ======================================================================== N2 — 마지막 기록 뒤 snapshot 하나로 시간 판정
class _Clock:
    """주입 시계 — 값을 차례로 내고, 다 쓰면 마지막 값을 계속 낸다 (+ extra).
    final_record 의 시계 호출 순서: 파일마다 쓰기 전 1 회 → 마지막 snapshot 1 회."""

    def __init__(self, *values):
        self.values, self.i, self.extra = list(values), 0, 0.0

    def __call__(self):
        v = self.values[min(self.i, len(self.values) - 1)]
        self.i += 1
        return v + self.extra


def test_n2_a_a_slow_last_write_past_the_limit_is_not_complete(tmp_path):
    """[RED 실패 — 지금은 COMPLETE] 마지막 쓰기 · 재읽기 · 해시 뒤 snapshot 이 한도를 넘으면 미완 · 파일과 해시는 보존 · 판정한 그 값을 반환."""
    out = tmp_path / "out"
    out.mkdir()
    fr = mon.final_record(out, {"ROWS.json": {"k": 1}}, roots=[out], limit_bytes=10 ** 6, clock=_Clock(0.5, 61.0), t0=0.0,
                          limit_s=60.0)
    assert fr["record_state"] == "RECORD_INCOMPLETE"
    assert fr["final_snapshot_s"] == 61.0
    assert fr["files"]["ROWS.json"] == hashlib.sha256((out / "ROWS.json").read_bytes()).hexdigest()


def test_n2_b_a_slow_final_size_scan_past_the_limit_is_not_complete(tmp_path, monkeypatch):
    """[RED 실패 — 지금은 COMPLETE] 쓰기 뒤 용량 조회가 늦어 한도를 넘어도 미완. 조회한 바이트 수는 그대로 남긴다."""
    out = tmp_path / "out"
    out.mkdir()
    clock, real = _Clock(0.5), mon.output_bytes

    def slow(roots):
        clock.extra = 60.5                      # 용량 조회가 60.5 s 걸린 것처럼 — 주입 시계만 옮긴다
        return real(roots)

    monkeypatch.setattr(mon, "output_bytes", slow)
    fr = mon.final_record(out, {"A.json": [1, 2]}, roots=[out], limit_bytes=10 ** 6, clock=clock, t0=0.0, limit_s=60.0)
    assert fr["record_state"] == "RECORD_INCOMPLETE" and fr["final_snapshot_s"] == 61.0
    assert fr["output_bytes_after"] == (out / "A.json").stat().st_size


def test_n2_c_within_limits_is_complete_and_returns_the_judged_snapshot(tmp_path):
    """[RED 통과 — 양성 대조] 한도 안이면 COMPLETE · 반환한 snapshot 이 판정에 쓴 값이다."""
    out = tmp_path / "out"
    out.mkdir()
    fr = mon.final_record(out, {"A.json": {"k": 1}}, roots=[out], limit_bytes=10 ** 6, clock=_Clock(0.5, 1.5), t0=0.0,
                          limit_s=60.0)
    assert fr["record_state"] == "COMPLETE" and fr["final_snapshot_s"] == 1.5 and fr["problems"] == []


def test_n2_d_time_and_size_both_over_are_both_recorded(tmp_path):
    """[RED 실패 — 지금은 크기만 남고 limit_violations 가 없다] 시간 · 크기 둘 다 넘으면 둘 다 기록 · COMPLETE 아님."""
    out = tmp_path / "out"
    out.mkdir()
    (out / "big.bin").write_bytes(b"z" * 900)
    fr = mon.final_record(out, {"R.json": {"a": "b" * 300}}, roots=[out], limit_bytes=1000, clock=_Clock(0.5, 61.0), t0=0.0,
                          limit_s=60.0)
    assert fr["record_state"] != "COMPLETE"
    assert fr.get("limit_violations") == ["time", "size"]


# ======================================================================== N3 — 느린 조회 뒤 · 정상 종료 직전 두 감시기 freshness
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
    """대본 작업자 — start 때 정해진 메시지를 큐에 넣고 곧바로 끝난 프로세스처럼 보인다 (target 을 부르지 않는다 · 실제 프로세스 0)."""

    def __init__(self, script, target=None, args=(), daemon=None):
        self.wid, self.q, self.script = args[0], args[4], script
        self.pid, self.exitcode = None, None

    def start(self):
        self.pid = 4_000_000 + self.wid
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


def _scripted_supervise(monkeypatch, disk_seconds):
    """작업자 1 (작업 0) 이 시작 · 끝 메시지만 내는 대본 + 주입 시계 (검토 회신 M2 의 '대본 시계 · 디스크 콜백 · 끝 이벤트').
    RSS 조회는 0.01 s, 디스크 조회는 `disk_seconds` 걸린 것처럼 시계를 옮긴다. 한도: RSS 공백 5 s · 디스크 공백 15 s · 마감 30 s."""
    import multiprocessing
    ctx = _ScriptedCtx({0: [("worker_start", 0, {"pid": 1, "t": 0.0}), ("worker_end", 0, {"t": 0.0})]})
    monkeypatch.setattr(multiprocessing, "get_context", lambda method=None: ctx)
    clk = {"t": 0.0}

    def rss(pids):
        clk["t"] += 0.01
        return 1000

    def disk(roots):
        clk["t"] += disk_seconds
        return (0, 10 ** 12)

    return mon.supervise([], {}, None, n_workers=1, limits=dict(LIM), t0=0.0, clock=lambda: clk["t"], rss_fn=rss,
                         disk_fn=disk, out_roots=[], tick=0.0, disk_every=0.0)


def test_n3_a_a_slow_terminal_disk_sample_cannot_hide_an_rss_gap(monkeypatch):
    """[RED 실패 — 지금은 global_stop None] 마지막 디스크 조회 6 s (디스크 15 s · 마감 30 s 는 만족) 뒤 모든 작업자가 끝났어도
    RSS 공백 6 s > 5 s 이면 정상 종료가 아니다."""
    out = _scripted_supervise(monkeypatch, 6.0)
    assert out["global_stop"] is not None and "메모리" in out["global_stop"] and "공백" in out["global_stop"]
    assert out["owned_alive_after"] == 0


def test_n3_b_a_quick_terminal_disk_sample_still_ends_normally(monkeypatch):
    """[RED 통과 — 양성 대조] 마지막 디스크 조회 1 s 면 RSS 공백 1 s ≤ 5 s — 확인이 거짓 중단을 만들지 않는다."""
    out = _scripted_supervise(monkeypatch, 1.0)
    assert out["global_stop"] is None


def test_n3_c_a_freshness_check_does_not_refresh_the_watch():
    """[RED 실패 — AttributeError: Watch.stale 없음 (구현 전)] 확인은 표본이 아니다 — 마지막 유효 시각 · 표본 목록을 바꾸지 않고, 다음
    성공 표본의 공백도 옛 유효 시각부터 잰다."""
    w = mon.Watch("메모리", gap_limit=5.0, t_start=0.0)
    assert w.observe(0.5, 100, 1.0) is None
    n = len(w.samples)
    assert w.stale(3.0) is None
    r = w.stale(7.0)
    assert r is not None and "공백" in r
    assert w.last_valid == 1.0 and len(w.samples) == n
    late = w.observe(7.2, 100, 7.5)
    assert late is not None and "늦은 성공 표본" in late


# ======================================================================== N4 — 구조 오류의 partial 이 작업자 경계를 넘는다
class _ListQueue:
    def __init__(self):
        self.items = []

    def put(self, item):
        self.items.append(item)


class _NeverStop:
    def is_set(self):
        return False


def test_n4_a_worker_loop_forwards_the_structural_partial():
    """[RED 실패 — 지금은 info 만 보낸다] 구조 오류 이벤트에 partial 이 따로 실리고 완료 (done) 는 없다."""
    part = {"n_eval": 7, "n_nonfinite": 2, "n_out_eval_PE": 3, "n_eval_G_violated": 1}

    def boom(task, ctx, notify=None, progress=None):
        raise mon.Structural({"kind": "structural", "origin": "util", "stage": "optimize", "type": "MemoryError",
                              "message": "fake"}, partial=part)

    q = _ListQueue()
    mon.worker_loop(0, [{"task_id": 5, "worker": 0}], {}, boom, q, _NeverStop(), {}, deadline_abs=time.monotonic() + 60)
    ev = [p for k, _, p in q.items if k == "structural"]
    assert len(ev) == 1 and ev[0].get("partial") == part and ev[0]["message"] == "fake"
    assert "done" not in [k for k, _, _ in q.items]


FAKE_UTIL = '''
import numpy as np

MODE = {"kind": "ok"}


class Result:
    pass


def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
    if MODE["kind"] == "bad_dvdq":
        return 5
    q = np.linspace(0.0, 1.0, interp_len)
    return (q * m_P - d_P, q * m_N - d_N, None, None, None, None, None, None)


def objective_fun(x, Model, halfcell):
    Model["touched"] = Model.get("touched", 0) + 1
    if MODE["kind"] == "memory_on_3" and Model["touched"] == 3:
        raise MemoryError("fake")
    dVdQ_hc(halfcell[1], halfcell[0], halfcell[3], halfcell[2], *x, interp_len=50)
    f = np.array([0.1, float(np.sum(np.asarray(x) ** 2)), 0.2, 0.3])
    if Model["touched"] == 2:
        f[1] = float("nan")
    return f


def run_optimization(Model, halfcell, obj_selection, pop_size=50):
    xs = [np.array([0.9, 0.8, 0.2, 0.1]), np.array([1.0, 1.0, 0.1, 0.4]), np.array([0.7, 0.6, 0.3, 0.2])]
    for x in xs:
        objective_fun(x, Model, halfcell)
    res = Result()
    res.X = np.array(xs)
    res.F = np.array([[0.5], [0.4], [0.2]])
    res.G = None
    res.success = True
    return res
'''


@pytest.fixture
def fake(tmp_path):
    import importlib.machinery
    import importlib.util
    p = tmp_path / "fake_util_LFP.py"
    p.write_text(FAKE_UTIL, encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader(f"fake_util_c4fix_{tmp_path.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    model = {"Q_exp_interp": np.linspace(-0.2, 1.2, 50), "V_exp_interp": np.linspace(2.0, 3.6, 50)}
    halfcell = [np.linspace(0, 1, 10), np.linspace(3.2, 3.5, 10), np.linspace(0, 1, 10), np.linspace(0.6, 0.1, 10)]
    ctx = {"util": mod, "util_file": str(p.resolve()), "models": {3: model}, "halfcell": halfcell,
           "extraction": {3: {"row": 3, "n_points": 42, "status": "OK"}}}
    return SimpleNamespace(mod=mod, ctx=ctx, model=model)


def _task(case=1, row=3, task_id=0):
    sel = {1: [0, 1]}[case]
    return {"task_id": task_id, "call_id": case * 11 + row, "case": case, "row": row, "obj_selection": sel,
            "algorithm": e3a.algorithm_of(sel), "worker": 0}


def test_n4_b_the_partial_crosses_the_worker_boundary_and_the_task_stays_interrupted(fake):
    """[RED 실패 — 지금 부모가 받는 구조 오류에 partial 이 없다] 실제 fork 작업자 1 · E3a 호출 1: 셋째 평가의 MemoryError 전까지 모은 계수
    (평가 3 · 비유한 1 · PE 영역 밖 평가 2 · G 위반 x 평가 1) 가 부모 기록에 남고, 그 작업은 완료가 아니라 중단이다."""
    fake.mod.MODE["kind"] = "memory_on_3"
    out = mon.supervise([_task()], fake.ctx, e3a.run_e3a_call, n_workers=1, limits=dict(LIM), t0=time.monotonic(),
                        rss_fn=lambda p: 1000, disk_fn=lambda r: (0, 10 ** 12), out_roots=[], tick=0.05, disk_every=0.05)
    assert out["global_stop"] is not None and "구조 오류" in out["global_stop"]
    part = out["structural"][0].get("partial") or {}
    assert (part.get("n_eval"), part.get("n_nonfinite"), part.get("n_out_eval_PE"), part.get("n_eval_G_violated")) == (3, 1, 2, 1)
    st = out["states"][0]
    assert st["state"] == "STARTED_INTERRUPTED" and (st.get("structural_partial") or {}).get("n_eval") == 3
    assert out["owned_alive_after"] == 0


def test_n4_c_an_error_inside_our_wrapper_is_structural_not_util_local(fake):
    """[RED 통과 — 특성 고정 (이미 구현된 분기 · 검토 회신이 명시를 요청)] 우리 감싸기 (counted_dv) 안의 오류는 바깥에 util frame 이 있어도
    구조 오류다. util 함수는 되돌려 놓는다."""
    fake.mod.MODE["kind"] = "bad_dvdq"
    with pytest.raises(mon.Structural) as ei:
        e3a.run_e3a_call(_task(), fake.ctx)
    info = ei.value.info
    assert info["kind"] == "structural" and info["origin"] == "ours" and info["type"] == "TypeError"
    assert ei.value.partial["n_eval"] == 1
    assert fake.mod.objective_fun.__name__ == "objective_fun" and fake.mod.dVdQ_hc.__name__ == "dVdQ_hc"


# ======================================================================== 기록 — 합성 NSGA2 의 분기 · 평가 수 · 예외 요약을 파일로
def test_out_the_synthetic_nsga2_outcome_is_kept_as_evidence():
    """[RED 통과 — 기록용 (기능 변경 없음)] 보존 util 사본 · 합성 곡선의 NSGA2 1 회 — 통과 시험이어도 분기 · 평가 수 · 예외 요약을 파일로
    남긴다 (검토 회신: 다음 승인 시험에서 outcome 보존). 위치는 단계 실행기가 주는 REIL_C4_FIX_EVIDENCE · REIL_C4_FIX_STEP."""
    out_dir, step = os.environ.get("REIL_C4_FIX_EVIDENCE"), os.environ.get("REIL_C4_FIX_STEP")
    assert out_dir and step, "단계 실행기 밖에서는 돌리지 않는다 (기록 위치 없음)"
    from scripts import reil_c5_pilot as c5
    util, uf = c5.load_util(UTIL_COPY, c5.UTIL_COPY_SHA)
    model, halfcell = c5.synthetic_inputs(util)
    ctx = {"util": util, "util_file": uf, "models": {1: model}, "halfcell": halfcell, "extraction": {1: {"row": 1}}}
    row = e3a.run_e3a_call(_task(case=1, row=1), ctx)
    err = row["error"]
    rec = {"termination": row["termination"], "n_eval": row["n_eval"], "expected_evals": row["algorithm"]["expected_evals"],
           "n_solutions": row["n_solutions"], "n_nonfinite": row["n_nonfinite"], "n_out_eval_any": row["n_out_eval_any"],
           "error": None if err is None else {k: err.get(k) for k in ("kind", "origin", "type", "message", "traceback")},
           "warnings_count": row["warnings_count"], "wall_s": row["wall"]}
    p = Path(out_dir) / f"{step}.nsga2_synthetic_outcome.json"
    assert not p.exists()
    p.write_text(json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    assert row["state"] == "COMPLETED" and row["termination"] in ("returned", "error") and 0 < row["n_eval"] <= 5000
