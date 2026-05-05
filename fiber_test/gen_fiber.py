"""
VGCF single-fiber LAMMPS data file generator.

Chain along +x axis: N spheres connected by harmonic bonds + harmonic angles.
Scale: r x1000, E x0.001  (same convention as the LIGGGHTS bimodal script).

Real VGCF reference (post-scale):
    r       = 0.5e-3 m   (radius of each sphere; fiber diameter 1e-3 m)
    L0      = 1.0e-3 m   (bond rest length = 2*r, touching spheres)
    rho     = 1900 kg/m^3
    E_sim   = 6.0e8 Pa   (600 GPa graphitic * 0.001)
"""

import math
from pathlib import Path

# ---- fiber geometry --------------------------------------------------------
N        = 10           # spheres per fiber  -> fiber length = (N-1)*L0
r        = 0.5e-3
L0       = 1.0e-3
rho      = 1900.0
E_sim    = 6.0e8

# place fiber horizontally; left tip at origin
x0, y0, z0 = 0.0, 0.0, 0.05

# ---- derived ---------------------------------------------------------------
A    = math.pi * r * r            # cross section
I    = math.pi * r**4 / 4.0       # 2nd moment of area
mass = rho * (4.0/3.0) * math.pi * r**3

# stretch:  U_bond  = K_b (r - r0)^2     -> K_b = (E A / L0) / 2
K_b  = 0.5 * E_sim * A / L0
# bend:     U_angle = K_a (theta - 180)^2 -> K_a = (E I / L0) / 2
K_a  = 0.5 * E_sim * I / L0

print(f"# bond_coeff  1 {K_b:.6e} {L0:.6e}")
print(f"# angle_coeff 1 {K_a:.6e} 180.0")
print(f"# per-sphere mass = {mass:.6e} kg")
print(f"# fiber length    = {(N-1)*L0*1e3:.3f} mm")

# ---- box (loose, just for visualization) ----------------------------------
xlo, xhi = -2*L0, (N+2)*L0
ylo, yhi = -5*L0, 5*L0
zlo, zhi = 0.0,   0.10

# ---- write LAMMPS data file -----------------------------------------------
out = Path(__file__).parent / "fiber.data"

n_atoms  = N
n_bonds  = N - 1
n_angles = N - 2

lines = []
lines.append("LAMMPS data file: single VGCF fiber (cantilever test)\n")
lines.append(f"{n_atoms} atoms")
lines.append(f"{n_bonds} bonds")
lines.append(f"{n_angles} angles")
lines.append("")
lines.append("1 atom types")
lines.append("1 bond types")
lines.append("1 angle types")
lines.append("")
lines.append(f"{xlo} {xhi} xlo xhi")
lines.append(f"{ylo} {yhi} ylo yhi")
lines.append(f"{zlo} {zhi} zlo zhi")
lines.append("")
lines.append("Atoms # hybrid")
lines.append("")
# atom_style hybrid sphere bond ->
#   atom-ID atom-type diameter density   x y z   molecule-ID
diam = 2.0 * r
mol_id = 1
for i in range(N):
    aid = i + 1
    x = x0 + i * L0
    y = y0
    z = z0
    lines.append(f"{aid} 1 {diam:.6e} {rho:.6e} {x:.6e} {y:.6e} {z:.6e} {mol_id}")

lines.append("")
lines.append("Bonds")
lines.append("")
for i in range(n_bonds):
    bid = i + 1
    a1, a2 = i + 1, i + 2
    lines.append(f"{bid} 1 {a1} {a2}")

lines.append("")
lines.append("Angles")
lines.append("")
for i in range(n_angles):
    aid = i + 1
    a1, a2, a3 = i + 1, i + 2, i + 3
    lines.append(f"{aid} 1 {a1} {a2} {a3}")

lines.append("")
out.write_text("\n".join(lines))
print(f"\nwrote {out}")
