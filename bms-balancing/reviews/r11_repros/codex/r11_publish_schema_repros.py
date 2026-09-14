#!/usr/bin/env python3
"""R11 adversarial repros for typed publication and check_u14.

Run from the R11 target's Linux environment, for example:

  PYTHONPATH=/tmp/r11-pydeps-publish PYTHONDONTWRITEBYTECODE=1 \
    python3 outputs/r11_publish_schema_repros.py

The target is imported and executed but never modified.  All runtime fixtures live
under a temporary directory and are removed at exit.
"""
from __future__ import annotations

import contextlib
import csv
import hashlib
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest import mock


WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
TARGET = WORKSPACE / "work" / "harness-r11-target-wsl" / "bms-balancing"
sys.path.insert(0, str(TARGET))
sys.dont_write_bytecode = True

from bms_balancing import data as D  # noqa: E402
from bms_balancing import schema as S  # noqa: E402
from bms_balancing import verify  # noqa: E402


def leaf(tag: str) -> dict:
    return {"path": f"/evidence/{tag}.xlsx", "sha256": hashlib.sha256(tag.encode()).hexdigest()}


def receipt(prefix: str) -> dict:
    return {
        "full_cell": leaf(prefix + "-full"),
        "half_cell": leaf(prefix + "-half"),
        "literature": {"gr": leaf(prefix + "-gr"), "si": leaf(prefix + "-si")},
    }


def duplicate_role_receipt(prefix: str) -> dict:
    # The dotted key and nested key both flatten to "literature.gr".
    return {
        "full_cell": leaf(prefix + "-full"),
        "half_cell": leaf(prefix + "-half"),
        "literature.gr": leaf(prefix + "-gr-decoy"),
        "literature": {"gr": leaf(prefix + "-gr-real"), "si": leaf(prefix + "-si")},
    }


ENV = {"python": "3.12", "numpy": "2.5", "scipy": "1.18", "platform": "linux"}


def degeneracy(rid: str, rec: dict | None = None, best_obj=1.0) -> dict:
    rec = rec or receipt("same")
    return {
        "state": "100",
        "si_source": "Li",
        "half_cell": "GITT",
        "w_dqdv": 0.0,
        "tol_percent_of_best": 1.0,
        "n_starts": 24,
        "seed": 0,
        "n_grid": 21,
        "n_samples": 400,
        "run_id": rid,
        "env": dict(ENV),
        "consumed_inputs": rec,
        "ref_consumed_inputs": rec,
        "inputs_sha": S.inputs_digest(rec),
        "n_accepted": 1,
        "best_obj": best_obj,
        "best_p": [1.0, 0.0, 1.0, 0.0, 0.2],
        "ref_p": [1.0, 0.0, 1.0, 0.0, 0.2],
        "best_modes_percent": {"LAM_PE": 0.0, "LAM_NE": 0.0, "LLI": 0.0},
        "LAM_PE_percent": 0.0,
        "LAM_NE_percent": 0.0,
        "LLI_percent": 0.0,
    }


def meta(name: str, rid: str, data: bytes, **updates) -> dict:
    m = {
        "artifact": name,
        "run_id": rid,
        "sha256": hashlib.sha256(data).hexdigest(),
        "env": dict(ENV),
        "started_utc": "2026-09-13T00:00:00+00:00",
        "git_commit_at_start": "665c87e",
        "git_state_changed_during_run": False,
        "state": "100",
        "half_cell_source": "GITT",
        "si_source": "Li",
        "starts": 24,
        "seed": 0,
        "argv": ["python3", "-m", "bms_balancing.verify", "degeneracy", "--state", "100"],
        "roster": {"kind": "degeneracy", "state": "100"},
    }
    m.update(updates)
    return m


