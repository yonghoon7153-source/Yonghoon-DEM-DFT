"""Codex R13 (대상 `94add7b`) NO-GO — P1 4 · P2 5 의 회귀.

리뷰어의 반례를 그대로 옮긴다. 패키지는 `reviews/r13_repros/codex/`
(zip sha256 `c4d51fcff1e6843d69302d870784ce6d80181e9454a5ca5664de8832055f6f60`,
manifest 163/163 일치 실측).

핵심 축 하나: **두 산출이 서로 같다는 것과 각각이 올바른 과학 산출이라는 것은 다르다.**
전 판은 roster 의 *개수*만 봤고 *구성원*을 독립적으로 정하지 않았다 — 잘못된 모집단을
양쪽에 두 번 적으면 승격 가능이었다.
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bms_balancing import data as D          # noqa: E402
from bms_balancing import schema as S        # noqa: E402
from test_review_findings import matrix_row, seal_combo   # noqa: E402
from test_r12_selfreview import _receipt                  # noqa: E402


# ---------------------------------------------------------------- helpers

def _profile_rows(gammas, *, roster=None):
    """profile 본문 + gamma_roster. roster 를 안 주면 '정직한 전수' 를 만든다."""
    n = len(gammas)
    r = roster if roster is not None else {
        "authority": S.CANONICAL_GAMMA_GRID_N, "requested": S.CANONICAL_GAMMA_GRID_N,
        "succeeded": n, "missing": [],
    }
    raw = json.dumps(r, sort_keys=True)
    rec_d, ref_d = _receipt(), _receipt("5", "6", "7", "8")
    rec, ref = json.dumps(rec_d, sort_keys=True), json.dumps(ref_d, sort_keys=True)
    rows = []
    for g in gammas:
        rows.append({c: "" for c in S.PROFILE_ROW} | {
            "gamma_Si": repr(float(g)), "obj": "1.0", "obj_ratio_to_best": "1.0",
            "rmse_pocv": "1.0", "a_PE": "1.1", "b_PE": "-0.1", "a_NE": "1.0", "b_NE": "0.0",
            "bounds": "ok", "LAM_PE_pct": "1.0", "LAM_NE_pct": "1.0", "LLI_pct": "1.0",
            "n_ok": "1", "n_tried": "1", "run_id": "R", "profile_scale": "global",
            "inputs_sha": S.inputs_digest(rec_d), "ref_inputs_sha": S.inputs_digest(ref_d),
            "consumed_inputs": rec, "ref_consumed_inputs": ref,
            "gamma_roster": raw,
        })
    return rows


def _canonical_combo_rows(state="100"):
    keys = sorted(S.canonical_combo_keys(state))
    return [matrix_row(half_cell=hc, si=si, w_dqdv=repr(w)) for hc, si, w in keys]


# ---------------------------------------------------------------- P1-1

def test_g01_profile_wrong_grid_is_rejected():
    """`profile_wrong_grid` — γ 21 개를 0~0.4 간격 0.02 로. 개수는 정본과 같다.

    전 판: `authority == CANONICAL_GAMMA_GRID_N` 이 **숫자끼리**의 비교라 통과.
    """
    good = S.canonical_gamma_grid()
    assert len(good) == S.CANONICAL_GAMMA_GRID_N
    assert not S.check_rows("profile", _profile_rows(good), list(S.PROFILE_ROW)), "정본 격자 대조군이 막혔다"

    wrong = [round(0.02 * i, 10) for i in range(S.CANONICAL_GAMMA_GRID_N)]      # 0 ~ 0.40
    assert len(wrong) == len(good) and wrong != good
    probs = S.check_rows("profile", _profile_rows(wrong), list(S.PROFILE_ROW))
    assert probs, "개수만 같은 잘못된 γ 격자가 canonical 로 통과했다 (Codex R13 P1-1)"
    assert any("격자" in p or "γ" in p for p in probs), probs


def test_g02_profile_missing_may_not_be_duplicates():
    """`profile_twenty_duplicate_missing` — 본문 1 행 + `missing` 20 개가 전부 같은 값.

    산술(1 + 20 == 21)은 맞아서 전 판은 통과했다. 본문 ∪ missing 이 정본 격자여야 한다.
    """
    good = S.canonical_gamma_grid()
    rows = _profile_rows(good[:1], roster={
        "authority": S.CANONICAL_GAMMA_GRID_N, "requested": S.CANONICAL_GAMMA_GRID_N,
        "succeeded": 1, "missing": [good[1]] * 20,
    })
    probs = S.check_rows("profile", rows, list(S.PROFILE_ROW))
    assert probs, "중복 missing 으로 산술만 맞춘 1 행짜리가 통과했다 (Codex R13 P1-1)"


def test_g03_matrix_self_declared_authority_is_rejected():
    """`matrix_self_declared_one_row_authority` — 1 행이 authority=requested=succeeded=1.

    전 판: `requested == authority` 만 봤고 둘 다 산출이 스스로 적은 수라 통과.
    """
    ok = _canonical_combo_rows("100")
    assert len(ok) == 32, len(ok)
    assert not S.check_rows("matrix", seal_combo(ok), list(S.MATRIX_ROW), name="matrix_100.csv"), \
        S.check_rows("matrix", seal_combo(ok), list(S.MATRIX_ROW), name="matrix_100.csv")

    one = [matrix_row(half_cell="GITT", si="Li", w_dqdv="0.0")]
    rows = seal_combo(one, authority=1)
    probs = S.check_rows("matrix", rows, list(S.MATRIX_ROW), name="matrix_100.csv")
    assert probs, "스스로 authority=1 이라 적은 1 행이 canonical 로 통과했다 (Codex R13 P1-1)"


def test_g04_matrix_undeclared_member_is_rejected():
    """`matrix_wrong_member` — 32 행이지만 Si 하나가 미등록 `Li2`."""
    rows = _canonical_combo_rows("100")
    assert any(r["si"] == "Li" for r in rows)
    for r in rows:
        if r["si"] == "Li":
            r["si"] = "Li2"
            break
    probs = S.check_rows("matrix", seal_combo(rows), list(S.MATRIX_ROW), name="matrix_100.csv")
    assert probs, "선언되지 않은 Si 소스가 개수만 맞아 통과했다 (Codex R13 P1-1)"
    assert any("Li2" in p for p in probs), probs


def test_g05_canonical_contract_is_shared_with_producer():
    """정본 모집단은 **한 곳**에서 나와야 한다 — producer 와 checker 가 같은 함수를 쓴다."""
    import inspect

    from bms_balancing import verify as V
    src = inspect.getsource(V.cmd_matrix) + inspect.getsource(V.cmd_profile)
    assert "canonical_combo_keys" in src, "producer 가 matrix 모집단을 따로 만든다 (두 벌이면 갈린다)"
    assert "canonical_gamma_grid" in src, "producer 가 γ 격자를 따로 만든다"
