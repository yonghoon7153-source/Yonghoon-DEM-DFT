"""
Case-by-case triage — find cases with suspicious/corrupted analysis output.

For each case, run 7 sanity checks. Flags cases needing attention.

Checks:
  1. porosity > 25%  (insufficient compaction; expected 13-20% at 300 MPa)
  2. porosity < 10%  (over-compaction; physically unrealistic)
  3. z-histogram uniform  (pile variation < 1.3× → not compacted)
  4. φ_SE mismatch with composition  (stored vs computed from atom count × radius³)
  5. τ_Dij < 1.0 or > 10  (out of physical bounds)
  6. σ_ionic missing but percolation > 50%  (network solver didn't run)
  7. σ_Lap_eff > 5× Bruggeman prediction  (anomalous scaling)

Output:
  - Summary table sorted by flag count (worst first)
  - /tmp/triage_report.csv with per-case flag columns

Usage:
  python3 scripts/triage_cases.py

Then for each flagged case:
  - Delete via webapp UI
  - Re-upload LIGGGHTS dump from cluster
  - Re-analyze
"""
from __future__ import annotations
import os, json, csv, math
from collections import defaultdict

import numpy as np
import pandas as pd


SIGMA_GRAIN_MS = 3.0  # LPSCl bulk conductivity


def _find_meta(cid: str) -> dict:
    for base in ('webapp/uploads', 'webapp/results'):
        p = f'{base}/{cid}/meta.json'
        if os.path.exists(p):
            try:
                return json.load(open(p))
            except Exception:
                pass
    return {}


def check_case(case_dir: str) -> dict | None:
    fm_path = f'{case_dir}/full_metrics.json'
    if not os.path.exists(fm_path):
        return None
    try:
        m = json.load(open(fm_path))
    except Exception:
        return None
    cid = os.path.basename(case_dir)
    meta = _find_meta(cid)
    name = meta.get('name', cid)

    flags = []

    # ─── 1. Porosity too high → not compacted ─────────────────────
    porosity = m.get('porosity')
    if porosity is not None and porosity > 25:
        flags.append(f'porosity_high ({porosity:.0f}%)')
    elif porosity is not None and porosity < 10:
        flags.append(f'porosity_low ({porosity:.0f}%)')

    # ─── 2/3. z-histogram uniformity (from atoms.csv) ────────────
    atoms_path = f'{case_dir}/atoms.csv'
    pile_ratio = None
    if os.path.exists(atoms_path):
        try:
            df = pd.read_csv(atoms_path, usecols=['z', 'type', 'radius'])
            h, _ = np.histogram(df.z, bins=10)
            # Compare edge bins to middle bins
            pile_top = max(h[:3]) / max(min(h[3:7]), 1)
            pile_bot = max(h[-3:]) / max(min(h[3:7]), 1)
            pile_ratio = max(pile_top, pile_bot)
            if pile_ratio < 1.3:
                flags.append(f'z_uniform (pile={pile_ratio:.2f}, not compacted)')
        except Exception:
            pass

    # ─── 4. φ_SE vs atom-count expectation ────────────────────────
    phi_stored = m.get('phi_se')
    phi_from_atoms = None
    if os.path.exists(atoms_path):
        try:
            df = pd.read_csv(atoms_path, usecols=['type', 'radius'])
            # SE = highest type number typically
            tm_str = meta.get('type_map', '')
            se_type = None
            for pair in tm_str.split(','):
                if ':' in pair:
                    k, v = pair.split(':', 1)
                    if v.strip() == 'SE':
                        se_type = int(k.strip())
                        break
            if se_type is not None:
                se_mask = df['type'] == se_type
                am_mask = ~se_mask
                se_vol = ((4/3) * math.pi * (df.loc[se_mask, 'radius']**3)).sum()
                am_vol = ((4/3) * math.pi * (df.loc[am_mask, 'radius']**3)).sum()
                # Expected φ_SE at target porosity 14%
                if (se_vol + am_vol) > 0:
                    phi_from_atoms = 0.86 * (se_vol / (se_vol + am_vol))
                    # Also compute from stored porosity for consistency check
                    if porosity is not None:
                        phi_from_poro = (1 - porosity/100) * (se_vol / (se_vol + am_vol))
                        if phi_stored and abs(phi_stored - phi_from_poro)/max(phi_stored, 0.01) > 0.15:
                            flags.append(f'phi_inconsistent ({phi_stored:.3f}≠{phi_from_poro:.3f})')
        except Exception:
            pass

    # ─── 5. τ_Dij bounds ──────────────────────────────────────────
    tau = m.get('tortuosity_mean')
    if tau is not None:
        if tau < 1.0:
            flags.append(f'tau_lt1 ({tau:.2f})')
        elif tau > 10:
            flags.append(f'tau_huge ({tau:.1f})')

    # ─── 6. σ missing despite percolation ────────────────────────
    perc = m.get('percolation_pct', 0)
    sig = m.get('sigma_full_mScm')
    if perc > 50 and sig is None:
        flags.append('sigma_None_despite_perc')

    # ─── 7. σ vs Bruggeman sanity ────────────────────────────────
    if phi_stored and sig:
        sig_brug = phi_stored**1.5 * SIGMA_GRAIN_MS  # naive Bruggeman upper bound
        if sig > 1.5 * sig_brug:
            flags.append(f'sigma>1.5×Brug ({sig/sig_brug:.1f}×)')

    return {
        'case_id':    cid,
        'name':       name,
        'path':       case_dir,
        'porosity':   round(porosity or 0, 1),
        'phi_SE':     round(phi_stored or 0, 3),
        'phi_atoms_14poro': round(phi_from_atoms or 0, 3) if phi_from_atoms else None,
        'tau_Dij':    round(tau or 0, 2) if tau else None,
        'sigma_mScm': round(sig, 4) if sig else None,
        'perc_pct':   round(perc, 1),
        'z_pile':     round(pile_ratio, 2) if pile_ratio else None,
        'n_flags':    len(flags),
        'flags':      ';'.join(flags) if flags else 'OK',
    }


