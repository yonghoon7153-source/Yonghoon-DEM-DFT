"""Synthetic plan/source binding checks only; no real S0 or registered plan written."""
import copy
import hashlib
import importlib
import json
import sys
from pathlib import Path

repo=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
sys.path.insert(0,str(repo/'scripts'))
s0=importlib.import_module('ca_s0_census')
rr=importlib.import_module('rint_r_chain')
source={'tool':s0.TOOL_VERSION,'tool_sha256':'a'*64,'stage':1,'kit_name':'SYNTHETIC_ONLY'}
p1,b1,h1=s0.make_plan(.05,s0.R_F_UM,s0.GAP_TOL_PRODUCTION,source)
source2=dict(source,tool_sha256='b'*64)
p2,b2,h2=s0.make_plan(.05,s0.R_F_UM,s0.GAP_TOL_PRODUCTION,source2)
files=[{'file':name,'sha256':hashlib.sha256((repo/'scripts'/name).read_bytes()).hexdigest()} for name in rr.S0_SAME_FILES]
rec={'file_digests':copy.deepcopy(files)}
valid=rr.s0_code_problem(rec,'synthetic',files)
bad=copy.deepcopy(rec)
next(x for x in bad['file_digests'] if x['file']=='carbon_junction.py')['sha256']='0'*64
why=rr.s0_code_problem(bad,'synthetic',files)
record={'plan_source_only_change':{
    'numbers_identical':p1['values_um']==p2['values_um'],'integers_identical':p1['integers']==p2['integers'],
    'formulas_identical':p1['formulas']==p2['formulas'],'bytes_different':b1!=b2,
    'hash_different':h1!=h2,'hash1':h1,'hash2':h2},
    'code_binding':{'current':valid,'old_carbon':why,'expected_code_files':list(rr.S0_SAME_FILES)},
    'limits':'The source SHA strings are synthetic. This tests structural dependence only, not actual field provenance.'}
record['passed']=all(record['plan_source_only_change'][k] for k in ('numbers_identical','integers_identical','formulas_identical','bytes_different','hash_different')) and valid is None and why is not None
out.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(record,ensure_ascii=False))
raise SystemExit(0 if record['passed'] else 1)
