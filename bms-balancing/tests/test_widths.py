"""폭(축퇴) 기계가 **실제로 쓴 상자**를 보는가 — cycles 경로에 폭을 붙이기 전의 선결 조건.

왜 지금 이것부터인가: `reviews/BML_R1_RESPONSE.md` §12-5 가 "이 데이터에서 LAM 분할은 점추정으로 보고할 수 없고
폭과 함께 보고해야 한다" 로 닫혔다. 그런데 폭을 재는 세 함수(`active_bounds` · `near_optimal_extrema` ·
`mode_profile_extrema`)가 상자를 **모듈 상수 `LB5`/`UB5` 로 하드코딩**하고 있다. `fit_cycles` 는 이미
`--gamma-lb` 로 상자를 바꿀 수 있으므로(`multistart` 는 `lb`/`ub` 를 받는다), 지금 그대로 폭을 붙이면
**적합은 좁은 상자에서 하고 폭은 넓은 상자에서 재는** 산출이 나온다.

세 발견 전부 같은 뿌리다: **상자가 인자가 아니라 상수다.**
"""
from __future__ import annotations

import csv
import pathlib
import sys

import numpy as np
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bms_balancing import verify as V             # noqa: E402
from bms_balancing.model import LB5, UB5          # noqa: E402

#: pristine 기준을 1 로 두면 LAM_NE = 1 − a_NE 가 되어 상자와 폭이 **직접** 대응한다.
#: (degradation_modes: LAM_NE = (a_NE_i·c_i − a_NE·c)/(a_NE_i·c_i), 여기서 a_NE_i=c_i=c=1)
REF_P = [1.0, 0.0, 1.0, 0.0, 0.25]
REF_C = 1.0
C_CELL = 1.0
BEST = [1.2, -0.1, 1.2, 0.0, 0.25]


def _flat_obj(best=BEST):
    """상자 안에서 사실상 평평한 목적함수 — 폭을 **상자만** 정하게 만든다.

    이렇게 해야 "폭이 좁아졌다" 가 최적화 실패가 아니라 상자 때문임이 분명해진다.
    """
    b = np.asarray(best, float)

    def obj(p):
        return 1.0 + 1e-12 * float(np.sum((np.asarray(p, float) - b) ** 2))
    return obj


def _narrow_box():
    """a_NE 와 γ 만 좁힌 상자. γ 하한 0.02 는 pyDMA Track C 규약(`--gamma-lb 0.02`) 그대로다."""
    lb = np.array(LB5, dtype=float).copy()
    ub = np.array(UB5, dtype=float).copy()
    lb[2], ub[2] = 1.19, 1.21          # a_NE → LAM_NE 는 -21 ~ -19 %p 로 갇힌다
    lb[4] = 0.02                        # γ 하한 (Track C)
    return lb, ub


# ── W-01 ────────────────────────────────────────────────────────────────
def test_w01_active_bounds_sees_the_box_that_was_actually_used():
    """[W-01] `active_bounds` 가 `LB5`/`UB5` 하고만 견준다 — `--gamma-lb 0.02` 로 돌린 적합이 **하한에 정확히
    붙어도** 아무 말도 안 한다.

    이건 규진팀 97 행에서 우리가 센 "경계에 정확히 붙은 32 행"(`BML_R1_RESPONSE` §2) 과 **같은 종류의 사실**이고,
    그 사실을 우리 산출에서는 못 세고 있다는 뜻이다. 실제로 pyDMA Track C 의 γ 사전 적합이 0.0200 으로
    하한에 붙었다 (§12-5) — 그런 해를 "경계에 붙지 않았다" 로 적으면 그건 위조다.
    """
    lb, ub = _narrow_box()
    pinned = [1.2, -0.1, 1.2, 0.0, 0.02]            # γ 가 이 상자의 하한에 정확히 붙은 해

    # 지금 있는 그대로: 상자를 물어볼 방법이 없어서 "경계 없음" 이라고 답한다.
    assert V.active_bounds(pinned) == [], "전제가 바뀌었다 — 기본 상자에서는 γ=0.02 가 경계가 아니다"

    hits = V.active_bounds(pinned, lb=lb, ub=ub)
    assert "gamma_Si=lb" in hits, hits


def test_w01b_active_bounds_without_a_box_still_means_the_default():
    """[W-01b] 상자를 안 주면 종전대로 `LB5`/`UB5` 다 — 기존 호출부(`cmd_matrix` 등)를 안 깬다."""
    at_default_lb = [1.0, -0.5, 1.0, -0.5, 0.0]
    assert set(V.active_bounds(at_default_lb)) == {
        "a_PE=lb", "b_PE=lb", "a_NE=lb", "b_NE=lb", "gamma_Si=lb"}
    assert V.active_bounds(at_default_lb) == V.active_bounds(at_default_lb, lb=LB5, ub=UB5)


