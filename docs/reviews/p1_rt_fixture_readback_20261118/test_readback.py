"""Original-directory and provenance guards exercised on synthetic return bytes."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_reader import render
from readback import inspect
sys.path.insert(0, str(HERE.parent / 'p1_rt_consumer_preparation_20261117'))
from test_rt_fixture import fixture


class Readback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = render()

    def setUp(self):
        temp = tempfile.TemporaryDirectory(dir=HERE if '#' in tempfile.gettempdir() else None)
        self.addCleanup(temp.cleanup)
        self.site = Path(temp.name).resolve()
        work = self.site / 'work'
        work.mkdir()
        self.job = fixture(work, None)
        with (self.job / 'run_manifest.txt').open('a') as f:
            f.write('job_id=90001\n')
        (self.site / 'SOURCE_PIN').write_text('a'*40)
        (self.site / 'submission.txt').write_text('90001;site\n')
        (self.job / 'rt_grammar_verdict.json').write_text(json.dumps(dict(status='FAIL', exit_code=2, checks={})))
        self.files = {p.relative_to(work).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in work.rglob('*') if p.is_file()}
        self.evidence = dict(job='90001', files=self.files, source_pin='a'*40)

    def read(self):
        return inspect(self.site, self.evidence, self.reader, 'b'*40)

    def test_old_result_is_retained(self):
        result = self.read()
        self.assertEqual((result['original_verdict'],result['status']),('FAIL','PASS'))
        self.assertEqual(sum(result['checks'].values()),20)
        self.assertEqual(result['inputs_verified_before_after'],len(self.files))
        self.assertFalse(result['physical_qualification'])

    def test_changed_input_and_wrong_receipts(self):
        for name, value in [('SOURCE_PIN','other'),('submission.txt','90002'),
                            ('work/fixture/P/rc','1')]:
            p = self.site / name
            raw = p.read_bytes()
            p.write_text(value)
            with self.assertRaises(ValueError):
                self.read()
            p.write_bytes(raw)

    def test_changed_during_read_stops(self):
        revised = self.reader + b"\nold=evaluate_fixture\ndef evaluate_fixture(run):\n    result=old(run)\n    (run/'P/rc').write_text('1')\n    return result\n"
        with self.assertRaisesRegex(ValueError, 'input digest differs'):
            inspect(self.site, self.evidence, revised, 'b'*40)


if __name__ == '__main__':
    unittest.main()
