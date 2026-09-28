"""R7 independent arithmetic/counterexamples, not a DEM or scheduler run.

Only imports plan/ced_matrix from the explicitly pinned R6 baseline. The pairwise
correction below is an audit calculation, NOT the proposed unprovided CLI.
All M/variance/scheduler examples are synthetic, not campaign measurements.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import sys

sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.stats import chi2, norm, t

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--source', type=Path, default=HERE / 'baseline' / 'make_mixer_deck.py')
ap.add_argument('--out', type=Path, default=HERE / 'audit_results.json')
args = ap.parse_args()
spec = importlib.util.spec_from_file_location('pinned_generator', args.source)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
baseline_E = dict(g.E_PHASE)
p = g.plan(100000, cgf=151.4)
names = tuple(g.TYPES) + ('WALL',)
r = {x: p['d'][x]/2 for x in g.TYPES}
nu = {x: g.PHASE_MECH[x][0] for x in g.TYPES}
nu['WALL'] = g.WALL_NU
checks = []

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

source_bytes=args.source.read_bytes()
source_blob=hashlib.sha1(b'blob '+str(len(source_bytes)).encode()+b'\0'+source_bytes).hexdigest()
check('baseline exact git blob', source_blob=='033fac54d73566ac1dad54f24cc28b9d0510ccbc')

def estar(a, b, Es):
    return 1/((1-nu[a]**2)/Es[a] + (1-nu[b]**2)/Es[b])

def contact(a, b, Es, ced):
    rs = r[a] if b == 'WALL' else r[a]*r[b]/(r[a]+r[b])
    A = 4/3*estar(a, b, Es)*math.sqrt(rs)
    B = 2*math.pi*rs*ced
    d0 = (B/A)**2
    return dict(F0_N=B*d0, U_sep_J=B*d0*d0/10, delta0_m=d0)

pair_rows = []
matrices = {}
for arm in ('LC', 'LH', 'E0'):
    base = g.ced_matrix(arm, p['d'])
    for factor in (14, 28):
        Es = dict(baseline_E, SE=baseline_E['SE']*factor)
        corrected = [[0.0]*len(names) for _ in names]
        for i, a in enumerate(g.TYPES):
            for j in range(i, len(names)):
                b = names[j]
                er = estar(a, b, Es)/estar(a, b, baseline_E)
                cr = er**(2/3)
                ced = base[i][j]*cr
                corrected[i][j] = corrected[j][i] = ced
                old = contact(a, b, baseline_E, base[i][j])
                new = contact(a, b, Es, ced)
                if old['F0_N'] == 0:
                    check(f'{arm}/{factor}/{a}-{b}: exact zero', new['F0_N'] == 0)
                    fr = ur = None
                else:
                    fr = new['F0_N']/old['F0_N']
                    ur = new['U_sep_J']/old['U_sep_J']
                    check(f'{arm}/{factor}/{a}-{b}: F0', abs(fr-1)<2e-14)
                    check(f'{arm}/{factor}/{a}-{b}: U', abs(ur-er**(-2/3))<2e-14)
                pair_rows.append(dict(arm=arm, factor=factor, pair=a+'--'+b,
                    E_star_ratio=er, CED_ratio=cr, F0_ratio=fr, U_ratio=ur,
                    original_CED_J_m3=base[i][j], proposed_CED_J_m3=ced,
                    original_F0_N=old['F0_N']))
        check(f'{arm}/{factor}: symmetry', corrected == list(map(list, zip(*corrected))))
        check(f'{arm}/{factor}: wallwall zero', corrected[-1][-1] == 0)
        matrices[f'{arm}_SE{factor}'] = corrected
check('9 non-wallwall unordered pairs per arm/level', len(pair_rows)==3*2*9)

def stats(values):
    x = np.asarray(values, dtype=float)
    n = len(x)
    avg = float(x.mean())
    sd = float(x.std(ddof=1))
    se = sd/math.sqrt(n)
    half = float(t.ppf(.975,n-1))*se
    return dict(values=x.tolist(), n=n, mean=avg, sd=sd, se=se,
                ci95=[avg-half, avg+half], MID_point_rule=(avg>=.10 and avg>=2*se))

dref = [.100, .101, .102]
q = [-.014, -.015, -.016]
dsoft = [a+b for a,b in zip(dref,q)]
equiv = dict(reference=stats(dref), soft=stats(dsoft), q=stats(q))
check('q equivalence passes', equiv['q']['ci95'][0]>-.02 and equiv['q']['ci95'][1]<.02)
check('reference MID passes', equiv['reference']['MID_point_rule'])
check('soft MID fails despite q equivalence', not equiv['soft']['MID_point_rule'])

observed, possible = stats([.04,.14,.24]), stats([.02,.12,.26])
epsilon = .02
u_mean = epsilon
u_se = math.sqrt(3*epsilon**2)/math.sqrt(3*2)
draft_pass = observed['mean']-u_mean>=.10 and observed['mean']-u_mean>=2*observed['se']
robust_pass = observed['mean']-u_mean>=.10 and observed['mean']-u_mean>=2*(observed['se']+u_se)
check('per-seed perturbation within .02', max(abs(a-b) for a,b in zip(observed['values'],possible['values']))<=.02+1e-15)
check('draft robust guard false green', draft_pass and not possible['MID_point_rule'])
check('conservative SE propagation refuses', not robust_pass)
guard = dict(observed=observed, possible_true=possible, per_seed_bound=epsilon,
             u_mean=u_mean, u_se=u_se, draft_pass=draft_pass, conservative_pass=robust_pass)

s0, sr, s = .020, .019, .0195
M = lambda sr_: (s0-s)/(s0-sr_)
normalization = dict(S0_squared=s0, S_squared=s, SR_squared=sr,
    SR_squared_new=sr*1.01, M_old=M(sr), M_new=M(sr*1.01), M_change=M(sr*1.01)-M(sr))
check('positive denominators', s0>sr*1.01)
check('one-percent SR change amplifies beyond .02', normalization['M_change']>.02)

def eq_power(n, sigma, mu=0.0, b=.02):
    # Under iid Normal q, mean independent of (n-1)*s^2/sigma^2 ~ chi2(n-1).
    # Integrate conditional P(-b+h < mean < b-h), no random simulation.
    df=n-1
    crit=float(t.ppf(.975,df))
    vmax=df*(b*math.sqrt(n)/(crit*sigma))**2
    def integrand(v):
        half=crit*sigma*math.sqrt(v/df)/math.sqrt(n)
        hi=(b-half-mu)/(sigma/math.sqrt(n))
        lo=(-b+half-mu)/(sigma/math.sqrt(n))
        return max(0.0,float(norm.cdf(hi)-norm.cdf(lo)))*float(chi2.pdf(v,df))
    return float(quad(integrand,0,vmax,epsabs=1e-11,epsrel=1e-10)[0])

critical=float(t.ppf(.975,2))
power = dict(assumption='iid Normal q, true mean zero; unknown campaign SD, illustrative only',
    t975_df2=critical, sd_limit_at_mean0=.02*math.sqrt(3)/critical,
    sd_limit_at_mean001=.01*math.sqrt(3)/critical,
    central_coverage_of_2SE_at_df2=float(t.cdf(2,2)-t.cdf(-2,2)),
    cases=[dict(n=3, sigma=sig, power=eq_power(3,sig)) for sig in (.005,.01,.02)])
check('power decreases with hypothetical noise', power['cases'][0]['power']>power['cases'][1]['power']>power['cases'][2]['power'])

# Logical countermodel to qualification, NOT outputs of any DEM trajectory.
qualification = dict(label='synthetic unconstrained-observable countermodel, not simulated physics',
    E0_max_overlap_pct=dict(ref=.8, ref2=.4, ref_dt_half=.79),
    E0_SR_squared=dict(ref=.010, ref2=.00998, ref_dt_half=.01005),
    M_bin7=dict(ref=dict(LC=.65,LH=.53),ref2=dict(LC=.65,LH=.59),
                ref_dt_half=dict(LC=.65,LH=.60)))
check('synthetic E0 reference rule b passes', qualification['E0_max_overlap_pct']['ref2']<qualification['E0_max_overlap_pct']['ref']<=1)
check('synthetic E0 dt rule c passes', abs(.8-.79)<=.1 and abs(.01005/.010-1)<=.01)
contrasts={k:v['LC']-v['LH'] for k,v in qualification['M_bin7'].items()}
qualification['d_bin7']=contrasts
check('E0 pass does not bind d-bin7', abs(contrasts['ref']-contrasts['ref2'])>.02 and abs(contrasts['ref']-contrasts['ref_dt_half'])>.02)

def prime(v):
    return v>=2 and all(v%d for d in range(2,math.isqrt(v)+1))
seeds={str(v):prime(v) for v in (15485863,86028121,104395301)}
check('three specified seeds are prime', all(seeds.values()))

scheduling=dict(label='deterministic 2-slot counterexample, NOT ibb ETA',
    initial_job_hours=[10,1], remaining_job_hours=10, gate_time_hours=5,
    no_hold_finish_hours=max(10,1+10), held_finish_hours=max(10,5+10),
    note='one freed slot idle from h1 to h5 despite unchanged capacity')
check('holding can increase makespan', scheduling['held_finish_hours']>scheduling['no_hold_finish_hours'])

out=dict(scope='independent arithmetic and logical counterexamples only; no DEM/MPI/scheduler or real campaign data',
    baseline_git_commit='18787ab98a13361c37b2343bd07ae276142d0953',
    baseline_git_blob=source_blob,
    baseline_source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
    prereg_copy_sha256=hashlib.sha256((HERE/'prereg_submitted.txt').read_bytes()).hexdigest(),
    pairwise_rows=pair_rows, proposed_matrices=matrices, equivalence_not_decision=equiv,
    incomplete_SE_guard=guard, normalization=normalization, equivalence_power=power,
    qualification_countermodel=qualification, seed_primality=seeds, scheduler_counterexample=scheduling,
    assertions=dict(passed=len(checks), failed=0, names=checks))
args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
compact={k:v for k,v in out.items() if k not in ('pairwise_rows','proposed_matrices','assertions')}
compact['pair_summary']=[x for x in pair_rows if x['arm']=='LC' and x['pair'] in ('AM_P--SE','SE--SE','SE--WALL')]
compact['assertions']=dict(passed=len(checks),failed=0)
print(json.dumps(compact,ensure_ascii=False,indent=2))