# ── W-02 ────────────────────────────────────────────────────────────────
def test_w02_near_optimal_extrema_respects_the_given_box():
    """[W-02] `near_optimal_extrema` 는 `bounds = list(zip(LB5, UB5))` 로 상자를 **하드코딩**한다.

    평평한 목적함수를 주면 폭은 순전히 상자가 정한다. 기본 상자의 a_NE ∈ [1.0, 1.4] 는 LAM_NE 40 %p 를 주고,
    좁힌 상자 [1.19, 1.21] 은 2 %p 를 줘야 한다. 상자를 무시하면 좁혀도 40 %p 가 그대로 나온다 — 즉
    **적합은 좁은 상자에서 하고 폭은 넓은 상자에서 재는** 산출이 된다.
    """
    obj = _flat_obj()
    wide = V.near_optimal_extrema(obj, REF_P, REF_C, C_CELL, BEST, 1.0,
                                  tol=1.0, seeds=[], n_starts=3, seed=0)
    assert wide["LAM_NE"]["span"] > 30.0, wide["LAM_NE"]

    lb, ub = _narrow_box()
    tight = V.near_optimal_extrema(obj, REF_P, REF_C, C_CELL, BEST, 1.0,
                                   tol=1.0, seeds=[], n_starts=3, seed=0, lb=lb, ub=ub)
    assert tight["LAM_NE"]["span"] < 5.0, tight["LAM_NE"]
    assert -21.5 <= tight["LAM_NE"]["min"] and tight["LAM_NE"]["max"] <= -18.5, tight["LAM_NE"]


# ── W-03 ────────────────────────────────────────────────────────────────
def test_w03_mode_profile_extrema_respects_the_given_box():
    """[W-03] `mode_profile_extrema` 도 같은 하드코딩이 두 군데다 — `bounds` 와 **격자를 까는 `box`**.

    격자가 기본 상자에서 깔리면 좁은 상자 밖의 mode 값을 후보로 세우고, 그 값들은 도달 불가로 버려진다.
    버려지는 건 맞지만 `grid_range_pct` 가 상자를 배신한다 — 산출에 그대로 실리는 값이다.
    """
    obj = _flat_obj()
    lb, ub = _narrow_box()
    tight = V.mode_profile_extrema(obj, REF_P, REF_C, C_CELL, BEST, 1.0,
                                   tol=1.0, n_grid=7, n_starts=2, seed=0, lb=lb, ub=ub)
    assert tight["LAM_NE"]["span"] < 5.0, tight["LAM_NE"]
    g_lo, g_hi = tight["LAM_NE"]["grid_range_pct"]
    assert -21.5 <= g_lo and g_hi <= -18.5, tight["LAM_NE"]["grid_range_pct"]


# ── W-04 ────────────────────────────────────────────────────────────────
def test_w04_a_box_that_is_not_a_box_is_refused():
    """[W-04] 상자를 인자로 열면 **틀린 상자**도 들어올 수 있다. lb > ub 나 길이가 5 가 아닌 것은 조용히
    이상한 폭을 내는 대신 거절한다 — 폭은 인용되는 숫자다."""
    obj = _flat_obj()
    bad_lb = np.array([1.0, -0.5, 1.4, -0.5, 0.0])      # a_NE 의 lb 가 ub 보다 크다
    bad_ub = np.array([1.4, 0.0, 1.0, 0.1, 0.5])
    with pytest.raises(ValueError):
        V.near_optimal_extrema(obj, REF_P, REF_C, C_CELL, BEST, 1.0,
                               tol=1.0, seeds=[], n_starts=2, seed=0, lb=bad_lb, ub=bad_ub)
    with pytest.raises(ValueError):
        V.near_optimal_extrema(obj, REF_P, REF_C, C_CELL, BEST, 1.0,
                               tol=1.0, seeds=[], n_starts=2, seed=0, lb=[1.0, 1.0], ub=UB5)


