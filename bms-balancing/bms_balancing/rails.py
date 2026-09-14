"""α·β 적합 결과표의 **난간** — `reviews/BML_R1_RESPONSE.md` §5 (리뷰어 Q4 표 채택).

네 층. 판정의 뜻이 층마다 다르다 — 섞으면 "반복 비율" 이 "비식별성" 으로 둔갑한다 (BML 1차 리뷰가 잡은 오류):

| 층 | 검사 | 판정 |
|---|---|---|
| 1 입력·후처리 계약 | 열 존재 · 유한값 · 기준행(cycle 0) 유일 · 중복 key · 단위 · **명시된 후처리 항등식의 오차** | 위반만 `error`, 오차는 언제나 기록 |
| 2 출력 패턴 | 파일별 상수 · 기준행과 비트 동일한 반복 · exact/tolerance zero · 두 LAM 일치율 · LLI≈1−x | `warning`/`info` — **원인·비식별성을 단정하지 않는다** |
| 3 optimizer 실제 제약 | 자유/고정 · lb/ub · active-bound 거리 · 종료 상태 · restart | **기록된 설정**과 비교. 설정 없이는 접촉을 확정하지 않는다; 설정 밖의 값만 `error` |
| 4 정량화 근거 | 잔차/profile 열의 존재와 범위 | `info` — 식별성 평가는 별도다. 반복 비율로 대체하지 않는다 |

"LAM 이 같으면 실패" 검사는 없다 — 정상적인 동등 열화나 의도된 제약(`a_NE ≥ 1`, Schmitt 2022 Fig.4b)도 탈락시킨다.
같은 함수가 규진팀 MATLAB 결과 xlsx 와 우리 `fit_cycles` 산출 양쪽에 걸린다 (`scripts/check_rails.py`).

항등식은 `main_blend_final.m:137-151` 의 수출 공식 그대로다 (37 행 전수에서 오차 0 실측, `REQ_FIT_RAILS.md` §1):
    x_cell = C_cell / C_0 · c_lit = C_cell·(a_PE + b_PE − b_NE) · LAM_PE = 1 − x·a_PE/a_PE0 ·
    LAM_NE = 1 − x·a_NE/a_NE0 · LLI = 1 − c_lit/c_lit0
"""
from __future__ import annotations

import math

#: 결과표의 11 열 (규진팀 `result_L_*.xlsx` 그대로) — 이 열만 요구한다; 더 있는 열은 4 층의 근거로 적는다
RESULT_COLUMNS = ("cycle", "C_cell", "x_cell", "a_PE", "b_PE", "a_NE", "b_NE", "c_lit", "LAM_PE", "LAM_NE", "LLI")
NUMERIC_COLUMNS = RESULT_COLUMNS[1:]
#: 적합 파라미터 열 — `gamma_Si` 는 있을 때만 (규진팀 표에는 없다)
PARAM_COLUMNS = ("a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si")
#: 4 층 — 있으면 근거로 적는 열
EVIDENCE_COLUMNS = ("rmse_pocv", "rmse_dvdq", "rmse_dqdv", "obj", "fval", "exitflag", "n_accepted", "n_starts",
                    "n_multistart", "run_id", "inputs_sha")
#: 항등식 이름 → (열, 식) — 식은 (행, 기준행) → 기대값
IDENTITIES = ("x_cell", "c_lit", "LAM_PE", "LAM_NE", "LLI")
LEVELS = ("error", "warning", "info")


def finding(layer: int, check: str, level: str, msg: str, **data) -> dict:
    assert level in LEVELS, level
    return {"layer": layer, "check": check, "level": level, "msg": msg, "data": data}


def _num(x) -> float:
    """셀 → float. bool 은 숫자가 아니다 (schema.py 의 `_is_num` 과 같은 규칙); 비어 있으면 nan."""
    if isinstance(x, bool) or x is None:
        return math.nan
    if isinstance(x, str) and not x.strip():
        return math.nan
    try:
        return float(x)
    except (TypeError, ValueError):
        return math.nan


def _cycle_key(x):
    v = _num(x)
    if math.isfinite(v) and v == int(v):
        return int(v)
    return str(x)


