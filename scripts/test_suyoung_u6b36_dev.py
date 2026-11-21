"""Synthetic contracts for the shifted U6(b) resolution ladder."""
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import tarfile
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


PATH = Path(__file__).resolve().with_name("suyoung_u6b36_dev.py")
SPEC = importlib.util.spec_from_file_location("u6b36_test_subject", PATH)
dev = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dev)


class RuleTests(unittest.TestCase):
    def test_A_accepts_shifted_only(self):
        got = dev.arm_rule([-1., -1., 0., .4])
        self.assertEqual(got["rule"], "A")
        self.assertAlmostEqual(got["interval"][0], .4 - .02)
        self.assertAlmostEqual(got["interval"][1], 1.6 + .02)

    def test_A_rejects_original_only(self):
        self.assertEqual(dev.arm_rule([-1., -1., 0., .9])["rule"], "UNCONVERGED")

    def test_A_both_inclusive_edges_and_outside(self):
        for sign in (-1., 1.):
            for ratio, rule in ((math.nextafter(.29, 0.), "UNCONVERGED"), (.29, "A"),
                                (.75, "A"), (math.nextafter(.75, 1.), "UNCONVERGED")):
                with self.subTest(sign=sign, ratio=ratio):
                    self.assertEqual(dev.arm_rule([-sign, -sign, 0., sign*ratio])["rule"], rule)

    def test_B_witness_and_constant(self):
        self.assertEqual(dev.arm_rule([-.01, -.01, 0., .009])["rule"], "B")
        self.assertEqual(dev.arm_rule([-.015, -.01, 0., .009])["rule"], "UNCONVERGED")
        self.assertEqual(dev.arm_rule([0.]*4)["interval"], [-.02, .02])
        self.assertEqual(dev.arm_rule([-.5, 0., .005, .004])["rule"], "B")

    def test_no_original_eight_cell_signal_on_shifted_ladder(self):
        self.assertNotIn("bias_signal", dev.arm_rule([.9, .04, 0., -.02]))
        with self.assertRaises(ValueError):
            dev.arm_rule([0., 0., 0., float("nan")])


def point_rows(pressure=.4):
    return {key: {"state":"VALUE", "pressure_MPa":pressure} for key in ("0.84","0.90","0.95")}


def history_fixture(folder, *, corrupt_trace=False):
    targets = {key: {"arms": {a: {"points_in_grid_order": [row]*4}
                              for a in ("S", "F")}} for key, row in point_rows().items()}
    targets["0.95"]["common"] = False
    for a in ("S", "F"):
        targets["0.95"]["arms"][a]["points_in_grid_order"][0] = {"state":"NOT_REACHED","pressure_MPa":None}
    inputs, files = {}, {}
    for a in ("S", "F"):
        for c in (12, 16, 24):
            name = a + str(c)
            trace = name.encode("ascii")
            sha = hashlib.sha256(trace).hexdigest()
            origin = "11-20-fixed-repeat" if a == "F" and c != 24 else "new"
            info = {"steps":1, "status":"TARGET_BRACKETED", "trace_sha256":sha, "origin":origin}
            inputs[name] = info
            receipt = dict(info, arm=a, cells=c, label="DEVELOPMENT_ONLY", protocol=dev.legacy.PROTOCOL,
                           source_sha256=dev.legacy.SOURCE, setting=1)
            files[f"run/arms/{name}/result.json"] = json.dumps(receipt).encode()
            files[f"run/arms/{name}/trace.csv"] = b"wrong" if corrupt_trace and name == "S12" else trace
    summary = {"protocol":dev.legacy.PROTOCOL, "label":"DEVELOPMENT_ONLY", "status":"DEVELOPMENT_READBACK",
               "setting":1, "resolutions":[8,12,16,24], "inputs":inputs, "targets":targets}
    files["run/summary.json"] = json.dumps(summary).encode()
    path = folder / "history.tar.gz"
    with tarfile.open(path, "w:gz") as archive:
        for name, data in files.items():
            member = tarfile.TarInfo(name)
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


