"""Independent static/data review; never imports or runs repository modules."""
import ast
import copy
import difflib
import hashlib
import json
import re
from pathlib import Path

H=Path(__file__).resolve().parent
R=H/'reference'
O=H.parent/'gate86_review_20261001/reference'
C=[]
def txt(p): return p.read_bytes().decode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(d): return json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def save(name,d): (H/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def check(n,b):
    C.append({'check':n,'pass':bool(b)})
    if not b:
        save('REVIEW_AUDIT_FAILURE.json',C)
        raise AssertionError(n)
def parsed(path): return ast.parse(txt(path))
def fun(tree,name): return next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==name)
def astsame(a,b): return ast.dump(ast.Module(body=a,type_ignores=[]),include_attributes=False)==ast.dump(ast.Module(body=b,type_ignores=[]),include_attributes=False)
def nondoc(f):
    b=f.body
    return b[1:] if b and isinstance(b[0],ast.Expr) and isinstance(b[0].value,ast.Constant) and isinstance(b[0].value.value,str) else b
def body(path,name):
    t=parsed(path); n=fun(t,name)
    return '\n'.join(txt(path).splitlines()[n.lineno-1:n.end_lineno])
pv=parsed(R/'tools/preserve.py'); oldpv=parsed(O/'tools/preserve.py'); ft=parsed(R/'src/fitting.py')
new=nondoc(fun(pv,'leg_run_spec')); expanded=[]
for node in new:
    if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='_check_leg_axes':
        expanded.extend(nondoc(fun(pv,'_check_leg_axes')))
    else: expanded.append(node)
check('V2 builder inlined AST exactly unchanged',astsame(expanded,nondoc(fun(oldpv,'leg_run_spec'))))
for name in ['_claim_planned_leg','resume_claim','assert_run_is_authorized','LegClaim','finalize_leg']:
    if name=='LegClaim':
        a=next(n for n in ast.walk(oldpv) if isinstance(n,ast.ClassDef) and n.name==name)
        b=next(n for n in ast.walk(pv) if isinstance(n,ast.ClassDef) and n.name==name)
    else:a=fun(oldpv,name);b=fun(pv,name)
    check('Unchanged authority AST '+name,ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False))
for name in ['_stage3_preflight','_prepare_stage3','_assert_fit_input_is_authorized','_record_phase','_run_fit_locked']:
    check('Unchanged existing fitting guard '+name,ast.dump(fun(parsed(O/'src/fitting.py'),name),include_attributes=False)==ast.dump(fun(ft,name),include_attributes=False))
check('io byte identical',(R/'src/io.py').read_bytes()==(O/'src/io.py').read_bytes())
check('design_wire byte identical',(R/'tools/design_wire.py').read_bytes()==(O/'tools/design_wire.py').read_bytes())

# Restricted literal evaluator for fixture data only: no Call, Attribute, Name, import, eval or exec.
def lit(n):
    if isinstance(n,ast.Constant): return n.value
    if isinstance(n,ast.Dict): return {lit(k):lit(v) for k,v in zip(n.keys,n.values)}
    if isinstance(n,(ast.List,ast.Tuple)): return [lit(x) for x in n.elts]
    if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Mult):
        a,b=lit(n.left),lit(n.right)
        if isinstance(a,str) and type(b) is int and 0<=b<=64:return a*b
    raise ValueError('Not permitted fixture literal: '+ast.dump(n))
