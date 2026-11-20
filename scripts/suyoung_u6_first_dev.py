"""CPU development pilot for the first U6(a) contact setting.

Lengths use ten disk diameters per box unit. Stress is in E=10 MPa units,
velocity in sqrt(E/rho) units. This driver does not produce an S/F comparison.
"""
import argparse
import csv
import importlib.util
import json
import math
from pathlib import Path
import sys
import time

import numpy as np


def load_material():
    # Isolate the 3a parameters from callers using the four-disk defaults.
    path = Path(__file__).with_name("dem_suyoung_sf2d_dev.py")
    spec = importlib.util.spec_from_file_location("suyoung_development_material", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.E, module.NU, module.RHO = 1., .45, 1.
    module.MU = module.E / (2 * (1 + module.NU))
    module.LAM = module.E * module.NU / ((1 + module.NU) * (1 - 2 * module.NU))
    module.YIELD = .04 * math.sqrt(2 / 3)
    return module


model = load_material()
DIAMETER = .1
WIDTH = math.sqrt(49 * math.pi * (DIAMETER / 2)**2 / .78)
LO = .15
TARGET = .12
WALL_SPEED = .034 * math.sqrt(model.MU)
PROTOCOL = 'development-mode-1-nodal-gradient'


def seed(cells):
    grid = round(cells / DIAMETER)
    spacing = .5 / grid
    local = np.arange(-cells, cells + 1) * spacing
    offset = np.array([(x, y) for x in local for y in local
                       if x*x + y*y <= (.5 * DIAMETER)**2])
    centers = np.array([(LO + (i + .5) * WIDTH/7, LO + (j + .5) * WIDTH/7)
                        for i in range(7) for j in range(7)])
    x = (centers[:, None, :] + offset[None, :, :]).reshape(-1, 2)
    ids = np.repeat(np.arange(49), len(offset))
    volume = np.full(len(ids), math.pi * (.5 * DIAMETER)**2 / len(offset))
    return x, ids, volume


def first_crossing(p0, p1, h0, h1, target):
    if not p0 < target <= p1:
        return None
    return h0 + (h1 - h0) * (target - p0) / (p1 - p0)


def walls(mass, xy, vel, lid, speed):
    floor = (xy[:, 1] <= LO) & (vel[:, 1] < 0)
    impulse = -float(mass[floor] @ vel[floor, 1])
    vel[floor, 1] = 0.
    top = (xy[:, 1] >= lid) & (vel[:, 1] > speed)
    vel[top, 1] = speed
    vel[(xy[:, 0] <= LO) & (vel[:, 0] < 0), 0] = 0.
    vel[(xy[:, 0] >= LO + WIDTH) & (vel[:, 0] > 0), 0] = 0.
    return impulse


def project_contacts(ids, nodes, mass, grad, vel, centers, friction):
    # Sort active field-node entries once. A node with k fields contributes
    # all k*(k-1)/2 pairs. At fixed field pair all nodes are independent.
    active = np.flatnonzero(mass > 1e-14 * mass.max())
    order = active[np.lexsort((ids[active], nodes[active]))]
    pairs = []
    shift = 1
    while shift < len(order):
        equal = nodes[order[:-shift]] == nodes[order[shift:]]
        if not equal.any():
            break
        pairs.append(np.column_stack((order[:-shift][equal], order[shift:][equal])))
        shift += 1
    if not pairs:
        return
    left, right = np.concatenate(pairs).T
    normal = grad[right] / mass[right, None] - grad[left] / mass[left, None]
    norms = np.linalg.norm(normal, axis=1)
    weak = norms < 1e-12
    normal[weak] = centers[ids[right[weak]]] - centers[ids[left[weak]]]
    norms[weak] = np.linalg.norm(normal[weak], axis=1)
    if np.any(norms <= 0):
        raise ArithmeticError("undefined normal")
    normal /= norms[:, None]
    # With two fields per node a single projection is exact. Handle triple
    # and higher shared nodes in the reference lexicographic order.
    _, inverse, counts = np.unique(nodes[left], return_inverse=True, return_counts=True)
    isolated = counts[inverse] == 1

    def apply(sub):
        a, b = left[sub], right[sub]
        va, vb, _, _ = model.pair_impulse(mass[a], mass[b], vel[a], vel[b], normal[sub], friction)
        vel[a], vel[b] = va, vb

    if isolated.any():
        apply(isolated)
    if not isolated.all():
        groups = ids[left] * len(centers) + ids[right]
        subsets = [(~isolated) & (groups == key) for key in np.unique(groups[~isolated])]
        for _ in range(4):
            for sub in subsets:
                apply(sub)


def advance(x, v, affine, elastic, ids, volume, grid, dt, lid):
    nodes, weights, gradient, offset = model.stencil(x, grid)
    nn = (grid + 1)**2
    key, slots = np.unique((ids[:, None] * nn + nodes).ravel(), return_inverse=True)
    # numpy 2.x altered return_inverse shape in some APIs; keep it explicit.
    slots = slots.reshape(weights.shape)
    weight_mass = volume[:, None] * weights
    transfer = volume[:, None, None] * (affine - dt*4*grid**2*model.stress(elastic))
    momentum = weight_mass[:, :, None]*v[:, None, :] + weights[:, :, None]*np.einsum(
        "pij,pqj->pqi", transfer, offset)
    flat = slots.ravel()

    def collect(a):
        return np.bincount(flat, weights=a.ravel(), minlength=len(key))

    mass = collect(weight_mass)
    if abs(float(mass.sum()) - float(volume.sum())) > 1e-12:
        raise ArithmeticError("mass mismatch")
    mom = np.column_stack([collect(momentum[:, :, k]) for k in range(2)])
    # For W(node - point), the nodal gradient is minus the point gradient.
    grad = np.column_stack([collect(-volume[:, None]*gradient[:, :, k]) for k in range(2)])
    gv = np.divide(mom, mass[:, None], out=np.zeros_like(mom), where=mass[:, None] > 0.)
    node = key % nn
    xy = np.column_stack(np.divmod(node, grid + 1)) / grid
    bottom = walls(mass, xy, gv, lid, -WALL_SPEED)
    count = np.bincount(ids)
    centers = np.column_stack([np.bincount(ids, weights=x[:, k])/count for k in range(2)])
    project_contacts(key // nn, node, mass, grad, gv, centers, .5)
    bottom += walls(mass, xy, gv, lid, -WALL_SPEED)
    velocity = gv[slots]
    v = np.einsum("pq,pqi->pi", weights, velocity)
    affine = 4*grid**2*np.einsum("pq,pqi,pqj->pij", weights, velocity, offset)
    x = x + dt*v
    elastic = model.plastic_project((np.eye(2) + dt*affine) @ elastic)
    pressure = bottom/(dt*WIDTH)
    if not math.isfinite(pressure) or not np.isfinite(x).all():
        raise ArithmeticError("nonfinite")
    return x, v, affine, elastic, pressure


def assess(a, b):
    if any(rec.get('status') != 'TARGET_BRACKETED' or rec.get('cells') != cells
           or rec.get('protocol') != PROTOCOL for rec, cells in ((a, 12), (b, 16))):
        return 'INCOMPLETE'
    if not all(isinstance(r.get('phi_m'), (float, int)) and math.isfinite(r['phi_m'])
               and r['phi_m'] > 0 for r in (a, b)):
        return 'INCOMPLETE'
    return ('WITHIN_DEVELOPMENT_BAND' if abs(a['phi_m'] - b['phi_m']) <= .005
            else 'OUTSIDE_DEVELOPMENT_BAND')


def run(cells, output, budget):
    output.mkdir(exist_ok=False)
    grid = round(cells / DIAMETER)
    dt = .35 / (grid * math.sqrt(model.LAM + 2*model.MU))
    x, ids, volume = seed(cells)
    v = np.zeros_like(x)
    affine = np.zeros((len(x), 2, 2))
    elastic = np.broadcast_to(np.eye(2), affine.shape).copy()
    t0 = time.monotonic()
    p0, h0, count, phi = 0., WIDTH, 0, None
    status = 'TIME_LIMIT'
    with (output/'trace.csv').open('x', encoding='ascii', newline='') as stream:
        trace = csv.writer(stream)
        trace.writerow(['step','time_code','height','bottom_pressure_E','phi_m'])
        trace.writerow([0, 0, WIDTH, 0, float(volume.sum())/WIDTH**2])
        while time.monotonic() - t0 < budget:
            count += 1
            h = WIDTH - dt*count*WALL_SPEED
            if h < .75*WIDTH:
                status = 'TARGET_NOT_REACHED'
                break
            x, v, affine, elastic, pressure = advance(
                x, v, affine, elastic, ids, volume, grid, dt, LO + h)
            trace.writerow([count, count*dt, h, pressure, float(volume.sum())/(WIDTH*h)])
            if count % 25 == 0:
                stream.flush()
            crossing = first_crossing(p0, pressure, h0, h, TARGET)
            if crossing is not None:
                phi = float(volume.sum())/(WIDTH*crossing)
                status = 'TARGET_BRACKETED'
                break
            p0, h0 = pressure, h
    result = dict(protocol=PROTOCOL, label='DEVELOPMENT_ONLY', status=status, cells=cells,
                  disks=49, points=len(ids), dt=dt, steps_attempted=count, phi_m=phi,
                  contact='shared_node_approach', friction=.5, wall_speed=WALL_SPEED,
                  target_E=TARGET, elapsed_s=time.monotonic()-t0, qualified=False)
    (output/'result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='ascii')
    print(json.dumps(result, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--cells', type=int, choices=[12,16])
    modes.add_argument('--summary', action='store_true')
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    if args.summary:
        results = []
        for n in (12,16):
            path = args.out / ('F'+str(n)) / 'result.json'
            results.append(json.loads(path.read_text()) if path.exists() else {})
        result = dict(label='DEVELOPMENT_ONLY', setting=1, assessment=assess(*results),
                      selected_setting=None, u6_qualified=False)
        with (args.out/'comparison.json').open('x', encoding='ascii') as out:
            json.dump(result, out, indent=2)
        print(json.dumps(result))
    else:
        run(args.cells, args.out, 570.)


if __name__ == '__main__':
    main()
