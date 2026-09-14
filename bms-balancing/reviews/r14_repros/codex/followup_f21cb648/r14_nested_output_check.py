"""Ordinary output-directory classification checks in new disposable Git repos."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    source = args.target.resolve() / "scripts/provenance.py"
    spec = importlib.util.spec_from_file_location("reviewed_provenance", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results = []
    for name, out_root, sibling, expected_dirty in (
        ("shallow_output_only", "out_alt", False, False),
        ("nested_output_only", "reports/out_u18", False, False),
        ("nested_with_sibling", "reports/out_u18", True, True),
    ):
        fixture = (args.output / name).resolve()
        fixture.mkdir()
        def git(*argv):
            return subprocess.check_output(["git", *argv], cwd=fixture, text=True)
        git("init", "-q")
        git("config", "user.name", "Local review fixture")
        git("config", "user.email", "fixture@example.invalid")
        (fixture / "README.txt").write_text("Synthetic output-path classification fixture.\n", encoding="utf-8")
        git("add", "README.txt")
        git("commit", "-qm", "Fixture baseline")
        artifact = fixture / out_root / "matrix_100.csv"
        artifact.parent.mkdir(parents=True)
        artifact.write_text("a,b\n1,2\n", encoding="utf-8")
        if sibling:
            (fixture / "reports/notes.txt").write_text("Outside the declared output root.\n", encoding="utf-8")
        observed = module.git_provenance(cwd=str(fixture), artifact=str(artifact),
                                         output_roots=(out_root, "out"))
        results.append({"case": name, "output_root": out_root, "expected_git_dirty": expected_dirty,
                        "observed": observed, "fixture": str(fixture),
                        "git_status": git("status", "--porcelain", "--untracked-files=normal")})
    (args.output / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
