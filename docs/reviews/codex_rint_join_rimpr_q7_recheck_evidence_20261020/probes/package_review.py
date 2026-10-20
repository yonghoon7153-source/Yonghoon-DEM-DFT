"""Package the completed review; verify immutable inputs and every ZIP member."""
from pathlib import Path
import hashlib
import json
import os
import zipfile

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
OLD = WORK / "rint_g2_impl_reverify_20261015"
OUT = WORK / "codex_rint_join_rimpr_q7_recheck_20261020.zip"


def native(path):
    name = str(path.resolve())
    return Path("\\\\?\\" + name) if os.name == "nt" and not name.startswith("\\\\?\\") else Path(name)


def data(path):
    return native(path).read_bytes()


def sha(b):
    return hashlib.sha256(b).hexdigest()


integrity = []
for root in (ROOT, OLD):
    manifest = json.loads(data(root / "source_manifest.json"))
    bad = []
    for entry in manifest["files"]:
        b = data(root / "source" / entry["path"])
        git = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        if sha(b) != entry["sha256"] or len(b) != entry["bytes"] or git != entry["git_blob"]:
            bad.append(entry["path"])
    integrity.append(dict(root=root.name, pin=manifest["pin"], files=len(manifest["files"]), mismatches=bad))
if any(x["mismatches"] for x in integrity):
    raise RuntimeError(integrity)
(ROOT / "evidence/final_source_integrity.json").write_text(
    json.dumps(integrity, ensure_ascii=False, indent=2), encoding="utf8")

chosen = {}


def add(path):
    name = path.relative_to(WORK).as_posix()
    if not name or ".." in Path(name).parts or name.startswith("/"):
        raise ValueError(name)
    chosen[name] = path


for path in ROOT.rglob("*"):
    if path.is_file() and "__pycache__" not in path.parts and path.name not in ("package_receipt.json", "compact_package_receipt.json"):
        add(path)
old_manifest = json.loads(data(OLD / "source_manifest.json"))
add(OLD / "source_manifest.json")
add(OLD / "codex_review_rint_g2_impl_fix_recheck_20261015.md")
for entry in old_manifest["files"]:
    add(OLD / "source" / entry["path"])
for path in (OLD / "tmp/join_independent").rglob("*"):
    if path.is_file():
        add(path)

entries = []
with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, path in sorted(chosen.items()):
        b = data(path)
        z.writestr(name, b)
        entries.append(dict(path=name, bytes=len(b), sha256=sha(b)))
    z.writestr("PACKAGE_MANIFEST.json", json.dumps(
        dict(kind="independent-review-evidence", pin="2b9efa253edbf455c2e1abfef1d60e51818e01f8",
             files=entries), ensure_ascii=False, indent=2).encode("utf8"))

with zipfile.ZipFile(OUT) as z:
    if z.testzip() is not None:
        raise RuntimeError("ZIP CRC mismatch")
    if len(z.namelist()) != len(set(z.namelist())):
        raise RuntimeError("Duplicate ZIP member")
    for entry in entries:
        b = z.read(entry["path"])
        if len(b) != entry["bytes"] or sha(b) != entry["sha256"]:
            raise RuntimeError("Read-back mismatch: " + entry["path"])
receipt = dict(zip=OUT.name, bytes=OUT.stat().st_size, sha256=sha(data(OUT)),
               members=len(entries) + 1, verified_files=len(entries),
               source_integrity=integrity, zip_crc="PASS", member_hashes="PASS")
(ROOT / "evidence/package_receipt.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf8")
print(json.dumps(receipt, ensure_ascii=False, indent=2))

compact = WORK / "codex_rint_join_rimpr_q7_recheck_20261020_review.zip"
light_entries = [x for x in entries if "/source/" not in x["path"]]
with zipfile.ZipFile(OUT) as full, zipfile.ZipFile(
        compact, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for entry in light_entries:
        z.writestr(entry["path"], full.read(entry["path"]))
    z.writestr("PACKAGE_MANIFEST.json", json.dumps(
        dict(kind="compact-review-evidence-without-source", full_package=OUT.name,
             full_package_sha256=receipt["sha256"], files=light_entries),
        ensure_ascii=False, indent=2).encode("utf8"))
with zipfile.ZipFile(compact) as z:
    if z.testzip() is not None or len(z.namelist()) != len(set(z.namelist())):
        raise RuntimeError("Compact ZIP invalid")
    for entry in light_entries:
        b = z.read(entry["path"])
        if len(b) != entry["bytes"] or sha(b) != entry["sha256"]:
            raise RuntimeError("Compact read-back mismatch: " + entry["path"])
light_receipt = dict(zip=compact.name, bytes=compact.stat().st_size,
                     sha256=sha(data(compact)), verified_files=len(light_entries),
                     zip_crc="PASS", member_hashes="PASS", includes_source=False)
(ROOT / "evidence/compact_package_receipt.json").write_text(
    json.dumps(light_receipt, ensure_ascii=False, indent=2), encoding="utf8")
print(json.dumps(light_receipt, ensure_ascii=False, indent=2))
