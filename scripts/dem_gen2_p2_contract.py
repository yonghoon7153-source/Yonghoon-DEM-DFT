"""Pure-data P2 native contract and separation diagnostics, Q-P2-1/2 only.

Revalidates original synthetic S0/LIVE inputs. Never reads files, starts an
engine, changes a plate, or grants actual registration/physical authority.
"""
from fractions import Fraction
import hashlib
import json
import math

from dem_gen2_s0_contract import decode_s0


S0_CONTRACT_PIN = 'f4647f2b7c218a6df7def3292c092273f9d4e35f'
ACTIVE = ['P2_NATIVE_PARAMS_V1', 'P2_S0_BOUNDARY_V1', 'P2_H0_RATIO_V1',
          'P2_EXPLICIT_GRAVITY_V1', 'P2_PHYSICAL_WINDOW_V1',
          'P2_SINGLE_ATTEMPT_V1', 'P2_TWO_ZERO_CLEAR_FOUR_POST_V1']
_IDENTITY = {'run_id','bed_id','arm_id','attempt_id','definition_id','unit_system_id'}
_WINDOW = {'kind','window_index','identity','plan_sha256','s0_id','s0_sha256',
    'inventory_id','mesh_id','wall_id','history_id','phase','plate_mode','lift_index',
    'start_step','end_step','gravity','complete','samples'}
_EVENT = {'kind','action','identity','plan_sha256','s0_id','s0_sha256',
    'after_window_index','step','mesh_id','wall_id','history_id','position_z'}
_SAMPLE = {'step','contact_count','contacts_complete','ke','surface_height',
           'pressure','plate_z','inventory_complete','particles'}


class _Outcome(ValueError):
    def __init__(self,status,reason):
        self.status=status
        super().__init__(reason)


def _dict(value,keys):
    if type(value) is not dict or any(type(k) is not str for k in value):
        raise ValueError('EXACT_DICT_AND_STRING_KEYS_REQUIRED')
    if set(value)!=keys:
        raise ValueError('EXACT_FIELDS_REQUIRED')
    return value


def _token(value):
    if (type(value) is not str or not 1<=len(value)<=128 or not value.isascii()
            or not value[0].isalpha() or any(not(c.isalnum() or c in '_-') for c in value)):
        raise ValueError('SYNTHETIC_TOKEN_REQUIRED')
    return value


def _one(value,choices):
    if type(value) is not str or value not in choices:
        raise ValueError('UNSUPPORTED_DECLARATION')
    return value


def _int(value,minimum=0,maximum=1000000000):
    if type(value) is not int or not minimum<=value<=maximum:
        raise ValueError('EXACT_BOUNDED_INTEGER_REQUIRED')
    return value


def _number(value,nonnegative=False):
    if type(value) not in (int,float):
        raise ValueError('FINITE_BUILTIN_NUMBER_REQUIRED')
    result=float(value)
    if not math.isfinite(result) or (nonnegative and result<0):
        raise ValueError('FINITE_BUILTIN_NUMBER_REQUIRED')
    return result


def _rat(value,signed=False,zero=False):
    if type(value) is not list or len(value)!=2:
        raise ValueError('EXACT_RATIONAL_REQUIRED')
    n,d=value
    if type(n) is not int or type(d) is not int or d<=0 or abs(n)>10**18 or d>10**18:
        raise ValueError('BOUNDED_EXACT_RATIONAL_REQUIRED')
    if not signed and n<(0 if zero else 1):
        raise ValueError('RATIONAL_DOMAIN')
    return Fraction(n,d)


def _pair(value):
    return [value.numerator,value.denominator]


def _hex(value,length=64):
    if type(value) is not str or len(value)!=length or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('LOWERCASE_DIGEST_REQUIRED')
    return value


