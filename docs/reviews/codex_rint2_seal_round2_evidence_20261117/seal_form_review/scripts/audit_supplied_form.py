"""Independent byte/layout check; does not read result JSON or execute an engine."""
from pathlib import Path
import hashlib, json, re, shlex

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'input'
X = INPUT / 'extra/seal_candidate_v2_1'
BUILD = X / 'build_20261120'
manifest = json.loads((BUILD / '_manifest.json').read_bytes())
out = {'test_only': True, 'checks': {}, 'commands': {}}
def check(name, value):
    out['checks'][name] = bool(value)
    assert value, name
def digest(b):
    return hashlib.sha256(b).hexdigest()
for rel, expect in manifest['outputs'].items():
    raw = (BUILD / rel).read_bytes()
    check('output_hash:' + rel, digest(raw) == expect['sha256'])
    check('output_bytes:' + rel, len(raw) == expect['bytes'])
check('maker_hash', digest((X / 'make_sealed_copy.py').read_bytes()) == manifest['tool_sha256'])
for key, path in {
    'reg': INPUT / 'repo/docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md',
    'cmd': INPUT / 'repo/docs/reviews/rint2_kgy_commands_20261020.md',
    'reg_ins': X / 'registration_R_insert.md', 'cmd_ins': X / 'commands_doc_insert.md',
    'plan': X / 'plan_candidate.json',
    's0': INPUT / 'repo/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json',
}.items():
    check('input_hash:' + key, digest(path.read_bytes()) == manifest['inputs'][key]['sha256'])
reg_rel = 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md'
orig = (INPUT / 'repo' / reg_rel).read_bytes()
marked = (BUILD / reg_rel).read_bytes().splitlines(keepends=True)
check('marked_is_original_plus_one_line', b''.join(marked[:1]+marked[2:]) == orig)
plan_raw = (X / 'plan_candidate.json').read_bytes()
plan = json.loads(plan_raw)
check('canonical_plan', json.dumps(plan, indent=1, sort_keys=True).encode('ascii') == plan_raw)
check('candidate_four_null', all(plan[k] is None for k in ('max_ladder_points','calib_rj_ratio_max','sv_cf_threshold','sv_cf_scope')))
s0 = json.loads((INPUT / 'repo/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json').read_bytes())
check('known_tolerances_match', all(s0['values_um'][k] == plan['tol_ff_um'] for k in ('tol_ff','tol_P','tol_sj')))
check('known_policy_values', plan['exec_policy']['max_hours'] == 168 and plan['exec_policy']['max_attempts'] == 8 and plan['p2_extra'] == '--step3-maxiter 5000000')
sealed_rel = manifest['sealed_rel']
for label, rel, counts in [('sealed', sealed_rel, (13,1)), ('commands','docs/reviews/rint2_kgy_commands_20261020.md',(14,1)), ('original',reg_rel,(0,0))]:
    text = (BUILD / rel).read_text(encoding='utf-8')
    entries = []
    for block in re.finditer(r'^```sh\s*\n(.*?)^```\s*$', text, re.M|re.S):
        body_raw = block.group(1)
        body = re.sub(r'\\\n\s*', ' ', body_raw)
        base = text[:block.start(1)].count('\n') + 1
        for m in re.finditer(r'python3\s+\S+/(rint_r_chain|ca_s0_census)\.py\s+[^\n]*', body):
            command = m.group(0)
            command = re.sub(r'<[^<>]*>', 'FIXTURE', command)
            args = shlex.split(command)
            tool = m.group(1)
            opt = '--registration' if tool == 'rint_r_chain' else '--r-doc'
            wanted = '~/dem-ca1/' + sealed_rel if tool == 'rint_r_chain' else sealed_rel
            actual = args[args.index(opt)+1] if opt in args else None
            check(f'{label}:command{len(entries)+1}:{opt}', actual == wanted)
            entries.append({'block_start_physical_line':base,'logical_block_line':1+body[:m.start()].count('\n'),'tool':tool,'stage':args[args.index('--stage')+1],'registration':actual})
    check(label + '_command_count', (sum(e['tool']=='rint_r_chain' for e in entries),sum(e['tool']=='ca_s0_census' for e in entries)) == counts)
    out['commands'][label] = entries
out['overall']='PASS'
print(json.dumps(out, ensure_ascii=False, indent=2))