# ── W-05 ────────────────────────────────────────────────────────────────
def test_w05_multistart_uses_the_same_box_rule():
    """[W-05] `multistart` 도 `resolve_box` 를 쓴다 — 상자 규칙이 **한 자리**여야 한다.

    R14 P2-2 의 교훈이 이것이다: "존재·비공백" 규칙이 두 벌이라 한 벌만 고쳐졌고 절반이 뚫려 있었다.
    상자도 같다. 지금은 네 함수(`multistart`·`active_bounds`·두 extrema)가 같은 함수를 부른다.
    """
    obj = _flat_obj()
    with pytest.raises(ValueError):
        V.multistart(obj, n_starts=2, lb=np.array([1.0, -0.5, 1.4, -0.5, 0.0]),
                     ub=np.array([1.4, 0.0, 1.0, 0.1, 0.5]))
    with pytest.raises(ValueError):
        V.multistart(obj, n_starts=2, lb=[1.0, 1.0], ub=UB5)


def test_w05b_resolve_box_defaults_and_passthrough():
    """[W-05b] 상자를 안 주면 `LB5`/`UB5` 그대로, 주면 그것 그대로 — 기본 경로가 안 바뀐다."""
    lo, hi = V.resolve_box()
    assert np.array_equal(lo, np.asarray(LB5, float)) and np.array_equal(hi, np.asarray(UB5, float))
    lb, ub = _narrow_box()
    lo2, hi2 = V.resolve_box(lb, ub)
    assert np.array_equal(lo2, lb) and np.array_equal(hi2, ub)
    with pytest.raises(ValueError):                 # 비유한 값도 거절
        V.resolve_box([1.0, -0.5, 1.0, -0.5, float("nan")], UB5)


# ── W-06 ────────────────────────────────────────────────────────────────
def test_w06_fit_cycles_records_bounds_against_the_box_it_used(tmp_path):
    """[W-06] **production 경로의 같은 결함.** `cycles.fit_cycles` 가 행마다 적는 `bounds` 열은
    `active_bounds(p)` 를 상자 없이 부른다 — 그래서 `--gamma-lb` 로 올린 하한에 γ 가 **정확히 붙어도**
    `"-"`(경계 없음)로 적힌다.

    이건 가정이 아니라 지금 나가는 산출이다. `BML_R1_RESPONSE` §2 에서 우리가 규진팀 97 행 중 32 행을
    "경계에 정확히 붙었다" 로 세었는데, 같은 검사를 우리 산출에는 못 걸고 있었다는 뜻이다.

    fixture 는 두 번 돌린다: 먼저 기본 상자에서 γ 를 얻고, 그 위로 하한을 올려 **붙을 수밖에 없게** 만든다.
    """
    sys.path.insert(0, str(ROOT / "tests"))
    from test_cycles import _cycle_workbook               # noqa: PLC0415
    from test_r6_internal import _synth_root              # noqa: PLC0415
    from bms_balancing import cycles as C                 # noqa: PLC0415

    src = _synth_root(tmp_path)
    wb = _cycle_workbook(src, tmp_path / "cyc.xlsx", n_cycles=2)
    hc = src / "data/half_cell/GITT/pristine.xlsx"
    base = dict(cell="w06", n_starts=2, seed=0, scale_seed=0)

    free = C.fit_cycles(src, hc, wb, "Li", **base)
    g_free = max(float(r["gamma_Si"]) for r in free["rows"])
    lb_gamma = min(round(g_free + 0.05, 6), float(UB5[4]))
    assert lb_gamma > g_free, (g_free, lb_gamma)         # 하한을 자유 최적값 **위로** 올린다

    pinned = C.fit_cycles(src, hc, wb, "Li", gamma_lb=lb_gamma, **base)
    at_lb = [r for r in pinned["rows"] if abs(float(r["gamma_Si"]) - lb_gamma) < 1e-6]
    assert at_lb, [(r["cycle"], r["gamma_Si"]) for r in pinned["rows"]]   # fixture 전제

    for r in at_lb:
        assert "gamma_Si=lb" in r["bounds"], (r["cycle"], r["gamma_Si"], r["bounds"], lb_gamma)


