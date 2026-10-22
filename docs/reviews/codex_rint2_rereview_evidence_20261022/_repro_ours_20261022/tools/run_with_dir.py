"""Launcher for `python3 -I` runs of scripts that import siblings (e.g. `from run_review import ...`).

-I omits the script directory from sys.path.  This puts back ONLY that directory (what a
plain `python script.py` would do) and runs the script unchanged as __main__.
Usage: python3 -I -X utf8 -B run_with_dir.py <script.py> [args...]
"""
import os
import runpy
import sys

script = os.path.abspath(sys.argv[1])
sys.argv = [script] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(script))
runpy.run_path(script, run_name='__main__')
