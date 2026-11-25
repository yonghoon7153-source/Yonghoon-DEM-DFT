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
    ap.add_argument("--generic", action="store_true",
                    help="B2O3 전용 단계(cfgNNNN 이름 파싱 · O-motif 판정 · top_dft 선별)를 "
                         "**건너뛰고** 입력을 그대로 이완해 에너지만 낸다. "
                         "cif 뿐 아니라 xyz(extxyz, 격자 포함)도 읽는다. "
                         "⛔ 조성이 다른 구조끼리 E/atom 을 비교하지 말 것 — "
                         "판정은 E_above_hull 로 (convex_hull_ehull.py).")
    ap.add_argument("--vram_fraction", type=float, default=None,
                    help="이 프로세스가 쓸 수 있는 VRAM 비율 상한 (예: 0.10). "
                         "다른 UMA 런과 같이 돌 때 **이쪽이 먼저 죽게** 만들어 "
                         "기존 런을 지키려는 것이다.")
    A = ap.parse_args()
    out = Path(A.out); (out / "relaxed").mkdir(parents=True, exist_ok=True)

    if A.vram_fraction:
        import torch
        if torch.cuda.is_available():
            torch.cuda.set_per_process_memory_fraction(A.vram_fraction)
            print(f"⚙ VRAM 상한 {A.vram_fraction:.0%} — 넘으면 **이 프로세스가** 죽는다")

    src = Path(A.indir)
    if A.generic:
        cifs = sorted([f for f in src.iterdir()
                       if f.suffix.lower() in ('.cif', '.xyz', '.vasp', '.poscar')]) \
               if src.is_dir() else [src]
    else:
        cifs = sorted(src.glob("*.cif"))
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

    if A.generic:
        rows.sort(key=lambda r: r["E_per_atom"])
        print(f"\n{'structure':<28}{'nat':>5}{'E (eV)':>14}{'E/atom':>11}{'V (Å³)':>10}")
        print("-" * 68)
        for r in rows:
            print(f"{r['name'][:26]:<28}{r['n_atoms']:>5}{r['E']:>14.4f}"
                  f"{r['E_per_atom']:>11.5f}{r['V']:>10.2f}")
        comps = {r["n_atoms"] for r in rows}
        print(f"\n✓ {len(rows)} relaxed → {out/'relaxed'} · {out/'stage1_all.json'}")
        if len(comps) > 1:
            print(f"  ⛔ **원자수가 서로 다르다({sorted(comps)}).** 위 E/atom 순서를 "
                  f"자리 선호나 안정성 순위로 읽지 말 것 — 조성이 다르면 화학퍼텐셜이 "
                  f"섞인다(Wang 2025 가 낸 바로 그 오류).")
            print(f"  → 판정은 E_above_hull 로: "
                  f"python3 tools/doping/convex_hull_ehull.py --cif <relaxed>.cif "
                  f"--elements Li Y P S Cl O --mode uma")
        return 0

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
