"""Synthetic-only review. No target edits and no real-data fits.
Run: python repro_followup3.py --target /path/to/bms-balancing --part fast|producer
GC targets are created and checked beneath this script's fresh fixture directory.
rc=0 means diagnostic completion, not product acceptance.
"""
import argparse, copy, csv, datetime, hashlib, importlib.util, io, json, os
import pathlib, subprocess, sys, tempfile, time
from unittest.mock import patch
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
ap=argparse.ArgumentParser();ap.add_argument('--target',required=True,type=pathlib.Path)
ap.add_argument('--part',choices=['fast','producer'],default='fast');a=ap.parse_args()
ROOT=a.target.resolve();HERE=pathlib.Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'tests'),str(ROOT/'scripts'),str(ROOT/'reviews')]
from bms_balancing import cycles as C, schema as S, data as D, verify as V
from test_widths import _fake_widths_csv
import evidence_gate as G
FIX=pathlib.Path(tempfile.mkdtemp(prefix='new-'+a.part+'-',dir=HERE)).resolve()
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
RESULT={}
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-c','http.sslBackend=openssl',*args],cwd=ROOT,text=True).strip()
def persist():dump(HERE/('NEW_'+a.part.upper()+'_RESULTS.json'),dict(head=git('rev-parse','HEAD'),fixture=str(FIX),cases=RESULT))
def run(name,script,*args):
 cmd=[sys.executable,str(ROOT/script),*map(str,args)]
 r=subprocess.run(cmd,cwd=ROOT,env=ENV,capture_output=True,text=True,encoding='utf-8',timeout=180)
 RESULT[name]=dict(command=cmd,rc=r.returncode,stdout=r.stdout,stderr=r.stderr)
 (HERE/(name+'.log')).write_text(r.stdout+'\nSTDERR\n'+r.stderr,encoding='utf-8');persist();return r
def snapshot(p):return {q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file()}
def gc_case(name,mode):
 out=FIX/name;part=out/'partial';entries=[]
 for att,body in [('A','old registered bytes'),('B','retained registered bytes')]:
  p=part/'matrix'/att/'matrix_100.csv';p.parent.mkdir(parents=True);p.write_text(body,encoding='utf-8')
  entries.append(dict(attempt=att,kind='matrix',artifact=p.name,status='partial',path=p.relative_to(part).as_posix(),sha256=sha(p),recorded_utc=att))
 old=part/'matrix/A/matrix_100.csv';new=part/'matrix/B/matrix_100.csv'
 if mode=='changed':old.write_text('DIFFERENT UNREGISTERED BYTES at same indexed pathname',encoding='utf-8')
 if mode=='missing-retained':new.unlink()
 if mode=='unindexed':(old.parent/'unknown.txt').write_text('do not delete',encoding='utf-8')
 dump(part/'index.json',dict(index_version=1,attempts=entries))
 for q in out.rglob('*'):
  assert not q.is_symlink() and q.resolve().is_relative_to(FIX)
 for e in entries:assert (part/e['path']).resolve().is_relative_to(FIX)
 before=snapshot(out);run(name,'scripts/gc_partial.py','--root',out,'--keep','1','--apply')
 RESULT[name].update(before=before,after=snapshot(out),index=json.loads((part/'index.json').read_text(encoding='utf-8')))
 persist()

