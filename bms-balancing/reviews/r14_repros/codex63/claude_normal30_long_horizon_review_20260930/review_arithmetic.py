"""Reviewer-owned, offline data arithmetic. Does not import or execute supplied code."""
import bisect
import csv
import hashlib
import json
import math
import re
import time
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 50
D = Decimal
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BASE = ROOT / "outputs/normal30_native_review_20260930"
DATA = BASE / "received/run/tables"
JAVA = BASE / "received/candidate/src/Normal30Candidate.java"
CLAUDE = Path("C:/Users/Administrator/Downloads/CLAUDE_REPLY_NORMAL30_LONG_HORIZON_KO_v2.md")
started = time.monotonic()
paths = [CLAUDE, JAVA, BASE / "NUMERIC_AUDIT.json", BASE / "REVIEW_KO.md",
         BASE / "received/run/batch_RETURN.json", BASE / "received/run/compile_RETURN.json",
         BASE / "received/run/OUTPUT_MPH_IDENTITY.json"]
paths += [DATA / n for n in ["preflight_global.csv", "preflight_boundary1.csv", "preflight_boundary4.csv",
          "preflight_MinLine_ce.csv", "preflight_MaxLine_ce.csv", "electrolyte_guard.csv",
          "axes_profile_N.csv", "axes_profile_P.csv", "axes_runtime_settings.csv"]]

