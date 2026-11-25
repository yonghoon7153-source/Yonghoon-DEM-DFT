"""Unscreened potential of one +q point charge + uniform compensating background (Ewald, G=0 dropped) in the lineage cell.
Probe = every other atom site. Reports the spread of phi over the cell and its dependence on the distance from the defect
lattice plane spanned by a1, a2 (perpendicular coordinate)."""
import itertools, math, sys
import numpy as np
from ase.io import read
from scipy.special import erfc
KE = 14.399645478425668
at = read(sys.argv[1], format="espresso-in")
c = at.cell.array; V = abs(np.linalg.det(c)); pos = at.get_positions(); sym = at.get_chemical_symbols()
n3 = np.cross(c[0], c[1]); A = np.linalg.norm(n3); n3 /= A; h = V / A
print(f"|a1| {np.linalg.norm(c[0]):.2f} |a2| {np.linalg.norm(c[1]):.2f} |a3| {np.linalg.norm(c[2]):.2f} A(a1xa2) {A:.1f} A^2  height {h:.2f} A  V {V:.0f}")
def phi_from(r0, probes, alpha=0.35, s=6.5):
    rc, kc = s/alpha, 2*alpha*s
    hh = V / np.linalg.norm(np.cross(c[[1,2,0]], c[[2,0,1]]), axis=1)
    nR = np.ceil((rc + np.linalg.norm(c,axis=1).sum()) / hh).astype(int)
    out = np.zeros(len(probes))
    d = probes - r0
    for i,j,k in itertools.product(*(range(-m,m+1) for m in nR)):
        r = np.linalg.norm(d + i*c[0]+j*c[1]+k*c[2], axis=1); m = (r>1e-8)&(r<rc)
        out[m] += erfc(alpha*r[m])/r[m]
    B = 2*math.pi*np.linalg.inv(c).T
    nk = np.ceil(kc*np.linalg.norm(c,axis=1)/(2*math.pi)).astype(int)
    G = np.array([i*B[0]+j*B[1]+k*B[2] for i,j,k in itertools.product(*(range(-m,m+1) for m in nk)) if (i,j,k)!=(0,0,0)])
    G2 = (G**2).sum(1); keep = G2 <= kc**2; G, G2 = G[keep], G2[keep]
    out += (np.cos(d @ G.T) * (4*math.pi/V*np.exp(-G2/(4*alpha**2))/G2)).sum(1)
    out -= math.pi/(alpha**2*V)
    return KE*out
for lab, el, idx1 in (("Cl114","Cl",114),("S51","S",51)):
    i0 = idx1-1; assert sym[i0]==el, (lab, sym[i0])
    others = [j for j in range(len(at)) if j!=i0]
    ph = phi_from(pos[i0], pos[others])
    ph2 = phi_from(pos[i0], pos[others], alpha=0.25, s=7.5)
    dz = ((pos[others]-pos[i0]) @ n3); dz = (dz + h/2) % h - h/2      # signed distance from the defect plane, wrapped
    far = np.abs(dz) > 0.40*h; mid = (np.abs(dz) > 6.5) & (np.abs(dz) < 8.5)
    print(f"{lab}: alpha-check max|dphi| {np.abs(ph-ph2).max():.2e} V · phi range over sites {ph.min():+.2f} .. {ph.max():+.2f} V"
          f" · mean phi |dz| 6.5-8.5 A {ph[mid].mean():+.2f} V (n {mid.sum()}) · |dz| > {0.40*h:.1f} A {ph[far].mean():+.2f} V (n {far.sum()})"
          f" · difference {ph[mid].mean()-ph[far].mean():.2f} V per unit charge · screened eps 4/5: {(ph[mid].mean()-ph[far].mean())/4:.1f}/{(ph[mid].mean()-ph[far].mean())/5:.1f} V")
