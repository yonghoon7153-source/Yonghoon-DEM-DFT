"""REIL P0 판정 규칙 — 합성 입력만 (REIL 자료 아님 · 자료를 열기 전에 RED 로 먼저 고정).

규칙 원문: 부속 A §2-5 (닫힌 구간식 · 정확 유리수 · P0_UNFIT) · §5-1 – §5-3 (분수 경계표 — 이 시험의 기대값) · v2 §3 (σ̂_v) ·
부속 D §3-2 (세 상태 · 종합) · §3-3 (시트 19 개 · 자동 대응 금지) · 승인 요청문 `docs/REIL_P0_APPROVAL_REQUEST_20261006.md` §4.
"""
from fractions import Fraction as F

import numpy as np
import pytest

from scripts import reil_p0 as p0

NOM = {i: r for i, r in enumerate(p0.NOMINAL)}


def st(i, tau, region, max_q):
    return p0.prior_compat(NOM[i], tau, region, max_q)["status"]


# ---- 부속 A §5-2 — τ = 0 · A0 의 필요충분 분수 경계 (끝점 닿음 = 양립) ----
@pytest.mark.parametrize("rows,lo,hi", [((1, 7), F(1, 1000), F(5)), ((2, 8), F(1, 2000), F(5, 2)),
                                        ((10,), F(1, 1300), F(50, 13)), ((6, 9), F(1, 600), F(25, 3))])
def test_a0_tau0_exact_fraction_boundaries(rows, lo, hi):
    for i in rows:
        assert st(i, "0", "A0", lo) == "PRIOR_COMPATIBLE"
        assert st(i, "0", "A0", hi) == "PRIOR_COMPATIBLE"            # 닫힌 구간 — 끝점에서 양립
        assert st(i, "0", "A0", hi + F(1, 10**12)) == "PRIOR_INCOMPATIBLE"
        assert st(i, "0", "A0", lo - F(1, 10**12)) == "PRIOR_INCOMPATIBLE"


def test_50_over_13_is_not_rounded_to_3_85():
    assert st(10, "0", "A0", 3.85) == "PRIOR_INCOMPATIBLE"            # 3.85 > 50/13 = 3.846153…
    assert st(10, "0", "A0", 3.846) == "PRIOR_COMPATIBLE"


# ---- 부속 A §5-1 — #0 · #4 · #5: τ = 0 은 A0 · A1 배제 · A2 양립 / τ = 0.02 는 max_q ≥ 1/400 ----
@pytest.mark.parametrize("i", [0, 4, 5])
def test_boundary_rows(i):
    for q in (0.5, 3.1, 7.0):
        assert st(i, "0", "A0", q) == "PRIOR_INCOMPATIBLE"
        assert st(i, "0", "A1", q) == "PRIOR_INCOMPATIBLE"
        assert st(i, "0", "A2", q) == "PRIOR_COMPATIBLE"
    for region in ("A0", "A1"):
        assert st(i, "0.02", region, F(1, 400)) == "PRIOR_COMPATIBLE"
        assert st(i, "0.02", region, F(1, 400) - F(1, 10**12)) == "PRIOR_INCOMPATIBLE"


# ---- 부속 A §5-3 — #2 · #8 의 τ = 0.02 / 0.05 경계 ----
def test_lli2_tau_boundaries():
    for i in (2, 8):
        assert st(i, "0.02", "A0", F(25, 8)) == "PRIOR_COMPATIBLE"
        assert st(i, "0.02", "A0", F(25, 8) + F(1, 10**12)) == "PRIOR_INCOMPATIBLE"
        assert st(i, "0.02", "A0", F(1, 2400)) == "PRIOR_COMPATIBLE"
        assert st(i, "0.05", "A0", F(5)) == "PRIOR_COMPATIBLE"
        assert st(i, "0.05", "A0", F(5) + F(1, 10**12)) == "PRIOR_INCOMPATIBLE"
        assert st(i, "0.05", "A0", F(1, 3000)) == "PRIOR_COMPATIBLE"


