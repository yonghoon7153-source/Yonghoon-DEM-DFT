"""Synthetic RT technical/reset/inventory consumer tests, no engine."""
import copy,hashlib,importlib.util,json,os,sys,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'p1_rt_numeric_preparation_20261117'))
from test_rt_numeric import row,write,grid_rows

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
M=load('rt_contract',os.environ.get('RT_CONTRACT_SOURCE',str(HERE/'rt_contract.py')))
RESETS=(('history_zwall_bot','property/atom',('global','per-atom')),('top_mesh','mesh/surface/stress',('global',)),
 ('n_neighs_mesh_top_mesh','property/atom',('global','per-atom')),('tracker_top_mesh','contacthistory/mesh',('global','per-atom')),
 ('contacthistory','contacthistory',('global','per-atom')))
BASE={'syntax':{'ok':True},'reset_log':{'ok':True},'g0':{'ok':True},
      **{k:{'status':'PASS'} for k in ('G1','G2','mesh_md5','G3')},
      'G2c':{'status':'FAIL'},'pre_post':{'equal':True},'un_erasure':{'seen':True},'history_test':{'pass':True}}
def put(p,s):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def atom(p,n=800,step=2000):
    cols=['id','type','x','y','z','vx','vy','vz','omegax','omegay','omegaz','radius']+[f'f_history_zwall_bot[{i}]' for i in range(1,5)]
    lines=['ITEM: TIMESTEP',str(step),'ITEM: NUMBER OF ATOMS',str(n),'ITEM: BOX BOUNDS pp pp ff','0 .05','0 .05','-.01 .1','ITEM: ATOMS '+' '.join(cols)]
    lines+=[' '.join(map(str,[i+1,1,.01,.01,.01,0,0,0,0,0,0,.001,0,0,0,0])) for i in range(n)]
    put(p,'\n'.join(lines)+'\n')
def screen(kind,bed='ps_3_7_r45',step=2000):
    r='LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n'
    r+=''.join(f'Resetting {k} state of Fix {f} Style {s} from restart file info\n' for f,s,ks in RESETS for k in ks)
    r+='Loop time of 0.01 on 6 procs for 0 steps\n'
    if kind.startswith('RT'):r+=f'UL_RT_DONE bed={bed} step={step}\n'
    elif kind=='R':r+='UL_R_DONE\n'
    elif kind=='UNread':r+='UL_UN_DONE\n'
    return r
def job_fixture(root,bed='ps_3_7_r45'):
    j=root/'current';j.mkdir();rows=grid_rows()
    records=['job_dir='+j.as_posix()]
    for stage,kind in [('R','R'),('UN','UNread'),('RT1','RT1'),('RT2','RT2')]+([('Ut0','Ut0')] if bed=='ps_7_3_r45' else []):
        put(j/stage/'screen.txt',screen(kind,bed));put(j/stage/'run_check.txt',f'{kind} screen.txt PASS rc=0 procs=6\n')
        records.append(f'stage={kind} screen=screen.txt rc=0 check=PASS')
    for s in ('RT1','RT2'):
        (j/s/'post').mkdir();write(j/s/'post/rt_pair_2000.dump',rows);atom(j/s/'post/rt_atom_2000.dump')
    (j/'R/g2').mkdir();write(j/'R/g2/contact_2000.liggghts',rows,26)
    orig=root/'original.dump';write(orig,rows,26)
    (j/'RT1/rt.bin').write_bytes(b'synthetic checkpoint');h=hashlib.sha256(b'synthetic checkpoint').hexdigest()
    ck=(j/'RT1/rt.bin').as_posix()
    records += [f'rt1_bin={ck} sha256={h}',f'rt2_ckpt={ck} sha256={h}']
    put(j/'RT2/log_screen.liggghts','read_restart '+ck+'\n')
    put(j/'run_manifest.txt','\n'.join(records)+'\n')
    return j,orig,rows
