"""Thin driver for the Suyoung 2D MPM registrations ① (contact mini) and ②-a (unloading springback).

DEVELOPMENT_ONLY.  This file runs nothing by itself.  It sets up one arm, steps it with the
byte-pinned physics sources (SOURCES, executed unchanged) and records what the registrations
need.  It makes no judgement (J1-J5, H_S, U4 and the dispositions belong to the readers that
come with the execution block).

What the driver adds, and nothing else:
  * geometry: 1-2 disk seeds and their material lower-wall outline, from the same formulas as
    the 49-disk `seed()` (scripts/suyoung_u6_first_dev.py) and `disk_boundary()`
    (material_floor.py), rewritten to take the disk centres; a test requires bit-identical
    output to the originals on the 49-disk bed (8/12/16/24 cells, and 36 with the Q13 guard);
  * a solver view handed to the pinned floor operator: box width, floor height, signed plate
    speed and the arm's contact call (the same role `bind_driver` plays in the setting-2 runs);
  * the registered elastic material E (reg1 §2): a private material copy with the return-
    mapping threshold YIELD = inf (the only non-geometry private constant);
  * the plate schedule: reg1 = monotone press to the registered end displacement; reg2-a =
    press until Φ_m first reaches 0.95, then the plate reversed for 0.06 model length;
  * observers wrapped around two private functions (`_other_walls` of the floor module and
    `_pair_impulse` of the contact kernel).  They read the top-plate impulse, side-wall hits and
    two-field normal impulses and return the original results; a test requires bit-identical
    states with and without them.

Modes: CHECK_ONLY (source hashes, plan table, seed hashes; no MPM step), SMOKE (a few steps of
the smallest arm, wiring only), RUN (one arm, for the execution block).
"""
import argparse
import csv
from dataclasses import asdict, dataclass
import hashlib
import io
import itertools
import json
import math
import os
from pathlib import Path
import platform
import sys
import tempfile
import time
from types import ModuleType, SimpleNamespace

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
LABEL = "DEVELOPMENT_ONLY"
SOURCES = {
    "scripts/dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
    "scripts/suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "scripts/suyoung_multicontact_dev.py": "acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645",
    "scripts/suyoung_u6b_dev.py": "50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762",
    "docs/reviews/suyoung_floor_contact_20261123/material_floor.py":
        "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b",
    "docs/reviews/suyoung_u6a_gates_20261123/gap_kernel.py":
        "95036c52c76fd468ec6f72f586f86fa7a4b4b1bdf2f5c49d55faa56d8c3a4297",
    "docs/reviews/suyoung_u6b_setting2_20261123/setting2_u6b.py":
        "8b25718d07a8e3dd676cee286a14fac4312ab74e1514ea29f73ea853f7268e08",
}
FLOOR_PATH = "docs/reviews/suyoung_floor_contact_20261123/material_floor.py"
KERNEL_PATH = "scripts/suyoung_multicontact_dev.py"
# Native 49-disk inputs already pinned by the earlier runners (fine_floor.py 12/24,
# matched_controls.py 16, q13.py 36): points, time step, sha256 of (x, ids, volume).
BED_PINS = {
    12: (21609, 0.001497578010986372,
         ("499e377a027ae742a609a8612d2eb324e00fcc7923ba8499aa041adbe5749b72",
          "d2a45cd7a3dfd8bdce398c2f2675dfa8c66ca16f278cab46f8dc16a1c01e3f5a",
          "1a9e9a6bfc902a4a0e6552ac9c83974b7715eabca9588111f8372c783457869d")),
    16: (39053, 0.0011231835082397789,
         ("ce12e262721141b2c4fc36cc72733686055a9e22ce62a8cc733a1e2ad591858a",
          "da5560998c5a66797d7928279d5b43f6e26cb8432aac52a37f99d7cef5a3d7b2",
          "06f4c3ce49ffece1d401bdcae453605728c4ba0e7731b4c2c6027e337cdc88b4")),
    24: (87857, 0.000748789005493186,
         ("09b0d2c662fa9efac2c59329c007c5c548fff49a8e0cf18712cca5c1daad20c1",
          "b1123a2bae8daf7e7bd45e7042443e86d3eefc21f7f2b605c248e88b8eaef2bc",
          "85b4c8db8d8daf34ea4f8f91f49f5d7edcbf1457bcbc9c08ea00872b9e15b242")),
    36: (198597, 0.0004991926703287907,
         ("9f8933b9cb8016a4e173d74109bf48f4d87507f07e7c3e78520ca22b47ad035e",
          "b65eb9e75f7ec625d4ec6888dc5fd344b34b3393c5bbd2424ecf3d9c6efe4a3d",
          "5c7b447c3b83887d1a044237cc37bfdd00ff20dfb676010b7827869526f9a4b4")),
}
WSL_ENVIRONMENT = ("3.12.3", "2.5.2")
THREAD_VARIABLES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")

# reg1 §2 · §4-4 · §7 and reg2 §3.
MINI_LEFT, MINI_RIGHT, MINI_X = .15, .85, .5
EPS_MAX = .20
PHI_STOP = .95
UNLOAD_TRAVEL = .06
LATERAL_LIMIT_D = .01
PENETRATION_LIMIT = 2e-12
REG1_CELLS = (8, 16, 24, 32, 48)
REG2_CELLS = (12, 16, 24, 36)
REG1_FIXED_S = (.005, .015)
REG1_RATE_S = {"S": (4.7e-6, 4.9e-6), "F": (3.0e-6, 3.6e-6)}
REG2_STEP_S = {"S": {12: .089, 16: .169, 24: .422, 36: .938}, "F": {12: .079, 16: .134, 24: .286, 36: .607}}

