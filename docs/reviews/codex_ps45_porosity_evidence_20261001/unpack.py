import pathlib,zipfile,tarfile,hashlib,json
R=pathlib.Path(__file__).resolve().parent
zpath=pathlib.Path('C:/Users/Administrator/Downloads/codex_ps45_porosity_request_20261001.zip')
dst=R/'inputs';dst.mkdir(exist_ok=True)
def target(root,name):
    if '\\' in name or ':' in name:raise ValueError(name)
    p=(root/name).resolve()
    if not p.is_relative_to(root.resolve()):raise ValueError(name)
    return p
with zipfile.ZipFile(zpath) as z:
    for i in z.infolist():
        if (i.external_attr>>16)&0o170000==0o120000:raise ValueError('symlink')
        p=target(dst,i.filename)
        if i.is_dir():p.mkdir(parents=True,exist_ok=True)
        else:
            p.parent.mkdir(parents=True,exist_ok=True)
            if p.exists() and p.read_bytes()!=z.read(i):raise ValueError('overwrite '+str(p))
            p.write_bytes(z.read(i))
bundle=dst/'codex_ps45_porosity_request_20261001'
inventory=[]
for archive in bundle.glob('*.tar.gz'):
    root=dst/archive.name.removesuffix('.tar.gz');root.mkdir(exist_ok=True)
    with tarfile.open(archive) as t:
        for m in t.getmembers():
            if not(m.isdir() or m.isfile()):raise ValueError('non-file member '+m.name)
            p=target(root,m.name)
            if m.isdir():p.mkdir(parents=True,exist_ok=True)
            else:
                p.parent.mkdir(parents=True,exist_ok=True);b=t.extractfile(m).read()
                if p.exists() and p.read_bytes()!=b:raise ValueError('overwrite '+str(p))
                p.write_bytes(b)
for p in sorted(dst.rglob('*')):
    if p.is_file():inventory.append(dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(R/'input_manifest.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(inventory,ensure_ascii=False,indent=2))
