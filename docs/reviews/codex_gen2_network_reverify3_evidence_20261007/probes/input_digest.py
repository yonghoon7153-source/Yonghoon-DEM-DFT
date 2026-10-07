"""Independent hashing of pinned registration inputs; no claim to reading WSL raw dumps."""
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[1];S=R/'source';sys.path.insert(0,str(S/'scripts'))
import run_network_194_parallel as rn
rows=[];cohorts=[]
for fam,prefix,cf in [('lhs','lhs00','docs/data/area_s2_cohort.tsv'),('lhsx','lhsx','docs/data/lhsx_descriptors_20260925/_cohort.tsv')]:
 hd=S/f'docs/data/{fam}_descriptors_cov_1e09f661d'
 for p in sorted(hd.glob(prefix+'_*.json')):
  j=json.loads(p.read_text(encoding='utf8'));raw=j['raw'];rows.append((fam,p.stem,[raw[k]['sha256'] for k in ['atom','contact','mesh','deck']]))
 cohorts.append(dict(name=fam,harvest_dir=str(hd),cohort=str(S/cf)))
rows.sort();ids=[f'{cid}\t{fam}' for fam,cid,_ in rows];rawlines=['\t'.join([cid,fam,*h]) for fam,cid,h in rows]
sha=lambda b:hashlib.sha256(b).hexdigest()
ind=dict(n=len(rows),ids_sha256=sha(('\n'.join(ids)+'\n').encode()),raw_sha256_table_sha256=sha(('\n'.join(rawlines)+'\n').encode()),cohort_tsv_sha256={c['name']:sha(Path(c['cohort']).read_bytes()) for c in cohorts})
plan=dict(cohorts=cohorts,queue=[dict(case=cid,cohort=fam) for fam,cid,_ in rows]);actual=rn.plan_input_digest(plan)
doc=(S/'docs/reviews/lhs_network_batch_registration_20261007_g2.md').read_text(encoding='utf8')
out=dict(independent=ind,runner=actual,equal=all(ind[k]==actual[k] for k in ind),registered_values_present=all(x in doc for x in [ind['ids_sha256'],ind['raw_sha256_table_sha256'],*ind['cohort_tsv_sha256'].values()]),counts={f:sum(r[0]==f for r in rows) for f in ('lhs','lhsx')},scope='Hashes of 194 pinned harvest metadata, not on-disk WSL raw byte verification')
(R/'evidence/input_digest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=False))
