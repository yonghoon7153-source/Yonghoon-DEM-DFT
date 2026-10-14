"""Offline SUPR-01 probes: real plan/digest/log/receipt functions, synthetic preflight status.

Does not call preflight(), cmd_run(), a numerical solver, WSL, or git mutation.
Only evidence/digest_probe outputs are created. Source files are read-only.
"""
from pathlib import Path
import contextlib
import copy
import hashlib
import io
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import types

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / 'source'
OUT = BASE / 'evidence' / 'digest_probe'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(SRC / 'scripts'))
import supp20_input_receipt as S
N = S.NP
PIN = 'df647d4e31224e1a270dae01dd41f91af3048361'
RESULTS = []


if '--raw-log-version' in sys.argv:
    version = sys.argv[sys.argv.index('--raw-log-version') + 1]
    log_name = sys.argv[sys.argv.index('--log-name') + 1]
    module = S
    if version == 'baseline':
        def load(name, file):
            spec = importlib.util.spec_from_file_location(name, file)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            spec.loader.exec_module(mod)
            return mod
        old_np = load('baseline_network_digest_probe', BASE / 'baseline/scripts/run_network_194_parallel.py')
        old_s = load('baseline_receipt_digest_probe', BASE / 'baseline/scripts/supp20_input_receipt.py')
        old_np.ROOT = SRC
        old_s.REPO = SRC
        old_s.NP = old_np
        module = old_s
    log_path = SRC / 'docs/reviews/codex_sup20_fix_reverify_evidence_20261014/evidence/receipt_extra' / (log_name + '.log')
    sys.exit(module.main(['--dry-run-log', str(log_path), '--json', str(OUT / (version + '_' + log_name + '_cli.json'))]))


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')


def bad(result):
    return sorted(c['id'] for c in result['checks'] if not c['ok'])


def check(name, actual, expected):
    RESULTS.append(dict(name=name, actual=actual, expected=expected, pass_=actual == expected))


def fixture(tag, cohorts, specs=None):
    """Use actual build_plan, plan_input_digest, print_preflight and record producer."""
    rp, lp, root = OUT / (tag + '.json'), OUT / (tag + '.log'), OUT / ('root_' + tag)
    argv = ['run', '--root', str(root), '--cohorts', ','.join(cohorts), '--dry-run', '--observe-imports', '--preflight-receipt', str(rp)]
    args = N._parse(argv)
    plan = N.build_plan(cohorts, specs or N.cohort_specs(args), args.case, args.order)
    dg = N.plan_input_digest(plan)
    pf = dict(cpu=dict(cpu_count=8, cpu_affinity=8), lanes=4,
              mem=dict(MemTotal_GB=32, MemAvailable_GB=30, SwapFree_GB=0, SwapTotal_GB=0),
              mem_budget_mb=0, first_lanes_est_mem_GB=1, est_mem_largest_mb=100,
              disk_free_GB=100, disk_need_GB=10, est_serial_h=1, est_makespan_h=0.25,
              git=dict(sha=PIN, short=PIN[:9], branch='SYNTHETIC_OFFLINE', dirty=False, porcelain=[]),
              n_raw_problems=0, generation=dict(generation='g2', problems=[], modes=['hertz', 'physics', 'hertz_h12']),
              dependency_closure=dict(files=list(N.CODE_FILES), errors=[]), lazy_census=dict(n_lazy=90, unclassified=[]),
              fork_census=[], input_digest=dg, warn=[], stop=[])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        printed = N.print_preflight(pf, plan, args, root)
        print(N.PREFLIGHT_COMPLETE_MARK)
    b = buf.getvalue().encode('utf-8')
    rec = N._preflight_receipt_record(args, argv, dict(pf=pf, plan=plan, printed=printed, completed=True, stage='complete'),
                                      0, b, lp, rp, 'SYNTHETIC_START', 'SYNTHETIC_END')
    lp.write_bytes(b)
    save(rp, rec)
    return rp, plan, dg


def verify(path, expected='supp20', approved=PIN):
    return N.preflight_receipt_checks(path, expect_set=expected, approved_sha=approved)


def echecks(result, dg=None, reg=None):
    rr = S._Receipt()
    S._preflight_registration_checks(rr, result, dg or N.plan_input_digest(S.plan_for()), reg or S.registration_values()[0])
    return dict(checks=rr.checks)


def alter(src, tag, digest_edit):
    rec = json.loads(src.read_text(encoding='utf-8'))
    text = Path(rec['log']['path']).read_text(encoding='utf-8')
    dg = copy.deepcopy(rec['input_digest'])
    digest_edit(dg)
    # Keep the edited log and record self-consistent to isolate value/schema checks.
    rec['input_digest'] = dg
    line = N.INPUT_DIGEST_LINE + ' ' + json.dumps(dg, sort_keys=True, separators=(',', ':'))
    text = re.sub(r'(?m)^\s*INPUT_DIGEST_JSON .*$', '  ' + line, text)
    lp, rp = OUT / (tag + '.log'), OUT / (tag + '.json')
    data = text.encode('utf-8')
    lp.write_bytes(data)
    rec['log'] = dict(path=str(lp), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), encoding='utf-8')
    save(rp, rec)
    return rp


