import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
E = setup(os.path.join(SCR, "..", "T_p3b"))
w, rc, log = run_pkg(E, "p3b", {"A5": "conv", "c1": "plateau", "c2": "zero"})
print("rc", rc, "status", [(r[1], r[4], r[8]) for r in status_rows(w)])
p = subprocess.run(["bash", os.path.join(w, "run_a5.sh"), "--infra-abort", "c2", "sched-7", "2026-11-22T00:00:00Z", "node fault"], cwd=w, capture_output=True, text=True)
print("infra-abort c2:", p.returncode, p.stdout.strip()[-100:])
p = subprocess.run(["bash", os.path.join(w, "run_a5.sh")], cwd=w, env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True)
print("PACK_ONLY:", p.returncode, p.stdout.strip()[-80:])
r, _ = chk(E, w)
print("check:", r["status"], "| aborted", r["aborted"], "| violations", r["ladder_violations"])
a = adopt(r)
print("adopt_a5 ->", a.get("adopted"), a.get("a5_rule"), "u_W", a.get("u_W_J_m2"))
