"""Reproduce R9 mutation-auditor exit-code misclassification without editing the target."""
from __future__ import annotations

import importlib.util
import pathlib
import sys


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: r9_evidence_classify_probe.py <bms-balancing>")
    root = pathlib.Path(sys.argv[1]).resolve()
    path = root / "reviews/r6_repros/codex_r6_mutation_audit.py"
    spec = importlib.util.spec_from_file_location("r9_audit_probe", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    summary = "1 failed, 51 deselected in 1.4s"
    for rc in (1, 2, 3, 4, 5):
        print(f"rc={rc}: {audit.classify(rc, summary)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
