"""New R1 JSON/text writer only, no candidate calls."""
from pathlib import Path
import json
OUT=Path(__file__).resolve().parents[1]
def read(n): return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def write(n,x): (OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
b=read('contracts/EXECUTION_BINDING.json')
old=OUT.parent/'microshort_s1o_20261007_133011'
cmd=b['unit']['commands']
cmd['cwd']=str(OUT).replace('\\','/')
for key in ('argv','parent_argv'):
    cmd[key]=[s.replace(str(old).replace('\\','/'),str(OUT).replace('\\','/')) for s in cmd[key]]
b['unit']['paths']['source_root']=str(OUT).replace('\\','/')
b['current_validation_engine_observation']['source']='reference/ORIGINAL_VALIDATION_PLAN.json (historical observation; not re-observed as functional-engine evidence in R1)'
b['r1_scope']={'id':'S1O-R1-N1-N4','functional_validation':'NOT_RUN','current_plan':'VALIDATION_PLAN_R1.json','original_manifest_sha256':'54c61d10b3bb11e0501e9933b220eca76d9f7cee503953a6f909185e04f965fe','inactive_path_update':'Source-interface paths point to this R1 copy only. No operational native command, output or authorization path was created.'}
b['r1_parent_projection']={
 'status':'STATIC_CONTRACT_ONLY_ADAPTER_OPEN',
 'Expected':{'common_requested_times_s':'Full fixed registered vector from POLICY_VARIANTS.request_vectors[comparison.expected_common_request_vector].tokens_s; immutable binding, canonical decimal strings; never copied from result count','required_count':'Count of full registered vector, NOT safe-prefix count','end_s':'Fixed exact configured endpoint'},
 'Native':{'stored_times_s':'Actual complete raw-native saved vector; strictly increasing finite decimal strings, from0 through actual end','stored_grid_identity':'Raw saved-grid evidence path/positive integer bytes/SHA; same registered source identity consumed by Python','final_time_s':'Actual final saved time; exact','guard_pair':'For PROTECTIVE_STOP_MATCHED: t_minus/t_plus, t_plus=actual endpoint<configured end, pair are last two stored states; retain stop operator/units/domain/no-post-integration proof'},
 'consumer_native_projection':'Same immutable raw evidence projected as native.stored_times_s/stored_grid_identity/last_stored_s/reason/guard_pair. Schema conversion is not native verification; adapter remains OPEN.',
 'comparison':'Normal: fixed complete vector. Protective: derive fixed vector prefix <= verified t_minus. Comparison grid must exactly match; full intersection remains separate, strictly ordered, includes every compared time and is subset of actual native grid (may include t_plus).',
 'charge':'S1O_CHARGE_BUDGET_R1 in CHARGE_BALANCE.json; full actual native grid, not safe comparison prefix; source/global Li binding and signed adjacent intervals consumed.',
 'precision':'Exact decimal strings and integers for new grid and comparison checks; float/double/CLR decimal transport rejected as precision-ambiguous. No tolerance change. Existing budget double checks unchanged.'}
write('contracts/EXECUTION_BINDING.json',b)
l=read('SOURCE_CONTRACT_LINKS.json')
l['consumer_inputs']['charge_balance']='CHARGE_BALANCE R1: mandatory complete native grid/global rows/same-source identities/endpoints/units; exact same-time Li; cumulative balance plus adjacent signed dqN/dqP with unchanged deadband. Raw adapter OPEN.'
l['consumer_inputs']['analyze']='R1 normalized native grid/readbacks/data identities bound to run+manifest; full charge interval includes protective t_plus, comparison safe prefix ends t_minus. Raw adapter OPEN.'
l['parent']='S1NativeAxis validates full actual grid and stop pair; S1Fields->S1ChargeFields and S1Coverage consume analyze evidence. Expected common grid is fixed independently; normal/full vs safe prefix distinguished. S1FinalReturn unchanged.'
l['precision']='Consumer Decimal50; parent R1 time/grid/comparison decisions use exact decimal lexemes and reject binary floating/CLR decimal transport. Existing budgets retain double. Functional boundary evidence is NOT_RUN; future exact fixtures required.'
l['current_validation_plan']='VALIDATION_PLAN_R1.json'
l['original_validation_plan']='reference/ORIGINAL_VALIDATION_PLAN.json'
write('SOURCE_CONTRACT_LINKS.json',l)
print(json.dumps({'kind':'R1_OFFLINE_SCHEMA_LINKS_WRITTEN','native_ready':False,'candidate_executed':False,'files':['contracts/EXECUTION_BINDING.json','SOURCE_CONTRACT_LINKS.json']}))
