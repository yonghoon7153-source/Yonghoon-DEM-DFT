"""Unexecuted tests-first DEMP metadata contract; no physical calculation.

Q-DEMP-1/2/3. No actual force/position/result payload is provided or read.
The subject is declared stage/evidence/roster consistency, never DEMP closure.
"""
import copy
import hashlib
import json
from pathlib import Path
import types
import unittest

source_path=Path(__file__).with_name('dem_gen2_demp_contract.py')
demp=types.ModuleType('dem_gen2_demp_contract')
exec(compile(source_path.read_bytes(),str(source_path),'exec'),demp.__dict__)

QUALIFICATION_PIN='b7fbe749ea8ffa3151b3e768de445c572940c43d'
STAGES=['INSERTION','STABILIZATION','COMPRESSION','SERVO','RA_END','UNLOADING','POST_SEPARATION']
VECTOR_ROLES=['plate_reaction','global_damping','contact_damping','gravity','inertia',
              'force_balance','torque_balance']
SCALAR_ROLES=['translational_ke','rotational_ke']


def independent_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,
        separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()


def refreeze(plan,context):
    """Only before a toy check; never an actual registration receipt."""
    context['expected_plan_sha256']=independent_hash(plan)


def fixture(mode='uncut'):
    """Two separately planned diameter cases, unequal declared roster sizes.

Each has 7 stage packets and 3 frame labels. No force/position is computed.
Surface cuts with center inside are a second valid metadata plan, not a claim
that the physical defect is absent. Actual static state remains unconfirmed.
"""
    static=dict(stage='RA_END',pressure_definition_id='toy_pressure_rule',
        area_definition_id='toy_area_rule',units_definition_id='toy_units',
        window_definition_id='toy_static_window',history_policy_id='toy_history_policy',
        damping_policy_id='toy_static_damping_policy',inventory_operator_id='fixed_declared_ids',
        metric_operator_id='toy_same_state_operator')
    cases=[]
    for suffix,diameter,count in (('d07',[7,10],2),('d1',[1,1],3)):
        identity=dict(run_id='run_'+suffix,attempt_id='attempt_'+suffix,bed_id='bed_'+suffix,
                      arm_id='arm_'+suffix,definition_id='definition_'+suffix)
        inventory=[dict(id=i+1,type=1,radius_definition_id='radius_'+suffix,
                        mass_definition_id='mass_'+suffix) for i in range(count)]
        cases.append(dict(case_id=suffix,diameter=dict(value=diameter,unit='um',
            kind='DECLARED_NOMINAL_MONODISPERSE_DIAMETER',experimental_PSD='UNKNOWN'),
            identity=identity,recipe_definition_id='toy_common_recipe',
            declared_load_label='same_toy_load_name',static_state_contract=copy.deepcopy(static),
            inventory_id='inventory_'+suffix,reference_inventory=inventory,
            mesh_id='mesh_'+suffix,wall_id='wall_'+suffix,history_id='history_'+suffix))
    stage_plans=[dict(stage=stage,global_damping=dict(policy='EXPLICIT_STAGE',
        definition_id='global_'+stage,model_id='toy_global_viscous'),
        contact_damping=dict(policy='EXPLICIT_STAGE',definition_id='contact_'+stage,
            model_id='toy_contact_damping'),
        force_representation='SIGNED_VECTOR_COMPONENTS',
        force_units_id='toy_force_units',torque_units_id='toy_torque_units',
        energy_units_id='toy_energy_units',gamma_units_id='toy_gamma_units',
        evidence_scope='DECLARATIONS_ONLY_NO_FORCE_RECALC') for stage in STAGES]
    plan=dict(schema='DEM_GEN2_DEMP_SYNTHETIC_CONTRACT_V1',purpose='SYNTHETIC_PREPARATION',
        assumptions=['Q-DEMP-1','Q-DEMP-2','Q-DEMP-3'],plan_id='toy_demp_'+mode,revision=1,
        source_manifest=dict(qualification_matrix_pin=QUALIFICATION_PIN,
            producer_pin='a'*40,consumer_pin='b'*40,definition_pin='c'*40),
        historical_label=dict(label='50kg/batch',meaning='PROJECT_LABEL_ONLY',
            exact_batch_meaning='UNKNOWN',compression_load_conversion='NOT_ESTABLISHED'),
        d9_prime=dict(scope='PURE_SE_300MPA_PLUS_RELAXATION_END',
            calibration_estimand='MASS_BASED_EPSILON_SPHERE',declared_TD=[164,100],
            external_target_percent=[10,13],epsilon_union='RECORD_ONLY'),
        stages=stage_plans,cases=cases,
        comparison=dict(target_static_state=static,recipe_definition_id='toy_common_recipe',
            n_matching='NOT_REQUIRED',actual_state_qualification='NOT_RUN',
            missing_policy='KEEP_PLANNED',retry_policy='NONE'),
        geometry=dict(profile='DECLARED_CLASSIFICATION_ONLY',
            center_and_surface='SEPARATE_FIELDS',continuity='CONTINUITY_UNCONFIRMED',
            actual_mesh_PBC_qualification='NOT_RUN'),
        actual_facts=dict(gamma=None,force_balance_budget=None,geometry_tolerance=None,
            mesh_PBC=None,continuous_trajectory=None,static_pressure_area=None,
            comparison_roster=None,registration_approval=None,qualification_receipt=None))
    context=dict(schema='DEMP_SYNTHETIC_FROZEN_CONTEXT_V1',
        qualification_matrix_pin=QUALIFICATION_PIN,expected_plan_sha256=independent_hash(plan),
        freeze_ordinal=1,first_evidence_ordinal=2)
    packets=[]
    for case in cases:
        for stage_index,stage in enumerate(STAGES):
            first_step=3*stage_index
            binding=dict(identity=copy.deepcopy(case['identity']),stage=stage,
                window_id=case['case_id']+'_'+stage,start_step=first_step,end_step=first_step+2,
                frame_ids=['frame_0','frame_1','frame_2'],inventory_id=case['inventory_id'])
            channels={}
            for role in VECTOR_ROLES+SCALAR_ROLES:
                units='toy_torque_units' if role=='torque_balance' else 'toy_energy_units' if role in SCALAR_ROLES else 'toy_force_units'
                channels[role]=dict(role=role,representation='SIGNED_VECTOR_COMPONENTS' if role in VECTOR_ROLES else 'SCALAR_DEFINITION',
                    units_id=units,binding=copy.deepcopy(binding),source_kind='SYNTHETIC_METADATA_ONLY',
                    source_id=case['case_id']+'_'+stage+'_'+role,source_sha256='d'*64,
                    value_access='NOT_READ')
            geometry_samples=[dict(frame_id='frame_'+str(i),step=first_step+i,center_region='INSIDE',
                sphere_relation='CUT' if mode=='surface_cut' else 'UNCUT') for i in range(3)]
            payload=dict(binding=binding,channels=channels,
                declared_inventory=copy.deepcopy(case['reference_inventory']),
                mesh_id=case['mesh_id'],wall_id=case['wall_id'],history_id=case['history_id'],
                global_damping_definition_id='global_'+stage,
                contact_damping_definition_id='contact_'+stage,
                static_state_contract=copy.deepcopy(static) if stage=='RA_END' else None,
                geometry=dict(profile='DECLARED_CLASSIFICATION_ONLY',
                    continuity='CONTINUITY_UNCONFIRMED',samples=geometry_samples,
                    center_outside_claim='NONE_RECORDED',
                    sphere_cut_claim='SAMPLE_RECORDED' if mode=='surface_cut' else 'NONE_RECORDED'))
            packets.append(dict(case_id=case['case_id'],stage=stage,status='PRESENT',
                payload=payload,failure_code=None))
    return plan,packets,context


