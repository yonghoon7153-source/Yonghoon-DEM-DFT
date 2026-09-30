"""Check evidence/source pins and package the read-only re-review."""
from pathlib import Path
import hashlib, json, re, zipfile

E=Path(__file__).resolve().parent
W=E.parent
R=W/'lhs_coverage_reverify_20260930'
O=W/'lhs_coverage_review_20260930'
report=W/'docs/reviews/codex_lhs_coverage_reverify_verdict_20260930.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
m=read(R/'source_manifest.json')
old=read(W/'lhs_coverage_evidence_20260930/source_manifest.json')
assert m['snapshot']=='ac484ba5cda082caffe2c3c408de86cbd760befc'
files={}
def add(p):
    files[p.relative_to(W).as_posix()]=p
add(report)
add(R/'source_manifest.json')
add(R/'prepare.py')
for x in m['candidate_targets']:
    p=R/'candidate'/x['path'];assert sha(p)==x['sha256'],p;add(p)
for group,folder in [('base_targets','baseline'),('candidate_targets','candidate')]:
    for x in old[group]:
        p=O/folder/x['path'];assert sha(p)==x['sha256'],p;add(p)
files['prior_source_manifest.json']=W/'lhs_coverage_evidence_20260930/source_manifest.json'
newbundle=R/'submitted/codex_lhs_coverage_reverify_request_20260930'
oldbundle=O/'candidate/docs/reviews/codex_lhs_coverage_request_20260930'
for x in m['patches']:
    p=newbundle/'patches'/x['name'];assert sha(p)==x['sha256']
    if 'first_review_sha256' in x:
        q=oldbundle/'patches'/x['name'];assert sha(q)==x['first_review_sha256'];add(q)
        assert p.read_bytes()!=q.read_bytes()
        assert p.read_text(encoding='utf-8').split('diff --git',1)[1]==q.read_text(encoding='utf-8').split('diff --git',1)[1]
for p in (R/'submitted').rglob('*'):
    if p.is_file():add(p)
for p in E.rglob('*'):
    if p.is_file() and '__pycache__' not in p.parts:add(p)
links=[]
for url in re.findall(r'\]\((C:/[^)]+)\)',report.read_text(encoding='utf-8')):
    path,sep,line=url.rpartition(':')
    if not sep or not line.isdigit():path,line=url,None
    p=Path(path);assert p.is_file(),url
    if line:assert 0<int(line)<=len(p.read_text(encoding='utf-8').splitlines()),url
    links.append(url)
a=read(E/'audit_results.json')
assert a['denominator_zero']['coverage_status_physics_v2'].startswith('blank:')
assert a['nan_isolated_radius']['coverage_status_physics_v2'].startswith('blank:')
assert a['valid_isolated_zero']['coverage_status_physics_v2']=='ok'
assert a['valid_isolated_zero']['coverage_AM_mean_physics_v2']==0
assert all(v['same'] for v in a['legacy_comparison'].values())
assert all(v['bad'] for v in a['ast_guard'].values())
p=read(E/'pipeline_results.json')
assert not p['atoms_only']['return']['success'] and p['atoms_only']['return']['status']=='failed'
assert p['atoms_only']['metrics'] is None
assert all(not v for v in p['status_schema'].values())
assert p['batch_copyshim']['rc']==0
h=read(E/'harvest_comparison.json')
assert h['old_new_calls']==16 and all(not v['mismatch'] for v in h['legacy_comparisons'])
assert h['tau_platform_control']['same']
d=read(E/'delta_results.json')
assert d['clean_harvester_import']['stdout']=='False'
assert d['schema_mutations']['missing_n_am_and_coverage']['pipeline_status']=='done'
assert d['schema_mutations']['area_nan']['pipeline_status']=='done'
rr=d['in_domain_rounding_false_alarm']
assert rr['in_domain'] and rr['contact_area_check']['all']['n_boundary_excluded']==0
assert rr['contact_area_check']['all']['n_beyond_tol']==1 and rr['diff_over_tol']>1.33
assert float(rr['decimal60_6sig_token'])==rr['tokens'][3]
assert all(v['all']['n_boundary_excluded']==1 for v in d['old_examples_at_production_entry'].values())
counts={}
for f in ['coverage_physics_vs_hertzian.log','lhs_descriptor_harvest.log','harvest_LF_control.log']:
    lines=(E/f).read_text(encoding='utf-8').splitlines()
    counts[f]=[sum(s.startswith('  ✓ ') for s in lines),sum(s.startswith('  ✗ ') for s in lines)]
assert counts['coverage_physics_vs_hertzian.log']==[16,0]
assert counts['lhs_descriptor_harvest.log']==[142,2]
assert counts['harvest_LF_control.log']==[143,1]
assert 'HOLD' in report.read_text(encoding='utf-8')
out=W/'outputs/codex_lhs_coverage_reverify_20260930.zip'
out.parent.mkdir(exist_ok=True)
checksums={k:sha(v) for k,v in sorted(files.items())}
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for k,p in sorted(files.items()):z.write(p,k)
    z.writestr('PACKAGE_SHA256SUMS.json',json.dumps(checksums,ensure_ascii=False,indent=2))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert all(hashlib.sha256(z.read(k)).hexdigest()==s for k,s in checksums.items())
meta=dict(snapshot=m['snapshot'],base=m['base'],file=out.name,bytes=out.stat().st_size,
    sha256=sha(out),members=len(files)+1,checked_local_report_links=len(links),
    verdict='HOLD',new_p1=0,closed=['LHSC-01','LHSC-02','LHSC-05','LHSC-06'],
    partial=['LHSC-03','LHSC-04'],patches={'0008':'GO','0009':'HOLD','0010':'HOLD','0011':'GO'},
    selftest_log_check_counts=counts)
out.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(meta,ensure_ascii=False,indent=2))

