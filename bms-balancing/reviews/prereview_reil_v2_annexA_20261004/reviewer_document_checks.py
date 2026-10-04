"""Reviewer-only byte and arithmetic checks, no REIL data or supplied program execution."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

root = Path(__file__).resolve().parent
expected = {
    'REIL_V2_ANNEX_A_REREVIEW_REQUEST_20261004.md':'d10b75f714377ebf68d47998bd03112b97c0454a',
    'REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md':'9f49d6061cf3c9e69ed35e3b00e5e0addafd8fd3',
    'REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md':'872ca88b3b5c57aebf295bd0109e95a830b3ae13',
    'PRIOR_REVIEW_KO.md':'3b02fe6dd2660f2c7da8383f232606cbf58986f7',
}
files=[]
for name, blob in expected.items():
    b=(root/'reference'/name).read_bytes()
    measured=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert measured == blob
    files.append({'file':'reference/'+name, 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest(), 'git_blob_sha1':measured, 'matches_fixed_ref':True})
assert (root/'reference/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md').read_bytes()==(root.parent/'reil_v2_prereview_20261004/reference/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md').read_bytes()
assert (root/'reference/PRIOR_REVIEW_KO.md').read_bytes()==(root.parent/'reil_v2_prereview_20261004/REVIEW_KO.md').read_bytes()

local_per_unit=128+3*46*4+2*16+1
assert local_per_unit==713
assert local_per_unit*77==54901
assert local_per_unit*77*2000+77*201==109817477
assert 11*(20+5)==275
ratios={
    'zero_margin_tau002_lower': F('0.0001')/F('0.04'),
    'nominal_010_lower':F('0.0001')/F('0.10'),
    'nominal_010_upper':F('0.5')/F('0.10'),
    'nominal_020_lower':F('0.0001')/F('0.20'),
    'nominal_020_upper':F('0.5')/F('0.20'),
    'nominal_013_lower':F('0.0001')/F('0.13'),
    'nominal_013_upper':F('0.5')/F('0.13'),
    'nominal_006_lower':F('0.0001')/F('0.06'),
    'nominal_006_upper':F('0.5')/F('0.06'),
    '020_tau002_lower':F('0.0001')/F('0.24'),
    '020_tau002_upper':F('0.5')/F('0.16'),
    '020_tau005_lower':F('0.0001')/F('0.30'),
    '020_tau005_upper':F('0.5')/F('0.10'),
}
assert list(map(str,ratios.values()))==['1/400','1/1000','5','1/2000','5/2','1/1300','50/13','1/600','25/3','1/2400','25/8','1/3000','5']

eps=F('1e-10')
dp,dn=F(float('0.1')),F(float('0.09990000005'))
g_residual=F('0.0001')-(dp-dn)
assert 0<g_residual<eps
mp=F(float('1.02000000005'))
nominal_residual=abs(mp-F(1))-F('0.02')
assert 0<nominal_residual<eps

# A synthetic scalar interpolation example, not a REIL curve evaluation.
upper=0.1
step=upper/999
q0,q1,q2=0.0,step,2*step
v0,v1,v2,cutoff=1.1,2.0,2.5,2.0
left=q0+(cutoff-v0)*(q1-q0)/(v1-v0)
right=q1+(cutoff-v1)*(q2-q1)/(v2-v1)
assert left != right and right==q1

report={
    'scope':'Only fixed-text identity, exact rational arithmetic, and a scalar binary64 interpolation counterexample. Not P0, REIL objective evaluation, fitting, implementation validation or empirical data processing.',
    'source_files':files,
    'v2_and_prior_review_match_previous_local_copies':True,
    'budget_arithmetic':{'local_per_unit':local_per_unit,'units':77,'local_total':54901,'objective_call_cap_excluding_separate_items':109817477,'E3a_optimizer_calls':275},
    'constant_rational_boundaries':{k:str(v) for k,v in ratios.items()},
    'constraint_tolerance_counterexamples':{
        'G':{'dP':float(dp),'dN':float(dn),'exact_rational_residual':str(g_residual),'residual_approx':float(g_residual),'strict_G_satisfied':False,'within_1e_minus10':True},
        'nominal_box':{'mP':float(mp),'nominal_mP':1,'tau':'0.02','exact_rational_residual':str(nominal_residual),'residual_approx':float(nominal_residual),'strict_nominal_box_satisfied':False,'within_1e_minus10':True},
        'limitation':'These are constraint-only examples. No assertion that a real REIL objective passes its threshold at these points.'
    },
    'cutoff_endpoint_counterexample':{'grid':'1000 uniform points on [0,0.1], first three nodes only','Q':[q0,q1,q2],'V':[v0,v1,v2],'cutoff':cutoff,'left_formula_result':left,'right_formula_result':right,'difference':left-right,'same_float_dedup_would_merge':left==right,'exact_shared_node':q1,'limitation':'Synthetic arithmetic, not a measured half-cell curve or supplied H4 implementation run.'},
    'provided_programs_executed':False,'data_files_opened':False,'P0_executed':False,'optimizer_executed':False,
}
(root/'REVIEW_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'source_blobs':len(files),'all_match':True,'budget_arithmetic':'MATCH','rational_constants':'MATCH','G_residual':float(g_residual),'nominal_residual':float(nominal_residual),'cutoff_left':left,'cutoff_right':right,'P0':False,'fitting':False}))
