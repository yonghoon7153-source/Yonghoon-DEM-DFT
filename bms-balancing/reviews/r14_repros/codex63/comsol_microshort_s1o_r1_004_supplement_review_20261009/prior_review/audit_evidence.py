"""Independent record/hash/fixture-data audit; received functions are never run."""
from pathlib import Path
from decimal import Decimal, localcontext
import base64, copy, difflib, hashlib, json, re, struct

ROOT=Path(__file__).resolve().parent
R=ROOT/'received'
O=ROOT.parent/'microshort_s1o_r1_003_stop_review_20261008/received'
def raw(p): return p.read_bytes()
def sha(b): return hashlib.sha256(b).hexdigest()
def j(p): return json.loads(raw(p).decode('utf-8-sig'))
checks=[]
def check(ok, label):
    checks.append({'check':label,'pass':bool(ok)})
    if not ok: raise AssertionError(label)
def ident_match(p, rec): return len(raw(p))==rec['bytes'] and sha(raw(p))==rec['sha256']
def norm(v):
    if isinstance(v,Decimal): return {'__decimal__':str(v)}
    if isinstance(v,bytes): return {'__bytes_base64__':base64.b64encode(v).decode('ascii')}
    if isinstance(v,dict): return {'__mapping__':[[norm(k),norm(val)] for k,val in v.items()]}
    if isinstance(v,(tuple,list)): return [norm(x) for x in v]
    return v
