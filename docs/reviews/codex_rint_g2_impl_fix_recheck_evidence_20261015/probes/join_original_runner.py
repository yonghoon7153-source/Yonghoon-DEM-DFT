"""Rerun the prior immutable join probes against this review snapshot.

Only virtual __file__ moves their output/root to this snapshot; probe text is
compiled unchanged. Record early failures and source digests as evidence.
"""
from pathlib import Path
import contextlib
import hashlib
import json
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent / 'rint_g2_impl_review_20261014/probes'
name = sys.argv[1]
assert name in ('join_adversarial.py', 'join_synthetic.py', 'join_global_precision.py')
raw = (OLD / name).read_bytes()
namespace = {'__name__': '__main__', '__file__': str(ROOT / 'probes' / name)}
record = {'source': str(OLD / name), 'source_sha256': hashlib.sha256(raw).hexdigest(),
          'virtual_file': namespace['__file__'], 'adaptation': 'none; source text unchanged'}
with (ROOT / 'evidence' / ('join_original_' + name[:-3] + '.log')).open('w', encoding='utf-8') as log:
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        try:
            exec(compile(raw, str(OLD / name), 'exec'), namespace)
            record['exit_code'] = 0
        except BaseException as exc:
            traceback.print_exc()
            record.update(exit_code=1, exception=type(exc).__name__, message=str(exc))
            # Preserve baseline rejection even when the old probe assumes full gate keys.
            if 'base' in namespace:
                base = namespace['base']
                record['baseline'] = {k: base[k] for k in ('status', 'rejections', 'entrance', 'g_geo', 'g_frame')}
(ROOT / 'evidence' / ('join_original_' + name[:-3] + '_run.json')).write_text(
    json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
print(name, record['exit_code'], record.get('exception', 'completed'))
sys.exit(record['exit_code'])
