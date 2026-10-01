"""Independent exact CSV arithmetic; no received module import or execution."""
import base64, csv, hashlib, json, re
from decimal import Decimal as D, getcontext
from pathlib import Path
getcontext().prec=50
ROOT=Path(__file__).resolve().parent
R=ROOT/'received'; T=R/'run/tables'
C=json.loads((R/'candidate/CONTRACT.json').read_text(encoding='utf-8-sig'))
checks=[]
def check(name, ok):
    checks.append({'check':name,'pass':bool(ok)})
    assert ok, name
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        assert reader.fieldnames and len(reader.fieldnames)==len(set(reader.fieldnames))
        for r in reader:
            assert None not in r and None not in r.values()
            yield r
def timed(p):
    out={}; prev=None
    for raw in rows(p):
        r={k:D(v) for k,v in raw.items()}; t=r['time_s']
        assert all(x.is_finite() for x in r.values()) and (prev is None or t>prev)
        out[t]=r; prev=t
    assert next(iter(out))==0
    return out
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
names=['electrolyte_guard.csv','preflight_global.csv','preflight_boundary1.csv','preflight_boundary4.csv','preflight_MinLine_ce.csv','preflight_MaxLine_ce.csv']
data={n:timed(T/n) for n in names}
g,gl,bn,bp,mn,mx=[data[n] for n in names]; ts=list(g)
check('5740 ordered stored times shared by six series, 0 to 480',len(ts)==5740 and ts[-1]==480 and all(list(x)==ts for x in data.values()))
req={D(x) for x in C['requested_times_s']}
check('4937 strict requests all present',len(req)==4937 and req<=set(ts))
check('stored interval cap',all(b-a<=(D('.000125') if a<D('.1') else D('.1'))*(1+D('1e-9'))+D('1e-12') for a,b in zip(ts,ts[1:])))
check('threshold0 and three guards zero at all stored times',all(r['threshold_mol_m3']==0 and all(r[k]==0 for k in ['electrolyte_guard','ocp_guard','surface_guard']) for r in g.values()))
check('surface global extrema in declared OCP ranges',all(r['ocp_guard']==0 and 0<r['xsurf_N_min']<=r['xsurf_N_max']<=D('.98') and D('.2228930343076256')<=r['xsurf_P_min']<=r['xsurf_P_max']<=D('.983245033354389') for r in gl.values()))
mindiff=max(abs(r['ce_min_all_mol_m3']-min(r[f'ce_min_d{i}_mol_m3'] for i in (1,2,3))) for r in g.values())
check('coupling/domain consistency and positive min/max',mindiff<=D('1e-9') and all(0<mn[t]['ce_mol_m3']<=mx[t]['ce_mol_m3'] for t in ts))
v={t:bp[t]['phis_V']-bn[t]['phis_V'] for t in ts}
residual=max(abs(v[t]-sum(bp[t][k]-bn[t][k] for k in ['Eeq_V','etamid_V','phil_V'])) for t in ts)
li_keys=['Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2']
li={t:sum(gl[t][k] for k in li_keys) for t in ts}
drift=max(abs(x-li[D(0)])/li[D(0)] for x in li.values())
check('voltage decomposition <=1e-8V; total Li drift <=1e-6',residual<=D('1e-8') and drift<=D('1e-6'))
bases={}; comparisons={}
for label,prefix,count,end,request_key in [('normal240','',3340,D(240),'baseline_requested_times_s'),('B020','B020_',987,D(5),'b020_requested_times_s')]:
    b={n:timed(R/'baseline'/(prefix+n)) for n in names[:4]}; bt=list(b[names[0]])
    br={D(x) for x in C[request_key]}; common=sorted(set(bt)&set(ts))
    check(label+' exact prefix time coverage',len(bt)==count and bt[-1]==end and all(list(x)==bt for x in b.values()) and common==bt==[t for t in ts if t<=end] and br<=set(bt))
    vb={t:b[names[3]][t]['phis_V']-b[names[2]][t]['phis_V'] for t in bt}
    vd={mode:max(abs(v[t]-vb[t]) for t in subset) for mode,subset in [('exact_common',common),('requested',sorted(br))]}
    initial={k:abs(gl[D(0)][k]-b[names[1]][D(0)][k]) for k in li_keys}
    check(label+' voltage and initial Li',max(vd.values())<=D('.001') and max(initial.values())<=D('1e-9'))
    ce={k:max(abs(g[t][k]-b[names[0]][t][k]) for t in common) for k in ['ce_min_all_mol_m3','ce_min_d1_mol_m3','ce_min_d2_mol_m3','ce_min_d3_mol_m3']}
    bases[label]={'prefix':prefix,'times':bt,'requests':br}
    comparisons[label]={'stored_common_count':len(common),'requested_count':len(br),'voltage_difference_V':vd,'surface_difference':{},'initial_Li_delta_mol_m2':initial,'ce_delta_observation_only':ce}
