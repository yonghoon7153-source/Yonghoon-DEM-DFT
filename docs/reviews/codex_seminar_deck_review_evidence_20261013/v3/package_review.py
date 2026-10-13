"""Package review outputs; verify source files remain byte-identical."""
from pathlib import Path
import hashlib, json, zipfile

R = Path(__file__).resolve().parent
OLD = R.parent/'seminar_review_20261013'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((R/'evidence/input_manifest.json').read_text(encoding='utf8'))
checks=json.loads((R/'evidence/followup_checks.json').read_text(encoding='utf8'))
changed=[]
for ver in ['v2','v3']:
    for item in manifest['inventory'][ver]:
        p=R/ver/item['path']
        if sha(p)!=item['sha256']:changed.append(str(p))
for path,expected in checks['original_inputs_sha256'].items():
    if sha(Path(path))!=expected:changed.append(path)
assert not changed,changed
report=R/'codex_review_seminar_v3_20261013.md'
text=report.read_text(encoding='utf8')
for target in ['Q-SEM-1','Q-SEM-2','Q-SEM-3','Q-SEM-4','Q-SEM-5','Q-SEM-6','Q-SEM-7','Q-SEM-8','Q-SEM-9','Q-SEM-10','Q-SEM-11']:
    assert target in text,target
for i in range(1,20): assert f'| {i} |' in text,i
assert text.rstrip().endswith('**최종 판정: NO-GO — 현재 파일 그대로의 발표판 확정. 위 P0 편집 후 수정 PPT/PDF 재확인.**')
integrity={'original_files_changed':changed,'v2_v3_extracted_files_verified':sum(len(x) for x in manifest['inventory'].values()),
           'report_sha256':sha(report),'source_pptx_sha256':sha(R/'v3/seminar_20261013_draft.pptx'),
           'source_pdf_sha256':sha(R/'v3/seminar_20261013_draft.pdf'),'no_simulation_executed':True}
(R/'evidence/final_integrity.json').write_text(json.dumps(integrity,ensure_ascii=False,indent=2),encoding='utf8')
files=[]
for p in R.rglob('*'):
    if p.is_file() and not any(x in p.relative_to(R).parts for x in ['v2','__pycache__']):
        if p.name not in ['bundle_manifest.json']:files.append(p)
for sub in ['sources','evidence']:
    files.extend(p for p in (OLD/sub).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for name in ['codex_review_seminar_20261013.md','verify_results.py','audit_artifacts.py']:
    files.append(OLD/name)
entries=[{'path':str(p.relative_to(R.parent)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)]
(R/'bundle_manifest.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf8')
files.append(R/'bundle_manifest.json')
zpath=R.parent/'codex_seminar_v3_review_20261013.zip'
with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(p,p.relative_to(R.parent))
with zipfile.ZipFile(zpath) as z:
    assert z.testzip() is None
    for entry in entries:
        assert hashlib.sha256(z.read(entry['path'])).hexdigest()==entry['sha256']
print(json.dumps({'report':str(report),'zip':str(zpath),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath),'files':len(files),**integrity},ensure_ascii=False,indent=2))
