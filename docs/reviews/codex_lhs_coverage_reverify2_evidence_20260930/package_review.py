"""Package the read-only review and independently verify every archived member."""
from pathlib import Path
import hashlib, json, re, zipfile, platform
E=Path(__file__).resolve().parent; R=E.parent; W=R.parent
OUT=W/'outputs'; OUT.mkdir(exist_ok=True)
name='codex_lhs_coverage_reverify2_20260930'
report=W/'docs/reviews/codex_lhs_coverage_reverify2_verdict_20260930.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((R/'source_manifest.json').read_text(encoding='utf-8'))
for row in manifest['candidate_targets']:
    assert sha(R/'candidate'/row['path'])==row['sha256'], row['path']
    assert sha(W/'lhs_coverage_reverify_20260930/candidate'/row['path'])==row['before_sha256'],row['path']
for row in manifest['actual_base']['candidate_targets']:
    assert sha(W/'lhs_coverage_reverify_20260930/candidate'/row['path'])==row['sha256'],row['path']
assert sha(Path(manifest['input_zip']['path']))==manifest['input_zip']['sha256']
links=[]
for raw in re.findall(r'\]\((C:/[^)]+)\)',report.read_text(encoding='utf-8')):
    m=re.fullmatch(r'(.*?):(\d+)',raw)
    p=Path(m.group(1) if m else raw)
    assert p.is_file(),raw
    if m:assert 1<=int(m.group(2))<=len(p.read_text(encoding='utf-8').splitlines()),raw
    links.append(raw)
files=[report,R/'prepare.py',R/'source_manifest.json']
files+=list((R/'submitted').rglob('*'))+list(E.rglob('*'))
source_names={row['path'] for row in manifest['candidate_targets']} | {
    'AGENTS.md','scripts/coverage_physics_vs_hertzian.py','scripts/plastic_coverage.py',
    'scripts/lhs_webapp_batch.py','webapp/pipeline_service.py'}
files += [R/'candidate'/s for s in sorted(source_names)]
files += [W/'lhs_coverage_reverify_evidence_20260930/prior_audit_results.json',
          W/'lhs_coverage_reverify_20260930/source_manifest.json',
          W/'docs/reviews/codex_lhs_coverage_reverify_verdict_20260930.md',
          W/'lhs_coverage_review_20260930/baseline/scripts/lhs_descriptor_harvest.py']
files=sorted(set(p for p in files if p.is_file() and '__pycache__' not in p.parts))
rows=[dict(path=p.relative_to(W).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
checks=dict(schema='independent_review_package/1',verdict='HOLD',input_zip=manifest['input_zip'],
            source_unchanged_after_tests=True,prior_candidate_unchanged=True,validated_report_links=len(links),
            python=platform.python_version(),files=rows,
            limitations=['Partial source bundle, not a complete executable repository',
                         'No DEM/native LIGGGHTS/remote jobs/production batch',
                         'Official producer expression scalar evaluation is not an installed-build execution'])
zpath=OUT/(name+'.zip')
assert not zpath.exists(),'Do not overwrite a delivered package'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(W).as_posix())
    z.writestr('PACKAGE_SHA256SUMS.json',json.dumps(checks,ensure_ascii=False,indent=2))
with zipfile.ZipFile(zpath) as z:
    for row in rows:
        b=z.read(row['path'])
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
    assert len(z.namelist())==len(rows)+1
receipt=dict(path=str(zpath),bytes=zpath.stat().st_size,sha256=sha(zpath),files=len(rows)+1,
             report_sha256=sha(report),input_zip_sha256=manifest['input_zip']['sha256'],
             source_unchanged_after_tests=True,prior_candidate_unchanged=True,validated_report_links=len(links))
(OUT/(name+'.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
