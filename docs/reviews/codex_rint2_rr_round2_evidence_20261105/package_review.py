import pathlib,hashlib,zipfile,json
r=pathlib.Path(__file__).resolve().parent
selected=[p for p in r.iterdir() if p.is_file() and p.name not in ('EVIDENCE_MANIFEST.sha256','delivery.json')]
selected.extend(p for p in (r/'received').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.pyo'))
for d in ('graph_review','runtime_review','root_review','science_review'):
    selected.extend(p for p in (r/d).iterdir() if p.is_file())
selected=sorted(set(selected),key=lambda p:p.relative_to(r).as_posix())
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(r).as_posix()+'\n' for p in selected)
mp=r/'EVIDENCE_MANIFEST.sha256';mp.write_text(manifest,encoding='utf-8',newline='\n')
zp=r.parent/'codex_rint2_rr_round2_review_evidence_20261105.zip'
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for p in selected+[mp]:
        z.write(p,p.relative_to(r).as_posix())
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    for line in manifest.splitlines():
        h,n=line.split('  ',1)
        assert hashlib.sha256(z.read(n)).hexdigest()==h,n
out={'zip':str(zp),'sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'bytes':zp.stat().st_size,'files':len(selected)+1,'report':str(r/'codex_review_rint2_rr_round2_20261105.md')}
(r/'delivery.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