# ── W-08 ────────────────────────────────────────────────────────────────
def test_w08_a_hex_digest_that_looks_like_a_float_is_not_an_infinite_number():
    """[W-08] `schema._finite_problems` 가 JSON 안의 **모든 문자열**에 `float()` 를 걸어 유한성을 본다.
    의도는 손으로 쓴 `"1e999"`·`"Infinity"` 를 잡는 것이었는데(자체 리뷰 C06), **hex digest 가 우연히 과학적
    표기법처럼 생기면 같이 걸린다.**

        float("796984e18157") == inf        # 796984 × 10^18157

    `inputs_sha` 는 12 자 hex 이고 `run_id` 는 32 자 hex 다. 즉 **입력이 바뀔 때마다 주사위를 굴리는 셈**이고,
    걸리면 정상 산출이 "스키마 위반" 으로 게시를 거부당한다. 실측으로 한 번 터졌다 —
    `test_i6p_05` 가 `! degeneracy 산출이 스키마를 어긴다 (1 건) … degeneracy.inputs_sha: 유한하지 않은 값
    ('796984e18157')` 로 실패했다 (tmp_path 가 digest 에 들어가 실행마다 값이 달라진다).

    계약: **식별자 필드는 숫자가 아니다.** 숫자 필드의 `"1e999"` 는 계속 잡고, digest·id 는 라벨로 둔다.
    """
    import math
    from bms_balancing import schema as S

    assert math.isinf(float("796984e18157")), "전제가 바뀌었다 — 이 문자열은 inf 로 파싱돼야 한다"

    # (1) digest 가 그렇게 생겼어도 문제로 세지 않는다
    assert S._finite_problems({"inputs_sha": "796984e18157"}, "d") == []
    assert S._finite_problems({"run_id": "796984e18157be4f796984e18157be4f"}, "d") == []

    # (2) 그렇다고 C06 의 구멍이 다시 열리면 안 된다 — **숫자 필드**의 무한대는 그대로 잡는다
    assert S._finite_problems({"best_obj": "1e999"}, "d"), "숫자 필드의 무한 문자열은 계속 잡아야 한다"
    assert S._finite_problems({"LLI_percent": {"min": "Infinity"}}, "d")
    assert S._finite_problems({"tol_percent_of_best": float("inf")}, "d")


def test_w08b_check_degeneracy_publishes_an_artifact_whose_digest_looks_numeric():
    """[W-08b] 위 결함의 **산출 쪽 모습**: 그런 digest 를 가진 정상 degeneracy JSON 이 거부됐다.

    여기서는 `_finite_problems` 가 내는 메시지만 본다 (다른 계약 위반은 이 시험의 축이 아니다).
    """
    from bms_balancing import schema as S
    j = {"state": "100", "si_source": "Li", "half_cell": "GITT", "run_id": "796984e18157be4f796984e18157be4f",
         "inputs_sha": "796984e18157", "best_obj": 1.0, "n_starts": 1}
    bad = [m for m in S._finite_problems({k: v for k, v in j.items()}, "degeneracy") if "유한하지" in m]
    assert bad == [], bad


# ══ 여기부터 본 작업: 폭을 cycles 산출에 붙인다 ═════════════════════════════
#
# `reviews/BML_R1_RESPONSE.md` §12-5 가 "이 데이터에서 LAM 분할은 점추정으로 보고할 수 없고 폭과 함께
# 보고해야 한다" 로 닫혔다. 그런데 `fit_cycles` 는 아직 점추정만 낸다 — 누가 그 CSV 를 표로 옮기면
# 우리가 쓴 경고는 안 따라간다. **폭을 같은 행에** 둔다 (별도 파일이면 또 떨어진다).

def _cycles_fixture(tmp_path, n_cycles=2):
    sys.path.insert(0, str(ROOT / "tests"))
    from test_cycles import _cycle_workbook                # noqa: PLC0415
    from test_r6_internal import _synth_root               # noqa: PLC0415
    src = _synth_root(tmp_path)
    wb = _cycle_workbook(src, tmp_path / "cyc.xlsx", n_cycles=n_cycles)
    return src, wb, src / "data/half_cell/GITT/pristine.xlsx"


WIDTH_COLS = ("width_status", "width_tol", "width_is_lower_bound",
              "LAM_PE_lo", "LAM_PE_hi", "LAM_NE_lo", "LAM_NE_hi", "LLI_lo", "LLI_hi")


def test_w09_cycles_row_declares_the_width_columns():
    """[W-09] 계약부터. 폭이 **행의 일부**여야 점추정만 옮겨 적는 일이 안 생긴다."""
    from bms_balancing import schema as S
    assert set(WIDTH_COLS) <= set(S.CYCLES_ROW), sorted(set(WIDTH_COLS) - set(S.CYCLES_ROW))
    assert S.required_columns("cycles") == S.CYCLES_ROW
    # 점추정 바로 뒤에 온다 — 표로 옮길 때 잘려 나가지 않도록
    i = S.CYCLES_ROW.index("LLI")
    assert S.CYCLES_ROW[i + 1] == "width_status", S.CYCLES_ROW[i:i + 3]


