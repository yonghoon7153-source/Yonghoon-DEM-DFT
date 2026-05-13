"""blender_render_with_arrows.py — paper-quality atomistic render + mechanism arrows.

Extends blender_render_interface.py to add:
  • 3D arrow (cylinder + cone tip) for vacancy → Li migration (Li5.4 case)
  • Empty wireframe sphere for vacancy marker
  • Optional: highlighted "key" atoms with emission glow
  • 3D text labels (basic, may need post-edit in Inkscape)

Usage:
    blender --background --python blender_render_with_arrows.py -- \\
        INPUT.xyz OUTPUT.png [comp1|comp4_v2]

The third arg sets annotation style:
    comp1     → "S-rich termination" label, no vacancy
    comp4_v2  → vacancy marker + migration arrow + Li-rich termination

Example:
    blender --background --python blender_render_with_arrows.py -- \\
        comp4_v2_R1_origin_d1.4_orthogonal.xyz comp4_v2_render.png comp4_v2
"""
import sys, os, math, re

try:
    import bpy
    from mathutils import Vector
except ImportError:
    print("Run inside Blender:")
    print("  blender --background --python blender_render_with_arrows.py -- in.xyz out.png comp1|comp4_v2")
    sys.exit(1)

# CLI args
argv = sys.argv
if "--" in argv:
    argv = argv[argv.index("--") + 1:]
else:
    argv = []

if len(argv) < 2:
    print("Need INPUT.xyz OUTPUT.png [annotation_style]")
    sys.exit(1)

INPUT_XYZ = argv[0]
OUTPUT_PNG = argv[1]
STYLE = argv[2] if len(argv) >= 3 else "comp4_v2"
print(f"Input: {INPUT_XYZ}\nOutput: {OUTPUT_PNG}\nStyle: {STYLE}")

# ────────────────────────────────────────────────────────
ELEMENT_COLORS = {
    'Li': (0.60, 0.44, 0.85, 1.0),
    'P':  (0.66, 0.66, 0.66, 1.0),
    'S':  (0.99, 0.78, 0.19, 1.0),
    'Cl': (0.12, 0.90, 0.12, 1.0),
    'Br': (0.65, 0.16, 0.16, 1.0),
    'Ni': (0.31, 0.47, 0.82, 1.0),
    'O':  (1.00, 0.11, 0.00, 1.0),
}
RADII = {
    'Li': 0.70, 'P': 0.95, 'S': 1.00, 'Cl': 0.95, 'Br': 1.10,
    'Ni': 0.80, 'O': 0.55,
}

BOND_CUTOFFS = [
    ('Li', 'O', 2.8, (0.10, 0.85, 1.00), 0.13, False),   # cyan, attractive
    ('S',  'O', 3.0, (1.00, 0.15, 0.10), 0.10, True),    # red, repulsive (dashed-style stub)
    ('Cl', 'O', 3.2, (1.00, 0.65, 0.10), 0.10, False),
    ('Br', 'O', 3.4, (0.60, 0.20, 0.80), 0.10, False),
]


def read_xyz(path):
    lines = open(path).read().splitlines()
    n = int(lines[0])
    header = lines[1]
    m = re.search(r'Lattice="([^"]+)"', header)
    cell = None
    if m:
        v = list(map(float, m.group(1).split()))
        cell = [v[0:3], v[3:6], v[6:9]]
    atoms = []
    for line in lines[2:2 + n]:
        p = line.split()
        if len(p) >= 4:
            atoms.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return cell, atoms


def make_material(name, color, metallic=0.1, roughness=0.3, emission=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = color
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = metallic
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = roughness
    if emission > 0 and 'Emission' in bsdf.inputs:
        bsdf.inputs['Emission'].default_value = (color[0], color[1], color[2], 1.0)
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emission
    return mat


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for blk in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(blk):
            blk.remove(item)


def add_sphere(loc, r, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=32, ring_count=16,
                                          location=loc)
    obj = bpy.context.active_object
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj


def add_cylinder(p1, p2, r, mat):
    v1, v2 = Vector(p1), Vector(p2)
    center = (v1 + v2) / 2
    diff = v2 - v1
    length = diff.length
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=length, vertices=16,
                                         location=center)
    obj = bpy.context.active_object
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    if diff.length > 0:
        obj.rotation_mode = 'QUATERNION'
        obj.rotation_quaternion = diff.to_track_quat('Z', 'Y')
    return obj


