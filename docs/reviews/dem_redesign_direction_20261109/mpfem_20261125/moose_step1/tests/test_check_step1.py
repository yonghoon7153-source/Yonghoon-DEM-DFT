#!/usr/bin/env python3
"""Tests for ../check_step1.py (written before the checker).  Standard library only.

Each test builds case folders (out.csv, rc.txt, run.log, disk.mesh.json) from synthetic
rows that satisfy the step-1 identities, breaks one thing, runs the checker as a
subprocess and looks at its exit code and JSON.

    python3 test_check_step1.py          # prints one line per test and the counts
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import synthetic as syn  # noqa: E402

CHECKER = os.path.join(os.path.dirname(HERE), "check_step1.py")


def make_case(root, name, tag="m13", rows=None, rc="0", log="Solve Converged!\n",
              columns=None, mesh_over=None):
    d = os.path.join(root, name)
    os.makedirs(d)
    rows = syn.make_rows(tag=tag) if rows is None else rows
    syn.write_csv(os.path.join(d, "out.csv"), rows, columns)
    if rc is not None:
        with open(os.path.join(d, "rc.txt"), "w") as f:
            f.write(rc + "\n")
    if log is not None:
        with open(os.path.join(d, "run.log"), "w") as f:
            f.write(log)
    syn.mesh_json(os.path.join(d, "disk.mesh.json"), tag=tag, **(mesh_over or {}))
    return d


def run(args):
    p = subprocess.run([sys.executable, CHECKER] + args, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def full(root, m13, m26, extra=()):
    out = os.path.join(root, "check.json")
    rc, text = run(["full", "--case", "m13=" + m13, "--case", "m26=" + m26, "--out", out]
                   + list(extra))
    data = None
    if os.path.exists(out):
        with open(out, encoding="utf-8") as f:
            data = json.load(f)
    return rc, text, data


def check(data, case, key):
    return data["cases"][case]["checks"][key]


def big_rows(rows):
    fmax = max(abs(r["F_bot_y"]) for r in rows)
    return [r for r in rows if r["time"] > 0 and abs(r["F_bot_y"]) >= 1e-2 * fmax]


# ---------------------------------------------------------------- tests
def t_pass_basic(root):
    rc, text, data = full(root, make_case(root, "a", "m13"), make_case(root, "b", "m26"))
    assert rc == 0, text
    assert data["all_pass"] is True
    assert data["label"] == "DEVELOPMENT_ONLY"
    for case in ("m13", "m26"):
        for key in ("C_all_converged", "C_reached_end", "P1", "P2", "P4"):
            assert check(data, case, key)["pass"] is True, (case, key)
    assert data["cases"]["m13"]["checks"]["C_all_converged"]["steps"] == 407
    reg = data["registered"]["tol"]
    assert reg == {"P1": 1e-3, "P2_syy": 1e-2, "P2_sxx": 1e-2, "P4": 1e-3,
                   "big_row_fraction": 1e-2, "C_end_rel": 1e-9}, reg


def t_p1_fail(root):
    rows = syn.make_rows()
    r = big_rows(rows)[10]
    r["F_top_y"] *= 1.0011
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 1, text
    p1 = check(data, "m13", "P1")
    assert p1["pass"] is False and 1.0e-3 < p1["value"] < 1.2e-3, p1
    assert p1["worst_time"] == r["time"]
    assert data["all_pass"] is False


def t_p1_just_below(root):
    rows = syn.make_rows()
    big_rows(rows)[10]["F_top_y"] *= 1 + 0.99e-3
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 0, text
    assert check(data, "m13", "P1")["pass"] is True


def t_p2_syy_fail(root):
    rows = syn.make_rows()
    big_rows(rows)[50]["int_syy"] *= 1.011
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 1, text
    p2 = check(data, "m13", "P2")
    assert p2["pass"] is False and 1.0e-2 < p2["syy_value"] < 1.2e-2, p2


def t_p2_sxx_fail(root):
    rows26 = syn.make_rows(tag="m26")
    r = big_rows(rows26)[50]
    r["int_sxx"] = 0.011 * r["int_syy"]
    rc, text, data = full(root, make_case(root, "c"), make_case(root, "d", "m26", rows=rows26))
    assert rc == 1, text
    p2 = check(data, "m26", "P2")
    assert p2["pass"] is False and abs(p2["sxx_value"] - 0.011) < 1e-9, p2
    assert check(data, "m13", "P2")["pass"] is True


def t_p4_fail(root):
    rows = syn.make_rows()
    r = big_rows(rows)[100]
    s = 1 + 1.1e-3
    for c in ("area", "int_sxx", "int_syy", "int_szz", "int_sxy"):
        r[c] *= s          # mean stresses unchanged, area ratio moves by 1.1e-3
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 1, text
    p4 = check(data, "m13", "P4")
    assert p4["pass"] is False and 1.0e-3 < p4["value"] < 1.2e-3, p4
    assert check(data, "m13", "P2")["pass"] is True     # P2 uses F h / A: 0.11 % shift only


def t_c_rc_fail(root):
    rc, text, data = full(root, make_case(root, "a", rc="1"), make_case(root, "b", "m26"))
    assert rc == 1, text
    c = check(data, "m13", "C_all_converged")
    assert c["pass"] is False and any("rc" in x for x in c["reasons"]), c


def t_c_rc_missing(root):
    rc, text, data = full(root, make_case(root, "a", rc=None), make_case(root, "b", "m26"))
    assert rc == 1, text
    assert check(data, "m13", "C_all_converged")["pass"] is False


def t_c_gap_fail(root):
    rows = syn.make_rows()
    del rows[200]
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 1, text
    c = check(data, "m13", "C_all_converged")
    assert c["pass"] is False and any("contiguous" in x for x in c["reasons"]), c


def t_c_log_fail(root):
    log = "Solve Converged!\n Solve Did NOT Converge!\nAborting as solve did not converge\n"
    rc, text, data = full(root, make_case(root, "a", log=log), make_case(root, "b", "m26"))
    assert rc == 1, text
    c = check(data, "m13", "C_all_converged")
    assert c["pass"] is False and any("log" in x for x in c["reasons"]), c


def t_c_log_missing(root):
    rc, text, data = full(root, make_case(root, "a", log=None), make_case(root, "b", "m26"))
    assert rc == 1, text
    c = check(data, "m13", "C_all_converged")
    assert c["pass"] is False and any("log" in x for x in c["reasons"]), c


def t_provenance(root):
    rc, text, data = full(root, make_case(root, "a"), make_case(root, "b", "m26"))
    assert rc == 0, text
    for case in ("m13", "m26"):
        h = data["cases"][case]["csv_sha256"]
        assert len(h) == 64 and all(ch in "0123456789abcdef" for ch in h), h
    assert len(data["checker_sha256"]) == 64
    assert "PASS" in text and "m13" in text and "m26" in text, text


def t_c_end_fail(root):
    rows = syn.make_rows()[:301]
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 1, text
    assert check(data, "m13", "C_reached_end")["pass"] is False
    assert check(data, "m13", "C_reached_end")["last_time"] == 300.0


def t_nonfinite(root):
    rows = syn.make_rows()
    big_rows(rows)[20]["int_syy"] = float("nan")
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc != 0, text
    case = data["cases"]["m13"]
    assert case["case_pass"] is False
    assert case["integrity"]["pass"] is False


def t_missing_column(root):
    cols = [c for c in syn.COLUMNS if c != "int_szz"]
    rc, text, data = full(root, make_case(root, "a", columns=cols), make_case(root, "b", "m26"))
    assert rc == 2, text
    assert data["cases"]["m13"]["integrity"]["pass"] is False
    assert data["all_pass"] is False


def t_no_contact(root):
    rows = syn.make_rows(k=0.0, k2=0.0)
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 1, text
    for key in ("P1", "P2", "P4"):
        c = check(data, "m13", key)
        assert c["pass"] is False and c.get("status") == "NOT_COMPUTED", (key, c)


def t_small_rows_ignored(root):
    rows = syn.make_rows()
    fmax = max(abs(r["F_bot_y"]) for r in rows)
    small = [r for r in rows if 0 < abs(r["F_bot_y"]) < 1e-2 * fmax]
    assert small, "synthetic curve needs rows below 1 % of the peak"
    small[0]["F_top_y"] *= 1.5          # big imbalance, but not a 'big' row
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 0, text
    assert check(data, "m13", "P1")["pass"] is True


def t_big_row_threshold_inclusive(root):
    rows = syn.make_rows()
    fmax = max(abs(r["F_bot_y"]) for r in rows)
    small = [r for r in rows if 0 < abs(r["F_bot_y"]) < 1e-2 * fmax]
    r = small[-1]
    scale = (1e-2 * fmax) / abs(r["F_bot_y"])
    for c in ("int_sxx", "int_syy", "int_szz", "int_sxy"):
        r[c] *= scale
    r["F_bot_y"] = math.copysign(1e-2 * fmax, r["F_bot_y"])   # exactly 1 % of the peak
    r["F_top_y"] = -1.5 * r["F_bot_y"]                          # and broken -> P1 must see it
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 1, text
    assert check(data, "m13", "P1")["pass"] is False


def t_signs_swapped(root):
    rows = syn.make_rows()
    for r in rows:
        r["F_top_y"], r["F_bot_y"] = -r["F_top_y"], -r["F_bot_y"]
    rc, text, data = full(root, make_case(root, "a", rows=rows), make_case(root, "b", "m26"))
    assert rc == 0, text


def t_area_ref_mismatch(root):
    m = make_case(root, "a", mesh_over={"disk_area_mesh_m2": syn.disk_area("m13") * (1 + 1e-6)})
    rc, text, data = full(root, m, make_case(root, "b", "m26"))
    assert rc == 2, text
    integ = data["cases"]["m13"]["integrity"]
    assert integ["pass"] is False and any("area" in x for x in integ["reasons"]), integ


def t_dt_half(root):
    a = make_case(root, "a", rows=syn.make_rows(dt=0.5))
    b = make_case(root, "b", "m26", rows=syn.make_rows(dt=0.5, tag="m26"))
    rc, text, data = full(root, a, b, extra=["--dt", "0.5"])
    assert rc == 0, text
    assert check(data, "m13", "C_all_converged")["steps"] == 814
    rc, text, data = full(root, a, b)          # same rows judged with dt 1: not contiguous
    assert rc == 1, text


def t_p6_report(root):
    rows26 = syn.make_rows(tag="m26")
    rows13 = syn.make_rows(tag="m13", k=2.0e6 * 1.02)
    rc, text, data = full(root, make_case(root, "a", rows=rows13),
                          make_case(root, "b", "m26", rows=rows26))
    assert rc == 0, text
    p6 = data["P6_report"]
    assert p6["kind"] == "REPORT_ONLY" and "pass" not in p6, p6
    # sigma_b = F / D; F13 / F26 ~ 1.02 on the linear part, the quadratic term is shared
    assert 0.015 < p6["ratio"] < 0.0205, p6
    assert p6["union_knots"] == 408, p6


def t_smoke_ok(root):
    rows = syn.make_rows(end_time=12.0)
    d = make_case(root, "s", rows=rows)
    rc, text = run(["smoke", "--case", d, "--end-time", "12"])
    assert rc == 0, text
    assert "SMOKE OK" in text, text


def t_smoke_no_contact(root):
    d = make_case(root, "s", rows=syn.make_rows(end_time=12.0, k=0.0, k2=0.0))
    rc, text = run(["smoke", "--case", d, "--end-time", "12"])
    assert rc == 1, text
    assert "contact" in text.lower(), text


def t_smoke_rc_fail(root):
    d = make_case(root, "s", rows=syn.make_rows(end_time=12.0), rc="1")
    rc, text = run(["smoke", "--case", d, "--end-time", "12"])
    assert rc == 1, text


def t_smoke_missing_csv(root):
    d = make_case(root, "s", rows=syn.make_rows(end_time=12.0))
    os.remove(os.path.join(d, "out.csv"))
    rc, text = run(["smoke", "--case", d, "--end-time", "12"])
    assert rc == 1, text


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_")]


def main():
    npass = nfail = 0
    for t in TESTS:
        root = tempfile.mkdtemp(prefix="ck_")
        try:
            t(root)
            npass += 1
            print("PASS", t.__name__)
        except Exception as exc:        # report and continue
            nfail += 1
            print("FAIL", t.__name__, "-", type(exc).__name__, str(exc)[:300].replace("\n", " | "))
        finally:
            shutil.rmtree(root, ignore_errors=True)
    print("check_step1 tests: %d passed, %d failed, %d total" % (npass, nfail, npass + nfail))
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
