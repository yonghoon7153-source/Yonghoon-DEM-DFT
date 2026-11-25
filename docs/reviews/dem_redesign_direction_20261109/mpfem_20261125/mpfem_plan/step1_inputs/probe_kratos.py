#!/usr/bin/env python3
"""Step-1 capability probe + material-point test for Kratos 10.4.4.

DRAFT for the MPFEM plan.  Written but NOT executed by its author.

K-1  imports, version, constitutive-law registry (HasConstitutiveLaw),
     element / condition names (read a one-cell .mdpa per name).
K-2  material-point tests, no element and no contact:
     plane-strain uniaxial compression  (sigma_xx = 0, eps_zz = 0, rate free)
     3D finite-strain law : F = diag(lx, ly, 1), lx solved so that sigma_xx = 0
     2D small-strain law  : strain vector [exx, eyy, 0], exx solved likewise
     + objectivity: after loading, F' = Q F (Q = 30 deg about z) must give
       Q^T sigma' Q = sigma (trial call, nothing committed).
Hand-check targets for E 10 MPa, nu 0.45, sigma_y 0.4 MPa, no hardening
(our arithmetic, small elastic strain):
     elastic slope  E/(1-nu^2)            = 12.539 MPa
     first yield    sigma_y/sqrt(1-nu+nu^2) = 0.46111 MPa  (elastic sigma_zz = nu sigma_yy)
     plateau        2 sigma_y/sqrt(3)      = 0.46188 MPa  (plane-strain J2 limit)
Variables of the plasticity laws are partly guessed ([추정] in step1 doc);
Check() errors are recorded verbatim so the next attempt can fix them.
Output: probe_report.json in the working directory.
"""
import argparse
import json
import math
import os
import tempfile
import traceback

E, NU, SY, RHO = 1.0e7, 0.45, 4.0e5, 1000.0
SLOPE = E / (1 - NU * NU)
YIELD1 = SY / math.sqrt(1 - NU + NU * NU)
PLATEAU = 2 * SY / math.sqrt(3)

LAWS = [
    "FiniteStrainIsotropicPlasticity3DVonMisesVonMises",
    "FiniteStrainIsotropicPlasticityPlaneStrainVonMisesVonMises",   # expected absent (binary strings)
    "FiniteStrainIsotropicPlasticityPlaneStressVonMisesVonMises",
    "SmallStrainJ2PlasticityPlaneStrain2DLaw",
    "SmallStrainJ2Plasticity3DLaw",
    "SmallStrainIsotropicPlasticityPlaneStrainVonMisesVonMises",
    "SmallStrainIsotropicPlasticity3DVonMisesVonMises",
    "PlasticityIsotropicKinematicJ2Law",
    "HyperElastic3DLaw",
    "HyperElasticPlaneStrain2DLaw",
    "LinearElastic3DLaw",
    "LinearElasticPlaneStrain2DLaw",
]
ELEMENTS_2D = ["SmallDisplacementBbarElement2D4N", "SmallDisplacementElement2D4N",
               "TotalLagrangianElement2D4N", "UpdatedLagrangianElement2D4N",
               "TotalLagrangianQ1P0MixedElement2D4N"]
ELEMENTS_3D = ["TotalLagrangianQ1P0MixedElement3D8N", "UpdatedLagrangianElement3D8N",
               "TotalLagrangianElement3D8N"]
CONDITIONS = {"LineCondition2D2N": 2, "SurfaceCondition3D4N": 3}

PROPS_FINITE_J2 = {"YOUNG_MODULUS": E, "POISSON_RATIO": NU, "DENSITY": RHO,
                   "YIELD_STRESS": SY, "YIELD_STRESS_TENSION": SY, "YIELD_STRESS_COMPRESSION": SY,
                   "HARDENING_CURVE": 3, "FRACTURE_ENERGY": 1.0e10}
PROPS_SMALL_J2 = {"YOUNG_MODULUS": E, "POISSON_RATIO": NU, "DENSITY": RHO, "THICKNESS": 1.0,
                  "YIELD_STRESS": SY, "ISOTROPIC_HARDENING_MODULUS": 0.0,
                  "EXPONENTIAL_SATURATION_YIELD_STRESS": SY, "HARDENING_EXPONENT": 1.0}


