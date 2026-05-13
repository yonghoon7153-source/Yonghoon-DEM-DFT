# -*- coding: utf-8 -*-
"""rhino_import_interface.py -- import xyz atoms into Rhino as spheres.

Run inside Rhino: Tools > PythonScript > Run Script. Select xyz file.
Creates:
  - Spheres for each atom (only interface region: z within +/-3 A of gap)
  - Layered by element with proper colors
  - Optional bond cylinders for Li-O, S-O within cutoff

After import, user manually:
  - Adds arrows (Curve > Polyline / FilletEdge for nice arrows)
  - Adds vacancy marker (dashed sphere via Cylinder Subtract)
  - Adds text labels (TextObject command)
  - Applies materials (Rhino default + adjust to taste)
  - Render via Rhino Render or KeyShot

Usage in Rhino:
    _-RunPythonScript "rhino_import_interface.py"

Or paste into Rhino Python editor.

Color preset matches our render scheme (CPK-ish).
"""
import rhinoscriptsyntax as rs
import os

# Element colors (RGB 0-255)
COLORS = {
    'Li': (153, 113, 217),
    'P':  (168, 168, 168),
    'S':  (252, 200, 48),
    'Cl': (31, 230, 31),
    'Br': (165, 42, 42),
    'Ni': (80, 120, 210),
    'O':  (255, 28, 0),
}
# Atomic radii in Å (visual)
RADII = {
    'Li': 0.70, 'P': 0.95, 'S': 1.00, 'Cl': 0.95, 'Br': 1.10,
    'Ni': 0.80, 'O': 0.55,
}

BOND_CUTOFFS = {
    ('Li', 'O'): 2.8,
    ('S',  'O'): 3.0,
    ('Cl', 'O'): 3.2,
    ('Br', 'O'): 3.4,
}

# ZOOM WINDOW: ±N Å around the SE-NCM interface (i.e. where Ni top + 0.5 ends)
INTERFACE_ZOOM_BELOW = 3.0   # show NCM down to 3 Å below interface
INTERFACE_ZOOM_ABOVE = 4.0   # show SE up to 4 Å above interface


def parse_xyz(path):
    lines = open(path).read().splitlines()
    n = int(lines[0])
    atoms = []
    for line in lines[2:2 + n]:
        p = line.split()
        if len(p) >= 4:
            atoms.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return atoms


def ensure_layer(name, color_rgb):
    if not rs.IsLayer(name):
        rs.AddLayer(name, color=color_rgb)
    return name


def create_atom(loc, el, layer):
    rs.CurrentLayer(layer)
    sphere = rs.AddSphere(loc, RADII.get(el, 0.8))
    if sphere:
        rs.ObjectColorSource(sphere, 1)
        rs.ObjectColor(sphere, COLORS.get(el, (128, 128, 128)))
    return sphere


def create_bond(p1, p2, layer, radius=0.10):
    rs.CurrentLayer(layer)
    line = rs.AddLine(p1, p2)
    # Make pipe (cylinder along line)
    pipe = rs.AddPipe(line, 0, radius, cap=2)
    rs.DeleteObject(line)
    return pipe


def main():
    path = rs.OpenFileName("Select xyz", "xyz files|*.xyz|All|*.*||")
    if not path:
        return
    atoms = parse_xyz(path)
    print("Read {} atoms from {}".format(len(atoms), path))

    # Determine interface from NCM atoms (Ni + O)
    ncm_z_max = max(a[3] for a in atoms if a[0] in ('Ni', 'O'))
    z_lo = ncm_z_max + 0.5 - INTERFACE_ZOOM_BELOW
    z_hi = ncm_z_max + 0.5 + INTERFACE_ZOOM_ABOVE
    print("Interface zoom: z = {:.2f} to {:.2f}".format(z_lo, z_hi))

    # Create layers
    layers = {}
    for el, c in COLORS.items():
        layers[el] = ensure_layer("atom_{}".format(el), c)
    bond_layer = ensure_layer("bonds", (100, 100, 100))

    # Place atoms
    n_atoms = 0
    placed = []
    for el, x, y, z in atoms:
        if z < z_lo or z > z_hi:
            continue
        create_atom((x, y, z), el, layers[el])
        placed.append((el, x, y, z))
        n_atoms += 1
    print("Placed {} atoms".format(n_atoms))

    # Bonds (between SE atoms and NCM O within cutoff)
    n_bonds = 0
    ncm_O = [(el, x, y, z) for (el, x, y, z) in placed if el == 'O']
    for el, x, y, z in placed:
        if el not in ('Li', 'S', 'Cl', 'Br'):
            continue
        for (oel, ox, oy, oz) in ncm_O:
            d = ((x - ox) ** 2 + (y - oy) ** 2 + (z - oz) ** 2) ** 0.5
            cutoff = BOND_CUTOFFS.get((el, 'O'), 0)
            if 0 < d <= cutoff:
                create_bond((x, y, z), (ox, oy, oz), bond_layer)
                n_bonds += 1
    print("Placed {} bonds".format(n_bonds))
    print("DONE. Now add arrows + labels + render.")


main()
