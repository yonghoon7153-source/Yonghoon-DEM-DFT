"""Independent negatives on genuine synthetic producer outputs, plus owned GC fixtures."""
import copy,csv,hashlib,json,pathlib,subprocess,sys
from run_checks import HERE,BMS,ENV,dump,run
out=HERE/'r17_controls';out.mkdir(exist_ok=False)
prior=json.loads((HERE/'r17_repros/NEW_PRODUCER_RESULTS.json').read_text(encoding='utf-8'))
fixture=pathlib.Path(prior['fixture']); paths=[fixture/('n'+str(i))/'cycles_syn_Li.csv' for i in (1,2)]
summary=[]
for name,mode in [('valid_control','valid'),('unchanged_axis','same'),('alias_mismatch','alias'),('row_starts_mismatch','row'),('second_axis_seed','seed')]:
    d=out/name;d.mkdir();src=paths[0] if mode=='same' else paths[1]
    art=d/src.name;art.write_bytes(src.read_bytes());meta=json.loads(src.with_name(src.name+'.meta.json').read_text(encoding='utf-8'))
    if mode=='alias':meta['starts']+=1
    if mode=='seed':meta['seed']+=7
    if mode=='row':
        with art.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
        for row in rows:row['n_starts']='999'
        with art.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
        meta['sha256']=hashlib.sha256(art.read_bytes()).hexdigest()
    dump(art.with_name(art.name+'.meta.json'),meta)
    for axis in ('starts','n_multistart'):
        x=run('control_'+name+'_'+axis,[sys.executable,'-B',BMS/'scripts/width_report.py',paths[0],art,'--axis',axis],BMS,60)
        summary.append(dict(case=name,axis=axis,rc=x['rc'],expected=0 if mode=='valid' else 2))
def snap(p):return {q.relative_to(p).as_posix():hashlib.sha256(q.read_bytes()).hexdigest() for q in p.rglob('*') if q.is_file()}
for name,mutation,apply in [('retained_changed','retained_changed',True),('doomed_missing','doomed_missing',True),('malformed_digest','digest',True),('dryrun_changed','doomed_changed',False)]:
    root=out/('gc_'+name);part=root/'partial';entries=[];files=[]
    for att,body in [('A',b'old'),('B',b'new')]:
        f=part/'matrix'/att/'matrix_100.csv';f.parent.mkdir(parents=True);f.write_bytes(body);files.append(f)
        entries.append(dict(kind='matrix',attempt=att,artifact=f.name,path=f.relative_to(part).as_posix(),status='partial',sha256=hashlib.sha256(body).hexdigest()))
    if mutation=='retained_changed':files[1].write_bytes(b'changed')
    if mutation=='doomed_changed':files[0].write_bytes(b'changed')
    if mutation=='doomed_missing':files[0].unlink()
    if mutation=='digest':entries[0]['sha256']='not-a-sha'
    dump(part/'index.json',dict(attempts=entries))
    assert all(not q.is_symlink() and q.resolve().is_relative_to(out.resolve()) for q in root.rglob('*'))
    before=snap(root)
    x=run('gc_extra_'+name,[sys.executable,'-B',BMS/'scripts/gc_partial.py','--root',root,'--keep','1']+(['--apply'] if apply else []),BMS,60)
    summary.append(dict(case='gc_'+name,rc=x['rc'],expected=2,before=before,after=snap(root),unchanged=before==snap(root)))
dump(out/'RESULTS.json',summary)
print(json.dumps(summary,ensure_ascii=True))
