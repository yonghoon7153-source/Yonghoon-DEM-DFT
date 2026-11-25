"""Synthetic MOOSE-like output for the step-1 checker tests (test data only, not physics).

The rows satisfy the step-1 identities exactly (P1 balance, P2 mean stress, P4 volume) so
that each test can break exactly one of them.  Column names are the postprocessor names
of ../step1_disk.i.
"""
import json
import math

D = 0.1
R = 0.05
GAP = 0.0017272 * D
H0 = 2 * R + 2 * GAP
E = 1.0e7
NU = 0.45
K = E / (3 * (1 - 2 * NU))
V = 2.5e-5                      # each plate, m per unit time
SY = 4.0e5

COLUMNS = ["time", "F_top_y", "F_bot_y", "F_top_x", "F_bot_x", "R_symy_y", "R_symx_x",
           "u_top", "u_bot", "area", "area_ref", "int_sxx", "int_syy", "int_szz", "int_sxy",
           "svm_max", "nl_its"]


def disk_area(tag="m13"):
    """Polygon area of the O-grid disk (exact-radius boundary), close to the mesher value."""
    nc = {"m13": 32, "m26": 64}[tag]
    return 0.5 * nc * R * R * math.sin(2 * math.pi / nc)


def mesh_json(path, tag="m13", area=None, **over):
    ns, nr = {"m13": (8, 2), "m26": (16, 4)}[tag]
    d = {"label": "DEVELOPMENT_ONLY", "generator": "synthetic", "dim": 2, "D_m": D, "R_m": R,
         "gap_m": GAP, "h0_between_plates_m": H0, "ns": ns, "nr": nr, "alpha": 0.6,
         "disk_area_mesh_m2": disk_area(tag) if area is None else area,
         "boundary_segments": 4 * ns}
    d.update(over)
    with open(path, "w", encoding="ascii") as f:
        json.dump(d, f, indent=1)
    return d


def force(approach, k=2.0e6, k2=3.0e6):
    pen = approach - 2 * GAP
    return k * pen + k2 * pen * pen if pen > 0 else 0.0


def make_rows(end_time=407.0, dt=1.0, A0=None, k=2.0e6, tag="m13"):
    """t = 0 row of zeros (MOOSE initial output) then one row per step."""
    A0 = disk_area(tag) if A0 is None else A0
    rows = [dict((c, 0.0) for c in COLUMNS)]
    n = int(round(end_time / dt))
    for i in range(1, n + 1):
        t = i * dt
        u_top, u_bot = -V * t, V * t
        h = H0 + u_top - u_bot
        F = force(u_bot - u_top, k=k)
        A = A0
        for _ in range(60):
            syy = -F * h / A
            A = A0 * (1 + (1 + NU) * syy / (3 * K))
        syy = -F * h / A
        szz = NU * syy
        rows.append({"time": t, "F_top_y": -F, "F_bot_y": F, "F_top_x": 0.0, "F_bot_x": 0.0,
                     "R_symy_y": 0.0, "R_symx_x": 0.0, "u_top": u_top, "u_bot": u_bot,
                     "area": A, "area_ref": A0, "int_sxx": 0.0, "int_syy": syy * A,
                     "int_szz": szz * A, "int_sxy": 0.0,
                     "svm_max": min(SY, abs(syy)), "nl_its": 3.0 if F > 0 else 0.0})
    return rows


def write_csv(path, rows, columns=None):
    columns = columns or COLUMNS
    with open(path, "w", encoding="ascii") as f:
        f.write(",".join(columns) + "\n")
        for r in rows:
            f.write(",".join(fmt(r[c]) for c in columns) + "\n")


def fmt(x):
    """Exact round trip (repr); MOOSE itself prints 14 significant digits."""
    x = float(x)
    if not math.isfinite(x):
        return "nan" if math.isnan(x) else ("inf" if x > 0 else "-inf")
    return repr(x)
