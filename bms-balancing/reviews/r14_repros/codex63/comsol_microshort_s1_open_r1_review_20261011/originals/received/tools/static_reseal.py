"""Author-owned static DATA inspector. Never imports/calls submitted modules."""
import ast, difflib, hashlib, json, pathlib, time
R = pathlib.Path(__file__).resolve().parents[1]
B = R/'basis/prior_preparation'
checks=[]
def readj(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def check(name,ok,detail=None):
 checks.append({'id':name,'matched':bool(ok),'detail':detail})
def identity(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
old=(B/'candidate/resource_connection.py.inactive.txt').read_text()
new=(R/'candidate/resource_connection.py.inactive.txt').read_text()
ot=ast.parse(old);nt=ast.parse(new)
check('resource_python_parse',True,'AST only; no compile/import/function evaluation')
olddefs={n.name:ast.get_source_segment(old,n) for n in ot.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
newdefs={n.name:ast.get_source_segment(new,n) for n in nt.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
allowed={'finite_time','project_owned_sample','resource_decision'}
for name in olddefs:
 if name not in allowed: check('unchanged_definition:'+name,olddefs[name]==newdefs[name])
check('added_definitions_exact',set(newdefs)-set(olddefs)=={'ExecutionClockContext','ResourceSession','bind_sample_clock'})
for name in ['ExecutionClockContext','ResourceSession']:
 node=next(n for n in nt.body if getattr(n,'name',None)==name)
 deco=next(d for d in node.decorator_list if isinstance(d,ast.Call) and isinstance(d.func,ast.Name) and d.func.id=='dataclass')
 kw={k.arg:k.value.value for k in deco.keywords}
 check('frozen_slots:'+name,kw.get('frozen') is True and kw.get('slots') is True)
session=next(n for n in nt.body if getattr(n,'name',None)=='ResourceSession')
decide=next(n for n in session.body if getattr(n,'name',None)=='decide')
check('sample_api_no_rebinding', [a.arg for a in decide.args.args]==['self','control','raw','previous_sample_end_s','contract'])
check('session_call_binds_clock','previous_sample_end_s, contract, self.clock)' in newdefs['ResourceSession'])
check('anchors_snapshot','tuple(anchors.items())' in newdefs['ResourceSession'])
check('anchors_scalar_only','type(v) in (str, int, bool, type(None))' in newdefs['ResourceSession'])
check('start_record_missing_explicit',"'CONTEXT_MISSING:'+name" in newdefs['ResourceSession'])
check('sample_identity_exact',"type(raw[name]) is str and raw[name] == getattr(context, name)" in newdefs['bind_sample_clock'])
check('sample_origins_required',"'CLOCK_ORIGIN_MISSING:'+name" in newdefs['bind_sample_clock'])
check('sample_origins_exact',"raw[name] == getattr(context, name)" in newdefs['bind_sample_clock'])
check('elapsed_only_context',"'native_elapsed_s':end-context.native_origin_s" in new and "'overall_elapsed_s':end-context.overall_origin_s" in new and "end-raw[" not in new)
proj=newdefs['project_owned_sample']
check('os_failure_before_clock',proj.index("'OS_QUERY_FAILURE'") < proj.index('bind_sample_clock'))
check('counter_type_keys_identity_before_dereference',proj.index("type(p) is dict") < proj.index("<= set(p)") < proj.index("type(p['pid'])") < proj.index("key = (p['pid']"))
check('counter_reasons',all(s in proj for s in ['PROCESS_COUNTER_SCHEMA','PROCESS_COUNTER_KEYS','PROCESS_COUNTER_IDENTITY_TYPE']))
check('only_typed_projection_exception_caught', 'except ResourceConnectionError as exc:' in newdefs['resource_decision'] and 'except Exception' not in newdefs['resource_decision'])
check('assessor_after_projection',newdefs['resource_decision'].index('project_owned_sample(') < newdefs['resource_decision'].index('control.assess_resources('))
check('no_new_time_budget',all(s not in new for s in ['7200','9000','stop_reserve_s']))
check('huge_clock_rejection','except OverflowError:' in newdefs['finite_time'] and 'return False' in newdefs['finite_time'])
for f in readj(B/'CODE_MANIFEST.json')['files']:
 if f['path'] not in ['candidate/resource_connection.py.inactive.txt','candidate/resource_connection.py.inactive.txt.diff.txt','LIMITED_VALIDATION_PLAN.json']:
  check('unchanged_candidate_member:'+f['path'],(R/f['path']).read_bytes()==(B/f['path']).read_bytes())
for p in [R/'candidate/raw_connection.py.inactive.txt',B/'reference/r1/candidate/control.py.inactive.txt',B/'reference/r1/candidate/consumer.py.inactive.txt']:
 ast.parse(p.read_text());check('python_ast:'+str(p.relative_to(R)),True)
check('native_inactive',all(readj(R/'NATIVE_CONNECTION_STATUS.json')[k] is False for k in ['native_ready','approved','usable']))
check('native_commands_null',readj(R/'NATIVE_CONNECTION_STATUS.json')['actual_native_argv'] is None and readj(R/'NATIVE_CONNECTION_STATUS.json')['actual_native_cwd'] is None)
check('four_open_retained',len(readj(R/'OPEN_CONNECTION_MAP.json')['unresolved'])==4)
before=readj(R/'evidence/SELECTED_SOURCES_BEFORE.json');after=[]
for f in before['files']:
 now=identity(pathlib.Path(f['path']));after.append(now);check('original_preserved:'+f['path'],now==f)
put(R/'evidence/SELECTED_SOURCES_AFTER_STATIC.json',{'files':after,'unique_paths':len(set(x['path'] for x in after))})
diff=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='prior_preparation/candidate/resource_connection.py.inactive.txt',tofile='OPEN_R1/candidate/resource_connection.py.inactive.txt'))
(R/'candidate/resource_connection.py.inactive.txt.diff.txt').write_text(diff,encoding='utf-8',newline='')
spans=[]
def span(p,name,a,b,kind='function'):
 raw=p.read_bytes();lines=raw.splitlines(keepends=True);section=b''.join(lines[a-1:b]);norm='\n'.join(raw.decode('utf-8-sig').splitlines()[a-1:b]).encode('utf-8')
 spans.append({'id':name,'path':str(p.relative_to(R)).replace('\\','/'),'first_line':a,'last_line':b,'byte_start_inclusive':sum(map(len,lines[:a-1])),'byte_end_exclusive':sum(map(len,lines[:b])),'raw_span_sha256':sha(section),'lf_no_final_lf_sha256':sha(norm),'source_bytes':len(raw),'source_sha256':sha(raw),'kind':kind})
for p in [R/'candidate/resource_connection.py.inactive.txt',R/'candidate/raw_connection.py.inactive.txt',B/'reference/r1/candidate/control.py.inactive.txt',B/'reference/r1/candidate/consumer.py.inactive.txt']:
 tree=ast.parse(p.read_text());prefix=p.name.split('.')[0]
 def walk(nodes,parents=''):
  for n in nodes:
   if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
    first=min([n.lineno]+[d.lineno for d in n.decorator_list]);span(p,prefix+'.'+parents+n.name,first,n.end_lineno)
    if isinstance(n,ast.ClassDef):walk(n.body,parents+n.name+'.')
 walk(tree.body)
 for i,line in enumerate(p.read_text().splitlines(),1):
  if any(s in line for s in ['OS_QUERY_FAILURE','CLOCK_ORIGIN_MISMATCH','PROCESS_COUNTER_SCHEMA','PROCESS_COUNTER_KEYS','PROCESS_COUNTER_IDENTITY_TYPE','STOP_METHOD_NOT_APPROVED','STOP_OWNERSHIP_LOST','QUADRATURE_METHOD_OPEN','QUADRATURE_PAYLOAD_BINDING','QUADRATURE_GRID_OR_SCOPE','STOP_RESERVE_ENTERED']):span(p,prefix+'.guard_line_'+str(i),i,i,'reason_site')
frag=R/'candidate/InstalledReadback.fragment.java.inactive.txt'
for n,a,b in [('s1OpenProperties',4,13),('s1OpenConfiguredReadback',14,26),('s1OpenStoredGrid',27,38)]:span(frag,n,a,b)
j=B/'reference/r1/candidate/variants/P0.java.inactive.txt'
for n,a,b in [('T_END_SECONDS',17,17),('TIMES',28,28),('checkShape',30,37),('TIME_ORIGIN_throw',34,34),('units',38,42),('evaluatedUnits',43,49),('quote',63,63),('table',64,73),('evaluate',338,349),('readSetting',493,509),('unknown_type_throw',507,507)]:span(j,'P0.'+n,a,b,'java_exact_extraction')
put(R/'FUNCTION_SPANS.json',{'normalization':'Inclusive one-based lines; CRLF/CR normalized to LF; preserve indentation; UTF-8 no BOM, no final LF. raw_span includes original line endings. Whole source SHA distinct.','status':'STATIC_EXTRACTION_MAP_ONLY_NOT_EXECUTED','spans':spans})
put(R/'STATIC_CHECKS.json',{'method':'Own AST/hash/text/data checks only; no candidate imports/calls, no functional cases','count':len(checks),'matched':sum(c['matched'] for c in checks),'all_matched':all(c['matched'] for c in checks),'checks':checks})
ph=readj(R/'PHASE_RECORDS.json');tick=int(time.perf_counter()*10000000);ph['static'].update(end_ticks=tick,elapsed_s=(tick-ph['static']['start_ticks'])/10000000);put(R/'PHASE_RECORDS.json',ph)
print(json.dumps({'static_checks':len(checks),'all_matched':all(c['matched'] for c in checks),'static_elapsed_s':ph['static']['elapsed_s'],'function_spans':len(spans),'functional_tests':0}))
if not all(c['matched'] for c in checks):raise SystemExit(1)
if ph['static']['elapsed_s']>ph['static']['limit_s']:raise SystemExit('STATIC_BUDGET_EXCEEDED')
