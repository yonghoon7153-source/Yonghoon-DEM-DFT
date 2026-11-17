"""One-off fix (2026-11-17) for the idealized argyrodite files whose halide sits in the 4d hole.

Defect: PS4 S on 16e x = 0.6173 (apex toward 4d) + Li 24g caging 4c, but Cl written on 4d ->
Cl 2.36 A from four PS4 apex S, cage centre 4c empty. Fix = invert every non-halide atom through a
P (4b) site (r -> 2 r_P - r); halides stay. 4a and 4b map onto themselves, 16e x -> 1 - x, Li 24g
-> its inverse, so Cl on 4d becomes the Li-cage centre (Morgan/de Klerk notation: Cl on the cage site
4c, free S on 4a). Same structure as moving Cl 4d -> 4c in the old frame; this frame keeps the
pipeline site names (P_4b, S_16e, S_4a, Cl_4d, Li_24g) literally true.

What this does NOT do: relax anything (ideal special positions, for figures/reference only); decide
the S/Cl ordering of real Li6PS5Cl (this is one ordered model: all Cl on the cage site).
Usage: python3 make_fixed.py <repo_root>   (writes the *_Clcage_2026_11_17 files, prints checks)
"""
import sys, warnings, json, itertools
warnings.filterwarnings("ignore")
from pathlib import Path
import numpy as np
from ase.io import read, write

R = Path(sys.argv[1])
JOBS = [  # (broken source, fixed output stem, formats) — 사본 셋은 2026-11-17 에 .BROKEN_Cl_in_4d_hole 로 이름을 바꿨다 · 정본은 그대로
    ("db/structures/lpscl_F43m_24G_canonical.cif", "db/structures/lpscl_F43m_24G_ideal_Clcage_2026_11_17", ("cif",)),
    ("paper_figures/comp1_V0_cubic.cif.BROKEN_Cl_in_4d_hole", "paper_figures/comp1_V0_cubic_Clcage_2026_11_17", ("cif", "vasp", "xyz")),
    ("paper_figures/lpscl_primitive_1fu.cif.BROKEN_Cl_in_4d_hole", "paper_figures/lpscl_primitive_1fu_Clcage_2026_11_17", ("cif", "vasp")),
    ("db/structures/lpscl_b2o3_scheme_F43m.cif.BROKEN_Cl_in_4d_hole", "db/structures/lpscl_b2o3_scheme_F43m_Clcage_2026_11_17", ("cif",)),
]
HAL = ("Cl", "Br", "I")

def fix(at):
    s = np.array(at.get_chemical_symbols()); hal = np.isin(s, HAL)
    c = at.positions[np.where(s == "P")[0][0]]
    new = at.copy(); pos = new.get_positions(); pos[~hal] = 2 * c - pos[~hal]
    new.set_positions(pos); new.wrap(); return new

def mind(at, A, B):
    s = np.array(at.get_chemical_symbols()); iA = np.where(np.isin(s, A))[0]; iB = np.where(np.isin(s, B))[0]
    if not len(iA) or not len(iB): return None
    return round(float(min(at.get_distances(i, iB, mic=True).min() for i in iA)), 3)

def checks(at):
    s = np.array(at.get_chemical_symbols()); D = at.get_all_distances(mic=True)
    cen = np.where(np.isin(s, ["P", "B"]))[0]
    tet = [int(((D[i] < 2.6) & np.isin(s, ["S", "O"])).sum()) for i in cen]
    hal = np.where(np.isin(s, HAL))[0]
    cage = [int(((D[i] < 2.6) & (s == "Li")).sum()) for i in hal]
    return {"S-X_min": mind(at, ["S"], HAL), "O-X_min": mind(at, ["O"], HAL), "P-S_min": mind(at, ["P"], ["S"]),
            "Li-S_min": mind(at, ["Li"], ["S"]), "Li-X_min": mind(at, ["Li"], HAL),
            "anions_within_2.6_of_each_P_or_B": tet, "Li_within_2.6_of_each_halide": cage}

out = {}
for src, stem, fmts in JOBS:
    ext = src.replace(".BROKEN_Cl_in_4d_hole", "").rsplit(".", 1)[1]   # 바꾼 이름은 ase 가 형식을 못 알아본다
    a0 = read(R / src, format={"cif": "cif", "xyz": "xyz", "vasp": "vasp"}[ext]); a1 = fix(a0)
    rec = {"source": src, "n": len(a0), "a_A": [round(x, 4) for x in a0.cell.lengths()],
           "before": checks(a0), "after": checks(a1), "written": []}
    for f in fmts:
        p = R / f"{stem}.{f}"; write(p, a1, format={"cif": "cif", "vasp": "vasp", "xyz": "xyz"}[f]); rec["written"].append(str(p.relative_to(R)))
    out[stem.split("/")[-1]] = rec
print(json.dumps(out, indent=1, ensure_ascii=False))
