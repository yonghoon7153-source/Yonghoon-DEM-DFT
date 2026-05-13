# -*- coding: utf-8 -*-
"""rhino_scheme_v2_literature.py -- literature-grounded mechanism scheme.

Two-panel mechanism figure based on:
  - Lee et al. Science 2025 (halide segregation to cathode)
  - Adeli & Nazar Angew 2019 (Li vacancy framework)
  - de Klerk & Wagemaker Chem Mater 2016 (4a/4d halogen disorder)
  - Famprikis PCCP 2019 (anion+cation disorder in mixed halide)
  - Zuo Angew 2023 (Cl-rich Wad enhancement)

LEFT panel (Li6 family, comp1/comp2):
  - Halogens locked at bulk 4a/4d positions, no migration pathway
  - Interface = Li-O contacts only
  - Pre-segregation state

RIGHT panel (Li5.4 family, comp3/4/5):
  - V_Li ghost at vacancy site
  - Halogens migrating toward NCM-O (curved arrows = Lee 2025)
  - Partial LiX-like coordination at interface
  - Post-segregation state, multi-bond active

Output: Rhino scene ready for render. Citation labels included as text.
Add manual curved arrows in Rhino afterward for halogen migration paths.
"""
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

# CPK colors
COLORS = {
    'Li':  (153, 113, 217),
    'Cl':  (31, 230, 31),
    'Br':  (165, 42, 42),
    'O':   (255, 28, 0),
    'S':   (252, 200, 48),
    'P':   (168, 168, 168),
    'Ni':  (80, 120, 210),
    'vac': (200, 200, 200),
}
RADII = {
    'Li': 0.70, 'Cl': 0.95, 'Br': 1.10, 'O': 0.55,
    'S': 1.00, 'P': 0.95, 'Ni': 0.80, 'vac': 0.75,
}

BOND_COLOR = {
    'Li-O':    (200, 170, 240),  # light purple = primary attraction
    'Cl-O':    (60, 230, 60),    # green
    'Br-O':    (200, 80, 80),    # wine
    'Li-X':    (140, 140, 140),  # gray = SE bulk bond
    'PS4':     (240, 200, 50),   # yellow
    'NCM':     (180, 60, 60),    # red-brown = NCM interior
}

_MAT = {}


def mat(name, rgb, transparency=0.0):
    key = (name, rgb, transparency)
    if key in _MAT:
        return _MAT[key]
    idx = sc.doc.Materials.Add()
    m = sc.doc.Materials[idx]
    r, g, b = rgb
    m.DiffuseColor = Rhino.Display.Color4f(r/255.0, g/255.0, b/255.0, 1.0).AsSystemColor()
    m.Transparency = transparency
    m.Name = name
    m.CommitChanges()
    _MAT[key] = idx
    return idx


def apply_mat(obj_id, mat_idx):
    o = sc.doc.Objects.Find(obj_id)
    if o:
        a = o.Attributes
        a.MaterialIndex = mat_idx
        a.MaterialSource = Rhino.DocObjects.ObjectMaterialSource.MaterialFromObject
        sc.doc.Objects.ModifyAttributes(o, a, True)


def atom(loc, el, scale=1.0, transparency=0.0, tag=""):
    r = RADII[el] * scale
    s = rs.AddSphere(loc, r)
    rgb = COLORS[el]
    rs.ObjectColorSource(s, 1)
    rs.ObjectColor(s, rgb)
    apply_mat(s, mat("mat_{}{}".format(el, tag), rgb, transparency))
    return s


def bond(p1, p2, bond_type, radius=0.10):
    line = rs.AddLine(p1, p2)
    pipe = rs.AddPipe(line, 0, radius, cap=2)
    rs.DeleteObject(line)
    if isinstance(pipe, list):
        pipe = pipe[0]
    rgb = BOND_COLOR[bond_type]
    rs.ObjectColorSource(pipe, 1)
    rs.ObjectColor(pipe, rgb)
    apply_mat(pipe, mat("bond_{}".format(bond_type), rgb, 0.0))
    return pipe


def label(loc, text, height=0.6):
    return rs.AddText(text, loc, height=height)


