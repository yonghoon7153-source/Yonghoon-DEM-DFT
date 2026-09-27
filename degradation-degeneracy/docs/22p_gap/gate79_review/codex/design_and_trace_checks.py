"""Reviewer-authored arithmetic and symbolic examples, NOT subject code execution.
The source control-flow facts are separately bound by data_audit.py's AST checks.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import json
O=Path(__file__).resolve().parent
rows=[]
expected={(0,0):(0,0),(0,1):(1,1),(1,0):(-1,-1),(1,1):(0,0),
          (None,0):(-1,0),(None,1):(0,1),(0,None):(0,1),(1,None):(-1,0),(None,None):(-1,1)}
for a,b in product([0,1,None],repeat=2):
    ds=[y-x for x in ([0,1] if a is None else [a]) for y in ([0,1] if b is None else [b])]
    assert (min(ds),max(ds))==expected[(a,b)]
    rows.append({'y33':a,'y34':b,'lower':min(ds),'upper':max(ds)})
assert Fraction(1,38)>0 and Fraction(1-2,40)<0
forty={'N':40,'n':38,'m':2,'D':1,'delta_cc':str(Fraction(1,38)),
       'missing_as_fail':str(Fraction(-1,40)),'bound':[str(Fraction(-1,40)),str(Fraction(1,40))]}
bank_group='same_physics'
observations=[('p22_grid_primary_v6',bank_group,'none',0.01,seed,0) for seed in [1,2]]
assert len(set(observations))==2
assert sum(1 for a,b in product(observations,repeat=2) if a[1]==b[1])==4
assert sum(1 for a,b in product(observations,repeat=2) if a==b)==2

def trace(rounds):
    """Independent minimal state model of the statically checked assignment order.
    Finite is supplied as a boolean; no optimizer, objective, numpy or reviewed function is called.
    """
    ok=False;last=None;last_finite=None;best=None;best_f=None;count=0;outer='max_rounds'
    for i,r in enumerate(rounds,1):
        count+=1;last=r['success']
        if not r['finite']:outer='nonfinite';break
        previous=best_f;ok=r['success'];last_finite=i
        if best_f is None or r['fun']<best_f:best_f=r['fun'];best=r['success']
        if previous is not None and previous-r['fun']<1e-12:outer='no_improvement';break
    return {'legacy_ok':ok,'last_finite_round':last_finite,'native_last_success':last,
            'native_best_success':best,'outer':outer,'n_rounds':count,'retained_best_f':best_f}
cases=[
 ('finite_success_then_nonfinite_failure',[{'finite':True,'fun':1.,'success':True},{'finite':False,'success':False}],True,False),
 ('finite_failure_then_nonfinite_success',[{'finite':True,'fun':1.,'success':False},{'finite':False,'success':True}],False,True),
 ('first_nonfinite_failure',[{'finite':False,'success':False}],False,False),
 ('first_nonfinite_success',[{'finite':False,'success':True}],False,True),
 ('finite_success_then_worse_finite_failure',[{'finite':True,'fun':1.,'success':True},{'finite':True,'fun':1.5,'success':False}],False,False),
 ('no_rounds',[],False,None)]
traces=[]
for name,rounds,want,last in cases:
    out=trace(rounds);assert out['legacy_ok']==want and out['native_last_success']==last
    traces.append({'case':name,'input':rounds,'result':out})
result={'scope':'Reviewer arithmetic and independent symbolic model; source is parsed as AST elsewhere but never imported/called.',
 'nine_state_bounds':rows,'forty_pair_counterexample':forty,
 'pairing_example':{'same_bank_group_join_rows':4,'exact_obs_key_pairs':2},
 'empty_denominators':{'n_zero':'delta_cc undefined','N_zero':'all contrasts undefined'},
 'logging_traces':traces,
 'finding':'The statically preserved nonfinite break precedes updating ok; legacy_ok is not unconditionally the last native success.',
 'not_native_runtime_reproduction':True,'subject_program_runs':0}
p=O/'DESIGN_AND_SYMBOLIC_CHECKS.json'
with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','bounds_states':9,'pairing_example':1,'symbolic_logging_cases':6,'subject_runs':0}))
