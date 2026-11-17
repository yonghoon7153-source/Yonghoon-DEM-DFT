"""Read-only record checks and small scalar arithmetic; never imports solver code."""
import contextlib
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / 'input/repo'
OUT = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read_json(p):
    return json.loads(p.read_text(encoding='utf-8'))

def dump(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

sets = ['rint2_probe6_a3_20261116', 'rint2_probe6_a4_20261116',
        'rint2_s0_sbe_20261116', 'rint2_q11_gpu_check_kgy_20261116']
hashes = []
for dataset in sets:
    folder = REPO / 'docs/data' / dataset
    for line in (folder / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        p = folder / name.lstrip('*')
        assert p.resolve().is_relative_to(folder.resolve()), name
        actual = sha(p)
        hashes.append(dict(dataset=dataset, path=name, expected=expected, actual=actual, ok=expected == actual))
dump('hash_checks.json', hashes)

probe = [read_json(REPO / 'docs/data' / d / 'probe6_report.json') for d in sets[:2]]
selected = ['n_dof', 'cg_iters', 'cert_iters', 'cert_resolve_iters', 'cg_resid',
            'cert_imbalance', 'cert_ok', 'cert_pass_a', 'cert_pass_b', 'cert_pass_c',
            'cert_pass_d', 'cert_status', 'code_matches_pin', 'bed_inputs_match_s0',
            'tol_ff_matches_s0']
probe_check = {'fields': [{k: p['fields'][k] for k in selected} for p in probe],
               'equal_selected_fields': all(probe[0]['fields'][k] == probe[1]['fields'][k] for k in selected),
               'arm_hash_record_identical': probe[0]['arm']['sha256'] == probe[1]['arm']['sha256'],
               'arm_hash_record': probe[0]['arm']['sha256'],
               'arm_bytes_available_in_bundle': False,
               'limits': 'Original arm JSON deliberately absent. Equality independently verifies receipt hash records, not original arm bytes.'}
dump('probe_checks.json', probe_check)

s0 = REPO / 'docs/data' / sets[2]
plan_p = s0 / 'files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json'
plan = read_json(plan_p)
kit = read_json(plan_p.with_name('s0_stage1_kit_SBE_vgcf100.json'))
store = read_json(s0 / 'files/s0log_20261116T004809Z/store_probe.json')
c = store['calls'][0]
s0_checks = {
    'plan_hash': sha(plan_p), 'plan_hash_declaration_matches': sha(plan_p) == plan_p.with_suffix('.sha256').read_text().split()[0],
    'u': plan['values_um']['u'], 'spacing_median_over_2': plan['source']['spacing']['median_um'] / 2,
    'tol_ff_rule_ok': plan['values_um']['tol_ff'] == min(plan['values_um']['u'], plan['values_um']['r_f']),
    'tol_P_sj_equal_ff': plan['values_um']['tol_P'] == plan['values_um']['tol_sj'] == plan['values_um']['tol_ff'],
    'input_roles': sorted(plan['source']['inputs_sha256']), 'calls': len(store['calls']),
    'n_instances': c['n_instances'], 'kit_n_instances': kit['junction_census']['census']['n_instances'],
    'store_start': store['store_start'], 'write_status': c['write']['status'], 'read_status': c['read']['status'],
    'same': c['same'], 'code_drift': c['code_drift'], 'error': c['error'],
    'T1': {'write_s': c['write']['seconds_write'], 'read_s': c['read']['seconds_read'],
           'read_build_ratio': c['read']['seconds_read'] / c['seconds_build'],
           'pass': c['write']['seconds_write'] <= 600 and c['read']['seconds_read'] <= 300 and c['read']['seconds_read'] <= .1 * c['seconds_build']},
    'T2': {'hwm_reset': c['hwm_reset'], 'increment_GiB': (max(c['rss_kb'][k]['VmHWM'] for k in ['after_write','after_read','after_gc']) - c['rss_kb']['before']['VmRSS']) / 1024**2},
    'T3': {'bytes': c['write']['bytes'], 'GiB': c['write']['bytes'] / 1024**3,
           'pass': c['write']['bytes'] == c['read']['bytes'] <= 2*1024**3},
    'rss_rc_lines': [l for l in (s0 / 'files/s0log_20261116T004809Z/rss.log').read_text().splitlines() if l.startswith('rc=')],
    'kit_code': kit['code'], 'kit_top_keys': sorted(kit),
}
s0_checks['T2']['pass'] = s0_checks['T2']['hwm_reset'] and s0_checks['T2']['increment_GiB'] <= 4
manifest = list(csv.DictReader(io.StringIO((s0 / 'MANIFEST.tsv').read_text()), delimiter='\t'))
declared_outputs = (s0 / 'files/s0log_20261116T004809Z/out_sha256.txt').read_text().splitlines()
manifest_by_name = {Path(row['path']).name: row for row in manifest}
s0_checks['output_receipt_vs_original_manifest'] = []
for line in declared_outputs:
    digest, name = line.split(maxsplit=1)
    name = Path(name.lstrip('*')).name
    s0_checks['output_receipt_vs_original_manifest'].append({'name': name, 'ok': manifest_by_name[name]['sha256'] == digest})
dump('s0_checks.json', s0_checks)

q = read_json(REPO / 'docs/data' / sets[3] / 'result.json')
pairs = ['control_old_old', 'control_new_new', 'short_old_new', 'main_old_new', 'resolve_old_new']
qcheck = {'pair_checks': {k: q[k] for k in pairs}, 'consume': q['consume'], 'system': q['system'],
          'main_iters': [q[f'main_{side}']['iters'] for side in ['old','new']],
          'resolve_iters': [q[f'resolve_{side}']['iters'] for side in ['old','new']],
          'short_runs_exact_200': all(v['info'] == v['iters'] == 200 for v in q['short_runs'].values()),
          'all_runs_gpu_jacobi': all(v['backend'] == {'fallback_reason':None,'precond':'jacobi','requested':'gpu','used':'gpu'} for v in list(q['short_runs'].values()) + [q[k] for k in ['main_old','main_new','resolve_old','resolve_new']]),
          'main_hash_same': q['main_old']['x_sha256'] == q['main_new']['x_sha256'],
          'resolve_hash_same': q['resolve_old']['x_sha256'] == q['resolve_new']['x_sha256'],
          'ratio_from_displayed_per_iter': q['main_old']['per_iter_s'] / q['main_new']['per_iter_s'],
          'ratio_from_displayed_seconds': q['main_old']['seconds'] / q['main_new']['seconds'],
          'files': q['files']}
dump('q11_checks.json', qcheck)

# Raw Git blob reads only. No checkout, solver execution, or network fetch.
gitdir = ROOT / 'objects.git'
pin = '64e4d213e8267bafaf3ae5af00a42996cefd3f33'
env = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0')
def blob(rev, path):
    return subprocess.check_output(['git', '--git-dir='+str(gitdir), 'show', rev+':'+path],env=env)
code_checks=[]
for entry in kit['code']['file_digests']:
    path, expected = entry['file'], entry['sha256']
    pp=path if path.startswith('scripts/') else 'scripts/'+path
    actual=hashlib.sha256(blob(pin,pp)).hexdigest()
    code_checks.append({'path':pp,'expected':expected,'actual':actual,'ok':actual==expected})
q11_source_checks=[]
for rev,which in [('11a794674','old'),(pin,'new')]:
    actual=hashlib.sha256(blob(rev,'scripts/step3_sigma.py')).hexdigest()
    expected=q['files'][which+'_sha256']
    q11_source_checks.append({'rev':rev,'expected':expected,'actual':actual,'ok':actual==expected})
solver_paths=['scripts/','docs/reviews/rint2_probe6_prep_20261110/tools/',
              'docs/data/rint2_s0_sbe_20261108/','docs/data/rint_eis_anchors.csv',
              'docs/reviews/sdcp_gain_prereg_v2_20260816.md']
candidate='c80d700bdd5915da82f77f839cb96ed4a5a6582e'
code_diff=subprocess.check_output(['git','--git-dir='+str(gitdir),'diff','--name-only',pin,candidate,'--']+solver_paths,env=env).decode().splitlines()
def flattened(x,path=''):
    if isinstance(x,dict):
        out={}
        for k,v in x.items(): out.update(flattened(v,path+'.'+k if path else k))
        return out
    return {path:x}
old_plan=json.loads(blob(pin,'docs/data/rint2_s0_sbe_20261108/files/sdcp/ca1_s0_sbe_20261106_memfix/cjunc_plan.json'))
pa,pb=flattened(old_plan),flattened(plan)
plan_diff_keys=[k for k in sorted(set(pa)|set(pb)) if pa.get(k)!=pb.get(k)]
e4_result = OUT / 'e4_baseline_checks.json'
e4 = read_json(e4_result) if e4_result.exists() else None
dump('code_pin_checks.json',{'code_pin':pin,'S0_file_digests':code_checks,'Q11_sources':q11_source_checks,
                            'candidate_commit':candidate,'full_solver_path_list_changes':code_diff,
                            'S0_plan_1108_vs_1116_different_keys':plan_diff_keys,
                            'S0_1116_dict_leaves_lists_atomic':len(flattened(kit)),
                            'S0_1113_kit_available':e4 is not None,
                            'S0_1113_kit_comparison':None if e4 is None else e4['comparisons']['metadata'],
                            'limitation':'Run verify_e4_baseline.py for exact historical commit extraction and independent 508-field comparison.' if e4 is None else '11-13 historical baseline independently checked; NPZ source bytes remain unopened, only hash records compared.'})

# Execute only the fully inspected standard-library scalar time-estimation file.
model_p = REPO / 'docs/reviews/rint2_time_reestimate_20261111/v3/work/time_budget_v3.py'
m = runpy.run_path(str(model_p), run_name='review_arithmetic_only')
oldargv = sys.argv
try:
    sys.argv = [str(model_p), '--json']
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        m['main']()
finally:
    sys.argv = oldargv
rerun = json.loads(capture.getvalue())
dump('time_model_rerun.json', rerun)
original = read_json(model_p.with_suffix('.json'))

# Independent implementation from stated component counts (no functions from author's model).
g = .017917 / ((.012310 + .012301) / 2)
r = 2578 / 879
def components(gpu_factor, ratio=r, multiplier=1, mode='arm'):
    prep_ratio = ratio if mode == 'arm' else 1
    cold = 3838 * gpu_factor * multiplier + 459
    return {'sbe_arm': 635 + cold, 'dbe_arm': prep_ratio*635 + ratio*cold,
            'dbe_cold': ratio*cold, 'dbe_prep': prep_ratio*635,
            'build': prep_ratio*4135, 'source': prep_ratio*4557 + 240}
def independently(mode='arm', ratio=r, multiplier=1):
    k, b = components(1,ratio,multiplier,mode), components(g,ratio,multiplier,mode)
    ladder = max(19*k['sbe_arm'] + 3*4135, 19*b['sbe_arm'] + 3*4135)
    result=[]
    for high in (0,1):
        vals=[]
        for nk in range(13):
            times=[]
            for n,c in ((nk,k),(12-nk,b)):
                unit = c['dbe_prep'] + (2+high)*c['dbe_cold'] + c['source'] + 2*c['dbe_arm']
                times.append(n*unit+3*c['build'] if n else 0)
            vals.append((ladder+max(times),nk))
        sec,nk=min(vals)
        result.append({'hours':sec/3600,'kgy_units':nk})
    return {'range': result, 'overflow_first_kgy_h':(8*k['dbe_arm']+5*k['build'])/3600,
            'overflow_first_gabia_h':(8*b['dbe_arm']+5*b['build'])/3600,
            'post_all_h':36*k['source']/3600}

maxiter=[]
for cap in (3000000,4000000,5000000,6000000):
    main=cap*2913/277885/3600
    resolve=cap*925/84485/3600
    row=next(v for v in rerun['maxiter'] if v['maxiter']==cap)
    maxiter.append({'cap':cap, 'one_kgy_h':main, 'one_gabia_h':main*g,
                    'main_plus_resolve_kgy_h':main+resolve, 'main_plus_resolve_gabia_h':(main+resolve)*g,
                    'author_model':row})
out={'hash_checks_pass':sum(v['ok'] for v in hashes),'hash_checks_total':len(hashes),
     'author_model_reproduces_stored_json':rerun == original,
     'independent_model':{name:independently(**args) for name,args in [
         ('base_arm',{}),('base_solve',{'mode':'solve'}),('double_r',{'ratio':2*r}),
         ('double_m',{'multiplier':2}),('double_r_and_m',{'ratio':2*r,'multiplier':2})]},
     'maxiter_table_independent':maxiter, 'cap_to_SBE':5000000/277885,
     'legacy_ratio_interval':[3054/704, 2*3054/704],
     'legacy_upper_times2_to_cap_margin':(5000000/277885)/(4*3054/704),
     'hours_112':168*2/3, 'attempts_remaining_after_four_pre_result_and_one_adopted':8-4-1,
     'limit':'Independent review only; author internal review counts are not independent verification.'}
overflow_mapping=[]
for ratio in (r, 4.0):
    for name,gpu in [('kgy',1),('gabia',g)]:
        cc=components(gpu,ratio)
        first=cc['sbe_arm']+4135
        hit=cc['sbe_arm']
        for sv_upper in (0,1):
            # The rule's T_DBE is the corner RUN, which includes main+SV-low(+SV-high).
            corner=cc['dbe_prep']+(2+sv_upper)*cc['dbe_cold']+cc['build']
            measured_ratio=corner/first
            predicted=measured_ratio*(8*hit+5*(first-hit))/3600
            actual_model=(8*cc['dbe_arm']+5*cc['build'])/3600
            overflow_mapping.append({'r_model':ratio,'machine':name,'SV_upper_solves':sv_upper,
                                     'T_first_s':first,'T_hit_s':hit,'T_DBE_corner_s':corner,
                                     'r_defined_by_candidate':measured_ratio,
                                     'rule_prediction_h':predicted,'eight_arm_model_h':actual_model,
                                     'rule_assigns':predicted<=112,'model_under_112':actual_model<=112})
out['overflow_operating_formula_vs_time_model'] = overflow_mapping
out['RCA11_scalar_synthetic_only'] = {
    'distance_um':.18, 'fibre_radius_um':.075,
    'recomputed_from_spacing': [{'spacing_um':d,'u':d/2,'contact':.18 <= .15+min(d/2,.075)} for d in [.10,.02]],
    'fixed_tol_contact':.18 <= .15 + plan['values_um']['tol_ff'],
    'interpretation':'Fixed registered input and tolerance remove this R re-selection freedom; they do not prove physical sampling invariance.'}
dump('summary.json',out)
print(json.dumps({'hash_pass':out['hash_checks_pass'],'hash_total':out['hash_checks_total'],
                  'model_json_equal':out['author_model_reproduces_stored_json'],
                  'base_arm':out['independent_model']['base_arm'], 'maxiter_5M':maxiter[2]},ensure_ascii=False,indent=2))
