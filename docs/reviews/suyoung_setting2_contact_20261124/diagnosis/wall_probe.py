"""Small setting-2 component controls. No dense trajectory or registered decision is run."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np


HASHES = {
    "material_floor.py": "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b",
    "gap_kernel.py": "95036c52c76fd468ec6f72f586f86fa7a4b4b1bdf2f5c49d55faa56d8c3a4297",
    "suyoung_multicontact_dev.py": "acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645",
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}


def load(path):
    if path.name in HASHES and hashlib.sha256(path.read_bytes()).hexdigest() != HASHES[path.name]:
        raise ValueError("Source mismatch: " + path.name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sources(material_floor, gap_kernel, kernel):
    return (load(material_floor), load(gap_kernel).GapProjector(load(kernel)),
            load(kernel.with_name("dem_suyoung_sf2d_dev.py")))


def marker_impulse(floor, material, g, d, initial=-1., gap=0.):
    pos = np.array([[.425, .15 + gap + d]])
    b = floor.MaterialBoundary([0], [[.425, .15 + gap]])
    _, w, _, rel = material.stencil(pos, g)
    wall = b.bind(pos, w, rel, np.arange(9)[None, :], g, .15, .001)
    mass = w[0]
    v = np.column_stack((np.zeros(9), np.full(9, initial)))
    impulse = wall.project(mass, v)
    exact = max(0., -gap / .001 - initial) / (1 + 4 * (g * d) ** 2)
    np.testing.assert_allclose(impulse, exact, atol=2e-13, rtol=2e-13)
    np.testing.assert_allclose(mass @ (v[:, 1] - initial), impulse, atol=2e-13)
    return dict(grid=g, d=d, gap=gap, incoming=initial, measured_J=impulse, analytic_J=exact)


def make_pair(floor, gap_operator, mu=.5, spacing=0., shared=True, vy=-1., vx=0., masses=(1.,1.)):
    radius = .02
    centers = np.array([[.5,.15+radius], [.5,.15+3*radius+spacing]])
    theta = np.arange(256) * (2*np.pi/256)
    circles = centers[:,None,:] + radius*np.stack((np.cos(theta), np.sin(theta)), axis=1)
    labels = np.repeat([0,1],256)
    geom = floor.MaterialBoundary(labels, circles.reshape(-1,2), labels)
    wall = floor.SurfaceStep(geom, labels[:, None], np.ones((512,1)), .15, .001)
    ids, nodes = np.array([0,1]), np.array([0,0] if shared else [0,1])
    mass = np.asarray(masses, dtype=float)
    grad = np.array([[0.,-1.],[0.,1.]])
    v = np.array([[0.,0.],[vx,vy]])
    def interbody(vel):
        gap_operator.project(geom,.001,ids,nodes,mass,grad,vel,centers,mu)
    return SimpleNamespace(v=v, wall=wall, body=interbody, mass=mass, ids=ids, nodes=nodes,
                           grad=grad, centers=centers, geom=geom, mu=mu, dt=.001)


def split(pair):
    v = pair.v.copy()
    j1 = pair.wall.project(pair.mass, v)
    pair.body(v)
    j2 = pair.wall.project(pair.mass, v)
    return v, j1+j2


def run(floor, gap, material):
    transfer = []
    for grid in (80,120,160,240):
        for offset in (0.,1/480, .25/grid):
            transfer.append(marker_impulse(floor,material,grid,offset))
    transfer += [marker_impulse(floor, material,80,1/480,initial=1.),
                 marker_impulse(floor, material,80,1/480,gap=.002)]
    cases = []
    for name, args, j, high in (
            ("loaded_mu0",dict(mu=0.),.5,-.5),
            ("loaded_mu05",dict(mu=.5),.5,-.5),
            ("double_lower_mass",dict(masses=(2.,1.)),2/3,-1/3),
            ("open_gap",dict(spacing=.002),0.,-1.),
            ("separate_nodes",dict(shared=False),0.,-1.),
            ("separating",dict(vy=1.),0.,1.)):
        pair = make_pair(floor,gap,**args)
        v, impulse = split(pair)
        np.testing.assert_allclose(v[:,1],[0.,high],rtol=2e-13,atol=2e-13)
        np.testing.assert_allclose(impulse,j,atol=2e-13)
        np.testing.assert_allclose(pair.mass @ (v[:,1]-pair.v[:,1]),impulse,atol=2e-13)
        cases.append(dict(case=name, lower_after=v[0,1],upper_after=v[1,1],wall_J=impulse))
    return dict(marker_controls=transfer, splitting_controls=cases)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    for name in ("material_floor","gap_kernel","kernel"):
        p.add_argument(name,type=Path)
    args = p.parse_args()
    print(json.dumps(run(*sources(**vars(args))),indent=2,allow_nan=False))
