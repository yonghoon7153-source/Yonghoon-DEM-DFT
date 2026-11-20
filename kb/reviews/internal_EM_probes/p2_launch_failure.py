import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
E = setup(os.path.join(SCR, "..", "T_p2"))
# VASP binary missing (typo / module not loaded): command exits 127 at once, writes nothing
w, rc, log = run_pkg(E, "p2", {}, vasp_cmd="vasp_std_typo_not_on_path")
print("rc", rc, "dirs", dirs(w))
print("status.tsv:", [(r[1], r[3], r[4], r[8]) for r in status_rows(w)])
print("\n".join(l for l in log.splitlines() if any(k in l for k in ("자격", "시작점", "c1 →", "c2 →", "▶", "✅", "⚠", "✗", "⛔"))))
r, _ = chk(E, w)
print("check:", r["status"], "|", r["why"][:140])
for k, v in r["attempts"].items():
    print("  ", k, v["status"], (v.get("why") or "")[:110])
a = adopt(r); print("adopt_a5 note:", a.get("a5_note"))
# Operator now tries to record the three 0-step aborts (rule: same stage again, max 2 for the job)
env = dict(os.environ)
for st in ("A5", "c1", "c2"):
    p = subprocess.run(["bash", os.path.join(w, "run_a5.sh"), "--infra-abort", st, "sched-9", "2026-11-21T00:00:00Z", "binary not found"], cwd=w, env=env, capture_output=True, text=True)
    print("infra-abort", st, "rc", p.returncode, p.stdout.strip()[-140:])
