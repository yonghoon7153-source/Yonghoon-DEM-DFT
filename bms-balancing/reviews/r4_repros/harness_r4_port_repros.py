"""R4 comparison/schema/precision review using synthetic numeric CSVs only.

No private battery data or MATLAB is needed. The target checkout is read-only.
Each CLI case invokes the actual verify.main dispatcher in a subprocess with
data loading and numerical objective values replaced by explicit test doubles.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

COLS = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
CASES = {
    "valid_declared_control": ("complete", 0),
    "nan_anchor_control": ("incomplete", 2),
    "nan_parameter_control": ("incomplete", 2),
    "missing_anchor_control": ("partial", 3),
    "declared_g17_mismatch_control": ("model_mismatch", 1),
    "requested_g17_mismatch_control": ("model_mismatch", 1),
    "inferred_precision_false_complete": ("complete", 0),
    "declared_g14_false_complete": ("complete", 0),
    "unrecognized_declaration_false_complete": ("complete", 0),
    "fixed1_roundtrip_compatible_control": ("complete", 0),
    "fixed1_roundtrip_incompatible": ("complete", 0),
    "fixed10_roundtrip_compatible_control": ("complete", 0),
    "fixed10_roundtrip_incompatible": ("complete", 0),
    "duplicate_metric_nan": ("complete", 0),
    "duplicate_anchor_nan": ("complete", 0),
    "partial_two_columns_control": ("partial", 3),
    "allowed_partial_control": ("partial", 0),
    "allowed_partial_does_not_hide_nan_control": ("incomplete", 2),
    "explicit_option_overrides_declaration": ("complete", 0),
    "invalid_option_control": ("ValueError", 2),
}


def scenario(v, name):
    anchors = {key: 1.0 for key, _ in v.ANCHOR_STAGE}
    anchors["dv_n"] = 350.0
    P = [list(p) for p in v.DD_EVAL_P]
    values = {c: [0.0123456789012345 * (j + 1) + .001 * i for i in range(len(P))]
              for j, c in enumerate(COLS)}
    m_anchors = dict(anchors)
    columns = list(COLS)
    rows = [p + [values[c][i] for c in COLS] for i, p in enumerate(P)]
    declaration = "%.17g"
    numeric_format = ".17g"
    extra_lines, cli_args, notes = [], [], {}
    if name == "nan_anchor_control":
        m_anchors["E_PE_0p5"] = float("nan")
    elif name == "nan_parameter_control":
        rows[3][0] = float("nan")
    elif name == "missing_anchor_control":
        del m_anchors["E_PE_0p5"]
    elif name in ("declared_g17_mismatch_control", "requested_g17_mismatch_control",
                  "inferred_precision_false_complete", "declared_g14_false_complete",
                  "unrecognized_declaration_false_complete", "explicit_option_overrides_declaration"):
        for row in rows:
            row[5] = .125
        values["rmse_pocv"] = [.125] * len(P)
        values["rmse_pocv"][3] += 1 / 1024
        notes.update(matlab_value=.125, python_value=values["rmse_pocv"][3],
                     absolute_difference=1 / 1024,
                     relative_difference=(1 / 1024) / values["rmse_pocv"][3])
        if name in ("requested_g17_mismatch_control", "inferred_precision_false_complete"):
            declaration = None
        if name == "requested_g17_mismatch_control":
            cli_args = ["--precision", "g17"]
        elif name == "declared_g14_false_complete":
            declaration, numeric_format = "%.14g", ".14g"
            notes["python_value_formatted_as_declared"] = format(values["rmse_pocv"][3], ".14g")
        elif name == "unrecognized_declaration_false_complete":
            declaration = "unsupported-format"
        elif name == "explicit_option_overrides_declaration":
            cli_args = ["--precision", "fixed:1"]
    elif name.startswith("fixed1"):
        decimals = 10 if name.startswith("fixed10") else 1
        declaration, numeric_format = f"%.{decimals}f", f".{decimals}f"
        values = {c: [(j + 1) / 10] * len(P) for j, c in enumerate(COLS)}
        if decimals == 10:
            values["rmse_pocv"] = [.0123456789] * len(P)
        rows = [p + [values[c][i] for c in COLS] for i, p in enumerate(P)]
        if decimals == 10:
            values["rmse_pocv"][3] = .01234567894 if "compatible_control" in name else .01234567899
        else:
            values["rmse_pocv"][3] = .149 if "compatible_control" in name else .199
        notes.update(matlab_printed_value=format(rows[3][5], numeric_format), python_value=values["rmse_pocv"][3],
                     python_value_formatted_as_declared=format(values["rmse_pocv"][3], numeric_format),
                     half_rounding_unit=.5 * 10 ** -decimals,
                     absolute_difference=abs(values["rmse_pocv"][3] - rows[3][5]),
                     relative_difference=abs(values["rmse_pocv"][3] - rows[3][5]) / values["rmse_pocv"][3])
    elif name == "duplicate_metric_nan":
        columns.append("rmse_pocv")
        for row in rows:
            row.append(float("nan"))
    elif name == "duplicate_anchor_nan":
        extra_lines = ["# E_PE_0p5,nan"]
    elif name in ("partial_two_columns_control", "allowed_partial_control",
                  "allowed_partial_does_not_hide_nan_control"):
        columns, rows = columns[:2], [r[:7] for r in rows]
        if name != "partial_two_columns_control":
            cli_args = ["--allow-partial"]
        if name == "allowed_partial_does_not_hide_nan_control":
            rows[3][5] = float("nan")
    elif name == "invalid_option_control":
        cli_args = ["--precision", "bogus"]
    return dict(anchors=anchors, P=P, values=values, m_anchors=m_anchors, columns=columns,
                rows=rows, declaration=declaration, numeric_format=numeric_format,
                extra_lines=extra_lines, cli_args=cli_args, notes=notes)


def write_scenario(path, s):
    head = [] if s["declaration"] is None else [f'# printed_format,{s["declaration"]}']
    head += s["extra_lines"]
    head += [f"# {k},{x:.17g}" for k, x in s["m_anchors"].items()]
    head.append("a_PE,b_PE,a_NE,b_NE,gamma_Si," + ",".join(s["columns"]))
    for row in s["rows"]:
        head.append(",".join([format(x, ".6f") for x in row[:5]]
                             + [format(x, s["numeric_format"]) for x in row[5:]]))
    path.write_text("\n".join(head) + "\n", encoding="utf-8")


def cli_worker(v, name, path):
    s = scenario(v, name)
    write_scenario(path, s)
    class Obj:
        def at(self, p, col): return s["values"][col][s["P"].index([float(x) for x in p])]
        def rmse_pocv(self, p): return self.at(p, "rmse_pocv")
        def rmse_dvdq(self, p): return self.at(p, "rmse_dvdq")
        def rmse_dqdv(self, p, weighted=False):
            return self.at(p, "rmse_dqdv_w" if weighted else "rmse_dqdv")
    with patch.object(v.D, "data_root", return_value=path.parent), \
         patch.object(v, "build", return_value=Obj()), \
         patch.object(v, "dd_eval_anchors", return_value=list(s["anchors"].items())):
        return v.main(["eval", "--compare", str(path)] + s["cli_args"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=Path(__file__).resolve().parents[1]
                    / "work/harness-r4-target/bms-balancing")
    ap.add_argument("--worker", choices=list(CASES))
    ap.add_argument("--csv", type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.target))
    from bms_balancing import verify as v
    if args.worker:
        return cli_worker(v, args.worker, args.csv)
    results = {}
    with tempfile.TemporaryDirectory(prefix="harness-r4-port-") as td:
        tmp = Path(td)
        for name, (wanted_status, wanted_rc) in CASES.items():
            s = scenario(v, name)
            path = tmp / (name + ".csv")
            write_scenario(path, s)
            precision = s["cli_args"][1] if s["cli_args"][:1] == ["--precision"] else None
            captured = io.StringIO()
            try:
                with contextlib.redirect_stdout(captured):
                    result = v._compare_dd_eval(s["anchors"], s["P"], s["values"], path, precision)
            except ValueError as exc:
                result = dict(status="ValueError", message=str(exc))
            assert result["status"] == wanted_status, (name, result, captured.getvalue())
            run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--target", str(args.target),
                                  "--worker", name, "--csv", str(path)], capture_output=True, text=True)
            assert run.returncode == wanted_rc, (name, run.returncode, run.stdout, run.stderr)
            if name.endswith("roundtrip_incompatible"):
                assert s["notes"]["python_value_formatted_as_declared"] != s["notes"]["matlab_printed_value"]
            results[name] = dict(helper_result=result, process_exit_code=run.returncode,
                                 notes=s["notes"], declaration=s["declaration"], options=s["cli_args"],
                                 verdict=[x for x in run.stdout.splitlines()
                                          if x.startswith("판정") or x.startswith("종료 코드") or "추정" in x])
    print(json.dumps({"target": str(args.target), "cases": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
