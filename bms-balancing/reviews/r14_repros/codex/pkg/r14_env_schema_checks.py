"""Read-only review of ordinary environment-metadata completeness.

Only disposable fixture copies are changed. No source, scientific values,
artifact bytes, hashes, receipts, or original sidecars are modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    target = args.target.resolve()
    output = args.output.resolve()
    fixture_root = Path(tempfile.mkdtemp(prefix="r14_env_schema_", dir=output.parent))
    artifacts = (
        "matrix_100.csv", "profile_gamma_100_Li.csv", "ne_shape_GITT_Li.csv",
        "degeneracy_100_Li.json",
    )
    report = {
        "scope": "Ordinary metadata validation; disposable copies only; no model execution",
        "target": str(target), "fixture_root": str(fixture_root), "cases": [],
    }
    for name in artifacts:
        original = target / "out" / name
        original_meta = original.with_name(name + ".meta.json")
        if not original.is_file():
            report["cases"].append({"artifact": name, "status": "not_present"})
            continue
        original_hashes = {str(p): digest(p) for p in (original, original_meta)}
        meta = json.loads(original_meta.read_text(encoding="utf-8-sig"))
        if not isinstance(meta.get("env"), dict) or not meta["env"].get("python"):
            raise ValueError(f"Expected complete current fixture: {name}")
        for mode in ("complete_env", "python_only_env", "env_missing"):
            directory = fixture_root / name.replace(".", "_") / mode
            directory.mkdir(parents=True)
            copied = directory / name
            copied_meta = directory / original_meta.name
            shutil.copyfile(original, copied)
            shutil.copyfile(original_meta, copied_meta)
            changed = json.loads(original_meta.read_text(encoding="utf-8-sig"))
            if mode == "python_only_env":
                changed["env"] = {"python": changed["env"]["python"]}
            elif mode == "env_missing":
                del changed["env"]
            if mode != "complete_env":
                copied_meta.write_text(json.dumps(changed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            command = [sys.executable, str(target / "scripts/check_u14.py"), "--new", str(directory), "--schema-only"]
            child_env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            result = subprocess.run(command, cwd=target, env=child_env, text=True, capture_output=True, timeout=60)
            promotion_lines = [line[len("PROMOTION "):] for line in result.stdout.splitlines() if line.startswith("PROMOTION ")]
            promotion = json.loads(promotion_lines[-1]) if promotion_lines else None
            report["cases"].append({
                "artifact": name, "mode": mode, "rc": result.returncode,
                "promotion": promotion, "stdout": result.stdout, "stderr": result.stderr,
                "command": command, "fixture_dir": str(directory),
                "artifact_bytes_unchanged": digest(copied) == original_hashes[str(original)],
                "original_artifact_and_sidecar_unchanged": all(digest(Path(p)) == value for p, value in original_hashes.items()),
            })
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "cases": [
        {key: item.get(key) for key in ("artifact", "mode", "rc", "status")}
        for item in report["cases"]
    ]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
