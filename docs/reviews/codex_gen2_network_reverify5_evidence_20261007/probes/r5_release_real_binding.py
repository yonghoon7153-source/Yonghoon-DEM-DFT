"""Review gate test using a genuine audit-produced stage mismatch payload.

The real audit is a synthetic one-case launcher audit CLI (rc 1), supplied by
the independent observation probe. Graft its emitted binding payload into the
detailed production194 gate fixture; no actual production194 claim is made.
"""
from pathlib import Path
import contextlib
import argparse
import copy
import io
import json
import sys
from unittest.mock import patch

R = Path(__file__).resolve().parents[1]
S = R / 'source'
ap=argparse.ArgumentParser();ap.add_argument('--output-name',default='r5_release_real_binding');args=ap.parse_args()
assert Path(args.output_name).name==args.output_name and args.output_name not in ('.','..')
E = R / 'evidence' / args.output_name
assert not E.exists(), 'Choose a fresh --output-name; preserve existing evidence'
E.mkdir(parents=True, exist_ok=True)
sys.path[:0] = [str(S / 'scripts'), str(S / 'webapp')]
p = S / 'scripts/test_lhs_release_v13.py'
ns = {'__file__': str(p), '__name__': 'review_fixture'}
exec(compile(p.read_text(encoding='utf8').split("print('V0  API')")[0], str(p), 'exec'), ns)
lb = ns['LRB']
src = R / 'evidence/r5_observation_run2/pair_missing_parse_liggghts/audit.json'
actual = json.loads(src.read_text(encoding='utf8'))
actual_io = actual['import_observation']
original_key, bad_binding = next(iter(actual_io['stage_binding']['attempts'].items()))
assert actual_io['problems'] == []
assert actual['import_observation_problems']
assert bad_binding['expected']['scripts/parse_liggghts.py'] == 1
assert bad_binding['observed'].get('scripts/parse_liggghts.py', 0) == 0
HD = ns['make_g2_handover_dir'](str(E / 'handover'))
verdict = E / 'TEST_ONLY_NOT_GO.md'
verdict.write_text('SYNTHETIC TEST ONLY. NOT AN APPROVAL.\n', encoding='utf8')
rows = []
for label in ('real_failure_summary_present', 'only_top_failure_list_cleared'):
    br = Path(ns['make_batch_root'](str(E / label / 'batch')))
    audit = json.loads((br / 'seal_audit.json').read_text(encoding='utf8'))
    bindings = audit['import_observation']['stage_binding']['attempts']
    key = next(iter(bindings))
    bindings[key] = copy.deepcopy(bad_binding)
    audit['import_observation_problems'] = [s.replace(original_key.split('|')[0], key.split('|')[0]) for s in actual['import_observation_problems']]
    if label == 'only_top_failure_list_cleared':
        audit['import_observation_problems'] = []
    (br / 'seal_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf8')
    row = dict(label=label, gate_problems=lb.v13_batch_gate_problems(str(br))[1])
    out = E / label / 'release'
    stream = io.StringIO()
    with patch.object(lb, 'v13_reread_tau', lambda *a, **k: []), contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
        try:
            lb.build_v13(out_dir=str(out), handover_dir=HD, batch_root=str(br), date='20991231', codex_verdict=str(verdict))
            row.update(build_accepted=True, check=lb.check_v13(str(out), HD))
        except Exception as ex:
            row.update(build_accepted=False, error=f'{type(ex).__name__}: {ex}')
    row['output_exists'] = out.exists()
    (E / label / 'build.log').write_text(stream.getvalue(), encoding='utf8')
    rows.append(row)
result = dict(scope=__doc__, actual_failed_audit=str(src), actual_binding=bad_binding,
              actual_obs_problems=actual_io['problems'], actual_top_problems=actual['import_observation_problems'], cases=rows)
(E / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(result, ensure_ascii=False, indent=2))
