"""Ordinary startup/path fixtures, no receipt forgery or target file edits."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,tempfile
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True)
p.add_argument('--full-sandbox',action='store_true');p.add_argument('--case',action='append')
a=p.parse_args();root=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(root/'docs/22p_gap'))
import mutation_replay as mr
assert mr.ROOT==root
initial_env=dict(os.environ);initial_sandbox=mr.SANDBOX
records=[]
cases=['plain','explicit','remove_loaded_path','reorder_loaded_path','cwd_only_candidate','cwd_on_pythonpath','namespace']
if a.case:cases=a.case
for case in cases:
 d=out/case;d.mkdir();start=d/'startup';start.mkdir();other=d/'other';other.mkdir()
 if a.full_sandbox:cwd=mr._make_sandbox()
 else:cwd=d/'replay';cwd.mkdir()
 content='# ordinary startup\n'
 if case=='explicit':content='import usercustomize\n'
 if case=='remove_loaded_path':content="import os,sys\n_here=os.path.dirname(__file__)\nsys.path[:]=[p for p in sys.path if os.path.abspath(p)!=_here]\n"
 if case=='reorder_loaded_path':
  (other/'sitecustomize.py').write_text('# another normal candidate, never imported\n',encoding='utf-8')
  content=f'import sys\nsys.path.insert(0,{str(other)!r})\n'
 if case=='namespace':(start/'sitecustomize').mkdir()
 else:(start/'sitecustomize.py').write_text(content,encoding='utf-8')
 (start/'usercustomize.py').write_text('VALUE=42\n',encoding='utf-8')
 os.environ['PYTHONPATH']=str(start);os.environ['PYTHONNOUSERSITE']='1'
 if case in ('cwd_only_candidate','cwd_on_pythonpath'):
  (cwd/'sitecustomize.py').write_text('# ordinary cwd file\n',encoding='utf-8')
  os.environ['PYTHONPATH']=str(other if case=='cwd_only_candidate' else cwd)
 mr.SANDBOX=cwd
 r=dict(case=case,ROOT=str(root),sandbox=str(cwd),pythonpath=os.environ['PYTHONPATH'],full_sandbox=a.full_sandbox)
 env=mr.replay_env()
 q=subprocess.run([sys.executable,'-c',"import json,sys; print(json.dumps({'loaded': 'sitecustomize' in sys.modules, 'origin':getattr(sys.modules.get('sitecustomize'),'__file__',None),'sys_path':sys.path}))"],env=env,cwd=cwd,capture_output=True)
 r['native_control']={'rc':q.returncode,'stdout':q.stdout.decode('utf-8','replace'),'stderr':q.stderr.decode('utf-8','replace')}
 try:
  rec=mr._observed_receipt();(d/'receipt.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
  r['customization']=rec.get('startup',{}).get('customization');r['history']=rec.get('startup',{}).get('startup_history')
  mr._assert_receipt_is_complete(rec);r['complete']=True
  ctx=mr._replay_context();r['context']=ctx
  r['parent']=mr._parent_customization_view(ctx)
  try:mr._assert_customization_matches_parent(rec,ctx);r['comparison']='ACCEPTED'
  except Exception as e:r['comparison']='REJECTED';r['comparison_error']=type(e).__name__+': '+str(e)
  try:mr._execution_receipt();r['entry']='ACCEPTED'
  except Exception as e:r['entry']='REJECTED';r['entry_error']=type(e).__name__+': '+str(e)
 except Exception as e:r['diagnostic_error']=type(e).__name__+': '+str(e)
 finally:mr.SANDBOX=initial_sandbox
 (d/'observation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');records.append(r)
 print(json.dumps({k:r.get(k) for k in ('case','complete','comparison','entry','entry_error','diagnostic_error')},ensure_ascii=True),flush=True)
os.environ.clear();os.environ.update(initial_env)
(out/'observations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
