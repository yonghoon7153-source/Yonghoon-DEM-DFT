"""Synthetic local kernel checks only; not a production S/F run."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np
spec=importlib.util.spec_from_file_location('sf',Path(__file__).with_name('dem_suyoung_sf2d_dev.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class Kernels(unittest.TestCase):
    def test_partition_and_gradient(self):
        x=np.array([[.23,.31],[.5,.5],[.72,.66]])
        _,w,g,_=m.stencil(x,32)
        np.testing.assert_allclose(w.sum(axis=1),1,atol=1e-14)
        np.testing.assert_allclose(g.sum(axis=1),0,atol=1e-13)

    def test_pair_conserves_momentum_and_loses_energy(self):
        ma=np.array([2.]);mb=np.array([1.]);va=np.array([[1.,.5]]);vb=np.array([[-1.,0.]])
        a,b,jn,jt=m.pair_impulse(ma,mb,va,vb,np.array([[1.,0.]]),.2)
        np.testing.assert_allclose(ma[:,None]*a+mb[:,None]*b,ma[:,None]*va+mb[:,None]*vb)
        self.assertLessEqual(float((ma[:,None]*a*a+mb[:,None]*b*b).sum()),float((ma[:,None]*va*va+mb[:,None]*vb*vb).sum()))
        self.assertLessEqual(float(jt[0]),.2*float(jn[0])+1e-14)
        self.assertAlmostEqual(float(a[0,0]-b[0,0]),0)

    def test_separating_pair_has_no_impulse(self):
        va=np.array([[-1.,1.]]);vb=np.array([[1.,0.]])
        a,b,jn,jt=m.pair_impulse(np.ones(1),np.ones(1),va,vb,np.array([[1.,0.]]),.2)
        np.testing.assert_array_equal(a,va);np.testing.assert_array_equal(b,vb)
        self.assertEqual(float(jn[0]+jt[0]),0)

    def test_receding_plate_does_not_pull(self):
        mass=np.ones((1,1));v=np.array([[[0.,-.3]]]);x=np.array([[.5,.9]])
        impulse=m.boundary(mass,v,x,.8,-.1)
        self.assertEqual(impulse,0);self.assertEqual(v[0,0,1],-.3)

    def test_identity_stress_and_volume_preserving_plastic_projection(self):
        np.testing.assert_array_equal(m.stress(np.eye(2)[None,:,:]),np.zeros((1,2,2)))
        F=np.array([[[2.,0],[0,.5]]]);p=m.plastic_project(F)
        self.assertAlmostEqual(float(np.linalg.det(p)[0]),1,places=13)
        self.assertLess(float(np.linalg.norm(np.log(np.linalg.svd(p)[1]))),float(np.linalg.norm(np.log(np.linalg.svd(F)[1]))))

    def test_one_field_S_F_same_kernel(self):
        a=m.initial_state(16);a['ids'][:]=0
        b={k:v.copy() for k,v in a.items()}
        sa=m.step(a,'S',16,.0001,.79,-.1,.2)
        sb=m.step(b,'F',16,.0001,.79,-.1,.2)
        for k in a:np.testing.assert_array_equal(a[k],b[k])
        self.assertEqual(sa,sb)

    def test_seed_ids_and_mass_preserved_for_both_arms(self):
        for arm in ('S','F'):
            state=m.initial_state(16);ids=state['ids'].copy()
            r=m.step(state,arm,16,.0001,.79,-.1,.2)
            np.testing.assert_array_equal(state['ids'],ids)
            self.assertAlmostEqual(r['mass'],len(ids)*(.5/16)**2,places=13)
            self.assertEqual(r['fields'],1 if arm=='S' else 4)

    def test_zero_denominator_ratio_is_missing(self):
        self.assertIsNone(m.ratio(1,0));self.assertIsNone(m.ratio(0,0));self.assertEqual(m.ratio(2,1),2)

    def test_tiny_cli_writes_both_arms_without_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'result'
            cmd=[sys.executable,'-I','-X','utf8','-B',str(Path(m.__file__)),
                 '--output',str(out),'--grid','16','--steps','4','--dt','0.0001']
            run=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
            self.assertEqual(run.returncode,0,run.stderr)
            result=json.loads((out/'SUMMARY.json').read_bytes())
            self.assertEqual(result['status'],'DEVELOPMENT_COMPLETE')
            self.assertEqual({k:v['steps_completed'] for k,v in result['arms'].items()},{'S':4,'F':4})
            self.assertFalse(result['registered_conclusions_adoptable'])
            original=(out/'SUMMARY.json').read_bytes()
            retry=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
            self.assertNotEqual(retry.returncode,0)
            self.assertEqual((out/'SUMMARY.json').read_bytes(),original)


if __name__=='__main__':unittest.main(verbosity=2)
