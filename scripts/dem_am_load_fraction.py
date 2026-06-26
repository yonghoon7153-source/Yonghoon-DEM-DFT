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


def main():
    ap = argparse.ArgumentParser(description="DEM AM-AM axial load fraction f_AM (Love-Weber) for --am-load-frac")
    ap.add_argument('--am', help='am_scaffold.csv (type,x,y,z,r)')
    ap.add_argument('--se', help='se_scaffold.csv (type,x,y,z,r)')
    ap.add_argument('--atoms', help='webapp atoms.csv (id,type,x,y,z,radius) — use with --type-map')
    ap.add_argument('--type-map', default='1:AM_P,2:AM_S,3:SE', help='for --atoms: e.g. "1:AM_P,2:SE"')
    a = ap.parse_args()
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
