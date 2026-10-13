"""REIL C4 — E3a 실행기 · Phase A 배열 정식 봉인 · identity · 계획 건조 (C4 v2 §1 · §4-1 · §4-3 · 상태 문서 §39 C4-0a).

    <venv>/bin/python -I bms-balancing/scripts/reil_c4_e3a.py identity    --venv V --seal S --seal-manifest-sha256 H --out <file.json>
    <venv>/bin/python -I bms-balancing/scripts/reil_c4_e3a.py seal-arrays --venv V --seal S --seal-manifest-sha256 H --out <새 폴더>
    <venv>/bin/python -I bms-balancing/scripts/reil_c4_e3a.py dryrun      --venv V --seal S --seal-manifest-sha256 H --out <새 폴더>
                                                                          --arrays <배열 봉인> --util-copy <util 사본> --p0-result <P0_RESULT.json>

봉인 경로와 전체 MANIFEST sha256 은 **기본값이 없다** (상태 문서 §38 — C4 실행기는 명시 인자로만 받는다).

- **E3a 호출 하나** (`run_e3a_call`): 보존된 util 의 `run_optimization(Model, halfcell, obj_selection, pop_size=50)` 을 노트북 case 표
  (발췌 cell 3 · 11) 그대로 직접 부른다. 노트북은 실행하지 않는다. 호출마다 Model · halfcell 의 깊은 사본을 넘긴다 — 노트북은 case 여섯이
  한 Model 객체를 공유하지만 (발췌 cell 8 `LFP_Models[case].append(data_extract)`) 그들 objective (util 157–236) 가 읽는 키
  (`Q_exp_interp` · `dVdQ_exp_interp` · `V_exp_interp`) 와 쓰는 키가 달라 값은 같다. 평가 수 · 비유한 · 영역 밖은 그들 `objective_fun` ·
  `dVdQ_hc` 를 호출 동안만 감싸 센다 (추가 계산 없음 · 끝나면 되돌린다). `success=True` 는 증거가 아니다 (util 589 의 대입).
- **배열** (`seal_arrays`): Phase A 넷 (A0 · A1/A2 상자 × seed 0 · 1) 을 C6 `reil_c6_profile.sobol` 과 같은 호출로 다시 만들어 수용된 봉인의
  npy 바이트 · raw sha 와 대조한 뒤 새 폴더에 봉인한다. 프로파일 Sobol 2 · 동시 Sobol 16 · label-seed 배열은 만들지 않는다 — 펼칠 상자가
  P0 의 사전표 · max_q 와 H 격자에서 나오므로 (부속 A §3-3 · §3-4 · §3-6) H 실행기 (C4-0b) 의 같은 코드 경로에서 만든다 (`NOT_IN_THIS_SEAL`).
- **건조** (`dryrun` · §39 6): 계획 · seed · 봉인 대조만. util 은 sha · AST 만 보고 import 하지 않는다 — 최적화 · 목적 호출 0.
"""
from __future__ import annotations

import argparse
import ast
import copy
import io
import json
import math
import os
import sys
import time
import traceback
import warnings
from pathlib import Path

HERE = Path(__file__).resolve()
BMS = HERE.parents[1]
if str(BMS) not in sys.path:      # `-I` 실행은 스크립트 폴더를 sys.path 에 넣지 않는다 — 시험과 같은 `scripts.` 모듈 객체를 쓴다
    sys.path.insert(0, str(BMS))
from scripts import reil_c4_monitor as mon  # noqa: E402
from scripts import reil_c5_pilot as c5  # noqa: E402

prof, p0 = c5.prof, c5.p0

