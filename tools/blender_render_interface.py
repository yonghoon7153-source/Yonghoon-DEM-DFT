"""blender_render_interface.py — paper-quality 3D rendering of SE/NCM interface via Blender.

Loads xyz file, builds atomic structure with proper spheres and bonds, sets up
scene (camera, HDRI light, materials), renders with Cycles ray tracer.

Usage:
    blender --background --python blender_render_interface.py -- INPUT.xyz OUTPUT.png

    # Example
    blender --background --python blender_render_interface.py -- \\
        comp4_v2_R1_origin_d1.4_orthogonal.xyz comp4_v2_render.png

Output:
    Paper-quality PNG (3840x2160 by default, Cycles ray-traced, ~1-3 min)

Requires:
    Blender 3.x or 4.x with Python (bpy) — install from blender.org
"""
import sys
import os

# Try import bpy (only works inside Blender)
try:
    import bpy
    import bmesh
    from mathutils import Vector
except ImportError:
    print("This script must be run inside Blender:")
    print("  blender --background --python blender_render_interface.py -- input.xyz output.png")
    sys.exit(1)

# ──────────────────────────────────────────────────────────────────
# Parse CLI args (after `--`)
# ──────────────────────────────────────────────────────────────────
argv = sys.argv
if "--" in argv:
    argv = argv[argv.index("--") + 1:]
else:
    argv = []

if len(argv) < 2:
    INPUT_XYZ = "comp4_v2_R1_origin_d1.4_orthogonal.xyz"
    OUTPUT_PNG = "interface_blender.png"
else:
    INPUT_XYZ = argv[0]
    OUTPUT_PNG = argv[1]

print(f"Input: {INPUT_XYZ}")
print(f"Output: {OUTPUT_PNG}")


# ──────────────────────────────────────────────────────────────────
# Element settings
# ──────────────────────────────────────────────────────────────────
ELEMENT_COLORS = {
    'Li': (0.60, 0.44, 0.85, 1.0),
    'P':  (0.66, 0.66, 0.66, 1.0),
    'S':  (0.99, 0.78, 0.19, 1.0),
    'Cl': (0.12, 0.90, 0.12, 1.0),
    'Br': (0.65, 0.16, 0.16, 1.0),
    'Ni': (0.31, 0.47, 0.82, 1.0),
    'O':  (1.00, 0.11, 0.00, 1.0),
}
# Atomic radii (Angstrom, visual scaling)
RADII = {
    'Li': 0.70, 'P': 0.95, 'S': 1.00, 'Cl': 0.95, 'Br': 1.10,
    'Ni': 0.80, 'O': 0.55,
}

BOND_CUTOFFS = [
    ('Li', 'O', 2.8, (0.10, 0.85, 1.00), 0.15),   # cyan
    ('S',  'O', 3.0, (1.00, 0.15, 0.10), 0.10),   # red
    ('Cl', 'O', 3.2, (1.00, 0.65, 0.10), 0.10),   # orange
    ('Br', 'O', 3.4, (0.60, 0.20, 0.80), 0.10),   # purple
]


# ──────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────
def read_xyz(path):
    """Simple xyz reader. Returns (cell_3x3, list of (element, x, y, z))."""
    import re
    lines = open(path).read().splitlines()
    n = int(lines[0])
    header = lines[1]
    # Extended xyz: Lattice="a1 a2 a3 b1 b2 b3 c1 c2 c3"
    m = re.search(r'Lattice="([^"]+)"', header)
    cell = None
    if m:
        vals = list(map(float, m.group(1).split()))
        cell = [vals[0:3], vals[3:6], vals[6:9]]
    atoms = []
    for line in lines[2:2 + n]:
        parts = line.split()
        if len(parts) >= 4:
            el = parts[0]
            x, y, z = map(float, parts[1:4])
            atoms.append((el, x, y, z))
    return cell, atoms


def make_material(name, color, metallic=0.1, roughness=0.3):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = color
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = metallic
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = roughness
    # Slight glossy
    return mat


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(block):
            block.remove(item)


def add_atom(location, radius, material):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius, segments=32, ring_count=16,
        location=location
    )
    obj = bpy.context.active_object
    obj.data.materials.append(material)
    # Smooth shading
    bpy.ops.object.shade_smooth()
    return obj


def add_bond(p1, p2, radius, material):
    """Cylinder connecting two points."""
    v1 = Vector(p1)
    v2 = Vector(p2)
    center = (v1 + v2) / 2
    diff = v2 - v1
    length = diff.length
    # Create at origin then position/orient
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=length, vertices=12,
        location=center
    )
    obj = bpy.context.active_object
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    # Align to vector
    if diff.length > 0:
        obj.rotation_mode = 'QUATERNION'
        obj.rotation_quaternion = diff.to_track_quat('Z', 'Y')
    return obj


