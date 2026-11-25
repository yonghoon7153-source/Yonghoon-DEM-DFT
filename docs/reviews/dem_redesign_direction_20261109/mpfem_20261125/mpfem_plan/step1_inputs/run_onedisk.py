#!/usr/bin/env python3
"""Step-1 one-disk driver for Kratos 10.4.4 (MPFEM plan).

DRAFT.  Written but NOT executed by its author.

Runs StructuralMechanicsAnalysis on a ProjectParameters JSON, with the mesh and
materials files given on the command line, inside a NEW output folder.  Writes
  trace.csv     one row per step (plate forces, approach, area, mean stresses,
                boundary-integral mean strains, active contact nodes, Newton its)
  summary.json  inputs sha256, versions, timing, and the hand checks
     C   every step converged and the run reached the end time
     P1  top / bottom plate force balance        (static runs only)
     P2  mean-stress identity  <s_yy> = -F h / A,  <s_xx> = 0   (frictionless plates)
     P3  elastic slope <s_yy>/<e_yy> = E/(1-nu^2), <e_xx>/<e_yy> = -nu/(1-nu)
         (only with --elastic-small-strain: linear elastic small-strain arm)
     P4  volume change = mean pressure / bulk modulus (3D slab only)
Forces are per unit thickness (3D reactions divided by the slab thickness).
Tolerances are development policy values (step1 doc section 4).
"""
import argparse
import csv
import hashlib
import json
import math
import os
import platform
import sys
import time


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--params", required=True)
    ap.add_argument("--mdpa", required=True, help="mesh path WITHOUT .mdpa")
    ap.add_argument("--materials", required=True)
    ap.add_argument("--out", required=True, help="new folder (must not exist)")
    ap.add_argument("--arm", default="unnamed")
    ap.add_argument("--elastic-small-strain", action="store_true", help="enable P3")
    ap.add_argument("--E", type=float, default=1.0e7)
    ap.add_argument("--nu", type=float, default=0.45)
    args = ap.parse_args()

    params_path, mdpa, mat = (os.path.abspath(p) for p in (args.params, args.mdpa, args.materials))
    mesh_json = mdpa + ".mesh.json"
    with open(mesh_json, encoding="ascii") as f:
        mesh = json.load(f)
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=False)
    here = os.path.abspath(__file__)

    import KratosMultiphysics as KM
    import KratosMultiphysics.StructuralMechanicsApplication  # noqa: F401
    import KratosMultiphysics.ContactStructuralMechanicsApplication  # noqa: F401
    import KratosMultiphysics.ConstitutiveLawsApplication  # noqa: F401
    import KratosMultiphysics.LinearSolversApplication  # noqa: F401
    from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import \
        StructuralMechanicsAnalysis

    with open(params_path, encoding="utf-8") as f:
        params = KM.Parameters(f.read())
    ss = params["solver_settings"]
    ss["model_import_settings"]["input_filename"].SetString(mdpa)
    ss["material_import_settings"]["materials_filename"].SetString(mat)
    params["problem_data"]["problem_name"].SetString(args.arm)
    static = ss["solver_type"].GetString().lower() == "static"
    if params.Has("output_processes") and params["output_processes"].Has("vtk_output"):
        for i in range(params["output_processes"]["vtk_output"].size()):
            params["output_processes"]["vtk_output"][i]["Parameters"]["output_path"].SetString(
                os.path.join(out, "vtk"))
    os.chdir(out)

    dim = int(mesh["dim"])
    thick = float(mesh["tz_m"]) if dim == 3 else 1.0
    h0, A0 = float(mesh["h0_between_plates_m"]), float(mesh["disk_area_mesh_m2"])
    E, nu = args.E, args.nu
    K = E / (3 * (1 - 2 * nu))
    rows, t_start = [], time.time()

    def record(stage, converged):
        mp = stage.model["Structure"]
        pi = mp.ProcessInfo

        def plate(name):
            sub = mp.GetSubModelPart(name)
            F = sum(n.GetSolutionStepValue(KM.REACTION_Y) for n in sub.Nodes) / thick
            u = next(iter(sub.Nodes)).GetSolutionStepValue(KM.DISPLACEMENT_Y)
            return F, u

        Ft, ut = plate("TopPlate")
        Fb, ub = plate("BottomPlate")
        hc = h0 + ut - ub
        area, S = 0.0, [0.0, 0.0, 0.0, 0.0]                  # xx, yy, zz, xy (area-weighted sums)
        for e in mp.GetSubModelPart("Disk").Elements:
            g = e.GetGeometry()
            a_e = g.Area() if dim == 2 else g.Volume() / thick
            area += a_e
            sig = e.CalculateOnIntegrationPoints(KM.CAUCHY_STRESS_VECTOR, pi)
            try:
                w = [float(x) for x in e.CalculateOnIntegrationPoints(KM.INTEGRATION_WEIGHT, pi)]
                if not w or sum(w) <= 0:
                    raise ValueError
            except Exception:
                w = [1.0] * len(sig)
            ws = sum(w)
            comp = (0, 1, None, 2) if dim == 2 else (0, 1, 2, 3)
            for k, c in enumerate(comp):
                if c is not None:
                    S[k] += a_e * sum(wi * float(s[c]) for wi, s in zip(w, sig)) / ws
        # small-strain mean strain from the initial boundary polygon (layer z = 0)
        exx = eyy = exy = 0.0
        active = nseg = 0
        seen = set()
        for cnd in mp.GetSubModelPart("DiskSurface").Conditions:
            nds = [n for n in cnd.GetNodes() if abs(n.Z0) < 1e-12]
            if len(nds) != 2:
                continue
            a, b = nds
            nseg += 1
            dx, dy = b.X0 - a.X0, b.Y0 - a.Y0
            L = math.hypot(dx, dy)
            nx_, ny_ = dy / L, -dx / L
            if nx_ * (a.X0 + b.X0) + ny_ * (a.Y0 + b.Y0) < 0:   # outward from the disk centre (0,0)
                nx_, ny_ = -nx_, -ny_
            ux = 0.5 * (a.GetSolutionStepValue(KM.DISPLACEMENT_X) + b.GetSolutionStepValue(KM.DISPLACEMENT_X))
            uy = 0.5 * (a.GetSolutionStepValue(KM.DISPLACEMENT_Y) + b.GetSolutionStepValue(KM.DISPLACEMENT_Y))
            exx += ux * nx_ * L
            eyy += uy * ny_ * L
            exy += 0.5 * (ux * ny_ + uy * nx_) * L
            for n in (a, b):
                if n.Id not in seen:
                    seen.add(n.Id)
                    active += int(n.Is(KM.ACTIVE))
        rows.append({
            "step": int(pi[KM.STEP]), "time": float(pi[KM.TIME]), "converged": int(bool(converged)),
            "nl_iterations": int(pi[KM.NL_ITERATION_NUMBER]),
            "u_top_m": ut, "u_bottom_m": ub, "approach_m": ub - ut, "h_contact_m": hc,
            "F_top_N_per_m": Ft, "F_bottom_N_per_m": Fb,
            "sigma_b_Pa": abs(Fb) / mesh["D_m"],
            "area_m2": area, "area_ratio": area / A0,
            "mean_sxx_Pa": S[0] / area, "mean_syy_Pa": S[1] / area,
            "mean_szz_Pa": (S[2] / area) if dim == 3 else float("nan"), "mean_sxy_Pa": S[3] / area,
            "mean_exx": exx / A0, "mean_eyy": eyy / A0, "mean_exy": exy / A0,
            "active_contact_nodes": active, "boundary_segments_used": nseg,
            "wall_s": time.time() - t_start,
        })

    class Stage(StructuralMechanicsAnalysis):
        def SolveSolutionStep(self):
            self._ok = super().SolveSolutionStep()
            return self._ok

        def FinalizeSolutionStep(self):
            super().FinalizeSolutionStep()
            record(self, getattr(self, "_ok", False))

    model = KM.Model()
    stage = Stage(model, params)
    failure = None
    try:
        stage.Run()
    except Exception as exc:  # keep the partial trace
        failure = "%s: %s" % (type(exc).__name__, str(exc)[:500])
    elapsed = time.time() - t_start

    with open(os.path.join(out, "trace.csv"), "w", newline="", encoding="ascii") as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    end_time = params["problem_data"]["end_time"].GetDouble()
    loaded = [r for r in rows if max(abs(r["F_top_N_per_m"]), abs(r["F_bottom_N_per_m"])) > 0]
    Fmax = max((abs(r["F_bottom_N_per_m"]) for r in rows), default=0.0)
    big = [r for r in loaded if abs(r["F_bottom_N_per_m"]) >= 1e-2 * Fmax] if Fmax > 0 else []
    checks = {}
    checks["C_all_converged"] = bool(rows) and all(r["converged"] for r in rows) and failure is None
    checks["C_reached_end"] = bool(rows) and rows[-1]["time"] >= end_time * (1 - 1e-9)
    if static and big:
        bal = max(abs(abs(r["F_top_N_per_m"]) - abs(r["F_bottom_N_per_m"]))
                  / max(abs(r["F_top_N_per_m"]), abs(r["F_bottom_N_per_m"])) for r in big)
        checks["P1_force_balance_max"] = bal
        checks["P1_pass"] = bal <= 1e-3
    if big:
        p2y = max(abs(r["mean_syy_Pa"] - (-abs(r["F_bottom_N_per_m"]) * r["h_contact_m"] / r["area_m2"]))
                  / (abs(r["F_bottom_N_per_m"]) * r["h_contact_m"] / r["area_m2"]) for r in big)
        p2x = max(abs(r["mean_sxx_Pa"]) / abs(r["mean_syy_Pa"]) for r in big)
        checks.update({"P2_syy_identity_max": p2y, "P2_sxx_over_syy_max": p2x})
        if static:          # the identity assumes equilibrium without inertia
            checks["P2_pass"] = p2y <= 1e-2 and p2x <= 1e-2
        else:
            checks["P2_report_only_dynamic"] = True
    checks["boundary_segments_used_last"] = rows[-1]["boundary_segments_used"] if rows else 0
    checks["boundary_segments_expected"] = int(mesh["boundary_segments"])
    if args.elastic_small_strain and big and checks["boundary_segments_used_last"] == checks["boundary_segments_expected"]:
        target = E / (1 - nu * nu)
        sl = [r["mean_syy_Pa"] / r["mean_eyy"] for r in big if r["mean_eyy"] != 0]
        ra = [r["mean_exx"] / r["mean_eyy"] for r in big if r["mean_eyy"] != 0]
        checks.update({"P3_slope_rel_err_max": max(abs(s / target - 1) for s in sl),
                       "P3_ratio_rel_err_max": max(abs(x / (-nu / (1 - nu)) - 1) for x in ra)})
        checks["P3_pass"] = checks["P3_slope_rel_err_max"] <= 1e-2 and checks["P3_ratio_rel_err_max"] <= 2e-2
    if dim == 3 and big:
        p4 = max(abs((r["area_ratio"] - 1) - (r["mean_sxx_Pa"] + r["mean_syy_Pa"] + r["mean_szz_Pa"]) / (3 * K))
                 for r in big)
        checks.update({"P4_volume_minus_pressure_max": p4, "P4_pass": p4 <= 1e-3})

    summary = {
        "label": "DEVELOPMENT_ONLY", "arm": args.arm, "static": static, "dim": dim,
        "failure": failure, "elapsed_s": elapsed, "steps": len(rows),
        "final_approach_m": rows[-1]["approach_m"] if rows else None,
        "max_sigma_b_Pa": Fmax / mesh["D_m"] if Fmax else 0.0,
        "checks": checks,
        "inputs_sha256": {"params": sha256(params_path), "mdpa": sha256(mdpa + ".mdpa"),
                          "materials": sha256(mat), "mesh_json": sha256(mesh_json), "driver": sha256(here)},
        "mesh": mesh,
        "versions": {"kratos": KM.Kernel.Version(), "python": sys.version.split()[0],
                     "platform": platform.platform(), "omp_num_threads": os.environ.get("OMP_NUM_THREADS")},
        "notes": "forces per unit thickness; sigma_b = |F_bottom| / D (reg1 G1 readout)",
    }
    with open(os.path.join(out, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps({"arm": args.arm, "steps": len(rows), "failure": failure, "checks": checks}))
    return 0 if failure is None else 1


if __name__ == "__main__":
    sys.exit(main())
