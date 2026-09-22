"""Build/check the reviewer-owned handoff; does not alter the target checkout."""
import datetime,hashlib,json,pathlib,shutil,zipfile
H=pathlib.Path(__file__).resolve().parent;ROOT=H.parents[1]/'work/r17-followup3-head/bms-balancing'
OUT=H.parent/'R17_FOLLOWUP3_e834b01_REVIEW_PACKAGE.zip'
assert (H/'full.json').is_file() and (H/'TEST_RESULTS.json').is_file()
assert not OUT.exists(), 'Refuse to overwrite an existing delivery ZIP'
def sha(b):return hashlib.sha256(b).hexdigest()
for name in ['scripts/gc_partial.py','scripts/width_report.py','scripts/verify_run_receipt.py','bms_balancing/schema.py','bms_balancing/verify.py','bms_balancing/cycles.py','reviews/evidence_gate.py','reviews/R17_FOLLOWUP2_RESPONSE.md','tests/test_r17_followup2.py']:
 dst=H/'reviewed_source'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dst)
payload=[]
for p in sorted(H.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or p.name in ['PACKAGE_MANIFEST.json','PACKAGE_RECEIPT.json']:continue
 assert not p.is_symlink() and p.resolve().is_relative_to(H)
 rel=p.relative_to(H).as_posix();b=p.read_bytes();payload.append(dict(path=rel,bytes=len(b),sha256=sha(b)))
assert len({x['path'].casefold() for x in payload})==len(payload)
manifest=json.dumps(dict(head='e834b01e4066c5e78c06b6ed1f77878e5a27a481',payload=payload),ensure_ascii=False,indent=2).encode('utf-8')+b'\n'
(H/'PACKAGE_MANIFEST.json').write_bytes(manifest)
with zipfile.ZipFile(OUT,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for row in payload:z.write(H/row['path'],row['path'])
 z.writestr('PACKAGE_MANIFEST.json',manifest)
with zipfile.ZipFile(OUT) as z:
 names=z.namelist();assert len(names)==len(set(names))==len(payload)+1
 assert set(names)=={p['path'] for p in payload}|{'PACKAGE_MANIFEST.json'}
 assert z.testzip() is None and z.read('PACKAGE_MANIFEST.json')==manifest
 for row in payload:
  b=z.read(row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256']
r=dict(zip=str(OUT),bytes=OUT.stat().st_size,sha256=sha(OUT.read_bytes()),payload_count=len(payload),entries=len(payload)+1,
 manifest_sha256=sha(manifest),exact_set_size_sha_crc_verified=True,recipient_verification=None,
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Independent synthetic code review, no production edits or real-data refits')
(H/'PACKAGE_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(r,ensure_ascii=True,indent=2))
