"""Match preliminary overlay byte dependencies and raw data to acquired pin."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SRC=ROOT/'source'
STAGE=HERE/'staged_source'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
names=set()
for p in (HERE/'evidence').glob('*.imports.json'):
    if 'test_part_b_' in p.name:
        names.update(json.loads(p.read_text(encoding='utf8')))
names.update(['scripts/test_rint_g2_join.py',
 'docs/data/real14_am_scaffold.csv',
 'docs/data/real14_reference_20260928/atom_2060000.liggghts.gz',
 'docs/data/real14_reference_20260928/contact_2060000.liggghts.gz',
 'docs/data/case15_corner_20261001/case15_am_scaffold.csv',
 'docs/data/case15_corner_20261001/atom_v4_1710000.liggghts.gz',
 'docs/data/case15_corner_20261001/contact_v4_1710000.liggghts.gz',
 'docs/data/heckel_sweep_scaffolds/LOOSE_am_scaffold.csv'])
rows=[]
for rel in sorted(names):
    p,q=SRC/rel,STAGE/rel
    row={'path':rel,'fullpin_sha256':sha(p) if p.exists() else None,'overlay_sha256':sha(q) if q.exists() else None}
    row['equal']=row['fullpin_sha256'] is not None and row['fullpin_sha256']==row['overlay_sha256']
    rows.append(row)
out={'pin':'5dc6f7f0b91fd9db39ab595f6b8c79a8f0d2f3b5','source':str(SRC),'n':len(rows),'all_equal':all(x['equal'] for x in rows),'files':rows}
(HERE/'evidence/fullpin_overlay_match.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
