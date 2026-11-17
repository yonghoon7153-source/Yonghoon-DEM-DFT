"""Expected-correct synthetic contracts for REG 15-5 / 15-5b; no engine."""
import copy
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rt_numeric',os.environ.get('RT_NUMERIC_SOURCE',str(HERE/'rt_numeric.py')))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
BOX=((0.0,0.05),(0.0,0.05),(-0.01,1.0))

def row(i=1,x=.01,y=.01,ft=1.0):
    return [x,y,.001,x+.00001,y,.001,i,i+1,0,1.,2.,3.,4.,5.,6.,ft,0.,0.,7.,8.,9.,.0003,.0001,.0002,.0003,.004,.005,x,y,.001]

def write(path,rows,n=30,step=2000,box=BOX,cols=None):
    rows=[v if n==30 else v[:21]+v[25:] for v in rows]
    cols=cols or [('c_ul_ph' if n==30 else 'c_cpl')+'['+str(i)+']' for i in range(1,n+1)]
    lines=['ITEM: TIMESTEP',str(step),'ITEM: NUMBER OF ENTRIES',str(len(rows)),'ITEM: BOX BOUNDS pp pp ff']
    lines += [' '.join(str(x) for x in b) for b in box]+['ITEM: ENTRIES '+' '.join(cols)]
    lines += [' '.join(str(x) for x in v) for v in rows]
    path.write_text('\n'.join(lines)+'\n',encoding='ascii')

def flipped(v):
    w=v[3:6]+v[:3]+v[6:];w[6],w[7]=v[7],v[6]
    for c in list(range(9,18))+[22,23,24]:w[c]=-w[c]
    return w

def grid_rows(p=2,q=2,n=100):
    rows=[]
    for ix in range(p):
        for iy in range(q):
            for j in range(n):
                rows.append(row(2*len(rows)+1,(ix+.4)*.05/p,(iy+.4)*.05/q))
    return rows

