"""Reviewer-owned data checks. Never imports or executes received source."""
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = 'bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/candidate/'
REQ = 'bms-balancing/docs/COMSOL_BMIN640_R2_NATIVE150_APPROVAL_REQUEST_20261006.md'
snap = json.loads((HERE / 'RECEIVED_SNAPSHOT.json').read_text(encoding='utf-8'))
files = snap['files']
checks = []
identities = {}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def check(name, condition, detail=None):
    checks.append({'check': name, 'status': 'MATCH' if condition else 'MISMATCH', 'detail': detail})

def data(path):
    return files[ROOT + path]['content']

def js(path):
    return json.loads(data(path))

for path, item in files.items():
    raw = item['content'].encode('utf-8')
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()
    identities[path] = {'bytes': len(raw), 'sha256': sha(raw), 'git_blob': blob}
    check('received Git blob ' + path, blob == item['sha'])
    if path.startswith(ROOT):
        check('same candidate blob at origin and initial request ' + path,
              blob == snap['historical_candidate_blobs'][path])

revised = snap['revised_request']
raw = revised['content'].encode('utf-8')
blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
check('revised request Git blob', blob == revised['sha'])
identities['revised_request'] = {'bytes': len(raw), 'sha256': sha(raw), 'git_blob': blob}

local = Path('C:/Users/Administrator/Desktop/COMSOL_BMIN640_R2_NATIVE150_APPROVAL_REQUEST_20261006.md')
local_bytes = local.read_bytes()
check('local attachment matches initial request byte for byte', local_bytes == files[REQ]['content'].encode('utf-8'))
identities['local_attachment'] = {'path': str(local), 'bytes': len(local_bytes), 'sha256': sha(local_bytes)}
check('amendment diff leaves candidate tree unchanged',
      not any(p.startswith(ROOT) for p in snap['changes_to_revised_request']['changed_files']))

m, c, command_map, field_spec = (js(p) for p in ['CODE_MANIFEST.json', 'CONTRACT.json', 'COMMAND_MAP.json', 'NATIVE_APPROVAL_FIELD_SPEC.json'])
manifest_sha = sha(data('CODE_MANIFEST.json').encode('utf-8'))
check('manifest identity', manifest_sha == '4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25')
check('manifest has exactly five unique members', len(m['files']) == len({r['file'] for r in m['files']}) == 5)
for row in m['files']:
    raw = data(row['file']).encode('utf-8')
    check('manifest member ' + row['file'], len(raw) == row['bytes'] and sha(raw) == row['sha256'])
check('inactive flags remain false', all(x['approved'] is False and x['usable'] is False for x in [m, c, field_spec]))
check('command map and approval field spec bind manifest', command_map['manifest_sha256'] == field_spec['code_manifest_sha256'] == manifest_sha)
check('field spec binds run and exact approval paths', field_spec['run_id'] == c['run_id'] and field_spec['future_approval_path'] == c['approval_path'] and field_spec['future_release_path'] == c['release_path'])
check('native argv map equals contract', all(command_map['native'][p]['argv'] == c['commands'][p] for p in ['compile', 'batch']))
check('native cwd equals run root', all(command_map['native'][p]['cwd'] == c['run_root'] for p in ['compile', 'batch']))
check('parent and Python cwd equal contract', all(command_map[p]['cwd'] == c['cwd'] for p in ['parent', 'execute', 'analyze']))
check('approval commands and budgets equal contract', field_spec['required_future_fields']['commands'] == c['commands'] and field_spec['required_future_fields']['budgets_seconds'] == c['budgets_seconds'])
check('six stage budgets sum to overall', sum(v for k, v in c['budgets_seconds'].items() if k != 'overall') == c['budgets_seconds']['overall'] == 10500)
check('five protected future paths', len(command_map['not_created_paths']) == len(set(command_map['not_created_paths'])) == 5)
check('external pins 16 with sha256 size and path', len(c['external_source_pins']) == 16 and all(re.fullmatch('[0-9a-f]{64}', r['sha256']) and isinstance(r['bytes'], int) and r['path'] for r in c['external_source_pins']))
check('NORMAL480 baseline nine pinned run tables', len(c['baseline_files']) == 9 and all('/normal480_offline_preparation_20261001/future_run_001/tables/' in r['path'] and re.fullmatch('[0-9a-f]{64}', r['sha256']) and r['bytes'] > 0 for r in c['baseline_files'].values()))

