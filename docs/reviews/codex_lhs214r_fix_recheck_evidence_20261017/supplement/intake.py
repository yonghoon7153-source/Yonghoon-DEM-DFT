"""Safely unpack supplied evidence; no Git or production writes."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,stat,zipfile
R=Path(__file__).resolve().parent
Z=Path('C:/Users/Administrator/Downloads/lhs214r_recheck_a4a1e52c0.zip')
O=R/'submitted'
O.mkdir(exist_ok=True)
def lp(p):return Path('\\\\?\\'+str(p.resolve())) if os.name=='nt' else p
rows=[]
with zipfile.ZipFile(Z) as z:
    assert z.testzip() is None
    seen=set()
    for info in z.infolist():
        p=PurePosixPath(info.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and ':' not in info.filename
        assert info.filename.casefold() not in seen;seen.add(info.filename.casefold())
        assert not stat.S_ISLNK(info.external_attr>>16)
        dest=O.joinpath(*p.parts)
        if info.is_dir():lp(dest).mkdir(parents=True,exist_ok=True);continue
        b=z.read(info);lp(dest.parent).mkdir(parents=True,exist_ok=True)
        assert not lp(dest).exists()
        lp(dest).write_bytes(b)
        rows.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
E=O/'lhs214r_recheck_a4a1e52c0/docs/reviews/lhs214r_fix_evidence_20261016'
sharows=[]
for line in (E/'SHA256SUMS').read_text(encoding='utf8').splitlines():
    want,name=line.split(maxsplit=1);name=name.lstrip('*')
    assert not Path(name).is_absolute() and '..' not in Path(name).parts
    b=lp(E/name).read_bytes();got=hashlib.sha256(b).hexdigest()
    sharows.append({'path':name,'ok':got==want,'sha256':got})
prev=R.parent/'lhs214r_fix_recheck_20261017'
request=O/'lhs214r_recheck_a4a1e52c0/docs/reviews/codex_lhs214r_fix_recheck_request_20261016.md'
old=prev/'submitted/codex_lhs214r_fix_recheck_request_20261016.md'
oldtree=json.loads((prev/'evidence/tree_60ba39e22.json').read_text(encoding='utf8'))
newtree=json.loads((R/'evidence/remote_root_tree.json').read_text(encoding='utf8'))
treechecks={p:{'old':next(x['sha'] for x in oldtree['tree'] if x['path']==p),'new':next(x['sha'] for x in newtree['tree'] if x['path']==p)} for p in ['scripts','webapp','AGENTS.md']}
for v in treechecks.values():v['identical']=v['old']==v['new']
out={'zip':{'path':str(Z),'bytes':Z.stat().st_size,'sha256':hashlib.sha256(Z.read_bytes()).hexdigest()},'files':rows,'sha256sums':sharows,'sha256sums_all_ok':all(x['ok'] for x in sharows),'request_previous_byte_identical':request.read_bytes()==old.read_bytes(),'tree_identity':treechecks}
(R/'evidence/intake.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k not in ('files','sha256sums')},ensure_ascii=False,indent=2));print('files',len(rows),'sha256sums',len(sharows))
