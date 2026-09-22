"""Verify saved observations; this is NOT independent replay of upstream mutation evidence."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent
rows={r['case']:r for r in json.loads((p/'import_full_cases/summary.json').read_text(encoding='utf-8'))}
for name in ('plain_control','zip_control','enabled_control'):
    assert rows[name]['completeness']=='PASS' and rows[name]['comparison']=='ACCEPTED',rows[name]
for name in ('disabled_but_explicit_import','relative_pythonpath'):
    assert rows[name]['completeness']=='PASS' and rows[name]['comparison']=='REJECTED',rows[name]
n=json.loads((p/'namespace_case_corrected/observation.json').read_text(encoding='utf-8'))
assert n['receipt']['startup']['startup_history']['status']=='failed'
assert 'sitecustomize' in n['receipt']['startup']['startup_history']['reason']
assert '_ReplayError' in n['completeness_result']
assert json.loads((p/'target_enabled.json').read_text())['rc']==0
assert json.loads((p/'target_disabled_venv.json').read_text())['rc']==1
assert 'test_an_enabled_user_site_still_compares_the_bytes' in (p/'target_disabled_venv.stdout.txt').read_text(encoding='utf-8')
assert json.loads((p/'preimages.json').read_text())['rc']==0
assert json.loads((p/'g64_replay.json').read_text())['rc']==1
a=json.loads((p/'FINAL_AUDIT.json').read_text(encoding='utf-8'))
assert not a['status']['stdout'] and not a['run_scope_diff']['stdout']
native=json.loads((p/'real_entry_sandbox_cases/observations.json').read_text(encoding='utf-8'))
assert len(native)==3
assert all(r['receipt_complete'] and r['entry_result']=='REJECTED' for r in native)
print('Saved observations consistent: 3 accepted controls; 3 normal-input rejection cases; 1 venv-dependent regression failure.')
print('No Linux kernel-lock pass or successful upstream mutation replay is claimed.')