def identity(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return {"path": str(p), "bytes": p.stat().st_size, "sha256": h.hexdigest()}

before = [identity(p) for p in paths]
prior = json.loads((BASE / "NUMERIC_AUDIT.json").read_text(encoding="utf-8-sig"))
pin_results = []
for p in paths:
    if p.parent == DATA:
        pin = prior["embedded_table_identities"].get(p.name)
        now = identity(p)
        pin_results.append({"file": p.name, "matches_prior_embedded_csv_identity": bool(pin and all(now[k] == pin[k] for k in ("bytes", "sha256")))})
assert all(x["matches_prior_embedded_csv_identity"] for x in pin_results)

def rows(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return [{k: D(v) for k, v in r.items()} for r in csv.DictReader(f)]

g, n, p = (rows(x) for x in ("preflight_global.csv", "preflight_boundary1.csv", "preflight_boundary4.csv"))
assert [r["time_s"] for r in g] == [r["time_s"] for r in n] == [r["time_s"] for r in p]
assert len(g) == 1237 and g[-1]["time_s"] == 30
gm, nm, pm = ({r["time_s"]: r for r in x} for x in (g, n, p))
source = JAVA.read_text(encoding="utf-8-sig")

# Source parameters are checked against literal definitions before using SI values.
checks = {"L_el": "52[um]", "L_sep": "25[um]", "L_pos": "44[um]", "epss_el_0": "0.63122",
          "epss_pos_0": "0.58803", "LAM_NE": "0.0257219788", "LAM_PE": "0.0296398242",
          "cs_Gr_max": "31507[mol/m^3]", "cs_NCM_max": "50707.7[mol/m^3]", "F_ref": "96485.33212[C/mol]",
          "rp_Gr": "7.5[um]", "rp_NCM": "10[um]", "D_g": "7.1e-15[m^2/s]", "D_NCM": "1e-13[m^2/s]",
          "C_rate": "0.1", "sigma_short": "1e-20[S/m]"}
for key, value in checks.items():
    assert '{"' + key + '","' + value + '"}' in source, (key, value)
F = D("96485.33212")
epsN = D("0.63122") * (1 - D("0.0257219788"))
epsP = D("0.58803") * (1 - D("0.0296398242"))
capN = epsN * D("52e-6") * D("31507")
capP = epsP * D("44e-6") * D("50707.7")
Q = D("0.58803") * D("44e-6") * D("50707.7") * (D(".927") - D(".215")) * F / 3600
current = Q * D(".1")
rateN, rateP = current / F / capN, -current / F / capP
rates = {"N": rateN, "P": rateP}
charge = {"model_parameters_checked": checks, "Q_areal_Ah_m2": Q, "i_app_A_m2": current,
          "active_capacity_mol_m2": {"N": capN, "P": capP}, "rates_per_s": rates,
          "exchange_ratio_N_over_P": rateN / rateP,
          "conditional_60s_average": {k: gm[D(0)]["xavg_" + k] + 60 * v for k, v in rates.items()},
          "max_average_departure_from_constant_current_formula": {
              k: max(abs(r["xavg_" + k] - g[0]["xavg_" + k] - r["time_s"] * v) for r in g)
              for k, v in rates.items()},
          "assumptions": "Fixed active inventories and csmax, constant Faradaic transfer, negligible leak, no side reaction/double-layer current. Not model independent."}

# Constant-flux, constant-D spherical diffusion series; no numerical PDE solve.
roots = []
for k in range(1, 257):
    lo, hi = k * math.pi, (k + .5) * math.pi - 1e-10
    for _ in range(60):
        mid = (lo + hi) / 2
        if math.tan(mid) - mid > 0:
            hi = mid
        else:
            lo = mid
    roots.append((lo + hi) / 2)

def fraction(t, radius, diffusivity, count=256):
    if t == 0:
        return 0.0
    return 1 - 10 * sum(math.exp(-z*z*diffusivity*t/(radius*radius))/(z*z) for z in roots[:count])

spheres = {}
for label, R, diffusion in (("N", 7.5e-6, 7.1e-15), ("P", 1e-5, 1e-13)):
    steady = abs(float(rates[label])) * R*R/(15*diffusion)
    lo, hi = 0., 5000.
    for _ in range(70):
        mid = (lo + hi) / 2
        if fraction(mid, R, diffusion) < .95:
            lo = mid
        else:
            hi = mid
    spheres[label] = {"radius_m": R, "D_m2_s": diffusion, "first_root": roots[0],
                      "slow_mode_tau_s": R*R/(diffusion*roots[0]**2), "steady_surface_average_gap": steady,
                      "t95_s": (lo+hi)/2, "fractions": {str(t): fraction(t,R,diffusion) for t in (5,10,20,30,60,300,900,1200)},
                      "series_128_vs_256_max_difference": max(abs(fraction(t,R,diffusion,128)-fraction(t,R,diffusion)) for t in (5,10,20,30,60)),
                      "local_sample_gap_ranges": {}}
    selected = {D(t): [] for t in (0,5,10,20,30)}
    with (DATA / ("axes_profile_" + label + ".csv")).open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            t = D(row["time_s"])
            if t in selected:
                difference = D(row["x_surface"]) - D(row["x_particle_average"])
                selected[t].append(difference if label == "N" else -difference)
    for t, values in selected.items():
        assert len(values) == 241
        spheres[label]["local_sample_gap_ranges"][str(t)] = {"count": len(values), "min": min(values), "max": max(values),
                         "min_fraction_steady": float(min(values))/steady, "max_fraction_steady": float(max(values))/steady}

def delta(col, a, b, data):
    return data[D(b)][col] - data[D(a)][col]

dxN = delta("x_surface",20,30,nm)
vdelta = delta("phis_V",20,30,pm)-delta("phis_V",20,30,nm)
decomp = {"dV_V": vdelta, "delta_xN_boundary1": dxN,
          "trajectory_dV_over_dxN_V": vdelta/dxN, "N_OCP_secant_V_per_x": delta("Eeq_V",20,30,nm)/dxN,
          "components_V": {"minus_N_Eeq": -delta("Eeq_V",20,30,nm), "P_Eeq": delta("Eeq_V",20,30,pm),
                           "eta_difference": delta("etamid_V",20,30,pm)-delta("etamid_V",20,30,nm),
                           "phi_l_difference": delta("phil_V",20,30,pm)-delta("phil_V",20,30,nm)}}
decomp["sum_residual_V"] = vdelta - sum(decomp["components_V"].values())

# Read table literals without executing Java. Default linear interpolation is independently checked against stored Eeq values.
def table(material, tag):
    prefix = f'material("{material}").propertyGroup("def").func("{tag}").set("table",new String[][]'
    line = next(s for s in source.splitlines() if prefix in s)
    return [(D(a), D(b)) for a,b in re.findall(r'\{"([\d.eE+-]+)","([\d.eE+-]+)"\}', line)]

un, dun, up, dup = table("mat35","int3"), table("mat35","int4"), table("mat54","int1"), table("mat54","int2")
def interp(t, x):
    assert t[0][0] <= x <= t[-1][0], (x,t[0][0],t[-1][0])
    i = min(len(t)-2, max(0,bisect.bisect_right([r[0] for r in t],x)-1))
    (a,va),(b,vb) = t[i:i+2]
    return va+(vb-va)*(x-a)/(b-a)
def en(x):
    return interp(un,x) + D(".15")*interp(dun,x)
def ep(x):
    return interp(up,x) + D(".15")*D(".001")*interp(dup,x)

ocp_match = {"N": max(abs(en(r["x_surface"])-r["Eeq_V"]) for r in n),
             "P": max(abs(ep(r["x_surface"])-r["Eeq_V"]) for r in p)}
assert max(ocp_match.values()) < D("1e-12")
stock = capN*g[0]["xavg_N"]+capP*g[0]["xavg_P"]
xp_min = max(up[0][0], dup[0][0])
xp_max = min(up[-1][0],dup[-1][0],(stock-capN*un[0][0])/capP)
xp_min = max(xp_min, (stock-capN*un[-1][0])/capP)
knots = {xp_min, xp_max}
for tab in (up,dup):
    knots.update(x for x,_ in tab if xp_min <= x <= xp_max)
for tab in (un,dun):
    knots.update((stock-capN*x)/capP for x,_ in tab if xp_min <= (stock-capN*x)/capP <= xp_max)
ocv = [(ep(xp)-en((stock-capP*xp)/capN), xp, (stock-capP*xp)/capN) for xp in knots]
top = max(ocv)
ocp = {"linear_table_check_against_1237_boundary_Eeq_max_residual_V": ocp_match,
       "temperature_K": "298.15", "P_dUdT_source_unit": "mV/K; converted to V/K before applying 0.15K",
       "fixed_stock_piecewise_linear_knots_checked": len(knots), "equilibrium_max_V": top[0],
       "at_xP": top[1], "at_xN": top[2], "gap_to_4p25V": D("4.25")-top[0],
       "initial_equilibrium_voltage_V": ep(g[0]["xavg_P"])-en(g[0]["xavg_N"]),
       "P_average_limit_constant_current_seconds": (g[0]["xavg_P"]-xp_min)/(-rateP),
       "P_quasisteady_surface_lead_seconds": D("1e-5")**2/(15*D("1e-13")),
       "scope": "Uniform equilibrium compositions, fixed stock, existing source linear OCP tables at 298.15K. Does not prove finite-current CV trajectory or post-cutoff rest exceeds table range."}

# One-mode interpolation scenarios, not a validated long-time asymptote.
selected = prior["selected_times"]
span = {int(t): float(r["ce_max_mol_m3"])-float(r["ce_min_mol_m3"]) for t,r in selected.items()}
fits=[]
for a,b,c in ((0,10,20),(10,20,30)):
    h=b-a
    decay=(span[c]-span[b])/(span[b]-span[a])
    tau=-h/math.log(decay)
    upper=span[a]+(span[b]-span[a])/(1-decay)
    amp=(upper-span[a])*math.exp(a/tau)
    pred=lambda t:upper-amp*math.exp(-t/tau)
    share=(float(selected["0"]["ce_min_mol_m3"])-float(selected["30"]["ce_min_mol_m3"]))/span[30]
    fits.append({"equal_spaced_fit_times_s":[a,b,c],"tau_s":tau,"span_infinity_mol_m3":upper,
                 "predicted_span_60":pred(60),"predicted_span_300":pred(300),
                 "fraction_infinity_at_30":span[30]/upper,"fraction_infinity_at_60":pred(60)/upper,
                 "held_30s_minimum_share":share,"predicted_ce60_min":1200-share*pred(60),
                 "predicted_ce60_max":1200+(1-share)*pred(60),"predicted_ce_infinity_min":1200-share*upper,
                 "not_a_tolerance_or_guarantee":True})

batch=json.loads((BASE/"received/run/batch_RETURN.json").read_text())
compile_=json.loads((BASE/"received/run/compile_RETURN.json").read_text())
mph=json.loads((BASE/"received/run/OUTPUT_MPH_IDENTITY.json").read_text())
cost={"anchor_stored_states":len(g),"time_intervals":len(g)-1,"solver_log_seconds_rounded":670,
      "batch_seconds":batch["elapsed_seconds"],"compile_seconds":compile_["elapsed_seconds"],
      "MPH_bytes_reported_not_received":mph["bytes"], "scenario":[]}
for t in (60,120,194,300,1200,2400):
    count=len(g)+10*(t-30)
    cost["scenario"].append({"physical_end_s":t,"stored_states_assuming_extra_10_per_s":count,
                           "batch_s":batch["elapsed_seconds"]*count/len(g),"MPH_decimal_GB":mph["bytes"]*count/len(g)/1e9})
cost["zero_margin_budget_3600s_end_time"] = 30+(((3600-compile_["elapsed_seconds"])/batch["elapsed_seconds"])*len(g)-len(g))/10
cost["rest_12h_only_scenario"]={"states":432000,"solver_days":670/len(g)*432000/86400,
                               "MPH_decimal_TB":mph["bytes"]/len(g)*432000/1e12}
assert 'binder.set("ElectricCorrModel","NoCorr")' in source
leak=[]
for sigma in (D("4.2e-7"),D("1.41e-6"),D("4.23e-6")):
    j=sigma*D("4.2")/D("25e-6")
    leak.append({"sigma_S_m":sigma,"assumed_separator_solid_drop_V":"4.2","j_A_m2":j,
                 "reference_capacity_percent_per_h":j/Q*100,"constant_4p2V_12h_percent":j*12/Q*100})
out={"scope":"Independent read-only arithmetic and analytical series; no new COMSOL/model solve or supplied code execution.",
     "prior_csv_hash_binding":pin_results,"charge":charge,"sphere":spheres,"voltage_20_to_30":decomp,
     "OCP_fixed_stock_check":ocp,"electrolyte_one_mode_scenarios":fits,"cost_scenarios":cost,
     "leak_order_of_magnitude":leak,"safety":"All scenario values are diagnostic estimates, not new execution tolerances or approval."}
after=[identity(p) for p in paths]
assert before == after
def write_json(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str)+"\n",encoding="utf-8")
write_json("CALCULATION_AUDIT.json",out)
write_json("SOURCE_IDENTITIES.json",{"scope":"Selected local received files only; no current remote system/MPH/prefs verification.",
                                    "before":before,"after":after,"unchanged":True})
print(json.dumps({"status":"OFFLINE_ARITHMETIC_COMPLETE","sources_unchanged":len(paths),
                  "sphere_tau_s":{k:v["slow_mode_tau_s"] for k,v in spheres.items()},
                  "sphere_t95_s":{k:v["t95_s"] for k,v in spheres.items()},
                  "OCP_max_V":str(top[0]),"elapsed_seconds":time.monotonic()-started},ensure_ascii=False))
