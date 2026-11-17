"""Verify the supplied archive and extracted review bytes; no solver or host access."""
from pathlib import Path, PurePosixPath
import argparse, csv, hashlib, io, json, stat, zipfile

ROOT=Path(__file__).resolve().parent
EXPECTED='7da8e749ed0954d5777bffd0d16f86ce490e2b15ed371077f3174a88e1503f88'
PIN='f40d005acce19b6c363e5c10c8668ec081b56f2e'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--zip');ap.add_argument('--input',default=str(ROOT/'input'));a=ap.parse_args()
    base=Path(a.input).resolve()
    rows=list(csv.DictReader(io.StringIO((base/'ZIP_MANIFEST.tsv').read_text(encoding='utf-8')),delimiter='\t'))
    checks=[]
    for row in rows:
        name=row['path'];parts=PurePosixPath(name)
        assert not parts.is_absolute() and '..' not in parts.parts and '\\' not in name,name
        p=base.joinpath(*parts.parts);assert p.resolve().is_relative_to(base),name
        data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert len(data)==int(row['bytes']) and hashlib.sha256(data).hexdigest()==row['sha256'],name
        if row['git_blob'] not in ('','-'):assert blob==row['git_blob'],name
        checks.append(name)
    all_files={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()}
    assert all_files-set(checks)=={'PIN.txt','ZIP_MANIFEST.tsv'}
    assert PIN in (base/'PIN.txt').read_text(encoding='utf-8')
    out={'pin':PIN,'manifest_rows':len(rows),'files':len(all_files),'input_bytes':'PASS'}
    if a.zip:
        zpath=Path(a.zip);assert hashlib.sha256(zpath.read_bytes()).hexdigest()==EXPECTED
        with zipfile.ZipFile(zpath) as z:
            assert z.testzip() is None
            names=[i.filename for i in z.infolist() if not i.is_dir()]
            assert len(names)==len(set(names)) and set(names)==all_files
            for info in z.infolist():
                pp=PurePosixPath(info.filename)
                assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in info.filename
                assert not stat.S_ISLNK(info.external_attr>>16)
                if not info.is_dir():assert z.read(info)==base.joinpath(*pp.parts).read_bytes(),info.filename
        out.update(zip_sha256=EXPECTED,crc='PASS',original_vs_extracted='ALL_BYTES_SAME')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
