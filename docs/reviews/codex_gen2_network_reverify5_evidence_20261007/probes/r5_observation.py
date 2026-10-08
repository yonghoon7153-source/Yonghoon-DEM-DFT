"""Independent staged audit CLI controls and mutations; no production execution.

Fixture data comes from review 4's one-case sealed baseline and real translated
pilot receipts. Only fixture construction rebinds record_sha after adding the
missing genuine pipeline stage shape; fault mutations leave the independent
record intact except named plan/skip controls.
"""
from pathlib import Path
import argparse, copy, json, os, shutil, subprocess, sys

R = Path(__file__).resolve().parents[1]
S = R / 'source'
OLD = R.parent / 'gen2_network_reverify4_20261007'
F = R / 'fixtures/observation_baseline'
E = R / 'evidence' / 'r5_observation_run2'
sys.path[:0] = [str(S / 'scripts'), str(S / 'webapp')]
import run_network_194_parallel as rn

CASE = 'lhs00_000'
STAGES = [dict(step=s, rc=0, ok=None if s == 'Network Merge' else True) for s in (
    'Parse', 'Bimodal Contact Analysis', 'Coverage Physics vs Hertzian', 'Network Solver (both modes)',
    'Network channel verdict (ionic/electronic/thermal)', 'Network stop contract (stop_after=network)',
    'Network ionic record check (승격 전 공용 기술 검사 · RGLR2-01)', 'Network Merge')]

def read(p):
    return json.loads(p.read_text(encoding='utf8'))

def write(p, j):
    p.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding='utf8')

def worker_path(root):
    return root / 'cases' / CASE / 'worker.json'

def record_paths(root):
    return [root / 'cases' / CASE / 'out/status.json', root / 'merged/lhs/status.json']

def set_record_stages(root, stages, copy_plan):
    for p in record_paths(root):
        j = read(p)
        rec = j['cases'][CASE]
        rec.update(stages=copy.deepcopy(stages), mode='bimodal')
        write(p, j)
    w = read(worker_path(root))
    w['attempts'][-1]['seal']['record_sha'] = rn._rec_sha(rec)
    w['attempts'][-1]['outcome'] = 'done'
    if copy_plan:
        w['attempts'][-1]['stage_plan'] = rn.stage_plan_of(rec)
    write(worker_path(root), w)

def make_control(label, copy_plan):
    root = E / label
    assert not root.exists(), f'Use a fresh output directory: {root}'
    base = F / 'seal_baseline' if F.is_dir() else OLD / 'fixtures/seal_baseline'
    shutil.copytree(base, root)
    man = read(root / 'manifest.json')
    man.update(repo_root=str(S), worker_script=str(S / 'scripts/lhs_webapp_batch.py'),
               observe_imports=True, import_obs_run_id='81dc4ccc995152e9f06cfbc45d1cae8e')
    man['plan']['cohorts'][0].update(harvest_dir=str(root / 'harvest'), cohort=str(root / 'cohort.tsv'))
    write(root / 'manifest.json', man)
    set_record_stages(root, STAGES, copy_plan)
    logs = root / 'import_obs/log'
    logs.mkdir(parents=True, exist_ok=True)
    original = F / 'receipt_log' if F.is_dir() else OLD / 'evidence/receipt_path_translation/import_obs/log'
    # Trusted fixture preparation only: receipts are unchanged reviewed data.
    # Replace the explicitly documented old source root, not arbitrary receipt
    # paths/instructions. This is platform relocation, not proof of authenticity.
    old_root = read(F / 'provenance.json')['translated_source_root'] if F.is_dir() else (OLD / 'source').as_posix()
    for start in original.glob('*.start.json'):
        j = read(start)
        if j['identity']['case'] != 'lhs00_055':
            continue
        token = start.name[:-len('.start.json')]
        for suffix in ('.start.json', '.txt'):
            text = (original / (token + suffix)).read_text(encoding='utf8')
            text = text.replace(old_root, S.as_posix()).replace('lhs00_055', CASE)
            (logs / (token + suffix)).write_text(text, encoding='utf8')
    return root

def processes(root):
    return rn.import_observation(root / 'import_obs', S)['processes']

def proc_for(root, name):
    return next(p for p in processes(root) if Path(p['main']).name == name)

def remove(root, name, pair=True):
    token = proc_for(root, name)['proc']
    for suffix in (['.start.json', '.txt'] if pair else ['.txt']):
        (root / 'import_obs/log' / (token + suffix)).unlink()

def duplicate(root, name):
    p = proc_for(root, name)
    oldtoken = p['proc']
    token = str(p['pid'] + 10000000) + '-aaaaaaaa'
    for suffix in ('.start.json', '.txt'):
        src = root / 'import_obs/log' / (oldtoken + suffix)
        lines = src.read_text(encoding='utf8').splitlines()
        head = json.loads(lines[0])
        head.update(proc=token, pid=p['pid'] + 10000000)
        (root / 'import_obs/log' / (token + suffix)).write_text(json.dumps(head) + '\n' + ''.join(x + '\n' for x in lines[1:]), encoding='utf8')

