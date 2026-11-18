"""AM/SE contact coverage on the cubic MPM measurement grid (x,y periodic)."""
import argparse
import json
import math
import numbers

import numpy as np


def seed_counts(am_phase, spheres, n_grid, lateral_origin):
    """Recreate the eight SE seed points per occupied MPM cell in the x/y RVE.

    Sphere coordinates and radii use the MPM unit box. The AM grid is the
    cropped lateral RVE, starting at lateral_origin, with the full z axis.
    """
    am = np.asarray(am_phase)
    if (am.ndim != 3 or 0 in am.shape or am.shape[0] != am.shape[1]
            or am.dtype.kind not in "iu" or np.any(am < 0) or np.any(am > 2)):
        raise ValueError("expected a square lateral RVE with AM phase codes 0, 1, 2")
    if (type(n_grid) is not int or type(lateral_origin) is not int or lateral_origin < 0
            or lateral_origin + am.shape[0] > n_grid):
        raise ValueError("periodic subgrid outside the MPM grid")
    width = am.shape[0]
    grid = np.zeros(am.shape, dtype=np.uint8)
    for cx, cy, cz, radius in spheres:
        if not all(math.isfinite(v) for v in (cx, cy, cz, radius)) or radius <= 0:
            raise ValueError("invalid sphere")
        z0 = max(0, math.floor((cz-radius)*n_grid))
        z1 = min(am.shape[2], math.ceil((cz+radius)*n_grid))
        if z1 <= z0:
            continue
        z = np.arange(z0, z1)
        axes = []
        for center in (cx, cy):
            left = math.floor((center-radius)*n_grid)
            right = math.ceil((center+radius)*n_grid)
            if right-left <= width:
                idx = np.arange(left, right)
            else:
                # Use the nearest periodic image per cell for a wide sphere.
                idx = np.arange(lateral_origin, lateral_origin+width)
                idx += width * np.rint((center*n_grid-(idx+.5))/width).astype(np.int64)
            axes.append(idx)
        x, y = axes
        dx2 = ((x+.5)/n_grid - cx)**2
        dy2 = ((y+.5)/n_grid - cy)**2
        dz2 = ((z+.5)/n_grid - cz)**2
        i,j,k = np.nonzero(dx2[:,None,None] + dy2[None,:,None] + dz2 <= radius*radius)
        grid[(x[i]-lateral_origin) % width, (y[j]-lateral_origin) % width, z[k]] = 8
    grid[am != 0] = 0
    return grid


def contact_census(am_phase, se_counts, h_um):
    """Walk distinct oriented AM faces. 0 is non-AM, 1 and 2 are AM phases."""
    am = np.asarray(am_phase)
    n = np.asarray(se_counts)
    if am.ndim != 3 or 0 in am.shape or n.shape != am.shape:
        raise ValueError("AM phases and SE counts require the same nonempty xyz grid")
    if am.dtype.kind not in "iu" or np.any(am > 2) or np.any(am < 0):
        raise ValueError("expected AM phase codes 0, 1, 2")
    if n.dtype.kind not in "iu" or np.any(n < 0):
        raise ValueError("SE counts must be nonnegative integers")
    if np.any((am != 0) & (n >= 4)):
        raise ValueError("ambiguous AM and occupied SE cell")
    if isinstance(h_um, bool) or not isinstance(h_um, numbers.Real):
        raise ValueError("expected cubic cell width in micrometres")
    h = float(h_um)
    area = h*h
    if h <= 0 or not math.isfinite(area) or area == 0:
        raise ValueError("expected positive finite cell face area")

    counts = {phase: [0, 0, 0] for phase in (1, 2)}

    def interface(src, dst, seam):
        # Interior and seam each enter once per spatial direction. At an
        # AM|non-AM face exactly one of the two orientations can contribute.
        for left, right in ((src, dst), (dst, src)):
            touching_se = n[right] >= 4
            non_am = am[right] == 0
            for phase, tally in counts.items():
                free = (am[left] == phase) & non_am
                covered = int(np.count_nonzero(free & touching_se))
                tally[0] += int(np.count_nonzero(free))
                tally[1] += covered
                if seam:
                    tally[2] += covered

    for axis in range(3):
        lower = [slice(None)] * 3
        upper = lower.copy()
        lower[axis], upper[axis] = slice(None, -1), slice(1, None)
        interface(tuple(lower), tuple(upper), False)
        if axis < 2 and am.shape[axis] > 1:
            lower[axis], upper[axis] = -1, 0
            interface(tuple(lower), tuple(upper), True)

    result = {}
    for phase, (free, covered, seam) in counts.items():
        reason = None
        if free == 0:
            reason = "free_surface_empty" if np.any(am == phase) else "phase_absent"
        result[phase] = dict(free_faces=free, covered_faces=covered,
                             free_area_um2=free * area, covered_area_um2=covered * area,
                             seam_unrepresented_faces=seam, seam_unrepresented_area_um2=seam * area,
                             C0=covered/free if free else None, reason=reason)
    return result


def compare(am_phase, seed_counts, end_counts, h_um, rigid):
    """Use one AM scaffold. Analytic rigid fractions, if known, use its free surface."""
    seed = contact_census(am_phase, seed_counts, h_um)
    end = contact_census(am_phase, end_counts, h_um)
    if len(rigid) != 2:
        raise ValueError("supply one rigid reference per AM phase")
    phases = {}
    for phase, analytic in zip((1, 2), rigid):
        first, last = seed[phase]["C0"], end[phase]["C0"]
        if analytic is not None:
            if (first is None or isinstance(analytic, bool) or not isinstance(analytic, numbers.Real)
                    or not 0 <= analytic <= 1):
                raise ValueError("reference requires a measurable phase and fraction in [0,1]")
            analytic = float(analytic)
        phases[str(phase)] = dict(C_rigid=analytic, C_seed=first, C_end=last,
                                  seed_bias=None if analytic is None else first - analytic,
                                  plastic_increment=None if first is None else last - first,
                                  seed=seed[phase], end=end[phase])
    return dict(estimator="raw_grid_faces", unit="fraction", band_um=0,
                h_um=float(h_um), periodic_axes=["x", "y"], phases=phases)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("npz", help="AM/end grids and h_um, with a seed grid or normalized SE spheres")
    for i in (1, 2):
        parser.add_argument("--rigid-am" + str(i), type=float, help="DM2 free-surface fraction")
    args = parser.parse_args(argv)
    with np.load(args.npz, allow_pickle=False) as data:
        if data["h_um"].shape:
            parser.error("h_um must be scalar")
        am = data["am_phase"]
        has_grid = "seed_counts" in data
        geometry = {"seed_spheres", "n_grid", "lateral_origin"}
        if has_grid and geometry.intersection(data.files):
            parser.error("ambiguous seed source")
        if not has_grid and not geometry.issubset(data.files):
            parser.error("missing seed grid or complete sphere geometry")
        seed = data["seed_counts"] if has_grid else seed_counts(
            am, data["seed_spheres"], data["n_grid"].item(), data["lateral_origin"].item())
        result = compare(am, seed, data["end_counts"],
                         data["h_um"].item(), [args.rigid_am1, args.rigid_am2])
    print(json.dumps(result, ensure_ascii=True, allow_nan=False))


if __name__ == "__main__":
    main()
