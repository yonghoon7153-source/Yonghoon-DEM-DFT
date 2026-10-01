"""Read-only porosity arithmetic review. No DEM/MPM simulation or production imports.
Run: python audit_porosity.py. Only writes evidence/ beside this script.
Geometry is NOT independently reharvested: original atom/mesh dumps are absent.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parent
B = ROOT / 'inputs/codex_ps45_porosity_request_20261001'
A = ROOT / 'inputs/ps45_lhs_20261001_1825/ps45_lhs_20261001_1825'
OUT = ROOT / 'evidence'
OUT.mkdir(exist_ok=True)
checks = []

def check(name, actual, expected, tol=1e-10):
    ok = abs(actual-expected) <= tol if isinstance(actual, (int, float)) else actual == expected
    checks.append(dict(name=name, actual=actual, expected=expected, tolerance=tol, passed=ok))
    if not ok:
        raise AssertionError(checks[-1])

def rows(path, delimiter=','):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def write_csv(name, data):
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(data)

for line in (B / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    sha, path = line.split(maxsplit=1)
    check('sha256:'+path, hashlib.sha256((B/path.removeprefix('./')).read_bytes()).hexdigest(), sha)

union = {r['case']: r for r in rows(A / 'union/ps45_union.tsv', '\t')}
handover = {r['case_id']: r for r in rows(B / 'post_fix/ps45_handover.csv')}
release = {r['case_id']: r for r in rows(B / 'post_fix/ps45_release_5rows.csv')}
order = ['10_0', '7_3', '5_5', '3_7', '0_10']
calc, sensitivity, provenance = [], [], []
for ps in order:
    case = 'ps_'+ps+'_r45'
    h = json.loads((A / 'harvest' / (case+'.json')).read_text(encoding='utf-8'))
    u = union[case]
    d = ROOT / 'reference/dem_scripts/ps_sweep_6mah_20260914' / ('in.'+case+'.liggghts')
    deck = d.read_text(encoding='utf-8')
    radii = {phase: float(re.search(r'^variable\s+r_'+phase+r'\s+equal\s+(\S+)', deck, re.M)[1])*1000
             for phase in ('AM_P', 'AM_S', 'SE')}
    counts = {p: h['phase_counts'].get(p, 0) for p in radii}
    V = {p: counts[p]*4*math.pi*radii[p]**3/3 for p in radii}
    # L from executable box declaration, not porosity output or a header comment.
    box = re.search(r'^region\s+reg_box\s+block\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', deck, re.M)
    lx = (float(box[2])-float(box[1]))*1000
    ly = (float(box[4])-float(box[3]))*1000
    H = (h['plate_z_sim']-h['z_floor_sim'])*1000
    Vbox = lx*ly*H
    phi_se, phi_am = V['SE']/Vbox, (V['AM_P']+V['AM_S'])/Vbox
    eps = 100*(1-phi_se-phi_am)
    for key, actual in [('thickness_um', H), ('lx_um', lx), ('eps_sphere_web', eps),
                        ('phi_se_sphere', phi_se), ('phi_am_sphere', phi_am)]:
        check(case+':'+key, actual, float(u[key]))
    check(case+':harvest_epsilon', eps, h['porosity_sphere_pct_RECORD_ONLY'])
    check(case+':counts_SE', counts['SE'], int(u['n_SE']), 0)
    check(case+':counts_AM', counts['AM_P']+counts['AM_S'], int(u['n_AM']), 0)
    check(case+':counts_all', sum(counts.values()), int(u['n_atoms']), 0)
    for key, actual in [('porosity_spheresum_nominal_gap_pct', eps), ('thickness_wall_gap_um', H)]:
        check(case+':handover_'+key, actual, float(handover[case][key]))
    N = int(u['mc_n'])
    mc_pct = float(u['mc_void_pct'])
    n_void_float = N*mc_pct/100
    n_void = round(n_void_float)
    check(case+':MC_integer_count', n_void_float, n_void, 1e-7)
    p = n_void/N
    se_pct = 100*math.sqrt(p*(1-p)/N)
    check(case+':MC_sigma', se_pct, float(u['mc_void_se_pct']))
    # Four mutually exclusive MC categories. This validates totals, not spatial membership.
    check(case+':MC_closure', mc_pct+sum(float(u[k]) for k in
          ['mc_SE_only_pct','mc_AM_only_pct','mc_both_pct']), 100)
    check(case+':handover_union', mc_pct, float(handover[case]['porosity_union_exact_pct']))
    check(case+':release_union', mc_pct, float(release[case]['porosity_union_exact_pct']))
    vout = sum(h['wall_record'][w]['v_out_sim'] for w in ['floor','plate'])*1e9
    clipping_pp = 100*vout/Vbox
    check(case+':clipped_epsilon', eps+clipping_pp, float(u['eps_sphere_clipped']))
    c = dict(case=case, PC_SC=ps.replace('_', ':'), **{'n_'+p: counts[p] for p in radii},
             Lx_um=lx, Ly_um=ly, H_um=H, V_AM_um3=V['AM_P']+V['AM_S'], V_SE_um3=V['SE'],
             Vbox_um3=Vbox, phi_se=phi_se, phi_am=phi_am, epsilon_sphere_pct=eps,
             epsilon_union_MC_pct=mc_pct, MC_N=N, MC_n_void=n_void, MC_SE_pp=se_pct,
             union_minus_sphere_pp=mc_pct-eps, direct_boundary_clipping_pp=clipping_pp,
             center_out=h['boundary_qc']['n_center_out'], fully_out=h['boundary_qc']['n_fully_out'])
    calc.append(c)
    drho_pp = -100*phi_se*(2.0/1.86-1)
    srow = dict(case=case, epsilon_sphere_pct=eps, density_SE_2_to_1p86_delta_pp=drho_pp,
                density_only_epsilon_pct=eps+drho_pp)
    for spring in (.01,.02,.03):
        label = str(round(spring*100))+'pct'
        spring_eps = 100*(1-(1-eps/100)/(1+spring))
        srow['springback_'+label+'_delta_pp'] = spring_eps-eps
        srow['combined_'+label+'_epsilon_pct'] = 100*(1-(1-eps/100-drho_pp/100)/(1+spring))
    sensitivity.append(srow)
    provenance.append(dict(case=case, remote_deck_sha256=hashlib.sha256(d.read_bytes()).hexdigest(),
                           handover_design_deck_sha256=handover[case]['ps45_deck_sha256'],
                           harvest_input_deck_sha256=h['handover_qc']['deck_sha256']))

exp = [('batch1','PC','10_0',20.7), ('batch1','PC+No1','5_5',14.6),
       ('batch1','PC+No2','5_5',14.5), ('mien3','No1','0_10',15.5),
       ('mien3','No2','0_10',16.7), ('mien3','PC','10_0',16.5),
       ('mien3','PC+No1','5_5',14.8)]
by_case = {r['case']:r for r in calc}
contrasts = []
for batch, material, ps, value in exp:
    c = by_case['ps_'+ps+'_r45']
    contrasts.append(dict(batch_label=batch, material_label=material, PC_SC=ps.replace('_',':'),
                          experiment_reported_pct=value,
                          sphere_minus_experiment_pp=c['epsilon_sphere_pct']-value,
                          union_minus_experiment_pp=c['epsilon_union_MC_pct']-value,
                          status='DESCRIPTIVE_ONLY_NOT_REPLICATES'))

write_csv('recomputed_5beds.csv', calc)
write_csv('density_springback_sensitivity.csv', sensitivity)
write_csv('descriptive_comparisons.csv', contrasts)
write_csv('deck_provenance.csv', provenance)
# Exact t-distribution planning examples, not an estimated sample size for these data.
try:
    from scipy.stats import t
    examples = []
    for sd in (.5,1.,2.):
        n = next(n for n in range(2,10001) if t.ppf(.975,n-1)*sd/math.sqrt(n)<=.5)
        examples.append(dict(assumed_SD_pp=sd, target_halfwidth_pp=.5, n=n,
                             halfwidth_pp=float(t.ppf(.975,n-1)*sd/math.sqrt(n))))
    write_csv('CI_planning_examples.csv', examples)
except ImportError:
    examples = 'scipy not installed: CI planning examples skipped; all arithmetic checks still run'

result = dict(scope='Aggregate arithmetic only; raw dumps/experiment records/MPM outputs unavailable',
              checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks),
              checks=checks, CI_planning=examples,
              minimum_contrasts=dict(
                  PC_minus_7_3_sphere_pp=calc[0]['epsilon_sphere_pct']-calc[1]['epsilon_sphere_pct'],
                  PC_minus_7_3_union_pp=calc[0]['epsilon_union_MC_pct']-calc[1]['epsilon_union_MC_pct']),
              remote_decks_byte_equal_harvest_inputs=all(r['remote_deck_sha256']==r['harvest_input_deck_sha256'] for r in provenance))
(OUT / 'audit_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2))
for c in calc:
    print(c['PC_SC'], 'H',format(c['H_um'],'.6f'), 'sphere',format(c['epsilon_sphere_pct'],'.9f'),
          'union_MC',format(c['epsilon_union_MC_pct'],'.6f'),'MC_SE',format(c['MC_SE_pp'],'.6f'))
