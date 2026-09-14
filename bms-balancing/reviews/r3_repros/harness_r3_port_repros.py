"""R3 benign numerical/validation probes. Target files remain unchanged."""
from __future__ import annotations

import argparse
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch


COLS = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]


def base(v):
    anchors = {key: 1.0 for key, _ in v.ANCHOR_STAGE}
    anchors["dv_n"] = 350.0
    P = [list(p) for p in v.DD_EVAL_P]
    py = {c: [0.0123456789012345 * (j + 1) + 0.001 * i for i in range(len(P))]
          for j, c in enumerate(COLS)}
    rows = [p + [py[c][i] for c in COLS] for i, p in enumerate(P)]
    return anchors, P, py, rows


def write_csv(path, anchors, rows):
    lines = [f"# {k},{x:.17g}" for k, x in anchors.items()]
    lines += ["a_PE,b_PE,a_NE,b_NE,gamma_Si," + ",".join(COLS)]
    lines += [",".join(format(x, ".17g") for x in row) for row in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def comparator_probes(v, tmp):
    results = {}
    cases = {"valid_control": "complete", "missing_rmse_row_control": "incomplete",
             "nan_rmse_control": "incomplete", "different_rmse_control": "model_mismatch",
             "missing_anchor": "complete", "nan_anchor": "complete", "nan_parameter": "complete",
             "all_short_g17_column": "complete"}
    for name, observed_status in cases.items():
        an, P, py, rows = base(v)
        man = dict(an)
        if name == "missing_rmse_row_control":
            rows.pop()
        elif name == "nan_rmse_control":
            rows[3][5] = float("nan")
        elif name == "different_rmse_control":
            rows[3][5] = 9.0
        elif name == "missing_anchor":
            del man["E_PE_0p5"]
        elif name == "nan_anchor":
            man["E_PE_0p5"] = float("nan")
        elif name == "nan_parameter":
            rows[3][0] = float("nan")
        elif name == "all_short_g17_column":
            # MATLAB .17g records an entire column of exact dyadic 0.125.
            # A Python implementation differs in one cell by exactly 1/1024.
            for row in rows:
                row[5] = 0.125
            py["rmse_pocv"] = [0.125] * len(P)
            py["rmse_pocv"][3] += 1.0 / 1024
        path = tmp / (name + ".csv")
        write_csv(path, man, rows)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            res = v._compare_dd_eval(an, P, py, path)
        assert res["status"] == observed_status, (name, res, out.getvalue())
        results[name] = {"result": res, "tolerances": v.printed_abs_tols(path),
                         "verdict": [x for x in out.getvalue().splitlines()
                                     if x.startswith("판정") or "E_PE_0p5" in x]}
        if name == "all_short_g17_column":
            results[name]["hidden_absolute_difference"] = 1.0 / 1024
            results[name]["hidden_relative_difference"] = (1.0 / 1024) / py["rmse_pocv"][3]
            assert v.printed_abs_tols(path)["rmse_pocv"] == 0.001
    return results


def worker(v, kind, out):
    import numpy as np
    an, P, py, rows = base(v)
    root = out.parent
    if kind == "compare":
        class Obj:
            def _at(self, p, col):
                idx = P.index(list(p))
                return py[col][idx]
            def rmse_pocv(self, p): return self._at(p, "rmse_pocv")
            def rmse_dvdq(self, p): return self._at(p, "rmse_dvdq")
            def rmse_dqdv(self, p, weighted=False):
                return self._at(p, "rmse_dqdv_w" if weighted else "rmse_dqdv")
        rows[3][5] = 9.0
        write_csv(out, an, rows)
        with patch.object(v.D, "data_root", return_value=root), \
             patch.object(v, "build", return_value=Obj()), \
             patch.object(v, "dd_eval_anchors", return_value=list(an.items())):
            return v.main(["eval", "--data-root", str(root), "--compare", str(out)])
    center = np.array([1.2, -0.25, 1.2, -0.15, 0.25])
    class Obj:
        c_cell = 1.0
        scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}
        def __call__(self, p):
            return float(1 + 1e-4 * np.square(np.asarray(p) - center).sum())
        def rmse_pocv(self, p): return self(p)
    def failed(fun, start, **kw):
        x = np.array([1.2, -0.25, 1.4, -0.15])
        return SimpleNamespace(x=x, fun=float(fun(x)), success=False, status=1,
                               message="ITERATIONS LIMIT")
    with patch.object(v.D, "data_root", return_value=root), \
         patch.object(v, "build", return_value=Obj()), \
         patch.object(v, "multistart", return_value=(center.copy(), 1.0, [])), \
         patch.object(v, "minimize", side_effect=failed):
        return v.main(["profile", "--data-root", str(root), "--starts", "1", "--grid", "2",
                       "--out", str(out)])


