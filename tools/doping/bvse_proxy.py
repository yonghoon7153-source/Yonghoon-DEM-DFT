#!/usr/bin/env python
"""bvse_proxy.py — Bond Valence Site Energy proxy (pure Python, no UMA).

Computes per-Li bond valence sums from final relaxed geometry and reports
distribution statistics that correlate with Li migration barrier.

Theory:
  BVS_Li = Σ exp((R0 - R_ij) / b)
  where the sum is over neighboring anions j (S, Cl, Br, I, O, N, F).
  R0 (single-bond reference length) and b (universal soft-cutoff) are
  tabulated per cation-anion pair (Brown 2002 + Adams 2003 BVS database).

  An ideal Li⁺ site has BVS ≈ 1.0 (full nominal valence). σ-fast ionic
  conductors exhibit BROAD BVS distributions across Li sites (Adams 2003
  / Mo 2014), indicating energetically near-equivalent positions and
  thus low migration barriers — the Li atom essentially sees a flat
  potential energy landscape.

Output per structure:
  bvs_li_mean, bvs_li_std, bvs_li_min, bvs_li_max
  n_li_undervalent (BVS < 0.7), n_li_overvalent (BVS > 1.3)
  bvs_li_proxy_score = std × (1 - |mean − 1.0|)  — higher = more sigma-favorable

Higher proxy score → flatter PES → expected faster σ.

Usage:
  python3 tools/doping/bvse_proxy.py \\
      --xyz_dir runs/.../structures \\
      --out runs/.../bvs_report.json

  # Or single file
  python3 tools/doping/bvse_proxy.py --xyz foo.xyz
"""
import argparse
import json
import math
from pathlib import Path
import sys
import numpy as np
from ase.io import read

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


# Bond valence parameters R0 (Å), b (Å) for Li-anion pairs.
# Sources: Brown & Altermatt 1985 (oxides), Adams 2003 (sulfides/halides),
# Mo et al. 2014 (BVSE refinement for Li ion conductors).
BVS_PARAMS = {
    'O':  {'R0': 1.466, 'b': 0.37},
    'S':  {'R0': 1.94,  'b': 0.40},   # Adams 2003 Li-S
    'Se': {'R0': 2.10,  'b': 0.40},
    'Te': {'R0': 2.32,  'b': 0.40},
    'F':  {'R0': 1.36,  'b': 0.37},
    'Cl': {'R0': 1.91,  'b': 0.37},
    'Br': {'R0': 2.07,  'b': 0.37},
    'I':  {'R0': 2.29,  'b': 0.37},
    'N':  {'R0': 1.61,  'b': 0.37},
}
NEIGHBOR_CUTOFF_A = 5.0  # neighbors within this distance contribute


