"""Final R6 d431404 numerical comparator review, with synthetic values only.

Data loading, objective values and anchors are doubles. CSV parsing, tolerance,
comparison and the public eval dispatcher are target production code. Every
case runs the helper and an independent eval subprocess. No target edits occur.
Optional C-format checks compare this Python runtime with local libc snprintf;
they are not a MATLAB execution.
"""
from __future__ import annotations

import argparse
import contextlib
import ctypes
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

COLS = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
PARAMS = ["a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si"]

# Each entry: producer decimal format, CSV value, Python value in row 3,
# observed target status, observed public command exit code.
CASES = {
    "exact_equal": (".17g", .125, .125, "complete", 0),
    "exact_mismatch": (".17g", .125, .1259765625, "model_mismatch", 1),
    "sig2_zero_r5_closed": (".2g", 0.0, .049, "model_mismatch", 1),
    "sig2_decade_r5_closed": (".2g", 10.0, 9.6, "model_mismatch", 1),
    "sig2_small_decade_r5_closed": (".2g", .0001, .000096, "model_mismatch", 1),
    "sig2_decade_valid": (".2g", 10.0, 9.96, "complete", 0),
    "sig0_r5_closed": (".0g", 1.0, 4.0, "model_mismatch", 1),
    "sig0_valid": (".0g", 1.0, 1.4, "complete", 0),
    "fixed10_inside": (".10f", .0123456789, .01234567894, "complete", 0),
    "fixed10_outside": (".10f", .0123456789, .01234567899, "model_mismatch", 1),
    "negative_zero_equal": (".2g", -0.0, -0.0, "complete", 0),
    "sig18_valid": (".18g", .12345678901234568, .12345678901234568, "complete", 0),
    "inferred": (".17g", .125, .125, "partial", 3),
    "inferred_allow_partial": (".17g", .125, .125, "partial", 3),
    "legacy_allow_partial": (".17g", .125, .125, "partial", 0),
    "duplicate_declaration_r5_closed": (".17g", .1, .149, "invalid", 2),
    "bad_anchor_r5_closed": (".17g", .125, .125, "invalid", 2),
    "bad_anchor_allow_partial_r5_closed": (".17g", .125, .125, "invalid", 2),
    "parameter_header_r5_closed": (".17g", .125, .125, "invalid", 2),
    "unknown_declaration": (".17g", .125, .125, "invalid", 2),
    "unknown_declaration_explicit_option": (".17g", .125, .125, "complete", 0),
    "loose_option_actual_difference": (".17g", .125, .126, "partial", 3),
    "loose_option_actual_equality": (".17g", .125, .125, "complete", 0),
    "loose_option_declared_noise": (".17g", .125, .125000000001, "partial", 3),
    "sig2_large_inside": (".2g", 1e308, 1.04e308, "complete", 0),
    "sig2_large_noise_overflow": (".2g", 1e308, 1.0500000001e308, "model_mismatch", 1),
    "sig2_scaled_noise_control": (".2g", 1.0, 1.0500000001, "complete", 0),
    "fixed0_large_noise_overflow": (".0f", 1e308, 1.000000000001e308, "model_mismatch", 1),
    "exact_large_noise_control": (".17g", 1e308, 1.000000000001e308, "complete", 0),
    "internal_v01_header_after_data": (".17g", .125, .125, "invalid", 2),
    "internal_v02_nondeclared_bad_option_tokens": (".17g", .123456789, .123456789, "invalid", 2),
    "internal_v02_nondeclared_valid_option_tokens": (".2g", .12, .123, "complete", 0),
    "internal_v03_missing_header": (".17g", .125, .125, "invalid", 2),
    "internal_v04_zero_metrics": (".17g", .125, .125, "invalid", 2),
    "internal_v06_numeric_declaration": (".17g", .125, .125, "invalid", 2),
    "internal_v07_missing_compare_file": (".17g", .125, .125, "invalid", 2),
}


def stable_reference_excess(v, spec, mv, pv):
    """Same formatter-defined connected interval, overflow-safe midpoint.

    Used only on same-sign close finite positive fixtures. Thus hi-lo is finite.
    This is a numerical control, not a proposed complete production patch.
    """
    fmt = v.token_format(spec)
    if fmt is None:
        return abs(mv-pv)
    token = format(mv, fmt)
    if format(pv, fmt) == token:
        return 0.0
    lo, hi = mv, pv
    for _ in range(400):
        mid = lo + (hi-lo) / 2.0
        if mid == lo or mid == hi:
            break
        if format(mid, fmt) == token:
            lo = mid
        else:
            hi = mid
    return abs(pv-hi)