# Registered numbers, transcribed for the CHECK_ONLY comparison (reg1 §3 table, §7; reg2 §3-1, §3-5, §3-6).
REGISTERED_REG1 = (
    ("G1", "PLATE", ("P",), 1, (454, 908, 1361, 1815, 2722), (600, 600, 600, 600, 600)),
    ("G1", "PLATE", ("P", "E"), 4, (1815, 3630, 5444, 7259, 10888), (600, 600, 600, 600, 1380)),
    ("G2", "S", ("P",), 1, (908, 1815, 2722, 3630, 5444), (600, 600, 600, 600, 1440)),
    ("G2", "F2", ("P",), 1, (908, 1815, 2722, 3630, 5444), (600, 600, 600, 600, 1140)),
    ("G2", "S", ("P", "E"), 4, (3630, 7259, 10888, 14517, 21775), (600, 600, 1080, 2040, 5640)),
    ("G2", "F2", ("P", "E"), 4, (3630, 7259, 10888, 14517, 21775), (600, 600, 960, 1680, 4380)),
    ("G2", "F1", ("P",), 4, (3630, 7259, 10888, 14517, 21775), (600, 600, 960, 1680, 4380)),
)
REGISTERED_POINTS_PER_DISK = (197, 797, 1793, 3209, 7213)
REGISTERED_REG1_TOTALS = dict(cpu_low_h=3.3, cpu_high_h=4.8, wall2_low_h=1.7, wall2_high_h=2.4,
                              cpu_high_without_24_h=4.2, longest_limit_s=5640)
REGISTERED_REG2_LIMIT_H = {("S", 36): 10, ("F2", 36): 6.5, ("C1", 36): 6.5, ("S", 24): 3, ("F2", 24): 2,
                           ("C1", 24): 2, ("S", 16): 1, ("F2", 16): 1, ("C1", 16): 1, ("S", 12): .5,
                           ("F2", 12): .5, ("C1", 12): .5}
REGISTERED_REG2_REPORT_LIMIT_H = {"S": 6, "F2": 4}
REGISTERED_REG2_TOTALS = dict(steps_36=18633, height_at_stop=.57672, cpu_h=16.0, wall2_h=8.1, report_wall2_h=2.4)

COLUMNS = ("step", "time_code", "height", "bottom_pressure_E", "phi_m", "phase", "u",
           "bottom_force", "top_force", "bottom_MPa", "top_MPa", "kinetic_energy", "momentum_y",
           "momentum_residual", "upper_center_x", "upper_dx_over_D", "sigma_yy_avg_MPa",
           "interfield_normal_impulse", "two_field_nodes", "multi_field_nodes", "side_wall_hits",
           "floor_max_penetration")
F_CONTACTS = ("F1", "F2", "C1")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def array_sha(*arrays):
    return [sha(np.ascontiguousarray(a, dtype="<i8" if a.dtype.kind in "iu" else "<f8").tobytes(order="C"))
            for a in arrays]


