"""REIL C4-0b1 한정 보완 (C4-0B1-N1–N3 · 승인 경계 A1) — 변경부와 같은 분기의 양성 · 음성 대조 (C4-0b1 결과 검토 회신 2026-10-13 · 상태 문서 §48).

승인 전 고정본: `docs/REIL_C4_0B1_FIX_CONTROLS_DRAFT_20261013.py.txt`. 승인 뒤 `tests/test_reil_c4_0b1_fix.py` 로 바이트 그대로 복사해 쓴다
(sha256 은 승인 요청문 `docs/REIL_C4_0B1_FIX_APPROVAL_REQUEST_20261013.md`). 고칠 곳 `docs/REIL_C4_0B1_FIX_PATCH_DRAFT_20261013.diff` 도 같이 고정.

합성 입력만 쓴다 — 이 시험이 tmp 에 쓰는 가짜 util · 가짜 minimize · 수용된 봉인 · P0 기록. 보존 util 사본 · REIL xlsx · pkl · 노트북은 쓰지 않는다.
각 시험 docstring 의 [RED …] 는 지금 코드 (패치 전) 에서의 예상이다 — 음성은 실패, 양성 대조 · 특성 고정은 통과.
"""
import hashlib
import json
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import reil_c4_h as h
from scripts import reil_c4_monitor as mon

BMS = Path(__file__).resolve().parents[1]
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
UTIL_COPY = BMS / "reviews" / "prereview_pybamm_reil_20261003" / "external" / "util_LFP.py.txt"
PHASE_A_ARRAYS = BMS / "reil_c4_arrays_20261013"
NEW_SEAL = BMS / "reil_c6_rebuild_20261013"
NEW_SEAL_MANIFEST = "4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc"
LIM = {"measure": 30.0, "grace": 3.0, "rss": 10 ** 12, "rss_gap": 5.0, "disk_new": 10 ** 12, "disk_free": 0, "disk_gap": 15.0}
X0 = [0.9, 0.8, 0.3, 0.1]                     # A0 상자 · G 안 · 가짜 목적의 최소점

FAKE_UTIL = '''
import numpy as np

MODE = {"kind": "ok", "calls": 0}


def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
    q = np.linspace(0.0, 4.0, interp_len)
    return (q * m_P - d_P, q * m_N - d_N, None, None, None, None, None, None)


def objective_fun(x, Model, halfcell):
    MODE["calls"] += 1
    Model["touched"] = Model.get("touched", 0) + 1
    kind, n = MODE["kind"], Model["touched"]
    if kind == "memory" or (kind == "nan_nan_memory" and n == 3):
        raise MemoryError("fake")
    if kind == "value_error":
        raise ValueError("fake util error")
    d = np.asarray(x, dtype=float) - np.array([0.9, 0.8, 0.3, 0.1])
    f = np.array([0.0, float(d @ d) + 1e-6, 0.0, float(np.abs(d).sum()) + 1e-6])
    if kind == "nan" or (kind == "nan_nan_memory" and n <= 2):
        f[1] = float("nan")
    return f
'''


