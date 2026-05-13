# -*- coding: utf-8 -*-
"""rhino_scheme_mechanism.py -- 2-panel mechanism scheme for paper.

Builds two symbolic mini-clusters side by side in Rhino:
  LEFT panel  (Li6 family):    NCM-O + full Li layer, Li-O bonds dominate
  RIGHT panel (Li5.4 family):  NCM-O + Li with vacancy + Cl/Br tilting toward
                               vacancy site, multi-halogen-O bonds

Run in Rhino: Tools > PythonScript > Run Script (no xyz needed; coords baked in).
After: add curved arrows for halogen migration, text labels, materials, render.
"""
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

# CPK colors
COLORS = {
    'Li': (153, 113, 217),
    'Cl': (31, 230, 31),
    'Br': (165, 42, 42),
    'O':  (255, 28, 0),
    'S':  (252, 200, 48),
    'vac': (200, 200, 200),
}
RADII = {
    'Li': 0.70, 'Cl': 0.95, 'Br': 1.10, 'O': 0.55, 'S': 1.00, 'vac': 0.70,
}

# Bond colors
BOND_COLOR = {
    'Li-O': (200, 170, 240),   # light purple
    'Cl-O': (60, 230, 60),     # green
    'Br-O': (200, 80, 80),     # wine
    'S-O':  (240, 200, 50),    # yellow
}

_MAT_CACHE = {}


def get_material(name, rgb, transparency=0.0):
    key = (name, rgb, transparency)
    if key in _MAT_CACHE:
        return _MAT_CACHE[key]
    idx = sc.doc.Materials.Add()
    mat = sc.doc.Materials[idx]
    r, g, b = rgb
    mat.DiffuseColor = Rhino.Display.Color4f(r / 255.0, g / 255.0, b / 255.0, 1.0).AsSystemColor()
    mat.Transparency = transparency
    mat.Name = name
    mat.CommitChanges()
    _MAT_CACHE[key] = idx
    return idx


def apply_mat(obj_id, mat_idx):
    obj = sc.doc.Objects.Find(obj_id)
    if obj:
        attrs = obj.Attributes
        attrs.MaterialIndex = mat_idx
        attrs.MaterialSource = Rhino.DocObjects.ObjectMaterialSource.MaterialFromObject
        sc.doc.Objects.ModifyAttributes(obj, attrs, True)


def add_atom(loc, el, radius_scale=1.0, transparency=0.0, name_suffix=""):
    r = RADII[el] * radius_scale
    sph = rs.AddSphere(loc, r)
    rgb = COLORS[el]
    rs.ObjectColorSource(sph, 1)
    rs.ObjectColor(sph, rgb)
    mat = get_material("mat_{}{}".format(el, name_suffix), rgb, transparency)
    apply_mat(sph, mat)
    return sph


def add_bond(p1, p2, bond_type, radius=0.12):
    line = rs.AddLine(p1, p2)
    pipe = rs.AddPipe(line, 0, radius, cap=2)
    rs.DeleteObject(line)
    rgb = BOND_COLOR[bond_type]
    rs.ObjectColorSource(pipe, 1)
    rs.ObjectColor(pipe, rgb)
    mat = get_material("mat_bond_{}".format(bond_type), rgb, 0.0)
    apply_mat(pipe, mat)
    return pipe


def add_label(loc, text, height=1.5):
    return rs.AddText(text, loc, height=height)


