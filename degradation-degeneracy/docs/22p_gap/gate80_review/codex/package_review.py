from pathlib import Path
import hashlib, json, subprocess, zipfile
O=Path(__file__).resolve().parent
W=Path('C:/Users/Administrator/Documents/Codex/g80_20260928')
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
before=json.loads((O/'SOURCE_BEFORE.json').read_text(encoding='utf-8'))
assert before=={p:identity((W/p).read_bytes()) for p in before}
assert not subprocess.check_output(['git','-C',str(W),'status','--porcelain=v1','-uall']).strip()
assert subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD']).decode().strip()=='9a26dd5f31ca6fae45d5a55f5c59e33408371984'
files={p.relative_to(O).as_posix():p.read_bytes() for p in sorted(O.rglob('*')) if p.is_file() and p.name not in {'MANIFEST.json','DELIVERY_RECEIPT.json'} and p.suffix!='.zip'}
manifest={'scope':'Gate80 read-only static/data review; no execution or stage3 approval',
          'files':{n:identity(b) for n,b in files.items()}}
mb=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
(O/'MANIFEST.json').write_bytes(mb)
zp=O/'GATE80_REVIEW_20260928.zip'
with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED) as z:
    for n,b in files.items():z.writestr(n,b)
    z.writestr('MANIFEST.json',mb)
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None and len(z.namelist())==len(set(x.casefold() for x in z.namelist()))
    assert set(z.namelist())==set(files)|{'MANIFEST.json'}
    assert z.read('MANIFEST.json')==mb
    for n,b in files.items():assert z.read(n)==b
r={'scope':'Reviewer package generation; recipient remains null','recipient':None,
   'zip':zp.name,**identity(zp.read_bytes()),'manifest_sha256':identity(mb)['sha256'],
   'payload_count':len(files),'exact_set_size_SHA_CRC_verified':True,'selected_source_files_unchanged':len(before),
   'decision':'G79-N1 accepted; stage2 closed in limited scope','execution_GO':False,'stage3_start_approved':False}
(O/'DELIVERY_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(r,ensure_ascii=False))
