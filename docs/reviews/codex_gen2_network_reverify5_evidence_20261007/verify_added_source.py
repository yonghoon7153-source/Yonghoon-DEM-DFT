from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
p=R/'source/docs/data/case15_corner_20261001/input_case15.liggghts'
expect='72481a3f3fb4a1b6bb5af00f20efac58a9dd636b'
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
b=p.read_bytes();vs=[b,b[:-1],b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'),b[:-1].replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')]
ok=[x for x in vs if blob(x)==expect];assert ok,'Git blob mismatch';b=ok[0];p.write_bytes(b)
mp=R/'source_manifest.json';rows=json.loads(mp.read_text());rows=[x for x in rows if x['path']!=str(p.relative_to(R/'source').as_posix())]
rows.append(dict(path=p.relative_to(R/'source').as_posix(),ref='aa7ec7fe98e8684f1a2138665f9eba978366c229',sha=expect,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
mp.write_text(json.dumps(rows,indent=2),encoding='utf8');print('verified',expect,len(b),'bytes',len(rows),'files')
