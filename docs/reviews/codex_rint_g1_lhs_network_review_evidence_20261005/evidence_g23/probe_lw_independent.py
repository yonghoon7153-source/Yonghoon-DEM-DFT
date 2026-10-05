"""Independent G2 falsification probes; no production writes."""
import copy
import json
import math
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "source/scripts"))
from dem_analysis_core import calc_love_weber_stress
from analyze_contacts import load_atoms_raw

V = 4.0 * math.pi / 3.0
TM = {1: "AM_P", 2: "SE"}

def atom(t, x, z, force=None):
    a = dict(type=t, x=x, y=2., z=z, radius=1.)
    if force is not None:
        # Equal-radius dimer with center separation 1.8: independent 50/50
        # tensile-positive stress/atom virial is -0.9 * F per particle.
        a.update(sigma_xx=0., sigma_yy=0., sigma_zz=-0.9 * force / V)
    return a

def contact(i, j, x, midz, force):
    return dict(id1=i, id2=j, fx=0., fy=0., fz=-force,
                fn_x=0., fn_y=0., fn_z=-force,
                ft_x=0., ft_y=0., ft_z=0.,
                cp_x=x, cp_y=2., cp_z=midz)

def run(a, c, pz=20.):
    return calc_love_weber_stress(a, c, TM, pz, return_arrays=True)

def compact(r):
    return {k: r.get(k) for k in ("status", "vm_cv", "type_stress", "checks", "wall")}

def swapped_forces_same_global_virial():
    a = {1: atom(1, 2., 2., 1.), 2: atom(1, 2., 3.8, 1.),
         3: atom(2, 7., 2., 3.), 4: atom(2, 7., 3.8, 3.)}
    correct = run(a, [contact(1, 2, 2., 2.9, 1.), contact(3, 4, 7., 2.9, 3.)])
    wrong = run(a, [contact(1, 2, 2., 2.9, 3.), contact(3, 4, 7., 2.9, 1.)])
    assert correct["status"] == wrong["status"] == "OK"
    assert wrong["checks"]["virial_total_rel"] < 1e-15
    assert math.isclose(correct["type_stress"]["AM_P"]["ratio"], .5)
    assert math.isclose(wrong["type_stress"]["AM_P"]["ratio"], 1.5)
    return dict(correct=compact(correct), wrong_paired_contact_forces=compact(wrong))

def invalid_atom_geometry():
    # One malformed isolated particle disables the all-atoms c_strs gate;
    # its undefined tensor poisons the all-particle population.
    a, _ = load_atoms_raw(str(ROOT / "evidence_g23/atoms_nan_radius.csv"))
    r = run(a, [contact(1, 2, 2., 2.9, 1.)])
    assert r["status"] == "OK"
    assert r["vm_cv"] == 0.
    assert np.isnan(r["arrays_vm"][2])
    assert r["type_stress"]["AM_P"]["ratio"] == 0.
    return dict(result=compact(r), arrays_vm=r["arrays_vm"].tolist(),
                finite_AM_P_mean_but_false_zero_ratio=True)

def zero_force_invalid_decomposition():
    a = {1: atom(1, 2., 2.), 2: atom(1, 2., 3.8)}
    c = contact(1, 2, 2., 2.9, 0.)
    c["fn_z"] = -1. # Total force is zero but sum of its components is not.
    r = run(a, [c])
    assert r["status"] == "OK" and r["checks"]["force_decomp_rel"] == 0.
    return compact(r)

def zero_virial_valid_decomposition():
    a = {1: atom(1, 2., 2., 0.), 2: atom(1, 2., 3.8, 0.)}
    r = run(a, [contact(1, 2, 2., 2.9, 0.)])
    assert r["status"].startswith("FAILED") and math.isinf(r["checks"]["virial_total_rel"])
    return compact(r)

def nan_plate_height():
    a = {1: atom(1, 2., 2., 1.), 2: atom(1, 2., 3.8, 1.)}
    r = run(a, [contact(1, 2, 2., 2.9, 1.)], pz=float("nan"))
    assert r["status"] == "OK" and r["wall"]["plate_flag"] == "mesh"
    return compact(r)

if __name__ == "__main__":
    print(json.dumps(dict(swapped_forces=swapped_forces_same_global_virial(),
        invalid_geometry=invalid_atom_geometry(),
        zero_force_bad_decomposition=zero_force_invalid_decomposition(),
        zero_virial_valid=zero_virial_valid_decomposition(),
        nan_plate=nan_plate_height()), indent=2))
