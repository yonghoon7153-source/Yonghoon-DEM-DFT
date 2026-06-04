#!/usr/bin/env python3
"""One-shot per-bond analysis: regenerate ALL bonds.json sections for a system.

Inputs (one directory + structure):
  - ICOHPLIST.lobster   (LOBSTER per-bond ICOHP, ext basis)
  - ACF.dat             (Bader basin charges, same atom order as the SCF input)
  - structure (cif/xyz)  (gives element order + bond lengths + site assignment)

Outputs a JSON with every modelc-parallel analysis:
  1. bader_charges (per element, q = Zval - basin)
  2. icohp_per_bond_type (P-S, Li-Cl, Li-S, S-S) + per-site splits (Li-S PS4/4d, Li-Cl 4a/4d)
  3. wilkening: per-bond |q_Li·q_X|/d vs ICOHP regression (r, slope)
  4. icohp_distance_correlation (slope dICOHP/dd per bond type)
  5. strongest_bonds top-5
  6. PS4 sum / formal charge

Usage:
  python3 analyze_per_bond_icohp.py \
    --lobster_dir <dir with ICOHPLIST.lobster> \
    --acf <ACF.dat> --struct <V0.cif> \
    --system comp1_v3 --out bonds_comp1_k444.json \
    [--zval Li:3,P:5,S:6,Cl:7] [--cl4a_cut 5] [--s4d_by_coord]
"""
import argparse
import json
import re
from collections import defaultdict
import numpy as np
from ase.io import read
from ase.neighborlist import neighbor_list


def parse_icohplist(path):
    """Return list of (i_idx, j_idx, label_i, label_j, dist, icohp). 1-based atom idx in file."""
    bonds = []
    for ln in open(path):
        p = ln.split()
        # format: COHP#  atomMU  atomNU  distance  tx ty tz  ICOHP
        if len(p) >= 8 and p[0].isdigit():
            li, lj = p[1], p[2]            # e.g. S5, Li23
            d = float(p[3]); ic = float(p[7])
            ii = int(re.sub(r'\D', '', li)) - 1
            jj = int(re.sub(r'\D', '', lj)) - 1
            ei = re.sub(r'\d+', '', li); ej = re.sub(r'\d+', '', lj)
            bonds.append((ii, jj, ei, ej, d, ic))
    return bonds


