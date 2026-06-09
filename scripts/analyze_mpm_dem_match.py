#!/usr/bin/env python3
"""Post-process docs/data/mpm_dem_match.csv (the DEM↔MPM wallP@512 cross-validation).

Reads the matcher CSV (no re-run) and prints, as paste-able text tables:
  • per-r_SE-band parity (meanΔ bias, mean|Δ|, Pearson),
  • force-chain outlier ID  — big-AM/small-SE (rSE≤0.5, high AM_wt) where the MPM
    continuum bears the wall load through rigid-AM force chains at high porosity
    while DEM rearranges (the quantified continuum limit, frame [4]),
  • rSE≤0.5 parity with those outliers removed (does the bulk tighten?),
  • Furnas dip   — porosity vs AM_wt, DEM | MPM medians (does the dip co-locate?),
  • size-crossover — porosity vs r_SE at fixed composition (does the ordering match?).

Frame [4]: agreement = cross-validation evidence; divergence = quantified
continuum limit.  This script does NOT tune anything — it only partitions the
already-computed parity so the single misleading 1:1 R² (dominated by the
force-chain corner) is decomposed into where the models agree vs diverge.
"""
import csv
import sys

import numpy as np

CSV = sys.argv[1] if len(sys.argv) > 1 else 'docs/data/mpm_dem_match.csv'
FC_THRESH = float(sys.argv[2]) if len(sys.argv) > 2 else 15.0   # MPM−DEM %p = force-chain flag

rows = []
with open(CSV) as fh:
    for d in csv.DictReader(fh):
        try:
            rows.append(dict(name=d['name'], dem=float(d['dem_porosity']),
                             mpm=float(d['mpm_porosity']), std=float(d.get('mpm_std', 0) or 0),
                             rse=float(d['r_SE']), amwt=float(d['AM_wt']),
                             ese=float(d.get('e_se_gpa', 0) or 0)))
        except (ValueError, KeyError):
            continue
rows = [r for r in rows if np.isfinite(r['mpm'])]
print(f"loaded {len(rows)} finite cases from {CSV}")
if not rows:
    sys.exit("no usable rows")

dem = np.array([r['dem'] for r in rows]); mpm = np.array([r['mpm'] for r in rows])
rse = np.array([r['rse'] for r in rows]); amwt = np.array([r['amwt'] for r in rows])


def parity(mask, lab):
    if mask.sum() < 1:
        return
    d, p = dem[mask], mpm[mask]
    pe = np.corrcoef(d, p)[0, 1] if mask.sum() >= 2 else float('nan')
    print(f"  {lab:22s} n={mask.sum():3d}  meanΔ={np.mean(p - d):+5.1f}  "
          f"mean|Δ|={np.mean(np.abs(p - d)):4.1f}  Pearson={pe:+.3f}")


print("\n── per-r_SE band parity ──")
for lo, hi, lab in [(0, 0.75, 'rSE≤0.5'), (0.75, 1.25, 'rSE≈1.0'), (1.25, 9.9, 'rSE≥1.5')]:
    parity((rse >= lo) & (rse < hi), lab)

print(f"\n── force-chain outliers (rSE≤0.5, MPM−DEM > {FC_THRESH:.0f}%p) ──")
fc = (rse <= 0.5) & (mpm - dem > FC_THRESH)
for r in sorted([r for r in rows if r['rse'] <= 0.5 and r['mpm'] - r['dem'] > FC_THRESH],
                key=lambda r: r['dem'] - r['mpm']):
    print(f"  {r['name'][:30]:30s} rSE={r['rse']:.2f} AMwt={r['amwt']:3.0f} "
          f"DEM={r['dem']:5.1f} MPM={r['mpm']:5.1f} Δ={r['mpm'] - r['dem']:+5.1f}")
print(f"  → {fc.sum()} force-chain cases (of {(rse <= 0.5).sum()} rSE≤0.5)")
parity((rse <= 0.5) & ~fc, 'rSE≤0.5 minus FC')

print("\n── Furnas dip: porosity vs AM_wt (rSE≤0.5), DEM | MPM medians ──")
band = rse <= 0.5
for lo, hi in [(0, 65), (65, 72), (72, 78), (78, 83), (83, 88), (88, 95), (95, 101)]:
    m = band & (amwt >= lo) & (amwt < hi)
    if m.sum() == 0:
        continue
    print(f"  AM {lo:3d}-{hi:3d}  n={m.sum():3d}  DEM={np.median(dem[m]):5.1f}  "
          f"MPM={np.median(mpm[m]):5.1f}")

print("\n── size-crossover: porosity vs r_SE (AM 78-86), DEM | MPM medians ──")
m0 = (amwt >= 78) & (amwt < 86)
for lo, hi, lab in [(0, 0.75, 'rSE≤0.5'), (0.75, 1.25, 'rSE≈1.0'), (1.25, 9.9, 'rSE≥1.5')]:
    m = m0 & (rse >= lo) & (rse < hi)
    if m.sum() == 0:
        continue
    print(f"  {lab:9s} n={m.sum():3d}  DEM={np.median(dem[m]):5.1f}  MPM={np.median(mpm[m]):5.1f}")
