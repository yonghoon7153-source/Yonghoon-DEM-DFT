from pathlib import Path,PurePosixPath
import zipfile,hashlib,json,stat,os
R=Path('t12r_recheck_20261026').resolve();S=Path('\\\\?\\'+str(R/'snapshot'));S.mkdir(exist_ok=False)
p=Path('C:/Users/Administrator/Downloads/codex-dem-gen2-t12r-96f15ed17e03.zip');bad=[]
with zipfile.ZipFile(p) as z:
 names=z.namelist();assert len(names)==len(set(n.casefold() for n in names))
 for info in z.infolist():
  n=info.filename;pp=PurePosixPath(n);assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in n and ':' not in n and not stat.S_ISLNK(info.external_attr>>16)
  dest=S/Path(*pp.parts);dest.parent.mkdir(parents=True,exist_ok=True)
  if not info.is_dir():dest.write_bytes(z.read(n))
 src=json.loads((S/'SOURCES.json').read_text(encoding='utf8'));print('SOURCE_METADATA_SAMPLE',str(next(iter(src.items())))[:500])
 for name,m in src.items():
  b=(S/name).read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  if hashlib.sha256(b).hexdigest()!=m['sha256'] or len(b)!=m['bytes'] or oid!=m['oid']:bad.append(name)
 manbad=[];manifest=(S/'MANIFEST.sha256').read_text(encoding='utf8').splitlines()
 for l in manifest:
  h,n=l.split('  ',1)
  if hashlib.sha256((S/n).read_bytes()).hexdigest()!=h:manbad.append(n)
 out={'zip':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'entries':len(names),'source_blobs':len(src),'source_mismatch':bad,'manifest_entries':len(manifest),'manifest_mismatch':manbad}
 (R/'evidence/intake.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(out);assert not bad and not manbad