def write_json(path, value):
    with Path(path).open("x", encoding="ascii", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def verify_sources(root):
    """Read and hash every pinned source; refuse on a missing file or a byte change."""
    raw = {}
    for relative, pin in SOURCES.items():
        path = Path(root) / relative
        if not path.is_file():
            raise ValueError("missing pinned source: " + relative)
        data = path.read_bytes()
        if sha(data) != pin:
            raise ValueError("pinned source bytes changed: " + relative)
        raw[relative] = data
    return raw


@dataclass(frozen=True)
class Arm:
    reg: str
    name: str
    geometry: str        # G1 | G2 | BED
    contact: str         # PLATE | S | F2 | F1 | C1
    material: str        # P | E
    cells: int
    load_div: int        # pressing speed = V0 / load_div
    unload_div: int | None = None   # reg2: reversed plate speed = V0 / unload_div


def reg1_arms():
    rows = []
    for geometry, contact, materials, div, _, _ in REGISTERED_REG1:
        for material in materials:
            for cells in REG1_CELLS:
                speed = "V0" if div == 1 else f"V{div}"
                rows.append(Arm("reg1", f"R1-{geometry}-{contact}-{material}-{speed}-{cells:02d}",
                                geometry, contact, material, cells, div))
    return rows


def reg2_arms():
    rows = [Arm("reg2", f"R2-BED-{c}-P-V0-{n:02d}", "BED", c, "P", n, 1, 1) for c in ("S", "F2", "C1")
            for n in REG2_CELLS]
    rows += [Arm("reg2", f"R2-BED-{c}-P-U4-24", "BED", c, "P", 24, 1, 4) for c in ("S", "F2")]
    return rows


def all_arms():
    return reg1_arms() + reg2_arms()


def disk_offsets(cells, diameter):
    grid = round(cells / diameter)
    spacing = .5 / grid
    local = np.arange(-cells, cells + 1) * spacing
    return np.array([(x, y) for x in local for y in local if x*x + y*y <= (.5 * diameter)**2])


def seed_disks(cells, centers, diameter):
    """`seed()` of scripts/suyoung_u6_first_dev.py with the disk centres as input."""
    offset = disk_offsets(cells, diameter)
    centers = np.asarray(centers, dtype=float)
    x = (centers[:, None, :] + offset[None, :, :]).reshape(-1, 2)
    ids = np.repeat(np.arange(len(centers)), len(offset))
    volume = np.full(len(ids), math.pi * (.5 * diameter)**2 / len(offset))
    return x, ids, volume


def bed_seed_centers(lo, width):
    """The centre expression of the original 49-disk `seed()`."""
    return np.array([(lo + (i + .5) * width/7, lo + (j + .5) * width/7) for i in range(7) for j in range(7)])


def bed_boundary_centers(lo, width):
    """The centre expression of the original `disk_boundary()` (it differs from seed() in rounding)."""
    return np.array([lo + (np.array(divmod(body, 7)) + .5)*(width/7) for body in range(49)])


def disk_boundary(floor, diameter, x, ids, centers):
    """`disk_boundary()` of material_floor.py for any number of disks with given centres."""
    centers = np.asarray(centers, dtype=float)
    require(np.array_equal(np.unique(ids), np.arange(len(centers))), "physical disk IDs 0..n-1 expected")
    vertices = floor.DISK_BOUNDARY_VERTICES
    theta = 2.*np.pi*np.arange(vertices)/vertices
    circle = diameter*.5*np.column_stack((np.cos(theta), np.sin(theta)))
    positions, owners = [], []
    for body in range(len(centers)):
        surface = centers[body] + circle
        idx = np.flatnonzero(ids == body)
        delta = surface[:, None, :] - x[idx][None, :, :]
        closest = np.argmin(np.einsum("sqi,sqi->sq", delta, delta), axis=1)
        positions.append(surface)
        owners.append(idx[closest])
    owners = np.concatenate(owners)
    return floor.MaterialBoundary(owners, np.concatenate(positions), ids[owners])


def lpt_two_cores(seconds):
    load = [0., 0.]
    for t in sorted(seconds, reverse=True):
        load[load.index(min(load))] += t
    return max(load)


class Engine:
    """Pinned sources and the arithmetic every arm shares (no MPM step)."""

    def __init__(self, root=REPO):
        self.root = Path(root).resolve()
        self.raw = verify_sources(self.root)
        self.u6b = self.fresh("scripts/suyoung_u6b_dev.py", "registration_u6b_driver")
        self.solver = self.fresh("scripts/suyoung_u6_first_dev.py", "registration_u6_solver")
        self.gap = self.fresh("docs/reviews/suyoung_u6a_gates_20261123/gap_kernel.py", "registration_gap_kernel")
        self.s2 = self.fresh("docs/reviews/suyoung_u6b_setting2_20261123/setting2_u6b.py", "registration_setting2_s")
        s = self.solver
        require(s.LO == MINI_LEFT and s.DIAMETER == .1 and self.u6b.THETA_MPA == .008 and self.u6b.E_MPA == 10.,
                "pinned solver constants")
        self.const = SimpleNamespace(
            D=s.DIAMETER, LO=s.LO, BED_WIDTH=s.WIDTH, W7=s.WIDTH/7, GP=(s.WIDTH/7 - s.DIAMETER)/2,
            V0=s.WALL_SPEED, CP=math.sqrt(s.model.LAM + 2*s.model.MU), MINI_WIDTH=MINI_RIGHT - MINI_LEFT,
            THETA_MPA=self.u6b.THETA_MPA, E_MPA=self.u6b.E_MPA)
        self._bed, self._plans = {}, {}

    def verify(self):
        require(verify_sources(self.root) == self.raw, "pinned sources changed after loading")

    def fresh(self, relative, name):
        """Execute verified bytes, unchanged, as a new private module."""
        path = self.root / relative
        module = ModuleType(name)
        module.__file__ = str(path)
        exec(compile(self.raw[relative], str(path), "exec"), module.__dict__)
        return module

    def bed(self, cells):
        if cells not in self._bed:
            self._bed[cells] = self.solver.seed(cells)
        return self._bed[cells]

    def dt(self, cells):
        view = SimpleNamespace(DIAMETER=self.const.D, model=self.solver.model)
        return self.u6b.step_size(view, cells)

    def geometry(self, arm):
        c = self.const
        if arm.geometry == "BED":
            return dict(kind="BED", disks=49, rows=7, centers=None,
                        boundary_centers=bed_boundary_centers(c.LO, c.BED_WIDTH), h0=c.BED_WIDTH, lo=c.LO,
                        width=c.BED_WIDTH, upper=None, u_end=None, u_geo=None)
        require(arm.geometry in ("G1", "G2"), "unknown geometry")
        rows = 1 if arm.geometry == "G1" else 2
        centers = np.array([(MINI_X, c.LO + (j + .5)*(c.BED_WIDTH/7)) for j in range(rows)])
        return dict(kind=arm.geometry, disks=rows, rows=rows, centers=centers, boundary_centers=centers,
                    h0=rows*c.W7, lo=c.LO, width=c.MINI_WIDTH, upper=rows - 1,
                    u_end=rows*(EPS_MAX*c.D + 2*c.GP), u_geo=2*rows*c.GP)

    def load_steps(self, cells, speed, total):
        width, dt = self.const.BED_WIDTH, self.dt(cells)
        k = 0
        while True:
            k += 1
            height = width - dt*k*speed
            require(height > .5*width, "no Φ_m stop before half height")
            if total / (width*height) >= PHI_STOP:
                return k

    def plan(self, arm):
        if arm not in self._plans:
            self._plans[arm] = self._plan(arm)
        return dict(self._plans[arm])

    def _plan(self, arm):
        c = self.const
        dt = self.dt(arm.cells)
        speed = c.V0 / arm.load_div
        per_disk = len(disk_offsets(arm.cells, c.D))
        kind = "S" if arm.contact == "S" else "F"
        out = dict(name=arm.name, reg=arm.reg, cells=arm.cells, grid=round(arm.cells / c.D), dt=dt,
                   load_speed=speed, v_over_cP=speed / c.CP, rate_kind=kind)
        if arm.geometry == "BED":
            unload = c.V0 / arm.unload_div
            n_load = self.load_steps(arm.cells, speed, float(self.bed(arm.cells)[2].sum()))
            n_unload = math.ceil(UNLOAD_TRAVEL / (unload*dt))
            steps = n_load + n_unload
            per_step = REG2_STEP_S[kind].get(arm.cells)
            est = None if per_step is None else steps*per_step
            out.update(points=49*per_disk, unload_speed=unload, unload_v_over_cP=unload / c.CP, n_load=n_load,
                       n_unload=n_unload, steps=steps, est_low_s=est, est_high_s=est,
                       limit_s=None if est is None else math.ceil(2*est/1800)*1800,
                       height_at_stop_nominal=49*math.pi*(c.D/2)**2 / (c.BED_WIDTH*PHI_STOP))
            return out
        g = self.geometry(arm)
        points = g["disks"]*per_disk
        steps = math.ceil(g["u_end"] / (speed*dt))
        low = steps*(REG1_FIXED_S[0] + points*REG1_RATE_S[kind][0])
        high = steps*(REG1_FIXED_S[1] + points*REG1_RATE_S[kind][1])
        out.update(points=points, unload_speed=None, n_load=steps, n_unload=0, steps=steps, u_end=g["u_end"],
                   est_low_s=low, est_high_s=high, limit_s=max(600, math.ceil(3*high/60)*60))
        return out

    def schedule(self, arm, total, n_load=None, n_unload=None):
        """(step, phase, plate height above the floor, plate speed handed to the plate operator)."""
        c = self.const
        dt, speed = self.dt(arm.cells), c.V0 / arm.load_div
        if arm.geometry != "BED":
            h0 = self.geometry(arm)["h0"]
            count = self.plan(arm)["steps"] if n_load is None else n_load
            return [(k, "LOAD", h0 - dt*k*speed, speed) for k in range(1, count + 1)]
        width = c.BED_WIDTH
        rows, k = [], 0
        while n_load is None or k < n_load:
            k += 1
            height = width - dt*k*speed
            rows.append((k, "LOAD", height, speed))
            if n_load is None and total / (width*height) >= PHI_STOP:
                break
            require(height > .5*width, "no Φ_m stop before half height")
        h_u = rows[-1][2] if rows else width
        unload = c.V0 / arm.unload_div
        count = math.ceil(UNLOAD_TRAVEL / (unload*dt)) if n_unload is None else n_unload
        rows += [(k + m, "UNLOAD", h_u + dt*m*unload, -unload) for m in range(1, count + 1)]
        return rows

    def source_record(self):
        return {path: sha(raw) for path, raw in self.raw.items()}


def plan_totals(engine, arms):
    plans = [engine.plan(a) for a in arms]
    low = [p["est_low_s"] for p in plans]
    high = [p["est_high_s"] for p in plans]
    return dict(arms=len(arms), cpu_low_h=sum(low)/3600, cpu_high_h=sum(high)/3600,
                wall2_low_h=lpt_two_cores(low)/3600, wall2_high_h=lpt_two_cores(high)/3600,
                longest_limit_s=max(p["limit_s"] for p in plans))


def elastic_material(solver):
    """reg1 §2 material E: the pinned 3a material with the return-mapping threshold at infinity."""
    material = solver.load_material()
    material.YIELD = math.inf
    return material


class Observer:
    """Reads impulses around the pinned operators; never writes a velocity."""

    def __init__(self):
        self.wall_speeds, self.lids, self.pairs = [], [], []
        self.other_walls_calls = self.contact_calls_total = 0
        self.begin(False)

    def begin(self, capture):
        self.dv, self.side, self.mass, self.contact_calls = [], 0, None, 0
        self.jn, self.two, self.multi, self.capture = 0., 0, 0, capture


def pair_record(ids, nodes, mass, dv):
    """Per disk pair at shared nodes: 2-field node count, ≥3-field node count, |impulse| sum at 2-field nodes."""
    active = np.flatnonzero(mass > 1e-14 * mass.max())
    order = active[np.argsort(nodes[active], kind="stable")]
    _, starts, counts = np.unique(nodes[order], return_index=True, return_counts=True)
    table = {}
    for start, count in zip(starts, counts):
        if count < 2:
            continue
        rows = order[start:start + count]
        bodies = sorted(int(b) for b in ids[rows])
        if count == 2:
            entry = table.setdefault(tuple(bodies), [0, 0, 0.])
            entry[0] += 1
            row = rows[int(np.argmax(ids[rows]))]
            entry[2] += float(np.linalg.norm(mass[row]*dv[row]))
        else:
            for pair in itertools.combinations(bodies, 2):
                table.setdefault(pair, [0, 0, 0.])[1] += 1
    return [dict(pair=list(p), two_field_nodes=a, multi_field_nodes=b, two_field_impulse_norm_sum=s)
            for p, (a, b, s) in sorted(table.items())]


class ArmRunner:
    """One arm: seeds, outline, private floor module, contact call, view; `step()` advances one step."""

    def __init__(self, engine, arm, observe=True):
        engine.verify()
        self.engine, self.arm = engine, arm
        c = engine.const
        g = engine.geometry(arm)
        self.geometry = g
        require(arm.contact in ("PLATE", "S", "F1", "F2", "C1") and arm.material in ("P", "E"), "arm kind")
        require((arm.geometry == "G1") == (arm.contact == "PLATE"), "plate-only contact is the one-disk arm")
        self.material = engine.solver.model if arm.material == "P" else elastic_material(engine.solver)
        width = c.BED_WIDTH if arm.geometry == "BED" else c.MINI_WIDTH
        self.view = SimpleNamespace(model=self.material, LO=c.LO, WIDTH=width, WALL_SPEED=c.V0 / arm.load_div,
                                    DIAMETER=c.D, project_contacts=self.contact)
        self.grid = round(arm.cells / c.D)
        self.dt = engine.u6b.step_size(self.view, arm.cells)
        if arm.geometry == "BED":
            self.x, self.ids, self.volume = engine.bed(arm.cells)
        else:
            self.x, self.ids, self.volume = seed_disks(arm.cells, g["centers"], c.D)
        self.seed_sha256 = array_sha(self.x, self.ids, self.volume)
        self.fields = engine.u6b.field_ids("S" if arm.contact == "S" else "F", self.ids)
        self.floor = engine.fresh(FLOOR_PATH, "registration_floor_" + arm.name.replace("-", "_"))
        self.boundary = disk_boundary(self.floor, c.D, self.x, self.ids, g["boundary_centers"])
        if arm.contact == "S":
            engine.s2.merge_surface_fields(self.boundary, self.ids)
        self.boundary_sha256 = array_sha(self.boundary.owners, self.boundary.positions, self.boundary.groups)
        self.kernel = self.projector = None
        if arm.contact in F_CONTACTS:
            self.kernel = engine.fresh(KERNEL_PATH, "registration_kernel_" + arm.name.replace("-", "_"))
            if arm.contact in ("F2", "C1"):
                self.projector = engine.gap.GapProjector(self.kernel)
        self.observer = Observer() if observe else None
        if observe:
            self.install_observers()
        self.advance = self.floor.make_advance(self.view, arm.cells, boundary=self.boundary)
        self.v = np.zeros_like(self.x)
        self.affine = np.zeros((len(self.x), 2, 2))
        self.elastic = np.broadcast_to(np.eye(2), self.affine.shape).copy()
        self.total = float(self.volume.sum())
        self.momentum = 0.
        self.upper = None if g["upper"] is None else self.ids == g["upper"]
        self.upper_x0 = None if self.upper is None else float(np.mean(self.x[self.upper, 0]))

    def install_observers(self):
        o = self.observer
        original_walls = self.floor._other_walls

        def observed_walls(solver, xy, gv, lid):
            before = gv.copy()
            original_walls(solver, xy, gv, lid)
            o.dv.append(gv[:, 1] - before[:, 1])
            o.side += int(np.count_nonzero(gv[:, 0] != before[:, 0]))
            o.wall_speeds.append(solver.WALL_SPEED)
            o.lids.append(lid)
            o.other_walls_calls += 1
        observed_walls.__wrapped__ = original_walls
        self.floor._other_walls = observed_walls
        target = None if self.kernel is None else (self.kernel if self.projector is None else self.projector.derived)
        if target is not None:
            original_pair = target._pair_impulse

            def observed_pair(*args):
                result = original_pair(*args)
                o.jn += float(np.sum(result[2]))
                return result
            observed_pair.__wrapped__ = original_pair
            target._pair_impulse = observed_pair

    def contact(self, ids, nodes, mass, grad, gv, centers, friction):
        """Bound as the view's project_contacts; the floor operator always passes friction 0.5."""
        require(friction == .5, "floor operator friction argument")
        o, kind = self.observer, self.arm.contact
        before = None
        if o is not None:
            o.mass = mass
            o.contact_calls += 1
            o.contact_calls_total += 1
            if kind in F_CONTACTS:
                active = mass > 1e-14 * mass.max()
                _, counts = np.unique(nodes[active], return_counts=True)
                o.two += int(np.count_nonzero(counts == 2))
                o.multi += int(np.count_nonzero(counts >= 3))
                if o.capture:
                    before = gv.copy()
        if kind in ("PLATE", "S"):
            self.engine.s2.single_field_contact(ids, nodes, mass, grad, gv, centers, friction)
        elif kind == "F1":
            self.kernel.project_contacts(ids, nodes, mass, grad, gv, centers, friction)
        else:
            require(self.advance.boundary is self.boundary, "contact outline is the floor outline")
            self.projector.project(self.boundary, self.dt, ids, nodes, mass, grad, gv, centers,
                                   friction if kind == "F2" else 0.)
        if before is not None:
            o.pairs = pair_record(ids, nodes, mass, gv - before)

    def step(self, k, phase, height, wall_speed, capture_pairs=False):
        o = self.observer
        if o is not None:
            o.begin(capture_pairs)
        self.view.WALL_SPEED = wall_speed
        x, v, affine, elastic, pressure = self.advance(self.x, self.v, self.affine, self.elastic, self.fields,
                                                       self.volume, self.grid, self.dt, self.view.LO + height)
        require(math.isfinite(pressure) and pressure >= 0., "invalid bottom reaction")
        self.x, self.v, self.affine, self.elastic = x, v, affine, elastic
        if o is None:
            return pressure, None
        return pressure, self.record(k, phase, height, pressure)

    def record(self, k, phase, height, pressure):
        o, c, dt = self.observer, self.engine.const, self.dt
        require(len(o.dv) == 2 and o.contact_calls == 1, "observer call counts")
        top_impulse = sum(float(o.mass @ d) for d in o.dv)
        top_force = -top_impulse / dt
        bottom_force = pressure * self.view.WIDTH
        momentum = float(self.volume @ self.v[:, 1])
        residual = (momentum - self.momentum) - (pressure*dt*self.view.WIDTH + top_impulse)
        self.momentum = momentum
        bed = self.arm.geometry == "BED"
        rec = dict(step=k, time_code=k*dt, height=height, bottom_pressure_E=pressure,
                   phi_m=self.total / (self.view.WIDTH*height) if bed else None, phase=phase,
                   u=self.geometry["h0"] - height, bottom_force=bottom_force, top_force=top_force,
                   bottom_MPa=pressure*c.E_MPA if bed else bottom_force / c.D * c.E_MPA,
                   top_MPa=(top_force / self.view.WIDTH if bed else top_force / c.D) * c.E_MPA,
                   kinetic_energy=.5*float(self.volume @ np.einsum("pi,pi->p", self.v, self.v)),
                   momentum_y=momentum, momentum_residual=residual, upper_center_x=None, upper_dx_over_D=None,
                   sigma_yy_avg_MPa=None, interfield_normal_impulse=None, two_field_nodes=None,
                   multi_field_nodes=None, side_wall_hits=o.side,
                   floor_max_penetration=self.advance.audit["max_penetration"])
        if not bed:
            cx = float(np.mean(self.x[self.upper, 0]))
            rec.update(upper_center_x=cx, upper_dx_over_D=(cx - self.upper_x0) / c.D)
        if self.arm.geometry == "G1":
            # reg1 J5 reports σ_b next to the volume-average σ_yy of the disk (one-disk arms only).
            # stress() is the Kirchhoff stress; current volume = V0·J, so the average is ΣV0τ_yy / ΣV0J.
            tau = self.material.stress(self.elastic)
            rec["sigma_yy_avg_MPa"] = (float(self.volume @ tau[:, 1, 1]) /
                                       float(self.volume @ np.linalg.det(self.elastic)) * c.E_MPA)
        if self.arm.contact in F_CONTACTS:
            rec.update(interfield_normal_impulse=o.jn, two_field_nodes=o.two, multi_field_nodes=o.multi)
        return rec

    def initial_record(self):
        bed = self.arm.geometry == "BED"
        h0 = self.geometry["h0"]
        rec = {k: 0 for k in COLUMNS}
        rec.update(height=h0, phase="INITIAL", phi_m=self.total / h0**2 if bed else None,
                   upper_center_x=self.upper_x0, upper_dx_over_D=None if bed else 0,
                   sigma_yy_avg_MPa=0 if self.arm.geometry == "G1" else None)
        if self.arm.contact not in F_CONTACTS:
            rec.update(interfield_normal_impulse=None, two_field_nodes=None, multi_field_nodes=None)
        return rec


class Monitors:
    """reg1 §4-4 technical watch: recorded per step; violations mark the arm, the run continues."""

    def __init__(self, mini):
        self.mini = mini
        self.max_dx, self.first_dx = 0., None
        self.side_total, self.first_side = 0, None
        self.max_pen, self.max_res = 0., 0.

    def update(self, k, rec):
        dx = rec.get("upper_dx_over_D")
        if dx is not None:
            self.max_dx = max(self.max_dx, abs(dx))
            if abs(dx) > LATERAL_LIMIT_D and self.first_dx is None:
                self.first_dx = k
        hits = rec["side_wall_hits"]
        self.side_total += hits
        if hits and self.first_side is None:
            self.first_side = k
        self.max_pen = max(self.max_pen, rec["floor_max_penetration"])
        self.max_res = max(self.max_res, abs(rec["momentum_residual"]))

    def summary(self):
        reasons = []
        if self.mini and self.first_dx is not None:
            reasons.append("LATERAL_OFFSET")
        if self.mini and self.first_side is not None:
            reasons.append("SIDE_WALL_CONTACT")
        if self.max_pen > PENETRATION_LIMIT:
            reasons.append("FLOOR_PENETRATION")
        return dict(lateral_limit_D=LATERAL_LIMIT_D if self.mini else None,
                    max_abs_upper_dx_over_D=self.max_dx if self.mini else None,
                    first_lateral_violation_step=self.first_dx, side_wall_hits_total=self.side_total,
                    first_side_wall_step=self.first_side, side_walls_watched=self.mini,
                    penetration_limit=PENETRATION_LIMIT, max_floor_penetration=self.max_pen,
                    max_abs_momentum_residual=self.max_res, technical_hold_reasons=reasons)


def environment():
    try:
        affinity = sorted(os.sched_getaffinity(0))
    except AttributeError:
        affinity = None
    return dict(python=platform.python_version(), numpy=np.__version__, platform=platform.platform(),
                wsl_target=dict(python=WSL_ENVIRONMENT[0], numpy=WSL_ENVIRONMENT[1]),
                matches_wsl_target=(platform.python_version(), np.__version__) == WSL_ENVIRONMENT,
                threads={k: os.environ.get(k) for k in THREAD_VARIABLES}, affinity=affinity)


def csv_value(value):
    return "" if value is None else value


def read_receipt(out, result):
    """Re-read the written trace and recompute the recorded summaries from it."""
    raw = (out / "trace.csv").read_bytes()
    rows = list(csv.reader(io.StringIO(raw.decode("ascii"), newline="")))
    require(tuple(rows[0]) == COLUMNS, "trace columns")
    data = rows[1:]
    require(len(data) == result["steps_done"] + 1 and [int(r[0]) for r in data] == list(range(len(data))),
            "trace rows")
    index = {name: i for i, name in enumerate(COLUMNS)}
    receipt = dict(label=LABEL, trace_sha256=sha(raw), rows=len(data), first_force_u_on=None,
                   load_steps_in_trace=sum(r[index["phase"]] == "LOAD" for r in data),
                   unload_steps_in_trace=sum(r[index["phase"]] == "UNLOAD" for r in data))
    if result["registration"] == "reg1":
        for r in data[1:]:
            if float(r[index["bottom_MPa"]]) > result["first_force"]["threshold_MPa"]:
                receipt["first_force_u_on"] = float(r[index["u"]])
                break
    require(receipt["trace_sha256"] == result["trace_sha256"] and
            receipt["first_force_u_on"] == (result.get("first_force") or {}).get("u_on"), "trace replay")
    return receipt


def run_arm(engine, arm, out, schedule=None, kind="RUN", limit_s=None):
    """Run one arm into a new folder: trace.csv (every step), result.json, receipt.json."""
    require(kind in ("RUN", "SMOKE", "TEST"), "run kind")
    require(kind != "RUN" or schedule is None, "RUN uses the registered schedule")
    out = Path(out)
    out.mkdir()
    started_ns, start = time.time_ns(), time.monotonic()
    plan = engine.plan(arm)
    limit = plan["limit_s"] if limit_s is None else limit_s
    if limit is None:
        require(kind == "TEST", "no registered limit for this arm")
        limit = math.inf
    steps_done, status, runner, rows = 0, "INCOMPLETE", None, []
    monitors = Monitors(mini=arm.geometry != "BED")
    first = None
    if arm.reg == "reg1" and arm.geometry != "BED":
        first = dict(threshold_MPa=engine.const.THETA_MPA, u_geo=engine.geometry(arm)["u_geo"], u_on=None,
                     step_on=None, u_on_minus_u_geo=None, sigma_b="bottom force / D x 10 MPa")
    stop = dict(k_u=None, h_u=None, phi_u=None, bottom_pressure_E_u=None, first_native_target_step=None)
    try:
        runner = ArmRunner(engine, arm)
        rows = engine.schedule(arm, runner.total) if schedule is None else list(schedule)
        with (out / "trace.csv").open("x", encoding="ascii", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(COLUMNS)
            initial = runner.initial_record()
            writer.writerow([csv_value(initial[c]) for c in COLUMNS])
            status = "COMPLETE"
            for i, (k, phase, height, wall) in enumerate(rows):
                if time.monotonic() - start >= limit:
                    status = "TIME_LIMIT"
                    break
                _, rec = runner.step(k, phase, height, wall, capture_pairs=i == len(rows) - 1)
                steps_done = k
                writer.writerow([csv_value(rec[c]) for c in COLUMNS])
                if not k % 25:
                    stream.flush()
                monitors.update(k, rec)
                if first is not None and first["u_on"] is None and rec["bottom_MPa"] > first["threshold_MPa"]:
                    first.update(u_on=rec["u"], step_on=k, u_on_minus_u_geo=rec["u"] - first["u_geo"])
                if phase == "LOAD" and arm.geometry == "BED":
                    stop.update(k_u=k, h_u=height, phi_u=rec["phi_m"], bottom_pressure_E_u=rec["bottom_pressure_E"])
                    # The native loop stopped at this pressure (1.2 MPa); reg2 presses on to Φ_m 0.95.
                    if stop["first_native_target_step"] is None and rec["bottom_pressure_E"] >= engine.solver.TARGET:
                        stop["first_native_target_step"] = k
    except BaseException as exc:
        if out.is_dir() and not (out / "incomplete.json").exists():
            write_json(out / "incomplete.json", dict(label=LABEL, arm=arm.name, status="INCOMPLETE",
                                                    steps_done=steps_done, reason=f"{type(exc).__name__}: {exc}"))
        raise
    o = runner.observer
    unloading = None
    if arm.geometry == "BED":
        last = rows[steps_done - 1] if steps_done else None
        unloading = dict(**stop, unload_speed=engine.const.V0 / arm.unload_div,
                         unload_steps_done=sum(1 for r in rows[:steps_done] if r[1] == "UNLOAD"),
                         unload_travel_done=None if not last or stop["h_u"] is None or last[1] != "UNLOAD"
                         else last[2] - stop["h_u"])
    result = dict(
        label=LABEL, physics_result=False, registration=arm.reg, arm=asdict(arm), schedule_kind=kind,
        status=status, steps_scheduled=len(rows), steps_planned=plan["steps"], steps_done=steps_done,
        elapsed_s=time.monotonic() - start, limit_s=None if math.isinf(limit) else limit,
        started_ns=started_ns, ended_ns=time.time_ns(), plan=plan, dt=runner.dt, grid=runner.grid,
        points=len(runner.ids), disks=runner.geometry["disks"], box_width=runner.view.WIDTH, floor=runner.view.LO,
        initial_height=runner.geometry["h0"], sources=engine.source_record(), seed_sha256=runner.seed_sha256,
        boundary_sha256=runner.boundary_sha256, trace_sha256=sha((out / "trace.csv").read_bytes()),
        final_state_sha256=array_sha(runner.x, runner.v, runner.affine, runner.elastic),
        floor_audit=dict(runner.advance.audit),
        observer_calls=dict(other_walls=o.other_walls_calls, contact=o.contact_calls_total),
        observed_functions=["material_floor._other_walls"] + (
            [] if runner.kernel is None else
            ["suyoung_multicontact_dev._pair_impulse" if runner.projector is None
             else "gap_kernel derived kernel._pair_impulse"]),
        private_constants=dict(box_width=runner.view.WIDTH, plate_speed_load=engine.const.V0 / arm.load_div,
                               plate_speed_unload=None if arm.unload_div is None else -engine.const.V0 / arm.unload_div,
                               material_yield="inf (registered elastic E)" if arm.material == "E" else "pinned 3a",
                               contact_friction_passed=0. if arm.contact == "C1" else .5),
        monitors=monitors.summary(), first_force=first, unloading=unloading,
        last_step_pairs=o.pairs, environment=environment(), stage3_go=False, three_dimensional_go=False,
        note="wiring and recording only; no J1-J5, H_S or U4 judgement is made by this driver")
    write_json(out / "result.json", result)
    write_json(out / "receipt.json", dict(read_receipt(out, result),
                                          result_sha256=sha((out / "result.json").read_bytes())))
    return result


def registration_problems(engine):
    """Compare the computed plan with the numbers written in the two registration drafts."""
    problems = []
    plans = {a.name: engine.plan(a) for a in all_arms()}
    for geometry, contact, materials, div, steps, limits in REGISTERED_REG1:
        for material in materials:
            for cells, n, limit in zip(REG1_CELLS, steps, limits, strict=True):
                name = f"R1-{geometry}-{contact}-{material}-{'V0' if div == 1 else 'V' + str(div)}-{cells:02d}"
                p = plans[name]
                if (p["steps"], p["limit_s"]) != (n, limit):
                    problems.append(f"{name}: steps/limit {p['steps']}/{p['limit_s']} vs registered {n}/{limit}")
                disks = 1 if geometry == "G1" else 2
                expected_points = disks * REGISTERED_POINTS_PER_DISK[REG1_CELLS.index(cells)]
                if p["points"] != expected_points:
                    problems.append(f"{name}: points {p['points']} vs registered {expected_points}")
    t1 = plan_totals(engine, reg1_arms())
    t1n = plan_totals(engine, [a for a in reg1_arms() if a.cells != 24])
    r = REGISTERED_REG1_TOTALS
    got = dict(cpu_low_h=round(t1["cpu_low_h"], 1), cpu_high_h=round(t1["cpu_high_h"], 1),
               wall2_low_h=round(t1["wall2_low_h"], 1), wall2_high_h=round(t1["wall2_high_h"], 1),
               cpu_high_without_24_h=round(t1n["cpu_high_h"], 1), longest_limit_s=t1["longest_limit_s"])
    problems += [f"reg1 {k}: {got[k]} vs registered {v}" for k, v in r.items() if got[k] != v]
    main = [a for a in reg2_arms() if a.unload_div == 1]
    for a in reg2_arms():
        hours = (REGISTERED_REG2_LIMIT_H[(a.contact, a.cells)] if a.unload_div == 1
                 else REGISTERED_REG2_REPORT_LIMIT_H[a.contact])
        if plans[a.name]["limit_s"] != hours*3600:
            problems.append(f"{a.name}: limit {plans[a.name]['limit_s']} s vs registered {hours} h")
    t2, t2all = plan_totals(engine, main), plan_totals(engine, reg2_arms())
    got2 = dict(steps_36=plans["R2-BED-S-P-V0-36"]["steps"],
                height_at_stop=round(plans["R2-BED-S-P-V0-36"]["height_at_stop_nominal"], 5),
                cpu_h=round(t2["cpu_high_h"], 1), wall2_h=round(t2["wall2_high_h"], 1),
                report_wall2_h=round(t2all["wall2_high_h"] - t2["wall2_high_h"], 1))
    problems += [f"reg2 {k}: {got2[k]} vs registered {v}" for k, v in REGISTERED_REG2_TOTALS.items() if got2[k] != v]
    return problems


def check_only(engine, require_wsl=False):
    lines, problems = [], []
    for path, digest in engine.source_record().items():
        lines.append(f"SOURCE_OK {digest}  {path}")
    env = environment()
    lines.append(f"ENVIRONMENT python={env['python']} numpy={env['numpy']} wsl_target="
                 f"{'/'.join(WSL_ENVIRONMENT)} matches={env['matches_wsl_target']}")
    if require_wsl and not env["matches_wsl_target"]:
        problems.append("environment differs from the WSL target")
    for a in all_arms():
        p = engine.plan(a)
        unload = "" if p["unload_speed"] is None else f" unload_V/cP={p['unload_v_over_cP']:.5f} n_unload={p['n_unload']}"
        lines.append(f"PLAN {a.name:<22} {a.geometry:<3} {a.contact:<5} {a.material} cells={a.cells:>2} "
                     f"grid={p['grid']:>3} V/cP={p['v_over_cP']:.5f}{unload} dt={p['dt']:.10g} "
                     f"points={p['points']:>6} steps={p['steps']:>6} limit_s={p['limit_s']:>6} "
                     f"est_s={p['est_low_s']:.0f}-{p['est_high_s']:.0f}")
    found = registration_problems(engine)
    problems += found
    lines.append("PLAN_MATCHES_REGISTRATION reg1 50/50 reg2 14/14" if not found else
                 f"PLAN_REGISTRATION_MISMATCH {len(found)}")
    t1, t2 = plan_totals(engine, reg1_arms()), plan_totals(engine, [a for a in reg2_arms() if a.unload_div == 1])
    t2all = plan_totals(engine, reg2_arms())
    lines.append(f"TOTAL reg1 arms=50 cpu_h={t1['cpu_low_h']:.2f}-{t1['cpu_high_h']:.2f} "
                 f"two_core_wall_h={t1['wall2_low_h']:.2f}-{t1['wall2_high_h']:.2f} longest_limit_s={t1['longest_limit_s']}")
    lines.append(f"TOTAL reg2 main_arms=12 cpu_h={t2['cpu_high_h']:.2f} two_core_wall_h={t2['wall2_high_h']:.2f} "
                 f"with_report_arms={t2all['wall2_high_h']:.2f}")
    c = engine.const
    floor = engine.fresh(FLOOR_PATH, "registration_check_floor")
    for geometry in ("G1", "G2"):
        centers = engine.geometry(Arm("reg1", "check", geometry, "PLATE" if geometry == "G1" else "F2", "P", 8, 1))["centers"]
        for cells, expected in zip(REG1_CELLS, REGISTERED_POINTS_PER_DISK, strict=True):
            x, ids, volume = seed_disks(cells, centers, c.D)
            per_disk = len(ids) // len(centers)
            outline = disk_boundary(floor, c.D, x, ids, centers)
            if per_disk != expected or len(outline.owners) != 256*len(centers):
                problems.append(f"{geometry} {cells}: points per disk {per_disk}")
            lines.append(f"SEED {geometry} cells={cells:>2} points_per_disk={per_disk} outline={len(outline.owners)} "
                         f"sha256(x,ids,volume)={','.join(h[:16] for h in array_sha(x, ids, volume))}")
    for cells, (points, dt, hashes) in BED_PINS.items():
        x, ids, volume = engine.bed(cells)
        ok = len(ids) == points and engine.dt(cells) == dt and tuple(array_sha(x, ids, volume)) == hashes
        if not ok:
            problems.append(f"bed {cells}: seed or time step differs from the native pin")
        lines.append(f"SEED BED cells={cells} points={len(ids)} dt={engine.dt(cells)!r} native_pin={'OK' if ok else 'DIFFERS'}")
    engine.gap.GapProjector(engine.fresh(KERNEL_PATH, "registration_check_kernel"))
    lines.append("CONTACT_KERNELS_LOADED gap_projector=OK")
    lines.append("MPM_STEPS 0")
    return lines, problems


def smallest_arm(engine):
    return min(reg1_arms(), key=lambda a: engine.plan(a)["est_high_s"])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    modes = parser.add_subparsers(dest="mode", required=True)
    check = modes.add_parser("CHECK_ONLY", help="source hashes, plan table and seed hashes; no MPM step")
    smoke = modes.add_parser("SMOKE", help="a few steps of one arm (default: the smallest); wiring only")
    run = modes.add_parser("RUN", help="one registered arm with its registered schedule and limit")
    for sub in (check, smoke, run):
        sub.add_argument("--root", type=Path, default=REPO, help="tree holding the pinned sources")
    check.add_argument("--require-wsl-env", action="store_true", help="fail unless Python 3.12.3 and NumPy 2.5.2")
    smoke.add_argument("--arm", help="arm name (default: the smallest registered arm)")
    smoke.add_argument("--steps", type=int, default=5, help="number of steps (default 5)")
    smoke.add_argument("--out", type=Path, help="new folder for the smoke output (default: a temporary folder)")
    run.add_argument("--arm", required=True, help="registered arm name, as printed by CHECK_ONLY")
    run.add_argument("--out", type=Path, required=True, help="new folder for this arm")
    run.add_argument("--cpu", type=int, help="require this single-CPU affinity and one thread per library")
    args = parser.parse_args(argv)
    try:
        engine = Engine(args.root)
    except (ValueError, OSError) as exc:
        print("SOURCE_PIN_MISMATCH", exc)
        return 1
    arms = {a.name: a for a in all_arms()}
    if args.mode == "CHECK_ONLY":
        lines, problems = check_only(engine, args.require_wsl_env)
        print("\n".join(lines))
        for p in problems:
            print("PROBLEM", p)
        print("CHECK_ONLY_OK" if not problems else "CHECK_ONLY_FAILED")
        return 0 if not problems else 1
    if args.arm is not None and args.arm not in arms:
        print("UNKNOWN_ARM", args.arm)
        return 2
    if args.mode == "SMOKE":
        arm = arms[args.arm] if args.arm else smallest_arm(engine)
        out = args.out if args.out is not None else Path(tempfile.mkdtemp(prefix="suyoung_driver_smoke_")) / "arm"
        rows = engine.schedule(arm, float(engine.bed(arm.cells)[2].sum()) if arm.geometry == "BED" else 1.)
        result = run_arm(engine, arm, out, schedule=rows[:args.steps], kind="SMOKE")
        print(f"SMOKE_RAN arm={arm.name} steps={result['steps_done']} status={result['status']} out={out} "
              "(wiring only; not a physics result)")
        return 0 if result["status"] == "COMPLETE" and result["steps_done"] == min(args.steps, len(rows)) else 1
    if args.cpu is not None:
        threads = {k: os.environ.get(k) for k in THREAD_VARIABLES}
        if os.sched_getaffinity(0) != {args.cpu} or any(v != "1" for v in threads.values()):
            print("AFFINITY_OR_THREADS_NOT_SET", sorted(os.sched_getaffinity(0)), threads)
            return 2
    try:
        result = run_arm(engine, arms[args.arm], args.out, kind="RUN")
    except Exception as exc:
        print("ARM_INCOMPLETE", type(exc).__name__, exc, file=sys.stderr)
        return 4
    print(f"ARM_DONE arm={args.arm} status={result['status']}")
    return {"COMPLETE": 0, "TIME_LIMIT": 3}.get(result["status"], 4)


if __name__ == "__main__":
    sys.exit(main())
