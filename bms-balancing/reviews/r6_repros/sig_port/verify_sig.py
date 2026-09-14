#!/usr/bin/env python3
"""Independent re-verification of sig_port F1/F2/F4/F5/F7/F9/F10/F11 against the detached worktree @1049894."""
import csv, errno, json, os, pathlib, re, shutil, subprocess, sys, importlib, contextlib, io
S = pathlib.Path(__file__).resolve().parent; BMS = S / "wt/bms-balancing"; DATA = S / "data"; PY = sys.executable
REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT"); OUT = S / "out_A"; OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(BMS))
def sh(cmd, cwd=BMS, env=None, **kw):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
def audit(root, *extra, env=None, cwd=BMS):
    r = sh([PY, "-m", "bms_balancing.verify", "eval", "--data-root", str(root), "--state", "pristine", *extra], env=env, cwd=cwd)
    return r.returncode, next((l for l in r.stdout.splitlines() if l.startswith("# scale_audit,")), ""), r.stderr
def sec(n): print(f"\n=== {n}", flush=True)

sec("F1 root label")
rc, ln, _ = audit(DATA / "가형 관련/degradation mode"); print("rc", rc, "|", ln[:100])
head = re.compile(r"state=(\S+) source=(\S+) si=(\S+) seed=(\d+) n=(\d+)")
print("test_u13 head.search:", head.search(ln).groups()); print("root=(\\S+) ->", re.search(r"root=(\S+)", ln).group(1))
la, lb = (re.search(r"root=(\S+)", audit(DATA / p)[1]).group(1) for p in ("cells/c168", "cells_v2/c168"))
print("cells/c168 vs cells_v2/c168 label:", repr(la), repr(lb), "SAME" if la == lb else "different")
print("--data-root . :", audit(".", env={**os.environ, "PYTHONPATH": str(BMS)}, cwd=DATA / "cells/c168")[1][:50])

sec("F2 forged U13 copy vs real test_u13")
fake = S / "f2_root"; (fake / "out").mkdir(parents=True, exist_ok=True); shutil.copy(BMS / "FINDINGS.md", fake / "FINDINGS.md")
lines = (BMS / "out/scale_audit_eval_u13.txt").read_text(encoding="utf-8").splitlines()
aud = [l for l in lines if l.startswith("# scale_audit,")]; hdr = [l for l in lines if not l.startswith("# scale_audit,")]
print("non-audit header lines of the copy:", hdr[:4])
first = {}
for l in aud:
    k = head.search(l).groups()[:3]; first.setdefault(k, l)
one_root = [first[(st, "GITT", "Li")] for st in ("pristine", "100", "200", "300_0009")]
forged = list(reversed(one_root * 4 + [first[("pristine", "GITT", "Kunz")], first[("pristine", "step_005C", "Li")]]))
(fake / "out/scale_audit_eval_u13.txt").write_text("\n".join(hdr + forged) + "\n", encoding="utf-8")
print("forged:", len(forged), "lines, distinct:", len(set(forged)), "(GITT/Li lines = first occurrence per state, x4, reversed)")
sys.path.insert(0, str(BMS / "tests")); T = importlib.import_module("test_review_findings"); old = T.ROOT; T.ROOT = fake
try:
    T.test_u13_scale_audit_transcript_meets_the_equivalence_condition_and_covers_the_recompare_configs(); print("real test_u13 on forged copy: PASSED")
except AssertionError as e: print("real test_u13 on forged copy: FAILED ->", e)
finally: T.ROOT = old

sec("F4 full-cell workbook identity")
from bms_balancing import data as D, verify
import pandas as pd
root = DATA / "cells_v2/c168"; d = root / "data/full_cell/large_cell_033C"
print("data.py select:", "sorted(d.glob('*.xlsx') ...)[0]  | candidates before:", [p.name for p in d.glob("*.xlsx")])
o1 = verify.build(root, "GITT", "100", "Li", scale_seed=0)
copy = d / "fullcell_states - 복사본.xlsx"; df = pd.read_excel(d / "fullcell_states.xlsx", header=None)
df.iloc[2:, 3] = df.iloc[2:, 3].astype(float) * 1.01; df.to_excel(copy, header=False, index=False)
try:
    err = io.StringIO()
    with contextlib.redirect_stderr(err): chosen = D.full_cell_workbook(root).name; o2 = verify.build(root, "GITT", "100", "Li", scale_seed=0)
    print("chosen:", repr(chosen), "| stderr warning:", err.getvalue().strip()[:110])
    print("scales pocv:", float(o1.scales["pocv"]).hex(), "->", float(o2.scales["pocv"]).hex(), "| dvdq:", float(o1.scales["dvdq"]).hex(), "->", float(o2.scales["dvdq"]).hex())
    r = sh([PY, "-m", "bms_balancing.verify", "eval", "--data-root", str(root), "--state", "100", "--out", str(OUT / "f4.csv")])
    print("eval rc", r.returncode, "| stderr has [data] warning:", "[data]" in r.stderr, "| eval csv header:", (OUT / "f4.csv").read_text(encoding="utf-8").splitlines()[0][:120])
    print("eval stdout/csv mention workbook name?:", "복사본" in r.stdout, "복사본" in (OUT / "f4.csv").read_text(encoding="utf-8"))
