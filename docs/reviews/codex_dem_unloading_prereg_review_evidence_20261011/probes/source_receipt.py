from pathlib import Path
import json, urllib.request, hashlib, tarfile
R=Path(__file__).resolve().parents[1]
BASE='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/'
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Codex-readonly-review'}),timeout=60) as r:return json.load(r)
pin=json.loads((R/'source_manifest.json').read_text())['pin']
head=get(BASE+'commits/claude%2Fstoic-knuth-NObVQ')
cmp=get(BASE+'compare/'+pin+'...'+head['sha'])
out=dict(review_pin=pin,checked_head=head['sha'],head_date=head['commit']['committer']['date'],commits=cmp['total_commits'],changed_paths=[e['filename'] for e in cmp['files']],attachment_sha256=hashlib.sha256((R/'submitted_request.md').read_bytes()).hexdigest(),request_repo_sha256=hashlib.sha256((R/'source/docs/reviews/codex_dem_unloading_prereg_request_20261009.md').read_bytes()).hexdigest())
(R/'evidence/pin_receipt.json').write_text(json.dumps(out,indent=2),encoding='utf8')
p=R/'source/docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz'
inv=[]
with tarfile.open(p) as tf:
    for member in tf:
        inv.append(dict(name=member.name,size=member.size))
        if member.isfile() and ('r8' in member.name or member.name.endswith('.liggghts')):
            dest=R/'evidence/ps73_logs'/member.name
            assert dest.resolve().is_relative_to((R/'evidence/ps73_logs').resolve())
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(tf.extractfile(member).read())
(R/'evidence/ps73_archive_inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
print(json.dumps(out,indent=2));print('archive members',len(inv))
