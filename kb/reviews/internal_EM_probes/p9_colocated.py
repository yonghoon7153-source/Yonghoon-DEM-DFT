import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
E = setup(os.path.join(SCR, "..", "T_p9"))
w = os.path.join(E["T"], "w_p9"); shutil.rmtree(w, ignore_errors=True); shutil.copytree(E["pkg"], w)
# round-2 leftovers in the same run/ (finished attempts of other jobs)
for j, el in (("P2S_S_A_bound", 29604), ("V5_s_outer_A_G4_e70_far_a4_a4/stageA", 77758), ("V5_s_outer_A_G4_e70_far_a4_a4", 118347), ("P2S_S_A_far", 700000)):
    d = os.path.join(w, "run", j); os.makedirs(d, exist_ok=True)
    B._write(os.path.join(d, "attempt.json"), json.dumps({"job": j, "rc": 0, "elapsed_s": el}))
    B._write(os.path.join(d, "OUTCAR"), " vasp.5.4.4\n")
w, rc, log = run_pkg(E, "p9", {"A5": "conv", "c1": "conv"}, fresh=False)
print("rc", rc, "| a5 dirs", [x for x in dirs(w) if "a5" in x])
print([l for l in log.splitlines() if "상한" in l][:2])
r, _ = chk(E, w); print("check:", r["status"], "|", r["why"][:100])