requested = [Decimal(t) for t in c['requested_times_s']]
primary = [Decimal(t) for t in c['primary_comparison_times_s']]
check('requested 1637 distinct ordered times 0 to 150', len(requested) == 1637 and requested == sorted(set(requested)) and requested[0] == 0 and requested[-1] == 150)
check('primary exactly 301 times 120 to 150 every 0.1', primary == [Decimal(120) + Decimal(i) / 10 for i in range(301)] and c['primary_comparison_count'] == 301 and set(primary) <= set(requested))
check('241 distinct ordered coordinates per electrode', all(len(v) == 241 and [Decimal(x) for x in v] == sorted({Decimal(x) for x in v}) for v in c['coordinates'].values()))
check('comparison limits unchanged', c['limits']['voltage_V'] == '0.001' and c['limits']['surface_x'] == '0.0001')
check('fresh solve one loadCopy zero', c['fresh_t0'] is True and c['runAll_calls'] == 1 and c['loadCopy_calls'] == 0 and Decimal(c['maximum_physical_s']) == 150)
java = data('src/Bmin640Candidate.java')
tlist = re.search(r'm\.study\("std1"\)\.feature\("time"\)\.set\("tlist","([^"]+)"\)', java)
check('Java requested times match contract', bool(tlist) and [Decimal(t) for t in tlist.group(1).split()] == requested)
check('Java one literal runAll call', java.count('.runAll()') == 1)

parent = data('PARENT_COMMAND.ps1')
ps_pin = re.search(r"BHash \(Join-Path \$PSHOME 'powershell.exe'\)\) -cne '([0-9a-f]{64})'", parent)
if not ps_pin:
    ps_pin = re.search(r"'([0-9a-f]{64})'.*POWERSHELL", parent)
check('parent embeds expected PS hash', '8bb6fa8c283b4d92120b1ef249a9b311b0f804d4cabbe9981159976c8be76a5e' in parent)
check('stopwatch starts before PARENT_START record', parent.index('$bClock=[Diagnostics.Stopwatch]::StartNew()') < parent.index("BSave 'PARENT_START.json'"))
check('POST_WRITE outside stopped transcript', parent.index('Stop-Transcript') < parent.index('USER_PARENT_FINAL_RETURN'))
check('NoExit is explicit and outer rc null', '-NoExit' in command_map['parent']['argv'] and command_map['parent']['completion_boundary']['outer_powershell_exit_code'] is None)
check('amended separate packaging and preexec limits present', '1,800 s' in revised['content'] and '≤ 50 MB' in revised['content'] and 'bmin640_native150_preexec_20261006/' in revised['content'])
check('native policy change prohibited', c['policy']['changes_allowed'] is False and c['policy']['effective_readback'] == 'UNVERIFIED')

out = {'scope': 'Received text bytes, JSON values, exact arithmetic, static source strings only. Not functional tests or execution-machine observations.',
       'status': 'MATCH' if all(x['status'] == 'MATCH' for x in checks) else 'MISMATCH',
       'checks_count': len(checks), 'mismatches': [x for x in checks if x['status'] != 'MATCH'],
       'identities': identities, 'checks': checks,
       'candidate_execution': 0, 'native_execution': 0, 'execution_machine_preflight': 0}
(HERE / 'STATIC_CHECKS_FINAL.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: out[k] for k in ['scope', 'status', 'checks_count', 'mismatches']}, ensure_ascii=False))
raise SystemExit(0 if out['status'] == 'MATCH' else 1)
