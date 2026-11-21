"""Measure both wall projections in the fixed F8/F16 loading solver."""
import argparse
from contextlib import ExitStack
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np


SCRIPTS = Path(__file__).resolve().parents[3] / "scripts"
SOURCE = {
    "suyoung_u6b_dev.py": "50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762",
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}
EXPECTED = {8: "03f3bc2c106aa466f1ccc2b774e0b768f2a902792006609680faa53038434cdf",
            16: "5475cc87df297533002afb621cbdac06c0319ca40eb65ddf40322ae6c018b0de"}
WALL_COLUMNS = ("step", "plate_displacement_code", "lid_code", "first_top_row",
                "bottom_J_pre", "bottom_J_post", "top_J_down_pre", "top_J_down_post",
                "floor_positive_mass_entries_pre", "floor_positive_mass_entries_post",
                "top_positive_mass_entries_pre", "top_positive_mass_entries_post", "bottom_pressure_E")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_driver(directory=SCRIPTS):
    for name, expected in SOURCE.items():
        if digest(directory/name) != expected:
            raise ValueError("fixed source mismatch: " + name)
    spec = importlib.util.spec_from_file_location("private_wall_driver", directory/"suyoung_u6b_dev.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    return driver


class WallObserver:
    """Own one private solver instance. Forward all calls and arguments unchanged."""

    def __init__(self, solver, open_output):
        self.solver = solver
        self.original_walls = solver.walls
        solver.walls = self.observe_wall
        self.open_output = open_output
        self.writer = None
        self.steps = 0
        self.calls = []

    def observe_wall(self, mass, xy, vel, lid, speed):
        # Read pre-clamp velocities. Several body-field entries can share a node.
        top = (xy[:, 1] >= lid) & (vel[:, 1] > speed)
        floor = (xy[:, 1] <= self.solver.LO) & (vel[:, 1] < 0.)
        top_down = float(np.sum(mass[top] * (vel[top, 1]-speed)))
        n_top = int(np.count_nonzero(top & (mass > 0.)))
        n_floor = int(np.count_nonzero(floor & (mass > 0.)))
        bottom = self.original_walls(mass, xy, vel, lid, speed)
        self.calls.append((bottom, top_down, n_floor, n_top))
        return bottom

    def advance(self, x, v, affine, elastic, fields, volume, grid, dt, lid):
        self.calls.clear()
        result = self.solver.advance(x, v, affine, elastic, fields, volume, grid, dt, lid)
        if len(self.calls) != 2:
            raise ValueError("expected two wall calls in each fixed solver step")
        step = self.steps + 1
        height = self.solver.WIDTH - dt*step*self.solver.WALL_SPEED
        bottom, top, floor_n, top_n = zip(*self.calls)
        pressure = (bottom[0] + bottom[1]) / (dt*self.solver.WIDTH)
        if self.solver.LO + height != lid or pressure != result[-1]:
            raise ValueError("wall observation and native driver differ")
        if self.writer is None:
            self.stream = self.open_output()
            self.writer = csv.writer(self.stream)
            self.writer.writerow(WALL_COLUMNS)
        top_row = int(np.searchsorted(np.arange(grid+1)/grid, lid, side="left"))
        self.writer.writerow((step, self.solver.WIDTH-height, lid, top_row, *bottom, *top,
                              *floor_n, *top_n, pressure))
        self.steps = step
        if step % 25 == 0:
            self.stream.flush()
        return result


def classification(native_status, trace_sha, cells):
    if native_status != "TARGET_BRACKETED":
        return "INCOMPLETE"
    if trace_sha != EXPECTED[cells]:
        return "TRACE_MISMATCH"
    return "DEVELOPMENT_WALL_READBACK"


def run(cells, budget, out):
    driver = load_driver()
    solver = driver.fixed_solver()
    with ExitStack() as files:
        def open_wall():
            return files.enter_context((out/"wall.csv").open("x", encoding="ascii", newline=""))

        collector = WallObserver(solver, open_wall)
        # run_arm exclusively creates out on entry and writes its native trace/receipt.
        native = driver.run_arm("F", cells, budget, out, advance=collector.advance)
        if collector.steps == 0:
            csv.writer(open_wall()).writerow(WALL_COLUMNS)
    trace_sha = digest(out/"trace.csv")
    if trace_sha != native["trace_sha256"] or collector.steps != native["steps"]:
        raise ValueError("native receipt and wall observation differ")
    status = classification(native["status"], trace_sha, cells)
    receipt = {
        "label": "DEVELOPMENT_ONLY", "status": status, "eligible_development_readback": status == "DEVELOPMENT_WALL_READBACK",
        "u6_qualified": False, "arm": "F", "setting": 1, "cells": cells, "steps": collector.steps,
        "E_MPa": 10., "dt": driver.step_size(solver, cells), "width": solver.WIDTH,
        "expected_trace_sha256": EXPECTED[cells], "trace_sha256": trace_sha,
        "wall_sha256": digest(out/"wall.csv"), "result_sha256": digest(out/"result.json"),
        "original_source_sha256": SOURCE, "observer_sha256": digest(Path(__file__)),
    }
    driver.write_json(out/"observer.json", receipt)
    print(json.dumps({"cells": cells, "status": status, "steps": collector.steps, "trace_sha256": trace_sha}))
    return 0 if receipt["eligible_development_readback"] else 4


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cells", type=int, choices=(8, 16), required=True)
    p.add_argument("--budget", type=float, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    try:
        return run(args.cells, args.budget, args.out)
    except (OSError, ValueError, ArithmeticError) as exc:
        print("WALL_OBSERVER_INCOMPLETE", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
