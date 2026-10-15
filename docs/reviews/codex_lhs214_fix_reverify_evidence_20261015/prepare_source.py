"""Read-only immutable GitHub intake, with verified local cache reuse."""
from pathlib import Path
import concurrent.futures, hashlib, json, os, sys, time, urllib.request, urllib.parse
R=Path(__file__).resolve().parent
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
def fetch(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-read-only-review'}),timeout=90) as f:return f.read()
        except Exception:
            if attempt==3:raise
            time.sleep(attempt+1)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def long(p):return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
for name in ('source','base','evidence','probes','notes','tmp','submitted'):(R/name).mkdir(parents=True,exist_ok=True)
for short,folder in [('9e3ef54ca','source'),('0c557e72a','base')]:
    cp=R/'evidence'/f'commit_{short}.json'
    if not cp.exists():cp.write_bytes(fetch(f'https://api.github.com/repos/{REPO}/commits/{short}'))
    commit=json.loads(cp.read_text(encoding='utf8'));pin=commit['sha']
    tp=R/'evidence'/f'tree_{short}.json'
    if not tp.exists():tp.write_bytes(fetch(f'https://api.github.com/repos/{REPO}/git/trees/{pin}?recursive=1'))
    tree=json.loads(tp.read_text(encoding='utf8'));assert not tree.get('truncated')
    es={e['path']:e for e in tree['tree'] if e['type']=='blob'}
    old=R.parent/'lhs214_failures_review_20261014'
    oldmf=json.loads((old/'source_manifest.json').read_text(encoding='utf8'))
    rows0=oldmf.get('files',oldmf.get('entries',[]))
    if isinstance(rows0,dict):rows0=[{'path':p} for p in rows0]
    paths={x['path'] for x in rows0 if x['path'] in es}
    paths|={p for p in es if (p.startswith('scripts/') and p.endswith('.py') and p.count('/')==1) or p.startswith('webapp/') and p.endswith(('.py','.js','.html'))}
    paths|={p for p in es if p.startswith('docs/reviews/lhs214_fix_evidence_20261015/') or p.startswith('docs/reviews/') and ('lhs214' in p or 'lhs_network_batch_registration' in p)}
    paths|={'AGENTS.md','CLAUDE.md','docs/reviews/findings.json','docs/reviews/selftest_inventory.tsv'}
    data_prefixes=('docs/data/lhs_descriptors_cov_1e09f661d/','docs/data/lhsx_descriptors_cov_1e09f661d/','docs/data/lhss_descriptors_cov_1e09f661d/','docs/data/lhs_union_20260927/','docs/data/lhss_union_1e09f661d/','docs/data/lhs_supp_runs_20261006/','docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/')
    paths|={p for p in es if p.startswith(data_prefixes) and es[p].get('size',0)<150_000_000}
    paths|={p for p in es if p.startswith(('docs/data/lhs_network194_11fcf91e8/','docs/data/lhs_webapp_contact_d1ec42fba/','docs/data/lhsx_webapp_contact_d1ec42fba/','docs/data/lhs_perc_audit_20261001/')) and es[p].get('size',0)<150_000_000}
    paths|={p for p in es if p.startswith('docs/data/lhs') and 'handover' in p and p.endswith(('.csv','.tsv','.json','.md')) and p.count('/')<=3}
    paths|={p for p in es if p.startswith('docs/reviews/codex_sup20_fix_reverify_evidence_20261014/evidence/receipt_extra/')}
    paths|={p for p in ('docs/data/area_s2_cohort.tsv','docs/data/lhsx_descriptors_20260925/_cohort.tsv','docs/data/lhsx_design_adapted_20260929.csv','docs/data/lhss_design_adapted_20261012.csv','docs/data/lhs_supp_design_20261006.csv','docs/data/lhs_design_20260818.csv') if p in es}
    if folder=='base':paths={p for p in paths if p.startswith(('scripts/','webapp/')) or p in ('AGENTS.md','CLAUDE.md')}
    paths|={p for p in sys.argv[1:] if p in es}
    caches=[R/folder,old/'source',R.parent/'rint_g2_impl_reverify_20261015/source',R.parent/'supr_reverify_20261014/source',R.parent/'supp20_support_review_20261012/source',R.parent/'gen2_network_reverify7_20261012/source']
    def one(p):
        e=es[p];b=None;reused=False
        for root in caches:
            q=long(root/p)
            if q.is_file():
                raw=q.read_bytes()
                if blob(raw)==e['sha']:b=raw;reused=True;break
        if b is None:b=fetch(f'https://raw.githubusercontent.com/{REPO}/{pin}/'+urllib.parse.quote(p))
        assert blob(b)==e['sha'],p
        q=long(R/folder/p);q.parent.mkdir(parents=True,exist_ok=True)
        if not q.exists():q.write_bytes(b)
        else:assert q.read_bytes()==b,p
        return {'path':p,'git_blob':e['sha'],'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'reused':reused}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:rows=list(pool.map(one,sorted(paths)))
    (R/f'{folder}_manifest.json').write_text(json.dumps({'pin':pin,'repo':REPO,'files':rows},ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'folder':folder,'pin':pin,'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'reused':sum(x['reused'] for x in rows)},ensure_ascii=False),flush=True)
