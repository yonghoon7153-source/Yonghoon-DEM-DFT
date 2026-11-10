"""Read-only review arithmetic. Synthetic curves only; no solver or project import.
The numbers are logical counterexamples to sufficiency, not simulated material data.
"""
import json
from pathlib import Path

out = Path(__file__).resolve().parent

def grade(r):
    if r >= 1.3:
        return "different"
    if 1 / 1.15 <= r <= 1.15:
        return "same"
    if r <= 1 / 1.3:
        return "opposite"
    return "intermediate"

# Repeat each value at all three paired packings and at >=2 comparison points.
# F has zero mesh error; S has first-order error. Both share the same nominal mesh.
mesh = []
for n in (8, 12, 16, 24, 48, 1000000000):
    r = 1.10 + 3.36 / n
    mesh.append({"cells_per_diameter": n, "S_over_F": r, "grade": grade(r),
                 "F_phi_m": 0.94})

# Monotone pressure curves, with deformed-volume ordinate requiring >= pressure.
definition = []
for phi, pref, rm, rd in ((0.90, 0.68, 0.60, 1.00), (0.95, 1.11, 1.00, 1.50)):
    definition.append({"phi": phi, "paper_pressure_MPa": pref,
        "mass_ratio": rm, "deformed_ratio": rd,
        "mass_pressure_MPa": pref * rm, "deformed_pressure_MPa": pref * rd,
        "pointwise_or_pass": (0.7 <= rm <= 1.4) or (0.7 <= rd <= 1.4)})

# Tangential equal/opposite impulses preserve momentum but can create energy.
m = 1.0
v0 = (1.0, -1.0)
v1 = (1.1, -1.1)
energy = {"momentum_before": sum(m * v for v in v0),
          "momentum_after": sum(m * v for v in v1),
          "kinetic_before": sum(0.5 * m * v * v for v in v0),
          "kinetic_after": sum(0.5 * m * v * v for v in v1),
          "interpretation": "Necessary extra energy/Coulomb check; not a full U5 solver run"}

result = {"scope": "synthetic arithmetic, zero solver runs", "mesh_grade_counterexample": mesh,
    "definition_OR_counterexample": definition,
    "global_mass_definition_pass": all(0.7 <= d["mass_ratio"] <= 1.4 for d in definition),
    "global_deformed_definition_pass": all(0.7 <= d["deformed_ratio"] <= 1.4 for d in definition),
    "momentum_not_dissipativity": energy,
    "effect_modification": {"R_at_2D_test": 1.1, "grade_at_2D_test": grade(1.1),
        "R_at_unobserved_3D_target": 1.5, "grade_at_3D_target": grade(1.5),
        "interpretation": "Logical potential-response example; no predicted or measured 3D values"}}
assert mesh[1]["grade"] == mesh[2]["grade"] == "different"
assert mesh[-1]["grade"] == "same"
assert all(d["pointwise_or_pass"] for d in definition)
assert not result["global_mass_definition_pass"] and not result["global_deformed_definition_pass"]
assert energy["momentum_before"] == energy["momentum_after"]
assert energy["kinetic_after"] > energy["kinetic_before"]
(out / "counterexamples.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("Synthetic arithmetic assertions passed; zero solver runs.")