def main():
    rows = []
    for root, _, files in os.walk('webapp'):
        if 'full_metrics.json' in files:
            rec = check_case(root)
            if rec:
                rows.append(rec)

    # Sort worst first
    rows.sort(key=lambda r: (-r['n_flags'], r['name']))
    flagged = [r for r in rows if r['n_flags'] > 0]

    print(f'\n=== TRIAGE REPORT — {len(rows)} cases scanned ===')
    print(f'  Clean  (0 flags): {len(rows) - len(flagged)}')
    print(f'  Flagged          : {len(flagged)}\n')

    if flagged:
        print(f'{"name":30s} {"poro":>5s} {"φ_SE":>5s} {"τ":>4s} {"σ":>8s} '
              f'{"pile":>4s} {"flags"}')
        print('-' * 120)
        for r in flagged:
            print(f'  {r["name"][:28]:30s} '
                  f'{r["porosity"]:>5.0f} '
                  f'{r["phi_SE"]:>5.2f} '
                  f'{(r["tau_Dij"] or 0):>4.1f} '
                  f'{(r["sigma_mScm"] or 0):>8.4f} '
                  f'{(r["z_pile"] or 0):>4.1f}  '
                  f'{r["flags"]}')

    print(f'\n=== CLEAN ({len(rows) - len(flagged)}) ===')
    for r in rows:
        if r['n_flags'] == 0:
            print(f'  ✓ {r["name"][:30]:32s} poro={r["porosity"]:>5.1f}%  '
                  f'φ_SE={r["phi_SE"]:.3f}  τ={r["tau_Dij"]:.2f}  '
                  f'σ={r["sigma_mScm"] or 0:.4f}')

    # CSV dump
    if rows:
        keys = list(rows[0].keys())
        with open('/tmp/triage_report.csv', 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
            w.writeheader()
            w.writerows(rows)
        print(f'\nWrote /tmp/triage_report.csv ({len(rows)} rows)')

    # Breakdown by flag type
    if flagged:
        print(f'\n=== FLAG FREQUENCY ===')
        flag_counts = defaultdict(int)
        for r in flagged:
            for f in r['flags'].split(';'):
                tag = f.split(' ')[0]
                flag_counts[tag] += 1
        for tag, c in sorted(flag_counts.items(), key=lambda x: -x[1]):
            print(f'  {tag:25s} {c}')


if __name__ == '__main__':
    main()
