"""Independent CPU probes for the proposed (not implemented) area contract.

Run from the review root with numpy/scipy and pinned source/scripts on path.
No source files are written.  Values are dimensionless resistance-network
tests or explicitly identified internal units, not material predictions.
"""
from pathlib import Path
import contextlib
import io
import json
import math
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source" / "scripts"))
import step3_sigma as s3


def resistance(n, edges, hi=0, lo=1):
    """Dirichlet solve for arbitrary positive resistor edges (i,j,R)."""
    lap = np.zeros((n, n))
    for i, j, r in edges:
        g = 1.0 / r
        lap[i, i] += g
        lap[j, j] += g
        lap[i, j] -= g
        lap[j, i] -= g
    p = np.zeros(n)
    p[hi] = 1.0
    free = [i for i in range(n) if i not in (hi, lo)]
    if free:
        p[free] = np.linalg.solve(lap[np.ix_(free, free)], -lap[np.ix_(free, [hi, lo])] @ p[[hi, lo]])
    current = float((lap @ p)[hi])
    return 1.0 / current, p.tolist()


def area_is_not_topology():
    # Both cases use two interface edges, each R=2; sum(g_iface)=1.
    # Same terminal and bulk graph: node 2 is connected to high by R=9.
    # A: both interface patches touch high directly. B: move one patch to 2.
    a, pa = resistance(3, [(0, 2, 9), (0, 1, 2), (0, 1, 2)])
    b, pb = resistance(3, [(0, 2, 9), (0, 1, 2), (2, 1, 2)])
    assert math.isclose(a, 1.0)
    assert math.isclose(b, 22 / 13)
    return {"sum_interface_conductance_both": 1.0,
            "R_same_bulk_graph_placement_A": a,
            "R_same_bulk_graph_placement_B": b,
            "relative_change_percent": 100 * (b / a - 1),
            "phi_A": pa, "phi_B": pb}


def voxel_boundary_placement():
    # Same conductive block and same electrode masks in every solve.
    # One bottom electrode column causes nonuniform interface potentials.
    # Changing only pid moves an N-face planar interface; prescribed sum gfilm
    # remains exactly 1/Rc for every cut. Internal G = 1e4 * physical G[S].
    vox = 1.0
    sid = np.ones((15, 1, 15), dtype=np.uint8)
    sigma = np.zeros(10)
    sigma[1] = 1.0
    bottom = np.zeros((15, 1), dtype=bool)
    bottom[0, 0] = True
    common = dict(z_bot_um=0, z_top_um=15, bot_allowed=bottom,
                  plate_band_um=0.5, plate_band_bot_um=0.5,
                  return_field=True)
    with contextlib.redirect_stdout(io.StringIO()):
        off = s3.solve_sigma_z(sid, sigma, vox, **common)
    # Rcode = L/(A*sigma_eff); here L=A=15.
    r0 = 1 / off["sigma_eff"]
    rows = []
    for rc in (0.1, 1.0, 10.0):
        for cut in (1, 7, 14):
            pid = np.zeros(sid.shape, dtype=np.int32)
            pid[:, :, cut:] = 1
            nfaces = 15
            r_face_ohm_cm2 = rc * nfaces * vox**2 / 1e4
            with contextlib.redirect_stdout(io.StringIO()):
                on = s3.solve_sigma_z(sid, sigma, vox, pid=pid,
                                    rint={(1, 1): r_face_ohm_cm2}, **common)
            assert on["interface"]["n_faces_rint"] == nfaces
            assert not on["unconverged"]
            r = 1 / on["sigma_eff"]
            drop = on["phi"][:, 0, cut - 1] - on["phi"][:, 0, cut]
            rows.append({"Rc_internal": rc, "cut_z_um": cut,
                         "N_faces": nfaces, "Rtotal_internal": r,
                         "incremental_R_internal": r - r0,
                         "sigma_on_over_off": on["sigma_eff"] / off["sigma_eff"],
                         "cell_drop_min_max": [float(drop.min()), float(drop.max())]})
    return {"Roff_internal": r0, "rows": rows}


