"""Model valid retry identity history on the proven staged positive fixture."""
import argparse, copy, json, shutil
from pathlib import Path
import r5_observation as p

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-name', default='r5_observation_retry', help='Fresh evidence subdirectory')
parser.add_argument('--baseline-output', default='r5_observation_run2', help='An existing successful main probe output directory')
args = parser.parse_args()
for value in (args.output_name, args.baseline_output):
    if Path(value).name != value or value in ('.', '..'):
        parser.error('Directory options must be plain subdirectory names')
DEST = p.R / 'evidence' / args.output_name
BASE = p.R / 'evidence' / args.baseline_output / 'control_new_plan'
if DEST.exists():
    parser.error(f'{DEST} already exists; choose a fresh --output-name')

def make(label, old_outcome='interrupted', old_plan=True, current_plan=True):
    root = DEST / label
    assert not root.exists()
    shutil.copytree(BASE, root)
    man = p.read(root / 'manifest.json')
    man['plan']['cohorts'][0].update(harvest_dir=str(root / 'harvest'), cohort=str(root / 'cohort.tsv'))
    p.write(root / 'manifest.json', man)
    w = p.read(p.worker_path(root))
    current = copy.deepcopy(w['attempts'][0])
    current.update(run=2, attempt=2)
    if not current_plan:
        current.pop('stage_plan')
    previous = copy.deepcopy(w['attempts'][0])
    previous.update(outcome=old_outcome)
    if old_outcome == 'done':
        previous['seal']['record_sha'] = 'older-record-hash-no-longer-current'
    else:
        previous['seal'].update(record_written=False, record_sha=None)
        previous.pop('stage_plan', None)
    if not old_plan:
        previous.pop('stage_plan', None)
    w['attempts'] = [previous, current]
    p.write(p.worker_path(root), w)
    logs = root / 'import_obs/log'
    existing = list(logs.iterdir())
    for src in existing:
        lines = src.read_text(encoding='utf8').splitlines()
        head = json.loads(lines[0])
        if old_outcome == 'done':
            clone = copy.deepcopy(head)
            clone['pid'] += 10000000
            clone['proc'] = str(clone['pid']) + '-aaaaaaaa'
            suffix = '.start.json' if src.name.endswith('.start.json') else '.txt'
            (logs / (clone['proc'] + suffix)).write_text(json.dumps(clone) + '\n' + ''.join(x + '\n' for x in lines[1:]), encoding='utf8')
        head['identity'].update(run_no='2', attempt='2')
        src.write_text(json.dumps(head) + '\n' + ''.join(x + '\n' for x in lines[1:]), encoding='utf8')
    if old_outcome != 'done':
        head = p.read(next(logs.glob('*.start.json')))
        head.update(proc='77777777-aaaaaaaa', pid=77777777)
        head['identity'].update(run_no='1', attempt='1')
        p.write(logs / '77777777-aaaaaaaa.start.json', head)
    return root

DEST.mkdir(parents=True, exist_ok=True)
out = []
for label, old_outcome, old_plan, current_plan, expected in (
    ('interrupted_then_done', 'interrupted', False, True, 0),
    ('two_completed_with_copies', 'done', True, True, 0),
    ('two_completed_current_fallback', 'done', True, False, 0),
    ('two_completed_missing_prior_plan', 'done', False, True, 1),
):
    out.append(p.audit(label, make(label, old_outcome, old_plan, current_plan), expected))
p.write(DEST / 'results.json', out)
print(f'{sum(x["passed"] for x in out)}/{len(out)} expected outcomes')
