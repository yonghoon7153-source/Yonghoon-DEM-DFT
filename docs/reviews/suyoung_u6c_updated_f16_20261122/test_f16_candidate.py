"""Adapter contract tests using synthetic rows and a seed only; no field timestep."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.arm = Path(self.workspace.name)/"F16"

    def fake_run(self, driver, arm, cells, budget, out):
        self.assertEqual((arm, cells, budget), ("F",16,1740.))
        out.mkdir()
        solver = driver.fixed_solver()
        x, ids, volume = solver.seed(cells)
        fields = driver.field_ids(arm, ids)
        self.assertIs(fields,ids)
        solver.project_contacts(np.array([0,1]),np.array([0,0]),np.ones(2),np.array([[0.,0.],[1.,0.]]),
                                np.zeros((2,2)),np.array([[0.,0.],[1.,0.]]),.5)
        w, t, s = solver.WIDTH,driver.step_size(solver, cells),solver.WALL_SPEED
        h = w-t*s
        text = ("step,time_code,height,bottom_pressure_E,phi_m\n"
                f"0,0,{w},0,{volume.sum()/w**2}\n"
                f"1,{t},{h},0.12,{volume.sum()/(w*h)}\n")
        (out/"trace.csv").write_text(text,encoding="ascii")
        result=dict(protocol=driver.PROTOCOL,label="DEVELOPMENT_ONLY",setting=1,arm=arm,cells=cells,
                    source_sha256=driver.SOURCE,trace_sha256=driver.digest(out/"trace.csv"),steps=1,
                    points_count=len(x),status="TARGET_BRACKETED",budget_s=budget,elapsed_s=0.,origin="new")
        driver.write_json(out/"result.json",result)
        return result

    def perform(self, callback=None):
        mods = subject.modules(REPO)
        driver=mods["driver"]
        with patch.object(driver, "run_arm", side_effect=lambda *args:(callback or self.fake_run)(driver,*args)), \
             patch.object(subject, "modules", return_value=mods):
            return subject.run(REPO,self.arm,1740.)

    def test_real_seed_and_single_pair(self):
        self.assertEqual(self.perform(),0)
        c=subject.check_arm(REPO,self.arm)
        self.assertEqual((c["mapping"],c["candidate_calls"],c["cells"]),("ORIGINAL",1,16))
        self.assertEqual(c["geometry_sha256"]["physical_ids"], c["geometry_sha256"]["field_ids"])

    def test_setup_never_calls_the_integrator(self):
        mods=subject.modules(REPO)
        with patch.object(subject,"modules",return_value=mods), \
             patch.object(mods["driver"],"run_arm",side_effect=AssertionError("Unexpected run_arm")), \
             patch.object(mods["kernel"],"project_contacts",side_effect=AssertionError("Unexpected projection")):
            outcome=subject.check_setup(REPO)
        self.assertEqual(outcome["status"],"F16_SETUP_OK")
        self.assertEqual(outcome["geometry_sha256"],subject.GEOMETRY)
        self.assertEqual((outcome["dt"],outcome["width"],outcome["wall_speed"]),
                         (subject.F16_DT,subject.WIDTH,subject.SPEED))

    def test_field_relabel_rejected(self):
        def altered(driver, arm, cells, budget, out):
            out.mkdir()
            _,ids,_=driver.fixed_solver().seed(cells)
            driver.field_ids(arm,48-ids)
        self.assertEqual(self.perform(altered),4)
        self.assertFalse((self.arm/"candidate.json").exists())

    def test_missing_projector_call_rejected(self):
        def idle(driver,*args):
            solver=driver.fixed_solver()
            with patch.object(solver,"project_contacts"):
                return self.fake_run(driver,*args)
        self.assertEqual(self.perform(idle),4)
        self.assertFalse((self.arm/"candidate.json").exists())

    def test_geometry_change_rejected(self):
        solver = subject.modules(REPO)["driver"].fixed_solver()
        x,ids,vol=solver.seed(16)
        x[25,1]=np.nextafter(x[25,1], 2.)
        with self.assertRaises(ValueError):
            subject.seed_identity(x,ids,vol)

    def test_existing_output_preserved(self):
        self.arm.mkdir()
        (self.arm/"marker").touch()
        with self.assertRaises(FileExistsError):
            self.perform()
        self.assertEqual([p.name for p in self.arm.iterdir()],["marker"])

    def test_return_binding_rejects_changed_trace(self):
        self.assertEqual(self.perform(),0)
        with (self.arm/"trace.csv").open("ab") as f:
            f.write(b"\n")
        with self.assertRaises(ValueError):
            subject.check_arm(REPO,self.arm)

    def test_time_limit_incomplete(self):
        def limited(driver,*args):
            native=self.fake_run(driver,*args)
            native["status"]="TIME_LIMIT"
            (self.arm/"result.json").write_text(json.dumps(native),encoding="ascii")
            return native
        self.assertEqual(self.perform(limited),4)
        self.assertFalse((self.arm/"candidate.json").exists())
        self.assertEqual(json.loads((self.arm/"incomplete.json").read_text())["native_status"],"TIME_LIMIT")

    def test_native_contact_stop_captured_without_another_call(self):
        mods=subject.modules(REPO)
        driver=mods["driver"]
        def failed(arm,cells,budget,out):
            out.mkdir()
            solver=driver.fixed_solver()
            _,ids,_=solver.seed(cells)
            driver.field_ids(arm,ids)
            centers=np.array([[-1.,-.3],[1.,-.3],[0.,.9]])
            solver.project_contacts(np.arange(3),np.full(3,17),np.ones(3),centers,-centers,centers,.5)
        with patch.object(subject,"modules",return_value=mods), \
             patch.object(mods["kernel"],"MAX_ITERATIONS",0), patch.object(driver,"run_arm",side_effect=failed):
            self.assertEqual(subject.run(REPO,self.arm,1740.),4)
        stop=json.loads((self.arm/"contact_stop.json").read_text())
        receipt=json.loads((self.arm/"incomplete.json").read_text())
        self.assertEqual((stop["scope"],stop["attempted_step"],stop["nodes"][0]["node_id"]),
                         ("NATIVE_UNRESOLVED_ROWS",1,17))
        self.assertEqual(receipt["contact_stop_sha256"],subject.digest((self.arm/"contact_stop.json").read_bytes()))
        with self.assertRaises(ValueError):
            subject.check_arm(REPO,self.arm)

    def test_f8_lineage_mutation_refused(self):
        self.assertEqual(self.perform(),0)
        record=json.loads((self.arm/"candidate.json").read_text())
        record["f8_original_trace_sha256"]="0"*64
        (self.arm/"candidate.json").write_text(json.dumps(record),encoding="ascii")
        with self.assertRaises(ValueError):
            subject.check_arm(REPO,self.arm)

    def test_wrong_budget_no_output(self):
        with self.assertRaises(ValueError):
            subject.run(REPO,self.arm,1800.)
        self.assertFalse(self.arm.exists())


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[3])
    parser.add_argument("--subject",type=Path,default=Path(__file__).with_name("f16_candidate.py"))
    args,rest=parser.parse_known_args()
    REPO=args.repo
    spec=importlib.util.spec_from_file_location("f16_under_test",args.subject)
    subject=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(subject)
    unittest.main(argv=[sys.argv[0]]+rest)
