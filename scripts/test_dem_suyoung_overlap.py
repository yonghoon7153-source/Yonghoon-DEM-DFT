import importlib.util,sys,unittest
from pathlib import Path
import numpy as np
spec=importlib.util.spec_from_file_location('overlap',Path(__file__).with_name('dem_suyoung_overlap.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sample(centers,ids,h=1.):
    n=len(ids);return dict(x=np.asarray(centers,dtype=float),particle_id=np.asarray(ids,dtype=np.int64),point_id=np.arange(n,dtype=np.int64),F_total=np.tile(np.eye(2),(n,1,1)),reference_area=np.full(n,h*h))
def refined(n):
    a=(np.arange(n)+.5)/n-.5;xx,yy=np.meshgrid(a,a);p=np.column_stack([xx.ravel(),yy.ravel()])
    return sample(np.vstack([p,p+[.3,0]]),[0]*(n*n)+[1]*(n*n),1/n)
class Overlap(unittest.TestCase):
    def test_01_disjoint_and_edge_touch(self):
        for dx in (1.,2.):self.assertAlmostEqual(m.measure_frame(sample([[0,0],[dx,0]],[0,1]))['cell_overlap_area'],0.)
    def test_02_half_squares_and_center_quadrature_limit(self):
        r=m.measure_frame(sample([[0,0],[.5,0]],[0,1]));self.assertAlmostEqual(r['cell_overlap_area'],.5)
        self.assertEqual(r['point_overlap_area_estimate'],0.,'centers on the other edge are excluded; quadrature can miss a thin overlap')
    def test_03_triple_overlap_counted_once(self):
        r=m.measure_frame(sample([[0,0]]*3,[0,1,2]));self.assertAlmostEqual(r['cell_overlap_area'],1.);self.assertAlmostEqual(r['point_overlap_area_estimate'],1.)
    def test_04_same_particle_is_not_interparticle(self):
        r=m.measure_frame(sample([[0,0],[0,0]],[7,7]));self.assertEqual(r['cell_overlap_area'],0.);self.assertAlmostEqual(r['within_particle_excess_area'],1.)
    def test_05_center_refinement(self):
        r=m.measure_frame(refined(20));self.assertAlmostEqual(r['cell_overlap_area'],.7);self.assertAlmostEqual(r['point_overlap_area_estimate'],.7,places=8)
    def test_06_invalid_inputs(self):
        for key,value in [('F_total',np.zeros((2,2,2))),('x',np.array([[0.,0.],[float('nan'),0.]])),('point_id',np.array([0,0])),('reference_area',np.array([1.,-1.]))]:
            d=sample([[0,0],[0,0]],[0,1]);d[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):m.measure_frame(d)
    def test_07_stroke_only_contact(self):
        r=m.measure_frame(sample([[0,0],[1.0001,0]],[0,1]),stroke_width=.00025)
        self.assertEqual(r['cell_overlap_area'],0.);self.assertGreater(r['drawn_overlap_area'],0.)
    def test_08_scale_and_input_unchanged(self):
        d=sample([[0,0],[.5,0]],[0,1]);before={k:v.tobytes() for k,v in d.items()};r=m.measure_frame(d)
        self.assertEqual(before,{k:v.tobytes() for k,v in d.items()})
        e=sample([[0,0],[1.,0]],[0,1],2.);s=m.measure_frame(e)
        self.assertAlmostEqual(s['cell_overlap_area'],4*r['cell_overlap_area']);self.assertAlmostEqual(s['union_area'],6.)
if __name__=='__main__':unittest.main()
