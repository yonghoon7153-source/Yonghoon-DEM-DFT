"""Synthetic fixed-plan arithmetic only; no MC, files beyond fixed source, or engine.

권고안 전제(Q-T5-01..05). Tiny n/seeds/alpha are fixtures, not scientific registration.
"""
from copy import deepcopy
from fractions import Fraction
import math
from pathlib import Path
import types
import unittest

_source = Path(__file__).with_name('dem_gen2_t5_contract.py')
t5 = types.ModuleType('fixed_t5_contract')
exec(compile(_source.read_bytes(), str(_source), 'exec'), t5.__dict__)


def fixture(quantity='VOLUME'):
    """Oracles below are independent geometry formulae, not production q outputs.

    Unit-radius two disjoint/tangent spheres: 2*(4*pi/3).
    Two unit spheres distance1: lens5*pi/12, union9*pi/4.
    Three coincident unit spheres: union4*pi/3, sum4*pi; pair-only subtraction0.
    Unit sphere centered on clipping plane: half-sphere2*pi/3.
    These are declared toy references; the API does not validate a geometry engine.
    """
    identity = dict(plan_id='toy_T5', revision=1, producer_pin='a'*40,
        operator_pin='b'*40, oracle_pin='c'*40, interval_method_pin='d'*40,
        frame_id='frame_A', inventory_id='inventory_A', unit_system_id='toy_units')
    estimands = [dict(id=op+'_'+roi, operator=op, region=roi,
        roi_id='roi_'+roi, denominator_id='den_'+roi,
        clipping_id='declared_clip', pbc_policy='NONE')
        for op in ('sphere', 'union') for roi in ('full', 'interior')]
    formulas = [('two_separate', 8*math.pi/3, 8*math.pi/3),
                ('two_tangent', 8*math.pi/3, 8*math.pi/3),
                ('two_overlap', 8*math.pi/3, 9*math.pi/4),
                ('three_coincident', 4*math.pi, 4*math.pi/3),
                ('wall_half', 2*math.pi/3, 2*math.pi/3)]
    cases = []
    for name, sphere, union in formulas:
        truth = {e['id']: (sphere if e['operator']=='sphere' else union) for e in estimands}
        if quantity == 'POROSITY':
            # Negative sphere porosity is a permitted arithmetic declaration;
            # clipping it to [0,1] would falsify the declared signed estimator.
            truth = {e['id']:-.25 for e in estimands}
        cases.append(dict(id=name, fixture_kind=name, oracle_id='oracle_'+name,
                          oracles=truth))
    seeds = [dict(repetition_id='rep_'+str(i), seed=s, dependence_group='group_'+str(i))
             for i,s in enumerate((11,17,23,29),1)]
    sizes = [16,64]
    cells = [dict(case_id=c['id'], estimand_id=e['id'], n=n,
                  alpha=[1,len(cases)*len(estimands)*len(sizes)*100])
             for c in cases for e in estimands for n in sizes]
    plan = dict(schema='DEM_GEN2_T5_SYNTHETIC_CONTRACT_V1',
        purpose='SYNTHETIC_PREPARATION', identity=identity, quantity=quantity,
        output_unit='SYNTHETIC_LENGTH_CUBED' if quantity=='VOLUME' else 'FRACTION',
        cases=cases, estimands=estimands, sample_sizes=sizes, seeds=seeds,
        dependence='INDEPENDENT_WITHIN_CELL_SHARED_ACROSS_CELLS',
        interval_definition=dict(method_id='declared_toy_intervals',
            nominal_level=[19,20], coverage_target=[3,4],
            evaluation='PLANNED_DENOMINATOR_ONLY', uncertainty='NOT_QUALIFIED'),
        error_policy=dict(mode='ABS', budget=.1),
        family=dict(alpha_family=[1,20],cells=cells),
        missing_policy='COUNT_IN_PLANNED_AND_HOLD', retry_policy='NONE')
    rows=[]
    for c in cases:
        for e in estimands:
            truth=c['oracles'][e['id']]
            for n in sizes:
                for j,s in enumerate(seeds):
                    rows.append(dict(identity=deepcopy(identity),case_id=c['id'],
                        estimand_id=e['id'],n=n,repetition_id=s['repetition_id'],seed=s['seed'],
                        oracle_id=c['oracle_id'],output_unit=plan['output_unit'],status='VALID',
                        value=truth if j<3 else truth+.15,
                        interval=[truth-.1,truth+.1] if j<3 else [truth+.1,truth+.2],
                        failure_code=None))
    return plan,rows


