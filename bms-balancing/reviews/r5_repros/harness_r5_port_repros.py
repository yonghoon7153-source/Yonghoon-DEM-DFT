"""R5 numerical comparator review: synthetic finite values, no private data.

Each selected case calls both the comparator helper and the real eval dispatcher
in a subprocess. Data loading, Objective values and anchors are explicit doubles;
CSV parsing, precision policy, comparison and process exit handling are production.
The checkout is read-only; fixtures live in a temporary directory.
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
PARAMS = ["a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si"]
CASES = {
    "exact_equal_control": ("complete", 0),
    "exact_mismatch_control": ("model_mismatch", 1),
    "inferred_control": ("partial", 3),
    "inferred_allow_partial_control": ("partial", 3),
    "unknown_declaration_control": ("invalid", 2),
    "g14_mismatch_control": ("model_mismatch", 1),
    "fixed10_inside_control": ("complete", 0),
    "fixed10_outside_control": ("model_mismatch", 1),
    "duplicate_metric_nan_control": ("invalid", 2),
    "duplicate_anchor_nan_control": ("invalid", 2),
    "nonnumeric_metric_control": ("invalid", 2),
    "schema_partial_control": ("partial", 3),
    "schema_allow_partial_control": ("partial", 0),
    "loose_override_control": ("partial", 3),
    "loose_override_allow_partial_control": ("partial", 3),
    "stricter_override_control": ("complete", 0),
    "sig2_nonboundary_inside_control": ("complete", 0),
    "sig2_nonboundary_outside_control": ("model_mismatch", 1),
    "sig2_zero_false_complete": ("complete", 0),
    "sig2_decade_false_complete": ("complete", 0),
    "sig2_small_decade_false_complete": ("complete", 0),
    "sig2_decade_valid_rounding_control": ("complete", 0),
    "sig0_false_complete": ("complete", 0),
    "duplicate_anchor_text_false_complete": ("complete", 0),
    "nonnumeric_anchor_allowed_as_legacy": ("partial", 0),
    "duplicate_declaration_strict_control": ("model_mismatch", 1),
    "duplicate_declaration_false_complete": ("complete", 0),
    "duplicate_declaration_invalid_then_valid": ("complete", 0),
    "parameter_header_swap_false_complete": ("complete", 0),
    "unknown_declaration_explicit_option": ("complete", 0),
}


def scenario(v, name):
    anchors = {key: 1.0 for key, _ in v.ANCHOR_STAGE}
    anchors["dv_n"] = 350.0
    P = [list(p) for p in v.DD_EVAL_P]
    vals = {c: [0.125] * len(P) for c in COLS}
    rows = [p + [vals[c][i] for c in COLS] for i, p in enumerate(P)]
    cols, params = list(COLS), list(PARAMS)
    fmt, declaration = ".17g", "%.17g"
    before, after, flags, notes = [], [], [], {}
    if name == "exact_mismatch_control":
        vals[COLS[0]][3] += 1 / 1024
    elif name.startswith("inferred"):
        declaration = None
        if "allow_partial" in name:
            flags = ["--allow-partial"]
    elif name.startswith("unknown_declaration"):
        declaration = "unsupported-format"
        if "explicit_option" in name:
            flags = ["--precision", "g17"]
    elif name == "g14_mismatch_control":
        fmt, declaration = ".14g", "%.14g"
        vals[COLS[0]][3] += 1 / 1024
    elif name.startswith("fixed10"):
        fmt, declaration = ".10f", "%.10f"
        for c in COLS:
            vals[c] = [.0123456789] * len(P)
        rows = [p + [vals[c][i] for c in COLS] for i, p in enumerate(P)]
        vals[COLS[0]][3] = .01234567894 if "inside" in name else .01234567899
    elif name == "duplicate_metric_nan_control":
        cols.append(COLS[0])
        for row in rows:
            row.append(float("nan"))
    elif name == "duplicate_anchor_nan_control":
        before = ["# E_PE_0p5,nan"]
    elif name == "nonnumeric_metric_control":
        rows[3][5] = "broken"
    elif name.startswith("schema_"):
        cols, rows = cols[:2], [row[:7] for row in rows]
        if "allow_partial" in name:
            flags = ["--allow-partial"]
    elif name.startswith("loose_override"):
        flags = ["--precision", "fixed:1"]
        if "allow_partial" in name:
            flags += ["--allow-partial"]
    elif name == "stricter_override_control":
        fmt, declaration = ".1f", "%.1f"
        for c in COLS:
            vals[c] = [.1] * len(P)
        rows = [p + [vals[c][i] for c in COLS] for i, p in enumerate(P)]
        flags = ["--precision", "g17"]
    elif name.startswith("sig"):
        examples = {
            "sig2_nonboundary_inside_control": (1.2, 1.24, 2),
            "sig2_nonboundary_outside_control": (1.2, 1.26, 2),
            "sig2_zero_false_complete": (0.0, .049, 2),
            "sig2_decade_false_complete": (10.0, 9.6, 2),
            "sig2_small_decade_false_complete": (.0001, .000096, 2),
            "sig2_decade_valid_rounding_control": (10.0, 9.96, 2),
            "sig0_false_complete": (1.0, 4.0, 0),
        }
        mv, pv, digits = examples[name]
        fmt, declaration = f".{digits}g", f"%.{digits}g"
        for c in COLS:
            vals[c] = [mv] * len(P)
        rows = [p + [vals[c][i] for c in COLS] for i, p in enumerate(P)]
        vals[COLS[0]][3] = pv
        spec = v.parse_precision_spec(declaration)
        notes = dict(matlab_token=format(mv, fmt), python_value=pv,
                     python_formatted=format(pv, fmt), applied_tolerance=v.cell_tol(spec, mv),
                     abs_difference=abs(mv-pv), relative_difference=abs(mv-pv)/max(abs(pv), 1e-30))
    elif name == "duplicate_anchor_text_false_complete":
        before = ["# E_PE_0p5,broken"]
    elif name == "nonnumeric_anchor_allowed_as_legacy":
        before = ["# E_PE_0p5,broken"]
        flags = ["--allow-partial"]
    elif name in ("duplicate_declaration_false_complete", "duplicate_declaration_strict_control"):
        if name == "duplicate_declaration_false_complete":
            after = ["# printed_format,%.1f"]
        for c in COLS:
            vals[c] = [.1] * len(P)
        rows = [p + [vals[c][i] for c in COLS] for i, p in enumerate(P)]
        vals[COLS[0]][3] = .149
        notes = dict(matlab_value=.1, python_value=.149,
                     abs_difference=.049, relative_difference=.049/.149)
    elif name == "duplicate_declaration_invalid_then_valid":
        before = ["# printed_format,unsupported-format"]
    elif name == "parameter_header_swap_false_complete":
        params[1], params[3] = params[3], params[1]
        notes = dict(expected_named_p=dict(zip(PARAMS, P[0])),
                     csv_named_p=dict(zip(params, P[0])))
    return dict(anchors=anchors, P=P, vals=vals, rows=rows, cols=cols, params=params,
                fmt=fmt, declaration=declaration, before=before, after=after, flags=flags, notes=notes)


def write_case(path, s):
    lines = list(s["before"])
    if s["declaration"] is not None:
        lines.append(f'# printed_format,{s["declaration"]}')
    lines += s["after"]
    broken_only = "# E_PE_0p5,broken" in s["before"] and "--allow-partial" in s["flags"]
    lines += [f"# {k},{x:.17g}" for k, x in s["anchors"].items()
              if not (broken_only and k == "E_PE_0p5")]
    lines += [",".join(s["params"] + s["cols"])]
    for row in s["rows"]:
        lines.append(",".join([format(x, ".6f") for x in row[:5]]
                    + [x if isinstance(x, str) else format(x, s["fmt"]) for x in row[5:]]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def worker(v, name, path):
    s = scenario(v, name)
    write_case(path, s)
    class Obj:
        def at(self, p, col): return s["vals"][col][s["P"].index([float(x) for x in p])]
        def rmse_pocv(self, p): return self.at(p, COLS[0])
        def rmse_dvdq(self, p): return self.at(p, COLS[1])
        def rmse_dqdv(self, p, weighted=False): return self.at(p, COLS[3] if weighted else COLS[2])
    with patch.object(v.D, "data_root", return_value=path.parent), \
         patch.object(v, "build", return_value=Obj()), \
         patch.object(v, "dd_eval_anchors", return_value=list(s["anchors"].items())):
        return v.main(["eval", "--compare", str(path)] + s["flags"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=Path(__file__).resolve().parents[1]
                    / "work/harness-r5-target/bms-balancing")
    ap.add_argument("--case", choices=list(CASES))
    ap.add_argument("--worker", choices=list(CASES))
    ap.add_argument("--csv", type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.target))
    from bms_balancing import verify as v
    if args.worker:
        return worker(v, args.worker, args.csv)
    results = {}
    with tempfile.TemporaryDirectory(prefix="harness-r5-port-") as td:
        for name in ([args.case] if args.case else CASES):
            s = scenario(v, name)
            path = Path(td) / (name + ".csv")
            write_case(path, s)
            capture = io.StringIO()
            precision = s["flags"][1] if s["flags"][:1] == ["--precision"] else None
            with contextlib.redirect_stdout(capture):
                result = v._compare_dd_eval(s["anchors"], s["P"], s["vals"], path, precision)
            run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--target", str(args.target),
                                  "--worker", name, "--csv", str(path)], capture_output=True, text=True)
            wanted_status, wanted_rc = CASES[name]
            assert result["status"] == wanted_status, (name, result, capture.getvalue())
            assert run.returncode == wanted_rc, (name, run.returncode, run.stdout, run.stderr)
            if "false_complete" in name and name.startswith("sig"):
                assert s["notes"]["matlab_token"] != s["notes"]["python_formatted"]
            results[name] = dict(helper_result=result, process_exit_code=run.returncode,
                                 notes=s["notes"], options=s["flags"],
                                 verdict=[line for line in run.stdout.splitlines()
                                          if line.startswith("판정") or line.startswith("종료 코드")])
    print(json.dumps({"target": str(args.target), "cases": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
