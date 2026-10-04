"""Reviewer-owned data and source-text checks. Never imports or executes received code."""
import csv
import hashlib
import io
import json
import re
import zipfile
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = json.loads((HERE / 'REFERENCE_TEXT.json').read_text(encoding='utf-8'))
FILES = {x['path']: x for x in REF['files']}
BASE = 'bms-balancing/comsol_candidates/bmin_particle640_20261004/'

def source(name):
    return FILES[BASE + name]['content']

def obj(name):
    return json.loads(source(name))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def ident(raw):
    return {'bytes': len(raw), 'sha256': sha(raw)}

def read_hash(stream):
    h = hashlib.sha256()
    total = 0
    while chunk := stream.read(1024 * 1024):
        h.update(chunk)
        total += len(chunk)
    return {'bytes': total, 'sha256': h.hexdigest()}

def span(text, start, end):
    assert text.count(start) == 1, ('nonunique start', start, text.count(start))
    a = text.index(start)
    b = len(text) if end is None else text.index(end, a + len(start))
    return a, b

out = {'scope': 'source text, hashes, JSON and archived data only; no received code imported, parsed as code, compiled or executed', 'commit': REF['commit']}
out['github_blobs'] = []
for name, record in FILES.items():
    raw = record['content'].encode('utf-8')
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    out['github_blobs'].append({'path': name, **ident(raw), 'git_blob': blob, 'matches_connector_blob': blob == record['sha']})

manifest = obj('candidate/CODE_MANIFEST.json')
out['manifest'] = ident(source('candidate/CODE_MANIFEST.json').encode())
out['manifest_files'] = [{'file': r['file'], 'matches': ident(source('candidate/' + r['file']).encode()) == {'bytes': r['bytes'], 'sha256': r['sha256']}} for r in manifest['files']]
changes = obj('CHANGE_BOUNDARIES.json')
literals = obj('LITERAL_CHANGE_MAP.json')['files']
out['reverse'] = []
for name, spec in changes['files'].items():
    current_raw = source('candidate/' + name).encode()
    original_raw = source('basis/source480/candidate/' + spec['basis']).encode()
    current = current_raw.decode().replace('\r\n', '\n')
    original = original_raw.decode().replace('\r\n', '\n')
    operations = []
    for op in spec['reverse']:
        if op['op'] == 'restore_block':
            a, b = span(current, *op['new'])
            x, y = span(original, *op['old'])
            operations.append({'op': op['op'], 'removed_normalized_bytes': b-a, 'restored_normalized_bytes': y-x})
            current = current[:a] + original[x:y] + current[b:]
        elif op['op'] == 'remove_insert':
            a, b = span(current, op['after'], op['before'])
            a += len(op['after'])
            operations.append({'op': op['op'], 'removed_normalized_bytes': b-a})
            current = current[:a] + current[b:]
        elif op['op'] == 'inverse_literals':
            key = op['table']
            for item in reversed(literals[key]):
                assert current.count(item['after']) == item['count'], (name, item['after'][:100], current.count(item['after']), item['count'])
                current = current.replace(item['after'], item['before'])
            operations.append({'op': op['op'], 'entries': len(literals[key]), 'occurrences': sum(x['count'] for x in literals[key])})
    restored = current.replace('\n', '\r\n').encode() if spec['line_endings'] == 'CRLF' else current.encode()
    nl_ok = current_raw.count(b'\n') == current_raw.count(b'\r\n') if spec['line_endings'] == 'CRLF' else b'\r' not in current_raw
    out['reverse'].append({'file': name, 'exact_basis_bytes': restored == original_raw, 'basis_sha256': sha(original_raw), 'restored_sha256': sha(restored), 'line_endings_match': nl_ok, 'operations': operations})

