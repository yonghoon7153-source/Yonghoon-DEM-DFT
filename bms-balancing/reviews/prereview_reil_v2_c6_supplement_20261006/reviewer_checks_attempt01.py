"""Reviewer-owned data/hash comparisons only; no supplied code import/evaluation."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
current = json.loads((root/'RECEIVED_SNAPSHOT.json').read_text(encoding='utf-8'))
prior_root = root.parent/'reil_annex_d_c6_review_20261006'
prior_tree = json.loads((prior_root/'TREE_SELECTION.json').read_text(encoding='utf-8'))
prior_snap = json.loads((prior_root/'RECEIVED_SNAPSHOT.json').read_text(encoding='utf-8'))
index = {x['path']:x for x in prior_tree['entries']}
checks = []
def check(name, ok, detail=None):
    checks.append({'id':name,'pass':bool(ok),'detail':detail})

prefix='bms-balancing/reil_c6_20261005/'
newset={x['path'] for x in current['seal_directory']}
oldset={p for p in index if p.startswith(prefix)}
check('seal_directory_exact_set_unchanged',newset==oldset,sorted(newset))
for row in current['seal_directory']:
    check('seal_blob_unchanged:'+row['path'],row['sha']==index[row['path']]['sha'] and row['size']==index[row['path']]['size'])

for rec in current['records']:
    if rec['lines'] is None:
        raw=rec['content'].encode('utf-8')
        got=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        check('full_text_git_blob:'+rec['path'],got==rec['sha'])
    else:
        # Returned sha is whole-file GitHub metadata, NOT a hash of the excerpt.
        expected=('513a6d736874b95a10d34f648d2d3443fdf6f9a8' if rec['commit']==current['prior_commit'] else
                  '65e0af7c9b347d5c086e5d100165c787ff3652c4' if '/tests/' in rec['path'] else
                  'c32ecdc3c4cdb456514e3abc14975103f412f32d')
        check('excerpt_origin_metadata:'+rec['path']+str(rec['lines']),rec['sha']==expected)

manifest=next(r for r in current['records'] if r['path']==prefix+'MANIFEST.json')
check('manifest_sha256_unchanged',hashlib.sha256(manifest['content'].encode()).hexdigest()=='e4adba0fed22e51de37d98067a623e2e3e9575cc9e1ea039a3a88363e2378e9f')
check('manifest_payload_count',len(json.loads(manifest['content']))==10)
lock=prior_snap['files'][prefix+'REIL_C6.lock.txt']['content']
newcode=next(r['content'] for r in current['records'] if r['lines']==[61,131])
for value in ('e5a630322aead38c00d7d20ca0050eb7cd2024eb035505a6ef7bab8e5329f0bd','00c80da0799ae100798d538d9946e030259eae3b2b39cb70f99e7ff6ac7e9be8'):
    check('allowlist_record_pin_in_historical_lock:'+value,value in lock and value in newcode)
red=next(r['content'] for r in current['records'] if r['path'].endswith('01_red_12failed_8passed.log'))
green=next(r['content'] for r in current['records'] if r['path'].endswith('02_green_20passed.log'))
full=next(r['content'] for r in current['records'] if r['path'].endswith('03_bms_full_548passed_1failed_count_line.log'))
check('red_summary','12 failed, 8 passed' in red)
check('red_typeerror_count',red.count("E       TypeError: classify_record_mismatches() got an unexpected keyword argument 'dists'")==10)
check('red_assertion_count',red.count('E       AssertionError:')==2)
check('green_summary','20 passed in 0.14s' in green)
check('full_run_failure_preserved','1 failed, 548 passed' in full and 'dirty=3' in full and 'rc=1' in full)
out={'scope':'Data/blob/substring comparisons only; not supplied tests or optimizer execution','passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks,'limitations':['Code was fetched as allowed excerpts; its full byte hash was not independently recomputed.','Full-run log is a short retained excerpt, not the complete pytest output.','No new environment emit/check or mutation tests ran in this review.']}
print(json.dumps(out,ensure_ascii=False,indent=2))