f49=next(n.value for n in parsed(R/'tests/test_preserve.py').body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_F49' for t in n.targets))
f=lit(f49); k='results/g87_golden';f.update({'in':k,'out':k})
g={'config_digest':'a'*16,'condition_ids_sha256':'b'*16,'n_conditions':12,'discharged_cache_sha256':'ab'*32,'out':k}
v5={'leg_spec_version':2,'leg_id':'g87_golden','grid':g,'fit':f}
gold=sha(canon(v5))
check('Independent v5 fixture canonical SHA',gold=='b8f90ad97a7509f72742f0962c50646787171fb0214ea83478c9e597117073b4')
ledger=txt(R/'docs/22p_gap/LEG_PRESERVATION.yaml')
oldledger=txt(O/'docs/22p_gap/LEG_PRESERVATION.yaml')
ledgerdiff=list(difflib.unified_diff(oldledger.splitlines(True),ledger.splitlines(True),fromfile='Gate86/ledger',tofile='Gate87/ledger'))
(H/'LEDGER.diff').write_text(''.join(ledgerdiff),encoding='utf-8')
changed_lines=[l[1:].strip() for l in ledgerdiff if l.startswith(('+','-')) and not l.startswith(('+++','---'))]
check('Ledger changes only validator/core anchors',len(changed_lines)==8 and all(l.startswith(('source_digest:','verification_receipt_core_sha256:')) for l in changed_lines))
check('Operational v5 address unchanged','0838df841ae7e4e6' in ledger and '0838df841ae7e4e6' in oldledger)
check('No operational v6 plan slots',not re.search(r'^\s+(planned_envelope|stage3_context):',ledger,re.M))
claim=(R/'docs/22p_gap/CLAIM_STATUS.yaml').read_bytes()
auth=json.loads(txt(H/'evidence/AUTH_TO_HEAD.json'))
check('Claim status unchanged since pre-code specification',not any(f['filename'].endswith('/CLAIM_STATUS.yaml') for f in auth['files']))
save('V5_COMPATIBILITY.json',{'golden':gold,'operational_grid_digest_prefix':'0838df841ae7e4e6','operational_grid_scope':'Existing spec bytes/address unchanged; not independently reserialized from YAML','builder_inlined_AST_same':True,'authority_AST_same':True,'planned_entries_unchanged':True,'received_code_execution':False})

receipts=[]
for leg,n in [('paired_fixed5_v4',35),('grid_fit_v5',34)]:
    rel='docs/22p_gap/receipts/'+leg+'.validate.yaml'
    now=(R/rel).read_bytes(); hist=(R/('docs/22p_gap/receipts/history/'+leg+'.validate.f1f4378f46610f08.yaml')).read_bytes()
    check('Exact receipt history '+leg,hist==(O/rel).read_bytes())
    a=hist.decode();b=now.decode()
    d=list(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='history/'+leg,tofile='current/'+leg))
    rows=[l[1:].strip() for l in d if l.startswith(('+','-')) and not l.startswith(('+++','---'))]
    delta=sorted(set(l.split(':',1)[0] for l in rows))
    check('Only stated receipt differences '+leg,len(rows)==8 and delta==['core_sha256','generated_at_utc','validator_commit','validator_source_digest'])
    def scalar(key):
        vals=re.findall(r'^\s*'+re.escape(key)+r':\s*(\S+)\s*$',b,re.M)
        check('Unique scalar '+leg+'/'+key,len(vals)==1)
        return vals[0]
    core=scalar('core_sha256')
    check('Receipt validator and count '+leg,scalar('validator_source_digest')=='864edfb73b9695a1' and int(scalar('n_checks'))==n)
    check('Core and validator anchored '+leg,core in ledger)
    receipts.append({'leg':leg,'core_sha256_declared':core,'file_sha256':sha(now),'diff_fields':delta,'n_checks':n,'stamp_text':b.split('\nstamp:\n')[1]})
    (H/(leg+'_RECEIPT.diff')).write_text(''.join(d),encoding='utf-8')
save('RECEIPT_COMPARISON.json',{'receipts':receipts,'scope':'Exact historical bytes, restricted text/scalar comparisons and declared ledger anchors; core hash not independently regenerated; no restore or re-receipting.'})

