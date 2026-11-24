"""One/two-carrier tests on the pinned material floor and its actual transfer stencil."""
import argparse
import importlib.util
from pathlib import Path
import unittest

import numpy as np


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def old_boundary(module, x, ids, pos, groups, pitch):
    owners = []
    for p, g in zip(pos, groups):
        idx = np.flatnonzero(ids==g)
        owners.append(idx[np.argmin(np.sum((x[idx]-p)**2,axis=1))])
    return module.MaterialBoundary(owners, pos, groups)


class CarrierTests(unittest.TestCase):
    def geometry(self, reverse=False, one=False, floor_gap=0.):
        # Exactly representable half-pitch offsets make this a genuine geometric tie.
        self.grid, self.dt, self.plane = 64, .001, .375
        pitch = .5/self.grid
        self.mark_x = .5 + .375/self.grid
        x = np.array([[self.mark_x-pitch/2,self.plane+floor_gap],[self.mark_x+pitch/2,self.plane+floor_gap]])
        if reverse:
            x = x[::-1]
        if one:
            x = x[:1]
        ids = np.zeros(len(x),dtype=int)
        pos = np.array([[self.mark_x,self.plane+floor_gap]])
        b = self.factory(floor,x,ids,pos,np.zeros(1,dtype=int),pitch)
        nodes, weights, _, offset = material.stencil(x,self.grid)
        key, inv = np.unique(nodes.ravel(),return_inverse=True)
        slots = inv.reshape(weights.shape)
        mass = np.bincount(slots.ravel(),weights=weights.ravel()) / len(x)
        coord = np.stack(np.divmod(key,self.grid+1),axis=1)/self.grid
        wall = b.bind(x,weights,offset,slots,self.grid,self.plane,self.dt)
        return b, wall, mass, coord

    def sample(self, reverse=False, one=False):
        b,wall,m,xy = self.geometry(reverse,one)
        gv = np.zeros_like(xy)
        # Positive/negative x grid nodes carry an antisymmetric speed perturbation.
        gv[:,1] = -1. + .2*((xy[:,0]-self.mark_x)*self.grid)**3
        before = gv.copy()
        speed = float(np.einsum("sq,sq->s",wall.coefficients,gv[wall.slots,1])[0])
        J = wall.project(m,gv)
        self.assertGreater(J,0)
        self.assertAlmostEqual(m@(gv[:,1]-before[:,1]),J,places=12)
        np.testing.assert_array_equal(gv[:,0],before[:,0])
        wall.transport(gv)
        self.assertGreaterEqual(float(b.positions[0,1]),self.plane-2e-15)
        return speed,J

    def test_equal_distance_surface_velocity_and_pressure_are_permutation_invariant(self):
        a=self.sample()
        b=self.sample(reverse=True)
        np.testing.assert_allclose(a,b,rtol=2e-14,atol=2e-14)

    def test_rigid_affine_reproduction_and_transport(self):
        b,wall,m,xy=self.geometry()
        L=np.array([[.05,.13],[-.11,.07]])
        t=np.array([.01,.2])
        gv=xy@L.T+t
        p=b.positions.copy()
        self.assertEqual(wall.project(m,gv),0.)
        wall.transport(gv)
        np.testing.assert_allclose(b.positions,p+self.dt*(p@L.T+t),atol=1e-15,rtol=0)

    def test_open_gap_has_no_reaction(self):
        _,wall,m,xy=self.geometry(floor_gap=.003)
        gv=np.column_stack((np.zeros(len(m)),np.full(len(m),-1.)))
        self.assertEqual(wall.project(m,gv),0.)

    def test_single_carrier_matches_original(self):
        result=self.sample(one=True)
        original=self.factory
        self.factory=old_boundary
        try:
            expected=self.sample(one=True)
        finally:
            self.factory=original
        np.testing.assert_allclose(result,expected,atol=1e-14,rtol=1e-14)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("material_floor",type=Path)
    parser.add_argument("material",type=Path)
    parser.add_argument("--candidate",type=Path,default=None)
    args=parser.parse_args()
    floor,material=load(args.material_floor),load(args.material)
    CarrierTests.factory=staticmethod(load(args.candidate).build_boundary if args.candidate else old_boundary)
    unittest.main(argv=["test_carrier_correction"],verbosity=2)
