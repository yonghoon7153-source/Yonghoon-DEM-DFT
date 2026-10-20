"""Write docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/_repro_ours_20261020/ :
our small outputs + probe path diff + helper scripts + results_ours.json (numbers for the README table).
Refuses to overwrite.  Usage: python3 -I build_repro_folder.py
"""
import hashlib
import json
import os
import shutil
import sys
import re

SCR = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad'
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a43562c127acff2de'
OURS = SCR + '/import_rq7_repro/rint_join_q7_recheck_20261020/evidence'
CODEX = SCR + '/import_rq7/x/rint_join_q7_recheck_20261020/evidence'
TOOLS = SCR + '/import_rq7_tools'
DEST = WT + '/docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/_repro_ours_20261020'
if os.path.exists(DEST):
    sys.exit('exists: ' + DEST)
os.makedirs(DEST + '/tools')


def sha_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(p):
    return json.load(open(p, encoding='utf-8'), parse_constant=float)


small = ['structure_minimal_replay.json', 'numeric_overflow_replay_current.json',
         'numeric_overflow_replay_baseline.json', 'q7_independent.json', 'submitted_new.json', 'submitted_old.json']
for f in small:
    shutil.copyfile(os.path.join(OURS, f), os.path.join(DEST, f))
shutil.copyfile(SCR + '/import_rq7_repro/probe_path_changes.diff', DEST + '/probe_path_changes.diff')
for t in ('patch_probes.py', 'json_compare.py', 'fixture_cmp.py', 'structure_summary.py', 'q7_summary.py',
          'q7_maxrel.py', 'npz_cmp.py', 'fail_sets.py', 'show_submitted.py', 'tree_vs_lstree.py',
          'manifest_vs_lstree.py', 'manifest_vs_tree.py', 'seal_scope.py', 'prior_vs_repo_named.py',
          'verify_package_manifest.py', 'list_zip.py', 'safe_extract.py', 'untar.py', 'build_import.py',
          'build_repro_folder.py'):
    shutil.copyfile(os.path.join(TOOLS, t), os.path.join(DEST, 'tools', t))

not_copied = {}
for f in sorted(os.listdir(OURS)):
    if f not in small:
        not_copied[f] = {'sha256': sha_file(os.path.join(OURS, f)), 'bytes': os.path.getsize(os.path.join(OURS, f))}


def tally(log):
    t = open(log, 'rb').read().decode('utf-8', 'replace')
    m = re.findall(r'^(\d+) PASS · (\d+) FAIL', t, re.M)
    if m:
        return f'{m[-1][0]} PASS / {m[-1][1]} FAIL'
    for k in ('STEP3 RINT SELFTEST PASS', 'SELFTEST PASS'):
        if k in t:
            return k
    return '?'


tests = {}
for f in sorted(os.listdir(OURS)):
    if f.startswith('submitted_') and f.endswith('.log'):
        tests[f] = {'ours': tally(os.path.join(OURS, f)), 'codex': tally(os.path.join(CODEX, f))}
q = load(os.path.join(OURS, 'q7_independent.json'))
qc = load(os.path.join(CODEX, 'q7_independent.json'))
sig = {}
for name in ('cnc_normal', 'cnc_registered_zero', 'cnc_doubled_all', 'rrm_normal', 'rrm_registered_zero', 'rrm_doubled_all'):
    a, b = qc['positive_controls'][name]['new']['sigma_eff'], q['positive_controls'][name]['new']['sigma_eff']
    sig[name] = {'codex': a, 'ours': b, 'rel_diff': abs(a - b) / abs(a)}
res = {
    'env_ours': {'python': q['python'], 'numpy': q['numpy'], 'scipy': q['scipy'], 'os': 'Linux (claude.ai cloud container, 4 vCPU)'},
    'env_codex': {'python': qc['python'], 'numpy': qc['numpy'], 'scipy': qc['scipy'], 'os': 'Windows'},
    'tree': {'current': 'worktree at d8808c164 (code = 2b9efa253; d8808c164 changes CLAUDE.md + two docs only)',
             'prior': 'git archive dcb97f1ed (scripts webapp + 7 docs/data paths + AGENTS.md CLAUDE.md)'},
    'tests_submitted': tests,
    'q7_sigma_direct_spsolve': sig,
    'q7_n9b': {'phi_sha256_codex': qc['n9b']['nan_zero']['old_nan']['phi']['sha256'],
               'phi_sha256_ours': q['n9b']['nan_zero']['old_nan']['phi']['sha256'],
               'nan_equals_zero_exact_ours': q['n9b']['nan_zero']['exact_equal'],
               'matrix_rhs_hashes_equal_codex_ours': qc['n9b']['nan_zero']['matrix'] == q['n9b']['nan_zero']['matrix'],
               'cut_deleted_sigma': {'codex': qc['n9b']['cut_deleted_k_changed']['generic_solve']['sigma_eff'],
                                     'ours': q['n9b']['cut_deleted_k_changed']['generic_solve']['sigma_eff']},
               'pure_cut_deleted_independent_ours': q['n9b']['pure_cut_deleted_independent']},
    'q7_summary_ours': q['summary'],
    'our_outputs_not_copied_here': not_copied,
}
with open(DEST + '/results_ours.json', 'x', encoding='utf-8') as fh:
    json.dump(res, fh, ensure_ascii=False, indent=2)
    fh.write('\n')
print(json.dumps(res['tests_submitted'], ensure_ascii=False, indent=1))
print(json.dumps(res['q7_sigma_direct_spsolve'], indent=1))
print('files', sum(len(f) for _, _, f in os.walk(DEST)))
