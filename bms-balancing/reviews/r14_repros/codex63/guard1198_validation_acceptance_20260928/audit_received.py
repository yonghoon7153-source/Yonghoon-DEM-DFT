"""Reviewer archive/data audit only; no received modules are imported or executed."""
import hashlib, json, stat, zipfile, io, difflib
from pathlib import Path, PurePosixPath

O=Path(__file__).resolve().parent
Z=Path('C:/Users/Administrator/Downloads/COMSOL63_GUARD1198_LIMITED_VALIDATION_PASS_20260928.zip')
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v): (O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def verify(z):
    ns=z.namelist(); assert len(ns)==len(set(x.casefold() for x in ns))
    for e in z.infolist():
        p=PurePosixPath(e.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in e.filename and ':' not in e.filename
        assert not stat.S_ISLNK(e.external_attr>>16)
    assert z.testzip() is None
    mraw=z.read('PACKAGE_MANIFEST.json');m=json.loads(mraw); fs=m['files']
    assert len(fs)==len({r['file'] for r in fs})
    assert set(ns)=={r['file'] for r in fs}|{'PACKAGE_MANIFEST.json'}
    for r in fs: assert ident(z.read(r['file']))=={k:r[k] for k in ('bytes','sha256')},r['file']
    return {'payload_count':len(fs),'entries':len(ns),'manifest':ident(mraw),'set_size_sha_crc_case_path_link':True}

b=Z.read_bytes()
with zipfile.ZipFile(Z) as z:
    audit={'package':{'path':str(Z),**ident(b)},**verify(z)}
    R=O/'received'
    if R.exists():
        for n in z.namelist(): assert (R/n).read_bytes()==z.read(n),n
    else:
        R.mkdir();z.extractall(R)
    history=z.read('history/COMSOL63_GUARD1198_LIMITED_TEST3_FAILURE_20260928.zip')
    with zipfile.ZipFile(io.BytesIO(history)) as h:
        audit['attempt03']={'zip':ident(history),**verify(h)}
        (O/'HISTORY_INVENTORY.txt').write_text('\n'.join(h.namelist())+'\n',encoding='utf-8')
        previous_harness=h.read('tests/run_python.py')
        assert ident(previous_harness)['sha256']==json.loads(z.read('CORRECTION.json'))['before_harness_sha256']
        audit['attempt03_to04_candidate_identical']=[]
        audit['candidate_without_attempt03_copy']=[]
        for n in z.namelist():
            if n.startswith('candidate/'):
                hn=n.replace('candidate/src/','candidate/')
                if hn in h.namelist():
                    assert z.read(n)==h.read(hn),n
                    audit['attempt03_to04_candidate_identical'].append(n)
                else: audit['candidate_without_attempt03_copy'].append(n)
        (O/'ACTUAL_HARNESS_DIFF.txt').write_text(''.join(difflib.unified_diff(previous_harness.decode('utf-8-sig').splitlines(True),z.read('tests/run_python.py').decode('utf-8-sig').splitlines(True),fromfile='attempt03',tofile='attempt04')),encoding='utf-8')
    old=O.parent/'guard1198_review_20260928'/'received'
    diff=[]
    for n in ['src/trigger_consumer.py','src/candidate_entry.py','PARENT_COMMAND.ps1','CONTRACT.json']:
        diff.extend(difflib.unified_diff((old/n).read_text(encoding='utf-8-sig').splitlines(True),z.read('candidate/'+n).decode('utf-8-sig').splitlines(True),fromfile='original/'+n,tofile='R1/'+n))
    (O/'CANDIDATE_FROM_PREPARATION.diff').write_text(''.join(diff),encoding='utf-8')
    audit['candidate_java_unchanged_from_preparation']=z.read('candidate/src/Guard1198Candidate.java')==(old/'src/Guard1198Candidate.java').read_bytes()
    assert audit['candidate_java_unchanged_from_preparation']
    audit['source_zip_unchanged']=Z.read_bytes()==b
    audit['subject_imports_executions']=0
    write('PACKAGE_AUDIT.json',audit)
    print(json.dumps(audit,ensure_ascii=False))
