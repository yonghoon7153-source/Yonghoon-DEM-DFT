"""REIL C5 비용 파일럿 — 셀 #1 · A0 · J_V = sqrt(f2) · Phase A 128 지역 실행 (COBYQA) 의 **비용**만 잰다.

승인 · 범위: `docs/REIL_C5_PILOT_APPROVAL_REQUEST_v2_20261006.md` (§1–§8) + 부록 `…_v2_ADDENDUM_20261006.md` (A1–A4) · 상태 §28.
결과는 확인적 분석에 쓰지 않는다 (바꿀 수 있는 것은 C4 의 벽시계 예산표와 병렬 수뿐 — v2 §8).

    <venv>/bin/python -I bms-balancing/scripts/reil_c5_pilot.py identity --venv <venv> --out <file.json>
    <venv>/bin/python -I bms-balancing/scripts/reil_c5_pilot.py dryrun   --venv <venv> --out <dir>
    <venv>/bin/python -I bms-balancing/scripts/reil_c5_pilot.py measure  --venv <venv> --out <dir> --xlsx <xlsx> --util <util_LFP.py> --approval <상태 문서 절>

- `identity` 는 **계산 없는 환경 식별**이다 (부록 A1): 실제 interpreter · 설치 파일 RECORD 해시 대조 (`lock_text`) · 판 메타데이터
  (`profile`) · COBYQA 옵션 표 · 구현 파일 재해시 · 봉인 MANIFEST. 합성 최적화 (`cobyqa_options`) · Sobol 생성 (`sobol`) · `emit` ·
  full C6 `check` 는 부르지 않는다 — full check 는 `NOT_RUN` 으로 남는다.
- `dryrun` 은 보존된 util 사본 · 해석식 합성 곡선 · fixture Sobol (rng 20261006 · 정식 배열 아님) 로 경로만 지난다 (시간 숫자는 비용 근거 아님).
- `measure` 는 v2 §10 (2) 의 별도 승인 뒤에만 쓴다. 측정 단계의 Sobol 은 A0 seed 0 · 1 배열만 다시 만들어 봉인과 바이트 대조한다.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import math
import os
import queue
import shutil
import subprocess
import sys
import time
import traceback
import warnings
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve()
BMS = HERE.parents[1]
REPO = HERE.parents[2]


def _sibling(name: str):
    """같은 폴더의 봉인 · P0 스크립트를 경로로 읽는다 (`-I` 실행에서도 · 패키지 import 에 기대지 않음)."""
    spec = importlib.util.spec_from_file_location(f"reil_c5_sibling_{name}", HERE.parent / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


prof = _sibling("reil_c6_profile")
p0 = _sibling("reil_p0")

#: v2 §1 — C6 봉인 `COBYQA_OPTIONS.json` 의 `options` 와 같은 8 개 (실행 때 대조 · 판 기본값에 기대지 않음)
OPTIONS = dict(prof.COBYQA_OPTIONS)
#: A0 상자 (십진 문자열 = 정확 유리수) · G: d_P − d_N ≥ 1e-4 · 증인 허용치 1e-10 (부속 A §2-1)
LO = ("0.6", "0.5", "0.005", "0")
HI = ("1.1", "1.1", "0.5", "1")
G_LB = Fraction("1e-4")
TOL = Fraction("1e-10")
SEALED = BMS / "reil_c6_rebuild_20261006"
PILOT_ARRAYS = {0: "sobol_A0_their_box_seed0.npy", 1: "sobol_A0_their_box_seed1.npy"}
SOBOL_N = 64
UTIL_SHA = p0.SHA_UTIL
XLSX_SHA = p0.SHA_XLSX
UTIL_COPY = BMS / "reviews" / "prereview_pybamm_reil_20261003" / "external" / "util_LFP.py.txt"
UTIL_COPY_SHA = "bdf78273d50f40ce3154d01a3ef8d36f0f5ea5ec1b04539584809d7b19b46f9c"
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
CELL_ROW = 1                       # #1 LLI-1 (v2 §1 · 규칙으로 다시 고른다)
BOUNDARY_ROWS = frozenset({0, 4, 5})
FIXTURE_SOBOL_RNG = 20261006       # 건조 실행 · 시험용 — 정식 배열 아님
BLAS_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
DATA_SUFFIXES = (".xlsx", ".pkl", ".ipynb")
STRUCTURAL = (MemoryError, OSError, KeyboardInterrupt, SystemExit, RecursionError)
STATES = ("NOT_STARTED", "STARTED_INTERRUPTED", "RETURNED_REEVAL_INTERRUPTED", "COMPLETED")
#: v2 §3 — 원점 = 부모 단조 시계 시작 (초)
LIMITS_MEASURE = {"prep": 600.0, "measure": 6300.0, "workers": 6420.0, "record": 6720.0, "total": 7200.0, "grace": 60.0,
                  "rss": 4 * 2 ** 30, "rss_gap": 5.0, "disk_new": 2 ** 30, "disk_free": 5 * 2 ** 30, "disk_gap": 15.0}
#: v2 §5 — 건조 실행: 벽시계 ≤ 300 s · 출력 ≤ 10 MB
LIMITS_DRY = {"prep": 60.0, "measure": 240.0, "workers": 255.0, "record": 280.0, "total": 300.0, "grace": 10.0,
              "rss": 4 * 2 ** 30, "rss_gap": 5.0, "disk_new": 10 * 2 ** 20, "disk_free": 5 * 2 ** 30, "disk_gap": 15.0}
DRY_OPTIONS = dict(OPTIONS, maxfev=50, maxiter=100)
N_WORKERS_MEASURE, N_WORKERS_DRY = 4, 2


class Structural(Exception):
    """구조 오류 — 파일럿 전체 중단 (v2 §2). `info` 는 `classify_exception` 의 결과."""

    def __init__(self, info: dict, partial: dict | None = None):
        super().__init__(info.get("message"))
        self.info = info
        self.partial = partial


class GlobalStop(Exception):
    """전역 중단 (v2 §6) — 식별 · 봉인 · 셀 규칙 · 경계 · 자원."""


# ---------------------------------------------------------------- 공통
def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, Fraction):
        return frac_str(o)
    if hasattr(o, "tolist") and not isinstance(o, (str, bytes)):
        return _jsonable(o.tolist())
    if isinstance(o, float) and not math.isfinite(o):
        return repr(o)                                     # "nan" · "inf" · "-inf" (JSON 표준 밖 토큰을 쓰지 않음)
    if hasattr(o, "item") and not isinstance(o, (str, bytes)):
        return _jsonable(o.item())
    return o


def dump(obj) -> bytes:
    return (json.dumps(_jsonable(obj), ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")


def model_digest(obj) -> str:
    """Model · halfcell 의 내용 해시 (실행 간 · 재평가 격리 확인 — 원본은 전후가 같아야 한다)."""
    h = hashlib.sha256()

    def walk(o):
        if isinstance(o, dict):
            h.update(b"{")
            for k in sorted(o, key=str):
                h.update(repr(k).encode())
                walk(o[k])
            h.update(b"}")
        elif isinstance(o, (list, tuple)):
            h.update(b"[")
            for v in o:
                walk(v)
            h.update(b"]")
        elif hasattr(o, "tobytes") and hasattr(o, "dtype"):
            h.update(f"nd{o.dtype.str}{o.shape}".encode())
            h.update(o.tobytes())
        else:
            h.update(repr(o).encode())
    walk(obj)
    return h.hexdigest()


# ---------------------------------------------------------------- 증인 · 종료 (부속 A §2-1 · §2-2 · v2 §2)
def exact_residuals(x) -> dict:
    """상자 · G 잔차를 **정확 유리수**로 (float 값 그대로의 유리수 · 상자 경계는 십진 문자열). 비유한 x 는 ValueError / OverflowError."""
    fx = [Fraction(float(v)) for v in x]
    if len(fx) != 4:
        raise ValueError(f"x 길이 {len(fx)} ≠ 4")
    box = max(max(Fraction(lo) - v, v - Fraction(hi), Fraction(0)) for v, lo, hi in zip(fx, LO, HI))
    g = max(G_LB - (fx[2] - fx[3]), Fraction(0))
    return {"box": box, "g": g}


def witness(*, solver_error: bool, reeval_error: bool, jv, x) -> str:
    if solver_error:
        return "invalid:SOLVER_ERROR"
    if reeval_error:
        return "invalid:REEVAL_ERROR"                      # C5 한정 새 이유 (v2 §2) — SOLVER_ERROR 를 넓히지 않음
    if jv is None or not math.isfinite(jv):
        return "invalid:NONFINITE"
    try:
        r = exact_residuals(x)
    except (ValueError, OverflowError, TypeError):
        return "invalid:NONFINITE"
    return "valid" if r["box"] <= TOL and r["g"] <= TOL else "invalid:INFEASIBLE_RETURN"


def feasibility_class(x) -> str:
    try:
        r = exact_residuals(x)
    except (ValueError, OverflowError, TypeError):
        return "nonfinite"
    if r["box"] == 0 and r["g"] == 0:
        return "feasible"
    return "within_tol" if r["box"] <= TOL and r["g"] <= TOL else "infeasible"


def termination_of(res) -> str:
    """`converged` (solver success) · `budget` (MAX_EVAL / MAX_ITER) · 그 밖 `unclassified` — 원 status · message 는 행에 따로."""
    from scipy._lib.cobyqa.settings import ExitStatus
    if bool(getattr(res, "success", False)):
        return "converged"
    if getattr(res, "status", None) in (ExitStatus.MAX_EVAL_WARNING.value, ExitStatus.MAX_ITER_WARNING.value):
        return "budget"
    return "unclassified"


# ---------------------------------------------------------------- 오류 분류 (v2 §2 — 전역 중단이 우선)
def _frame_kind(filename: str, util_file) -> str | None:
    f = os.path.realpath(filename)
    if util_file and f == os.path.realpath(str(util_file)):
        return "util"
    if f == str(HERE):
        return "ours"
    if f"{os.sep}scipy{os.sep}" in f:
        return "scipy"
    return None


def classify_exception(exc: BaseException, stage: str, util_file=None) -> dict:
    """발생 단계 (optimize · reeval · label · 그 밖) · 위치 (util · optimizer · ours) · 형 · traceback 요약.

    위치: 가장 안쪽 frame 부터 밖으로 — util frame 을 먼저 만나면 util, 우리 frame 을 먼저 만나면 (그 사이 scipy 를 지났으면 optimizer,
    아니면 ours). numpy 등 그 밖의 frame 은 건너뛴다. 지역 오류는 구조 목록이 아니고 (optimize: util · optimizer) 또는
    (reeval · label: util) 인 것뿐 — 나머지는 전부 구조 오류다."""
    frames = traceback.extract_tb(exc.__traceback__)
    origin, seen_scipy = None, False
    for fr in reversed(frames):
        k = _frame_kind(fr.filename, util_file)
        if k == "util":
            origin = "util"
            break
        if k == "ours":
            origin = "optimizer" if seen_scipy else "ours"
            break
        if k == "scipy":
            seen_scipy = True
    if origin is None:
        origin = "optimizer" if seen_scipy else "ours"
    local = not isinstance(exc, STRUCTURAL) and (
        (stage == "optimize" and origin in ("util", "optimizer")) or (stage in ("reeval", "label") and origin == "util"))
    return {"kind": "local" if local else "structural", "origin": origin, "stage": stage, "type": type(exc).__name__,
            "message": str(exc)[:500], "traceback": [f"{Path(fr.filename).name}:{fr.lineno}:{fr.name}" for fr in frames[-6:]]}


# ---------------------------------------------------------------- 평가 (v2 §2)
class Objective:
    """J_V(x) = sqrt(objective_fun(x, M, halfcell)[1]) — 호출마다 센다 (예외로 끝난 호출 포함) · 비유한은 바꾸지 않고 넘긴다."""

    def __init__(self, util, model, halfcell, progress=None):
        self.util, self.model, self.halfcell, self.progress = util, model, halfcell, progress
        self.n_eval = 0
        self.n_nonfinite = 0

    def __call__(self, x):
        import numpy as np
        self.n_eval += 1
        if self.progress is not None:
            self.progress(self.n_eval)
        f = self.util.objective_fun(np.asarray(x, dtype=float), self.model, self.halfcell)
        v = float(np.sqrt(f[1]))
        if not math.isfinite(v):
            self.n_nonfinite += 1
        return v


def n_out_labels(util, x, halfcell, q_exp) -> dict:
    """외삽 라벨 — 그들 `dVdQ_hc` 1 회 (목적 평가 아님) · 실험 Q 점 중 슬라이스 `Q_*_hc_ad[Q0*_ID:Qmax*_ID]` 범위 밖 수."""
    import numpy as np
    out = util.dVdQ_hc(halfcell[1], halfcell[0], halfcell[3], halfcell[2], *[float(v) for v in x], interp_len=500)
    qe = np.asarray(q_exp, dtype=float)
    res = {}
    for name, q in (("n_out_PE", np.asarray(out[0], float)), ("n_out_NE", np.asarray(out[1], float))):
        seg = q[int(np.argmin(np.abs(q))):int(np.argmax(q))]
        res[name] = "미확인" if seg.size == 0 else int(np.sum((qe < np.min(seg)) | (qe > np.max(seg))))
    return res


def run_one(run: dict, ctx: dict, notify=None, progress=None) -> dict:
    """지역 실행 하나 — 최적화 → (반환점이 있으면) 독립 재평가 1 회 → 라벨. 구조 오류는 `Structural` 로 올린다 (행을 만들지 않음)."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, minimize
    util, uf = ctx["util"], ctx.get("util_file")
    notify = notify or (lambda kind, payload: None)
    t0, c0 = time.monotonic(), time.process_time()
    row = {"run_id": run["run_id"], "seed": run["seed"], "row": run["row"], "x0": [float(v) for v in run["x0"]],
           "worker": run.get("worker"), "t_start": t0}
    obj = Objective(util, copy.deepcopy(ctx["model"]), ctx["halfcell"], progress)
    opts = dict(ctx["options"])
    row["options_received"] = {k: repr(v) for k, v in sorted(opts.items())}
    res, err = None, None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            res = minimize(obj, np.asarray(run["x0"], dtype=float), method="COBYQA",
                           bounds=Bounds([float(v) for v in LO], [float(v) for v in HI]),
                           constraints=LinearConstraint([[0.0, 0.0, 1.0, -1.0]], float(G_LB), np.inf), options=opts)
        except BaseException as e:  # noqa: BLE001 — 분류해서 지역 / 구조로 나눈다
            info = classify_exception(e, "optimize", uf)
            if info["kind"] == "structural":
                raise Structural(info, partial={**row, "n_eval": obj.n_eval}) from None
            err = info
    msgs = sorted({f"{w.category.__name__}: {w.message}" for w in caught})
    if any("Unknown solver options" in m for m in msgs):
        raise Structural({"kind": "structural", "origin": "optimizer", "stage": "optimize", "type": "OptimizeWarning",
                          "message": "알 수 없는 옵션 경고 — fail-closed (부속 A §3-1)", "traceback": msgs[:3]})
    row.update(n_eval=obj.n_eval, n_nonfinite=obj.n_nonfinite, warnings=msgs[:20])
    if err is not None:
        row.update(termination="solver_error", witness="invalid:SOLVER_ERROR", reeval_attempts=0, error=err, x=None, fun=None,
                   status=None, message=None, nfev=None, nit=None, jv_reeval=None, reeval_error=None, residual_box=None,
                   residual_g=None, feasibility_class=None, n_out_PE=None, n_out_NE=None)
    else:
        x = [float(v) for v in res.x]
        row.update(x=x, fun=float(res.fun), status=int(res.status), message=str(res.message),
                   nfev=int(getattr(res, "nfev", -1)), nit=int(getattr(res, "nit", -1)), termination=termination_of(res), error=None)
        notify("returned", {"run_id": run["run_id"], "x": x, "status": row["status"], "message": row["message"],
                            "termination": row["termination"], "n_eval": obj.n_eval})
        row["reeval_attempts"] = 1
        jv, rerr = None, None
        try:
            jv = Objective(util, copy.deepcopy(ctx["model"]), ctx["halfcell"])(np.asarray(x, dtype=float))
        except BaseException as e:  # noqa: BLE001
            info = classify_exception(e, "reeval", uf)
            if info["kind"] == "structural":
                raise Structural(info, partial=row) from None
            rerr = info
        row.update(jv_reeval=jv, reeval_error=rerr,
                   witness=witness(solver_error=False, reeval_error=rerr is not None, jv=jv, x=x),
                   feasibility_class=feasibility_class(x))
        try:
            r = exact_residuals(x)
            row.update(residual_box=frac_str(r["box"]), residual_g=frac_str(r["g"]))
        except (ValueError, OverflowError):
            row.update(residual_box=None, residual_g=None)
        lab = {"n_out_PE": "미확인", "n_out_NE": "미확인"}
        if rerr is None:
            try:
                lab = n_out_labels(util, x, ctx["halfcell"], ctx["model"]["Q_exp_interp"])
            except BaseException as e:  # noqa: BLE001 — 라벨 실패는 '미확인' (증인 불변) · 구조 오류는 전역 중단
                info = classify_exception(e, "label", uf)
                if info["kind"] == "structural":
                    raise Structural(info, partial=row) from None
                lab = {"n_out_PE": "미확인", "n_out_NE": "미확인", "label_error": info}
        row.update(lab)
    t1 = time.monotonic()
    row.update(t_end=t1, wall=t1 - t0, cpu=time.process_time() - c0, state="COMPLETED")
    return row