def compute_migration_volume(atoms, bvs_lo: float = 0.8,
                            bvs_hi: float = 1.2,
                            n_grid: int = 20,
                            cutoff: float = 5.0) -> dict:
    """Quantitative Li-migration accessible volume.

    Samples an n_grid³ uniform fractional grid throughout the unit cell,
    treats each grid point as a virtual Li site, computes the bond
    valence sum from neighboring anions, and counts the fraction of
    grid points falling within [bvs_lo, bvs_hi] — the energetically
    acceptable range for a Li⁺ ion (Adams 2010 / Mo 2014).

    Higher migration_volume_fraction → larger accessible region → faster
    Li transport (BVSE-style cheap proxy for AIMD σ). Not a substitute
    for full AIMD, but provides an O(seconds) screening filter for the
    "Top-N to invest in AIMD" decision.

    Output:
      migration_volume_fraction: ratio of acceptable grid points
      accessible_volume_A3: that fraction × cell volume
      grid_bvs_mean / grid_bvs_std: bulk BVS landscape statistics
      bvs_threshold_used: (lo, hi)
    """
    syms = atoms.get_chemical_symbols()
    anion_idx = [i for i, s in enumerate(syms) if s in BVS_PARAMS]
    if not anion_idx:
        return {'migration_volume_fraction': 0.0,
               'accessible_volume_A3': 0.0,
               'error': 'no anions'}

    cell = atoms.cell.array
    pos = atoms.get_positions()
    anion_pos = pos[anion_idx]
    anion_syms = [syms[i] for i in anion_idx]

    # Fractional grid
    one = np.linspace(0, 1, n_grid, endpoint=False)
    frac = np.array(np.meshgrid(one, one, one, indexing='ij')).reshape(3, -1).T
    cart = frac @ cell  # (n_grid³, 3)

    # PBC-replicated anions for fast tree lookup
    from scipy.spatial import cKDTree
    shifts = np.array([[i, j, k] for i in (-1, 0, 1)
                       for j in (-1, 0, 1) for k in (-1, 0, 1)])
    anion_pbc = np.concatenate([anion_pos + s @ cell for s in shifts])
    anion_pbc_syms = anion_syms * 27

    tree = cKDTree(anion_pbc)
    distances, indices = tree.query(cart, k=25,
                                   distance_upper_bound=cutoff)

    # Vectorized BVS accumulation: pre-compute per-symbol R0, b arrays
    R0_arr = np.array([BVS_PARAMS[s]['R0'] for s in anion_pbc_syms])
    b_arr = np.array([BVS_PARAMS[s]['b'] for s in anion_pbc_syms])
    # For each grid point, accumulate exp((R0 - d)/b) over its neighbors
    bvs_grid = np.zeros(cart.shape[0])
    for k in range(distances.shape[1]):
        col_d = distances[:, k]
        col_i = indices[:, k]
        valid = (col_d < np.inf) & (col_i < len(anion_pbc))
        if not valid.any():
            continue
        idx = col_i[valid]
        bvs_grid[valid] += np.exp((R0_arr[idx] - col_d[valid]) / b_arr[idx])

    n_total = len(bvs_grid)
    accessible_mask = (bvs_grid >= bvs_lo) & (bvs_grid <= bvs_hi)
    n_accessible = int(accessible_mask.sum())
    vol_cell = atoms.get_volume()

    return {
        'migration_volume_fraction': n_accessible / n_total,
        'accessible_volume_A3': (n_accessible / n_total) * vol_cell,
        'grid_resolution': n_grid,
        'grid_bvs_mean': float(bvs_grid.mean()),
        'grid_bvs_std': float(bvs_grid.std()),
        'bvs_threshold_used': [bvs_lo, bvs_hi],
        'cutoff_A': cutoff,
    }


