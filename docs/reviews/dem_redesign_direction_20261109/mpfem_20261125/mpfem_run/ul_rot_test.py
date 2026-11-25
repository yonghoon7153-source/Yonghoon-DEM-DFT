# Development test (1저자 11-25 choice (나)): element-level rigid-rotation check after plastic flow.
# Criteria fixed BEFORE the run:
#   R1  gradual 30 deg rotation in 300 committed steps: max |Q^T sigma Q - sigma_before| <= 1e-3 * sigma_y
#   R2  end of compression: Cauchy von Mises sigma_eq within +-2 % of sigma_y (perfect plasticity)
#   control C1 (finite-strain J2 + TL element) is expected to FAIL R1 (reproduces the material-point result)
# Path: isochoric plane-strain compression F = diag(1/ly, ly, 1), ly 1 -> 0.85 in 100 steps, then rotation.
# usage: <venv python> -I ul_rot_test.py <step1_inputs dir> <out.json>
import json, math, sys

sys.path.insert(0, sys.argv[1])
import probe_kratos as PK
import KratosMultiphysics as KM
import KratosMultiphysics.StructuralMechanicsApplication  # noqa: F401
import KratosMultiphysics.ConstitutiveLawsApplication  # noqa: F401

H = 0.005
X0 = [(0, 0, 0), (H, 0, 0), (H, H, 0), (0, H, 0), (0, 0, H), (H, 0, H), (H, H, H), (0, H, H)]


def build(elem_name, law_name, props):
    model = KM.Model()
    mp = model.CreateModelPart("mp", 2)
    mp.AddNodalSolutionStepVariable(KM.DISPLACEMENT)
    mp.AddNodalSolutionStepVariable(KM.REACTION)
    mp.AddNodalSolutionStepVariable(KM.VOLUME_ACCELERATION)
    mp.ProcessInfo[KM.DOMAIN_SIZE] = 3
    mp.ProcessInfo[KM.DELTA_TIME] = 1.0
    for i, p in enumerate(X0):
        mp.CreateNewNode(i + 1, *p)
    for v, r in ((KM.DISPLACEMENT_X, KM.REACTION_X), (KM.DISPLACEMENT_Y, KM.REACTION_Y), (KM.DISPLACEMENT_Z, KM.REACTION_Z)):
        KM.VariableUtils().AddDof(v, r, mp)
    prop = mp.CreateNewProperties(1)
    unreg = PK.set_props(KM, prop, props)
    prop.SetValue(KM.CONSTITUTIVE_LAW, KM.KratosGlobals.GetConstitutiveLaw(law_name).Clone())
    el = mp.CreateNewElement(elem_name, 1, list(range(1, 9)), prop)
    sch = KM.ResidualBasedIncrementalUpdateStaticScheme()
    sch.Initialize(mp)
    if not sch.ElementsAreInitialized():
        sch.InitializeElements(mp)
    return model, mp, el, unreg, sch


def step(mp, el, sch, F, t):
    mp.CloneTimeStep(t)
    mp.ProcessInfo[KM.STEP] = int(t)
    for i, node in enumerate(mp.Nodes):
        x0 = X0[node.Id - 1]
        x = [sum(F[a][b] * x0[b] for b in range(3)) for a in range(3)]
        u = KM.Array3([x[0] - x0[0], x[1] - x0[1], x[2] - x0[2]])
        node.SetSolutionStepValue(KM.DISPLACEMENT, 0, u)
        node.X, node.Y, node.Z = x[0], x[1], x[2]
    pi = mp.ProcessInfo
    A, Dx, b = KM.CompressedMatrix(), KM.Vector(), KM.Vector()
    sch.InitializeSolutionStep(mp, A, Dx, b)
    sch.InitializeNonLinIteration(mp, A, Dx, b)
    lhs, rhs = KM.Matrix(), KM.Vector()
    el.CalculateLocalSystem(lhs, rhs, pi)
    sch.FinalizeNonLinIteration(mp, A, Dx, b)
    sig = el.CalculateOnIntegrationPoints(KM.CAUCHY_STRESS_VECTOR, pi)
    sch.FinalizeSolutionStep(mp, A, Dx, b)
    n = len(sig)
    return [sum(float(s[k]) for s in sig) / n for k in range(6)]


