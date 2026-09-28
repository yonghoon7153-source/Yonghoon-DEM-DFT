"""Package read-only review artifacts and verify every archived byte. No simulation."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "mixer_highbo_round6_evidence_20260928"
REPORT = ROOT / "docs/reviews/codex_review_mixer_highbo_round6_20260928.md"
OUT = ROOT / "codex_mixer_highbo_round6_review_20260928.zip"
MAN = ROOT / "codex_mixer_highbo_round6_review_20260928_manifest.json"
ATTEST = ROOT / "codex_mixer_highbo_round6_review_20260928_attestation.json"
paths = [REPORT, Path(__file__).resolve()]
paths += [p for p in EVIDENCE.rglob("*") if p.is_file() and "__pycache__" not in p.parts
          and p.suffix != ".pyc" and not any(x.startswith("synthetic_") for x in p.parts)]
payload = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in sorted(paths)}
manifest = {"schema": "review_evidence/v1", "pin": "18787ab98a13361c37b2343bd07ae276142d0953",
            "scope": "Review only. Synthetic Python probes, no DEM/MPI/scheduler or real LH/LC frame reads.",
            "files": [{"path": n, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
                      for n,b in payload.items()]}
mraw = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
MAN.write_bytes(mraw)
with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in payload.items():
        info = zipfile.ZipInfo(n, (2026,9,28,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info,b)
    z.writestr("MANIFEST.json",mraw)
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(payload) | {"MANIFEST.json"}
    assert len(z.namelist()) == len(set(z.namelist()))
    assert z.read("MANIFEST.json") == mraw
    for row in manifest["files"]:
        b = z.read(row["path"])
        assert len(b) == row["bytes"] and hashlib.sha256(b).hexdigest() == row["sha256"], row
    # Verify the source mirror inside the archive independently of its filesystem.
    source = json.loads(z.read("mixer_highbo_round6_evidence_20260928/sources.json"))
    for row in source["files"]:
        b = z.read("mixer_highbo_round6_evidence_20260928/" + row["path"])
        got = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        assert got == row["blob_sha"], row
attest = {"schema": "review_archive_check/v1", "pin": manifest["pin"], "files_verified": len(payload),
          "source_blobs_verified": len(source["files"]), "zip_bytes": OUT.stat().st_size,
          "zip_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
          "manifest_sha256": hashlib.sha256(mraw).hexdigest(),
          "report_sha256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
          "verdict": "HOLD",
          "note": "Archive integrity is not validation of future production runs."}
ATTEST.write_text(json.dumps(attest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps(attest, indent=2))

