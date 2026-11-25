"""MPFEM step 1 (MOOSE) checker - development data.  Standard library only.

Checks fixed before any run: mpfem_plan/step1_kratos_onedisk.md section 4, computed with the
formulas of mpfem_plan/step1_inputs/run_onedisk.py.  Rows used by P1 P2 P4 = steps whose
|F_bot| >= 1 % of the peak |F_bot|.  Forces per unit thickness (2D plane strain).
  C   every step converged (exit code 0, no failure line in run.log, steps dt, 2 dt, ... with
      no gap) and the run reached the end time
  P1  | |F_top| - |F_bot| | / max(|F_top|, |F_bot|)                                <= 1e-3
  P2  | <syy> + |F_bot| h / A | / (|F_bot| h / A)  and  |<sxx>| / |<syy>|            <= 1e-2
  P4  | (A / A0 - 1) - (<sxx> + <syy> + <szz>) / (3 K) |,  K = E / (3 (1 - 2 nu))      <= 1e-3
  P6  report only (m13 vs m26): sigma_b(u) = |F_bot| / D against the plate approach u,
      shape of rule U6c-06: common support, union of samples, max difference / fine maximum
<s> = area-weighted mean Cauchy stress of the disk in the current configuration, A = current
disk area, A0 = initial disk polygon area, h = distance between the plate faces.

  check_step1.py full  --case m13=DIR --case m26=DIR [--dt 1] [--end-time 407] [--out JSON]
  check_step1.py smoke --case DIR [--dt 1] [--end-time 12]
DIR holds out.csv (MOOSE postprocessors), rc.txt, run.log and disk.mesh.json.
Exit: 0 all checks pass | 1 a check fails | 2 invalid input (missing or non-finite data).
"""
import argparse
import bisect
import csv
import hashlib
import json
import math
import os
import sys

E, NU, D_REG, SY = 1.0e7, 0.45, 0.1, 4.0e5
K = E / (3 * (1 - 2 * NU))
TOL = {"P1": 1e-3, "P2_syy": 1e-2, "P2_sxx": 1e-2, "P4": 1e-3,
       "big_row_fraction": 1e-2, "C_end_rel": 1e-9}
REQUIRED = ["time", "F_top_y", "F_bot_y", "u_top", "u_bot", "area", "area_ref",
            "int_sxx", "int_syy", "int_szz"]
MARKERS = ["did not converge", "cannot continue", "*** error", "aborting"]
INF = float("inf")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


def worst(pairs):
    """Max over (value, time); NaN counts as +inf so that it can never pass."""
    best = (-INF, None)
    for v, t in pairs:
        v = INF if math.isnan(v) else v
        if v > best[0]:
            best = (v, t)
    return best


