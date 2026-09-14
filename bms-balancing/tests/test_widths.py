"""폭(축퇴) 기계가 **실제로 쓴 상자**를 보는가 — cycles 경로에 폭을 붙이기 전의 선결 조건.

왜 지금 이것부터인가: `reviews/BML_R1_RESPONSE.md` §12-5 가 "이 데이터에서 LAM 분할은 점추정으로 보고할 수 없고
폭과 함께 보고해야 한다" 로 닫혔다. 그런데 폭을 재는 세 함수(`active_bounds` · `near_optimal_extrema` ·
`mode_profile_extrema`)가 상자를 **모듈 상수 `LB5`/`UB5` 로 하드코딩**하고 있다. `fit_cycles` 는 이미
`--gamma-lb` 로 상자를 바꿀 수 있으므로(`multistart` 는 `lb`/`ub` 를 받는다), 지금 그대로 폭을 붙이면
**적합은 좁은 상자에서 하고 폭은 넓은 상자에서 재는** 산출이 나온다.

세 발견 전부 같은 뿌리다: **상자가 인자가 아니라 상수다.**
"""
from __future__ import annotations

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
