#!/usr/bin/env python3
"""Independent finite-grid attack probes; all observations are synthetic."""
import argparse
import copy
from decimal import Decimal
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def load(path):
    spec = importlib.util.spec_from_file_location('independent_subject', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(value):
    return hashlib.sha256(value).hexdigest()


def fixture():
    # Independent three-point fixture, not imported from the author's tests.
    blobs = {'condition.json': b'{"synthetic":true,"wall":"fixed"}\n',
             'raw.json': b'{"synthetic":true,"data":"declared separately"}\n'}
    width = {'unit': 'U', 'boundary': 'inclusive', 'widths': {x: .1 for x in ['a', 'b', 'c']}}
    contract = {'schema': 'mixer_d3_decision_contract/1', 'analysis_id': 'independent-flat',
                'condition_sha256': sha(blobs['condition.json']),
                'grid': [{'id': x, 'bo': b} for x, b in zip(['a', 'b', 'c'], [1, 2, 3])],
                'calibration': {'T1': copy.deepcopy(width), 'T2': copy.deepcopy(width)},
                'validation': {'flow': dict(copy.deepcopy(width), kind='scalar')},
                'seed_policy': {'allowed_role_overlap': []}}
    def point(value):
        return {'state': 'eligible', 'value': value, 'unit': 'U', 'source_ids': ['raw'],
                'flags': ['INSENSITIVE'],
                'uncertainty': {'value': .01, 'unit': 'U', 'n': 3, 'df': 2, 'method': 'synthetic supplied'}}
    obs = {'schema': 'mixer_d3_observations/1', 'contract_sha256': 'a' * 64,
           'condition_artifact': 'condition',
           'artifacts': [{'id': 'condition' if name.startswith('condition') else 'raw',
                          'path': name, 'sha256': sha(data)} for name, data in blobs.items()],
           'calibration': {t: {'experiment': point(v), 'predictions': {b: point(v) for b in ['a', 'b', 'c']}}
                           for t, v in [('T1', 3), ('T2', 5)]},
           'validation': {'flow': {'experiment': point(7), 'predictions': {b: point(7) for b in ['a', 'b', 'c']}}},
           'seed_manifest': {'C0': [101], 'C1': [103], 'C2': [107]}}
    return contract, obs, blobs


def run(module):
    evidence = {'scope': 'synthetic arithmetic and malformed-input probes only', 'checks': []}
    def check(name, truth, detail=None):
        evidence['checks'].append({'name': name, 'pass': bool(truth), 'detail': detail})
        if not truth:
            raise AssertionError(name)
    def calc(c=None, o=None, a=None):
        fc, fo, fa = fixture()
        return module.evaluate(c if c is not None else fc, o if o is not None else fo,
                               contract_sha256='a' * 64, artifact_loader=(a if a is not None else fa).__getitem__)
    r = calc()
    check('flat_INSENSITIVE_retained', r['S'] == ['a', 'b', 'c'] and 'no-identifiability-claim' in r['limitations'])
    c, o, _ = fixture()
    del o['calibration']['T1']['predictions']['b']['uncertainty']
    r = calc(c, o)
    check('missing_uncertainty_UNASSESSED', r['calibration']['T1'][1]['status'] == 'UNASSESSED' and r['S'] == ['a', 'c'])
    check('unknown_gap_not_bridged', r['neighbor_groups'] == [['a'], ['c']])
    # Independent ternary truth table for all six calibration predictions.
    combinations = 0
    for states in itertools.product('CIU', repeat=6):
        c, o, _ = fixture()
        expect = {'T1': set(), 'T2': set()}
        for (test, b), state in zip(itertools.product(['T1', 'T2'], ['a', 'b', 'c']), states):
            if state == 'C': expect[test].add(b)
            elif state == 'I': o['calibration'][test]['predictions'][b]['value'] = 99
            else: del o['calibration'][test]['predictions'][b]
        r = calc(c, o)
        assert r['S'] == sorted(expect['T1'] & expect['T2']), states
        assert r['calibration_complete'] == ('U' not in states), states
        combinations += 1
    check('intersection_729_truth_rows', combinations == 729)
    c, o, _ = fixture()
    c['validation']['stop'] = {'kind': 'categorical', 'unit': 'state', 'rule': 'exact-match', 'labels': ['flow', 'stopped']}
    o['validation']['flow']['predictions']['a']['value'] = 99
    r = calc(c, o)
    check('validation_incomplete_precedence', r['S'] == ['a', 'b', 'c'] and r['validation']['aggregate'] == 'incomplete'
          and r['validation']['candidates'][0]['status'] == 'unassessed'
          and r['validation']['candidates'][0]['items']['flow']['status'] == 'incompatible')
    c, o, _ = fixture()
    o['calibration']['T1']['experiment']['value'] = Decimal('0.4')
    o['calibration']['T1']['predictions']['a']['value'] = Decimal('0.3')
    r = calc(c, o)
    check('exact_inclusive_boundary', r['calibration']['T1'][0]['status'] == 'COMPATIBLE')
    o['calibration']['T1']['predictions']['a']['value'] = Decimal('0.2999999999999999999999999999999999999999999999999999999999999999')
    r = calc(c, o)
    check('just_outside_64_digit_boundary', r['calibration']['T1'][0]['status'] == 'INCOMPATIBLE')
    for val in [Decimal('1e300'), Decimal('-1e300'), Decimal('1e-300')]:
        c, o, _ = fixture()
        o['calibration']['T1']['experiment']['value'] = -val
        o['calibration']['T1']['predictions']['a']['value'] = val
        c['calibration']['T1']['widths']['a'] = abs(val)
        check('large_exact_difference_' + str(val), calc(c, o)['calibration']['T1'][0]['status'] == 'INCOMPATIBLE')
    rejects = 0
    for val in [True, False, '1', '١', Decimal('NaN'), Decimal('Infinity'), Decimal('1e301')]:
        c, o, _ = fixture()
        o['calibration']['T1']['experiment']['value'] = val
        try: calc(c, o)
        except module.ContractError: rejects += 1
    check('invalid_numeric_rejected', rejects == 7)
    seed_rejects = 0
    for seed, role in itertools.product([15485863, 86028121, 104395301], ['C0', 'C1', 'C2']):
        c, o, _ = fixture(); o['seed_manifest'][role] = [seed]
        try: calc(c, o)
        except module.ContractError: seed_rejects += 1
    check('reserved_seeds_nine_cases', seed_rejects == 9)
    c, o, _ = fixture(); o['seed_manifest']['C2'] = [101]
    try: calc(c, o); overlap_rejected = False
    except module.ContractError: overlap_rejected = True
    check('undeclared_seed_overlap', overlap_rejected)
    c['seed_policy']['allowed_role_overlap'] = [['C2', 'C0']]
    check('explicit_seed_pairing_not_independence', not calc(c, o)['seed_check']['independent_samples_certified'])
    c, o, blobs = fixture(); blobs['raw.json'] += b'tampered'
    try: calc(c, o, blobs); changed_rejected = False
    except module.ContractError: changed_rejected = True
    check('changed_raw_bytes_rejected', changed_rejected)
    # Fact about scope: matching raw-byte hashes do not verify extraction of values.
    c, o, _ = fixture(); before = calc(c, o)
    for row in o['calibration']['T1']['predictions'].values(): row['value'] = 999
    after = calc(c, o)
    evidence['source_value_binding_limit'] = {'same_verified_raw_hashes': before['verified_artifact_sha256'] == after['verified_artifact_sha256'],
                                            'S_before': before['S'], 'S_after': after['S'],
                                            'meaning': 'supplied summary numbers are not re-extracted from source bytes'}
    evidence['bo_po_present'] = all('bo_po' in point for point in after['grid'])
    return evidence


def cli_probe(module_path, out):
    result = {}
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp); c, o, blobs = fixture()
        for name, data in blobs.items(): (root / name).write_bytes(data)
        contract = root / 'contract.json'; obs = root / 'observations.json'; dest = root / 'result.json'
        for label, literal in [('control', None), ('huge_positive_exponent', '1e9999999999999999999999'),
                               ('huge_negative_exponent', '1e-9999999999999999999999'), ('duplicate', '1,"bo":2')]:
            text = json.dumps(c)
            if literal is not None: text = text.replace('"bo": 1', '"bo": ' + literal, 1)
            contract.write_text(text); o['contract_sha256'] = sha(contract.read_bytes()); obs.write_text(json.dumps(o))
            if dest.exists(): dest.unlink()
            cp = subprocess.run([sys.executable, '-I', '-B', str(module_path), '--contract', str(contract), '--observations', str(obs), '--out', str(dest)], capture_output=True, text=True)
            result[label] = {'rc': cp.returncode, 'output_exists': dest.exists(), 'stdout': cp.stdout, 'stderr': cp.stderr}
        (out / 'cli-probes.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--module', type=Path, required=True); parser.add_argument('--out', type=Path, required=True); args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    evidence = run(load(args.module)); evidence['reader_sha256'] = sha(args.module.read_bytes())
    (args.out / 'results.json').write_text(json.dumps(evidence, indent=2) + '\n')
    cli_probe(args.module, args.out)
    print(json.dumps({'checks': len(evidence['checks']), 'passed': sum(row['pass'] for row in evidence['checks'])}))
