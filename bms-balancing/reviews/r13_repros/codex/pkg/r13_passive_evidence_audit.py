"""Read stored R13 evidence and package hashes; never load or execute target code.

Usage: python -B r13_passive_evidence_audit.py --target PATH
Writes a single JSON report to stdout and does not modify the target or output files.
Recorded replay decisions are reported as historical data, not fresh test results.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def report_evidence(directory: Path) -> list[dict]:
    reports = []
    for path in sorted(directory.glob("*.json")):
        item = {"file": path.name}
        try:
            data = read_json(path)
            probes = data.get("probes", {})
            statuses = {key: value.get("상태") for key, value in probes.items()}
            requested = data.get("requested")
            rc_path = path.with_name(path.name + ".rc.txt")
            rc = int(rc_path.read_text(encoding="utf-8").strip())
            item.update(
                valid_json=True,
                recorded_target_head=data.get("target_head"),
                recorded_expected_head=data.get("expected_head"),
                recorded_expected_tree=data.get("expected_tree"),
                recorded_mode=data.get("mode"),
                requested=requested,
                requested_count=len(requested) if isinstance(requested, list) else None,
                observed_keys=list(probes),
                observed_record_count=len(probes),
                requested_equals_observed=(requested == list(probes))
                if isinstance(requested, list) else None,
                status_counts=dict(sorted(Counter(statuses.values()).items())),
                recorded_closed=data.get("closed"),
                recorded_evidence_eligible=data.get("evidence_eligible"),
                recorded_instrument_sealed=data.get("instrument_sealed"),
                recorded_package_digest_ok=data.get("package_digest_ok"),
                recorded_dirty=data.get("dirty"),
                recorded_dirty_paths=data.get("dirty_paths"),
                recorded_rc=rc,
                recorded_rc_reason=data.get("rc_reason"),
                nonclosed_status_records=[
                    {"key": key, "status": status,
                     "recorded_reached": probes[key].get("도달")}
                    for key, status in statuses.items()
                    if status not in ("반례 소멸", "닫힘")
                ],
                recorded_nonzero_child_rcs=[
                    {"key": key, "status": statuses[key], "child_rc": value["child_rc"]}
                    for key, value in probes.items()
                    if value.get("child_rc") not in (None, 0)
                ],
            )
        except (OSError, ValueError, TypeError, AttributeError) as exc:
            item.update(error=f"{type(exc).__name__}: {exc}")
        reports.append(item)
    return reports


def report_package(target: Path, round_name: str) -> dict:
    directory = target / "reviews" / f"{round_name}_repros" / "codex"
    item = {"round": round_name}
    manifests = sorted(directory.glob("*SHA256SUMS*"))
    if len(manifests) != 1:
        return {**item, "error": f"Expected one manifest, found {len(manifests)}"}
    manifest = manifests[0]
    entries, problems, seen = [], [], set()
    for line_no, line in enumerate(manifest.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or not re.fullmatch(r"[0-9a-fA-F]{64}", parts[0]):
            problems.append(f"Malformed manifest line {line_no}")
            continue
        expected, name = parts[0].lower(), parts[1].strip()
        if name.startswith("*"):
            name = name[1:]
        path = (directory / name).resolve()
        if not path.is_relative_to(directory.resolve()):
            problems.append(f"Manifest line {line_no} is outside its package")
            continue
        if name in seen:
            problems.append(f"Duplicate manifest name: {name}")
        seen.add(name)
        if not path.is_file():
            entries.append({"file": name, "status": "missing"})
            problems.append(f"Missing file: {name}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        status = "ok" if actual == expected else "mismatch"
        entries.append({"file": name, "status": status,
                        "expected_sha256": expected, "actual_sha256": actual})
        if status != "ok":
            problems.append(f"Hash mismatch: {name}")
    return {**item, "manifest": manifest.name, "manifest_entries": len(entries),
            "actual_files_including_manifest": sum(p.is_file() for p in directory.iterdir()),
            "all_entries_match": bool(entries) and not problems,
            "problems": problems, "entries": entries}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    args = parser.parse_args()
    target = args.target.resolve()
    evidence = target / "reviews" / "r12_repros" / "replay_ours_after_selfreview"
    if not evidence.is_dir():
        parser.error(f"Stored evidence directory not found: {evidence}")
    reports = report_evidence(evidence)
    packages = [report_package(target, round_name) for round_name in ("r7", "r9", "r10", "r11")]
    out = {"audit_mode": "passive file reads and SHA-256 only",
           "executed_target_or_archived_code": False,
           "target": str(target),
           "limitations": ["No fresh replay, scientific computation, or commit verification.",
                           "Record counts do not imply independent case coverage.",
                           "Recorded closed/eligible/rc fields are historical claims."],
           "reports": reports, "packages": packages}
    print(json.dumps(out, ensure_ascii=True, indent=2))
    return 0 if (len(reports) == 5 and all("error" not in r for r in reports)
                 and all(p.get("all_entries_match") for p in packages)) else 1


if __name__ == "__main__":
    sys.exit(main())
