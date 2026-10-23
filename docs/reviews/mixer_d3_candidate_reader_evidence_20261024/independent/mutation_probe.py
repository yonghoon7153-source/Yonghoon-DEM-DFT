#!/usr/bin/env python3
"""Independent guard-removal tests; never modifies the reviewed source."""
from pathlib import Path
import argparse, subprocess, sys, json, hashlib
parser=argparse.ArgumentParser(); parser.add_argument('--module',required=True,type=Path); parser.add_argument('--out',required=True,type=Path); args=parser.parse_args()
root=Path(__file__).resolve().parent; code=args.module.read_text(); target=args.out; target.mkdir(exist_ok=False)
cases=[('boundary_exclusive','compatible = difference <= width','compatible = difference < width','exact_inclusive_boundary'),('intersection_union','if bid in accepted_sets["T1"] and bid in accepted_sets["T2"]','if bid in accepted_sets["T1"] or bid in accepted_sets["T2"]','missing_uncertainty_UNASSESSED'),('bridge_unknown_gap','previous_selected = bid in candidate_ids','previous_selected = True','unknown_gap_not_bridged'),('missing_uncertainty_accepted','required.add("uncertainty")','pass  # mutation: missing uncertainty accepted','missing_uncertainty_UNASSESSED'),('reserved_seed_check_removed','or set(seeds) & RESERVED_CONFIRMATION_SEEDS','or False','reserved_seeds_nine_cases'),('source_bytes_check_removed','if actual != expected:','if False:','changed_raw_bytes_rejected'),('incompatible_beats_incomplete','status = "unassessed" if "unassessed" in statuses else "incompatible" if "incompatible" in statuses else "compatible"','status = "incompatible" if "incompatible" in statuses else "unassessed" if "unassessed" in statuses else "compatible"','validation_incomplete_precedence')]
results=[]
for name,old,new,expected in cases:
 assert code.count(old)==1,(name,code.count(old)); folder=target/name; folder.mkdir(); mutant=folder/'mixer_d3_candidates.py'; mutant.write_text(code.replace(old,new))
 cp=subprocess.run([sys.executable,'-I','-B',str(root/'probe_independent.py'),'--module',str(mutant),'--out',str(folder/'results')],capture_output=True,text=True)
 (folder/'stdout.log').write_text(cp.stdout); (folder/'stderr.log').write_text(cp.stderr)
 found=cp.returncode!=0 and 'AssertionError' in cp.stderr and expected in cp.stderr
 results.append({'mutation':name,'rc':cp.returncode,'expected_failure':expected,'expected_assertion_detected':found,'mutant_sha256':hashlib.sha256(mutant.read_bytes()).hexdigest()})
 assert found,(name,cp.stderr)
(target/'summary.json').write_text(json.dumps(results,indent=2)+'\n'); print(json.dumps({'mutations':len(results),'expected_assertions':sum(x['expected_assertion_detected'] for x in results)}))
