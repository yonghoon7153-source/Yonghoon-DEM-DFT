#!/usr/bin/env python3
"""Executable R11 data-contract counterexamples for bms-balancing at 2add074c.

The target tree is read-only.  All fixtures live in temporary directories.
Run with the bundled Windows Python (numpy/scipy/pandas are needed only for the
producer cases):

  python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
from types import SimpleNamespace


DEFAULT_TARGET = Path(
    r"C:\Users\Administrator\Documents\Codex\2026-08-24\claude-14-gate-code-review-9qkx05-2"
    r"\work\harness-r11-target-wsl\bms-balancing"
)


def _load(target: Path):
    # The desktop runtime intentionally keeps optional scientific wheels in a
    # task-local dependency directory.  Prefer that already-installed copy;
    # this repro never downloads packages.
    task_root = Path(__file__).resolve().parents[1]
    for extra in (task_root / "work" / "gate26-pydeps", task_root / "outputs" / "r9_evidence_pydeps"):
        if extra.is_dir():
            sys.path.insert(0, str(extra))
            break
    sys.path.insert(0, str(target))
    sys.path.insert(0, str(target / "scripts"))
    from bms_balancing import data as D  # noqa: PLC0415
    from bms_balancing import schema as S  # noqa: PLC0415
    return D, S


def _receipt(S, seed: int, prefix: str) -> tuple[dict, str]:
    chars = "123456789abcdef"
    hs = [chars[(seed + i) % len(chars)] * 64 for i in range(4)]
    value = {
        "full_cell": {"path": f"{prefix}/full.xlsx", "sha256": hs[0]},
        "half_cell": {"path": f"{prefix}/half.xlsx", "sha256": hs[1]},
        "literature": {
            "gr": {"path": f"{prefix}/gr.xlsx", "sha256": hs[2]},
            "si": {"path": f"{prefix}/si.csv", "sha256": hs[3]},
        },
    }
    return value, S.inputs_digest(value)


def _matrix_row(S, rid: str, target_receipt: tuple[dict, str], ref_receipt: tuple[dict, str]) -> dict:
    consumed, digest = target_receipt
    ref_consumed, ref_digest = ref_receipt
    row = {k: "1" for k in S.MATRIX_ROW}
    row.update(
        half_cell="GITT",
        si="Li",
        w_dqdv="0",
        run_id=rid,
        inputs_sha=digest,
        ref_inputs_sha=ref_digest,
        consumed_inputs=json.dumps(consumed, sort_keys=True),
        ref_consumed_inputs=json.dumps(ref_consumed, sort_keys=True),
        scale_audit_target="",
        scale_audit_ref="",
        bounds="-",
        ref_bounds="-",
    )
    return row


def _write_signed_matrix(S, directory: Path, rid: str, target_receipt, ref_receipt) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    art = directory / "matrix_100.csv"
    with art.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=S.MATRIX_ROW, lineterminator="\n")
        wr.writeheader()
        wr.writerow(_matrix_row(S, rid, target_receipt, ref_receipt))
    meta = {
        "artifact": art.name,
        "state": "100",
        "half_cell_source": "GITT",
        "si_source": "Li",
        "starts": 24,
        "seed": 0,
        "run_id": rid,
        "sha256": hashlib.sha256(art.read_bytes()).hexdigest(),
        "env": {"python": "3.12.3", "numpy": "2.5.3", "scipy": "1.18.1", "platform": "fixture"},
        "started_utc": "2026-09-13T00:00:00+00:00",
        "git_commit_at_start": "0" * 40,
        "git_state_changed_during_run": False,
    }
    (directory / (art.name + ".meta.json")).write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return art


def case_receipt_identity_not_compared(target: Path, S) -> dict:
    """Different valid input bytes still receive promotion_eligible:true."""
    with tempfile.TemporaryDirectory(prefix="r11-receipt-") as td:
        root = Path(td)
        old, new = root / "old", root / "new"
        old_t, old_r = _receipt(S, 0, "old-target"), _receipt(S, 4, "old-ref")
        new_t, new_r = _receipt(S, 8, "new-target"), _receipt(S, 11, "new-ref")
        _write_signed_matrix(S, old, "same-run-id", old_t, old_r)
        _write_signed_matrix(S, new, "same-run-id", new_t, new_r)
        cmd = [sys.executable, str(target / "scripts" / "check_u14.py"), "--new", str(new), "--old", str(old)]
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        p = subprocess.run(
            cmd, cwd=target, text=True, encoding="utf-8", errors="replace",
            capture_output=True, timeout=120, env=env,
        )
        promotion_line = next((x for x in p.stdout.splitlines() if x.startswith("PROMOTION ")), "")
        promotion = json.loads(promotion_line[len("PROMOTION "):]) if promotion_line else None
        return {
            "command": cmd,
            "returncode": p.returncode,
            "promotion": promotion,
            "old_target_digest": old_t[1],
            "new_target_digest": new_t[1],
            "old_ref_digest": old_r[1],
            "new_ref_digest": new_r[1],
            "all_four_digests_changed": len({old_t[1], new_t[1], old_r[1], new_r[1]}) == 4,
            "stdout_tail": p.stdout.splitlines()[-12:],
            "stderr": p.stderr,
        }


def case_receipt_path_and_role_collisions(S) -> dict:
    base, digest = _receipt(S, 0, "actual")
    swapped_paths = json.loads(json.dumps(base))
    swapped_paths["full_cell"]["path"], swapped_paths["half_cell"]["path"] = (
        swapped_paths["half_cell"]["path"],
        swapped_paths["full_cell"]["path"],
    )
    duplicate = json.loads(json.dumps(base))
    duplicate["literature.gr"] = {
        "path": "conflicting/direct-gr.xlsx",
        "sha256": "f" * 64,
    }
    duplicate_digest = S.inputs_digest(duplicate)
    return {
        "base_digest": digest,
        "path_swapped_digest": S.inputs_digest(swapped_paths),
        "path_swap_validate_problems": S.validate_receipt(swapped_paths, digest, "path-swap"),
        "duplicate_flattened_role_leaves": [role for role, _ in S.receipt_leaves(duplicate)],
        "duplicate_role_validate_problems": S.validate_receipt(duplicate, duplicate_digest, "duplicate-role"),
    }


class _FakeObjective:
    scale_audit = None
    c_cell = 1.0
    n_scale_samples = 50
    scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}

    def __init__(self, S, tag="fixture"):
        self.consumed_inputs, self.inputs_sha = _receipt(S, 1, tag)

    def __call__(self, _p):
        return 1.0

    def rmse_pocv(self, _p):
        return 1.0


def _simple_csv_writer(dest, rows, keys):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=keys, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


@contextlib.contextmanager
def _patched(obj, **changes):
    old = {k: getattr(obj, k) for k in changes}
    try:
        for k, v in changes.items():
            setattr(obj, k, v)
        yield
    finally:
        for k, v in old.items():
            setattr(obj, k, v)


def _run_fake_matrix(target: Path, S, *, state: str, only_source: bool, only_wdqdv: bool, make_files: list[tuple[str, str]]) -> dict:
    import numpy as np  # noqa: PLC0415
    from bms_balancing import verify  # noqa: PLC0415

    with tempfile.TemporaryDirectory(prefix="r11-matrix-") as td:
        root = Path(td) / "data-root"
        (root / "data" / "literature").mkdir(parents=True, exist_ok=True)
        created = []
        for source, st in make_files:
            p = verify.D.half_cell_path(root, source, st)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"present measurement")
            created.append(str(p))
        out = Path(td) / f"matrix_{state}.csv"
        args = SimpleNamespace(
            data_root=str(root), source="GITT", state=state, si_source="Li", w_dqdv=0.0,
            starts=1, seed=0, only_source=only_source, only_wdqdv=only_wdqdv,
            out=str(out), run_id="matrix-r11",
        )

        def fake_build(_root, hc, st, si, **_kwargs):
            return _FakeObjective(S, f"{hc}-{st}-{si}")

        def fake_multistart(_obj, **_kwargs):
            return np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []

        buf = io.StringIO()
        with _patched(
            verify,
            build=fake_build,
            multistart=fake_multistart,
            degradation_modes=lambda *_a, **_k: {"LAM_PE": 0.01, "LAM_NE": 0.02, "LLI": 0.03},
            atomic_write_csv=_simple_csv_writer,
        ), contextlib.redirect_stdout(buf):
            rc = verify.cmd_matrix(args)
        rows = list(csv.DictReader(out.open(encoding="utf-8"))) if out.is_file() else []
        summary_line = next((x for x in buf.getvalue().splitlines() if x.startswith("SUMMARY ")), "")
        summary = json.loads(summary_line[len("SUMMARY "):]) if summary_line else None
        return {
            "returncode": rc,
            "canonical_written": out.is_file(),
            "canonical_path": str(out),
            "rows": len(rows),
            "half_cell_sources_in_rows": sorted({r["half_cell"] for r in rows}),
            "input_files_present_during_run": created,
            "summary": summary,
            "stdout_key_lines": [
                x for x in buf.getvalue().splitlines()
                if x.startswith("SUMMARY ") or x.startswith("wrote ")
            ],
        }


def case_allowlisted_measurement_still_excluded(target: Path, D, S) -> dict:
    declared = D.declared_states("GITT")
    result = _run_fake_matrix(
        target,
        S,
        state="300_0147",
        only_source=False,
        only_wdqdv=False,
        make_files=[("GITT", "300_0147"), ("step_005C", "300_0147")],
    )
    result.update(
        allowlist_entry_present=("GITT", "300_0147") in D.HALF_CELL_ABSENT,
        declared_states=declared,
        present_but_excluded="300_0147" not in declared,
        full_population_if_both_present=2 * len(D.SI_SOURCES) * 2,
    )
    return result


def case_matrix_diagnostic_axes_claim_complete(target: Path, D, S) -> dict:
    result = _run_fake_matrix(
        target,
        S,
        state="100",
        only_source=True,
        only_wdqdv=True,
        make_files=[("GITT", "100"), ("step_005C", "100")],
    )
    result["full_authority_rows"] = 2 * len(D.SI_SOURCES) * 2
    return result


def case_profile_grid_one_claims_complete(target: Path, S) -> dict:
    import numpy as np  # noqa: PLC0415
    from bms_balancing import verify  # noqa: PLC0415

    with tempfile.TemporaryDirectory(prefix="r11-profile-") as td:
        out = Path(td) / "profile_gamma_100_Li.csv"
        args = SimpleNamespace(
            data_root="fixture", source="GITT", state="100", si_source="Li", w_dqdv=0.0,
            starts=1, seed=0, grid=1, profile_scale="global", tol=0.01,
            out=str(out), run_id="profile-r11",
        )

        def fake_multistart(_obj, **_kwargs):
            return np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []

        def fake_minimize(_f, _s, **_kwargs):
            return SimpleNamespace(fun=1.0, x=np.array([1.0, 0.0, 1.0, 0.0]), success=True)

        buf = io.StringIO()
        with _patched(
            verify.D,
            data_root=lambda _x: Path(td),
        ), _patched(
            verify,
            build=lambda *_a, **_k: _FakeObjective(S, "profile"),
            multistart=fake_multistart,
            minimize=fake_minimize,
            degradation_modes=lambda *_a, **_k: {"LAM_PE": 0.01, "LAM_NE": 0.02, "LLI": 0.03},
            atomic_write_csv=_simple_csv_writer,
        ), contextlib.redirect_stdout(buf):
            rc = verify.cmd_profile(args)
        rows = list(csv.DictReader(out.open(encoding="utf-8"))) if out.is_file() else []
        roster = json.loads(rows[0]["gamma_roster"]) if rows else None
        summary_line = next((x for x in buf.getvalue().splitlines() if x.startswith("SUMMARY ")), "")
        summary = json.loads(summary_line[len("SUMMARY "):]) if summary_line else None
        return {
            "returncode": rc,
            "canonical_written": out.is_file(),
            "rows": len(rows),
            "gamma_roster": roster,
            "summary_status": summary.get("status") if summary else None,
            "default_grid_in_wrapper": 21,
            "stdout_key_lines": [
                x for x in buf.getvalue().splitlines()
                if x.startswith("SUMMARY ") or x.startswith("wrote ")
            ],
        }


def case_ne_shape_reader_accepts_typed_error_row(target: Path, S) -> dict:
    """The production ne_shape reader bypasses schema.check_rows.

    A signed matrix row tagged as an error is rejected by the shared validator
    but still supplies gamma_target/ref_gamma to the scientific consumer.
    """
    import ne_shape  # noqa: PLC0415

    with tempfile.TemporaryDirectory(prefix="r11-reader-") as td:
        out = Path(td)
        receipt = _receipt(S, 0, "reader")
        row = _matrix_row(S, "reader-r11", receipt, receipt)
        row["gamma_Si"] = "0.4"
        row["ref_gamma_Si"] = "0.2"
        row["error"] = "optimizer failed"
        art = out / "matrix_100.csv"
        header = [*S.MATRIX_ROW, "error"]
        with art.open("w", newline="", encoding="utf-8") as fh:
            wr = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
            wr.writeheader()
            wr.writerow(row)
        meta = {
            "artifact": art.name,
            "state": "100",
            "run_id": "reader-r11",
            "sha256": hashlib.sha256(art.read_bytes()).hexdigest(),
        }
        (out / (art.name + ".meta.json")).write_text(json.dumps(meta), encoding="utf-8")
        validator_problems = S.check_rows("matrix", [row], header)
        info = ne_shape.fitted_pair_info(out, "100", "GITT", "Li")
        return {
            "shared_validator_rejected": bool(validator_problems),
            "validator_problems": validator_problems,
            "production_reader_returned": info,
            "reader_used_error_row": bool(info and info["gamma_target"] == 0.4 and info["gamma_ref"] == 0.2),
        }


def _as_wsl(path: Path) -> str:
    s = str(path.resolve()).replace("\\", "/")
    if len(s) >= 3 and s[1] == ":":
        return f"/mnt/{s[0].lower()}/{s[3:]}"
    return s


def case_shape_wrapper_accepts_partial_and_reads_stale(target: Path) -> dict:
    """The production function propagates rc=3, but the outer wrapper maps it to rc=0.

    It also selects namespace-wide `ls | head -1`, so the status read for the fresh
    partial result comes from a stale canonical artifact.
    """
    script_text = (target / "scripts" / "run_states.sh").read_text(encoding="utf-8")
    begin = script_text.index("# ══ DEFS BEGIN ══")
    defs = script_text[begin:script_text.index("\nfail=0")]
    with tempfile.TemporaryDirectory(prefix="r11-shape-") as td:
        root = Path(td)
        partial = root / "partial"
        partial.mkdir(parents=True)
        stale = root / "ne_shape_A_Li.csv"
        fresh = partial / "ne_shape_Z_Li.csv"
        stale.write_text("state\n100\n", encoding="utf-8")
        fresh.write_text("state\n100\n", encoding="utf-8")
        (root / (stale.name + ".meta.json")).write_text(json.dumps({"status": "complete"}), encoding="utf-8")
        (partial / (fresh.name + ".meta.json")).write_text(json.dumps({"status": "partial"}), encoding="utf-8")
        wroot = _as_wsl(root)
        body = (
            f"OUT={shlex.quote(wroot)}\nSTARTS=2\nSI=Li\nBMS_DATA_ROOT=synthetic\n"
            + defs
            + f"""
