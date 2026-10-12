"""Package review artifacts; never modify pinned source or original repository."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,shutil,sys,zipfile
R=Path(__file__).resolve().parent
def xp(p):return Path('\\\\?\\'+str(p.resolve())) if os.name=='nt' else p
def h(b):return hashlib.sha256(b).hexdigest()
old=R.parent/'gen2_network_reverify6_20261011'
c=json.loads((R/'evidence/r7_contract.json').read_text(encoding='utf8'))
paths=set(c['sealed32']['hashes'])|set(c['handover'])
for rel in paths:
    src=old/'source'/rel;dst=R/'baseline_r6/source'/rel
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(xp(src),xp(dst))
for src in (old/'evidence').glob('r6_s0b_*.input.json'):
    dst=R/'baseline_r6/evidence'/src.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
shutil.copyfile(old/'source_manifest.json',R/'baseline_r6/source_manifest.json')
entries={}
for base,dirs,files in os.walk(xp(R)):
    dirs[:]=[d for d in dirs if d not in ('tmp','__pycache__','.git')]
    for name in files:
        p=Path(base)/name;rel=p.relative_to(xp(R)).as_posix()
        if name in ('MANIFEST.sha256.json','bundle_receipt.json') or name.endswith(('.pyc','.zip')):continue
        entries[rel]=p
manifest={k:{'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for k,p in sorted(entries.items())}
mf=R/'MANIFEST.sha256.json';mf.write_text(json.dumps({'review_pin':c['pin'],'files':manifest},ensure_ascii=False,indent=2),encoding='utf8')
entries[mf.name]=mf
out=R.parent/'codex_gen2_network_reverify7_20261012.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for rel,p in sorted(entries.items()):z.write(p,arcname=R.name+'/'+rel)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    names=z.namelist();assert len(set(names))==len(names)
    assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
    for rel,row in manifest.items():
        data=z.read(R.name+'/'+rel);assert len(data)==row['bytes'] and h(data)==row['sha256'],rel
receipt={'zip':str(out),'bytes':out.stat().st_size,'sha256':h(out.read_bytes()),'entries':len(entries),
         'manifest_files':len(manifest),'manifest_sha256':h(mf.read_bytes()),'all_payload_hashes_match':True,'hazards':[]}
(R/'bundle_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False))