# ---------------------------------------------------------------- 작업자 · 조정 (v2 §3)
def _threads(pid: int):
    try:
        for ln in Path(f"/proc/{pid}/status").read_text().splitlines():
            if ln.startswith("Threads:"):
                return int(ln.split()[1])
    except OSError:
        return None
    return None


def rss_bytes(pids) -> int:
    """부모 + 작업자 VmRSS 합 (표본). 이미 끝난 pid 는 건너뛴다."""
    tot = 0
    for pid in pids:
        try:
            txt = Path(f"/proc/{pid}/status").read_text()
        except FileNotFoundError:
            continue
        for ln in txt.splitlines():
            if ln.startswith("VmRSS:"):
                tot += int(ln.split()[1]) * 1024
    return tot


def disk_sample(out_dir) -> tuple:
    out_dir = Path(out_dir)
    used = sum(p.stat().st_size for p in out_dir.rglob("*") if p.is_file())
    return used, shutil.disk_usage(out_dir).free


def _worker(wid, runs, ctx, q, stop, prog):
    try:
        q.put(("worker_start", wid, {"pid": os.getpid(), "threads": _threads(os.getpid()), "t": time.monotonic(),
                                     "blas_env": {k: os.environ.get(k) for k in BLAS_VARS}}))
        for run in runs:
            if stop.is_set():
                break
            rid = run["run_id"]
            q.put(("start", rid, {"worker": wid, "t": time.monotonic()}))

            def progress(n, rid=rid):
                prog[rid] = n

            def notify(kind, payload):
                q.put((kind, payload["run_id"], _jsonable({**payload, "t": time.monotonic()})))
            try:
                row = run_one(run, ctx, notify=notify, progress=progress)
            except Structural as s:
                q.put(("structural", rid, {**s.info, "t": time.monotonic()}))
                return
            q.put(("done", rid, _jsonable(row)))
        q.put(("worker_end", wid, {"t": time.monotonic()}))
    except BaseException as e:  # noqa: BLE001 — 작업자 자체의 예외 = 우리 코드 = 구조 오류
        q.put(("structural", None, {**classify_exception(e, "worker", ctx.get("util_file")), "t": time.monotonic()}))