finally: copy.unlink()
print("meta keys (run_states.sh PYMETA):", re.findall(r'"([a-z_]+)":', "".join((BMS / "scripts/run_states.sh").read_text(encoding="utf-8").splitlines()[62:69])))
print("README/run_states/FINDINGS mention 워크북|workbook|xlsx 하나:", bool(sh(["grep", "-rlE", "워크북|workbook|xlsx 하나", "README.md", "scripts/run_states.sh", "FINDINGS.md"]).stdout.strip()))

sec("F5 args not in signature")
root = DATA / "가형 관련/degradation mode"; rows = {}
for m in ("global", "per-gamma"):
    r = sh([PY, "-m", "bms_balancing.verify", "profile", "--data-root", str(root), "--state", "100", "--starts", "1", "--grid", "5", "--seed", "0",
            "--profile-scale", m, "--run-id", "RID-SAME", "--out", str(OUT / f"p_{m}.csv")])
    print(m, "rc", r.returncode, "| stdout SUMMARY has profile_scale:", f'"profile_scale": "{m}"' in r.stdout)
    rows[m] = list(csv.DictReader((OUT / f"p_{m}.csv").open(encoding="utf-8")))
print("csv header:", list(rows["global"][0])); print("same header:", list(rows["global"][0]) == list(rows["per-gamma"][0]), "| run_id:", rows["global"][0]["run_id"], rows["per-gamma"][0]["run_id"])
print("row0 obj:", rows["global"][0]["obj"], "vs", rows["per-gamma"][0]["obj"], "| LAM_NE_pct:", rows["global"][0]["LAM_NE_pct"], "vs", rows["per-gamma"][0]["LAM_NE_pct"])
js = {}
for n in ("4", "40"):
    r = sh([PY, "-m", "bms_balancing.verify", "degeneracy", "--data-root", str(root), "--state", "100", "--starts", "1", "--grid", "3", "--samples", n, "--seed", "0", "--run-id", "RID-SAME"])
    js[n] = json.loads(r.stdout)