class ReadbackTests(unittest.TestCase):
    def test_history_reuses_exact_six_and_rejects_wrong_archive(self):
        with tempfile.TemporaryDirectory() as d:
            path, sha = history_fixture(Path(d))
            with self.assertRaises(ValueError):
                dev.read_history(path, "0"*64)
            rows = dev.read_history(path, sha)
            self.assertEqual(set(rows), {(a,c) for a in ("S","F") for c in (12,16,24)})
            self.assertTrue(all(row["points"] == point_rows() for row in rows.values()))

    def test_old_eight_cell_misses_do_not_disqualify_shifted_target(self):
        with tempfile.TemporaryDirectory() as d:
            path, sha = history_fixture(Path(d))
            rows = dev.read_history(path,sha)
            for arm in ("S","F"):
                rows[(arm,36)] = {"points":point_rows()}
            got = dev.compare(rows,{})["targets"]["0.95"]
            self.assertTrue(got["common"])
            self.assertIsNotNone(got["ln_S_over_F_interval_report_only"])

    def test_history_rejects_inconsistent_member(self):
        with tempfile.TemporaryDirectory() as d:
            path, sha = history_fixture(Path(d), corrupt_trace=True)
            with self.assertRaises(ValueError):
                dev.read_history(path, sha)

    def test_closed_intervals_and_noise(self):
        rows = {(a,c): {"points":point_rows(.4 if a=="S" else .2)}
                for a in ("S","F") for c in dev.GRIDS}
        got = dev.compare(rows, {})
        self.assertEqual(got["resolutions"], [12,16,24,36])
        low, high = got["targets"]["0.90"]["ln_S_over_F_interval_report_only"]
        self.assertAlmostEqual(low, math.log(2)-.04)
        self.assertAlmostEqual(high, math.log(2)+.04)
        for c in dev.GRIDS:
            rows[("F",c)]["points"]["0.90"] = {"state":"NOISE","pressure_MPa":.008}
        self.assertIsNone(dev.compare(rows, {})["targets"]["0.90"]["ln_S_over_F_interval_report_only"][1])
        self.assertFalse(got["stage3_go"])
        self.assertFalse(got["u6_qualified"])

    def test_missed_target_is_local_but_missing_arm_is_incomplete(self):
        rows = {(a,c): {"points":point_rows()} for a in ("S","F") for c in dev.GRIDS}
        rows[("S",36)]["points"]["0.95"] = {"state":"NOT_REACHED","pressure_MPa":None}
        got = dev.compare(rows, {})
        self.assertEqual(got["status"], "DEVELOPMENT_READBACK")
        self.assertEqual(got["missing_36_targets"], {"S36":["0.95"]})
        self.assertFalse(got["targets"]["0.95"]["common"])
        self.assertIsNone(got["targets"]["0.95"]["ln_S_over_F_interval_report_only"])
        self.assertTrue(got["targets"]["0.90"]["common"])
        del rows[("S",36)]
        self.assertEqual(dev.compare(rows,{("S",36):"TIME_LIMIT"})["status"], "INCOMPLETE_INPUT")

    def test_run_forwards_36_and_never_an_old_arm(self):
        with patch.object(dev.legacy, "run_arm", return_value={"status":"TARGET_BRACKETED"}) as solver:
            dev.run("F", 25., Path("new"))
            solver.assert_called_once_with("F", 36, 25., Path("new"))

    def test_summary_time_limit_and_missing_arm_give_rc4_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            out = root/"summary.json"
            old, sha = history_fixture(root)
            rows = dev.read_history(old,sha)
            (root/"S36").mkdir()
            receipt = dict(arm="S",cells=36,origin="new",label="DEVELOPMENT_ONLY",setting=1,
                           protocol=dev.legacy.PROTOCOL,source_sha256=dev.legacy.SOURCE,status="TIME_LIMIT")
            (root/"S36"/"result.json").write_text(json.dumps(receipt),encoding="ascii")
            args = ["summarize","--history",str(old),"--runs",str(root),"--out",str(out)]
            with patch.object(dev,"read_history",return_value=rows):
                self.assertEqual(dev.main(args),4)
                self.assertEqual(json.loads(out.read_bytes())["unavailable"],
                                 {"S36":"TIME_LIMIT","F36":"MISSING_ARM_OR_RECEIPT"})
                before = out.read_bytes()
                self.assertEqual(dev.main(args),2)
                self.assertEqual(out.read_bytes(),before)

    def test_new_arm_trace_binding_and_terminal_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            old, sha = history_fixture(root)
            rows = dev.read_history(old,sha)
            folder = root/"S36"
            folder.mkdir()
            trace = b"wrong trace"
            (folder/"trace.csv").write_bytes(trace)
            receipt = dict(arm="S",cells=36,origin="new",label="DEVELOPMENT_ONLY",setting=1,
                           protocol=dev.legacy.PROTOCOL,source_sha256=dev.legacy.SOURCE,
                           trace_sha256="0"*64,status="TARGET_BRACKETED",steps=1)
            with patch.object(dev,"read_history",return_value=rows):
                for h, message in (("0"*64,"trace hash"),(hashlib.sha256(trace).hexdigest(),"trace columns")):
                    receipt["trace_sha256"] = h
                    (folder/"result.json").write_text(json.dumps(receipt),encoding="ascii")
                    with self.assertRaisesRegex(ValueError,message):
                        dev.summarize(old,root,root/"summary.json")
            self.assertFalse((root/"summary.json").exists())

    def test_complete_geometry_limit_preserves_reached_points_and_does_not_stop_launch(self):
        solver = SimpleNamespace(DIAMETER=.1, WIDTH=.7, TARGET=.12,
                                 model=SimpleNamespace(LAM=1.,MU=1.))
        dt = dev.legacy.step_size(solver,36)
        solver.WALL_SPEED = .1*solver.WIDTH/dt
        area = 49*math.pi*(solver.DIAMETER/2)**2
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            old, sha = history_fixture(root)
            rows = dev.read_history(old,sha)
            for arm in ("S","F"):
                folder = root/(arm+"36")
                folder.mkdir()
                trace = folder/"trace.csv"
                with trace.open("w",newline="",encoding="ascii") as out:
                    writer = csv.writer(out)
                    writer.writerow(dev.legacy.COLUMNS)
                    for step in (0,1,2):
                        h = solver.WIDTH-step*dt*solver.WALL_SPEED
                        writer.writerow([step,step*dt,h,step*.02,area/(solver.WIDTH*h)])
                receipt = dict(arm=arm,cells=36,origin="new",label="DEVELOPMENT_ONLY",setting=1,
                               protocol=dev.legacy.PROTOCOL,source_sha256=dev.legacy.SOURCE,
                               trace_sha256=hashlib.sha256(trace.read_bytes()).hexdigest(),status="GEOMETRY_LIMIT",steps=2)
                (folder/"result.json").write_text(json.dumps(receipt),encoding="ascii")
            with patch.object(dev,"read_history",return_value=rows), patch.object(dev.legacy,"fixed_solver",return_value=solver):
                got = dev.summarize(old,root,root/"summary.json")
                self.assertEqual(got["inputs"]["S36"]["status"],"GEOMETRY_LIMIT")
                self.assertTrue(got["targets"]["0.90"]["common"])
            with patch.object(dev,"run",return_value={"status":"GEOMETRY_LIMIT"}):
                self.assertEqual(dev.main(["run","--model","S","--budget","1","--out",str(root)]),0)

    def test_pinned_36_initialization_with_synthetic_reaction(self):
        def advance(x, v, affine, elastic, fields, volume, grid, dt, lid):
            self.assertEqual(grid, 360)
            self.assertEqual(len(set(fields)), 49)
            return x, v, affine, elastic, .13
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)/"F36"
            r = dev.legacy.run_arm("F",36,120.,folder,advance=advance)
            self.assertEqual(r["steps"], 1)
            self.assertEqual(dev.legacy.read_run(folder,"F",36)["status"], "TARGET_BRACKETED")
            with self.assertRaises(FileExistsError):
                dev.run("S",120.,folder)


if __name__ == "__main__":
    unittest.main()