def write_cell_mdpa(path, name, dim, kind):
    if dim == 2:
        nodes = [(1, 0, 0), (2, 1, 0), (3, 1, 1), (4, 0, 1)]
        conn = "1 2 3 4"
        cconn = "1 2"
    else:
        nodes = [(1, 0, 0, 0), (2, 1, 0, 0), (3, 1, 1, 0), (4, 0, 1, 0),
                 (5, 0, 0, 1), (6, 1, 0, 1), (7, 1, 1, 1), (8, 0, 1, 1)]
        conn = "1 2 3 4 5 6 7 8"
        cconn = "1 2 3 4"
    with open(path, "w", encoding="ascii") as f:
        f.write("Begin ModelPartData\nEnd ModelPartData\nBegin Properties 1\nEnd Properties\nBegin Nodes\n")
        for n in nodes:
            c = list(n[1:]) + [0] * (3 - len(n[1:]))
            f.write("%d %g %g %g\n" % (n[0], c[0], c[1], c[2]))
        f.write("End Nodes\n")
        if kind == "element":
            f.write("Begin Elements %s\n1 1 %s\nEnd Elements\n" % (name, conn))
        else:
            f.write("Begin Conditions %s\n1 1 %s\nEnd Conditions\n" % (name, cconn))


def can_read(KM, name, dim, kind, tmp):
    base = os.path.join(tmp, "%s_%s" % (kind, name))
    write_cell_mdpa(base + ".mdpa", name, dim, kind)
    model = KM.Model()
    mp = model.CreateModelPart("t")
    mp.ProcessInfo[KM.DOMAIN_SIZE] = dim
    mp.AddNodalSolutionStepVariable(KM.DISPLACEMENT)
    try:
        KM.ModelPartIO(base).ReadModelPart(mp)
        return {"ok": True}
    except Exception as exc:  # unregistered name -> reader error
        return {"ok": False, "error": str(exc).splitlines()[0][:300]}


def set_props(KM, prop, values):
    """Set the values whose variables are registered; return the names that are not."""
    missing = []
    for name, val in values.items():
        if not KM.KratosGlobals.HasVariable(name):
            missing.append(name)
            continue
        var = KM.KratosGlobals.GetVariable(name)
        prop.SetValue(var, int(val) if KM.KratosGlobals.GetVariableType(name) == "Integer" else float(val))
    return missing