def scenario(v, name):
    fmt, mv, pv, _, _ = CASES[name]
    anchors = {key: 1.0 for key, _ in v.ANCHOR_STAGE}
    anchors["dv_n"] = 350.0
    P = [list(p) for p in v.DD_EVAL_P]
    vals = {col: [mv] * len(P) for col in COLS}
    vals[COLS[0]][3] = pv
    rows = [p + [mv] * len(COLS) for p in P]
    params, cols = list(PARAMS), list(COLS)
    declaration, extra, flags, missing = "%" + fmt, [], [], []
    if name.startswith("inferred"):
        declaration = None
        if "allow_partial" in name:
            flags = ["--allow-partial"]
    elif name == "legacy_allow_partial":
        rows, cols = [row[:7] for row in rows], cols[:2]
        flags = ["--allow-partial"]
    elif name == "duplicate_declaration_r5_closed":
        extra = ["# printed_format,%.1f"]
    elif name.startswith("bad_anchor"):
        extra = ["# E_PE_0p5,broken"]
        if "allow_partial" in name:
            missing = ["E_PE_0p5"]
            flags = ["--allow-partial"]
    elif name == "parameter_header_r5_closed":
        params[1], params[3] = params[3], params[1]
    elif name.startswith("unknown_declaration"):
        declaration = "unsupported-format"
        if "explicit_option" in name:
            flags = ["--precision", "g17"]
    elif name.startswith("loose_option"):
        flags = ["--precision", "fixed:1"]
    elif name.startswith("internal_v02"):
        declaration = None
        flags = ["--precision", "sig:2"]
    elif name == "internal_v04_zero_metrics":
        cols, rows, flags = [], [row[:5] for row in rows], ["--allow-partial"]
    elif name == "internal_v06_numeric_declaration":
        declaration = "17"
    spec = v.parse_precision_spec("%" + fmt)
    reference = stable_reference_excess(v, spec, mv, pv)
    notes = dict(matlab_token=format(mv, fmt), python_value=pv,
                 python_formatted=format(pv, fmt), raw_relative=abs(mv-pv)/max(abs(pv), 1e-30),
                 target_excess=v.token_excess(spec, mv, pv), reference_excess=reference,
                 reference_relative=reference/max(abs(pv), 1e-30))
    return dict(name=name, anchors=anchors, P=P, vals=vals, rows=rows, params=params, cols=cols, fmt=fmt,
                declaration=declaration, extra=extra, flags=flags, missing=missing, notes=notes)


def write_case(path, s):
    lines = [] if s["declaration"] is None else [f'# printed_format,{s["declaration"]}']
    lines += s["extra"]
    lines += [f"# {key},{value:.17g}" for key, value in s["anchors"].items() if key not in s["missing"]]
    lines += [",".join(s["params"] + s["cols"])]
    lines += [",".join([format(x, ".6f") for x in row[:5]]
                       + [format(x, s["fmt"]) for x in row[5:]]) for row in s["rows"]]
    if s["name"] in ("internal_v01_header_after_data", "internal_v03_missing_header"):
        header = next(line for line in lines if line.startswith("a_PE,"))
        lines.remove(header)
        if s["name"] == "internal_v01_header_after_data":
            lines.append(header)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if s["name"] == "internal_v07_missing_compare_file":
        path.unlink()  # Only this just-created disposable fixture is removed.


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


def libc_format_checks():
    libc = ctypes.CDLL(None)
    printf = libc.snprintf
    printf.restype = ctypes.c_int
    values = [0.0, -0.0, .125, -.125, 1.25, -1.25, 2.5, -2.5, 9.95, 9.96, 10.0]
    for exponent in [-300, -5, -4, -3, 0, 1, 2, 15, 16, 300]:
        x = 10.0 ** exponent
        values += [math.nextafter(x, 0.0), x, math.nextafter(x, math.inf)]
    formats = [f".{n}g" for n in (0, 1, 2, 3, 10, 15, 16, 17, 18)] + [f".{n}f" for n in (0, 1, 2, 10)]
    mismatches = []
    for fmt in formats:
        for x in values:
            buf = ctypes.create_string_buffer(4096)
            n = printf(buf, len(buf), ("%" + fmt).encode("ascii"), ctypes.c_double(x))
            assert 0 <= n < len(buf), (fmt, x, n)
            actual, python_text = buf.value.decode("ascii"), format(x, fmt)
            if actual != python_text:
                mismatches.append(dict(format=fmt, value=x, c=actual, python=python_text))
    return dict(runtime=sys.version, scope="local libc snprintf, NOT MATLAB",
                comparisons=len(values)*len(formats), mismatches=mismatches)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=Path(__file__).resolve().parents[1] / "work/harness-r6-d431404/bms-balancing")
    ap.add_argument("--case", choices=list(CASES))
    ap.add_argument("--worker", choices=list(CASES))
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--libc-formats", action="store_true")
    args = ap.parse_args()
    if args.libc_formats:
        print(json.dumps(libc_format_checks(), ensure_ascii=False, indent=2))
        return 0
    sys.path.insert(0, str(args.target))
    from bms_balancing import verify as v
    if args.worker:
        return worker(v, args.worker, args.csv)
    results = {}
    with tempfile.TemporaryDirectory(prefix="harness-r6-port-") as td:
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
            expected_status, expected_rc = CASES[name][-2:]
            assert result["status"] == expected_status, (name, result, capture.getvalue())
            assert run.returncode == expected_rc, (name, run.returncode, run.stdout, run.stderr)
            if "overflow" in name:
                assert math.isinf(s["notes"]["target_excess"]), (name, s["notes"])
                assert 0 < s["notes"]["reference_relative"] <= v.MODEL_REL, (name, s["notes"])
            results[name] = dict(helper_result=result, process_exit_code=run.returncode, notes=s["notes"],
                                 options=s["flags"], verdict=[line for line in run.stdout.splitlines()
                                     if line.startswith("판정") or line.startswith("종료 코드")])
    print(json.dumps(dict(target=str(args.target), cases=results), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

