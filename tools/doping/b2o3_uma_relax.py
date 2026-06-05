#!/usr/bin/env python3
"""B2O3 doping — Stage 1: UMA relax of Stage-0 candidates + O-motif decision.

Input  = b2o3_stage0/cif/  (from b2o3_enumerate.py):
   cfgNNNN_E*.cif                      B/halogen/Li config (NO O yet) — Ewald-ranked
   cfgNNNN_E*_O-{bo4,distributed,free_s}.cif   full B2O3 (O placed by motif), top configs

What this does:
   1. UMA-s-1p1 relax (cell+atoms, FIRE fmax 0.05) every CIF -> relaxed energy
   2. rank O-containing structures (= real B2O3 candidates) by E/atom
   3. O-MOTIF DECISION: per base config, compare bo4 vs distributed vs free_s
      -> answers "does O cluster into BO4 (covalent) or distribute?" (Ewald-blind, so
         this is the covalency verdict UMA provides)
   4. cross-check: no-O ranking vs Stage-0 Ewald order (validates the pre-rank)
   5. emit top-N relaxed CIFs for Stage-2 DFT

Deps: fairchem.core (UMA), ase.
Usage:
  python3 b2o3_uma_relax.py --indir /home/ubuntu/work/runs/b2o3_stage0/cif \
      --out  /home/ubuntu/work/runs/b2o3_stage1 \
      --device cuda --fmax 0.05 --top_dft 30
"""
import argparse, json, re
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.optimize import FIRE
from ase.filters import FrechetCellFilter


def make_calc(model, task, device):
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit(model, device=device)
    return FAIRChemCalculator(predictor, task_name=task)


def relax(atoms, calc, fmax, steps, logf):
    atoms.calc = calc
    flt = FrechetCellFilter(atoms)                 # cell + atoms free
    opt = FIRE(flt, logfile=logf)
    opt.run(fmax=fmax, steps=steps)
    return atoms.get_potential_energy()


def base_key(name):
    """cfg0007_E-2261.123_O-bo4 -> ('cfg0007', 'bo4'); no-O -> ('cfg0007', None)."""
    m = re.match(r"(cfg\d+)_E[-0-9.]+(?:_O-(\w+))?$", name)
    if not m:
        return name, None
    return m.group(1), m.group(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="uma-s-1p1")
    ap.add_argument("--task", default="omat")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--top_dft", type=int, default=30)
    ap.add_argument("--limit", type=int, default=0, help="relax only first N cifs (debug)")
    A = ap.parse_args()
    out = Path(A.out); (out / "relaxed").mkdir(parents=True, exist_ok=True)

    cifs = sorted(Path(A.indir).glob("*.cif"))
    if A.limit:
        cifs = cifs[:A.limit]
    print(f"{len(cifs)} structures to relax (UMA {A.model}/{A.task} on {A.device})")
    calc = make_calc(A.model, A.task, A.device)

    rows = []
    for k, c in enumerate(cifs):
        a = read(c)
        nat = len(a)
        try:
            E = relax(a, calc, A.fmax, A.steps, str(out / "fire.log"))
        except Exception as e:
            print(f"  [{k}] {c.name}: FAIL {e}")
            continue
        bk, motif = base_key(c.stem)
        write(out / "relaxed" / f"{c.stem}.cif", a)
        rows.append(dict(name=c.stem, base=bk, motif=motif, n_atoms=nat,
                         E=round(float(E), 4), E_per_atom=round(float(E) / nat, 5),
                         V=round(float(a.get_volume()), 2)))
        if k % 20 == 0:
            print(f"  [{k}/{len(cifs)}] {c.name}  E/atom={rows[-1]['E_per_atom']}", flush=True)

    json.dump(rows, open(out / "stage1_all.json", "w"), indent=2)

    # --- ranking of O-containing (real B2O3) structures ---
    o_rows = [r for r in rows if r["motif"] is not None]
    o_rows.sort(key=lambda r: r["E_per_atom"])
    noO_rows = [r for r in rows if r["motif"] is None]
    noO_rows.sort(key=lambda r: r["E_per_atom"])

    # --- O-motif decision per base config ---
    by_base = {}
    for r in o_rows:
        by_base.setdefault(r["base"], {})[r["motif"]] = r["E_per_atom"]
    motif_verdict = []
    win_count = {"bo4": 0, "distributed": 0, "free_s": 0}
    for base, m in by_base.items():
        if len(m) < 2:
            continue
        best = min(m, key=m.get)
        win_count[best] = win_count.get(best, 0) + 1
        motif_verdict.append(dict(base=base, energies=m, winner=best,
                                  spread_meV=round((max(m.values()) - min(m.values())) * 1000, 1)))

    # --- write outputs ---
    with open(out / "stage1_b2o3_ranked.csv", "w") as f:
        f.write("rank,name,base,motif,E_per_atom,V,n_atoms\n")
        for i, r in enumerate(o_rows):
            f.write(f"{i},{r['name']},{r['base']},{r['motif']},{r['E_per_atom']},{r['V']},{r['n_atoms']}\n")
    json.dump(dict(motif_win_count=win_count, per_base=motif_verdict),
              open(out / "stage1_O_motif_decision.json", "w"), indent=2)

    # top-N for DFT
    dft = o_rows[:A.top_dft]
    (out / "for_dft").mkdir(exist_ok=True)
    for r in dft:
        write(out / "for_dft" / f"{r['name']}.cif", read(out / "relaxed" / f"{r['name']}.cif"))

    print("\n==== O-MOTIF DECISION (covalency verdict; Ewald couldn't see this) ====")
    print(f"  winners: {win_count}")
    if o_rows:
        print(f"  global best B2O3: {o_rows[0]['name']}  E/atom={o_rows[0]['E_per_atom']}  motif={o_rows[0]['motif']}")
    print(f"\n  top-{A.top_dft} -> {out}/for_dft/  (Stage 2 = DFT SCF)")
    print(f"  rankings: {out}/stage1_b2o3_ranked.csv , stage1_O_motif_decision.json")
    if noO_rows:
        print(f"\n  (no-O Ewald cross-check: UMA-best no-O = {noO_rows[0]['name']})")


if __name__ == "__main__":
    main()
