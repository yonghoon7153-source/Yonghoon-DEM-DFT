#!/usr/bin/env python3
"""Author mutation checks; synthetic local source copies only."""
import argparse, ast, hashlib, json, pathlib, shutil, subprocess, sys
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--reader',type=pathlib.Path,required=True)
parser.add_argument('--tests',type=pathlib.Path,required=True)
parser.add_argument('--out',type=pathlib.Path,required=True)
args=parser.parse_args()
ROOT=args.out.resolve();ROOT.mkdir(parents=True,exist_ok=False)
SOURCE=args.reader.resolve()
TEST=args.tests.resolve()
MUTATIONS=[
 ('strict-boundary', 'compatible = difference <= width', 'compatible = difference < width', 'test_boundary_is_exact_inclusive_decimal'),
 ('union-instead-of-intersection', 'bid in accepted_sets["T1"] and bid in accepted_sets["T2"]', 'bid in accepted_sets["T1"] or bid in accepted_sets["T2"]', 'test_calibration_states_exhaustive_81'),
 ('forget-missing-validation', 'status = "unassessed" if "unassessed" in statuses else "incompatible" if "incompatible" in statuses else "compatible"', 'status = "incompatible" if "incompatible" in statuses else "compatible"', 'test_validation_states_exhaustive_81_preserves_S'),
 ('drop-failed-candidates', '"S_T2": accepted["T2"], "S": S,', '"S_T2": accepted["T2"], "S": [x["id"] for x in candidates if x["status"] == "compatible"],', 'test_validation_states_exhaustive_81_preserves_S'),
 ('ignore-unknown-predictions', '_obj(predictions, tid + ".predictions", ids)', '_obj(predictions, tid + ".predictions", predictions)', 'test_unknown_fields_ids_units_rejected_even_excluded_candidate'),
 ('trust-source-digest', 'if actual != expected:', 'if False:', 'test_artifact_and_contract_binding'),
 ('allow-reserved-seeds', 'or set(seeds) & RESERVED_CONFIRMATION_SEEDS', 'or False', 'test_seed_reserved_duplicates_and_overlap'),
 ('join-across-gap', 'previous_selected = bid in candidate_ids', 'previous_selected = bool(neighbor_groups)', 'test_groups_respect_registered_topology_and_unknown_gap'),
 ('empty-success', '"not-applicable" if not S else', '"all-compatible" if not S else', 'test_empty_grid_result_not_validation_success'),
 ('ignore-unit-mismatch', 'point["unit"] != rule["unit"]:', 'False:', 'test_unknown_fields_ids_units_rejected_even_excluded_candidate'),
 ('flat-is-missing', 'if not prediction["eligible"] or not experiment["eligible"]:', 'if not prediction["eligible"] or not experiment["eligible"] or "INSENSITIVE" in prediction.get("flags", []):', 'test_flat_valid_response_keeps_candidates_without_identifiability_claim'),
 ('binary-float-boundary', 'difference = abs(prediction["value"] - experiment["value"])', 'difference = abs(float(prediction["value"]) - float(experiment["value"]))', 'test_boundary_is_exact_inclusive_decimal'),
]
source=SOURCE.read_text()
results=[]
for name,old,new,target in MUTATIONS:
 if source.count(old)!=1: raise RuntimeError((name,source.count(old)))
 mutated=source.replace(old,new,1);ast.parse(mutated)
 folder=ROOT/'mutants'/name;folder.mkdir(parents=True,exist_ok=True)
 (folder/SOURCE.name).write_text(mutated)
 shutil.copyfile(TEST,folder/TEST.name)
 run=subprocess.run([sys.executable,'-I',str(folder/TEST.name),'DecisionTests.'+target],capture_output=True,text=True)
 (folder/'test.log').write_text(run.stdout+run.stderr)
 results.append({'name':name,'target':target,'rc':run.returncode,'syntactically_valid':True,'assertion_failed':'FAIL:' in run.stderr,'unexpected_error':'ERROR:' in run.stderr,'source_sha256':hashlib.sha256(mutated.encode()).hexdigest()})
report={'scope':'author mutation checks of synthetic decision tests; not independent review','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'test_sha256':hashlib.sha256(TEST.read_bytes()).hexdigest(),'count':len(results),'all_detected_by_assertion':all(x['rc']!=0 and x['assertion_failed'] and not x['unexpected_error'] for x in results),'results':results}
(ROOT/'mutation-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
sys.exit(0 if report['all_detected_by_assertion'] else 1)
