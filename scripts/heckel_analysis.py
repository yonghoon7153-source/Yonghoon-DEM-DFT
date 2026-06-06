#!/usr/bin/env python3
"""Heckel fit for the pure-SE pressure series.

Reads heckel/manifest.json — a list of points:
  [{"P_MPa": 100, "plate_z": 0.0xxxx, "atom": "...", "contacts": ["...","..."]}, ...]
(plate_z from each mesh_*.stl vertex; contacts optional → enables ε_union/D_union.)

Computes per pressure:
  D_sphere = ΣV_sphere / V_box        (relative density, material-conserving)
  D_union  = (ΣV_sphere - ΣV_lens)/V_box   (geometric; <1 even when over-compressed)
Fits Heckel:  ln(1/(1-D)) = K·P + A   → mean yield pressure P_y = 1/K,
σ_y ≈ P_y/3.  Compares to LPSCl (σ_y≈0.30 GPa, H≈0.85 GPa).

Verdict: linear fit (high R²) with P_y ≈ 0.85 GPa → elastic-softened DEM
faithfully mimics LPSCl plasticity.  Curved / P_y far off → elastic limit.
"""
import json, math, sys
import numpy as np

R_SE = 0.0005
BOX = 0.05


def vol_and_lens(atom, contacts, plate_z):
    V_sphere = 0.0
    with open(atom) as f:
        for _ in range(9): next(f)
        for line in f:
            p = line.split()
            if len(p) < 6: continue
            r = float(p[5]); V_sphere += (4/3)*math.pi*r**3
    V_lens = 0.0
    for cf in (contacts or []):
        with open(cf) as f:
            for line in f:
                if line.startswith('ITEM'): continue
                p = line.split()
                if len(p) < 23: continue
                try: d = float(p[22])
                except: continue
                if 0 < d < 2*R_SE:
                    V_lens += (math.pi/12.0)*d**2*(6.0*R_SE - d)
    V_box = BOX*BOX*plate_z
    return V_sphere, V_lens, V_box


def heckel(P, D):
    """Linear fit ln(1/(1-D)) = K*P + A on points with D<1."""
    m = D < 0.999
    P, D = np.asarray(P)[m], np.asarray(D)[m]
    if len(P) < 2: return None
    y = np.log(1.0/(1.0 - D))
    K, A = np.polyfit(P, y, 1)
    yhat = K*P + A
    ss = np.sum((y - y.mean())**2)
    r2 = 1 - np.sum((y - yhat)**2)/ss if ss > 0 else float('nan')
    Py = 1.0/K if K > 0 else float('nan')            # MPa
    return dict(K=K, A=A, r2=r2, Py_MPa=Py, sigma_y_MPa=Py/3.0)


def main():
    man = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'heckel/manifest.json'))
    rows = []
    for e in man:
        Vs, Vl, Vb = vol_and_lens(e['atom'], e.get('contacts'), e['plate_z'])
        eps_s = (1 - Vs/Vb)*100
        D_s = Vs/Vb
        D_u = (Vs - Vl)/Vb if Vl > 0 else float('nan')
        eps_u = (1 - D_u)*100 if Vl > 0 else float('nan')
        rows.append(dict(P=e['P_MPa'], eps_s=eps_s, D_s=D_s, eps_u=eps_u, D_u=D_u))
        print(f"  P={e['P_MPa']:>4} MPa  ε_sphere={eps_s:+6.2f}%  D_sphere={D_s:.4f}"
              f"   ε_union={eps_u:6.2f}%  D_union={D_u:.4f}")
    P = [r['P'] for r in rows]
    print("\nHeckel fit on D_union (physical, <1):")
    fu = heckel(P, [r['D_u'] for r in rows])
    if fu:
        print(f"  R²={fu['r2']:.4f}  P_y={fu['Py_MPa']:.0f} MPa ({fu['Py_MPa']/1000:.2f} GPa)"
              f"  σ_y≈{fu['sigma_y_MPa']:.0f} MPa")
        print(f"  LPSCl ref: σ_y≈300 MPa, H≈850 MPa → P_y≈850 MPa expected")
        ok = (fu['r2'] > 0.97) and (500 < fu['Py_MPa'] < 1200)
        print(f"  VERDICT: {'✓ elastic-softened DEM mimics plastic yield' if ok else '⚠ deviates — inspect linearity / P_y'}")
    print("\nHeckel fit on D_sphere (flags over-compression where D≥1):")
    fs = heckel(P, [r['D_s'] for r in rows])
    if fs:
        print(f"  R²={fs['r2']:.4f}  P_y={fs['Py_MPa']:.0f} MPa")
    over = [r['P'] for r in rows if r['D_s'] >= 1.0]
    if over:
        print(f"  ⚠ D_sphere≥1 (over-compression artifact) at P={over} MPa → use D_union there")


if __name__ == '__main__':
    main()
