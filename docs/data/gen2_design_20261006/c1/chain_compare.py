#!/usr/bin/env python3
"""designC1 — sphere-chain FV (fv_sphere_chain_table.txt) vs edge models (r=1, sigma=1, d=2h)."""
import math, numpy as np
T = np.loadtxt(__file__.rsplit('/',1)[0] + '/fv_sphere_chain_table.txt')
print(f'{"s":>5} {"R_FV":>9} | {"H0 cyl+Max":>11} {"H1 cyl+psi":>11} {"H12 W+psi":>10} | {"(R_FV-R_W)/(psi R_M)":>21}')
for s, h, r1, r2, r3, R, p in T:
    psi = (1-s)**1.5; RM = 1/(2*s); Rcyl = 2*h/math.pi; V = math.pi*(h - h**3/3); RW = 2*h*h/V
    H0, H1, H12 = Rcyl+RM, Rcyl+psi*RM, RW+psi*RM
    print(f'{s:5.2f} {R:9.5f} | {100*(H0/R-1):+10.1f}% {100*(H1/R-1):+10.1f}% {100*(H12/R-1):+9.1f}% | {(R-RW)/(psi*RM):21.4f}')
