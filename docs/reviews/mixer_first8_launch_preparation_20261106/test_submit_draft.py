import hashlib, json, os, pathlib, subprocess, tempfile, time, unittest, runpy
CANON=runpy.run_path(str(pathlib.Path(__file__).resolve().parent/"submit_one.py.txt"))["canonical_runner"]
HERE=pathlib.Path(__file__).resolve().parent
class Submission(unittest.TestCase):
 def exercise(self,mode,mutate=None,hook=None):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td); case=p/'case';case.mkdir();bin=p/'bin';bin.mkdir();calls=p/'calls'
   sb=bin/'sbatch';sb.write_text('#!/bin/sh\nprintf x >> "$CALLS"\n'+{'ok':'echo 12345\n','fail':'echo failure >&2\nexit 1\n','ambiguous':'echo "12345 extra"\n'}[mode]);sb.chmod(0o755)
   def seal(name,data):
    q=p/name;q.write_text(data);return {'path':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
   c={'schema':'mixer_first8_execution_approval/1','execution_authorized':True,'gate':'QUALIFICATION_PILOT_GO','case':'PRECAL_E0','np':20,'author_choices_confirmed':True,'approved_concurrency':1,'wave_release':['PRECAL_E0'],'case_dir':str(case),'complete_source_seal_reviewed':True,'runner_reviewed':True,'walltime_approved':True}
   for k in ('author_go','qualification','mxd2r_disposition','runner','binary','mpi_launcher'):c[k]=seal(k,'synthetic test artifact')
   c['policy']=seal('policy',json.dumps({'execution_authorized':True,'policy_id':'SYNTHETIC','allowed_to_submit':['PRECAL_E0']}))
   live={'observed_unix':time.time(),'qos':'cpu-60','partition':'cpu','reserved_cpus':0,'running_first8':0}
   for k in ('qos_verified','disk_budget_verified','inode_budget_verified','d07_finished','qualification_accepted','paths_verified'):live[k]=True
   c['live_preflight']=seal('live',json.dumps(live));files=[]
   for n in ('in.mixer','deck_meta.json','Drum.stl','Front.stl','Back.stl'):
    q=case/n;q.write_bytes((HERE/'planned_assets'/'PRECAL_E0'/n).read_bytes());files.append({'path':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
   source_root=p/'source';source_root.mkdir();seal_doc=json.loads((HERE/'source_seal.json').read_text());c['source_pin']=seal_doc['source_pin'];c['source_root']=str(source_root)
   repo=HERE.parents[2]
   for a in seal_doc['files']:
    q=source_root/a['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((repo/a['path']).read_bytes());files.append({'path':str(q),'sha256':a['sha256']})
   c['runner_bindings']={'python':str(p/'python'),'job_start':str(p/'job_start'),'stdout':str(p/'out'),'stderr':str(p/'err'),'walltime':'1-00:00:00'}
   files.append(seal('python','mock source'))
   files.append(seal('job_start',(HERE/'job_start.py.txt').read_text()))
   c['runner']=seal('runner',CANON(c,str(p/'approval.json')))
   c['source_manifest']=seal('manifest',json.dumps({'files':files}))
   if mutate:mutate(c,live,seal)
   approval=p/'approval.json';approval.write_text(json.dumps(c));env=dict(os.environ,PATH=str(bin)+':'+os.environ['PATH'],CALLS=str(calls))
   if hook:return hook(c,approval,files,seal)
   cmd=['python3',str(HERE/'submit_one.py.txt'),str(approval)]
   first=subprocess.run(cmd,env=env,capture_output=True,text=True);second=subprocess.run(cmd,env=env,capture_output=True,text=True)
   return first.returncode,second.returncode,calls.read_text() if calls.exists() else ''
 def test_exact_once(self):self.assertEqual(self.exercise('ok'),(0,2,'x'))
 def test_failure_no_retry(self):self.assertEqual(self.exercise('fail'),(2,2,'x'))
 def test_ambiguous_no_retry(self):self.assertEqual(self.exercise('ambiguous'),(2,2,'x'))
 def test_missing_go(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c.update(execution_authorized=False)),(2,2,''))
 def test_cpu_cap(self):
  def bad(c,l,s):l['reserved_cpus']=41;c['live_preflight']=s('live',json.dumps(l))
  self.assertEqual(self.exercise('ok',bad),(2,2,''))
 def test_identity(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c['binary'].update(sha256='0'*64)),(2,2,''))
 def test_source_pin(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c.update(source_pin='bad')),(2,2,''))
 def test_runner_bytes(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c.update(runner=s('runner','arbitrary command'))),(2,2,''))
 def test_changed_job_start(self):
  def change(c,l,seal):
   new=seal('job_start','arbitrary Python code')
   m=json.loads(pathlib.Path(c['source_manifest']['path']).read_text())
   for a in m['files']:
    if a['path']==new['path']:a.update(new)
   c['source_manifest']=seal('manifest',json.dumps(m))
  self.assertEqual(self.exercise('ok',change),(2,2,''))
 def test_choices(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c.update(author_choices_confirmed=False)),(2,2,''))
if __name__=='__main__':unittest.main()
