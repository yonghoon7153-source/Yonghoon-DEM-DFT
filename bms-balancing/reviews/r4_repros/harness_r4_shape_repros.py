"""R4 benign numerical audit of gamma diagnostics, witnesses, and grid scope.

Actual target Blend and ne_shape.main run with synthetic external inputs. No
private data or edits to target code are required.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import sys
from unittest.mock import patch


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def actual_blend_case(root, label, reference, fitted, truth, offset=0.0):
    import numpy as np
    from bms_balancing.model import Blend
    ns = load("r4_ne_shape_" + label, root / "scripts/ne_shape.py")
    u = np.linspace(0, 1, 301)
    arrays = ((1-u)**2, .1 + .7*u, 1-u, .1 + .7*u)
    blend = Blend(*arrays, window=11, poly_order=3)

    class InputPath:
        def __init__(self, state):
            self.state = state

        def is_file(self):
            return True

    class HalfInput:
        def __init__(self, path, **unused):
            self.state = path.state

        def E_PE(self, x):
            return 4.2 - .7*np.asarray(x)

        def E_NE(self, x):
            if self.state == "pristine":
                return blend.E(x, reference)
            return blend.E(x, truth) + offset

    buffer = io.StringIO()
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(ns.D, "STATES", ["pristine", "100"]))
        stack.enter_context(patch.object(ns.D, "data_root", return_value=Path("unused")))
        stack.enter_context(patch.object(ns.D, "half_cell_path", side_effect=lambda r, s, st: InputPath(st)))
        stack.enter_context(patch.object(ns.D, "load_literature", return_value=arrays))
        stack.enter_context(patch.object(ns, "HalfCell", HalfInput))
        stack.enter_context(patch.object(ns, "raw_ne_capacity", return_value=1.0))
        stack.enter_context(patch.object(ns, "fitted_pair", return_value=(fitted, reference)))
        stack.enter_context(patch.object(sys, "argv", ["ne_shape.py", "--write", ""]))
        stack.enter_context(contextlib.redirect_stdout(buffer))
        rc = ns.main()
    stdout = buffer.getvalue()
    measured = blend.E(ns.GRID, truth) + offset
    pristine = blend.E(ns.GRID, reference)
    a = float(np.max(abs(measured-pristine)))*1000
    b = float(np.max(abs(blend.E(ns.GRID, fitted)-pristine)))*1000
    fitted_delta = (blend.E(ns.GRID, fitted)-measured)*1000
    percent_over_50 = float(np.mean(abs(fitted_delta)>50))*100
    headroom = ns.gamma_headroom(blend, reference, a)
    witness = headroom["witness"]
    witness_amp = None if witness is None else float(np.max(abs(blend.E(ns.GRID,witness)-pristine)))*1000
    assert rc == 0
    if witness is not None:
        assert 0 <= witness <= .5 and witness_amp >= a-1e-9
    err = float(np.max(abs(blend.E(ns.GRID,truth)-measured)))
    if offset == 0:
        assert err == 0
    bad = "γ 를 어떻게 고르든 남고" in stdout
    return {"fixture": label, "reference_gamma": reference,
            "supplied_fitted_gamma": fitted, "true_measured_gamma": truth,
            "exact_model_error_V": err, "measured_amplitude_mV": a,
            "fitted_pair_amplitude_mV": b, "ratio_b_over_a": b/a,
            "selected_fit_fraction_over_50mV_percent": percent_over_50,
            "headroom": headroom, "witness_amplitude_mV": witness_amp,
            "universal_mismatch_claim_printed": bad,
            "actual_critical_stdout": [ln.strip() for ln in stdout.splitlines()
                                       if "모양이 아니다" in ln or "어떻게 고르든" in ln
                                       or "흡수한다 =" in ln or "표현력이나" in ln]}


def independent_grid_check(root):
    import numpy as np
    from bms_balancing.model import Blend
    ns = load("r4_grid_checks", root / "scripts/ne_shape.py")
    u=np.linspace(0,1,301)
    b=Blend((1-u)**2,.1+.7*u,1-u,.1+.7*u,window=11,poly_order=3)
    ref=.15
    true=.45025
    base=b.E(ns.GRID,ref)
    threshold=float(np.max(abs(b.E(ns.GRID,true)-base)))*1000
    got=ns.gamma_headroom(b,ref,threshold)
    amps=np.array([np.max(abs(b.E(ns.GRID,g)-base))*1000 for g in ns.GAMMA_GRID])
    valid=np.flatnonzero(amps>=threshold-1e-9)
    expected=float(ns.GAMMA_GRID[valid[np.argmin(abs(ns.GAMMA_GRID[valid]-ref))]])
    assert got["witness"]==expected and got["fam_max"]==float(max(amps))
    assert abs(got["witness"]-true)<.0011
    return {"known_legal_continuous_witness": true,"reported_nearest_grid_witness":got["witness"],
            "reported_result_matches_independent_grid_reduction":True,
            "note":"nearest is only among sampled gamma values, as the helper documents"}


def finite_grid_scope(root):
    """A smooth toy interface illustrates what a finite gamma scan can certify.

    This toy is deliberately NOT an instance of actual Blend. It tests the
    numerical contract, not a reversal of the private-data 86.01mV result.
    """
    import numpy as np
    ns=load("r4_scope",root/"scripts/ne_shape.py")
    class SmoothToy:
        def E(self,x,gamma):
            return np.full_like(np.asarray(x,dtype=float),
                                .1*np.exp(-((float(gamma)-.2505)/.00005)**2))
    toy=SmoothToy()
    result=ns.gamma_headroom(toy,.1,50)
    known_amp=float(np.max(abs(toy.E(ns.GRID,.2505)-toy.E(ns.GRID,.1))))*1000
    assert result["witness"] is None and known_amp==100
    return {"toy_not_actual_Blend":True,"scan":result,"actual_legal_gamma":.2505,
            "actual_toy_amplitude_mV":known_amp,
            "classification":"scope check only: absence on a grid is not global absence"}


def artifacts(root):
    rows=list(csv.DictReader((root/"out/ne_shape_GITT_Li.csv").open(encoding="utf-8")))
    vals=[]
    for r in rows:
        ref=float(r["gamma_ref"])
        assert abs(float(r["legal_dgamma_neg"])+ref)<1e-6
        assert abs(float(r["legal_dgamma_pos"])-(.5-ref))<1e-6
        witness=None if not r["gamma_witness"] else float(r["gamma_witness"])
        if witness is not None:
            assert 0<=witness<=.5
            assert abs(float(r["gamma_witness_delta"])-(witness-ref))<.000051
        vals.append({"state":r["state"],"selected_delta":float(r["gamma_target"])-ref,
                     "witness":witness,"saved_witness_delta":r["gamma_witness_delta"],
                     "saved_grid_family_max_mV":float(r["gamma_family_max_mV"])})
    return {"role_and_bound_arithmetic_consistent":True,"rows":vals,
            "private_literature_witness_amplitudes_independently_recomputed":False}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--target",type=Path,default=Path(__file__).resolve().parents[1]/"work/harness-r4-target/bms-balancing")
    args=ap.parse_args()
    sys.path.insert(0,str(args.target))
    old=actual_blend_case(args.target,"R3_low_ratio_control",.15,.16,.45)
    assert not old["universal_mismatch_claim_printed"]
    bad=actual_blend_case(args.target,"broad_residual_exact_family",.15,0.,.5)
    assert bad["universal_mismatch_claim_printed"] and bad["exact_model_error_V"]==0
    assert bad["selected_fit_fraction_over_50mV_percent"]>30
    outside=actual_blend_case(args.target,"old_amplitude_bound_control",.25,.26,.25,.1)
    assert outside["headroom"]["witness"] is None
    result={"R3_low_ratio_control":old,"remaining_c_branch_counterexample":bad,
            "R3_bound_control":outside,"headroom_grid_reduction":independent_grid_check(args.target),
            "grid_scope_illustration":finite_grid_scope(args.target),"committed_artifacts":artifacts(args.target)}
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
