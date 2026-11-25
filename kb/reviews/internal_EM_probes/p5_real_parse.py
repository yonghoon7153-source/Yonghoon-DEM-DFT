import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
R = os.path.join(SCR, "..", "real", "run", "V5_s_outer_A_G4_e70_far_a4_a4")
for tag, d, stage, var in (("a4B as c1", R, "c1", "c1"), ("a4A as A5", os.path.join(R, "stageA"), "A5", "A5f")):
    osz = B.R2._read_raw(os.path.join(d, "OSZICAR")); out = B.R2._read_raw(os.path.join(d, "OUTCAR")); inc = B.R2._read_raw(os.path.join(d, "INCAR"))
    st = B.judge5(osz, out, inc, 0, stage)
    print(tag, "judge5:", st[0], "rows", st[1], "why", st[4], "| row_gate", B.row_gate(osz, stage))
    sec, why = B.secondary_numbers(osz, stage)
    print("   secondary:", "computed n=%s" % sec["n_steps"] if sec else why)
    print("   hist_max", B.hist_max(out), "| rms_jumps n", len(B.rms_jumps(osz, stage)))
    o = V.parse_outcar(B.R2._read(os.path.join(d, "OUTCAR")))
    o["_body"] = V._strip_incar_echo(B.R2._read(os.path.join(d, "OUTCAR")))[0]
    job = json.load(open(os.path.join(E_pkg := setup(os.path.join(SCR, "..", "T_p5"))["pkg"], "jobs.json")))["jobs"][0] if False else None
    meta = json.load(open("/home/user/Yonghoon-DEM-DFT/db/inputs/wad_a5_vasp_2026_11_20/jobs.json"))
    job = meta["jobs"][0]
    missing, bad, src = B.audit5(o, job, var)
    print("   audit5 missing", missing, "| bad", [b.split(" ")[0] for b in bad], "| echo", src["echo"])
    print("   energies parsed:", {k: (o.get(k) is not None) for k in ("TOTEN_eV", "E_sigma0_eV", "Edisp_eV")}, "| version", o.get("version")[:30])
    ev = B.R2.restart_evidence(d)
    import re
    print("   restart_evidence: istart", ev["istart"], "icharg", ev["icharg"], "not_read", ev["not_read_phrase"], "regex hit", re.search("the WAVECAR file was read successfully", ev["text"], re.M) is not None)
    print("   outcar_dims", B.R2.outcar_dims(B.R2._read(os.path.join(d, "OUTCAR"))))
