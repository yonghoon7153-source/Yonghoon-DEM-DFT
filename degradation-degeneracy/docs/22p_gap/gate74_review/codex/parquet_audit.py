"""Read stored Arrow/Parquet as data only; no fitting/scoring/project imports."""
from pathlib import Path
import sys,json,collections,hashlib,csv,io
O=Path(__file__).resolve().parent
sys.path.insert(0,str(O.parents[1]/'work/gate26-pydeps'))
import pyarrow.parquet as pq
D=Path('C:/Users/Administrator/Documents/Codex/g74_20260926/degradation-degeneracy')
B=D/'artifacts/grid_fit_v5'
out={}
for name in ('fits.parquet','curves.parquet','multistart.parquet','multistart_paired.parquet','multistart_random_only.parquet'):
    f=pq.ParquetFile(B/name)
    fields=f.schema_arrow.names
    keys=[k for k in ('cond_id','objective','run_signature','run_sig','restart_idx','seed_kind') if k in fields]
    rows=f.read(columns=keys).to_pylist()
    out[name]={'rows':f.metadata.num_rows,'columns':fields,
               'selected_column_counts':{k:dict(collections.Counter(str(r[k]) for r in rows)) for k in keys if k not in ('cond_id',)},
               'unique_cond_id':len({r['cond_id'] for r in rows}) if 'cond_id' in keys else None}
    if name=='fits.parquet': fits=rows
    if name=='curves.parquet': curves=rows
fit_ids={r['cond_id'] for r in fits}; curve_ids={r['cond_id'] for r in curves}
assert len(fits)==12276 and len(fit_ids)==len(curve_ids)==3069 and fit_ids==curve_ids
assert all(n==1 for n in collections.Counter((r['cond_id'],r['objective']) for r in fits).values())
objectives={r['objective'] for r in fits}
assert objectives=={'pocv','pocv_dvdq','pocv_dvdq_dqdv','dqdv_only'}
assert all(len({r['objective'] for r in fits if r['cond_id']==cid})==4 for cid in fit_ids)
failed=list(csv.DictReader(io.StringIO((B/'failed.csv').read_text(encoding='utf-8'))))
failed_ids={r['cond_id'] for r in failed}
assert len(failed)==len(failed_ids)==924 and not (failed_ids&curve_ids)
assert all(r['reason'].startswith('infeasible:') for r in failed)
all_ids=sorted(failed_ids|curve_ids)
all_digest=hashlib.sha256('\n'.join(all_ids).encode()).hexdigest()[:16]
fit_digest=hashlib.sha256('\n'.join(sorted(fit_ids)).encode()).hexdigest()[:16]
assert len(all_ids)==3993 and all_digest=='7b08e97e129d0bf4' and fit_digest=='f4e633ebe62924a6'
partial_ids={}
for folder in ('attempt12_partial_results','attempt3_partial_results','attempt4_partial_results'):
    root=D/'docs/22p_gap/run_windows/grid_fit_v5/wsl'/folder
    done=[json.loads(x)['cond_id'] for x in (root/'completed.jsonl').read_text().splitlines()]
    ff=list(csv.DictReader(io.StringIO((root/'failed.csv').read_text())))
    assert len(done)==len(set(done))==len(ff)==924
    assert set(done)=={r['cond_id'] for r in ff}==failed_ids
    assert all(r['reason'].startswith('infeasible:') for r in ff)
    partial_ids[folder]={'unique_completed':len(done),'all_equal_infeasible_ids':True,'completed_feasible_conditions':0,
                         'does_not_prove_no_solver_work_started':True}
out['completeness']={'fits_unique_condition_objective_pairs':12276,'condition_sets_equal':True,
 'objectives_per_condition':4,'feasible_ids':3069,'infeasible_ids':924,'ids_disjoint':True,
 'total_ids':3993,'total_condition_digest':all_digest,'fit_condition_digest':fit_digest,'row_failures_in_failed_csv':0}
out['wsl_partials']=partial_ids
out['scope']='Read-only stored data; no scientific recomputation; numerical validity/worker-cause/zero attempted computations not inferred.'
with (O/'PARQUET_DATA_AUDIT.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'completeness':out['completeness'],'wsl':partial_ids,'files':{n:v['rows'] for n,v in out.items() if isinstance(v,dict) and 'rows' in v}},ensure_ascii=False))
