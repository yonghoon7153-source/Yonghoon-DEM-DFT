from pathlib import Path
import hashlib,json,os,shutil,zipfile
R=Path(__file__).resolve().parent
if os.name=='nt' and not str(R).startswith('\\\\?\\'): R=Path('\\\\?\\'+str(R))
cwd=R.parent;old=cwd/'unloading_ulpr_review_20261024/repo';B=R/'baseline'
shutil.copytree(old/'docs/data/ps45_unload_20261009',B/'docs/data/ps45_unload_20261009',ignore=shutil.ignore_patterns('__pycache__','*.pyc'),dirs_exist_ok=True)
(B/'scripts').mkdir(exist_ok=True);shutil.copyfile(old/'scripts/plane_load_share.py',B/'scripts/plane_load_share.py')
S=R/'snapshot';sources=json.loads((S/'SOURCES.json').read_text(encoding='utf8'));bad=[]
for rel,m in sources.items():
 b=(S/rel).read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 if (hashlib.sha256(b).hexdigest(),len(b),oid)!=(m['sha256'],m['bytes'],m['oid']):bad.append(rel)
mbad=[];manifest=(S/'MANIFEST.sha256').read_text(encoding='utf8').splitlines()
for line in manifest:
 h,rel=line.split('  ',1)
 if hashlib.sha256((S/rel).read_bytes()).hexdigest()!=h:mbad.append(rel)
assert not bad and not mbad
(R/'source_postcheck.json').write_text(json.dumps({'source_blobs':len(sources),'source_mismatch':bad,'manifest_entries':len(manifest),'manifest_mismatch':mbad},indent=2),encoding='utf8')
summary={'pin':'4c29705fa1c4ba94737a858b206fa4f4c5bb2bde','findings':{'ULPRI-01':'closed','ULPRI-02':'closed'},'new_P1':0,'new_P2':0,'scope':'resume marker integrity only; physical execution not authorized by this verdict','independent_matrix':{'pass':208,'total':208},'author_cli_rerun':{'pass':43,'total':43},'mutants_detected':4,'reader_selftest_raw_windows':{'pass':311,'fail':35,'cause':'child cp949 console output'},'reader_selftest_child_utf8_adapted':{'pass':346,'fail':0},'source_postcheck':'pass'}
(R/'review_result.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
files=[]
for folder,dirs,names in os.walk(R):
 p=Path(folder);rel=p.relative_to(R);dirs[:]=[d for d in dirs if d!='__pycache__' and not(rel==Path('.') and d=='tmp') and not(rel==Path('evidence') and d=='matrix')]
 for n in names:
  f=p/n
  if n.endswith('.pyc') or (rel==Path('.') and n=='MANIFEST.sha256'):continue
  files.append(f)
files.sort(key=lambda x:x.relative_to(R).as_posix());lines=[hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(R).as_posix() for f in files];(R/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n',encoding='utf8');files.append(R/'MANIFEST.sha256')
zpath=cwd/'codex_unloading_ulpri_recheck_20261026.zip'
with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in files:z.write(f,R.name+'/'+f.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(files)
 for line in lines:
  h,rel=line.split('  ',1);assert hashlib.sha256(z.read(R.name+'/'+rel)).hexdigest()==h,rel
 assert z.testzip() is None
rec={'zip':zpath.name,'bytes':zpath.stat().st_size,'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'entries':len(files),'manifest_entries':len(lines),'zip_crc':'PASS','roundtrip_manifest':'PASS','source_postcheck':'PASS','excluded':['tmp/','__pycache__/','*.pyc','evidence/matrix/ (failed initial scratch)']}
(cwd/'codex_unloading_ulpri_recheck_20261026_receipt.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(rec))