def write_json_unit(directory: pathlib.Path, obj: dict, *, meta_updates=None) -> pathlib.Path:
    directory.mkdir(parents=True, exist_ok=True)
    name = "degeneracy_100_Li.json"
    data = (json.dumps(obj, ensure_ascii=False, sort_keys=True, allow_nan=True) + "\n").encode()
    f = directory / name
    f.write_bytes(data)
    m = meta(name, obj["run_id"], data, **(meta_updates or {}))
    f.with_name(name + ".meta.json").write_text(json.dumps(m, ensure_ascii=False) + "\n", encoding="utf-8")
    return f


def matrix_row(rid: str, *, obj="1.0") -> dict:
    rec = receipt("matrix")
    d = {k: "1" for k in S.MATRIX_ROW}
    d.update(
        {
            "half_cell": "GITT",
            "si": "Li",
            "w_dqdv": "0",
            "run_id": rid,
            "inputs_sha": S.inputs_digest(rec),
            "ref_inputs_sha": S.inputs_digest(rec),
            "consumed_inputs": json.dumps(rec),
            "ref_consumed_inputs": json.dumps(rec),
            "scale_audit_target": "",
            "scale_audit_ref": "",
            "obj": obj,
            "bounds": "-",
            "ref_bounds": "-",
        }
    )
    return d


def write_matrix_unit(directory: pathlib.Path, row: dict, *, meta_updates=None) -> pathlib.Path:
    directory.mkdir(parents=True, exist_ok=True)
    f = directory / "matrix_100.csv"
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=list(S.MATRIX_ROW), lineterminator="\n")
    w.writeheader()
    w.writerow(row)
    data = buf.getvalue().encode()
    f.write_bytes(data)
    m = meta(f.name, row["run_id"], data, **(meta_updates or {}))
    f.with_name(f.name + ".meta.json").write_text(json.dumps(m, ensure_ascii=False) + "\n", encoding="utf-8")
    return f


def profile_row(rid: str, *, gamma_roster="not-json") -> dict:
    rec = receipt("profile")
    d = {k: "1" for k in S.PROFILE_ROW}
    d.update(
        {
            "gamma_Si": "0.2",
            "run_id": rid,
            "bounds": "-",
            "profile_scale": "global",
            "inputs_sha": S.inputs_digest(rec),
            "ref_inputs_sha": S.inputs_digest(rec),
            "consumed_inputs": json.dumps(rec),
            "ref_consumed_inputs": json.dumps(rec),
            "gamma_roster": gamma_roster,
        }
    )
    return d


def run_check(*args: os.PathLike | str) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run(
        [sys.executable, str(TARGET / "scripts" / "check_u14.py"), *map(str, args)],
        cwd=TARGET,
        env=env,
        text=True,
        capture_output=True,
    )
    line = next((x for x in p.stdout.splitlines() if x.startswith("PROMOTION ")), "")
    promotion = json.loads(line[len("PROMOTION ") :]) if line else None
    return {"rc": p.returncode, "promotion": promotion, "stdout_tail": p.stdout.splitlines()[-8:], "stderr": p.stderr}


class FakeObjective:
    def __init__(self, tag: str):
        self.c_cell = 1.0
        self.scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}
        self.scale_audit = None
        self.n_scale_samples = 1
        self.consumed_inputs = receipt(tag)
        self.inputs_sha = S.inputs_digest(self.consumed_inputs)

    def __call__(self, _p):
        return 1.0

    def rmse_pocv(self, _p):
        return 0.1

    def _auto_scales(self, *_a, **_k):
        return {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}


def fake_build(_root, source, state, si, **_kwargs):
    return FakeObjective(f"{source}-{state}-{si}")


def fake_multistart(_obj, **_kwargs):
    return verify.np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []


def fake_modes(*_args):
    return {"LAM_PE": 0.0, "LAM_NE": 0.0, "LLI": 0.0}


