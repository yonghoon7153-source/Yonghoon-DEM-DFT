#!/usr/bin/env python3
"""R6 validator lens — independent adversarial VERIFICATION (refutation attempts), target worktree @ 1049894.

Fixtures are written by THIS script (not the lens's): distinct anchor values, multiplicative 1.5 % gap,
own file names. CLI is driven exactly as tests/test_review_findings.py::test_r3_07 does (data_root/build/
anchors patched, verify.main(["eval","--compare",…]) in a separate process, cwd = worktree bms-balancing).
Run: python3 verify_r6.py [v01 … v09 | all]
"""
import sys, os, io, json, shutil, pathlib, subprocess, contextlib, textwrap, uuid
SCR = pathlib.Path(__file__).resolve().parent
WT = SCR / "wt_verify_validator" / "bms-balancing"
FX = SCR / "fixtures"; FX.mkdir(exist_ok=True)
sys.path.insert(0, str(WT)); sys.path.insert(0, str(WT / "scripts"))
from bms_balancing import verify
from bms_balancing.verify import ANCHOR_STAGE, DD_EVAL_P, PARAM_COLS
import provenance as pv

COLS = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
P = [list(p) for p in DD_EVAL_P]
ANCH = {k: round(0.5 + 0.07 * n, 6) for n, (k, _) in enumerate(ANCHOR_STAGE)}; ANCH["dv_n"] = 412.0
# Python rmse in [0.04455, 0.044755]; MATLAB = Python * 1.015 (gap 1.5 %). All in [0.0445, 0.0455) → %.2g prints "0.045".
PY = {c: [0.04455 + 0.000025 * i + 0.00001 * j for i in range(len(P))] for j, c in enumerate(COLS)}
ML = {c: [x * 1.015 for x in PY[c]] for c in COLS}
GAP = max(abs(ML[c][i] - PY[c][i]) / PY[c][i] for c in COLS for i in range(len(P)))
assert 0.014 < GAP < 0.016 and all(format(PY[c][i], ".2g") == format(ML[c][i], ".2g") == "0.045" for c in COLS for i in range(len(P)))


def csv(name, decl="# printed_format,%.17g", header="top", fmt=".17g", ncols=4, anchors=True, vals=None, extra_rows=()):
    vals = vals or ML
    lines = ([decl] if decl else []) + ([f"# {k},{v:.17g}" for k, v in ANCH.items()] if anchors else [])
    hdr = ",".join(PARAM_COLS + COLS[:ncols])
    body = list(extra_rows) + [",".join([format(x, ".6f") for x in p] + [format(vals[c][i], fmt) for c in COLS[:ncols]])
                               for i, p in enumerate(P)]
    if header == "top":
        lines += [hdr] + body
    elif header == "bottom":
        lines += body + [hdr]
    else:
        lines += body
    p = FX / name; p.write_text("\n".join(lines) + "\n", encoding="utf-8"); return p


DRIVER = SCR / "driver.py"
DRIVER.write_text(textwrap.dedent(f'''
    """mock driver — same shape as tests/test_review_findings.py::test_r3_07: data_root/build/dd_eval_anchors patched,
    then verify.main(["eval", "--compare", <csv>, *extra]) → sys.exit(rc)."""
    import sys, json
    sys.path.insert(0, {str(WT)!r})
    from unittest.mock import patch
    from bms_balancing import verify
    an = json.loads(sys.argv[1]); py = json.loads(sys.argv[2]); P = {P!r}
    class Obj:
        def _at(self, p, col): return py[col][P.index([float(x) for x in p])]
        def rmse_pocv(self, p): return self._at(p, "rmse_pocv")
        def rmse_dvdq(self, p): return self._at(p, "rmse_dvdq")
        def rmse_dqdv(self, p, weighted=False): return self._at(p, "rmse_dqdv_w" if weighted else "rmse_dqdv")
    with patch.object(verify.D, "data_root", return_value=None), \\
         patch.object(verify, "build", return_value=Obj()), \\
         patch.object(verify, "dd_eval_anchors", return_value=list(an.items())):
        sys.exit(verify.main(["eval", "--compare", sys.argv[3]] + sys.argv[4:]))
'''), encoding="utf-8")