class T5ContractTests(unittest.TestCase):
    def assert_closed(self,result):
        for key in ('physical_ready','execution_go','gate_write'):
            self.assertIs(result[key],False)
        self.assertEqual(result['qualification'],'NOT_RUN')
        self.assertEqual(result['registration_status'],'DRAFT_UNREGISTERED')
        for key in ('interval_generation_qualification','true_coverage_inference','pbc_qualification'):
            self.assertEqual(result[key],'NOT_QUALIFIED')
        self.assertEqual(result['research_results'],0)

    def rejected_plan(self,plan):
        result=t5.validate_t5_plan(plan)
        self.assertEqual(result['status'],'REJECTED')
        self.assert_closed(result)

    def rejected_rows(self,plan,rows):
        result=t5.audit_t5_coverage(plan,rows)
        self.assertEqual(result['status'],'REJECTED')
        self.assert_closed(result)

    def test_01_normal_plan_and_independent_oracles(self):
        p,r=fixture()
        out=t5.validate_t5_plan(p)
        self.assertEqual(out['status'],'SYNTHETIC_PLAN_VALID')
        self.assertEqual(out['planned_cells'],40)
        self.assertEqual(out['planned_trials'],160)
        self.assertEqual(p['cases'][3]['oracles']['union_full'],4*math.pi/3)
        self.assertEqual(p['cases'][3]['oracles']['sphere_full'],4*math.pi)
        self.assertEqual(p['cases'][4]['oracles']['union_full'],2*math.pi/3)
        self.assert_closed(out)

    def test_02_fixed_four_repetitions_have_three_covered(self):
        p,r=fixture();out=t5.audit_t5_coverage(p,r)
        self.assertEqual(out['status'],'SYNTHETIC_BOOKKEEPING_COMPLETE')
        self.assertEqual(out['planned_trials'],160)
        for c in out['cells']:
            self.assertEqual((c['planned'],c['valid'],c['covered']),(4,4,3))
            self.assertEqual(c['conservative_coverage'],.75)
        self.assert_closed(out)

    def test_03_missing_row_keeps_planned_denominator(self):
        p,r=fixture();r.pop(3);out=t5.audit_t5_coverage(p,r)
        self.assertEqual(out['status'],'INCOMPLETE')
        c=out['cells'][0]
        self.assertEqual((c['planned'],c['missing'],c['valid'],c['covered']),(4,1,3,3))
        self.assertEqual(c['conservative_coverage'],.75)
        self.assertEqual(c['eligible_coverage_diagnostic'],1.)
        self.assertEqual(len(out['missing_keys']),1)
        self.assert_closed(out)

    def test_04_explicit_missing_and_failed_are_preserved(self):
        p,r=fixture()
        for row,status in zip(r[:2],('MISSING','FAILED')):
            row.update(status=status,value=None,interval=None,failure_code='toy_failure')
        out=t5.audit_t5_coverage(p,r)
        self.assertEqual(out['status'],'INCOMPLETE')
        c=out['cells'][0]
        self.assertEqual((c['planned'],c['missing'],c['failed'],c['valid'],c['covered']),(4,1,1,2,1))
        self.assertEqual(c['conservative_coverage'],.25)
        self.assert_closed(out)

    def test_05_all_missing_has_null_eligible_diagnostic(self):
        p,r=fixture();out=t5.audit_t5_coverage(p,[])
        self.assertEqual(out['status'],'INCOMPLETE')
        self.assertEqual(out['cells'][0]['conservative_coverage'],0.)
        self.assertIsNone(out['cells'][0]['eligible_coverage_diagnostic'])
        self.assertIsNone(out['cells'][0]['mean_bias'])
        self.assertEqual(len(out['missing_keys']),160)
        self.assert_closed(out)

    def test_06_duplicate_and_manifest_substitution(self):
        for mutate in (lambda r:r.append(deepcopy(r[0])),
                       lambda r:r[0].update(seed=17),
                       lambda r:r[0].update(n=32),
                       lambda r:r[0].update(repetition_id='rep_other'),
                       lambda r:r[0].update(case_id='other'),
                       lambda r:r[0].update(estimand_id='other')):
            p,r=fixture();mutate(r)
            with self.subTest(mutate=mutate): self.rejected_rows(p,r)

    def test_07_identity_pins_frame_inventory_and_units(self):
        for key in ('producer_pin','operator_pin','oracle_pin','interval_method_pin',
                    'frame_id','inventory_id','unit_system_id','plan_id'):
            p,r=fixture();r[0]['identity'][key]='e'*40 if key.endswith('_pin') else 'other'
            with self.subTest(key=key): self.rejected_rows(p,r)
        p,r=fixture();r[0]['output_unit']='FRACTION';self.rejected_rows(p,r)
        p,r=fixture();r[0]['oracle_id']='other';self.rejected_rows(p,r)

    def test_08_nonfinite_values_and_reversed_intervals(self):
        for bad in (float('nan'),float('inf'),-float('inf'),True,'0.5'):
            p,r=fixture();r[0]['value']=bad
            with self.subTest(bad=type(bad).__name__): self.rejected_rows(p,r)
        p,r=fixture();r[0]['interval']=[1.,0.];self.rejected_rows(p,r)
        p,r=fixture();r[0]['interval']=[0.,float('nan')];self.rejected_rows(p,r)

    def test_09_status_payload_and_unknown_fields(self):
        for change in ({'status':'PASS'},{'failure_code':'hidden_failure'},{'interval':None},
                       {'extra':'value'},{'status':'FAILED'},{'status':'MISSING'}):
            p,r=fixture();r[0].update(change)
            with self.subTest(change=tuple(change)): self.rejected_rows(p,r)

    def test_10_plan_schema_context_and_operator_scope(self):
        for change in ({'purpose':'PRODUCTION'},{'schema':'other'},{'extra':1},
                       {'quantity':'PRESSURE'},{'retry_policy':'AUTOMATIC'},
                       {'missing_policy':'DROP'}, {'output_unit':'MPa'}):
            p,r=fixture();p.update(change)
            with self.subTest(change=tuple(change)): self.rejected_plan(p)
        p,r=fixture();p['estimands'][0]['operator']='pair_lens';self.rejected_plan(p)
        p,r=fixture();p['estimands'][0]['region']='unknown';self.rejected_plan(p)

    def test_11_sample_sizes_and_repetition_manifest(self):
        for sizes in ([True,64],[16.,64],[0,64],[64,16],[16,16],[],[16,'64']):
            p,r=fixture();p['sample_sizes']=sizes
            with self.subTest(sizes=sizes): self.rejected_plan(p)
        for field in ('seed','repetition_id','dependence_group'):
            p,r=fixture();p['seeds'][1][field]=p['seeds'][0][field]
            with self.subTest(field=field): self.rejected_plan(p)

    def test_12_family_exact_set_and_alpha_budget(self):
        for mutate in (lambda p:p['family']['cells'].pop(),
                       lambda p:p['family']['cells'].append(deepcopy(p['family']['cells'][0])),
                       lambda p:p['family']['cells'][0].update(n=32),
                       lambda p:p['family']['cells'][0].update(alpha=[1,1])):
            p,r=fixture();mutate(p)
            with self.subTest(mutate=mutate): self.rejected_plan(p)

    def test_13_probability_fields_use_exact_ratios(self):
        for bad in ([1,0],[2,1],[-1,20],[True,20],[1.,20],.95):
            p,r=fixture();p['interval_definition']['nominal_level']=bad
            with self.subTest(bad=bad): self.rejected_plan(p)
        p,r=fixture();p['family']['alpha_family']=[1,100]
        self.assertEqual(t5.validate_t5_plan(p)['status'],'SYNTHETIC_PLAN_VALID')

    def test_14_geometry_interval_not_clamped_to_probability(self):
        p,r=fixture();out=t5.audit_t5_coverage(p,r)
        self.assertEqual(out['status'],'SYNTHETIC_BOOKKEEPING_COMPLETE')
        self.assertGreater(out['cells'][0]['oracle'],1.)
        self.assertEqual(out['cells'][0]['covered'],3)
        self.assertEqual(out['cells'][0]['output_unit'],'SYNTHETIC_LENGTH_CUBED')

    def test_15_negative_porosity_preserved(self):
        p,r=fixture('POROSITY');out=t5.audit_t5_coverage(p,r)
        self.assertEqual(out['status'],'SYNTHETIC_BOOKKEEPING_COMPLETE')
        self.assertEqual(out['cells'][0]['oracle'],-.25)
        self.assertEqual(out['cells'][0]['covered'],3)
        self.assert_closed(out)

    def test_16_bias_and_scatter_are_distinct(self):
        p,r=fixture('POROSITY')
        for i,v in enumerate((-.375,-.125,-.375,-.125)):
            r[i]['value']=v
        out=t5.audit_t5_coverage(p,r)
        self.assertEqual(out['status'],'SYNTHETIC_BOOKKEEPING_COMPLETE')
        c=out['cells'][0]
        self.assertEqual(c['mean_bias'],0.)
        self.assertEqual(c['max_abs_error'],.125)
        self.assertEqual(c['rmse'],.125)

    def test_17_relative_zero_denominator_is_refused(self):
        p,r=fixture();p['error_policy']['mode']='REL'
        p['cases'][0]['oracles']['sphere_full']=0.;self.rejected_plan(p)
        p,r=fixture();p['error_policy']['mode']='REL'
        self.assertEqual(t5.validate_t5_plan(p)['status'],'SYNTHETIC_PLAN_VALID')

    def test_18_pbc_never_becomes_qualified(self):
        p,r=fixture()
        for e in p['estimands']:e['pbc_policy']='XY_PERIODIC'
        out=t5.audit_t5_coverage(p,r)
        self.assertEqual(out['status'],'SYNTHETIC_BOOKKEEPING_COMPLETE')
        self.assertEqual(out['pbc_requirement'],'REQUIRED_UNQUALIFIED')
        self.assert_closed(out)

    def test_19_nominal_level_not_empirical_coverage(self):
        p,r=fixture();p['interval_definition']['nominal_level']=[99,100]
        out=t5.audit_t5_coverage(p,r)
        self.assertEqual(out['status'],'SYNTHETIC_BOOKKEEPING_COMPLETE')
        self.assertEqual(out['cells'][0]['conservative_coverage'],.75)
        p['calibration_target']=[10,13];self.rejected_plan(p)

    def test_20_input_is_not_mutated(self):
        p,r=fixture();before=deepcopy((p,r))
        t5.validate_t5_plan(p);t5.audit_t5_coverage(p,r)
        self.assertEqual((p,r),before)

    def test_21_nonbuiltin_mappings_and_lists_refused(self):
        class D(dict):pass
        class L(list):pass
        p,r=fixture();self.rejected_plan(D(p));self.rejected_rows(p,L(r))
        p,r=fixture();p['identity']=D(p['identity']);self.rejected_plan(p)
        p,r=fixture();r[0]=D(r[0]);self.rejected_rows(p,r)

    def test_22_key_subclasses_refused_before_hash_or_equality(self):
        calls=[]
        class K(str):
            def __hash__(self):calls.append('hash');return str.__hash__(self)
            def __eq__(self,other):calls.append('eq');return str.__eq__(self,other)
        p,r=fixture();value=p.pop('schema');p[K('schema')]=value;calls.clear()
        self.rejected_plan(p);self.assertEqual(calls,[])
        p,r=fixture();value=r[0].pop('status');r[0][K('status')]=value;calls.clear()
        self.rejected_rows(p,r);self.assertEqual(calls,[])

    def test_23_missing_or_extra_oracle_estimand_and_case(self):
        p,r=fixture();p['cases'][0]['oracles'].pop('sphere_full');self.rejected_plan(p)
        p,r=fixture();p['estimands'][0]['id']=p['estimands'][1]['id'];self.rejected_plan(p)
        p,r=fixture();p['cases'][0]['fixture_kind']='unknown';self.rejected_plan(p)


if __name__ == '__main__':
    unittest.main()