def assemble_states(runs, ev: dict, prog, reason, t_stop) -> list:
    """실행마다 정확히 하나의 상태 — 0 으로 채우지 않는다 · 숨은 재시작 없음 (v2 §3)."""
    out = []
    for r in runs:
        rid = r["run_id"]
        base = {"run_id": rid, "seed": r["seed"], "row": r["row"], "x0": [float(v) for v in r["x0"]], "worker": r["worker"]}
        if rid in ev["done"]:
            out.append({**ev["done"][rid], "state": "COMPLETED"})
        elif rid in ev["returned"]:
            ret = ev["returned"][rid]
            out.append({**base, "state": "RETURNED_REEVAL_INTERRUPTED", "returned": ret, "witness": "미확정",
                        "reeval_complete": False, "elapsed_s": t_stop - ev["started"][rid]["t"] if rid in ev["started"] else None,
                        "interrupt_reason": reason})
        elif rid in ev["started"]:
            n = prog[rid] if prog is not None else 0
            out.append({**base, "state": "STARTED_INTERRUPTED", "n_eval_observed": f"≥ {int(n)} · 미확인",
                        "elapsed_s": t_stop - ev["started"][rid]["t"], "interrupt_reason": reason})
        else:
            out.append({**base, "state": "NOT_STARTED", "interrupt_reason": reason or "작업자가 끝난 뒤 남은 실행"})
    return out


