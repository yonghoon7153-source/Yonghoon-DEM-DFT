"""Reviewer-owned data-only audit. No subject imports, solves, restore or publishers."""
from pathlib import Path
import collections, csv, hashlib, io, json, subprocess, sys, zipfile
O = Path(__file__).resolve().parent
W = Path('C:/Users/Administrator/Documents/Codex/g74_20260926')
D = W / 'degradation-degeneracy'
sys.path.insert(0, str(O.parents[1] / 'work/gate26-pydeps'))
import yaml
H = 'a49a021833282e0bd04c4565591668dc323e9630'
C = '7a7945564e6a94803b4d3bc72e8202534189ccdb'
E = 'e34eea8455d87f8e33c6ae7113fe3d16ddb600e3'
DATA = 'd9f8791c6473ad972e3b6475192c2f8f569cded9'

def git(*args): return subprocess.check_output(['git','-c','http.sslBackend=openssl','-c','credential.interactive=never','-C',str(W),*args])
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(n, obj):
    if (O/n).exists():
        assert json.loads((O/n).read_text(encoding='utf-8'))==obj, n
        return
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2,default=str); f.write('\n')
def raw(ref, name): return git('show',ref+':degradation-degeneracy/'+name)
def obj(name): return yaml.safe_load((D/name).read_bytes())
def hist(ref,name): return yaml.safe_load(raw(ref,name))
def canon(obj): return json.dumps(obj,ensure_ascii=False,sort_keys=True,allow_nan=False,separators=(',',':')).encode()

