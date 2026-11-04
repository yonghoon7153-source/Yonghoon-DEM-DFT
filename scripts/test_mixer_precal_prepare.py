#!/usr/bin/env python3
"""Synthetic preparation checks only: no simulator, jobs, remote hosts or run data."""
import builtins
import copy
import hashlib
import io
import json
import re
import unittest
from contextlib import redirect_stdout
from unittest import mock

import make_mixer_deck as gen
import mixer_deck_diff as diff
import mixer_deck_readback as rb
import mixer_precal_prepare as prep


IDS = tuple('PRECAL_R1_B%d_%s' % (b, role) for b in (1, 2, 3) for role in ('U', 'C')) + ('PRECAL_N0', 'PRECAL_E0')


def rebound(meta, raw):
    result = copy.deepcopy(meta)
    result.update(deck_sha256=hashlib.sha256(raw).hexdigest(), deck_bytes=len(raw))
    return result


class Preparation(unittest.TestCase):
    def test_01_first8_physical_bindings(self):
        self.assertEqual(prep.CASE_IDS, IDS)
        for case_id in IDS:
            with self.subTest(case_id=case_id):
                item = prep.prepare_case(case_id)
                self.assertEqual(set(item), {'case_id', 'role', 'deck', 'meta'})
                self.assertIs(type(item['deck']), bytes)
                binding = prep.validate_case(case_id, item['deck'], item['meta'])
                self.assertEqual(binding['case_id'], case_id)
                self.assertEqual(binding['role'], item['role'])
                self.assertEqual(binding['seed'], 32452843)
                self.assertEqual(binding['np_proposed'], 20)
                self.assertEqual(binding['revolutions'], 0 if case_id == 'PRECAL_E0' else 2)
                self.assertEqual(binding['density_generation'], 'lab20261014')
                self.assertEqual(set(binding['phases']), {'AM_P', 'AM_S', 'SE'})
                self.assertEqual(sum(binding['expected_counts'].values()), binding['n_planned'])
                parsed = rb.read_deck(item['deck'].decode('utf-8'))
                for phase, desc in binding['phases'].items():
                    self.assertEqual(desc['radius_m'], parsed['templates'][desc['type']]['radius'])
                drum = [t for _, t in parsed['cmds'] if t[:2] == ['fix', 'Drum']][0]
                self.assertEqual(binding['r_container'], .5 * float(drum[drum.index('scale') + 1]))
                self.assertEqual(binding['geometry']['length'], .2 * float(drum[drum.index('scale') + 1]))
                self.assertEqual(binding['frame_pm']['phases'], binding['phases'])
                self.assertEqual(binding['frame_pm']['meta_steps'], {k: item['meta']['steps'][k] for k in ('t0_planned', 'dump_every')})
                self.assertIsNone(binding['frame_pm']['n_expected_file'])
                self.assertIsNone(item['meta']['registered'])

    def test_02_standard_d2_three_pairs(self):
        for b in (1, 2, 3):
            a = prep.prepare_case('PRECAL_R1_B%d_U' % b)
            c = prep.prepare_case('PRECAL_R1_B%d_C' % b)
            r = diff.diff_d2_decks(a['deck'], c['deck'], a['meta'], c['meta'])
            self.assertEqual(r['verdict'], 'PASS', r['failures'])
            self.assertFalse(r['execution_authorized'])

    def test_03_zero_controls_separate_contract(self):
        for case_id in IDS[-2:]:
            p = prep.prepare_case(case_id)
            self.assertEqual(p['meta']['schema'], 'mixer_precal_baseline_meta/1')
            self.assertEqual(p['meta']['control_role'], p['role'])
            self.assertNotIn('adhesion_rule', p['meta'])
            d = rb.read_deck(p['deck'].decode())
            self.assertTrue(all(x == 0 for x in d['ced'].values()))
            self.assertEqual(rb.read_d2(p['deck'], p['meta'])['verdict'], 'FAIL')
            with self.assertRaises(SystemExit):
                gen.gm_arm({'AM_P': .1, 'AM_S': .1, 'SE': 1.}, gamma_wall=gen.gm_wall_from_ncm(.1), bo_se=0.)

    def test_04_remaining12_and_untrusted_ids(self):
        rejected = ['PRECAL_R%d_B%d_%s' % (r, b, s) for r in (2, 3) for b in (1, 2, 3) for s in ('U', 'C')]
        rejected += ['', None, True, [], {}, 'PRECAL_E0 ', '../PRECAL_E0', 'PRECAL_R1_B４_U']
        for value in rejected:
            with self.subTest(value=value), self.assertRaises(ValueError):
                prep.prepare_case(value)
            with self.assertRaises(ValueError):
                prep.validate_case(value, b'', {})

    def test_05_cross_case_and_baseline_swap(self):
        for source, target in [(IDS[0], IDS[1]), (IDS[0], IDS[2]), ('PRECAL_N0', 'PRECAL_E0'), ('PRECAL_E0', IDS[0])]:
            p = prep.prepare_case(source)
            with self.assertRaises(ValueError):
                prep.validate_case(target, p['deck'], p['meta'])

    def test_06_metadata_mutations(self):
        for cid in (IDS[0], 'PRECAL_N0', 'PRECAL_E0'):
            p = prep.prepare_case(cid)
            mutations = [lambda m: m.update(seed=15485863), lambda m: m.update(arm='LC'),
                         lambda m: m.update(registered='legacy registration'), lambda m: m.update(revolutions=True),
                         lambda m: m.update(n_atoms_planned=99999), lambda m: m.update(np_proposed=20),
                         lambda m: m.update(dens_gen='gen1'), lambda m: m.update(dump_modify_format='%g'),
                         lambda m: m.update(cgf=float('nan')), lambda m: m.update(cgf=float('inf')),
                         lambda m: m.update(argv=()), lambda m: m['steps'].update(fill=0),
                         lambda m: m.update(stiffen_se=1), lambda m: m['radius_m'].update(SE=1e-5)]
            if cid == IDS[0]:
                mutations += [lambda m: m['adhesion_rule'].update(bo_se=0),
                              lambda m: m['adhesion_rule'].update(bo_se=21.244),
                              lambda m: m['adhesion_rule'].update(gamma_wall=.0256),
                              lambda m: m['adhesion_rule']['gamma'].update(AM_P=1.)]
            else:
                mutations += [lambda m: m.update(control_role='U'), lambda m: m.update(schema='mixer_deck_meta/1')]
            for i, mutation in enumerate(mutations):
                with self.subTest(cid=cid, mutation=i):
                    m = copy.deepcopy(p['meta']); mutation(m)
                    with self.assertRaises(ValueError):
                        prep.validate_case(cid, p['deck'], m)

    def test_07_rehashed_deck_mutations(self):
        for cid in (IDS[0], 'PRECAL_N0', 'PRECAL_E0'):
            p = prep.prepare_case(cid)
            changes = [lambda d: d.replace(b'%.17g', b'%.16g'),
                       lambda d: d.replace(b'boundary        f f f', b'boundary        p p p'),
                       lambda d: d.replace(b'9.81 vector', b'9.82 vector'),
                       lambda d: d.replace(b'32452843', b'15485863'),
                       lambda d: d + b'run 1\n', lambda d: d.replace(b'\n', b'\r\n'),
                       lambda d: d + b'# changed provenance\n', lambda d: d + b'\xff']
            for i, change in enumerate(changes):
                raw = change(p['deck'])
                self.assertNotEqual(raw, p['deck'], (cid, i))
                with self.subTest(cid=cid, mutation=i), self.assertRaises(ValueError):
                    prep.validate_case(cid, raw, rebound(p['meta'], raw))

    def test_08_bad_physical_bytes_and_types(self):
        p = prep.prepare_case(IDS[0])
        for raw in (p['deck'].decode(), bytearray(p['deck']), None, b''):
            with self.assertRaises(ValueError):
                prep.validate_case(IDS[0], raw, p['meta'])
        with self.assertRaises(ValueError):
            prep.validate_case(IDS[0], p['deck'] + b'\n', p['meta'])
        for meta in (None, [], 'not metadata'):
            with self.assertRaises(ValueError):
                prep.validate_case(IDS[0], p['deck'], meta)

    def test_09_generator_state_restored_success_and_failure(self):
        old_types = gen.TYPES
        old_arms = copy.deepcopy(gen.ARMS)
        try:
            gen.set_phases(('AM_P', 'SE'))
            before_types = gen.TYPES
            prep.prepare_case(IDS[0])
            self.assertEqual(gen.TYPES, before_types)
            self.assertEqual(gen.ARMS, old_arms)
            with mock.patch.object(gen, 'deck', side_effect=SystemExit('synthetic refusal')):
                with self.assertRaises(ValueError):
                    prep.prepare_case(IDS[0])
            self.assertEqual(gen.TYPES, before_types)
            self.assertEqual(gen.ARMS, old_arms)
        finally:
            gen.set_phases(old_types)

    def test_10_no_file_writes_or_stdout(self):
        original_open = builtins.open
        def read_only(path, mode='r', *args, **kwargs):
            if any(x in mode for x in 'wax+'):
                self.fail('API attempted a file write')
            return original_open(path, mode, *args, **kwargs)
        output = io.StringIO()
        with mock.patch('builtins.open', side_effect=read_only), mock.patch('os.mkdir', side_effect=AssertionError('mkdir')), \
                mock.patch('os.makedirs', side_effect=AssertionError('makedirs')), redirect_stdout(output):
            p = prep.prepare_case('PRECAL_E0')
            prep.validate_case('PRECAL_E0', p['deck'], p['meta'])
        self.assertEqual(output.getvalue(), '')

    def test_11_return_objects_not_shared(self):
        p = prep.prepare_case(IDS[0]); pristine = copy.deepcopy(p)
        b = prep.validate_case(IDS[0], p['deck'], p['meta'])
        b['frame_pm']['phases']['SE']['radius_m'] = 9
        self.assertEqual(p, pristine)
        p['meta']['seed'] = 0
        self.assertEqual(prep.prepare_case(IDS[0]), pristine)

    def test_12_cli_report_only(self):
        output = io.StringIO()
        with redirect_stdout(output):
            rc = prep.main([])
        result = json.loads(output.getvalue())
        self.assertEqual(rc, 0)
        self.assertEqual([p['case_id'] for p in result['cases']], list(IDS))
        self.assertTrue(all(p['status'] == 'STATIC_VALID' for p in result['cases']))
        self.assertTrue(all(p['verdict'] == 'PASS' for p in result['pairs']))
        self.assertFalse(result['execution_authorized'])
        self.assertIsNone(result['registered'])
        self.assertEqual(result['research_results'], 0)

    def test_13_zero_guard_beyond_source_output_oracle(self):
        for cid in IDS[-2:]:
            p = prep.prepare_case(cid)
            raw, replacements = re.subn(
                rb'(fix mC all property/global cohesionEnergyDensity peratomtypepair 4 &\n)(\s*)0',
                rb'\g<1>\g<2>1', p['deck'], count=1)
            self.assertEqual(replacements, 1)
            bad = dict(p, deck=raw, meta=rebound(p['meta'], raw))
            # Even a common defect in the source-output oracle cannot turn a
            # nonzero control into a zero-CED certificate.
            with mock.patch.object(prep, '_generate', return_value=bad):
                with self.assertRaisesRegex(ValueError, 'zero CED'):
                    prep.validate_case(cid, bad['deck'], bad['meta'])

    def test_14_d2_readback_beyond_source_output_oracle(self):
        p = prep.prepare_case(IDS[0])
        raw = p['deck'].replace(b'9.81 vector', b'9.82 vector')
        self.assertNotEqual(raw, p['deck'])
        bad = dict(p, deck=raw, meta=rebound(p['meta'], raw))
        with mock.patch.object(prep, '_generate', return_value=bad):
            with self.assertRaisesRegex(ValueError, 'D2 readback refused:.*gravity'):
                prep.validate_case(IDS[0], bad['deck'], bad['meta'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
