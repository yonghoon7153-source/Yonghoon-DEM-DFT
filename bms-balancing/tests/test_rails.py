"""α·β 적합 결과표의 **난간** (`reviews/BML_R1_RESPONSE.md` §5 — 리뷰어 Q4 표 채택).

네 층: (1) 입력·후처리 계약 — 위반만 실패, 오차 기록 · (2) 출력 패턴 — **경고**, 원인·비식별성 단정 금지 ·
(3) optimizer 실제 제약 — 기록된 설정과 비교 (관측 최댓값과 구분) · (4) 정량화 근거 — 잔차/profile 의 존재.
"LAM 이 같으면 실패" 검사는 만들지 않는다. metadata 없이 상한 접촉을 확정하지 않는다.

같은 검사가 규진팀 MATLAB 결과 xlsx 와 우리 `fit_cycles` 산출 양쪽에 걸린다 — 두 벌로 두지 않는다.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bms_balancing import rails as R          # noqa: E402


def _table(n=6, *, a_pe=None, a_ne=None, b_ne=None):
    """항등식이 **정확히** 성립하는 합성 결과표 (11 열, 기준행 cycle 0)."""
    c0 = 0.004
    rows = []
    for k in range(n):
        x = 1.0 - 0.02 * k
        C = c0 * x
        ape = (a_pe[k] if a_pe is not None else 1.08 + 0.004 * k)
        bpe = -0.14 - 0.003 * k
        ane = (a_ne[k] if a_ne is not None else 1.01 + 0.002 * k)
        bne = (b_ne[k] if b_ne is not None else -0.001 * (k + 1))
        c_lit = C * (ape + bpe - bne)
        rows.append({"cycle": k, "C_cell": C, "x_cell": x, "a_PE": ape, "b_PE": bpe, "a_NE": ane, "b_NE": bne,
                     "c_lit": c_lit, "LAM_PE": None, "LAM_NE": None, "LLI": None})
    r0 = rows[0]
    for r in rows:
        r["LAM_PE"] = 1.0 - r["x_cell"] * r["a_PE"] / r0["a_PE"]
        r["LAM_NE"] = 1.0 - r["x_cell"] * r["a_NE"] / r0["a_NE"]
        r["LLI"] = 1.0 - r["c_lit"] / r0["c_lit"]
    return rows


def _by(findings, level=None, check=None):
    return [f for f in findings if (level is None or f["level"] == level) and (check is None or f["check"] == check)]


def test_rails_01_clean_table_has_no_errors_and_no_repeat_warnings():
    rep = R.run_all(_table())
    assert rep["ok"] is True and not _by(rep["findings"], "error"), rep["findings"]
    assert not _by(rep["findings"], "warning", "repeated_values"), rep["findings"]
    # 항등식 오차는 위반이 아니어도 **기록**된다
    ident = _by(rep["findings"], check="identity")
    assert ident and all(f["data"]["max_abs_err"] <= 1e-12 for f in ident), ident


def test_rails_02_identity_violation_is_an_error_with_the_error_recorded():
    rows = _table()
    rows[3]["LLI"] += 1e-3
    rep = R.run_all(rows)
    errs = _by(rep["findings"], "error", "identity")
    assert rep["ok"] is False and errs, rep["findings"]
    e = next(f for f in errs if f["data"]["name"] == "LLI")
    assert abs(e["data"]["max_abs_err"] - 1e-3) < 1e-9 and e["data"]["rows"] == [3], e
    # 수출 공식 그대로: c_lit = C_cell·(a_PE + b_PE − b_NE)
    rows = _table(); rows[2]["c_lit"] *= 1.01
    rep = R.run_all(rows)
    assert any(f["data"]["name"] == "c_lit" for f in _by(rep["findings"], "error", "identity")), rep["findings"]


def test_rails_03_repeated_values_and_lam_agreement_are_warnings_never_errors():
    """`a_PE` 가 기준행과 비트 동일하게 반복되고 두 LAM 이 일치해도 — **경고**만 낸다 (원인을 단정하지 않는다)."""
    rows = _table(a_pe=[1.1] * 6, a_ne=[1.0] * 6)
    rep = R.run_all(rows)
    assert rep["ok"] is True and not _by(rep["findings"], "error"), rep["findings"]
    rep_w = {f["data"]["column"]: f for f in _by(rep["findings"], "warning", "repeated_values")}
    assert "a_PE" in rep_w and rep_w["a_PE"]["data"]["equal_to_reference"] == {"incl": 6, "excl": 5, "n": 6, "n_excl": 5}, rep_w
    assert "a_NE" in rep_w and rep_w["a_NE"]["data"]["constant"] is True, rep_w
    lam = _by(rep["findings"], check="lam_agreement")
    assert lam and lam[0]["level"] in ("warning", "info") and lam[0]["data"]["equal_excl"] == 5, lam
    # 정상 표에서는 반복 경고가 없다 — 검사가 새 축을 실제로 본다
    assert not _by(R.run_all(_table())["findings"], "warning", "repeated_values")


def test_rails_04_reference_row_duplicates_and_nonfinite_are_contract_errors():
    rows = _table()
    rep = R.run_all(rows[1:])                                        # 기준행 없음
    assert rep["ok"] is False and _by(rep["findings"], "error", "reference_row"), rep["findings"]
    rep = R.run_all(rows + [dict(rows[2])])                          # 중복 cycle
    assert rep["ok"] is False and _by(rep["findings"], "error", "duplicate_key"), rep["findings"]
    bad = _table(); bad[4]["a_PE"] = float("nan")
    rep = R.run_all(bad)
    assert rep["ok"] is False and _by(rep["findings"], "error", "finite"), rep["findings"]
    neg = _table(); neg[1]["C_cell"] = -neg[1]["C_cell"]
    assert _by(R.run_all(neg)["findings"], "error", "units")


def test_rails_05_bounds_are_judged_only_against_recorded_settings():
    """metadata 없이 상한 접촉을 확정하지 않는다 — 설정을 주면 active-bound 거리를 **기록**하고 (경고),
    설정 밖의 값만 실패다."""
    rows = _table(a_ne=[1.0] * 6)
    rep = R.run_all(rows)
    assert not _by(rep["findings"], "error") and _by(rep["findings"], "info", "settings_absent"), rep["findings"]
    assert not _by(rep["findings"], check="active_bound")
    settings = {"lb": [1.0, -0.5, 1.0, -0.5, 0.0], "ub": [1.4, 0.0, 1.4, 0.1, 0.5],
                "free": ["a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si"], "n_multistart": 20}
    rep = R.run_all(rows, settings=settings)
    ab = {f["data"]["column"]: f for f in _by(rep["findings"], check="active_bound")}
    assert ab["a_NE"]["level"] == "warning" and ab["a_NE"]["data"]["at_lb"] == 6 and ab["a_NE"]["data"]["min_dist_lb"] == 0.0, ab
    assert ab["a_PE"]["data"]["at_lb"] == 0 and ab["a_PE"]["data"]["at_ub"] == 0, ab
    assert rep["ok"] is True
    out = _table(); out[2]["a_PE"] = 1.5                             # 기록된 ub 밖 — 계약 위반
    # 항등식은 다시 맞춘다 (경계 검사만 보려고)
    out = _rebuild(out)
    rep = R.run_all(out, settings=settings)
    assert rep["ok"] is False and _by(rep["findings"], "error", "outside_bounds"), rep["findings"]


def _rebuild(rows):
    r0 = rows[0]
    for r in rows:
        r["c_lit"] = r["C_cell"] * (r["a_PE"] + r["b_PE"] - r["b_NE"])
    for r in rows:
        r["LAM_PE"] = 1.0 - r["x_cell"] * r["a_PE"] / r0["a_PE"]
        r["LAM_NE"] = 1.0 - r["x_cell"] * r["a_NE"] / r0["a_NE"]
        r["LLI"] = 1.0 - r["c_lit"] / r0["c_lit"]
    return rows


def test_rails_06_cli_reads_xlsx_and_csv_and_exit_codes_are_typed(tmp_path):
    import pandas as pd
    rows = _table()
    xlsx, csv_ = tmp_path / "result_L_x.xlsx", tmp_path / "result.csv"
    pd.DataFrame(rows).to_excel(xlsx, index=False)
    pd.DataFrame(rows).to_csv(csv_, index=False)

    def cli(*args):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/check_rails.py"), *map(str, args)],
                           cwd=ROOT, capture_output=True, text=True, timeout=120)
        line = next((l for l in r.stdout.splitlines() if l.startswith("RAILS ")), None)
        return r.returncode, r.stdout + r.stderr, (json.loads(line[len("RAILS "):]) if line else None)

    rc, out, j = cli(xlsx)
    assert rc == 0 and j and j["ok"] is True and j["files"][0]["n_rows"] == 6, out[-800:]
    rc, out, j = cli(csv_, "--json", tmp_path / "r.json")
    assert rc == 0 and json.loads((tmp_path / "r.json").read_text(encoding="utf-8"))["ok"] is True, out[-800:]
    bad = _table(); bad[3]["LLI"] += 1e-3
    pd.DataFrame(bad).to_excel(tmp_path / "bad.xlsx", index=False)
    rc, out, j = cli(tmp_path / "bad.xlsx")
    assert rc == 2 and j["ok"] is False and "LLI" in out, out[-800:]
    pd.DataFrame(rows).drop(columns=["c_lit"]).to_excel(tmp_path / "nocol.xlsx", index=False)
    rc, out, j = cli(tmp_path / "nocol.xlsx")
    assert rc == 3 and "c_lit" in out, out[-800:]
    # 여러 파일 + 설정 파일
    (tmp_path / "settings.json").write_text(json.dumps({"lb": [1.0, -0.5, 1.0, -0.5, 0.0], "ub": [1.4, 0.0, 1.4, 0.1, 0.5]}), encoding="utf-8")
    rc, out, j = cli(xlsx, csv_, "--settings", tmp_path / "settings.json")
    assert rc == 0 and len(j["files"]) == 2 and all(f["settings"] for f in j["files"]), out[-800:]


def test_rails_07_extra_columns_are_allowed_and_reported_not_rejected():
    """우리 `fit_cycles` 산출은 열이 더 있다 (rmse·run_id·receipt) — 11 열 계약만 요구하고 나머지는 근거(4 층)로 적는다."""
    rows = [dict(r, rmse_pocv=0.001 + 1e-5 * i, run_id="r", gamma_Si=0.2) for i, r in enumerate(_table())]
    rep = R.run_all(rows)
    assert rep["ok"] is True
    ev = _by(rep["findings"], check="evidence")
    assert ev and "rmse_pocv" in ev[0]["data"]["present"], ev
