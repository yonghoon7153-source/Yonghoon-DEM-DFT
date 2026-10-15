"""Package review evidence with source-integrity checks and member hashes."""
from pathlib import Path
import ast,hashlib,json,zipfile,os
R=Path(__file__).resolve().parent
O=R.parent/'rint_g2_impl_review_20261014'
def long(p):return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
def digest(b):return hashlib.sha256(b).hexdigest()
src=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
for x in src['files']:
    b=long(R/'source'/x['path']).read_bytes()
    assert digest(b)==x['sha256'],x['path']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob'],x['path']
for p in (R/'probes').glob('*.py'):ast.parse(p.read_text(encoding='utf8'))
for p in R.glob('*.py'):ast.parse(p.read_text(encoding='utf8'))
baseline=json.loads((R/'evidence/baseline_tests.json').read_text(encoding='utf8'))
assert len(baseline)==9 and all(x['rc']==0 for x in baseline)
for f in ('off_compatibility.json','off_before_fix.json'):
    rows=json.loads((R/'evidence'/f).read_text(encoding='utf8'))['cases']
    assert len(rows)==16 and all(x['all_keys_values_array_bytes_equal'] for x in rows)
entries=[]
for directory in ('source','source_prior','probes','notes','support','evidence'):
    for p in (R/directory).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:entries.append(p)
entries += [p for p in R.iterdir() if p.is_file() and p.suffix in ('.py','.md','.json')]
entries += list((O/'probes').glob('*.py')) + list((O/'source/scripts').glob('*.py'))
entries += [O/'codex_review_rint_g2_impl_20261014.md',O/'source_manifest.json']
entries=sorted(set(entries))
manifest=[]
out=R.parent/'codex_rint_g2_impl_fix_recheck_20261015.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in entries:
        b=long(p).read_bytes();name=p.relative_to(R.parent).as_posix()
        z.writestr(name,b);manifest.append({'path':name,'bytes':len(b),'sha256':digest(b)})
    z.writestr('PACKAGE_MANIFEST.json',json.dumps({'pin':src['pin'],'files':manifest},ensure_ascii=False,indent=2).encode('utf8'))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    for x in manifest:assert digest(z.read(x['path']))==x['sha256'],x['path']
summary={'zip':str(out),'bytes':out.stat().st_size,'sha256':digest(out.read_bytes()),
         'members':len(manifest)+1,'source_files_verified':len(src['files']),
         'total_uncompressed_bytes':sum(x['bytes'] for x in manifest)}
(R.parent/'codex_rint_g2_impl_fix_recheck_20261015_package_receipt.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
