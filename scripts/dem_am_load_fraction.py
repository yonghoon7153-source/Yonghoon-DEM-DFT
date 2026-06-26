#!/usr/bin/env python3
"""DEM AM-AM axial load fraction f_AM (Love-Weber) → MPM wallP conditional (--am-load-frac).

f_AM = σ_zz^(AM-AM contacts) / σ_zz^(all contacts) = the fraction of the axial (compression-z)
load carried by the RIGID AM-AM contact network (Love-Weber granular stress, σ_ij = Σ f_i·l_j).

WHY this and not the per-atom von-Mises partition: a per-atom stress (von Mises or σ_zz) counts an
AM particle's stress from ALL its contacts, and a stiff dispersed AM stress-concentrates (Eshelby)
even when it carries NO axial skeleton load → the per-atom f_AM is > 0 in SE-rich (WRONG, would
over-fire the wallP conditional and harm the SE-rich regime where the MPM is already correct).
The AM-AM *contact-network* σ_zz is ~0 when AM does not percolate (few/no AM-AM contacts) and large
when AM forms force chains (mono-large) → it AUTO-GATES: f_AM≈0 for SE-rich, large for the SE-poor
mono-large corner.  Feed to `mpm3d_compaction.py --am-load-frac f_AM` so the SE servo bears only its
(1−f_AM) share (Tabor-style wallP conditional, docs/mpm_wallP_conditional_troubleshooting.md).

The σ_zz ratio is scale/volume-free: per contact, F·l_z²/|l| with Hertz F=(4/3)E*√R*·δ^1.5; the
relative pair-type stiffness E* (AM-AM ≫ SE-SE/AM-SE because E_AM=140 ≫ E_SE,eff=1.35 GPa) is what
weights the AM-AM force chains.  Uses the DEM-effective E_SE=1.35 (the softened modulus the scaffold
was equilibrated at), AM=140 GPa.

  python3 scripts/dem_am_load_fraction.py --am am_scaffold.csv --se se_scaffold.csv
  python3 scripts/dem_am_load_fraction.py --atoms results/<case>/atoms.csv --type-map "1:AM_P,2:SE"
"""
import argparse
import math
import numpy as np

try:
    from scipy.spatial import cKDTree
except ImportError:
    raise SystemExit("dem_am_load_fraction needs scipy (cKDTree)")

E_AM = 140.0     # GPa (NCM)
E_SE = 1.35      # GPa (DEM EFFECTIVE / softened — the scaffold's equilibrium modulus)
NU = 0.30


def _estar(Ea, Eb, nu=NU):
    return 1.0 / ((1.0 - nu * nu) / Ea + (1.0 - nu * nu) / Eb)


def _read_csv(path):
    """type,x,y,z,r rows (scaffold or atoms; '#'-comment + optional header tolerated)."""
    T, X, R = [], [], []
    import csv as _csv
    with open(path) as f:
        rd = _csv.reader(f)
        for row in rd:
            if not row or row[0].lstrip().startswith('#'):
                continue
            try:
                t = int(float(row[0])); x = float(row[1]); y = float(row[2]); z = float(row[3]); r = float(row[4])
            except (ValueError, IndexError):
                continue
            T.append(t); X.append((x, y, z)); R.append(r)
    return np.array(T), np.array(X, dtype=float), np.array(R, dtype=float)


def _read_atoms(path, type_map):
    """webapp atoms.csv (id,type,x,y,z,radius); SE = labels containing 'SE' in type_map, else AM."""
    import csv as _csv
    se_types = {int(tok.split(':')[0]) for tok in type_map.split(',')
                if ':' in tok and 'SE' in tok.split(':', 1)[1].upper()} or {3}
    T, X, R, isSE = [], [], [], []
    with open(path) as f:
        rd = _csv.DictReader(f)
        cols = {c.lower(): c for c in rd.fieldnames}
        tk, xk, yk, zk = cols['type'], cols['x'], cols['y'], cols['z']
        rk = cols.get('radius') or cols.get('r')
        for row in rd:
            t = int(float(row[tk]))
            T.append(t); X.append((float(row[xk]), float(row[yk]), float(row[zk]))); R.append(float(row[rk]))
            isSE.append(t in se_types)
    return np.array(T), np.array(X, dtype=float), np.array(R, dtype=float), np.array(isSE, dtype=bool)


