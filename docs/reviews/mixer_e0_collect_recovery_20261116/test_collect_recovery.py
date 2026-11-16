import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('prep',HERE/'prepare_collect.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
SHA='56f2d5ea366e55c987417bc7fea0f777598fb807f21de1887ae4aeea8af2a943'

class Recovery(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.p=Path(self.tmp.name)/'packet';self.p.mkdir()
        (self.p/'returns').mkdir();(self.p/'evidence').mkdir()
        (self.p/'returns/e0_report.tar.gz').write_bytes(b'original-report')
        h=hashlib.sha256(b'original-report').hexdigest()
        (self.p/'returns/SHA256SUMS').write_text(h+'  e0_report.tar.gz\n')
        (self.p/'evidence/controller_first.json').write_bytes(b'{"state":"INCOMPLETE"}')
        for folder in ('control','B'):
            (self.p/folder).mkdir();(self.p/folder/'keep').write_bytes(b'unchanged')

    def attempt(self, **kw):
        args=dict(job='366423',queue='',accounting='366423|COMPLETED|0:0|01:00:00|20|1|\n',live_controllers=[],controller_sha=SHA)
        args.update(kw);return m.prepare(self.p,**args)

    def test_first_returns_and_all_evidence_preserved(self):
        try:r=self.attempt()
        except Exception as e:self.fail('recovery preparation rejected: '+str(e))
        old=self.p/r['history']
        self.assertEqual((old/'returns/e0_report.tar.gz').read_bytes(),b'original-report')
        self.assertEqual((old/'evidence/controller_first.json').read_bytes(),b'{"state":"INCOMPLETE"}')
        self.assertFalse((self.p/'returns').exists())
        self.assertTrue((self.p/'evidence').is_dir())
        for folder in ('control','B'):self.assertEqual((self.p/folder/'keep').read_bytes(),b'unchanged')

    def test_running_job_cannot_rotate_any_output(self):
        with self.assertRaises(ValueError):self.attempt(queue='366423|RUNNING\n')
        self.assertTrue((self.p/'returns/e0_report.tar.gz').is_file())

    def test_unknown_or_duplicate_terminal_record_rejected(self):
        for a in ('','366423|RUNNING|0:0|\n','366423|COMPLETED|0:0|\n366423|COMPLETED|0:0|\n','366424|COMPLETED|0:0|\n'):
            with self.subTest(a=a),self.assertRaises(ValueError):self.attempt(accounting=a)

    def test_failed_terminal_job_is_collected_not_promoted(self):
        try:r=self.attempt(accounting='366423|FAILED|1:0|\n')
        except Exception as e:self.fail('failed-job evidence must be recoverable: '+str(e))
        self.assertEqual(r['terminal']['state'],'FAILED')
        self.assertFalse(r['scientific_acceptance'])

    def test_live_old_controller_blocks_rotation(self):
        with self.assertRaises(ValueError):self.attempt(live_controllers=[123])

    def test_wrong_controller_identity_blocks_rotation(self):
        with self.assertRaises(ValueError):self.attempt(controller_sha='0'*64)

    def test_manifest_corruption_preserves_original(self):
        (self.p/'returns/e0_report.tar.gz').write_bytes(b'corrupt')
        with self.assertRaises(ValueError):self.attempt()
        self.assertEqual((self.p/'returns/e0_report.tar.gz').read_bytes(),b'corrupt')

    def test_second_preparation_does_not_rotate_again(self):
        try:self.attempt()
        except Exception as e:self.fail('first recovery preparation: '+str(e))
        with self.assertRaises(FileExistsError):self.attempt()
        self.assertTrue((self.p/'collection_history/collect_366423_20261116/returns/e0_report.tar.gz').is_file())

    def test_existing_destination_is_not_overwritten(self):
        x=self.p/'collection_history/collect_366423_20261116';x.mkdir(parents=True)
        (x/'marker').write_bytes(b'keep')
        with self.assertRaises(FileExistsError):self.attempt()
        self.assertEqual((x/'marker').read_bytes(),b'keep')

    def test_frozen_collect_main_original_collision_then_new_archives(self):
        spec=importlib.util.spec_from_file_location('frozen',HERE.parents[2]/'scripts/mixer_e0_pilot_ibb.py')
        old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        self.assertEqual(hashlib.sha256(Path(old.__file__).read_bytes()).hexdigest(),SHA)
        case=self.p/'B'/old.F8/'cases/PRECAL_E0';case.mkdir(parents=True)
        (case/'submission.receipt.json').write_text('{"state":"SUBMITTED","job_id":"366423"}')
        (case/'job_end.json').write_text('{"returncode":0}')
        (case/'synthetic.log').write_bytes(b'no simulation was executed')
        (self.p/'B_manifest.json').write_text('{"files":[]}')
        executable=self.p/'dummy';executable.write_bytes(b'not an executable')
        argv=['controller','--collect','--root',str(self.p),'--binary',str(executable),'--mpi',str(executable),'--env-prefix',str(self.p)]
        def invoke():
            with patch.object(old.sys,'argv',argv),patch.object(old.sys,'platform','linux'),patch.dict(os.environ,dict(os.environ)),\
                 patch.object(old,'author_scope',return_value={}),\
                 patch.object(old,'wait_job',return_value={'state':'COMPLETED','exit_code':'0:0'}),\
                 patch.object(old,'runtime',return_value={'matches':True}),\
                 patch.object(old.os,'statvfs',return_value=SimpleNamespace(f_bavail=10**10,f_frsize=1024),create=True),\
                 patch.object(old,'command',side_effect=AssertionError('external command forbidden')):
                return old.main()
        with self.assertRaisesRegex(ValueError,'report already exists'):invoke()
        original=(self.p/'returns/e0_report.tar.gz').read_bytes()
        r=self.attempt()
        self.assertEqual(invoke(),0)
        self.assertEqual((self.p/r['history']/'returns/e0_report.tar.gz').read_bytes(),original)
        self.assertTrue((self.p/'returns/e0_full_result.tar.gz').is_file())
        rows=(self.p/'returns/SHA256SUMS').read_text().splitlines()
        self.assertEqual(len(rows),2)
        for line in rows:
            h,name=line.split('  ');self.assertEqual(hashlib.sha256((self.p/'returns'/name).read_bytes()).hexdigest(),h)

if __name__=='__main__':unittest.main(verbosity=2)
