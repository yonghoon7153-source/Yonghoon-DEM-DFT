"""Mutation check for ../check_step1.py: break one rule at a time in a scratch copy; the
checker tests must fail on every mutant.   python3 mutate_check.py   (about a minute)"""
import os
import shutil
import subprocess
import sys
import tempfile

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUTANTS = [
    ("big-row threshold strict", 'fb(r) >= TOL["big_row_fraction"] * fmax',
     'fb(r) > TOL["big_row_fraction"] * fmax'),
    ("P1 tolerance 1e-2", '"P1": 1e-3', '"P1": 1e-2'),
    ("log markers ignored", "        if hits:\n", "        if False:\n"),
    ("contiguity ignored", 'if not abs(r["time"] - k * dt)', 'if False and not abs(r["time"] - k * dt)'),
    ("P2 sign flipped", "abs(syy + ref) / ref", "abs(syy - ref) / ref"),
    ("P4 area ratio inverted", 'abs((r["area"] / A0 - 1)', 'abs((A0 / r["area"] - 1)'),
    ("rc ignored", "    elif rc != 0:\n", "    elif False:\n"),
    ("area_ref integrity off", "if refs and mesh and not", "if False and refs and mesh and not"),
    ("P2 sxx part dropped", 'vy <= TOL["P2_syy"] and vx <= TOL["P2_sxx"]', 'vy <= TOL["P2_syy"]'),
    ("NOT_COMPUTED passes", '{"pass": False, "status": "NOT_COMPUTED"',
     '{"pass": True, "status": "NOT_COMPUTED"'),
]


def skip(d, names):
    return [n for n in names if n == "__pycache__"
            or (n.startswith("run_") and os.path.isdir(os.path.join(d, n)))]


def main():
    killed = 0
    for name, old, new in MUTANTS:
        tmp = tempfile.mkdtemp(prefix="mut_")
        try:
            dst = os.path.join(tmp, "moose_step1")
            shutil.copytree(SRC, dst, ignore=skip)
            p = os.path.join(dst, "check_step1.py")
            with open(p, encoding="ascii") as f:
                text = f.read()
            if text.count(old) != 1:
                print("%-26s NOT APPLIED (pattern count %d)" % (name, text.count(old)))
                continue
            with open(p, "w", encoding="ascii") as f:
                f.write(text.replace(old, new))
            r = subprocess.run([sys.executable, os.path.join(dst, "tests", "test_check_step1.py")],
                               capture_output=True, text=True)
            fails = [l.split()[1] for l in r.stdout.splitlines() if l.startswith("FAIL")]
            killed += bool(fails)
            print("%-26s %s  %s" % (name, "KILLED" if fails else "SURVIVED", " ".join(fails)))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print("mutants killed %d / %d" % (killed, len(MUTANTS)))
    return 0 if killed == len(MUTANTS) else 1


if __name__ == "__main__":
    sys.exit(main())