base=R/'docs/22p_gap/gate87_evidence'
logtexts={p.name:txt(p) for p in base.glob('*.log')}
full=logtexts['13_full_replay_7fbaa45b_run2_374_of_374_rc0.log']
counts={'hit':len(re.findall(r'^물었다\s',full,re.M)),'survived':len(re.findall(r'^★ 안 물었다',full,re.M)),'error':len(re.findall(r'^★ 실행오류',full,re.M)),'declared':len(re.findall(r'^신고\s',full,re.M))}
check('Full mutation markers 374/0/0/11',counts=={'hit':374,'survived':0,'error':0,'declared':11})
check('Full replay totals and rc',all(s in full for s in ['scenario_total 385','site_total 423','ran 374','replay rc=0']))
partial=logtexts['12_full_replay_7fbaa45b_attempt1_cut_at_2h_254_of_374.log']
check('Partial replay is 254 only',len(re.findall(r'^물었다\s',partial,re.M))==254 and '124' in partial)
py=logtexts['10_full_pytest_7fbaa45b_2109passed.log'];sm=logtexts['11_smoke_7fbaa45b_rc0.log']
check('Full pytest log matches',all(s in py for s in ['7fbaa45b1f2a217a41272426260f75bdabf62a28 dirty=0','2109 passed, 1 xfailed','pytest rc=0']))
check('Smoke rc0','rc=0' in sm)
check('RED52/11','52 failed, 11 passed' in logtexts['01_red_test_gate87_round2b.log'])
check('GREEN63 twice',all('63 passed' in logtexts[k] for k in ['04_green_63passed.log','06_green_after_witness_fix_63passed.log']))
first=logtexts['07_replay_g87_round1_emit_expect_3survived.log']
survivors=re.findall(r'^([^\s:]+-g87): 변이 rc 가 1\(시험 실패\)이 아니다 \(0\)',first,re.M)
check('Actual 3 first survivors',len(survivors)==3)
verify=logtexts['09_replay_g87_verify_expect_rc0.log']
check('Final g87 mutation22',len(re.findall(r'^물었다\s',verify,re.M))==22 and 'rc=0' in verify)
save('LOG_AUDIT.json',{'pytest':{'passed':2109,'xfailed':1,'rc':0,'head':'7fbaa45b1f2a217a41272426260f75bdabf62a28','clean_start_declared_in_log':True},'smoke_rc':0,'full_replay':counts,'partial_replay':{'hit':254,'rc':124,'not_acceptance':True},'first_g87_survivors':survivors,'final_g87':22,'remote_process_independently_observed':False,'scope':'Checked preserved source log content and SHA, no reviewer rerun.'})

mt=parsed(R/'docs/22p_gap/mutation_replay.py');muts=[]
source={'PRESERVE':txt(R/'tools/preserve.py'),'FITTING':txt(R/'src/fitting.py'),'RUNSH':txt(R/'run.sh')}
for node in ast.walk(mt):
    if isinstance(node,ast.Tuple) and len(node.elts)==5 and isinstance(node.elts[0],ast.Constant) and isinstance(node.elts[0].value,str) and node.elts[0].value.endswith('-g87'):
        name=node.elts[0].value; target=node.elts[1].id;pre=ast.literal_eval(node.elts[2]);hits=source[target].count(pre)
        check('Unique mutation preimage '+name,hits==1)
        muts.append({'name':name,'target':target,'line':node.lineno,'preimage_occurrences':hits,'selector':ast.literal_eval(node.elts[4])})
check('22 static mutation registrations',len(muts)==22)
save('MUTATION_STATIC.json',{'registrations':muts,'replay_by_reviewer':False})

