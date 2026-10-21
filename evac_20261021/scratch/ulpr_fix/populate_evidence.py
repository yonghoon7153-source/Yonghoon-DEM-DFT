#!/usr/bin/env python3
"""Copy the 10-21 ULPR fix run outputs into the evidence folder + machine index (no authored prose).
python3 -I -B populate_evidence.py"""
import glob
import json
import os
import shutil

S = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/ulpr_fix'
EV = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-aa282bca507003e72/docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021'
CMD = {
    'ul_lib': 'python3 -I -B ul_lib.py --selftest', 'ul_s3': 'python3 -I -B ul_s3.py --selftest', 'ul_observers': 'python3 -I -B ul_observers.py --selftest',
    'ul_gates': 'python3 -I -B ul_gates.py --selftest', 'ul_reader': 'python3 -I -B ul_reader.py --selftest', 'ul_runner_test': 'python3 -I -B ul_runner_test.py --selftest',
    'seal_selftest': 'python3 -I -B seal_kit.py --selftest', 'seal_check': 'python3 -I -B seal_kit.py --check',
    'decks_selftest': 'python3 -I -B make_unload_decks.py --selftest', 'decks_check': 'python3 -I -B make_unload_decks.py --check',
    'hist_decks_selftest': 'python3 -I -B history_test/make_history_decks.py --selftest', 'hist_decks_check': 'python3 -I -B history_test/make_history_decks.py --check',
    'hist_read_selftest': 'python3 -I -B history_test/read_history.py --selftest',
}
STATES = [
    ('base_286a8d562', 'head', '286a8d562', '기준 = 원장 ULPR 등재 커밋 (키트 = 10-15 판 그대로)'),
    ('st_tests_first', 'st_tests_first', 'f1b911f76', '시험 먼저'),
    ('st_ulpr01', 'st_ulpr01', '55fff3eb1', 'ULPR-01 수정'),
    ('st_ulpr0304', 'st_ulpr0304', '2932b63bc', 'ULPR-03 · 04 수정'),
    ('st_guard1', 'st_guard1', 'c21b1a051', '지킴 시험 첫째'),
    ('prefix_guards', 'tf_guard2', 'f1b911f76 + 지킴 시험 (c21b1a051 · 28b66e116 의 ul_reader.py 시험 부분만 patch)', '고치기 전 판 (시험 먼저 코드) + 지킴 시험 다섯'),
]


def counts(path):
    txt = open(path, encoding='utf-8', errors='replace').read().splitlines()
    ok = sum(1 for ln in txt if ln.lstrip().startswith('✓'))
    bad = sum(1 for ln in txt if ln.lstrip().startswith('✗'))
    last = next((ln for ln in reversed(txt) if ln.strip()), '')
    return ok, bad, last[:200]


index = {'note': '키트 자체시험 · 검사 화면 (stdout + stderr) — 커밋마다 git archive 사본 (커밋 내용 그대로 · 키트 + 키트가 읽는 리포 파일) · 현재 폴더 = 사본 리포 뿌리 · '
                 '명령 = python3 -I -B <사본>/docs/data/ps45_unload_20261009/<cmd 의 스크립트> · BLAS 1 스레드 · Linux · Python 3.11.15 · '
                 'prefix_guards = 시험 먼저 커밋 사본에 뒤 두 지킴 커밋의 ul_reader.py 시험 부분만 patch (고치기 전 코드로 지킴 시험을 돌린 판)',
         'states': {}}
for dst, src, commit, what in STATES:
    sd = os.path.join(S, 'logs', src)
    dd = os.path.join(EV, 'logs', dst)
    os.makedirs(dd, exist_ok=True)
    ent = {'commit': commit, 'what': what, 'logs': {}}
    for p in sorted(glob.glob(os.path.join(sd, '*.log'))):
        name = os.path.basename(p)[:-4]
        shutil.copy2(p, os.path.join(dd, os.path.basename(p)))
        ok, bad, last = counts(p)
        ent['logs'][name] = {'cmd': CMD.get(name), 'n_check_lines_ok': ok, 'n_check_lines_fail': bad, 'last_line': last}
    index['states'][dst] = ent
with open(os.path.join(EV, 'logs', 'index.json'), 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=1)
    f.write('\n')

R = os.path.join(EV, 'results')
os.makedirs(R, exist_ok=True)
for n in ('pre_ul01_final.json', 'pre_ul01_final.log', 'probe_misc_final.json', 'probe_misc_final.log', 'mutations_final.json'):
    shutil.copy2(os.path.join(S, 'results_pin', n), os.path.join(R, n))
shutil.copy2(os.path.join(S, 'probes_out', 'mutations.json'), os.path.join(R, 'mutations_first_c21b1a051.json'))
os.makedirs(os.path.join(EV, 'tools'), exist_ok=True)
shutil.copy2(os.path.join(S, 'mutate.py'), os.path.join(EV, 'tools', 'mutate.py'))
CP = os.path.join(S, 'codex_pin')
CD = os.path.join(R, 'codex_probes_pin')
os.makedirs(CD, exist_ok=True)
for p in sorted(glob.glob(os.path.join(CP, 'logs', '*.log'))):
    shutil.copy2(p, os.path.join(CD, os.path.basename(p)))


