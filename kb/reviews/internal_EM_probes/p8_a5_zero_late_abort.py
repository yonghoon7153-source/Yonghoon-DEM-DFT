import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
E = setup(os.path.join(SCR, "..", "T_p8"))
w, rc, log = run_pkg(E, "p8", {"A5": "zero", "c1": "conv"})
print("run 1 rc", rc, [(r[1], r[4], r[8]) for r in status_rows(w)])
p = subprocess.run(["bash", os.path.join(w, "run_a5.sh"), "--infra-abort", "A5", "sched-4", "2026-11-22T00:00:00Z", "node fault"], cwd=w, capture_output=True, text=True)
print("late infra-abort A5 (c1 already done):", p.returncode, p.stdout.strip()[-70:])
w, rc, log = run_pkg(E, "p8", {"A5": "conv", "c1": "conv", "c2": "plateau"}, fresh=False)
print("run 2 rc", rc, [(r[1], r[4]) for r in status_rows(w)])
r, _ = chk(E, w)
print("check:", r["status"], "| start", r["start_point"]["from"], "| c1", r["attempts"]["c1"]["status"], "| c2", r["attempts"]["c2"]["status"], "| viol", r["ladder_violations"])
a = adopt(r); print("adopt_a5 ->", a.get("adopted"), a.get("a5_rule"))