def plan_mutate(root, fn):
    w = read(worker_path(root))
    fn(w['attempts'][-1])
    write(worker_path(root), w)

def failed_old_attempt(root):
    w = read(worker_path(root))
    w['attempts'].insert(0, dict(run=0, attempt=0, outcome='interrupted'))
    write(worker_path(root), w)
    head = read(next((root / 'import_obs/log').glob('*.start.json')))
    head.update(proc='77777777-aaaaaaaa', pid=77777777)
    head['identity'].update(run_no='0', attempt='0')
    write(root / 'import_obs/log/77777777-aaaaaaaa.start.json', head)

def audit(label, root, expect):
    env = dict(os.environ)
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    p = subprocess.run([sys.executable, '-B', str(S / 'scripts/run_network_194_parallel.py'), 'audit',
                        '--root', str(root), '--json', str(root / 'audit.json')], capture_output=True, text=True, encoding='utf8', env=env)
    (root / 'audit.log').write_text(p.stdout + p.stderr, encoding='utf8')
    a = read(root / 'audit.json')
    obs = a.get('import_observation') or {}
    row = dict(label=label, rc=p.returncode, expected_rc=expect, passed=p.returncode == expect,
               verdicts=a.get('verdicts'), merged=a.get('merged'), generation_problems=a.get('generation_problems'),
               input_problems=a.get('input_problems'), observation_problems=a.get('import_observation_problems'),
               n_started=obs.get('n_started'), n_finalized=obs.get('n_finalized'),
               completed=obs.get('completed_attempts'), unfinalized_noncompleted=obs.get('unfinalized_noncompleted'),
               stage_binding=obs.get('stage_binding'), audit=str(root / 'audit.json'))
    print(json.dumps({k: row[k] for k in ('label','rc','expected_rc','passed','observation_problems')}, ensure_ascii=False), flush=True)
    return row

def main():
    global E
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-name', default='r5_observation_run2', help='Fresh subdirectory beneath evidence; existing evidence is never overwritten')
    args = parser.parse_args()
    if Path(args.output_name).name != args.output_name or args.output_name in ('.', '..'):
        parser.error('--output-name must be one plain directory name')
    E = R / 'evidence' / args.output_name
    if E.exists():
        parser.error(f'{E} already exists; choose a fresh --output-name')
    E.mkdir(parents=True, exist_ok=True)
    old = make_control('control_old_fallback', False)
    new = make_control('control_new_plan', True)
    out = [audit('control_old_fallback', old, 0), audit('control_new_plan', new, 0)]
    assert all(x['passed'] and not x['observation_problems'] for x in out), 'Positive controls must pass first'
    variants = []
    for script in ('parse_liggghts.py', 'analyze_contacts_bimodal.py', 'coverage_physics_vs_hertzian.py', 'network_conductivity.py', 'lhs_webapp_batch.py'):
        variants.append(('pair_missing_' + script[:-3], lambda root, s=script: remove(root, s), 1))
    variants.extend([
        ('parser_final_missing', lambda r: remove(r, 'parse_liggghts.py', False), 1),
        ('coverage_pair_missing_contact_duplicate', lambda r: (remove(r, 'coverage_physics_vs_hertzian.py'), duplicate(r, 'analyze_contacts_bimodal.py')), 1),
        ('unexpected_duplicate_parser', lambda r: duplicate(r, 'parse_liggghts.py'), 1),
        ('only_worker_solver', lambda r: [remove(r, s) for s in ('parse_liggghts.py','analyze_contacts_bimodal.py','coverage_physics_vs_hertzian.py')], 1),
        ('plan_mismatch', lambda r: plan_mutate(r, lambda a: a['stage_plan']['stages'].pop(2)), 1),
        ('plan_missing_current_fallback', lambda r: plan_mutate(r, lambda a: a.pop('stage_plan')), 0),
        ('unknown_stage', lambda r: set_record_stages(r, STAGES + [dict(step='Mystery Stage', rc=0, ok=True)], True), 1),
        ('stage_e_out_of_scope', lambda r: set_record_stages(r, STAGES + [dict(step='Stage E (literature-grounded grain corrections)', rc=0, ok=True)], True), 1),
        ('csv_fallback_legitimate', lambda r: (set_record_stages(r, [dict(step='Parse (CSV fallback)', rc=0, ok=None)] + STAGES[1:], True), remove(r,'parse_liggghts.py')), 0),
        ('noncompleted_unfinalized', failed_old_attempt, 0),
    ])
    for label, fn, expect in variants:
        root = E / label
        shutil.copytree(new, root)
        man = read(root / 'manifest.json')
        man['plan']['cohorts'][0].update(harvest_dir=str(root / 'harvest'), cohort=str(root / 'cohort.tsv'))
        write(root / 'manifest.json', man)
        fn(root)
        out.append(audit(label, root, expect))
    write(E / 'results.json', out)
    print(f'{sum(x["passed"] for x in out)}/{len(out)} expected outcomes', flush=True)

if __name__ == '__main__':
    main()
