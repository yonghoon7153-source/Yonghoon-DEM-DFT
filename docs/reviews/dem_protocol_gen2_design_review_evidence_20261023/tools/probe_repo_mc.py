#!/usr/bin/env python3
"""Exercise the repository MC operator against a half-volume single sphere."""
import argparse, hashlib, json, math, sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
sys.path.insert(0,str(a.repo.resolve()/'scripts'))
from dem_analysis_core import calc_porosity_union_exact
radius=(.5*3/(4*math.pi))**(1/3)
atoms={1:dict(x=.5,y=.5,z=.5,radius=radius)}
rows=[]
for seed in range(8):
    r=calc_porosity_union_exact(atoms,1,box_xy=1,mc_n=100,seed=seed)
    assert r['union_exact_status']=='OK'
    rows.append(dict(seed=seed,void_pct=r['porosity_union_exact_pct'],se_pct=r['porosity_union_exact_se_pct'],within_1sigma=abs(r['porosity_union_exact_pct']-50)<=r['porosity_union_exact_se_pct']))
assert not rows[1]['within_1sigma'] and abs(rows[1]['void_pct']-55)<1e-12
out=dict(synthetic_only=True,analytic_void_pct=50,radius=radius,box=[1,1,1],center=[.5,.5,.5],n=100,rows=rows,operator_sha256=hashlib.sha256((a.repo/'scripts/dem_analysis_core.py').read_bytes()).hexdigest(),note='Seeds are witnesses, not a binomial-coverage estimate; independent exact coverage is in results.json.')
a.out.parent.mkdir(parents=True,exist_ok=True)
a.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(witnesses=len(rows),one_sigma_failures=sum(not x['within_1sigma'] for x in rows),out=str(a.out))))
