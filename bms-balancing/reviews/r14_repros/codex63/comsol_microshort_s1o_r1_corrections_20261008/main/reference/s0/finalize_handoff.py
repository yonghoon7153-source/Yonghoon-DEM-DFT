"""Own artifact-only final packaging. No scientific/candidate program execution."""
import hashlib,json,pathlib,zipfile,time,datetime,stat
R=pathlib.Path(__file__).resolve().parent
t0=time.perf_counter()
def sh(b):return hashlib.sha256(b).hexdigest()
def gb(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def put(n,v):
    with (R/n).open('x',encoding='utf-8',newline='\n') as f: json.dump(v,f,indent=2,ensure_ascii=False);f.write('\n')
prov=json.loads((R/'SOURCE_PROVENANCE_EXPECTED.json').read_bytes())
rows=[]
for e in prov['entries']:
    b=(R/e['local_path']).read_bytes()
    if e['local_path'].endswith('.java.txt'): transform='identity';original=b
    elif e['local_path'].endswith('NEXT_MODEL_READINESS_DECISION.md'):
        assert b.endswith(b'\n') and b'\r' not in b
        transform='remove exactly one trailing LF then convert LF to CRLF';original=b[:-1].replace(b'\n',b'\r\n')
    else:
        assert b.endswith(b'\n');transform='remove exactly one trailing LF';original=b[:-1]
    assert gb(original)==e['git_blob_sha'],e['local_path']
    rows.append(dict(path=e['local_path'],transform_for_identity_comparison_only=transform,
                     local_bytes=len(b),reconstructed_original_bytes=len(original),reconstructed_original_sha256=sh(original),git_blob_match=True))
for n in ['COMSOL_MICROSHORT_S0_SEND_TO_CODEX_v2_DEEP_20261007.md','COMSOL_MICROSHORT_PHYSICS_REQUEST_DRAFT_20261007.md']:
    b=(R/'sources'/n).read_bytes();o=(pathlib.Path('C:/Users/Administrator/Downloads')/n).read_bytes()
    assert b[:-1]==o and b[-1:]==b'\n'
    rows.append(dict(path='sources/'+n,transform_for_identity_comparison_only='remove exactly one trailing LF',
                     local_bytes=len(b),original_bytes=len(o),original_sha256=sh(o),original_byte_comparison=True))
put('SOURCE_TEXT_EQUIVALENCE.json',{'scope':'Exact byte transformations for static reading copies only. No source file rewritten. Not native preservation evidence.',
    'comparisons':rows,'all_nine_comparisons_pass':True,'candidate_changed':False,'scientific_arithmetic_rerun':False})
excluded={'MANIFEST.json','FINAL_MANIFEST.json','FINAL_DELIVERY_RECEIPT.json','FINAL_TOOL_RETURN.json'}
payload={}
for p in sorted(R.rglob('*')):
    assert not p.is_symlink()
    if not p.is_file():continue
    rel=p.relative_to(R).as_posix()
    if rel in excluded or rel.endswith('.zip'):continue
    if rel=='DELIVERY_RECEIPT.json':rel='history/FIRST_DELIVERY_RECEIPT.json'
    if rel=='PRELIMINARY_PACKAGE_TOOL_RETURN.json':rel='history/PRELIMINARY_PACKAGE_TOOL_RETURN.json'
    assert rel.casefold() not in {x.casefold() for x in payload}
    payload[rel]=p.read_bytes()
manifest={'kind':'FINAL_S0_HANDOFF_MANIFEST','self_excluded':True,
    'files':[{'path':n,'bytes':len(b),'sha256':sh(b)} for n,b in payload.items()]}
put('FINAL_MANIFEST.json',manifest)
payload['MANIFEST.json']=(R/'FINAL_MANIFEST.json').read_bytes()
name='COMSOL_MICROSHORT_S0_DEEP_HANDOFF_20261007.zip'
with zipfile.ZipFile(R/name,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n,b in payload.items():z.writestr(n,b)
with zipfile.ZipFile(R/name) as z:
    assert set(z.namelist())==set(payload) and len(z.namelist())==len(payload)
    for i in z.infolist():
        p=pathlib.PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename
        assert not stat.S_ISLNK(i.external_attr>>16)
        assert z.read(i)==payload[i.filename]
    assert z.testzip() is None
b=(R/name).read_bytes()
result={'status':'S0_FINAL_HANDOFF_VERIFIED_NOT_NATIVE_APPROVAL',
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'zip':{'file':name,'bytes':len(b),'sha256':sh(b)},'payload_count_excluding_manifest':len(payload)-1,
    'manifest_sha256':sh(payload['MANIFEST.json']),
    'source_text_equivalence':{'all_nine_pass':True,'Java_byte_exact':True,'markdown_format_only_differences_disclosed':True},
    'checks':['exact_set','casefold_collisions','path_safety','no_links','member_bytes_sha256','CRC','manifest'],
    'recipient':None,'approved':False,'native_calls':0,'candidate_execution':0,'scientific_arithmetic_rerun':False,
    'elapsed_snapshot_before_receipt_write_and_tool_return_s':time.perf_counter()-t0}
put('FINAL_DELIVERY_RECEIPT.json',result)
assert json.loads((R/'FINAL_DELIVERY_RECEIPT.json').read_bytes())==result
result['final_snapshot_after_receipt_readback_before_tool_return_s']=time.perf_counter()-t0
print(json.dumps(result,indent=2,ensure_ascii=False))
