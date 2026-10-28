from pathlib import Path
import json,hashlib,sys,importlib.util,copy
R=Path(__file__).resolve().parent
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for file in ['cache_verified.json','data_cache_verified.json','remote_manifest.json','remote_extra_manifest.json']:
 for x in json.loads((R/file).read_text(encoding='utf8')):
  candidates=[R/'repo'/x['path'],R/'before'/x['path'],R/'wslpin'/x['path'],R/'context'/Path(x['path']).name]
  valid=[p for p in candidates if p.is_file() and blob(p.read_bytes())==x['git_sha']]
  assert valid,(file,x['path'],x['git_sha'])
  p=valid[0];rows.append(dict(file=p.relative_to(R).as_posix(),git_sha=x['git_sha'],sha256=sha(p.read_bytes())))
a=(R/'before/scripts/run_network_194_parallel.py').read_bytes();b=(R/'repo/scripts/run_network_194_parallel.py').read_bytes()
assert a.count(b'_HEX40.match(gsha)')==2
assert a.replace(b'_HEX40.match(gsha)',b'_HEX40.fullmatch(gsha)')==b
assert all(x['same'] for x in json.loads((R/'b7_to_35_identity.json').read_text()))
assert all(x['same'] for x in json.loads((R/'registration_pin_identity.json').read_text()))
sys.path.insert(0,str(R/'repo/scripts'))
import run_network_194_parallel as N
spec=importlib.util.spec_from_file_location('before_runner',R/'before/scripts/run_network_194_parallel.py');B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B);B.ROOT=N.ROOT
old_crlf=[]
for label,kind in [('net194','production194'),('netsupp20','supp20')]:
 p=R/'independent'/f'{label}_relocated.json';v=json.loads(p.read_text());v['git']['sha']+='\r\n';dst=R/'independent'/f'{label}_old_crlf.json';dst.write_text(json.dumps(v),encoding='utf8')
 res=B.preflight_receipt_checks(dst,expect_set=kind,approved_sha='35f0327377a4213774010a090df4d224e50d29e1');bad=sorted(x['id'] for x in res['checks'] if not x['ok']);assert bad==['P10','P7'],bad;old_crlf.append({'set':kind,'bad':bad})
out={'all_pinned_bytes_unchanged_after_tests':True,'verified_records':len(rows),'files':rows,'runner_only_two_exact_replacements':True,'old_crlf_actual_calls':old_crlf}
(R/'independent/final_integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k!='files'},ensure_ascii=False))
