"""UNEXECUTED candidate: normal30/protected-stop consumer. No COMSOL/import/process calls.
Functions below require changed-branch validation before any native release.
"""
from pathlib import Path
from decimal import Decimal as D, localcontext
import csv, json, re, base64, hashlib

class EvidenceError(ValueError): pass
HEADERS={
 'electrolyte_guard.csv':'time_s ce_min_all_mol_m3 ce_min_d1_mol_m3 ce_min_d2_mol_m3 ce_min_d3_mol_m3 threshold_mol_m3 electrolyte_guard ocp_guard surface_guard'.split(),
 'preflight_global.csv':'time_s Li_N_mol_m2 Li_P_mol_m2 Li_electrolyte_mol_m2 xavg_N xavg_P xsurf_N_min xsurf_N_max xsurf_P_min xsurf_P_max ocp_guard reaction_N_A_m2 reaction_P_A_m2 leak_leftward_A_m2'.split(),
 'guard_binding.csv':'electrolyte_expression stop_storage active terminate_on threshold_SI'.split()}
for _n in ('preflight_boundary1.csv','preflight_boundary4.csv'):
    HEADERS[_n]='time_s phis_V phil_V Eeq_V eta_V etamid_V x_surface x_particle_average cs_surface_mol_m3 reaction_input_mol_m3 csmax_mol_m3 direct_Eeq_surface_V Isx_A_m2'.split()
for _n in ('axes_profile_N.csv','axes_profile_P.csv'):
    HEADERS[_n]='time_s coordinate_m x_surface x_particle_average Eeq_V etaMid_V phil_V domain_id'.split()
def need(ok, why):
    if not ok: raise EvidenceError(why)
def number(value):
    try: x=D(value)
    except Exception as e: raise EvidenceError('NUMBER') from e
    need(x.is_finite(),'NONFINITE');return x
def identity(p):
    p=Path(p)
    with p.open('rb') as f: h=hashlib.file_digest(f,'sha256').hexdigest()
    return {'path':p.resolve().as_posix(),'bytes':p.stat().st_size,'sha256':h}
def pinned(ref):
    got=identity(ref['path']);need(got==ref,'SOURCE_IDENTITY');return Path(ref['path'])
def rows(p):
    with Path(p).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);h=reader.fieldnames
        need(h and len(h)==len(set(h)),'CSV_HEADER')
        if Path(p).name in HEADERS:need(h==HEADERS[Path(p).name],'CSV_HEADER_CONTRACT')
        if Path(p).name.startswith('units_'):need(h==['tag','phase','expected','actual'],'UNIT_HEADER')
        for row in reader:
            need(None not in row and all(v is not None for v in row.values()),'CSV_WIDTH')
            yield row
def timed(p):
    result={};prior=None
    for row in rows(p):
        t=number(row['time_s']);need(prior is None or t>prior,'DUPLICATE_OR_UNORDERED_TIME')
        values={k:number(v) for k,v in row.items()};result[t]=values;prior=t
    need(result and next(iter(result))==0,'EMPTY_OR_TIME_ORIGIN');return result
def extract_tables(console_path,dest):
    dest=Path(dest);need(not dest.exists(),'TABLE_DEST_EXISTS');dest.mkdir()
    found={}
    with Path(console_path).open(encoding='utf-8-sig',errors='strict') as f:
        for line in f:
            if not line.startswith('AUDIT_TABLE_BASE64='):continue
            name,data=line.rstrip('\r\n').split('=',1)[1].split('|',1)
            need(re.fullmatch(r'[A-Za-z0-9_]+\.csv',name) is not None and name not in found,'TABLE_PATH_OR_DUPLICATE')
            raw=base64.b64decode(data,validate=True);p=dest/name
            with p.open('xb') as s:s.write(raw)
            found[name]=identity(p)
    need(found,'NO_TABLES');return found