def _expected(r: dict, r0: dict) -> dict:
    x = r["C_cell"] / r0["C_cell"]
    c_lit = r["C_cell"] * (r["a_PE"] + r["b_PE"] - r["b_NE"])
    c_lit0 = r0["C_cell"] * (r0["a_PE"] + r0["b_PE"] - r0["b_NE"])
    return {"x_cell": x, "c_lit": c_lit,
            "LAM_PE": 1.0 - x * r["a_PE"] / r0["a_PE"],
            "LAM_NE": 1.0 - x * r["a_NE"] / r0["a_NE"],
            "LLI": 1.0 - c_lit / c_lit0}


def _numeric_rows(rows: list) -> list:
    return [{k: (_num(r.get(k)) if k != "cycle" else _cycle_key(r.get("cycle"))) for k in r} for r in rows]


# ── 1 층 — 입력·후처리 계약 ────────────────────────────────────────────────────────────────────────
def check_contract(rows: list, atol: float = 1e-9) -> list:
    p = []
    header = list(rows[0]) if rows else []
    missing = [c for c in RESULT_COLUMNS if c not in header]
    if missing:
        return [finding(1, "columns", "error", f"필수 열이 없다: {missing} (요구 11 열: {', '.join(RESULT_COLUMNS)})",
                        missing=missing)]
    if not rows:
        return [finding(1, "rows", "error", "행이 없다")]
    R = _numeric_rows(rows)
    for c in NUMERIC_COLUMNS:
        bad = [i for i, r in enumerate(R) if not math.isfinite(r[c])]
        if bad:
            p.append(finding(1, "finite", "error", f"{c}: 유한 숫자가 아닌 행 {bad}", column=c, rows=bad))
    keys = [r["cycle"] for r in R]
    dup = sorted({k for k in keys if keys.count(k) > 1}, key=str)
    if dup:
        p.append(finding(1, "duplicate_key", "error", f"cycle 중복 {dup} — 행을 셀 수 없다", keys=dup))
    refs = [i for i, r in enumerate(R) if r["cycle"] == 0]
    if len(refs) != 1:
        p.append(finding(1, "reference_row", "error", f"기준행(cycle 0)이 {len(refs)} 개다 — 항등식의 분모가 없다",
                         count=len(refs)))
    unit_bad = [i for i, r in enumerate(R) if math.isfinite(r["C_cell"]) and r["C_cell"] <= 0]
    unit_bad += [i for i, r in enumerate(R) if math.isfinite(r["x_cell"]) and r["x_cell"] <= 0]
    if unit_bad:
        p.append(finding(1, "units", "error", f"C_cell ≤ 0 또는 x_cell ≤ 0 인 행 {sorted(set(unit_bad))}",
                         rows=sorted(set(unit_bad))))
    over = [i for i, r in enumerate(R) if math.isfinite(r["x_cell"]) and r["x_cell"] > 1.0 + 1e-6]
    if over:
        p.append(finding(2, "units", "warning", f"x_cell > 1 인 행 {over} — 기준보다 용량이 크다 (기록만)", rows=over))
    if any(f["level"] == "error" for f in p):
        return p                                                       # 항등식은 계약이 선 뒤에만 뜻이 있다
    r0 = R[refs[0]]
    for name in IDENTITIES:
        errs = []
        for i, r in enumerate(R):
            e = _expected(r, r0)[name] - r[name]
            errs.append(abs(e) if math.isfinite(e) else math.inf)
        worst = max(errs)
        bad = [i for i, e in enumerate(errs) if e > atol]
        level = "error" if bad else "info"
        p.append(finding(1, "identity", level,
                         f"{name}: 후처리 항등식 최대 오차 {worst:.3e}" + (f" — 위반 행 {bad} (atol {atol:g})" if bad else ""),
                         name=name, max_abs_err=worst, rows=bad, atol=atol))
    return p


