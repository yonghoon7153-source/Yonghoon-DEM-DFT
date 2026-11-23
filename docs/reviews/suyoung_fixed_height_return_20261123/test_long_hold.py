"""Manufactured checks for the long hold return and observation boundary. No MPM time stepping."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest


def load(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


here=Path(__file__).resolve().parent
l=load("long_hold",here/"long_hold.py")


def write_json(path,data):
    with path.open("x",encoding="utf8") as f:
        json.dump(data,f)


class PinnedDriver(unittest.TestCase):
    def test_only_observation_is_inserted(self):
        source=next((p/l.DRIVER for p in (here.parent.parent.parent, *[a/"history" for a in here.parents])
                     if (p/l.DRIVER).is_file()),None)
        if source is None:
            import os
            source=Path(os.environ["SHORT_HOLD_DRIVER"])
        original=source.read_bytes()
        result=l.derive_driver(original)
        self.assertEqual(result.count(l.CHECKPOINT),1)
        self.assertEqual(result.replace(l.CHECKPOINT,b""),original)
        self.assertIn(l.COMPLETED+l.CHECKPOINT,result)
        # Compiling the observer here never calls the numerical solver.
        compile(result,"fixed-driver","exec")
        self.assertNotEqual(l.digest(l.CHECKPOINT),l.digest(original))

    def test_wrong_source_fails_closed(self):
        with self.assertRaises(ValueError):
            l.derive_driver(l.COMPLETED)

    def test_schedule_and_time_limits(self):
        self.assertEqual(l.RAMP,{12:1638,24:3276})
        self.assertEqual(l.HOLD,{12:4800,24:9600})
        self.assertEqual(l.OLD_HOLD,{12:1200,24:2400})
        self.assertEqual(l.BUDGET,{12:2400,24:7200})
        self.assertEqual(l.HOLD[12]//300,l.HOLD[24]//600)
        self.assertEqual(l.HOLD[12]//300,16)


class Boundary(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.d=Path(self.tmp.name)
        self.files={name:(name+"\r\n1,0.5\r\n").encode() for name in l.CSV}
        self.spec={"physical_ids":[9,1]}
        self.files["layer_spec.json"]=json.dumps(self.spec).encode()
        for name,raw in self.files.items():
            (self.d/name).write_bytes(raw)
        self.state={k:hashlib.sha256(k.encode()).hexdigest() for k in ("x","v","affine","elastic","boundary","ids","mass")}
        self.fork={"step":1638,"state_sha256":self.state.copy(),"height":.8}
        plan=SimpleNamespace(receipt={"fork":self.fork.copy()},files=self.files)
        self.e=SimpleNamespace(replay={12:plan},q=SimpleNamespace(write_json=write_json),identity=dict(release="release"))

    def checkpoint(self):
        l.confirm_before_extension(self.d,self.e,12,self.fork,self.spec,self.state)

    def test_all_five_prefixes_and_materials_bound_with_receipt(self):
        self.checkpoint()
        for name in l.CSV:
            with (self.d/name).open("ab") as f:
                f.write(b"2,1\r\n")
        result=l.read_boundary(self.e,12,self.d)
        self.assertEqual(result["step"],2838)
        self.assertEqual(result["prefix_sha256"],{n:l.digest(self.files[n]) for n in l.CSV})
        self.assertEqual(result["replay_endpoint_state_sha256"],self.state)

    def test_changed_csv_stops_before_extra_step(self):
        for name in l.CSV:
            with self.subTest(name=name):
                (self.d/name).write_bytes(self.files[name].replace(b"0.5",b"0.6"))
                with self.assertRaises(ValueError):
                    self.checkpoint()
                self.assertFalse((self.d/"old_hold_boundary.json").exists())
                (self.d/name).write_bytes(self.files[name])

    def test_extra_time_row_before_continuation_is_rejected(self):
        p=self.d/"energy.csv"
        p.write_bytes(self.files[p.name]+b"2,0.75\r\n")
        with self.assertRaises(ValueError):
            self.checkpoint()

    def test_changed_fork_or_layer_identity(self):
        with self.assertRaises(ValueError):
            l.confirm_before_extension(self.d,self.e,12,self.fork|{"step":1639},self.spec,self.state)
        with self.assertRaises(ValueError):
            l.confirm_before_extension(self.d,self.e,12,self.fork,{"physical_ids":[1,9]},self.state)

    def test_later_edit_detected_on_summary(self):
        self.checkpoint()
        p=self.d/"layer_steps.csv"
        p.write_bytes(b"C"+self.files[p.name][1:])
        with self.assertRaises(ValueError):
            l.read_boundary(self.e,12,self.d)

    def test_bad_terminal_fingerprint(self):
        self.checkpoint()
        p=self.d/"old_hold_boundary.json"
        d=json.loads(p.read_bytes())
        d["replay_endpoint_state_sha256"]["v"]="lost"
        p.write_text(json.dumps(d))
        with self.assertRaises(ValueError):
            l.read_boundary(self.e,12,self.d)


class Windows(unittest.TestCase):
    def test_equal_time_impulses_require_two_fine_steps(self):
        row=lambda f,t:dict(floor_impulse=f,lid_downward_impulse=t)
        got=l.paired_pressure([row(3,2),row(2,2)],[row(4,1),row(0,0),row(2,1),row(0,1)],1,2)
        self.assertAlmostEqual(got["floor_MPa"]["mean"],-.5)
        self.assertAlmostEqual(got["lid_MPa"]["mean"],.5)
        self.assertEqual(got["floor_MPa"]["min"],-1)
        self.assertAlmostEqual(got["floor_MPa"]["rms"],math.sqrt(.5))
        self.assertAlmostEqual(got["mean_of_plates_MPa"]["mean"],0.)
        self.assertAlmostEqual(got["half_plate_difference_MPa"]["mean"],-.5)
        with self.assertRaises(ValueError):
            l.paired_pressure([row(1,2)],[row(2,2)],1,2)

    def test_all_sixteen_partitions_and_last_four(self):
        def synthetic_window(walls,layers,energies,dt,width):
            self.assertEqual(len(walls),len(layers))
            self.assertEqual(len(walls),len(energies))
            floor=l.average([r["floor_impulse"] for r in walls])*10/(dt*width)
            return dict(floor_mean_MPa=floor,lid_mean_MPa=0.,whole_delta_Py_MPa=floor,
                        floor_minus_lid_mean_MPa=floor,particle_ke={"mean":energies[0]})
        e=SimpleNamespace(short=SimpleNamespace(window=synthetic_window),fine=SimpleNamespace(DT={12:2.,24:1.}),
                          ctx=SimpleNamespace(solver=SimpleNamespace(WIDTH=10.)))
        obs={}
        arms={}
        for n in l.RAMP:
            size=300*(n//12)
            vals=[{"floor_impulse":0,"lid_downward_impulse":0}]*l.RAMP[n]
            for i in range(16):
                vals += [{"floor_impulse":(i+1)*2. if n==12 else 0.,"lid_downward_impulse":0}]*size
            ke=[0.]*(l.RAMP[n]+1)+[float(i+1) for i in range(16) for _ in range(size)]
            obs[n]=(vals,vals,ke)
            arms[n]={"windows":{}}
            for i,name in enumerate(l.WINDOW_NAMES):
                lo=l.RAMP[n]+size*i
                hi=lo+size
                arms[n]["windows"][name]=synthetic_window(vals[lo:hi],vals[lo:hi],ke[lo+1:hi+1],e.fine.DT[n],10.)
        windows=l.make_windows(e,arms,obs)
        self.assertEqual([w["source"] for w in windows],["previous"]*4+["extension"]*12)
        self.assertEqual([w["F12_minus_F24"]["floor_MPa"]["mean"] for w in windows],list(range(1,17)))
        self.assertEqual(windows[-1]["time_since_stop"],[9000.,9600.])
        tail=l.last_four(windows)["F12_minus_F24_floor_MPa"]
        self.assertEqual(tail["values"],[13,14,15,16])
        self.assertEqual(tail["last_minus_first"],3.)
        self.assertEqual(tail["mean"],14.5)
        with self.assertRaises(ValueError):
            l.last_four(windows[:-1])
        arms[24]["windows"][l.WINDOW_NAMES[3]]["floor_mean_MPa"]=-2.
        with self.assertRaises(ValueError):
            l.make_windows(e,arms,obs)


if __name__=="__main__":
    unittest.main()
