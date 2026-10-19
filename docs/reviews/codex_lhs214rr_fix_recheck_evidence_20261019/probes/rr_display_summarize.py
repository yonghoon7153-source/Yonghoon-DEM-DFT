"""Summarize current-versus-old full-page comparisons and test fixture diff."""
import difflib
import hashlib
import json
from pathlib import Path

review=Path(__file__).resolve().parents[1]
old=review.parent/'lhs214r_fix_recheck_20261017/source'
source=review/'source'
new_data=json.loads((review/'evidence/rr_display_extended_source.json').read_text(encoding='utf-8'))
old_data=json.loads((review/'evidence/rr_display_extended_old.json').read_text(encoding='utf-8'))
changes=[]
for case,new in new_data['cases'].items():
    prior=old_data['cases'][case]
    for where in ('loader','route'):
        a,b=prior.get(where,{}),new.get(where,{})
        for lab in sorted(a.keys() | b.keys()):
            if a.get(lab)!=b.get(lab):
                changes.append(dict(case=case,where=where,label=lab,old=a.get(lab),new=b.get(lab)))
template='webapp/templates/single.html'
old_template=(old/template).read_bytes(); new_template=(source/template).read_bytes()
test='webapp/test_pipeline_provenance.py'
fixture_diff=''.join(difflib.unified_diff((old/test).read_text(encoding='utf-8').splitlines(True),
    (source/test).read_text(encoding='utf-8').splitlines(True),fromfile='60ba39e22/'+test,tofile='77d8fd44/'+test))
(review/'evidence/rr_display_pipeline_fixture.diff').write_text(fixture_diff,encoding='utf-8')
summary=dict(cases=len(new_data['cases']),checks_each=len(new_data['checks']),
    source_failures=new_data['failures'],old_failure_count=len(old_data['failures']),
    changes=changes,changed_cases=len({c['case'] for c in changes}),
    old_new_template_equal=old_template==new_template,
    template_sha256=hashlib.sha256(new_template).hexdigest(),
    http={tree:{code:sum(r.get('http')==code for r in data['cases'].values()) for code in (200,500)}
          for tree,data in [('source',new_data),('old',old_data)]},
    input_files_all_unchanged=all(r.get('input_unchanged') for d in (new_data,old_data) for r in d['cases'].values()))
summary['all_changes_only_stale_delta_to_dash'] = all(
    c['old'] and c['new'] and len(c['old'])==len(c['new']) and
    all(a[:2]==b[:2] and b[2]=='—' for a,b in zip(c['old'],c['new'])) for c in changes)
summary['state_label_controls'] = []
for stem, token in [('valid_zero_0.0_no_through_path_', '비관통'),
                    ('not_computed_None_full_over_conduction_', 'full_over_conduction')]:
    for side in ('h','p','both'):
        name=stem+side+'_fourcol'
        r=new_data['cases'][name]
        label=next(k for k in r['route'] if k.startswith('σ_ionic network state'))
        cells=r['route'][label][0]
        affected=(0,) if side=='h' else (1,) if side=='p' else (0,1)
        summary['state_label_controls'].append(dict(case=name,cells=cells,
            passed=all(token in cells[i] for i in affected)))
(review/'evidence/rr_display_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ('changes','source_failures')},ensure_ascii=False))