# ============================================================
# LEFT PANEL: Li6 family (comp1/comp2 prototype)
# ============================================================
def build_li6_panel(origin_x=0.0):
    """NCM-O row at z=0, Li layer at z=2.2, Cl floating above (not reaching O)."""
    rs.AddLayer("panel_Li6")
    rs.CurrentLayer("panel_Li6")

    # NCM-O atoms (3 in a row along x)
    O_pos = []
    for i, dx in enumerate([-2.5, 0.0, 2.5]):
        p = (origin_x + dx, 0, 0)
        add_atom(p, 'O')
        O_pos.append(p)

    # Full Li layer (4 atoms above, dense)
    Li_pos = []
    for i, dx in enumerate([-3.0, -1.0, 1.0, 3.0]):
        p = (origin_x + dx, 0.3, 2.2)
        add_atom(p, 'Li')
        Li_pos.append(p)

    # Cl far above (does NOT reach interface in Li6)
    p_cl = (origin_x + 0.0, -0.5, 4.5)
    add_atom(p_cl, 'Cl', transparency=0.3)  # slightly transparent = "not active"

    # Li-O bonds: 3 strong bonds
    add_bond(Li_pos[0], O_pos[0], 'Li-O', radius=0.13)
    add_bond(Li_pos[1], O_pos[1], 'Li-O', radius=0.13)
    add_bond(Li_pos[3], O_pos[2], 'Li-O', radius=0.13)
    # weaker middle bond
    add_bond(Li_pos[2], O_pos[1], 'Li-O', radius=0.08)

    # Label
    add_label((origin_x - 2.5, 0, 7.0), "Li6 family", height=0.9)
    add_label((origin_x - 2.5, 0, 6.0), "Li-O dominant", height=0.5)


# ============================================================
# RIGHT PANEL: Li5.4 family (comp3/4/5 prototype)
# ============================================================
def build_li54_panel(origin_x=12.0):
    """NCM-O row at z=0, Li with vacancy at z=2.2, Cl+Br tilted into vacancy."""
    rs.AddLayer("panel_Li54")
    rs.CurrentLayer("panel_Li54")

    # NCM-O atoms
    O_pos = []
    for i, dx in enumerate([-2.5, 0.0, 2.5]):
        p = (origin_x + dx, 0, 0)
        add_atom(p, 'O')
        O_pos.append(p)

    # Li layer with VACANCY at center
    Li_pos = []
    for i, dx in enumerate([-3.0, -1.0, 3.0]):  # skip dx=1.0 (vacancy position)
        p = (origin_x + dx, 0.3, 2.2)
        add_atom(p, 'Li')
        Li_pos.append(p)

    # VACANCY MARKER: transparent ghost sphere at missing Li site
    vac_pos = (origin_x + 1.0, 0.3, 2.2)
    vac = add_atom(vac_pos, 'vac', radius_scale=1.1, transparency=0.7, name_suffix="_vac")

    # Cl tilted DOWN toward vacancy (closer to O)
    p_cl = (origin_x + 1.4, -0.4, 3.0)  # was up high, now near O2
    add_atom(p_cl, 'Cl')

    # Br tilted toward vacancy too (other side)
    p_br = (origin_x + 0.4, 0.4, 3.2)
    add_atom(p_br, 'Br')

    # Bonds: Li-O (fewer because vacancy)
    add_bond(Li_pos[0], O_pos[0], 'Li-O', radius=0.13)
    add_bond(Li_pos[2], O_pos[2], 'Li-O', radius=0.13)

    # Halogen-O bonds: NEW contacts enabled by vacancy
    add_bond(p_cl, O_pos[2], 'Cl-O', radius=0.13)
    add_bond(p_cl, O_pos[1], 'Cl-O', radius=0.10)
    add_bond(p_br, O_pos[1], 'Br-O', radius=0.13)
    add_bond(p_br, O_pos[0], 'Br-O', radius=0.10)

    # Label
    add_label((origin_x - 2.5, 0, 7.0), "Li5.4 family", height=0.9)
    add_label((origin_x - 2.5, 0, 6.0), "halogen redistribution", height=0.5)
    add_label((origin_x + 0.5, 0.3, 1.5), "V_Li", height=0.5)


def main():
    print("Building 2-panel mechanism scheme...")
    build_li6_panel(origin_x=0.0)
    build_li54_panel(origin_x=12.0)

    # Zoom to fit
    rs.ZoomExtents(all=True)
    print("DONE. Now:")
    print("  1. Adjust view (Perspective, F4 rotate)")
    print("  2. Add curved arrows (Curve > InterpCrv) for halogen migration")
    print("  3. Set Display to Rendered")
    print("  4. Run Render command")


main()
