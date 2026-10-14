"""Read-only reconciliation of submitted LHS214 execution evidence.

Only writes the review's own evidence/evidence_recomputed.json. No solver imports.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'submitted/lhs214_run_evidence_1014_1520'
PIN = '1087a9b2f4a93aa6a3b0debc698a14fffa13488d'

def read_json(p):
    return json.loads(p.read_text(encoding='utf-8'))

def rows(p):
    with p.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def loc(p, pattern):
    return [i for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1) if re.search(pattern, line)]

def only(d, keys):
    return {k: d.get(k) for k in keys}

def freq(values):
    return dict(Counter(str(v) for v in values))

result = {'review_pin': PIN, 'files': [], 'batches': {}, 'failures': [], 'comparisons': {}}
for p in sorted(BASE.rglob('*')):
    if p.is_file():
        result['files'].append({'path': str(p.relative_to(BASE)).replace('\\', '/'), 'bytes': p.stat().st_size, 'sha256': sha(p)})

manifests = []
for folder, logfile in [('net194_1087a9b2f', 'net194_run_1014_1431.log'), ('netsupp20_1087a9b2f', 'netsupp20_run_1014_1502.log')]:
    d = BASE / folder
    m, a, rr, merge = [read_json(d / name) for name in ['manifest.json', 'seal_audit.json', 'reread.json', 'merge_report.json']]
    manifests.append(m)
    progress, audit_rows = rows(d / 'progress.tsv'), rows(d / 'seal_audit.tsv')
    by_case = {r['case']: r for r in progress}
    queue = m['plan']['queue']
    qids = {r['case'] for r in queue}
    done = {r['case'] for r in progress if r['outcome'] == 'done'}
    failed = {r['case'] for r in progress if r['outcome'] == 'failed'}
    reread_ids = {r['case'] for r in rr['cases']}
    audit_by_case = {r['case']: r for r in a['cases']}
    procs = a['import_observation']['processes']
    by_proc_case = defaultdict(list)
    for p in procs:
        by_proc_case[p['identity']['case']].append(p)
    completed = {x[0] for x in a['import_observation']['completed_attempts']}
    bindings = a['import_observation']['stage_binding']['attempts']
    ts_start, ts_end = min(r['start'] for r in progress), max(r['end'] for r in progress)
    time_events = [(r['start'], 1) for r in progress] + [(r['end'], -1) for r in progress]
    live = max_live = 0
    for t, delta in sorted(time_events):
        live += delta
        max_live = max(max_live, live)
    loglines = (BASE / logfile).read_text(encoding='utf-8').splitlines()
    log_progress = []
    for lineno, line in enumerate(loglines, 1):
        match = re.match(r'\[(\d+)/(\d+)\] (\S+) (\S+) rc=(-?\d+).*?도는 중 (\d+)', line)
        if match:
            log_progress.append({'line': lineno, 'index': int(match[1]), 'n': int(match[2]), 'case': match[3], 'outcome': match[4], 'rc': int(match[5]), 'running': int(match[6])})
    log_digest = [json.loads(line.split('INPUT_DIGEST_JSON ', 1)[1]) for line in loglines if 'INPUT_DIGEST_JSON ' in line]
    local_source_hashes = {k: sha(ROOT / 'source' / k) for k in m['code_hashes'] if (ROOT / 'source' / k).exists()}
    queue_ids_digest = hashlib.sha256(('\n'.join(f"{x['case']}\t{x['cohort']}" for x in sorted(queue, key=lambda x:(x['cohort'],x['case'])))+'\n').encode()).hexdigest()
    code_fp_from_manifest = hashlib.sha256(json.dumps(sorted(m['code_hashes'].items()),separators=(',',':')).encode()).hexdigest()
    code_fp_from_source = hashlib.sha256(json.dumps(sorted(local_source_hashes.items()),separators=(',',':')).encode()).hexdigest()
    handover_hashes = {k: sha(ROOT/'source'/k) for k in m['handover_code_hashes'] if (ROOT/'source'/k).exists()}
    summary = {
        'manifest': only(m, ['created','git','expected_network_generation','seal','input_digest','import_obs_run_id','retries','argv','python_versions','lanes']),
        'n_queue': len(queue), 'n_queue_unique': len(qids),
        'progress_n': len(progress), 'progress_unique': len(by_case),
        'outcomes': freq(r['outcome'] for r in progress), 'rcs': freq(r['rc'] for r in progress),
        'attempts': freq(r['attempt'] for r in progress), 'runs': freq(r['run'] for r in progress),
        'signals': freq(r['signal'] for r in progress), 'failed_ids': sorted(failed),
        'queue_vs_progress_equal': qids == set(by_case),
        'queue_ids_sha256_recomputed': queue_ids_digest,
        'queue_ids_sha256_matches': queue_ids_digest == m['input_digest']['ids_sha256'],
        'cohorts': {c: freq(r['outcome'] for r in progress if r['cohort'] == c) for c in sorted({r['cohort'] for r in progress})},
        'time': {'first_start': ts_start, 'last_end': ts_end, 'timestamp_span_s': (datetime.fromisoformat(ts_end)-datetime.fromisoformat(ts_start)).total_seconds(), 'sum_worker_wall_s': sum(float(r['wall_s']) for r in progress), 'max_timestamp_overlap_half_open': max_live, 'max_log_running_after_completion': max(x['running'] for x in log_progress), 'run_summary_lines': [{'line': i, 'text': s} for i, s in enumerate(loglines,1) if '실행 끝' in s or '최대 동시' in s]},
        'rss_mb_range_all': [min(float(r['peak_rss_mb']) for r in progress), max(float(r['peak_rss_mb']) for r in progress)],
        'rss_mb_range_failed': [min(float(by_case[x]['peak_rss_mb']) for x in failed), max(float(by_case[x]['peak_rss_mb']) for x in failed)],
        'log': {'progress_n': len(log_progress), 'progress_cases_equal': {x['case'] for x in log_progress} == qids, 'progress_outcome_rc_equal': all((x['outcome'], str(x['rc'])) == (by_case[x['case']]['outcome'], by_case[x['case']]['rc']) for x in log_progress), 'digest_count': len(log_digest), 'digest_equal_manifest': log_digest == [m['input_digest']]},
        'audit': {'n':len(a['cases']), 'verdicts_recount':freq(x['verdict'] for x in a['cases']), 'generations_recount':freq(x.get('generation') for x in a['cases']), 'record_status_recount':freq(x['record_status'] for x in a['cases']), 'ids_equal_progress':set(audit_by_case)==qids, 'progress_status_equal':all(x['record_status']==by_case[x['case']]['outcome'] for x in a['cases']), 'tsv_n':len(audit_rows), 'tsv_json_rows_equal':all(all(t[k]==str(audit_by_case[t['case']].get(k,'')) for k in ['cohort','record_status','verdict','form','merged','why']) and t['record_sha256']==audit_by_case[t['case']]['record_sha'] for t in audit_rows), 'fp_start_end_pin_match':all(x['fp_start']==x['fp_end']==m['seal']['code_fp'] and x['git_sha']==PIN for x in a['cases']), 'problems':only(a,['generation_problems','input_problems','code_root_changed_now','import_observation_problems']), 'audited_at':a['audited_at']},
        'import_observation': {'reported':only(a['import_observation'], ['n_processes','n_started','n_finalized','outside','problems','tmp_leftover','unfinalized_noncompleted']), 'processes_n':len(procs), 'processes_unique':len({x['proc'] for x in procs}), 'all_final':all(x['final'] for x in procs), 'roles':freq(x['role'] for x in procs), 'per_case_process_count':freq(len(v) for v in by_proc_case.values()), 'case_ids_equal_queue':set(by_proc_case)==qids, 'identity_matches_manifest':all(x['identity']['run_id']==m['import_obs_run_id'] and x['identity']['run_no']=='1' and x['identity']['attempt']=='1' for x in procs), 'completed_attempts_n':len(a['import_observation']['completed_attempts']), 'completed_cases_equal_done': completed==done, 'binding_attempt_n':len(bindings), 'binding_cases_equal_done':{k.split('|')[0] for k in bindings}==done, 'binding_expected_observed_equal':all(x['expected']==x['observed'] and not x['unclassified'] for x in bindings.values()), 'observed_files_union_count':len(set().union(*(set(x['files']) for x in procs))), 'files_outside_manifest_code_hashes':sorted(set().union(*(set(x['files']) for x in procs))-set(m['code_hashes']))},
        'reread': {'reported':only(rr,['n_fail','expected_n','read_n','set_equal','missing','extra','seal_fp','launch_sha','manifest_sha256']), 'n_cases':len(rr['cases']), 'unique':len(reread_ids), 'ids_equal_progress_done':reread_ids==done, 'missing_equal_failed':{x[0] for x in rr['missing']}==failed, 'failed_meta':[x for x in rr['meta'] if not x['ok']], 'failed_case_checks':[(x['case'],c) for x in rr['cases'] for c in x['checks'] if not c['ok']], 'manifest_sha_matches_actual':rr['manifest_sha256']==sha(d/'manifest.json'), 'physics_model_below_continuum': [{'case':x['case'], 'sigma_ratio':x['sigma_ratio']['physics']} for x in rr['cases'] if x['statuses']['physics'][0]=='MODEL_BELOW_CONTINUUM_BOUND'], 'status_counts': {mode:freq(x['statuses'][mode][0] for x in rr['cases']) for mode in ['hertz','physics','hertz_h12']}},
        'merge': {'reported':only(merge,['merged_at','cohorts','failures','structural','mixed_generation','anomalies','allow_mixed_generation']), 'failed_ids_equal_progress':{x['case'] for x in merge['failures']}==failed},
        'source_hash_checks': {'n_available':len(local_source_hashes), 'mismatches':[k for k,v in local_source_hashes.items() if v!=m['code_hashes'][k]], 'unavailable':sorted(set(m['code_hashes'])-set(local_source_hashes)), 'fp_recomputed_from_manifest':code_fp_from_manifest, 'fp_recomputed_from_source':code_fp_from_source, 'fp_matches':code_fp_from_source==code_fp_from_manifest==m['seal']['code_fp'], 'handover_n_available':len(handover_hashes), 'handover_mismatches':[k for k,v in handover_hashes.items() if v!=m['handover_code_hashes'][k]]},
    }
    for case in sorted(failed):
        f = d / 'failed' / case
        worker = read_json(f/'worker.json')
        attempt = read_json(f/'network_attempt.json')
        w = worker['attempts'][0]
        p = by_case[case]
        matching = {k:str(w[k])==p[k] for k in ['attempt','run','outcome','rc','wall_s','peak_rss_mb','contacts','start','end']}
        seal = w['seal']
        result['failures'].append({'batch':folder,'case':case,'progress_line':next(i for i,x in enumerate(progress,2) if x['case']==case), 'audit_tsv_line':next(i for i,x in enumerate(audit_rows,2) if x['case']==case), 'worker_attempt_count':len(worker['attempts']), 'progress_worker_match':matching, 'worker':only(w,['start','end','wall_s','batch_elapsed_s','rc','signal','peak_rss_mb','outcome','failed_stages','network_run_id','stage_plan']), 'attempt':attempt, 'seal_matches_audit':seal['record_sha']==audit_by_case[case]['record_sha'] and seal['fp_start']==seal['fp_end']==m['seal']['code_fp'] and seal['git_sha_start']==seal['git_sha_end']==PIN, 'log_lines':(f/'log.txt').read_text(encoding='utf-8').splitlines(), 'import_process_roles':freq(x['role'] for x in by_proc_case[case])})
    result['batches'][folder] = summary

p = read_json(BASE/'diag_lhsx054/network_conductivity_physics.json')
h = read_json(BASE/'diag_lhsx054/network_conductivity_hertzian.json')
c = p['solve_certificate_full']
result['diagnostic_lhsx054'] = {'physics':only(p,['solve_certificate_full','sigma_full','sigma_full_status','sigma_full_reason','ionic_status','ionic_status_reason','electronic_status','thermal_status','n_boundary_overlap','n_area_physics_unavailable','sigma_bulk_net','sigma_bulk_net_status','sigma_constr_net','sigma_constr_net_reason']), 'q_reconstructed_from_certificate':c['I_bottom']/c['delta_V']*c['g_to_q'], 'hertz':only(h,['sigma_full','sigma_full_status','sigma_full_reason','ionic_status','solve_certificate_full']), 'source_line_locations': {'physics_guard':loc(BASE/'diag_lhsx054/network_conductivity_physics.json',r'over_conduction_guard|sigma_ratio >|"I_bottom"|"g_to_q"|"sigma_full_reason"|"ionic_status"')}}
receipt = read_json(BASE/'supp20_postrun_receipt.json')
result['receipt'] = {'n_checks':len(receipt['checks']), 'n_checks_ok':sum(x['ok'] for x in receipt['checks']), 'failed_checks':[x for x in receipt['checks'] if not x['ok']], **only(receipt,['scope','rc','generated','manual','inputs','recorded','warnings'])}
result['comparisons'] = {'manifest_code_hashes_equal': manifests[0]['code_hashes']==manifests[1]['code_hashes'], 'manifest_handover_code_hashes_equal':manifests[0]['handover_code_hashes']==manifests[1]['handover_code_hashes'], 'pin_all_match':all(x['git']['sha']==PIN for x in manifests), 'fp_all_match':len({x['seal']['code_fp'] for x in manifests})==1, 'failed_attempt_reasons':freq(x['attempt']['reason'] for x in result['failures']), 'failure_attempt_pins':freq(x['attempt']['code_sha'] for x in result['failures']), 'failure_stage_plans':freq(json.dumps(x['worker']['stage_plan']['stages'],sort_keys=True) for x in result['failures'])}
out = ROOT/'evidence/evidence_recomputed.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
compact = {'files':len(result['files']), 'batches':{k:{field:v[field] for field in ['n_queue','outcomes','cohorts','time','log','audit','import_observation','source_hash_checks']} for k,v in result['batches'].items()}, 'q_lhsx054':result['diagnostic_lhsx054']['q_reconstructed_from_certificate'], 'comparisons':result['comparisons']}
print(json.dumps(compact,ensure_ascii=False,indent=2))
