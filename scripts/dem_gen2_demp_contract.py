"""DEMP declaration/metadata consistency only; Q-DEMP-1/2/3 preparation.

No force or geometry calculator, raw-data reader, source authenticator, physical
qualification or actual same-state comparison is implemented here.
"""
from fractions import Fraction
import hashlib
import json


QUALIFICATION_MATRIX_PIN='b7fbe749ea8ffa3151b3e768de445c572940c43d'
STAGES=('INSERTION','STABILIZATION','COMPRESSION','SERVO','RA_END','UNLOADING','POST_SEPARATION')
VECTOR_ROLES=('plate_reaction','global_damping','contact_damping','gravity','inertia','force_balance','torque_balance')
SCALAR_ROLES=('translational_ke','rotational_ke')
_STATE={'stage','pressure_definition_id','area_definition_id','units_definition_id',
        'window_definition_id','history_policy_id','damping_policy_id',
        'inventory_operator_id','metric_operator_id'}
_IDENTITY={'run_id','attempt_id','bed_id','arm_id','definition_id'}


class _NotComputed(ValueError):
    pass


def _dict(value,keys):
    # Check key type before set/hash/equality can invoke a subclass hook.
    if type(value) is not dict or any(type(k) is not str for k in value):
        raise ValueError('EXACT_DICT_AND_STRING_KEYS_REQUIRED')
    if set(value)!=keys:
        raise ValueError('EXACT_FIELDS_REQUIRED')
    return value


def _list(value,minimum,maximum):
    if type(value) is not list or not minimum<=len(value)<=maximum:
        raise ValueError('BOUNDED_EXACT_LIST_REQUIRED')
    return value


def _int(value,minimum=0,maximum=1000000000):
    if type(value) is not int or not minimum<=value<=maximum:
        raise ValueError('BOUNDED_EXACT_INTEGER_REQUIRED')
    return value


def _token(value):
    if (type(value) is not str or not 1<=len(value)<=128 or not value.isascii()
            or not value[0].isalpha() or any(not(c.isalnum() or c in '_-') for c in value)):
        raise ValueError('SYNTHETIC_TOKEN_REQUIRED')
    return value


def _one(value,allowed):
    if type(value) is not str or value not in allowed:
        raise ValueError('UNSUPPORTED_DECLARATION')
    return value


def _hex(value,length=64):
    if type(value) is not str or len(value)!=length or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('LOWERCASE_DIGEST_REQUIRED')
    return value


def _ratio(value):
    _list(value,2,2)
    return Fraction(_int(value[0],1),_int(value[1],1))


def _canonical(value):
    def inspect(item,ancestors,depth):
        if depth>48:
            raise ValueError('JSON_DEPTH_LIMIT')
        if type(item) in (type(None),bool,int,str):
            return
        if type(item) not in (dict,list) or id(item) in ancestors:
            raise ValueError('EXACT_ACYCLIC_METADATA_REQUIRED')
        ancestors=ancestors|{id(item)}
        if type(item) is dict:
            for key,member in item.items():
                if type(key) is not str:
                    raise ValueError('EXACT_STRING_KEYS_REQUIRED')
                inspect(member,ancestors,depth+1)
        else:
            for member in item:
                inspect(member,ancestors,depth+1)
    inspect(value,set(),0)
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')


def _identity(value):
    _dict(value,_IDENTITY)
    for member in value.values():_token(member)
    return dict(value)


def _state(value):
    _dict(value,_STATE)
    _one(value['stage'],('RA_END',))
    for key,member in value.items():
        if key!='stage':_token(member)
    return dict(value)


def _roster(value):
    result={}
    for item in _list(value,1,256):
        _dict(item,{'id','type','radius_definition_id','mass_definition_id'})
        particle=_int(item['id'],1)
        if particle in result:raise ValueError('DUPLICATE_DECLARED_PARTICLE')
        result[particle]=(_int(item['type'],1),_token(item['radius_definition_id']),
                          _token(item['mass_definition_id']))
    return result


