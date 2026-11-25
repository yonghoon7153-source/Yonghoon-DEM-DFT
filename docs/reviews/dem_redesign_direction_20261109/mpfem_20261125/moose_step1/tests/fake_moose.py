#!/usr/bin/env python3
"""Test double for moose-opt (block / runner tests only).  It is NOT MOOSE and solves nothing.

It checks what the runner must have prepared (input file, local disk.msh, disk.mesh.json)
and writes out.csv in the column layout of ../step1_disk.i from tests/synthetic.py.
FAKE_MOOSE_MODE: pass (default) | reject | diverge | p1fail
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import synthetic as syn  # noqa: E402


def main(argv):
    if "--version" in argv:
        print("fake-moose test double (not MOOSE)")
        return 0
    mode = os.environ.get("FAKE_MOOSE_MODE", "pass")
    with open(os.environ.get("FAKE_MOOSE_ARGLOG", os.devnull), "a") as f:
        f.write(os.getcwd() + " | " + " ".join(argv) + "\n")
    if "-i" not in argv:
        print("*** ERROR ***\nno input file")
        return 1
    with open(argv[argv.index("-i") + 1], encoding="ascii") as f:
        text = f.read()
    over = dict(a.split("=", 1) for a in argv if "=" in a and not a.startswith("-"))

    def param(name):
        if "Executioner/" + name in over:
            return float(over["Executioner/" + name])
        return float(re.search(r"^\s*%s\s*=\s*(\S+)" % name, text, re.M).group(1))

    if "file = disk.msh" not in text or not os.path.exists("disk.msh"):
        print("*** ERROR ***\nmesh file disk.msh not found next to the input")
        return 1
    with open("disk.mesh.json", encoding="ascii") as f:
        mesh = json.load(f)
    if mode == "reject":
        print("*** ERROR ***\nfake rejection: parameter 'bogus' is not a valid parameter")
        return 1
    end, dt = param("end_time"), param("dt")
    rows = syn.make_rows(end_time=end, dt=dt, A0=mesh["disk_area_mesh_m2"])
    if mode == "p1fail":
        for r in rows[1:]:
            r["F_top_y"] *= 1.01
    stop = None
    if mode == "diverge" and end > 50:
        stop = 50
        rows = rows[:stop + 1]
    for r in rows[1:]:
        print("Time Step %d, time = %g" % (round(r["time"] / dt), r["time"]))
        print(" Solve Converged!")
    syn.write_csv("out.csv", rows)
    if stop:
        print("Time Step %d, time = %g" % (stop + 1, (stop + 1) * dt))
        print(" Solve Did NOT Converge!")
        print("Aborting as solve did not converge and input selected to abort")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