def read_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def evaluate(d, dt, end_time):
    res = {"dir": os.path.abspath(d), "integrity": {"pass": True, "reasons": []},
           "checks": {}, "report": {}}
    bad = res["integrity"]["reasons"]
    path = os.path.join(d, "out.csv")
    cols, rows_all = [], []
    if os.path.exists(path):
        res["csv_sha256"] = sha256(path)
        with open(path, newline="", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            cols = rd.fieldnames or []
            rows_all = [dict((k, num(v)) for k, v in r.items()) for r in rd]
    else:
        bad.append("out.csv missing")
    miss = [c for c in REQUIRED if c not in cols]
    if os.path.exists(path) and miss:
        bad.append("columns missing: " + " ".join(miss))
    mesh = {}
    mtext = read_text(os.path.join(d, "disk.mesh.json"))
    try:
        mesh = json.loads(mtext) if mtext is not None else {}
    except ValueError:
        pass
    if not mesh:
        bad.append("disk.mesh.json missing or unreadable")
    D, h0 = mesh.get("D_m", float("nan")), mesh.get("h0_between_plates_m", float("nan"))
    A0 = mesh.get("disk_area_mesh_m2", float("nan"))
    if mesh:
        if D != D_REG:
            bad.append("mesh D_m %r != registered %r" % (D, D_REG))
        if not abs(h0 - (2 * mesh.get("R_m", 0.0) + 2 * mesh.get("gap_m", 0.0))) <= 1e-12:
            bad.append("mesh h0 inconsistent with R and gap")
    rows = [r for r in rows_all if not miss and r.get("time", 0.0) > 0]
    if not miss:
        for r in rows:
            nf = [c for c in REQUIRED if not math.isfinite(r[c])]
            if nf:
                bad.append("non-finite %s at time %r" % (",".join(nf), r["time"]))
                break
        times = [r["time"] for r in rows]
        if any(b <= a for a, b in zip(times, times[1:])):
            bad.append("time not strictly increasing")
        refs = [r["area_ref"] for r in rows if math.isfinite(r["area_ref"])]
        if refs and mesh and not (max(abs(a - A0) for a in refs) <= 1e-9 * abs(A0)):
            bad.append("area_ref differs from the mesh polygon area by more than 1e-9")
    res["integrity"]["pass"] = not bad

    # ---------------- C
    rc_text = read_text(os.path.join(d, "rc.txt"))
    log = read_text(os.path.join(d, "run.log"))
    why = []
    try:
        rc = int(rc_text.strip())
    except (AttributeError, ValueError):
        rc = None
    if rc is None:
        why.append("rc.txt missing or unreadable")
    elif rc != 0:
        why.append("exit code rc %d" % rc)
    if log is None:
        why.append("run.log missing")
    else:
        hits = [ln.strip() for ln in log.splitlines() if any(m in ln.lower() for m in MARKERS)]
        if hits:
            why.append("log: " + hits[0][:120])
    for k, r in enumerate(rows, 1):
        if not abs(r["time"] - k * dt) <= 1e-9 * max(1.0, k * dt):
            why.append("steps not contiguous with dt %g at time %r" % (dt, r["time"]))
            break
    if rows and "nl_its" in cols and any(r["nl_its"] > 30 for r in rows):
        why.append("nl_its above 30")
    if not rows:
        why.append("no step rows")
    expected = int(round(end_time / dt))
    res["checks"]["C_all_converged"] = {"pass": bool(rows) and not why, "reasons": why,
                                        "steps": len(rows), "expected_steps": expected, "rc": rc}
    last = rows[-1]["time"] if rows else None
    res["checks"]["C_reached_end"] = {
        "pass": bool(rows) and last >= end_time * (1 - TOL["C_end_rel"]),
        "last_time": last, "end_time": end_time}

    # ---------------- P1 P2 P4 (rows with |F_bot| >= 1 % of the peak)
    fb = lambda r: abs(r["F_bot_y"])
    ft = lambda r: abs(r["F_top_y"])
    fmax = max((fb(r) for r in rows if math.isfinite(fb(r))), default=0.0)
    loaded = [r for r in rows if max(ft(r), fb(r)) > 0]
    big = [r for r in loaded if fb(r) >= TOL["big_row_fraction"] * fmax] if fmax > 0 else []
    if not big:
        nc = {"pass": False, "status": "NOT_COMPUTED",
              "reason": "no step with |F_bot| >= 1 % of the peak (no contact force)"}
        for key in ("P1", "P2", "P4"):
            res["checks"][key] = dict(nc)
    else:
        v, t = worst(((abs(ft(r) - fb(r)) / max(ft(r), fb(r)), r["time"]) for r in big))
        res["checks"]["P1"] = {"pass": v <= TOL["P1"], "value": v, "tol": TOL["P1"],
                               "worst_time": t}
        p2y, p2x = [], []
        for r in big:
            A = r["area"]
            ref = fb(r) * (h0 + r["u_top"] - r["u_bot"]) / A
            syy, sxx = r["int_syy"] / A, r["int_sxx"] / A
            p2y.append((abs(syy + ref) / ref, r["time"]))
            p2x.append((abs(sxx) / abs(syy) if syy != 0 else INF, r["time"]))
        vy, ty = worst(p2y)
        vx, tx = worst(p2x)
        res["checks"]["P2"] = {"pass": vy <= TOL["P2_syy"] and vx <= TOL["P2_sxx"],
                               "syy_value": vy, "sxx_value": vx, "tol": TOL["P2_syy"],
                               "worst_time_syy": ty, "worst_time_sxx": tx}
        v, t = worst(((abs((r["area"] / A0 - 1)
                           - (r["int_sxx"] + r["int_syy"] + r["int_szz"]) / r["area"] / (3 * K)),
                       r["time"]) for r in big))
        res["checks"]["P4"] = {"pass": v <= TOL["P4"], "value": v, "tol": TOL["P4"],
                               "worst_time": t, "K_Pa": K}

    # ---------------- report only
    rep = res["report"]
    rep["Fmax_N_per_m"] = fmax
    rep["sigma_b_max_Pa"] = fmax / D_REG
    rep["big_rows"] = len(big)
    rep["first_big_time"] = big[0]["time"] if big else None
    if rows:
        rep["final_approach_m"] = rows[-1]["u_bot"] - rows[-1]["u_top"]
        if mesh:
            rep["area_ref_vs_mesh_rel"] = max(abs(r["area_ref"] - A0) for r in rows) / abs(A0)
    opt = lambda c: c in cols
    if big and opt("F_top_x") and opt("F_bot_x"):
        rep["Fx_over_Fbot_max"] = worst(((max(abs(r["F_top_x"]), abs(r["F_bot_x"])) / fb(r),
                                          r["time"]) for r in big))[0]
    if big and opt("R_symy_y"):
        rep["symy_reaction_over_Fbot_max"] = worst(((abs(r["R_symy_y"]) / fb(r), r["time"])
                                                    for r in big))[0]
    if rows and opt("nl_its"):
        rep["nl_its_max"] = max(r["nl_its"] for r in rows)
        rep["nl_its_total"] = sum(r["nl_its"] for r in rows)
    if rows and opt("svm_max"):
        rep["svm_max_over_sy"] = max(r["svm_max"] for r in rows) / SY
    res["case_pass"] = res["integrity"]["pass"] and all(c["pass"] for c in res["checks"].values())
    res["_curve"] = [(0.0, 0.0)] + [(r["u_bot"] - r["u_top"], fb(r) / D_REG) for r in rows]
    return res


def interp(u, xs, ys):
    i = bisect.bisect_right(xs, u) - 1
    if i >= len(xs) - 1:
        return ys[-1]
    w = (u - xs[i]) / (xs[i + 1] - xs[i])
    return ys[i] + w * (ys[i + 1] - ys[i])


def p6(coarse, fine):
    out = {"kind": "REPORT_ONLY", "coarse": "m13", "fine": "m26",
           "rule": "U6c-06 shape: common support [0, min end], union of native samples, "
                   "piecewise linear, max |coarse - fine| / max |fine|"}
    a, ya = zip(*coarse) if coarse else ((), ())
    b, yb = zip(*fine) if fine else ((), ())
    ok = (len(a) > 1 and len(b) > 1 and all(map(math.isfinite, a + b + ya + yb))
          and all(q > p for p, q in zip(a, a[1:])) and all(q > p for p, q in zip(b, b[1:])))
    if not ok:
        out.update(status="HOLD", reason="curve missing, non-finite or not increasing in u")
        return out
    end = min(a[-1], b[-1])
    knots = sorted(set(x for x in a if x <= end) | set(x for x in b if x <= end))
    diff = [(abs(interp(u, a, ya) - interp(u, b, yb)), u) for u in knots]
    ref = [(abs(interp(u, b, yb)), u) for u in knots]
    num_, u_num = max(diff)
    den, u_den = max(ref)
    out.update(support_m=[0.0, end], union_knots=len(knots), max_abs_difference_MPa=num_ / 1e6,
               u_at_max_difference_m=u_num, fine_max_MPa=den / 1e6, u_at_fine_max_m=u_den,
               ratio=(num_ / den) if den > 0 else None)
    if den == 0:
        out.update(status="HOLD", reason="zero reference")
    return out


def fmt(x):
    return "n/a" if x is None else ("%.3g" % x)


def line(name, r):
    c = r["checks"]
    a, b = c["C_all_converged"], c["C_reached_end"]
    s = ["%s:" % name,
         "C %s (%d/%d steps, rc %s)" % ("PASS" if a["pass"] and b["pass"] else "FAIL",
                                        a["steps"], a["expected_steps"], a["rc"])]
    for key in ("P1", "P2", "P4"):
        x = c[key]
        if x.get("status") == "NOT_COMPUTED":
            s.append("%s FAIL (not computed)" % key)
        elif key == "P2":
            s.append("P2 %s syy %s sxx %s (tol %g)" % ("PASS" if x["pass"] else "FAIL",
                     fmt(x["syy_value"]), fmt(x["sxx_value"]), x["tol"]))
        else:
            s.append("%s %s %s (tol %g)" % (key, "PASS" if x["pass"] else "FAIL",
                                            fmt(x["value"]), x["tol"]))
    rp = r["report"]
    s.append("Fmax %s N/m, sigma_b max %s MPa" % (fmt(rp.get("Fmax_N_per_m")),
                                                  fmt(rp.get("sigma_b_max_Pa", 0) / 1e6)))
    if not r["integrity"]["pass"]:
        s.append("INVALID INPUT: " + "; ".join(r["integrity"]["reasons"]))
    return s[0] + " " + " | ".join(s[1:])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("full", "smoke"))
    ap.add_argument("--case", action="append", required=True, help="NAME=DIR (full) or DIR (smoke)")
    ap.add_argument("--dt", type=float, default=1.0)
    ap.add_argument("--end-time", type=float, default=None)
    ap.add_argument("--out", default=None, help="JSON report (full mode)")
    args = ap.parse_args(argv)

    if args.mode == "smoke":
        end = 12.0 if args.end_time is None else args.end_time
        r = evaluate(args.case[0], args.dt, end)
        c = r["checks"]
        why = list(r["integrity"]["reasons"]) + c["C_all_converged"]["reasons"]
        if not c["C_reached_end"]["pass"]:
            why.append("end time %g not reached (last %r)" % (end, c["C_reached_end"]["last_time"]))
        if r["report"]["Fmax_N_per_m"] <= 0:
            why.append("no contact force (F_bot = 0 on every step)")
        if why:
            print("SMOKE FAIL: " + "; ".join(why))
            return 1
        pv = " ".join("%s=%s" % (k, fmt(c[k].get("value", c[k].get("syy_value"))))
                      for k in ("P1", "P2", "P4") if "status" not in c[k])
        print("SMOKE OK: %d steps, rc 0, contact force %s N/m at the last step; preview (not "
              "judged) %s" % (c["C_all_converged"]["steps"], fmt(r["report"]["Fmax_N_per_m"]), pv))
        return 0

    end = 407.0 if args.end_time is None else args.end_time
    cases = {}
    for spec in args.case:
        name, _, d = spec.partition("=")
        cases[name] = evaluate(d, args.dt, end)
    curves = {k: v.pop("_curve") for k, v in cases.items()}
    if "m13" in curves and "m26" in curves:
        rep6 = p6(curves["m13"], curves["m26"])
    else:
        rep6 = {"kind": "REPORT_ONLY", "status": "HOLD", "reason": "needs cases m13 and m26"}
    invalid = any(not r["integrity"]["pass"] for r in cases.values())
    all_pass = bool(cases) and all(r["case_pass"] for r in cases.values())
    report = {
        "label": "DEVELOPMENT_ONLY", "kind": "mpfem_step1_moose_check",
        "registered": {"E_Pa": E, "nu": NU, "K_Pa": K, "D_m": D_REG, "tol": TOL,
                       "source": "mpfem_plan/step1_kratos_onedisk.md section 4; formulas of "
                                 "mpfem_plan/step1_inputs/run_onedisk.py"},
        "dt": args.dt, "end_time": end, "cases": cases, "P6_report": rep6,
        "all_pass": all_pass, "checker_sha256": sha256(os.path.abspath(__file__)),
    }
    print("== MPFEM step 1 (MOOSE) check - DEVELOPMENT_ONLY (checks fixed before the run)")
    for name, r in cases.items():
        print(line(name, r))
    if rep6.get("ratio") is not None:
        print("P6 (report only) m13 vs m26 sigma_b(u): max|diff| %s MPa / fine max %s MPa = %s "
              "(0..%s m, %d samples)" % (fmt(rep6["max_abs_difference_MPa"]),
                                          fmt(rep6["fine_max_MPa"]), fmt(rep6["ratio"]),
                                          fmt(rep6["support_m"][1]), rep6["union_knots"]))
    else:
        print("P6 (report only): %s" % rep6.get("reason"))
    print("ALL (C P1 P2 P4 on %s): %s" % (" and ".join(cases), "PASS" if all_pass else "FAIL"))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=1, allow_nan=True)
            f.write("\n")
        print("JSON: " + os.path.abspath(args.out))
    return 2 if invalid else (0 if all_pass else 1)


if __name__ == "__main__":
    sys.exit(main())