def test_w10_widths_off_is_empty_not_zero(tmp_path):
    """[W-10] **안 잰 것과 0 은 다르다.** 폭을 안 켜면 값이 비어 있어야 한다 — 0 으로 채우면 읽는 쪽이
    "폭이 0 이다(= 완벽히 식별된다)" 로 읽는다. 이건 본체 게이트 61차가 잡은 축과 같다: **측정 실패가
    성공 영수증이 되면 안 된다.**"""
    from bms_balancing import cycles as C                  # noqa: PLC0415
    src, wb, hc = _cycles_fixture(tmp_path)
    out = C.fit_cycles(src, hc, wb, "Li", cell="w10", n_starts=2, seed=0, scale_seed=0)
    for r in out["rows"]:
        assert r["width_status"] == "not_requested", r["width_status"]
        for c in ("LAM_PE_lo", "LAM_PE_hi", "LAM_NE_lo", "LAM_NE_hi", "LLI_lo", "LLI_hi",
                  "width_tol", "width_is_lower_bound"):
            assert r[c] == "", (c, repr(r[c]))
    assert out["settings"]["widths"] is False


def test_w11_widths_on_bracket_the_point_estimate(tmp_path):
    """[W-11] 켜면 폭이 붙고, **점추정이 그 안에 있어야 한다.**

    단위가 이 시험의 진짜 축이다 — `near_optimal_extrema` 는 %, 행의 `LAM_*`/`LLI` 는 분수다.
    나누는 것을 잊으면 폭이 100 배가 되고 점추정은 여전히 안에 들어가므로 **범위 검사만으로는 안 걸린다.**
    그래서 폭의 크기에도 상한을 건다.
    """
    from bms_balancing import cycles as C                  # noqa: PLC0415
    src, wb, hc = _cycles_fixture(tmp_path)
    out = C.fit_cycles(src, hc, wb, "Li", cell="w11", n_starts=2, seed=0, scale_seed=0,
                       widths=True, width_tol=0.01, width_starts=2)
    assert out["settings"]["widths"] is True and out["settings"]["width_tol"] == 0.01
    for r in out["rows"]:
        assert r["width_status"] == "measured", r
        assert r["width_is_lower_bound"] is True, r["width_is_lower_bound"]
        assert float(r["width_tol"]) == 0.01
        for mode in ("LAM_PE", "LAM_NE", "LLI"):
            lo, hi, pt = float(r[f"{mode}_lo"]), float(r[f"{mode}_hi"]), float(r[mode])
            assert lo <= pt <= hi, (r["cycle"], mode, lo, pt, hi)
            assert hi - lo <= 2.0, (r["cycle"], mode, "폭이 분수 단위를 넘는다 — %/분수 혼동?", lo, hi)


def test_w12_the_width_is_measured_in_the_box_the_fit_used(tmp_path):
    """[W-12] **W-02 의 값어치가 여기서 나온다.** γ 하한을 올려 상자를 좁히면 **보고되는 폭도 좁아져야** 한다.
    폭 함수가 모듈 상수를 읽던 전 판에서는 이 둘이 같은 값이 나왔다 — 적합은 좁은 상자, 폭은 넓은 상자."""
    from bms_balancing import cycles as C                  # noqa: PLC0415
    src, wb, hc = _cycles_fixture(tmp_path)
    base = dict(cell="w12", n_starts=2, seed=0, scale_seed=0, widths=True, width_tol=0.05, width_starts=2)
    wide = C.fit_cycles(src, hc, wb, "Li", **base)
    tight = C.fit_cycles(src, hc, wb, "Li", gamma_lb=0.45, **base)   # γ 를 [0.45, 0.50] 으로 가둔다
    assert tight["settings"]["lb"][4] == 0.45
    w = max(float(r["LAM_NE_hi"]) - float(r["LAM_NE_lo"]) for r in wide["rows"])
    t = max(float(r["LAM_NE_hi"]) - float(r["LAM_NE_lo"]) for r in tight["rows"])
    assert t < w, ("좁힌 상자인데 폭이 안 줄었다 — 폭이 적합의 상자를 안 본다", w, t)