# ---- v2 §1-3 · #3 — m_P ≤ 0.69 · LII ≥ 0.95 → ±0.05 로도 A0 · A1 배제 (A2 는 G 없음) ----
def test_row3_structurally_incompatible_under_G():
    for tau in ("0", "0.02", "0.05"):
        for q in (0.01, 3.1, 100.0):
            assert st(3, tau, "A0", q) == "PRIOR_INCOMPATIBLE"
            assert st(3, tau, "A1", q) == "PRIOR_INCOMPATIBLE"


def test_empty_box_intersection_is_incompatible():
    # m_P 명목 1.3 은 A0 상자 [0.6, 1.1] 밖 — τ = 0.05 로도 P = ∅
    r = p0.prior_compat(("1.3", "1", "1.2"), "0.05", "A0", 3.0)
    assert r["status"] == "PRIOR_INCOMPATIBLE" and r["P"] is None


# ---- P0_UNFIT — 수치 · 자료 실패를 PRIOR_INCOMPATIBLE 로 바꾸지 않는다 ----
@pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf"), None])
def test_bad_max_q_is_unfit_not_incompatible(bad):
    assert st(1, "0", "A0", bad) == "P0_UNFIT"


def test_max_q_float_is_used_exactly():
    q = 0.1 + 0.2                       # 0.30000000000000004 — Fraction(q) 그대로
    r = p0.prior_compat(NOM[1], "0", "A0", q)
    assert r["max_q_fraction"] == str(F(q))


def test_table_shape_and_endpoints_as_fraction_and_decimal():
    t = p0.prior_table(3.1)
    assert len(t) == 99 and {(r["row"], r["tau"], r["region"]) for r in t} == {
        (i, tau, a) for i in range(11) for tau in ("0", "0.02", "0.05") for a in ("A0", "A1", "A2")}
    r = next(x for x in t if (x["row"], x["tau"], x["region"]) == (2, "0", "A0"))
    assert r["lhs"]["fraction"] == ["1/5", "1/5"] and r["lhs"]["decimal"][0].startswith("0.2")
    assert all(x["status"] == "P0_UNFIT" for x in p0.prior_table(float("nan")))


# ---- σ̂_v (v2 §3) ----
def test_sigma_v_zero_on_cubic_and_unfit_rules():
    v = np.polyval([1e-3, -2e-2, 0.1, 3.3], np.arange(40.0))
    val, status = p0.sigma_v(v)
    assert status == "OK" and val < 1e-10            # 3 차 다항식은 SG(3, 21) 가 정확히 재현
    assert p0.sigma_v(v[:20]) == (None, "UNFIT")      # 점 21 개 미만
    assert p0.sigma_v(v[:21])[1] == "OK"
    w = v.copy(); w[5] = np.nan
    assert p0.sigma_v(w) == (None, "UNFIT")


def test_sigma_v_matches_definition_on_noise():
    from scipy.signal import savgol_filter
    rng = np.random.default_rng(0)
    v = 3.3 + 0.01 * rng.standard_normal(200)
    want = float(np.sqrt(np.mean((v - savgol_filter(v, 21, 3, mode="interp")) ** 2)))
    assert p0.sigma_v(v) == (want, "OK")


# ---- 세 상태 (부속 D §3-2) ----
@pytest.mark.parametrize("c,d,want", [("일치", "일치", "일치"), ("불일치", "일치", "불일치"), ("일치", "불일치", "불일치"),
                                      ("불일치", "판정 불가", "불일치"), ("판정 불가", "일치", "판정 불가"),
                                      ("판정 불가", "판정 불가", "판정 불가")])
def test_combine(c, d, want):
    assert p0.combine(c, d) == want


