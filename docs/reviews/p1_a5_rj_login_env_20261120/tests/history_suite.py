"""Linux-only offline release QA. Temp replicas, fixed kit extraction, fake scheduler/SSH; no engine."""
import contextlib,copy,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch,Mock

ops=Path(__file__).resolve().parent
out=Path(os.environ["A5_QA_INPUT"])
files=out/"build_payload"; packet=out/"author_packet"
def module(name,p):
    spec=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
C=module("release_control",files/"RJ_ONE_SUBMIT.py")
S=module("frozen_site",files/"rj_site.py")
R=module("readback",packet/"a5_collect.py")
B=module("fixed_boot",packet/"a5_boot.py")
H=hashlib.sha256
ACTUAL=json.loads((files/"site_receipt.json").read_bytes())
def output(p, data):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
def executable(p, text):
    output(p,text.encode());p.chmod(0o700)

class Release(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.temp=Path(self.tmp.name); self.home=self.temp/"home";self.home.mkdir()
        self.bin=self.temp/"bin";self.bin.mkdir()
        self.here=self.home/C.DISPATCH;self.here.mkdir()
        for f in files.iterdir():shutil.copyfile(f,self.here/f.name)
        self.root=self.home/S.NEW
        self.spy=self.temp/"sbatch_calls"
        executable(self.bin/"sbatch",'#!/bin/sh\nprintf "%s\\n" "$@" >> "'+str(self.spy)+'"\nprintf "%s\\n" 111111\n')
        self.env=patch.dict(os.environ,{"HOME":str(self.home),"PATH":str(self.bin)+":"+os.environ["PATH"]})
        self.env.start();self.addCleanup(self.env.stop)
        h=copy.deepcopy(ACTUAL)
        ids={}
        for n in S.INPUTS:
            b=n.encode();output(self.home/S.OLD/S.BED/"in"/n,b);ids[n]=(len(b),H(b).hexdigest())
        self.history=h["historical"]
        self.old=h;self.current=copy.deepcopy(h)
        self.fake=SimpleNamespace(inspect=lambda home,host:self.current,validate_return=S.validate_return,
             OLD=S.OLD,NEW=S.NEW,BED=S.BED,SUMS=S.SUMS,INPUTS=ids,file_id=S.file_id,
             history_state=Mock(return_value=self.history))
    def deploy(self,q="99999999999",r="68719476736"):
        return C.deploy(self.here,self.old,self.fake,self.home,q,r,"ibb-master")
    def test_frozen_inputs(self):
        self.assertTrue(S.validate_return(self.old));self.assertEqual(C.sha(self.here/"site_receipt.json"),C.SITE_SHA)
        self.assertEqual(C.sha(self.here/"RJ_A5_NP6.sbatch"),C.WORKER_SHA)
        self.assertEqual(C.sha(self.here/"fixed_kit_9fd6aa9d3bee.zip"),C.KIT_SHA)
        self.assertEqual(C.sha(self.here/"rj_site.py"),C.SITE_PROGRAM_SHA)
    def test_visible_home_alias_on_lustre(self):
        alias=self.temp/"home_link";alias.symlink_to(self.home,target_is_directory=True)
        self.assertTrue(C.dispatch_location(self.here/"RJ_ONE_SUBMIT.py",alias))
        separate=self.temp/"otherhome";separate.mkdir()
        (separate/C.DISPATCH).symlink_to(self.here,target_is_directory=True)
        self.assertFalse(C.dispatch_location(self.here/"RJ_ONE_SUBMIT.py",separate))
    def test_exclusive_receipt(self):
        path=self.here/"test_receipt.json"
        C.exclusive_json(path,{"ok":1})
        with self.assertRaises(FileExistsError):C.exclusive_json(path,{"ok":2})
        self.assertEqual(json.loads(path.read_bytes()),{"ok":1})
    def test_normal_job(self):
        self.assertEqual(self.deploy()["job_id"],"111111")
        args=self.spy.read_text().splitlines()
        for flag in ("--no-requeue","--ntasks=6","--time=5-00:00:00","--partition=cpu"):self.assertIn(flag,args)
        self.assertEqual(len(list((self.root/"fixed_kit").rglob("A5_SHA256SUMS"))),1)
        self.assertEqual(sum(p.is_file() for p in (self.root/"fixed_kit").rglob("*")),143)
        self.assertEqual(json.loads((self.root/"author_intent.json").read_bytes())["previous_result"],"VALUE_MISMATCH")
        for n in self.fake.INPUTS:
            a=self.home/S.OLD/S.BED/"in"/n; b=self.root/S.BED/"in"/n
            self.assertEqual(a.read_bytes(),b.read_bytes());self.assertFalse(a.samefile(b))
        with self.assertRaises((OSError,ValueError)):self.deploy()
        self.assertEqual(args,self.spy.read_text().splitlines())
    def test_disk_before_staging(self):
        self.current["parent_available_bytes"]=self.old["input_copy_bytes"]+1
        with self.assertRaises(ValueError):self.deploy()
        self.assertFalse(self.root.exists());self.assertFalse(self.spy.exists())
    def test_quota_contract(self):
        for q,r in (("UNKNOWN","68719476736"),("68719476735","68719476736"),("123","-1"),("CONFIRMED_UNLIMITED","252405453")):
            with self.subTest(q=q,r=r):
                with self.assertRaises(ValueError):self.deploy(q,r)
        self.assertFalse(self.root.exists())
    def test_reconfirmed_no_limit(self):
        self.assertTrue(self.deploy("CONFIRMED_UNLIMITED")["acknowledged"])
    def test_receipt_drift(self):
        for key in ("runtime","input_sha256","resolved_destination_sha256","source_identities","historical"):
            with self.subTest(key=key):
                self.current=copy.deepcopy(self.old)
                k=self.current[key]
                if key=="runtime": k["mpirun"]["sha256"]="a"*64
                elif key=="input_sha256":k[next(iter(k))]="b"*64
                elif key=="source_identities":k["hist"]["sha256"]="c"*64
                elif key=="historical":k["previous_submission_marker_count"]=2
                else:self.current[key]="a"*64
                with self.assertRaises(ValueError):self.deploy()
        self.assertFalse(self.spy.exists());self.assertFalse(self.root.exists())
    def test_history_changes_during_copy(self):
        self.fake.history_state.return_value={"unexpected":"UB"}
        with self.assertRaises(ValueError):self.deploy()
        self.assertTrue(self.root.is_dir());self.assertFalse(self.spy.exists())
    def test_ambiguous_then_no_retry(self):
        executable(self.bin/"sbatch",'#!/bin/sh\necho attempt >> "'+str(self.spy)+'"\necho "oops"\n')
        with self.assertRaises(ValueError):self.deploy()
        self.assertFalse(json.loads((self.root/"submit_once/reply.json").read_bytes())["acknowledged"])
        with self.assertRaises(FileExistsError):self.deploy()
        self.assertEqual(self.spy.read_text(),"attempt\n")
    def test_stage_rejects_mismatching_source(self):
        name=next(iter(self.fake.INPUTS)); (self.home/S.OLD/S.BED/"in"/name).write_bytes(b"changed")
        with self.assertRaises(ValueError): self.deploy()
        self.assertFalse(self.spy.exists())
    def observe(self,jobstate=None,rc="0",report=False,marker=True):
        if marker:
            output(self.root/"submit_once/reply.json",json.dumps({"acknowledged":True,"job_id":"111111"}).encode())
        if jobstate:
            executable(self.bin/"sacct",'#!/bin/sh\nprintf "%s\\n" "111111|'+jobstate+'"\n')
        output(self.root/"worker_once/finished",("job=111111 runner_rc="+rc+" end=stub\n").encode())
        output(self.root/"worker_once/shell_exit",("job=111111 shell_rc="+rc+" end=stub\n").encode())
        if report:output(self.root/S.BED/"RJ.report.tgz",b"synthetic-report")
        bio=io.BytesIO()
        with patch.object(R.socket,"gethostname",return_value="ibb-master"):R.main(self.home,bio)
        with zipfile.ZipFile(bio) as z:
            v=json.loads(z.read("return.json"))
            for row in z.read("SHA256SUMS").decode().splitlines():
                h,n=row.split("  ");self.assertEqual(H(z.read(n)).hexdigest(),h)
            return v,set(z.namelist())
    def test_accounting_running(self):
        v,n=self.observe("RUNNING|0:0",report=True);self.assertEqual(v["status"],"SUBMITTED_ACCOUNTING_PENDING")
        self.assertNotIn("RJ.report.tgz",n)
    def test_terminal_success(self):
        v,n=self.observe("COMPLETED|0:0",report=True);self.assertEqual(v["status"],"COMPLETED_REPORT_RETURNED")
        self.assertFalse(v["report"]["partial_or_failure_evidence"]);self.assertEqual(v["report"]["content_readback"],"PENDING")
    def test_terminal_rc2_keeps_partial(self):
        v,n=self.observe("FAILED|2:0",rc="2",report=True);self.assertEqual(v["status"],"FINISHED_REVIEW_REQUIRED")
        self.assertIn("RJ.report.tgz",n);self.assertTrue(v["report"]["partial_or_failure_evidence"])
    def test_terminal_without_report(self):
        output(self.root/S.BED/"RJ/run_manifest.txt",b"synthetic")
        v,n=self.observe("COMPLETED|0:0");self.assertEqual(v["status"],"FINISHED_REVIEW_REQUIRED")
        self.assertIn("diagnostics/run_manifest.txt",n)
    def test_pending_accounting(self):
        v,n=self.observe("PENDING|0:0");self.assertIsNone(v.get("report"))
    def test_boot_incomplete_or_bad_quota(self):
        data=(packet/"a5_bound_payload.zip").read_bytes()
        isolated=self.temp/"fresh";isolated.mkdir()
        stat=SimpleNamespace(f_bavail=10**13,f_frsize=1)
        for q,raw in (("UNKNOWN",data),("30",data),("CONFIRMED_UNLIMITED",data[:-1]),("CONFIRMED_UNLIMITED",b"~"+data[1:])):
            with self.subTest(q=q):
                with patch.dict(os.environ,HOME=str(isolated)),patch.object(B.socket,"gethostname",return_value="ibb-master"),patch.object(B.os,"statvfs",return_value=stat),patch.object(sys,"argv",["main","GO_NEW_A5_RJ_ONCE",q,"68719476736"]),patch.object(sys,"stdin",SimpleNamespace(buffer=io.BytesIO(raw))):
                    with self.assertRaises(ValueError): B.main()
                self.assertEqual(list(isolated.iterdir()),[])
    def test_boot_duplicate(self):
        data=(packet/"a5_bound_payload.zip").read_bytes()
        with patch.object(B.socket,"gethostname",return_value="ibb-master"),patch.object(B.os,"statvfs",return_value=SimpleNamespace(f_bavail=10**13,f_frsize=1)),patch.object(sys,"argv",["main","GO_NEW_A5_RJ_ONCE","CONFIRMED_UNLIMITED","68719476736"]),patch.object(sys,"stdin",SimpleNamespace(buffer=io.BytesIO(data))):
            with self.assertRaises(FileExistsError): B.main()
        self.assertFalse(self.spy.exists())
    def test_syntax(self):
        for f in (packet/"PASTE_A5_RJ_1120.txt",packet/"quota.sh",files/"RJ_A5_NP6.sbatch"):
            subprocess.run(["bash","-n",str(f)],check=True)
    def test_worker_preserves_scope(self):
        t=(files/"RJ_A5_NP6.sbatch").read_text()
        for s in ("--no-requeue","NP=6","shell_rc=","cross_node","site.history_state","A5_AUTHOR_GO=GO_NEW_PS73_RJ",
                  "run_unload_a5_candidate.sh","sha256sum --check --status deployment.SHA256SUMS"):self.assertIn(s,t)
        self.assertNotIn("ALLOW_CONCURRENT=1",t)
        self.assertNotIn("sbatch ",t)
    def test_worker_cross_node_guard(self):
        code=(files/"RJ_A5_NP6.sbatch").read_text().split("<<'HISTORY'\n",1)[1].split("\nHISTORY\n",1)[0]
        folder=self.temp/"worker";folder.mkdir()
        before=copy.deepcopy(self.old["historical"])
        output(folder/"site_receipt.json",json.dumps(self.old).encode())
        output(folder/"rj_site.py",b'import json\nfrom pathlib import Path\nOLD="old";BED="bed"\ndef history_state(_):return json.loads(Path("now.json").read_bytes())\n')
        def run(h):
            output(folder/"now.json",json.dumps(h).encode())
            return subprocess.run([sys.executable,"-I","-B","-"],input=code.encode(),cwd=folder,capture_output=True).returncode
        changed=copy.deepcopy(before);changed["existing_outputs"]["RJ"]["dev"]+=99
        self.assertEqual(run(changed),0)
        for key in ("bytes","mtime_ns"):
            changed=copy.deepcopy(before);changed["existing_outputs"]["RJ.report.tgz"][key]+=1
            self.assertNotEqual(run(changed),0)
        changed=copy.deepcopy(before);changed["existing_outputs"]["UB"]={"kind":"directory"}
        self.assertNotEqual(run(changed),0)
        changed=copy.deepcopy(before);changed["legacy_rj_entries"][0]["manifest"]["sha256"]="a"*64
        self.assertNotEqual(run(changed),0)
    def test_boot_survives_channel_close(self):
        data=(packet/"a5_bound_payload.zip").read_bytes()
        isolated=self.temp/"isolated";isolated.mkdir()
        child=Mock();child.wait.side_effect=subprocess.TimeoutExpired("fake",480)
        with patch.dict(os.environ,HOME=str(isolated)),patch.object(B.socket,"gethostname",return_value="ibb-master"),patch.object(B.os,"statvfs",return_value=SimpleNamespace(f_bavail=10**13,f_frsize=1)),patch.object(sys,"argv",["main","GO_NEW_A5_RJ_ONCE","CONFIRMED_UNLIMITED","68719476736"]),patch.object(sys,"stdin",SimpleNamespace(buffer=io.BytesIO(data))),patch.object(B.subprocess,"Popen",return_value=child) as pop,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(B.main(),75)
            self.assertEqual(pop.call_count,1)
            self.assertTrue(pop.call_args.kwargs["start_new_session"])
            self.assertEqual(pop.call_args.kwargs["stdin"],subprocess.DEVNULL)
            self.assertTrue((isolated/C.DISPATCH/"controller.stderr").exists())
    def test_wsl_entry_no_token_and_quota(self):
        pkg=self.temp/"pkg";shutil.copytree(packet,pkg)
        log=self.temp/"connections"
        executable(self.bin/"ssh",'#!/bin/bash\ncat >/dev/null\nprintf "FAKE ONLY\\n" >> "'+str(log)+'"\nexit 255\n')
        for args in ([],["wrong"],["GO_NEW_A5_RJ_ONCE","UNKNOWN"]):
            r=subprocess.run(["bash",str(pkg/"PASTE_A5_RJ_1120.txt"),*args],capture_output=True)
            self.assertNotEqual(r.returncode,0)
        self.assertFalse(log.exists())
        r=subprocess.run(["bash",str(pkg/"PASTE_A5_RJ_1120.txt"),"GO_NEW_A5_RJ_ONCE","CONFIRMED_UNLIMITED"],capture_output=True)
        self.assertEqual(r.returncode,255);self.assertEqual(log.read_text().count("FAKE ONLY"),1)
        ret=next(pkg.glob("a5_new_rj_dispatch_*"))
        self.assertEqual((ret/"command_rc.txt").read_text(),"255\n")
        subprocess.run(["sha256sum","-c","--status","SHA256SUMS"],cwd=ret,check=True)
    def test_worker_wrong_slurm(self):
        for env in ({"SLURM_JOB_ID":"1","SLURM_NTASKS":"4"},{"SLURM_JOB_ID":"1","SLURM_NTASKS":"6","SLURM_ARRAY_JOB_ID":"33"}):
            r=subprocess.run(["bash",str(files/"RJ_A5_NP6.sbatch")],capture_output=True,env=dict(os.environ,**env))
            self.assertNotEqual(r.returncode,0);self.assertFalse(self.root.exists())

if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Release)
    ids=[t.id().rsplit(".",1)[1] for t in suite]
    rr=unittest.TextTestRunner(verbosity=1).run(suite)
    if rr.wasSuccessful():
        (out/"history_24.json").write_text(json.dumps({"passed_offline_methods":len(ids),"methods":ids,"real_ssh":0,
            "real_submissions":0,"engine_runs":0,"environment":"local WSL Python "+sys.version.split()[0]},indent=2)+"\n",encoding="utf-8")
    sys.exit(0 if rr.wasSuccessful() else 1)
