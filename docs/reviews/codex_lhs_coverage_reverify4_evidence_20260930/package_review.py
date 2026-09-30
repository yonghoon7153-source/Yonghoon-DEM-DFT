"""Pin reviewed source and archive the Korean verdict plus independent evidence."""
from pathlib import Path
import hashlib,json,re,zipfile,platform
E=Path(__file__).resolve().parent;R=E.parent;W=R.parent
OUT=W/'outputs';OUT.mkdir(exist_ok=True)
name='codex_lhs_coverage_reverify4_20260930'
report=W/'docs/reviews/codex_lhs_coverage_reverify4_verdict_20260930.md'
prior=W/'lhs_coverage_reverify3_20260930/candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((R/'source_manifest.json').read_text(encoding='utf-8'))
changed={row['path'] for row in m['candidate_targets']}
for row in m['candidate_targets']:
    assert sha(R/'candidate'/row['path'])==row['sha256'],row['path']
    assert sha(prior/row['path'])==row['before_sha256'],row['path']
for row in m['actual_base']['candidate_targets']:
    assert sha(prior/row['path'])==row['sha256'],row['path']
assert sha(Path(m['input_zip']['path']))==m['input_zip']['sha256']
links=[]
for raw in re.findall(r'\]\((C:/[^)]+)\)',report.read_text(encoding='utf-8')):
    ma=re.fullmatch(r'(.*?):(\d+)',raw)
    p=Path(ma.group(1) if ma else raw)
    assert p.is_file(),raw
    if ma:assert 1<=int(ma.group(2))<=len(p.read_text(encoding='utf-8').splitlines()),raw
    links.append(raw)
files=[report,R/'prepare.py',R/'source_manifest.json']
files+=list((R/'submitted').rglob('*'))+list(E.rglob('*'))
sources=changed|{
    'AGENTS.md','scripts/lens_geometry.py','scripts/coverage_physics_vs_hertzian.py','scripts/plastic_coverage.py',
    'scripts/lhs_webapp_batch.py','webapp/pipeline_service.py','scripts/lhs_perc_extract.py'}
for s in sorted(sources-changed):
    assert sha(R/'candidate'/s)==sha(prior/s),s
files += [R/'candidate'/s for s in sorted(sources)]
files += [W/'lhs_coverage_reverify_evidence_20260930/prior_audit_results.json',
    W/'lhs_coverage_reverify3_20260930/source_manifest.json',
    W/'docs/reviews/codex_lhs_coverage_reverify3_verdict_20260930.md',
    W/'lhs_coverage_review_20260930/baseline/scripts/lhs_descriptor_harvest.py']
files=sorted(set(p for p in files if p.is_file() and '__pycache__' not in p.parts))
rows=[dict(path=p.relative_to(W).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
checks=dict(schema='independent_review_package/1',verdict='HOLD',new_P1=0,new_P2=['LHSC-03-R5'],
    closed_prior_P2=['LHSC-03-R4','LHSC-04-R4-PIN'],
    nonblocking_P3=['LHSC-04-R5-PIN-TYPE','LHSC-04-R5-DOMAIN'],
    input_zip=m['input_zip'],reviewed_source_unchanged_after_tests=True,prior_candidate_targets_unchanged=True,
    validated_report_links=len(links),python=platform.python_version(),files=rows,
    limitations=['Partial source bundle; complete repository and dependencies needed for full replay',
        'No DEM, installed engine execution, production batch, merge or remote jobs',
        'Submitted Linux selftests distinct from independent Windows execution',
        'Synthetic finite-sample validation is not a proof of all binary64 inputs'])
zp=OUT/(name+'.zip');assert not zp.exists(),'Do not overwrite delivered evidence'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(W).as_posix())
    z.writestr('PACKAGE_SHA256SUMS.json',json.dumps(checks,ensure_ascii=False,indent=2))
with zipfile.ZipFile(zp) as z:
    for row in rows:
        b=z.read(row['path'])
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
    assert len(z.namelist())==len(rows)+1
receipt=dict(path=str(zp),bytes=zp.stat().st_size,sha256=sha(zp),files=len(rows)+1,report_sha256=sha(report),
    input_zip_sha256=m['input_zip']['sha256'],reviewed_source_unchanged_after_tests=True,prior_candidate_targets_unchanged=True,
    validated_report_links=len(links))
(OUT/(name+'.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