@pytest.fixture
def fake(tmp_path):
    """가짜 util 을 파일로 써서 경로로 로드한다 — 그 frame 이 util 로 분류되게 (C4-0a 보완 시험과 같은 방식)."""
    import importlib.machinery
    import importlib.util
    p = tmp_path / "fake_util_LFP_h.py"
    p.write_text(FAKE_UTIL, encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader(f"fake_util_c4h_{tmp_path.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    model = {"Q_exp_interp": np.linspace(0.0, 3.0, 100), "V_exp_interp": np.linspace(2.0, 3.6, 100),
             "dVdQ_exp_interp": np.full(100, 0.2)}
    ctx = {"util": mod, "util_file": str(p.resolve()), "models": {3: model}, "halfcell": [None] * 4,
           "options": dict(h.DRY_OPTIONS), "gates": {}, "denominators": {}}
    return SimpleNamespace(mod=mod, ctx=ctx)


def _task(objective="J_V", task_id=0):
    return {"task_id": task_id, "run_id": 0, "unit": f"{objective}|A0|3", "objective": objective, "region": "A0", "row": 3,
            "seed": 0, "start_index": 0, "x0": list(X0), "worker": 0}


def _supervise(task, ctx):
    """실제 fork 작업자 1 · 감시 모듈 그대로 (worker_loop → supervise)."""
    return mon.supervise([task], ctx, h.run_phase_a, n_workers=1, limits=dict(LIM), t0=time.monotonic(),
                         rss_fn=lambda p: 1000, disk_fn=lambda r: (0, 10 ** 12), out_roots=[], tick=0.05, disk_every=0.05)


def _fake_minimize(monkeypatch, *, status, success, n_calls, message="fake status"):
    """정해진 status 로 돌아오는 가짜 minimize — 목적을 n_calls 번 부른 뒤 x0 를 돌려준다 (COBYQA 내부 경로에 기대지 않는 분기 고정)."""
    import scipy.optimize as so

    def fake(fun, x0, **kw):
        for _ in range(n_calls):
            fun(np.asarray(x0, dtype=float))
        return SimpleNamespace(x=np.asarray(x0, dtype=float), fun=0.5, status=status, success=success, message=message,
                               nfev=n_calls, nit=1)
    monkeypatch.setattr(so, "minimize", fake)


# ======================================================================== N1 — 구조 중지에도 그때까지의 행 · 계수 · 경고 · 중지 오류
def test_n1_a_counts_and_the_stop_error_cross_the_worker_boundary(fake):
    """[RED 실패 — 지금 partial 에 n_nonfinite · 중지 오류가 없다] 실제 fork 작업자 1 · COBYQA 1 실행: 목적 호출 1 · 2 가 NaN · 3 이 MemoryError →
    부모 기록에 평가 3 · 비유한 2 · 중지 오류 MemoryError 가 남고, 그 작업은 완료가 아니라 중단이다 (검토 회신의 한정 반례)."""
    fake.mod.MODE["kind"] = "nan_nan_memory"
    out = _supervise(_task(), fake.ctx)
    assert out["global_stop"] is not None and "구조 오류" in out["global_stop"] and "MemoryError" in out["global_stop"]
    st = out["states"][0]
    part = st.get("structural_partial") or {}
    assert st["state"] == "STARTED_INTERRUPTED"
    assert (part.get("n_eval"), part.get("n_nonfinite")) == (3, 2)
    assert (part.get("stop_error") or {}).get("type") == "MemoryError" and part.get("unit") == "J_V|A0|3"
    assert out["owned_alive_after"] == 0


def test_n1_b_an_unknown_option_stop_keeps_counts_and_warnings(fake):
    """[RED 실패 — 지금 옵션 경고 중지에는 partial 이 없다] 모르는 옵션 → 실행은 끝까지 돈 뒤 fail-closed 구조 중지 (부속 A §3-1). partial 에
    그때까지의 행 · 평가 수 · 비유한 수 · 경고 원문 · 중지 오류가 남는다."""
    ctx = dict(fake.ctx, options=dict(h.DRY_OPTIONS, not_a_cobyqa_option=1))
    with pytest.raises(mon.Structural) as ei:
        h.run_phase_a(_task(), ctx)
    part = ei.value.partial or {}
    assert ei.value.info["type"] == "OptimizeWarning"
    assert part.get("n_eval", 0) > 0 and part.get("n_nonfinite") == 0
    assert any("Unknown solver options" in w for w in part.get("warnings", []))
    assert (part.get("stop_error") or {}).get("type") == "OptimizeWarning" and part.get("task_id") == 0


def test_n1_c_an_error_in_our_code_after_the_run_keeps_the_row_so_far(fake, monkeypatch):
    """[RED 실패 — 지금 wrapper 의 partial 은 task_id · unit · run_id 뿐] 반환 · 재평가 뒤 우리 코드 (정확 잔차) 의 예외 → 구조 중지. partial 에
    평가 수 · 비유한 수 · 반환점 · termination · 중지 오류가 남는다."""
    _fake_minimize(monkeypatch, status=0, success=True, n_calls=2)

    def boom(x, region):
        raise RuntimeError("fake ours")
    monkeypatch.setattr(h, "exact_residuals", boom)
    with pytest.raises(mon.Structural) as ei:
        h.run_phase_a(_task(), fake.ctx)
    part = ei.value.partial or {}
    assert ei.value.info["origin"] == "ours" and ei.value.info["type"] == "RuntimeError"
    assert (part.get("n_eval"), part.get("n_nonfinite"), part.get("x"), part.get("termination")) == (2, 0, X0, "converged")
    assert (part.get("stop_error") or {}).get("type") == "RuntimeError"


def test_n1_d_the_same_path_without_an_error_completes(fake):
    """[RED 통과 — 양성 대조] n1_a 와 같은 실제 fork 경로 · 같은 작업에서 오류가 없으면 완료 행 (평가 수 · 비유한 0 · 유효 증인) 이고 전역 중지 없음."""
    out = _supervise(_task(), fake.ctx)
    st = out["states"][0]
    assert out["global_stop"] is None and st["state"] == "COMPLETED"
    assert st["n_eval"] > 0 and st["n_nonfinite"] == 0 and st["witness"] == "valid"


# ======================================================================== N2 — 미분류 termination 은 전체 중지 (C4 v2 §5-4 · §6)
def test_n2_a_termination_is_converged_budget_or_unclassified():
    """[RED 실패 — 지금 LINALG_ERROR 가 solver_error] 성공 → converged · MAX_EVAL / MAX_ITER → budget · 그 밖 (알려진 오류 status · 모르는 status ·
    성공이 아닌 status 0) → unclassified. solver_error 는 최적화 중 지역 예외 (반환점 없음) 에만 남는다."""
    from scipy._lib.cobyqa.settings import ExitStatus as S
    assert h.termination(SimpleNamespace(success=True, status=S.RADIUS_SUCCESS.value)) == "converged"
    assert h.termination(SimpleNamespace(success=False, status=S.MAX_EVAL_WARNING.value)) == "budget"
    assert h.termination(SimpleNamespace(success=False, status=S.MAX_ITER_WARNING.value)) == "budget"
    for st in (S.LINALG_ERROR.value, S.INFEASIBLE_ERROR.value, 999, S.RADIUS_SUCCESS.value):
        assert h.termination(SimpleNamespace(success=False, status=st)) == "unclassified"


def test_n2_b_an_unclassified_return_stops_before_the_reeval(fake, monkeypatch):
    """[RED 실패 — DID NOT RAISE · 지금은 solver_error 로 재평가 · 증인까지 간다] 모르는 status 999 반환 → 구조 중지 · 원 status · message · 반환점 ·
    평가 수가 partial 에 남고, 재평가 · 증인은 없다 (목적 호출 = 최적화 중 3 회뿐)."""
    _fake_minimize(monkeypatch, status=999, success=False, n_calls=3, message="weird stop")
    with pytest.raises(mon.Structural) as ei:
        h.run_phase_a(_task(), fake.ctx)
    part = ei.value.partial or {}
    assert ei.value.info["type"] == "UnclassifiedTermination" and "999" in ei.value.info["message"]
    assert (part.get("status"), part.get("message"), part.get("termination")) == (999, "weird stop", "unclassified")
    assert part.get("n_eval") == 3 and part.get("x") == X0 and "witness" not in part and "value" not in part
    assert fake.mod.MODE["calls"] == 3


@pytest.mark.parametrize("status,success,want", [(0, True, "converged"), (5, False, "budget")])
def test_n2_c_success_and_budget_returns_continue_to_the_reeval(fake, monkeypatch, status, success, want):
    """[RED 통과 — 양성 대조] 성공 · 예산 반환은 지역 결과로 재평가 · 증인까지 간다 (termination 은 덮어쓰지 않는다)."""
    _fake_minimize(monkeypatch, status=status, success=success, n_calls=2)
    row = h.run_phase_a(_task(), fake.ctx)
    assert row["state"] == "COMPLETED" and row["termination"] == want and row["witness"] == "valid"
    assert row["n_eval"] == 2 and fake.mod.MODE["calls"] == 3


def test_n2_d_an_unclassified_return_is_a_global_stop_across_the_worker_boundary(fake, monkeypatch):
    """[RED 실패 — 지금은 완료 · 전역 중지 없음] 실제 fork 작업자 1: 미분류 반환 → 전역 중지 · 작업 중단 · partial 에 원 status 999."""
    _fake_minimize(monkeypatch, status=999, success=False, n_calls=1)
    out = _supervise(_task(), fake.ctx)
    st = out["states"][0]
    assert out["global_stop"] is not None and "UnclassifiedTermination" in out["global_stop"]
    assert st["state"] == "STARTED_INTERRUPTED" and (st.get("structural_partial") or {}).get("status") == 999


# ======================================================================== N3 — 재평가 예외는 REEVAL_ERROR (C4 v2 §5-3)
def test_n3_a_a_local_reeval_exception_is_reeval_error_and_counted_apart(fake, monkeypatch):
    """[RED 실패 — 지금 invalid:NONFINITE] 반환점의 독립 재평가에서 util 의 지역 예외 → invalid:REEVAL_ERROR · 원 termination 유지 · 원인 원문 ·
    이유별 집계에서 NONFINITE 와 따로."""
    _fake_minimize(monkeypatch, status=0, success=True, n_calls=0)
    fake.mod.MODE["kind"] = "value_error"
    row = h.run_phase_a(_task(), fake.ctx)
    assert row["state"] == "COMPLETED" and row["termination"] == "converged"
    assert row["witness"] == "invalid:REEVAL_ERROR" and row["value"] is None
    err = row["reeval_error"]
    assert (err["kind"], err["origin"], err["stage"], err["type"]) == ("local", "util", "reeval", "ValueError")
    other = {"run_id": 1, "seed": 0, "witness": "invalid:NONFINITE", "value": float("nan"), "x": X0, "termination": "budget"}
    s = h.phase_a_summary([row, other], expected=2)
    assert s["invalid_by_reason"] == {"NONFINITE": 1, "REEVAL_ERROR": 1} and s["unfit"]


def test_n3_b_a_normal_nan_return_stays_nonfinite(fake, monkeypatch):
    """[RED 통과 — 양성 대조] 재평가가 예외 없이 NaN 을 돌려주면 invalid:NONFINITE · 재평가 오류 없음 · termination 유지."""
    _fake_minimize(monkeypatch, status=0, success=True, n_calls=0)
    fake.mod.MODE["kind"] = "nan"
    row = h.run_phase_a(_task(), fake.ctx)
    assert row["witness"] == "invalid:NONFINITE" and row["reeval_error"] is None and row["termination"] == "converged"
    assert h.phase_a_summary([row], expected=1)["invalid_by_reason"] == {"NONFINITE": 1}


def test_n3_c_a_structural_reeval_error_stops_with_the_termination_kept(fake, monkeypatch):
    """[RED 통과 — 특성 고정] 재평가의 구조 오류 (MemoryError) → 구조 중지 · partial 에 원 termination · 반환점 · 평가 수."""
    _fake_minimize(monkeypatch, status=5, success=False, n_calls=0)
    fake.mod.MODE["kind"] = "memory"
    with pytest.raises(mon.Structural) as ei:
        h.run_phase_a(_task(), fake.ctx)
    part = ei.value.partial or {}
    assert ei.value.info["type"] == "MemoryError" and ei.value.info["stage"] == "reeval"
    assert (part.get("termination"), part.get("x"), part.get("n_eval")) == ("budget", X0, 0)


# ======================================================================== A1 — 건조는 계획 · seed · 봉인만 읽는다 (C4 v2 §4-5)
def _fake_ident(**kw):
    return {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"}


def _forbid(name):
    def f(*a, **k):
        raise AssertionError(f"건조 · 대조가 {name} 을 불렀다")
    return f


def test_a1_a_the_dryrun_only_reads(tmp_path, monkeypatch):
    """[RED 실패 — 지금 건조가 Sobol 을 다시 만들고 (봉인 대조) util 을 불러 합성 최적화를 돈다] Sobol 생성 · 최적화 · util 로드를 막아도 건조는
    PLAN.json 하나만 쓰고, 기록이 그 셋의 0 회를 적는다."""
    harr = tmp_path / "h_arrays"
    seal = h.seal_h_arrays(harr, p0_result=P0_RESULT)
    import scipy.optimize as so
    from scipy.stats import qmc
    from scripts import reil_c5_pilot as c5
    monkeypatch.setattr(qmc, "Sobol", _forbid("qmc.Sobol"))
    monkeypatch.setattr(so, "minimize", _forbid("minimize"))
    monkeypatch.setattr(c5, "load_util", _forbid("load_util"))
    out = tmp_path / "dry"
    rec = h.dryrun(out, venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, arrays_dir=PHASE_A_ARRAYS, h_arrays_dir=harr,
                   h_manifest_sha256=seal["manifest_sha256"], util_copy=UTIL_COPY, p0_result=P0_RESULT, env_identity=_fake_ident)
    assert rec["ok"] and sorted(p.name for p in out.iterdir()) == ["PLAN.json"]
    plan = json.loads((out / "PLAN.json").read_text(encoding="utf-8"))
    assert plan["execution"] == {"optimizer_calls": 0, "objective_calls": 0, "util_imported": False, "sobol_generated": 0}
    assert plan["arrays"]["h"]["mode"] == "bytes" and plan["phase_a"]["registered_runs"] == 9856


def _reseal_manifest(out: Path, rel: str) -> str:
    man = json.loads((out / "MANIFEST.json").read_bytes())
    b = (out / rel).read_bytes()
    man["files"][rel] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    mb = (json.dumps(man, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")
    (out / "MANIFEST.json").write_bytes(mb)
    return hashlib.sha256(mb).hexdigest()


def test_a1_b_byte_mode_refuses_an_array_changed_together_with_its_manifest_entry(tmp_path):
    """[RED 실패 — TypeError: regenerate 인자 없음 (구현 전)] 생성기 없이도: npy 한 값과 MANIFEST 의 그 항목을 함께 바꾸면 INDEX 의 블록 raw sha
    와 맞지 않아 거부한다."""
    out = tmp_path / "h_arrays"
    h.seal_h_arrays(out, p0_result=P0_RESULT, units=["J_V|A0|3"])
    f = out / "profile" / "J_V_A0_3.npy"
    a = np.load(f, allow_pickle=False)
    a[0, 0] = np.nextafter(a[0, 0], 2.0)
    np.save(f, a, allow_pickle=False)
    sha = _reseal_manifest(out, "profile/J_V_A0_3.npy")
    with pytest.raises(h.HStop):
        h.check_h_arrays(out, manifest_sha256=sha, p0_result=P0_RESULT, regenerate=False)


def test_a1_c_byte_mode_accepts_an_untouched_seal_without_the_generator(tmp_path, monkeypatch):
    """[RED 실패 — TypeError (구현 전)] 손대지 않은 봉인 → 생성기를 막아도 bytes 대조 통과 · mode = bytes."""
    out = tmp_path / "h_arrays"
    rec = h.seal_h_arrays(out, p0_result=P0_RESULT, units=["J_Vs|A1|0", "rho|A0|1"])
    from scipy.stats import qmc
    monkeypatch.setattr(qmc, "Sobol", _forbid("qmc.Sobol"))
    chk = h.check_h_arrays(out, manifest_sha256=rec["manifest_sha256"], p0_result=P0_RESULT, regenerate=False)
    assert chk["ok"] and chk["mode"] == "bytes" and chk["n_labels"] == rec["n_labels"] and chk["complete"] is False
