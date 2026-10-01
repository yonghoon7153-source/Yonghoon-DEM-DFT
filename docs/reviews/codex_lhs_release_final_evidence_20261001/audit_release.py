import csv,json,pathlib,sys,math,collections,hashlib,copy,subprocess,os,tempfile
import numpy as np
R=pathlib.Path(__file__).resolve().parent;S=R/'snapshot';E=R/'evidence';E.mkdir(exist_ok=True)
sys.path.insert(0,str(S/'scripts'))
import lhs_design_dataset as D
import lhs_release_build as B
def read(p,sep=','):
    with open(p,encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter=sep))
def js(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,x): (E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
out={};contexts={};colsall=[]
for family,n in [('lhs',130),('lhsx',64)]:
    data=S/'docs/data';prefix=data/'lhs_release_20261001_v11'/f'{family}_release_20261001_v11'
    rel=read(str(prefix)+'.csv');can=read(data/f'{family}_handover_20261001.csv')
    design=read(data/('lhs_design_20260818.csv' if family=='lhs' else 'lhsx_design_adapted_20260929.csv'))
    h=D.load_harvest(data/f'{family}_descriptors_cov_1e09f661d');u=D.load_union(data/'lhs_union_20260927'/f'{family}{n}_union.tsv')
    w=D.load_webapp(data/f'{family}_webapp_contact_d1ec42fba')
    got,cols,report=D.build_handover(design,h,union=u,webapp=w,webapp_groups='contact,percolation')
    contexts[family]=(design,h,u,w,rel)
    diffs=[(a['case_id'],c,a.get(c),b.get(c)) for a,b in zip(can,got) for c in a if str(a[c])!=str(b.get(c,''))]
    handerrs=B.check(str(data/f'{family}_handover_20261001.csv'),str(prefix))
    meta={'rows':len(rel),'cols':len(rel[0]),'unique_ids':len(set(r['case_id'] for r in rel)), 'build_cols':len(cols),'build_diffs':diffs[:20],'n_build_diffs':len(diffs),'release_check':handerrs,'report':report}
    meta['source_hash_disagreements']=[]
    for r in rel:
        c=r['case_id'];hv=h[c];st=w['status'][c]
        for k,v in st.get('sha',{}).items():
            want=hv.get('raw',{}).get(k,{}).get('sha256')
            if v!=want:meta['source_hash_disagreements'].append([c,k,want,v])
    meta['hold']=dict(collections.Counter(r['physical_target_status'] for r in rel));meta['reasons']=dict(collections.Counter(r['hold_reason_codes'] for r in rel));meta['boundary']=dict(collections.Counter(r['boundary_state'] for r in rel))
    meta['nonfinite']=[];meta['negative_rates']=[];meta['blank_columns']={};meta['constant_columns']={}
    for c in rel[0]:
        vals=[r[c] for r in rel];meta['blank_columns'][c]=vals.count('')
        if len(set(vals))==1:meta['constant_columns'][c]=vals[0]
        for r in rel:
            if r[c]=='':continue
            try:v=float(r[c])
            except ValueError:continue
            if not math.isfinite(v):meta['nonfinite'].append([r['case_id'],c,r[c]])
            if ('pct' in c or '_frac' in c) and v<0:meta['negative_rates'].append([r['case_id'],c,v])
    meta['nonpercolating']=sum(float(r['percolation_pct'])==0 for r in rel)
    meta['tau_truncated']=sum(hv['tau_wall_detail']['n_truncated'] for hv in h.values())
    meta['hold_target_cells_populated']={c:sum(r['physical_target_status']=='HOLD' and r[c]!='' for r in rel) for c in ['thickness_wall_gap_um','thickness_mass_conserving_um','porosity_union_exact_pct','coverage_AM_total_hertz_pct','tortuosity_SE_wall','ionic_active_pct']}
    errs=collections.defaultdict(float);bad=[];derived=[]
    for r in rel:
        c=r['case_id'];hv=h[c];np_=float(r['n_AM_P_measured'] or 0);ns=float(r['n_AM_S_measured'] or 0);nse=float(r['n_SE_measured']);na=np_+ns
        def ck(k,a,b):
            e=abs(a-b);errs[k]=max(errs[k],e)
            if e>1e-8*max(1,abs(b)):bad.append([c,k,a,b])
        ck('closure',float(r['porosity_union_exact_pct'])/100+float(r['phi_se_mass_conserving'])+float(r['phi_am_mass_conserving']),1)
        ck('SE_CN',float(r['se_se_cn'])*nse,2*float(r['area_SE_SE_n']))
        ck('AM_CN',float(r['am_am_cn'])*na,2*float(r['am_am_n_contacts']))
        ck('AM_SE_CN',float(r['am_se_cn_mean'])*na,float(r['area_AM전체_SE_n']))
        ck('ionic_sum',sum(float(r['ionic_'+s+'_pct']) for s in ['active','dead','no_se']),100)
        ck('ionic_isolation',float(r['am_ionic_isolated_pct']),float(r['ionic_dead_pct'])+float(r['ionic_no_se_pct']))
        ck('volume_fraction',float(r['phi_se_mass_conserving']),(1-float(r['porosity_union_exact_pct'])/100)*float(r['se_of_solid_vol']))
        cv=sum(N*float(r['coverage_'+ph+'_hertz_pct']) for ph,N in [('AM_P',np_),('AM_S',ns)] if N)
        ck('coverage_total',float(r['coverage_AM_total_hertz_pct']),cv/na)
        ck('thickness',float(r['thickness_mass_conserving_um']),float(r['thickness_wall_gap_um'])*(1-hv['porosity_sphere_pct_RECORD_ONLY']/100)/(1-float(r['porosity_union_exact_pct'])/100))
        eps=float(u[c]['mc_void_pct']);pse=float(u[c]['mc_SE_only_pct']);pam=float(u[c]['mc_AM_only_pct']);both=float(u[c]['mc_both_pct'])
        phi=float(r['phi_se_mass_conserving'])*100
        derived.append({'case':c,'status':r['physical_target_status'],'phi_SE_mass_pct':phi,'SE_exclusive_pct':pse,'SE_union_inclusive_pct':pse+both,'phi_minus_upper_pp':phi-pse-both,'porosity':eps,'thickness_ratio':float(r['thickness_mass_conserving_um'])/float(r['thickness_wall_gap_um']),'boundary_out_pct':sum(hv['wall_record'][s]['v_out_pct'] for s in ('floor','plate'))})
    meta['identity_max_errors']=dict(errs);meta['identity_bad']=bad
    meta['MC_SE_mass_outside_geometric_interval']=[x for x in derived if x['phi_SE_mass_pct']<x['SE_exclusive_pct']-0.1 or x['phi_minus_upper_pp']>0.1]
    meta['thickness_ratio']=[min(x['thickness_ratio'] for x in derived),float(np.median([x['thickness_ratio'] for x in derived])),max(x['thickness_ratio'] for x in derived)]
    meta['status_summaries']={}
    for status in ('OK','HOLD'):
        rr=[r for r in rel if r['physical_target_status']==status]
        ss={}
        for k in ['am_pct','ps_frac','se_of_solid_vol','thickness_wall_gap_um','porosity_union_exact_pct','coverage_AM_total_hertz_pct','percolation_pct','ionic_active_pct','am_ionic_isolated_pct']:
            vv=[float(r[k]) for r in rr if r[k]!=''];ss[k]={'min':min(vv),'median':float(np.median(vv)),'max':max(vv)}
        meta['status_summaries'][status]=ss
    for dic in read(str(prefix)+'_columns.tsv','\t'):
        c=dic['column'];colsall.append(dict(dataset=family,column=c,source=dic['source'],blank=meta['blank_columns'][c],constant=meta['constant_columns'].get(c),meaning=dic['meaning']))
    out[family]=meta
save('release_audit.json',out);save('column_inventory.json',colsall)
mut=[]
d,h,u,w,rel=contexts['lhs'];case=d[0]['case_id']
def probe(label,change):
    dd,hh,uu,ww=copy.deepcopy((d,h,u,w));change(dd,hh,uu,ww)
    try:
        rows,cols,rep=D.build_handover(dd,hh,union=uu,webapp=ww,webapp_groups='contact,percolation'); rec={'probe':label,'accepted':True,'row':{k:rows[0].get(k) for k in ['case_id','physical_target_status','hold_reason_codes','boundary_state','coverage_AM_total_hertz_pct','ionic_active_pct','ionic_dead_pct','ionic_no_se_pct','AM_P_ionic_no_se_pct','AM_S_ionic_no_se_pct','porosity_union_exact_pct','phi_se_mass_conserving','phi_am_mass_conserving']}}
    except Exception as e:rec={'probe':label,'accepted':False,'error':type(e).__name__+': '+str(e)}
    mut.append(rec)
probe('G1_single_contact_count',lambda d,h,u,w:w['rows'][case].update(area_AM_P_SE_n='2061'))
probe('P2_top_reachable_negative',lambda d,h,u,w:w['rows'][case].update(top_reachable_pct='-1'))
probe('T2_tau_25',lambda d,h,u,w:h[case]['tau_wall_detail'].update(tau_mean=25))
probe('D1_sum_change',lambda d,h,u,w:w['rows'][case].update(ionic_dead_pct='40'))
probe('C1_noninteger_component_size',lambda d,h,u,w:h[case]['tau_detail']['band_detail'].update(largest_comp_frac=0.5))
probe('coverage_total_plus_1',lambda d,h,u,w:h[case].update(coverage_AM_total_hertz_pct=h[case]['coverage_AM_total_hertz_pct']+1))
def negative(d,h,u,w):
    row=w['rows'][case];N=sum(v for k,v in h[case]['phase_counts'].items() if k!='SE');np_=h[case]['phase_counts']['AM_P'];ns=h[case]['phase_counts']['AM_S'];a=float(row['ionic_active_pct']);row.update(ionic_no_se_pct=str(-100/N),ionic_dead_pct=str(100-a+100/N))
    for ph,n in [('AM_P',np_),('AM_S',ns)]:
        a=float(row[ph+'_ionic_active_pct']);no=-100/n if ph=='AM_P' else 0.;row.update({ph+'_ionic_no_se_pct':str(no),ph+'_ionic_dead_pct':str(100-a-no)})
probe('negative_ionic_no_se_counts',negative)
probe('drop_eligibility',lambda d,h,u,w:h[case]['handover_qc'].update(physical_target_status=None,hold_reason_codes=None,boundary_state=None))
probe('union_SE_fraction_half',lambda d,h,u,w:u[case].update(se_of_solid_vol='0.5'))
probe('union_MC_SE_fraction_swap',lambda d,h,u,w:u[case].update(mc_SE_only_pct='50'))
probe('raw_sha_mismatch',lambda d,h,u,w:w['status'][case]['sha'].update(atom='0'*64))
probe('design_row_duplicate',lambda d,h,u,w:d.__setitem__(1,copy.deepcopy(d[0])))
save('mutation_results.json',mut)
print(json.dumps({k:{x:v[x] for x in ['rows','cols','n_build_diffs','release_check','hold','nonfinite','nonpercolating','tau_truncated','identity_bad','thickness_ratio']} for k,v in out.items()},ensure_ascii=False,indent=2))
print(json.dumps(mut,ensure_ascii=False,indent=2))
