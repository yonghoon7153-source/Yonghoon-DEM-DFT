"""The native full-run readback uses tiny manufactured traces here; no field simulation."""
import csv
import io
import json
import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

_spec=importlib.util.spec_from_file_location("subject",Path(__file__).with_name("full_floor.py"))
f=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(f)


def fixture(pressures=(0., 0., .09, .12)):
    spec = NS(WIDTH=1., SPEED=.01, DT=.125)
    dt = .25
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    w.writerow(f.COLS)
    for i, p in enumerate(pressures):
        height = 1.-i*dt*.01
        w.writerow((i,i*dt,height,p,.78/height))
    raw = buf.getvalue().encode()
    prefix = b"".join(raw.splitlines(keepends=True)[:3])
    audit = dict(steps=len(pressures)-1, floor_passes=2*(len(pressures)-1),
                 positive_passes=sum(p>0 for p in pressures), accumulated_impulse=sum(pressures)*dt,
                 max_grid_impulse_error=0.,max_g2p_momentum_error=0.,max_penetration=0.,
                 disk_boundary_vertices=256)
    result=dict(arm="F",setting=1,cells=8,origin="new",label="DEVELOPMENT_ONLY",
                protocol="U6b-setting1-bottom-loading-v1",status="TARGET_BRACKETED",steps=len(pressures)-1,
                points_count=9653,budget_s=f.BUDGET[8],elapsed_s=1.,trace_sha256=f.sha(raw),source_sha256={})
    return spec,raw,prefix,result,audit


