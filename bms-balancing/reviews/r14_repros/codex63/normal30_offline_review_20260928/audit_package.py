"""Reviewer-owned byte/JSON archive audit. Never imports received modules."""
import hashlib, json, pathlib, stat, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
SRC=pathlib.Path('C:/Users/Administrator/Downloads/COMSOL63_NORMAL30_OFFLINE_PREPARATION_20260928.zip')
def sha(b): return hashlib.sha256(b).hexdigest()
raw=SRC.read_bytes()
out={'source':str(SRC),'bytes':len(raw),'sha256':sha(raw),'errors':[]}
with zipfile.ZipFile(SRC) as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    for i in z.infolist():
        p=pathlib.PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename
        assert not stat.S_ISLNK(i.external_attr >> 16)
    assert z.testzip() is None
    m=json.loads(z.read('PACKAGE_MANIFEST.json'))
    assert set(names)=={'PACKAGE_MANIFEST.json'}|{r['file'] for r in m['files']}
    for r in m['files']:
        b=z.read(r['file']); assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['file']
    out.update(payload_count=len(m['files']),manifest_sha256=sha(z.read('PACKAGE_MANIFEST.json')),code_manifest_sha256=sha(z.read('CODE_MANIFEST.json')))
    assert out['code_manifest_sha256']==m['code_manifest_sha256']=='28dd6da5cc76885263c17b2671548a00692064807e02e77ceb6f3edbdd946fa5'
    for pre in ('','basis/'):
        cm=json.loads(z.read(pre+'CODE_MANIFEST.json'))
        for r in cm['files']:
            p=pre+r['file']
            if p not in names:
                out.setdefault('basis_manifest_members_not_included',[]).append(p);continue
            b=z.read(p);assert sha(b)==r['sha256'] and len(b)==r['bytes'],p
    dst=ROOT/'received'; assert not dst.exists(),'extraction target exists'
    for n in names:
        p=dst/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
out['checks']=['exact_set','size','sha256','CRC','unique_case_paths','no_path_escape_or_symlinks','candidate_code_manifest']
(ROOT/'PACKAGE_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