def test_w13_a_failed_width_is_not_a_number(tmp_path, monkeypatch):
    """[W-13] 폭 계산이 실패하면 **조용히 값을 지어내지 않는다.** 상태가 `failed` 이고 칸은 비어 있어야 한다.
    적합 자체는 살아 있으므로 산출을 통째로 버리지도 않는다 — 못 잰 것은 못 쟀다고 적는다."""
    from bms_balancing import cycles as C                  # noqa: PLC0415
    from bms_balancing import verify as V                  # noqa: PLC0415
    src, wb, hc = _cycles_fixture(tmp_path)

    def boom(*a, **k):
        raise RuntimeError("일부러 실패")
    monkeypatch.setattr(V, "near_optimal_extrema", boom)
    monkeypatch.setattr(C, "near_optimal_extrema", boom, raising=False)

    out = C.fit_cycles(src, hc, wb, "Li", cell="w13", n_starts=2, seed=0, scale_seed=0,
                       widths=True, width_tol=0.01, width_starts=2)
    for r in out["rows"]:
        assert r["width_status"] == "failed", r["width_status"]
        for c in ("LAM_PE_lo", "LAM_NE_hi", "LLI_lo"):
            assert r[c] == "", (c, repr(r[c]))
        assert r["LAM_NE"] not in (None, ""), "적합 자체는 살아 있어야 한다"


def test_w14_the_published_artifact_carries_widths_and_passes_both_validators(tmp_path):
    """[W-14] 계약 고리를 닫는다: CLI 로 게시한 CSV 가 (a) 폭 열을 싣고 (b) `check_rails` 와
    `check_u14 --schema-only` 를 **둘 다** 통과해야 한다.

    열을 늘리면 난간·승격 게이트가 같이 움직인다 — 늘려 놓고 검사를 안 돌리면 그 열은 계약이 아니라 장식이다.
    """
    import json as _json
    import subprocess

    src, wb, hc = _cycles_fixture(tmp_path)
    out = tmp_path / "out"
    rc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/fit_cycles.py"),
         "--data-root", str(src), "--half-cell", str(hc), "--full-cell", str(wb),
         "--cell", "w14", "--si-source", "Li", "--starts", "2", "--seed", "0", "--scale-seed", "0",
         "--widths", "--width-tol", "0.05", "--width-starts", "2", "--out", str(out)],
        cwd=ROOT, capture_output=True, text=True, timeout=1800)
    assert rc.returncode == 0, (rc.returncode, rc.stdout[-1500:], rc.stderr[-1500:])

    art = out / "cycles_w14_Li.csv"
    rows = list(csv.DictReader(art.open(encoding="utf-8")))
    assert rows and all(r["width_status"] == "measured" for r in rows), [r["width_status"] for r in rows]
    for r in rows:
        for mode in ("LAM_PE", "LAM_NE", "LLI"):
            assert float(r[f"{mode}_lo"]) <= float(r[mode]) <= float(r[f"{mode}_hi"]), (r["cycle"], mode)
        assert r["width_is_lower_bound"] == "True", r["width_is_lower_bound"]
        assert float(r["width_tol"]) == 0.05

    meta = _json.loads((out / "cycles_w14_Li.csv.meta.json").read_text(encoding="utf-8"))
    assert meta["widths"] is True and meta["width_tol"] == 0.05 and meta["width_starts"] == 2
    assert meta["width_method"] == "near_optimal_extrema", meta.get("width_method")

    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_rails.py"), str(art)],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, ("check_rails", r.returncode, r.stdout[-1200:], r.stderr[-800:])

    # ⚠ `check_u14` 의 rc 를 0 으로 단언하지 않는다 — **작업 트리가 dirty 하면 provenance 로 막히는 것이
    #   정상**이고(그게 그 게이트의 일이다), baseline 이 없으면 `baseline_absent` 도 선다. 이 시험의 축은
    #   "열을 늘린 것이 **계약**을 깨뜨리지 않는가" 이므로 그 버킷만 본다. (전 판은 rc 0 을 단언했다가
    #   dirty 트리에서 빨갛게 났다 — 검사기가 옳고 단언이 틀렸다.)
    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(out), "--schema-only"],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    line = next(l for l in r.stdout.splitlines() if l.startswith("PROMOTION "))
    blocked = _json.loads(line[len("PROMOTION "):])["blocked_by"]
    for bucket in ("schema", "provenance_cols", "content", "unit", "controls", "numbers", "alias"):
        assert blocked[bucket] == 0, (bucket, blocked, r.stdout[-1200:])
    assert "새 스키마: 전부 갖췄다" in r.stdout, r.stdout[-800:]


