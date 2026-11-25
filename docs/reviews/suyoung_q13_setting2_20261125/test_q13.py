import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

def module(name):
    path = Path(__file__).with_name(name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class Q13Tests(unittest.TestCase):
    def targets(self):
        return {k: {"common": True, "ln_S_over_F_interval_report_only": [-.02, .03],
                    "arms": {a: {"ln_pressure_interval": [-1., -.5]} for a in ("S", "F")}}
                for k in ("0.84", "0.90", "0.95")}

    def test_prepare_only(self):
        q = module("q13")
        rows = self.targets()
        rows["0.95"]["common"] = False
        self.assertEqual(q.decision(rows), "PREPARE_STAGE3_REVIEW")

    def test_single_missing_primary_closes(self):
        q = module("q13")
        for point in ("0.84", "0.90"):
            rows = self.targets()
            rows[point]["arms"]["S"]["ln_pressure_interval"] = None
            self.assertEqual(q.decision(rows), "CLOSE_2D_UNDISTINGUISHED")

    def test_no_finite_ratio_closes(self):
        q = module("q13")
        rows = self.targets()
        rows["0.90"]["ln_S_over_F_interval_report_only"] = [None, 0.1]
        self.assertEqual(q.decision(rows), "CLOSE_2D_UNDISTINGUISHED")

    def test_common_third_point_is_required(self):
        q = module("q13")
        rows = self.targets()
        rows["0.95"]["ln_S_over_F_interval_report_only"] = None
        self.assertEqual(q.decision(rows), "HOLD_OTHER_COMMON_POINT")

    def test_missing_input_is_technical(self):
        with self.assertRaises((KeyError, ValueError)):
            module("q13").decision({})

    def test_separate_physical_cores(self):
        choose = module("coordinate").choose_cores
        topology = {2:(0,1),3:(0,1),7:(0,4),8:(1,1)}
        self.assertEqual(choose(topology), {"S":2,"F":7})
        with self.assertRaises(ValueError):
            choose({2:(0,1),3:(0,1)})

    def test_missing_second_arm_or_same_core(self):
        validate = module("coordinate").validate_execution
        sample = {"S":{"arm":"S","cpu":2,"core":[0,1],"affinity":[2],"threads":1,"rc":0},
                  "F":{"arm":"F","cpu":3,"core":[0,1],"affinity":[3],"threads":1,"rc":0}}
        with self.assertRaises(ValueError):
            validate(sample)
        del sample["F"]
        with self.assertRaises(ValueError):
            validate(sample)

    def test_worker_error_never_becomes_decision(self):
        rows = {a:dict(arm=a,core=[0,i],cpu=i,affinity=[i],threads=1,rc=4 if i else 0,
                       started_ns=0,ended_ns=10) for i,a in enumerate("SF")}
        with self.assertRaises(ValueError):
            module("coordinate").validate_execution(rows)

    def test_archive_hash_mismatch_stops_reader(self):
        with tempfile.TemporaryDirectory() as name:
            folder=Path(name)
            (folder/"screen.txt").write_bytes(b"success")
            (folder/"SHA256SUMS").write_text("0"*64+"  screen.txt\n")
            with self.assertRaises(ValueError):
                module("coordinate").checks(folder,["screen.txt"])

    @unittest.skipUnless(sys.platform.startswith("linux"),"live affinity uses Linux")
    def test_real_scheduler_with_two_mock_workers(self):
        self.run_mock_pair(False)

    @unittest.skipUnless(sys.platform.startswith("linux"),"live affinity uses Linux")
    def test_failed_mock_worker_retains_finished_peer(self):
        self.run_mock_pair(True)

    def run_mock_pair(self,fail):
        coord=module("coordinate")
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            run=root/"run"
            run.mkdir()
            (root/"q13.py").write_text(
                "import json,os,sys,time\nfrom pathlib import Path\nBUDGET={'S':10,'F':10}\n"
                "if __name__=='__main__':\n"
                "    arm=sys.argv[sys.argv.index('--arm')+1]\n"
                "    cpu=int(sys.argv[sys.argv.index('--cpu')+1])\n"
                "    top=Path('/sys/devices/system/cpu')/f'cpu{cpu}'/'topology'\n"
                "    ids=[int((top/k).read_text()) for k in ['physical_package_id','core_id']]\n"
                "    out=Path(sys.argv[sys.argv.index('--run')+1])\n"
                "    (out/(arm+'_affinity.json')).write_text(json.dumps(dict(arm=arm,cpu=cpu,core=ids,"
                "affinity=list(os.sched_getaffinity(0)),threads=1)))\n"
                "    time.sleep(.3)\n"
                "    sys.exit(4 if arm=='S' and (out/'fail').exists() else 0)\n")
            if fail:
                (run/"fail").touch()
                with self.assertRaises(ValueError):
                    coord.run_pair(root,run,root,root)
            else:
                coord.run_pair(root,run,root,root)
            rows=json.loads((run/"execution.json").read_text())
            self.assertEqual({a:r["rc"] for a,r in rows.items()},{"S":4 if fail else 0,"F":0})
            self.assertNotEqual(rows["S"]["core"],rows["F"]["core"])

if __name__ == "__main__":
    unittest.main()
