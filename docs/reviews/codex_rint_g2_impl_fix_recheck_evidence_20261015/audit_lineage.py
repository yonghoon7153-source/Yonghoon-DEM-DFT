"""Read-only remote commit evidence; compare test-first/fix blobs at fixed SHAs."""
from pathlib import Path
import json, urllib.request
R=Path(__file__).resolve().parent
repo='yonghoon7153-source/Yonghoon-DEM-DFT'
shas={'tests_first':'e9d0cd87d2fb9320492662dab12f5c112c27f678',
      'fix':'25aecac221ba6502a31a04d9b20b700f5283711a',
      'pin':'dcb97f1ed942f622d9189eee1a1e9432dc05a655'}
rows={}
for name,sha in shas.items():
    p=R/'evidence'/f'commit_{name}.json'
    if not p.exists():
        url=f'https://api.github.com/repos/{repo}/commits/{sha}'
        req=urllib.request.Request(url,headers={'User-Agent':'Read-only-independent-review'})
        with urllib.request.urlopen(req,timeout=60) as f:p.write_bytes(f.read())
    obj=json.loads(p.read_text(encoding='utf8'));assert obj['sha']==sha
    rows[name]={'sha':sha,'date':obj['commit']['committer']['date'],
                'parents':[x['sha'] for x in obj['parents']],
                'files':[{'path':x['filename'],'blob':x['sha'],'status':x['status'],
                          'additions':x['additions'],'deletions':x['deletions']} for x in obj['files']]}
current={x['path']:x['git_blob'] for x in json.loads((R/'source_manifest.json').read_text(encoding='utf8'))['files']}
rows['tests_unchanged_at_pin']=[{'path':x['path'],'same_blob':x['blob']==current.get(x['path'])}
    for x in rows['tests_first']['files'] if x['path'].startswith('scripts/test_rint')]
(R/'evidence/lineage_summary.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps(rows,indent=2,ensure_ascii=False))
