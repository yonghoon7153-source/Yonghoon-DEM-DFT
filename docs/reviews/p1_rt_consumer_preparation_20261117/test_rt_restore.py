"""Adapter/CLI uses raw legacy checks; no engine, no production data."""
import contextlib,copy,io,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import rt_restore as M
from test_rt_contract import put,screen,atom,write
SOURCE=HERE.parents[2]/'docs/data/ps45_unload_20261009'
class Restore(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=os.environ.get('RT_TEST_TMPDIR'));self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.bed='ps_7_3_r45';self.job=self.root/self.bed/'RJ';self.job.mkdir(parents=True)
        self.r={'schema':'rt_restore_candidate_v1','restore_rule':'rev5_g2cp','status':'RESTORED',
                'bed':self.bed,'job':'RJ','operational_qualification':False}
    def cli(self,*extra,code=0):
        with patch.object(M,'restore',return_value=self.r),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(M.main([str(self.root),self.bed,*extra]),code)
    def test_default_no_certificate_and_no_receipt_write(self):
        put(self.job/'receipt.txt','old');self.cli();self.assertEqual(list(self.job.iterdir()),[self.job/'receipt.txt'])
    def test_explicit_publish_then_reread_preserves_certificate(self):
        self.cli('--publish-new');raw=(self.job/'restore_verdict.json').read_bytes()
        self.r['status']='UNCONFIRMED';self.cli(code=2);self.assertEqual(raw,(self.job/'restore_verdict.json').read_bytes())
        self.cli('--publish-new',code=3);self.assertEqual(raw,(self.job/'restore_verdict.json').read_bytes())
    def test_publish_failure_nonzero(self):
        with patch.object(M,'publish_new',side_effect=OSError('injected')):self.cli('--publish-new',code=3)
    def test_gate_requires_rev5_and_both_prereqs_and_receipt(self):
        class Old:
            receipt=(True,'','grammar_prereq=PASS\nrt_grammar_prereq=PASS\n')
            def _job_receipt(self,*a):return self.receipt
        old=Old()
        with patch.object(M,'legacy_reader',return_value=old):
            put(self.job/'restore_verdict.json',json.dumps(self.r));self.assertTrue(M.job_restored(self.root,self.bed,'RJ'))
            old.receipt=(True,'','grammar_prereq=PASS\n');self.assertFalse(M.job_restored(self.root,self.bed,'RJ'))
            old.receipt=(False,'','grammar_prereq=PASS\nrt_grammar_prereq=PASS\n');self.assertFalse(M.job_restored(self.root,self.bed,'RJ'))
            old.receipt=(True,'','grammar_prereq=PASS\nrt_grammar_prereq=PASS\n')
            for key in ('restore_rule','schema','bed','job'):
                r=self.r.copy();r[key]='old';put(self.job/'restore_verdict.json',json.dumps(r));self.assertFalse(M.job_restored(self.root,self.bed,'RJ'))
    def test_gate_duplicate_or_contradictory_prereq_not_accepted(self):
        class Old:
            receipt=''
            def _job_receipt(self,*a):return True,'',self.receipt
        old=Old();put(self.job/'restore_verdict.json',json.dumps(self.r))
        with patch.object(M,'legacy_reader',return_value=old):
            for key in ('grammar_prereq','rt_grammar_prereq'):
                for value in ('PASS','FAIL'):
                    old.receipt='grammar_prereq=PASS\nrt_grammar_prereq=PASS\n'+key+'='+value+'\n'
                    self.assertFalse(M.job_restored(self.root,self.bed,'RJ'))
    def test_actual_legacy_reader_synthetic_small_fixture_not_qualified(self):
        old=M.legacy_reader(SOURCE);P=old.ul_lib.load_params(str(SOURCE/'unload_params.json'))
        old._mk_rj(str(self.root),self.bed,P)
        step=P['beds'][self.bed]['s0'];orig=self.root/self.bed/'in'/f'contact_{step}.liggghts'
        rows=M.C.N.read_contacts(orig,'legacy26')['rows'].values()
        rt=[v[:21]+[0.,0.,0.,0.]+v[21:] for v in rows]
        records=['job_dir='+self.job.as_posix()]
        for kind in ('R','UNread','Ut0','RT1','RT2'):records.append(f'stage={kind} screen=screen.txt rc=0 check=PASS')
        for s in ('RT1','RT2'):
            put(self.job/s/'screen.txt',screen(s,self.bed,step));put(self.job/s/'run_check.txt',f'{s} screen.txt PASS rc=0 procs=6\n')
            (self.job/s/'post').mkdir();write(self.job/s/'post'/f'rt_pair_{step}.dump',rt,step=step);atom(self.job/s/'post'/f'rt_atom_{step}.dump',3,step)
        (self.job/'RT1/rt.bin').write_bytes(b'fixture')
        import hashlib
        h=hashlib.sha256(b'fixture').hexdigest();ck=(self.job/'RT1/rt.bin').as_posix()
        records += [f'rt1_bin={ck} sha256={h}',f'rt2_ckpt={ck} sha256={h}']
        put(self.job/'run_manifest.txt','\n'.join(records)+'\n');put(self.job/'RT2/log_screen.liggghts','read_restart '+ck+'\n')
        p=self.root/self.bed/'in'/P['beds'][self.bed]['orig_log']
        put(p,(self.job/'R/screen.txt').read_text().replace('on 6 procs','on 24 procs')+'\n6 by 4 by 1 MPI processor grid\n')
        hist=self.root/'history.json';put(hist,json.dumps({'schema':'ps45_unload_history_verdict_v1','exit_code':0,
              'rows':{f'H{i}':{'status':'PASS'} for i in range(6)},'info':{'syn':{'status':'PASS','plate_fn_sign':-1},'force_timing':'PASS'}}))
        r=M.restore(self.root,self.bed,'RJ',hist,SOURCE)
        self.assertEqual(r['checks']['G2cp']['status'],'PASS');self.assertTrue(all(s['ok'] for s in r['checks']['rt_technical'].values()))
        self.assertEqual(r['status'],'UNCONFIRMED',r);self.assertFalse((self.job/'restore_verdict.json').exists())

    def test_source_selection_failure_keeps_prior_failure_priority(self):
        class Old:
            class ul_lib:
                @staticmethod
                def load_params(_):return {'ext_10_0':{},'beds':{self.bed:{'orig_log':'log.txt','atoms':3}}}
            def restore_verdict(self,*_):return {'s0':2000,'checks':checks}
        clean={'syntax':{'ok':True},'g0':{'ok':True},'pre_post':{'equal':True},'G2c':{'status':'FAIL'}}
        cases=[('syntax',{'ok':False},'SYNTAX_FAIL'),('g0',{'ok':False},'VALUE_MISMATCH'),
               ('G1',{'status':'FAIL'},'VALUE_MISMATCH'),('pre_post',{'equal':False},'VALUE_MISMATCH'),
               ('G2',{'status':'NOT_COMPUTED'},'UNCONFIRMED'),('G2c',{'status':'FAIL'},'UNCONFIRMED')]
        for key,value,expected in cases:
            with self.subTest(key=key):
                checks=copy.deepcopy(clean);checks[key]=value
                with patch.object(M,'legacy_reader',return_value=Old()),patch.object(M.C,'select_source',side_effect=ValueError('no unique source')):
                    r=M.restore(self.root,self.bed,kit=SOURCE)
                self.assertEqual(r['status'],expected)
                self.assertEqual(r['checks'].get('G2c_cont'),checks['G2c'])
                self.assertNotIn('G2c',r['checks']);self.assertFalse(r['checks']['source_selection']['ok'])

if __name__=='__main__':unittest.main(verbosity=2)
