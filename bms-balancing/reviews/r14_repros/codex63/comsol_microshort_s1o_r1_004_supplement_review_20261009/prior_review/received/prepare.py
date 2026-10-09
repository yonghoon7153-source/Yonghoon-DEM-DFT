"""Data/AST-only preparation; no candidate functions or functional engine."""
import ast,json,hashlib,sys,time,shutil,difflib,zipfile
from pathlib import Path
R=Path(__file__).resolve().parent;S=R.parent;OLD=S/'future_validation_fixture_R1_003'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def h(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':h(b)}
def write(name,o):
 with (R/name).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2)
origin=read(R/'ORIGIN.json')
assert origin['start_free_bytes']>=2*1024**3
manifest=read(S/'CODE_MANIFEST.json');assert identity(S/'CODE_MANIFEST.json')['sha256']=='4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da'
oldseal=read(OLD/'FIRST_SEAL.json');before=[]
for pin in oldseal['files']:
 now=identity(pin['path']);assert now['bytes']==pin['bytes'] and now['sha256']==pin['sha256'];before.append(now)
oldzip=OLD/'COMSOL_MICROSHORT_S1O_R1_003_VALIDATION_STOP_20261008.zip'
assert identity(oldzip)['sha256']=='11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b'
review=Path('C:/Users/BML/Desktop/COMSOL_MICROSHORT_S1O_R1_003_STOP_REVIEW_20261008.zip')
assert identity(review)['sha256']=='56c52add014684850a533136d1add01e1a937db1cebcbc0236d40413cc5eaffe'
with zipfile.ZipFile(review) as z:
 b=z.read('NEXT_LIMITED_APPROVAL_DRAFT_KO.md');assert h(b)=='8bd02f0fbecbd3612635be2a234ac250533f404db7b7cf98b1f1d5b394912015';(R/'reference/NEXT_LIMITED_APPROVAL_DRAFT_KO.md').write_bytes(b)
shutil.copyfile(oldzip,R/'reference/R1_003_ORIGINAL_RESULT.zip')
for n in ('shared_fixture.py','input_binding.py'):shutil.copyfile(OLD/'harness'/n,R/'harness'/n)
sys.path.insert(0,str(R/'harness'))
from inputs import inputs,negatives
from input_binding import fingerprint,normalize
pins={k:{'function':fn,'fingerprint':fingerprint(fn,args,{}),'definition':normalize(args)} for k,(fn,args) in inputs().items()}
oldinputs={x['id']:x for x in read(OLD/'CONSUMER_INPUT_IDENTITIES.json')}
delta=[]
for cid,x in negatives().items():
 fp=fingerprint(x['function'],x['args'],{});assert [fp]==oldinputs[cid]['calls']
 delta.append({'id':cid,'positive_control':x['control'],'delta':x['delta'],'derived_negative_fingerprint':fp,'prior_recipe_identity':oldinputs[cid]['recipe_identity'],'exact_match':True,'candidate_calls':0})