c = obj('candidate/CONTRACT.json')
old = obj('basis/source480/candidate/CONTRACT.json')
out['contract_diff'] = {'changed': [k for k in c.keys() & old.keys() if c[k] != old[k]], 'added': sorted(c.keys()-old.keys()), 'removed': sorted(old.keys()-c.keys())}
out['contract_diff']['changed'].sort()
expected = changes['json_files']['CONTRACT.json']
out['contract_diff']['matches_declarations'] = all(set(out['contract_diff'][k]) == set(expected[k]) for k in ('changed', 'added', 'removed'))
req = c['requested_times_s']
pri = [t for t in req if Decimal(120) <= Decimal(t) <= Decimal(150)]
out['contract_values'] = {'requested_count': len(req), 'prefix_exact': req == old['requested_times_s'][:1637], 'primary_count': len(pri), 'primary_exact': pri == c['primary_comparison_times_s'], 'primary_0p1_grid': [Decimal(t) for t in pri] == [Decimal(120)+Decimal(i)/10 for i in range(301)], 'coordinates_exact': c['coordinates'] == old['coordinates'], 'limits_exact': c['limits'] == old['limits'], 'runtime_requirements_exact': c['runtime_settings_required'] == old['runtime_settings_required'], 'native_budget_sum': sum(v for k,v in c['budgets_seconds'].items() if k != 'overall'), 'native_overall': c['budgets_seconds']['overall']}
plan = obj('LIMITED_VALIDATION_PLAN.json')
out['validation_plan'] = {'groups': len(plan['groups']), 'cases': sum(len(g['cases']) for g in plan['groups']), 'ids_unique': len({x['id'] for g in plan['groups'] for x in g['cases']}) == plan['cases'], 'budget_sum': sum(v for k,v in plan['budget_seconds'].items() if k!='overall'), 'budget_overall': plan['budget_seconds']['overall']}

archive = Path('C:/Users/Administrator/Downloads/COMSOL63_NORMAL480_NATIVE_RESULT_20261001.zip')
with archive.open('rb') as s:
    out['baseline_archive'] = {'path': str(archive), **read_hash(s)}
out['baseline_archive']['matches_scope'] = out['baseline_archive']['sha256'] == c['baseline_run']['result_zip']['sha256'] and out['baseline_archive']['bytes'] == c['baseline_run']['result_zip']['bytes']
with zipfile.ZipFile(archive) as z:
    out['basis_zip_comparison'] = []
    for name, record in FILES.items():
        prefix = BASE+'basis/source480/'
        if not name.startswith(prefix):
            continue
        member = name[len(prefix):]
        raw = z.read(member)
        out['basis_zip_comparison'].append({'member': member, 'byte_identical': raw == record['content'].encode(), **ident(raw)})
    result_raw = z.read('run/DIAGNOSTIC_RESULT.json')
    result = json.loads(result_raw)
    out['historical_paths'] = {'record': ident(result_raw), 'tables': []}
    out['baseline_tables'] = []
    for name, pin in c['baseline_files'].items():
        member = 'run/tables/'+name
        with z.open(member) as s:
            actual = read_hash(s)
        out['baseline_tables'].append({'member': member, **actual, 'matches_candidate_pin': actual == {'bytes': pin['bytes'], 'sha256': pin['sha256']}})
        recorded = result['tables_manifest'][name]
        out['historical_paths']['tables'].append({'name': name, 'path': recorded['path'], 'matches_candidate_full_pin': recorded == pin})
    console_matches = []
    console_sha = hashlib.sha256()
    at_start = True
    with z.open('run/batch_console.log') as s:
        while part := s.readline(65536):
            console_sha.update(part)
            if at_start and part.startswith((b'AXES_PARTICLE=', b'AXES_PHYSICAL_MESH_DOMAIN=', b'AXES_ACTUAL_MESH=')):
                console_matches.append(part.decode('utf-8').rstrip('\r\n'))
            at_start = part.endswith(b'\n')
    out['baseline_console'] = {'sha256': console_sha.hexdigest(), 'member_bytes': z.getinfo('run/batch_console.log').file_size, 'mesh_lines': console_matches, 'expected_lines_once': all(console_matches.count(x.replace('Nel=640','Nel=320')) == 1 for x in c['mesh_readback_required'])}
    batch = z.read('run/batch.log').decode('utf-8-sig')
    out['baseline_dof'] = re.findall(r'Number of degrees of freedom solved for: (\d+) \(plus (\d+) internal DOFs\)\.', batch)
    settings = list(csv.DictReader(io.StringIO(z.read('run/tables/axes_runtime_settings.csv').decode('utf-8-sig'))))
    out['baseline_settings'] = {'keys': [r['key'] for r in settings], 'count': len(settings)}

print(json.dumps(out, ensure_ascii=False, indent=2))