normal, plan20, dg20 = fixture('supp20_normal', ['lhss'])
v = verify(normal)
check('normal P0-P10', bad(v), [])
check('normal E1-E2', bad(echecks(v)), [])
for reg_key in ['n', 'ids_sha256', 'raw_sha256_table_sha256', 'cohort_tsv_sha256', 'code_fp']:
    changed_reg = S.registration_values()[0]
    changed_reg[reg_key] = 21 if reg_key == 'n' else '0' * 64
    check('normal receipt vs different registration ' + reg_key, bad(echecks(v, reg=changed_reg)),
          ['E2'] if reg_key == 'code_fp' else ['E1'])

alt = SRC / 'docs/reviews/codex_sup20_fix_reverify_evidence_20261014/evidence/receipt_extra/alternate_cohort.tsv'
specs = N.cohort_specs(types.SimpleNamespace())
specs['lhss']['cohort'] = str(alt)
alternate, _, dg_alt = fixture('supp20_old_alternate_tsv', ['lhss'], specs)
v_alt = verify(alternate)
check('old alternate TSV content hash', N.sha256_file(alt), '8d5dcbd28061327f7c4f8c1a0b8915647c368236a78ced0c5ed7c3693100f1d4')
check('old alternate same ids/raw', [dg_alt[k] for k in ('n', 'ids_sha256', 'raw_sha256_table_sha256')],
      [dg20[k] for k in ('n', 'ids_sha256', 'raw_sha256_table_sha256')])
check('old alternate rejected by values', sorted(bad(v_alt) + bad(echecks(v_alt))), ['E1', 'P9'])

for key in N.INPUT_DIGEST_KEYS:
    p = alter(normal, 'missing_' + key, lambda d, k=key: d.pop(k))
    vv = verify(p)
    check('missing digest key ' + key, sorted(bad(vv) + bad(echecks(vv))), ['E1', 'P2', 'P9'])
p = alter(normal, 'unknown_digest_key', lambda d: d.update(unregistered='x'))
vv = verify(p)
check('unknown digest key', sorted(bad(vv) + bad(echecks(vv))), ['E1', 'P2', 'P9'])
p = alter(normal, 'cross_cohort_mapping', lambda d: d.update(cohort_tsv_sha256={'lhs': d['cohort_tsv_sha256']['lhss']}))
vv = verify(p)
check('cohort SHA key crossed', sorted(bad(vv) + bad(echecks(vv))), ['E1', 'P9'])
check('supp20 receipt as production194', bad(verify(normal, 'production194')), ['P6', 'P9'])

for approved, want in [(PIN, []), (PIN[:7], []), (PIN.upper(), []), ('0' * 40, ['P10']), ('xyz1234', ['P10']), (PIN[:6], ['P10'])]:
    check('approved SHA ' + approved, bad(verify(normal, approved=approved)), want)
no_sha = verify(normal, approved=None)
check('approved SHA absent warning', [bad(no_sha), len(no_sha['warnings'])], [[], 1])

normal194, plan194, dg194 = fixture('production194_normal', ['lhs', 'lhsx'])
check('production194 normal P0-P10', bad(verify(normal194, 'production194')), [])
check('production194 receipt as supp20', bad(verify(normal194)), ['P6', 'P9'])
doc = (SRC / 'docs/reviews/lhs_network_batch_registration_20261007_g2.md').read_text(encoding='utf-8')
reg194 = {
    'n': int(re.search(r'^\| 케이스 수 \| (\d+)', doc, re.M)[1]),
    'ids_sha256': re.search(r'^\| `ids_sha256`[^\n]+\| `([a-f0-9]{64})`', doc, re.M)[1],
    'raw_sha256_table_sha256': re.search(r'^\| `raw_sha256_table_sha256`[^\n]+\| `([a-f0-9]{64})`', doc, re.M)[1],
    'missing_raw_sha': [],
    'cohort_tsv_sha256': dict(re.findall(r'(lhsx?) `([a-f0-9]{64})`', next(line for line in doc.splitlines() if line.startswith('| 코호트 TSV sha256')))),
}
check('production194 actual committed digest = approved registration section 2', dg194, reg194)

# Demonstrate the documented boundary: different default inputs remain ID-registered,
# so P9 alone cannot certify preregistered raw/TSV values. No source files are changed.
specs = copy.deepcopy(N.COHORT_SPECS)
cohort_copy = OUT / 'production194_altered_cohort.tsv'
cohort_copy.write_bytes((SRC / specs['lhs']['cohort']).read_bytes() + b'\n')
harvest_copy = OUT / 'production194_altered_harvest'
harvest_copy.mkdir(exist_ok=True)
for p in (SRC / specs['lhs']['harvest']).glob('*.json'):
    shutil.copyfile(p, harvest_copy / p.name)