def guard_evidence(c,g):
    ts=list(g);need(len(ts)>=3,'GUARD_TOO_FEW_STATES')
    threshold=number(c['threshold_mol_m3']);need(threshold==0,'NORMAL_THRESHOLD')
    need(number(c['maximum_physical_s'])==30,'NORMAL_END_CONTRACT')
    limit=number(c['limits']['minimum_consistency_mol_m3']);ties=[]
    keys=['electrolyte_guard','ocp_guard','surface_guard']
    for t,v in g.items():
        need(0<=t<=30,'GUARD_TIME_RANGE');need(v['threshold_mol_m3']==0,'THRESHOLD')
        vals=[v['ce_min_d%d_mol_m3'%d] for d in (1,2,3)];mn=min(vals)
        need(abs(v['ce_min_all_mol_m3']-mn)<=limit,'MINIMUM_OPERATOR_INCONSISTENT')
        need(all(v[k] in (0,1) for k in keys),'GUARD_BOOLEAN')
        need(v['electrolyte_guard']==D(int(v['ce_min_all_mol_m3']<=0)),'GUARD_VALUE')
        ties.append({'time_s':str(t),'exact_minimum_domains':[i+1 for i,x in enumerate(vals) if x==mn],
                     'near_tie_domains':[i+1 for i,x in enumerate(vals) if 0<x-mn<=number(c['limits']['near_tie_mol_m3'])]})
    need(all(g[ts[0]][k]==0 for k in keys),'INITIAL_GUARD')
    need(all(g[t][k]==0 for t in ts[:-1] for k in keys),'GUARD_BEFORE_FINAL')
    active=[k for k in keys if g[ts[-1]][k]==1]
    if active:
        minus,plus=ts[-2:];need(0<minus<plus<=30,'STOP_PAIR')
        if 'electrolyte_guard' in active:need(g[minus]['ce_min_all_mol_m3']>0>=g[plus]['ce_min_all_mol_m3'],'STOP_MINIMUM_CROSSING')
        status='PROTECTIVE_STOP_OBSERVED';safe=minus
    else:
        need(ts[-1]==30,'DID_NOT_REACH_30');status='NORMAL_30S_REACHED';safe=ts[-1]
    for a,b in zip(ts,ts[1:]):
        cap=D('.000125') if a<D('.1') else D('.1')
        need(b-a<=cap+D('1e-12')+cap*D('1e-9'),'ACCEPTED_STEP_CAP')
    return {'status':status,'final_time_s':str(ts[-1]),'safe_prefix_end_s':str(safe),
            't_minus':str(ts[-2]),'t_plus':str(ts[-1]),'active_guards':active,
            'stored_times_s':[str(x) for x in ts],'ties':ties,'threshold_mol_m3':'0'}
def rounded_contains(token,value):
    x=number(token);half=D(1).scaleb(x.as_tuple().exponent)/2
    return abs(x-value)<=half
def native_stop(c,batch,console,pair):
    fatal=r'/\*{3,}\s*Error\s*\*{3,}/|Error running java class\.|Security preference .*does not allow|OutOfMemoryError|Exception in thread'
    need(not re.search(fatal,batch+'\n'+console,re.I),'NATIVE_FATAL')
    pattern=r'Information: Stop condition fulfilled at t = ([0-9.eE+\-]+) \(([^\r\n]+)\)\.'
    hits=list(re.finditer(pattern,batch))
    normal=pair['status']=='NORMAL_30S_REACHED';last=number(pair['final_time_s'])
    need(len(hits)==(0 if normal else 1),'NATIVE_STOP_COUNT')
    opening=list(re.finditer(r'^<---- Time-Dependent Solver.*$',batch,re.M))
    closing=list(re.finditer(r'^----- Time-Dependent Solver.*-+>\s*$',batch,re.M))
    need(len(opening)==len(closing)==1 and opening[0].start()<closing[0].start(),'SOLVER_SECTION')
    if not normal:
        hit=hits[0]
        expected=[c['guard_stop_descriptions'][k] for k in pair['active_guards']]
        need(hit.group(2) in expected,'NATIVE_STOP_REASON')
        need(rounded_contains(hit.group(1),last),'NATIVE_STOP_TIME')
        need(opening[0].start()<hit.start()<closing[0].start(),'STOP_OUTSIDE_SOLVER')
    step_re=r'^\s*(\d+)\s+([0-9.eE+\-]+)\s+([0-9.eE+\-]+)\s+out\s+'
    step=list(re.finditer(step_re,batch[opening[0].end():closing[0].start()],re.M))
    need(step and rounded_contains(step[-1].group(2),last),'FINAL_NATIVE_STEP')
    stored=[number(x) for x in pair['stored_times_s']]
    need(len(step)==len(stored) and [int(x.group(1)) for x in step]==list(range(len(step))),'NATIVE_STORED_STEP_COUNT')
    need(all(rounded_contains(s.group(2),t) for s,t in zip(step,stored)),'NATIVE_STORED_TIME_BINDING')
    boundary=closing[0].end() if normal else hits[0].end()
    need(not re.search(step_re,batch[boundary:],re.M),'INTEGRATION_AFTER_TERMINATION')
    need(console.count('NORMAL30_PRODUCER_COMPLETE')==1 and console.count('PREFLIGHT_SOLVER_RETURNED=true')==1 and 'producer_failure.csv|' not in console,'PRODUCER_OUTPUT_FAILURE')
    return {'status':'NATIVE_NORMAL_END_MATCHED' if normal else 'NATIVE_PROTECTIVE_STOP_MATCHED',
            'reported_time':step[-1].group(2),'stop_reason':None if normal else hits[0].group(2),
            'no_integration_after_termination':True,'after_stop_export_allowed':True,
            'step_count':len(step),'rounding_note':'Native tokens rounded; exact stored end time from CSV.'}
