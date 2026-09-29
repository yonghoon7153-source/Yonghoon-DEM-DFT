"""Package review-only evidence using an explicit allowlist, then verify it."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
FILES = [
    "README.md", "SOURCES.md", "review.md",
    "bundle_original.md", "bundle_lf.md", "prereg_v22_extracted.md",
    "audit_round8.py", "audit_results.json", "package_evidence.py",
    "baseline/make_mixer_deck.py", "baseline/measure_mixing_index.py",
    "baseline/prior_r7_verdict.md",
]
def sha(data):
    return hashlib.sha256(data).hexdigest()

records = {}
for name in FILES:
    path = ROOT / name
    if not path.is_file():
        raise RuntimeError("Missing evidence: " + name)
    data = path.read_bytes()
    records[name] = {"bytes": len(data), "sha256": sha(data)}

manifest = {
    "schema": "review_evidence_manifest/v1",
    "review": "mixer LH round 8 preregistration",
    "scope": "No DEM, no production edits, no scheduler or real campaign results.",
    "files": records,
    "note": "MANIFEST.json excludes itself to avoid a recursive hash.",
}
(ROOT / "MANIFEST.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
dest = ROOT.parent / "codex_mixer_highbo_round8_prereg_20260929.zip"
members = FILES + ["MANIFEST.json"]
with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in members:
        archive.write(ROOT / name, arcname=name)
with zipfile.ZipFile(dest) as archive:
    assert set(archive.namelist()) == set(members)
    assert len(archive.namelist()) == len(members)
    assert archive.testzip() is None
    for name, expected in records.items():
        data = archive.read(name)
        assert len(data) == expected["bytes"]
        assert sha(data) == expected["sha256"]
    assert archive.read("MANIFEST.json") == (ROOT / "MANIFEST.json").read_bytes()
print(json.dumps({
    "zip": str(dest), "bytes": dest.stat().st_size,
    "sha256": sha(dest.read_bytes()), "entries": len(members),
    "verification": "CRC + exact member set + all file SHA256 PASS",
}, ensure_ascii=False, indent=2))