if a.part=='fast':
 for name,mode in [('gc_valid_control','valid'),('gc_changed_bytes','changed'),('gc_missing_retained','missing-retained'),('gc_unindexed_control','unindexed')]:gc_case(name,mode)
 # Common-receipt cycle must not silently contradict the per-cycle body.
 for val in [None,999]:
  name='common_cycle_control' if val is None else 'common_cycle_999'
  p=_fake_widths_csv(FIX/name,'cycles_syn_Li.csv',w_dqdv=0)
  mp=p.with_name(p.name+'.meta.json');m=json.loads(mp.read_text(encoding='utf-8'))
  m.update(git_commit=git('rev-parse','HEAD'),dataset_manifest=D.half_cell_manifest_identity())
  if val is not None:m['consumed_inputs']['full_cell']['cycle']=val
  dump(mp,m);run(name,'scripts/width_report.py',p)
 # Typed-invalid receipt must give a structured rejection, not AttributeError.
 base=G.run_receipt(head=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}'),
  instrument={'reviews/evidence_gate.py':git('rev-parse','HEAD:./reviews/evidence_gate.py')},
  package_digest='a'*64,materialized=None,runtime={'python':sys.version.split()[0],'platform':sys.platform})
 for name,change in [('receipt_valid_control',{}),('receipt_code_null',{'code':None}),('receipt_instrument_list',{'instrument':['not-a-map']}),('receipt_tree_instead_of_blob',{'instrument':{'bms_balancing':git('rev-parse','HEAD:./bms_balancing')}})]:
  r=copy.deepcopy(base);r.update(change);r['signature']=G.receipt_signature(r);p=FIX/(name+'.json');dump(p,r)
  run(name,'scripts/verify_run_receipt.py','--receipt',p,'--target',ROOT)
 # Explicit solver-return fault injection, NOT evidence that SciPy natively emits it.
 best=np.array([3.,0.,3.,0.,.1]);lo=best.copy();hi=best.copy();lo[0]=2.5;hi[0]=3.5
 from types import SimpleNamespace
 def fault(fun,x0,**kw):return SimpleNamespace(fun=0.,x=np.array([25.,0.,3.,0.,.1]),success=False)
 try:
  with patch.object(V,'minimize',fault):
   rr=V.near_optimal_extrema(lambda x:1.,best,3.,3.,best,1.,tol=0.,seeds=[],n_starts=0,seed=0,lb=lo,ub=hi)
  RESULT['optimizer_out_of_box_fault']=dict(returned=rr,expected_PE_range=[-100/6,100/6],injected_x=[25,0,3,0,.1],injected_success=False)
 except Exception as e:RESULT['optimizer_out_of_box_fault']=dict(exception=type(e).__name__,message=str(e))
 persist()
else:
 from test_r6_internal import _synth_root
 from test_cycles import _cycle_workbook
 from provenance import git_provenance,sidecar_dict
 src=_synth_root(FIX);wb=_cycle_workbook(src,FIX/'syn.xlsx',n_cycles=2);arts=[]
 for starts in [1,2]:
  t=time.monotonic();runid='review-synthetic-starts-'+str(starts)
  res=C.fit_cycles(src,src/'data/half_cell/GITT/pristine.xlsx',wb,'Li',cell='syn',
   objective_version='legacy_matlab',n_starts=starts,seed=0,scale_seed=0,run_id=runid,
   widths=True,width_tol=.01,width_starts=0,width_grid=0)
  dest=FIX/('n'+str(starts));dest.mkdir();art=dest/'cycles_syn_Li.csv'
  with art.open('w',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,fieldnames=S.CYCLES_ROW,lineterminator='\n');w.writeheader();w.writerows(res['rows'])
  pv=git_provenance(cwd=str(ROOT));extra={'cell':'syn','si_source':'Li','starts':starts,'seed':0,'scale_seed':0,'w_dqdv':0.,'cycles':res['cycles'],'status':'complete','dataset_manifest':D.half_cell_manifest_identity(),'consumed_inputs':res['consumed'],**res['settings']}
  meta=sidecar_dict(art.name,art.read_bytes(),run_id=runid,started={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'git':pv},argv=['review-synthetic-API-fixture'],pv=pv,extra=extra)
  dump(art.with_name(art.name+'.meta.json'),meta);arts.append(art)
  run('starts'+str(starts)+'_single','scripts/width_report.py',art)
  RESULT['starts'+str(starts)+'_single'].update(seconds=time.monotonic()-t,scope='real fit_cycles synthetic inputs; review serialization; NOT production publication CLI')
  persist()
 run('starts_axis_compare','scripts/width_report.py',*arts,'--axis','starts')
 run('n_multistart_axis_compare','scripts/width_report.py',*arts,'--axis','n_multistart')
persist();print(json.dumps({k:v.get('rc',v.get('exception','observed')) for k,v in RESULT.items()},ensure_ascii=True,indent=2))
