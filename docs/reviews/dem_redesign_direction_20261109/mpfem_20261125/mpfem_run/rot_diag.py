# Development diagnostic (added after K-2 P5d failed): is the 3D finite-strain J2 law
# frame-indifferent, (a) for one sudden 30 deg rotation, (b) for the same rotation applied
# in small committed increments?  Control: hyperelastic law, sudden rotation, must be exact.
# usage: <venv python> -I rot_diag.py <step1_inputs dir> <out.json>
import json, math, sys

sys.path.insert(0, sys.argv[1])
import probe_kratos as PK  # constants, set_props
import KratosMultiphysics as KM
import KratosMultiphysics.StructuralMechanicsApplication  # noqa: F401
import KratosMultiphysics.ConstitutiveLawsApplication  # noqa: F401


def make(law_name, props):
    model = KM.Model()
    mp = model.CreateModelPart("mp")
    mp.ProcessInfo[KM.DOMAIN_SIZE] = 3
    h = 0.005
    pts = [(0, 0, 0), (h, 0, 0), (h, h, 0), (0, h, 0), (0, 0, h), (h, 0, h), (h, h, h), (0, h, h)]
    nds = [mp.CreateNewNode(i + 1, *p) for i, p in enumerate(pts)]
    geom = KM.Hexahedra3D8(*nds)
    prop = mp.CreateNewProperties(1)
    PK.set_props(KM, prop, props)
    cl = KM.KratosGlobals.GetConstitutiveLaw(law_name).Clone()
    prop.SetValue(KM.CONSTITUTIVE_LAW, cl)
    cl.Check(prop, geom, mp.ProcessInfo)
    N = KM.Vector(8)
    for i in range(8):
        N[i] = 1.0 / 8
    cl.InitializeMaterial(prop, geom, N)
    p = KM.ConstitutiveLawParameters()
    p.SetMaterialProperties(prop)
    p.SetElementGeometry(geom)
    p.SetProcessInfo(mp.ProcessInfo)
    p.SetShapeFunctionsValues(N)
    p.SetShapeFunctionsDerivatives(KM.Matrix(8, 3))
    opts = KM.Flags()
    opts.Set(KM.ConstitutiveLaw.COMPUTE_STRESS, True)
    opts.Set(KM.ConstitutiveLaw.COMPUTE_CONSTITUTIVE_TENSOR, True)
    p.SetOptions(opts)
    keep = {"model": model, "stress": KM.Vector(6), "strain": KM.Vector(6), "C": KM.Matrix(6, 6),
            "F": KM.Matrix(3, 3), "N": N, "geom": geom, "prop": prop}
    p.SetStressVector(keep["stress"])
    p.SetStrainVector(keep["strain"])
    p.SetConstitutiveMatrix(keep["C"])
    return cl, p, keep


def resp(cl, p, keep, lx, ly, th):
    c, s = math.cos(th), math.sin(th)
    F = keep["F"]
    for i in range(3):
        for j in range(3):
            F[i, j] = 0.0
    F[0, 0], F[0, 1], F[1, 0], F[1, 1], F[2, 2] = c * lx, -s * ly, s * lx, c * ly, 1.0
    p.SetDeformationGradientF(F)
    p.SetDeterminantF(lx * ly)
    cl.CalculateMaterialResponseCauchy(p)
    return [float(v) for v in p.GetStressVector()]


def back(sr, th):
    c, s = math.cos(th), math.sin(th)
    xx, yy, xy = sr[0], sr[1], sr[3]
    return (c * c * xx + s * s * yy + 2 * c * s * xy,
            s * s * xx + c * c * yy - 2 * c * s * xy,
            -c * s * xx + c * s * yy + (c * c - s * s) * xy, sr[2])


def compress(cl, p, keep, ly_end, nsteps=600):
    lx = 1.0
    for n in range(1, nsteps + 1):
        ly = 1.0 + (ly_end - 1.0) * n / nsteps
        a, b = lx, lx + 1e-4
        fa, fb = resp(cl, p, keep, a, ly, 0.0)[0], resp(cl, p, keep, b, ly, 0.0)[0]
        for _ in range(30):
            if abs(fb) < 1e-6 * PK.SY or fb == fa:
                break
            a, b, fa = b, b - fb * (b - a) / (fb - fa), fb
            fb = resp(cl, p, keep, b, ly, 0.0)[0]
        lx = b
        resp(cl, p, keep, lx, ly, 0.0)
        cl.FinalizeMaterialResponseCauchy(p)
    return lx


def case(law, props, ly_end, nrot, th_end=math.radians(30.0)):
    cl, p, keep = make(law, props)
    lx = compress(cl, p, keep, ly_end)
    s0 = resp(cl, p, keep, lx, ly_end, 0.0)
    for k in range(1, nrot + 1):
        th = th_end * k / nrot
        sr = resp(cl, p, keep, lx, ly_end, th)
        if k < nrot:
            cl.FinalizeMaterialResponseCauchy(p)
    b = back(sr, th_end)
    diff = max(abs(b[0] - s0[0]), abs(b[1] - s0[1]), abs(b[2] - s0[3]), abs(b[3] - s0[2]))
    return {"law": law, "ly_end": ly_end, "n_rot_steps": nrot, "max_abs_diff_Pa": diff,
            "diff_over_sigma_y": diff / PK.SY, "s0_xx_yy_zz_xy": [s0[0], s0[1], s0[2], s0[3]]}


out = {"label": "DEVELOPMENT_ONLY", "added_after": "K-2 P5d failed (sudden 30 deg)", "cases": []}
elastic_props = {"YOUNG_MODULUS": PK.E, "POISSON_RATIO": PK.NU, "DENSITY": PK.RHO}
for nrot in (1,):
    out["cases"].append(case("HyperElastic3DLaw", elastic_props, 0.99, nrot))
for nrot in (1, 30, 300):
    out["cases"].append(case("FiniteStrainIsotropicPlasticity3DVonMisesVonMises", PK.PROPS_FINITE_J2, 0.85, nrot))
out["cases"].append(case("FiniteStrainIsotropicPlasticity3DVonMisesVonMises", PK.PROPS_FINITE_J2, 0.999, 1))
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
for c in out["cases"]:
    print(c["law"][:40], "ly", c["ly_end"], "steps", c["n_rot_steps"], "diff/sy", f'{c["diff_over_sigma_y"]:.3e}')
