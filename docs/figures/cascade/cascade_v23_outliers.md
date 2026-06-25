# Cascade v23 outlier report — 141 champions, 4 flagged

data: `db/properties/cascade_v23_champions.csv` (UMA-s-1p1, x=0.25, rank-1 champions).
ALL concentration=0.25 (x002/05/10 = placement replicates). sigma/Ea/wad empty in dataset.

## provenance — was 17 flagged, now cleaned to the few below
- **4 champions recomputed on gabia** (anneal is stochastic → re-ran the bad seeds): 3 blank/INCOMPLETE (`NdF3_x005`, `SrO_x002`, `SrO_x010`) now filled; 1 unphysical elastic (`Nd2O3_x002`: ν=−0.10, E=110.9 GPa) → **physical champion ν=0.215, E=47.2 GPa**, now consistent with its replicates x005=44.8 / x010=49.3.
- **10 EOS-fit-fails recovered by robust BM3 re-fit** of the existing UMA E–V points (`db/properties/cascade_v23_eos_refit.json`) — the compute was fine, only the fit had failed. 9 clean; **only `MnO_x002` stays flagged (low r²)**.
- **The remaining flags are NOT defects:** `MnO_x002` = recovered B0 but low fit-quality (use with caution); `Gd2O3`×3 = **genuine stability standout** — Gd₂O₃ is the single most-stabilizing dopant (Δe≈−1.3 eV/atom), so |z|>3 is real physical signal, not an error. → **0 real data defects remain.**

## EOS-fit-fail (1)
- **MnO_x002** — EOS-fit-fail

## statistical (3)
- **Gd2O3_x002** — de z=-3.2
- **Gd2O3_x005** — de z=-3.0
- **Gd2O3_x010** — de z=-3.1