def orchestrate(runs, ctx, *, n_workers, limits, t0, clock=time.monotonic, rss_fn=None, disk_fn=None, out_dir=None,
                tick=1.0, disk_every=5.0) -> dict:
    """실행 → 작업자 배정은 실행 번호로 고정 (`run["worker"]`). 표본 감시 · 단계 경계 · 전역 중단 → 소유 작업자만 종료."""
    import multiprocessing as mp
    mpc = mp.get_context("fork")
    q, stop = mpc.Queue(), mpc.Event()
    prog = mpc.Array("q", max(r["run_id"] for r in runs) + 1, lock=False)
    procs = {w: mpc.Process(target=_worker, args=(w, [r for r in runs if r["worker"] == w], ctx, q, stop, prog), daemon=True)
             for w in range(n_workers)}
    rss_fn = rss_fn or rss_bytes
    disk_fn = disk_fn or disk_sample
    ev = {"started": {}, "returned": {}, "done": {}, "worker_start": {}, "worker_end": {}, "structural": []}
    samples = {"rss": [], "disk": []}
    reason = None

    def handle(msg):
        kind, key, payload = msg
        if kind == "start":
            ev["started"][key] = payload
        elif kind == "returned":
            ev["returned"][key] = payload
        elif kind == "done":
            ev["done"][key] = payload
        elif kind == "worker_start":
            ev["worker_start"][key] = payload
        elif kind == "worker_end":
            ev["worker_end"][key] = payload
        elif kind == "structural":
            ev["structural"].append({"run_id": key, **payload})

    def drain(timeout=0.05):
        while True:
            try:
                handle(q.get(timeout=timeout))
            except queue.Empty:
                return True
            except Exception:  # noqa: BLE001 — 강제 종료 뒤 깨진 메시지 · 읽기 실패는 기록 미완으로 남긴다
                return False

    if clock() - t0 >= limits["measure"]:
        reason = f"단계 경계 — 측정 끝 ({limits['measure']} s) 전에 시작하지 못했다"
    else:
        for p in procs.values():
            p.start()
    last_rss = last_disk = clock()
    last_disk_try = -1e18
    while reason is None:
        try:
            handle(q.get(timeout=tick))
        except queue.Empty:
            pass
        now = clock()
        if ev["structural"]:
            s = ev["structural"][0]
            reason = f"구조 오류: {s.get('type')} ({s.get('origin')} · {s.get('stage')}) {s.get('message')}"[:400]
            break
        if now - t0 >= limits["measure"]:
            reason = f"단계 경계 — 측정 {limits['measure']} s 에 신규 시작 중지 · 진행 중 실행 중단"
            break
        for w, p in procs.items():
            if p.exitcode is not None and w not in ev["worker_end"]:
                drain()
                if not ev["structural"] and w not in ev["worker_end"]:
                    reason = f"작업자 {w} 비정상 종료 (exitcode {p.exitcode}) — 종료 메시지 없음"
                    break
        if reason or ev["structural"]:
            if reason is None:
                continue
            break
        try:
            v = rss_fn([os.getpid()] + [p.pid for p in procs.values() if p.is_alive()])
        except Exception as e:  # noqa: BLE001
            reason = f"감시 실패 (메모리 표본): {type(e).__name__}: {e}"
            break
        if v is not None:
            samples["rss"].append((now - t0, int(v)))
            last_rss = now
            if v > limits["rss"]:
                reason = f"메모리 표본 {v} B > 상한 {limits['rss']} B"
                break
        elif now - last_rss > limits["rss_gap"]:
            reason = f"메모리 표본 누락 {now - last_rss:.1f} s > {limits['rss_gap']} s"
            break
        if now - last_disk_try >= disk_every:
            last_disk_try = now
            try:
                d = disk_fn(out_dir)
            except Exception as e:  # noqa: BLE001
                reason = f"감시 실패 (디스크 표본): {type(e).__name__}: {e}"
                break
            if d is not None:
                used, free = d
                samples["disk"].append((now - t0, int(used), int(free)))
                last_disk = now
                if used > limits["disk_new"] or free < limits["disk_free"]:
                    reason = f"디스크 표본: 새 산출 {used} B (상한 {limits['disk_new']}) · 여유 {free} B (하한 {limits['disk_free']})"
                    break
            elif now - last_disk > limits["disk_gap"]:
                reason = f"디스크 표본 누락 {now - last_disk:.1f} s > {limits['disk_gap']} s"
                break
        if len(ev["worker_end"]) == n_workers:
            break
    t_stop = clock()
    drained_ok = True
    if reason is not None:
        stop.set()
        for p in procs.values():
            if p.is_alive():
                p.terminate()
        deadline = time.monotonic() + limits["grace"]
        for p in procs.values():
            if p.pid is not None:
                p.join(max(0.0, deadline - time.monotonic()))
        for p in procs.values():
            if p.is_alive():
                p.kill()
                p.join(5)
    else:
        for p in procs.values():
            p.join(limits["grace"])
    drained_ok = drain(0.1)
    alive_after = sum(1 for p in procs.values() if p.is_alive())
    states = assemble_states(runs, ev, prog, reason, t_stop)
    return {"states": states, "global_stop": reason, "samples": samples, "workers": ev["worker_start"],
            "worker_end": ev["worker_end"], "structural": ev["structural"], "owned_alive_after": alive_after,
            "drain_ok": drained_ok, "t_stop": t_stop - t0, "exitcodes": {w: p.exitcode for w, p in procs.items()}}


