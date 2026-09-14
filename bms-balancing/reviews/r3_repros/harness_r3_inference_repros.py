"""R3 numerical-inference review: public artifacts and benign synthetic data.

Run with --root /path/to/target/bms-balancing. No private data or target writes.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import pathlib
import statistics
import sys


ROOTS = {"pouch": "out", "fixedhc": "out/cells_pouch_fixedhc",
         "c168": "out/cells_c168", "c171": "out/cells_c171"}
STATES = ("100", "200", "300_0009")


def script_module(root, name):
    spec = importlib.util.spec_from_file_location("review_" + name,
                                                root / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matrix_row(root, label, state, source="GITT"):
    # Replicate the committed new regression's file and row selection.
    path = sorted((root / ROOTS[label]).glob(f"matrix_{state}*.csv"))[-1]
    with path.open(encoding="utf-8", newline="") as stream:
        matches = [r for r in csv.DictReader(stream) if r.get("si") == "Li"
                   and r.get("half_cell", "GITT") == source
                   and float(r.get("w_dqdv", 0)) == 0]
    assert len(matches) == 1, (path, state, source, len(matches))
    return path, matches[0]


def noise_counterexample(root):
    import numpy as np
    sys.path.insert(0, str(root))
    from bms_balancing.model import Objective

    class CorrectLinearModel(Objective):
        """Keep production RMSE calculation; use a known exact forward model."""
        def __init__(self, x, voltage):
            self.capacity = x
            self.voltage = voltage

        def E_cell(self, p, x):
            return p[0] + p[1] * x

    x = np.linspace(0., 1., 501)
    design = np.column_stack([np.ones_like(x), x])
    truth = np.array([3.25, .85])
    true_voltage = design @ truth
    rng = np.random.default_rng(472901)
    results = []
    targets = {}
    for label in ROOTS:
        observed = []
        for state in STATES:
            source, row = matrix_row(root, label, state)
            sigma = float(row["rmse_pocv"])
            targets[label, state] = sigma
            # Every vector lies in the residual space of the exactly specified
            # fitted model; this isolates noise from parameter/model error.
            noise = rng.normal(size=x.size)
            noise -= design @ np.linalg.lstsq(design, noise, rcond=None)[0]
            noise *= sigma / np.sqrt(np.mean(noise ** 2))
            voltage = true_voltage + noise
            fit = np.linalg.lstsq(design, voltage, rcond=None)[0]
            objective = CorrectLinearModel(x, voltage)
            rmse = objective.rmse_pocv(fit)
            model_error = float(np.max(np.abs(objective.E_cell(truth, x) - true_voltage)))
            parameter_error = float(np.max(np.abs(fit - truth)))
            assert model_error == 0.
            assert parameter_error < 1e-12
            assert abs(rmse - sigma) < 1e-14
            observed.append(rmse)
            results.append({"cell": label, "state": state,
                            "artifact_target_rmse_mV": sigma * 1000,
                            "correct_model_refit_rmse_mV": rmse * 1000,
                            "model_bias_mV": model_error * 1000,
                            "max_parameter_error": parameter_error})
        print("NOISE_EXACT_TREND", json.dumps({"cell": label,
              "noise_only_300_over_100": observed[-1]/observed[0],
              "rmse_mV": [v*1000 for v in observed]}))
    print("NOISE_EXACT_FITS", json.dumps(results))

    # Independent iid Gaussian noise, without residual-space construction.
    # Unequal sigma alone gives the cylinder trend in a correctly specified
    # model. Sigma values are constructed to the artifact, not estimated data.
    ensemble = []
    for label in ("pouch", "c168", "c171"):
        ratios = []
        for _ in range(300):
            rmses = []
            for state in ("100", "300_0009"):
                voltage = true_voltage + rng.normal(0., targets[label,state], x.size)
                fit = np.linalg.lstsq(design, voltage, rcond=None)[0]
                rmses.append(CorrectLinearModel(x, voltage).rmse_pocv(fit))
            ratios.append(rmses[-1]/rmses[0])
        ensemble.append({"cell":label, "imposed_noise_sd_ratio":targets[label,"300_0009"]/targets[label,"100"],
                         "median_refit_rmse_ratio":float(np.median(ratios)),
                         "q025_q975":[float(v) for v in np.quantile(ratios,[.025,.975])]})
    print("IID_NOISE_ENSEMBLE", json.dumps(ensemble))

    # A deterministic measurement nuisance gives the same table with an exact
    # equilibrium model: Vobs=Veq+I*R_s(x), I=1 A, SOC-dependent positive R_s.
    h = np.sin(4*np.pi*x)
    h -= design @ np.linalg.lstsq(design, h, rcond=None)[0]
    h /= np.sqrt(np.mean(h**2))
    current_results = []
    for label in ("c168", "c171"):
        rmses=[]
        for state in STATES:
            c=targets[label,state]
            resistance=c*(float(np.max(np.abs(h)))+.1+h)
            assert np.all(resistance>0)
            voltage=true_voltage+resistance  # current 1 A
            fit=np.linalg.lstsq(design, voltage, rcond=None)[0]
            rmses.append(CorrectLinearModel(x, voltage).rmse_pocv(fit))
        current_results.append({"cell":label,"measurement_current_A":1.,
                                "equilibrium_model_bias":0.,
                                "residual_mV":[v*1000 for v in rmses],
                                "rmse_300_over_100":rmses[-1]/rmses[0]})
    print("CURRENT_NUISANCE_EXACT_TREND",json.dumps(current_results))


def denominator_audit(root):
    import numpy as np
    compare=script_module(root,"compare_states")
    bands={label:compare.load_degeneracy(root/sub) for label,sub in ROOTS.items()}
    records=[]
    for label in ROOTS:
        for state in STATES:
            path,row=matrix_row(root,label,state)
            j=bands[label][state]["j"]
            matrix_p=np.array([float(row[k]) for k in ("a_PE","b_PE","a_NE","b_NE","gamma_Si")])
            matrix_ref=np.array([float(row[k]) for k in ("ref_a_PE","ref_b_PE","ref_a_NE","ref_b_NE","ref_gamma_Si")])
            records.append({"cell":label,"state":state,"matrix":str(path.relative_to(root)),
                            "degeneracy":bands[label][state]["file"],
                            "halfwidth":j["LLI_percent"]["span"]/2,
                            "target_rmse_mV":float(row["rmse_pocv"])*1000,
                            "reference_rmse_mV":float(row["ref_rmse_pocv"])*1000,
                            "matrix_objective":float(row["obj"]),
                            "degeneracy_objective":j["best_obj"],
                            "max_target_parameter_difference":float(np.max(np.abs(matrix_p-j["best_p"]))),
                            "max_reference_parameter_difference":float(np.max(np.abs(matrix_ref-j["ref_p"])))})
    groups=[[r for r in records if r["cell"] in labels]
            for labels in (("pouch","fixedhc"),("c168","c171"))]

    def summary(column):
        groups_values=[sorted(r["halfwidth"]/r[column] for r in group) for group in groups]
        p,c=groups_values
        return {"pouch_count":len(p),"cylinder_count":len(c),
                "pouch_range":[p[0],p[-1]],"cylinder_range":[c[0],c[-1]],
                "max_over_max":c[-1]/p[-1],"median_over_median":statistics.median(c)/statistics.median(p),
                "min_over_min":c[0]/p[0],"ranges_overlap":c[0]<p[-1]}

    target=summary("target_rmse_mV")
    ref=summary("reference_rmse_mV")
    print("TARGET_RMSE_DENOMINATOR",json.dumps(target))
    print("DECLARED_PRISTINE_DENOMINATOR",json.dumps(ref))
    assert abs(target["max_over_max"]-2.85)<.01
    assert not np.isclose(target["max_over_max"],ref["max_over_max"])
    text=(root/"FINDINGS.md").read_text(encoding="utf-8")
    assert "물리 단위(pristine 적합의 `rmse_pocv`" in text
    assert "| LLI 반폭 정규화 | 파우치 (7 적합)" in text
    assert target["pouch_count"]==6

    raw_six=[sorted(r["halfwidth"] for r in group) for group in groups]
    omitted=bands["pouch"]["300_0147"]["j"]
    raw_seven=sorted(raw_six[0]+[omitted["LLI_percent"]["span"]/2])
    print("COUNT_MEDIAN_CHANGE",json.dumps({
        "claimed_pouch_n":7,"actual_pouch_n":6,
        "raw_six_median_ratio":statistics.median(raw_six[1])/statistics.median(raw_six[0]),
        "raw_seven_median_ratio":statistics.median(raw_six[1])/statistics.median(raw_seven),
        "omitted_state":"300_0147","omitted_source":omitted["half_cell"],
        "reason": "Omitting a different source may be sound, but must change the table label/population."}))
    print("MATRIX_DEGENERACY_ALIGNMENT",json.dumps(records))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=pathlib.Path,default=pathlib.Path.cwd())
    parser.add_argument("--case",choices=("all","noise","denominator"),default="all")
    args=parser.parse_args()
    root=args.root.resolve()
    if args.case in ("all","noise"):
        noise_counterexample(root)
    if args.case in ("all","denominator"):
        denominator_audit(root)
    print("R3_NUMERICAL_REPRO_ASSERTIONS_PASSED")
