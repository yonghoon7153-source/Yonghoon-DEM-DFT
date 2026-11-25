import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
E = setup(os.path.join(SCR, "..", "T_p7"))
# c1 stalls; c2 would be next. Simulate 'c2 prep failed' (e.g. disk full while copying the 6.8 GB WAVECAR): c2 folder with input copies only.
w, rc, log = run_pkg(E, "p7", {"A5": "conv", "c1": "plateau", "c2": "conv"})
r, ex = chk(E, w)
c2 = os.path.join(ex, "run", B.JOB + "_c2"); shutil.rmtree(c2)
os.makedirs(c2)
for f in ("INCAR", "POSCAR", "KPOINTS", "POTCAR.titel", "POTCAR.sha256", "POTCAR.species.sha256"):
    src = os.path.join(ex, "run", B.JOB + "_c1", f)
    shutil.copy(src, c2) if f != "INCAR" else shutil.copy(os.path.join(E["pkg"], "jobs", B.JOB, "INCAR.a5c2"), os.path.join(c2, "INCAR"))
res = B.check_return(E["pkg"], ex, E["msha"], E["reg"])[1]
print("c2 prep-failed: check", res["status"], "| c2", res["attempts"]["c2"]["status"], "| viol", res["ladder_violations"])
a = adopt(res); print("   adopt ->", a.get("adopted"), a.get("a5_rule"))
# c1 prep failed, c2 never created
c1 = os.path.join(ex, "run", B.JOB + "_c1")
for f in os.listdir(c1):
    if f not in ("INCAR", "POSCAR", "KPOINTS", "POTCAR.titel", "POTCAR.sha256", "POTCAR.species.sha256"):
        os.remove(os.path.join(c1, f))
shutil.copy(os.path.join(E["pkg"], "jobs", B.JOB, "INCAR.a5c1"), os.path.join(c1, "INCAR"))
shutil.rmtree(c2)
res = B.check_return(E["pkg"], ex, E["msha"], E["reg"])[1]
print("c1 prep-failed: check", res["status"], "| c1", res["attempts"]["c1"]["status"])
a = adopt(res); print("   adopt ->", a.get("adopted"), "| note:", a.get("a5_note"))
print("W0 original unchanged across all probes:", B._sha(E["w0p"]) == E["w0"]["sha256"])