def binding_evidence(c,folder,console):
    rr=list(rows(folder/'guard_binding.csv'));need(len(rr)==1,'GUARD_BINDING_MISSING')
    r=rr[0]
    need(r=={'electrolyte_expression':c['guard_expression'],'stop_storage':'stepbefore_stepafter','active':'on','terminate_on':'true','threshold_SI':'0.0'},'GUARD_BINDING_VALUE')
    for tag,selection in [('minguardall','[1, 2, 3]'),('minguard1','[1]'),('minguard2','[2]'),('minguard3','[3]')]:
        expected='ELECTROLYTE_COUPLING='+tag+'|dimension=1|entities='+selection+'|points=lagrange|lagrange=5'
        need(console.splitlines().count(expected)==1,'COUPLING_BINDING')
    return 'PASS'
def coverage(c,target,baseline,minus):
    comparison_end=min(D(5),minus)
    requested={number(x) for x in c['baseline_requested_times_s'] if number(x)<=comparison_end}
    all_actual=set(target);actual={t for t in target if t<=comparison_end};base=set(baseline)
    common=sorted(actual&base);full=sorted(all_actual&base)
    missing_target=sorted(requested-actual);missing_base=sorted(requested-base)
    strict={number(x) for x in c['requested_times_s'] if number(x)<=minus}
    missing_strict=sorted(strict-all_actual)
    info={'status':'PASS','comparison_end_s':str(comparison_end),'expected_requested':[str(x) for x in sorted(requested)],
          'common_stored':[str(x) for x in common],'missing_target':[str(x) for x in missing_target],
          'missing_baseline':[str(x) for x in missing_base],'target_noncommon':[str(x) for x in sorted(actual-base)],
          'common_count':len(common),'common_first':str(common[0]) if common else None,'common_last':str(common[-1]) if common else None,
          'full_intersection':[str(x) for x in full],'full_intersection_count':len(full),
          'strict_requested_through_safe_end':[str(x) for x in sorted(strict)],'missing_strict_requested':[str(x) for x in missing_strict],
          'policy':'Exact intersection; compare <=min(5,safe-prefix end). No interpolation or nearest substitution.'}
    need(not missing_target and not missing_base and not missing_strict,'STRICT_REQUEST_TIME_MISSING:'+json.dumps(info))
    need(len(requested)>=2 and any(x>0 for x in requested),'INSUFFICIENT_REQUEST_PREFIX:'+json.dumps(info))
    need(len(common)>=2 and common[0]==0 and common[-1]>0,'EMPTY_OR_ZERO_ONLY_COMMON:'+json.dumps(info))
    return common,info
def profile(p,expected_times,coordinates,domain,limit):
    expected=[number(x) for x in coordinates];need(len(expected)==241,'COORDINATE_CONTRACT')
    result={};last=None;idx=0
    for raw in rows(p):
        v={k:number(x) for k,x in raw.items()};t=v['time_s']
        if t!=last:
            if last is not None:need(idx==241,'PROFILE_COUNT')
            need(last is None or t>last,'PROFILE_TIME_ORDER');need(t in expected_times,'PROFILE_UNEXPECTED_TIME')
            result[t]=[];idx=0;last=t
        need(idx<241 and abs(v['coordinate_m']-expected[idx])<=limit and v['domain_id']==domain,'PROFILE_COORD_DOMAIN')
        lo,hi=(D(0),D('.98')) if domain==1 else (D('.2228930343076256'),D('.983245033354389'))
        need(lo<=v['x_surface']<=hi and 0<v['x_surface']<1,'PROFILE_SURFACE_RANGE')
        result[t].append(v['x_surface']);idx+=1
    need(idx==241 and set(result)==set(expected_times),'PROFILE_MISSING_TIME_OR_COUNT');return result
