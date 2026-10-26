"""Adapt original registration inputs only; original file and production files remain untouched."""
import argparse, hashlib, importlib.util, json, os, sys
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument('--repo',required=True); ap.add_argument('--original',required=True); ap.add_argument('--label',required=True)
a=ap.parse_args()
repo=Path(a.repo).resolve(); original=Path(a.original).resolve(); root=Path(__file__).resolve().parents[2]
os.environ['RINT_REVIEW_SOURCE']=str(repo)
sp=importlib.util.spec_from_file_location('original_registration',original)
m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
# Redirect ONLY probe-owned fixtures; loading the original never invokes main().
dest=root/'tmp'/'chain'/a.label; dest.mkdir(parents=True,exist_ok=True)
m.__file__=str(dest/'probe_registration_current.py')
old_arm=m.arm
def arm(s,err=0.0):
    r=old_arm(s,err)
    r.update(target_lo=1.0-err if s else None,target_hi=1.0+err if s else None,scale=float(s) if s else None)
    return r
m.arm=arm
names={'RCA01':'rca01','passive_endpoint_sweep':'endpoint_sweep','certificate_padding':'guard_padding',
 'PRE2_impl03':'plan_validation','SBE_origin_union':'sbe_origin_union','RCA02_and_origin_scope':'dbe_origin',
 'RCA08_09_10_13':'logic','DBE_R_monotonicity':'dbe_nonmonotone','SV_all3_origin_scope':'sv_origin_scope','time_estimate':'budget'}
out={}
for key,fn in names.items():
    try: out[key]=getattr(m,fn)()
    except m.rr.Stop as e: out[key]={'stopped':e.code,'cause':e.cause}
meta={'repo':str(repo),'original':str(original),'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
 'python':sys.version,'source_hashes':{p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in
 ('scripts/rint_r_chain.py','scripts/run_contract.py','scripts/ca_ext_svcf.py','scripts/step3_conv_cert.py')},
 'adaptation':'arm adds target_lo=1-err,target_hi=1+err,scale=sigma; zero fields None; Stop recorded; no behavior change to production'}
output=Path(__file__).with_name('registration_'+a.label+'.json')
output.write_text(json.dumps({'meta':meta,'results':out},ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
print(json.dumps({'output':str(output),'DBE_R_monotonicity':out['DBE_R_monotonicity'],
 'origin':out['RCA02_and_origin_scope'],'SV_counts':out['SV_all3_origin_scope']['sv_enabled_counts']},ensure_ascii=False,indent=2))

