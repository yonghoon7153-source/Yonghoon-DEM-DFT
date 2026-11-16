"""Purged-job monitoring regressions. Scheduler, time, and observation are mocked."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('pilot',os.environ.get('E0_TEST_SOURCE',str(Path(__file__).with_name('mixer_e0_pilot_ibb.py'))))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
JID='366423'

def response(rc=0,out='',err=''):
    return SimpleNamespace(returncode=rc,stdout=out,stderr=err)

class PurgedQueue(unittest.TestCase):
    def drive(self,queries,accounting=None,accounting_error=False):
        if accounting is None:accounting=['366423|COMPLETED|0:0|01:00:00|20|1|\n']
        qi=ai=0;clock=[100.];calls=[];times=[1000000]
        def command(argv,timeout):
            nonlocal qi
            self.assertEqual(argv,['squeue','-h','-j',JID,'-o','%i|%T'])
            calls.append(argv);r=queries[min(qi,len(queries)-1)];qi+=1;return r
        def capture(folder,label,argv):
            nonlocal ai
            self.assertEqual(argv,['sacct','-n','-P','-j',JID,'--format=JobIDRaw,State,ExitCode,Elapsed,AllocCPUS,NNodes,MaxRSS'])
            ai+=1
            if accounting_error:raise ValueError('command failed: sacct')
            return accounting[min(ai-1,len(accounting)-1)],{}
        def sleep(seconds):clock[0]+=seconds
        def ns():times[0]+=1;return times[0]
        result=None;error=None
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'evidence').mkdir();case=root/'case';case.mkdir()
            with patch.object(m,'command',side_effect=command),patch.object(m,'capture',side_effect=capture),\
                 patch.object(m,'watch_row'),patch.object(m.time,'monotonic',side_effect=lambda:clock[0]),\
                 patch.object(m.time,'time',return_value=10000.),patch.object(m.time,'time_ns',side_effect=ns),\
                 patch.object(m.time,'sleep',side_effect=sleep):
                try:result=m.wait_job(root,case,JID)
                except ValueError as exc:error=str(exc)
            terminal=(root/'evidence/scheduler_terminal.json')
            record=json.loads(terminal.read_bytes()) if terminal.exists() else None
            evidence=[json.loads(p.read_bytes()) for p in (root/'evidence').glob('squeue_absent_*.json')]
        return dict(result=result,error=error,terminal=record,queries=len(calls),sacct=ai,evidence=evidence)

    def test_exact_slurm_purged_error_reaches_terminal_accounting(self):
        r=self.drive([response(1,err='slurm_load_jobs error: Invalid job id specified\n')])
        self.assertIsNone(r['error']);self.assertEqual(r['result']['state'],'COMPLETED')
        self.assertEqual(r['sacct'],1);self.assertEqual(r['terminal'],r['result'])

    def test_supported_diagnostic_prefixes(self):
        for text in ('Invalid job id specified\n','squeue: error: Invalid job id specified\n'):
            with self.subTest(text=text):
                r=self.drive([response(1,err=text)])
                self.assertIsNone(r['error']);self.assertEqual(r['sacct'],1)

    def test_purged_error_is_preserved_as_absence_not_completion(self):
        text='slurm_load_jobs error: Invalid job id specified\n'
        r=self.drive([response(1,err=text)])
        self.assertEqual(len(r['evidence']),1)
        self.assertEqual(r['evidence'][0],dict(job_id=JID,state='ABSENT',reason='SQUEUE_INVALID_JOB_ID',returncode=1,stdout='',stderr=text,terminal_confirmed=False))

    def test_purged_without_accounting_never_finishes(self):
        r=self.drive([response(1,err='Invalid job id specified')],accounting=[''])
        self.assertIn('terminal state unknown',r['error'])
        self.assertIsNone(r['terminal']);self.assertIsNone(r['result'])
        self.assertGreater(r['sacct'],1)

    def test_delayed_accounting_still_required(self):
        r=self.drive([response(1,err='Invalid job id specified')],accounting=['','366423|COMPLETED|0:0|\n'])
        self.assertIsNone(r['error']);self.assertEqual(r['sacct'],2)

    def test_accounting_command_failure_remains_failure(self):
        r=self.drive([response(1,err='Invalid job id specified')],accounting_error=True)
        self.assertEqual(r['error'],'command failed: sacct');self.assertIsNone(r['terminal'])

    def test_failed_job_not_promoted_to_completed(self):
        r=self.drive([response(1,err='Invalid job id specified')],accounting=['366423|FAILED|1:0|\n'])
        self.assertIsNone(r['error']);self.assertEqual((r['result']['state'],r['result']['exit_code']),('FAILED','1:0'))

    def test_unrelated_or_mixed_errors_remain_query_failures(self):
        for text in ('Unable to contact slurm controller','Permission denied','',
                     'warning: Invalid job id specified; unrelated error',
                     'slurm_load_jobs error: Invalid job id specified\nPermission denied\n',
                     'Invalid job id specified\nInvalid job id specified\n'):
            with self.subTest(text=text):
                r=self.drive([response(1,err=text)])
                self.assertIn('squeue watch failed',r['error']);self.assertEqual(r['sacct'],0)
                self.assertFalse(r['evidence'])

    def test_nonempty_stdout_or_other_returncode_not_hidden(self):
        for q in (response(1,'366423|RUNNING\n','Invalid job id specified'),
                  response(2,err='Invalid job id specified'),response(-15,err='Invalid job id specified')):
            with self.subTest(q=q):
                r=self.drive([q]);self.assertIn('squeue watch failed',r['error']);self.assertEqual(r['sacct'],0)

    def test_successful_empty_queue_behavior_preserved(self):
        r=self.drive([response()]);self.assertIsNone(r['error']);self.assertEqual(r['sacct'],1)
        self.assertFalse(r['evidence'])

    def test_running_then_purged_job(self):
        r=self.drive([response(out='366423|RUNNING\n'),response(1,err='Invalid job id specified')])
        self.assertIsNone(r['error']);self.assertEqual((r['queries'],r['sacct']),(2,1))

    def test_wrong_job_or_nonterminal_accounting_does_not_finish(self):
        for a in ('366424|COMPLETED|0:0|\n','366423|RUNNING|0:0|\n','366423|COMPLETED|0:0|\n366423|COMPLETED|0:0|\n'):
            with self.subTest(a=a):
                r=self.drive([response(1,err='Invalid job id specified')],accounting=[a])
                self.assertIn('terminal state unknown',r['error']);self.assertIsNone(r['terminal'])

if __name__=='__main__':unittest.main(verbosity=2)
