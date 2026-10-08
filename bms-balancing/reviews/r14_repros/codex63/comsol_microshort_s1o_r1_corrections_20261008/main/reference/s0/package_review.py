"""Own S0 artifact audit/packager. Never imports or executes supplied programs.
No COMSOL/JVM/native calls. Writes only new artifacts in this script's folder.
"""
import datetime
import difflib
import hashlib
import json
import pathlib
import re
import stat
import time
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
start = time.perf_counter()
def sha(b): return hashlib.sha256(b).hexdigest()
def put(name, obj):
    with (ROOT/name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write('\n')
def read(name): return (ROOT/name).read_bytes()
checks = {}
base = read('sources/Normal480Candidate.java.txt')
cand = read('candidate/MicroshortS1RestCandidate.java.inactive.txt')
checks['source_java_sha'] = sha(base) == 'c70526cf6884eabc57b63dd43dce4b47fb0decf59af68d3f550f1b987d053797'
checks['candidate_sha'] = sha(cand) == 'a90d1e66db796f6b8077fa1d158620d1ec548265a1508b698e35da8ef6e3492c'
changes = json.loads(read('candidate/LITERAL_CHANGE_MAP.json'))['changes']
text = base.decode('utf-8')
for c in changes:
    assert text.count(c['before']) == 1, c['name']
    text = text.replace(c['before'],c['after'],1)
checks['twenty_literal_changes_reconstruct_candidate'] = len(changes)==20 and text.encode('utf-8')==cand
for c in reversed(changes):
    assert text.count(c['after']) == 1, c['name']
    text = text.replace(c['after'],c['before'],1)
checks['reverse_reconstructs_original_bytes'] = text.encode('utf-8')==base
diff = ''.join(difflib.unified_diff(base.decode().splitlines(True),cand.decode().splitlines(True),
    fromfile='sources/Normal480Candidate.java.txt',tofile='candidate/MicroshortS1RestCandidate.java.inactive.txt'))
checks['unified_diff_exact'] = diff.encode()==read('candidate/S1_REVIEW_ONLY.diff.txt')
ct = cand.decode()
checks['entry_guard_text_and_no_runall'] = '.runAll(' not in ct and 'public static void main(String[] args) throws Exception { denyS0Execution(); }' in ct
times = [float(x) for x in read('candidate/REQUESTED_TIMES_S1_3600.txt').split()]
checks['times401_monotonic_endpoints'] = len(times)==401 and times[0]==0 and times[-1]==3600 and all(a<b for a,b in zip(times,times[1:]))
checks['pilot_common255_times'] = len([t for t in times if t<=120])==255
calc = json.loads(read('analysis/ANALYTIC_RESULT.json'))
ret = json.loads(read('analysis/ARITHMETIC_TOOL_RETURN.json'))
checks['arithmetic_output_matches_return'] = json.loads(ret['output'])==calc and ret['exit_code']==0
checks['arithmetic_checks_all_true'] = all(calc['own_arithmetic_checks'].values())
checks['arithmetic_source_bound'] = calc['source_java_text_sha256']==sha(base)
decision=json.loads(read('DECISION.json'))
checks['native_flags_false'] = decision['approved'] is False and decision['native_approved'] is False and decision['usable_for_native'] is False
checks['report_no_japanese'] = not re.search('[\u3040-\u30ff]',read('S0_REPORT_KO.md').decode())
checks['all_A_to_F_present'] = all(('## '+c+'.') in read('S0_REPORT_KO.md').decode() for c in 'ABCDEF')
assert all(checks.values()),checks

prov=json.loads(read('SOURCE_PROVENANCE_EXPECTED.json'))
records=[]
for e in prov['entries']:
    b=read(e['local_path'])
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    records.append(dict(e,bytes=len(b),sha256=sha(b),observed_git_blob=blob,exact_git_blob_match=blob==e['git_blob_sha']))
incoming=[]
for name in ['COMSOL_MICROSHORT_S0_SEND_TO_CODEX_v2_DEEP_20261007.md','COMSOL_MICROSHORT_PHYSICS_REQUEST_DRAFT_20261007.md']:
    p=pathlib.Path('C:/Users/Administrator/Downloads')/name
    b=p.read_bytes(); copy=read('sources/'+name)
    incoming.append({'path':str(p),'bytes':len(b),'sha256':sha(b),
        'reading_copy_sha256':sha(copy),'byte_match_to_reading_copy':b==copy,
        'utf8_text_match_normalized_line_endings':b.decode('utf-8-sig').replace('\r\n','\n')==copy.decode('utf-8-sig').replace('\r\n','\n')})
put('SOURCE_IDENTITIES.json',{'scope':'Current source copies vs pinned Git blobs and current incoming originals vs earlier reading copies. Not a remote-machine preservation audit.',
    'commit':prov['commit'],'repository_sources':records,'incoming_originals':incoming,
    'all_git_blobs_match':all(x['exact_git_blob_match'] for x in records),
    'all_incoming_bytes_match':all(x['byte_match_to_reading_copy'] for x in incoming)})
put('STATIC_ARTIFACT_AUDIT.json',{'kind':'OWN_TEXT_ARITHMETIC_ARTIFACT_CHECKS_NOT_CANDIDATE_FUNCTIONAL_TESTS',
    'checks':checks,'checks_count':len(checks),'status':'PASS','COMSOL_calls':0,'provided_program_execution':0,
    'source_blob_matches':sum(x['exact_git_blob_match'] for x in records),'source_blob_count':len(records)})

excluded={'MANIFEST.json','DELIVERY_RECEIPT.json','FINAL_PACKAGE_TOOL_RETURN.json'}
payload=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_symlink(): raise RuntimeError('SYMLINK_NOT_ALLOWED')
    if not p.is_file(): continue
    rel=p.relative_to(ROOT).as_posix()
    if rel in excluded or rel.lower().endswith('.zip'): continue
    if '__pycache__' in p.parts: raise RuntimeError('UNEXPECTED_PYCACHE')
    b=p.read_bytes()
    payload.append({'path':rel,'bytes':len(b),'sha256':sha(b)})
assert len({x['path'].casefold() for x in payload})==len(payload)
put('MANIFEST.json',{'kind':'S0_PAYLOAD_MANIFEST','self_excluded':True,'files':payload})
zipname='COMSOL_MICROSHORT_S0_DEEP_REVIEW_20261007.zip'
zp=ROOT/zipname
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for item in payload: z.write(ROOT/item['path'],item['path'])
    z.write(ROOT/'MANIFEST.json','MANIFEST.json')
expected={x['path']:x for x in payload}
with zipfile.ZipFile(zp) as z:
    names=z.namelist()
    assert set(names)==set(expected)|{'MANIFEST.json'} and len(names)==len(expected)+1
    assert len({n.casefold() for n in names})==len(names)
    for info in z.infolist():
        p=pathlib.PurePosixPath(info.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and ':' not in info.filename
        assert not stat.S_ISLNK(info.external_attr>>16)
        b=z.read(info)
        if info.filename=='MANIFEST.json': assert b==read('MANIFEST.json')
        else:
            e=expected[info.filename]
            assert len(b)==e['bytes'] and sha(b)==e['sha256']
    assert z.testzip() is None
for item in payload:
    assert sha(read(item['path']))==item['sha256']
zb=zp.read_bytes()
receipt={'status':'S0_PACKAGE_VERIFIED_NOT_NATIVE_APPROVAL','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'zip':{'file':zipname,'bytes':len(zb),'sha256':sha(zb)},'payload_count':len(payload),
 'manifest':{'bytes':len(read('MANIFEST.json')),'sha256':sha(read('MANIFEST.json'))},
 'checks':['exact_set','casefold_collisions','relative_safe_paths','no_symlinks','member_size_sha256','CRC','manifest_readback','local_payload_unchanged'],
 'source_git_blob_matches':sum(x['exact_git_blob_match'] for x in records),
 'incoming_originals_byte_matches':sum(x['byte_match_to_reading_copy'] for x in incoming),
 'recipient':None,'approved':False,'native_calls':0,'elapsed_snapshot_before_receipt_write_and_tool_return_s':time.perf_counter()-start}
put('DELIVERY_RECEIPT.json',receipt)
assert json.loads(read('DELIVERY_RECEIPT.json'))==receipt
print(json.dumps(dict(receipt,final_snapshot_after_receipt_readback_before_tool_return_s=time.perf_counter()-start),ensure_ascii=False,indent=2))