profiles={}
for electrode,domain in [('N',1),('P',3)]:
    coords=[D(x) for x in C['coordinates'][electrode]]
    check(electrode+' coordinates sorted distinct241',len(coords)==len(set(coords))==241 and coords==sorted(coords))
    stored={}; selected={}; stats={}
    for label,prefix,folder,expected in [('normal240','',R/'baseline',bases['normal240']['times']),('B020','B020_',R/'baseline',bases['B020']['times']),('target','',T,ts)]:
        values={}; seen=[]; idx=0; prev=None; count=0; low=D(1); high=D(0)
        delta={b:{'exact_common':D(0),'requested':D(0)} for b in bases}
        for raw in rows(folder/(prefix+f'axes_profile_{electrode}.csv')):
            row={k:D(x) for k,x in raw.items()}; t=row['time_s']; x=row['x_surface']
            assert all(a.is_finite() for a in row.values())
            if t!=prev:
                assert prev is None or idx==241
                assert prev is None or t>prev
                seen.append(t); idx=0; prev=t
                if label!='target':values[t]=[]
            assert idx<241 and row['domain_id']==domain and abs(row['coordinate_m']-coords[idx])<=D('1e-15')
            assert 0<x<1 and (x<=D('.98') if domain==1 else D('.2228930343076256')<=x<=D('.983245033354389'))
            low=min(low,x); high=max(high,x)
            if label!='target':values[t].append(x)
            else:
                for b in bases:
                    if t in stored[b]:
                        dx=abs(x-stored[b][t][idx]);delta[b]['exact_common']=max(delta[b]['exact_common'],dx)
                        if t in bases[b]['requests']:delta[b]['requested']=max(delta[b]['requested'],dx)
                if t in map(D,[0,5,30,60,120,180,240,360,480]):selected.setdefault(str(t),[]).append(x)
            idx+=1; count+=1
        check(electrode+' '+label+' complete finite time/coordinate/domain product',seen==expected and idx==241 and count==241*len(expected))
        stats[label]={'rows':count,'minimum':low,'maximum':high}
        if label!='target':stored[label]=values
        else:
            for b in bases:
                check(electrode+' '+b+' surface <=1e-4',max(delta[b].values())<=D('1e-4'))
                comparisons[b]['surface_difference'][electrode]=delta[b]
    profiles[electrode]={'statistics':stats,'selected_ranges':{t:{'min':min(a),'max':max(a)} for t,a in selected.items()}}
settings={r['key']:r['actual_value'] for r in rows(T/'axes_runtime_settings.csv')}
check('runtime settings readback',all(settings[k]==x for k,x in C['runtime_settings_required'].items()))
check('study requested time list',list(map(D,settings['study_tlist'].split()))==sorted(req))
check('guard actual binding',list(rows(T/'guard_binding.csv'))==[{'electrolyte_expression':C['guard_expression'],'stop_storage':'stepbefore_stepafter','active':'on','terminate_on':'true','threshold_SI':'0.0'}])
unit_count=0
for p in T.glob('units_*.csv'):
    rs=list(rows(p));check('unit readback '+p.name,len(rs)==1 and rs[0]['expected']==rs[0]['actual']);unit_count+=1
