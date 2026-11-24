"""Read-only phase and free-surface observations for the B2-U development deck."""
from math import atan, degrees, hypot, pi

import numpy as np


RADIUS = .01258325
HALF_LENGTH = .00251665
PERIOD = .782508
OMEGA = 2 * pi / PERIOD
DT = 2.373e-7
ROTATION_START = 1121213
SAVE_EVERY = 32976
HEADER = b"ITEM: ATOMS id type x y z vx vy vz fx fy fz radius"
THRESHOLDS = (.025, .05, .10)


def turns(step):
    return (step - ROTATION_START) * DT / PERIOD


def phase(step):
    t = turns(step)
    if t < 0:
        return "PRE_ROTATION"
    if t < 1:
        return "TURN_0_TO_1"
    if t < 2:
        return "TURN_1_TO_2"
    return "AFTER_TWO_TURNS"


def surface_fit(y, z, r, quantile):
    edges = np.linspace(-.6 * RADIUS, .6 * RADIUS, 16)
    points = []
    for low, high in zip(edges, edges[1:]):
        mask = (y >= low) & (y < high)
        if mask.sum() >= 8:
            points.append(((low + high) / 2, np.quantile(z[mask] + r[mask], quantile)))
    if len(points) < 10 or points[0][0] > -.35 * RADIUS or points[-1][0] < .35 * RADIUS:
        return None
    h, top = np.asarray(points).T
    a, b = np.triu_indices(len(h), 1)
    slope = float(np.median((top[b] - top[a]) / (h[b] - h[a])))
    intercept = float(np.median(top - h * slope))
    residual = float(np.sqrt(np.mean((top - slope * h - intercept) ** 2)) / RADIUS)
    return slope, intercept, residual, len(points)


def profile(y, z, vy, vz, r, slope, intercept):
    norm = hypot(1, slope)
    along = (y + slope * (z - intercept)) / norm
    depth = (intercept + slope * y - z) / (norm * RADIUS)
    mask = (abs(along) <= .25 * RADIUS) & (depth >= 0) & (depth < .60)
    # Tangential flow is positive downhill. Both fields use the same lab-frame tangent.
    tangent = -np.sign(slope) / norm
    lab = tangent * (vy[mask] + slope * vz[mask]) / (OMEGA * RADIUS)
    wall = tangent * (-z[mask] + slope * y[mask]) / RADIUS
    bins = np.minimum((depth[mask] / .02).astype(int), 29)
    weights = r[mask] ** 3
    counts = np.bincount(bins, minlength=30)
    volumes = np.bincount(bins, weights=weights, minlength=30)
    result = []
    # One point is one particle center; sphere volume sets the local mean velocity.
    lab_sum = np.bincount(bins, weights=weights * lab, minlength=30)
    rel_sum = np.bincount(bins, weights=weights * (lab - wall), minlength=30)
    for i, count in enumerate(counts):
        enough = count >= 8
        result.append(dict(depth_R=(i + .5) * .02, n=int(count),
                           lab_over_omega_R=float(lab_sum[i] / volumes[i]) if enough else None,
                           relative_over_omega_R=float(rel_sum[i] / volumes[i]) if enough else None))
    return result


def layer_boundary(rows, cutoff):
    result = dict(cutoff=cutoff, delta_over_R=None, bracket_over_R=None, status="NO_SURFACE_COVERAGE")
    previous = None
    for i, row in enumerate(rows):
        if row["lab_over_omega_R"] is None:
            if previous is not None:
                result["status"] = "DEPTH_COVERAGE_GAP"
                return result
            if i >= 1:
                return result
            continue  # One empty skin bin is possible when only centers are sampled.
        u = min(row["lab_over_omega_R"], row["relative_over_omega_R"] - cutoff)
        d = row["depth_R"]
        if u <= 0:
            if previous is None:
                result["status"] = "NO_RESOLVED_SURFACE_FLOW"
                return result
            prev_d, prev_u = previous
            result.update(delta_over_R=prev_d + (d - prev_d) * prev_u / (prev_u - u),
                          bracket_over_R=[prev_d, d], status="RESOLVED")
            return result
        previous = d, u
    result["status"] = "LOWER_BOUND_ONLY"
    return result


def wall_slip(y, z, vy, vz, r, rotating):
    """Near-cylinder particle centers; no contact force or particle spin is available."""
    rho = np.hypot(y, z)
    mask = (rho > 0) & (RADIUS - rho - r <= r)
    result = dict(near_wall_particles=int(mask.sum()), azimuthal_slip_fraction=None)
    if rotating and mask.sum() >= 8:
        angle_speed = (-z[mask] * vy[mask] + y[mask] * vz[mask]) / rho[mask] ** 2
        result["azimuthal_slip_fraction"] = float(np.average(1 - angle_speed / OMEGA, weights=r[mask]**3))
    return result