#: 노트북 발췌 cell 3 (`case_selection`) · cell 11 (`pop_size=50`) — 건조 실행이 발췌와 다시 대조한다
CASES = {0: [1], 1: [0, 1], 2: [2, 3], 3: [0, 1, 2], 4: [0, 1, 3], 5: [0, 1, 2, 3]}
POP_SIZE = 50
CALL_TEXT = "run_optimization(Model, halfcell, obj_selection, pop_size=50)"
ROWS = tuple(range(11))                                   # P0 분석 행 #0–#10 (발췌 cell 8 의 시트 11)
#: util 사본 564 (`run_multiple_ga` 기본값 — `run_optimization` 은 pop_size 를 넘기지 않는다) · 690–697 (100 세대 · seed 1 · das-dennis 8 분할)
GA_RUNS, GA_POP, N_GEN, NSGA_SEED, NSGA3_PARTITIONS = 20, 50, 100, 1, 8
G_EPS = 1e-4                                              # util 613 · 634 · 655: G = x[3] − x[2] + 1e-4 (≤ 0 이면 실현 가능)
UTIL_FUNCS = ("objective_fun", "dVdQ_hc", "run_optimization", "run_multiple_ga")
EXCERPTS = BMS / "reviews" / "prereview_pybamm_reil_20261003" / "external" / "NOTEBOOK_SOURCE_EXCERPTS.json"
EXCERPTS_SHA = "95cca5f35aaaf72757812068251d72064b464cff6ef3f523c756f33d27d243a9"
ARRAY_NAMES = tuple(f"sobol_{box}_seed{seed}.npy" for box in prof.BOXES for seed in prof.SOBOL_SEEDS)
NOT_IN_THIS_SEAL = {
    "label-seed": "label 이 seed 를 정하는 배열 (부속 A §3-6 '그 밖의 모든 Sobol' — 아래 둘 포함). 펼칠 상자가 P0 의 사전표 · max_q 와 "
                  "H 격자에서 나오므로 H 실행기 (C4-0b) 의 같은 코드 경로에서 만들어 봉인한다",
    "profile-sobol-2": "프로파일 시작 s3 · s4 — 등식 소거 뒤 자유 변수 상자 위 Sobol 2 (부속 A §3-3) → C4-0b",
    "simultaneous-sobol-16": "동시 양립 — 상자 P × N × (d_P 상자) × (d_N 상자) 위 Sobol 16 전부 봉인 · 앞 12 사용 (부속 A §3-4) → C4-0b",
    "timing": "v2 §4-3 — 규칙은 바꾸지 않고 C4 첫 국소 실행 전에 끝낸다. C4-0b 도 첫 국소 실행 전이다 (상태 문서 §40 에 밝힌다)",
}


class E3aStop(Exception):
    """이 단계의 전역 중단 (봉인 불일치 · 출력 충돌 · 자료 경로 · 식별 실패)."""


_OURS = frozenset(os.path.realpath(p) for p in (__file__, mon.__file__, c5.__file__))
_sha, _jsonable = c5._sha, c5._jsonable


def _read(p) -> bytes:
    try:
        return Path(p).read_bytes()
    except OSError as e:
        raise E3aStop(f"{p} 를 읽지 못한다: {type(e).__name__}: {e}") from None


def _json(p):
    try:
        return json.loads(_read(p))
    except ValueError as e:
        raise E3aStop(f"{p} 가 JSON 이 아니다: {e}") from None


def _guard(paths) -> None:
    """자료 경로 (.xlsx · .pkl · .ipynb) 금지 — C5 `guard_paths` 규칙 그대로."""
    try:
        c5.guard_paths(paths)
    except c5.GlobalStop as e:
        raise E3aStop(str(e)) from None


def _ours(message: str, stage: str = "setup") -> dict:
    return {"kind": "structural", "origin": "ours", "stage": stage, "type": "E3aSetup", "message": message, "traceback": []}


# ---------------------------------------------------------------- 계획 (v2 §1)
def algorithm_of(obj_selection) -> dict:
    """util 682–701 의 분기 그대로 — 목적 1 개 GA 20 seed · 2–3 개 NSGA2 · 4 개 NSGA3. 평가 수 = pop × 세대 × seed 수 (산술 · 한도 아님)."""
    n = len(obj_selection)
    if n == 1:
        name, pop, seeds = "GA", GA_POP, list(range(GA_RUNS))
    elif n in (2, 3):
        name, pop, seeds = "NSGA2", POP_SIZE, [NSGA_SEED]
    elif n == 4:
        name, pop, seeds = "NSGA3", math.comb(NSGA3_PARTITIONS + n - 1, n - 1), [NSGA_SEED]     # das-dennis(4, 8) = 165 방향
    else:
        raise ValueError(f"목적 수 {n} — util 은 1–4 만 받는다 (util 699)")
    return {"name": name, "pop": pop, "gen": N_GEN, "seeds": seeds, "expected_evals": pop * N_GEN * len(seeds)}


def plan_calls(n_workers: int) -> list:
    """호출 번호 = case × 11 + 행 · 작업자 = 호출 번호 mod n_workers (고정 배정). 값은 순서와 무관하다 — 호출마다 그들 seed 로 새로 시작하고
    Model 은 사본이다. case 순으로 두면 GA 11 호출 (호출당 평가 100,000) 이 작업자 넷에 3 · 3 · 3 · 2 로 갈린다."""
    if n_workers < 1:
        raise ValueError("n_workers ≥ 1")
    calls = []
    for case in sorted(CASES):
        for row in ROWS:
            cid = case * len(ROWS) + row
            sel = list(CASES[case])
            calls.append({"call_id": cid, "task_id": cid, "case": case, "row": row, "obj_selection": sel,
                          "algorithm": algorithm_of(sel), "worker": cid % n_workers})
    return calls


