"""Package reviewer artifacts; verify inputs unchanged and output archive exactness."""
import hashlib,json,pathlib,zipfile,datetime
ROOT=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
audit=json.loads((ROOT/'PACKAGE_AUDIT.json').read_bytes());src=pathlib.Path(audit['source']);raw=src.read_bytes()
assert len(raw)==audit['bytes'] and sha(raw)==audit['sha256']
source_manifest=json.loads((ROOT/'received/PACKAGE_MANIFEST.json').read_bytes())
for r in source_manifest['files']:
    b=(ROOT/'received'/r['file']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['file']
assert sha((ROOT/'received/PACKAGE_MANIFEST.json').read_bytes())==audit['manifest_sha256']
put(ROOT/'SOURCE_AFTER_CHECK.json',{'input_archive_bytes_unchanged':True,'input_archive_sha256':sha(raw),'extracted_payloads_unchanged':len(source_manifest['files']),'remote_current_files_verified':False,'received_code_executions':0})
put(ROOT/'REVIEWER_TOOL_NOTES.json',{'reviewer_diagnostic_notes':['A read-only path search had overbroad output and absent guessed paths; narrowed afterward. No permissions changed; no received code executed.'],'target_test_failures_observed_this_review':None,'static_counterexamples_are_not_target_executions':True})
excluded={'COMSOL63_NORMAL30_OFFLINE_REVIEW_20260928.zip','REVIEW_PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json'}
paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts)
manifest={'scope':'Independent static normal30 review; two revisions requested; no native approval','files':[{'file':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths]}
put(ROOT/'REVIEW_PACKAGE_MANIFEST.json',manifest)
target=ROOT/'COMSOL63_NORMAL30_OFFLINE_REVIEW_20260928.zip'
assert not target.exists(),'do not overwrite sealed reviewer package'
with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in paths:z.write(p,p.relative_to(ROOT).as_posix())
    z.write(ROOT/'REVIEW_PACKAGE_MANIFEST.json','REVIEW_PACKAGE_MANIFEST.json')
with zipfile.ZipFile(target) as z:
    names=z.namelist();assert len(names)==len(set(names))==len({s.casefold() for s in names})
    assert set(names)=={'REVIEW_PACKAGE_MANIFEST.json'}|{r['file'] for r in manifest['files']}
    assert z.testzip() is None
    for r in manifest['files']:
        b=z.read(r['file']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'reviewer generation; not native execution evidence or authorization','package':{'path':str(target),'bytes':target.stat().st_size,'sha256':sha(target.read_bytes())},'payload_count':len(paths),'manifest_sha256':sha((ROOT/'REVIEW_PACKAGE_MANIFEST.json').read_bytes()),'verification':'exact set/unique case paths/every size+SHA/CRC verified','recipient':None,'native30_approved':False,'received_code_executions':0}
put(ROOT/'DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
