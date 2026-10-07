"""S0: reviewer-written piecewise-analytic arithmetic, not COMSOL or a DFN solver.
Only parses four literal OCP/entropy tables from a TEXT copy; never imports source.
Outputs JSON to stdout. All voltage predictions omit kinetic/diffusive polarization.
"""
import bisect
import hashlib
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / "sources/Normal480Candidate.java.txt"
raw = JAVA.read_bytes()
source = raw.decode("utf-8")
def table(material, function):
    prefix = f'm.component("comp1").material("{material}").propertyGroup("def").func("{function}").set("table",new String[][]'
    lines = [line for line in source.splitlines() if prefix in line]
    assert len(lines) == 1
    pairs = [(float(a), float(b)) for a,b in re.findall(r'\{"([^"]+)","([^"]+)"\}', lines[0])]
    assert len(pairs)>5 and all(pairs[i][0]<pairs[i+1][0] for i in range(len(pairs)-1))
    return pairs

TN, EN = table("mat35","int3"), table("mat35","int4")
TP, EP = table("mat54","int1"), table("mat54","int2")
def interp(tab,x):
    if not tab[0][0] <= x <= tab[-1][0]: raise ValueError("NO_EXTRAPOLATION")
    j=max(0,min(bisect.bisect_right([p[0] for p in tab],x)-1,len(tab)-2))
    a,b=tab[j],tab[j+1]; slope=(b[1]-a[1])/(b[0]-a[0])
    return a[1]+slope*(x-a[0]),slope

def un(x):
    u,du=interp(TN,x); e,de=interp(EN,x)
    return u+0.15*e,du+0.15*de
def up(x):
    u,du=interp(TP,x); e,de=interp(EP,x)
    return u+0.15*e/1000,du+0.15*de/1000

F=96485.33212
epsN=.63122*(1-.0257219788); epsP=.58803*(1-.0296398242)
AN=epsN*52e-6*31507; AP=epsP*44e-6*50707.7
stock=.58803*44e-6*50707.7*.927+.63122*52e-6*31507*.01172068149
stock-=.003765381*3600*.0439355/F/(1.53938e-4)
CN,CP=F*AN,F*AP
Q=.58803*44e-6*50707.7*(.927-.215)*F/3600
i01=Q/10
L=25e-6
def xp_for(xn): return (stock-AN*xn)/AP
def voltage(xn):
    xp=xp_for(xn); uN,sN=un(xn); uP,sP=up(xp)
    k=-(sP/CP+sN/CN)
    return {"xN":xn,"xP":xp,"U_V":uP-uN,"UN_V":uN,"UP_V":uP,
            "UN_slope_V_per_x":sN,"UP_slope_V_per_x":sP,
            "k_V_per_C_m2":k,"slope_V_per_nominal_SOC":k*3600*Q}
def integrate(xn,sigma,T):
    xp=xp_for(xn); g=sigma/L
    qmax=min((xn-max(TN[0][0],EN[0][0]))*CN,
             (min(TP[-1][0],EP[-1][0])-xp)*CP)
    knots={0.,qmax}
    for a,_ in TN+EN:
        q=(xn-a)*CN
        if 0<q<qmax:knots.add(q)
    for a,_ in TP+EP:
        q=(a-xp)*CP
        if 0<q<qmax:knots.add(q)
    knots=sorted(knots)
    q=0.;t=0.;steps=0
    for a,b in zip(knots,knots[1:]):
        # Slopes at the midpoint avoid double-valued knot derivatives.
        mid=(a+b)/2
        uN,sN=un(xn-mid/CN);uP,sP=up(xp+mid/CP)
        k=-(sP/CP+sN/CN)
        ua=up(xp+a/CP)[0]-un(xn-a/CN)[0]
        ub=ua-k*(b-a)
        if ua<=0:break
        if abs(k)<1e-16:dt=(b-a)/(g*ua)
        elif ub<=0:dt=math.inf
        else:dt=-math.log1p(-k*(b-a)/ua)/(g*k)
        if t+dt>=T:
            d=T-t
            dq=g*ua*d if abs(k)<1e-16 else -ua/k*math.expm1(-g*k*d)
            q=a+dq;t=T;steps+=1;break
        q=b;t+=dt;steps+=1
    final=voltage(xn-q/CN)
    return {"time_s":t,"requested_time_s":T,"within_table":t>=T,"q_C_m2":q,
            "nominal_SOC_loss_percent":100*q/(3600*Q),
            "delta_U_mV":1000*(final["U_V"]-voltage(xn)["U_V"]),
            "U_final_V":final["U_V"],"xN_final":final["xN"],"xP_final":final["xP"],
            "dUdt_final_mV_per_h":-final["k_V_per_C_m2"]*g*final["U_V"]*3.6e6,
            "analytic_segments":steps}

