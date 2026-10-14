"""Independent read-only input/definition audit. No runner/receipt imports or solves."""
from pathlib import Path
import ast
import collections
import csv
import hashlib
import io
import json
import tarfile

R = Path(__file__).resolve().parents[1]
S = R / 'source'
B = R.parent / 'supp20_support_review_20261012/source'
sha = lambda b: hashlib.sha256(b).hexdigest()

def assignment(tree, name):
    return next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))

def csv_rows(p, sep=','):
    return list(csv.DictReader(io.StringIO(p.read_text(encoding='utf-8')), delimiter=sep))

def tar(p):
    with tarfile.open(p, 'r:gz') as t:
        members = t.getmembers()
        hazards = [m.name for m in members if m.name.startswith(('/', '\\'))
                   or '..' in Path(m.name).parts or m.issym() or m.islnk()]
        return {m.name:t.extractfile(m).read() for m in members if m.isfile()}, hazards, len(members)

def flat(v, pre=''):
    if isinstance(v, dict):
        return {kk:vv for k, x in v.items() for kk,vv in flat(x, pre + ('.' if pre else '') + k).items()}
    return {pre:v}

trees = [ast.parse((p/'scripts/lhs_design_dataset.py').read_text(encoding='utf-8')) for p in (B,S)]
keys = ['lhsx_w_AM_P', 'lhsx_w_AM_S', 'lhss_w_AM_P', 'lhss_w_AM_S']
definitions = []
for t in trees:
    d=assignment(t,'DESIGN_DEFINE')
    definitions.append({ast.literal_eval(k): ast.literal_eval(v) for k,v in zip(d.keys,d.values) if ast.literal_eval(k) in keys})
    for i,k in enumerate(d.keys):
        if ast.literal_eval(k) in keys: d.values[i] = ast.Constant(value='DEFINITION_REMOVED_FOR_CODE_COMPARISON')
    t.body = [n for n in t.body if not(isinstance(n, ast.FunctionDef) and n.name == '_selftest')]

results = {'definitions':dict(before=definitions[0],after=definitions[1]),
           'dataset_nonselftest_ast_equal_excluding_four_definitions':ast.dump(trees[0])==ast.dump(trees[1])}
results['source_slot_validation']={}
for ds, fname in [('lhss','lhss_design_adapted_20261012.csv'),('lhsx','lhsx_design_adapted_20260929.csv')]:
    p=S/'docs/data'/fname
    rows=csv_rows(p)
    bad=[]; mono=[]
    for row in rows:
        kind=row[ds+'_kind']; wp=float(row[ds+'_w_AM_P']); ws=float(row[ds+'_w_AM_S'])
        expected=wp/(wp+ws) if kind=='bimodal' else 1.0 if kind=='mono_AM_P' else 0.0
        if abs(expected-float(row['ps_frac']))>1e-12 or (kind!='bimodal' and ws!=0): bad.append(row['case_id'])
        if kind=='mono_AM_S': mono.append(dict(case_id=row['case_id'],P=wp,S=ws,old_formula=wp/(wp+ws),ps_frac=float(row['ps_frac'])))
    results['source_slot_validation'][ds]=dict(n=len(rows),kinds=dict(collections.Counter(r[ds+'_kind'] for r in rows)),bad=bad,monoS=mono,
        unchanged_from_baseline=p.read_bytes()==(B/'docs/data'/fname).read_bytes(),sha256=sha(p.read_bytes()))

nptree=ast.parse((S/'scripts/run_network_194_parallel.py').read_text(encoding='utf-8'))
sealed=ast.literal_eval(assignment(nptree,'CODE_FILES'))
hashes={k:sha((S/k).read_bytes()) for k in sealed}
results['sealed']=dict(n=len(sealed),changed=[k for k in sealed if (S/k).read_bytes()!=(B/k).read_bytes()],
    code_fp=sha(json.dumps(sorted(hashes.items()),separators=(',',':')).encode()),hashes=hashes)
results['other_unchanged']={p:(S/p).read_bytes()==(B/p).read_bytes() for p in [
    'scripts/lhss_design_adapter.py','scripts/lhsx_design_adapter.py','scripts/run_network_194_parallel.py',
    'docs/data/lhs_supp_design_20261006.csv','docs/data/lhss_design_adapted_20261012.csv']}

