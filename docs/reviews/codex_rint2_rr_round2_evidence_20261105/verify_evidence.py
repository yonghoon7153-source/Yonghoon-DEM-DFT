import pathlib,hashlib,sys
r=pathlib.Path(__file__).resolve().parent
lines=(r/'EVIDENCE_MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
bad=[]
for line in lines:
    h,n=line.split('  ',1)
    p=r/n
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:bad.append(n)
print({'files':len(lines),'mismatches':bad})
sys.exit(bool(bad))
