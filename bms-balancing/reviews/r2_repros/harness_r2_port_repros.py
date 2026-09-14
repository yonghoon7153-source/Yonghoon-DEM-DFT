"""Benign numerical review probes against the immutable R2 checkout.

Run with a Python environment containing numpy, scipy, pandas and openpyxl.
No original/private MATLAB files or battery data are needed. The target is read
only; malformed comparison inputs and profile output live in a temporary dir.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch


def comparator_probes(v, tmp):
    anchors = {key: 1.0 for key, _ in v.ANCHOR_STAGE}
    anchors["dv_n"] = 350.0
    columns = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
    parameters = [list(p) for p in v.DD_EVAL_P]
    py = {col: [0.0123456789012345 * (j + 1) + 0.001 * i
                for i in range(len(parameters))]
          for j, col in enumerate(columns)}
    original = [p + [py[col][i] for col in columns]
                for i, p in enumerate(parameters)]
    scenarios = {}
    for kind in ("valid_control", "missing_last_row", "wrong_parameter_row", "nan_rmse_row",
                 "short_g17_token_masks_rmse_change"):
        rows = [r.copy() for r in original]
        current_py = {key: values.copy() for key, values in py.items()}
        if kind == "missing_last_row":
            rows.pop()
        elif kind == "wrong_parameter_row":
            rows[3][0] += 0.05
            rows[3][5:] = [9.0] * 4
        elif kind == "nan_rmse_row":
            rows[3][5:] = [float("nan")] * 4
        elif kind == "short_g17_token_masks_rmse_change":
            # The actual writer uses .17g. Exact 1.5 remains "1.5", which does
            # not make other columns uncertain to 0.1 in this full-precision file.
            rows[0][7] = current_py["rmse_dqdv"][0] = 1.5
            rows[3][5] += 0.025
        path = tmp / f"{kind}.csv"
        lines = [f"# {key},{value:.17g}" for key, value in anchors.items()]
        lines.append("a_PE,b_PE,a_NE,b_NE,gamma_Si," + ",".join(columns))
        lines.extend(",".join(f"{x:.17g}" for x in row) for row in rows)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = v._compare_dd_eval(anchors, parameters, current_py, path)
        output = buf.getvalue()
        scenarios[kind] = {
            "returned": result,
            "inferred_absolute_tolerance": v.printed_abs_tol(path),
            "incorrect_all_match": "전부 일치" in output and kind != "valid_control",
            "warning_and_verdict": [line for line in output.splitlines()
                                    if "행 수가 다르다" in line or "격자가 어긋났다" in line
                                    or line.startswith("판정:") or "nan" in line],
        }
    assert not scenarios["valid_control"]["incorrect_all_match"]
    assert all(scenarios[k]["incorrect_all_match"] for k in scenarios if k != "valid_control")
    return scenarios


def profile_failed_result_probe(v, tmp):
    import numpy as np

    center = np.array([1.2, -0.25, 1.2, -0.15, 0.25])

    class SyntheticObjective:
        c_cell = 1.0
        scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}

        def __call__(self, p):
            return float(1.0 + 1e-4 * np.square(np.asarray(p) - center).sum())

        def rmse_pocv(self, p):
            return float(self(p))

    obj = SyntheticObjective()
    failed = []

    def nonconverged(fun, start, **kwargs):
        x = np.array([1.2, -0.25, 1.4, -0.15])
        value = float(fun(x))
        failed.append(value)
        return SimpleNamespace(x=x, fun=value, success=False, status=1,
                               message="STOP: TOTAL NO. of ITERATIONS REACHED LIMIT")

    args = SimpleNamespace(data_root=str(tmp), source="GITT", state="200", si_source="Li",
                           w_dqdv=0.0, seed=0, starts=1, grid=2, tol=0.01,
                           profile_scale="global", out=str(tmp / "failed_profile.csv"))
    output = io.StringIO()
    with patch.object(v.D, "data_root", return_value=tmp), \
         patch.object(v, "build", return_value=obj), \
         patch.object(v, "multistart", return_value=(center.copy(), 1.0, [])), \
         patch.object(v, "minimize", side_effect=nonconverged), \
         contextlib.redirect_stdout(output):
        v.cmd_profile(args)
    with Path(args.out).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    result = {"all_profile_optimizer_calls_failed": len(failed), "emitted_fit_rows": len(rows),
              "rows": [{k: row[k] for k in ("gamma_Si", "obj_ratio_to_best", "LAM_NE_pct")}
                       for row in rows],
              "output_records_optimizer_failure": "success" in output.getvalue()
                                                     or "not_success" in output.getvalue()}
    assert len(failed) == 4 and len(rows) == 2
    assert all(float(row["obj_ratio_to_best"]) <= 1.01 for row in rows)
    assert all(abs(float(row["LAM_NE_pct"]) + 100 / 6) < 1e-9 for row in rows)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=Path(__file__).resolve().parents[1]
                    / "work/harness-r2-target/bms-balancing")
    args = ap.parse_args()
    sys.path.insert(0, str(args.target))
    from bms_balancing import verify
    with tempfile.TemporaryDirectory(prefix="harness-r2-port-") as td:
        tmp = Path(td)
        results = {"target": str(args.target), "comparison": comparator_probes(verify, tmp),
                   "failed_profile": profile_failed_result_probe(verify, tmp)}
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
