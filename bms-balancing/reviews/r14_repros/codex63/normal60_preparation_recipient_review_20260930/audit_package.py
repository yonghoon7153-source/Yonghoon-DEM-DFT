"""Recipient ZIP integrity and inert extraction; never import received code."""
import hashlib,json,stat,zipfile
from pathlib import Path,PurePosixPath
root=Path(__file__).resolve().parent
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
reports=[]
for name,folder,mname in [
 ('COMSOL63_NORMAL60_OFFLINE_PREPARATION_20260930.zip','received','PACKAGE_MANIFEST.json'),
 ('NORMAL60_PREPARATION_DELIVERY_SUPPLEMENT_20260930.zip','supplement','MANIFEST.json')]:
    src=Path('C:/Users/Administrator/Downloads')/name
    before=sha(src); dest=root/folder
    assert not dest.exists()
    with zipfile.ZipFile(src) as z:
        names=z.namelist()
        assert len(names)==len(set(names))==len(set(n.casefold() for n in names))
        assert sum(x.file_size for x in z.infolist())<128*1024**2
        raw=z.read(mname); rows=json.loads(raw)['files']; refs={x['file']:x for x in rows}
        assert len(refs)==len(rows) and set(names)==set(refs)|{mname}
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            assert not p.is_absolute() and ':' not in info.filename and '\\' not in info.filename
            assert all(s not in ('','.','..') and s==s.rstrip(' .') for s in info.filename.split('/'))
            assert not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16) and not info.flag_bits&1
            b=z.read(info)
            if info.filename in refs:
                ref=refs[info.filename]
                assert len(b)==ref['bytes'] and hashlib.sha256(b).hexdigest()==ref['sha256'], info.filename
        dest.mkdir()
        for info in z.infolist():
            p=dest.joinpath(*PurePosixPath(info.filename).parts);p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f:f.write(z.read(info))
    assert sha(src)==before
    reports.append({'file':name,'bytes':src.stat().st_size,'sha256':before,'payloads':len(rows),
        'entries':len(names),'manifest':mname,'manifest_sha256':hashlib.sha256(raw).hexdigest(),
        'exact_set_size_sha_crc_paths_case_link':'PASS','original_zip_unchanged':True})
(root/'ARCHIVE_AUDIT.json').write_text(json.dumps(reports,indent=2)+'\n',encoding='utf-8')
print(json.dumps(reports,indent=2))
