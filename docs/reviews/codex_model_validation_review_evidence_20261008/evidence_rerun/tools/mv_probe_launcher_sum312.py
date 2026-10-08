"""Diagnostic launcher: run a probe with builtins.sum replaced by an emulation
of CPython 3.12's built-in sum() (Neumaier-compensated float accumulation,
gh-100425).  Used only to test whether the last-ULP differences between
our Python 3.11 rerun and the Codex Python 3.12 evidence come from that change.

Usage: python3 -I -B mv_probe_launcher_sum312.py /abs/path/to/probe.py
"""
import builtins
import math
import runpy
import site
import sys


def sum312(iterable, start=0):
    it = iter(iterable)
    result = start
    if type(result) is int:
        i = result
        for item in it:
            if type(item) is int or type(item) is bool:
                i += item
                continue
            result = i + item
            break
        else:
            return i
    if type(result) is float:
        f, c = result, 0.0
        for item in it:
            if type(item) is float:
                t = f + item
                if abs(f) >= abs(item):
                    c += (f - t) + item
                else:
                    c += (item - t) + f
                f = t
                continue
            if type(item) is int and -(2 ** 63) <= item < 2 ** 63:
                f += float(item)
                continue
            if c and math.isfinite(c):
                f += c
            result = f + item
            break
        else:
            if c and math.isfinite(c):
                f += c
            return f
    for item in it:
        result = result + item
    return result


probe = sys.argv[1]
user_site = site.getusersitepackages()
try:
    pos = sys.path.index("/usr/local/lib/python3.11/dist-packages")
except ValueError:
    pos = len(sys.path)
if user_site not in sys.path:
    sys.path.insert(pos, user_site)
builtins.sum = sum312
sys.argv = [probe]
runpy.run_path(probe, run_name="__main__")
