from pathlib import Path
import hashlib, importlib.util, json, os, re, subprocess, sys

import argparse
parser = argparse.ArgumentParser(description="Independent mutants against verified actual consumer source")
parser.add_argument('--source', type=Path, required=True, help='Root containing frozen fixture script and evidence JSON')
parser.add_argument('--repo', type=Path, required=True, help='Read-only Git source repository')
parser.add_argument('--output', type=Path, required=True, help='New scratch output directory')
args = parser.parse_args()
FREEZE, OUT = args.source.resolve(), args.output.resolve()
OUT.mkdir(parents=True)
script = FREEZE / 'scripts/test_dem_gen2_t12_consumer_contract.py'
spec = importlib.util.spec_from_file_location('fixture_author', script)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
manifest = json.loads((FREEZE / h.EVIDENCE / 'source-manifest.json').read_text())
contract_path = FREEZE / h.EVIDENCE / 'p1-consumer-contract.json'

def once(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new, 1)

def rounding(text):
    old = text[text.index('def _resume_integer(x):'):text.index('def _csv(path, cols):')]
    return once(text, old, 'def _resume_integer(x):\n    return _i(x)\n\n\n')

def no_first_priority(text):
    start, end = text.index('def _s0_dump('), text.index('def _s0_frame(')
    part = once(text[start:end], '            return None, s0', '            continue')
    return text[:start]+part+text[end:]

def rewrite_input(text):
    start, end = text.index('def read_run('), text.index('def parent_sums(')
    part = text[start:end]
    before, sep, after = part.rpartition('    return out')
    assert sep
    insertion = "    with open(os.path.join(d, 'ul_events.csv'), 'a', encoding='utf-8') as mutated:\n        mutated.write('\\n')\n"
    return text[:start]+before+insertion+sep+after+text[end:]

mutations = [
    ('resume_rounding', 'ul_reader.py', rounding),
    ('s0_fallback_past_corrupt', 'ul_reader.py', no_first_priority),
    ('s0_ignores_requested_step', 'ul_reader.py', lambda s: once(s, " and d['step'] == s0 and len(set(ids)) == len(ids)", " and len(set(ids)) == len(ids)")),
    ('atom_ignores_requested_step', 'ul_reader.py', lambda s: once(s, "    if A['step'] != step:", '    if False:')),
    ('gravity_dispatch_removed', 'ul_reader.py', lambda s: once(s, "    return P['g_aux'] if job.startswith('G_') else P['s3']['g']", "    return P['s3']['g']")),
    ('history_difference_ignored', 'ul_reader.py', lambda s: once(s, 'if x is None or y is None or abs(x - y) > max(rel * abs(x), floor):', 'if x is None or y is None:')),
    ('g2c_missing_column_is_failure', 'ul_gates.py', lambda s: once(s, "out['status'] = 'NOT_COMPUTED'   # ULPR-04", "out['status'] = 'FAIL'   # ULPR-04")),
    ('raw_input_rewritten', 'ul_reader.py', rewrite_input),
]
def raw_preflight_removed(s):
    start = s.index('    if os.path.isfile(event_path):')
    end = s.index('    ev, pr = _csv(event_path', start)
    return s[:start] + s[end:]


def raw_preflight_splitlines(s):
    start = s.index('    if os.path.isfile(event_path):')
    end = s.index('    ev, pr = _csv(event_path', start)
    part = once(s[start:end], ".read().split('\\n')", '.read().splitlines()')
    return s[:start] + part + s[end:]


def manifest_guard(s, filter_first=False):
    start = s.index("            if any(c in ln for c in ")
    end = s.index("            line = ln.strip", start)
    if filter_first:
        return s[:start] + "            if not ln.strip().startswith('resume_from='):\n                continue\n" + s[start:]
    return s[:start] + s[end:]

mutations += [
    ('raw_marker_preflight_removed', 'ul_reader.py', raw_preflight_removed),
    ('auth_ignores_marker_problems', 'ul_reader.py', lambda s: once(s, 'if pr or marker_pr else _resume_auth(d, events)', 'if pr else _resume_auth(d, events)')),
    ('manifest_separator_guard_removed', 'ul_reader.py', manifest_guard),
    ('manifest_key_filter_before_separator', 'ul_reader.py', lambda s: manifest_guard(s, True)),
    ('raw_marker_preflight_splitlines', 'ul_reader.py', raw_preflight_splitlines),
]
expected_failures = {
    'resume_rounding': {'resume_fractional_k_precision', 'resume_fractional_step_precision', 'resume_fractional_state_precision'},
    's0_fallback_past_corrupt': {'s0_corrupt_first_no_fallback'},
    's0_ignores_requested_step': {'s0_filename_is_not_step'},
    'atom_ignores_requested_step': {'atom_wrong_step'},
    'gravity_dispatch_removed': {'gravity_G_UB'},
    'history_difference_ignored': {'wall_delta_max_changed'},
    'g2c_missing_column_is_failure': {'contact_missing_column'},
    'raw_input_rewritten': {'resume_exact_scientific'},
    'raw_marker_preflight_removed': {'resume_single_leading_ls_raw_csv'},
    'auth_ignores_marker_problems': {'resume_marker_leading_ascii_space', 'resume_single_leading_ls_raw_csv'},
    'manifest_separator_guard_removed': {'resume_manifest_embedded_nel', 'resume_manifest_embedded_ls', 'resume_manifest_embedded_ps'},
    'manifest_key_filter_before_separator': {'resume_manifest_embedded_nel', 'resume_manifest_embedded_ls', 'resume_manifest_embedded_ps'},
    'raw_marker_preflight_splitlines': {'resume_single_leading_ls_raw_csv'},
}
child = '''
from pathlib import Path
import importlib.util,json,sys
script,source,fixtures,contract = map(Path,sys.argv[1:])
spec=importlib.util.spec_from_file_location('fixture_author',script)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
sys.path.insert(0,str(source))
import ul_reader,ul_gates,ul_lib,ul_s3
cases=h.run_probes(fixtures,ul_reader,ul_gates,ul_lib,ul_s3,json.loads(contract.read_text()))
print(json.dumps({'failed':[x['case'] for x in cases if not x['pass']], 'case_count':len(cases)}))
'''
reports=[]
for name, filename, change in mutations:
    dest=OUT/name
    source, fixtures=dest/'source',dest/'fixtures'
    source.mkdir(parents=True); fixtures.mkdir()
    verified=h.snapshot(args.repo,manifest,source)
    target=source/filename
    raw=target.read_text()
    target.write_text(change(raw))
    r=subprocess.run([sys.executable,'-I','-c',child,str(script),str(source),str(fixtures),str(contract_path)],capture_output=True,text=True)
    observation=json.loads(r.stdout) if r.returncode==0 else {'error':r.stderr}
    reports.append({'mutation':name,'source_verified_before_mutation':verified[filename],
                    'mutant_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                    'returncode':r.returncode,'observation':observation,
                    'expected_failed_cases':sorted(expected_failures[name]),
                    'detected':r.returncode == 0 and observation.get('case_count') == 52 and expected_failures[name].issubset(observation.get('failed', []))})
(OUT/'report.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps(reports,indent=2))

raise SystemExit(0 if all(x['detected'] for x in reports) else 1)
