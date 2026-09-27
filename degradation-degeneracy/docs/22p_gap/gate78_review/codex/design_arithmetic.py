"""Algebraic counterexamples only. No repository import, solver, data analysis or tests."""
from pathlib import Path
from itertools import product
from fractions import Fraction
from collections import Counter
import json
O=Path(__file__).resolve().parent
def frac(n,d):return str(Fraction(n,d))

# 0=pass, 1=raw-degeneracy fail, None=unobserved label.
rows=[]
for a,b in product((0,1,None),repeat=2):
    choices_a=(0,1) if a is None else (a,)
    choices_b=(0,1) if b is None else (b,)
    values=sorted({bb-aa for aa,bb in product(choices_a,choices_b)})
    imputed=(1 if b is None else b)-(1 if a is None else a)
    rows.append({'label_33':a,'label_34':b,'admissible_d':values,
                 'lower':min(values),'upper':max(values),'missing_as_fail_d':imputed,
                 'is_upper_bound':imputed==max(values)})
assert next(r for r in rows if r['label_33'] is None and r['label_34']==0)['is_upper_bound'] is False
assert next(r for r in rows if r['label_33'] is None and r['label_34'] is None)['upper']==1

# Same latent bank family, two noise realizations: match by realization, not group alone.
left=[{'group':'G','seed':'s1','label':0},{'group':'G','seed':'s2','label':1}]
right=[{'group':'G','seed':'s1','label':1},{'group':'G','seed':'s2','label':0}]
correct=[(a['label'],b['label']) for a in left for b in right if (a['group'],a['seed'])==(b['group'],b['seed'])]
group_only=[(a['label'],b['label']) for a in left for b in right if a['group']==b['group']]
def counts(pairs):return {f'{a}->{b}':sum(1 for x in pairs if x==(a,b)) for a,b in product((0,1),repeat=2)}
assert len(correct)==2 and len(group_only)==4
pairing={'planned_observation_pairs':2,'same_pair_group_id':True,'correct_table':counts(correct),
 'group_only_many_to_many_table':counts(group_only),'correct_n':2,'incorrect_n':4,
 'correct_delta':frac(sum(b-a for a,b in correct),len(correct)),
 'incorrect_delta':frac(sum(b-a for a,b in group_only),len(group_only)),
 'note':'Delta happens to agree at zero; transition counts and denominator are still wrong.'}

# Forty planned pairs, thirty-eight complete, sum(d)=+1; two missing 33 with observed 34 pass.
N,n,m,D=40,38,2,1
example={'N':N,'n_complete':n,'m_missing_pairs':m,'complete_sum_d':D,
 'missing_pattern':'2 x (33 unknown, 34 pass)',
 'missing_fraction':frac(m,N),'request_over_5pct_gate_fires':m*100>N*5,
 'complete_pair_delta':frac(D,n),'missing_as_fail_delta_full_planned_denominator':frac(D-m,N),
 'sharp_full_planned_lower':frac(D-m,N),'sharp_full_planned_upper':frac(D,N),
 'sign_flip_in_imputed_point_estimate':True}
assert example['request_over_5pct_gate_fires'] is False
assert Fraction(D,n)>0 and Fraction(D-m,N)<0 and Fraction(D,N)>0

# A positive missing count below 5% is allowed by the proposed rule but not a zero-failure gate.
zero_gate={'N':100,'missing_due_to_solver_failure':1,'over_5pct':1*100>100*5,
 'violates_zero_solver_failure':True,
 'note':'If 5% is a separate reporting policy it must not replace section6.2 solver-health acceptance.'}
out={'scope':'Reviewer-owned finite algebra and fabricated rows; not subject code regression or actual scientific results',
 'head':'720f0a0e466afb595fbd73a50f89416898cc927c','labels':{'pass':0,'raw_degeneracy_fail':1,'unobserved':None},
 'contribution':'d = label_34 - label_33; positive means 34 has more failures',
 'single_pair_state_table':rows,'state_table_count':len(rows),'pairing_counterexample':pairing,
 'missing_sensitivity_counterexample':example,'zero_gate_distinction':zero_gate,
 'recommended_formula':{'complete_pair':'D/n, n>0; label as complete-pair conditional descriptive statistic',
  'full_planned_bound':'[(D + sum(lower_i))/N, (D + sum(upper_i))/N], N>0',
  'looser_conservative_bound':'[(D-m)/N, (D+m)/N]; may ignore known one-sided outcomes',
  'not_a_confidence_interval':True,'no_claim_of_missing_at_random':True},
 'subject_imports':0,'solver_calls':0,'provided_tests_executed':0}
with (O/'DESIGN_ARITHMETIC.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':'DESIGN_ARITHMETIC_COMPLETE','label_state_rows':9,
 'pairing_rows_correct':2,'pairing_rows_group_only':4,'missing_counterexample':example},ensure_ascii=False))
