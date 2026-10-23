"""Verify imported archive and three-mutation evidence; no tests or file edits.

python -I verify_addendum.py --repo REPO --out OUT [--original REVIEW_ROOT]
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--repo',required=True,type=Path)
ap.add_argument('--out',required=True,type=Path)
ap.add_argument('--original',type=Path)
a=ap.parse_args()
e=a.repo.resolve()/'docs/reviews/dem_unloading_ulpr_fix_evidence_20261023'
p=e/'independent/package'; out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
sha=lambda b: hashlib.sha256(b).hexdigest()
prov=json.loads((p/'archive-provenance.json').read_text())
result={'archive_sha256':sha((p/prov['archive']).read_bytes())}
result['archive_hash_matches']=result['archive_sha256']==prov['sha256']
expected_report='6c89262bb17b71e88d215fc001a7c11e498a6b757735eeedd6ba59555d270b8b'
snapshot=json.loads((p/'snapshot-sha256.json').read_text())
with zipfile.ZipFile(p/prov['archive']) as z:
    result['member_count']=len(z.namelist())
    result['archive_crc_ok']=z.testzip() is None
    result['archived_report_sha256']=sha(z.read('PACKAGE-REVIEW.original.md'))
    result['archived_report_matches_original']=result['archived_report_sha256']==expected_report
    result['snapshot_members']=[{'name':n,'hash_matches':sha(z.read('snapshot/'+n))==h} for n,h in snapshot.items() if n!='input-package.diff']
    result['diff_hash_matches']=sha((p/'input-package.diff').read_bytes())==snapshot['input-package.diff']
    if a.original:
        result['archive_bytes_match_original']={n:z.read(n)==(a.original/'PACKAGE-REVIEW.md' if n=='PACKAGE-REVIEW.original.md' else a.original/'package'/n).read_bytes() for n in z.namelist()}
        result['copied_package_bytes_match_original']={str(x.relative_to(p)):x.read_bytes()==(a.original/'package'/x.relative_to(p)).read_bytes() for x in p.rglob('*') if x.is_file() and x.name not in ['reviewed-snapshot.zip','archive-provenance.json'] and (a.original/'package'/x.relative_to(p)).is_file()}
    live=(e/'independent/PACKAGE-REVIEW.md').read_text()
    original=z.read('PACKAGE-REVIEW.original.md').decode()
    prefix=original.replace('`dump-final/SUMMARY.md`','`../dump-final/SUMMARY.md`')
    result['live_report_only_reference_fix_and_note']=live.startswith(prefix) and live[len(prefix):].strip().startswith('반입 메모:')
rows=json.loads((p/'authorization-mutations-final/results.json').read_text())
result['source_matches_current']=rows['source_sha256']==sha((a.repo/'docs/data/ps45_unload_20261009/ul_reader.py').read_bytes())
result['script_hash_matches']=rows['script_sha256']==sha((p/'authorization_mutations.py').read_bytes())
result['mutations']=[]
for r in rows['mutations']:
    log=(p/'authorization-mutations-final'/(r['name']+'.log')).read_text()
    result['mutations'].append({'name':r['name'],'rc':r['rc'],'R38':len(r['expected_failures']),'related_R28':len(r['related_existing_R28_failures']),'traceback':r['traceback'],'unexpected':r['unexpected_failures'],'raw_failures_match':[x.strip() for x in log.splitlines() if '✗' in x]==r['failures'],'mutant_hash_matches':sha((p/'authorization-mutations-final'/(r['name']+'.py')).read_bytes())==r['mutant_sha256']})
result['request_sha256']=sha((a.repo/'docs/reviews/codex_dem_unloading_ulpr_recheck_request_20261023.md').read_bytes())
result['evidence_readme_sha256']=sha((e/'README.md').read_bytes())
(out/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
