"""Offline contracts for the authorized first N0 development wave."""
from pathlib import Path
import runpy
import tarfile
import tempfile
import unittest
from unittest.mock import patch


def controller():
    return runpy.run_path(str(Path(__file__).with_name('mixer_rotation_n0_ibb.py')))


class RotationTests(unittest.TestCase):
    def test_rotating_deck_identity(self):
        c = controller()
        root = Path(__file__).resolve().parents[1]
        deck = root / c['base']['F8'] / 'planned_assets/PRECAL_N0/in.mixer'
        c['rotation_deck'](deck.read_bytes())
        with self.assertRaises(ValueError):
            c['rotation_deck'](deck.read_bytes().replace(b'32976', b'1000'))

    def test_wall_limits(self):
        check = controller()['wall_limits']
        check('cpu-60|', 'author|cpu-60|7-00:00:00', 'MaxTime=14-00:00:00 State=UP', 'author')
        for qos, assoc, part in [
            ('cpu-60|1-00:00:00', 'author|cpu-60|7-00:00:00', 'MaxTime=14-00:00:00 State=UP'),
            ('cpu-60|', 'other|cpu-60|7-00:00:00', 'MaxTime=14-00:00:00 State=UP'),
            ('cpu-60|', 'author|cpu-60|1-00:00:00', 'MaxTime=14-00:00:00 State=UP'),
            ('cpu-60|', 'author|cpu-60|7-00:00:00', 'MaxTime=1-00:00:00 State=UP'),
        ]:
            with self.subTest(qos=qos, assoc=assoc, part=part), self.assertRaises(ValueError):
                check(qos, assoc, part, 'author')

    def test_exact_frames(self):
        check = controller()['frames_ok']
        names = ['mix_%d.liggghts' % (i * 32976) for i in range(1, 235)]
        self.assertTrue(check(names))
        self.assertFalse(check(names[:-1]))
        self.assertFalse(check(names[1:] + ['mix_0.liggghts']))
        self.assertFalse(check(names + names[:1]))

    def test_terminal_requires_exact_parent_and_exit(self):
        check = controller()['completed']
        end = dict(job_id='42', returncode=0)
        self.assertTrue(check('42|COMPLETED|0:0|', '42', end))
        for acct, item in [
            ('42.batch|COMPLETED|0:0|', end), ('42|TIMEOUT|0:0|', end),
            ('42|COMPLETED|1:0|', end), ('42|COMPLETED|0:0|', dict(job_id='43', returncode=0)),
            ('', end), ('42|COMPLETED|0:0|', None),
        ]:
            self.assertFalse(check(acct, '42', item))

    def test_fresh_authority(self):
        val = controller()['authority']()
        self.assertEqual(val['allowed_to_submit'], ['PRECAL_N0'])
        self.assertEqual(val['previous_job'], '366423')
        self.assertTrue(val['development_qualification_accepted'])
        self.assertFalse(val['paper_qualification'])
        self.assertFalse(val['e0_W9_at_T9'])
        self.assertFalse(val['automatic_retry'])

    def test_archives_and_immutable_pointer(self):
        c = controller()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'packet'
            here = root / 'B' / c['base']['F8']
            case = here / 'cases/PRECAL_N0'
            (case / 'post').mkdir(parents=True)
            for i in range(1, 235):
                (case / 'post' / ('mix_%d.liggghts' % (i * 32976))).write_bytes(b'x')
            for name in ('admission', 'approvals'):
                (here / name).mkdir()
            for path in (root / 'control/rotation_pin.json', root / 'control/n0_author_go.json',
                         root / 'B_manifest.json', here / 'campaign_policy.json'):
                c['put'](path, {})
            c['put'](case / 'job_end.json', dict(job_id='42', returncode=0))
            with patch.dict(c['base'], runtime=lambda *args: {'matches': True}):
                self.assertEqual(0, c['collect'](root, case, '42', '42|COMPLETED|0:0|', None, None, None))
            record = c['read'](root.parent / 'return.json')
            self.assertTrue(record['return_ready'])
            folder = root.parent / record['directory']
            sums = (folder / 'SHA256SUMS').read_text().splitlines()
            for line in sums:
                digest, name = line.split('  ')
                self.assertEqual(digest, c['sha'](folder / name))
            with tarfile.open(folder / 'n0_full_result.tar.gz') as tar:
                self.assertEqual(len(tar.getnames()), 235)

    def test_collect_only_unfinished_stops_before_writing(self):
        c = controller()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ValueError, 'not accounted terminal'):
                c['collect'](root, root, '42', '42|RUNNING|0:0|', None, None, None)
            self.assertEqual(list(root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()

