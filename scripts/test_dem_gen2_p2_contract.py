"""Unexecuted tests-first P2 native/separation contract; synthetic inputs only.

No implementation body exists when this suite is first written. S0 must be
fixed before running. Copy exact dependencies; install audit before project code.
Q-P2-1/2 are toy preparation assumptions, not actual registration or engine GO.
"""
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest

source_dir = Path(__file__).parent
s0_fixture_module = types.ModuleType('fixed_synthetic_s0_fixture')
s0_fixture_module.__file__ = str(source_dir / 'test_dem_gen2_s0_contract.py')
exec(compile(Path(s0_fixture_module.__file__).read_bytes(),
             s0_fixture_module.__file__, 'exec'), s0_fixture_module.__dict__)
sys.modules['dem_gen2_s0_contract'] = s0_fixture_module.s0
p2 = types.ModuleType('dem_gen2_p2_contract')
p2.__file__ = str(source_dir / 'dem_gen2_p2_contract.py')
exec(compile(Path(p2.__file__).read_bytes(), p2.__file__, 'exec'), p2.__dict__)

# Replace with the final S0 dependency pin before freezing the first red suite.
S0_PIN = 'f4647f2b7c218a6df7def3292c092273f9d4e35f'
ACTIVE = ['P2_NATIVE_PARAMS_V1', 'P2_S0_BOUNDARY_V1', 'P2_H0_RATIO_V1',
          'P2_EXPLICIT_GRAVITY_V1', 'P2_PHYSICAL_WINDOW_V1',
          'P2_SINGLE_ATTEMPT_V1', 'P2_TWO_ZERO_CLEAR_FOUR_POST_V1']