def _sigzz_pairs(Xi, Ri, Xj, Rj, Estar, same):
    """Σ over overlapping (i,j) of F·l_z²/|l|, F = (4/3)·Estar·√R*·δ^1.5.  same=True → within one set."""
    if len(Xi) == 0 or len(Xj) == 0:
        return 0.0, 0
    rmax_i, rmax_j = Ri.max(), Rj.max()
    if same:
        pairs = cKDTree(Xi).query_pairs(r=rmax_i + rmax_j, output_type='ndarray')
        if len(pairs) == 0:
            return 0.0, 0
        ii, jj = pairs[:, 0], pairs[:, 1]
        Xa, Ra, Xb, Rb = Xi[ii], Ri[ii], Xi[jj], Ri[jj]
    else:
        ta, tb = cKDTree(Xi), cKDTree(Xj)
        lol = ta.query_ball_tree(tb, r=rmax_i + rmax_j)
        ii = np.array([a for a, lst in enumerate(lol) for _ in lst], dtype=int)
        jj = np.array([b for lst in lol for b in lst], dtype=int)
        if len(ii) == 0:
            return 0.0, 0
        Xa, Ra, Xb, Rb = Xi[ii], Ri[ii], Xj[jj], Rj[jj]
    d = Xb - Xa
    dist = np.sqrt((d * d).sum(axis=1))
    delta = (Ra + Rb) - dist                                  # overlap (>0 = contact)
    m = (delta > 0) & (dist > 1e-12)
    if not m.any():
        return 0.0, int(m.sum())
    delta, dist = delta[m], dist[m]
    lz = d[m][:, 2]
    Rstar = (Ra[m] * Rb[m]) / (Ra[m] + Rb[m])
    F = (4.0 / 3.0) * Estar * np.sqrt(Rstar) * np.power(delta, 1.5)   # Hertz normal force (rel. scale)
    return float(np.sum(F * lz * lz / dist)), int(m.sum())


def am_load_fraction(T, X, R, isSE):
    am = ~isSE
    Xam, Ram, Xse, Rse = X[am], R[am], X[isSE], R[isSE]
    s_aa, n_aa = _sigzz_pairs(Xam, Ram, Xam, Ram, _estar(E_AM, E_AM), same=True)
    s_ss, n_ss = _sigzz_pairs(Xse, Rse, Xse, Rse, _estar(E_SE, E_SE), same=True)
    s_as, n_as = _sigzz_pairs(Xam, Ram, Xse, Rse, _estar(E_AM, E_SE), same=False)
    tot = s_aa + s_ss + s_as
    f_am = (s_aa / tot) if tot > 0 else 0.0
    return {
        'f_AM': round(f_am, 4),
        'sigzz_AM_AM': s_aa, 'sigzz_SE_SE': s_ss, 'sigzz_AM_SE': s_as,
        'n_AM': int(am.sum()), 'n_SE': int(isSE.sum()),
        'n_contacts_AM_AM': n_aa, 'n_contacts_AM_SE': n_as, 'n_contacts_SE_SE': n_ss,
        'SE_target_GPa_at_300': round(0.30 * (1.0 - f_am), 4),
    }


