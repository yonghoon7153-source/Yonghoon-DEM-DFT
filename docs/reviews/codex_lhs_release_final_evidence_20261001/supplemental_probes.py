import csv, json, pathlib, sys, hashlib, tempfile, shutil, subprocess, os, collections
import numpy as np
import networkx as nx
R=pathlib.Path(__file__).resolve().parent; S=R/'snapshot'; E=R/'evidence'
sys.path.insert(0,str(S/'scripts'))
import lhs_release_build as B
import lhs_descriptor_harvest as H
import dem_analysis_core as C
def save(name,obj): (E/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def read(p):
    with open(p,encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(p,rows):
    with open(p,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
tree={x['path']:x for x in json.loads((R/'tree.json').read_text(encoding='utf-8')) if x['type']=='blob'}
files=[]
for p in sorted(S.rglob('*')):
    if not p.is_file() or '__pycache__' in str(p):continue
    path=p.relative_to(S).as_posix(); b=p.read_bytes(); gh=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    files.append(dict(path=path,sha256=hashlib.sha256(b).hexdigest(),git_blob=gh,expected=tree.get(path,{}).get('sha'),match=gh==tree.get(path,{}).get('sha')))
save('snapshot_manifest.json',files)
result={'snapshot_files':len(files),'snapshot_mismatches':[f for f in files if not f['match']]}
with tempfile.TemporaryDirectory() as t:
    t=pathlib.Path(t); hand=S/'docs/data/lhs_handover_20261001.csv'; orig=read(hand)
    columns=list(read(S/'docs/data/lhs_release_20261001_v11/lhs_release_20261001_v11.csv')[0])
    p=str(t/'release');B.build(str(hand),columns,p)
    result['export_baseline']=B.check(str(hand),p)
    rr=read(p+'.csv');rr[0]['ionic_no_se_pct']='-1';write(p+'.csv',rr)
    result['export_changed_value']=B.check(str(hand),p)
    B.build(str(hand),columns,p);rr=read(p+'.csv');rr[0],rr[1]=rr[1],rr[0];write(p+'.csv',rr)
    result['export_shuffled_rows']=B.check(str(hand),p)
    B.build(str(hand),[c for c in columns if c not in ('physical_target_status','hold_reason_codes','boundary_state')],p)
    result['export_omitted_eligibility']=dict(columns=len(read(p+'.csv')[0]),errors=B.check(str(hand),p))
    mutated=t/'h.csv';rr=orig.copy();rr[1]=rr[0].copy();write(mutated,rr)
    shutil.copyfile(hand.with_name(hand.stem+'_columns.tsv'), t/'h_columns.tsv')
    B.build(str(mutated),columns,p)
    result['export_duplicate_canonical']=dict(rows=len(rr),unique=len({x['case_id'] for x in rr}),errors=B.check(str(mutated),p))
# Actual production functions: neither wall contact nor full-height normalization is implied.
xyz=np.array([[0.,0.,1.],[3.,0.,5.],[0.,0.,9.]])
g=nx.Graph();g.add_edge(0,1,distance=5.);g.add_edge(1,2,distance=5.)
result['tau_bent_path']=H._tau_sample(g,xyz,[{0,1,2}],{0},{2},100,100,200,42)
result['tau_bent_path'].update(path_length=10.,pair_dz=8.,wall_height=10.,path_div_wall_height=1.)
atoms={i:dict(type=3,x=float(i*4),y=0.,z=z,radius=1.) for i,z in enumerate([1.5,1.5,1.5,8.5,8.5,8.5],1)}
atoms[7]=dict(type=1,x=16.,y=1.5,z=8.5,radius=1.)
contacts=[dict(id1=7,id2=4)]
perc=C.calc_percolation(atoms,contacts,[3],10.,box_x=100.,box_y=100.)
ionic=C.calc_ionic_active_am(atoms,contacts,perc,[3],[1],{1:'AM_P',3:'SE'})
result['band_not_wall']=dict(top_se=sorted(perc['top_se']),bottom_se=sorted(perc['bottom_se']),percolation_pct=perc['percolation_pct'],top_reachable_pct=perc['top_reachable_pct'],physical_top_contacts=sum(a['type']==3 and a['z']+a['radius']>=10 for a in atoms.values()),ionic=ionic)
result['eligibility_recomputed']={}
for family in ('lhs','lhsx'):
    rows=read(S/f'docs/data/lhs_release_20261001_v11/{family}_release_20261001_v11.csv');bad=[];counts=collections.Counter();qc=collections.Counter();minband=[10**9,10**9]
    for r in rows:
        h=json.loads((S/f'docs/data/{family}_descriptors_cov_1e09f661d'/f"{r['case_id']}.json").read_text(encoding='utf-8'))
        wr=h['wall_record'];out=sum(wr[k]['n_center_out'] for k in ('floor','plate'));full=sum(wr[k]['n_fully_out'] for k in ('floor','plate'))
        neg=h['porosity_sphere_pct_RECORD_ONLY']<0;status='HOLD' if out or neg else 'OK';state='FULLY_OUT' if full else 'CENTER_CROSSED' if out else 'INSIDE'
        reasons=[]
        if out:reasons.append('BOUNDARY_CENTER_OUT')
        if neg:reasons.append('NEGATIVE_POROSITY')
        if status!=r['physical_target_status'] or state!=r['boundary_state'] or set(reasons)!=set(filter(None,r['hold_reason_codes'].split('|'))):bad.append(r['case_id'])
        counts[status]+=1
        for k,v in h.items():
            if any(x in k for x in ('n_bad_free','n_cap','n_invalid')) and isinstance(v,(int,float)):qc[k]+=v
    result['eligibility_recomputed'][family]=dict(counts=counts,mismatches=bad,coverage_qc=qc)
# Command-line regeneration and byte comparison, output stays in evidence.
result['cli_regeneration']=[]
for fam,n in [('lhs',130),('lhsx',64)]:
    out=E/f'regenerated_{fam}.csv';args=[sys.executable,str(S/'scripts/lhs_design_dataset.py'),'--export-handover',str(out),'--harvest',f'docs/data/{fam}_descriptors_cov_1e09f661d','--union',f'docs/data/lhs_union_20260927/{fam}{n}_union.tsv','--webapp',f'docs/data/{fam}_webapp_contact_d1ec42fba','--webapp-groups','contact,percolation']
    if fam=='lhsx':args+=['--design','docs/data/lhsx_design_adapted_20260929.csv']
    p=subprocess.run(args,cwd=S,capture_output=True,text=True,encoding='utf-8',timeout=90)
    (E/f'cli_{fam}.log').write_text(p.stdout+p.stderr,encoding='utf-8')
    target=S/f'docs/data/{fam}_handover_20261001.csv'
    result['cli_regeneration'].append(dict(dataset=fam,rc=p.returncode,byte_equal=out.exists() and out.read_bytes()==target.read_bytes(),generated_sha256=hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None,target_sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
save('supplemental_probes.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