check('19 unit evidence records',unit_count==19)
embedded={}; markers=[]; fatal=[]
with (R/'run/batch_console.log').open(encoding='utf-8-sig') as f:
    for line in f:
        if line.startswith('AUDIT_TABLE_BASE64='):
            name,s=line.strip().split('=',1)[1].split('|',1)
            assert re.fullmatch(r'[A-Za-z0-9_]+\.csv',name) and name not in embedded
            raw=base64.b64decode(s,validate=True);h=hashlib.sha256(raw).hexdigest()
            assert (T/name).stat().st_size==len(raw) and sha(T/name)==h
            embedded[name]={'bytes':len(raw),'sha256':h}
        else:
            if re.search(r'Error running java class|OutOfMemoryError|Exception in thread|Security preference .*does not allow|/\*{3,}\s*Error',line,re.I):fatal.append(line[:500])
            if line.strip():markers.append(line.strip())
check('35 raw tables directly match native console bytes',len(embedded)==35 and set(embedded)=={p.name for p in T.iterdir() if p.is_file()})
check('native producer completion once and no fatal signature',not fatal and markers.count('NORMAL480_PRODUCER_COMPLETE')==1 and markers.count('PREFLIGHT_SOLVER_RETURNED=true; physical checks separate')==1)
for tag,sel in [('minguardall','[1, 2, 3]'),('minguard1','[1]'),('minguard2','[2]'),('minguard3','[3]')]:
    check('coupling '+tag,markers.count(f'ELECTROLYTE_COUPLING={tag}|dimension=1|entities={sel}|points=lagrange|lagrange=5')==1)
log=(R/'run/batch.log').read_text(encoding='utf-8-sig')
step_rows=[x.split() for x in log.splitlines() if re.match(r'^\s*\d+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+out\s+',x)]
check('native rounded5740 steps match exact saved times',len(step_rows)==len(ts) and all(int(s[0])==i and abs(D(s[1])-t)<=D(1).scaleb(D(s[1]).as_tuple().exponent)/2 for i,(s,t) in enumerate(zip(step_rows,ts))))
check('single time solver normal end and no subsequent integration',len(re.findall(r'^<---- Time-Dependent Solver',log,re.M))==1 and log.count('Time-stepping completed.')==1 and 'Stop condition fulfilled' not in log and not re.search(r'^\s*\d+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+out\s+',log.split('Time-stepping completed.')[1],re.M))
selected={str(t):{'voltage_V':v[t],'ce_min_mol_m3':g[t]['ce_min_all_mol_m3'],'ce_max_mol_m3':mx[t]['ce_mol_m3'],**{k:gl[t][k] for k in ['xavg_N','xavg_P','xsurf_N_min','xsurf_N_max','xsurf_P_min','xsurf_P_max']}} for t in map(D,[0,5,30,60,120,180,240,360,480])}
reported=json.loads((R/'run/DIAGNOSTIC_RESULT.json').read_text())['numeric']
check('reported drift and residual match independent exact arithmetic',D(reported['maximum_Li_relative_drift'])==drift and D(reported['maximum_voltage_identity_V'])==residual)
for label,rep in [('normal240',reported),('B020',reported['b020_comparison'])]:
    check(label+' reported voltage/surface match',D(rep['maximum_voltage_delta_V'])==comparisons[label]['voltage_difference_V']['exact_common'] and D(rep['maximum_surface_delta'])==max(x['exact_common'] for x in comparisons[label]['surface_difference'].values()))
regular_steps=[s for s in step_rows if int(s[0])>0]
check('post-initial native step column layout',all(len(s)==12 for s in regular_steps))
result={'status':'PASS','scope':'Reviewer Decimal50 arithmetic, exact time/coordinate products and native log decoding, not simulation','checks':checks,'stored_times':len(ts),'requested_times':len(req),'profile_rows':len(ts)*482,'comparisons':comparisons,'profiles':profiles,'maximum_Li_relative_drift':drift,'maximum_voltage_identity_V':residual,'minimum_operator_consistency':mindiff,'selected_times':selected,'late_count':sum(t>240 for t in ts),'native_last_step':step_rows[-1],'native_Tfail_max_post_initial':max(int(s[8]) for s in regular_steps),'native_NLfail_max_post_initial':max(int(s[9]) for s in regular_steps),'initial_Tfail':'NOT_PRINTED','native_log_summary':[x.strip() for x in log.splitlines() if any(k in x for k in ['cores in total','Solution time:','Class run time:','Save time:','Total time:','Physical memory:','Virtual memory:'])],'embedded_tables':embedded}
(ROOT/'NUMERIC_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','profiles','embedded_tables']},indent=2,default=str))
