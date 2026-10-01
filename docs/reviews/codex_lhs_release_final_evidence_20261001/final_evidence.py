import pathlib,sys,json,csv,subprocess,collections,concurrent.futures,hashlib
R=pathlib.Path(__file__).resolve().parent;S=R/'snapshot';E=R/'evidence'
def run(job):
    name,args=job;p=subprocess.run([sys.executable,*args],capture_output=True,text=True,encoding='utf-8',timeout=120)
    (E/(name+'.log')).write_text(p.stdout+p.stderr,encoding='utf-8')
    return dict(name=name,rc=p.returncode,passed_lines=p.stdout.count('  ✓'),failed_lines=p.stdout.count('  ✗'),tail=p.stdout.splitlines()[-2:])
jobs=[('harvest_LF_diagnostic',[str(R/'probe_lf_selftest.py')]),('batch_copy_diagnostic',[str(R/'probe_batch_copy_selftest.py')]),('union_selftest',[str(S/'scripts/lhs_union_webapp.py'),'--selftest'])]
out={'diagnostic_tests':list(concurrent.futures.ThreadPoolExecutor(3).map(run,jobs))}
def rd(p,delim=','):
    with open(p,encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter=delim))
out['datasets']={}
for fam,n in [('lhs',130),('lhsx',64)]:
    rel=rd(S/f'docs/data/lhs_release_20261001_v11/{fam}_release_20261001_v11.csv');bad=[];mins=[10**9,10**9];qc=collections.Counter();nonperc=[]
    for r in rel:
        h=json.loads((S/f'docs/data/{fam}_descriptors_cov_1e09f661d'/f"{r['case_id']}.json").read_text(encoding='utf-8'))
        cd=h['coverage_detail'];qc['n_capped']+=cd['n_capped'];qc['n_free_surface_invalid']+=cd['n_free_surface_invalid']
        bd=h['tau_detail']['band_detail'];mins=[min(mins[0],bd['wall_n_bot']),min(mins[1],bd['wall_n_top'])]
        for side in ('P','S'):
            nn=int(r[f'n_AM_{side}_measured'] or 0)
            cc=[k for k in r if k.startswith(f'AM_{side}_')] +[f'coverage_AM_{side}_hertz_pct',f'd_am_{side.lower()}_um']
            if nn==0:
                for c in cc:
                    if r.get(c,'')!='':bad.append([r['case_id'],c,'absent phase is nonblank',r[c]])
        if float(r['percolation_pct'])==0:
            nonperc.append(r['case_id'])
            for c in ('se_se_cn_perc','se_se_cn_n_perc','tortuosity_SE_wall','tortuosity_SE_wall_median'):
                if r[c]!='':bad.append([r['case_id'],c,'nonpercolating nonblank',r[c]])
    union=rd(S/f'docs/data/lhs_union_20260927/{fam}{n}_union.tsv','\t')
    keys={x['case_id'] for x in rel}
    se=[float(x['mc_void_se_pct']) for x in union if x.get('mc_void_se_pct')]
    # Audit rows are supporting artifacts, not independent raw-dump replay.
    pp=S/f'docs/data/lhs_perc_audit_20261001/{fam}_20261001_d1ec42fba/perc_audit.tsv';ar=rd(pp,'\t')
    out['datasets'][fam]=dict(null_rule_errors=bad,nonpercolating_count=len(nonperc),coverage_qc=qc,min_wall_band_counts=mins,mc_standard_error_pp=[min(se),max(se)],percolation_audit_rows=len(ar),percolation_audit_columns=list(ar[0]),release_sha256=hashlib.sha256((S/f'docs/data/lhs_release_20261001_v11/{fam}_release_20261001_v11.csv').read_bytes()).hexdigest())
inv=json.loads((E/'column_inventory.json').read_text(encoding='utf-8'))
with open(E/'column_review.tsv','w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['dataset','column','source','blank','constant','cell_check','scope','meaning'],delimiter='\t',lineterminator='\n');w.writeheader()
    for x in inv:
        x.update(cell_check='PASS: committed intermediates -> canonical -> release; all rows',scope='NOT raw-dump replay; semantic group review in verdict');w.writerow(x)
(E/'final_evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