write('INPUT_SEAL.json',{'positive_inputs':pins,'negative_delta_binding':delta,'new_python_inputs':4,'negative_retests':0})
py=read(OLD/'results/PYTHON_RESULTS.json');ps=read(OLD/'results/ps_first_failure.json')
assert py['status']=='PASS' and py['count']==99 and len(ps['cases'])==28
assert all(x['status']=='PASS' for x in py['cases']) and all(x['result']=='PASS' and x['reason_matches'] and x['reach_matches'] and x['extra_assertions'] for x in ps['cases'])
parent02=next(x for x in ps['cases'] if x['id']=='PARENT02')
assert parent02['raw_return']['comparison']=='EXCEEDS_LIMITS' and 'S1Fields' in parent02['target_reach']
write('REUSE_MAP.json',{'prior_python':identity(OLD/'results/PYTHON_RESULTS.json'),'prior_ps':identity(OLD/'results/ps_first_failure.json'),'prior_pass_ids':[x['id'] for x in py['cases']]+[x['id'] for x in ps['cases']],'prior_count':127,'READ02_12_closure':'conditional on new matching positive4 PASS plus static exact delta binding','PARENT_R114_positive':parent02,'shared_producer_loader_and_production_functions':'unchanged raw loader/extraction and JSON parsing; R113-only cast is declared fixture mutation','new_order':['PARENT_R115','PARENT_R113','PARENT_R114'],'native_ready':False})
plan=read(OLD/'VALIDATION_PLAN_CORRECTED.json');ids=['PARENT_R115','PARENT_R113','PARENT_R114'];plan['cases']=[next(x for x in plan['cases'] if x['id']==cid) for cid in ids];plan['scope']='R1_004 three original incomplete PS cases; Python four auxiliary positive inputs separately';plan['prospective_fixture_root']=str(R)
plan.pop('commands',None)
write('VALIDATION_PLAN_CORRECTED.json',plan)
recipes=read(OLD/'harness/PS_INPUT_RECIPES.json');recipes['cases']=[next(x for x in recipes['cases'] if x['id']==cid) for cid in ids];recipes['case_count']=3;recipes['kind']='S1O_R1_004_SUBSET_RECIPES'
recipes['cases'][1]['mutations']=['same POLICY02 JSON string0.001 quotes removed only','parse actual CLR type/value recorded first','only value leaf explicitly cast to Double; rest unchanged']
write('harness/PS_INPUT_RECIPES.json',recipes)
text=(OLD/'harness/ps_harness.ps1').read_text()
text=text.replace("$cases.Count -eq 31","$cases.Count -eq 3").replace("@($recipes.cases).Count -eq 31","@($recipes.cases).Count -eq 3").replace(' -gt 300',' -gt 180').replace(' -le 300',' -le 180').replace('limit_s=300','limit_s=180')
text=text.replace('S1O_R1_PS_PRODUCER_SECOND_SEAL','S1O_R1_004_REUSED_PRODUCER_SEAL')
text=text.replace("        $id=[string]$case.id","        $id=[string]$case.id\n        $global:S1ValidationReached.Clear()\n        $currentDiagnostic=@{id=$id;target_entered=$false;reach=@();transport=$null}\n        HWrite 'current_case_diagnostic.json' $currentDiagnostic")
needle="                HRequire ($result.comparison_details.maxima.voltage_V.value -is [double]) 'R113_DOUBLE_AFTER_JSON_PARSE'"
assert text.count(needle)==1
replacement=r'''                $parsedValue=$result.comparison_details.maxima.voltage_V.value
                $typeName=$(if($null -eq $parsedValue){'null'}else{$parsedValue.GetType().FullName})
                $currentDiagnostic.transport=@{source_sha256=$p.source.sha256;mutant_bytes=$utf8.GetByteCount($mutant);mutant_sha256=(HHash ($utf8.GetBytes($mutant)));token_match_index=$matches[0].Index;parsed_clr_type=$typeName;parsed_value=[string]$parsedValue}
                HWrite 'current_case_diagnostic.json' $currentDiagnostic
                HRequire ($null -ne $parsedValue -and $parsedValue -isnot [string] -and $parsedValue -isnot [bool] -and $typeName -in @('System.Decimal','System.Double','System.Single','System.Int32','System.Int64')) 'R113_NUMERIC_PARSE_TYPE'
                HRequire (-not [double]::IsNaN([double]$parsedValue) -and -not [double]::IsInfinity([double]$parsedValue) -and [decimal]$parsedValue -eq [decimal]0.001) 'R113_EXACT_FINITE_VALUE'
                $result.comparison_details.maxima.voltage_V.value=$null
                $restBefore=$result|ConvertTo-Json -Depth 100 -Compress
                $result.comparison_details.maxima.voltage_V.value=[double]$parsedValue
                $castValue=$result.comparison_details.maxima.voltage_V.value
                $currentDiagnostic.transport.cast_clr_type=$castValue.GetType().FullName
                $currentDiagnostic.transport.cast_value_roundtrip=$castValue.ToString('R',[Globalization.CultureInfo]::InvariantCulture)
                $currentDiagnostic.transport.double_bits_hex=([BitConverter]::DoubleToInt64Bits($castValue)).ToString('X16')
                $result.comparison_details.maxima.voltage_V.value=$null
                $restAfter=$result|ConvertTo-Json -Depth 100 -Compress
                $result.comparison_details.maxima.voltage_V.value=$castValue
                $currentDiagnostic.transport.other_leaves_unchanged=($restBefore -ceq $restAfter)
                HWrite 'current_case_diagnostic.json' $currentDiagnostic
                HRequire ($castValue -is [double] -and $restBefore -ceq $restAfter) 'R113_EXPLICIT_SINGLE_LEAF_DOUBLE'
                $recipeTransport=$currentDiagnostic.transport'''
