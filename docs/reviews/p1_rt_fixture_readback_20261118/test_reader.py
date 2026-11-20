"""Check the same standalone reader on literal LIGGGHTS column headers."""
import hashlib
import os
from pathlib import Path
import runpy
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'p1_rt_consumer_preparation_20261117'))
from test_rt_fixture import BUILD, SOURCE, fixture


class HeaderReadback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        reader = Path(cls.temp.name) / 'reader.py'
        if os.environ.get('RT_BEFORE') == '1':
            code, _ = BUILD.standalone(SOURCE)
        else:
            sys.path.insert(0, str(HERE))
            from build_reader import render
            code = render()
        reader.write_bytes(code)
        cls.reader = runpy.run_path(str(reader))

    def setUp(self):
        # The engine treats '#' in a restart command as a comment.
        temp_root = HERE if '#' in tempfile.gettempdir() else None
        tmp = tempfile.TemporaryDirectory(dir=temp_root)
        self.addCleanup(tmp.cleanup)
        self.job = fixture(Path(tmp.name), None)

    def change_headers(self, kind, transform):
        paths = []
        for stage in ('RT1', 'RT2'):
            path = self.job / stage / 'post' / ('rt_' + kind + '_2000.dump')
            lines = path.read_bytes().splitlines(keepends=True)
            lines[8] = transform(lines[8].rstrip(b'\r\n')) + b'\n'
            path.write_bytes(b''.join(lines))
            paths.append(path)
        return paths

    def verdict(self):
        return self.reader['evaluate_fixture'](self.job)

    def test_engine_pair_header(self):
        paths = self.change_headers('pair', lambda s: s + b' ')
        r = self.verdict()
        self.assertTrue(r['checks']['pair_read'])
        self.assertEqual(r['numeric']['input_sha256'], [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths])

    def test_engine_atom_header(self):
        self.change_headers('atom', lambda s: s + b' ')
        self.assertTrue(self.verdict()['checks']['atom_read'])

    def test_fields_and_unchanged_artifacts(self):
        for kind in ('atom','pair'):
            self.change_headers(kind, lambda s: s + b' ')
        before = {p:p.read_bytes() for p in self.job.rglob('*') if p.is_file()}
        r = self.verdict()
        self.assertEqual(r['status'], 'PASS')
        self.assertEqual(sum(r['checks'].values()),20)
        self.assertEqual(before,{p:p.read_bytes() for p in before})

    def test_bad_headers_still_rejected(self):
        for kind in ('atom','pair'):
            field = kind + '_read'
            for label, f in [('tab', lambda s:s+b'\t'),('extra', lambda s:s+b' extra '),
                             ('leading',lambda s:b' '+s),('duplicate',lambda s:s+b' '+s.split()[-1]),
                             ('missing',lambda s:s.rsplit(b' ',1)[0]+b' '),
                             ('swap',lambda s:b' '.join(s.split()[:-2]+s.split()[-2:][::-1])+b' ')]:
                with self.subTest(kind=kind, label=label):
                    originals = {p:p.read_bytes() for p in self.job.glob('RT*/post/rt_'+kind+'*.dump')}
                    self.change_headers(kind,f)
                    self.assertFalse(self.verdict()['checks'][field])
                    for path, data in originals.items():path.write_bytes(data)


if __name__ == '__main__':
    unittest.main()
