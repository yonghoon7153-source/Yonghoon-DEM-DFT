"""Reviewer-authored CSV/log calculations; supplied producer/consumer never run."""
from pathlib import Path
from decimal import Decimal as D, getcontext
import csv, json, re, hashlib, base64, collections, time

getcontext().prec=60
O=Path(__file__).resolve().parent; R=O/'received'; T=R/'run/tables'; B=R/'baseline'
started=time.perf_counter()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f)
        assert rd.fieldnames and len(rd.fieldnames)==len(set(rd.fieldnames)),p
        for v in rd:
            assert None not in v and all(x is not None for x in v.values()),p
            yield v
def timed(p):
    out={}
    for r in rows(p):
        v={k:D(s) for k,s in r.items()};assert all(x.is_finite() for x in v.values()),p
        t=v['time_s']; assert not out or t>next(reversed(out)),p
        out[t]=v
    assert out and next(iter(out))==0,p
    return out
def max_at(values):
    t,x=max(values,key=lambda v:v[1]);return {'value':str(x),'time_s':str(t)}
def ref(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
c=load(R/'candidate/CONTRACT.json'); result=load(R/'run/TRIGGER_RESULT.json')
g=timed(T/'electrolyte_guard.csv'); ts=list(g); minus,plus=ts[-2:]
assert (minus,plus)==(D('1.75'),D('1.8'))
guard_error=D(0); ties=[]
for i,(t,v) in enumerate(g.items()):
    ds=[v[f'ce_min_d{j}_mol_m3'] for j in (1,2,3)]
    guard_error=max(guard_error,abs(min(ds)-v['ce_min_all_mol_m3']))
    assert v['threshold_mol_m3']==1198 and v['ocp_guard']==v['surface_guard']==0
    assert v['electrolyte_guard']==int(v['ce_min_all_mol_m3']<=1198)==int(i==len(ts)-1)
    ties.append({'time_s':str(t),'exact_minimum_domains':[j+1 for j,x in enumerate(ds) if x==min(ds)],'near_tie_domains':[j+1 for j,x in enumerate(ds) if 0<x-min(ds)<=D('1e-9')]})
    if i:
        cap=D('.000125') if ts[i-1]<D('.1') else D('.1')
        assert t-ts[i-1]<=cap+D('1e-12')+cap*D('1e-9')
assert guard_error<=D(c['limits']['minimum_consistency_mol_m3'])
assert result['pair']['stored_times_s']==[str(t) for t in ts] and result['pair']['ties']==ties
assert list(rows(T/'guard_binding.csv'))==[{'electrolyte_expression':c['guard_expression'],'stop_storage':'stepbefore_stepafter','active':'on','terminate_on':'true','threshold_SI':'1198.0'}]

# Decode raw stdout tables as bytes, not code. Check every table against the exported CSV.
markers=[]; encoded={}; props={}; prop_duplicates=[]
with (R/'run/batch_console.log').open(encoding='utf-8-sig') as f:
    for line in f:
        if line.startswith('AUDIT_TABLE_BASE64='):
            name,payload=line.rstrip('\r\n').split('=',1)[1].split('|',1)
            assert name not in encoded and re.fullmatch(r'[A-Za-z0-9_]+\.csv',name)
            b=base64.b64decode(payload,validate=True); assert b==(T/name).read_bytes(),name
            encoded[name]={'bytes':len(b),'sha256':sha(b)}
        else:
            markers.append(line.rstrip('\r\n'))
        if line.startswith('AXES_SOLVER_PROP='):
            key,typ,val=line.rstrip('\r\n').split('=',1)[1].split('|',2)
            if key in props:prop_duplicates.append(key)
            props[key]={'type':typ,'value_text':val}
assert set(encoded)=={p.name for p in T.iterdir()}==set(result['tables_manifest'])
for n,i in encoded.items():assert i=={k:result['tables_manifest'][n][k] for k in i}
assert markers.count('GUARD1198_PRODUCER_COMPLETE')==1
assert not any('producer_failure' in x for x in encoded)
for tag,sel in [('minguardall','[1, 2, 3]'),('minguard1','[1]'),('minguard2','[2]'),('minguard3','[3]')]:
    assert markers.count(f'ELECTROLYTE_COUPLING={tag}|dimension=1|entities={sel}|points=lagrange|lagrange=5')==1
batch=(R/'run/batch.log').read_text(encoding='utf-8-sig')
assert not re.search(r'/\*{3,}\s*Error\s*\*{3,}/|Error running java class\.|Security preference .*does not allow|OutOfMemoryError|Exception in thread',batch+'\n'+'\n'.join(markers),re.I)
beg=list(re.finditer(r'^<---- Time-Dependent Solver.*$',batch,re.M));end=list(re.finditer(r'^----- Time-Dependent Solver.*-+>\s*$',batch,re.M))
stops=list(re.finditer(r'Information: Stop condition fulfilled at t = ([\d.eE+\-]+) \(([^\r\n]+)\)\.',batch))
assert len(beg)==len(end)==len(stops)==1 and beg[0].end()<stops[0].start()<end[0].start()
assert stops[0].group(2)==c['stop_description'] and D(stops[0].group(1))==plus
step_pattern=r'^\s*(\d+)\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+out\s+'
steps=list(re.finditer(step_pattern,batch[beg[0].end():end[0].start()],re.M))
assert len(steps)==len(ts) and [int(s.group(1)) for s in steps]==list(range(len(ts)))
for s,t in zip(steps,ts):
    native=D(s.group(2));assert abs(native-t)<=D(1).scaleb(native.as_tuple().exponent)/2
assert not re.search(step_pattern,batch[stops[0].end():],re.M)

# Time joins are exact decimal joins. The final noncommon stop is never interpolated.
names=['preflight_global.csv','preflight_boundary1.csv','preflight_boundary4.csv']
cur={n:timed(T/n) for n in names}; old={n:timed(B/n) for n in names}
assert all(list(v)==ts for v in cur.values())
bt=list(old[names[0]]);assert all(list(v)==bt for v in old.values())
assert list(timed(B/'electrolyte_guard.csv'))==bt
actual_intersection=sorted(set(ts)&set(bt))
common=[t for t in actual_intersection if t<=minus]; requested=sorted(D(x) for x in c['requested_times_s'] if D(x)<=minus)
assert common[-1]==minus and plus not in common and len(common)==922 and len(requested)==122
assert set(requested)<=set(ts)&set(bt)
coverage=result['numeric']['coverage']
assert [D(x) for x in coverage['common_stored']]==common and [D(x) for x in coverage['expected_requested']]==requested
vdelta={}; resid={}; li={}; initial_diffs={}
Lcols=['Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2']; glob=cur[names[0]]
L0=sum(glob[D(0)][k] for k in Lcols)
for t in ts:
    n,p=cur[names[1]][t],cur[names[2]][t]
    vol=p['phis_V']-n['phis_V']; parts=sum(p[k]-n[k] for k in ['Eeq_V','etamid_V','phil_V'])
    resid[t]=abs(vol-parts);li[t]=abs(sum(glob[t][k] for k in Lcols)-L0)/L0
    assert glob[t]['ocp_guard']==0
    for electrode,lo,hi in [('N',D(0),D('.98')),('P',D('.2228930343076256'),D('.983245033354389'))]:
        assert lo<=glob[t]['xsurf_'+electrode+'_min']<=glob[t]['xsurf_'+electrode+'_max']<=hi
        assert 0<glob[t]['xsurf_'+electrode+'_min']<=glob[t]['xsurf_'+electrode+'_max']<1
    if t in common:
        vdelta[t]=abs(vol-(old[names[2]][t]['phis_V']-old[names[1]][t]['phis_V']))
for col in Lcols:initial_diffs[col]=str(abs(glob[D(0)][col]-old[names[0]][D(0)][col]))
assert all(D(x)<=D('1e-9') for x in initial_diffs.values())

dx_by_time={t:D(0) for t in common}; pinfo={}
for electrode,domain,lo,hi in [('N',1,D(0),D('.98')),('P',3,D('.2228930343076256'),D('.983245033354389'))]:
    coords=[D(x) for x in c['coordinates'][electrode]];assert len(coords)==241 and len(set(coords))==241
    profiles=[];counts=[];errors=[]
    for folder,expected_ts in [(T,ts),(B,bt)]:
        prof={};count=0;err=D(0);colnames=None
        for r in rows(folder/f'axes_profile_{electrode}.csv'):
            assert list(r)==['time_s','coordinate_m','x_surface','x_particle_average','Eeq_V','etaMid_V','phil_V','domain_id']
            v={k:D(s) for k,s in r.items()};assert all(x.is_finite() for x in v.values())
            t=v['time_s']; assert t==expected_ts[count//241]
            j=count%241;err=max(err,abs(v['coordinate_m']-coords[j]))
            assert v['domain_id']==domain and lo<=v['x_surface']<=hi and 0<v['x_surface']<1
            prof.setdefault(t,[]).append(v['x_surface']);count+=1
        assert count==len(expected_ts)*241 and list(prof)==expected_ts and err<=D(c['limits']['coordinate_m'])
        profiles.append(prof);counts.append(count);errors.append(str(err))
    for t in common:dx_by_time[t]=max(dx_by_time[t],max(abs(x-y) for x,y in zip(profiles[0][t],profiles[1][t])))
    pinfo[electrode]={'target_rows':counts[0],'baseline_rows':counts[1],'coordinate_max_errors_m':errors,'points_per_time':241,'domain':domain}

units={ 'eguard':['s']+['mol/m^3']*5+['1']*3, 'nglobal':['s']+['mol/m^2']*3+['1']*7+['A/m^2']*3,
        'point1':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
        'MinLinece':['s','mol/m^3'],'MaxLinece':['s','mol/m^3'],'profiletimes':['s'],'profileN':['s','m','1','1','V','V','V','1']}
units['point4']=units['point1'];units['profileP']=units['profileN']; unit_count=0
for tag,base_units in units.items():
    for phase in (['inferred','configured','evaluated'] if tag=='eguard' else ['configured','evaluated']):
        wanted=base_units.copy()
        if phase!='configured':
            for j in {'eguard':[6,7,8],'nglobal':[10],'profileN':[7],'profileP':[7]}.get(tag,[]):wanted[j]=''
        text='['+', '.join(wanted)+']'
        assert list(rows(T/f'units_{tag}_{phase}.csv'))==[{'tag':tag,'phase':phase,'expected':text,'actual':text}]
        unit_count+=1
metrics={'maximum_voltage_delta_V':max(vdelta.values()),'maximum_surface_delta':max(dx_by_time.values()),'maximum_Li_relative_drift':max(li.values()),'maximum_voltage_identity_V':max(resid.values())}
for k,v in metrics.items():assert abs(v-D(result['numeric'][k]))<=D('1e-50'),k
for k,limit in [('maximum_voltage_delta_V','voltage_V'),('maximum_surface_delta','surface_x'),('maximum_Li_relative_drift','relative_Li'),('maximum_voltage_identity_V','voltage_identity_V')]:assert metrics[k]<=D(c['limits'][limit])
expected_props=load(R/'external/10_expected_solver.json')
diff={k:{'baseline':expected_props.get(k),'observed':props.get(k)} for k in sorted(set(expected_props)|set(props)) if expected_props.get(k)!=props.get(k)}
windows=[]
for family,times in [('requested',requested),('common',common)]:
    for name,l,h in [('0-stop_prefix',D(0),minus),('0-0.1',D(0),D('.1')),('0.1-1',D('.1'),D(1)),('1-stop_prefix',D(1),minus)]:
        sub=[t for t in times if l<=t<=h]
        windows.append({'family':family,'window':name,'count':len(sub),'voltage':max_at((t,vdelta[t]) for t in sub),'surface':max_at((t,dx_by_time[t]) for t in sub)})
audit={'status':'PASS','precision_decimal':60,'tables_base64_bytes_matched':len(encoded),'unit_records':unit_count,
    'guard':{'stored_times':len(ts),'pre':{k:str(v) for k,v in g[minus].items()},'post':{k:str(v) for k,v in g[plus].items()},'minimum_consistency_max_error':str(guard_error),'single_final_guard_transition':True,'other_guards_zero':True},
    'native':{'time_solver_sections':1,'raw_step_rows':len(steps),'step_indices_contiguous':True,'rounded_times_match_exact_csv':True,'stop_line':stops[0].group(0),'no_logged_steps_after_stop':True,'core_declaration_lines':[x for x in batch.splitlines() if 'cores in total' in x]},
    'coverage':{'target':len(ts),'baseline':len(bt),'actual_time_intersection':len(actual_intersection),'common_comparison_prefix':len(common),'requested_prefix':len(requested),'common_last':str(common[-1]),'target_noncommon':[str(t) for t in ts if t not in set(bt)],'stop_exists_in_baseline':plus in bt,'stop_excluded_by_pretrigger_prefix_contract':True,'no_interpolation':True},
    'profiles':pinfo,'metrics':{k:str(v) for k,v in metrics.items()},'initial_li_component_delta_mol_m2':initial_diffs,'eight_prefix_views_reviewer_calculated':windows,
    'solver_properties':{'observed_count':len(props),'expected_count':len(expected_props),'duplicates':prop_duplicates,'differences':diff},
    'resource_mesh_markers':[x for x in markers if x.startswith(('AXES_PHYSICAL_MESH_DOMAIN=','AXES_PARTICLE=','ELECTROLYTE_THRESHOLD_','PREFLIGHT_TIME='))],
    'elapsed_seconds':time.perf_counter()-started,'received_programs_executed':0}
(O/'NUMERIC_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in audit.items() if k not in ['solver_properties','eight_prefix_views_reviewer_calculated','resource_mesh_markers']},ensure_ascii=False))
print('SOLVER_DIFF',json.dumps(audit['solver_properties'],ensure_ascii=False))