def measure(x, y, z, vy, vz, r, rotating):
    mid = abs(x) <= .5 * HALF_LENGTH
    y, z, vy, vz, r = (a[mid] for a in (y, z, vy, vz, r))
    result = dict(midplane_particles=int(len(y)), theta_signed_deg=None, theta_deg=None,
                  surface_q_sensitivity_deg={}, surface_rms_over_R=None, surface_columns=0,
                  delta_over_R=None, delta_m=None, layer_status="NO_SURFACE_FIT",
                  layer_sensitivity=[], center_profile=[],
                  wall_frame_kinematics=wall_slip(y, z, vy, vz, r, rotating))
    fits = {q: surface_fit(y, z, r, q) for q in (.985, .99, .995)}
    result["surface_q_sensitivity_deg"] = {
        str(q): degrees(atan(fit[0])) if fit else None for q, fit in fits.items()}
    if fits[.99] is None:
        return result
    slope, intercept, rms, columns = fits[.99]
    signed = degrees(atan(slope))
    result.update(theta_signed_deg=signed, theta_deg=abs(signed), surface_columns=columns,
                  surface_rms_over_R=rms)
    if not rotating or abs(slope) < .01:
        result["layer_status"] = "PRE_ROTATION" if not rotating else "DOWNHILL_DIRECTION_UNRESOLVED"
        return result
    rows = profile(y, z, vy, vz, r, slope, intercept)
    bounds = [layer_boundary(rows, cutoff) for cutoff in THRESHOLDS]
    delta = bounds[1]["delta_over_R"]
    result.update(center_profile=rows, layer_sensitivity=bounds, delta_over_R=delta,
                  delta_m=delta * RADIUS if delta is not None else None, layer_status=bounds[1]["status"])
    return result


def observe_frame(stream, expected_step):
    if stream.readline().strip() != b"ITEM: TIMESTEP" or int(stream.readline()) != expected_step:
        raise ValueError("B2 frame timestep mismatch")
    if expected_step % SAVE_EVERY or stream.readline().strip() != b"ITEM: NUMBER OF ATOMS":
        raise ValueError("B2 frame clock or count header mismatch")
    count = int(stream.readline())
    if count <= 0 or not stream.readline().startswith(b"ITEM: BOX BOUNDS"):
        raise ValueError("invalid B2 frame header")
    for _ in range(3):
        bounds = [float(s) for s in stream.readline().split()]
        if len(bounds) != 2 or not all(np.isfinite(bounds)) or bounds[0] >= bounds[1]:
            raise ValueError("invalid rectangular frame bounds")
    if stream.readline().strip() != HEADER:
        raise ValueError("unexpected B2 data columns")
    data = np.loadtxt(stream, comments=None, ndmin=2)
    if data.shape != (count, 12) or not np.isfinite(data).all():
        raise ValueError("incomplete or nonfinite B2 atom table")
    ids, types = data[:, 0], data[:, 1]
    if (np.any(ids <= 0) or np.any(ids != np.floor(ids)) or len(np.unique(ids)) != count
            or not np.isin(types, (1, 2, 3)).all() or np.any(data[:, 11] <= 0)):
        raise ValueError("invalid B2 particles")
    result = measure(data[:, 2], data[:, 3], data[:, 4], data[:, 6], data[:, 7], data[:, 11],
                     rotating=expected_step > ROTATION_START)
    result.update(step=expected_step, frame_index=expected_step // SAVE_EVERY,
                  phase=phase(expected_step), turns_since_rotation=turns(expected_step), atom_count=count)
    return result


def distribution(values):
    valid = [value for value in values if value is not None]
    if not valid:
        return dict(n=0, median=None, q25=None, q75=None)
    low, mid, high = np.quantile(valid, [.25, .5, .75])
    return dict(n=len(valid), median=float(mid), q25=float(low), q75=float(high))


def grouped(records):
    return dict(frames=len(records),
                theta_deg=distribution(r["theta_deg"] for r in records),
                delta_over_R=distribution(r["delta_over_R"] for r in records),
                wall_slip_fraction=distribution(r["wall_frame_kinematics"]["azimuthal_slip_fraction"]
                                                for r in records))


def summarize(records):
    recs = sorted(records, key=lambda r: r["step"])
    if [r["step"] for r in recs] != [i * SAVE_EVERY for i in range(34, 235)]:
        raise ValueError("expected pre-rotation frame 34 and rotating frames 35 through 234")
    first = [r for r in recs if phase(r["step"]) == "TURN_0_TO_1"]
    second = [r for r in recs if phase(r["step"]) == "TURN_1_TO_2"]
    return dict(independent_seeds=1, rotation_start_step=ROTATION_START, save_steps=SAVE_EVERY,
                dt_s=DT, period_s=PERIOD, radius_m=RADIUS,
                pre_rotation_slope_deg=recs[0]["theta_signed_deg"], pre_rotation_step=recs[0]["step"],
                material_yield_angle_deg=None, mu_wall_effective=None,
                turn_0_to_1=grouped(first), turn_1_to_2=grouped(second),
                second_turn_quarters=[grouped([r for r in second if quarter <=
                    (turns(r["step"]) - 1) * 4 < quarter + 1]) for quarter in range(4)],
                post_two_turns_frames=1, terminal=grouped([recs[-1]]))