def _canonical(value):
    def inspect(item,ancestors,depth):
        if depth>48:
            raise ValueError('JSON_DEPTH_LIMIT')
        kind=type(item)
        if kind in (type(None),bool,int,str):
            return
        if kind is float:
            _number(item)
            return
        if kind not in (dict,list) or id(item) in ancestors:
            raise ValueError('EXACT_ACYCLIC_JSON_REQUIRED')
        ancestors=ancestors|{id(item)}
        if kind is dict:
            for key,member in item.items():
                if type(key) is not str:
                    raise ValueError('EXACT_STRING_KEYS_REQUIRED')
                inspect(member,ancestors,depth+1)
        else:
            for member in item:
                inspect(member,ancestors,depth+1)
    inspect(value,set(),0)
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _identity(value,expected=None):
    _dict(value,_IDENTITY)
    for member in value.values():
        _token(member)
    if expected is not None and value!=expected:
        raise ValueError('IDENTITY_MISMATCH')
    return dict(value)


def _gravity(value):
    _dict(value,{'policy','variant','vector','basis_id'})
    _one(value['policy'],('EXPLICIT_VECTOR',))
    _one(value['variant'],('MAIN','BRIDGE'))
    _token(value['basis_id'])
    if type(value['vector']) is not list or len(value['vector'])!=3:
        raise ValueError('EXPLICIT_GRAVITY_VECTOR_REQUIRED')
    for member in value['vector']:
        _rat(member,signed=True)
    return json.loads(_canonical(value))


def _inventory(value):
    if type(value) is not list or not 1<=len(value)<=256:
        raise ValueError('SMALL_COMPLETE_INVENTORY_REQUIRED')
    result={}
    for particle in value:
        _dict(particle,{'id','type','radius','mass'})
        particle_id=_int(particle['id'],1)
        kind=_int(particle['type'],1)
        radius,mass=_number(particle['radius']),_number(particle['mass'])
        if radius<=0 or mass<=0 or particle_id in result:
            raise ValueError('INVALID_PARTICLE_INVENTORY')
        result[particle_id]=(kind,radius,mass)
    return result


def _report(status,reason,compiled=None,events=None):
    events=events or {}
    return dict(status=status,reason=reason,compiled=compiled,
        primary_status='SELECTION_UNRESOLVED',
        trajectory_status='POST_DIAGNOSTIC_CANDIDATE' if status=='SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE' else 'NOT_COMPUTED',
        first_pressure_crossing=events.get('first_pressure_crossing'),
        second_zero_window_end=events.get('second_zero_window_end'),
        plate_clear_event=events.get('plate_clear_event'),post_end=events.get('post_end'),
        checked_post_windows=events.get('checked_post_windows',0),
        physical_ready=False,execution_go=False,transition_authorized=False,
        gate_write=False,operational_seal_modified=False,registration_complete=False,
        source_authenticated=False,hidden_history_qualified=False,
        actual_T0='NOT_RUN',actual_T11='NOT_RUN',actual_T12='NOT_RUN',
        actual_S0=None,actual_unload_case=None,research_results=0,
        assumptions=['Q-P2-1','Q-P2-2'],whole_status='HOLD')