print("degeneracy keys:", sorted(js["4"])); print("keys differing 4 vs 40:", sorted(k for k in js["4"] if js["4"].get(k) != js["40"].get(k)), "| n_accepted", js["4"]["n_accepted"], js["40"]["n_accepted"])
from types import SimpleNamespace
old_si = verify.D.SI_SOURCES; verify.D.SI_SOURCES = ["Li"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        verify.cmd_matrix(SimpleNamespace(data_root=str(root), source="GITT", state="100", si_source="Li", w_dqdv=0.0, seed=0, starts=1, only_source=True, only_wdqdv=True, out=str(OUT / "m.csv"), run_id="RID-M"))
finally: verify.D.SI_SOURCES = old_si
mh = list(csv.DictReader((OUT / "m.csv").open(encoding="utf-8")))[0]; print("matrix header:", list(mh)); print("matrix has starts?:", [k for k in mh if "start" in k])
ws = (BMS / "scripts/run_states.sh").read_text(encoding="utf-8").splitlines()
print("run_states.sh seed literals:", [(i + 1, l.strip()[:70]) for i, l in enumerate(ws) if '"seed": 0' in l or "--seed 0" in l])
print("run_states.sh profile/matrix stdout->.log ('-' redirect):", [(i + 1, l.strip()[:60]) for i, l in enumerate(ws) if l.strip().startswith("run ") and '" -' in l or l.strip().endswith('" - \\')])
print("run_states.sh passes --profile-scale / --samples:", any("--profile-scale" in l for l in ws), [l.strip()[:80] for l in ws if "--samples" in l])

sec("F7 provenance cwd")
c = S / "prov_clone"; shutil.rmtree(c, ignore_errors=True); sh(["git", "clone", "-q", "--shared", str(REPO), str(c)], cwd=S); sh(["git", "checkout", "-q", "1049894"], cwd=c)
b = c / "bms-balancing"; mod = b / "out/matrix_300_0147.csv"; art = "out/degeneracy_300_0147_Li.json"; print("files exist:", mod.exists(), (b / art).exists())
with mod.open("a", encoding="utf-8") as fh: fh.write("\n")
for label, cwd, argv in (("cwd=bms-balancing", b, [str(b / "scripts/provenance.py"), art]), ("cwd=repo-root", c, [str(b / "scripts/provenance.py"), "bms-balancing/" + art]), ("cwd=/tmp", pathlib.Path("/tmp"), [str(b / "scripts/provenance.py"), str(b / art)])):
    j = json.loads(sh([PY, *argv], cwd=cwd).stdout); print(f"{label:20s} git_dirty={j['git_dirty']} code={j['git_modified_code']} outputs={j['git_modified_outputs']}")
print("provenance.git_provenance signature:", [l.strip() for l in (BMS / "scripts/provenance.py").read_text(encoding="utf-8").splitlines() if l.startswith("def git_provenance")])
print("ne_shape.py chdir/cwd pin:", sh(["grep", "-n", "chdir\\|git_provenance(", "scripts/ne_shape.py"]).stdout.strip()); print("run_states.sh cd:", ws[17].strip())

sec("F9 non-UTF-8")
r = sh([PY, "-m", "bms_balancing.verify", "degeneracy", "--data-root", str(root), "--state", "100", "--starts", "1", "--grid", "3", "--samples", "2", "--run-id", "RID"])
j = OUT / "f9.json"; j.write_text(r.stdout, encoding="utf-8"); print("degeneracy JSON has Hangul:", bool(re.search("[가-힣]", r.stdout)))
snippet = 'import json,sys\nd = json.load(open(sys.argv[1]))\nsys.exit(0 if isinstance(d, dict) and d else 1)'
for label, extra in (("LC_ALL=C only (PEP538 coercion on)", {"LC_ALL": "C"}), ("LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0", {"LC_ALL": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"})):
    env = {k: v for k, v in os.environ.items() if k not in ("LANG", "LC_CTYPE", "PYTHONUTF8", "PYTHONIOENCODING")}; env.update(extra)
    r1 = sh([PY, "-c", snippet, str(j)], env=env); r2 = sh([PY, str(BMS / "scripts/provenance.py"), "--check-run-id", str(j), "RID"], env=env)
    print(f"{label:42s} check_artifact rc={r1.returncode} | check-run-id rc={r2.returncode}", (r2.stderr.strip().splitlines() or [r2.stdout.strip()])[-1][:70])
for lab, rt in (("kr basename '가형 관련'", DATA / "kr/가형 관련"), ("user-like root basename 'degradation mode'", DATA / "가형 관련/degradation mode")):
    outp = OUT / f"f9_{len(lab)}.csv"; outp.unlink(missing_ok=True)
    rc, ln, err = audit(rt, "--out", str(outp), env={**os.environ, "PYTHONIOENCODING": "cp1252"})
    print(f"PYTHONIOENCODING=cp1252 {lab:44s} rc={rc} out_written={outp.exists()}", (err.strip().splitlines() or [""])[-1][:70] if rc else "")
print("run_states.sh sets PYTHONUTF8/LC_ALL:", [l.strip() for l in ws if "PYTHONUTF8" in l or "LC_ALL" in l])

sec("F10 ENOLCK")
import fcntl; dd = S / "f10"; shutil.rmtree(dd, ignore_errors=True); dd.mkdir(); real = fcntl.flock
def boom(fh, op): raise OSError(errno.ENOLCK, "No locks available")
fcntl.flock = boom
try:
    try: verify.atomic_write_csv(dd / "profile.csv", [{"gamma_Si": 0.1, "obj": 1.0, "run_id": "r"}], ["gamma_Si", "obj", "run_id"]); print("no exception")
    except OSError as e: print("raised:", e)
finally: fcntl.flock = real
print("files left:", sorted(p.name for p in dd.iterdir())); print("R6_REQUEST flock/WSL note:", [l.strip()[:120] for l in (BMS / "reviews/R6_REQUEST.md").read_text(encoding="utf-8").splitlines() if "flock" in l][:2])

sec("F11 stale numbers / .lock")
r = sh([PY, "-m", "pytest", "tests/", "--collect-only", "-q", "-p", "no:cacheprovider"]); print("collect-only items:", sum(1 for l in r.stdout.splitlines() if "::" in l))
for f in ("reviews/R6_REQUEST.md", "WORKING_STATE.md"): print(f, "'86 passed' lines:", [i + 1 for i, l in enumerate((BMS / f).read_text(encoding="utf-8").splitlines()) if "86 passed" in l])
print("last commit touching R6_REQUEST.md:", sh(["git", "log", "-1", "--format=%h", "--", "bms-balancing/reviews/R6_REQUEST.md"], cwd=REPO).stdout.strip(), "| test_u13 added in 1049894:", "test_u13" in sh(["git", "show", "1049894", "--", "bms-balancing/tests/test_review_findings.py"], cwd=REPO).stdout)
print(".gitignore has .lock:", ".lock" in (BMS / ".gitignore").read_text(encoding="utf-8"), "| .lock files left by this script's verify runs:", sorted(p.name for p in OUT.glob("*.lock")))
print("git_provenance untracked handling:", [l.strip()[:80] for l in (BMS / "scripts/provenance.py").read_text(encoding="utf-8").splitlines() if "untracked" in l])
