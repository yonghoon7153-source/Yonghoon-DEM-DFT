"""render_interface_plotly.py — VESTA-quality 3D atomistic view using Plotly.

Mesh3d spheres with proper depth, lighting, and interactivity.
Output: interactive HTML (rotate/zoom) + static PNG (needs kaleido).

Usage:
    pip install plotly kaleido     # if not already installed
    python3 render_interface_plotly.py file1.xyz [file2.xyz ...]
"""
import sys, re
from pathlib import Path
import numpy as np
from ase.io import read

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    print("Install: pip install plotly kaleido")
    sys.exit(1)

COLORS = {
    'Li': '#9971D9', 'P': '#A8A8A8', 'S': '#FCC830',
    'Cl': '#1FE61F', 'Br': '#A52A2A',
    'Ni': '#5078D2', 'O': '#FF1C00',
}
# Atomic radii in Å (vdW-like)
RADII = {
    'Li': 0.76, 'P': 1.07, 'S': 1.04, 'Cl': 1.02, 'Br': 1.20,
    'Ni': 0.83, 'O': 0.66,
}

BOND_RULES = [
    ('Li', 'O', 2.8, 'cyan',   3.0),
    ('S',  'O', 3.0, 'red',    2.0),
    ('Cl', 'O', 3.2, 'orange', 2.0),
    ('Br', 'O', 3.4, 'purple', 2.0),
]


def clean_name(path):
    stem = Path(path).stem
    cleaned = re.sub(r'^[0-9a-f]{6,8}-', '', stem)
    parts = cleaned.split('_')
    name = parts[0]
    if len(parts) > 1 and ('v1' in parts[1] or 'v2' in parts[1]):
        name = name + '_' + parts[1]
    return name


def sphere_mesh(center, radius, color, resolution=16):
    """Create a sphere mesh for plotly."""
    phi = np.linspace(0, 2 * np.pi, resolution)
    theta = np.linspace(0, np.pi, resolution)
    phi, theta = np.meshgrid(phi, theta)
    x = center[0] + radius * np.sin(theta) * np.cos(phi)
    y = center[1] + radius * np.sin(theta) * np.sin(phi)
    z = center[2] + radius * np.cos(theta)
    return go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, color], [1, color]],
        showscale=False,
        lighting=dict(ambient=0.4, diffuse=0.7, specular=0.5, roughness=0.5),
        lightposition=dict(x=100, y=100, z=200),
        hoverinfo='skip',
    )


def assign_ncm_se(atoms):
    syms = np.array(atoms.get_chemical_symbols())
    z = atoms.positions[:, 2]
    ncm_native = np.isin(syms, ['Ni', 'O'])
    z_ncm_max = z[ncm_native].max() if ncm_native.any() else 0
    z_cut = z_ncm_max + 0.5
    return z <= z_cut, z > z_cut, z_cut


def make_panel_traces(atoms, name, zoom_pad=4.0, radius_scale=1.0):
    """Generate plotly traces for one comp panel."""
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.positions
    ncm_mask, se_mask, z_cut = assign_ncm_se(atoms)

    z_se_min = pos[se_mask, 2].min() if se_mask.any() else z_cut
    z_lo = z_se_min - zoom_pad - 4
    z_hi = z_se_min + zoom_pad + 2
    mask_zoom = (pos[:, 2] >= z_lo) & (pos[:, 2] <= z_hi)

    traces = []
    # Spheres
    for i in np.where(mask_zoom)[0]:
        el = sym[i]
        r = RADII.get(el, 1.0) * radius_scale
        traces.append(sphere_mesh(pos[i], r, COLORS.get(el, '#888')))

    # Bond contacts
    sym_arr = sym
    ncm_O_idx = np.where(ncm_mask & (sym_arr == 'O'))[0]
    counts = {f"{s}-O": 0 for s in ['Li', 'S', 'Cl', 'Br']}
    for i in np.where(se_mask)[0]:
        se_el = sym[i]
        if se_el not in ('Li', 'S', 'Cl', 'Br'): continue
        cutoff = {'Li': 2.8, 'S': 3.0, 'Cl': 3.2, 'Br': 3.4}[se_el]
        for j in ncm_O_idx:
            d = atoms.get_distance(i, j, mic=True)
            if d <= cutoff and z_lo <= pos[i, 2] <= z_hi and z_lo <= pos[j, 2] <= z_hi:
                for rule_se, _, _, color, lw in BOND_RULES:
                    if rule_se == se_el:
                        traces.append(go.Scatter3d(
                            x=[pos[i, 0], pos[j, 0]],
                            y=[pos[i, 1], pos[j, 1]],
                            z=[pos[i, 2], pos[j, 2]],
                            mode='lines',
                            line=dict(color=color, width=lw),
                            hoverinfo='skip', showlegend=False,
                        ))
                        counts[f"{se_el}-O"] += 1
                        break

    return traces, counts, (z_lo, z_hi)


def main(xyz_paths):
    n = len(xyz_paths)
    specs = [[{'type': 'scene'}] * n]
    titles = []
    for path in xyz_paths:
        titles.append(clean_name(path))
    fig = make_subplots(rows=1, cols=n, specs=specs, subplot_titles=titles,
                        horizontal_spacing=0.02)

    for k, path in enumerate(xyz_paths, start=1):
        a = read(path)
        traces, counts, (z_lo, z_hi) = make_panel_traces(a, clean_name(path))
        for t in traces:
            fig.add_trace(t, row=1, col=k)

        # Update scene aspect + view
        scene_id = 'scene' if k == 1 else f'scene{k}'
        fig.update_layout(**{scene_id: dict(
            xaxis_title='x (Å)', yaxis_title='y (Å)', zaxis_title='z (Å)',
            zaxis=dict(range=[z_lo, z_hi]),
            aspectmode='data',
            camera=dict(eye=dict(x=1.5, y=-1.5, z=0.6)),
            bgcolor='white',
        )})

        # Append counts under title
        count_str = "  ".join([f"{k_}={v}" for k_, v in counts.items() if v > 0])
        annot_text = fig.layout.annotations[k - 1].text
        fig.layout.annotations[k - 1].text = f"<b>{annot_text}</b><br>{count_str}"

    fig.update_layout(
        title="SE/NCM interface — 3D atomistic view (Plotly mesh3d)",
        height=750,
        width=420 * n + 100,
        margin=dict(l=10, r=10, t=80, b=10),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )

    out_html = "interface_plotly_3d.html"
    out_png  = "interface_plotly_3d.png"
    fig.write_html(out_html)
    print(f"Saved interactive: {out_html}")
    try:
        fig.write_image(out_png, scale=2)
        print(f"Saved static: {out_png}")
    except Exception as e:
        print(f"[WARN] static PNG export failed (install kaleido): {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 render_interface_plotly.py f1.xyz f2.xyz f3.xyz")
        sys.exit(1)
    main(sys.argv[1:])