def _compile(plan,s0_bytes,context):
    _dict(context,{'schema','s0_contract_pin','expected_plan_sha256','expected_s0_sha256',
                  's0_contract','live_plan','servo_frames','ra_frames'})
    _one(context['schema'],('SYNTHETIC_P2_S0_SOURCE_CONTEXT_V1',))
    _one(context['s0_contract_pin'],(S0_CONTRACT_PIN,))
    expected_plan=_hex(context['expected_plan_sha256'])
    expected_s0=_hex(context['expected_s0_sha256'])
    if type(s0_bytes) is not bytes or not 1<=len(s0_bytes)<=1048576:
        raise ValueError('EXACT_BOUNDED_S0_BYTES_REQUIRED')
    archive_hash=_digest(s0_bytes)
    if archive_hash!=expected_s0:
        raise ValueError('EXTERNAL_S0_BYTES_MISMATCH')
    envelope=decode_s0(s0_bytes,context['s0_contract'],context['live_plan'],
                       context['servo_frames'],context['ra_frames'])
    boundary=envelope['boundary_candidate']
    _dict(plan,{'schema','purpose','protocol','assumptions','plan_id','revision','identity','header','params'})
    _one(plan['schema'],('DEM_GEN2_P2_NATIVE_SYNTHETIC_PLAN_V1',))
    _one(plan['purpose'],('SYNTHETIC_PREPARATION',))
    _one(plan['protocol'],('P2',))
    _token(plan['plan_id']);_int(plan['revision'],1)
    if (type(plan['assumptions']) is not list or any(type(v) is not str for v in plan['assumptions'])
            or plan['assumptions']!=['Q-P2-1','Q-P2-2']):
        raise ValueError('ASSUMPTIONS_REQUIRED')
    identity=_identity(plan['identity'],boundary['identity'])
    header=_dict(plan['header'],{'schema','protocol','profile','active_definitions',
        'producer_pin','consumer_definition_pin','s0_contract_pin','s0_sha256','params_sha256','source_mapping'})
    _one(header['schema'],('P2_NATIVE_ACTIVE_HEADER_V1',))
    _one(header['protocol'],('P2',));_one(header['profile'],('P2_NATIVE_ULPR_V1',))
    if (type(header['active_definitions']) is not list
            or any(type(v) is not str for v in header['active_definitions'])
            or header['active_definitions']!=ACTIVE):
        raise ValueError('NATIVE_ACTIVE_DEFINITIONS_REQUIRED')
    if _hex(header['producer_pin'],40)!=boundary['source_identity']['producer_pin']:
        raise ValueError('PRODUCER_PIN_MISMATCH')
    _hex(header['consumer_definition_pin'],40)
    _one(header['s0_contract_pin'],(S0_CONTRACT_PIN,))
    if _hex(header['s0_sha256'])!=archive_hash:
        raise ValueError('HEADER_S0_MISMATCH')
    mapping=_dict(header['source_mapping'],{'atom_profile','pair_reference_sha256','wall_reference_sha256'})
    _one(mapping['atom_profile'],('ATOM16',))
    for role in ('pair','wall'):
        if _hex(mapping[role+'_reference_sha256'])!=_digest(_canonical(context['s0_contract'][role+'_reference'])):
            raise ValueError('S0_MAPPING_MISMATCH')
    params=_dict(plan['params'],{'schema','s0_id','h0_basis','bottom_z','h0',
        'increment_ratio_A','increment_ratio_B','lift_cap_ratio','unload_case','primary_selection',
        'units','gravity','pbc_policy','time','pressure_crossing_threshold','max_ke',
        'max_surface_drift','zero_windows','post_windows','clear_action'})
    _one(params['schema'],('P2_NATIVE_ULPR_PARAMS_V1',))
    if _token(params['s0_id'])!=envelope['s0_id']:
        raise ValueError('S0_ID_MISMATCH')
    _one(params['h0_basis'],('S0_PLATE_Z_MINUS_DECLARED_BOTTOM',))
    bottom=_rat(params['bottom_z'],signed=True)
    h0=_rat(params['h0'])
    if h0!=Fraction(_number(boundary['plate']['position'][2]))-bottom:
        raise ValueError('S0_H0_MISMATCH')
    ratio_a,ratio_b,cap=(_rat(params[k]) for k in ('increment_ratio_A','increment_ratio_B','lift_cap_ratio'))
    if max(ratio_a,ratio_b)>cap:
        raise ValueError('INCREMENT_EXCEEDS_LIFT_CAP')
    selected=_one(params['unload_case'],('A','B'))
    increment=h0*(ratio_a if selected=='A' else ratio_b)
    _one(params['primary_selection'],('SELECTION_UNRESOLVED',))
    units=_dict(params['units'],{'length','time','pressure','energy','gravity'})
    for key,value in {'length':'TOY_LENGTH','time':'s','pressure':'TOY_PRESSURE',
                      'energy':'TOY_ENERGY','gravity':'TOY_ACCELERATION'}.items():
        _one(units[key],(value,))
    gravity=_gravity(params['gravity'])
    _one(params['pbc_policy'],('NONE','XY_PERIODIC'))
    times=_dict(params['time'],{'dt_seconds','dt_half_seconds','window_seconds',
                              'window_steps','half_window_steps','grid_choice'})
    dt,half_dt,window=(_rat(times[k]) for k in ('dt_seconds','dt_half_seconds','window_seconds'))
    steps,half_steps=_int(times['window_steps'],1,256),_int(times['half_window_steps'],1,256)
    if half_dt*2!=dt or half_steps!=2*steps or dt*steps!=window or half_dt*half_steps!=window:
        raise ValueError('EXACT_PHYSICAL_WINDOW_AND_HALF_PAIR_REQUIRED')
    choice=_one(times['grid_choice'],('coarse','half'))
    if choice!=boundary['source_identity']['grid_choice']:
        raise ValueError('S0_GRID_CHOICE_MISMATCH')
    t11=context['live_plan']['t11_plan']
    scale=_rat(t11['units']['physical_seconds_per_deck_time'])
    if (dt!=_rat(t11['time']['dt_deck'])*scale
            or half_dt!=_rat(t11['time']['dt_half_deck'])*scale):
        raise ValueError('S0_T11_PHYSICAL_TIME_MISMATCH')
    threshold,max_ke,drift=(_rat(params[k],zero=True) for k in ('pressure_crossing_threshold','max_ke','max_surface_drift'))
    if _int(params['zero_windows'])!=2 or _int(params['post_windows'])!=4:
        raise ValueError('TWO_ZERO_AND_FOUR_POST_REQUIRED')
    _one(params['clear_action'],('MOVE_CLEAR',))
    if _hex(header['params_sha256'])!=_digest(_canonical(params)):
        raise ValueError('PARAMS_BYTES_MISMATCH')
    plan_hash=_digest(_canonical(plan))
    if plan_hash!=expected_plan:
        raise ValueError('EXTERNAL_PLAN_BYTES_MISMATCH')
    compiled=dict(h0=_pair(h0),selected_increment=_pair(increment),maximum_lift=_pair(h0*cap),
        window_steps=steps,half_window_steps=half_steps,
        selected_window_steps=steps if choice=='coarse' else half_steps,
        selected_dt_seconds=_pair(dt if choice=='coarse' else half_dt),
        s0_sha256=archive_hash,plan_sha256=plan_hash,s0_contract_pin=S0_CONTRACT_PIN,
        source_authenticated=False,physical_ready=False,registration_complete=False,
        pbc_qualification='NOT_QUALIFIED',actual_unload_case=None)
    return dict(public=compiled,identity=identity,boundary=boundary,
        s0_id=envelope['s0_id'],plan_sha256=plan_hash,s0_sha256=archive_hash,
        gravity=gravity,inventory=_inventory(boundary['reference_inventory']),
        base_plate_z=Fraction(_number(boundary['plate']['position'][2])),
        increment=increment,cap=h0*cap,threshold=threshold,max_ke=max_ke,max_surface_drift=drift)