# =============================================================
# LEFT PANEL: Li6 family (vacancy-poor, pre-segregation)
# =============================================================
def panel_Li6(x0=0.0):
    rs.AddLayer("Li6_panel"); rs.CurrentLayer("Li6_panel")

    # NCM cathode oxygen layer (bottom) -- 4 O atoms
    O = []
    for dx in [-3.0, -1.0, 1.0, 3.0]:
        p = (x0 + dx, 0, 0)
        atom(p, 'O')
        O.append(p)
    # Ni below O (showing NCM)
    for dx in [-2.0, 0.0, 2.0]:
        atom((x0 + dx, 0.3, -1.5), 'Ni', scale=0.9)

    # SE Li layer (full, 4 atoms)
    Li = []
    for dx in [-3.0, -1.0, 1.0, 3.0]:
        p = (x0 + dx, 0.3, 2.4)
        atom(p, 'Li')
        Li.append(p)

    # PS4 tetrahedron (just P+S clusters for symbol)
    atom((x0 - 1.5, 1.2, 4.5), 'P', scale=0.9)
    for sx, sy, sz in [(-2.3, 1.0, 5.0), (-0.8, 1.0, 5.0), (-1.5, 2.0, 5.0), (-1.5, 1.0, 3.8)]:
        atom((x0 + sx, sy, sz), 'S')

    # Halogen TRAPPED in bulk (high up, NOT at interface)
    # Cl at 4a-like position (bulk)
    atom((x0 + 1.5, 1.2, 5.5), 'Cl', transparency=0.0, tag="_bulk")
    # Br at 4d-like position (also bulk)
    atom((x0 + 0.5, -1.0, 4.8), 'Br', transparency=0.0, tag="_bulk")

    # Li-O bonds (only active channel)
    bond(Li[0], O[0], 'Li-O', radius=0.13)
    bond(Li[1], O[1], 'Li-O', radius=0.13)
    bond(Li[2], O[2], 'Li-O', radius=0.13)
    bond(Li[3], O[3], 'Li-O', radius=0.13)

    # Labels
    label((x0 - 3.0, -2.5, 8.5), "Li6 family", height=0.9)
    label((x0 - 3.0, -2.5, 7.7), "(comp1, comp2)", height=0.45)
    label((x0 - 3.0, -2.5, 6.9), "Vacancy-poor", height=0.4)
    label((x0 - 3.0, -2.5, 6.3), "Halogen locked in bulk", height=0.4)
    label((x0 - 3.0, -2.5, 5.7), "Single channel: Li-O", height=0.4)
    label((x0 - 3.0, -2.5, 5.1), "Wad ~ 190 mJ/m^2", height=0.4)

    # NCM label
    label((x0 - 3.5, 0, -2.2), "NCM cathode", height=0.4)
    label((x0 - 3.5, 0, 2.5), "SE bulk", height=0.4)