# ---------------------------------------------------------------- 오류 분류 · 계수
def classify(exc: BaseException, util_file) -> dict:
    """E3a 오류 분류 — 형 · 메시지 · traceback 요약 · 구조 목록은 C5 `classify_exception` 그대로, 위치만 E3a 규칙으로 다시 정한다.

    C5 의 `_frame_kind` 는 자기 파일만 '우리' 로 알아 이 실행기 · 감시 모듈의 frame 을 건너뛴다 — 그러면 계수용 감싸기 안의 오류가 그 바깥
    util frame 때문에 '지역 (util)' 이 된다. 여기서는 가장 안쪽부터 밖으로 걸어 처음 만나는 util frame 이면 util, e3a · monitor · c5 frame
    이면 우리 — pymoo · scipy · numpy 등 라이브러리 frame 은 건너뛴다 (그들 코드 경로 안). 지역 = 구조 목록 밖 且 위치 util · 나머지는 구조."""
    info = c5.classify_exception(exc, "optimize", util_file)
    uf = os.path.realpath(str(util_file)) if util_file else None
    origin = "ours"
    for fr in reversed(traceback.extract_tb(exc.__traceback__)):
        f = os.path.realpath(fr.filename)
        if f == uf:
            origin = "util"
            break
        if f in _OURS:
            break
    local = origin == "util" and not isinstance(exc, c5.STRUCTURAL)
    info.update(kind="local" if local else "structural", origin=origin, c5_origin=info["origin"])
    return info


def _n_out(q, qe):
    """실험 Q 점 중 그들 슬라이스 `q[argmin|q| : argmax q]` (util 178–185) 범위 밖 수 · 빈 슬라이스면 None (미확인). C5 `n_out_labels` 와 같은 식."""
    import numpy as np
    q = np.asarray(q, dtype=float)
    seg = q[int(np.argmin(np.abs(q))):int(np.argmax(q))]
    if seg.size == 0:
        return None
    return int(np.sum((qe < np.min(seg)) | (qe > np.max(seg))))


def _tally(st: dict, v) -> None:
    """평가 하나의 영역 밖 표 (그 평가가 `dVdQ_hc` 에 닿았을 때만 · 뒤에 예외로 끝나도 센다)."""
    if v is None:
        return
    pe, ne = v
    st["n_dvdq_observed"] += 1
    st["n_out_unknown_eval"] += int(pe is None or ne is None)
    st["n_out_eval_PE"] += int(bool(pe))
    st["n_out_eval_NE"] += int(bool(ne))
    st["n_out_eval_any"] += int(bool(pe) or bool(ne))


class _WarnCount:
    """경고를 쌓지 않고 (형 · 문구) 별로 센다 — GA 호출은 평가 100,000 이라 경고 목록을 저장하지 않는다. 서로 다른 문구는 50 개까지."""
    LIMIT = 50

    def __init__(self):
        self.counts: dict = {}
        self.overflow = 0

    def __call__(self, message, category, filename, lineno, file=None, line=None):
        key = f"{category.__name__}: {str(message)[:200]}"
        if key in self.counts or len(self.counts) < self.LIMIT:
            self.counts[key] = self.counts.get(key, 0) + 1
        else:
            self.overflow += 1


def _rows(a, ncol=None):
    """2 차원 float 배열로 — 모양 · 형이 안 맞으면 None (기록에는 원형이 따로 남는다)."""
    import numpy as np
    try:
        m = np.atleast_2d(np.asarray(a, dtype=float))
    except (TypeError, ValueError):
        return None
    if m.ndim != 2 or (ncol is not None and m.shape[1] != ncol):
        return None
    return m


def _g_violation(x):
    """그들 식 그대로 (float): max(0, x[3] − x[2] + 1e-4) · 비유한이면 None."""
    v = float(x[3]) - float(x[2]) + G_EPS
    return max(0.0, v) if math.isfinite(v) else None


def _exact(x) -> dict:
    """정확 유리수 잔차 (C5 증인 규칙 · 상자 = A0 · G 하한 십진 1e-4)."""
    try:
        r = c5.exact_residuals(x)
        return {"g": c5.frac_str(r["g"]), "box": c5.frac_str(r["box"])}
    except (ValueError, OverflowError):
        return {"g": None, "box": None}


