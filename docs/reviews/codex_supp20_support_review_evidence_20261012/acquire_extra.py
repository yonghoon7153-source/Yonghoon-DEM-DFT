from pathlib import Path
import ast,sys,json,hashlib,urllib.request,urllib.parse
R=Path(__file__).resolve().parent; S=R/'source'
m=json.loads((R/'source_manifest.json').read_text(encoding='utf8'));pin=m['pin']
entries={e['path']:e for e in json.loads((R/'tree.json').read_text(encoding='utf8'))['tree'] if e['type']=='blob'}
def add(p):
    e=entries[p]; dst=S/p
    if dst.exists():return
    u='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+pin+'/'+urllib.parse.quote(p)
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Codex-read-only-review'}),timeout=60) as f:b=f.read()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha']
    dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    m['files'].append(dict(path=p,sha=e['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=False));print(p,flush=True)
for p in sys.argv[1:]:
    if p.endswith('/'):
        for key in sorted(entries):
            if key.startswith(p):add(key)
    else:add(p)
for iteration in range(8):
    missing=set()
    for src in (S/'scripts').glob('*.py'):
        try:tree=ast.parse(src.read_text(encoding='utf8'))
        except (SyntaxError,UnicodeError):continue
        for n in ast.walk(tree):
            names=[x.name for x in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) and n.module else []
            for name in names:
                p='scripts/'+name.replace('.','/')+'.py'
                if p in entries and not (S/p).exists():missing.add(p)
    if not missing:break
    for p in sorted(missing):add(p)
(R/'source_manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
