"""Check the wall split against synthetic native and observation returns."""
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent


class WallReadbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("wall_summary", HERE / "wall_summary.py")
        cls.subject = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.subject)

    def test_signed_split_on_native_max_not_max_of_each_component(self):
        # Rows are displacement, total, pre, post. The signed split can oppose.
        c = [(0.,0.,0.,0.), (.5,6.,3.,3.), (1.,10.,5.,5.)]
        f = [(0.,0.,0.,0.), (.25,1.,1.,0.), (.75,3.,0.,3.), (1.25,5.,1.,4.)]
        result = self.subject.decompose(c, f)
        self.assertEqual(result["common_end_u"], 1.)
        self.assertEqual(result["union_knots"], 5)
        worst = result["at_first_worst_total_gap"]
        self.assertEqual(worst["u"], 1.)
        self.assertEqual(worst["coarse_minus_fine_MPa"], {"total":6., "pre":4.5, "post":1.5})

    def test_keeps_opposing_effects_and_first_tie(self):
        coarse = [(0.,0.,0.,0.), (.25,2.,0.,2.), (.5,2.,2.,0.)]
        fine = [(0.,0.,0.,0.), (.25,1.,1.,0.), (.5,1.,0.,1.)]
        got = self.subject.decompose(coarse, fine)["at_first_worst_total_gap"]
        self.assertEqual(got["u"], .25)
        self.assertEqual(got["coarse_minus_fine_MPa"], {"total":1., "pre":-1., "post":2.})

    def fixture(self, parent, cell, width=1., dt=.25):
        module = self.subject
        folder = parent / f"F{cell}"
        folder.mkdir()
        def csv_bytes(names, records):
            stream = io.StringIO(newline="")
            writer = csv.writer(stream)
            writer.writerow(names)
            writer.writerows(records)
            return stream.getvalue().encode("ascii")
        trace = csv_bytes(module.TRACE, [(0,0,width,0,.78), (1,dt,.875,.5,.81), (2,2*dt,.75,1.,.84)])
        sha = lambda b: hashlib.sha256(b).hexdigest()
        trace_sha = sha(trace)
        result = dict(protocol="U6b-setting1-bottom-loading-v1",label="DEVELOPMENT_ONLY",setting=1,
                      origin="new",arm="F",cells=cell,trace_sha256=trace_sha,steps=2,
                      source_sha256={k:v for k,v in module.SOURCES.items() if k!="suyoung_u6b_dev.py"},
                      status="TARGET_BRACKETED")
        rdata = json.dumps(result).encode()
        wall = csv_bytes(module.WALL, [
            (1,.125,1.025,0,.09375,.03125,0.,0.,1,1,0,0,.5),
            (2,.25,.90,0,.1875,.0625,0.,0.,1,1,0,0,1.),
        ])
        observer = dict(status="DEVELOPMENT_WALL_READBACK",eligible_development_readback=True,
                        label="DEVELOPMENT_ONLY",setting=1, trace_sha256=trace_sha, expected_trace_sha256=trace_sha,
                        wall_sha256=sha(wall), result_sha256=sha(rdata), observer_sha256=self.observer_sha,
                        original_source_sha256=module.SOURCES, arm="F",cells=cell,steps=2,dt=dt,width=width,
                        E_MPa=10.,u6_qualified=False)
        for name, data in (("trace.csv",trace),("wall.csv",wall),("result.json",rdata),
                           ("observer.json",json.dumps(observer).encode())):
            (folder/name).write_bytes(data)
        return folder, trace_sha

    @property
    def observer_sha(self):
        return "0"*64

    def test_trace_sidecar_hash_and_scaling(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder, sha = self.fixture(Path(tmp),8)
            with patch.dict(self.subject.EXPECTED,{8:sha}):
                rows, receipt = self.subject.read_arm(folder,8,self.observer_sha)
                self.assertEqual(rows[0], (0.,0.,0.,0.))
                self.assertEqual(rows[-1], (.25,10.,7.5,2.5))
                self.assertEqual(receipt["trace_sha256"], sha)
                with (folder/"wall.csv").open("ab") as out:
                    out.write(b"\n")
                with self.assertRaises(ValueError):
                    self.subject.read_arm(folder,8,self.observer_sha)

    def test_wrong_coordinate_step_or_unnormalized_reaction_in_hash_consistent_sidecar(self):
        for old, new in [(b"1,0.125,",b"1,0.12,"), (b"1,0.125,",b"2,0.125,"),
                         (b"0.09375,0.03125",b"0.1,0.03125")]:
            with self.subTest(old=old,new=new), tempfile.TemporaryDirectory() as tmp:
                folder, sha = self.fixture(Path(tmp),8)
                side = folder / "wall.csv"
                raw = side.read_bytes()
                changed = raw.replace(old, new, 1)
                self.assertNotEqual(changed, raw)
                side.write_bytes(changed)
                obsfile = folder / "observer.json"
                obs = json.loads(obsfile.read_bytes())
                obs["wall_sha256"] = hashlib.sha256(changed).hexdigest()
                obsfile.write_text(json.dumps(obs))
                with patch.dict(self.subject.EXPECTED,{8:sha}), self.assertRaises(ValueError):
                    self.subject.read_arm(folder,8,self.observer_sha)

    def test_missing_arms_do_not_issue_readback(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.subject.summarize(Path(tmp),self.observer_sha)
            self.assertEqual(result["status"], "INCOMPLETE")
            self.assertFalse(result["u6_qualified"])
            self.assertNotIn("decomposition",result)

    def test_two_complete_returns_and_binding_to_observer_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hashes = {c:self.fixture(root,c)[1] for c in (8,16)}
            with patch.dict(self.subject.EXPECTED,hashes):
                report = self.subject.summarize(root,self.observer_sha)
                self.assertEqual(report["status"], "DEVELOPMENT_WALL_DECOMPOSED")
                self.assertEqual(report["decomposition"]["maximum_absolute_total_gap_MPa"],0.)
                self.assertEqual(report["arms"]["F16"]["curve_knots_with_initial_state"],3)
                bad = self.subject.summarize(root,"f"*64)
                self.assertEqual(set(bad["issues"]), {"F8","F16"})
                self.assertNotIn("decomposition",bad)


if __name__ == "__main__":
    unittest.main()