class Numeric(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.a=self.root/'a.dump';self.b=self.root/'b.dump'
        self.rows=[row(),row(3,.02,.02)]
        write(self.a,self.rows);write(self.b,self.rows)
    def call(self,name,*a,**kw):
        self.assertTrue(callable(getattr(m,name,None)),name+' not implemented')
        return getattr(m,name)(*a,**kw)
    def compare(self,status='PASS',**kw):
        before=[p.read_bytes() if p.exists() else None for p in (self.a,self.b)]
        r=self.call('g2cp_compare',self.b,self.a,expected_step=2000,**kw)
        self.assertEqual(r['status'],status,r)
        self.assertEqual(before,[p.read_bytes() if p.exists() else None for p in (self.a,self.b)])
        return r
    def test_normal_and_exact_metrics(self):
        r=self.compare();self.assertEqual(r['n_orig'],2);self.assertEqual(r['n_exact_compared_pairs'],2)
        self.assertEqual(r['discriminating_frac'],1);self.assertFalse(r['physical_qualification'])
    def test_orientation_and_periodic_wrap(self):
        rows=[flipped(v) for v in reversed(self.rows)]
        for v in rows:
            for c in (0,1,3,4,27,28):v[c]+=.05
        write(self.b,rows);self.compare()
    def test_history_all_four_columns_are_compared(self):
        for c in range(21,25):
            with self.subTest(column=c+1):
                v=copy.deepcopy(self.rows);v[0][c]*=2;write(self.b,v);self.compare('FAIL')
    def test_force_position_geometry_columns_are_compared(self):
        for c in list(range(6))+list(range(9,18))+list(range(25,30)):
            with self.subTest(column=c+1):
                v=copy.deepcopy(self.rows);v[0][c]+=.001;write(self.b,v);self.compare('FAIL')
    def test_torque_and_periodic_flag_excluded(self):
        v=copy.deepcopy(self.rows)
        for c in (8,18,19,20):v[0][c]+=19
        write(self.b,v);self.compare()
    def test_reference_column_median_floor(self):
        v=[row(1),row(3),row(5)];v[0][22]=0;v[1][22]=v[2][22]=10
        write(self.a,v);t=copy.deepcopy(v);t[0][22]=.00009;write(self.b,t);self.compare()
        t[0][22]=.00011;write(self.b,t);self.compare('FAIL')
    def test_zero_floor_never_hides_nonzero(self):
        v=copy.deepcopy(self.rows)
        for w in v:w[22]=0
        write(self.a,v);v[0][22]=1e-20;write(self.b,v);self.compare('FAIL')
    def test_consistent_duplicate_and_conflicting_duplicate(self):
        write(self.b,self.rows+[flipped(self.rows[0])]);r=self.compare();self.assertEqual(r['n_dup_consistent'],1)
        v=flipped(self.rows[0]);v[22]+=.001;write(self.b,self.rows+[v]);self.compare('FAIL')
    def test_exact_id_boundary_and_fractional_tokens(self):
        v=row(2**53-1);write(self.a,[v]);write(self.b,[v]);self.compare()
        for token in ('9007199254740993','9007199254740993.0','2.0000000000000001','0','-1','nan','1_0'):
            with self.subTest(token=token):
                w=v.copy();w[6]=token;write(self.b,[w]);self.compare('FAIL')
    def test_missing_columns_each_side(self):
        for side in (self.a,self.b):
            for i in range(30):
                write(self.a,self.rows);write(self.b,self.rows)
                lines=side.read_text().splitlines();cs=lines[8].split()[2:];del cs[i]
                lines[8]='ITEM: ENTRIES '+' '.join(cs)
                for j in range(9,len(lines)):
                    toks=lines[j].split();del toks[i];lines[j]=' '.join(toks)
                side.write_text('\n'.join(lines)+'\n');self.compare('NOT_COMPUTED')
    def test_column_order_extra_and_duplicate(self):
        cols=['c_ul_ph[%d]'%i for i in range(1,31)]
        for bad in (cols[::-1],cols+['extra'],cols+[cols[0]]):
            write(self.b,self.rows,cols=bad);self.compare('FAIL')
    def test_structure_nonfinite_rows_and_box(self):
        for mutate in ('row_short','nan','count','step','duplicate_frame','box','prefix'):
            with self.subTest(mutate=mutate):
                write(self.b,self.rows);s=self.b.read_text();lines=s.splitlines()
                if mutate=='row_short':lines[9]=' '.join(lines[9].split()[:-1])
                if mutate=='nan':lines[9]='nan '+' '.join(lines[9].split()[1:])
                if mutate=='count':lines[3]='3'
                if mutate=='step':lines[1]='2001'
                if mutate=='duplicate_frame':lines+=lines
                if mutate=='box':lines[5]='0.05 0'
                if mutate=='prefix':lines[0]='ITEM: TIMESTEPS'
                self.b.write_text('\n'.join(lines)+'\n');self.compare('FAIL')
    def test_missing_file_and_two_empty(self):
        self.b.unlink();self.compare('NOT_COMPUTED')
        write(self.a,[]);write(self.b,[]);self.compare('NOT_COMPUTED')
    def test_one_empty_or_disjoint_is_failure(self):
        write(self.b,[]);self.compare('FAIL')
        write(self.b,[row(5)]);self.compare('FAIL')
    def test_projection_retains_legacy_twenty_six_order(self):
        r=self.call('read_contacts',self.a,'rt30');self.assertEqual(r['status'],'PASS')
        p=self.call('project_legacy',r['rows'][(1,2)])
        self.assertEqual(p,self.rows[0][:21]+self.rows[0][25:])
    def test_bad_header_encoding_and_unreadable_are_failures(self):
        for bad in (b'not a dump', self.b.read_bytes().replace(b'ITEM: ENTRIES',b'ITEM: WRONG'), b'\xff'):
            self.b.write_bytes(bad);self.compare('FAIL')
        self.b.unlink();self.b.mkdir()
        r=self.call('g2cp_compare',self.b,self.a,expected_step=2000);self.assertEqual(r['status'],'FAIL')
    def test_report_only_force_shear_and_exact_bytes_are_distinct(self):
        v=copy.deepcopy(self.rows)
        for w in v:w[15]=0
        write(self.a,v);write(self.b,v)
        r=self.compare();self.assertEqual(r['discriminating_frac'],0);self.assertEqual(r['shear_nonzero_frac'],1)
        v[0][18]+=1;write(self.b,v)
        r=self.compare();self.assertEqual(r['n_bitwise_compared_pairs'],2)
        self.assertEqual(r['n_bitwise_full30_pairs'],1);self.assertFalse(r['input_bytes_equal'])
        self.assertEqual(r['max_relative_difference'],[0]*24)

class Continuity(Numeric):
    # Reuse only helpers, not Numeric's test methods (separate class assembled below).
    def setUp(self):
        Numeric.setUp(self);self.rows=grid_rows();write(self.a,self.rows,26);write(self.b,self.rows,26)
    def guard(self,status='PASS',**kw):
        args=dict(expected_step=2000,grid_text='2 by 2 by 1 MPI processor grid\nLoop time of 0 on 4 procs for 0 steps',expected_grid=(2,2,1),expected_np=4)
        args.update(kw);r=self.call('cont_guard',self.b,self.a,**args);self.assertEqual(r['status'],status,r);return r
    def test_normal_fixed_minimum_and_cells(self):
        r=self.guard();self.assertEqual(r['W'],0);self.assertEqual([c['n_loaded'] for c in r['cells']],[100]*4)
        self.assertEqual(m.MIN_CELL_PAIRS,100)
    def test_global_exact_boundary_and_above(self):
        for n,s in ((20,'PASS'),(21,'FAIL')):
            v=copy.deepcopy(self.rows)
            for w in v[:n]:w[15]=0
            write(self.b,v,26);r=self.guard(s);self.assertAlmostEqual(r['W'],n/400)
    def test_reset_ratio_strict_half(self):
        for value,s in ((.5,'PASS'),(.499,'FAIL')):
            v=copy.deepcopy(self.rows)
            for w in v:w[15]=value
            write(self.b,v,26);self.guard(s)
    def test_weight_not_pair_count(self):
        v=copy.deepcopy(self.rows);v[0][15]=1000;write(self.a,v,26);v[0][15]=0;write(self.b,v,26)
        r=self.guard('FAIL');self.assertGreater(r['W'],.7);self.assertEqual(r['n_reset_like'],1)
    def test_small_weights_do_not_force_failure_by_count(self):
        v=copy.deepcopy(self.rows)
        for w in v[:60]:w[15]=.001
        write(self.a,v,26);t=copy.deepcopy(v)
        for w in t[:60]:w[15]=0
        write(self.b,t,26);r=self.guard();self.assertEqual(r['n_reset_like'],60)
    def test_six_by_four_each_cell_erasure_and_axes(self):
        v=grid_rows(6,4);write(self.a,v,26)
        for c in range(24):
            t=copy.deepcopy(v)
            for w in t[c*100:(c+1)*100]:w[15]=0
            write(self.b,t,26)
            r=self.guard('FAIL',grid_text='6 by 4 by 1 MPI processor grid\non 24 procs',expected_grid=(6,4,1),expected_np=24)
            self.assertLess(r['W'],.05);self.assertEqual(r['cells'][c]['W'],1)
            self.assertEqual(r['cells'][c]['index'],[c//4,c%4])
    def test_cell_half_boundary_and_above(self):
        v=grid_rows(6,4);write(self.a,v,26)
        for n,s in ((50,'PASS'),(51,'FAIL')):
            t=copy.deepcopy(v)
            for w in t[:n]:w[15]=0
            write(self.b,t,26);self.guard(s,grid_text='6 by 4 by 1 MPI processor grid\non 24 procs',expected_grid=(6,4,1),expected_np=24)
    def test_minimum_ninety_nine_unconfirmed(self):
        write(self.a,self.rows[1:],26);write(self.b,self.rows[1:],26);self.guard('NOT_COMPUTED')
    def test_cell_violation_beats_other_cell_99(self):
        v=grid_rows(6,4)[1:];write(self.a,v,26);t=copy.deepcopy(v)
        for w in t[99:199]:w[15]=0
        write(self.b,t,26)
        self.guard('FAIL',grid_text='6 by 4 by 1 MPI processor grid\non 24 procs',expected_grid=(6,4,1),expected_np=24)
    def test_global_violation_beats_unknown_grid(self):
        v=copy.deepcopy(self.rows)
        for w in v:w[15]=0
        write(self.b,v,26);self.guard('FAIL',grid_text='')
    def test_grid_missing_duplicate_axes_procs_balance(self):
        good='2 by 2 by 1 MPI processor grid\non 4 procs'
        for text in ('',good+'\n'+good,'1 by 4 by 1 MPI processor grid\non 4 procs',good.replace('on 4','on 8'),good+'\nbalance 1.1 shift x 10 1.0',good+'\nfix b all balance 10 1.1 shift x 10 1.0'):
            with self.subTest(text=text):self.guard('NOT_COMPUTED',grid_text=text)
        self.guard(grid_text=good+'\n# balance is disabled')
    def test_boundary_pairs_excluded_and_counted(self):
        v=copy.deepcopy(self.rows);v[0][0]=0.025;write(self.a,v,26);write(self.b,v,26)
        r=self.guard('NOT_COMPUTED');self.assertEqual(r['n_ambiguous_atoms'],1)
    def test_origin_shift_wrap_and_original_positions_used(self):
        box=((.1,.15),(-.2,-.15),(-.01,1))
        v=copy.deepcopy(self.rows)
        for w in v:
            w[0]+=.1;w[3]+=.1;w[1]-=.2;w[4]-=.2
        write(self.a,v,26,box=box);t=copy.deepcopy(v)
        for w in t:w[0]=w[3]=0;w[1]=w[4]=0
        write(self.b,t,26,box=box);self.guard()
    def test_cross_cell_pairs_only_global(self):
        v=copy.deepcopy(self.rows);extra=row(1001,.01,.01,1000);extra[3]=.04;v.append(extra)
        write(self.a,v,26);t=copy.deepcopy(v);t[-1][15]=0;write(self.b,t,26)
        r=self.guard('FAIL');self.assertEqual(r['n_cross_cell_pairs'],1)
    def test_rt30_projection_both_targets(self):
        write(self.b,self.rows,30);self.guard(test_layout='rt30')
        v=copy.deepcopy(self.rows)
        for w in v:w[15]=0
        write(self.b,v,30);self.guard('FAIL',test_layout='rt30')
    def test_zero_reference_denominator_and_empty_rules(self):
        v=copy.deepcopy(self.rows)
        for w in v:w[15]=0
        write(self.a,v,26);write(self.b,v,26);self.guard('NOT_COMPUTED')
        write(self.a,[],26);write(self.b,[],26);self.guard('NOT_COMPUTED')
        write(self.b,[row()],26);self.guard('FAIL')
    def test_set_difference_precedes_grid_absence(self):
        write(self.b,self.rows[1:],26);self.guard('FAIL',grid_text='')
    def test_missing_columns_file_and_bad_structure(self):
        self.b.unlink();self.guard('NOT_COMPUTED')
        write(self.b,self.rows,26,step=2001);self.guard('FAIL')
        write(self.b,self.rows,26);s=self.b.read_text().replace('c_cpl[26]','extra');self.b.write_text(s);self.guard('NOT_COMPUTED')
    def test_finite_extreme_force_scaling(self):
        v=copy.deepcopy(self.rows)
        for w in v:w[15]=1e308;w[16]=1e308;w[17]=1e308
        write(self.a,v,26);write(self.b,v,26);self.guard()
        t=copy.deepcopy(v)
        for w in t:w[15]=w[16]=w[17]=0
        write(self.b,t,26);self.guard('FAIL')
    def test_collapse_means_strict_half_not_only_zero(self):
        v=copy.deepcopy(self.rows)
        for w in v:w[15]=.49
        write(self.b,v,26);r=self.guard('FAIL');self.assertEqual(r['collapse_frac'],1)
        for w in v:w[15]=.5
        write(self.b,v,26);r=self.guard();self.assertEqual(r['collapse_frac'],0)

# Keep helper reuse without executing the Numeric tests against legacy fixtures.
for name in Numeric.__dict__:
    if name.startswith('test_') and name not in Continuity.__dict__:setattr(Continuity,name,None)

if __name__=='__main__':unittest.main(verbosity=2)
