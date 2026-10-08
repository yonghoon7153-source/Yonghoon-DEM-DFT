"""Launch one probe under `python3 -I -B` with this container's user site added.

Usage: python3 -I -B mv_probe_launcher.py /abs/path/to/probe.py
Isolated mode keeps the script dir, cwd and PYTHON* env out of sys.path, but
it also drops the user site-packages, where this container's pandas finds its
required python-dateutil.  The user site (our own environment, not the ZIP)
is inserted at the position it has in normal mode, then the probe runs via
runpy.run_path (a file path is not added to sys.path).
"""
import runpy
import site
import sys

probe = sys.argv[1]
user_site = site.getusersitepackages()
try:
    pos = sys.path.index("/usr/local/lib/python3.11/dist-packages")
except ValueError:
    pos = len(sys.path)
if user_site not in sys.path:
    sys.path.insert(pos, user_site)
sys.argv = [probe]
runpy.run_path(probe, run_name="__main__")
