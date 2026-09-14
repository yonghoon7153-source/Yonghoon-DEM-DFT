"""R5 benign scientific provenance and gamma-scope fixtures.

Real target ne_shape.main/fitted_pair/_write_csv/git_provenance are exercised.
Synthetic external electrode inputs and supplied matrix fit values are NOT
optimizer results. All fixture edits remain inside TemporaryDirectory.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True,
                          capture_output=True, text=True).stdout.strip()


def matrix(path, gamma, reference=.15):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["half_cell", "si", "w_dqdv",
                                               "gamma_Si", "ref_gamma_Si"])
        writer.writeheader()
        writer.writerow(dict(half_cell="GITT", si="Li", w_dqdv=0,
                             gamma_Si=gamma, ref_gamma_Si=reference))


def init_repo(cwd):
    git(cwd, "init", "-q")
    git(cwd, "config", "user.email", "fixture@example.invalid")
    git(cwd, "config", "user.name", "R5 numerical fixture")
    git(cwd, "config", "core.quotePath", "true")
    (cwd / "code.py").write_text("scale = 1\n", encoding="utf-8")
    matrix(cwd / "out/matrix_100.csv", .16)
    git(cwd, "add", "code.py", "out/matrix_100.csv")
    git(cwd, "commit", "-qm", "synthetic matrix reference")


@contextlib.contextmanager
def working_directory(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def synthetic_inputs(ns, reference=.15):
    import numpy as np
    from bms_balancing.model import Blend
    u = np.linspace(0, 1, 301)
    arrays = ((1-u)**2, .1+.7*u, 1-u, .1+.7*u)
    blend = Blend(*arrays, window=11, poly_order=3)
    return arrays, blend


def run_diagnostic(ns, cwd, truth=.45, offset=0., reference=.15):
    import numpy as np
    arrays, blend = synthetic_inputs(ns, reference)

    class InputPath:
        def __init__(self, state):
            self.state = state

        def is_file(self):
            return True

    class HalfInput:
        def __init__(self, path, **unused):
            self.state = path.state

        def E_PE(self, x):
            return 4.2-.7*np.asarray(x)

        def E_NE(self, x):
            return blend.E(x, reference if self.state == "pristine" else truth) + (
                0. if self.state == "pristine" else offset)

    buffer = io.StringIO()
    with contextlib.ExitStack() as stack:
        stack.enter_context(working_directory(cwd))
        stack.enter_context(patch.object(ns.D, "STATES", ["pristine", "100"]))
        stack.enter_context(patch.object(ns.D, "data_root", return_value=Path("unused")))
        stack.enter_context(patch.object(ns.D, "half_cell_path", side_effect=lambda r, s, st: InputPath(st)))
        stack.enter_context(patch.object(ns.D, "load_literature", return_value=arrays))
        stack.enter_context(patch.object(ns, "HalfCell", HalfInput))
        stack.enter_context(patch.object(ns, "raw_ne_capacity", return_value=1.0))
        # fitted_pair, main, CSV writer, and git_provenance are NOT replaced.
        stack.enter_context(patch.object(sys, "argv", ["ne_shape.py", "--out-dir", "out", "--write", "out"]))
        stack.enter_context(contextlib.redirect_stdout(buffer))
        assert ns.main() == 0
    artifact = cwd / "out/ne_shape_GITT_Li.csv"
    row = next(csv.DictReader(artifact.open(encoding="utf-8")))
    meta = json.loads(artifact.with_name(artifact.name + ".meta.json").read_text(encoding="utf-8"))
    return {"row": row, "meta": meta, "stdout": buffer.getvalue()}


def consumed_untracked_input(root):
    ns = load("r5_input_diag", root / "scripts/ne_shape.py")
    import provenance
    with tempfile.TemporaryDirectory(prefix="bms-r5-input-") as td:
        cwd = Path(td)
        init_repo(cwd)
        first = run_diagnostic(ns, cwd)
        matrix(cwd / "out/matrix_100_v2.csv", .45)
        second = run_diagnostic(ns, cwd)
        fields = ["git_commit", "git_dirty", "git_modified_code", "git_modified_outputs", "gamma_from"]
        before = {f: first["meta"][f] for f in fields}
        after = {f: second["meta"][f] for f in fields}
        assert before == after
        assert before["git_dirty"] is False and before["git_modified_outputs"] == []
        assert float(first["row"]["gamma_target"]) == .16
        assert float(second["row"]["gamma_target"]) == .45
        assert float(first["row"]["ratio_b_over_a"]) < .034
        assert float(second["row"]["ratio_b_over_a"]) == 1.
        status = git(cwd, "status", "--porcelain", "--untracked-files=all")
        new_digest = hashlib.sha256((cwd / "out/matrix_100_v2.csv").read_bytes()).hexdigest()

        # R4-07 positive controls: tracked changed inputs are listed as outputs;
        # non-output code modification correctly makes git_dirty true.
        (cwd / "out/matrix_100_v2.csv").unlink()
        matrix(cwd / "out/matrix_100.csv", .45)
        with working_directory(cwd):
            tracked = provenance.git_provenance(artifact="out/ne_shape_GITT_Li.csv")
        assert tracked["git_dirty"] is False
        assert tracked["git_modified_outputs"] == ["out/matrix_100.csv"]
        (cwd / "code.py").write_text("scale = 2\n", encoding="utf-8")
        with working_directory(cwd):
            code = provenance.git_provenance(artifact="out/ne_shape_GITT_Li.csv")
        assert code["git_dirty"] is True and code["git_modified_code"] == ["code.py"]
        return {"synthetic_external_data_and_supplied_fit_values": True,
                "real_fitted_pair_main_csv_writer_and_provenance": True,
                "before_input": "out/matrix_100.csv", "after_input": "out/matrix_100_v2.csv",
                "untracked_input_sha256": new_digest,
                "before": {k:first["row"][k] for k in ["gamma_target", "gamma_ref", "ratio_b_over_a"]},
                "after": {k:second["row"][k] for k in ["gamma_target", "gamma_ref", "ratio_b_over_a"]},
                "identical_provenance": before,
                "actual_full_git_status": status.splitlines(),
                "tracked_input_positive_control": tracked,
                "code_edit_positive_control": code}


def quoted_path_roles(root):
    pv = load("r5_provenance_quoted", root / "scripts/provenance.py")
    with tempfile.TemporaryDirectory(prefix="bms-r5-quoted-") as td:
        cwd = Path(td)
        init_repo(cwd)
        name = "out/측정.csv"
        (cwd / name).write_text("value\n1\n", encoding="utf-8")
        git(cwd, "add", name)
        git(cwd, "commit", "-qm", "synthetic named output")
        (cwd / name).write_text("value\n2\n", encoding="utf-8")
        result = pv.git_provenance(cwd=cwd)
        assert result["git_dirty"] is True
        assert result["git_modified_outputs"] == []
        assert len(result["git_modified_code"]) == 1
        return {"actual_changed_path":name,
                "git_status":git(cwd,"status","--porcelain","--untracked-files=no"),
                "provenance":result,
                "expected": {"git_dirty":False,"git_modified_outputs":[name],"git_modified_code":[]}}


def amplitude_shape_scope(root):
    import numpy as np
    ns = load("r5_gamma_scope", root / "scripts/ne_shape.py")
    _, blend = synthetic_inputs(ns)
    ref = .15
    base = blend.E(ns.GRID,ref)
    exact = blend.E(ns.GRID,.5)
    amplitude = float(np.max(abs(exact-base)))
    shifted = base + amplitude
    one = ns.gamma_headroom(blend,ref,amplitude*1000)
    two = ns.gamma_headroom(blend,ref,float(np.max(abs(shifted-base)))*1000)
    assert one == two and one["witness"] == .5
    models = np.array([blend.E(ns.GRID,g) for g in ns.GAMMA_GRID])
    exact_errors = np.max(abs(models-exact), axis=1)*1000
    shifted_errors = np.max(abs(models-shifted), axis=1)*1000
    assert float(np.min(exact_errors)) == 0.
    assert float(np.min(shifted_errors)) > 50
    with tempfile.TemporaryDirectory(prefix="bms-r5-gamma-") as td:
        cwd = Path(td)
        init_repo(cwd)
        matrix(cwd / "out/matrix_100.csv", 0.)
        old_control = run_diagnostic(ns,cwd,truth=.5)
        assert float(old_control["row"]["frac_over_50mV"]) == 68.
        assert "γ 를 어떻게 고르든 남고" not in old_control["stdout"]
        matrix(cwd / "out/matrix_100.csv", .5)
        result = run_diagnostic(ns,cwd,truth=ref,offset=amplitude)
        lines = result["stdout"].splitlines()
        critical = [x.strip() for x in lines if "다른 γ 에서도" in x or "증인 열이," in x]
        assert critical
        assert "γ 를 어떻게 고르든 남고" not in result["stdout"]
        return {"classification":"Q5 clarification, not an independent new P1",
                "actual_Blend_synthetic_measurements":True,
                "same_measured_amplitude_mV":amplitude*1000,
                "same_headroom_for_both_measurements":one,
                "exact_family_min_max_error_on_grid_mV":float(np.min(exact_errors)),
                "shifted_family_min_max_error_on_grid_mV":float(np.min(shifted_errors)),
                "selected_fit_frac_over_50mV_percent":float(result["row"]["frac_over_50mV"]),
                "actual_critical_stdout":critical,
                "old_R4_universal_impossibility_claim_absent":True,
                "old_R4_exact_family_control_frac_over_50mV_percent":float(old_control["row"]["frac_over_50mV"]),
                "limitation":"Residual lower bound here is only over the stated gamma501/x400 grid; no claim about private-data fits or all continuous gamma."}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--target",type=Path,default=Path(__file__).resolve().parents[1]/"work/harness-r5-target/bms-balancing")
    a=ap.parse_args()
    sys.path.insert(0,str(a.target))
    results={"consumed_untracked_input":consumed_untracked_input(a.target),
             "quoted_path_roles":quoted_path_roles(a.target),
             "amplitude_shape_scope":amplitude_shape_scope(a.target)}
    print(json.dumps(results,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