fail=0
shape_rc=0
shape_step {json.dumps(wroot)} bash -c 'exit 3' || shape_rc=$?
case "$shape_rc" in
  0) ;;
  3) say 'OUTER accepted rc3 as nonfailure\\n' ;;
  *) fail=$((fail+1)) ;;
esac
if [ "$fail" -eq 0 ]; then say 'OUTER 전부 통과\\n'; fi
echo SHAPE_RC=$shape_rc
echo FAIL_COUNT=$fail
exit $((fail > 0))
"""
        )
        runner = root / "run.sh"
        runner.write_text(body, encoding="utf-8", newline="\n")
        cmd = ["wsl.exe", "-e", "bash", _as_wsl(runner)]
        env = dict(
            os.environ, OUT=wroot, STARTS="2", SI="Li", BMS_DATA_ROOT="synthetic",
            PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
        )
        p = subprocess.run(
            cmd, cwd=target, env=env, text=True, encoding="utf-8", errors="replace",
            capture_output=True, timeout=120,
        )
        return {
            "command": cmd,
            "returncode": p.returncode,
            "stdout": p.stdout.splitlines(),
            "stderr": p.stderr.splitlines(),
            "stale_status": "complete",
            "fresh_partial_status": "partial",
        }


CASES = {
    "receipt_identity": case_receipt_identity_not_compared,
    "receipt_shape": case_receipt_path_and_role_collisions,
    "allowlist": case_allowlisted_measurement_still_excluded,
    "matrix_subset": case_matrix_diagnostic_axes_claim_complete,
    "profile_grid": case_profile_grid_one_claims_complete,
    "shape_reader": case_ne_shape_reader_accepts_typed_error_row,
    "shape_wrapper": case_shape_wrapper_accepts_partial_and_reads_stale,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    ap.add_argument("--case", choices=["all", *CASES], default="all")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    target = args.target.resolve()
    D, S = _load(target)
    selected = CASES if args.case == "all" else {args.case: CASES[args.case]}
    results = {}
    for name, fn in selected.items():
        try:
            if name == "receipt_identity":
                results[name] = fn(target, S)
            elif name == "receipt_shape":
                results[name] = fn(S)
            elif name in {"allowlist", "matrix_subset"}:
                results[name] = fn(target, D, S)
            elif name == "profile_grid":
                results[name] = fn(target, S)
            elif name == "shape_reader":
                results[name] = fn(target, S)
            else:
                results[name] = fn(target)
        except Exception as exc:  # keep independent cases visible
            results[name] = {"error": f"{type(exc).__name__}: {exc}"}
    payload = {
        "target": str(target),
        "expected_head": "2add074cf0c3ebfaa02b22d2311dd4330f0879b0",
        "code_head": "665c87e1",
        "results": results,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if not any("error" in r for r in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