def _prepare(plan,context):
    _dict(context,{'schema','qualification_matrix_pin','expected_plan_sha256',
                   'freeze_ordinal','first_evidence_ordinal'})
    _one(context['schema'],('DEMP_SYNTHETIC_FROZEN_CONTEXT_V1',))
    _one(context['qualification_matrix_pin'],(QUALIFICATION_MATRIX_PIN,))
    expected=_hex(context['expected_plan_sha256'])
    if _int(context['freeze_ordinal'])>=_int(context['first_evidence_ordinal']):
        raise ValueError('DECLARED_ORDER_NOT_BEFORE_EVIDENCE')
    _dict(plan,{'schema','purpose','assumptions','plan_id','revision','source_manifest',
                'historical_label','d9_prime','stages','cases','comparison','geometry','actual_facts'})
    _one(plan['schema'],('DEM_GEN2_DEMP_SYNTHETIC_CONTRACT_V1',))
    _one(plan['purpose'],('SYNTHETIC_PREPARATION',))
    assumptions=_list(plan['assumptions'],3,3)
    if any(type(a) is not str for a in assumptions) or assumptions!=['Q-DEMP-1','Q-DEMP-2','Q-DEMP-3']:
        raise ValueError('ASSUMPTIONS_REQUIRED')
    _token(plan['plan_id']);_int(plan['revision'],1)
    manifest=_dict(plan['source_manifest'],{'qualification_matrix_pin','producer_pin','consumer_pin','definition_pin'})
    _one(manifest['qualification_matrix_pin'],(QUALIFICATION_MATRIX_PIN,))
    for key in ('producer_pin','consumer_pin','definition_pin'):_hex(manifest[key],40)
    label=_dict(plan['historical_label'],{'label','meaning','exact_batch_meaning','compression_load_conversion'})
    for key,expected_value in {'label':'50kg/batch','meaning':'PROJECT_LABEL_ONLY',
        'exact_batch_meaning':'UNKNOWN','compression_load_conversion':'NOT_ESTABLISHED'}.items():
        _one(label[key],(expected_value,))
    d9=_dict(plan['d9_prime'],{'scope','calibration_estimand','declared_TD','external_target_percent','epsilon_union'})
    _one(d9['scope'],('PURE_SE_300MPA_PLUS_RELAXATION_END',))
    _one(d9['calibration_estimand'],('MASS_BASED_EPSILON_SPHERE',))
    _one(d9['epsilon_union'],('RECORD_ONLY',))
    if _ratio(d9['declared_TD'])!=Fraction(41,25):raise ValueError('SETTLED_TD_POLICY_CHANGED')
    target=_list(d9['external_target_percent'],2,2)
    if [_int(v) for v in target]!=[10,13]:raise ValueError('SETTLED_EXTERNAL_TARGET_CHANGED')
    stages={}
    for expected_stage,item in zip(STAGES,_list(plan['stages'],7,7)):
        _dict(item,{'stage','global_damping','contact_damping','force_representation',
            'force_units_id','torque_units_id','energy_units_id','gamma_units_id','evidence_scope'})
        _one(item['stage'],(expected_stage,))
        for role in ('global_damping','contact_damping'):
            declaration=_dict(item[role],{'policy','definition_id','model_id'})
            _one(declaration['policy'],('EXPLICIT_STAGE',))
            _token(declaration['definition_id']);_token(declaration['model_id'])
        if (item['global_damping']['model_id']==item['contact_damping']['model_id']
                or item['global_damping']['definition_id']==item['contact_damping']['definition_id']):
            raise ValueError('GLOBAL_AND_CONTACT_DAMPING_MUST_REMAIN_SEPARATE')
        _one(item['force_representation'],('SIGNED_VECTOR_COMPONENTS',))
        _one(item['evidence_scope'],('DECLARATIONS_ONLY_NO_FORCE_RECALC',))
        for key in ('force_units_id','torque_units_id','energy_units_id','gamma_units_id'):_token(item[key])
        stages[expected_stage]=item
    comparison=_dict(plan['comparison'],{'target_static_state','recipe_definition_id','n_matching',
        'actual_state_qualification','missing_policy','retry_policy'})
    target_state=_state(comparison['target_static_state'])
    recipe=_token(comparison['recipe_definition_id'])
    for key,expected_value in {'n_matching':'NOT_REQUIRED','actual_state_qualification':'NOT_RUN',
        'missing_policy':'KEEP_PLANNED','retry_policy':'NONE'}.items():_one(comparison[key],(expected_value,))
    cases={};diameters=set()
    for item in _list(plan['cases'],2,2):
        _dict(item,{'case_id','diameter','identity','recipe_definition_id','declared_load_label',
            'static_state_contract','inventory_id','reference_inventory','mesh_id','wall_id','history_id'})
        case_id=_token(item['case_id'])
        if case_id in cases:raise ValueError('DUPLICATE_CASE')
        diameter=_dict(item['diameter'],{'value','unit','kind','experimental_PSD'})
        _one(diameter['unit'],('um',));_one(diameter['kind'],('DECLARED_NOMINAL_MONODISPERSE_DIAMETER',))
        _one(diameter['experimental_PSD'],('UNKNOWN',))
        number=_ratio(diameter['value'])
        if number in diameters or number not in (Fraction(7,10),Fraction(1)):
            raise ValueError('EXACT_NOMINAL_DIAMETER_CASES_REQUIRED')
        diameters.add(number)
        identity=_identity(item['identity'])
        if _token(item['recipe_definition_id'])!=recipe:raise ValueError('RECIPE_RULE_MISMATCH')
        _token(item['declared_load_label'])
        state=_state(item['static_state_contract'])
        if state!=target_state:raise ValueError('FULL_STATIC_STATE_CONTRACT_MISMATCH')
        for key in ('inventory_id','mesh_id','wall_id','history_id'):_token(item[key])
        cases[case_id]=dict(declaration=item,identity=identity,state=state,
                           roster=_roster(item['reference_inventory']))
    geometry=_dict(plan['geometry'],{'profile','center_and_surface','continuity','actual_mesh_PBC_qualification'})
    for key,expected_value in {'profile':'DECLARED_CLASSIFICATION_ONLY','center_and_surface':'SEPARATE_FIELDS',
        'continuity':'CONTINUITY_UNCONFIRMED','actual_mesh_PBC_qualification':'NOT_RUN'}.items():
        _one(geometry[key],(expected_value,))
    actual=_dict(plan['actual_facts'],{'gamma','force_balance_budget','geometry_tolerance','mesh_PBC',
        'continuous_trajectory','static_pressure_area','comparison_roster','registration_approval','qualification_receipt'})
    if any(value is not None for value in actual.values()):raise ValueError('ACTUAL_FACTS_MUST_REMAIN_UNSELECTED')
    if hashlib.sha256(_canonical(plan)).hexdigest()!=expected:raise ValueError('EXTERNAL_PLAN_DIGEST_MISMATCH')
    return dict(cases=cases,stages=stages,planned={(case,stage) for case in cases for stage in STAGES})