def am_load_fraction_peratom(atoms_path, type_map):
    """ACTUAL-FORCE cross-check: f_AM from the LIGGGHTS per-atom virial σ_zz (the SAME hooke/hysteresis
    stress the dashboard von Mises uses — NOT a Hertz reconstruction).  f_AM_peratom = Σ_AM V_p·σzz_p /
    Σ_all V_p·σzz_p (V_p = atom volume).  This is the AM-PHASE axial-stress share (incl. the AM-SE part on
    AM atoms), so it BRACKETS the Hertz AM-AM-only value from above (AM-AM-only ≤ true ≤ AM-phase-share):
    the frozen-AM MPM misses the AM-AM skeleton load for sure, and partly the AM-SE load it absorbs.
    Needs atoms.csv with sigma_xx/yy/zz (LIGGGHTS compute stress/atom; present where the dashboard shows
    von-Mises ratios)."""
    import csv as _csv
    se_types = {int(t.split(':')[0]) for t in type_map.split(',') if ':' in t and 'SE' in t.split(':', 1)[1].upper()} or {3}
    num = 0.0; den = 0.0; n_am = 0; n_se = 0; have = False
    with open(atoms_path) as f:
        rd = _csv.DictReader(f); cols = {c.lower(): c for c in rd.fieldnames}
        tk = cols['type']; rk = cols.get('radius') or cols.get('r'); zzk = cols.get('sigma_zz')
        if zzk is None:
            return None
        have = True
        for row in rd:
            t = int(float(row[tk])); r = float(row[rk]); szz = float(row[zzk])
            v = r * r * r                                   # ∝ atom volume (4/3π cancels in ratio)
            contrib = v * szz
            den += contrib
            if t in se_types: n_se += 1
            else: n_am += 1; num += contrib
    if not have or den == 0:
        return None
    return {'f_AM_peratom': round(num / den, 4), 'n_AM': n_am, 'n_SE': n_se}


def am_load_fraction_liggghts(atom_dump, contact_dump=None):
    """★ ACTUAL-force f_AM from LIGGGHTS dumps (hooke/hysteresis, NOT Hertz reconstruction).
    atom_dump: 'ITEM: ATOMS id type ... c_strs[1] c_strs[2] c_strs[3] ...' (compute stress/atom; the
      dashboard von-Mises basis).  Robust by COLUMN NAME.  → per-atom AM-PHASE σ_zz virial share.
    contact_dump (optional): 'ITEM: ENTRIES c_cpl[...]' from `compute pair/gran/local pos id force ...`.
      → per-contact AM-AM-only Love-Weber f_AM with the REAL contact force.  ⚠ column layout is
      INPUT-SPECIFIC (positional); the indices below match input_real_14.liggghts
      (pos[1-6] id[7-8] force[9-11]→fz=c_cpl[11]; verified: Σ f_z·l_z == atom-virial total).  Other
      inputs may differ → cross-check Σ(f·l) vs atom virial; if mismatched, the force column moved.
    real_14 result: Hertz(AM-AM) 0.847 OVER-estimates the actual AM-AM 0.670 (per-atom AM-phase 0.809)."""
    al = open(atom_dump).readlines()
    hi = next(k for k, l in enumerate(al) if l.startswith('ITEM: ATOMS'))
    cols = al[hi].split()[2:]
    ci = {c: i for i, c in enumerate(cols)}
    idk, tk = ci['id'], ci['type']
    zzk = ci.get('c_strs[3]')
    id2type = {}; sAM = 0.0; sSE = 0.0
    for l in al[hi + 1:]:
        p = l.split()
        if len(p) < len(cols): continue
        aid = int(float(p[idk])); t = int(float(p[tk])); id2type[aid] = t
        if zzk is not None:
            szz = float(p[zzk]); (globals(), sSE)  # noqa
            if t == 3: sSE += szz
            else: sAM += szz
    out = {'f_AM_peratom_AMphase': round(sAM / (sAM + sSE), 4) if (sAM + sSE) else None}
    if contact_dump:
        cl = open(contact_dump).readlines()
        ej = next(k for k, l in enumerate(cl) if l.startswith('ITEM: ENTRIES'))
        saa = sas = sss = 0.0; naa = nas = nss = 0
        for l in cl[ej + 1:]:
            p = l.split()
            if len(p) < 26: continue
            try:
                z1 = float(p[2]); z2 = float(p[5]); fz = float(p[11])      # real_14 layout (verified)
                i1 = int(float(p[6])); i2 = int(float(p[7]))
            except ValueError:
                continue
            c = fz * (z2 - z1); t1 = id2type.get(i1); t2 = id2type.get(i2)
            if t1 is None or t2 is None: continue
            if t1 != 3 and t2 != 3: saa += c; naa += 1
            elif t1 == 3 and t2 == 3: sss += c; nss += 1
            else: sas += c; nas += 1
        tc = saa + sas + sss
        out.update({'f_AM_contact_AMAM': round(saa / tc, 4) if tc else None,
                    'contact_sigzz_total': round(tc, 3), 'atom_virial_total': round(sAM + sSE, 3),
                    'n_AM_AM': naa, 'n_AM_SE': nas, 'n_SE_SE': nss})
    return out