def setup_camera(target=(0, 0, 10), distance=30, elev=15, azim=-45):
    import math
    azim_r = math.radians(azim)
    elev_r = math.radians(elev)
    cam_x = target[0] + distance * math.cos(elev_r) * math.cos(azim_r)
    cam_y = target[1] + distance * math.cos(elev_r) * math.sin(azim_r)
    cam_z = target[2] + distance * math.sin(elev_r)

    cam_data = bpy.data.cameras.new('Camera')
    cam_obj = bpy.data.objects.new('Camera', cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = (cam_x, cam_y, cam_z)

    # Track to target
    direction = Vector(target) - Vector((cam_x, cam_y, cam_z))
    cam_obj.rotation_mode = 'QUATERNION'
    cam_obj.rotation_quaternion = direction.to_track_quat('-Z', 'Y')

    bpy.context.scene.camera = cam_obj
    cam_data.lens = 50  # 50mm focal
    return cam_obj


def setup_lighting():
    # Key light
    light_data = bpy.data.lights.new('Key', type='AREA')
    light_data.energy = 800
    light_data.size = 10
    light_obj = bpy.data.objects.new('Key', light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (15, -10, 20)

    # Fill light
    fill_data = bpy.data.lights.new('Fill', type='AREA')
    fill_data.energy = 300
    fill_data.size = 15
    fill_obj = bpy.data.objects.new('Fill', fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-15, 10, 15)

    # World HDRI-like ambient
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new('World')
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.95, 0.95, 0.95, 1.0)
    bg.inputs['Strength'].default_value = 0.5


def setup_render():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128       # decent quality, fast
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False
    # Performance
    try:
        scene.cycles.device = 'GPU'
    except Exception:
        pass


def distance_pbc(p1, p2, cell):
    """Compute min-image distance between two cartesian points given cell."""
    if cell is None:
        return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)**0.5
    # Convert to fractional, wrap, convert back — approximate for orthogonal-ish cells
    import numpy as np
    cell_arr = np.array(cell)
    inv = np.linalg.inv(cell_arr)
    d = np.array(p2) - np.array(p1)
    frac = inv @ d
    frac -= np.round(frac)
    cart = cell_arr @ frac
    return float(np.linalg.norm(cart))


# ──────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────
def main():
    print("Clearing scene…")
    clear_scene()

    print("Reading xyz…")
    cell, atoms = read_xyz(INPUT_XYZ)
    print(f"  {len(atoms)} atoms read, cell = {cell}")

    # Determine z range and SE/NCM partition
    z_vals = [a[3] for a in atoms]
    z_ncm_max = max(a[3] for a in atoms if a[0] in ('Ni', 'O'))
    z_cut = z_ncm_max + 0.5
    print(f"  z_cut = {z_cut:.3f}")

    # Build materials cache
    materials = {}
    for el, col in ELEMENT_COLORS.items():
        materials[el] = make_material(f"mat_{el}", col,
                                       metallic=0.1 if el != 'Ni' else 0.6,
                                       roughness=0.25)

    bond_materials = {}
    for se_el, ncm_el, cutoff, col, _ in BOND_CUTOFFS:
        bond_materials[(se_el, ncm_el)] = make_material(
            f"bond_{se_el}_{ncm_el}", (*col, 1.0), metallic=0.0, roughness=0.5)

    # Zoom window: ±5 Å around interface
    z_se_min = min(a[3] for a in atoms if a[3] > z_cut)
    z_lo = z_se_min - 6
    z_hi = z_se_min + 7

    print("Adding atoms (zoom around interface)…")
    n_added = 0
    for el, x, y, z in atoms:
        if z < z_lo or z > z_hi:
            continue
        radius = RADII.get(el, 0.8)
        add_atom((x, y, z), radius, materials[el])
        n_added += 1
    print(f"  {n_added} atoms drawn")

    # Bond contacts
    print("Adding bond contacts…")
    n_bonds = 0
    ncm_o = [a for a in atoms if a[0] == 'O' and a[3] <= z_cut]
    for el, x, y, z in atoms:
        if el not in ('Li', 'S', 'Cl', 'Br'):
            continue
        if z < z_lo or z > z_hi:
            continue
        # Find rules
        for se_el, ncm_el, cutoff, col, bond_r in BOND_CUTOFFS:
            if se_el != el:
                continue
            for o_el, ox, oy, oz in ncm_o:
                if oz < z_lo - 1 or oz > z_hi + 1:
                    continue
                d = distance_pbc((x, y, z), (ox, oy, oz), cell)
                if d <= cutoff:
                    add_bond((x, y, z), (ox, oy, oz), bond_r,
                             bond_materials[(se_el, ncm_el)])
                    n_bonds += 1
    print(f"  {n_bonds} bonds drawn")

    # Camera target = center of interface zoom region
    xs = [a[1] for a in atoms if z_lo <= a[3] <= z_hi]
    ys = [a[2] for a in atoms if z_lo <= a[3] <= z_hi]
    cx = (max(xs) + min(xs)) / 2
    cy = (max(ys) + min(ys)) / 2
    cz = (z_lo + z_hi) / 2
    print(f"  Camera target: ({cx:.2f}, {cy:.2f}, {cz:.2f})")

    distance = max(max(xs) - min(xs), max(ys) - min(ys), z_hi - z_lo) * 1.6
    setup_camera(target=(cx, cy, cz), distance=distance, elev=10, azim=-60)
    setup_lighting()
    setup_render()

    bpy.context.scene.render.filepath = os.path.abspath(OUTPUT_PNG)
    print(f"Rendering to {OUTPUT_PNG}…")
    bpy.ops.render.render(write_still=True)
    print("DONE.")


if __name__ == "__main__":
    main()
