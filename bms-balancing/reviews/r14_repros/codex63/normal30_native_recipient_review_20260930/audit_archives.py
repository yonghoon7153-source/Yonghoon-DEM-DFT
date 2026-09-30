"""Recipient-owned evidence extraction. Received scripts are never run."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile
R=Path(__file__).resolve().parent
def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
reports=[]
for name,folder in [('COMSOL63_NORMAL30_NATIVE_RESULT_20260930.zip','received'),('NORMAL30_DELIVERY_SUPPLEMENT_20260930.zip','supplement')]:
    src=Path('C:/Users/Administrator/Downloads')/name
    pre=digest(src);out=R/folder;assert not out.exists();out.mkdir()
    with zipfile.ZipFile(src) as z:
        names=z.namelist();assert len(names)==len(set(names))==len(set(n.casefold() for n in names))
        total=sum(e.file_size for e in z.infolist());assert total<1024**3
        mraw=z.read('MANIFEST.json');m=json.loads(mraw);rows=m['files']
        assert len(rows)==len({x['file'] for x in rows})
        assert set(names)=={x['file'] for x in rows}|{'MANIFEST.json'}
        expected={x['file']:x for x in rows}
        for e in z.infolist():
            p=PurePosixPath(e.filename)
            assert not p.is_absolute() and not any(x in ('.','..','') for x in p.parts)
            assert ':' not in e.filename and '\\' not in e.filename and not e.is_dir() and not (e.flag_bits&1)
            assert not stat.S_ISLNK(e.external_attr>>16)
            target=out.joinpath(*p.parts);target.parent.mkdir(parents=True,exist_ok=True)
            h=hashlib.sha256();n=0
            with z.open(e) as a,target.open('xb') as b:
                while chunk:=a.read(1024*1024):b.write(chunk);h.update(chunk);n+=len(chunk)
            if e.filename!='MANIFEST.json':
                row=expected[e.filename];assert n==row['bytes'] and h.hexdigest()==row['sha256'],e.filename
        # Reading every entry to EOF above also enforces each ZIP CRC.
    assert pre==digest(src)
    reports.append(dict(file=name,bytes=src.stat().st_size,sha256=pre,payloads=len(rows),entries=len(names),uncompressed_bytes=total,
        manifest_sha256=hashlib.sha256(mraw).hexdigest(),size_sha_crc_exact_set_path_case_link=True,input_unchanged=True))
(R/'ARCHIVE_AUDIT.json').write_text(json.dumps(reports,indent=2)+'\n',encoding='utf-8')
print(json.dumps(reports,indent=2))