class Readback(unittest.TestCase):
    def test_first_positive_distinguished_from_terminal(self):
        data=f.validate_complete(*fixture(),cells=8,expected_sources={})
        self.assertEqual((data["first_nonzero_step"],data["terminal_step"]),(2,3))
        self.assertAlmostEqual(data["first_nonzero_displacement_code"],.005)
        self.assertAlmostEqual(data["terminal_pressure_MPa"],1.2)

    def test_single_step_positive_is_enough_only_if_terminal_target(self):
        data=f.validate_complete(*fixture((0.,0.,.123)),cells=8,expected_sources={})
        self.assertEqual(data["first_nonzero_step"],data["terminal_step"])

    def test_geometry_terminal_with_or_without_pressure(self):
        for pressure in (0.,.05):
            s,r,p,j,a=fixture([0.,0.]+[pressure]*99)
            data=f.validate_complete(s,r,p,dict(j,status="GEOMETRY_LIMIT"),a,cells=8,expected_sources={})
            self.assertIs(data["reached_target"],False)
            self.assertEqual(data["terminal_step"],100)
            self.assertEqual(data["first_nonzero_step"],2 if pressure else None)
            if not pressure:
                self.assertIsNone(data["first_nonzero_displacement_code"])

    def test_premature_geometry_and_disguised_target(self):
        for prs in ((0.,0.,.10,.11),tuple([0.]*100+[.12])):
            s,r,p,j,a=fixture(prs)
            with self.assertRaisesRegex(ValueError,"GEOMETRY"):
                f.validate_complete(s,r,p,dict(j,status="GEOMETRY_LIMIT"),a,cells=8,expected_sources={})

    def test_prefix_must_be_raw_identical(self):
        s,r,p,j,a=fixture()
        with self.assertRaises(ValueError):
            f.validate_complete(s,r,p.replace(b"0.0",b"0.00",1),j,a,cells=8,expected_sources={})

    def test_early_and_missing_crossings(self):
        for trace in ((0.,0.,.12,.125),(0.,0.,.01,.119)):
            with self.subTest(trace=trace),self.assertRaises(ValueError):
                f.validate_complete(*fixture(trace),cells=8,expected_sources={})

    def test_no_clipping_nonfinite_or_clock_substitution(self):
        s,r,p,j,a=fixture()
        for old,new in ((b"0.5,",b"0.5001,"),(b"0.09,",b"nan,"),(b"0.09,",b"-0.09,"),
                        (b"0.995,",b"0.994,")):
            changed=r.replace(old,new)
            self.assertNotEqual(changed,r)
            with self.subTest(new=new),self.assertRaises(ValueError):
                f.validate_complete(s,changed,p,dict(j,trace_sha256=f.sha(changed)),a,cells=8,expected_sources={})

    def test_native_receipt_fields(self):
        s,r,p,j,a=fixture()
        for k,v in {"source_sha256":{"other":"hash"},"trace_sha256":"wrong","steps":2,"points_count":39053,
                    "status":"TIME_LIMIT","origin":"copied","budget_s":10,"elapsed_s":float("nan")}.items():
            with self.subTest(k=k),self.assertRaises(ValueError):
                f.validate_complete(s,r,p,dict(j,**{k:v}),a,cells=8,expected_sources={})

    def test_impulse_schedule_and_material_penetration(self):
        s,r,p,j,a=fixture()
        for k,v in {"positive_passes":1,"floor_passes":7,"disk_boundary_vertices":32,"max_penetration":1e-6,
                    "accumulated_impulse":.8,"max_grid_impulse_error":-1.,"max_g2p_momentum_error":float("inf")}.items():
            with self.subTest(k=k),self.assertRaises(ValueError):
                f.validate_complete(s,r,p,j,dict(a,**{k:v}),cells=8,expected_sources={})

    def test_incomplete_run_cannot_be_reread_as_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"F8"
            p.mkdir()
            (p/"incomplete.json").write_text("{}")
            with self.assertRaisesRegex(ValueError,"INCOMPLETE"):
                f.read_arm(None,None,8,p)

    def native_mock(self,folder,*,reason="success"):
        m,raw,prefix,res,audit=fixture()
        init=(object(),object(),object())
        op=NS(dt_for=lambda m,c: m.DT*2,write_json=lambda p,v:p.write_text(json.dumps(v)))
        m.GEOMETRY={8:["x","id","vol"]}
        m.seed_arrays=lambda solver,c: init
        solver=NS(seed=lambda n:False,project_contacts=lambda *a:False,LO=.1)
        driver=NS(SOURCE={},field_ids=lambda a,ids:ids,fixed_solver=lambda:False)
        kernel=NS(project_contacts=lambda *args: 0)
        class Advance:
            def __init__(self):
                self.audit=audit
                self.n=0
            def __call__(self,*args):
                solver.project_contacts(.5)
                self.n+=1
                prs=[0.,.09,.12][self.n-1]
                return (None,None,None,None, .001 if reason=="wrong_prefix" and self.n==1 else prs)
        candidate=NS(make_advance=lambda s,c: Advance())
        def driver_arm(arm,cells,budget,out,*,advance):
            self.assertIs(driver.fixed_solver(),solver)
            self.assertEqual(budget,f.BUDGET[cells])
            out.mkdir()
            x,ids,vol=solver.seed(cells)
            for step in range(1,4):
                advance(x,None,None,None,ids,vol,80,.25,solver.LO+(m.WIDTH-step*.25*m.SPEED))
            (out/"trace.csv").write_bytes(raw)
            result=dict(res,status="GEOMETRY_LIMIT") if reason=="limit" else res
            (out/"result.json").write_text(json.dumps(result))
            return result
        driver.run_arm=driver_arm
        settings=(op,m,{"release":"synthetic"},driver,solver,kernel,candidate,{})
        saves=(solver.seed,solver.project_contacts,driver.fixed_solver)
        code=f.run_arm(settings,{8:prefix},8,folder)
        self.assertEqual((solver.seed,solver.project_contacts,driver.fixed_solver),saves)
        return code,settings,prefix

    def test_native_workflow_and_reread(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/"F8"
            code,parts,prior=self.native_mock(dest)
            self.assertEqual(code,0)
            _,rec=f.read_arm(parts,{8:prior},8,dest)
            self.assertEqual(rec["first_nonzero_step"],2)
            with self.assertRaisesRegex(ValueError,"EXISTING_ARM"):
                self.native_mock(dest)
            rec["prior_trace_sha256"]="incorrect"
            (dest/"full_receipt.json").write_text(json.dumps(rec))
            with self.assertRaisesRegex(ValueError,"FULL_RECEIPT"):
                f.read_arm(parts,{8:prior},8,dest)

    def test_partial_is_returned_on_native_stop_or_changed_prefix(self):
        with tempfile.TemporaryDirectory() as tmp:
            for reason in ("limit","wrong_prefix"):
                d=Path(tmp)/reason
                self.assertEqual(self.native_mock(d,reason=reason)[0],4)
                self.assertFalse((d/"full_receipt.json").exists())
                self.assertEqual(json.loads((d/"incomplete.json").read_text())["status"],"INCOMPLETE")

if __name__=="__main__":
    unittest.main()