def independent_bytes(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(value).hexdigest()


def pair(value):
    return [value.numerator, value.denominator]


def refreeze(plan, context):
    """Toy setup only; never an operating seal or authentication claim."""
    plan['header']['params_sha256'] = digest(independent_bytes(plan['params']))
    context['expected_plan_sha256'] = digest(independent_bytes(plan))


def fixture(grid_choice='coarse', unload_case='A'):
    """Seven small windows: contact, zero, zero, clear, four post windows.

At coarse dt=1/8 and T_W=2, W=16. Boundary step=96; second zero ends
at 144, clear follows at the same step, and post window 4 ends at 208.
Half has W=32, boundary=192, second zero=288, post end=416.
No q output generates the invented force/contact/surface samples below.
"""
    s0_contract, envelope, live_plan, servo, ra = s0_fixture_module.fixture(grid_choice=grid_choice)
    archive = s0_fixture_module.archive_bytes(envelope)
    boundary = envelope['boundary_candidate']
    params = dict(schema='P2_NATIVE_ULPR_PARAMS_V1', s0_id=envelope['s0_id'],
        h0_basis='S0_PLATE_Z_MINUS_DECLARED_BOTTOM', bottom_z=[0,1], h0=[10,1],
        increment_ratio_A=[1,10], increment_ratio_B=[1,40], lift_cap_ratio=[1,5],
        unload_case=unload_case, primary_selection='SELECTION_UNRESOLVED',
        units=dict(length='TOY_LENGTH', time='s', pressure='TOY_PRESSURE',
                   energy='TOY_ENERGY', gravity='TOY_ACCELERATION'),
        gravity=dict(policy='EXPLICIT_VECTOR', variant='MAIN',
            vector=[[0,1],[0,1],[-1,1]], basis_id='toy_gravity_v1'),
        pbc_policy='NONE',
        time=dict(dt_seconds=[1,8], dt_half_seconds=[1,16], window_seconds=[2,1],
                  window_steps=16, half_window_steps=32, grid_choice=grid_choice),
        pressure_crossing_threshold=[1,1], max_ke=[1,1000], max_surface_drift=[1,1000],
        zero_windows=2, post_windows=4, clear_action='MOVE_CLEAR')
    header = dict(schema='P2_NATIVE_ACTIVE_HEADER_V1', protocol='P2',
        profile='P2_NATIVE_ULPR_V1', active_definitions=list(ACTIVE),
        producer_pin='a'*40, consumer_definition_pin='e'*40, s0_contract_pin=S0_PIN,
        s0_sha256=digest(archive), params_sha256=digest(independent_bytes(params)),
        source_mapping=dict(atom_profile='ATOM16',
            pair_reference_sha256=digest(independent_bytes(s0_contract['pair_reference'])),
            wall_reference_sha256=digest(independent_bytes(s0_contract['wall_reference']))))
    plan = dict(schema='DEM_GEN2_P2_NATIVE_SYNTHETIC_PLAN_V1', purpose='SYNTHETIC_PREPARATION',
        protocol='P2', assumptions=['Q-P2-1','Q-P2-2'], plan_id='toy_p2_A', revision=1,
        identity=copy.deepcopy(boundary['identity']), header=header, params=params)
    context = dict(schema='SYNTHETIC_P2_S0_SOURCE_CONTEXT_V1', s0_contract_pin=S0_PIN,
        expected_plan_sha256=digest(independent_bytes(plan)), expected_s0_sha256=digest(archive),
        s0_contract=s0_contract, live_plan=live_plan, servo_frames=servo, ra_frames=ra)
    w = 16 if grid_choice == 'coarse' else 32
    start = boundary['end_step']
    h0 = Fraction(10)
    increment = h0 * Fraction(*(params['increment_ratio_A'] if unload_case=='A'
                                else params['increment_ratio_B']))
    zero_plate = h0 + 2*increment
    clear_plate = zero_plate + 1
    trace = []
    for index in range(7):
        phase = 'UNLOADING' if index < 3 else 'POST'
        lift_index = 1 if index == 0 else 2
        z = h0 + lift_index*increment if phase=='UNLOADING' else clear_plate
        window = dict(kind='WINDOW', window_index=index,
            identity=copy.deepcopy(plan['identity']), plan_sha256=context['expected_plan_sha256'],
            s0_id=envelope['s0_id'], s0_sha256=digest(archive),
            inventory_id=boundary['inventory_id'], mesh_id=boundary['plate']['mesh_id'],
            wall_id=boundary['plate']['wall_id'], history_id=boundary['plate']['history_id'],
            phase=phase, plate_mode='BOUND' if phase=='UNLOADING' else 'CLEARED',
            lift_index=lift_index, start_step=start+index*w+1,
            end_step=start+(index+1)*w, gravity=copy.deepcopy(params['gravity']),
            complete=True, samples=[])
        for offset in range(w):
            window['samples'].append(dict(step=window['start_step']+offset,
                contact_count=2 if index==0 else 0, contacts_complete=True,
                ke=0., surface_height=10., pressure=2. if index==0 else .5,
                plate_z=float(z), inventory_complete=True,
                particles=copy.deepcopy(boundary['reference_inventory'])))
        trace.append(window)
        if index == 2:
            trace.append(dict(kind='PLATE_CLEAR', action='MOVE_CLEAR',
                identity=copy.deepcopy(plan['identity']),
                plan_sha256=context['expected_plan_sha256'],
                s0_id=envelope['s0_id'], s0_sha256=digest(archive),
                after_window_index=2, step=window['end_step'],
                mesh_id=boundary['plate']['mesh_id'], wall_id=boundary['plate']['wall_id'],
                history_id=boundary['plate']['history_id'], position_z=pair(clear_plate)))
    return plan, archive, context, trace


class P2NativeContract(unittest.TestCase):
    def authority_off(self, result):
        for key in ('physical_ready','execution_go','transition_authorized','gate_write',
                    'operational_seal_modified','registration_complete',
                    'source_authenticated','hidden_history_qualified'):
            self.assertIs(result[key],False)
        for key in ('actual_T0','actual_T11','actual_T12'):
            self.assertEqual(result[key],'NOT_RUN')
        self.assertIsNone(result['actual_S0'])
        self.assertIsNone(result['actual_unload_case'])
        self.assertEqual(result['research_results'],0)
        self.assertEqual(result['whole_status'],'HOLD')
        self.assertEqual(result['assumptions'],['Q-P2-1','Q-P2-2'])

    def accepted(self,args):
        result=p2.validate_p2_contract(*args[:3])
        self.assertEqual(result['status'],'SYNTHETIC_P2_CONTRACT_CONSISTENT',result)
        self.authority_off(result)
        return result['compiled']

    def rejected(self,args):
        result=p2.validate_p2_contract(*args[:3])
        self.assertEqual(result['status'],'REJECTED',result)
        self.assertIsNone(result['compiled'])
        self.authority_off(result)
        return result

    def diagnose(self,args,status):
        result=p2.diagnose_p2_separation(*args)
        self.assertEqual(result['status'],status,result)
        self.authority_off(result)
        self.assertEqual(result['primary_status'],'SELECTION_UNRESOLVED')
        if status!='SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE':
            self.assertNotEqual(result['trajectory_status'],'POST_DIAGNOSTIC_CANDIDATE')
        return result

    def test_01_native_contract_compiles_hand_calculated_h0_ratios(self):
        for case,expected in (('A',[1,1]),('B',[1,4])):
            with self.subTest(case=case):
                result=self.accepted(fixture(unload_case=case))
                self.assertEqual(result['h0'],[10,1])
                self.assertEqual(result['selected_increment'],expected)
                self.assertEqual(result['maximum_lift'],[2,1])
                self.assertEqual(result['window_steps'],16)
                self.assertEqual(result['half_window_steps'],32)

    def test_02_native_discriminator_header_and_params_refuse_p1_renaming(self):
        for location,key,value in (('plan','protocol','P1'),('header','schema','r8'),
            ('header','profile','P1_r8'),('params','schema','P1_UNLOAD_PARAMS'),
            ('header','active_definitions',['r8'])):
            args=fixture();p=args[0];obj=p if location=='plan' else p[location]
            obj[key]=value;refreeze(p,args[2])
            with self.subTest(location=location,key=key):self.rejected(args)

    def test_03_header_and_external_plan_hashes_are_distinct_guards(self):
        args=fixture();args[0]['params']['max_ke']=[1,100];self.rejected(args)
        args=fixture();args[0]['plan_id']='changed_after_freeze';self.rejected(args)
        args=fixture();args[0]['header']['s0_sha256']='e'*64
        refreeze(args[0],args[2]);self.rejected(args)
        args=fixture();args[0]['header']['source_mapping']['pair_reference_sha256']='e'*64
        refreeze(args[0],args[2]);self.rejected(args)

    def test_04_s0_is_decoded_and_original_live_inputs_revalidated(self):
        args=fixture();args[2]['ra_frames'][-1]['channels']['plate']['values']['velocity'][2]=1.
        self.rejected(args)
        args=fixture();args[2]['ra_frames'].pop();self.rejected(args)
        args=fixture();args[2]['live_plan']={'status':'SYNTHETIC_RA_END_CANDIDATE'}
        self.rejected(args)

    def test_05_self_consistent_archive_rehash_cannot_hide_bad_atom_or_missing_object(self):
        for mutation in ('mass','omega','object'):
            p,b,c,t=fixture();body=json.loads(b)['body']
            if mutation=='object':body['objects'].pop()
            else:
                atom=body['objects'][0]
                payload=s0_fixture_module.payload_json(atom)
                if mutation=='mass':payload['rows'][0][6]=9.
                else:payload['rows'][0].pop(10)
                s0_fixture_module.replace_payload(atom,independent_bytes(payload))
            s0_fixture_module.rechain(body)
            b=s0_fixture_module.archive_bytes(body)
            p['header']['s0_sha256']=digest(b);c['expected_s0_sha256']=digest(b)
            refreeze(p,c)
            with self.subTest(mutation=mutation):self.rejected((p,b,c,t))

    def test_06_s0_identity_and_native_h0_are_not_free_labels(self):
        for location,key,value in (('identity','attempt_id','old_attempt'),
            ('identity','unit_system_id','another_unit'),('params','s0_id','other_s0'),
            ('params','h0',[9,1]),('params','bottom_z',[11,1]),
            ('params','h0_basis','P1_H0_117')):
            args=fixture();args[0][location][key]=value;refreeze(args[0],args[2])
            with self.subTest(location=location,key=key):self.rejected(args)

    def test_07_dt_half_requires_double_steps_and_same_physical_window(self):
        compiled=self.accepted(fixture(grid_choice='half'))
        self.assertEqual(compiled['selected_window_steps'],32)
        self.assertEqual(compiled['selected_dt_seconds'],[1,16])
        for key,value in (('half_window_steps',16),('dt_half_seconds',[1,32]),
                          ('window_steps',15),('window_seconds',[5,3])):
            args=fixture();args[0]['params']['time'][key]=value;refreeze(args[0],args[2])
            with self.subTest(key=key):self.rejected(args)

    def test_08_explicit_gravity_and_case_selection_cannot_be_inferred(self):
        for change in ('missing','prefix_policy','missing_case','legacy_units'):
            args=fixture();p=args[0]
            if change=='missing':del p['params']['gravity']
            elif change=='prefix_policy':p['params']['gravity']['policy']='INFER_G_PREFIX'
            elif change=='missing_case':p['params']['unload_case']=None
            else:p['params']['units']['gravity']='P1_IMPLICIT'
            refreeze(p,args[2])
            with self.subTest(change=change):self.rejected(args)

    def test_09_two_zero_clear_then_four_post_has_independent_events(self):
        result=self.diagnose(fixture(),'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE')
        self.assertEqual(result['trajectory_status'],'POST_DIAGNOSTIC_CANDIDATE')
        self.assertEqual(result['first_pressure_crossing']['step'],113)
        self.assertEqual(result['second_zero_window_end'],{'window_index':2,'step':144})
        self.assertEqual(result['plate_clear_event']['step'],144)
        self.assertEqual(result['post_end'],{'window_index':6,'step':208})
        self.assertEqual(result['checked_post_windows'],4)

    def test_10_half_grid_uses_same_physical_end_with_more_steps(self):
        result=self.diagnose(fixture(grid_choice='half'),'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE')
        self.assertEqual(result['second_zero_window_end']['step'],288)
        self.assertEqual(result['post_end']['step'],416)
        self.assertEqual(Fraction(416,16),Fraction(208,8))

    def test_11_primary_selection_stays_unresolved_without_pressure_crossing(self):
        args=fixture()
        for record in args[3]:
            if record['kind']=='WINDOW':
                for sample in record['samples']:sample['pressure']=2.
        result=self.diagnose(args,'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE')
        self.assertIsNone(result['first_pressure_crossing'])
        self.assertEqual(result['primary_status'],'SELECTION_UNRESOLVED')

    def test_12_one_zero_window_cannot_authorize_clear(self):
        args=fixture();event=args[3].pop(3)
        event.update(after_window_index=1,step=128)
        args[3].insert(2,event)
        self.diagnose(args,'REJECTED')

    def test_13_missing_counts_or_incomplete_samples_are_not_zero(self):
        for change in ('none','missing','false','incomplete_inventory'):
            args=fixture();sample=args[3][1]['samples'][0]
            if change=='none':sample['contact_count']=None
            elif change=='missing':del sample['contact_count']
            elif change=='false':sample['contacts_complete']=False
            else:sample['inventory_complete']=False
            with self.subTest(change=change):self.diagnose(args,'NOT_COMPUTED')

    def test_14_one_nonzero_sample_breaks_second_zero_window(self):
        args=fixture();args[3][2]['samples'][7]['contact_count']=1
        self.diagnose(args,'REJECTED')

    def test_15_gap_stale_duplicate_or_wrong_attempt_is_not_a_contiguous_window(self):
        for change in ('gap','stale','duplicate','attempt','history'):
            args=fixture();window=args[3][2]
            if change=='gap':window['samples'].pop(7)
            elif change=='stale':window['samples'][7]['step']-=1
            elif change=='duplicate':window['samples'].insert(7,copy.deepcopy(window['samples'][7]))
            elif change=='attempt':window['identity']['attempt_id']='old_attempt'
            else:window['history_id']='recreated_plate'
            with self.subTest(change=change):
                self.diagnose(args,'INCOMPLETE' if change=='gap' else 'REJECTED')

    def test_16_early_clear_mode_or_legacy_mesh_deletion_is_refused(self):
        for change in ('mode','event_action','position','old_event'):
            args=fixture()
            if change=='mode':args[3][1]['plate_mode']='CLEARED'
            elif change=='event_action':args[3][3]['action']='DELETE_MESH'
            elif change=='position':args[3][3]['position_z']=[11,1]
            else:args[3][3]['identity']['attempt_id']='old_attempt'
            with self.subTest(change=change):self.diagnose(args,'REJECTED')

    def test_17_clear_event_required_between_zero_and_post_windows(self):
        args=fixture();args[3].pop(3);self.diagnose(args,'REJECTED')
        args=list(fixture());args[3]=args[3][:3]
        result=self.diagnose(args,'INCOMPLETE')
        self.assertEqual(result['second_zero_window_end']['step'],144)
        self.assertIsNone(result['plate_clear_event'])

    def test_18_only_three_post_windows_are_incomplete(self):
        args=fixture();args[3].pop()
        result=self.diagnose(args,'INCOMPLETE')
        self.assertEqual(result['checked_post_windows'],3)
        self.assertIsNone(result['post_end'])

    def test_19_post_surface_drift_or_energy_budget_is_not_converged(self):
        for field,value in (('ke',1.),('surface_height',11.)):
            args=fixture();args[3][-1]['samples'][-1][field]=value
            with self.subTest(field=field):self.diagnose(args,'NOT_CONVERGED')

    def test_20_same_particle_count_with_new_mass_type_or_id_is_not_same_s0_inventory(self):
        for field,value in (('mass',9.),('type',3),('id',3)):
            args=fixture();args[3][-1]['samples'][0]['particles'][0][field]=value
            with self.subTest(field=field):self.diagnose(args,'REJECTED')

    def test_21_post_has_zero_contacts_fixed_clear_position_and_same_gravity(self):
        for change in ('contact','plate','gravity','s0'):
            args=fixture();window=args[3][-1]
            if change=='contact':window['samples'][0]['contact_count']=1
            elif change=='plate':window['samples'][0]['plate_z']=12.
            elif change=='gravity':window['gravity']['vector'][2]=[0,1]
            else:window['s0_id']='another_s0'
            with self.subTest(change=change):self.diagnose(args,'REJECTED')

    def test_22_no_automatic_window_extension_or_event_replay(self):
        args=fixture();args[3].append(copy.deepcopy(args[3][-1]));self.diagnose(args,'REJECTED')
        args=fixture();args[3].insert(4,copy.deepcopy(args[3][3]));self.diagnose(args,'REJECTED')

    def test_23_exact_count_and_finite_numeric_fields_are_required(self):
        for value in (True,-1,0.0,'0'):
            args=fixture();args[3][1]['samples'][0]['contact_count']=value
            with self.subTest(value=value):self.diagnose(args,'REJECTED')
        for field in ('ke','surface_height','pressure','plate_z'):
            args=fixture();args[3][-1]['samples'][0][field]=float('nan')
            with self.subTest(field=field):self.diagnose(args,'REJECTED')

    def test_24_unknown_actual_authority_and_non_native_objects_are_refused(self):
        for location in ('plan','header','params','context'):
            args=fixture();obj=args[2] if location=='context' else args[0] if location=='plan' else args[0][location]
            obj['execution_go']=True;refreeze(args[0],args[2])
            with self.subTest(location=location):self.rejected(args)
        args=fixture();args[3][0]['execution_go']=True;self.diagnose(args,'REJECTED')

    def test_25_original_inputs_are_not_mutated(self):
        args=fixture();before=copy.deepcopy(args)
        self.accepted(args);self.diagnose(args,'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE')
        self.assertEqual(args,before)

    def test_26_direct_subclass_hooks_are_not_called(self):
        calls=[]
        class TrapDict(dict):
            def __getitem__(self,key):calls.append('getitem');raise AssertionError('hook')
        class TrapList(list):
            def __iter__(self):calls.append('iter');raise AssertionError('hook')
        class TrapInt(int):
            def __int__(self):calls.append('int');raise AssertionError('hook')
        for change in ('plan','context','trace','count'):
            args=list(fixture())
            if change=='plan':args[0]=TrapDict(args[0]);self.rejected(args)
            elif change=='context':args[2]=TrapDict(args[2]);self.rejected(args)
            elif change=='trace':args[3]=TrapList(args[3]);self.diagnose(args,'REJECTED')
            else:args[3][1]['samples'][0]['contact_count']=TrapInt(0);self.diagnose(args,'REJECTED')
        self.assertEqual(calls,[])

    def test_27_key_subclass_is_checked_before_hash_or_equality(self):
        calls=[]
        class TrapKey(str):
            def __hash__(self):calls.append('hash');return str.__hash__(self)
            def __eq__(self,other):calls.append('eq');return str.__eq__(self,other)
        args=fixture();value=args[0].pop('schema');args[0][TrapKey('schema')]=value;calls.clear()
        self.rejected(args);self.assertEqual(calls,[])

    def test_28_unloading_position_cannot_exceed_h0_scaled_cap(self):
        args=fixture()
        for sample in args[3][0]['samples']:sample['plate_z']=13.
        args[3][0]['lift_index']=3
        self.diagnose(args,'REJECTED')

    def test_29_post_pressure_crossing_is_not_an_unloading_crossing(self):
        args=fixture()
        for record in args[3]:
            if record['kind']=='WINDOW' and record['phase']=='UNLOADING':
                for sample in record['samples']:sample['pressure']=2.
        result=self.diagnose(args,'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE')
        self.assertIsNone(result['first_pressure_crossing'])
        self.assertEqual(result['primary_status'],'SELECTION_UNRESOLVED')


if __name__=='__main__':
    unittest.main()
