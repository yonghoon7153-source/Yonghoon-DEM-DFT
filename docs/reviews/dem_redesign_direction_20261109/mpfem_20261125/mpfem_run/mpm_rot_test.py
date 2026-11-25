# Development check (1저자 11-25 질문): our MPM material update (scripts/mpm3d_compaction.py lines 2954-2957 stress,
# 3017-3028 F update + Hencky return map) under the same compression -> rigid rotation path. numpy transcription.
import math, sys
import numpy as np
E, NU, SY = 1.0e7, 0.45, 4.0e5
MU, LA = E / (2 * (1 + NU)), E * NU / ((1 + NU) * (1 - 2 * NU))
def tau(F):
    U, s, Vt = np.linalg.svd(F); J = np.prod(s)
    return 2 * MU * (F - U @ Vt) @ F.T + np.eye(3) * LA * J * (J - 1)     # Kirchhoff (code line 2956-2957)
def plastic(F, yld):
    U, s, Vt = np.linalg.svd(F)
    e = np.log(np.maximum(s, 1e-4)); tr = e.mean(); d = e - tr; dn = np.linalg.norm(d) + 1e-9
    dg = dn - yld / (2 * MU)
    if dg > 0:
        e = (d - dg * d / dn) + tr
        F = U @ np.diag(np.exp(e)) @ Vt
    return F
def run(nrot, dtype):
    F = np.eye(3, dtype=dtype); ly_prev = 1.0
    for k in range(1, 101):                                   # isochoric plane-strain compression ly 1 -> 0.85
        ly = 1.0 - 0.15 * k / 100
        L = np.diag([ly_prev / ly - 1.0, ly / ly_prev - 1.0, 0.0])   # first-order step (I + dt C)
        F = plastic(((np.eye(3) + L) @ F).astype(dtype), SY); ly_prev = ly
    t0 = tau(F.astype(np.float64)); J0 = np.linalg.det(F)
    dth = (math.pi / 6) / nrot; W = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 0]], dtype=np.float64)
    Racc = np.eye(3)
    for k in range(nrot):                                     # rigid rotation as MPM sees it: F <- (I + dt W) F
        A = np.eye(3) + dth * W
        F = plastic((A @ F).astype(dtype), SY); Racc = A @ Racc
    t1 = tau(F.astype(np.float64)); J1 = np.linalg.det(F)
    th = nrot * math.atan(dth)                                # rotation angle actually applied by the first-order steps
    Q = np.array([[math.cos(th), -math.sin(th), 0], [math.sin(th), math.cos(th), 0], [0, 0, 1.0]])
    diff = np.abs(Q.T @ t1 @ Q - t0).max()
    vm0 = math.sqrt(1.5) * np.linalg.norm(t0 - np.trace(t0) / 3 * np.eye(3))
    return diff / SY, J1 / J0 - 1.0, vm0 / SY
print('our MPM update, rotation 30 deg after 15 % compression (diff = max |Q^T tau Q - tau0| / sy)')
for dt in (np.float64, np.float32):
    for n in (300, 3000, 30000):
        d, dJ, vm = run(n, dt)
        print(f'  {dt.__name__:7s} steps {n:>6d}  diff/sy {d:.3e}  J drift {dJ:+.2e}  vonMises(t0)/sy {vm:.4f}')
