# comp3 / comp5 v2 Pipeline Steps 1-3 — Deploy Guide

> Spawned 2026-05-10 from comp4_v2 production code (KISTI `/data/work/comp4_v2/1_step1to3/`).
> Verbatim copy with **only halogen split + filenames** changed.

---

## 1. Halogen split (per family Li5.4 PS4.4 X1.6)

| comp | formula              | Cl per fu | Br per fu | Cl in cell (5 fu) | Br in cell | `combinations(range(8), N)` | Stage 1b total |
|------|----------------------|-----------|-----------|-------------------|------------|------------------------------|----------------|
| comp3 | Li5.4PS4.4Cl1.0Br0.6 | 1.0       | 0.6       | 5                 | 3          | `N=5` → 56 perms             | 5 × 56 = 280   |
| comp4 | Li5.4PS4.4Cl0.8Br0.8 | 0.8       | 0.8       | 4                 | 4          | `N=4` → 70 perms             | 5 × 70 = 350   |
| comp5 | Li5.4PS4.4Cl0.6Br1.0 | 0.6       | 1.0       | 3                 | 5          | `N=3` → 56 perms             | 5 × 56 = 280   |

Cell: rhombo 5 fu (62 atoms), shared `ref_comp3.cif` (positions only — script reassigns species).

---

## 2. ⚠️ Known gotcha — `cache_stage1b.json` not saved by step1to3.py

`anneal_rank.py` **requires** `cache_stage1b.json` (full Stage 1b results) to run rank 1-4
post-hoc. But the production `step1to3.py` (verbatim) **only dumps top-10 to
`comp{3,4,5}_v2_results.json`** — not the full list.

**Options:**
- **(a) Skip ranks 2-4**: only run `step1to3.py` → champion.xyz from rank 0 only.
- **(b) Manually add cache save**: insert one line after Stage 1b sort (line ~99):
  ```python
  with open('cache_stage1b.json', 'w') as f:
      json.dump(h_results, f, default=lambda x: x.tolist() if hasattr(x, 'tolist') else x)
  ```
  Then `anneal_rank.py 1..4` works.
- **(c) Modify `anneal_rank.py`** to read top-10 from `comp{N}_v2_results.json`
  and limit `RANK ≤ 9`.

Default below uses **option (a)** — single rank0 run only. User can modify.

---

## 3. KISTI deploy (GPU0 = comp3, GPU1 = comp5)

### 3.1 Setup directories
```bash
ssh kserver116-27   # or wherever
mkdir -p /data/work/comp3_v2/1_step1to3 /data/work/comp5_v2/1_step1to3
```

### 3.2 Pull files from this repo
```bash
RAW=https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/debug-api-500-error-iukkt/필독/step1_halogen_li_anneal

# comp3
cd /data/work/comp3_v2/1_step1to3
for f in ref_comp3.cif comp3_v2_step1to3.py anneal_rank.py run_ranks_1to4.sh watchdog_comp3v2.sh; do
  wget -q "$RAW/comp3_lpscbr/$f"
done
chmod +x *.sh

# comp5
cd /data/work/comp5_v2/1_step1to3
for f in ref_comp3.cif comp5_v2_step1to3.py anneal_rank.py run_ranks_1to4.sh watchdog_comp5v2.sh; do
  wget -q "$RAW/comp5_lpscbr/$f"
done
chmod +x *.sh
```

### 3.3 Launch (parallel, ~14h each)
```bash
# Terminal 1: comp3 on GPU0
cd /data/work/comp3_v2/1_step1to3
nohup ./watchdog_comp3v2.sh > watchdog.out 2>&1 &
echo "comp3 PID: $!"

# Terminal 2: comp5 on GPU1
cd /data/work/comp5_v2/1_step1to3
nohup ./watchdog_comp5v2.sh > watchdog.out 2>&1 &
echo "comp5 PID: $!"
```

`CUDA_VISIBLE_DEVICES` is exported inside each watchdog: comp3=0, comp5=1.

### 3.4 Monitor
```bash
tail -f /data/work/comp3_v2/1_step1to3/run.log
tail -f /data/work/comp5_v2/1_step1to3/run.log
# or
nvidia-smi -l 5
```

### 3.5 Champion outputs (~14h later)
- `/data/work/comp3_v2/1_step1to3/comp3_v2_champion.xyz`
- `/data/work/comp5_v2/1_step1to3/comp5_v2_champion.xyz`
- `comp{3,5}_v2_results.json` (best_s, best_cl, best_br, li_spread, top10s, champion)

---

## 4. Verification checklist (before launch)

```bash
# Inside each comp dir
python -c "
from pymatgen.core import Structure
ref = Structure.from_file('ref_comp3.cif')
print(f'Atoms: {len(ref)}')
print(f'Composition: {ref.composition}')
# Should print: Atoms: 62, Composition: Li27 P5 S22 Br3 Cl5
"

# Confirm halogen split in script
grep 'combinations(range(8)' comp3_v2_step1to3.py   # should show: range(8), 5 (5 Cl)
grep 'combinations(range(8)' comp5_v2_step1to3.py   # should show: range(8), 3 (3 Cl)
```

---

## 5. Spawn diff summary (vs comp4 reference)

```diff
# comp3 vs comp4
- """comp4 v2 (Li5.4 PS4.4 Cl0.8 Br0.8) ...
+ """comp3 v2 (Li5.4 PS4.4 Cl1.0 Br0.6) ...

- print(f"\n=== Stage 1b: top 5 S × 70 Cl/Br = 350 LBFGS ===", flush=True)
- halogen_perms = list(combinations(range(8), 4))
- h_results = []; total = 5*70; done = 0
+ print(f"\n=== Stage 1b: top 5 S × 56 Cl/Br = 280 LBFGS ===", flush=True)
+ halogen_perms = list(combinations(range(8), 5))   # 5 Cl, 3 Br
+ h_results = []; total = 5*56; done = 0

- write(f'comp4_v2_anneal_rank{rank}.xyz', a)
+ write(f'comp3_v2_anneal_rank{rank}.xyz', a)
# (and all other comp4_v2_* → comp3_v2_*)
```

comp5 same pattern with `combinations(range(8), 3)` (3 Cl, 5 Br) and `comp5_v2_*`.

**Logic NOT changed**:
- ref structure load, free-site partitioning, Li_configs (seed=42, 27 of 54), build()
- Stage 1a (45 S placements all-Cl), LBFGS settings (fmax=0.01 or 0.005)
- Stage 2 (top 1 halogen × 20 Li), Stage 3 (500K 100ps + 300K 10ps + LBFGS)
- json.dump structure, champion copy, all print formats

---

## 6. Expected timing (per comp)

| Stage | Approx |
|-------|--------|
| 1a (45 LBFGS) | ~30 min |
| 1b (280 LBFGS, 200 steps each) | ~3.5 h |
| 2 (20 Li LBFGS) | ~15 min |
| 3 (5 × [100ps MD + 10ps quench + LBFGS]) | ~10 h |
| **Total** | **~14 h** |

comp4 took similar (5 × 70 = 350 in Stage 1b vs comp3/5's 280, so Stage 1b is ~20% faster for comp3/5).