# =============================================================
# RIGHT PANEL: Li5.4 family (vacancy-rich, post-segregation)
# =============================================================
def panel_Li54(x0=14.0):
    rs.AddLayer("Li54_panel"); rs.CurrentLayer("Li54_panel")

    # NCM cathode oxygen layer
    O = []
    for dx in [-3.0, -1.0, 1.0, 3.0]:
        p = (x0 + dx, 0, 0)
        atom(p, 'O')
        O.append(p)
    for dx in [-2.0, 0.0, 2.0]:
        atom((x0 + dx, 0.3, -1.5), 'Ni', scale=0.9)

    # SE Li layer WITH VACANCY (skip dx=1.0)
    Li = []
    for dx in [-3.0, -1.0, 3.0]:
        p = (x0 + dx, 0.3, 2.4)
        atom(p, 'Li')
        Li.append(p)

    # V_Li ghost sphere (transparent gray at missing Li site)
    vac_pos = (x0 + 1.0, 0.3, 2.4)
    atom(vac_pos, 'vac', scale=1.1, transparency=0.7, tag="_vac")

    # PS4 cluster (slightly disordered, Famprikis 2019)
    atom((x0 - 1.5, 1.2, 4.5), 'P', scale=0.9)
    for sx, sy, sz in [(-2.3, 1.0, 5.0), (-0.8, 1.0, 5.0), (-1.5, 2.0, 5.0), (-1.5, 1.0, 3.8)]:
        atom((x0 + sx, sy, sz), 'S')

    # Halogen SEGREGATED toward NCM-O (Lee 2025 Science)
    # Cl tilted down, close to NCM-O[2] = (x0+1, 0, 0). Forms partial LiX layer
    cl_pos = (x0 + 1.3, -0.3, 1.4)
    atom(cl_pos, 'Cl')

    # Br on other side, near NCM-O[1] = (x0-1, 0, 0)
    br_pos = (x0 - 0.7, 0.4, 1.6)
    atom(br_pos, 'Br')

    # Li-O bonds (fewer due to vacancy)
    bond(Li[0], O[0], 'Li-O', radius=0.13)
    bond(Li[2], O[3], 'Li-O', radius=0.13)

    # X-O bonds (new channel activated by segregation)
    bond(cl_pos, O[2], 'Cl-O', radius=0.14)
    bond(cl_pos, O[3], 'Cl-O', radius=0.10)
    bond(br_pos, O[1], 'Br-O', radius=0.14)
    bond(br_pos, O[0], 'Br-O', radius=0.10)

    # Li (still some) coordinating with migrated X = partial LiX layer
    bond(Li[1], cl_pos, 'Li-X', radius=0.08)
    bond(Li[1], br_pos, 'Li-X', radius=0.08)

    # Labels
    label((x0 - 3.0, -2.5, 8.5), "Li5.4 family", height=0.9)
    label((x0 - 3.0, -2.5, 7.7), "(comp3, comp4, comp5)", height=0.45)
    label((x0 - 3.0, -2.5, 6.9), "Vacancy-rich (V_Li)", height=0.4)
    label((x0 - 3.0, -2.5, 6.3), "Halide segregation to NCM", height=0.4)
    label((x0 - 3.0, -2.5, 5.7), "Multi-channel: Li-O + Cl-O + Br-O", height=0.4)
    label((x0 - 3.0, -2.5, 5.1), "Wad ~ 288 mJ/m^2 (+50%)", height=0.4)

    # V_Li in-place label
    label((x0 + 1.4, 0.5, 2.4), "V_Li", height=0.4)
    label((x0 + 1.4, 0.5, 1.9), "[Adeli 2019]", height=0.3)

    # NCM / SE layer labels
    label((x0 - 3.5, 0, -2.2), "NCM cathode", height=0.4)
    label((x0 - 3.5, 0, 2.5), "SE bulk", height=0.4)

    # Migration annotation (text only -- actual curved arrows manual)
    label((x0 + 2.5, -1, 3.5), "Halide migration", height=0.3)
    label((x0 + 2.5, -1, 3.0), "[Lee, Science 2025]", height=0.3)


# =============================================================
# Bottom citation block (paper figure caption-like)
# =============================================================
def citation_block(x0=7.0):
    rs.AddLayer("citations"); rs.CurrentLayer("citations")
    cy = -5.5
    label((x0 - 5, cy, 0), "Literature basis:", height=0.5)
    refs = [
        "Lee et al. Science 388, 724 (2025) -- halide segregation to cathode",
        "Adeli & Nazar, Angew. Chem. 58, 8681 (2019) -- Li vacancy framework",
        "de Klerk & Wagemaker, Chem. Mater. 28, 3122 (2016) -- 4a/4d halogen disorder",
        "Famprikis et al. PCCP 21, 22311 (2019) -- mixed halide anion+cation disorder",
        "Zuo et al. Angew. Chem. 62, e202213228 (2023) -- Cl-rich NMC Wad enhancement",
    ]
    for i, r in enumerate(refs):
        label((x0 - 5, cy - 0.7 - 0.5 * i, 0), r, height=0.3)


def main():
    print("Building literature-grounded mechanism scheme v2...")
    panel_Li6(x0=0.0)
    panel_Li54(x0=14.0)
    citation_block(x0=7.0)

    rs.ZoomExtents(all=True)
    print("DONE.")
    print()
    print("Next manual steps in Rhino:")
    print("  1. Set Perspective view, F4 to rotate")
    print("  2. Display mode -> Rendered")
    print("  3. Add CURVED ARROWS in Li5.4 panel:")
    print("     - Cl arrow: from initial bulk position down to NCM-O area")
    print("     - Br arrow: from initial bulk position down to NCM-O area")
    print("     Curve > Interpolate Points, then Pipe(0.05), add Cone at tip")
    print("  4. Add dashed Circle around V_Li ghost for emphasis")
    print("  5. Run Render command")
    print()
    print("Bond color legend:")
    print("  Light purple = Li-O (primary, both panels)")
    print("  Green        = Cl-O (Li5.4 only, halide segregation)")
    print("  Wine         = Br-O (Li5.4 only, halide segregation)")
    print("  Gray         = Li-X (residual Li coordinating segregated halide)")


main()
