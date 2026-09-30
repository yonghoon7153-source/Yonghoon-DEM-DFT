"""Disclosed Windows fixture controls and legacy-output comparison, no source edits."""
import sys, os, json, io, contextlib, importlib.util, builtins, shutil
from pathlib import Path
E=Path(__file__).resolve().parent; C=E.parent/'candidate'; W=E.parent.parent
B=W/'lhs_coverage_review_20260930/baseline'
sys.path[:0]=[str(C/'scripts'),str(W/'lhs_coverage_review_20260930/deps')]
import numpy as np
import lhs_descriptor_harvest as h
sp=importlib.util.spec_from_file_location('baseline_harvest',B/'scripts/lhs_descriptor_harvest.py')
old=importlib.util.module_from_spec(sp);sys.modules[sp.name]=old;sp.loader.exec_module(old)
comparisons=[]
saved=h.harvest
def compare(*a,**kw):
    n=saved(*a,**kw)
    try:b=old.harvest(*a,**kw)
    except old.BedRefusal:return n
    keys=[k for k in b if k not in ['wall_touch','wall_touch_rule']]
    mism=[k for k in keys if json.dumps(b[k],sort_keys=True,default=str)!=json.dumps(n[k],sort_keys=True,default=str)]
    comparisons.append(dict(case=n['case'],old_keys_compared=len(keys),mismatch=mism))
    return n
h.harvest=compare
origopen=builtins.open
def lfopen(file,mode='r',*a,**kw):
    if 'w' in mode and 'b' not in mode and 'newline' not in kw:kw['newline']='\n'
    return origopen(file,mode,*a,**kw)
builtins.open=lfopen
buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):rc=h.selftest()
finally:h.harvest=saved;builtins.open=origopen
(E/'harvest_LF_control.log').write_text(buf.getvalue(),encoding='utf-8')
xyz=np.random.default_rng(7).uniform([0,0,.3],[10,10,19.7],size=(900,3))
atoms={k:xyz[:,i] for i,k in enumerate(['x','y','z'])};atoms['radius']=np.full(900,.6)
arg=(atoms,np.array(['SE']*900),np.zeros(3),np.array([10.,10.,20.]))
ot=old.tortuosity_se(*arg,plate_z=20.);nt=h.tortuosity_se(*arg,plate_z=20.)
R=dict(harvest_LF_control=dict(returncode=rc,failures=h._FAILS,comparisons=comparisons,
    tau_baseline={k:ot[k] for k in ['tau_mean','tau_median','n_sampled','n_valid']},
    tau_candidate={k:nt[k] for k in ['tau_mean','tau_median','n_sampled','n_valid']},tau_equal=ot==nt))
import lhs_webapp_batch as batch
origlink=Path.symlink_to
def copyshim(self,target,target_is_directory=False):
    assert not target_is_directory
    shutil.copyfile(target,self)
Path.symlink_to=copyshim
buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):rc=batch._selftest()
finally:Path.symlink_to=origlink
(E/'batch_copy_control.log').write_text(buf.getvalue(),encoding='utf-8')
R['batch_copy_control']=dict(returncode=rc,note='Only symlink_to replaced by byte-copy in process. NOT deployment symlink certification.')
(E/'regression_results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(R,ensure_ascii=False,indent=2))
