"""Refute a blanket M56 equivalence claim with reviewer-owned tiny path inputs.

No research and no original-file writes. Calls the actual function directly;
the sole mutant change is historical is_dir -> exists. No helper is mocked.
"""
from pathlib import Path
import ast
import json
import os
import sys
OUT = Path(__file__).resolve().parent
REPO = Path(os.environ.get('RINT_REVIEW_REPO', str(OUT.parent / 'package/repo'))).resolve()
sys.path.insert(0, str(REPO / 'scripts'))
import rint_r_chain as RR

root = OUT / 'm56_synthetic'
root.mkdir(exist_ok=True)
(root / 'attempt_1').write_text('not a directory\n', encoding='utf-8')
(root / 'attempt_1.rejected.json').write_text('{}\n', encoding='utf-8')
s = {'resume': {'from': 1, 'copied': [], 'rerun': 'R', 'compared': [], 'determinism': 'assumed'},
     'runs': [{'name': 'R', 'outdir': 'R_arm1', 'arms': 1, 'arm_list': None}]}
src = Path(RR.__file__).read_text(encoding='utf-8')
node = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == 'resume_rerun_problem')
fn = ast.get_source_segment(src, node)
old = '    if not src.is_dir():'
new = '    if not src.exists():'
assert fn.count(old) == 1
ns = dict(RR.__dict__)
exec(compile(fn.replace(old, new), '<M56-exact-historical-mutation>', 'exec'), ns)
actual = RR.resume_rerun_problem(s, root / 'attempt_2', 'TIME_LIMIT', 'NEXT')
mutant = ns['resume_rerun_problem'](s, root / 'attempt_2', 'TIME_LIMIT', 'NEXT')
result = {'python': sys.version, 'scope': __doc__, 'summary': s, 'current': actual, 'mutant': mutant,
          'distinguishable': isinstance(actual, str) and mutant is None,
          'boundary': 'This is a direct helper counterexample to the equivalence label, not a current-code resume eligibility failure or full CLI replay.'}
(OUT / 'm56_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if result['distinguishable'] else 1)