def assign_sites(atoms, cl4a_zli_cut=5):
    """Classify Cl as 4a (Z_Li>=cut) / 4d, and S as PS4 (bonded to P) / 4d (free)."""
    syms = atoms.get_chemical_symbols()
    # P-S bonds → PS4 sulfurs
    ii, jj = neighbor_list('ij', atoms, {('P', 'S'): 2.4})
    ps4_S = set()
    for a, b in zip(ii, jj):
        if syms[a] == 'S': ps4_S.add(a)
        if syms[b] == 'S': ps4_S.add(b)
    S_site = {i: ('PS4' if i in ps4_S else '4d') for i in range(len(atoms)) if syms[i] == 'S'}
    # Cl coordination by Li
    iC, jC = neighbor_list('ij', atoms, {('Cl', 'Li'): 3.4})
    zli = defaultdict(int)
    for a, b in zip(iC, jC):
        if syms[a] == 'Cl': zli[a] += 1
    Cl_site = {i: ('4a' if zli[i] >= cl4a_zli_cut else '4d')
               for i in range(len(atoms)) if syms[i] == 'Cl'}
    return S_site, Cl_site


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lobster_dir', required=True)
    ap.add_argument('--acf', required=True)
    ap.add_argument('--struct', required=True)
    ap.add_argument('--system', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--zval', default='Li:3,P:5,S:6,Cl:7')
    ap.add_argument('--cl4a_cut', type=int, default=5)
    args = ap.parse_args()

    zval = {k: int(v) for k, v in (x.split(':') for x in args.zval.split(','))}
    atoms = read(args.struct)
    syms = atoms.get_chemical_symbols()
    nat = len(atoms)

    # --- Bader ---
    basin = np.loadtxt(args.acf, skiprows=2, max_rows=nat, usecols=4)
    bader = {}
    by_el = defaultdict(list)
    for s, b in zip(syms, basin):
        by_el[s].append(b)
    for el, bs in by_el.items():
        bs = np.array(bs)
        bader[el] = {'q_e': round(zval[el] - bs.mean(), 4),
                     'std': round(bs.std(), 4), 'n': len(bs)}
    q_atom = {i: zval[syms[i]] - basin[i] for i in range(nat)}  # per-atom Bader charge

    # --- sites ---
    S_site, Cl_site = assign_sites(atoms, args.cl4a_cut)

    # --- ICOHP per bond ---
    bonds = parse_icohplist(f"{args.lobster_dir}/ICOHPLIST.lobster")
    bytype = defaultdict(list)         # 'P-S' -> [icohp,...]
    persite = defaultdict(list)        # 'Li-S(PS4)' -> [(d,icohp,wilk)]
    allbonds = []
    for ii, jj, ei, ej, d, ic in bonds:
        key = '-'.join(sorted([ei, ej]))
        bytype[key].append(ic)
        # per-site + wilkening (only metal-anion)
        site = None
        if {ei, ej} == {'Li', 'S'}:
            si = ii if ei == 'S' else jj
            site = f"Li-S({S_site.get(si, '?')})"
        elif {ei, ej} == {'Li', 'Cl'}:
            ci = ii if ei == 'Cl' else jj
            site = f"Li-Cl({Cl_site.get(ci, '?')})"
        if site:
            wilk = abs(q_atom[ii] * q_atom[jj]) / d
            persite[site].append((d, ic, wilk))
        allbonds.append({'atoms': f"{ei}{ii+1}-{ej}{jj+1}", 'pair': key,
                         'd_A': round(d, 3), 'icohp_eV': round(ic, 3)})

    icohp_type = {k: {'icohp_eV': round(np.mean(v), 4), 'n_bonds': len(v)}
                  for k, v in sorted(bytype.items())}

    # per-site mean + Wilkening regression + distance slope
    site_out = {}
    for site, rows in persite.items():
        d = np.array([r[0] for r in rows]); ic = np.array([r[1] for r in rows])
        wk = np.array([r[2] for r in rows])
        o = {'icohp_eV': round(ic.mean(), 4), 'std_eV': round(ic.std(), 4), 'n_bonds': len(rows)}
        if len(rows) >= 3:
            # ICOHP vs distance slope
            o['dist_slope_eV_per_A'] = round(np.polyfit(d, ic, 1)[0], 3)
            # Wilkening: ICOHP vs |q.q|/d
            if wk.std() > 1e-9:
                r = float(np.corrcoef(wk, ic)[0, 1])
                o['wilkening_r'] = round(r, 3)
                o['wilkening_slope'] = round(np.polyfit(wk, ic, 1)[0], 3)
        site_out[site] = o

    allbonds.sort(key=lambda x: x['icohp_eV'])
    top5 = allbonds[:5]

    # PS4 charge sum
    ps4_sum = sum(q_atom[i] for i in range(nat) if syms[i] in ('P', 'S'))
    # actually PS4 = P + bonded S; approximate as P + PS4-S
    ps4_q = sum(q_atom[i] for i in range(nat)
                if syms[i] == 'P' or (syms[i] == 'S' and S_site.get(i) == 'PS4'))

    out = {
        'system': args.system,
        '_provenance': 'k444 (paper-grade): LOBSTER ext-basis 70/560 + Bader AE plot_num=17, '
                       'one-shot via analyze_per_bond_icohp.py',
        'bader_charges': bader,
        'n_electrons_recovered': round(float(basin.sum()), 3),
        'PS4_sum_q_e': round(ps4_q, 3),
        'icohp_per_bond_type_eV': icohp_type,
        'icohp_per_site': site_out,
        'strongest_bonds_top5': top5,
        'site_counts': {
            'Cl_4a': sum(1 for v in Cl_site.values() if v == '4a'),
            'Cl_4d': sum(1 for v in Cl_site.values() if v == '4d'),
            'S_PS4': sum(1 for v in S_site.values() if v == 'PS4'),
            'S_4d': sum(1 for v in S_site.values() if v == '4d'),
        },
    }
    json.dump(out, open(args.out, 'w'), indent=2, ensure_ascii=False)
    print(f"=== {args.system} per-bond analysis (k444) ===")
    print(f"Bader: " + "  ".join(f"{el} {bader[el]['q_e']:+.3f}" for el in ['Li', 'P', 'S', 'Cl'] if el in bader))
    print(f"sites: {out['site_counts']}")
    print("ICOHP/bond:")
    for k, v in icohp_type.items():
        print(f"  {k:8s} {v['icohp_eV']:+.4f} (n={v['n_bonds']})")
    print("per-site:")
    for k, v in site_out.items():
        extra = f" r={v.get('wilkening_r')}" if 'wilkening_r' in v else ""
        print(f"  {k:14s} {v['icohp_eV']:+.4f} ±{v['std_eV']:.3f} (n={v['n_bonds']}){extra}")
    print(f"top bond: {top5[0]['atoms']} {top5[0]['icohp_eV']} eV")
    print(f"→ {args.out}")


if __name__ == '__main__':
    main()
