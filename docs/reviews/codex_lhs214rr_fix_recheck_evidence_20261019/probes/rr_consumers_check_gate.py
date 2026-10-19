"""Existing release checker rechecks the actual failing R04 reread gate."""
import json
from pathlib import Path
import rr_consumers_run as R
import lhs_release_build as RB

report = json.loads((R.EV / 'independent_r04.json').read_text(encoding='utf-8'))
root = Path(report['fixture_root'])
gate = root / 'batch/reread.json'
original = gate.read_bytes()
record = json.loads(original)
actual = report['variants']['h0_cf_flip']['reread']
cid = actual['case']
next(r for r in record['cases'] if r['case'] == cid).update(checks=actual['checks'], statuses=actual['statuses'], row_cells=actual['row_cells'])
try:
    gate.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    problems = RB.check_v13(str(root / 'output'), str(root / 'handover'))
finally:
    gate.write_bytes(original)
result = {'variant': 'h0_cf_flip', 'actual_gate_check_problems': problems,
          'K2_present': any('K2' in p for p in problems),
          'restored_check': RB.check_v13(str(root / 'output'), str(root / 'handover'))}
R.save('actual_gate_check.json', result)
print(json.dumps(result, ensure_ascii=False, indent=2))
