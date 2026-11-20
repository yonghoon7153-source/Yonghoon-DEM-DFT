import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
E = setup(os.path.join(SCR, "..", "T_p4"))
# (a) operator runs from the parent folder; W0 path relative to that cwd (it exists from there)
rel = os.path.relpath(E["w0p"], E["T"])
print("relative W0 path (exists from cwd):", rel, os.path.exists(os.path.join(E["T"], rel)))
w, rc, log = run_pkg(E, "p4a", {"A5": "conv", "c1": "conv"}, w0path=rel, cwd=E["T"])
j = json.load(open(os.path.join(w, "run", "w0_check.json")))
print("(a) rc", rc, "| w0 verified", j["verified"], "|", j["why"], "| A5 variant", [r[1] for r in status_rows(w)][:1])
# (b) typo in absolute path: silently treated like 'none'
w, rc, log = run_pkg(E, "p4b", {"A5": "crash", "c1": "conv"}, w0path=E["w0p"] + "_typo")
j = json.load(open(os.path.join(w, "run", "w0_check.json")))
print("(b) rc", rc, "| w0 verified", j["verified"], "|", j["why"], "| stages", [(r[1], r[4]) for r in status_rows(w)])
print("   ", [l for l in log.splitlines() if "자격 미달" in l or "⓪" in l][:3])
# (c) operator notices, fixes the path, re-runs
w, rc, log = run_pkg(E, "p4b", {"A5": "crash", "c1": "conv"}, w0path=E["w0p"], fresh=False)
print("(c) rc", rc, "|", log.strip().splitlines()[-1][:160])