def test_w15_the_width_columns_are_a_tagged_union_not_just_optional(tmp_path):
    """[W-15] 폭 칸을 "비어도 되는 열" 로 풀어 주면, `measured` 라고 적어 놓고 칸을 비운 행이 통과한다.
    그건 §12-5 가 막으려던 것과 **같은 종류의 위조**다 — 폭을 적었다고 말하면서 폭이 없다.

    계약을 tagged union 으로 못 박는다 (shape 의 `gamma_witness` 짝 규칙과 같은 모양):
      · `width_status` 는 셋 중 하나 — measured · not_requested · failed
      · `measured` 면 여덟 칸이 **전부 차** 있어야 한다
      · 나머지 둘이면 여덟 칸이 **전부 비어** 있어야 한다 (0 으로 채우는 것도 위반)
    """
    from bms_balancing import schema as S
    from test_cycles import _cycle_workbook                # noqa: F401,PLC0415  (fixture 경로 확보)

    base = {c: "1" for c in S.CYCLES_ROW}
    base.update({"cell": "x", "bounds": "-", "run_id": "r", "inputs_sha": "s", "consumed_inputs": "{}"})
    W = ("width_tol", "width_is_lower_bound", "LAM_PE_lo", "LAM_PE_hi",
         "LAM_NE_lo", "LAM_NE_hi", "LLI_lo", "LLI_hi")

    def probs(row):
        return [m for m in S.check_rows("cycles", [row], list(S.CYCLES_ROW), name="t.csv") if "width" in m or "폭" in m]

    ok_off = dict(base, width_status="not_requested", **{c: "" for c in W})
    assert probs(ok_off) == [], probs(ok_off)

    ok_on = dict(base, width_status="measured", width_is_lower_bound="True",
                 **{c: "0.01" for c in W if c != "width_is_lower_bound"})
    assert probs(ok_on) == [], probs(ok_on)

    # (1) measured 인데 칸이 비었다 — 위조
    lying = dict(ok_on, LAM_NE_lo="")
    assert probs(lying), "measured 라고 적고 폭을 비운 행이 통과했다"

    # (2) not_requested 인데 값이 있다 — 안 잰 것에 값이 붙었다
    ghost = dict(ok_off, LAM_NE_lo="0.0", LAM_NE_hi="0.0")
    assert probs(ghost), "안 쟀다면서 폭이 0 으로 적힌 행이 통과했다"

    # (3) 모르는 상태
    weird = dict(ok_off, width_status="maybe")
    assert probs(weird), "선언에 없는 width_status 가 통과했다"


# ══ W-16~W-18: 폭을 읽는 쪽 (`scripts/width_report.py`) ═════════════════════
#
# 비교는 **축 하나만 달라야** 뜻이 있다. 손으로 두 번 돌리면 한 줄에서 seed 를 흘려도 눈에 안 보이므로
# (`run_states.sh` 가 같은 이유로 스크립트다), 읽는 쪽이 sidecar 를 보고 **거부**한다.

