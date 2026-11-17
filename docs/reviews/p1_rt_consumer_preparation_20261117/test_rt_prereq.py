"""Candidate identity and actual raw reread, never a field fixture."""
import copy,hashlib,json,os,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import test_rt_fixture as F
import rt_fixture_prereq as M
from test_rt_contract import put
class Prereq(unittest.TestCase):
    def setUp(self):
        F.Fixture.setUp(self)
        self.hkit=self.kit/'history_test'
        self.expected={n:F.rawhash(self.hkit/n) for n in M.FILES}
        for stage,deck in M.STAGES:
            put(self.run/stage/'deck.txt',deck+'\n')
            for n in (deck,'plate_hist.stl'):(self.run/stage/n).write_bytes((self.hkit/n).read_bytes())
        self.binary='1'*64
        self.verdict=self.run/'rt_grammar_verdict.json'
        self.verdict.write_text(json.dumps(self.mod.evaluate_fixture(self.run)),encoding='utf8')
        sums=self.hkit/'RT_CANDIDATE_SHA256SUMS'
        self.assertTrue(sums.is_file(),'candidate identity list not shipped')
        p=self.run/'run_manifest.txt'
        put(p,p.read_text()+f'mode=rt_grammar\nend=synthetic_done\nkit={self.hkit.as_posix()}\nsums_sha256={F.rawhash(sums)}\nlmp_sha256={self.binary}\n')
    def check(self,ok=True):
        before={p:p.read_bytes() for p in self.run.rglob('*') if p.is_file()}
        r=M.check(self.verdict,self.binary,self.expected)
        self.assertEqual(r['ok'],ok,r);self.assertFalse(r['operational_go'])
        self.assertEqual(before,{p:p.read_bytes() for p in self.run.rglob('*') if p.is_file()})
        return r
    def test_valid_twenty_raw_reread(self):self.check()
    def test_forged_json_true_does_not_hide_changed_raw(self):
        put(self.run/'RT1/screen.out','bad');self.check(False)
    def test_wrong_binary_missing_end_and_duplicate_manifest(self):
        p=self.run/'run_manifest.txt';good=p.read_text()
        for s in (good.replace(self.binary,'2'*64),good.replace('end=synthetic_done\n',''),good+'mode=rt_grammar\n'):
            put(p,s);self.check(False)
    def test_source_deck_reader_contract_and_list_mutations(self):
        paths=[self.run/'RT1/in.hist_rt1.liggghts',self.run/'P/plate_hist.stl',
               self.hkit/'read_rt_grammar.py',self.hkit/'rt_fixture_contract.json',self.hkit/'RT_CANDIDATE_SHA256SUMS']
        for p in paths:
            old=p.read_bytes();p.write_bytes(old+b'\n');self.check(False);p.write_bytes(old)
    def test_false_int_boolean_extra_missing_check(self):
        original=json.loads(self.verdict.read_bytes())
        bad=[]
        for value in (False,1,None):
            v=copy.deepcopy(original);v['checks']['pairs']=value;bad.append(v)
        v=copy.deepcopy(original);v['exit_code']=False;bad.append(v)
        v=copy.deepcopy(original);v['checks']['extra']=True;bad.append(v)
        v=copy.deepcopy(original);del v['checks']['pairs'];bad.append(v)
        for v in bad:self.verdict.write_text(json.dumps(v));self.check(False)
    def test_other_verdict_location_and_absent_binary(self):
        v=json.loads(self.verdict.read_bytes());v['run_dir']=str(self.root);self.verdict.write_text(json.dumps(v));self.check(False)
    def test_honest_run_alias_if_supported(self):
        alias=self.root/'alias'
        try:alias.symlink_to(self.run,target_is_directory=True)
        except OSError:self.skipTest('local symlink privilege unavailable')
        self.verdict=alias/self.verdict.name;self.check()
    def test_candidate_identity_is_not_self_supplied_approval(self):
        wrong=self.expected.copy();wrong['read_rt_grammar.py']='0'*64
        self.assertFalse(M.check(self.verdict,self.binary,wrong)['ok'])

if __name__=='__main__':unittest.main(verbosity=2)