def publication_repros(tmp: pathlib.Path) -> dict:
    marker = tmp / "half.xlsx"
    marker.write_bytes(b"fixture")
    common = (
        mock.patch.object(verify.D, "data_root", lambda _x=None: tmp),
        mock.patch.object(verify.D, "half_cell_path", lambda *_a, **_k: marker),
        mock.patch.object(verify, "build", fake_build),
        mock.patch.object(verify, "multistart", fake_multistart),
        mock.patch.object(verify, "degradation_modes", fake_modes),
        mock.patch.object(verify, "active_bounds", lambda _p: []),
    )

    for p in common:
        p.start()
    try:
        matrix_out = tmp / "publish" / "matrix_100.csv"
        args = SimpleNamespace(
            data_root=str(tmp),
            source="GITT",
            state="100",
            only_source=True,
            only_wdqdv=True,
            w_dqdv=0.0,
            starts=0,
            seed=0,
            out=str(matrix_out),
            run_id="matrix-filtered",
        )
        matrix_stdout = io.StringIO()
        with contextlib.redirect_stdout(matrix_stdout):
            matrix_rc = verify.cmd_matrix(args)
        with matrix_out.open(encoding="utf-8") as fh:
            matrix_rows = list(csv.DictReader(fh))

        profile_out = tmp / "publish" / "profile_gamma_100_Li.csv"

        def ok_minimize(_f, _s, **_kwargs):
            return SimpleNamespace(fun=1.0, x=verify.np.array([1.0, 0.0, 1.0, 0.0]), success=True)

        pargs = SimpleNamespace(
            data_root=str(tmp),
            source="GITT",
            state="100",
            si_source="Li",
            w_dqdv=0.0,
            starts=0,
            seed=0,
            grid=1,
            tol=0.01,
            profile_scale="global",
            out=str(profile_out),
            run_id="profile-grid-one",
        )
        with mock.patch.object(verify, "minimize", ok_minimize):
            profile_stdout = io.StringIO()
            with contextlib.redirect_stdout(profile_stdout):
                profile_rc = verify.cmd_profile(pargs)
        with profile_out.open(encoding="utf-8") as fh:
            profile_rows = list(csv.DictReader(fh))

        calls = {"n": 0}

        def half_fail_minimize(_f, _s, **_kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                return SimpleNamespace(fun=1.0, x=verify.np.array([1.0, 0.0, 1.0, 0.0]), success=True)
            return SimpleNamespace(fun=float("inf"), x=verify.np.array([1.0, 0.0, 1.0, 0.0]), success=False)

        stdout_args = SimpleNamespace(**vars(pargs))
        stdout_args.grid = 2
        stdout_args.out = None
        stdout_args.run_id = "profile-stdout-partial"
        with mock.patch.object(verify, "minimize", half_fail_minimize):
            partial_stdout = io.StringIO()
            with contextlib.redirect_stdout(partial_stdout):
                partial_rc = verify.cmd_profile(stdout_args)
        summary_line = next(x for x in partial_stdout.getvalue().splitlines() if x.startswith("SUMMARY "))
        partial_summary = json.loads(summary_line[len("SUMMARY ") :])
    finally:
        for p in reversed(common):
            p.stop()

    expected_full_matrix = len(D.HALF_FILE) * len(D.SI_SOURCES) * 2
    return {
        "matrix_filtered_canonical": {
            "rc": matrix_rc,
            "canonical_exists": matrix_out.is_file(),
            "rows": len(matrix_rows),
            "full_authority_rows": expected_full_matrix,
            "only_half_cells": sorted({r["half_cell"] for r in matrix_rows}),
            "only_weights": sorted({r["w_dqdv"] for r in matrix_rows}),
        },
        "profile_grid1_canonical": {
            "rc": profile_rc,
            "canonical_exists": profile_out.is_file(),
            "rows": len(profile_rows),
            "gamma_roster": json.loads(profile_rows[0]["gamma_roster"]),
        },
        "profile_partial_stdout": {
            "rc": partial_rc,
            "reported_status": partial_summary["status"],
            "gamma_roster": partial_summary["gamma_roster"],
            "out_was_none": True,
        },
    }


def checker_repros(tmp: pathlib.Path) -> dict:
    out = {}

    # A complete, valid unit still advertises promotion under --schema-only,
    # where there is no baseline, no roster pairing, and no numeric comparison.
    schema = tmp / "schema-only"
    write_json_unit(schema, degeneracy("schema-only"))
    out["schema_only_no_baseline"] = run_check("--new", schema, "--schema-only")

    # In schema-only mode, env/control/argv are also skipped.  META_KEYS only
    # requires env to be non-null, so {} is accepted; controls and argv may vanish.
    weak = tmp / "schema-only-weak-meta"
    f = write_json_unit(weak, degeneracy("weak-meta"), meta_updates={"env": {}})
    mp = f.with_name(f.name + ".meta.json")
    m = json.loads(mp.read_text(encoding="utf-8"))
    for k in ("state", "half_cell_source", "si_source", "starts", "seed", "argv", "roster"):
        m.pop(k, None)
    mp.write_text(json.dumps(m) + "\n", encoding="utf-8")
    out["schema_only_skips_env_controls_argv"] = run_check("--new", weak, "--schema-only")

    # Full comparison also does not require or validate argv/roster.
    argv_old, argv_new = tmp / "argv-old", tmp / "argv-new"
    write_json_unit(argv_old, degeneracy("argv-old"))
    nf = write_json_unit(argv_new, degeneracy("argv-new"))
    nmp = nf.with_name(nf.name + ".meta.json")
    nm = json.loads(nmp.read_text(encoding="utf-8"))
    nm.pop("argv", None)
    nm.pop("roster", None)
    nmp.write_text(json.dumps(nm) + "\n", encoding="utf-8")
    out["full_compare_missing_argv_and_roster"] = run_check("--new", argv_new, "--old", argv_old)

    # The flag exists specifically to say the checkout changed during the run,
    # but its value is never consumed by check_u14.
    changed_old, changed_new = tmp / "changed-old", tmp / "changed-new"
    write_json_unit(changed_old, degeneracy("changed-old"))
    write_json_unit(
        changed_new,
        degeneracy("changed-new"),
        meta_updates={"git_state_changed_during_run": True, "git_commit_at_start": "attacker-commit"},
    )
    out["changed_git_state_promoted"] = run_check("--new", changed_new, "--old", changed_old)

    # The artifact's own env is only checked for non-emptiness, while promotion
    # consults the independently editable sidecar env.  The two may contradict.
    artifact_env_old, artifact_env_new = tmp / "artifact-env-old", tmp / "artifact-env-new"
    write_json_unit(artifact_env_old, degeneracy("artifact-env-old"))
    env_obj = degeneracy("artifact-env-new")
    env_obj["env"] = {"python": "alien", "numpy": "alien", "scipy": "alien", "platform": "alien"}
    write_json_unit(artifact_env_new, env_obj)
    out["artifact_env_disagrees_with_meta_promoted"] = run_check(
        "--new", artifact_env_new, "--old", artifact_env_old
    )

    # Per-file hardlinks evade the directory-only independence check.
    alias_old, alias_new = tmp / "alias-old", tmp / "alias-new"
    old_file = write_json_unit(alias_old, degeneracy("alias"))
    alias_new.mkdir()
    new_file = alias_new / old_file.name
    os.link(old_file, new_file)
    os.link(old_file.with_name(old_file.name + ".meta.json"), new_file.with_name(new_file.name + ".meta.json"))
    alias_result = run_check("--new", alias_new, "--old", alias_old)
    alias_result["directories_samefile"] = os.path.samefile(alias_new, alias_old)
    alias_result["artifacts_samefile"] = os.path.samefile(new_file, old_file)
    alias_result["metas_samefile"] = os.path.samefile(
        new_file.with_name(new_file.name + ".meta.json"), old_file.with_name(old_file.name + ".meta.json")
    )
    out["per_file_alias_self_comparison"] = alias_result

    # float() accepts inf, and the numeric comparator regards inf == inf.
    inf_old, inf_new = tmp / "inf-old", tmp / "inf-new"
    write_matrix_unit(inf_old, matrix_row("inf-old", obj="inf"))
    write_matrix_unit(inf_new, matrix_row("inf-new", obj="inf"))
    out["matrix_inf_promoted"] = run_check("--new", inf_new, "--old", inf_old)

    jinf_old, jinf_new = tmp / "jinf-old", tmp / "jinf-new"
    write_json_unit(jinf_old, degeneracy("jinf-old", best_obj=float("inf")))
    write_json_unit(jinf_new, degeneracy("jinf-new", best_obj=float("inf")))
    out["degeneracy_infinity_promoted"] = run_check("--new", jinf_new, "--old", jinf_old)

    invalid_roster_row = profile_row("invalid-roster")
    out["profile_gamma_roster_not_validated"] = {
        "gamma_roster": invalid_roster_row["gamma_roster"],
        "problems": S.check_rows("profile", [invalid_roster_row], list(S.PROFILE_ROW)),
    }

    # Both receipts are structurally canonical and self-consistent, but all four
    # input byte identities changed.  ROW_SKIP/JSON_NUM omit their comparison.
    changed_rec_old, changed_rec_new = tmp / "changed-rec-old", tmp / "changed-rec-new"
    write_json_unit(changed_rec_old, degeneracy("changed-rec-old", receipt("bytes-A")))
    write_json_unit(changed_rec_new, degeneracy("changed-rec-new", receipt("bytes-B")))
    out["changed_valid_input_digests_promoted"] = run_check(
        "--new", changed_rec_new, "--old", changed_rec_old
    )

    # Duplicate flattened roles are accepted, and a changed but individually
    # valid receipt is not compared with the baseline receipt/digest.
    normal, equivocal = receipt("old"), duplicate_role_receipt("new")
    out["duplicate_receipt_direct"] = {
        "flattened_roles": [role for role, _ in S.receipt_leaves(equivocal)],
        "problems": S.validate_receipt(equivocal, S.inputs_digest(equivocal)),
    }
    rec_old, rec_new = tmp / "receipt-old", tmp / "receipt-new"
    write_json_unit(rec_old, degeneracy("receipt-old", normal))
    write_json_unit(rec_new, degeneracy("receipt-new", equivocal))
    out["changed_equivocal_receipt_promoted"] = run_check("--new", rec_new, "--old", rec_old)

    return out


def shape_step_repro() -> dict:
    root = str(TARGET)
    shell = f'''set -u
ROOT={root!s}
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/partial"
printf 'state,run_id\\n100,old\\n' > "$T/partial/ne_shape_GITT_Li.csv"
printf '{{"status":"partial"}}\\n' > "$T/partial/ne_shape_GITT_Li.csv.meta.json"
OUT="$T" STARTS=1 SI=Li BMS_DATA_ROOT="$T"
source <(sed -n '30,/^fail=0$/p' "$ROOT/scripts/run_states.sh" | sed '$d')
printf 'import sys\\nsys.exit(0)\\n' > "$T/returns_zero.py"
shape_step "$T" python3 "$T/returns_zero.py"
printf 'SHAPE_STEP_RC=%s\\n' "$?"
'''
    p = subprocess.run(["bash", "-lc", shell], text=True, capture_output=True, cwd=TARGET)
    return {"process_rc": p.returncode, "stdout": p.stdout.splitlines(), "stderr": p.stderr.splitlines()}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="r11-publish-schema-") as td:
        tmp = pathlib.Path(td)
        results = {
            "target": str(TARGET),
            "publication": publication_repros(tmp),
            "checker": checker_repros(tmp),
            "shape_step": shape_step_repro(),
        }
    print(json.dumps(results, ensure_ascii=False, indent=2, allow_nan=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
