"""Twenty-check fixture synthetic mutations and code closure."""
import copy,hashlib,importlib.util,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from test_rt_contract import put,atom,screen,row,write,load
SOURCE=HERE.parents[2]/'docs/data/ps45_unload_20261009'
BUILD=load('prepare_consumer',HERE/'prepare_consumer.py')
def rawhash(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def fixture(root,kit):
    run=root/'fixture';run.mkdir()
    producer=run/'P';producer.mkdir();put(producer/'rc','0\n');(producer/'fixture.bin').write_bytes(b'producer')
    ck=(run/'RT1/rt.bin').as_posix();h=hashlib.sha256(b'rt-binary').hexdigest()
    for kind in ('RT1','RT2'):
        d=run/kind;put(d/'deck.txt','in.hist_'+kind.lower()+'.liggghts\n')
        put(d/'rc','0\n');put(d/'np.txt','6\n');put(d/'ckpt.txt',(producer/'fixture.bin').as_posix()+'\n' if kind=='RT1' else ck+'\n')
        put(d/'screen.out',screen(kind,'hist_rt'))
        put(d/'log.liggghts','read_restart '+(producer/'fixture.bin').as_posix()+'\n' if kind=='RT1' else 'read_restart '+ck+'\n')
        (d/'post').mkdir();write(d/'post/rt_pair_2000.dump',[row(i) for i in range(1,20,2)]);atom(d/'post/rt_atom_2000.dump',20)
    (run/'RT1/rt.bin').write_bytes(b'rt-binary')
    original=run/'RT1/post/rt_pair_2000.dump'
    lines=original.read_text().splitlines();lines[8]='ITEM: ENTRIES '+' '.join(f'c_hb_ph[{i}]' for i in range(1,8))
    lines[9:]=[' '.join(t[6:9]+t[21:25]) for t in (line.split() for line in lines[9:])]
    put(producer/'producer/pair_2000.dump','\n'.join(lines)+'\n')
    put(run/'run_manifest.txt',f'job_dir={run.as_posix()}\nrt1_bin={ck} sha256={h}\nrt2_ckpt={ck} sha256={h}\n')
    return run
class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=os.environ.get('RT_TEST_TMPDIR'));self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.assertTrue(callable(getattr(BUILD,'build',None)),'fixture builder missing')
        self.kit=self.root/'kit';BUILD.build(SOURCE,self.kit)
        self.reader=self.kit/'history_test/read_rt_grammar.py'
        self.mod=load('rt_grammar',self.reader);self.run=fixture(self.root,self.kit)
    def verdict(self,status='PASS'):
        r=self.mod.evaluate_fixture(self.run);self.assertEqual(r['status'],status,r)
        self.assertEqual(len(r['checks']),20)
        return r
    def test_normal_twenty_checks_no_writes(self):
        before={p:p.read_bytes() for p in self.run.rglob('*') if p.is_file()}
        r=self.verdict();self.assertTrue(all(x is True for x in r['checks'].values()))
        self.assertEqual(before,{p:p.read_bytes() for p in self.run.rglob('*') if p.is_file()})
    def test_every_named_check_has_negative_observation(self):
        # Change each required evidence class independently, rebuilding a fresh synthetic run.
        mutations=[
         ('P_tech','P/rc','1'),('RT1_exists','RT1/deck.txt','wrong'),('RT2_exists','RT2/deck.txt','wrong'),
         ('RT1_args','RT1/np.txt','4'),('RT2_args','RT2/ckpt.txt','wrong'),
         ('RT1_tech','RT1/rc','1'),('RT2_tech','RT2/rc','1'),
         ('RT1_marker','RT1/screen.out',screen('RT1','wrong')),('RT2_marker','RT2/screen.out',screen('RT2','wrong')),
         ('RT1_resets','RT1/screen.out',screen('RT1','hist_rt').replace('Resetting','Not-resetting')),
         ('RT2_resets','RT2/screen.out',screen('RT2','hist_rt').replace('Resetting','Not-resetting')),
         ('bind_sha','RT1/rt.bin','changed'),('bind_path','RT2/log.liggghts','read_restart other\n'),
         ('post_list','RT1/post/rt_pair_999.dump','extra'),
         ('pair_read','RT1/post/rt_pair_2000.dump','bad'),('atom_read','RT1/post/rt_atom_2000.dump','bad')]
        for name,path,value in mutations:
            p=self.run/path;old=p.read_bytes() if p.exists() else None;put(p,value)
            r=self.verdict('FAIL');self.assertIs(r['checks'][name],False,name)
            if old is None:p.unlink()
            else:p.write_bytes(old)
        p=self.run/'RT1/post/rt_atom_2000.dump';old=p.read_bytes();put(p,p.read_text().replace('2000','2001',1));self.assertFalse(self.verdict('FAIL')['checks']['step']);p.write_bytes(old)
        for s in ('RT1','RT2'):write(self.run/s/'post/rt_pair_2000.dump',[])
        self.assertFalse(self.verdict('FAIL')['checks']['pairs'])
        for s in ('RT1','RT2'):write(self.run/s/'post/rt_pair_2000.dump',[row(i) for i in range(1,20,2)])
        changed=[row(i) for i in range(1,20,2)];changed[0][22]*=2
        write(self.run/'RT2/post/rt_pair_2000.dump',changed);self.assertFalse(self.verdict('FAIL')['checks']['g2cp'])
        write(self.run/'RT2/post/rt_pair_2000.dump',[row(i) for i in range(1,20,2)])
        p=self.run/'P/producer/pair_2000.dump';t=p.read_text();put(p,t.replace('0.0001','0.0009'));self.assertFalse(self.verdict('FAIL')['checks']['hist_value'])
    def test_deltaMax_is_report_only_for_producer_history(self):
        p=self.run/'P/producer/pair_2000.dump';put(p,p.read_text().replace('0.0003','0.0004',1));self.verdict()
    def test_producer_fractional_ID_and_conflicting_duplicate(self):
        p=self.run/'P/producer/pair_2000.dump';raw=p.read_bytes();lines=p.read_text().splitlines()
        for token in ('1.0000000000000001','9007199254740993','0','0_1'):
            bad=lines.copy();bad[9]=token+' '+' '.join(bad[9].split()[1:]);put(p,'\n'.join(bad)+'\n');self.assertFalse(self.verdict('FAIL')['checks']['hist_value'])
        p.write_bytes(raw)
        bad=lines.copy();bad[3]='11';words=bad[9].split();words[4]='0.1';bad.append(' '.join(words));put(p,'\n'.join(bad)+'\n')
        self.assertFalse(self.verdict('FAIL')['checks']['hist_value'])
    def test_full_dump_extra_frame_atom_fractional_id(self):
        p=self.run/'RT1/post/rt_atom_2000.dump';raw=p.read_bytes();p.write_bytes(raw+raw);self.assertFalse(self.verdict('FAIL')['checks']['atom_read']);p.write_bytes(raw)
        lines=raw.decode().splitlines();lines[9]='1.0000000000000001 '+' '.join(lines[9].split()[1:]);put(p,'\n'.join(lines)+'\n')
        self.assertFalse(self.verdict('FAIL')['checks']['atom_read'])
    def test_bind_duplicate_missing_and_path_alias(self):
        p=self.run/'run_manifest.txt';good=p.read_text()
        put(p,good+good.splitlines()[0]+'\n');self.verdict('FAIL');put(p,good)
        (self.run/'RT1/rt.bin').unlink();self.verdict('FAIL')
    def test_isolated_script_uses_no_repository_modules(self):
        isolated=self.root/'isolated';isolated.mkdir();p=isolated/'read_rt_grammar.py';p.write_bytes(self.reader.read_bytes())
        cp=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(p),str(self.run)],capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stderr);self.assertEqual(json.loads(cp.stdout)['status'],'PASS')
    def test_closed_sources_equal_numeric_binding_and_history(self):
        closure=self.mod.SOURCE_SHA256
        self.assertEqual(closure['numeric'],rawhash(HERE.parent/'p1_rt_numeric_preparation_20261117/rt_numeric.py'))
        self.assertEqual(self.mod.N.g2cp_compare.__code__.co_code,load('numeric_orig',HERE.parent/'p1_rt_numeric_preparation_20261117/rt_numeric.py').g2cp_compare.__code__.co_code)
        self.assertEqual(closure['binding'],rawhash(HERE.parent/'p1_rt_runner_preparation_20261117/rt_binding.py'))
        self.assertEqual(self.mod.CONTRACT['tolerances'],json.loads((SOURCE/'history_test/history_params.json').read_bytes())['tolerances'])
    def test_original_and_prior_layers_unchanged(self):
        report=json.loads((self.kit/'RT_CONSUMER_LAYER.json').read_bytes())
        self.assertFalse(report['operational_kit_ready'])
        for p in SOURCE.rglob('*'):
            if p.is_file():self.assertEqual(p.read_bytes(),(self.kit/p.relative_to(SOURCE)).read_bytes())
        self.assertIn('RT_RUNNER_LAYER_ONLY',(self.kit/'run_unload_rt_dev.sh').read_text())
        previous=self.root/'previous'
        load('previous_builder',HERE.parent/'p1_rt_numeric_preparation_20261117/prepare_numeric.py').build(SOURCE,previous)
        old={p.relative_to(previous).as_posix():p.read_bytes() for p in previous.rglob('*') if p.is_file()}
        new={p.relative_to(self.kit).as_posix():p.read_bytes() for p in self.kit.rglob('*') if p.is_file()}
        self.assertEqual(len(old),113);self.assertEqual(len(new),122)
        self.assertEqual(old,{name:new[name] for name in old})

if __name__=='__main__':unittest.main(verbosity=2)