def _binding(value,case,case_id,stage):
    _dict(value,{'identity','stage','window_id','start_step','end_step','frame_ids','inventory_id'})
    if _identity(value['identity'])!=case['identity']:raise ValueError('CASE_IDENTITY_MISMATCH')
    _one(value['stage'],(stage,))
    if _token(value['window_id'])!=case_id+'_'+stage:raise ValueError('STAGE_WINDOW_ID_MISMATCH')
    start,end=_int(value['start_step']),_int(value['end_step'])
    frames=_list(value['frame_ids'],1,32)
    for frame in frames:_token(frame)
    if len(set(frames))!=len(frames) or end-start+1!=len(frames):
        raise ValueError('EXACT_DECLARED_FRAME_WINDOW_REQUIRED')
    if _token(value['inventory_id'])!=case['declaration']['inventory_id']:raise ValueError('INVENTORY_ID_MISMATCH')
    return value


def _payload(payload,case,case_id,stage,stage_plan):
    _dict(payload,{'binding','channels','declared_inventory','mesh_id','wall_id','history_id',
        'global_damping_definition_id','contact_damping_definition_id','static_state_contract','geometry'})
    binding=_binding(payload['binding'],case,case_id,stage)
    for key in ('mesh_id','wall_id','history_id'):
        if _token(payload[key])!=case['declaration'][key]:raise ValueError('WALL_OR_HISTORY_IDENTITY_MISMATCH')
    for role in ('global_damping','contact_damping'):
        if _token(payload[role+'_definition_id'])!=stage_plan[role]['definition_id']:
            raise ValueError('STAGE_DAMPING_DEFINITION_MISMATCH')
    if _roster(payload['declared_inventory'])!=case['roster']:raise ValueError('FULL_DECLARED_ROSTER_MISMATCH')
    channels=payload['channels']
    if type(channels) is not dict or any(type(k) is not str for k in channels):
        raise ValueError('EXACT_CHANNEL_MAPPING_REQUIRED')
    required=set(VECTOR_ROLES+SCALAR_ROLES)
    if not required.issubset(channels):raise _NotComputed('REQUIRED_CHANNEL_DECLARATION_MISSING')
    _dict(channels,required)
    for role,channel in channels.items():
        _dict(channel,{'role','representation','units_id','binding','source_kind','source_id','source_sha256','value_access'})
        _one(channel['role'],(role,))
        _one(channel['representation'],('SIGNED_VECTOR_COMPONENTS' if role in VECTOR_ROLES else 'SCALAR_DEFINITION',))
        unit_key='torque_units_id' if role=='torque_balance' else 'energy_units_id' if role in SCALAR_ROLES else 'force_units_id'
        if _token(channel['units_id'])!=stage_plan[unit_key]:raise ValueError('CHANNEL_UNIT_DECLARATION_MISMATCH')
        if _binding(channel['binding'],case,case_id,stage)!=binding:raise ValueError('SAME_DECLARED_FRAME_REQUIRED')
        _one(channel['source_kind'],('SYNTHETIC_METADATA_ONLY',));_one(channel['value_access'],('NOT_READ',))
        _token(channel['source_id']);_hex(channel['source_sha256'])
    if stage=='RA_END':
        if payload['static_state_contract'] is None:raise _NotComputed('RA_STATIC_STATE_CONTRACT_MISSING')
        if _state(payload['static_state_contract'])!=case['state']:raise ValueError('RA_STATE_CONTRACT_MISMATCH')
    elif payload['static_state_contract'] is not None:
        raise ValueError('NON_RA_STAGE_IS_NOT_STATIC_ENDPOINT')
    geometry=_dict(payload['geometry'],{'profile','continuity','samples','center_outside_claim','sphere_cut_claim'})
    _one(geometry['profile'],('DECLARED_CLASSIFICATION_ONLY',))
    _one(geometry['continuity'],('CONTINUITY_UNCONFIRMED',))
    samples=_list(geometry['samples'],0,32)
    if len(samples)<len(binding['frame_ids']):raise _NotComputed('CLASSIFICATION_FRAME_MISSING')
    if len(samples)!=len(binding['frame_ids']):raise ValueError('EXTRA_CLASSIFICATION_FRAME')
    outside=cuts=0
    for index,sample in enumerate(samples):
        _dict(sample,{'frame_id','step','center_region','sphere_relation'})
        if (_token(sample['frame_id'])!=binding['frame_ids'][index]
                or _int(sample['step'])!=binding['start_step']+index):
            raise ValueError('CLASSIFICATION_WINDOW_MISMATCH')
        if sample['center_region'] is None or sample['sphere_relation'] is None:
            raise _NotComputed('CLASSIFICATION_UNKNOWN')
        center=_one(sample['center_region'],('INSIDE','OUTSIDE','UNKNOWN'))
        sphere=_one(sample['sphere_relation'],('UNCUT','CUT','UNKNOWN'))
        if center=='UNKNOWN' or sphere=='UNKNOWN':raise _NotComputed('CLASSIFICATION_UNKNOWN')
        outside+=center=='OUTSIDE';cuts+=sphere=='CUT'
    for field,count in (('center_outside_claim',outside),('sphere_cut_claim',cuts)):
        _one(geometry[field],('NONE_RECORDED','SAMPLE_RECORDED'))
        if geometry[field]!=('SAMPLE_RECORDED' if count else 'NONE_RECORDED'):
            raise ValueError('DECLARED_CLASSIFICATION_CLAIM_MISMATCH')
    return outside,cuts


