"""Reviewer-authored ZIP/hash/text inspection only; imports standard library only.

No supplied programs are executed, imported, or extracted. Prints JSON to stdout.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import zipfile
import zlib

downloads = Path(r"C:\Users\Administrator\Downloads")
archive = downloads / "GATE93_N2_ORIGINAL_LOGS.zip"
manifest_path = downloads / "GATE93_N2_LOG_MANIFEST.json"
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
archive_bytes = archive.read_bytes()
result = {
    "review_method": "Recipient read-only ZIP, hash, CRC, metadata and text inspection; no supplied code run.",
    "archive": {"path": str(archive), "size": len(archive_bytes), "sha256": hashlib.sha256(archive_bytes).hexdigest()},
    "manifest": {"path": str(manifest_path), "size": len(manifest_bytes), "sha256": hashlib.sha256(manifest_bytes).hexdigest()},
    "manifest_text": manifest_bytes.decode("utf-8"),
    "request_text": (downloads / "GATE94_REQUEST.md").read_text(encoding="utf-8"),
    "entries": [],
}
with zipfile.ZipFile(archive) as z:
    result["zip_testzip_first_bad"] = z.testzip()
    result["zip_comment_hex"] = z.comment.hex()
    names = [i.filename for i in z.infolist()]
    result["duplicate_names"] = sorted({n for n in names if names.count(n) > 1})
    canon = [n.replace("\\", "/").casefold().rstrip("/") for n in names]
    result["casefold_collisions"] = sorted({n for n in canon if canon.count(n) > 1})
    result["manifest_duplicate_paths"] = sorted({m["path"] for m in manifest["files"] if sum(x["path"] == m["path"] for x in manifest["files"]) > 1})
    for i in z.infolist():
        b = z.read(i)
        unix_mode = i.external_attr >> 16
        parts = i.filename.replace("\\", "/").split("/")
        local = struct.unpack_from("<4s5H3I2H", archive_bytes, i.header_offset)
        local_name = archive_bytes[i.header_offset+30:i.header_offset+30+local[-2]]
        local_decoded = local_name.decode("utf-8" if local[2] & 0x800 else "cp437")
        text = b.decode("utf-8")
        lines = text.splitlines()
        matched = [m for m in manifest["files"] if i.filename == m["path"] or i.filename.endswith("/" + m["path"])]
        m = matched[0] if len(matched) == 1 else None
        status = []
        for s in m.get("status_lines", []) if m else []:
            exact = [j+1 for j, line in enumerate(lines) if line == s]
            stripped = [j+1 for j, line in enumerate(lines) if line.strip() == s]
            prefix = [j+1 for j, line in enumerate(lines) if line.strip().startswith(s)]
            status.append({"manifest_text": s, "exact_lines": exact, "stripped_exact_lines": stripped, "prefix_lines": prefix, "classification": "exact" if exact else "whitespace-trimmed" if stripped else "truncated-prefix" if prefix else "NOT_FOUND"})
        result["entries"].append({
            "path": i.filename,
            "size": len(b), "size_declared": i.file_size,
            "compressed_size": i.compress_size,
            "compression": i.compress_type,
            "sha256": hashlib.sha256(b).hexdigest(),
            "git_blob_sha1": hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest(),
            "crc32_actual": f"{zlib.crc32(b) & 0xffffffff:08x}", "crc32_central": f"{i.CRC:08x}",
            "crc_ok": zlib.crc32(b) & 0xffffffff == i.CRC,
            "zip_datetime_non_authoritative": i.date_time,
            "unix_mode_octal": oct(unix_mode), "is_symlink": stat.S_ISLNK(unix_mode),
            "regular_or_directory_mode": stat.S_IFMT(unix_mode) in (0, stat.S_IFREG, stat.S_IFDIR),
            "is_directory": i.is_dir(), "encrypted": bool(i.flag_bits & 1),
            "unsafe_path": i.filename.startswith(("/", "\\")) or any(x in (".", "..") or ":" in x or x.endswith((".", " ")) for x in parts if x) or "\\" in i.filename,
            "local_central_name_equal": local_decoded == i.filename,
            "manifest_path": m["path"] if m else None,
            "manifest_size_equal": len(b) == m["size"] if m else None,
            "manifest_sha256_equal": hashlib.sha256(b).hexdigest() == m["sha256"] if m else None,
            "newline_terminated": b.endswith(b"\n"), "line_count": len(lines),
            "status_lines": status,
            "actual_evidence_lines": [{"line": j+1, "text": line} for j,line in enumerate(lines) if re.search(r"^(?:start |end )?head |^rc=|\bpassed\b|scenario_total|실행한 변이|^★|MISMATCH|n_failed|check.*0|^paired|^grid",line)],
            "text": text,
        })
manifest_set = {m["path"] for m in manifest["files"]}
log_entries = [e for e in result["entries"] if e["path"].endswith(".log")]
result["logs_manifest_exact_set"] = {e["manifest_path"] for e in log_entries} == manifest_set and len(log_entries) == len(manifest_set)
result["archive_entry_count"] = len(result["entries"])
result["log_count"] = len(log_entries)
result["manifest_count"] = len(manifest["files"])
result["uncompressed_bytes"] = sum(e["size"] for e in result["entries"])
print(json.dumps(result, ensure_ascii=False, indent=2))
