"""Independent S02 diagnostics. Production files stay unmodified.

Original fixture scans run the real producer. Diagnostic fixture adjustments and
in-memory negative controls are explicitly labelled and never replace raw results.
"""
from pathlib import Path
import contextlib
import copy
import hashlib
import inspect
import io
import json
import math
import os
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
tmp = ROOT / 'tmp/s02_probe'
tmp.mkdir(parents=True, exist_ok=True)
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
os.environ['TEMP'] = os.environ['TMP'] = str(tmp)
sys.path[:0] = [str(ROOT / 'source/scripts'), str(ROOT / 'source/webapp'),
               str(WORK / 'lhs_coverage_review_20260930/deps'), str(WORK / 'gen2_network_reverify3_20261007/deps')]
import numpy as np
import scipy
import network_conductivity as nc
import tau_flux as tf
import test_l214r_r01_restored_full as submitted
from test_lhs214_model_limit import chain_bed, net3

OUT = dict(environment=dict(python=sys.version, platform=platform.platform(), numpy=np.__version__, scipy=scipy.__version__),
           source_pin='685c2bbdbbfee82898a9ec062bb9c2bc94612fc8', checks=[], logs={})
transcript = io.StringIO()


def mark(name, condition, detail=None):
    row = dict(name=name, ok=bool(condition), detail=detail)
    OUT['checks'].append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)


def shift(value, count):
    for _ in range(abs(count)):
        value = math.nextafter(value, math.inf if count > 0 else 0.0)
    return value


def produce(A, C, plate, bx, by):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1, plate, bx, by, None, contact_mode='hertzian')


def raw_from_record(rec):
    cert = rec['solve_certificate_full']
    geo = cert['geometry']
    # Independently spell out the same contracted arithmetic, no search helper.
    thick = geo['plate_z'] * geo['scale']
    area = geo['box_x'] * geo['box_y'] * geo['scale'] ** 2
    return (cert['I_bottom'] / cert['delta_V']) * thick / area


def section_capture(name, fn):
    submitted._ok, submitted._fail = 0, []
    log = io.StringIO()
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        fn()
    text = log.getvalue()
    OUT['logs'][name] = text
    transcript.write('\n=== ' + name + ' ===\n' + text)
    return dict(pass_count=submitted._ok, fail_count=len(submitted._fail), failures=list(submitted._fail))


def dynamic_replace(module, name, before, after):
    original = getattr(module, name)
    source = inspect.getsource(original)
    assert source.count(before) == 1, (name, before, source.count(before))
    # Definition executes in an isolated namespace sharing production globals.
    scope = dict(module.__dict__)
    exec(compile(source.replace(before, after), '<s02 in-memory negative control>', 'exec'), scope)
    setattr(module, name, scope[name])
    return original


start = time.perf_counter()
A, C, plate, _ = chain_bed(1.0, area=submitted.E_AREA)
original_bys = dict(submitted.E_BY)
OUT['registered_fixture'] = dict(area=submitted.E_AREA, bx=submitted.E_BX, by=original_bys, expected_q=submitted.E_Q)
OUT['original_records'] = {}
for label, by in original_bys.items():
    rec = produce(A, C, plate, submitted.E_BX, by)
    OUT['original_records'][label] = dict(by=by, raw=raw_from_record(rec), status=rec['sigma_full_status'], cert=rec['solve_certificate_full'])
mark('original fixture raw values all strictly below 1.5', all(v['raw'] < 1.5 for v in OUT['original_records'].values()),
     {k: v['raw'] for k, v in OUT['original_records'].items()})

# Exhaustively inspect the relevant representable box_y neighbourhood with the
# actual producer; no submitted search helper and no tolerance.
scan = []
for offset in range(-512, 513):
    by = shift(original_bys['eq'], offset)
    rec = produce(A, C, plate, submitted.E_BX, by)
    scan.append(dict(offset=offset, by=by, raw=raw_from_record(rec), status=rec['sigma_full_status'], I_bottom=rec['solve_certificate_full']['I_bottom']))
