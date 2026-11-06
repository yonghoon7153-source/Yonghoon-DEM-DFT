"""REIL C4-0b1 한정 보완 2 (C4-0B1-N1 잔여) — 모르는 옵션 경고 중지 전에 이미 받은 반환 필드를 partial 에 남긴다 (재검토 회신 2026-10-14 · 상태 문서 §51).

승인 전 고정본: `docs/REIL_C4_0B1_FIX2_CONTROLS_DRAFT_20261014.py.txt`. 승인 뒤 `tests/test_reil_c4_0b1_fix2.py` 로 바이트 그대로 복사해 쓴다
(sha256 은 승인 요청문 `docs/REIL_C4_0B1_FIX2_APPROVAL_REQUEST_20261014.md`). 고칠 곳 `docs/REIL_C4_0B1_FIX2_PATCH_DRAFT_20261014.diff` 도 같이 고정.

합성 입력만 쓴다 — 이 시험이 tmp 에 쓰는 가짜 util · 가짜 minimize (경고를 스스로 낸다). 보존 util 사본 · REIL 자료는 쓰지 않는다.
각 시험 docstring 의 [RED …] 는 지금 코드 (패치 전) 에서의 예상이다 — 음성은 실패, 양성 대조는 통과.
"""
import time
import warnings
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import reil_c4_h as h
from scripts import reil_c4_monitor as mon

LIM = {"measure": 30.0, "grace": 3.0, "rss": 10 ** 12, "rss_gap": 5.0, "disk_new": 10 ** 12, "disk_free": 0, "disk_gap": 15.0}
X0 = [0.9, 0.8, 0.3, 0.1]                     # A0 상자 · G 안 · 가짜 목적의 최소점
UNKNOWN = "Unknown solver options: not_a_cobyqa_option"

FAKE_UTIL = '''
import numpy as np

MODE = {"kind": "ok", "calls": 0}


def dVdQ_hc(V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=300):
    q = np.linspace(0.0, 4.0, interp_len)
    return (q * m_P - d_P, q * m_N - d_N, None, None, None, None, None, None)


def objective_fun(x, Model, halfcell):
    MODE["calls"] += 1
    if MODE["kind"] == "value_error":
        raise ValueError("fake util error")
    d = np.asarray(x, dtype=float) - np.array([0.9, 0.8, 0.3, 0.1])
    return np.array([0.0, float(d @ d) + 1e-6, 0.0, float(np.abs(d).sum()) + 1e-6])
'''


