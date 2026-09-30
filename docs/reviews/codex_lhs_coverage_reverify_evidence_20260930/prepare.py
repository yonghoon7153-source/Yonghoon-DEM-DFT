"""Read-only production review: prepare a disposable copy of the previous candidate."""
from pathlib import Path
import hashlib, json, shutil, subprocess, re
R=Path(__file__).resolve().parent; W=R.parent
OLD=W/'lhs_coverage_review_20260930/candidate'; C=R/'candidate'
bundle=R/'submitted/codex_lhs_coverage_reverify_request_20260930'
old_manifest=json.loads((W/'lhs_coverage_evidence_20260930/source_manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for item in old_manifest['candidate_targets']:
    assert sha(OLD/item['path'])==item['sha256'],item['path']
checks={line.split(maxsplit=1)[1].lstrip('*'):line.split()[0] for line in (bundle/'SHA256SUMS').read_text().splitlines() if line.strip()}
patches=sorted((bundle/'patches').glob('*.patch'))
assert len(patches)==11
records=[]
for i,p in enumerate(patches):
    expected=checks.get(p.name,checks.get('patches/'+p.name))
    assert sha(p)==expected,(p.name,sha(p),expected)
    rec=dict(name=p.name,sha256=sha(p))
    if i<7:
        oldp=OLD/'docs/reviews/codex_lhs_coverage_request_20260930/patches'/p.name
        assert p.read_bytes().split(b'diff --git ',1)[1]==oldp.read_bytes().split(b'diff --git ',1)[1],p.name
        rec.update(first_review_sha256=sha(oldp),byte_identical=sha(p)==sha(oldp),diff_body_identical=True)
    records.append(rec)
assert not C.exists(),'Use a fresh destination; do not overwrite a review snapshot'
shutil.copytree(OLD,C,ignore=shutil.ignore_patterns('.git','__pycache__'))
for p in patches[7:]:
    for args in [['git','apply','--check',str(p)],['git','apply',str(p)]]:
        proc=subprocess.run(args,cwd=C,capture_output=True,text=True)
        assert proc.returncode==0,proc.stderr
targets=sorted({f for p in patches for f in re.findall(r'^diff --git a/(.*?) b/',p.read_text(encoding='utf-8'),re.M)})
manifest=dict(snapshot='ac484ba5cda082caffe2c3c408de86cbd760befc',base='da4670594',
              prior_snapshot=old_manifest['snapshot'],patches=records,
              candidate_targets=[dict(path=f,sha256=sha(C/f)) for f in targets])
(R/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
