"""Contract tests of the single-gate operator; all input is synthetic."""
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from contextlib import contextmanager
from unittest.mock import patch


def load():
    p = Path(__file__).with_name("setting2_run.py")
    s = importlib.util.spec_from_file_location("setting2_tested",p)
    module = importlib.util.module_from_spec(s)
    s.loader.exec_module(module)
    return module


run = load()
rule = SimpleNamespace(BAND=.005,grid_status=lambda d:"WITHIN_DEVELOPMENT_BAND" if d<=.005 else "OUTSIDE")


class Selection(unittest.TestCase):
    def test_only_twelve_and_sixteen_choose(self):
        values = {8:3., 12:.005, 16:.01, 24:7.}
        self.assertEqual(run.decision(rule,values), (.005,"PASS"))
        self.assertEqual(run.decision(rule,values|{16:.010000001})[1],"FAIL")
        self.assertEqual(run.decision(rule,values|{8:1.02,24:1.1})[1],"PASS")

    def test_missing_and_nonfinite_never_select(self):
        for bad in ({8:.78,12:1,16:1},{8:.7,12:float("nan"),16:1,24:1},{8:.8,12:1,16:0,24:.8}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                run.decision(rule,bad)

    def test_output_is_complete_exclusive_and_marks_setting_two(self):
        source = SimpleNamespace(PROTOCOL="prior",write_json=object())
        original = source.write_json
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"result.json"
            data = dict(setting=1,protocol="prior",status="TIME_LIMIT")
            with run.mark_native_result(source):
                source.write_json(path,data)
            self.assertIs(source.write_json,original)
            self.assertEqual(json.loads(path.read_bytes()),data)
            self.assertEqual((data["setting"],data["protocol"],data["status"]),(2,run.PROTOCOL,"TIME_LIMIT"))
            with self.assertRaises(FileExistsError):
                run.write_json(path,{"changed":True})
            self.assertEqual(json.loads(path.read_bytes()),data)

    def test_unexpected_native_result_path_rejected_and_writer_restored(self):
        sentinel = object()
        src = SimpleNamespace(PROTOCOL="old",write_json=sentinel)
        with self.assertRaises(ValueError),run.mark_native_result(src):
            src.write_json(Path("wrong_name"),dict(setting=1,protocol="old"))
        self.assertIs(src.write_json,sentinel)


class Terminal(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.p = Path(scratch.name)
        trace = b"data"
        self.ctx = SimpleNamespace(driver=SimpleNamespace(SOURCE={"solver":"id"}),
            compare=SimpleNamespace(read_native=lambda *args:([0.,1.],[0.,1.2])),
            solver=SimpleNamespace(WIDTH=1.,WALL_SPEED=.01,TARGET=.12))
        self.e = SimpleNamespace(identity={"setting":2}, ctx=self.ctx,rule=SimpleNamespace(bracket_value=lambda *args:.91),
            gap=SimpleNamespace(VERTICES=256,BASE_KERNEL="K",PAIR_MATERIAL="M"))
        (self.p/"trace.csv").write_bytes(trace)
        self.result = dict(arm="F",cells=8,setting=2,protocol=run.PROTOCOL,label="DEVELOPMENT_ONLY",
            origin="new",budget_s=1800,source_sha256=self.ctx.driver.SOURCE,points_count=99,status="TARGET_BRACKETED",
            elapsed_s=3.,steps=1,trace_sha256=run.sha(trace))
        run.write_json(self.p/"result.json",self.result)
        self.obs = dict(identity=self.e.identity,cells=8,geometry_sha256=["geom"],steps=1,interbody_calls=1,
            gap=dict(setting=2,cell_size_gap_correction=True,distance_based_contact_detection=False,
                     gap_law="positive_projected_support_gap_over_dt",boundary_vertices_per_body=256,
                     normal="pinned_field_mass_gradient_b_minus_a_with_center_fallback",
                     base_kernel_sha256="K",pair_material_sha256="M",calls=1),
            floor=dict(steps=1,floor_passes=2,disk_boundary_vertices=256,max_penetration=0.,accumulated_impulse=.012))
        run.write_json(self.p/"observation.json",self.obs)

    def observe(self):
        return run.target_receipt(self.e,8,self.p,self.obs,.1,["geom"],99)

    def test_bound_target(self):
        output = self.observe()
        self.assertEqual(output["bracket_steps"],[0,1])
        self.assertEqual(output["phi_m"],.91)
        self.assertEqual(output["observation_sha256"],run.sha((self.p/"observation.json").read_bytes()))

    def test_corrupt_trace_and_timeout_rejected(self):
        for status in ("TIME_LIMIT","GEOMETRY_LIMIT","INCOMPLETE"):
            (self.p/"result.json").write_text(json.dumps(self.result|{"status":status}))
            with self.subTest(status=status), self.assertRaises(ValueError):
                self.observe()
        (self.p/"result.json").write_text(json.dumps(self.result))
        (self.p/"trace.csv").write_bytes(b"changed")
        with self.assertRaises(ValueError): self.observe()

    def test_missing_gap_call_or_distance_filter_rejected(self):
        orig = self.obs["gap"]
        for patch_info in ({"calls":0},{"distance_based_contact_detection":True},{"base_kernel_sha256":"changed"}):
            self.obs["gap"] = orig|patch_info
            with self.subTest(patch_info=patch_info), self.assertRaises(ValueError): self.observe()

    def test_floor_impulse_must_close(self):
        self.obs["floor"]["accumulated_impulse"]=.022
        with self.assertRaises(ValueError): self.observe()

    def test_preexisting_or_failed_arm_is_never_reused(self):
        with self.assertRaises(ValueError): run.run_arm(self.e,8,self.p)
        arm = self.p/"F8"
        arm.mkdir()
        (arm/"incomplete.json").write_text("{}")
        with self.assertRaises(ValueError): run.summarize(self.e,self.p)

    def test_native_entry_records_success_and_retains_timeout(self):
        arrays = (None,list(range(99)),[1.]*99)
        solver = self.ctx.solver
        solver.LO = .15
        driver = self.ctx.driver
        driver.PROTOCOL = "old"
        driver.write_json = run.write_json
        @contextmanager
        def bind(ctx,seed,proj):
            ctx.solver.seed,ctx.solver.project_contacts = seed,proj
            yield
        self.e.fine = SimpleNamespace(bind_driver=bind)
        info = self.obs["gap"]
        class Gap:
            def __init__(self,k): self.count=0
            def project(self,*args): self.count+=1
            def metadata(self): return info|{"calls":self.count}
        self.e.gap.GapProjector = Gap
        self.ctx.kernel = object()
        class Floor:
            def __init__(obj): obj.boundary=object(); obj.audit=self.obs["floor"]
            def __call__(obj,*args): solver.project_contacts(.5)
        self.ctx.floor = SimpleNamespace(make_advance=lambda s,n:Floor())
        def native(arm,n,budget,out,advance):
            out.mkdir(); solver.seed(n)
            advance(None,None,None,None,arrays[1],arrays[2],80,.1,solver.LO+(1.-.1*solver.WALL_SPEED))
            (out/"trace.csv").write_bytes(b"data")
            result = self.result|{"setting":1,"protocol":driver.PROTOCOL,
                                   "status":"TIME_LIMIT" if out.name=="timeout" else "TARGET_BRACKETED"}
            driver.write_json(out/"result.json",result)
            return result
        driver.run_arm = native
        with patch.object(run,"seed_and_clock",return_value=(arrays,.1,["geom"])):
            run.run_arm(self.e,8,self.p/"success")
            self.assertEqual(json.loads((self.p/"success"/"target_receipt.json").read_bytes())["status"],"TARGET_BRACKETED")
            with self.assertRaisesRegex(ValueError,"TIME_LIMIT"):
                run.run_arm(self.e,8,self.p/"timeout")
            self.assertTrue((self.p/"timeout"/"incomplete.json").exists())
            self.assertFalse((self.p/"timeout"/"target_receipt.json").exists())


if __name__ == "__main__":
    unittest.main()
