"""R4 scientific review: actual artifact checks and finite plateau counterexample.

No private data or target modifications. Run --target /path/to/bms-balancing.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import pathlib
import sys
import warnings
from unittest import mock


ROOTS={"pouch":"out", "fixedhc":"out/cells_pouch_fixedhc",
       "c168":"out/cells_c168", "c171":"out/cells_c171"}
STATES=("100","200","300_0009")


def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_artifacts(root):
    compare=load_module(root/"scripts/compare_states.py","r4_compare")
    rows=[]
    for label,sub in ROOTS.items():
        latest=compare.load_degeneracy(root/sub)
        ratios=[]
        for state in STATES:
            path=sorted((root/sub).glob(f"matrix_{state}*.csv"))[-1]
            with path.open(encoding="utf-8") as stream:
                selected=[r for r in csv.DictReader(stream) if
                          r.get("si")=="Li" and r.get("half_cell")=="GITT" and float(r["w_dqdv"])==0]
            assert len(selected)==1
            r=selected[0]
            j=latest[state]["j"]
            assert [float(r[k]) for k in ("a_PE","b_PE","a_NE","b_NE","gamma_Si")]==j["best_p"]
            assert [float(r[k]) for k in ("ref_a_PE","ref_b_PE","ref_a_NE","ref_b_NE","ref_gamma_Si")]==j["ref_p"]
            assert float(r["obj"])==j["best_obj"]
            rec={"cell":label,"state":state,"width":j["LLI_percent"]["span"]/2,
                 "target_rmse_mV":float(r["rmse_pocv"])*1000,
                 "reference_rmse_mV":float(r["ref_rmse_pocv"])*1000}
            rows.append(rec)
            ratios.append(rec["target_rmse_mV"])
        print("RESIDUAL_OBSERVATION",json.dumps({"cell":label,"rmse_mV":ratios,
              "ratio_300_over_100":ratios[-1]/ratios[0]}))
    for denominator in ("target_rmse_mV","reference_rmse_mV"):
        p=sorted(r["width"]/r[denominator] for r in rows if r["cell"] in ("pouch","fixedhc"))
        c=sorted(r["width"]/r[denominator] for r in rows if r["cell"] in ("c168","c171"))
        assert len(p)==6 and len(c)==6
        print("NORMALIZATION_CLOSURE",json.dumps({"denominator":denominator,"pouch_n":len(p),
              "cylinder_n":len(c),"pouch_range":[p[0],p[-1]],"cylinder_range":[c[0],c[-1]],
              "max_ratio":c[-1]/p[-1],"range_overlap":c[0]<p[-1]}))
    print("MATRIX_DEGENERACY_ALIGNMENT",json.dumps({"pairs":len(rows),"all_exact":True}))


def actual_regression_closure(root):
    tests=load_module(root/"tests/test_review_findings.py","r4_review_findings")
    tests.test_section_1_12_physical_normalization_and_misfit_tables_match_artifacts()
    tests.test_r3_01_findings_keeps_the_residual_growth_as_observation_not_as_cause()
    print("ACTUAL_CLOSURE_REGRESSIONS",json.dumps({"R3_01": "PASS", "R3_04":"PASS"}))
    original_ctx=tests._r2_tables_ctx
    cases={"wrong_population":("파우치 (6 적합, GITT)","파우치 (7 적합, GITT)"),
           "swapped_target_denominator_label":("/rmse_pocv (대상 적합)","/rmse_pocv (pristine 기준 적합)")}
    for name,(old,new) in cases.items():
        def mutated_ctx(old=old,new=new):
            B,objs,rmse,sec,S=original_ctx()
            assert old in sec
            return B,objs,rmse,sec.replace(old,new),S
        with mock.patch.object(tests,"_r2_tables_ctx",mutated_ctx):
            try:
                tests.test_section_1_12_physical_normalization_and_misfit_tables_match_artifacts()
            except AssertionError:
                print("CLOSURE_NEGATIVE_CONTROL",json.dumps({"case":name,"rejected":True}))
            else:
                raise AssertionError("R3-04 regression did not reject "+name)


def plateau_scale_scope(root):
    import numpy as np
    from bms_balancing.model import Objective,LB5,UB5

    class FinitePlateau(Objective):
        """Entire input voltage family is finite, continuous, and nondecreasing."""
        def __init__(self):
            self.x_model=np.linspace(0.,1.,101)
            self.vol_dq_fit=np.linspace(0.,.8,41)
            self.dq_fit_data=np.full(41,2.)
            self.w_peak=np.ones(41)
            self.window=5
            self.poly_order=2
            self.use_peak_weight=False
            self.w_pocv=self.w_dvdq=self.w_dqdv=1.

        def E_cell(self,p,x):
            return np.maximum(0.,np.asarray(x)-(p[0]-1.1))

        def rmse_pocv(self,p):
            return 1.

        def rmse_dvdq(self,p):
            return 1.

    objective=FinitePlateau()
    seed,n=0,50
    samples=LB5+np.random.default_rng(seed).random((n,5))*(UB5-LB5)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        values=np.array([objective.rmse_dqdv(p) for p in samples])
        result=objective._auto_scales(seed,n)
    non_nan=np.sort(values[~np.isnan(values)])
    # This formula is the ORIGINAL algorithm printed in FINDINGS §1-13,
    # not an independently retrieved private MATLAB function.
    declared_original_mean=float(np.mean(non_nan[:max(1,len(non_nan)//2)]))
    direct_inf=next(p for p,v in zip(samples,values) if np.isinf(v))
    forward=objective.E_cell(direct_inf,objective.x_model)
    assert np.all(np.isfinite(forward)) and np.all(np.diff(forward)>=0.)
    assert np.isinf(objective.rmse_dqdv(direct_inf))
    assert np.isinf(declared_original_mean)
    assert np.isfinite(result["dqdv"]) and result["dqdv"]>.9
    finite_example=next(p for p,v in zip(samples,values) if np.isfinite(v))
    objective.scales=result
    finite_point_python_objective=objective(finite_example)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sentinel_at_inf_point=objective(direct_inf)
    objective.scales={"pocv":1.,"dvdq":1.,"dqdv":declared_original_mean}
    finite_point_reported_original_objective=objective(finite_example)
    assert sentinel_at_inf_point==1e6
    assert abs(finite_point_python_objective-finite_point_reported_original_objective)>.9
    print("PLATEAU_AUTOSCALE_COUNTEREXAMPLE",json.dumps({
          "finite_forward":True,"nondecreasing_forward":True,"n_samples":n,
          "n_finite_rmse":int(np.isfinite(values).sum()),"n_inf_rmse":int(np.isinf(values).sum()),
          "n_nan_rmse":int(np.isnan(values).sum()),
          "declared_original_non_nan_count":len(non_nan),
          "declared_original_lower_half_mean":str(declared_original_mean),
          "python_auto_scale_dqdv":result["dqdv"],
          "finite_point_python_objective":finite_point_python_objective,
          "finite_point_with_reported_original_scales":finite_point_reported_original_objective,
          "wrapper_sentinel_at_inf_point":sentinel_at_inf_point,
          "example_parameters":direct_inf.tolist(),
          "warning_kinds":sorted(set(str(w.message) for w in caught)),
          "private_matlab_run":False}))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--target",type=pathlib.Path,default=pathlib.Path.cwd())
    parser.add_argument("--case",choices=("all","closure","plateau"),default="all")
    args=parser.parse_args()
    root=args.target.resolve()
    sys.path.insert(0,str(root))
    if args.case in ("all","closure"):
        verify_artifacts(root)
        actual_regression_closure(root)
    if args.case in ("all","plateau"):
        plateau_scale_scope(root)
    print("R4_INFERENCE_REPRO_ASSERTIONS_PASSED")
