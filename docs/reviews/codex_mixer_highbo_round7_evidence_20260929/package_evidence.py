"""Package only this review's fixed evidence list and verify archived bytes."""
from pathlib import Path
import hashlib
import json
import zipfile

root=Path(__file__).resolve().parent
names=[
    'README.md','SOURCES.md','review.md','attachment_original.txt',
    'prereg_submitted.txt','audit_prereg.py','audit_results.json',
    'baseline/make_mixer_deck.py','baseline/measure_mixing_index.py',
    'baseline/prior_r6_verdict.md','package_evidence.py',
]
def sha(b):
    return hashlib.sha256(b).hexdigest()
assert sha((root/'attachment_original.txt').read_bytes())=='011f7ea89cd4686832e35f054db85daa42bad2e6b7420010dbe475925ad1030b'
assert sha((root/'prereg_submitted.txt').read_bytes())=='79255022bef5a87092073a24c45519d15b7294502428d88e8f6dee345417e860'
rows=[dict(path=n,bytes=(root/n).stat().st_size,sha256=sha((root/n).read_bytes())) for n in names]
manifest=dict(schema='review_evidence/v1',review='LH round7 prereg 2026-09-29',
              scope='arithmetic and design review; no simulations or external mutations',files=rows)
(root/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out=root.parent/'codex_mixer_highbo_round7_prereg_20260929.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for n in names+['MANIFEST.json']:
        z.write(root/n,n)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(names)+1
    assert all(sha(z.read(r['path']))==r['sha256'] for r in rows)
print(json.dumps(dict(zip=str(out),bytes=out.stat().st_size,sha256=sha(out.read_bytes()),
    entries=len(names)+1,verified_files=len(rows),crc='PASS'),ensure_ascii=False))