def mat_point(KM, law_name, dim, props, h=0.005, nsteps=600, ly_end=0.85):
    """Plane-strain uniaxial path; returns dict with curve and checks."""
    model = KM.Model()
    mp = model.CreateModelPart("mp")
    mp.ProcessInfo[KM.DOMAIN_SIZE] = dim
    if dim == 3:
        pts = [(0, 0, 0), (h, 0, 0), (h, h, 0), (0, h, 0), (0, 0, h), (h, 0, h), (h, h, h), (0, h, h)]
        nds = [mp.CreateNewNode(i + 1, *p) for i, p in enumerate(pts)]
        geom = KM.Hexahedra3D8(*nds)
    else:
        pts = [(0, 0, 0), (h, 0, 0), (h, h, 0), (0, h, 0)]
        nds = [mp.CreateNewNode(i + 1, *p) for i, p in enumerate(pts)]
        geom = KM.Quadrilateral2D4(*nds)
    prop = mp.CreateNewProperties(1)
    out = {"law": law_name, "check_rc": None, "unregistered_variables": set_props(KM, prop, props)}
    cl = KM.KratosGlobals.GetConstitutiveLaw(law_name).Clone()
    nsz = int(cl.GetStrainSize())          # fix 1: plane strain = 4 (xx yy zz xy) · 3D = 6
    out_nsz = nsz
    prop.SetValue(KM.CONSTITUTIVE_LAW, cl)
    out["check_rc"] = int(cl.Check(prop, geom, mp.ProcessInfo))
    npt = len(nds)
    N = KM.Vector(npt)
    for i in range(npt):
        N[i] = 1.0 / npt
    cl.InitializeMaterial(prop, geom, N)
    p = KM.ConstitutiveLawParameters()
    p.SetMaterialProperties(prop)
    p.SetElementGeometry(geom)
    p.SetProcessInfo(mp.ProcessInfo)
    p.SetShapeFunctionsValues(N)
    p.SetShapeFunctionsDerivatives(KM.Matrix(npt, dim))
    opts = KM.Flags()
    opts.Set(KM.ConstitutiveLaw.COMPUTE_STRESS, True)
    opts.Set(KM.ConstitutiveLaw.COMPUTE_CONSTITUTIVE_TENSOR, True)
    opts.Set(KM.ConstitutiveLaw.USE_ELEMENT_PROVIDED_STRAIN, dim == 2)
    p.SetOptions(opts)
    stress, strain, Cm = KM.Vector(nsz), KM.Vector(nsz), KM.Matrix(nsz, nsz)
    p.SetStressVector(stress)
    p.SetStrainVector(strain)
    p.SetConstitutiveMatrix(Cm)
    Fk = KM.Matrix(3, 3) if dim == 3 else KM.Matrix(2, 2)   # fix 2: keep F alive (Parameters holds a pointer)
    evk = KM.Vector(nsz)                                      # fix 2: keep 2D strain alive

    def response(lx, ly, rot=0.0):
        """Cauchy stress for F = Q diag(lx, ly, 1) (3D) or small strain (2D)."""
        if dim == 3:
            c, s = math.cos(rot), math.sin(rot)
            F = Fk
            for i in range(3):
                for j in range(3):
                    F[i, j] = 0.0
            F[0, 0], F[0, 1], F[1, 0], F[1, 1], F[2, 2] = c * lx, -s * ly, s * lx, c * ly, 1.0
            p.SetDeformationGradientF(F)
            p.SetDeterminantF(lx * ly)
        else:
            ev = evk
            for i in range(nsz):
                ev[i] = 0.0
            ev[0], ev[1] = lx - 1.0, ly - 1.0
            p.SetStrainVector(ev)
            F = Fk
            F[0, 0], F[0, 1], F[1, 0], F[1, 1] = lx, 0.0, 0.0, ly
            p.SetDeformationGradientF(F)
            p.SetDeterminantF(lx * ly)
        cl.CalculateMaterialResponseCauchy(p)
        return [float(v) for v in p.GetStressVector()]

    curve, lx = [], 1.0
    for n in range(1, nsteps + 1):
        ly = 1.0 + (ly_end - 1.0) * n / nsteps
        a, b = lx, lx + 1e-4
        fa, fb = response(a, ly)[0], response(b, ly)[0]
        for _ in range(30):                        # secant on sigma_xx(lx) = 0
            if abs(fb) < 1e-6 * SY or fb == fa:
                break
            a, b, fa = b, b - fb * (b - a) / (fb - fa), fb
            fb = response(b, ly)[0]
        lx = b
        sig = response(lx, ly)
        cl.FinalizeMaterialResponseCauchy(p)
        if dim == 3:
            sxx, syy, szz, sxy = sig[0], sig[1], sig[2], sig[3]
        else:
            if nsz == 4:                           # fix 1: plane strain law returns sigma_zz
                sxx, syy, szz, sxy = sig[0], sig[1], sig[2], sig[3]
            else:
                sxx, syy, sxy = sig
                szz = NU * (sxx + syy)             # elastic estimate only
        seq = math.sqrt(0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2) + 3 * sxy ** 2)
        curve.append({"ly": ly, "lx": lx, "sxx": sxx, "syy": syy, "szz": szz, "seq": seq})

    eyy = [c["ly"] - 1.0 for c in curve]
    syy = [c["syy"] for c in curve]
    k = 1                                          # eps_yy = -5e-4 with the default path
    slope = syy[k] / eyy[k]
    first = None
    for i in range(1, len(curve)):
        s0, s1 = curve[i - 1]["seq"], curve[i]["seq"]
        if s0 < 0.999 * SY <= s1:
            w = (0.999 * SY - s0) / (s1 - s0)
            first = abs(syy[i - 1] + w * (syy[i] - syy[i - 1])) / 0.999
            break
    out.update({
        "strain_size": out_nsz,
        "slope_Pa": slope, "slope_target_Pa": SLOPE, "slope_rel_err": slope / SLOPE - 1,
        "first_yield_abs_syy_Pa": first, "first_yield_target_Pa": YIELD1,
        "plateau_abs_syy_Pa": abs(syy[-1]), "plateau_target_Pa": PLATEAU,
        "curve_every_10": curve[::10],
    })
    # tolerances = development policy values (step1 doc section 4): finite strain looser
    out["P5a_slope"] = abs(out["slope_rel_err"]) <= 5e-3
    out["P5b_first_yield"] = first is not None and abs(first / YIELD1 - 1) <= (1e-2 if dim == 3 else 5e-3)
    out["P5c_plateau"] = abs(abs(syy[-1]) / PLATEAU - 1) <= (2e-2 if dim == 3 else 5e-3)
    if dim == 3:
        # objectivity at the final committed state (trial calls, nothing finalized)
        lxf, lyf = curve[-1]["lx"], curve[-1]["ly"]
        s0 = response(lxf, lyf, 0.0)
        th = math.radians(30.0)
        sr = response(lxf, lyf, th)
        c, s = math.cos(th), math.sin(th)
        # back-rotate sr (Voigt xx,yy,zz,xy,yz,xz) by Q^T about z
        xx, yy, xy = sr[0], sr[1], sr[3]
        bxx = c * c * xx + s * s * yy + 2 * c * s * xy
        byy = s * s * xx + c * c * yy - 2 * c * s * xy
        bxy = -c * s * xx + c * s * yy + (c * c - s * s) * xy
        diff = max(abs(bxx - s0[0]), abs(byy - s0[1]), abs(bxy - s0[3]), abs(sr[2] - s0[2]))
        out["objectivity_max_abs_diff_Pa"] = diff
        out["P5d_objectivity"] = diff <= 1e-6 * SY
        out["rotation_check_state_ly"] = lyf
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="probe_report.json")
    ap.add_argument("--law3d", default="FiniteStrainIsotropicPlasticity3DVonMisesVonMises")
    ap.add_argument("--law2d", default="SmallStrainJ2PlasticityPlaneStrain2DLaw")
    args = ap.parse_args()
    rep = {"label": "DEVELOPMENT_ONLY", "step": "K-1/K-2", "targets_Pa": {
        "slope": SLOPE, "first_yield": YIELD1, "plateau": PLATEAU}}
    import KratosMultiphysics as KM
    rep["imports"] = {}
    for app in ("StructuralMechanicsApplication", "ContactStructuralMechanicsApplication",
                "ConstitutiveLawsApplication", "LinearSolversApplication", "MeshingApplication"):
        try:
            __import__("KratosMultiphysics." + app)
            rep["imports"][app] = True
        except Exception as exc:
            rep["imports"][app] = "FAIL: " + str(exc)[:200]
    rep["kratos_version"] = KM.Kernel.Version()
    rep["laws"] = {n: bool(KM.KratosGlobals.HasConstitutiveLaw(n)) for n in LAWS + [args.law3d, args.law2d]}
    with tempfile.TemporaryDirectory() as tmp:
        rep["elements"] = {n: can_read(KM, n, 2, "element", tmp) for n in ELEMENTS_2D}
        rep["elements"].update({n: can_read(KM, n, 3, "element", tmp) for n in ELEMENTS_3D})
        rep["conditions"] = {n: can_read(KM, n, d, "condition", tmp) for n, d in CONDITIONS.items()}
    rep["material_point"] = {}
    for key, law, dim, props in (("3d_finite_J2", args.law3d, 3, PROPS_FINITE_J2),
                                 ("2d_small_J2", args.law2d, 2, PROPS_SMALL_J2)):
        if not rep["laws"][law]:
            rep["material_point"][key] = {"law": law, "skipped": "law not registered"}
            continue
        try:
            rep["material_point"][key] = mat_point(KM, law, dim, props)
        except Exception:
            rep["material_point"][key] = {"law": law, "error": traceback.format_exc()[-1500:]}
    usable_3d = [n for n in ELEMENTS_3D if rep["elements"][n]["ok"]]
    rep["usable_3d_elements_in_order"] = usable_3d       # Q1P0 first (anti-locking), then UL, TL
    k1 = (all(v is True for v in rep["imports"].values())
          and rep["laws"].get(args.law3d) is True
          and bool(usable_3d)
          and rep["conditions"]["SurfaceCondition3D4N"]["ok"])
    mp3 = rep["material_point"].get("3d_finite_J2", {})
    k2 = all(mp3.get(k) is True for k in ("P5a_slope", "P5b_first_yield", "P5c_plateau", "P5d_objectivity"))
    rep["K1_pass"], rep["K2_pass"] = bool(k1), bool(k2)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=1)
    print(json.dumps({"K1_pass": rep["K1_pass"], "K2_pass": rep["K2_pass"],
                      "laws_missing": [n for n, v in rep["laws"].items() if not v]}))


if __name__ == "__main__":
    main()