def fingerprint(fn,args):
    b=json.dumps({'function':fn,'args':norm(args),'kwargs':norm({})},separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
    return {'function':fn,'canonical_bytes':len(b),'sha256':sha(b)}

cm=j(O/'source/CODE_MANIFEST.json')
check(sha(raw(O/'source/CODE_MANIFEST.json'))=='4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da','accepted production manifest')
check(len(cm['files'])==21 and all(ident_match(O/'source'/e['path'],e) for e in cm['files']),'all 21 production members')
plan=j(R/'VALIDATION_PLAN_CORRECTED.json'); oldplan=j(O/'VALIDATION_PLAN_CORRECTED.json')
for e in plan['extraction_spans']:
    text=raw(O/'source'/e['source']).decode('utf-8-sig').replace('\r\n','\n').splitlines()
    b='\n'.join(text[e['start_line']-1:e['end_line']]).encode()
    check(bool(b) and sha(b)==e['sha256'],'span '+e['name'])
check(plan['extraction_spans']==oldplan['extraction_spans'],'43 extraction spans unchanged')
observed=j(R/'results/ps_extraction_observed.json')
check(ident_match(O/'source/candidate/Parent.ps1.inactive.txt',{'bytes':observed['source_bytes'],'sha256':observed['source_sha256']}),'PS observed parent bytes')
spans={x['name']:x for x in plan['extraction_spans'] if x['source'].endswith('Parent.ps1.inactive.txt')}
check(len(observed['spans'])==15 and all(x['sha256']==spans[x['name']]['sha256'] for x in observed['spans']),'PS observed 15 spans')
for name in ('shared_fixture.py','input_binding.py'):
    check(raw(R/'harness'/name)==raw(O/'harness'/name),'unchanged fixture helper '+name)
oldps=raw(O/'harness/ps_harness.ps1').decode('utf-8-sig').replace('\r\n','\n')
newps=raw(R/'harness/ps_subset.ps1').decode('utf-8-sig').replace('\r\n','\n')
diff=''.join(difflib.unified_diff(oldps.splitlines(True),newps.splitlines(True),fromfile='R1_003/ps_harness.ps1',tofile='R1_004/ps_subset.ps1'))
check(diff==raw(R/'PS_SUBSET.diff').decode().replace('\r\n','\n'),'PS diff complete and exact')
check(oldps[oldps.index('function HProducer'):oldps.index('function HRequire')]==newps[newps.index('function HProducer'):newps.index('function HRequire')],'common producer loader unchanged')

psseal=j(R/'results/PS_PRODUCER_SEAL.json')
check(psseal['harness_sha256']==sha(raw(R/'harness/ps_subset.ps1')),'new PS seal binds NEW harness')
for e in psseal['files']:
    check(ident_match(R/e['path'],e) and raw(R/e['path'])==raw(O/e['path']),'unchanged producer '+e['path'])
check(ident_match(O/'results/PYTHON_RESULTS.json',psseal['python_results']) and ident_match(O/'results/PYTHON_SESSION.json',psseal['python_session']),'producer seal binds old python results/session')
py=j(R/'results/PYTHON_RESULTS.json'); ps=j(R/'results/ps_results.json')
for name,rs in [('PYTHON',py),('POWERSHELL',ps)]:
    stdout=raw(R/f'results/{name}_STDOUT.txt').decode('utf-8-sig')
    lines=[json.loads(x) for x in stdout.splitlines() if x.strip()]
    check(lines==rs['cases'],name+' raw stdout equals every result case')
    session=j(R/f'results/{name}_SESSION.json')
    check(session['rc']==0 and not session['timed_out'] and session['within_limits'],name+' rc0 within budget')
    check(ident_match(R/f'results/{name}_STDOUT.txt',session['stdout']) and ident_match(R/f'results/{name}_STDERR.txt',session['stderr']),name+' stdout stderr identities')
    check(raw(R/f'results/{name}_STDERR.txt')==b'',name+' empty stderr')
    attempt=j(R/f'results/{name}_ATTEMPT.json')
    check(ident_match(R/'FIRST_SEAL.json',attempt['first_seal']) and attempt['retry']==0,name+' attempt sealed before session')

ids=['PARENT_R115','PARENT_R113','PARENT_R114']
check([x['id'] for x in ps['cases']]==ids==plan['ps_order'],'PS exact three order')
check(all(x['result']=='PASS' and x['reason_matches'] and x['reach_matches'] and x['extra_assertions'] for x in ps['cases']),'PS three cases passed reason and reach')
check(ps['cases'][0]['raw_return']['comparison']=='WITHIN_LIMITS_THIS_WINDOW','R115 positive WITHIN')
for x,reason,stage in [(ps['cases'][1],'DECIMAL_TRANSPORT_PRECISION','comparison_numerics'),(ps['cases'][2],'COMPARISON_SUMMARY_CONTRADICTION','fields')]:
    check(x['raw_return']['reason']==reason and x['raw_return']['stage']==stage and {'S1Decision','S1Fields','S1ComparisonNumerics'}<=set(x['target_reach']),x['id']+' actual rejection stage')
t=ps['cases'][1]['json_transport']
policy=raw(R/'results/producers/POLICY02.json')
pattern=rb'("voltage_V"\s*:\s*\{[^{}]*"value"\s*:\s*)"0\.001"'
matches=list(re.finditer(pattern,policy)); mutant=re.sub(pattern,rb'\g<1>0.001',policy)
check(len(matches)==1 and len(mutant)==len(policy)-2 and len(mutant)==t['mutant_bytes'] and sha(mutant)==t['mutant_sha256'],'R113 quote-only mutant bytes')
check(t['token_match_index']==matches[0].start() and t['source_sha256']==sha(policy),'R113 original and token offset')
check(t['parsed_clr_type']=='System.Decimal' and t['parsed_value']=='0.001' and t['cast_clr_type']=='System.Double' and t['other_leaves_unchanged'],'R113 observed parse/cast separation')
check(struct.pack('>d',0.001).hex().upper()==t['double_bits_hex'],'R113 IEEE754 bits')

rawcsv=b'time_s,value\n0,1\n1,2\n'
identity=lambda b:{'path':'fixture/simple.csv','bytes':len(b),'sha256':sha(b)}
with localcontext() as ctx:
    ctx.prec=50
    coords=[Decimal('0.000052')*Decimal(i)/Decimal(240) for i in range(241)]
    profile=[{'time_s':Decimal(0),'coordinate_m':x,'domain_id':Decimal(1),'x_surface':Decimal('.445'),'x_particle_average':Decimal('.445')} for x in coords]
baselines={
 'READ_CTRL_CSV':('read_csv_bytes',[rawcsv,['time_s','value'],identity(rawcsv),{'time_s':'s','value':'1'},{'time_s':'s','value':'1'}]),
 'READ_CTRL_TIME':('timed_rows',[[{'time_s':Decimal(0)},{'time_s':Decimal(1)}],'1']),
 'READ_CTRL_COVERAGE':('coverage',[[Decimal(0),Decimal(1)],[Decimal(0),Decimal(1)],['0','1'],['0','1'],['0','1'],'1']),
 'READ_CTRL_PROFILE':('profile_rows',[profile,[Decimal(0)],coords,1])}
inp=j(R/'INPUT_SEAL.json'); oldinp={x['id']:x for x in j(O/'CONSUMER_INPUT_IDENTITIES.json')}
check(list(baselines)==[x['id'] for x in py['cases']],'four auxiliary positives only')
for x in py['cases']:
    fn,args=baselines[x['id']]; pin=inp['positive_inputs'][x['id']]
    check(pin['definition']==norm(args) and pin['fingerprint']==fingerprint(fn,args),'independent baseline data '+x['id'])
    check(x['input']==pin and x['status']=='PASS' and x['target_calls']==1 and fn in x['reached_functions'],'positive target entered '+x['id'])
for row in inp['negative_delta_binding']:
    cid=row['id']; i=int(cid[-2:]); fn,a=copy.deepcopy(baselines[row['positive_control']])
    if i==2:a[2]['sha256']='0'*64
    elif i==3:a[3]={'time_s':'ms','value':'1'}
    elif i==4:a[1]=['other','value']
    elif i in (5,6,7):
        a[0]={5:b'time_s,value\n0\n',6:b'time_s,value\n0,NaN\n',7:b'time_s,value\n'}[i];a[2]=identity(a[0])
    elif i==8:a[0][1]['time_s']=Decimal(0)
    elif i==9:a[0]=[Decimal(0)]
    elif i==10:a[:5]=[[Decimal(0)],[Decimal(0)],['0'],['0'],['0']]
    elif i==11:a[0][0]['domain_id']=Decimal(3)
    elif i==12:a[0].pop()
    fp=fingerprint(fn,a)
    check(fp==row['derived_negative_fingerprint'] and [fp]==oldinp[cid]['calls'],cid+' independently derived negative fingerprint equals old input')
    check(ident_match(O/row['prior_recipe_identity']['path'].replace('\\','/'),row['prior_recipe_identity']),cid+' old recipe bytes')

oldpy=j(O/'results/PYTHON_RESULTS.json'); oldpsr=j(O/'results/ps_first_failure.json'); reuse=j(R/'REUSE_MAP.json')
oldrecords=oldpy['cases']+oldpsr['cases']; oldids=[x['id'] for x in oldrecords]
check(len(oldrecords)==127 and oldids==reuse['prior_pass_ids'],'127 exact old results reused')
check(reuse['PARENT_R114_positive']==next(x for x in oldpsr['cases'] if x['id']=='PARENT02'),'R114 old positive exact record')
cover=j(R/'ORIGINAL130_COVERAGE_MAP.json')
check(len(cover['cases'])==130 and len({x['id'] for x in cover['cases']})==130 and {x['id'] for x in cover['cases']}=={x['id'] for x in oldplan['cases']},'all 130 original IDs covered without duplicates')
for c,r in zip(cover['cases'],oldrecords+ps['cases']):
    check(c['id']==r['id'] and c['observed']==r['observed'] and c['reached']==r.get('reached_functions',r.get('target_reach')),'coverage row '+c['id'])
check(cover['auxiliary_cases']==py['cases'],'auxiliary four kept separate')

seal=j(R/'FIRST_SEAL.json'); after=j(R/'SELECTED_SOURCES_AFTER.json'); before=j(R/'BEFORE.json')
oldseal=j(O/'FIRST_SEAL.json')
check(before['prior_files']==oldseal['files'],'prior 123 identities unchanged')
check(len(seal['files'])==after['count']==len(after['items'])==246,'246 preserved paths count')
check(all(x['before']==x['after'] and x['match'] for x in after['items']),'all 246 submitted before/after equal')
check([x['before'] for x in after['items']]==seal['files'],'after exact sealed set')
check(len({x['path'].casefold() for x in seal['files']})==246,'246 unique sealed paths')
available=0; remote=[]
for e in seal['files']:
    path=e['path'].replace('\\','/')
    local=None
    if '/future_validation_fixture_R1_004/' in path: local=R/path.split('/future_validation_fixture_R1_004/',1)[1]
    elif '/future_validation_fixture_R1_003/' in path: local=O/path.split('/future_validation_fixture_R1_003/',1)[1]
    elif '/microshort_s1o_r1_20261008/' in path:local=O/'source'/path.split('/microshort_s1o_r1_20261008/',1)[1]
    if local is not None and local.is_file():
        check(ident_match(local,e),'sealed supplied bytes '+str(local.relative_to(ROOT.parent)))
        available+=1
    else:remote.append(e)
for e in oldseal['files']:
    check(e in seal['files'],'old sealed file retained '+e['path'])
tool=j(R/'ENGINE_TOOL_RETURNS.json')
for engine,key in [('PYTHON','python'),('POWERSHELL','powershell_completion')]:
    rec=tool[key];out=json.loads(rec['output']);session=j(R/f'results/{engine}_SESSION.json')
    check(rec['exit_code']==0 and out['rc']==0 and out['within_limits'] and out['elapsed_s']>=session['elapsed_s'],'post session return '+engine)
    check(ident_match(R/f'results/{engine}_SESSION.json',out['session']),engine+' post-write session identity')
close=j(R/'VALIDATION_CLOSEOUT.json'); origin=j(R/'ORIGIN.json'); delivery=j(R/'DELIVERY_ORIGIN.json')
check(seal['origin']==origin and seal['preseal_elapsed_s']<600,'origin and preseal budget')
delta=(delivery['monotonic_ticks']-origin['monotonic_ticks'])/origin['frequency']
check(abs((close['overall_snapshot_s']-close['delivery_snapshot_s'])-delta)<0.002,'same origin delivery clock boundary')
result={'kind':'INDEPENDENT_STATIC_RECORD_AUDIT','checks':checks,'passed_checks':len(checks),
 'production_files':21,'prior_pass_reused':127,'original_new_cases':3,'auxiliary_positive_cases':4,'original_total':130,
 'read_negative_data_bindings':11,'preserved_identity_records':246,'directly_available_sealed_file_bytes':available,
 'remote_identity_only_count':len(remote),'remote_identity_only':remote,
 'actual_candidate_calls_by_reviewer':0,'test_reruns_by_reviewer':0,'native_calls_by_reviewer':0,
 'R113_transport':t,'delivery_origin_relative_seconds':delta,'latest_internal_snapshot_s':close['overall_snapshot_s'],
 'packaging_snapshot_from_user_transcription_s':569.9144170000218,'later_614_480_observation':'USER_REPORT_ONLY_PENDING_ORIGINAL'}
(ROOT/'RECORD_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','remote_identity_only')},ensure_ascii=False))