# ---------------------------------------------------------------- 요약 (비용용 — 판정 아님 · v2 §7)
def _stats(xs):
    xs = sorted(float(x) for x in xs if x is not None)
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "min": xs[0], "median": xs[len(xs) // 2], "max": xs[-1], "sum": sum(xs)}


def summarize(states, *, wall=None) -> dict:
    by = Counter(s["state"] for s in states)
    comp = [s for s in states if s["state"] == "COMPLETED"]
    local = [s for s in comp if s.get("termination") == "solver_error" or s.get("witness") == "invalid:REEVAL_ERROR"]
    normal = [s for s in comp if s not in local]
    interrupted = [s for s in states if s["state"] in ("STARTED_INTERRUPTED", "RETURNED_REEVAL_INTERRUPTED")]
    workers = {}
    for s in comp:
        w = workers.setdefault(s.get("worker"), {"runs": 0, "busy_s": 0.0, "cpu_s": 0.0})
        w["runs"] += 1
        w["busy_s"] += float(s.get("wall") or 0.0)
        w["cpu_s"] += float(s.get("cpu") or 0.0)
    busy = [w["busy_s"] for w in workers.values()]
    evals = sum(int(s.get("n_eval") or 0) for s in comp)
    out = {"n_planned": len(states), "by_state": {k: by.get(k, 0) for k in STATES},
           "completed": len(comp), "completed_without_local_error": len(normal), "completed_local_error": len(local),
           "interrupted": len(interrupted), "not_started": by.get("NOT_STARTED", 0),
           "wall_completed_s": _stats(s.get("wall") for s in normal), "wall_local_error_s": _stats(s.get("wall") for s in local),
           "cpu_completed_s": _stats(s.get("cpu") for s in normal),
           "censored_elapsed_s": sorted(float(s["elapsed_s"]) for s in interrupted if s.get("elapsed_s") is not None),
           "censored_note": "중단 실행의 경과는 우측 검열 — 완료 분포에 섞지 않는다",
           "budget_ratio_of_completed": (sum(1 for s in comp if s.get("termination") == "budget") / len(comp)) if comp else None,
           "invalid_ratio_of_completed": (sum(1 for s in comp if str(s.get("witness", "")).startswith("invalid")) / len(comp))
           if comp else None,
           "evals_completed": evals,
           "wall_per_eval_s": (sum(float(s.get("wall") or 0) for s in comp) / evals) if evals else None,
           "workers": workers, "wall_s": wall,
           "occupancy": {str(k): (v["busy_s"] / wall) for k, v in workers.items()} if wall else None,
           "load_imbalance_s": (max(busy) - min(busy)) if busy else None,
           "note": "작업자 관측 wall · CPU · 점유 · 부하 불균형 — 직렬 대조가 없어 speedup · 병렬 효율이라 부르지 않는다"}
    assert sum(out["by_state"].values()) == len(states), "상태가 실행을 빠짐없이 나누지 않는다"
    return out


# ---------------------------------------------------------------- 기록 (v2 §7)
def _write_bytes(path: Path, data: bytes) -> None:
    path.write_bytes(data)


def final_record(out_dir, parts: dict, *, clock=time.monotonic, t0=0.0, limit=float("inf"), write=None) -> dict:
    """행 → 요약 → 자원 → 종료 기록 순서로 쓰고 다시 읽어 해시 → 그 뒤 시각 snapshot 한 번. 실패 · 경계 초과 = `RECORD_INCOMPLETE`
    (이미 쓴 파일은 보존 · 다시 쓰지 않음)."""
    write = write or _write_bytes
    out_dir = Path(out_dir)
    state, files, problems = "COMPLETE", {}, []
    for name, obj in parts.items():
        if clock() - t0 > limit:
            state = "RECORD_INCOMPLETE"
            problems.append(f"최종 기록 단계 경계 {limit} s 초과 — {name} 부터 쓰지 않았다")
            break
        data = dump(obj)
        try:
            write(out_dir / name, data)
            back = (out_dir / name).read_bytes()
        except OSError as e:
            state = "RECORD_INCOMPLETE"
            problems.append(f"{name} 쓰기 실패: {type(e).__name__}: {e}")
            break
        if back != data:
            state = "RECORD_INCOMPLETE"
            problems.append(f"{name} 다시 읽은 바이트가 다르다")
            break
        files[name] = _sha(back)
    return {"record_state": state, "files": files, "problems": problems, "final_snapshot_s": clock() - t0}


def git_state(repo=REPO) -> dict:
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True)
    st = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True)
    return {"head": head.stdout.strip(), "head_rc": head.returncode, "porcelain": st.stdout, "porcelain_rc": st.returncode}


def split_dirty(porcelain: str, own_prefixes) -> dict:
    """작업 트리 줄을 '이 실행의 산출' 과 '그 밖' 으로 — 산출로 생긴 dirty 와 소스 변경을 섞지 않는다."""
    own, other = [], []
    for ln in porcelain.splitlines():
        if not ln.strip():
            continue
        path = ln[3:].strip().strip('"')
        (own if any(path.startswith(str(p).rstrip("/")) for p in own_prefixes) else other).append(ln)
    return {"own_output": own, "other": other}