# ---------------------------------------------------------------- E3a 호출 하나 (v2 §1 · §4-1)
def run_e3a_call(task: dict, ctx: dict, notify=None, progress=None) -> dict:
    """`util.run_optimization(Model 사본, halfcell 사본, obj_selection, pop_size=50)` 1 회.

    ctx: {"util", "util_file", "models": {행: Model}, "halfcell", "extraction": {행: P0 추출 기록}}. 그들 util 의 오류 (위치 util · 구조 목록
    밖) 는 '지역' 오류 행으로 남기고, 그 밖 (MemoryError · OSError · 우리 코드 · …) 은 `mon.Structural` 로 올린다 (행을 만들지 않음)."""
    import numpy as np
    util, uf = ctx["util"], ctx.get("util_file")
    sel, r = list(task["obj_selection"]), task["row"]
    if CASES.get(task.get("case")) != sel or task.get("algorithm") != algorithm_of(sel):
        raise mon.Structural(_ours(f"계획 불일치 — case {task.get('case')} · 목적 {sel} · 알고리즘이 노트북 표 / util 분기와 다르다"))
    if r not in ctx["models"] or r not in ctx["extraction"] or "Q_exp_interp" not in ctx["models"][r]:
        raise mon.Structural(_ours(f"행 #{r} 의 Model (Q_exp_interp) 또는 P0 추출 기록이 없다"))
    t0, c0 = time.monotonic(), time.process_time()
    row = {k: task[k] for k in ("task_id", "call_id", "case", "row", "obj_selection", "algorithm", "worker") if k in task}
    base_model, base_hc = ctx["models"][r], ctx["halfcell"]
    digests = (c5.model_digest(base_model), c5.model_digest(base_hc))
    model, halfcell = copy.deepcopy(base_model), copy.deepcopy(base_hc)
    qe = np.asarray(model["Q_exp_interp"], dtype=float)
    lo, hi = (np.asarray(v, dtype=float) for v in prof.BOXES["A0_their_box"])
    st = dict.fromkeys(("n_eval", "n_nonfinite", "n_nonfinite_any_of_4", "n_out_eval_PE", "n_out_eval_NE", "n_out_eval_any",
                        "n_out_unknown_eval", "n_dvdq_observed", "n_eval_x_out_of_box", "n_eval_G_violated"), 0)
    cur = {"v": None}
    real_obj, real_dv = util.objective_fun, util.dVdQ_hc

    def counted_dv(*a, **k):
        out = real_dv(*a, **k)
        cur["v"] = (_n_out(out[0], qe), _n_out(out[1], qe))
        return out

    def counted_obj(x, *a, **k):
        st["n_eval"] += 1                                    # 예외로 끝난 평가도 센다
        if progress is not None:
            progress(st["n_eval"])
        xv = np.asarray(x, dtype=float).ravel()
        if xv.size == 4:
            st["n_eval_x_out_of_box"] += int(bool(np.any(xv < lo) or np.any(xv > hi)))
            st["n_eval_G_violated"] += int(bool(xv[3] - xv[2] + G_EPS > 0))
        cur["v"] = None
        try:
            f = real_obj(x, *a, **k)
        finally:
            _tally(st, cur["v"])
        fv = np.asarray(f, dtype=float).ravel()
        st["n_nonfinite"] += int(not np.all(np.isfinite(fv[[i for i in sel if i < fv.size]])))   # optimizer 가 받은 목적
        st["n_nonfinite_any_of_4"] += int(not np.all(np.isfinite(fv)))
        return f

    res, err, wc = None, None, _WarnCount()
    util.objective_fun, util.dVdQ_hc = counted_obj, counted_dv
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("always")
            warnings.showwarning = wc
            try:
                res = util.run_optimization(model, halfcell, sel, pop_size=POP_SIZE)
            except BaseException as e:  # noqa: BLE001 — 분류해서 지역 / 구조로 나눈다
                info = classify(e, uf)
                if info["kind"] == "structural":
                    raise mon.Structural(info, partial={**row, **st}) from None
                err = info
    finally:
        util.objective_fun, util.dVdQ_hc = real_obj, real_dv
    if (c5.model_digest(base_model), c5.model_digest(base_hc)) != digests:
        raise mon.Structural(_ours("원본 Model / halfcell 이 호출 뒤 달라졌다 — 격리 실패", stage="record"))
    row.update(st)
    row.update(extraction=copy.deepcopy(ctx["extraction"][r]), model_digest=digests[0], halfcell_digest=digests[1],
               warnings_count=wc.counts, warnings_distinct_overflow=wc.overflow, success_is_evidence=False,
               n_eval_minus_expected=st["n_eval"] - task["algorithm"]["expected_evals"])
    if err is not None:
        row.update(termination="error", error=err, X=None, F=None, G=None, G_status="미반환 (호출 오류)", n_solutions=None,
                   F_nonfinite_count=None, G_violation_recomputed=None, G_violation_exact=None, box_violation_exact=None,
                   success_reported=None)
    else:
        X, F, G = (getattr(res, k, None) for k in ("X", "F", "G"))
        xs = None if X is None else _rows(X, 4)            # np.asarray(None, float) 은 nan 이 된다 — None 은 따로 둔다
        fs = None if F is None else _rows(F)
        ex = None if xs is None else [_exact(x) for x in xs]
        s = getattr(res, "success", None)
        row.update(termination="returned", error=None,
                   X=None if X is None else _jsonable(X), F=None if F is None else _jsonable(F),
                   G=None if G is None else _jsonable(G), G_status="없음" if G is None else "보고됨",
                   n_solutions=None if xs is None else int(xs.shape[0]),
                   F_nonfinite_count=None if fs is None else int(np.sum(~np.all(np.isfinite(fs), axis=1))),
                   G_violation_recomputed=None if xs is None else [_g_violation(x) for x in xs],
                   G_violation_exact=None if ex is None else [e["g"] for e in ex],
                   box_violation_exact=None if ex is None else [e["box"] for e in ex],
                   success_reported=bool(s) if isinstance(s, (bool, np.bool_)) else (None if s is None else repr(s)))
    t1 = time.monotonic()
    row.update(wall=t1 - t0, cpu=time.process_time() - c0, state="COMPLETED")
    return row