def add_3d_arrow(p1, p2, mat, shaft_r=0.12, tip_r=0.30, tip_h=0.5):
    """Cylinder shaft + cone tip → 3D arrow."""
    v1, v2 = Vector(p1), Vector(p2)
    diff = v2 - v1
    L = diff.length
    if L <= tip_h:
        # Just a cone
        bpy.ops.mesh.primitive_cone_add(radius1=tip_r, depth=L, vertices=16,
                                         location=(v1 + v2) / 2)
    else:
        # Shaft
        shaft_end = v2 - diff.normalized() * tip_h
        shaft_mid = (v1 + shaft_end) / 2
        shaft_len = (shaft_end - v1).length
        bpy.ops.mesh.primitive_cylinder_add(radius=shaft_r, depth=shaft_len,
                                             vertices=16, location=shaft_mid)
        shaft = bpy.context.active_object
        shaft.data.materials.append(mat)
        bpy.ops.object.shade_smooth()
        if (shaft_end - v1).length > 0:
            shaft.rotation_mode = 'QUATERNION'
            shaft.rotation_quaternion = (shaft_end - v1).to_track_quat('Z', 'Y')
        # Tip
        tip_center = v2 - diff.normalized() * (tip_h / 2)
        bpy.ops.mesh.primitive_cone_add(radius1=tip_r, depth=tip_h, vertices=16,
                                         location=tip_center)
    tip = bpy.context.active_object
    tip.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    if diff.length > 0:
        tip.rotation_mode = 'QUATERNION'
        tip.rotation_quaternion = diff.to_track_quat('Z', 'Y')