assert git('rev-parse','HEAD').decode().strip()==H
assert not git('status','--porcelain=v1','-uall').strip()
tracked=[p for p in git('ls-files','-z','--','degradation-degeneracy').decode().split('\0') if p]
dump('SOURCE_BEFORE.json',{p:ident((W/p).read_bytes()) for p in tracked})
scope=['degradation-degeneracy/'+n for n in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
scope_paths=[p for p in git('ls-files','-z','--',*scope).decode().split('\0') if p]
hh=hashlib.sha256()
for p in sorted(scope_paths):
    hh.update(p.removeprefix('degradation-degeneracy/').encode()); hh.update((W/p).read_bytes())
assert hh.hexdigest()[:16]=='c2ef1a811e70bb4c'
diffs={}
for label,a,b,paths in [
    ('CODE_TO_HEAD_SCOPE',C,H,scope),('CODE_TO_EXEC_SCOPE',C,E,scope),
    ('EXEC_TO_DATA_INDEX',E,DATA,['degradation-degeneracy/artifacts/artifact_index.yaml']),
    ('DATA_TO_CORRECTED_INDEX',DATA,H,['degradation-degeneracy/artifacts/artifact_index.yaml']),
    ('G73_TO_G74_LEDGER','b0c0b9ca',H,['degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml']),
    ('DATA_COMMIT_STATS',E,DATA,['degradation-degeneracy'])]:
    flags=['--stat'] if label.endswith('STATS') else []
    bts=git('diff','--no-ext-diff',*flags,a,b,'--',*paths)
    (O/(label+'.diff')).write_bytes(bts); diffs[label]=ident(bts)
assert diffs['CODE_TO_HEAD_SCOPE']['bytes']==diffs['CODE_TO_EXEC_SCOPE']['bytes']==0

name='docs/22p_gap/LEG_PRESERVATION.yaml'
ledger=obj(name)
plans=[]
for ref in ('951b6136','69c3c826',E):
    l=hist(ref,name); p=next(x for x in l['planned'] if x['leg_id']=='grid_fit_v5')
    calculated=hashlib.sha256(canon(p['run_spec'])).hexdigest()
    assert p['run_spec_digest']==calculated
    plans.append({'commit':git('rev-parse',ref).decode().strip(),'row':p,'computed_run_spec_digest':calculated})
base=plans[0]['row']['run_spec']
for p in plans[1:]:
    a=json.loads(json.dumps(p['row']['run_spec']));a['grid']['discharged_cache_sha256']=None
    assert a==base
dump('PLAN_HISTORY.json',plans)

old_idx=hist(E,'artifacts/artifact_index.yaml'); initial_idx=hist(DATA,'artifacts/artifact_index.yaml'); idx=obj('artifacts/artifact_index.yaml')
assert set(old_idx['runs'])==set(idx['runs'])-{'grid_fit_v5'}
assert initial_idx['runs']=={'grid_fit_v5':idx['runs']['grid_fit_v5']}
assert all(v==idx['runs'][k] for k,v in old_idx['runs'].items())
# Compare each restored YAML run block byte-for-byte, not just parsed values.
def blocks(b):
    import re
    starts=list(re.finditer(rb'^  ([A-Za-z0-9_]+):\r?$',b,re.M))
    return {m[1].decode(): b[m.start():starts[i+1].start() if i+1<len(starts) else len(b)] for i,m in enumerate(starts)}
old_blocks=blocks(raw(E,'artifacts/artifact_index.yaml')); new_blocks=blocks((D/'artifacts/artifact_index.yaml').read_bytes())
assert all(v==new_blocks[k] for k,v in old_blocks.items())
assert blocks(raw(DATA,'artifacts/artifact_index.yaml'))['grid_fit_v5']==new_blocks['grid_fit_v5']
old_art=git('diff','--name-only',E,H,'--',*[f'degradation-degeneracy/artifacts/{k}' for k in old_idx['runs']]).decode().splitlines()
assert not old_art

reg='docs/22p_gap/_exec_class'
old_reg={Path(p).name:ident(raw(E,p)) for p in git('ls-tree','-r','--name-only',E,'--','degradation-degeneracy/'+reg).decode().splitlines() for p in [p.removeprefix('degradation-degeneracy/')]}
new_reg={p.name:ident(p.read_bytes()) for p in (D/reg).glob('*.json')}
assert len(old_reg)==367 and len(new_reg)==369 and all(new_reg.get(k)==v for k,v in old_reg.items())
added={k:json.loads((D/reg/k).read_bytes()) for k in new_reg.keys()-old_reg.keys()}
def snapshot(name):
    return {line.split()[0].split('/')[-1]:line.split()[1] for line in (D/name).read_text().splitlines() if line.strip()}
gabia='docs/22p_gap/run_windows/grid_fit_v5/gabia/'
before=snapshot(gabia+'registry_before.txt');after=snapshot(gabia+'registry_after.txt')
assert before=={k:v['sha256'] for k,v in old_reg.items()}
assert after=={k:v['sha256'] for k,v in new_reg.items()}

bundle='artifacts/grid_fit_v5'; payload=obj(bundle+'/payload_sha256.yaml')
members={p.relative_to(D/bundle).as_posix():ident(p.read_bytes()) for p in (D/bundle).rglob('*') if p.is_file()}
assert set(members)==set(payload)|{'payload_sha256.yaml'}
assert all(members[k]['sha256']==v for k,v in payload.items())
receipt=obj('docs/22p_gap/receipts/grid_fit_v5.validate.yaml'); core=receipt['core']
assert core['bundle']['files']==len(members)==29
assert core['bundle']['bytes']==sum(x['bytes'] for x in members.values())
assert core['bundle']['payload_index_sha256']==members['payload_sha256.yaml']['sha256']
assert core['bundle']['fits_sha256']==members['fits.parquet']['sha256']
assert hashlib.sha256(yaml.safe_dump(core,allow_unicode=True,sort_keys=False,width=100).encode('utf-8')).hexdigest()==receipt['core_sha256']
leg=next(x for x in ledger['legs'] if x['leg_id']=='grid_fit_v5')
ev=leg['evidence'];assert ev['verification_receipt_core_sha256']==receipt['core_sha256']
assert ev['out']==obj(bundle+'/restore_map.yaml')['run_dir']==core['restore']['run_dir_relative']
outputs={x['role']:x for x in core['outputs']}
assert outputs['rescored_summary']['source_file_sha256']==members['fits.parquet']['sha256']
assert outputs['sealed_summary']['file_sha256']==members['degeneracy_summary.yaml']['sha256']
assert outputs['sealed_summary']['semantic_sha256']==outputs['rescored_summary']['semantic_sha256']
assert len(core['validation']['checks'])==core['validation']['n_checks']==33
rows=list(csv.DictReader(io.StringIO((D/bundle/'failed.csv').read_text(encoding='utf-8'))))
fail_values={k:dict(collections.Counter(r[k] for r in rows)) for k in rows[0] if k.lower() in ('reason','error','status')}
partials={}
wsl='docs/22p_gap/run_windows/grid_fit_v5/wsl'
for folder in ('attempt12_partial_results','attempt3_partial_results','attempt4_partial_results'):
    records=[json.loads(x) for x in (D/wsl/folder/'completed.jsonl').read_text().splitlines()]
    partials[folder]={'records':len(records),'keyset':sorted(records[0]),'status':dict(collections.Counter(x.get('status') for x in records)),
                     'failed_csv_rows':len(list(csv.DictReader(io.StringIO((D/wsl/folder/'failed.csv').read_text()))))}
cache_ids={p.name:ident(p.read_bytes()) for p in (D/wsl).glob('discharged_cache*.json')}

report={'head':H,'code':C,'execution_head':E,'source_digest':hh.hexdigest()[:16],'scope_files':len(scope_paths),
 'tracked_files':len(tracked),'diffs':diffs,'plan_history_count':len(plans),
 'index':{'prior_runs':list(old_idx['runs']),'data_runs':list(initial_idx['runs']),'corrected_runs':list(idx['runs']),
          'prior_blocks_byte_identical':True,'new_block_byte_identical':True,'old_bundle_changes':old_art},
 'registry':{'before':367,'after':369,'prior_bytes_unchanged':True,'snapshots_match':True,'added':added},
 'bundle':{'files':len(members),'bytes':sum(v['bytes'] for v in members.values()),'exact_set_sha':True,'payload_index':members['payload_sha256.yaml']},
 'receipt':{'core_sha':receipt['core_sha256'],'core_rehashed':True,'reported_validation_checks':len(core['validation']['checks']),
            'output_anchors_match':True,'rescored_output_content_supplied':False,'validation_rerun':False,'stamp':receipt['stamp']},
 'failed_csv':{'rows':len(rows),'reason_counts':fail_values},'wsl_partials':partials,'wsl_cache_files':cache_ids,
 'cohort':next(x for x in ledger['cohorts'] if x['cohort_id']=='g18_2026_09_15'),
 'grid_fit_v5_claim_roles':leg.get('claim_roles'),'regeneration_capability':ev.get('regeneration_capability'),
 'project_imports':0,'main_compute_restore_class_changes':0,'reviewer_parsing_only':True}
dump('DATA_AUDIT.json',report)
refs=['docs/22p_gap/GATE74_REQUEST.md',name,'docs/22p_gap/receipts/grid_fit_v5.validate.yaml',
      'docs/RESULTS_grid_fit_v5.md','docs/GATE70_WORKING_STATE.md','artifacts/artifact_index.yaml',
      'src/grid.py','src/baseline.py','tools/preserve.py','scripts/archive_results.sh','docs/22p_gap/plan_leg.py',
      'tests/test_docs_lint.py','docs/22p_gap/CLAIM_STATUS.yaml','docs/22p_gap/row_projection.py','docs/22p_gap/make_receipt.py']
refs += [p.relative_to(D).as_posix() for p in (D/'docs/22p_gap/run_windows/grid_fit_v5').rglob('*') if p.is_file()]
refs += [bundle+'/'+p for p in payload if Path(p).suffix in ('.yaml','.json','.csv')]
refs += [bundle+'/payload_sha256.yaml']
for n in sorted(set(refs)):
    if not (D/n).is_file():continue
    dest=O/'reference'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((D/n).read_bytes())
dump('IDENTITY.json',{'head':H,'execution_head':E,'code':C,'scope_files':len(scope_paths),'source_digest':hh.hexdigest()[:16],
                     'reference_files':len(set(refs)),'tracked_before':len(tracked),'request':ident((D/'docs/22p_gap/GATE74_REQUEST.md').read_bytes())})
print(json.dumps({k:v for k,v in report.items() if k not in ('cohort','registry')},ensure_ascii=False,default=str))
