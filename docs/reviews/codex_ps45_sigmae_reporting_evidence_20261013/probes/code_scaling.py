"""Small synthetic checks of pinned network_conductivity, no DEM runs or source edits.

Print JSON evidence to stdout. All monkeypatches are restored. This deliberately uses
equal radii for AM_P and AM_S to isolate the type correction from geometric changes.
"""
from __future__ import annotations
import contextlib
import copy
import hashlib
import io
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
REVIEW = Path(__file__).resolve().parents[1]
WORK = REVIEW.parent
for path in (WORK / "lhs_coverage_review_20260930/deps",
             WORK / "gen2_network_reverify3_20261007/deps",
             REVIEW / "source/scripts"):
    sys.path.insert(0, str(path))
import numpy as np
import scipy
import networkx
import network_conductivity as nc
import tau_flux as tf

PIN = "46cd0bdb872e7d6c85ca50ec4172e98377253130"
BASELINE = 0.05
ALTERNATE = 0.0041
RATIO = ALTERNATE / BASELINE
BRANCHES = {"full": "full", "bulk_only": "bulk_net", "constriction_only": "constr_net"}
ORIGINAL_REL = nc.sigma_AM_relative


def quiet(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(kind="mixed", delta=0.1, box=30.0, disc_fraction=None):
    """15 spheres: 3 columns x 5 heights, 22 contacts; exact sphere intersection discs."""
    r = 4.5
    d = 2 * r - delta
    atoms = {}
    for row in range(5):
        for col in range(3):
            aid = 1 + row * 3 + col
            ty = 1 if kind == "pure_pc" else 2
            if kind == "mixed":
                # Asymmetric routes contain P-P, P-S and S-S edges.
                ty = [[1, 2, 1], [1, 2, 2], [2, 2, 1], [1, 1, 2], [2, 1, 1]][row][col]
            atoms[aid] = dict(type=ty, x=r + col * d, y=r, z=r + row * d, radius=r)
    area = math.pi * (r * r - (d / 2) ** 2)
    if disc_fraction is not None:
        area = math.pi * (r * disc_fraction) ** 2
    contacts = []
    for row in range(5):
        for col in range(3):
            aid = 1 + row * 3 + col
            for other in ([aid + 3] if row < 4 else []) + ([aid + 1] if col < 2 else []):
                contacts.append(dict(id1=aid, id2=other, delta=delta, contact_area=area))
    return atoms, contacts, dict(target_types=[1, 2], scale=1.0, plate_z=2*r+4*d,
                                box_x=box, box_y=box, mode="electronic", type_map={1:"AM_P",2:"AM_S"})


def build_and_run(kind, contact_mode, baseline, off=False, delta=0.1, box=30.0, disc_fraction=None):
    a, c, kw = fixture(kind, delta, box, disc_fraction)
    nc.SIGMA_AM_ELECTRONIC = baseline
    nc.sigma_AM_relative = (lambda r, t: 1.0) if off else ORIGINAL_REL
    net = quiet(nc.build_network, a, c, **kw, contact_mode=contact_mode)
    raw = {}
    fields = {}
    for branch, suffix in BRANCHES.items():
        g, q, f = quiet(nc.solve_network, net, mode=branch, return_field=True)
        raw[suffix] = {"G": g, "q": q, "unrounded_mScm": None if q is None else q*baseline*1000,
                       "solve_info": copy.deepcopy(net["solve_info"][branch])}
        fields[suffix] = f
    published = quiet(nc.run_decomposition, a, c, **kw, contact_mode=contact_mode,
                      sigma_bulk=nc.SIGMA_AM_ELECTRONIC)
    return dict(raw=raw, published=published, edges=net["edges"], fields=fields,
                boundaries={"bottom":sorted(net["bottom"]),"top":sorted(net["top"]),
                            "rule":net["boundary_rule"]},
                flags={k: net[k] for k in ("n_floor_only","n_clamp_zero","area_binding_counts_physics")})


def compact(run):
    out = {"boundaries": run["boundaries"], "flags": run["flags"], "branches": {}}
    for suffix, val in run["raw"].items():
        p = run["published"]
        cert = p["solve_certificate_"+suffix]
        out["branches"][suffix] = {
            "q_raw":val["q"], "q_published":p["sigma_"+suffix],
            "mScm_raw":val["unrounded_mScm"], "mScm_published":p["sigma_"+suffix+"_mScm"],
            "status":p["sigma_"+suffix+"_status"], "reason":p["sigma_"+suffix+"_reason"],
            "certificate_problem":nc.certificate_problem(cert),
            "certificate": {k:cert.get(k) for k in ("channel","branch","role","sigma_bulk_S_cm",
                "status","reason","method","I_bottom","I_top","conservation_rel","residual_rel","g_to_q")},
        }
    return out


def relerr(value, reference):
    return abs(value-reference)/abs(reference) if reference else abs(value-reference)


def main():
    file_before = sha(Path(nc.__file__))
    runs = {}
    global_checks = []
    disabling_checks = []
    for mode in ("hertzian", "physics"):
        for kind in ("pure_pc", "pure_sc", "mixed"):
            tag = mode+"/"+kind
            base = build_and_run(kind, mode, BASELINE)
            new = build_and_run(kind, mode, ALTERNATE)
            off = build_and_run(kind, mode, BASELINE, off=True)
            runs[tag] = {"baseline":compact(base), "alternate":compact(new), "relative_disabled":compact(off)}
            branch_checks = {}
            for suffix in BRANCHES.values():
                br, nr = base["raw"][suffix], new["raw"][suffix]
                bc = copy.deepcopy(base["published"]["solve_certificate_"+suffix])
                nc_ = copy.deepcopy(new["published"]["solve_certificate_"+suffix])
                del bc["sigma_bulk_S_cm"]
                del nc_["sigma_bulk_S_cm"]
                old_dim = base["published"]["sigma_"+suffix+"_mScm"]
                new_dim = new["published"]["sigma_"+suffix+"_mScm"]
                branch_checks[suffix] = {
                    "raw_q_bitwise_equal":br["q"] == nr["q"],
                    "raw_info_equal":br["solve_info"] == nr["solve_info"],
                    "certificate_equal_except_sigma_bulk":bc == nc_,
                    "unrounded_ratio":nr["unrounded_mScm"]/br["unrounded_mScm"] if br["q"] else None,
                    "linear_relative_error":relerr(nr["unrounded_mScm"],br["unrounded_mScm"]*RATIO) if br["q"] else None,
                    "rounded_new_minus_rounded_old_times_ratio":new_dim-old_dim*RATIO if old_dim is not None else None,
                }
            global_checks.append({"case":tag,"edges_equal":base["edges"]==new["edges"],
                                  "fields_equal":base["fields"]==new["fields"],"branches":branch_checks})
            qratios = {suffix:off["raw"][suffix]["q"]/base["raw"][suffix]["q"]
                       for suffix in BRANCHES.values() if base["raw"][suffix]["q"] and off["raw"][suffix]["q"]}
            edge_ratios = {key:sorted(set(round(e1[key]/e0[key], 12)
                                  for e0,e1 in zip(base["edges"],off["edges"]) if e0[key]))
                           for key in ("R_bulk","R_constriction","R_total")}
            v0 = base["fields"]["full"]["node_V"]
            v1 = off["fields"]["full"]["node_V"]
            disabling_checks.append({"case":tag,"q_disabled_over_original":qratios,
                                     "edge_R_disabled_over_original_unique":edge_ratios,
                                     "maximum_voltage_change":max(abs(v1[k]-v0[k]) for k in v0)})

    # Exercise the real top-level consumer of the global, including merged certificates.
    top_level = []
    nc.sigma_AM_relative = ORIGINAL_REL
    for mode in ("hertzian", "physics"):
        records = []
        for baseline in (BASELINE, ALTERNATE):
            a,c,kw = fixture("mixed")
            # Independent SE replica makes the ionic parent record exist.
            a.update({aid+100:{**atom,"type":3,"y":18.0} for aid,atom in list(a.items())})
            c += [{**edge,"id1":edge["id1"]+100,"id2":edge["id2"]+100} for edge in list(c)]
            nc.SIGMA_AM_ELECTRONIC=baseline
            rec = quiet(nc._run_all_networks, a,c,[3],[1,2],{1:"AM_P",2:"AM_S",3:"SE"},
                        1.0,kw["plate_z"],30.0,30.0,str(REVIEW/"tmp"),contact_mode=mode)
            records.append(rec)
        old,new=records
        accepted_patched=tf.sigma0_binding_problems(new)
        nc.SIGMA_AM_ELECTRONIC=BASELINE
        after_restore=tf.sigma0_binding_problems(new)
        top_level.append({"contact_mode":mode,"original_mScm":old["electronic_sigma_full_mScm"],
            "alternate_mScm":new["electronic_sigma_full_mScm"],
            "q_equal":old["electronic_sigma_full"]==new["electronic_sigma_full"],
            "status_original":old["electronic_status"],"status_alternate":new["electronic_status"],
            "sigma_binding_problems_while_patched":accepted_patched,
            "sigma_binding_problems_after_restore":after_restore})

    # Check a cap/floor case without inventing a valid constriction-only result.
    barriers=[]
    for mode,kind,box,disc_fraction in (("physics","mixed",30.0,0.999),
                                       ("physics","mixed",4.0,None),
                                       ("hertzian","mixed",4.0,None),
                                       ("hertzian","pure_pc",30.0,0.0)):
        args=dict(box=box,disc_fraction=disc_fraction)
        base=build_and_run(kind,mode,BASELINE,**args)
        new=build_and_run(kind,mode,ALTERNATE,**args)
        off=build_and_run(kind,mode,BASELINE,off=True,**args)
        barriers.append({"contact_mode":mode,"kind":kind,"delta":0.1,"box":box,"disc_fraction":disc_fraction,
            "physical_geometry":False,
            "purpose":"synthetic defensive-branch stress; deliberately inconsistent area or box; not physical evidence",
            "baseline":compact(base),"alternate":compact(new),"relative_disabled":compact(off)})

    nc.SIGMA_AM_ELECTRONIC=BASELINE
    nc.sigma_AM_relative=ORIGINAL_REL
    return {"pinned_commit":PIN,"source_sha256":file_before,"source_sha256_after":sha(Path(nc.__file__)),
        "python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"networkx":networkx.__version__,
        "scope":"synthetic only; actual imported build_network/solve_network/run_decomposition/_run_all_networks; source read-only",
        "fixture":"15 nodes, 22 edges, equal r=4.5 um, 3 columns x 5 layers, intersection-disc contacts, 3 bottom + 3 top nodes under L0",
        "baseline_S_cm":BASELINE,"alternate_S_cm":ALTERNATE,"expected_scaling":RATIO,
        "factor_r45":ORIGINAL_REL(4.5,"AM_P"),"exact_factor_r45":"8/35",
        "exact_disable_multiplier":35/8,"rounded_0229_disable_multiplier":1/0.229,
        "rounded_0229_relative_error":relerr(1/0.229,35/8),
        "global_checks":global_checks,"disabling_checks":disabling_checks,
        "top_level_checks":top_level,"barriers":barriers,"runs":runs}


if __name__ == "__main__":
    try:
        print(json.dumps(main(),ensure_ascii=True,indent=2))
    finally:
        nc.SIGMA_AM_ELECTRONIC=BASELINE
        nc.sigma_AM_relative=ORIGINAL_REL