def _fake_widths_csv(d, name, *, w_dqdv, seed=0, spans=(1.0, 5.0, 2.0)):
    """폭이 실린 cycles CSV + sidecar 한 벌 — 리포터는 순수 reader 라 적합을 안 돌려도 된다."""
    import json as _j
    from bms_balancing import schema as S                  # noqa: PLC0415
    d.mkdir(parents=True, exist_ok=True)
    art = d / name
    rows = []
    for k in (0, 1):
        r = {c: "" for c in S.CYCLES_ROW}
        r.update(cell="syn", cycle=str(k), C_cell="1", x_cell="1", a_PE="1.1", b_PE="0", a_NE="1.1",
                 b_NE="0", gamma_Si="0.25", c_lit="1", obj="1", rmse_pocv="1", rmse_dvdq="1", rmse_dqdv="1",
                 n_starts="4", n_accepted="4", scale_seed="0", scale_pocv="1", scale_dvdq="1", scale_dqdv="1",
                 bounds="-", run_id="r", inputs_sha="s", consumed_inputs="{}",
                 width_status="measured", width_tol="0.01", width_is_lower_bound="True")
        for m, sp in zip(("LAM_PE", "LAM_NE", "LLI"), spans):
            r[m] = str(k * 0.01)
            r[f"{m}_lo"] = str(k * 0.01 - sp / 200.0)      # 폭 = sp %p (행 단위는 분수)
            r[f"{m}_hi"] = str(k * 0.01 + sp / 200.0)
        rows.append(r)
    with art.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(S.CYCLES_ROW)); w.writeheader(); w.writerows(rows)
    meta = {"cell": "syn", "si_source": "Li", "starts": 4, "seed": seed, "scale_seed": 0,
            "w_pocv": 1.0, "w_dvdq": 1.0, "w_dqdv": float(w_dqdv), "optimizer": "L-BFGS-B (scipy)",
            "lb": [1.0, -0.5, 1.0, -0.5, 0.0], "ub": [1.4, 0.0, 1.4, 0.1, 0.5],
            "initial": [1.08, -0.04, 1.05, -0.03, 0.25], "gamma_prefit": False, "gamma_lb": None,
            "n_multistart": 4, "cycles": [0, 1],
            "widths": True, "width_tol": 0.01, "width_starts": 3, "width_method": "near_optimal_extrema"}
    art.with_name(art.name + ".meta.json").write_text(
        _j.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return art


def _report(*args):
    import subprocess
    return subprocess.run([sys.executable, str(ROOT / "scripts/width_report.py"), *map(str, args)],
                          cwd=ROOT, capture_output=True, text=True, timeout=300)


def test_w16_width_report_prints_the_interval_and_compares_one_axis(tmp_path):
    """[W-16] 표와 비교가 실제로 나온다. 비교는 **축 하나**(w_dqdv)만 다를 때."""
    a = _fake_widths_csv(tmp_path / "w0", "cycles_syn_Li.csv", w_dqdv=0, spans=(1.0, 20.0, 4.0))
    b = _fake_widths_csv(tmp_path / "w1", "cycles_syn_Li.csv", w_dqdv=1, spans=(1.0, 10.0, 8.0))
    r = _report(a)
    assert r.returncode == 0 and "하한" in r.stdout, (r.returncode, r.stdout[-600:], r.stderr[-400:])
    r = _report(a, b, "--axis", "w_dqdv")
    assert r.returncode == 0, (r.returncode, r.stdout[-600:], r.stderr[-600:])
    assert "좁아졌다" in r.stdout and "넓어졌다" in r.stdout, r.stdout[-800:]
    assert "0.500" in r.stdout, ("LAM_NE 20→10 %p 면 비가 0.5 여야 한다", r.stdout[-800:])


def test_w17_width_report_refuses_a_comparison_that_moved_two_things(tmp_path):
    """[W-17] **가드가 이 도구의 값어치다.** 축 말고 다른 설정이 다르면 비교를 거부하고 **무엇이 다른지 짚는다**.
    거부하지 않으면 "dQ/dV 를 넣으니 폭이 좁아졌다" 가 실은 seed 차이인 경우를 못 가른다."""
    a = _fake_widths_csv(tmp_path / "A", "cycles_syn_Li.csv", w_dqdv=0, seed=0)
    b = _fake_widths_csv(tmp_path / "B", "cycles_syn_Li.csv", w_dqdv=1, seed=7)      # 둘이 움직였다
    r = _report(a, b, "--axis", "w_dqdv")
    assert r.returncode == 2, (r.returncode, r.stdout[-400:])
    assert "다른 설정이 다르다" in r.stderr and "seed" in r.stderr, r.stderr[-500:]

    same = _fake_widths_csv(tmp_path / "C", "cycles_syn_Li.csv", w_dqdv=0, seed=0)   # 축이 안 움직였다
    r = _report(a, same, "--axis", "w_dqdv")
    assert r.returncode == 2 and "가 같다" in r.stderr, (r.returncode, r.stderr[-400:])


def test_w18_width_report_refuses_artifacts_that_carry_no_width(tmp_path):
    """[W-18] 폭 없는 산출이나 **안 잰 행이 섞인** 산출로는 표를 그리지 않는다 — 모집단을 말할 수 없다."""
    from bms_balancing import schema as S                  # noqa: PLC0415
    a = _fake_widths_csv(tmp_path / "A", "cycles_syn_Li.csv", w_dqdv=0)

    rows = list(csv.DictReader(a.open(encoding="utf-8")))
    rows[1]["width_status"] = "not_requested"
    for c in ("width_tol", "width_is_lower_bound", "LAM_PE_lo", "LAM_PE_hi",
              "LAM_NE_lo", "LAM_NE_hi", "LLI_lo", "LLI_hi"):
        rows[1][c] = ""
    mixed = tmp_path / "M" / "cycles_syn_Li.csv"
    mixed.parent.mkdir(parents=True, exist_ok=True)
    with mixed.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(S.CYCLES_ROW)); w.writeheader(); w.writerows(rows)
    r = _report(mixed)
    assert r.returncode == 2 and "measured" in r.stderr, (r.returncode, r.stderr[-400:])

    bare = tmp_path / "N" / "cycles_syn_Li.csv"
    bare.parent.mkdir(parents=True, exist_ok=True)
    cols = [c for c in S.CYCLES_ROW if not c.startswith("width") and not c.endswith(("_lo", "_hi"))]
    with bare.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    r = _report(bare)
    assert r.returncode == 2 and "폭 열이 없다" in r.stderr, (r.returncode, r.stderr[-400:])
