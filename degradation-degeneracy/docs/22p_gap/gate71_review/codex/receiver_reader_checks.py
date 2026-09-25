"""Receiver-only, bounded reader probes; no project import, writer, restore, or solve.

Compiles only named, reviewed AST definitions from the fixed source. The src.io
import in the receipt reader is replaced with the independently measured digest.
This does NOT exercise the complete module, Linux mount checks, attach or promotion.
"""
from pathlib import Path
import ast, copy, hashlib, json, re, secrets, sys, types, unicodedata
import yaml

OUT = Path(__file__).resolve().parent
DD = Path('C:/Users/Administrator/Documents/Codex/g71_20260925/degradation-degeneracy')
SOURCE = DD / 'tools/preserve.py'
raw = SOURCE.read_bytes()
tree = ast.parse(raw, filename=str(SOURCE))
names = {'PreserveError', '_is_hex64', '_nonempty_str',
         '_repo_relative_or_refuse', '_receipt_core_sha256',
         'read_verification_receipt', '_typed_exec_class_record', '_declared_index'}
constants = {'_HEX64', 'EXEC_CLASSES', 'EXEC_CLASS_SMOKE', 'EXEC_CLASS_CANONICAL',
             'EXEC_CLASS_RECORD_KEYS_MODERN', 'EXEC_CLASS_RECORD_KEYS_LEGACY',
             '_EXEC_CLASS_RECORDED_AT'}
selected = []
for n in tree.body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names:
        selected.append(n)
    elif isinstance(n, ast.Assign):
        assigned = {t.id for t in n.targets if isinstance(t, ast.Name)}
        if assigned & constants or any(x.startswith('VERIFICATION_RECEIPT_') for x in assigned):
            selected.append(n)
assert {n.name for n in selected if isinstance(n, (ast.FunctionDef, ast.ClassDef))} == names
g = {'Path': Path, 'hashlib': hashlib, 'secrets': secrets, 'unicodedata': unicodedata,
     're': re, 'REPO_ROOT': DD}
exec(compile(ast.Module(body=selected, type_ignores=[]), str(SOURCE)+'[SELECTED_READERS_ONLY]', 'exec'), g)

measurement = json.loads((OUT/'IDENTITY.json').read_text(encoding='utf-8'))
fake_src = types.ModuleType('src')
fake_io = types.ModuleType('src.io')
fake_io.source_digest = lambda: measurement['source_digest_independent_byte_calculation']
sys.modules['src'] = fake_src
sys.modules['src.io'] = fake_io

