"""UNEXECUTED candidate: bmin640 150 s/protected-stop consumer (particle Nel 640 vs NORMAL480 run/tables, 120-150 s window). No COMSOL/import/process calls.
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
for _n in ('preflight_MinLine_ce.csv','preflight_MaxLine_ce.csv'):
    HEADERS[_n]='time_s ce_mol_m3'.split()
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
    need(number(c['maximum_physical_s'])==150,'NORMAL_END_CONTRACT')
    limit=number(c['limits']['minimum_consistency_mol_m3']);ties=[]
    keys=['electrolyte_guard','ocp_guard','surface_guard']
    for t,v in g.items():
        need(0<=t<=150,'GUARD_TIME_RANGE');need(v['threshold_mol_m3']==0,'THRESHOLD')
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
        minus,plus=ts[-2:];need(0<minus<plus<=150,'STOP_PAIR')
        if 'electrolyte_guard' in active:need(g[minus]['ce_min_all_mol_m3']>0>=g[plus]['ce_min_all_mol_m3'],'STOP_MINIMUM_CROSSING')
        status='PROTECTIVE_STOP_OBSERVED';safe=minus
    else:
        need(ts[-1]==150,'DID_NOT_REACH_150');status='NORMAL_150S_REACHED';safe=ts[-1]
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
    normal=pair['status']=='NORMAL_150S_REACHED';last=number(pair['final_time_s'])
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
    need(console.count('BMIN640_PRODUCER_COMPLETE')==1 and console.count('PREFLIGHT_SOLVER_RETURNED=true')==1 and 'producer_failure.csv|' not in console,'PRODUCER_OUTPUT_FAILURE')
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
def window_coverage(c,target,baseline,minus):
    start,end=(number(c['comparison_window_s'][k]) for k in ('start','end'))
    need(start==120 and end==150 and number(c['maximum_physical_s'])==end,'WINDOW_CONTRACT')
    requested=[number(x) for x in c['requested_times_s']]
    need(len(requested)==len(set(requested))==1637 and requested[0]==0 and requested[-1]==end,'REQUEST_CONTRACT')
    primary=[t for t in requested if start<=t<=end]
    need(len(primary)==c['primary_comparison_count']==301 and [str(t) for t in primary]==c['primary_comparison_times_s'],'PRIMARY_CONTRACT')
    actual=set(target);base=set(baseline);chosen=set(primary)
    reach=[t for t in primary if t<=minus];strict=[t for t in requested if t<=minus]
    missing_target=[t for t in reach if t not in actual];missing_base=[t for t in primary if t not in base]
    missing_strict=[t for t in strict if t not in actual]
    aux=sorted(t for t in actual&base if start<=t<=min(end,minus) and t not in chosen)
    outside=[t for t in requested if t<start and t<=minus and t in actual and t in base]
    info={'status':'PASS','window_start_s':str(start),'window_end_s':str(end),'safe_prefix_end_s':str(minus),
          'primary_expected':[str(t) for t in primary],'primary_compared':[str(t) for t in reach],'primary_compared_count':len(reach),
          'primary_complete':len(reach)==len(primary),'missing_target':[str(t) for t in missing_target],'missing_baseline':[str(t) for t in missing_base],
          'auxiliary_common_stored':[str(t) for t in aux],'auxiliary_count':len(aux),'outside_window_requested_common_count':len(outside),
          'strict_requested_through_safe_end':[str(t) for t in strict],'missing_strict_requested':[str(t) for t in missing_strict],
          'policy':'Exact membership. Primary = contract requested times in [120,150] (301), judged; auxiliary = extra exact common stored times in the window, reported separately, never judged; outside-window requested times are observation only. No interpolation, nearest substitution or rounding match.'}
    need(not missing_target and not missing_base and not missing_strict,'STRICT_REQUEST_TIME_MISSING:'+json.dumps(info))
    return reach,aux,outside,info
def extreme(items):
    # First maximum |delta| in iteration order (later ties do not replace it); None for an empty set.
    best=None
    for d,t,j in items:
        if best is None or abs(d)>abs(best[0]):best=(d,t,j)
    if best is None:return None
    return {'maximum_absolute':str(abs(best[0])),'signed_delta':str(best[0]),'time_s':str(best[1]),'coordinate_index':best[2]}
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
    need(number(c['limits']['voltage_V'])==D('0.001') and number(c['limits']['surface_x'])==D('0.0001'),'LIMIT_CONTRACT')
    names=['preflight_global.csv','preflight_boundary1.csv','preflight_boundary4.csv']
    data={n:timed(folder/n) for n in names};times=list(g)
    need(all(list(x)==times for x in data.values()),'NUMERIC_TIME_SET')
    base={n:timed(pinned(c['baseline_files'][n])) for n in names}
    need(all(list(x)==list(base[names[0]]) for x in base.values()),'BASELINE_TIME_SET')
    primary,aux,outside,info=window_coverage(c,times,base[names[0]],minus)
    bg=timed(pinned(c['baseline_files']['electrolyte_guard.csv']))
    need(list(bg)==list(base[names[0]]),'BASELINE_GUARD_TIME_SET')
    lines={}
    for kind in ('MinLine','MaxLine'):
        name='preflight_'+kind+'_ce.csv';lines[kind]=(timed(folder/name),timed(pinned(c['baseline_files'][name])))
        need(list(lines[kind][0])==times and list(lines[kind][1])==list(bg),'ELECTROLYTE_LINE_TIME_SET')
    glob,n,p=(data[n] for n in names);bglob,bn,bp=(base[n] for n in names)
    li_keys=('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2')
    L0=sum(glob[D(0)][k] for k in li_keys);need(L0>0,'LI_INITIAL')
    components={}
    for key in li_keys:
        current=glob[D(0)][key];reference=bglob[D(0)][key]
        need(current>0 and reference>0,'INITIAL_LI_COMPONENT_POSITIVE')
        delta=abs(current-reference);limit=number(c['limits']['initial_Li_absolute_mol_m2'])
        need(limit==D('1e-9'),'INITIAL_LI_LIMIT')
        need(delta<=limit,'INITIAL_LI_COMPONENT')
        components[key]={'status':'PASS','current':str(current),'baseline':str(reference),'absolute_delta':str(delta),'unit':'mol/m^2','absolute_limit':'1e-9','relative_delta_reference_only':str(delta/reference)}
    li=voltage=D(0)
    for t in times:
        v=glob[t];need(v['ocp_guard']==0,'GLOBAL_OCP_GUARD')
        for lo,hi,col in [(D(0),D('.98'),'N'),(D('.2228930343076256'),D('.983245033354389'),'P')]:
            need(lo<=v['xsurf_'+col+'_min']<=v['xsurf_'+col+'_max']<=hi and v['xsurf_'+col+'_min']>0 and v['xsurf_'+col+'_max']<1,'GLOBAL_SURFACE_RANGE')
        Lt=sum(v[k] for k in li_keys);li=max(li,abs((Lt-L0)/L0))
        V=p[t]['phis_V']-n[t]['phis_V'];parts=sum(p[t][k]-n[t][k] for k in ('Eeq_V','etamid_V','phil_V'));voltage=max(voltage,abs(V-parts))
    need(li<=number(c['limits']['relative_Li']),'LI_DRIFT');need(voltage<=number(c['limits']['voltage_identity_V']),'VOLTAGE_IDENTITY')
    ce_keys=['ce_min_all_mol_m3','ce_min_d1_mol_m3','ce_min_d2_mol_m3','ce_min_d3_mol_m3']
    sets=(('primary',primary),('auxiliary',aux),('outside_window_observation',outside));windows={}
    for key,ts in sets:
        w={'time_count':len(ts),
           'voltage_V':extreme(((p[t]['phis_V']-n[t]['phis_V'])-(bp[t]['phis_V']-bn[t]['phis_V']),t,None) for t in ts),
           'total_Li_mol_m2':extreme((sum(glob[t][k] for k in li_keys)-sum(bglob[t][k] for k in li_keys),t,None) for t in ts)}
        for k in ce_keys:w[k]=extreme((g[t][k]-bg[t][k],t,None) for t in ts)
        for kind,(cur_l,old_l) in lines.items():w['ce_'+kind]=extreme((cur_l[t]['ce_mol_m3']-old_l[t]['ce_mol_m3'],t,None) for t in ts)
        windows[key]=w
    for electrode,domain in [('N',1),('P',3)]:
        name='axes_profile_'+electrode+'.csv'
        cur=profile(folder/name,times,c['coordinates'][electrode],domain,number(c['limits']['coordinate_m']))
        old=profile(pinned(c['baseline_files'][name]),base[names[0]],c['coordinates'][electrode],domain,number(c['limits']['coordinate_m']))
        for key,ts in sets:
            m=extreme((a-b,t,j) for t in ts for j,(a,b) in enumerate(zip(cur[t],old[t])))
            if m is not None:m['coordinate_m']=c['coordinates'][electrode][m['coordinate_index']]
            windows[key]['surface_x_'+electrode]=m
    return {'status':'PASS','coverage':info,'windows':windows,'initial_Li_components':components,
            'maximum_Li_relative_drift':str(li),'maximum_voltage_identity_V':str(voltage),
            'sign_convention':'delta = candidate (particle Nel 640) minus NORMAL480 (particle Nel 320) at identical stored times; surface deltas pointwise over the 241 contract coordinates per electrode',
            'judged_window':'primary only; auxiliary and outside_window_observation are never judged',
            'observation_tolerance':None}
def incomplete_result(state=None):
    state=state or {}
    return {'limited_result':'INCOMPLETE','diagnostic':'INCOMPLETE','sampled_comparison':'INCOMPLETE',
            'preservation':state.get('preservation','INCOMPLETE'),'process_cleanup':state.get('process_cleanup','INCOMPLETE'),
            'policy_preservation':state.get('policy_preservation','INCOMPLETE'),'errors':[],
            'overall':'INCOMPLETE','normal_gate':'INCOMPLETE','effective_policy':'UNVERIFIED','native_approved_by_this_result':False,
            'native_completion':'NOT_ESTABLISHED','evidence_validity':'INVALID','mesh_comparison':'INCONCLUSIVE'}

def analyze(c,folder,batch,console,state):
    result=incomplete_result(state);folder=Path(folder)
    try:
        # Termination first, so native_completion stays a separate field from the configuration evidence (B-min v2 section 6).
        g=timed(folder/'electrolyte_guard.csv');termination=guard_evidence(c,g)
        result['termination']=termination;result['native_termination']=native_stop(c,batch,console,termination)
        result['diagnostic']=termination['status']
    except Exception as e:result['errors'].append({'axis':'termination','type':type(e).__name__,'error':str(e)});return three_fields(c,result,state)
    try:
        binding_evidence(c,folder,console);result['runtime_settings']=runtime_evidence(c,folder)
        result['mesh_readback']=mesh_evidence(c,batch,console)
    except Exception as e:result['errors'].append({'axis':'configuration','type':type(e).__name__,'error':str(e)});return three_fields(c,result,state)
    try:
        units_evidence(folder)
        with localcontext() as ctx:
            ctx.prec=50;result['numeric']=numeric(c,folder,g,number(termination['safe_prefix_end_s']))
        result['sampled_comparison']='PASS'
    except Exception as e:result['errors'].append({'axis':'numeric','type':type(e).__name__,'error':str(e)})
    accepted=(not result['errors'] and state.get('status')=='NATIVE_RETURN_READY' and state.get('errors')==[]
              and result['sampled_comparison']=='PASS' and all(result[k]=='PASS' for k in ('preservation','process_cleanup','policy_preservation')))
    if accepted:
        result['limited_result']='BMIN640_150S_COMPARISON_COMPLETE' if result['diagnostic']=='NORMAL_150S_REACHED' else 'PROTECTED_STOP_150S_INCOMPLETE'
    # Observed protection survives numeric failure in diagnostic/termination; never a normal success.
    return three_fields(c,result,state)
def three_fields(c,result,state):
    # B-min v2 section 6: three separate fields. A limit excess is a valid comparison result, never a solver failure.
    native=result.get('native_termination') or {}
    if result['diagnostic']=='NORMAL_150S_REACHED' and native.get('status')=='NATIVE_NORMAL_END_MATCHED' and state.get('status')=='NATIVE_RETURN_READY' and state.get('errors')==[]:
        result['native_completion']='NORMAL_150S_COMPLETED'
    elif result['diagnostic']=='PROTECTIVE_STOP_OBSERVED' and native.get('status')=='NATIVE_PROTECTIVE_STOP_MATCHED':
        result['native_completion']='PROTECTIVE_STOP'
    else:
        result['native_completion']='NOT_ESTABLISHED'
    result['native_completion_cause']=None if result['native_completion']=='NORMAL_150S_COMPLETED' else {
        'diagnostic':result['diagnostic'],'native_status':native.get('status'),'state_status':state.get('status'),'state_errors':state.get('errors'),
        'termination_errors':[e for e in result['errors'] if e.get('axis')=='termination']}
    valid=result['limited_result']=='BMIN640_150S_COMPARISON_COMPLETE'
    result['evidence_validity']='VALID' if valid else 'INVALID'
    result['evidence_failures']=[] if valid else list(result['errors'])+[{'stage':'native_state','status':state.get('status'),'errors':state.get('errors')}]
    if valid:
        pw=result['numeric']['windows']['primary'];lv=number(c['limits']['voltage_V']);lx=number(c['limits']['surface_x'])
        within=number(pw['voltage_V']['maximum_absolute'])<=lv and all(number(pw['surface_x_'+e]['maximum_absolute'])<=lx for e in ('N','P'))
        result['mesh_comparison']='WITHIN_LIMITS_THIS_WINDOW' if within else 'EXCEEDS_LIMITS'
    else:
        result['mesh_comparison']='INCONCLUSIVE'
    result['mesh_comparison_rule']=c['comparison_rule']
    result['mesh_comparison_scope']='This input, particle radial mesh 320 vs 640 only, 120-150 s primary window, declared sample. Not an error bound, convergence order, true-solution accuracy, physical-mesh, late-480 s or finite-sigma claim.'
    result['field_authority']='Consumer values are provisional: the parent POST_WRITE record decides the final three fields after the entry, budget, delivery and record checks.'
    return result

def runtime_evidence(c,folder):
    settings={}
    for r in rows(folder/'axes_runtime_settings.csv'):
        need(set(r)=={'key','actual_value'} and r['key'] not in settings,'RUNTIME_SETTINGS_SCHEMA')
        settings[r['key']]=r['actual_value']
    need(settings.get('study_tlist','').split()==c['requested_times_s'],'RUNTIME_TLIST')
    for k,v in c['runtime_settings_required'].items():need(settings.get(k)==v,'RUNTIME_SETTING:'+k)
    base={}
    for r in rows(pinned(c['baseline_files']['axes_runtime_settings.csv'])):
        need(set(r)=={'key','actual_value'} and r['key'] not in base,'BASELINE_SETTINGS_SCHEMA')
        base[r['key']]=r['actual_value']
    need(set(settings)==set(base),'RUNTIME_SETTING_KEYS_VS_NORMAL480')
    need(base['study_tlist'].split()[:len(c['requested_times_s'])]==c['requested_times_s'],'BASELINE_TLIST_PREFIX')
    diff=sorted(k for k in base if k!='study_tlist' and settings[k]!=base[k]);need(not diff,'RUNTIME_SETTING_VS_NORMAL480:'+','.join(diff))
    return {'status':'PASS','requested_count':len(c['requested_times_s']),'settings':{k:settings[k] for k in c['runtime_settings_required']},
            'baseline_comparison':{'status':'PASS','keys':len(base),'allowed_difference':['study_tlist = 1637-entry prefix of the NORMAL480 list']}}
def mesh_evidence(c,batch,console):
    lines=console.splitlines()
    for expected in c['mesh_readback_required']:need(lines.count(expected)==1,'MESH_READBACK:'+expected)
    # BMIN-N2: the transient DOF read-back is required I-3 evidence, taken only from the single Time-Dependent Solver section.
    opening=list(re.finditer(r'^<---- Time-Dependent Solver.*$',batch,re.M))
    closing=list(re.finditer(r'^----- Time-Dependent Solver.*-+>\s*$',batch,re.M))
    need(len(opening)==len(closing)==1 and opening[0].start()<closing[0].start(),'SOLVER_SECTION')
    pattern=r'Number of degrees of freedom solved for: (\d+) \(plus (\d+) internal DOFs\)\.'
    section=batch[opening[0].end():closing[0].start()]
    mentions=[x for x in section.splitlines() if 'Number of degrees of freedom' in x]
    need(len(mentions)==1,'TRANSIENT_DOF_READBACK_COUNT:'+str(len(mentions)))
    hit=re.search(pattern,mentions[0]);need(hit is not None,'TRANSIENT_DOF_READBACK_FORMAT')
    solved,internal=int(hit.group(1)),int(hit.group(2));need(solved>0,'TRANSIENT_DOF_READBACK_VALUE')
    want={'solved':c['expected_transient_dof']['solved'],'internal':c['expected_transient_dof']['internal']}
    outside=[{'solved':int(a),'internal':int(b)} for a,b in re.findall(pattern,batch[:opening[0].end()]+'\n'+batch[closing[0].start():])]
    same=solved==want['solved'] and internal==want['internal']
    return {'status':'PASS','required_lines':c['mesh_readback_required'],
            'transient_dof':{'solved':solved,'internal':internal,'line':mentions[0].strip()},
            'expected_transient_dof':want,'transient_dof_matches_expected':same,
            'transient_dof_difference':{'solved':solved-want['solved'],'internal':internal-want['internal']},
            'review_note':None if same else 'Observed transient DOF differs from the extrapolated expectation (2045 + 242*640); state the cause in the result review. Not a gate.',
            'dof_outside_transient_section':outside,
            'dof_policy':'I-3: exactly one well-formed DOF line inside the single Time-Dependent Solver section is required (missing, outside-only, ambiguous or malformed is incomplete); a difference from the extrapolated expectation is recorded, not a gate.'}
