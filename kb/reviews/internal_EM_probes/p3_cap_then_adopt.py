import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
# cap 0.001 h = 3.6 s; wrapper makes c1 take ~5 s so A5 + c1 exceed the cap before c2
E = setup(os.path.join(SCR, "..", "T_p3"), cap_h=0.001)
wrap = os.path.join(E["T"], "slow_vasp.sh")
B._write(wrap, f'#!/bin/bash\ncase "$(basename "$PWD")" in *_c1) sleep 5;; esac\nexec {PY} -B {E["fake"]}\n'); os.chmod(wrap, 0o755)
w, rc, log = run_pkg(E, "p3", {"A5": "conv", "c1": "plateau", "c2": "conv"}, vasp_cmd=wrap)
print("rc", rc, "dirs", dirs(w))
print("\n".join(l for l in log.splitlines() if any(k in l for k in ("상한", "⏸", "c1 →", "▶ c2"))))
r, _ = chk(E, w)
print("check:", r["status"], "|", r["why"][:140], "| violations", r["ladder_violations"])
print("c1:", r["attempts"]["c1"]["status"], r["attempts"]["c1"].get("secondary"), r["attempts"]["c1"].get("completeness"))
a = adopt(r)
print("adopt_a5 ->", a.get("adopted"), a.get("a5_rule"), a.get("labels"), "u_W", a.get("u_W_J_m2"))
