"""Verify immutable inputs and package review artifacts, never editing sources."""
from pathlib import Path
import hashlib
import json
import os
import zipfile

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "lhs214s_recheck_20261019"


def native(path):
    p = str(path.resolve())
    return Path("\\\\?\\" + p) if os.name == "nt" and not p.startswith("\\\\?\\") else Path(p)


def read(path):
    return native(path).read_bytes()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(root):
    manifest = json.loads(read(root / "source_manifest.json"))
    problems, paths = [], set()
    for row in manifest["files"]:
        rel = row["path"]
        paths.add(rel)
        data = read(root / "source" / rel)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if sha(data) != row["sha256"] or blob != row["git_blob"] or len(data) != row["bytes"]:
            problems.append(rel)
    actual = set()
    for folder, dirs, files in os.walk(native(root / "source")):
        for name in files:
            actual.add(Path(folder, name).relative_to(native(root / "source")).as_posix())
    tree = json.loads(read(root / "evidence/tree.json"))
    blobs = {r["path"]: r["sha"] for r in tree["tree"] if r["type"] == "blob"}
    extras = []
    for rel in sorted(actual - paths):
        data = read(root / "source" / rel)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        extras.append(dict(path=rel, bytes=len(data), sha256=sha(data),
                           matches_pin_blob=blobs.get(rel) == blob,
                           in_pin_tree=rel in blobs))
    return dict(pin=manifest["pin"], files=len(paths), changed=problems,
                extra_files=extras, missing_files=sorted(paths - actual))


integrity = {"baseline": verify(BASE), "current": verify(ROOT)}
assert all(not v["changed"] and not v["missing_files"] for v in integrity.values()), integrity
assert not integrity["current"]["extra_files"], "New review snapshot gained unmanifested files"
(ROOT / "evidence/final_integrity.json").write_text(json.dumps(integrity, indent=2), encoding="utf8")

entries = {}


def include(path, arc=None):
    entries[arc or path.relative_to(ROOT).as_posix()] = read(path)


for rel in ("codex_review_lhs214cx_fix_recheck_20261020.md", "README.md",
            "source_manifest.json", "intake.py", "package_review.py"):
    include(ROOT / rel)
for top in ("submitted", "probes", "evidence"):
    for folder, dirs, files in os.walk(native(ROOT / top)):
        dirs[:] = [d for d in dirs if d not in ("tmp", "__pycache__")]
        for name in files:
            p = Path(folder, name)
            arc = p.relative_to(native(ROOT)).as_posix()
            if p.suffix != ".pyc":
                include(p, arc)
include(BASE / "source_manifest.json", "baseline_review/source_manifest.json")
include(BASE / "codex_review_lhs214s_fix_recheck_20261019.md",
        "baseline_review/codex_review_lhs214s_fix_recheck_20261019.md")

source_paths = [
    "AGENTS.md",
    "scripts/supp20_input_receipt.py",
    "scripts/test_l214r_r01_restored_full.py",
    "scripts/test_lhs214_model_limit.py",
    "scripts/test_l214r02_model_limit_flag.py",
    "scripts/network_conductivity.py",
    "scripts/tau_flux.py",
    "scripts/run_network_194_parallel.py",
    "scripts/lhs_release_build.py",
    "docs/reviews/selftest_inventory.tsv",
    "docs/reviews/lhs_network_batch_registration_20261007_g2.md",
    "docs/reviews/lhs_network_batch_registration_20261012_supp20.md",
    "docs/reviews/codex_lhs214cx_fix_recheck_request_20261019.md",
    "docs/reviews/lhs214cx_fix_evidence_20261019/s02/README.md",
    "docs/reviews/lhs214cx_fix_evidence_20261019/s06/README.md",
]
for rel in source_paths:
    include(ROOT / "source" / rel, "source_review/" + rel)
for rel in ("scripts/supp20_input_receipt.py", "scripts/test_l214r_r01_restored_full.py"):
    include(BASE / "source" / rel, "baseline_review/" + rel)

manifest = {name: dict(bytes=len(data), sha256=sha(data)) for name, data in sorted(entries.items())}
entries["CONTENTS_SHA256.json"] = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf8")
out = ROOT / "codex_lhs214cx_fix_recheck_20261020.zip"
with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, data in sorted(entries.items()):
        z.writestr(name, data)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert len(z.namelist()) == len(set(z.namelist())) == len(entries)
    for name, row in manifest.items():
        data = z.read(name)
        assert len(data) == row["bytes"] and sha(data) == row["sha256"]
receipt = dict(file=out.name, bytes=out.stat().st_size, sha256=sha(read(out)),
               entries=len(entries), content_hashes_verified=len(manifest), crc="PASS",
               source_integrity=integrity)
(ROOT / "delivery_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf8")
print(json.dumps({k: v for k, v in receipt.items() if k != "source_integrity"}))
print(json.dumps({k: dict(files=v["files"], changed=len(v["changed"]), missing=len(v["missing_files"]),
                         extras=len(v["extra_files"]), extras_pin_matched=sum(x["matches_pin_blob"] for x in v["extra_files"]))
                  for k, v in integrity.items()}))