# ── 2 층 — 출력 패턴 (경고·정보만) ───────────────────────────────────────────────────────────────
def scan_patterns(rows: list, zero_tol: float = 1e-12) -> list:
    p = []
    if not rows or any(c not in rows[0] for c in RESULT_COLUMNS):
        return p
    R = _numeric_rows(rows)
    ref_i = next((i for i, r in enumerate(R) if r["cycle"] == 0), None)
    others = [i for i in range(len(R)) if i != ref_i]
    for c in PARAM_COLUMNS:
        if c not in rows[0]:
            continue
        vals = [r[c] for r in R]
        constant = len(vals) > 1 and all(v == vals[0] for v in vals)
        incl = excl = 0
        if ref_i is not None:
            incl = sum(1 for v in vals if v == vals[ref_i])
            excl = sum(1 for i in others if vals[i] == vals[ref_i])
        run, best = 1, 1
        for a, b in zip(vals, vals[1:]):
            run = run + 1 if a == b else 1
            best = max(best, run)
        data = {"column": c, "constant": constant, "max_run": best,
                "equal_to_reference": {"incl": incl, "excl": excl, "n": len(vals), "n_excl": len(others)},
                "n_unique": len(set(vals))}
        if constant or excl > 0:
            p.append(finding(2, "repeated_values", "warning",
                             f"{c}: " + ("파일 내부 상수 (고유값 1)" if constant else
                                         f"기준행과 비트 동일한 행 {excl}/{len(others)} (기준행 포함 {incl}/{len(vals)})")
                             + " — 패턴 기록이지 원인(bound·고정·축퇴) 단정이 아니다", **data))
        exact0 = sum(1 for v in vals if v == 0.0)
        tiny = [(R[i]["cycle"], v) for i, v in enumerate(vals) if v != 0.0 and abs(v) < zero_tol]
        if exact0 or tiny:
            p.append(finding(2, "zeros", "warning",
                             f"{c}: exact 0 {exact0} 행" + (f" · |v|<{zero_tol:g} 미세값 {tiny}" if tiny else ""),
                             column=c, exact_zero=exact0, tiny=tiny))
    if ref_i is not None and others:
        eq = sum(1 for i in others if abs(R[i]["LAM_PE"] - R[i]["LAM_NE"]) <= zero_tol)
        p.append(finding(2, "lam_agreement", "warning" if eq else "info",
                         f"LAM_PE ≈ LAM_NE (atol {zero_tol:g}) 기준행 제외 {eq}/{len(others)} — 정상 동등 열화·의도된 제약도 "
                         f"이렇게 보인다; 실패 조건이 아니다", equal_excl=eq, n_excl=len(others), atol=zero_tol))
        diff = [R[i]["LLI"] - (1.0 - R[i]["x_cell"]) for i in others]
        close = sum(1 for d in diff if abs(d) <= 1e-12)
        p.append(finding(2, "lli_vs_capacity", "info",
                         f"LLI ≈ 1−x_cell (atol 1e-12) 기준행 제외 {close}/{len(others)} · LLI−(1−x) 범위 "
                         f"{min(diff):.10f} ~ {max(diff):.10f}", close_excl=close, n_excl=len(others),
                         diff_min=min(diff), diff_max=max(diff)))
    return p


