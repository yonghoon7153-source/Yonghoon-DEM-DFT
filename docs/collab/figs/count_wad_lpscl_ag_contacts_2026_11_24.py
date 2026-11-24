"""count_wad_lpscl_ag_contacts_2026_11_24.py — contact / outer-layer counts for the LPSCl pair figures and report text.

  python3 docs/collab/figs/count_wad_lpscl_ag_contacts_2026_11_24.py <out.json>
      LPSCl|Ag(111) (P1) per termination x registry: SE atoms touching Ag (S<=2.9 · Li/Cl<=3.0 · P<=3.2 A, minimum image),
      S split into S_PS4 (a P within 2.5 A) / S_free · z gap (lowest Ag - highest SE). Source of
      db/properties/wad_lpscl_ag_termination_contacts_2026_11_24.csv.
  python3 docs/collab/figs/count_wad_lpscl_ag_contacts_2026_11_24.py --outer_csv <out.csv>
      P1 (Ag) and P2 (graphite) per termination x registry: composition of the SE outer layer (SE atoms within
      1.0 A of the highest SE atom) · z gap (lowest substrate atom - highest SE atom). Source of
      db/properties/wad_lpscl_termination_outer_layer_2026_11_24.csv (2026-11-24 · report section 2-4).

What this tool cannot do: it reads UMA+D3 relaxed geometry only — no energies, no bonding analysis; the z gap is a
height difference between planes of atoms, not an interatomic distance.
"""
import argparse
import csv
import json

import numpy as np
from ase.geometry import get_distances
from ase.io import read

D = 'db/raw/wad_se_pairs_uma_2026_10_01/relax'
SRC = 'db/raw/wad_se_pairs_uma_2026_10_01/relax/<pair>_<term>/<reg>/relaxed.extxyz (UMA+D3 relaxed)'
OUTER_WIN = 1.0


def s_in_ps4(a, sym):
    P = np.where(sym == 'P')[0]; S = np.where(sym == 'S')[0]
    _, dsp = get_distances(a.positions[S], a.positions[P], cell=a.cell, pbc=a.pbc)
    return {int(S[i]): bool((dsp[i] < 2.5).any()) for i in range(len(S))}


def contacts():
    out = {}
    for term in ('s_outer', 'li_outer'):
        for reg in ('A', 'B'):
            a = read(f'{D}/P1_{term}/{reg}/relaxed.extxyz')
            sym = np.array(a.get_chemical_symbols()); z = a.positions[:, 2]
            ag = np.where(sym == 'Ag')[0]; se = np.where(sym != 'Ag')[0]
            ag_low = z[ag].min(); se_top = z[se].max()
            above = z[ag].mean() > z[se].mean()
            _, dm = get_distances(a.positions[se], a.positions[ag], cell=a.cell, pbc=a.pbc)
            dmin = dm.min(axis=1)
            inps4 = s_in_ps4(a, sym)
            area = float(np.linalg.norm(np.cross(a.cell[0], a.cell[1])))
            cnt = {}
            for k, i in enumerate(se):
                el = sym[i]; d = dmin[k]
                cut = {'S': 2.9, 'Li': 3.0, 'Cl': 3.0, 'P': 3.2}[el]
                if d <= cut:
                    key = el if el != 'S' else ('S_PS4' if inps4[int(i)] else 'S_free')
                    cnt[key] = cnt.get(key, 0) + 1
            out[f'{term}_{reg}'] = {'n_atoms': len(a), 'ag_above': bool(above), 'area_A2': round(area, 2), 'contacts': cnt,
                                    'gap_A': round(float(ag_low - se_top) if above else float(z[se].min() - z[ag].max()), 3)}
    return out


def outer_rows():
    rows = []
    for pair, sub, name in (('P1', 'Ag', 'LPSCl|Ag(111)'), ('P2', 'C', 'LPSCl|graphite (3 layers)')):
        for term, tname in (('s_outer', 'S-outer'), ('li_outer', 'Li-PS4-outer')):
            for reg in ('A', 'B'):
                a = read(f'{D}/{pair}_{term}/{reg}/relaxed.extxyz')
                sym = np.array(a.get_chemical_symbols()); z = a.positions[:, 2]
                sb = np.where(sym == sub)[0]; se = np.where(sym != sub)[0]
                assert z[sb].mean() > z[se].mean(), f'{pair}_{term}/{reg}: substrate is not above the SE'
                top = z[se].max()
                outer = [i for i in se if z[i] > top - OUTER_WIN]
                inps4 = s_in_ps4(a, sym)
                c = {'S_free': 0, 'S_PS4': 0, 'Li': 0, 'Cl': 0, 'P': 0}
                for i in outer:
                    el = sym[i]
                    c[el if el != 'S' else ('S_PS4' if inps4[int(i)] else 'S_free')] += 1
                rows.append({'pair': name, 'substrate': sub, 'termination': tname, 'registry': reg, 'n_atoms': len(a),
                             'area_A2': round(float(np.linalg.norm(np.cross(a.cell[0], a.cell[1]))), 2),
                             'outer_S_free': c['S_free'], 'outer_S_PS4': c['S_PS4'], 'outer_Li': c['Li'],
                             'outer_Cl': c['Cl'], 'outer_P': c['P'], 'outer_window_A': OUTER_WIN,
                             'z_gap_substrate_to_SE_A': round(float(z[sb].min() - top), 3),
                             'definition': 'outer = SE atoms within 1.0 A of the highest SE atom · S_PS4 = S with a P within 2.5 A · '
                                           'z gap = lowest substrate atom z - highest SE atom z',
                             'source': SRC})
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('json_out', nargs='?')
    ap.add_argument('--outer_csv')
    args = ap.parse_args()
    if args.json_out:
        out = contacts(); print(json.dumps(out, indent=1)); json.dump(out, open(args.json_out, 'w'), indent=1)
    if args.outer_csv:
        rows = outer_rows()
        with open(args.outer_csv, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
        for r in rows:
            print(r['pair'], r['termination'], r['registry'], r['outer_S_free'], r['outer_S_PS4'], r['outer_Li'], r['outer_Cl'], r['z_gap_substrate_to_SE_A'])
    if not (args.json_out or args.outer_csv):
        ap.error('give <out.json> and/or --outer_csv <out.csv>')
