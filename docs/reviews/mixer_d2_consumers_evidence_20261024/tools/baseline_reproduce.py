#!/usr/bin/env python3
"""Reproduce the three legacy consumer limitations, without a simulator."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scripts', type=Path, default=Path(__file__).parent/'scripts')
    ap.add_argument('--baseline', type=Path, default=Path(__file__).parent/'baseline')
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    sys.path.insert(0,str(a.scripts))
    f = module('d2_fixtures',a.scripts/'test_mixer_d2_consumers.py')
    rb = module('baseline_readback',a.baseline/'mixer_deck_readback.py')
    dd = module('baseline_diff',a.baseline/'mixer_deck_diff.py')
    smoke = module('baseline_smoke',a.baseline/'mixer_smoke_blind.py')
    uncoated,um,lab_counts = f.fixture()
    coated,cm,_ = f.fixture(coated=True)
    soft,sm,_ = f.fixture(stiff=1.)
    gen1,gm,gen1_counts = f.fixture(generation='gen1')
    legacy_counts = {str(k):v for k,v in smoke._expected_counts({'stiffen_se':20}).items()}
    old_table = rb.compare('E',rb.read_deck(soft,label='lab_soft'),rb.read_deck(uncoated,label='lab20'))
    old_diffs = {allow:dd.diff_decks(uncoated,coated,allow=allow)['verdict'] for allow in ['A','B','U','E','EB']}
    result = dict(baseline_pin='486a57cf58d3e0d93ef79be6aae50968929099c0',
        scope='Synthetic text reproduction only; no run or registration',
        inputs=dict(n_total=100000,cgf=151.4,rho=.3,bo=.73),
        baseline_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(a.baseline.glob('*.py'))},
        old_readback_lab_table=old_table,
        old_d2_pair_allow_results=old_diffs,
        gen1_actual_plan=gen1_counts,lab_actual_plan=lab_counts,old_smoke_counts=legacy_counts,
        reproduced=dict(lab_readback_rejected=old_table['verdict']=='FAIL',
            no_d2_comparison=all(v=='FAIL' for v in old_diffs.values()),
            smoke_lab_plan_mismatch=legacy_counts!=lab_counts and legacy_counts==gen1_counts),
        new_readback=f.rb.read_d2(uncoated,um),new_pair=f.dd.diff_d2_decks(uncoated,coated,um,cm),
        new_plan=f.smoke.d2_plan_check(uncoated,um))
    result['all_reproduced']=all(result['reproduced'].values())
    result['new_development_paths_pass']=all(result[k]['verdict']=='PASS' for k in ['new_readback','new_pair','new_plan'])
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ['reproduced','gen1_actual_plan','lab_actual_plan','old_smoke_counts','all_reproduced','new_development_paths_pass']},ensure_ascii=False,indent=2))
    return 0 if result['all_reproduced'] and result['new_development_paths_pass'] else 1

if __name__=='__main__':
    raise SystemExit(main())
