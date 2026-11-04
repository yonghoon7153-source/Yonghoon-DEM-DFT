"""Small real prepare/observe API boundary check; no frames or simulator.

Usage: python probe_unmocked_binding.py /path/to/repo
Temporary generated text inputs are local synthetic fixtures, never research runs.
"""
import hashlib
import json
from pathlib import Path
import platform
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'scripts'))
import mixer_precal_prepare as P
import mixer_precal_observe as O


def snapshot(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob('*') if p.is_file()}


rows = []
with tempfile.TemporaryDirectory(prefix='precal-binding-') as tmp:
    for cid in P.CASE_IDS:
        item = P.prepare_case(cid)
        run = Path(tmp) / cid
        (run / 'post').mkdir(parents=True)
        (run / 'in.mixer').write_bytes(item['deck'])
        (run / 'deck_meta.json').write_text(json.dumps(item['meta']), encoding='utf-8')
        before = snapshot(run)
        result = O.analyse_run(cid, run)
        assert result['status'] == 'TECH' and result['reasons'] == ['missing/duplicate t0'], result
        assert result['contact'] is None and result['mixing'] is None
        assert before == snapshot(run)
        assert 'make_mixer_resume' in result['provenance']['module_sha256']
        item['meta']['deck_sha256'] = '0' * 64
        (run / 'deck_meta.json').write_text(json.dumps(item['meta']), encoding='utf-8')
        before_bad = snapshot(run)
        bad = O.analyse_run(cid, run)
        assert bad['status'] == 'TECH' and bad['reasons'] == ['metadata does not bind actual deck bytes'], bad
        assert bad['contact'] is None and bad['mixing'] is None
        assert before_bad == snapshot(run)
        rows.append(dict(case_id=cid, valid_binding_stop=result['reasons'],
                         forged_hash_stop=bad['reasons'], inputs_unchanged=True,
                         both_refusals_without_metrics=True,
                         module_sha256=result['provenance']['module_sha256']))
print(json.dumps(dict(python=platform.python_version(), cases=rows,
                     valid_bindings_reaching_missing_frame=len(rows),
                     forged_hashes_rejected=len(rows), mock_used=False,
                     limitation='Negative input-binding boundary only; no positive 100000-particle pipeline, frames, research result, simulator, host or physical qualification.'), indent=2))
