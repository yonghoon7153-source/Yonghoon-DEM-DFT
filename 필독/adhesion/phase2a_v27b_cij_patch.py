"""Phase 2a v27b — F (Cij vs adhesion) patch.

v27 F phase failed silently because elastic.json mlip_300K_supercell results
have 'comp5_A' and 'comp5_B' (Li ordering basin split, paper #1 finding) but
the script looked for plain 'comp5'.

v27b fixes:
- Use comp5_B (more representative basin, C44=13.9 close to comp3,4) as comp5
- Use mlip_600K_snapshot (richer dataset — has modelc + std)
- Fall back to mlip_300K_supercell_2x2x1 if 600K missing
- Compute R(Cij vs paper exp Wad) for all Cij components
- Compare with v15 R(Cl-O) = -0.91

Run on KISTI:
  conda activate uma
  cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
  wget -O phase2a_v27b_cij_patch.py 'https://.../phase2a_v27b_cij_patch.py'
  python3 phase2a_v27b_cij_patch.py 2>&1 | tee phase2a_v27_results/v27b_run.log
"""
import os, json, time, urllib.request
from pathlib import Path
import numpy as np

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
ALL_COMPS = PAPER_COMPS + ['modelC']
V15_R_CL_O = -0.9136

DB_BASE = "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/review-ml-migration-W29af/db/properties"

RESULTS_DIR = Path("phase2a_v27_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG = RESULTS_DIR / "v27b_run.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


def fetch_db(name):
    if Path(name).exists():
        return json.load(open(name))
    url = f"{DB_BASE}/{name}"
    log(f"  fetching {name} from GitHub...")
    return json.load(urllib.request.urlopen(url, timeout=15))


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if x.std() == 0 or y.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def main():
    t0 = time.time()
    log("=" * 70)
    log("v27b — F phase patched (Cij vs adhesion R)")
    log("=" * 70)

    elastic = fetch_db("elastic.json")

    # Try mlip_600K_snapshot first (richer dataset)
    sec_name = 'mlip_600K_snapshot'
    sec = elastic.get(sec_name, {}).get('results', [])
    if not sec:
        sec_name = 'mlip_300K_supercell_2x2x1'
        sec = elastic.get(sec_name, {}).get('results', [])

    log(f"\nUsing source: {sec_name}")

    # Map id -> row, with comp5_B as canonical comp5
    by_comp = {}
    for row in sec:
        rid = row.get('id', '')
        if rid in ('comp1', 'comp2', 'comp3', 'comp4'):
            by_comp[rid] = row
        elif rid == 'comp5_B':  # representative basin
            by_comp['comp5'] = row
        elif rid == 'modelc':
            by_comp['modelC'] = row

    # Print available
    log(f"\n--- Cij per comp (basin A skipped, using B for comp5) ---")
    fields = ['C11', 'C12', 'C44', 'K', 'G', 'E', 'nu']
    log(f"{'comp':<8} {'paper':>6} " + ' '.join(f"{f:>7}" for f in fields))
    for c in ALL_COMPS:
        row = by_comp.get(c, {})
        if not row:
            log(f"{c:<8} {'?':>6} {' MISSING ':>56}")
            continue
        paper = PAPER_EXP.get(c, '?')
        vals = [row.get(f) for f in fields]
        vals_s = []
        for v in vals:
            vals_s.append(f"{v:>7.2f}" if v is not None else "    N/A")
        log(f"{c:<8} {str(paper):>6} " + ' '.join(vals_s))

    # Compute R per Cij field
    log(f"\n--- R(Cij vs paper exp Wad), v15 R(Cl-O) = {V15_R_CL_O:+.4f} ---")
    paper_y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R_results = {}
    for f in fields:
        x = []
        valid = True
        for c in PAPER_COMPS:
            v = by_comp.get(c, {}).get(f)
            if v is None:
                valid = False
                break
            x.append(v)
        if not valid:
            log(f"  R({f:<4}) = N/A (missing)")
            continue
        R = pearson(x, paper_y)
        flag = "⭐" if abs(R) > 0.85 else ("+" if abs(R) > 0.7 else "")
        same_dir = "(same dir as Cl-O)" if R * V15_R_CL_O > 0 else "(opposite dir)"
        log(f"  R({f:<4}) = {R:+.4f}  {flag} {same_dir}")
        R_results[f] = R

    # Also basin A check (comp5_A is the anomalous basin)
    log(f"\n--- Basin A check (comp5_A) ---")
    comp5_A = next((r for r in sec if r.get('id') == 'comp5_A'), None)
    if comp5_A:
        log(f"  comp5_A: C44={comp5_A.get('C44',0):.2f}, "
            f"E={comp5_A.get('E',0):.2f}, K={comp5_A.get('K',0):.2f}")
        comp5_B = next((r for r in sec if r.get('id') == 'comp5_B'), None)
        if comp5_B:
            log(f"  comp5_B: C44={comp5_B.get('C44',0):.2f}, "
                f"E={comp5_B.get('E',0):.2f}, K={comp5_B.get('K',0):.2f}")
            log(f"  ΔC44 (B-A) = {comp5_B.get('C44',0)-comp5_A.get('C44',0):+.2f}")

        # Recompute R using basin A instead
        log(f"\n--- R using basin A (anomalous basin) for comp5 ---")
        by_comp_A = dict(by_comp)
        by_comp_A['comp5'] = comp5_A
        for f in fields:
            x = [by_comp_A.get(c, {}).get(f) for c in PAPER_COMPS]
            if any(v is None for v in x):
                continue
            R = pearson(x, paper_y)
            log(f"  R({f:<4}, basin A) = {R:+.4f}")

    log(f"\n=== v27b DONE: {(time.time()-t0):.1f} sec ===")
    json.dump({'source': sec_name, 'by_comp': by_comp, 'R_results': R_results,
              'v15_R_Cl-O_baseline': V15_R_CL_O},
             open(RESULTS_DIR / "v27b_summary.json", 'w'),
             indent=2, default=str)


if __name__ == "__main__":
    main()
