import re, numpy as np
from pathlib import Path

STRAIN = 0.005

def read_stress(pwout):
    text = Path(pwout).read_text()
    blocks = list(re.finditer(
        r'total\s+stress\s.*?\(kbar\).*?\n((?:\s*\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s*\n){3})',
        text))
    rows = blocks[-1].group(1).strip().split('\n')
    sig = np.zeros((3,3))
    for r,line in enumerate(rows):
        v = list(map(float, line.split()))
        sig[r] = v[3:6]   # kbar columns
    return np.array([sig[0,0], sig[1,1], sig[2,2], sig[1,2], sig[0,2], sig[0,1]])

sig = {}
for s in ('p','m'):
    for i in range(1,7):
        f = Path(f"e{i}_{s}/pw.out")
        sig[(i,s)] = read_stress(f)
        print(f"e{i}_{s}: {sig[(i,s)]}")

C = np.zeros((6,6))
for j in range(1,7):
    ds = (sig[(j,'p')] - sig[(j,'m')]) / (2*STRAIN)
    for i in range(6):
        C[i,j-1] = -ds[i] * 0.1   # kbar->GPa
C = 0.5*(C + C.T)

print("\nCij (GPa, symmetrized):")
for i in range(6):
    print("  " + "  ".join(f"{C[i,j]:7.2f}" for j in range(6)))

# VRH
K_V = (C[0,0]+C[1,1]+C[2,2] + 2*(C[0,1]+C[0,2]+C[1,2]))/9
G_V = (C[0,0]+C[1,1]+C[2,2] - C[0,1]-C[0,2]-C[1,2] + 3*(C[3,3]+C[4,4]+C[5,5]))/15
S = np.linalg.inv(C)
K_R = 1/(S[0,0]+S[1,1]+S[2,2] + 2*(S[0,1]+S[0,2]+S[1,2]))
G_R = 15/(4*(S[0,0]+S[1,1]+S[2,2]) - 4*(S[0,1]+S[0,2]+S[1,2]) + 3*(S[3,3]+S[4,4]+S[5,5]))
K = 0.5*(K_V+K_R); G = 0.5*(G_V+G_R)
E = 9*K*G/(3*K+G); nu = (3*K-2*G)/(2*(3*K+G))

print(f"\nC11={C[0,0]:.2f}  C12={C[0,1]:.2f}  C13={C[0,2]:.2f}")
print(f"C33={C[2,2]:.2f}  C44={C[3,3]:.2f}")
print(f"K={K:.2f}  G={G:.2f}  E={E:.2f}  nu={nu:.3f}  GPa")