scratch = OUT/'receiver_readonly_inputs'
scratch.mkdir(exist_ok=False)
base_path = DD/'docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml'
base = yaml.safe_load(base_path.read_bytes())
leg = base['core']['leg_id']
results = []
def case(name, mutate=None, corrupt_hash=False):
    rec = copy.deepcopy(base)
    if mutate:
        mutate(rec['core'])
    rec['core_sha256'] = g['_receipt_core_sha256'](rec['core'])
    if corrupt_hash:
        rec['core_sha256'] = '0'*64
    p = scratch/(name+'.yaml')
    p.write_bytes(yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, width=100).encode('utf-8'))
    item = {'id': name, 'input_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    try:
        got = g['read_verification_receipt'](p.name, leg, repo_root=scratch)
        item['reader_outcome'] = 'ACCEPTED'
        item['core_returned_unchanged'] = got == rec['core']
    except g['PreserveError'] as exc:
        item['reader_outcome'] = 'REJECTED'
        item['reason'] = str(exc)
    results.append(item)
    return rec

case('R00_real_receipt_control')
case('R01_wrong_leg_control', lambda c: c.update(leg_id='different_leg'))
case('R02_wrong_core_hash_control', corrupt_hash=True)
case('R03_validator_fail_control', lambda c: c['validation'].update(ok=False))
single = case('R04_missing_sealed_summary', lambda c: c.update(outputs=[c['outputs'][0]]))
def mismatch(c):
    c['outputs'][1]['semantic_sha256'] = '0'*64
different = case('R05_disagreeing_semantic_pair', mismatch)
case('R06_wrong_source_fits', lambda c: c['outputs'][0].update(source_file_sha256='0'*64))
case('R07_wrong_restore_run', lambda c: c['restore'].update(run_dir_relative='results/ANOTHER_RUN'))
case('R08_nonhex_semantic', lambda c: c['outputs'][0].update(semantic_sha256='not-a-digest'))
case('R09_missing_source_fits', lambda c: c['outputs'][0].pop('source_file_sha256'))
case('R10_declared_identity_null', lambda c: c['identity'].update(make_receipt_sha256=None))

# The producer's PURE output-consistency predicate, without build/restore/scoring.
producer_source = DD/'docs/22p_gap/make_receipt.py'
pt = ast.parse(producer_source.read_bytes(), filename=str(producer_source))
pn = next(n for n in pt.body if isinstance(n, ast.FunctionDef) and n.name=='_outputs_agree')
pg = {}
exec(compile(ast.Module(body=[pn], type_ignores=[]), str(producer_source)+'[PURE_PREDICATE_ONLY]', 'exec'), pg)
producer_results = []
for name, rec in [('P00_real_pair', base), ('P01_single_output', single), ('P02_different_pair', different)]:
    try:
        value = pg['_outputs_agree'](rec['core']['outputs'])
        producer_results.append({'id':name, 'outcome':'ACCEPTED', 'value':value})
    except SystemExit as exc:
        producer_results.append({'id':name, 'outcome':'REJECTED', 'reason':str(exc)})

# E5 closure: read the records only; never call registration or promotion.
records = []
for p in sorted((DD/'docs/22p_gap/_exec_class').glob('*.json')):
    rec = json.loads(p.read_bytes())
    g['_typed_exec_class_record'](rec, p.stem, str(p))
    records.append(p.name)
cid = 'a'*64
modern = {'content_id':cid, 'execution_class':'canonical', 'evidence':'control',
          'recorded_at':'2026-09-25T00:00:00Z', 'sealed':True}
e5 = []
for name, rec in [
    ('C00_modern', modern),
    ('C01_legacy', {k:v for k,v in modern.items() if k!='sealed'}),
    ('C02_two_keys', {'content_id':cid, 'execution_class':'canonical'}),
    ('C03_ill_typed', dict(modern, sealed=[], evidence=17, recorded_at=False, extra=1)),
    ('C04_nonbool_sealed', dict(modern, sealed='true')),
]:
    try:
        g['_typed_exec_class_record'](rec, cid, 'in-memory fixture')
        e5.append({'id':name, 'outcome':'ACCEPTED'})
    except g['PreserveError'] as exc:
        e5.append({'id':name, 'outcome':'REJECTED', 'reason':str(exc)})

# Parse the actual production index and independently rehash its members as DATA.
bundle = DD/'artifacts/paired_fixed5_v4'
idx = bundle/'payload_sha256.yaml'
mapping, why = g['_declared_index'](idx)
assert mapping and why is None and all(v is not None for v in mapping.values())
walked = {p.relative_to(bundle).as_posix() for p in bundle.rglob('*') if p.is_file() and p != idx}
assert walked == set(mapping)
mismatches = [name for name, want in mapping.items() if hashlib.sha256((bundle/name).read_bytes()).hexdigest()!=want]
assert not mismatches
unknown = scratch/'unsupported_index.json'
unknown.write_bytes(b'{}\n')
unknown_got, unknown_why = g['_declared_index'](unknown)
assert unknown_got is None

assert [r['reader_outcome'] for r in results[:4]] == ['ACCEPTED', 'REJECTED', 'REJECTED', 'REJECTED']
assert all(r['reader_outcome']=='ACCEPTED' for r in results[4:])
assert [r['outcome'] for r in producer_results] == ['ACCEPTED','REJECTED','REJECTED']
assert [r['outcome'] for r in e5] == ['ACCEPTED','ACCEPTED','REJECTED','REJECTED','REJECTED']
report = {
    'scope':'Selected exact AST readers and one pure producer predicate; src.io digest stubbed to independent measurement. Not a full module/attach/restore/promotion run.',
    'source_sha256':hashlib.sha256(raw).hexdigest(),
    'selected_definitions':[{ 'name':getattr(n,'name',None), 'line':n.lineno, 'end_line':n.end_lineno} for n in selected],
    'reader_cases':results, 'producer_pure_predicate_cases':producer_results,
    'exec_class_cases':e5, 'historical_registry_records_typed_only':len(records),
    'actual_bundle_data_check':{'index_members':len(mapping),'exact_set':True,'hash_mismatches':mismatches,
                              'unsupported_index_result':unknown_got,'unsupported_index_reason':unknown_why},
    'attach_calls':0,'restores':0,'class_writes':0,'calculations':0,'project_module_imports':0,
    'reviewer_input_fixture_writes':len(results)+1,
}
(OUT/'READER_CHECKS.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
print(json.dumps({'receipt_reader':[(r['id'],r['reader_outcome']) for r in results],
                  'producer':producer_results, 'exec_class_cases':e5, 'registry_records':len(records),
                  'actual_bundle':report['actual_bundle_data_check'], 'scope':report['scope']},ensure_ascii=False,indent=2))
