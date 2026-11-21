"""Synthetic dispatch decisions and receipt/reader binding tests."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ps73_sequence as s


class State:
    def __init__(self, arms=(), half=False, slow=False):
        self.present = set(arms)
        self.half, self.slow = half, slow
        self.rejected = None
        self.bad_gate = None
        self.rm = True
        self.t3_ok = True

    def check_arm(self, arm):
        s.require(arm != self.rejected, 'ARM_OUTCOME_INVALID')

    def allows(self, arm):
        return arm != self.bad_gate

    def selection(self):
        uv = 'UVb' if self.half else 'UVa'
        if uv not in self.present:
            return {'stage':'need_UV', 'next':[uv]}
        tup, arm = {(False,False):('t1','UB'), (False,True):('t2','UVa'),
                    (True,False):('t3','UT3'), (True,True):('t4','UVb')}[self.half,self.slow]
        return {'stage':'resolved', 'tuple':tup, 'arm':arm}

    def rm_pair(self, arm):
        return self.rm

    def combined_ok(self):
        return self.t3_ok


class Sequence(unittest.TestCase):
    def test_base_order(self):
        for n in range(3):
            arms = ['UB','UT','UC']
            r = s.plan(State(arms[:n]))
            self.assertEqual((r['status'],r['next_arm']), ('READY',arms[n]))

    def test_four_rows_and_aux_boundary(self):
        for half in (False, True):
            for slow in (False, True):
                with self.subTest(half=half, slow=slow):
                    base = ['UB','UT','UC']
                    uv = 'UVb' if half else 'UVa'
                    self.assertEqual(s.plan(State(base,half,slow))['next_arm'],uv)
                    base.append(uv)
                    if half and not slow:
                        self.assertEqual(s.plan(State(base,half,slow))['next_arm'],'UTc')
                        base.append('UTc')
                    r = s.plan(State(base,half,slow))
                    self.assertEqual((r['status'],r['next_arm']),('REVIEW',None))
                    self.assertEqual(r['gravity_status'],'DEFERRED_C12_AMENDMENT')
                    self.assertEqual(r['gravity_candidate'], 'G_'+{(False,False):'UB',(False,True):'UVa',(True,False):'UT3',(True,True):'UVb'}[half,slow])

    def test_partial_or_out_of_order(self):
        for st in (State(['UT']), State(['UB','UVa']), State(['UB','UT','UC','UVa','UVb']),
                   State(['UB','UT','UC','UVa','G_UB']), State(['UT3'])):
            self.assertEqual(s.plan(st)['status'],'STOP')
        st = State(['UB']); st.rejected = 'UB'
        self.assertEqual(s.plan(st)['status'],'STOP')
        st = State(); st.bad_gate='UB'
        self.assertEqual(s.plan(st)['status'],'STOP')

    def test_t3_parent_required(self):
        st=State(['UB','UT','UC','UVb'],True,False); st.rm=False
        self.assertEqual(s.plan(st)['status'],'STOP')
        st.present.add('UTc'); st.rm=True; st.t3_ok=False
        self.assertEqual(s.plan(st)['status'],'STOP')

    def test_ambiguous_selection_fails(self):
        for result in ({'stage':'SELECTION_UNRESOLVED'}, {'stage':'need_UV','next':['UB']},
                       {'stage':'need_UV','next':['UVa','UVb']}, {'stage':'resolved','tuple':'t2','arm':'UT3'}):
            st=State(['UB','UT','UC'])
            with patch.object(st,'selection',return_value=result):
                self.assertEqual(s.plan(st)['status'],'STOP')

    def test_receipt_validation(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'UB'; a.mkdir()
            m=b'bed=ps_7_3_r45\njob=UB\nslurm_job=713 slurm_ntasks=6 slurm_nodes=nodeX\nreader_arm_rc=0\nend=T fails=0 reader_rc=0\n'
            v=b'{"job":"UB","bed":"ps_7_3_r45"}'
            (a/'run_manifest.txt').write_bytes(m);(a/'arm_verdict.json').write_bytes(v)
            info=dict(arm='UB',job_id=713,state='COMPLETED',exit_code='0:0',runner_rc=0,technical_ok=True,manifest_sha256=hashlib.sha256(m).hexdigest(),verdict_sha256=hashlib.sha256(v).hexdigest())
            self.assertEqual(s.receipt(a,'UB',info)['job'],'UB')
            for key,val in [('technical_ok',False),('state','FAILED'),('runner_rc',False),('job_id','999'),('manifest_sha256','0'*64),('verdict_sha256','f'*64),('arm','UT')]:
                with self.subTest(key=key),self.assertRaises(s.Halt):
                    s.receipt(a,'UB',dict(info,**{key:val}))
            for mut in (m.replace(b'fails=0',b'fails=1'), m+b'end=T fails=0 reader_rc=0\n', m.replace(b'reader_arm_rc=0',b'reader_arm_rc=2')):
                (a/'run_manifest.txt').write_bytes(mut)
                with self.assertRaises(s.Halt):
                    s.receipt(a,'UB',dict(info,manifest_sha256=hashlib.sha256(mut).hexdigest()))

    def test_control_is_complete_no_move(self):
        P = {'windows':{'W0':5,'uc_steps_dt0':10},'beds':{s.BED:{'s0':100,'h0':1.25}}}
        rows = [{'arm':'UC','bed':s.BED,'step':100+5*i,'w':i,'k':0,'phase':4,'plate_z':1.25,'lift':0.0,'Ps_avg':0.5,'ke_tr_avg':0.5,'ke_rot_avg':0.5} for i in (1,2)]
        run={'summary':{'arm':'UC','bed':s.BED,'result':'DONE','step':'110'},'events':[{'event':'START','step':100},{'event':'NOMOVE_DONE','step':110}],'windows':rows, 'problems':[],'steps':[]}
        self.assertTrue(s.control_ok(run,P))
        for bad in (dict(run,windows=rows[:1]),dict(run,windows=[rows[0],dict(rows[1],lift=1)]),
                    dict(run,windows=[rows[0],dict(rows[1],plate_z=float('nan'))]),
                    dict(run,events=run['events'][:-1]),dict(run,problems=['partial'])):
            self.assertFalse(s.control_ok(bad,P))

    def test_cli_missing_site_is_never_ready(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(s.recommend(Path(d),Path(d),{})['status'],'STOP')


@unittest.skipUnless(os.environ.get('PS73_TEST_KIT'), 'supply immutable synthetic-fixture kit')
class FrozenReader(unittest.TestCase):
    def setUp(self):
        kit=Path(os.environ['PS73_TEST_KIT']).resolve()
        s.verify_kit(kit)
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        spec=importlib.util.spec_from_file_location('test_ps73_original',str(kit/'ul_reader.py'))
        old=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        self.state=s.Originals.__new__(s.Originals)
        self.state.root,self.state.bed,self.state.old=self.root,self.root/s.BED,old
        self.state.params=old.ul_lib.load_params(str(kit/'unload_params.json'))
        self.state.receipts={}

    def make_arm(self,arm,idx,relative,summary='DONE'):
        st=self.state
        old,P=st.old,st.params
        mid=relative/100*P['beds'][s.BED]['h0']*P['units']['um_per_deck_m']
        half=arm in ('UT','UVb')
        fixture={'W':10000 if half else 5000,'dt':5e-7 if half else 1e-6,
                 'steps':old._ladder([mid-.025,mid+.025,mid+.075,mid+.125],[1.2,.8,.6,.4]),
                 'events':[('CROSS',1,'first'),('RM',3,'ncross2')], 'summary':summary}
        d=Path(old._mk_arm(str(self.root),s.BED,arm,fixture,P))
        v=old._arm_v(str(self.root),s.BED,arm,P)
        self.assertEqual(v['primary_status'],'OK')
        m=('job=%s\nbed=%s\nslurm_job=%s slurm_ntasks=6 slurm_nodes=synthetic\n'
           'reader_arm_rc=0\nend=T fails=0 reader_rc=0\n')%(arm,s.BED,idx)
        raw=json.dumps(v,default=str,allow_nan=False).encode()
        (d/'arm_verdict.json').write_bytes(raw)
        (d/'run_manifest.txt').write_bytes(m.encode())
        st.receipts[arm]=dict(arm=arm,job_id=idx,state='COMPLETED',exit_code='0:0',runner_rc=0,
                              technical_ok=True,manifest_sha256=s.digest(m.encode()),verdict_sha256=s.digest(raw))
        return d

    def test_selection_state_uses_site_original_even_with_stale_selection_json(self):
        st=self.state
        for arm,idx,rho in [('UB',701,1.0),('UT',702,1.2)]:
            self.make_arm(arm,idx,rho)
            st.check_arm(arm)
        (st.bed/'selection.json').write_text('{"stage":"resolved","tuple":"t1"}',encoding='utf8')
        self.assertEqual(st.selection()['next'],['UVb'])
        self.make_arm('UVb',703,1.22)
        self.assertEqual(st.selection()['tuple'],'t3')
        st.check_arm('UVb')

    def test_corrupted_current_result_is_rejected_even_if_saved_report_and_rc_match(self):
        st=self.state
        d=self.make_arm('UB',801,1.0)
        st.check_arm('UB')
        (d/'ul_events.csv').write_text('event,k,step,plate_z,lift,detail\n',encoding='utf8')
        with self.assertRaises(s.Halt):
            st.check_arm('UB')

if __name__=='__main__':
    unittest.main()