def gp(log):
    d = json.loads(open(os.path.join(CP, 'logs', log), encoding='utf-8').read())
    res = d['results']
    return {'case_count': len(res), 'all_expectations_satisfied': d['all_expectations_satisfied'],
            'unsatisfied': {k: {'expected_gate': v['expected_gate'], 'gate': v['gate'], 'raw_status': v['raw_status'],
                                'problems_head': [x[:160] for x in v.get('problems', [])[:2]]} for k, v in res.items() if not v['expectation_satisfied']},
            'satisfied_gate_false': sorted(k for k, v in res.items() if v['expectation_satisfied'] and not v['gate']),
            'satisfied_gate_true': sorted(k for k, v in res.items() if v['expectation_satisfied'] and v['gate'])}


ev = os.path.join(CP, 'evidence')
rr = json.load(open(os.path.join(ev, 'resume_recheck.json'), encoding='utf-8'))
rq = json.load(open(os.path.join(ev, 'receipt_ids_recheck.json'), encoding='utf-8'))
ha = json.load(open(os.path.join(ev, 'history_actual_audit.json'), encoding='utf-8'))
gt = json.load(open(os.path.join(ev, 'grammar_types.json'), encoding='utf-8'))
gw = json.load(open(os.path.join(ev, 'grammar_windows_r32.json'), encoding='utf-8'))
summ = {
    'kit_source': '리뷰 핀 28b66e116 git archive (키트 SHA256SUMS sha256 ecf406a6… · history_test/SHA256SUMS 8ff722d2…)',
    'probes': '판정문 증거 docs/reviews/codex_dem_unloading_kit_fix_recheck_evidence_20261015/probes · support 바이트 그대로 + 사전 리뷰 변형 둘 (이 폴더 probes/)',
    'run': 'python3 -I -X utf8 -B probes/<탐침>.py (grammar_provenance = --run-id ulprfix_orig · kitreader = --run-id ulprfix_kitreader) · BLAS 1 스레드 · Linux',
    'resume_recheck': {'summary': rr.get('summary'),
                       'failed': {k: {'expected': v.get('expected'), 'pass': v.get('pass')} for k, v in rr['cases'].items() if not v.get('pass')}},
    'receipt_ids_recheck_original': 'rc 1 · IndexError 줄 296 (요약 JSON 없음 · 화면 = receipt_ids_recheck.log)',
    'receipt_ids_recheck_q4tolerant': {'summary': rq.get('summary'),
                                       'g2c_missing_column_actual_cli': rq['cases']['g2c_missing_column_actual_cli'],
                                       'g2c_c_cpl7_missing': {'matches': rq['cases']['g2c_c_cpl7_missing'].get('matches'),
                                                              'restore_status': rq['cases']['g2c_c_cpl7_missing']['actual']['restore']['returned']['status'],
                                                              'G2c': rq['cases']['g2c_c_cpl7_missing']['actual']['G2c']['returned']['status'],
                                                              'next_UB': rq['cases']['g2c_c_cpl7_missing']['actual']['restore']['next_UB']},
                                       'g2c_c_cpl8_missing': {'matches': rq['cases']['g2c_c_cpl8_missing'].get('matches'),
                                                              'restore_status': rq['cases']['g2c_c_cpl8_missing']['actual']['restore']['returned']['status'],
                                                              'G2c': rq['cases']['g2c_c_cpl8_missing']['actual']['G2c']['returned']['status'],
                                                              'next_UB': rq['cases']['g2c_c_cpl8_missing']['actual']['restore']['next_UB']}},
    'grammar_provenance_original': gp('grammar_provenance.log'),
    'grammar_provenance_kitreader': gp('grammar_provenance_kitreader.log'),
    'grammar_types': {'all_expectations_satisfied': gt.get('all_expectations_satisfied'),
                      'cases': {k: v.get('expectation_satisfied') for k, v in gt.get('cases', {}).items()},
                      'git_bash_smoke': gt.get('git_bash_smoke')},
    'history_actual': {k: ha.get(k) for k in ('reader_rc', 'equal_except_run_dir', 'rows', 'unsafe_members', 'sealed_manifest_matches')},
    'kit_byte_checks': open(os.path.join(CP, 'logs', 'kit_byte_checks.log'), encoding='utf-8').read().strip().splitlines()[-1],
    'grammar_windows_r32': {'initial': gw.get('initial'), 'crlf_counts': {k: v.get('crlf_count') for k, v in gw.get('file_bytes', {}).items()}},
    'not_run': {'source_audit.py': 'GitHub API · 앞 회차 폴더 · 그 핀 원천 목록 대조용'},
}
with open(os.path.join(CD, 'summary.json'), 'w', encoding='utf-8') as f:
    json.dump(summ, f, ensure_ascii=False, indent=1, default=str)
    f.write('\n')
print('ok', sorted(os.listdir(EV)), sorted(os.listdir(os.path.join(EV, 'logs'))), sorted(os.listdir(R)), sorted(os.listdir(CD)))