def test_cycle_state_rules_no_inference():
    # 메타데이터 없음 → 판정 불가 (NaN 분절 번호 · step 순번으로 채우지 않는다)
    assert p0.cycle_state(cycle_cols=[], values=None, n_cells=1)[0] == "판정 불가"
    # cycle 열 하나 · 셀 하나 · 선택 행 전부 5 → 일치 · 하나라도 다르면 불일치
    assert p0.cycle_state(["Cycle"], [5, 5, 5.0], 1)[0] == "일치"
    assert p0.cycle_state(["Cycle"], [5, 5, 6], 1)[0] == "불일치"
    # 셀 둘 이상인 시트의 cycle 열 하나는 셀에 결속할 근거가 없다 → 판정 불가
    assert p0.cycle_state(["Cycle"], [5, 5], 2)[0] == "판정 불가"
    # 비수치 · 결측 → 판정 불가
    assert p0.cycle_state(["Cycle"], [5, None], 1)[0] == "판정 불가"
    assert p0.cycle_state(["Cycle", "Cycle.1"], [5, 5], 1)[0] == "판정 불가"


def test_direction_needs_documented_sign_convention():
    # P0 입력에 장비 · 전지 부호 규약 문서가 없다 → raw 를 적되 판정 불가 (추측으로 통과시키지 않는다)
    assert p0.direction_state(step_values=["CC_Chg"], current_sign="양", convention=None)[0] == "판정 불가"


# ---- 시트 이름 집합 (부속 D §3-3) ----
def test_sheet_set_exact_no_fuzzy_matching():
    assert p0.sheet_set_diff(list(p0.SHEETS_ALL)) == {"missing": [], "extra": [], "same": True}
    near = [s if s != "12-14 12-15" else "12-14 12-15 " for s in p0.SHEETS_ALL]
    d = p0.sheet_set_diff(near)
    assert d["same"] is False and d["missing"] == ["12-14 12-15"] and d["extra"] == ["12-14 12-15 "]


def test_fixed_tables_match_protocol():
    assert len(p0.SHEETS_ANALYSIS) == 11 and len(p0.SHEETS_ALL) == 19 and len(set(p0.SHEETS_ALL)) == 19
    assert p0.CELL_IDX == [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0]
    assert p0.STEP_IDX == [6, 6, 6, 7, 6, 0, 0, 6, 6, 6, 6]
    assert [tuple(map(F, r)) for r in p0.NOMINAL][3] == (F("0.64"), F(1), F(1))


def test_util_static_check_rejects_top_level_side_effects():
    ok = "import numpy as np\nfrom x import y\n\ndef f():\n    return open('a','w')\n"
    assert p0.util_static_check(ok)["ok"] is True
    for bad in ("import pickle\npickle.load(open('r.pkl','rb'))\n", "x = 1\n", "import os\nos.system('ls')\n",
                "if True:\n    import subprocess\n"):
        assert p0.util_static_check(bad)["ok"] is False


# ---- 노트북 대조 — 검토 묶음에 보존된 셀 원문 (같은 커밋 · 실행 0) 으로 합성 노트북을 만들어 (한 번뿐인 P0 실행 전에 확인) ----
EXC = "reviews/prereview_pybamm_reil_20261003/external/NOTEBOOK_SOURCE_EXCERPTS.json"


def _nb_from_excerpts(mutate=None):
    import json
    from pathlib import Path
    exc = json.loads((Path(__file__).resolve().parents[1] / EXC).read_text(encoding="utf-8"))
    cells = [{"cell_type": "code", "source": ["# filler\n"]} for _ in range(max(c["cell_index"] for c in exc["cells"]) + 1)]
    for c in exc["cells"]:
        cells[c["cell_index"]] = {"cell_type": "code", "source": list(c["source"])}
    if mutate:
        mutate(cells)
    return json.dumps({"cells": cells}).encode(), exc


def test_notebook_check_accepts_preserved_cells():
    nb, exc = _nb_from_excerpts()
    r = p0._notebook_check(nb, exc)
    assert r["ok"] is True and all(r["constants"].values()), r


@pytest.mark.parametrize("old,new", [("cell_idx = [1,0,0,0,0,0,1,1,1,0,0]", "cell_idx = [1,0,0,0,0,0,1,1,0,0,0]"),
                                     ("LFP_mass_factor = 20.16", "LFP_mass_factor = 20.15"),
                                     ("[0.64,0.56,0.51]", "[0.64,0.56,0.52]")])
