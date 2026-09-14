"""Read-only R14 follow-up document and historical-byte audit."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
root=Path(sys.argv[1]);repo=root.parent
old='1bb45b358db4850c73e185d5f851e35fbcff9ad6'
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args])
def sha(b):return hashlib.sha256(b).hexdigest()
head=git('rev-parse','HEAD').decode().strip()
req=root/'reviews/R14_REQUEST.md'; rb=req.read_bytes()
attached=Path(sys.argv[2]).read_bytes()
old_req=subprocess.run(['git','-C',str(repo),'show',old+':bms-balancing/reviews/R14_REQUEST.md'],capture_output=True)
print('REQUEST',json.dumps({'head':head,'bytes':len(rb),'sha256':sha(rb),'matches_original_attachment':rb==attached,'was_present_in_target_commit':old_req.returncode==0,'matches_old_commit_blob':rb==old_req.stdout if old_req.returncode==0 else None}))
print('TARGET_OLD_TREE',git('rev-parse',old+'^{tree}').decode().strip())
print('OUT_TREE',json.dumps({'old':git('rev-parse',old+':bms-balancing/out').decode().strip(),'current':git('rev-parse','HEAD:bms-balancing/out').decode().strip(),'committed_diff':git('diff','--name-only',old,'HEAD','--','bms-balancing/out').decode().splitlines(),'working_copy_diff':git('diff','--name-only','HEAD','--','bms-balancing/out').decode().splitlines()}))
paths=[p for p in (root/'out').glob('*.meta.json')]
checkpaths=[]
for p in paths:
    checkpaths.extend([p,p.with_name(p.name[:-10])])
checkpaths.extend(p for p in (root/'out/archive/legacy_r6_u14').iterdir() if p.is_file())
bad=[]
for p in checkpaths:
    oldb=git('show',old+':bms-balancing/'+p.relative_to(root).as_posix())
    if p.read_bytes()!=oldb:bad.append(p.relative_to(root).as_posix())
print('ACTUAL_ARTIFACT_BYTES',json.dumps({'checked':len(checkpaths),'different':bad}))
pkg=root/'reviews/r14_repros/codex/HARNESS_R14_1BB45B35_REVIEW_PACKAGE.zip'
original=Path(sys.argv[3]); pb=pkg.read_bytes()
with zipfile.ZipFile(pkg) as z:
    manifest=json.loads(z.read('PACKAGE_MANIFEST.json')); fail=[]; extractedfail=[]
    for e in manifest['payloads']:
        b=z.read(e['path'])
        if len(b)!=e['bytes'] or sha(b)!=e['sha256']:fail.append(e['path'])
        local=root/'reviews/r14_repros/codex/pkg'/e['path']
        if not local.is_file() or local.read_bytes()!=b:extractedfail.append(e['path'])
    print('REVIEW_PACKAGE',json.dumps({'bytes':len(pb),'sha256':sha(pb),'matches_original_local_zip':pb==original.read_bytes(),'crc_bad':z.testzip(),'payload_count':len(manifest['payloads']),'manifest_failures':fail,'extracted_payload_mismatches':extractedfail}))
print('P2_3_BASE',git('rev-parse','37a889b^').decode().strip())
print('CORRECTED_CODE_DIFF',git('diff','--name-only','df6413d649ef51ace16d634c3856f857d598c79d',old,'--','*.py','*.sh').decode().splitlines())
print('OLD_WRONG_CODE_DIFF_COUNT',len(git('diff','--name-only','ef8e8f6',old,'--','*.py','*.sh').decode().splitlines()))