class DempContract(unittest.TestCase):
    def authority_off(self,result):
        for key in ('physical_ready','execution_go','gate_write','registration_complete',
                    'source_authenticated','demp01_closed','demp02_closed','actual_state_comparable'):
            self.assertIs(result[key],False)
        self.assertEqual(result['actual_qualification'],'NOT_RUN')
        self.assertEqual(result['continuity'],'CONTINUITY_UNCONFIRMED')
        self.assertEqual(result['research_results'],0)
        self.assertEqual(result['whole_status'],'HOLD')
        self.assertEqual(result['assumptions'],['Q-DEMP-1','Q-DEMP-2','Q-DEMP-3'])

    def check(self,args,status):
        result=demp.validate_demp_contract(*args)
        self.assertEqual(result['status'],status,result)
        self.authority_off(result)
        return result

    def test_01_two_complete_toy_plans_do_not_close_physical_defects(self):
        for mode,cuts in (('uncut',0),('surface_cut',42)):
            with self.subTest(mode=mode):
                result=self.check(fixture(mode),'SYNTHETIC_DEMP_CONTRACT_CONSISTENT')
                self.assertEqual((result['planned_packets'],result['complete_packets']),(14,14))
                self.assertEqual(result['declared_inventory_counts'],{'d07':2,'d1':3})
                self.assertEqual(result['center_outside_samples'],0)
                self.assertEqual(result['sphere_cut_samples'],cuts)

    def test_02_missing_stage_packet_stays_in_planned_denominator(self):
        args=fixture();args[1].pop(2)
        result=self.check(args,'INCOMPLETE')
        self.assertEqual((result['planned_packets'],result['complete_packets'],result['missing_packets']),(14,13,1))

    def test_03_failed_partial_and_explicit_missing_are_not_success(self):
        args=fixture()
        for packet,status in zip(args[1][:3],('FAILED','PARTIAL','MISSING')):
            packet.update(status=status,payload=None,failure_code='toy_missing_evidence')
        result=self.check(args,'INCOMPLETE')
        self.assertEqual(result['planned_packets'],14)
        self.assertEqual((result['complete_packets'],result['failed_packets'],result['partial_packets'],result['missing_packets']),(11,1,1,1))

    def test_04_duplicate_extra_or_unknown_stage_cannot_replace_ra_end(self):
        for change in ('duplicate','extra_case','wrong_stage'):
            args=fixture()
            if change=='duplicate':args[1].append(copy.deepcopy(args[1][0]))
            elif change=='extra_case':args[1][0]['case_id']='unplanned'
            else:args[1][4]['stage']='COMPRESSION'
            with self.subTest(change=change):self.check(args,'REJECTED')

    def test_05_stage_gamma_must_be_explicit_and_separate_from_contact(self):
        for change in ('missing_compression','inherit','merged_models','abs_force'):
            args=fixture();p=args[0]
            if change=='missing_compression':p['stages'].pop(2)
            elif change=='inherit':p['stages'][2]['global_damping']['policy']='INHERIT_PREPARATION'
            elif change=='merged_models':p['stages'][2]['contact_damping']['model_id']=p['stages'][2]['global_damping']['model_id']
            else:p['stages'][2]['force_representation']='ABS_MAGNITUDE'
            refreeze(p,args[2])
            with self.subTest(change=change):self.check(args,'REJECTED')

    def test_06_missing_damping_or_rotational_channel_is_not_reaction_only_success(self):
        for role in ('global_damping','contact_damping','torque_balance','rotational_ke'):
            args=fixture();del args[1][2]['payload']['channels'][role]
            with self.subTest(role=role):self.check(args,'NOT_COMPUTED')

    def test_07_wrong_stage_unit_frame_inventory_or_sign_representation_is_rejected(self):
        for change in ('stage','frame','inventory','unit','abs','role'):
            args=fixture();channel=args[1][2]['payload']['channels']['global_damping']
            if change=='stage':channel['binding']['stage']='STABILIZATION'
            elif change=='frame':channel['binding']['frame_ids'][1]='other_frame'
            elif change=='inventory':channel['binding']['inventory_id']='other_inventory'
            elif change=='unit':channel['units_id']='toy_pressure_units'
            elif change=='abs':channel['representation']='ABS_MAGNITUDE'
            else:channel['role']='contact_damping'
            with self.subTest(change=change):self.check(args,'REJECTED')

    def test_08_current_plate_reaction_is_not_a_completed_force_recalculation(self):
        args=fixture();args[1][2]['payload']['channels']['plate_reaction']['value']=750.
        self.check(args,'REJECTED')
        args=fixture();args[0]['stages'][2]['evidence_scope']='PHYSICAL_BALANCE_VERIFIED'
        refreeze(args[0],args[2]);self.check(args,'REJECTED')

    def test_09_equal_particle_count_with_changed_declared_identity_is_refused(self):
        for key,value in (('id',99),('type',2),('mass_definition_id','other_mass'),('radius_definition_id','other_radius')):
            args=fixture();args[1][2]['payload']['declared_inventory'][0][key]=value
            with self.subTest(key=key):self.check(args,'REJECTED')

    def test_10_particle_loss_or_duplicate_is_not_hidden_by_count_metadata(self):
        args=fixture();args[1][2]['payload']['declared_inventory'].pop();self.check(args,'REJECTED')
        args=fixture();roster=args[1][2]['payload']['declared_inventory'];roster[1]=copy.deepcopy(roster[0])
        self.check(args,'REJECTED')

    def test_11_center_inside_surface_cut_does_not_become_center_passage(self):
        args=fixture('surface_cut');result=self.check(args,'SYNTHETIC_DEMP_CONTRACT_CONSISTENT')
        self.assertEqual(result['center_outside_samples'],0)
        self.assertEqual(result['sphere_cut_samples'],42)
        self.assertFalse(result['demp02_closed'])

    def test_12_same_endpoints_do_not_hide_declared_middle_outside_sample(self):
        args=fixture();geometry=args[1][2]['payload']['geometry']
        geometry['samples'][1]['center_region']='OUTSIDE'
        self.check(args,'REJECTED')
        geometry['center_outside_claim']='SAMPLE_RECORDED'
        result=self.check(args,'SYNTHETIC_DEMP_CONTRACT_CONSISTENT')
        self.assertEqual(result['center_outside_samples'],1)
        self.assertEqual(result['continuity'],'CONTINUITY_UNCONFIRMED')

    def test_13_sample_gaps_unknown_labels_and_claimed_continuity_cannot_certify_no_leak(self):
        for change in ('missing_frame','unknown','continuity','physical_mesh'):
            args=fixture();geometry=args[1][2]['payload']['geometry']
            if change=='missing_frame':geometry['samples'].pop(1)
            elif change=='unknown':geometry['samples'][1]['center_region']='UNKNOWN'
            elif change=='continuity':geometry['continuity']='PROVEN_NO_CROSSING'
            else:geometry['profile']='ACTUAL_STL_PBC_QUALIFIED'
            with self.subTest(change=change):
                self.check(args,'NOT_COMPUTED' if change in ('missing_frame','unknown') else 'REJECTED')

    def test_14_old_attempt_or_changed_wall_history_is_not_same_declared_stage(self):
        for change in ('attempt','mesh','wall','history','damping'):
            args=fixture();payload=args[1][4]['payload']
            if change=='attempt':payload['binding']['identity']['attempt_id']='old_attempt'
            elif change=='damping':payload['global_damping_definition_id']='global_COMPRESSION'
            else:payload[change+'_id']='other_'+change
            with self.subTest(change=change):self.check(args,'REJECTED')

    def test_15_same_load_name_cannot_hide_different_static_state_contract(self):
        for field in ('pressure_definition_id','area_definition_id','units_definition_id',
                      'window_definition_id','history_policy_id','damping_policy_id','metric_operator_id'):
            args=fixture();args[0]['cases'][1]['static_state_contract'][field]='other_rule'
            refreeze(args[0],args[2])
            with self.subTest(field=field):self.check(args,'REJECTED')

    def test_16_same_contract_labels_are_not_enough_if_ra_packet_is_other_state(self):
        args=fixture();args[1][11]['payload']['static_state_contract']['stage']='COMPRESSION'
        self.check(args,'REJECTED')
        args=fixture();args[1][11]['payload']['static_state_contract']=None
        self.check(args,'NOT_COMPUTED')

    def test_17_case_names_without_state_definition_or_same_n_requirement_are_invalid(self):
        args=fixture();args[0]['cases'][1]['static_state_contract']=None
        refreeze(args[0],args[2]);self.check(args,'REJECTED')
        args=fixture();args[0]['comparison']['n_matching']='FORCE_EQUAL_N'
        refreeze(args[0],args[2]);self.check(args,'REJECTED')

    def test_18_50kg_project_label_cannot_be_used_as_compression_load_conversion(self):
        for key,value in (('meaning','COMPRESSIVE_MASS'),('compression_load_conversion','50KG_EQUALS_300MPA'),
                          ('exact_batch_meaning','MEASURED_LOAD')):
            args=fixture();args[0]['historical_label'][key]=value;refreeze(args[0],args[2])
            with self.subTest(key=key):self.check(args,'REJECTED')

    def test_19_nominal_model_diameter_is_not_real_psd_or_actual_measurement(self):
        args=fixture();args[0]['cases'][0]['diameter']['experimental_PSD']='CONFIRMED'
        refreeze(args[0],args[2]);self.check(args,'REJECTED')
        args=fixture();args[0]['cases'][0]['diameter']['value']=[1,1]
        refreeze(args[0],args[2]);self.check(args,'REJECTED')

    def test_20_settled_d9_prime_policy_is_preserved_without_claiming_measurement(self):
        args=fixture();args[0]['d9_prime']['calibration_estimand']='EPSILON_UNION'
        refreeze(args[0],args[2]);self.check(args,'REJECTED')
        args=fixture();args[0]['actual_facts']['force_balance_budget']=[2,100]
        refreeze(args[0],args[2]);self.check(args,'REJECTED')

    def test_21_hash_and_declared_order_do_not_allow_plan_only_replacement(self):
        args=fixture();args[0]['revision']=2;self.check(args,'REJECTED')
        args=fixture();args[2]['freeze_ordinal']=2;self.check(args,'REJECTED')
        args=fixture();args[0]['source_manifest']['qualification_matrix_pin']='e'*40
        refreeze(args[0],args[2]);self.check(args,'REJECTED')

    def test_22_unknown_fields_status_receipts_and_actual_authority_are_rejected(self):
        args=fixture();args[1][0]={'status':'PASS','rc':0};self.check(args,'REJECTED')
        args=fixture();args[1][0]['payload']['execution_go']=True;self.check(args,'REJECTED')
        args=fixture();args[0]['purpose']='ACTUAL_QUALIFICATION';refreeze(args[0],args[2]);self.check(args,'REJECTED')

    def test_23_inputs_are_unchanged(self):
        args=fixture('surface_cut');before=copy.deepcopy(args)
        self.check(args,'SYNTHETIC_DEMP_CONTRACT_CONSISTENT')
        self.assertEqual(args,before)

    def test_24_exact_types_and_key_types_do_not_invoke_hooks(self):
        calls=[]
        class TrapDict(dict):
            def __getitem__(self,key):calls.append('getitem');raise AssertionError('hook')
        class TrapKey(str):
            def __hash__(self):calls.append('hash');return str.__hash__(self)
            def __eq__(self,other):calls.append('eq');return str.__eq__(self,other)
        args=list(fixture());args[0]=TrapDict(args[0]);self.check(args,'REJECTED')
        args=fixture();value=args[0].pop('schema');args[0][TrapKey('schema')]=value;calls.clear()
        self.check(args,'REJECTED');self.assertEqual(calls,[])
        args=fixture();args[1][0]['payload']['declared_inventory'][0]['id']=True
        self.check(args,'REJECTED')

    def test_25_self_consistent_stage_windows_cannot_run_backward_or_overlap(self):
        for first in (0,8):
            args=fixture();payload=args[1][3]['payload']
            payload['binding'].update(start_step=first,end_step=first+2)
            for channel in payload['channels'].values():
                channel['binding']=copy.deepcopy(payload['binding'])
            for i,sample in enumerate(payload['geometry']['samples']):sample['step']=first+i
            with self.subTest(first_step=first):self.check(args,'REJECTED')


if __name__=='__main__':
    unittest.main()
