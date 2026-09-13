"""Benign, in-memory scientific schema checks for the R13 review.

Imports the read-only target; never writes an artifact, sidecar, or target file.
The tabular values and input-byte labels are synthetic, not scientific evidence.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import pathlib
import sys


TARGET = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(TARGET))
sys.path.insert(0, str(TARGET / "scripts"))
from bms_balancing import schema as S
import check_u14 as C


def receipt(half="GITT", si="Li", state="100"):
    def leaf(label):
        data = f"capacity,voltage\n0,1\n1,2\n# synthetic {label}\n".encode()
        return {"path": f"synthetic/{label}.csv", "sha256": hashlib.sha256(data).hexdigest()}

    return {
        "half_cell": leaf(f"half_{half}_{state}"),
        "full_cell": leaf("full"),
        "literature": {"gr": leaf("gr"), "si": leaf(f"si_{si}")},
    }


def audit():
    return {
        metric: {
            "n": 50, "n_finite": 50, "n_inf": 0, "n_nan": 0,
            "n_exception": 0, "raw_lower_half_mean": 1.0, "scale": 1.0000000000000002,
            "eps_rel": 2.220446049250313e-16, "equivalent_within_rel": True,
        }
        for metric in ("pocv", "dvdq", "dqdv")
    }


def matrix_rows():
    out = []
    si_sources = ("Baggetto", "Friedrich", "Jiang", "Kunz", "Li", "Lu", "Sethuraman", "Wetjen")
    for half in ("GITT", "step_005C"):
        for si in si_sources:
            for w in (0.0, 1.0):
                ci, ri = receipt(half, si), receipt(half, si, "pristine")
                row = {key: "1.0" for key in S.MATRIX_ROW}
                row.update(
                    half_cell=half, si=si, w_dqdv=str(w), run_id="synthetic-run",
                    consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(ri),
                    inputs_sha=S.inputs_digest(ci), ref_inputs_sha=S.inputs_digest(ri),
                    scale_audit_target=json.dumps(audit()), scale_audit_ref=json.dumps(audit()),
                    scale_seed="0", n_scale_samples="50",
                    scale_pocv_target="1.0000000000000002", scale_dvdq_target="1.0000000000000002",
                    scale_dqdv_target="1.0000000000000002", scale_pocv_ref="1.0000000000000002",
                    scale_dvdq_ref="1.0000000000000002", scale_dqdv_ref="1.0000000000000002",
                    bounds="-", ref_bounds="-",
                    combo_roster=json.dumps({"authority": 32, "requested": 32, "succeeded": 32,
                                              "missing_input": [], "failed": [], "absent": []}),
                )
                out.append(row)
    return out


def csv_bytes(rows, header):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=header, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def degeneracy():
    ci, ri = receipt(), receipt(state="pristine")
    out = {key: 1.0 for key in S.DEGENERACY_KEYS}
    out.update(
        state="100", si_source="Li", half_cell="GITT", run_id="synthetic-run",
        env={key: "synthetic-version" for key in S.ENV_KEYS},
        consumed_inputs=ci, ref_consumed_inputs=ri, inputs_sha=S.inputs_digest(ci),
        best_p=[1.0] * 5, ref_p=[1.0] * 5,
        best_modes_percent={key: 1.0 for key in ("LAM_PE", "LAM_NE", "LLI")},
    )
    return out


results = {}
rows = matrix_rows()
results["matrix_control_schema"] = S.check_rows("matrix", rows, list(S.MATRIX_ROW))
assert not results["matrix_control_schema"]

original = csv_bytes(rows, S.MATRIX_ROW)
reversed_rows = csv_bytes(list(reversed(rows)), S.MATRIX_ROW)
results["matrix_reorder_identity"] = C._input_identity_problems("matrix_synthetic.csv", "matrix", original, reversed_rows)
assert results["matrix_reorder_identity"] == ([], [])

changed = copy.deepcopy(rows)
ci = receipt(si="Li_alternate")
changed[0].update(consumed_inputs=json.dumps(ci), inputs_sha=S.inputs_digest(ci))
results["matrix_first_row_alternate_input"] = C._input_identity_problems(
    "matrix_synthetic.csv", "matrix", original, csv_bytes(changed, S.MATRIX_ROW)
)
assert results["matrix_first_row_alternate_input"][0]

changed_reference = copy.deepcopy(rows)
ri = receipt(si="Li_alternate", state="pristine")
changed_reference[0].update(ref_consumed_inputs=json.dumps(ri), ref_inputs_sha=S.inputs_digest(ri))
results["matrix_first_row_alternate_reference_input"] = C._input_identity_problems(
    "matrix_synthetic.csv", "matrix", original, csv_bytes(changed_reference, S.MATRIX_ROW)
)
assert results["matrix_first_row_alternate_reference_input"][0]

profile = []
for i in range(21):
    row = {key: "1.0" for key in S.PROFILE_ROW}
    ci, ri = receipt(), receipt(state="pristine")
    row.update(
        gamma_Si=str(i / 40), bounds="-", run_id="synthetic-run", profile_scale="global",
        consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(ri),
        inputs_sha=S.inputs_digest(ci), ref_inputs_sha=S.inputs_digest(ri),
        gamma_roster=json.dumps({"authority": 21, "requested": 21, "succeeded": 21, "missing": []}),
    )
    profile.append(row)
results["profile_control_schema"] = S.check_rows("profile", profile, list(S.PROFILE_ROW))
assert not results["profile_control_schema"]
results["profile_reorder_identity"] = C._input_identity_problems(
    "profile_synthetic.csv", "profile", csv_bytes(profile, S.PROFILE_ROW),
    csv_bytes(list(reversed(profile)), S.PROFILE_ROW),
)
assert results["profile_reorder_identity"] == ([], [])

profile_changed = copy.deepcopy(profile)
ci = receipt(si="Li_alternate")
profile_changed[0].update(consumed_inputs=json.dumps(ci), inputs_sha=S.inputs_digest(ci))
results["profile_first_row_alternate_input"] = C._input_identity_problems(
    "profile_synthetic.csv", "profile", csv_bytes(profile, S.PROFILE_ROW),
    csv_bytes(profile_changed, S.PROFILE_ROW),
)
assert results["profile_first_row_alternate_input"][0]

ci = receipt()
results["receipt_dict_and_json_string_agree"] = S.receipt_map(ci) == S.receipt_map(json.dumps(ci))
assert results["receipt_dict_and_json_string_agree"]

j = degeneracy()
results["degeneracy_control_schema"] = S.check_degeneracy(j)
assert not results["degeneracy_control_schema"]

missing_ref = dict(j, ref_consumed_inputs={})
results["degeneracy_empty_reference_schema"] = S.check_degeneracy(missing_ref)
incomplete = copy.deepcopy(j["ref_consumed_inputs"])
incomplete["half_cell"].pop("path")
results["degeneracy_reference_missing_locator_dict"] = S.check_degeneracy(dict(j, ref_consumed_inputs=incomplete))
results["degeneracy_reference_missing_locator_json_string"] = S.check_degeneracy(
    dict(j, ref_consumed_inputs=json.dumps(incomplete))
)
results["degeneracy_both_empty_reference_comparison"] = C._input_identity_problems(
    "degeneracy_synthetic.json", "degeneracy",
    json.dumps(missing_ref).encode(), json.dumps(missing_ref).encode(),
)
results["degeneracy_candidate_empty_reference_comparison"] = C._input_identity_problems(
    "degeneracy_synthetic.json", "degeneracy", json.dumps(j).encode(), json.dumps(missing_ref).encode()
)
assert results["degeneracy_candidate_empty_reference_comparison"][0]
results["degeneracy_baseline_empty_reference_comparison"] = C._input_identity_problems(
    "degeneracy_synthetic.json", "degeneracy", json.dumps(missing_ref).encode(), json.dumps(j).encode()
)
assert results["degeneracy_baseline_empty_reference_comparison"][1]

for label, value in (("empty_string", ""), ("empty_json_object", "{}")):
    amended = copy.deepcopy(rows)
    amended[0]["scale_audit_target"] = value
    results[f"matrix_scale_audit_{label}_schema"] = S.check_rows("matrix", amended, list(S.MATRIX_ROW))
results["matrix_scale_audit_comparison_excluded"] = "scale_audit_target" in S.ROW_SKIP

env = {key: "synthetic-version" for key in S.ENV_KEYS}
results["pandas_version_change"] = S.env_problems(env, dict(env, pandas="synthetic-version-2"))
results["pandas_version_missing"] = S.env_problems(env, {key: value for key, value in env.items() if key != "pandas"})
results["openpyxl_is_comparison_axis"] = "openpyxl" in S.ENV_KEYS

print(json.dumps(results, ensure_ascii=False, indent=2))