def _report(status,reason,prepared=None,complete=0,missing=0,failed=0,partial=0,outside=0,cuts=0):
    return dict(status=status,reason=reason,
        planned_packets=len(prepared['planned']) if prepared else 0,
        complete_packets=complete,missing_packets=missing,failed_packets=failed,partial_packets=partial,
        declared_inventory_counts={k:len(v['roster']) for k,v in prepared['cases'].items()} if prepared else {},
        center_outside_samples=outside,sphere_cut_samples=cuts,continuity='CONTINUITY_UNCONFIRMED',
        physical_ready=False,execution_go=False,gate_write=False,registration_complete=False,
        source_authenticated=False,demp01_closed=False,demp02_closed=False,
        actual_state_comparable=False,actual_qualification='NOT_RUN',research_results=0,
        assumptions=['Q-DEMP-1','Q-DEMP-2','Q-DEMP-3'],whole_status='HOLD')


def validate_demp_contract(plan,packets,context):
    """Check CASE_GLOBAL_DECLARATION metadata; never close DEMP-01/02."""
    prepared=None
    try:
        prepared=_prepare(plan,context)
        received={}
        windows={}
        outside=cuts=0
        for packet in _list(packets,0,28):
            _dict(packet,{'case_id','stage','status','payload','failure_code'})
            case_id,stage=_token(packet['case_id']),_token(packet['stage'])
            key=(case_id,stage)
            if key not in prepared['planned'] or key in received:raise ValueError('UNPLANNED_OR_DUPLICATE_PACKET')
            status=_one(packet['status'],('PRESENT','MISSING','FAILED','PARTIAL'))
            if status=='PRESENT':
                if packet['failure_code'] is not None:raise ValueError('PRESENT_PACKET_WITH_FAILURE')
                c,s=_payload(packet['payload'],prepared['cases'][case_id],case_id,stage,prepared['stages'][stage])
                outside+=c;cuts+=s
                binding=packet['payload']['binding']
                windows[key]=(binding['start_step'],binding['end_step'])
            else:
                if packet['payload'] is not None:raise ValueError('NONCOMPLETE_PACKET_WITH_PAYLOAD')
                _token(packet['failure_code'])
            received[key]=status
        for case_id in prepared['cases']:
            previous_end=None
            for stage in STAGES:
                bounds=windows.get((case_id,stage))
                if bounds is None:continue
                start,end=bounds
                if previous_end is not None and start<=previous_end:
                    raise ValueError('DECLARED_STAGE_WINDOWS_OVERLAP_OR_RUN_BACKWARD')
                previous_end=end
        complete=sum(value=='PRESENT' for value in received.values())
        missing=len(prepared['planned'])-len(received)+sum(value=='MISSING' for value in received.values())
        failed=sum(value=='FAILED' for value in received.values())
        partial=sum(value=='PARTIAL' for value in received.values())
        status='INCOMPLETE' if missing or failed or partial else 'SYNTHETIC_DEMP_CONTRACT_CONSISTENT'
        return _report(status,'DECLARATION_METADATA_ONLY',prepared,complete,missing,failed,partial,outside,cuts)
    except _NotComputed as error:
        return _report('NOT_COMPUTED',error.args[0],prepared)
    except (KeyError,TypeError,ValueError,OverflowError,RecursionError):
        return _report('REJECTED','INVALID_DEMP_DECLARATION_CONTRACT',prepared)