class Contract(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=os.environ.get('RT_TEST_TMPDIR'));self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.job,self.orig,self.rows=job_fixture(self.root);self.base=copy.deepcopy(BASE)
    def call(self,name,*a,**kw):
        self.assertTrue(callable(getattr(M,name,None)),name+' missing');return getattr(M,name)(*a,**kw)
    def evaluate(self,status='RESTORED',**kw):
        args=dict(bed='ps_3_7_r45',step=2000,atoms=800,reference_contact=self.orig,
                  grid_text='2 by 2 by 1 MPI processor grid\non 4 procs',grid=(2,2,1),written_np=4,legacy_checks=self.base)
        args.update(kw);r=self.call('evaluate',self.job,**args);self.assertEqual(r['status'],status,r);return r
    def test_normal_legacy_continuity_mismatch_is_report_only(self):
        r=self.evaluate();self.assertEqual(r['restore_rule'],'rev5_g2cp');self.assertFalse(r['operational_qualification'])
        self.assertEqual(r['checks']['G2c_cont']['status'],'FAIL')
        self.assertFalse((self.job/'restore_verdict.json').exists())
    def test_all_stage_failures_and_missing_records(self):
        for stage in ('R','UN','RT1','RT2'):
            p=self.job/stage/'run_check.txt';good=p.read_bytes()
            for text in ('','RT1 screen.txt FAIL rc=1\n'):
                put(p,text);self.evaluate('SYNTAX_FAIL')
            p.write_bytes(good)
    def test_manifest_stage_duplicate_failure_and_missing(self):
        p=self.job/'run_manifest.txt';good=p.read_text()
        for line in ('stage=RT1 screen=screen.txt rc=0 check=PASS\n','stage=RT1 skipped\n'):
            put(p,good+line);self.evaluate('SYNTAX_FAIL')
        put(p,good.replace('stage=RT2 screen=screen.txt rc=0 check=PASS\n',''));self.evaluate('SYNTAX_FAIL')
    def test_screen_banner_np_error_abort_and_exact_marker(self):
        p=self.job/'RT1/screen.txt';good=p.read_text()
        bad=[good.replace('3d5c00f','bad'),good.replace('on 6','on 4'),good+'ERROR broken\n',good+'UL_ABORT reason=x\n',
             good+'MPI_ABORT\n',good+'Segmentation fault\n',good.replace('step=2000','step=2001'),
             good+'UL_RT_DONE bed=ps_3_7_r45 step=2000\n']
        for text in bad:
            put(p,text);self.evaluate('SYNTAX_FAIL')
    def test_each_reset_of_each_stage(self):
        for stage in ('R','RT1','RT2'):
            p=self.job/stage/'screen.txt';good=p.read_text()
            for line in [x for x in good.splitlines() if x.startswith('Resetting')]:
                put(p,good.replace(line+'\n',''));self.evaluate('VALUE_MISMATCH')
            put(p,good)
    def test_numeric_failure_beats_missing_post_other_stage(self):
        (self.job/'RT1/post/rt_atom_2000.dump').unlink()
        self.base['G2']['status']='FAIL';self.evaluate('VALUE_MISMATCH')
    def test_post_each_prefix_extra_and_missing(self):
        for stage in ('RT1','RT2'):
            for kind in ('pair','atom'):
                p=self.job/stage/'post'/f'rt_{kind}_2000.dump';raw=p.read_bytes();p.unlink();self.evaluate('UNCONFIRMED');p.write_bytes(raw)
                extra=p.with_name(f'rt_{kind}_2001.dump');extra.write_bytes(raw);self.evaluate('UNCONFIRMED');extra.unlink()
    def test_obs_does_not_pollute_post_inventory(self):
        put(self.job/'RT1/obs/rt_wall_2000.dump','report only');self.evaluate()
    def test_binding_failure_beats_missing_numeric(self):
        (self.job/'RT1/post/rt_pair_2000.dump').unlink()
        p=self.job/'run_manifest.txt';put(p,p.read_text()+'job_dir='+self.job.as_posix()+'\n');self.evaluate('SYNTAX_FAIL')
    def test_missing_checkpoint_reread_preserves_old_cert_and_receipt(self):
        put(self.job/'restore_verdict.json','old certificate');put(self.job/'receipt.txt','old receipt')
        (self.job/'RT1/rt.bin').unlink();before={p:p.read_bytes() for p in self.job.rglob('*') if p.is_file()}
        self.evaluate('UNCONFIRMED');self.assertEqual(before,{p:p.read_bytes() for p in self.job.rglob('*') if p.is_file()})
    def test_reset_and_g0_and_prepost_keep_failure_priority(self):
        for key,field in [('g0','ok'),('pre_post','equal')]:
            self.base=copy.deepcopy(BASE);self.base[key][field]=False;self.base['G1']['status']='NOT_COMPUTED'
            self.evaluate('VALUE_MISMATCH')
    def test_missing_history_and_erasure_never_restore(self):
        for key,field in [('history_test','pass'),('un_erasure','seen')]:
            for value in (None,False,'True',1):
                self.base=copy.deepcopy(BASE);self.base[key][field]=value;self.evaluate('UNCONFIRMED')
    def test_missing_legacy_component_not_pass(self):
        for key in BASE:
            if key in ('G2c','reset_log'):continue
            self.base=copy.deepcopy(BASE);del self.base[key]
            self.evaluate('SYNTAX_FAIL' if key=='syntax' else 'VALUE_MISMATCH' if key=='g0' else 'UNCONFIRMED')
    def test_continuity_wide_reset_even_perfect_roundtrip_fails(self):
        z=copy.deepcopy(self.rows)
        for v in z:v[15]=0
        for stage in ('RT1','RT2'):write(self.job/stage/'post/rt_pair_2000.dump',z)
        self.evaluate('VALUE_MISMATCH')
    def test_r_and_rt1_continuity_both_required(self):
        z=copy.deepcopy(self.rows)
        for v in z:v[15]=0
        write(self.job/'R/g2/contact_2000.liggghts',z,26);self.evaluate('VALUE_MISMATCH')
    def test_atom_report_changes_do_not_replace_pair_gate(self):
        p=self.job/'RT2/post/rt_atom_2000.dump';put(p,p.read_text().replace('1 1 0.01','1 1 0.02',1))
        r=self.evaluate();self.assertFalse(r['checks']['rt_atoms']['base12_bits_equal'])
    def test_seven_three_requires_Ut0_only_RJ(self):
        self.evaluate('SYNTAX_FAIL',bed='ps_7_3_r45')
    def test_written_source_selection_no_concatenation_or_fallback(self):
        bed='ps_10_0_r45';root=self.root/'sources'
        for stage in ('EXT','EXT2'):put(root/bed/stage/'screen.txt',stage)
        p=self.call('select_source',root,bed,'RJ2',3650000,{'s0p':3650000,'s0pp':3700000},'orig.log')
        self.assertEqual(p['log'],root/bed/'EXT/screen.txt')
        p=self.call('select_source',root,bed,'RJ2',3700000,{'s0p':3650000,'s0pp':3700000},'orig.log')
        self.assertEqual(p['log'],root/bed/'EXT2/screen.txt')
        with self.assertRaises(ValueError):self.call('select_source',root,bed,'RJ2',3660000,{'s0p':3650000,'s0pp':3700000},'orig.log')
    def test_technical_or_binding_failure_skips_RT_value_readers(self):
        p=self.job/'run_manifest.txt';put(p,p.read_text()+'job_dir='+self.job.as_posix()+'\n')
        with patch.object(M.N,'g2cp_compare',side_effect=AssertionError('RT numeric must not run')),patch.object(M.N,'cont_guard',side_effect=AssertionError('RT continuity must not run')),patch.object(M,'atom_report',side_effect=AssertionError('RT atom values must not run')):
            self.evaluate('SYNTAX_FAIL')
    def test_roundtrip_uncomputed_for_incomplete_binding_or_inventory(self):
        (self.job/'RT1/rt.bin').unlink()
        self.assertEqual(self.evaluate('UNCONFIRMED')['checks']['G2cp']['status'],'NOT_COMPUTED')

if __name__=='__main__':unittest.main(verbosity=2)
