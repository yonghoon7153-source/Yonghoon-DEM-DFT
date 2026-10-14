"""REIL P0 — 자료를 처음 여는 결정적 단계 (맞춤 0 · 목적함수 호출 0 · 최적화 0).

승인: `docs/REIL_P0_APPROVAL_REQUEST_20261006.md` (사용자 승인 · 상태 문서 §17 · §19). 규칙 원문: v2 §1-3 · §1-5 · §3 · §4-2 ·
부속 A §2-5 · 부속 C §4 · 부속 D §3. 판정 함수는 `tests/test_reil_p0.py` 가 합성 입력으로 고정한다 (자료를 열기 전에 RED → GREEN).

    <venv>/bin/python -I bms-balancing/scripts/reil_p0.py run <xlsx> <util_LFP.py> <notebook.ipynb> <excerpts.json> <out.json>

- 그들 추출 경로 (`visualize_LFP_data` · `extract_battery_data`) 를 **고치지 않고** 부른다. 실패한 입력은 `P0_UNFIT` (다른 경로로 대신하지 않는다).
- raw 대응표 (부속 D §3-1) 의 행 범위는 그들 함수가 돌려주지 않으므로 같은 분절 규칙을 다시 계산해 적고, 그 배열이 그들 출력과 같은지 대조한다.
- 노트북은 JSON 텍스트로만 읽는다 (실행 0). `results/*.pkl` 은 열지 않는다. `util_LFP.py` 는 import 전에 AST 로 최상위 문장을 검사한다.
- 중단 (rc 3): sha256 불일치 · 노트북 상수 불일치 · util 최상위 부작용 · 시트 이름 집합 차이. 예외 (rc 4). 정상 (rc 0).
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import re
import sys
from fractions import Fraction as F

#: v2 §1-3 · 노트북 셀 9 `theoretical` — 십진 문자열 (판정은 이 문자열의 정확한 유리수로)
NOMINAL = [("1", "1", "1"), ("1", "1", "0.9"), ("1", "1", "0.8"), ("0.64", "1", "1"), ("1", "0.56", "1"), ("0.64", "1", "0.64"),
           ("0.64", "1", "0.58"), ("1", "0.56", "0.9"), ("1", "0.56", "0.8"), ("0.64", "0.56", "0.58"), ("0.64", "0.56", "0.51")]
LABELS = ["Fresh", "LLI-1", "LLI-2", "LAM_PE-1", "LAM_NE-1", "LAM_PE,LLI-1", "LAM_PE,LLI-2", "LAM_NE,LLI-1", "LAM_NE,LLI-2",
          "All mode-1", "All mode-2"]
#: 부속 D §3-3 — 분석 11 · 기준 2 · 밖 6 (C1-core 기록 §1 의 집합 · 실제 xlsx 를 본 목록이 아니다)
SHEETS_ANALYSIS = ["15-LFP 16-Gr Full-cell @ C_20", "15-LFP 16-Gr SOC-10", "15-LFP 16-Gr SOC-20", "12-LFP 16-Gr SOC-100",
                   "15-LFP 12-Gr Full-cell @ C_20", "Full cell after FM SOC 0", "Full cell after FM SOC 10", "15-LFP 12-Gr SOC-10",
                   "15-LFP 12-Gr SOC-20", "12-LFP 12-Gr SOC-10", "12-LFP 12-Gr SOC-20"]
SHEETS_REF = ["12-LFP C_20 Updated", "12-Graphite Half-cell @ C_20"]
SHEETS_OUTSIDE = ["12-LFP 16-Gr Full-cell @ C_20", "12-LFP 16-Gr SOC-10", "12-LFP Half-cell @ C_20", "12-Graphite Half-cell @ C_30",
                  "Half cell after FM", "12-14 12-15"]
SHEETS_ALL = SHEETS_ANALYSIS + SHEETS_REF + SHEETS_OUTSIDE
#: 노트북 셀 8 — 고치지 않는다 (P0 는 노트북 원문과 대조만)
CELL_IDX = [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0]
STEP_IDX = [6, 6, 6, 7, 6, 0, 0, 6, 6, 6, 6]
#: 노트북 셀 6 — 반쪽전지 기준 (시트 · step 6 · 셀 index 1)
REF_STEP, REF_CELL = 6, 1

TAUS = ("0", "0.02", "0.05")
#: v2 §4-1 · 부속 A §2-5 — m 상자 · Δ = d_P − d_N 의 영역별 구간 D
BOX_M = {"A0": (("0.6", "1.1"), ("0.5", "1.1")), "A1": (("0.3", "1.5"), ("0.3", "1.5")), "A2": (("0.3", "1.5"), ("0.3", "1.5"))}
D_INT = {"A0": ("1e-4", "0.5"), "A1": ("1e-4", "2"), "A2": ("-2", "2")}

#: 기대 sha256 (v1 §2 · wiki raw 2026-10-03)
SHA_XLSX = "fd50e09542be7adb2270963d65a6e7b5ccae1473a512f68462c2dd419d620ee1"
SHA_UTIL = "3c19e45ef8a64ce67cda1f623551e758d4c0f67086bbae02b978428d78de1c76"
SHA_NOTEBOOK = "388f2a6f101abf42ef8c7c1c627b7046e8bf900b913d22f83435b39eb81a9e29"
SIZE_XLSX = 10_841_377
NOTEBOOK_CELLS = (3, 4, 6, 8, 9, 11)          # 검토 묶음 `NOTEBOOK_SOURCE_EXCERPTS.json` 의 셀 — 원문 바이트 대조
UTIL_IMPORT_ALLOW = {"numpy", "pandas", "datetime", "scipy", "pickle", "matplotlib", "seaborn", "pymoo"}

#: 부속 D §3-1 — 기대 전극 반응 (방향 축의 "기대")
EXPECTED_REACTION = {"analysis": "완전지 충전 = PE 탈리튬 · NE 리튬화", SHEETS_REF[0]: "LFP 탈리튬", SHEETS_REF[1]: "흑연 리튬화"}


# ---------------------------------------------------------------- 사전 양립성 (부속 A §2-5)
def _fr(x) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def _dec(x) -> str:
    return f"{float(x):.12g}"


def _iv(lo, hi):
    return {"fraction": [_fr(lo), _fr(hi)], "decimal": [_dec(lo), _dec(hi)]}


def _clip(c, tau, box):
    lo, hi = max(c - tau, F(box[0])), min(c + tau, F(box[1]))
    return (lo, hi) if lo <= hi else None


def _max_q_fraction(max_q):
    if max_q is None or isinstance(max_q, bool):
        return None
    if isinstance(max_q, F):
        return max_q if max_q > 0 else None
    try:
        q = float(max_q)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(q) or q <= 0:
        return None
    return F(q)                                    # float 값 그대로의 정확한 유리수


def prior_compat(nominal, tau, region, max_q) -> dict:
    """{x ∈ A : ‖h(x) − h_true‖∞ ≤ τ} ≠ ∅ — 양립 ⇔ P ≠ ∅ 且 N ≠ ∅ 且 [min P − max I, max P − min I] ∩ D/max_q ≠ ∅ (닫힌 구간)."""
    t = F(tau)
    mp, mn, lii = (F(v) for v in nominal)
    q = _max_q_fraction(max_q)
    out = {"nominal": list(nominal), "tau": tau, "region": region, "D": list(D_INT[region]),
           "max_q_fraction": _fr(q) if q is not None else None}
    if q is None:
        return {**out, "status": "P0_UNFIT", "reason": "max_q 가 유한한 양수가 아님", "P": None, "N": None, "I": None,
                "lhs": None, "rhs": None}
    P, N = _clip(mp, t, BOX_M[region][0]), _clip(mn, t, BOX_M[region][1])
    I = (lii - t, lii + t)
    dlo, dhi = (F(v) for v in D_INT[region])
    rhs = (dlo / q, dhi / q)
    out.update(P=_iv(*P) if P else None, N=_iv(*N) if N else None, I=_iv(*I), rhs=_iv(*rhs))
    if P is None or N is None:
        return {**out, "status": "PRIOR_INCOMPATIBLE", "reason": "상자 ∩ 허용오차 구간이 빔", "lhs": None}
    lhs = (P[0] - I[1], P[1] - I[0])
    ok = lhs[0] <= rhs[1] and rhs[0] <= lhs[1]
    return {**out, "status": "PRIOR_COMPATIBLE" if ok else "PRIOR_INCOMPATIBLE",
            "reason": "구간 교차" if ok else "m_P − LII 구간과 D/max_q 가 교차하지 않음", "lhs": _iv(*lhs)}


def prior_table(max_q) -> list:
    return [{"row": i, "label": LABELS[i], **prior_compat(NOMINAL[i], tau, region, max_q)}
            for i in range(11) for tau in TAUS for region in ("A0", "A1", "A2")]


# ---------------------------------------------------------------- σ̂_v (v2 §3)
def sigma_v(v):
    import numpy as np
    from scipy.signal import savgol_filter
    try:
        a = np.asarray(v, dtype=float)
    except (TypeError, ValueError):
        return None, "UNFIT"
    if a.ndim != 1 or a.size < 21 or not np.all(np.isfinite(a)):
        return None, "UNFIT"
    r = a - savgol_filter(a, 21, 3, mode="interp")
    return float(np.sqrt(np.mean(r ** 2))), "OK"


# ---------------------------------------------------------------- 세 상태 (부속 D §3-2)
def combine(c, d) -> str:
    if "불일치" in (c, d):
        return "불일치"
    if c == d == "일치":
        return "일치"
    return "판정 불가"


def cycle_state(cycle_cols, values, n_cells):
    """명시적 cycle 열이 하나이고 셀이 하나인 시트에서만 선택 행에 결속한다 (그 밖은 결속 근거 없음 → 판정 불가). 추정 금지."""
    if not cycle_cols:
        return "판정 불가", "cycle 메타데이터 없음 (NaN 분절 번호 · step 순번 · 곡선 모양으로 채우지 않는다)"
    if len(cycle_cols) != 1:
        return "판정 불가", f"cycle 열 {len(cycle_cols)} 개 — 선택 셀에 결속할 근거 없음"
    if n_cells != 1:
        return "판정 불가", f"셀 {n_cells} 개 시트의 cycle 열 하나 — 선택 셀에 결속할 근거 없음"
    vals = []
    for v in values or []:
        try:
            f = float(v)
        except (TypeError, ValueError):
            return "판정 불가", "cycle 값 비수치"
        if not math.isfinite(f):
            return "판정 불가", "cycle 값 결측 · 비유한"
        vals.append(f)
    if not vals:
        return "판정 불가", "선택 행 없음"
    if all(f == 5 for f in vals):
        return "일치", f"열 {cycle_cols[0]!r} 의 선택 행 전부 5"
    return "불일치", f"열 {cycle_cols[0]!r} 의 선택 행 값 {sorted(set(vals))[:10]}"


def direction_state(step_values, current_sign, convention):
    """확인된 부호 규약 (장비 · 전지 문서) 이 있어야 판정한다. P0 입력에는 그런 문서가 없다 → raw 만 적고 판정 불가."""
    if convention is None:
        return "판정 불가", "부호 규약 · step 뜻을 정하는 문서가 P0 입력에 없음 (raw 칸에 보존 · 추측으로 통과시키지 않는다)"
    raise ValueError("이번 등록에 부호 규약 문서는 없다 — 규약을 쓰려면 새 등록")


# ---------------------------------------------------------------- 시트 이름 · util 정적 검사
def sheet_set_diff(actual) -> dict:
    a, want = list(actual), set(SHEETS_ALL)
    missing = [s for s in SHEETS_ALL if s not in set(a)]
    extra = [s for s in a if s not in want]
    return {"missing": missing, "extra": extra, "same": not missing and not extra and len(a) == len(set(a))}


def _is_docstring(node) -> bool:
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)


def util_static_check(text, allowed=None) -> dict:
    """최상위 문장이 import · 함수 정의 · 문서 문자열뿐인가 (import 시 실행되는 코드 = 부작용 후보). allowed 가 주어지면 import 최상위 이름도 대조."""
    tree = ast.parse(text)
    bad, imports = [], []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            imports += names
            if allowed is not None and any(n.split(".")[0] not in allowed for n in names):
                bad.append((node.lineno, "허용 밖 import " + ",".join(names)))
        elif isinstance(node, ast.FunctionDef) or _is_docstring(node):
            continue
        elif (isinstance(node, ast.ClassDef) and not node.decorator_list and not node.keywords
              and all(isinstance(b, ast.Name) for b in node.bases)
              and all(isinstance(n, ast.FunctionDef) or _is_docstring(n) for n in node.body)):
            continue                               # 메서드 정의만 있는 클래스 — 본문이 import 때 실행할 코드가 없다
        else:
            bad.append((node.lineno, type(node).__name__))
    return {"ok": not bad, "bad": bad, "imports": imports,
            "functions": [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]}


# ---------------------------------------------------------------- 실행 (자료 개봉)
class Stop(Exception):
    pass


def _sha_file(p) -> tuple:
    b = open(p, "rb").read()
    return hashlib.sha256(b).hexdigest(), len(b), b


def _notebook_check(nb_bytes, excerpts) -> dict:
    nb = json.loads(nb_bytes.decode("utf-8"))
    cells = nb["cells"]
    exc = {c["cell_index"]: c["source"] for c in excerpts["cells"]}
    diffs = [i for i in NOTEBOOK_CELLS if "".join(cells[i]["source"]) != "".join(exc[i])]
    src = {i: "".join(cells[i]["source"]) for i in NOTEBOOK_CELLS}
    lit = {}
    for i in (4, 8, 9):
        for node in ast.parse(src[i]).body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                try:
                    lit[node.targets[0].id] = ast.literal_eval(node.value)
                except ValueError:
                    lit[node.targets[0].id] = ast.unparse(node.value)
    const = {"sheets": lit.get("sheets") == SHEETS_ANALYSIS, "cell_idx": lit.get("cell_idx") == CELL_IDX,
             "step_idx": lit.get("step_idx") == STEP_IDX,
             "theoretical": [[F(str(x)) for x in r] for r in lit.get("theoretical", [])] == [[F(x) for x in r] for r in NOMINAL],
             "LFP_mass_factor": lit.get("LFP_mass_factor") == 20.16, "Gr_mass_factor": lit.get("Gr_mass_factor") == 11.4,
             "area": lit.get("area") == "0.25 * np.pi * 1.2 ** 2", "LFP_mass_12": lit.get("LFP_mass_12") == "13.5 * area",
             "Gr_mass_12": lit.get("Gr_mass_12") == "5.77 * area",
             "cell6_refs": all(s in src[6] for s in (f"sheet_name='{SHEETS_REF[0]}'", f"sheet_name='{SHEETS_REF[1]}'", "step_idx=6",
                                                     "PE_data = LFP_data[1]", "NE_data = Gr_data[1]"))}
    return {"cells_equal_excerpts": not diffs, "cells_differing": diffs, "constants": const, "ok": not diffs and all(const.values())}


def _sign(series) -> str:
    import pandas as pd
    s = pd.to_numeric(series, errors="coerce")
    if s.isna().any():
        return "비수치 · 결측 포함"
    if (s > 0).all():
        return "양"
    if (s < 0).all():
        return "음"
    if (s == 0).all():
        return "0"
    return "섞임"


def _their_drop(df):
    """visualize_LFP_data 47–61 행과 같은 열 제거 (기록용 재계산 — 그들 함수 결과와 배열 대조)."""
    import datetime
    try:
        dt = [c for c in df.columns if isinstance(c, datetime.datetime)][-1]
        df = df.iloc[:, df.columns.get_loc(dt) + 1:]
        dt_found = str(dt)
    except Exception:  # noqa: BLE001 — 그들 코드의 bare except 와 같은 분기
        dt_found = None
    return df.drop(columns=[c for c in df.columns if "Unnamed" in c or c.startswith("S")]), dt_found


def _raw_entry(xlsx, sheet, cell, step, their_arr, util):
    import numpy as np
    import pandas as pd
    df = pd.read_excel(xlsx, sheet_name=sheet)
    post, dt_found = _their_drop(df)
    n_cells = len(range(0, post.shape[1] - 1, 2))
    col = 2 * cell
    miss = post[post.iloc[:, col].isna()].index.to_list()
    miss.insert(0, 0)
    miss.append(post.shape[0])
    s0, s1 = miss[step], miss[step + 1]
    cc_end = post.iloc[s0:s1, col].idxmax()
    rows = list(range(s0 + 1, cc_end))
    mine = util.filter_first_occurrences_by_column(np.array([post.iloc[s0 + 1:cc_end, col], post.iloc[s0 + 1:cc_end, col + 1]]), 0)
    same = bool(their_arr is not None and mine.shape == their_arr.shape and np.array_equal(mine, their_arr, equal_nan=True))
    headers = [str(c) for c in df.columns]
    post_headers = [str(c) for c in post.columns]
    cyc = [str(c) for c in df.columns if re.search(r"cycle", str(c), re.I)]
    stepc = [str(c) for c in df.columns if re.search(r"step|mode|state", str(c), re.I)]
    curc = [str(c) for c in df.columns if re.search(r"current|curr|\(m?A\)", str(c), re.I)]
    cyc_vals = df.loc[rows, cyc[0]].tolist() if len(cyc) == 1 and rows else None
    raw = {"sheet": sheet, "cell_idx": cell, "step_idx": step, "nan_segment": step, "nan_segments_total": len(miss) - 1,
           "segment_rows_df_index": [int(s0), int(s1)], "cc_end_df_index": int(cc_end),
           "selected_rows_df_index": [rows[0], rows[-1]] if rows else None, "selected_rows_excel": [rows[0] + 2, rows[-1] + 2] if rows else None,
           "n_selected_rows": len(rows), "cycle_columns": cyc,
           "cycle_values_unique": sorted({str(v) for v in cyc_vals})[:20] if cyc_vals is not None else "없음",
           "step_columns": {c: sorted({str(v) for v in df.loc[rows, c].tolist()})[:20] for c in stepc} if rows else {},
           "current_columns_sign": {c: _sign(df.loc[rows, c]) for c in curc} if rows else {},
           "q_v_columns": [post_headers[col], post_headers[col + 1]]}
    c_state, c_why = cycle_state(cyc, cyc_vals, n_cells)
    d_state, d_why = direction_state(raw["step_columns"], raw["current_columns_sign"], None)
    cells_list = {"n_cells": n_cells, "headers_after_their_drop": post_headers,
                  "cell_columns": [[post_headers[c], post_headers[c + 1]] for c in range(0, post.shape[1] - 1, 2)],
                  "cell_idx_points_to": [post_headers[col], post_headers[col + 1]]}
    extraction = {"datetime_header_found": dt_found, "headers_original": headers,
                  "dropped_columns": [h for h in headers if h not in set(post_headers)], "replicate_equals_their_output": same}
    return raw, (c_state, c_why), (d_state, d_why), cells_list, extraction


def run(xlsx, util_path, nb_path, excerpts_path, out_path) -> int:
    import importlib.util
    import numpy as np
    import pandas as pd
    import scipy

    res = {"schema": "reil-p0/v1", "stopped": None, "fitting_calls": 0, "objective_calls": 0, "optimizer_calls": 0}
    try:
        # 1. 식별
        sx, nx, _ = _sha_file(xlsx)
        su, _, ub = _sha_file(util_path)
        sn, nn, nbb = _sha_file(nb_path)
        res["identity"] = {"xlsx": {"sha256": sx, "bytes": nx, "ok": sx == SHA_XLSX and nx == SIZE_XLSX},
                           "util_LFP.py": {"sha256": su, "ok": su == SHA_UTIL},
                           "notebook": {"sha256": sn, "bytes": nn, "ok": sn == SHA_NOTEBOOK}}
        if not all(v["ok"] for v in res["identity"].values()):
            raise Stop("sha256 불일치 (§6-2)")
        res["notebook_check"] = _notebook_check(nbb, json.load(open(excerpts_path, encoding="utf-8")))
        if not res["notebook_check"]["ok"]:
            raise Stop("노트북 상수 · 셀 원문 불일치 (§6-4)")
        res["util_static"] = util_static_check(ub.decode("utf-8"), UTIL_IMPORT_ALLOW)
        if not res["util_static"]["ok"]:
            raise Stop("util_LFP.py 최상위 부작용 후보 (§6-3)")
        names = pd.ExcelFile(xlsx).sheet_names
        res["sheet_names"] = {"actual": names, **sheet_set_diff(names)}
        if not res["sheet_names"]["same"]:
            raise Stop("시트 이름 집합 차이 — 그 뒤 범위는 사용자 결정 (§6-4 · 부속 D §3-3)")

        spec = importlib.util.spec_from_file_location("util_LFP", util_path)
        util = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(util)
        res["versions"] = {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__, "pandas": pd.__version__}

        # 2–3. 반쪽전지 기준 · max_q (노트북 셀 4 · 6 그대로)
        area = 0.25 * np.pi * 1.2 ** 2
        LFP_mass_12, Gr_mass_12 = 13.5 * area, 5.77 * area
        inputs, max_q = [], None
        ref = {}
        for sheet in SHEETS_REF:
            ent = {"sheet": sheet, "kind": "reference", "cell_idx": REF_CELL, "step_idx": REF_STEP}
            try:
                d = util.visualize_LFP_data(data_file=xlsx, sheet_name=sheet, step_idx=REF_STEP)
                arr = d[REF_CELL]
                ref[sheet] = arr
                ent.update(status="OK", n_points=int(arr.shape[1]), V_first=float(arr[1][0]), V_last=float(arr[1][-1]),
                           Q_first=float(arr[0][0]), Q_last=float(arr[0][-1]))
            except Exception as e:  # noqa: BLE001 — 그들 함수 실패 = 그 입력 P0_UNFIT (다른 경로로 대신하지 않는다)
                ent.update(status="P0_UNFIT", reason=f"{type(e).__name__}: {e}")
            inputs.append(ent)
        if SHEETS_REF[0] in ref:
            PE = ref[SHEETS_REF[0]]
            q_PE_hc = PE[0][np.argmin(PE[0]):np.argmax(PE[0])] / LFP_mass_12 * 20.16
            mq = float(np.max(q_PE_hc.flatten())) if q_PE_hc.size else float("nan")
            res["max_q"] = {"float": mq, "repr": repr(mq), "fraction": _fr(F(mq)) if math.isfinite(mq) else None,
                            "n_q_PE_hc": int(q_PE_hc.size), "status": "OK" if _max_q_fraction(mq) is not None else "P0_UNFIT",
                            "path": "노트북 셀 6 (PE_data = LFP_data[1] · [argmin:argmax] / LFP_mass_12 × 20.16) · util 718–719 np.max"}
            max_q = mq
        else:
            res["max_q"] = {"status": "P0_UNFIT", "reason": "PE 기준 추출 실패"}
        if SHEETS_REF[1] in ref:
            NE = ref[SHEETS_REF[1]]
            q_NE_hc = NE[0][np.argmin(NE[0]):np.argmax(NE[0])] / Gr_mass_12 * 11.4
            res["q_NE_hc_max_record_only"] = float(np.max(q_NE_hc)) if q_NE_hc.size else None

        # 2 · 5. 분석 11 — 추출 기록 · σ̂_v
        their = {}
        res["sigma_v"] = []
        for i, sheet in enumerate(SHEETS_ANALYSIS):
            ent = {"sheet": sheet, "kind": "analysis", "row": i, "label": LABELS[i], "cell_idx": CELL_IDX[i], "step_idx": STEP_IDX[i]}
            try:
                d = util.visualize_LFP_data(data_file=xlsx, sheet_name=sheet, step_idx=STEP_IDX[i], visualize=False)
                m = util.extract_battery_data(data=d, idx=CELL_IDX[i])
                their[sheet] = d[CELL_IDX[i]]
                ent.update(status="OK", n_points=int(len(m["Q_exp"])), V_first=float(m["V_exp"][0]), V_last=float(m["V_exp"][-1]),
                           Q_first=float(m["Q_exp"][0]), Q_exp_max=float(m["Q_exp_max"]))
                val, s = sigma_v(m["V_exp"])
            except Exception as e:  # noqa: BLE001
                ent.update(status="P0_UNFIT", reason=f"{type(e).__name__}: {e}")
                val, s = None, "UNFIT"
            inputs.append(ent)
            res["sigma_v"].append({"row": i, "sheet": sheet, "sigma_v_V": val, "status": s,
                                   "rule": "SG polyorder 3 · window 21 · mode=interp · 그들 경로의 V (중복 제거 뒤 · 보간 전) · 표본 순서"})
        res["extraction"] = inputs

        # 4. 사전 양립성 99 칸
        res["prior_table"] = prior_table(max_q)

        # 6 · 7. 대응표 · 셀 열 목록 (입력 13)
        res["correspondence"], res["cell_columns"] = [], []
        jobs = [(s, CELL_IDX[i], STEP_IDX[i], their.get(s), "analysis") for i, s in enumerate(SHEETS_ANALYSIS)]
        jobs += [(s, REF_CELL, REF_STEP, ref.get(s), s) for s in SHEETS_REF]
        for sheet, cell, step, arr, kind in jobs:
            try:
                raw, cy, di, cl, ex = _raw_entry(xlsx, sheet, cell, step, arr, util)
                res["correspondence"].append({"raw": raw, "cycle": {"state": cy[0], "basis": cy[1]},
                                              "direction": {"expected": EXPECTED_REACTION[kind], "state": di[0], "basis": di[1]},
                                              "overall": combine(cy[0], di[0])})
                res["cell_columns"].append({"sheet": sheet, **cl, **ex})
            except Exception as e:  # noqa: BLE001
                res["correspondence"].append({"raw": {"sheet": sheet}, "error": f"{type(e).__name__}: {e}", "overall": "판정 불가"})

        # 7. 밖 6 시트 — 이름 · 열 머리 · 행 수만
        res["outside_sheets"] = []
        for sheet in SHEETS_OUTSIDE:
            df = pd.read_excel(xlsx, sheet_name=sheet)
            res["outside_sheets"].append({"sheet": sheet, "headers": [str(c) for c in df.columns], "n_rows": int(df.shape[0])})
        rc = 0
    except Stop as e:
        res["stopped"] = str(e)
        rc = 3
    except Exception as e:  # noqa: BLE001
        res["stopped"] = f"예외 (§6-5): {type(e).__name__}: {e}"
        rc = 4
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
        f.write("\n")
    print(json.dumps({"rc": rc, "stopped": res["stopped"], "max_q": res.get("max_q"),
                      "statuses": {k: sum(1 for r in res.get("prior_table", []) if r["status"] == k)
                                   for k in ("PRIOR_COMPATIBLE", "PRIOR_INCOMPATIBLE", "P0_UNFIT")}}, ensure_ascii=False))
    return rc


if __name__ == "__main__":
    if len(sys.argv) != 7 or sys.argv[1] != "run":
        raise SystemExit(__doc__)
    sys.exit(run(*sys.argv[2:7]))
