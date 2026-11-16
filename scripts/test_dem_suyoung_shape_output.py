"""Local synthetic output regressions; no field or material qualification."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import numpy as np


def load_source(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = load_source(os.environ.get('SUYOUNG_TEST_SOURCE',
                str(Path(__file__).with_name('dem_suyoung_sf2d_dev.py'))), 'sf_shape_test')


class ShapeOutput(unittest.TestCase):
    def observer(self, out, state=None, steps=7, every=3):
        self.assertTrue(hasattr(m, 'ShapeObserver'), 'shape observation is not implemented')
        return m.ShapeObserver(Path(out), 'S', m.initial_state(16) if state is None else state,
                               16, steps, .0005, .15, every)

    def run_with_shape(self, arm, out, steps):
        # The old implementation can still run; missing output is an assertion failure.
        extra = dict(shape_every=120) if hasattr(m, 'ShapeObserver') else {}
        return m.run_arm(arm, 16, steps, .0005, .15, .2, out, 600, **extra)

    def test_01_initial_state_is_copied_and_identities_are_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            state = m.initial_state(16)
            obs = self.observer(td, state)
            with np.load(Path(td)/'S_shape/frame_000000.npz', allow_pickle=False) as frame:
                np.testing.assert_array_equal(frame['X'], state['x'])
                np.testing.assert_array_equal(frame['point_id'], np.arange(len(state['x'])))
                np.testing.assert_array_equal(frame['particle_id'], state['ids'])
                np.testing.assert_array_equal(frame['F_total'], state['F'])
                self.assertEqual(frame['step'].item(), 0)
                self.assertEqual(frame['time_code'].item(), 0)
            before = obs.X.copy()
            state['x'][:] += .01
            np.testing.assert_array_equal(obs.X, before)
            self.assertFalse(np.shares_memory(obs.F_total, state['F']))

    def test_02_total_map_uses_increment_history_not_projected_elastic_F(self):
        with tempfile.TemporaryDirectory() as td:
            state = m.initial_state(16)
            obs = self.observer(td, state, steps=2, every=1)
            gradient = np.array([[200., 20.], [0., -100.]])
            state['C'][:] = gradient
            state['F'][:] = 3*np.eye(2)  # Deliberately unrelated elastic diagnostic.
            expected = (np.eye(2)+.0005*gradient) @ (np.eye(2)+.0005*gradient)
            for i in (1, 2):
                obs.after_step(state, i, dict(plate_pressure=1.))
            np.testing.assert_allclose(obs.F_total, np.tile(expected, (len(state['x']), 1, 1)), rtol=0, atol=0)
            self.assertFalse(np.array_equal(obs.F_total, state['F']))

    def test_03_poisoned_observer_does_not_feed_force_or_physical_state(self):
        with tempfile.TemporaryDirectory() as td:
            a, b = m.initial_state(16), m.initial_state(16)
            obs = self.observer(td, b, steps=8)
            obs.F_total[:] *= 7.0
            for i in range(1, 9):
                top = m.TOP0-.15*.0005*i
                da = m.step(a, 'F', 16, .0005, top, -.15, .2)
                db = m.step(b, 'F', 16, .0005, top, -.15, .2)
                obs.after_step(b, i, db)
                self.assertEqual(da, db)
                for k in a:
                    self.assertEqual(a[k].tobytes(), b[k].tobytes(), k)

    def test_04_frames_are_exact_observed_steps_not_interpolation(self):
        with tempfile.TemporaryDirectory() as td:
            state = m.initial_state(16)
            obs = self.observer(td, state)
            captured = {}
            for i in range(1, 8):
                diag = m.step(state, 'S', 16, .0005, m.TOP0-.15*.0005*i, -.15, .2)
                captured[i] = {k: state[k].copy() for k in ('x', 'v', 'ids', 'F')}
                obs.after_step(state, i, diag)
            obs.finish()
            manifest = json.loads((Path(td)/'S_shape/MANIFEST.json').read_bytes())
            self.assertEqual([r['step'] for r in manifest['frames']], [0, 1, 3, 6, 7])
            for row in manifest['frames'][1:]:
                i = row['step']
                with np.load(Path(td)/'S_shape'/row['npz']['path'], allow_pickle=False) as frame:
                    for key, src in [('x', 'x'), ('v', 'v'), ('particle_id', 'ids'), ('F_elastic', 'F')]:
                        self.assertEqual(frame[key].tobytes(), captured[i][src].tobytes(), key)
                    self.assertEqual(frame['time_code'].item().hex(), (.0005*i).hex())
                    self.assertEqual(frame['top_code'].item().hex(), (m.TOP0-.15*.0005*i).hex())

    def test_05_output_on_off_trace_and_final_240_mean_are_bit_identical(self):
        with tempfile.TemporaryDirectory() as td:
            for arm in ('S', 'F'):
                off, on = Path(td)/('off_'+arm), Path(td)/('on_'+arm)
                off.mkdir(); on.mkdir()
                a = m.run_arm(arm, 16, 1200, .0005, .15, .2, off, 600)
                b = self.run_with_shape(arm, on, 1200)
                self.assertEqual((off/(arm+'_trace.jsonl')).read_bytes(), (on/(arm+'_trace.jsonl')).read_bytes())
                self.assertEqual(a['tail_mean_plate_pressure'].hex(), b['tail_mean_plate_pressure'].hex())
                self.assertEqual(b['tail_window_steps'], 240)
                pressure = on/(arm+'_shape/pressure_all.jsonl')
                self.assertTrue(pressure.is_file(), 'per-step pressure history missing')
                rows = [json.loads(line) for line in pressure.read_text().splitlines()]
                self.assertEqual([r['step'] for r in rows], list(range(1, 1201)))
                values = [r['plate_pressure'] for r in rows[-240:]]
                self.assertEqual(float(np.mean(values)).hex(), b['tail_mean_plate_pressure'].hex())

    def test_06_default_off_matches_original_source_bytes(self):
        baseline = os.environ.get('SUYOUNG_BASELINE_SOURCE')
        self.assertTrue(baseline, 'baseline source must be supplied for preservation check')
        old = load_source(baseline, 'sf_original_test')
        with tempfile.TemporaryDirectory() as td:
            for arm in ('S', 'F'):
                before, after = Path(td)/('before_'+arm), Path(td)/('after_'+arm)
                before.mkdir(); after.mkdir()
                a = old.run_arm(arm, 16, 24, .0005, .15, .2, before, 600)
                b = m.run_arm(arm, 16, 24, .0005, .15, .2, after, 600)
                self.assertEqual((before/(arm+'_trace.jsonl')).read_bytes(), (after/(arm+'_trace.jsonl')).read_bytes())
                a.pop('seconds'); b.pop('seconds')
                self.assertEqual(a, b)

    def test_07_manifest_binds_every_frame_and_svg_uses_carried_quads(self):
        with tempfile.TemporaryDirectory() as td:
            state = m.initial_state(16)
            obs = self.observer(td, state, steps=1)
            state['C'][:, 0, 1] = 100.
            obs.after_step(state, 1, dict(plate_pressure=2.))
            obs.finish()
            root = Path(td)/'S_shape'
            manifest = json.loads((root/'MANIFEST.json').read_bytes())
            for row in manifest['frames']:
                for key in ('npz', 'svg'):
                    item = row[key]; data = (root/item['path']).read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(), item['sha256'])
                    self.assertEqual(len(data), item['bytes'])
            svg = ET.fromstring((root/'frame_000001.svg').read_text())
            polys = svg.findall('.//{http://www.w3.org/2000/svg}polygon')
            self.assertEqual(len(polys), len(state['x']))
            offsets = .25/16*np.array([[-1,-1],[1,-1],[1,1],[-1,1]])
            expected = state['x'][0]+offsets@obs.F_total[0].T
            actual = np.array([[float(v) for v in pair.split(',')] for pair in polys[0].attrib['points'].split()])
            np.testing.assert_array_equal(actual, expected)
            self.assertEqual(polys[0].attrib['data-point-id'], '0')
            self.assertEqual(polys[0].attrib['data-particle-id'], str(state['ids'][0]))

    def test_08_particle_id_change_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            state = m.initial_state(16); obs = self.observer(td, state)
            state['ids'][0] = 99
            with self.assertRaisesRegex(ValueError, 'identity'):
                obs.after_step(state, 1, dict(plate_pressure=0.))
            self.assertFalse((Path(td)/'S_shape/MANIFEST.json').exists())

    def test_09_missing_or_duplicate_step_is_rejected(self):
        for seq in ((2,), (1, 1)):
            with self.subTest(seq=seq), tempfile.TemporaryDirectory() as td:
                state = m.initial_state(16); obs = self.observer(td, state)
                with self.assertRaisesRegex(ValueError, 'step sequence'):
                    for i in seq: obs.after_step(state, i, dict(plate_pressure=0.))

    def test_10_incomplete_observer_cannot_claim_complete(self):
        with tempfile.TemporaryDirectory() as td:
            obs = self.observer(td)
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                obs.finish()
            self.assertFalse((Path(td)/'S_shape/MANIFEST.json').exists())

    def test_11_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            self.observer(td)
            snapshot = {p.name: p.read_bytes() for p in (Path(td)/'S_shape').iterdir()}
            with self.assertRaises(FileExistsError): self.observer(td)
            self.assertEqual(snapshot, {p.name: p.read_bytes() for p in (Path(td)/'S_shape').iterdir()})

    def test_12_nonfinite_or_inverted_total_map_is_rejected(self):
        for bad in (float('nan'), -1.):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as td:
                state = m.initial_state(16); obs = self.observer(td, state)
                obs.F_total[:, 0, 0] = bad
                with self.assertRaisesRegex(ValueError, 'total map'):
                    obs.after_step(state, 1, dict(plate_pressure=0.))

    def test_13_cli_shape_output_and_no_false_completion_on_error(self):
        self.assertTrue(hasattr(m, 'ShapeObserver'), 'shape CLI is not implemented')
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)/'run'
            self.assertEqual(m.main(['--output', str(out), '--grid', '16', '--steps', '4',
                                     '--shape-output', '--shape-every', '2']), 0)
            for arm in ('S', 'F'):
                doc = json.loads((out/(arm+'_shape/MANIFEST.json')).read_bytes())
                self.assertEqual(doc['status'], 'SHAPE_OUTPUT_COMPLETE')
                self.assertEqual([r['step'] for r in doc['frames']], [0, 1, 2, 4])
            self.assertTrue(json.loads((out/'INPUT.json').read_bytes())['shape_output'])
            failed = Path(td)/'failed_output'
            with patch.object(m.ShapeObserver, 'save_frame', side_effect=OSError('synthetic output failure')):
                self.assertEqual(m.main(['--output', str(failed), '--grid', '16', '--steps', '4',
                                         '--shape-output', '--shape-every', '2']), 2)
            summary = json.loads((failed/'SUMMARY.json').read_bytes())
            self.assertEqual(summary['status'], 'INCOMPLETE')
            self.assertIsNone(summary['plate_stress_ratio_S_over_F'])
            self.assertFalse(summary['registered_conclusions_adoptable'])

    def test_14_each_arm_has_a_separate_cli_for_external_600s_limit(self):
        for arm in ('S', 'F'):
            with self.subTest(arm=arm), tempfile.TemporaryDirectory() as td:
                out = Path(td)/'run'
                try:
                    rc = m.main(['--output', str(out), '--grid', '16', '--steps', '4',
                                 '--shape-output', '--shape-every', '2', '--arm', arm])
                except SystemExit as exc:
                    rc = exc.code
                self.assertEqual(rc, 0, 'single-arm invocation is not available')
                summary = json.loads((out/'SUMMARY.json').read_bytes())
                self.assertEqual(list(summary['arms']), [arm])
                self.assertEqual(summary['status'], 'DEVELOPMENT_COMPLETE')
                self.assertEqual(summary['ratio_status'], 'SINGLE_ARM_ONLY')
                self.assertIsNone(summary['plate_stress_ratio_S_over_F'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