# ---------------------------------------------------------------- Phase A 배열 정식 봉인 (v2 §4-3)
def _sobol_make(seed: int, box: str):
    from scipy.stats import qmc
    lo, hi = prof.BOXES[box]
    return qmc.scale(qmc.Sobol(d=prof.SOBOL_D, scramble=True, rng=seed).random_base2(m=prof.SOBOL_M), lo, hi)


def phase_a_arrays(make=None) -> dict:
    """Phase A 넷 — C6 `reil_c6_profile.sobol` 과 같은 호출 · 같은 저장 형식 (`<f8` · C 연속)."""
    import numpy as np
    make = make or _sobol_make
    return {f"sobol_{box}_seed{seed}.npy": np.ascontiguousarray(make(seed, box), dtype="<f8")
            for box in prof.BOXES for seed in prof.SOBOL_SEEDS}


def seal_arrays(out, *, c6_seal, make=None, c6_manifest_sha256=None) -> dict:
    """다시 만든 넷을 수용된 봉인 (C6) 의 npy 바이트 · SOBOL_PHASE_A.json 의 raw / npy sha 와 대조 → 전부 같을 때만 새 폴더에 쓴다.
    폴더가 이미 있거나 하나라도 다르면 아무것도 쓰지 않고 `E3aStop`."""
    import numpy as np
    import scipy
    out, c6 = Path(out), Path(c6_seal)
    if out.exists():
        raise E3aStop(f"{out} 가 이미 있다 — 봉인 폴더는 새로 만든다 (덮어쓰지 않음)")
    man_b = _read(c6 / "MANIFEST.json")
    c6_man_sha = _sha(man_b)
    if c6_manifest_sha256 is not None and c6_man_sha != c6_manifest_sha256:
        raise E3aStop(f"수용된 봉인 MANIFEST sha256 {c6_man_sha} ≠ 명시 {c6_manifest_sha256}")
    try:
        c6_man = json.loads(man_b)
    except ValueError as e:
        raise E3aStop(f"수용된 봉인 MANIFEST 가 JSON 이 아니다: {e}") from None
    for n in ARRAY_NAMES + ("SOBOL_PHASE_A.json",):
        if c6_man.get(n) is None or _sha(_read(c6 / n)) != c6_man[n]:
            raise E3aStop(f"수용된 봉인의 {n} 가 그 MANIFEST 와 다르다")
    c6_sobol = _json(c6 / "SOBOL_PHASE_A.json").get("arrays", {})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        arrays = phase_a_arrays(make)
    blobs, meta, probs = {}, {}, []
    for name, a in arrays.items():
        buf = io.BytesIO()
        np.save(buf, a, allow_pickle=False)
        b, c6_npy = buf.getvalue(), _read(c6 / name)
        want = c6_sobol.get(name[len("sobol_"):-len(".npy")], {})
        rec = {"shape": list(a.shape), "dtype": a.dtype.str, "raw_float64_le_sha256": _sha(a.tobytes()), "npy_sha256": _sha(b),
               "c6_npy_sha256": _sha(c6_npy), "c6_raw_float64_le_sha256": want.get("raw_float64_le_sha256"),
               "c6_record_npy_sha256": want.get("npy_sha256")}
        if b != c6_npy:
            probs.append(f"{name}: 다시 만든 npy 바이트 ≠ 수용된 봉인")
        if rec["raw_float64_le_sha256"] != rec["c6_raw_float64_le_sha256"] or rec["npy_sha256"] != rec["c6_record_npy_sha256"]:
            probs.append(f"{name}: raw / npy sha256 ≠ 수용된 봉인 SOBOL_PHASE_A.json")
        blobs[name], meta[name] = b, rec
    if probs:
        raise E3aStop("Phase A 배열 불일치 — 아무것도 쓰지 않았다: " + "; ".join(probs))
    arrays_json = {
        "schema": "reil-c4-arrays-v1", "scope": "C4-0a · Phase A 넷 (C4 v2 §4-3 · 상태 문서 §39 · §40)",
        "call": f"scipy.stats.qmc.Sobol(d={prof.SOBOL_D}, scramble=True, rng=<seed>).random_base2(m={prof.SOBOL_M}) → qmc.scale(unit, lo, hi)",
        "save": "np.save(np.ascontiguousarray(a, dtype='<f8'), allow_pickle=False)", "boxes": prof.BOXES,
        "seeds": list(prof.SOBOL_SEEDS), "arrays": meta, "c6_seal": str(c6), "c6_manifest_sha256": c6_man_sha,
        "generation_warnings": sorted({f"{w.category.__name__}: {w.message}" for w in caught}),
        "env": {"python": sys.version, "executable": sys.executable, "numpy": np.__version__, "scipy": scipy.__version__},
        "not_in_this_seal": NOT_IN_THIS_SEAL,
    }
    aj = mon._dump(arrays_json)
    man = {"ARRAYS.json": _sha(aj), **{n: _sha(b) for n, b in blobs.items()}}
    mb = mon._dump(man)
    out.mkdir(exist_ok=False)
    for name, b in blobs.items():
        (out / name).write_bytes(b)
    (out / "ARRAYS.json").write_bytes(aj)
    (out / "MANIFEST.json").write_bytes(mb)
    back = {n: _sha((out / n).read_bytes()) for n in man}
    if back != man or (out / "MANIFEST.json").read_bytes() != mb:
        raise E3aStop("봉인 폴더를 다시 읽은 바이트가 쓴 것과 다르다")
    return {"ok": True, "out": str(out), "manifest": man, "manifest_sha256": _sha(mb), "c6_manifest_sha256": c6_man_sha,
            "generation_warnings": arrays_json["generation_warnings"]}


