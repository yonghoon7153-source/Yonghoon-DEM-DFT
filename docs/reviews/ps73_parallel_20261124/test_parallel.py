import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

def app():
    spec=importlib.util.spec_from_file_location("parallel",Path(__file__).with_name("parallel.py"))
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

class Contracts(unittest.TestCase):
    def setUp(self):
        self.p=app()
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name).resolve()
        self.origin=self.home/"old"
        self.origin.mkdir()
        self.ops=self.home/"parallel"
        self.ops.mkdir()

    def test_original_ub_selection_and_lock_untouched(self):
        for n in ("UB","selection.json","worker.lock"):
            (self.origin/n).write_bytes(n.encode())
        for a in ("UB","UT","UC","UVa"):
            d=self.p.arm_dir(self.ops,self.origin,a)
            d.mkdir(parents=True)
            (d/"selection.json").write_text(a)
        self.assertEqual([(self.origin/n).read_text() for n in ("UB","selection.json","worker.lock")],
                         ["UB","selection.json","worker.lock"])

    def test_paths_disjoint_even_for_ub_resume(self):
        dirs=[self.p.arm_dir(self.ops,self.origin,a) for a in ("UB","UT","UC","UVa")]
        self.assertEqual(len(set(dirs)),4)
        for d in dirs:
            self.assertFalse(self.origin in d.parents)
        with self.assertRaises(ValueError):
            self.p.arm_dir(self.origin/"new",self.origin,"UT")
        with self.assertRaises(ValueError):
            self.p.arm_dir(self.ops,self.origin,"UVb")

    def test_symlinked_workspace_refused(self):
        try:
            (self.ops/"runs").symlink_to(self.origin,target_is_directory=True)
        except OSError:
            self.skipTest("symlink privilege unavailable")
        with self.assertRaises(ValueError):
            self.p.arm_dir(self.ops,self.origin,"UT")

    def test_capacity_58_and_queue_lag(self):
        q="1|RUNNING|20\n2|PENDING|20\n368469|RUNNING|6"
        self.assertEqual(self.p.projected(q,12,{}),58)
        self.assertEqual(self.p.projected(q,6,{"101":6}),58)
        self.assertEqual(self.p.projected(q+"\n101|PENDING|6",6,{"101":6}),58)

    def test_capacity_over_or_indeterminate_refused(self):
        for q in ("1|RUNNING|49","1|RUNNING|40\n2|PENDING|9","1|RUNNING|bad","1|RUNNING|6\n1|RUNNING|6"):
            with self.assertRaises(ValueError):
                self.p.projected(q,12,{})
        self.assertEqual(self.p.projected("1|RUNNING|48",12,{}),60)

    def test_ub_release_is_success_only(self):
        for s in ("RUNNING","FAILED","TIMEOUT","PENDING"):
            self.assertFalse(self.p.ub_ready(s,None))
        self.assertFalse(self.p.ub_ready("COMPLETED",{"runner_rc":1,"technical_ok":False}))
        self.assertTrue(self.p.ub_ready("COMPLETED",{"runner_rc":0,"technical_ok":True}))

    def test_only_timeout_and_forward_checkpoint(self):
        self.assertTrue(self.p.resume_ok("UT","TIMEOUT",3350000,3200000))
        for a,s,h,b in (("UC","TIMEOUT",4,3),("UB","FAILED",4,3),("UVa","TIMEOUT",3,3),("UT","TIMEOUT",3,4)):
            self.assertFalse(self.p.resume_ok(a,s,h,b))

    def test_partial_duplicate_and_ambiguous_submit(self):
        calls=[]
        def send():
            calls.append(1)
            raise RuntimeError("lost reply")
        with self.assertRaises(RuntimeError):
            self.p.claim_submit(self.ops,{},send)
        with self.assertRaises(FileExistsError):
            self.p.claim_submit(self.ops,{},send)
        self.assertEqual(calls,[1])

if __name__=="__main__":
    unittest.main()