data=S/'docs/data/lhs_supp_runs_20261006'
p2=data/'lhss_harvest_20261011_r2.tgz';p3=data/'lhss_harvest_r3_1e09f661d.tgz'
a,h2,n2=tar(p2); b,h3,n3=tar(p3)
pre2='lhss_out_20261011/';pre3='lhss_out_r3_1e09f661d/'
j2={Path(n).stem:json.loads(v) for n,v in a.items() if n.startswith(pre2+'descriptors_r2/lhss_') and n.endswith('.json')}
j3={Path(n).stem:json.loads(v) for n,v in b.items() if n.startswith(pre3+'descriptors_r3/lhss_') and n.endswith('.json')}
deltas={}
for k in sorted(j3):
    x,y=flat(j2[k]),flat(j3[k])
    deltas[k]=dict(changed=[q for q in x.keys() & y.keys() if x[q]!=y[q]],r2_only=sorted(x.keys()-y.keys()),r3_only=sorted(y.keys()-x.keys()))
hdir=S/'docs/data/lhss_descriptors_cov_1e09f661d'
u3=S/'docs/data/lhss_union_1e09f661d/lhss20_union.tsv'
results['archives']=dict(r2_sha256=sha(p2.read_bytes()),r3_sha256=sha(p3.read_bytes()),member_counts=[n2,n3],hazards=h2+h3,
    harvest_head=b[pre3+'harvest_head.txt'].decode().strip(),case_ids_equal=sorted(j2)==sorted(j3),deltas=deltas,
    imported_descriptor_mismatches=[k for k in j3 if b[pre3+'descriptors_r3/'+k+'.json']!=(hdir/(k+'.json')).read_bytes()],
    union_import_byte_equal=b[pre3+'lhss20_union_r3.tsv']==u3.read_bytes(),
    union_r2_r3_byte_equal=a[pre2+'lhss20_union_r2.tsv']==b[pre3+'lhss20_union_r3.tsv'],
    union_r2_r3_cells_equal=list(csv.DictReader(io.StringIO(a[pre2+'lhss20_union_r2.tsv'].decode()),delimiter='\t'))==list(csv.DictReader(io.StringIO(b[pre3+'lhss20_union_r3.tsv'].decode()),delimiter='\t')),
    cohort_bytes_equal=a[pre2+'_cohort.tsv']==b[pre3+'_cohort.tsv']==(hdir/'_cohort.tsv').read_bytes(),
    family_lf_equal=b[pre3+'_design_family.csv'].replace(b'\r\n',b'\n')==(hdir/'_design_family.csv').read_bytes(),
    summary_bytes_equal=b[pre3+'descriptors_r3/_batch_summary.json']==(hdir/'_batch_summary.json').read_bytes())

ids=''.join(f'{k}\tlhss\n' for k in sorted(j3))
rawlines=[];missing=[];actual_files=[]
for k in sorted(j3):
    raw=j3[k]['raw']
    hh=[raw.get(n,{}).get('sha256','') for n in ('atom','contact','mesh','deck')]
    if not all(hh):missing.append(k)
    rawlines.append('\t'.join([k,'lhss',*hh]))
    for n in ('atom','contact','mesh','deck'):
        actual_files.append(dict(case=k,kind=n,path=raw[n].get('path'),sha256=raw[n].get('sha256')))
results['input_digest']=dict(n=len(j3),ids_sha256=sha(ids.encode()),raw_sha256_table_sha256=sha(('\n'.join(rawlines)+'\n').encode()),
    cohort_tsv_sha256=sha((hdir/'_cohort.tsv').read_bytes()),missing_raw_sha=missing,
    raw_bytes_not_recomputed='raw dumps/meshes/decks on author WSL are not present; hashes here are recalculated from committed descriptor claims, not raw bytes',raw_items=actual_files)
results['registration_values_present']={k:str(v) in (S/'docs/reviews/lhs_network_batch_registration_20261012_supp20.md').read_text(encoding='utf-8') for k,v in results['input_digest'].items() if k.endswith('sha256')}
out=R/'evidence/design_extra.json'
out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in results.items() if k not in ('definitions','archives','sealed','input_digest')},ensure_ascii=False,indent=2))
print('sealed:', results['sealed']['n'],results['sealed']['changed'],results['sealed']['code_fp'])
print('archives:', {k:v for k,v in results['archives'].items() if k!='deltas'})
print('r2/r3 changes:',dict(collections.Counter(tuple(d['changed']) for d in deltas.values())))
print('r2-only counts:',dict(collections.Counter(len(d['r2_only']) for d in deltas.values())))
print('r3-only counts:',dict(collections.Counter(len(d['r3_only']) for d in deltas.values())))
print('input:',{k:v for k,v in results['input_digest'].items() if k!='raw_items'})
print('saved',out)
