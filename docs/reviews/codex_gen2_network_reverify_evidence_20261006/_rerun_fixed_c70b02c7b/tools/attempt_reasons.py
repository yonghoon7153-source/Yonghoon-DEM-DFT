"""Read network_attempt.json left by each acceptance publication run → status · stage · failure reason (first 400 chars).

usage: python3 -I attempt_reasons.py <acceptance_dir>
"""
import json
import sys
from pathlib import Path

base = Path(sys.argv[1])
for lab in ('baseline', 'missing_full_cert', 'full_cert_from_cf', 'full_cert_from_h12', 'missing_cf_cert', 'cf_bad_conservation',
            'missing_constr_cert'):
    p = base / lab / 'network_attempt.json'
    try:
        a = json.loads(p.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        print(f'{lab}: no attempt record ({type(e).__name__})')
        continue
    keys = sorted(a)
    reason = a.get('latest_attempt_reason') or a.get('reason') or a.get('why') or ''
    print(f"{lab}: status={a.get('latest_attempt_status')!r} stage={a.get('latest_attempt_stage')!r} active={a.get('active_network_run_id')!r}")
    print(f"    keys={keys}")
    print(f"    reason={str(reason)[:700]}")