OUT['scan_1025'] = scan
hits = {label: [r for r in scan if r['raw'] == tgt] for label, tgt in submitted.E_Q.items()}
OUT['exact_hits'] = hits
mark('1025 real solves: next/equal present, prev has no representable input at fixed area/bx', bool(hits['next']) and bool(hits['eq']) and not hits['prev'],
     {k: [r['offset'] for r in v] for k, v in hits.items()})
mark('real q is non-increasing across scanned by; I_bottom unchanged',
     all(a['raw'] >= b['raw'] for a, b in zip(scan, scan[1:])) and len({r['I_bottom'] for r in scan}) == 1)
OUT['adjacent_skip'] = [r for r in scan if -21 <= r['offset'] <= -14]

# Re-run submitted search starting in both directions and beyond its cap.
OUT['registered_offsets'] = []
for offset in (0, 18, -18, 64, -64, 512, -512, 513, -513):
    by0 = {k: shift(v, offset) for k, v in original_bys.items()}
    found, steps, probs = submitted.find_boundary_inputs(nc, A, C, plate, submitted.E_BX, by0)
    row = dict(offset=offset, found=found, steps=steps, problems=probs)
    OUT['registered_offsets'].append(row)
    mark(f'original fixture offset {offset:+d}: unavailable prev is explicit failure', 'prev' in probs and 'prev' not in found, row)

# Positive fixture from the PRIOR independent review, which was explicitly
# disclosed there: do not present this result as the unmodified submission.
derived_area = 0.500000001001
derived_bys = dict(next=0.7281737983380614, eq=0.7281737983380615, prev=0.7281737983380616)
DA, DC, DP, _ = chain_bed(1.0, area=derived_area)
OUT['diagnostic_fixture'] = dict(area=derived_area, bx=submitted.E_BX, by=derived_bys, origin='prior independent rr_numeric_chain_boundary.json; not submitted defaults')
derived_raw = {k: raw_from_record(produce(DA, DC, DP, submitted.E_BX, by)) for k, by in derived_bys.items()}
mark('diagnostic fixture independently reproduces exact three raw q values', derived_raw == submitted.E_Q, derived_raw)
base_checks = submitted._e_checks(nc, tf, DA, DC, DP, submitted.E_BX, derived_bys)
mark('diagnostic fixture original E1-E4 all pass', len(base_checks) == 4 and all(cond for _, cond, _ in base_checks), base_checks)
OUT['diagnostic_offsets'] = []
for offset, cap in ((0, 0), (18, 512), (-18, 512), (64, 512), (-64, 512), (512, 512), (-512, 512), (513, 512), (-513, 512), (18, 0)):
    by0 = {k: shift(v, offset) for k, v in derived_bys.items()}
    found, steps, probs = submitted.find_boundary_inputs(nc, DA, DC, DP, submitted.E_BX, by0, cap=cap)
    row = dict(offset=offset, cap=cap, found=found, steps=steps, problems=probs)
    OUT['diagnostic_offsets'].append(row)
    expected_success = abs(offset) <= cap
    mark(f'diagnostic fixture offset {offset:+d}, cap {cap}: bounded search', (not probs) == expected_success, row)

# Helper failure states and independence of E5 from errors in E.
published = produce(DA, DC, DP, submitted.E_BX, derived_bys['eq'])
before = copy.deepcopy(published)
value, error = submitted._call(submitted.restore, published, 'hertz')
mark('restore computed record: explicit ValueError and no mutation', value is None and error.startswith('ValueError:') and 'q_withheld' in error and published == before, error)
e5_standalone = section_capture('E5 standalone', lambda: submitted.sec_E5({}))
mark('E5 standalone boundary control passes', e5_standalone['pass_count'] == 1 and e5_standalone['fail_count'] == 0, e5_standalone)
real_raw = submitted._e_raw_q
def raise_search(*args):
    raise RuntimeError('s02 deliberate solver exception')
