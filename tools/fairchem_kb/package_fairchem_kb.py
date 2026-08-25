#!/usr/bin/env python3
"""Create a deterministic, public-safe Fair-Chem knowledge ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import zipfile
from pathlib import Path
from typing import Any


RELEASE_ID = "fairchem_official_kb_2026_08_21"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
ALLOWED_SUFFIXES = {".md", ".json", ".csv", ".py"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def selected_files(repo_root: Path) -> list[Path]:
    roots = [
        repo_root / "kb" / "fairchem",
        repo_root / "db" / "knowledge" / "fairchem",
        repo_root / "tools" / "fairchem_kb",
    ]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            raise FileNotFoundError(root)
        files.extend(
            path
            for path in root.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix.lower() != ".pyc"
        )
    readme = repo_root / "docs" / "reviews" / f"{RELEASE_ID}_README.md"
    if not readme.exists():
        raise FileNotFoundError(readme)
    files.append(readme)
    files = sorted(set(files), key=lambda p: p.relative_to(repo_root).as_posix())
    for path in files:
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            raise ValueError(f"Public bundle contains disallowed file type: {path}")
        lowered = path.name.lower()
        if any(token in lowered for token in ("token", "checkpoint", "trajectory", "password", "secret")):
            raise ValueError(f"Public bundle filename triggers sensitive-artifact guard: {path}")
    return files


def file_status(rel: str) -> str:
    if rel.startswith("db/knowledge/fairchem/"):
        return "generated_machine_index_or_curated_registry"
    if rel.startswith("tools/fairchem_kb/"):
        return "project_builder_or_curated_seed"
    return "project_authored_documentation"


def build(repo_root: Path) -> tuple[Path, Path]:
    repo_root = repo_root.resolve()
    snapshot_path = repo_root / "db" / "knowledge" / "fairchem" / "snapshot.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    prefix = f"{RELEASE_ID}_{snapshot['source_commit'][:8]}"
    files = selected_files(repo_root)

    entries: list[dict[str, Any]] = []
    payloads: list[tuple[str, bytes]] = []
    for path in files:
        rel = path.relative_to(repo_root).as_posix()
        data = path.read_bytes()
        archive_path = f"{prefix}/{rel}"
        payloads.append((archive_path, data))
        entries.append(
            {
                "repo_path": rel,
                "archive_path": archive_path,
                "bytes": len(data),
                "sha256": sha256(data),
                "mime_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "status": file_status(rel),
                "license_scope": "project-authored metadata/documentation; upstream source remains linked, not copied",
            }
        )

    manifest = {
        "schema_version": "fairchem-kb-release-v1",
        "release_id": RELEASE_ID,
        "bundle_prefix": prefix,
        "generated_at": "2026-08-21T00:00:00+00:00",
        "official_source": snapshot["official_repo"],
        "official_source_commit": snapshot["source_commit"],
        "official_source_commit_time": snapshot["source_commit_time"],
        "knowledge_schema_version": snapshot["schema_version"],
        "payload_count": len(entries),
        "payload_bytes": sum(item["bytes"] for item in entries),
        "files": entries,
        "excluded": [
            {"kind": "official source file contents", "reason": "indexed by path/hash/link rather than redistributed"},
            {"kind": "pretrained checkpoints", "reason": "gated external artifacts with separate licenses"},
            {"kind": "Hugging Face datasets", "reason": "large external payloads and separate licenses"},
            {"kind": "paper PDFs and cropped figures", "reason": "managed locally in litdb; redistribution rights vary"},
            {"kind": "tokens, credentials and server-only paths", "reason": "security and portability"},
            {"kind": "raw trajectories", "reason": "not needed for this source-knowledge bundle"}
        ],
        "coverage_contract": snapshot["coverage_contract"],
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    payloads.append((f"{prefix}/manifest.json", manifest_bytes))

    out_dir = repo_root / "docs" / "reviews"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / f"{RELEASE_ID}_MANIFEST.json"
    zip_path = out_dir / f"{RELEASE_ID}.zip"
    manifest_path.write_bytes(manifest_bytes)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for archive_path, data in sorted(payloads):
            info = zipfile.ZipInfo(archive_path, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    digest_path = out_dir / f"{RELEASE_ID}.zip.sha256"
    digest_path.write_text(f"{sha256(zip_path.read_bytes())}  {zip_path.name}\n", encoding="ascii", newline="\n")
    return zip_path, manifest_path


def validate_zip(zip_path: Path, manifest_path: Path) -> list[str]:
    errors: list[str] = []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {item["archive_path"]: item for item in manifest["files"]}
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            errors.append("duplicate ZIP members")
        for path, meta in expected.items():
            if path not in names:
                errors.append(f"missing ZIP member: {path}")
                continue
            data = archive.read(path)
            if len(data) != meta["bytes"]:
                errors.append(f"byte count mismatch: {path}")
            if sha256(data) != meta["sha256"]:
                errors.append(f"hash mismatch: {path}")
        manifest_member = f"{manifest['bundle_prefix']}/manifest.json"
        if manifest_member not in names:
            errors.append("embedded manifest missing")
        forbidden = (".pt", ".pth", ".pdf", ".png", ".jpg", ".xyz", ".traj")
        if any(name.lower().endswith(forbidden) for name in names):
            errors.append("forbidden payload type present")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    zip_path, manifest_path = build(args.repo_root)
    errors = validate_zip(zip_path, manifest_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2
    print(json.dumps({"zip": str(zip_path), "bytes": zip_path.stat().st_size, "sha256": sha256(zip_path.read_bytes())}, ensure_ascii=False))
    print("Fair-Chem KB package validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
