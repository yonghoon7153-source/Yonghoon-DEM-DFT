"""Same expected-correct tests against V1 and V2; no remote call, scheduler, or engine."""
from contextlib import ExitStack, redirect_stdout
from importlib.util import module_from_spec, spec_from_file_location
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace

WORK=Path(__file__).resolve().parent
spec=spec_from_file_location("previous_suite", WORK/"history_suite.py")
old=module_from_spec(spec); spec.loader.exec_module(old)
B,C,S=old.B,old.C,old.S

class LoginRegression(unittest.TestCase):
    def setUp(self):
        fixture=old.Release("test_normal_job")
        fixture.setUp(); self.addCleanup(fixture.doCleanups)
        self.f=fixture
        self.home=fixture.temp/"login"; self.home.mkdir()
        self.marker=fixture.temp/"profile_executed"
        self.profile=fixture.temp/"login.initializer"
        self.profile.write_text("touch "+str(self.marker)+"\n")
        self.payload=(old.packet/"a5_bound_payload.zip").read_bytes()
        self.entered=ExitStack(); self.addCleanup(self.entered.close)
        envbase={"HOME":str(self.home),"PATH":str(self.f.bin)+":/usr/bin:/bin","USER":"synthetic","LANG":"C"}
        self.entered.enter_context(patch.dict(os.environ,envbase,clear=True))
        self.entered.enter_context(patch.object(sys,"argv",["fixed","GO_NEW_A5_RJ_ONCE","CONFIRMED_UNLIMITED","68719476736"]))
        self.entered.enter_context(patch.object(B.socket,"gethostname",return_value="ibb-master"))
        self.entered.enter_context(patch.object(B.os,"statvfs",return_value=SimpleNamespace(f_bavail=10**13,f_frsize=1)))

    def boot(self, extra, host="ibb-master"):
        self.child_environments=[]
        def fake_start(args,**kwargs):
            self.child_environments.append(dict(kwargs.get("env",os.environ)))
            self.assertTrue(kwargs["start_new_session"])
            self.assertEqual(args[0],sys.executable)
            (kwargs["cwd"]/"controller_end.json").write_text(json.dumps({"controller_rc":0,"reply":{"job_id":"11111"}}))
            return Mock(wait=Mock(return_value=0))
        with patch.dict(os.environ,extra),patch.object(B.socket,"gethostname",return_value=host), \
             patch.object(sys,"stdin",SimpleNamespace(buffer=io.BytesIO(self.payload))), \
             patch.object(B.subprocess,"Popen",side_effect=fake_start), redirect_stdout(io.StringIO()):
            return B.main()

    def controller(self, extra):
        ctxfile=self.f.temp/"scheduler_environment.json"
        # Inspect the original exec environment. A Python interpreter can add LC_CTYPE at startup.
        old.executable(self.f.bin/"sbatch", "#!/usr/bin/python3\nimport json,os\nfrom pathlib import Path\np=Path("+repr(str(ctxfile))+")\nraw=Path('/proc/self/environ').read_bytes()\nenv=dict(os.fsdecode(x).split('=',1) for x in raw.split(b'\\0') if x)\nwith p.open('x') as f: json.dump(env, f)\nprint(444444)\n")
        real_deploy=C.deploy
        self.in_controller=[]
        def bridge(folder,prior,_frozen_site,home,quota,budget,host):
            self.in_controller.append(dict(os.environ))
            self.assertEqual(host,"ibb-master")
            return real_deploy(folder,prior,self.f.fake,home,quota,budget,host)
        with patch.dict(os.environ,dict(extra,HOME=str(self.f.home))), \
             patch.object(C,"__file__",str(self.f.here/"RJ_ONE_SUBMIT.py")), patch.object(C,"deploy",side_effect=bridge):
            reply=C.main()
        self.assertEqual(reply["job_id"],"444444")
        return json.loads(ctxfile.read_text())

    def test_boot_accepts_ibb_profile_and_removes_it_before_child(self):
        try: result=self.boot({"BASH_ENV":str(self.profile)})
        except ValueError as exc: self.fail("valid ibb login refused by bootstrap: "+str(exc))
        self.assertEqual(result,0)
        self.assertEqual(len(self.child_environments),1)
        child=self.child_environments[0]
        self.assertNotIn("BASH_ENV",child)
        self.assertNotIn("SLURM_CONF",child)
        self.assertFalse(self.marker.exists())

    def test_controller_accepts_ibb_profile_and_filters_batch_process(self):
        try: environment=self.controller({"BASH_ENV":str(self.profile),"A5_UNRELATED_TEST":"unlisted"})
        except ValueError as exc: self.fail("valid ibb login refused by controller: "+str(exc))
        self.assertEqual(len(self.in_controller),1)
        self.assertNotIn("BASH_ENV",self.in_controller[0])
        for key in ("BASH_ENV","ENV","SLURM_CONF","A5_UNRELATED_TEST"):
            self.assertNotIn(key,environment)
        allowed={"HOME","PATH","LANG","LC_ALL","USER","LOGNAME","SHELL","LD_LIBRARY_PATH","TMPDIR"}
        self.assertFalse(set(environment)-allowed)
        self.assertFalse(self.marker.exists())

    def test_clean_login_boot(self):
        self.assertEqual(self.boot({}),0)
        self.assertEqual(len(self.child_environments),1)

    def test_clean_login_controller(self):
        env=self.controller({})
        self.assertNotIn("BASH_ENV",env)
        self.assertNotIn("SLURM_CONF",env)

    def test_ibb_boot_still_rejects_prohibited_context(self):
        for name,value in (("ENV","on"),("SLURM_CONF","present"),("SLURM_JOB_ID","1"),("SBATCH_QOS","x")):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError,"wrong login context"):
                    self.boot({"BASH_ENV":str(self.profile),name:value})
                self.assertEqual([],self.child_environments)
                self.assertEqual([],list(self.home.iterdir()))

    def test_ibb_controller_still_rejects_prohibited_context(self):
        for name,value in (("ENV","on"),("SLURM_CONF","present"),("SLURM_JOB_ID","1"),("SBATCH_QOS","x")):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError,"scheduler injection/active allocation"):
                    self.controller({"BASH_ENV":str(self.profile),name:value})
                self.assertEqual([],self.in_controller)
                self.assertFalse(self.f.root.exists())
                self.assertFalse((self.f.temp/"scheduler_environment.json").exists())

    def test_wrong_host_stops_before_boot(self):
        with self.assertRaisesRegex(ValueError,"wrong login context"):
            self.boot({"BASH_ENV":str(self.profile)},"not-ibb")
        self.assertEqual([],self.child_environments)
        self.assertEqual([],list(self.home.iterdir()))

if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(LoginRegression)
    names=[x.id().split(".")[-1] for x in suite]
    rr=unittest.TextTestRunner(verbosity=2).run(suite)
    errors=[case.id().split(".")[-1] for case,details in rr.errors]
    failures=[case.id().split(".")[-1] for case,details in rr.failures]
    result={"methods":len(names),"case_names":names,"failed_assertions":failures,"unexpected_errors":errors,"rc":0 if rr.wasSuccessful() else 1}
    (old.out/"login_check.json").write_text(json.dumps(result,indent=2)+"\n")
    sys.exit(result["rc"])
