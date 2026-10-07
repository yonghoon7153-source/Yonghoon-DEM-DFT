"""Same pinned production analysis, changed reviewer-only dependency; no production edits."""
from pathlib import Path
import sys,json,shutil,importlib.util,contextlib,io
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];S=R/'source';D=R/'evidence/dependency_gap';D.mkdir(exist_ok=True)
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import run_network_194_parallel as rn,dem_analysis_core as dc
alt=R/'tmp/dependency_alt';alt.mkdir(exist_ok=True)
for rel in set(rn.CODE_FILES)|{'scripts/fracture_model.py'}:
 p=alt/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/rel,p)
cl0=rn.code_dependency_closure(alt);fp0=rn.code_fp(rn.code_hashes(alt))
def load(p):
 spec=importlib.util.spec_from_file_location('fracture_model',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
atoms={1:dict(type=1,radius=.006,x=0.,y=0.,z=.006),2:dict(type=1,radius=.006,x=.0118,y=0.,z=.006)}
contacts=[dict(id1=1,id2=2,delta=.0002,fn=0.)]
with patch.dict(sys.modules,{'fracture_model':load(alt/'scripts/fracture_model.py')}):a=dc.calc_fracture_stages(atoms,contacts,{1:'AM_P'},scale=1000.)
p=alt/'scripts/fracture_model.py';s=p.read_text(encoding='utf8');assert 'K_IC_AM_P = 0.3e6' in s
p.write_text(s.replace('K_IC_AM_P = 0.3e6','K_IC_AM_P = 30.0e6'),encoding='utf8')
with patch.dict(sys.modules,{'fracture_model':load(p)}):b=dc.calc_fracture_stages(atoms,contacts,{1:'AM_P'},scale=1000.)
cl1=rn.code_dependency_closure(alt);fp1=rn.code_fp(rn.code_hashes(alt))
out=dict(fixture='two AM_P spheres r=6 um, delta=0.2 um, force channel absent; no physical claim',change='reviewer copy: K_IC_AM_P 0.3e6 -> 30e6 Pa m^0.5',source_call='dem_analysis_core.calc_fracture_stages (called by run_full_analysis)',hash_before=fp0,hash_after=fp1,hash_unchanged=fp0==fp1,closure_before=cl0,closure_after=cl1,fracture_model_in_closure='scripts/fracture_model.py' in cl1['files'],changed_metrics={k:[a.get(k),b.get(k)] for k in set(a)|set(b) if a.get(k)!=b.get(k)},baseline=a,mutant=b)
(R/'evidence/dependency_gap.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in out.items() if k not in ('baseline','mutant','closure_before','closure_after')},ensure_ascii=False,indent=2))
