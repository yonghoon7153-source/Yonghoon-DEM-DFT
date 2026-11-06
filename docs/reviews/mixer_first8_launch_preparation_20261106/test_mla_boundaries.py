"""Local synthetic tests only. No scheduler, MPI or other subprocess may run."""
import concurrent.futures, contextlib, hashlib, io, json, os, pathlib, runpy
import subprocess, sys, tempfile, threading, time, types, unittest
from unittest.mock import patch

HERE=pathlib.Path(__file__).resolve().parent
VALID_ENV={'SLURM_NTASKS':'20','SLURM_JOB_ID':'12345','SLURM_JOB_PARTITION':'cpu',
           'SLURM_JOB_QOS':'cpu-60','SLURM_CPUS_PER_TASK':'1','SLURM_JOB_NUM_NODES':'1'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def audit(event,args):
    if event in {'subprocess.Popen','os.system','os.exec','os.posix_spawn','socket.connect'}:
        raise AssertionError('No external process/network in MLA mocks: '+event)

class Fixture:
    def __init__(self,root,concurrency=1):
        self.root=pathlib.Path(root);self.calls=[];self.call_lock=threading.Lock();self.mode='ok'
        for n in ('submit_one.py.txt','job_start.py.txt','source_seal.json','static_asset_manifest.json'):
            (self.root/n).write_bytes((HERE/n).read_bytes())
        self.ns=runpy.run_path(str(self.root/'submit_one.py.txt'))
        self.ns['main'].__globals__['subprocess']=types.SimpleNamespace(run=self.scheduler,TimeoutExpired=subprocess.TimeoutExpired)
        self.source=self.root/'source';self.source.mkdir()
        self.source_files=[]
        seal=json.loads((HERE/'source_seal.json').read_text())
        for a in seal['files']:
            p=self.source/a['path'];p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes((HERE.parents[2]/a['path']).read_bytes());self.source_files.append({'path':str(p),'sha256':a['sha256']})
        self.source_pin=seal['source_pin'];self.concurrency=concurrency
        self.author=self.put('author_go','SYNTHETIC AUTHOR DOCUMENT - NOT REAL GO')
        self.campaign=self.put('campaign_policy.json',json.dumps({'schema':'mixer_first8_campaign/1',
            'campaign_id':'mixer_precal_first8_20261106','install_root':str(self.root),'execution_authorized':True,'np':20,
            'max_concurrency':concurrency,'cpu_cap':60,'author_go_sha256':self.author['sha256']}))
        self.python=self.put('python','SYNTHETIC INTERPRETER - NEVER EXECUTED')
    def put(self,name,data):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(data if isinstance(data,bytes) else data.encode())
        return {'path':str(p),'sha256':sha(p)}
    def make(self,name='PRECAL_E0'):
        root=self.root/'cases'/name;root.mkdir(parents=True)
        c={'schema':'mixer_first8_execution_approval/1','execution_authorized':True,
           'gate':'QUALIFICATION_PILOT_GO' if name=='PRECAL_E0' else 'MAP_CASE_GO','case':name,
           'np':20,'case_dir':str(root),'author_choices_confirmed':True,'approved_concurrency':self.concurrency,
           'wave_release':[name],'runner_reviewed':True,'walltime_approved':True,'author_go':self.author,
           'campaign_policy':self.campaign,'source_root':str(self.source),'source_pin':self.source_pin,
           'minimum_free_bytes':1,'minimum_free_inodes':1}
        def put(k,data):return self.put('approvals/'+name+'/'+k,data)
        for k in ('qualification','mxd2r_disposition','binary','mpi_launcher'):c[k]=put(k,'SYNTHETIC NOT EXECUTABLE')
        live={'observed_unix':time.time(),'qos':'cpu-60','partition':'cpu','reserved_cpus':0,'running_first8':0}
        for k in ('qos_verified','disk_budget_verified','inode_budget_verified','d07_finished','qualification_accepted','paths_verified'):live[k]=True
        c['live_preflight']=put('live',json.dumps(live))
        c['policy']=put('policy',json.dumps({'execution_authorized':True,'policy_id':'SYNTHETIC-COMMON-POLICY','allowed_to_submit':[name]}))
        files=list(self.source_files)
        for n in ('in.mixer','deck_meta.json','Drum.stl','Front.stl','Back.stl'):
            p=root/n;p.write_bytes((HERE/'planned_assets'/name/n).read_bytes());files.append({'path':str(p),'sha256':sha(p)})
        c['runner_bindings']={'python':self.python['path'],'job_start':str(self.root/'job_start.py.txt'),
             'stdout':str(root/'slurm.stdout'),'stderr':str(root/'slurm.stderr'),'walltime':'1-00:00:00'}
        files.extend([self.python,{'path':str(self.root/'job_start.py.txt'),'sha256':sha(self.root/'job_start.py.txt')}])
        ap=self.root/'approvals'/name/'approval.json'
        c['runner']=put('runner',self.ns['canonical_runner'](c,str(ap)))
        c['source_manifest']=put('manifest',json.dumps({'files':files}));ap.write_text(json.dumps(c))
        return c,ap,files,put
    def scheduler(self,argv,**kwargs):
        with self.call_lock:self.calls.append((argv,kwargs));n=len(self.calls)
        if self.mode=='timeout':raise subprocess.TimeoutExpired(argv,60)
        if self.mode=='interrupt':raise KeyboardInterrupt('synthetic interrupted submission')
        return types.SimpleNamespace(returncode=1 if self.mode=='failed' else 0,
          stdout='12345 extra\n' if self.mode=='ambiguous' else str(12345+n)+'\n',stderr='')
    def submit(self,ap):return self.ns['main'](str(ap))
    def start(self,c,ap,env=None,side_effect=None,rc=0):
        root=pathlib.Path(c['case_dir'])
        (root/'submission.claim.json').write_text(json.dumps({'approval_sha256':sha(ap)}))
        ns=runpy.run_path(c['runner_bindings']['job_start']);calls=[]
        def fake(argv,**kw):
            calls.append((argv,kw))
            if side_effect:side_effect(root)
            return types.SimpleNamespace(returncode=rc)
        ns['main'].__globals__['subprocess']=types.SimpleNamespace(run=fake)
        with patch.dict(os.environ,VALID_ENV if env is None else env,clear=True),patch.object(sys,'argv',['job_start',str(ap)]):
            try:return ns['main'](),None,calls
            except Exception as e:return None,e,calls

class MLATests(unittest.TestCase):
    def test_submission_environment_injection(self):
        keys=('SBATCH_ARRAY_INX','SBATCH_QOS','SBATCH_PARTITION','SBATCH_TIMELIMIT','SBATCH_OUTPUT','SBATCH_ERROR',
              'SLURM_CLUSTERS','SLURM_HINT','SLURM_EXPORT_ENV','SALLOC_QOS','SRUN_CPUS_PER_TASK')
        for key in keys:
            with self.subTest(key=key),tempfile.TemporaryDirectory() as td:
                f=Fixture(td);c,ap,_,_=f.make()
                with patch.dict(os.environ,{key:'unapproved'}):
                    with self.assertRaises(ValueError):f.submit(ap)
                self.assertEqual(len(f.calls),0)
    def test_normal_submission_argv_and_environment(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td);c,ap,_,_=f.make()
            with patch.dict(os.environ,{'UNAPPROVED_PLUGIN':'x','BASH_ENV':'/unapproved'}):f.submit(ap)
            argv,kw=f.calls[0]
            for arg in ('--partition=cpu','--qos=cpu-60','--nodes=1','--ntasks=20','--cpus-per-task=1',
                        '--time=1-00:00:00','--output='+c['runner_bindings']['stdout'],'--error='+c['runner_bindings']['stderr']):self.assertIn(arg,argv)
            self.assertIn('env',kw);self.assertNotIn('UNAPPROVED_PLUGIN',kw['env']);self.assertNotIn('BASH_ENV',kw['env'])
    def test_job_allocation_mismatch_before_mpi(self):
        for key,value in [('SLURM_JOB_QOS','other'),('SLURM_JOB_PARTITION','other'),('SLURM_CPUS_PER_TASK','4'),
                          ('SLURM_JOB_NUM_NODES','2'),('SLURM_ARRAY_JOB_ID','123'),('SLURM_HET_GROUP','0')]:
            with self.subTest(key=key),tempfile.TemporaryDirectory() as td:
                f=Fixture(td);c,ap,_,_=f.make();env=dict(VALID_ENV);env[key]=value
                rc,error,calls=f.start(c,ap,env);self.assertIsNotNone(error);self.assertEqual(calls,[])
    def test_shared_concurrency_one(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td);a=f.make('PRECAL_R1_B1_U')[1];b=f.make('PRECAL_R1_B1_C')[1];barrier=threading.Barrier(2)
            def go(ap):
                barrier.wait(timeout=5)
                try:f.submit(ap);return True
                except (ValueError,OSError):return False
            with concurrent.futures.ThreadPoolExecutor(2) as pool:out=list(pool.map(go,[a,b]))
            self.assertEqual(sum(out),1);self.assertEqual(len(f.calls),1)
    def test_two_slots_then_third_refused(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td,2);aps=[f.make(k)[1] for k in ('PRECAL_R1_B1_U','PRECAL_R1_B1_C','PRECAL_R1_B2_U')]
            f.submit(aps[0]);f.submit(aps[1])
            with self.assertRaises((ValueError,OSError)):f.submit(aps[2])
            self.assertEqual(len(f.calls),2)
    def test_uncertain_submission_holds_other_cases(self):
        for mode in ('ambiguous','failed','timeout','interrupt'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as td:
                f=Fixture(td,2);a=f.make('PRECAL_R1_B1_U')[1];b=f.make('PRECAL_R1_B1_C')[1];f.mode=mode
                with self.assertRaises((ValueError,KeyboardInterrupt)):f.submit(a)
                f.mode='ok'
                with self.assertRaises((ValueError,OSError)):f.submit(b)
                self.assertEqual(len(f.calls),1)
    def test_same_case_race_still_single_attempt(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td,2);ap=f.make()[1];barrier=threading.Barrier(2)
            def go(_):
                barrier.wait(timeout=5)
                try:f.submit(ap);return True
                except (ValueError,OSError):return False
            with concurrent.futures.ThreadPoolExecutor(2) as pool:out=list(pool.map(go,range(2)))
            self.assertEqual(sum(out),1);self.assertEqual(len(f.calls),1)
    def test_campaign_limit_cannot_be_changed_per_case(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td);c,ap,_,_=f.make();c['approved_concurrency']=2;ap.write_text(json.dumps(c))
            with self.assertRaises(ValueError):f.submit(ap)
            self.assertEqual(len(f.calls),0)
    def test_campaign_policy_installation_binding(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td);c,ap,_,_=f.make();p=pathlib.Path(c['campaign_policy']['path'])
            policy=json.loads(p.read_text());policy['install_root']='/another/installation';p.write_text(json.dumps(policy))
            c['campaign_policy']['sha256']=sha(p);ap.write_text(json.dumps(c))
            with self.assertRaises(ValueError):f.submit(ap)
            self.assertEqual(len(f.calls),0)
    def test_existing_receipts_refuse_submission(self):
        for name in ('job_end.json','job_start.json','simulator.stdout','simulator.stderr','submission.receipt.json'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as td:
                f=Fixture(td);c,ap,_,_=f.make();p=pathlib.Path(c['case_dir'])/name;p.write_bytes(b'OLD OUTPUT')
                with self.assertRaises((ValueError,OSError)):f.submit(ap)
                self.assertEqual(len(f.calls),0);self.assertEqual(p.read_bytes(),b'OLD OUTPUT')
    def test_existing_end_receipt_refuses_mpi(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td);c,ap,_,_=f.make();p=pathlib.Path(c['case_dir'])/'job_end.json';p.write_bytes(b'OLD OUTPUT')
            rc,error,calls=f.start(c,ap);self.assertIsNotNone(error);self.assertEqual(calls,[]);self.assertEqual(p.read_bytes(),b'OLD OUTPUT')
    def test_late_end_receipt_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td);c,ap,_,_=f.make()
            rc,error,calls=f.start(c,ap,side_effect=lambda root:(root/'job_end.json').write_bytes(b'LATE OUTPUT'))
            self.assertIsNotNone(error);self.assertEqual(len(calls),1);self.assertEqual((pathlib.Path(c['case_dir'])/'job_end.json').read_bytes(),b'LATE OUTPUT')
    def test_new_normal_and_failed_job_receipts(self):
        for code in (0,9):
            with self.subTest(code=code),tempfile.TemporaryDirectory() as td:
                f=Fixture(td);c,ap,_,_=f.make();rc,error,calls=f.start(c,ap,rc=code)
                self.assertIsNone(error);self.assertEqual(rc,code);self.assertEqual(len(calls),1)
                end=json.loads((pathlib.Path(c['case_dir'])/'job_end.json').read_text());self.assertEqual(end['returncode'],code)
                self.assertEqual(end['state'],'EXITED_REQUIRES_QUALIFICATION' if code==0 else 'TECH_HOLD')
    def test_spawn_error_keeps_tech_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            f=Fixture(td);c,ap,_,_=f.make()
            def fail(root):raise OSError('synthetic MPI unavailable')
            rc,error,calls=f.start(c,ap,side_effect=fail);self.assertIsNotNone(error);self.assertEqual(len(calls),1)
            end=json.loads((pathlib.Path(c['case_dir'])/'job_end.json').read_text());self.assertEqual(end['state'],'TECH_HOLD');self.assertIsNone(end['returncode'])

if __name__=='__main__':
    sys.addaudithook(audit)
    unittest.main()