# Pin every link of G87-N1 without executing the received functions.
facts={
 'shell_fit_only':'if [[ "$MODE" != "fit" ]]; then' in txt(R/'run.sh'),
 'claim_starts_with_empty_phases':'"phases": {}' in body(R/'tools/preserve.py','_claim_planned_leg'),
 'fit_declared_external_input_can_pass_without_grid_receipt':'if declared is None:' in body(R/'src/fitting.py','_assert_fit_input_is_authorized') and 'got = fit_input_package_digest(got_map)' in body(R/'src/fitting.py','_assert_fit_input_is_authorized'),
 'phase_order_fixed_grid_fit':'CLAIM_PHASES = ("grid", "fit")' in txt(R/'tools/preserve.py'),
 'fit_completion_requires_predecessor':'_before = _order[:_order.index(phase)]' in body(R/'tools/preserve.py','phase_done') and '_open = [p for p in _before if p not in _have]' in body(R/'tools/preserve.py','phase_done') and 'if _open:' in body(R/'tools/preserve.py','phase_done'),
 'commit_before_phase_done':body(R/'src/fitting.py','_run_fit_staged').index('commit_run_outputs(_exec_cap, [logical_out])') < body(R/'src/fitting.py','_run_fit_staged').index('_record_phase(claim, "fit", summary, logical_out)'),
 'record_phase_skips_if_no_claim':'if claim is None:\n        return' in body(R/'src/fitting.py','_record_phase'),
 'smoke_claim_none':'return (None, live_fit,' in body(R/'src/fitting.py','_assert_fit_authorized'),
 'grid_gate_uses_v2':'spec = leg_run_spec(leg, live_grid, declared.get("fit") or {})' in body(R/'src/grid.py','_assert_grid_authorized'),
 'v2_builder_version2':'"leg_spec_version": 2' in body(R/'tools/preserve.py','leg_run_spec'),
 'claim_compares_spec_digest':'if e["run_spec_digest"] != want:' in body(R/'tools/preserve.py','_claim_planned_leg'),
 'finalize_also_requires_all_phases':'missing = [p for p in CLAIM_PHASES' in body(R/'tools/preserve.py','finalize_leg'),
 'positive_claim_test_stops_before_run_fit':'F._assert_fit_authorized(' in body(R/'tests/test_gate87_round2b.py','test_s02_04_a_matching_v3_plan_and_context_reach_claim_issuance') and 'F.run_fit(' not in body(R/'tests/test_gate87_round2b.py','test_s02_04_a_matching_v3_plan_and_context_reach_claim_issuance'),
 'positive_completion_test_uses_smoke':'smoke namespace → 승인 면제' in body(R/'tests/test_gate87_round2b.py','test_s04_01_the_entrypoint_builds_the_context_from_the_ledger_and_run_fit_completes'),
 's02_input_fixture_is_curves_hash_only':'hashlib.sha256((in_dir / "curves.parquet").read_bytes()).hexdigest()' in body(R/'tests/test_gate87_round2b.py','_live_pair'),
}
for k,v in facts.items():check('N1 source fact '+k,v)
locations=[]
for path,names in [('src/fitting.py',['_assert_fit_input_is_authorized','_assert_fit_authorized','_record_phase','_run_fit_staged']),('tools/preserve.py',['_claim_planned_leg','phase_done','finalize_leg']),('src/grid.py',['_assert_grid_authorized'])]:
    t=parsed(R/path)
    for name in names:
        n=fun(t,name); locations.append({'path':path,'function':name,'start':n.lineno,'end':n.end_lineno})
save('G87_N1_STATIC_TRACE.json',{'finding':'G87-N1','severity':'P1','kind':'Static call/data-flow counterexample, not an executed production probe','facts':facts,'locations':locations,'preconditions':['Fresh prospective v3 plan, correct source identity, external input package digest and v4 envelope/design, isolated non-smoke authority/output','No predecessor grid receipt for this new claim; fit computation hypothetically returns successfully'], 'trace':['New claim phases={}','Matching external input package accepted without a same-claim grid receipt','run_fit and native stage3 checks are not skipped','After successful fit, commit_run_outputs precedes _record_phase(fit)','phase_done(fit) computes predecessors=[grid], absent=[grid], raises PreserveError before writing fit receipt','finalize also refuses missing grid/fit; legacy grid entry builds v2 spec, mismatching v3 claim'], 'test_gap':['s02_04 ends at claim issuance','s04_01 is smoke: claim=None, _record_phase returns','Use fit_input_package_digest(_fit_input_digests(staged input)), not the existing s02 fixture curves-only hash, for the requested new non-smoke regression'], 'not_claimed':['No production/research run was executed by reviewer','No claim about an already-run real v6 leg or numeric error']})
save('REVIEW_AUDIT.json',{'checks':C,'passed':sum(c['pass'] for c in C),'received_code_executions':0,'project_tests':0,'COMSOL':0,'finding':'G87-N1 P1 STATIC','scope':'Byte/AST/data/log checks only, not functional validation.'})
print(json.dumps({'checks':len(C),'logs':13,'mutations_static':len(muts),'v5_golden':gold,'finding':'G87-N1 P1: fit-only vs required grid predecessor'}))
