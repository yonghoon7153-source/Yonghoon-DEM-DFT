#!/usr/bin/env python3
"""Generate 12 finite-strain RELAX inputs for nd elastic (stress method).

Reads an SCF input (nd V0: cell + positions + &system/HUBBARD/ATOMIC_SPECIES),
applies the 6 Voigt strains x +/-h (default 0.005, tensor) as new_cell = cell.(I+E),
keeps crystal coords fixed, and writes strain_{11,22,33,23,13,12}_{p,m}.in with
calculation='relax'. Stress from each -> tools/modelc_v3/fit_elastic_cij_stress.py.

Preserves EVERYTHING in the source (DFT+U HUBBARD, nspin=2 starting_magnetization,
mixed USPP/PAW ATOMIC_SPECIES) by text-editing only: cell block + a few &control/
&electrons/&ions keys. Same protocol as modelc elastic_relaxed_ion (E=27.66 GPa).

Run on KISTI in the champion dir:
    python3 gen_nd_strain_inputs.py scf_k661.in
then sanity-check one (cat strain_11_p.in) before submitting the array.
"""
import re, sys
import numpy as np
from pathlib import Path

SRC = sys.argv[1] if len(sys.argv) > 1 else "scf_k661.in"
H = 0.005
STRAINS = {  # Voigt label -> unit symmetric strain tensor
    "11": [[1,0,0],[0,0,0],[0,0,0]], "22": [[0,0,0],[0,1,0],[0,0,0]],
    "33": [[0,0,0],[0,0,0],[0,0,1]], "23": [[0,0,0],[0,0,1],[0,1,0]],
    "13": [[0,0,1],[0,0,0],[1,0,0]], "12": [[0,1,0],[1,0,0],[0,0,0]],
}

txt = Path(SRC).read_text()

# --- parse CELL_PARAMETERS angstrom (3 vectors) ---
m = re.search(r"(CELL_PARAMETERS\s*\(?\s*angstrom\s*\)?\s*\n"
              r"(?:\s*[-+\d.eE]+\s+[-+\d.eE]+\s+[-+\d.eE]+\s*\n){3})", txt, re.I)
if not m:
    sys.exit("ERROR: CELL_PARAMETERS angstrom block not found")
cell_block = m.group(1)
cell = np.array([[float(x) for x in r.split()]
                 for r in cell_block.strip().splitlines()[1:4]])
print(f"V0 cell (A):\n{cell}\nV0 volume = {abs(np.linalg.det(cell)):.2f} A^3\n")

def edit(label, sign):
    E = H * sign * np.array(STRAINS[label], float)
    new_cell = cell @ (np.eye(3) + E)         # a_i' = a_i (I+E), E symmetric
    tag = f"strain_{label}_{'p' if sign>0 else 'm'}"
    t = txt
    # 1) strained cell
    cs = "CELL_PARAMETERS angstrom\n" + "\n".join(
        "  " + "  ".join(f"{x:18.12f}" for x in row) for row in new_cell) + "\n"
    t = t.replace(cell_block, cs)
    # 2) &control: scf->relax, prefix, outdir, tighten forces, ensure stress/force print
    t = re.sub(r"calculation\s*=\s*['\"][^'\"]*['\"]", "calculation = 'relax'", t, count=1)
    t = re.sub(r"prefix\s*=\s*['\"][^'\"]*['\"]", f"prefix = '{tag}'", t, count=1)
    t = re.sub(r"outdir\s*=\s*['\"][^'\"]*['\"]", f"outdir = './tmp_{tag}/'", t, count=1)
    if re.search(r"forc_conv_thr", t): t = re.sub(r"forc_conv_thr\s*=\s*[^\n]+", "forc_conv_thr = 1.0d-4", t, count=1)
    if re.search(r"tstress", t) is None: t = re.sub(r"(&CONTROL\s*\n)", r"\1  tstress=.true.\n  tprnfor=.true.\n", t, count=1, flags=re.I)
    # 3) &electrons: tighten conv_thr for accurate stress
    t = re.sub(r"conv_thr\s*=\s*[^\n]+", "conv_thr = 1.0d-9", t, count=1)
    # 4) &ions: bfgs (damp->bfgs); add block if missing
    if re.search(r"&IONS", t, re.I):
        t = re.sub(r"ion_dynamics\s*=\s*['\"][^'\"]*['\"]", "ion_dynamics = 'bfgs'", t, count=1)
    else:
        t = re.sub(r"(&ELECTRONS.*?\n\s*/\s*\n)", r"\1&IONS\n  ion_dynamics='bfgs'\n/\n", t, count=1, flags=re.S|re.I)
    # checks
    for must in ["HUBBARD", "starting_magnetization", "ATOMIC_SPECIES", "relax"]:
        if must.lower() not in t.lower():
            print(f"  !! WARN {tag}: '{must}' missing after edit — verify!")
    Path(f"{tag}.in").write_text(t)
    return tag

tags = [edit(l, s) for l in STRAINS for s in (+1, -1)]
print("generated", len(tags), "inputs:", " ".join(tags))
print("\nSANITY: diff vs source for strain_11_p (should show ONLY cell + control/electrons/ions):")
print("  diff <(sed -n '1,40p' %s) <(sed -n '1,40p' strain_11_p.in)" % SRC)