def main():
    ap = argparse.ArgumentParser(description="DEM AM-AM axial load fraction f_AM (Love-Weber) for --am-load-frac")
    ap.add_argument('--am', help='am_scaffold.csv (type,x,y,z,r)')
    ap.add_argument('--se', help='se_scaffold.csv (type,x,y,z,r)')
    ap.add_argument('--atoms', help='webapp atoms.csv (id,type,x,y,z,radius) — use with --type-map')
    ap.add_argument('--type-map', default='1:AM_P,2:AM_S,3:SE', help='for --atoms: e.g. "1:AM_P,2:SE"')
    ap.add_argument('--atoms-sigzz', help='ACTUAL-FORCE cross-check: atoms.csv WITH per-atom sigma_zz '
                    '(LIGGGHTS virial, the dashboard von-Mises basis) → f_AM from real hooke/hysteresis '
                    'forces, no Hertz reconstruction.  Reports the AM-phase axial-stress share (brackets '
                    'the Hertz AM-AM-only from above).  use with --type-map')
    a = ap.parse_args()
    if a.atoms_sigzz:
        pa = am_load_fraction_peratom(a.atoms_sigzz, a.type_map)
        if pa is None:
            print("  [atoms-sigzz] no sigma_zz column in atoms.csv (LIGGGHTS compute stress/atom not dumped)")
        else:
            print(f"f_AM_peratom = {pa['f_AM_peratom']:.3f}   (ACTUAL hooke virial σ_zz, AM-phase share; "
                  f"n_AM {pa['n_AM']}, n_SE {pa['n_SE']})")
            print("  vs Hertz AM-AM-only (--am/--se) → the two BRACKET the true f_AM (AM-AM-only ≤ true ≤ AM-phase-share)")
        if not (a.am or a.atoms):
            return pa
    if a.atoms:
        T, X, R, isSE = _read_atoms(a.atoms, a.type_map)
    elif a.am and a.se:
        Ta, Xa, Ra = _read_csv(a.am); Ts, Xs, Rs = _read_csv(a.se)
        T = np.concatenate([Ta, Ts]); X = np.vstack([Xa, Xs]); R = np.concatenate([Ra, Rs])
        isSE = np.concatenate([np.zeros(len(Ta), bool), np.ones(len(Ts), bool)])
    else:
        raise SystemExit("give --atoms (+--type-map) OR --am and --se")
    res = am_load_fraction(T, X, R, isSE)
    print(f"f_AM = {res['f_AM']:.3f}   (AM-AM load share of axial σ_zz)")
    print(f"  → --am-load-frac {res['f_AM']:.3f}   (SE_target @300MPa = {res['SE_target_GPa_at_300']*1000:.0f} MPa)")
    print(f"  σ_zz  AM-AM {res['sigzz_AM_AM']:.4g} / AM-SE {res['sigzz_AM_SE']:.4g} / SE-SE {res['sigzz_SE_SE']:.4g}")
    print(f"  contacts  AM-AM {res['n_contacts_AM_AM']} / AM-SE {res['n_contacts_AM_SE']} / SE-SE {res['n_contacts_SE_SE']}"
          f"   (n_AM {res['n_AM']}, n_SE {res['n_SE']})")
    print(f"  GATE check: f_AM→0 means AM dispersed (SE-rich, conditional auto-OFF); large means AM percolates")
    return res


if __name__ == '__main__':
    main()
