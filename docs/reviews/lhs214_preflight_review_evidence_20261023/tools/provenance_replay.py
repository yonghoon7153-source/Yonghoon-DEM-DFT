"""Replay the ratification patches and old S0b failure without source edits."""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get('REPO_ROOT', Path(__file__).resolve().parents[4])).expanduser().resolve()
OUT = Path(os.environ.get('EVIDENCE_OUT', Path.cwd() / 'lhs214-reproduction')).expanduser().resolve()
OUT.mkdir(parents=True, exist_ok=True)
TOOL = 'scripts/supp20_input_receipt.py'
CODE = 'fe23f2b839f0a49adb077348fec6d4c85443b62a'
RAT = 'f82929b0644be39b44e9fba9ea04cf9d60de9146'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

package = (ROOT / 'docs/reviews/lhs214_relaunch_package_20261020.md').read_text()
blocks = re.findall(r'````diff\n(.*?)\n````', package, re.S)
assert len(blocks) == 2
scratch = OUT / 'ratification-replay'
scratch.mkdir(exist_ok=True)
git_dir = git('rev-parse', '--absolute-git-dir').decode().strip()
results = []
for number, block in enumerate(blocks):
    rel = re.search(r'^--- a/(.+)$', block, re.M).group(1)
    assert rel in ('docs/reviews/lhs_network_batch_registration_20261007_g2.md',
                   'docs/reviews/lhs_network_batch_registration_20261012_supp20.md')
    target = scratch / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(git('show', RAT + '^:' + rel))
    patch = OUT / ('ratification_' + str(number) + '.patch')
    patch.write_text(block.replace('⬜(날짜)', '10-21 ·') + '\n')
    # An explicit work tree keeps application away from the reviewed checkout,
    # even when EVIDENCE_OUT happens to be inside that checkout.
    base = ['git', '--git-dir', git_dir, '--work-tree', str(scratch), 'apply']
    subprocess.run(base + ['--check', str(patch)], cwd=scratch, check=True)
    subprocess.run(base + [str(patch)], cwd=scratch, check=True)
    equal = target.read_bytes() == git('show', RAT + ':' + rel)
    results.append({'file': rel, 'date_placeholders': block.count('⬜(날짜)'),
                    'matches_ratified_commit': equal})
    assert equal
(OUT / 'ratification-replay.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')

old = git('show', CODE + '^:' + TOOL)
old_path = OUT / 'old_receipt.py'
old_path.write_bytes(old)
program = "import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); ns={'__file__':sys.argv[2],'__name__':'independent_old'}; exec(compile(Path(sys.argv[3]).read_text(),sys.argv[2],'exec'),ns); raise SystemExit(ns['_selftest']())"
with (OUT / 'old_receipt_current_documents.log').open('w') as log:
    run = subprocess.run([sys.executable, '-I', '-c', program, str(ROOT / 'scripts'),
                          str(ROOT / TOOL), str(old_path)], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
lines = (OUT / 'old_receipt_current_documents.log').read_text().splitlines()
failures = [line for line in lines if line.startswith('  FAIL')]
old_result = {'rc': run.returncode, 'last': lines[-1], 'failures': failures,
              'old_source_sha256': hashlib.sha256(old).hexdigest()}
(OUT / 'old_receipt_current_documents.json').write_text(json.dumps(old_result, ensure_ascii=False, indent=2) + '\n')
assert run.returncode == 1 and len(failures) == 1 and 'S0b' in failures[0]
assert '121/122 PASS' in lines[-1]
print(json.dumps({'ratification': results, 'old_receipt_rc': run.returncode,
                  'old_receipt_last_line': lines[-1]}, ensure_ascii=False, indent=2))
