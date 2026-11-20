"""Manufactured, one-step contact through the actual point-to-grid transfers."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import suyoung_u6_first_dev as u


class ContactDirection(unittest.TestCase):
    def check_node(self, sparse, approach, axis, reverse):
        grid = 32
        mid = (grid // 2) * (grid + 1) + grid // 2
        x = np.full((2, 2), .5)
        x[:, axis] += [-.01, .01]
        ids = np.array([1,0] if reverse else [0,1])
        v = np.zeros((2, 2))
        v[:,axis] = [.02,-.02] if approach else [-.02,.02]
        before = v[:,axis].copy()
        affine = np.zeros((2,2,2))
        elastic = np.repeat(np.eye(2)[None], 2, axis=0)
        observed = []
        if sparse:
            original = u.project_contacts

            def observe(fields, nodes, mass, grad, velocity, centers, friction):
                result = original(fields, nodes, mass, grad, velocity, centers, friction)
                take = np.flatnonzero(nodes == mid)
                by_id = velocity[take[np.argsort(fields[take])],axis]
                observed.extend(by_id[ids])
                return result

            with patch.object(u, 'project_contacts', observe):
                u.advance(x,v,affine,elastic,ids,np.full(2,(.5/grid)**2),grid,.0001,.85)
        else:
            original = u.model.contact

            def observe(mass, velocity, grad, centers, friction):
                result = original(mass, velocity, grad, centers, friction)
                observed.extend(velocity[ids,mid,axis])
                return result

            state = dict(x=x, v=v, C=affine, F=elastic, ids=ids)
            with patch.object(u.model, 'contact', observe):
                u.model.step(state,'F',grid,.0001,.85,0.,.5)
        np.testing.assert_allclose(observed, np.zeros(2) if approach else before, atol=1e-13)

    def test_dense_approach(self):
        self.check_node(False,True,0,False)

    def test_dense_separation(self):
        self.check_node(False,False,1,True)

    def test_sparse_approach(self):
        self.check_node(True,True,1,True)

    def test_sparse_separation(self):
        self.check_node(True,False,0,False)

    def test_old_protocol_does_not_mix(self):
        old = dict(status='TARGET_BRACKETED',cells=12,phi_m=.8,protocol='development-mode-1')
        fresh = dict(old,cells=16,protocol=u.PROTOCOL)
        self.assertEqual(u.assess(old,fresh), 'INCOMPLETE')


if __name__ == '__main__':
    unittest.main()
