"""Offline, synthetic MPM state/measurement and identity contracts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    import mpm_coverage_state as adapter
except ModuleNotFoundError as exc:
    if exc.name != "mpm_coverage_state":
        raise
    adapter = None


def fixture():
    # At N=16, origin=1 and span=15. The adjacent cell centers are 5.5/16 and 6.5/16.
    w = 0.96 - 0.04
    scale = w / 0.05
    am = np.array([[1, (5.5/16-.04)/scale, (5.5/16-.04)/scale, (4.5/16-.05)/scale, .02/scale]])
    se = am.copy()
    se[:,0] = 3
    se[:,1] = (6.5/16-.04)/scale
    centers = np.column_stack((.04+am[:,1]*scale,.04+am[:,2]*scale,.05+am[:,3]*scale))
    radii = am[:,4]*scale
    meta = dict(schema="mpm3d_state_v1", n_pts=9, n_grid=16, nz=18, n_am=1, periodic=True,
                FLOOR=.05, um_box_um=1000/scale, am_scaffold=True, se_dump=True,
                lateral_box=.05, dilate_z=1., am_radii_deformed=False)
    points = np.tile([6.5/16,5.5/16,4.5/16], (9,1)).astype(np.float32)
    points[-1] = [15.5/16,3.5/16,17.5/16]
    state = dict(meta_json=np.array(json.dumps(meta)), x=points, phase=np.array([1]*8+[2],np.int8),
                 am_pos=centers, am_r_pristine=radii.copy(), am_r_applied=radii.copy(),
                 se_id=np.zeros(9,dtype=np.int32))
    return state,am,se


class NativeCoverage(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(adapter, "missing state and custody adapter")
        self.state,self.am,self.se=fixture()

    def test_native_to_c0_without_deformation(self):
        am, seed, end, h = adapter.state_grids(self.state,self.am,self.se)
        self.assertEqual(am.shape,(15,15,18))
        self.assertEqual(h,1000/(.92/.05)/16)
        self.assertEqual(am[4,4,4],1)
        self.assertEqual(seed[5,4,4],8)
        np.testing.assert_array_equal(seed,end)
        from mpm_coverage_c0 import compare
        phases=compare(am,seed,end,h,[None,None])["phases"]
        self.assertEqual(phases["1"]["C_seed"],1/6)
        self.assertEqual(phases["1"]["plastic_increment"],0)
        self.assertIsNone(phases["2"]["C_end"])

    def test_periodic_xy_tall_z_and_phase_filter(self):
        self.state["x"][:4]=[.5/16,5.5/16,17.5/16]
        for non_se in (2,3,4,5,6):
            with self.subTest(non_se=non_se):
                self.state["phase"][-1]=non_se
                _,_,end,_=adapter.state_grids(self.state,self.am,self.se)
                self.assertEqual(end[-1,4,17],4)
                self.assertEqual(end[5,4,4],4)
                self.assertEqual(end.sum(),8)

    def test_am_overlap_preserves_writer_order_and_seam(self):
        state,am,se=fixture()
        am=np.repeat(am,2,axis=0)
        am[:,0]=[1,2]
        scale=(.96-.04)/.05
        am[:,1]=(.5/16-.04)/scale
        am[1,1]+=15/16/scale
        state["am_pos"]=np.column_stack((.04+am[:,1]*scale,.04+am[:,2]*scale,.05+am[:,3]*scale))
        state["am_r_pristine"]=state["am_r_applied"]=am[:,4]*scale
        meta=json.loads(str(state["meta_json"]))
        meta["n_am"]=2
        state["meta_json"]=np.array(json.dumps(meta))
        for first,last in ((1,2),(2,1)):
            am[:,0]=[first,last]
            grid,_,_,_=adapter.state_grids(state,am,se)
            self.assertEqual(grid[-1,4,4],last)

    def test_outside_z_and_nonfinite_rejected(self):
        for pos in ([.4,.3,-.01],[.4,.3,18/16],[np.nan,.3,.4]):
            with self.subTest(pos=pos):
                self.state["x"][0]=pos
                with self.assertRaises(ValueError):
                    adapter.state_grids(self.state,self.am,self.se)

    def test_shuffled_polydisperse_mask_matches_naive_sphere_writer(self):
        origin, shape = adapter.grid_shape(12, 14)
        ijk = np.moveaxis(np.indices(shape), 0, -1)
        centers = (ijk + [origin+.5, origin+.5, .5]) / 12
        rng = np.random.default_rng(705)
        rows = rng.uniform(0,1,size=(16,4))
        rows[:, 3] = np.linspace(.09,.53,16)
        phases = np.tile([2,1],8)
        period = shape[0] / 12
        for order in (np.arange(16),rng.permutation(16)):
            expected = np.zeros(shape,dtype=np.uint8)
            for i in order:
                delta = centers - rows[i,:3]
                delta[:,:,:,:2] -= np.rint(delta[:,:,:,:2] / period) * period
                hit = (delta**2).sum(axis=3) <= rows[i,3]**2
                expected[hit] = phases[i]
            np.testing.assert_array_equal(adapter.am_grid(rows[order],phases[order],12,origin,shape), expected)

    def test_reject_wrong_grid_scope_and_scene(self):
        for key,bad in (("periodic",False),("schema","other"),("n_pts",10),("am_radii_deformed",True),("um_box_um",1.0),("FLOOR",.02)):
            state,am,se=fixture()
            meta=json.loads(str(state["meta_json"]))
            meta[key]=bad
            state["meta_json"]=np.array(json.dumps(meta))
            with self.subTest(key=key), self.assertRaises(ValueError):
                adapter.state_grids(state,am,se)
        self.am[0,1]+=.0003
        with self.assertRaises(ValueError):
            adapter.state_grids(self.state,self.am,self.se)

    def test_reject_missing_or_misidentified_seed(self):
        with self.assertRaises(ValueError):  # SE scaffold geometry gives zero cells instead of one
            adapter.state_grids(self.state,self.am,self.am.copy())
        self.se[:,3]+=20
        with self.assertRaises(ValueError):
            adapter.state_grids(self.state,self.am,self.se)

    def test_cli_checks_original_bytes_and_native_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            state_path=d/"state.npz"
            np.savez(state_path,**self.state)
            am_path,se_path=d/"am.csv",d/"se.csv"
            np.savetxt(am_path,self.am,delimiter=",",fmt="%.18e")
            np.savetxt(se_path,self.se,delimiter=",",fmt="%.18e")
            files=[state_path,am_path,se_path]
            manifest=d/"receipt.json"
            manifest.write_text(json.dumps({k:hashlib.sha256(v.read_bytes()).hexdigest()
                                for k,v in zip(("state","am_scaffold","se_scaffold"),files)}))
            cmd=[sys.executable,"-I","-B",str(HERE/"mpm_coverage_state.py"),*map(str,files),str(manifest)]
            result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.assertEqual(result.returncode,0,result.stderr.decode())
            doc=json.loads(result.stdout)
            self.assertEqual(doc["coverage"]["phases"]["1"]["C_end"],1/6)
            self.assertEqual(doc["se_point_identity"],"UNESTABLISHED")
            se_path.write_bytes(se_path.read_bytes()+b"\n")
            result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(result.stdout,b"")

    def test_alternate_same_count_sources_do_not_establish_run_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            state, am, se = fixture()
            statefile, afile, sfile = d/"state.npz", d/"am.csv", d/"se.csv"
            np.savez(statefile, **state)
            source = d/"declared.json"
            shifted = se.copy()
            shifted[0,1] += 2/16 / ((.96-.04)/.05)
            relabelled = am.copy()
            relabelled[0,0] = 2
            for source_am, source_se, active, expected_seed in (
                    (am,se,"1",1/6), (am,shifted,"1",0.), (relabelled,se,"2",1/6)):
                with self.subTest(active=active, expected_seed=expected_seed):
                    np.savetxt(afile,source_am,delimiter=",",fmt="%.18e")
                    np.savetxt(sfile,source_se,delimiter=",",fmt="%.18e")
                    declared = {role:hashlib.sha256(p.read_bytes()).hexdigest() for role,p in
                                (("state",statefile),("am_scaffold",afile),("se_scaffold",sfile))}
                    source.write_text(json.dumps(declared))
                    run = subprocess.run([sys.executable,"-I","-B",str(HERE/"mpm_coverage_state.py"),
                                          str(statefile),str(afile),str(sfile),str(source)],
                                         stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    self.assertEqual(run.returncode,0,run.stderr.decode())
                    record = json.loads(run.stdout)
                    self.assertEqual(record["source_sha256"],declared)
                    self.assertEqual(record["coverage"]["phases"][active]["C_seed"],expected_seed)
                    self.assertEqual(record.get("execution_source_identity"),"NOT_ESTABLISHED")
                    self.assertEqual(record.get("coverage_source_scope"),
                                     "CONDITIONAL_ON_EXTERNAL_RUN_BINDING")


class IdentityTransport(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(adapter, "missing state and custody adapter")
        self.key=np.array([11,13,15,17,19,21,23,25],dtype=np.int64)
        self.seed_owner=np.array([901]*4+[303]*4)
        self.xyz=np.tile([6.5/16,5.5/16,4.5/16],(8,1))
        self.rank={901:1,303:8}

    def vote(self,keys=None):
        return adapter.transport_owners(self.key,self.seed_owner,self.key if keys is None else keys,
                                        self.xyz,self.rank,16,18)

    def test_majority_uses_carried_id_with_external_tie_rank(self):
        grid=self.vote()
        self.assertEqual(grid[5,4,4],901)  # external canonical rank, not lower DEM atom number
        self.assertEqual(np.count_nonzero(grid!=-1),1)
        self.xyz[0]=[.5/16,3.5/16,4.5/16]
        self.assertEqual(self.vote()[5,4,4],303)
        self.assertEqual(self.vote()[-1,2,4],-1)  # one SE point is below occupancy

    def test_reordered_points_keyed_not_positional(self):
        self.xyz[0]=[.5/16,.5/16,.5/16]
        old=self.vote()
        self.xyz=self.xyz[::-1]
        np.testing.assert_array_equal(self.vote(self.key[::-1]),old)

    def test_missing_split_duplicate_or_ambiguous_rank_refused(self):
        for keys in (self.key[:-1],np.array([11]*8),self.key+1):
            with self.subTest(keys=keys), self.assertRaises(ValueError):
                self.vote(keys)
        self.rank[901]=8
        with self.assertRaises(ValueError):
            self.vote()

    def test_exact_integer_ids_and_rank_above_binary64(self):
        original=2**53+17
        self.seed_owner=np.array([original]*4+[original+1]*4,dtype=np.int64)
        self.rank={original:201,original+1:200}
        self.assertEqual(self.vote()[5,4,4],original+1)
        self.seed_owner=self.seed_owner.astype(np.float64)
        with self.assertRaises(ValueError):
            self.vote()


if __name__=="__main__":
    unittest.main()