def check_arrays(arrays_dir, manifest_sha256) -> dict:
    """C4 배열 봉인 폴더 대조 — MANIFEST 의 이름 집합 · 바이트 · ARRAYS.json 이 명시한 수용 봉인 (C6) MANIFEST 에 묶였는가."""
    d = Path(arrays_dir)
    mb = _read(d / "MANIFEST.json")
    try:
        man = json.loads(mb)
    except ValueError as e:
        raise E3aStop(f"배열 봉인 MANIFEST 가 JSON 이 아니다: {e}") from None
    want = sorted(("ARRAYS.json",) + ARRAY_NAMES)
    if sorted(man) != want:
        raise E3aStop(f"배열 봉인 MANIFEST 의 이름 집합이 다르다: {sorted(man)}")
    bad = [n for n in want if _sha(_read(d / n)) != man[n]]
    if bad:
        raise E3aStop(f"배열 봉인: {bad} 의 바이트가 MANIFEST 와 다르다")
    meta = _json(d / "ARRAYS.json")
    if meta.get("c6_manifest_sha256") != manifest_sha256:
        raise E3aStop(f"배열 봉인의 수용 봉인 MANIFEST {meta.get('c6_manifest_sha256')} ≠ 명시 {manifest_sha256}")
    if any(meta.get("arrays", {}).get(n, {}).get("npy_sha256") != man[n] for n in ARRAY_NAMES):
        raise E3aStop("ARRAYS.json 의 npy sha256 이 MANIFEST 와 다르다")
    return {"arrays_dir": str(d), "manifest_sha256": _sha(mb), "manifest": man, "c6_manifest_sha256": manifest_sha256}