def source_hashes(paths) -> dict:
    return {str(p): (_sha(Path(p).read_bytes()) if Path(p).is_file() else None) for p in paths}


def source_changed(start: dict, end: dict) -> list:
    return sorted(k for k in set(start) | set(end) if start.get(k) != end.get(k))


# ---------------------------------------------------------------- 식별 · 봉인 (부록 A1 · v2 §4)
def check_options(table: dict, options: dict) -> list:
    """C6 봉인 `COBYQA_OPTIONS.json` 의 `options` 표 ↔ 실제 전달할 옵션 (이름 집합 · repr 값 · 문서화)."""
    bad = []
    if set(table) != set(options):
        bad.append(f"옵션 이름 집합이 다르다: 봉인 {sorted(table)} · 전달 {sorted(options)}")
    for k, v in options.items():
        t = table.get(k)
        if not isinstance(t, dict) or t.get("planned") != repr(v) or t.get("documented") is not True:
            bad.append(f"옵션 {k}: 봉인 {None if t is None else t.get('planned')!r} ≠ 전달 {v!r} (또는 문서화 안 됨)")
    return bad


def env_identity(*, venv, sealed=SEALED, options=OPTIONS, impl_root=None) -> dict:
    """계산 없는 환경 식별 (부록 A1 1–5). 합성 최적화 · Sobol · emit · full check 를 부르지 않는다."""
    probs, rec = [], {}
    rec.update(executable=os.path.realpath(sys.executable), prefix=sys.prefix, version=sys.version, venv=str(venv))
    if os.path.realpath(sys.prefix) != os.path.realpath(str(venv)):
        probs.append(f"interpreter: sys.prefix {sys.prefix} ≠ 지정 venv {venv}")
    sealed = Path(sealed)
    try:
        man_b = (sealed / "MANIFEST.json").read_bytes()
        man = json.loads(man_b)
        rec["seal_manifest_sha256"] = _sha(man_b)
        for n, h in sorted(man.items()):
            if not (sealed / n).is_file() or _sha((sealed / n).read_bytes()) != h:
                probs.append(f"봉인 MANIFEST: {n} 의 바이트가 MANIFEST 와 다르다")
    except (OSError, ValueError) as e:
        probs.append(f"봉인 MANIFEST 를 읽지 못한다: {type(e).__name__}: {e}")
    try:
        lock = prof.lock_text().encode("utf-8")
        rec["lock_sha256_now"] = _sha(lock)
        if lock != (sealed / "REIL_C6.lock.txt").read_bytes():
            probs.append("lock: 지금 설치 (RECORD 대조) 의 lock 바이트가 봉인 REIL_C6.lock.txt 와 다르다")
    except (SystemExit, OSError) as e:
        probs.append(f"lock: {type(e).__name__}: {e}")
    try:
        pb = prof._dump(prof.profile()).encode("utf-8")
        rec["profile_sha256_now"] = _sha(pb)
        if pb != (sealed / "PROFILE.json").read_bytes():
            probs.append("profile: 지금 판 · 플랫폼 · 빌드 메타데이터가 봉인 PROFILE.json 과 다르다")
    except (OSError, ImportError) as e:
        probs.append(f"profile: {type(e).__name__}: {e}")
    try:
        cob = json.loads((sealed / "COBYQA_OPTIONS.json").read_text(encoding="utf-8"))
        probs += check_options(cob["options"], options)
        if impl_root is None:
            import scipy
            impl_root = Path(scipy.__file__).resolve().parents[1]
        for rel, h in sorted(cob["implementation_files_sha256"].items()):
            p = Path(impl_root) / rel
            if not p.is_file() or _sha(p.read_bytes()) != h:
                probs.append(f"COBYQA 구현 파일: {rel} 가 봉인 해시와 다르다")
    except (OSError, ValueError, KeyError) as e:
        probs.append(f"COBYQA_OPTIONS 봉인을 읽지 못한다: {type(e).__name__}: {e}")
    return {"ok": not probs, "problems": probs, "record": rec, "full_c6_check": "NOT_RUN",
            "note": "계산 없는 식별 — 'C6 전체 기능 PASS' 가 아니다 (부록 A1)"}


def pilot_arrays(sealed=SEALED, *, make=None) -> tuple:
    """측정 단계 전용 — A0 seed 0 · 1 배열만 다시 만들어 봉인 npy 와 바이트 대조 (A1 · A2 · unit · 옛 seed= 는 하지 않음)."""
    import numpy as np
    if make is None:
        from scipy.stats import qmc

        def make(seed):
            lo, hi = prof.BOXES["A0_their_box"]
            u = qmc.Sobol(d=4, scramble=True, rng=seed).random_base2(m=6)
            return qmc.scale(u, lo, hi)
    arrays, probs = {}, []
    for seed, name in PILOT_ARRAYS.items():
        a = np.ascontiguousarray(make(seed), dtype="<f8")
        buf = io.BytesIO()
        np.save(buf, a, allow_pickle=False)
        want = (Path(sealed) / name).read_bytes()
        if buf.getvalue() != want:
            probs.append(f"Sobol 파일럿 배열 seed {seed}: 다시 만든 npy 바이트가 봉인 {name} 와 다르다")
        arrays[seed] = a
    return arrays, probs


def plan_runs(arrays: dict, n_workers: int) -> list:
    """실행 번호 = seed × 64 + 행 · 작업자 = 실행 번호 mod n_workers (고정 배정)."""
    import numpy as np
    runs = []
    for seed in sorted(arrays):
        a = np.asarray(arrays[seed], dtype=float)
        if a.ndim != 2 or a.shape[1] != 4 or not np.all(np.isfinite(a)):
            raise GlobalStop(f"시작점 배열 seed {seed} 의 모양 / 유한성이 다르다: {a.shape}")
        for i in range(a.shape[0]):
            rid = seed * SOBOL_N + i
            runs.append({"run_id": rid, "seed": int(seed), "row": i, "x0": [float(v) for v in a[i]], "worker": rid % n_workers})
    return runs