text=text.replace(needle,replacement)
oldtransport="                $recipeTransport=@{source_sha256=$p.source.sha256;mutant_bytes=$utf8.GetByteCount($mutant);mutant_sha256=(HHash ($utf8.GetBytes($mutant)));token_match_index=$matches[0].Index;parsed_clr_type=$result.comparison_details.maxima.voltage_V.value.GetType().FullName}"
assert text.count(oldtransport)==1;text=text.replace(oldtransport,'')
text=text.replace('            $observed=S1Decision $native $analysis $result $expected $completion',"            $currentDiagnostic.target_entered=$true\n            $observed=S1Decision $native $analysis $result $expected $completion")
text=text.replace('        $pass=$reasonMatches -and $reachMatches -and $extraChecks',"        if($id -eq 'PARENT_R113'){$extraChecks=$extraChecks -and $observed.stage -ceq 'comparison_numerics'}\n        if($id -eq 'PARENT_R114'){$extraChecks=$extraChecks -and $observed.stage -ceq 'fields'}\n        $currentDiagnostic.reach=$reach\n        HWrite 'current_case_diagnostic.json' $currentDiagnostic\n        $pass=$reasonMatches -and $reachMatches -and $extraChecks")
text=text.replace("$failure=@{status='INCOMPLETE';","$failure=@{diagnostic=$currentDiagnostic;status='INCOMPLETE';")
(R/'harness/ps_subset.ps1').write_text(text,encoding='utf-8',newline='\n')
diff=''.join(difflib.unified_diff((OLD/'harness/ps_harness.ps1').read_text().splitlines(True),text.splitlines(True),fromfile='R1_003/ps_harness.ps1',tofile='R1_004/ps_subset.ps1'))
(R/'PS_SUBSET.diff').write_text(diff,encoding='utf-8')
(R/'results/producers').mkdir()
producer=read(OLD/'results/PS_PRODUCER_SEAL.json')
for p in producer['files']:
 raw=(OLD/p['path']).read_bytes();assert h(raw)==p['sha256'] and len(raw)==p['bytes'];(R/p['path']).write_bytes(raw)
producer['kind']='S1O_R1_004_REUSED_PRODUCER_SEAL';producer['harness_sha256']=identity(R/'harness/ps_subset.ps1')['sha256'];producer['origin']='Original R1_003 actual producers; not regenerated';write('results/PS_PRODUCER_SEAL.json',producer)
runner=(OLD/'tools/run_engine_once.ps1').read_text().replace('$seal.cases -ne 130','$seal.cases -ne 7').replace('$seal.preseal_elapsed_s -gt 720','$seal.preseal_elapsed_s -gt 600').replace('(1860-120)','(1200-60)').replace('$priorResult.count -ne 99','$priorResult.count -ne 4')
(R/'harness/run_engine_once.ps1').write_text(runner,encoding='utf-8',newline='\n')
for p in (R/'harness').glob('*.py'):ast.parse(p.read_text())
# Validate extraction identities as text only, including production Python spans.
for span in read(OLD/'VALIDATION_PLAN_CORRECTED.json')['extraction_spans']:
 lines=(S/span['source']).read_text().splitlines();b='\n'.join(lines[span['start_line']-1:span['end_line']]).encode();assert b and h(b)==span['sha256']
deps=read(OLD/'DEPENDENCY_ORIGINS.json');depchecked=[]
for x in deps['module_origins']:
 if 'sha256' in x:
  now=identity(x['origin']);assert now['sha256']==x['sha256'] and now['bytes']==x['bytes'];depchecked.append(now)
write('DEPENDENCY_ORIGINS.json',{'reused_from':identity(OLD/'DEPENDENCY_ORIGINS.json'),'files':depchecked,'builtin_frozen':[x for x in deps['module_origins'] if 'sha256' not in x],'candidate_calls':0})
write('BEFORE.json',{'prior_first_seal':identity(OLD/'FIRST_SEAL.json'),'prior_files':before,'review_zip':identity(review),'source_manifest':identity(S/'CODE_MANIFEST.json')})
engines=oldseal['engines'];commands=[{'engine':'python','argv':[engines[0]['path'],'-I','-B',str(R/'harness/python_subset.py')],'cwd':str(R),'limit_s':120},{'engine':'powershell','argv':[engines[1]['path'],'-NoLogo','-NoProfile','-NonInteractive','-File',str(R/'harness/ps_subset.ps1')],'cwd':str(R),'limit_s':180}]
write('COMMANDS.json',commands)
print(json.dumps({'prepared':True,'new_inputs':7,'negative_data_bindings':len(delta),'production_calls':0,'elapsed_s':time.perf_counter()-origin['monotonic_ticks']/origin['frequency']}))
