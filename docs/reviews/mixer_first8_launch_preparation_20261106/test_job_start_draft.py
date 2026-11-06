import hashlib,json,os,pathlib,runpy,sys,types,unittest
from unittest.mock import patch
import importlib.util
HERE=pathlib.Path(__file__).resolve().parent
fixture_spec=importlib.util.spec_from_file_location('first8_local_test_fixture',str(HERE/'test_submit_draft.py'))
fixture_module=importlib.util.module_from_spec(fixture_spec)
fixture_spec.loader.exec_module(fixture_module)

VALID_ENV={'SLURM_NTASKS':'20','SLURM_JOB_ID':'12345','SLURM_JOB_PARTITION':'cpu','SLURM_JOB_QOS':'cpu-60','SLURM_CPUS_PER_TASK':'1','SLURM_JOB_NUM_NODES':'1'}

class JobStart(unittest.TestCase):
 def fixture(self,mode):
  def hook(c,ap,files,seal):
   c.update(minimum_free_bytes=1,minimum_free_inodes=1)
   ap.write_text(json.dumps(c));root=pathlib.Path(c['case_dir']);raw=ap.read_bytes()
   (root/'submission.claim.json').write_text(json.dumps({'approval_sha256':hashlib.sha256(raw).hexdigest()}))
   if mode=='approval':ap.write_text(json.dumps(dict(c,np=10)))
   if mode=='asset':(root/'in.mixer').write_text('changed')
   if mode=='nonfresh':(root/'post').mkdir()
   if mode=='floor':
    c.pop('minimum_free_bytes');ap.write_text(json.dumps(c));(root/'submission.claim.json').write_text(json.dumps({'approval_sha256':hashlib.sha256(ap.read_bytes()).hexdigest()}))
   namespace=runpy.run_path(c['runner_bindings']['job_start'])
   with patch.dict(os.environ,dict(VALID_ENV,SLURM_NTASKS='19' if mode=='rank' else '20')),patch.object(sys,'argv',['job_start',str(ap)]),patch('subprocess.run',return_value=types.SimpleNamespace(returncode=0)) as call:
    if mode=='ok':
     self.assertEqual(namespace['main'](),0);self.assertEqual(call.call_count,1)
     self.assertEqual(call.call_args.args[0],[c['mpi_launcher']['path'],'--oversubscribe','--bind-to','none','-np','20',c['binary']['path'],'-in','in.mixer'])
     self.assertEqual(call.call_args.kwargs['env']['OMP_NUM_THREADS'],'1')
    else:
     with self.assertRaises(ValueError):namespace['main']()
     call.assert_not_called()
  fixture_module.Submission().exercise('ok',hook=hook)
 def test_positive_mock_only(self):self.fixture('ok')
 def test_approval_drift(self):self.fixture('approval')
 def test_rank(self):self.fixture('rank')
 def test_asset_drift(self):self.fixture('asset')
 def test_nonfresh(self):self.fixture('nonfresh')
 def test_missing_floor(self):self.fixture('floor')
 def test_job_start_approval_single_snapshot(self):
  def hook(c,ap,files,seal):
   c.update(minimum_free_bytes=1,minimum_free_inodes=1);ap.write_text(json.dumps(c))
   initial=ap.read_bytes();root=pathlib.Path(c['case_dir'])
   (root/'submission.claim.json').write_text(json.dumps({'approval_sha256':hashlib.sha256(initial).hexdigest()}))
   ns=runpy.run_path(c['runner_bindings']['job_start']);oldbytes=pathlib.Path.read_bytes;reads=[]
   def rb(p):
    raw=oldbytes(p)
    if p==ap:
     reads.append(1);ap.write_text(json.dumps(dict(c,np=999)))
    return raw
   with patch.object(pathlib.Path,'read_bytes',rb),patch.dict(os.environ,VALID_ENV,clear=True),patch.object(sys,'argv',['job_start',str(ap)]),patch('subprocess.run',return_value=types.SimpleNamespace(returncode=0)) as call:
    self.assertEqual(ns['main'](),0);self.assertEqual(call.call_count,1);self.assertEqual(len(reads),1)
  fixture_module.Submission().exercise('ok',hook=hook)
 def test_submit_approval_replacement_snapshot(self):
  def hook(c,ap,files,seal):
   initial=ap.read_bytes();oldbytes=pathlib.Path.read_bytes;oldtext=pathlib.Path.read_text;replaced=[]
   def change(p,raw):
    if p==ap and not replaced:
     replaced.append(True);ap.write_text(json.dumps(dict(c,np=999)))
    return raw
   def rb(p):return change(p,oldbytes(p))
   def rt(p,*a,**kw):return change(p,oldtext(p,*a,**kw))
   ns=runpy.run_path(str(pathlib.Path(c['runner_bindings']['job_start']).parent/'submit_one.py.txt'))
   with patch.object(pathlib.Path,'read_bytes',rb),patch.object(pathlib.Path,'read_text',rt),patch('subprocess.run',return_value=types.SimpleNamespace(returncode=0,stdout='12345\n',stderr='')):
    ns['main'](str(ap))
   claim=json.loads((pathlib.Path(c['case_dir'])/'submission.claim.json').read_text())
   self.assertEqual(claim['approval_sha256'],hashlib.sha256(initial).hexdigest())
   # Job-start reads changed bytes and must reject the original claim before MPI.
   start=runpy.run_path(c['runner_bindings']['job_start'])
   with patch.dict(os.environ,VALID_ENV,clear=True),patch.object(sys,'argv',['job_start',str(ap)]),patch('subprocess.run') as call:
    with self.assertRaises(ValueError):start['main']()
    call.assert_not_called()
  fixture_module.Submission().exercise('ok',hook=hook)
if __name__=='__main__':unittest.main()