def l1_scope():
    # Counts per unit true area are |nk|/h^2. In the continuum limit both
    # prescriptions recover integral jump^2/r. They are not identical finite
    # networks for nonuniform jumps sampled at different face endpoints.
    nx, nz = math.cos(math.pi / 6), math.sin(math.pi / 6)
    dx, dz = 1.0, 2.0
    s = nx + nz
    return {"normal_xz": [nx, nz], "L1": s,
            "sum_g_common_jump_L1": (nx + nz) / s,
            "sum_g_common_jump_axis": nx * nx + nz * nz,
            "heterogeneous_face_jumps": [dx, dz],
            "current_L1": (nx * dx + nz * dz) / s,
            "current_axis": nx * nx * dx + nz * nz * dz,
            "energy_L1": (nx * dx**2 + nz * dz**2) / s,
            "energy_axis": nx * nx * dx**2 + nz * nz * dz**2,
            "interpretation": "Finite-grid inequivalence, not a proof either continuum limit is wrong."}


def am_boundary_relabel():
    """Actual rasterize geometry: original pid vs physical midplane, same sid."""
    radius, delta, bridge, rho_film = 1.0, 0.02, 0.24, 1e-3
    distance = 2 * radius - delta
    top = 2 * radius + distance
    centers = np.array([[1.0, 1.0, radius], [1.0, 1.0, radius + distance]])
    area_true = math.pi * (radius**2 - (distance / 2)**2)
    sigma = np.zeros(10)
    sigma[1] = 0.01
    rows = []
    for vox in (0.2, 0.1):
        sid, original = s3.rasterize(centers, np.full(2, radius), np.full(2, 2),
                                     None, None, (0, 0, 0), (2, 2, top), vox,
                                     bridge_um=bridge)
        physical_plane = radius + distance / 2
        plane = np.where((np.arange(sid.shape[2]) + 0.5) * vox < physical_plane, 0, 1)
        plane = np.broadcast_to(plane[None, None, :], sid.shape).copy().astype(np.int32)
        plane[sid == 0] = -1
        common = dict(z_bot_um=0, z_top_um=top)
        with contextlib.redirect_stdout(io.StringIO()):
            off = s3.solve_sigma_z(sid, sigma, vox, **common)
        for label, pid in (("rasterize_pid", original), ("contact_midplane", plane)):
            nfaces = 0
            for axis in range(3):
                a, b = [slice(None)] * 3, [slice(None)] * 3
                a[axis], b[axis] = slice(None, -1), slice(1, None)
                a, b = tuple(a), tuple(b)
                nfaces += int(((sid[a] == 1) & (sid[b] == 1) & (pid[a] != pid[b])).sum())
            r_face = rho_film * nfaces * vox**2 / area_true
            with contextlib.redirect_stdout(io.StringIO()):
                on = s3.solve_sigma_z(sid, sigma, vox, rint={(1, 1): r_face}, pid=pid, **common)
            assert on["interface"]["n_faces_rint"] == nfaces
            assert not on["unconverged"]
            rows.append({"vox_um": vox, "placement": label, "n_faces": nfaces,
                         "same_Atrue_um2": area_true,
                         "normalized_sum_gfilm_S": nfaces * vox**2 * 1e-8 / r_face,
                         "sigma_off": off["sigma_eff"], "sigma_on": on["sigma_eff"],
                         "sigma_on_over_off": on["sigma_eff"] / off["sigma_eff"]})
    return rows


def sensitivity_and_bounds():
    # Identical added film term is insufficient to require equal relative
    # sigma changes if bulk/contact baseline resistances differ.
    return {"shared_film_R": 1.0,
            "model_A_R0": 1.0, "model_B_R0": 10.0,
            "model_A_sigma_on_over_off": 1 / 2,
            "model_B_sigma_on_over_off": 10 / 11,
            "model_A_delta_ln_sigma": math.log(1 / 2),
            "model_B_delta_ln_sigma": math.log(10 / 11),
            "only_intramodel_monotonicity_is_guaranteed": True}


def junction_series_reference():
    # A junction has 1 ohm on each fiber lead to the two contact nodes and
    # a pure contact resistance 5. A measured terminal R includes the leads.
    lead_a, lead_b, r_contact = 1.0, 1.0, 5.0
    measured_total = lead_a + r_contact + lead_b
    return {"correct_pure_contact_model_R": measured_total,
            "double_count_if_measured_terminal_R_used_as_Rj": lead_a + measured_total + lead_b,
            "junction_power_correct_at_unit_voltage": r_contact / measured_total**2,
            "test_requirement": "Define Rj reference planes and retained axial/access resistances."}


if __name__ == "__main__":
    print(json.dumps({"area_is_not_topology": area_is_not_topology(),
                      "voxel_boundary_placement": voxel_boundary_placement(),
                      "AM_boundary_placement": am_boundary_relabel(),
                      "L1_scope": l1_scope(),
                      "sensitivity_and_bounds": sensitivity_and_bounds(),
                      "junction_reference": junction_series_reference()}, indent=2))