def fixture_starts():
    """건조 실행 · 시험의 시작점 4 — `qmc.Sobol(4, scramble=True, rng=20261006)` (정식 배열 아님 · 봉인과 대조하지 않음)."""
    from scipy.stats import qmc
    lo, hi = prof.BOXES["A0_their_box"]
    return qmc.scale(qmc.Sobol(d=4, scramble=True, rng=FIXTURE_SOBOL_RNG).random_base2(m=2), lo, hi)


def select_cell(res: dict) -> int:
    """셀 고정 규칙 (v2 §1): 번호 순 첫 행 중 A0 τ 0 · 0.02 · 0.05 모두 PRIOR_COMPATIBLE · 경계 행 #0 · #4 · #5 아님 · P0 추출 OK."""
    ok = {e.get("row") for e in res.get("extraction", []) if e.get("kind") == "analysis" and e.get("status") == "OK"}
    comp: dict = {}
    for r in res.get("prior_table", []):
        if r.get("region") == "A0":
            comp.setdefault(r["row"], {})[r["tau"]] = r["status"]
    for i in sorted(comp):
        if i in BOUNDARY_ROWS or i not in ok:
            continue
        if all(comp[i].get(t) == "PRIOR_COMPATIBLE" for t in p0.TAUS):
            return i
    raise GlobalStop("셀 규칙이 고를 행이 없다")


def require_cell(res: dict) -> int:
    i = select_cell(res)
    if i != CELL_ROW:
        raise GlobalStop(f"셀 규칙이 #{i} 를 골랐다 — 고정 #{CELL_ROW} 가 아니면 중지 (다른 셀 fallback 없음)")
    return i


def guard_paths(paths) -> None:
    bad = [str(p) for p in paths if str(p).lower().endswith(DATA_SUFFIXES)]
    if bad:
        raise GlobalStop(f"자료 경로 접근 금지 (이 단계): {bad}")