def validate_p2_contract(plan,s0_bytes,context):
    """Validate native declarations against actual supplied synthetic S0 bytes."""
    try:
        prepared=_compile(plan,s0_bytes,context)
        return _report('SYNTHETIC_P2_CONTRACT_CONSISTENT','DECLARATIONS_AND_BYTES_ONLY',prepared['public'])
    except (KeyError,TypeError,ValueError,OverflowError,RecursionError):
        return _report('REJECTED','INVALID_NATIVE_P2_CONTRACT')


def _complete(value,reason):
    if value is None or value is False:
        raise _Outcome('NOT_COMPUTED',reason)
    if value is not True:
        raise ValueError('EXACT_COMPLETENESS_BOOL_REQUIRED')


def _stamp(record,prepared):
    _identity(record['identity'],prepared['identity'])
    for key in ('plan_sha256','s0_sha256'):
        if _hex(record[key])!=prepared[key]:
            raise ValueError('TRACE_BYTES_IDENTITY_MISMATCH')
    if _token(record['s0_id'])!=prepared['s0_id']:
        raise ValueError('TRACE_S0_ID_MISMATCH')
    for key in ('mesh_id','wall_id','history_id'):
        if _token(record[key])!=prepared['boundary']['plate'][key]:
            raise ValueError('TRACE_PLATE_HISTORY_MISMATCH')