def add_vacancy_marker(loc, r, mat):
    """Wireframe sphere = empty vacancy."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 1.2, segments=16, ring_count=8,
                                          location=loc)
    obj = bpy.context.active_object
    obj.data.materials.append(mat)
    # Wireframe modifier
    bpy.ops.object.modifier_add(type='WIREFRAME')
    obj.modifiers["Wireframe"].thickness = 0.08
    return obj


def add_text(loc, text, size=0.6, mat=None, rotation=(math.pi/2, 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rotation)
    obj = bpy.context.active_object
    obj.data.body = text
    obj.data.size = size
    if mat:
        obj.data.materials.append(mat)
    return obj


def setup_camera(target, distance, elev=10, azim=-60):
    azim_r = math.radians(azim)
    elev_r = math.radians(elev)
    cam_x = target[0] + distance * math.cos(elev_r) * math.cos(azim_r)
    cam_y = target[1] + distance * math.cos(elev_r) * math.sin(azim_r)
    cam_z = target[2] + distance * math.sin(elev_r)

    cam_data = bpy.data.cameras.new('Camera')
    cam_obj = bpy.data.objects.new('Camera', cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = (cam_x, cam_y, cam_z)
    direction = Vector(target) - Vector((cam_x, cam_y, cam_z))
    cam_obj.rotation_mode = 'QUATERNION'
    cam_obj.rotation_quaternion = direction.to_track_quat('-Z', 'Y')
    bpy.context.scene.camera = cam_obj
    cam_data.lens = 50


def setup_lighting():
    key = bpy.data.lights.new('Key', 'AREA')
    key.energy = 1000
    key.size = 12
    obj1 = bpy.data.objects.new('Key', key)
    bpy.context.collection.objects.link(obj1)
    obj1.location = (15, -12, 25)

    fill = bpy.data.lights.new('Fill', 'AREA')
    fill.energy = 400
    fill.size = 18
    obj2 = bpy.data.objects.new('Fill', fill)
    bpy.context.collection.objects.link(obj2)
    obj2.location = (-15, 10, 18)

    world = bpy.context.scene.world or bpy.data.worlds.new('World')
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.97, 0.97, 0.97, 1.0)
    bg.inputs['Strength'].default_value = 0.6


def setup_render():
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 128
    sc.cycles.use_denoising = True
    sc.render.resolution_x = 2400
    sc.render.resolution_y = 1600
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'PNG'
    sc.render.film_transparent = False
    try:
        sc.cycles.device = 'GPU'
    except Exception:
        pass


# ────────────────────────────────────────────────────────
def main():
    clear_scene()
    cell, atoms = read_xyz(INPUT_XYZ)
    print(f"  {len(atoms)} atoms read")

    z_ncm_max = max(a[3] for a in atoms if a[0] in ('Ni', 'O'))
    z_cut = z_ncm_max + 0.5
    z_se_min = min(a[3] for a in atoms if a[3] > z_cut)
    z_lo = z_se_min - 6
    z_hi = z_se_min + 7

    materials = {el: make_material(f"mat_{el}", c) for el, c in ELEMENT_COLORS.items()}
    bond_materials = {(s, n): make_material(f"bond_{s}_{n}", (*col, 1.0),
                                            metallic=0.0, roughness=0.5)
                      for s, n, _, col, _, _ in BOND_CUTOFFS}
    arrow_mat = make_material("arrow", (0.60, 0.44, 0.85, 1.0),
                              metallic=0.2, roughness=0.3, emission=1.5)
    vacancy_mat = make_material("vacancy", (0.1, 0.1, 0.1, 1.0),
                                metallic=0.0, roughness=0.5)
    text_mat = make_material("text", (0.1, 0.1, 0.1, 1.0))

    # Atoms
    n_added = 0
    for el, x, y, z in atoms:
        if z < z_lo or z > z_hi:
            continue
        add_sphere((x, y, z), RADII.get(el, 0.8), materials[el])
        n_added += 1
    print(f"  {n_added} atoms drawn")

    # Bonds
    ncm_o = [a for a in atoms if a[0] == 'O' and a[3] <= z_cut]
    n_bonds = 0
    for el, x, y, z in atoms:
        if el not in ('Li', 'S', 'Cl', 'Br') or z < z_lo or z > z_hi:
            continue
        for se_el, ncm_el, cutoff, _, bond_r, _ in BOND_CUTOFFS:
            if se_el != el:
                continue
            for _, ox, oy, oz in ncm_o:
                if oz < z_lo - 1:
                    continue
                d = ((x - ox)**2 + (y - oy)**2 + (z - oz)**2)**0.5
                if d <= cutoff:
                    add_cylinder((x, y, z), (ox, oy, oz), bond_r,
                                 bond_materials[(se_el, ncm_el)])
                    n_bonds += 1
    print(f"  {n_bonds} bonds drawn")

    # Annotations based on style
    xs = [a[1] for a in atoms if z_lo <= a[3] <= z_hi]
    ys = [a[2] for a in atoms if z_lo <= a[3] <= z_hi]
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2

    if STYLE == "comp4_v2":
        # Vacancy + migration arrow (in SE bulk above interface)
        vac_z = z_se_min + 6
        vac_pos = (cx, cy + 1, vac_z)
        add_vacancy_marker(vac_pos, 0.7, vacancy_mat)
        # Migration arrow: vacancy → interface
        arrow_end = (cx + 1, cy + 0.5, z_se_min + 0.7)
        add_3d_arrow(vac_pos, arrow_end, arrow_mat, shaft_r=0.10, tip_r=0.30, tip_h=0.6)

        # 3D Text label: "V_Li" above vacancy
        add_text((vac_pos[0], vac_pos[1] - 1.5, vac_pos[2] + 1.0),
                 "V_Li", size=0.7, mat=text_mat)
        add_text((cx + 4, cy + 1.5, (vac_pos[2] + z_se_min) / 2),
                 "Li migration", size=0.5, mat=text_mat)
        # Title at top
        add_text((cx - 4, cy, z_hi + 1.5),
                 "Li5.4: vacancy-driven Li-rich termination",
                 size=0.7, mat=text_mat)
    else:  # comp1 or other Li6
        add_text((cx - 4, cy, z_hi + 1.5),
                 "Li6: stoichiometric S-rich termination",
                 size=0.7, mat=text_mat)

    # Camera
    cz = (z_lo + z_hi) / 2
    distance = max(max(xs) - min(xs), max(ys) - min(ys), z_hi - z_lo) * 1.5
    setup_camera((cx, cy, cz), distance, elev=8, azim=-55)
    setup_lighting()
    setup_render()

    bpy.context.scene.render.filepath = os.path.abspath(OUTPUT_PNG)
    print(f"Rendering to {OUTPUT_PNG} …")
    bpy.ops.render.render(write_still=True)
    print("DONE.")


if __name__ == "__main__":
    main()
