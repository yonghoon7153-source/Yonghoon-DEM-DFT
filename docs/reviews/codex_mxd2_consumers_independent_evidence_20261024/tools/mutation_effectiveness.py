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
    original = {key: getattr(rb, key) for key in ('_d2_need', '_d2_close', '_d2_float_token', '_d2_counts', '_d2_lifecycle')}

    def restore():
        for key, value in original.items():
            setattr(rb, key, value)

    def skip_need(text):
        rb._d2_need = lambda condition, message: None if message == text else original['_d2_need'](condition, message)

    def skip_close(text):
        rb._d2_close = lambda value, expected, tol, name: None if name == text else original['_d2_close'](value, expected, tol, name)

    # This independent fixture uses parameters distinct from the author's fixtures.
    # No author's fixture helper is used by the discriminating probes.
    def fixture(coated=False, density_scale=1.):
        import make_mixer_deck as gen
        density = gen.DENS_GENERATIONS['lab20261014']
        old_phases = gen.TYPES
        try:
            gen.set_phases(('AM_P', 'AM_S', 'SE'))
            gen.DENS_GENERATIONS['lab20261014'] = {key: value * density_scale for key, value in density.items()}
            gen.register_arm('INDEPENDENT_MUTATION', gen.gm_arm(
                {'AM_P': 1. if coated else .25, 'AM_S': 1. if coated else .25, 'SE': 1.},
                gamma_wall=.0064, bo_se=1.125, layered=True, rho_uncoated_ncm=.25))
            plan = gen.plan(100003, cgf=125., stiffen_se=20., dens_gen='lab20261014')
            rpm = gen.resolve_rpm(plan['R'])
            generated = gen.deck(plan, rpm, 2, seed=49979687, arm='INDEPENDENT_MUTATION', hold_bo_pairwise=True)
            generated_meta = gen.deck_meta(plan, rpm, 2, 49979687, 'INDEPENDENT_MUTATION', generated, hold_bo_pairwise=True)
        finally:
            gen.DENS_GENERATIONS['lab20261014'] = density
            gen.ARMS.pop('INDEPENDENT_MUTATION', None)
            gen.set_phases(old_phases)
        generated_meta['dens_g_cm3'] = dict(density)
        return generated, generated_meta

    text, meta = fixture()

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

    def ceiling_probe():
        rows = helper.logical(text)
        matrix = next(row for row in rows if row[0] == 'fix' and row[4] == 'cohesionEnergyDensity')
        matrix[7:] = [format(float(token) * 100, '.12g') for token in matrix[7:]]
        changed = helper.render(rows)
        changed_meta = helper.rebound(changed, meta)
        changed_meta['adhesion_rule']['bo_se'] *= 100 ** 3
        return rb.read_d2(changed, changed_meta)

    def pair_probe():
        a, am = text, meta
        b, bm = fixture(coated=True)
        rows = helper.logical(b)
        region = next(row for row in rows if row[:3] == ['region', 'reg', 'block'])
        region[3] = str(float(region[3]) * 1.1)
        changed = helper.render(rows)
        return dd.diff_d2_decks(a, changed, am, helper.rebound(changed, bm))

    def count_probe():
        result = rb.read_d2(text, meta)
        return {'verdict': 'PASS' if result.get('expected_counts') == {'1': 176, '2': 859, '3': 98965} else 'FAIL',
                'counts': result.get('expected_counts')}

    def lifecycle_probe():
        rows = helper.logical(text)
        rows.remove(['unfix', 'insA'])
        index = next(i for i, row in enumerate(rows) if row[0] == 'run')
        rows.insert(index, ['unfix', 'insA'])
        changed = helper.render(rows)
        return rb.read_d2(changed, helper.rebound(changed, meta))

    def density_probe():
        generated, generated_meta = fixture(density_scale=1.2)
        return rb.read_d2(generated, generated_meta)

    def skip_density():
        rb._d2_close = lambda value, expected, tol, name: None if name.startswith('actual density ') else original['_d2_close'](value, expected, tol, name)

    mutants = [
        ('hash_binding_removed', lambda: skip_need('metadata SHA256 != actual deck'), hash_probe),
        ('absolute_Bo_removed', lambda: skip_close('absolute printed SE Bo'), bo_probe),
        ('gravity_vector_removed', lambda: skip_need('actual gravity != declared mixer gravity'), gravity_probe),
        ('nonCED_pair_equality_removed', lambda: skip_need('non-CED command tokens differ (geometry/seed/gravity/material/time/etc.)'), pair_probe),
        ('ASCII_float_lexeme_removed', lambda: setattr(rb, '_d2_float_token', lambda value, name: float(value)), numeric_probe),
        ('overlap_ceiling_removed', lambda: skip_need('static pair overlap exceeds 1%'), ceiling_probe),
        ('actual_counts_replaced_by_gen1_default', lambda: setattr(rb, '_d2_counts', lambda *args: {'1': 176, '2': 859, '3': 98965}), count_probe),
        ('actual_density_binding_removed', skip_density, density_probe),
        ('lifecycle_validation_removed', lambda: setattr(rb, '_d2_lifecycle', lambda commands: None), lifecycle_probe),
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
        print(json.dumps({**{key: row[key] for key in ('name', 'tests_run', 'mutation_effective', 'killed_by_tests')},
                          'failure_count': len(row['failures']), 'error_count': len(row['errors'])}), flush=True)
    restore()
    after = hashes()
    ok = results[0]['regression_suite_passed'] and before == after and all(row['mutation_effective'] and row['killed_by_tests'] for row in results)
    summary = {'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'source_hashes_before': before, 'source_hashes_after': after, 'source_unchanged': before == after,
               'results': results, 'all_expectations_met': ok,
               'scope': 'in-process guards mutated in memory only; child CLI tests still see original source'}
    (out / 'results.json').write_text(json.dumps(summary, indent=2) + '\n')
    return int(not ok)


if __name__ == '__main__':
    raise SystemExit(main())