def cli(path, *extra, py=None):
    r = subprocess.run([sys.executable, str(DRIVER), json.dumps(ANCH), json.dumps(py or PY), str(path), *extra],
                       capture_output=True, text=True, encoding="utf-8", cwd=str(WT))
    return r.returncode, r.stdout + r.stderr


def tail(out, n=2):
    ls = [l.rstrip() for l in out.splitlines() if l.startswith(("판정", "종료 코드", "  ! ", "      - ")) or "Error" in l]
    return " | ".join(ls[-n:])


def compare(path, py=None, **kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = verify._compare_dd_eval(dict(ANCH), P, py or PY, path, **kw)
    return res, buf.getvalue()


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd or str(WT)); return (r.stdout + r.stderr).rstrip()


# ─────────────────────────────────────────────────────────────────────────────────────────────
def v01():
    print("# V6-01 header BELOW data rows — declaration %.2g, tokens %.17g, model gap 1.5 %")
    top = csv("v01_hdr_top.csv", decl="# printed_format,%.2g", header="top")
    bot = csv("v01_hdr_bottom.csv", decl="# printed_format,%.2g", header="bottom")
    for label, p in (("header top   ", top), ("header bottom", bot)):
        rc, out = cli(p); print(f"  {label}: rc={rc}  {tail(out)}")
        print(f"      audit(spec sig:2) = {verify.dd_eval_csv_audit(p, spec=('sig', 2))[:1]}")
    wide_row = ",".join([format(x, ".6f") for x in P[0]] + [format(ML[c][0], ".17g") for c in COLS] + ["7.7"])
    wide = csv("v01_wide_row_before_hdr.csv", header="bottom", extra_rows=[wide_row])
    print(f"  10-field row before 9-col header: audit = {verify.dd_eval_csv_audit(wide, spec=('exact', 17))}")
    rc, out = cli(wide); print(f"      comparator on that file: rc={rc}  {tail(out)}  (row count 9≠8 → incomplete, not the audit)")
    print("  writer check — does any writer emit the header after data?")
    print("    matlab/dd_eval.m:210-211 →", sh("sed -n '210,211p' matlab/dd_eval.m").replace("\n", " ⏎ "))
    print("    first version 56a35a8 :118-119 →", sh("git show 56a35a8:bms-balancing/matlab/dd_eval.m | sed -n '118,119p'").replace("\n", " ⏎ "))
    print("    matlab/tests/mirror_dd_eval.py:188 (header appended before rows?) →", sh("sed -n '188,189p' matlab/tests/mirror_dd_eval.py").replace("\n", " ⏎ "))
    print("    verify.py cmd_eval --out: lines = [header] then rows (verify.py:936-941)")


def v02():
    print("# V6-02 --precision option never audited against tokens (tokens %.17g, gap 1.5 %)")
    undecl = csv("v02_undecl.csv", decl=None)
    e17 = csv("v02_decl_e17.csv", decl="# printed_format,%.17e", fmt=".17e")
    num = csv("v02_decl_17.csv", decl="# printed_format,17")
    g17 = csv("v02_decl_g17.csv")
    for label, p, extra in [("no decl, auto                 ", undecl, ()),
                            ("no decl, --precision g17      ", undecl, ("--precision", "g17")),
                            ("no decl, --precision sig:2    ", undecl, ("--precision", "sig:2")),
                            ("no decl, --precision fixed:0  ", undecl, ("--precision", "fixed:0")),
                            ("decl %.17e, --precision sig:2 ", e17, ("--precision", "sig:2")),
                            ("decl '17', --precision sig:2  ", num, ("--precision", "sig:2")),
                            ("CTRL decl %.17g, --precision sig:2", g17, ("--precision", "sig:2")),
                            ("CTRL decl %.17g, auto         ", g17, ())]:
        rc, out = cli(p, *extra); print(f"  {label}: rc={rc}  {tail(out)}")
    print("  branch: verify.py:1020 →", sh("sed -n '1020p' bms_balancing/verify.py").strip())
    print("  branch: verify.py:1116-1118 →", sh("sed -n '1116,1118p' bms_balancing/verify.py").replace("\n", " ⏎ ").strip())
    print("  resolve_precision(undecl, 'sig:2') →", {k: v for k, v in verify.resolve_precision(undecl, "sig:2").items() if k in ("source", "spec", "conflict", "declared_spec")})
    print("  README:59 documented order: '옵션 → 선언 → 추정'; '옵션이 선언보다 느슨해도 마찬가지(complete 아님)'; '해석 못 하는 선언은 --precision 을 명시하면 옵션이 대체한다 (R5 Q1)'")