# ---------------------------------------------------------------- identity · 건조
def identity(*, venv, seal, manifest_sha256, env_identity=None) -> dict:
    """계산 없는 환경 식별 (C5 `env_identity` 재사용) + 명시한 봉인의 전체 MANIFEST sha256 대조. full C6 check 는 부르지 않는다 —
    C4-ENV 의 check 1 회로 인정 (상태 문서 §38)."""
    seal = Path(seal)
    r = dict((env_identity or c5.env_identity)(venv=venv, sealed=seal))
    r["problems"] = list(r.get("problems", []))
    try:
        got = _sha(seal.joinpath("MANIFEST.json").read_bytes())
    except OSError as e:
        got = None
        r["problems"].append(f"봉인 MANIFEST 를 읽지 못한다: {type(e).__name__}: {e}")
    if got is not None and got != manifest_sha256:
        r["problems"].append(f"봉인 MANIFEST sha256 {got} ≠ 명시 {manifest_sha256}")
    r.update(ok=bool(r.get("ok")) and not r["problems"], seal_path=str(seal), manifest_sha256_expected=manifest_sha256,
             manifest_sha256_actual=got, full_c6_check="CREDITED — C4-ENV 의 C6 check 1 회 (상태 문서 §38) · 여기서는 부르지 않음")
    return r


def notebook_case_table(path=EXCERPTS) -> dict:
    """노트북 발췌 (P0 가 원 노트북 셀과 바이트로 대조한 묶음) 의 case 표 · 호출 문구를 이 모듈의 상수와 대조한다 (노트북은 열지 않는다)."""
    b = _read(path)
    if _sha(b) != EXCERPTS_SHA:
        raise E3aStop(f"노트북 발췌 sha256 {_sha(b)} ≠ 기대 {EXCERPTS_SHA}")
    cells = {c["cell_index"]: "".join(c["source"]) for c in json.loads(b)["cells"]}
    table = None
    for node in ast.parse(cells[3]).body:
        if isinstance(node, ast.Assign) and [getattr(t, "id", None) for t in node.targets] == ["case_selection"]:
            table = ast.literal_eval(node.value)
    if table != CASES or CALL_TEXT not in cells[11]:
        raise E3aStop(f"노트북 발췌의 case 표 / 호출이 상수와 다르다: {table!r}")
    return {"excerpts": str(path), "excerpts_sha256": EXCERPTS_SHA, "case_selection_equal": True, "call_text_present": True,
            "cell8_one_model_shared_by_cases": "LFP_Models[case].append(data_extract)" in cells[8]}


