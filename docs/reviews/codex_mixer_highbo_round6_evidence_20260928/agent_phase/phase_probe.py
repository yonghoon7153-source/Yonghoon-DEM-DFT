"""Independent bounded synthetic phase-receipt review. Never executes a simulator.

The old review fixture supplies only geometry/log writers; production modules are
loaded from the current pinned mirror. Only Python's run-status heredoc runs.
"""
from __future__ import annotations

import collections
import contextlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
import mixer_restart_phase_test as pt
import check_contact_validity as cv
import measure_mixing_index
import make_mixer_deck
import mixer_deck_diff

oldpath = ROOT / "fixture_helpers.py"
spec = importlib.util.spec_from_file_location("old_fixture", oldpath)
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
fx.ROOT = ROOT


def write_log(base, sub, end, n1, banner=False, resume=None):
    lines = [fx.BANNER]
    if sub == "B":
        lines.append(f"RESUME_STEP {n1 if resume is None else resume}")
    lines += ["Step Atoms KinEng", f"{end} 0 0", "Loop time fixture"]
    if banner:
        lines.append("Total wall time: 0:00:01")
    (base / sub / "log.lmp").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(td):
    run, base, U, g, binary = fx.fixture(td)
    for sub in ("A", "B"):
        write_log(base, sub, g["run_total"], g["n1"])
    fx.status(base)
    fx.bind(run, binary)
    return run, base, U, g, binary


def result(base):
    out = base / "receipt.json"
    rc = fx.quiet(pt.analyze, str(base), out=str(out))
    cli = subprocess.run([sys.executable, str(ROOT / "scripts/mixer_restart_phase_test.py"),
                          "analyze", str(base)], capture_output=True, text=True, encoding="utf-8")
    return dict(passed=rc["passed"], cli_rc=cli.returncode, reasons=rc["reasons"],
                deck_steps=rc["deck_steps"], resume_steps_B=rc["resume_steps_B"],
                run_total=rc["run_total"], nA=len(rc["steps_checked_A"]), nB=len(rc["steps_checked_B"]),
                angle_error_deg=rc["angle_error_deg"], pos_bound_m=rc["pos_bound_m"],
                residual_max_m=rc["residual_max_m"], ab_max=rc["ab_max_vertex_diff_m"],
                completion={s: {k: rc["run_status"][s][k] for k in
                                ("complete", "completion_basis", "last_thermo_step", "banner")}
                            for s in ("A", "B")}), rc


def triangle_bag(T):
    """Exact, synthetic-only oracle: a multiset of three-vertex triangles.

    Deliberately not a proposed floating-point production implementation.
    """
    return collections.Counter(tuple(sorted(tuple(float(x) for x in p) for p in tri)) for tri in T)


def point_bag(T):
    return collections.Counter(tuple(float(x) for x in p) for p in T.reshape(-1, 3))


