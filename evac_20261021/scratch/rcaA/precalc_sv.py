import numpy as np


def ref_I(nn, edges, bot, top):
    L = np.zeros((nn, nn)); b = np.zeros(nn)
    for i, j, g in edges:
        L[i, i] += g; L[j, j] += g; L[i, j] -= g; L[j, i] -= g
    for i, g in bot:
        L[i, i] += g; b[i] += g
    for i, g in top:
        L[i, i] += g
    phi = np.linalg.solve(L, b)
    return float(sum(g * (1.0 - phi[i]) for i, g in bot)), phi


GAX, GPL = 100.0, 200.0
gsv = 2 * 100 * 250 / 350.0
for gj in (0.5, 0.25, 1.0, 0.4):
    # A0..A20 = 0..20 ; b0 (2,1,1) = 21 ; b1..b21 = (3,1,1..21) = 22..42 ; s = 43
    A = list(range(21)); B = list(range(21, 43)); S = 43
    E = [(A[i], A[i + 1], GAX) for i in range(20)] + [(B[i], B[i + 1], GAX) for i in range(21)]
    E += [(A[1], B[0], gj)]
    Esv = [(A[20], S, gsv), (S, B[20], gsv)]
    If, phf = ref_I(44, E + Esv, [(A[0], GPL)], [(B[21], GPL)])
    Ic, _ = ref_I(44, E + [(S, B[20], gsv)], [(A[0], GPL)], [(B[21], GPL)])
    P = {}
    for i, j, g in E + Esv:
        P[(i, j)] = g * (phf[i] - phf[j]) ** 2
    Psv = sum(P[(i, j)] for i, j, g in Esv)
    Pvv = P[(A[1], B[0])]
    Isv = gsv * (phf[A[20]] - phf[S])
    print(f'gj {gj}: I_full {If:.6g} I_cut {Ic:.6g} ratio {If / Ic:.6g} · P_sv {Psv:.4g} P_vv {Pvv:.4g} guard {Psv >= Pvv} · '
          f'SV current frac {Isv / If:.4f}')