def units_evidence(folder):
    configs={'eguard':['s']+['mol/m^3']*5+['1']*3,'nglobal':['s']+['mol/m^2']*3+['1']*7+['A/m^2']*3,
             'point1':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
             'point4':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
             'MinLinece':['s','mol/m^3'],'MaxLinece':['s','mol/m^3'],'profiletimes':['s'],
             'profileN':['s','m','1','1','V','V','V','1'],'profileP':['s','m','1','1','V','V','V','1']}
    for tag,u in configs.items():
        for phase in (['inferred','configured','evaluated'] if tag=='eguard' else ['configured','evaluated']):
            expected=u.copy()
            if phase!='configured':
                for i in ([6,7,8] if tag=='eguard' else [10] if tag=='nglobal' else [7] if tag in ('profileN','profileP') else []):expected[i]=''
            rr=list(rows(folder/('units_'+tag+'_'+phase+'.csv')));need(len(rr)==1,'UNIT_ROW_COUNT')
            r=rr[0];text='['+', '.join(expected)+']'
            need(r=={'tag':tag,'phase':phase,'expected':text,'actual':text},'UNIT_STAGE')
    return 'PASS'
def numeric(c,folder,g,minus):
    names=['preflight_global.csv','preflight_boundary1.csv','preflight_boundary4.csv']
    data={n:timed(folder/n) for n in names};times=list(g)
    need(all(list(x)==times for x in data.values()),'NUMERIC_TIME_SET')
    base={n:timed(pinned(c['baseline_files'][n])) for n in names}
    need(all(list(x)==list(base[names[0]]) for x in base.values()),'BASELINE_TIME_SET')
    common,info=coverage(c,times,base[names[0]],minus)
    glob,n,p=(data[n] for n in names);bn,bp=base[names[1]],base[names[2]]
    L0=sum(glob[D(0)][k] for k in ('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2'));need(L0>0,'LI_INITIAL')
    components={}
    for key in ('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2'):
        current=glob[D(0)][key];reference=base[names[0]][D(0)][key]
        need(current>0 and reference>0,'INITIAL_LI_COMPONENT_POSITIVE')
        delta=abs(current-reference);limit=number(c['limits']['initial_Li_absolute_mol_m2'])
        need(limit==D('1e-9'),'INITIAL_LI_LIMIT')
        need(delta<=limit,'INITIAL_LI_COMPONENT')
        components[key]={'status':'PASS','current':str(current),'baseline':str(reference),'absolute_delta':str(delta),'unit':'mol/m^2','absolute_limit':'1e-9','relative_delta_reference_only':str(delta/reference)}
    li=voltage=deltaV=dx=D(0)
    for t in times:
        v=glob[t];need(v['ocp_guard']==0,'GLOBAL_OCP_GUARD')
        for lo,hi,col in [(D(0),D('.98'),'N'),(D('.2228930343076256'),D('.983245033354389'),'P')]:
            need(lo<=v['xsurf_'+col+'_min']<=v['xsurf_'+col+'_max']<=hi and v['xsurf_'+col+'_min']>0 and v['xsurf_'+col+'_max']<1,'GLOBAL_SURFACE_RANGE')
        Lt=sum(v[k] for k in ('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2'));li=max(li,abs((Lt-L0)/L0))
        V=p[t]['phis_V']-n[t]['phis_V'];parts=sum(p[t][k]-n[t][k] for k in ('Eeq_V','etamid_V','phil_V'));voltage=max(voltage,abs(V-parts))
        if t in common:deltaV=max(deltaV,abs(V-(bp[t]['phis_V']-bn[t]['phis_V'])))
    need(li<=number(c['limits']['relative_Li']),'LI_DRIFT');need(voltage<=number(c['limits']['voltage_identity_V']),'VOLTAGE_IDENTITY')
    for electrode,domain in [('N',1),('P',3)]:
        name='axes_profile_'+electrode+'.csv'
        cur=profile(folder/name,times,c['coordinates'][electrode],domain,number(c['limits']['coordinate_m']))
        old=profile(pinned(c['baseline_files'][name]),base[names[0]],c['coordinates'][electrode],domain,number(c['limits']['coordinate_m']))
        for t in common:dx=max(dx,max(abs(a-b) for a,b in zip(cur[t],old[t])))
    need(deltaV<=number(c['limits']['voltage_V']) and dx<=number(c['limits']['surface_x']),'SAMPLE_TOLERANCE')
    return {'status':'PASS','coverage':info,'initial_Li_components':components,'late_interval':late_summary(glob,n,p,g),'maximum_voltage_delta_V':str(deltaV),'maximum_surface_delta':str(dx),'maximum_Li_relative_drift':str(li),'maximum_voltage_identity_V':str(voltage),'terminal_times_excluded_from_comparison':[str(t) for t in times[-2:] if t not in common]}
