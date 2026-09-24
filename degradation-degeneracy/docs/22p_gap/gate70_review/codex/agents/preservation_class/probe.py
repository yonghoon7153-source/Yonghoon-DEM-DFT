"""Executed review probe, retained as evidence; do not rerun blindly.

Class/index/cleanup inputs are owned fixtures. The precheck was documented as
read-only by production code, but it created an empty original-tree _claims
directory before failing on native Windows. See REPORT.md for that side effect.
"""
import ast
import json
import shutil
import sys
from pathlib import Path

REPO = Path('C:/Users/Administrator/Documents/Codex/g70_20260924/degradation-degeneracy')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))
from tools import preserve as P

cid = 'a' * 64
results = {}
for name in ('minimal', 'illtyped'):
    result = P._read_exec_class_at(HERE / 'fixtures' / f'{name}.json', cid)
    results[f'class_reader_{name}'] = result

results['malformed_index_members'] = P._declared_index_members(HERE / 'fixtures' / 'index.txt')
try:
    P.precheck_leg_run('grid_fit_v4', '5e660a8c73d5663a')
except Exception as exc:
    results['precheck_grid_fit_v4'] = {'error_type': type(exc).__name__, 'message': str(exc)}
else:
    results['precheck_grid_fit_v4'] = {'accepted': True}

# Run the exact session fixture body with ROOT redirected to owned fixture space.
# No pytest import, no product registry writes, no recursive deletion.
tree = ast.parse((REPO / 'tests' / 'conftest.py').read_text(encoding='utf-8'))
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
          and n.name == '_exec_class_registry_is_not_polluted_by_tests')
fn.decorator_list = []
probe_root = HERE / 'fixtures' / 'cleaner_root'
authority = probe_root / 'docs' / '22p_gap' / '_exec_class'
scope = {'ROOT': probe_root}
exec(compile(ast.Module(body=[fn], type_ignores=[]), str(REPO / 'tests' / 'conftest.py'), 'exec'), scope)
fixture = scope[fn.name]()
next(fixture)
new_record = authority / 'legitimate_new_canonical.json'
assert HERE in new_record.resolve().parents
shutil.copyfile(HERE / 'fixtures' / 'minimal.json', new_record)
results['cleaner_new_canonical_before_teardown'] = new_record.exists()
try:
    next(fixture)
except StopIteration:
    pass
results['cleaner_new_canonical_after_teardown'] = new_record.exists()
results['cleaner_existing_record_retained'] = (authority / 'existing.json').is_file()
print(json.dumps(results, indent=2, ensure_ascii=True))
