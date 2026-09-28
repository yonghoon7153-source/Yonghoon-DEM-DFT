"""Run stock Python selftest, explicitly stop before its Bash launcher fixtures.

No source edits. Stock Python checks use the production run-status heredoc.
The last two checks invoke a fake simulator through Bash; they are outside this
Python-only execution and are reported as not executed.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
tempfile.tempdir = str(HERE)
sys.path.insert(0, str(HERE.parent / "scripts"))
import mixer_restart_phase_test as pt

class LauncherFixtureNotExecuted(Exception):
    pass

original_run = subprocess.run
def python_only_run(args, *a, **kw):
    if args and args[0] == "bash":
        raise LauncherFixtureNotExecuted("Stopped before Bash/fake-launcher fixtures; no simulator or MPI executed")
    return original_run(args, *a, **kw)

subprocess.run = python_only_run
capture = io.StringIO()
stopped = None
try:
    with contextlib.redirect_stdout(capture):
        returned_rc = pt._selftest()
except LauncherFixtureNotExecuted as e:
    stopped = str(e)
finally:
    subprocess.run = original_run
transcript = capture.getvalue()
(HERE / "phase_selftest_python.txt").write_text(transcript, encoding="utf-8")
result = {"executed_pass": sum(l.startswith("  PASS  ") for l in transcript.splitlines()),
          "executed_fail": sum(l.startswith("  FAIL  ") for l in transcript.splitlines()),
          "unexecuted": ["14 LMP_LAUNCH Bash fixture", "14b plain Bash fixture"],
          "stop": stopped}
(HERE / "phase_selftest_python.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
assert result["executed_pass"] == 28 and result["executed_fail"] == 0, result