states=[voltage(x) for x in [.01172068149,.105,.205,.315,.445,.495,.705]]
xn=.445
v=voltage(xn)
ladder=[]
for sigma in [1e-20,1.7e-8,1.7e-7,1.7e-6,1.7e-5]:
    j=sigma*v["U_V"]/L
    k=v["k_V_per_C_m2"]
    ladder.append({"sigma_S_m":sigma,"j0_A_m2":j,"r0_vs_0p1C":j/i01,
        "C_rate_leak_per_h":j/Q,"dUdt_initial_mV_per_h":-k*j*3.6e6,
        "tau_capacity_h":Q/j,"tau_voltage_s":L/(sigma*k),
        "nominal_1h_loss_constant_U_percent":100*j/Q,
        "at_1800s":integrate(xn,sigma,1800),
        "at_3600s":integrate(xn,sigma,3600)})
lam=4.493409457909064
tauN=(7.5e-6)**2/(7.1e-15*lam**2)
tauP=(10e-6)**2/(1e-13*lam**2)
tau_e=[]
for length,por,beta in [(52e-6,1-.1-epsN,2.5),(25e-6,.45,1.5),(44e-6,1-.1-epsP,2.2)]:
    # eps dc/dt = div(D eps^beta grad c)
    tau_e.append({"L_m":length,"eps":por,"D_dyn_m2_s":7.5e-11*por**(beta-1),
                  "L2_over_Ddyn_s":length**2/(7.5e-11*por**(beta-1)),
                  "slab_first_mode_s":length**2/(math.pi**2*7.5e-11*por**(beta-1))})
# Explicit checks of our own arithmetic, not functional tests of candidate programs.
checks={"inventory_reproduces_historical_xP":abs(xp_for(.01172068149)-.9240638866948166)<1e-12,
 "historical_OCV":abs(voltage(.01172068149)["U_V"]-2.1653333265)<1e-9,
 "r0p01_is_0p001C":abs((.01*i01)/Q-.001)<1e-15,
 "positive_temperature_unit":EP[0][1]/1000<.001,
 "monotone_ladder":all(ladder[i]["at_3600s"]["q_C_m2"]<ladder[i+1]["at_3600s"]["q_C_m2"] for i in range(4)),
 "all_proposed_within_table":all(x["at_3600s"]["within_table"] for x in ladder)}
assert all(checks.values()),checks
out={"kind":"S0_PIECEWISE_ANALYTIC_SCENARIO_NOT_COMSOL_RESULT",
 "source_java_text_sha256":hashlib.sha256(raw).hexdigest(),
 "source_lines":{"ocpN":142,"entropyN":151,"ocpP":272,"entropyP":281,"parameters":"587-607"},
 "interpolation":"piecewise linear, bounded, entropy N V/K and P mV/K; T=298.15K, reference298K",
 "method":"exact exponential per OCP/entropy segment of dq/dt=(sigma/L)*U(q); no reaction/ohmic/diffusion polarization",
 "parameters":{"AN_mol_m2":AN,"AP_mol_m2":AP,"stock_solid_mol_m2":stock,"CN_C_m2":CN,"CP_C_m2":CP,"Q_Ah_m2":Q,"i01_A_m2":i01},
 "initial_state_comparison":states,"chosen_state":v,"ladder":ladder,
 "relaxation":{"sphere_tau_N_s":tauN,"sphere_tau_P_s":tauP,"electrolyte_layer_estimates":tau_e,
   "electrolyte_fullcell_L2_pi2_Ddyn_range_s":[(121e-6)**2/(math.pi**2*max(t["D_dyn_m2_s"] for t in tau_e)),(121e-6)**2/(math.pi**2*min(t["D_dyn_m2_s"] for t in tau_e))],
   "sigma_for_tau_voltage_equal_tauN_S_m":L/(v["k_V_per_C_m2"]*tauN),
   "sigma_for_capacity_time_equal_tauN_S_m":3600*Q*L/(v["U_V"]*tauN)},
 "own_arithmetic_checks":checks,"COMSOL_calls":0,"provided_program_executions":0}
print(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False))

