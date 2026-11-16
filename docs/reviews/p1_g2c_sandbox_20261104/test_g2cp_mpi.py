"""Small fake-runner tests; no engine, scheduler, network or scientific input."""
import argparse
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
BASH = 'bash'

def posix(path):
    s = str(Path(path).resolve()).replace('\\', '/')
    return '/' + s[0].lower() + s[2:] if len(s)>1 and s[1]==':' else s

def load_module():
    p = ROOT/'g2cp_mpi.py'
    assert p.is_file(), 'MPI support absent'
    s = importlib.util.spec_from_file_location('g2cp_mpi', p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m

FAKE_LMP = '''#!/bin/bash
for x in "$@"; do
  if [ "$x" = -h ]; then printf 'LIGGGHTS (fake)\\nCommand line options:\\n'; exit 1; fi
done
declare -A v
while [ "$#" -gt 0 ]; do
  case "$1" in
    -var) v["$2"]="$3"; shift 3;;
    -log) log="$2"; shift 2;;
    -in) deck="$2"; shift 2;;
    *) exit 91;;
  esac
done
printf '%s|%s|%s|%s\\n' "$deck" "${v[PX]:-1}" "${v[PY]:-1}" "${FAKE_NP:-1}" >> "$FAKE_CALLS"
n=${v[N]:-200}; nm=$((n-1))
if [ -n "${v[POST]:-}" ]; then
  for f in c_$n.txt cpre_$nm.txt atom_$n.txt; do printf 'synthetic\\n' > "${v[POST]}/$f"; done
fi
if [ -n "${v[RST]:-}" ]; then
  for f in restart_$n.bin restart_cmd.bin restart_rt.bin; do printf 'synthetic\\n' > "${v[RST]}/$f"; done
fi
printf '  %s by %s by 1 MPI processor grid\\nLoop time of 0.01 on %s procs for 200 steps with 1220 atoms\\n' "${v[PX]:-1}" "${v[PY]:-1}" "${FAKE_LOG_NP:-${FAKE_NP:-1}}" > "$log"
'''
FAKE_MPI = '''#!/bin/bash
if [ "$1" = --version ]; then printf 'fake MPI 1\\n'; exit 0; fi
[ "$1 $2 $3 $4" = '--oversubscribe --bind-to none -np' ] || exit 92
export FAKE_NP="$5"
shift 5
exec "$@"
'''

class MPITests(unittest.TestCase):
    def setup_run(self, td, np='2', n='200', log_np=None):
        base=Path(td); src=base/'sandbox';src.mkdir()
        for p in ROOT.iterdir():
            if p.is_file(): shutil.copyfile(p,src/p.name)
        (src/'run_40000').mkdir()
        shutil.copyfile(ROOT/'run_40000/inputs.md5',src/'run_40000/inputs.md5')
        home=base/'fake_home';home.mkdir();out=base/'new_output'
        for name,data in [('lmp',FAKE_LMP),('mpirun',FAKE_MPI)]:
            p=base/name;p.write_text(data,encoding='utf-8',newline='\n');p.chmod(0o755)
        (base/'PROVENANCE.txt').write_text('pin '+'a'*40+'\n',encoding='ascii',newline='\n')
        env={k:v for k,v in os.environ.items() if not k.startswith(('G2CP_', 'SLURM_', 'FAKE_'))}
        env.update(HOME=posix(home),LMP=posix(base/'lmp'),G2CP_MPIRUN=posix(base/'mpirun'),
                   SLURM_JOB_ID='90001',SLURM_NTASKS=np,SLURM_SUBMIT_DIR=posix(base),
                   FAKE_CALLS=posix(base/'calls.txt'),G2CP_TLONG='10',G2CP_TSHORT='10')
        if np!='serial':env['G2CP_NP']=np
        if log_np is not None:env['FAKE_LOG_NP']=log_np
        cmd=[BASH,'--noprofile','--norc',posix(src/'run_g2cp.sh'),n,posix(out)]
        return base,src,out,env,cmd

    def test_01_np2_np4_nine_calls(self):
        for np,py in [('2','1'),('4','2')]:
            with self.subTest(np=np),tempfile.TemporaryDirectory() as td:
                base,src,out,env,cmd=self.setup_run(td,np)
                p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=60)
                self.assertEqual(p.returncode,0,p.stderr[-500:])
                calls=(base/'calls.txt').read_text().splitlines()
                self.assertEqual(calls,[f'{deck}|2|{py}|{np}' for deck in ['MPA.liggghts','MPA2.liggghts','MPR.liggghts','MPR.liggghts','MPR.liggghts','MPBW.liggghts','MPR.liggghts','MPBW.liggghts','MPR.liggghts']])
                identity=(out/'lmp_identity.txt').read_text()
                self.assertEqual(identity.count('\nnp '+np+'\n'),1)
                ledger=(base/'fake_home/g2cp_mpi_ledger.txt').read_text()
                self.assertEqual(ledger.count('kind=attempt '),1)
                self.assertIn('provenance='+'a'*40,ledger)

    def test_02_preflight_no_run(self):
        for np,n,change in [('3','200',None),('','200',None),('2','39900',None),('2','200','nojob'),('2','200','ntasks'),('2','200','provenance'),('2','200','override')]:
            with self.subTest(case=(np,n,change)),tempfile.TemporaryDirectory() as td:
                base,src,out,env,cmd=self.setup_run(td,np,n)
                if change=='nojob':env.pop('SLURM_JOB_ID')
                if change=='ntasks':env['SLURM_NTASKS']='4'
                if change=='provenance':(base/'PROVENANCE.txt').write_text('pin invalid\n')
                if change=='override':env['G2CP_LEDGER']=posix(base/'other')
                p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=60)
                self.assertEqual(p.returncode,3,p.stderr[-500:])
                self.assertFalse(out.exists());self.assertFalse((base/'calls.txt').exists())
                self.assertIn('G2CP_PRESTOP rc=3 reason=',p.stderr)

    def test_03_wrong_runtime_procs_stops(self):
        with tempfile.TemporaryDirectory() as td:
            base,src,out,env,cmd=self.setup_run(td,'2',log_np='1')
            p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,4,p.stderr[-500:]);self.assertTrue((out/'STOP.txt').is_file())
            self.assertEqual(len((base/'calls.txt').read_text().splitlines()),1)

    def test_04_serial_calls_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            base,src,out,env,cmd=self.setup_run(td,'serial')
            p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,0,p.stderr[-500:])
            self.assertEqual((base/'calls.txt').read_text().splitlines(),[f'{deck}|1|1|1' for deck in ['A.liggghts','A2.liggghts','R.liggghts','R.liggghts','R.liggghts','BW.liggghts','R.liggghts','BW.liggghts','R.liggghts']])
            self.assertNotIn('\nnp ',(out/'lmp_identity.txt').read_text())
            self.assertFalse((base/'fake_home/g2cp_mpi_ledger.txt').exists())

    def test_05_log_boundary(self):
        m=load_module()
        good='  2 by 1 by 1 MPI processor grid\nLoop time of 1 on 2 procs for 200 steps with 1220 atoms\n'
        self.assertEqual(m.check_log(good,2),[])
        for bad in (good.replace('on 2','on 1'),good+good,good.replace('2 by 1','1 by 2'),good.split('\n',1)[1],good+'ERROR on proc 1: fail\n'):
            self.assertTrue(m.check_log(bad,2))

    def test_06_identity_missing_and_duplicate(self):
        m=load_module();logs={a:'2 by 1 by 1 MPI processor grid\nLoop time of 1 on 2 procs for 200 steps\n' for a in m.ARMS}
        self.assertTrue(m.check_identity('np 2\nprocs_grid 2 1 1\n',logs)['ok'])
        for text in ('','np 2\n','np 1\nprocs_grid 1 1 1\n','np 2\nnp 2\nprocs_grid 2 1 1\n'):
            self.assertFalse(m.check_identity(text,logs)['ok'])

    def test_07_owner_boundary(self):
        m=load_module();box=((0.,1.),(0.,1.),(0.,1.))
        self.assertEqual(m.owner((.2,.3,.4),box,4),(0,0))
        self.assertEqual(m.owner((.8,.8,.4),box,4),(1,1))
        self.assertIsNone(m.owner((.5,.3,.4),box,4))
        self.assertIsNone(m.owner((.5+5e-13,.3,.4),box,4))
        with self.assertRaises(ValueError):m.owner((2.,.3,.4),box,4)

    def test_08_comparator_rejects_missing_np(self):
        s=importlib.util.spec_from_file_location('comparison',ROOT/'compare_g2cp.py')
        c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
        self.assertTrue(hasattr(c,'parallel_gate'),'comparator has no MPI gate')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for arm in c.ARMS:
                (root/arm).mkdir()
                (root/arm/'log.txt').write_text('2 by 1 by 1 MPI processor grid\nLoop time of 1 on 2 procs for 200 steps\n')
            (root/'lmp_identity.txt').write_text('np 2\nprocs_grid 2 1 1\n')
            self.assertTrue(c.parallel_gate(str(root))['ok'])
            (root/'lmp_identity.txt').write_text('procs_grid 2 1 1\n')
            self.assertFalse(c.parallel_gate(str(root))['ok'])

    def test_09_rank_prediction_and_negative_controls(self):
        m=load_module()
        s=importlib.util.spec_from_file_location('comparison',ROOT/'compare_g2cp.py')
        c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
        atoms={'ok':True,'box':((0.,1.),(0.,1.),(0.,1.)),'by_id':{}}
        C={'ok':True,'by_key':{}}; A={'ok':True,'by_key':{}}
        for a,b,x,y,flag,delta in [(1,2,.1,.2,0,0),(3,4,.4,.6,0,1),(5,6,.8,.1,1,1),(7,8,.5,.7,0,0)]:
            atoms['by_id'][a]=(1,[x,.2,.2]);atoms['by_id'][b]=(1,[y,.2,.2])
            v=[0.]*30;v[8]=flag
            C['by_key'][a,b]={'v':v.copy(),'flipped':False}
            v[9]=delta;A['by_key'][a,b]={'v':v,'flipped':False}
        names=[g for g,_ in c._groups(c.LAYOUT[30])]
        check=lambda:m.pred_ma3p(C,A,atoms,2,c._cmp_groups,names)
        good=check();self.assertEqual(good['status'],'맞음');self.assertEqual(good['counts'],{'same':1,'rank_boundary':1,'periodic':1,'ambiguous':1})
        for key,col,value in [((3,4),9,1),((1,2),9,1),((7,8),25,1)]:
            with self.subTest(key=key,col=col):
                old=C['by_key'][key]['v'][col];C['by_key'][key]['v'][col]=value
                self.assertEqual(check()['status'],'틀림')
                C['by_key'][key]['v'][col]=old

    def test_10_mpi_full_comparator_roundtrip(self):
        self.assertTrue((ROOT/'g2cp_mpi.py').is_file(),'MPI support absent')
        s=importlib.util.spec_from_file_location('fixture',ROOT/'test_g2cp.py')
        fixture=importlib.util.module_from_spec(s);s.loader.exec_module(fixture)
        c=fixture.load_cmp()
        for np,py in [(2,1),(4,2)]:
            with self.subTest(np=np),tempfile.TemporaryDirectory() as td:
                root=Path(td)/'out';fixture.write_fixture(str(root))
                with (root/'lmp_identity.txt').open('a',encoding='utf-8',newline='\n') as f:f.write(f'np {np}\nprocs_grid 2 {py} 1\n')
                with (root/'inputs.md5').open('a',encoding='utf-8',newline='\n') as f:
                    for name in ('MPA.liggghts','MPA2.liggghts','MPR.liggghts','MPBW.liggghts','g2cp_mpi.py'):
                        f.write(hashlib.md5((ROOT/name).read_bytes()).hexdigest()+'  '+name+'\n')
                for arm in c.ARMS:
                    (root/arm/'log.txt').write_text(f'2 by {py} by 1 MPI processor grid\nLoop time of 1 on {np} procs for 40000 steps\n',encoding='utf-8',newline='\n')
                result,rc=c.compare_all(str(root),40000)
                self.assertEqual(rc,0,result.get('mpi_gate'))
                self.assertTrue(result['mpi_gate']['ok']);self.assertTrue(result['deck_gate']['ok'])
                self.assertEqual([result['judgment'][k]['status'] for k in ('다','라')],['PASS','PASS'])
                self.assertEqual(result['predictions']['가']['status'],'해당 없음')
                self.assertIn('마-3p',result['predictions']);self.assertIsNotNone(result['mpi']['n_rb'])
                (root/'lmp_identity.txt').write_text('procs_grid 2 '+str(py)+' 1\n',encoding='utf-8',newline='\n')
                result,rc=c.compare_all(str(root),40000)
                self.assertEqual(rc,2)
                self.assertEqual([result['judgment'][k]['status'] for k in ('다','라')],['NOT_COMPUTED','NOT_COMPUTED'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bash',default='bash');p.add_argument('--report',type=Path)
    a=p.parse_args();BASH=a.bash
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MPITests))
    if a.report:a.report.write_text(json.dumps({'methods':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'real_engine':False,'real_mpi':False},indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if r.wasSuccessful() else 1)