def diagnose_p2_separation(plan,s0_bytes,context,trace):
    """Consume full synthetic step windows; never selects primary or moves plates."""
    events=dict(checked_post_windows=0)
    try:
        prepared=_compile(plan,s0_bytes,context)
        if type(trace) is not list or len(trace)>65:
            raise ValueError('SMALL_EXACT_TRACE_REQUIRED')
        w=prepared['public']['selected_window_steps']
        boundary=prepared['boundary']
        index=zero_count=last_lift=0
        clear_z=None
        previous_z=prepared['base_plate_z']
        post_heights=[]
        for record in trace:
            if type(record) is not dict or any(type(k) is not str for k in record):
                raise ValueError('EXACT_RECORD_REQUIRED')
            kind=_one(record.get('kind'),('WINDOW','PLATE_CLEAR'))
            if kind=='PLATE_CLEAR':
                _dict(record,_EVENT);_stamp(record,prepared)
                _one(record['action'],('MOVE_CLEAR',))
                if clear_z is not None or zero_count!=2:
                    raise ValueError('TWO_VALID_ZERO_WINDOWS_BEFORE_CLEAR_REQUIRED')
                end=events['second_zero_window_end']
                if (_int(record['after_window_index'])!=end['window_index']
                        or _int(record['step'])!=end['step']):
                    raise ValueError('CLEAR_EVENT_ORDER_MISMATCH')
                clear_z=_rat(record['position_z'],signed=True)
                if clear_z<=previous_z:
                    raise ValueError('PLATE_MUST_MOVE_UP_AFTER_SEPARATION')
                events['plate_clear_event']=dict(step=end['step'],after_window_index=end['window_index'],
                                                 action='MOVE_CLEAR',position_z=_pair(clear_z))
                continue
            _dict(record,_WINDOW);_stamp(record,prepared)
            if events['checked_post_windows']>=4:
                raise ValueError('POST_BUDGET_EXTENSION_FORBIDDEN')
            if clear_z is None and zero_count==2:
                raise ValueError('CLEAR_EVENT_REQUIRED_BEFORE_NEXT_WINDOW')
            if _int(record['window_index'])!=index:
                raise ValueError('CONTIGUOUS_WINDOW_INDEX_REQUIRED')
            first=boundary['end_step']+index*w+1
            end=boundary['end_step']+(index+1)*w
            if _int(record['start_step'])!=first or _int(record['end_step'])!=end:
                raise ValueError('CONTIGUOUS_STEP_WINDOW_REQUIRED')
            phase='UNLOADING' if clear_z is None else 'POST'
            _one(record['phase'],(phase,))
            _one(record['plate_mode'],('BOUND' if clear_z is None else 'CLEARED',))
            if _token(record['inventory_id'])!=boundary['inventory_id']:
                raise ValueError('INVENTORY_ID_MISMATCH')
            if _gravity(record['gravity'])!=prepared['gravity']:
                raise ValueError('EXPLICIT_GRAVITY_MISMATCH')
            _complete(record['complete'],'WINDOW_INCOMPLETE')
            lift=_int(record['lift_index'])
            if clear_z is None:
                if lift<last_lift or lift*prepared['increment']>prepared['cap']:
                    raise ValueError('H0_SCALED_LIFT_CAP_OR_ORDER')
                position=prepared['base_plate_z']+lift*prepared['increment']
            else:
                if lift!=last_lift:
                    raise ValueError('POST_LIFT_IDENTITY_MISMATCH')
                position=clear_z
            samples=record['samples']
            if type(samples) is not list:
                raise ValueError('EXACT_SAMPLE_LIST_REQUIRED')
            if len(samples)<w:
                raise _Outcome('INCOMPLETE','STEP_SAMPLES_MISSING')
            if len(samples)!=w:
                raise ValueError('EXTRA_STEP_SAMPLES')
            all_zero=True
            crossing=None
            for offset,sample in enumerate(samples):
                if type(sample) is not dict or any(type(k) is not str for k in sample):
                    raise ValueError('EXACT_SAMPLE_REQUIRED')
                required_observations={'contact_count','contacts_complete','inventory_complete','particles'}
                if not required_observations.issubset(sample):
                    raise _Outcome('NOT_COMPUTED','REQUIRED_CONTACT_OR_INVENTORY_MISSING')
                _dict(sample,_SAMPLE)
                _complete(sample['contacts_complete'],'CONTACTS_INCOMPLETE')
                _complete(sample['inventory_complete'],'INVENTORY_INCOMPLETE')
                if sample['contact_count'] is None:
                    raise _Outcome('NOT_COMPUTED','CONTACT_COUNT_MISSING')
                count=_int(sample['contact_count'])
                if _int(sample['step'])!=first+offset:
                    raise ValueError('EXACT_STEP_SAMPLE_ORDER_REQUIRED')
                if _inventory(sample['particles'])!=prepared['inventory']:
                    raise ValueError('S0_PARTICLE_INVENTORY_MISMATCH')
                ke=_number(sample['ke'],nonnegative=True)
                height=_number(sample['surface_height'])
                pressure=_number(sample['pressure'])
                plate_z=Fraction(_number(sample['plate_z']))
                if plate_z!=position:
                    raise ValueError('DECLARED_PLATE_POSITION_MISMATCH')
                if Fraction(ke)>prepared['max_ke']:
                    raise _Outcome('NOT_CONVERGED','TOY_KE_BUDGET_EXCEEDED')
                all_zero=all_zero and count==0
                if clear_z is not None:
                    if count!=0:
                        raise ValueError('POST_CONTACT_REAPPEARED')
                    post_heights.append(Fraction(height))
                if phase=='UNLOADING' and crossing is None and Fraction(pressure)<=prepared['threshold']:
                    crossing=dict(step=first+offset,window_index=index)
            if events.get('first_pressure_crossing') is None and crossing is not None:
                events['first_pressure_crossing']=crossing
            if clear_z is None:
                zero_count=zero_count+1 if all_zero else 0
                last_lift=lift
                previous_z=position
                if zero_count==2:
                    events['second_zero_window_end']=dict(window_index=index,step=end)
            else:
                if max(post_heights)-min(post_heights)>prepared['max_surface_drift']:
                    raise _Outcome('NOT_CONVERGED','TOY_SURFACE_DRIFT_BUDGET_EXCEEDED')
                events['checked_post_windows']+=1
                if events['checked_post_windows']==4:
                    events['post_end']=dict(window_index=index,step=end)
            index+=1
        if clear_z is None or events['checked_post_windows']!=4:
            return _report('INCOMPLETE','SEPARATION_OR_POST_BUDGET_INCOMPLETE',events=events)
        return _report('SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE','SYNTHETIC_SEQUENCE_AND_TOY_LIMITS_ONLY',events=events)
    except _Outcome as error:
        return _report(error.status,error.args[0],events=events)
    except (KeyError,TypeError,ValueError,OverflowError,RecursionError):
        return _report('REJECTED','INVALID_NATIVE_P2_TRACE_OR_SOURCE',events=events)
