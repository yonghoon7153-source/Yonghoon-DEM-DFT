#!/usr/bin/env python3
"""Read-only numerical breakdown; never an acceptance verdict or simulation."""
import array
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
from decimal import Decimal

COLUMNS = [f'c_cpl[{i}]' for i in range(1, 27)]
COMPONENTS = list(range(1, 7)) + list(range(10, 19)) + list(range(22, 27))
FAMILIES = ['positions'] * 6 + ['total_force'] * 3 + ['normal_force'] * 3 + ['tangent_force'] * 3 + ['area', 'delta'] + ['contact_point'] * 3
PERIODIC = {0, 1, 3, 4, 17, 18}
BOX = 0.05
REL = 1e-5
MAX_ROWS = 600000
MAX_LINE_BYTES = 8192
MAX_FILE_BYTES = 512 * 1024 * 1024
PIN = '4c29705fa1c4ba94737a858b206fa4f4c5bb2bde'
ROOT = Path('/home/yonghoon/ps45_unload_20261009')
KIT = ROOT / 'kit_20261026_221507_ps_7_3_r45_RJ_2kW5'
JOB = ROOT / 'ps_7_3_r45/RJ'
ORIGINAL = ROOT / 'ps_7_3_r45/in/contact_3200000.liggghts'
TEST = JOB / 'R/g2/contact_3200000.liggghts'
ORIGINAL_SHA = '53ae293b4586d091dfca58ab430c174f36b641dcd24678eb10d10fc3f416e65c'
SEAL_SHA = 'bb9f305f476815d7448ee5069ceb8fa3b9f138f3be1dc59703fcc8eec09c03bb'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact_id(token):
    if re.fullmatch(r'[+-]?[0-9]+', token):
        value = int(token)
    else:
        value = float(token)
        require(math.isfinite(value) and value.is_integer(), 'invalid pair ID: ' + token)
        require(Decimal(token) == Decimal(int(value)), 'rounded fractional pair ID: ' + token)
    require(0 < value <= 2**53, 'pair ID out of exact range: ' + token)
    return int(value)


def normalized(values, reverse):
    if reverse:
        values = values[3:6] + values[:3] + values[6:9] + [-x for x in values[9:18]] + values[18:]
    result = values[:6] + values[9:18] + values[21:26]
    for c in PERIODIC:
        result[c] %= BOX
    return result


def signature(stat):
    return (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)


def rows(path, metadata, expected_step=3200000):
    """Single standard local frame; strict errors, no skipped malformed rows."""
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        before = os.fstat(stream.fileno())
        require(before.st_size <= MAX_FILE_BYTES, 'file exceeds diagnostic byte cap')
        def line():
            raw = stream.readline(MAX_LINE_BYTES + 1)
            require(len(raw) <= MAX_LINE_BYTES, 'line exceeds diagnostic byte cap')
            require(bool(raw), f'{path}: unexpected EOF')
            h.update(raw)
            return raw.decode('utf-8').rstrip('\r\n')
        require(line() == 'ITEM: TIMESTEP', 'unexpected TIMESTEP header')
        step = int(line())
        require(step == expected_step, f'unexpected step {step}, expected {expected_step}')
        require(line() == 'ITEM: NUMBER OF ENTRIES', 'unexpected count header')
        declared = int(line())
        require(0 < declared <= MAX_ROWS, 'row count outside diagnostic limit')
        box_header = line()
        require(box_header.split()[:3] == ['ITEM:', 'BOX', 'BOUNDS'], 'unexpected BOX header')
        require(not {'xy', 'xz', 'yz'}.intersection(box_header.split()[3:]), 'tilted BOX header outside diagnostic subset')
        bounds = []
        for _ in range(3):
            values = line().split()
            require(len(values) == 2, 'non-orthogonal BOX record')
            lo, hi = map(float, values)
            require(math.isfinite(lo) and math.isfinite(hi) and lo < hi, 'invalid BOX bounds')
            bounds.append([lo, hi])
        require(line().split() == ['ITEM:', 'ENTRIES'] + COLUMNS, 'unexpected/missing/reordered contact columns')
        count = blanks = 0
        while True:
            raw = stream.readline(MAX_LINE_BYTES + 1)
            if not raw:
                break
            require(len(raw) <= MAX_LINE_BYTES, 'line exceeds diagnostic byte cap')
            h.update(raw)
            text = raw.decode('utf-8').strip()
            if not text:
                blanks += 1
                continue
            require(not text.startswith('ITEM:'), 'multiple frames')
            tokens = text.split()
            require(len(tokens) == 26, f'row {count + 1}: wrong width')
            i, j = exact_id(tokens[6]), exact_id(tokens[7])
            values = [float(t) for t in tokens]
            require(all(map(math.isfinite, values)), f'row {count + 1}: nonfinite value')
            count += 1
            require(count <= declared, 'more rows than declared')
            yield (min(i, j), max(i, j)), normalized(values, i > j), i > j
        require(count == declared, f'row count {count} != {declared}')
        require(signature(before) == signature(os.fstat(stream.fileno())) == signature(os.stat(path)), 'file changed while reading')
        metadata.update(path=str(path), bytes=before.st_size, sha256=h.hexdigest(), step=step,
                        rows=count, blank_lines=blanks, header_bounds=bounds,
                        comparison_box=[BOX, BOX], stat_signature=list(signature(before)), stat_before_after_stable=True)


