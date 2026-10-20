"""Capture isolated generation probe failure and dependency-only positive control."""
from pathlib import Path
import json
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parser_audit as a

original_run = a.sr.NP.subprocess.run
captures = []
dependency_adapter = False


def capture(argv, *args, **kwargs):
    if isinstance(argv, (tuple, list)) and argv and str(argv[0]).lower() == "git":
        raise AssertionError("Git commands prohibited")
    is_probe = isinstance(argv, list) and len(argv) > 4 and argv[1:4] == ["-I", "-B", "-c"] and argv[4] == a.sr.NP.GEN_PROBE
    if is_probe and dependency_adapter:
        argv = list(argv)
        argv[4] = "import sys; sys.path[:0] = " + repr(list(map(str, a.DEPS))) + "\n" + argv[4]
    result = original_run(argv, *args, **kwargs)
    if is_probe:
        captures.append(dict(dependency_adapter=dependency_adapter, returncode=result.returncode,
                             stdout=result.stdout, stderr=result.stderr, executable=argv[0],
                             flags=argv[1:4], cwd=kwargs.get("cwd")))
    return result


with patch.object(a.sr.NP.subprocess, "run", capture):
    raw = a.sr.NP.derive_generation(a.sr.NP.ROOT)
    dependency_adapter = True
    adapted = a.sr.NP.derive_generation(a.sr.NP.ROOT)
a.save("generation_environment.json", dict(raw=raw, dependency_path_only=adapted, subprocesses=captures,
       note="git_info is never called by derive_generation; this contrast changes only isolated child sys.path."))
print(json.dumps(dict(raw_error=raw.get("error"), raw_generation=raw.get("generation"),
                      adapted_error=adapted.get("error"), adapted_generation=adapted.get("generation"))))