try:
    submitted._e_raw_q = raise_search
    result = section_capture('E exception followed by E5', lambda: (submitted._guard('E', lambda: submitted.sec_E({})), submitted._guard('E5', lambda: submitted.sec_E5({}))))
finally:
    submitted._e_raw_q = real_raw
mark('E exception remains FAIL; E5 still executes and passes', result['pass_count'] == 1 and result['fail_count'] == 1 and 'RuntimeError' in result['failures'][0], result)

# Negative controls alter only functions held in this probe process. Numerical
# constants and source files remain untouched. Search must not bless a wrong
# publication policy or a removed consumer rejection.
OUT['negative_controls'] = []
for label, old, new in (
    ('producer_ge_instead_of_gt', 'reject = sigma_ratio > FULL_Q_GUARD_MAX', 'reject = sigma_ratio >= FULL_Q_GUARD_MAX'),
    ('producer_round_before_compare', 'reject = sigma_ratio > FULL_Q_GUARD_MAX', 'reject = round(sigma_ratio, 8) > FULL_Q_GUARD_MAX'),
    ('producer_guard_disabled', 'reject = sigma_ratio > FULL_Q_GUARD_MAX', 'reject = False'),
):
    original = dynamic_replace(nc, 'solve_network', old, new)
    try:
        found, steps, probs = submitted.find_boundary_inputs(nc, DA, DC, DP, submitted.E_BX, derived_bys)
        checks = submitted._e_checks(nc, tf, DA, DC, DP, submitted.E_BX, found) if not probs else []
        row = dict(label=label, search_found=found, search_problems=probs, assertions=checks)
        OUT['negative_controls'].append(row)
        mark(label + ': search succeeds but wrong policy is detected', not probs and any(not cond for _, cond, _ in checks), row)
    finally:
        nc.solve_network = original
original = dynamic_replace(tf, '_cert_published_problem', "if branch == 'full' and q_rec > nc.FULL_Q_GUARD_MAX:", "if False:")
try:
    checks = submitted._e_checks(nc, tf, DA, DC, DP, submitted.E_BX, derived_bys)
    result = section_capture('consumer guard disabled E5', lambda: submitted.sec_E5({}))
    row = dict(label='consumer_guard_disabled', assertions=checks, e5=result)
    OUT['negative_controls'].append(row)
    mark('consumer guard removed: E4 and independent E5 fail', not checks[3][1] and result['fail_count'] == 1, row)
finally:
    tf._cert_published_problem = original

OUT['production_file_identity'] = {}
for rel in ('scripts/network_conductivity.py', 'scripts/tau_flux.py'):
    oldbytes = (WORK / 'lhs214rr_recheck_20261019/source' / rel).read_bytes()
    newbytes = (ROOT / 'source' / rel).read_bytes()
    OUT['production_file_identity'][rel] = dict(equal=oldbytes == newbytes, sha256=hashlib.sha256(newbytes).hexdigest())
mark('producer and consumer files unchanged from baseline', all(x['equal'] for x in OUT['production_file_identity'].values()), OUT['production_file_identity'])
OUT['seconds'] = time.perf_counter() - start
OUT['summary'] = dict(passed=sum(c['ok'] for c in OUT['checks']), total=len(OUT['checks']))
(ROOT / 'evidence/s02_boundary.json').write_text(json.dumps(OUT, ensure_ascii=False, indent=2), encoding='utf8')
(ROOT / 'evidence/s02_boundary_sections.log').write_text(transcript.getvalue(), encoding='utf8')
print(json.dumps(dict(summary=OUT['summary'], seconds=OUT['seconds']), ensure_ascii=False))
sys.exit(0 if all(c['ok'] for c in OUT['checks']) else 1)
