import os,sys,json,importlib.util,contextlib,io,builtins
from pathlib import Path
E=Path(__file__).resolve().parent
ROOT=E.parent/'lhs_coverage_review_20260930'; C=Path(os.environ.get('LHS_REVIEW_REPO',ROOT/'candidate'))
B=Path(os.environ.get('LHS_REVIEW_BASELINE',ROOT/'baseline'))
sys.path[:0]=[str(C/'scripts'),str(ROOT/'deps')]
import lhs_descriptor_harvest as h
sp=importlib.util.spec_from_file_location('baseline_harvest',B/'scripts/lhs_descriptor_harvest.py')
old=importlib.util.module_from_spec(sp);sys.modules[sp.name]=old;sp.loader.exec_module(old)
results=[]; saved=h.harvest
def compare(*a,**kw):
    n=saved(*a,**kw)
    try:
        b=old.harvest(*a,**kw)
    except old.BedRefusal:
        return n  # Intentional selftest mutant disables the candidate time gate only.
    keys=[k for k in b if k not in ['wall_touch','wall_touch_rule']]
    mism=[k for k in keys if json.dumps(b[k],sort_keys=True,default=str)!=json.dumps(n[k],sort_keys=True,default=str)]
    results.append({'case':n['case'],'old_keys_compared':len(keys),'mismatch':mism})
    return n
h.harvest=compare
# Generated raw files use platform-default CRLF; normalize only fixture writes
# to LF here, the Linux producer convention. Production source is unchanged.
origopen=builtins.open
def lfopen(file,mode='r',*a,**kw):
    if 'w' in mode and 'b' not in mode and 'newline' not in kw:
        kw['newline']='\n'
    return origopen(file,mode,*a,**kw)
builtins.open=lfopen
buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
        result=h.selftest()
finally:
    h.harvest=saved;builtins.open=origopen
(E/'harvest_LF_control.log').write_text(buf.getvalue(),encoding='utf-8')
summary={'selftest_return':result,'selftest_failures':h._FAILS,'old_new_calls':len(results),'legacy_comparisons':results,'LF_fixture_shim':True}
import numpy as np
xyz=np.random.default_rng(7).uniform([0,0,.3],[10,10,19.7],size=(900,3))
atoms={k:xyz[:,i] for i,k in enumerate(['x','y','z'])};atoms['radius']=np.full(900,.6)
arg=(atoms,np.array(['SE']*900),np.zeros(3),np.array([10.,10.,20.]))
oldtau=old.tortuosity_se(*arg,plate_z=20.)
newtau=h.tortuosity_se(*arg,plate_z=20.)
summary['tau_platform_control']={'base':{k:oldtau[k] for k in ['tau_mean','tau_median','n_sampled','n_valid']},'candidate':{k:newtau[k] for k in ['tau_mean','tau_median','n_sampled','n_valid']},'same':oldtau==newtau}
(E/'harvest_comparison.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='legacy_comparisons'},ensure_ascii=False))
print('legacy mismatch', [r for r in results if r['mismatch']])
