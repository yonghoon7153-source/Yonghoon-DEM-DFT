#!/usr/bin/env python3
"""Extract DEM design points (1:1 MPM-matchable) from docs/case_summary.csv.

For each DEM case pulls the geometry + composition + measured porosity needed to
reproduce it in the champion MPM (scripts/mpm2d_PS_pressure.py):
  r_AM_P, r_AM_S, r_SE (µm)  |  phi_am, phi_se (vol frac)  |  P:S (AM_P:AM_S)
  AM wt%  |  thickness (µm) / areal capacity tag  |  DEM porosity @ target P

Writes docs/data/dem_design_points.csv → fed to scripts/mpm_dem_match.py on the
GPU box, which runs the MPM at the SAME (sizes, composition) and reads porosity
at the SAME pressure → 1:1 DEM↔MPM porosity cross-validation (frame [4]).

Run:  python3 scripts/dem_design_points.py [--pressure 300] [--real-only]
"""
import argparse
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, '..', 'docs', 'case_summary.csv')
OUT = os.path.join(HERE, '..', 'docs', 'data', 'dem_design_points.csv')

RHO_AM, RHO_SE = 4.8, 2.0   # g/cc (vol↔wt), matches MPM


def _f(row, key):
    v = row.get(key, '')
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _ps(row):
    """AM_P:AM_S ratio → (P, S) ints, from meta/fm ps_ratio or ps_frac_AM_P."""
    for k in ('meta__ps_ratio', 'fm__ps_ratio'):
        v = row.get(k, '')
        if v and ':' in str(v):
            try:
                p, s = (int(round(float(z))) for z in str(v).split(':'))
                return p, s
            except Exception:
                pass
    fp = _f(row, 'meta__ps_frac_AM_P')
    if fp is not None:
        p = int(round(fp * 10)); return p, 10 - p
    return 7, 3   # default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pressure', type=float, default=300.0,
                    help='keep cases at this target pressure MPa (±tol)')
    ap.add_argument('--tol', type=float, default=40.0)
    ap.add_argument('--real-only', action='store_true',
                    help='only input_*real* cases (the champion family)')
    a = ap.parse_args()

    with open(SUMMARY) as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        name = r.get('meta__name') or r.get('case_id') or ''
        rAP = _f(r, 'fm__r_AM_P'); rAS = _f(r, 'fm__r_AM_S'); rSE = _f(r, 'fm__r_SE')
        phi_am = _f(r, 'fm__phi_am'); phi_se = _f(r, 'fm__phi_se')
        poro = _f(r, 'fm__porosity'); P = _f(r, 'fm__target_pressure_mpa')
        thick = _f(r, 'fm__thickness_um')
        e_se = _f(r, 'fm__e_se_eff_gpa')   # SE Young's modulus (E05/E15 variants differ)
        # Monomodal AM (P:S=0:10) cases have NO AM_P → r_AM_P is blank.  Don't
        # require it; AM_S + SE is a valid 2-size system.  ratio_P just becomes 0
        # (the MPM build then skips the empty AM_P phase).
        if None in (rAS, rSE, phi_am, phi_se, poro):
            continue
        if rSE <= 0 or rAS <= 0:
            continue
        if rAP is None or rAP <= 0:
            rAP = 0.0
        if P is not None and abs(P - a.pressure) > a.tol:
            continue
        if a.real_only and 'real' not in name:
            continue
        p, s = _ps(r)
        # AM wt% from vol fractions
        wam = phi_am * RHO_AM; wse = phi_se * RHO_SE
        am_wt = 100.0 * wam / (wam + wse) if (wam + wse) > 0 else 0.0
        # capacity tag from name (1mAh / 2mAh / …)
        mah = ''
        mm = re.search(r'(\d+)mAh', name)
        if mm:
            mah = mm.group(1)
        out.append(dict(name=name, r_AM_P=rAP, r_AM_S=rAS, r_SE=rSE,
                        ratio_P=round(rAP / rSE, 3) if rAP > 0 else 0.0,
                        ratio_S=round(rAS / rSE, 3),
                        phi_am=phi_am, phi_se=phi_se, AM_wt=round(am_wt, 1),
                        PS=f'{p}:{s}', mAh=mah, thickness_um=thick or '',
                        P_MPa=P or a.pressure, dem_porosity=round(poro, 3),
                        e_se_gpa=round(e_se, 4) if e_se else 1.35))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cols = ['name', 'r_AM_P', 'r_AM_S', 'r_SE', 'ratio_P', 'ratio_S',
            'phi_am', 'phi_se', 'AM_wt', 'PS', 'mAh', 'thickness_um',
            'P_MPa', 'dem_porosity', 'e_se_gpa']
    with open(OUT, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for d in out:
            w.writerow(d)
    print(f"wrote {OUT}  ({len(out)} design points @ {a.pressure}±{a.tol} MPa"
          f"{' real-only' if a.real_only else ''})")
    # quick summary
    print(f"  {'name':28s} {'rP/rS/rSE(µm)':16s} {'AMwt':>5s} {'P:S':>4s} {'DEMε%':>6s}")
    for d in sorted(out, key=lambda x: x['name'])[:40]:
        print(f"  {d['name'][:28]:28s} "
              f"{d['r_AM_P']:.1f}/{d['r_AM_S']:.1f}/{d['r_SE']:.2f}   "
              f"{d['AM_wt']:5.1f} {d['PS']:>4s} {d['dem_porosity']:6.1f}")
    print(f"  ... total {len(out)}")


if __name__ == '__main__':
    main()
