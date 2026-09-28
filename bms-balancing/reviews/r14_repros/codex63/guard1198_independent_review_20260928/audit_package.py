"""Reviewer-owned archive/data audit. Never imports or executes received code."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile
O=Path(__file__).resolve().parent
Z=Path('C:/Users/Administrator/Downloads/COMSOL63_GUARD1198_OFFLINE_PREPARATION_20260928.zip')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
b=Z.read_bytes(); R=O/'received'; R.mkdir(exist_ok=False)
with zipfile.ZipFile(Z) as z:
    names=z.namelist();assert len(names)==len(set(n.casefold() for n in names))
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename
        assert not stat.S_ISLNK(i.external_attr>>16)
    raw=z.read('PACKAGE_MANIFEST.json'); m=json.loads(raw); fs={x['file']:x for x in m['files']}
    assert len(fs)==len(m['files']) and set(names)==set(fs)|{'PACKAGE_MANIFEST.json'}
    assert z.testzip() is None
    for name,v in fs.items():assert ident(z.read(name))=={k:v[k] for k in ('bytes','sha256')},name
    z.extractall(R)
prev=O.parent/'b020_longer_plan_review_20260928'
for n in ['NEXT_OFFLINE_DIRECTIVE_KO.md','REVIEW_KO.md','ROADMAP_KO.md']:
    assert (R/'received'/n).read_bytes()==(prev/n).read_bytes()
assert b==Z.read_bytes()
a={'zip':str(Z),**ident(b),'payload':len(fs),'manifest':ident(raw),
   'exact_set_size_SHA_CRC_path_case_link':True,'three_prior_reviewer_documents_byte_identical':True,
   'source_zip_unchanged':True,'subject_code_execution':0}
(O/'PACKAGE_AUDIT.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(a))