def Fmat(ly, th):
    c, s = math.cos(th), math.sin(th)
    lx = 1.0 / ly
    return [[c * lx, -s * ly, 0.0], [s * lx, c * ly, 0.0], [0.0, 0.0, 1.0]]


def seq(sv):
    xx, yy, zz, xy, yz, xz = sv
    return math.sqrt(0.5 * ((xx - yy) ** 2 + (yy - zz) ** 2 + (zz - xx) ** 2) + 3 * (xy * xy + yz * yz + xz * xz))


def back(sv, th):
    c, s = math.cos(th), math.sin(th)
    xx, yy, zz, xy = sv[0], sv[1], sv[2], sv[3]
    return [c * c * xx + s * s * yy + 2 * c * s * xy, s * s * xx + c * c * yy - 2 * c * s * xy, zz,
            -c * s * xx + c * s * yy + (c * c - s * s) * xy]


def run_case(tag, elem_name, law_name, props, nrot):
    model, mp, el, unreg, sch = build(elem_name, law_name, props)
    t = 0
    ly_end, n1 = 0.85, 100
    for k in range(1, n1 + 1):
        t += 1
        s_before = step(mp, el, sch, Fmat(1.0 + (ly_end - 1.0) * k / n1, 0.0), t)
    th_end = math.radians(30.0)
    for k in range(1, nrot + 1):
        t += 1
        s_after = step(mp, el, sch, Fmat(ly_end, th_end * k / nrot), t)
    b = back(s_after, th_end)
    ref = [s_before[0], s_before[1], s_before[2], s_before[3]]
    diff = max(abs(b[i] - ref[i]) for i in range(4))
    se = seq(s_before)
    return {"tag": tag, "element": elem_name, "law": law_name, "n_rot_steps": nrot,
            "unregistered_variables": unreg, "sigma_before_xx_yy_zz_xy": ref,
            "sigma_eq_end_over_sy": se / PK.SY, "rot_max_abs_diff_over_sy": diff / PK.SY,
            "R1_pass": (diff <= 1e-3 * PK.SY) if nrot >= 300 else None,
            "R2_pass": abs(se / PK.SY - 1.0) <= 0.02}


SMALL_GENERIC = dict(PK.PROPS_FINITE_J2)
cases = [
    ("C1_control_finite_TL", "TotalLagrangianElement3D8N", "FiniteStrainIsotropicPlasticity3DVonMisesVonMises", PK.PROPS_FINITE_J2),
    ("C2_smallgeneric_UL", "UpdatedLagrangianElement3D8N", "SmallStrainIsotropicPlasticity3DVonMisesVonMises", SMALL_GENERIC),
    ("C3_smallJ2_UL", "UpdatedLagrangianElement3D8N", "SmallStrainJ2Plasticity3DLaw", PK.PROPS_SMALL_J2),
]
out = {"label": "DEVELOPMENT_ONLY", "criteria": "R1 <= 1e-3 sy after 300-step 30 deg; R2 sigma_eq within 2 % of sy",
       "results": []}
for tag, en, ln, pr in cases:
    for nrot in (300, 1):
        try:
            out["results"].append(run_case(tag, en, ln, pr, nrot))
        except Exception as exc:
            out["results"].append({"tag": tag, "n_rot_steps": nrot, "error": repr(exc)[:400]})
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
for r in out["results"]:
    if "error" in r:
        print(r["tag"], r["n_rot_steps"], "ERROR", r["error"][:200])
    else:
        print(r["tag"], "rot", r["n_rot_steps"], "diff/sy", f'{r["rot_max_abs_diff_over_sy"]:.3e}',
              "seq/sy", f'{r["sigma_eq_end_over_sy"]:.4f}', "R1", r["R1_pass"], "R2", r["R2_pass"])
