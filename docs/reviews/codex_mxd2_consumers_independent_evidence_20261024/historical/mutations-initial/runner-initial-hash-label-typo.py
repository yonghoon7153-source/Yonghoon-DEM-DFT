#!/usr/bin/env python3
"""Isolated in-memory validator mutations; frozen source bytes remain unchanged."""
import argparse
import copy
import hashlib
import io
import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(repo / 'scripts'))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import mixer_deck_readback as rb
    import mixer_deck_diff as dd
    import test_mixer_d2_consumers as tests
    import attack_consumers as helper
    files = ['make_mixer_deck.py', 'mixer_deck_readback.py', 'mixer_deck_diff.py', 'mixer_smoke_blind.py', 'test_mixer_d2_consumers.py']
    hashes = lambda: {name: hashlib.sha256((repo / 'scripts' / name).read_bytes()).hexdigest() for name in files}
    before = hashes()
    original = {key: getattr(rb, key) for key in ('_d2_need', '_d2_close', '_d2_float_token', '_d2_counts')}

    def restore():
        for key, value in original.items():
            setattr(rb, key, value)

    def skip_need(text):
        rb._d2_need = lambda condition, message: None if message == text else original['_d2_need'](condition, message)

    def skip_close(text):
        rb._d2_close = lambda value, expected, tol, name: None if name == text else original['_d2_close'](value, expected, tol, name)

    # Independent fixture file was generated before these mutations; the author fixture
    # is used only by its own regression suite, not by the discriminating probes below.
    text = (Path(__file__).resolve().parent / 'canonical/in.mixer').read_text()
    meta = json.loads((Path(__file__).resolve().parent / 'canonical/deck_meta.json').read_text())

    def hash_probe():
        changed = copy.deepcopy(meta)
        changed['deck_sha256'] = '0' * 64
        return rb.read_d2(text, changed)

    def bo_probe():
        changed = copy.deepcopy(meta)
        changed['adhesion_rule']['bo_se'] *= 2
        return rb.read_d2(text, changed)

    def gravity_probe():
        changed = text.replace('vector 0.0 0.0 -1.0', 'vector 0.0 0.0 1.0')
        assert changed != text
        return rb.read_d2(changed, helper.rebound(changed, meta))

    def numeric_probe():
        changed = text.replace('gravity 9.81', 'gravity ９.81')
        assert changed != text
        return rb.read_d2(changed, helper.rebound(changed, meta))

    def pair_probe():
        # Matching coated fixture from the independently generated lifecycle fixtures.
        folder = Path(__file__).resolve().parent / 'command-order-v1-repro/positive'
        a = (folder / 'reference.in').read_text()
        am = json.loads((folder / 'reference_meta.json').read_text())
        b = (folder / 'new.in').read_text()
        bm = json.loads((folder / 'new_meta.json').read_text())
        rows = helper.logical(b)
        region = next(row for row in rows if row[:3] == ['region', 'reg', 'block'])
        region[3] = str(float(region[3]) * 1.1)
        changed = helper.render(rows)
        return dd.diff_d2_decks(a, changed, am, helper.rebound(changed, bm))

    def count_probe():
        result = rb.read_d2(text, meta)
        return {'verdict': 'PASS' if result.get('expected_counts') == {'1': 176, '2': 859, '3': 98965} else 'FAIL',
                'counts': result.get('expected_counts')}

    mutants = [
        ('hash_binding_removed', lambda: skip_need('actual deck sha256 != metadata'), hash_probe),
        ('absolute_Bo_removed', lambda: skip_close('absolute printed SE Bo'), bo_probe),
        ('gravity_vector_removed', lambda: skip_need('actual gravity != declared mixer gravity'), gravity_probe),
        ('nonCED_pair_equality_removed', lambda: skip_need('non-CED command tokens differ (geometry/seed/gravity/material/time/etc.)'), pair_probe),
        ('ASCII_float_lexeme_removed', lambda: setattr(rb, '_d2_float_token', lambda value, name: float(value)), numeric_probe),
        ('actual_counts_replaced_by_gen1_default', lambda: setattr(rb, '_d2_counts', lambda *args: {'1': 176, '2': 859, '3': 98965}), count_probe),
    ]
    results = []
    for name, install, probe in [('baseline', lambda: None, lambda: rb.read_d2(text, meta)), *mutants]:
        restore()
        probe_before = probe()
        install()
        probe_after = probe()
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
        (out / (name + '.log')).write_text(stream.getvalue())
        row = {'name': name, 'probe_before': probe_before, 'probe_after': probe_after,
               'tests_run': result.testsRun, 'failures': [test.id() for test, _ in result.failures],
               'errors': [test.id() for test, _ in result.errors], 'regression_suite_passed': result.wasSuccessful()}
        row['mutation_effective'] = name == 'baseline' or (probe_before.get('verdict') == 'FAIL' and probe_after.get('verdict') == 'PASS')
        row['killed_by_tests'] = name == 'baseline' or (bool(result.failures) and not result.errors)
        results.append(row)
        print(json.dumps({key: row[key] for key in ('name', 'tests_run', 'mutation_effective', 'killed_by_tests', 'failures', 'errors')}), flush=True)
    restore()
    after = hashes()
    ok = results[0]['regression_suite_passed'] and before == after and all(row['mutation_effective'] and row['killed_by_tests'] for row in results)
    summary = {'source_hashes_before': before, 'source_hashes_after': after, 'source_unchanged': before == after,
               'results': results, 'all_expectations_met': ok,
               'scope': 'in-process guards mutated in memory only; child CLI tests still see original source'}
    (out / 'results.json').write_text(json.dumps(summary, indent=2) + '\n')
    return int(not ok)


if __name__ == '__main__':
    raise SystemExit(main())