def load_util(path, expected_sha: str):
    """그들 util 을 sha256 대조 · AST 최상위 검사 (P0 와 같은 규칙) 뒤에 경로로 로드한다 (`.txt` 사본도 같은 방식)."""
    path = Path(path).resolve()
    b = path.read_bytes()
    if _sha(b) != expected_sha:
        raise GlobalStop(f"util sha256 {_sha(b)[:16]} ≠ 기대 {expected_sha[:16]}")
    st = p0.util_static_check(b.decode("utf-8"))
    if not st.get("ok"):
        raise GlobalStop(f"util 최상위 문장 검사 실패: {st.get('bad')}")
    loader = importlib.machinery.SourceFileLoader("reil_util_lfp", str(path))
    spec = importlib.util.spec_from_loader("reil_util_lfp", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod, str(path)


def synthetic_inputs(util) -> tuple:
    """건조 실행 입력 — 해석식 단조 곡선 (REIL 자료 아님). Model 은 그들 `extract_battery_data` 로 만든다 (xlsx 경로 0)."""
    import numpy as np
    q_pe = np.linspace(0.0, 3.2, 400)
    v_pe = 3.25 + 0.15 * q_pe / 3.2 + 0.05 * np.tanh(4.0 * (q_pe - 2.9))
    q_ne = np.linspace(0.0, 3.6, 400)
    v_ne = 0.08 + 0.5 * np.exp(-4.0 * q_ne)
    q = np.linspace(0.0, 2.4, 300)
    v = 2.6 + 0.9 * np.sqrt(q / 2.4)
    model = util.extract_battery_data([np.vstack([q, v])], 0)
    return model, [q_pe, v_pe, q_ne, v_ne]


# ---------------------------------------------------------------- 파일럿 본체 (건조 · 측정 공통)
def run_pilot(*, out_dir: Path, ctx: dict, runs: list, n_workers: int, limits: dict, t0: float, header: dict,
              watch_files: list, clock=time.monotonic) -> int:
    start_hashes = source_hashes(watch_files)
    git0 = git_state()
    model_h0, half_h0 = model_digest(ctx["model"]), model_digest(ctx["halfcell"])
    if clock() - t0 > limits["prep"]:
        raise GlobalStop(f"단계 경계 — 준비 {limits['prep']} s 초과")
    t_meas = clock()
    orch = orchestrate(runs, ctx, n_workers=n_workers, limits=limits, t0=t0, clock=clock, out_dir=out_dir)
    wall = clock() - t_meas
    git1 = git_state()
    end_hashes = source_hashes(watch_files)
    changed = source_changed(start_hashes, end_hashes)
    rel_out = os.path.relpath(out_dir, REPO)
    end = {"git_start": git0, "git_end": git1, "dirty_end": split_dirty(git1["porcelain"], [rel_out]),
           "source_hashes_start": start_hashes, "source_hashes_end": end_hashes, "source_changed": changed,
           "model_digest_start": model_h0, "model_digest_end": model_digest(ctx["model"]),
           "halfcell_digest_start": half_h0, "halfcell_digest_end": model_digest(ctx["halfcell"]),
           "global_stop": orch["global_stop"], "owned_alive_after": orch["owned_alive_after"], "drain_ok": orch["drain_ok"],
           "workers": orch["workers"], "worker_end": orch["worker_end"], "exitcodes": orch["exitcodes"],
           "external_rc": "바깥 래퍼가 따로 적는다"}
    parts = {"ROWS.json": orch["states"], "SUMMARY.json": summarize(orch["states"], wall=wall),
             "RESOURCES.json": orch["samples"], "RUN_RECORD.json": {**header, **end}}
    fr = final_record(out_dir, parts, clock=clock, t0=t0, limit=limits["record"])
    incomplete = fr["record_state"] != "COMPLETE" or bool(changed) or orch["owned_alive_after"] or not orch["drain_ok"] \
        or end["model_digest_start"] != end["model_digest_end"] or end["halfcell_digest_start"] != end["halfcell_digest_end"]
    print(json.dumps({"FINAL_SNAPSHOT_s": fr["final_snapshot_s"], "record_state": fr["record_state"], "files": fr["files"],
                      "record_incomplete": bool(incomplete), "global_stop": orch["global_stop"],
                      "by_state": summarize(orch["states"])["by_state"]}, ensure_ascii=False))
    return 0 if not incomplete and orch["global_stop"] is None else 2


def _new_out(out: Path) -> Path:
    if out.exists():
        raise GlobalStop(f"출력 폴더가 이미 있다: {out} — 중지 (삭제 · 재사용 · 새 이름 우회 없음)")
    out.mkdir(parents=True)
    return out


def cmd_identity(venv, out) -> int:
    r = env_identity(venv=venv)
    Path(out).write_bytes(dump(r))
    print(json.dumps({"ok": r["ok"], "problems": r["problems"], "full_c6_check": r["full_c6_check"]}, ensure_ascii=False))
    return 0 if r["ok"] else 3


def cmd_dryrun(venv, out) -> int:
    t0 = time.monotonic()
    out = _new_out(Path(out))
    ident = env_identity(venv=venv, options=OPTIONS)
    if not ident["ok"]:
        raise GlobalStop(f"환경 식별 실패: {ident['problems']}")
    guard_paths([UTIL_COPY])
    util, uf = load_util(UTIL_COPY, UTIL_COPY_SHA)
    model, halfcell = synthetic_inputs(util)
    runs = plan_runs({0: fixture_starts()}, N_WORKERS_DRY)
    ctx = {"util": util, "util_file": uf, "model": model, "halfcell": halfcell, "options": DRY_OPTIONS}
    header = {"kind": "dryrun (합성 · 비용 근거 아님)", "argv": sys.argv, "cwd": os.getcwd(), "identity": ident,
              "util_copy_sha256": UTIL_COPY_SHA, "options": {k: repr(v) for k, v in DRY_OPTIONS.items()},
              "fixture_sobol": f"qmc.Sobol(4, scramble=True, rng={FIXTURE_SOBOL_RNG}).random_base2(2) · A0 상자",
              "blas_env_set": {k: os.environ.get(k) for k in BLAS_VARS}, "n_workers": N_WORKERS_DRY, "limits": LIMITS_DRY,
              "start_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    return run_pilot(out_dir=out, ctx=ctx, runs=runs, n_workers=N_WORKERS_DRY, limits=LIMITS_DRY, t0=t0, header=header,
                     watch_files=[HERE, UTIL_COPY, SEALED / "MANIFEST.json"])


def load_measure_inputs(util, xlsx):
    """셀 #1 (`15-LFP 16-Gr SOC-10` · step 6 · cell 0) · 노트북 셀 6 의 halfcell — 그들 경로 그대로 (측정 단계 전용)."""
    import numpy as np
    sheet = p0.SHEETS_ANALYSIS[CELL_ROW]
    d = util.visualize_LFP_data(data_file=str(xlsx), sheet_name=sheet, step_idx=p0.STEP_IDX[CELL_ROW], visualize=False)
    model = util.extract_battery_data(data=d, idx=p0.CELL_IDX[CELL_ROW])
    area = 0.25 * np.pi * 1.2 ** 2
    lfp_mass_12, gr_mass_12 = 13.5 * area, 5.77 * area
    pe = util.visualize_LFP_data(data_file=str(xlsx), sheet_name=p0.SHEETS_REF[0], step_idx=p0.REF_STEP)[p0.REF_CELL]
    ne = util.visualize_LFP_data(data_file=str(xlsx), sheet_name=p0.SHEETS_REF[1], step_idx=p0.REF_STEP)[p0.REF_CELL]
    q_pe = pe[0][np.argmin(pe[0]):np.argmax(pe[0])] / lfp_mass_12 * 20.16
    v_pe = pe[1][np.argmin(pe[0]):np.argmax(pe[0])]
    q_ne = ne[0][np.argmin(ne[0]):np.argmax(ne[0])] / gr_mass_12 * 11.4
    v_ne = ne[1][np.argmin(ne[0]):np.argmax(ne[0])]
    return model, [q_pe, v_pe, q_ne, v_ne]


def cmd_measure(venv, out, xlsx, util_path, approval) -> int:
    t0 = time.monotonic()
    if not approval:
        raise GlobalStop("측정은 v2 §10 (2) 의 별도 승인 기록 (--approval) 없이 시작하지 않는다")
    out = _new_out(Path(out))
    ident = env_identity(venv=venv, options=OPTIONS)
    if not ident["ok"]:
        raise GlobalStop(f"환경 식별 실패: {ident['problems']}")
    if _sha(Path(xlsx).read_bytes()) != XLSX_SHA:
        raise GlobalStop("xlsx sha256 이 기대와 다르다")
    arrays, probs = pilot_arrays()
    if probs:
        raise GlobalStop("; ".join(probs))
    require_cell(json.loads(P0_RESULT.read_text(encoding="utf-8")))
    util, uf = load_util(util_path, UTIL_SHA)
    model, halfcell = load_measure_inputs(util, xlsx)
    runs = plan_runs(arrays, N_WORKERS_MEASURE)
    ctx = {"util": util, "util_file": uf, "model": model, "halfcell": halfcell, "options": OPTIONS}
    header = {"kind": "measure (C5 비용 파일럿)", "argv": sys.argv, "cwd": os.getcwd(), "approval": approval, "identity": ident,
              "util_sha256": UTIL_SHA, "xlsx_sha256": XLSX_SHA, "options": {k: repr(v) for k, v in OPTIONS.items()},
              "pilot_arrays_sha256": {s: _sha(a.tobytes()) for s, a in arrays.items()},
              "run_map": "run_id = seed × 64 + row · worker = run_id mod 4",
              "blas_env_set": {k: os.environ.get(k) for k in BLAS_VARS}, "n_workers": N_WORKERS_MEASURE,
              "limits": LIMITS_MEASURE, "start_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    return run_pilot(out_dir=out, ctx=ctx, runs=runs, n_workers=N_WORKERS_MEASURE, limits=LIMITS_MEASURE, t0=t0, header=header,
                     watch_files=[HERE, Path(util_path), Path(xlsx), SEALED / "MANIFEST.json"])


def main(argv=None) -> int:
    import argparse
    for k in BLAS_VARS:                                  # 설정값 (관측은 작업자 Threads 로 따로)
        os.environ[k] = "1"
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("identity", "dryrun", "measure"):
        s = sub.add_parser(name)
        s.add_argument("--venv", required=True)
        s.add_argument("--out", required=True)
        if name == "measure":
            s.add_argument("--xlsx", required=True)
            s.add_argument("--util", required=True)
            s.add_argument("--approval", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "identity":
            return cmd_identity(a.venv, a.out)
        if a.cmd == "dryrun":
            return cmd_dryrun(a.venv, a.out)
        return cmd_measure(a.venv, a.out, a.xlsx, a.util, a.approval)
    except GlobalStop as e:
        print(f"GLOBAL_STOP: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
