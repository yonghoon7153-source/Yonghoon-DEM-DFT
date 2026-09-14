"""Ordinary empty-value checks for environment metadata, disposable copies only."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


target = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
source = target / "out/matrix_100.csv"
source_meta = source.with_name(source.name + ".meta.json")
baseline_hashes = {str(p): sha(p) for p in (source, source_meta)}
original = json.loads(source_meta.read_text(encoding="utf-8-sig"))
fixture_root = Path(tempfile.mkdtemp(prefix="r14_env_values_", dir=output.parent))
report = {"target": str(target), "scope": "Only scipy environment value; original scientific artifact bytes and sidecar unchanged", "cases": []}
for label, value in (("complete", original["env"]["scipy"]), ("empty_string", ""), ("null", None), ("spaces", "   "), ("tabs_newlines", "\t\n")):
    fixture = fixture_root / label
    fixture.mkdir()
    shutil.copyfile(source, fixture / source.name)
    candidate_meta = json.loads(source_meta.read_text(encoding="utf-8-sig"))
    candidate_meta["env"]["scipy"] = value
    (fixture / source_meta.name).write_text(json.dumps(candidate_meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    command = [sys.executable, str(target / "scripts/check_u14.py"), "--new", str(fixture), "--schema-only"]
    result = subprocess.run(command, cwd=target, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True, timeout=60)
    lines = [line[10:] for line in result.stdout.splitlines() if line.startswith("PROMOTION ")]
    report["cases"].append({"label": label, "scipy_value": value, "rc": result.returncode,
        "promotion": json.loads(lines[-1]) if lines else None, "stdout": result.stdout, "stderr": result.stderr,
        "command": command, "fixture": str(fixture),
        "artifact_unchanged": sha(fixture/source.name) == baseline_hashes[str(source)]})
report["originals_unchanged"] = all(sha(Path(p)) == digest for p, digest in baseline_hashes.items())
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"output": str(output), "originals_unchanged": report["originals_unchanged"],
    "cases": [{"label": case["label"], "rc": case["rc"], "blocked_by": case["promotion"]["blocked_by"]} for case in report["cases"]]}, ensure_ascii=False, indent=2))