def dryrun(out, *, venv, seal, manifest_sha256, arrays_dir, util_copy, p0_result, env_identity=None, n_workers=4) -> dict:
    """무자료 건조 (§39 6) — identity · util 사본 (sha · AST · import 0) · 노트북 발췌 case 표 · 배열 봉인 · P0 추출 기록 → PLAN.json. 최적화 호출 0."""
    out = Path(out)
    _guard([out, seal, arrays_dir, util_copy, p0_result])
    if out.exists():
        raise E3aStop(f"{out} 가 이미 있다 — 덮어쓰지 않는다")
    t0 = time.monotonic()
    ident = identity(venv=venv, seal=seal, manifest_sha256=manifest_sha256, env_identity=env_identity)
    if not ident["ok"]:
        raise E3aStop(f"identity 실패: {ident['problems']}")
    ub = _read(util_copy)
    if _sha(ub) != c5.UTIL_COPY_SHA:
        raise E3aStop(f"util 사본 sha256 {_sha(ub)} ≠ 기대 {c5.UTIL_COPY_SHA}")
    ust = p0.util_static_check(ub.decode("utf-8"))
    missing = [f for f in UTIL_FUNCS if f not in ust["functions"]]
    if not ust["ok"] or missing:
        raise E3aStop(f"util 사본 정적 검사 실패: {ust['bad']} · 없는 함수 {missing}")
    nb = notebook_case_table()
    arr = check_arrays(arrays_dir, manifest_sha256)
    p0b = _read(p0_result)
    try:
        res = json.loads(p0b)
    except ValueError as e:
        raise E3aStop(f"P0 결과가 JSON 이 아니다: {e}") from None
    ext = {e.get("row"): e for e in res.get("extraction", []) if e.get("kind") == "analysis"}
    if set(ext) != set(ROWS) or any(ext[r].get("status") != "OK" for r in ROWS):
        raise E3aStop(f"P0 분석 추출 기록이 #0–#10 전부 OK 가 아니다: {sorted(ext, key=str)}")
    if res.get("notebook_check", {}).get("ok") is not True:
        raise E3aStop("P0 의 노트북 대조가 ok 가 아니다")
    calls = plan_calls(n_workers)
    for c in calls:
        c["extraction"] = ext[c["row"]]
    by_worker: dict = {}
    for c in calls:
        by_worker[c["worker"]] = by_worker.get(c["worker"], 0) + c["algorithm"]["expected_evals"]
    plan = {
        "schema": "reil-c4-e3a-plan-v1",
        "scope": "C4-0a 무자료 건조 (상태 문서 §39 6) — 계획 · seed · 봉인 대조만 · 자료 개봉 0 · util import 0 · 최적화 / 목적 호출 0",
        "optimizer_calls": 0, "objective_calls": 0, "util_imported": False,
        "n_calls": len(calls), "n_workers": n_workers, "calls": calls,
        "expected_evals_total": sum(c["algorithm"]["expected_evals"] for c in calls),
        "expected_evals_by_worker": {str(w): v for w, v in sorted(by_worker.items())},
        "optimizer_runs_total": sum(len(c["algorithm"]["seeds"]) for c in calls),
        "cases": {str(k): v for k, v in CASES.items()}, "pop_size": POP_SIZE, "call_text": CALL_TEXT,
        "algorithm_source": "util 사본 564–591 (GA 20 seed · pop 50 · 100 세대) · 682–701 (NSGA2 pop 50 · NSGA3 das-dennis(4, 8) = 165 · "
                            "100 세대 · seed 1) — 평가 수는 pop × 세대 × seed 의 산술 (한도 아님)",
        "util_copy": str(util_copy), "util_copy_sha256": c5.UTIL_COPY_SHA,
        "util_static": {"ok": ust["ok"], "required_functions": list(UTIL_FUNCS)},
        "notebook": nb, "p0_notebook_check_ok": True, "arrays": arr,
        "p0_result": str(p0_result), "p0_result_sha256": _sha(p0b), "identity": ident,
        "not_this_step": "C4-E (66 호출 실제 실행) · 자료 개봉 · 맞춤 · H — 별도 승인",
        "elapsed_s": time.monotonic() - t0,
    }
    data = mon._dump(plan)
    out.mkdir(exist_ok=False)
    (out / "PLAN.json").write_bytes(data)
    if (out / "PLAN.json").read_bytes() != data:
        raise E3aStop("PLAN.json 을 다시 읽은 바이트가 쓴 것과 다르다")
    return {"ok": True, "out": str(out), "plan_sha256": _sha(data), "n_calls": len(calls), "optimizer_calls": 0,
            "expected_evals_total": plan["expected_evals_total"], "identity_ok": True}


# ---------------------------------------------------------------- CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="reil_c4_e3a", description=(__doc__ or "").splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("identity", "seal-arrays", "dryrun"):
        s = sub.add_parser(name)
        s.add_argument("--venv", required=True)
        s.add_argument("--seal", required=True, type=Path)
        s.add_argument("--seal-manifest-sha256", required=True)
        s.add_argument("--out", required=True, type=Path)
        if name == "dryrun":
            s.add_argument("--arrays", required=True, type=Path)
            s.add_argument("--util-copy", required=True, type=Path)
            s.add_argument("--p0-result", required=True, type=Path)
            s.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "identity":
            _guard([a.out, a.seal])
            if a.out.exists():
                raise E3aStop(f"{a.out} 가 이미 있다")
            r = identity(venv=a.venv, seal=a.seal, manifest_sha256=a.seal_manifest_sha256)
            a.out.write_bytes(mon._dump(r))
            summary = {"ok": r["ok"], "problems": r["problems"]}
        elif a.cmd == "seal-arrays":
            _guard([a.out, a.seal])
            ident = identity(venv=a.venv, seal=a.seal, manifest_sha256=a.seal_manifest_sha256)
            if not ident["ok"]:
                raise E3aStop(f"identity 실패: {ident['problems']}")
            summary = {**seal_arrays(a.out, c6_seal=a.seal, c6_manifest_sha256=a.seal_manifest_sha256), "identity": ident}
        else:
            summary = dryrun(a.out, venv=a.venv, seal=a.seal, manifest_sha256=a.seal_manifest_sha256, arrays_dir=a.arrays,
                             util_copy=a.util_copy, p0_result=a.p0_result, n_workers=a.workers)
    except E3aStop as e:
        print(json.dumps({"ok": False, "stop": str(e)}, ensure_ascii=False))
        return 3
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary.get("ok") else 3


if __name__ == "__main__":
    sys.exit(main())
