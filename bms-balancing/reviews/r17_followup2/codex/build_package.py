"""Package review-owned evidence plus exact read-only source snapshots."""
import datetime, hashlib, json, pathlib, zipfile
H=pathlib.Path(__file__).resolve().parent
R=H.parents[1]/'work/r17-followup2-a4c311ef/bms-balancing'
identity=json.loads((H/'REVIEW_IDENTITY.json').read_text(encoding='utf-8'))
if identity['git_status'] or identity['bms_diff_fix_to_head']:
    raise RuntimeError('Unclean or unexpected code identity')
if not all(x['lf_normalized_equal'] for x in identity['files'].values()):
    raise RuntimeError('Source differs beyond recorded line endings')
payload={}
excluded={'PACKAGE_MANIFEST.json','PACKAGE_RECEIPT.json'}
for p in sorted(H.iterdir()):
    if p.is_file() and p.suffix in ('.md','.py','.json','.log','.xml') and p.name not in excluded:
        payload[p.name]=p.read_bytes()
for rel,meta in identity['files'].items():
    raw=(R/rel).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=meta['checkout_sha256']:
        raise RuntimeError('Source changed after final identity: '+rel)
    payload['source_snapshot/'+rel]=raw
producer=json.loads((H/'PRODUCER_READER_RESULTS.json').read_text(encoding='utf-8'))
fixture=pathlib.Path(producer['fixture']).resolve()
if not fixture.is_relative_to(H) or not fixture.name.startswith('producer-'):
    raise RuntimeError('Unexpected synthetic source')
for p in sorted(fixture.rglob('*')):
    if p.is_symlink():raise RuntimeError('Unexpected link in fixture')
    if p.is_file():payload['producer_fixture/'+p.relative_to(fixture).as_posix()]=p.read_bytes()
if len({k.casefold() for k in payload})!=len(payload):raise RuntimeError('Case collision')
manifest={'version':1,'target':identity['target'],'payload_count':len(payload),
    'files':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payload.items())]}
manifest_raw=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
(H/'PACKAGE_MANIFEST.json').write_bytes(manifest_raw)
payload['PACKAGE_MANIFEST.json']=manifest_raw
zpath=H/'R17_FOLLOWUP2_a4c311ef_REVIEW_PACKAGE.zip'
with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n,b in sorted(payload.items()):z.writestr(n,b)
with zipfile.ZipFile(zpath) as z:
    names=z.namelist()
    if len(names)!=len(set(names)) or set(names)!=set(payload):raise RuntimeError('Wrong archive set')
    if z.testzip() is not None:raise RuntimeError('CRC failure')
    for n,b in payload.items():
        if z.read(n)!=b:raise RuntimeError('Archive byte mismatch: '+n)
receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'archive':zpath.name,'bytes':zpath.stat().st_size,'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),
    'manifest_sha256':hashlib.sha256(manifest_raw).hexdigest(),'payload_count':manifest['payload_count'],
    'entries_including_manifest':len(payload),'exact_set_size_sha_crc_verified':True,
    'recipient_verification':None,'target':identity['target']}
(H/'PACKAGE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
