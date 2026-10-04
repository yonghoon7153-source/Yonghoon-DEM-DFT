"""Recipient-owned ZIP/data review. Never imports or executes supplied code."""
import csv, hashlib, io, json, math, re, stat, sys, zipfile
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOWNLOADS = Path('C:/Users/Administrator/Downloads')
MAIN = DOWNLOADS / 'COMSOL63_RTOL30_NATIVE_RESULT_20261004.zip'
SUPP = DOWNLOADS / 'RTOL30_NATIVE_DELIVERY_SUPPLEMENT_20261004.zip'
getcontext().prec = 50

def sha(b): return hashlib.sha256(b).hexdigest()
def identity(p):
    with p.open('rb') as f: h = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'file': p.name, 'bytes': p.stat().st_size, 'sha256': h}
def js(z, n): return json.loads(z.read(n).decode('utf-8-sig'))
def save(n, v): (ROOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
def compact(v):
    if isinstance(v, dict): return {k:compact(x) for k,x in v.items()}
    if isinstance(v,list): return {'count':len(v),'first':v[:2],'last':v[-1:]} if len(v)>8 else [compact(x) for x in v]
    return v

def verify(p):
    with zipfile.ZipFile(p) as z:
        entries=z.infolist(); names=[i.filename for i in entries]
        assert len(names)==len(set(n.casefold() for n in names))
        assert all(not n.startswith(('/', '\\')) and ':' not in n and '..' not in n.replace('\\','/').split('/') for n in names)
        assert all(not stat.S_ISLNK(i.external_attr>>16) for i in entries)
        manifest=js(z,'MANIFEST.json'); items=manifest['files']
        assert len(items)==len(set(x['file'] for x in items))
        assert set(names)=={x['file'] for x in items}|{'MANIFEST.json'}
        for item in items:
            h=hashlib.sha256(); count=0
            with z.open(item['file']) as stream:
                while b:=stream.read(1024*1024): h.update(b);count+=len(b)
            assert count==item['bytes'] and h.hexdigest()==item['sha256'],item['file']
        return dict(identity(p),payload_count=len(items),entries=len(names),uncompressed_bytes=sum(i.file_size for i in entries),manifest_sha256=sha(z.read('MANIFEST.json')),CRC_exact_set_path_case_size_SHA=True)

def perform_verify():
    result={'archives':[verify(MAIN),verify(SUPP)],'provided_code_executed':False}
    assert result['archives'][0]['sha256']=='1f879c8805491cefdc990b666bfe1a6a8e74d7ef47beb84f7e6ba1a66c14e3f5'
    assert result['archives'][1]['sha256']=='778618d3d92beb91aa02e4cd23570af3dbfbc868e0bb1f019ef0abbe27de7e8b'
    save('ARCHIVE_AUDIT.json',result)
    print(json.dumps(result,ensure_ascii=False))

def dump(names):
    with zipfile.ZipFile(MAIN) as z, zipfile.ZipFile(SUPP) as s:
        for name in names:
            source=s if name.startswith('supp:') else z; name=name.removeprefix('supp:')
            print('\nFILE '+name)
            if name.endswith('.json'): print(json.dumps(compact(js(source,name)),ensure_ascii=False,indent=2))
            else: print(source.read(name).decode('utf-8-sig'))

def rows(z,n):
    with z.open(n) as b, io.TextIOWrapper(b,encoding='utf-8-sig',newline='') as f:
        yield from csv.DictReader(f)

def numeric_table(z,n):
    out={}; prev=None
    for r in rows(z,n):
        d={k:Decimal(v) for k,v in r.items()}
        assert all(v.is_finite() for v in d.values()),n
        t=d['time_s'];assert t not in out and (prev is None or t>prev),n
        out[t]=d;prev=t
    return out

def maximum_update(s,delta,where):
    a=abs(delta)
    if not s or a>s['maximum_absolute_delta']:
        s.clear();s.update(maximum_absolute_delta=a,signed_delta_candidate_minus_reference=delta,first_argmax=where,equal_maximum_count=1)
    elif a==s['maximum_absolute_delta']:s['equal_maximum_count']+=1

def profile_groups(z,n,meta):
    prev=None; group=[]; coords0=None; times=[]; count=0
    def validate(group):
        nonlocal coords0,count
        coords=[(r['coordinate_m'],r['domain_id']) for r in group]
        assert len(coords)==241 and len(set(coords))==241,n
        if coords0 is None:coords0=coords
        assert coords==coords0,n
        count+=len(group)
    for r in rows(z,n):
        r={k:Decimal(v) for k,v in r.items()}; assert all(v.is_finite() for v in r.values()),n
        assert 0<=r['x_surface']<=1 and 0<=r['x_particle_average']<=1,n
        t=r['time_s']
        if prev is not None and t!=prev:
            assert t>prev,n
            validate(group);times.append(prev);yield prev,group;group=[]
        prev=t;group.append(r)
    if group:validate(group);times.append(prev);yield prev,group
    meta.update(rows=count,times=times,coordinates=coords0)

def perform_numeric():
    out={'method':'Independent recipient Decimal50 arithmetic on saved CSV only; supplied analyzer never imported or called.'}
    with zipfile.ZipFile(MAIN) as z:
        c=js(z,'candidate/CONTRACT.json');diag=js(z,'run/DIAGNOSTIC_RESULT.json')
        req=set(map(Decimal,c['requested_times_s'])); assert len(req)==437
        tables={}
        for label,prefix in [('target','run/tables/'),('NORMAL30','baseline/'),('B020','baseline/B020_')]:
            tables[label]={k:numeric_table(z,prefix+k+'.csv') for k in ['preflight_global','preflight_boundary1','preflight_boundary4','electrolyte_guard']}
            tlist=list(tables[label]['preflight_global'])
            assert all(list(x)==tlist for x in tables[label].values())
        tg=tables['target'];tt=set(tg['preflight_global']); assert min(tt)==0 and max(tt)==30 and req<=tt
        settings={r['key']:r['actual_value'] for r in rows(z,'run/tables/axes_runtime_settings.csv')}
        assert all(settings[k]==v for k,v in c['runtime_settings_required'].items())
        assert set(map(Decimal,settings['study_tlist'].split()))==req
        out['runtime_settings_match']=True
        out['coverage']={}
        comparisons={}
        for label,base in [('NORMAL30',tables['NORMAL30']),('B020',tables['B020'])]:
            bt=set(base['preflight_global']); common=tt&bt
            expected=set(map(Decimal,c['b020_requested_times_s'] if label=='B020' else c['requested_times_s']))
            assert expected<=common
            out['coverage'][label]={'target_saved':len(tt),'reference_saved':len(bt),'exact_common':len(common),'mandatory_requested':len(expected),'target_noncommon':len(tt-bt),'reference_noncommon':len(bt-tt),'no_interpolation':True}
            comparisons[label]={key:{'voltage':{},'surface':{},'common_time_count':sum(predicate(t) for t in common)} for key,predicate in [('0_to_5_inclusive',lambda t:t<=5),('after_5_to_30',lambda t:t>5),('0_to_30_inclusive',lambda t:True)]}
            for t in sorted(common):
                dv=(tg['preflight_boundary4'][t]['phis_V']-tg['preflight_boundary1'][t]['phis_V'])-(base['preflight_boundary4'][t]['phis_V']-base['preflight_boundary1'][t]['phis_V'])
                for key in ['0_to_30_inclusive','0_to_5_inclusive' if t<=5 else 'after_5_to_30']:
                    maximum_update(comparisons[label][key]['voltage'],dv,{'time_s':t})
        profile_meta={};matched=Counter()
        for e in ['N','P']:
            metas={k:{} for k in ['target','NORMAL30','B020']}
            refs={k:iter(profile_groups(z,'baseline/'+('B020_' if k=='B020' else '')+'axes_profile_'+e+'.csv',metas[k])) for k in ['NORMAL30','B020']}
            curs={k:next(it,None) for k,it in refs.items()}
            for t,group in profile_groups(z,'run/tables/axes_profile_'+e+'.csv',metas['target']):
                assert t in tt
                for label in refs:
                    while curs[label] is not None and curs[label][0]<t:curs[label]=next(refs[label],None)
                    if curs[label] is None or curs[label][0]!=t:continue
                    bg=curs[label][1]
                    for r,b in zip(group,bg):
                        assert (r['coordinate_m'],r['domain_id'])==(b['coordinate_m'],b['domain_id'])
                        assert r['domain_id']==(1 if e=='N' else 3)
                        delta=r['x_surface']-b['x_surface'];matched[(label,e)]+=1
                        for key in ['0_to_30_inclusive','0_to_5_inclusive' if t<=5 else 'after_5_to_30']:
                            maximum_update(comparisons[label][key]['surface'],delta,{'time_s':t,'electrode':e,'coordinate_m':r['coordinate_m'],'domain_id':r['domain_id']})
            for k,it in refs.items():
                for _ in it:pass
            for label,m in metas.items():
                assert set(m['times'])==set(tables[label]['preflight_global'])
                profile_meta[label+'_'+e]={'rows':m['rows'],'saved_times':len(m['times']),'coordinates_per_time':len(m['coordinates']),'first_coordinate':m['coordinates'][0][0],'last_coordinate':m['coordinates'][-1][0],'finite_and_valid_fraction':True}
        out['profile_checks']=profile_meta;out['comparison_rows']={str(k):v for k,v in matched.items()}
        out['comparisons']=comparisons
        primary=diag['numeric']['primary_comparison'];second=diag['numeric']['b020_comparison']
        for label,reported in [('NORMAL30',primary),('B020',second)]:
            r=comparisons[label]['0_to_30_inclusive'];assert r['voltage']['maximum_absolute_delta']==Decimal(reported['maximum_voltage_delta_V']);assert r['surface']['maximum_absolute_delta']==Decimal(reported['maximum_surface_delta'])
            assert r['voltage']['maximum_absolute_delta']<=Decimal('.001') and r['surface']['maximum_absolute_delta']<=Decimal('.0001')
        interval=js(z,'delivery/INTERVAL_SENSITIVITY.json')['stats']
        for k,v in interval.items():
            actual=comparisons['NORMAL30'][k];assert actual['common_time_count']==v['common_time_count']
            for metric in ['voltage','surface']:
                for field in ['maximum_absolute_delta','signed_delta_candidate_minus_reference']:assert actual[metric][field]==Decimal(v[metric][field])
                assert actual[metric]['equal_maximum_count']==v[metric]['equal_maximum_count']
                for f,val in actual[metric]['first_argmax'].items():assert val==(v[metric]['first_argmax'][f] if f=='electrode' else Decimal(v[metric]['first_argmax'][f]))
        totalcols=['Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2']
        li0=sum(tg['preflight_global'][Decimal(0)][k] for k in totalcols)
        lidrift=max(abs(sum(row[k] for k in totalcols)-li0)/abs(li0) for row in tg['preflight_global'].values())
        residual=max(abs((tg['preflight_boundary4'][t]['phis_V']-tg['preflight_boundary1'][t]['phis_V'])-sum(tg['preflight_boundary4'][t][k]-tg['preflight_boundary1'][t][k] for k in ['Eeq_V','etamid_V','phil_V'])) for t in tt)
        assert lidrift==Decimal(diag['numeric']['maximum_Li_relative_drift']) and residual==Decimal(diag['numeric']['maximum_voltage_identity_V'])
        initial={k:abs(tg['preflight_global'][Decimal(0)][k]-tables['NORMAL30']['preflight_global'][Decimal(0)][k]) for k in totalcols};assert all(v==0 for v in initial.values())
        for r in tg['electrolyte_guard'].values():
            assert all(r[k]==0 for k in ['electrolyte_guard','ocp_guard','surface_guard','threshold_mol_m3'])
            assert r['ce_min_all_mol_m3']==min(r[k] for k in ['ce_min_d1_mol_m3','ce_min_d2_mol_m3','ce_min_d3_mol_m3'])>0
        units={}
        for n in z.namelist():
            if n.startswith('run/tables/units_'):
                rs=list(rows(z,n));assert all(r['actual']==r['expected'] for r in rs),n;units[n]=len(rs)
        out['invariants']={'Li_initial_component_absolute_deltas':initial,'maximum_Li_relative_drift':lidrift,'maximum_voltage_identity_V':residual,'minimum_electrolyte_mol_m3':min(r['ce_min_all_mol_m3'] for r in tg['electrolyte_guard'].values()),'all_saved_guards_zero':True,'units_tables_equal':len(units)}
        out['matches_producer_metrics_and_locations']=True
    save('NUMERIC_AUDIT.json',out);print(json.dumps(out,ensure_ascii=False,default=str))

def norm(p): return re.sub('/+','/',p.replace('\\','/')).casefold()

def perform_evidence():
    out={};checks=[]
    def ck(label,ok):
        checks.append({'label':label,'pass':bool(ok)})
        assert ok,label
    with zipfile.ZipFile(MAIN) as z,zipfile.ZipFile(SUPP) as s:
        items={x['file']:x for x in js(z,'MANIFEST.json')['files']}
        mapping=js(z,'delivery/SOURCE_PATH_MAP.json'); reverse={norm(v):k for k,v in mapping.items()}
        linked=[];outside=[]
        def pins(o):
            if isinstance(o,dict):
                if set(('path','sha256','bytes'))<=o.keys():yield o
                for v in o.values():yield from pins(v)
            elif isinstance(o,list):
                for v in o:yield from pins(v)
        for name in ['candidate/CONTRACT.json','authorization/rtol30_001.json','authorization/USER_DECISION.json','authorization/VALIDATION_RELEASE.json','parent/PARENT_START.json','parent/FINAL_BOUNDARY.json','run/CLASS_IDENTITY.json','run/DIAGNOSTIC_RESULT.json']:
            for pin in pins(js(z,name)):
                member=reverse.get(norm(pin['path']))
                if member:
                    entry=items[member];ck(name+' -> '+member,entry['bytes']==pin['bytes'] and entry['sha256']==pin['sha256']);linked.append(member)
                else:outside.append(pin)
        manifest=js(z,'candidate/CODE_MANIFEST.json');msha=sha(z.read('candidate/CODE_MANIFEST.json'))
        ck('accepted candidate manifest',msha=='ac5c29c9676ea3846c582a089683ffbd98466714bbdf49dfa8fca39fdc792847')
        prior=ROOT.parent/'rtol30_preparation_review_20261003'/'received'
        for entry in manifest['files']:
            b=z.read('candidate/'+entry['file']);ck('production seal '+entry['file'],len(b)==entry['bytes'] and sha(b)==entry['sha256'])
            ck('original preparation bytes '+entry['file'],b==(prior/entry['file']).read_bytes())
        ck('run Java byte identity',z.read('run/Rtol30Candidate.java')==z.read('candidate/src/Rtol30Candidate.java'))
        c=js(z,'candidate/CONTRACT.json');ap=js(z,'authorization/rtol30_001.json');state=js(z,'run/NATIVE_STATE.json');gate=js(z,'run/GATE.json')
        ck('approval run and manifest',ap['approved'] is True and ap['run_id']==c['run_id'] and ap['code_manifest_sha256']==msha)
        ud=js(z,'authorization/USER_DECISION.json');ck('decision statement bytes',len(ud['statement'].encode())==ud['statement_bytes'] and sha(ud['statement'].encode())==ud['statement_sha256'])
        ck('approval limits',ap['limits']['compile']==ap['limits']['batch']==ap['limits']['solve']==1 and ap['limits']['retry']==ap['limits']['control']==0)
        ck('policy change prohibited',ap['allow_policy_changes'] is False)
        ck('gate responses',gate['status']=='INPUT_GATE_OK' and len(gate['answers'])==2 and all(a['response']==a['challenge'] and 0<=a['end']-a['start']<=60 for a in gate['answers']))
        ck('gate before compile',gate['answers'][-1]['end']<js(z,'run/compile_RESERVATION.json')['start'])
        phases={}
        for phase in ['compile','batch']:
            reservation=js(z,'run/'+phase+'_RESERVATION.json');result=js(z,'run/'+phase+'_RETURN.json')
            ck(phase+' argv and cwd',reservation['argv']==c['commands'][phase]==ap['commands'][phase] and reservation['cwd']==c['run_root'])
            ck(phase+' return/state equal',result==state[phase])
            ck(phase+' successful owned cleanup',result['rc']==0 and result['root_exit_observed'] and not result['timeout'] and result['cleanup']=='PASS' and not result['remaining_owned'] and not result['recording_errors'] and not result['cleanup_errors'] and result['termination_request'] is None)
            names=sorted(n for n in z.namelist() if n.startswith('run/'+phase+'_event_'))
            ck(phase+' event sequence',names==['run/'+phase+'_event_'+str(i).zfill(6)+'.json' for i in range(1,len(names)+1)])
            ev=[js(z,n) for n in names];ck(phase+' ordered root/assignment/resume', [x['event'] for x in ev[:3]]==['root','assignment','resume'] and ev[0]['suspended'] and ev[1]['assigned_before_resume'] and ev[2]['assigned_before_resume'])
            ck(phase+' single resume and final return',sum(x['event']=='resume' for x in ev)==1 and ev[-1]['terminal_observation']==result)
            phases[phase]={'events':len(ev),'rc':result['rc'],'elapsed_seconds':result['elapsed_seconds'],'cleanup_seconds':result['cleanup_elapsed_seconds'],'event_types':dict(Counter(x['event'] for x in ev))}
        ck('compile ends before batch',js(z,'run/compile_RESERVATION.json')['start']+state['compile']['elapsed_seconds']<=js(z,'run/batch_RESERVATION.json')['start'])
        budget=ap['budgets_seconds'];post=js(s,'POST_WRITE_USER_RETURN.json')['value'];final=js(z,'parent/FINAL_BOUNDARY.json');dec=js(z,'parent/PARENT_LOCAL_DECISION.json');diag=js(z,'run/DIAGNOSTIC_RESULT.json')
        ck('native compile+batch budget',sum(state[p]['elapsed_seconds'] for p in phases)<=budget['compile_batch'])
        ck('analysis budget',diag['analysis_elapsed_seconds']<=budget['analysis'])
        ck('postwrite record identity',post['boundary']['sha256']==sha(z.read('parent/FINAL_BOUNDARY.json')) and post['boundary']['bytes']==len(z.read('parent/FINAL_BOUNDARY.json')))
        ck('postwrite timer and no errors',post['snapshot_seconds']>=post['pre_write_seconds']==final['elapsed_seconds'] and post['snapshot_seconds']<=budget['overall'] and post['delivery_elapsed_seconds']<=budget['delivery'] and not post['record_errors'] and not final['errors'])
        ck('NoExit boundary preserved',post['raw_host_rc'] is None and final['raw_host_rc'] is None and final['host_boundary']=='SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT')
        ck('child parent rc',all(dec[k]['native_rc']==0 and dec[k]['returned'] and not dec[k]['new_error'] for k in ['native_return','analysis_return']))
        ck('postwrite duplicate identity',z.read('delivery/POST_WRITE_USER_RETURN.json')==s.read('POST_WRITE_USER_RETURN.json'))
        receipt=js(s,'DELIVERY_RECEIPT.json');pack=js(s,'PACKAGING_TOOL_RETURN.json');pack_stdout=json.loads(pack['completion']['output'])
        observed=identity(MAIN)
        ck('delivery receipt main identity',receipt['zip']['bytes']==observed['bytes'] and receipt['zip']['sha256']==observed['sha256'])
        ck('main packaging return and receipt',pack['completion']['exit_code']==0 and all(pack_stdout[k]==v for k,v in receipt.items()))
        ck('recipient null and native reruns zero',receipt['recipient'] is None and receipt['native_reruns']==0)
        before=js(z,'delivery/PRESERVATION_BEFORE.json');after=js(s,'PRESERVATION_AFTER.json');bmap={norm(x['path']):x for x in before};amap={norm(x['path']):x for x in after}
        ck('preservation names no duplicates',len(bmap)==len(before) and len(amap)==len(after))
        ck('all selected before identities retained',all(k in amap and (v['bytes'],v['sha256'])==(amap[k]['bytes'],amap[k]['sha256']) for k,v in bmap.items()))
        matched_pres=0
        for k,pin in bmap.items():
            member=reverse.get(k)
            if member:
                ck('preservation available member '+member,items[member]['bytes']==pin['bytes'] and items[member]['sha256']==pin['sha256']);matched_pres+=1
        pol=js(z,'run/POLICY_BEFORE.json');recheck=js(z,'preexec_evidence/09/AUTHORIZATION_RECHECK.json')
        ck('prior security snapshot',pol['security']==recheck['security_only'] and len(pol['security'])==16 and pol['security']['security.external.filepermission']=='limited' and pol['security']['security.external.enable']=='on')
        ck('default prefs start and end record',pol['default']==ap['default_prefs_identity'] and amap[norm(pol['default']['path'])]['sha256']==pol['default']['sha256'])
        ck('policy native result no errors',state['policy_preservation']=='PASS' and not state['errors'])
        previous=ROOT.parent/'normal30_native_review_20260930'/'received'
        baseline_verified=[]
        for name,pin in c['baseline_files'].items():
            source=previous/('baseline/'+name[5:] if name.startswith('B020_') else 'run/tables/'+name)
            ck('baseline prior recipient '+name,identity(source)['sha256']==items['baseline/'+name]['sha256']);baseline_verified.append(name)
        ck('baseline log prior recipient',identity(previous/'run/batch.log')['sha256']==items['comparison_logs/normal30_rtol1e6_batch.log']['sha256'])
        ck('current log copy equality',items['run/batch.log']['sha256']==items['comparison_logs/rtol1e7_batch.log']['sha256'])
        logcheck={};steps=js(z,'delivery/SOLVER_STEP_OBSERVATIONS.json')
        for label,name in [('rtol1e7','run/batch.log'),('normal30_rtol1e6','comparison_logs/normal30_rtol1e6_batch.log')]:
            lines=z.read(name).decode('utf-8-sig').splitlines(); parsed=[]
            for i,line in enumerate(lines,1):
                toks=line.split()
                if len(toks)>=8 and toks[0].isdigit() and toks[3]=='out':
                    initial=toks[0]=='0';parsed.append({'step':int(toks[0]),'time_s':toks[1],'reported_stepsize':toks[2],'Tfail':None if initial else int(toks[8]),'NLfail':None if initial else int(toks[9]),'source_line':i})
            reported=steps[label];ck(label+' step rows',len(parsed)==reported['logged_state_rows_including_initial'])
            for row,rep in zip(parsed,reported['rows']):ck(label+' log row '+str(row['step']),all((Decimal(rep[k])==Decimal(v)) if k=='time_s' else rep[k]==v for k,v in row.items()))
            ck(label+' native end',Decimal(parsed[-1]['time_s'])==30 and parsed[-1]['step']==reported['last_step_index'] and 'Time-stepping completed.' in lines)
            ck(label+' counters zero',all(row['Tfail']==row['NLfail']==0 for row in parsed[1:]))
            logcheck[label]={'logged_rows':len(parsed),'last_step_index':parsed[-1]['step'],'Tfail':0,'NLfail':0,'time_solver_seconds':reported['time_solver_solution_seconds'],'reported_core_lines':[l for l in lines if 'cores in total' in l]}
        out.update(check_count=len(checks),all_pass=True,checks=checks,candidate_manifest_sha256=msha,linked_unique_members=len(set(linked)),unpackaged_identity_claims=outside,phases=phases,selected_preservation={'before_count':len(before),'after_count':len(after),'available_members_bound':matched_pres,'additional_after_records':len(set(amap)-set(bmap))},prior_recipient_baselines_matched=baseline_verified,log_observations=logcheck,budgets={'compile_batch_seconds':sum(state[p]['elapsed_seconds'] for p in phases),'analysis_seconds':diag['analysis_elapsed_seconds'],'parent_postwrite_seconds':post['snapshot_seconds'],'parent_overall_limit':budget['overall'],'postwrite_delivery_seconds':post['delivery_elapsed_seconds']},delivery={'main_packaging_chunk':pack['completion']['chunk_id'],'main_packaging_rc':pack['completion']['exit_code'],'collection_packaging_snapshot_seconds':receipt['collection_analysis_package_snapshot_seconds'],'separate_from_native_parent_budget':True},scope='Saved records plus available bytes only; not live OS/process/prefs/MPH/console observation; prior approvals are historical, not new authorization.')
    save('EVIDENCE_AUDIT.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ['checks','unpackaged_identity_claims']},ensure_ascii=False))

if __name__=='__main__':
    if sys.argv[1]=='verify':perform_verify()
    elif sys.argv[1]=='dump':dump(sys.argv[2:])
    elif sys.argv[1]=='numeric':perform_numeric()
    elif sys.argv[1]=='evidence':perform_evidence()
