"""Independent archive verification/extraction. Never imports supplied source."""
import hashlib, json, stat, zipfile, re
from pathlib import Path, PurePosixPath

O = Path(__file__).resolve().parent
Z = Path('C:/Users/Administrator/Downloads/COMSOL63_GUARD1198_NATIVE_RESULT_FOR_REVIEW_20260928.zip')
def ident(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def dump(n, v): (O/n).write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
raw = Z.read_bytes()
with zipfile.ZipFile(Z) as z:
    ns = z.namelist()
    assert len(ns) == len(set(n.casefold() for n in ns))
    for e in z.infolist():
        p = PurePosixPath(e.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in e.filename and ':' not in e.filename
        assert not stat.S_ISLNK(e.external_attr >> 16)
    mraw = z.read('PACKAGE_MANIFEST.json'); m = json.loads(mraw)['files']
    assert len(m) == len({x['file'] for x in m})
    assert set(ns) == {x['file'] for x in m} | {'PACKAGE_MANIFEST.json'}
    for x in m:
        assert ident(z.read(x['file'])) == {k:x[k] for k in ('bytes','sha256')}, x['file']
    assert z.testzip() is None
    R = O/'received'
    if R.exists():
        for n in ns: assert (R/n).read_bytes() == z.read(n), n
    else:
        R.mkdir(); z.extractall(R)
    prior = O.parent/'guard1198_validation_review_20260928'/'received'/'candidate'
    pins=[]
    for n in ns:
        if n.startswith('candidate/'):
            p=prior/n.removeprefix('candidate/')
            if p.exists():
                assert p.read_bytes()==z.read(n), n
                pins.append(n)
    assert (R/'run/Guard1198Candidate.java').read_bytes()==(R/'candidate/src/Guard1198Candidate.java').read_bytes()
    audit={'source':{'path':str(Z), **ident(raw)},'entries':len(ns),'payload':len(m),'uncompressed_bytes':sum(x.file_size for x in z.infolist()),'manifest':ident(mraw),'exact_set_size_sha_crc_path_case_link':True,'prior_candidate_exact_matches':pins,'run_java_equals_candidate':True,'source_unchanged':ident(Z.read_bytes())==ident(raw),'received_code_executions':0}
    dump('PACKAGE_AUDIT.json',audit)
    dump('SOURCE_BEFORE.json', {'input_zip':ident(raw),'extracted':m})
    print(json.dumps(audit,ensure_ascii=False))
    print('KEY_FILES', '\n'.join(n for n in ns if not re.search(r'_event_\d+\.json$',n) and not n.startswith('external/')))