@pytest.fixture
def fake(tmp_path):
    """가짜 util 을 파일로 써서 경로로 로드한다 — 그 frame 이 util 로 분류되게 (한정 보완 1 의 시험과 같은 방식)."""
    import importlib.machinery
    import importlib.util
    p = tmp_path / "fake_util_LFP_h2.py"
    p.write_text(FAKE_UTIL, encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader(f"fake_util_c4h2_{tmp_path.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    model = {"Q_exp_interp": np.linspace(0.0, 3.0, 100), "V_exp_interp": np.linspace(2.0, 3.6, 100),
             "dVdQ_exp_interp": np.full(100, 0.2)}
    ctx = {"util": mod, "util_file": str(p.resolve()), "models": {3: model}, "halfcell": [None] * 4,
           "options": dict(h.DRY_OPTIONS), "gates": {}, "denominators": {}}
    return SimpleNamespace(mod=mod, ctx=ctx)


def _task(task_id=0):
    return {"task_id": task_id, "run_id": 0, "unit": "J_V|A0|3", "objective": "J_V", "region": "A0", "row": 3,
            "seed": 0, "start_index": 0, "x0": list(X0), "worker": 0}


def _fake_minimize(monkeypatch, *, warn, n_calls, status=0, success=True, message="fake status"):
    """알려진 반환을 주는 가짜 minimize — warn 이면 scipy 와 같은 모르는 옵션 경고를 먼저 낸다 · 목적을 n_calls 번 부른 뒤 x0 를 돌려준다."""
    import scipy.optimize as so

    def fake(fun, x0, **kw):
        if warn:
            warnings.warn(UNKNOWN, so.OptimizeWarning)
        for _ in range(n_calls):
            fun(np.asarray(x0, dtype=float))
        return SimpleNamespace(x=np.asarray(x0, dtype=float), fun=0.5, status=status, success=success, message=message,
                               nfev=n_calls, nit=1)
    monkeypatch.setattr(so, "minimize", fake)


RETURN_FIELDS = {"x": X0, "fun": 0.5, "status": 0, "message": "fake status", "nfev": 2, "nit": 1, "termination": "converged"}


def test_r1_a_a_known_return_survives_the_option_warning_stop(fake, monkeypatch):
    """[RED 실패 — 지금 partial 에 반환 필드가 없다] 경고 + 알려진 정상 반환 → OptimizeWarning 구조 중지 · partial 에 반환점 · status · message ·
    termination 등과 계수 · 경고 · 중지 오류가 남고, 재평가 · 증인으로 가지 않는다 (목적 호출 = 최적화 중 2 회뿐)."""
    _fake_minimize(monkeypatch, warn=True, n_calls=2)
    with pytest.raises(mon.Structural) as ei:
        h.run_phase_a(_task(), fake.ctx)
    part = ei.value.partial or {}
    assert ei.value.info["type"] == "OptimizeWarning"
    assert {k: part.get(k) for k in RETURN_FIELDS} == RETURN_FIELDS
    assert (part.get("n_eval"), part.get("n_nonfinite")) == (2, 0) and any(UNKNOWN in w for w in part.get("warnings", []))
    assert (part.get("stop_error") or {}).get("type") == "OptimizeWarning"
    assert "witness" not in part and "value" not in part and fake.mod.MODE["calls"] == 2


def test_r1_b_the_return_fields_cross_the_worker_boundary(fake, monkeypatch):
    """[RED 실패 — 지금 부모의 structural_partial 에 반환점 · status 가 없다] 실제 fork 작업자 1: 같은 경고 + 알려진 반환 → 전역 중지 · 작업 중단 ·
    부모 기록에 반환점 · status · termination · 계수."""
    _fake_minimize(monkeypatch, warn=True, n_calls=2)
    out = mon.supervise([_task()], fake.ctx, h.run_phase_a, n_workers=1, limits=dict(LIM), t0=time.monotonic(),
                        rss_fn=lambda p: 1000, disk_fn=lambda r: (0, 10 ** 12), out_roots=[], tick=0.05, disk_every=0.05)
    st = out["states"][0]
    part = st.get("structural_partial") or {}
    assert out["global_stop"] is not None and "OptimizeWarning" in out["global_stop"] and st["state"] == "STARTED_INTERRUPTED"
    assert (part.get("x"), part.get("status"), part.get("termination"), part.get("n_eval")) == (X0, 0, "converged", 2)
    assert out["owned_alive_after"] == 0


def test_r1_c_without_a_return_nothing_is_filled_and_the_original_error_is_kept(fake, monkeypatch):
    """[RED 실패 — 지금 partial 에 원 지역 오류가 없다] 경고 뒤 목적의 util 지역 오류로 반환이 없다 → OptimizeWarning 구조 중지 · partial 에 원 지역 오류
    (ValueError · util) 가 남고, 반환점 · status · message · termination 은 채우지 않는다."""
    _fake_minimize(monkeypatch, warn=True, n_calls=1)
    fake.mod.MODE["kind"] = "value_error"
    with pytest.raises(mon.Structural) as ei:
        h.run_phase_a(_task(), fake.ctx)
    part = ei.value.partial or {}
    err = part.get("error") or {}
    assert ei.value.info["type"] == "OptimizeWarning" and (part.get("stop_error") or {}).get("type") == "OptimizeWarning"
    assert (err.get("kind"), err.get("origin"), err.get("type")) == ("local", "util", "ValueError")
    assert not ({"x", "fun", "status", "message", "nfev", "nit", "termination", "witness", "value"} & set(part))
    assert (part.get("n_eval"), part.get("n_nonfinite")) == (1, 0)


def test_r1_d_the_same_path_without_the_warning_completes(fake, monkeypatch):
    """[RED 통과 — 양성 대조] 같은 알려진 반환에서 경고가 없으면 완료 행 — 반환 필드 그대로 · 재평가 1 회 · 유효 증인."""
    _fake_minimize(monkeypatch, warn=False, n_calls=2)
    row = h.run_phase_a(_task(), fake.ctx)
    assert row["state"] == "COMPLETED" and row["witness"] == "valid"
    assert {k: row.get(k) for k in RETURN_FIELDS} == RETURN_FIELDS and fake.mod.MODE["calls"] == 3


def test_r1_e_the_real_scipy_warning_path_keeps_the_returned_point(fake):
    """[RED 실패 — 지금 partial 에 반환점이 없다] 실제 minimize (COBYQA) 에 모르는 옵션 → scipy 의 경고 · 실제 반환 → 구조 중지 · partial 에 반환점
    (유한 4 값) · status · message · termination · nfev 가 있고, 재평가는 없다 (목적 호출 = 평가 수)."""
    ctx = dict(fake.ctx, options=dict(h.DRY_OPTIONS, not_a_cobyqa_option=1))
    with pytest.raises(mon.Structural) as ei:
        h.run_phase_a(_task(), ctx)
    part = ei.value.partial or {}
    x = part.get("x")
    assert ei.value.info["type"] == "OptimizeWarning"
    assert isinstance(x, list) and len(x) == 4 and all(np.isfinite(x))
    assert isinstance(part.get("status"), int) and isinstance(part.get("message"), str) and part.get("termination") in ("converged", "budget", "unclassified")
    assert part.get("nfev", 0) > 0 and fake.mod.MODE["calls"] == part.get("n_eval") and "witness" not in part
