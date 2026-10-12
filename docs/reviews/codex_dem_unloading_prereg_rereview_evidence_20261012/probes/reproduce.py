"""Offline recheck of document-review evidence; never runs DEM or project code.

Run from any directory: python -X utf8 -B probes/reproduce.py
Writes only this review's evidence/reproduction.json.
"""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_manifest(name, folder):
    obj = json.loads((ROOT / name).read_text(encoding="utf-8-sig"))
    verified = 0
    for entry in obj["files"]:
        content = (ROOT / folder / entry["path"]).read_bytes()
        assert sha(content) == entry["sha256"], entry["path"]
        assert len(content) == entry["bytes"], entry["path"]
        if "blob_sha" in entry:
            blob = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
            assert blob == entry["blob_sha"], entry["path"]
        verified += 1
    return {"pin": obj["pin"], "verified_files": verified}


checks = {}
for stem, script in [("state", "ulr_state.py"), ("observers", "ulr_observers.py")]:
    result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "probes" / script)],
                            capture_output=True, text=True, encoding="utf-8", check=True)
    actual = json.loads(result.stdout)
    saved = json.loads((ROOT / "evidence" / f"{stem}.json").read_text(encoding="utf-8-sig"))
    assert actual == saved, stem
    checks[stem] = {"returncode": result.returncode, "saved_json_equal": True, "stderr": result.stderr}

receipt = json.loads((ROOT / "evidence/pin_receipt.json").read_text(encoding="utf-8-sig"))
attached = {}
for short, repo in [
    ("prereg.md", "docs/reviews/dem_unloading_ps45_prereg_20261009.md"),
    ("request.md", "docs/reviews/codex_dem_unloading_prereg_rereview_request_20261011.md"),
]:
    data = (ROOT / "submitted" / short).read_bytes()
    assert data == (ROOT / "source" / repo).read_bytes()
    assert sha(data) == receipt["attachment_sha256"][short]
    attached[short] = {"sha256": sha(data), "equals_pinned_source": True}

schedule = {
    "independent_R_end": 3600000 + 2000,
    "main_extension_end": 3600000 + 60000,
    "S0_prime": 3650000,
    "S0_prime_window": [3650000 - 5000, 3650000 + 5000],
    "optional_extension_end": 3660000 + 50000,
    "S0_double_prime": 3700000,
    "S0_double_prime_window": [3700000 - 5000, 3700000 + 5000],
    "S0_prime_mod_contact_cadence_10000": 3650000 % 10000,
    "main_end_mod_restart_cadence_50000": 3660000 % 50000,
}
assert schedule["S0_prime_window"][1] < schedule["main_extension_end"]
assert schedule["S0_double_prime_window"][1] < schedule["optional_extension_end"]
assert schedule["S0_prime_mod_contact_cadence_10000"] == 0
assert schedule["main_end_mod_restart_cadence_50000"] == 10000

report = {
    "purpose": "document-review finite arithmetic and evidence-integrity checks only",
    "DEM_or_MPM_executed": False,
    "project_modules_imported": False,
    "runtime": {"python": sys.version, "platform": platform.platform()},
    "probe_results": checks,
    "attachments": attached,
    "source": verify_manifest("source_manifest.json", "source"),
    "upstream": verify_manifest("upstream_manifest.json", "upstream"),
    "schedule": schedule,
    "result": "PASS",
    "limitations": [
        "PASS is not a DEM result, kit execution, or production-release verdict.",
        "Synthetic decision examples are not a tested implementation of the not-yet-built kit.",
        "Hash checks establish the reviewed files, not scientific correctness.",
    ],
}
(ROOT / "evidence/reproduction.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