def main():
    out = {"pin": "18787ab98a13361c37b2343bd07ae276142d0953",
           "scope": "Synthetic geometry and logs only; no simulator, MPI, job, or Git mutation"}
    with tempfile.TemporaryDirectory(prefix="synthetic_", dir=HERE) as tmp:
        td = Path(tmp)
        for mode in ("normal", "gen_end_truncated", "bad_resume_step", "banner_short_tail",
                     "changed_gen_motion_signature", "B_checkpoint_other_path", "permuted_triangles"):
            run, base, U, g, binary = build(td / mode)
            if mode == "gen_end_truncated":
                original = g["run_total"]
                g["run_total"], g["n1"] = 9500, 9000
                fx.js(base / "gen.json", g)
                for sub in ("A", "B"):
                    for p in (base / sub / "post_mesh").glob("*.stl"):
                        if int(p.stem.split("_")[-1]) > 9500:
                            p.unlink()
                    write_log(base, sub, 9500, 9000)
                fx.status(base)
            elif mode == "bad_resume_step":
                write_log(base, "B", g["run_total"], g["n1"], resume=g["n1"] + 500)
                fx.status(base)
            elif mode == "banner_short_tail":
                for sub in ("A", "B"):
                    write_log(base, sub, 14000, g["n1"], banner=True)
                fx.status(base)
            elif mode == "changed_gen_motion_signature":
                # Source measurement still uses sealed ORIGINAL A/B STL. The
                # campaign instead uses a translated Drum, and only mutable gen
                # metadata is redirected to its new motion signature.
                original_sig = pt.motion_signature((base / "A/in.phase_a").read_text(encoding="utf-8"), str(base / "A"))
                drum = cv.read_stl(run / "Drum.stl")
                drum[..., 1] += .01
                fx.write_stl(run / "Drum.stl", drum)
                g["motion_signature"] = cv.motion_signature(fx.SMALL, str(run))
                fx.js(base / "gen.json", g)
                fx.bind(run, binary)
            elif mode == "B_checkpoint_other_path":
                bp = base / "B/in.phase_b"
                bp.write_text(re.sub(r"(?m)^read_restart\s+restart_pt/ckpt\.bin", "read_restart unrelated/other.bin", bp.read_text(encoding="utf-8")), encoding="utf-8")
                seal = json.loads((base / "seal.json").read_text())
                seal["files"]["B/in.phase_b"] = fx.sha(bp)
                fx.js(base / "seal.json", seal)
            elif mode == "permuted_triangles":
                for sub in ("A", "B"):
                    for p in (base / sub / "post_mesh").glob("*.stl"):
                        T = cv.read_stl(p)
                        # Different rank-like ordering in A and B, plus an
                        # independently permuted vertex order within triangles.
                        order = np.arange(len(T))[::-1] if sub == "A" else np.roll(np.arange(len(T)), 7)
                        fx.write_stl(p, T[order][:, [2, 0, 1], :])
                fx.status(base)
            r, rc = result(base)
            if mode in ("normal", "banner_short_tail", "changed_gen_motion_signature", "B_checkpoint_other_path"):
                r["consumer"] = fx.accept(base / "receipt.json", run)
            if mode == "changed_gen_motion_signature":
                r.update(measured_A_signature=original_sig, advertised_signature=g["motion_signature"],
                         signature_different=original_sig != g["motion_signature"],
                         unmeasured_campaign_drum_shift_m=.01 * .0149277,
                         seal_unchanged=True)
            if mode == "B_checkpoint_other_path":
                r["read_restart_line"] = next(l for l in bp.read_text(encoding="utf-8").splitlines() if l.startswith("read_restart"))
            out[mode] = r
        # Geometric acceptance oracle: reversing listing/internal vertex order
        # preserves triangles, whereas flattened-coordinate equality does not
        # prove the three-vertex connectivity or duplicate multiplicity.
        a = np.array([[0., 0., 0.], [1., 0., 0.], [1., 1., 0.]])
        b = np.array([[0., 0., 1.], [1., 1., 1.], [0., 1., 1.]])
        mesh = np.stack([a, b])
        rewire = mesh.copy()
        rewire[0, 1], rewire[1, 2] = mesh[1, 2].copy(), mesh[0, 1].copy()
        dup_source = np.stack([a, a, b])
        dup_wrong = np.stack([a, b, b])
        out["triangle_oracle"] = {
            "permutation_pass": triangle_bag(mesh) == triangle_bag(mesh[::-1, ::-1]),
            "rewire_same_point_bag": point_bag(mesh) == point_bag(rewire),
            "rewire_triangle_bag_equal": triangle_bag(mesh) == triangle_bag(rewire),
            "duplicate_change_same_triangle_set": set(triangle_bag(dup_source)) == set(triangle_bag(dup_wrong)),
            "duplicate_change_triangle_bag_equal": triangle_bag(dup_source) == triangle_bag(dup_wrong),
        }
    out["assertions"] = {
        "normal_passes": out["normal"]["cli_rc"] == 0 and out["normal"]["consumer"]["accepted"],
        "original_truncation_closed": out["gen_end_truncated"]["cli_rc"] == 1,
        "bad_resume_closed": out["bad_resume_step"]["cli_rc"] == 1,
        "banner_tail_remaining": out["banner_short_tail"]["cli_rc"] == 0,
        "metadata_signature_remaining": out["changed_gen_motion_signature"]["cli_rc"] == 0 and out["changed_gen_motion_signature"]["consumer"]["accepted"],
        "permutation_false_red": out["permuted_triangles"]["cli_rc"] == 1,
        "triangle_topology_oracle": not out["triangle_oracle"]["rewire_triangle_bag_equal"] and not out["triangle_oracle"]["duplicate_change_triangle_bag_equal"],
    }
    (HERE / "phase_probe_output.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    assert all(out["assertions"].values()), out["assertions"]


if __name__ == "__main__":
    main()
