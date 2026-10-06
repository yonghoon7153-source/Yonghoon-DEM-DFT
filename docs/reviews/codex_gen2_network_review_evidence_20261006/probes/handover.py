"""Re-read actual publication probe outputs through the production handover loader.

The batch record is a fixture captured from each published full_metrics record;
it is not a historical campaign receipt. No production files are modified.
"""
from pathlib import Path
import sys, json
R = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(R/'source/scripts'), str(R/'source/webapp')]
import lhs_design_dataset as lhs
import lhs_release_build as release

root = R/'evidence/publication'
labels = ['baseline', 'h12_as_primary', 'bad_psi', 'bad_electrode', 'partial_missing_g2']
results = []
for selected in [[x] for x in labels] + [['baseline', 'h12_as_primary'], ['baseline', 'bad_psi']]:
    wv = dict(stop_after='network', source='review fixture: published records', status={}, rows={})
    for case in selected:
        fm = json.loads((root/case/'full_metrics.json').read_text(encoding='utf8'))
        wv['status'][case] = dict(status='done', network_run_id=fm['network_run_id'])
        wv['rows'][case] = {k: '' if v is None else str(v) for k,v in fm.items()}
    try:
        got = lhs.load_tau_results(root, wv)
        result = dict(cases=selected, accepted=True, values={c: r['cells'] for c,r in got['cases'].items()},
                      same_generation_checks=got['same_generation_checks'])
    except Exception as exc:
        result = dict(cases=selected, accepted=False, error=repr(exc))
    results.append(result)
    print(selected, result['accepted'], result.get('error',''), flush=True)

# Name-based release gate does not independently inspect the upstream model.
# Do not claim that this minimal fixture is a complete 194-case handover.
results.append(dict(primary_names_appendix_only=release.appendix_only(['f_ion_hertz','tau2_ion_hertz']),
                    explicit_h12_names_appendix_only=release.appendix_only(['f_ion_hertz_h12','tau2_ion_hertz_h12'])))
(R/'evidence/handover.json').write_text(json.dumps(results, indent=2, ensure_ascii=False),encoding='utf8')
