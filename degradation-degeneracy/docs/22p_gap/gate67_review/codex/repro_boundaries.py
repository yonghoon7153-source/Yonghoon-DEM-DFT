"""New G67 boundary cases. Real Python subprocesses, sandbox-only fixtures.
No production edits. Only the declared forged-receipt cases alter a receipt copy.
"""
import argparse, copy, hashlib, importlib.util, json, os, pathlib, subprocess, sys, zipfile
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True)
a=p.parse_args();root=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(root/'docs/22p_gap'));sys.path.insert(0,str(root/'tests'))
import mutation_replay as mr
orig_exe=sys.executable; orig_env=dict(os.environ); orig_sandbox=mr.SANDBOX
env=dict(os.environ);env.pop('PYTHONNOUSERSITE',None)
interpreters={}
for mode in ('off','on'):
 v=out/('venv-'+mode)
 cmd=[orig_exe,'-m','venv','--without-pip']+(['--system-site-packages'] if mode=='on' else [])+[str(v)]
 r=subprocess.run(cmd,env=env,capture_output=True,timeout=180);assert r.returncode==0,r.stderr
 interpreters[mode]=str(v/('Scripts/python.exe' if os.name=='nt' else 'bin/python'))
summary=[]
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def attempt(fn):
 try: fn();return {'result':'ACCEPTED'}
 except Exception as e:return {'result':'REJECTED','error_type':type(e).__name__,'error':str(e)}
def collect(label,mode,start):
 d=out/label;d.mkdir();sys.executable=interpreters[mode]
 os.environ['PYTHONPATH']=str(start);os.environ.pop('PYTHONNOUSERSITE',None)
 cwd=mr._make_sandbox();mr.SANDBOX=cwd
 rec={'case':label,'mode':mode,'sandbox':str(cwd),'pythonpath':str(start),'executable':sys.executable}
 q=subprocess.run([sys.executable,'-c',"import sys,site,json;print(json.dumps({'user_site':site.ENABLE_USER_SITE,'customization':{n:{'loaded':n in sys.modules,'origin':getattr(sys.modules.get(n),'__file__',None),'locations':list(getattr(getattr(sys.modules.get(n),'__spec__',None),'submodule_search_locations',[]) or [])} for n in ('sitecustomize','usercustomize')},'sys_path':sys.path}))"],cwd=cwd,env=mr.replay_env(),capture_output=True)
 rec['native_control']={'rc':q.returncode,'stdout':q.stdout.decode('utf-8','replace'),'stderr':q.stderr.decode('utf-8','replace')}
 body=mr._observed_receipt();dump(d/'receipt.json',body)
 rec['complete']=attempt(lambda:mr._assert_receipt_is_complete(body))
 ctx=mr._replay_context();dump(d/'context.json',ctx)
 rec['comparison']=attempt(lambda:mr._assert_customization_matches_parent(body,ctx))
 rec['entry']=attempt(mr._execution_receipt)
 rec['customization']=body.get('startup',{}).get('customization')
 if label.startswith('namespace'):
  forged=copy.deepcopy(body);forged['startup']['customization']['usercustomize']='<absent>'
  dump(d/'forged.json',forged)
  rec['forged_complete']=attempt(lambda:mr._assert_receipt_is_complete(forged))
  rec['forged_comparison']=attempt(lambda:mr._assert_customization_matches_parent(forged,ctx))
  orig=mr._observed_receipt
  try:
   mr._observed_receipt=lambda:copy.deepcopy(forged)
   rec['forged_actual_entry']=attempt(mr._execution_receipt)
  finally:mr._observed_receipt=orig
 dump(d/'observation.json',rec);summary.append(rec)
 print(json.dumps({k:v for k,v in rec.items() if k not in ('native_control','customization')},ensure_ascii=True),flush=True)
 mr.SANDBOX=orig_sandbox

startup=out/'explicit-namespace';(startup/'usercustomize').mkdir(parents=True)
(startup/'sitecustomize.py').write_text('import usercustomize\n',encoding='utf-8')
collect('namespace_explicit_off','off',startup)
collect('namespace_explicit_on','on',startup)
for kind,clean in [('package',False),('package',True),('module',True)]:
 label='zip_'+kind+('_remove_path' if clean else '_plain')
 archive=out/(label+'.zip')
 body='# standard ZIP startup\n'
 if clean:
  arc='os.path.dirname(os.path.dirname(__file__))' if kind=='package' else 'os.path.dirname(__file__)'
  body='import os, sys\n_arc='+arc+'\nsys.path[:]=[p for p in sys.path if os.path.normcase(os.path.normpath(p)) != os.path.normcase(os.path.normpath(_arc))]\n'
 with zipfile.ZipFile(archive,'x') as z:z.writestr('sitecustomize/__init__.py' if kind=='package' else 'sitecustomize.py',body)
 collect(label,'off',archive)
sys.executable=orig_exe;os.environ.clear();os.environ.update(orig_env);mr.SANDBOX=orig_sandbox
spec=importlib.util.spec_from_file_location('g67_subject_tests',root/'tests/test_gate66_defensive.py')
tm=importlib.util.module_from_spec(spec);spec.loader.exec_module(tm)
for label,extra in [('premise_pytest_usage_error',{'PYTEST_ADDOPTS':'--g67-option-does-not-exist'}),('premise_collection_only',{'PYTEST_ADDOPTS':'--collect-only'})]:
 q=tm._premise_run(orig_exe,extra)
 result=attempt(lambda:tm.test_g66_08_the_premise_test_does_not_fail_on_an_inherited_env(extra))
 rec={'case':label,'env_extra':extra,'subprocess_rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'committed_test_result':result}
 dump(out/(label+'.json'),rec);summary.append(rec);print(json.dumps(rec,ensure_ascii=True),flush=True)
dump(out/'summary.json',summary)