# ── 3 층 — optimizer 실제 제약 (기록된 설정과만 비교) ──────────────────────────────────────────────
def check_settings(rows: list, settings: dict | None, bound_tol: float = 1e-9) -> list:
    p = []
    if not rows or any(c not in rows[0] for c in RESULT_COLUMNS):
        return p
    if not isinstance(settings, dict) or not settings:
        return [finding(3, "settings_absent", "info",
                        "optimizer 설정(lb/ub/free/restart) 기록이 없다 — 경계 접촉·고정을 확정하지 않는다 "
                        "(관측 최댓값의 반복은 bound 가 아니다)")]
    R = _numeric_rows(rows)
    lb, ub = settings.get("lb"), settings.get("ub")
    if isinstance(lb, list) and isinstance(ub, list) and len(lb) == len(ub) == len(PARAM_COLUMNS):
        for j, c in enumerate(PARAM_COLUMNS):
            if c not in rows[0]:
                continue
            vals = [r[c] for r in R if math.isfinite(r[c])]
            if not vals:
                continue
            lo, hi = float(lb[j]), float(ub[j])
            outside = [R[i]["cycle"] for i, r in enumerate(R) if math.isfinite(r[c]) and (r[c] < lo - bound_tol or r[c] > hi + bound_tol)]
            if outside:
                p.append(finding(3, "outside_bounds", "error",
                                 f"{c}: 기록된 [{lo}, {hi}] 밖의 값 — cycle {outside}", column=c, cycles=outside, lb=lo, ub=hi))
                continue
            at_lb = sum(1 for v in vals if abs(v - lo) <= bound_tol)
            at_ub = sum(1 for v in vals if abs(v - hi) <= bound_tol)
            data = {"column": c, "lb": lo, "ub": hi, "at_lb": at_lb, "at_ub": at_ub, "n": len(vals),
                    "min_dist_lb": min(v - lo for v in vals), "min_dist_ub": min(hi - v for v in vals)}
            p.append(finding(3, "active_bound", "warning" if (at_lb or at_ub) else "info",
                             f"{c}: lb 접촉 {at_lb}/{len(vals)} · ub 접촉 {at_ub}/{len(vals)} · 최소 거리 lb {data['min_dist_lb']:.3e} "
                             f"ub {data['min_dist_ub']:.3e} (기록된 [{lo}, {hi}])", **data))
    else:
        p.append(finding(3, "settings_incomplete", "warning", "설정에 lb/ub 다섯 개가 없다 — 경계 축은 검사하지 않았다"))
    free = settings.get("free")
    if isinstance(free, list):
        fixed = [c for c in PARAM_COLUMNS if c in rows[0] and c not in free]
        for c in fixed:
            vals = {r[c] for r in R}
            p.append(finding(3, "fixed_parameter", "warning" if len(vals) > 1 else "info",
                             f"{c}: 설정상 고정인데 " + (f"고유값 {len(vals)} 개" if len(vals) > 1 else "상수다"),
                             column=c, n_unique=len(vals)))
    if "n_multistart" in settings:
        p.append(finding(3, "restarts", "info", f"MultiStart 시작점 {settings['n_multistart']} (기록)", n=settings["n_multistart"]))
    if "exitflag" in rows[0]:
        bad = [R[i]["cycle"] for i, r in enumerate(R) if not (math.isfinite(r["exitflag"]) and r["exitflag"] > 0)]
        p.append(finding(3, "exit_status", "warning" if bad else "info",
                         f"exitflag ≤ 0 인 cycle {bad}" if bad else "종료 상태 전부 양수", cycles=bad))
    return p


# ── 4 층 — 정량화 근거 ──────────────────────────────────────────────────────────────────────────
def summarize_evidence(rows: list) -> list:
    if not rows:
        return []
    present = [c for c in EVIDENCE_COLUMNS if c in rows[0]]
    R = _numeric_rows(rows)
    ranges = {}
    for c in present:
        vals = [r[c] for r in R if math.isfinite(r[c])]
        if vals:
            ranges[c] = [min(vals), max(vals)]
    msg = ("잔차/종료 상태 열 " + ", ".join(present) if present else
           "잔차·profile·종료 상태 열이 없다 — 식별성은 이 표로 평가할 수 없다 (별도 평가; 반복 비율로 대체하지 않는다)")
    return [finding(4, "evidence", "info", msg, present=present, ranges=ranges)]


def run_all(rows: list, settings: dict | None = None, atol: float = 1e-9) -> dict:
    """네 층 전부 → {"ok", "findings", "n_rows", "columns", "counts"}. `ok` 는 1·3 층의 `error` 가 없을 때만."""
    rows = [dict(r) for r in rows]
    f = check_contract(rows, atol=atol)
    if not any(x["level"] == "error" for x in f):
        f += scan_patterns(rows) + check_settings(rows, settings) + summarize_evidence(rows)
    counts = {lv: sum(1 for x in f if x["level"] == lv) for lv in LEVELS}
    return {"ok": counts["error"] == 0, "findings": f, "n_rows": len(rows),
            "columns": list(rows[0]) if rows else [], "counts": counts}