def cli_and_stale_profile(target, tmp):
    script = str(Path(__file__).resolve())
    command = [sys.executable, script, "--target", str(target)]
    comp = subprocess.run(command + ["--worker", "compare", "--out", str(tmp / "cli.csv")],
                          capture_output=True, text=True)
    assert comp.returncode == 0 and "앵커는 전부 맞는데 rmse 가 갈린다" in comp.stdout
    csvpath = tmp / "profile.csv"
    stale = "gamma_Si,obj,LAM_NE_pct,n_ok,n_tried\n0,1,42,1,1\n"
    csvpath.write_text(stale, encoding="utf-8")
    shell_text = (target / "scripts/run_states.sh").read_text(encoding="utf-8")
    helpers = shell_text[shell_text.index("say ()"):shell_text.index("\nfail=0")]
    shell = helpers + '\nrun "profile synthetic" "$1" - "$2" "$3" "$4" --target "$5" --worker profile --out "$1"\n'
    logpath = tmp / "profile.log"
    r = subprocess.run(["bash", "-c", shell, "r3-profile", str(csvpath), str(logpath),
                        sys.executable, script, str(target)], capture_output=True, text=True)
    log = logpath.read_text(encoding="utf-8")
    assert r.returncode == 0 and "OK" in r.stderr
    assert "모든 γ 가 실패" in log and csvpath.read_text(encoding="utf-8") == stale
    return {"comparison_cli": {"returncode": comp.returncode,
                               "verdict": [x for x in comp.stdout.splitlines() if x.startswith("판정")]},
            "stale_profile": {"run_states_helper_returncode": r.returncode,
                              "helper_output": r.stderr.strip(), "old_csv_unchanged": True,
                              "failure_log": [x for x in log.splitlines() if "실패" in x or x.startswith("SUMMARY")]}}


def actual_recompare(target, v):
    results = {}
    for path in sorted((target / "out/recompare").glob("*_r2.csv")):
        ma, mr, mh = v.read_dd_eval_csv(path)
        # The .txt starts with full-precision Python output before prose.
        pa, pr, ph = v.read_dd_eval_csv(path.with_suffix(".txt"))
        assert mh == ph and len(ma) == len(pa) == 16 and len(mr) == len(pr) == 8
        assert all(len(row) == 9 for row in mr + pr)
        ar = max(abs(ma[k] - pa[k]) / max(abs(pa[k]), 1e-30) for k in ma)
        rr = max(abs(mr[i][j] - pr[i][j]) / max(abs(pr[i][j]), 1e-30)
                 for i in range(8) for j in range(5, 9))
        assert all(mr[i][:5] == pr[i][:5] for i in range(8))
        assert max(ar, rr) < 1e-9
        results[path.name] = {"anchor_max_rel": ar, "rmse_max_rel": rr,
                              "count": 48, "scope": "independent arithmetic over supplied output pair, not MATLAB execution"}
    assert len(results) == 4
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=Path(__file__).resolve().parents[1]
                    / "work/harness-r3-target/bms-balancing")
    ap.add_argument("--worker", choices=["compare", "profile"])
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.target))
    from bms_balancing import verify
    if args.worker:
        return worker(verify, args.worker, args.out)
    with tempfile.TemporaryDirectory(prefix="harness-r3-port-") as td:
        tmp = Path(td)
        results = {"target": str(args.target), "comparator": comparator_probes(verify, tmp),
                   "public_path": cli_and_stale_profile(args.target, tmp),
                   "actual_recompare": actual_recompare(args.target, verify)}
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