def v03():
    print("# V6-03 header-less file — declaration %.2g, tokens %.17g, gap 1.5 %")
    nohdr = csv("v03_no_header.csv", decl="# printed_format,%.2g", header=None)
    rc3, o3 = cli(nohdr); rc0, o0 = cli(nohdr, "--allow-partial")
    print(f"  no header, auto             : rc={rc3}  {tail(o3, 3)}")
    print(f"  no header, --allow-partial  : rc={rc0}  {tail(o0, 3)}")
    print(f"  audit(spec sig:2) = {verify.dd_eval_csv_audit(nohdr, spec=('sig', 2))}")
    ctrl = csv("v03_no_header_g17.csv", header=None)
    rc, o = cli(ctrl, "--allow-partial"); print(f"  CTRL no header, decl %.17g, --allow-partial: rc={rc}  {tail(o)}")
    res, _ = compare(nohdr); print(f"  direct: status={res['status']} compared={res['compared']}/{res['expected']} partial_reasons={res['partial_reasons']}")
    print("  history: git log --follow matlab/dd_eval.m first commit =", sh("git log --follow --format=%h -- matlab/dd_eval.m | tail -1"),
          "; its file write:", sh("git show 56a35a8:bms-balancing/matlab/dd_eval.m | sed -n '118p'").strip())
    print("  committed dd_eval CSVs with a header:", sh("for f in $(git ls-files | grep -i 'dd_eval.*\\.csv$'); do printf '%s=%s ' $f $(grep -c '^a_PE' $f); done"))


def v04():
    print("# V6-04 zero rmse columns / zero anchors under --allow-partial")
    pa = csv("v04_params_plus_anchors.csv", ncols=0)
    po = csv("v04_params_only.csv", ncols=0, anchors=False)
    rc, o = cli(pa); print(f"  5 param cols + 16 anchors, auto            : rc={rc}  {tail(o, 3)}")
    rc, o = cli(pa, "--allow-partial"); print(f"  5 param cols + 16 anchors, --allow-partial : rc={rc}  {tail(o, 3)}")
    rc, o = cli(po, "--allow-partial"); print(f"  5 param cols, NO anchors,  --allow-partial : rc={rc}  {tail(o, 3)}")
    res, _ = compare(po); print(f"  direct(params only): status={res['status']} compared={res['compared']}/{res['expected']} anchors={res['anchors_compared']}/{res['anchors_expected']}")
    print("  README:59 / --help: --allow-partial = '옛 스키마(앵커·열 누락)의 부분 대조를 종료 코드 0'. Oldest real schema (56a35a8) = 2 rmse cols + header; §1-8: 구판 = 앵커 10 · rmse 2 열")