first = next(p for p in sorted(harvest_copy.glob('*.json')) if not p.name.startswith('_'))
j = json.loads(first.read_text(encoding='utf-8'))
j['raw']['atom']['sha256'] = 'a' * 64 if j['raw']['atom']['sha256'] != 'a' * 64 else 'b' * 64
save(first, j)
specs['lhs'].update(cohort=str(cohort_copy), harvest=str(harvest_copy))
old_specs = N.COHORT_SPECS
try:
    only_tsv = copy.deepcopy(old_specs)
    only_tsv['lhs']['cohort'] = str(cohort_copy)
    N.COHORT_SPECS = only_tsv
    changed_tsv194, _, dg194_tsv = fixture('production194_same_ids_raw_other_tsv', ['lhs', 'lhsx'])
    v_tsv194 = verify(changed_tsv194, 'production194')
    N.COHORT_SPECS = specs
    altered194, _, dg194_alt = fixture('production194_selfconsistent_other_inputs', ['lhs', 'lhsx'])
    vv = verify(altered194, 'production194')
finally:
    N.COHORT_SPECS = old_specs
check('194 same IDs/raw but different TSV passes internal P0-P10 with changed default input', bad(v_tsv194), [])
check('194 manual preregistered-value comparison catches TSV-only change',
      sorted(k for k in N.INPUT_DIGEST_KEYS if dg194_tsv[k] != reg194[k]), ['cohort_tsv_sha256'])
check('194 documented selfconsistent-current-input boundary P0-P10', bad(vv), [])
check('194 manual preregistered-value comparison catches changed inputs',
      sorted(k for k in N.INPUT_DIGEST_KEYS if dg194_alt[k] != reg194[k]), ['cohort_tsv_sha256', 'raw_sha256_table_sha256'])
check('194 same altered receipt on real pinned inputs fails P9', bad(verify(altered194, 'production194')), ['P9'])


def manifest(path, plan, dg):
    hashes = N.code_hashes()
    m = dict(schema=N.SCHEMA, launch_format=N.LAUNCH_FORMAT, plan=plan, input_digest=dg, code_hashes=hashes,
             code_dependency_closure=list(N.CODE_FILES), handover_code_hashes={rel: N.sha256_file(N.ROOT / rel) for rel in N.HANDOVER_FILES},
             git=dict(sha=PIN, short=PIN[:9], dirty=False), observe_imports=True, import_obs_run_id='cd' * 16,
             generation_probe=dict(generation='g2', problems=[]), **{N.GEN_KEY: 'g2'},
             seal=dict(schema=N.LAUNCH_SEAL_SCHEMA, launch_format=N.LAUNCH_FORMAT, code_fp=N.code_fp(hashes), files=len(hashes), **{N.GEN_KEY: 'g2'}))
    save(path, m)
    return path


ms = manifest(OUT / 'supp20_manifest.json', plan20, dg20)
mp = manifest(OUT / 'production194_manifest.json', plan194, dg194)
for approved, wanted in [(PIN, []), (PIN[:7], []), ('0' * 40, ['F7', 'G7']), ('xyz1234', ['F7', 'G7'])]:
    rr = S._Receipt()
    reg = S.registration_values()[0]
    S._manifest_checks(rr, 'F', ms, 'supp20', reg, dg20, approved_sha=approved)
    S._manifest_checks(rr, 'G', mp, 'production194', reg, approved_sha=approved)
    check('manifest F7/G7 approval ' + approved, bad(dict(checks=rr.checks)), wanted)

raw_logs = ['wrong_tsv_full_log', 'wrong_tsv_registered_grep', 'observation_off_full_log',
            'observation_off_truncated_before_stop', 'missing_three_prerequisite_lines']
raw_log_results = []
for name in raw_logs:
    row = dict(name=name)
    for version in ['baseline', 'fixed']:
        p = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(Path(__file__).resolve()),
                            '--raw-log-version', version, '--log-name', name], capture_output=True, encoding='utf-8')
        (OUT / (version + '_' + name + '_cli.log')).write_text(p.stdout + p.stderr, encoding='utf-8')
        row[version] = p.returncode
    raw_log_results.append(row)
    check('old raw-log CLI baseline->fixed ' + name, [row['baseline'], row['fixed']],
          [1 if name == 'observation_off_full_log' else 0, 1])

summary = dict(pin=PIN, method='Offline synthetic preflight status; real input planning, hashing, log producer, receipt record and validators. No actual dry-run or numerical/WSL execution.',
               source_digest20=dg20, source_digest194=dg194, registered194=reg194, altered_digest194=dg194_alt,
               raw_log_cli=raw_log_results, results=RESULTS, passed=sum(r['pass_'] for r in RESULTS), total=len(RESULTS))
save(OUT / 'results.json', summary)
print(json.dumps(dict(passed=summary['passed'], total=summary['total'], failures=[r for r in RESULTS if not r['pass_']]), ensure_ascii=False))
sys.exit(0 if summary['passed'] == summary['total'] else 1)