def incomplete_result(state=None):
    state=state or {}
    return {'limited_result':'INCOMPLETE','diagnostic':'INCOMPLETE','sampled_comparison':'INCOMPLETE',
            'preservation':state.get('preservation','INCOMPLETE'),'process_cleanup':state.get('process_cleanup','INCOMPLETE'),
            'policy_preservation':state.get('policy_preservation','INCOMPLETE'),'errors':[],
            'overall':'INCOMPLETE','normal_gate':'INCOMPLETE','effective_policy':'UNVERIFIED','native_approved_by_this_result':False}

def analyze(c,folder,batch,console,state):
    result=incomplete_result(state);folder=Path(folder)
    try:
        binding_evidence(c,folder,console);result['runtime_settings']=runtime_evidence(c,folder)
        g=timed(folder/'electrolyte_guard.csv');termination=guard_evidence(c,g)
        result['termination']=termination;result['native_termination']=native_stop(c,batch,console,termination)
        result['diagnostic']=termination['status']
    except Exception as e:result['errors'].append({'axis':'termination','type':type(e).__name__,'error':str(e)});return result
    try:
        units_evidence(folder)
        with localcontext() as ctx:
            ctx.prec=50;result['numeric']=numeric(c,folder,g,number(termination['safe_prefix_end_s']))
        result['sampled_comparison']='PASS'
    except Exception as e:result['errors'].append({'axis':'numeric','type':type(e).__name__,'error':str(e)})
    accepted=(not result['errors'] and state.get('status')=='NATIVE_RETURN_READY' and state.get('errors')==[]
              and result['sampled_comparison']=='PASS' and all(result[k]=='PASS' for k in ('preservation','process_cleanup','policy_preservation')))
    if accepted:
        result['limited_result']='NORMAL_30S_DIAGNOSTIC_COMPLETE' if result['diagnostic']=='NORMAL_30S_REACHED' else 'PROTECTED_STOP_30S_INCOMPLETE'
    # Observed protection survives numeric failure in diagnostic/termination; never a normal success.
    return result

def runtime_evidence(c,folder):
    settings={}
    for r in rows(folder/'axes_runtime_settings.csv'):
        need(set(r)=={'key','actual_value'} and r['key'] not in settings,'RUNTIME_SETTINGS_SCHEMA')
        settings[r['key']]=r['actual_value']
    need(settings.get('study_tlist','').split()==c['requested_times_s'],'RUNTIME_TLIST')
    for k,v in c['runtime_settings_required'].items():need(settings.get(k)==v,'RUNTIME_SETTING:'+k)
    return {'status':'PASS','requested_count':len(c['requested_times_s']),'settings':{k:settings[k] for k in c['runtime_settings_required']}}


def late_summary(glob,n,p,g):
    ts=[t for t in g if t>D(5)]
    if not ts:return {'status':'NOT_REACHED','count':0,'claim':'No >5 s stored states; not a 30 s completion.'}
    series={'voltage_V':{t:p[t]['phis_V']-n[t]['phis_V'] for t in ts}}
    for k in ('ce_min_all_mol_m3','ce_min_d1_mol_m3','ce_min_d2_mol_m3','ce_min_d3_mol_m3','electrolyte_guard','ocp_guard','surface_guard'):
        series[k]={t:g[t][k] for t in ts}
    for k in ('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2','xavg_N','xavg_P','xsurf_N_min','xsurf_N_max','xsurf_P_min','xsurf_P_max'):
        series[k]={t:glob[t][k] for t in ts}
    return {'status':'OBSERVED','count':len(ts),'first_time_s':str(ts[0]),'last_time_s':str(ts[-1]),
            'claim':'Stored-state diagnostic only. No >5 s baseline equivalence, physical validation or long-time convergence.',
            'metrics':{k:{'first':str(v[ts[0]]),'last':str(v[ts[-1]]),'min':str(min(v.values())),'max':str(max(v.values()))} for k,v in series.items()}}