def compute_bvs_per_li(atoms) -> dict:
    """Bond valence sum per Li atom + distribution stats."""
    syms = atoms.get_chemical_symbols()
    li_idx = [i for i, s in enumerate(syms) if s == 'Li']
    anion_idx = [i for i, s in enumerate(syms) if s in BVS_PARAMS]
    if not li_idx or not anion_idx:
        return {'error': 'no Li or no anions'}

    D = atoms.get_all_distances(mic=True)
    bvs_values = []
    for li in li_idx:
        bvs = 0.0
        for j in anion_idx:
            r = D[li, j]
            if r > NEIGHBOR_CUTOFF_A:
                continue
            sym = syms[j]
            p = BVS_PARAMS[sym]
            bvs += math.exp((p['R0'] - r) / p['b'])
        bvs_values.append(bvs)
    arr = np.array(bvs_values)

    mean = float(arr.mean())
    std = float(arr.std())
    # Proxy: σ-fast Li conductors have FLAT PES across Li sites, i.e. BVS≈1.0
    # consistently with SMALL std (Adams 2003 / Mo 2014 BVSE landscape). Fixed
    # sign convention vs earlier version (which inverted the chemistry):
    # high std means some deep-trap + some over-coordinated sites that block
    # percolation. Score combines (closeness of mean to 1) × (1 - std).
    deviation_from_1 = abs(mean - 1.0)
    proxy = max(0.0, 1.0 - deviation_from_1) * max(0.0, 1.0 - std)

    return {
        'bvs_li_mean': mean,
        'bvs_li_std': std,
        'bvs_li_min': float(arr.min()),
        'bvs_li_max': float(arr.max()),
        'n_li_undervalent_lt_0p7': int(np.sum(arr < 0.7)),
        'n_li_overvalent_gt_1p3': int(np.sum(arr > 1.3)),
        'n_li_ideal_0p8_to_1p2': int(np.sum((arr > 0.8) & (arr < 1.2))),
        'bvs_li_proxy_score': float(proxy),
        'bvs_values': arr.tolist(),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--xyz', nargs='+', help='Individual xyz files')
    p.add_argument('--xyz_dir', help='Directory to scan recursively')
    p.add_argument('--out', required=True, help='Output JSON')
    p.add_argument('--backfill', action='store_true',
                  help='이미 있는 json 에 li_mobility_score 만 채운다 (**새 계산 0**). '
                       '입력 두 개(migration_volume_fraction · bvs_li_proxy_score)가 '
                       '이미 저장돼 있으므로 산수만 하면 된다. 구조·격자 재계산 없음. '
                       '멱등 — 이미 있으면 값이 같은지 확인만 하고 넘어간다.')
    p.add_argument('--grid_resolution', type=int, default=20,
                  help='Migration volume grid (default 20³ = 8000 points; '
                       'increase to 30 for finer scan at ~3× cost)')
    args = p.parse_args()

    # ── --backfill (2026-08-25) ────────────────────────────────────────────
    #   왜: li_mobility_score 를 저장 뒤에 계산하던 버그로 이 값이 한 번도 json 에
    #     안 들어갔다(cascade_v23_all.csv 에서 0/3615). 그 결과 combine_rankings 의
    #     이동도 30 % 가 전원 상수가 됐다. 입력 두 개는 저장돼 있으니 **재계산 없이**
    #     채울 수 있다. MD 를 접고 BVSE 로 간 결정이 그제서야 랭킹에 반영된다.
    #   ⛔ 못 하는 것: 순위를 다시 매기지 않는다. 그건 combine_rankings 의 일이고,
    #     결과가 바뀌는 일이라 사람이 판단할 사안이다.
    if args.backfill:
        src = Path(args.out)
        if not src.is_file():
            print(f"⛔ 없다: {src}")
            return 2
        d = json.loads(src.read_text())
        recs = d.get('records', [])
        filled = skipped = same = 0
        for r in recs:
            if 'migration_volume_fraction' not in r or 'bvs_li_proxy_score' not in r:
                skipped += 1
                continue
            v = 3 * r['migration_volume_fraction'] + r['bvs_li_proxy_score']
            if 'li_mobility_score' in r:
                same += abs(r['li_mobility_score'] - v) < 1e-9
                continue
            r['li_mobility_score'] = v
            filled += 1
        print(f"backfill: 채움 {filled} · 이미 있음 {same} · 입력 부족 {skipped} "
              f"/ 전체 {len(recs)}")
        if filled:
            bak = src.with_suffix(src.suffix + '.bak_backfill')
            if not bak.exists():
                bak.write_text(src.read_text())
                print(f"  · 원본 보존 → {bak.name}")
            d['_backfill'] = {'field': 'li_mobility_score',
                              'formula': '3*migration_volume_fraction + bvs_li_proxy_score',
                              'n_filled': filled,
                              'why': '저장 뒤 계산 버그로 누락됐던 값 (재계산 0)'}
            src.write_text(json.dumps(d, indent=2, default=str))
            print(f"  ✓ {src}")
        else:
            print("  · 채울 것이 없다 (전부 이미 있거나 입력이 없다)")
        return 0

    def winner_name(xyz_path):
        """NEW-D fix (v4.5.17): cascade outputs like
        04_anneal/{winner}/post_relax.xyz all share stem='post_relax',
        causing dict-key collision in collect_dataset. Use parent dir
        name in that case. Same pattern as combine_rankings.py CR-A
        (v4.5.8) — applied here too."""
        p = Path(xyz_path)
        if p.stem in ('post_relax', 'post_md'):
            return p.parent.name
        return p.stem

    paths = []
    explicit_xyz = bool(args.xyz)
    if args.xyz:
        paths.extend(Path(p) for p in args.xyz)
    if args.xyz_dir:
        paths.extend(sorted(Path(args.xyz_dir).rglob('*.xyz')))
    # NEW-A fix (v4.5.16): only auto-exclude intermediate files when scanning
    # by directory. Explicit --xyz list means the caller knows which files to
    # process — trust them. v4.5 CR-3 swap made BVSE primary input
    # `04_anneal/*/post_relax.xyz`, and this filter was excluding the very
    # files cascade explicitly passes. Resulted in `records: []` (silent fail).
    if not explicit_xyz:
        paths = [p for p in paths
                 if p.name not in ('post_md.xyz', 'post_relax.xyz')]
    print(f"Processing {len(paths)} structures")

    # Resume — load existing records if present
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if out.exists():
        try:
            prev = json.loads(out.read_text())
            for r in prev.get('records', []):
                if 'name' in r:
                    existing[r['name']] = r
            print(f"  Resume: {len(existing)} records already computed")
        except Exception:
            existing = {}

    records = list(existing.values())
    # NEW-D: use winner_name for resume + record naming (parent dir when
    # stem is 'post_relax'/'post_md').
    todo = [p for p in paths if winner_name(p) not in existing]
    print(f"  To compute: {len(todo)}/{len(paths)}")

    for i, xpath in enumerate(todo):
        wname = winner_name(xpath)
        try:
            atoms = read(str(xpath))
            bvs = compute_bvs_per_li(atoms)
            mig = compute_migration_volume(atoms,
                                          n_grid=args.grid_resolution)
            records.append({'name': wname, 'xyz': str(xpath),
                          **bvs, **mig})
        except Exception as e:
            records.append({'name': wname, 'error': str(e)})
        if (i + 1) % 50 == 0 or (i + 1) == len(todo):
            # Periodic save for crash resilience
            out.write_text(json.dumps({
                'provenance': get_provenance(),
                'n_records': len(records),
                'records': records,
            }, indent=2, default=str))
            print(f"  {i+1}/{len(todo)}")

    # ⛔⛔ 2026-08-25 — li_mobility_score 를 **저장한 뒤에** 계산하고 있었다.
    #   그래서 화면의 순위표에만 쓰이고 json 에는 한 번도 안 들어갔다:
    #     cascade_v23_all.csv 에서 migration_volume_fraction 681/3615 (있음)
    #                          li_mobility_score          **0/3615** (없음)
    #   그 빈 열을 combine_rankings.py 가 읽고, normalize() 가 "전부 결측이면 0.5" 로
    #   메워서 **score_combined 의 이동도 30 % 가 전원 동일한 상수**가 됐다.
    #   = MD 를 접고 BVSE 로 갈아탔는데, 그 BVSE 결과조차 랭킹에 안 들어가고 있었다.
    #   → 저장 **전에** 계산한다. (아래 순위표는 이 값을 그대로 다시 쓴다)
    for r in records:
        if 'bvs_li_proxy_score' in r and 'migration_volume_fraction' in r:
            r['li_mobility_score'] = (3 * r['migration_volume_fraction']
                                      + r['bvs_li_proxy_score'])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'provenance': get_provenance(),
        'n_records': len(records),
        'records': records,
    }, indent=2, default=str))

    # Rank by migration volume × proxy score (combined Li mobility metric)
    ok = [r for r in records if 'bvs_li_proxy_score' in r
          and 'migration_volume_fraction' in r]
    # (위에서 이미 계산·저장했다. 여기 남겨 둔 것은 옛 json 을 --resume 으로 이어받은
    #  경우를 위한 폴백이다 — 값이 이미 있으면 같은 값이므로 무해하다.)
    for r in ok:
        r.setdefault('li_mobility_score',
                     3 * r['migration_volume_fraction'] + r['bvs_li_proxy_score'])
    ok.sort(key=lambda r: -r['li_mobility_score'])
    print(f"\n{'Rank':<5}{'Name':<45}{'⟨BVS⟩':>8}{'σ BVS':>8}{'V_mig%':>9}"
          f"{'mob_score':>11}")
    for i, r in enumerate(ok[:20], 1):
        print(f"{i:<5}{r['name'][:43]:<45}"
              f"{r['bvs_li_mean']:>7.3f} "
              f"{r['bvs_li_std']:>7.3f} "
              f"{r['migration_volume_fraction']*100:>7.2f}% "
              f"{r['li_mobility_score']:>10.4f}")
    print(f"\n✓ {len(records)} BVS records → {out}")


if __name__ == '__main__':
    main()
