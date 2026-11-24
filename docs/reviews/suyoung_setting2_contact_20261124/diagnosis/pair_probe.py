"""Isolate pair response with fixed disk quadrature and the setting-2 native projector."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np


GAP_SHA = "95036c52c76fd468ec6f72f586f86fa7a4b4b1bdf2f5c49d55faa56d8c3a4297"
DT16 = 0.0011231835082397789
RADIUS = .05
REL_SPEED = .02


def load(path, digest):
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError("unexpected source: " + path.name)
    spec = importlib.util.spec_from_file_location("pair_probe_" + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scatter(material, centers, cells):
    index = np.arange(-15, 16)
    mesh = np.stack(np.meshgrid(index, index), axis=-1).reshape(-1, 2)
    offsets = mesh[(mesh * mesh).sum(axis=1) <= 15**2] * (RADIUS/15.)
    points = np.concatenate([center + offsets for center in centers])
    owner = np.repeat(np.arange(2), len(offsets))
    grid = 10*cells
    nodes, weights, gradient, _ = material.stencil(points, grid)
    keys = nodes + (grid+1)**2 * owner[:, None]
    unique, slots = np.unique(keys.ravel(), return_inverse=True)
    slots = slots.ravel()
    area = (RADIUS/15.)**2
    mass = area*np.bincount(slots, weights=weights.ravel())
    grad = area*np.column_stack([np.bincount(slots, weights=-gradient[:,:,k].ravel()) for k in range(2)])
    return unique//(grid+1)**2, unique%(grid+1)**2, mass, grad, len(offsets)


def run_case(projector, material, cells, angle_deg, offset, gap, mode, friction, normal_rule):
    angle = np.deg2rad(angle_deg)
    direction = np.array([np.sin(angle), np.cos(angle)])
    center = np.array([.4827, .4541]) + offset
    centers = np.array([center, center+(2*RADIUS+gap)*direction])
    ids, nodes, mass, grad, npoints = scatter(material, centers, cells)
    dt = DT16*16/cells
    u = np.array([.5*REL_SPEED*direction, (-.5 if mode == "approach" else .5)*REL_SPEED*direction])
    v = u[ids].copy()
    before = v.copy()
    if normal_rule == "geometric_control":
        # Zero the supplied gradient to select the native kernel's center-normal fallback.
        grad = np.zeros_like(grad)
    phase = 2*np.pi*np.arange(256)/256
    circle = RADIUS*np.column_stack((np.cos(phase),np.sin(phase)))
    polygons = centers[:,None,:] + circle[None,:,:]
    body = SimpleNamespace(groups=np.repeat([0,1],256), positions=polygons.reshape(-1,2))
    active = mass > 1.e-14*mass.max()
    common = np.intersect1d(nodes[active & (ids==0)], nodes[active & (ids==1)])
    projected = []
    for node in common:
        a, b = np.flatnonzero(active & (nodes==node))
        n = grad[b]/mass[b] - grad[a]/mass[a]
        n = direction if np.linalg.norm(n)<1e-12 else n/np.linalg.norm(n)
        projected.append(float(np.min(polygons[1]@n)-np.max(polygons[0]@n)))
    projector.project(body,dt,ids,nodes,mass,grad,v,centers,friction)
    dv = v-before
    j = [np.sum(mass[ids==i,None]*dv[ids==i],axis=0) for i in (0,1)]
    scale = mass[ids==0].sum()*REL_SPEED
    return dict(cells=cells,angle_deg=angle_deg,origin_shift=offset.tolist(),gap=gap,dt=dt,
                max_relative_travel=REL_SPEED*dt,normal=normal_rule,friction=friction,motion=mode,
                material_points_each=npoints,shared_nodes=len(common),
                nodes_with_negative_projected_gap=sum(x<0 for x in projected),
                minimum_projected_gap=min(projected,default=None),
                changed_nodes=int(np.count_nonzero((ids==0)&(np.linalg.norm(dv,axis=1)>1.e-13))),
                impulse_body_2_xy=j[1].tolist(), axial_impulse_over_mU=float(j[1]@direction/scale),
                vertical_impulse_over_mU=float(j[1][1]/scale), net_impulse_over_mU=float(np.linalg.norm(j[0]+j[1])/scale))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_root",type=Path,help="extracted setting 2 package or checkout containing the three pinned files")
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    root=args.source_root
    gap=load(root/"docs/reviews/suyoung_u6a_gates_20261123/gap_kernel.py",GAP_SHA)
    scripts=root/"history/old_full/prefix/scripts"
    if not scripts.is_dir():
        scripts=root/"scripts"
    material=load(scripts/"dem_suyoung_sf2d_dev.py",gap.PAIR_MATERIAL)
    kernel=load(scripts/"suyoung_multicontact_dev.py",gap.BASE_KERNEL)
    projector=gap.GapProjector(kernel)
    rows=[]
    for cells in (8,12,16,24):
        for angle in (0.,22.5):
            for offset in (np.zeros(2),np.array([.0019,.0027])):
                for friction in (0.,.5):
                    for normal in ("native_gradient","geometric_control"):
                        rows.append(run_case(projector,material,cells,angle,offset,.0005,"approach",friction,normal))
                for gap_size,mode,normal in ((.0005,"comotion","native_gradient"),(.05,"approach","native_gradient"),
                                             (0.,"approach","geometric_control")):
                    rows.append(run_case(projector,material,cells,angle,offset,gap_size,mode,.5,normal))
    summary=dict(cases=len(rows),disks=2,field_runs=0,native_projector_calls=projector.calls,dt16=DT16,
                 pinned_gap_sha256=GAP_SHA,pinned_kernel_sha256=gap.BASE_KERNEL,pinned_material_sha256=gap.PAIR_MATERIAL,
                 rows=rows)
    with args.output.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(summary,stream,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
