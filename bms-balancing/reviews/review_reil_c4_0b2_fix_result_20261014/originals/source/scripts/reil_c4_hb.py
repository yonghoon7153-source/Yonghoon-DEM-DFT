"""REIL C4-0b2 — Phase B (프로파일 · 동시 · 명목) · 적응적 시작점 봉인 · H4 대조 · 표지 · 연결부 · 읽기 전용 건조 (상태 문서 §55).

근거: 범위 확인 요청 `docs/REIL_C4_0B2_CONFIRMATION_REQUEST_20261014.md` (사용자 "권고대로" — ray 유보 · 한 번에 · reil_c4_h 의 지역 실행기 일반화) ·
부속 A §1-1 (공통 갱신) · §1-2–§1-4 (문턱) · §2 (증인 · 수치 규칙) · §3-2–§3-8 (순서 · 프로파일 · 동시 · 명목 · seed · 보고 · 상한) ·
§4-4–§4-6 (H4 대조 · ray) · §7 (라벨) · 부속 B §1-2–§1-3 (등급 · 라벨) · §2 (적응적 시작점 봉인 · 부족) · §4 (수용 범위) · v2 §4-4–§4-5 ·
재검토 회신 2026-10-14 §5 (연결부 순서 · 공통 갱신 1 회 · 7,040 은 끝점 게이트만 반영한 계획 수).

    <venv>/bin/python -I bms-balancing/scripts/reil_c4_hb.py dryrun-b --venv <venv> --seal <C6 봉인> --seal-manifest-sha256 <sha>
        --arrays <Phase A 배열> --h-arrays <0b1 배열> --h-manifest-sha256 <sha> --util-copy <util 사본> --p0-result <P0> --out <새 폴더>

연결부: 단계 A (C4-A — 1 파 Phase A → 저장된 기록으로 완료 대조 → ρ 2 파) · 단계 B (C4-B — 단위마다 프로파일 → 동시 → 명목 · H4 는 대조 뒤
Phase B · ray 에 닿으면 RayNotImplemented → 등록 탐색 대조 → 공통 갱신 1 회 → 같은 최종 저장점 집합의 판독 · 표지).
이 파일이 아닌 것: ray (유보 — 미구현 · 완료로 세지 않음) · 보고 서식 (H1 머리말 · U-a…U-e — C4-B 보고 단계) · E3a 완료 확인 (C4-A 실행기) ·
자료 개봉 · 맞춤 · 실제 H 실행 (C4-A · C4-B). 건조는 계획 · seed · 봉인만 읽는다 (합성 실행 · Sobol 생성 0).
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import sys
import time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve()
BMS = HERE.parents[1]
if str(BMS) not in sys.path:
    sys.path.insert(0, str(BMS))

from scripts import reil_c4_h as h  # noqa: E402

mon, c5, p0, e3a = h.mon, h.c5, h.p0, h.e3a
HStop = h.HStop


class RayNotImplemented(HStop):
    """ray (부속 A §4-6) 는 유보 — 미구현 (범위 확인 §9-2). 연결부가 ray 단계에 닿으면 그 (셀 · 영역) 을 갱신하지 않고 멈춘다."""


class WaveStop(HStop):
    """단계 A 의 ρ 파가 전역 중지로 끝났다 (C4B2-N1) — 중지 원문 (reason) 을 들고 올라가, 남은 ρ 를 실행 없이 분류한 뒤 멈춘다."""

    def __init__(self, message, reason):
        super().__init__(message)
        self.reason = reason


#: 부속 A §4-4 — 사전 고정 후보 (이 순서) · x = (m_P, m_N, d_P, d_N) 십진 문자열
R_CANDIDATES = (("R1", ("1.0", "1.0", "0.10", "0.05")), ("R2", ("0.9", "0.9", "0.20", "0.10")), ("R3", ("0.8", "0.8", "0.15", "0.05")))
C_SCALES = ("0.9", "1.1")
SYM_TOL, NEG_TOL = 1e-9, 1e-6           # 양성 = 구현 대칭 기준 · 음성 = 구별 판정선 (B §4 — 구현 대조)
N_NOMINAL = 201                         # A §3-5 · §3-8 '격자 201 평가' — 양 끝 포함 201 점 (41 등분점과 같은 읽기)
TAUS_ALL = ("0",) + tuple(h.SIM_TAUS)
ROWS_CUT = frozenset({0, 4, 5})         # v2 §4-5 끝 — 경계 행 (#0 · #4 · #5) 의 LII 폭에 '제약 절단'
ELIMINATION = {"m_P": "m_P := t", "m_N": "m_N := t", "LII": "d_N := d_P − max_q (m_P − t)"}
_SLOTS = ("s1", "s2", "s3", "s4")
_UNITS = {u["unit"]: u for u in h.units()}


def _unit_of(name: str) -> dict:
    if name not in _UNITS:
        raise HStop(f"모르는 단위 {name!r}")
    return _UNITS[name]


def _key(unit: str, stage: str, *parts) -> str:
    return "|".join([unit, stage] + [str(p) for p in parts])


def _xsha(x) -> str:
    import numpy as np
    return h._sha(np.ascontiguousarray(np.asarray(x, dtype=float), dtype="<f8").tobytes())


# ---------------------------------------------------------------- 정확 잔차 (부속 A §2-2 · B §1-2)
def h_exact(x, max_q) -> tuple:
    """h(x) = (m_P, m_N, LII) · LII = m_P − (d_P − d_N)/max_q — float 좌표의 정확 유리수 (B §4 의 Fraction(float) 뜻 그대로)."""
    fx = [F(float(v)) for v in x]
    return fx[0], fx[1], fx[0] - (fx[2] - fx[3]) / F(max_q)


def residuals_b(x, region, *, max_q, k=None, t=None, tau=None, row=None):
    """B §1-2 의 제약별 정확 잔차 — 영역 A (상자 좌표마다 · G) + 프로파일 등식 |h_k(x) − t| (기록 · 수용 — 등급 아님) + 명목 τ 상자
    (좌표마다 · 수용). 비유한 x → None."""
    base = h.exact_residuals(x, region)
    if base is None:
        return None
    hx = h_exact(x, max_q)
    if k is not None:
        base["eq"] = abs(hx[h.COORDS.index(k)] - F(float(t)))
    if tau is not None:
        nom, tt = [F(v) for v in p0.NOMINAL[row]], F(tau)
        by = [max(abs(a - b) - tt, F(0)) for a, b in zip(hx, nom)]
        base["tau_by_coord"], base["tau"] = by, max(by)
    return base


# ---------------------------------------------------------------- 적응적 시작점 봉인 (부속 B §2-1 둘째 행 · §2-5)
def _safe(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16] + "_" + "".join(c if c.isalnum() else "_" for c in key)[:80]


def seal_starts(seal_dir, key, record) -> dict:
    """그 시작점을 쓰는 지역 실행이 시작하기 직전에 실제 배열을 봉인한다 — 근거 run · 증인 식별 · 변환은 record 에 · 시작 배열 sha256 을 붙인다.
    같은 key 는 다시 쓰지 않는다 (끝난 실행의 시작점을 소급해 바꾸지 않는다)."""
    import numpy as np
    d = Path(seal_dir)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{_safe(key)}.json"
    arr = np.ascontiguousarray(np.asarray(record["array"], dtype=float), dtype="<f8")
    rec = {"schema": "reil-c4-0b2-start-seal-v1", "key": key, **record, "array": arr.tolist(),
           "start_array_sha256": h._sha(arr.tobytes()), "n_starts": int(arr.shape[0])}
    b = c5.dump(rec)
    try:
        with open(p, "xb") as f:
            f.write(b)
    except FileExistsError:
        raise HStop(f"시작점 봉인 {key} 가 이미 있다 — 끝난 실행의 시작점을 소급해 바꾸지 않는다 (B §2-1)") from None
    return {"path": str(p), "sha256": h._sha(b), "start_array_sha256": rec["start_array_sha256"], "n_starts": rec["n_starts"]}


def verify_seal(seal) -> dict:
    """실행 직전 대조 — 봉인 파일의 바이트 sha256 이 작업에 결속한 값과 같아야 한다."""
    b = e3a._read(seal["path"])
    if h._sha(b) != seal["sha256"]:
        raise HStop(f"시작점 봉인 {seal['path']} 의 바이트가 결속한 sha256 과 다르다")
    return json.loads(b)


def _seal_check(task) -> dict:
    s = task.get("seal")
    if not s:
        raise HStop(f"작업 {task.get('task_id')}: 시작점 봉인이 결속되지 않았다 (B §2-1)")
    rec = verify_seal(s)
    if [float(v) for v in rec["array"][s["row"]]] != [float(v) for v in task["x0"]]:
        raise HStop(f"작업 {task.get('task_id')}: 시작점이 봉인 배열의 행 {s['row']} 과 다르다")
    return {"start_seal_sha256": s["sha256"], "start_array_sha256": rec["start_array_sha256"], "start_row": s["row"]}


def _extra(task, seal) -> dict:
    return {"stage": task["stage"], "k": task.get("k", "-"), "grid_index": task.get("grid_index", "-"), "t": task.get("t"),
            "tau": task.get("tau"), "slot": task.get("slot"), **seal}


# ---------------------------------------------------------------- Phase B 지역 문제 (부속 A §3-3 · §3-4 · §3-5)
def profile_problem(task, ctx) -> dict:
    """프로파일 격자점의 3 변수 문제 — 등식 소거 (A §3-3): m_P · m_N := t · LII → d_N := d_P − max_q (m_P − t) (그때 d_N 상자 → 선형 제약 ·
    G → m_P ≥ t + 1e-4/max_q). 자유 변수 상자 = bounds · 수용에 등식 잔차 (≤ 1e-10) · 등급은 영역 A."""
    region, k, t = task["region"], task["k"], float(task["t"])
    q = F(ctx["max_q"])
    qf = float(q)
    names, lo, hi = h.free_box(k, region)
    cons = []
    if k == "m_P":
        def full(z):
            return [t, float(z[0]), float(z[1]), float(z[2])]
    elif k == "m_N":
        def full(z):
            return [float(z[0]), t, float(z[1]), float(z[2])]
    elif k == "LII":
        def full(z):
            return [float(z[0]), float(z[1]), float(z[2]), float(z[2]) - qf * (float(z[0]) - t)]
    else:
        raise HStop(f"좌표 {k!r}")
    if k in ("m_P", "m_N") and region in h.G_REGIONS:
        cons.append(([[0.0, 1.0, -1.0]], float(h.G_LB), math.inf))
    if k == "LII":
        dnl, dnh = h.BOX_D[region][1]
        cons.append(([[-qf, 0.0, 1.0]], float(F(dnl)) - qf * t, float(F(dnh)) - qf * t))
        if region in h.G_REGIONS:
            cons.append(([[1.0, 0.0, 0.0]], t + float(h.G_LB / q), math.inf))
    seal = _seal_check(task)
    x0 = [float(v) for v in task["x0"]]
    return {"x0": x0, "x0_full": full(x0), "lo": [float(F(v)) for v in lo], "hi": [float(F(v)) for v in hi], "cons": cons, "full": full,
            "residuals": lambda x: residuals_b(x, region, max_q=q, k=k, t=t), "active": lambda x: h.active_set(x, region),
            "accept": ("eq",), "free": True, "free_names": list(names), "row_extra": _extra(task, seal)}


def sim_problem(task, ctx) -> dict:
    """동시 양립 τ 의 4 변수 문제 (A §3-4) — bounds = 상자 P × N × (d_P 상자) × (d_N 상자) · 선형 제약 = G 와 LII(x) ∈ I 의 두 면 ·
    수용에 명목 τ 상자 (좌표마다 ≤ 1e-10)."""
    row, region, tau = task["row"], task["region"], task["tau"]
    q = F(ctx["max_q"])
    qf = float(q)
    sb = h.sim_box(row, region, tau, q)
    if sb is None:
        raise HStop(f"#{row} · {region} · τ {tau}: PRIOR_INCOMPATIBLE — 동시 양립 작업을 만들지 않는다 (A §3-4)")
    lii, tt = F(p0.NOMINAL[row][2]), F(tau)
    cons = [([[1.0, 0.0, -1.0 / qf, 1.0 / qf]], float(lii - tt), float(lii + tt))]
    if region in h.G_REGIONS:
        cons.append(([[0.0, 0.0, 1.0, -1.0]], float(h.G_LB), math.inf))
    seal = _seal_check(task)
    x0 = [float(v) for v in task["x0"]]
    return {"x0": x0, "x0_full": list(x0), "lo": [float(v) for v in sb[0]], "hi": [float(v) for v in sb[1]], "cons": cons,
            "full": lambda z: [float(v) for v in z], "residuals": lambda x: residuals_b(x, region, max_q=q, tau=tau, row=row),
            "active": lambda x: h.active_set(x, region), "accept": ("tau",), "free": True, "free_names": list(h.VARS),
            "row_extra": _extra(task, seal)}


def nominal_interval(row, region, max_q):
    """A §3-5: m_P · m_N 명목 고정 → Δ* = max_q (m_P* − LII*) (정확) · d_N 허용 구간 [max(lo(d_N), lo(d_P) − Δ*), min(hi(d_N), hi(d_P) − Δ*)].
    빈 구간이면 None."""
    q = F(max_q)
    m_p, _, lii = (F(v) for v in p0.NOMINAL[row])
    delta = q * (m_p - lii)
    (dpl, dph), (dnl, dnh) = h.BOX_D[region]
    lo, hi = max(F(dnl), F(dpl) - delta), min(F(dnh), F(dph) - delta)
    return None if lo > hi else {"delta": delta, "lo": lo, "hi": hi}


def nominal_grid(iv) -> list:
    """201 등분 격자 — 양 끝 포함 201 점 (정확 유리수)."""
    return [iv["lo"] + (iv["hi"] - iv["lo"]) * F(i, N_NOMINAL - 1) for i in range(N_NOMINAL)]


def _nominal_full(row, delta):
    m_p, m_n, dl = float(F(p0.NOMINAL[row][0])), float(F(p0.NOMINAL[row][1])), float(delta)

    def full(z):
        return [m_p, m_n, float(z[0]) + dl, float(z[0])]
    return full


def _nominal_setup(task, ctx):
    row, region = task["row"], task["region"]
    q = F(ctx["max_q"])
    st = p0.prior_compat(p0.NOMINAL[row], "0", region, q)["status"]
    if st != "PRIOR_COMPATIBLE":
        raise HStop(f"#{row} · {region} · τ = 0: {st} — 명목점 정확 대조를 만들지 않는다 (A §3-5)")
    iv = nominal_interval(row, region, q)
    if iv is None:
        raise HStop(f"#{row} · {region}: P0 는 양립인데 d_N 허용 구간이 비었다")
    return q, iv, _nominal_full(row, iv["delta"])


def nominal_problem(task, ctx) -> dict:
    """명목점 다듬기의 1 변수 문제 (A §3-5) — d_N ∈ 허용 구간 · d_P := d_N + Δ* · 수용에 τ = 0 상자."""
    q, iv, full = _nominal_setup(task, ctx)
    row, region = task["row"], task["region"]
    seal = _seal_check(task)
    x0 = [float(v) for v in task["x0"]]
    return {"x0": x0, "x0_full": full(x0), "lo": [float(iv["lo"])], "hi": [float(iv["hi"])], "cons": [], "full": full,
            "residuals": lambda x: residuals_b(x, region, max_q=q, tau="0", row=row), "active": lambda x: h.active_set(x, region),
            "accept": ("tau",), "free": True, "free_names": ["d_N"], "row_extra": _extra(task, seal)}


_PROBLEMS = {"profile": profile_problem, "simultaneous": sim_problem, "nominal": nominal_problem}


def _make_b(task, ctx) -> dict:
    st = task.get("stage")
    if st not in _PROBLEMS:
        raise HStop(f"모르는 Phase B 단계 {st!r}")
    return _PROBLEMS[st](task, ctx)


def run_phase_b(task, ctx, notify=None, progress=None) -> dict:
    """Phase B 지역 실행 하나 — `supervise` 의 task_fn 계약 · reil_c4_h 의 같은 지역 실행기 (N1–N3 fail-closed 그대로) · 실행 직전 봉인 대조."""
    return h.run_local(task, ctx, _make_b, notify, progress)


def run_nominal_grid(task, ctx, notify=None, progress=None) -> dict:
    """명목점 격자 (A §3-5) — 201 점마다 독립 평가 · 정확 잔차 · 수용 · 라벨 (`supervise` 의 task_fn 계약). 평가 중 지역 예외는 그 점의
    REEVAL_ERROR · 구조 오류는 mon.Structural (partial = 그때까지의 격자점)."""
    acc = {"row": {k: task.get(k) for k in h._ROW_KEYS}}
    try:
        h._check_task(task, ctx)
        q, iv, full = _nominal_setup(task, ctx)
        row, region = task["row"], task["region"]
        prob = {"residuals": lambda x: residuals_b(x, region, max_q=q, tau="0", row=row), "active": lambda x: h.active_set(x, region),
                "accept": ("tau",)}
        pts = []
        acc["row"] = {**acc["row"], "stage": "nominal_grid", "grid": pts}
        t0 = time.monotonic()
        for i, d in enumerate(nominal_grid(iv)):
            x = full([float(d)])
            rec = {"index": i, "d_N": h.frac_str(d), "x": x, "stage": "nominal_grid"}
            rec.update(h._assess(task, ctx, x, prob, acc))
            pts.append(rec)
            if progress is not None:
                progress(i + 1)
        return {**acc["row"], "delta": h.frac_str(iv["delta"]), "interval": [h.frac_str(iv["lo"]), h.frac_str(iv["hi"])],
                "n_points": len(pts), "wall": time.monotonic() - t0, "state": "COMPLETED"}
    except mon.Structural:
        raise
    except BaseException as e:  # noqa: BLE001 — 우리 코드 · 설정의 예외 = 구조 오류
        info = h.classify(e, "ours", ctx.get("util_file"))
        raise mon.Structural(info, partial=h._partial(acc, info)) from None


# ---------------------------------------------------------------- 봉인 배열 (0b1 · 맞춤 전 봉인 — 읽기만)
_INDEX_CACHE: dict = {}
_NPY_CACHE: dict = {}


def _stamp(p: Path) -> tuple:
    st = p.stat()
    return str(p.resolve()), st.st_size, st.st_mtime_ns


def _index(arrays_dir) -> dict:
    p = Path(arrays_dir) / "INDEX.json"
    key = _stamp(p)
    if key not in _INDEX_CACHE:
        idx = json.loads(e3a._read(p))
        _INDEX_CACHE.clear()
        _INDEX_CACHE[key] = {e["label"]: e for e in idx["entries"]}
    return _INDEX_CACHE[key]


def sealed_block(arrays_dir, label):
    """맞춤 전 봉인 배열에서 label 의 블록 — INDEX 의 행 범위 · raw float64 sha256 대조 (MANIFEST 인증은 단계 B 시작의 check_h_arrays)."""
    import numpy as np
    ent = _index(arrays_dir).get(label)
    if ent is None:
        raise HStop(f"봉인 배열에 label {label} 이 없다")
    p = Path(arrays_dir) / ent["file"]
    key = _stamp(p)
    if key not in _NPY_CACHE:
        if len(_NPY_CACHE) > 64:
            _NPY_CACHE.clear()
        _NPY_CACHE[key] = np.load(io.BytesIO(e3a._read(p)), allow_pickle=False)
    blk = np.ascontiguousarray(_NPY_CACHE[key][ent["rows"][0]:ent["rows"][1]], dtype="<f8")
    if h._sha(blk.tobytes()) != ent["raw_sha256"]:
        raise HStop(f"{label}: 봉인 블록의 raw sha256 이 INDEX 와 다르다")
    return blk, ent


# ---------------------------------------------------------------- 프로파일 순회 · 시작 (부속 A §3-3 · B §2-2)
def profile_order(ts, center_value) -> list:
    """중심 = center_value 에 가장 가까운 격자점 (같으면 작은 t) · 나머지는 (중심과의 거리, t) 오름차순 — 바깥으로 번갈아 · sweep 하나."""
    v = [F(t) for t in ts]
    cv = F(center_value)
    c = min(range(len(v)), key=lambda i: (abs(v[i] - cv), v[i]))
    return sorted(range(len(v)), key=lambda i: (abs(v[i] - v[c]), v[i]))


def inner_neighbor(i, center):
    """안쪽 이웃 — 중심 쪽으로 붙은 격자점 (index 기준) · 중심 자신은 None."""
    if i == center:
        return None
    return i + 1 if i < center else i - 1


def _free_of(k, x) -> list:
    drop = {"m_P": 0, "m_N": 1, "LII": 3}[k]
    return [float(v) for j, v in enumerate(x) if j != drop]


def _clip_start(z, names, lo, hi) -> tuple:
    out, clip = [], []
    for n, v, a, b in zip(names, z, lo, hi):
        w = min(max(v, a), b)
        if w != v:
            clip.append({"coord": n, "from": v, "to": w})
        out.append(w)
    return out, clip


def profile_starts(*, k, region, t, max_q, ranked, inner, is_center, sobol2) -> dict:
    """명목 4 (B §2-2) = s1 (x̂⁽⁰⁾) · s2 (안쪽 이웃의 최적 유효 증인 → 안쪽으로 걸어 처음 만나는 유효 증인 → 중심이거나 없으면 Phase A 둘째 →
    없으면 시작 부족 (s2)) · s3 · s4 (봉인 Sobol 2). 둘이 정확히 같으면 뒤의 것을 다음 Phase A 유효 증인으로 · 바닥나면 시작 부족 (중복).
    증인 좌표가 bounds 를 반올림만큼 넘으면 시작점 구성에서만 자르고 기록한다 (증인 판정이 아니다). 복제 · 추가 추출 없음."""
    names, lo_s, hi_s = h.free_box(k, region)
    lo, hi = [float(F(v)) for v in lo_s], [float(F(v)) for v in hi_s]

    def wit(src, x):
        z, clip = _clip_start(_free_of(k, x), names, lo, hi)
        return {"source": src, "x_free": z, "clip": clip, "replaced": [], "witness_x": [float(v) for v in x]}
    cand = list(ranked)
    if not cand:
        raise HStop("Phase A 유효 증인 0 — 단위 UNFIT 이라 프로파일을 시작하지 않는다 (A §1-1)")
    slots = [("s1", wit({"kind": "phase_a", "run_id": cand[0]["run_id"]}, cand[0]["x"]))]
    used, shortages, s2 = 1, [], None
    if not is_center:
        for nb in inner:
            w = nb.get("witness")
            if w:
                s2 = wit({"kind": "grid", "grid_index": nb["grid_index"], "run_id": w.get("run_id")}, w["x"])
                break
    if s2 is None:
        if len(cand) > 1:
            s2, used = wit({"kind": "phase_a", "run_id": cand[1]["run_id"]}, cand[1]["x"]), 2
        else:
            shortages.append("시작 부족 (s2)")
    if s2 is not None:
        slots.append(("s2", s2))
    for j, slot in enumerate(("s3", "s4")):
        slots.append((slot, {"source": {"kind": "sobol", "row": j}, "x_free": [float(v) for v in sobol2[j]], "clip": [], "replaced": [],
                             "witness_x": None}))
    starts = []
    for slot, s in slots:
        while s is not None and any(s["x_free"] == p["x_free"] for p in starts):
            if used < len(cand):
                nxt = cand[used]
                used += 1
                r = wit({"kind": "phase_a", "run_id": nxt["run_id"]}, nxt["x"])
                r["replaced"] = s["replaced"] + [s["source"]]
                s = r
            else:
                shortages.append("시작 부족 (중복)")
                s = None
        if s is not None:
            starts.append({"slot": slot, **s})
    return {"starts": starts, "shortages": shortages, "array": [s["x_free"] for s in starts], "n_starts": len(starts)}


def grid_point_value(rows) -> dict:
    """J_k(t) = 네 실행의 유효 반환점 중 최소 (그 x 가 증인 · 같으면 slot 순) · 넷 다 무효면 '실패' (A §3-3 · §3-7)."""
    valid = [r for r in rows if r.get("witness") == "valid" and h._fin(r.get("value"))]
    if not valid:
        return {"value": None, "witness_slot": None, "n_valid": 0, "search": "실패", "witness": None}
    best = min(valid, key=lambda r: (float(r["value"]), _SLOTS.index(r["slot"]) if r.get("slot") in _SLOTS else len(_SLOTS)))
    return {"value": float(best["value"]), "witness_slot": best.get("slot"), "n_valid": len(valid), "search": "OK", "witness": best}


def _tids(store, n) -> int:
    start = store["next_task_id"]
    store["next_task_id"] += n
    return start


def _completed(out, key, store) -> list:
    st = out["states"]
    if out.get("global_stop") or any(s.get("state") != "COMPLETED" for s in st):
        store["phase_b"][key] = {"status": "INCOMPLETE", "key": key, "states": st, "global_stop": out.get("global_stop")}
        _event(store, "incomplete", key, reason=out.get("global_stop"))
        raise HStop(f"{key}: 전역 중지 · 미완 — {out.get('global_stop')} (미완을 완료로 세지 않는다)")
    return st


def _b_tasks(store, unit, stage, starts, seal, **fields) -> list:
    t0 = _tids(store, len(starts))
    return [{"task_id": t0 + i, "run_id": i, "unit": unit["unit"], "objective": unit["objective"], "region": unit["region"],
             "row": unit["row"], "seed": None, "stage": stage, "slot": s["slot"], "x0": list(s.get("x_free", s.get("x"))), "worker": 0,
             "seal": {"path": seal["path"], "sha256": seal["sha256"], "row": i}, **fields} for i, s in enumerate(starts)]


def _seal_starts_view(starts) -> list:
    out = []
    for s in starts:
        wx = s.get("witness_x")
        out.append({k: v for k, v in s.items() if k != "witness_x"} | {"witness": None if wx is None else {"x": wx, "x_sha256": _xsha(wx)}})
    return out


def profile_point(unit, k, gi, ctx, runner, store, *, arrays_dir, seal_dir, ranked, inner, is_center, grid=None, J0=None) -> dict:
    """프로파일 격자점 하나 — 시작 (B §2-2) → 실행 직전 봉인 (B §2-1) → 최대 4 실행 → J_k(t). 같은 격자점은 다시 돌리지 않는다."""
    key = _key(unit["unit"], "profile", k, gi)
    if key in store["phase_b"]:
        raise HStop(f"{key}: 이미 기록된 격자점 — 다시 돌리지 않는다")
    g = grid or h.profile_grid(k, unit["region"], unit["row"], F(ctx["max_q"]))
    t = g["t"][gi]
    lab = h.label(unit["row"], unit["region"], unit["objective"], "profile", k=k, grid_index=gi)
    blk, ent = sealed_block(arrays_dir, lab)
    if ent.get("t") != t or ent.get("t_fraction") != g["t_fraction"][gi] or blk.shape != (2, 3):
        raise HStop(f"{lab}: 봉인 격자점 (t · 모양) 이 지금 격자와 다르다")
    st = profile_starts(k=k, region=unit["region"], t=t, max_q=ctx["max_q"], ranked=ranked, inner=inner, is_center=is_center, sobol2=blk)
    for s in st["starts"]:
        if s["source"]["kind"] == "sobol":
            s["source"] = {**s["source"], "label": lab, "raw_sha256": ent["raw_sha256"]}
    record = {"unit": unit["unit"], "stage": "profile", "k": k, "grid_index": gi, "t": t, "t_fraction": g["t_fraction"][gi],
              "label": lab, "starts": _seal_starts_view(st["starts"]), "shortages": st["shortages"], "is_center": bool(is_center),
              "transform": {"k": k, "t": t, "elimination": ELIMINATION[k], "bounds_clip": any(s["clip"] for s in st["starts"])},
              "array": st["array"]}
    seal = seal_starts(seal_dir, key, record)
    tasks = _b_tasks(store, unit, "profile", st["starts"], seal, k=k, grid_index=gi, t=t, tau=None)
    rows = _completed(runner(tasks, ctx, run_phase_b), key, store)
    gv = grid_point_value(rows)
    w = gv["witness"]
    rec = {"status": "DONE", "unit": unit["unit"], "stage": "profile", "k": k, "grid_index": gi, "t": t, "t_fraction": g["t_fraction"][gi],
           "seal": seal, "shortages": st["shortages"], "n_starts": st["n_starts"], "rows": rows, "value": gv["value"],
           "witness_slot": gv["witness_slot"], "witness_run_id": None if w is None else w.get("run_id"),
           "witness_x": None if w is None else w.get("x"), "n_valid": gv["n_valid"], "search": gv["search"],
           "below_J0": bool(gv["value"] is not None and J0 is not None and gv["value"] < float(J0)), "tasks": tasks}
    store["phase_b"][key] = rec
    return rec


def _grid_of(unit, k, ctx, grids=None) -> tuple:
    g = h.profile_grid(k, unit["region"], unit["row"], F(ctx["max_q"]))
    idx = list(range(len(g["t"])))
    if grids is not None:
        sel = grids(unit["unit"], k)
        if sel is not None:
            if len(set(sel)) != len(sel) or any(i not in idx for i in sel):
                raise HStop(f"{unit['unit']} · {k}: 주입한 격자 부분집합 {sel} 이 등록 격자 밖")
            idx = sorted(sel)
    return g, idx


def run_profile_k(unit, k, ctx, runner, store, *, arrays_dir, seal_dir, ranked, J0=None, grids=None) -> dict:
    """좌표 k 의 프로파일 — 중심 = x̂⁽⁰⁾ 의 h_k 에 가장 가까운 격자점 · (거리, t) 순 · 각 점은 안쪽 이웃이 끝난 뒤 (s2 가 그 결과에 기댄다).
    미평가 (영역 밖 · 중복) 점은 돌리지 않고 그대로 기록한다. 중심 · 순서는 실행에 쓰는 저장 float 격자 (g["t"]) 의 정확 값으로 정한다 —
    반올림 전 분수 (t_fraction) 가 아니다 (C4B2-N2)."""
    g, idx = _grid_of(unit, k, ctx, grids)
    vals = [F(g["t"][i]) for i in idx]
    hk = h_exact(ranked[0]["x"], ctx["max_q"])[h.COORDS.index(k)]
    order = profile_order(vals, hk)
    center = order[0]
    done, points = {}, []
    for pos in order:
        inner, p = [], inner_neighbor(pos, center)
        while p is not None:
            r = done[p]
            inner.append({"grid_index": idx[p], "witness": None if r["search"] != "OK" else {"run_id": r["witness_run_id"], "x": r["witness_x"]}})
            p = inner_neighbor(p, center)
        pt = profile_point(unit, k, idx[pos], ctx, runner, store, arrays_dir=arrays_dir, seal_dir=seal_dir, ranked=ranked, inner=inner,
                           is_center=(pos == center), grid=g, J0=J0)
        done[pos] = pt
        points.append(pt)
    return {"unit": unit["unit"], "k": k, "points": sorted(points, key=lambda r: r["grid_index"]), "order": [idx[p] for p in order],
            "center": idx[center], "skipped": g["skipped"]}


# ---------------------------------------------------------------- 동시 양립 (부속 A §3-4 · B §2-3 · §1-3)
def sim_starts(*, row, region, tau, max_q, ranked, sobol16) -> dict:
    """명목 16 = 가용 상위 min(4, n_valid) (Phase A 유효 증인 J 순 · m_P · m_N 을 P · N 으로 자름 · d 그대로) + 고정 Sobol 앞 12. 자른 뒤 같은 좌표
    → 다음 순위 · 바닥나면 시작 부족 (중복) · n_valid < 4 → 시작 부족 (Phase A 증인). Sobol 뒤 4 는 쓰지 않는다 (균형 성질 주장 없음)."""
    sb = h.sim_box(row, region, tau, F(max_q))
    if sb is None:
        raise HStop(f"#{row} · {region} · τ {tau}: PRIOR_INCOMPATIBLE — 시작을 만들지 않는다")
    lo, hi = [float(v) for v in sb[0]], [float(v) for v in sb[1]]
    n_valid = len(ranked)
    m = min(4, n_valid)
    shortages = [f"시작 부족 (Phase A 증인) {4 - n_valid}"] if n_valid < 4 else []
    starts = []
    for w in ranked:
        if len(starts) >= m:
            break
        x = [float(v) for v in w["x"]]
        z = [min(max(x[0], lo[0]), hi[0]), min(max(x[1], lo[1]), hi[1]), x[2], x[3]]
        clip = [{"coord": n, "from": x[j], "to": z[j], "rule": "P · N 으로 자르기"} for j, n in ((0, "m_P"), (1, "m_N")) if z[j] != x[j]]
        for j, n in ((2, "d_P"), (3, "d_N")):
            v = min(max(z[j], lo[j]), hi[j])
            if v != z[j]:
                clip.append({"coord": n, "from": z[j], "to": v, "rule": "bounds 반올림 자르기"})
                z[j] = v
        if any(z == s["x"] for s in starts):
            continue
        starts.append({"slot": f"w{len(starts) + 1}", "source": {"kind": "phase_a", "run_id": w["run_id"]}, "x": z, "clip": clip,
                       "witness_x": x})
    if len(starts) < m:
        shortages.append("시작 부족 (중복)")
    for j in range(h.SIM_USE):
        starts.append({"slot": f"sobol{j}", "source": {"kind": "sobol", "row": j}, "x": [float(v) for v in sobol16[j]], "clip": [],
                       "witness_x": None})
    return {"starts": starts, "shortages": shortages, "array": [s["x"] for s in starts], "n_starts": len(starts)}


def run_simultaneous(unit, tau, ctx, runner, store, *, arrays_dir, seal_dir, ranked) -> dict:
    """τ 하나의 동시 양립 — P0 가 PRIOR_INCOMPATIBLE 이면 돌리지 않는다 (기록만) · 시작 16 → 실행 직전 봉인 → 실행."""
    key = _key(unit["unit"], "simultaneous", tau)
    if key in store["phase_b"]:
        raise HStop(f"{key}: 이미 기록된 동시 양립 — 다시 돌리지 않는다")
    q = F(ctx["max_q"])
    if h.sim_box(unit["row"], unit["region"], tau, q) is None:
        rec = {"status": "NOT_RUN", "category": "NOT_RUN:PRIOR_INCOMPATIBLE", "unit": unit["unit"], "stage": "simultaneous", "tau": tau,
               "reason": "P0 PRIOR_INCOMPATIBLE — 돌리지 않는다 (A §3-4 · B §1-3)"}
        store["phase_b"][key] = rec
        _event(store, "not_run", key, category=rec["category"])
        return rec
    lab = h.label(unit["row"], unit["region"], unit["objective"], "simultaneous", tau=tau)
    blk, ent = sealed_block(arrays_dir, lab)
    if blk.shape != (2 ** h.SIM_M, 4):
        raise HStop(f"{lab}: 봉인 블록 모양 {blk.shape}")
    st = sim_starts(row=unit["row"], region=unit["region"], tau=tau, max_q=q, ranked=ranked, sobol16=blk)
    for s in st["starts"]:
        if s["source"]["kind"] == "sobol":
            s["source"] = {**s["source"], "label": lab, "raw_sha256": ent["raw_sha256"]}
    record = {"unit": unit["unit"], "stage": "simultaneous", "tau": tau, "label": lab, "starts": _seal_starts_view(st["starts"]),
              "shortages": st["shortages"], "transform": "m_P · m_N 을 P · N 으로 자름 · d 그대로 (bounds 반올림 자르기만)",
              "sobol_unused_rows": list(range(h.SIM_USE, 2 ** h.SIM_M)), "array": st["array"]}
    seal = seal_starts(seal_dir, key, record)
    tasks = _b_tasks(store, unit, "simultaneous", st["starts"], seal, k="-", grid_index="-", t=None, tau=tau)
    rows = _completed(runner(tasks, ctx, run_phase_b), key, store)
    valid = [float(r["value"]) for r in rows if r.get("witness") == "valid" and h._fin(r.get("value"))]
    rec = {"status": "DONE", "unit": unit["unit"], "stage": "simultaneous", "tau": tau, "seal": seal, "shortages": st["shortages"],
           "n_starts": st["n_starts"], "rows": rows, "n_valid": len(valid), "value": min(valid) if valid else None}
    store["phase_b"][key] = rec
    return rec


# ---------------------------------------------------------------- 명목점 정확 대조 (부속 A §3-5)
def run_nominal_stage(unit, ctx, runner, store, *, seal_dir) -> dict:
    """τ = 0 — P0 가 PRIOR_INCOMPATIBLE 이면 돌리지 않는다 · 201 점 격자 평가 → 최저 유효 격자점 (같으면 작은 d_N) → 실행 직전 봉인 → 1 변수
    COBYQA 다듬기 1 회 → 둘 중 유효 최소 (같으면 격자점)."""
    key = _key(unit["unit"], "nominal")
    if key in store["phase_b"]:
        raise HStop(f"{key}: 이미 기록된 명목점 대조 — 다시 돌리지 않는다")
    q = F(ctx["max_q"])
    st0 = p0.prior_compat(p0.NOMINAL[unit["row"]], "0", unit["region"], q)["status"]
    if st0 != "PRIOR_COMPATIBLE":
        cat = "NOT_RUN:PRIOR_INCOMPATIBLE" if st0 == "PRIOR_INCOMPATIBLE" else f"NOT_RUN:{st0}"
        rec = {"status": "NOT_RUN", "category": cat, "unit": unit["unit"], "stage": "nominal", "reason": f"P0 τ = 0 {st0} — 돌리지 않는다 (A §3-5)"}
        store["phase_b"][key] = rec
        _event(store, "not_run", key, category=cat)
        return rec
    base = {"unit": unit["unit"], "objective": unit["objective"], "region": unit["region"], "row": unit["row"], "seed": None, "worker": 0}
    gtask = {"task_id": _tids(store, 1), "run_id": 0, **base, "stage": "nominal_grid"}
    grow = _completed(runner([gtask], ctx, run_nominal_grid), key, store)[0]
    grid = grow["grid"]
    valid = [p for p in grid if p.get("witness") == "valid" and h._fin(p.get("value"))]
    rec = {"status": "DONE", "unit": unit["unit"], "stage": "nominal", "delta": grow.get("delta"), "interval": grow.get("interval"),
           "grid": grid, "start": None, "refine": None, "best": None}
    if not valid:
        rec.update(search="실패", reason="유효 격자점 0 — 다듬기 없음")
        store["phase_b"][key] = rec
        return rec
    start = min(valid, key=lambda p: (float(p["value"]), F(p["d_N"])))
    z0 = [float(F(start["d_N"]))]
    seal = seal_starts(seal_dir, key, {"unit": unit["unit"], "stage": "nominal", "array": [z0], "shortages": [],
                                       "starts": [{"slot": "refine", "source": {"kind": "nominal_grid", "index": start["index"]},
                                                   "x_free": z0, "witness": {"x": start["x"], "x_sha256": _xsha(start["x"])}}],
                                       "transform": "m_P · m_N 명목 고정 · d_P := d_N + Δ*"})
    rtask = {"task_id": _tids(store, 1), "run_id": 0, **base, "stage": "nominal", "k": "-", "grid_index": "-", "t": None, "tau": "0",
             "slot": "refine", "x0": z0, "seal": {"path": seal["path"], "sha256": seal["sha256"], "row": 0}}
    rrow = _completed(runner([rtask], ctx, run_phase_b), key, store)[0]
    cands = [(float(start["value"]), 0, "grid")]
    if rrow.get("witness") == "valid" and h._fin(rrow.get("value")):
        cands.append((float(rrow["value"]), 1, "refine"))
    b = min(cands)
    rec.update(start=start, refine=rrow, best={"source": b[2], "value": b[0]}, search="OK", seal=seal)
    store["phase_b"][key] = rec
    return rec


# ---------------------------------------------------------------- H4 대조 (부속 A §4-4 · §4-5 · B §4)
def h4_candidates() -> list:
    return [{"name": n, "x": [float(F(v)) for v in xs], "x_decimal": list(xs)} for n, xs in R_CANDIDATES]


def _scaled(xs, c) -> list:
    return [float(F(c) * F(v)) for v in xs]


def h4_positive(util, model, halfcell, gate, *, region="A0", jvs=None) -> dict:
    """양성 대조 (A §4-4) — R1 → R2 → R3 · 셀마다 x · 0.9x · 1.1x 셋이 모두 유효 (§2-1 · n_out = 0 · §4-2 교차 · span > 0) 인 첫 후보.
    통과 ⇔ |J_V^s(c·x) − J_V^s(x)| ≤ 1e-9 V (c 둘 다). 실패 → H4 구현 기각 (모든 셀 H4 중지 · 구현 점검) — 실측 가설의 판정이 아니다.
    유효 후보 없음 → 그 셀 H4 UNFIT (구현 검증 불가)."""
    f = jvs or h.j_vs
    tried = []
    for name, xs in R_CANDIDATES:
        tried.append(name)
        pts, ok = {}, True
        for c in ("1",) + C_SCALES:
            x = _scaled(xs, c)
            r = f(util, x, model, halfcell, gate)
            cls = h.feasibility_class(h.exact_residuals(x, region))
            lab = c5.n_out_labels(util, x, halfcell, model["Q_exp_interp"])
            p = {"x": x, "value": r.get("value"), "reason": r.get("reason"), "span": r.get("span"), "feasibility_class": cls, **lab}
            pts[c] = p
            span = p["span"]
            if not (h._fin(p["value"]) and cls in ("exact_feasible", "numerically_accepted") and lab.get("n_out_PE") == 0
                    and lab.get("n_out_NE") == 0 and h._fin(span) and float(span) > 0):
                ok = False
                break
        if not ok:
            continue
        vals = {c: float(pts[c]["value"]) for c in pts}
        diffs = {c: abs(vals[c] - vals["1"]) for c in C_SCALES}
        passed = all(d <= SYM_TOL for d in diffs.values())
        return {"status": "PASS" if passed else "FAIL", "candidate": name, "tried": tried, "values": vals, "diffs": diffs, "points": pts,
                "stop_all_cells": not passed,
                "meaning": "구현 대칭 검사 통과 (1e-9 V 는 구현 기준 · 실험 정밀도 아님)" if passed else
                           "H4 구현 기각 — 모든 셀 H4 중지 · 구현 점검 (실측 가설의 판정이 아니다)"}
    return {"status": "UNFIT_UNVERIFIABLE", "candidate": None, "tried": tried, "stop_all_cells": False,
            "meaning": "유효 후보 없음 — 그 셀 H4 UNFIT (구현 검증 불가 · 가설 판정 아님)"}


def h4_negative(util, halfcell, x, *, vfull=None) -> dict:
    """음성 대조 (A §4-5) — 같은 기준점 x 에서 D_abs = RMSE_k |V_full^{c·x}(Q_k) − V_full^{x}(Q_k)| · Q_k = linspace(Q_lo^x, Q_hi^x, 100) (x 자신의
    두 cutoff 교차 사이 · 절대 좌표 · 교차는 1000 점 격자 · B §3). 통과 ⇔ D_abs > 1e-6 V (c 둘 다). 실패 → 구현 · 수치 점검 — H4 가설의 기각이 아니다."""
    import numpy as np
    vf = vfull or h.v_full
    fn, qmax = vf(util, x, halfcell)
    qg = np.linspace(0.0, qmax, h.N_GRID)
    vg = np.asarray(fn(qg), dtype=float)
    cr = {c: h.crossings(qg, vg, float(c)) for c in h.CUTOFFS}
    if any(cr[c]["flat"] or cr[c]["n_unique"] != 1 for c in h.CUTOFFS):
        return {"status": "INVALID_REFERENCE", "D_abs": None, "action": "구현 · 수치 점검",
                "meaning": "기준점의 cutoff 교차가 유일하지 않다 — 가설 판정 아님", "crossings": {c: cr[c]["n_unique"] for c in cr}}
    qs = sorted(cr[c]["items"][0]["Q"] for c in h.CUTOFFS)
    qk = np.linspace(qs[0], qs[1], h.N_S)
    base = np.asarray(fn(qk), dtype=float)
    d = {}
    for c in C_SCALES:
        fc, _ = vf(util, [float(F(c) * F(float(v))) for v in x], halfcell)
        d[c] = float(np.sqrt(np.mean((np.asarray(fc(qk), dtype=float) - base) ** 2)))
    passed = all(math.isfinite(v) and v > NEG_TOL for v in d.values())
    return {"status": "PASS" if passed else "FAIL", "D_abs": d, "Q_k": [qs[0], qs[1]], "action": None if passed else "구현 · 수치 점검",
            "meaning": "구별 판정선 1e-6 V 를 넘는다 (구현 대조)" if passed else "구현 · 수치 점검 대상 — H4 가설의 기각이 아니다 (A §4-5 · B §4)"}


def record_h4(store, cell, r) -> dict:
    """대조 결과 기록 — 양성 실패 (또는 stop_all_cells) 는 모든 셀의 H4 를 멈춘다 · 후보 없음은 그 셀만 UNFIT (구현 검증 불가)."""
    rec = {k: r.get(k) for k in ("status", "candidate", "stop_all_cells", "meaning", "action")}
    store["h4"]["cells"][cell] = rec
    if r.get("status") == "FAIL" or r.get("stop_all_cells"):
        store["h4"]["implementation_rejected"] = {"cell": cell, **rec}
    _event(store, "h4_control", f"cell {cell}", status=r.get("status"))
    return rec


def h4_block(store, cell):
    """그 셀의 H4 를 막는 사유 (없으면 None)."""
    if store["h4"]["implementation_rejected"]:
        return "NOT_RUN:H4_IMPLEMENTATION_REJECTED"
    c = store["h4"]["cells"].get(cell)
    if c and c.get("status") == "UNFIT_UNVERIFIABLE":
        return "NOT_RUN:H4_CONTROL_UNVERIFIABLE"
    return None


def _h4_controls(cell, ctx, store):
    """단계 B 에서 그 셀 H4 의 Phase B 앞에 대조 (위치는 등록에 없는 선택 — 범위 확인 §8-3). 음성 실패도 H4 를 막는다 (구현 · 수치 점검)."""
    if store["h4"]["implementation_rejected"] is None and cell not in store["h4"]["cells"]:
        r = h4_positive(ctx["util"], ctx["models"][cell], ctx["halfcell"], ctx["gates"][cell])
        record_h4(store, cell, r)
        ref = r.get("candidate")
        if r.get("status") == "PASS" and ref not in store["h4"]["negative"]:
            neg = h4_negative(ctx["util"], ctx["halfcell"], [float(F(v)) for v in dict(R_CANDIDATES)[ref]])
            store["h4"]["negative"][ref] = {k: neg.get(k) for k in ("status", "D_abs", "action", "meaning")}
            if neg.get("status") != "PASS":
                store["h4"]["implementation_rejected"] = {"cell": cell, "by": "negative", "reference": ref, **store["h4"]["negative"][ref]}
    return h4_block(store, cell)


# ---------------------------------------------------------------- 표지 · 판독 (부속 A §7 · §3-7 · B §1-2 · §1-3)
def point_status(point, T) -> str:
    """격자점 상태 (A §3-7) — 충족 (유효 증인 · J ≤ T) · 초과 · 실패 (네 실행 모두 무효) · 미평가 (영역 밖 · 중복)."""
    s = point.get("search")
    if s == "미평가":
        return "미평가"
    if s != "OK" or not h._fin(point.get("value")):
        return "실패"
    return "충족" if h.reading(point["value"], T)["pass"] else "초과"


def _region_grade(p):
    """영역 A 의 등급 (B §1-2) — 저장된 정확 잔차 (상자 · G). 수용 밖이면 None."""
    r = p.get("residuals") or {}
    if r.get("box") is None:
        return None
    vals = [F(r["box"])] + ([F(r["g"])] if r.get("g") is not None else [])
    if any(v > h.TOL for v in vals):
        return None
    return "exact_feasible" if all(v == 0 for v in vals) else "numerically_accepted"


def _claim_grade(base, excess):
    """주장의 등급 — 영역 A 등급 + 주장 구간 초과량 (정확): 초과 > 1e-10 → 주장 밖 · 0 < 초과 ≤ 1e-10 → numerically_accepted (B §1-2 끝)."""
    if base is None or excess > h.TOL:
        return None
    return "exact_feasible" if base == "exact_feasible" and excess <= 0 else "numerically_accepted"


def _satisfied(p, T) -> bool:
    return p.get("witness") == "valid" and h._fin(p.get("value")) and T is not None and h.reading(p["value"], T)["pass"]


def extra_labels(ws, T, *, row, k=None) -> list:
    """부가 축 (A §7 · B §1-3) — 함께 붙는 라벨 (서로 대체하지 않는다): 외삽 의존 · 제약 절단 · 경계 근접 · 선형 제약 경계 · budget 종료 증인."""
    lab = set()
    for p in ws:
        n_out = [p.get(n) for n in ("n_out_PE", "n_out_NE")]
        if any(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in n_out):
            lab.add("외삽 의존")
        if any(v == "미확인" for v in n_out):
            lab.add("외삽 라벨 미확인")
        if T is not None and h._fin(p.get("value")) and h.reading(p["value"], T)["near_boundary"]:
            lab.add("경계 근접")
        if _region_grade(p) == "numerically_accepted":
            lab.add("선형 제약 경계")
        if p.get("termination") == "budget":
            lab.add("budget 종료 증인")
    if ws and k == "LII" and row in ROWS_CUT:
        lab.add("제약 절단")
    return sorted(lab)


def _compat(grades, rely, T, *, row, k=None) -> dict:
    gs = Counter(grades)
    out = {"grades": {"exact_feasible": gs.get("exact_feasible", 0), "numerically_accepted": gs.get("numerically_accepted", 0)}}
    extra = extra_labels(rely, T, row=row, k=k)
    if out["grades"]["exact_feasible"]:
        return {"value": "COMPATIBLE", "unresolved": False, **out, "extra": extra}
    if out["grades"]["numerically_accepted"]:
        return {"value": "COMPATIBLE (수치 경계 의존)", "unresolved": True, **out, "extra": sorted(set(extra) | {"선형 제약 경계"})}
    return {"value": "NOT_FOUND", "unresolved": True, **out, "extra": extra}


def compat_individual(points, k, tau, T, *, row, max_q) -> dict:
    """개별 양립 (v2 §4-4 · B §1-2 · §1-3) — [t*_k − τ, t*_k + τ] 안의 격자점 (grid_t 정확) 의 충족 증인 · 등급은 영역 A 且 실제 |h_k(x) − t*_k| ≤ τ.
    주장이 exact 증인에 서면 그것에, 아니면 수치 수용 증인에 기댄다 (부가 라벨은 기대는 증인으로)."""
    i = h.COORDS.index(k)
    ts, tt = F(p0.NOMINAL[row][i]), F(tau)
    grades, sup = [], {"exact_feasible": [], "numerically_accepted": []}
    for p in points:
        if p is None or p.get("grid_t") is None or abs(F(p["grid_t"]) - ts) > tt or not _satisfied(p, T):
            continue
        g = _claim_grade(_region_grade(p), abs(h_exact(p["x"], max_q)[i] - ts) - tt)
        if g:
            grades.append(g)
            sup[g].append(p)
    return _compat(grades, sup["exact_feasible"] or sup["numerically_accepted"], T, row=row, k=k)


def _compat_box(ws, tau, T, *, row, region, max_q) -> dict:
    st = p0.prior_compat(p0.NOMINAL[row], tau, region, F(max_q))["status"]
    if st != "PRIOR_COMPATIBLE":
        return {"value": "PRIOR_INCOMPATIBLE" if st == "PRIOR_INCOMPATIBLE" else st, "unresolved": False,
                "grades": {"exact_feasible": 0, "numerically_accepted": 0}, "extra": []}
    nom, tt = [F(v) for v in p0.NOMINAL[row]], F(tau)
    grades, sup = [], {"exact_feasible": [], "numerically_accepted": []}
    for p in ws:
        if not _satisfied(p, T):
            continue
        g = _claim_grade(_region_grade(p), max(abs(a - b) - tt for a, b in zip(h_exact(p["x"], max_q), nom)))
        if g:
            grades.append(g)
            sup[g].append(p)
    return _compat(grades, sup["exact_feasible"] or sup["numerically_accepted"], T, row=row)


def compat_simultaneous(ws, tau, T, *, row, region, max_q) -> dict:
    """동시 양립 (v2 §4-4) — 그 τ 탐색의 충족 증인 · 등급은 영역 A 且 ‖h(x) − h*‖∞ ≤ τ. P0 PRIOR_INCOMPATIBLE 은 어떤 점으로도 뒤집지 않는다 (B §1-3)."""
    return _compat_box(ws, tau, T, row=row, region=region, max_q=max_q)


def compat_nominal(ws, T, *, row, region, max_q) -> dict:
    """명목점 정확 대조 (τ = 0 · A §3-5) — 격자점 · 다듬기의 충족 증인 · 등급은 영역 A 且 h(x) = h* (정확)."""
    return _compat_box(ws, "0", T, row=row, region=region, max_q=max_q)


def _support(e) -> dict:
    v, g, p = e
    return {"grid_index": p.get("grid_index"), "grid_t": p.get("grid_t"), "slot": p.get("slot"), "task_id": p.get("task_id"),
            "run_id": p.get("run_id"), "x": [float(z) for z in p["x"]], "h_k": h.frac_str(v), "grade": g, "value": p.get("value")}


def width(points, k, tau, T, *, max_q, row=None) -> dict:
    """발견 폭 (v2 §4-5 · A §3-7 · B §1-3) — 충족 증인의 실제 h_k (정확) 차 > 2τ 且 둘 다 exact_feasible → WIDE · 수치 수용 증인에 기대면
    WIDE (수치 경계 의존) + UNRESOLVED · 아니면 NARROW_FOUND (UNRESOLVED — 좁음 확정이 아니다).
    폭 주장마다 근거를 직접 결속한다 (C4B2-N3): support = 그 주장이 서는 증인 (WIDE 둘 = 최소 · 최대 h_k · NARROW_FOUND = 고려한 증인의 양 끝) ·
    grades = 고려한 충족 증인의 등급별 수 (B §1-3 끝) · extra = 근거 증인의 부가 라벨 (WIDE 는 그 둘 · NARROW_FOUND 는 고려한 증인 전부 — 수치 수용
    증인이면 선형 제약 경계) · 경계 행 (#0 · #4 · #5) 의 LII 폭에는 언제나 제약 절단 (v2 §1-3 · §4-5)."""
    i, two = h.COORDS.index(k), 2 * F(tau)
    every = []
    for p in points:
        if p is None or not _satisfied(p, T):
            continue
        g = _region_grade(p)
        if g is None:
            continue
        every.append((h_exact(p["x"], max_q)[i], g, p))
    ex = [e for e in every if e[1] == "exact_feasible"]

    def ends(es):
        return min(es, key=lambda e: e[0]), max(es, key=lambda e: e[0])
    lo = hi = None
    basis = every
    if len(ex) >= 2 and ends(ex)[1][0] - ends(ex)[0][0] > two:
        out = {"value": "WIDE", "unresolved": False}
        lo, hi = ends(ex)
        basis = [lo, hi]
    elif len(every) >= 2 and ends(every)[1][0] - ends(every)[0][0] > two:
        out = {"value": "WIDE (수치 경계 의존)", "unresolved": True}
        lo, hi = ends(every)
        basis = [lo, hi]
    else:
        out = {"value": "NARROW_FOUND", "unresolved": True}
        if every:
            lo, hi = ends(every)
    extra = set(extra_labels([e[2] for e in basis], T, row=row, k=k))
    if k == "LII" and row in ROWS_CUT:
        extra.add("제약 절단")
    out["observed"] = None if lo is None else [h.frac_str(lo[0]), h.frac_str(hi[0])]
    out["grades"] = {"exact_feasible": len(ex), "numerically_accepted": len(every) - len(ex)}
    out["support"] = [] if lo is None else ([_support(lo)] if lo is hi else [_support(lo), _support(hi)])
    out["extra"] = sorted(extra)
    return out


def _judgments(u, J_hat, sig, J_V=None, J_D=None) -> dict:
    th = h.thresholds(u["objective"], u["region"], J_hat=J_hat, sigma_v=sig, J_hat_V=J_V, J_hat_D=J_D)
    out = {}
    for name, t in th.items():
        if t["status"] != "OK":
            out[name] = {"status": "UNFIT", "reason": t["reason"]}
        elif "T" in t:
            out[name] = {"status": "OK", "T": t["T"]}
        else:
            for d, T in t["T_by_delta"].items():
                out[f"{name}|δ={d}"] = {"status": "OK", "T": T, "main": d == h.DELTA_MAIN}
    return out


def _read_unit(store, u, T, vfun, *, ctx, grids) -> dict:
    name, row, region = u["unit"], u["row"], u["region"]
    q = F(ctx["max_q"])
    grid_out, comp_ind, wid = {}, {}, {}
    for k in h.COORDS:
        g, idx = _grid_of(u, k, ctx, grids)
        pts, wits = [], []
        for gi in idx:
            rec = store["phase_b"][_key(name, "profile", k, gi)]
            gv = grid_point_value([dict(r, value=vfun(r)) for r in rec["rows"]])
            pts.append({"grid_index": gi, "t": g["t"][gi], "status": point_status(gv, T), "value": gv["value"], "below_J0": rec.get("below_J0")})
            if gv["search"] == "OK":
                wits.append(dict(gv["witness"], grid_t=g["t_fraction"][gi]))
        pts += [{"grid_index": None, "t": s["t"], "status": "미평가", "reason": s["reason"]} for s in g["skipped"]]
        grid_out[k] = pts
        comp_ind[k] = {tau: compat_individual(wits, k, tau, T, row=row, max_q=q) for tau in TAUS_ALL}
        wid[k] = {tau: width(wits, k, tau, T, max_q=q, row=row) for tau in h.SIM_TAUS}
    comp_sim = {}
    for tau in h.SIM_TAUS:
        rec = store["phase_b"].get(_key(name, "simultaneous", tau)) or {}
        rows = [dict(r, value=vfun(r)) for r in rec.get("rows", [])] if rec.get("status") == "DONE" else []
        comp_sim[tau] = compat_simultaneous(rows, tau, T, row=row, region=region, max_q=q)
    nrec = store["phase_b"].get(_key(name, "nominal")) or {}
    nrows = []
    if nrec.get("status") == "DONE":
        nrows = [dict(p, value=vfun(p)) for p in nrec.get("grid", [])]
        if nrec.get("refine"):
            nrows.append(dict(nrec["refine"], value=vfun(nrec["refine"])))
    return {"T": T, "computation": "OK", "grid": grid_out, "compat_individual": comp_ind, "compat_simultaneous": comp_sim,
            "compat_nominal": compat_nominal(nrows, T, row=row, region=region, max_q=q), "width": wid,
            "status_counts": dict(Counter(p["status"] for k in grid_out for p in grid_out[k]))}


def _labels(store, u, t, vfun, *, ctx, grids) -> dict:
    if t["status"] != "OK":
        return {"T": None, "computation": f"UNFIT:{t['reason']}"}
    return _read_unit(store, u, t["T"], vfun, ctx=ctx, grids=grids)


def _read_cell_region(cell, region, store, ctx, grids, upd) -> dict:
    """판독 (A §1-1 · B §4) — 같은 최종 저장점 집합에 옛 (Ĵ⁽⁰⁾) · 새 (최종 Ĵ) 문턱을 적용 · 새 평가 0. 주 판정 = 갱신 뒤 · 갱신 전은 부표.
    결합 단위는 모든 유효 (J_V, J_D) 쌍을 최종 분모로 다시 비교한다."""
    states = store["unit_states"][f"{cell}|{region}"]
    final = upd["final"]
    sig = (ctx.get("sigma_v") or {}).get(cell)
    out = {}
    for u in h.units():
        if u["row"] != cell or u["region"] != region:
            continue
        name, st = u["unit"], states[u["unit"]]
        if st["status"] == "NOT_RUN":
            out[name] = {"computation": f"UNFIT:{st['category']}", "reason": st.get("reason")}
            continue
        if st["status"] == "UNFIT":
            out[name] = {"computation": "UNFIT:유효 증인 0", "reason": st.get("reason")}
            continue
        if u["objective"] == "rho":
            pv, pd = store["rho_denominators"][name]
            fv, fd = final.get(f"J_V|A0|{cell}"), final.get(f"J_D|A0|{cell}")
            jpre, jfin = _judgments(u, None, sig, J_V=pv, J_D=pd), _judgments(u, None, sig, J_V=fv, J_D=fd)
            ok_f = h._fin_pos(fv) and h._fin_pos(fd)

            def vfin(r, fv=fv, fd=fd, ok_f=ok_f):
                c = r.get("components")
                if not ok_f or r.get("witness") != "valid" or not c:
                    return float("nan")
                return h.rho(c["J_V"], c["J_D"], fv, fd)

            def vpre(r):
                return r.get("value")
            rho_list = [{"rho_final": vfin(p), "rho_search": p.get("value"), "J_V": p["components"]["J_V"], "J_D": p["components"]["J_D"],
                         "stage": p.get("stage")} for p in unit_points(store, name) if p.get("witness") == "valid"]
        else:
            jpre = _judgments(u, store["summaries"][name]["J0"], sig)
            jfin = _judgments(u, final.get(name), sig)

            def vpre(r):
                return r.get("value")
            vfin = vpre
            rho_list = None
        rec = {"pre": {j: _labels(store, u, t, vpre, ctx=ctx, grids=grids) for j, t in jpre.items()},
               "final": {j: _labels(store, u, t, vfin, ctx=ctx, grids=grids) for j, t in jfin.items()},
               "thresholds": {"pre": jpre, "final": jfin}}
        if rho_list is not None:
            rec["final_rho"] = rho_list
        out[name] = rec
    return out


# ---------------------------------------------------------------- 연결부 (회신 §5-3–5 · 부속 A §3-2 · §1-1 · B §4)
def new_store() -> dict:
    """연결부 기록 — 단계 A · B 를 따로 (C4-A · C4-B) 돌려도 저장된 기록으로 이어 간다."""
    return {"schema": "reil-c4-0b2-store-v1", "phase_a": {}, "not_run": {}, "not_run_b": {}, "summaries": {}, "rho_denominators": {},
            "phase_b": {}, "h4": {"cells": {}, "negative": {}, "implementation_rejected": None}, "unit_states": {}, "registry": {},
            "searches_done": {}, "updates": {}, "readings": {}, "ray": {"status": "미구현", "reached": 0}, "events": [],
            "planned_units": [], "next_task_id": 0, "seq": 0}


def _event(store, kind, key, **kw) -> None:
    store["seq"] += 1
    store["events"].append({"seq": store["seq"], "kind": kind, "key": key, **kw})


def _set_not_run(store, unit, category, reason) -> None:
    store["not_run"][unit] = {"category": category, "reason": reason}
    _event(store, "not_run", unit, category=category)


def _not_run_a(u, ctx):
    if u["objective"] == "J_Vs" and not (ctx["gates"].get(u["row"]) or {}).get("accepted"):
        return "NOT_RUN:ENDPOINT_GATE", "P0 끝점 수용 아님 → 그 셀 H4 UNFIT (부속 A §4-3) — 적용 가능성 실패이지 반증이 아니다"
    if u["objective"] in ("J_D", "rho"):
        g = h.jd_gate(ctx["models"][u["row"]])
        if not g["ok"]:
            return "NOT_RUN:JD_EMPTY_MASK", f"J_D {g['reason']} — 자료 쪽 UNFIT (v2 그대로 · J_D · ρ)"
    return None


def phase_a_complete(rows, unit, arrays) -> dict:
    """저장된 기록으로 Phase A 완료 판정 — 128 행 · 모두 COMPLETED · run 번호 0–127 각각 한 번 · x0 = 봉인 배열 · 단위 일치 (회신 §5-3)."""
    if not rows:
        return {"complete": False, "reasons": ["기록 없음"]}
    u, n = _unit_of(unit), 2 * h.PHASE_A_N
    reasons = []
    if len(rows) != n:
        reasons.append(f"행 {len(rows)} ≠ {n}")
    bad = sorted({str(r.get("state")) for r in rows if r.get("state") != "COMPLETED"})
    if bad:
        reasons.append(f"완료가 아닌 상태 {bad}")
    done = [r for r in rows if r.get("state") == "COMPLETED"]
    rids = [r.get("run_id") for r in done]
    if any(not isinstance(i, int) or isinstance(i, bool) for i in rids) or sorted(rids) != list(range(n)):
        reasons.append("run 번호 누락 · 중복")
    for r in done:
        rid = r.get("run_id")
        if r.get("unit") != unit:
            reasons.append(f"run {rid}: 단위 {r.get('unit')} ≠ {unit}")
            break
        if isinstance(rid, int) and 0 <= rid < n:
            seed, i = divmod(rid, h.PHASE_A_N)
            if [float(v) for v in (r.get("x0") or [])] != [float(v) for v in arrays[(u["region"], seed)][i]]:
                reasons.append(f"run {rid}: x0 가 봉인 배열과 다르다")
                break
    return {"complete": not reasons, "reasons": reasons}


def _group(tasks, states) -> dict:
    by = {t["task_id"]: t["unit"] for t in tasks}
    out: dict = {}
    for s in states:
        out.setdefault(by[s["task_id"]], []).append(s)
    return out


def direct_runner(tasks, ctx, task_fn) -> dict:
    """감시 없는 순차 실행기 (시험 · 소규모) — supervise 와 같은 출력 꼴. 구조 오류에서 멈추고 남은 작업은 시작하지 않는다."""
    states, stop = [], None
    for t in tasks:
        if stop is not None:
            states.append({"task_id": t["task_id"], "worker": t.get("worker"), "state": "NOT_STARTED", "interrupt_reason": stop})
            continue
        try:
            row = task_fn(t, ctx)
            states.append({**row, "task_id": t["task_id"], "state": "COMPLETED"})
        except mon.Structural as s:
            info = s.info if isinstance(s.info, dict) else {"message": str(s.info)}
            stop = f"구조 오류: {info.get('type')} ({info.get('origin')} · {info.get('stage')}) {info.get('message')}"[:400]
            states.append({"task_id": t["task_id"], "worker": t.get("worker"), "state": "STARTED_INTERRUPTED",
                           "structural_partial": s.partial, "interrupt_reason": stop})
    return {"states": states, "global_stop": stop}


def supervise_runner(*, limits, n_workers, **kw):
    """감시 모듈 `supervise` 실행기 — 작업자 배정은 순번 % n (단계마다 새 원점 t0)."""
    def runner(tasks, ctx, task_fn):
        ts = [dict(t, worker=i % n_workers) for i, t in enumerate(tasks)]
        return mon.supervise(ts, ctx, task_fn, n_workers=n_workers, limits=limits, t0=time.monotonic(), **kw)
    return runner


def stage_a(unit_names, ctx, runner, store, arrays, n_workers=1) -> dict:
    """단계 A (C4-A 의 연결부) — 1 파: ρ 밖 단위의 Phase A (끝점 게이트 · J_D 빈 마스크는 미실행 기록) → 저장된 기록으로 완료 대조 →
    2 파: ρ (두 단일 목적 Phase A 완료 · 분모 유한 양수일 때만 · A §3-2 2).
    전역 중지 (C4B2-N1): 그 파의 행과 완료 대조를 기록하고, 아직 돌지 않은 ρ 는 실행 없이 NOT_RUN:RHO_PRECONDITION (사유에 중지 원문) 으로
    분류한 뒤 멈춘다 — ρ 의 선행 조건 = 앞 파가 전역 중지 없이 끝남 · 두 단일 목적 Phase A 완료 · 분모 유한 양수."""
    want = list(dict.fromkeys(unit_names))
    us = [_unit_of(n) for n in want]
    for u in us:
        if u["unit"] in store["planned_units"]:
            raise HStop(f"{u['unit']}: 이미 단계 A 에 올린 단위 — 다시 돌리지 않는다")
        store["planned_units"].append(u["unit"])
    wave1 = []
    for u in us:
        if u["objective"] == "rho":
            continue
        nr = _not_run_a(u, ctx)
        if nr:
            _set_not_run(store, u["unit"], *nr)
            continue
        wave1.append(u)
    stop = None
    if wave1:
        tasks = h.phase_a_tasks(wave1, arrays, n_workers, start_id=_tids(store, len(wave1) * 2 * h.PHASE_A_N))
        out = runner(tasks, ctx, h.run_phase_a)
        by = _group(tasks, out["states"])
        for u in wave1:
            store["phase_a"][u["unit"]] = by.get(u["unit"], [])
        stop = out.get("global_stop") or None
        if stop:
            _event(store, "global_stop", "phase_a wave 1", reason=stop)
        for u in wave1:
            chk = phase_a_complete(store["phase_a"][u["unit"]], u["unit"], arrays)
            _event(store, "phase_a_complete" if chk["complete"] else "phase_a_incomplete", u["unit"], reasons=chk["reasons"])
    rho = []
    for u in us:
        if u["objective"] != "rho":
            continue
        try:
            rho.append(rho_wave(u["row"], ctx, runner, store, arrays, n_workers, stopped=stop))
        except WaveStop as e:
            stop = e.reason
            rho.append({"status": "STOPPED", "unit": u["unit"], "reason": stop})
    if stop:
        raise HStop(f"단계 A 전역 중지 — {stop} (계획 단위는 모두 기록 · 분류했다)")
    return {"planned": want, "wave1": [u["unit"] for u in wave1], "rho": rho}


def rho_wave(row, ctx, runner, store, arrays, n_workers=1, stopped=None) -> dict:
    """결합 Phase A (A §3-2 2 · §1-3) — 같은 셀의 J_V A0 · J_D A0 Phase A 가 저장된 기록으로 둘 다 완료일 때만 · 분모 Ĵ⁽⁰⁾ 가 유한한 양수일 때만.
    중단 · 선행 미완은 완료가 아니다 → NOT_RUN:RHO_PRECONDITION (회신 §5-3). stopped (앞 파의 전역 중지 원문) 가 있으면 실행 없이 같은 분류 ·
    사유에 원문 (C4B2-N1). 이 ρ 파 자체가 전역 중지되면 행 · 완료 대조를 기록하고 WaveStop."""
    unit = f"rho|A0|{row}"
    if unit in store["phase_a"] or unit in store["not_run"]:
        raise HStop(f"{unit}: 이미 기록된 결합 단위 — 다시 돌리지 않는다")
    if unit not in store["planned_units"]:
        store["planned_units"].append(unit)
    deps = (f"J_V|A0|{row}", f"J_D|A0|{row}")
    nr = _not_run_a(_unit_of(unit), ctx)
    if nr:
        _set_not_run(store, unit, *nr)
        return {"status": "NOT_RUN", "category": nr[0], "reason": nr[1]}
    problems = [] if not stopped else [f"앞 파 전역 중지 ({stopped}) — ρ 를 시작하지 않는다"]
    for d in deps:
        if d in store["not_run"]:
            problems.append(f"{d} 미실행 ({store['not_run'][d]['category']})")
            continue
        chk = phase_a_complete(store["phase_a"].get(d), d, arrays)
        if not chk["complete"]:
            problems.append(f"{d}: {'; '.join(chk['reasons'][:3])}")
    if problems:
        reason = "선행 미완 — " + " · ".join(problems) + " (중단 · 선행 미완을 완료로 취급하지 않는다)"
        _set_not_run(store, unit, "NOT_RUN:RHO_PRECONDITION", reason)
        return {"status": "NOT_RUN", "category": "NOT_RUN:RHO_PRECONDITION", "reason": reason}
    sums = {d: h.phase_a_summary(store["phase_a"][d]) for d in deps}
    store["summaries"].update(sums)
    den = h.rho_denominators(sums, row)
    if den is None:
        reason = f"분모 Ĵ⁽⁰⁾ 가 유한한 양수가 아님 (J_V {sums[deps[0]]['J0']} · J_D {sums[deps[1]]['J0']}) → 결합 UNFIT (A §1-2)"
        _set_not_run(store, unit, "NOT_RUN:RHO_PRECONDITION", reason)
        return {"status": "NOT_RUN", "category": "NOT_RUN:RHO_PRECONDITION", "reason": reason}
    _event(store, "rho_start", unit, denominators=list(den))
    ctx2 = dict(ctx, denominators={**(ctx.get("denominators") or {}), row: den})
    tasks = h.phase_a_tasks([_unit_of(unit)], arrays, n_workers, start_id=_tids(store, 2 * h.PHASE_A_N))
    out = runner(tasks, ctx2, h.run_phase_a)
    store["phase_a"][unit] = out["states"]
    store["rho_denominators"][unit] = list(den)
    stop = out.get("global_stop") or None
    if stop:
        _event(store, "global_stop", unit, reason=stop)
    chk = phase_a_complete(out["states"], unit, arrays)
    _event(store, "phase_a_complete" if chk["complete"] else "phase_a_incomplete", unit, reasons=chk["reasons"])
    if stop:
        raise WaveStop(f"{unit}: 결합 Phase A 전역 중지 — {stop}", stop)
    return {"status": "DONE", "denominators": list(den), "complete": chk["complete"]}


def _ranked(rows) -> list:
    valid = sorted((r for r in rows if r.get("witness") == "valid" and h._fin(r.get("value"))), key=lambda r: (r["value"], r["run_id"]))
    return [{"run_id": r["run_id"], "x": r["x"], "value": r["value"]} for r in valid]


def _unit_state(name, store, arrays) -> dict:
    if name in store["not_run"]:
        return {"status": "NOT_RUN", **store["not_run"][name]}
    chk = phase_a_complete(store["phase_a"].get(name), name, arrays)
    if not chk["complete"]:
        raise HStop(f"{name}: Phase A 미완 — 단계 B 를 시작하지 않는다 ({'; '.join(chk['reasons'][:3])})")
    summ = h.phase_a_summary(store["phase_a"][name])
    store["summaries"][name] = summ
    if summ["unfit"]:
        return {"status": "UNFIT", "reason": "유효 증인 0 — 하류 없음 (A §1-1 · §2-3)"}
    return {"status": "FIT"}


def run_searches(cell, region, ctx, runner, store, *, arrays, arrays_dir, seal_dir, grids=None) -> dict:
    """단계 B 의 등록 탐색 (A §3-2 3) — 단위마다 프로파일 (좌표 셋) → 동시 양립 (τ 둘) → 명목점 대조. H4 는 대조 뒤 Phase B · ray 에 닿으면 멈춘다.
    Phase A 가 저장된 기록으로 완료가 아니면 시작하지 않는다."""
    key = f"{cell}|{region}"
    if key in store["unit_states"] or key in store["updates"]:
        raise HStop(f"{key}: 이미 단계 B 탐색을 했다 — 다시 돌리지 않는다")
    us = [u for u in h.units() if u["row"] == cell and u["region"] == region]
    states = {u["unit"]: _unit_state(u["unit"], store, arrays) for u in us}
    for u in us:
        name = u["unit"]
        if states[name]["status"] != "FIT":
            continue
        if u["objective"] == "J_Vs":
            blk = _h4_controls(cell, ctx, store)
            if blk:
                store["not_run_b"][name] = {"category": blk, "reason": "H4 대조 결과 — 그 단위의 Phase B 를 돌리지 않는다 (가설 판정 아님)"}
                states[name] = {"status": "NOT_RUN", "category": blk, "reason": store["not_run_b"][name]["reason"]}
                _event(store, "not_run", name, category=blk)
                continue
        uctx = ctx
        if u["objective"] == "rho":
            den = store["rho_denominators"].get(name)
            if not den:
                raise HStop(f"{name}: 결합 Phase A 분모 기록이 없다")
            uctx = dict(ctx, denominators={**(ctx.get("denominators") or {}), cell: tuple(den)})
        ranked = _ranked(store["phase_a"][name])
        J0 = store["summaries"][name]["J0"]
        for k in h.COORDS:
            run_profile_k(u, k, uctx, runner, store, arrays_dir=arrays_dir, seal_dir=seal_dir, ranked=ranked, J0=J0, grids=grids)
        for tau in h.SIM_TAUS:
            run_simultaneous(u, tau, uctx, runner, store, arrays_dir=arrays_dir, seal_dir=seal_dir, ranked=ranked)
        run_nominal_stage(u, uctx, runner, store, seal_dir=seal_dir)
        if u["objective"] == "J_Vs":
            store["ray"]["reached"] += 1
            _event(store, "ray_reached", name)
            raise RayNotImplemented(f"{name}: H4 Phase B 뒤 ray 단계 — ray 는 유보 (미구현) · 이 (셀 · 영역) 은 갱신하지 않는다 (범위 확인 §9-2)")
    store["unit_states"][key] = states
    return {"cell": cell, "region": region, "units": {n: s["status"] for n, s in states.items()}}


def _registered(cell, region, store, ctx, grids=None) -> dict:
    """등록 탐색 목록 (A §3-2 · §3-8) — 키 → 종류. 단위 미실행 · UNFIT · H4 막힘은 하류를 등록하지 않는다 (그 사유로 기록)."""
    states = store["unit_states"][f"{cell}|{region}"]
    reg = {}
    for u in h.units():
        if u["row"] != cell or u["region"] != region:
            continue
        name = u["unit"]
        if name in store["not_run"]:
            continue
        reg[f"{name}|phase_a"] = "phase_a"
        if states[name]["status"] != "FIT":
            continue
        for k in h.COORDS:
            _, idx = _grid_of(u, k, ctx, grids)
            for gi in idx:
                reg[_key(name, "profile", k, gi)] = "profile"
        for tau in h.SIM_TAUS:
            reg[_key(name, "simultaneous", tau)] = "simultaneous"
        reg[_key(name, "nominal")] = "nominal"
    return reg


def missing_searches(cell, region, store, ctx, grids=None) -> list:
    """등록 탐색 중 끝 기록 (DONE · 등록 사유의 NOT_RUN) 이 없는 것 — 은폐 불허 (회신 §5-4)."""
    miss = []
    for key, kind in _registered(cell, region, store, ctx, grids).items():
        if kind == "phase_a":
            name = key[:-len("|phase_a")]
            rows = store["phase_a"].get(name) or []
            if len(rows) != 2 * h.PHASE_A_N or any(r.get("state") != "COMPLETED" for r in rows):
                miss.append(key)
            continue
        rec = store["phase_b"].get(key)
        if not rec or rec.get("status") not in ("DONE", "NOT_RUN"):
            miss.append(key)
    return miss


def common_update_once(cell, region, store) -> dict:
    """공통 갱신 (A §1-1) — (셀 · 영역) 의 등록 탐색 대조가 끝난 뒤 한 번. 계산은 reil_c4_h.common_update (불변식 포함) 그대로."""
    key = f"{cell}|{region}"
    if not store["searches_done"].get(key):
        raise HStop(f"{key}: 등록 탐색 대조 전 — 중간 갱신 거부 (A §1-1 · 회신 §5-4)")
    if key in store["updates"]:
        raise HStop(f"{key}: 공통 갱신은 (셀 · 영역) 마다 한 번 — 두 번째 갱신 거부")
    recs = pool_records(store, cell, region)
    pre = {}
    for u in h.units():
        if u["row"] == cell and u["region"] == region and u["objective"] != "rho":
            s = store["summaries"].get(u["unit"])
            if s and not s["unfit"]:
                pre[(u["objective"], region, cell)] = float(s["J0"])
    res = h.common_update(recs, pre)
    upd = {"final": {f"{o}|{r}|{c}": v for (o, r, c), v in res["final"].items()},
           "pre": {f"{o}|{r}|{c}": v for (o, r, c), v in res["pre"].items()},
           "combined_lower": res["combined_lower"], "rho_hat": {str(k): v for k, v in res["rho_hat"].items()}, "n_records": len(recs)}
    store["updates"][key] = upd
    _event(store, "common_update", key)
    return upd


def finalize(cell, region, store, ctx, grids=None) -> dict:
    """등록 탐색 대조 → 공통 갱신 1 회 → 같은 최종 저장점 집합의 판독 · 표지. 빠진 탐색이 있으면 갱신하지 않는다 (구조 중지 · 목록 기록)."""
    key = f"{cell}|{region}"
    if key in store["updates"]:
        raise HStop(f"{key}: 공통 갱신은 (셀 · 영역) 마다 한 번 — 다시 하지 않는다 (A §1-1)")
    if key not in store["unit_states"]:
        raise HStop(f"{key}: 단계 B 탐색 기록이 없다 — 등록 탐색이 끝나기 전에는 갱신하지 않는다")
    miss = missing_searches(cell, region, store, ctx, grids)
    if miss:
        _event(store, "update_refused", key, missing=miss[:50])
        raise HStop(f"{key}: 등록 탐색 기록이 빠졌다 — 공통 갱신 거부 (은폐 불허): {miss}")
    store["registry"][key] = _registered(cell, region, store, ctx, grids)
    store["searches_done"][key] = True
    upd = common_update_once(cell, region, store)
    reading = _read_cell_region(cell, region, store, ctx, grids, upd)
    store["readings"][key] = reading
    return {"cell": cell, "region": region, "update": upd, "reading": reading, "ray": dict(store["ray"])}


def stage_b(cell, region, ctx, runner, store, *, arrays, arrays_dir, seal_dir, grids=None) -> dict:
    """단계 B (C4-B 의 연결부) — 등록 탐색 (run_searches) → finalize."""
    run_searches(cell, region, ctx, runner, store, arrays=arrays, arrays_dir=arrays_dir, seal_dir=seal_dir, grids=grids)
    return finalize(cell, region, store, ctx, grids=grids)


def unit_points(store, unit) -> list:
    """한 단위의 저장된 기록 점 전부 (A §1-1 의 기록 점) — Phase A 행 · Phase B 반환점 · 명목 격자점 · 다듬기. 대조 점은 넣지 않는다 · 정해진 순서."""
    pts = [dict(r, stage="phase_a") for r in store["phase_a"].get(unit, []) if r.get("state") == "COMPLETED"]
    for key in sorted(k for k in store["phase_b"] if k.startswith(unit + "|")):
        rec = store["phase_b"][key]
        if rec.get("status") != "DONE" or rec.get("stage") in h.CONTROL_STAGES:
            continue
        if rec["stage"] == "nominal":
            pts += [dict(p, stage="nominal_grid") for p in rec.get("grid", [])]
            if rec.get("refine"):
                pts.append(dict(rec["refine"]))
        else:
            pts += [dict(r) for r in rec.get("rows", []) if r.get("stage") not in h.CONTROL_STAGES]
    return pts


def pool_records(store, cell, region) -> list:
    """공통 갱신의 입력 — (셀 · 영역) 단위들의 기록 점을 common_update 의 꼴로 (대조 점 제외 · 결합 단위는 성분과 함께)."""
    out = []
    for u in h.units():
        if u["row"] != cell or u["region"] != region:
            continue
        for p in unit_points(store, u["unit"]):
            if p.get("stage") in h.CONTROL_STAGES:
                continue
            out.append({"objective": u["objective"], "region": region, "row": cell, "value": p.get("value"),
                        "valid": p.get("witness") == "valid", "stage": p.get("stage"), "components": p.get("components")})
    return out


def plan_counts(store) -> dict:
    """계획 · 실행 · 미실행 · 미해결을 따로 센다 (회신 §5-5 · C4B2-N1) — 단위와 지역 실행 모두 겹치지 않는 칸으로:
    단위: 계획 = 작업을 만든 단위 (run_units = 완료 · 착수 뒤 중단 · 미착수 · 미완 기타) + 미실행 (범주별) + 미분류 (0 이어야 한다).
    지역 실행: 계획 (단위마다 128) = 상태별 행 (COMPLETED · STARTED_INTERRUPTED · NOT_STARTED · 그 밖) + 행 수 차 (128 − 행 수) + 미실행 단위의 128 +
    미분류 단위의 128. 완료 = 단계 A 가 저장된 행 · 봉인 배열로 기록한 완료 대조 (phase_a_complete 사건) · UNFIT = 완료 단위 중 유효 증인 0 만."""
    planned = list(store["planned_units"])
    n = 2 * h.PHASE_A_N
    nr = Counter(store["not_run"][u]["category"] for u in planned if u in store["not_run"])
    run_units = [u for u in planned if u in store["phase_a"] and u not in store["not_run"]]
    unaccounted = [u for u in planned if u not in store["phase_a"] and u not in store["not_run"]]
    checked = {e["key"]: e["kind"] == "phase_a_complete" for e in store["events"] if e["kind"] in ("phase_a_complete", "phase_a_incomplete")}
    classes = dict.fromkeys(("완료", "착수 뒤 중단", "미착수", "미완 (기타)"), 0)
    states, mismatch, unfit = Counter(), 0, 0
    for u in run_units:
        rows = store["phase_a"][u]
        st = [r.get("state") for r in rows]
        states.update(str(s) for s in st)
        mismatch += n - len(rows)
        if checked.get(u):
            classes["완료"] += 1
            unfit += int(h.phase_a_summary(rows)["unfit"])
        elif rows and all(s == "NOT_STARTED" for s in st):
            classes["미착수"] += 1
        elif any(s in ("COMPLETED", "STARTED_INTERRUPTED") for s in st) and any(s in ("STARTED_INTERRUPTED", "NOT_STARTED") for s in st):
            classes["착수 뒤 중단"] += 1
        else:
            classes["미완 (기타)"] += 1
    pa = {"planned_units": len(planned), "run_units": len(run_units), "unit_classes": classes, "not_run": dict(sorted(nr.items())),
          "unaccounted_units": unaccounted, "unfit_units": unfit,
          "planned_runs": n * len(planned), "executed_runs": states.get("COMPLETED", 0), "run_states": dict(sorted(states.items())),
          "row_count_mismatch": mismatch, "not_run_runs": n * sum(nr.values()), "unaccounted_runs": n * len(unaccounted),
          "global_stops": [e.get("reason") for e in store["events"] if e["kind"] == "global_stop"],
          "identity": {"units": "planned_units = run_units + Σ not_run + |unaccounted_units| · run_units = Σ unit_classes",
                       "runs": "planned_runs = Σ run_states + row_count_mismatch + not_run_runs + unaccounted_runs"},
          "note": "이 기록이 본 단위의 계획 · 실행 · 미실행이다. 건조의 끝점 게이트만 반영한 계획 수 (7,040) 는 실행 가능 수 · 완료 수가 아니며, "
                  "J_D 마스크 · ρ 선행 · UNFIT 은 여기서 따로 센다. run_units 는 작업을 만든 단위다 (완료와 같은 뜻이 아니다 — unit_classes 로 나눈다)"}
    pb = {}
    for key, reg in store["registry"].items():
        keys = [k for k, kind in reg.items() if kind != "phase_a"]
        done = sum(1 for k in keys if (store["phase_b"].get(k) or {}).get("status") == "DONE")
        nrb = Counter(store["phase_b"][k]["category"] for k in keys if (store["phase_b"].get(k) or {}).get("status") == "NOT_RUN")
        pb[key] = {"registered": len(keys), "done": done, "not_run": dict(sorted(nrb.items()))}
    unresolved = {"초과": 0, "실패": 0, "NOT_FOUND": 0}
    for reading in store["readings"].values():
        for r in reading.values():
            for lab in (r.get("final") or {}).values():
                if lab.get("computation") != "OK":
                    continue
                for pts in lab["grid"].values():
                    for p in pts:
                        if p["status"] in ("초과", "실패"):
                            unresolved[p["status"]] += 1
                claims = [c for ck in lab["compat_individual"].values() for c in ck.values()]
                claims += list(lab["compat_simultaneous"].values()) + [lab["compat_nominal"]]
                unresolved["NOT_FOUND"] += sum(1 for c in claims if c["value"] == "NOT_FOUND")
    return {"phase_a": pa, "phase_b": pb, "unresolved": unresolved,
            "not_run_b_units": dict(sorted(Counter(v["category"] for v in store["not_run_b"].values()).items()))}


# ---------------------------------------------------------------- 읽기 전용 건조 (C4 v2 §4-5 · 승인 경계 C4-0B1-A1 이후 규칙)
def dryrun_b(out, *, venv, seal, manifest_sha256, arrays_dir, h_arrays_dir, h_manifest_sha256, util_copy, p0_result,
             env_identity=None) -> dict:
    """Phase B 계획 (끝점 게이트 반영 상한 · 미정 항목) — identity · util 사본 (sha · AST · import 0) · Phase A 배열 (C6 결속) · 0b1 배열
    (바이트 대조 · 생성기 0) · P0 → PLAN_B.json 하나. 최적화 · 목적 호출 · util import · Sobol 생성 · 자료 개봉 0."""
    out = Path(out)
    e3a._guard([out, seal, arrays_dir, h_arrays_dir, util_copy, p0_result])
    if out.exists():
        raise HStop(f"{out} 가 이미 있다 — 덮어쓰지 않는다")
    t0 = time.monotonic()
    ident = e3a.identity(venv=venv, seal=seal, manifest_sha256=manifest_sha256, env_identity=env_identity)
    if not ident["ok"]:
        raise HStop(f"identity 실패: {ident['problems']}")
    ub = e3a._read(util_copy)
    if h._sha(ub) != c5.UTIL_COPY_SHA:
        raise HStop(f"util 사본 sha256 {h._sha(ub)} ≠ 기대 {c5.UTIL_COPY_SHA}")
    ust = p0.util_static_check(ub.decode("utf-8"))
    if not ust["ok"]:
        raise HStop(f"util 사본 정적 검사 실패: {ust.get('bad')}")
    arr = e3a.check_arrays(arrays_dir, seal=seal, manifest_sha256=manifest_sha256)
    hchk = h.check_h_arrays(h_arrays_dir, manifest_sha256=h_manifest_sha256, p0_result=p0_result, regenerate=False)
    if not hchk["complete"]:
        raise HStop(f"0b1 배열 봉인이 77 단위 전부가 아니다 ({hchk['units']})")
    p0b = e3a._read(p0_result)
    res = json.loads(p0b)
    q = h._p0_max_q(res)
    ext = {e.get("row"): e for e in res.get("extraction", []) if e.get("kind") == "analysis"}
    if set(ext) != set(h.ROWS) or any(ext[r].get("status") != "OK" for r in h.ROWS):
        raise HStop("P0 분석 추출 기록이 #0–#10 전부 OK 가 아니다")
    gates = {r: h.endpoint_gate(ext[r]["V_first"], ext[r]["V_last"]) for r in h.ROWS}
    us = h.units()
    gated = [u for u in us if u["objective"] == "J_Vs" and not gates[u["row"]]["accepted"]]
    fit = [u for u in us if u not in gated]
    names = {u["unit"] for u in fit}
    idx = _index(h_arrays_dir)
    prof = [e for e in idx.values() if e["stage"] == "profile" and e["unit"] in names]
    sim = [e for e in idx.values() if e["stage"] == "simultaneous" and e["unit"] in names]
    nom = [u for u in fit if p0.prior_compat(p0.NOMINAL[u["row"]], "0", u["region"], q)["status"] == "PRIOR_COMPATIBLE"]
    n_a = 2 * h.PHASE_A_N
    pb = {"units_after_endpoint_gate": len(fit), "profile_grid_points": len(prof), "profile_runs_ub": 4 * len(prof),
          "simultaneous_searches": len(sim), "simultaneous_runs_ub": 2 ** h.SIM_M * len(sim), "nominal_units": len(nom),
          "nominal_refine_ub": len(nom), "nominal_grid_evaluations_ub": N_NOMINAL * len(nom),
          "undetermined": ["J_D 유효 마스크 (자료 쪽 — C4-A 에서 셀마다 판정 · 빈 마스크면 그 셀 J_D · ρ 미실행)",
                           "ρ 선행 조건 (두 단일 목적 Phase A 완료 · 분모 유한 양수 — C4-A 기록)",
                           "Phase A UNFIT (유효 증인 0 이면 그 단위 Phase B 없음 — C4-A 기록)",
                           "시작 부족 (s2 · 중복 · Phase A 증인 수 — 실행 때 기록 · 실행 수를 줄이기만 한다)"]}
    pb["upper_bound_local_runs"] = pb["profile_runs_ub"] + pb["simultaneous_runs_ub"] + pb["nominal_refine_ub"]
    plan = {
        "schema": "reil-c4-0b2-plan-b-v1",
        "scope": "읽기 전용 건조 = 계획 · seed · 봉인만 읽음 (C4 v2 §4-5 · A1 이후 규칙) — Phase B 상한 (끝점 게이트 반영) · 미정 항목. 자료 개봉 0 · 맞춤 0",
        "execution": {"optimizer_calls": 0, "objective_calls": 0, "util_imported": False, "sobol_generated": 0},
        "phase_a": {"registered_runs": n_a * len(us), "planned_after_endpoint_gate": n_a * len(fit),
                    "note": "끝점 게이트만 반영한 계획 수 — 실행 가능 수 · 완료 수가 아니다. J_D 유효 마스크 · ρ 선행 조건에 따른 미실행 · 미해결은 "
                            "C4-A 기록에서 따로 센다 (회신 2026-10-14 §5-5)"},
        "phase_b": pb,
        "h4": {"endpoint_gated_units": len(gated), "controls": "양성 R1–R3 · 음성 D_abs — 끝점 수용 셀에서만 (이 자료에서는 0 셀)",
               "note": "11 셀 모두 끝점 수용 실패 → H4 22 단위 UNFIT (적용 가능성 실패 · 반증 아님 · ν 고정)"},
        "ray": {"status": "미구현", "reached": 0, "note": "유보 (범위 확인 §9-2) — 이 자료에서 도달 경로 0 · 완료로 세지 않는다"},
        "gates": {"h4_endpoint": {str(r): g for r, g in gates.items()}},
        "arrays": {"phase_a": {k: arr[k] for k in ("arrays_dir", "manifest_sha256", "c6_manifest_sha256", "c6_direct_match")}, "h": hchk},
        "identity": ident, "util_copy": str(util_copy), "util_copy_sha256": c5.UTIL_COPY_SHA, "p0_result": str(p0_result),
        "p0_result_sha256": h._sha(p0b),
        "not_this_step": "C4-E / C4-A / C4-B (자료 실행) · 비용 중단 규칙 · reserve — 별도 승인",
    }
    plan["elapsed_s"] = time.monotonic() - t0
    pbytes = c5.dump(plan)
    out.mkdir(exist_ok=False)
    (out / "PLAN_B.json").write_bytes(pbytes)
    if (out / "PLAN_B.json").read_bytes() != pbytes:
        raise HStop("다시 읽은 바이트가 쓴 것과 다르다")
    return {"ok": True, "out": str(out), "plan_sha256": h._sha(pbytes), "execution": plan["execution"], "identity_ok": True,
            "phase_a_planned_after_endpoint_gate": plan["phase_a"]["planned_after_endpoint_gate"],
            "phase_b_upper_bound_local_runs": pb["upper_bound_local_runs"], "elapsed_s": plan["elapsed_s"]}


# ---------------------------------------------------------------- CLI
def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="reil_c4_hb", description="REIL C4-0b2 — 읽기 전용 Phase B 건조 (기본 경로 없음)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dryrun-b")
    for a in ("--venv", "--seal", "--seal-manifest-sha256", "--arrays", "--h-arrays", "--h-manifest-sha256", "--util-copy",
              "--p0-result", "--out"):
        d.add_argument(a, required=True)
    a = ap.parse_args(argv)
    rec = dryrun_b(Path(a.out), venv=a.venv, seal=Path(a.seal), manifest_sha256=a.seal_manifest_sha256, arrays_dir=Path(a.arrays),
                   h_arrays_dir=Path(a.h_arrays), h_manifest_sha256=a.h_manifest_sha256, util_copy=Path(a.util_copy),
                   p0_result=Path(a.p0_result))
    print(json.dumps(c5._jsonable(rec), ensure_ascii=False, sort_keys=True))
    return 0 if rec.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
