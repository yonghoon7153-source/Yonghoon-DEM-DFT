"""Independent review supplement. Reads delivered artifacts; no producer execution."""
from pathlib import Path
import hashlib, json, math, re, urllib.request, urllib.parse
from lxml import etree
R=Path(__file__).resolve().parent
PIN='90ca2c8cd6766c5e5df173533a78893cec04f6c3'
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Codex-review'}),timeout=40) as f: return f.read()
p='docs/reviews/dem_protocol_gen2_plan_draft_20261014.md'
entry=next(e for e in json.loads((R/'evidence/tree.json').read_text(encoding='utf8'))['tree'] if e['path']==p)
dest=R/'source'/p
b=dest.read_bytes() if dest.exists() else fetch(f'https://raw.githubusercontent.com/{REPO}/{PIN}/{p}')
assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==entry['sha']
dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b)
supp={'path':p,'pin':PIN,'blob_sha':entry['sha'],'sha256':hashlib.sha256(b).hexdigest()}
try:
    lit=json.loads(fetch(f'https://api.github.com/repos/{REPO}/commits/ebfed0ff5cb3ef81d386ca0575037469a824e3e5'))
    (R/'evidence/lit_branch_commit.json').write_text(json.dumps(lit,ensure_ascii=False,indent=2),encoding='utf8')
    supp['lit_head']=lit['sha']
except Exception as e: supp['lit_head_error']=str(e)
bundle=[]
for x in sorted((R/'input/repo').rglob('*')):
    if not x.is_file(): continue
    rel=x.relative_to(R/'input/repo'); y=R/'source'/rel
    bundle.append({'path':str(rel),'same_as_pin':y.exists() and x.read_bytes()==y.read_bytes()})
obj=json.loads((R/'evidence/pptx.json').read_text(encoding='utf8'))
# Baseline is recovered independently from the previous review delivery.
import runpy
baseline=runpy.run_path(str(R/'inspect_deck.py'))
old=baseline['old']; ns=baseline['ns']
refs={7:2,15:3,12:10,16:11}
def renum(t):
    return re.sub(r'\[([0-9]+(?:\s*,\s*[0-9]+)*)\]',lambda m:'['+', '.join(str(refs.get(int(n),int(n))) for n in re.findall(r'\d+',m[1]))+']',t)
inherited=[]
for n,o in {1:1,2:2,4:5,6:7,8:4,18:17}.items():
    a=old['slides'][o-1]; c=obj['slides'][n-1]
    target=[renum(t) for t in a['texts']]
    # Only the final bridge text is new on these mapped slides; show it explicitly.
    remainder=c['texts'][len(target):]
    inherited.append({'new':n,'old':o,'body_prefix_equal':target==c['texts'][:len(target)],'added_text':remainder,'notes_equal':list(map(renum,a['notes']))==c['notes'],'image_hashes_equal':sorted(x['sha256'] for x in a['media'])==sorted(x['sha256'] for x in c['media'])})
fp=R/'input/repo/docs/seminar_20261013/figs_v3/F_p4.png'
fhash=hashlib.sha256(fp.read_bytes()).hexdigest()
fp_embedded=any(x['sha256']==fhash for x in obj['slides'][10]['media'])
slope=math.log(4.8260/3.8694)/math.log(3.927/2.618)
anchor=2.618*(4.47/3.8694)**(1/slope)
out={'supplemental_source':supp,'bundle_repo':bundle,'inheritance':inherited,'F_p4_embedded':fp_embedded,'F_p4_sha256':fhash,'anchor_arithmetic':{'local_log_slope':slope,'interpolated_S_cm':anchor,'R':70.53/34,'Q':59.28/70.53},'scope':'Anchor: recomputation from recorded outputs, not raw solver rerun; no simulation.'}
(R/'evidence/final_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k!='bundle_repo'},ensure_ascii=True,indent=2))
print('bundle_repo_mismatch', [x for x in bundle if not x['same_as_pin']])