def test_notebook_check_rejects_changed_constants(old, new):
    def mut(cells):
        for c in cells:
            c["source"] = [s.replace(old, new) for s in c["source"]]
    nb, exc = _nb_from_excerpts()
    nb2, _ = _nb_from_excerpts(mut)
    assert nb != nb2
    r = p0._notebook_check(nb2, exc)
    assert r["ok"] is False


# ---- raw 대응표 재계산 — 합성 xlsx + 보존된 util 사본 (검토 묶음 `util_LFP.py.txt` · 같은 커밋) 으로 그들 함수와 배열 대조 ----
UTIL_TXT = "reviews/prereview_pybamm_reil_20261003/external/util_LFP.py.txt"


def _load_util(tmp_path):
    import importlib.util
    import os
    from pathlib import Path
    os.environ.setdefault("MPLBACKEND", "Agg")
    src = (Path(__file__).resolve().parents[1] / UTIL_TXT).read_text(encoding="utf-8")
    p = tmp_path / "util_LFP.py"
    p.write_text(src, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("util_LFP_copy", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_raw_entry_matches_their_extraction_on_synthetic_sheet(tmp_path):
    pytest.importorskip("pymoo")
    import datetime
    import pandas as pd
    util = _load_util(tmp_path)
    nan = float("nan")
    q = [0.0, 0.5, 1.0, nan, 0.0, 0.2, 0.4, 0.4, 0.6, 0.5, nan, 0.0, 0.3]   # 분절 0 · 1 · 2 (중복 Q 0.4 · idxmax 뒤 하강)
    v = [3.0, 3.1, 3.2, nan, 3.3, 3.35, 3.4, 3.41, 3.5, 3.45, nan, 3.6, 3.7]
    # 장비 메타데이터 열은 datetime 머리 앞 — 그들 코드가 버린다 (raw 칸은 원래 머리에서 읽는다)
    df = pd.DataFrame({"Cycle": [4] * 4 + [5] * 7 + [6] * 2, "Step": ["CC_Chg"] * 13, "Current (mA)": [1.0] * 13,
                       datetime.datetime(2024, 1, 2): [nan] * 13, "Q1": q, "V1": v, "Q2": q, "V2": v})
    x = tmp_path / "syn.xlsx"
    df.to_excel(x, sheet_name="S1heet", index=False)
    d = util.visualize_LFP_data(data_file=str(x), sheet_name="S1heet", step_idx=1)
    raw, cy, di, cl, ex = p0._raw_entry(str(x), "S1heet", 1, 1, d[1], util)
    assert ex["replicate_equals_their_output"] is True
    assert raw["segment_rows_df_index"] == [3, 10] and raw["cc_end_df_index"] == 8 and raw["n_selected_rows"] == 4
    assert raw["cycle_columns"] == ["Cycle"] and cy[0] == "판정 불가"          # 셀 둘 (Q1/V1 · Q2/V2) → 결속 근거 없음
    assert di[0] == "판정 불가" and raw["current_columns_sign"] == {"Current (mA)": "양"}
    assert "Cycle" in ex["headers_original"] and cl["cell_idx_points_to"] == ["Q2", "V2"]


# ---- 실제 util_LFP.py 가 최상위에 ElementwiseProblem 하위 클래스 셋 (594 · 616 · 637 줄 — 메서드 정의만) 을 둔다 (2026-10-06 실행 전 점검) ----
def test_util_static_check_allows_method_only_classes_but_not_class_body_code():
    ok = "from m import Base\n\nclass P(Base):\n    def __init__(self, a):\n        super().__init__(n=1)\n\n    def _evaluate(self, x, out):\n        out['F'] = [x]\n"
    assert p0.util_static_check(ok)["ok"] is True
    for bad in ("class P:\n    import os\n    os.system('ls')\n", "class P:\n    x = open('f', 'w')\n",
                "@register\nclass P:\n    def f(self):\n        pass\n", "class P(make_base()):\n    def f(self):\n        pass\n"):
        assert p0.util_static_check(bad)["ok"] is False, bad
