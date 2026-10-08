"""Owned inert control fixtures; no candidate import and no OS/native operations.

AUTH01's single registered input enters actual execute_once. Its actual internal
authorization return is observed as the first inert adapter argument. All method
names and all fourteen events are declared below. Fixture approval objects are
synthetic data only, never files at operational approval/runtime paths.
"""
from copy import deepcopy
from hashlib import sha256
import json


def canonical(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def identity(name, digit):
    return {'path': 'fixture://S1O_CONTROL/' + name, 'bytes': 1, 'sha256': digit * 64}


def authorization_fixture():
    engines = [identity('engine-not-executable', '1')]
    dependencies = [identity('dependency-not-imported', '2')]
    policy = {'changes_allowed': False, 'source_prefs': identity('prefs-not-read', '3')}
    unit = {'run_id': 'FIXTURE_NO_NATIVE', 'variant_id': 'P0',
            'sigma_short_S_m': '1.7e-6', 'initialization_id': 'FIXTURE_ONLY',
            'physical_window_s': [0, 120],
            'commands': {'status': 'NATIVE_COMMANDS_FROZEN', 'cwd': 'fixture://cwd',
                         'argv': ['INERT_NO_EXEC'], 'parent_argv': ['INERT_NO_PARENT'],
                         'native_compile_argv': ['INERT_NO_COMPILE'],
                         'native_batch_argv': ['INERT_NO_BATCH'], 'native_cwd': 'fixture://cwd'},
            'paths': {'status': 'FROZEN_NATIVE_PATHS', 'source_root': 'fixture://source',
                      'proposed_native_root': 'fixture://no-runtime',
                      'must_be_absent': ['fixture://never-created'],
                      'approval_path': 'fixture://no-approval', 'release_path': 'fixture://no-release',
                      'user_decision_path': 'fixture://no-user-decision'},
            'counts': {'compile': 1, 'batch': 1, 'solve': 1, 'control': 0, 'retry': 0,
                       'separate_initialization_solve': 0, 'fresh_direct_challenges': 2},
            'resource_contract_sha256': '4' * 64,
            'phase_limits_s': {'native': 7200, 'cleanup': 120}, 'overall_limit_s': 9000}
    binding = {'schema': 'S1O_EXECUTION_BINDING_V1', 'native_ready': True,
               'adapter_status': 'IMPLEMENTED_VALIDATED_ACCEPTED', 'open_blockers': [],
               'unit': unit, 'engine_pins': engines, 'dependency_pins': dependencies,
               'policy_pin': policy}
    manifest = {'schema': 'S1O_CODE_MANIFEST_V1', 'native_ready': True,
                'files': [identity('candidate-not-loaded', '5')]}
    acceptance = {'status': 'ACCEPTED_CHANGED_BRANCH_VALIDATION',
                  'manifest_sha256': '6' * 64, 'execution_binding_sha256': canonical(binding),
                  'evidence_sha256': '7' * 64}
    approval = {'approved': True, 'usable': True, 'kind': 'SEPARATE_NATIVE_ONE_RUN_APPROVAL',
                'manifest_sha256': '6' * 64, 'execution_binding_sha256': canonical(binding),
                'validation_evidence_sha256': '7' * 64, 'user_statement_sha256': '8' * 64,
                'unit': deepcopy(unit), 'policy_pin': deepcopy(policy)}
    observed = {'manifest_sha256': '6' * 64, 'payload': deepcopy(manifest['files']),
                'engines': deepcopy(engines), 'dependencies': deepcopy(dependencies),
                'cwd': unit['commands']['cwd'], 'argv': deepcopy(unit['commands']['argv']),
                'path_absence': deepcopy(unit['paths']['must_be_absent']), 'path_collisions': [],
                'path_resolution': 'NO_REPARSE_NO_ESCAPE', 'pending_owned_runs': [],
                'other_comsol_work': [], 'policy': deepcopy(policy), 'elevated': False,
                'attempt_history': [], 'adapter_identity_verified': True,
                'resource_enforcement_ready': True}
    return {'binding': binding, 'manifest': manifest, 'acceptance': acceptance,
            'approval': approval, 'observed': observed}


def rebind(args):
    """Declared pure fixture derivations for mutations of a binding leaf."""
    args['approval']['unit'] = deepcopy(args['binding']['unit'])
    args['approval']['policy_pin'] = deepcopy(args['binding']['policy_pin'])
    args['observed']['policy'] = deepcopy(args['binding']['policy_pin'])
    digest = canonical(args['binding'])
    args['acceptance']['execution_binding_sha256'] = digest
    args['approval']['execution_binding_sha256'] = digest


EXPECTED_ADAPTER_EVENTS = [
    'recheck_authorization_readonly', 'create_exclusive_evidence_and_reserve_one_attempt',
    'obtain_two_fresh_direct_user_challenges_same_python', 'stage_exact_authorized_bytes_and_prefs_copy',
    'require_previous_owned_job_empty', 'require_time_and_resources_with_stop_reserve:compile',
    'run_one_monitored_owned_phase:compile', 'require_previous_owned_job_empty',
    'require_time_and_resources_with_stop_reserve:batch', 'run_one_monitored_owned_phase:batch',
    'require_time_for_analysis_and_delivery', 'analyze_existing_evidence_once',
    'verify_owned_cleanup_and_preservation', 'final_write_readback_postwrite_budget']


class InertAdapter:
    """Only recorded in-memory calls; never delegates to any native implementation."""
    def __init__(self):
        self.events = []
        self.actual_authorization = None

    def mark(self, name):
        self.events.append(name)

    def recheck_authorization_readonly(self, auth):
        self.mark('recheck_authorization_readonly')
        self.actual_authorization = deepcopy(auth)

    def create_exclusive_evidence_and_reserve_one_attempt(self, auth):
        self.mark('create_exclusive_evidence_and_reserve_one_attempt')

    def obtain_two_fresh_direct_user_challenges_same_python(self, auth):
        self.mark('obtain_two_fresh_direct_user_challenges_same_python')

    def stage_exact_authorized_bytes_and_prefs_copy(self, auth):
        self.mark('stage_exact_authorized_bytes_and_prefs_copy')

    def require_previous_owned_job_empty(self, auth):
        self.mark('require_previous_owned_job_empty')

    def require_time_and_resources_with_stop_reserve(self, auth, phase):
        self.mark('require_time_and_resources_with_stop_reserve:' + phase)

    def run_one_monitored_owned_phase(self, auth, phase):
        self.mark('run_one_monitored_owned_phase:' + phase)
        return {'rc': 0, 'record_errors': [], 'cleanup': 'PASS', 'within_limits': True,
                'fixture_only': True, 'real_process_started': False}

    def require_time_for_analysis_and_delivery(self, auth):
        self.mark('require_time_for_analysis_and_delivery')

    def analyze_existing_evidence_once(self, auth):
        self.mark('analyze_existing_evidence_once')
        return {'fixture_only': True, 'candidate_consumer_called': False}

    def verify_owned_cleanup_and_preservation(self, auth):
        self.mark('verify_owned_cleanup_and_preservation')
        return 'PASS'

    def final_write_readback_postwrite_budget(self, auth, result):
        self.mark('final_write_readback_postwrite_budget')
        return {'fixture_only': True, 'actual_write_performed': False}


def resource_fixture():
    limits = {'maximum_sample_gap_s': 6, 'maximum_sampling_duration_s': 1,
              'rss_early_stop_bytes': 8589934592, 'commit_early_stop_bytes': 10737418240,
              'output_early_stop_bytes': 5368709120, 'host_commit_reserve_bytes': 2147483648,
              'host_ram_reserve_bytes': 2147483648, 'volume_free_reserve_bytes': 8589934592,
              'native_wall_limit_s': 7200, 'overall_wall_limit_s': 9000, 'stop_reserve_s': 120}
    ownership = {'status': 'VERIFIED_PRIVATE_JOB', 'assigned_before_resume': True,
                 'identity_fresh': True, 'job_identity': 'fixture-private-job',
                 'root_pid': 100, 'root_creation_filetime': 1,
                 'member_pid_creation_pairs': [[100, 1]]}
    sample = {'status': 'MEASURED', 'counter_errors': [],
              'scope': 'EXACT_PRIVATE_JOB_MEMBERS_PLUS_OWNED_OUTPUT_TREE',
              'job_identity': 'fixture-private-job',
              'rss_aggregation': 'SUM_UNIQUE_MEMBER_WORKING_SETS_NO_JOB_TOTAL_ADD',
              'commit_aggregation': 'JOB_ACCOUNTING_TOTAL_NO_MEMBER_TOTAL_ADD',
              'monotonic_s': 100, 'native_elapsed_s': 10, 'overall_elapsed_s': 20,
              'sample_gap_s': 5, 'sampling_duration_s': 0.1, 'job_rss_bytes': 1073741824,
              'job_private_commit_bytes': 2147483648, 'host_commit_available_bytes': 4294967296,
              'host_available_ram_bytes': 4294967296, 'owned_output_growth_bytes': 0,
              'volume_free_bytes': 17179869184}
    return {'sample': sample, 'ownership': ownership, 'contract': {'proposal_limits': limits}}


def stop_fixture():
    return {'state': {'status': 'STOP_REQUESTED', 'last_monotonic_s': 0,
                      'cleanup_deadline_s': 120, 'overall_deadline_s': 1000},
            'event': {'monotonic_s': 10, 'ownership_verified': True, 'job_empty': True,
                      'root_signaled': True, 'exit_query_succeeded': True,
                      'remaining_members': [], 'unattributed_processes': [], 'handle_errors': [],
                      'force_attempts': 1, 'force_call_succeeded': True},
            'capabilities': {'cooperative_stop': 'SUPPORTED_VERIFIED', 'cooperative_wait_s': 15,
                             'force_verify_reserve_s': 90, 'force_only_explicitly_approved': False}}


def control_input_definitions():
    """Own static fixture construction only; never calls or imports candidate code."""
    records = {}
    def add(cid, args, route, expected, detail=None, mutation=None, control=None):
        records[cid] = {'id': cid, 'input_id': cid + ':01', 'fixture_only': True,
                        'route': route, 'arguments': args, 'expected': expected,
                        'expected_detail': detail, 'mutation_leaves': mutation or [],
                        'positive_control_case_id': control or ('AUTH01' if cid.startswith('AUTH') else 'RESOURCE01'),
                        'real_native_calls': 0, 'actual_user_input_calls': 0}
    reasons = {2: 'SEPARATE_NATIVE_APPROVAL_REQUIRED', 3: 'SOURCE_IDENTITY',
               4: 'ENGINE_OR_DEPENDENCY_IDENTITY', 5: 'VALIDATION_ACCEPTANCE_BINDING',
               6: 'APPROVED_RUN_UNIT_MISMATCH', 7: 'CALL_COUNTS_NOT_APPROVED',
               8: 'COMMAND_OR_CWD_MISMATCH', 9: 'PATH_OR_CONCURRENT_WORK',
               10: 'POLICY_OR_PRIVILEGE_MISMATCH', 11: 'NO_RETRY_EXISTING_ATTEMPT',
               12: 'OFFLINE_NATIVE_NOT_READY', 13: 'NATIVE_COMMANDS_UNRESOLVED',
               14: 'NATIVE_PATHS_UNRESOLVED', 15: 'CURRENT_POLICY_PIN_UNRESOLVED'}
    mutations = {2: ['approval={}; empty object preserves object-type gate'],
                 3: ['observed.payload[0].sha256'], 4: ['observed.engines[0].sha256'],
                 5: ['acceptance.manifest_sha256'], 6: ['approval.unit.sigma_short_S_m'],
                 7: ['binding.unit.counts.solve', 'derived approval.unit', 'derived binding digest pins'],
                 8: ['observed.cwd'], 9: ['observed.path_collisions'], 10: ['observed.elevated'],
                 11: ['observed.attempt_history'], 12: ['manifest.native_ready'],
                 13: ['binding.unit.commands.native_compile_argv', 'derived approval.unit', 'derived binding digest pins'],
                 14: ['binding.unit.paths.proposed_native_root', 'derived approval.unit', 'derived binding digest pins'],
                 15: ['binding.policy_pin', 'derived approval/observed policy', 'derived binding digest pins']}
    for i in range(1, 16):
        a = authorization_fixture()
        if i == 2: a['approval'] = {}
        if i == 3: a['observed']['payload'][0]['sha256'] = '9' * 64
        if i == 4: a['observed']['engines'][0]['sha256'] = '9' * 64
        if i == 5: a['acceptance']['manifest_sha256'] = '9' * 64
        if i == 6: a['approval']['unit']['sigma_short_S_m'] = '1.7e-7'
        if i == 7: a['binding']['unit']['counts']['solve'] = 2; rebind(a)
        if i == 8: a['observed']['cwd'] = 'fixture://wrong-cwd'
        if i == 9: a['observed']['path_collisions'] = ['fixture://never-created']
        if i == 10: a['observed']['elevated'] = True
        if i == 11: a['observed']['attempt_history'] = ['fixture-prior-attempt']
        if i == 12: a['manifest']['native_ready'] = False
        if i == 13: a['binding']['unit']['commands']['native_compile_argv'] = None; rebind(a)
        if i == 14: a['binding']['unit']['paths']['proposed_native_root'] = None; rebind(a)
        if i == 15: a['binding']['policy_pin'] = None; rebind(a)
        add(f'AUTH{i:02d}', a, 'execute_once' if i == 1 else 'authorize_execution',
            'AUTHORIZED_ONE_RUN' if i == 1 else reasons[i],
            {'actual_authorization_status': 'AUTHORIZED_ONE_RUN', 'adapter_events': EXPECTED_ADAPTER_EVENTS} if i == 1 else {'exception_stage': 'authorization'},
            mutations.get(i, []))
    for i in range(1, 9):
        a = resource_fixture(); details = []; leaf = []
        if i == 2: del a['sample']['job_rss_bytes']; details = ['COUNTER_MISSING_OR_NONFINITE:job_rss_bytes']; leaf = ['sample.job_rss_bytes removed']
        if i == 3: a['sample']['job_rss_bytes'] = {'fixture_float': 'NaN'}; details = ['COUNTER_MISSING_OR_NONFINITE:job_rss_bytes']; leaf = ['sample.job_rss_bytes tagged NaN; decode this leaf only']
        if i == 4: a['ownership']['status'] = 'UNVERIFIED'; details = ['OWNERSHIP_UNVERIFIED']; leaf = ['ownership.status']
        if i == 5: a['sample']['rss_aggregation'] = 'SUM_MEMBERS_PLUS_JOB_TOTAL'; details = ['RSS_DOUBLE_COUNT_OR_UNKNOWN']; leaf = ['sample.rss_aggregation']
        if i == 6: a['sample']['job_rss_bytes'] = 8589934593; details = ['RESOURCE_THRESHOLD:job_rss_bytes']; leaf = ['sample.job_rss_bytes']
        if i == 7: a['sample']['sample_gap_s'] = 6.0001; details = ['RESOURCE_THRESHOLD:sample_gap_s']; leaf = ['sample.sample_gap_s']
        if i == 8: a['sample']['native_elapsed_s'] = 7080.0001; details = ['STOP_RESERVE_ENTERED:native_elapsed_s']; leaf = ['sample.native_elapsed_s']
        add(f'RESOURCE{i:02d}', a, 'assess_resources', 'CONTINUE_WITHIN_SAMPLED_LIMITS' if i == 1 else 'STOP_REQUIRED', {'reasons': details}, leaf)
    for i in range(9, 16):
        a = stop_fixture(); detail = {}; leaf = []
        if i in (10, 11):
            a['capabilities']['cooperative_stop'] = 'UNAVAILABLE'
            a['capabilities']['force_only_explicitly_approved'] = i == 11
            leaf = ['capabilities.cooperative_stop', 'capabilities.force_only_explicitly_approved']
        if i == 12: a['state'].update(status='WAITING_COOPERATIVE', wait_until_s=10); a['event'].update(job_empty=False, root_signaled=False); leaf = ['state.status', 'state.wait_until_s', 'event.job_empty', 'event.root_signaled']
        if i == 13: a['state']['status'] = 'FORCE_PENDING'; leaf = ['state.status']
        if i in (14, 15): a['state']['status'] = 'VERIFY_PENDING'; leaf = ['state.status']
        if i == 14: a['event']['remaining_members'] = [[100, 1]]; leaf += ['event.remaining_members']
        expected = {9:'WAITING_COOPERATIVE',10:'UNRESOLVED',11:'FORCE_PENDING',12:'FORCE_PENDING',13:'VERIFY_PENDING',14:'UNRESOLVED',15:'TERMINATED_VERIFIED'}[i]
        action = {9:'REQUEST_COOPERATIVE_ONCE',10:'NONE',11:'FORCE_OWNED_JOB_ONCE',12:'FORCE_OWNED_JOB_ONCE',13:'VERIFY_TERMINATION',14:'NONE',15:'CLOSE_OWNED_HANDLES_AND_RECORD'}[i]
        detail = {'next_action': action}
        if i == 9: detail['wait_until_s'] = 25
        if i == 10: detail['error'] = 'STOP_METHOD_NOT_APPROVED'
        if i == 11: detail['cooperative_status'] = 'UNAVAILABLE_DECLARED'
        if i == 14: detail['error'] = 'TERMINATION_UNCONFIRMED'
        ctrl = 'RESOURCE11' if i == 10 else ('RESOURCE15' if i == 14 else f'RESOURCE{i:02d}')
        add(f'RESOURCE{i:02d}', a, 'advance_stop', expected, detail, leaf, ctrl)
    a = authorization_fixture(); a['manifest']['native_ready'] = False
    add('RESOURCE16', a, 'execute_once', 'OFFLINE_NATIVE_NOT_READY',
        {'exception_stage':'authorization', 'adapter_events':[]}, ['manifest.native_ready'], 'AUTH01')
    return records


def execute_control_case(cid, ctl, descriptor):
    """One registered actual control input. Exceptions propagate to session driver."""
    get = (lambda name: ctl[name]) if isinstance(ctl, dict) else (lambda name: getattr(ctl, name))
    a = deepcopy(descriptor['arguments']); route = descriptor['route']
    if cid == 'RESOURCE03':
        assert a['sample']['job_rss_bytes'] == {'fixture_float':'NaN'}
        a['sample']['job_rss_bytes'] = float('nan')
    spy = InertAdapter()
    if route in ('authorize_execution', 'execute_once'):
        args = [a[k] for k in ('binding','manifest','acceptance','approval','observed')]
        if route == 'execute_once':
            try:
                actual = get(route)(*args, adapter=spy)
            except Exception as exc:
                if cid == 'RESOURCE16':
                    assert spy.events == [], 'unexpected inert event before authorization denial'
                    setattr(exc, 'fixture_adapter_events', list(spy.events))
                raise
        else:
            actual = get(route)(*args)
    elif route == 'assess_resources':
        actual = get(route)(a['sample'], a['ownership'], a['contract'])
    elif route == 'advance_stop':
        actual = get(route)(a['state'], a['event'], a['capabilities'])
    else:
        raise AssertionError('Unregistered control route ' + route)
    if cid == 'AUTH01':
        assert spy.events == EXPECTED_ADAPTER_EVENTS, spy.events
        assert spy.actual_authorization is not None
        assert spy.actual_authorization['status'] == 'AUTHORIZED_ONE_RUN'
        assert actual['errors'] == [] and actual['calls'] == {'compile':1,'batch':1}
        assert actual['process_cleanup'] == 'PASS'
        assert actual['native_completion'] == 'INCOMPLETE' and actual['overall'] == 'INCOMPLETE'
        observed = spy.actual_authorization['status']
    else:
        observed = actual['status']
        for key, value in (descriptor.get('expected_detail') or {}).items():
            assert actual.get(key) == value, (cid, key, actual.get(key), value)
    return {'observed': observed, 'stage': route, 'return_value': actual,
            'adapter_events': list(spy.events), 'actual_authorization': spy.actual_authorization,
            'expected_detail': descriptor.get('expected_detail'), 'fixture_only': True}
