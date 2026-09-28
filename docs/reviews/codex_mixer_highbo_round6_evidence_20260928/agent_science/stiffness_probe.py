"""Synthetic contact/generator arithmetic only; never runs a DEM executable.

Imports the pinned mirror without bytecode or source mutation. The force and
energy calculations below use the generator's small-overlap SJKR approximation,
not a claim that finite-overlap sjkr or a loaded contact network is invariant.
"""
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
source = Path(__file__).resolve().parents[1] / "scripts" / "make_mixer_deck.py"
spec = importlib.util.spec_from_file_location("generator", source)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def state(multiplier):
    g.E_PHASE["SE"] = 1e7 * multiplier
    p = g.plan(100000, cgf=151.4)
    nus = {t: g.PHASE_MECH[t][0] for t in g.TYPES}
    nus["WALL"] = g.WALL_NU
    radii = {t: p["d"][t] / 2 for t in g.TYPES}
    rayleigh = {}
    for t in g.TYPES:
        nu, mat = g.PHASE_MECH[t]
        shear = g.E_PHASE[t] / (2 * (1 + nu))
        rayleigh[t] = .2 * math.pi * radii[t] * math.sqrt(g.DENS[mat] * 1000 / shear) / (.1631 * nu + .8766)
    output = {"SE_multiplier": multiplier, "plan_dt_s": p["dt"], "deck_dt_s": float(f'{p["dt"]:.4g}'),
              "rayleigh20_by_phase_s": rayleigh, "dt_min_phase": min(rayleigh, key=rayleigh.get),
              "diameters_m": p["d"], "R_m": p["R"], "pairs": {}, "CED_matrices_J_m3": {}}
    for arm in ("LC", "LH"):
        matrix = g.ced_matrix(arm, p["d"])
        output["CED_matrices_J_m3"][arm] = matrix
        output["pairs"][arm] = {}
        names = g.TYPES + ("WALL",)
        for i, a in enumerate(g.TYPES):
            for j in range(i, len(names)):
                b = names[j]
                estar = 1 / ((1-nus[a]**2)/g.E_PHASE[a] + (1-nus[b]**2)/g.E_PHASE[b])
                rstar = radii[a] if b == "WALL" else radii[a]*radii[b]/(radii[a]+radii[b])
                A = 4/3 * estar * math.sqrt(rstar)
                B = 2*math.pi*rstar*matrix[i][j]
                delta0 = (B/A)**2
                force0 = B*delta0
                # Net-force minimum is 4/27 of the zero-load adhesive force.
                pull_off = 4/27 * force0
                # Work from stable overlap delta0 to zero for F=A*d^1.5-B*d.
                separation_energy = B*delta0**2/10
                output["pairs"][arm][a+"--"+b] = {"E_star_Pa": estar, "CED_J_m3": matrix[i][j],
                    "adhesive_equilibrium_overlap_m": delta0, "adhesive_equilibrium_force_N": force0,
                    "pull_off_N": pull_off, "separation_energy_J": separation_energy}
    return output

base, stiff = state(1), state(14)
ratios = {}
for arm in base["pairs"]:
    ratios[arm] = {}
    for pair, original in base["pairs"][arm].items():
        changed = stiff["pairs"][arm][pair]
        ratios[arm][pair] = {k: changed[k]/v for k,v in original.items()}
        ratios[arm][pair]["fixed_load_overlap_ratio"] = ratios[arm][pair]["E_star_Pa"]**(-2/3)
        ratios[arm][pair]["fixed_velocity_elastic_impact_overlap_ratio"] = ratios[arm][pair]["E_star_Pa"]**(-2/5)
worst_original = .05763
scale = ratios["LC"]["AM_P--SE"]["E_star_Pa"]
required_mixed_scale = (worst_original/.01)**1.5
required_mixed_estar = base["pairs"]["LC"]["AM_P--SE"]["E_star_Pa"]*required_mixed_scale
required_E_SE = (1-.30**2)/(1/required_mixed_estar - (1-.25**2)/g.E_PHASE["AM_P"])
output = {"scope": "synthetic arithmetic only; no simulation or campaign-frame reads",
          "base": base, "stiff": stiff, "ratios": ratios,
          "overall_dt_shrink": base["plan_dt_s"]/stiff["plan_dt_s"],
          "SE14_fixed_load_projected_max_delta_over_rmin": worst_original*scale**(-2/3),
          "SE14_fixed_velocity_elastic_impact_projected_max_delta_over_rmin": worst_original*scale**(-2/5),
          "SE_multiplier_for_fixed_load_projected_1pct_from_known_mixed_max": required_E_SE/1e7,
          "assumptions": ["No network-force or velocity redistribution", "Same geometry, mass, Poisson ratios",
              "Exact generator CED output; contact force ratios use small-overlap SJKR", "Baseline observed maximum is development data, not prediction validation"]}
if "--compact" in sys.argv:
    compact = {k: v for k,v in output.items() if k not in ("base", "stiff", "ratios")}
    for key, data in (("base", base), ("stiff", stiff)):
        compact[key] = {k:v for k,v in data.items() if k != "pairs"}
    compact["changed_pair_ratios"] = {k:v for k,v in ratios["LC"].items() if "SE" in k}
    print(json.dumps(compact, indent=2))
else:
    print(json.dumps(output, indent=2))