def v05():
    print("# V6-05 verify_unit ignores meta artifact/state")
    d = FX / "v05_real"; d.mkdir(exist_ok=True)
    shutil.copy(WT / "out/matrix_300_0147.csv", d / "matrix_200.csv"); shutil.copy(WT / "out/matrix_300_0147.csv.meta.json", d / "matrix_200.csv.meta.json")
    r = subprocess.run([sys.executable, str(WT / "scripts/provenance.py"), "--verify-unit", str(d / "matrix_200.csv")], capture_output=True, text=True, cwd=str(WT))
    print(f"  (a) REAL pair out/matrix_300_0147.csv(+meta) copied to matrix_200.csv → rc={r.returncode} {r.stdout.strip()!r}  (that meta has no run_id/sha256: pre-R5)")
    d2 = FX / "v05_synth"; d2.mkdir(exist_ok=True)
    rid = uuid.uuid4().hex
    a = d2 / "matrix_100.csv"
    a.write_text("half_cell,si,w_dqdv,run_id,obj,rmse_pocv\n" + "\n".join(f"GITT,Li,0.0,{rid},0.6597,0.0183" for _ in range(3)) + "\n", encoding="utf-8")
    meta = {"artifact": a.name, "state": "100", "half_cell_source": "GITT", "si_source": "Li", "starts": 24, "seed": 0,
            "w_dqdv_note": "명령별", "data_root": "/x", "run_id": rid, "sha256": pv.sha256_file(a), "git_commit": "0" * 40,
            "git_dirty": False, "git_modified_outputs": [], "git_modified_code": [], "created_utc": "2026-09-11T00:00:00+00:00"}
    (d2 / "matrix_100.csv.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    b = d2 / "matrix_200.csv"; shutil.copy(a, b); shutil.copy(str(a) + ".meta.json", str(b) + ".meta.json")
    for f in (a, b):
        r = subprocess.run([sys.executable, str(WT / "scripts/provenance.py"), "--verify-unit", str(f)], capture_output=True, text=True, cwd=str(WT))
        print(f"  (b) synthetic write_meta-shaped meta: --verify-unit {f.name} → rc={r.returncode} {r.stdout.strip()!r}; meta.artifact={json.loads((f.parent / (f.name + '.meta.json')).read_text())['artifact']!r} state='100'")
    ca = subprocess.run([sys.executable, "-c", "import csv,sys\nr = list(csv.DictReader(open(sys.argv[1])))\nsys.exit(0 if r and r[0] else 1)", str(b)])
    print(f"  (c) run_states.sh check_artifact one-liner on renamed copy → rc={ca.returncode} (0 = passes)")
    print("  matrix row keys (verify.py:1247-1256): half_cell, si, w_dqdv, run_id, scale_*, obj, rmse_pocv … — no 'state' field; 'state' only in stdout summary (verify.py:1271)")
    print("  verify_unit reads only m['run_id'], m['sha256'] (provenance.py:129); write_meta writes 'artifact' and 'state' (run_states.sh:63)")


def v06():
    print("# V6-06 numeric declaration `# printed_format,17` (tokens == Python, no gap → isolates the status)")
    same = csv("v06_decl_17_same.csv", decl="# printed_format,17", vals=PY)
    pol = verify.resolve_precision(same)
    print(f"  resolve_precision: source={pol['source']!r} declared_raw={pol['declared_raw']!r}; read_dd_eval_meta={verify.read_dd_eval_meta(same)}; read_dd_eval_csv anchors['printed_format']={verify.read_dd_eval_csv(same)[0].get('printed_format')}")
    print(f"  audit(spec None) = {verify.dd_eval_csv_audit(same)}   (n_decl counted, value never validated)")
    rc, o = cli(same); print(f"  auto                  : rc={rc}  {tail(o, 3)}")
    rc, o = cli(same, "--precision", "sig:2"); lab = [l for l in o.splitlines() if "정밀도:" in l]; print(f"  --precision sig:2     : rc={rc}  label={lab[0].strip() if lab else None}")
    bad = csv("v06_decl_text_bad.csv", decl="# printed_format,seventeen", vals=PY)
    rc, o = cli(bad); print(f"  CTRL text decl 'seventeen', auto: rc={rc}  {tail(o)}")
    rc, o = cli(bad, "--precision", "sig:2"); lab = [l for l in o.splitlines() if "정밀도:" in l]; print(f"  CTRL text decl, --precision sig:2: rc={rc}  label={lab[0].strip() if lab else None}")
    print("  FINDINGS §1-8 R4: '해석 못 하는 선언은 invalid(종료 2)다'; README:59: '두 번째 형식 선언 … invalid', '예외 하나: 해석 못 하는 선언은 --precision 을 명시하면 옵션이 대체한다'")


def v07():
    print("# V6-07 unreadable --compare path")
    rc1, o1 = cli(FX / "does_not_exist.csv"); rc2, o2 = cli(FX)
    print(f"  missing file: rc={rc1}  last stderr line: {o1.strip().splitlines()[-1]!r}  '종료 코드' printed: {'종료 코드' in o1}")
    print(f"  directory   : rc={rc2}  last stderr line: {o2.strip().splitlines()[-1]!r}")
    print("  cmd_eval catches only ValueError (verify.py:955); read_dd_eval_csv → Path.read_text (verify.py:552) raises OSError uncaught")
    print("  README:59 / --help: '종료 코드: 0 complete · 1 갈림 · 2 미완 · 3 부분' — 1 = 갈림(앵커/목적함수)")


def v08():
    print("# V6-08 duplicate run_id column in CSV")
    import csv as _csv
    rid, other = "a" * 32, "b" * 32
    p = FX / "v08_dup_run_id.csv"; p.write_text(f"run_id,half_cell,run_id\n{other},GITT,{rid}\n{other},GITT,{rid}\n", encoding="utf-8")
    print(f"  check_run_id(rid=last col)  → {pv.check_run_id(p, rid)}")
    print(f"  check_run_id(rid=first col) → {pv.check_run_id(p, other)}")
    print(f"  DictReader row → {list(_csv.DictReader(p.open(encoding='utf-8')))[0]}")
    print("  writers: atomic_write_csv(path, rows, keys) takes fieldnames from dict keys (unique) — no repo writer can emit two run_id columns; hand-edit only")
    print("  asymmetry: dd_eval_csv_audit flags '중복 열' (verify.py:632-634); check_run_id does not")


def v09():
    print("# V6-09 signed zero under %f")
    ex_a = verify.token_excess(("fixed", 6), 0.0, -1e-20); ex_b = verify.token_excess(("fixed", 6), -0.0, 1e-20); ex_c = verify.token_excess(("fixed", 6), 0.0, 1e-20)
    print(f"  token '0.000000' vs pv=-1e-20: excess={ex_a:.3g} eff=excess/max(|pv|,1e-30)={ex_a / max(1e-20, 1e-30):.3g} (MODEL_REL={verify.MODEL_REL:.0e})")
    print(f"  token '-0.000000' vs pv=+1e-20: excess={ex_b:.3g};  CTRL token '0.000000' vs pv=+1e-20: excess={ex_c:.3g}")
    ml = {c: list(PY[c]) for c in COLS}; py2 = {c: list(PY[c]) for c in COLS}
    ml["rmse_pocv"][2] = 0.0; py2["rmse_pocv"][2] = -1e-20
    f = csv("v09_signed_zero_f6.csv", decl="# printed_format,%.6f", fmt=".6f", vals=ml)
    rc, o = cli(f, py=py2); print(f"  comparator (%.6f, one cell MATLAB 0.000000 vs Python -1e-20): rc={rc}  {tail(o)}")
    import numpy as np
    z = float(np.sqrt(np.mean(np.zeros(5) ** 2))); print(f"  reachability: rmse = sqrt(mean(r²)) (model.py:348,352,372-373) → {z!r} → format {format(z, '.6f')!r}; a negative or -0.0 rmse cannot be produced by either side")
    print("  current writers declare %.17g (exact → token_excess = |mv−pv|, no bisection); %f only in pre-R3 files (§1-8: 구판 %.10f)")


def raw_cli():
    print("# raw CLI without BMS_DATA_ROOT (why the mock driver is needed, as in tests)")
    r = subprocess.run([sys.executable, "-m", "bms_balancing.verify", "eval", "--compare", str(FX / "v02_decl_g17.csv")], capture_output=True, text=True, cwd=str(WT), env={**os.environ, "BMS_DATA_ROOT": ""})
    print(f"  rc={r.returncode} stderr={r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''!r}")


CASES = {"v01": v01, "v02": v02, "v03": v03, "v04": v04, "v05": v05, "v06": v06, "v07": v07, "v08": v08, "v09": v09, "raw": raw_cli}
if __name__ == "__main__":
    print(f"target {WT}  HEAD {sh('git rev-parse --short HEAD')}  gap {GAP:.3%}  fixtures {FX}")
    want = sys.argv[1:] or list(CASES)
    for name in want:
        print(); CASES[name]()