def analyze(original, test, expected_original_sha=None):
    data = array.array('d')
    index = {}
    reversed_original = bytearray()
    provenance = {'original': {}, 'test': {}}
    discriminating = 0
    for key, values, reverse in rows(original, provenance['original']):
        require(key not in index, f'original duplicate pair {key}; diagnostic refuses duplicate changes')
        index[key] = len(index)
        data.extend(values)
        reversed_original.append(reverse)
        discriminating += math.sqrt(sum(values[c] ** 2 for c in (12, 13, 14))) > 0
    if expected_original_sha:
        require(provenance['original']['sha256'] == expected_original_sha, 'original SHA256 mismatch')
        require(provenance['original']['bytes'] == 149687008, 'original size mismatch')
    n = len(index)
    medians = []
    for c in range(20):
        column = sorted(abs(data[i]) for i in range(c, len(data), 20))
        med = column[n // 2] if n % 2 else (column[n // 2 - 1] + column[n // 2]) / 2
        require(math.isfinite(med), 'median arithmetic overflow')
        medians.append(med)
        del column
    seen = bytearray(n)
    counts = [dict(column=f'c_cpl[{c}]', family=family, first_fail=0, any_fail=0,
                   max_abs_delta=0.0, zero_threshold_fail=0, examples=[]) for c, family in zip(COMPONENTS, FAMILIES)]
    families = {f: {'first_fail': 0, 'any_fail': 0} for f in dict.fromkeys(FAMILIES)}
    force = [dict(column=f'c_cpl[{COMPONENTS[c]}]', original_zero=0, test_zero=0,
                  nonzero_to_zero=0, nonzero_sign_flip=0) for c in range(6, 15)]
    mismatch = reversed_test = changed_orientation = 0
    for key, values, reverse in rows(test, provenance['test']):
        require(key in index, f'extra test pair {key}; diagnostic incomplete')
        row_index = index[key]
        require(not seen[row_index], f'test duplicate pair {key}; diagnostic refuses duplicate changes')
        seen[row_index] = 1
        reversed_test += reverse
        changed_orientation += reverse != bool(reversed_original[row_index])
        failed = []
        for c, b in enumerate(values):
            a = data[row_index * 20 + c]
            delta = abs(a - b)
            if c in PERIODIC:
                delta = min(delta, BOX - delta)
            threshold = REL * max(abs(a), medians[c])
            require(math.isfinite(delta) and math.isfinite(threshold), 'comparison arithmetic overflow')
            counts[c]['max_abs_delta'] = max(counts[c]['max_abs_delta'], delta)
            if delta > threshold:
                failed.append(c)
                counts[c]['any_fail'] += 1
                counts[c]['zero_threshold_fail'] += threshold == 0
                if len(counts[c]['examples']) < 3:
                    counts[c]['examples'].append(dict(pair=list(key), original=a, test=b, abs_delta=delta, threshold=threshold))
            if 6 <= c < 15:
                f = force[c - 6]
                f['original_zero'] += a == 0
                f['test_zero'] += b == 0
                f['nonzero_to_zero'] += a != 0 and b == 0
                f['nonzero_sign_flip'] += a != 0 and b != 0 and (a > 0) != (b > 0)
        if failed:
            mismatch += 1
            counts[failed[0]]['first_fail'] += 1
            families[FAMILIES[failed[0]]]['first_fail'] += 1
            for family in {FAMILIES[c] for c in failed}:
                families[family]['any_fail'] += 1
    require(all(seen), f'missing test pairs: {n - sum(seen)}; diagnostic incomplete')
    for path, meta in [(original, provenance['original']), (test, provenance['test'])]:
        require(signature(os.stat(path)) == tuple(meta['stat_signature']), 'input changed during complete analysis')
    return dict(diagnostic_status='COMPLETE_NUMERIC_BREAKDOWN_NOT_A_VERDICT', provenance=provenance,
                n_orig=n, n_test=sum(seen), reproduced_pair_mismatches=mismatch,
                mismatch_fraction=mismatch/n, original_abs_medians=medians, components=counts, families=families,
                orientation=dict(original_reversed=sum(reversed_original), test_reversed=reversed_test,
                                 pair_orientation_changed=changed_orientation), force_zero_sign=force,
                discriminating_frac=discriminating/n, duplicate_policy='Refuse all duplicates; recorded run had none',
                tolerance=dict(relative=REL, box=[BOX, BOX], comparison='strict delta > rel*max(abs(original), full_original_abs_median); no floor'),
                limitations='No threshold changes, new acceptance verdict or cause inference. Stat stability is not atomic snapshot proof.')


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def unique_json(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON field: ' + key)
        result[key] = value
    return result


def bind_job(job=JOB, kit=KIT):
    expected_modules = {
        'SHA256SUMS': SEAL_SHA,
        'ul_gates.py': 'c8d45a9cf75f0806e612d810942d23adea4b40feaa5f31f7d279eb8386358de6',
        'ul_lib.py': '23a79392352e01631c6d1f6aaecdb31fc8a53be518ee6f27b815896e161727e6',
        'ul_reader.py': 'dfc06b8dbf53a8cab05df297890e1f8ca1d0fa038536c7c13ed8b8677e521723',
    }
    actual_modules = {name: sha_file(kit/name) for name in expected_modules}
    require(actual_modules == expected_modules, 'job kit seal/source identity differs from accepted 4c')
    manifest_path, verdict_path = job/'run_manifest.txt', job/'restore_verdict.json'
    manifest_raw, verdict_raw = manifest_path.read_bytes(), verdict_path.read_bytes()
    manifest, stages = {}, []
    for line in manifest_raw.decode('utf-8').splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition('=')
        require(bool(separator), 'unexpected manifest line')
        if key == 'stage':
            stages.append(value)
        else:
            require(key not in manifest, 'duplicate manifest field: ' + key)
            manifest[key] = value
    expected = {
        'kit': str(KIT), 'repo_head': PIN, 'repo_dirty_here': '0', 'sums_sha256': SEAL_SHA,
        'lmp_sha256': 'ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f',
        'np': '6', 'bed': 'ps_7_3_r45', 'job': 'RJ', 'resume': '0',
        'slurm_job': '323957 slurm_ntasks=6 slurm_nodes=node04',
        'allow_other_lmp': '0', 'gate': 'ALLOW', 'grammar_prereq': 'PASS',
        'reader_restore_rc': '2', 'reader_kebase_rc': '0',
        'end': '2026-10-26T22:51:37+09:00 fails=0 reader_rc=2',
    }
    require(all(manifest.get(k) == v for k, v in expected.items()), 'manifest is not the recorded job323957 outcome')
    require(stages == ['G0 rc=0', 'Ut0 screen=screen.txt rc=0 check=PASS',
                       'R screen=screen.txt rc=0 check=PASS', 'UNread screen=screen.txt rc=0 check=PASS',
                       'UK screen=screen.txt rc=0 check=PASS'], 'unexpected stage outcomes/order')
    verdict = json.loads(verdict_raw, object_pairs_hook=unique_json)
    require(verdict.get('bed') == 'ps_7_3_r45' and verdict.get('job') == 'RJ' and
            verdict.get('s0') == 3200000 and verdict.get('status') == 'VALUE_MISMATCH', 'unexpected restore verdict')
    gate = verdict['checks']['G2c']
    expected_gate = dict(status='FAIL', n_orig=562605, n_test=562605, n_mismatch=545583,
                         missing=[], extra=[], n_dup_consistent=0, dup_conflicts=[], why=[], discriminating_frac=1.0)
    require(all(gate.get(k) == v for k, v in expected_gate.items()), 'G2c verdict differs from recorded outcome')
    return dict(job_id='323957', accepted_pin=PIN, module_sha256=actual_modules,
                manifest_sha256=hashlib.sha256(manifest_raw).hexdigest(),
                verdict_sha256=hashlib.sha256(verdict_raw).hexdigest(),
                recorded_gate=expected_gate, restore_status='VALUE_MISMATCH')


def self_sha256():
    injected = globals().get('__diagnostic_sha256__')
    return injected if injected else sha_file(Path(__file__))


def main():
    binding = bind_job()
    result = analyze(ORIGINAL, TEST, ORIGINAL_SHA)
    after = bind_job()
    require(after == binding, 'binding evidence changed during diagnostic')
    common = dict(job_binding=binding, diagnostic_sha256=self_sha256(),
                  limits=dict(max_rows=MAX_ROWS, max_line_bytes=MAX_LINE_BYTES, max_file_bytes=MAX_FILE_BYTES),
                  operational_scope='Existing two contact files only; no rerun/retry, code or tolerance changes, or follow-on arms')
    matches = (result['n_orig'] == result['n_test'] == 562605 and
               result['reproduced_pair_mismatches'] == 545583 and result['discriminating_frac'] == 1.0)
    if not matches:
        return dict(common, diagnostic_status='PARITY_DISCREPANCY_NOT_A_VERDICT', recorded_gate_match=False,
                    provenance=result['provenance'], observed_aggregates={k:result[k] for k in
                    ('n_orig','n_test','reproduced_pair_mismatches','discriminating_frac')})
    return dict(result, **common, recorded_gate_match=True)


def cli():
    try:
        result = main()
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result['diagnostic_status'] == 'COMPLETE_NUMERIC_BREAKDOWN_NOT_A_VERDICT' else 2
    except Exception as error:
        print(json.dumps({'diagnostic_status': 'INCOMPLETE_NO_VERDICT', 'error': str(error),
                          'type': type(error).__name__, 'diagnostic_sha256': self_sha256()}, indent=2))
        return 2


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(cli())
