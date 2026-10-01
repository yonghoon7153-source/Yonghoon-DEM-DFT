import hashlib,json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent
W=R.parent
tree=json.loads((R/'tree.json').read_text(encoding='utf-8'))
sources=[W/'lhs_coverage_reverify5_20260930/candidate',W/'lhs_coverage_review_20260930/candidate']
copied=[]
for e in tree:
    p=e['path']
    if e['type']!='blob' or not (p.startswith('scripts/') or p.startswith('docs/data/lhs_descriptors_20260925/') or p in ['docs/data/lhs_percolation_measured_20260915.csv','docs/data/liggghts_add_pair_pin.json','docs/data/case_master_column_census_20260919.tsv']): continue
    dst=R/'snapshot'/p
    if dst.exists(): continue
    for src in sources:
        f=src/p
        if not f.is_file(): continue
        b=f.read_bytes()
        h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        if h==e['sha']:
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dst);copied.append(p);break
print('hash verified reused',len(copied))
(R/'reused.json').write_text(json.dumps(copied,indent=2),encoding='utf-8')
